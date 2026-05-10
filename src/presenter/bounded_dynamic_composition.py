"""Proof-only runtime composition for presentations."""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Optional

from src.aoi.constants import AOI_WORKFLOW_KEY
from src.consumers.registry import get_consumer_registry
from src.renderers.validator import validate_renderer_config, validate_renderer_data
from src.presenter.adaptive_specs.keys import (
    BUILDER_TEMPLATE_KEY_CONDITIONS_BALANCE_SHEET,
    BUILDER_TEMPLATE_KEY_CONDITIONS_PATH_DEPENDENCY_MATRIX,
    BUILDER_TEMPLATE_KEY_RELATIONSHIP_COMPARISON_REVIEW,
    BUILDER_TEMPLATE_KEY_RELATIONSHIP_PROFILE_DOSSIER,
    SIGNAL_EXTRACTOR_KEY_CONDITIONS_SURFACE_SIGNALS_V1,
    SIGNAL_EXTRACTOR_KEY_RELATIONSHIP_SURFACE_SIGNALS_V1,
)
from src.presenter.adaptive_specs.registry import (
    AdaptiveSpecRegistryError,
    get_adaptive_composition_spec,
    get_adaptive_suite_composition_spec,
)
from src.presenter.adaptive_specs.schemas import (
    AdaptiveCompositionSpec,
    AdaptiveDecisionRule,
    AdaptivePredicate,
    AdaptiveSuiteCompositionSpec,
    AdaptiveSuiteSurfaceSpec,
)

from .schemas import CompositionIssue, ViewPayload

COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1 = "bounded_dynamic_genealogy_v1"
COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1 = "adaptive_relationship_surface_v1"
COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1 = "declarative_relationship_surface_v1"
COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1 = (
    "adaptive_genealogy_relationship_conditions_v1"
)
COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1 = (
    "declarative_genealogy_relationship_conditions_suite_v1"
)
COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1 = "adaptive_aoi_theme_surface_v1"
COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1 = "adaptive_aoi_theme_report_suite_v1"
GENEALOGY_WORKFLOW_KEY = "intellectual_genealogy"
DERIVATION_KIND_GENERATED_RUNTIME_PARENT = "generated_runtime_parent"
DERIVATION_KIND_RUNTIME_SURFACE_FAMILY = "runtime_surface_family"
ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY = "genealogy_relationship_landscape"
ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY = "genealogy_conditions"
ADAPTIVE_AOI_THEME_VIEW_KEY = "aoi_by_theme"
ADAPTIVE_AOI_REPORT_VIEW_KEY = "aoi_thematic_report"
RELATIONSHIP_PROFILE_DOSSIER = "relationship_profile_dossier"
RELATIONSHIP_COMPARISON_REVIEW = "relationship_comparison_review"
RELATIONSHIP_FIELD_MAP = "relationship_field_map"
CONDITIONS_BALANCE_SHEET = "conditions_balance_sheet"
CONDITIONS_PATH_DEPENDENCY_MATRIX = "conditions_path_dependency_matrix"
AOI_THEME_DOSSIER = "aoi_theme_dossier"
AOI_THEME_COMPARISON_REVIEW = "aoi_theme_comparison_review"
AOI_REPORT_BRIEFING = "aoi_report_briefing"
AOI_REPORT_EVIDENCE_REVIEW = "aoi_report_evidence_review"
DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_ISSUE_TARGET = (
    "__suite_spec__:declarative_genealogy_relationship_conditions_suite_v1"
)
_SUPPORTED_COMPOSITION_MODES = {
    COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1,
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
}
_MODE_WORKFLOW_MAP = {
    COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1: GENEALOGY_WORKFLOW_KEY,
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1: GENEALOGY_WORKFLOW_KEY,
    COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1: GENEALOGY_WORKFLOW_KEY,
    COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1: GENEALOGY_WORKFLOW_KEY,
    COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1: GENEALOGY_WORKFLOW_KEY,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1: AOI_WORKFLOW_KEY,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1: AOI_WORKFLOW_KEY,
}
_RELATIONSHIP_TYPE_WEIGHTS = {
    "direct_precursor": 5,
    "methodological_ancestor": 4,
    "counter_position": 4,
    "conceptual_sibling": 4,
    "indirect_contextualizer": 3,
    "stylistic_influence": 2,
}
_RELATIONSHIP_STRENGTH_WEIGHTS = {
    "strong": 3,
    "moderate": 2,
    "weak": 1,
}


def get_supported_composition_modes() -> tuple[str, ...]:
    """Return the registered bounded composition modes in stable order."""

    return tuple(sorted(_SUPPORTED_COMPOSITION_MODES))


def get_supported_composition_modes_for_workflow(workflow_key: str) -> tuple[str, ...]:
    """Return registered bounded composition modes for one workflow."""

    return tuple(
        sorted(
            composition_mode
            for composition_mode, expected_workflow in _MODE_WORKFLOW_MAP.items()
            if expected_workflow == workflow_key
        )
    )


@dataclass(frozen=True)
class AdaptiveRejectedFamily:
    family: str
    reason: str


@dataclass(frozen=True)
class AdaptiveSurfaceSelection:
    target_surface: str
    selected_family: str
    signal_summary: dict[str, Any]
    rationale: str
    rejected_families: tuple[AdaptiveRejectedFamily, ...]
    ordered_cards: tuple[dict[str, Any], ...]

    def as_trace_details(self) -> dict[str, Any]:
        return {
            "target_surface": self.target_surface,
            "selected_family": self.selected_family,
            "signal_summary": self.signal_summary,
            "rejected_families": [
                {
                    "family": rejected.family,
                    "reason": rejected.reason,
                }
                for rejected in self.rejected_families
            ],
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class AdaptiveConditionsSelection:
    target_surface: str
    selected_family: str
    signal_summary: dict[str, Any]
    rationale: str
    rejected_families: tuple[AdaptiveRejectedFamily, ...]
    source_payload: dict[str, Any]

    def as_trace_details(self) -> dict[str, Any]:
        return {
            "target_surface": self.target_surface,
            "selected_family": self.selected_family,
            "signal_summary": self.signal_summary,
            "rejected_families": [
                {
                    "family": rejected.family,
                    "reason": rejected.reason,
                }
                for rejected in self.rejected_families
            ],
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class AdaptiveSurfaceSuiteSelection:
    surface_decisions: tuple[AdaptiveSurfaceSelection | AdaptiveConditionsSelection, ...]

    def as_trace_details(self) -> dict[str, Any]:
        return {
            "surface_decisions": [
                decision.as_trace_details()
                for decision in self.surface_decisions
            ]
        }


@dataclass(frozen=True)
class GroupChildSpec:
    view_key: str
    group_role: str
    group_reason: str


@dataclass(frozen=True)
class GroupSpec:
    view_key: str
    view_name: str
    position: float
    why_this_grouping: str
    children: tuple[GroupChildSpec, ...]


GENEALOGY_GROUP_SPECS: tuple[GroupSpec, ...] = (
    GroupSpec(
        view_key="dynamic_genealogy_briefing",
        view_name="Situation Map",
        position=1.0,
        why_this_grouping=(
            "This grouping establishes the target work and the relationship field "
            "before moving into development and judgment."
        ),
        children=(
            GroupChildSpec(
                view_key="genealogy_target_profile",
                group_role="Target framing",
                group_reason="Profiles the target work's internal conceptual terrain.",
            ),
            GroupChildSpec(
                view_key="genealogy_relationship_landscape",
                group_role="Relational map",
                group_reason="Maps the strongest predecessor and sibling relationships around the target.",
            ),
        ),
    ),
    GroupSpec(
        view_key="dynamic_genealogy_trajectory",
        view_name="Development Arc",
        position=2.0,
        why_this_grouping=(
            "This grouping follows how the work develops, shifts, and strategically "
            "positions itself over the course of the genealogy."
        ),
        children=(
            GroupChildSpec(
                view_key="genealogy_text_profiling",
                group_role="Text anatomy",
                group_reason="Shows the internal profile and distribution of the target text.",
            ),
            GroupChildSpec(
                view_key="genealogy_idea_evolution",
                group_role="Development line",
                group_reason="Tracks how central ideas move across predecessors and the target work.",
            ),
            GroupChildSpec(
                view_key="genealogy_tactics",
                group_role="Strategic moves",
                group_reason="Surfaces the argumentative and tactical moves that shape development.",
            ),
        ),
    ),
    GroupSpec(
        view_key="dynamic_genealogy_horizon",
        view_name="Conditions & Judgment",
        position=3.0,
        why_this_grouping=(
            "This grouping closes on the surrounding conditions and the final synthetic "
            "judgment that the genealogy supports."
        ),
        children=(
            GroupChildSpec(
                view_key="genealogy_conditions",
                group_role="Conditions field",
                group_reason="Surfaces enabling and constraining conditions around the target work.",
            ),
            GroupChildSpec(
                view_key="genealogy_portrait",
                group_role="Synthetic judgment",
                group_reason="Provides the final portrait and evaluative summary of the genealogy.",
            ),
        ),
    ),
)


class InvalidCompositionModeError(ValueError):
    """Raised when a requested composition mode is invalid for the route/workflow."""


class BoundedCompositionValidationError(ValueError):
    """Raised when proof-mode runtime composition fails validation."""

    def __init__(self, issues: list[CompositionIssue]):
        self.issues = issues
        super().__init__("bounded_dynamic_composition_validation_failed")


def list_supported_composition_modes_for_workflow(workflow_key: str) -> list[str]:
    """Return the bounded runtime composition modes supported by a workflow."""

    return [
        composition_mode
        for composition_mode, expected_workflow in _MODE_WORKFLOW_MAP.items()
        if expected_workflow == workflow_key
    ]


def validate_requested_composition_mode(
    *,
    workflow_key: str,
    composition_mode: Optional[str],
) -> None:
    """Validate an optional proof-mode composition request."""
    if not composition_mode:
        return
    if composition_mode not in _SUPPORTED_COMPOSITION_MODES:
        raise InvalidCompositionModeError("invalid_composition_mode")
    expected_workflow = _MODE_WORKFLOW_MAP.get(composition_mode)
    if expected_workflow and workflow_key != expected_workflow:
        raise InvalidCompositionModeError("invalid_composition_mode_for_workflow")


def should_apply_bounded_dynamic_composition(
    *,
    workflow_key: str,
    composition_mode: Optional[str],
) -> bool:
    validate_requested_composition_mode(
        workflow_key=workflow_key,
        composition_mode=composition_mode,
    )
    return composition_mode in _SUPPORTED_COMPOSITION_MODES


def apply_bounded_dynamic_composition(
    *,
    payloads: dict[str, ViewPayload],
    workflow_key: str,
    consumer_key: str,
    composition_mode: Optional[str],
) -> bool:
    """Apply a bounded proof-mode runtime composition against the payload map."""
    if not should_apply_bounded_dynamic_composition(
        workflow_key=workflow_key,
        composition_mode=composition_mode,
    ):
        return False

    if composition_mode == COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1:
        return _apply_adaptive_relationship_surface(
            payloads=payloads,
            consumer_key=consumer_key,
        )
    if composition_mode == COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1:
        return _apply_declarative_relationship_surface(
            payloads=payloads,
            workflow_key=workflow_key,
            consumer_key=consumer_key,
            composition_mode=composition_mode,
        )
    if composition_mode == COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1:
        return _apply_declarative_relationship_conditions_suite(
            payloads=payloads,
            workflow_key=workflow_key,
            consumer_key=consumer_key,
            composition_mode=composition_mode,
        )
    if composition_mode == COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1:
        return _apply_adaptive_aoi_theme_surface(
            payloads=payloads,
            consumer_key=consumer_key,
        )
    if composition_mode == COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1:
        return _apply_adaptive_aoi_theme_report_suite(
            payloads=payloads,
            consumer_key=consumer_key,
        )
    if composition_mode == COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1:
        return _apply_adaptive_relationship_conditions_suite(
            payloads=payloads,
            consumer_key=consumer_key,
        )

    return _apply_generated_parent_genealogy_composition(
        payloads=payloads,
        consumer_key=consumer_key,
    )


def get_runtime_composition_stage_name(composition_mode: Optional[str]) -> str:
    """Return the trace-stage name for a composition mode."""
    if composition_mode in {
        COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
        COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
    }:
        return "adaptive_surface_suite_selection"
    if composition_mode in {
        COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
        COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
        COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
    }:
        return "adaptive_surface_selection"
    return "bounded_dynamic_composition"


def inspect_runtime_composition(
    *,
    payloads: dict[str, ViewPayload],
    workflow_key: str,
    composition_mode: Optional[str],
) -> Optional[dict[str, Any]]:
    """Return inspectable diagnostics for a requested runtime composition."""
    validate_requested_composition_mode(
        workflow_key=workflow_key,
        composition_mode=composition_mode,
    )
    if composition_mode == COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1:
        selection = _select_adaptive_relationship_conditions_suite(payloads)
        return selection.as_trace_details()
    if composition_mode == COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1:
        selection = _select_declarative_relationship_conditions_suite(
            payloads=payloads,
            workflow_key=workflow_key,
            composition_mode=composition_mode,
        )
        return selection.as_trace_details()
    if composition_mode == COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1:
        selection = _select_adaptive_aoi_theme_report_suite(payloads)
        return selection.as_trace_details()
    if composition_mode == COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1:
        selection = _select_adaptive_aoi_theme_surface(payloads)
        return selection.as_trace_details()
    if composition_mode == COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1:
        selection = _select_declarative_relationship_surface(
            payloads=payloads,
            workflow_key=workflow_key,
            composition_mode=composition_mode,
        )
        return selection.as_trace_details()
    if composition_mode != COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1:
        return None
    selection = _select_adaptive_relationship_surface(payloads)
    return selection.as_trace_details()


def inspect_runtime_composition_on_payload_copy(
    *,
    payloads: dict[str, ViewPayload],
    workflow_key: str,
    consumer_key: str,
    composition_mode: str,
) -> tuple[bool, Optional[dict[str, Any]], list[CompositionIssue]]:
    """Evaluate one runtime composition mode against a copied payload map.

    The readiness route uses this helper so inspection never mutates the shared
    payload map built by presenter payload preparation.
    """

    payload_copy: dict[str, ViewPayload] = {
        key: payload.model_copy(deep=True) if isinstance(payload, ViewPayload) else deepcopy(payload)
        for key, payload in payloads.items()
    }
    try:
        composition_applied = apply_bounded_dynamic_composition(
            payloads=payload_copy,
            workflow_key=workflow_key,
            consumer_key=consumer_key,
            composition_mode=composition_mode,
        )
        inspection_details = inspect_runtime_composition(
            payloads=payload_copy,
            workflow_key=workflow_key,
            composition_mode=composition_mode,
        )
        return composition_applied, inspection_details, []
    except BoundedCompositionValidationError as error:
        return False, None, list(error.issues)


def _apply_generated_parent_genealogy_composition(
    *,
    payloads: dict[str, ViewPayload],
    consumer_key: str,
) -> bool:
    issues: list[CompositionIssue] = []
    child_payloads_by_parent: dict[str, list[tuple[GroupChildSpec, ViewPayload]]] = {}

    for group in GENEALOGY_GROUP_SPECS:
        child_payloads: list[tuple[GroupChildSpec, ViewPayload]] = []
        for child_spec in group.children:
            child_payload = payloads.get(child_spec.view_key)
            if child_payload is None:
                issues.append(
                    CompositionIssue(
                        view_key=group.view_key,
                        field="children",
                        message=f"Missing required grouped view: {child_spec.view_key}",
                        reason="missing_group_child",
                    )
                )
                continue
            child_payloads.append((child_spec, child_payload))
        child_payloads_by_parent[group.view_key] = child_payloads

    if issues:
        raise BoundedCompositionValidationError(issues)

    generated_parents: dict[str, ViewPayload] = {}
    parent_assignments: list[tuple[ViewPayload, str]] = []

    for group in GENEALOGY_GROUP_SPECS:
        grouped_specs = child_payloads_by_parent[group.view_key]
        grouped_children = [child_payload for _child_spec, child_payload in grouped_specs]
        payload = ViewPayload(
            view_key=group.view_key,
            view_name=group.view_name,
            description="",
            renderer_type="accordion",
            renderer_config={
                "sections": [
                    {"key": "why_this_grouping", "title": "Why This Grouping"},
                    {"key": "included_views", "title": "Included Views"},
                ],
                "section_renderers": {
                    "why_this_grouping": {
                        "renderer_type": "prose_block",
                        "config": {},
                    },
                    "included_views": {
                        "renderer_type": "mini_card_list",
                        "config": {
                            "title_field": "view_name",
                            "subtitle_field": "group_role",
                            "description_field": "group_reason",
                        },
                    },
                },
            },
            presentation_stance="diagnostic",
            priority="primary",
            rationale="Runtime proof grouping for bounded dynamic composition.",
            data_quality="rich",
            source_parent_view_key=None,
            phase_number=None,
            engine_key=None,
            chain_key=None,
            scope="aggregated",
            has_structured_data=True,
            structured_data={
                "why_this_grouping": group.why_this_grouping,
                "included_views": [
                    {
                        "view_key": child.view_key,
                        "view_name": child.view_name,
                        "group_role": child_spec.group_role,
                        "group_reason": child_spec.group_reason,
                    }
                    for child_spec, child in grouped_specs
                ],
            },
            reading_scaffold=None,
            raw_prose=None,
            prose_ref_view_key=None,
            items=None,
            tab_count=len(grouped_children),
            visibility="if_data_exists",
            position=group.position,
            children=[],
        )
        payload.selection_priority = "primary"
        payload.navigation_state = "normal"
        payload.derivation_kind = DERIVATION_KIND_GENERATED_RUNTIME_PARENT
        issues.extend(_validate_runtime_payload(payload, consumer_key=consumer_key))
        generated_parents[group.view_key] = payload
        parent_assignments.extend(
            (child_payload, group.view_key)
            for _child_spec, child_payload in grouped_specs
        )

    if issues:
        raise BoundedCompositionValidationError(issues)

    for child_payload, parent_view_key in parent_assignments:
        child_payload.source_parent_view_key = parent_view_key
    payloads.update(generated_parents)

    return True


def _apply_adaptive_relationship_surface(
    *,
    payloads: dict[str, ViewPayload],
    consumer_key: str,
) -> bool:
    selection = _select_adaptive_relationship_surface(payloads)
    base_payload = payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY]
    adaptive_payload = _build_relationship_surface_payload(
        base_payload=base_payload,
        selection=selection,
        builder_template_key=selection.selected_family,
    )

    issues = _validate_runtime_payload(adaptive_payload, consumer_key=consumer_key)
    if issues:
        raise BoundedCompositionValidationError(issues)

    payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY] = adaptive_payload
    return True


def _apply_declarative_relationship_surface(
    *,
    payloads: dict[str, ViewPayload],
    workflow_key: str,
    consumer_key: str,
    composition_mode: str,
) -> bool:
    selection = _select_declarative_relationship_surface(
        payloads=payloads,
        workflow_key=workflow_key,
        composition_mode=composition_mode,
    )
    spec = _load_adaptive_spec_or_raise_validation(
        composition_mode=composition_mode,
        workflow_key=workflow_key,
        issue_target=ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )
    family_spec = _family_spec_by_key(spec)[selection.selected_family]
    base_payload = payloads[spec.target_surface]
    adaptive_payload = _build_relationship_surface_payload(
        base_payload=base_payload,
        selection=selection,
        builder_template_key=family_spec.builder_template_key,
    )
    adaptive_payload.view_name = family_spec.view_name

    issues = _validate_runtime_payload(adaptive_payload, consumer_key=consumer_key)
    if issues:
        raise BoundedCompositionValidationError(issues)

    payloads[spec.target_surface] = adaptive_payload
    return True


def _apply_declarative_relationship_conditions_suite(
    *,
    payloads: dict[str, ViewPayload],
    workflow_key: str,
    consumer_key: str,
    composition_mode: str,
) -> bool:
    selection = _select_declarative_relationship_conditions_suite(
        payloads=payloads,
        workflow_key=workflow_key,
        composition_mode=composition_mode,
    )
    spec = _load_adaptive_suite_spec_or_raise_validation(
        composition_mode=composition_mode,
        workflow_key=workflow_key,
    )
    relationship_spec = _suite_surface_spec_by_target(
        spec,
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )
    conditions_spec = _suite_surface_spec_by_target(
        spec,
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
    )
    relationship_selection = selection.surface_decisions[0]
    conditions_selection = selection.surface_decisions[1]
    relationship_family_spec = _family_spec_by_key(relationship_spec)[relationship_selection.selected_family]
    conditions_family_spec = _family_spec_by_key(conditions_spec)[conditions_selection.selected_family]

    relationship_payload = payloads[relationship_spec.target_surface]
    adapted_relationship_payload = _build_relationship_surface_payload(
        base_payload=relationship_payload,
        selection=relationship_selection,
        builder_template_key=relationship_family_spec.builder_template_key,
    )
    adapted_relationship_payload.view_name = relationship_family_spec.view_name

    conditions_payload = payloads[conditions_spec.target_surface]
    adapted_conditions_payload = _build_conditions_surface_payload(
        base_payload=conditions_payload,
        selection=conditions_selection,
        builder_template_key=conditions_family_spec.builder_template_key,
    )
    adapted_conditions_payload.view_name = conditions_family_spec.view_name

    issues: list[CompositionIssue] = []
    issues.extend(_validate_runtime_payload(adapted_relationship_payload, consumer_key=consumer_key))
    issues.extend(_validate_runtime_payload(adapted_conditions_payload, consumer_key=consumer_key))
    if issues:
        raise BoundedCompositionValidationError(issues)

    payloads[relationship_spec.target_surface] = adapted_relationship_payload
    payloads[conditions_spec.target_surface] = adapted_conditions_payload
    return True


def _apply_adaptive_relationship_conditions_suite(
    *,
    payloads: dict[str, ViewPayload],
    consumer_key: str,
) -> bool:
    relationship_selection = _select_adaptive_relationship_surface(payloads)
    conditions_selection = _select_adaptive_conditions_surface(payloads)

    relationship_payload = payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY]
    if relationship_selection.selected_family == RELATIONSHIP_PROFILE_DOSSIER:
        adapted_relationship_payload = _build_relationship_profile_dossier_payload(
            base_payload=relationship_payload,
            selection=relationship_selection,
        )
    elif relationship_selection.selected_family == RELATIONSHIP_FIELD_MAP:
        adapted_relationship_payload = _build_relationship_field_map_payload(
            base_payload=relationship_payload,
            selection=relationship_selection,
        )
    else:
        adapted_relationship_payload = _build_relationship_comparison_review_payload(
            base_payload=relationship_payload,
            selection=relationship_selection,
        )

    conditions_payload = payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY]
    if conditions_selection.selected_family == CONDITIONS_PATH_DEPENDENCY_MATRIX:
        adapted_conditions_payload = _build_conditions_path_dependency_matrix_payload(
            base_payload=conditions_payload,
            selection=conditions_selection,
        )
    else:
        adapted_conditions_payload = _build_conditions_balance_sheet_payload(
            base_payload=conditions_payload,
            selection=conditions_selection,
        )

    issues: list[CompositionIssue] = []
    issues.extend(_validate_runtime_payload(adapted_relationship_payload, consumer_key=consumer_key))
    issues.extend(_validate_runtime_payload(adapted_conditions_payload, consumer_key=consumer_key))
    if issues:
        raise BoundedCompositionValidationError(issues)

    payloads[ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY] = adapted_relationship_payload
    payloads[ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY] = adapted_conditions_payload
    return True


def _apply_adaptive_aoi_theme_surface(
    *,
    payloads: dict[str, ViewPayload],
    consumer_key: str,
) -> bool:
    selection = _select_adaptive_aoi_theme_surface(payloads)
    base_payload = payloads[ADAPTIVE_AOI_THEME_VIEW_KEY]

    if selection.selected_family == AOI_THEME_DOSSIER:
        adaptive_payload = _build_aoi_theme_dossier_payload(
            base_payload=base_payload,
            selection=selection,
        )
    else:
        adaptive_payload = _build_aoi_theme_comparison_review_payload(
            base_payload=base_payload,
            selection=selection,
        )

    issues = _validate_runtime_payload(adaptive_payload, consumer_key=consumer_key)
    if issues:
        raise BoundedCompositionValidationError(issues)

    payloads[ADAPTIVE_AOI_THEME_VIEW_KEY] = adaptive_payload
    return True


def _apply_adaptive_aoi_theme_report_suite(
    *,
    payloads: dict[str, ViewPayload],
    consumer_key: str,
) -> bool:
    theme_selection = _select_adaptive_aoi_theme_surface(payloads)
    report_selection = _select_adaptive_aoi_report_surface(payloads)

    theme_payload = payloads[ADAPTIVE_AOI_THEME_VIEW_KEY]
    if theme_selection.selected_family == AOI_THEME_DOSSIER:
        adapted_theme_payload = _build_aoi_theme_dossier_payload(
            base_payload=theme_payload,
            selection=theme_selection,
        )
    else:
        adapted_theme_payload = _build_aoi_theme_comparison_review_payload(
            base_payload=theme_payload,
            selection=theme_selection,
        )

    report_payload = payloads[ADAPTIVE_AOI_REPORT_VIEW_KEY]
    if report_selection.selected_family == AOI_REPORT_EVIDENCE_REVIEW:
        adapted_report_payload = _build_aoi_report_evidence_review_payload(
            base_payload=report_payload,
            selection=report_selection,
        )
    else:
        adapted_report_payload = _build_aoi_report_briefing_payload(
            base_payload=report_payload,
            selection=report_selection,
        )

    issues: list[CompositionIssue] = []
    issues.extend(_validate_runtime_payload(adapted_theme_payload, consumer_key=consumer_key))
    issues.extend(_validate_runtime_payload(adapted_report_payload, consumer_key=consumer_key))
    if issues:
        raise BoundedCompositionValidationError(issues)

    payloads[ADAPTIVE_AOI_THEME_VIEW_KEY] = adapted_theme_payload
    payloads[ADAPTIVE_AOI_REPORT_VIEW_KEY] = adapted_report_payload
    return True


def _select_adaptive_relationship_surface(
    payloads: dict[str, ViewPayload],
) -> AdaptiveSurfaceSelection:
    payload = _resolve_relationship_target_payload(
        payloads=payloads,
        view_key=ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )
    ranked_cards, signal_summary = _extract_relationship_surface_signals(payload)
    family = _choose_relationship_surface_family_key(signal_summary)
    return _hydrate_relationship_surface_selection(
        payload=payload,
        selected_family=family,
        ranked_cards=ranked_cards,
        signal_summary=signal_summary,
    )


def _select_declarative_relationship_surface(
    *,
    payloads: dict[str, ViewPayload],
    workflow_key: str,
    composition_mode: str,
) -> AdaptiveSurfaceSelection:
    spec = _load_adaptive_spec_or_raise_validation(
        composition_mode=composition_mode,
        workflow_key=workflow_key,
        issue_target=ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )
    payload = _resolve_relationship_target_payload(
        payloads=payloads,
        view_key=spec.target_surface,
    )
    ranked_cards, signal_summary = _run_declarative_signal_extractor(
        signal_extractor_key=spec.signal_extractor_key,
        payload=payload,
    )
    selected_family = _select_declarative_relationship_surface_family(
        spec=spec,
        signal_summary=signal_summary,
        issue_target=spec.target_surface,
    )
    return _hydrate_relationship_surface_selection(
        payload=payload,
        selected_family=selected_family,
        ranked_cards=ranked_cards,
        signal_summary=signal_summary,
        declared_families={family.family_key for family in spec.families},
    )


def _select_declarative_relationship_conditions_suite(
    *,
    payloads: dict[str, ViewPayload],
    workflow_key: str,
    composition_mode: str,
) -> AdaptiveSurfaceSuiteSelection:
    spec = _load_adaptive_suite_spec_or_raise_validation(
        composition_mode=composition_mode,
        workflow_key=workflow_key,
    )
    relationship_spec = _suite_surface_spec_by_target(
        spec,
        ADAPTIVE_RELATIONSHIP_SURFACE_VIEW_KEY,
    )
    conditions_spec = _suite_surface_spec_by_target(
        spec,
        ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
    )

    relationship_payload = _resolve_relationship_target_payload(
        payloads=payloads,
        view_key=relationship_spec.target_surface,
    )
    ranked_cards, relationship_signal_summary = _run_declarative_signal_extractor(
        signal_extractor_key=relationship_spec.signal_extractor_key,
        payload=relationship_payload,
    )
    relationship_selection = _hydrate_relationship_surface_selection(
        payload=relationship_payload,
        selected_family=_select_declarative_relationship_surface_family(
            spec=relationship_spec,
            signal_summary=relationship_signal_summary,
            issue_target=relationship_spec.target_surface,
        ),
        ranked_cards=ranked_cards,
        signal_summary=relationship_signal_summary,
        declared_families={family.family_key for family in relationship_spec.families},
    )

    conditions_payload = _resolve_adaptive_target_payload(
        payloads=payloads,
        view_key=conditions_spec.target_surface,
    )
    conditions_source_payload, conditions_signal_summary = _run_declarative_signal_extractor(
        signal_extractor_key=conditions_spec.signal_extractor_key,
        payload=conditions_payload,
    )
    conditions_selection = _hydrate_conditions_surface_selection(
        payload=conditions_payload,
        selected_family=_select_declarative_relationship_surface_family(
            spec=conditions_spec,
            signal_summary=conditions_signal_summary,
            issue_target=conditions_spec.target_surface,
        ),
        signal_summary=conditions_signal_summary,
        source_payload=conditions_source_payload,
        declared_families={family.family_key for family in conditions_spec.families},
    )

    return AdaptiveSurfaceSuiteSelection(
        surface_decisions=(
            relationship_selection,
            conditions_selection,
        )
    )


def _resolve_relationship_target_payload(
    *,
    payloads: dict[str, ViewPayload],
    view_key: str,
) -> ViewPayload:
    return _resolve_adaptive_target_payload(
        payloads=payloads,
        view_key=view_key,
    )


def _resolve_adaptive_target_payload(
    *,
    payloads: dict[str, ViewPayload],
    view_key: str,
) -> ViewPayload:
    payload = payloads.get(view_key)
    if payload is None:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=view_key,
                    field="view_key",
                    message=f"Missing adaptive target surface: {view_key}",
                    reason="missing_adaptive_target_surface",
                )
            ]
        )
    return payload


def _extract_relationship_surface_signals(
    payload: ViewPayload,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cards = _extract_relationship_cards(payload)
    if not cards:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=payload.view_key,
                    field="items",
                    message="Adaptive relationship surface requires structured per-item relationship cards.",
                    reason="adaptive_surface_missing_structured_items",
                )
            ]
        )

    ranked_cards = sorted(
        (_decorate_relationship_card(card) for card in cards),
        key=lambda card: (-int(card["_adaptive_score"]), str(card.get("work_title") or "")),
    )
    score_total = sum(int(card["_adaptive_score"]) for card in ranked_cards)
    top_score = int(ranked_cards[0]["_adaptive_score"])
    second_score = int(ranked_cards[1]["_adaptive_score"]) if len(ranked_cards) > 1 else 0
    top_share = round(top_score / score_total, 2) if score_total else 1.0
    relationship_types = Counter(str(card.get("relationship_type") or "unknown") for card in ranked_cards)
    strengths = Counter(str(card.get("relationship_strength") or "unknown") for card in ranked_cards)

    signal_summary = {
        "relationship_count": len(ranked_cards),
        "distinct_relationship_types": len(relationship_types),
        "relationship_type_counts": dict(sorted(relationship_types.items())),
        "strength_counts": dict(sorted(strengths.items())),
        "dominant_work_title": ranked_cards[0].get("work_title") or "",
        "dominant_relationship_type": ranked_cards[0].get("relationship_type") or "",
        "top_score": top_score,
        "second_score": second_score,
        "score_gap": top_score - second_score,
        "top_share": top_share,
    }
    return ranked_cards, signal_summary


def _choose_relationship_surface_family_key(signal_summary: dict[str, Any]) -> str:
    relationship_count = int(signal_summary["relationship_count"])
    distinct_types = int(signal_summary["distinct_relationship_types"])
    top_share = float(signal_summary["top_share"])
    score_gap = int(signal_summary["score_gap"])

    dominant_relationship = relationship_count == 1 or (top_share >= 0.45 and score_gap >= 5)
    diffuse_field = (
        relationship_count >= 5
        or (relationship_count >= 4 and top_share < 0.5)
        or (relationship_count >= 4 and distinct_types >= 3)
    )

    if dominant_relationship:
        return RELATIONSHIP_PROFILE_DOSSIER
    if diffuse_field:
        return RELATIONSHIP_FIELD_MAP
    return RELATIONSHIP_COMPARISON_REVIEW


def _hydrate_relationship_surface_selection(
    *,
    payload: ViewPayload,
    selected_family: str,
    ranked_cards: list[dict[str, Any]],
    signal_summary: dict[str, Any],
    declared_families: Optional[set[str]] = None,
) -> AdaptiveSurfaceSelection:
    relationship_count = int(signal_summary["relationship_count"])
    distinct_types = int(signal_summary["distinct_relationship_types"])
    dominant_work = str(signal_summary["dominant_work_title"] or "The leading work")
    top_share = float(signal_summary["top_share"])
    score_gap = int(signal_summary["score_gap"])

    if selected_family == RELATIONSHIP_PROFILE_DOSSIER:
        rationale = (
            f"{dominant_work} clearly dominates the relationship field "
            f"({round(top_share * 100)}% of weighted relationship strength, "
            f"{score_gap} points ahead of the next work), so a single-work dossier is the clearest surface."
        )
        rejected = (
            AdaptiveRejectedFamily(
                family=RELATIONSHIP_COMPARISON_REVIEW,
                reason="No side-by-side cluster is close enough to displace the dominant relationship.",
            ),
            AdaptiveRejectedFamily(
                family=RELATIONSHIP_FIELD_MAP,
                reason="The field is not diffuse enough to justify a distributed relationship map.",
            ),
        )
    elif selected_family == RELATIONSHIP_FIELD_MAP:
        rationale = (
            f"The field spreads across {relationship_count} relationships and {distinct_types} relationship types "
            f"with no single dominant precursor (top share {round(top_share * 100)}%), so a field map is the "
            f"most legible family."
        )
        rejected = (
            AdaptiveRejectedFamily(
                family=RELATIONSHIP_PROFILE_DOSSIER,
                reason="No single relationship dominates strongly enough to sustain a dossier surface.",
            ),
            AdaptiveRejectedFamily(
                family=RELATIONSHIP_COMPARISON_REVIEW,
                reason="The field is too crowded or heterogeneous for a bounded side-by-side review.",
            ),
        )
    else:
        comparable_titles = ", ".join(
            str(card.get("work_title") or "")
            for card in ranked_cards[: min(3, len(ranked_cards))]
        )
        rationale = (
            f"Several relationships remain materially comparable ({comparable_titles}), so a comparison review "
            f"fits better than a single dominant dossier or a broad field map."
        )
        rejected = (
            AdaptiveRejectedFamily(
                family=RELATIONSHIP_PROFILE_DOSSIER,
                reason="The top relationship does not separate cleanly enough from the next tier.",
            ),
            AdaptiveRejectedFamily(
                family=RELATIONSHIP_FIELD_MAP,
                reason="The field is not large or diffuse enough to warrant a full relationship map.",
            ),
        )

    if declared_families is not None:
        rejected = tuple(item for item in rejected if item.family in declared_families)

    return AdaptiveSurfaceSelection(
        target_surface=payload.view_key,
        selected_family=selected_family,
        signal_summary=signal_summary,
        rationale=rationale,
        rejected_families=rejected,
        ordered_cards=tuple(ranked_cards),
    )


def _load_adaptive_spec_or_raise_validation(
    *,
    composition_mode: str,
    workflow_key: str,
    issue_target: str,
) -> AdaptiveCompositionSpec:
    try:
        spec = get_adaptive_composition_spec(composition_mode)
    except AdaptiveSpecRegistryError as exc:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=issue_target,
                    field="composition_mode",
                    message=str(exc),
                    reason="adaptive_spec_validation_failed",
                )
            ]
        ) from exc

    expected_workflow = _MODE_WORKFLOW_MAP.get(composition_mode)
    if expected_workflow and spec.workflow_key != expected_workflow:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=spec.target_surface,
                    field="workflow_key",
                    message=(
                        f"Adaptive composition spec workflow '{spec.workflow_key}' does not match "
                        f"mode workflow '{expected_workflow}'."
                    ),
                    reason="adaptive_spec_workflow_mismatch",
                )
            ]
        )
    if workflow_key != spec.workflow_key:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=spec.target_surface,
                    field="workflow_key",
                    message=(
                        f"Adaptive composition spec workflow '{spec.workflow_key}' does not match "
                        f"requested workflow '{workflow_key}'."
                    ),
                    reason="adaptive_spec_workflow_mismatch",
                )
            ]
        )
    return spec


def _load_adaptive_suite_spec_or_raise_validation(
    *,
    composition_mode: str,
    workflow_key: str,
) -> AdaptiveSuiteCompositionSpec:
    issue_target = DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_ISSUE_TARGET
    try:
        spec = get_adaptive_suite_composition_spec(composition_mode)
    except AdaptiveSpecRegistryError as exc:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=issue_target,
                    field="composition_mode",
                    message=str(exc),
                    reason="adaptive_spec_validation_failed",
                )
            ]
        ) from exc

    expected_workflow = _MODE_WORKFLOW_MAP.get(composition_mode)
    if expected_workflow and spec.workflow_key != expected_workflow:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=issue_target,
                    field="workflow_key",
                    message=(
                        f"Adaptive composition spec workflow '{spec.workflow_key}' does not match "
                        f"mode workflow '{expected_workflow}'."
                    ),
                    reason="adaptive_spec_workflow_mismatch",
                )
            ]
        )
    if workflow_key != spec.workflow_key:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=issue_target,
                    field="workflow_key",
                    message=(
                        f"Adaptive composition spec workflow '{spec.workflow_key}' does not match "
                        f"requested workflow '{workflow_key}'."
                    ),
                    reason="adaptive_spec_workflow_mismatch",
                )
            ]
        )
    return spec


def _run_declarative_signal_extractor(
    *,
    signal_extractor_key: str,
    payload: ViewPayload,
) -> tuple[Any, dict[str, Any]]:
    extractor = _declarative_signal_extractors().get(signal_extractor_key)
    if extractor is None:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=payload.view_key,
                    field="signal_extractor_key",
                    message=f"Unknown declarative signal extractor: {signal_extractor_key}",
                    reason="adaptive_spec_unknown_signal_extractor",
                )
            ]
        )
    return extractor(payload)


def _select_declarative_relationship_surface_family(
    *,
    spec: AdaptiveCompositionSpec | AdaptiveSuiteSurfaceSpec,
    signal_summary: dict[str, Any],
    issue_target: str,
) -> str:
    for rule in spec.decision_rules:
        if _decision_rule_matches(rule, signal_summary, issue_target=issue_target):
            return rule.family_key
    return spec.default_family


def _decision_rule_matches(
    rule: AdaptiveDecisionRule,
    signal_summary: dict[str, Any],
    *,
    issue_target: str,
) -> bool:
    if not rule.match_any:
        return False
    return any(
        all(
            _predicate_matches(predicate, signal_summary, issue_target=issue_target)
            for predicate in predicate_group
        )
        for predicate_group in rule.match_any
    )


def _predicate_matches(
    predicate: AdaptivePredicate,
    signal_summary: dict[str, Any],
    *,
    issue_target: str,
) -> bool:
    metric_value = signal_summary.get(predicate.metric)
    if metric_value is None:
        return False
    if predicate.operator == "eq":
        return metric_value == predicate.value
    if predicate.operator == "gte":
        return metric_value >= predicate.value
    raise BoundedCompositionValidationError(
        [
            CompositionIssue(
                view_key=issue_target,
                field="operator",
                message=f"Unsupported adaptive predicate operator: {predicate.operator}",
                reason="adaptive_spec_invalid_operator",
            )
        ]
    )


def _family_spec_by_key(
    spec: AdaptiveCompositionSpec | AdaptiveSuiteSurfaceSpec,
) -> dict[str, Any]:
    return {family.family_key: family for family in spec.families}


def _suite_surface_spec_by_target(
    spec: AdaptiveSuiteCompositionSpec,
    target_surface: str,
) -> AdaptiveSuiteSurfaceSpec:
    for surface_spec in spec.surfaces:
        if surface_spec.target_surface == target_surface:
            return surface_spec
    raise BoundedCompositionValidationError(
        [
            CompositionIssue(
                view_key=DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_ISSUE_TARGET,
                field="surfaces",
                message=f"Adaptive suite spec is missing required target surface: {target_surface}",
                reason="adaptive_spec_validation_failed",
            )
        ]
    )


def _select_adaptive_relationship_conditions_suite(
    payloads: dict[str, ViewPayload],
) -> AdaptiveSurfaceSuiteSelection:
    return AdaptiveSurfaceSuiteSelection(
        surface_decisions=(
            _select_adaptive_relationship_surface(payloads),
            _select_adaptive_conditions_surface(payloads),
        )
    )


def _select_adaptive_aoi_theme_report_suite(
    payloads: dict[str, ViewPayload],
) -> AdaptiveSurfaceSuiteSelection:
    return AdaptiveSurfaceSuiteSelection(
        surface_decisions=(
            _select_adaptive_aoi_theme_surface(payloads),
            _select_adaptive_aoi_report_surface(payloads),
        )
    )


def _select_adaptive_conditions_surface(
    payloads: dict[str, ViewPayload],
) -> AdaptiveConditionsSelection:
    payload = _resolve_adaptive_target_payload(
        payloads=payloads,
        view_key=ADAPTIVE_CONDITIONS_SURFACE_VIEW_KEY,
    )
    source_payload, signal_summary = _extract_conditions_surface_signals(payload)
    return _hydrate_conditions_surface_selection(
        payload=payload,
        selected_family=_choose_conditions_surface_family_key(signal_summary),
        signal_summary=signal_summary,
        source_payload=source_payload,
    )


def _select_adaptive_aoi_theme_surface(
    payloads: dict[str, ViewPayload],
) -> AdaptiveSurfaceSelection:
    payload = payloads.get(ADAPTIVE_AOI_THEME_VIEW_KEY)
    if payload is None:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=ADAPTIVE_AOI_THEME_VIEW_KEY,
                    field="view_key",
                    message="Missing adaptive target surface: aoi_by_theme",
                    reason="missing_adaptive_target_surface",
                )
            ]
        )

    source_payload = _extract_aoi_theme_source_payload(payload)
    raw_section_order = source_payload.get("_section_order")
    if not isinstance(raw_section_order, list) or not raw_section_order:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=payload.view_key,
                    field="_section_order",
                    message="Adaptive AOI theme surface requires a non-empty _section_order.",
                    reason="adaptive_surface_missing_section_order",
                )
            ]
        )
    section_order = [str(theme_id) for theme_id in raw_section_order]

    raw_titles = source_payload.get("_section_titles")
    if not isinstance(raw_titles, dict):
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=payload.view_key,
                    field="_section_titles",
                    message="Adaptive AOI theme surface requires a _section_titles mapping.",
                    reason="adaptive_surface_missing_section_titles",
                )
            ]
        )

    theme_metrics: list[dict[str, Any]] = []
    for theme_id in section_order:
        theme_name = str(raw_titles.get(theme_id) or "").strip()
        if not theme_name:
            raise BoundedCompositionValidationError(
                [
                    CompositionIssue(
                        view_key=payload.view_key,
                        field=f"_section_titles.{theme_id}",
                        message=f"Adaptive AOI theme surface requires a title for theme '{theme_id}'.",
                        reason="adaptive_surface_missing_theme_title",
                    )
                ]
            )
        theme_payload = source_payload.get(theme_id)
        if not isinstance(theme_payload, dict):
            raise BoundedCompositionValidationError(
                [
                    CompositionIssue(
                        view_key=payload.view_key,
                        field=theme_id,
                        message=f"Adaptive AOI theme surface requires structured data for theme '{theme_id}'.",
                        reason="adaptive_surface_missing_theme_payload",
                    )
                ]
            )

        findings = _coerce_runtime_list(theme_payload.get("findings"))
        source_documents = _coerce_runtime_string_list(theme_payload.get("source_documents"))
        key_claims = _coerce_runtime_list(theme_payload.get("key_claims"))
        sin_type_counter = Counter(
            str(item.get("sin_type_label") or "").strip()
            for item in findings
            if str(item.get("sin_type_label") or "").strip()
        )
        dominant_sin_type = (
            sorted(sin_type_counter.items(), key=lambda item: (-item[1], item[0]))[0][0]
            if sin_type_counter
            else "—"
        )

        theme_metrics.append(
            {
                "theme_id": theme_id,
                "theme_name": theme_name,
                "overview": str(theme_payload.get("overview") or ""),
                "engagement": str(theme_payload.get("engagement") or ""),
                "key_claims": key_claims,
                "philosophical_commitments": _coerce_runtime_list(theme_payload.get("philosophical_commitments")),
                "argumentative_moves": _coerce_runtime_list(theme_payload.get("argumentative_moves")),
                "source_documents": source_documents,
                "findings": findings,
                "finding_count": len(findings),
                "source_document_count": len(source_documents),
                "key_claim_count": len(key_claims),
                "dominant_sin_type": dominant_sin_type,
            }
        )

    ranked_themes = sorted(
        theme_metrics,
        key=lambda item: (
            -int(item["finding_count"]),
            -int(item["source_document_count"]),
            -int(item["key_claim_count"]),
            str(item["theme_name"]),
            str(item["theme_id"]),
        ),
    )
    dominant_theme = ranked_themes[0]
    total_finding_count = sum(int(item["finding_count"]) for item in ranked_themes)
    dominant_theme_findings = int(dominant_theme["finding_count"])
    dominant_theme_share = round(dominant_theme_findings / total_finding_count, 2) if total_finding_count else 1.0
    second_theme_findings = int(ranked_themes[1]["finding_count"]) if len(ranked_themes) > 1 else 0

    signal_summary = {
        "theme_count": len(ranked_themes),
        "total_finding_count": total_finding_count,
        "dominant_theme_id": dominant_theme["theme_id"],
        "dominant_theme_name": dominant_theme["theme_name"],
        "dominant_theme_findings": dominant_theme_findings,
        "dominant_theme_share": dominant_theme_share,
        "second_theme_findings": second_theme_findings,
        "theme_source_document_counts": {
            str(item["theme_id"]): int(item["source_document_count"]) for item in ranked_themes
        },
        "theme_key_claim_counts": {
            str(item["theme_id"]): int(item["key_claim_count"]) for item in ranked_themes
        },
        "dominant_sin_type_per_theme": {
            str(item["theme_id"]): str(item["dominant_sin_type"]) for item in ranked_themes
        },
        "original_section_order": list(section_order),
        "section_titles": {
            str(theme_id): str(raw_titles.get(theme_id) or "") for theme_id in section_order
        },
    }

    family, rationale, rejected = _choose_aoi_theme_surface_family(signal_summary)
    return AdaptiveSurfaceSelection(
        target_surface=payload.view_key,
        selected_family=family,
        signal_summary=signal_summary,
        rationale=rationale,
        rejected_families=rejected,
        ordered_cards=tuple(dict(item) for item in ranked_themes),
    )


def _select_adaptive_aoi_report_surface(
    payloads: dict[str, ViewPayload],
) -> AdaptiveSurfaceSelection:
    payload = payloads.get(ADAPTIVE_AOI_REPORT_VIEW_KEY)
    if payload is None:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=ADAPTIVE_AOI_REPORT_VIEW_KEY,
                    field="view_key",
                    message="Missing adaptive target surface: aoi_thematic_report",
                    reason="missing_adaptive_target_surface",
                )
            ]
        )

    source_payload = _extract_aoi_report_source_payload(payload)
    summary = str(source_payload.get("summary") or "").strip()
    engagement_pattern = str(source_payload.get("engagement_pattern") or "").strip()
    reading_implications = str(source_payload.get("reading_implications") or "").strip()
    key_divergences = _normalize_aoi_report_key_divergences(payload.view_key, source_payload.get("key_divergences"))
    sin_distribution = _normalize_aoi_report_sin_distribution(payload.view_key, source_payload.get("sin_distribution"))

    key_divergence_count = len(key_divergences)
    sin_distribution_count = len(sin_distribution)
    non_empty_prose_sections = sum(
        1
        for value in (summary, engagement_pattern, reading_implications)
        if bool(value)
    )
    signal_summary = {
        "key_divergence_count": key_divergence_count,
        "sin_distribution_count": sin_distribution_count,
        "non_empty_prose_sections": non_empty_prose_sections,
        "summary_length": len(summary),
        "engagement_pattern_length": len(engagement_pattern),
        "reading_implications_length": len(reading_implications),
    }

    family, rationale, rejected = _choose_aoi_report_surface_family(signal_summary)
    return AdaptiveSurfaceSelection(
        target_surface=payload.view_key,
        selected_family=family,
        signal_summary=signal_summary,
        rationale=rationale,
        rejected_families=rejected,
        ordered_cards=(),
    )


def _choose_conditions_surface_family_key(signal_summary: dict[str, Any]) -> str:
    if (
        int(signal_summary["path_dependencies_count"]) >= 2
        and int(signal_summary["path_signal_minus_balance_signal"]) >= 0
    ):
        return CONDITIONS_PATH_DEPENDENCY_MATRIX
    return CONDITIONS_BALANCE_SHEET


def _hydrate_conditions_surface_selection(
    *,
    payload: ViewPayload,
    selected_family: str,
    signal_summary: dict[str, Any],
    source_payload: dict[str, Any],
    declared_families: Optional[set[str]] = None,
) -> AdaptiveConditionsSelection:
    enabling_count = int(signal_summary["enabling_conditions_count"])
    constraining_count = int(signal_summary["constraining_conditions_count"])
    path_count = int(signal_summary["path_dependencies_count"])
    debt_count = int(signal_summary["unacknowledged_debts_count"])
    alternative_count = int(signal_summary["alternative_paths_count"])
    overall_balance = str(signal_summary["overall_balance"] or "balanced")

    if selected_family == CONDITIONS_PATH_DEPENDENCY_MATRIX:
        rationale = (
            f"Path dependencies and alternative branches dominate this conditions field "
            f"({path_count} dependencies, {alternative_count} alternatives, balance={_humanize_label(overall_balance)}), "
            "so a path-dependency matrix is the clearest surface."
        )
        rejected = (
            AdaptiveRejectedFamily(
                family=CONDITIONS_BALANCE_SHEET,
                reason="The conditions field is driven more by causal lock-in and branching structure than by a pressure balance summary.",
            ),
        )
    else:
        rationale = (
            f"The conditions field reads most clearly as an enabling/constraining balance "
            f"({enabling_count} enabling, {constraining_count} constraining, {debt_count} debts, "
            f"balance={_humanize_label(overall_balance)}), so a balance-sheet surface is the best fit."
        )
        rejected = (
            AdaptiveRejectedFamily(
                family=CONDITIONS_PATH_DEPENDENCY_MATRIX,
                reason="Path dependencies are not dense enough to displace the higher-level balance of enabling and constraining pressures.",
            ),
        )

    if declared_families is not None:
        rejected = tuple(item for item in rejected if item.family in declared_families)

    return AdaptiveConditionsSelection(
        target_surface=payload.view_key,
        selected_family=selected_family,
        signal_summary=signal_summary,
        rationale=rationale,
        rejected_families=rejected,
        source_payload=source_payload,
    )


def _choose_aoi_theme_surface_family(
    signal_summary: dict[str, Any],
) -> tuple[str, str, tuple[AdaptiveRejectedFamily, ...]]:
    theme_count = int(signal_summary["theme_count"])
    total_finding_count = int(signal_summary["total_finding_count"])
    dominant_theme_name = str(signal_summary.get("dominant_theme_name") or "The leading theme")
    dominant_theme_findings = int(signal_summary["dominant_theme_findings"])
    dominant_theme_share = float(signal_summary["dominant_theme_share"])

    if total_finding_count == 0:
        rationale = (
            f"No bound findings are present across {theme_count} themes, so a dossier preserves the richest "
            "per-theme reading surface."
        )
        return (
            AOI_THEME_DOSSIER,
            rationale,
            (
                AdaptiveRejectedFamily(
                    family=AOI_THEME_COMPARISON_REVIEW,
                    reason="No bounded findings are present, so a comparative table would collapse into thin empty rows.",
                ),
            ),
        )

    if theme_count <= 3 and dominant_theme_share >= 0.5:
        rationale = (
            f"{dominant_theme_name} carries {dominant_theme_findings} of {total_finding_count} findings "
            f"({round(dominant_theme_share * 100)}%), so a dossier-led reading is the clearest surface."
        )
        return (
            AOI_THEME_DOSSIER,
            rationale,
            (
                AdaptiveRejectedFamily(
                    family=AOI_THEME_COMPARISON_REVIEW,
                    reason="The thematic field is not distributed enough to justify a side-by-side comparison surface.",
                ),
            ),
        )

    rationale = (
        f"The findings remain distributed across {theme_count} themes with no single theme exceeding "
        f"{round(dominant_theme_share * 100)}% of the evidence, so a comparison review is the most legible family."
    )
    return (
        AOI_THEME_COMPARISON_REVIEW,
        rationale,
        (
            AdaptiveRejectedFamily(
                family=AOI_THEME_DOSSIER,
                reason="No single theme dominates strongly enough to sustain a dossier-led reading surface.",
            ),
        ),
    )


def _choose_aoi_report_surface_family(
    signal_summary: dict[str, Any],
) -> tuple[str, str, tuple[AdaptiveRejectedFamily, ...]]:
    key_divergence_count = int(signal_summary["key_divergence_count"])
    sin_distribution_count = int(signal_summary["sin_distribution_count"])
    non_empty_prose_sections = int(signal_summary["non_empty_prose_sections"])

    if key_divergence_count >= 4 and sin_distribution_count >= 3:
        rationale = (
            f"The report carries {key_divergence_count} divergence cards across {sin_distribution_count} sin "
            "categories, so an evidence-led review is the clearest surface."
        )
        return (
            AOI_REPORT_EVIDENCE_REVIEW,
            rationale,
            (
                AdaptiveRejectedFamily(
                    family=AOI_REPORT_BRIEFING,
                    reason="The report evidence is dense enough that a prose-first briefing would hide the comparative structure.",
                ),
            ),
        )

    rationale = (
        f"The report is driven more by briefing prose ({non_empty_prose_sections} non-empty prose sections) "
        f"than by dense divergence matrices ({key_divergence_count} divergences, {sin_distribution_count} sin categories), "
        "so a briefing-led closeout is the best fit."
    )
    return (
        AOI_REPORT_BRIEFING,
        rationale,
        (
            AdaptiveRejectedFamily(
                family=AOI_REPORT_EVIDENCE_REVIEW,
                reason="The divergence and sin-distribution evidence is not dense enough to displace the prose-led report summary.",
            ),
        ),
    )


def _declarative_signal_extractors() -> dict[str, Any]:
    return {
        SIGNAL_EXTRACTOR_KEY_RELATIONSHIP_SURFACE_SIGNALS_V1: _extract_relationship_surface_signals,
        SIGNAL_EXTRACTOR_KEY_CONDITIONS_SURFACE_SIGNALS_V1: _extract_conditions_surface_signals,
    }


def _relationship_surface_builders() -> dict[str, Any]:
    return {
        RELATIONSHIP_PROFILE_DOSSIER: _build_relationship_profile_dossier_payload,
        RELATIONSHIP_COMPARISON_REVIEW: _build_relationship_comparison_review_payload,
        RELATIONSHIP_FIELD_MAP: _build_relationship_field_map_payload,
        BUILDER_TEMPLATE_KEY_RELATIONSHIP_PROFILE_DOSSIER: _build_relationship_profile_dossier_payload,
        BUILDER_TEMPLATE_KEY_RELATIONSHIP_COMPARISON_REVIEW: _build_relationship_comparison_review_payload,
    }


def _build_relationship_surface_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveSurfaceSelection,
    builder_template_key: str,
) -> ViewPayload:
    builder = _relationship_surface_builders().get(builder_template_key)
    if builder is None:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=base_payload.view_key,
                    field="builder_template_key",
                    message=f"Unknown relationship surface builder template: {builder_template_key}",
                    reason="adaptive_spec_unknown_builder_template",
                )
            ]
        )
    return builder(
        base_payload=base_payload,
        selection=selection,
    )


def _conditions_surface_builders() -> dict[str, Any]:
    return {
        CONDITIONS_BALANCE_SHEET: _build_conditions_balance_sheet_payload,
        CONDITIONS_PATH_DEPENDENCY_MATRIX: _build_conditions_path_dependency_matrix_payload,
        BUILDER_TEMPLATE_KEY_CONDITIONS_BALANCE_SHEET: _build_conditions_balance_sheet_payload,
        BUILDER_TEMPLATE_KEY_CONDITIONS_PATH_DEPENDENCY_MATRIX: _build_conditions_path_dependency_matrix_payload,
    }


def _build_conditions_surface_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveConditionsSelection,
    builder_template_key: str,
) -> ViewPayload:
    builder = _conditions_surface_builders().get(builder_template_key)
    if builder is None:
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=base_payload.view_key,
                    field="builder_template_key",
                    message=f"Unknown conditions surface builder template: {builder_template_key}",
                    reason="adaptive_spec_unknown_builder_template",
                )
            ]
        )
    return builder(
        base_payload=base_payload,
        selection=selection,
    )


def _build_relationship_profile_dossier_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveSurfaceSelection,
) -> ViewPayload:
    lead_card = dict(selection.ordered_cards[0])
    supporting_cards = [dict(card) for card in selection.ordered_cards[1:]]
    counterfactual = str(
        lead_card.get("counterfactual_loss")
        or lead_card.get("what_would_be_lost")
        or ""
    ).strip()
    field_snapshot = {
        "dominant_work": lead_card.get("work_title") or "",
        "dominant_relationship": lead_card.get("relationship_type_label") or "",
        "relationship_count": selection.signal_summary["relationship_count"],
        "distinct_relationship_types": selection.signal_summary["distinct_relationship_types"],
        "top_share": f"{round(float(selection.signal_summary['top_share']) * 100)}%",
    }

    structured_data: dict[str, Any] = {}
    sections: list[dict[str, str]] = []
    section_renderers: dict[str, dict[str, Any]] = {}
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="focus_summary",
        title="Why This Relationship Dominates",
        value=selection.rationale,
        renderer_type="prose_block",
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="dominant_relationship",
        title="Dominant Relationship",
        value=[lead_card],
        renderer_type="mini_card_list",
        config={
            "title_field": "work_title",
            "subtitle_field": "relationship_type_label",
            "badge_field": "relationship_strength_label",
            "description_field": "centrality_excerpt",
        },
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="supporting_relationships",
        title="Supporting Context",
        value=supporting_cards,
        renderer_type="mini_card_list",
        config={
            "title_field": "work_title",
            "subtitle_field": "relationship_type_label",
            "badge_field": "relationship_strength_label",
            "description_field": "summary",
        },
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="field_snapshot",
        title="Field Snapshot",
        value=field_snapshot,
        renderer_type="key_value_table",
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="dominant_evidence",
        title="Key Evidence",
        value={"evidence": lead_card.get("key_evidence") or []},
        renderer_type="evidence_trail",
        config={
            "steps": [
                {
                    "label": "Evidence",
                    "field": "evidence",
                    "variant": "current",
                    "item_title_field": "evidence_type",
                    "item_quote_field": "quote",
                }
            ]
        },
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="counterfactual_focus",
        title="Without This Work",
        value=counterfactual,
        renderer_type="prose_block",
    )

    payload = base_payload.model_copy(deep=True)
    payload.view_name = "Relationship Dossier"
    payload.description = selection.rationale
    payload.renderer_type = "accordion"
    payload.renderer_config = {
        "sections": sections,
        "section_renderers": section_renderers,
    }
    payload.presentation_stance = "narrative"
    payload.scope = "aggregated"
    payload.has_structured_data = True
    payload.structured_data = structured_data
    payload.items = None
    payload.raw_prose = None
    payload.tab_count = None
    payload.data_quality = "rich"
    payload.derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY
    return payload


def _build_relationship_comparison_review_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveSurfaceSelection,
) -> ViewPayload:
    rows = [
        {
            "work_title": card.get("work_title") or "",
            "relationship_type": card.get("relationship_type_label") or "",
            "strength": card.get("relationship_strength_label") or "",
            "channels": card.get("primary_channels") or "",
            "why_it_matters": card.get("comparison_excerpt") or "",
        }
        for card in selection.ordered_cards
    ]

    payload = base_payload.model_copy(deep=True)
    payload.view_name = "Relationship Comparison Review"
    payload.description = selection.rationale
    payload.renderer_type = "table"
    payload.renderer_config = {
        "compact": True,
        "sortable": True,
        "columns": [
            {"key": "work_title", "label": "Work", "sortable": True},
            {"key": "relationship_type", "label": "Relationship", "sortable": True},
            {"key": "strength", "label": "Strength", "sortable": True},
            {"key": "channels", "label": "Channels", "sortable": False},
            {"key": "why_it_matters", "label": "Why It Matters", "sortable": False},
        ],
    }
    payload.presentation_stance = "comparison"
    payload.scope = "aggregated"
    payload.has_structured_data = True
    payload.structured_data = rows
    payload.items = None
    payload.raw_prose = None
    payload.tab_count = None
    payload.data_quality = "rich"
    payload.derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY
    return payload


def _build_relationship_field_map_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveSurfaceSelection,
) -> ViewPayload:
    structured_data: dict[str, Any] = {}
    sections: list[dict[str, str]] = []
    section_renderers: dict[str, dict[str, Any]] = {}
    field_snapshot = {
        "relationship_count": selection.signal_summary["relationship_count"],
        "distinct_relationship_types": selection.signal_summary["distinct_relationship_types"],
        "strongest_work": selection.signal_summary["dominant_work_title"],
        "strongest_relationship": _humanize_label(
            str(selection.signal_summary["dominant_relationship_type"] or "")
        ),
        "top_share": f"{round(float(selection.signal_summary['top_share']) * 100)}%",
    }

    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="field_summary",
        title="Field Summary",
        value=selection.rationale,
        renderer_type="prose_block",
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="field_snapshot",
        title="Field Snapshot",
        value=field_snapshot,
        renderer_type="key_value_table",
    )

    cards_by_type: dict[str, list[dict[str, Any]]] = {}
    for card in selection.ordered_cards:
        relationship_type = str(card.get("relationship_type") or "other")
        cards_by_type.setdefault(relationship_type, []).append(dict(card))

    for relationship_type, cards in sorted(
        cards_by_type.items(),
        key=lambda item: (-len(item[1]), -max(int(card["_adaptive_score"]) for card in item[1]), item[0]),
    ):
        title = f"{_humanize_label(relationship_type)} Band"
        key = f"{relationship_type}_band"
        _append_runtime_section(
            structured_data=structured_data,
            sections=sections,
            section_renderers=section_renderers,
            key=key,
            title=title,
            value=cards,
            renderer_type="mini_card_list",
            config={
                "title_field": "work_title",
                "subtitle_field": "relationship_strength_label",
                "description_field": "summary",
            },
        )

    payload = base_payload.model_copy(deep=True)
    payload.view_name = "Relationship Field Map"
    payload.description = selection.rationale
    payload.renderer_type = "accordion"
    payload.renderer_config = {
        "sections": sections,
        "section_renderers": section_renderers,
    }
    payload.presentation_stance = "diagnostic"
    payload.scope = "aggregated"
    payload.has_structured_data = True
    payload.structured_data = structured_data
    payload.items = None
    payload.raw_prose = None
    payload.tab_count = None
    payload.data_quality = "rich"
    payload.derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY
    return payload


def _build_conditions_balance_sheet_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveConditionsSelection,
) -> ViewPayload:
    source = selection.source_payload
    meta = dict(source.get("meta") or {})
    structured_data: dict[str, Any] = {}
    sections: list[dict[str, str]] = []
    section_renderers: dict[str, dict[str, Any]] = {}

    snapshot = {
        "overall_balance": _humanize_label(str(meta.get("overall_balance") or "balanced")),
        "enabling_conditions_count": meta.get("enabling_conditions_count", 0),
        "constraining_conditions_count": meta.get("constraining_conditions_count", 0),
        "path_dependencies_count": meta.get("path_dependencies_count", 0),
        "unacknowledged_debts_count": meta.get("unacknowledged_debts_count", 0),
        "alternative_paths_count": meta.get("alternative_paths_count", 0),
    }

    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="conditions_snapshot",
        title="Conditions Snapshot",
        value=snapshot,
        renderer_type="key_value_table",
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="enabling_pressures",
        title="Enabling Pressures",
        value=source.get("enabling_conditions") or [],
        renderer_type="mini_card_list",
        config={
            "title_field": "description",
            "subtitle_field": "condition_type",
            "badge_field": "essentiality",
            "description_field": "how_it_enables",
        },
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="constraining_pressures",
        title="Constraining Pressures",
        value=source.get("constraining_conditions") or [],
        renderer_type="mini_card_list",
        config={
            "title_field": "description",
            "subtitle_field": "constraint_type",
            "badge_field": "binding_force",
            "description_field": "how_navigated",
        },
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="unacknowledged_debts",
        title="Unacknowledged Debts",
        value=source.get("unacknowledged_debts") or [],
        renderer_type="mini_card_list",
        config={
            "title_field": "what_is_owed",
            "subtitle_field": "creditor_work",
            "description_field": "possible_reasons",
        },
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="synthetic_judgment",
        title="Synthetic Judgment",
        value=source.get("synthetic_judgment"),
        renderer_type="prose_block",
    )
    _append_runtime_section(
        structured_data=structured_data,
        sections=sections,
        section_renderers=section_renderers,
        key="counterfactual_stakes",
        title="Counterfactual Stakes",
        value=source.get("counterfactual_analysis"),
        renderer_type="prose_block",
    )

    payload = base_payload.model_copy(deep=True)
    payload.view_name = "Conditions Balance Sheet"
    payload.description = selection.rationale
    payload.renderer_type = "accordion"
    payload.renderer_config = {
        "sections": sections,
        "section_renderers": section_renderers,
    }
    payload.presentation_stance = "diagnostic"
    payload.scope = "aggregated"
    payload.has_structured_data = True
    payload.structured_data = structured_data
    payload.items = None
    payload.raw_prose = None
    payload.tab_count = None
    payload.data_quality = "rich"
    payload.derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY
    return payload


def _build_conditions_path_dependency_matrix_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveConditionsSelection,
) -> ViewPayload:
    source = selection.source_payload
    path_rows = [
        {
            "description": str(item.get("description") or ""),
            "chain_depth": len(item.get("chain") or []),
            "chain_summary": " -> ".join(str(step) for step in (item.get("chain") or [])),
            "if_absent": str(item.get("if_absent") or ""),
            "acknowledged": "Yes" if bool(item.get("is_acknowledged")) else "No",
        }
        for item in source.get("path_dependencies") or []
        if isinstance(item, dict)
    ]
    alternative_rows = [
        {
            "branching_point": str(item.get("branching_point") or ""),
            "path_not_taken": str(item.get("path_not_taken") or ""),
            "why_not_taken": str(item.get("why_not_taken") or ""),
            "implications": str(item.get("implications") or ""),
        }
        for item in source.get("alternative_paths") or []
        if isinstance(item, dict)
    ]

    payload = base_payload.model_copy(deep=True)
    payload.view_name = "Conditions Path-Dependency Matrix"
    payload.description = selection.rationale
    payload.renderer_type = "table"
    payload.renderer_config = {
        "compact": True,
        "sortable": True,
    }
    payload.presentation_stance = "diagnostic"
    payload.scope = "aggregated"
    payload.has_structured_data = True
    payload.structured_data = {
        "tables": [
            {
                "title": "Path Dependencies",
                "columns": [
                    {"key": "description", "label": "Dependency", "sortable": True},
                    {"key": "chain_depth", "label": "Chain Depth", "sortable": True},
                    {"key": "chain_summary", "label": "Chain", "sortable": False},
                    {"key": "if_absent", "label": "If Absent", "sortable": False},
                    {"key": "acknowledged", "label": "Acknowledged", "sortable": True},
                ],
                "rows": path_rows,
            },
            {
                "title": "Alternative Paths",
                "columns": [
                    {"key": "branching_point", "label": "Branching Point", "sortable": True},
                    {"key": "path_not_taken", "label": "Path Not Taken", "sortable": True},
                    {"key": "why_not_taken", "label": "Why Not Taken", "sortable": False},
                    {"key": "implications", "label": "Implications", "sortable": False},
                ],
                "rows": alternative_rows,
            },
        ]
    }
    payload.items = None
    payload.raw_prose = None
    payload.tab_count = None
    payload.data_quality = "rich"
    payload.derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY
    return payload


def _build_aoi_theme_dossier_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveSurfaceSelection,
) -> ViewPayload:
    signal_summary = selection.signal_summary
    theme_objects = [dict(item) for item in selection.ordered_cards]
    dominant_theme_name = str(signal_summary.get("dominant_theme_name") or "The leading theme")
    total_finding_count = int(signal_summary["total_finding_count"])
    dominant_theme_findings = int(signal_summary["dominant_theme_findings"])
    theme_count = int(signal_summary["theme_count"])
    original_section_order = [str(theme_id) for theme_id in signal_summary.get("original_section_order") or []]
    section_titles = {
        str(theme_id): str(title or "")
        for theme_id, title in dict(signal_summary.get("section_titles") or {}).items()
    }
    if total_finding_count > 0:
        suite_summary = (
            f"{dominant_theme_name} carries {dominant_theme_findings} of {total_finding_count} findings across "
            f"{theme_count} themes, so the surface is rendered as a dossier-led thematic reading."
        )
    else:
        suite_summary = (
            f"{theme_count} themes are present with no bound findings, so the surface is rendered as a "
            "dossier-led thematic reading."
        )

    theme_lookup = {
        str(theme["theme_id"]): dict(theme)
        for theme in theme_objects
    }
    structured_data: dict[str, Any] = {
        "suite_summary": suite_summary,
        "_section_order": list(original_section_order),
        "_section_titles": dict(section_titles),
    }
    sections: list[dict[str, str]] = [{"key": "suite_summary", "title": "Theme Summary"}]
    for theme_id in original_section_order:
        theme = theme_lookup[theme_id]
        structured_data[theme_id] = {
            "overview": str(theme.get("overview") or ""),
            "engagement": str(theme.get("engagement") or ""),
            "key_claims": list(theme.get("key_claims") or []),
            "philosophical_commitments": list(theme.get("philosophical_commitments") or []),
            "argumentative_moves": list(theme.get("argumentative_moves") or []),
            "source_documents": list(theme.get("source_documents") or []),
            "findings": list(theme.get("findings") or []),
        }
        sections.append({"key": theme_id, "title": section_titles[theme_id]})

    payload = base_payload.model_copy(deep=True)
    payload.view_name = "Theme Dossier"
    payload.description = selection.rationale
    payload.renderer_type = "accordion"
    payload.renderer_config = {
        "sections": sections,
        "section_renderers": {
            "suite_summary": {
                "renderer_type": "prose_block",
                "config": {},
            },
            "_default": {
                "sub_renderers": {
                    "overview": {"renderer_type": "annotated_prose"},
                    "engagement": {"renderer_type": "annotated_prose"},
                    "key_claims": {
                        "renderer_type": "rich_description_list",
                        "config": {
                            "title_field": "title",
                            "description_field": "description",
                        },
                    },
                    "philosophical_commitments": {
                        "renderer_type": "rich_description_list",
                        "config": {
                            "title_field": "title",
                            "description_field": "description",
                        },
                    },
                    "argumentative_moves": {
                        "renderer_type": "rich_description_list",
                        "config": {
                            "title_field": "title",
                            "description_field": "description",
                        },
                    },
                    "source_documents": {"renderer_type": "chip_grid"},
                    "findings": {
                        "renderer_type": "mini_card_list",
                        "config": {
                            "title_field": "title",
                            "subtitle_field": "subtitle",
                            "description_field": "description",
                            "badge_field": "badge",
                        },
                    },
                },
            },
        },
    }
    payload.presentation_stance = "narrative"
    payload.scope = "aggregated"
    payload.has_structured_data = True
    payload.structured_data = structured_data
    payload.items = None
    payload.raw_prose = None
    payload.tab_count = None
    payload.data_quality = "rich"
    payload.derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY
    payload.source_parent_view_key = "aoi_thematic_analysis"
    return payload


def _build_aoi_theme_comparison_review_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveSurfaceSelection,
) -> ViewPayload:
    rows = [
        {
            "theme_name": str(theme["theme_name"]),
            "finding_count": int(theme["finding_count"]),
            "dominant_sin_type": str(theme["dominant_sin_type"]),
            "source_document_count": int(theme["source_document_count"]),
            "key_claim_count": int(theme["key_claim_count"]),
            "overview_excerpt": _truncate_runtime_overview(str(theme.get("overview") or "")),
        }
        for theme in selection.ordered_cards
    ]

    payload = base_payload.model_copy(deep=True)
    payload.view_name = "Theme Comparison Review"
    payload.description = selection.rationale
    payload.renderer_type = "table"
    payload.renderer_config = {
        "compact": True,
        "sortable": True,
        "columns": [
            {"key": "theme_name", "label": "Theme", "sortable": True},
            {"key": "finding_count", "label": "Findings", "sortable": True},
            {"key": "dominant_sin_type", "label": "Dominant Sin Type", "sortable": True},
            {"key": "source_document_count", "label": "Sources", "sortable": True},
            {"key": "key_claim_count", "label": "Key Claims", "sortable": True},
            {"key": "overview_excerpt", "label": "Overview", "sortable": False},
        ],
    }
    payload.presentation_stance = "comparison"
    payload.scope = "aggregated"
    payload.has_structured_data = True
    payload.structured_data = rows
    payload.items = None
    payload.raw_prose = None
    payload.tab_count = None
    payload.data_quality = "rich"
    payload.derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY
    payload.source_parent_view_key = "aoi_thematic_analysis"
    return payload


def _build_aoi_report_briefing_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveSurfaceSelection,
) -> ViewPayload:
    source = _extract_aoi_report_source_payload(base_payload)
    summary = str(source.get("summary") or "").strip()
    engagement_pattern = str(source.get("engagement_pattern") or "").strip()
    reading_implications = str(source.get("reading_implications") or "").strip()
    key_divergences = _normalize_aoi_report_key_divergences(base_payload.view_key, source.get("key_divergences"))
    sin_distribution = _normalize_aoi_report_sin_distribution(base_payload.view_key, source.get("sin_distribution"))

    key_divergence_count = int(selection.signal_summary["key_divergence_count"])
    sin_distribution_count = int(selection.signal_summary["sin_distribution_count"])
    if key_divergence_count > 0:
        suite_summary = (
            f"{key_divergence_count} key divergences are distributed across {sin_distribution_count} sin "
            "categories, so the report is rendered as a briefing-led closeout."
        )
    else:
        suite_summary = (
            "The report is rendered as a briefing-led closeout because the prose sections dominate "
            "the available structured evidence."
        )

    payload = base_payload.model_copy(deep=True)
    payload.view_name = "Report Briefing"
    payload.description = selection.rationale
    payload.renderer_type = "accordion"
    payload.renderer_config = {
        "sections": [
            {"key": "suite_summary", "title": "Report Summary"},
            {"key": "summary", "title": "Summary"},
            {"key": "engagement_pattern", "title": "Engagement Pattern"},
            {"key": "reading_implications", "title": "Reading Implications"},
            {"key": "key_divergences", "title": "Key Divergences"},
            {"key": "sin_distribution", "title": "Sin Distribution"},
        ],
        "section_renderers": {
            "suite_summary": {"renderer_type": "prose_block", "config": {}},
            "summary": {"renderer_type": "annotated_prose", "config": {}},
            "engagement_pattern": {"renderer_type": "annotated_prose", "config": {}},
            "reading_implications": {"renderer_type": "annotated_prose", "config": {}},
            "key_divergences": {
                "renderer_type": "mini_card_list",
                "config": {
                    "title_field": "title",
                    "subtitle_field": "subtitle",
                    "description_field": "description",
                    "badge_field": "badge",
                },
            },
            "sin_distribution": {
                "renderer_type": "mini_card_list",
                "config": {
                    "title_field": "sin_type",
                    "subtitle_field": "count",
                    "description_field": "description",
                },
            },
        },
    }
    payload.presentation_stance = "summary"
    payload.scope = "aggregated"
    payload.has_structured_data = True
    payload.structured_data = {
        "suite_summary": suite_summary,
        "summary": summary,
        "engagement_pattern": engagement_pattern,
        "reading_implications": reading_implications,
        "key_divergences": key_divergences,
        "sin_distribution": sin_distribution,
    }
    payload.items = None
    payload.raw_prose = None
    payload.tab_count = None
    payload.data_quality = "rich"
    payload.derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY
    payload.source_parent_view_key = "aoi_thematic_analysis"
    return payload


def _build_aoi_report_evidence_review_payload(
    *,
    base_payload: ViewPayload,
    selection: AdaptiveSurfaceSelection,
) -> ViewPayload:
    source = _extract_aoi_report_source_payload(base_payload)
    key_divergences = _normalize_aoi_report_key_divergences(base_payload.view_key, source.get("key_divergences"))
    sin_distribution = _normalize_aoi_report_sin_distribution(base_payload.view_key, source.get("sin_distribution"))
    snapshot_rows = [
        {
            "summary_excerpt": _truncate_runtime_report_excerpt(str(source.get("summary") or "")),
            "engagement_excerpt": _truncate_runtime_report_excerpt(str(source.get("engagement_pattern") or "")),
            "implications_excerpt": _truncate_runtime_report_excerpt(str(source.get("reading_implications") or "")),
        }
    ]

    payload = base_payload.model_copy(deep=True)
    payload.view_name = "Report Evidence Review"
    payload.description = selection.rationale
    payload.renderer_type = "table"
    payload.renderer_config = {
        "compact": True,
        "sortable": True,
    }
    payload.presentation_stance = "diagnostic"
    payload.scope = "aggregated"
    payload.has_structured_data = True
    payload.structured_data = {
        "tables": [
            {
                "title": "Report Snapshot",
                "columns": [
                    {"key": "summary_excerpt", "label": "Summary", "sortable": False},
                    {"key": "engagement_excerpt", "label": "Engagement Pattern", "sortable": False},
                    {"key": "implications_excerpt", "label": "Implications", "sortable": False},
                ],
                "rows": snapshot_rows,
            },
            {
                "title": "Key Divergences",
                "columns": [
                    {"key": "title", "label": "Divergence", "sortable": True},
                    {"key": "subtitle", "label": "Theme", "sortable": True},
                    {"key": "description", "label": "Description", "sortable": False},
                    {"key": "badge", "label": "Severity", "sortable": True},
                ],
                "rows": key_divergences,
            },
            {
                "title": "Sin Distribution",
                "columns": [
                    {"key": "sin_type", "label": "Sin Type", "sortable": True},
                    {"key": "count", "label": "Count", "sortable": True},
                    {"key": "description", "label": "Description", "sortable": False},
                ],
                "rows": sin_distribution,
            },
        ]
    }
    payload.items = None
    payload.raw_prose = None
    payload.tab_count = None
    payload.data_quality = "rich"
    payload.derivation_kind = DERIVATION_KIND_RUNTIME_SURFACE_FAMILY
    payload.source_parent_view_key = "aoi_thematic_analysis"
    return payload


def _append_runtime_section(
    *,
    structured_data: dict[str, Any],
    sections: list[dict[str, str]],
    section_renderers: dict[str, dict[str, Any]],
    key: str,
    title: str,
    value: Any,
    renderer_type: str,
    config: Optional[dict[str, Any]] = None,
) -> None:
    if not _has_runtime_value(value):
        return

    structured_data[key] = value
    sections.append({"key": key, "title": title})
    section_renderers[key] = {
        "renderer_type": renderer_type,
        "config": config or {},
    }


def _has_runtime_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) > 0
    return True


def _extract_relationship_cards(payload: ViewPayload) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    for item in payload.items or []:
        if not isinstance(item, dict):
            continue
        structured = item.get("structured_data")
        if not isinstance(structured, dict):
            continue
        card = dict(structured)
        work_title = (
            card.get("work_title")
            or item.get("work_title")
            or item.get("work_key")
            or "Untitled work"
        )
        card["work_title"] = str(work_title)
        if item.get("work_key") and not card.get("work_key"):
            card["work_key"] = str(item["work_key"])
        cards.append(card)
    return cards


def _extract_conditions_source_payload(payload: ViewPayload) -> dict[str, Any]:
    if not isinstance(payload.structured_data, dict):
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=payload.view_key,
                    field="structured_data",
                    message="Adaptive conditions surface requires top-level structured_data on genealogy_conditions.",
                    reason="adaptive_surface_missing_structured_payload",
                )
            ]
        )
    return payload.structured_data


def _extract_conditions_surface_signals(
    payload: ViewPayload,
) -> tuple[dict[str, Any], dict[str, Any]]:
    source_payload = _extract_conditions_source_payload(payload)
    meta = source_payload.get("meta")
    meta = meta if isinstance(meta, dict) else {}

    enabling_conditions = _coerce_runtime_list(source_payload.get("enabling_conditions"))
    constraining_conditions = _coerce_runtime_list(source_payload.get("constraining_conditions"))
    path_dependencies = _coerce_runtime_list(source_payload.get("path_dependencies"))
    unacknowledged_debts = _coerce_runtime_list(source_payload.get("unacknowledged_debts"))
    alternative_paths = _coerce_runtime_list(source_payload.get("alternative_paths"))
    counterfactual_analysis = str(source_payload.get("counterfactual_analysis") or "").strip()
    synthetic_judgment = str(source_payload.get("synthetic_judgment") or "").strip()

    if not any(
        [
            enabling_conditions,
            constraining_conditions,
            path_dependencies,
            unacknowledged_debts,
            alternative_paths,
            counterfactual_analysis,
            synthetic_judgment,
        ]
    ):
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=payload.view_key,
                    field="structured_data",
                    message="Adaptive conditions surface requires structured top-level conditions data.",
                    reason="adaptive_surface_missing_structured_payload",
                )
            ]
        )

    enabling_count = _runtime_count(meta.get("enabling_conditions_count"), enabling_conditions)
    constraining_count = _runtime_count(meta.get("constraining_conditions_count"), constraining_conditions)
    path_count = _runtime_count(meta.get("path_dependencies_count"), path_dependencies)
    debt_count = _runtime_count(meta.get("unacknowledged_debts_count"), unacknowledged_debts)
    alternative_count = _runtime_count(meta.get("alternative_paths_count"), alternative_paths)

    overall_balance = _normalize_overall_balance(meta.get("overall_balance"))
    if overall_balance is None:
        if enabling_count > constraining_count:
            overall_balance = "enabling_dominant"
        elif constraining_count > enabling_count:
            overall_balance = "constraining_dominant"
        else:
            overall_balance = "balanced"

    path_signal = path_count + alternative_count
    balance_signal = enabling_count + constraining_count + debt_count
    normalized_source_payload = {
        "meta": {
            "overall_balance": overall_balance,
            "enabling_conditions_count": enabling_count,
            "constraining_conditions_count": constraining_count,
            "path_dependencies_count": path_count,
            "unacknowledged_debts_count": debt_count,
            "alternative_paths_count": alternative_count,
        },
        "enabling_conditions": enabling_conditions,
        "constraining_conditions": constraining_conditions,
        "path_dependencies": path_dependencies,
        "unacknowledged_debts": unacknowledged_debts,
        "alternative_paths": alternative_paths,
        "counterfactual_analysis": counterfactual_analysis,
        "synthetic_judgment": synthetic_judgment,
    }
    signal_summary = {
        "overall_balance": overall_balance,
        "enabling_conditions_count": enabling_count,
        "constraining_conditions_count": constraining_count,
        "path_dependencies_count": path_count,
        "unacknowledged_debts_count": debt_count,
        "alternative_paths_count": alternative_count,
        "counterfactual_present": bool(counterfactual_analysis),
        "synthesis_present": bool(synthetic_judgment),
        "path_signal": path_signal,
        "balance_signal": balance_signal,
        "path_signal_minus_balance_signal": path_signal - balance_signal,
    }
    return normalized_source_payload, signal_summary


def _extract_aoi_theme_source_payload(payload: ViewPayload) -> dict[str, Any]:
    if not isinstance(payload.structured_data, dict):
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=payload.view_key,
                    field="structured_data",
                    message="Adaptive AOI theme surface requires top-level structured_data on aoi_by_theme.",
                    reason="adaptive_surface_missing_structured_payload",
                )
            ]
        )
    source_payload = dict(payload.structured_data)
    renderer_config = payload.renderer_config if isinstance(payload.renderer_config, dict) else {}
    sections = renderer_config.get("sections")

    if "_section_order" not in source_payload and isinstance(sections, list):
        source_payload["_section_order"] = [
            str(section.get("key"))
            for section in sections
            if isinstance(section, dict)
            and section.get("key") is not None
            and str(section.get("key")) in source_payload
        ]

    if "_section_titles" not in source_payload and isinstance(sections, list):
        source_payload["_section_titles"] = {
            str(section.get("key")): str(section.get("title") or "")
            for section in sections
            if isinstance(section, dict)
            and section.get("key") is not None
            and str(section.get("key")) in source_payload
        }

    return source_payload


def _extract_aoi_report_source_payload(payload: ViewPayload) -> dict[str, Any]:
    if not isinstance(payload.structured_data, dict):
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=payload.view_key,
                    field="structured_data",
                    message="Adaptive AOI report surface requires top-level structured_data on aoi_thematic_report.",
                    reason="adaptive_surface_missing_structured_payload",
                )
            ]
        )
    return payload.structured_data


def _normalize_aoi_report_key_divergences(
    view_key: str,
    value: Any,
) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=view_key,
                    field="key_divergences",
                    message="Adaptive AOI report surface requires key_divergences to be a list of objects.",
                    reason="adaptive_report_invalid_key_divergences_shape",
                )
            ]
        )

    normalized: list[dict[str, str]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise BoundedCompositionValidationError(
                [
                    CompositionIssue(
                        view_key=view_key,
                        field=f"key_divergences[{index}]",
                        message="Adaptive AOI report surface requires every key_divergences item to be an object.",
                        reason="adaptive_report_invalid_key_divergence_item",
                    )
                ]
            )
        title = str(item.get("title") or "").strip()
        description = str(item.get("description") or "").strip()
        if not title or not description:
            raise BoundedCompositionValidationError(
                [
                    CompositionIssue(
                        view_key=view_key,
                        field=f"key_divergences[{index}]",
                        message="Adaptive AOI report surface requires every key divergence to include title and description.",
                        reason="adaptive_report_missing_key_divergence_fields",
                    )
                ]
            )
        normalized.append(
            {
                "title": title,
                "subtitle": str(item.get("subtitle") or "").strip(),
                "description": description,
                "badge": str(item.get("badge") or "").strip(),
            }
        )
    return normalized


def _normalize_aoi_report_sin_distribution(
    view_key: str,
    value: Any,
) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise BoundedCompositionValidationError(
            [
                CompositionIssue(
                    view_key=view_key,
                    field="sin_distribution",
                    message="Adaptive AOI report surface requires sin_distribution to be a list of objects.",
                    reason="adaptive_report_invalid_sin_distribution_shape",
                )
            ]
        )

    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise BoundedCompositionValidationError(
                [
                    CompositionIssue(
                        view_key=view_key,
                        field=f"sin_distribution[{index}]",
                        message="Adaptive AOI report surface requires every sin_distribution item to be an object.",
                        reason="adaptive_report_invalid_sin_distribution_item",
                    )
                ]
            )
        sin_type = str(item.get("sin_type") or "").strip()
        count = item.get("count")
        if not sin_type or count is None:
            raise BoundedCompositionValidationError(
                [
                    CompositionIssue(
                        view_key=view_key,
                        field=f"sin_distribution[{index}]",
                        message="Adaptive AOI report surface requires every sin distribution item to include sin_type and count.",
                        reason="adaptive_report_missing_sin_distribution_fields",
                    )
                ]
            )
        normalized.append(
            {
                "sin_type": sin_type,
                "count": _normalize_runtime_count_value(count),
                "description": str(item.get("description") or "").strip(),
            }
        )
    return normalized


def _coerce_runtime_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _coerce_runtime_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _runtime_count(meta_value: Any, fallback_items: list[dict[str, Any]]) -> int:
    if isinstance(meta_value, bool):
        return int(meta_value)
    if isinstance(meta_value, int):
        return meta_value
    if isinstance(meta_value, float):
        return int(meta_value)
    if isinstance(meta_value, str):
        try:
            return int(meta_value)
        except ValueError:
            return len(fallback_items)
    return len(fallback_items)


def _normalize_runtime_count_value(value: Any) -> Any:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return 0
        try:
            return int(stripped)
        except ValueError:
            return stripped
    return value


def _normalize_overall_balance(value: Any) -> Optional[str]:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    if normalized in {"enabling_dominant", "constraining_dominant", "balanced"}:
        return normalized
    return None


def _decorate_relationship_card(card: dict[str, Any]) -> dict[str, Any]:
    decorated = dict(card)
    relationship_type = str(decorated.get("relationship_type") or "other")
    relationship_strength = str(decorated.get("relationship_strength") or "weak")
    channels = decorated.get("influence_channels") or []
    channel_names = [
        str(channel.get("channel") or "")
        for channel in channels
        if isinstance(channel, dict) and channel.get("channel")
    ]
    comparison_excerpt = str(
        decorated.get("centrality_assessment")
        or decorated.get("summary")
        or ""
    ).strip()
    decorated["relationship_type_label"] = _humanize_label(relationship_type)
    decorated["relationship_strength_label"] = _humanize_label(relationship_strength)
    decorated["primary_channels"] = ", ".join(channel_names[:3])
    decorated["centrality_excerpt"] = comparison_excerpt
    decorated["comparison_excerpt"] = comparison_excerpt
    decorated["_adaptive_score"] = (
        _RELATIONSHIP_TYPE_WEIGHTS.get(relationship_type, 2)
        * _RELATIONSHIP_STRENGTH_WEIGHTS.get(relationship_strength, 1)
    )
    return decorated


def _humanize_label(value: str) -> str:
    return value.replace("_", " ").strip().title()


def _truncate_runtime_overview(value: str) -> str:
    trimmed = value.strip()
    if not trimmed:
        return "—"
    if len(trimmed) <= 150:
        return trimmed
    return f"{trimmed[:147]}..."


def _truncate_runtime_report_excerpt(value: str) -> str:
    trimmed = value.strip()
    if not trimmed:
        return "—"
    if len(trimmed) <= 160:
        return trimmed
    return f"{trimmed[:157]}..."


def _validate_runtime_payload(
    payload: ViewPayload,
    *,
    consumer_key: str,
) -> list[CompositionIssue]:
    issues: list[CompositionIssue] = []
    consumer = get_consumer_registry().get(consumer_key)
    supported_renderers = set(consumer.supported_renderers or []) if consumer else set()
    supported_sub_renderers = set(consumer.supported_sub_renderers or []) if consumer else set()

    if consumer and payload.renderer_type not in supported_renderers:
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field="renderer_type",
                message=f"Renderer '{payload.renderer_type}' is not supported by consumer '{consumer_key}'.",
                reason="renderer_not_supported_by_consumer",
            )
        )

    section_renderers = payload.renderer_config.get("section_renderers")
    if isinstance(section_renderers, dict):
        for section_key, renderer_spec in section_renderers.items():
            if isinstance(renderer_spec, dict):
                if isinstance(renderer_spec.get("sub_renderers"), dict):
                    for sub_key, sub_renderer_spec in renderer_spec["sub_renderers"].items():
                        renderer_key = None
                        if isinstance(sub_renderer_spec, dict):
                            renderer_key = sub_renderer_spec.get("renderer_type")
                        if renderer_key not in supported_sub_renderers and renderer_key not in supported_renderers:
                            issues.append(
                                CompositionIssue(
                                    view_key=payload.view_key,
                                    field=f"section_renderers.{section_key}.sub_renderers.{sub_key}",
                                    message=f"Sub-renderer '{renderer_key}' is not supported by consumer '{consumer_key}'.",
                                    reason="sub_renderer_not_supported_by_consumer",
                                )
                            )
                    continue
                renderer_key = renderer_spec.get("renderer_type")
                if renderer_key not in supported_sub_renderers and renderer_key not in supported_renderers:
                    issues.append(
                        CompositionIssue(
                            view_key=payload.view_key,
                            field=f"section_renderers.{section_key}",
                            message=f"Sub-renderer '{renderer_key}' is not supported by consumer '{consumer_key}'.",
                            reason="sub_renderer_not_supported_by_consumer",
                        )
                    )

    config_validation = validate_renderer_config(payload.renderer_type, payload.renderer_config)
    if not config_validation.valid:
        issues.extend(
            CompositionIssue(
                view_key=payload.view_key,
                field="renderer_config",
                message=error["message"],
                reason="renderer_config_validation_failed",
            )
            for error in config_validation.errors
        )

    data_validation = validate_renderer_data(
        payload.renderer_type,
        payload.structured_data,
        payload.renderer_config,
    )
    if not data_validation.valid:
        issues.extend(
            CompositionIssue(
                view_key=payload.view_key,
                field="structured_data",
                message=error["message"],
                reason="renderer_data_validation_failed",
            )
            for error in data_validation.errors
        )

    return issues
