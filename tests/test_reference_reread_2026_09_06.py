"""The owner's references re-read against the texts (Evgeny, 2026-09-06 23:31, relayed by the Stacks' brief session):
the engine loads under Test a position with the registry's verdicts, reads a statements file through the citation
family's index machinery (the comment as A, the works as primary windows), and its rows render to the references
lane's JSON by code, follow-ups ranked."""
import json

from src.dossier.reread import render_reread

COMMENT = "Sewell's critique of Brenner turns on the uncomfortable case of the Dutch, where commercial agriculture arose without lords. Smith's Guatemala work shows regional systems shaping class formation."
SEWELL = "In the Dutch case commercial agriculture developed in the absence of a seigneurial class, which Brenner's model cannot accommodate. I argue that Brenner underestimates this."
FINAL = """## The references, re-read

Sewell does argue the Dutch case against Brenner, though as an anomaly Brenner's model cannot accommodate rather than a refutation (X3.F1). Smith's Guatemala work is not held (X3.F2).

## Follow-up questions

1. Do you take the Dutch case as refuting Brenner or as an anomaly he must absorb? (X4.F1)

## Findings ledger
- [R1.F1] The reader says Sewell's critique of Brenner rests on the Dutch case — dim: recollection — pair-ref: st1/SEWELL — says: Sewell criticises Brenner over the Dutch case — clue: the uncomfortable case of the Dutch — part: part 1 — anchor: "Sewell's critique of Brenner turns on the uncomfortable case of the Dutch" — doc: turn-3 — confidence: high
- [R2.F1] Sewell treats the Dutch case as one Brenner's model cannot accommodate — dim: source_says — pair-ref: st1/SEWELL — p-says: Commercial agriculture arose in the Netherlands without a seigneurial class; Brenner's model cannot accommodate it and underestimates it. — where: the Dutch section — voice: author — anchor: "which Brenner's model cannot accommodate" — doc: em:SEWELL — confidence: high
- [X3.F1] The recollection holds in part: an anomaly, not a refutation — dim: reread — pair-ref: st1/SEWELL — verdict: holds_in_part — reason: Sewell says the model cannot accommodate the case, not that it fails — implication: part 1 should say anomaly, not refutation — anchor: "Sewell's critique of Brenner turns on the uncomfortable case of the Dutch" — doc: turn-3 — anchor-b: "which Brenner's model cannot accommodate" — doc-b: em:SEWELL — confidence: high
- [R1.F2] The reader says Smith's Guatemala work shows regional systems shaping class formation — dim: recollection — pair-ref: st2/SMITH (unheld) — says: regional systems shape class formation — clue: Guatemala — part: part 1 — anchor: "Smith's Guatemala work shows regional systems shaping class formation" — doc: turn-3 — confidence: high
- [X3.F2] Smith's Guatemala work is not held — dim: reread — pair-ref: st2/SMITH — verdict: unverifiable — reason: the work is not held — implication: none until held — anchor: "Smith's Guatemala work shows regional systems shaping class formation" — doc: turn-3 — confidence: high
- [X4.F2] Which of Smith's Guatemala texts do you mean? — dim: follow_up — licensed-by: st2/SMITH — part: part 1 — rank: 2 — anchor: "Smith's Guatemala work shows regional systems" — doc: turn-3 — confidence: medium
- [X4.F1] Do you take the Dutch case as refuting Brenner or as an anomaly he must absorb? — dim: follow_up — licensed-by: st1/SEWELL — part: part 1 — rank: 1 — anchor-b: "I argue that Brenner underestimates this." — doc-b: em:SEWELL — confidence: high
"""


def test_the_engine_loads_under_test_a_position_with_the_registry_verdicts():
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.vocabularies.registry import get_vocabulary_registry
    from src.dossier.catalog import purpose_catalog
    cap = get_engine_registry().get_capability_definition("reference_reread")
    assert cap and [d.key for d in cap.analytical_dimensions] == ["recollection", "source_says", "reread", "follow_up"]
    op = get_operationalization_registry().get("reference_reread")
    assert [d.id_prefix for d in op.process.dimensions] == ["R1", "R2", "X3", "X4"] and [d.scope for d in op.process.dimensions] == ["document", "document", "corpus", "corpus"]
    assert get_vocabulary_registry().values_for("reference_reread", "verdict") == ["holds", "holds_in_part", "diverges", "not_in_text", "unverifiable"]
    cat = purpose_catalog("researcher")
    groups = cat.get("groups") if isinstance(cat, dict) else cat
    assert any(e.get("engine_key") == "reference_reread" for e in next(g for g in groups if g.get("key") == "test_position").get("engines", []))


def test_a_statements_file_reaches_the_engine_as_the_comment_and_the_works():
    from src.sources.citation_evidence import prepare_citation_sources
    obj = {"memo": {"uid": "turn-3", "title": "Evgeny on part 1, turn 3"},
           "statements": [{"no": 1, "section": "part 1", "statement": COMMENT.split(". ")[0] + ".", "sources": ["SEWELL"], "kind": "attribution", "who": "Sewell, William H."},
                          {"no": 2, "section": "part 1", "statement": COMMENT.split(". ")[1], "sources": ["SMITH"], "kind": "attribution"}],
           "sources": [{"label": "SEWELL", "uid": "em:SEWELL", "title": "A critique of Brenner", "year": "1985", "creators": "Sewell, William H.", "text": SEWELL}]}
    docs, context = prepare_citation_sources("reference_reread", {"statements": json.dumps(obj)})
    assert set(docs) == {"turn-3", "em:SEWELL"}
    assert docs["turn-3"].startswith("SOURCE ROLE: citing_author") and "[st1]" in docs["turn-3"] and "[st2]" in docs["turn-3"]
    assert docs["em:SEWELL"].startswith("SOURCE ROLE: primary_window") and "seigneurial" in docs["em:SEWELL"]
    assert "st1/SEWELL" in context and '"label": "SMITH"' in context and "CITATION INDEX METADATA" in context   # SMITH unheld: an unresolved reference, no pair
    # the reception map would not take the works; the reread reads the comment and the works only
    assert prepare_citation_sources("citation_engagement_map", {"statements": json.dumps(obj)})[0].keys() == {"turn-3"}


def test_the_reread_renders_by_code_with_follow_ups_ranked():
    out = render_reread(FINAL, failed=["X4.F2"], refs={"st1": {"no": 1, "who": "Sewell"}})
    assert out["rows"] == 7 and out["conjectures"] == 1 and out["verdicts"] == {"holds_in_part": 1, "unverifiable": 1}
    a, b = out["references"]
    assert a["pair"] == "st1/SEWELL" and a["statement"] == "st1" and a["work"] == "SEWELL" and a["statement_ref"] == {"no": 1, "who": "Sewell"}
    assert a["says"] == "Sewell criticises Brenner over the Dutch case" and a["clue"] == "the uncomfortable case of the Dutch" and a["part"] == "part 1"
    assert a["source_says"].startswith("Commercial agriculture arose") and a["where"] == "the Dutch section" and a["voice"] == "author"
    assert a["verdict"] == "holds_in_part" and a["implication"] == "part 1 should say anomaly, not refutation" and a["rows"] == ["R1.F1", "R2.F1", "X3.F1"]
    assert a["quote"].startswith("Sewell's critique") and a["quote_verified"] and a["quote_b"] == "which Brenner's model cannot accommodate" and a["doc_b"] == "em:SEWELL"
    assert b["pair"] == "st2/SMITH" and b["verdict"] == "unverifiable" and b["source_says"] == "" and b["rows"] == ["R1.F2", "X3.F2"]   # "(unheld)" stripped from the key
    assert a["missing_rows"] == [] and b["missing_rows"] == ["source_says"]
    assert [(f["rank"], f["id"], f["conjecture"]) for f in out["follow_ups"]] == [(1, "X4.F1", False), (2, "X4.F2", True)]
    assert out["follow_ups"][0]["question"].startswith("Do you take the Dutch case") and out["follow_ups"][0]["quote_b"] == "I argue that Brenner underestimates this."
    assert out["summary"].startswith("Sewell does argue the Dutch case") and "(X3.F1)" not in out["summary"]
    assert render_reread("") is None


def test_the_light_call_and_the_job_route_serve_the_reread(monkeypatch):
    from src.dossier.engine_call import call_engine
    from src.dossier.reread import rows_from_job
    from src.sources.schemas import SourceSpec
    obj = {"memo": {"uid": "turn-3", "title": "Evgeny on part 1, turn 3"},
           "statements": [{"no": 1, "section": "part 1", "statement": COMMENT.split(". ")[0] + ".", "sources": ["SEWELL"], "kind": "attribution"},
                          {"no": 2, "section": "part 1", "statement": COMMENT.split(". ")[1], "sources": ["SMITH"], "kind": "attribution"}],
           "sources": [{"label": "SEWELL", "uid": "em:SEWELL", "title": "A critique of Brenner", "year": "1985", "creators": "Sewell, William H.", "text": SEWELL}]}
    src = [SourceSpec(kind="paste", role="statements", key="statements", title="the comment and its works", text=json.dumps(obj))]
    seen = {}

    def fake_call(system, user, *, model_hint, label, **kw):
        seen["user"] = user
        return {"content": FINAL, "model_used": model_hint, "input_tokens": 3000, "output_tokens": 900}

    out = call_engine("reference_reread", src, packet={"turn": 3, "part": "part 1"}, call_fn=fake_call)
    assert "SOURCE [turn-3]" in seen["user"] and "SOURCE [em:SEWELL]" in seen["user"] and "CITATION PACKET" in seen["user"]
    assert out["shaped"]["references"][0]["verdict"] == "holds_in_part" and out["shaped"]["follow_ups"][0]["rank"] == 1
    assert out["wall"]["verified"] >= 4     # the anchors sit in the comment and in Sewell's text
    assert rows_from_job({"analysis": {"4.1": {"engine_key": "reference_reread", "final_output": FINAL, "final_wall": {"failed_ids": ["X4.F2"]}}}}) == (FINAL, {"X4.F2"})
    assert rows_from_job({"analysis": {}}) is None


def test_a_statements_source_reaches_the_engine_on_the_job_path_too():
    """On a dossier job a role=statements source travels as CONTEXT SUPPLIED WITH THE JOB; the chain runner restores it as
    a witness for the family's engines (it restored evidence indexes only, which would have left an engines-only job
    with no source at all, 2026-09-07)."""
    from src.executor.chain_runner import _citation_context_envelopes
    from src.sources.citation_evidence import prepare_citation_sources
    obj = {"memo": {"uid": "turn-8", "title": "Evgeny on part 1, turn 8"},
           "statements": [{"no": 1, "section": "part 1", "statement": "Sewell's critique of Brenner turns on the Dutch case.", "sources": ["SEWELL"], "kind": "attribution"}],
           "sources": [{"label": "SEWELL", "uid": "em:KXEL24MY", "title": "On the Emergence of Capitalism", "year": "2024", "creators": "Sewell, William H.", "text": SEWELL}]}
    upstream = "CONTEXT SUPPLIED WITH THE JOB [statements]:\n" + json.dumps(obj) + "\n\n---\n\nOTHER CONTEXT"
    sources, rest = _citation_context_envelopes("reference_reread", {"target": ""}, upstream)   # the empty corpus of a witness-only job
    assert set(sources) == {"citation-envelope:statements"} and rest.strip().endswith("OTHER CONTEXT") and "turn-8" not in rest
    docs, context = prepare_citation_sources("reference_reread", sources)
    assert set(docs) == {"turn-8", "em:KXEL24MY"} and "st1/SEWELL" in context
    # an engine outside the family keeps the envelope as context
    assert _citation_context_envelopes("argument_architecture", {"d": "x"}, upstream) == ({"d": "x"}, upstream)
