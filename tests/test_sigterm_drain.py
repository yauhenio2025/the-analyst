"""A deploy costs at most one interrupted call, not a lost step: SIGTERM flips a process-wide drain flag, `runner.start`
refuses new threads, reconnaissance pauses between documents (`DossierDraining`), `_run` treats the pause as a quiet
stop that leaves the job's active status for the next instance's boot recovery, and the handler waits for idle
(2026-09-05, evening)."""
import time

import pytest

from src.dossier import drain, reconnaissance, runner
from src.dossier.common import DossierDraining
from src.dossier.schemas import CorpusMap, DossierJob
from src.sources.schemas import Document


@pytest.fixture(autouse=True)
def _clean_drain_flag():
    drain.reset_drain()
    yield
    drain.reset_drain()


def test_drain_flag_round_trip():
    assert drain.is_draining() is False
    drain.request_drain()
    assert drain.is_draining() is True and runner.is_draining() is True and reconnaissance.is_draining() is True
    drain.reset_drain()
    assert drain.is_draining() is False


class _FakeThread:
    made = []

    def __init__(self, *a, **kw):
        self.kw = kw
        _FakeThread.made.append(self)

    def start(self):
        self.started = True


def test_start_refuses_while_draining_and_starts_otherwise(monkeypatch):
    _FakeThread.made.clear()
    monkeypatch.setattr(runner.threading, "Thread", _FakeThread)
    drain.request_drain()
    assert runner.start("d-drain") is False
    assert _FakeThread.made == [] and "d-drain" not in runner._running          # job left alone for the next instance
    drain.reset_drain()
    try:
        assert runner.start("d-go") is True
        assert len(_FakeThread.made) == 1 and _FakeThread.made[0].started and _FakeThread.made[0].kw["name"] == "dossier-d-go"
        assert "d-go" in runner._running and runner.running_count() >= 1
    finally:
        with runner._lock:
            runner._running.discard("d-go")


def _doc(key, text):
    return Document.model_construct(key=key, title=f"Title {key}", text=text, char_count=len(text), creators="x", year="2026", publication="p", stacks_key=key)


def _fake_call_json(calls, *, drain_after_first=False):
    def call_json(job_id, step, *, label, system, user, tool_name, schema, model_cls, max_tokens):
        calls.append(label)
        if drain_after_first and len(calls) == 1:
            drain.request_drain()                                                # SIGTERM lands while this call is in flight
        if tool_name == "record_profiles":
            key = user.split("[")[1].split("]")[0] if "[" in user else "?"
            return {"profiles": [{"doc_key": key, "title": "", "genre": "g", "one_line": "o", "thesis": "t", "method": "m", "key_claims": [], "entities": [], "tensions": []}]}, None
        return CorpusMap(candidate_angles=["a"]), None
    return call_json


def _per_document_path(monkeypatch, calls, **kw):
    monkeypatch.setattr(reconnaissance, "SINGLE_CALL_MAX_CHARS", 10)           # force the per-document path
    monkeypatch.setattr(reconnaissance.events, "emit", lambda *a, **k: None)
    monkeypatch.setattr(reconnaissance, "documents_index", lambda docs: " ".join(f"[{d.key}]" for d in docs))
    monkeypatch.setattr(reconnaissance, "corpus_text", lambda docs, max_chars_per_doc=None: "")
    monkeypatch.setattr(reconnaissance, "call_json", _fake_call_json(calls, **kw))


def test_reconnaissance_pauses_between_documents_when_draining(monkeypatch):
    calls, checkpoints = [], []
    _per_document_path(monkeypatch, calls, drain_after_first=True)
    docs = [_doc("A", "alpha text"), _doc("B", "beta text"), _doc("C", "gamma text")]
    with pytest.raises(DossierDraining) as exc:
        reconnaissance.run_reconnaissance(DossierJob(), docs, persist=lambda **f: checkpoints.append(f["profiles"]))
    assert calls == ["profile 1/3: Title A"]                                       # the call in flight finished, nothing more was bought
    assert "before profile 2/3" in str(exc.value)
    assert len(checkpoints) == 1 and checkpoints[0].partial and [p.doc_key for p in checkpoints[0].profiles] == ["A"]   # on the record for the next instance


def test_reconnaissance_pauses_before_the_corpus_map_when_draining(monkeypatch):
    calls = []
    _per_document_path(monkeypatch, calls)
    docs = [_doc("A", "alpha text"), _doc("B", "beta text")]
    flags = iter([False, False, True])                                           # clean between documents; SIGTERM before the map
    monkeypatch.setattr(reconnaissance, "is_draining", lambda: next(flags))
    with pytest.raises(DossierDraining, match="before the corpus map"):
        reconnaissance.run_reconnaissance(DossierJob(), docs, persist=lambda **f: None)
    assert calls == ["profile 1/2: Title A", "profile 2/2: Title B"]


def test_reconnaissance_runs_to_the_end_when_not_draining(monkeypatch):
    calls = []
    _per_document_path(monkeypatch, calls)
    recon = reconnaissance.run_reconnaissance(DossierJob(), [_doc("A", "alpha text"), _doc("B", "beta text")], persist=lambda **f: None)
    assert [p.doc_key for p in recon.profiles] == ["A", "B"] and recon.partial is False and len(calls) == 3


def _runner_harness(monkeypatch, seen, status="reconnaissance", step="reconnaissance"):
    monkeypatch.setattr(runner, "get_job", lambda job_id: DossierJob(id=job_id, status=status, step=step))
    monkeypatch.setattr(runner, "load_documents", lambda job: [])
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: seen.append(("update", f)))
    monkeypatch.setattr(runner.events, "emit", lambda job_id, kind, **kw: seen.append(("emit", kind, kw)))


def test_runner_treats_draining_mid_step_as_a_pause_not_a_failure(monkeypatch):
    seen = []
    _runner_harness(monkeypatch, seen)
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: (_ for _ in ()).throw(DossierDraining("instance restart before profile 3/9")))
    runner._run("d-x")
    updates = [f for k, *rest in seen if k == "update" for f in rest]
    assert updates == []                                                          # status untouched: still 'reconnaissance' for boot recovery
    notes = [kw for k, kind, kw in [e for e in seen if e[0] == "emit"] if kind == "note"]
    assert len(notes) == 1 and notes[0]["payload_json"]["kind"] == "drain_pause" and notes[0]["phase"] == "reconnaissance"
    assert "resumes on the next instance" in notes[0]["detail"] and "reconnaissance" in notes[0]["detail"]
    assert not any(kind in ("job_failed", "job_finished") for _, kind, *_ in [e for e in seen if e[0] == "emit"])
    assert "d-x" not in runner._running


def test_runner_pauses_between_steps_when_draining_and_records_the_next_step(monkeypatch):
    seen, ran = [], []
    _runner_harness(monkeypatch, seen, status="reconnaissance", step="brief")
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: ran.append(step))
    drain.request_drain()
    runner._run("d-y")
    assert ran == []                                                              # no step started on a dying instance
    assert [f for k, *rest in seen if k == "update" for f in rest] == [{"step": "brief"}]   # step recorded, status untouched
    notes = [(kind, kw) for k, kind, kw in [e for e in seen if e[0] == "emit"] if kind == "note"]
    assert len(notes) == 1 and notes[0][1]["payload_json"] == {"kind": "drain_pause", "step": "brief", "why": "between steps"}


def test_runner_finishes_normally_when_not_draining(monkeypatch):
    seen, ran = [], []
    _runner_harness(monkeypatch, seen, status="crosscheck", step="receipts")
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: ran.append(step))
    runner._run("d-z")
    assert ran == ["receipts"] and ("update", {"status": "done", "step": "receipts"}) in seen


def test_wait_for_idle_returns_at_once_when_nothing_runs_and_times_out_otherwise():
    t0 = time.monotonic()
    assert drain.wait_for_idle(5.0, running_count=lambda: 0) is True
    assert time.monotonic() - t0 < 0.5
    t0 = time.monotonic()
    assert drain.wait_for_idle(0.05, running_count=lambda: 2, poll_s=0.01) is False
    assert 0.04 <= time.monotonic() - t0 < 1.0
    # becomes idle mid-wait
    counts = iter([1, 1, 0])
    assert drain.wait_for_idle(2.0, running_count=lambda: next(counts), poll_s=0.01) is True


def test_wait_for_idle_defaults_to_the_dossier_runner_count():
    assert runner.running_count() == 0
    assert drain.wait_for_idle(0.05, poll_s=0.01) is True
    with runner._lock:
        runner._running.add("d-busy")
    try:
        assert drain.wait_for_idle(0.03, poll_s=0.01) is False
    finally:
        with runner._lock:
            runner._running.discard("d-busy")
