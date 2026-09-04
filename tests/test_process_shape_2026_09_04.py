"""The process shape (study 2026-09-04): extract → verify → synthesize, routed per step, walled by code."""
import os

import pytest

from src.engines.registry import get_engine_registry
from src.executor.ledger_walls import SourceIndex, check_citations, parse_rows, render_rows, verify_rows
from src.executor.process_runner import ProcessRunResult, preview_prompts, resolve_step_model, run_process
from src.operationalizations.registry import get_operationalization_registry
from src.operationalizations.schemas import ProcessSpec, ProcessStep
from src.stages.capability_composer import compose_all_pass_prompts
from src.stages.process_composer import LEDGER_HEADING, compose_oneshot_prompt

ENGINES = ("conditions_of_possibility_analyzer", "argument_architecture")

SOURCE = (
    "Abstract. We argue that AUKUS is not simply a security partnership, but rather constitutes a mutation of "
    "neoliberalism emerging in the context of bipartisanship. Much of the commentary focuses exclusively on "
    "geopolitics. Labor's support for AUKUS while in opposition was due to a fear of being 'wedged' on defence. "
    "This is not to say that AUKUS as a security partnership is completely geopolitically fetishist. "
    "Regulatory control is motivated by geopolitics, which in turn reshapes market mechanisms."
)


def _op(key):
    return get_operationalization_registry().get(key)


def _cap(key):
    return get_engine_registry().get_capability_definition(key)


def test_both_engines_hold_a_process_and_keep_their_stance_passes():
    for key in ENGINES:
        op = _op(key)
        spec = op.process_for_depth("dvs")
        assert spec is not None and spec.key == "dvs"
        assert [s.kind for s in spec.steps] == ["extract", "verify", "synthesize"]
        assert spec.final_step.is_final and spec.final_step.brief
        doc_dims = [d for d in spec.dimensions if d.scope == "document"]
        assert 5 <= len(doc_dims) <= 6 and all(d.questions and d.method_card and d.answer_shape for d in doc_dims)
        assert any(d.scope == "corpus" for d in spec.dimensions)
        assert op.process_for_depth("deep") is None
        # the four-stance deep path is untouched (the study's production control)
        assert len(compose_all_pass_prompts(_cap(key), depth="deep")) == 4


def test_questions_ask_about_the_text_not_the_authors():
    banned = ("author's prior work", "reputational stake", "embarrassment", "strategic concealment", "why might the author")
    for key in ENGINES:
        for d in _op(key).process.dimensions:
            for q in d.questions:
                assert not any(b in q.lower() for b in banned), (key, d.key, q)


def test_prompts_carry_method_cards_questions_laws_and_ledger_shape():
    for key in ENGINES:
        cap, spec = _cap(key), _op(key).process
        pps = preview_prompts(cap, spec, {"doc": SOURCE})
        kinds = [p.kind for p in pps]
        assert kinds.count("extract") == len([d for d in spec.dimensions if d.scope == "document"])
        assert kinds[-2:] == ["verify", "synthesize"]
        for p in pps:
            assert "Anchoring law" in p.system and LEDGER_HEADING in p.system
            assert "About the text, not the authors" in p.system
        ex = pps[0]
        dim = spec.dimensions[0]
        assert dim.method_card.strip()[:40] in ex.system and dim.questions[0] in ex.system and f"[{dim.id_prefix}.F1]" in ex.system
        syn = pps[-1]
        assert spec.final_step.brief.strip()[:60] in syn.system and "from:" in syn.system
        one = compose_oneshot_prompt(cap, spec, {"doc": SOURCE})
        assert all(d.questions[0] in one.system for d in spec.dimensions if d.scope == "document")


def test_routing_precedence(monkeypatch):
    spec = ProcessSpec(routing={"cheap": "openrouter/a/cheap", "strong": "claude-x"}, steps=[
        ProcessStep(key="e", kind="extract", model_tier="cheap"),
        ProcessStep(key="s", kind="synthesize", model_tier="strong"),
        ProcessStep(key="m", kind="verify", model_tier="mid"),
    ])
    e, s, m = spec.steps
    monkeypatch.delenv("PROCESS_ROUTING_CHEAP", raising=False)
    monkeypatch.delenv("PROCESS_ROUTING_MID", raising=False)
    assert resolve_step_model(e, spec) == "openrouter/a/cheap"
    assert resolve_step_model(s, spec) == "claude-x"
    assert resolve_step_model(s, spec, model_hint="claude-fable-5-1") == "claude-fable-5-1"      # the plan picks the strong model
    assert resolve_step_model(e, spec, model_hint="claude-fable-5-1") == "openrouter/a/cheap"    # never the cheap one
    assert resolve_step_model(m, spec) == "openrouter/deepseek/deepseek-v4-pro"                  # house default for an unrouted tier
    monkeypatch.setenv("PROCESS_ROUTING_CHEAP", "openrouter/env/model")
    assert resolve_step_model(e, spec) == "openrouter/env/model"
    assert resolve_step_model(e, spec, tier_overrides={"cheap": "openrouter/study/model"}) == "openrouter/study/model"
    e2 = ProcessStep(key="e2", kind="extract", model_tier="mid", model="openrouter/explicit/x")
    assert resolve_step_model(e2, spec) == "openrouter/explicit/x"


def test_ledger_walls_verify_anchors_and_ids():
    text = "\n".join([
        LEDGER_HEADING,
        '- [D1.F1] The text presupposes a redefinition — dim: givens — anchor: "constitutes a mutation of neoliberalism emerging in the context of bipartisanship" — depends: the thesis — confidence: high',
        '- [D1.F2] Bad anchor — dim: givens — anchor: "this sentence is nowhere in the source at all" — confidence: low',
        '- [D1.F3] Trimmed anchor — dim: givens — anchor: "Labor\'s support for AUKUS while in opposition was due to a fear of being \'wedged\' on defence and then some words not there" — confidence: medium',
        '- [D1.F3] Duplicate id — dim: givens — anchor: "focuses exclusively on geopolitics" — confidence: medium',
    ])
    rows = parse_rows(text)
    assert [r.id for r in rows] == ["D1.F1", "D1.F2", "D1.F3", "D1.F3"]
    assert rows[0].finding == "The text presupposes a redefinition" and rows[0].dim == "givens" and rows[0].confidence == "high"
    rep = verify_rows(rows, SourceIndex({"doc": SOURCE}))
    assert rep.rows == 4 and rep.verified == 3 and rep.failed_ids == ["D1.F2"] and rep.trimmed == 1 and rep.duplicate_ids == ["D1.F3"]
    assert rows[2].anchor_trimmed and rows[2].anchor.endswith("on defence")
    assert check_citations("as [D1.F1] and [D1.F9] show, see [V.F2]", {"D1.F1"}, also_ok={"V.F2"}) == ["D1.F9"]
    assert render_rows(rows[:1]).startswith(LEDGER_HEADING + "\n- [D1.F1]")
    # ids bolded or numbered the way Sonnet writes them (frontier run, 22:18) still parse
    bold = parse_rows('- **[F1]** A — dim: givens — anchor: "x" — confidence: high\n* [**F2**] B — anchor: "y"\n2. [F3] C — anchor: "z"')
    assert [r.id for r in bold] == ["F1", "F2", "F3"] and bold[0].finding == "A"
    # curly quotes with a page reference after the closing quote (DeepSeek, frontier run 22:22); a counter-anchor is not the anchor
    ds = parse_rows('* [D1.F1] X — dim: givens — anchor: “stops short of addressing structural forces” (p. 110) — depends: y — counter-anchor: "other" — confidence: high')
    assert ds[0].anchor == "stops short of addressing structural forces" and ds[0].confidence == "high"
    # no bullet at all (DeepSeek on paper two, 23:14)
    bare = parse_rows('[F22] The typology would remain valid — dim: rivals — anchor: “The forms presented in Table 1 are ideal types” — confidence: medium')
    assert bare[0].id == "F22" and bare[0].anchor.startswith("The forms presented")
    # a PDF's spaced hyphen ("cross- referenced") verifies against the closed form a model writes, and vice versa
    pdf = SourceIndex({"d": "Data from interviews were cross-  referenced with other sources; a market- driven network."})
    assert pdf.find("interviews were cross-referenced with other sources") == "d"
    assert pdf.find("a market- driven network") == "d" and pdf.find("a market driven network") is None


def _fake_call_factory(log):
    """A fake model: extractions return two rows (one bad anchor), the re-anchor fixes it, the critic rejects
    one row and adds a miss, the synthesis cites ids and closes with a ledger."""
    def call(system, user, *, model_hint, label, **_):
        log.append((label, model_hint))
        if "re-anchor" in label:
            content = LEDGER_HEADING + '\n- [D1.F2] Fixed — dim: givens — anchor: "focuses exclusively on geopolitics" — confidence: medium'
        elif "| extract |" in label:
            prefix = [ln for ln in system.splitlines() if ln.startswith("- [") and ".F1]" in ln][0].split("]")[0][3:].rsplit(".F", 1)[0]
            content = "\n".join([
                LEDGER_HEADING,
                f'- [{prefix}.F1] A given — dim: x — anchor: "constitutes a mutation of neoliberalism" — confidence: high',
                f'- [{prefix}.F2] Bad — dim: x — anchor: "not in the source at all, sadly" — confidence: low',
                "### Counter-evidence\n- none\n### Open questions\n- none",
            ]).replace(f"[{prefix}.F2]", "[D1.F2]" if prefix == "D1" else f"[{prefix}.F2]")
        elif "| verify" in label:
            ids = [ln.split("]")[0][3:] for ln in user.splitlines() if ln.startswith("- [")]
            rows = [f'- [{i}] kept — dim: x — anchor: "constitutes a mutation of neoliberalism" — status: confirmed — reason: ok — confidence: high' for i in ids[:-1]]
            rows.append(f'- [{ids[-1]}] dropped — dim: x — anchor: "constitutes a mutation of neoliberalism" — status: rejected — reason: biography — confidence: low')
            rows.append('- [V.F1] A miss — dim: visibility — anchor: "fear of being \'wedged\' on defence" — status: added — confidence: high')
            content = "\n".join([LEDGER_HEADING] + rows + ["### Must keep\n- V.F1: the mechanism the frame does not own"])
        else:
            content = ("# The reading\n\nThe text rests on one given [D1.F1]; its own evidence names a mechanism the frame does not own [V.F1]. "
                       "A rejected idea [ZZ.F9] is not here.\n\n" + LEDGER_HEADING +
                       '\n- [F1] One given — dim: givens — anchor: "constitutes a mutation of neoliberalism" — from: D1.F1 — confidence: high'
                       '\n- [F2] The mechanism — dim: visibility — anchor: "fear of being \'wedged\' on defence" — from: V.F1 — confidence: high'
                       "\n### Counter-evidence\n- none\n### Open questions\n- none\n### Tables\n- givens: rows F1")
        return {"content": content, "model_used": model_hint, "input_tokens": 1000, "output_tokens": 200, "duration_ms": 5, "retries": 0}
    return call


def test_run_process_end_to_end_with_a_fake_model(monkeypatch):
    for tier in ("CHEAP", "MID", "STRONG"):
        monkeypatch.delenv(f"PROCESS_ROUTING_{tier}", raising=False)
    key = "conditions_of_possibility_analyzer"
    cap, spec = _cap(key), _op(key).process
    log = []
    calls_seen = []
    res = run_process(cap, spec, {"aukus": SOURCE}, tier_overrides={"cheap": "openrouter/openai/gpt-5.6-luna", "mid": "openrouter/deepseek/deepseek-v4-pro", "strong": "claude-sonnet-4-6"},
                      call_fn=_fake_call_factory(log), on_call=calls_seen.append, parallelism=2)
    assert isinstance(res, ProcessRunResult)
    doc_dims = [d for d in spec.dimensions if d.scope == "document"]
    ex = res.calls_for("extract")
    assert len(ex) == len(doc_dims) and all(c.model_used == "openrouter/openai/gpt-5.6-luna" for c in ex)
    # the bad anchor was re-anchored on D1 (the fake fixes only D1.F2) and dropped elsewhere
    d1 = [c for c in ex if c.dimension_key == "givens"][0]
    assert d1.reanchored == 1 and d1.dropped_ids == []
    others = [c for c in ex if c.dimension_key != "givens"]
    assert all(len(c.dropped_ids) == 1 for c in others)
    v = res.calls_for("verify")
    assert len(v) == 1 and v[0].model_used == "openrouter/deepseek/deepseek-v4-pro" and v[0].wall["rejected"] == 1 and v[0].wall["added"] == 1
    s = res.calls_for("synthesize")
    assert len(s) == 1 and s[0].model_used == "claude-sonnet-4-6"
    assert res.final_content.startswith("# The reading") and res.final_wall["anchor_rate"] == 1.0
    assert res.final_wall["missing_cited"] == ["ZZ.F9"]          # a cited id that exists nowhere is reported, never invented
    assert res.cost_usd > 0 and len(calls_seen) == len(res.calls)
    # a 're-anchor' round is not a separate call record, but its tokens are added to the extraction's receipt
    assert d1.input_tokens == 2000


def test_chain_runner_dispatches_a_process_depth(monkeypatch):
    import src.executor.chain_runner as cr

    seen = {}

    def fake_run_process(cap_def, spec, documents, **kw):
        seen["engine"] = cap_def.engine_key; seen["docs"] = list(documents); seen["hint"] = kw.get("model_hint")
        from src.executor.process_runner import ProcessRunResult, StepCall
        sc = StepCall(step_key="synthesize", kind="synthesize", model_used="m", content="# reading\n\n" + LEDGER_HEADING + "\n- [F1] x — anchor: \"y\" — confidence: high")
        kw["on_call"](sc)
        return ProcessRunResult(engine_key=cap_def.engine_key, process_key=spec.key, calls=[sc], final_content=sc.content)

    monkeypatch.setattr("src.executor.process_runner.run_process", fake_run_process)
    monkeypatch.setattr(cr, "save_output", lambda **kw: "po-test")
    monkeypatch.setattr(cr, "update_job_tokens", lambda *a, **kw: None)
    out = cr._run_engine_passes(
        cap_def=_cap("argument_architecture"), document_text="t", depth="dvs", focus_dimensions=None,
        previous_engine_output=None, upstream_context="", context_emphasis=None, engine_label=None,
        job_id="job-test", phase_number=1.0, work_key="w1", model_hint="claude-fable-5-1",
        requires_full_documents=False, cancellation_check=None,
    )
    assert seen == {"engine": "argument_architecture", "docs": ["w1"], "hint": "claude-fable-5-1"}
    assert len(out) == 1 and out[0].stance_key == "synthesize" and out[0].content.startswith("# reading")
