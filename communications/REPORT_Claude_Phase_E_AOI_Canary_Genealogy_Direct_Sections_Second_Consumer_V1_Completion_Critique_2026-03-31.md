# Critique Report: Phase E AOI Canary Genealogy Direct-Sections Second-Consumer V1 Completion

Date: 2026-03-31
Reviewer: Claude Opus 4.6
Completion Memo Under Review: `communications/MEMO_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion.md`
Prompt: `communications/PROMPT_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion_review_claude.md`

---

## Verdict: Approve with revisions

The completion claim is earned. The code changes, test coverage, proof artifacts, and live closeout all confirm that one bounded non-AOI compose path (`intellectual_genealogy` / `direct_sections`) is now live-proved on the already-live-proved `aoi-canary` second consumer. The boundary framing is honest. The revisions required are factual corrections in the artifact inventory, not strategic redirections.

---

## Strategic Assessment

### Where the memo is strategically right

1. **The bounded claim is correctly scoped.** The memo says exactly what it means: one bounded non-AOI compose path works inside the existing AOI-branded second-consumer shell. It does not overreach to claim broad host-neutral generality, generic consumer architecture, or de-AOI-ification. This is honest documentation.

2. **This is real Phase E progress.** Before this slice, the second consumer had only been proved on AOI-local transient surfaces (source selection, source profile dossier, source profile comparison). The fact that the same `aoi-canary` shell can now accept a `card_grid`-rooted genealogy page without semantic reconstruction is a genuine new signal about the analyzer-owned substrate's composability. The varied variable is no longer "which AOI preset?" but "which workflow family?" This is the right direction.

3. **The render-path generalization is appropriately thin.** The canary's `App.tsx` now renders:
   - `tab` roots through `TabShell`
   - non-`tab` roots directly through `RendererHost`

   This is exactly the level of generalization the distilled strategic roadmap demands: no invented AOI wrapper, no semantic reconstruction, no planner/lowering fetches in the canary. The host renders what the analyzer serves.

4. **The case-aware validator is a real improvement over globally looser validation.** The `validateTransientProofSurface()` function validates against each fixture's own `expected_root_renderer` and `expected_raw_json_view_keys`. AOI proof cases still require `tab` root + their pinned raw-json leaf sets. The direct-sections case requires `card_grid` root + empty raw-json set. This is not validation relaxation; it is case-aware precision. The memo's framing here is accurate.

5. **Alignment with anti-drift rules is correct.** Per the fixed-direction roadmap:
   - Rule 2 (current-app work must unblock proof or codify host contracts): This slice proves a host contract seam (non-tab root rendering) and tests a broader compose admission.
   - Rule 3 (prefer upstream fixes): The primary change is analyzer-side consumer admission broadening.
   - Rule 6 (upstream AOI accretion is still drift if it deepens coupling): This change broadens *beyond* AOI, not deeper into it.

### Where the memo is overstated

1. **The artifact inventory lists a `.md` closeout file that does not exist.** The memo claims four live closeout artifacts:

   ```
   - communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.md
   - communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.json
   - communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.har
   - communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.png
   ```

   Only three exist (`.json`, `.har`, `.png`). The `.md` file is absent on disk. This is a factual error that must be corrected: either produce the `.md` file or remove the reference.

2. **The style-token request failure is undisclosed.** The live closeout JSON records one `allowed_non_analytical_requests` entry:

   ```json
   {
     "method": "GET",
     "url": "http://localhost:8001/v1/styles/tokens/explanatory_narrative",
     "status": -1
   }
   ```

   `status: -1` means the request failed (connection refused: the canary tried port 8001 but the analyzer was on 8011). The memo states that `forbidden_analytical_requests_observed = []`, which is correct, and `allowed_non_analytical_requests` are "disclosed honestly," but does not mention that the one allowed request actually failed. This is non-blocking (the canary gracefully degrades without style tokens), but for documentary honesty the memo should acknowledge the failed non-analytical request explicitly rather than leaving the reader to discover it in the JSON.

### Where the memo is too timid

1. **The memo does not name what this proves about render-path generalization.** The fact that the canary now has a `tab`/non-`tab` rendering branch is a modest but real architectural capability. The memo frames this as a thin implementation detail. Strategically, it means the canary host layer is no longer structurally locked to one root renderer type. This is worth saying explicitly, because future non-AOI proof targets (if any) will inherit this capability without additional host changes. The memo should acknowledge this as a small but durable gain.

2. **The test coverage for fail-closed rejection of unsupported consumer/workflow combinations could be stronger.** The scope recommendation memo called for tests that prove "unsupported combinations still fail closed." The analyzer side has `test_compose_from_intent_rejects_unknown_workflow`, but there is no explicit test for a known consumer (like `aoi-canary`) being rejected on an unsupported workflow (something other than AOI or `intellectual_genealogy`). The `_SUPPORTED_HANDOFF_KINDS` and `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` gates would catch this at runtime, but the scope recommendation's call for explicit fail-closed tests is not fully met. This is minor and does not invalidate the completion claim, but it is worth noting.

### Where the memo is missing implementation-critical caveats

1. **Both repos were in DIRTY state during the live proof capture.** The live closeout JSON records:
   - `analyzer_v2_repo_state: "DIRTY"`
   - `aoi_canary_repo_state: "DIRTY"`

   The proof bundle and fixture are committed, and the dirty state is from unrelated ongoing work (the communications files themselves), so this is not a real integrity concern. But for a completion memo that claims frozen proof, mentioning the dirty repo state and explaining that the relevant code is committed would strengthen documentary authority.

2. **The completion memo should reference the scope recommendation review verdicts.** The memo lists the Claude and Codex scope reviews in its header, but does not reference whether the implementation honored the specific revisions those reviews called for. The Claude scope review (`REPORT_Claude_Phase_E_Non_AOI_Direct_Sections_Second_Consumer_Scope_Recommendation_Critique_2026-03-31.md`) gave "Approve with revisions" and called for explicit fixture type system changes, transient identity generation pattern documentation, and stronger assertion about non-tab root as a definite blocker. Checking these off in the completion memo would close the review loop.

---

## Proof Artifact Verification

### Proof bundle: `PROOF_phase_e_transient_second_consumer_aoi_canary_genealogy_direct_sections_2026-03-31.json`

Verified:
- `consumer_key = "aoi-canary"` -- correct
- `workflow_key = "intellectual_genealogy"` -- correct
- `route_family = "direct_sections"` -- correct
- `planning_decision_id = "planning-decision-5f5b0182f2f9"` -- matches matrix bundle lineage
- `compose_call.endpoint = "/v1/presenter/compose-from-intent"` -- correct route
- `response_json.presentation.resolver_version = "compose-from-intent-v2"` -- correct
- Root view `renderer_type = "card_grid"` -- confirmed non-tab root
- `consumer_adaptation_truth.root_renderer_matches = true` -- expected `card_grid`, observed `card_grid`
- `consumer_adaptation_truth.raw_json_set_matches = true` -- both expected and observed empty
- `view_count = 1` -- single view, no tab wrapper
- Trace stages are coherent: semantic_surface_matching -> hierarchy_planning -> page_plan -> view_generation -> transformation_execution -> consumer_adaptation -> contract_validation (0 issues)

### Live closeout: `PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.json`

Verified:
- `canary_mode = "transient_proof"` -- correct
- `proof_case = "genealogy_direct_sections"` -- correct
- `observed_request_json_equals_pinned_fixture_request = true` -- fixture identity preserved
- `response_status = 200` -- success
- `observed_root_renderer = "card_grid"` -- matches expected
- `raw_json_leaf_keys = []` -- empty as expected
- `forbidden_analytical_requests_observed = []` -- no forbidden upstream calls
- `compose_request_count_in_session = 1` -- single compose call
- Screenshot path and HAR path both reference correct filenames

### Screenshot: `PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.png`

Visually confirmed:
- App title: "Bennavv vs Otto Neurath" (consistent with proof lineage)
- Mode: `transient_proof`
- Consumer: `aoi-canary`
- Route family: `genealogy: direct_sections`
- Workflow: `intellectual_genealogy`
- "Genealogy: direct sections" selector button is active (dark background)
- "Relationship Comparison Map" card_grid renders directly (not inside a tab shell)
- Influence Channels and Key Evidence sub-sections are visible
- Strategy summary matches fixture display metadata
- No error state visible

### Fixture: `aoi-canary/src/fixtures/transient-genealogy-direct-sections.json`

Verified:
- `request_kind = "direct_sections"` -- correct discriminated union arm
- `planning_decision_id = "planning-decision-5f5b0182f2f9"` -- matches lineage
- `proof_bundle_identity` points to the correct proof bundle
- `expected_root_renderer = "card_grid"` -- correct
- `expected_raw_json_view_keys = []` -- empty
- `request.workflow_key = "intellectual_genealogy"` -- correct
- `request.consumer_key = "aoi-canary"` -- correct
- Request body matches the observed request in the live closeout

---

## Test Coverage Verification

### Analyzer-side tests

- `test_aoi_canary_transient_genealogy_direct_sections_proof_preserves_non_aoi_root_truth` (test_aoi_canary_contract.py:221-238): Verifies root renderer is `card_grid`, empty raw-json set, route family and workflow key correctness. **Solid.**
- `test_compose_from_intent_accepts_aoi_canary_for_genealogy_direct_sections` (test_compose_from_intent.py:832-878): End-to-end test verifying `aoi-canary` on `intellectual_genealogy` produces a valid response with correct resolver version and view count. **Solid.**
- `test_compose_from_intent_rejects_unknown_workflow` (test_compose_from_intent.py:827-829): Negative test for unknown workflows. **Present but could be stronger** with consumer-specific rejection tests.

### Canary-side tests

- `transientClient.test.ts`: Tests for `composeFromIntent()` request dispatch (line 284-306), `normalizeTransientPresentation` with planning-decision identity (line 356-369), and comprehensive bounded proof surface validation including root-renderer drift detection for direct-sections (line 424-439). **Solid.**
- `App.test.tsx`: Full integration test switching to the "Genealogy: direct sections" proof case (line 520-585), verifying compose-from-intent is called, correct content renders, and no error states appear. **Solid.**

---

## Required Revisions

These revisions are factual corrections, not strategic redirections.

### 1. Fix the artifact inventory (REQUIRED)

Remove the reference to the non-existent `.md` closeout file:

```
communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.md
```

Or produce the file. The current memo claims four files; only three exist.

### 2. Disclose the failed style-token request (RECOMMENDED)

Add a brief note in the "Honest Boundary" or "Verification" section acknowledging that the one `allowed_non_analytical_requests` entry returned `status: -1` (connection failure to port 8001 for style tokens). Explain that this is non-blocking: the canary gracefully degrades without style tokens, and the proof bar does not require style-token availability.

### 3. Acknowledge repo state during proof capture (MINOR)

Add a sentence noting that both repos were in DIRTY state during live proof capture, with the caveat that the proof-relevant code (compose_from_intent.py changes, fixture, and test files) is committed.

---

## Conclusion

The completion claim is earned. The code changes are minimal and correct. The proof artifacts are mechanically auditable and consistent. The boundary claims are honest and appropriately scoped. The memo does not overreach to claim broad generality.

The strategic significance is real but bounded: the second consumer is no longer proved only on AOI-local transient surfaces, and the canary host now has a thin but durable render-path generalization that does not reconstruct semantics. This is genuine Phase E progress toward the broader host-neutral substrate goal.

After the three revisions above, this completion memo should be accepted as documentary authority for this slice.
