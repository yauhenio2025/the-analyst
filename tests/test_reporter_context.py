import copy
import json

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
