"""Exercise the worker seam without a model, HTTP service, or real application data."""
import copy
import hashlib
import threading
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
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "inquiries.sqlite")
    monkeypatch.setattr(blob_store, "_ready", False)
    monkeypatch.setattr(history_tracker, "HISTORY_DIR", tmp_path / "capability_history")
    app = FastAPI()
    app.include_router(router, prefix="/v1")
    return TestClient(app)


@pytest.fixture
def input_data():
    return {"method": "constructive_inquiry", "context": {
        "inquiry_id": "stacks:sample", "revision": 1, "question": "When does a ruler's strategy vary independently?",
        "commitments": [{"id": "part:1", "text": "Rulers face constraints from property relations.",
                         "part_id": 1, "version_id": 3, "position": 0, "approved": True}],
        "purpose": "Clarify the scope of a developing account", "stage": "exploration",
        "prior_readings": [{"job_id": "old-job", "phase": "4.1", "rows": [{"text": "Prior conjecture"}]}],
        "author_responses": [{"text": "The earlier derivation exaggerated my starting belief.", "decision": "correct"}]},
        "sources": [{"key": "em:SOURCE1", "title": "First case", "uid": "em:SOURCE1", "version": "v1",
                     "authors": ["Brenner, Robert"], "text": "  Rulers adopted different fiscal strategies under similar property constraints.\n"},
                    {"key": "em:SOURCE2", "title": "Second case", "uid": "em:SOURCE2", "authors": ["Hintze, Otto"],
                     "text": "Coercive capacities varied between neighbouring jurisdictions."}]}


@pytest.fixture
def result_data():
    return {"summary": "Fiscal strategies may vary within the same property constraints.",
        "proposed_account": {"status": "proposed", "text": "Constraints condition a range of fiscal strategies.",
            "derivation": "Distinguish constraints from determination.", "mechanism": "Coercive capacities may shape strategic selection.",
            "scope": "A provisional comparison of the two supplied cases.", "commitment_ids": ["part:1"], "evidence_ids": ["E1"]},
        "evidence": [{"id": "E1", "source_key": "em:SOURCE1",
                      "quote": "Rulers adopted different fiscal strategies under similar property constraints.",
                      "claim": "The source reports variation in fiscal strategies.", "role": "supports", "locus": "opening"}],
        "new_questions": [{"id": "Q1", "question": "Which capacities permit strategic variation?", "why": "Separates a constraint from a sufficient cause."}],
        "tests": [{"id": "T1", "question": "Does capacity account for the difference?", "procedure": "Compare the supplied case accounts for capacity differences.",
                   "discriminates": "Capacity explains variation versus property relations determine the strategy.",
                   "evidence_needed": "A case account linking fiscal choice and capacities.", "source_keys": ["em:SOURCE1", "em:SOURCE2"]}],
        "revisions": [{"id": "R1", "level": "local", "commitment_id": "part:1", "before": "Rulers face constraints from property relations.",
                       "after": "Property relations constrain, but may not determine, fiscal strategy.",
                       "reason": "Makes room for variation reported in this case.", "evidence_ids": ["E1"]}],
        "self_scrutiny": "Capacity must explain variation independently; merely adding an exception would protect the account.",
        "test_outcome": None}


def prepared(client, input_data):
    response = client.post("/v1/inquiries/prepare", json=input_data)
    assert response.status_code == 200, response.text
    return response.json()


def completion(preparation, input_data, result_data):
    return {"prepared_id": preparation["prepared_id"], "input_fingerprint": preparation["input_fingerprint"],
            "method_fingerprint": preparation["method_fingerprint"], "input": input_data, "result": result_data,
            "execution": {"provider": "claude_subscription", "model": "fixture", "job_id": "local-job", "cost_usd": 0}}


def test_initial_roundtrip_freezes_sources_context_and_central_method(client, input_data, result_data):
    p = prepared(client, input_data)
    assert p == prepared(client, input_data)
    assert input_data["sources"][0]["text"].strip() in p["user_prompt"]
    assert "earlier derivation exaggerated" in p["user_prompt"]
    assert p["source_manifest"][0]["text_sha256"] == hashlib.sha256(input_data["sources"][0]["text"].encode()).hexdigest()
    assert "method_card" not in p["system_prompt"]  # method content is composed, not a pathname or a duplicated doctrine
    response = client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data))
    assert response.status_code == 200, response.text
    receipt = response.json()
    assert not receipt["replayed"]
    assert receipt["result"]["proposed_account"]["status"] == "proposed"
    assert receipt["validation"]["verified_anchors"] == 1
    reading = readings.reading(**{"job_id": receipt["reading"]["job_id"], "phase": receipt["reading"]["phase"]})
    assert reading["context"]["author_responses"][0]["decision"] == "correct"
    assert reading["rows"][0]["conjecture"] is False
    assert reading["rows"][-1]["conjecture"] is True
    assert reading["result"]["proposed_account"]["derivation"] == result_data["proposed_account"]["derivation"]
    assert readings.readings_for(person="Brenner")["count"] == 1
    # All selected texts are indexed, including those whose only returned role is a future test.
    assert readings.readings_for(text="em:SOURCE2")["count"] == 1
    assert client.get("/v1/inquiries/receipts/" + receipt["receipt_id"]).json()["input_fingerprint"] == p["input_fingerprint"]


@pytest.mark.parametrize("change", ["question", "revision", "source", "method_fingerprint", "input_fingerprint"])
def test_completion_rejects_changed_frozen_input(client, input_data, result_data, change):
    p = prepared(client, input_data)
    body = completion(p, input_data, result_data)
    if change == "question":
        body["input"]["context"]["question"] += " A changed question?"
    elif change == "revision":
        body["input"]["context"]["revision"] += 1
    elif change == "source":
        body["input"]["sources"][0]["text"] += " A silently changed source."
    else:
        body[change] = "wrong"
    assert client.post("/v1/inquiries/complete", json=body).status_code == 409
    assert readings.readings_for(person="Brenner")["count"] == 0


def test_frozen_method_survives_registry_edit(client, input_data, result_data, monkeypatch):
    p = prepared(client, input_data)
    monkeypatch.setattr(service, "method_record", lambda _: pytest.fail("Completion must use the frozen method"))
    assert client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data)).status_code == 200


def test_missing_central_method_fails_closed(client, input_data, monkeypatch):
    import src.operationalizations.registry as registry
    class EmptyRegistry:
        def get(self, key):
            return None
    monkeypatch.setattr(registry, "get_operationalization_registry", lambda: EmptyRegistry())
    response = client.post("/v1/inquiries/prepare", json=input_data)
    assert response.status_code == 503
    assert "no local method fallback" in response.json()["detail"]


@pytest.mark.parametrize("quote,status", [("Invented quotations cannot support a reading.", "quote_not_found"),
    ("Coercive capacities varied between neighbouring jurisdictions.", "quote_not_found"), ("Rulers", "quote_too_short")])
def test_failed_quotes_remain_visible_and_never_move_to_other_source(client, input_data, result_data, quote, status):
    p = prepared(client, input_data)
    result_data["evidence"][0]["quote"] = quote
    receipt = client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data)).json()
    evidence = receipt["result"]["evidence"][0]
    assert evidence["quote"] == quote and evidence["source_key"] == "em:SOURCE1"
    assert evidence["verified"] is False and evidence["anchor_status"] == status
    assert receipt["validation"]["failed_anchors"][0]["evidence_id"] == "E1"
    assert readings.reading(receipt["reading"]["job_id"], receipt["reading"]["phase"])["rows"][0]["conjecture"] is True


@pytest.mark.parametrize("change", ["commitment", "source", "evidence", "duplicate", "attribution", "before", "outcome"])
def test_result_reference_and_shape_checks(client, input_data, result_data, change):
    p = prepared(client, input_data)
    if change == "commitment": result_data["proposed_account"]["commitment_ids"] = ["invented"]
    elif change == "source": result_data["evidence"][0]["source_key"] = "invented"
    elif change == "evidence": result_data["proposed_account"]["evidence_ids"] = ["invented"]
    elif change == "duplicate": result_data["evidence"].append(copy.deepcopy(result_data["evidence"][0]))
    elif change == "attribution": result_data["proposed_account"]["status"] = "author_position"
    elif change == "before": result_data["revisions"][0]["before"] = "The worker's invented version of the commitment."
    else: result_data["test_outcome"] = {"test_id": "T1", "status": "strengthened", "explanation": "Not actually a retest", "evidence_ids": ["E1"]}
    assert client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data)).status_code == 422


def test_receipt_import_is_idempotent_and_conflicting_results_are_immutable(client, input_data, result_data):
    p = prepared(client, input_data)
    body = completion(p, input_data, result_data)
    first = client.post("/v1/inquiries/complete", json=body).json()
    second = client.post("/v1/inquiries/complete", json=body).json()
    assert first["receipt_id"] == second["receipt_id"] and second["replayed"]
    assert readings.readings_for(text="em:SOURCE1")["count"] == 1
    body["result"]["summary"] = "A replacement must not silently overwrite the first reading."
    assert client.post("/v1/inquiries/complete", json=body).status_code == 409
    assert client.get("/v1/inquiries/receipts/" + first["receipt_id"]).json()["result"]["summary"] == first["result"]["summary"]


def test_parallel_different_results_have_one_winner(client, input_data, result_data):
    p = prepared(client, input_data)
    a = completion(p, input_data, result_data)
    b = copy.deepcopy(a)
    b["result"]["summary"] = "A concurrent different result."
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda body: client.post("/v1/inquiries/complete", json=body), [a, b]))
    assert sorted(r.status_code for r in results) == [200, 409]
    assert readings.readings_for(text="em:SOURCE1")["count"] == 1


def test_retry_repairs_interrupted_reading_index(client, input_data, result_data, monkeypatch):
    p = prepared(client, input_data)
    body = completion(p, input_data, result_data)
    save = readings.save_reading
    monkeypatch.setattr(readings, "save_reading", lambda *a, **kw: (_ for _ in ()).throw(RuntimeError("database interrupted")))
    with pytest.raises(RuntimeError, match="database interrupted"):
        client.post("/v1/inquiries/complete", json=body)
    monkeypatch.setattr(readings, "save_reading", save)
    response = client.post("/v1/inquiries/complete", json=body)
    assert response.status_code == 200 and response.json()["replayed"]
    assert readings.readings_for(text="em:SOURCE1")["count"] == 1


def test_retest_requires_exact_prior_test_and_returns_outcome(client, input_data, result_data):
    input_data["method"] = "constructive_retest"
    assert client.post("/v1/inquiries/prepare", json=input_data).status_code == 422
    input_data["context"]["previous_result"] = copy.deepcopy(result_data)
    input_data["context"]["test"] = copy.deepcopy(result_data["tests"][0])
    p = prepared(client, input_data)
    assert client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data)).status_code == 422
    result_data["test_outcome"] = {"test_id": "T1", "status": "inconclusive", "explanation": "The cases show variation but do not establish its cause.", "evidence_ids": ["E1"]}
    receipt = client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data)).json()
    assert receipt["result"]["test_outcome"]["status"] == "inconclusive"
    assert receipt["reading"]["phase"] == "constructive_retest"
    input_data["context"]["test"]["procedure"] = "Replace the already selected test without telling the caller."
    assert client.post("/v1/inquiries/prepare", json=input_data).status_code == 422


def test_feedback_is_immutable_deduped_and_attached_to_central_reading(client, input_data, result_data):
    p = prepared(client, input_data)
    receipt = client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data)).json()
    url = "/v1/inquiries/receipts/" + receipt["receipt_id"] + "/feedback"
    feedback = {"feedback_id": "stacks:feedback:1", "text": "My commitment was narrower; I reject this derivation.", "decision": "reject", "revision_id": "R1"}
    a = client.post(url, json=feedback)
    b = client.post(url, json=feedback)
    assert a.status_code == 200 and a.json() == b.json()
    reading = readings.reading(receipt["reading"]["job_id"], receipt["reading"]["phase"])
    assert len(reading["author_feedback"]) == 1 and reading["author_feedback"][0]["text"] == feedback["text"]
    feedback["text"] = "A changed event is not a retry."
    assert client.post(url, json=feedback).status_code == 409
    feedback.update(feedback_id="different", revision_id="missing")
    assert client.post(url, json=feedback).status_code == 422


def test_input_identity_changes_with_context_source_version_and_method(client, input_data, result_data):
    first = prepared(client, input_data)
    for change in ("question", "version", "source", "method"):
        variant = copy.deepcopy(input_data)
        if change == "question": variant["context"]["question"] += " Why?"
        elif change == "version": variant["sources"][0]["version"] = "v2"
        elif change == "source": variant["sources"][0]["text"] += " A newly held paragraph."
        else:
            variant["method"] = "constructive_retest"
            variant["context"].update(previous_result=result_data, test=result_data["tests"][0])
        assert prepared(client, variant)["prepared_id"] != first["prepared_id"]


@pytest.mark.parametrize("previous", [{"tests": 42}, {"tests": []}, {"tests": None}])
def test_malformed_or_incomplete_previous_result_is_validation_error(client, input_data, result_data, previous):
    input_data["method"] = "constructive_retest"
    input_data["context"].update(previous_result=previous, test=result_data["tests"][0])
    assert client.post("/v1/inquiries/prepare", json=input_data).status_code == 422


def test_a_retest_accepts_the_shaped_prior_receipt(client, input_data, result_data):
    p = prepared(client, input_data)
    initial = client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data)).json()
    input_data["method"] = "constructive_retest"
    input_data["context"].update(previous_result=initial["result"], test=initial["result"]["tests"][0])
    assert client.post("/v1/inquiries/prepare", json=input_data).status_code == 200


def test_evidence_cannot_collide_with_construction_row_id(client, input_data, result_data):
    p = prepared(client, input_data)
    result_data["evidence"][0]["id"] = "proposed_account"
    result_data["proposed_account"]["evidence_ids"] = ["proposed_account"]
    result_data["revisions"][0]["evidence_ids"] = ["proposed_account"]
    assert client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data)).status_code == 422


def test_concurrent_feedback_cannot_hide_author_events(client, input_data, result_data, monkeypatch):
    p = prepared(client, input_data)
    receipt = client.post("/v1/inquiries/complete", json=completion(p, input_data, result_data)).json()
    paused = threading.Event()
    proceed = threading.Event()
    save = readings.save_reading

    def out_of_order(reading, **kwargs):
        if [e["feedback_id"] for e in reading["author_feedback"]] == ["A"]:
            paused.set()
            assert proceed.wait(5)
        save(reading, **kwargs)

    monkeypatch.setattr(readings, "save_reading", out_of_order)
    url = "/v1/inquiries/receipts/" + receipt["receipt_id"] + "/feedback"
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(client.post, url, json={"feedback_id": "A", "text": "First correction"})
        try:
            assert paused.wait(5)
            second = client.post(url, json={"feedback_id": "B", "text": "Second correction"})
            assert second.status_code == 200
        finally:
            proceed.set()
        assert first.result().status_code == 200
    reading = readings.reading(receipt["reading"]["job_id"], receipt["reading"]["phase"])
    assert {e["feedback_id"] for e in reading["author_feedback"]} == {"A", "B"}


def test_concurrent_imports_keep_each_source_index_entry(client, input_data, result_data, monkeypatch):
    bodies = []
    for revision in (1, 2, 3):
        variant = copy.deepcopy(input_data)
        variant["context"]["revision"] = revision
        bodies.append(completion(prepared(client, variant), variant, result_data))
    barrier = threading.Barrier(3)
    save = readings.save_reading

    def together(*args, **kwargs):
        barrier.wait(timeout=5)
        save(*args, **kwargs)

    monkeypatch.setattr(readings, "save_reading", together)
    with ThreadPoolExecutor(max_workers=3) as pool:
        responses = list(pool.map(lambda body: client.post("/v1/inquiries/complete", json=body), bodies))
    assert [r.status_code for r in responses] == [200, 200, 200]
    assert readings.readings_for(text="em:SOURCE1")["count"] == 3
    assert readings.readings_for(person="Brenner")["count"] == 3


def test_interrupted_strict_index_transaction_rolls_back_then_replays(client, input_data, result_data, monkeypatch):
    p = prepared(client, input_data)
    body = completion(p, input_data, result_data)
    save = readings._save_reading

    def interrupted(*args, **kwargs):
        save(*args, **kwargs)
        raise RuntimeError("index transaction interrupted")

    monkeypatch.setattr(readings, "_save_reading", interrupted)
    with pytest.raises(RuntimeError, match="index transaction interrupted"):
        client.post("/v1/inquiries/complete", json=body)
    assert readings.readings_for(text="em:SOURCE1")["count"] == 0
    monkeypatch.setattr(readings, "_save_reading", save)
    replay = client.post("/v1/inquiries/complete", json=body).json()
    assert replay["replayed"] and readings.readings_for(text="em:SOURCE1")["count"] == 1
