"""Presenter-owned composition law keyed by shared composition roles."""

from __future__ import annotations

from dataclasses import dataclass

from src.engines.composition_roles import COMPOSITION_ROLE_SET, CompositionRole


@dataclass(frozen=True)
class CompositionRoleSpec:
    pattern_key: str
    presentation_stance: str
    description_prefix: str
    rationale_prefix: str


COMPOSITION_ROLE_SPECS: dict[CompositionRole, CompositionRoleSpec] = {
    "synthesis_primary": CompositionRoleSpec(
        pattern_key="accordion_sections",
        presentation_stance="summary",
        description_prefix="Structured thematic synthesis",
        rationale_prefix=(
            "Matched synthesis semantics to an accordion surface for concise layered reading."
        ),
    ),
    "comparison_map": CompositionRoleSpec(
        pattern_key="card_grid_grouped",
        presentation_stance="comparison",
        description_prefix="Grouped comparison map",
        rationale_prefix=(
            "Matched comparison semantics to a grouped card grid for side-by-side scanning."
        ),
    ),
    "findings_bank": CompositionRoleSpec(
        pattern_key="accordion_sections",
        presentation_stance="evidence",
        description_prefix="Structured findings bank",
        rationale_prefix=(
            "Matched findings-bank semantics to an accordion surface to preserve grouped evidence."
        ),
    ),
    "report_closeout": CompositionRoleSpec(
        pattern_key="prose_narrative",
        presentation_stance="narrative",
        description_prefix="Narrative report closeout",
        rationale_prefix=(
            "Matched closeout semantics to prose so the report reads as a connected narrative."
        ),
    ),
    "inventory_listing": CompositionRoleSpec(
        pattern_key="card_grid_simple",
        presentation_stance="diagnostic",
        description_prefix="Inventory and listing surface",
        rationale_prefix=(
            "Matched deterministic inventory/listing semantics to a simple card grid."
        ),
    ),
}

COMPOSITION_ROLE_HINTS = frozenset(COMPOSITION_ROLE_SPECS.keys())

if COMPOSITION_ROLE_HINTS != COMPOSITION_ROLE_SET:
    raise RuntimeError(
        "composition role registry keys must match the shared CompositionRole set"
    )


def get_composition_role_spec(role: CompositionRole) -> CompositionRoleSpec:
    return COMPOSITION_ROLE_SPECS[role]
