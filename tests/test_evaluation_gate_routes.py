import asyncio

import pytest
from fastapi import HTTPException

from src.api.routes.evaluations import (
    get_evaluation_gate_decision_endpoint,
    list_evaluation_gate_decisions_endpoint,
)
from src.evaluations.gate_schemas import (
    EvaluationGateRequiredCase,
    EvaluationGateRuleTable,
    PersistedEvaluationGateDecision,
)
from src.evaluations.gate_store import save_evaluation_gate_decision


def _gate(gate_id: str, *, created_at: str) -> PersistedEvaluationGateDecision:
    return PersistedEvaluationGateDecision(
        gate_decision_id=gate_id,
        created_at=created_at,
        gate_key="bounded_platform_readiness_v1",
        gate_definition_version="v1",
        evaluation_pack_key="phase4_frozen_governance_v1",
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


def test_get_evaluation_gate_decision_endpoint_returns_gate(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path)
    gate = save_evaluation_gate_decision(
        _gate("gate-decision-route", created_at="2026-03-29T01:00:00+00:00")
    )

    fetched = asyncio.run(get_evaluation_gate_decision_endpoint(gate.gate_decision_id))

    assert fetched.gate_decision_id == gate.gate_decision_id
    assert fetched.gate_key == "bounded_platform_readiness_v1"


def test_list_evaluation_gate_decisions_endpoint_returns_filtered_summaries(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path)
    save_evaluation_gate_decision(
        _gate("gate-decision-a", created_at="2026-03-29T00:00:00+00:00")
    )
    save_evaluation_gate_decision(
        PersistedEvaluationGateDecision(
            gate_decision_id="gate-decision-b",
            created_at="2026-03-29T01:00:00+00:00",
            gate_key="other-gate",
            gate_definition_version="v1",
            evaluation_pack_key="other-pack",
            input_report_ids_by_case_key={},
            contains_live_revalidation=False,
            rule_table=EvaluationGateRuleTable(),
            overall_verdict="fail",
        )
    )

    response = asyncio.run(
        list_evaluation_gate_decisions_endpoint(
            gate_key="bounded_platform_readiness_v1",
            evaluation_pack_key="phase4_frozen_governance_v1",
            limit=10,
        )
    )

    assert response.count == 1
    assert response.gates[0].gate_decision_id == "gate-decision-a"


def test_get_evaluation_gate_decision_endpoint_returns_404_for_missing_gate(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("src.evaluations.gate_store.EVALUATION_GATES_DIR", tmp_path)

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(get_evaluation_gate_decision_endpoint("gate-decision-missing"))

    assert excinfo.value.status_code == 404
