# Critique: Stage 5 AOI Execution-Backed Browser Closeout Scope

Date: 2026-03-25
Reviewer: Codex
Memo under review: `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md`

## Verdict

Approve after revision.

## Findings

### 1. High: the memo narrows "closeout" to browser identity proof, but Stage 2 closure still requires re-grading the recovered execution-backed ready case itself

The memo's deliverables and acceptance criteria are now mostly browser-artifact-shaped: request JSON, HAR, screenshot, and an explicit decision (`communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md:168`, `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md:200`). The earlier proof plan was stricter: it explicitly required re-grading the recovered ready case against the relevant rubric dimensions (`communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md:233`, `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md:242`). The frozen rubric is stricter still: Stage 2 closure requires not just one `execution_backed` ready case, but evidence strong enough to support repeated bounded AOI transient use (`communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md:128`).

That gap is not theoretical. Live inspection on 2026-03-25 of `GET http://127.0.0.1:8002/v1/results/by-job/job-6ee8b0621177/presentation?consumer_key=the-critic` shows run-level metadata keyed to `otto_neurath`, but `presentation.execution_summary.phase_results["1.0"].final_output_preview` still names `john_oneill` as the selected source thinker. That is enough to say the recovered case itself still needs explicit grading and explanation before any Stage 2 closure claim. Browser identity proof alone is not enough.

Implication: the memo is over-thin for a Stage 2 closure decision. It is strong enough for a browser closeout pass, but not yet strong enough for a closure bar unless it restores explicit recovered-case grading.

### 2. High: "explicit saved-result row selection" is not enforced by the product path; the UI auto-loads latest and the backend still has a latest-result fallback

The memo correctly says no implicit "latest result" assumption may count (`communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md:110`, `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md:114`). The code does not enforce that discipline.

In `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`, `selectedSource` defaults to `currentSourceResult ?? savedResults[0]` (`:254`), the panel auto-loads `loadSavedResults({ autoLoadLatest: true })` on mount (`:801`, `:823`), and the explicit clickable saved-result list is only shown when no presentation is already loaded (`:1392`). On the backend, `_resolve_source_backed_compose_identity` still falls back to `_resolve_latest_saved_aoi_result(...)` if both ids are absent (`/home/evgeny/projects/the-critic/api/server.py:18961`).

So the counted path supports explicit row selection, but it does not require it. The memo's current artifact list is therefore too weak: one screenshot and one HAR may prove that compose happened, but not that the operator deliberately pinned `gen-v2-18853b558ef1` rather than riding the auto-loaded latest state.

Implication: the memo needs a stronger artifact requirement for pre-compose row pinning, not just post-compose proof.

### 3. Medium: the recovered run is honest as an `execution_backed` counted source only if the documentary trail says "fresh run, later recovered/backfilled", not simply "fresh run"

The actual boundaries are good. Live `GET /api/analysis/anxiety_of_influence_thematic_single_thinker/jobs/job-6ee8b0621177` returns `status=completed`, `v2_job_id=job-6ee8b0621177`, and `analysis_id=gen-v2-18853b558ef1`. Live `GET /v1/results/by-job/job-6ee8b0621177?consumer_key=the-critic` returns `result_state=ready`, `presentation_status=completed`, and `restore_available=true`. That means the counted source is still genuinely tied to a fresh analyzer execution, not to fixture-only reuse.

But the browser-visible source is not the untouched original launch moment. It is a recovered and backfilled local consume point. The local `v2_run_references` row for `job-6ee8b0621177` now has the right `local_snapshot_analysis_id`, but as of 2026-03-25 it still shows `advisory_status = pending` in the local DB while the live job-detail API reports `completed`. That mismatch is not currently load-bearing for compose, but it makes the proof easy to mis-document if the closeout talks as though nothing recovery-shaped happened.

Implication: the memo should require the closeout to call the source exactly what it is: a recovered fresh execution-backed run.

### 4. Medium: local DB drift is real enough that the memo needs a stricter preflight pin, even though the recovered run itself is currently clean

Live DB inspection on 2026-03-25 shows 783 AOI local snapshot rows for `round5-proof-dossier-final-1774100000`. Of those, 782 belong to the older proof job `proof-round5-adaptive-aoi-dossier-final-1774100000`, and 275 of those rows still have null thinker identity. The recovered run `job-6ee8b0621177` is currently much cleaner: one local row, correct thinker identity, and the expected `gen-v2-18853b558ef1`.

This does not mean a new AOI launch should be authorized by default. It means the opposite: the recovered run is currently the least ambiguous counted source, and another launch would only add more naming and ordering churn. But it also means the memo should not rely on "the recovered run is obvious" without a preflight pin. On March 25, 2026, it is obvious; after any new AOI activity, it may not be.

Implication: the memo should require a preflight capture of live job detail, live saved-result detail, and visible saved-result ordering before browser work starts.

### 5. Low: the planner-primary identity chain is actually backed by code, so not authorizing a new AOI launch by default is reasonable

This is the confirming part of the review.

The planner branch includes `source_v2_job_id` in saved-result planning context and handoff (`src/orchestrator/task_planner.py:220`, `src/orchestrator/task_planner.py:435`, `src/orchestrator/task_planner.py:533`). The AOI panel carries it into `/compose-from-intent` on the planner-backed path (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:564`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:595`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:656`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:663`). The compose page preserves and forwards it into `composeFromSelection` (`/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:232`, `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:429`). The host compose proxy resolves and forwards the exact canonical id (`/home/evgeny/projects/the-critic/api/server.py:20911`, `/home/evgeny/projects/the-critic/api/server.py:20925`). Analyzer-v2 rejects selection compose without `source_v2_job_id` (`src/presenter/compose_from_intent.py:547`, `src/presenter/compose_from_intent.py:556`).

Warm snapshot is also fail-closed now. `_best_effort_ensure_local_snapshot_analysis_id(...)` and `_save_v2_presentation_to_db(...)` return `None` rather than inventing ids on non-durable save (`/home/evgeny/projects/the-critic/api/server.py:19029`, `/home/evgeny/projects/the-critic/api/server.py:19142`, `/home/evgeny/projects/the-critic/api/server.py:20313`).

Implication: the memo is right to treat this as a browser closeout slice rather than another repair tranche, but only after the revisions above.

## Direct answers

1. Is using the recovered fresh run `job-6ee8b0621177` / `gen-v2-18853b558ef1` as the counted source still honest for `execution_backed`?

Yes, with one condition: the closeout must name it as a fresh execution-backed run that was later recovered/backfilled for local consumption. Recovery does not erase freshness, but hiding the recovery step would weaken the claim materially.

2. Does the codebase actually support the memo's required identity discipline?

Mostly yes. The planner-primary branch preserves `source_v2_job_id`, warm snapshot now fail-closes on non-durable save, `/compose-from-intent` preserves the id when the planner path is used, and `compose-from-selection` proxies the exact resolved `source_v2_job_id`. The weak spot is operational rather than architectural: explicit row selection is supported but not enforced, and latest-result fallback still exists if both ids disappear.

3. Is the memo right not to authorize a new AOI launch by default?

Yes. The recovered run is live, queryable, and currently cleaner than the surrounding local AOI snapshot state. Launching another run by default would add documentary ambiguity faster than it would add useful proof.

4. Does the memo under-specify operational hazards?

Yes.

- Row ordering/latest-result ambiguity is real because the panel auto-loads latest and the backend still has a latest fallback.
- Local DB drift is real because this project currently carries hundreds of older AOI local snapshot rows.
- Recovery vs fresh-launch ambiguity is real unless launch time and recovery/backfill time are explicitly labeled.
- Browser artifact capture is too weak if it does not prove deliberate row pinning before compose.

5. Is one successful browser closeout on that recovered run enough for Stage 2 closure under the current rubric?

No, not by browser closeout alone. It can be the necessary final execution-backed browser proof, but the closeout still has to re-grade the recovered ready case against the rubric and defend the stronger "repeated bounded AOI transient use" claim. The memo currently does not require enough of that.

6. Does the memo keep the bigger picture honest?

Mostly yes. It keeps the Stage 5 seam gate already passed, Stage 2 still open, and Tranche 3 still blocked, which matches the roadmap trail (`communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:193`, `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:195`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1177`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1300`).

7. Is the step appropriately narrow, or is it still smuggling in broader closure by implication?

It is mostly narrow, but the current acceptance section smuggles in broader closure by implication. It treats browser identity proof plus an explicit decision as enough, without requiring the recovered case itself to clear the full Stage 2 bar.

## Recommended revisions before execution

1. Put explicit recovered-case rubric grading back into scope. Reuse the earlier proof-plan requirement to re-check `selection_fit`, `rationale_clarity`, `rendered_usefulness`, and `operational_behavior` on the recovered execution-backed case before any Stage 2 closure claim.
2. Strengthen the artifact bundle so it proves deliberate row pinning. Require a pre-compose capture showing the AOI saved-result list with `job-6ee8b0621177` / `gen-v2-18853b558ef1` visibly selected or otherwise pinned before planner handoff.
3. Add a preflight pin note: record the live job-detail response, live saved-result detail response, and visible saved-result ordering before browser work. If any new AOI run exists after 2026-03-25, revise the counted-source assumption first.
4. Require the closeout memo to call the source exactly what it is: "recovered fresh execution-backed run", not simply "fresh run".
5. Add one explicit non-count rule: if the browser attempt relies on auto-loaded latest state without a captured deliberate pin to the recovered row, it does not count.
6. Add one explicit decision rule: even if browser closeout succeeds, Stage 2 remains open unless the closeout separately argues why this recovered case is strong enough to support repeated bounded AOI transient use under `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md:128`.
