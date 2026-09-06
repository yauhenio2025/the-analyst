"""The dossier spend cap is enforced between steps: a job over its cap does not start another model-bearing step;
the receipts step always runs; a job under its cap is untouched."""
from src.dossier import runner
from src.dossier.schemas import DossierJob, DossierOptions, Totals


def _job(cost, cap, status="analysis", step="analysis"):
    return DossierJob(id="d-cap", status=status, step=step, options=DossierOptions(intent="x", spend_cap_usd=cap),
                      totals=Totals(cost_usd=cost, llm_calls=3))


def test_the_engines_are_refused_when_spent_plus_the_plans_estimate_exceeds_the_cap(monkeypatch):
    from src.dossier.schemas import DossierPlan
    seen, steps = [], []
    job = _job(1.8, 8.0, status="planning", step="plan")
    job.plan = DossierPlan(plan_id="p1", estimated_cost_usd=7.5)
    monkeypatch.setattr(runner, "get_job", lambda job_id: job)
    monkeypatch.setattr(runner, "load_documents", lambda job: [])
    monkeypatch.setattr(runner, "_next_step", lambda job: "analysis")
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: steps.append(step))
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: seen.append(f))
    monkeypatch.setattr(runner.events, "emit", lambda job_id, kind, **kw: seen.append((kind, kw.get("detail", ""))))
    runner._run("d-cap")
    assert steps == []                                                                   # the engines never started
    failed = [f for f in seen if isinstance(f, dict) and f.get("status") == "failed"]
    assert failed and failed[0]["error"] == "RuntimeError: spend cap: $1.80 spent and the plan estimates $7.50 more for the engines, over the cap of $8.00; raise the cap or shorten the path"


def test_a_resume_into_a_completed_analysis_is_not_refused(monkeypatch):
    """dossier-d2f1a77d8cc0 (2026-09-06): resumed after the cap failure, the runner re-entered 'analysis' by name and the
    estimate rule refused it although the engines were done and would be reused."""
    from src.dossier.schemas import DossierPlan
    steps = []
    job = _job(9.59, 8.0, status="analysis", step="analysis"); job.plan = DossierPlan(plan_id="p1", estimated_cost_usd=4.71)
    job.analysis = {"4.1": {"phase_number": 4.1, "engine_key": "citation_engagement_map", "final_output": "done"}}
    monkeypatch.setattr(runner, "get_job", lambda job_id: job)
    monkeypatch.setattr(runner, "load_documents", lambda job: [])
    monkeypatch.setattr(runner, "_next_step", lambda job: "analysis")
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: steps.append(step))
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: None)
    monkeypatch.setattr(runner.events, "emit", lambda *a, **k: None)
    runner._run("d-cap")
    assert steps[:2] == ["analysis", "spine"]


def test_after_paid_engines_the_desks_finish_and_the_overrun_is_noted_once(monkeypatch):
    """The Stacks' first pair (2026-09-06): $9.59 of engines against a cap of 8; the desks must not be refused."""
    seen, steps = [], []
    monkeypatch.setattr(runner, "get_job", lambda job_id: _job(9.59, 8.0, status="analysis", step="analysis"))
    monkeypatch.setattr(runner, "load_documents", lambda job: [])
    monkeypatch.setattr(runner, "_next_step", lambda job: "spine")
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: steps.append(step))
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: seen.append(f))
    monkeypatch.setattr(runner.events, "emit", lambda job_id, kind, **kw: seen.append((kind, kw.get("detail", ""))))
    runner._run("d-cap")
    assert steps[:2] == ["spine", "tables"] and "receipts" in steps                         # every desk ran
    notes = [d for k, d in [x for x in seen if isinstance(x, tuple)] if k == "note" and d.startswith("over the spend cap")]
    assert len(notes) == 1 and "$9.59 of $8.00" in notes[0]
    assert not any(isinstance(f, dict) and f.get("status") == "failed" for f in seen)


def test_a_chosen_path_job_does_not_pause_at_the_brief(monkeypatch):
    """entry chosen + a fixed path on the request: the brief is written for the record, own_path is chosen, the run goes on."""
    from src.dossier.schemas import Brief, BriefOption, DossierJob, DossierOptions, PathRequest
    import src.dossier.brief as brief_mod
    seen = []
    job = DossierJob(id="d-chosen", status="reconnaissance", step="brief",
                     options=DossierOptions(intent="x", entry="chosen", path=PathRequest(steps=[{"engine_key": "citation_engagement_map", "depth": "standard"}])))
    monkeypatch.setattr(brief_mod, "run_brief", lambda job, docs, **kw: Brief(options=[BriefOption(key="a", title="A")]))
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: seen.append(f))
    monkeypatch.setattr(runner.events, "emit", lambda job_id, kind, **kw: seen.append((kind, kw.get("detail", ""))))
    monkeypatch.setattr(runner, "record_step_duration", lambda *a, **k: None, raising=False)
    runner._run_step(job, "brief", [])
    assert job.chosen_option == "own_path" and job.brief.option("own_path") is not None
    assert any(isinstance(f, dict) and f.get("chosen_option") == "own_path" for f in seen)
    assert not any(isinstance(f, dict) and f.get("status") == "awaiting_brief" for f in seen)


def test_no_cap_means_no_ceiling_and_receipts_are_never_refused():
    runner._over_cap(_job(50.0, None), "spine")                                            # no cap, no ceiling
    runner._over_cap(_job(50.0, 8.0), "receipts")                                          # over the cap, receipts still run
    runner._over_cap(_job(50.0, 8.0), "tables")                                            # a desk after the engines is never refused
