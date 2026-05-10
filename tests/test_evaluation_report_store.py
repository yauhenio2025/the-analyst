import pytest

from src.evaluations.report_store import (
    list_evaluation_reports,
    load_evaluation_report,
    save_evaluation_report,
)
from src.evaluations.schemas import PersistedEvaluationReport


def _report(
    report_id: str,
    *,
    created_at: str,
    evaluation_pack_key: str = "phase4_frozen_governance_v1",
    case_key: str = "case-a",
) -> PersistedEvaluationReport:
    return PersistedEvaluationReport(
        evaluation_report_id=report_id,
        created_at=created_at,
        evaluation_pack_key=evaluation_pack_key,
        case_key=case_key,
        subject_kind="compose_session",
        subject_identity="compose-session-123",
        workflow_key="intellectual_genealogy",
        consumer_key="the-critic",
        overall_verdict="pass",
    )


def test_evaluation_report_store_round_trips_and_lists_newest_first(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(
        "src.evaluations.report_store.EVALUATION_REPORTS_DIR",
        tmp_path,
    )

    older = save_evaluation_report(
        _report("evaluation-report-older", created_at="2026-03-29T00:00:00+00:00", case_key="case-older")
    )
    newer = save_evaluation_report(
        _report("evaluation-report-newer", created_at="2026-03-29T01:00:00+00:00", case_key="case-newer")
    )

    loaded = load_evaluation_report(older.evaluation_report_id)
    summaries = list_evaluation_reports(limit=10)

    assert loaded is not None
    assert loaded.evaluation_report_id == older.evaluation_report_id
    assert [summary.evaluation_report_id for summary in summaries] == [
        newer.evaluation_report_id,
        older.evaluation_report_id,
    ]


def test_evaluation_report_store_filters_by_pack_and_case(
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
            evaluation_pack_key="phase4_frozen_governance_v1",
            case_key="case-a",
        )
    )
    save_evaluation_report(
        _report(
            "evaluation-report-b",
            created_at="2026-03-29T01:00:00+00:00",
            evaluation_pack_key="other-pack",
            case_key="case-b",
        )
    )

    filtered = list_evaluation_reports(
        evaluation_pack_key="phase4_frozen_governance_v1",
        case_key="case-a",
        limit=10,
    )

    assert len(filtered) == 1
    assert filtered[0].evaluation_report_id == "evaluation-report-a"
