# Review: Close Read Concept-Analysis analyzer-v2 Runtime Authority And analyzer-mgmt Visibility Scope

Reviewer: Claude Opus 4.6
Date: 2026-04-06
Memo Under Review: `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_runtime_authority_and_analyzer_mgmt_visibility_scope.md`

---

## Context Check

Confirmed read of every required document:

| # | Document | Read? |
|---|----------|-------|
| 1 | `MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md` | Yes |
| 2 | `MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md` | Yes |
| 3 | `MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md` | Yes |
| 4 | `MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md` | Yes |
| 5 | `MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md` | Yes |
| 6 | `MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md` | Yes |
| 7 | `MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` | Yes |
| 8 | `MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md` | Yes |
| 9 | `MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md` | Yes |
| 10 | `MEMO_2026-04-01_close_read_direction_dictation_reference.md` | Yes |
| 11 | `MEMO_2026-04-01_close_read_direction_change_and_implications.md` | Yes |
| 12 | `DYNAMIC_BESPOKE_APPS_VISION.md` | Yes |

Code files inspected:

| # | File | Inspected? |
|---|------|-----------|
| 1 | `the-critic/api/server.py` | Yes (grep for concept-analysis seams; file is 926KB) |
| 2 | `the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py` | Yes (full) |
| 3 | `analyzer-v2/src/engines/definitions/inferential_commitment_mapper.json` | Yes (full) |
| 4 | `analyzer-v2/src/operationalizations/definitions/inferential_commitment_mapper.yaml` | Yes (full) |
| 5 | `analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json` | Yes (full) |
| 6 | `analyzer-v2/src/workflows/definitions/` | Yes (directory listing) |
| 7 | `analyzer-v2/src/transformations/definitions/` | Yes (directory listing) |
| 8 | `analyzer-mgmt/frontend/src/pages/engines/[key].tsx` | Yes (full) |
| 9 | `analyzer-mgmt/frontend/src/pages/workflows/[key].tsx` | Yes (full) |
| 10 | `analyzer-mgmt/frontend/src/pages/implementations/index.tsx` | Yes (full) |
| 11 | `analyzer-mgmt/frontend/src/pages/transformations/[key].tsx` | Yes (full) |
| 12 | `analyzer-mgmt/frontend/src/pages/jobs/[id].tsx` | Yes (full) |
| 13 | `analyzer-mgmt/frontend/src/lib/api.ts` | Yes (full) |
| 14 | `analyzer-v2/src/orchestrator/concept_by_ref.py` | Yes (full, local only) |

Live URLs checked:

| # | URL | Result |
|---|-----|--------|
| 1 | `analyzer-v2.onrender.com/v1/meta/definitions-version` | 200 - 202 engines, 26 chains, 8 workflows |
| 2 | `analyzer-v2.onrender.com/v1/engines` | 200 - 147 engines listed |
| 3 | `analyzer-v2.onrender.com/v1/engines/inferential_commitment_mapper` | 200 - engine EXISTS on Render |
| 4 | `analyzer-v2.onrender.com/v1/chains` | 200 - 26 chains |
| 5 | `analyzer-v2.onrender.com/v1/chains/concept_analysis_12_phase` | 200 - chain EXISTS on Render |
| 6 | `analyzer-v2.onrender.com/v1/operationalizations` | 200 - 18 entries |
| 7 | `analyzer-v2.onrender.com/v1/operationalizations/inferential_commitment_mapper` | 200 - 4 stances, 3 depths |
| 8 | `analyzer-v2.onrender.com/v1/workflows` | 200 - 8 workflows, NONE are concept workflows |
| 9 | `analyzer-v2.onrender.com/v1/transformations` | 200 - 25 templates, NONE are concept host-contract |
| 10 | `analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref` | 404 - endpoint does not exist |
| 11 | `analyzer-mgmt-frontend.onrender.com/engines/inferential_commitment_mapper` | 404 - "Engine not found" |
| 12 | `analyzer-mgmt-frontend.onrender.com/chains/concept_analysis_12_phase` | Partial - "Failed to load chain" |
| 13 | `analyzer-mgmt-frontend.onrender.com/operationalizations/inferential_commitment_mapper` | 200 - SPA shell loaded |
| 14 | `analyzer-mgmt-frontend.onrender.com/workflows` | 200 - page loads |
| 15 | `analyzer-mgmt-frontend.onrender.com/implementations` | 200 - page loads |
| 16 | `analyzer-mgmt-frontend.onrender.com/transformations` | 200 - shows "0 reusable transformation recipes" |

---

## Verdict

**Approve with corrections.**

The strategic direction is right. The specific claims need qualification and the implementation sequence needs an additional pre-phase.

---

## Detailed Assessment

### 1. Does the live Render evidence support the memo's claim that the missing layer is deployment/authority/visibility rather than missing capability primitives?

**Yes, with an important qualifier.**

The memo's foundational claim is correct. The capability bricks ARE deployed on Render:

- `inferential_commitment_mapper` engine: **live** at `/v1/engines/inferential_commitment_mapper` with full schema, extraction focus, and semantic visual intent
- `inferential_commitment_mapper` operationalization: **live** at `/v1/operationalizations/inferential_commitment_mapper` with 4 stances (discovery, confrontation, dialectical, integration) and 3 depth sequences
- `concept_analysis_12_phase` chain: **live** at `/v1/chains/concept_analysis_12_phase` with all 12 constituent engines

What is NOT deployed:

- `/v1/workflows` returns 8 workflows, zero of which are concept workflows (influence: 2, genealogy: 1, decision_support: 3, synthesis: 1, outline: 1)
- `/v1/transformations` returns 25 templates, zero of which are concept host-contract extraction
- `/v1/orchestrator/concept-analysis-by-ref` returns 404

So yes: the missing layer is composition/authority/visibility, not capability invention. The bricks exist. The wiring does not.

**The qualifier:** The memo says "analyzer-mgmt already has the right surfaces" and implies these surfaces work for concept assets. They do not. See Finding #3 below.

### 2. Is it right to insist on staying within existing analyzer-v2 types rather than inventing a new concept-runtime abstraction?

**Yes. This is the correct decision.**

The local code proves the point:

- `concept_inferential_single_concept.json` is a standard workflow definition that references engine `inferential_commitment_mapper`
- `concept_logical_single_concept.json` is a standard workflow definition that references chain `concept_analysis_12_phase`
- `concept_inferential_host_contract_extraction.json` is a standard `llm_extract` transformation template
- `concept_logical_host_contract_extraction.json` is a standard `llm_extract` transformation template
- `concept_by_ref.py` uses standard `WorkflowExecutionPlan`, `PhaseExecutionSpec`, and `TargetWork` types

None of these require a new top-level type. The existing vocabulary (engine + operationalization + chain + workflow + transformation) is sufficient for representing concept-analysis composition. The recomposition scope memo and the family boundary memo both support this conclusion.

The broader roadmap (default families and composable modules, the "brain" direction audit) also confirms that the right strategy is proving the existing types can represent concept-family composition before introducing any new abstractions.

### 3. Does the memo correctly assign authority?

**The authority assignment is correct in principle but the analyzer-mgmt leg is currently broken.**

The three-way authority split is sound:

- **analyzer-v2**: execution, composition, provenance, translated artifacts
- **analyzer-mgmt**: visibility, editability, human operator inspection
- **Critic**: thin launch/poll/fetch/render

However, the live Render evidence reveals a **pre-existing visibility failure** that the memo does not acknowledge:

| Asset | Exists in analyzer-v2 API? | Visible in analyzer-mgmt? |
|-------|---------------------------|--------------------------|
| Engine: `inferential_commitment_mapper` | YES (200) | **NO** (404 "Engine not found") |
| Chain: `concept_analysis_12_phase` | YES (200) | **NO** ("Failed to load chain") |
| Operationalization: `inferential_commitment_mapper` | YES (200) | Shell loads (needs JS hydration to verify) |
| Transformations (all 25) | YES (200) | **NO** ("0 reusable transformation recipes") |

This means:

- analyzer-v2 already serves the concept capability bricks correctly through its API
- analyzer-mgmt already FAILS to display them despite the data being live
- deploying new concept workflows and transformations to analyzer-v2 will not automatically make them visible in analyzer-mgmt if the existing data-fetching pipeline is broken

**Correction required:** The memo must acknowledge that Phase B has a hidden Phase A.5 dependency: fix whatever is causing analyzer-mgmt to fail on assets that already exist in the analyzer-v2 API. Deploying more assets to a backend whose management console already can't render existing assets will not achieve the "visibility law."

### 4. Is the analyzer-mgmt visibility requirement concrete enough?

**It is correctly specified in terms of WHAT should be visible, but incomplete in terms of HOW given the current breakage.**

The memo lists exactly the right pages:

- inferential engine page
- inferential operationalization page
- concept-analysis chain page
- new concept inferential workflow page
- new concept logical workflow page
- new inferential host-contract transformation page
- new logical host-contract transformation page

This is specific and testable. The problem is that the first three pages already fail on live Render despite the underlying data existing. The memo's acceptance criteria ("on Render, the new concept workflows are visible on workflows/implementations pages") cannot be met without first fixing the existing rendering pipeline.

The "Visibility Law" section is the strongest part of the memo. It correctly insists that composition must be legible through engines / passes / stances / depths / chains / transformations rather than disappearing behind host-local glue code. This principle should survive any corrections.

### 5. Does the memo overstate how quickly Critic can be stripped back?

**Yes, moderately.**

Phase C and Phase D as written are reasonable in scope but may understate the effort, based on two observations:

**a) The recomposition code already partially delegates to analyzer-v2:**

`analyzer_v2_recomposition.py` already calls `execute_transformation_sync(template_key, packet)` to produce translated host-contract artifacts. It then validates against Pydantic models (`InferentialAnalysisResult`, `LogicalAnalysisResult`), adds `_analysis_provenance`, and returns the result to the caller. So the "shift translation authority" story (Phase C) is partly underway locally, but the translated artifacts are still materialized inside Critic rather than fetched from analyzer-v2 as persisted artifacts.

**b) The Critic server.py is massive and deeply entangled:**

The `server.py` is ~926KB with in-memory caches (`_CONCEPT_JOBS`, `_CONCEPT_JOB_CANCELLATION`, `_CONCEPT_ANALYSES_CACHE`), DB models (`ConceptAnalysis`), import chains into `analyze_cross_concept`, and background job infrastructure. Phase D ("remove or sharply reduce Critic-local recomposition code") needs more granular scoping about exactly which code paths can be removed vs. which need to stay for host-local concerns (e.g., the DB read models, the cross-corpus concept analysis, the concept extraction cache).

The memo's instinct ("keep only thin launch/retrieval/render seams") is correct, but the path from the current 926KB server to "thin client" is not one tranche of work.

**Recommended correction:** Phase D should be scoped as "reduce Critic to delegating launch + poll + fetch for the admitted submodes (inferential, logical)" with an explicit deferral of cross-corpus concept analysis thinning and legacy concept cache removal to a subsequent tranche.

### 6. Is "translated host-contract artifacts owned by analyzer-v2" the right next architectural move?

**Yes. There is no more-prior seam that needs to be solved first.**

The precedent chain supports this:

1. The family boundary memo correctly admitted inferential and logical as the two concept submodes
2. The family implementation scope correctly identified that analyzer-v2 already has the engine + operationalization + chain primitives
3. The fresh-project runtime scope correctly established that concept analysis runs should operate over registered-corpus document references
4. The recomposition scope correctly identified that the next step was rebasing on analyzer-v2 types rather than inventing new ones

This memo is the logical next step: make the rebased composition the live deployed truth. There is no missing seam between the recomposition scope and this scope.

The one thing to verify: the `concept_by_ref.py` code correctly uses `load_registered_documents_in_order` and the standard `create_job` + `start_execution_thread` path, which means it builds on the fresh-project runtime work. The dependency chain is clean.

### 7. Does the memo stay correctly narrower than the excluded items?

**Yes, with one minor ambiguity.**

The memo explicitly excludes:

| Exclusion | Correctly excluded? |
|-----------|-------------------|
| New concept submodes | Yes - stays within inferential + logical |
| General module-composition work | Yes - operates on existing types only |
| New Close Read UI work | Yes - no UI changes proposed |
| Standalone Close Read host work | Yes - Critic stays as the host |

The minor ambiguity is in the "bounded orchestrator launch seam" (Phase A). The `concept_by_ref.py` code creates a POST endpoint at `/v1/orchestrator/concept-analysis-by-ref`. This is a new API surface, which is fine and correctly scoped, but the memo should be explicit that this route is bounded to the two admitted submodes and does not become a generic concept-analysis gateway.

The code itself IS correctly bounded - `ConceptAnalysisByRefRequest` has `analysis_mode` that accepts "inferential" or "logical", and the workflow key directly maps to the two admitted workflow definitions. This is right.

### 8. Is there any place where the memo confuses local implementation evidence with live deployed authority?

**Yes. This is the memo's most significant weakness.**

The memo opens with "The live deployed Render state already proves the key strategic point" and then lists evidence about what analyzer-v2 and analyzer-mgmt already expose. This is partially correct for the API endpoints but **wrong for analyzer-mgmt visibility**.

Specific confusions:

1. **Memo claim:** "analyzer-mgmt already serves working pages for engines, chains, operationalizations, workflows, implementations, transformations"
   **Reality:** The list/index pages load (workflows, implementations, transformations) but the detail pages for concept-relevant assets fail:
   - `/engines/inferential_commitment_mapper` → 404
   - `/chains/concept_analysis_12_phase` → "Failed to load chain"
   - `/transformations` → shows 0 templates despite 25 existing

2. **Memo claim:** "the specific concept-relevant pages already load for /engines/inferential_commitment_mapper"
   **Reality:** This page returns 404 "Engine not found" on live Render despite the engine existing in the analyzer-v2 API.

3. **All 5 concept composition files are untracked locally:**
   - `src/orchestrator/concept_by_ref.py` → `??` (untracked)
   - `src/workflows/definitions/concept_inferential_single_concept.json` → `??`
   - `src/workflows/definitions/concept_logical_single_concept.json` → `??`
   - `src/transformations/definitions/concept_inferential_host_contract_extraction.json` → `??`
   - `src/transformations/definitions/concept_logical_host_contract_extraction.json` → `??`

   These have never been committed to git, let alone deployed. The memo correctly identifies that these need to be deployed, but phrases it as "the missing layer" when it should acknowledge that even the local code has not reached the committed state yet.

The memo does not deliberately mislead - the distinction between "exists in the API" and "renders in the management console" is subtle. But the acceptance criteria ("on Render, the new concept workflows are visible on workflows/implementations pages") will fail unless the pre-existing analyzer-mgmt rendering issues are fixed first.

---

## Summary of Required Corrections

### Must-fix before implementation

1. **Add Phase A.0: Fix analyzer-mgmt data-fetching for existing concept assets.** The engine detail page, chain detail page, and transformations list page all fail to render data that the analyzer-v2 API correctly serves. Phase B cannot succeed without this.

2. **Acknowledge that all 5 concept composition files are currently untracked.** Phase A should include "commit and deploy" as an explicit step, not assume the code is already in the pipeline.

3. **Correct the claim that analyzer-mgmt "already loads" concept-relevant detail pages.** It does not. The list/index pages load, but the detail pages fail for the two key concept assets.

### Should-fix for precision

4. **Scope Phase D more tightly.** "Thin the Critic" should mean: for the two admitted submodes, Critic delegates launch/poll/fetch to analyzer-v2 and renders the translated artifacts. Cross-corpus concept analysis, extraction caching, and legacy concept DB models should be explicitly deferred.

5. **Clarify that the orchestrator seam is POST-only and bounded to two submodes.** The `concept-analysis-by-ref` endpoint is not a general concept gateway.

6. **Note the engine count discrepancy.** The meta endpoint reports 202 engines on disk but only 147 appear in the list endpoint. This is not blocking but suggests a filtering issue that could affect visibility.

### No change needed

- The strategic direction is correct
- The "no new substrate types" decision is correct
- The authority assignment (analyzer-v2 / analyzer-mgmt / Critic) is correct
- The scope boundaries (no new submodes, no module-composition widening, no UI redesign) are correct
- The sequencing (deploy composition → expose in mgmt → shift authority → thin host) is correct
- The visibility law is the strongest and most important part of the memo

---

## Answers to Explicit Questions

**Does the live Render evidence support the memo's claim that the missing layer is deployment/authority/visibility rather than missing capability primitives?**
Yes. The engines, operationalizations, and chains are live on Render. The missing pieces are exactly workflows, transformations, and the orchestrator seam.

**Is it right to insist on staying within existing analyzer-v2 types rather than inventing a new concept-runtime abstraction?**
Yes. The local code proves all five composition assets fit cleanly into existing types.

**Does the memo correctly assign authority to the three layers?**
Yes in principle. The analyzer-mgmt leg is broken in practice and needs repair before Phase B can succeed.

**Is the analyzer-mgmt visibility requirement concrete enough?**
Yes for what should be visible. Incomplete for how, given the existing rendering failures.

**Does the memo overstate how quickly Critic can be stripped back?**
Moderately. The recomposition code already delegates transformations to analyzer-v2, but the 926KB server.py with its caches, DB models, and cross-corpus infrastructure will not thin cleanly in one pass.

**Is "translated host-contract artifacts owned by analyzer-v2" the right next architectural move?**
Yes. No more-prior seam exists. The dependency chain from family boundary through recomposition to this scope is clean.

**Does the memo stay correctly narrower than the excluded items?**
Yes. No scope drift detected.

**Is there any place where the memo confuses local implementation evidence with live deployed authority?**
Yes. The analyzer-mgmt visibility claims are the most significant confusion - the memo asserts working detail pages for concept assets that actually fail to render on live Render. The 5 composition files being untracked locally is a secondary instance.

---

## Final Recommendation

**Approve with corrections.** The strategic direction, authority model, scope boundaries, and "no new types" decision are all correct. The implementation sequence needs an explicit Phase A.0 (fix analyzer-mgmt rendering for existing concept assets) and Phase D needs tighter scoping. The memo's claims about current analyzer-mgmt visibility must be corrected to match live Render evidence.
