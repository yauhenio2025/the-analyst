"""Deterministic bounded review/disposition builder and harness."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from typing import Optional

from src.evaluations.gate_store import load_evaluation_gate_decision
from src.evaluations.review_definitions import get_evaluation_review_definition
from src.evaluations.review_schemas import (
    EvaluationReviewDecisionSummary,
    EvaluationReviewerIdentity,
    PersistedEvaluationReviewDecision,
    ReviewDisposition,
)
from src.evaluations.review_store import (
    build_evaluation_review_decision_id,
    save_evaluation_review_decision,
)


def build_evaluation_review_decision(
    *,
    review_key: str,
    gate_decision_id: str,
    reviewer_name: str,
    reviewer_role: str,
    disposition: ReviewDisposition,
    rationale: str,
    waiver_reasons: Optional[list[str]] = None,
    save_decision: bool = True,
) -> PersistedEvaluationReviewDecision:
    """Build one bounded review/disposition decision over an exact gate decision."""

    review_definition = get_evaluation_review_definition(review_key)
    gate_decision = load_evaluation_gate_decision(gate_decision_id)
    if gate_decision is None:
        raise ValueError(f"Evaluation gate decision '{gate_decision_id}' was not found.")

    _validate_gate_against_review_definition(
        review_definition=review_definition,
        gate_decision=gate_decision,
    )

    normalized_reviewer_name = _normalize_required_text(reviewer_name, "reviewer_name")
    normalized_reviewer_role = _normalize_required_text(reviewer_role, "reviewer_role")
    normalized_rationale = _normalize_required_text(rationale, "rationale")
    normalized_waiver_reasons = _normalize_waiver_reasons(waiver_reasons or [])

    _validate_disposition_alignment(
        disposition=disposition,
        observed_gate_verdict=gate_decision.overall_verdict,
    )
    if disposition == "waive":
        if not normalized_waiver_reasons:
            raise ValueError(
                "Disposition 'waive' requires at least one non-blank waiver reason."
            )
    elif normalized_waiver_reasons:
        raise ValueError("Waiver reasons are allowed only when disposition='waive'.")

    review_decision = PersistedEvaluationReviewDecision(
        review_decision_id=build_evaluation_review_decision_id(),
        created_at=_now_iso(),
        review_key=review_definition.review_key,
        review_definition_version=review_definition.review_definition_version,
        gate_decision_id=gate_decision.gate_decision_id,
        gate_key=gate_decision.gate_key,
        gate_definition_version=gate_decision.gate_definition_version,
        evaluation_pack_key=gate_decision.evaluation_pack_key,
        reviewer_identity=EvaluationReviewerIdentity(
            reviewer_name=normalized_reviewer_name,
            reviewer_role=normalized_reviewer_role,
        ),
        disposition=disposition,
        rationale=normalized_rationale,
        observed_gate_verdict=gate_decision.overall_verdict,
        contains_live_revalidation=gate_decision.contains_live_revalidation,
        observed_gate_blocking_reasons=list(gate_decision.blocking_reasons),
        waiver_reasons=normalized_waiver_reasons,
    )
    if save_decision:
        save_evaluation_review_decision(review_decision)
    return review_decision


def _validate_gate_against_review_definition(*, review_definition, gate_decision) -> None:
    mismatches: list[str] = []
    if gate_decision.gate_key != review_definition.gate_key:
        mismatches.append(
            f"gate_key mismatch: expected '{review_definition.gate_key}', observed '{gate_decision.gate_key}'"
        )
    if gate_decision.gate_definition_version != review_definition.gate_definition_version:
        mismatches.append(
            "gate_definition_version mismatch: "
            f"expected '{review_definition.gate_definition_version}', observed '{gate_decision.gate_definition_version}'"
        )
    if gate_decision.evaluation_pack_key != review_definition.evaluation_pack_key:
        mismatches.append(
            "evaluation_pack_key mismatch: "
            f"expected '{review_definition.evaluation_pack_key}', observed '{gate_decision.evaluation_pack_key}'"
        )
    if mismatches:
        raise ValueError("; ".join(mismatches))


def _validate_disposition_alignment(
    *,
    disposition: ReviewDisposition,
    observed_gate_verdict: str,
) -> None:
    if disposition not in {"accept", "reject", "waive"}:
        raise ValueError(
            f"Unknown disposition '{disposition}'. Expected one of: accept, reject, waive."
        )
    if disposition == "accept" and observed_gate_verdict != "pass":
        raise ValueError(
            f"Disposition 'accept' is valid only for gate verdict 'pass', observed '{observed_gate_verdict}'."
        )
    if disposition == "waive" and observed_gate_verdict == "pass":
        raise ValueError(
            "Disposition 'waive' is valid only for gate verdicts 'fail' or 'error'."
        )


def _normalize_required_text(raw_value: str, field_name: str) -> str:
    normalized_value = raw_value.strip()
    if not normalized_value:
        raise ValueError(f"{field_name} must be non-blank.")
    return normalized_value


def _normalize_waiver_reasons(raw_reasons: list[str]) -> list[str]:
    return [reason.strip() for reason in raw_reasons if reason.strip()]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entrypoint for bounded review/disposition decisions."""

    parser = argparse.ArgumentParser(description="Build one bounded review/disposition decision.")
    parser.add_argument("--review-key", required=True, help="Evaluation review definition key")
    parser.add_argument("--gate-decision-id", required=True, help="Exact gate decision id")
    parser.add_argument("--reviewer-name", required=True, help="Reviewer name label")
    parser.add_argument("--reviewer-role", required=True, help="Reviewer role label")
    parser.add_argument(
        "--disposition",
        required=True,
        choices=["accept", "reject", "waive"],
        help="Review disposition over the referenced gate",
    )
    parser.add_argument("--rationale", required=True, help="Required written rationale")
    parser.add_argument(
        "--waiver-reason",
        action="append",
        default=[],
        help="Optional waiver reason. Repeat when disposition=waive.",
    )
    args = parser.parse_args(argv)

    review_decision = build_evaluation_review_decision(
        review_key=args.review_key,
        gate_decision_id=args.gate_decision_id,
        reviewer_name=args.reviewer_name,
        reviewer_role=args.reviewer_role,
        disposition=args.disposition,
        rationale=args.rationale,
        waiver_reasons=args.waiver_reason,
        save_decision=True,
    )

    summary = EvaluationReviewDecisionSummary(
        review_decision_id=review_decision.review_decision_id,
        created_at=review_decision.created_at,
        review_key=review_decision.review_key,
        review_definition_version=review_decision.review_definition_version,
        gate_decision_id=review_decision.gate_decision_id,
        gate_key=review_decision.gate_key,
        evaluation_pack_key=review_decision.evaluation_pack_key,
        disposition=review_decision.disposition,
        observed_gate_verdict=review_decision.observed_gate_verdict,
        contains_live_revalidation=review_decision.contains_live_revalidation,
    )
    print(summary.model_dump_json())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
