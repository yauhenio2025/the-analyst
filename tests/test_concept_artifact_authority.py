from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if root_str in sys.path:
    sys.path.remove(root_str)
sys.path.insert(0, root_str)

from src.api.routes.orchestrator import get_concept_analysis_by_ref_result
from src.executor import db as executor_db
from src.orchestrator import concept_artifact_authority as authority
from src.orchestrator.schemas import TargetWork, WorkflowExecutionPlan
from src.executor import workflow_runner


def _configure_temp_sqlite(monkeypatch, tmp_path: Path) -> Path:
    sqlite_path = tmp_path / "executor.db"
    monkeypatch.setattr(executor_db, "DATABASE_URL", "")
    monkeypatch.setattr(executor_db, "SQLITE_PATH", sqlite_path)
    monkeypatch.setattr(executor_db, "_initialized", False)
    return sqlite_path


def _insert_job(job_id: str, workflow_key: str = "concept_logical_single_concept") -> None:
    executor_db.init_db()
    executor_db.execute(
        """INSERT INTO executor_jobs
           (job_id, plan_id, status, workflow_key, created_at)
           VALUES (%s, %s, %s, %s, %s)""",
        (
            job_id,
            f"plan-{job_id}",
            "completed",
            workflow_key,
            "2026-04-06T00:00:00+00:00",
        ),
    )


def test_load_concept_translated_artifact_supports_exact_and_latest_validated(monkeypatch, tmp_path):
    _configure_temp_sqlite(monkeypatch, tmp_path)
    timestamps = iter(
        [
            "2026-04-06T10:00:00+00:00",
            "2026-04-06T11:00:00+00:00",
            "2026-04-06T12:00:00+00:00",
        ]
    )
    monkeypatch.setattr(authority, "_now_iso", lambda: next(timestamps))
    _insert_job("job-a")
    _insert_job("job-b")

    authority.upsert_concept_translated_artifact(
        consumer_key="the-critic",
        external_project_id="proj-1",
        concept_name="innovation",
        analysis_mode="logical",
        workflow_key="concept_logical_single_concept",
        engine_or_chain_key="concept_analysis_12_phase",
        depth="deep",
        analyzer_v2_job_id="job-a",
        translation_template_key="concept_logical_host_contract_extraction",
        contract_validation_status=authority.CONCEPT_ARTIFACT_VALIDATION_PASSED,
        translated_artifact={"synthesis": {"overall_assessment": "passed-row"}},
        validation_errors=[],
        analysis_context={"run": "passed"},
    )
    authority.upsert_concept_translated_artifact(
        consumer_key="the-critic",
        external_project_id="proj-1",
        concept_name="innovation",
        analysis_mode="logical",
        workflow_key="concept_logical_single_concept",
        engine_or_chain_key="concept_analysis_12_phase",
        depth="deep",
        analyzer_v2_job_id="job-b",
        translation_template_key="concept_logical_host_contract_extraction",
        contract_validation_status=authority.CONCEPT_ARTIFACT_VALIDATION_FAILED,
        translated_artifact={"synthesis": {"overall_assessment": "failed-row"}},
        validation_errors=["bad contract"],
        analysis_context={"run": "failed"},
    )

    exact = authority.load_concept_translated_artifact(
        consumer_key="the-critic",
        external_project_id="proj-1",
        concept_name="innovation",
        analysis_mode="logical",
        analyzer_v2_job_id="job-b",
    )
    assert exact is not None
    assert exact["analyzer_v2_job_id"] == "job-b"
    assert exact["contract_validation_status"] == authority.CONCEPT_ARTIFACT_VALIDATION_FAILED

    latest_validated = authority.load_concept_translated_artifact(
        consumer_key="the-critic",
        external_project_id="proj-1",
        concept_name="innovation",
        analysis_mode="logical",
    )
    assert latest_validated is not None
    assert latest_validated["analyzer_v2_job_id"] == "job-a"
    assert latest_validated["contract_validation_status"] == authority.CONCEPT_ARTIFACT_VALIDATION_PASSED


def test_materialize_concept_translated_artifact_stores_passed_row(monkeypatch, tmp_path):
    _configure_temp_sqlite(monkeypatch, tmp_path)
    monkeypatch.setattr(authority, "_now_iso", lambda: "2026-04-06T13:00:00+00:00")
    monkeypatch.setattr(
        authority,
        "get_job",
        lambda job_id: {
            "job_id": job_id,
            "workflow_key": "concept_logical_single_concept",
            "plan_data": {
                "_concept_by_ref_context": {
                    "consumer_key": "the-critic",
                    "external_project_id": "proj-2",
                    "concept_name": "history",
                    "analysis_mode": "logical",
                    "workflow_key": "concept_logical_single_concept",
                    "subject_author": "Ryan Walter",
                    "subject_name": "Walter Project",
                    "depth": "deep",
                    "external_doc_keys": ["subject-main"],
                }
            },
        },
    )
    monkeypatch.setattr(
        authority,
        "load_phase_outputs",
        lambda **_: [
            {
                "engine_key": "concept_argument_formalization",
                "pass_number": 1,
                "id": "out-1",
                "content": "phase output",
            }
        ],
    )
    monkeypatch.setattr(
        authority,
        "translate_logical_result",
        lambda **kwargs: {
            "synthesis": {"overall_assessment": "coherent"},
            "_analysis_provenance": {"execution_owner": "analyzer-v2", "analyzer_v2_job_id": kwargs["analyzer_job_id"]},
        },
    )
    _insert_job("job-logical-1")

    stored = authority.materialize_concept_translated_artifact("job-logical-1")

    assert stored is not None
    assert stored["analyzer_v2_job_id"] == "job-logical-1"
    assert stored["contract_validation_status"] == authority.CONCEPT_ARTIFACT_VALIDATION_PASSED
    assert stored["translated_artifact_json"]["synthesis"]["overall_assessment"] == "coherent"
    assert stored["analysis_context"]["external_project_id"] == "proj-2"


def test_execute_plan_materializes_concept_artifact_before_completion(monkeypatch):
    statuses: list[str] = []
    progress_details: list[str] = []
    materialized: list[str] = []

    plan = WorkflowExecutionPlan(
        plan_id=f"plan-{uuid4().hex[:8]}",
        workflow_key="concept_logical_single_concept",
        thinker_name="Ryan Walter",
        target_work=TargetWork(title="Doctrine", author="Ryan Walter", description="Target"),
        prior_works=[],
        strategy_summary="summary",
        phases=[],
        recommended_views=[],
        estimated_llm_calls=0,
        estimated_depth_profile="deep",
    )

    monkeypatch.setattr(workflow_runner, "load_plan", lambda *_: plan)
    monkeypatch.setattr(workflow_runner, "get_job", lambda *_: {"phase_results": {}})
    monkeypatch.setattr(workflow_runner, "is_cancelled", lambda *_: False)
    monkeypatch.setattr(workflow_runner, "clear_cancellation", lambda *_: None)
    monkeypatch.setattr(
        workflow_runner,
        "update_job_status",
        lambda _job_id, status, error=None: statuses.append(status),
    )
    monkeypatch.setattr(
        workflow_runner,
        "update_job_progress",
        lambda _job_id, **kwargs: progress_details.append(kwargs.get("detail") or ""),
    )
    monkeypatch.setattr(workflow_runner, "_run_auto_presentation", lambda *_: None)
    monkeypatch.setattr(
        workflow_runner,
        "materialize_concept_translated_artifact",
        lambda job_id: materialized.append(job_id) or {"artifact_id": "ok"},
    )

    workflow_runner.execute_plan("job-concept-1", plan.plan_id, plan_object=plan)

    assert materialized == ["job-concept-1"]
    assert "Materializing translated host artifact" in progress_details
    assert statuses[-1] == "completed"
    assert statuses.index("completed") > -1


def test_get_concept_analysis_by_ref_result_supports_exact_lookup(monkeypatch):
    monkeypatch.setattr(
        "src.api.routes.orchestrator.load_concept_translated_artifact",
        lambda **_: {
            "consumer_key": "the-critic",
            "external_project_id": "proj-3",
            "concept_name": "innovation",
            "analysis_mode": "inferential",
            "workflow_key": "concept_inferential_single_concept",
            "engine_or_chain_key": "inferential_commitment_mapper",
            "depth": "standard",
            "analyzer_v2_job_id": "job-inf-1",
            "translation_template_key": "concept_inferential_host_contract_extraction",
            "contract_validation_status": "passed",
            "validation_errors": [],
            "produced_at": "2026-04-06T14:00:00+00:00",
            "translated_artifact_json": {"synthesis": {"surface_presentation": "x"}},
        },
    )

    response = asyncio.run(
        get_concept_analysis_by_ref_result(
            consumer_key="the-critic",
            external_project_id="proj-3",
            concept_name="innovation",
            analysis_mode="inferential",
            analyzer_v2_job_id="job-inf-1",
        )
    )

    assert response.lookup_mode == "exact_run"
    assert response.analyzer_v2_job_id == "job-inf-1"
    assert response.translated_artifact["synthesis"]["surface_presentation"] == "x"


def test_parse_artifact_row_normalizes_datetime_fields():
    row = authority._parse_artifact_row(
        {
            "translated_artifact_json": {"synthesis": {}},
            "validation_errors": [],
            "analysis_context": {},
            "produced_at": datetime(2026, 4, 6, 16, 20, tzinfo=UTC),
            "updated_at": datetime(2026, 4, 6, 16, 21, tzinfo=UTC),
        }
    )

    assert row is not None
    assert row["produced_at"] == "2026-04-06T16:20:00+00:00"
    assert row["updated_at"] == "2026-04-06T16:21:00+00:00"
