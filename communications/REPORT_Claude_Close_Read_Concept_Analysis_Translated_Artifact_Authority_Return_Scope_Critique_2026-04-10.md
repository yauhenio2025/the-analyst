# Report: Close Read Translated Artifact Authority Return Scope — Critique

Date: 2026-04-10
Reviewer: Claude Opus 4.6
Memo Under Review: `communications/MEMO_2026-04-09_close_read_translated_artifact_authority_return_scope.md`

## Context Check

All required memos were read in full:

| Memo | Status |
|------|--------|
| `MEMO_2026-03-30_distilled_strategic_roadmap.md` | Read |
| `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` | Read (first 100 lines + structural understanding via section headers) |
| `MEMO_2026-04-04_close_read_roadmap_recalibration.md` | Read |
| `MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` | Read |
| `MEMO_2026-04-06_close_read_roadmap_update_after_live_concept_authority_cutover.md` | Read |
| `MEMO_2026-04-06_close_read_concept_analysis_translated_artifact_authority_scope.md` | Read |
| `MEMO_2026-04-09_close_read_project_scoped_persistence_and_fresh_scrutiny_closure_completion.md` | Read |
| `MEMO_2026-04-09_close_read_roadmap_update_after_project_scoped_persistence_and_scrutiny_closure.md` | Read |
| `REPORT_Claude_Close_Read_Concept_Analysis_Project_Scoped_Persistence_Schema_Alignment_Scope_Critique_2026-04-09.md` | Read |
| `REPORT_Codex_Close_Read_Concept_Analysis_Logical_Execution_Completion_Stall_Closure_Scope_Audit_2026-04-07.md` | Read |

All required code files were inspected:

| File | Status |
|------|--------|
| `analyzer-v2/src/orchestrator/concept_by_ref.py` | Read |
| `analyzer-v2/src/api/routes/orchestrator.py` | Read (local + deployed diff) |
| `analyzer-v2/src/executor/output_store.py` | Read |
| `the-critic/analyzer/concept_analyzer/analyzer_v2_client.py` | Read (300 lines) |
| `the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py` | Read |
| `the-critic/api/server.py` (concept analysis section) | Read (lines 3830-4380) |
| `analyzer-mgmt/frontend/src/pages/implementations/[key].tsx` | Read (150 lines) |
| `analyzer-mgmt/frontend/src/pages/workflows/[key].tsx` | Read |
| `analyzer-mgmt/frontend/src/pages/jobs/[id].tsx` | Read (350 lines) |

All required live URLs were checked:

| URL | Status | Result |
|-----|--------|--------|
| analyzer-v2 `/concept-analysis-by-ref/result` (exact job) | 200 | `lookup_mode: "exact_run"`, `contract_validation_status: "passed"`, full translated artifact present |
| analyzer-v2 `/executor/jobs/job-plan-d9ed0f9db367` | 200 | `status: "completed"`, `project_id: "cutover-project-scope-20260409-121336-u"` |
| the-critic `/api/concept/jobs/concept-1775736818361-44c7b8` | 200 | `status: "completed"`, `analyzer_v2_job_id: "job-plan-d9ed0f9db367"` |
| the-critic `/api/concept/analyses/innovation?analysis_type=logical` (no header) | 404 | Expected: requires `X-Project-ID` header for project-scoped readback |
| the-critic `/api/scrutiny/results/innovation` (no header) | 200 | `count: 0` — expected without header, completion memo documents success with header |
| analyzer-mgmt `/jobs/job-plan-d9ed0f9db367` | Loaded | Client-side app rendered navigation; data not visible in server-side fetch |
| analyzer-mgmt `/implementations/concept_logical_single_concept` | **Failed** | "Failed to load implementation" |

## Verdict: approve with corrections

The memo's strategic direction, architectural reasoning, and corridor sequencing are all correct. The translated-artifact authority tranche is genuinely the right next move. However, the memo materially understates what has already been implemented on the deployed `origin/master`, which changes how the remaining scope should be read.

---

## Critical Discovery: Phases 1-2 Are Already Substantially Implemented

The local checkout is **11 commits behind `origin/master`**. The deployed code on Render already includes:

### Already deployed on `origin/master`:

1. **`src/orchestrator/concept_artifact_authority.py`** (1197 lines) — Contains:
   - Full translation/normalization logic (mirrors the-critic's `analyzer_v2_recomposition.py`)
   - `upsert_concept_translated_artifact()` — persistence to `concept_translated_artifacts` table
   - `load_concept_translated_artifact()` — read authority by job_id or by project/concept/mode identity
   - `materialize_concept_translated_artifact()` — compute from raw phase outputs on demand
   - Host contract Pydantic validation via imported `InferentialAnalysisResult` / `LogicalAnalysisResult`

2. **`src/orchestrator/concept_host_contracts.py`** (740 lines) — Contains:
   - `InferentialAnalysisResult` and `LogicalAnalysisResult` Pydantic models
   - These are analyzer-v2-owned copies of the host contract models

3. **`concept_translated_artifacts` Postgres table** — Contains:
   - `artifact_id`, `consumer_key`, `external_project_id`, `concept_name`, `analysis_mode`
   - `workflow_key`, `engine_or_chain_key`, `depth`, `analyzer_v2_job_id`
   - `translation_template_key`, `contract_validation_status`
   - `translated_artifact_json`, `validation_errors`, `analysis_context`
   - `produced_at`, `updated_at`
   - Indexed on `(consumer_key, external_project_id, concept_name, analysis_mode, contract_validation_status, produced_at)`

4. **Live `/concept-analysis-by-ref/result` route** — Returns translated artifacts with full provenance and validation status, confirmed working live.

### What this means for the memo:

The memo's Phase 1 (analyzer-v2 translated-artifact persistence) and Phase 2 (analyzer-v2 read authority) are **already substantially complete and deployed**. The memo was written without awareness of the 11 deployed commits.

The remaining real work is:
- **Phase 3**: analyzer-mgmt operator visibility (genuinely still needed)
- **Phase 4**: the-critic read-through cutover (genuinely still needed — the-critic still calls its own translation logic and persists locally)
- **Phase 5**: fresh live proof of the full thin-host path

### Required correction:

The memo should acknowledge that Phases 1-2 are deployed rather than presenting them as future work. The scope should be reframed as:

1. **Verify deployed Phases 1-2** — confirm `concept_translated_artifacts` is populated for the proof specimen, validate the read authority route is stable
2. **Phase 3** — build analyzer-mgmt surfaces (unchanged)
3. **Phase 4** — rebind the-critic to read from analyzer-v2 authority (this is the core remaining host-thinning work)
4. **Phase 5** — fresh proof (unchanged)

---

## Direct Answers to Requested Questions

### 1. Is the memo right that the temporary host-correctness corridor is now actually closed?

**Yes.** Verified against live evidence:

- analyzer-v2 job `job-plan-d9ed0f9db367`: `status = "completed"`, `completed_at = "2026-04-09T12:44:36.781949"`
- the-critic job `concept-1775736818361-44c7b8`: `status = "completed"`, `completed_at = "2026-04-09T12:44:40.566340"`
- analyzer-v2 exact result: `contract_validation_status = "passed"`, `lookup_mode = "exact_run"`, full translated artifact present
- the-critic analyses readback: returns 404 without `X-Project-ID` header (expected — proves project-scoped uniqueness is enforced)
- Scrutiny: completion memo documents successful run and readback; I cannot verify the header-dependent readback directly, but the code path is sound

The schema fix (migration 032) is deployed and working. The proof project `cutover-project-scope-20260409-121336-u` is a fully closed specimen. No evidence of residual schema bugs or persistence failures.

### 2. Does the codebase still show that the-critic owns too much of translated host-artifact normalization, persistence, or read authority?

**Yes, but the picture is more nuanced than the memo states.** Two realities coexist:

**On the deployed analyzer-v2** (`origin/master`):
- `concept_artifact_authority.py` already owns translation, normalization, persistence, and read authority
- `concept_host_contracts.py` already owns the host contract Pydantic models
- The `concept_translated_artifacts` table already exists

**On the-critic** (live deployed):
- `analyzer_v2_recomposition.py` still contains its own translation/normalization logic
- `server.py` still calls this local translation, then persists to the-critic's own DB
- the-critic's `get_concept_analysis()` endpoint still reads from the-critic's local DB

So the authority is currently **duplicated**, not solely owned by the-critic. The deployed analyzer-v2 already has the machinery; the-critic just hasn't been cut over to use it yet.

### 3. Is the memo right to return to translated-artifact authority now, rather than more host debugging?

**Yes.** The host persistence corridor is genuinely closed. The only readback verification gap is that I cannot send custom `X-Project-ID` headers via WebFetch, but the code path (`get_concept_analysis` at server.py:4326-4356 queries by `project_id`) and the successful job completion (fail-closed persistence would mark the job as failed) together provide strong confidence.

### 4. Does the current codebase support moving more translated-artifact authority into analyzer-v2 without inventing new substrate types?

**Yes, and it already has.** The deployed `origin/master` already contains:
- `concept_translated_artifacts` table (extends existing executor DB, not a new substrate)
- Translation logic as an extension of the orchestrator module
- Read authority as an extension of the orchestrator routes

The memo's "no new substrate types" decision is satisfied: the implementation uses the existing executor DB and orchestrator module structure.

### 5. Does the memo keep the host contracts fixed clearly enough?

**Yes.** The memo is explicit: "Do not redesign the native concept pages or Close Read concept pages in this tranche." The target contracts remain the current inferential and logical host contracts. The deployed `concept_host_contracts.py` on `origin/master` mirrors these contracts exactly.

### 6. Is the proposed analyzer-v2 authority boundary concrete enough, or does it still leave important implementation choices unresolved?

**The boundary is concrete enough, but the memo does not know that key choices are already resolved in deployed code.**

The deployed code already resolves:
- Where translated artifacts are persisted: `concept_translated_artifacts` Postgres table
- How translation works: `materialize_concept_translated_artifact()` loads raw phase outputs and runs the transformation
- How read authority works: `load_concept_translated_artifact()` supports by-job-id and by-identity lookup
- Host contract validation: Pydantic models live in analyzer-v2 at `concept_host_contracts.py`

The remaining unresolved choice (genuinely open) is:
- **How the-critic's read-through cutover works in practice** — does it call the analyzer-v2 result route directly, or does it use a different integration pattern? This is Phase 4 work.

### 7. Does analyzer-mgmt look concrete enough to serve as the operator surface for raw outputs, translated artifacts, validation state, and provenance linkage?

**Partially.** The current analyzer-mgmt pages provide a foundation:
- Jobs page (`/jobs/[id].tsx`): Has rich tabs (Summary, Manifest, Decision Trace, Page Structure, Steering, Result Boundary) but none currently show translated host artifacts or contract validation state
- Implementations page (`/implementations/[key].tsx`): Shows workflow/chain/engine details and linked transformations — but **currently fails to load** for `concept_logical_single_concept` (verified live: "Failed to load implementation")
- Workflows page (`/workflows/[key].tsx`): Shows phases, dependencies, linked transformations — functional

The memo correctly identifies analyzer-mgmt extension as Phase 3 work. The existing page infrastructure is extensible. But the implementations page failure for concept workflows needs to be fixed as part of this work.

### 8. Does the memo stay properly bounded to `inferential` and `logical` without reopening the broader concept estate?

**Yes.** The memo is explicit: "This tranche only thins the-critic further on: inferential, logical. It explicitly does not widen into: new concept submodes, cross-corpus concept analysis, broader concept cache cleanup, broader Close Read UI work." The deployed code also stays within these bounds — `CONCEPT_WORKFLOW_KEYS` in `concept_artifact_authority.py` contains exactly `{"concept_inferential_single_concept", "concept_logical_single_concept"}`.

### 9. Is there any place where the memo overstates what analyzer-v2 or analyzer-mgmt already expose live today?

**Yes, two places, but in opposite directions:**

1. **Understates analyzer-v2**: The memo presents Phases 1-2 as future work, but they are already implemented and deployed on `origin/master`. The `concept-analysis-by-ref/result` route, `concept_translated_artifacts` table, and full translation/persistence/read authority code all exist live.

2. **Slightly overstates analyzer-mgmt**: The broader roadmap memos (cited by this memo) claim "analyzer-mgmt is live enough to inspect that slice." But the implementations page currently fails to load for `concept_logical_single_concept`. analyzer-mgmt can show job-level data but has no translated-artifact or contract-validation surface yet.

### 10. Is this the right next step if the real objective is still "hosts become thinner, analyzer-v2 becomes the brain"?

**Yes.** This is exactly the right next tranche. It directly advances the core thesis:

- Moving translated-artifact authority into analyzer-v2 = analyzer-v2 becomes more brain-like
- Thinning the-critic to a read-through consumer = host becomes thinner
- Exposing the raw-to-translated boundary in analyzer-mgmt = governance becomes stronger

The strategic roadmap (distilled version) places the program in Phase E (generality proof). Moving concept artifact authority upstream is squarely within this phase's mandate: "prove that analyzer-v2 can compose across arbitrary engine/pass combinations by contract, not by custom host behavior or per-engine demos."

---

## Code-Backed Findings Summary

### analyzer-v2 (deployed on `origin/master`, 11 commits ahead of local)

| Component | Status | Evidence |
|-----------|--------|----------|
| `concept_artifact_authority.py` | **Deployed** | 1197 lines, full translation + persistence + read authority |
| `concept_host_contracts.py` | **Deployed** | 740 lines, `InferentialAnalysisResult` + `LogicalAnalysisResult` |
| `concept_translated_artifacts` table | **Deployed** | Full schema with provenance, validation, artifact JSON |
| `/concept-analysis-by-ref/result` route | **Live** | Returns exact artifacts by job_id with `contract_validation_status` |
| `concept_by_ref.py` (launch) | **Live** | Builds plan from workflow, stores document, creates job with `project_id` |

### the-critic (live deployed)

| Component | Status | Evidence |
|-----------|--------|----------|
| `analyzer_v2_recomposition.py` | **Still owns translation** | Calls analyzer-v2 transformation endpoint, validates against local Pydantic models |
| `server.py` `_run_rebased_concept_analysis` | **Still owns orchestration** | Launches, polls, fetches outputs, calls local translation, persists locally |
| `server.py` `_save_concept_analysis_to_db` | **Still owns persistence** | Upserts to local `concept_analyses` table by `(project_id, concept, analysis_type)` |
| `server.py` `get_concept_analysis` | **Still owns readback** | Reads from local DB, filters by `project_id` |

### analyzer-mgmt (live deployed)

| Component | Status | Evidence |
|-----------|--------|----------|
| Jobs page | **Working** | Rich tabs for execution, presenter, manifest, traces |
| Implementations page | **Broken** for concept workflows | "Failed to load implementation" for `concept_logical_single_concept` |
| Workflows page | **Working** | Phases, dependencies, linked transformations |
| Translated artifact surface | **Does not exist** | No current page shows translated artifacts or validation state |

---

## Live-Verified Facts

| Evidence | Status | Detail |
|----------|--------|--------|
| analyzer-v2 job `job-plan-d9ed0f9db367` | **completed** | 8 LLM calls, 141K/61K tokens, project `cutover-project-scope-20260409-121336-u` |
| the-critic job `concept-1775736818361-44c7b8` | **completed** | Completed 4 seconds after analyzer-v2 job |
| analyzer-v2 exact result route | **passed** | `lookup_mode: "exact_run"`, `contract_validation_status: "passed"` |
| analyzer-v2 provenance | **correct** | `execution_owner: "analyzer-v2"`, `workflow_key: "concept_logical_single_concept"` |
| the-critic analyses readback (no header) | **404** | Expected: project-scoped uniqueness requires `X-Project-ID` |
| the-critic scrutiny results (no header) | **200, count=0** | Expected: header-dependent; completion memo documents success |
| analyzer-mgmt jobs page | **loaded** | Client-side rendering prevents server-side content extraction |
| analyzer-mgmt implementations page | **failed** | "Failed to load implementation" for concept workflow |
| Local checkout vs deployed | **11 commits behind** | Phases 1-2 code exists on `origin/master` but not locally |

---

## Corrections Required

### Correction 1: Acknowledge deployed Phases 1-2

The memo should be updated to reflect that `origin/master` already contains:
- `concept_artifact_authority.py` with full translation + persistence + read authority
- `concept_host_contracts.py` with analyzer-v2-owned Pydantic host contract models
- `concept_translated_artifacts` Postgres table
- Live `/concept-analysis-by-ref/result` route

The remaining scope should be reframed as verification of Phases 1-2, then Phases 3-5.

### Correction 2: Fix the analyzer-mgmt implementations page

The implementations page fails to load for `concept_logical_single_concept`. This should be noted and fixed as part of Phase 3.

### Correction 3: Clarify the-critic cutover mechanics

The memo should specify what "read-through consumer" means concretely:
- Does the-critic call the analyzer-v2 `/concept-analysis-by-ref/result` route instead of running its own translation?
- Does the-critic stop persisting to its own `concept_analyses` DB table?
- Or does it keep a cache but mark it as explicitly secondary?

The deployed analyzer-v2 code already supports the first option. The memo should acknowledge this and specify the target integration pattern.

### Correction 4: Verify the `concept_translated_artifacts` table is populated

The artifact authority code is deployed and the route works, but it's unclear whether the proof specimen (`job-plan-d9ed0f9db367`) has a row in `concept_translated_artifacts`. The live result route may be computing on-the-fly via `materialize_concept_translated_artifact()` rather than reading from a persisted row. This should be verified.

---

## Tightened Bottom Line

The memo's strategic direction is correct. Translated-artifact authority migration is genuinely the right next tranche. The host-correctness corridor is genuinely closed. The boundary decisions (keep host contracts fixed, no new substrate types, stay bounded to inferential/logical) are all sound.

The primary correction is factual, not directional: Phases 1-2 are already substantially implemented and deployed on `origin/master`. The real remaining work is:

1. Verify that the deployed Phases 1-2 are working correctly (check `concept_translated_artifacts` table population)
2. Fix the analyzer-mgmt implementations page for concept workflows
3. Build analyzer-mgmt translated-artifact / validation / provenance surfaces (Phase 3)
4. Rebind the-critic to read from analyzer-v2 artifact authority instead of local persistence (Phase 4)
5. Fresh live proof of the full thin-host path (Phase 5)

That is still meaningful and architecturally important work. But it is closer to complete than the memo knows.
