"""Code-defined bounded disposition-resolution definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationDispositionResolutionDefinition:
    resolution_key: str
    resolution_definition_version: str
    review_key: str
    review_definition_version: str
    gate_key: str
    gate_definition_version: str
    evaluation_pack_key: str
    scope_label: str = "retrospective_frozen_pack_resolution"


BOUNDED_PLATFORM_READINESS_RESOLUTION_V1 = EvaluationDispositionResolutionDefinition(
    resolution_key="bounded_platform_readiness_resolution_v1",
    resolution_definition_version="v1",
    review_key="bounded_platform_readiness_review_v1",
    review_definition_version="v1",
    gate_key="bounded_platform_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_frozen_governance_v1",
)


BOUNDED_GENEALOGY_LIFECYCLE_RESOLUTION_V1 = EvaluationDispositionResolutionDefinition(
    resolution_key="bounded_genealogy_lifecycle_resolution_v1",
    resolution_definition_version="v1",
    review_key="bounded_genealogy_lifecycle_review_v1",
    review_definition_version="v1",
    gate_key="bounded_genealogy_lifecycle_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
)


BOUNDED_AOI_EXEMPLAR_RESOLUTION_V1 = EvaluationDispositionResolutionDefinition(
    resolution_key="bounded_aoi_exemplar_resolution_v1",
    resolution_definition_version="v1",
    review_key="bounded_aoi_exemplar_review_v1",
    review_definition_version="v1",
    gate_key="bounded_aoi_exemplar_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
)


BOUNDED_ROUTING_PLANNING_RESOLUTION_V1 = EvaluationDispositionResolutionDefinition(
    resolution_key="bounded_routing_planning_resolution_v1",
    resolution_definition_version="v1",
    review_key="bounded_routing_planning_review_v1",
    review_definition_version="v1",
    gate_key="bounded_routing_planning_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_routing_planning_governance_v1",
)


BOUNDED_PLANNER_TO_PRESENTATION_RESOLUTION_V1 = EvaluationDispositionResolutionDefinition(
    resolution_key="bounded_planner_to_presentation_resolution_v1",
    resolution_definition_version="v1",
    review_key="bounded_planner_to_presentation_review_v1",
    review_definition_version="v1",
    gate_key="bounded_planner_to_presentation_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
)


BOUNDED_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_RESOLUTION_V1 = EvaluationDispositionResolutionDefinition(
    resolution_key="bounded_planner_to_presentation_cross_campaign_resolution_v1",
    resolution_definition_version="v1",
    review_key="bounded_planner_to_presentation_cross_campaign_review_v1",
    review_definition_version="v1",
    gate_key="bounded_planner_to_presentation_cross_campaign_readiness_v1",
    gate_definition_version="v1",
    evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
)


_RESOLUTION_DEFINITIONS: dict[str, EvaluationDispositionResolutionDefinition] = {
    BOUNDED_PLATFORM_READINESS_RESOLUTION_V1.resolution_key: BOUNDED_PLATFORM_READINESS_RESOLUTION_V1,
    BOUNDED_GENEALOGY_LIFECYCLE_RESOLUTION_V1.resolution_key: BOUNDED_GENEALOGY_LIFECYCLE_RESOLUTION_V1,
    BOUNDED_AOI_EXEMPLAR_RESOLUTION_V1.resolution_key: BOUNDED_AOI_EXEMPLAR_RESOLUTION_V1,
    BOUNDED_ROUTING_PLANNING_RESOLUTION_V1.resolution_key: BOUNDED_ROUTING_PLANNING_RESOLUTION_V1,
    BOUNDED_PLANNER_TO_PRESENTATION_RESOLUTION_V1.resolution_key: BOUNDED_PLANNER_TO_PRESENTATION_RESOLUTION_V1,
    BOUNDED_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_RESOLUTION_V1.resolution_key: BOUNDED_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_RESOLUTION_V1,
}


def get_evaluation_disposition_resolution_definition(
    resolution_key: str,
) -> EvaluationDispositionResolutionDefinition:
    """Return one known bounded disposition-resolution definition."""

    try:
        return _RESOLUTION_DEFINITIONS[resolution_key]
    except KeyError as exc:
        raise ValueError(
            f"Unknown evaluation disposition resolution definition: {resolution_key}"
        ) from exc
