"""The dossier spend cap is enforced between steps: a job over its cap does not start another model-bearing step;
the receipts step always runs; a job under its cap is untouched."""
from src.dossier import runner
from src.dossier.schemas import DossierJob, DossierOptions, Totals


def _job(cost, cap, status="analysis", step="analysis"):
    return DossierJob(id="d-cap", status=status, step=step, options=DossierOptions(intent="x", spend_cap_usd=cap),
                      totals=Totals(cost_usd=cost, llm_calls=3))


def test_a_job_over_its_cap_fails_before_the_next_step_and_the_error_names_the_amounts(monkeypatch):
    seen, steps = [], []
    monkeypatch.setattr(runner, "get_job", lambda job_id: _job(9.5, 8.0, status="analysis", step="analysis"))
    monkeypatch.setattr(runner, "load_documents", lambda job: [])
    monkeypatch.setattr(runner, "_next_step", lambda job: "spine")
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: steps.append(step))
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: seen.append(f))
    monkeypatch.setattr(runner.events, "emit", lambda job_id, kind, **kw: seen.append((kind, kw.get("detail", ""))))
    runner._run("d-cap")
    assert steps == []                                                                   # spine never started
    failed = [f for f in seen if isinstance(f, dict) and f.get("status") == "failed"]
    assert failed and failed[0]["error"] == "RuntimeError: spend cap reached: $9.50 of $8.00 before spine"
    assert any(k == "job_failed" for k, _ in [x for x in seen if isinstance(x, tuple)])


def test_a_job_under_its_cap_runs_and_the_receipts_step_is_never_blocked(monkeypatch):
    steps = []
    monkeypatch.setattr(runner, "get_job", lambda job_id: _job(7.9, 8.0, status="crosscheck", step="crosscheck"))
    monkeypatch.setattr(runner, "load_documents", lambda job: [])
    monkeypatch.setattr(runner, "_next_step", lambda job: "receipts")
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: steps.append(step))
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: None)
    monkeypatch.setattr(runner.events, "emit", lambda *a, **k: None)
    runner._run("d-cap")
    assert steps == ["receipts"]
    runner._over_cap(_job(50.0, 8.0), "receipts")                                          # over the cap, still allowed
    runner._over_cap(_job(50.0, None), "spine")                                            # no cap, no ceiling


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
