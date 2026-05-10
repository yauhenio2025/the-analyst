"""Serve-time renderer contract enforcement for served presenter payloads."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Optional

from jsonschema import Draft7Validator

from src.consumers.registry import get_consumer_registry
from src.renderers.registry import get_renderer_registry
from src.renderers.validator import validate_renderer_config, validate_renderer_data
from src.sub_renderers.registry import get_sub_renderer_registry

from .bounded_dynamic_composition import (
    BoundedCompositionValidationError,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
    COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
    COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
    COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
    COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
    COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
)
from .schemas import CompositionIssue, ViewPayload

logger = logging.getLogger(__name__)

NESTED_SECTIONS_RENDERER = "nested_sections"
POLICY_STRICT = "strict"
POLICY_SHADOW = "shadow"
POLICY_WARN = "warn"


class ServedIntent(str, Enum):
    """Internal presentation intent used to decide final serve-time enforcement."""

    TRANSIENT_COMPOSE_OUTPUT = "transient_compose_output"
    EFFECTIVE_MANIFEST_SERVED = "effective_manifest_served"
    FULL_PAGE_PRESENTATION_SERVED = "full_page_presentation_served"
    SINGLE_VIEW_PRESENTATION_SERVED = "single_view_presentation_served"
    MANIFEST_INSPECTION_FOR_STATUS = "manifest_inspection_for_status"
    MANIFEST_INSPECTION_FOR_TRACE = "manifest_inspection_for_trace"
    MANIFEST_PREVIEW_FOR_DISCOVERY = "manifest_preview_for_discovery"
    VIEW_SOURCE_FOR_POLISH = "view_source_for_polish"
    PAGE_SOURCE_FOR_DELIVERY_STYLE = "page_source_for_delivery_style"
    VIEW_SOURCE_FOR_DELIVERY_STYLE = "view_source_for_delivery_style"
    PAGE_SOURCE_FOR_SCAFFOLD_GENERATION = "page_source_for_scaffold_generation"
    VIEW_SOURCE_FOR_VARIANT_GENERATION = "view_source_for_variant_generation"
    PAGE_PREVIEW_FOR_ORCHESTRATOR_STATUS = "page_preview_for_orchestrator_status"


@dataclass(frozen=True)
class ServedRendererContractPolicy:
    """Resolved final-boundary enforcement policy for one served artifact."""

    mode: str
    served_intent: ServedIntent
    coverage_key: str
    reason: str


_EXTERNAL_SERVED_INTENTS = frozenset(
    {
        ServedIntent.TRANSIENT_COMPOSE_OUTPUT,
        ServedIntent.EFFECTIVE_MANIFEST_SERVED,
        ServedIntent.FULL_PAGE_PRESENTATION_SERVED,
        ServedIntent.SINGLE_VIEW_PRESENTATION_SERVED,
    }
)
_INSPECTION_SUPPORT_INTENTS = frozenset(
    {
        ServedIntent.MANIFEST_INSPECTION_FOR_STATUS,
        ServedIntent.MANIFEST_INSPECTION_FOR_TRACE,
        ServedIntent.MANIFEST_PREVIEW_FOR_DISCOVERY,
        ServedIntent.VIEW_SOURCE_FOR_POLISH,
        ServedIntent.PAGE_SOURCE_FOR_DELIVERY_STYLE,
        ServedIntent.VIEW_SOURCE_FOR_DELIVERY_STYLE,
        ServedIntent.PAGE_SOURCE_FOR_SCAFFOLD_GENERATION,
        ServedIntent.VIEW_SOURCE_FOR_VARIANT_GENERATION,
        ServedIntent.PAGE_PREVIEW_FOR_ORCHESTRATOR_STATUS,
    }
)
_STRICT_AOI_COMPOSITION_MODES = frozenset(
    {
        COMPOSITION_MODE_ADAPTIVE_AOI_THEME_SURFACE_V1,
        COMPOSITION_MODE_ADAPTIVE_AOI_THEME_REPORT_SUITE_V1,
    }
)
_STRICT_GENEALOGY_COMPOSITION_MODES = frozenset(
    {
        COMPOSITION_MODE_DECLARATIVE_RELATIONSHIP_SURFACE_V1,
    }
)
_SHADOW_GENEALOGY_COMPOSITION_MODES = frozenset(
    {
        COMPOSITION_MODE_ADAPTIVE_RELATIONSHIP_SURFACE_V1,
        COMPOSITION_MODE_ADAPTIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_V1,
        COMPOSITION_MODE_DECLARATIVE_GENEALOGY_RELATIONSHIP_CONDITIONS_SUITE_V1,
        "bounded_dynamic_genealogy_v1",
    }
)


def resolve_served_renderer_contract_policy(
    *,
    served_intent: ServedIntent,
    workflow_key: str,
    consumer_key: str,
    composition_mode: Optional[str],
) -> ServedRendererContractPolicy:
    """Resolve strict/shadow/warn policy for one served artifact."""

    coverage_key = (
        f"{served_intent.value}:{workflow_key or 'unknown'}:{consumer_key or 'unknown'}:"
        f"{composition_mode or 'authored'}"
    )

    if served_intent in _INSPECTION_SUPPORT_INTENTS:
        return ServedRendererContractPolicy(
            mode=POLICY_WARN,
            served_intent=served_intent,
            coverage_key=coverage_key,
            reason="inspection_or_support_intent_is_non_strict",
        )

    if served_intent == ServedIntent.TRANSIENT_COMPOSE_OUTPUT:
        return ServedRendererContractPolicy(
            mode=POLICY_STRICT,
            served_intent=served_intent,
            coverage_key=coverage_key,
            reason="transient_compose_output_is_always_strict",
        )

    if served_intent not in _EXTERNAL_SERVED_INTENTS:
        return ServedRendererContractPolicy(
            mode=POLICY_WARN,
            served_intent=served_intent,
            coverage_key=coverage_key,
            reason="unlisted_served_intent_defaults_to_warn",
        )

    if composition_mode in _STRICT_AOI_COMPOSITION_MODES:
        return ServedRendererContractPolicy(
            mode=POLICY_STRICT,
            served_intent=served_intent,
            coverage_key=coverage_key,
            reason="strict_aoi_served_surface",
        )

    if composition_mode in _STRICT_GENEALOGY_COMPOSITION_MODES:
        return ServedRendererContractPolicy(
            mode=POLICY_STRICT,
            served_intent=served_intent,
            coverage_key=coverage_key,
            reason="strict_genealogy_served_surface",
        )

    if composition_mode in _SHADOW_GENEALOGY_COMPOSITION_MODES:
        return ServedRendererContractPolicy(
            mode=POLICY_SHADOW,
            served_intent=served_intent,
            coverage_key=coverage_key,
            reason="shadow_genealogy_served_surface",
        )

    return ServedRendererContractPolicy(
        mode=POLICY_WARN,
        served_intent=served_intent,
        coverage_key=coverage_key,
        reason="authored_or_unlisted_combination_warn_only",
    )


def is_renderer_contract_enforced_mode(composition_mode: Optional[str]) -> bool:
    """Back-compat check for strict manifest/page/view served surfaces."""

    policy = resolve_served_renderer_contract_policy(
        served_intent=ServedIntent.FULL_PAGE_PRESENTATION_SERVED,
        workflow_key="",
        consumer_key="the-critic",
        composition_mode=composition_mode,
    )
    return policy.mode == POLICY_STRICT


def enforce_final_payload_contract_or_raise(
    payload: ViewPayload,
    *,
    composition_mode: Optional[str],
    served_intent: ServedIntent = ServedIntent.FULL_PAGE_PRESENTATION_SERVED,
    workflow_key: str = "",
    consumer_key: str = "",
) -> list[CompositionIssue]:
    return enforce_final_payload_contracts_or_raise(
        [payload],
        composition_mode=composition_mode,
        served_intent=served_intent,
        workflow_key=workflow_key,
        consumer_key=consumer_key,
    )


def enforce_payload_contract_or_raise(payload: ViewPayload) -> None:
    enforce_payload_contracts_or_raise([payload])


def enforce_final_payload_contracts_or_raise(
    payloads: Iterable[ViewPayload],
    *,
    composition_mode: Optional[str],
    served_intent: ServedIntent = ServedIntent.FULL_PAGE_PRESENTATION_SERVED,
    workflow_key: str = "",
    consumer_key: str = "",
) -> list[CompositionIssue]:
    """Apply strict/shadow/warn final-boundary enforcement for served payloads."""

    policy = resolve_served_renderer_contract_policy(
        served_intent=served_intent,
        workflow_key=workflow_key,
        consumer_key=consumer_key,
        composition_mode=composition_mode,
    )
    issues = collect_served_payload_contract_issues(
        payloads,
        consumer_key=consumer_key,
    )
    if not issues:
        return []

    if policy.mode == POLICY_STRICT:
        raise BoundedCompositionValidationError(issues)

    if policy.mode == POLICY_SHADOW:
        logger.warning(
            "served_renderer_contract_shadow_issues coverage=%s issues=%s",
            policy.coverage_key,
            [issue.model_dump() for issue in issues],
        )

    return issues


def enforce_payload_contracts_or_raise(
    payloads: Iterable[ViewPayload],
) -> None:
    """Strict recursive contract validation without policy resolution."""

    issues = collect_served_payload_contract_issues(payloads, consumer_key="")
    if issues:
        raise BoundedCompositionValidationError(issues)


def collect_served_payload_contract_issues(
    payloads: Iterable[ViewPayload],
    *,
    consumer_key: str,
) -> list[CompositionIssue]:
    issues: list[CompositionIssue] = []
    for payload in _iter_payload_tree(payloads):
        issues.extend(_collect_renderer_contract_issues(payload))
        issues.extend(
            _collect_container_contract_issues(
                payload,
                consumer_key=consumer_key,
            )
        )
    return issues


def _iter_payload_tree(payloads: Iterable[ViewPayload]) -> Iterable[ViewPayload]:
    seen: set[str] = set()

    def _walk(nodes: Iterable[ViewPayload]) -> Iterable[ViewPayload]:
        for payload in nodes:
            if payload.view_key in seen:
                continue
            seen.add(payload.view_key)
            yield payload
            if payload.children:
                yield from _walk(payload.children)

    yield from _walk(payloads)


def _collect_renderer_contract_issues(payload: ViewPayload) -> list[CompositionIssue]:
    renderer = get_renderer_registry().get(payload.renderer_type)
    if renderer is None or renderer.config_schema is None or renderer.input_data_schema is None:
        return [
            CompositionIssue(
                view_key=payload.view_key,
                field="renderer_type",
                message=(
                    f"Renderer contract is missing for served renderer "
                    f"'{payload.renderer_type}'."
                ),
                reason="renderer_definition_missing",
            )
        ]

    issues: list[CompositionIssue] = []

    config_validation = validate_renderer_config(
        renderer_key=payload.renderer_type,
        config=payload.renderer_config,
    )
    if not config_validation.schema_available:
        return [
            CompositionIssue(
                view_key=payload.view_key,
                field="renderer_type",
                message=(
                    f"Renderer contract is missing for served renderer "
                    f"'{payload.renderer_type}'."
                ),
                reason="renderer_definition_missing",
            )
        ]
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

    if _should_validate_structured_data(payload):
        data_validation = validate_renderer_data(
            renderer_key=payload.renderer_type,
            data=payload.structured_data,
            renderer_config=payload.renderer_config,
        )
        if not data_validation.schema_available:
            return [
                CompositionIssue(
                    view_key=payload.view_key,
                    field="renderer_type",
                    message=(
                        f"Renderer contract is missing for served renderer "
                        f"'{payload.renderer_type}'."
                    ),
                    reason="renderer_definition_missing",
                )
            ]
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


def _collect_container_contract_issues(
    payload: ViewPayload,
    *,
    consumer_key: str,
) -> list[CompositionIssue]:
    if payload.renderer_type == "tab":
        return _collect_tab_container_issues(payload)

    renderer = get_renderer_registry().get(payload.renderer_type)
    if renderer is None:
        return []

    section_renderers = (payload.renderer_config or {}).get("section_renderers")
    if not isinstance(section_renderers, dict):
        return []

    declared_sections = _declared_section_keys(payload.renderer_config)
    structured_data = payload.structured_data if isinstance(payload.structured_data, dict) else None
    issues: list[CompositionIssue] = []
    for section_key, spec in section_renderers.items():
        issues.extend(
            _collect_section_renderer_spec_issues(
                payload=payload,
                consumer_key=consumer_key,
                parent_renderer_type=payload.renderer_type,
                parent_allowed_section_renderers=set(renderer.available_section_renderers or []),
                section_key=section_key,
                spec=spec,
                declared_sections=declared_sections,
                section_data=structured_data.get(section_key) if structured_data and section_key != "_default" else structured_data,
                skip_section_alignment=(section_key == "_default"),
            )
        )
    return issues


def _collect_tab_container_issues(payload: ViewPayload) -> list[CompositionIssue]:
    if not payload.children:
        return []

    if payload.structured_data is None and not payload.has_structured_data:
        return []

    if not isinstance(payload.structured_data, dict):
        return [
            CompositionIssue(
                view_key=payload.view_key,
                field="structured_data",
                message="Tab container payload must carry structured_data aligned to child views.",
                reason="tab_child_alignment_missing_structured_data",
            )
        ]

    expected_child_keys = [child.view_key for child in payload.children]
    declared_section_keys = _ordered_declared_section_keys(payload.renderer_config)
    actual_child_keys = list(payload.structured_data.keys())
    keys_align_to_children = actual_child_keys == expected_child_keys
    keys_align_to_sections = bool(declared_section_keys) and actual_child_keys == declared_section_keys
    section_child_count_aligned = not declared_section_keys or len(declared_section_keys) == len(payload.children)
    if not ((keys_align_to_children or keys_align_to_sections) and section_child_count_aligned):
        return [
            CompositionIssue(
                view_key=payload.view_key,
                field="structured_data",
                message=(
                    "Tab container structured_data keys must align to child views or declared tab "
                    f"sections (child keys {expected_child_keys}, section keys {declared_section_keys}, "
                    f"found {actual_child_keys})."
                ),
                reason="tab_child_alignment_mismatch",
            )
        ]
    return []


def _collect_section_renderer_spec_issues(
    *,
    payload: ViewPayload,
    consumer_key: str,
    parent_renderer_type: str,
    parent_allowed_section_renderers: set[str],
    section_key: str,
    spec: Any,
    declared_sections: set[str],
    section_data: Any,
    skip_section_alignment: bool = False,
) -> list[CompositionIssue]:
    issues: list[CompositionIssue] = []
    field_prefix = f"renderer_config.section_renderers.{section_key}"

    if not skip_section_alignment and section_key != "_default" and section_key not in declared_sections:
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=field_prefix,
                message=f"Section renderer references undeclared section '{section_key}'.",
                reason="section_renderer_unknown_section_key",
            )
        )
    if (
        not skip_section_alignment
        and section_key != "_default"
        and isinstance(payload.structured_data, dict)
        and section_key not in payload.structured_data
    ):
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=field_prefix,
                message=f"Section renderer references missing structured_data key '{section_key}'.",
                reason="section_renderer_missing_structured_data_key",
            )
        )

    if not isinstance(spec, dict):
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=field_prefix,
                message="Section renderer spec must be an object.",
                reason="section_renderer_spec_not_object",
            )
        )
        return issues

    renderer_type = spec.get("renderer_type")
    if not isinstance(renderer_type, str) or not renderer_type:
        config = spec.get("config")
        top_level_sub_renderers = spec.get("sub_renderers")
        nested_sub_renderers = config.get("sub_renderers") if isinstance(config, dict) else None
        if isinstance(top_level_sub_renderers, dict) or isinstance(nested_sub_renderers, dict):
            renderer_type = NESTED_SECTIONS_RENDERER
    if not isinstance(renderer_type, str) or not renderer_type:
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=f"{field_prefix}.renderer_type",
                message="Section renderer spec must declare a renderer_type.",
                reason="missing_section_renderer_type",
            )
        )
        return issues

    if renderer_type == NESTED_SECTIONS_RENDERER:
        issues.extend(
            _collect_nested_sections_issues(
                payload=payload,
                consumer_key=consumer_key,
                field_prefix=field_prefix,
                parent_renderer_type=parent_renderer_type,
                parent_allowed_section_renderers=parent_allowed_section_renderers,
                spec=spec,
                section_data=section_data,
                is_default_spec=skip_section_alignment,
            )
        )
        return issues

    sub_renderer = get_sub_renderer_registry().get(renderer_type)
    if sub_renderer is None:
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=f"{field_prefix}.renderer_type",
                message=f"Section renderer '{renderer_type}' is not defined.",
                reason="sub_renderer_definition_missing",
            )
        )
        return issues

    if parent_renderer_type not in (sub_renderer.parent_renderer_types or []):
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=f"{field_prefix}.renderer_type",
                message=(
                    f"Section renderer '{renderer_type}' is not allowed for parent "
                    f"renderer '{parent_renderer_type}'."
                ),
                reason="sub_renderer_not_allowed_for_parent",
            )
        )
    if (
        parent_allowed_section_renderers
        and renderer_type not in parent_allowed_section_renderers
        and renderer_type != NESTED_SECTIONS_RENDERER
    ):
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=f"{field_prefix}.renderer_type",
                message=(
                    f"Section renderer '{renderer_type}' is not declared in parent renderer "
                    f"'{parent_renderer_type}' available_section_renderers."
                ),
                reason="sub_renderer_not_declared_for_parent",
            )
        )
    if not _consumer_supports_sub_renderer(
        consumer_key=consumer_key,
        renderer_type=renderer_type,
    ):
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=f"{field_prefix}.renderer_type",
                message=(
                    f"Section renderer '{renderer_type}' is not supported by consumer "
                    f"'{consumer_key}'."
                ),
                reason="sub_renderer_not_supported_by_consumer",
            )
        )

    issues.extend(
        _collect_sub_renderer_config_issues(
            view_key=payload.view_key,
            renderer_type=renderer_type,
            config=spec.get("config") or {},
            field_prefix=f"{field_prefix}.config",
        )
    )
    return issues


def _collect_nested_sections_issues(
    *,
    payload: ViewPayload,
    consumer_key: str,
    field_prefix: str,
    parent_renderer_type: str,
    parent_allowed_section_renderers: set[str],
    spec: dict[str, Any],
    section_data: Any,
    is_default_spec: bool,
) -> list[CompositionIssue]:
    issues: list[CompositionIssue] = []
    nested_definition = get_sub_renderer_registry().get(NESTED_SECTIONS_RENDERER)
    if nested_definition is None:
        return [
            CompositionIssue(
                view_key=payload.view_key,
                field=f"{field_prefix}.renderer_type",
                message="Nested sections renderer contract is missing.",
                reason="sub_renderer_definition_missing",
            )
        ]

    if parent_renderer_type not in (nested_definition.parent_renderer_types or []):
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=f"{field_prefix}.renderer_type",
                message=(
                    "Nested sections renderer is not allowed for parent "
                    f"renderer '{parent_renderer_type}'."
                ),
                reason="sub_renderer_not_allowed_for_parent",
            )
        )
    if not _consumer_supports_sub_renderer(
        consumer_key=consumer_key,
        renderer_type=NESTED_SECTIONS_RENDERER,
    ):
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=f"{field_prefix}.renderer_type",
                message=(
                    f"Nested sections renderer is not supported by consumer '{consumer_key}'."
                ),
                reason="sub_renderer_not_supported_by_consumer",
            )
        )

    config = spec.get("config") or {}
    if not isinstance(config, dict):
        config = {}
    else:
        config = dict(config)
    raw_sub_renderers = spec.get("sub_renderers")
    if raw_sub_renderers is None and isinstance(config.get("sub_renderers"), dict):
        raw_sub_renderers = config.pop("sub_renderers")
    issues.extend(
        _collect_sub_renderer_config_issues(
            view_key=payload.view_key,
            renderer_type=NESTED_SECTIONS_RENDERER,
            config=config,
            field_prefix=f"{field_prefix}.config",
        )
    )
    if not isinstance(raw_sub_renderers, dict):
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=f"{field_prefix}.sub_renderers",
                message="Nested sections renderer must declare sub_renderers as an object.",
                reason="nested_sub_renderers_not_object",
            )
        )
        return issues

    if not is_default_spec and not isinstance(section_data, dict):
        issues.append(
            CompositionIssue(
                view_key=payload.view_key,
                field=field_prefix,
                message="Nested sections renderer requires object-shaped structured_data for its section.",
                reason="nested_sections_requires_object_data",
            )
        )
        return issues

    for nested_section_key, nested_spec in raw_sub_renderers.items():
        issues.extend(
            _collect_section_renderer_spec_issues(
                payload=payload,
                consumer_key=consumer_key,
                parent_renderer_type=parent_renderer_type,
                parent_allowed_section_renderers=set(),
                section_key=nested_section_key,
                spec=nested_spec,
                declared_sections=set(section_data.keys()) if isinstance(section_data, dict) else set(),
                section_data=section_data.get(nested_section_key) if isinstance(section_data, dict) and nested_section_key != "_default" else section_data,
                skip_section_alignment=is_default_spec,
            )
        )
    return issues


def _collect_sub_renderer_config_issues(
    *,
    view_key: str,
    renderer_type: str,
    config: Any,
    field_prefix: str,
) -> list[CompositionIssue]:
    if config is None:
        return []
    if not isinstance(config, dict):
        return [
            CompositionIssue(
                view_key=view_key,
                field=field_prefix,
                message=f"Sub-renderer config for '{renderer_type}' must be an object.",
                reason="sub_renderer_config_not_object",
            )
        ]

    sub_renderer = get_sub_renderer_registry().get(renderer_type)
    if sub_renderer is None:
        return []

    schema = sub_renderer.config_schema
    if not isinstance(schema, dict):
        return []

    validator = Draft7Validator(schema)
    return [
        CompositionIssue(
            view_key=view_key,
            field=field_prefix,
            message=error.message,
            reason="sub_renderer_config_validation_failed",
        )
        for error in validator.iter_errors(config)
    ]


def _declared_section_keys(renderer_config: dict[str, Any] | None) -> set[str]:
    return set(_ordered_declared_section_keys(renderer_config))


def _ordered_declared_section_keys(renderer_config: dict[str, Any] | None) -> list[str]:
    sections = (renderer_config or {}).get("sections")
    if not isinstance(sections, list):
        return []
    keys: list[str] = []
    for section in sections:
        if isinstance(section, dict) and isinstance(section.get("key"), str):
            keys.append(section["key"])
    return keys


def _consumer_supports_sub_renderer(*, consumer_key: str, renderer_type: str) -> bool:
    if not consumer_key:
        return True
    consumer = get_consumer_registry().get(consumer_key)
    if consumer is None:
        return True
    return renderer_type in (consumer.supported_sub_renderers or [])


def _should_validate_structured_data(payload: ViewPayload) -> bool:
    if payload.structured_data is not None:
        return True
    if payload.has_structured_data:
        return True
    return False
