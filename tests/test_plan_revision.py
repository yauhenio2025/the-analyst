from src.orchestrator.plan_revision import apply_revision_to_plan


def test_apply_revision_to_plan_normalizes_scalar_chapter_targets():
    plan = {"phases": []}
    revision_result = {
        "revision": {"revision_type": "pre_execution", "revision_number": 1},
        "revised_phases": [
            {
                "phase_number": 1.0,
                "phase_name": "AOI",
                "chapter_targets": ["ch8", " ch9 "],
            }
        ],
    }

    updated = apply_revision_to_plan(plan, revision_result, completed_phases=set())

    assert updated["phases"][0]["chapter_targets"] == [
        {"chapter_id": "ch8"},
        {"chapter_id": "ch9"},
    ]


def test_apply_revision_to_plan_drops_mapping_chapter_targets():
    plan = {"phases": []}
    revision_result = {
        "revision": {"revision_type": "pre_execution", "revision_number": 1},
        "revised_phases": [
            {
                "phase_number": 1.0,
                "phase_name": "AOI",
                "chapter_targets": {"Target Work": ["ch8", "ch9"]},
            }
        ],
    }

    updated = apply_revision_to_plan(plan, revision_result, completed_phases=set())

    assert updated["phases"][0]["chapter_targets"] is None
