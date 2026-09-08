"""Reviewed PDF columns preserve fragments, not a guessed contiguous envelope."""
import hashlib

import pytest

from src.dossier.pdf_quote_layout import column_views, pdf_column_quote

LEFT = [
    "workers organize around common demands",
    "and build durable institutions together.",
    "their collective capacities can change",
    "when bargaining creates lasting ties.",
    "the research compares different workplaces",
    "and distinguishes protest from organization.",
    "workers face different institutional rules",
    "while contingent staff have fewer resources.",
    "the authors preserve these qualifications",
    "and trace the limits of their evidence.",
    "other findings complicate the initial claim",
    "without replacing one theory with another.",
]
RIGHT = [
    "other scholars describe different outcomes",
    "and insist on careful comparisons of cases.",
    "professional identity may sustain dissent",
    "while failing to create workplace power.",
    "the evidence includes contradictory cases",
    "and several limits on causal inference.",
    "some campaigns win enduring agreements",
    "while others disappear after retaliation.",
    "the mechanism depends on specific context",
    "and should not become a universal sequence.",
    "these differences remain part of the debate",
    "rather than being hidden by one conclusion.",
]


def fixture(left=None, right=None, ending="\n"):
    body = "".join(a.ljust(60) + b + ending for a, b in zip(left or LEFT, right or RIGHT))
    pages = [{"page": 3, "start": 0, "end": len(body)}]
    review = {"reviewed_from_pdf": True, "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
              "pdf_sha256": "frozen-pdf-sha", "method": "test_visual_layout_review",
              "pages": [{"page": 3, "kind": "prose_columns", "columns": 2,
                         "gutter_column": 59, "reviewed_start": 0, "reviewed_end": len(body)}]}
    return body, pages, review


def match(quote, body, pages, review, ranges=None):
    return pdf_column_quote(quote, body, ranges or [(0, len(body))], pages,
                            review=review, pdf_sha256="frozen-pdf-sha")


@pytest.mark.parametrize("ending", ["\n", "\r\n", "\r"])
def test_exact_ordered_fragments_and_original_line_endings(ending):
    body, pages, review = fixture(ending=ending)
    result = match(LEFT[0] + " " + LEFT[1], body, pages, review)
    assert result["quote_match"] == "pdf_column_layout"
    assert result["quote_layout"]["page"] == 3
    assert result["source_quote"] == LEFT[0] + ending + LEFT[1]
    spans = result["quote_spans"]
    assert all(s["text"] == body[s["start"]:s["end"]] for s in spans)
    assert "".join(s["text"] for s in spans) == result["source_quote"]
    assert all(a["end"] <= b["start"] for a, b in zip(spans, spans[1:]))
    assert body[result["quote_start"]:result["quote_end"]] != result["source_quote"]


def test_line_hyphenation_keeps_fragments_and_hyphenated_words():
    left = LEFT.copy();left[0] = "workers share common workplace organi-";left[1] = "zation and worker-identity."
    body, pages, review = fixture(left=left)
    result = match("workers share common workplace organization and worker-identity.", body, pages, review)
    assert result["quote_layout"]["normalization"] == "line_hyphenation"
    assert "organi-\nzation" in result["source_quote"]
    assert match("workers share common workplace organization and workeridentity.", body, pages, review) is None


@pytest.mark.parametrize("damage", ["missing", "not_reviewed", "body_hash", "pdf_hash", "gutter", "region"])
def test_no_layout_interpretation_without_matching_pdf_review(damage):
    body, pages, review = fixture()
    if damage == "missing":review = None
    elif damage == "not_reviewed":review["reviewed_from_pdf"] = False
    elif damage == "body_hash":review["body_sha256"] = "other"
    elif damage == "pdf_hash":review["pdf_sha256"] = "other"
    elif damage == "gutter":review["pages"][0]["gutter_column"] = 20
    else:review["pages"][0]["reviewed_end"] += 1
    assert match(LEFT[0] + " " + LEFT[1], body, pages, review) is None


def test_never_join_unread_ranges_or_different_pages():
    body, pages, review = fixture()
    quote = LEFT[0] + " " + LEFT[1]
    boundary = body.index(LEFT[1])
    assert match(quote, body, pages, review, [(0, boundary), (boundary, len(body))]) is None
    split = [{"page": 3, "start": 0, "end": boundary}, {"page": 4, "start": boundary, "end": len(body)}]
    review["pages"][0]["reviewed_end"] = boundary
    assert match(quote, body, split, review) is None


@pytest.mark.parametrize("caption", ["Table 1: Separate survey rows\n", "Table IV: Results\n",
                                   "left heading".ljust(60) + "Table 1: Separate survey rows\n"])
def test_labeled_tables_rejected_even_if_review_claims_columns(caption):
    body, _, _ = fixture();body = caption + body
    assert column_views(body, 0, len(body)) == []


def test_unlabelled_independent_cells_require_an_external_pdf_review():
    body, pages, _ = fixture()
    assert pdf_column_quote(LEFT[0] + " " + LEFT[1], body, [(0, len(body))], pages) is None


def test_separate_nonmaximal_gutter_is_ambiguous():
    first = "".join(a.ljust(60) + b + "\n" for a, b in zip(LEFT, RIGHT))
    second = "".join((a + " with additional explanatory prose here").ljust(100) + b + "\n"
                     for a, b in zip(LEFT[:8], RIGHT[:8]))
    body = first + second
    assert column_views(body, 0, len(body)) == []


def test_single_space_crossing_header_is_a_barrier():
    body, _, _ = fixture()
    lines = body.splitlines(keepends=True)
    header = "Full width header words crossing the inferred gutter".ljust(59, "x") + " right header tail\n"
    lines.insert(1, header);body = "".join(lines)
    views = column_views(body, 0, len(body))
    assert views and all("\x00" in v[0] for v in views)
    assert all("right header tail" not in v[0] for v in views)


@pytest.mark.parametrize("break_char", ["\u2028", "\u2029", "\v", "\f", "\x85"])
def test_unsupported_line_separators_fail_closed(break_char):
    body, _, _ = fixture(ending=break_char)
    assert column_views(body, 0, len(body)) == []


@pytest.mark.parametrize("quote", ["Workers organize around common demands and build durable institutions together.",
                                  "workers organize around different demands and build durable institutions together."])
def test_no_case_or_word_substitution(quote):
    body, pages, review = fixture()
    assert match(quote, body, pages, review) is None


def test_field_integration_and_cached_rebuild_keep_contiguous_evidence():
    import copy
    from test_field_investigation_2026_09_09 import fixture as inquiry_fixture, freeze, fake
    from src.dossier.field_investigation import run_field_investigation
    raw, _, _, _ = inquiry_fixture(field_count=1, primary_count=1)
    body, pages, review = fixture()
    raw['field'][0].update(body=body, page_spans=pages, source_metadata={'pdf_sha256': 'frozen-pdf-sha'})
    raw['quote_layout_reviews'] = {'referee:0': review}
    _, packet, _, bodies = freeze(raw)
    calls = [];delegate = fake(calls)
    def call(key, sources, **kwargs):
        result = delegate(key, sources, **kwargs)
        if key.endswith('_field_read'):
            result['rows'][0]['anchor'] = LEFT[0] + ' ' + LEFT[1]
        return result
    first = run_field_investigation(packet, bodies, call=call, save=lambda _: None)
    column = next(e for e in first['evidence'] if e['source_role'] == 'field')
    primary = next(e for e in first['evidence'] if e['source_role'] == 'primary')
    assert column['quote_verified'] and column['quote_match'] == 'pdf_column_layout'
    assert column['pages'] == [3] and column['page_urls'] == ['https://example.org/0.pdf#page=3']
    assert 'quote_spans' not in primary
    cached = copy.deepcopy(first);cached['evidence'] = []
    count = len(calls)
    second = run_field_investigation(packet, bodies, call=call, save=lambda _: None, state=cached)
    assert len(calls) == count and second['cost_usd'] == first['cost_usd']
    assert next(e for e in second['evidence'] if e['source_role'] == 'primary') == primary
    assert next(e for e in second['evidence'] if e['source_role'] == 'field') == column


@pytest.mark.parametrize('changed', [False, True])
def test_separate_layout_review_artifact_is_frozen_before_executor(monkeypatch, changed):
    import json
    from src.dossier import investigation as inv, blob_store
    from src.dossier.schemas import DossierJob
    from src.sources.schemas import Document
    body, pages, review = fixture()
    raw = json.dumps({'field:one': review}).encode()
    packet = {'kind': 'field_investigation'}
    restored = {'analysis': {}}
    if changed:restored['quote_layout_review_artifact_sha256'] = 'previous-content-hash'
    monkeypatch.setattr(inv, 'load_investigation', lambda _: restored)
    monkeypatch.setattr(blob_store, 'get_blob', lambda key: ('application/json', raw if key.startswith('investigation-layout-review:') else json.dumps(packet).encode()))
    seen = []
    def execute(*args, **kwargs):
        seen.append(kwargs['state']);return {'analysis': {}}
    job = DossierJob()
    docs = [Document(key='investigation', role='plan', text=json.dumps(packet), title='Frozen plan')]
    if changed:
        with pytest.raises(ValueError, match='review artifact changed'):
            inv.run_job_investigation(job, docs, chain='field_investigation', executor=execute)
        assert not seen
    else:
        inv.run_job_investigation(job, docs, chain='field_investigation', executor=execute)
        assert seen[0]['quote_layout_reviews']['field:one'] == review
        assert seen[0]['quote_layout_review_artifact_sha256'] == hashlib.sha256(raw).hexdigest()
