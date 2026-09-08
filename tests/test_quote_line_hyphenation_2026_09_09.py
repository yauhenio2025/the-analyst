"""Source-exact regressions for PDF line-wrap hyphenation; no remote calls."""
import pytest

from src.dossier.investigation import quote_span


# The six originally unverified quotes in referee:402074's first saved reading.
PDF_QUOTES = [('F2',
  'Finally, we examine how this work ethic requires both bosses and workers to be devoted to '
  'innovation and to the company, generating a form of enthusiastic docility.',
  'Finally, we examine how\n'
  'this work ethic requires both bosses and workers to be devoted to inno-\n'
  'vation and to the company, generating a form of enthusiastic docility.'),
 ('F3',
  'First, much of Silicon Valley attaches a utopian, civilizational mission and importance to '
  'conventional understandings of work and labor.',
  'First, much of Silicon Valley attaches a utopian, civili-\n'
  'zational mission and importance to conventional understandings of\n'
  'work and labor.'),
 ('F7',
  'Silicon Valley bosses have historically attempted to strategically divide workers along ethnic, '
  'class, and gender lines so as to discourage solidarity and meaningful organizing.',
  'Silicon Valley bosses have historically attempted to strate-\n'
  'gically divide workers along ethnic, class, and gender lines so as to\n'
  'discourage solidarity and meaningful organizing.'),
 ('F9',
  'Musk’s ideology of work valorizes highly skilled, innovative, complex forms of labor in a way '
  'that renders unseen the everyday, lower-paid, and lower-skilled kinds of work',
  'Musk’s ideology of work valo-\n'
  'rizes highly skilled, innovative, complex forms of labor in a way that\n'
  'renders unseen the everyday, lower-paid, and lower-skilled kinds of\n'
  'work'),
 ('F12',
  'he demonstrates no inclination to give workers on Earth any democratic control on the factory '
  'floor.',
  'he demonstrates no inclination to give workers on Earth any demo-\n'
  'cratic control on the factory floor.'),
 ('F19',
  'efforts to incorporate an anti-work politics into theorizations of democracy and “the good '
  'life,” one that helps imagine futurities beyond the tireless need to labor, are essential for '
  'this task.',
  'efforts to incorporate an anti-work politics into theorizations of democ-\n'
  'racy and “the good life,” one that helps imagine futurities beyond the\n'
  'tireless need to labor, are essential for this task.')]


@pytest.mark.parametrize("finding,quote,source", PDF_QUOTES)
def test_real_field_quotes_keep_original_pdf_span(finding, quote, source):
    prefix = "Unread preface. "
    body = prefix + source + " Unread conclusion."
    lo, hi = len(prefix), len(prefix) + len(source)
    span = quote_span(quote, body, [(lo, hi)])
    assert span == (lo, hi, "line_hyphenation"), finding
    assert body[span[0]:span[1]] == source
    assert quote_span(source, body, [(lo, hi)]) == (lo, hi, "exact")


@pytest.mark.parametrize("newline", ["\n", "\r", "\r\n"])
@pytest.mark.parametrize("indent", ["", " ", "\t    "])
def test_one_line_ending_and_indentation(newline, indent):
    source = "The inno-" + newline + indent + "vation\nmatters."
    assert quote_span("The innovation matters.", source, [(0, len(source))]) == (
        0, len(source), "line_hyphenation"
    )


@pytest.mark.parametrize("source,quote", [
    ("inno-vation", "innovation"),
    ("inno- vation", "innovation"),
    ("inno- \nvation", "innovation"),
    ("inno-\n\nvation", "innovation"),
    ("inno-\n \t\nvation", "innovation"),
    ("inno-\r\n \r\nvation", "innovation"),
    ("inno-\nVation", "innoVation"),
    ("inno-\nvation", "innoVation"),
    ("inno-\nvation", "innovations"),
    ("inno-\nvation!", "innovation?"),
    ("inno\u00ad\nvation", "innovation"),
    ("inno\u2010\nvation", "innovation"),
    ("1-\na", "1a"),
    ("a-\n1", "a1"),
    ("inno-\nvation and anti-work", "innovation and antiwork"),
])
def test_only_narrow_line_hyphenation_is_permitted(source, quote):
    assert quote_span(quote, source, [(0, len(source))]) is None


@pytest.mark.parametrize("split", [4, 5, 6, 7])
def test_adjacent_inspected_windows_cannot_be_joined(split):
    source = "inno-\nvation"
    assert quote_span("innovation", source, [(0, split), (split, len(source))]) is None


def test_disjoint_windows_cannot_be_joined():
    source = "inno-\nunread vation"
    assert quote_span("innovation", source, [(0, 6), (13, len(source))]) is None


def test_match_stays_inside_range_even_at_hyphenation_boundary():
    source = "inno-\nvation"
    assert quote_span("innovation", source, [(1, len(source))]) is None
    assert quote_span("innovation", source, [(0, len(source) - 1)]) is None


def test_mixed_preserved_and_removed_hyphens():
    source = "Anti-work inno-\nvation and demo-\ncracy."
    assert quote_span("Anti-work innovation and democracy.", source, [(0, len(source))]) == (
        0, len(source), "line_hyphenation"
    )


def test_exact_and_whitespace_precedence_remain_unchanged():
    body = "inno-\nvation. innovation."
    start = body.index("innovation")
    assert quote_span("innovation.", body, [(0, len(body))]) == (start, len(body), "exact")
    body = "inno-\nvation matters. innovation\nmatters."
    start = body.index("innovation")
    assert quote_span("innovation matters.", body, [(0, len(body))]) == (
        start, len(body), "whitespace_only"
    )
    assert quote_span("", body, [(0, len(body))]) is None
    assert quote_span("   ", body, [(0, len(body))]) is None
