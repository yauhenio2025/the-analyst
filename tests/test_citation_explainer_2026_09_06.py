"""One citation explained in its place (owner, 2026-09-06: "shouldn't explaining citations be folded into the engines?"):
the engine loads under Trace the citations, its vocabularies are the registry's, its rows render to the Stacks'
explanation shape by code, and the light call route runs it in the request through the walls without a dossier job."""
import pytest

from src.dossier.explainer import render_explanation, rows_with_fields

SECTION = ("Weber's concept of political capitalism was developed to describe the ancient world. Riley argues that the "
           "United States now fits it. As Weber put it, profit here comes from the state rather than the market. This is a "
           "reading, not a proof; the evidence is in the data on rents.")

FINAL = """## How

Weber is cited as an authority whose concept the text borrows: political capitalism names a form of profit-making Riley applies to the present (E1.F1).

## Why here

The passage needs Weber's definition to license its central move, calling the American case political capitalism (E2.F1).

## In the argument

The section opens the argument; Weber's concept is the adopted framework, and the section then narrows it to rents (E3.F1).

## Findings ledger
- [E1.F1] Weber is invoked as the named authority for the concept the text applies — dim: how — ref: 2583 — move: authority — stance: adopts — object: the concept of political capitalism — anchor: "As Weber put it, profit here comes from the state rather than the market." — doc: em:C9LPBLYH — confidence: high
- [E1.F2] Riley later turns the same concept against its source, disputing the wider claim — dim: how — ref: 2583 — move: foil — stance: disputes — object: the wider claim — anchor: "This is a reading, not a proof; the evidence is in the data on rents." — doc: em:C9LPBLYH — confidence: medium
- [E2.F1] The passage needs the definition to call the American case political capitalism — dim: why_here — ref: 2583 — supports: the United States now fits it — qualification: a reading, not a proof — anchor: "This is a reading, not a proof" — doc: em:C9LPBLYH — confidence: medium
- [E3.F1] The section opens the argument and adopts Weber's concept as its framework — dim: in_argument — ref: 2583 — section-role: the opening definition — place: adopted_framework — anchor: "Weber's concept of political capitalism was developed to describe the ancient world." — doc: em:C9LPBLYH — confidence: high
"""


def test_the_engine_loads_with_the_registry_vocabularies_and_sits_under_trace_the_citations():
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.vocabularies.registry import get_vocabulary_registry
    from src.dossier.catalog import purpose_catalog
    cap = get_engine_registry().get_capability_definition("citation_explainer")
    assert cap and [d.key for d in cap.analytical_dimensions] == ["how", "why_here", "in_argument", "across_texts"]
    op = get_operationalization_registry().get("citation_explainer")
    assert op and [d.id_prefix for d in op.process.dimensions] == ["E1", "E2", "E3", "X4"]
    assert [m.mode for m in op.depth_sequences if m.depth_key in ("surface", "standard")] == ["oneshot", "oneshot_checked"]
    reg = get_vocabulary_registry()
    assert reg.values_for("citation_explainer", "move") == reg.get("citation_moves").value_list()
    assert reg.values_for("citation_explainer", "stance") == reg.get("citation_stances").value_list()
    assert reg.values_for("citation_explainer", "place") == ["evidence", "adopted_framework", "opponent", "courtesy", "qualified_role"]
    assert reg.values_for("citation_explainer", "relation") == ["continuity", "change", "contrast", "unordered"]
    cat = purpose_catalog("researcher")
    groups = cat.get("groups") if isinstance(cat, dict) else cat
    tc = next(g for g in groups if g.get("key") == "trace_citations")
    assert any(e.get("engine_key") == "citation_explainer" for e in tc.get("engines", []))


def test_the_explanation_renders_from_the_rows_by_code():
    rows = rows_with_fields(FINAL, failed=["E2.F1"])
    assert [r["id"] for r in rows] == ["E1.F1", "E1.F2", "E2.F1", "E3.F1"] and rows[2]["conjecture"] and not rows[0]["conjecture"]
    out = render_explanation(FINAL, failed=["E2.F1"], refs={"2583": {"ref_id": 2583}})
    assert out["rows"] == 4 and out["conjectures"] == 1 and len(out["explanations"]) == 1
    e = out["explanation"]
    assert e["ref"] == "2583" and e["doc"] == "em:C9LPBLYH" and e["citation"] == {"ref_id": 2583}
    assert e["intent"] == e["move"] == "authority" and e["stance"] == "adopts" and e["place"] == "adopted_framework"
    assert e["quote"] == "As Weber put it, profit here comes from the state rather than the market." and e["quote_verified"] is True
    assert e["how"].startswith("Weber is cited as an authority") and "(E1.F1)" not in e["how"]      # the reading's part, ids stripped
    assert e["why"].startswith("The passage needs Weber's definition") and e["fit"].startswith("The section opens the argument")
    assert e["supports"] == "the United States now fits it" and e["qualification"] == "a reading, not a proof" and e["section_role"] == "the opening definition"
    assert e["rows"] == ["E1.F1", "E1.F2", "E2.F1", "E3.F1"] and e["conjectures"] == 1
    assert [(m["id"], m["move"], m["stance"]) for m in e["more"]] == [("E1.F2", "foil", "disputes")]   # the first row is the headline
    assert render_explanation("") is None
    bold = FINAL.replace("## How\n\n", "## Reading\n\n**How.** ").replace("\n\n## Why here\n\n", "\n\n**Why here.** ").replace("\n\n## In the argument\n\n", "\n\n**In the argument.** ")
    e2 = render_explanation(bold)["explanation"]
    assert e2["how"].startswith("Weber is cited as an authority") and e2["fit"].startswith("The section opens the argument") and "(E3.F1)" not in e2["fit"]


def test_the_light_call_runs_the_engine_through_the_walls_in_the_request():
    from src.dossier.engine_call import call_engine, normalize_model
    from src.sources.schemas import SourceSpec
    seen = {}

    def fake_call(system, user, *, model_hint, label, **kw):
        seen["system"], seen["user"], seen["model"] = system, user, model_hint
        return {"content": FINAL, "model_used": model_hint, "input_tokens": 4000, "output_tokens": 600, "duration_ms": 1200}

    src = [SourceSpec(kind="paste", key="em:C9LPBLYH", title="Riley, Dylan (2014) — Back to Weber!", text=SECTION)]
    packet = {"citation_id": "2583", "person": "Weber, Max", "passage": "As Weber put it, profit here comes from the state rather than the market."}
    out = call_engine("citation_explainer", src, packet=packet, depth="surface", model="anthropic/claude-sonnet-5", call_fn=fake_call)
    assert seen["model"] == "claude-sonnet-5" and "CITATION PACKET" in seen["user"] and "SOURCE [em:C9LPBLYH]" in seen["user"]
    assert "One citation explained" in seen["system"] or "citation_explainer" in seen["system"]
    assert "at most 2 rows per dimension" in seen["system"]     # the one-call ledger honours the final step's max_rows
    assert out["engine_key"] == "citation_explainer" and out["depth"] == "surface" and out["model"] == "claude-sonnet-5"
    assert [r["id"] for r in out["rows"]] == ["E1.F1", "E1.F2", "E2.F1", "E3.F1"]
    assert out["wall"] == {"anchors": 4, "verified": 4, "failed_ids": []} and out["rows"][0]["fields"]["move"] == "authority"
    assert out["shaped"]["explanation"]["quote_verified"] is True and out["shaped"]["explanation"]["intent"] == "authority"
    assert out["cost_usd"] > 0 and out["estimated_usd"] > 0 and len(out["calls"]) == 1 and out["calls"][0]["step"] == "read"
    # the wall catches a quote that is not in the section
    bad = FINAL.replace("As Weber put it, profit here comes from the state rather than the market.", "Weber said the state is the source of profit.")
    out2 = call_engine("citation_explainer", src, packet=packet, call_fn=lambda *a, **k: {"content": bad, "model_used": "m"})
    assert out2["wall"]["failed_ids"] == ["E1.F1"] and out2["shaped"]["explanation"]["quote_verified"] is False
    # refusals before spending
    with pytest.raises(ValueError):
        call_engine("citation_explainer", src, packet=packet, spend_cap_usd=0.0, call_fn=fake_call)
    with pytest.raises(ValueError):
        call_engine("citation_explainer", src, depth="deep", call_fn=fake_call)
    with pytest.raises(KeyError):
        call_engine("no_such_engine", src, call_fn=fake_call)
    assert normalize_model("openai/gpt-5.6-sol-pro") == "openrouter/openai/gpt-5.6-sol-pro" and normalize_model("claude-sonnet-5") == "claude-sonnet-5"
    with pytest.raises(ValueError):
        normalize_model("sonnet")


def test_the_route_maps_errors_to_status_codes(monkeypatch):
    from fastapi import HTTPException
    from src.api.routes import engines as R
    from src.sources.schemas import SourceSpec
    req = R.EngineCallRequest(sources=[SourceSpec(kind="paste", key="k", text="t")])
    monkeypatch.setattr("src.dossier.engine_call.call_engine", lambda *a, **k: (_ for _ in ()).throw(KeyError("no engine")))
    with pytest.raises(HTTPException) as e:
        R.call_engine_route("x", req)
    assert e.value.status_code == 404
    monkeypatch.setattr("src.dossier.engine_call.call_engine", lambda *a, **k: (_ for _ in ()).throw(ValueError("over the cap")))
    with pytest.raises(HTTPException) as e:
        R.call_engine_route("x", req)
    assert e.value.status_code == 400 and "cap" in e.value.detail
    monkeypatch.setattr("src.dossier.engine_call.call_engine", lambda *a, **k: {"ok": True})
    assert R.call_engine_route("x", req) == {"ok": True}
