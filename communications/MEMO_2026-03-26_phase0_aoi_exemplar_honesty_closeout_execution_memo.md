# Memo: Phase 0 AOI Exemplar Honesty Closeout Execution Memo

Date: 2026-03-26
Status: Draft execution memo for implementation review
Program: Dynamic Bespoke Apps Platformization
Supersedes:
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`
  - but only as the immediate next-step execution memo; the March 26 roadmap reconciliation and source-content repair closeout now define the stricter Phase 0 boundary
Depends on:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md`
- `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_completion.md`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh`
- `/home/evgeny/projects/the-critic/test-stage5-aoi-landing-smoke.js`

## Purpose

Define one bounded immediate execution memo for Phase 0.

This memo exists to generate the evidence needed for the last honest AOI exemplar judgment:

- one fresh post-fix `execution_backed` AOI rerun on the Otto Neurath corpus
- specifically the `evolution_ready` ready case from the frozen Stage 5 rubric
- one counted planner-primary browser proof on that fresh run
- one explicit Stage 2 decision written from the result

This memo is intentionally not:

- a Phase 1 planning memo
- a new AOI repair-scope memo
- a new strategic roadmap

## Summary

The approved roadmap and the latest Stage 5 closeouts now converge on one next honest move:

- run one fresh post-fix `execution_backed` AOI case through the real Critic launch route
- treat that case explicitly as the `evolution_ready` case only
- prove the planner-primary browser path on that fresh case
- grade the result honestly against the frozen Stage 5 rubric
- write the explicit Stage 2 decision

The recovered run `job-6ee8b0621177` remains useful background evidence that:

- the host/browser seam is structurally repaired
- the analyzer-side source-content identity repair is landed

But it is not closure-grade evidence and must not be reused as the final Phase 0 proof source.

The final Stage 2 decision from this memo must rest on three things together:

- the already-passed frozen Stage 5 seam-gate baseline evidence from the fixture-backed four-case pack
- whether this fresh `evolution_ready` rerun is truly `execution_backed`
- whether the combined baseline-plus-fresh evidence is strong enough to support repeated bounded AOI transient use

Phase 0 closes on the grade itself, not on whether the grade is flattering.

If the fresh rerun exposes a new seam, document it and defer it.
Do not reopen open-ended AOI repair inside this memo.

## Fixed Target

Default execution target:

- project id: `round5-proof-dossier-final-1774100000`
- thinker id: `otto_neurath`
- thinker name: `Otto Neurath`
- workflow key: `anxiety_of_influence_thematic_single_thinker`
- rubric case: `evolution_ready`
- ready-case task: `Show how Aaron Benanav's use of Otto Neurath's planning argument evolves across the corpus.`
- reference-text source directory:
  - `/home/evgeny/projects/the-critic/others/influences/otto-neurath/`
- expected local corpus inventory:
  - `Economic Writings Selections 1904-1945 - Otto Neurath - Vienna Circle Collection - 2004.pdf`
  - `Empiricism and Sociology - Otto Neurath - Vienna Circle Collection - 1973.pdf`
  - `Modern Man in the Making - Otto Neurath - A. A. Knopf - 1939.pdf`
  - `Philosophical Papers 1913-1946 - Otto Neurath - Vienna Circle Collection - 1983.pdf`

The fixed target is deliberate.

If this exact target cannot be executed fresh, stop and write a revision memo.
Do not silently switch:

- project
- thinker
- task
- workflow
- or fixture strength

## Why This Is The Next Honest Step

The Phase 0 roadmap now says:

- finish the AOI exemplar honestly with one fresh post-fix rerun
- write the Stage 2 decision explicitly
- do not keep AOI repair as the main line after that grade exists

The latest Stage 5 closeouts say:

- the repaired host/browser path now passes structurally on the recovered run
- the analyzer-side source-content identity repair is landed
- the next honest step is one fresh post-fix `execution_backed` AOI rerun on the same Otto Neurath documents

So the open question is now narrow:

- after the repair, does one fresh real `evolution_ready` AOI run stay clean enough to upgrade that case to `execution_backed` inside the already-passed fixture pack and support an honest Stage 2 decision?

That is the only question this memo should answer.

## Bounded Claim

This slice should do exactly four things:

1. verify preconditions for a valid fresh run
2. launch one fresh AOI run through the real Critic route
3. capture one counted planner-primary browser proof on that fresh run
4. write one explicit Stage 2 decision from the frozen rubric

This slice does not independently satisfy the frozen rubric's full four-case requirement.
It upgrades or fails to upgrade the `evolution_ready` case within the already-carried baseline pack for:

- `engagement_ready`
- `non_profile_ready`
- `selection_blocked`

This slice should not do any of the following by default:

- reopen host/browser repair
- reopen analyzer-side diagnosis beyond what is needed to grade the fresh run honestly
- attempt Phase 1 bridge generalization
- treat the recovered run as closure evidence
- write a broader AOI architecture memo
- update the roadmap again

## Must Land

- one fresh post-fix `execution_backed` AOI run through:
  - `POST /api/influence/thinkers/{thinker_id}/run-thematic-analysis-v2`
- one active-run boundary proof for the fresh run
- one completed-result boundary proof for the fresh run
- one counted planner-primary browser proof on the fresh run only
- one explicit Stage 2 decision memo saying either:
  - `closure-grade exemplar achieved`
  - or `bounded repaired proof only`, with the exact reason

## Must Not Widen

- no more AOI-only polish beyond what is required to run and grade the fresh rerun honestly
- do not reopen older host/browser seams into open-ended repair inside Phase 0
- if the fresh rerun exposes a new seam, document it and defer the repair rather than letting Phase 0 become another AOI branch
- do not treat a failed or disappointing grade as authority to keep Phase 0 open indefinitely
- do not pivot to Phase 1 implementation before the Phase 0 decision memo is written

## Preflight Contract

Before execution starts, verify all of the following explicitly.

### 1. Local services are running and actual ports are recorded

Record the resolved local endpoints instead of assuming defaults:

- analyzer-v2
- Critic backend
- Critic webapp

Use the real resolved ports consistently in commands and artifacts.

### 2. The required endpoints respond

At minimum verify:

- analyzer definitions/meta endpoint responds
- Critic backend responds
- Critic webapp responds

### 3. AOI selector/provider availability is confirmed

Do not start the proof if the analyzer cannot make the AOI selector call.

Record only whether the provider was available.
Do not print secrets into artifacts.

### 4. The AOI proof surface loads

Verify the browser page loads for:

- `/p/round5-proof-dossier-final-1774100000/anxiety-of-influence/otto_neurath/v2-thematic`

### 5. Otto reference texts exist for the fixed project/thinker

Use the Critic backend reference-text routes for:

- project `round5-proof-dossier-final-1774100000`
- thinker `otto_neurath`
- `GET /api/influence/thinkers/{thinker_id}/texts`
- `POST /api/influence/thinkers/{thinker_id}/texts`

Before launch, record the exact backend inventory for the thinker:

- text count
- `filename`
- `original_filename`
- `source_document_id`

The backend inventory must correspond to this exact four-document Otto corpus:

- `Economic Writings Selections 1904-1945 - Otto Neurath - Vienna Circle Collection - 2004.pdf`
- `Empiricism and Sociology - Otto Neurath - Vienna Circle Collection - 1973.pdf`
- `Modern Man in the Making - Otto Neurath - A. A. Knopf - 1939.pdf`
- `Philosophical Papers 1913-1946 - Otto Neurath - Vienna Circle Collection - 1983.pdf`

The expected text count is therefore `4`.

If the inventory is missing texts, has extra texts, or does not preserve the intended corpus boundary, stop and write a revision memo.
Do not treat "some Otto texts exist" as sufficient.

If the fixed four-document inventory is absent, upload the known Otto PDF set as multipart files through:

- `POST /api/influence/thinkers/{thinker_id}/texts`

Upload source directory:

- `/home/evgeny/projects/the-critic/others/influences/otto-neurath/`

After upload, verify both of the following before proceeding:

- the upload response shows nonzero `uploaded_count`
- a fresh `GET /api/influence/thinkers/{thinker_id}/texts` returns the exact four-document inventory above with a nonzero count

If the exact corpus inventory still does not exist after upload, stop and write a revision memo.

## Execution Sequence

### Step 1: Launch one fresh AOI run through the real Critic route

Use the real backend launch route:

- `POST /api/influence/thinkers/{thinker_id}/run-thematic-analysis-v2`

Required launch truth:

- returned `job_id`
- returned `status`
- returned `workflow_key`
- returned `created_at`

For this proof, treat the returned Critic `job_id` as the analyzer-v2 job id for the fresh run.
Do not imply a separate fresh local identity at launch time.

### Step 2: Capture the active-run boundary

While the fresh run is still active:

- run the direct-poll smoke once against the active run id
- preserve the script output as a proof artifact

This artifact is supplemental.
It does not replace the counted browser proof.

### Step 3: Poll the fresh run to durable completion

Poll the generic AOI job-detail route until the fresh run reaches durable `completed` or a hard timeout:

- `GET /api/analysis/anxiety_of_influence_thematic_single_thinker/jobs/{job_id}`

For this memo, authoritative completion means the job-detail response reports:

- `status == "completed"`

Preserve at minimum:

- `job_id`
- `v2_job_id`
- `analysis_id`
- completion status
- selected thinker identity
- workflow key

Operational expectation:

- use a bounded hard timeout such as `180` minutes
- if the run fails or times out, stop and write a revision memo instead of improvising a new proof path

### Step 4: Capture the completed-result boundary

After completion:

- run the direct-poll smoke again against the completed result
- preserve the output as a proof artifact

This artifact is also supplemental.
It does not replace the counted browser proof.

### Step 5: Run the counted planner-primary browser proof on the fresh run only

Use the real AOI V2 thematic page.

Establish the proof source in this exact order:

1. click `Clear`
2. confirm the observable post-`Clear` UI condition:
   - no saved result is selected
   - `Plan source-backed handoff` is disabled
3. explicitly row-pin the fresh run
4. capture the row-pin artifact
5. only then continue into planner-backed handoff

This sequence is mandatory because the current AOI panel auto-loads the latest saved result and otherwise falls back to the first saved result until explicit source selection is forced by `Clear`.

Stay on the planner-primary branch only:

- no legacy dossier/comparison fallback
- no profile/autostart shortcut as substitute for the planner-backed path

Required browser-proof conditions:

- the fixed task text is used
- the fresh run is the proof source through `Clear -> explicit row pin -> planner-backed handoff`, not through default page state
- `source_v2_job_id` is preserved end to end as the canonical proof identity
- the host-boundary `source_analysis_id` is preserved only as supporting continuity evidence and must not override canonical proof identity
- the compose request remains planner-primary

Required captured artifacts:

- corpus inventory artifact
- pre-submit compose-page artifact showing:
  - planner-backed selection summary
  - selected-source list
  - rejected-source list if present
  - the visible `Compose planned AOI selection` button before the request fires
- row-pin artifact captured after `Clear`, after explicit fresh-run selection, and before planner-backed handoff continues
- request JSON artifact
- HAR artifact
- screenshot artifact

### Step 6: Grade the exemplar honestly against the frozen rubric

Grade at minimum:

- `selection_fit`
- `rationale_clarity`
- `rendered_usefulness`
- `operational_behavior`

Use the frozen rubric in:

- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`

Apply that rubric to this memo honestly as one fresh `evolution_ready` case only, carried on top of the already-passed fixture-backed baseline pack for the other cases.

Do not soften the bar after seeing the result.

### Step 7: Write the explicit Stage 2 decision

The decision memo must state separately:

- carried-forward Stage 5 seam-gate status from the frozen baseline pack
- whether this fresh `evolution_ready` case is truly `execution_backed`
- whether the combined baseline-plus-fresh evidence is strong enough to support repeated bounded AOI transient use
- Stage 2 closure status

The final verdict line must say one of two things only:

- `closure-grade exemplar achieved`
- `bounded repaired proof only`

If the answer is non-closure, name the exact reason without softening.
Do not phrase this memo as if one fresh rerun independently reruns or satisfies the full four-case gate.

## Closeout Rules

There are three valid closeout shapes.

### Closeout A: Valid fresh attempt, closure-grade result

If the fresh rerun is closure-grade:

- write the Stage 2 decision memo as closure-grade
- mark Phase 0 complete
- move the main line to Phase 1

### Closeout B: Valid fresh attempt, non-closure result

If the fresh rerun is not closure-grade but is still honestly gradable:

- write the Stage 2 decision memo as bounded repaired proof only
- preserve the exact non-closure reason
- mark Phase 0 complete anyway
- move the main line to Phase 1 using that failure as the boundary condition

### Closeout C: Invalid attempt because truthful grading was impossible

If truthful grading was impossible because of:

- missing reference texts
- provider unavailability
- launch failure
- hard timeout
- or another precondition/infrastructure failure that prevents a valid Phase 0 attempt

Then:

- write a bounded revision memo
- do not widen into repair inside the same slice
- do not claim a Phase 0 grade exists yet

## Suggested Artifact Outputs

If execution happens on a later date, keep the filename stems and replace the date.

Suggested proof artifacts:

- `communications/PROOF_phase0_aoi_execution_backed_launch_2026-03-26.json`
- `communications/PROOF_phase0_aoi_execution_backed_active_boundary_2026-03-26.json`
- `communications/PROOF_phase0_aoi_execution_backed_completed_boundary_2026-03-26.json`
- `communications/PROOF_phase0_aoi_execution_backed_corpus_inventory_2026-03-26.json`
- `communications/PROOF_phase0_aoi_execution_backed_compose_pre_submit_2026-03-26.png`
- `communications/PROOF_phase0_aoi_execution_backed_row_pin_2026-03-26.json`
- `communications/PROOF_phase0_aoi_execution_backed_requests_2026-03-26.json`
- `communications/PROOF_phase0_aoi_execution_backed_session_2026-03-26.har`
- `communications/PROOF_phase0_aoi_execution_backed_state_2026-03-26.png`

Suggested decision closeout:

- `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_decision.md`

Suggested revision closeout if no valid attempt exists:

- `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_revision.md`

## Existing Helpers

These helpers are useful when they match the bounded proof need, but they are not substitutes for the browser proof itself:

- `/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh`
- `/home/evgeny/projects/the-critic/test-stage5-aoi-landing-smoke.js`

If the direct-poll helper is used, follow the invocation examples in:

- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`

Do not assume helper defaults are correct for AOI, because the direct-poll script requires explicit project/workflow inputs.

## Final Constraint

This memo should generate the last honest AOI exemplar judgment and then stop.

It should not become another vehicle for:

- extending AOI-only work
- redesigning the architecture
- or reopening the roadmap
