# Review: Stage 13 Tier A / AOI Canary Live Proof Closeout Scope

**Reviewer**: Claude Opus 4.6
**Date**: 2026-03-24
**Memo reviewed**: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`

---

## Verdict: APPROVED

The scope is correctly framed, appropriately bounded, and the right immediate next step. No revision is strictly required before implementation. Three findings below should be noted during execution but do not gate approval.

---

## Findings (ordered by severity)

### Finding 1: Proof fixtures mask a preparation-quality gap (MEDIUM)

**Claim tested**: The live proof will show that a second consumer renders through `result_discovery -> result_manifest -> result_presentation` without rebuilding analytical truth locally.

**What the codebase actually shows**:

Both existing AOI proof jobs (`proof-round5-adaptive-aoi-dossier-final-*` and `proof-round5-adaptive-aoi-comparison-final-*`) have `presentation_runs.status = completed`, but their `stats` column reads `{"proof_fixture": true, "round": 5}`. The real preparation pipeline was never run on them:

- `presentation_cache`: empty for both jobs
- `presentation_artifacts`: empty for both jobs
- `polish_cache`: empty for both jobs

The manifest will report `restore_available: true` and `presentation_status: completed` because the proof fixtures satisfy those checks. The `/v1/results/by-job/{job_id}/presentation` endpoint will assemble a page, but it will be built from raw 1-4KB phase outputs rather than from structured, transformed, polished data.

**Why this matters for the proof**: The rendered result in the canary will be real but degraded. A skeptical reviewer could argue the proof demonstrates route wiring but not meaningful rendering quality. The scope memo is silent on this gap.

**Recommendation**: Either:
- (a) Call `POST /v1/results/by-job/{job_id}/refresh-presentation` on one proof job before the live proof run to get a fully prepared presentation (this requires the analyzer server + LLM key), or
- (b) Acknowledge explicitly in the closeout memo that the proof demonstrates the contract seam and rendering path but uses fixture-backed preparation data, not a fully LLM-prepared presentation

Option (b) is honest and sufficient for Tier A. Option (a) is stronger but adds operational scope.

### Finding 2: `attach-project` may not be needed at all (LOW)

**Claim tested**: The memo's Decision 4 frames `attach-project` as an "allowed data-prep move" that might be required.

**What the codebase actually shows**:

Both AOI proof jobs already have `project_id` attached:
- `proof-round5-adaptive-aoi-dossier-final-1774100000` -> `project_id: round5-proof-dossier-final-1774100000`
- `proof-round5-adaptive-aoi-comparison-final-1774100000` -> `project_id: round5-proof-comparison-final-1774100000`

Discovery will find them immediately. The canary just needs to be configured with the correct `project_id` via `VITE_AOI_PROJECT_ID` or URL `?project_id=round5-proof-dossier-final-1774100000`.

**Why this matters**: This is good news. The scope memo's framing of `attach-project` as a potentially required step is more cautious than necessary. The proof path is simpler than the memo implies. However, the memo's caution here is not wrong -- it's just conservative. No revision needed.

### Finding 3: The canary has an undeclared env var type gap (LOW)

**What the codebase shows**: `VITE_AOI_PROJECT_ID` and `VITE_AOI_WORKFLOW_KEY` are used at runtime in `App.tsx` but are not declared in `vite-env.d.ts`'s `ImportMetaEnv` interface. Only `VITE_ANALYZER_V2_URL`, `VITE_AOI_JOB_ID`, and `VITE_AOI_MODE` are declared.

This works because Vite's default typing allows arbitrary `import.meta.env` access returning `string | undefined`, and the app handles `undefined` correctly (enters `config_missing` state). Type-check passes.

**Why this matters**: It's a minor hygiene issue. If a small compatibility fix is allowed during proof closeout, adding these two declarations to `vite-env.d.ts` would be appropriate. But this is not a blocker.

---

## Assessment of Key Review Questions

### Is this proof closeout rather than another architecture tranche?

**Yes, correctly framed.** Verified against the live codebase:

- `aoi-canary` App.tsx implements a full reducer-driven state machine with 10 explicit states
- `resultsClient.ts` has typed fetches for all three result contract endpoints
- 13 tests pass covering happy path, all major error states, URL vs env priority, manifest gating, and no-fallback behavior
- The analyzer-side `results.py` has all required endpoints wired and functional
- The analyzer canary contract test passes

The code is genuinely landed. The remaining gap is purely evidence capture against live data. This is not architecture work.

### Is discovery-first live proof the correct acceptance seam?

**Yes.** The canary's `getResolvedLiveScope()` resolves `project_id` and `workflow_key` from URL params or env, then calls `discoverResults()` with those parameters. If `project_id` is absent, the app enters `config_missing` without making any network requests. Manual `job_id` is clearly labeled as a debug-only bypass. The proof path matches the acceptance path the scope memo describes.

### Is the proposed live evidence set strong enough to count as Tier A closeout?

**Yes, with the caveat from Finding 1.** The five deliverables (proof data record, saved API evidence, ready-state UI proof, negative-state UI proof, closeout memo) are sufficient. The one gap is that the memo doesn't explicitly acknowledge the proof-fixture preparation quality concern. But this is addressable during execution without scope revision.

### Is one negative-state proof necessary and sufficient?

**Necessary: yes.** Without at least one negative proof, the claim that "live failures are not masked by artifact fallback" rests entirely on test coverage, not live evidence.

**Sufficient: yes, for Tier A.** The scope memo lists four acceptable options. The simplest and most convincing is `config_missing` -- just run the canary in discovery-first mode without setting `project_id`. The app will immediately show the `config_missing` state with no network requests, no fallback, no artifact content. This is trivially reproducible and unambiguous.

A second negative state (e.g., `discovery_empty` with a bogus `project_id`) would strengthen the proof but is not required for Tier A closure.

### Is the `attach-project` framing honest?

**Yes, and more cautious than necessary.** As noted in Finding 2, the proof data already has `project_id` attached. The memo frames `attach-project` as a possible prerequisite while being explicit that it's out-of-band prep rather than product work. That framing is correct and honest.

### Is the memo too narrow (risk of memo closure without real proof)?

**No.** The deliverables require live evidence: actual API responses, actual UI screenshots, actual state transitions. The memo is explicit that "local tests only" is not the acceptance bar. The main risk mitigated here is that the proof fixtures produce a degraded rendering -- but even a degraded rendering proves the contract seam.

### Is the memo too broad (risk of drifting into Tranche 2 AOI exemplar work)?

**No.** The non-goals are clear and comprehensive. The scope explicitly rejects transient compose, task-launch, lifecycle, and exemplar-loop work. The deliverables are evidence artifacts, not code features. The "small compatibility or proof-surface fixes" allowance is correctly bounded.

### Are hidden live-environment prerequisites missing?

Two implicit prerequisites should be acknowledged during execution:

1. **The analyzer server must be running and reachable** from wherever the canary is opened. If testing locally, this means `uvicorn src.api.main:app` on port 8001 (or the deployed Render URL).

2. **The canary needs `project_id` configuration** -- either `VITE_AOI_PROJECT_ID=round5-proof-dossier-final-1774100000` in the environment or `?project_id=round5-proof-dossier-final-1774100000` in the URL. The correct `project_id` to use is one of the two proof jobs. The `workflow_key` defaults to `anxiety_of_influence_thematic_single_thinker` which matches the database.

These are operational details, not scope gaps. They don't require memo revision but should be noted in the closeout evidence.

### Is the roadmap sequencing right?

**Yes.** Close Tier A live proof first, then move to AOI exemplar completion. The reasoning is sound:

- Tier A is code-complete but not documentary-closed
- Moving to Tranche 2 (AOI exemplar) without closing Tier A would leave the program claiming two partial achievements instead of one closed one
- The live proof closeout is small enough (~1-2 hours of evidence capture work) that deferring it risks it being forgotten permanently
- The master roadmap and draft next-stages roadmap both place this step before AOI exemplar work

---

## Open Questions

1. **Should the closeout memo distinguish proof-fixture-backed vs. fully-prepared presentation?** The current proof data will produce a valid but degraded rendering. Tier A closure should be explicit about this rather than silently accepting it as equivalent to a real user-facing presentation. (Recommendation: acknowledge it; don't block on it.)

2. **Should the closeout capture a `refresh-presentation` proof as a bonus?** Running `POST /v1/results/by-job/{job_id}/refresh-presentation` on one proof job would demonstrate the full pipeline. This is out of scope for the closeout but would significantly strengthen the evidence. (Recommendation: optional bonus, not required.)

3. **Should the analyzer canary contract test (`test_aoi_canary_contract.py`) be expanded to test the discovery→manifest→presentation flow, not just renderer mapping?** Currently it only tests that the `aoi-canary` consumer definition supports the correct renderer types. A pipeline integration test would close an analyzer-side coverage gap. (Recommendation: note the gap in the closeout memo for future work, don't block on it.)

---

## Judgment: This is the right immediate next step

The scope memo correctly identifies the remaining gap as evidence capture, not architecture. The code is verified as landed and functional. The proof data exists and is discoverable. The negative-state proof is trivially achievable. The boundaries are tight enough to prevent scope creep but flexible enough to accommodate small compatibility fixes.

The only real risk is declaring Tier A closed based on a fixture-backed proof when the rendering quality is degraded. But Tier A's bounded claim is about the *contract seam* (discovery → manifest → presentation → render), not about the *presentation quality* of the rendered output. As long as the closeout memo is explicit about this distinction, the proof is honest.

**Approved for implementation as written.**

---

## Concrete Revisions (recommended but not required before implementation)

None blocking. Three notes for execution:

1. Record in the closeout memo whether `refresh-presentation` was run before the proof or whether the proof used fixture-backed preparation data.
2. Use `project_id=round5-proof-dossier-final-1774100000` for the primary proof path -- this job has all 3 artifact families ready.
3. If the canary's `vite-env.d.ts` is touched for any reason during proof, add `VITE_AOI_PROJECT_ID` and `VITE_AOI_WORKFLOW_KEY` declarations.
