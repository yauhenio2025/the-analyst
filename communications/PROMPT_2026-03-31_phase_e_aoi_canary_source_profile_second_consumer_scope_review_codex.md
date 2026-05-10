Please audit the proposed next scope memo for analyzer-v2:

- `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_second_consumer_scope.md`

Your job is to audit the scope memo against the real repo and the larger program direction, not to implement it.

Please do all of the following:

1. Test the robustness of the memo’s assumptions.
2. Check whether the memo is the right next bounded Phase E step in light of the broader roadmap and overall objectives.
3. Scrutinize the memo’s claims against the actual codebase.
4. Read the most relevant recent memos in `communications/` and `docs/` that materially affect this decision.
5. Call out any strategic drift, hidden coupling, stale assumptions, missing acceptance criteria, or misleading phrasing.
6. State clearly whether the proposed `aoi-canary` / AOI `source_profile` step is the right next move, or whether a different narrower/stronger slice should come first.

Minimum files to inspect:

- `src/presenter/compose_from_intent.py`
- `src/analysis_products/source_backed_readiness.py`
- `src/api/routes/results.py`
- `src/consumers/definitions/aoi-canary.json`
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts`
- `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-selection.json`
- `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md`
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Output requirements:

- Write the audit to:
  - `communications/REPORT_Codex_Phase_E_AOI_Canary_Source_Profile_Second_Consumer_Scope_Audit_2026-03-31.md`
- Start with a clear verdict:
  - `Approve`
  - `Approve with corrections`
  - `Reject`
- Then give the highest-signal findings, with codebase-backed specifics.
- Be explicit about any corrections needed in the memo.
- If you think a different next bounded step is better, say exactly what it is and why.

Do not modify code.
Do not implement the scope.
Do not rewrite the memo directly.
Just produce the audit report in the file above.
