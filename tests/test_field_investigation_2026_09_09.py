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


def fake(calls, *, fail_stage=None, bad_memo=False, large_readings=False, select_last=False, drop_in_second=False):
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
            r = row('evidence', uid=uid, relation='direct', speaker='source author', voice='reported', bears_on='E1', bearing='supports')
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
        elif key == 'memo_critic':
            rows = [{**row('verdict', explanation='E1', state='settled', evidence_used='x'), 'id': 'C1.F1'},
                    {**row('best_idea', first_paragraph='1', developed='partly', why='named once'), 'id': 'C2.F1'},
                    {**row('gap', explanation='E1', rests_on='x'), 'id': 'C3.F1'}]
            prose = 'The best idea is named once and not developed.'
            if packet.get('reading') == 'revision':          # the second critic reads the revision against the draft
                dropped = packet['dropped_citations']
                rows.append({**row('unused', identity=next(iter(dropped['by_source']), 'none'), kind='dropped_source',
                                   disposition='must_use' if dropped['count'] else 'rightly_left', explanation='E1'), 'id': 'C5.F1'})
                prose = 'The revision dropped a source it must restore.' if dropped['count'] else 'Nothing dropped.'
        elif key.endswith('_field_map'):
            items = json.loads(sources[0].text)
            ev = packet.get('evidence') or [e for item in items for e in item['evidence']]
            ids = ';'.join(e['citation_id'] for e in ev if e['quote_verified'])
            rows = [row('debate', claim_kind='field_finding', evidence_ids=ids)]
        else:
            from src.dossier.context_packing import expand_evidence_rows
            ev = expand_evidence_rows(packet['evidence'])
            ids = ';'.join(e['citation_id'] for e in ev if e['quote_verified'])
            rows = [row('judgment' if key.endswith('_adjudicate') else 'answer', claim_kind='comparison', evidence_ids=ids)]
            if key.endswith('_memo'):
                rows += [{**row('revision', disposition='changed' if packet['mode'] == 'follow_up' else 'new',
                                baseline='prior' if packet['mode'] == 'follow_up' else 'standalone',
                                before='Provisional old view', after='Revised bounded view', evidence_ids=ids), 'id':'E2.F1'}]
                prose = f'The inquiry revises its scope [{ids.replace(";", "; ")}].'
                if packet.get('critic') and 'dropped_citations' not in packet:      # the first revision quietly drops all but one source
                    prose = f'The inquiry revises its scope [{ids.split(";")[0]}].'
                if drop_in_second and 'dropped_citations' in packet and 'validation_errors' not in packet:   # the second drops one too
                    prose = f'The inquiry revises its scope [{"; ".join(ids.split(";")[1:])}].'
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
    monkeypatch.setattr(dossier,'get_job_progress',lambda jid:job)
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


def test_many_repeated_field_evidence_rows_fit_without_discarding_quotes():
    _,packet,_,bodies=fixture(field_count=46,primary_count=115)
    base=fake([])
    def engine(key,sources,**kwargs):
        result=base(key,sources,**kwargs)
        if key.endswith('_field_read'):
            original=result['rows'][0]
            result['rows']=[{**copy.deepcopy(original),'id':f'E1.F{i+1}',
                            'finding':('Evidence-led account of worker action, organization and political alliances in its historical and institutional setting. '+'Specific source-qualified implications. '*4)} for i in range(24)]
        return result
    saves=[]
    run_field_investigation(packet,bodies,call=engine,save=lambda s:saves.append(copy.deepcopy(s)),spend_cap_usd=100)
    state=saves[-1]
    assert state['complete'] and state['running_stage'] is None
    field=[e for e in state['evidence'] if e['source_role']=='field']
    assert len(field)==1104 and all(e['source_quote'] and e['finding'] for e in field)
    manifests=state['call_input_manifests']
    assert any(m['evidence_representation']=='field_reference_index_and_primary_quotations' for m in manifests.values())
    assert len(manifests['adjudication']['evidence_ids'])==1106
    assert manifests['adjudication']['evidence_representation']=='verified_quotations'
    assert manifests['adjudication']['chars']<640000 and 'adjudication' in state['calls']
    assert manifests['adjudication']['packing']['evidence_record_encoding']=='grouped_evidence_v1'


def test_final_reconciliation_decisions_control_reads_and_caps_are_disclosed():
    _,packet,_,bodies=fixture(primary_count=3)
    base=fake([])
    def engine(key,sources,**kwargs):
        if kwargs['packet'].get('selection_mode') == 'resolve_conflicts':
            return {'rows': [row('candidate', uid='em:AUTHOR00', decision='defer',
                                reason='Explicit reconciliation excludes this text')], 'cost_usd': .1}
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


def test_large_parent_answer_does_not_displace_reviewed_memo_or_collection_gaps():
    raw,_,_,_=fixture(prior=False)
    raw['parent_investigation']={'answer':{'searches':'Search artifacts ' * 500000,'readings':[{'uid':'em:AUTHOR00'}],
                                          'evidence':[{'id':'retained'}]},
                                  'memo':'Reviewed baseline memo tail.',
                                  'reviews':[{'data':'Source audit ' * 9000}]}
    raw['field_gaps']=[{'query_id':90,'code':'query_not_found'}]
    _,packet,_,bodies=freeze(raw)
    calls=[]
    state=run_field_investigation(packet,bodies,call=fake(calls),save=lambda s:None)
    memo_call=next(c for c in calls if c[0].endswith('_memo'))
    baseline=next(c for c in memo_call[2]['prior_context'] if c['key']=='prior_investigations')
    assert not baseline['truncated'] and 'Reviewed baseline memo tail.' in baseline['text']
    assert 'Source audit '*9000 in baseline['text'] and 'Search artifacts Search artifacts' not in baseline['text']
    assert baseline['full_prior_packet_chars']>8000000 and baseline['answer_artifacts_summarized']
    assert state['field_gaps']==state['coverage']['field_gaps']==memo_call[2]['field_gaps']



def test_program_path_reads_thinker_first_replaces_maps_and_selection_and_revises_after_critic():
    raw, packet, _, bodies = fixture(field_count=3, primary_count=5)
    packet['research_state'] = {"question": packet["question"], "hunch": "a hunch", "prose": "Program prose: the stake and four explanations.",
                                "explanations": [{"id": "E1", "claim": "Collective organization mediates agency", "priority": 1, "undercuts_if": "agency without organization"},
                                                 {"id": "E2", "claim": "Networks substitute for organization", "priority": 2}],
                                "readings": [{"order": 1, "uid": "em:AUTHOR03", "why": "settles the stake", "look_for": "organization; agency"}],
                                "candidates": [{"uid": "em:AUTHOR01", "hits": {"agency": 1}, "total": 1, "already_ordered": False}],
                                "scans": [{"phrases": ["agency"], "explanations": ["E1"]}], "lanes": [], "gaps": [], "problems": []}
    calls = []
    state = run_field_investigation(packet, bodies, call=fake(calls), save=lambda s: None)
    keys = [c[0] for c in calls]
    assert state['complete'] and state['program_path'] is True and state['plan_source'] == 'research_state'
    assert 'field_investigation_plan' not in keys and 'field_investigation_author_select' not in keys and 'field_investigation_field_map' not in keys
    author_reads = [i for i, k in enumerate(keys) if k == 'field_investigation_author_read']
    field_reads = [i for i, k in enumerate(keys) if k == 'field_investigation_field_read']
    assert author_reads and field_reads and max(author_reads) < min(field_reads)          # the thinker first
    assert state['selected_primary_uids'] == ['em:AUTHOR03', 'em:AUTHOR01'] and state['selection']['source'] == 'research_program'
    assert state['coverage']['primary']['read_count'] == 2 and state['coverage']['field']['read_count'] == 3
    assert state['field_map']['source'] == 'code_evidence_tables' and state['field_map']['tables']['explanations'][0]['id'] == 'E1'
    assert len(state['field_map']['tables']['explanations'][0]['supports']) == 3          # every verified field finding bears on E1 in the fake
    assert state['support_routes']['global_to_synthesis']['policy'].startswith('program evidence tables')
    field = [e for e in state['evidence'] if e['source_role'] == 'field'][0]
    assert field['voice'] == 'reported' and field['bears_on'] == ['E1'] and field['bearing'] == 'supports' and field['speaker_in_context'] in (True, False)
    assert keys.count('memo_critic') == 2 and keys.count('field_investigation_memo') == 3
    memo_calls = [i for i, k in enumerate(keys) if k == 'field_investigation_memo']
    critic_calls = [i for i, k in enumerate(keys) if k == 'memo_critic']
    assert memo_calls[0] < critic_calls[0] < memo_calls[1] < critic_calls[1] < memo_calls[2] == len(keys) - 1
    assert state['memo_critic_rows'][1]['fields']['developed'] == 'partly'
    critic_packet = calls[critic_calls[0]][2]
    assert 'research_state' in critic_packet and 'evidence' not in critic_packet and critic_packet['evidence_identities']
    assert critic_packet['unused_bearing_findings']['count'] == 0                    # the draft cited every verified finding
    assert critic_packet['unused_figures']['count'] == 0 and 'unused_figures' in calls[memo_calls[1]][2]
    revise_packet = calls[memo_calls[1]][2]
    assert revise_packet['previous_draft'] and revise_packet['critic'] and revise_packet['critic_rows'] and 'unused_bearing_findings' in revise_packet
    second_critic = calls[critic_calls[1]][2]
    assert second_critic['reading'] == 'revision' and second_critic['previous_draft'] == state['memo_draft'] and second_critic['first_critic']
    verified = [e['citation_id'] for e in state['evidence'] if e['quote_verified']]
    assert len(verified) == 5 and verified[0].startswith('em:')                                  # two thinker rows first, then three field rows
    assert second_critic['dropped_citations']['count'] == 4                                       # the revision kept the first thinker citation only
    assert second_critic['unused_bearing_findings']['count'] == 3                                 # so every field finding that bears on E1 is unused
    assert state['memo_dropped_citations']['count'] == 4 and state['memo_must_use'] == ['C5.F1']
    second_revision = calls[memo_calls[2]][2]
    assert second_revision['dropped_citations']['count'] == 4 and second_revision['critic_rows'][-1]['fields']['disposition'] == 'must_use'
    assert state['memo_source'] == 'revision2' and len(state['memo_validation']['references']) == 5        # the second revision restored them
    assert state['memo_dropped_by_second_revision']['count'] == 0
    assert any(k.startswith('memo_critic') for k in state['method_snapshots'])


def test_unused_and_dropped_lists_are_assembled_by_code():
    from src.dossier.field_investigation import cited_identities, dropped_citations, unused_bearing_findings
    draft = 'One [a:1/F1; b:2/E1.F3] and two [c:3/F2].'
    revision = 'One [a:1/F1].'
    assert cited_identities(draft) == {'a:1/F1', 'b:2/E1.F3', 'c:3/F2'}
    dropped = dropped_citations(draft, revision, [{'citation_id': 'b:2/E1.F3', 'title': 'B'}, {'citation_id': 'c:3/F2', 'title': 'C'}])
    assert dropped['count'] == 2 and dropped['by_source'] == {'b:2': {'title': 'B', 'identities': ['b:2/E1.F3']}, 'c:3': {'title': 'C', 'identities': ['c:3/F2']}}
    tables = {'explanations': [{'id': 'E1', 'supports': [{'citation_id': 'a:1/F1', 'voice': 'narration', 'title': 'A', 'finding': 'f', 'quote': 'q'},
                                                          {'citation_id': 't:9/F1', 'voice': 'direct', 'speaker': 'CEO', 'title': 'T', 'finding': 'own words', 'quote': 'q' * 300}]
                                                          + [{'citation_id': f't:9/F{n}', 'voice': 'direct', 'title': 'T', 'finding': 'more', 'quote': 'q'} for n in range(2, 12)],
                                'undercuts': [{'citation_id': 'f:5/F2', 'voice': 'document', 'title': 'Fed', 'finding': 'displaces', 'quote': 'q'}]}]}
    unused = unused_bearing_findings(tables, {'a:1/F1'})
    assert unused['count'] == 12 and unused['by_source'] == {'T': 11, 'Fed': 1} and unused['listed'] == 7        # six per source at most
    assert [r['citation_id'] for r in unused['rows'][:3]] == ['t:9/F1', 't:9/F2', 'f:5/F2']                     # every source's strongest first
    assert all(r['citation_id'].startswith('t:9/') for r in unused['rows'][3:])
    assert len(unused['rows'][0]['quote']) == 160 and unused['rows'][0]['bearing'] == 'supports'


def test_second_revision_that_drops_what_the_first_cited_is_sent_back_once():
    raw, packet, _, bodies = fixture(field_count=3, primary_count=5)
    packet['research_state'] = {"question": packet["question"], "hunch": "a hunch", "prose": "p",
                                "explanations": [{"id": "E1", "claim": "Collective organization mediates agency", "priority": 1}],
                                "readings": [{"order": 1, "uid": "em:AUTHOR03", "why": "settles the stake"}], "candidates": [], "scans": [], "lanes": [], "gaps": [], "problems": []}
    calls = []
    state = run_field_investigation(packet, bodies, call=fake(calls, drop_in_second=True), save=lambda s: None)
    keys = [c[0] for c in calls]
    assert keys.count('field_investigation_memo') == 4 and keys.count('memo_critic') == 2
    repair = calls[-1][2]
    assert repair['validation_errors']['dropped_required_citations'] and repair['previous_draft'] and repair['critic_rows']
    assert state['memo_revision2_repaired'] is True and state['memo_source'] == 'revision2'
    assert state['memo_validation']['dropped_required_citations'] == [] and state['memo_dropped_by_second_revision']['count'] == 0


def test_program_path_falls_back_to_legacy_selection_when_the_program_names_nothing_available():
    raw, packet, _, bodies = fixture(field_count=2, primary_count=3)
    packet['research_state'] = {"question": packet["question"], "explanations": [{"id": "E1", "claim": "x"}], "readings": [{"order": 1, "uid": "em:NOPE"}],
                                "candidates": [], "scans": [], "prose": "p"}
    calls = []
    state = run_field_investigation(packet, bodies, call=fake(calls), save=lambda s: None)
    keys = [c[0] for c in calls]
    assert state['complete'] and 'field_investigation_author_select' in keys and 'field_investigation_field_map' not in keys
    assert state['field_map']['source'] == 'code_evidence_tables'


def test_unused_figures_lists_the_magnitudes_the_memo_does_not_carry():
    from src.dossier.field_investigation import unused_figures
    ev = [{"citation_id": "a:1/F1", "source_role": "field", "quote_verified": True, "bearing": "context", "title": "A",
           "source_quote": "In 2024, Tether reported $13.7 billion in net income with only 150 employees", "finding": "profit"},
          {"citation_id": "a:1/F2", "source_role": "field", "quote_verified": True, "bearing": "supports", "title": "A", "source_quote": "no number here", "finding": "words"},
          {"citation_id": "b:2/F1", "source_role": "field", "quote_verified": True, "bearing": "supports", "title": "B", "source_quote": "over 60 percent of supply", "finding": "share"},
          {"citation_id": "p:3/F1", "source_role": "primary", "quote_verified": True, "source_quote": "$5 billion", "finding": "thinker"},
          {"citation_id": "c:4/F1", "source_role": "field", "quote_verified": False, "source_quote": "$9 billion", "finding": "unverified"}]
    out = unused_figures(ev, {"b:2/F1"})
    assert out["count"] == 1 and out["rows"][0]["citation_id"] == "a:1/F1" and out["rows"][0]["figure"].startswith("$13.7")


def test_program_selects_the_field_read_set_over_the_cap_venues_then_bearing():
    from src.dossier.field_investigation import program_field_selection
    raw, packet, _, bodies = fixture(field_count=4, primary_count=3)
    rows = {r["uid"]: r for r in packet["field"]}
    rows["referee:0"]["source_metadata"] = {"discovery": {"bearing": "context"}}
    rows["referee:1"]["pdf_url"] = "https://home.treasury.gov/system/files/x.pdf"
    rows["referee:2"]["bearing"] = "undercuts"
    rs = {"question": packet["question"], "prose": "p", "explanations": [{"id": "E1", "claim": "x", "priority": 1}],
          "readings": [{"order": 1, "uid": "em:AUTHOR01", "why": "w"}], "candidates": [], "scans": [], "gaps": [], "problems": [],
          "lanes": [{"id": "P3.F2", "voice": "official", "venues": "treasury.gov; federalreserve.gov"}]}
    selected, decisions = program_field_selection(rs, packet, bodies, 2)
    assert selected == ["referee:1", "referee:2"] and decisions["referee:3"]["decision"] == "defer" and decisions["referee:0"]["reason"].startswith("its hit is context")
    packet["research_state"] = rs
    packet["limits"] = {**packet.get("limits", {}), "max_field_texts": 2}
    calls = []
    state = run_field_investigation(packet, bodies, call=fake(calls), save=lambda s: None)
    assert state["complete"] and state["field_selection"]["selected"] == ["referee:1", "referee:2"] and state["field_selection"]["eligible"] == 4
    assert state["coverage"]["field"]["read_count"] == 2 and sorted(state["coverage"]["field"]["unread_uids"]) == ["referee:0", "referee:3"]
