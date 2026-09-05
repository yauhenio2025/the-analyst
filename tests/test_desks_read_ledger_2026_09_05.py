"""The desks read the findings ledger by id (2026-09-05): verified rows citable, paraphrases apart, rejected rows hidden;
the spine names finding ids and keeps only ones that exist; tables and figures see the ledger."""
from src.dossier import spine as S
from src.dossier import tables as T
from src.dossier.common import analysis_ledger, ledger_ids
from src.dossier.figures import material_text
from src.dossier.schemas import DossierJob, DossierSpine, ExhibitsBudget, SpineSection, SpineTableSpec
from src.sources.schemas import Document

DOC = ("We argue that AUKUS is not simply a security partnership, but rather constitutes a mutation of neoliberalism emerging "
       "in the context of bipartisanship. Labor's support for AUKUS while in opposition was due to a fear of being 'wedged' on defence.")
FINAL = "\n".join([
    "# Reading", "", "The text rests on one given [F1] and names a mechanism the frame does not own [F2]; a stretch [F3] was rejected.", "",
    "## Findings ledger",
    '- [F1] The text presupposes a redefinition of neoliberalism — dim: givens — anchor: "constitutes a mutation of neoliberalism emerging in the context of bipartisanship" — confidence: high',
    '- [F2] The text explains bipartisanship by an electoral mechanism — dim: visibility — anchor: "fear of being \'wedged\' on defence" — confidence: high',
    '- [F4] A paraphrased quote — dim: givens — anchor: "Labour feared being wedged on defence issues" — anchor-verified: no — confidence: medium',
    "### Counter-evidence", "- none", "### Open questions", "- none",
    "### Rejected by the critic",
    '- [F3] About the authors — dim: inheritance — anchor: "constitutes a mutation of neoliberalism" — status: rejected — reason: biography — confidence: low',
    "### Check receipt", "- critic: x; rows in: 4",
])


def _job():
    j = DossierJob()
    j.analysis = {"1.0": {"engine_name": "Conditions of Possibility Analyzer", "final_output": FINAL}}
    return j


def _docs():
    return [Document(key="aukus", title="AUKUS", text=DOC)]


def test_ledger_renders_verified_rows_and_paraphrases_apart_and_hides_rejected():
    out = analysis_ledger(_job(), _docs())
    assert "FINDINGS LEDGER" in out and "verified verbatim" in out
    assert '- [F1] (Conditions of Possibility Analyzer) The text presupposes a redefinition of neoliberalism — anchor [aukus]: "constitutes a mutation' in out
    assert "- [F2] (Conditions of Possibility Analyzer)" in out and "anchor [aukus]" in out
    assert "paraphrase" in out and '- [F4] (Conditions of Possibility Analyzer) A paraphrased quote — near: "Labour feared' in out
    assert "[F3]" not in out and "biography" not in out
    assert ledger_ids(_job()) == {"F1", "F2", "F4"}
    # without documents the rows are listed as written, not re-verified
    plain = analysis_ledger(_job())
    assert "not re-verified" in plain and "[F1]" in plain and "[F3]" not in plain


def test_spine_prompt_carries_the_ledger_and_coerces_finding_ids():
    j = _job()
    user = S._user(j, _docs())
    assert user.index("FINDINGS LEDGER") < user.index("ANALYSIS PROSE") and "[F1]" in user
    assert "finding_ids" in S.SECTION_SCHEMA["properties"] and "finding_ids" not in S.SECTION_SCHEMA["required"]
    assert "FINDINGS LEDGER" in S.SYSTEM
    raw = {"thesis": "T.", "summary_job": "a", "conclusion_job": "b", "sections": [
        {"key": "one", "heading": "One", "claim": "C.", "reader_needs_next": "", "evidence_kind": "mechanism", "table": None, "figure": None,
         "anchors_planned": [{"doc_key": "aukus", "quote": "constitutes a mutation of neoliberalism emerging in the context of bipartisanship"}],
         "feeds": [], "finding_ids": ["F1", "[F2]", "F9"]}]}
    spine = S.coerce_spine(raw, ExhibitsBudget())
    assert spine.sections[0].finding_ids == ["F1", "F2", "F9"]
    known = ledger_ids(j)
    kept = [i for i in spine.sections[0].finding_ids if i in known]
    assert kept == ["F1", "F2"]   # F9 exists in no ledger; build_spine drops it the same way


def test_tables_and_figures_see_the_ledger_and_the_section_findings():
    j = _job()
    j.spine = DossierSpine(thesis="T.", sections=[
        SpineSection(key="one", heading="One", claim="C1.", finding_ids=["F1", "F2"],
                     table=SpineTableSpec(intent="i", row_unit="one row = one given", columns=["Given", "Depends"], carries_claims=["c"]))])
    specs = T._specs_text(j.spine)
    assert "findings this section rests on (ledger ids): F1, F2" in specs
    user = T._spine_user(j, _docs())
    assert "FINDINGS LEDGER" in user and "may be copied character-for-character as row anchors" in T.SPINE_SYSTEM
    mat = material_text(j)
    ledger_block = mat.split("FINDINGS LEDGER", 1)[1].split("ANALYSIS PROSE", 1)[0]
    assert "[F1]" in ledger_block and "[F3]" not in ledger_block   # the prose may mention F3; the ledger block does not offer it


def test_a_foreign_doc_key_does_not_hide_a_verbatim_quote_but_a_wrong_known_key_does():
    from src.executor.ledger_walls import SourceIndex
    idx = SourceIndex({"up47F76C1E": DOC, "other": "Nothing relevant here."})
    q = "constitutes a mutation of neoliberalism"
    assert idx.find(q, prefer="document") == "up47F76C1E"      # the executor's key names no document: search all
    assert idx.find(q, prefer="up47F76C1E") == "up47F76C1E"
    assert idx.find(q, prefer="other") is None                 # a corpus row that names the wrong document fails
    j = _job(); j.analysis["1.0"]["final_output"] = j.analysis["1.0"]["final_output"].replace(
        '— anchor: "constitutes a mutation of neoliberalism emerging in the context of bipartisanship" —',
        '— anchor: "constitutes a mutation of neoliberalism emerging in the context of bipartisanship" — doc: document —')
    out = analysis_ledger(j, _docs())
    assert '- [F1] (Conditions of Possibility Analyzer) The text presupposes a redefinition of neoliberalism — anchor [aukus]' in out
