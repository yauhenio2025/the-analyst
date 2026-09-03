"""The anchor wall: rows without a verbatim anchor are dropped; trimmed/re-keyed anchors are recorded."""
from src.dossier.schemas import Anchor, Cell, Row, Table
from src.dossier.walls import NormalizedCorpus, normalize, verify_anchor, verify_table

DOC_A = """Sustainability and neoliberalism are major contemporary idea systems that permeate a lot of the
discourse in media, corporate board rooms, policy forums, research settings, and classrooms. While
sustainability – as a term and concept – is invoked freely, neoliberalism operates in a somewhat stealth fashion."""
DOC_B = """Digital platforms reconfigure apparel production networks through a spatial-digital fix that relocates
risk to producers, who bear the cost of demand volatility."""


def _corpus():
    return NormalizedCorpus({"A": DOC_A, "B": DOC_B})


def test_normalize_handles_quotes_dashes_and_linebreaks():
    assert normalize("a “quoted” – word\n  next") == 'a "quoted" - word next'
    assert normalize("exploit-\native") == "exploitative"


def test_exact_anchor_verifies_across_linebreak():
    a = verify_anchor(Anchor(doc_key="A", quote="permeate a lot of the discourse in media, corporate board rooms"), _corpus())
    assert a is not None and a.verified and not a.trimmed


def test_typography_differences_are_tolerated():
    a = verify_anchor(Anchor(doc_key="A", quote="sustainability — as a term and concept — is invoked freely"), _corpus())
    assert a is not None and a.verified


def test_wrong_doc_key_is_corrected():
    a = verify_anchor(Anchor(doc_key="A", quote="relocates risk to producers, who bear the cost of demand volatility"), _corpus())
    assert a is not None and a.doc_key == "B"


def test_paraphrase_is_rejected_and_trailing_junk_is_trimmed():
    assert verify_anchor(Anchor(doc_key="A", quote="Sustainability and neoliberalism are the two dominant ideologies of our age"), _corpus()) is None
    t = verify_anchor(Anchor(doc_key="A", quote="neoliberalism operates in a somewhat stealth fashion and hides its engines"), _corpus())
    assert t is not None and t.trimmed and t.quote == "neoliberalism operates in a somewhat stealth fashion"


def test_verify_table_drops_rows_without_verified_anchor():
    table = Table(key="t", caption="c", columns=["Thing", "Evidence"], rows=[
        Row(cells=[Cell(value="ok row"), Cell(value="x", anchor=Anchor(doc_key="A", quote="neoliberalism operates in a somewhat stealth fashion"))]),
        Row(cells=[Cell(value="bad row"), Cell(value="y", anchor=Anchor(doc_key="B", quote="this sentence is nowhere in the documents at all"))]),
        Row(cells=[Cell(value="no anchor row"), Cell(value="z")]),
        Row(cells=[Cell(value="rekeyed row"), Cell(value="w", anchor=Anchor(doc_key="A", quote="Digital platforms reconfigure apparel production networks"))]),
    ])
    out, report = verify_table(table, _corpus())
    assert [r.cells[0].value for r in out.rows] == ["ok row", "rekeyed row"]
    assert out.rows_dropped == 2 and report["rows_dropped"] == 2
    assert report["anchors_rekeyed"] == 1 and report["anchors_dropped"] == 1
    assert out.rows[1].cells[1].anchor.doc_key == "B"
    assert len(report["failed_quotes"]) == 1
