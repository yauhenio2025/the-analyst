import pytest

from src.evaluations.gate_schemas import (
    EvaluationGateRequiredCase,
    EvaluationGateRuleTable,
    PersistedEvaluationGateDecision,
)
from src.evaluations.gate_store import (
    list_evaluation_gate_decisions,
    load_evaluation_gate_decision,
    save_evaluation_gate_decision,
)


def _gate(
    gate_id: str,
    *,
    created_at: str,
    gate_key: str = "bounded_platform_readiness_v1",
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
) -> PersistedEvaluationGateDecision:
    return PersistedEvaluationGateDecision(
        gate_decision_id=gate_id,
        created_at=created_at,
        gate_key=gate_key,
        gate_definition_version="v1",
        evaluation_pack_key=evaluation_pack_key,
        input_report_ids_by_case_key={
            "aoi_exemplar_march27_execution_backed": "evaluation-report-aoi",
        },
        contains_live_revalidation=True,
        rule_table=EvaluationGateRuleTable(
            required_cases=[
                EvaluationGateRequiredCase(
                    case_key="aoi_exemplar_march27_execution_backed",
                    required_dimensions=["selection_fit"],
                )
            ]
        ),
        overall_verdict="pass",
    )


def test_evaluation_gate_store_round_trips_and_lists_newest_first(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path)

    older = save_evaluation_gate_decision(
        _gate("gate-decision-older", created_at="2026-03-29T00:00:00+00:00")
    )
    newer = save_evaluation_gate_decision(
        _gate("gate-decision-newer", created_at="2026-03-29T01:00:00+00:00")
    )

    loaded = load_evaluation_gate_decision(older.gate_decision_id)
    summaries = list_evaluation_gate_decisions(limit=10)

    assert loaded is not None
    assert loaded.gate_decision_id == older.gate_decision_id
    assert [summary.gate_decision_id for summary in summaries] == [
        newer.gate_decision_id,
        older.gate_decision_id,
    ]


def test_evaluation_gate_store_filters_by_gate_and_pack(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path)

    save_evaluation_gate_decision(
        _gate(
            "gate-decision-a",
            created_at="2026-03-29T00:00:00+00:00",
            gate_key="bounded_platform_readiness_v1",
            evaluation_pack_key="phase4_frozen_governance_v1",
        )
    )
    save_evaluation_gate_decision(
        _gate(
            "gate-decision-b",
            created_at="2026-03-29T01:00:00+00:00",
            gate_key="other-gate",
            evaluation_pack_key="other-pack",
        )
    )

    filtered = list_evaluation_gate_decisions(
        gate_key="bounded_platform_readiness_v1",
        evaluation_pack_key="phase4_frozen_governance_v1",
        limit=10,
    )

    assert len(filtered) == 1
    assert filtered[0].gate_decision_id == "gate-decision-a"
