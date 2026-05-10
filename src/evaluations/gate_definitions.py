"""Code-defined bounded release-gate definitions."""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluations.gate_schemas import (
    EvaluationGateRequiredCase,
    EvaluationGateRuleTable,
    GateVerdictPolicy,
)


@dataclass(frozen=True)
class EvaluationGateDefinition:
    gate_key: str
    gate_definition_version: str
    evaluation_pack_key: str
    rule_table: EvaluationGateRuleTable


BOUNDED_PLATFORM_READINESS_V1 = EvaluationGateDefinition(
    gate_key="bounded_platform_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_frozen_governance_v1",
    rule_table=EvaluationGateRuleTable(
        scope_label="retrospective_frozen_pack_gate",
        required_cases=[
            EvaluationGateRequiredCase(
                case_key="aoi_exemplar_march27_execution_backed",
                required_verdict="pass",
                required_dimensions=[
                    "selection_fit",
                    "rationale_clarity",
                    "rendered_usefulness",
                    "operational_behavior",
                ],
            ),
            EvaluationGateRequiredCase(
                case_key="genealogy_lifecycle_march28_session_reopen",
                required_verdict="pass",
                required_dimensions=[
                    "identity_integrity",
                    "saved_truth_fidelity",
                    "reopen_integrity",
                    "boundary_observance",
                ],
            ),
        ],
        verdict_policy=GateVerdictPolicy(),
    ),
)


BOUNDED_GENEALOGY_LIFECYCLE_READINESS_V1 = EvaluationGateDefinition(
    gate_key="bounded_genealogy_lifecycle_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
    rule_table=EvaluationGateRuleTable(
        scope_label="retrospective_frozen_pack_gate",
        required_cases=[
            EvaluationGateRequiredCase(
                case_key="genealogy_lifecycle_march28_session_reopen",
                required_verdict="pass",
                required_dimensions=[
                    "identity_integrity",
                    "saved_truth_fidelity",
                    "reopen_integrity",
                    "boundary_observance",
                ],
            )
        ],
        verdict_policy=GateVerdictPolicy(),
    ),
)


BOUNDED_AOI_EXEMPLAR_READINESS_V1 = EvaluationGateDefinition(
    gate_key="bounded_aoi_exemplar_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
    rule_table=EvaluationGateRuleTable(
        scope_label="retrospective_frozen_pack_gate",
        required_cases=[
            EvaluationGateRequiredCase(
                case_key="aoi_exemplar_march27_execution_backed",
                required_verdict="pass",
                required_dimensions=[
                    "selection_fit",
                    "rationale_clarity",
                    "rendered_usefulness",
                    "operational_behavior",
                ],
            )
        ],
        verdict_policy=GateVerdictPolicy(),
    ),
)


BOUNDED_ROUTING_PLANNING_READINESS_V1 = EvaluationGateDefinition(
    gate_key="bounded_routing_planning_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_routing_planning_governance_v1",
    rule_table=EvaluationGateRuleTable(
        scope_label="retrospective_frozen_pack_gate",
        required_cases=[
            EvaluationGateRequiredCase(
                case_key="aoi_saved_result_handoff_current_contract",
                required_verdict="pass",
                required_dimensions=[
                    "route_fidelity",
                    "source_contract_fidelity",
                    "planning_followup_fidelity",
                    "decision_trace_integrity",
                ],
            ),
            EvaluationGateRequiredCase(
                case_key="genealogy_saved_result_direct_sections_snapshot_march28",
                required_verdict="pass",
                required_dimensions=[
                    "route_fidelity",
                    "source_contract_fidelity",
                    "planning_followup_fidelity",
                    "decision_trace_integrity",
                ],
            ),
        ],
        verdict_policy=GateVerdictPolicy(),
    ),
)


BOUNDED_PLANNER_TO_PRESENTATION_READINESS_V1 = EvaluationGateDefinition(
    gate_key="bounded_planner_to_presentation_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
    rule_table=EvaluationGateRuleTable(
        scope_label="retrospective_frozen_pack_gate",
        required_cases=[
            EvaluationGateRequiredCase(
                case_key="aoi_compose_selection_current_contract",
                required_verdict="pass",
                required_dimensions=[
                    "handoff_contract_fidelity",
                    "planner_presentation_agreement",
                    "presentation_contract_fidelity",
                    "composition_trace_integrity",
                ],
            ),
            EvaluationGateRequiredCase(
                case_key="genealogy_direct_sections_compose_snapshot_march28",
                required_verdict="pass",
                required_dimensions=[
                    "handoff_contract_fidelity",
                    "planner_presentation_agreement",
                    "presentation_contract_fidelity",
                    "composition_trace_integrity",
                ],
            ),
        ],
        verdict_policy=GateVerdictPolicy(),
    ),
)


BOUNDED_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_READINESS_V1 = EvaluationGateDefinition(
    gate_key="bounded_planner_to_presentation_cross_campaign_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
    rule_table=EvaluationGateRuleTable(
        scope_label="retrospective_frozen_pack_gate",
        required_cases=[
            EvaluationGateRequiredCase(
                case_key="aoi_compose_selection_current_contract_fresh_campaign",
                required_verdict="pass",
                required_dimensions=[
                    "handoff_contract_fidelity",
                    "planner_presentation_agreement",
                    "presentation_contract_fidelity",
                    "composition_trace_integrity",
                ],
            ),
            EvaluationGateRequiredCase(
                case_key="genealogy_direct_sections_compose_current_contract_fresh_campaign",
                required_verdict="pass",
                required_dimensions=[
                    "handoff_contract_fidelity",
                    "planner_presentation_agreement",
                    "presentation_contract_fidelity",
                    "composition_trace_integrity",
                ],
            ),
        ],
        verdict_policy=GateVerdictPolicy(),
    ),
)


_GATE_DEFINITIONS: dict[str, EvaluationGateDefinition] = {
    BOUNDED_PLATFORM_READINESS_V1.gate_key: BOUNDED_PLATFORM_READINESS_V1,
    BOUNDED_GENEALOGY_LIFECYCLE_READINESS_V1.gate_key: BOUNDED_GENEALOGY_LIFECYCLE_READINESS_V1,
    BOUNDED_AOI_EXEMPLAR_READINESS_V1.gate_key: BOUNDED_AOI_EXEMPLAR_READINESS_V1,
    BOUNDED_ROUTING_PLANNING_READINESS_V1.gate_key: BOUNDED_ROUTING_PLANNING_READINESS_V1,
    BOUNDED_PLANNER_TO_PRESENTATION_READINESS_V1.gate_key: BOUNDED_PLANNER_TO_PRESENTATION_READINESS_V1,
    BOUNDED_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_READINESS_V1.gate_key: BOUNDED_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_READINESS_V1,
}


def get_evaluation_gate_definition(gate_key: str) -> EvaluationGateDefinition:
    """Return one known gate definition."""

    try:
        return _GATE_DEFINITIONS[gate_key]
    except KeyError as exc:
        raise ValueError(f"Unknown evaluation gate: {gate_key}") from exc
