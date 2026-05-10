"""Derived current governance-status helpers over the resolution/review/gate chain."""

from __future__ import annotations

from dataclasses import dataclass

from src.evaluations.gate_store import load_evaluation_gate_decision
from src.evaluations.governance_status_schemas import (
    EffectiveGovernanceStatus,
    EvaluationCurrentGovernanceStatusResponse,
)
from src.evaluations.resolution_definitions import (
    get_evaluation_disposition_resolution_definition,
)
from src.evaluations.resolution_store import load_current_evaluation_disposition_resolution
from src.evaluations.review_store import load_evaluation_review_decision


@dataclass(frozen=True)
class GovernanceStatusDerivationError(Exception):
    status_code: int
    detail: str


def load_current_evaluation_governance_status(
    resolution_key: str,
    gate_decision_id: str,
) -> EvaluationCurrentGovernanceStatusResponse:
    """Load one semantic current-governance-status view over the linked chain."""

    resolution = load_current_evaluation_disposition_resolution(
        resolution_key=resolution_key,
        gate_decision_id=gate_decision_id,
    )
    if resolution is None:
        raise GovernanceStatusDerivationError(
            status_code=404,
            detail=(
                "No current evaluation disposition resolution was found for "
                f"resolution_key='{resolution_key}' and gate_decision_id='{gate_decision_id}'"
            ),
        )

    try:
        resolution_definition = get_evaluation_disposition_resolution_definition(
            resolution.resolution_key
        )
    except ValueError as exc:
        raise GovernanceStatusDerivationError(
            status_code=409,
            detail=(
                "Current governance-status chain is inconsistent: "
                f"{exc}"
            ),
        ) from exc
    _validate_resolution_against_definition(
        resolution=resolution,
        resolution_definition=resolution_definition,
    )

    review = load_evaluation_review_decision(resolution.review_decision_id)
    if review is None:
        raise GovernanceStatusDerivationError(
            status_code=409,
            detail=(
                "Current governance-status chain is inconsistent: "
                f"review '{resolution.review_decision_id}' referenced by "
                f"resolution '{resolution.resolution_id}' was not found."
            ),
        )

    gate = load_evaluation_gate_decision(resolution.gate_decision_id)
    if gate is None:
        raise GovernanceStatusDerivationError(
            status_code=409,
            detail=(
                "Current governance-status chain is inconsistent: "
                f"gate '{resolution.gate_decision_id}' referenced by "
                f"resolution '{resolution.resolution_id}' was not found."
            ),
        )

    _validate_resolution_against_review(resolution=resolution, review=review)
    _validate_review_against_gate(review=review, gate=gate)

    return EvaluationCurrentGovernanceStatusResponse(
        resolution_key=resolution.resolution_key,
        gate_decision_id=resolution.gate_decision_id,
        effective_governance_status=_derive_effective_governance_status(
            resolution.adopted_review_disposition
        ),
        scope_label=resolution_definition.scope_label,
        resolution=resolution,
    )


def _derive_effective_governance_status(
    adopted_review_disposition: str,
) -> EffectiveGovernanceStatus:
    if adopted_review_disposition == "accept":
        return "approved"
    if adopted_review_disposition == "reject":
        return "blocked"
    if adopted_review_disposition == "waive":
        return "exception_recorded"
    raise GovernanceStatusDerivationError(
        status_code=409,
        detail=(
            "Current governance-status chain is inconsistent: "
            f"unknown adopted review disposition '{adopted_review_disposition}'."
        ),
    )


def _validate_resolution_against_definition(*, resolution, resolution_definition) -> None:
    mismatches: list[str] = []
    if (
        resolution.resolution_definition_version
        != resolution_definition.resolution_definition_version
    ):
        mismatches.append(
            "resolution_definition_version expected "
            f"'{resolution_definition.resolution_definition_version}' observed "
            f"'{resolution.resolution_definition_version}'"
        )
    if resolution.review_key != resolution_definition.review_key:
        mismatches.append(
            f"review_key expected '{resolution_definition.review_key}' observed '{resolution.review_key}'"
        )
    if (
        resolution.review_definition_version
        != resolution_definition.review_definition_version
    ):
        mismatches.append(
            "review_definition_version expected "
            f"'{resolution_definition.review_definition_version}' observed "
            f"'{resolution.review_definition_version}'"
        )
    if resolution.gate_key != resolution_definition.gate_key:
        mismatches.append(
            f"gate_key expected '{resolution_definition.gate_key}' observed '{resolution.gate_key}'"
        )
    if (
        resolution.gate_definition_version
        != resolution_definition.gate_definition_version
    ):
        mismatches.append(
            "gate_definition_version expected "
            f"'{resolution_definition.gate_definition_version}' observed "
            f"'{resolution.gate_definition_version}'"
        )
    if resolution.evaluation_pack_key != resolution_definition.evaluation_pack_key:
        mismatches.append(
            "evaluation_pack_key expected "
            f"'{resolution_definition.evaluation_pack_key}' observed "
            f"'{resolution.evaluation_pack_key}'"
        )
    if mismatches:
        raise GovernanceStatusDerivationError(
            status_code=409,
            detail=(
                "Current governance-status chain is inconsistent: "
                + "; ".join(mismatches)
            ),
        )


def _validate_resolution_against_review(*, resolution, review) -> None:
    mismatches: list[str] = []
    if resolution.review_key != review.review_key:
        mismatches.append(
            f"review_key expected '{resolution.review_key}' observed '{review.review_key}'"
        )
    if resolution.review_definition_version != review.review_definition_version:
        mismatches.append(
            "review_definition_version expected "
            f"'{resolution.review_definition_version}' observed "
            f"'{review.review_definition_version}'"
        )
    if resolution.gate_decision_id != review.gate_decision_id:
        mismatches.append(
            f"gate_decision_id expected '{resolution.gate_decision_id}' observed '{review.gate_decision_id}'"
        )
    if resolution.gate_key != review.gate_key:
        mismatches.append(
            f"gate_key expected '{resolution.gate_key}' observed '{review.gate_key}'"
        )
    if resolution.gate_definition_version != review.gate_definition_version:
        mismatches.append(
            "gate_definition_version expected "
            f"'{resolution.gate_definition_version}' observed "
            f"'{review.gate_definition_version}'"
        )
    if resolution.evaluation_pack_key != review.evaluation_pack_key:
        mismatches.append(
            "evaluation_pack_key expected "
            f"'{resolution.evaluation_pack_key}' observed "
            f"'{review.evaluation_pack_key}'"
        )
    if resolution.adopted_review_disposition != review.disposition:
        mismatches.append(
            "adopted_review_disposition expected "
            f"'{resolution.adopted_review_disposition}' observed '{review.disposition}'"
        )
    if resolution.observed_gate_verdict != review.observed_gate_verdict:
        mismatches.append(
            "observed_gate_verdict expected "
            f"'{resolution.observed_gate_verdict}' observed '{review.observed_gate_verdict}'"
        )
    if resolution.contains_live_revalidation != review.contains_live_revalidation:
        mismatches.append(
            "contains_live_revalidation expected "
            f"'{resolution.contains_live_revalidation}' observed "
            f"'{review.contains_live_revalidation}'"
        )
    if mismatches:
        raise GovernanceStatusDerivationError(
            status_code=409,
            detail=(
                "Current governance-status chain is inconsistent between resolution and review: "
                + "; ".join(mismatches)
            ),
        )


def _validate_review_against_gate(*, review, gate) -> None:
    mismatches: list[str] = []
    if review.gate_decision_id != gate.gate_decision_id:
        mismatches.append(
            f"gate_decision_id expected '{review.gate_decision_id}' observed '{gate.gate_decision_id}'"
        )
    if review.gate_key != gate.gate_key:
        mismatches.append(
            f"gate_key expected '{review.gate_key}' observed '{gate.gate_key}'"
        )
    if review.gate_definition_version != gate.gate_definition_version:
        mismatches.append(
            "gate_definition_version expected "
            f"'{review.gate_definition_version}' observed "
            f"'{gate.gate_definition_version}'"
        )
    if review.evaluation_pack_key != gate.evaluation_pack_key:
        mismatches.append(
            "evaluation_pack_key expected "
            f"'{review.evaluation_pack_key}' observed "
            f"'{gate.evaluation_pack_key}'"
        )
    if review.observed_gate_verdict != gate.overall_verdict:
        mismatches.append(
            "observed_gate_verdict expected "
            f"'{review.observed_gate_verdict}' observed '{gate.overall_verdict}'"
        )
    if review.contains_live_revalidation != gate.contains_live_revalidation:
        mismatches.append(
            "contains_live_revalidation expected "
            f"'{review.contains_live_revalidation}' observed "
            f"'{gate.contains_live_revalidation}'"
        )
    if mismatches:
        raise GovernanceStatusDerivationError(
            status_code=409,
            detail=(
                "Current governance-status chain is inconsistent between review and gate: "
                + "; ".join(mismatches)
            ),
        )
