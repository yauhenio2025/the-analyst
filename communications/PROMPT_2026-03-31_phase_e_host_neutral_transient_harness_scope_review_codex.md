Please audit the proposed next Phase E scope memo for analyzer-v2:

- `communications/MEMO_2026-03-31_phase_e_host_neutral_transient_harness_scope.md`

Important framing:

- this memo is intended as the next bounded Phase E scope after the `aoi-canary` genealogy `direct_sections` second-consumer completion
- your job is to audit whether this is the right next broader variable in light of the roadmap, the current codebase, and the broader analyzer-v2-as-the-brain objective
- the memo now proposes one proof-only transient consumer contract plus one minimal harness over exactly two cases:
  - AOI `source_selection`
  - genealogy `direct_sections`
- the claim must stay narrow:
  - this is about proving consumer-side pattern reuse and bounded host-independence beyond the AOI-branded shell
  - it is not a claim of new analyzer-side generality, because the transient compose routes are already generic at the HTTP boundary

Please do all of the following:

1. Test the robustness of the memo’s assumptions.
2. Check whether the memo names the right next broader Phase E question in light of the broader roadmap and overall objectives.
3. Scrutinize the memo’s claims against the actual codebase.
4. Read the most relevant recent memos in `communications/` and `docs/` that materially affect this choice.
5. Call out any strategic drift, hidden coupling, stale assumptions, missing acceptance criteria, or misleading phrasing.
6. State clearly whether one proof-only transient consumer contract plus one minimal harness over AOI `source_selection` plus genealogy `direct_sections` is the right next move, or whether some other narrower/stronger step should come first.

Minimum files to inspect:

- `src/presenter/compose_from_intent.py`
- `src/presenter/schemas.py`
- `src/consumers/definitions/aoi-canary.json`
- `src/consumers/definitions/`
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts`
- `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx`
- `/home/evgeny/projects/aoi-canary/src/components/TabShell.tsx`
- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json`
- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-31.json`
- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_genealogy_direct_sections_2026-03-31.json`
- `communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.json`
- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Output requirements:

- Write the audit to:
  - `communications/REPORT_Codex_Phase_E_Proof_Only_Transient_Consumer_And_Minimal_Harness_Scope_Audit_2026-03-31.md`
- Start with a clear verdict:
  - `Approve`
  - `Approve with corrections`
  - `Reject`
- Then give the highest-signal findings, with codebase-backed specifics.
- Be explicit about any corrections needed in the memo.
- If you think a different next bounded step is better, say exactly what it is and why.
- Explicitly call out whether the memo keeps a real technology boundary:
  - the new harness must not import from or depend on the `aoi-canary` repo
- If you think the proposed proof-only consumer/harness claim is too strong, restate the narrowest honest claim.

Do not modify code.
Do not implement the scope.
Do not rewrite the memo directly.
Just produce the audit report in the file above.
