"""No-charge packing, immutable text retention, and guard-stop continuation."""
import copy
import hashlib
import json

import pytest

from src.dossier.context_packing import input_chars, pack_final_context, expand_evidence_rows
from src.dossier.investigation import _spec
from tests.test_field_investigation_2026_09_09 import fixture, freeze, fake


def sample():
    prior = 'Original baseline memo with exact quotes.\n' * 1800
    primary = 'Complete primary-source reading.\n' * 1500
    evidence = [{'citation_id': 'referee:1/F1', 'source_role': 'field', 'quote_verified': True,
                 'source_quote': 'Exact field quote. ' * 2000, 'finding': 'Exact finding.'},
                {'citation_id': 'em:AAAAAA/F1', 'source_role': 'primary', 'quote_verified': True,
                 'source_quote': 'Exact primary quote. ' * 2000, 'finding': 'Exact author finding.'}]
    collection = {'query_id': 4, 'name': 'A collection', 'focus_statement': 'Its substantive scope.',
                  'seed_count': 100, 'seeds': [{'title': 'Full seed acquisition history ' * 5000}],
                  'pdf_status': {'enabled': True, 'stats': {'available': 46}, 'seeds': [{'status': 'history ' * 30000}]}}
    upstream = {'field_collections': [collection], 'field_map': 'Entire source map. ' * 2000, 'evidence': evidence,
                'prior_context': [{'key': 'prior', 'kind': 'prior_investigations', 'title': 'Original memo',
                                   'text': prior, 'inspected_ranges': [[0, len(prior)]], 'truncated': False,
                                   'total_chars': len(prior), 'matched_queries': ['organization'], 'large_search_metadata': 'x' * 20000}],
                'adjudication': 'Complete adjudication. ' * 1000, 'previous_draft': 'Complete previous draft. ' * 1000,
                'validation_errors': {'unsupported': ['referee:1/missing']}}
    readings = [{'uid': 'em:AAAAAA', 'title': 'Source title', 'reading': primary, 'inspected_ranges': [[0, 30]],
                 'reading_mode': 'windows', 'source_metadata': {'uid': 'em:AAAAAA', 'body_sha256': 'a'*64,
                    'date_scope': 'in_scope', 'read_uid': 'reading:AAAAAA', 'acquisition_history': 'p' * 30000}}]
    return [_spec('field-argument-map', upstream['field_map']), _spec('primary-readings', json.dumps(readings))], upstream


def test_packing_retains_all_quotes_texts_drafts_and_full_omitted_metadata():
    sources, upstream = sample(); original = copy.deepcopy((sources, upstream))
    packed_sources, packed, manifest = pack_final_context('memo:repair', sources, upstream, packet_sha256='f'*64)
    assert (sources, upstream) == original
    assert manifest['original_chars'] - manifest['packed_chars'] > 100000
    for key in ('evidence', 'adjudication', 'previous_draft', 'validation_errors'):
        assert packed[key] == upstream[key]
    reference = packed['prior_context'][0]['text']['context_source_key']
    context_source = next(s for s in packed_sources if s.key == reference)
    assert context_source.text == upstream['prior_context'][0]['text'] and context_source.role == 'plan'
    assert json.loads(packed_sources[1].text)[0]['reading'] == json.loads(sources[1].text)[0]['reading']
    assert packed_sources[0].text == upstream['field_map'] and 'field_map' not in packed
    assert packed['field_map_source'] == 'field-argument-map'
    assert packed['field_collections'][0]['focus_statement'] == upstream['field_collections'][0]['focus_statement']
    assert packed['field_collections'][0]['pdf_status']['stats'] == {'available': 46}
    for omission in manifest['omitted_metadata']:
        text = json.dumps(omission['value'], ensure_ascii=False)
        assert hashlib.sha256(text.encode()).hexdigest() == omission['sha256']
        assert len(text) == omission['chars'] and omission['also_retained_in']
    assert any(o['value'] == upstream['field_collections'][0]['seeds'] for o in manifest['omitted_metadata'])
    assert input_chars(packed_sources, packed) == manifest['packed_chars']


def test_compaction_is_deterministic_and_never_applied_to_reading_or_selection():
    sources, upstream = sample()
    assert pack_final_context('memo', sources, upstream, packet_sha256='f'*64) == pack_final_context('memo', sources, upstream, packet_sha256='f'*64)
    for stage in ('read:primary:em:AAAAAA', 'author_selection:1', 'field_map'):
        a, b, m = pack_final_context(stage, sources, upstream, packet_sha256='f'*64)
        assert a is sources and b is upstream and m is None


def test_only_exact_duplicate_named_map_is_removed():
    sources, upstream = sample(); sources[0].text += ' Distinct map text.'
    a, b, m = pack_final_context('adjudication', sources, upstream, packet_sha256='f'*64)
    assert b['field_map'] == upstream['field_map'] and a[0].text == sources[0].text
    assert 'field_map_source' not in b


def test_no_text_or_quote_truncation_when_inputs_still_exceed_limit():
    sources, upstream = sample(); upstream['previous_draft'] = 'A' * 900000
    a, b, m = pack_final_context('memo:repair', sources, upstream, packet_sha256='f'*64)
    assert b['previous_draft'] == upstream['previous_draft'] and b['evidence'] == upstream['evidence']
    assert input_chars(a,b) > 640000


def test_resume_after_old_guard_reuses_every_paid_call_and_source_window(monkeypatch):
    import src.dossier.context_packing as packing
    from src.dossier.field_investigation import run_field_investigation
    raw,_,_,_=fixture(primary_count=1)
    raw['field_collections'] = [{'name': 'Collection', 'seeds': [{'acquisition': 'x' * 155000}]}]
    _,packet,_,bodies=freeze(raw)
    calls, saves = [], []
    base = fake(calls)
    def call(key, sources, **kw):
        result = base(key,sources,**kw)
        if key.endswith('_author_read'):
            result['prose'] = result['final_output'] = 'P' * 500000
        return result
    original = packing.pack_final_context
    monkeypatch.setattr(packing,'pack_final_context',lambda stage,sources,upstream,**kw:(sources,upstream,None))
    with pytest.raises(ValueError,match='input is'):
        run_field_investigation(packet,bodies,call=call,save=lambda s:saves.append(copy.deepcopy(s)))
    before=saves[-1]; assert before['paused_reason']=='input_limit' and before['running_stage'] is None
    prior_calls=copy.deepcopy(before['calls']); ranges=copy.deepcopy(before['read_inputs']); count=len(calls)
    monkeypatch.setattr(packing,'pack_final_context',original)
    after=run_field_investigation(packet,bodies,call=call,save=lambda s:saves.append(copy.deepcopy(s)),state=before)
    assert after['complete'] and after['read_inputs']==ranges
    assert all(after['calls'][key]==value for key,value in prior_calls.items())
    assert len(calls)-count == 2
    assert after['cost_usd'] == pytest.approx(len(after['calls'])*0.1)
    manifest=after['call_input_manifests']['adjudication']
    assert manifest['packing']['original_chars']>640000 and manifest['chars']<640000
    assert manifest['evidence_representation']=='verified_quotations'
    assert manifest['packing']['all_evidence_quotes_and_findings_retained'] is True
    assert not manifest['packing']['field_reference_fallback_applied']
    supplied=next(c[2] for c in calls if c[0].endswith('_adjudicate'))
    assert all('source_quote' in e for e in supplied['evidence'])
    run_field_investigation(packet,bodies,call=lambda *a,**kw:pytest.fail('paid replay'),save=lambda s:None,state=after)


def test_prior_metadata_table_is_lossless_and_large_memo_stays_non_anchor_context():
    sources, upstream = sample()
    original = upstream['prior_context'][0]
    upstream['prior_context'] = [{**original, 'key': f'prior-{i}', 'text': original['text'] if i==0 else 'Exact short text.'} for i in range(40)]
    a,b,manifest = pack_final_context('memo',sources,upstream,packet_sha256='f'*64)
    table=b['prior_context']; assert isinstance(table,dict)
    restored=[dict(zip(table['fields'],row)) for row in table['rows']]
    for old,new in zip(upstream['prior_context'],restored):
        assert new['title']==old['title'] and new['inspected_ranges']==old['inspected_ranges']
        text=new['text']
        if isinstance(text,dict):
            source=next(s for s in a if s.key==text['context_source_key'])
            assert source.role=='plan'; text=source.text
        assert text==old['text']
    assert len(restored)==40


def test_grouped_evidence_preserves_quotes_speakers_missing_fields_and_source_order():
    sources, upstream = sample()
    upstream['evidence'] = [
        {'uid':f'source:{i%3}', 'citation_id':f'source:{i%3}/F{i}', 'source_role':'field' if i%3 else 'primary',
         'title':f'Complete title {i%3}', 'source_quote':f'Exact quotation {i}.\nIncluding punctuation—unchanged.',
         'finding':f'A distinct finding {i}.', 'quote_verified':bool(i%4),
         'fields':{'speaker':f'Speaker {i%3}', 'locus':f'page {i}', 'uid':f'source:{i%3}'},
         **({'year':None} if i%2 else {})} for i in range(90)]
    upstream['evidence'][4]['fields'].pop('locus')
    original = copy.deepcopy(upstream['evidence'])
    _, packed, receipt = pack_final_context('adjudication',sources,upstream,packet_sha256='f'*64)
    assert packed['evidence']['format'] == 'grouped_evidence_v1'
    assert expand_evidence_rows(packed['evidence']) == original == upstream['evidence']
    assert len(json.dumps(packed['evidence'])) < len(json.dumps(original))
    assert receipt['evidence_record_encoding'] == 'grouped_evidence_v1'
    assert receipt['evidence_sha256'] == hashlib.sha256(json.dumps(original,ensure_ascii=False).encode()).hexdigest()


def test_final_registry_archive_keeps_classification_proofs_and_live_references():
    sources, upstream = sample()
    identity={'hostname':'institute.example','name':'Institute','identity_evidence':{
        'classification':'think_tank','quote':'An independent research institute.', 'reason':'Explicit original description.',
        'original':{'url':'https://institute.example/about','text':'Full identity page ' * 3000}}}
    upstream['institutional_metadata_records']={'orphan':identity,'still-used':{'complete':'Retained record'}}
    upstream['field_collections'][0].update(institutional_context={'plan':{'registry_records':[{'institutional_metadata_ref':'orphan'}],'search_outcomes':{'institute.example':3}},'coverage':[{'name':'Institute','searched':True}]},
        discovery_context={'identity_method_snapshot':{'version':1,'body':'Frozen method'},'report':{'leads':7},'usage':{'cost_usd':1}})
    upstream['explicit_identity']={'institutional_metadata_ref':'still-used'}
    original = copy.deepcopy(upstream)
    _, packed, receipt = pack_final_context('memo',sources,upstream,packet_sha256='f'*64)
    assert upstream == original
    assert packed['institutional_metadata_records'] == {'still-used':{'complete':'Retained record'}}
    proof=packed['institution_classification_receipts'][0]['identity_evidence']
    assert proof['quote'] == identity['identity_evidence']['quote'] and proof['classification']=='think_tank'
    assert proof['original']['url'] == identity['identity_evidence']['original']['url']
    assert 'text' not in proof['original'] and proof['original']['text_sha256']
    context=packed['field_collections'][0]['institutional_context']
    assert context['coverage']==original['field_collections'][0]['institutional_context']['coverage']
    assert context['plan']['search_outcomes']=={'institute.example':3}
    assert any(o['path']=='institutional_metadata_records.orphan' and o['value']==identity for o in receipt['omitted_metadata'])
    assert any(o['path'].endswith('identity_method_snapshot') and o['value']=={'version':1,'body':'Frozen method'} for o in receipt['omitted_metadata'])


def test_repeated_baseline_memo_is_supplied_once_with_exact_reconstructable_values():
    sources, upstream = sample()
    memo='A complete memo with its source quotations.\n' * 400
    records=[{'id':4,'memo':memo,'argument_map':'The complete map.'}, {'id':4,'memo':memo,'extra':'A distinct retained qualification.'}]
    original='[SOURCE CHARACTERS 0:100000]\n'+json.dumps(records,ensure_ascii=False)
    upstream['prior_context'][0]['text']=original
    packed_sources, packed, receipt=pack_final_context('memo',sources,upstream,packet_sha256='f'*64)
    source=next(s for s in packed_sources if s.key.startswith('prior-context-text:'))
    data=json.loads(source.text.split('\n',1)[1])
    assert data['format']=='shared_prior_text_v1' and list(data['texts'].values())==[memo]
    restored=[]
    for record in data['records']:
        restored.append({k:data['texts'][v['retained_text_ref']] if isinstance(v,dict) and 'retained_text_ref' in v else v for k,v in record.items()})
    assert restored==records and source.role=='plan'
    assert any(o['value']==original for o in receipt['omitted_metadata'])
    assert upstream['prior_context'][0]['text']==original
