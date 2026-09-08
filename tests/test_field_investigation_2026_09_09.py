"""Bilateral inquiry integration and source/budget/resume regressions; no paid calls."""
import copy
import json

import pytest

from src.dossier.field_investigation import run_field_investigation, validate_claims
from src.sources.field_investigation import expand_field_investigation


def fixture(field_count=2, primary_count=2, prior=True):
    raw = {"author": {"id": "riley-dylan", "name": "Riley, Dylan"}, "question": "How do organization and worker agency relate?",
           "primary": [{"uid": f"em:AUTHOR{i:02d}", "title": f"Author argument {i}", "year": 2022,
                        "profile": {"thesis": f"Collective organization argument {i}"},
                        "body": "Collective organization mediates agency. This is a bounded historical claim."} for i in range(primary_count)],
           "field": [{"uid": f"referee:{i}", "title": f"Field argument {i}", "authors": [f"Researcher {i}"], "year": 2024,
                      "referee_paper_id": i, "external_reference_id": f"referee:{i}", "pdf_url": f"https://example.org/{i}.pdf",
                      "body": "Workplace networks support mobilization. Political commitments differ.",
                      "page_spans": [{"page": 1, "start": 0, "end": 68}]} for i in range(field_count)],
           "limits": {"max_primary_texts": 2, "max_primary_chars": 20000}}
    if prior:
        raw['prior_investigations'] = [{"job_id": "first-memo", "memo": "Earlier account overgeneralized organizational weakness.",
                                       "sources": ["em:AUTHOR00"]}]
    return freeze(raw)


def freeze(raw):
    docs = expand_field_investigation(json.dumps(raw))
    return raw, json.loads(docs[-1].text), docs, {d.key: d.text for d in docs if d.role == 'source'}


def row(dim, **fields):
    return {"id": "E1.F1", "dim": dim, "doc": "investigation-question", "anchor": "", "fields": fields,
            "finding": "A bounded supported claim", "confidence": "high"}


def fake(calls, *, fail_stage=None, bad_memo=False, large_readings=False, select_last=False):
    failed = False
    def call(key, sources, *, packet, **kwargs):
        nonlocal failed
        calls.append((key, [s.key for s in sources], copy.deepcopy(packet), copy.deepcopy(sources)))
        assert sum(len(s.text) for s in sources) + len(json.dumps(packet)) < 650000
        if fail_stage and fail_stage == key and not failed:
            failed = True
            raise RuntimeError('simulated interruption')
        prose = 'A complete source reading.' + (' Detailed reading.' * 3000 if large_readings and key.endswith('_field_read') else '')
        if key.endswith('_plan'):
            rows = [row('query', query='organization')]
        elif key.endswith(('_field_read', '_author_read')):
            src = sources[0]
            uid = packet['source_metadata']['uid']
            r = row('evidence', uid=uid, relation='direct', speaker='source author')
            first_window = src.text.split('\n', 1)[1].split('\n\n')[0]
            quote = first_window.split('.')[0] + '.' if '.' in first_window else first_window[:80]
            r.update(doc=src.key, anchor=quote)
            rows = [r]
        elif key.endswith('_author_select'):
            items = json.loads(sources[0].text)
            if packet['selection_mode'] == 'reconcile':
                items = items[-packet['limits']['max_texts']:] if select_last else items[:packet['limits']['max_texts']]
            rows = [row('candidate', uid=item['inventory']['uid'], decision='read', reason='Field-guided relevance', priority='1') for item in items]
            for i, r in enumerate(rows):
                r['id'] = f'E1.F{i+1}'
        elif key.endswith('_field_map'):
            items = json.loads(sources[0].text)
            ev = packet.get('evidence') or [e for item in items for e in item['evidence']]
            ids = ';'.join(e['citation_id'] for e in ev if e['quote_verified'])
            rows = [row('debate', claim_kind='field_finding', evidence_ids=ids)]
        else:
            ev = packet['evidence']
            ids = ';'.join(e['citation_id'] for e in ev if e['quote_verified'])
            rows = [row('judgment' if key.endswith('_adjudicate') else 'answer', claim_kind='comparison', evidence_ids=ids)]
            if key.endswith('_memo'):
                rows += [{**row('revision', disposition='changed' if packet['mode'] == 'follow_up' else 'new',
                                baseline='prior' if packet['mode'] == 'follow_up' else 'standalone',
                                before='Provisional old view', after='Revised bounded view', evidence_ids=ids), 'id':'E2.F1'}]
                prose = f'The inquiry revises its scope [{ids.replace(";", "; ")}].'
                if bad_memo:
                    rows[0]['fields'].update(claim_kind='thinker_position', evidence_ids='referee:0/E1.F1')
        return {"engine_key": key, "rows": rows, "cost_usd": .1, "model": "fake", "wall": {"failed_ids": []},
                "calls": [{"input_tokens": 11, "output_tokens": 5}], "final_output": prose, "prose": prose}
    return call


def test_packet_preserves_roles_external_ids_pages_and_missing_inventory():
    raw, _, _, _ = fixture()
    raw['field'].append({'uid':'referee:missing','title':'Unavailable','body':''})
    _, packet, docs, bodies = freeze(raw)
    assert packet['field'][0]['body_sha256'] and packet['field'][0]['referee_paper_id'] == 0
    assert packet['field'][-1]['body_state'] == 'missing'
    assert docs[-1].role == 'plan' and docs[-1].key == 'investigation'
    assert bodies['field:referee:0'].startswith('Workplace')
    assert raw['field'][0]['body']
    from src.sources.resolve import resolve_sources
    from src.sources.schemas import SourceSpec
    assert resolve_sources([SourceSpec(kind='paste', role='field_investigation', text=json.dumps(raw))])[-1].role == 'plan'
    raw['field'][0]['page_spans'][0]['end'] = 9999
    with pytest.raises(ValueError, match='page spans'):
        freeze(raw)


def test_all_field_texts_read_before_selection_and_every_author_profile_judged():
    _, packet, _, bodies = fixture(field_count=47, primary_count=115)
    calls = []
    state = run_field_investigation(packet, bodies, call=fake(calls, select_last=True), save=lambda s:None)
    assert state['complete'] and len(state['triage']) == 115
    assert state['coverage']['field']['read_count'] == 47
    assert state['coverage']['primary']['read_count'] == 2
    assert state['selected_primary_uids'] == ['em:AUTHOR113', 'em:AUTHOR114']
    keys = [c[0] for c in calls]
    assert max(i for i,k in enumerate(keys) if k.endswith('_field_read')) < keys.index('field_investigation_author_select')
    assert state['coverage']['absence_claims_supported'] is False
    assert len(state['coverage']['primary']['unread_uids']) == 113
    field = next(e for e in state['evidence'] if e['source_role']=='field')
    assert field['quote_verified'] and field['pages']==[1] and field['page_urls']==['https://example.org/0.pdf#page=1']
    assert field['source_metadata']['external_reference_id']=='referee:0'


def test_standalone_has_new_position_without_fabricating_prior():
    _, packet, _, bodies = fixture(prior=False)
    state=run_field_investigation(packet,bodies,call=fake([]),save=lambda s:None)
    assert state['mode']=='standalone' and state['changes'][0]['fields']['baseline']=='standalone'
    assert state['changes'][0]['fields']['disposition']=='new'


def test_field_only_citations_cannot_support_thinker_attribution():
    _, packet, _, bodies = fixture()
    saves=[]
    with pytest.raises(ValueError, match='memo support'):
        run_field_investigation(packet,bodies,call=fake([],bad_memo=True),save=lambda s:saves.append(copy.deepcopy(s)))
    state=saves[-1]
    assert state['memo'] and not state['complete'] and state['readings'] and state['adjudication']
    assert not state['memo_validation']['claims']['supported']
    assert not validate_claims([row('answer',claim_kind='field_finding',evidence_ids='missing/E1.F1')],state['evidence'])['supported']


def test_cached_calls_ranges_quotes_and_cost_survive_resume():
    _,packet,_,bodies=fixture()
    saves,calls=[],[]
    engine=fake(calls,fail_stage='field_investigation_adjudicate')
    with pytest.raises(RuntimeError,match='interruption'):
        run_field_investigation(packet,bodies,call=engine,save=lambda s:saves.append(copy.deepcopy(s)))
    before=saves[-1]
    original_ranges=copy.deepcopy(before['read_inputs'])
    state=run_field_investigation(packet,bodies,call=engine,save=lambda s:None,state=before)
    assert state['complete'] and state['read_inputs']==original_ranges
    assert sum(c[0]=='field_investigation_plan' for c in calls)==1
    assert state['cost_usd']==pytest.approx(len(state['calls'])*.1)
    run_field_investigation(packet,bodies,call=lambda *a,**k:pytest.fail('paid repeat'),save=lambda s:None,state=state)
    altered=dict(bodies);altered['field:referee:0']+='changed'
    with pytest.raises(ValueError,match='rendition changed'):
        run_field_investigation(packet,altered,call=engine,save=lambda s:None,state=state)
    changed=copy.deepcopy(packet);changed['question']='New question'
    with pytest.raises(ValueError,match='packet changed'):
        run_field_investigation(changed,bodies,call=engine,save=lambda s:None,state=state)


def test_caps_and_cancel_prevent_unpaid_progress_but_keep_checkpoints():
    _,packet,_,bodies=fixture()
    packet['limits']['max_field_chars']=1
    with pytest.raises(ValueError,match='cannot inspect'):
        run_field_investigation(packet,bodies,call=lambda *a,**k:pytest.fail('no spending'),save=lambda s:None)
    packet['limits'].pop('max_field_chars')
    saves=[]
    with pytest.raises(ValueError,match='spend cap'):
        run_field_investigation(packet,bodies,call=fake([]),save=lambda s:saves.append(copy.deepcopy(s)),spend_cap_usd=.15)
    assert len(saves[-1]['calls'])==2
    calls=[]
    def check():
        if calls: raise RuntimeError('cancelled')
    with pytest.raises(RuntimeError,match='cancelled'):
        run_field_investigation(packet,bodies,call=fake(calls),save=lambda s:None,check=check)
    assert len(calls)==1


def test_large_field_readings_are_mapped_in_batches_without_losing_outputs():
    _,packet,_,bodies=fixture(field_count=12)
    calls=[]
    state=run_field_investigation(packet,bodies,call=fake(calls,large_readings=True),save=lambda s:None)
    assert state['complete'] and len(state['field_maps'])>1
    assert len([r for r in state['readings'] if len(r['reading'])>50000])==12
    assert any(c[2].get('map_scope')=='global_reconciliation' for c in calls)


def test_registry_api_runner_and_external_source_readings(monkeypatch):
    from src.dossier.catalog import resolve_path_request
    from src.dossier.schemas import PathRequest, CreateDossierRequest, DossierJob, DossierOptions, OutputOptions
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.workflows.registry import get_workflow_registry
    from src.api.routes import dossier
    from src.dossier import runner, investigation, blob_store, engine_call, events
    from src.readings import registry
    raw,packet,docs,bodies=fixture()
    path=resolve_path_request(PathRequest(chain_key='field_investigation'),'researcher')
    assert len(path.steps)==7 and get_workflow_registry().get('field_investigation')
    for step in path.steps:
        assert get_engine_registry().get_capability_definition(step.engine_key)
        assert get_operationalization_registry().get(step.engine_key).mode_for_depth('surface')=='oneshot'
    fields={'sources':[{'kind':'paste','role':'field_investigation','text':json.dumps(raw)}], 'intent':'Question',
            'entry':'chosen','path':{'chain_key':'field_investigation'},'output':{'text':False,'tables':False,'figures':0,'plates':0}}
    assert dossier.validate_lane(CreateDossierRequest(**fields))['entry']=='chosen'
    with pytest.raises(ValueError,match='one author_investigation'):
        dossier.validate_lane(CreateDossierRequest(**{**fields,'path':{'chain_key':'author_investigation'}}))
    job=DossierJob(id='field-test',options=DossierOptions(intent='Question',entry='chosen',path=PathRequest(chain_key='field_investigation'),
                   output=OutputOptions(text=False,tables=False,figures=0,plates=0),spend_cap_usd=8))
    blobs,writes,indexed={},{},[]
    monkeypatch.setattr(runner,'update_job',lambda jid,**fields:writes.update(fields))
    monkeypatch.setattr(runner,'record_step_duration',lambda *a:None)
    monkeypatch.setattr(events,'emit',lambda *a,**k:None)
    monkeypatch.setattr(blob_store,'put_blob',lambda key,mime,data:blobs.update({key:data}))
    monkeypatch.setattr(blob_store,'get_blob',lambda key:('application/json',blobs[key]) if key in blobs else None)
    monkeypatch.setattr(engine_call,'call_engine',fake([]))
    monkeypatch.setattr(registry,'index_job',lambda job,only_phases=None:indexed.extend(only_phases))
    runner._run_step(job,'plan',docs)
    assert len(job.plan.phases)==7
    runner._run_step(job,'analysis',docs)
    state=json.loads(blobs['investigation:field-test'])
    assert state['complete'] and job.totals.cost_usd==pytest.approx(len(state['calls'])*.1)
    assert len(indexed)==len(set(indexed))==len(state['analysis'])
    monkeypatch.setattr(dossier,'_load',lambda jid:job)
    assert dossier.get_investigation(job.id)['kind']=='field_investigation'
    monkeypatch.setattr(investigation,'load_investigation',lambda jid:None)
    assert dossier.get_investigation(job.id)['complete'] is False
    phase={'engine_key':'field_investigation_field_read','final_output':'[E1.F1] Network argument — dim: evidence — uid: referee:67 — anchor: "Network argument" — doc: field:referee:67 — confidence: high'}
    reading=registry.reading_from_phase({'id':job.id,'packet':packet},'2',phase)
    assert 'referee:67' in reading['texts'] and reading['renders'][0].endswith('/investigation')


def test_long_windows_keep_exact_quote_spans_and_full_baseline_context():
    raw,_,_,_=fixture(field_count=1)
    body='x' * 120000+' Workplace networks support mobilization. '+'z' * 120000
    raw['field'][0]['body']=body
    raw['field'][0]['page_spans']=[{'page':1,'start':0,'end':120000},{'page':2,'start':120000,'end':len(body)}]
    raw['limits']['max_field_chars']=12000
    raw['prior_investigations'][0]['memo']='Earlier claims. ' * 3000 + 'The final old conclusion must remain visible.'
    for i in range(30):
        raw.setdefault('prior_readings',[]).append({'job_id':f'prior-{i}','rows':['Some prior rows']})
    _,packet,_,bodies=freeze(raw)
    calls=[]
    state=run_field_investigation(packet,bodies,call=fake(calls),save=lambda s:None)
    reading=next(r for r in state['readings'] if r['source_role']=='field')
    assert reading['reading_mode']=='windows' and reading['inspected_chars']<=12000
    assert all(a[1]<b[0] for a,b in zip(reading['inspected_ranges'],reading['inspected_ranges'][1:]))
    memo_call=next(c for c in calls if c[0].endswith('_memo'))
    baseline=next(c for c in memo_call[2]['prior_context'] if c['key']=='prior_investigations')
    assert not baseline['truncated'] and 'final old conclusion' in baseline['text']


def test_fabricated_quotes_remain_conjectures_and_unsupported_map_stops():
    _,packet,_,bodies=fixture()
    base=fake([])
    def engine(key,sources,**kwargs):
        result=base(key,sources,**kwargs)
        if key.endswith('_field_read'):
            result['rows'][0]['anchor']='Fabricated unsupported evidence.'
        if key.endswith('_field_map'):
            result['rows'][0]['fields']['evidence_ids']='referee:0/E1.F1'
        return result
    saved=[]
    with pytest.raises(ValueError,match='field map support'):
        run_field_investigation(packet,bodies,call=engine,save=lambda s:saved.append(copy.deepcopy(s)))
    state=saved[-1]
    assert not state['complete'] and len(state['readings'])==2
    assert all(e['conjecture'] and not e['quote_verified'] for e in state['evidence'])


def test_support_repair_keeps_paid_draft_and_resumes_without_repeating_it():
    _,packet,_,bodies=fixture()
    base=fake([])
    def engine(key,sources,**kwargs):
        result=base(key,sources,**kwargs)
        if key.endswith('_memo') and 'validation_errors' not in kwargs['packet']:
            result['rows'][0]['fields'].update(claim_kind='thinker_position',evidence_ids='referee:0/E1.F1')
        return result
    state=run_field_investigation(packet,bodies,call=engine,save=lambda s:None)
    assert state['complete'] and 'memo' in state['calls'] and 'memo:repair' in state['calls']
    assert state['calls']['memo']['rows'][0]['fields']['claim_kind']=='thinker_position'
    assert state['memo_rows'][0]['fields']['claim_kind']=='comparison'
    run_field_investigation(packet,bodies,call=lambda *a,**k:pytest.fail('no repeated repair'),save=lambda s:None,state=state)


def test_parent_investigation_keeps_reviewed_baseline_and_existing_lineage():
    raw,_,_,_=fixture(prior=False)
    raw['parent_investigation']={'job_id':'parent','memo':'Reviewed memo','reviews':[{'quote':'A separately verified contrary passage.'}]}
    raw['prior_investigations']=[{'job_id':'older','memo':'Earlier lineage'}]
    _,packet,_,bodies=freeze(raw)
    assert packet['parent_investigation']==raw['parent_investigation']
    assert packet['prior_investigations'][0]['job_id']=='parent' and len(packet['prior_investigations'])==2
    state=run_field_investigation(packet,bodies,call=fake([]),save=lambda s:None)
    assert state['mode']=='follow_up'


def test_many_field_evidence_rows_fit_downstream_without_discarding_support_ids():
    _,packet,_,bodies=fixture(field_count=46,primary_count=115)
    base=fake([])
    def engine(key,sources,**kwargs):
        result=base(key,sources,**kwargs)
        if key.endswith('_field_read'):
            original=result['rows'][0]
            result['rows']=[{**copy.deepcopy(original),'id':f'E1.F{i+1}',
                            'finding':('Evidence-led account of worker action, organization and political alliances in its historical and institutional setting. '+'Specific source-qualified implications. '*4)} for i in range(24)]
        return result
    state=run_field_investigation(packet,bodies,call=engine,save=lambda s:None,spend_cap_usd=100)
    assert state['complete'] and len([e for e in state['evidence'] if e['source_role']=='field'])==1104
    manifests=state['call_input_manifests']
    assert any(m['evidence_representation']=='field_reference_index_and_primary_quotations' for m in manifests.values())
    assert len(manifests['memo']['evidence_ids'])==1106
    assert all(m['chars']<640000 for m in manifests.values())


def test_final_reconciliation_decisions_control_reads_and_caps_are_disclosed():
    _,packet,_,bodies=fixture(primary_count=3)
    base=fake([])
    def engine(key,sources,**kwargs):
        result=base(key,sources,**kwargs)
        if key.endswith('_author_select') and kwargs['packet']['selection_mode']=='reconcile':
            result['rows'].append({**row('candidate',uid='em:AUTHOR00',decision='defer',reason='Final reconciliation excludes this text'),'id':'E1.F99'})
        return result
    state=run_field_investigation(packet,bodies,call=engine,save=lambda s:None)
    assert 'em:AUTHOR00' not in state['selected_primary_uids']
    assert next(r for r in state['triage'] if r['uid']=='em:AUTHOR00')['decision']=='defer'
    def overselect(key,sources,**kwargs):
        result=base(key,sources,**kwargs)
        if key.endswith('_author_select') and kwargs['packet']['selection_mode']=='reconcile':
            result['rows'].append({**row('candidate',uid='em:AUTHOR02',decision='read',reason='Third candidate'),'id':'E1.F99'})
        return result
    state=run_field_investigation(packet,bodies,call=overselect,save=lambda s:None)
    assert next(r for r in state['triage'] if r['uid']=='em:AUTHOR02')['deferred_by_cap']


def test_field_allocation_finishes_short_articles_and_reserves_long_work_reading():
    raw,_,_,_=fixture(field_count=3)
    for r,size in zip(raw['field'],[90000,20000,200000]):
        r['body']='a'*size
        r['page_spans']=[]
    raw['limits']['max_field_chars']=160000
    _,packet,_,bodies=freeze(raw)
    state=run_field_investigation(packet,bodies,call=fake([]),save=lambda s:None)
    reads=[r for r in state['readings'] if r['source_role']=='field']
    assert [r['reading_mode'] for r in reads]==['full','full','windows']
    assert state['reading_allocations']['field']=={'referee:0':90000,'referee:1':20000,'referee:2':50000}
    assert state['coverage']['field']['inspected_chars']<=160000
