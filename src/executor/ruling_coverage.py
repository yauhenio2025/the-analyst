"""Structural coverage of critic rulings; no ID repair or semantic assessment."""
from __future__ import annotations

from collections import Counter
from typing import Iterable, Protocol


class _Row(Protocol):
    id: str
    status: str


_ORIGINAL_STATUSES = frozenset({"confirmed", "weakened", "rejected"})


def critic_ruling_coverage(original_rows: Iterable[_Row], rulings: Iterable[_Row]) -> dict:
    """Report exact-ID coverage without treating carried rows as explicit rulings.

    Counts refer to input rows; diagnostic ID lists preserve first appearance and
    contain each ID once. An explicit ruling counts only when its original ID and
    ruling ID are both unique and its status is confirmed, weakened, or rejected.
    Added rows may introduce new IDs; `added` is invalid on an original ID.

    Complete means a nonempty original ledger has one valid ruling per row, no
    duplicate IDs in either input, and no unexpected non-added rulings. Duplicate
    additions therefore remain a structural error even if originals were ruled.
    This function diagnoses ambiguity instead of choosing between duplicate rows.
    """
    originals, decisions = list(original_rows), list(rulings)
    original_counts = Counter(row.id for row in originals)
    ruling_counts = Counter(row.id for row in decisions)
    original_ids = list(original_counts)
    duplicate_original_ids = [rid for rid, count in original_counts.items() if count > 1]
    duplicate_ruling_ids = [rid for rid, count in ruling_counts.items() if count > 1]
    valid_ids = {
        row.id for row in decisions
        if original_counts[row.id] == 1 and ruling_counts[row.id] == 1
        and row.status in _ORIGINAL_STATUSES
    }
    missing = [rid for rid in original_ids if rid not in valid_ids]
    unexpected = list(dict.fromkeys(
        row.id for row in decisions if row.id not in original_counts and row.status != "added"
    ))
    invalid = list(dict.fromkeys(
        row.id for row in decisions if row.id in original_counts and row.status not in _ORIGINAL_STATUSES
    ))
    return {
        "original_count": len(originals),
        "explicitly_ruled_count": len(valid_ids),
        "missing_or_unruled_ids": missing,
        "unexpected_nonadded_ids": unexpected,
        "invalid_original_status_ids": invalid,
        "duplicate_original_ids": duplicate_original_ids,
        "duplicate_ruling_ids": duplicate_ruling_ids,
        "coverage_complete": bool(originals) and not (
            missing or unexpected or invalid or duplicate_original_ids or duplicate_ruling_ids
        ),
    }
