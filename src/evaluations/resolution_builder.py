"""Deterministic bounded disposition-resolution builder and harness."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from typing import Optional

from src.evaluations.resolution_definitions import (
    get_evaluation_disposition_resolution_definition,
)
from src.evaluations.resolution_schemas import (
    EvaluationDispositionResolutionSummary,
    EvaluationResolverIdentity,
    PersistedEvaluationDispositionResolution,
)
from src.evaluations.resolution_store import (
    build_evaluation_disposition_resolution_id,
    save_evaluation_disposition_resolution,
)
from src.evaluations.review_store import load_evaluation_review_decision


def build_evaluation_disposition_resolution(
    *,
    resolution_key: str,
    review_decision_id: str,
    resolver_name: str,
    resolver_role: str,
    resolution_note: str,
    save_resolution: bool = True,
) -> PersistedEvaluationDispositionResolution:
    """Build one bounded current-disposition resolution over an exact review decision."""

    resolution_definition = get_evaluation_disposition_resolution_definition(resolution_key)
    review_decision = load_evaluation_review_decision(review_decision_id)
    if review_decision is None:
        raise ValueError(f"Evaluation review decision '{review_decision_id}' was not found.")

    _validate_review_against_resolution_definition(
        resolution_definition=resolution_definition,
        review_decision=review_decision,
    )

    normalized_resolver_name = _normalize_required_text(resolver_name, "resolver_name")
    normalized_resolver_role = _normalize_required_text(resolver_role, "resolver_role")
    normalized_resolution_note = _normalize_required_text(resolution_note, "resolution_note")

    resolution = PersistedEvaluationDispositionResolution(
        resolution_id=build_evaluation_disposition_resolution_id(),
        resolution_key=resolution_definition.resolution_key,
        created_at=_now_iso(),
        resolution_definition_version=resolution_definition.resolution_definition_version,
        review_decision_id=review_decision.review_decision_id,
        review_key=review_decision.review_key,
        review_definition_version=review_decision.review_definition_version,
        gate_decision_id=review_decision.gate_decision_id,
        gate_key=review_decision.gate_key,
        gate_definition_version=review_decision.gate_definition_version,
        evaluation_pack_key=review_decision.evaluation_pack_key,
        resolver_identity=EvaluationResolverIdentity(
            resolver_name=normalized_resolver_name,
            resolver_role=normalized_resolver_role,
        ),
        resolution_note=normalized_resolution_note,
        adopted_review_disposition=review_decision.disposition,
        observed_gate_verdict=review_decision.observed_gate_verdict,
        contains_live_revalidation=review_decision.contains_live_revalidation,
    )
    if save_resolution:
        save_evaluation_disposition_resolution(resolution)
    return resolution


def _validate_review_against_resolution_definition(
    *,
    resolution_definition,
    review_decision,
) -> None:
    mismatches: list[str] = []
    if review_decision.review_key != resolution_definition.review_key:
        mismatches.append(
            "review_key mismatch: "
            f"expected '{resolution_definition.review_key}', observed '{review_decision.review_key}'"
        )
    if (
        review_decision.review_definition_version
        != resolution_definition.review_definition_version
    ):
        mismatches.append(
            "review_definition_version mismatch: "
            f"expected '{resolution_definition.review_definition_version}', observed '{review_decision.review_definition_version}'"
        )
    if review_decision.gate_key != resolution_definition.gate_key:
        mismatches.append(
            f"gate_key mismatch: expected '{resolution_definition.gate_key}', observed '{review_decision.gate_key}'"
        )
    if (
        review_decision.gate_definition_version
        != resolution_definition.gate_definition_version
    ):
        mismatches.append(
            "gate_definition_version mismatch: "
            f"expected '{resolution_definition.gate_definition_version}', observed '{review_decision.gate_definition_version}'"
        )
    if review_decision.evaluation_pack_key != resolution_definition.evaluation_pack_key:
        mismatches.append(
            "evaluation_pack_key mismatch: "
            f"expected '{resolution_definition.evaluation_pack_key}', observed '{review_decision.evaluation_pack_key}'"
        )
    if mismatches:
        raise ValueError("; ".join(mismatches))


def _normalize_required_text(raw_value: str, field_name: str) -> str:
    normalized_value = raw_value.strip()
    if not normalized_value:
        raise ValueError(f"{field_name} must be non-blank.")
    return normalized_value


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entrypoint for bounded disposition-resolution decisions."""

    parser = argparse.ArgumentParser(
        description="Build one bounded disposition-resolution decision."
    )
    parser.add_argument(
        "--resolution-key", required=True, help="Evaluation disposition-resolution definition key"
    )
    parser.add_argument("--review-decision-id", required=True, help="Exact review decision id")
    parser.add_argument("--resolver-name", required=True, help="Resolver name label")
    parser.add_argument("--resolver-role", required=True, help="Resolver role label")
    parser.add_argument("--resolution-note", required=True, help="Required written resolution note")
    args = parser.parse_args(argv)

    resolution = build_evaluation_disposition_resolution(
        resolution_key=args.resolution_key,
        review_decision_id=args.review_decision_id,
        resolver_name=args.resolver_name,
        resolver_role=args.resolver_role,
        resolution_note=args.resolution_note,
        save_resolution=True,
    )

    summary = EvaluationDispositionResolutionSummary(
        resolution_id=resolution.resolution_id,
        resolution_key=resolution.resolution_key,
        created_at=resolution.created_at,
        resolution_definition_version=resolution.resolution_definition_version,
        review_decision_id=resolution.review_decision_id,
        review_key=resolution.review_key,
        gate_decision_id=resolution.gate_decision_id,
        gate_key=resolution.gate_key,
        evaluation_pack_key=resolution.evaluation_pack_key,
        adopted_review_disposition=resolution.adopted_review_disposition,
        observed_gate_verdict=resolution.observed_gate_verdict,
        contains_live_revalidation=resolution.contains_live_revalidation,
    )
    print(summary.model_dump_json())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
