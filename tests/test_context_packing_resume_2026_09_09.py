"""Transactional preflight, process isolation, and synchronous normal continuation."""
import copy
import json
import sys
from pathlib import Path

import pytest

from scripts import resume_field_with_context_packing as utility
from tests.test_superseded_call_reconciliation_2026_09_09 import stored as accounting_stored, JOB, raw, state, snapshot
from src.dossier import blob_store as blobs
from src.dossier.schemas import Receipt
from src.dossier.store import compute_totals
from src.executor import db


@pytest.fixture
def paused(accounting_stored, tmp_path):
    db.execute("ALTER TABLE dossier_jobs ADD COLUMN step TEXT")
    db.execute("ALTER TABLE dossier_jobs ADD COLUMN error TEXT")
    db.execute("UPDATE dossier_jobs SET status='failed',step='analysis',error='input limit'")
    current=state();current.update(complete=False,running_stage=None,paused_reason='input_limit',current_stage='adjudication',
        read_inputs={'read:source':{'ranges':[[0,15]],'body_sha256':'a'*64}},call_input_manifests={'adjudication':{'chars':700001}})
    blobs.put_blob('investigation:'+JOB,'application/json',raw(current))
    module_dir=tmp_path/'modules';module_dir.mkdir()
    (module_dir/'context_packing.py').write_text("POLICY_MARKER = 'patched'\n")
    (module_dir/'field_investigation.py').write_text("POLICY_MARKER = 'patched'\n")
    return module_dir


def finish(job_id):
    assert sys.modules['src.dossier.field_investigation'].POLICY_MARKER=='patched'
    assert db.execute('SELECT status FROM dossier_jobs WHERE id=%s',(job_id,),fetch='one')['status']=='analysis'
    current=state();current['calls']['adjudication']={'cost_usd':0.1};current['analysis']['24']={'final_output':'New adjudication'}
    current.update(complete=True,paused_reason=None,running_stage=None,current_stage='done',cost_usd=0.2201)
    blobs.put_blob('investigation:'+job_id,'application/json',raw(current))
    row=db.execute('SELECT receipts_json,totals_json FROM dossier_jobs WHERE id=%s',(job_id,),fetch='one')
    receipts=json.loads(row['receipts_json'])+[Receipt(step='analysis',kind='llm',cost_usd=0.1,label='adjudication').model_dump()]
    totals=compute_totals(receipts,json.loads(row['totals_json']))
    db.execute("UPDATE dossier_jobs SET status='done',analysis_json=%s,receipts_json=%s,totals_json=%s WHERE id=%s",
               (json.dumps(current['analysis']),json.dumps(receipts),json.dumps(totals),job_id))


def test_preflight_is_read_only_and_never_loads_or_runs_modules(paused,monkeypatch):
    before=snapshot()
    monkeypatch.setattr(utility,'_run_normal',lambda *a:pytest.fail('dry-run executed runner'))
    monkeypatch.setattr(utility,'_modules',lambda *a:pytest.fail('dry-run loaded code'))
    result=utility.resume(JOB,paused)
    assert result['status']=='ready' and not result['applied'] and result['preflight']['cached_call_count']==1
    assert snapshot()==before


def test_apply_waits_for_normal_runner_and_preserves_saved_prefix(paused,monkeypatch):
    preflight=utility.resume(JOB,paused)['preflight'];old=copy.deepcopy(state());module=sys.modules.get('src.dossier.field_investigation')
    original_checkpoint=blobs.get_blob('investigation:'+JOB)[1]
    monkeypatch.setattr(utility,'_run_normal',finish)
    result=utility.resume(JOB,paused,apply=True,expected=preflight,competing_resumes_disabled=True)
    assert result['status']=='done' and result['complete'] and result['additional_calls']==1
    assert result['saved_call_prefix_unchanged'] and result['read_inputs_unchanged']
    assert all(state()['calls'][k]==v for k,v in old['calls'].items())
    assert sys.modules.get('src.dossier.field_investigation') is module
    assert blobs.get_blob(result['launch_artifact']+':result') is not None
    assert blobs.get_blob(result['checkpoint_artifact']['key'])[1]==original_checkpoint
    launch=json.loads(blobs.get_blob(result['launch_artifact'])[1])
    assert launch['checkpoint_artifact']==result['checkpoint_artifact']
    with pytest.raises(ValueError,match='must be failed'):
        utility.resume(JOB,paused,apply=True,expected=preflight,competing_resumes_disabled=True)


@pytest.mark.parametrize('changed',['code','checkpoint','coordination'])
def test_refuses_changed_preflight_or_missing_resume_coordination(paused,changed,monkeypatch):
    preflight=utility.resume(JOB,paused)['preflight']
    if changed=='code':(paused/'context_packing.py').write_text("POLICY_MARKER='different'\n")
    if changed=='checkpoint':
        current=state();current['updated_at']='changed';blobs.put_blob('investigation:'+JOB,'application/json',raw(current))
    before=snapshot()
    monkeypatch.setattr(utility,'_run_normal',lambda *a:pytest.fail('unsafe launch'))
    with pytest.raises(ValueError,match='changed|disable competing'):
        utility.resume(JOB,paused,apply=True,expected=preflight,competing_resumes_disabled=changed!='coordination')
    assert snapshot()==before


def test_running_or_provider_inflight_job_cannot_be_recovered(paused):
    db.execute("UPDATE dossier_jobs SET status='analysis'")
    with pytest.raises(ValueError,match='must be failed'):
        utility.resume(JOB,paused)
    db.execute("UPDATE dossier_jobs SET status='failed'")
    current=state();current['running_stage']='adjudication';blobs.put_blob('investigation:'+JOB,'application/json',raw(current))
    with pytest.raises(ValueError,match='must be idle'):
        utility.resume(JOB,paused)


def test_interrupted_launch_fails_job_and_cannot_repeat_same_checkpoint(paused,monkeypatch):
    preflight=utility.resume(JOB,paused)['preflight']
    def fail(_):raise RuntimeError('injected before runner work')
    monkeypatch.setattr(utility,'_run_normal',fail)
    with pytest.raises(RuntimeError,match='injected'):
        utility.resume(JOB,paused,apply=True,expected=preflight,competing_resumes_disabled=True)
    assert db.execute('SELECT status FROM dossier_jobs',fetch='one')['status']=='failed'
    with pytest.raises(ValueError,match='already has a launch receipt'):
        utility.resume(JOB,paused,apply=True,expected=preflight,competing_resumes_disabled=True)


def test_schema_or_module_error_is_caught_before_any_launch(paused):
    (paused/'context_packing.py').write_text('syntax !!!')
    before=snapshot()
    with pytest.raises(SyntaxError):utility.resume(JOB,paused)
    assert snapshot()==before
