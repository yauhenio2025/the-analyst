# Memo: Stage 5 AOI Execution-Backed Browser Closeout Rerun Scope

Date: 2026-03-26
Status: Draft scope memo for implementation review
Program: Dynamic Bespoke Apps Platformization
Supersedes:
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md` (pre-idempotence-repair draft)
Depends on:
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_revision.md`
- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_completion.md`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_precompose_pin_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_requests_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_session_2026-03-26.har`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_state_2026-03-26.png`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Summary

The bounded host-side idempotence repair is now landed.

So the next honest step is no longer another local-snapshot repair slice.

The next honest step is the counted planner-primary browser closeout rerun on the repaired host behavior for the same recovered fresh execution-backed AOI source:

- upstream counted source: `job-6ee8b0621177`
- thinker: `otto_neurath`
- fixed task: `Show how Aaron Benanav's use of Otto Neurath's planning argument evolves across the corpus.`

Important identity rule for this rerun:

- anchor counted-source truth on the recovered upstream `source_v2_job_id`
- treat local `source_analysis_id` as a host/browser-boundary identity that must be resolved at preflight from the repaired host
- then prove that the same upstream `source_v2_job_id` survives end to end and that the same preflight-resolved local `source_analysis_id` survives through the host compose boundary

This is a rerun scope, not a new repair tranche.

## Why This Is Now The Next Honest Step

Current program state is:

- the frozen Stage 5 seam gate already passed on fixture-backed evidence
- one fresh execution-backed AOI run exists and remains the right counted upstream source candidate
- the first browser-closeout attempt failed because host-local snapshot identity was unstable
- the bounded host-side idempotence repair for that instability is now implemented and verified

So the unresolved question is no longer:

- can the host reuse one canonical local snapshot id for the recovered upstream run?

It is now:

- can the repaired host consume that recovered source on the counted planner-backed `compose-from-selection` path strongly enough to support an honest Stage 2 decision?

That is the right next bounded question.

## Bounded Claim

This slice should do one thing:

- rerun the counted planner-primary browser closeout on the repaired host behavior and then write the Stage 2 decision explicitly

This slice should not reopen:

- analyzer recovery
- host idempotence repair
- AOI planning law
- compose contract repair
- a new AOI launch by default
- the frozen four-case Stage 5 pack
- roadmap order
- Tranche 3 generalization

## Scope Decisions

### Decision 1: Treat this as a rerun, not another repair pass

No product, API, schema, or code changes are authorized up front for this slice.

If the rerun exposes a genuinely new seam, stop and write a revision memo.
Do not silently turn the rerun into another repair tranche.

### Decision 2: Keep the upstream source fixed, but resolve the local alias at execution time

The fixed counted upstream source remains:

- `source_v2_job_id = job-6ee8b0621177`

Do not silently substitute another AOI run unless the closeout memo explicitly explains why the recovered source could not be consumed honestly.

Do **not** hardcode the historical local alias `gen-v2-18853b558ef1` as the counted local source for the rerun.

Reason:

- earlier failed attempts legitimately churned local aliases for the same upstream run
- the repair goal was to re-establish one current canonical local row, not necessarily to preserve the oldest historical local alias forever

So the rerun must:

1. fetch Critic job detail for `job-6ee8b0621177`
2. record the current returned canonical `analysis_id`
3. verify that the saved-result detail for that `analysis_id` resolves back to the same upstream `v2_job_id`
4. use that preflight-resolved local id as the counted `source_analysis_id`

Identity law for this rerun should be stated explicitly:

- `source_v2_job_id = job-6ee8b0621177` is the real counted source truth end to end
- `source_analysis_id` is enforceable today only at the host/browser boundary
- so the rerun must prove upstream truth through the compose page and the host `compose-from-selection` request body, not only through `/compose-from-intent` URL state

### Decision 3: Preserve the counted planner-primary path exactly

The counted path must remain:

- AOI V2 thematic panel
- if a presentation auto-loads on entry, click `Clear` first
- explicitly click the recovered saved-result row
- planner-backed handoff request
- normal host snapshot step
- `/compose-from-intent`
- `compose-from-selection`

No profile/autostart path may count.
No `compose-from-source` path may count.
No implicit “latest saved result” state may count.

The auto-loaded state does not count as row pinning.

### Decision 4: Accept normal snapshot reuse, but require stable identity

On the repaired host path, the normal snapshot step may behave in either of two valid ways:

- reuse the already-canonical local snapshot id with no new warmup insert
- perform the normal warm/reuse call and still return the same canonical local snapshot id

What matters is not whether a warmup request happens.

What matters is:

- the same preflight-resolved canonical `source_analysis_id` stays in force
- the same recovered upstream `source_v2_job_id = job-6ee8b0621177` stays in force

If the rerun rewrites either identity during the counted path, the attempt does not count.

### Decision 5: Require a pre-compose identity bundle

Before compose continuation, the artifact bundle must prove all of these together:

- job-detail preflight for `job-6ee8b0621177`
- saved-result detail for the preflight-resolved local `analysis_id`
- explicit row click-selection in the AOI panel
- `/compose-from-intent` URL/query preserving:
  - `source_v2_job_id = job-6ee8b0621177`
  - `source_analysis_id = <preflight-resolved-canonical-local-id>`
- compose page state still carrying the same two source identities
- host `compose-from-selection` request body preserving:
  - `source_v2_job_id = job-6ee8b0621177`
  - `source_analysis_id = <preflight-resolved-canonical-local-id>`

If the browser proof loses any one of those links, the rerun is not closure-grade.

### Decision 6: Re-grade the recovered execution-backed case explicitly

The closeout for this rerun must answer separately:

- did the repaired host now support an honest counted planner-primary browser proof?
- is the resulting evidence honestly `execution_backed` under the frozen rubric?
- does the recovered case now pass the relevant rubric dimensions:
  - `selection_fit`
  - `rationale_clarity`
  - `rendered_usefulness`
  - `operational_behavior`
- is the evidence strong enough to support repeated bounded AOI transient use, or only one repaired recovered-case success?

Do not collapse “browser rerun passed” into “Stage 2 definitely closed” without writing those judgments explicitly.

### Decision 7: Keep roadmap order fixed

Do not rerun the frozen four-case Stage 5 pack in this slice.

That pack is already the fixture-backed seam baseline.
This slice exists only to add or deny the missing counted browser evidence on the repaired host.

Roadmap order stays unchanged:

- Stage 2 remains open until this rerun is graded honestly
- Tranche 3 remains blocked until that Stage 2 decision is explicit

### Decision 8: Use explicit stop-and-revise rules

Stop and write a revision memo if any of these happen:

- the recovered row cannot be surfaced after clearing any auto-loaded presentation
- the explicit row click binds to a different source than the preflight-resolved canonical source
- the planner-backed request drifts to a different `source_v2_job_id`
- the normal snapshot step rewrites the canonical local `source_analysis_id`
- `/compose-from-intent` drops or rewrites either counted identity
- the product path drifts onto `compose-from-source`, profile autostart, or another non-counted branch
- `compose-from-selection` fails on the repaired recovered source
- the artifact bundle is too weak to prove the counted path actually consumed the repaired recovered source

## Proposed Deliverables

### 1. Counted browser rerun bundle

At minimum:

- one preflight identity artifact proving:
  - job-detail source = `job-6ee8b0621177`
  - current canonical local `analysis_id`
  - saved-result detail resolves back to the same upstream source
- one pre-compose row-pin artifact proving:
  - auto-loaded presentation was cleared if present
  - the saved-results list was visible
  - the recovered row was explicitly clicked
- one request JSON artifact proving:
  - `fixture_strength = execution_backed`
  - counted path used `compose-from-selection`
  - `source_v2_job_id_preserved = true`
  - `source_analysis_id_preserved = true`
  - proof comes from the host `compose-from-selection` request body, not only the `/compose-from-intent` URL
- one browser HAR
- one screenshot

### 2. One closeout memo

Produce one of:

- success: `communications/MEMO_<actual-date>_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md`
- failure/revision: `communications/MEMO_<actual-date>_stage5_aoi_execution_backed_browser_closeout_rerun_revision.md`

That memo must state:

- whether the repaired recovered source really counted
- whether the evidence is honestly `execution_backed`
- whether Stage 2 now closes or stays open
- whether repeated bounded AOI transient use is now justified
- whether Tranche 3 remains blocked

### 3. Roadmap update only if the Stage 2 status or reason changes

If the rerun changes Stage 2 status, update the roadmap docs in the same pass.
If Stage 2 remains open, update them only if the reason changed materially.

## Acceptance Criteria

This scope is successful only if one of these is true:

1. the repaired host consumes the recovered upstream source on the counted planner-primary browser path, the artifact bundle proves identity continuity honestly, the recovered case is re-graded explicitly against the frozen rubric, and the closeout writes the Stage 2 decision explicitly
2. the rerun fails on a genuinely new browser/product seam and a revision memo documents that seam without widening scope

Anything weaker should be treated as incomplete rather than “close enough.”
