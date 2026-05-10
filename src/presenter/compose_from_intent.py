"""Bounded transient compose-from-intent orchestration for AOI."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any, Optional

from src.aoi.constants import AOI_WORKFLOW_KEY
from src.engines.composition_roles import is_composition_role
from src.engines.discovery import resolve_capability_definition
from src.llm.client import (
    EXTRACTION_MODEL_FALLBACK,
    GENERATION_MODEL,
    call_extraction_model,
    parse_llm_json_response,
)
from src.presenter.composition_role_registry import (
    COMPOSITION_ROLE_HINTS,
    get_composition_role_spec,
)
from src.presenter.first_hop_affordance import (
    GENEALOGY_WORKFLOW_KEY,
    MIGRATED_COMPOSITION_ENGINE_FAMILIES as _MIGRATED_COMPOSITION_ENGINE_FAMILIES,
    MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS as _MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS,
    derive_first_hop_affordance,
)
from src.presenter.manifest_builder import adapt_renderer_for_consumer
from src.presenter.renderer_contract_enforcement import (
    ServedIntent,
    enforce_final_payload_contracts_or_raise,
)
from src.presenter.schemas import (
    ComposeFromIntentRequest,
    ComposeFromIntentResponse,
    ComposeFromSelectionRequest,
    ComposeFromSourceRequest,
    ComposeFromIntentTrace,
    ComposeFromIntentTraceEntry,
    FirstHopAffordance,
    TransientIntentPagePresentation,
    TransientIntentView,
    ViewPayload,
)
from src.presenter.composition_source_bridge import (
    CompositionMaterializedSection,
    ComposeFromSourceResolutionError,
    build_selection_composition_bridge,
    build_source_composition_bridge,
)
from src.presenter.composition_resolver import find_applicable_template
from src.presenter.dynamic_prompt import compose_dynamic_extraction_prompt
from src.renderers.registry import get_renderer_registry
from src.styles.registry import StyleRegistry
from src.styles.schemas import StyleSchool
from src.transformations.executor import TransformationExecutor
from src.views.generator import ViewGenerateRequest, generate_view
from src.views.pattern_registry import get_pattern_registry
from src.views.schemas import DataSourceRef, TransformationSpec, ViewDefinition

logger = logging.getLogger(__name__)

TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"
TRANSIENT_COMPOSE_TARGET_PAGE = "compose_from_intent_transient"
TRANSIENT_COMPOSE_RESOLVER_VERSION = "compose-from-intent-v2"
TRANSIENT_COMPOSE_SOURCE_RESOLVER_VERSION = "compose-from-source-v3"
TRANSIENT_COMPOSE_SELECTION_RESOLVER_VERSION = "compose-from-selection-v1"
TRANSIENT_PRESENTATION_CONTRACT_VERSION = 1
DEFAULT_STYLE_SCHOOL = StyleSchool.EXPLANATORY_NARRATIVE.value
_SOURCE_PROFILE_DEFAULT_INTENTS = {
    "dossier": (
        "Compose a compact AOI briefing page that foregrounds the high-level thematic synthesis "
        "and then closes with the structured report."
    ),
    "comparison": (
        "Compose a structured AOI comparison page that foregrounds the engagement map, then the "
        "sin findings, and ends with the report closeout."
    ),
}
_ALLOWED_PATTERN_KEYS = frozenset(
    {
        "prose_narrative",
        "accordion_sections",
        "card_grid_simple",
        "card_grid_grouped",
        "tab_with_children",
    }
)
_ALLOWED_RENDERER_TYPES = frozenset({"prose", "accordion", "card_grid", "tab"})
_INVENTORY_LISTING_TOKENS = frozenset(
    {
        "inventory",
        "inventories",
        "listing",
        "listings",
        "catalog",
        "catalogue",
        "index",
        "register",
        "ledger",
        "directory",
        "roster",
    }
)
_TITLE_ROLE_HINTS = (
    ("inventory_listing", frozenset({"inventory", "listing", "catalog", "catalogue", "index", "register", "ledger", "directory", "roster"})),
    ("comparison_map", frozenset({"comparison", "mapping", "map", "matrix"})),
    ("findings_bank", frozenset({"findings", "finding", "evidence", "bank"})),
    ("synthesis_primary", frozenset({"synthesis", "thematic", "themes", "overview"})),
    ("report_closeout", frozenset({"report", "closeout", "conclusion", "summary"})),
)
_CLOSEOUT_ROLES = frozenset({"report_closeout"})
_COMPARISON_PARENT_ROLES = frozenset({"comparison_map", "findings_bank"})
_HANDOFF_KIND_DIRECT_SECTIONS = "direct_sections"
_HANDOFF_KIND_SOURCE_PROFILE = "source_profile"
_HANDOFF_KIND_SOURCE_SELECTION = "source_selection"
_FIRST_HOP_AFFORDANCE_ELIGIBLE_HANDOFFS = frozenset(
    {
        (AOI_WORKFLOW_KEY, _HANDOFF_KIND_SOURCE_PROFILE),
        (AOI_WORKFLOW_KEY, _HANDOFF_KIND_SOURCE_SELECTION),
        (GENEALOGY_WORKFLOW_KEY, _HANDOFF_KIND_DIRECT_SECTIONS),
    }
)
_SUPPORTED_HANDOFF_KINDS = {
    AOI_WORKFLOW_KEY: frozenset(
        {
            _HANDOFF_KIND_DIRECT_SECTIONS,
            _HANDOFF_KIND_SOURCE_PROFILE,
            _HANDOFF_KIND_SOURCE_SELECTION,
        }
    ),
    GENEALOGY_WORKFLOW_KEY: frozenset({_HANDOFF_KIND_DIRECT_SECTIONS}),
}
_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS = {
    TRANSIENT_COMPOSE_CONSUMER_KEY: frozenset(
        {
            _HANDOFF_KIND_DIRECT_SECTIONS,
            _HANDOFF_KIND_SOURCE_PROFILE,
            _HANDOFF_KIND_SOURCE_SELECTION,
        }
    ),
    "aoi-canary": frozenset(
        {
            _HANDOFF_KIND_DIRECT_SECTIONS,
            _HANDOFF_KIND_SOURCE_PROFILE,
            _HANDOFF_KIND_SOURCE_SELECTION,
        }
    ),
    "transient-proof-harness": frozenset(
        {
            _HANDOFF_KIND_DIRECT_SECTIONS,
            _HANDOFF_KIND_SOURCE_SELECTION,
        }
    ),
    "transient-proof-probe": frozenset(
        {
            _HANDOFF_KIND_DIRECT_SECTIONS,
            _HANDOFF_KIND_SOURCE_SELECTION,
        }
    ),
}
_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER = {
    TRANSIENT_COMPOSE_CONSUMER_KEY: frozenset({"dossier", "comparison"}),
    "aoi-canary": frozenset({"dossier", "comparison"}),
}


class ComposeFromIntentClientError(ValueError):
    """Client-side request validation error."""


class ComposeFromIntentUpstreamError(RuntimeError):
    """Planner/generator/transformation orchestration failure."""


class ComposeFromIntentDependencyUnavailable(RuntimeError):
    """Upstream LLM dependency unavailable."""


@dataclass(frozen=True)
class _PlannerRow:
    section_index: int
    pattern_key: str
    view_name: str
    description: str
    presentation_stance: str
    rationale: str
    semantic_role: str = ""
    source_family_key: Optional[str] = None
    profile: Optional[str] = None
    materialization_position: Optional[int] = None
    is_closeout: bool = False


@dataclass(frozen=True)
class _PlannerSectionContext:
    section_index: int
    engine_key: str
    title: str
    prose: str
    source_family_key: Optional[str] = None
    composition_role_hint: Optional[str] = None
    profile: Optional[str] = None
    materialization_position: Optional[int] = None


@dataclass(frozen=True)
class _PlannerParent:
    pattern_key: str
    view_name: str
    description: str
    presentation_stance: str
    rationale: str


@dataclass(frozen=True)
class _SemanticPagePlan:
    leaf_rows: tuple[_PlannerRow, ...]
    parent: Optional[_PlannerParent] = None


class ComposeFromIntentTraceStage(ComposeFromIntentTraceEntry):
    """Back-compat alias for local readability."""


def compose_from_intent(request: ComposeFromIntentRequest) -> ComposeFromIntentResponse:
    """Compose a transient AOI page directly from intent + prose."""

    return _compose_handoff_sections(
        request,
        handoff_kind=_HANDOFF_KIND_DIRECT_SECTIONS,
        resolver_version=TRANSIENT_COMPOSE_RESOLVER_VERSION,
    )


def compose_from_source(request: ComposeFromSourceRequest) -> ComposeFromIntentResponse:
    """Compose a transient AOI page from an existing AOI v2 result."""

    _validate_source_request(request)
    bridge = build_source_composition_bridge(
        source_v2_job_id=request.source_v2_job_id,
        profile=request.profile,
    )
    sections = [entry.section for entry in bridge.materialized_sections]
    effective_intent = (request.user_intent or "").strip() or _SOURCE_PROFILE_DEFAULT_INTENTS[request.profile]
    intent_request = ComposeFromIntentRequest.model_validate(
        {
            "workflow_key": request.workflow_key,
            "consumer_key": request.consumer_key,
            "user_intent": effective_intent,
            "prose_sections": [section.model_dump() for section in sections],
            "style_school": request.style_school,
        }
    )
    return _compose_handoff_sections(
        intent_request,
        handoff_kind=_HANDOFF_KIND_SOURCE_PROFILE,
        resolver_version=TRANSIENT_COMPOSE_SOURCE_RESOLVER_VERSION,
        planning_sections=bridge.materialized_sections,
        trace_prefix=[
            ComposeFromIntentTraceStage(
                stage="source_catalog_resolution",
                details=bridge.catalog.to_trace_dict(),
            ),
            ComposeFromIntentTraceStage(
                stage="source_selection",
                details=bridge.selection.to_trace_dict(),
            ),
            ComposeFromIntentTraceStage(
                stage="section_materialization",
                details={
                    "selection_kind": "profile",
                    "profile": request.profile,
                    "section_count": len(bridge.materialized_sections),
                    "sections": [
                        section.to_trace_dict() for section in bridge.materialized_sections
                    ],
                },
            )
        ],
    )


def compose_from_selection(request: ComposeFromSelectionRequest) -> ComposeFromIntentResponse:
    """Compose a transient AOI page from an explicit planner-selected source set."""

    _validate_selection_request(request)
    bridge = build_selection_composition_bridge(
        source_v2_job_id=request.source_v2_job_id,
        selection=request.selection,
        selection_summary=request.selection_summary or "",
        legacy_profile_equivalent=request.legacy_profile_equivalent,
    )
    sections = [entry.section for entry in bridge.materialized_sections]
    intent_request = ComposeFromIntentRequest.model_validate(
        {
            "workflow_key": request.workflow_key,
            "consumer_key": request.consumer_key,
            "user_intent": request.user_intent.strip(),
            "prose_sections": [section.model_dump() for section in sections],
            "style_school": request.style_school,
        }
    )
    response = _compose_handoff_sections(
        intent_request,
        handoff_kind=_HANDOFF_KIND_SOURCE_SELECTION,
        resolver_version=TRANSIENT_COMPOSE_SELECTION_RESOLVER_VERSION,
        planning_sections=bridge.materialized_sections,
        trace_prefix=[
            ComposeFromIntentTraceStage(
                stage="source_catalog_resolution",
                details=bridge.catalog.to_trace_dict(),
            ),
            ComposeFromIntentTraceStage(
                stage="source_selection",
                details=bridge.selection.to_trace_dict(),
            ),
            ComposeFromIntentTraceStage(
                stage="section_materialization",
                details={
                    "selection_kind": "explicit",
                    "section_count": len(bridge.materialized_sections),
                    "sections": [
                        section.to_trace_dict() for section in bridge.materialized_sections
                    ],
                },
            ),
        ],
    )
    if isinstance(response, ComposeFromIntentResponse):
        response.persistable_compose_request = intent_request
    return response


def _compose_handoff_sections(
    request: ComposeFromIntentRequest,
    *,
    handoff_kind: str,
    resolver_version: str,
    planning_sections: Optional[list[CompositionMaterializedSection]] = None,
    trace_prefix: Optional[list[ComposeFromIntentTraceStage]] = None,
) -> ComposeFromIntentResponse:
    """Compose a transient page from a validated handoff of explicit prose sections."""

    _validate_request(request, handoff_kind=handoff_kind)

    trace_entries: list[ComposeFromIntentTraceStage] = list(trace_prefix or [])
    section_contexts = _build_planner_section_contexts(
        request,
        planning_sections=planning_sections,
    )
    page_plan = _plan_page_structure(request, section_contexts=section_contexts)
    section_contexts_by_index = {context.section_index: context for context in section_contexts}
    trace_entries.append(
        ComposeFromIntentTraceStage(
            stage="semantic_surface_matching",
            details={
                "sections": [
                    {
                        "section_index": row.section_index,
                        "engine_key": section_contexts_by_index[row.section_index].engine_key,
                        "title": section_contexts_by_index[row.section_index].title,
                        "source_family_key": row.source_family_key,
                        "composition_role_hint": section_contexts_by_index[row.section_index].composition_role_hint,
                        "semantic_role": row.semantic_role,
                        "pattern_key": row.pattern_key,
                        "inventory_listing": row.semantic_role == "inventory_listing",
                    }
                    for row in page_plan.leaf_rows
                ],
            },
        )
    )
    trace_entries.append(
        ComposeFromIntentTraceStage(
            stage="hierarchy_planning",
            details=_build_hierarchy_trace(page_plan),
        )
    )
    trace_entries.append(
        ComposeFromIntentTraceStage(
            stage="page_plan",
            details=_build_page_plan_trace(page_plan),
        )
    )

    executor = TransformationExecutor()
    generated_view_definitions: list[ViewDefinition] = []
    leaf_payloads: list[ViewPayload] = []
    generation_details: list[dict[str, Any]] = []
    transformation_details: list[dict[str, Any]] = []
    seen_view_keys: set[str] = set()
    parent_view_key = _build_parent_view_key(page_plan.parent) if page_plan.parent is not None else None

    for planner_position, row in enumerate(page_plan.leaf_rows):
        section = request.prose_sections[row.section_index]
        raw_generated_view = _generate_view_definition(
            planner_row=row,
            section=section,
            planner_position=planner_position,
            consumer_key=request.consumer_key,
            workflow_key=request.workflow_key,
        )
        normalized_view = _normalize_generated_view_definition(
            raw_view=raw_generated_view,
            planner_row=row,
            section=section,
            planner_position=planner_position,
            consumer_key=request.consumer_key,
            parent_view_key=parent_view_key,
        )
        if normalized_view.view_key in seen_view_keys:
            raise ComposeFromIntentUpstreamError(
                f"compose-from-intent generated a duplicate normalized view_key: {normalized_view.view_key}"
            )
        seen_view_keys.add(normalized_view.view_key)
        transformed_data, extraction_meta = _transform_section_prose(
            section=section,
            view_def=normalized_view,
            planner_row=row,
            executor=executor,
        )
        payload = _build_transient_payload(
            view_def=normalized_view,
            planner_row=row,
            section=section,
            planner_position=planner_position,
            transformed_data=transformed_data,
        )
        generated_view_definitions.append(normalized_view)
        leaf_payloads.append(payload)
        generation_details.append(
            {
                "view_key": normalized_view.view_key,
                "pattern_key": row.pattern_key,
                "renderer_type": normalized_view.renderer_type,
                "engine_key": section.engine_key,
                "parent_view_key": normalized_view.parent_view_key,
            }
        )
        transformation_details.append(extraction_meta)

    payloads = leaf_payloads
    if page_plan.parent is not None:
        parent_view = _build_parent_view_definition(
            parent=page_plan.parent,
            consumer_key=request.consumer_key,
            workflow_key=request.workflow_key,
        )
        parent_payload = _build_parent_transient_payload(
            view_def=parent_view,
            parent=page_plan.parent,
            child_rows=page_plan.leaf_rows,
            child_payloads=leaf_payloads,
        )
        generated_view_definitions = [parent_view, *generated_view_definitions]
        payloads = [parent_payload]
        generation_details.insert(
            0,
            {
                "view_key": parent_view.view_key,
                "pattern_key": page_plan.parent.pattern_key,
                "renderer_type": parent_view.renderer_type,
                "engine_key": None,
                "parent_view_key": None,
                "kind": "container",
            },
        )

    trace_entries.append(
        ComposeFromIntentTraceStage(
            stage="view_generation",
            details={"views": generation_details},
        )
    )
    trace_entries.append(
        ComposeFromIntentTraceStage(
            stage="transformation_execution",
            details={"views": transformation_details},
        )
    )

    adapted_payloads, adaptation_details = _adapt_payloads_for_consumer(
        payloads,
        consumer_key=request.consumer_key,
    )
    _normalize_transient_served_payloads(adapted_payloads)
    trace_entries.append(
        ComposeFromIntentTraceStage(
            stage="consumer_adaptation",
            details={"views": adaptation_details},
        )
    )

    enforce_final_payload_contracts_or_raise(
        adapted_payloads,
        composition_mode=None,
        served_intent=ServedIntent.TRANSIENT_COMPOSE_OUTPUT,
        workflow_key=request.workflow_key,
        consumer_key=request.consumer_key,
    )
    trace_entries.append(
        ComposeFromIntentTraceStage(
            stage="contract_validation",
            details={
                "view_count": _count_payload_tree(adapted_payloads),
                "issues": 0,
            },
        )
    )

    first_hop_affordance_enabled = _handoff_supports_first_hop_affordance(
        workflow_key=request.workflow_key,
        handoff_kind=handoff_kind,
    )
    transient_views = [
        _to_transient_view(
            payload,
            first_hop_affordance_enabled=first_hop_affordance_enabled,
        )
        for payload in adapted_payloads
    ]
    presentation = _build_transient_presentation(
        workflow_key=request.workflow_key,
        consumer_key=request.consumer_key,
        style_school=request.style_school or DEFAULT_STYLE_SCHOOL,
        views=transient_views,
        resolver_version=resolver_version,
    )

    return ComposeFromIntentResponse(
        presentation=presentation,
        generated_view_definitions=generated_view_definitions,
        trace=ComposeFromIntentTrace(
            resolver_version=resolver_version,
            entries=trace_entries,
        ),
    )


def _validate_handoff_capability(
    *,
    workflow_key: str,
    consumer_key: str,
    handoff_kind: str,
    route_label: str,
    profile: Optional[str] = None,
) -> None:
    error_message = get_transient_handoff_capability_error(
        workflow_key=workflow_key,
        consumer_key=consumer_key,
        handoff_kind=handoff_kind,
        route_label=route_label,
        profile=profile,
    )
    if error_message is not None:
        raise ComposeFromIntentClientError(error_message)


def get_transient_handoff_capability_error(
    *,
    workflow_key: str,
    consumer_key: str,
    handoff_kind: str,
    route_label: str,
    profile: Optional[str] = None,
) -> Optional[str]:
    supported_consumer_handoffs = _REGISTERED_TRANSIENT_CONSUMER_ADAPTERS.get(consumer_key)
    if supported_consumer_handoffs is None:
        return f"{route_label} only supports registered consumer adapters; got '{consumer_key}'"
    if handoff_kind not in supported_consumer_handoffs:
        return f"{route_label} does not support consumer_key='{consumer_key}' for handoff_kind='{handoff_kind}'"
    supported_handoffs = _SUPPORTED_HANDOFF_KINDS.get(workflow_key)
    if supported_handoffs is None or handoff_kind not in supported_handoffs:
        return f"{route_label} does not support workflow_key='{workflow_key}' for handoff_kind='{handoff_kind}'"
    if handoff_kind == _HANDOFF_KIND_SOURCE_PROFILE and profile is not None:
        supported_profiles = _REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER.get(consumer_key)
        if supported_profiles is None or profile not in supported_profiles:
            return f"{route_label} does not support consumer_key='{consumer_key}' for profile='{profile}'"
    return None


def _validate_request(request: ComposeFromIntentRequest, *, handoff_kind: str) -> None:
    _validate_handoff_capability(
        workflow_key=request.workflow_key,
        consumer_key=request.consumer_key,
        handoff_kind=handoff_kind,
        route_label="compose-from-intent",
    )
    if not request.user_intent.strip():
        raise ComposeFromIntentClientError("user_intent must not be empty")
    if not request.prose_sections:
        raise ComposeFromIntentClientError("prose_sections must contain at least one section")
    if len(request.prose_sections) > 4:
        raise ComposeFromIntentClientError("prose_sections may contain at most 4 sections")

    from src.engines.registry import get_engine_registry

    engine_registry = get_engine_registry()
    for index, section in enumerate(request.prose_sections):
        if not section.engine_key.strip():
            raise ComposeFromIntentClientError(f"prose_sections[{index}].engine_key must not be empty")
        if not section.title.strip():
            raise ComposeFromIntentClientError(f"prose_sections[{index}].title must not be empty")
        if not section.prose.strip():
            raise ComposeFromIntentClientError(f"prose_sections[{index}].prose must not be empty")
        if (
            engine_registry.get(section.engine_key) is None
            and engine_registry.get_capability_definition(section.engine_key) is None
        ):
            raise ComposeFromIntentClientError(
                f"Unknown engine_key in prose_sections[{index}]: {section.engine_key}"
            )

    _validate_optional_style_school(request.style_school)


def _validate_source_request(request: ComposeFromSourceRequest) -> None:
    _validate_handoff_capability(
        workflow_key=request.workflow_key,
        consumer_key=request.consumer_key,
        handoff_kind=_HANDOFF_KIND_SOURCE_PROFILE,
        route_label="compose-from-source",
        profile=request.profile,
    )
    if not request.source_v2_job_id.strip():
        raise ComposeFromIntentClientError("source_v2_job_id must not be empty")
    _validate_optional_style_school(request.style_school)


def _validate_selection_request(request: ComposeFromSelectionRequest) -> None:
    _validate_handoff_capability(
        workflow_key=request.workflow_key,
        consumer_key=request.consumer_key,
        handoff_kind=_HANDOFF_KIND_SOURCE_SELECTION,
        route_label="compose-from-selection",
    )
    if not request.source_v2_job_id.strip():
        raise ComposeFromIntentClientError("source_v2_job_id must not be empty")
    if not request.user_intent.strip():
        raise ComposeFromIntentClientError("user_intent must not be empty")
    if not request.selection:
        raise ComposeFromIntentClientError("selection must contain at least one source family")
    _validate_optional_style_school(request.style_school)


def _validate_optional_style_school(style_school: Optional[str]) -> None:
    if style_school is None:
        return
    try:
        school = StyleSchool(style_school)
    except ValueError as exc:
        raise ComposeFromIntentClientError(
            f"Unknown style_school: {style_school}"
        ) from exc
    if StyleRegistry().get_style(school) is None:
        raise ComposeFromIntentClientError(
            f"Style school is not available: {style_school}"
        )

def _build_planner_section_contexts(
    request: ComposeFromIntentRequest,
    *,
    planning_sections: Optional[list[CompositionMaterializedSection]] = None,
) -> list[_PlannerSectionContext]:
    if planning_sections is not None and len(planning_sections) != len(request.prose_sections):
        raise ComposeFromIntentUpstreamError(
            "compose-from-intent materialized section metadata did not match the request shape"
        )

    contexts: list[_PlannerSectionContext] = []
    for index, section in enumerate(request.prose_sections):
        materialized = planning_sections[index] if planning_sections is not None else None
        contexts.append(
            _PlannerSectionContext(
                section_index=index,
                engine_key=section.engine_key,
                title=section.title,
                prose=section.prose,
                source_family_key=materialized.source_family_key if materialized is not None else None,
                composition_role_hint=materialized.composition_role_hint if materialized is not None else None,
                profile=materialized.profile if materialized is not None else None,
                materialization_position=materialized.materialization_position if materialized is not None else None,
            )
        )
    return contexts


def _plan_page_structure(
    request: ComposeFromIntentRequest,
    *,
    section_contexts: list[_PlannerSectionContext],
) -> _SemanticPagePlan:
    planner_rows = [_match_section_to_planner_row(context) for context in section_contexts]
    planner_rows.sort(key=lambda row: _planner_row_sort_key(row, grouped=False))

    has_closeout = any(row.is_closeout for row in planner_rows)
    has_non_closeout = any(not row.is_closeout for row in planner_rows)
    if not has_closeout or not has_non_closeout:
        return _SemanticPagePlan(leaf_rows=tuple(planner_rows))

    grouped_rows = sorted(planner_rows, key=lambda row: _planner_row_sort_key(row, grouped=True))
    if request.workflow_key == AOI_WORKFLOW_KEY:
        parent_title = (
            "AOI Comparison"
            if any(row.semantic_role in _COMPARISON_PARENT_ROLES for row in grouped_rows)
            else "AOI Briefing"
        )
        parent_description = (
            "Tabbed AOI navigation that separates working analytical surfaces from the report closeout."
        )
    else:
        parent_title = (
            "Analytical Comparison"
            if any(row.semantic_role in _COMPARISON_PARENT_ROLES for row in grouped_rows)
            else "Analytical Briefing"
        )
        parent_description = (
            "Tabbed analytical navigation that separates working analytical surfaces from the report closeout."
        )
    parent = _PlannerParent(
        pattern_key="tab_with_children",
        view_name=parent_title,
        description=parent_description,
        presentation_stance="comparison"
        if parent_title == "AOI Comparison"
        or parent_title == "Analytical Comparison"
        else "summary",
        rationale=(
            "Grouped mixed working-content and closeout sections into a bounded tab shell."
        ),
    )
    return _SemanticPagePlan(leaf_rows=tuple(grouped_rows), parent=parent)


def _match_section_to_planner_row(context: _PlannerSectionContext) -> _PlannerRow:
    semantic_role = _resolve_semantic_role(context)
    role_spec = get_composition_role_spec(semantic_role)
    pattern_key = role_spec.pattern_key
    if pattern_key not in _ALLOWED_PATTERN_KEYS:
        raise ComposeFromIntentUpstreamError(
            f"compose-from-intent semantic matcher selected blocked pattern '{pattern_key}'"
        )

    title = context.title.strip()
    return _PlannerRow(
        section_index=context.section_index,
        pattern_key=pattern_key,
        view_name=title,
        description=f"{role_spec.description_prefix} for {title}.",
        presentation_stance=role_spec.presentation_stance,
        rationale=role_spec.rationale_prefix,
        semantic_role=semantic_role,
        source_family_key=context.source_family_key,
        profile=context.profile,
        materialization_position=context.materialization_position,
        is_closeout=semantic_role in _CLOSEOUT_ROLES,
    )


def _resolve_semantic_role(context: _PlannerSectionContext) -> str:
    role_hint = (context.composition_role_hint or "").strip()
    if role_hint in COMPOSITION_ROLE_HINTS:
        return role_hint

    from src.engines.registry import get_engine_registry

    cap_def = resolve_capability_definition(get_engine_registry(), context.engine_key)
    if cap_def is None and context.engine_key in _MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS:
        raise ComposeFromIntentUpstreamError(
            "compose-from-intent semantic matcher requires valid composition_role metadata "
            f"for migrated engine family '{context.engine_key}'"
        )
    if cap_def is not None:
        composition_role = getattr(cap_def, "composition_role", None)
        if cap_def.engine_key in _MIGRATED_COMPOSITION_ENGINE_FAMILIES:
            if not is_composition_role(composition_role):
                raise ComposeFromIntentUpstreamError(
                    "compose-from-intent semantic matcher requires valid composition_role metadata "
                    f"for migrated engine family '{context.engine_key}'"
                )
            return composition_role
        if is_composition_role(composition_role):
            return composition_role

    match_tokens = set(_tokenize_matcher_text(context.title)) | set(
        _tokenize_matcher_text(context.engine_key)
    )
    if match_tokens & _INVENTORY_LISTING_TOKENS:
        return "inventory_listing"

    for role, tokens in _TITLE_ROLE_HINTS:
        if match_tokens & tokens:
            return role

    raise ComposeFromIntentUpstreamError(
        "compose-from-intent semantic matcher could not assign an allowed leaf family "
        f"for section '{context.title}' ({context.engine_key})"
    )


def _tokenize_matcher_text(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _planner_row_sort_key(row: _PlannerRow, *, grouped: bool) -> tuple[int, int]:
    base_order = row.materialization_position or (row.section_index + 1)
    if not grouped:
        return (base_order, row.section_index)
    return (1 if row.is_closeout else 0, base_order)


def _build_hierarchy_trace(page_plan: _SemanticPagePlan) -> dict[str, Any]:
    if page_plan.parent is None:
        closeout_count = sum(1 for row in page_plan.leaf_rows if row.is_closeout)
        non_closeout_count = len(page_plan.leaf_rows) - closeout_count
        grouping_reason = (
            "flat_all_closeout"
            if closeout_count and not non_closeout_count
            else "flat_all_working_content"
        )
        return {
            "grouped": False,
            "grouping_reason": grouping_reason,
            "top_level_count": len(page_plan.leaf_rows),
            "leaf_count": len(page_plan.leaf_rows),
        }

    return {
        "grouped": True,
        "grouping_reason": "mixed_working_content_and_closeout",
        "top_level_count": 1,
        "leaf_count": len(page_plan.leaf_rows),
        "parent": {
            "pattern_key": page_plan.parent.pattern_key,
            "view_name": page_plan.parent.view_name,
            "presentation_stance": page_plan.parent.presentation_stance,
        },
    }


def _build_page_plan_trace(page_plan: _SemanticPagePlan) -> dict[str, Any]:
    if page_plan.parent is None:
        return {
            "top_level_count": len(page_plan.leaf_rows),
            "views": [
                {
                    "kind": "leaf",
                    "section_index": row.section_index,
                    "pattern_key": row.pattern_key,
                    "view_name": row.view_name,
                    "semantic_role": row.semantic_role,
                    "presentation_stance": row.presentation_stance,
                }
                for row in page_plan.leaf_rows
            ],
        }

    return {
        "top_level_count": 1,
        "views": [
            {
                "kind": "parent",
                "pattern_key": page_plan.parent.pattern_key,
                "view_name": page_plan.parent.view_name,
                "presentation_stance": page_plan.parent.presentation_stance,
                "children": [
                    {
                        "kind": "leaf",
                        "section_index": row.section_index,
                        "pattern_key": row.pattern_key,
                        "view_name": row.view_name,
                        "semantic_role": row.semantic_role,
                        "presentation_stance": row.presentation_stance,
                    }
                    for row in page_plan.leaf_rows
                ],
            }
        ],
    }


def _build_parent_view_key(parent: _PlannerParent) -> str:
    return f"compose_intent_parent_{_slugify(parent.view_name)}"


def _generate_view_definition(
    *,
    planner_row: _PlannerRow,
    section: Any,
    planner_position: int,
    consumer_key: str,
    workflow_key: str,
) -> ViewDefinition:
    request = ViewGenerateRequest(
        pattern_key=planner_row.pattern_key,
        engine_key=section.engine_key,
        workflow_key=workflow_key,
        target_app=consumer_key,
        target_page=TRANSIENT_COMPOSE_TARGET_PAGE,
        position=float(planner_position + 1),
        presentation_stance=planner_row.presentation_stance,
        description=planner_row.description,
        save=False,
    )
    try:
        response = asyncio.run(generate_view(request))
    except Exception as exc:
        _raise_if_dependency_unavailable(exc)
        raise ComposeFromIntentUpstreamError(
            f"compose-from-intent view generation failed for engine '{section.engine_key}': {exc}"
        ) from exc

    return response.view


def _normalize_generated_view_definition(
    *,
    raw_view: ViewDefinition,
    planner_row: _PlannerRow,
    section: Any,
    planner_position: int,
    consumer_key: str,
    parent_view_key: Optional[str] = None,
) -> ViewDefinition:
    pattern = get_pattern_registry().get(planner_row.pattern_key)
    if pattern is None:
        raise ComposeFromIntentUpstreamError(
            f"compose-from-intent pattern registry missing '{planner_row.pattern_key}'"
        )
    if pattern.renderer_type not in _ALLOWED_RENDERER_TYPES:
        raise ComposeFromIntentUpstreamError(
            f"compose-from-intent pattern '{planner_row.pattern_key}' resolved blocked renderer "
            f"'{pattern.renderer_type}'"
        )

    engine_key_slug = _slugify(section.engine_key)
    normalized_view = raw_view.model_copy(deep=True)
    normalized_view.view_key = f"compose_intent_{planner_position + 1:02d}_{engine_key_slug}"
    normalized_view.view_name = planner_row.view_name
    normalized_view.description = planner_row.description
    normalized_view.target_app = consumer_key
    normalized_view.target_page = TRANSIENT_COMPOSE_TARGET_PAGE
    normalized_view.renderer_type = pattern.renderer_type
    normalized_view.presentation_stance = planner_row.presentation_stance
    normalized_view.position = float(planner_position + 1)
    normalized_view.parent_view_key = parent_view_key
    normalized_view.visibility = "if_data_exists"
    normalized_view.status = "draft"
    normalized_view.generation_mode = "generated"
    normalized_view.source_project = "compose_from_intent_transient"

    if normalized_view.view_key != f"compose_intent_{planner_position + 1:02d}_{engine_key_slug}":
        raise ComposeFromIntentUpstreamError("compose-from-intent view key normalization failed")

    return normalized_view


def _transform_section_prose(
    *,
    section: Any,
    view_def: ViewDefinition,
    planner_row: _PlannerRow,
    executor: TransformationExecutor,
) -> tuple[Any, dict[str, Any]]:
    if view_def.renderer_type == "prose":
        view_def.transformation = TransformationSpec(type="none")
        return (
            section.prose,
            {
                "view_key": view_def.view_key,
                "engine_key": section.engine_key,
                "renderer_type": view_def.renderer_type,
                "extraction_source": "passthrough",
                "template_key": None,
            },
        )

    if planner_row.source_family_key is not None:
        preserved = _try_preserve_source_family_data(section.prose, view_def)
        if preserved is not None:
            return (
                preserved,
                {
                    "view_key": view_def.view_key,
                    "engine_key": section.engine_key,
                    "renderer_type": view_def.renderer_type,
                    "extraction_source": "source_family_preserved",
                    "template_key": None,
                    "source_family_key": planner_row.source_family_key,
                },
            )

    transformation_spec, extraction_source, template_key = _resolve_transformation_spec(
        view_def=view_def,
        planner_row=planner_row,
        engine_key=section.engine_key,
    )
    view_def.transformation = transformation_spec

    result = asyncio.run(
        executor.execute(
            data=section.prose,
            transformation_type=transformation_spec.type,
            field_mapping=transformation_spec.field_mapping,
            llm_extraction_schema=transformation_spec.llm_extraction_schema,
            llm_prompt_template=transformation_spec.llm_prompt_template,
            stance_key=transformation_spec.stance_key,
            cache_key=None,
        )
    )
    if not result.success:
        _raise_if_dependency_unavailable(RuntimeError(result.error or "unknown transformation failure"))
        raise ComposeFromIntentUpstreamError(
            f"compose-from-intent transformation failed for '{view_def.view_key}': {result.error}"
        )

    transformed_data = result.data
    return (
        transformed_data,
        {
            "view_key": view_def.view_key,
            "engine_key": section.engine_key,
            "renderer_type": view_def.renderer_type,
            "extraction_source": extraction_source,
            "template_key": template_key,
            "cached": result.cached,
        },
    )


def _resolve_transformation_spec(
    *,
    view_def: ViewDefinition,
    planner_row: _PlannerRow,
    engine_key: str,
) -> tuple[TransformationSpec, str, Optional[str]]:
    proxy_view = SimpleNamespace(
        data_source=SimpleNamespace(engine_key=engine_key, chain_key=None),
        renderer_type=view_def.renderer_type,
        transformation=SimpleNamespace(type="llm_extract"),
    )
    template = find_applicable_template(proxy_view, renderer_type=view_def.renderer_type)
    if template is not None and _is_transient_usable_template(template, view_def.renderer_type):
        return (
            TransformationSpec(
                type=template.transformation_type,
                field_mapping=template.field_mapping,
                llm_extraction_schema=template.llm_extraction_schema,
                llm_prompt_template=template.llm_prompt_template,
                stance_key=template.stance_key or planner_row.presentation_stance,
            ),
            "curated",
            template.template_key,
        )

    renderer = get_renderer_registry().get(view_def.renderer_type)
    if renderer is None or renderer.input_data_schema is None:
        raise ComposeFromIntentUpstreamError(
            f"compose-from-intent renderer metadata missing for '{view_def.renderer_type}'"
        )

    dynamic_config = _build_dynamic_transient_config(
        engine_key=engine_key,
        renderer_type=view_def.renderer_type,
        renderer_config=view_def.renderer_config,
        pattern_key=planner_row.pattern_key,
        stance_key=planner_row.presentation_stance,
        renderer_input_schema=renderer.input_data_schema,
    )
    return (
        TransformationSpec(
            type="llm_extract",
            llm_extraction_schema=renderer.input_data_schema,
            llm_prompt_template=str(dynamic_config["system_prompt"]),
            stance_key=planner_row.presentation_stance,
        ),
        "dynamic",
        None,
    )


def _build_dynamic_transient_config(
    *,
    engine_key: str,
    renderer_type: str,
    renderer_config: dict[str, Any],
    pattern_key: str,
    stance_key: Optional[str],
    renderer_input_schema: dict[str, Any],
) -> dict[str, Any]:
    config = compose_dynamic_extraction_prompt(
        engine_key=engine_key,
        renderer_type=renderer_type,
        stance_key=stance_key,
    )
    config_context = json.dumps(renderer_config, indent=2, ensure_ascii=False)
    schema_context = json.dumps(renderer_input_schema, indent=2, ensure_ascii=False)
    config["system_prompt"] = (
        f"{config['system_prompt']}\n\n"
        "## Transient Compose Context\n"
        f"Pattern key: {pattern_key}\n"
        "Use the final renderer configuration below when choosing field names and nesting.\n"
        f"Renderer config:\n{config_context}\n\n"
        "The following renderer input schema is prompt guidance for the target shape.\n"
        f"Input data schema:\n{schema_context}"
    )
    config["source"] = "compose_from_intent_dynamic"
    return config


def _try_preserve_source_family_data(
    prose: str,
    view_def: ViewDefinition,
) -> Optional[dict[str, Any]]:
    """Parse source-family JSON prose directly as structured data.

    When prose is already a serialized AOI artifact, preserving it avoids
    lossy LLM re-extraction and keeps the original structured keys intact.
    Returns None if the prose is not valid JSON or not a dict, in which
    case the caller falls through to normal LLM extraction.
    """
    try:
        parsed = json.loads(prose)
    except (json.JSONDecodeError, TypeError):
        return None
    if not isinstance(parsed, dict):
        return None

    view_def.transformation = TransformationSpec(type="none")
    _reconcile_renderer_config_with_data(view_def.renderer_config, parsed)
    return parsed


def _reconcile_renderer_config_with_data(
    renderer_config: Optional[dict[str, Any]],
    structured_data: dict[str, Any],
) -> None:
    """Remove section_renderers entries that reference keys missing from structured_data.

    This prevents contract enforcement from flagging section_renderers that were
    generated by the view pattern but don't match the actual preserved artifact
    keys.  It also prunes the ``sections`` list so declared sections stay
    consistent with section_renderers.
    """
    if not isinstance(renderer_config, dict):
        return

    section_renderers = renderer_config.get("section_renderers")
    if not isinstance(section_renderers, dict):
        return

    data_keys = set(structured_data.keys())
    stale_keys = [
        key for key in section_renderers
        if key != "_default" and key not in data_keys
    ]
    for key in stale_keys:
        del section_renderers[key]

    sections = renderer_config.get("sections")
    if isinstance(sections, list):
        renderer_config["sections"] = [
            section for section in sections
            if not isinstance(section, dict)
            or section.get("key") in data_keys
            or section.get("key") in section_renderers
        ]


def _build_transient_payload(
    *,
    view_def: ViewDefinition,
    planner_row: _PlannerRow,
    section: Any,
    planner_position: int,
    transformed_data: Any,
) -> ViewPayload:
    return ViewPayload(
        view_key=view_def.view_key,
        view_name=view_def.view_name,
        description=view_def.description,
        renderer_type=view_def.renderer_type,
        renderer_config=view_def.renderer_config,
        presentation_stance=view_def.presentation_stance,
        priority="primary",
        rationale=planner_row.rationale,
        data_quality="generated",
        top_level_group=None,
        source_parent_view_key=view_def.parent_view_key,
        promoted_to_top_level=False,
        selection_priority="primary",
        navigation_state="normal",
        structuring_policy=None,
        semantic_scaffold_type=None,
        scaffold_hosting_mode=None,
        derivation_kind="compose_from_intent_transient",
        phase_number=None,
        engine_key=section.engine_key,
        chain_key=None,
        scope="aggregated",
        has_structured_data=transformed_data is not None,
        structured_data=transformed_data,
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=None,
        tab_count=None,
        visibility=view_def.visibility,
        position=view_def.position,
        children=[],
    )


def _build_parent_view_definition(
    *,
    parent: _PlannerParent,
    consumer_key: str,
    workflow_key: str,
) -> ViewDefinition:
    return ViewDefinition(
        view_key=_build_parent_view_key(parent),
        view_name=parent.view_name,
        description=parent.description,
        target_app=consumer_key,
        target_page=TRANSIENT_COMPOSE_TARGET_PAGE,
        renderer_type="tab",
        renderer_config={
            "tab_style": "underline",
            "default_tab": 0,
            "show_count_badges": False,
        },
        data_source=DataSourceRef(
            workflow_key=workflow_key,
            phase_number=1.0,
            engine_key=None,
            chain_key=None,
            result_path="compose_from_intent_transient.parent",
            scope="aggregated",
        ),
        transformation=TransformationSpec(type="none"),
        presentation_stance=parent.presentation_stance,
        position=1.0,
        parent_view_key=None,
        child_display_mode="deep_dives",
        visibility="if_data_exists",
        status="draft",
        source_project="compose_from_intent_transient",
        generation_mode="generated",
        planner_hint="",
        planner_eligible=False,
        audience_overrides={},
    )


def _build_parent_transient_payload(
    *,
    view_def: ViewDefinition,
    parent: _PlannerParent,
    child_rows: tuple[_PlannerRow, ...],
    child_payloads: list[ViewPayload],
) -> ViewPayload:
    ordered_children = [child.model_copy(deep=True) for child in child_payloads]
    return ViewPayload(
        view_key=view_def.view_key,
        view_name=view_def.view_name,
        description=view_def.description,
        renderer_type=view_def.renderer_type,
        renderer_config=view_def.renderer_config,
        presentation_stance=view_def.presentation_stance,
        priority="primary",
        rationale=parent.rationale,
        data_quality="generated",
        top_level_group=None,
        source_parent_view_key=None,
        promoted_to_top_level=False,
        selection_priority="primary",
        navigation_state="normal",
        structuring_policy=None,
        semantic_scaffold_type=None,
        scaffold_hosting_mode=None,
        derivation_kind="compose_from_intent_transient",
        phase_number=None,
        engine_key=None,
        chain_key=None,
        scope="aggregated",
        has_structured_data=True,
        structured_data=_build_parent_tab_structured_data(
            child_rows=child_rows,
            child_payloads=ordered_children,
        ),
        reading_scaffold=None,
        raw_prose=None,
        prose_ref_view_key=None,
        items=None,
        tab_count=len(ordered_children),
        visibility=view_def.visibility,
        position=view_def.position,
        children=ordered_children,
    )


def _build_parent_tab_structured_data(
    *,
    child_rows: tuple[_PlannerRow, ...],
    child_payloads: list[ViewPayload],
) -> dict[str, Any]:
    entries: dict[str, Any] = {}
    for position, (row, payload) in enumerate(zip(child_rows, child_payloads, strict=True), start=1):
        entries[payload.view_key] = {
            "label": payload.view_name,
            "description": payload.description,
            "semantic_role": row.semantic_role,
            "position": position,
        }
    return entries


def _adapt_payloads_for_consumer(
    payloads: list[ViewPayload],
    *,
    consumer_key: str,
) -> tuple[list[ViewPayload], list[dict[str, Any]]]:
    adapted_payloads: list[ViewPayload] = []
    adaptation_details: list[dict[str, Any]] = []

    for payload in payloads:
        adapted_payloads.append(
            _adapt_payload_for_consumer(
                payload,
                consumer_key=consumer_key,
                adaptation_details=adaptation_details,
            )
        )

    return adapted_payloads, adaptation_details


def _adapt_payload_for_consumer(
    payload: ViewPayload,
    *,
    consumer_key: str,
    adaptation_details: list[dict[str, Any]],
) -> ViewPayload:
    copied = payload.model_copy(deep=True)
    served_renderer_type, served_renderer_config, adaptation = adapt_renderer_for_consumer(
        renderer_type=copied.renderer_type,
        renderer_config=copied.renderer_config,
        consumer_key=consumer_key,
    )
    copied.renderer_type = served_renderer_type
    copied.renderer_config = served_renderer_config
    copied.children = [
        _adapt_payload_for_consumer(
            child,
            consumer_key=consumer_key,
            adaptation_details=adaptation_details,
        )
        for child in copied.children
    ]
    adaptation_details.append(
        {
            "view_key": copied.view_key,
            "renderer_type": served_renderer_type,
            "adapted": adaptation is not None,
        }
    )
    return copied


def _handoff_supports_first_hop_affordance(*, workflow_key: str, handoff_kind: str) -> bool:
    return (workflow_key, handoff_kind) in _FIRST_HOP_AFFORDANCE_ELIGIBLE_HANDOFFS


def _to_transient_view(
    payload: ViewPayload,
    *,
    first_hop_affordance_enabled: bool,
) -> TransientIntentView:
    return TransientIntentView(
        view_key=payload.view_key,
        view_name=payload.view_name,
        description=payload.description,
        renderer_type=payload.renderer_type,
        renderer_config=payload.renderer_config,
        presentation_stance=payload.presentation_stance,
        rationale=payload.rationale,
        engine_key=payload.engine_key,
        position=payload.position,
        visibility=payload.visibility,
        has_structured_data=payload.has_structured_data,
        structured_data=payload.structured_data,
        items=payload.items,
        first_hop_affordance=_derive_first_hop_affordance(
            payload,
            first_hop_affordance_enabled=first_hop_affordance_enabled,
        ),
        children=[
            _to_transient_view(
                child,
                first_hop_affordance_enabled=first_hop_affordance_enabled,
            )
            for child in payload.children
        ],
    )


def _derive_first_hop_affordance(
    payload: ViewPayload,
    *,
    first_hop_affordance_enabled: bool,
) -> FirstHopAffordance | None:
    return derive_first_hop_affordance(
        payload,
        enabled=first_hop_affordance_enabled,
    )


def _normalize_transient_served_payloads(payloads: list[ViewPayload]) -> None:
    for payload in payloads:
        _normalize_transient_served_payload(payload)


def _normalize_transient_served_payload(payload: ViewPayload) -> None:
    if payload.renderer_type == "card_grid":
        normalized = _normalize_card_grid_contract_shape(
            structured_data=payload.structured_data,
            renderer_config=payload.renderer_config,
        )
        if normalized is not None:
            payload.structured_data = normalized["structured_data"]
            payload.has_structured_data = payload.structured_data is not None
            payload.renderer_config = normalized["renderer_config"]
    for child in payload.children:
        _normalize_transient_served_payload(child)


def _normalize_card_grid_contract_shape(
    *,
    structured_data: Any,
    renderer_config: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not isinstance(renderer_config, dict):
        return None

    source = structured_data
    items_path = renderer_config.get("items_path")
    if isinstance(items_path, str) and items_path:
        resolved = _get_path(structured_data, items_path)
        if resolved is not None:
            source = resolved

    normalized_data: Any | None = None
    if isinstance(source, list):
        normalized_data = source
    elif isinstance(source, dict):
        array_groups = {
            key: value
            for key, value in source.items()
            if isinstance(value, list)
            and all(isinstance(item, dict) for item in value)
        }
        if array_groups:
            normalized_data = array_groups

    if normalized_data is None:
        return None

    normalized_config = dict(renderer_config)
    normalized_config.pop("items_path", None)
    if isinstance(normalized_data, dict) and len(normalized_data) > 1:
        normalized_config["group_by"] = "_category"

    return {
        "structured_data": normalized_data,
        "renderer_config": normalized_config,
    }


def _build_transient_presentation(
    *,
    workflow_key: str,
    consumer_key: str,
    style_school: str,
    views: list[TransientIntentView],
    resolver_version: str,
) -> TransientIntentPagePresentation:
    ordered_views = sorted(views, key=lambda view: (view.position, view.view_key))
    contract_manifest = {
        "workflow_key": workflow_key,
        "consumer_key": consumer_key,
        "resolver_version": resolver_version,
        "style_school": style_school,
        "views": [_transient_identity_row(view) for view in ordered_views],
    }
    content_manifest = {
        "workflow_key": workflow_key,
        "consumer_key": consumer_key,
        "views": [_transient_content_row(view) for view in ordered_views],
    }
    return TransientIntentPagePresentation(
        workflow_key=workflow_key,
        consumer_key=consumer_key,
        presentation_contract_version=TRANSIENT_PRESENTATION_CONTRACT_VERSION,
        presentation_hash=_stable_fingerprint(contract_manifest),
        presentation_content_hash=_stable_fingerprint(content_manifest),
        resolver_version=resolver_version,
        style_school=style_school,
        views=ordered_views,
        view_count=_count_view_tree(ordered_views),
    )


def _transient_identity_row(view: TransientIntentView) -> dict[str, Any]:
    return {
        "view_key": view.view_key,
        "renderer_type": view.renderer_type,
        "renderer_config": view.renderer_config,
        "presentation_stance": view.presentation_stance,
        "position": view.position,
        "visibility": view.visibility,
        "first_hop_affordance": (
            view.first_hop_affordance.model_dump(mode="json", exclude_none=True)
            if view.first_hop_affordance is not None
            else None
        ),
        "children": [_transient_identity_row(child) for child in view.children],
    }


def _transient_content_row(view: TransientIntentView) -> dict[str, Any]:
    return {
        "view_key": view.view_key,
        "structured_data": view.structured_data,
        "items": view.items,
        "children": [_transient_content_row(child) for child in view.children],
    }


def _count_view_tree(views: list[TransientIntentView]) -> int:
    return sum(1 + _count_view_tree(view.children) for view in views)


def _count_payload_tree(payloads: list[ViewPayload]) -> int:
    return sum(1 + _count_payload_tree(payload.children) for payload in payloads)


def _stable_fingerprint(value: Any) -> str:
    serialized = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    import hashlib

    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _stable_json_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def _truncate_for_planner(prose: str, *, max_chars: int = 4000) -> str:
    text = prose.strip()
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars].rsplit(" ", 1)[0].rstrip()
    return f"{truncated}..."


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "section"


def _is_transient_usable_template(template: Any, renderer_type: str) -> bool:
    if getattr(template, "transformation_type", "") != "none":
        return True
    return renderer_type == "prose"


def _get_path(obj: Any, path: str) -> Any:
    current = obj
    for segment in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(segment)
    return current


def _call_llm_or_raise(
    *,
    prompt: str,
    system_prompt: str,
    model: str,
    fallback_model: str,
    max_tokens: int,
) -> tuple[str, str, int]:
    try:
        return call_extraction_model(
            prompt=prompt,
            system_prompt=system_prompt,
            model=model,
            fallback_model=fallback_model,
            max_tokens=max_tokens,
        )
    except Exception as exc:
        if _is_dependency_unavailable(exc):
            raise ComposeFromIntentDependencyUnavailable(
                _dependency_unavailable_message(exc)
            ) from exc
        raise ComposeFromIntentUpstreamError(str(exc)) from exc


def _is_dependency_unavailable(exc: BaseException) -> bool:
    dependency_exception_names = {
        "APIConnectionError",
        "APITimeoutError",
        "InternalServerError",
        "ConnectError",
        "ConnectTimeout",
        "ReadTimeout",
        "PoolTimeout",
        "RemoteProtocolError",
    }
    dependency_message_markers = (
        "LLM service unavailable",
        "ANTHROPIC_API_KEY",
        "anthropic library not installed",
    )

    for candidate in _exception_chain(exc):
        message = str(candidate)
        if any(marker in message for marker in dependency_message_markers):
            return True
        if candidate.__class__.__name__ in dependency_exception_names:
            return True

    return False


def _dependency_unavailable_message(exc: BaseException) -> str:
    for candidate in _exception_chain(exc):
        message = str(candidate).strip()
        if not message:
            continue
        if (
            "LLM service unavailable" in message
            or "ANTHROPIC_API_KEY" in message
            or "anthropic library not installed" in message
        ):
            return message
        if _is_dependency_unavailable(candidate):
            return message
    return str(exc)


def _exception_chain(exc: BaseException) -> list[BaseException]:
    chain: list[BaseException] = []
    seen: set[int] = set()
    current: BaseException | None = exc

    while current is not None and id(current) not in seen:
        chain.append(current)
        seen.add(id(current))
        current = current.__cause__ or current.__context__

    return chain
