"""Plumbing fixes from the engine harness study (2026-09-04)."""
from src.engines.registry import get_engine_registry
from src.executor.context_broker import assemble_inner_pass_context, split_ledger
from src.llm.backends import ModelRefusal
from src.stages.capability_composer import compose_all_pass_prompts


def _passes(key):
    return compose_all_pass_prompts(get_engine_registry().get_capability_definition(key), depth="deep")


def test_final_pass_writes_for_the_reader_not_the_next_pass():
    for key in ("conditions_of_possibility_analyzer", "argument_architecture"):
        pps = _passes(key)
        assert pps[-1].is_final and not any(p.is_final for p in pps[:-1])
        assert "FINAL pass" in pps[-1].prompt
        assert "next analytical pass" not in pps[-1].prompt
        assert "For the next pass" not in pps[-1].prompt
        assert "next analytical pass" in pps[0].prompt


def test_every_pass_carries_anchoring_and_ledger_laws_and_its_description():
    for p in _passes("conditions_of_possibility_analyzer"):
        assert "Anchoring law" in p.prompt and "## Findings ledger" in p.prompt
        assert p.description and p.description in p.prompt


def test_prior_pass_context_keeps_ledgers_and_caps_prose():
    long_prose = "reasoning " * 5000
    out = long_prose + "\n\n## Findings ledger\n- [F1] a — anchor: \"q\" — confidence: high\n### Counter-evidence\n- none\n### Open questions\n- y"
    prose, ledger = split_ledger(out)
    assert ledger.startswith("## Findings ledger") and "[F1]" in ledger and "## Findings ledger" not in prose
    ctx = assemble_inner_pass_context({1: out, 2: out}, [1, 2], {1: "discovery", 2: "architecture"})
    assert ctx.count("## Findings ledger") == 2
    assert len(ctx) < 2 * len(out)
    assert "truncated" in ctx


def test_refusal_is_its_own_error():
    err = ModelRefusal("label", "claude-fable-5-1")
    assert isinstance(err, RuntimeError) and err.model_id == "claude-fable-5-1" and "refus" in str(err)
