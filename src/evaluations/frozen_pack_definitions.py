"""Code-defined frozen governance packs for deterministic evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


COMMUNICATIONS_DIR = Path(__file__).resolve().parents[2] / "communications"


@dataclass(frozen=True)
class FrozenArtifactDefinition:
    ref_key: str
    relative_path: str
    expected_sha256: str

    @property
    def absolute_path(self) -> Path:
        return COMMUNICATIONS_DIR / self.relative_path


@dataclass(frozen=True)
class FrozenEvaluationCaseDefinition:
    case_key: str
    evaluator_key: str
    subject_kind: str
    subject_identity: str
    workflow_key: str
    consumer_key: str | None = None
    supporting_subjects: dict[str, str] = field(default_factory=dict)
    artifacts: tuple[FrozenArtifactDefinition, ...] = ()


@dataclass(frozen=True)
class FrozenEvaluationPackDefinition:
    evaluation_pack_key: str
    cases: tuple[FrozenEvaluationCaseDefinition, ...]


def _artifact(ref_key: str, relative_path: str, expected_sha256: str) -> FrozenArtifactDefinition:
    return FrozenArtifactDefinition(
        ref_key=ref_key,
        relative_path=relative_path,
        expected_sha256=expected_sha256,
    )


PHASE4_FROZEN_GOVERNANCE_V1 = FrozenEvaluationPackDefinition(
    evaluation_pack_key="phase4_frozen_governance_v1",
    cases=(
        FrozenEvaluationCaseDefinition(
            case_key="aoi_exemplar_march27_execution_backed",
            evaluator_key="aoi_exemplar",
            subject_kind="executor_job",
            subject_identity="job-744edf255ad5",
            workflow_key="anxiety_of_influence_thematic_single_thinker",
            consumer_key="the-critic",
            supporting_subjects={
                "project_id": "round5-proof-dossier-final-1774100000",
                "source_analysis_id": "gen-v2-554e681522b9",
            },
            artifacts=(
                _artifact(
                    "stage5_exemplar_eval_summary",
                    "PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json",
                    "7b6857dc6ef28c4e6efb6905ab095e5368c8d8607ea2383a26f90c7fbd6153d9",
                ),
                _artifact(
                    "stage5_pack_rerun_summary",
                    "PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json",
                    "f0db9d891ffd53aa37b3a94104efc861bf6f83ce710d5bec47904fa93cc1562c",
                ),
                _artifact(
                    "march27_ready_manifest",
                    "PROOF_phase0_aoi_execution_backed_after_guard_recalibration_ready_manifest_2026-03-27.json",
                    "7083f17a6c24e65090b76abd0308d025686b5dffdde1d974ed475df71ce1aa0c",
                ),
                _artifact(
                    "march27_completed_boundary_core",
                    "PROOF_phase0_aoi_execution_backed_after_guard_recalibration_completed_boundary_core_2026-03-27.json",
                    "d9fbe6dfe65c6c02e3edecd39b191c55db8ade6fb7484b3de811a0e79eb6f2ad",
                ),
                _artifact(
                    "march27_requests",
                    "PROOF_phase0_aoi_execution_backed_after_guard_recalibration_requests_2026-03-27.json",
                    "d3b784d1a6865e28eb8914fa30bd002824c249eaf7f660d78d4ad6f8ad056b50",
                ),
            ),
        ),
        FrozenEvaluationCaseDefinition(
            case_key="genealogy_lifecycle_march28_session_reopen",
            evaluator_key="genealogy_lifecycle",
            subject_kind="compose_session",
            subject_identity="compose-session-0877864dcca7",
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            supporting_subjects={
                "project_id": "round4-proof-balance-final-1774012011",
                "source_v2_job_id": "proof-round4-adaptive-balance-final-1774012011",
                "planning_decision_id": "planning-decision-2524994934e0",
            },
            artifacts=(
                _artifact(
                    "phase3_preflight",
                    "PROOF_phase3_bounded_lifecycle_v1_preflight_2026-03-28.json",
                    "6cc3361f1566794cc4c451f881c3671d718d1630798a720aaa3e264897652c67",
                ),
                _artifact(
                    "phase3_saved_session",
                    "PROOF_phase3_bounded_lifecycle_v1_saved_session_2026-03-28.json",
                    "92a3daeb4319cc44aeb3ea81ed51f652e41cd8ae434e567e07a5ef6abc3a97e0",
                ),
                _artifact(
                    "phase3_reopen_segment",
                    "PROOF_phase3_bounded_lifecycle_v1_reopen_segment_2026-03-28.json",
                    "9ca0bef56abbe3b8f1f7a382a5787aa12670115bfe858eeb2fc196102fe074d1",
                ),
                _artifact(
                    "phase3_invalid_session",
                    "PROOF_phase3_bounded_lifecycle_v1_invalid_session_2026-03-28.json",
                    "1be918042e277124bdb2424d224add7791e6f828bd293cdf3093c0235a434dbf",
                ),
            ),
        ),
    ),
)


PHASE4_GENEALOGY_LIFECYCLE_GOVERNANCE_V1 = FrozenEvaluationPackDefinition(
    evaluation_pack_key="phase4_genealogy_lifecycle_governance_v1",
    cases=(
        FrozenEvaluationCaseDefinition(
            case_key="genealogy_lifecycle_march28_session_reopen",
            evaluator_key="genealogy_lifecycle",
            subject_kind="compose_session",
            subject_identity="compose-session-0877864dcca7",
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            supporting_subjects={
                "project_id": "round4-proof-balance-final-1774012011",
                "source_v2_job_id": "proof-round4-adaptive-balance-final-1774012011",
                "planning_decision_id": "planning-decision-2524994934e0",
            },
            artifacts=(
                _artifact(
                    "phase3_preflight",
                    "PROOF_phase3_bounded_lifecycle_v1_preflight_2026-03-28.json",
                    "6cc3361f1566794cc4c451f881c3671d718d1630798a720aaa3e264897652c67",
                ),
                _artifact(
                    "phase3_saved_session",
                    "PROOF_phase3_bounded_lifecycle_v1_saved_session_2026-03-28.json",
                    "92a3daeb4319cc44aeb3ea81ed51f652e41cd8ae434e567e07a5ef6abc3a97e0",
                ),
                _artifact(
                    "phase3_reopen_segment",
                    "PROOF_phase3_bounded_lifecycle_v1_reopen_segment_2026-03-28.json",
                    "9ca0bef56abbe3b8f1f7a382a5787aa12670115bfe858eeb2fc196102fe074d1",
                ),
                _artifact(
                    "phase3_invalid_session",
                    "PROOF_phase3_bounded_lifecycle_v1_invalid_session_2026-03-28.json",
                    "1be918042e277124bdb2424d224add7791e6f828bd293cdf3093c0235a434dbf",
                ),
            ),
        ),
    ),
)


PHASE4_AOI_EXEMPLAR_GOVERNANCE_V1 = FrozenEvaluationPackDefinition(
    evaluation_pack_key="phase4_aoi_exemplar_governance_v1",
    cases=(
        FrozenEvaluationCaseDefinition(
            case_key="aoi_exemplar_march27_execution_backed",
            evaluator_key="aoi_exemplar",
            subject_kind="executor_job",
            subject_identity="job-744edf255ad5",
            workflow_key="anxiety_of_influence_thematic_single_thinker",
            consumer_key="the-critic",
            supporting_subjects={
                "project_id": "round5-proof-dossier-final-1774100000",
                "source_analysis_id": "gen-v2-554e681522b9",
            },
            artifacts=(
                _artifact(
                    "stage5_exemplar_eval_summary",
                    "PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json",
                    "7b6857dc6ef28c4e6efb6905ab095e5368c8d8607ea2383a26f90c7fbd6153d9",
                ),
                _artifact(
                    "stage5_pack_rerun_summary",
                    "PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json",
                    "f0db9d891ffd53aa37b3a94104efc861bf6f83ce710d5bec47904fa93cc1562c",
                ),
                _artifact(
                    "march27_ready_manifest",
                    "PROOF_phase0_aoi_execution_backed_after_guard_recalibration_ready_manifest_2026-03-27.json",
                    "7083f17a6c24e65090b76abd0308d025686b5dffdde1d974ed475df71ce1aa0c",
                ),
                _artifact(
                    "march27_completed_boundary_core",
                    "PROOF_phase0_aoi_execution_backed_after_guard_recalibration_completed_boundary_core_2026-03-27.json",
                    "d9fbe6dfe65c6c02e3edecd39b191c55db8ade6fb7484b3de811a0e79eb6f2ad",
                ),
                _artifact(
                    "march27_requests",
                    "PROOF_phase0_aoi_execution_backed_after_guard_recalibration_requests_2026-03-27.json",
                    "d3b784d1a6865e28eb8914fa30bd002824c249eaf7f660d78d4ad6f8ad056b50",
                ),
            ),
        ),
    ),
)


PHASE4_ROUTING_PLANNING_GOVERNANCE_V1 = FrozenEvaluationPackDefinition(
    evaluation_pack_key="phase4_routing_planning_governance_v1",
    cases=(
        FrozenEvaluationCaseDefinition(
            case_key="aoi_saved_result_handoff_current_contract",
            evaluator_key="routing_planning_decision",
            subject_kind="planning_decision",
            subject_identity="planning-decision-1b0dbef41b28",
            workflow_key="anxiety_of_influence_thematic_single_thinker",
            consumer_key="the-critic",
            supporting_subjects={
                "source_v2_job_id": "job-744edf255ad5",
            },
            artifacts=(
                _artifact(
                    "aoi_route_current_contract",
                    "PROOF_phase_d_aoi_route_decision_current_contract_2026-03-30.json",
                    "548858520b821238a2970774f0e7766f52e41c66bad38805a19d201d419393a2",
                ),
                _artifact(
                    "aoi_planning_current_contract",
                    "PROOF_phase_d_aoi_planning_decision_current_contract_2026-03-30.json",
                    "4606bbb3756d54dd43f84d4541f07536a7c800cb1857f25788c3c1100ed4f6d9",
                ),
                _artifact(
                    "aoi_planning_snapshot_current_contract",
                    "PROOF_phase_d_aoi_planning_snapshot_current_contract_2026-03-30.json",
                    "116e12d743fb3ceba9fac7ff51bb34aab8a34af8757badb5d1107cf94f0bf95e",
                ),
            ),
        ),
        FrozenEvaluationCaseDefinition(
            case_key="genealogy_saved_result_direct_sections_snapshot_march28",
            evaluator_key="routing_planning_decision",
            subject_kind="planning_decision",
            subject_identity="planning-decision-b1600d054991",
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            supporting_subjects={
                "source_v2_job_id": "proof-round4-adaptive-balance-final-1774012011",
            },
            artifacts=(
                _artifact(
                    "phase2_trace_multi_surface",
                    "PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json",
                    "af95f300d6393525e44d830fd24a0a9456cd2cd2b77bbaa36d68f77565eb5275",
                ),
                _artifact(
                    "genealogy_planning_snapshot",
                    "PROOF_phase_d_genealogy_direct_sections_planning_snapshot_2026-03-30.json",
                    "a3829761409372d2e1c0c7adb1dc9e4a3efbc04ee3ddf714da27ff10de4cbb24",
                ),
            ),
        ),
    ),
)


PHASE4_PLANNER_TO_PRESENTATION_GOVERNANCE_V1 = FrozenEvaluationPackDefinition(
    evaluation_pack_key="phase4_planner_to_presentation_governance_v1",
    cases=(
        FrozenEvaluationCaseDefinition(
            case_key="aoi_compose_selection_current_contract",
            evaluator_key="planner_presentation_decision",
            subject_kind="planning_decision",
            subject_identity="planning-decision-1b0dbef41b28",
            workflow_key="anxiety_of_influence_thematic_single_thinker",
            consumer_key="the-critic",
            supporting_subjects={
                "source_v2_job_id": "job-744edf255ad5",
            },
            artifacts=(
                _artifact(
                    "aoi_transient_compose_current_contract",
                    "PROOF_phase_d_aoi_transient_compose_current_contract_2026-03-30.json",
                    "e050301d3d65c974d281103bba14e0791d40896f1708d0217546f0699791ffbf",
                ),
            ),
        ),
        FrozenEvaluationCaseDefinition(
            case_key="genealogy_direct_sections_compose_snapshot_march28",
            evaluator_key="planner_presentation_decision",
            subject_kind="planning_decision",
            subject_identity="planning-decision-b1600d054991",
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            supporting_subjects={
                "source_v2_job_id": "proof-round4-adaptive-balance-final-1774012011",
            },
            artifacts=(
                _artifact(
                    "phase2_trace_multi_surface",
                    "PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json",
                    "af95f300d6393525e44d830fd24a0a9456cd2cd2b77bbaa36d68f77565eb5275",
                ),
                _artifact(
                    "genealogy_planning_snapshot",
                    "PROOF_phase_d_genealogy_direct_sections_planning_snapshot_2026-03-30.json",
                    "a3829761409372d2e1c0c7adb1dc9e4a3efbc04ee3ddf714da27ff10de4cbb24",
                ),
            ),
        ),
    ),
)


PHASE4_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_GOVERNANCE_V1 = FrozenEvaluationPackDefinition(
    evaluation_pack_key="phase4_planner_to_presentation_cross_campaign_governance_v1",
    cases=(
        FrozenEvaluationCaseDefinition(
            case_key="aoi_compose_selection_current_contract_fresh_campaign",
            evaluator_key="planner_presentation_decision",
            subject_kind="planning_decision",
            subject_identity="planning-decision-d6b6bb0cd7ac",
            workflow_key="anxiety_of_influence_thematic_single_thinker",
            consumer_key="the-critic",
            supporting_subjects={
                "source_v2_job_id": "job-744edf255ad5",
            },
            artifacts=(
                _artifact(
                    "aoi_transient_compose_cross_campaign",
                    "PROOF_phase_d_cross_campaign_aoi_transient_compose_2026-03-30.json",
                    "448051ed0976b4db1a2cdea6d5df77c4f47cfa2c476beecd10fef08a36986bb8",
                ),
            ),
        ),
        FrozenEvaluationCaseDefinition(
            case_key="genealogy_direct_sections_compose_current_contract_fresh_campaign",
            evaluator_key="planner_presentation_decision",
            subject_kind="planning_decision",
            subject_identity="planning-decision-5f5b0182f2f9",
            workflow_key="intellectual_genealogy",
            consumer_key="the-critic",
            supporting_subjects={
                "source_v2_job_id": "proof-round4-adaptive-balance-final-1774012011",
            },
            artifacts=(
                _artifact(
                    "genealogy_transient_compose_cross_campaign",
                    "PROOF_phase_d_cross_campaign_genealogy_transient_compose_2026-03-30.json",
                    "36e0096d02de828e37cd53fe1194c093f464b7426c40fcd62f1e9f3dc60c75f9",
                ),
            ),
        ),
    ),
)


_PACKS: dict[str, FrozenEvaluationPackDefinition] = {
    PHASE4_FROZEN_GOVERNANCE_V1.evaluation_pack_key: PHASE4_FROZEN_GOVERNANCE_V1,
    PHASE4_GENEALOGY_LIFECYCLE_GOVERNANCE_V1.evaluation_pack_key: PHASE4_GENEALOGY_LIFECYCLE_GOVERNANCE_V1,
    PHASE4_AOI_EXEMPLAR_GOVERNANCE_V1.evaluation_pack_key: PHASE4_AOI_EXEMPLAR_GOVERNANCE_V1,
    PHASE4_ROUTING_PLANNING_GOVERNANCE_V1.evaluation_pack_key: PHASE4_ROUTING_PLANNING_GOVERNANCE_V1,
    PHASE4_PLANNER_TO_PRESENTATION_GOVERNANCE_V1.evaluation_pack_key: PHASE4_PLANNER_TO_PRESENTATION_GOVERNANCE_V1,
    PHASE4_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_GOVERNANCE_V1.evaluation_pack_key: PHASE4_PLANNER_TO_PRESENTATION_CROSS_CAMPAIGN_GOVERNANCE_V1,
}


def get_frozen_pack_definition(evaluation_pack_key: str) -> FrozenEvaluationPackDefinition:
    """Return one known frozen evaluation pack definition."""

    try:
        return _PACKS[evaluation_pack_key]
    except KeyError as exc:
        raise ValueError(f"Unknown evaluation pack: {evaluation_pack_key}") from exc


def iter_pack_artifacts(
    pack_definition: FrozenEvaluationPackDefinition,
) -> list[FrozenArtifactDefinition]:
    """Return all pinned frozen artifact refs for a pack."""

    artifacts: list[FrozenArtifactDefinition] = []
    for case_definition in pack_definition.cases:
        artifacts.extend(case_definition.artifacts)
    return artifacts
