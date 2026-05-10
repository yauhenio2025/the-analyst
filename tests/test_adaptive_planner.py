from src.orchestrator.adaptive_planner import _normalize_chapter_targets


def test_normalize_chapter_targets_accepts_scalar_ids():
    targets = _normalize_chapter_targets(["ch1", " appendix_a "])

    assert targets is not None
    assert [target.chapter_id for target in targets] == ["ch1", "appendix_a"]


def test_normalize_chapter_targets_accepts_mapping_entries():
    targets = _normalize_chapter_targets(
        [
            {
                "chapter_id": "ch7",
                "chapter_title": "Planning",
                "work_key": "target",
                "rationale": "Key chapter",
            }
        ]
    )

    assert targets is not None
    assert targets[0].chapter_id == "ch7"
    assert targets[0].chapter_title == "Planning"
    assert targets[0].work_key == "target"


def test_normalize_chapter_targets_ignores_unsupported_entries():
    targets = _normalize_chapter_targets([None, 7, ""])

    assert targets is None
