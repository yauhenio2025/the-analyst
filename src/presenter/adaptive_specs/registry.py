"""Lazy registry for repo-tracked adaptive composition specs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import (
    AdaptiveCompositionSpec,
    AdaptiveSuiteCompositionSpec,
    normalize_adaptive_spec_payload,
    normalize_adaptive_suite_spec_payload,
)


class AdaptiveSpecRegistryError(ValueError):
    """Raised when a declarative adaptive composition spec cannot be loaded or validated."""


_SPEC_CACHE: dict[str, AdaptiveCompositionSpec] = {}
_SUITE_SPEC_CACHE: dict[str, AdaptiveSuiteCompositionSpec] = {}
_DEFINITIONS_DIR = Path(__file__).resolve().parent / "definitions"
_SUITE_DEFINITIONS_DIR = Path(__file__).resolve().parent / "suite_definitions"


def get_adaptive_composition_spec(composition_mode: str) -> AdaptiveCompositionSpec:
    if composition_mode in _SPEC_CACHE:
        return _SPEC_CACHE[composition_mode]

    raw_spec = _read_raw_spec_payload(
        definitions_dir=_DEFINITIONS_DIR,
        composition_mode=composition_mode,
        label="Adaptive composition spec",
    )
    spec = _normalize_single_surface_spec(
        composition_mode=composition_mode,
        raw_spec=raw_spec,
    )

    _SPEC_CACHE[composition_mode] = spec
    return spec


def get_adaptive_suite_composition_spec(composition_mode: str) -> AdaptiveSuiteCompositionSpec:
    if composition_mode in _SUITE_SPEC_CACHE:
        return _SUITE_SPEC_CACHE[composition_mode]

    raw_spec = _read_raw_spec_payload(
        definitions_dir=_SUITE_DEFINITIONS_DIR,
        composition_mode=composition_mode,
        label="Adaptive suite composition spec",
    )
    spec = _normalize_suite_spec(
        composition_mode=composition_mode,
        raw_spec=raw_spec,
    )

    _SUITE_SPEC_CACHE[composition_mode] = spec
    return spec


def load_all_adaptive_specs() -> dict[str, AdaptiveCompositionSpec]:
    specs: dict[str, AdaptiveCompositionSpec] = {}
    for spec_path in sorted(_DEFINITIONS_DIR.glob("*.json")):
        specs[spec_path.stem] = get_adaptive_composition_spec(spec_path.stem)
    return specs


def load_all_adaptive_suite_specs() -> dict[str, AdaptiveSuiteCompositionSpec]:
    specs: dict[str, AdaptiveSuiteCompositionSpec] = {}
    for spec_path in sorted(_SUITE_DEFINITIONS_DIR.glob("*.json")):
        specs[spec_path.stem] = get_adaptive_suite_composition_spec(spec_path.stem)
    return specs


def _read_raw_spec_payload(
    *,
    definitions_dir: Path,
    composition_mode: str,
    label: str,
) -> Any:
    spec_path = definitions_dir / f"{composition_mode}.json"
    if not spec_path.exists():
        raise AdaptiveSpecRegistryError(f"{label} not found: {composition_mode}")

    try:
        raw_spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdaptiveSpecRegistryError(f"{label} could not be read: {composition_mode}") from exc

    if not isinstance(raw_spec, dict):
        raise AdaptiveSpecRegistryError(f"{label} is invalid: {composition_mode}")
    raw_mode = raw_spec.get("composition_mode")
    if raw_mode != composition_mode or spec_path.stem != composition_mode:
        raise AdaptiveSpecRegistryError(
            f"{label} composition_mode does not match filename: {composition_mode}"
        )
    return raw_spec


def _normalize_single_surface_spec(
    *,
    composition_mode: str,
    raw_spec: Any,
) -> AdaptiveCompositionSpec:
    try:
        return normalize_adaptive_spec_payload(raw_spec)
    except Exception as exc:
        raise AdaptiveSpecRegistryError(f"Adaptive composition spec is invalid: {composition_mode}") from exc


def _normalize_suite_spec(
    *,
    composition_mode: str,
    raw_spec: Any,
) -> AdaptiveSuiteCompositionSpec:
    try:
        spec = normalize_adaptive_suite_spec_payload(raw_spec)
    except Exception as exc:
        raise AdaptiveSpecRegistryError(f"Adaptive suite composition spec is invalid: {composition_mode}") from exc
    _validate_runtime_suite_shape(spec)
    return spec


def _validate_runtime_suite_shape(spec: AdaptiveSuiteCompositionSpec) -> None:
    if spec.composition_mode != "declarative_genealogy_relationship_conditions_suite_v1":
        return

    expected_order = [
        "genealogy_relationship_landscape",
        "genealogy_conditions",
    ]
    actual_order = [surface.target_surface for surface in spec.surfaces]
    if actual_order != expected_order:
        raise AdaptiveSpecRegistryError(
            "Adaptive suite composition spec is invalid: declarative_genealogy_relationship_conditions_suite_v1"
        )
