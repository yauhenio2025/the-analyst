Please review the proposed recommended next Phase E scope memo for analyzer-v2:

- `communications/MEMO_2026-03-31_phase_e_non_aoi_direct_sections_second_consumer_scope_recommendation.md`

Important framing:

- this memo is intentionally a recommendation memo, not yet roadmap-ratified text
- your job is to critique whether this is the right recommended next bounded Phase E step after AOI `source_profile:comparison` closeout

Please do all of the following:

1. Test the robustness of the memo’s assumptions.
2. Examine the memo in light of the bigger picture and the overall analyzer-v2-as-brain objectives.
3. Scrutinize the memo’s claims against the actual codebase.
4. Look through any relevant recent memos in `communications/` and `docs/` that materially bear on this next-step recommendation.
5. Identify where the memo is strategically right, where it is overstated, where it is too timid, and where it is missing implementation-critical constraints.
6. Be explicit about whether one bounded non-AOI `direct_sections` second-consumer proof on `aoi-canary` is the right next move, or whether some other narrower/stronger next step is better.

Minimum code/doc surfaces to inspect:

- `src/presenter/compose_from_intent.py`
- `src/presenter/schemas.py`
- `src/api/routes/orchestrator.py`
- `src/orchestrator/direct_sections_compose_harness.py`
- `src/consumers/definitions/aoi-canary.json`
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts`
- `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx`
- `/home/evgeny/projects/aoi-canary/src/components/TabShell.tsx`
- `communications/PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json`
- `communications/PROOF_phase_e_aoi_canary_source_profile_comparison_live_closeout_2026-03-31.json`
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_comparison_second_consumer_scope.md`
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_dossier_second_consumer_v1_completion.md`
- `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Output requirements:

- Write the critique to:
  - `communications/REPORT_Claude_Phase_E_Non_AOI_Direct_Sections_Second_Consumer_Scope_Recommendation_Critique_2026-03-31.md`
- Start with a clear verdict:
  - `Approve`
  - `Approve with revisions`
  - `Reject`
- Then give the highest-signal strategic and implementation findings.
- Be concrete about any corrections needed in the memo.
- If you think a different next bounded step is better, say exactly what it is and why.

Do not modify code.
Do not implement the scope.
Do not rewrite the memo directly.
Just produce the critique report in the file above.
