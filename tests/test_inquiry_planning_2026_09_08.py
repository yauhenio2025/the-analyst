"""Exercise preparation over actual API schemas and isolated durable storage."""
import copy
import json
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.routes.inquiries import router
from src.inquiries import service
from src.readings import registry as readings


@pytest.fixture
def client(tmp_path, monkeypatch):
    from src.executor import db
    from src.dossier import blob_store
    from src.engines import history_tracker
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "planning.sqlite")
    monkeypatch.setattr(blob_store, "_ready", False)
    monkeypatch.setattr(history_tracker, "HISTORY_DIR", tmp_path / "history")
    app = FastAPI()
    app.include_router(router, prefix="/v1")
    return TestClient(app)


@pytest.fixture
def discovery():
    return {"method": "inquiry_preparation", "phase": "discovery", "context": {
        "inquiry_id": "stacks:1", "revision": 1, "question": "Develop the account through Calabria.",
        "commitments": [{"id": "part:1", "text": "Development and underdevelopment can be systemic.",
                         "approved": True, "version_id": 11}],
        "author_responses": [{"decision": "correct", "text": "Cases should extend the theory."}]}}


@pytest.fixture
def plan():
    return {"phase": "discovery", "status": "ready", "selected_commitment_ids": ["part:1"],
        "selected_test_id": None, "research_brief": "Find the full Arrighi–Piselli Calabria article.",
        "rationale": "The case should expose an explanatory addition or limit.",
        "evidence_requirements": ["The whole case argument, with contrary evidence."],
        "selected_sources": [], "selected_prior_reading_ids": [],
        "coverage": "Discovery only; no primary evidence has been read.", "gaps": []}


@pytest.fixture
def selection(discovery, plan):
    return {**discovery, "phase": "selection", "discovery_plan": plan,
        "sources": [
            {"key": "em:FULL", "title": "Capitalist Development in Hostile Environments", "chars": 255_066,
             "readable": True, "coverage": "Held article rendition; 104 page-marker blocks.", "preview": "Opening passage"},
            {"key": "em:BOOK", "title": "A related book", "chars": 487_405, "readable": True,
             "windows": [{"id": "chapter:3", "chars": 50_000, "locus": "Chapter 3", "preview": "Chapter opening"},
                         {"id": "chapter:4", "chars": 180_000, "locus": "Chapter 4"}]},
            {"key": "em:MISSING", "title": "Unheld evidence", "chars": 0, "readable": False}],
        "prior_readings": [{"id": "read:1", "job_id": "prior-job", "phase": "construction",
                            "summary": "Prior conjecture", "source_keys": ["em:FULL"]}],
        "budget": {"max_chars": 400_000, "max_sources": 2, "max_prior_readings": 1}}


@pytest.fixture
def packet(plan):
    return {**copy.deepcopy(plan), "phase": "selection", "selected_sources": [{"source_key": "em:FULL", "window_ids": []}],
        "selected_prior_reading_ids": ["read:1"], "coverage": "The held article rendition and prior context."}


def prepared(client, data):
    response = client.post("/v1/inquiries/planning/prepare", json=data)
    assert response.status_code == 200, response.text
    return response.json()


def completion(p, data, result):
    return {"prepared_id": p["prepared_id"], "input_fingerprint": p["input_fingerprint"],
            "method_fingerprint": p["method_fingerprint"], "input": data, "result": result,
            "execution": {"provider": "claude_subscription", "model": "fixture", "cost_usd": 0}}


def finish(client, p, data, result):
    return client.post("/v1/inquiries/planning/complete", json=completion(p, data, result))


def prior_result():
    return {"summary": "A proposed account.", "proposed_account": {"status": "proposed", "text": "An account.",
        "derivation": "A derivation.", "mechanism": "A mechanism.", "scope": "A scope.",
        "commitment_ids": ["part:1"], "evidence_ids": []}, "evidence": [], "new_questions": [],
        "tests": [{"id": "T1", "question": "Does dispossession produce growth?", "procedure": "Compare cases.",
            "discriminates": "Two accounts.", "evidence_needed": "A second case.", "source_keys": []},
            {"id": "T2", "question": "Does a different mechanism apply?", "procedure": "Examine differences.",
            "discriminates": "Alternative mechanisms.", "evidence_needed": "Contrary evidence.", "source_keys": []}],
        "revisions": [], "self_scrutiny": "The account remains tentative.", "test_outcome": None}


def test_discovery_roundtrip_freezes_central_method_and_returns_receipt_without_primary_reading(client, discovery, plan):
    p = prepared(client, discovery)
    assert p == prepared(client, discovery)
    assert "Prepare the thinking environment" in p["system_prompt"]
    assert "Cases should extend the theory." in p["user_prompt"]
    frozen = json.loads(p["user_prompt"])["input"]
    assert frozen["context"]["commitments"][0]["version_id"] == 11
    response = finish(client, p, discovery, plan)
    assert response.status_code == 200, response.text
    receipt = response.json()
    assert receipt["validation"]["selected_chars"] == 0
    assert receipt["result"]["selected_sources"] == []
    assert client.get("/v1/inquiries/planning/receipts/" + receipt["receipt_id"]).json()["result"] == plan
    assert readings.readings_for(job=receipt["receipt_id"])["count"] == 0


def test_selection_respects_full_article_budget_and_carries_only_selected_memory(client, selection, packet):
    response = finish(client, prepared(client, selection), selection, packet)
    assert response.status_code == 200, response.text
    assert response.json()["validation"]["selected_chars"] == 255_066
    assert response.json()["result"]["selected_prior_reading_ids"] == ["read:1"]


def test_supplied_windows_can_fit_a_bounded_question_without_changing_source_identity(client, selection, packet):
    packet["selected_sources"].append({"source_key": "em:BOOK", "window_ids": ["chapter:3"]})
    response = finish(client, prepared(client, selection), selection, packet)
    assert response.status_code == 200, response.text
    assert response.json()["validation"]["selected_chars"] == 305_066


@pytest.mark.parametrize("change", ["commitment", "source", "window", "memory", "unreadable", "full_book_budget",
    "window_budget", "source_count", "memory_count", "phase", "changed_commitments", "duplicate_source", "duplicate_window"])
def test_selection_rejects_unfounded_references_and_over_budget_packets(client, selection, packet, change):
    if change == "commitment": packet["selected_commitment_ids"] = ["invented"]
    elif change == "source": packet["selected_sources"][0]["source_key"] = "invented"
    elif change == "window": packet["selected_sources"][0]["window_ids"] = ["invented"]
    elif change == "memory": packet["selected_prior_reading_ids"] = ["invented"]
    elif change == "unreadable": packet["selected_sources"] = [{"source_key": "em:MISSING", "window_ids": []}]
    elif change == "full_book_budget": packet["selected_sources"] = [{"source_key": "em:BOOK", "window_ids": []}]
    elif change == "window_budget": packet["selected_sources"].append({"source_key": "em:BOOK", "window_ids": ["chapter:4"]})
    elif change == "source_count":
        selection["budget"]["max_sources"] = 1
        packet["selected_sources"].append({"source_key": "em:BOOK", "window_ids": ["chapter:3"]})
    elif change == "memory_count": selection["budget"]["max_prior_readings"] = 0
    elif change == "phase": packet.update(phase="discovery", selected_sources=[], selected_prior_reading_ids=[])
    elif change == "changed_commitments":
        selection["context"]["commitments"].append({"id": "part:2", "text": "Another commitment.", "approved": True})
        packet["selected_commitment_ids"].append("part:2")
    elif change == "duplicate_source": packet["selected_sources"] *= 2
    else: packet["selected_sources"] = [{"source_key": "em:BOOK", "window_ids": ["chapter:3", "chapter:3"]}]
    assert finish(client, prepared(client, selection), selection, packet).status_code == 422


def test_missing_commitment_blocks_meaningfully_without_inventing_an_author_position(client, discovery, plan):
    discovery["context"]["commitments"] = []
    p = prepared(client, discovery)
    assert finish(client, p, discovery, plan).status_code == 422
    plan.update(status="blocked", selected_commitment_ids=[], gaps=["No current author commitment was supplied."])
    assert finish(client, p, discovery, plan).status_code == 200


def test_unapproved_candidate_cannot_be_promoted_by_planning(client, discovery, plan):
    discovery["context"]["commitments"][0]["approved"] = False
    assert finish(client, prepared(client, discovery), discovery, plan).status_code == 422


def test_inadequate_coverage_can_block_with_no_selected_evidence(client, selection, packet):
    packet.update(status="blocked", selected_sources=[], selected_prior_reading_ids=[],
                  gaps=["The supplied excerpt cannot support the required whole-book account."])
    assert finish(client, prepared(client, selection), selection, packet).status_code == 200


@pytest.mark.parametrize("change", ["question", "source", "method_fingerprint", "input_fingerprint", "budget", "discovery"])
def test_changed_frozen_packet_is_rejected(client, selection, packet, change):
    p = prepared(client, selection)
    body = completion(p, selection, packet)
    if change == "question": body["input"]["context"]["question"] += " Changed."
    elif change == "source": body["input"]["sources"][0]["preview"] += " Changed."
    elif change == "budget": body["input"]["budget"]["max_chars"] -= 1
    elif change == "discovery": body["input"]["discovery_plan"]["rationale"] += " Changed."
    else: body[change] = "wrong"
    assert client.post("/v1/inquiries/planning/complete", json=body).status_code == 409


def test_completion_survives_catalogue_edit_and_retries_are_immutable(client, discovery, plan, monkeypatch):
    p = prepared(client, discovery)
    monkeypatch.setattr(service, "method_record", lambda _: pytest.fail("Completion reads its frozen method"))
    a = finish(client, p, discovery, plan)
    b = finish(client, p, discovery, plan)
    assert a.status_code == b.status_code == 200
    assert b.json()["replayed"]
    plan["rationale"] = "A different decision cannot overwrite the first result."
    assert finish(client, p, discovery, plan).status_code == 409


def test_concurrent_conflicting_completions_have_one_winner(client, discovery, plan):
    p = prepared(client, discovery)
    a = completion(p, discovery, plan)
    b = copy.deepcopy(a)
    b["result"]["rationale"] = "An alternative rationale."
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses = list(pool.map(lambda data: client.post("/v1/inquiries/planning/complete", json=data), [a, b]))
    assert sorted(r.status_code for r in responses) == [200, 409]


def test_retest_chooses_a_real_test_before_selection_and_preserves_requested_test(client, discovery, plan):
    discovery["context"].update(previous_result=prior_result(), requested_test_id="T1")
    p = prepared(client, discovery)
    assert finish(client, p, discovery, plan).status_code == 422
    plan["selected_test_id"] = "T2"
    assert finish(client, p, discovery, plan).status_code == 422
    plan["selected_test_id"] = "invented"
    assert finish(client, p, discovery, plan).status_code == 422
    plan["selected_test_id"] = "T1"
    assert finish(client, p, discovery, plan).status_code == 200


def test_selection_cannot_change_prior_test_after_seeing_evidence(client, selection, packet):
    selection["context"]["previous_result"] = prior_result()
    selection["discovery_plan"]["selected_test_id"] = "T1"
    packet["selected_test_id"] = "T2"
    assert finish(client, prepared(client, selection), selection, packet).status_code == 422


@pytest.mark.parametrize("change", ["no_discovery", "malformed_previous", "unknown_requested_test", "duplicate_candidate"])
def test_invalid_preparation_context_fails_before_worker(client, selection, change):
    if change == "no_discovery": selection.pop("discovery_plan")
    elif change == "malformed_previous": selection["context"]["previous_result"] = {"tests": []}
    elif change == "unknown_requested_test":
        selection["context"].update(previous_result=prior_result(), requested_test_id="invented")
    else: selection["sources"].append(copy.deepcopy(selection["sources"][0]))
    assert client.post("/v1/inquiries/planning/prepare", json=selection).status_code == 422


def test_missing_central_method_has_no_local_reasoning_fallback(client, discovery, monkeypatch):
    from src.operationalizations import registry
    class EmptyRegistry:
        def get(self, key):
            return None
    monkeypatch.setattr(registry, "get_operationalization_registry", lambda: EmptyRegistry())
    assert client.post("/v1/inquiries/planning/prepare", json=discovery).status_code == 503


def test_wanted_work_and_failed_text_readiness_are_visible_and_frozen(client, selection, packet):
    selection["availability"] = {"wants": [{"title": "The full case", "acq_status": "queued"}],
                                 "omitted_uids": ["em:OMITTED"], "text_preparation_error": "OCR failed for one appendix"}
    p = prepared(client, selection)
    supplied = json.loads(p["user_prompt"])["input"]["availability"]
    assert supplied == selection["availability"]
    assert "pending acquisition" in p["system_prompt"]
    selection["availability"]["wants"][0]["acq_status"] = "arrived"
    assert finish(client, p, selection, packet).status_code == 409
    assert prepared(client, selection)["prepared_id"] != p["prepared_id"]
