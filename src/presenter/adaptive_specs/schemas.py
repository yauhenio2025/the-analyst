"""Pydantic schemas for declarative adaptive composition specs."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from .keys import (
    ALLOWED_BUILDER_TEMPLATE_KEYS,
    ALLOWED_OPERATOR_KEYS,
    ALLOWED_SIGNAL_EXTRACTOR_KEYS,
)


class AdaptivePredicate(BaseModel):
    metric: str
    operator: str
    value: float | int

    @field_validator("operator")
    @classmethod
    def _validate_operator(cls, value: str) -> str:
        if value not in ALLOWED_OPERATOR_KEYS:
            raise ValueError(f"Unsupported adaptive predicate operator: {value}")
        return value


class AdaptiveDecisionRule(BaseModel):
    family_key: str
    match_any: list[list[AdaptivePredicate]] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_match_any(self) -> "AdaptiveDecisionRule":
        for predicate_group in self.match_any:
            if not predicate_group:
                raise ValueError("Adaptive decision rules cannot include empty predicate groups.")
        return self


class AdaptiveFamilySpec(BaseModel):
    family_key: str
    builder_template_key: str
    view_name: str

    @field_validator("builder_template_key")
    @classmethod
    def _validate_builder_template_key(cls, value: str) -> str:
        if value not in ALLOWED_BUILDER_TEMPLATE_KEYS:
            raise ValueError(f"Unknown builder_template_key: {value}")
        return value


class AdaptiveCompositionSpec(BaseModel):
    composition_mode: str
    workflow_key: str
    target_surface: str
    signal_extractor_key: str
    default_family: str
    families: list[AdaptiveFamilySpec] = Field(default_factory=list)
    decision_rules: list[AdaptiveDecisionRule] = Field(default_factory=list)

    @field_validator("signal_extractor_key")
    @classmethod
    def _validate_signal_extractor_key(cls, value: str) -> str:
        if value not in ALLOWED_SIGNAL_EXTRACTOR_KEYS:
            raise ValueError(f"Unknown signal_extractor_key: {value}")
        return value

    @model_validator(mode="after")
    def _validate_family_refs(self) -> "AdaptiveCompositionSpec":
        if not self.families:
            raise ValueError("Adaptive composition specs must declare at least one family.")

        family_keys: list[str] = [family.family_key for family in self.families]
        if len(set(family_keys)) != len(family_keys):
            raise ValueError("Adaptive composition specs cannot declare duplicate family_key values.")

        if self.default_family not in family_keys:
            raise ValueError("Adaptive composition spec default_family must be declared in families.")

        for family in self.families:
            if family.builder_template_key != family.family_key:
                raise ValueError("Adaptive composition spec v1 requires builder_template_key to equal family_key.")

        declared_family_keys = set(family_keys)
        for rule in self.decision_rules:
            if rule.family_key not in declared_family_keys:
                raise ValueError("Adaptive composition decision rule references an undeclared family.")

        return self


class AdaptiveSuiteSurfaceSpec(BaseModel):
    target_surface: str
    signal_extractor_key: str
    default_family: str
    families: list[AdaptiveFamilySpec] = Field(default_factory=list)
    decision_rules: list[AdaptiveDecisionRule] = Field(default_factory=list)

    @field_validator("signal_extractor_key")
    @classmethod
    def _validate_signal_extractor_key(cls, value: str) -> str:
        if value not in ALLOWED_SIGNAL_EXTRACTOR_KEYS:
            raise ValueError(f"Unknown signal_extractor_key: {value}")
        return value

    @model_validator(mode="after")
    def _validate_family_refs(self) -> "AdaptiveSuiteSurfaceSpec":
        if not self.families:
            raise ValueError("Adaptive suite surface specs must declare at least one family.")

        family_keys = [family.family_key for family in self.families]
        if len(set(family_keys)) != len(family_keys):
            raise ValueError("Adaptive suite surface specs cannot declare duplicate family_key values.")

        if self.default_family not in family_keys:
            raise ValueError("Adaptive suite surface spec default_family must be declared in families.")

        for family in self.families:
            if family.builder_template_key != family.family_key:
                raise ValueError("Adaptive composition spec v1 requires builder_template_key to equal family_key.")

        declared_family_keys = set(family_keys)
        for rule in self.decision_rules:
            if rule.family_key not in declared_family_keys:
                raise ValueError("Adaptive composition decision rule references an undeclared family.")

        return self


class AdaptiveSuiteCompositionSpec(BaseModel):
    composition_mode: str
    workflow_key: str
    surfaces: list[AdaptiveSuiteSurfaceSpec] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_surfaces(self) -> "AdaptiveSuiteCompositionSpec":
        if not self.surfaces:
            raise ValueError("Adaptive suite composition specs must declare at least one surface.")

        target_surfaces = [surface.target_surface for surface in self.surfaces]
        if len(set(target_surfaces)) != len(target_surfaces):
            raise ValueError("Adaptive suite composition specs cannot declare duplicate target_surface values.")

        return self


def normalize_adaptive_spec_payload(raw_payload: Any) -> AdaptiveCompositionSpec:
    """Validate a raw spec payload into the frozen adaptive-spec contract."""

    return AdaptiveCompositionSpec.model_validate(raw_payload)


def normalize_adaptive_suite_spec_payload(raw_payload: Any) -> AdaptiveSuiteCompositionSpec:
    """Validate a raw suite-spec payload into the bounded adaptive-suite contract."""

    return AdaptiveSuiteCompositionSpec.model_validate(raw_payload)
