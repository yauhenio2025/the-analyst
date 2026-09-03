"""Tests for the run-event ledger (src/events/store.py) on a temp SQLite DB,
plus the /v1/events routes (JSON list, summary, SSE stream)."""

import json
import sys
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if root_str in sys.path:
    sys.path.remove(root_str)
sys.path.insert(0, root_str)

from src.executor import db as executor_db  # noqa: E402
from src.events import store  # noqa: E402
from src.events.pricing import estimate_cost  # noqa: E402
from src.events.schemas import EVENT_KINDS, RunEvent  # noqa: E402
from src.events import context as events_context  # noqa: E402


@pytest.fixture
def sqlite_store(tmp_path, monkeypatch):
    """Point the executor DB layer at a fresh SQLite file and reset the lazy-init flag."""
    monkeypatch.setattr(executor_db, "DATABASE_URL", "")
    monkeypatch.setattr(executor_db, "SQLITE_PATH", tmp_path / "events-test.db")
    store.reset_for_tests()
    yield store
    store.reset_for_tests()


# ---------------------------------------------------------------------------
# store
# ---------------------------------------------------------------------------

def test_append_and_list_seq_monotonic(sqlite_store):
    job = "job-test-1"
    seqs = [
        store.append_event(job, "job_started", detail="started"),
        store.append_event(job, "phase_started", phase="1.0", detail="phase 1"),
        store.append_event(job, "note", detail="hello", extra_field="folded into payload"),
    ]
    assert seqs == [1, 2, 3]

    events = store.list_events(job)
    assert [e["seq"] for e in events] == [1, 2, 3]
    assert [e["kind"] for e in events] == ["job_started", "phase_started", "note"]
    assert events[1]["phase"] == "1.0"
    assert events[2]["payload"] == {"extra_field": "folded into payload"}
    assert all(e["ts"].endswith("+00:00") for e in events)

    # after_seq / limit
    assert [e["seq"] for e in store.list_events(job, after_seq=1)] == [2, 3]
    assert [e["seq"] for e in store.list_events(job, after_seq=0, limit=2)] == [1, 2]
    assert store.list_events(job, after_seq=3) == []
    assert store.last_seq(job) == 3

    # other jobs have their own sequence
    assert store.append_event("job-test-2", "note", detail="other") == 1
    assert store.list_events("job-test-2")[0]["seq"] == 1

    # every row validates as a RunEvent
    for e in events:
        RunEvent(**e)


def test_all_kinds_accepted(sqlite_store):
    job = "job-kinds"
    for i, kind in enumerate(EVENT_KINDS, start=1):
        assert store.append_event(job, kind, detail=kind) == i
    assert len(store.list_events(job)) == len(EVENT_KINDS)


def test_append_never_raises(sqlite_store, monkeypatch):
    monkeypatch.setattr(executor_db, "SQLITE_PATH", Path("/nonexistent-dir-for-events-test/x.db"))
    store.reset_for_tests()
    assert store.append_event("job-broken", "note", detail="x") == 0
    assert store.list_events("job-broken") == []
    assert store.job_summary("job-broken")["events"] == 0


def test_cost_is_estimated_from_model_when_missing(sqlite_store):
    job = "job-cost"
    store.append_event(
        job, "call_finished", model="claude-sonnet-4-6",
        input_tokens=1_000_000, output_tokens=100_000, duration_ms=1234,
    )
    ev = store.list_events(job)[0]
    assert ev["cost_usd"] == pytest.approx(3.0 + 1.5)
    assert ev["model"] == "claude-sonnet-4-6"

    # unknown model -> null cost (never raises)
    store.append_event(job, "call_finished", model="mystery-model-9", input_tokens=10, output_tokens=10)
    assert store.list_events(job)[1]["cost_usd"] is None

    # explicit cost is preserved
    store.append_event(job, "call_finished", model="claude-sonnet-4-6", input_tokens=10, output_tokens=10, cost_usd=0.5)
    assert store.list_events(job)[2]["cost_usd"] == 0.5


def test_pricing_table():
    assert estimate_cost("claude-haiku-4-5-20251001", 1_000_000, 1_000_000) == pytest.approx(6.0)
    assert estimate_cost("claude-opus-4-6", 1_000_000, 0) == pytest.approx(5.0)
    assert estimate_cost("gemini-3.1-pro-preview", 0, 1_000_000) == pytest.approx(12.0)
    assert estimate_cost("openrouter/anthropic/claude-sonnet-4-6", 1_000_000, 0) == pytest.approx(3.0)
    assert estimate_cost("claude-sonnet-4-6-20991231", 1_000_000, 0) == pytest.approx(3.0)  # family fallback
    assert estimate_cost("totally-unknown", 1, 1) is None
    assert estimate_cost(None, 1, 1) is None


def test_prompt_excerpt_and_hash():
    system = "S" * 5000
    user = "U" * 5000
    excerpt = store.prompt_excerpt(system, user)
    assert excerpt == "S" * 2000 + "\n---\n" + "U" * 1000
    h1 = store.prompt_hash(system, user)
    h2 = store.prompt_hash(system, user + "x")
    assert len(h1) == 64 and h1 != h2
    assert store.output_excerpt("O" * 9000) == "O" * 2000


def test_excerpts_truncated_on_write(sqlite_store):
    job = "job-trunc"
    store.append_event(job, "call_finished", output_excerpt="X" * 9000, prompt_excerpt="P" * 9000, detail="d" * 5000)
    ev = store.list_events(job)[0]
    assert len(ev["output_excerpt"]) == 2000
    assert len(ev["prompt_excerpt"]) <= 3016
    assert len(ev["detail"]) == 1000


def test_job_summary(sqlite_store):
    job = "job-summary"
    store.append_event(job, "job_started", ts="2026-09-03T10:00:00+00:00", detail="go",
                       payload={"workflow_key": "wf"})
    store.append_event(job, "phase_started", phase="1.0", ts="2026-09-03T10:00:01+00:00",
                       payload={"phase_name": "Profile", "engines": ["eng_a"]})
    store.append_event(job, "call_started", phase="1.0", engine="eng_a", model="claude-sonnet-4-6",
                       ts="2026-09-03T10:00:02+00:00")
    store.append_event(job, "call_finished", phase="1.0", engine="eng_a", model="claude-sonnet-4-6",
                       input_tokens=10_000, output_tokens=2_000, duration_ms=30_000,
                       ts="2026-09-03T10:00:32+00:00")
    store.append_event(job, "call_failed", phase="1.0", engine="eng_a", model="claude-sonnet-4-6",
                       ts="2026-09-03T10:00:33+00:00")
    store.append_event(job, "call_finished", phase="1.0", engine="eng_b", model="claude-haiku-4-5-20251001",
                       input_tokens=1_000, output_tokens=500, duration_ms=5_000,
                       ts="2026-09-03T10:00:40+00:00")
    store.append_event(job, "narration", phase="1.0", narrator="This step reads the book.",
                       ts="2026-09-03T10:00:41+00:00")
    store.append_event(job, "phase_finished", phase="1.0", duration_ms=45_000,
                       ts="2026-09-03T10:00:46+00:00",
                       payload={"phase_name": "Profile", "status": "completed"})
    store.append_event(job, "phase_started", phase="2.0", ts="2026-09-03T10:00:47+00:00",
                       payload={"phase_name": "Scan"})

    s = store.job_summary(job)
    assert s["status"] == "running"
    assert s["calls"] == 2
    assert s["failed_calls"] == 1
    assert s["input_tokens"] == 11_000
    assert s["output_tokens"] == 2_500
    expected_cost = (10_000 * 3 + 2_000 * 15) / 1e6 + (1_000 * 1 + 500 * 5) / 1e6
    assert s["cost_usd"] == pytest.approx(expected_cost)
    assert s["duration_ms"] == 47_000  # first event -> last event
    assert s["events"] == 9 and s["last_seq"] == 9

    assert [p["phase"] for p in s["phases"]] == ["1.0", "2.0"]
    p1 = s["phases"][0]
    assert p1["name"] == "Profile"
    assert p1["status"] == "completed"
    assert p1["calls"] == 2
    assert p1["input_tokens"] == 11_000
    assert p1["duration_ms"] == 45_000
    assert p1["narrator"] == "This step reads the book."
    assert set(p1["engines"]) == {"eng_a", "eng_b"}
    p2 = s["phases"][1]
    assert p2["status"] == "running" and p2["calls"] == 0

    store.append_event(job, "job_finished", ts="2026-09-03T10:01:00+00:00", payload={"status": "completed"})
    s2 = store.job_summary(job)
    assert s2["status"] == "completed"
    assert s2["duration_ms"] == 60_000
    assert store.has_terminal_event(job)

    store.append_event("job-failed", "job_failed", payload={"status": "cancelled"})
    assert store.job_summary("job-failed")["status"] == "cancelled"


def test_concurrent_appends_keep_seq_unique(sqlite_store):
    job = "job-threads"
    results: list[int] = []
    lock = threading.Lock()

    def worker(n: int) -> None:
        for i in range(10):
            seq = store.append_event(job, "note", detail=f"t{n}-{i}")
            with lock:
                results.append(seq)

    threads = [threading.Thread(target=worker, args=(n,)) for n in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(results) == 50
    assert 0 not in results
    assert sorted(results) == list(range(1, 51))
    assert [e["seq"] for e in store.list_events(job, limit=100)] == list(range(1, 51))


def test_payload_json_roundtrip_and_objects(sqlite_store):
    job = "job-payload"
    store.append_event(job, "artifact", payload={"nested": {"a": [1, 2, 3]}, "path": Path("/tmp/x")})
    ev = store.list_events(job)[0]
    assert ev["payload"]["nested"] == {"a": [1, 2, 3]}
    assert ev["payload"]["path"] == "/tmp/x"


# ---------------------------------------------------------------------------
# context
# ---------------------------------------------------------------------------

def test_context_scope_merges_and_restores():
    assert events_context.current() == {}
    with events_context.scope(job_id="j", phase="1.0"):
        assert events_context.current() == {"job_id": "j", "phase": "1.0"}
        with events_context.scope(engine="e", pass_name="Pass 1"):
            assert events_context.current()["engine"] == "e"
            assert events_context.current()["job_id"] == "j"
        assert "engine" not in events_context.current()
    assert events_context.current() == {}
    assert events_context.phase_key(1) == "1.0"
    assert events_context.phase_key(1.5) == "1.5"
    assert events_context.phase_key(None) is None


def test_new_threads_start_with_empty_context():
    seen = {}
    with events_context.scope(job_id="parent"):
        t = threading.Thread(target=lambda: seen.update(ctx=events_context.current()))
        t.start()
        t.join()
    assert seen["ctx"] == {}


# ---------------------------------------------------------------------------
# hooks (use the store; narrator disabled)
# ---------------------------------------------------------------------------

def test_hooks_emit_call_events_via_engine_runner_context(sqlite_store, monkeypatch):
    monkeypatch.setenv("EVENTS_NARRATOR", "off")
    from src.events import hooks

    job = "job-hooks"
    ctx = {"job_id": job, "phase": "1.0", "chain": "c", "engine": "eng", "pass_name": "Pass 1: Discovery",
           "stance": "discovery", "work_key": None}
    hooks.call_started(job, ctx, model="claude-sonnet-4-6", system_prompt="sys", user_message="usr",
                       attempt=1, max_attempts=5, label="L")
    hooks.call_finished(job, ctx, model="claude-sonnet-4-6", system_prompt="sys", user_message="usr",
                        content="out", input_tokens=100, output_tokens=50, thinking_tokens=0,
                        duration_ms=10, attempt=1)
    hooks.call_failed(job, ctx, model="claude-sonnet-4-6", system_prompt="sys", user_message="usr",
                      error="boom", duration_ms=5, attempt=2, max_attempts=5, will_retry=True, retry_delay_s=30)
    events = store.list_events(job)
    assert [e["kind"] for e in events] == ["call_started", "call_finished", "call_failed"]
    started, finished, failed = events
    assert started["prompt_excerpt"] == "sys\n---\nusr"
    assert started["prompt_hash"] == store.prompt_hash("sys", "usr")
    assert started["input_chars"] == 6
    assert finished["output_excerpt"] == "out"
    assert finished["cost_usd"] == pytest.approx((100 * 3 + 50 * 15) / 1e6)
    assert finished["engine"] == "eng" and finished["stance"] == "discovery"
    assert "claude-sonnet-4-6" in finished["detail"]
    assert failed["payload"]["will_retry"] is True and failed["payload"]["retry_delay_s"] == 30


def test_hooks_job_and_phase_events(sqlite_store, monkeypatch):
    monkeypatch.setenv("EVENTS_NARRATOR", "off")
    from src.events import hooks
    from src.executor.schemas import PhaseResult, PhaseStatus
    from src.orchestrator.schemas import PhaseExecutionSpec, TargetWork, WorkflowExecutionPlan
    from src.workflows.schemas import WorkflowPhase

    job = "job-hooks-2"
    plan = WorkflowExecutionPlan(
        workflow_key="intellectual_genealogy",
        thinker_name="Author",
        target_work=TargetWork(title="Book", description="d"),
        strategy_summary="Do the thing.",
        phases=[
            PhaseExecutionSpec(phase_number=1.0, phase_name="Synthesis", engine_key="aoi_thematic_synthesis"),
            PhaseExecutionSpec(phase_number=2.0, phase_name="Mapping", engine_key="aoi_engagement_mapping",
                               depends_on=[1.0], context_emphasis="focus on X"),
        ],
        estimated_llm_calls=4,
    )
    wf1 = WorkflowPhase(phase_number=1.0, phase_name="Synthesis", phase_description="Read the sources.",
                        engine_key="aoi_thematic_synthesis")
    wf2 = WorkflowPhase(phase_number=2.0, phase_name="Mapping", phase_description="Map engagements.",
                        engine_key="aoi_engagement_mapping", depends_on_phases=[1.0])

    assert hooks.job_started(job, plan, None) == 1
    assert hooks.phase_started(job, plan, wf1, plan.phases[0]) == 2
    assert hooks.phase_started(job, plan, wf2, plan.phases[1]) == 3
    result = PhaseResult(phase_number=2.0, phase_name="Mapping", status=PhaseStatus.COMPLETED,
                         duration_ms=1500, total_tokens=10, final_output="final prose")
    assert hooks.phase_finished(job, plan.phases[1], result) == 4
    assert hooks.job_finished(job, "completed") == 5

    events = store.list_events(job)
    js = events[0]
    assert js["payload"]["workflow_key"] == plan.workflow_key
    assert [p["phase"] for p in js["payload"]["phases"]] == ["1.0", "2.0"]
    assert js["payload"]["phases"][1]["depends_on"] == ["1.0"]
    ps = events[2]
    assert ps["phase"] == "2.0"
    assert ps["payload"]["engines"] == ["aoi_engagement_mapping"]
    assert ps["payload"]["depends_on"] == ["1.0"]
    assert ps["payload"]["context_emphasis"] == "focus on X"
    pf = events[3]
    assert pf["kind"] == "phase_finished" and pf["payload"]["status"] == "completed"
    assert pf["output_excerpt"] == "final prose"
    assert events[4]["kind"] == "job_finished" and events[4]["payload"]["status"] == "completed"

    # failure / cancellation map onto job_failed with a status payload
    hooks.job_finished(job, "cancelled")
    assert store.list_events(job)[-1]["kind"] == "job_failed"
    assert store.list_events(job)[-1]["payload"]["status"] == "cancelled"


def test_narrator_prompt_and_cache(sqlite_store, monkeypatch):
    from src.events import narrator

    narrator.clear_cache()
    prompt = narrator.build_narration_prompt(
        {"phase": "2.0", "phase_name": "Mapping", "description": "Map it", "engines": [{"key": "e", "name": "Engine"}],
         "depends_on": [{"phase": "1.0", "phase_name": "Synthesis"}], "context_emphasis": "X"},
        {"workflow_key": "wf", "strategy_summary": "S"},
    )
    assert "phase 2.0: Mapping" in prompt and "Receives the output of: phase 1.0 (Synthesis)" in prompt

    # disabled -> no event, no thread
    monkeypatch.setenv("EVENTS_NARRATOR", "off")
    assert narrator.narrate_phase_async("job-n", "wf", "2.0", {"phase": "2.0"}, {}) is None
    assert store.list_events("job-n") == []

    # enabled with a fake API: thread runs, event emitted, second call served from cache
    monkeypatch.delenv("EVENTS_NARRATOR", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    calls = []

    def fake_call(prompt, *, model=narrator.NARRATOR_MODEL):
        calls.append(prompt)
        return "It reads the book to find its main claims."

    monkeypatch.setattr(narrator, "call_narrator", fake_call)
    t = narrator.narrate_phase_async("job-n", "wf", "2.0", {"phase": "2.0", "phase_name": "Mapping"}, {})
    assert t is not None
    t.join(timeout=5)
    ev = store.list_events("job-n")
    assert len(ev) == 1 and ev[0]["kind"] == "narration"
    assert ev[0]["narrator"] == "It reads the book to find its main claims."
    assert ev[0]["payload"]["cached"] is False

    assert narrator.narrate_phase_async("job-n2", "wf", "2.0", {"phase": "2.0"}, {}) is None
    ev2 = store.list_events("job-n2")
    assert len(ev2) == 1 and ev2[0]["payload"]["cached"] is True
    assert len(calls) == 1
    narrator.clear_cache()


# ---------------------------------------------------------------------------
# API routes (events router only — avoids booting the whole app)
# ---------------------------------------------------------------------------

@pytest.fixture
def events_client(sqlite_store, monkeypatch):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from src.api.routes import events as events_routes

    monkeypatch.setattr(events_routes, "POLL_INTERVAL_S", 0.05)
    monkeypatch.setattr(events_routes, "HEARTBEAT_INTERVAL_S", 0.2)
    monkeypatch.setattr(events_routes, "CLOSE_AFTER_TERMINAL_S", 0.3)
    app = FastAPI()
    app.include_router(events_routes.router)
    return TestClient(app)


def test_events_routes_list_and_summary(events_client):
    job = "job-api"
    store.append_event(job, "job_started", detail="go")
    store.append_event(job, "call_finished", phase="1.0", model="claude-sonnet-4-6",
                       input_tokens=1000, output_tokens=100, duration_ms=10)

    r = events_client.get(f"/v1/events/{job}")
    assert r.status_code == 200
    body = r.json()
    assert [e["seq"] for e in body] == [1, 2]
    assert body[1]["cost_usd"] == pytest.approx((1000 * 3 + 100 * 15) / 1e6)
    assert body[0]["payload"] == {}

    r = events_client.get(f"/v1/events/{job}", params={"after": 1, "limit": 5})
    assert [e["seq"] for e in r.json()] == [2]

    r = events_client.get(f"/v1/events/{job}/summary")
    assert r.status_code == 200
    s = r.json()
    assert s["calls"] == 1 and s["status"] == "running" and s["last_seq"] == 2

    assert events_client.get("/v1/events/no-such-job").json() == []


def test_events_stream_replays_then_closes_after_terminal(events_client):
    job = "job-sse"
    store.append_event(job, "job_started", detail="go")
    store.append_event(job, "note", detail="middle")
    store.append_event(job, "job_finished", detail="done", payload={"status": "completed"})

    frames: list[str] = []
    with events_client.stream("GET", f"/v1/events/{job}/stream", params={"after": 1}) as r:
        assert r.status_code == 200
        assert r.headers["content-type"].startswith("text/event-stream")
        for line in r.iter_lines():
            frames.append(line)

    text = "\n".join(frames)
    assert "event: run_event" in text
    data_lines = [l for l in frames if l.startswith("data: ")]
    payloads = [json.loads(l[len("data: "):]) for l in data_lines]
    assert [p["seq"] for p in payloads] == [2, 3]  # replay honours ?after=
    assert payloads[-1]["kind"] == "job_finished"
    assert any(l.startswith(": closed") for l in frames)
