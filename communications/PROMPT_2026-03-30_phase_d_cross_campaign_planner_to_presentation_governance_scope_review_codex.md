# Prompt: Codex Audit Of Phase D Cross-Campaign Planner-To-Presentation Governance Scope

Audit this scope memo against the live repo and the broader program direction:

- `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_scope.md`

Also read enough surrounding material to test whether the memo is strategically honest and codebase-accurate:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-30_phase_d_planner_to_presentation_governance_family_v1_completion.md`
- `communications/MEMO_2026-03-30_phase_d_planner_to_presentation_governance_family_scope.md`
- `communications/MEMO_2026-03-30_phase_d_routing_planning_governance_family_v1_completion.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- relevant recent Phase D / Stage 15 review and completion memos in `communications/`

Inspect the codebase directly, especially:

- `src/evaluations/frozen_pack_harness.py`
- `src/evaluations/frozen_pack_definitions.py`
- `src/evaluations/gate_definitions.py`
- `src/evaluations/review_definitions.py`
- `src/evaluations/resolution_definitions.py`
- `src/evaluations/governance_status.py`
- `src/orchestrator/task_planner.py`
- `src/api/routes/presenter.py`
- `src/presenter/compose_from_intent.py`
- `tests/test_frozen_governance_pack.py`
- `tests/test_bounded_release_gate.py`
- `tests/test_bounded_review_disposition.py`
- `tests/test_bounded_disposition_resolution.py`
- `tests/test_evaluation_governance_status.py`
- `tests/test_evaluation_governance_status_routes.py`

Inspect the relevant proof artifacts directly:

- `communications/PROOF_phase_d_aoi_transient_compose_current_contract_2026-03-30.json`
- `communications/PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`
- `communications/PROOF_phase_d_genealogy_direct_sections_planning_snapshot_2026-03-30.json`

Audit questions:

1. Is a second fresh planner-to-presentation proof campaign the right next bounded Phase D step?
2. Does the memo accurately describe the current substrate and the real remaining gap after planner-to-presentation governance landed?
3. Is reusing `planner_presentation_decision` the right default, or is a fresh genealogy bundle likely to force a bigger evaluator change than the memo admits?
4. Does the memo stay honest about proving anti-coupling rather than generic evaluator extensibility or Phase E generality?
5. Are the proposed pack/family boundaries and regression expectations viable?
6. Is there a smaller cleaner next step that would still materially reduce proving-campaign coupling?

If useful, run non-destructive verification commands or focused tests.

Output requirements:

- Write the audit to:
  - `communications/REPORT_Codex_Phase_D_Cross_Campaign_Planner_To_Presentation_Governance_Scope_Audit_2026-03-30.md`
- Give a bottom-line verdict:
  - `Approve`
  - `Approve with corrections`
  - `Reject`
- Summarize the strongest confirmed claims
- Call out concrete scope corrections or risks with file references where relevant
- Distinguish clearly between:
  - strategic disagreement
  - scope correction
  - implementation caution
