import asyncio

import pytest
from fastapi import HTTPException

from src.api.routes.evaluations import (
    get_evaluation_report_endpoint,
    list_evaluation_reports_endpoint,
)
from src.evaluations.report_store import save_evaluation_report
from src.evaluations.schemas import PersistedEvaluationReport


def _report(report_id: str, *, created_at: str, case_key: str) -> PersistedEvaluationReport:
    return PersistedEvaluationReport(
        evaluation_report_id=report_id,
        created_at=created_at,
        evaluation_pack_key="phase4_frozen_governance_v1",
        case_key=case_key,
        subject_kind="executor_job",
        subject_identity="job-744edf255ad5",
        workflow_key="anxiety_of_influence_thematic_single_thinker",
        consumer_key="the-critic",
        overall_verdict="pass",
    )


def test_get_evaluation_report_endpoint_returns_report(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )
    report = save_evaluation_report(
        _report(
            "evaluation-report-route",
            created_at="2026-03-29T01:00:00+00:00",
            case_key="aoi_exemplar_march27_execution_backed",
        )
    )

    fetched = asyncio.run(get_evaluation_report_endpoint(report.evaluation_report_id))

    assert fetched.evaluation_report_id == report.evaluation_report_id
    assert fetched.case_key == "aoi_exemplar_march27_execution_backed"


def test_list_evaluation_reports_endpoint_returns_filtered_summaries(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )
    save_evaluation_report(
        _report(
            "evaluation-report-a",
            created_at="2026-03-29T00:00:00+00:00",
            case_key="aoi_exemplar_march27_execution_backed",
        )
    )
    save_evaluation_report(
        _report(
            "evaluation-report-b",
            created_at="2026-03-29T01:00:00+00:00",
            case_key="genealogy_lifecycle_march28_session_reopen",
        )
    )

    response = asyncio.run(
        list_evaluation_reports_endpoint(
            evaluation_pack_key="phase4_frozen_governance_v1",
            case_key="genealogy_lifecycle_march28_session_reopen",
            limit=10,
        )
    )

    assert response.count == 1
    assert response.reports[0].evaluation_report_id == "evaluation-report-b"


def test_get_evaluation_report_endpoint_returns_404_for_missing_report(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )

    with pytest.raises(HTTPException) as excinfo:
        asyncio.run(get_evaluation_report_endpoint("evaluation-report-missing"))

    assert excinfo.value.status_code == 404
