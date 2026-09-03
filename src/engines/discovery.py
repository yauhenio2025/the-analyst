"""Capability-aware engine discovery helpers.

This module keeps the legacy JSON registry and the capability YAML registry
separate, while providing a merged "discoverable" view for browse/admin flows.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.engines.composition_roles import CompositionRole, is_composition_role
from src.engines.registry import EngineRegistry
from src.engines.schemas import EngineDefinition, EngineSummary
from src.engines.schemas_v2 import CapabilityEngineDefinition


@dataclass(frozen=True)
class DiscoverableEngine:
    """One discoverable engine family exposed on browse/filter surfaces."""

    engine_key: str
    summary: EngineSummary
    legacy_engine_key: str | None = None
    legacy_engine: EngineDefinition | None = None
    capability_definition: CapabilityEngineDefinition | None = None


class CapabilityMetadataResolutionError(ValueError):
    """Raised when canonical capability metadata cannot supply required values."""


def _first_paragraph(text: str | None) -> str:
    if not text:
        return ""
    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
    return paragraphs[0] if paragraphs else text.strip()


def _coalesce_str(*values: str | None) -> str:
    for value in values:
        if value and value.strip():
            return value.strip()
    return ""


def _coalesce_optional_str(*values: str | None) -> str | None:
    for value in values:
        if value and value.strip():
            return value.strip()
    return None


def _merge_list(*collections: list[str]) -> list[str]:
    seen: set[str] = set()
    merged: list[str] = []
    for collection in collections:
        for item in collection:
            if item not in seen:
                seen.add(item)
                merged.append(item)
    return merged


def resolve_capability_definition(
    registry: EngineRegistry,
    engine_key: str,
) -> CapabilityEngineDefinition | None:
    """Resolve a capability definition by canonical key or legacy alias."""
    cap_def = registry.get_capability_definition(engine_key)
    if cap_def is not None:
        return cap_def

    for candidate in registry.list_capability_definitions():
        if candidate.legacy_engine_key == engine_key:
            return candidate
    return None


def resolve_composition_role(
    registry: EngineRegistry,
    engine_key: str,
) -> CompositionRole:
    """Resolve one validated composition role from canonical or legacy engine keys."""
    capability = resolve_capability_definition(registry, engine_key)
    if capability is None:
        raise CapabilityMetadataResolutionError(
            f"No canonical capability metadata found for engine '{engine_key}'."
        )

    composition_role = getattr(capability, "composition_role", None)
    if not is_composition_role(composition_role):
        raise CapabilityMetadataResolutionError(
            "Canonical capability metadata for engine "
            f"'{engine_key}' is missing a valid composition_role."
        )
    return composition_role


def resolve_legacy_engine(
    registry: EngineRegistry,
    engine_key: str,
) -> EngineDefinition | None:
    """Resolve a legacy engine directly or through a capability alias bridge."""
    legacy = registry.get(engine_key)
    if legacy is not None:
        return legacy

    cap_def = resolve_capability_definition(registry, engine_key)
    if cap_def is None or not cap_def.legacy_engine_key:
        return None
    return registry.get(cap_def.legacy_engine_key)


def engine_exists(registry: EngineRegistry, engine_key: str) -> bool:
    """Return True if either legacy or capability metadata exists for a key."""
    return (
        registry.get(engine_key) is not None
        or resolve_capability_definition(registry, engine_key) is not None
    )


def build_engine_summary(
    *,
    canonical_key: str,
    legacy_engine: EngineDefinition | None,
    capability_definition: CapabilityEngineDefinition | None,
) -> EngineSummary:
    """Build a discoverable summary from a legacy/capability pair."""
    if legacy_engine is None and capability_definition is None:
        raise ValueError("At least one engine definition must be provided")

    engine_name = _coalesce_str(
        legacy_engine.engine_name if legacy_engine else None,
        capability_definition.engine_name if capability_definition else None,
        canonical_key.replace("_", " ").title(),
    )
    description = _coalesce_str(
        legacy_engine.description if legacy_engine else None,
        _first_paragraph(
            capability_definition.problematique if capability_definition else None
        ),
    )
    category = (
        legacy_engine.category
        if legacy_engine is not None
        else capability_definition.category
    )
    kind = (
        legacy_engine.kind
        if legacy_engine is not None
        else capability_definition.kind
    )
    version = (
        legacy_engine.version
        if legacy_engine is not None and legacy_engine.version is not None
        else capability_definition.version
    )

    return EngineSummary(
        engine_key=canonical_key,
        engine_name=engine_name,
        description=description,
        category=category,
        kind=kind,
        version=version,
        family=legacy_engine.family if legacy_engine else "analytical",
        home_organ=legacy_engine.home_organ if legacy_engine else "the-analyst",
        status=legacy_engine.status if legacy_engine else "live",
        sync=legacy_engine.sync if legacy_engine else "native",
        paradigm_keys=_merge_list(
            legacy_engine.paradigm_keys if legacy_engine else [],
            capability_definition.paradigm_keys if capability_definition else [],
        ),
        has_profile=bool(legacy_engine and legacy_engine.engine_profile is not None),
        apps=_merge_list(
            legacy_engine.apps if legacy_engine else [],
            capability_definition.apps if capability_definition else [],
        ),
        function=_coalesce_optional_str(
            legacy_engine.function if legacy_engine else None,
            capability_definition.function if capability_definition else None,
        ),
    )


def list_discoverable_engines(registry: EngineRegistry) -> list[DiscoverableEngine]:
    """Return the merged discoverable engine set.

    Canonical key policy:
    - if a capability definition exists, its engine_key is the public browse key
    - same-key legacy engines are matched implicitly
    - differing legacy aliases are matched through legacy_engine_key
    - unmatched legacy JSON engines remain discoverable under their own key
    """

    legacy_by_key = {engine.engine_key: engine for engine in registry.list_all()}
    matched_legacy: set[str] = set()
    discoverable: list[DiscoverableEngine] = []

    for cap_def in registry.list_capability_definitions():
        legacy = legacy_by_key.get(cap_def.engine_key)
        if legacy is None and cap_def.legacy_engine_key:
            legacy = legacy_by_key.get(cap_def.legacy_engine_key)
        if legacy is not None:
            matched_legacy.add(legacy.engine_key)

        discoverable.append(
            DiscoverableEngine(
                engine_key=cap_def.engine_key,
                summary=build_engine_summary(
                    canonical_key=cap_def.engine_key,
                    legacy_engine=legacy,
                    capability_definition=cap_def,
                ),
                legacy_engine_key=legacy.engine_key if legacy else None,
                legacy_engine=legacy,
                capability_definition=cap_def,
            )
        )

    for legacy in legacy_by_key.values():
        if legacy.engine_key in matched_legacy:
            continue
        discoverable.append(
            DiscoverableEngine(
                engine_key=legacy.engine_key,
                summary=build_engine_summary(
                    canonical_key=legacy.engine_key,
                    legacy_engine=legacy,
                    capability_definition=None,
                ),
                legacy_engine_key=legacy.engine_key,
                legacy_engine=legacy,
                capability_definition=None,
            )
        )

    return sorted(discoverable, key=lambda entry: entry.summary.engine_key)


def resolve_discoverable_engine(
    registry: EngineRegistry,
    engine_key: str,
) -> DiscoverableEngine | None:
    """Resolve a discoverable engine by canonical key or legacy alias."""
    for engine in list_discoverable_engines(registry):
        if engine.summary.engine_key == engine_key:
            return engine
        if engine.legacy_engine_key == engine_key:
            return engine
    return None


def resolve_engine_display_name(registry: EngineRegistry, engine_key: str) -> str:
    """Resolve the most useful human-readable name for an engine key."""
    discoverable = resolve_discoverable_engine(registry, engine_key)
    if discoverable is not None:
        return discoverable.summary.engine_name
    return engine_key.replace("_", " ").title()
