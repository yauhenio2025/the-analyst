# Prompt: Claude Review Of Phase E Transient Second-Consumer Scope

Read and critique:

- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`

Ground the review in both the bigger program objective and the live code reality.

At minimum, inspect:

- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- any recent completion or review memos in `communications/` that materially bear on the Phase E matrix closeout and the second-consumer question

Inspect analyzer-v2 directly, especially:

- `src/presenter/compose_from_intent.py`
- `src/presenter/manifest_builder.py`
- `src/consumers/definitions/aoi-canary.json`
- `src/api/routes/presenter.py`
- `tests/test_compose_from_intent.py`
- `tests/test_representative_composition_matrix.py`

Inspect the current `aoi-canary` repo directly, especially:

- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts`
- `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/resultsClient.test.ts`
- `/home/evgeny/projects/aoi-canary/README.md`

Questions to answer:

1. Is this the right next Phase E slice after the representative composition matrix, or is it reopening an older second-consumer seam in the wrong way?
2. Is the memo honest about what this slice would and would not prove for the analyzer-v2-as-brain objective?
3. Is `aoi-canary` the right bounded target for a transient second-consumer proof?
4. Is AOI `source_selection` the right default proof path, or is the memo undershooting or overshooting there?
5. Is the memo accurate about the current codebase boundary:
   - transient compose still structurally single-consumer
   - `aoi-canary` already result-backed but not transient
   - analyzer-side adaptation may need to carry unsupported renderers via fallback
6. Does the memo stay disciplined against drift into generic consumer architecture, product UX, or full consumer generality claims?

Output requirements:

- Write the output to:
  - `communications/REPORT_Claude_Phase_E_Transient_Second_Consumer_Scope_Critique_2026-03-30.md`
- Start with a clear verdict:
  - `Approve`
  - `Approve with revisions`
  - `Reject`
- Prioritize concrete findings, strategic risks, contradictions, and scope corrections
- Be explicit about what the memo gets right
- Keep the distinction between strategic disagreement and implementation/detail correction clear
