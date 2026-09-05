"""Dossier jobs survive a deploy: startup recovery restarts orphaned jobs, reconnaissance resumes from its
per-document checkpoint, cancellation is honoured inside the profile loop (2026-09-05)."""
from datetime import datetime, timedelta, timezone

from src.dossier import reconnaissance, runner
from src.dossier.common import DossierCancelled
from src.dossier.schemas import CorpusMap, DocumentProfile, DossierJob, DossierJobSummary, Reconnaissance
from src.sources.schemas import Document


def _summary(job_id, status, step, updated_at):
    return DossierJobSummary(id=job_id, status=status, step=step, created_at=updated_at, updated_at=updated_at)


def test_recover_orphaned_dossiers_restarts_recent_active_jobs_and_fails_stale_ones(monkeypatch):
    now = datetime(2026, 9, 5, 10, 0, tzinfo=timezone.utc)
    recent = (now - timedelta(minutes=30)).replace(tzinfo=None).isoformat()      # store writes naive UTC
    stale = (now - timedelta(hours=40)).replace(tzinfo=None).isoformat()
    rows = [
        _summary("d-analysis", "analysis", "analysis", recent),
        _summary("d-recon", "reconnaissance", "reconnaissance", recent),
        _summary("d-queued", "queued", "", recent),
        _summary("d-old", "composing", "compose", stale),
        _summary("d-waiting", "awaiting_brief", "brief", recent),
        _summary("d-done", "done", "receipts", recent),
        _summary("d-failed", "failed", "analysis", recent),
        _summary("d-cancelled", "cancelled", "reconnaissance", recent),
    ]
    started, updated, emitted = [], [], []
    monkeypatch.setattr(runner, "list_jobs", lambda limit=50: rows)
    monkeypatch.setattr(runner, "start", lambda job_id: started.append(job_id) or True)
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: updated.append((job_id, f)))
    monkeypatch.setattr(runner.events, "emit", lambda job_id, kind, **kw: emitted.append((job_id, kind)))
    out = runner.recover_orphaned_dossiers(now=now)
    assert started == ["d-analysis", "d-recon", "d-queued"]
    assert out["resumed"] == started and out["failed"] == ["d-old"] and out["skipped"] == []
    assert updated == [("d-old", {"status": "failed", "error": updated[0][1]["error"]})] and "not resumed automatically" in updated[0][1]["error"]
    assert ("d-old", "job_failed") in emitted and all(j not in {"d-waiting", "d-done", "d-failed", "d-cancelled"} for j, _ in emitted)


def _doc(key, text):
    return Document.model_construct(key=key, title=f"Title {key}", text=text, char_count=len(text), creators="x", year="2026", publication="p", stacks_key=key)


def _fake_call_json(calls):
    def call_json(job_id, step, *, label, system, user, tool_name, schema, model_cls, max_tokens):
        calls.append(label)
        if tool_name == "record_profiles":
            key = user.split("[")[1].split("]")[0] if "[" in user else "?"
            return {"profiles": [{"doc_key": key, "title": "", "genre": "g", "one_line": "o", "thesis": "t", "method": "m", "key_claims": [], "entities": [], "tensions": []}]}, None
        return CorpusMap(candidate_angles=["a"]), None
    return call_json


def test_reconnaissance_checkpoints_each_profile_and_resumes_from_them(monkeypatch):
    monkeypatch.setattr(reconnaissance, "SINGLE_CALL_MAX_CHARS", 10)           # force the per-document path
    monkeypatch.setattr(reconnaissance.events, "emit", lambda *a, **k: None)
    monkeypatch.setattr(reconnaissance, "documents_index", lambda docs: " ".join(f"[{d.key}]" for d in docs))
    monkeypatch.setattr(reconnaissance, "corpus_text", lambda docs, max_chars_per_doc=None: "")
    calls, checkpoints = [], []
    monkeypatch.setattr(reconnaissance, "call_json", _fake_call_json(calls))
    docs = [_doc("A", "alpha text"), _doc("B", "beta text"), _doc("C", "gamma text")]
    job = DossierJob()
    recon = reconnaissance.run_reconnaissance(job, docs, persist=lambda **f: checkpoints.append(f["profiles"]))
    assert [p.doc_key for p in recon.profiles] == ["A", "B", "C"] and recon.partial is False
    assert len(checkpoints) == 3 and all(c.partial for c in checkpoints) and [p.doc_key for p in checkpoints[1].profiles] == ["A", "B"]
    # a restart mid-way: the job carries the checkpoint after B — only C is profiled again
    calls.clear()
    job2 = DossierJob(profiles=checkpoints[1])
    recon2 = reconnaissance.run_reconnaissance(job2, docs, persist=lambda **f: None)
    assert [c for c in calls if c.startswith("profile")] == ["profile 3/3: Title C"]
    assert [p.doc_key for p in recon2.profiles] == ["A", "B", "C"]


def test_reconnaissance_stops_when_cancelled_between_documents(monkeypatch):
    monkeypatch.setattr(reconnaissance, "SINGLE_CALL_MAX_CHARS", 10)
    monkeypatch.setattr(reconnaissance.events, "emit", lambda *a, **k: None)
    monkeypatch.setattr(reconnaissance, "documents_index", lambda docs: " ".join(f"[{d.key}]" for d in docs))
    monkeypatch.setattr(reconnaissance, "corpus_text", lambda docs, max_chars_per_doc=None: "")
    calls = []
    monkeypatch.setattr(reconnaissance, "call_json", _fake_call_json(calls))
    docs = [_doc("A", "alpha text"), _doc("B", "beta text"), _doc("C", "gamma text")]
    flags = iter([False, True, True, True])
    try:
        reconnaissance.run_reconnaissance(DossierJob(), docs, cancel_check=lambda: next(flags))
        raise AssertionError("expected DossierCancelled")
    except DossierCancelled:
        pass
    assert calls == ["profile 1/3: Title A"]                                       # one profile bought, then stopped


def test_runner_treats_cancellation_as_quiet_stop(monkeypatch):
    seen = []
    monkeypatch.setattr(runner, "get_job", lambda job_id: DossierJob(id=job_id, status="reconnaissance", step="reconnaissance"))
    monkeypatch.setattr(runner, "load_documents", lambda job: [])
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: (_ for _ in ()).throw(DossierCancelled("cancelled at profile 2/3")))
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: seen.append(("update", f)))
    monkeypatch.setattr(runner.events, "emit", lambda job_id, kind, **kw: seen.append(("emit", kind)))
    runner._run("d-x")
    assert ("emit", "note") in seen and not any(k == "update" and f.get("status") == "failed" for k, f in seen)   # cancelled, not failed
