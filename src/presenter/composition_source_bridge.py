"""AOI source-to-composition bridge for transient compose-from-source."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from src.analysis_products.store import load_aoi_normalized_artifact
from src.aoi.constants import AOI_WORKFLOW_KEY
from src.aoi.contract import (
    AOI_ENGAGEMENT_MAPPING_ENGINE,
    AOI_SIN_FINDINGS_ENGINE,
    AOI_THEMATIC_REPORT_ENGINE,
    AOI_THEMATIC_SYNTHESIS_ENGINE,
)
from src.engines.discovery import (
    CapabilityMetadataResolutionError,
    resolve_composition_role,
)
from src.engines.registry import get_engine_registry
from src.executor.job_manager import get_job
from src.executor.output_store import load_phase_outputs
from src.executor.plan_context import load_effective_plan_context
from src.objectives.registry import get_objective
from src.presenter.schemas import (
    AoiRejectedSourceInput,
    AoiSelectedSourceInput,
    ComposeFromIntentSectionInput,
    ComposeFromSourceProfile,
)

AOI_DEFAULT_OBJECTIVE_KEY = "influence_thematic"

CandidateState = Literal["available", "unavailable", "invalid"]
SourceBackendKind = Literal["artifact", "phase_output_metadata", "normalized_report_payload"]

SOURCE_FAMILY_THEMATIC_SYNTHESIS = "thematic_synthesis"
SOURCE_FAMILY_ENGAGEMENT_MAPPING = "engagement_mapping"
SOURCE_FAMILY_SIN_FINDINGS = "sin_findings"
SOURCE_FAMILY_THEMATIC_REPORT = "thematic_report"

_SOURCE_FAMILY_ORDER = {
    SOURCE_FAMILY_THEMATIC_SYNTHESIS: 1,
    SOURCE_FAMILY_ENGAGEMENT_MAPPING: 2,
    SOURCE_FAMILY_SIN_FINDINGS: 3,
    SOURCE_FAMILY_THEMATIC_REPORT: 4,
}

_SOURCE_FAMILY_DEFINITIONS = {
    SOURCE_FAMILY_THEMATIC_SYNTHESIS: {
        "engine_key": AOI_THEMATIC_SYNTHESIS_ENGINE,
        "title": "Thematic Synthesis",
        "source_backend_kind": "artifact",
    },
    SOURCE_FAMILY_ENGAGEMENT_MAPPING: {
        "engine_key": AOI_ENGAGEMENT_MAPPING_ENGINE,
        "title": "Engagement Mapping",
        "source_backend_kind": "artifact",
    },
    SOURCE_FAMILY_SIN_FINDINGS: {
        "engine_key": AOI_SIN_FINDINGS_ENGINE,
        "title": "Sin Findings",
        "source_backend_kind": "artifact",
    },
    SOURCE_FAMILY_THEMATIC_REPORT: {
        "engine_key": AOI_THEMATIC_REPORT_ENGINE,
        "title": "AOI Report",
        "source_backend_kind": "phase_output_metadata",
    },
}

_PROFILE_SELECTION_PRESETS = {
    "dossier": [
        (
            SOURCE_FAMILY_THEMATIC_SYNTHESIS,
            1,
            "Selected by the dossier preset to foreground the high-level thematic synthesis.",
        ),
        (
            SOURCE_FAMILY_THEMATIC_REPORT,
            2,
            "Selected by the dossier preset as the structured report closeout.",
        ),
    ],
    "comparison": [
        (
            SOURCE_FAMILY_ENGAGEMENT_MAPPING,
            1,
            "Selected by the comparison preset to open with the engagement map.",
        ),
        (
            SOURCE_FAMILY_SIN_FINDINGS,
            2,
            "Selected by the comparison preset to surface the findings bank after engagement.",
        ),
        (
            SOURCE_FAMILY_THEMATIC_REPORT,
            3,
            "Selected by the comparison preset as the structured report closeout.",
        ),
    ],
}


class ComposeFromSourceResolutionError(ValueError):
    """Source-backed compose could not resolve required AOI source material."""


@dataclass(frozen=True)
class CompositionSourceCandidate:
    source_family_key: str
    engine_key: str
    title: str
    source_backend_kind: SourceBackendKind
    candidate_state: CandidateState
    provenance_pointer: dict[str, Any] = field(default_factory=dict)
    composition_role_hint: str = ""
    summary_metadata: dict[str, Any] = field(default_factory=dict)
    plan_context_enrichment: dict[str, Any] = field(default_factory=dict)
    resolution_note: str = ""
    materialization_payload: Any = None

    def to_trace_dict(self) -> dict[str, Any]:
        payload = {
            "source_family_key": self.source_family_key,
            "engine_key": self.engine_key,
            "title": self.title,
            "source_backend_kind": self.source_backend_kind,
            "candidate_state": self.candidate_state,
            "provenance_pointer": self.provenance_pointer,
            "composition_role_hint": self.composition_role_hint,
            "summary_metadata": self.summary_metadata,
            "plan_context": self.plan_context_enrichment,
        }
        if self.resolution_note:
            payload["resolution_note"] = self.resolution_note
        return payload


@dataclass(frozen=True)
class CompositionSourceCatalog:
    source_v2_job_id: str
    workflow_key: str
    objective_key: str
    objective_source: str
    plan_context_found: bool
    plan_context_source: str
    selected_source_thinker_id: Optional[str]
    selected_source_thinker_name: Optional[str]
    candidates: list[CompositionSourceCandidate]
    plan_source_mismatches: list[dict[str, Any]] = field(default_factory=list)

    def to_trace_dict(self) -> dict[str, Any]:
        details: dict[str, Any] = {
            "source_v2_job_id": self.source_v2_job_id,
            "workflow_key": self.workflow_key,
            "objective_key": self.objective_key,
            "objective_source": self.objective_source,
            "plan_context_found": self.plan_context_found,
            "plan_context_source": self.plan_context_source,
            "selected_source_thinker_id": self.selected_source_thinker_id,
            "selected_source_thinker_name": self.selected_source_thinker_name,
            "candidates": [candidate.to_trace_dict() for candidate in self.candidates],
        }
        if self.plan_source_mismatches:
            details["plan_source_mismatches"] = self.plan_source_mismatches
        return details


@dataclass(frozen=True)
class SelectedCompositionSource:
    candidate: CompositionSourceCandidate
    materialization_position: int
    rationale: str

    def to_trace_dict(self) -> dict[str, Any]:
        return {
            "source_family_key": self.candidate.source_family_key,
            "engine_key": self.candidate.engine_key,
            "candidate_state": self.candidate.candidate_state,
            "selection_rank": self.materialization_position,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class RejectedCompositionSource:
    candidate: CompositionSourceCandidate
    rationale: str

    def to_trace_dict(self) -> dict[str, Any]:
        return {
            "source_family_key": self.candidate.source_family_key,
            "engine_key": self.candidate.engine_key,
            "candidate_state": self.candidate.candidate_state,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class CompositionSourceSelection:
    profile: Optional[ComposeFromSourceProfile]
    selected: list[SelectedCompositionSource]
    rejected: list[RejectedCompositionSource]
    selection_kind: Literal["profile", "explicit"] = "profile"
    selection_summary: str = ""
    legacy_profile_equivalent: Optional[ComposeFromSourceProfile] = None

    def to_trace_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "selection_kind": self.selection_kind,
            "selected": [candidate.to_trace_dict() for candidate in self.selected],
            "rejected": [candidate.to_trace_dict() for candidate in self.rejected],
            "selection_summary": self.selection_summary,
        }
        if self.profile is not None:
            payload["profile"] = self.profile
        if self.legacy_profile_equivalent is not None:
            payload["legacy_profile_equivalent"] = self.legacy_profile_equivalent
        return payload


@dataclass(frozen=True)
class CompositionMaterializedSection:
    source_family_key: str
    engine_key: str
    title: str
    materialization_position: int
    profile: Optional[ComposeFromSourceProfile]
    composition_role_hint: str
    section: ComposeFromIntentSectionInput

    def to_trace_dict(self) -> dict[str, Any]:
        payload = {
            "source_family_key": self.source_family_key,
            "engine_key": self.engine_key,
            "title": self.title,
            "selection_rank": self.materialization_position,
        }
        if self.profile is not None:
            payload["profile"] = self.profile
        return payload


@dataclass(frozen=True)
class CompositionSourceBridgeResult:
    catalog: CompositionSourceCatalog
    selection: CompositionSourceSelection
    materialized_sections: list[CompositionMaterializedSection]


def evaluate_compose_profile_feasibility(
    catalog: CompositionSourceCatalog,
) -> tuple[list[ComposeFromSourceProfile], dict[ComposeFromSourceProfile, list[str]]]:
    """Return feasible profiles and per-profile blockers for the resolved catalog."""

    by_family = {candidate.source_family_key: candidate for candidate in catalog.candidates}
    feasible: list[ComposeFromSourceProfile] = []
    blocked: dict[ComposeFromSourceProfile, list[str]] = {}

    for profile, preset in _PROFILE_SELECTION_PRESETS.items():
        blockers: list[str] = []
        for source_family_key, _position, _rationale in preset:
            candidate = by_family.get(source_family_key)
            if candidate is None:
                blockers.append(f"{source_family_key} (missing_from_catalog)")
                continue
            if candidate.candidate_state != "available":
                blockers.append(f"{source_family_key} ({candidate.candidate_state})")
        if blockers:
            blocked[profile] = blockers
            continue
        feasible.append(profile)

    return feasible, blocked


def build_source_composition_bridge(
    *,
    source_v2_job_id: str,
    profile: ComposeFromSourceProfile,
) -> CompositionSourceBridgeResult:
    """Resolve AOI source material into deterministic compose sections."""

    catalog = resolve_source_catalog(source_v2_job_id=source_v2_job_id)
    selection = select_source_catalog(catalog, profile=profile)
    materialized_sections = materialize_selected_sources(selection)
    return CompositionSourceBridgeResult(
        catalog=catalog,
        selection=selection,
        materialized_sections=materialized_sections,
    )


def build_selection_composition_bridge(
    *,
    source_v2_job_id: str,
    selection: list[AoiSelectedSourceInput],
    selection_summary: str = "",
    legacy_profile_equivalent: Optional[ComposeFromSourceProfile] = None,
) -> CompositionSourceBridgeResult:
    """Resolve AOI source material from an explicit planner-provided selection."""

    catalog = resolve_source_catalog(source_v2_job_id=source_v2_job_id)
    resolved_selection = select_source_catalog_by_selection(
        catalog,
        selection=selection,
        selection_summary=selection_summary,
        legacy_profile_equivalent=legacy_profile_equivalent,
    )
    materialized_sections = materialize_selected_sources(resolved_selection)
    return CompositionSourceBridgeResult(
        catalog=catalog,
        selection=resolved_selection,
        materialized_sections=materialized_sections,
    )


def resolve_source_catalog(*, source_v2_job_id: str) -> CompositionSourceCatalog:
    """Build the full AOI source catalog without throwing per-candidate failures."""

    job = get_job(source_v2_job_id) or {}
    engine_registry = get_engine_registry()
    effective_plan_context = load_effective_plan_context(
        source_v2_job_id,
        job.get("plan_id", ""),
    )
    merged_plan_data = _merged_plan_data(job)
    plan = effective_plan_context.plan

    workflow_key = (
        getattr(plan, "workflow_key", None)
        or merged_plan_data.get("workflow_key")
        or job.get("workflow_key")
        or AOI_WORKFLOW_KEY
    )
    objective_key = (
        getattr(plan, "objective_key", None)
        or merged_plan_data.get("objective_key")
        or AOI_DEFAULT_OBJECTIVE_KEY
    )
    if getattr(plan, "objective_key", None):
        objective_source = effective_plan_context.source
    elif merged_plan_data.get("objective_key"):
        objective_source = "merged_plan_data"
    else:
        objective_source = "workflow_default"
    if get_objective(objective_key) is None:
        objective_key = AOI_DEFAULT_OBJECTIVE_KEY
        objective_source = "workflow_default"

    thinker_id = (
        getattr(plan, "selected_source_thinker_id", None)
        or merged_plan_data.get("selected_source_thinker_id")
    )
    thinker_name = (
        getattr(plan, "selected_source_thinker_name", None)
        or merged_plan_data.get("selected_source_thinker_name")
    )

    candidates = [
        _resolve_artifact_candidate(
            source_v2_job_id=source_v2_job_id,
            source_family_key=SOURCE_FAMILY_THEMATIC_SYNTHESIS,
            plan=plan,
            engine_registry=engine_registry,
        ),
        _resolve_artifact_candidate(
            source_v2_job_id=source_v2_job_id,
            source_family_key=SOURCE_FAMILY_ENGAGEMENT_MAPPING,
            plan=plan,
            engine_registry=engine_registry,
        ),
        _resolve_artifact_candidate(
            source_v2_job_id=source_v2_job_id,
            source_family_key=SOURCE_FAMILY_SIN_FINDINGS,
            plan=plan,
            engine_registry=engine_registry,
        ),
        _resolve_report_candidate(
            source_v2_job_id=source_v2_job_id,
            plan=plan,
            engine_registry=engine_registry,
        ),
    ]

    mismatches = [
        {
            "source_family_key": candidate.source_family_key,
            "plan_mismatch": candidate.plan_context_enrichment.get("plan_mismatch"),
        }
        for candidate in candidates
        if candidate.plan_context_enrichment.get("plan_mismatch")
    ]

    return CompositionSourceCatalog(
        source_v2_job_id=source_v2_job_id,
        workflow_key=workflow_key,
        objective_key=objective_key,
        objective_source=objective_source,
        plan_context_found=plan is not None,
        plan_context_source=effective_plan_context.source,
        selected_source_thinker_id=thinker_id,
        selected_source_thinker_name=thinker_name,
        candidates=sorted(candidates, key=lambda item: _SOURCE_FAMILY_ORDER[item.source_family_key]),
        plan_source_mismatches=mismatches,
    )


def select_source_catalog(
    catalog: CompositionSourceCatalog,
    *,
    profile: ComposeFromSourceProfile,
) -> CompositionSourceSelection:
    """Apply the bounded AOI preset selector over the resolved source catalog."""

    preset = _PROFILE_SELECTION_PRESETS[profile]
    selected_by_family = {family: (position, rationale) for family, position, rationale in preset}

    selected: list[SelectedCompositionSource] = []
    rejected: list[RejectedCompositionSource] = []

    for candidate in catalog.candidates:
        selected_entry = selected_by_family.get(candidate.source_family_key)
        if selected_entry is not None:
            position, rationale = selected_entry
            selected.append(
                SelectedCompositionSource(
                    candidate=candidate,
                    materialization_position=position,
                    rationale=rationale,
                )
            )
            continue
        rejected.append(
            RejectedCompositionSource(
                candidate=candidate,
                rationale=(
                    f"Rejected because the '{profile}' preset does not materialize "
                    f"the '{candidate.source_family_key}' source family."
                ),
            )
        )

    selected.sort(key=lambda item: item.materialization_position)
    _raise_for_unresolvable_required_candidates(
        source_v2_job_id=catalog.source_v2_job_id,
        selection_label=profile,
        selected=selected,
    )
    return CompositionSourceSelection(
        selection_kind="profile",
        profile=profile,
        selected=selected,
        rejected=rejected,
        selection_summary=f"Selected the bounded '{profile}' AOI preset.",
        legacy_profile_equivalent=profile,
    )


def select_source_catalog_by_selection(
    catalog: CompositionSourceCatalog,
    *,
    selection: list[AoiSelectedSourceInput],
    selection_summary: str = "",
    legacy_profile_equivalent: Optional[ComposeFromSourceProfile] = None,
) -> CompositionSourceSelection:
    """Apply an explicit planner-provided AOI source-family selection."""

    _validate_requested_selection(selection)
    selected_by_family = {
        item.source_family_key: (item.selection_rank, item.rationale)
        for item in selection
    }
    seen_requested_families: set[str] = set()
    selected: list[SelectedCompositionSource] = []
    rejected: list[RejectedCompositionSource] = []

    for candidate in catalog.candidates:
        selected_entry = selected_by_family.get(candidate.source_family_key)
        if selected_entry is not None:
            selection_rank, rationale = selected_entry
            seen_requested_families.add(candidate.source_family_key)
            selected.append(
                SelectedCompositionSource(
                    candidate=candidate,
                    materialization_position=selection_rank,
                    rationale=rationale,
                )
            )
            continue
        rejected.append(
            RejectedCompositionSource(
                candidate=candidate,
                rationale=(
                    "Rejected by the planner-backed AOI selection for this task."
                ),
            )
        )

    missing = sorted(set(selected_by_family.keys()) - seen_requested_families)
    if missing:
        raise ComposeFromSourceResolutionError(
            "compose-from-selection referenced source families missing from the AOI catalog: "
            + ", ".join(missing)
        )

    selected.sort(key=lambda item: item.materialization_position)
    inferred_legacy_equivalent = legacy_profile_equivalent or _infer_legacy_profile_equivalent(selected)
    _raise_for_unresolvable_required_candidates(
        source_v2_job_id=catalog.source_v2_job_id,
        selection_label="explicit_selection",
        selected=selected,
    )
    return CompositionSourceSelection(
        selection_kind="explicit",
        profile=None,
        selected=selected,
        rejected=rejected,
        selection_summary=selection_summary,
        legacy_profile_equivalent=inferred_legacy_equivalent,
    )


def materialize_selected_sources(
    selection: CompositionSourceSelection,
) -> list[CompositionMaterializedSection]:
    """Materialize selected source candidates into compose-from-intent sections."""

    sections: list[CompositionMaterializedSection] = []
    for selected in selection.selected:
        candidate = selected.candidate
        if candidate.candidate_state != "available" or candidate.materialization_payload is None:
            selection_label = selection.profile or selection.selection_kind
            raise ComposeFromSourceResolutionError(
                f"compose-from-source selection '{selection_label}' could not materialize "
                f"source family '{candidate.source_family_key}' because it is {candidate.candidate_state}"
            )
        section = ComposeFromIntentSectionInput(
            engine_key=candidate.engine_key,
            title=candidate.title,
            prose=_stable_json_text(candidate.materialization_payload),
        )
        sections.append(
            CompositionMaterializedSection(
                source_family_key=candidate.source_family_key,
                engine_key=candidate.engine_key,
                title=candidate.title,
                materialization_position=selected.materialization_position,
                profile=selection.profile,
                composition_role_hint=candidate.composition_role_hint,
                section=section,
            )
        )
    return sections


def _resolve_artifact_candidate(
    *,
    source_v2_job_id: str,
    source_family_key: str,
    plan: Any,
    engine_registry: Any,
) -> CompositionSourceCandidate:
    definition = _SOURCE_FAMILY_DEFINITIONS[source_family_key]
    engine_key = definition["engine_key"]
    plan_context_enrichment = _build_plan_context_enrichment(plan, engine_key)
    provenance_pointer = {"job_id": source_v2_job_id, "engine_key": engine_key}
    role_hint_or_invalid = _resolve_candidate_role_hint(
        engine_registry=engine_registry,
        source_v2_job_id=source_v2_job_id,
        source_family_key=source_family_key,
        engine_key=engine_key,
        title=definition["title"],
        source_backend_kind="artifact",
        provenance_pointer=provenance_pointer,
        summary_metadata={"payload_kind": "normalized_artifact"},
        plan_context_enrichment=plan_context_enrichment,
    )
    if isinstance(role_hint_or_invalid, CompositionSourceCandidate):
        return role_hint_or_invalid
    role_hint = role_hint_or_invalid
    try:
        artifact_payload = load_aoi_normalized_artifact(source_v2_job_id, engine_key)
    except Exception as exc:
        return CompositionSourceCandidate(
            source_family_key=source_family_key,
            engine_key=engine_key,
            title=definition["title"],
            source_backend_kind="artifact",
            candidate_state="invalid",
            provenance_pointer=provenance_pointer,
            composition_role_hint=role_hint,
            summary_metadata={"payload_kind": "normalized_artifact"},
            plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="invalid"),
            resolution_note=f"Artifact load failed: {exc}",
        )

    if artifact_payload is None:
        return CompositionSourceCandidate(
            source_family_key=source_family_key,
            engine_key=engine_key,
            title=definition["title"],
            source_backend_kind="artifact",
            candidate_state="unavailable",
            provenance_pointer=provenance_pointer,
            composition_role_hint=role_hint,
            summary_metadata={"payload_kind": "normalized_artifact"},
            plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="unavailable"),
            resolution_note="No normalized AOI artifact was found for this engine.",
        )
    if not isinstance(artifact_payload, dict):
        return CompositionSourceCandidate(
            source_family_key=source_family_key,
            engine_key=engine_key,
            title=definition["title"],
            source_backend_kind="artifact",
            candidate_state="invalid",
            provenance_pointer=provenance_pointer,
            composition_role_hint=role_hint,
            summary_metadata={"payload_kind": "normalized_artifact"},
            plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="invalid"),
            resolution_note="Normalized AOI artifact payload is not an object.",
        )
    return CompositionSourceCandidate(
        source_family_key=source_family_key,
        engine_key=engine_key,
        title=definition["title"],
        source_backend_kind="artifact",
        candidate_state="available",
        provenance_pointer=provenance_pointer,
        composition_role_hint=role_hint,
        summary_metadata=_summarize_payload(artifact_payload, payload_kind="normalized_artifact"),
        plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="available"),
        resolution_note="Loaded from normalized AOI artifact store.",
        materialization_payload=artifact_payload,
    )


def _resolve_report_candidate(
    *,
    source_v2_job_id: str,
    plan: Any,
    engine_registry: Any,
) -> CompositionSourceCandidate:
    definition = _SOURCE_FAMILY_DEFINITIONS[SOURCE_FAMILY_THEMATIC_REPORT]
    engine_key = AOI_THEMATIC_REPORT_ENGINE
    plan_context_enrichment = _build_plan_context_enrichment(plan, engine_key)
    provenance_pointer = {"job_id": source_v2_job_id, "engine_key": engine_key}
    role_hint_or_invalid = _resolve_candidate_role_hint(
        engine_registry=engine_registry,
        source_v2_job_id=source_v2_job_id,
        source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
        engine_key=engine_key,
        title=definition["title"],
        source_backend_kind="phase_output_metadata",
        provenance_pointer=provenance_pointer,
        summary_metadata={"payload_kind": "report_sections"},
        plan_context_enrichment=plan_context_enrichment,
    )
    if isinstance(role_hint_or_invalid, CompositionSourceCandidate):
        return role_hint_or_invalid
    role_hint = role_hint_or_invalid
    try:
        outputs = load_phase_outputs(job_id=source_v2_job_id, engine_key=engine_key)
    except Exception as exc:
        return CompositionSourceCandidate(
            source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
            engine_key=engine_key,
            title=definition["title"],
            source_backend_kind="phase_output_metadata",
            candidate_state="invalid",
            provenance_pointer=provenance_pointer,
            composition_role_hint=role_hint,
            summary_metadata={"payload_kind": "report_sections"},
            plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="invalid"),
            resolution_note=f"Report output lookup failed: {exc}",
        )

    if not outputs:
        return CompositionSourceCandidate(
            source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
            engine_key=engine_key,
            title=definition["title"],
            source_backend_kind="phase_output_metadata",
            candidate_state="unavailable",
            provenance_pointer=provenance_pointer,
            composition_role_hint=role_hint,
            summary_metadata={"payload_kind": "report_sections"},
            plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="unavailable"),
            resolution_note="No thematic report phase outputs were found.",
        )

    latest = max(
        outputs,
        key=lambda row: (
            row.get("phase_number", 0),
            row.get("pass_number", 0),
            row.get("created_at") or "",
            row.get("id") or "",
        ),
    )
    metadata = latest.get("metadata") or {}
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except Exception as exc:
            return CompositionSourceCandidate(
                source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
                engine_key=engine_key,
                title=definition["title"],
                source_backend_kind="phase_output_metadata",
                candidate_state="invalid",
                provenance_pointer=_report_provenance(source_v2_job_id, latest),
                composition_role_hint=role_hint,
                summary_metadata={"payload_kind": "report_sections"},
                plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="invalid"),
                resolution_note=f"Could not parse report metadata JSON: {exc}",
            )
    if not isinstance(metadata, dict):
        return CompositionSourceCandidate(
            source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
            engine_key=engine_key,
            title=definition["title"],
            source_backend_kind="phase_output_metadata",
            candidate_state="invalid",
            provenance_pointer=_report_provenance(source_v2_job_id, latest),
            composition_role_hint=role_hint,
            summary_metadata={"payload_kind": "report_sections"},
            plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="invalid"),
            resolution_note="Report metadata is not an object.",
        )

    normalized = metadata.get("normalized")
    if not isinstance(normalized, dict):
        return CompositionSourceCandidate(
            source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
            engine_key=engine_key,
            title=definition["title"],
            source_backend_kind="normalized_report_payload",
            candidate_state="invalid",
            provenance_pointer=_report_provenance(source_v2_job_id, latest),
            composition_role_hint=role_hint,
            summary_metadata={"payload_kind": "report_sections"},
            plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="invalid"),
            resolution_note="Report metadata does not contain a normalized payload object.",
        )

    report_sections = normalized.get("report_sections")
    if not isinstance(report_sections, dict):
        return CompositionSourceCandidate(
            source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
            engine_key=engine_key,
            title=definition["title"],
            source_backend_kind="normalized_report_payload",
            candidate_state="invalid",
            provenance_pointer=_report_provenance(source_v2_job_id, latest),
            composition_role_hint=role_hint,
            summary_metadata={"payload_kind": "report_sections"},
            plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="invalid"),
            resolution_note="Normalized report payload does not contain a report_sections object.",
        )

    return CompositionSourceCandidate(
        source_family_key=SOURCE_FAMILY_THEMATIC_REPORT,
        engine_key=engine_key,
        title=definition["title"],
        source_backend_kind="normalized_report_payload",
        candidate_state="available",
        provenance_pointer=_report_provenance(source_v2_job_id, latest),
        composition_role_hint=role_hint,
        summary_metadata=_summarize_payload(
            report_sections,
            payload_kind="report_sections",
            extra={"derived_payload_kind": "normalized_report_payload"},
        ),
        plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="available"),
        resolution_note="Loaded from the latest thematic report phase output metadata.",
        materialization_payload={"report_sections": report_sections},
    )


def _resolve_candidate_role_hint(
    *,
    engine_registry: Any,
    source_v2_job_id: str,
    source_family_key: str,
    engine_key: str,
    title: str,
    source_backend_kind: SourceBackendKind,
    provenance_pointer: dict[str, Any],
    summary_metadata: dict[str, Any],
    plan_context_enrichment: dict[str, Any],
) -> str | CompositionSourceCandidate:
    try:
        return resolve_composition_role(engine_registry, engine_key)
    except CapabilityMetadataResolutionError as exc:
        return CompositionSourceCandidate(
            source_family_key=source_family_key,
            engine_key=engine_key,
            title=title,
            source_backend_kind=source_backend_kind,
            candidate_state="invalid",
            provenance_pointer=provenance_pointer,
            composition_role_hint="",
            summary_metadata=summary_metadata,
            plan_context_enrichment=_with_plan_mismatch(plan_context_enrichment, live_state="invalid"),
            resolution_note=f"Composition role metadata resolution failed: {exc}",
        )


def _raise_for_unresolvable_required_candidates(
    *,
    source_v2_job_id: str,
    selection_label: str,
    selected: list[SelectedCompositionSource],
) -> None:
    missing = [item for item in selected if item.candidate.candidate_state != "available"]
    if not missing:
        return
    details = ", ".join(
        f"{item.candidate.source_family_key} ({item.candidate.candidate_state}: {item.candidate.resolution_note})"
        for item in missing
    )
    raise ComposeFromSourceResolutionError(
        f"compose-from-source selection '{selection_label}' could not resolve required AOI source material "
        f"for source_v2_job_id '{source_v2_job_id}': {details}"
    )


def _validate_requested_selection(selection: list[AoiSelectedSourceInput]) -> None:
    if not selection:
        raise ComposeFromSourceResolutionError("compose-from-selection requires at least one selected source family")

    seen_families: set[str] = set()
    seen_ranks: set[int] = set()
    for item in selection:
        if item.source_family_key in seen_families:
            raise ComposeFromSourceResolutionError(
                f"compose-from-selection duplicated source family '{item.source_family_key}'"
            )
        if item.selection_rank in seen_ranks:
            raise ComposeFromSourceResolutionError(
                f"compose-from-selection duplicated selection_rank '{item.selection_rank}'"
            )
        seen_families.add(item.source_family_key)
        seen_ranks.add(item.selection_rank)

    expected_ranks = list(range(1, len(selection) + 1))
    if sorted(seen_ranks) != expected_ranks:
        raise ComposeFromSourceResolutionError(
            "compose-from-selection requires contiguous selection_rank values starting at 1"
        )


def _infer_legacy_profile_equivalent(
    selected: list[SelectedCompositionSource],
) -> Optional[ComposeFromSourceProfile]:
    family_order = tuple(item.candidate.source_family_key for item in sorted(
        selected,
        key=lambda item: item.materialization_position,
    ))
    for profile, preset in _PROFILE_SELECTION_PRESETS.items():
        preset_families = tuple(source_family_key for source_family_key, _rank, _rationale in preset)
        if family_order == preset_families:
            return profile
    return None


def _merged_plan_data(job: dict[str, Any]) -> dict[str, Any]:
    plan_data = job.get("plan_data")
    if not isinstance(plan_data, dict):
        return {}
    if plan_data.get("_type") == "request_snapshot":
        merged = dict(plan_data.get("plan_request") or {})
        for key, value in (plan_data.get("request_options") or {}).items():
            if key not in merged and value is not None:
                merged[key] = value
        return merged
    return dict(plan_data)


def _build_plan_context_enrichment(plan: Any, engine_key: str) -> dict[str, Any]:
    if plan is None:
        return {"plan_context_found": False}

    phase_matches: list[dict[str, Any]] = []
    for phase in getattr(plan, "phases", []) or []:
        declared = False
        if getattr(phase, "engine_key", None) == engine_key:
            declared = True
        overrides = getattr(phase, "engine_overrides", None) or {}
        if engine_key in overrides:
            declared = True
        if not declared:
            continue
        phase_matches.append(
            {
                "phase_number": getattr(phase, "phase_number", None),
                "phase_name": getattr(phase, "phase_name", ""),
                "skip": bool(getattr(phase, "skip", False)),
                "skip_reason": getattr(phase, "skip_reason", None),
            }
        )

    if not phase_matches:
        plan_state = "not_declared"
    elif all(match["skip"] for match in phase_matches):
        plan_state = "declared_skipped"
    else:
        plan_state = "declared_active"

    return {
        "plan_context_found": True,
        "plan_state": plan_state,
        "objective_key": getattr(plan, "objective_key", None),
        "workflow_key": getattr(plan, "workflow_key", None),
        "selected_source_thinker_id": getattr(plan, "selected_source_thinker_id", None),
        "selected_source_thinker_name": getattr(plan, "selected_source_thinker_name", None),
        "phase_matches": phase_matches,
    }


def _with_plan_mismatch(plan_context_enrichment: dict[str, Any], *, live_state: CandidateState) -> dict[str, Any]:
    enrichment = dict(plan_context_enrichment)
    plan_state = enrichment.get("plan_state")
    mismatch: Optional[str] = None
    if live_state == "available" and plan_state == "declared_skipped":
        mismatch = "plan_declared_skipped_but_live_source_available"
    elif live_state in {"unavailable", "invalid"} and plan_state == "declared_active":
        mismatch = f"plan_declared_active_but_live_source_{live_state}"
    if mismatch:
        enrichment["plan_mismatch"] = mismatch
    return enrichment


def _report_provenance(source_v2_job_id: str, latest: dict[str, Any]) -> dict[str, Any]:
    return {
        "job_id": source_v2_job_id,
        "engine_key": AOI_THEMATIC_REPORT_ENGINE,
        "output_id": latest.get("id"),
        "phase_number": latest.get("phase_number"),
        "pass_number": latest.get("pass_number"),
        "created_at": latest.get("created_at"),
    }


def _summarize_payload(
    payload: Any,
    *,
    payload_kind: str,
    extra: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    summary: dict[str, Any] = {"payload_kind": payload_kind}
    if isinstance(payload, dict):
        summary["top_level_keys"] = sorted(payload.keys())
    elif isinstance(payload, list):
        summary["item_count"] = len(payload)
    if extra:
        summary.update(extra)
    return summary


def _stable_json_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)
