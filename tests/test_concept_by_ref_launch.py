from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
root_str = str(ROOT)
if root_str in sys.path:
    sys.path.remove(root_str)
sys.path.insert(0, root_str)

from src.orchestrator.concept_by_ref import run_concept_analysis_by_ref
from src.orchestrator.pipeline_schemas import ConceptAnalysisByRefRequest


def test_run_concept_analysis_by_ref_builds_single_phase_job(monkeypatch):
    captured: dict[str, object] = {}

    monkeypatch.setattr(
        "src.orchestrator.concept_by_ref.load_registered_documents_in_order",
        lambda **_: [
            {
                "external_doc_key": "subject-main",
                "title": "Walter Main Text",
                "author": "Ryan Walter",
                "binding_role": "target",
                "text": "Main source text",
            },
            {
                "external_doc_key": "response-1",
                "title": "Response",
                "author": "Ryan Walter",
                "binding_role": "context",
                "text": "Response text",
            },
        ],
    )
    monkeypatch.setattr(
        "src.orchestrator.concept_by_ref.store_document",
        lambda **_: "doc-packet-1",
    )

    def _save_plan(plan):
        captured["plan"] = plan

    monkeypatch.setattr("src.orchestrator.concept_by_ref._save_plan", _save_plan)
    monkeypatch.setattr(
        "src.orchestrator.concept_by_ref.create_job",
        lambda **kwargs: {
            "job_id": kwargs["job_id"],
            "cancel_token": "token-123",
        },
    )
    monkeypatch.setattr(
        "src.orchestrator.concept_by_ref.start_execution_thread",
        lambda **kwargs: captured.setdefault("thread", kwargs),
    )

    request = ConceptAnalysisByRefRequest(
        consumer_key="the-critic",
        external_project_id="walter-demo",
        concept_name="history",
        analysis_mode="logical",
        workflow_key="concept_logical_single_concept",
        external_doc_keys=["subject-main", "response-1"],
        project_id="walter-demo",
        subject_author="Ryan Walter",
        subject_name="Ryan Walter on Doctrine",
    )

    response = run_concept_analysis_by_ref(request)

    plan = captured["plan"]
    assert plan.workflow_key == "concept_logical_single_concept"
    assert len(plan.phases) == 1
    assert plan.phases[0].phase_name == "Logical Concept Analysis"
    assert plan.phases[0].depth == "deep"
    assert response.workflow_key == "concept_logical_single_concept"
    assert response.analysis_mode == "logical"
    assert response.concept_name == "history"
    assert response.plan_id == plan.plan_id
    assert response.cancel_token == "token-123"
    assert captured["thread"]["document_ids"] == {"target": "doc-packet-1"}
