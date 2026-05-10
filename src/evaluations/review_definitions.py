"""Code-defined bounded review/disposition definitions."""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluations.schemas import EvaluationOverallVerdict


@dataclass(frozen=True)
class EvaluationReviewDefinition:
    review_key: str
    review_definition_version: str
    gate_key: str
    gate_definition_version: str
    evaluation_pack_key: str
    scope_label: str = "retrospective_frozen_pack_review"
    accept_allowed_gate_verdicts: tuple[EvaluationOverallVerdict, ...] = ("pass",)
    reject_allowed_gate_verdicts: tuple[EvaluationOverallVerdict, ...] = (
        "pass",
        "fail",
        "error",
    )
    waive_allowed_gate_verdicts: tuple[EvaluationOverallVerdict, ...] = ("fail", "error")


BOUNDED_PLATFORM_READINESS_REVIEW_V1 = EvaluationReviewDefinition(
    review_key="bounded_platform_readiness_review_v1",
    review_definition_version="v1",
    gate_key="bounded_platform_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_frozen_governance_v1",
)


BOUNDED_GENEALOGY_LIFECYCLE_REVIEW_V1 = EvaluationReviewDefinition(
    review_key="bounded_genealogy_lifecycle_review_v1",
    review_definition_version="v1",
    gate_key="bounded_genealogy_lifecycle_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
)


BOUNDED_AOI_EXEMPLAR_REVIEW_V1 = EvaluationReviewDefinition(
    review_key="bounded_aoi_exemplar_review_v1",
    review_definition_version="v1",
    gate_key="bounded_aoi_exemplar_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
)


BOUNDED_ROUTING_PLANNING_REVIEW_V1 = EvaluationReviewDefinition(
    review_key="bounded_routing_planning_review_v1",
    review_definition_version="v1",
    gate_key="bounded_routing_planning_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_routing_planning_governance_v1",
)


BOUNDED_PLANNER_TO_PRESENTATION_REVIEW_V1 = EvaluationReviewDefinition(
    review_key="bounded_planner_to_presentation_review_v1",
    review_definition_version="v1",
    gate_key="bounded_planner_to_presentation_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
)


BOUNDED_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_REVIEW_V1 = EvaluationReviewDefinition(
    review_key="bounded_planner_to_presentation_cross_campaign_review_v1",
    review_definition_version="v1",
    gate_key="bounded_planner_to_presentation_cross_campaign_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
)


_REVIEW_DEFINITIONS: dict[str, EvaluationReviewDefinition] = {
    BOUNDED_PLATFORM_READINESS_REVIEW_V1.review_key: BOUNDED_PLATFORM_READINESS_REVIEW_V1,
    BOUNDED_GENEALOGY_LIFECYCLE_REVIEW_V1.review_key: BOUNDED_GENEALOGY_LIFECYCLE_REVIEW_V1,
    BOUNDED_AOI_EXEMPLAR_REVIEW_V1.review_key: BOUNDED_AOI_EXEMPLAR_REVIEW_V1,
    BOUNDED_ROUTING_PLANNING_REVIEW_V1.review_key: BOUNDED_ROUTING_PLANNING_REVIEW_V1,
    BOUNDED_PLANNER_TO_PRESENTATION_REVIEW_V1.review_key: BOUNDED_PLANNER_TO_PRESENTATION_REVIEW_V1,
    BOUNDED_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_REVIEW_V1.review_key: BOUNDED_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_REVIEW_V1,
}


def get_evaluation_review_definition(review_key: str) -> EvaluationReviewDefinition:
    """Return one known bounded review definition."""

    try:
        return _REVIEW_DEFINITIONS[review_key]
    except KeyError as exc:
        raise ValueError(f"Unknown evaluation review definition: {review_key}") from exc
