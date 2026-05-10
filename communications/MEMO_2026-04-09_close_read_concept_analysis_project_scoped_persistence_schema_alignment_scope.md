# Memo: Close Read Concept-Analysis Project-Scoped Persistence Schema Alignment Scope

Subtitle: Correct the live host persistence seam by aligning `concept_analyses` uniqueness with multi-project runtime semantics, then rerun fresh logical readback and scrutiny proof

Date: 2026-04-09
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Close Read Roadmap Context:
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_live_concept_authority_cutover.md`
Immediate Superseded Scope:
- `communications/MEMO_2026-04-07_close_read_concept_analysis_logical_execution_completion_stall_closure_scope.md`
Immediate Architectural Context:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_translated_artifact_authority_scope.md`
Immediate Host Closure Context:
- `communications/MEMO_2026-04-07_close_read_concept_analysis_logical_readback_and_scrutiny_closure_scope.md`
Primary Review Corrections:
- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Logical_Execution_Completion_Stall_Closure_Scope_Audit_2026-04-07.md`
- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Logical_Execution_Completion_Stall_Closure_Scope_Critique_2026-04-07.md`
Primary Live Evidence:
- `https://the-critic.onrender.com/api/concept/jobs/concept-1775529506826-c585ea`
- `https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical` with header `X-Project-ID: cutover-logical-readback-closure-20260407-023428`
- `https://the-critic.onrender.com/api/projects/cutover-logical-readback-closure-20260407-023428/documents`
- `https://analyzer-v2.onrender.com/v1/executor/jobs/job-plan-936b5b61e93f`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?consumer_key=the-critic&external_project_id=cutover-logical-readback-closure-20260407-023428&concept_name=innovation&analysis_mode=logical&analyzer_v2_job_id=job-plan-936b5b61e93f`
Primary Code Evidence:
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/api/models_db.py`
- `/home/evgeny/projects/the-critic/api/alembic/versions/001_initial_schema.py`
- `/home/evgeny/projects/the-critic/api/alembic/versions/017_add_multi_project_support.py`
- `/home/evgeny/projects/the-critic/render.yaml`

## Purpose

Replace the falsified analyzer-v2-stall diagnosis with the current live-supported blocker:

- analyzer-v2 logical execution completes
- the exact translated logical artifact validates successfully
- the-critic fails to persist the fresh project-scoped logical result because the live database uniqueness rule still ignores `project_id`

This tranche should fix that host schema/runtime mismatch first, then rerun fresh logical readback and scrutiny proof.

## Bottom Line

The active blocker is not analyzer-v2 execution.

The active blocker is:

- `the-critic` runtime writes concept analyses as if they are unique per `(project_id, concept, analysis_type)`
- but the live database still enforces uniqueness globally on `(concept, analysis_type)`

That mismatch causes the exact observed live failure:

- a fresh project launches logical successfully
- analyzer-v2 completes and produces a valid translated artifact
- the-critic attempts to insert a new row
- the write collides with an earlier project’s row for the same `(concept, analysis_type)`
- the host job fails
- readback remains `404`

So the next honest tranche is:

1. align the `concept_analyses` schema and runtime semantics to project scope
2. redeploy the-critic with the migration
3. rerun fresh logical proof on a brand-new project
4. rerun scrutiny on that fresh logical result

## What Is Already True

### 1. analyzer-v2 logical execution is not the current blocker

The current live specimen proves:

- analyzer-v2 job `job-plan-936b5b61e93f` completed
- exact translated artifact lookup returns a valid logical artifact
- `contract_validation_status = "passed"`

So the current tranche should not reopen analyzer-v2 execution-stall investigation by default.

### 2. The host persistence correctness patch already improved behavior

The deployed the-critic no longer silently reports `completed` when concept-analysis persistence fails.

That means the new live failure is explicit and more precise:

- host persistence failed honestly
- the job is marked `failed`

This is a real improvement, but it did not close the underlying schema seam.

### 3. The failure is systemic across fresh projects

The reports show the same pattern across multiple post-cutover logical specimens:

- older project with the same concept can persist
- later fresh project with the same concept and analysis type fails

This points to a schema-wide multi-project uniqueness problem, not a specimen-specific glitch.

## Scope Summary

Implement one narrow schema-alignment tranche:

1. make `concept_analyses` uniqueness project-aware
2. align ORM metadata and any helper expectations with that project-aware uniqueness
3. ensure the deployment runs the migration on Render
4. rerun fresh logical proof on a clean new project
5. rerun fresh scrutiny on that new logical result

This is a host persistence/schema tranche, not an analyzer-v2 executor tranche.

## Key Decisions To Freeze

### 1. Do not reopen analyzer-v2 execution first

Treat analyzer-v2 logical execution as good enough pending only regression checks after the host schema fix.

Only reopen analyzer-v2 execution investigation if logical completion fails again after the host schema fix is live.

### 2. Fix the schema the right way: project-scoped uniqueness

The preferred correction is:

- uniqueness on `(project_id, concept, analysis_type)`

not:

- preserving the old global uniqueness and weakening runtime semantics to match it

The runtime is already project-scoped almost everywhere else.
The schema should catch up to that reality.

### 3. Keep the tranche bounded

Do not widen into:

- analyzer-mgmt work
- translated artifact authority redesign
- new concept submodes
- broader cache cleanup
- Close Read UI changes

### 4. Fresh proof must use a brand-new project

Do not certify closure on the duplicate-document April 7 proof project.

Use a final clean project with:

- one subject document
- one response document
- no duplicate uploads

### 5. Preserve the broader corridor

This tranche is still subordinate to the April 6 corridor:

1. runtime authority
2. translated artifact authority
3. thinner host

The schema fix is a bounded prerequisite to continue that corridor honestly.

## Implementation Sequence

### Phase 1: Align schema, ORM, and runtime assumptions

Implement the host-side correction in `the-critic`:

- add an Alembic migration that drops the old unique constraint on `(concept, analysis_type)`
- add a new unique constraint on `(project_id, concept, analysis_type)`
- update ORM metadata in `models_db.py` so the code-level schema matches the migrated live schema
- preserve or improve indexing for project-scoped readback

### Phase 2: Deploy and verify migration behavior

Because `render.yaml` already runs `alembic upgrade head`, deployment should apply the new migration on Render.

Verify live that:

- the migration ran
- fresh concept-analysis writes no longer collide across projects

### Phase 3: Rerun fresh logical proof

Create one brand-new project and upload one clean subject doc and one clean response doc.

Record:

- critic logical job id
- analyzer-v2 logical job id

Require:

- analyzer-v2 job `completed`
- the-critic job `completed`
- `GET /api/concept/analyses/:concept` returns the fresh logical result
- persisted logical result includes `_analysis_provenance.execution_owner == "analyzer-v2"`

### Phase 4: Rerun fresh scrutiny proof

Only after fresh logical readback is real:

- launch one fresh scrutiny job
- verify scrutiny readback on the same clean project

If scrutiny still fails after logical persistence is closed, scope one final tiny scrutiny-specific closure slice.

## Public Interfaces / Behavioral Expectations

No new public routes are required.

The behavioral change is:

- concept analyses should be able to persist independently per project for the same concept and analysis type

That is already the runtime’s intended semantic model.

## Test Plan

### 1. Focused local regression tests

Add or update tests proving:

- two different projects can persist the same `(concept, analysis_type)` without conflict
- same project still upserts cleanly on repeated writes
- fresh logical readback remains project-scoped

### 2. Migration correctness

Verify locally or in staging that:

- old constraint is removed
- new project-scoped unique constraint exists
- repeated writes behave as expected

### 3. Fresh hosted proof

On a final clean project:

- launch logical
- confirm analyzer-v2 completion
- confirm the-critic completion
- confirm logical readback
- launch scrutiny
- confirm scrutiny readback

## Out Of Scope

This tranche should not include:

- analyzer-v2 workflow or chain redesign
- analyzer-mgmt UI work
- broader translated artifact authority movement
- inferential changes unless a shared host schema seam unexpectedly affects them
- Close Read UI work

## Roadmap Implication

The corrected near-term corridor is:

1. runtime authority: materially established
2. host persistence correctness: partially established
3. project-scoped persistence schema alignment: immediate blocker
4. then fresh logical + scrutiny closure proof
5. then resume the broader translated-artifact-authority corridor

So the next serious move is:

- **fix the-critic concept-analysis persistence schema to be project-aware**

Only after that should the program revisit anything upstream.
