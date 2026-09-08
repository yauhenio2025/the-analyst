"""Question development over real routes and isolated persistence; no model calls."""
import copy
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.routes.questions import router
from src.inquiries import service as shared
from src.questions import service
from src.readings import registry as readings


@pytest.fixture
def client(tmp_path, monkeypatch):
    from src.executor import db
    from src.dossier import blob_store
    from src.engines import history_tracker
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "questions.sqlite")
    monkeypatch.setattr(blob_store, "_ready", False)
    monkeypatch.setattr(history_tracker, "HISTORY_DIR", tmp_path / "history")
    app = FastAPI()
    app.include_router(router, prefix="/v1")
    with TestClient(app) as client:
        yield client


@pytest.fixture
def context():
    return {"question_id": "stacks:question:1", "revision": 1,
            "problem": "Why do similar forms of market dependence accompany development and underdevelopment?",
            "motivation": "Make the difference in outcomes intelligible.", "commitments": []}


@pytest.fixture
def input_data(context):
    return {"method": "question_development", "phase": "development", "context": context, "sources": []}


@pytest.fixture
def result():
    return {"summary": "Ask what produces the difference without assuming growth is the default.",
        "proposal": {"status": "proposed", "question": "Under what conditions does market dependence produce divergent outcomes?",
            "motivation": "Explain the divergence rather than treat underdevelopment as a residual.",
            "change": "Both outcomes become part of the explanandum.",
            "assumptions": [{"text": "Market dependence may be compatible with distinct outcomes.",
                             "status": "proposed", "commitment_ids": []}],
            "enables": "Compare mechanisms that generate different outcomes.", "preserves": [], "retires": []},
        "alternatives": [{"id": "A1", "question": "Which relations connect the two outcomes?",
                          "reason": "Focus on a possible interdependence rather than parallel outcomes."}],
        "prerequisites": [{"id": "P1", "question": "What counts as development in this comparison?",
                           "reason": "The comparison needs a defensible outcome definition."}],
        "evidence": [], "next_activity": {"kind": "exploration", "question": "Which mechanisms could explain divergent outcomes?",
            "reason": "There is no settled account to test yet.", "commitment_ids": []}}


@pytest.fixture
def discovery(context):
    return {"method": "question_preparation", "phase": "discovery", "context": context}


@pytest.fixture
def plan():
    return {"phase": "discovery", "status": "ready", "needs_sources": False,
            "research_brief": "Clarify the explanatory object and its assumptions before searching.",
            "rationale": "The supplied problem supports a conceptual reframing now.", "evidence_requirements": [],
            "selected_sources": [], "selected_prior_reading_ids": [],
            "coverage": "The author's problem only; no claim about an unread source.", "gaps": []}


def prepare(client, data):
    response = client.post("/v1/questions/prepare", json=data)
    assert response.status_code == 200, response.text
    return response.json()


def complete_body(p, data, result):
    return {**{k: p[k] for k in ("prepared_id", "input_fingerprint", "method_fingerprint")},
            "input": data, "result": result, "execution": {"provider": "fixture_subscription", "cost_usd": 0}}


def finish(client, p, data, result):
    return client.post("/v1/questions/complete", json=complete_body(p, data, result))


def add_source(data):
    data["sources"] = [{"key": "em:CASE", "uid": "em:CASE", "title": "A case with divergent outcomes", "version": "v1",
                        "authors": ["Example, Author"], "text": "  [p. 2]\nThe same market relations accompanied sharply different local outcomes.\n"}]


def add_evidence(result):
    result["evidence"] = [{"id": "E1", "source_key": "em:CASE",
        "quote": "The same market relations accompanied sharply different local outcomes.",
        "claim": "The source reports divergent outcomes under similar market relations.", "role": "context", "locus": "p. 2"}]


def add_commitment(data):
    data["context"]["commitments"] = [{"id": "part:1", "text": "Development and underdevelopment may be systemic.",
        "part_id": 1, "version_id": 3, "approved": True}]


def test_problem_without_commitments_or_sources_produces_proposed_question_not_accepted_belief(client, input_data, result):
    p = prepare(client, input_data)
    assert p == prepare(client, input_data)
    assert "A question may emerge before" in p["system_prompt"]
    assert p["source_manifest"] == []
    response = finish(client, p, input_data, result)
    assert response.status_code == 200, response.text
    receipt = response.json()
    assert receipt["result"]["proposal"]["status"] == "proposed"
    assert receipt["validation"]["conceptual_only"] is True
    record = readings.reading(receipt["receipt_id"], "question_development")
    assert record["sources"] == record["texts"] == record["persons"] == []
    assert record["rows"][0]["conjecture"] and record["rows"][0]["doc"] == ""
    assert record["kind"] == "question_development"
    assert readings.readings_for(job=receipt["receipt_id"])["count"] == 1
    assert client.get("/v1/questions/receipts/" + receipt["receipt_id"]).json()["result"] == receipt["result"]


def test_primary_reading_retains_source_identity_coverage_and_origin_separately_from_proposal(client, input_data, result):
    add_source(input_data); add_evidence(result)
    input_data["context"].update(origin_inquiry={"id": "old:1", "attempt_id": 3},
        preparation={"coverage": [{"source_key": "em:CASE", "whole_rendition": False,
            "ranges": [{"start": 10, "end": 87}], "rendition_version": "original-hash"}],
            "context_gaps": ["Earlier case not supplied."]},
        prior_readings=[{"job_id": "prior", "phase": "construction", "rows": [{"text": "An inherited conjecture."}]}])
    p = prepare(client, input_data)
    assert p["source_manifest"][0]["text_sha256"] == hashlib.sha256(input_data["sources"][0]["text"].encode()).hexdigest()
    response = finish(client, p, input_data, result)
    assert response.status_code == 200, response.text
    receipt = response.json()
    assert receipt["validation"]["verified_anchors"] == 1
    record = readings.reading(receipt["receipt_id"], "question_development")
    assert record["context"]["preparation"] == input_data["context"]["preparation"]
    assert record["context"]["origin_inquiry"] == {"id": "old:1", "attempt_id": 3}
    assert readings.readings_for(text="em:CASE")["count"] == 1
    assert readings.readings_for(person="Example")["count"] == 1


@pytest.mark.parametrize("change", ["problem", "motivation", "current_question", "origin", "coverage", "source", "method_fingerprint"])
def test_changed_problem_purpose_source_or_provenance_cannot_complete_frozen_question(client, input_data, result, change):
    add_source(input_data)
    p = prepare(client, input_data)
    body = complete_body(p, input_data, result)
    if change == "method_fingerprint": body[change] = "changed"
    elif change == "source": input_data["sources"][0]["text"] += "A later rendition."
    elif change == "origin": input_data["context"]["origin_inquiry"] = {"id": "different"}
    elif change == "coverage": input_data["context"]["preparation"] = {"coverage": "A different selection"}
    else: input_data["context"][change] = "A substantively different problem or purpose."
    assert client.post("/v1/questions/complete", json=body).status_code == 409


def test_method_change_does_not_destroy_pending_completion_and_different_result_conflicts(client, input_data, result, monkeypatch):
    p = prepare(client, input_data)
    monkeypatch.setattr(shared, "method_record", lambda _: pytest.fail("Completion uses its frozen method"))
    first = finish(client, p, input_data, result)
    again = finish(client, p, input_data, result)
    assert first.status_code == again.status_code == 200 and again.json()["replayed"]
    result["proposal"]["question"] = "An alternative that cannot overwrite this receipt?"
    assert finish(client, p, input_data, result).status_code == 409


@pytest.mark.parametrize("change", ["unknown_commitment", "unapproved", "invented_belief", "missing_handoff_commitment", "unknown_source", "context_as_source", "accepted_proposal", "duplicate_id", "verification_flag"])
def test_unfounded_author_and_source_references_are_rejected(client, input_data, result, change):
    add_commitment(input_data)
    if change == "unknown_commitment": result["proposal"]["assumptions"][0]["commitment_ids"] = ["invented"]
    elif change == "unapproved":
        input_data["context"]["commitments"][0]["approved"] = False
        result["next_activity"].update(kind="constructive_inquiry", commitment_ids=["part:1"])
    elif change == "invented_belief": result["proposal"]["assumptions"][0]["status"] = "author_stated"
    elif change == "missing_handoff_commitment": result["next_activity"]["kind"] = "constructive_inquiry"
    elif change == "unknown_source": add_evidence(result)
    elif change == "context_as_source":
        input_data["context"]["prior_readings"] = [{"source_key": "em:CASE", "text": "A prior model's answer."}]
        add_evidence(result)
    elif change == "accepted_proposal": result["proposal"]["status"] = "accepted"
    elif change == "duplicate_id": result["alternatives"][0]["id"] = "proposal"
    else:
        add_source(input_data); add_evidence(result)
        result["evidence"][0]["verified"] = True
    assert finish(client, prepare(client, input_data), input_data, result).status_code == 422


@pytest.mark.parametrize("approved", [True, None])
def test_constructive_handoff_can_reference_actual_approved_or_explicit_commitment(client, input_data, result, approved):
    add_commitment(input_data)
    input_data["context"]["commitments"][0]["approved"] = approved
    result["proposal"]["assumptions"][0].update(status="author_stated", commitment_ids=["part:1"])
    result["next_activity"].update(kind="constructive_inquiry", commitment_ids=["part:1"])
    response = finish(client, prepare(client, input_data), input_data, result)
    assert response.status_code == 200, response.text
    assert response.json()["result"]["next_activity"]["commitment_ids"] == ["part:1"]
    assert response.json()["result"]["proposal"]["status"] == "proposed"


@pytest.mark.parametrize("kind", ["author_investigation", "exploration", "author_clarification", "pause"])
def test_other_next_activities_do_not_require_a_settled_account(client, input_data, result, kind):
    result["next_activity"]["kind"] = kind
    assert finish(client, prepare(client, input_data), input_data, result).status_code == 200


@pytest.mark.parametrize("quote,status", [("Invented evidence must remain visibly unverified.", "quote_not_found"), ("The same", "quote_too_short")])
def test_quote_wall_preserves_unverified_evidence_without_endorsing_interpretation(client, input_data, result, quote, status):
    add_source(input_data); add_evidence(result)
    result["evidence"][0]["quote"] = quote
    response = finish(client, prepare(client, input_data), input_data, result)
    assert response.status_code == 200, response.text
    evidence = response.json()["result"]["evidence"][0]
    assert evidence["verified"] is False and evidence["anchor_status"] == status
    assert response.json()["result"]["proposal"]["status"] == "proposed"


def test_wrong_source_quote_is_not_silently_moved_to_the_matching_source(client, input_data, result):
    add_source(input_data); add_evidence(result)
    input_data["sources"].append({"key": "em:OTHER", "title": "Another source", "text": "An unrelated account of the history."})
    result["evidence"][0]["source_key"] = "em:OTHER"
    response = finish(client, prepare(client, input_data), input_data, result).json()
    assert response["result"]["evidence"][0]["anchor_status"] == "quote_not_found"


def test_discovery_can_skip_source_operations_without_inventing_a_commitment(client, discovery, plan):
    p = prepare(client, discovery)
    response = finish(client, p, discovery, plan)
    assert response.status_code == 200, response.text
    receipt = response.json()
    assert receipt["result"]["needs_sources"] is False
    assert "reading" not in receipt
    assert readings.readings_for(job=receipt["receipt_id"])["count"] == 0


@pytest.fixture
def selection(discovery, plan):
    discovery.update(phase="selection", discovery_plan={**plan, "needs_sources": True},
        candidates=[{"key": "em:FULL", "title": "Complete case rendition", "chars": 255_066, "readable": True},
                    {"key": "em:BOOK", "title": "A book", "chars": 487_405, "readable": True,
                     "windows": [{"id": "chapter:3", "chars": 20_000, "locus": "Chapter 3"}]},
                    {"key": "em:MISSING", "title": "Missing article", "chars": 0, "readable": False}],
        prior_readings=[{"id": "prior:1", "job_id": "old", "phase": "reading", "summary": "A prior conjecture."}],
        availability={"wants": [{"title": "Missing article", "acq_status": "queued"}], "omitted_uids": ["em:OMITTED"]})
    return discovery


@pytest.fixture
def selected(plan):
    return {**plan, "phase": "selection", "needs_sources": True,
            "selected_sources": [{"source_key": "em:FULL", "window_ids": []},
                                 {"source_key": "em:BOOK", "window_ids": ["chapter:3"]}],
            "selected_prior_reading_ids": ["prior:1"]}


def test_selection_uses_supplied_windows_and_freezes_pending_evidence(client, selection, selected):
    p = prepare(client, selection)
    assert json.loads(p["user_prompt"])["input"]["availability"] == selection["availability"]
    response = finish(client, p, selection, selected)
    assert response.status_code == 200, response.text
    assert response.json()["validation"]["selected_chars"] == 275_066
    selection["availability"]["wants"][0]["acq_status"] = "arrived"
    assert finish(client, p, selection, selected).status_code == 409


def test_missing_evidence_can_yield_explicitly_limited_conceptual_progress(client, selection, selected):
    selected.update(needs_sources=False, selected_sources=[],
        rationale="We can first clarify what a systemic explanation would need to explain.",
        coverage="Conceptual development only; the missing article has not been read.",
        gaps=["Source claims await the readable article."])
    assert finish(client, prepare(client, selection), selection, selected).status_code == 200


@pytest.mark.parametrize("change", ["source", "window", "memory", "unreadable", "budget", "source_count", "memory_count", "disjoint", "phase", "no_sources", "conceptual_with_sources"])
def test_invalid_selections_cannot_materialize_invented_or_over_budget_evidence(client, selection, selected, change):
    if change == "source": selected["selected_sources"][0]["source_key"] = "invented"
    elif change == "window": selected["selected_sources"][0]["window_ids"] = ["invented"]
    elif change == "memory": selected["selected_prior_reading_ids"] = ["invented"]
    elif change == "unreadable": selected["selected_sources"] = [{"source_key": "em:MISSING"}]
    elif change == "budget": selected["selected_sources"][1]["window_ids"] = []
    elif change == "source_count": selection["budget"] = {"max_sources": 1}
    elif change == "memory_count": selection["budget"] = {"max_prior_readings": 0}
    elif change == "disjoint": selected["selected_sources"][1]["window_ids"] = ["chapter:3", "chapter:4"]
    elif change == "phase": selected.update(phase="discovery", selected_sources=[], selected_prior_reading_ids=[])
    elif change == "no_sources": selected["selected_sources"] = []
    else: selected["needs_sources"] = False
    assert finish(client, prepare(client, selection), selection, selected).status_code == 422


def test_blocked_plan_requires_specific_gap(client, discovery, plan):
    plan.update(status="blocked")
    p = prepare(client, discovery)
    assert finish(client, p, discovery, plan).status_code == 422
    plan["gaps"] = ["The problem names two incompatible meanings of development without an intended relation."]
    assert finish(client, p, discovery, plan).status_code == 200


@pytest.mark.parametrize("change", ["wrong_method", "planning_primary", "selection_without_plan", "conceptual_selection", "development_candidates", "primary_budget", "malformed_previous"])
def test_invalid_prepare_contracts_fail_before_execution(client, input_data, selection, change):
    data = input_data
    if change == "wrong_method": data["method"] = "question_preparation"
    elif change == "planning_primary":
        data = selection
        add_source(data)
    elif change == "selection_without_plan":
        data = selection
        data.pop("discovery_plan")
    elif change == "conceptual_selection":
        data = selection
        data["discovery_plan"]["needs_sources"] = False
    elif change == "development_candidates": data["candidates"] = selection["candidates"]
    elif change == "primary_budget":
        add_source(data)
        data["budget"] = {"max_chars": 1}
    else: data["context"]["previous_result"] = {"proposal": {"question": "Incomplete"}}
    assert client.post("/v1/questions/prepare", json=data).status_code == 422


def test_previous_proposal_and_author_correction_survive_as_context_not_accepted_state(client, input_data, result):
    add_source(input_data); add_evidence(result)
    first = finish(client, prepare(client, input_data), input_data, result).json()
    input_data["context"].update(revision=2, current_question="How do relations between regions shape both outcomes?",
        previous_result=first["result"], author_responses=[{"decision": "rewrite", "text": "The relation between outcomes is my real concern."}])
    p = prepare(client, input_data)
    assert "The relation between outcomes" in p["user_prompt"]
    response = finish(client, p, input_data, result)
    assert response.status_code == 200, response.text
    assert response.json()["result"]["proposal"]["status"] == "proposed"


def test_immutable_feedback_is_resolved_from_events_even_after_stale_index_write(client, input_data, result):
    receipt = finish(client, prepare(client, input_data), input_data, result).json()
    stale = readings.reading(receipt["receipt_id"], "question_development")
    path = "/v1/questions/receipts/" + receipt["receipt_id"] + "/feedback"
    event = {"feedback_id": "stacks:feedback:1", "text": "I want the relation between outcomes explained, not just their difference.",
             "decision": "rewrite", "revision_id": "proposal"}
    first, again = client.post(path, json=event), client.post(path, json=event)
    assert first.status_code == again.status_code == 200 and first.json() == again.json()
    readings.save_reading(stale, strict=True)
    assert readings.reading(receipt["receipt_id"], "question_development")["author_feedback"][0]["text"] == event["text"]
    assert client.get(path.removesuffix("/feedback")).json()["result"]["proposal"]["status"] == "proposed"
    event["text"] = "A different event cannot replace the saved correction."
    assert client.post(path, json=event).status_code == 409
    event.update(feedback_id="new", revision_id="invented")
    assert client.post(path, json=event).status_code == 422


def test_conflicting_concurrent_results_have_one_immutable_winner(client, input_data, result):
    p = prepare(client, input_data)
    a = complete_body(p, input_data, result)
    b = copy.deepcopy(a)
    b["result"]["proposal"]["question"] = "A genuinely different question?"
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda body: client.post("/v1/questions/complete", json=body), [a, b]))
    assert sorted(r.status_code for r in responses) == [200, 409]
    receipt = next(r.json() for r in responses if r.status_code == 200)
    assert readings.readings_for(job=receipt["receipt_id"])["count"] == 1


def test_retry_repairs_interrupted_index_without_replacing_saved_answer(client, input_data, result, monkeypatch):
    p = prepare(client, input_data)
    original = readings.save_reading
    monkeypatch.setattr(readings, "save_reading", lambda *a, **k: (_ for _ in ()).throw(RuntimeError("index unavailable")))
    with pytest.raises(RuntimeError, match="index unavailable"):
        finish(client, p, input_data, result)
    monkeypatch.setattr(readings, "save_reading", original)
    response = finish(client, p, input_data, result)
    assert response.status_code == 200 and response.json()["replayed"]
    assert readings.readings_for(job=response.json()["receipt_id"])["count"] == 1


def test_missing_central_method_has_no_local_fallback(client, input_data, monkeypatch):
    from src.operationalizations import registry
    class Empty:
        def get(self, key):
            return None
    monkeypatch.setattr(registry, "get_operationalization_registry", lambda: Empty())
    assert client.post("/v1/questions/prepare", json=input_data).status_code == 503
