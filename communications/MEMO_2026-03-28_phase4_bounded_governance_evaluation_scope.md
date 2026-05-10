# Memo: Phase 4 Bounded Governance And Evaluation Scope

Subtitle: First analyzer-owned evaluation/report substrate over the frozen AOI exemplar and genealogy lifecycle cases

Date: 2026-03-28
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_completion.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md`
- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
- `communications/MEMO_2026-03-19_phase4_cross_workflow_workspace_scope.md` as an older superseded workspace line, not the active next step

## Purpose

Define the immediate next bounded slice after Phase 3 closed honestly.

This memo is not a Phase 4 implementation plan.
It is the scoping memo that should decide what the first real governance/evaluation slice is, before code lands.

The next step should not be:

- another lifecycle redesign
- new transient consumer registration
- cross-workflow workspace productization
- human approval UI
- broad publish/share semantics

The next step should be a bounded analyzer-owned governance/evaluation substrate.

## Why Phase 4 is now the right next line

The earlier reasons for deferring governance/evaluation no longer dominate:

- the planner-to-presentation bridge is no longer AOI-only
- one bounded non-AOI transient proof exists outside the AOI page stack
- bounded lifecycle law is now implemented and live-proved
- the program now has two materially different frozen proof cases:
  - the AOI execution-backed exemplar closeout
  - the genealogy transient lifecycle closeout

That means the missing seam is no longer structural first.
It is evaluative and operational:

- there is still no analyzer-owned evaluation report object
- there is still no frozen cross-case evaluation pack
- there is still no shared cross-case governance layer on top of the inspection/report surfaces that already exist

So the next honest step is to build the first bounded governance/evaluation layer on top of the now-proved architecture.

## Current code-backed boundary

### What already exists

The codebase already contains most of the underlying truth needed for bounded governance work:

- analyzer-owned routing and planning truth:
  - `src/orchestrator/task_router.py`
  - `src/orchestrator/task_planner.py`
  - `src/orchestrator/planning_decision_store.py`
- analyzer-owned transient presentation truth:
  - `src/presenter/compose_from_intent.py`
  - `src/presenter/compose_session_store.py`
  - `src/api/routes/presenter.py`
- analyzer-owned read-only inspection seams that already normalize part of the platform truth:
  - `src/analysis_products/result_contract.py`
  - `src/analysis_products/source_backed_readiness.py`
  - `src/api/routes/results.py`
  - `src/api/routes/presenter.py`
  - `src/api/routes/orchestrator.py`
- executor-backed durable truth for older bounded cases:
  - `src/executor/db.py`
  - executor read surfaces via `src/api/routes/executor.py`
  - `src/api/routes/executor.py`
- durable closeout artifacts for two important bounded cases:
  - AOI exemplar closeout artifacts from March 27
  - genealogy lifecycle closeout artifacts from March 28
- trace-bearing objects already embedded in platform truth:
  - routing decisions
  - planning decisions
  - planning snapshots
  - transient compose traces
  - compose-session saved truth

### What does not yet exist

The codebase still lacks a first-class governance/evaluation layer:

- no `evaluation_report` object
- no analyzer-owned persistent evaluation-report store
- no frozen evaluation-pack contract
- no bounded harness that turns existing platform truth into auditable evaluation reports
- no read-only report retrieval seam
- no normalized case verdicts over the frozen AOI and genealogy proofs

Important asymmetry the first slice must name explicitly:

- the genealogy lifecycle case is cleanly evaluable from `planning_decision_store` plus `compose_session_store`, with proof artifacts as supporting evidence
- the AOI exemplar case is not
  - its durable truth is split across the executor persistence layer, typed results/readiness/manifest surfaces, and the frozen Phase 0 / Stage 5 proof artifacts
  - it has no matching `PersistedTaskPlanningDecision`
  - it has no matching `PersistedComposeSession`

So the first governance slice must be authorized to evaluate unlike cases through different evidence access paths while still normalizing into one shared report shape.

## Strategic decision

The first Phase 4 slice should be:

- one analyzer-owned evaluation-report substrate
- one frozen two-case composite evidence pack
- one deterministic harness that emits persisted reports from existing analyzer-owned truth plus explicit frozen proof artifacts

It should not be:

- a human approval application
- an LLM-graded composition quality system
- a new Critic UI
- another live browser proof campaign

The bounded default should be:

- extend the existing results/readiness/manifest/trace/planning-decision/compose-session substrate rather than replacing it
- evaluate from frozen durable truth and explicit frozen proof artifacts
- fail closed if required truth is missing
- store a thin verdict report analyzer-side as a first-class governance object
- expose a read-only inspection seam

## Scope decision

### In scope

The first Phase 4 slice should land all of the following together.

#### 1. One analyzer-owned evaluation report object and store

Add one bounded persistent report shape, for example `PersistedEvaluationReport`, stored analyzer-side in file-backed JSON parallel to planning decisions and compose sessions.

Required properties:

- analyzer-generated `evaluation_report_id`
- `created_at`
- `evaluation_pack_key`
- `case_key`
- `subject_kind`
- `subject_identity`
- `workflow_key`
- optional `consumer_key`
- frozen input/evidence references
- ordered `checks`
- ordered dimension summaries
- overall verdict

The report is the governance object.
Not the memo.
Not the HAR.
Not the raw session JSON alone.

But it should be a thin verdict layer over existing truth, not a second parallel truth store.
It should summarize and cite the evidence it evaluated.
It should not duplicate full manifests, full traces, full session payloads, or full proof bundles into a new subsystem.

Because one report may mix live API reads with frozen artifact reads, the evidence-mode fields should be per-check, not merely per-report.
Each check should carry:

- `evidence_mode`
- `evidence_observed_at`
- `live_revalidation_performed`

#### 2. One frozen two-case composite evidence pack

The first pack should be deliberately narrow and explicitly cross-case.

It should include:

1. AOI exemplar case

- fixed March 27 execution-backed closeout case
- primary subject identity:
  - `job-744edf255ad5`
- required supporting evidence should include:
  - typed result/readiness/manifest truth for that job
  - executor persistence/read-layer truth for that job and its presentation state
  - the March 27 closeout artifact family
  - the carried-forward Stage 5 AOI rubric and eval-summary artifact family
- note explicitly:
  - this case has no planning-decision snapshot in `planning_decision_store`
  - this case has no compose-session record in `compose_session_store`

2. Genealogy lifecycle case

- fixed March 28 transient lifecycle closeout case
- primary subject identity:
  - `session_id = compose-session-0877864dcca7`
- required supporting evidence should include:
  - saved compose-session truth
  - the planning snapshot referenced by that saved session
  - typed result/readiness/manifest truth for the supporting source job
  - the March 28 lifecycle closeout artifact family
- note explicitly:
  - `planning_decision_id` is provenance for this case, not lifecycle identity

The pack is frozen on purpose.
The goal is governance infrastructure over known-good bounded cases, not fresh live execution by default.

The frozen pack should therefore be modeled as composite evidence packs, not as isolated subject ids.

#### 3. One deterministic bounded rubric

The v1 rubric should be deterministic and evidence-backed.
Do not introduce subjective LLM quality grading in this first slice.

The rubric can be case-specific internally, but it should normalize into one shared report shape.

At minimum, the first slice should cover checks for:

- identity/readiness integrity
- route/planning/compose trace integrity where applicable
- saved-truth fidelity where applicable
- boundary observance:
  - no forbidden path substitutions
  - no fake host-local reconstruction
- lifecycle reopen integrity for the session-based case

The key idea is:

- normalize verdict structure
- not force identical raw checks on unlike case types

The report should stay honest about time and evidence mode:

- retrospective frozen-evidence verdicts are acceptable in v1
- they should be labeled as such
- they should not be misrepresented as fresh live reruns of current head behavior

#### 4. One bounded harness and one inspection seam

There should be one deliberate way to generate the reports and one deliberate way to inspect them.

Recommended bounded shape:

- one analyzer-owned harness command or test-like runner that materializes the frozen reports
- one read-only analyzer retrieval surface for persisted reports
- harness logic should reuse existing analyzer inspection seams where possible:
  - `GET /v1/results/by-job/{job_id}`
  - `GET /v1/results/by-job/{job_id}/source-backed-readiness`
  - `GET /v1/presenter/manifest/{job_id}`
  - `GET /v1/presenter/trace/{job_id}`
  - `GET /v1/orchestrator/planning-decisions/{planning_decision_id}`
  - `GET /v1/presenter/compose-sessions/{session_id}`
  - executor persistence/read-layer access for the AOI exemplar case where no planning/session store object exists

The first slice does not need a Critic review page.
A read-only analyzer retrieval seam is enough if the reports are stable and inspectable.

## Must land

The first Phase 4 slice should be treated as complete only if all of the following are true:

1. persisted evaluation reports exist as analyzer-owned objects
2. the AOI exemplar case and the genealogy lifecycle case can both be evaluated into that same report substrate despite their different evidence locations
3. the reports are generated from existing analyzer-owned truth plus explicit frozen proof artifacts, not from fresh live reruns by default
4. the reports cite concrete evidence references and fixed subject identities
5. the reports fail closed if required truth is missing or inconsistent
6. there is one deliberate report-inspection seam that does not require reading raw files directly

## Must not widen

- do not build human approval UI in this slice
- do not add publish/share workflow
- do not add new transient consumer registration
- do not re-run the March 27 AOI exemplar or the March 28 genealogy lifecycle proof by default
- do not let “evaluation” become hidden new planner or presenter law
- do not use subjective LLM scoring as the first governance substrate
- do not treat memos alone as the governance object
- do not silently invent a fake normalization layer that pretends AOI and genealogy have the same durable-truth locations
- do not revive the older March 19 cross-workflow workspace proof as the active next step

## Primary code and evidence surfaces to scrutinize

The main code/evidence surfaces for this scope are:

- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/source_backed_readiness.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_session_store.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/presenter.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/results.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/executor.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/db.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
- the AOI and genealogy proof artifacts referenced by those two closeout memos

If the scope review finds that the frozen cases cannot be evaluated honestly from durable truth plus saved artifacts, that should be surfaced as the key blocker rather than widening immediately into fresh browser reruns or UI work.

## Acceptance bar

The scope is correct only if the later implementation can honestly deliver:

- one analyzer-owned thin verdict report object
- one frozen two-case composite evidence pack
- one deterministic, inspectable verdict structure
- one read-only inspection seam
- no hidden dependency on fresh live proof reruns

If review shows that truthful governance requires a different first slice, that should be stated explicitly.
But the default should be:

- governance as analyzer-owned evaluation reports over frozen bounded cases

not:

- governance as more product UI or more live-proof repetition

## Next-step intent

If this scope survives review, the next artifact should be a concrete Phase 4 implementation plan for:

- bounded analyzer-owned evaluation reports
- one frozen AOI-plus-genealogy evaluation pack
- one read-only inspection seam

That would be the first real Stage 15 / Phase 4 code slice.
