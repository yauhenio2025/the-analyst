"""Only the observed literal empty ledger spelling is tolerated; absence is still assessed."""
from types import SimpleNamespace

import pytest

from src.executor.process_runner import StepCall, _assess_call, _scope_rows, run_oneshot_checked, run_process
from src.executor.scoped_outcomes import render_scope_json
from src.operationalizations.schemas import ProcessDimension, ProcessSpec, ProcessStep


SOURCE = "The archive inventory lists two registers and their shelf positions."
CAP = SimpleNamespace(engine_key="inventory", engine_name="Inventory", problematique="Inspect the inventory.")
IDENTITY = {"document_keys": ["a"], "dimension_key": "evidence"}


@pytest.fixture(autouse=True)
def no_provider_calls(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("offline test attempted a provider call")
    monkeypatch.setattr("src.executor.engine_runner.get_backend", forbidden)
    monkeypatch.setattr("src.executor.process_runner._default_call", forbidden)


def record(**changes):
    return {**IDENTITY, "outcome": "no_relevant_instance", "sections_inspected": ["Inventory"],
            "coverage": "complete", "criterion": "An argued incompatibility between commitments.",
            "basis": "This inventory reports locations, without asserting incompatible commitments.",
            "limitations": ["The listed registers themselves were not inspected."], "finding_ids": [],
            "review_state": "supported_within_stated_scope", "review_basis": "Checked the supplied inventory.", **changes}


def content(body="(empty)", *, declared=None, heading=True):
    return (("## Findings ledger\n" if heading else "") + body + "\n\n"
            + render_scope_json([record() if declared is None else declared]))


def assess(text, **flags):
    call = StepCall(step_key="verify", kind="verify", content=text, **flags)
    rows = _scope_rows(call)
    scopes = _assess_call(call, [IDENTITY], rows, {"a": SOURCE}, reviewing=True)
    return call, rows, scopes[0]


@pytest.mark.parametrize("body", ["", "(empty)", " \n (empty) \n "])
def test_exact_empty_marker_with_valid_review_preserves_explicit_negative(body):
    text = content(body)
    call, rows, scope = assess(text)
    assert rows == [] and call.content == text and not call.scope_parse_error
    assert scope["outcome"] == "no_relevant_instance"
    assert scope["review_state"] == "supported_within_stated_scope"
    assert scope["finding_ids"] == [] and scope["evidence_state"]["blocking_issues"] == []


@pytest.mark.parametrize("body", [
    "(EMPTY)", "empty", "None", "No findings.", "`(empty)`", "- (empty)",
    "(empty)\n(empty)", "(empty) extra prose", "(empty)\n- malformed finding without ID",
    '- [F1] A malformed anchor — anchor: "first" — anchor: "second"',
])
def test_other_prose_and_malformed_rows_are_not_an_empty_ledger(body):
    call, rows, scope = assess(content(body))
    assert rows == [] and call.scope_parse_error
    assert scope["outcome"] == "inconclusive" and scope["review_state"] == "unchecked"


def test_marker_without_ledger_heading_is_still_missing_input():
    call, rows, scope = assess(content(heading=False))
    assert rows == [] and call.scope_parse_error == "Missing findings ledger section"
    assert scope["outcome"] == "inconclusive"


@pytest.mark.parametrize("text", ["## Findings ledger\n(empty)", "## Findings ledger\n(empty)\n\n## Scope outcomes\nnot json"])
def test_marker_cannot_supply_missing_or_malformed_scope_assessment(text):
    _, rows, scope = assess(text)
    assert rows == [] and scope["outcome"] == "inconclusive" and scope["review_state"] == "unchecked"


@pytest.mark.parametrize("flags", [{"partial": True}, {"stop_reason": "max_tokens"},
                                   {"stop_reason": "error"}, {"invocation_error": "provider failed"}])
def test_marker_does_not_clear_partial_or_failed_invocation(flags):
    _, rows, scope = assess(content(), **flags)
    assert rows == [] and scope["outcome"] == "inconclusive"
    assert "Invocation is known partial or failed" in scope["evidence_state"]["blocking_issues"]


def test_marker_does_not_turn_findings_present_into_supported_absence():
    _, rows, scope = assess(content(declared=record(outcome="findings_present")))
    assert rows == [] and scope["outcome"] == "inconclusive"
    assert scope["review_state"] == "unchecked"


def process():
    return ProcessSpec(scoped_outcomes=True, framing="Only report qualifying incompatibilities.",
                       dimensions=[ProcessDimension(key="evidence", name="Evidence", id_prefix="D1",
                                                    questions=["Does the source assert incompatible commitments?"])],
                       steps=[ProcessStep(key="extract", kind="extract", model_tier="cheap"),
                              ProcessStep(key="verify", kind="verify", model_tier="mid", consumes=["extract"]),
                              ProcessStep(key="synthesize", kind="synthesize", model_tier="strong",
                                          consumes=["verify"], is_final=True)])


@pytest.mark.parametrize("runner", [run_oneshot_checked, run_process])
def test_marker_still_requires_nonempty_selected_source_before_any_call(runner):
    with pytest.raises(ValueError, match="missing source is not absence"):
        runner(CAP, process(), {"a": " "})


@pytest.mark.parametrize("deep", [False, True])
def test_empty_marker_is_reviewed_and_preserved_without_manufacturing_rows(deep):
    reader, critic = content(""), content()
    synthesis = "The supplied inventory has no qualifying instance.\n\n## Findings ledger"
    pending = iter([reader, critic, synthesis] if deep else [reader, critic])
    calls = []
    def fake(system, user, **kwargs):
        calls.append((system, user, kwargs))
        return {"content": next(pending), "model_used": kwargs["model_hint"]}
    result = (run_process(CAP, process(), {"a": SOURCE}, call_fn=fake, parallelism=1, reanchor=False)
              if deep else run_oneshot_checked(CAP, process(), {"a": SOURCE}, call_fn=fake))
    assert len(calls) == (3 if deep else 2)
    assert [call.content for call in result.calls] == ([reader, critic, synthesis] if deep else [reader, critic])
    assert result.final_wall["rows"] == 0
    scope = result.final_wall["scope_outcomes"][0]
    assert scope["outcome"] == "no_relevant_instance" and scope["review_state"] == "supported_within_stated_scope"
    assert scope["finding_ids"] == [] and "no relevant instance reported" in result.final_content
    if deep:
        assert '"outcome": "no_relevant_instance"' in calls[-1][1]
        assert '"review_state": "supported_within_stated_scope"' in calls[-1][1]
