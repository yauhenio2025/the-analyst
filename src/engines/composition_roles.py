"""Shared composition-role types for engine metadata and presenter composition."""

from __future__ import annotations

from typing import Literal, TypeAlias, TypeGuard, get_args

CompositionRole: TypeAlias = Literal[
    "synthesis_primary",
    "comparison_map",
    "findings_bank",
    "report_closeout",
    "inventory_listing",
]

COMPOSITION_ROLE_VALUES = get_args(CompositionRole)
COMPOSITION_ROLE_SET = frozenset(COMPOSITION_ROLE_VALUES)


def is_composition_role(value: object) -> TypeGuard[CompositionRole]:
    return isinstance(value, str) and value in COMPOSITION_ROLE_SET
