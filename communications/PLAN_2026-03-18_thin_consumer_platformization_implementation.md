# Plan: Thin Consumer Platformization Implementation

Date: 2026-03-18

## Purpose

This plan translates the execution brief into repo/file-owned implementation work.

It is meant to answer:

- which repo owns each deliverable
- which files are the primary work surfaces
- what order to execute the work in
- what the proof outputs and verification steps should be

This plan assumes the scope defined in:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_snapshot_after_stage9.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`

## Working Order

If someone asks "which repo do I open first?", the answer should be:

1. **Open `the-critic` first** for the forcing-function work:
   - proving vehicle lives there
   - host-thinning pain is visible there
   - consumer contract duplication is visible there
2. **Open `analyzer-v2` second** for the first artifact proof and any run/result contract additions the workspace actually needs
3. **Return to `the-critic` last** to complete the cross-workflow workspace proof and write the proof record

This order is deliberate.
It prevents the program from drifting into abstract analyzer-v2 substrate work before the host boundary and consumer needs are made concrete.

## Repo Ownership Summary

| Deliverable | Primary repo | Secondary repo | Why |
|---|---|---|---|
| Stage 9 closure tail | `the-critic` + docs | `analyzer-v2` communications | The residuals are Critic-facing, but the closure record lives in the program docs |
| Deliverable A: authority / routing boundary | `the-critic` | `analyzer-v2` | The Critic still carries the polling-era plumbing; analyzer-v2 may need small API/observability additions |
| Deliverable B: consumer contract / host adapter | `the-critic` | none initially | The first proof should be a shared module/pattern inside the proving vehicle before package extraction |
| Deliverable C: first artifact reuse proof | `analyzer-v2` | none | Stable identity, lookup, freshness, and manifest reuse signal all belong upstream |
| Deliverable D: cross-workflow generic workspace proof | `the-critic` | `analyzer-v2` | The proving vehicle is the generic workspace, but it depends on upstream manifest/run fields |

## Phase 0: Close The Stage 9 Tail

### Primary repo

- `the-critic`

### Files

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_snapshot_after_stage9.md`

### Tasks

1. Resolve or explicitly waive the three `v2_run_references.corpus_ref` `NULL` rows for the late post-cutover AOI jobs.
2. Resolve or explicitly waive the missing legacy-warning evidence item.
3. Link the Stage 9 snapshot and next-steps memos from the Stage 9 runbook or evidence home.

### Verification

- Each closure item is either resolved or explicitly waived in writing.

## Phase 1: Deliverable A

## A1. `the-critic`: Remove Primary-Path Polling-Era Ownership

### Primary repo

- `the-critic`

### Files

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_client.py`
- `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`

### Current pain points

- `_GENEALOGY_JOBS`
- `_V2_JOB_MAPPINGS`
- compatibility logic in `get_genealogy_job()`
- primary-path dependence on Critic-side advisory state for cancel/resume/import/cache flows

### Tasks

1. Demote `_GENEALOGY_JOBS` and `_V2_JOB_MAPPINGS` from primary bounded-v2 authority to:
   - local-only legacy compatibility, or
   - imported-local snapshot alias handling only
2. Make the generic analysis cancel/resume/import/cache routes obviously thin wrappers over analyzer-v2-backed identity.
3. Remove any remaining primary-path expectation that Critic owns bounded-v2 job progress truth.
4. Keep only host responsibilities that still legitimately belong to The Critic:
   - project/document loading
   - start-path payload assembly
   - compatibility cache when explicitly needed

### Verification

- bounded-v2 job truth is not lost if Critic-local polling-era state disappears
- generic analysis routes still work for cancel/resume/import/cache

## A2. `analyzer-v2`: Supply Any Missing API / Observability Fields

### Primary repo

- `analyzer-v2`

### Files

- `/home/evgeny/projects/analyzer-v2/src/api/routes/runs.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/results.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/run_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_run_contract.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`

### Tasks

1. Confirm the generic workspace has the upstream fields it needs for:
   - active run discovery
   - completion transition
   - restore availability
   - selected thinker identity for AOI
2. Add any missing run/result manifest fields needed to support the proving vehicle cleanly.
3. Keep these changes small and driven by the proving vehicle, not by abstract API design.

### Verification

- `AnalysisWorkspacePage` can rely on analyzer-v2 run/result contracts without needing Critic-only reconstruction

## Phase 2: Deliverable B

## B1. Create A Shared Consumer Contract Inside `the-critic`

### Primary repo

- `the-critic`

### Files

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyPage.tsx`
- new shared module(s), recommended:
  - `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts`
  - `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts`

### Why this lives in `the-critic` first

The first proof is not package extraction.
The first proof is that the proving vehicle stops copying the same bounded-v2 logic inline.

### Tasks

1. Extract the repeated bounded-v2 behaviors into a shared client/host-adapter layer:
   - run discovery
   - run-by-job polling
   - result manifest fetch
   - result presentation fetch
   - refresh-presentation
   - cache-v2 handoff
   - cancel/resume wrapper calls
2. Make `AnalysisWorkspacePage` use that shared layer.
3. Make at least one second bounded surface use the same shared layer:
   - preferred: `AoiV2ThematicPanel`
   - optional follow-on: `GenealogyPage`
4. Document the host contract in code comments or a local frontend note so the next consumer does not infer its behavior from copy-paste.

### Verification

- the proving vehicle imports the contract instead of carrying custom inline fetch/poll logic
- at least one second bounded surface also uses the same shared contract

## Phase 3: Deliverable C

## C1. Implement The First Artifact Reuse Proof In `analyzer-v2`

### Primary repo

- `analyzer-v2`

### Files

- `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/run_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/presentation_api.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_presentation_api.py`

### First proof only

- artifact class: `genealogy.relationship_classification`
- jobs: exactly 2
- freshness rule: exactly 1
- lookup path: exactly 1

### Tasks

1. Define stable reusable identity for the `genealogy.relationship_classification` artifact class.
2. Define one freshness rule for when Job 2 may reuse Job 1's artifact.
3. Implement one lookup path for reuse resolution.
4. Expose the reuse signal in the Job 2 result manifest for the `genealogy.relationship_classification` family.
5. Use the explicit observable required by the execution brief:
   - `reuse_state = "reused"`
   - `reused_from_job_id = "<job-1-id>"`
6. Add hit/miss coverage in tests.

### Verification

- Job 1 computes/stores the artifact
- Job 2 reuses it
- Job 2 manifest exposes the required reuse signal

## Phase 4: Deliverable D

## D1. Make `AnalysisWorkspacePage` The Cross-Workflow Proof Surface

### Primary repo

- `the-critic`

### Files

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useWorkflowMetadata.ts`
- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx`
- `/home/evgeny/projects/the-critic/api/models_genealogy.py`
- `/home/evgeny/projects/the-critic/api/server.py`

### Why this phase exists

The proving vehicle only counts if it can carry both bounded workflows, not just genealogy.

### Tasks

1. Make `AnalysisWorkspacePage` capable of starting/restoring AOI thematic runs without collapsing back into bespoke page logic.
2. Pass AOI-required bounded parameters cleanly through the generic path:
   - at minimum `selected_source_thinker_id`
3. Add or refine the route/entry behavior from the AOI page so the generic workspace can be exercised deliberately for the AOI workflow.
4. Keep the solution bounded:
   - do not broaden into a general dynamic-form system
   - do not rewrite the full AOI page

### Verification

- `AnalysisWorkspacePage` can run or restore `intellectual_genealogy`
- `AnalysisWorkspacePage` can run or restore `anxiety_of_influence_thematic_single_thinker`
- both use the same shared consumer contract from Phase 2

## Phase 5: Proof Record

### Primary repo

- `analyzer-v2` communications

### File to create

- `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-XX_thin_consumer_platformization_round1.md`

### Owner

- the maintainer closing Deliverable D

### Required contents

1. the two bounded workflows proved via `AnalysisWorkspacePage`
2. the two genealogy job ids used in the artifact reuse proof
3. the exact Job 2 manifest reuse signal
4. whether each execution-brief exit criterion passed, failed, or was explicitly deferred

## Non-Goals For This Plan

This plan does **not** include:

- a new standalone consumer app
- multi-thinker AOI work
- broad dynamic page generation
- package extraction of the consumer contract before the in-repo proof exists
- platform-wide artifact economy generalization

## Done Means

This implementation plan is complete only when the execution brief exit criteria are met.

That means:

1. generic workspace proof across genealogy + AOI
2. no primary-path dependence on polling-era Critic run ownership
3. shared consumer contract used rather than copied
4. one real artifact reuse proof with manifest-level signal
5. one written proof record

Until then, dynamic-composition work remains blocked by design.
