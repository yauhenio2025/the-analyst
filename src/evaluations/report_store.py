"""File-backed persistence for evaluation reports."""

from __future__ import annotations

from pathlib import Path
from typing import Optional
from uuid import uuid4

from src.evaluations.schemas import (
    EvaluationReportSummary,
    PersistedEvaluationReport,
)


EVALUATION_REPORTS_DIR = Path(__file__).parent / "reports"


def build_evaluation_report_id() -> str:
    """Create one analyzer-owned evaluation report id."""

    return f"evaluation-report-{uuid4().hex[:12]}"


def save_evaluation_report(report: PersistedEvaluationReport) -> PersistedEvaluationReport:
    """Persist one evaluation report."""

    EVALUATION_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = EVALUATION_REPORTS_DIR / f"{report.evaluation_report_id}.json"
    report_path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return report


def load_evaluation_report(evaluation_report_id: str) -> Optional[PersistedEvaluationReport]:
    """Load one evaluation report by id."""

    normalized_id = evaluation_report_id.strip()
    if not normalized_id:
        return None
    report_path = EVALUATION_REPORTS_DIR / f"{normalized_id}.json"
    if not report_path.exists():
        return None
    return PersistedEvaluationReport.model_validate_json(
        report_path.read_text(encoding="utf-8")
    )


def list_evaluation_reports(
    *,
    evaluation_pack_key: Optional[str] = None,
    case_key: Optional[str] = None,
    limit: int = 20,
) -> list[EvaluationReportSummary]:
    """List persisted evaluation report summaries newest-first."""

    reports: list[EvaluationReportSummary] = []
    if not EVALUATION_REPORTS_DIR.exists():
        return reports

    for report_path in sorted(EVALUATION_REPORTS_DIR.glob("evaluation-report-*.json")):
        report = PersistedEvaluationReport.model_validate_json(
            report_path.read_text(encoding="utf-8")
        )
        if evaluation_pack_key and report.evaluation_pack_key != evaluation_pack_key:
            continue
        if case_key and report.case_key != case_key:
            continue
        reports.append(summarize_evaluation_report(report))

    reports.sort(key=lambda item: item.created_at, reverse=True)
    return reports[: max(limit, 0)]


def summarize_evaluation_report(report: PersistedEvaluationReport) -> EvaluationReportSummary:
    """Project a persisted report into its lightweight summary row."""

    return EvaluationReportSummary(
        evaluation_report_id=report.evaluation_report_id,
        created_at=report.created_at,
        evaluation_pack_key=report.evaluation_pack_key,
        case_key=report.case_key,
        subject_kind=report.subject_kind,
        subject_identity=report.subject_identity,
        workflow_key=report.workflow_key,
        consumer_key=report.consumer_key,
        overall_verdict=report.overall_verdict,
    )
