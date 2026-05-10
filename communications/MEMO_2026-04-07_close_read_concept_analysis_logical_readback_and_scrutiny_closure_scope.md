# Memo: Close Read Concept-Analysis Logical Readback And Scrutiny Closure Scope

Subtitle: Close the remaining post-execution gap on the admitted logical seam by making fresh analyzer-v2-backed logical completion materialize into the-critic readback and scrutiny surfaces on a brand-new project

Date: 2026-04-07
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Close Read Roadmap Context:
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_live_concept_authority_cutover.md`
Immediate Scope Predecessor:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_translated_artifact_authority_scope.md`
Immediate Completion Context:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_and_thin_client_cutover_completion.md`
Primary Live Evidence:
- `https://the-critic.onrender.com/api/concept/jobs/concept-1775492799147-00033a`
- `https://the-critic.onrender.com/api/concept/jobs/concept-1775493067650-78640a`
- `https://analyzer-v2.onrender.com/v1/executor/jobs/job-plan-547eea461fe3`
- `https://analyzer-v2.onrender.com/v1/executor/jobs/job-plan-03f3e58a8ac6`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?consumer_key=the-critic&external_project_id=cutover-artifact-authority-20260406-162636&concept_name=innovation&analysis_mode=inferential&analyzer_v2_job_id=job-plan-547eea461fe3`
- `https://the-critic.onrender.com/api/concept/analyses/innovation`
- `https://the-critic.onrender.com/api/scrutiny/results/innovation`
Primary Code Evidence:
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_by_ref.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/workflow_runner.py`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_client.py`

## Purpose

Define the next bounded fix after translated-artifact authority landed live:

- fresh `inferential` proof is now closed end to end
- fresh `logical` execution also completes in analyzer-v2 and the-critic
- but the-critic readback and scrutiny surfaces still do not close on that fresh logical run

This tranche is not about new execution capability.
It is about making a completed analyzer-v2-backed logical run reliably materialize into:

- the-critic concept-analysis readback
- the-critic scrutiny input/launch surface if needed
- the-critic scrutiny result persistence/readback surface if needed

for a brand-new project with no stale host-local history.

## Bottom Line

The current live state is asymmetric:

- fresh inferential proof on the new project is complete
- fresh logical execution on the same new project is complete
- but the host-visible logical read model is not closing

The exact live evidence is:

- project: `cutover-artifact-authority-20260406-162636`
- inferential critic job: `concept-1775492799147-00033a`
- inferential analyzer-v2 job: `job-plan-547eea461fe3`
- logical critic job: `concept-1775493067650-78640a`
- logical analyzer-v2 job: `job-plan-03f3e58a8ac6`

This should be read as a regression from the earlier hosted logical proof, not as evidence that logical readback has never worked.

The immediate completion predecessor already proved logical readback and scrutiny on:

- project: `cutover-live-tiny-20260406`
- critic job: `concept-1775483282630-a0a4aa`
- analyzer-v2 job: `job-plan-bb384ca511fa`

Live facts:

- `job-plan-03f3e58a8ac6` completed in analyzer-v2
- `concept-1775493067650-78640a` completed in the-critic
- `GET /api/concept/analyses/innovation` with `X-Project-ID: cutover-artifact-authority-20260406-162636` returned `404`
- `GET /api/scrutiny/results/innovation` on that same project returned `count = 0`

So the remaining honest gap is:

- post-completion logical persistence/readback closure on the host side

not:

- analyzer-v2 execution
- exact analyzer-v2 artifact lookup
- inferential artifact authority

## What Is Already True

### 1. analyzer-v2 translated-artifact authority is live

The deployed stack exposes a live exact-artifact route and fresh inferential already proved that it works.

The current local checkout should not be treated as the canonical authority for that route shape by itself:

- local `orchestrator.py` in this checkout still visibly shows the launch `POST`
- the live deployed stack is what proved the exact read surface
- this memo is therefore grounded in live evidence first, not in the assumption that this checkout fully mirrors deployed analyzer-v2

Fresh inferential proof already demonstrated:

- exact lookup by `analyzer_v2_job_id`
- `lookup_mode = "exact_run"`
- `contract_validation_status = "passed"`

### 2. the-critic is already fetching exact analyzer-v2 artifacts

The current host path no longer depends on local semantic translation as primary authority for the admitted seams.

For fresh inferential, this is already proven live.

### 3. The remaining failure is downstream of logical completion

The logical chain reached completion on analyzer-v2 and the-critic still marked the concept job completed.

So the bug surface is narrower than “logical execution is broken.”

The strongest default diagnosis from the current code is not generic “readback closure” in the abstract.
It is more specifically:

- silent host persistence failure on the logical save path

because `_save_concept_analysis_to_db(...)` in `/home/evgeny/projects/the-critic/api/server.py` currently catches exceptions and only logs a warning, while the surrounding concept job can still be marked completed in memory.

Secondary possibilities remain:

- logical readback querying the wrong storage identity or shape
- logical persistence succeeding but readback filtering failing
- scrutiny result persistence/readback failing separately after logical persistence is fixed

## Scope Summary

Implement one narrow closure tranche:

1. trace the completed fresh logical run from analyzer-v2 artifact authority into the-critic persistence layer
2. repair whatever prevents that completed logical artifact from appearing in `GET /api/concept/analyses/:concept`
3. verify whether scrutiny closure now follows automatically; if not, repair only the remaining scrutiny-specific persistence/readback seam
4. rerun the final fresh logical plus scrutiny proof on a brand-new project id

This tranche should stop once the fresh logical seam is symmetric with fresh inferential.

## Key Decisions To Freeze

### 1. Do not reopen artifact-authority design

Assume the analyzer-v2 exact artifact surface is correct unless direct evidence falsifies it.

The live inferential proof already shows:

- exact read contract works
- analyzer-v2 artifact storage works
- exact-job-id fetch in the-critic works

So this tranche should not drift back into redesigning the artifact-authority boundary.

### 2. Treat silent host persistence failure as the default diagnosis until disproven

The default assumption should be:

- logical artifact authority exists upstream
- the host-side logical save path is the first place to inspect
- only after that should the investigation broaden to readback filtering or other mapping issues

The specific code reason for this default is:

- `_save_concept_analysis_to_db(...)` currently swallows persistence exceptions with `logger.warning(...)`
- `run_concept_analysis_thread(...)` can still mark the job `completed` after that call

That pattern matches the observed live symptom exactly:

- job completes
- readback returns `404`

Only broaden scope if direct evidence shows the analyzer-v2 logical artifact itself is absent or invalid.

### 3. Keep the seam bounded to `logical`

Inferential is already closed on the fresh project.

This tranche should not re-open inferential unless the logical fix unexpectedly requires a shared-path repair.

### 4. Scrutiny must remain analyzer-v2-backed

The fix must not reintroduce fallback to old local-runtime-only logical data.

The target state remains:

- scrutiny derives from analyzer-v2-backed translated logical output
- persisted logical result shows `_analysis_provenance.execution_owner == "analyzer-v2"`

### 5. analyzer-mgmt is adjacent evidence, not critical path

analyzer-mgmt may provide useful operator evidence during debugging, but it is not the critical-path seam for this bug.

This tranche should only touch analyzer-mgmt if direct debugging requires an operator-surface confirmation of:

- the completed logical analyzer-v2 job
- the translated logical artifact
- the workflow/transformation provenance

## Implementation Sequence

### Phase 1: Trace the completed fresh logical run end to end

Use the completed fresh logical run as the debugging specimen:

- project `cutover-artifact-authority-20260406-162636`
- critic job `concept-1775493067650-78640a`
- analyzer-v2 job `job-plan-03f3e58a8ac6`

Confirm, with code-backed tracing, all of the following:

- exact analyzer-v2 logical artifact exists or can be read for `job-plan-03f3e58a8ac6`
- the-critic receives it
- the-critic attempts to persist it through `_save_concept_analysis_to_db(...)`
- whether `_save_concept_analysis_to_db(...)` raises internally and gets silently swallowed
- the-critic readback path for `/api/concept/analyses/:concept` can or cannot see it

This phase should end with one explicit root-cause statement, not a vague suspicion.

### Phase 2: Repair logical persistence/readback closure

Fix the identified seam so a completed fresh logical run becomes visible through:

- `GET /api/concept/analyses/:concept`
- native concept-analysis rendering surfaces
- Close Read concept surfaces if they depend on the same read model

If the issue is shared between persistence and readback, fix both together.

### Phase 3: Verify scrutiny closure, then repair only if it remains open

Do not assume scrutiny requires a separate repair before proving that logical persistence/readback is fixed.

Split scrutiny into two distinct checks:

1. scrutiny input/launch closure
2. scrutiny result persistence/readback closure

That means:

- argument inventory is visible where scrutiny expects it
- scrutiny target selection can resolve a real argument/premise from the new logical result
- scrutiny result persistence/readback closes on the same project if a fresh scrutiny job is launched

If logical persistence/readback repair makes scrutiny work automatically, do not widen scope with extra scrutiny-specific changes.

### Phase 4: Fresh rerun proof

Run the final proof again on a brand-new project id, not the previously used one.

The rerun must include:

- fresh logical run
- exact analyzer-v2 logical artifact lookup by exact `analyzer_v2_job_id`
- fresh scrutiny run on that new logical result
- successful host readback through:
  - `/api/concept/analyses/:concept`
  - `/api/scrutiny/results/:concept`

## Public Interfaces / Contract Changes

No user-facing route changes.

The relevant interfaces stay:

- analyzer-v2 exact artifact read:
  - `GET /v1/orchestrator/concept-analysis-by-ref/result`
- the-critic concept readback:
  - `GET /api/concept/analyses/:concept`
- the-critic scrutiny readback:
  - `GET /api/scrutiny/results/:concept`

The change is behavioral:

- a completed fresh logical run must now appear consistently across those existing read surfaces

## Test Plan

### 1. Root-cause trace

For completed logical run `job-plan-03f3e58a8ac6` / `concept-1775493067650-78640a`, verify:

- exact analyzer-v2 artifact exists
- the-critic can fetch it
- persistence step succeeds or fails in a directly observable way
- readback step returns it

Document the exact failing seam before shipping the fix.

### 2. Focused regression

After the fix:

- fresh inferential proof remains valid
- fresh logical completion still succeeds
- logical readback now returns persisted data instead of `404`
- if a fresh scrutiny job is launched, scrutiny readback no longer returns empty results

### 3. Final hosted proof

Use a brand-new project id:

- `cutover-logical-readback-closure-<UTC-yyyymmdd-hhmmss>`

Record:

- critic logical job id
- analyzer-v2 logical job id
- scrutiny job id

Confirm:

- exact logical artifact lookup returns `lookup_mode = "exact_run"`
- persisted logical result contains `_analysis_provenance.execution_owner = "analyzer-v2"`
- `/api/concept/analyses/:concept` returns the new logical artifact
- if a fresh scrutiny job is launched, scrutiny succeeds against that new logical artifact
- if a fresh scrutiny job is launched, `/api/scrutiny/results/:concept` returns the new scrutiny result

## Out Of Scope

This tranche does not include:

- new concept submodes
- inferential redesign
- broader cache cleanup
- analyzer-mgmt redesign
- new Close Read UI work
- cross-corpus concept work

## Completion Condition

This tranche is complete only when the live stack proves all three of these together on a brand-new project:

1. fresh logical execution completes
2. fresh logical readback closes through the-critic
3. fresh scrutiny closes against that same logical artifact

Until then, the admitted concept slice should be treated as:

- fresh inferential: closed
- fresh logical execution: closed
- fresh logical readback and scrutiny closure: still open
