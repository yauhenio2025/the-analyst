"""Enumerated fields pinned to their vocabularies (2026-09-07): the fields a vocabulary declares for an engine, the values it allows,
and the drift — a value outside them. Shape, never meaning: the wall reports drift where a row is produced; a reader may normalise a
value that contains exactly one vocabulary word ("qualified culmination" → culmination), keeping the raw."""
from __future__ import annotations

import re
from typing import Any, Optional


def pinned_fields(engine_key: Optional[str]) -> dict[str, list[str]]:
    """field → allowed values, for every vocabulary that names this engine."""
    if not engine_key:
        return {}
    from src.vocabularies.registry import get_vocabulary_registry
    out: dict[str, list[str]] = {}
    for v in get_vocabulary_registry().for_engine(engine_key):
        for u in v.used_by:
            if u.engine_key == engine_key and u.field:
                out[u.field] = v.value_list()
    return out


def match_value(raw: str, allowed: list[str]) -> tuple[Optional[str], Optional[str]]:
    """(the allowed value the raw one is, or None; the single allowed word the raw one contains, or None)."""
    val = (raw or "").strip().lower().replace(" ", "_")
    if val in allowed:
        return val, None
    hits = [a for a in allowed if re.search(r"(?<![a-z])" + re.escape(a).replace("_", "[ _]") + r"(?![a-z])", (raw or "").lower())]
    return None, (hits[0] if len(hits) == 1 else None)


def drift_of(fields: dict[str, Any], pinned: dict[str, list[str]]) -> list[dict]:
    """The pinned fields whose value is outside its vocabulary, with the word it could be normalised to (or None). No mutation."""
    out = []
    for field, allowed in pinned.items():
        raw = str(fields.get(field) or "").strip()
        if not raw:
            continue
        exact, fixed = match_value(raw, allowed)
        if exact is None:
            out.append({"field": field, "value": raw, "fixed": fixed})
    return out


def vocabulary_drift(rows, engine_key: Optional[str]) -> list[dict]:
    """The wall's report over ledger rows (LedgerRow objects with render(), or dicts with `fields`): one entry per drifted field,
    with the row id. Empty when the engine has no pinned fields."""
    pinned = pinned_fields(engine_key)
    if not pinned:
        return []
    from src.dossier.explainer import fields_of
    out = []
    for r in rows:
        fields = r.get("fields") if isinstance(r, dict) else fields_of(r.render() if hasattr(r, "render") else str(r))
        rid = r.get("id") if isinstance(r, dict) else getattr(r, "id", "")
        for d in drift_of(fields or {}, pinned):
            out.append({"id": rid, **d})
    return out
