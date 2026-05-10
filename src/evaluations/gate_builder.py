"""Deterministic bounded release-gate builder and harness."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from typing import Optional

from src.evaluations.frozen_pack_definitions import get_frozen_pack_definition
from src.evaluations.frozen_pack_harness import run_frozen_pack
from src.evaluations.gate_definitions import get_evaluation_gate_definition
from src.evaluations.gate_schemas import (
    EvaluationGateCaseSummary,
    EvaluationGateDecisionSummary,
    GateDimensionVerdict,
    PersistedEvaluationGateDecision,
)
from src.evaluations.gate_store import (
    build_evaluation_gate_decision_id,
    save_evaluation_gate_decision,
)
from src.evaluations.report_store import load_evaluation_report
from src.evaluations.schemas import PersistedEvaluationReport


def build_evaluation_gate_decision(
    *,
    gate_key: str,
    evaluation_pack_key: str,
    input_report_ids_by_case_key: dict[str, str],
    save_decision: bool = True,
) -> PersistedEvaluationGateDecision:
    """Build one bounded gate decision over exact persisted report ids."""

    gate_definition = get_evaluation_gate_definition(gate_key)
    if evaluation_pack_key != gate_definition.evaluation_pack_key:
        raise ValueError(
            f"Gate '{gate_key}' requires evaluation_pack_key='{gate_definition.evaluation_pack_key}', "
            f"got '{evaluation_pack_key}'"
        )
    pack_definition = get_frozen_pack_definition(evaluation_pack_key)
    pack_cases = {case.case_key: case for case in pack_definition.cases}
    required_cases = gate_definition.rule_table.required_cases
    expected_case_keys = {case.case_key for case in required_cases}
    provided_case_keys = set(input_report_ids_by_case_key)

    case_summaries: list[EvaluationGateCaseSummary] = []
    blocking_reasons: list[str] = []
    contains_live_revalidation = False

    for unexpected_case_key in sorted(provided_case_keys - expected_case_keys):
        blocking_reasons.append(f"unexpected input case_key '{unexpected_case_key}' provided")

    for required_case in required_cases:
        case_summary = _evaluate_required_case(
            required_case=required_case,
            input_report_id=input_report_ids_by_case_key.get(required_case.case_key),
            pack_case=pack_cases.get(required_case.case_key),
            expected_pack_key=pack_definition.evaluation_pack_key,
        )
        case_summaries.append(case_summary)
        contains_live_revalidation = (
            contains_live_revalidation or case_summary.contains_live_revalidation
        )
        blocking_reasons.extend(
            f"{required_case.case_key}: {reason}" for reason in case_summary.blocking_reasons
        )

    gate_decision = PersistedEvaluationGateDecision(
        gate_decision_id=build_evaluation_gate_decision_id(),
        created_at=_now_iso(),
        gate_key=gate_definition.gate_key,
        gate_definition_version=gate_definition.gate_definition_version,
        evaluation_pack_key=gate_definition.evaluation_pack_key,
        input_report_ids_by_case_key=dict(input_report_ids_by_case_key),
        contains_live_revalidation=contains_live_revalidation,
        rule_table=gate_definition.rule_table,
        case_summaries=case_summaries,
        overall_verdict=_derive_gate_verdict(
            case_summaries=case_summaries,
            has_unexpected_inputs=bool(provided_case_keys - expected_case_keys),
        ),
        blocking_reasons=blocking_reasons,
    )
    if save_decision:
        save_evaluation_gate_decision(gate_decision)
    return gate_decision


def generate_then_build_evaluation_gate_decision(
    *,
    gate_key: str,
    evaluation_pack_key: str,
    save_reports: bool = True,
    save_decision: bool = True,
) -> PersistedEvaluationGateDecision:
    """Materialize fresh frozen-pack reports, then gate those exact ids."""

    reports = run_frozen_pack(evaluation_pack_key, save_report=save_reports)
    report_ids_by_case_key = {
        report.case_key: report.evaluation_report_id for report in reports
    }
    return build_evaluation_gate_decision(
        gate_key=gate_key,
        evaluation_pack_key=evaluation_pack_key,
        input_report_ids_by_case_key=report_ids_by_case_key,
        save_decision=save_decision,
    )


def _evaluate_required_case(
    *,
    required_case,
    input_report_id: Optional[str],
    pack_case,
    expected_pack_key: str,
) -> EvaluationGateCaseSummary:
    dimension_verdicts = {
        dimension_key: "missing" for dimension_key in required_case.required_dimensions
    }
    if pack_case is None:
        return EvaluationGateCaseSummary(
            case_key=required_case.case_key,
            dimension_verdicts=dimension_verdicts,
            case_verdict="error",
            blocking_reasons=["case definition is missing from the frozen evaluation pack"],
        )

    if not input_report_id:
        return EvaluationGateCaseSummary(
            case_key=required_case.case_key,
            subject_kind=pack_case.subject_kind,
            subject_identity=pack_case.subject_identity,
            workflow_key=pack_case.workflow_key,
            consumer_key=pack_case.consumer_key,
            dimension_verdicts=dimension_verdicts,
            case_verdict="error",
            blocking_reasons=["required report id was not provided"],
        )

    report = load_evaluation_report(input_report_id)
    if report is None:
        return EvaluationGateCaseSummary(
            case_key=required_case.case_key,
            evaluation_report_id=input_report_id,
            subject_kind=pack_case.subject_kind,
            subject_identity=pack_case.subject_identity,
            workflow_key=pack_case.workflow_key,
            consumer_key=pack_case.consumer_key,
            dimension_verdicts=dimension_verdicts,
            case_verdict="error",
            blocking_reasons=[f"report '{input_report_id}' was not found"],
        )

    dimension_verdicts = _collect_dimension_verdicts(report, required_case.required_dimensions)
    blocking_reasons, has_structural_mismatch = _validate_report_against_case_definition(
        report=report,
        required_case=required_case,
        pack_case=pack_case,
        expected_pack_key=expected_pack_key,
        dimension_verdicts=dimension_verdicts,
    )
    case_verdict = _derive_case_verdict(
        report=report,
        dimension_verdicts=dimension_verdicts,
        has_structural_mismatch=has_structural_mismatch,
    )

    return EvaluationGateCaseSummary(
        case_key=required_case.case_key,
        evaluation_report_id=report.evaluation_report_id,
        report_overall_verdict=report.overall_verdict,
        dimension_verdicts=dimension_verdicts,
        case_verdict=case_verdict,
        contains_live_revalidation=any(
            check.live_revalidation_performed for check in report.checks
        ),
        subject_kind=report.subject_kind,
        subject_identity=report.subject_identity,
        workflow_key=report.workflow_key,
        consumer_key=report.consumer_key,
        blocking_reasons=blocking_reasons,
    )


def _collect_dimension_verdicts(
    report: PersistedEvaluationReport,
    required_dimensions: list[str],
) -> dict[str, GateDimensionVerdict]:
    dimensions_by_key = {
        dimension.dimension_key: dimension for dimension in report.dimension_summaries
    }
    verdicts: dict[str, GateDimensionVerdict] = {}
    for dimension_key in required_dimensions:
        dimension = dimensions_by_key.get(dimension_key)
        verdicts[dimension_key] = dimension.status if dimension is not None else "missing"
    return verdicts


def _validate_report_against_case_definition(
    *,
    report: PersistedEvaluationReport,
    required_case,
    pack_case,
    expected_pack_key: str,
    dimension_verdicts: dict[str, GateDimensionVerdict],
) -> tuple[list[str], bool]:
    structural_reasons: list[str] = []
    substantive_reasons: list[str] = []

    if report.evaluation_pack_key != expected_pack_key:
        structural_reasons.append(
            f"report pack mismatch: expected '{expected_pack_key}', observed '{report.evaluation_pack_key}'"
        )
    if report.case_key != required_case.case_key:
        structural_reasons.append(
            f"report case_key mismatch: expected '{required_case.case_key}', observed '{report.case_key}'"
        )
    if report.subject_kind != pack_case.subject_kind:
        structural_reasons.append(
            f"report subject_kind mismatch: expected '{pack_case.subject_kind}', observed '{report.subject_kind}'"
        )
    if report.subject_identity != pack_case.subject_identity:
        structural_reasons.append(
            f"report subject_identity mismatch: expected '{pack_case.subject_identity}', observed '{report.subject_identity}'"
        )
    if report.workflow_key != pack_case.workflow_key:
        structural_reasons.append(
            f"report workflow_key mismatch: expected '{pack_case.workflow_key}', observed '{report.workflow_key}'"
        )
    if pack_case.consumer_key is not None and report.consumer_key != pack_case.consumer_key:
        structural_reasons.append(
            f"report consumer_key mismatch: expected '{pack_case.consumer_key}', observed '{report.consumer_key}'"
        )
    if report.overall_verdict != required_case.required_verdict:
        substantive_reasons.append(
            f"report overall_verdict='{report.overall_verdict}' does not satisfy required '{required_case.required_verdict}'"
        )
    for dimension_key, verdict in dimension_verdicts.items():
        if verdict == "missing":
            structural_reasons.append(f"required dimension '{dimension_key}' is missing")
        elif verdict == "fail":
            substantive_reasons.append(
                f"required dimension '{dimension_key}' has verdict 'fail'"
            )
        elif verdict == "error":
            substantive_reasons.append(
                f"required dimension '{dimension_key}' has verdict 'error'"
            )
        elif verdict == "not_applicable":
            substantive_reasons.append(
                f"required dimension '{dimension_key}' has verdict 'not_applicable'"
            )
    return structural_reasons + substantive_reasons, bool(structural_reasons)


def _derive_case_verdict(
    *,
    report: PersistedEvaluationReport,
    dimension_verdicts: dict[str, GateDimensionVerdict],
    has_structural_mismatch: bool,
) -> str:
    if has_structural_mismatch or any(verdict == "missing" for verdict in dimension_verdicts.values()):
        return "error"
    if report.overall_verdict == "error":
        return "error"
    if any(verdict == "error" for verdict in dimension_verdicts.values()):
        return "error"
    if report.overall_verdict == "fail":
        return "fail"
    if any(verdict in {"fail", "not_applicable"} for verdict in dimension_verdicts.values()):
        return "fail"
    return "pass"


def _derive_gate_verdict(
    *,
    case_summaries: list[EvaluationGateCaseSummary],
    has_unexpected_inputs: bool,
) -> str:
    if has_unexpected_inputs:
        return "error"
    if any(case.case_verdict == "error" for case in case_summaries):
        return "error"
    if any(case.case_verdict == "fail" for case in case_summaries):
        return "fail"
    return "pass"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_report_mapping(entries: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for entry in entries:
        if "=" not in entry:
            raise ValueError(f"Invalid --report-id entry '{entry}'. Expected case_key=report_id.")
        case_key, report_id = entry.split("=", 1)
        normalized_case_key = case_key.strip()
        normalized_report_id = report_id.strip()
        if not normalized_case_key or not normalized_report_id:
            raise ValueError(f"Invalid --report-id entry '{entry}'. Expected case_key=report_id.")
        if normalized_case_key in mapping:
            raise ValueError(
                f"Duplicate --report-id input for case_key '{normalized_case_key}' is not allowed."
            )
        mapping[normalized_case_key] = normalized_report_id
    return mapping


def main(argv: Optional[list[str]] = None) -> int:
    """CLI entrypoint for bounded release-gate decisions."""

    parser = argparse.ArgumentParser(description="Build one bounded release gate decision.")
    parser.add_argument("--gate-key", required=True, help="Evaluation gate key")
    parser.add_argument("--pack-key", required=True, help="Frozen evaluation pack key")
    parser.add_argument(
        "--report-id",
        action="append",
        default=[],
        help="Explicit case_key=evaluation_report_id input. Repeat once per case.",
    )
    parser.add_argument(
        "--generate-pack-reports",
        action="store_true",
        help="Materialize fresh frozen-pack reports, then build the gate over those exact ids.",
    )
    args = parser.parse_args(argv)

    if args.generate_pack_reports and args.report_id:
        raise SystemExit("Use either --generate-pack-reports or --report-id inputs, not both.")
    if not args.generate_pack_reports and not args.report_id:
        raise SystemExit("Provide either --generate-pack-reports or at least one --report-id.")

    if args.generate_pack_reports:
        gate_decision = generate_then_build_evaluation_gate_decision(
            gate_key=args.gate_key,
            evaluation_pack_key=args.pack_key,
            save_reports=True,
            save_decision=True,
        )
    else:
        gate_decision = build_evaluation_gate_decision(
            gate_key=args.gate_key,
            evaluation_pack_key=args.pack_key,
            input_report_ids_by_case_key=_parse_report_mapping(args.report_id),
            save_decision=True,
        )

    summary = EvaluationGateDecisionSummary(
        gate_decision_id=gate_decision.gate_decision_id,
        created_at=gate_decision.created_at,
        gate_key=gate_decision.gate_key,
        gate_definition_version=gate_decision.gate_definition_version,
        evaluation_pack_key=gate_decision.evaluation_pack_key,
        overall_verdict=gate_decision.overall_verdict,
        contains_live_revalidation=gate_decision.contains_live_revalidation,
    )
    print(summary.model_dump_json())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
