"""The findings ledger — targets minted by walls, clamps and the cross-check judge (DESIGN §C.4 "Ledger").

A finding is a recorded fact with ONE affordance. Code never closes one by
silence: it stays open until a later pass records a fate. `source` says who
minted it — `wall` (an exhibit desk's own arithmetic), `clamp` (the cross-check's
code clamps, which outrank the judge) or `judge`.
"""
from __future__ import annotations

import logging
import uuid
from typing import Any, Optional

from src.dossier.schemas import AFFORDANCES, FINDING_KINDS, Fate, Finding, FindingWhere

logger = logging.getLogger(__name__)


def mint(kind: str, *, note: str, affordance: str = "none", where: Optional[dict[str, Any]] = None, quote: str = "",
         realization: Optional[str] = None, source: str = "wall", round: int = 0, recommended: bool = True) -> Finding:
    if kind not in FINDING_KINDS:
        raise ValueError(f"unknown finding kind {kind!r}")
    if affordance not in AFFORDANCES:
        affordance = "none"
    return Finding(id=f"fnd-{uuid.uuid4().hex[:8]}", kind=kind, where=FindingWhere(**(where or {})), quote=quote[:400],
                   note=note[:1200], affordance=affordance, realization=realization, recommended=recommended,
                   source=source, round=round)


def open_findings(findings: list[Finding]) -> list[Finding]:
    return [f for f in findings if f.status == "open"]


def record_fate(finding: Finding, fate: str, rationale: str = "", *, by: str = "code", round: int = 0) -> Finding:
    finding.fates.append(Fate(round=round, fate=fate, rationale=rationale[:600], by=by))
    if fate in ("resolved", "superseded", "executed"):
        finding.status = "resolved" if fate != "superseded" else "superseded"
    elif fate in ("skipped", "failed", "persists", "regressed"):
        finding.status = "open"
    return finding


def by_id(findings: list[Finding], fid: str) -> Optional[Finding]:
    for f in findings:
        if f.id == fid:
            return f
    return None


def append(job, new: list[Finding], persist=None) -> list[Finding]:
    """Add findings to the job (and persist when a persist callable is given). Returns the full ledger."""
    if not new:
        return job.findings
    job.findings = list(job.findings) + list(new)
    if persist is not None:
        try:
            persist(findings=job.findings)
        except Exception as exc:  # bookkeeping never kills the run
            logger.warning(f"findings persist failed: {exc}")
    return job.findings


def summary_line(findings: list[Finding]) -> str:
    opened = open_findings(findings)
    if not opened:
        return "no open findings"
    kinds: dict[str, int] = {}
    for f in opened:
        kinds[f.kind] = kinds.get(f.kind, 0) + 1
    return f"{len(opened)} open: " + ", ".join(f"{k} ×{n}" if n > 1 else k for k, n in kinds.items())
