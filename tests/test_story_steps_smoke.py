"""Smoke tests for the story desk: module constants, the verbatim re-cut, and the windows table."""
from src.story import steps
from src.story.schemas import APPROACHES, APPROACH_WINDOWS


def test_step_names_present():
    assert set(steps.STEP.values()) == {"reconnaissance", "map", "approaches", "brief", "spine", "handoff"}


def test_raw_verbatim_folds_hyphenation_dashes_and_case():
    text = "The Liberal–National Coali-\ntion government, under then Prime Minister Scott Morrison, signed."
    q = "the liberal-national coalition government, under then prime minister scott morrison"
    raw = steps.raw_verbatim(q, text)
    assert raw is not None and raw in text and raw.startswith("The Liberal")


def test_raw_verbatim_rejects_paraphrase():
    assert steps.raw_verbatim("a sentence that is not there", "The quick brown fox.") is None


def test_every_approach_has_a_window():
    assert set(APPROACH_WINDOWS) == set(APPROACHES)
    assert all(lo < hi for lo, hi in APPROACH_WINDOWS.values())
