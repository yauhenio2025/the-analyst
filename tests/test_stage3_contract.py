"""Stage 3 result contract tests: restore, discovery, attach-project."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from src.analysis_products.result_contract import (
    ConflictError,
    _compute_restore,
    attach_project_to_job,
    build_discovery_summaries,
    build_result_manifest,
)
from src.analysis_products.schemas import AnalysisResultManifest, DiscoverySummary
from src.aoi.constants import AOI_WORKFLOW_KEY
from src.executor.db import execute, init_db
from src.executor.job_manager import create_job, get_job


# ---------------------------------------------------------------------------
# restore_available / restore_reason
# ---------------------------------------------------------------------------


class TestComputeRestore:
    def test_ready_with_completed_preparation(self):
        avail, reason = _compute_restore(
            result_state="ready",
            preparation_status="completed",
            job_status="completed",
        )
        assert avail is True
        assert reason == "presentation_ready"

    def test_stale_with_completed_preparation(self):
        # Revised contract: stale results are not restore-available
        avail, reason = _compute_restore(
            result_state="stale",
            preparation_status="completed",
            job_status="completed",
        )
        assert avail is False
        assert reason == "presentation_stale"

    def test_legacy_untracked_with_completed_preparation(self):
        # Revised contract: legacy_untracked is never restore-available
        avail, reason = _compute_restore(
            result_state="legacy_untracked",
            preparation_status="completed",
            job_status="completed",
        )
        assert avail is False
        assert reason == "legacy_untracked"

    def test_legacy_untracked_without_preparation(self):
        avail, reason = _compute_restore(
            result_state="legacy_untracked",
            preparation_status="not_started",
            job_status="completed",
        )
        assert avail is False
        assert reason == "legacy_untracked"

    def test_failed_job(self):
        avail, reason = _compute_restore(
            result_state="failed",
            preparation_status="not_started",
            job_status="failed",
        )
        assert avail is False
        assert reason == "failed"

    def test_failed_preparation(self):
        avail, reason = _compute_restore(
            result_state="failed",
            preparation_status="failed",
            job_status="completed",
        )
        assert avail is False
        assert reason == "failed"

    def test_preparing_job(self):
        avail, reason = _compute_restore(
            result_state="preparing",
            preparation_status="running",
            job_status="running",
        )
        assert avail is False
        assert reason == "preparing"

    def test_not_prepared(self):
        # Stale check fires before preparation_status check
        avail, reason = _compute_restore(
            result_state="stale",
            preparation_status="not_started",
            job_status="completed",
        )
        assert avail is False
        assert reason == "presentation_stale"

    def test_not_prepared_non_stale(self):
        avail, reason = _compute_restore(
            result_state="ready",
            preparation_status="not_started",
            job_status="completed",
        )
        assert avail is False
        assert reason == "not_prepared"


def _mock_completed_manifest(monkeypatch, *, result_state="ready", preparation_status="completed"):
    """Set up monkeypatches for a completed job manifest."""
    monkeypatch.setattr(
        "src.analysis_products.result_contract.get_job",
        lambda job_id: {
            "job_id": job_id,
            "plan_id": "plan-1",
            "workflow_key": "intellectual_genealogy",
            "status": "completed",
        },
    )
    monkeypatch.setattr(
        "src.analysis_products.result_contract.lookup_job_corpus",
        lambda job_id: "corp-1",
    )
    monkeypatch.setattr(
        "src.analysis_products.result_contract.load_effective_plan_context",
        lambda job_id, plan_id=None: SimpleNamespace(plan=object(), source="job_plan_data"),
    )
    monkeypatch.setattr(
        "src.analysis_products.result_contract.get_preparation_state",
        lambda job_id: {
            "status": preparation_status,
            "detail": "Ready",
            "active": False,
        },
    )
    if preparation_status == "completed":
        monkeypatch.setattr(
            "src.analysis_products.result_contract.build_presentation_manifest",
            lambda job_id, consumer_key, slim=True, read_only=True: SimpleNamespace(
                presentation_contract_version=1,
                presentation_hash="hash-1",
                presentation_content_hash="content-1",
                prepared_at="2026-03-16T10:00:00+00:00",
                artifacts_ready=True,
            ),
        )
    monkeypatch.setattr(
        "src.analysis_products.result_contract.summarize_job_artifacts",
        lambda job_id, preparation_status=None, ensure_corpus=False: [],
    )


def test_manifest_includes_restore_fields_when_ready(monkeypatch):
    _mock_completed_manifest(monkeypatch)
    manifest = build_result_manifest("job-1", consumer_key="the-critic")
    assert manifest.restore_available is True
    assert manifest.restore_reason == "presentation_ready"


def test_manifest_restore_unavailable_when_not_prepared(monkeypatch):
    _mock_completed_manifest(monkeypatch, preparation_status="not_started")
    manifest = build_result_manifest("job-1", consumer_key="the-critic")
    assert manifest.restore_available is False
    assert manifest.restore_reason == "preparing"


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def _aoi_plan_data():
    return {
        "workflow_key": AOI_WORKFLOW_KEY,
        "objective_key": "influence_thematic",
        "thinker_name": "Aaron Benanav",
        "selected_source_thinker_id": "otto_neurath",
        "selected_source_thinker_name": "Otto Neurath",
        "target_work": {"title": "Beyond Capitalism", "author": "Aaron Benanav"},
        "prior_works": [],
    }


def test_discovery_filters_by_project_and_workflow(monkeypatch):
    """Discovery returns only completed jobs matching project+workflow filters."""
    init_db()

    job_ids = []
    try:
        # Create two completed jobs: one matching, one not
        j1 = f"job-disc-match-{uuid4().hex[:8]}"
        j2 = f"job-disc-other-{uuid4().hex[:8]}"
        job_ids.extend([j1, j2])

        create_job(j1, "plan-1", plan_data=_aoi_plan_data(),
                    workflow_key=AOI_WORKFLOW_KEY, project_id="proj-1")
        create_job(j2, "plan-2", plan_data=_aoi_plan_data(),
                    workflow_key=AOI_WORKFLOW_KEY, project_id="proj-2")

        # Mark both completed
        from src.executor.job_manager import update_job_status
        update_job_status(j1, "completed")
        update_job_status(j2, "completed")

        summaries = build_discovery_summaries(
            project_id="proj-1",
            workflow_key=AOI_WORKFLOW_KEY,
            consumer_key="the-critic",
        )

        assert len(summaries) == 1
        assert summaries[0].job_id == j1
        assert summaries[0].project_id == "proj-1"
        assert isinstance(summaries[0], DiscoverySummary)
    finally:
        for jid in job_ids:
            execute("DELETE FROM analysis_artifacts WHERE job_id = %s", (jid,))
            execute("DELETE FROM executor_jobs WHERE job_id = %s", (jid,))


def test_discovery_filters_by_thinker_id(monkeypatch):
    """Discovery can filter AOI results by selected_source_thinker_id."""
    init_db()

    job_ids = []
    try:
        j1 = f"job-thinker-a-{uuid4().hex[:8]}"
        j2 = f"job-thinker-b-{uuid4().hex[:8]}"
        job_ids.extend([j1, j2])

        plan_a = {**_aoi_plan_data(), "selected_source_thinker_id": "neurath"}
        plan_b = {**_aoi_plan_data(), "selected_source_thinker_id": "popper"}

        create_job(j1, "plan-a", plan_data=plan_a,
                    workflow_key=AOI_WORKFLOW_KEY, project_id="proj-1")
        create_job(j2, "plan-b", plan_data=plan_b,
                    workflow_key=AOI_WORKFLOW_KEY, project_id="proj-1")

        from src.executor.job_manager import update_job_status
        update_job_status(j1, "completed")
        update_job_status(j2, "completed")

        summaries = build_discovery_summaries(
            project_id="proj-1",
            workflow_key=AOI_WORKFLOW_KEY,
            selected_source_thinker_id="neurath",
        )

        assert len(summaries) == 1
        assert summaries[0].job_id == j1
        assert summaries[0].selected_source_thinker_id == "neurath"
    finally:
        for jid in job_ids:
            execute("DELETE FROM analysis_artifacts WHERE job_id = %s", (jid,))
            execute("DELETE FROM executor_jobs WHERE job_id = %s", (jid,))


def test_discovery_does_not_assemble_pages(monkeypatch):
    """Discovery should not call assemble_page or build_presentation_manifest expensively."""
    init_db()

    job_id = f"job-disc-nopage-{uuid4().hex[:8]}"
    try:
        create_job(job_id, "plan-1", plan_data=_aoi_plan_data(),
                    workflow_key=AOI_WORKFLOW_KEY, project_id="proj-1")

        from src.executor.job_manager import update_job_status
        update_job_status(job_id, "completed")

        # Track whether assemble_page was called
        assemble_calls = []
        monkeypatch.setattr(
            "src.analysis_products.result_contract.assemble_page",
            lambda *a, **kw: assemble_calls.append(1),
        )

        summaries = build_discovery_summaries(
            project_id="proj-1",
            workflow_key=AOI_WORKFLOW_KEY,
        )

        # discovery uses build_result_manifest (which calls build_presentation_manifest
        # for completed preps), but NOT assemble_page
        assert assemble_calls == []
        assert len(summaries) >= 1
    finally:
        execute("DELETE FROM analysis_artifacts WHERE job_id = %s", (job_id,))
        execute("DELETE FROM executor_jobs WHERE job_id = %s", (job_id,))


def test_discovery_ordering_stable():
    """Discovery results should be ordered by completed_at DESC."""
    init_db()

    job_ids = []
    try:
        j1 = f"job-disc-ord1-{uuid4().hex[:8]}"
        j2 = f"job-disc-ord2-{uuid4().hex[:8]}"
        job_ids.extend([j1, j2])

        create_job(j1, "plan-1", plan_data=_aoi_plan_data(),
                    workflow_key=AOI_WORKFLOW_KEY, project_id="proj-ord")
        from src.executor.job_manager import update_job_status
        update_job_status(j1, "completed")

        create_job(j2, "plan-2", plan_data=_aoi_plan_data(),
                    workflow_key=AOI_WORKFLOW_KEY, project_id="proj-ord")
        update_job_status(j2, "completed")

        summaries = build_discovery_summaries(
            project_id="proj-ord",
            workflow_key=AOI_WORKFLOW_KEY,
        )

        # j2 was completed after j1, so should come first
        assert len(summaries) == 2
        assert summaries[0].job_id == j2
        assert summaries[1].job_id == j1
    finally:
        for jid in job_ids:
            execute("DELETE FROM analysis_artifacts WHERE job_id = %s", (jid,))
            execute("DELETE FROM executor_jobs WHERE job_id = %s", (jid,))


# ---------------------------------------------------------------------------
# Attach project
# ---------------------------------------------------------------------------


def test_attach_project_sets_null_project():
    init_db()
    job_id = f"job-attach-{uuid4().hex[:8]}"

    try:
        create_job(job_id, "plan-1", workflow_key="intellectual_genealogy")
        result = attach_project_to_job(job_id, "proj-attach-1")

        assert result.attached is True
        assert result.idempotent is False
        assert result.project_id == "proj-attach-1"

        # Verify in DB
        job = get_job(job_id)
        assert job["project_id"] == "proj-attach-1"
    finally:
        execute("DELETE FROM executor_jobs WHERE job_id = %s", (job_id,))


def test_attach_project_idempotent_same_project():
    init_db()
    job_id = f"job-attach-idem-{uuid4().hex[:8]}"

    try:
        create_job(job_id, "plan-1", project_id="proj-same",
                    workflow_key="intellectual_genealogy")
        result = attach_project_to_job(job_id, "proj-same")

        assert result.attached is False
        assert result.idempotent is True
    finally:
        execute("DELETE FROM executor_jobs WHERE job_id = %s", (job_id,))


def test_attach_project_conflict_different_project():
    init_db()
    job_id = f"job-attach-conf-{uuid4().hex[:8]}"

    try:
        create_job(job_id, "plan-1", project_id="proj-original",
                    workflow_key="intellectual_genealogy")

        with pytest.raises(ConflictError):
            attach_project_to_job(job_id, "proj-different")
    finally:
        execute("DELETE FROM executor_jobs WHERE job_id = %s", (job_id,))


def test_attach_project_not_found():
    with pytest.raises(ValueError, match="Job not found"):
        attach_project_to_job("nonexistent-job-id", "proj-1")


# ---------------------------------------------------------------------------
# Generic workflow discovery with missing corpus_ref
# ---------------------------------------------------------------------------


def test_discovery_generic_workflow_missing_corpus():
    """Generic workflows with missing corpus_ref still return discoverable summaries."""
    init_db()
    job_id = f"job-disc-generic-{uuid4().hex[:8]}"

    try:
        create_job(job_id, "plan-gen",
                    plan_data={"workflow_key": "intellectual_genealogy",
                               "target_work": {"title": "T", "author": "A"},
                               "prior_works": []},
                    workflow_key="intellectual_genealogy",
                    project_id="proj-gen")

        from src.executor.job_manager import update_job_status
        update_job_status(job_id, "completed")

        summaries = build_discovery_summaries(
            project_id="proj-gen",
            workflow_key="intellectual_genealogy",
        )

        assert len(summaries) == 1
        s = summaries[0]
        assert s.job_id == job_id
        # No corpus means stale/legacy — but still discoverable
        assert s.restore_reason in ("not_prepared", "preparing", "presentation_stale",
                                     "legacy_untracked", "presentation_ready")
    finally:
        execute("DELETE FROM analysis_artifacts WHERE job_id = %s", (job_id,))
        execute("DELETE FROM executor_jobs WHERE job_id = %s", (job_id,))
