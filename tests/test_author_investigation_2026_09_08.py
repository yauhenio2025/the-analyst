"""Question-led orchestration regressions. No paid calls, databases or external services."""
import copy
import json

import pytest

from src.dossier.investigation import (citation_paths, inspected_ranges, run_investigation,
                                        search_inventory)
from src.sources.author_investigation import expand_author_investigation
from src.sources.resolve import resolve_sources
from src.sources.schemas import SourceSpec


def fixture():
    packet = {"author": {"id": "riley-dylan", "name": "Riley, Dylan"},
              "question": "Does Riley discuss worker organizing and historical labor protest?",
              "scope": {"year_from": 2011, "year_to": 2026, "historical_context": True,
                        "context": "Class and labor agency; distinguish industrial action from voting."},
              "primary": [
                  {"uid": "em:AAAAAAA1", "title": "Work and politics", "year": 2022, "date_scope": "in_scope",
                   "body": "Worker organizing requires collective power. The strike changed their organization.",
                   "read_uid": "em:READAAA1", "citations": [{"key": "silver:forces", "title": "Forces of Labor", "held_uid": "em:SILVER01"}]},
                  {"uid": "em:BBBBBBB2", "title": "Collective institutions", "year": 2009, "date_scope": "earlier_context",
                   "body": "The organization built durable collective institutions.", "citations": [{"key": "silver:forces", "title": "Forces of Labor"}]},
                  {"uid": "em:CCCCCCC3", "title": "Political agency", "year": 2018, "date_scope": "in_scope",
                   "profile": {"thesis": "Collective bargaining shaped political agency."}, "body": "Collective bargaining shaped political agency."},
                  {"uid": "em:MISSING4", "title": "Unavailable interview", "year": 2024, "date_scope": "in_scope",
                   "profile": {"thesis": "Industrial action in California"}, "body": ""},
                  {"uid": "em:OUTSIDE5", "title": "Container metadata", "year": 2030, "date_scope": "outside_range",
                   "body_state": "excluded", "body": "Worker organizing", "selection_reason": "Outside selected date range"},
                  {"uid": "em:UNDATED6", "title": "Undated talk", "date_scope": "undated", "body": ""}],
              "secondary": [{"uid": "memo:weber", "title": "Earlier Weber memo", "kind": "memo",
                             "body": "The previous memo suggests looking at unions; this is not Riley's testimony."}],
              "referee": {"thinker_id": 77, "works": [{"title": "Forces of Labor"}]},
              "prior_readings": [{"job_id": "prior", "rows": ["retained clue"]}],
              "limits": {"max_read_texts": 8, "max_primary_chars": 20000}}
    docs = expand_author_investigation(json.dumps(packet))
    frozen = json.loads(docs[-1].text)
    return packet, frozen, docs, {d.key: d.text for d in docs if d.role == "source"}


def row(dim, uid=None, **fields):
    if uid:
        fields["uid"] = uid
    return {"id": "E1.F1" if dim == "evidence" else "E2.F1", "dim": dim, "fields": fields,
            "doc": f"primary:{uid}" if uid else "investigation-question", "anchor": "", "confidence": "high"}


def fake_engine(calls, fail_once=None):
    failures = set()
    def call(key, sources, *, packet, **kwargs):
        calls.append((key, [s.key for s in sources], copy.deepcopy(packet)))
        if key == "author_investigation_plan":
            rows = [row("query", query="worker organizing"), row("query", query="strike")]
        elif key == "author_investigation_triage":
            inventory = json.loads(sources[0].text)
            rows = [row("candidate", r["inventory"]["uid"],
                        decision={"em:AAAAAAA1": "read", "em:BBBBBBB2": "defer", "em:CCCCCCC3": "read"}.get(r["inventory"]["uid"], "unavailable"),
                        priority="1" if r["inventory"]["uid"] == "em:AAAAAAA1" else "3", reason="Profile or primary context merits checking") for r in inventory]
        elif key == "author_investigation_read":
            uid = sources[0].key.removeprefix("primary:")
            if fail_once == uid and uid not in failures:
                failures.add(uid)
                raise RuntimeError("simulated provider interruption")
            quote = sources[0].text.split("\n", 1)[1].split(".")[0] + "."
            r = row("evidence", uid, relation="direct", speaker="Riley", context="A qualified collective action argument", locus="source chars")
            r["anchor"] = "A fabricated quote." if uid == "em:CCCCCCC3" else quote
            rows = [r]
            if uid == "em:AAAAAAA1":
                rows.append(row("citation_lead", uid, work_key="silver:forces", reason="Compare this same source in the earlier text"))
        else:
            rows = [row("answer", answer="The supplied material supports a qualified answer.")]
        return {"engine_key": key, "rows": rows, "cost_usd": 0.1, "model": "fake", "wall": {"failed_ids": []},
                "calls": [{"input_tokens": 11, "output_tokens": 5}], "final_output": "Saved ledger", "prose": "A bounded answer with evidence [em:AAAAAAA1/E1.F1]." if key.endswith("_memo") else "A bounded source reading."}
    return call


def test_packet_expansion_preserves_inventory_and_primary_source_identity():
    original, packet, docs, bodies = fixture()
    assert len(packet["primary"]) == len(original["primary"]) == 6
    assert all("body" not in r for r in packet["primary"])
    assert packet["primary"][0]["body_sha256"] and packet["primary"][0]["read_uid"] == "em:READAAA1"
    assert bodies["primary:em:AAAAAAA1"] == original["primary"][0]["body"]
    assert packet["primary"][3]["body_state"] == "missing"
    resolved = resolve_sources([SourceSpec(kind="paste", role="author_investigation", text=json.dumps(original))])
    assert resolved[-1].role == "plan" and resolved[-1].key == "investigation"
    assert all(d.char_count == len(d.text) for d in resolved)
    assert original["primary"][0]["body"]  # the caller's object was not mutated


def test_duplicate_uids_and_missing_question_fail_before_models():
    p, _, _, _ = fixture()
    p["primary"].append(copy.deepcopy(p["primary"][0]))
    with pytest.raises(ValueError, match="duplicate"):
        expand_author_investigation(json.dumps(p))
    with pytest.raises(ValueError, match="question"):
        expand_author_investigation('{"author":{"id":"a"},"primary":[]}')


def test_search_is_complete_and_citation_identity_drives_paths():
    _, packet, _, bodies = fixture()
    searches = search_inventory(packet["primary"], bodies, ["worker organizing", "strike"])
    by = {s["uid"]: s for s in searches}
    assert by["em:AAAAAAA1"]["match_count"] == 2
    assert by["em:CCCCCCC3"]["searched_chars"] > 0 and by["em:CCCCCCC3"]["match_count"] == 0
    assert by["em:OUTSIDE5"]["searched_chars"] == 0
    paths = citation_paths(packet["primary"], searches, ["worker organizing"])
    assert any(p["from_uids"] == ["em:AAAAAAA1"] and p["to_uid"] == "em:BBBBBBB2" for p in paths)
    assert all(p["substantive_relevance"] == "unjudged" for p in paths)


def test_windows_are_exact_non_overlapping_and_bounded():
    body = "a" * 80000 + "worker organizing" + "z" * 60000
    searches = {"matches": [{"hits": [{"start": 80000}]}]}
    ranges = inspected_ranges(body, searches, 18000)
    assert sum(hi - lo for lo, hi in ranges) <= 18000
    assert any(lo <= 80000 < hi for lo, hi in ranges)
    assert all(a[1] < b[0] for a, b in zip(ranges, ranges[1:]))
    assert inspected_ranges("short", {}, 100) == [(0, 5)]


def test_every_profile_is_triaged_semantic_misses_read_and_new_citation_leads_followed():
    _, packet, _, bodies = fixture()
    calls, snapshots = [], []
    state = run_investigation(packet, bodies, call=fake_engine(calls), save=lambda s: snapshots.append(copy.deepcopy(s)))
    assert state["complete"] and state["memo"]
    assert len(state["triage"]) == len(packet["primary"])
    assert {r["uid"] for r in state["readings"]} == {"em:AAAAAAA1", "em:BBBBBBB2", "em:CCCCCCC3"}
    assert state["citation_followups"][0]["to_uid"] == "em:BBBBBBB2"
    assert any(c[0] == "author_investigation_triage" and "retained clue" in str(c) for c in calls) is False  # context is a source, not fabricated primary input
    reads = [c for c in calls if c[0] == "author_investigation_read"]
    assert all(len(c[1]) == 1 and c[1][0].startswith("primary:") for c in reads)
    evidence = {r["uid"]: r for r in state["evidence"]}
    assert evidence["em:AAAAAAA1"]["quote_verified"] and evidence["em:AAAAAAA1"]["read_uid"] == "em:READAAA1"
    assert not evidence["em:CCCCCCC3"]["quote_verified"] and evidence["em:CCCCCCC3"]["conjecture"]
    assert state["coverage"]["absence_claims_supported"] is False
    assert state["coverage"]["missing_uids"] == ["em:MISSING4", "em:UNDATED6"]
    assert state["coverage"]["excluded_uids"] == ["em:OUTSIDE5"]
    assert state["coverage"]["undated_uids"] == ["em:UNDATED6"]
    assert any(s.get("evidence") and not s.get("complete") for s in snapshots)
    assert all(k.isdigit() for k in state["analysis"])  # existing ledger routes sort numeric phase keys
    assert state["stage_status"]["memo"] == "complete"


def test_resume_keeps_completed_paid_work_and_quote_artifacts():
    _, packet, _, bodies = fixture()
    calls, snapshots = [], []
    call = fake_engine(calls, fail_once="em:CCCCCCC3")
    with pytest.raises(RuntimeError, match="provider interruption"):
        run_investigation(packet, bodies, call=call, save=lambda s: snapshots.append(copy.deepcopy(s)))
    checkpoint = snapshots[-1]
    assert checkpoint["evidence"][0]["quote_verified"]
    state = run_investigation(packet, bodies, call=call, save=lambda s: None, state=checkpoint)
    assert state["complete"] and state["cost_usd"] == pytest.approx(0.7)
    assert sum(c[0] == "author_investigation_plan" for c in calls) == 1
    assert sum(c[1] == ["primary:em:AAAAAAA1"] for c in calls) == 1
    assert sum(c[1] == ["primary:em:CCCCCCC3"] for c in calls) == 2
    again = run_investigation(packet, bodies, call=lambda *a, **k: pytest.fail("completed calls cannot repeat"), save=lambda s: None, state=state)
    assert again["complete"]


def test_budget_and_cancel_leave_partial_work_and_caps_disclose_deferred_candidates():
    _, packet, _, bodies = fixture()
    snapshots = []
    with pytest.raises(ValueError, match="spend cap"):
        run_investigation(packet, bodies, call=fake_engine([]), save=lambda s: snapshots.append(copy.deepcopy(s)), spend_cap_usd=0.15)
    assert snapshots[-1]["calls"] and not snapshots[-1].get("complete")
    packet["limits"]["max_read_texts"] = 1
    state = run_investigation(packet, bodies, call=fake_engine([]), save=lambda s: None)
    assert state["coverage"]["read_count"] == 1 and state["coverage"]["deferred_candidates"]
    changed = copy.deepcopy(packet); changed["question"] = "Different question"
    with pytest.raises(ValueError, match="packet changed"):
        run_investigation(changed, bodies, call=fake_engine([]), save=lambda s: None, state=state)


def test_all_records_are_executable_and_reading_routes_attach_to_author():
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.dossier.catalog import resolve_path_request
    from src.dossier.schemas import PathRequest
    from src.workflows.registry import get_workflow_registry
    from src.readings.registry import reading_from_phase
    path = resolve_path_request(PathRequest(chain_key="author_investigation"), "researcher")
    assert len(path.steps) == 4
    for step in path.steps:
        assert get_engine_registry().get_capability_definition(step.engine_key)
        assert get_operationalization_registry().get(step.engine_key).mode_for_depth("surface") == "oneshot"
    assert get_workflow_registry().get("author_investigation")
    phase = {"engine_key": "author_investigation_read", "final_output": '[E1.F1] Collective action matters — dim: evidence — uid: em:AAAAAAA1 — anchor: "Collective action matters" — doc: primary:em:AAAAAAA1 — confidence: high'}
    reading = reading_from_phase({"id": "dossier-test", "packet": {"author": {"id": "riley-dylan", "name": "Riley, Dylan"}}}, "3", phase)
    assert "Riley, Dylan" in reading["persons"] and "em:AAAAAAA1" in reading["texts"]
    assert reading["renders"][0].endswith("/investigation")


def test_partial_artifact_http_view_and_wrong_recipe(monkeypatch):
    from fastapi import HTTPException
    from src.api.routes import dossier
    from src.dossier import investigation
    from src.dossier.schemas import DossierJob, DossierOptions, PathRequest
    job = DossierJob(id="dossier-test", status="analysis", options=DossierOptions(intent="Question", entry="chosen", path=PathRequest(chain_key="author_investigation")))
    monkeypatch.setattr(dossier, "_load", lambda jid: job)
    monkeypatch.setattr(investigation, "load_investigation", lambda jid: {"memo": "", "evidence": [{"quote": "retained"}], "calls": {"private": {}}, "complete": False})
    out = dossier.get_investigation(job.id)
    assert out["status"] == "analysis" and out["evidence"] and "calls" not in out
    monkeypatch.setattr(investigation, "load_investigation", lambda jid: None)
    assert dossier.get_investigation(job.id)["complete"] is False
    job.options.path = PathRequest(chain_key="oeuvre_position")
    with pytest.raises(HTTPException) as exc:
        dossier.get_investigation(job.id)
    assert exc.value.status_code == 409


def test_dossier_runner_uses_registered_specialized_executor_and_durable_accounting(monkeypatch):
    from src.dossier import runner, investigation, blob_store, engine_call, events
    from src.readings import registry
    from src.dossier.schemas import DossierJob, DossierOptions, PathRequest, OutputOptions
    _, _, docs, _ = fixture()
    job = DossierJob(id="dossier-investigation-test", options=DossierOptions(
        intent="Question", entry="chosen", path=PathRequest(chain_key="author_investigation"),
        output=OutputOptions(text=False, tables=False, figures=0, plates=0), spend_cap_usd=2.0))
    writes, blobs, indexed = [], {}, []
    monkeypatch.setattr(runner, "update_job", lambda jid, **fields: writes.append(fields))
    monkeypatch.setattr(runner, "record_step_duration", lambda *a: None)
    monkeypatch.setattr(events, "emit", lambda *a, **k: None)
    monkeypatch.setattr(blob_store, "put_blob", lambda key, mime, data: blobs.update({key: data}))
    monkeypatch.setattr(blob_store, "get_blob", lambda key: ("application/json", blobs[key]) if key in blobs else None)
    monkeypatch.setattr(investigation, "load_investigation", lambda jid: None)
    monkeypatch.setattr(engine_call, "call_engine", fake_engine([]))
    monkeypatch.setattr(registry, "index_job", lambda job: indexed.append(copy.deepcopy(job)))
    runner._run_step(job, "plan", docs)
    assert job.plan.plan_id == "investigation:dossier-investigation-test"
    assert len(job.plan.phases) == 4
    runner._run_step(job, "analysis", docs)
    artifact = json.loads(blobs["investigation:dossier-investigation-test"])
    assert artifact["complete"] and job.analysis and indexed
    assert job.totals.cost_usd == pytest.approx(.7) and job.totals.llm_calls == 7
    assert job.totals.input_tokens == 77 and len(job.receipts) == 7
    assert any("analysis" in fields and "receipts" in fields for fields in writes)


def test_cancel_between_calls_keeps_plan_without_starting_another_call():
    _, packet, _, bodies = fixture()
    calls, snapshots = [], []
    def check():
        if calls:
            raise RuntimeError("cancelled")
    with pytest.raises(RuntimeError, match="cancelled"):
        run_investigation(packet, bodies, call=fake_engine(calls), save=lambda s: snapshots.append(copy.deepcopy(s)), check=check)
    assert len(calls) == 1 and snapshots[-1]["plan"] and snapshots[-1]["searches"]


def test_prior_reading_ids_are_resolved_and_secondary_search_finds_buried_evidence():
    from src.dossier.investigation import hydrate_prior_readings, _context
    packet = {"prior_readings": ["old-job", {"job_id": "other", "phase": "2"}], "secondary": [
        {"uid": "old-memo", "source_key": "secondary:old-memo", "title": "Old analysis", "kind": "memo"}]}
    looked = []
    def reading(job, phase):
        looked.append((job, phase))
        return {"job_id": job, "phase": phase, "rows": [{"text": "A previously recorded union argument"}]}
    hydrated = hydrate_prior_readings(packet, lookup_index=lambda **kw: {"readings": [{"phase": "4.1"}]}, lookup_reading=reading)
    assert looked == [("old-job", "4.1"), ("other", "2")]
    assert all(r["status"] == "resolved" for r in hydrated["prior_readings_resolution"])
    bodies = {"secondary:old-memo": "irrelevant preface " * 10000 + "The union organized a strike." + " conclusion" * 10000}
    context = _context(hydrated, bodies, queries=["union", "strike"], cap=5000)
    old = next(c for c in context if c["key"] == "secondary:old-memo")
    assert old["searched_chars"] == len(bodies[old["key"]])
    assert "union organized a strike" in old["text"] and old["truncated"]
    assert any(c["key"] == "reading:old-job:4.1" and "previously recorded" in c["text"] for c in context)
    assert sum(c["supplied_chars"] for c in context) <= 5000


def test_new_citation_followup_takes_next_slot_before_initial_candidates_and_metadata_travels():
    _, packet, _, bodies = fixture()
    packet["limits"]["max_read_texts"] = 2
    packet["primary"][0].update(bibliographic={"extra": "Original Date: 2010; reprint 2019"},
                                attribution_required=True, roles=["guest"], creators_short="Host and Riley")
    calls = []
    state = run_investigation(packet, bodies, call=fake_engine(calls), save=lambda s: None)
    assert [r["uid"] for r in state["readings"]] == ["em:AAAAAAA1", "em:BBBBBBB2"]
    assert "em:CCCCCCC3" in state["coverage"]["deferred_candidates"]
    read = next(c for c in calls if c[0] == "author_investigation_read")
    assert read[2]["coverage"]["source_metadata"]["attribution_required"]
    assert "Original Date" in state["evidence"][0]["source_metadata"]["bibliographic"]["extra"]
    memo = next(c for c in calls if c[0] == "author_investigation_memo")
    assert memo[2]["source_readings"][0]["source_metadata"]["roles"] == ["guest"]


def test_api_requires_the_specialized_chain_and_engines_only_output():
    from src.api.routes.dossier import validate_lane
    from src.dossier.schemas import CreateDossierRequest
    original, _, _, _ = fixture()
    fields = {"sources": [{"kind": "paste", "role": "author_investigation", "text": json.dumps(original)}],
              "entry": "chosen", "path": {"chain_key": "author_investigation"}, "intent": "Question",
              "output": {"text": False, "tables": False, "figures": 0, "plates": 0}}
    assert validate_lane(CreateDossierRequest(**fields))["entry"] == "chosen"
    with pytest.raises(ValueError, match="own memo"):
        validate_lane(CreateDossierRequest(**{**fields, "output": None}))
    with pytest.raises(ValueError, match="one author_investigation"):
        validate_lane(CreateDossierRequest(**{**fields, "path": {"chain_key": "oeuvre_position"}}))


@pytest.mark.parametrize('citation', ['[em:INVENTED/E1.F9]', '[em:CCCCCCC3/E1.F1]', ''])
def test_memo_with_unknown_unverified_or_missing_evidence_references_stays_a_draft(citation):
    _, packet, _, bodies = fixture()
    original = fake_engine([])
    snapshots = []
    def call(key, sources, **kw):
        out = original(key, sources, **kw)
        if key.endswith('_memo'):
            out['prose'] = 'This answer needs evidence. ' + citation
        return out
    with pytest.raises(ValueError, match='memo references'):
        run_investigation(packet, bodies, call=call, save=lambda s: snapshots.append(copy.deepcopy(s)))
    state = snapshots[-1]
    assert state['complete'] is False and state['memo'] and state['evidence']
    assert not state['memo_validation']['supported']
    assert state['paused_reason'] == 'memo_citation_validation'


def test_reading_budget_is_shared_across_intended_slots():
    _, packet, _, bodies = fixture()
    packet['limits'] = {'max_read_texts': 3, 'max_primary_chars': 30000}
    for uid in ('em:AAAAAAA1', 'em:BBBBBBB2', 'em:CCCCCCC3'):
        key = 'primary:' + uid
        bodies[key] = ('Worker organizing creates collective power. ' * 5000)
        row = next(r for r in packet['primary'] if r['uid'] == uid)
        row['body_chars'] = len(bodies[key])
    state = run_investigation(packet, bodies, call=fake_engine([]), save=lambda s: None)
    assert state['coverage']['read_count'] == 3
    assert state['coverage']['inspected_chars'] <= 30000
    assert all(r['reading_mode'] == 'windows' for r in state['readings'])
    assert all(r['inspected_chars'] < 15000 for r in state['readings'])
