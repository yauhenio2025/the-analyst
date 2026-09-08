"""Constructive methods are discoverable records consumed by the ordinary engine runner.

The subscription adapter can reuse their method text without inheriting dossier row syntax.
These checks use a fake model call and never request a paid inference.
"""

import asyncio

import pytest

from src.engines.registry import get_engine_registry
from src.operationalizations.registry import get_operationalization_registry


METHODS = ("constructive_inquiry", "constructive_retest")


@pytest.fixture(autouse=True)
def _isolate_registry_history(monkeypatch, tmp_path):
    from src.engines import history_tracker

    monkeypatch.setattr(history_tracker, "HISTORY_DIR", tmp_path / "capability_history")


def _records(key):
    cap = get_engine_registry().get_capability_definition(key)
    op = get_operationalization_registry().get(key)
    assert cap is not None and op is not None and op.process is not None
    return cap, op


def test_constructive_methods_are_discoverable_without_legacy_duplicates():
    from src.api.routes.engines import get_capability_definition, list_engines
    from src.api.routes.operationalizations import get_operationalization

    summaries = asyncio.run(
        list_engines(
            category=None, paradigm=None, app=None, function=None,
            search="constructive", family=None, organ=None,
        )
    )
    keys = [summary.engine_key for summary in summaries]
    for key in METHODS:
        assert keys.count(key) == 1
        cap = asyncio.run(get_capability_definition(key))
        op = asyncio.run(get_operationalization(key))
        assert cap.engine_key == op.engine_key == key
        assert get_engine_registry().get(key) is None
        assert cap.output_mode == "prose" and cap.output_contract is None
        assert {dimension.key for dimension in cap.analytical_dimensions} == {
            dimension.key for dimension in op.process.dimensions
        }
        assert all(op.mode_for_depth(depth) == "oneshot" for depth in ("surface", "standard", "deep"))


@pytest.mark.parametrize("key", METHODS)
def test_oneshot_composer_consumes_the_central_method_and_ledger_contract(key):
    from src.stages.process_composer import compose_oneshot_prompt

    cap, op = _records(key)
    cap = cap.model_copy(update={"problematique": "CAPABILITY DESCRIPTION IS NOT THE METHOD"})
    spec = op.process
    prompt = compose_oneshot_prompt(cap, spec, {"held-case": "The case material."})

    assert spec.framing in prompt.system
    assert spec.final_step.brief in prompt.system
    assert "CAPABILITY DESCRIPTION IS NOT THE METHOD" not in prompt.system
    assert "## Findings ledger" in prompt.system
    assert len({dimension.id_prefix for dimension in spec.dimensions}) == len(spec.dimensions)
    for dimension in spec.dimensions:
        assert dimension.method_card in prompt.system
        assert all(question in prompt.system for question in dimension.questions)
        assert dimension.answer_shape in prompt.system
        assert f"dim: {dimension.key}" in dimension.answer_shape
        assert "anchor:" in dimension.answer_shape and "doc:" in dimension.answer_shape


@pytest.mark.parametrize("key,prefix", [("constructive_inquiry", "C3"), ("constructive_retest", "R2")])
def test_light_engine_call_keeps_anchored_rows_and_context_separate(key, prefix):
    from src.dossier.engine_call import call_engine
    from src.sources.schemas import SourceSpec

    quote = "The council changed the rules before any selection occurred."
    calls = []
    cap, op = _records(key)

    def fake_model(system, user, **kwargs):
        calls.append((system, user, kwargs))
        return {
            "content": (
                f"The temporal ordering challenges the proposed mechanism [{prefix}.F1].\n\n"
                "## Findings ledger\n"
                f'- [{prefix}.F1] The rules changed before selection — dim: evidence '
                f'— basis: source_claim — bearing: challenges — interpretation: the proposed causal order needs revision '
                f'— location: unknown — anchor: "{quote}" — doc: held-case — confidence: medium\n'
                f'- [{prefix}.F2] A claim available only in context — dim: evidence '
                '— anchor: "Selection necessarily causes every change in the rules." '
                '— doc: held-case — confidence: low'
            ),
            "model_used": kwargs["model_hint"],
            "input_tokens": 0,
            "output_tokens": 0,
        }

    result = call_engine(
        key,
        [SourceSpec(key="held-case", text=quote)],
        packet={
            "commitments": [{"id": "author-c1", "text": "Selection necessarily causes every change in the rules."}],
            "question": "How did these rules arise?",
            "previous_result": {"id": "prior-1", "account": "Selection generates rules."},
            "test": {"id": "test-1", "question": "Did selection precede the rule change?"},
        },
        depth="surface",
        model="openrouter/openai/gpt-5.6-sol",
        spend_cap_usd=100,
        call_fn=fake_model,
    )

    assert len(calls) == 1
    system, user, _ = calls[0]
    assert op.process.framing in system and op.process.final_step.brief in system
    assert '"author-c1"' in user and '"test-1"' in user and '"prior-1"' in user
    assert "SOURCE [held-case]:" in user
    assert result["engine_key"] == cap.engine_key
    assert result["cost_usd"] == 0
    assert result["wall"]["verified"] == 1
    assert result["wall"]["failed_ids"] == [f"{prefix}.F2"]
    assert result["rows"][0]["anchor_verified"] is True
    assert result["rows"][0]["fields"]["bearing"] == "challenges"
    assert result["rows"][1]["anchor_verified"] is False
