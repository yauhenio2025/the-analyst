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
    writes, blobs, indexed, indexed_phases = [], {}, [], []
    monkeypatch.setattr(runner, "update_job", lambda jid, **fields: writes.append(fields))
    monkeypatch.setattr(runner, "record_step_duration", lambda *a: None)
    monkeypatch.setattr(events, "emit", lambda *a, **k: None)
    monkeypatch.setattr(blob_store, "put_blob", lambda key, mime, data: blobs.update({key: data}))
    monkeypatch.setattr(blob_store, "get_blob", lambda key: ("application/json", blobs[key]) if key in blobs else None)
    monkeypatch.setattr(investigation, "load_investigation", lambda jid: None)
    monkeypatch.setattr(engine_call, "call_engine", fake_engine([]))
    def index(job, only_phases=None):
        indexed.append(copy.deepcopy(job))
        indexed_phases.extend(only_phases or list(job['analysis']))
    monkeypatch.setattr(registry, "index_job", index)
    runner._run_step(job, "plan", docs)
    assert job.plan.plan_id == "investigation:dossier-investigation-test"
    assert len(job.plan.phases) == 4
    runner._run_step(job, "analysis", docs)
    artifact = json.loads(blobs["investigation:dossier-investigation-test"])
    assert artifact["complete"] and job.analysis and indexed
    assert len(indexed_phases) == len(set(indexed_phases)) == len(job.analysis)
    assert job.totals.cost_usd == pytest.approx(.7) and job.totals.llm_calls == 7
    assert job.totals.input_tokens == 77 and len(job.receipts) == 7
    assert any("analysis" in fields and "receipts" in fields for fields in writes)
    zero = job.model_copy(deep=True)
    zero.id = "dossier-zero-cap"
    zero.options.spend_cap_usd = 0
    monkeypatch.setattr(engine_call, "call_engine", lambda *a, **k: pytest.fail("zero cap must not default to eight dollars"))
    with pytest.raises(ValueError, match="spend cap"):
        runner._run_step(zero, "analysis", docs)
    assert json.loads(blobs["investigation:dossier-zero-cap"])["cost_usd"] == 0


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


def test_citation_followup_preserves_initial_candidates_and_metadata_travels():
    _, packet, _, bodies = fixture()
    packet["limits"]["max_read_texts"] = 2
    packet["primary"][0].update(bibliographic={"extra": "Original Date: 2010; reprint 2019"},
                                attribution_required=True, roles=["guest"], creators_short="Host and Riley")
    calls = []
    state = run_investigation(packet, bodies, call=fake_engine(calls), save=lambda s: None)
    assert [r["uid"] for r in state["readings"]] == ["em:AAAAAAA1", "em:CCCCCCC3"]
    assert state["citation_followups"][0]["to_uid"] == "em:BBBBBBB2"
    assert state["citation_followups"][0]["status"] == "deferred"
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


def test_explicit_zero_cap_refuses_all_paid_work():
    _, packet, _, bodies = fixture()
    snapshots = []
    with pytest.raises(ValueError, match='spend cap'):
        run_investigation(packet, bodies, call=lambda *a, **kw: pytest.fail('zero cap cannot call a model'),
                          save=lambda s: snapshots.append(copy.deepcopy(s)), spend_cap_usd=0)
    assert snapshots[-1]['cost_usd'] == 0 and not snapshots[-1]['calls']


@pytest.mark.parametrize('finding_id', ['F1', 'E1.F1'])
def test_real_engine_finding_ids_validate_and_saved_memo_resumes_without_another_call(finding_id):
    """The real first run returned F1..Fn, the generic runner's canonical IDs."""
    _, packet, _, bodies = fixture()
    original = fake_engine([])
    def call(key, sources, **kw):
        result = original(key, sources, **kw)
        if key.endswith('_read'):
            for row in result['rows']:
                if row['dim'] == 'evidence':
                    row['id'] = finding_id
        if key.endswith('_memo'):
            result['prose'] = f'Riley gives organization a political role [em:AAAAAAA1/{finding_id}].'
        return result
    state = run_investigation(packet, bodies, call=call, save=lambda s: None)
    expected = f'em:AAAAAAA1/{finding_id}'
    assert state['evidence'][0]['citation_id'] == expected
    assert state['memo_validation']['references'] == [expected]
    assert state['memo_validation']['supported'] and state['complete']
    # Emulate the already-paid draft left behind by the former over-narrow validator.
    state.update(complete=False, paused_reason='memo_citation_validation', current_stage='memo_validation')
    state['stages'].remove('done')
    cost = state['cost_usd']
    resumed = run_investigation(packet, bodies, state=state,
                               call=lambda *a, **kw: pytest.fail('saved source readings and memo must not be billed again'),
                               save=lambda s: None)
    assert resumed['complete'] and resumed['paused_reason'] is None and resumed['cost_usd'] == cost


def test_unknown_bare_finding_ids_remain_unverified():
    _, packet, _, bodies = fixture()
    original = fake_engine([])
    snapshots = []
    def call(key, sources, **kw):
        result = original(key, sources, **kw)
        if key.endswith('_memo'):
            result['prose'] = 'An unsupported claim [em:AAAAAAA1/F99].'
        return result
    with pytest.raises(ValueError, match='memo references'):
        run_investigation(packet, bodies, call=call, save=lambda s: snapshots.append(copy.deepcopy(s)))
    assert snapshots[-1]['memo_validation']['unsupported_memo_citations'] == ['em:AAAAAAA1/F99']
    assert not snapshots[-1]['complete']


def test_method_shaped_rows_before_final_generic_ledger_are_recovered():
    from src.dossier.investigation import recover_answer_rows
    from src.executor.context_broker import split_ledger
    output = '''## Inventory decisions
- [T1.F1] Read the organizing argument — dim: candidate — uid: em:AAAAAAA1 — decision: read — priority: 1 — reason: Direct organizing evidence — queries: organizing; unions — anchor: "Worker organizing" — doc: inventory-batch — confidence: high

## Verified Findings Ledger
- [F1] Organization matters — dim: candidate — anchor: "Worker organizing" — doc: inventory-batch — confidence: high
'''
    # This is the real failure shape: the later generic ledger drops uid/decision.
    assert 'decision: read' not in split_ledger(output)[1]
    result = {'final_output': output, 'rows': [{'id': 'F1', 'doc': 'inventory-batch', 'dim': 'candidate',
                                               'fields': {'confidence': 'high'}, 'anchor': 'Worker organizing'}]}
    rows = recover_answer_rows(result)
    selected = next(r for r in rows if r['id'] == 'T1.F1')
    assert selected['fields']['uid'] == 'em:AAAAAAA1' and selected['fields']['decision'] == 'read'
    assert selected['anchor_verified'] is False  # recovering shape is not verifying a primary quote
    assert len(result['original_rows']) == 1 and len(result['rows']) == 2
    unchanged = copy.deepcopy(result)
    recover_answer_rows(result)
    assert result == unchanged


def test_cached_split_triage_rows_recover_without_paid_replay_and_source_identity_is_sufficient():
    _, packet, _, bodies = fixture()
    calls, snapshots = [], []
    original = fake_engine(calls)
    def split_call(key, sources, **kwargs):
        result = original(key, sources, **kwargs)
        if key.endswith('_triage'):
            decision_rows = result['rows']
            lines = []
            for i, row in enumerate(decision_rows, 1):
                f = row['fields']
                lines.append(f'- [T1.F{i}] Candidate — dim: candidate — uid: {f["uid"]} — decision: {f["decision"]} — priority: {f["priority"]} — reason: {f["reason"]} — anchor: "Question" — doc: inventory-batch — confidence: high')
            result['final_output'] = '\n'.join(lines) + '\n\n## Verified Findings Ledger\n- [F1] A reading — dim: candidate — anchor: "Question" — doc: inventory-batch — confidence: high'
            result['rows'] = [{'id': 'F1', 'dim': 'candidate', 'doc': 'inventory-batch', 'fields': {}, 'anchor': 'Question'}]
        if key.endswith('_read'):
            for row in result['rows']:
                if row['dim'] == 'evidence':
                    row['fields'].pop('uid', None)  # canonical doc already identifies the single source
        return result
    state = run_investigation(packet, bodies, call=split_call, save=lambda s: snapshots.append(copy.deepcopy(s)))
    assert state['complete'] and all(r['decision'] != 'read' or not r.get('triage_missing') for r in state['triage'])
    assert state['evidence'][0]['quote_verified'] and state['evidence'][0]['uid_inferred_from_source']
    # Restore exactly the old cached call.rows shape, retaining its complete raw output.
    for result in state['calls'].values():
        if result.get('engine_key') == 'author_investigation_triage':
            result['rows'] = result['original_rows']
    resumed = run_investigation(packet, bodies, state=state,
                               call=lambda *a, **kw: pytest.fail('recover cached decisions instead of rerunning triage'), save=lambda s: None)
    assert resumed['complete'] and not any(r.get('triage_missing') for r in resumed['triage'])


def test_pdf_whitespace_quote_matches_keep_exact_source_offsets_and_reject_changed_words():
    from src.dossier.investigation import quote_span
    # The actual Riley Positivism reading flattened these PDF line wraps.
    model = 'Positivism could emerge in both industrial capitalist and preindustrial contexts; however, the types of positivism differ in these two cases because the structure of the intelligentsia differs.'
    source = 'Positivism could emerge in both industrial\ncapitalist and preindustrial contexts; however, the types of positivism differ in these two\ncases because the structure of the intelligentsia differs.'
    body = 'Unread preface. ' + source + ' Unread conclusion.'
    lo, hi = len('Unread preface. '), len('Unread preface. ') + len(source)
    assert quote_span(model, body, [(lo, hi)]) == (lo, hi, 'whitespace_only')
    assert quote_span(source, body, [(lo, hi)]) == (lo, hi, 'exact')
    assert quote_span(model, body, [(0, lo)]) is None
    assert quote_span(model, body, [(lo, lo + 40), (lo + 40, hi)]) is None
    assert quote_span(model.replace('could', 'cannot'), body, [(lo, hi)]) is None
    assert quote_span(model.replace('preindustrial', 'pre-industrial'), body, [(lo, hi)]) is None
    assert quote_span(model.replace(';', ','), body, [(lo, hi)]) is None


def test_novel_citation_targets_rank_by_saved_semantics_and_cap_survives_resume():
    original, _, _, _ = fixture()
    for uid in ('em:DDDDDDD4', 'em:EEEEEEE5'):
        original['primary'].append({'uid': uid, 'body': 'Institutions matter.', 'year': 2020,
                                    'citations': [{'key': 'silver:forces'}]})
    docs = expand_author_investigation(json.dumps(original))
    packet = json.loads(docs[-1].text)
    bodies = {d.key: d.text for d in docs if d.role == 'source'}
    base = fake_engine([])
    def call(key, sources, **kwargs):
        result = base(key, sources, **kwargs)
        if key.endswith('_triage'):
            for r in result['rows']:
                uid = r['fields']['uid']
                if uid in ('em:BBBBBBB2', 'em:DDDDDDD4', 'em:EEEEEEE5'):
                    r['fields'].update(decision='defer', priority={'em:BBBBBBB2': '5', 'em:DDDDDDD4': '2', 'em:EEEEEEE5': '1'}[uid])
        return result
    state = run_investigation(packet, bodies, call=call, save=lambda s: None)
    assert [r['uid'] for r in state['readings']] == ['em:AAAAAAA1', 'em:CCCCCCC3', 'em:EEEEEEE5', 'em:DDDDDDD4']
    assert set(state['coverage']['novel_citation_uids']) == {'em:DDDDDDD4', 'em:EEEEEEE5'}
    assert next(r for r in state['citation_followups'] if r['to_uid'] == 'em:BBBBBBB2')['status'] == 'deferred'
    # A reload may reorder object keys. Explicit analysis phases retain call order.
    state = json.loads(json.dumps(state, sort_keys=True))
    again = run_investigation(packet, bodies, state=state,
                              call=lambda *a, **k: pytest.fail('a third novel target must not be read on resume'), save=lambda s: None)
    assert len(again['readings']) == 4
    assert len(again['coverage']['novel_citation_uids']) == 2


def test_whitespace_verified_evidence_keeps_model_quote_and_exact_source_quote():
    _, packet, _, bodies = fixture()
    uid = 'em:AAAAAAA1'
    bodies['primary:' + uid] = 'Worker organizing requires\ncollective power. The strike changed their organization.'
    base = fake_engine([])
    def call(key, sources, **kwargs):
        result = base(key, sources, **kwargs)
        if key.endswith('_read') and sources[0].key == 'primary:' + uid:
            result['rows'][0]['anchor'] = 'Worker organizing requires collective power.'
        return result
    state = run_investigation(packet, bodies, call=call, save=lambda s: None)
    e = next(r for r in state['evidence'] if r['uid'] == uid)
    assert e['quote_verified'] and e['quote_match'] == 'whitespace_only'
    assert e['model_quote'] == e['quote'] == 'Worker organizing requires collective power.'
    assert e['source_quote'] == bodies[e['source_key']][e['quote_start']:e['quote_end']]
    assert '\n' in e['source_quote']


def test_legacy_paid_reading_without_coverage_replays_old_ranges_before_new_selection():
    from src.dossier.investigation import _legacy_read_inputs
    _, packet, _, bodies = fixture()
    primary = packet['primary']
    # Earlier code queued a shared-citation target ahead of the second core text.
    candidates = [{'uid': 'em:AAAAAAA1', 'decision': 'read', 'fields': {'priority': '1'}},
                  {'uid': 'em:CCCCCCC3', 'decision': 'read', 'fields': {'priority': '3'}}]
    state = {'calls': {
        'read:em:AAAAAAA1': {'rows': [row('citation_lead', 'em:AAAAAAA1', work_key='silver:forces')]},
        'read:em:BBBBBBB2': {'rows': []}},
        'readings': [{'uid': 'em:AAAAAAA1', 'inspected_ranges': [[0, len(bodies['primary:em:AAAAAAA1'])]]}]}
    searches = {r['uid']: r for r in search_inventory(primary, bodies, ['worker organizing'])}
    inputs = _legacy_read_inputs(state, primary, bodies, searches, candidates, 2, 20000)
    assert list(inputs) == ['em:AAAAAAA1', 'em:BBBBBBB2']
    assert inputs['em:BBBBBBB2']['ranges'] == [(0, len(bodies['primary:em:BBBBBBB2']))]
    state['readings'][0]['inspected_ranges'][0][1] -= 1
    with pytest.raises(ValueError, match='saved reading ranges differ'):
        _legacy_read_inputs(state, primary, bodies, searches, candidates, 2, 20000)


def test_completed_triage_restores_paid_decisions_when_expanded_paths_change_batch_sizes():
    _, packet, _, bodies = fixture()
    state = run_investigation(packet, bodies, call=fake_engine([]), save=lambda s: None)
    expected = {r['uid']: r['decision'] for r in state['triage']}
    # Citation expansion after reconciliation can exceed a former batch boundary.
    state['citation_paths'].append({'work_key': 'large-shared-work', 'to_uid': 'em:AAAAAAA1',
                                    'from_uids': ['em:' + 'X' * 240000]})
    state = run_investigation(packet, bodies, state=state, save=lambda s: None,
                              call=lambda *a, **k: pytest.fail('repartitioning cannot repeat paid triage'))
    assert {r['uid']: r['decision'] for r in state['triage']} == expected


def test_memo_deduplicates_provenance_but_keeps_source_windows_and_all_evidence_ids():
    _, packet, _, bodies = fixture()
    calls = []
    state = run_investigation(packet, bodies, call=fake_engine(calls), save=lambda s: None)
    memo = next(c for c in calls if c[0] == 'author_investigation_memo')[2]
    assert [r['citation_id'] for r in memo['evidence']] == [r['citation_id'] for r in state['evidence']]
    assert all('source_metadata' in r for r in state['evidence'])
    assert all('source_metadata' not in r for r in memo['evidence'])
    for reading in state['readings']:
        supplied = next(r for r in memo['source_readings'] if r['uid'] == reading['uid'])
        assert supplied['source_metadata'] == reading['source_metadata']
        assert supplied['inspected_ranges'] == reading['inspected_ranges']
        assert supplied['body_sha256'] == reading['body_sha256']
    assert all(r['dim'] != 'evidence' for reading in memo['source_readings'] for r in reading['rows'])


def test_resume_restores_cached_readings_together_without_repeated_triage_writes():
    _, packet, _, bodies = fixture()
    original = run_investigation(packet, bodies, call=fake_engine([]), save=lambda s: None)
    checkpoints = []
    resumed = run_investigation(packet, bodies, state=copy.deepcopy(original),
                               call=lambda *a, **k: pytest.fail('completed calls cannot repeat'),
                               save=lambda s: checkpoints.append((s['current_stage'], len(s['readings']))))
    assert resumed['complete']
    assert [s for s in checkpoints if s[0] == 'triage'] == [('triage', 3)]
    assert [s for s in checkpoints if s[0] == 'reading'] == [('reading', 3)]
    assert all(count == 3 for _, count in checkpoints)
