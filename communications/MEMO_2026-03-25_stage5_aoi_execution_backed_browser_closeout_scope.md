# Memo: Stage 5 AOI Execution-Backed Browser Closeout Scope

Date: 2026-03-25
Status: Draft scope memo
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Summary

The Stage 5 AOI seam gate has already passed on fixture-backed evidence.

One fresh live `execution_backed` `evolution_ready` run has also now been launched, completed, recovered to analyzer presentation readiness, and backfilled to a durable Critic local snapshot id:

- fresh job id: `job-6ee8b0621177`
- fresh local analysis id: `gen-v2-18853b558ef1`
- selected source thinker: `otto_neurath`

So the next honest step is no longer another repair tranche and no longer another fresh AOI launch by default.

The remaining gap is narrower:

- use the recovered fresh run as the counted browser source
- capture the planner-primary browser proof bundle on that exact run
- re-grade that recovered case against the frozen rubric
- then write the Stage 2 closure decision honestly

This is a browser closeout slice, not a new architecture slice.

## Why This Is The Next Honest Step

The current program state is now:

- Stage 5 seam behavior already passed on the frozen fixture-backed pack
- a fresh execution-backed AOI run now exists and is durably queryable again
- the missing proof element is the counted planner-backed browser path on that same recovered fresh run
- browser identity proof alone is not enough for Stage 2 closure; the recovered case still has to be re-graded explicitly against the frozen rubric before any closure claim

So the unresolved question is no longer:

- can the backend launch or recover a fresh AOI run at all?

It is now:

- can the real AOI host UI consume that recovered fresh run on the counted planner-backed `compose-from-selection` path while preserving its canonical identity strongly enough to support an honest Stage 2 decision?

That is the right next bounded question for the exemplar.

## Bounded Claim

This slice should do one thing:

- close the missing counted browser evidence on the recovered fresh `execution_backed` AOI run

This slice should not reopen:

- analyzer auto-presentation recovery
- host warm-snapshot durability
- completed-job local snapshot backfill
- AOI selection law
- the frozen four-case Stage 5 pack
- new AOI corpus uploads by default
- Tranche 3 generalization
- lifecycle/governance work

## Scope Decisions

### Decision 1: Treat this as a browser closeout, not a new repair tranche

No product, API, schema, or code changes are authorized up front for this slice.

If the counted browser path on the recovered run exposes a genuinely new seam, stop and write a revision memo.
Do not silently widen this scope into another repair pass.

### Decision 2: Use the recovered fresh run as the fixed counted source

Default counted source for this slice is:

- `source_v2_job_id = job-6ee8b0621177`
- `source_analysis_id = gen-v2-18853b558ef1`
- thinker = `otto_neurath`
- task = `Show how Aaron Benanav's use of Otto Neurath's planning argument evolves across the corpus.`

Reason:

- this run is already fresh
- it is already recovered to `result_state = ready`
- it already resolves through the Critic job-detail and saved-result routes
- spending another long AOI launch before exhausting this recovered fresh proof source would be wasteful and would blur the documentary trail

Do not silently substitute another AOI run unless the closeout memo explicitly explains why the recovered fresh run could not be consumed honestly.
The closeout must name this source exactly as it is: a recovered fresh execution-backed run with later local snapshot backfill, not an untouched fresh launch moment.

### Decision 3: Preserve the counted planner-primary path exactly

The counted path must remain:

- AOI V2 thematic panel
- explicit click-selection of the recovered saved-result row
- planner-backed handoff request
- warm snapshot
- `/compose-from-intent`
- `compose-from-selection`

No profile/autostart branch may count.
No `compose-from-source` branch may count.
No implicit “latest result” assumption may count.

The AOI panel currently auto-loads the latest saved result by default, so relying on whatever row is already selected does not count.

Before continuing into compose, the operator must explicitly click the recovered fresh row and verify that the selected saved-result row is the recovered fresh run and that the compose URL preserves:

- `source_analysis_id = gen-v2-18853b558ef1`
- `source_v2_job_id = job-6ee8b0621177`

If the browser attempt relies only on auto-loaded latest state without a captured deliberate pin to the recovered row, it does not count.

### Decision 4: Keep `execution_backed` documentary, not inferred

This slice should still treat `execution_backed` as an evidence tier that must be proven through cross-linked artifacts rather than assumed from one field.

Required counted browser bundle must cross-link the same recovered fresh run through:

- recovered live summary
- selected saved-result row identity
- `/compose-from-intent` URL/query state
- `compose-from-selection` request payload
- counted HAR / screenshot

If the browser proof drifts onto any other saved result row or loses the canonical `source_v2_job_id`, the attempt does not count as closure-grade execution-backed evidence.

### Decision 5: Freeze the broader pack and roadmap order

Do not rerun the frozen four-case Stage 5 pack in this slice.

That pack already passed and remains the fixture-backed seam baseline.
This slice exists only to add the missing counted browser evidence on top of that baseline.

Roadmap order also stays unchanged:

- Stage 2 remains open until the counted browser closeout is written honestly
- Tranche 3 remains blocked until that Stage 2 decision is explicit

### Decision 6: Make the Stage 2 decision explicit rather than implied

The closeout for this slice must answer separately:

- did the recovered fresh run hold on the counted planner-primary browser path?
- is the resulting evidence honestly `execution_backed` under the frozen rubric?
- is one successful recovered fresh case enough to support Stage 2 closure under the current rubric?
- is the evidence strong enough to support repeated bounded AOI transient use, or only one recovered-case success?

The closeout must also explicitly re-grade the recovered execution-backed case against the relevant frozen-rubric dimensions:

- `selection_fit`
- `rationale_clarity`
- `rendered_usefulness`
- `operational_behavior`

The repeated-use assessment must say whether the recovery repairs now represent durable infrastructure or only recovered-case scaffolding. If they behave like recovered-case-only scaffolding, one successful browser closeout is not enough to claim the stronger repeated-use bar.

Do not collapse “browser proof passed” into “Stage 2 definitely closed” without answering those questions directly.

### Decision 7: Use explicit stop-and-revise rules

Stop and write a revision memo if any of the following occur:

- the recovered saved-result row cannot be surfaced or selected in the AOI panel
- the planner-backed request binds to a different saved result row than the recovered fresh run
- warm snapshot rewrites or drops the canonical `source_v2_job_id`
- `/compose-from-intent` does not preserve the recovered fresh identity in URL/query state
- the product path drifts onto `compose-from-source`, profile autostart, or other non-counted branches
- `compose-from-selection` fails on the recovered fresh run
- the resulting artifact bundle is too weak to prove that the counted path actually used the recovered fresh run

## Proposed Deliverables

### 1. Counted browser proof bundle on the recovered fresh run

At minimum:

- one pre-compose row-identity artifact proving that the explicitly selected AOI saved-result row is `job-6ee8b0621177` / `gen-v2-18853b558ef1`
- one request JSON artifact proving:
  - `fixture_strength = execution_backed`
  - selected row identity = `job-6ee8b0621177`
  - `source_v2_job_id_preserved = true`
  - counted path used `compose-from-selection`
- one browser HAR
- one screenshot showing the real host path

### 2. One closeout memo

Produce one of:

- success: `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_completion.md`
- failure/revision: `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_revision.md`

That memo must state:

- whether the recovered fresh run really counted
- whether Stage 2 now closes or stays open
- whether Tranche 3 remains blocked

### 3. Roadmap update only if the Stage 2 decision changes

If the browser closeout changes the Stage 2 status, update the roadmap docs in the same pass.
If Stage 2 remains open, update them only if the reason changed materially.

## Acceptance Criteria

This scope is successful only if one of these is true:

1. the recovered fresh run is consumed on the counted planner-primary browser path, the artifact bundle proves that identity honestly, the recovered case is re-graded explicitly against the frozen rubric, and the closeout writes the Stage 2 decision explicitly
2. the recovered fresh run fails on a genuinely new browser/product seam and a revision memo documents that seam without widening scope

Anything weaker should be treated as incomplete rather than “basically done.”
