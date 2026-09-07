"""The encounter (Evgeny, 2026-09-07 17:40: 'encounter, then impact scan'): the deep operation around one thinker, as records."""
import json
import yaml

from src.engines.schemas_v2 import CapabilityEngineDefinition
from src.operationalizations.registry import get_operationalization_registry


def test_the_encounter_engines_load_with_their_vocabulary_and_recipe():
    from src.vocabularies.registry import get_vocabulary_registry
    from src.dossier.catalog import load_recipes
    from src.sources.citation_evidence import FAMILY
    reg = get_operationalization_registry(); vr = get_vocabulary_registry()
    dims = {}
    for k in ("encounter_map", "encounter_draft"):
        CapabilityEngineDefinition.model_validate(yaml.safe_load(open(f"src/engines/capability_definitions/{k}.yaml")))
        op = reg.get(k); dims[k] = [d.key for d in op.process.dimensions]; assert all(d.scope == "document" for d in op.process.dimensions)
    assert dims == {"encounter_map": ["position", "concept", "opponent", "turn", "silence"], "encounter_draft": ["axis", "relation", "take", "question_back", "read_next"]}
    assert vr.values_for("encounter_draft", "take") == ["absorb", "translate", "refuse", "defer"] and vr.values_for("encounter_draft", "relation")[1] == "collides"
    recipes = {r["key"]: r for r in load_recipes()}
    assert [s["engine_key"] for s in recipes["encounter_round"]["steps"]] == ["encounter_map", "encounter_draft"] and "encounter_draft" in recipes["distinction_settle"]["context"]
    assert {"encounter_map", "encounter_draft"} <= FAMILY


def test_the_encounter_renders_per_axis_with_challenges_and_the_route():
    from src.dossier.encounter import render_encounter
    em = ("[E1.F1] Hintze: the state is an institutional enterprise directed toward power and rule, and rivalry among states shapes it — dim: position — question: whether a logic can be deduced from state activity — text: em:JZJL34ZJ — period: late — locus: pp. 2-3 — anchor: \"the state is an institutional enterprise\" — doc: em:JZJL34ZJ — confidence: high\n"
          "[E2.F1] Staatsräson: the reason of state beside the economic reason — dim: concept — concept: Staatsräson — carries: E1.F1 — puts_to_owner: translate — anchor: \"Wirtschaftsräson neben der Staatsräson\" — doc: em:JZJL34ZJ — confidence: high\n"
          "[E3.F1] Hintze against Marx: the state is not an epiphenomenon of class — dim: opponent — opponent: Marx — question: the state's autonomy — shared: no — anchor: \"not an epiphenomenon\" — doc: em:JZJL34ZJ — confidence: medium\n"
          "[E5.F1] Hintze does not address market dependence in the held windows — dim: silence — question: market dependence — anchor: \"maybe a solution would lie in Otto Hintze\" — doc: focal:turn-11 — confidence: medium")
    ed = ("[X1.F1] The state's own logic versus a response to capital: it decides whether states can be classified like classes — dim: axis — gathers: E1.F1 — parts: 6; 1 — anchor: \"classifying states into different kinds\" — doc: focal:turn-11 — confidence: high\n"
          "[X2.F1] On the state's own logic: parallel — dim: relation — axis: X1.F1 — relation: parallel — ours: states have imperatives of their own — theirs: the state as an enterprise directed to power — bridge: Lane's protection rent — bears_on: 6; 8 — anchor: \"states have a logic\" — doc: argument — confidence: high\n"
          "[X3.F1] translate Staatsräson: into the structural interests of states within the system — dim: take — element: E2.F1 — take: Translate — into: structural interests of states — anchor: \"structural interests\" — doc: focal:turn-11 — confidence: medium\n"
          "[X4.F1] Do you take Hintze's Staatsräson as your states' structural interests, or as one of several imperatives? — dim: question_back — from: X3.F1 — kind: choose — options: the structural interest itself | one imperative among several — anchor: \"structural interests\" — doc: focal:turn-11 — confidence: high\n"
          "[X5.F1] Hintze's essay on the state as enterprise, for the reason of state — dim: read_next — text: em:JZJL34ZJ — held: yes — rank: 1 — axis: X1.F1 — why: it states the enterprise view whole — anchor: \"institutional enterprise\" — doc: em:JZJL34ZJ — confidence: high")
    job = {"id": "d-enc", "analysis": {"4.8": {"engine_key": "encounter_map", "final_output": em, "final_wall": {"failed_ids": []}}, "4.9": {"engine_key": "encounter_draft", "final_output": ed, "final_wall": {"failed_ids": []}}}}
    out = render_encounter(job, thinker="Hintze")
    assert out["rows"] == 9 and out["conjectures"] == 0 and out["thinker"] == "Hintze"
    ax = out["axes"][0]
    assert ax["relations"][0]["relation"] == "parallel" and ax["positions"][0]["locus"] == "pp. 2-3" and ax["route"][0]["held"] == "yes"
    assert ax["positions"][0]["ref"] == "em:JZJL34ZJ" and ax["positions"][0]["text"].startswith("Hintze: the state is an institutional enterprise")   # the sentence stays; the text's uid is `ref`
    assert out["takes"][0]["take"] == "translate" and out["takes"][0]["take_raw"] == "" and out["vocabulary_drift"] == []   # canonical form; a case difference is not drift and keeps no raw
    c = out["challenges"][0]
    assert c["encounter"] is True and c["take"]["take"] == "translate" and c["ask"]["options"] == ["the structural interest itself", "one imperative among several"] and c["relation"] is None
    assert out["silences"][0]["question"] == "market dependence" and out["opponents"][0]["shared"] == "no"
    assert render_encounter({"analysis": {}}) is None


def test_the_encounter_page_reads_as_text_with_titles_and_no_ids_on_the_face():
    from src.dossier.encounter import render_encounter
    from src.dossier.encounter_page import compose_encounter_page, texts_of_job
    em = ("[E1.F1] Hintze: the state is an institutional enterprise directed toward power and rule — dim: position — question: whether a logic can be deduced from state activity — text: em:JZJL34ZJ — period: late — locus: pp. 2-3 — anchor: \"the state is an institutional enterprise\" — doc: em:JZJL34ZJ — confidence: high\n"
          "[E2.F1] Staatsräson: the reason of state beside the economic reason — dim: concept — concept: Staatsräson — carries: E1.F1 — puts_to_owner: translate — anchor: \"Wirtschaftsräson\" — doc: em:JZJL34ZJ — confidence: high\n"
          "[E3.F1] Hintze against Marx: the state is not an epiphenomenon of class — dim: opponent — opponent: Marx — question: autonomy — shared: no — anchor: \"not an epiphenomenon\" — doc: em:JZJL34ZJ — confidence: medium")
    ed = ("[X1.F1] The state's own logic versus a response to capital: whether states can be classified like classes — dim: axis — gathers: E1.F1 — parts: 6 — anchor: \"classifying states\" — doc: focal:turn-11 — confidence: high\n"
          "[X2.F1] On the state's own logic: parallel — dim: relation — axis: X1.F1 — relation: parallel — ours: states have imperatives of their own — theirs: the state as an enterprise directed to power — bridge: Lane's protection rent — bears_on: 6; 8 — anchor: \"states have a logic\" — doc: argument — confidence: high\n"
          "[X3.F1] translate Staatsräson: into the structural interests of states — dim: take — element: E2.F1 — take: translate — into: structural interests of states — anchor: \"structural interests\" — doc: focal:turn-11 — confidence: medium\n"
          "[X4.F1] Do you take Staatsräson as your states' structural interests? — dim: question_back — from: X3.F1 — kind: choose — options: yes | one imperative among several — anchor: \"structural interests\" — doc: focal:turn-11 — confidence: high\n"
          "[X5.F1] Hintze's essay on the state as enterprise — dim: read_next — text: em:JZJL34ZJ — held: yes — rank: 1 — axis: X1.F1 — why: it states the enterprise view whole — anchor: \"institutional enterprise\" — doc: em:JZJL34ZJ — confidence: high")
    job = {"id": "d-enc", "documents": [{"key": "statements-exchange-11", "role": "statements", "executor_doc_id": "s1"}],
           "analysis": {"4.8": {"engine_key": "encounter_map", "final_output": em, "final_wall": {"failed_ids": []}}, "4.9": {"engine_key": "encounter_draft", "final_output": ed, "final_wall": {"failed_ids": []}}}}
    texts = texts_of_job(job, lambda i: json.dumps({"sources": [{"uid": "em:JZJL34ZJ", "title": "The State as an Enterprise and Constitutional Reform", "year": "1927", "creators": "Hintze, Otto"}]}))
    assert texts["em:JZJL34ZJ"]["year"] == "1927"
    html = compose_encounter_page(render_encounter(job, thinker="Hintze"), texts, turn="exchange 11", prose={"encounter_draft": "## Reading\n\nHintze…"}, cost_usd=0.34)
    face = html.split("<details class='about'>")[0]
    assert "<h1>Your encounter with Hintze</h1>" in face and "1927 · The State as an Enterprise and Constitutional Reform" in face and "em:JZJL34ZJ" not in face
    assert "Yours parallel his." in face and "Bears on parts 6, 8." in face and "<b>translate</b>" in face and "against</span>Marx" in face
    assert "[E1.F1]" not in face and "[X" not in face and "How this page was made" in html and "$0.34" in html
