import asyncio
from types import SimpleNamespace
from unittest.mock import patch

from src.api.routes.orchestrator import get_analysis
from src.presenter.renderer_contract_enforcement import ServedIntent


def test_completed_orchestrator_analysis_uses_explicit_presentation_consumer_and_intent():
    captured: dict[str, object] = {}

    def _assemble_page(job_id: str, *, consumer_key: str, served_intent: ServedIntent):
        captured.update(
            {
                "job_id": job_id,
                "consumer_key": consumer_key,
                "served_intent": served_intent,
            }
        )
        return SimpleNamespace(
            model_dump=lambda: {
                "job_id": job_id,
                "consumer_key": consumer_key,
                "presentation_contract_version": 1,
            }
        )

    completed_job = {
        "job_id": "job-varoufakis-style-completed",
        "plan_id": "plan-varoufakis-style",
        "status": "completed",
        "workflow_key": "intellectual_genealogy",
    }

    with patch("src.executor.job_manager.get_job", return_value=completed_job), patch(
        "src.presenter.presentation_api.assemble_page",
        side_effect=_assemble_page,
    ):
        result = asyncio.run(get_analysis(completed_job["job_id"]))

    assert result["status"] == "completed"
    assert result["presentation"]["consumer_key"] == "the-critic"
    assert captured == {
        "job_id": completed_job["job_id"],
        "consumer_key": "the-critic",
        "served_intent": ServedIntent.PAGE_PREVIEW_FOR_ORCHESTRATOR_STATUS,
    }
