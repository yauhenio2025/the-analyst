"""Exact reviewed batch repairs; temporary fixtures and network-free replay only."""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

batch = load('batch_recovery', 'scripts/study_argument_family_score_batch_recovery_2026_09_05.py')
base = load('batch_base_fixtures', 'tests/test_study_argument_family_score_recovery_2026_09_05.py')
campaign = base.campaign
offline = base.offline
RAW = (ROOT / 'tests/fixtures/argument_family_2026_09_05/malformed_sol_score_castoriadis.json').read_bytes()
MANUAL_RAW = (ROOT / 'tests/fixtures/argument_family_2026_09_05/malformed_sonnet_score_ganzinger.json').read_bytes()
KEY = 'score__sol__dialectical_structure__original__castoriadis'
MANUAL_KEY = 'score__sonnet__counterfactual_analyzer__candidate__ganzinger'


def item(first, key, raw, offsets, inserted):
    fixed = raw
    for offset in reversed(offsets):
        fixed = fixed[:offset] + inserted.encode() + fixed[offset:]
    return {'key': key, 'attempt': 'fixture', 'failed_job_sha256': '', 'raw_sha256': first.sha(raw),
            'corrected_sha256': first.sha(fixed), 'corrected_path': 'reader_notes/' + key + '.json',
            'edits': [{'offset': o, 'insert': inserted} for o in offsets]}, fixed


@pytest.mark.parametrize('raw,key,offsets,insertion', [(RAW, KEY, [1888], '}'),
    (MANUAL_RAW, MANUAL_KEY, [1055,1076,3312,3322], '\\')])
def test_exact_actual_insertions_preserve_all_other_bytes(raw, key, offsets, insertion):
    _, first = batch.load_dependencies()
    h = first.load_harness()
    reviewed, fixed = item(first, key, raw, offsets, insertion)
    actual, judgment = batch.reviewed_repair(first, h, raw, reviewed)
    assert actual == fixed and len(actual) == len(raw) + len(offsets)
    assert judgment == h.parse_score(fixed.decode()) and len(judgment['reasons']) == 6
    with pytest.raises(json.JSONDecodeError):
        h.parse_score(raw.decode())


@pytest.mark.parametrize('edits', [[{'offset':1888,'insert':'0'}], [{'offset':1888,'insert':'text'}],
    [{'offset':1888,'insert':'}}'}], [{'offset':1887,'insert':'}'}], [{'offset':10,'insert':'\\'}],
    [{'offset':1888,'insert':'}','delete':1}], [{'offset':1888,'insert':'}'}]*2,
    [{'offset':True,'insert':'}'}]])
def test_no_general_edit_or_unreviewed_syntax_repairs(edits):
    _, first = batch.load_dependencies()
    reviewed, _ = item(first, KEY, RAW, [1888], '}')
    reviewed['edits'] = edits
    with pytest.raises(RuntimeError):
        batch.reviewed_repair(first, first.load_harness(), RAW, reviewed)


@pytest.fixture
def ready(campaign, monkeypatch):
    c = campaign
    c.collector, _ = batch.load_dependencies()
    c.first = base.recovery
    h = c.first.load_harness()
    c.h = h
    c.keys = {KEY, MANUAL_KEY}
    native = h.validate_completed
    # Only corpus-free fixture parent/synthetic scores are stubbed. All first and
    # batch score replays use the original harness validator and strict parser.
    def validate(job, record, *args):
        if job['key'] in c.keys | {c.first.TARGET}:
            return native(job, record, *args)
        h.require(record['status'] == 'complete' and c.first.sha((c.run / record['output']).read_bytes()) == record['output_sha256'], 'Parent/output changed')
        return True
    monkeypatch.setattr(h, 'validate_completed', validate)
    monkeypatch.setattr(h, 'guard_inputs', lambda p: h.require(p == c.plan, 'Plan changed'))
    monkeypatch.setattr(h, 'build_plan', lambda *args: (c.plan, {}, {}))
    prompt = json.loads((c.first.attempt(c.run) / 'call-0001.prompt.json').read_bytes())
    monkeypatch.setattr(h, 'judge_prompt', lambda *args: prompt)
    monkeypatch.setattr(h, 'estimate', lambda *args: {'estimate_usd': .2})
    c.plan.update(models=h.MODELS, calibration={})
    first_record = c.first.candidate_record(h, c.records[c.first.TARGET], c.first.recover_known(h, base.RAW.decode()), 'fixture-manifest')
    c.records[c.first.TARGET] = first_record
    h.write_json(c.first.attempt(c.run) / 'job.json', first_record)
    (c.run / first_record['output']).write_bytes(c.first.score_bytes(first_record['judgment']))
    monkeypatch.setattr(c.first, 'validate_adopted', lambda h, run, record: h.require(record == first_record, 'First recovery changed'))
    c.calls = []
    c.response = {}
    c.rt.core.run_engine_call = lambda **kwargs: c.calls.append(kwargs) or dict(c.response)
    c.rt.core.estimate_cost = lambda *args: .040208
    batch.install_reporting(c.first, c.collector, h)
    c.items = []
    for key, raw, rater, offsets, insertion in [(KEY, RAW, 'sol', [1888], '}'),
            (MANUAL_KEY, MANUAL_RAW, 'sonnet', [1055,1076,3312,3322], '\\')]:
        job = {'key':key, 'kind':'judge', 'reading':'g0', 'rater':rater, 'base_calls':1}
        c.plan['judgments'].append(job)
        c.response.update(content=raw.decode(), model_used=h.MODELS['judge_' + rater], input_tokens=1000,
                          output_tokens=500, retries=0, partial=None, stop_reason=None)
        with pytest.raises(json.JSONDecodeError):
            h.execute_job(job,c.plan,c.run,c.records,{}, {},c.run.parent,16,c.rt)
        c.collector.defer(c.first,h,job,c.records[key],c.plan,c.run,c.records,{}, {},c.rt)
        reviewed, fixed = item(c.first,key,raw,offsets,insertion)
        entry = c.collector.pending_entries(c.run)[key]
        reviewed.update(attempt=entry['attempt'], failed_job_sha256=entry['failed_job_sha256'])
        (c.run / reviewed['corrected_path']).write_bytes(fixed)
        c.items.append(reviewed)
    for i in range(len(c.plan['judgments']),48):
        key = 'synthetic' + str(i)
        job = {'key':key,'kind':'judge'}
        c.plan['judgments'].append(job)
        output = 'outputs/' + key + '.md'
        (c.run / output).write_text(key)
        c.records[key] = {**job,'status':'complete','output':output,'output_sha256':c.first.sha(key.encode())}
    for job in c.plan['judgments']:
        record = c.records[job['key']]
        if job['key'] not in c.keys | {c.first.TARGET}:
            record.update(invocations=1, attempt='synthetic')
            h.write_json(c.run/'receipts'/job['key']/'synthetic'/'call-0001.json', {'status':'complete','cost_usd':0})
    h.write_json(c.run/'plan.json',c.plan)
    h.write_json(c.run/'results.json',c.records)
    monkeypatch.setattr(c.first,'PLAN_SHA',c.first.sha((c.run/'plan.json').read_bytes()))
    memo = c.run/'reader_notes/review.md'; memo.write_text('Human reviewed exact syntax artifacts.')
    c.approval = {'identity':c.first.IDENTITY, 'decision':'adopt_reviewed_exact_scores',
        'results_sha256':c.first.sha((c.run/'results.json').read_bytes()),
        'pending_sha256':c.first.sha((c.run/c.collector.PENDING).read_bytes()),
        'adapter_sha256':c.first.sha(Path(batch.__file__).read_bytes()),'collector_sha256':batch.COLLECTOR_SHA,
        'first_wrapper_sha256':c.first.sha(Path(c.first.__file__).read_bytes()),
        'review_files':{str(c.log):c.first.sha(c.log.read_bytes()),str(memo):c.first.sha(memo.read_bytes())}, 'repairs':c.items}
    c.approval_path = c.run/'reader_notes/approval.json'
    h.write_json(c.approval_path,c.approval)
    return c


def test_full_48_call_gate_and_no_write_preview(ready):
    c = ready
    before = {str(p):p.read_bytes() for p in c.run.rglob('*') if p.is_file()}
    result = batch.prepare(c.first,c.collector,c.h,c.rt,c.run,c.approval_path)
    assert set(result[2]) == c.keys and len(c.calls) == 2
    assert before == {str(p):p.read_bytes() for p in c.run.rglob('*') if p.is_file()}
    assert not (c.run/batch.BUNDLE).exists()


def test_batch_adoption_preserves_all_failures_calls_and_first_record(ready):
    c = ready
    before = (c.run/'results.json').read_bytes()
    call_bytes = {str(p):p.read_bytes() for p in c.run.glob('receipts/*/*/call-*')}
    first_before = copy.deepcopy(c.records[c.first.TARGET])
    result = batch.adopt(c.first,c.collector,c.h,c.rt,c.run,c.approval_path)
    assert result['new_paid_calls'] == 0 and set(result['batch_keys']) == c.keys
    assert (c.run/batch.BUNDLE/'results.failed.json').read_bytes() == before
    assert call_bytes == {str(p):p.read_bytes() for p in c.run.glob('receipts/*/*/call-*')}
    records = c.h.read_json(c.run/'results.json')
    assert records[c.first.TARGET] == first_before and len(c.calls) == 2
    for job in c.plan['judgments']:
        if job['key'] in c.keys | {c.first.TARGET}:
            assert c.h.validate_completed(job,records[job['key']],c.plan,c.run,records,{}, {},c.rt)
    assert c.h.parse_score.__name__ == 'parse_score'
    with pytest.raises(json.JSONDecodeError):
        c.h.parse_score(RAW.decode())
    with pytest.raises(RuntimeError,match='bundle already exists'):
        batch.adopt(c.first,c.collector,c.h,c.rt,c.run,c.approval_path)
    assert len(c.calls) == 2


@pytest.mark.parametrize('artifact',['parent','raw','prompt','response','receipt','failed_job','pending','corrected','memo','approval','missing_score','extra_attempt'])
def test_changed_bindings_refuse_before_any_publication(ready,artifact):
    c=ready
    record=c.records[KEY]
    attempt=c.run/'receipts'/KEY/record['attempt']
    paths={'parent':c.run/c.records['g0']['output'],'raw':attempt/'call-0001.md',
        'prompt':attempt/'call-0001.prompt.json','response':attempt/'call-0001.response.json',
        'receipt':attempt/'call-0001.json','failed_job':attempt/'job.json',
        'pending':c.run/c.collector.PENDING,'corrected':c.run/c.items[0]['corrected_path'],
        'memo':c.run/'reader_notes/review.md','approval':c.approval_path}
    if artifact=='missing_score':
        c.plan['judgments'].pop()
        c.h.write_json(c.run/'plan.json',c.plan)
        c.first.PLAN_SHA=c.first.sha((c.run/'plan.json').read_bytes())
    elif artifact=='extra_attempt':
        c.h.write_json(c.run/'receipts'/KEY/'second'/'call-0001.json',{'status':'complete','cost_usd':0})
    elif artifact=='approval':
        approval=copy.deepcopy(c.approval); approval['repairs'].pop(); c.h.write_json(c.approval_path,approval)
    else:
        paths[artifact].write_bytes(paths[artifact].read_bytes()+b' ')
    with pytest.raises((RuntimeError,KeyError)):
        batch.adopt(c.first,c.collector,c.h,c.rt,c.run,c.approval_path)
    assert not(c.run/batch.BUNDLE).exists() and len(c.calls)==2


@pytest.mark.parametrize('artifact',['manifest','original','corrected','score','record','raw'])
def test_post_adoption_tampering_refuses_replay(ready,artifact):
    c=ready
    batch.adopt(c.first,c.collector,c.h,c.rt,c.run,c.approval_path)
    records=c.h.read_json(c.run/'results.json'); record=records[KEY]
    if artifact=='record':
        record['judgment']['specificity']=1
    else:
        bundle=c.run/batch.BUNDLE
        paths={'manifest':bundle/'manifest.json','original':bundle/KEY/'job.failed.json',
               'corrected':bundle/KEY/'corrected.raw.json','score':c.run/record['output'],
               'raw':c.run/'receipts'/KEY/record['attempt']/'call-0001.md'}
        paths[artifact].write_bytes(paths[artifact].read_bytes()+b' ')
    job=next(j for j in c.plan['judgments'] if j['key']==KEY)
    with pytest.raises(RuntimeError):
        c.h.validate_completed(job,record,c.plan,c.run,records,{}, {},c.rt)
    assert c.h.parse_score.__name__=='parse_score' and len(c.calls)==2


def test_same_raw_in_unreviewed_job_does_not_receive_repair(ready):
    c=ready
    batch.adopt(c.first,c.collector,c.h,c.rt,c.run,c.approval_path)
    job={'key':'unreviewed','kind':'judge','reading':'g0','rater':'sol','base_calls':1}
    c.plan['judgments'].append(job)
    c.response.update(content=RAW.decode(),model_used=c.h.MODELS['judge_sol'])
    records=c.h.read_json(c.run/'results.json')
    with pytest.raises(json.JSONDecodeError):
        c.h.execute_job(job,c.plan,c.run,records,{}, {},c.run.parent,16,c.rt)
    assert len(c.calls)==3 and records['unreviewed']['status']=='failed'


@pytest.mark.parametrize('argv',[['--run'],['--phase','judge'],['--adopt'],['--phase','report','--adopt']])
def test_cli_cannot_launch_calls_or_implicit_adoption(argv,monkeypatch):
    monkeypatch.setattr(batch,'load_dependencies',lambda:pytest.fail('Invalid mode loaded dependencies'))
    with pytest.raises(SystemExit):
        batch.main(argv)


def test_active_campaign_lock_blocks_adoption(ready):
    c=ready
    with c.first.campaign_lock(c.run):
        with pytest.raises(RuntimeError,match='Campaign is active'):
            batch.adopt(c.first,c.collector,c.h,c.rt,c.run,c.approval_path)
    assert not(c.run/batch.BUNDLE).exists() and len(c.calls)==2


def test_report_separates_first_batch_and_native_counts():
    from types import SimpleNamespace
    collector,first=batch.load_dependencies()
    h=first.load_harness()
    result={'valid_judgments':48,'validation_errors':{}}
    h.report=lambda *args: copy.deepcopy(result)
    batch.install_reporting(first,collector,h)
    records={first.TARGET:{'status':'complete'}, KEY:{'status':'complete','recovery':{'method':'reviewed_exact_score_syntax_insertions'}},
             MANUAL_KEY:{'status':'complete','recovery':{'method':'reviewed_exact_score_syntax_insertions'}}}
    plan={'generations':[],'judgments':[{'key':k} for k in records]}
    output=h.report(plan,Path('/unused'),records,{}, {},SimpleNamespace())['score_recovery']
    assert output['valid_native_scores']==45 and output['valid_first_recovered_scores']==1
    assert output['valid_batch_recovered_scores']==2 and output['valid_recovered_scores']==3
    assert output['historical_parser_failures_preserved']==3 and len(output['recovered_keys'])==3


def test_actual_elling_whitespace_boundary_preserves_all_existing_bytes():
    _,first=batch.load_dependencies()
    raw=(ROOT/'tests/fixtures/argument_family_2026_09_05/malformed_sonnet_score_elling.json').read_bytes()
    assert first.sha(raw)=='67c4066c0f45ccb40bd5ea5a803100618db34df490a5f780bd1bfe1a30bcfb87'
    offset=raw.index(b', "one_line":')
    reviewed,fixed=item(first,'elling',raw,[offset],'}')
    actual,value=batch.reviewed_repair(first,first.load_harness(),raw,reviewed)
    assert actual==fixed and actual[:offset]==raw[:offset] and actual[offset+1:]==raw[offset:]
    assert len(value['reasons'])==6


@pytest.mark.parametrize('boundary',[b',\t"one_line" \r\n:',b', "one_line":'])
def test_json_whitespace_is_preserved_at_approved_boundary(boundary):
    _,first=batch.load_dependencies()
    raw=RAW.replace(b',"one_line":',boundary)
    offset=raw.index(boundary)
    reviewed,fixed=item(first,KEY,raw,[offset],'}')
    assert batch.reviewed_repair(first,first.load_harness(),raw,reviewed)[0]==fixed


@pytest.mark.parametrize('mutation',[lambda raw:raw+b', "one_line":',
    lambda raw:raw.replace(b',"one_line":',b',\v"one_line":'),
    lambda raw:raw.replace(b',"one_line":',b', "one_line" ;')])
def test_ambiguous_or_non_json_boundary_is_refused(mutation):
    _,first=batch.load_dependencies()
    raw=mutation(RAW)
    reviewed,_=item(first,KEY,raw,[1888],'}')
    with pytest.raises(RuntimeError,match='unique one_line delimiter'):
        batch.reviewed_repair(first,first.load_harness(),raw,reviewed)


def test_unplanned_recovery_record_cannot_inflate_report():
    collector,first=batch.load_dependencies()
    h=first.load_harness()
    h.report=lambda *args: pytest.fail('Unplanned record reached native report')
    batch.install_reporting(first,collector,h)
    records={'fabricated':{'status':'complete','recovery':{'method':'reviewed_exact_score_syntax_insertions'}}}
    with pytest.raises(RuntimeError,match='Unexpected record'):
        h.report({'generations':[],'judgments':[]},Path('/unused'),records,{}, {},None)
