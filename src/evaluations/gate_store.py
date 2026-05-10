"""File-backed persistence for evaluation gate decisions."""

from __future__ import annotations

from pathlib import Path
from typing import Optional
from uuid import uuid4

from src.evaluations.gate_schemas import (
    EvaluationGateDecisionSummary,
    PersistedEvaluationGateDecision,
)


EVALUATION_GATES_DIR = Path(__file__).parent / "gates"


def build_evaluation_gate_decision_id() -> str:
    """Create one analyzer-owned evaluation gate-decision id."""

    return f"gate-decision-{uuid4().hex[:12]}"


def save_evaluation_gate_decision(
    gate_decision: PersistedEvaluationGateDecision,
) -> PersistedEvaluationGateDecision:
    """Persist one evaluation gate decision."""

    EVALUATION_GATES_DIR.mkdir(parents=True, exist_ok=True)
    gate_path = EVALUATION_GATES_DIR / f"{gate_decision.gate_decision_id}.json"
    gate_path.write_text(gate_decision.model_dump_json(indent=2), encoding="utf-8")
    return gate_decision


def load_evaluation_gate_decision(
    gate_decision_id: str,
) -> Optional[PersistedEvaluationGateDecision]:
    """Load one evaluation gate decision by id."""

    normalized_id = gate_decision_id.strip()
    if not normalized_id:
        return None
    gate_path = EVALUATION_GATES_DIR / f"{normalized_id}.json"
    if not gate_path.exists():
        return None
    return PersistedEvaluationGateDecision.model_validate_json(
        gate_path.read_text(encoding="utf-8")
    )


def list_evaluation_gate_decisions(
    *,
    gate_key: Optional[str] = None,
    evaluation_pack_key: Optional[str] = None,
    limit: int = 20,
) -> list[EvaluationGateDecisionSummary]:
    """List persisted gate-decision summaries newest-first."""

    gates: list[EvaluationGateDecisionSummary] = []
    if not EVALUATION_GATES_DIR.exists():
        return gates

    for gate_path in sorted(EVALUATION_GATES_DIR.glob("gate-decision-*.json")):
        gate_decision = PersistedEvaluationGateDecision.model_validate_json(
            gate_path.read_text(encoding="utf-8")
        )
        if gate_key and gate_decision.gate_key != gate_key:
            continue
        if evaluation_pack_key and gate_decision.evaluation_pack_key != evaluation_pack_key:
            continue
        gates.append(summarize_evaluation_gate_decision(gate_decision))

    gates.sort(key=lambda item: item.created_at, reverse=True)
    return gates[: max(limit, 0)]


def summarize_evaluation_gate_decision(
    gate_decision: PersistedEvaluationGateDecision,
) -> EvaluationGateDecisionSummary:
    """Project one persisted gate decision into a lightweight summary."""

    return EvaluationGateDecisionSummary(
        gate_decision_id=gate_decision.gate_decision_id,
        created_at=gate_decision.created_at,
        gate_key=gate_decision.gate_key,
        gate_definition_version=gate_decision.gate_definition_version,
        evaluation_pack_key=gate_decision.evaluation_pack_key,
        overall_verdict=gate_decision.overall_verdict,
        contains_live_revalidation=gate_decision.contains_live_revalidation,
    )
