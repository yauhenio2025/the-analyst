"""Thin lowering adapter and proof harness for direct-sections composition handoff."""

from __future__ import annotations

from src.orchestrator.task_planning_schemas import (
    DirectSectionsCompositionHandoffPlan,
    PersistedTaskPlanningDecision,
)
from src.presenter.compose_from_intent import _PlannerSectionContext, _match_section_to_planner_row
from src.presenter.schemas import ComposeFromIntentRequest


class DirectSectionsLoweringError(RuntimeError):
    """Raised when a direct-sections handoff cannot be truthfully lowered."""


def lower_direct_sections_handoff_plan(
    handoff_plan: DirectSectionsCompositionHandoffPlan,
) -> ComposeFromIntentRequest:
    """Lower an internal direct-sections handoff into the thin public compose request."""

    if not handoff_plan.consumer_key:
        raise DirectSectionsLoweringError(
            "Direct-sections handoff is missing consumer_key for compose-from-intent lowering."
        )
    if len(handoff_plan.prose_sections) != len(handoff_plan.section_trace):
        raise DirectSectionsLoweringError(
            "Direct-sections handoff trace does not align with prose_sections."
        )

    for index, (section, trace_row) in enumerate(
        zip(handoff_plan.prose_sections, handoff_plan.section_trace),
        start=1,
    ):
        if trace_row.order != index:
            raise DirectSectionsLoweringError(
                "Direct-sections handoff trace order is not contiguous."
            )
        if trace_row.engine_key != section.engine_key or trace_row.title != section.title:
            raise DirectSectionsLoweringError(
                "Direct-sections handoff trace does not match lowered section identity."
            )
        inferred_row = _match_section_to_planner_row(
            _PlannerSectionContext(
                section_index=index - 1,
                engine_key=section.engine_key,
                title=section.title,
                prose=section.prose,
            )
        )
        if trace_row.role_hint and inferred_row.semantic_role != trace_row.role_hint:
            raise DirectSectionsLoweringError(
                "Direct-sections lowering would lose required semantic metadata; "
                f"expected role_hint='{trace_row.role_hint}' but inferred '{inferred_row.semantic_role}'."
            )

    return ComposeFromIntentRequest(
        workflow_key=handoff_plan.workflow_key,
        consumer_key=handoff_plan.consumer_key,
        user_intent=handoff_plan.resolved_intent_seed.strip(),
        prose_sections=[section.model_copy(deep=True) for section in handoff_plan.prose_sections],
    )


def lower_persisted_planning_snapshot(
    snapshot: PersistedTaskPlanningDecision,
) -> ComposeFromIntentRequest:
    """Lower a persisted planning snapshot into the thin compose request."""

    decision = snapshot.planning_decision
    handoff_plan = decision.direct_sections_composition_handoff_plan
    if (
        decision.planning_outcome_kind != "direct_sections_composition_handoff_plan"
        or handoff_plan is None
    ):
        raise DirectSectionsLoweringError(
            "Persisted planning snapshot does not contain a direct-sections composition handoff."
        )
    return lower_direct_sections_handoff_plan(handoff_plan)

