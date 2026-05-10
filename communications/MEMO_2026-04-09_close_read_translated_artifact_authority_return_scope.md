# Memo: Close Read Translated Artifact Authority Return Scope

Subtitle: Resume the deferred architectural corridor by moving translated host-artifact authority further out of the-critic and into analyzer-v2, now that the host persistence and scrutiny closure slice is complete

Date: 2026-04-09
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Roadmap Context:
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_live_concept_authority_cutover.md`
- `communications/MEMO_2026-04-09_close_read_roadmap_update_after_project_scoped_persistence_and_scrutiny_closure.md`
Immediate Completion Predecessor:
- `communications/MEMO_2026-04-09_close_read_project_scoped_persistence_and_fresh_scrutiny_closure_completion.md`
Immediate Architectural Predecessor:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_translated_artifact_authority_scope.md`
Primary Live Evidence:
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?consumer_key=the-critic&external_project_id=cutover-project-scope-20260409-121336-u&concept_name=innovation&analysis_mode=logical&analyzer_v2_job_id=job-plan-d9ed0f9db367`
- `https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical` with header `X-Project-ID: cutover-project-scope-20260409-121336-u`
- `https://the-critic.onrender.com/api/concept/jobs/concept-1775736818361-44c7b8`
- `https://the-critic.onrender.com/api/scrutiny/results/innovation` with header `X-Project-ID: cutover-project-scope-20260409-121336-u`
Primary Code Evidence:
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_by_ref.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/output_store.py`
- `/tmp/critic-logical-readback-closure/analyzer/concept_analyzer/analyzer_v2_client.py`
- `/tmp/critic-logical-readback-closure/analyzer/concept_analyzer/analyzer_v2_recomposition.py`
- `/tmp/critic-logical-readback-closure/api/server.py`
Deployed Remote Reality Check:
- the current local analyzer-v2 checkout may lag the deployed Render code for this seam
- the live deployed stack already exposes a working dedicated translated-artifact read route and supporting authority code
- this tranche must therefore treat local/live alignment as explicit work rather than assuming the local checkout is the full truth

## Purpose

Resume the architectural corridor that was temporarily interrupted by host persistence and scrutiny closure work.

The immediate question is no longer whether the admitted concept seam can run, persist, read back, and support scrutiny.
It can.

The immediate question is again:

- why the-critic still materially owns too much of translated host-artifact normalization, persistence, and read authority
- how to move that authority boundary into analyzer-v2 without redesigning the host contract

## Bottom Line

The next honest tranche is not more host debugging.

The next honest tranche is:

1. consolidate and verify the analyzer-v2 translated-artifact authority that is already live on Render
2. align the local analyzer-v2 checkout and docs to that deployed authority surface
3. make analyzer-mgmt show raw outputs, translated artifacts, validation, and provenance together for this concept seam
4. reduce the-critic to a thinner read-through consumer for `inferential` and `logical`

## What Is Already True

The system now proves all of the following on a fresh live project:

- analyzer-v2 executed the logical run
- analyzer-v2 produced a translated host artifact
- exact analyzer-v2 artifact lookup validated successfully
- the-critic completed the logical job and read it back
- the same logical artifact supported a fresh scrutiny run and persisted readback

Concrete live proof specimen:

- project: `cutover-project-scope-20260409-121336-u`
- critic logical job: `concept-1775736818361-44c7b8`
- analyzer-v2 logical job: `job-plan-d9ed0f9db367`
- scrutiny job: `scrut-1775747770360-df335f`

That means the corridor no longer needs to spend time proving that the admitted concept family basically works.

It also means the next tranche is not invention from zero.

The live deployed stack already proves:

- a dedicated analyzer-v2 translated-artifact read route exists and works
- exact-run lookup by `analyzer_v2_job_id` works
- latest-validated lookup by project/concept/mode identity works

So the next tranche is partly consolidation, local/live alignment, operator-surface repair, and host cutover, not greenfield artifact-authority invention.

## What Is Still Not Architecturally Clean

Even after live closure, the-critic still owns too much of the semantic host seam:

- local normalization and recomposition logic for host-facing concept artifacts
- host-visible persistence/readback authority for concept analyses
- local mirroring that is still too close to semantic ownership rather than pure compatibility caching

So analyzer-v2 is already the execution and validation brain, but it is not yet the clean sole authority for translated host artifacts.

The remaining architectural dirt is concentrated in two places:

- the-critic still performs too much local translation/persistence/read authority work
- analyzer-mgmt is not yet a concrete concept-translated-artifact operator surface live

## Scope Summary

Implement one bounded translated-artifact authority tranche:

1. verify and formalize the already-live analyzer-v2 translated-artifact authority surface
2. align the local analyzer-v2 checkout and docs with that deployed authority surface
3. surface the raw-to-translated boundary clearly in analyzer-mgmt
4. rebind the-critic so local persisted copies are explicitly secondary and non-authoritative for `inferential` and `logical`

This stage is about authority relocation, not new concept capability.

## Key Decisions To Freeze

### 1. Keep the host contract fixed

Do not redesign the native concept pages or Close Read concept pages in this tranche.

The target contracts remain:

- current inferential host contract
- current full logical host contract

The change is where those artifacts become authoritative, not what the host renders.

### 2. No new substrate types

Stay inside existing analyzer-v2 surfaces:

- workflows
- transformations
- executor output storage
- orchestrator read surfaces
- analyzer-mgmt operator surfaces

If anything is missing, extend those surfaces rather than inventing a new layer.

The important correction here is:

- the dedicated analyzer-v2 translated-artifact read route already exists live
- the tranche should consolidate around that route and its supporting authority code rather than pretending the read surface must be invented from zero

### 3. analyzer-v2 owns provenance and validation

For each translated host artifact, analyzer-v2 should own and expose:

- workflow key
- engine or chain key
- depth
- analyzer-v2 job id
- translation template key
- contract validation status
- produced-at timestamp

This is already substantially true on the deployed route and should be treated as the starting point for consolidation, not a hypothetical future surface.

### 4. the-critic local persistence becomes explicitly secondary

For `inferential` and `logical`:

- local the-critic persistence may remain as compatibility cache if needed
- but it must not be treated as the semantic source of truth

### 5. Keep the boundary narrow

Do not widen into:

- new concept submodes
- cross-corpus concept analysis
- broader cache cleanup
- broader Close Read UI work
- standalone Close Read extraction

### 6. analyzer-mgmt must be treated as needing explicit concept-seam work

Do not assume analyzer-mgmt is already an adequate operator console for this exact seam.

What is true today:

- generic workflow/composition pages exist
- generic jobs pages exist

What is not yet good enough live:

- the concept implementation page is not yet a trustworthy operator surface for `concept_logical_single_concept`
- the concept translated artifact, validation state, and provenance are not yet coherently surfaced on the live concept job/operator trail

## Implementation Sequence

### Phase 1: verify deployed analyzer-v2 artifact authority and align local code

Treat the live deployed analyzer-v2 authority surface as the starting point, not an assumption.

Verify and document:

- exact-run translated-artifact lookup
- latest-validated translated-artifact lookup
- provenance and validation fields returned live
- where the supporting authority code lives on the deployed remote

Then align the local analyzer-v2 checkout and docs so the local implementation story matches what is already live.

### Phase 2: formalize analyzer-v2 artifact authority as the canonical path

Use the existing live translated-artifact route and supporting authority code as the canonical read path for this seam.

If any consolidation is still needed, keep it inside:

- orchestrator read surfaces
- existing result/output storage
- existing host-contract authority code

### Phase 3: analyzer-mgmt operator visibility

Extend analyzer-mgmt so operators can inspect, on the same job/operator trail:

- raw phase outputs
- translated host artifact
- validation state
- provenance linkage back to workflow and transformation

This phase must explicitly include concept-seam repair where needed.

At minimum:

- fix the broken concept implementation/detail surface
- make the concept translated artifact and validation state visible from the live job/operator trail
- do not claim analyzer-mgmt is already good enough for this seam until that is proven in browser, not just assumed from generic pages

### Phase 4: thinner host cutover

Rebind the-critic so, for `inferential` and `logical`:

- launch still goes through analyzer-v2
- polling still goes through analyzer-v2
- host-visible rendering reads from analyzer-v2 translated-artifact authority
- local persistence is explicitly secondary

### Phase 5: fresh live proof

Reprove the full path live by showing:

- analyzer-v2 translated artifact exists and validates
- analyzer-mgmt shows it
- the-critic renders from analyzer-v2 artifact authority
- hosted scrutiny still works against the analyzer-v2-backed logical artifact

The previous host-correctness proof project above should now be treated as the baseline specimen that justifies starting this tranche, not as unfinished proof work that still needs closure.

## Updated Bottom Line

The roadmap is back on its real architectural task:

- **analyzer-v2 owns translated host artifacts**
- **analyzer-mgmt exposes the raw-to-translated boundary**
- **the-critic becomes thinner still**

But the honest wording after the April 10 reviews is:

- analyzer-v2 already owns substantial translated-artifact authority live
- analyzer-mgmt still needs explicit concept-seam operator work
- the-critic still needs the main cutover away from local semantic ownership
