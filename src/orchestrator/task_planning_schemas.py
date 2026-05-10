"""Schemas for Stage 9 route-plus-hydrate-plus-plan planning."""

from __future__ import annotations

from typing import Annotated, Any, Literal, Optional

from pydantic import Field

from src.orchestrator.pipeline_schemas import (
    AnalyzeByRefRequest,
    AnalyzeRequest,
    ChapterUpload,
    PriorWorkByRef,
    PriorWorkWithText,
    TargetChapterByRef,
)
from src.orchestrator.schemas import TargetWork, WorkflowExecutionPlan
from src.orchestrator.task_routing_schemas import (
    CompositionTaskRequest,
    CompositionTaskRoutingDecision,
    RoutingConfidence,
    StrictBaseModel,
)
from src.presenter.schemas import (
    AoiRejectedSourceInput,
    AoiSelectedSourceInput,
    ComposeFromIntentSectionInput,
)

PlanningOutcomeKind = Literal[
    "genealogy_execution_plan",
    "aoi_composition_handoff_plan",
    "direct_sections_composition_handoff_plan",
    "aoi_selection_blocked",
    "insufficient_context",
    "unsupported",
]
HydrationStatus = Literal["satisfied", "required", "unresolved"]
DownstreamReadiness = Literal[
    "ready_for_genealogy_execution",
    "ready_for_aoi_compose_handoff",
    "ready_for_direct_sections_compose_handoff",
    "blocked_for_aoi_selection",
    "needs_more_context",
    "unsupported",
]
AoiSelectionBlockedReasonCode = Literal[
    "no_usable_source_families",
    "llm_timeout",
    "llm_provider_failure",
    "llm_invalid_output",
    "llm_selection_failed_validation",
]


class RegisteredCorpusPlanningContext(StrictBaseModel):
    """Planner-ready context for genealogy planning over registered docs."""

    context_mode: Literal["registered_corpus"] = "registered_corpus"
    consumer_key: str
    external_project_id: str
    thinker_name: str
    target_work: TargetWork
    target_external_doc_key: str
    target_chapter_external_doc_keys: list[str] = Field(default_factory=list)
    prior_works: list[PriorWorkByRef] = Field(default_factory=list)
    context_external_doc_keys: list[str] = Field(default_factory=list)
    research_question: Optional[str] = None
    depth_preference: Optional[str] = None
    focus_hint: Optional[str] = None
    project_id: Optional[str] = None

    def to_analyze_by_ref_request(
        self,
        *,
        workflow_key: str,
        objective_key: str,
    ) -> AnalyzeByRefRequest:
        return AnalyzeByRefRequest(
            consumer_key=self.consumer_key,
            external_project_id=self.external_project_id,
            thinker_name=self.thinker_name,
            target_work=self.target_work,
            target_external_doc_key=self.target_external_doc_key,
            target_chapter_external_doc_keys=self.target_chapter_external_doc_keys,
            prior_works=self.prior_works,
            context_external_doc_keys=self.context_external_doc_keys,
            research_question=self.research_question,
            depth_preference=self.depth_preference,
            focus_hint=self.focus_hint,
            workflow_key=workflow_key,
            project_id=self.project_id,
            skip_plan_review=False,
            objective_key=objective_key,
        )


class InlineDocumentsPlanningContext(StrictBaseModel):
    """Planner-ready context for genealogy planning over inline documents."""

    context_mode: Literal["inline_documents"] = "inline_documents"
    thinker_name: str
    target_work: TargetWork
    target_work_text: str
    target_work_chapters: list[ChapterUpload] = Field(default_factory=list)
    prior_works: list[PriorWorkWithText] = Field(default_factory=list)
    research_question: Optional[str] = None
    depth_preference: Optional[str] = None
    focus_hint: Optional[str] = None
    project_id: Optional[str] = None

    def to_analyze_request(
        self,
        *,
        workflow_key: str,
        objective_key: str,
    ) -> AnalyzeRequest:
        return AnalyzeRequest(
            thinker_name=self.thinker_name,
            target_work=self.target_work,
            target_work_text=self.target_work_text,
            target_work_chapters=self.target_work_chapters,
            prior_works=self.prior_works,
            research_question=self.research_question,
            depth_preference=self.depth_preference,
            focus_hint=self.focus_hint,
            workflow_key=workflow_key,
            project_id=self.project_id,
            skip_plan_review=False,
            objective_key=objective_key,
        )


class SavedResultPlanningContext(StrictBaseModel):
    """Planner-ready context for bounded result-backed planning."""

    context_mode: Literal["saved_result"] = "saved_result"
    source_v2_job_id: Optional[str] = None
    consumer_key: Optional[str] = None


TaskPlanningContext = Annotated[
    RegisteredCorpusPlanningContext | InlineDocumentsPlanningContext | SavedResultPlanningContext,
    Field(discriminator="context_mode"),
]


class TaskPlanningRequest(StrictBaseModel):
    """Input for POST /v1/orchestrator/plan-task."""

    task_request: CompositionTaskRequest
    prior_routing_decision: Optional[CompositionTaskRoutingDecision] = None
    planning_context: Optional[TaskPlanningContext] = None
    persist_decision: bool = False


class PlanningTraceEntry(StrictBaseModel):
    """One coarse trace entry for planning."""

    stage: str
    details: dict[str, Any] = Field(default_factory=dict)


class RejectedPlanningAlternative(StrictBaseModel):
    """A bounded record explaining why another planning path was rejected."""

    alternative_key: str
    rejection_reason: str
    details: list[str] = Field(default_factory=list)


class AoiCompositionHandoffPlan(StrictBaseModel):
    """Bounded AOI handoff metadata over the Stage 7 source bridge."""

    workflow_key: str
    objective_key: str
    consumer_key: Optional[str] = None
    source_v2_job_id: str
    compose_entrypoint_kind: Literal["presenter.compose_from_selection"] = "presenter.compose_from_selection"
    selected_source_thinker_id: Optional[str] = None
    selected_source_thinker_name: Optional[str] = None
    selected_sources: list[AoiSelectedSourceInput] = Field(default_factory=list)
    rejected_sources: list[AoiRejectedSourceInput] = Field(default_factory=list)
    selection_summary: str = ""
    resolved_intent_seed: str = ""
    legacy_profile_equivalent: Optional[Literal["dossier", "comparison"]] = None
    expected_source_families: list[str] = Field(default_factory=list)
    available_source_families: list[str] = Field(default_factory=list)
    expected_producer_engines: list[str] = Field(default_factory=list)
    bridge_contract_targets: list[str] = Field(
        default_factory=lambda: ["CompositionSourceCatalog", "CompositionSourceSelection"]
    )
    allowed_profiles: list[str] = Field(default_factory=list)
    blocked_profiles: dict[str, list[str]] = Field(default_factory=dict)
    handoff_notes: list[str] = Field(default_factory=list)


class DirectSectionsSectionTrace(StrictBaseModel):
    """One bounded provenance record for a direct-sections handoff section."""

    order: int = Field(ge=1)
    engine_key: str
    title: str
    provenance_pointer: dict[str, Any] = Field(default_factory=dict)
    role_hint: Optional[str] = None
    rationale: str = ""


class DirectSectionsCompositionHandoffPlan(StrictBaseModel):
    """Workflow-neutral direct-sections handoff for transient composition."""

    workflow_key: str
    objective_key: str
    consumer_key: Optional[str] = None
    source_v2_job_id: str
    compose_entrypoint_kind: Literal["presenter.compose_from_intent"] = "presenter.compose_from_intent"
    resolved_intent_seed: str = ""
    prose_sections: list[ComposeFromIntentSectionInput] = Field(default_factory=list)
    section_trace: list[DirectSectionsSectionTrace] = Field(default_factory=list)
    handoff_notes: list[str] = Field(default_factory=list)


class TaskPlanningDecision(StrictBaseModel):
    """Analyzer-owned Stage 9 planning decision."""

    normalized_task_summary: str
    planning_decision_id: Optional[str] = None
    routing_decision: CompositionTaskRoutingDecision
    planning_outcome_kind: PlanningOutcomeKind
    planning_confidence: RoutingConfidence
    hydration_status: HydrationStatus
    required_hydration: list[str] = Field(default_factory=list)
    required_host_preparation: list[str] = Field(default_factory=list)
    downstream_readiness: DownstreamReadiness
    downstream_followup_contract: dict[str, Any] = Field(default_factory=dict)
    hydrated_document_ids: dict[str, str] = Field(default_factory=dict)
    workflow_execution_plan: Optional[WorkflowExecutionPlan] = None
    aoi_composition_handoff_plan: Optional[AoiCompositionHandoffPlan] = None
    direct_sections_composition_handoff_plan: Optional[DirectSectionsCompositionHandoffPlan] = None
    aoi_selection_blocked_reason_code: Optional[AoiSelectionBlockedReasonCode] = None
    aoi_selection_blocked_reason_detail: Optional[str] = None
    rejected_planning_alternatives: list[RejectedPlanningAlternative] = Field(default_factory=list)
    trace: list[PlanningTraceEntry] = Field(default_factory=list)


class PersistedTaskPlanningDecision(StrictBaseModel):
    """Immutable analyzer-owned planning snapshot used for stable host recovery."""

    planning_decision_id: str
    created_at: str
    workflow_key: Optional[str] = None
    consumer_key: Optional[str] = None
    selected_source_thinker_id: Optional[str] = None
    selected_source_thinker_name: Optional[str] = None
    source_v2_job_id: Optional[str] = None
    task_request: CompositionTaskRequest
    routing_decision: CompositionTaskRoutingDecision
    planning_decision: TaskPlanningDecision
