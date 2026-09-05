"""A matching shortened quote must not be reported as a complete original quote."""
import json

from src.dossier.schemas import Anchor
from src.dossier.walls import MAX_QUOTE_CHARS, NormalizedCorpus, verify_anchor
from src.executor.ledger_walls import SourceIndex, parse_rows, render_rows, verify_rows


SOURCE = (
    "The account distinguishes the claims supported by one argument from the conclusions "
    "that retain independent grounds elsewhere in the paper, and preserves each qualification "
    "when a disputed premise is removed from the reconstruction."
)


def test_length_clipping_marks_primary_and_secondary_ledger_anchors_after_roundtrip():
    rows = parse_rows(
        '- [F1] Two anchored routes — anchor: ' + json.dumps(SOURCE)
        + ' — anchor-b: ' + json.dumps(SOURCE)
    )
    index = SourceIndex({"paper": SOURCE})
    report = verify_rows(rows, index)
    assert report.verified_anchors == 2 and report.trimmed == 1
    assert rows[0].anchor == SOURCE[:MAX_QUOTE_CHARS].rstrip()
    rendered = render_rows(rows)
    assert "trimmed-anchor: yes" in rendered and "trimmed-anchor-b: yes" in rendered
    reparsed = parse_rows(rendered)
    assert verify_rows(reparsed, index).trimmed == 1
    assert reparsed[0].anchor_trimmed and reparsed[0].extra_anchors[0].trimmed


def test_dossier_length_clipping_and_reverification_preserve_provenance():
    corpus = NormalizedCorpus({"paper": SOURCE})
    shortened = verify_anchor(Anchor(doc_key="paper", quote=SOURCE), corpus)
    assert shortened is not None and shortened.verified and shortened.trimmed
    assert shortened.quote == SOURCE[:MAX_QUOTE_CHARS].rstrip()
    verified_again = verify_anchor(shortened, corpus)
    assert verified_again is not None and verified_again.trimmed
    assert verified_again.quote == shortened.quote


def test_exact_quote_at_limit_does_not_acquire_a_shortening_flag():
    quote = SOURCE[:MAX_QUOTE_CHARS]
    corpus = NormalizedCorpus({"paper": SOURCE})
    exact = verify_anchor(Anchor(doc_key="paper", quote=quote), corpus)
    assert exact is not None and not exact.trimmed
    rows = parse_rows('- [F1] Finding — anchor: ' + json.dumps(quote))
    assert verify_rows(rows, SourceIndex({"paper": SOURCE})).trimmed == 0


def test_midword_length_cut_preserves_existing_text_and_membership_decision():
    # The held-out critic produced a 204-character anchor ending in a long word.
    source = "An extended source account " * 7 + "supplementaryqualification"
    assert len(source) > MAX_QUOTE_CHARS
    assert source[MAX_QUOTE_CHARS - 1].isalnum() and source[MAX_QUOTE_CHARS].isalnum()
    rows = parse_rows('- [F1] Finding — anchor: ' + json.dumps(source))
    report = verify_rows(rows, SourceIndex({"paper": source}))
    assert report.verified == 1 and report.trimmed == 1
    assert rows[0].anchor == source[:MAX_QUOTE_CHARS]
