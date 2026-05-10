# Review: Close Read Concept-Analysis Live Authority Deployment And Thin-Client Cutover Scope

Date: 2026-04-06
Reviewer: Claude (Opus 4.6, 1M context)
Memo Under Review: `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_deployment_and_cutover_scope.md`

## Context Check

Confirmed read in full:

- `MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md` -- Strategic audit of "analyzer-v2 is the brain" vs actual codebase reality
- `MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_runtime_authority_and_analyzer_mgmt_visibility_scope.md` -- The parent scope defining runtime authority + analyzer-mgmt visibility for concept analysis
- `MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_local_visibility_and_operator_trail_completion.md` -- The predecessor completion proving local operator-trail coherence
- `MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md` -- Recomposition strategy: rebasing Critic concept runtime onto analyzer-v2 capabilities
- `MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md` -- Fresh-project runtime enablement for concept family
- `MEMO_2026-04-06_close_read_roadmap_update_after_local_analyzer_v2_visibility_slice.md` -- Roadmap update: next move is live authority, not more local work
- `MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` -- Roadmap: default families + later composable modules destination
- `MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md` -- Implementation scope for first concept family cut
- `MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md` -- Product boundary: inferential + logical core, deferred tiers
- `MEMO_2026-04-01_close_read_direction_dictation_reference.md` -- User dictation: Close Read as flagship, follow-up operations, composition layer
- `MEMO_2026-04-01_close_read_direction_change_and_implications.md` -- Strategic implications of dictation: operation families, artifact routing
- `DYNAMIC_BESPOKE_APPS_VISION.md` -- Vision: analyzer-v2 as brain, apps as ephemeral presentations

Code files inspected:

- `src/orchestrator/concept_by_ref.py` -- Bounded concept launch helper
- `src/api/routes/orchestrator.py` -- The `concept-analysis-by-ref` route (line 501)
- `src/workflows/schemas.py` -- `linked_transformation_keys` field on WorkflowDefinition (line 169)
- `src/workflows/registry.py` -- Propagation of linked_transformation_keys into summaries
- `src/workflows/definitions/concept_inferential_single_concept.json`
- `src/workflows/definitions/concept_logical_single_concept.json`
- `src/transformations/definitions/concept_inferential_host_contract_extraction.json`
- `src/transformations/definitions/concept_logical_host_contract_extraction.json`
- `analyzer-mgmt/frontend/src/lib/api.ts`
- `analyzer-mgmt/frontend/src/pages/implementations/[key].tsx`
- `analyzer-mgmt/frontend/src/pages/workflows/[key].tsx`
- `analyzer-mgmt/frontend/src/pages/jobs/[id].tsx`
- `the-critic/api/server.py`
- `the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py`

Live Render URLs checked:

- `https://analyzer-v2.onrender.com/v1/meta/definitions-version`
- `https://analyzer-v2.onrender.com/v1/workflows`
- `https://analyzer-v2.onrender.com/v1/transformations`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref`
- `https://analyzer-mgmt-frontend.onrender.com/implementations`
- `https://analyzer-mgmt-frontend.onrender.com/workflows`
- `https://analyzer-mgmt-frontend.onrender.com/transformations`
- `https://analyzer-mgmt-frontend.onrender.com/engines/inferential_commitment_mapper`
- `https://analyzer-mgmt-frontend.onrender.com/chains/concept_analysis_12_phase`

---

## Verdict: APPROVE WITH CORRECTIONS

The memo is directionally correct, strategically well-placed, and makes the right call that deployment/live authority is now the bottleneck, not more local design. The corrections below are material but do not change the fundamental scope decision.

---

## Detailed Assessment By Question

### 1. Is the memo right that the next gap is deployment/live authority/cutover rather than more local concept-runtime design?

**Yes. This is confirmed by hard evidence.**

The git status of the key concept-runtime files is unambiguous:

| File | Git Status |
|------|-----------|
| `src/orchestrator/concept_by_ref.py` | `??` (untracked, never committed) |
| `src/workflows/definitions/concept_inferential_single_concept.json` | `??` (untracked) |
| `src/workflows/definitions/concept_logical_single_concept.json` | `??` (untracked) |
| `src/transformations/definitions/concept_inferential_host_contract_extraction.json` | `??` (untracked) |
| `src/transformations/definitions/concept_logical_host_contract_extraction.json` | `??` (untracked) |
| `src/workflows/schemas.py` | `M` (modified, uncommitted) |
| `src/workflows/registry.py` | `M` (modified, uncommitted) |
| `src/api/routes/orchestrator.py` | `M` (modified, uncommitted) |

Every single concept-runtime asset is either untracked or uncommitted. The local code exists and is real, but it has zero presence in git, and therefore zero presence on Render. The memo's diagnosis is exactly right.

### 2. Does the codebase support the claim that local prerequisites are in place for a live deployment tranche?

**Yes, with one caveat.**

The local code is substantive and real:

- `concept_by_ref.py` (212 lines) implements a complete by-ref launch flow: document loading, analysis packet composition, plan building, job creation, execution thread start. It is not a stub.
- The two workflow definitions correctly declare `linked_transformation_keys` pointing to their respective host-contract transformation templates.
- The two transformation templates contain detailed LLM extraction schemas matching the exact current Critic host contracts (7-section inferential, 8-section logical including `conditional_web`, `argumentative_weight`, `textual_shifts`).
- `WorkflowDefinition.linked_transformation_keys` is properly defined in `schemas.py` (line 169) and propagated through `WorkflowSummary` (line 229) and `WorkflowRegistry.list_all()`.
- `analyzer_v2_recomposition.py` in the-critic contains real translation functions (`translate_inferential_result`, `translate_logical_result`) that call analyzer-v2 transformations and validate against Pydantic host-contract models.

**Caveat**: The `analyzer_v2_recomposition.py` file lives in the-critic, not in analyzer-v2. Its deployment depends on a the-critic push, which the memo mentions in Phase 4 but does not explicitly call out as a separate deployment dependency. This is a minor sequencing clarification, not a design flaw.

### 3. Does the memo correctly keep the tranche inside existing analyzer-v2 types?

**Yes. Fully confirmed.**

The scope uses only:
- engines (existing `inferential_commitment_mapper`)
- chains (existing `concept_analysis_12_phase`)
- workflows (new `concept_inferential_single_concept`, `concept_logical_single_concept`)
- transformations (new `concept_inferential_host_contract_extraction`, `concept_logical_host_contract_extraction`)
- one bounded orchestrator route (`/v1/orchestrator/concept-analysis-by-ref`)

No new substrate types. No new top-level abstractions. This is exactly the discipline the roadmap requires.

### 4. Is the operator-console law now concrete enough?

**Yes, with one correction needed.**

The local code confirms:

- `implementations/[key].tsx` imports `TransformationTemplate` and is designed to show workflow composition with linked transformations.
- `workflows/[key].tsx` imports `TransformationTemplate` and `EngineChainSpec`, showing chain-aware phase display.
- `jobs/[id].tsx` includes a result-boundary tab that links back to workflow context.
- The `linked_transformation_keys` field flows from definitions through registry through API into the frontend.

**Correction needed**: The analyzer-mgmt frontend URLs all return HTTP 200, but that only proves the SPA shell serves. It does not prove the actual pages render correctly with concept data. The SPA returns the same HTML shell for any route. The memo should acknowledge that Phase 3 ("Validate live analyzer-mgmt visibility") requires actual browser rendering verification, not just HTTP 200 checks. This could be addressed by specifying that Phase 3 validation must include:

- clicking through to a specific concept workflow detail page
- confirming the linked transformation cards render
- confirming the chain composition view renders for the logical workflow

### 5. Does the memo overstate readiness for Critic thinning?

**Slightly. The translation layer is real but the launch/poll/fetch integration layer is not yet explicitly evidenced.**

What exists in the-critic:
- `analyzer_v2_recomposition.py`: real translation functions that call analyzer-v2 transformation endpoints and validate against host-contract Pydantic models
- `analyzer_v2_client.py` (imported but not directly inspected): presumably an HTTP client for analyzer-v2

What the Critic cutover additionally requires but is not yet evidenced as complete:
1. Launch: API endpoint in `server.py` that calls `POST /v1/orchestrator/concept-analysis-by-ref` on analyzer-v2
2. Poll: Polling logic that checks `GET /v1/executor/jobs/{job_id}` on analyzer-v2
3. Fetch: Result retrieval from analyzer-v2 phase outputs
4. Persist: Storing translated results in the-critic's concept-analysis database tables
5. Route integration: Making the existing concept analysis endpoints in server.py use the new analyzer-v2 path instead of the old local analyzer path

The memo's Phase 4 describes these requirements correctly in principle. But "complete the bounded Critic cutover" is a larger implementation surface than the memo's concise phrasing suggests. The memo should be more explicit that Phase 4 is the heaviest implementation phase, not merely a wiring exercise.

**Recommendation**: Add a sub-phase breakdown to Phase 4 that makes the integration work explicit:
- 4a: Add analyzer-v2 concept launch endpoint to the-critic API
- 4b: Add polling/fetch integration
- 4c: Wire translation layer into persistence path
- 4d: Route existing concept API to the new path for inferential/logical

### 6. Does the memo stay properly narrower than the deferred concerns?

**Yes. This is one of the memo's strongest qualities.**

Explicitly excluded and correctly so:
- New concept submodes (assumption, semantic_field, causal, metaphorical): confirmed excluded
- Broader composition-layer work: confirmed excluded
- New Close Read UI work: confirmed excluded
- Standalone Close Read host work: confirmed excluded
- Cross-corpus concept analysis: confirmed excluded
- Legacy concept cache retirement: confirmed excluded

The scope is genuinely bounded to:
- Two admitted submodes: inferential, logical
- One bounded orchestrator route
- Two workflow definitions
- Two transformation definitions
- Deployment + validation + bounded cutover

This is the right level of discipline for a tranche that must prove live authority rather than expand scope.

### 7. Is there any place where the memo still confuses local proof with live deployed authority?

**One minor instance.**

The memo's "What Is Already True Locally" section (lines 63-74) correctly enumerates the local assets. But line 72 says:

> analyzer-mgmt implementation/workflow/jobs visibility consistent with the frozen operator law

This is locally true but could be misread as claiming live consistency. The local visibility/operator-trail completion memo is careful about this distinction, but the deployment scope memo slightly blurs it by listing it as an unqualified assertion. A small clarification ("locally consistent") would prevent drift.

Otherwise the memo is disciplined about the local/live distinction. The "What Is Still False Live" section (lines 79-86) is correctly harsh. The "Hard Stops" section explicitly says local-only proof does not count.

### 8. Does the memo make deployment itself part of scope strongly enough?

**Yes, and this is the memo's decisive strength.**

The deployment requirement is woven through the entire document:

- Phase 1 "Hard stop: untracked local files do not count as deployed authority" (line 157)
- Phase 2 entirely about live Render validation
- Phase 3 entirely about live analyzer-mgmt validation
- Risk #1: "Do not claim completion on local-only proof" (line 253)
- Acceptance criteria explicitly require "On Render" evidence

**One correction**: The memo should be even more explicit about the commit step. The files are not just "not deployed" -- they are not even committed to git. Phase 1 should explicitly say "git add, commit, push" as separate verified steps, because the current state is that these files have never entered version control at all. The memo says "commit, push, and deploy" but doesn't emphasize that these are **untracked** files with no git history, which is a stronger statement than "local-only code."

### 9. Is the live browser-acceptance requirement concrete enough, especially for the logical scrutiny check?

**Not quite concrete enough. Needs tightening.**

Phase 5 (lines 199-207) says:

1. inferential live concept run succeeds
2. logical live concept run succeeds
3. both appear correctly in native concept pages and Close Read
4. one logical scrutiny flow succeeds against translated analyzer-v2-backed logical output

Items 1-3 are clear enough.

Item 4 is architecturally important but operationally underspecified:

- How will the test verify that scrutiny reads "translated analyzer-v2-backed logical output" rather than some old cached local-runtime logical result?
- What constitutes a "successful" scrutiny flow -- does a premise need to be selected, scrutiny generated, and result rendered?
- Should the test verify that the `_analysis_provenance.execution_owner == "analyzer-v2"` field is set on the logical result that scrutiny operates on?

**Recommendation**: Tighten Phase 5 item 4 to include:

- Verify the logical result has `_analysis_provenance.execution_owner == "analyzer-v2"` before scrutiny begins
- Select at least one scrutinizable premise from the translated logical output
- Generate one scrutiny result
- Confirm the scrutiny result is persisted and readable

This makes the scrutiny check falsifiable rather than aspirational.

---

## Additional Findings From Live Render Verification

### Live analyzer-v2 state (checked 2026-04-06)

| Endpoint | Status | Finding |
|----------|--------|---------|
| `/v1/meta/definitions-version` | 200 | `workflow_count: 8`, `engine_count: 202` |
| `/v1/workflows` | 200 | 8 workflows returned. **No concept workflows present.** Listed: anxiety_of_influence_thematic_single_thinker, decider_answer_processing, outline_editor, intellectual_genealogy, lines_of_attack, decider_question_lifecycle, anxiety_of_influence (v2), and one more. |
| `/v1/transformations` | 200 | Multiple templates returned. **No concept host-contract transformations present.** All returned are AOI or chain-related. |
| `/v1/orchestrator/concept-analysis-by-ref` | **404** | Route does not exist on deployed stack. (Expected -- `concept_by_ref.py` is untracked locally.) |

### Live analyzer-mgmt state

All frontend URLs return HTTP 200 (SPA shell). This confirms the SPA deploys and serves, but **does not confirm** that:
- the concept workflows render on the workflows page
- the concept transformations render on the transformations page
- implementation detail pages correctly display linked transformations

This reinforces the correction above: Phase 3 must include actual browser rendering verification.

### Key finding on route naming

The live deployed route is `/v1/orchestrator/analyze-by-ref` (for genealogy, confirmed 405 on GET). The concept route would be `/v1/orchestrator/concept-analysis-by-ref` (confirmed 404 on deployed, exists locally in `orchestrator.py` line 501). These are correctly distinct routes. No naming collision.

---

## Assessment Against Broader Strategic Context

### Alignment with "analyzer-v2 as the brain" direction audit

The March 26 direction audit correctly identified that the program was still mostly AOI/the-critic-specific. This concept-analysis tranche is the first move toward proving that the brain architecture can handle a materially different family (concept analysis vs AOI/genealogy) through the same analyzer-v2 substrate types. That makes it strategically high-value.

### Alignment with Close Read roadmap

The Close Read roadmap (default families + composable modules) requires concept analysis as the third serious default family. This tranche advances that by making the concept family genuinely analyzer-v2-brained rather than Critic-local. The roadmap update memo explicitly says the next step should be live authority, not more local infrastructure. This memo follows that directive exactly.

### Alignment with dictation reference

The user dictation describes a Close Read app where one does "genealogical analysis, logical analysis, Anxiety of Influence" with follow-up operations. The concept family is directly referenced. Making concept analysis analyzer-v2-owned is a prerequisite for the dictation's vision of composable engine families under Close Read.

---

## Required Corrections (for "approve with corrections")

### Correction 1: Acknowledge untracked status explicitly

Phase 1 should explicitly state that the key files (`concept_by_ref.py`, 2 workflow definitions, 2 transformation definitions) are currently **untracked** in git, not merely uncommitted. This is a stronger statement than "local-only" and makes the commit step non-negotiable.

### Correction 2: Add sub-phase breakdown to Phase 4

Phase 4 ("Complete the bounded Critic cutover") is the heaviest implementation phase and currently reads as a simple wiring step. Break it into:

- 4a: Critic API integration (launch/poll/fetch against live analyzer-v2)
- 4b: Translation layer wiring (connect `analyzer_v2_recomposition.py` to persistence)
- 4c: Route cutover (make existing concept API endpoints use analyzer-v2 path for inferential/logical)
- 4d: Verify Critic deployment to Render reflects the cutover

This also makes explicit that the-critic needs its own deployment push, which is a separate dependency.

### Correction 3: Tighten Phase 5 scrutiny check

Phase 5 item 4 needs:

- Explicit provenance verification (`_analysis_provenance.execution_owner == "analyzer-v2"`)
- At least one premise selection + scrutiny generation + result readback
- Falsifiable criterion for what "succeeds against translated output" means

### Correction 4: Specify analyzer-mgmt browser rendering verification

Phase 3 should specify that "pages load" means actual data rendering, not HTTP 200 from the SPA shell. The specific verification must include clicking through to concept asset detail pages and confirming linked transformations render.

### Correction 5: Clarify that analyzer-mgmt SPA 200 is not proof

The memo's predecessor scope memo explicitly checked analyzer-mgmt URLs and found them returning 200. That is necessary but not sufficient. The deployment scope should acknowledge this distinction to avoid false-positive Phase 3 completion claims.

---

## Summary

The memo correctly identifies the decisive next gap: local concept-runtime assets must become live deployed authority before the architecture claim is honest. The codebase confirms that the local prerequisites are genuine code, not stubs. The live Render stack confirms the gap is real. The scope discipline is strong -- no new substrate types, no scope creep into deferred families or broader composition work. The five corrections above are material but bounded, and they strengthen the tranche rather than changing its direction.

This is the right next operational tranche after the local visibility/operator-trail completion.
