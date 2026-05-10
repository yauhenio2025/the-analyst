"""Bounded analyzer-side saved-result bridge for genealogy direct-sections handoff."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from src.engines.discovery import (
    CapabilityMetadataResolutionError,
    resolve_composition_role,
)
from src.engines.registry import get_engine_registry
from src.executor.job_manager import get_job
from src.executor.output_store import load_phase_outputs
from src.orchestrator.task_planning_schemas import (
    DirectSectionsCompositionHandoffPlan,
    DirectSectionsSectionTrace,
)
from src.presenter.schemas import ComposeFromIntentSectionInput

GENEALOGY_WORKFLOW_KEY = "intellectual_genealogy"
_MAX_GENEALOGY_DIRECT_SECTIONS = 4


class GenealogySavedResultBridgeError(RuntimeError):
    """Raised when a saved genealogy result cannot support bounded direct sections."""


@dataclass(frozen=True)
class _PreferredGenealogySection:
    engine_keys: tuple[str, ...]
    default_title: str
    rationale: str


_PREFERRED_GENEALOGY_SECTION_ORDER: tuple[_PreferredGenealogySection, ...] = (
    _PreferredGenealogySection(
        engine_keys=("genealogy_relationship_classification", "genealogy_pass1b_relationship_classification"),
        default_title="Relationship Comparison Map",
        rationale=(
            "Derived from the analyzer-owned relationship-classification output already saved for the genealogy result."
        ),
    ),
    _PreferredGenealogySection(
        engine_keys=("genealogy_final_synthesis", "genealogy_pass7_final_synthesis"),
        default_title="Genealogy Report",
        rationale=(
            "Derived from the analyzer-owned final genealogy synthesis output already saved for the result."
        ),
    ),
)


def build_genealogy_saved_result_handoff_plan(
    *,
    source_v2_job_id: str,
    task_text: str,
    consumer_key: Optional[str],
    workflow_key: str = GENEALOGY_WORKFLOW_KEY,
    objective_key: str = "genealogical",
) -> DirectSectionsCompositionHandoffPlan:
    """Build one bounded direct-sections handoff from analyzer-owned saved-result truth."""

    job = get_job(source_v2_job_id)
    if job is None:
        raise GenealogySavedResultBridgeError(
            f"Saved genealogy result '{source_v2_job_id}' was not found."
        )
    if (job.get("workflow_key") or "") != GENEALOGY_WORKFLOW_KEY:
        raise GenealogySavedResultBridgeError(
            f"Saved result '{source_v2_job_id}' is not an intellectual_genealogy run."
        )
    if (job.get("status") or "") != "completed":
        raise GenealogySavedResultBridgeError(
            f"Saved result '{source_v2_job_id}' is not completed and cannot support direct-sections composition."
        )

    prose_sections, section_trace = extract_genealogy_saved_result_sections(source_v2_job_id)
    if not prose_sections:
        raise GenealogySavedResultBridgeError(
            f"Saved result '{source_v2_job_id}' did not yield any analyzer-owned genealogy sections."
        )

    return DirectSectionsCompositionHandoffPlan(
        workflow_key=workflow_key,
        objective_key=objective_key,
        consumer_key=consumer_key,
        source_v2_job_id=source_v2_job_id,
        resolved_intent_seed=task_text.strip(),
        prose_sections=prose_sections,
        section_trace=section_trace,
        handoff_notes=[
            "Derived only from analyzer-owned saved-result truth; no analysis rerun and no host-local semantic reconstruction.",
            "Lower through the thin compose-from-intent adapter only; do not widen the presenter boundary in this slice.",
        ],
    )


def extract_genealogy_saved_result_sections(
    source_v2_job_id: str,
) -> tuple[list[ComposeFromIntentSectionInput], list[DirectSectionsSectionTrace]]:
    """Extract 1-4 truthful genealogy sections from analyzer-owned saved-result outputs."""

    latest_outputs = _latest_phase_outputs_by_engine(source_v2_job_id)
    engine_registry = get_engine_registry()
    prose_sections: list[ComposeFromIntentSectionInput] = []
    trace_rows: list[DirectSectionsSectionTrace] = []

    for spec in _PREFERRED_GENEALOGY_SECTION_ORDER:
        output_row = _first_matching_output(spec.engine_keys, latest_outputs)
        if output_row is None:
            continue

        prose = str(output_row.get("content") or "").strip()
        if not prose:
            continue

        engine_key = str(output_row.get("engine_key") or "").strip()
        title = _derive_section_title(engine_key, spec.default_title, engine_registry)
        role_hint = _resolve_section_role_hint(engine_registry, engine_key)
        order = len(prose_sections) + 1
        prose_sections.append(
            ComposeFromIntentSectionInput(
                engine_key=engine_key,
                title=title,
                prose=prose,
            )
        )
        trace_rows.append(
            DirectSectionsSectionTrace(
                order=order,
                engine_key=engine_key,
                title=title,
                provenance_pointer={
                    "job_id": source_v2_job_id,
                    "output_id": output_row.get("id"),
                    "phase_number": output_row.get("phase_number"),
                    "pass_number": output_row.get("pass_number"),
                    "engine_key": engine_key,
                },
                role_hint=role_hint,
                rationale=spec.rationale,
            )
        )

    if len(prose_sections) > _MAX_GENEALOGY_DIRECT_SECTIONS:
        raise GenealogySavedResultBridgeError(
            "Genealogy saved-result section extraction exceeded the bounded 4-section cap."
        )
    return prose_sections, trace_rows


def _latest_phase_outputs_by_engine(job_id: str) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in load_phase_outputs(job_id=job_id):
        engine_key = str(row.get("engine_key") or "").strip()
        if not engine_key:
            continue
        current = latest.get(engine_key)
        if current is None or _is_newer_output(row, current):
            latest[engine_key] = row
    return latest


def _is_newer_output(candidate: dict[str, Any], current: dict[str, Any]) -> bool:
    candidate_pass = int(candidate.get("pass_number") or 0)
    current_pass = int(current.get("pass_number") or 0)
    if candidate_pass != current_pass:
        return candidate_pass > current_pass
    return str(candidate.get("id") or "") > str(current.get("id") or "")


def _first_matching_output(
    engine_keys: tuple[str, ...],
    latest_outputs: dict[str, dict[str, Any]],
) -> Optional[dict[str, Any]]:
    for engine_key in engine_keys:
        match = latest_outputs.get(engine_key)
        if match is not None:
            return match
    return None


def _resolve_section_role_hint(engine_registry: Any, engine_key: str) -> str:
    try:
        return resolve_composition_role(engine_registry, engine_key)
    except CapabilityMetadataResolutionError as exc:
        raise GenealogySavedResultBridgeError(
            "Saved genealogy result cannot emit a truthful role_hint for "
            f"engine '{engine_key}': {exc}"
        ) from exc


def _derive_section_title(engine_key: str, default_title: str, engine_registry: Any) -> str:
    if default_title.strip():
        return default_title
    capability = engine_registry.get_capability_definition(engine_key)
    if capability is not None and getattr(capability, "engine_name", None):
        return str(capability.engine_name).strip()
    engine = engine_registry.get(engine_key)
    if engine is not None and getattr(engine, "engine_name", None):
        return str(engine.engine_name).strip()
    return engine_key.replace("_", " ").strip().title()
