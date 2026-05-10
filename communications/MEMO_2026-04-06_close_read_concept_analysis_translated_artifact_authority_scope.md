# Memo: Close Read Concept-Analysis Translated Artifact Authority Scope

Subtitle: Move translated host-contract authority for the admitted concept-analysis seams out of the-critic and into analyzer-v2, while keeping the current host/UI contract fixed

Date: 2026-04-06
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Roadmap Context:
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_live_concept_authority_cutover.md`
Immediate Completion Predecessor:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_and_thin_client_cutover_completion.md`
Immediate Scope Predecessor:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_deployment_and_cutover_scope.md`
Runtime Authority Context:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_runtime_authority_and_analyzer_mgmt_visibility_scope.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md`
Primary Code Evidence:
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_by_ref.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/concept_inferential_single_concept.json`
- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/concept_logical_single_concept.json`
- `/home/evgeny/projects/analyzer-v2/src/transformations/definitions/concept_inferential_host_contract_extraction.json`
- `/home/evgeny/projects/analyzer-v2/src/transformations/definitions/concept_logical_host_contract_extraction.json`
- `/home/evgeny/projects/analyzer-v2/src/executor/output_store.py`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_client.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/jobs/[id].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/implementations/[key].tsx`

## Purpose

Define the next bounded tranche after live runtime authority and first thin-client cutover:

- analyzer-v2 should become the authority for translated host-contract artifacts, not just the executor behind them
- analyzer-mgmt should expose those translated artifacts, their validation status, and provenance as first-class operator surfaces
- the-critic should stop acting as the authority for translated concept-analysis persistence/readback on the admitted concept seams

This stage is about authority relocation, not new concept capability.

## Bottom Line

The live authority proof changed what the honest next gap is.

The gap is no longer:

- live concept execution
- live concept workflow deployment
- live operator-console visibility
- first host cutover

The next gap is:

- translated host artifacts are still materially owned by the-critic

So the next tranche should move the translated artifact boundary itself into analyzer-v2.

## What Is Already True

The current live stack already proves:

- analyzer-v2 executes the admitted concept runs live
- analyzer-v2 runs the bounded concept workflows and host-contract transformations live
- the-critic can fetch analyzer-v2 transformation output and validate it into current host contracts
- persisted logical output now carries analyzer-v2 provenance and supports hosted scrutiny

So the architecture is already close to the target.

## What Is Still Not Architecturally Clean

Even after live cutover, the-critic still owns too much of the host-artifact seam:

- strict host-contract normalization for logical output
- translated-result persistence/readback authority
- host-visible concept-analysis read model

That means analyzer-v2 is the execution brain, but not yet the complete translated-artifact authority.

## Scope Summary

Implement one bounded translated-artifact authority tranche:

1. analyzer-v2 persists translated host-contract artifacts as first-class analyzer outputs
2. analyzer-v2 exposes those artifacts, validation status, and provenance through a stable read surface
3. analyzer-mgmt surfaces the translated artifacts and their validation/provenance alongside workflow/job/operator context
4. the-critic stops treating its local translated concept-analysis store as the semantic authority for `inferential` and `logical`
5. the-critic becomes a read-through consumer of analyzer-v2 translated artifacts, with any local cache explicitly non-authoritative

## Key Decisions To Freeze

### 1. No new substrate types

Stay inside existing analyzer-v2 types:

- engines
- operationalizations
- chains
- workflows
- transformations
- existing result/output/artifact storage surfaces

If anything is missing, repair those surfaces instead of inventing another layer.

### 2. Keep the host contract fixed

Do not redesign native concept pages or Close Read pages in this tranche.

The target contracts remain:

- current inferential host contract
- current full logical host contract

The change is where those translated artifacts become authoritative, not what the host renders.

### 3. analyzer-v2 must own translated artifact provenance and validation

For each translated host artifact, analyzer-v2 should own and expose:

- workflow key
- engine or chain key
- depth
- job/run reference
- translation template key
- contract validation status
- produced-at timestamp

### 4. analyzer-mgmt must show raw and translated sides together

The operator surface should no longer stop at workflow composition.
For this concept slice it should show:

- run/job context
- raw phase outputs
- translated host artifact
- contract validation state
- provenance linkage back to workflow and transformation

### 5. Critic thinning remains bounded

This tranche only thins the-critic further on:

- `inferential`
- `logical`

It explicitly does not widen into:

- new concept submodes
- cross-corpus concept analysis
- broader concept cache cleanup
- broader Close Read UI work

## Implementation Sequence

### Phase 1: Analyzer-v2 translated artifact authority

Add the translated host artifact as a first-class persisted analyzer-v2 output for the two admitted concept workflows.

That means analyzer-v2 should store:

- raw workflow/phase outputs
- translated host-contract artifact
- validation/provenance metadata for that artifact

### Phase 2: Analyzer-v2 read surface

Expose a stable analyzer-v2 read path for translated concept host artifacts by:

- job/run reference
- concept
- analysis mode
- project

This read path should be enough for the-critic to stop treating its own stored copy as the authority.

### Phase 3: analyzer-mgmt artifact/operator visibility

Add or extend analyzer-mgmt surfaces so an operator can inspect:

- which workflow produced the artifact
- which transformation produced the host shape
- whether validation passed
- the raw-to-translated boundary

This should integrate with the existing implementation/workflow/jobs operator trail rather than inventing a new admin app.

### Phase 4: the-critic read-through cutover

Rebind the-critic so, for `inferential` and `logical`:

- launch still goes through analyzer-v2
- polling still goes through analyzer-v2
- rendered host data is fetched from analyzer-v2 translated-artifact authority
- any local persistence/cache is explicitly secondary and non-authoritative

### Phase 5: hosted proof

Prove the full path live by showing:

- analyzer-v2 translated artifact exists and validates
- analyzer-mgmt shows it live
- the-critic renders from that artifact without reasserting semantic authority
- hosted logical scrutiny still works against the analyzer-v2-backed logical artifact

## Public Interfaces / Contract Changes

### analyzer-v2

Add a stable translated-artifact read surface for concept workflows.

The exact route shape can be decided in implementation, but it must be:

- explicit
- by-reference
- project-aware
- sufficient for thin-host consumption

### analyzer-mgmt

No new standalone product area is required.
But current live operator surfaces must expand to show translated artifact and validation/provenance state.

### the-critic

No user-facing route changes:

- `/p/:projectId/close-read/concepts`
- `/p/:projectId/close-read/concepts/:conceptSlug`
- native `/concept-analysis/...`

The contract change is architectural:

- local translated concept-analysis persistence/readback is no longer the semantic authority

## Test Plan

### analyzer-v2 artifact authority

- translated inferential host artifact persists as a first-class analyzer-v2 output
- translated logical host artifact persists as a first-class analyzer-v2 output
- artifact provenance and validation metadata are present

### analyzer-mgmt visibility

- operator can inspect the translated host artifact live in analyzer-mgmt
- operator can trace artifact -> transformation -> workflow/implementation -> underlying chain or engine
- raw and translated boundaries are both visible

### the-critic thin read-through

- the-critic renders inferential from analyzer-v2 translated artifact authority
- the-critic renders logical from analyzer-v2 translated artifact authority
- local persistence, if retained, is demonstrably non-authoritative

### hosted acceptance

- run fresh inferential and logical concept jobs
- confirm analyzer-v2 serves the translated artifacts
- confirm analyzer-mgmt shows them
- confirm the-critic renders them
- confirm hosted logical scrutiny still succeeds against the analyzer-v2-backed logical artifact

## Assumptions and Defaults

- The current live runtime-authority tranche is complete enough to move to artifact authority next.
- analyzer-v2 already has the capability substrate needed for this move.
- analyzer-mgmt should remain the operator console; the answer is to deepen it, not replace it.
- the-critic should get thinner from here, not thicker.
