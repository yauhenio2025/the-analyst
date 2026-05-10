from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from src.aoi.constants import AOI_WORKFLOW_KEY

from .schemas import FirstHopAffordance, ViewPayload

GENEALOGY_WORKFLOW_KEY = "intellectual_genealogy"
FIRST_HOP_ALLOWED_DESTINATIONS = ("arsenal", "research_todo")
FIRST_HOP_SPECIALIZED_FAMILY_FINDINGS_BANK_ARSENAL_PROMOTION_V1 = (
    "findings_bank_arsenal_promotion_v1"
)
AOI_FINDINGS_BANK_SPECIALIZATION_VIEW_KEY = "aoi_by_sin_type"
AOI_FINDINGS_BANK_SPECIALIZATION_ENGINE_KEY = "aoi_sin_findings"
GENEALOGY_IDEA_EVOLUTION_VIEW_KEY = "genealogy_idea_evolution"
GENEALOGY_IDEA_EVOLUTION_ENGINE_KEY = "concept_synthesis"
FIRST_HOP_AFFORDANCE_ELIGIBLE_WORKFLOW_KEYS = frozenset(
    {AOI_WORKFLOW_KEY, GENEALOGY_WORKFLOW_KEY}
)
MIGRATED_COMPOSITION_ENGINE_FAMILIES = frozenset(
    {
        "aoi_thematic_synthesis",
        "aoi_engagement_mapping",
        "aoi_sin_findings",
        "aoi_thematic_report",
        "genealogy_relationship_classification",
        "genealogy_final_synthesis",
    }
)
MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS = frozenset(
    MIGRATED_COMPOSITION_ENGINE_FAMILIES
    | {
        "genealogy_pass1b_relationship_classification",
        "genealogy_pass7_final_synthesis",
    }
)


def workflow_supports_first_hop_affordance(workflow_key: str) -> bool:
    return workflow_key in FIRST_HOP_AFFORDANCE_ELIGIBLE_WORKFLOW_KEYS


def is_migrated_analytical_leaf_payload(payload: ViewPayload) -> bool:
    return bool(
        payload.engine_key in MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS
        and not payload.children
    )


def is_genealogy_idea_evolution_first_hop_eligible_leaf(payload: ViewPayload) -> bool:
    return bool(
        payload.view_key == GENEALOGY_IDEA_EVOLUTION_VIEW_KEY
        and payload.engine_key == GENEALOGY_IDEA_EVOLUTION_ENGINE_KEY
        and not payload.children
    )


def derive_first_hop_affordance(
    payload: ViewPayload,
    *,
    enabled: bool,
) -> FirstHopAffordance | None:
    if not enabled or not (
        is_migrated_analytical_leaf_payload(payload)
        or is_genealogy_idea_evolution_first_hop_eligible_leaf(payload)
    ):
        return None
    return FirstHopAffordance(
        capturable=True,
        allowed_destinations=list(FIRST_HOP_ALLOWED_DESTINATIONS),
    )


def attach_first_hop_affordances(
    payloads: Iterable[ViewPayload],
    *,
    workflow_key: str,
) -> None:
    enabled = workflow_supports_first_hop_affordance(workflow_key)
    for payload in payloads:
        _attach_first_hop_affordances_to_payload(
            payload,
            affordance_enabled=enabled,
            workflow_key=workflow_key,
        )


def _attach_first_hop_affordances_to_payload(
    payload: ViewPayload,
    *,
    affordance_enabled: bool,
    workflow_key: str,
) -> None:
    payload.first_hop_affordance = derive_first_hop_affordance(
        payload,
        enabled=affordance_enabled,
    )
    if (
        payload.first_hop_affordance is not None
        and workflow_key == AOI_WORKFLOW_KEY
        and payload.view_key == AOI_FINDINGS_BANK_SPECIALIZATION_VIEW_KEY
        and payload.engine_key == AOI_FINDINGS_BANK_SPECIALIZATION_ENGINE_KEY
        and _payload_has_complete_findings_bank_handles(payload)
    ):
        payload.first_hop_affordance.specialized_family = (
            FIRST_HOP_SPECIALIZED_FAMILY_FINDINGS_BANK_ARSENAL_PROMOTION_V1
        )
    for child in payload.children:
        _attach_first_hop_affordances_to_payload(
            child,
            affordance_enabled=affordance_enabled,
            workflow_key=workflow_key,
        )


def _payload_has_complete_findings_bank_handles(payload: ViewPayload) -> bool:
    structured_data = payload.structured_data
    if not isinstance(structured_data, dict):
        return False

    saw_card = False
    for key, value in structured_data.items():
        if key.startswith("_"):
            continue
        if not isinstance(value, list):
            continue
        for item in value:
            if not isinstance(item, dict):
                return False
            saw_card = True
            finding_id = item.get("finding_id")
            if not isinstance(finding_id, str) or not finding_id.strip():
                return False
    return saw_card
