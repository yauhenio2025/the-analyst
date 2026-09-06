"""A plan survives a deploy: the file store is ephemeral, the executor job keeps plan_data (dossier-8577d8159b38 lost
its plan on resume after a redeploy, 2026-09-06)."""
import json
from pathlib import Path


def _plan_dict():
    from src.orchestrator.schemas import WorkflowExecutionPlan, PhaseExecutionSpec, TargetWork
    p = WorkflowExecutionPlan(plan_id="plan-test-durable", workflow_key="dossier_standard", thinker_name="Test",
                              target_work=TargetWork(title="Test paper", description="A paper for the test."),
                              phases=[PhaseExecutionSpec(phase_number=1.0, phase_name="Argument", engine_key="argument_architecture", depth="standard", passes=1)])
    return json.loads(p.model_dump_json())


def test_load_plan_falls_back_to_the_executor_copy_and_writes_the_file_back(tmp_path, monkeypatch):
    from src.orchestrator import planner
    from src.executor import job_manager
    monkeypatch.setattr(planner, "PLANS_DIR", tmp_path)
    data = _plan_dict()
    monkeypatch.setattr(job_manager, "find_job_by_plan", lambda plan_id: {"job_id": "job-x", "plan_data": data} if plan_id == data["plan_id"] else None)
    plan = planner.load_plan(data["plan_id"])
    assert plan is not None and plan.plan_id == data["plan_id"] and [p.engine_key for p in plan.phases] == ["argument_architecture"]
    assert (tmp_path / f"{data['plan_id']}.json").exists()
    assert planner.load_plan("plan-nowhere") is None


def test_failed_sub_job_with_plan_data_is_resumed_not_restarted(monkeypatch):
    from src.dossier import analysis
    resumed, started = [], []
    monkeypatch.setattr(analysis, "_resume_sub_job", lambda sub: resumed.append(sub["job_id"]))
    monkeypatch.setattr(analysis, "_start_sub_job", lambda job, plan_id, document_ids: started.append(plan_id) or "job-new")
    monkeypatch.setattr(analysis, "_is_live", lambda sub_job_id: False)
    monkeypatch.setattr(analysis, "_store_corpus", lambda job, docs: ("doc-1", "title"))
    monkeypatch.setattr(analysis, "_store_source_bindings", lambda job, docs: {})
    monkeypatch.setattr(analysis.events, "emit", lambda *a, **k: None)
    import src.executor.job_manager as jm
    monkeypatch.setattr(jm, "get_job", lambda job_id: {"job_id": job_id, "status": "failed", "plan_data": _plan_dict(), "error": "PoolError"})
    src = analysis.run_analysis.__code__
    # exercise only the decision: call the branch through a tiny job stub and stop before the polling loop
    class Plan:  # the dossier plan summary
        plan_id = "plan-test-durable"; phases = []
    class Job:
        id = "dossier-t"; plan = Plan(); analysis_job_id = "job-old"
    try:
        analysis.run_analysis(Job(), [], cancel_check=lambda: True)
    except Exception:
        pass  # the polling loop is not under test; the decision happened before it
    assert resumed == ["job-old"] and started == []
