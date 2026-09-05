"""Every engine with a process runs the same shape: modes per depth, text-facing questions, method cards, Sol as the strong tier."""
from src.engines.registry import get_engine_registry
from src.executor.process_runner import preview_prompts
from src.operationalizations.registry import get_operationalization_registry
from src.stages.process_composer import LEDGER_HEADING, compose_oneshot_prompt

UNDER_THE_SHAPE = ("conditions_of_possibility_analyzer", "argument_architecture", "inferential_commitment_mapper", "epistemological_method_detector",
                   "deep_summarization", "statistical_evidence", "event_timeline_causal")   # + the first-queue methods S1, E8, T1 (2026-09-06)
BANNED = ("author's prior work", "reputational", "embarrass", "would the author be comfortable", "husserlian critique", "the author's own social position")


def test_four_engines_share_the_shape():
    reg = get_operationalization_registry()
    for key in UNDER_THE_SHAPE:
        op = reg.get(key); spec = op.process
        assert spec is not None, key
        assert {d: op.mode_for_depth(d) for d in ("surface", "standard", "deep", "dvs")} == {"surface": "oneshot", "standard": "oneshot_checked", "deep": "dvs", "dvs": "dvs"}, key
        assert spec.routing["strong"] == "openrouter/openai/gpt-5.6-sol" and spec.routing["mid"].endswith("deepseek-v4-pro")
        doc_dims = [d for d in spec.dimensions if d.scope == "document"]
        assert 5 <= len(doc_dims) <= 6 and any(d.scope == "corpus" for d in spec.dimensions), key
        for d in spec.dimensions:
            assert d.questions and d.method_card and d.answer_shape and d.indicators, (key, d.key)
            assert "Do:" in d.method_card, (key, d.key)   # a card says what to DO
            for q in d.questions:
                assert not any(b in q.lower() for b in BANNED), (key, d.key, q)
        assert sum(1 for d in doc_dims if d.load_bearing) >= 3, key
        assert "1." in spec.final_step.brief and "2." in spec.final_step.brief and spec.final_step.reader and spec.final_step.tables, key   # a numbered reader's order (a preamble rule may precede it)


def test_prompts_compose_for_the_new_engines():
    reg = get_operationalization_registry(); ereg = get_engine_registry()
    for key in ("inferential_commitment_mapper", "epistemological_method_detector", "deep_summarization", "statistical_evidence", "event_timeline_causal"):
        cap = ereg.get_capability_definition(key); spec = reg.get(key).process
        one = compose_oneshot_prompt(cap, spec, {"doc": "text"})
        assert LEDGER_HEADING in one.system and "Anchoring law" in one.system and spec.dimensions[0].questions[0] in one.system
        pps = preview_prompts(cap, spec, {"doc": "text"})
        assert [p.kind for p in pps][-2:] == ["verify", "synthesize"] and len([p for p in pps if p.kind == "extract"]) == 5
