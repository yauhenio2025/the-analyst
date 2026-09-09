"""The cohort adapter reads a central two-phase method, without running a model."""
import asyncio


def test_cohort_placement_is_discoverable_and_serves_both_method_cards(monkeypatch, tmp_path):
    from src.engines import history_tracker
    monkeypatch.setattr(history_tracker, 'HISTORY_DIR', tmp_path / 'history')
    from src.api.routes.engines import get_capability_definition
    from src.api.routes.operationalizations import get_process

    key = 'cohort_school_placement'
    cap = asyncio.run(get_capability_definition(key))
    process = asyncio.run(get_process(key))
    assert cap.engine_key == process.key == key and cap.operation == 'placement'
    assert {d.key for d in cap.analytical_dimensions} == {d.key for d in process.dimensions} == {'shortlist', 'review'}
    assert all(d.method_card and d.answer_shape for d in process.dimensions)
    assert process.framing and process.final_step.is_final


def test_cohort_method_preserves_the_oeuvre_placement_scope():
    from src.operationalizations.registry import get_operationalization_registry
    registry = get_operationalization_registry()
    oeuvre = registry.get('thinker_placement').process
    cohort = registry.get('cohort_school_placement').process
    assert 'PERSONS_UNKNOWN' in oeuvre.framing
    assert [d.key for d in oeuvre.dimensions] == ['fit', 'new_school', 'verdict']
    assert [d.key for d in cohort.dimensions] == ['shortlist', 'review']
