# Memo: Close Read Project-Scoped Persistence And Fresh Scrutiny Closure Completion

Subtitle: Close the host persistence corridor by proving fresh logical readback and fresh scrutiny persistence on the same clean project, without reopening analyzer-v2 execution or host schema diagnosis

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
Immediate Completion Predecessor:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_and_thin_client_cutover_completion.md`
Immediate Scope Predecessor:
- `communications/MEMO_2026-04-09_close_read_concept_analysis_project_scoped_persistence_schema_alignment_scope.md`
Primary Review Confirmation:
- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Project_Scoped_Persistence_Schema_Alignment_Scope_Critique_2026-04-09.md`
Primary Live Evidence:
- `https://the-critic.onrender.com/api/concept/jobs/concept-1775736818361-44c7b8`
- `https://analyzer-v2.onrender.com/v1/executor/jobs/job-plan-d9ed0f9db367`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?consumer_key=the-critic&external_project_id=cutover-project-scope-20260409-121336-u&concept_name=innovation&analysis_mode=logical&analyzer_v2_job_id=job-plan-d9ed0f9db367`
- `https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical` with header `X-Project-ID: cutover-project-scope-20260409-121336-u`
- `https://the-critic.onrender.com/api/scrutinize/jobs/scrut-1775747770360-df335f`
- `https://the-critic.onrender.com/api/scrutiny/results/innovation` with header `X-Project-ID: cutover-project-scope-20260409-121336-u`
Primary Code Evidence:
- `/tmp/critic-logical-readback-closure/api/models_db.py`
- `/tmp/critic-logical-readback-closure/api/alembic/versions/032_make_concept_analysis_uniqueness_project_scoped.py`
- `/tmp/critic-logical-readback-closure/api/server.py`
- `/tmp/critic-logical-readback-closure/tests/test_concept_live_cutover.py`

## Purpose

Record completion of the bounded host-persistence closure corridor:

- project-scoped concept-analysis uniqueness is aligned live
- fresh logical readback works on a brand-new project
- fresh scrutiny launched from that same logical artifact persisted and read back correctly

This memo closes the persistence/debugging slice and prevents roadmap drift back into already-resolved diagnosis.

## Bottom Line

The host persistence corridor is now closed for the admitted concept seam.

What is now proven live:

- analyzer-v2 completed the fresh logical run
- the-critic completed the matching logical host job
- the exact analyzer-v2 translated artifact validated with `contract_validation_status = "passed"`
- host logical readback returned `200` under the correct `X-Project-ID`
- a fresh `quick` scrutiny run launched from the returned logical argument inventory
- scrutiny persisted and read back correctly on the same project

So the active blocker is no longer:

- concept-analysis schema alignment
- logical host readback closure
- fresh scrutiny persistence closure

## What Was Implemented

### 1. Project-scoped concept-analysis schema alignment

The-critic host persistence was corrected so `concept_analyses` uniqueness now matches runtime semantics:

- unique key on `(project_id, concept, analysis_type)`
- corresponding project-aware index for readback/upsert
- ORM metadata aligned with the live schema
- migration shipped through Render’s `alembic upgrade head` path

### 2. Regression coverage for the schema seam

Focused tests now prove:

- same concept + analysis type can persist across different projects
- same-project rewrites still update the same row
- the host concept-analysis DB write path no longer silently swallows write failure

### 3. Fresh scrutiny proof on the same clean project

Using the clean proof project:

- project: `cutover-project-scope-20260409-121336-u`
- critic logical job: `concept-1775736818361-44c7b8`
- analyzer-v2 logical job: `job-plan-d9ed0f9db367`

The scrutiny request was derived from the first valid logical argument:

- argument id: `ARG-01`
- premise index: `0`
- mode: `quick`

The fresh scrutiny job:

- scrutiny job: `scrut-1775747770360-df335f`

completed successfully and the DB-backed readback returned a matching row for:

- `project_id = cutover-project-scope-20260409-121336-u`
- `concept = innovation`
- `argument_id = ARG-01`
- `premise_index = 0`
- `mode = quick`

## Live Proof Summary

### Logical

- critic job `concept-1775736818361-44c7b8` completed at `2026-04-09T12:44:40.566340`
- analyzer-v2 job `job-plan-d9ed0f9db367` completed at `2026-04-09T12:44:36.781949`
- analyzer-v2 exact result route returned:
  - `lookup_mode = exact_run`
  - `contract_validation_status = "passed"`
- logical readback returned the fresh analyzer-v2-backed result with:
  - `_analysis_provenance.execution_owner = "analyzer-v2"`
  - `_analysis_provenance.workflow_key = "concept_logical_single_concept"`
  - `_analysis_provenance.translation_template_key = "concept_logical_host_contract_extraction"`

### Scrutiny

- scrutiny job `scrut-1775747770360-df335f` completed
- `GET /api/scrutiny/results/innovation` for the same project returned `count = 1`
- the returned row matched the launched scrutiny target and mode

## What This Means Architecturally

The system is now past the host correctness corridor that temporarily interrupted the broader concept-analysis migration.

What is complete:

- live analyzer-v2 runtime authority for admitted concept analysis
- bounded thin-host cutover in the-critic
- fail-closed concept-analysis persistence behavior
- project-scoped concept-analysis persistence semantics
- fresh logical readback closure
- fresh scrutiny closure on the same live project

What is still not architecturally complete:

- translated host-artifact authority still materially lives too much in the-critic
- analyzer-v2 is the execution and validation authority, but not yet the sole translated-artifact read authority for hosts

## Updated Bottom Line

The Close Read concept host-correctness corridor is now closed.

The next serious move is no longer:

- more host persistence debugging
- more logical closure diagnostics
- more scrutiny closure work

The next serious move is again:

- move translated host-artifact authority more fully into analyzer-v2
- expose that boundary cleanly in analyzer-mgmt
- thin the-critic further into a read-through host
