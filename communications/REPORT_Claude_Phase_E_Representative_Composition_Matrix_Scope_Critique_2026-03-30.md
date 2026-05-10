# Report: Claude Critique Of Phase E Representative Composition Matrix Scope

Date: 2026-03-30
Reviewer: Claude (Opus 4.6)
Reviewed Document: `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_scope.md`
Program: Dynamic Bespoke Apps Platformization

---

## Verdict: Approve

This is a clean, well-bounded first Phase E slice. The memo is strategically honest, accurately grounded in the codebase, and avoids the Phase D habits it claims to leave behind. The three-case matrix is the right representative matrix over the live substrate.

---

## What The Memo Gets Right

### 1. The strategic pivot is genuine

The memo correctly identifies that the Phase D question (is governance artifact-identity-coupled to one proof lineage?) has been answered, and that the Phase E question (can analyzer-v2 compose across handoff families without per-app intelligence?) is a fundamentally different kind of question. This is not a relabeled governance memo.

The decision to vary composition/handoff family while holding consumer fixed is exactly right. Consumer generality and composition generality are orthogonal claims; testing both simultaneously would produce a proof that proves neither cleanly.

### 2. The three cases are materially distinct

The codebase confirms that the three proposed cases exercise genuinely different code paths:

- **AOI `source_profile` via `compose-from-source`**: enters through `compose_from_source()` → calls `build_source_composition_bridge()` → lowers through `_compose_handoff_sections()` with `handoff_kind="source_profile"` and `resolver_version="compose-from-source-v3"`. The profile parameter (`dossier`/`comparison`) selects which source family subset to materialize. No planning decision is involved; the request carries `source_v2_job_id` + `profile` directly.

- **AOI `source_selection` via `compose-from-selection`**: enters through `compose_from_selection()` → calls `build_selection_composition_bridge()` → lowers through `_compose_handoff_sections()` with `handoff_kind="source_selection"` and `resolver_version="compose-from-selection-v1"`. The selection payload carries ranked `AoiSelectedSourceInput` entries produced by the planner's LLM-backed source selection step. This path is planner-mediated.

- **Genealogy `direct_sections` via `compose-from-intent`**: enters through `compose_from_intent()` → lowers through `_compose_handoff_sections()` with `handoff_kind="direct_sections"` and `resolver_version="compose-from-intent-v2"`. The genealogy path enters from the analyzer-owned lowering route at `GET /v1/orchestrator/planning-decisions/{id}/compose-from-intent-request`, which converts a persisted `DirectSectionsCompositionHandoffPlan` into a thin `ComposeFromIntentRequest`.

The three cases share the final `_compose_handoff_sections()` orchestration core and the `ComposeFromIntentResponse` output shape, but they enter through different routes, use different request contracts, carry different source identities, and have different planning intermediaries. That is exactly the right kind of matrix for a generality proof.

### 3. The proof law is precise and testable

The five-point law the memo proposes (route-faithful request, `ComposeFromIntentResponse` shape, `view_count == len(generated_view_definitions)`, resolver version agreement, no host-side reconstruction) is directly verifiable against the existing code. These are not vague architectural aspirations — they can be asserted in a test.

### 4. The honest claim boundary is calibrated correctly

The memo is explicit that this proves composition generality across live handoff families — not arbitrary engine composition, not consumer generality, not open-ended workflow-family generality. That matches the actual codebase boundary: `_SUPPORTED_HANDOFF_KINDS` is a hard-coded mapping of two workflow keys to their allowed handoff kinds, and `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` is a frozenset containing exactly `"the-critic"`.

### 5. The out-of-scope list is strategically sound

Excluding new consumer surfaces, new workflow families, arbitrary engine/pass graph search, governance extension, and generic plugin architecture is the right set of exclusions. Each of these would pull the slice into either Phase D habits or premature Phase F productization.

---

## Concrete Findings

### Finding 1: The AOI `source_selection` four-family evolution-ready path is confirmed in code

The memo specifies that case 2 should "use the evolution-ready four-family selection path, not a narrowed two-family shortcut." This is accurate to the codebase. `ComposeFromSelectionRequest.selection` accepts a list of `AoiSelectedSourceInput` entries, and the task planner's `_AOI_PROFILE_FAMILY_SETS` maps profiles to source family subsets across four source families: `thematic_synthesis`, `engagement_mapping`, `sin_findings`, `thematic_report`. The planner's LLM selection step can select across all four families, and the selection payload preserves the full ranked selection including rejected alternatives.

This is the right thing to require for the proof because it exercises the most interesting composition boundary: the planner chooses the source families, not a hardcoded profile shortcut.

### Finding 2: The genealogy lowering route is correctly identified

The memo says genealogy enters through "persisted planning decision → analyzer-owned lowering → `POST /v1/presenter/compose-from-intent`." This matches the live code: `GET /v1/orchestrator/planning-decisions/{id}/compose-from-intent-request` is a real route (`src/api/routes/orchestrator.py:365`) that takes a `planning_decision_id` and `consumer_key`, loads the persisted snapshot, and returns a thin `ComposeFromIntentRequest`. The memo correctly notes that `planning_decision_id` is not part of the public compose-from-intent request contract — it is bundle-level capture metadata, not request truth.

### Finding 3: The response shape convergence claim is accurate

All three paths do converge on `ComposeFromIntentResponse`, which wraps `TransientIntentPagePresentation` + `list[ViewDefinition]` + `ComposeFromIntentTrace`. The route definitions in `src/api/routes/presenter.py` confirm this: all three endpoints (`compose-from-intent`, `compose-from-source`, `compose-from-selection`) declare `response_model=ComposeFromIntentResponse`.

### Finding 4: One minor naming precision issue

The memo says the three routes are "compose-from-source", "compose-from-selection", and "compose-from-intent". Technically, the genealogy path's public entry point is `POST /v1/presenter/compose-from-intent`, but its *analyzer-owned* entry point is the lowering route at `GET /v1/orchestrator/planning-decisions/{id}/compose-from-intent-request`. The matrix proof should be clear about whether it is testing the public compose-from-intent endpoint alone (which any caller could hit) or the full analyzer-owned lowering chain (which includes persisted planning truth). The memo's case 3 description lists the lowering chain, which is the right choice for a Phase E proof — but the proof record should capture both the lowering step and the compose step as separate evidence surfaces, not just the final compose request/response.

### Finding 5: The resolver_version strings are stable and verified

The memo claims three resolver versions: `compose-from-source-v3`, `compose-from-selection-v1`, `compose-from-intent-v2`. These are confirmed as string constants in `src/presenter/compose_from_intent.py:57-59`. They are stable and test-anchored in `tests/test_compose_from_intent.py`.

---

## Strategic Assessment

### Question 1: Is this the right first Phase E slice, or still drifting inside Phase D habits?

**This is genuinely Phase E.** The proof is about composition generality, not governance. It does not add new evaluator families, governance chains, or review/disposition flows. The proof seam is a matrix test over live composition routes, not a retrospective evaluation of frozen artifacts. The memo explicitly forbids turning the proof into "a new governance family" or "a new evaluator architecture."

The most telling indicator is the variable: the matrix varies the handoff family, not the governance chain. Phase D varied the proof campaign; Phase E varies the composition path. That is the correct dimension shift.

### Question 2: Is the memo honest about what this matrix would and would not prove?

**Yes.** The honest claim boundary is precise: "analyzer-v2 can already compose and render across a small representative matrix of live handoff families without per-app intelligence." The honest non-claims (no arbitrary engine composition, no consumer generality, no open-ended workflow-family generality) are each tied to real codebase constraints. The memo does not overstate.

### Question 3: Are the proposed three composition families the right representative matrix?

**Yes.** These are the only three live handoff kinds in the codebase (`_SUPPORTED_HANDOFF_KINDS` maps exactly `{AOI_WORKFLOW_KEY: {direct_sections, source_profile, source_selection}, GENEALOGY_WORKFLOW_KEY: {direct_sections}}`). The matrix exhausts the currently supported composition surface. It is not cherry-picked — it is the full live substrate.

The three cases are also structurally representative of meaningfully different composition patterns:
- Case 1 (source_profile): no planning decision, direct source identity
- Case 2 (source_selection): planner-mediated, LLM-backed selection
- Case 3 (direct_sections): planning-decision-persisted, analyzer-owned lowering, cross-workflow

That gives a 2×2 coverage of {AOI, genealogy} × {planner-mediated, direct} with the three cases covering three of the four cells (the fourth — genealogy planner-mediated — does not exist in the substrate yet).

### Question 4: Is keeping `consumer_key=the-critic` fixed the right isolation choice?

**Yes.** The codebase has only one registered transient consumer adapter: `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS = frozenset({TRANSIENT_COMPOSE_CONSUMER_KEY})` where `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"`. Attempting to vary the consumer would require inventing new consumer infrastructure, which would conflate consumer expansion with composition generality. Fixing the consumer and varying the handoff family isolates exactly the right variable for the first Phase E question.

### Question 5: Is the memo accurate about the codebase and current route/contract reality?

**Yes, with one minor precision note (Finding 4 above).** The routes, request schemas, response shapes, resolver versions, and handoff kind mappings are all accurately described. The genealogy lowering chain is correctly identified. The four-family evolution-ready AOI selection path is correctly described.

### Question 6: Is there a smaller or cleaner first Phase E step?

**No.** A single-case proof (e.g., only AOI source_profile) would not demonstrate generality — it would be a bounded Phase D-style proof of one composition path. A two-case proof (e.g., AOI source_profile + AOI source_selection) would demonstrate generality within one workflow but not across workflows. The three-case matrix is the minimal set that proves cross-workflow, cross-handoff-kind composition generality over the live substrate.

One could argue for a two-case matrix of {AOI source_selection, genealogy direct_sections} (dropping source_profile as a less interesting variant of source_selection). That would still prove cross-workflow generality. But source_profile is the only non-planner-mediated path, and including it is cheap (same test harness, different fixture), so the three-case matrix is the right call.

---

## Risks

### Risk 1: Test isolation vs. live execution dependency

The memo says the proof seam "may be one dedicated integration-style test file." If the tests mock the LLM layer (view generation, transformation extraction), the proof demonstrates contract agreement but not live end-to-end composition. If the tests require live LLM calls, they become expensive and non-deterministic.

**Recommendation**: The proof should include both: deterministic contract-level tests with mocked LLM calls (for CI), and a one-time live execution captured as frozen proof artifacts under `communications/`. The memo's proof record requirement (section 2) already handles the live execution side.

### Risk 2: The genealogy case may require a live planning decision

For case 3 (genealogy direct_sections), the full lowering chain starts from a persisted planning decision. If no suitable planning decision exists on disk, the proof would need to run the planner first. The memo should clarify whether the proof is expected to execute the planner or rely on existing persisted planning decisions. If the latter, it should name the planning decision explicitly to avoid brittleness.

**Recommendation**: The proof should capture and pin one fresh planning decision as part of the proof campaign, similar to the Phase D cross-campaign approach.

---

## Bottom Line

This memo is strategically correct, codebase-accurate, and properly bounded. The three-case composition matrix is the right first Phase E slice: it is the minimal set that proves cross-handoff, cross-workflow composition generality over the live substrate without inventing new infrastructure or collapsing back into Phase D governance habits.

Approve without revision.
