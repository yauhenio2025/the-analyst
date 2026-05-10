# Review: Phase 4 Bounded Governance And Evaluation Scope

Date: 2026-03-28
Reviewer: Claude (Opus 4.6, 1M context)
Subject: `communications/MEMO_2026-03-28_phase4_bounded_governance_evaluation_scope.md`

---

## 1. Verdict

The scope direction is **correct and well-bounded**. A frozen two-case evaluation pack with deterministic rubrics and a read-only inspection seam is the right first governance slice. The memo correctly avoids premature LLM scoring, human approval UI, and live-proof re-execution.

However, the memo has one structural gap that must be addressed before implementation: **the two cases have fundamentally different durable-truth locations, and the memo does not name this asymmetry**. Without addressing it, the implementation will either silently invent a normalization layer the scope doesn't authorize, or will produce a harness that only works cleanly for one of the two cases.

The scope should survive review with targeted revisions, not a redesign.

---

## 2. Findings

### 2.1 Evidence asymmetry between the two cases (CRITICAL)

This is the most important finding.

The memo treats both cases as if they share a uniform "durable truth" substrate. They do not.

**Genealogy lifecycle case** — clean, evaluable from operational stores:

| Evidence source | Location | Programmatic access |
|---|---|---|
| Planning decision | `src/orchestrator/planning_decisions/planning-decision-b1600d054991.json` | `load_task_planning_decision()` |
| Compose session | `src/presenter/compose_sessions/compose-session-0877864dcca7.json` | `load_compose_session()` |
| Documentary proof artifacts | `communications/PROOF_phase3_bounded_lifecycle_v1_*.json` | File reads (ad hoc schema) |

All key fields are present in the compose session: `workflow_key`, `consumer_key`, `planning_decision_id`, `source_v2_job_id`, `presentation_hash`, `presentation_content_hash`, `resolver_version`, full `compose_request` and `compose_response`.

**AOI exemplar case** — split, requires different access paths:

| Evidence source | Location | Programmatic access |
|---|---|---|
| Executor job record | `src/executor/executor.db` table `executor_jobs` | SQLite query |
| 36 phase outputs | `src/executor/executor.db` table `phase_outputs` | SQLite query |
| Presentation run record | `src/executor/executor.db` table `presentation_runs` | SQLite query |
| Documentary proof artifacts | `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_*.json/har/png` (15 files) | File reads (ad hoc schema per file) |
| Planning decision | **DOES NOT EXIST in planning_decision_store** | N/A |
| Compose session | **DOES NOT EXIST in compose_session_store** | N/A |

The AOI exemplar (Phase 0) ran through the older AOI-specific path before Phase 1C landed planning-decision persistence. There is no `PersistedTaskPlanningDecision` for `job-744edf255ad5`. The AOI compose path used `compose-from-selection`, not `compose-from-intent` with explicit session saving. So there is no `PersistedComposeSession` for this job.

**Why this matters for the scope**: The memo's rubric includes "route/planning/compose trace integrity" and "saved-truth fidelity." These checks are meaningful for the genealogy case because real structured operational data exists in named stores. For the AOI case, the equivalent truth lives in the executor SQLite database and in the ad hoc documentary proof JSON files in `communications/`. The harness cannot use the same access paths for both.

The memo already says "The rubric can be case-specific internally" and "not force identical raw checks on unlike case types." That is the right instinct. But the scope must go further and name the actual evidence surfaces per case, or the implementation will have to invent this mapping without authorization.

### 2.2 Communications proof artifacts are documentary, not structured governance data

The memo says "evidence should come from the closeout artifact family." The closeout artifact families in `communications/` are ad hoc captures: raw JSON from API responses, HAR session recordings, PNG screenshots, prose memos. Each file has its own implicit schema based on what was captured during the live proof session.

Examples from the AOI case:
- `PROOF_phase0_..._terminal_state_2026-03-27.json`: has `{status, job_id, workflow_key, completed_at}`
- `PROOF_phase0_..._row_pin_2026-03-27.json`: has `{clicked_row_job_id, compose_request, compose_response}`
- `PROOF_phase0_..._requests_2026-03-27.json`: 892KB of raw HTTP request/response captures

A deterministic harness reading these needs to know each file's structure. This is not inherently wrong — the files exist and are real evidence. But the scope should acknowledge that reading communications proof artifacts requires per-artifact schema knowledge, not just a directory scan.

### 2.3 The executor database is a critical evidence surface the memo does not name

The memo lists `planning_decision_store.py` and `compose_session_store.py` as primary code surfaces but never mentions `src/executor/executor.db` or `src/executor/db.py`. For the AOI case, the executor database is the primary source of operational durable truth:

- `executor_jobs` table: job_id, plan_id, status, workflow_key, project_id, created_at, completed_at
- `phase_outputs` table: 36 rows of engine output prose for `job-744edf255ad5`
- `presentation_runs` table: presentation completion status

The harness must be authorized to read from the executor DB for the AOI case. This is not a widening — the DB already exists and already has API read paths. But the scope should name it.

### 2.4 All codebase claims verified as accurate

Every file path and data structure claim in the memo was verified against the actual codebase:

- `src/orchestrator/task_router.py` — exists, 527 lines
- `src/orchestrator/task_planner.py` — exists, functional
- `src/orchestrator/planning_decision_store.py` — exists, 122 lines, stores to `planning_decisions/` directory
- `src/presenter/compose_from_intent.py` — exists, resolver version `compose-from-intent-v2`
- `src/presenter/compose_session_store.py` — exists, 112 lines, stores to `compose_sessions/` directory
- `src/api/routes/orchestrator.py` — has planning-decision retrieval and lowering endpoints
- `src/api/routes/presenter.py` — has compose-session save and fetch endpoints
- No evaluation/governance module exists yet (confirmed)

The compose session for `compose-session-0877864dcca7` is persisted in the operational store with all expected fields including `presentation_hash`, `presentation_content_hash`, and `resolver_version`.

The executor job for `job-744edf255ad5` is confirmed in the executor database with `status=completed`, `workflow_key=anxiety_of_influence_thematic_single_thinker`, 36 phase outputs, and `presentation_runs` status `completed`.

### 2.5 The scope correctly identifies what not to do

The "must not widen" list is well-calibrated:

- No human approval UI
- No publish/share workflow
- No new transient consumer registration
- No live re-execution by default
- No subjective LLM scoring
- No treatment of memos alone as governance objects

These constraints all pass the anti-drift filter from the fixed-direction roadmap. The proposed work moves analytical evaluation upstream into analyzer-v2 and does not add consumer-owned intelligence. Good.

### 2.6 The frozen pack concept is sound

Two materially different cases with one shared report shape is the right first pack size. The cases differ in:

- Workflow family (AOI vs. genealogy)
- Durable truth substrate (executor DB vs. compose session store)
- Proof era (Phase 0 pre-bridge vs. Phase 3 post-lifecycle)
- Composition path (compose-from-selection vs. compose-from-intent)
- Subject identity type (job_id vs. session_id)

This diversity is a feature, not a problem. A governance rubric that can normalize across these two unlike cases has proven more than a rubric that evaluates two instances of the same thing.

### 2.7 The inspection seam is appropriately narrow

A read-only retrieval endpoint for persisted reports is the correct minimal seam. No Critic review page is needed in this slice. The reports themselves should be self-contained enough that an API consumer (or a future review page) can display them without needing to re-derive the evidence chain.

---

## 3. Open Questions

### 3.1 Where does the harness read AOI evidence from?

The genealogy case can be evaluated entirely from two operational stores (`planning_decision_store` + `compose_session_store`). The AOI case requires either:

- (a) reading the executor database directly for job/phase/presentation truth, plus parsing specific communications proof artifacts for boundary-observance checks, OR
- (b) pre-normalizing the AOI evidence into a case-evidence bundle that the harness reads uniformly

The scope should state which approach it intends.

### 3.2 Are the communications proof artifacts frozen by file path or by content identity?

The memo references `job-744edf255ad5` and `compose-session-0877864dcca7` as canonical subject identities. But the evidence chain passes through specific files in `communications/` that are identified by naming convention, not by content hash. If a file is renamed, moved, or overwritten, the harness would break silently.

Should the evaluation pack include an explicit evidence manifest that pins file paths + content hashes?

### 3.3 What happens when the executor database changes schema?

The executor DB schema has already been extended (e.g., `workflow_key`, `project_id`, `corpus_ref` columns were added after initial creation). If the evaluation harness reads directly from the executor DB, it couples governance to executor schema evolution. Is this acceptable, or should the harness read through the existing API routes (`GET /v1/executor/jobs/{job_id}`, `GET /v1/executor/jobs/{job_id}/results`)?

### 3.4 Does the report shape need to record where each check's evidence came from?

If the report just says "identity integrity: pass" without recording "read from executor_jobs where job_id = X", a future reader cannot verify the check. Should each check carry explicit evidence provenance?

---

## 4. Concrete Revisions

### 4.1 Name the evidence surfaces per case (REQUIRED)

Add a section to the scope that explicitly maps each case to its evidence sources:

**AOI exemplar case evidence:**
- Executor database: `executor_jobs`, `phase_outputs`, `presentation_runs` for `job-744edf255ad5`
- Communications proof artifacts: the 15-file `PROOF_phase0_aoi_execution_backed_after_guard_recalibration_*` family
- Note: no planning_decision_store record exists for this case

**Genealogy lifecycle case evidence:**
- Planning decision store: `planning-decision-b1600d054991.json` (or the specific decision linked to the compose session)
- Compose session store: `compose-session-0877864dcca7.json`
- Communications proof artifacts: the 7-file `PROOF_phase3_bounded_lifecycle_v1_*` family

### 4.2 Add the executor database to the primary code surfaces list (REQUIRED)

The "Primary code and evidence surfaces to scrutinize" section must include:

- `/home/evgeny/projects/analyzer-v2/src/executor/db.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/executor.db`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/executor.py` (for existing read paths)

### 4.3 Require an explicit evidence manifest in the evaluation pack (RECOMMENDED)

The frozen evaluation pack should include one manifest object that lists, for each case:
- canonical subject identity
- evidence source locations (store paths, DB queries, or API routes)
- expected evidence file names with content hashes where applicable

This makes the "fail closed if required truth is missing" check concrete rather than implicit.

### 4.4 Authorize case-specific evidence access in the rubric (RECOMMENDED)

The rubric section says checks should be deterministic and evidence-backed but doesn't authorize different access patterns per case. Add explicit language:

- For the genealogy case: the harness may read from `planning_decision_store` and `compose_session_store` via their existing Python load functions
- For the AOI case: the harness may read from the executor database via existing API routes or direct DB queries, and may parse specific communications proof artifacts by their known schemas

### 4.5 Consider whether the report should embed evidence snapshots or reference them (RECOMMENDED)

Two options:
- (a) The report embeds key evidence values (e.g., `job_status: completed`, `presentation_hash: 7269c27d...`) — self-contained but larger
- (b) The report references evidence locations and a reader must follow the references — smaller but not self-verifying

For a first governance slice, option (a) is stronger: the report should be self-contained and inspectable without chasing references. The scope should state a preference.

### 4.6 No revision needed for the remaining scope (CONFIRMED)

The following aspects of the scope are correct as written and need no revision:

- The choice of deterministic rubrics over LLM scoring
- The choice of file-backed JSON report persistence
- The choice of a read-only inspection seam
- The "must not widen" constraints
- The acceptance bar
- The strategic positioning as Phase 4 / Stage 15
- The decision to evaluate from frozen truth rather than fresh reruns

---

## Summary judgment

The scope is well-designed and strategically correct. The main gap is that it treats the evidence substrate as uniform when it is not. The AOI case and genealogy case have materially different durable-truth locations, and the scope must name this asymmetry so the implementation can handle it honestly rather than papering over it. With the revisions above — especially 4.1 and 4.2 — the scope is ready for implementation planning.
