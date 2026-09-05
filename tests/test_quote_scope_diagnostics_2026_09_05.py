"""Diagnostic-only corrections: no inferred ID aliases or changed scope policy."""
import copy
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.executor.context_broker import split_ledger
from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows
from src.executor.process_runner import run_oneshot_checked, run_process
from src.executor.scoped_outcomes import assess_scopes, render_scope_json
from src.operationalizations.schemas import ProcessDimension, ProcessSpec, ProcessStep


SOURCE = "The archive contains a register and a separately maintained index."
CAP = SimpleNamespace(engine_key="diagnostic", engine_name="Diagnostic", problematique="Inspect the archive.")
EMPTY_REFS = "Findings-present claim declares no finding references"
LOST_REFS = "One or more declared finding references lack retained verified evidence"
OLD_LOST_REFS = "Declared findings have no retained verified evidence"
DISCLOSURE_PREFIX = "- Prose citations do not resolve to retained findings: "


@pytest.fixture(autouse=True)
def no_provider_calls(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("offline test attempted a provider call")
    monkeypatch.setattr("src.executor.engine_runner.get_backend", forbidden)
    monkeypatch.setattr("src.executor.process_runner._default_call", forbidden)


def row(rid, *, status="", quote=SOURCE):
    return (f"- [{rid}] An archive finding — dim: evidence — doc: a — anchor: {json.dumps(quote)}"
            + (f" — status: {status}" if status else ""))


def process():
    return ProcessSpec(dimensions=[ProcessDimension(key="evidence", name="Evidence", id_prefix="D1",
                                                   questions=["What evidence occurs?"])],
                       steps=[ProcessStep(key="extract", kind="extract", model_tier="cheap"),
                              ProcessStep(key="verify", kind="verify", model_tier="mid", consumes=["extract"]),
                              ProcessStep(key="synthesize", kind="synthesize", model_tier="strong",
                                          consumes=["verify"], is_final=True)])


def sequence(*responses):
    pending = iter(responses)
    calls = []
    def fake(system, user, **kwargs):
        calls.append((system, user, kwargs))
        return {"content": next(pending), "model_used": kwargs["model_hint"]}
    return fake, calls


@pytest.mark.parametrize("ids,bad_anchor,issue", [
    ([], False, EMPTY_REFS),
    (["F3", "F4", "V.F1"], False, LOST_REFS),
    (["F3", "F4"], True, LOST_REFS),
    (["V.F1"], False, LOST_REFS),
    (["F3", "F4"], False, None),
])
def test_scope_diagnostic_distinguishes_empty_and_any_loss(ids, bad_anchor, issue):
    rows = parse_rows(row("F3") + "\n" + row("F4", quote="Missing source words." if bad_anchor else SOURCE))
    verify_rows(rows, SourceIndex({"a": SOURCE}))
    before = copy.deepcopy(rows)
    declared = {"document_keys": ["a"], "dimension_key": "evidence", "outcome": "findings_present",
                "sections_inspected": ["Register"], "coverage": "partial", "criterion": "Recorded archive evidence.",
                "basis": "The inspected register and index support these findings.", "limitations": [],
                "finding_ids": ids, "review_state": "supported_within_stated_scope", "review_basis": "Checked the register."}
    actual = assess_scopes(render_scope_json([declared]), [{"document_keys": ["a"], "dimension_key": "evidence"}],
                           rows, {"a": SOURCE}, reviewing=True)[0]
    assert actual["evidence_state"]["blocking_issues"] == ([issue] if issue else [])
    assert actual["outcome"] == ("inconclusive" if issue else "findings_present")
    assert actual["finding_ids"] == ids and rows == before
    assert actual["review_state"] == ("unchecked" if issue else "supported_within_stated_scope")


def test_quote_only_wall_does_not_claim_prose_was_checked():
    wall = verify_rows(parse_rows(row("F1")), SourceIndex({"a": SOURCE})).as_dict()
    assert wall["missing_cited"] == []
    assert wall["citation_check"] == {"status": "not_checked"}


def test_checked_prose_reports_rejected_and_absent_ids_without_remapping():
    prose = "A retained claim [F1], rejected claim [F2], absent claim [F99], and addition alias [V.F1]. Again [F2]."
    tail = "\n### Counter-evidence\nA retained auxiliary claim [F88].\n### Open questions\nAn open issue."
    reading = prose + "\n\n## Findings ledger\n" + row("F1") + "\n" + row("F2") + tail
    critic = "## Findings ledger\n" + row("F1", status="confirmed") + "\n" + row("F2", status="rejected") + "\n" + row("V.F1", status="added")
    fake, calls = sequence(reading, critic)
    result = run_oneshot_checked(CAP, process(), {"a": SOURCE}, call_fn=fake)
    assert len(calls) == 2 and [call.content for call in result.calls] == [reading, critic]
    assert result.calls[0].wall["citation_check"] == {"status": "not_checked"}
    assert result.final_wall["missing_cited"] == ["F2", "F99", "V.F1"]
    assert result.final_wall["citation_check"] == {
        "status": "checked", "scope": "retained_ledger",
        "missing_rejected_ids": ["F2"], "missing_other_ids": ["F99", "V.F1"],
    }
    final_prose, ledger = split_ledger(result.final_content)
    assert final_prose.strip() == prose and tail in result.final_content
    retained = parse_rows(ledger)
    assert [r.id for r in retained] == ["F1", "F3"]
    assert retained[1].lineage == ["V.F1"]
    assert "### Rejected by the critic\n- [F2]" in result.final_content
    assert (DISCLOSURE_PREFIX + "rejected IDs [F2]; other absent IDs [F99], [V.F1].") in result.final_content
    assert "rejected-row records and addition lineage do not resolve these citations" in result.final_content
    # Auxiliary sections, receipts and lineage are outside this explicitly prose-only check.
    assert "F88" not in result.final_wall["missing_cited"]


@pytest.mark.parametrize("prose", ["A claim [F1].", "A reading with no bracketed finding IDs."])
def test_checked_empty_is_explicit_and_adds_no_error_disclosure(prose):
    reading = prose + "\n\n## Findings ledger\n" + row("F1")
    critic = "## Findings ledger\n" + row("F1", status="confirmed")
    fake, _ = sequence(reading, critic)
    result = run_oneshot_checked(CAP, process(), {"a": SOURCE}, call_fn=fake)
    assert result.final_wall["missing_cited"] == []
    assert result.final_wall["citation_check"] == {
        "status": "checked", "scope": "retained_ledger", "missing_rejected_ids": [], "missing_other_ids": []}
    assert DISCLOSURE_PREFIX not in result.final_content


def test_unchecked_oneshot_remains_unchecked():
    reading = "A claim [F99].\n\n## Findings ledger\n" + row("F1")
    fake, calls = sequence(reading)
    result = run_oneshot_checked(CAP, process(), {"a": SOURCE}, call_fn=fake, check=False)
    assert len(calls) == 1 and result.final_content == reading
    assert result.final_wall["citation_check"] == {"status": "not_checked"}


def test_deep_synthesis_preserves_earlier_rejected_id_allowance():
    extracted = "## Findings ledger\n" + row("D1.F1") + "\n" + row("D1.F2")
    critic = "## Findings ledger\n" + row("D1.F1", status="confirmed") + "\n" + row("D1.F2", status="rejected")
    synthesized = "Earlier retained [D1.F1], earlier rejected [D1.F2], and absent [F99].\n\n## Findings ledger\n" + row("F1")
    fake, calls = sequence(extracted, critic, synthesized)
    result = run_process(CAP, process(), {"a": SOURCE}, call_fn=fake, reanchor=False, parallelism=1)
    assert len(calls) == 3 and result.final_content == synthesized
    assert result.final_wall["missing_cited"] == ["F99"]
    assert result.final_wall["citation_check"] == {
        "status": "checked", "scope": "final_and_earlier_ledgers",
        "missing_rejected_ids": [], "missing_other_ids": ["F99"],
    }


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def test_saved_harris_offline_replay_when_artifacts_are_available():
    """Opt in with IDEAS_ARGUMENT_RUN_DIR; never commit source/model text as a fixture."""
    directory = os.environ.get("IDEAS_ARGUMENT_RUN_DIR")
    if not directory:
        pytest.skip("Set IDEAS_ARGUMENT_RUN_DIR to the local completed argument-family campaign")
    folder = Path(directory)
    plan = json.loads((folder / "plan.json").read_text())
    assert plan["identity"] == "530df62823ec1915b1a4a48472d4b59782e6017f92f9d5496a8c645c5836ad16"
    assert digest({k: v for k, v in plan.items() if k != "identity"}) == plan["identity"]
    key = "counterfactual_analyzer__candidate__harris"
    record = json.loads((folder / "results.json").read_text())[key]
    job = next(j for j in plan["generations"] if j["key"] == key)
    assert record["status"] == "complete" and record["identity"] == plan["identity"]
    assert record["job_sha256"] == digest(job)
    attempt = folder / "receipts" / key / record["attempt"]
    assert json.loads((attempt / "job.json").read_text()) == record
    assert {str(p.relative_to(folder)): digest(p.read_bytes()) for p in attempt.glob("call-*")} == record["invocation_files_sha256"]
    baseline = (folder / record["output"]).read_bytes()
    assert digest(baseline) == record["output_sha256"]
    source_key = plan["source_groups"]["harris"][0]
    source = plan["sources"][source_key]
    source_paths = [Path(p) for p in plan["input_files_sha256"] if Path(p).name == source["filename"]]
    assert len(source_paths) == 1
    raw_source = source_paths[0].read_bytes()
    assert digest(raw_source) == source["sha256"] == plan["input_files_sha256"][str(source_paths[0])]
    definition = plan["definitions"][job["engine"]]
    cap = SimpleNamespace(**definition["capability"])
    spec = ProcessSpec.model_validate(definition["process"])
    position = 0
    raw_responses = []
    def replay(system, user, **kwargs):
        nonlocal position
        position += 1
        assert position <= record["invocations"] == 2
        stem = attempt / f"call-{position:04d}"
        receipt = json.loads(stem.with_suffix(".json").read_text())
        prompt = json.loads(stem.with_suffix(".prompt.json").read_text())
        response = json.loads(stem.with_suffix(".response.json").read_text())
        raw = stem.with_suffix(".md").read_bytes()
        assert receipt["status"] == "complete" and not receipt.get("partial")
        assert receipt.get("stop_reason") not in ("length", "max_tokens", "error")
        assert receipt["model_requested"] == receipt["model_used"] == response["model_used"] == kwargs["model_hint"]
        assert receipt["label"] == kwargs["label"]
        assert prompt == {"system": system, "user": user} and digest(prompt) == receipt["prompt_sha256"]
        assert digest(response) == receipt["response_sha256"] and digest(raw) == receipt["output_sha256"]
        assert response["content"].encode() == raw
        raw_responses.append(response["content"])
        return response
    result = run_oneshot_checked(cap, spec, {source_key: raw_source.decode()}, call_fn=replay,
                                 tier_overrides={"strong": plan["models"]["read"], "mid": plan["models"]["critic"]})
    assert position == 2 and [call.content for call in result.calls] == raw_responses
    assert result.final_wall["missing_cited"] == ["F4", "F5", "F7", "F11"]
    assert result.final_wall["citation_check"] == {
        "status": "checked", "scope": "retained_ledger",
        "missing_rejected_ids": ["F4", "F5", "F7", "F11"], "missing_other_ids": [],
    }
    # Remove only the new diagnostic line and restore the precise wording delta.
    # Every other byte, including source-derived prose, retained/rejected rows and lineage, must match.
    lines = result.final_content.splitlines(keepends=True)
    assert sum(line.startswith(DISCLOSURE_PREFIX) for line in lines) == 1
    restored = "".join(line for line in lines if not line.startswith(DISCLOSURE_PREFIX)).replace(LOST_REFS, OLD_LOST_REFS)
    assert restored.encode() == baseline
    assert split_ledger(result.final_content)[0] == split_ledger(baseline.decode())[0]
    actual_process, baseline_process = copy.deepcopy(result.receipts()), copy.deepcopy(record["process"])
    for receipt in (actual_process, baseline_process):
        receipt.pop("seconds")  # Offline CPU timing is not the original invocation duration.
        for call in receipt["calls"]:
            call.pop("duration_ms")
    for wall in [actual_process["final_wall"], *(call["wall"] for call in actual_process["calls"])]:
        wall.pop("citation_check", None)
        if wall["missing_cited"]:
            assert wall["missing_cited"] == ["F4", "F5", "F7", "F11"]
            wall["missing_cited"] = []  # Frozen oneshot did not check these IDs.
        for scope in wall.get("scope_outcomes", []):
            scope["evidence_state"]["blocking_issues"] = [
                issue.replace(LOST_REFS, OLD_LOST_REFS) for issue in scope["evidence_state"]["blocking_issues"]]
    assert actual_process == baseline_process
