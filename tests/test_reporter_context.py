import copy
import json
import pytest

from src.dossier.reporter_context import pack_reporter_context
from src.dossier.investigation import _spec
from src.dossier.field_investigation import run_field_investigation
from tests.test_field_investigation_2026_09_09 import fixture, freeze, fake


def reporter_row():
    spans = [{"char_start": 0, "char_end": 18, "start_seconds": 1.2, "end_seconds": 4.6,
              "speaker": None, "role": "unattributed", "text": "Original testimony",
              "raw_text": "Original testimony", "snapshot_passage_url": "https://example.org/" + "x" * 700000}]
    return {"uid": "reporter:panel", "passage_spans": spans, "source_metadata": {
        "provider": "reporter", "source_format": "video", "speakers": [], "completeness": "partial",
        "gaps": ["Speaker unknown"], "spans": spans,
        "provenance": {"generated": True, "language": "en", "segments": ["raw caption archive"],
                       "transcript_spans": spans}}}


def test_media_reader_preserves_original_text_and_exact_attribution_in_small_context():
    sources = [_spec('field:reporter:panel', 'Original testimony')]
    upstream = {"field_collections": [{"kind": "reporter"}], "source_metadata": reporter_row(),
                "evidence": [{"source_quote": "Unchanged verified quote"}]}
    before = copy.deepcopy((sources, upstream))
    a,b,receipt = pack_reporter_context('field_read:reporter:panel', sources, upstream, packet_sha256='f'*64)
    assert (sources, upstream) == before and a == sources
    assert b['evidence'] == upstream['evidence']
    native=b['source_metadata']['source_metadata']
    span=dict(zip(native['native_passages']['fields'],native['native_passages']['rows'][0]))
    assert span['speaker'] is None and span['role']=='unattributed'
    assert (span['char_start'],span['char_end'],span['start_seconds'],span['end_seconds'])==(0,18,1.2,4.6)
    assert native['completeness']=='partial' and native['gaps']==['Speaker unknown']
    assert native['provenance']=={'generated':True,'language':'en'}
    assert receipt['packed_chars'] < 5000 and receipt['original_chars'] > 640000
    archived={o['path']:o['value'] for o in receipt['omitted_metadata']}
    assert archived['source_metadata.source_metadata.spans']==upstream['source_metadata']['source_metadata']['spans']


def test_planner_only_removes_exact_duplicate_metadata_already_in_packet():
    common={'question':'The exact question', 'scope':{'instructions':'Preserve this distinction'},
            'field_collections':[{'kind':'reporter'}], 'field_gaps':[{'message':'Unavailable'}]}
    a,b,r=pack_reporter_context('plan',[_spec('investigation-question',json.dumps(common))],common,packet_sha256='f'*64)
    question=json.loads(a[0].text)
    assert b==common and question=={k:v for k,v in common.items() if k not in ('field_collections','field_gaps')}
    distinct={**common,'field_gaps':[{'message':'A distinct caveat'}]}
    a,_,_=pack_reporter_context('plan',[_spec('investigation-question',json.dumps(distinct))],common,packet_sha256='f'*64)
    assert json.loads(a[0].text)['field_gaps']==distinct['field_gaps']


def test_media_collection_completes_all_stages_and_retains_native_metadata_on_resume():
    raw,_,_,_=fixture(primary_count=1)
    raw['field_collections']=[{'kind':'reporter'}]
    raw['field'][0].update(reporter_row())
    _,packet,_,bodies=freeze(raw)
    calls=[]
    state=run_field_investigation(packet,bodies,call=fake(calls),save=lambda _:None)
    assert state['complete']
    reading=next(r for r in state['readings'] if r['uid']=='reporter:panel')
    assert reading['source_metadata']['source_metadata']==raw['field'][0]['source_metadata']
    assert any('reporter_packing' in r for r in state['call_input_manifests'].values())
    for key,_,upstream,sources in calls:
        if key.endswith('_field_map') and sources[0].key=='field-readings':
            for row in json.loads(sources[0].text):
                assert row['reading']['reading']=='A complete source reading.'
                assert row['evidence']
    def forbidden(*args,**kwargs):
        raise AssertionError('Completed paid call must not replay')
    assert run_field_investigation(packet,bodies,call=forbidden,save=lambda _:None,state=state)['complete']


def test_final_coverage_references_only_exact_duplicate_gap_records():
    gaps=[{'uid':f'reporter:{i}','message':'This source was not acquired. ' * 10} for i in range(400)]
    upstream={'field_collections':[{'kind':'reporter'}], 'field_gaps':gaps,
              'coverage':{'field_gaps':copy.deepcopy(gaps),'read_count':27},
              'evidence':[{'source_quote':'Exact quotation','finding':'Exact supported finding'}]}
    a,b,receipt=pack_reporter_context('adjudication',[],upstream,packet_sha256='f'*64)
    assert b['field_gaps']==gaps and b['evidence']==upstream['evidence']
    assert 'field_gaps' not in b['coverage'] and b['coverage']['read_count']==27
    assert receipt['original_chars']-receipt['packed_chars']>100000
    assert receipt['omitted_metadata'][0]['value']==gaps
    upstream['coverage']['field_gaps'].append({'message':'A distinct caveat'})
    a,b,receipt=pack_reporter_context('memo',[],upstream,packet_sha256='f'*64)
    assert b==upstream and receipt is None


@pytest.mark.parametrize('stage', ['memo', 'memo_repair'])
def test_institutional_final_and_repair_inputs_factor_identical_registry_originals_losslessly(stage):
    record = {'hostname':'institute.example','identity_evidence':{'original':{'url':'https://institute.example/about','text':'Policy research institute. ' * 1500}}}
    upstream = {'field_collections':[{'kind':'reporter','institutional_context':{'plan':{'registry_records':[record]}}}],
                'evidence':[{'source_quote':'Unchanged signed claim.','finding':'Explicit disagreement.'}]}
    readings = [{'reading':{'reading':'A complete source reading.', 'source_metadata':{'source_metadata':{'provider':'reporter',
                'institutional_admission':{'institutions':[{'registry_record':record}]}}}},'evidence':[{'source_quote':'Unchanged signed claim.'}]} for _ in range(12)]
    sources = [_spec('field-readings',json.dumps(readings)), _spec('field-original','Unchanged original source body.')]
    a,b,receipt = pack_reporter_context(stage,sources,upstream,packet_sha256='f'*64)
    assert receipt['original_chars'] - receipt['packed_chars'] > 350000
    assert a[1].text == sources[1].text and b['evidence'] == upstream['evidence']
    assert list(b['institutional_metadata_records'].values()) == [record]
    restored = json.loads(a[0].text)
    for row in restored:
        assert row['reading']['reading'] == 'A complete source reading.'
        assert row['evidence'] == [{'source_quote':'Unchanged signed claim.'}]
        ref = row['reading']['source_metadata']['source_metadata']['institutional_admission']['institutions'][0]['registry_record']['institutional_metadata_ref']
        assert b['institutional_metadata_records'][ref] == record
    assert all(o.get('sha256') for o in receipt['omitted_metadata'])


@pytest.mark.parametrize('stage', ['read:reporter:pdf', 'memo', 'memo:repair'])
def test_large_institutional_pdf_preserves_originals_pages_and_identity_without_directory_profiles(stage):
    body = 'Exact acquired source paragraph.\n' * 10000
    pages = [{'page': 7, 'char_start': 0, 'char_end': len(body), 'text': body}]
    record = {'hostname': 'institute.example', 'name': 'Institute', 'country': 'France',
              'description': 'Directory selection context. ' * 5000, 'topics': ['Labour'],
              'business_model': 'Directory label', 'identity_evidence': {'quote': 'Independent policy research.'}}
    upstream = {'field_collections': [{'kind': 'reporter', 'institutional_context': {
        'plan': {'registry_records': [record], 'scope_excluded': [{'hostname': 'other.example', 'reason': 'Unknown identity'}]},
        'coverage': [{'hostname': 'institute.example', 'searched': True}]}}],
        'source_metadata': {'source_metadata': {'provider': 'reporter', 'provenance': {'page_spans': pages}}},
        'evidence': [{'source_quote': 'Exact acquired source paragraph.', 'finding': 'A qualified claim.'}],
        'previous_draft': 'The complete paid draft.'}
    original = copy.deepcopy(upstream)
    sources = [_spec('field:reporter:pdf', body)]
    a, b, receipt = pack_reporter_context(stage, sources, upstream, packet_sha256='f'*64)
    assert upstream == original and a[0].text == body
    assert b['evidence'] == original['evidence'] and b['previous_draft'] == original['previous_draft']
    context = b['field_collections'][0]['institutional_context']
    assert context['coverage'] == original['field_collections'][0]['institutional_context']['coverage']
    assert context['plan']['registry_records'][0]['identity_evidence'] == record['identity_evidence']
    assert context['plan']['scope_excluded'][0]['reason'] == 'Unknown identity'
    assert b['source_metadata']['source_metadata']['provenance']['page_spans'] == [
        {'page': 7, 'char_start': 0, 'char_end': len(body)}]
    archived = {r['path']: r['value'] for r in receipt['omitted_metadata']}
    assert archived['source_metadata.source_metadata.provenance.page_spans'] == pages
    assert archived['field_collections[0].institutional_context.plan.registry_records[0].directory_profile']['description'] == record['description']
    assert receipt['packed_chars'] < 640000 < receipt['original_chars']


def test_bulky_provenance_records_stay_out_of_the_reading_input():
    from src.dossier.investigation import _spec
    from src.dossier.reporter_context import pack_reporter_context
    big = "x" * 900000
    span = {"char_start": 0, "char_end": 5, "text": "hello", "raw_text": "[...]", "speaker": "Speaker 1"}
    row = {"uid": "reporter:src_a", "title": "Odd Lots", "passage_spans": [span],
           "source_metadata": {"provider": "reporter", "uid": "reporter:src_a", "spans": [span],
                               "provenance": {"original_text": big, "transcript_spans": [{"t": 1}], "page_url": "https://omny.fm/x", "retrieval_receipts": [{"ok": True}]}}}
    upstream = {"field_collections": [{"kind": "reporter"}], "source_metadata": row}
    sources, packed, manifest = pack_reporter_context("read:field:reporter:src_a", [_spec("field:reporter:src_a", "hello world")], upstream, packet_sha256="0" * 64)
    prov = packed["source_metadata"]["source_metadata"]["provenance"]
    assert "original_text" not in prov and prov["original_text_omitted"]["chars"] > 900000 and prov["page_url"] == "https://omny.fm/x" and prov["retrieval_receipts"] == [{"ok": True}]
    assert {o["path"] for o in manifest["omitted_metadata"]} >= {"source_metadata.source_metadata.provenance.original_text", "source_metadata.source_metadata.provenance.transcript_spans"} or any("original_text" in o["path"] for o in manifest["omitted_metadata"])
    assert manifest["packed_chars"] < 5000 and manifest["original_chars"] > 900000
