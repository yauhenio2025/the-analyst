"""Header parsing of a stacks export (3-item fixture) and the paste auto-split."""
from src.sources.resolve import resolve_sources
from src.sources.schemas import SourceSpec
from src.sources.stacks import looks_like_stacks_export, parse_header, split_stacks_export

FIXTURE = """STACKS EXPORT — 3 items — 2026-09-03 04:44 UTC
Each item starts with a line of the form:  ===== [n/N] Creator (Year) — Title — Publication — [Library · Key] =====

CONTENTS
===== [1/3] Dholakia, Nikhilesh; Ziliberberg, Cristian (2024) — Change and Legitimation Narratives — Sustainability in Art, Fashion and Wine — [EM Book Research · SG4IGV3Y] =====
===== [2/3] Kuang, Aiping et al. (2024) — Digital Platform, Spatial-Digital Fix — Economic Geography 100/5-6 — [EM Book Research · XDYU5FSQ] =====
===== [3/3] Nassar, Alexandre (2021) — Brand activism: Towards a better understanding — EMAC Conference — [EM Book Research · U3PWD6J3] =====



===== [1/3] Dholakia, Nikhilesh; Ziliberberg, Cristian (2024) — Change and Legitimation Narratives — Sustainability in Art, Fashion and Wine — [EM Book Research · SG4IGV3Y] =====

Sustainability and neoliberalism are major contemporary idea systems that permeate a lot of the discourse in media.
The fashion industry is a case in point. Sustainability aspects of fast fashion get high visibility.

===== [2/3] Kuang, Aiping et al. (2024) — Digital Platform, Spatial-Digital Fix — Economic Geography 100/5-6 — [EM Book Research · XDYU5FSQ] =====

Digital platforms reconfigure apparel production networks through a spatial-digital fix that relocates risk to producers.
Second paragraph of the second paper, long enough to count as a body.

===== [3/3] Nassar, Alexandre (2021) — Brand activism: Towards a better understanding — EMAC Conference — [EM Book Research · U3PWD6J3] =====

Brand activism is examined in the light of the Economies of Worth theory, where brands justify their stances.
"""


def test_split_skips_contents_and_yields_three_documents():
    docs = split_stacks_export(FIXTURE)
    assert [d.key for d in docs] == ["SG4IGV3Y", "XDYU5FSQ", "U3PWD6J3"]
    assert docs[0].creators == "Dholakia, Nikhilesh; Ziliberberg, Cristian"
    assert docs[0].year == "2024"
    assert docs[0].title == "Change and Legitimation Narratives"
    assert docs[0].publication == "Sustainability in Art, Fashion and Wine"
    assert docs[0].library == "EM Book Research"
    assert docs[1].creators == "Kuang, Aiping et al."
    assert docs[2].year == "2021"
    assert docs[0].text.startswith("Sustainability and neoliberalism")
    assert "=====" not in docs[0].text
    assert docs[1].text.endswith("count as a body.")
    assert all(d.char_count == len(d.text) for d in docs)


def test_parse_header_tolerates_missing_parts():
    h = parse_header("Someone (2020) — A Title")
    assert h["creators"] == "Someone" and h["year"] == "2020" and h["title"] == "A Title" and h["publication"] == ""
    h2 = parse_header("Just a title")
    assert h2["title"] == "Just a title"
    h3 = parse_header("Author (2019) — Title — With — Dashes — Journal — [Lib · KEY1]")
    assert h3["title"] == "Title — With — Dashes" and h3["publication"] == "Journal" and h3["stacks_key"] == "KEY1"


def test_paste_auto_splits_and_plain_paste_is_single_document():
    assert looks_like_stacks_export(FIXTURE)
    docs = resolve_sources([SourceSpec(kind="paste", text=FIXTURE)])
    assert len(docs) == 3
    plain = resolve_sources([SourceSpec(kind="paste", title="Memo", text="A plain memo.\n\nWith two paragraphs.")])
    assert len(plain) == 1 and plain[0].title == "Memo" and plain[0].key == "memo"
    both = resolve_sources([SourceSpec(kind="paste", text=FIXTURE), SourceSpec(kind="paste", text=FIXTURE)])
    assert len(both) == 6 and len({d.key for d in both}) == 6
