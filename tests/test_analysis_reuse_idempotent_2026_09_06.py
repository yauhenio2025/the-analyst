"""A resume that reuses a completed executor job must not record its receipts or replay its events a second time
(dossier-d2f1a77d8cc0, 2026-09-06: $9.59 of engines shown as $17.38 after one resume)."""
from src.dossier import analysis
from src.dossier.schemas import DossierJob, Receipt


ROWS = [{"id": "o1", "phase_number": 4.1, "pass_number": 1, "engine_key": "citation_engagement_map", "model_used": "sol",
         "input_tokens": 1000, "output_tokens": 100, "content": "- [D3.F1] a row — dim: citation_move", "created_at": "2026-09-06T10:00:00", "metadata": {}}]


def _run(monkeypatch, job):
    recorded, mirrored = [], []
    monkeypatch.setattr(analysis, "record", lambda job_id, receipt: recorded.append(receipt))
    monkeypatch.setattr(analysis, "_mirror_events", lambda job_id, sub, after: mirrored.append(after) or 99)
    monkeypatch.setattr(analysis.events, "emit", lambda *a, **k: None)
    import src.executor.output_store as store
    monkeypatch.setattr(store, "load_all_job_outputs", lambda sub, include_content=True: ROWS)
    import src.executor.job_manager as jm
    monkeypatch.setattr(jm, "get_job", lambda sub: {"status": "completed", "id": sub})
    from src.dossier.schemas import DossierPlan
    job.plan = DossierPlan(plan_id="p1")
    job.analysis_job_id = "exec-1"
    sub_id, out = analysis.run_analysis(job, [])
    return sub_id, out, recorded, mirrored


def test_first_fold_records_receipts_and_mirrors_events(monkeypatch):
    sub_id, out, recorded, mirrored = _run(monkeypatch, DossierJob(id="d1"))
    assert sub_id == "exec-1" and "4.1" in out and len(recorded) == 1 and mirrored == [0]


def test_a_second_fold_of_the_same_executor_job_records_nothing(monkeypatch):
    job = DossierJob(id="d1")
    job.receipts = [Receipt(step="analysis", kind="llm", model="sol", label="citation_engagement_map pass 1", input_tokens=1000, output_tokens=100, cost_usd=0.5, source_job_id="exec-1")]
    sub_id, out, recorded, mirrored = _run(monkeypatch, job)
    assert "4.1" in out and out["4.1"]["final_output"].startswith("- [D3.F1]")     # the analysis is still assembled
    assert recorded == [] and mirrored == []                                          # nothing recorded or replayed twice
