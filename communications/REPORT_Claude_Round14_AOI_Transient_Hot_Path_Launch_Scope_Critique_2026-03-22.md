# Scope Critique: Round 14 / AOI Transient Hot-Path Launch

**Date**: 2026-03-22
**Reviewer**: Claude Opus 4.6 (fresh session, no prior round context)
**Memo under review**: `communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`

**Verdict: Approve after revision** (two issues require memo amendment before implementation)

---

## Findings by Severity

### 1. MEDIUM — The "Otherwise Newest" Handoff Fallback Has No Backend Support

The memo proposes this source selection rule (line 158-160):

> - if the user currently has a saved AOI result selected/restored in the AOI panel, launch transient compose from that saved result
> - otherwise launch from the newest saved AOI result for the current thinker/project

The first arm is sound. The second arm has a gap.

**The-critic's `server.py` source resolution** (`_resolve_source_backed_compose_identity()`, lines ~18621-18628) requires the caller to provide EITHER `source_analysis_id` OR `source_v2_job_id`. It does **not** implement a "discover newest for thinker and use that" fallback. If neither is provided, the handler fails.

This means the "otherwise newest" rule cannot live in the backend — it must be implemented as frontend logic: `AoiV2ThematicPanel` selects the newest from its already-loaded `savedResults` list and passes its `source_analysis_id` to the compose launch. This is achievable (the panel already has `savedResults` state from `useBoundedV2Workspace`), but the memo should acknowledge:

1. the "newest" resolution happens in the browser, not in the backend
2. the affordance should be **disabled** (not quietly erroring) when `savedResults` is empty
3. the panel must guarantee that `savedResults` is loaded before evaluating the fallback

**Required revision**: Amend the handoff rule to make the resolution site explicit. State that the frontend resolves "newest" from its already-loaded saved-results list and passes a concrete `source_analysis_id`, rather than implying the backend discovers the newest result.

### 2. MEDIUM — Round 13 Browser Proof Artifacts Are Still Pending

The round 13 completion memo explicitly states:

> Code is complete but operational proof artifacts are pending

Round 13's own stated proof standard requires saved request/response/screenshot artifacts from a real browser session launching dossier and comparison from an actual saved AOI result. Those artifacts are not yet in the repository.

Round 14 builds directly on top of round 13's source-backed compose. If round 13's browser-level proof has a lurking failure (e.g., the proxy path works in tests but breaks under real CORS/session conditions), round 14's hot-path launch will inherit that failure invisibly.

**Required revision**: The memo should state as a precondition that round 13's browser proof artifacts must be captured and verified before round 14 implementation begins. Alternatively, round 14's proof standard should subsume round 13's pending browser proof (since a successful hot-path launch from the real AOI panel would necessarily prove source-backed compose works end-to-end).

### 3. LOW — LLM Latency Surface Not Addressed

`compose_from_source` calls Claude Sonnet for page planning (via `compose_from_intent`'s planner, lines 475-591 in `compose_from_intent.py`). This introduces 3-10 seconds of LLM latency on the hot path.

The memo describes UX discipline (lines 195-205) but does not mention loading state behavior. A user clicking "Compose dossier" from the AOI panel and waiting 5-10 seconds with no feedback would feel broken.

**Recommendation** (not blocking): The round 14 implementation should include explicit loading/transition UX. The existing `AoiComposeFromIntentPage` already has a `loading` boolean state — the concern is the navigation transition itself. Consider either:
- Navigating immediately and showing a loading state on the transient page (current behavior, acceptable)
- Or showing a brief inline loading indicator before navigation (nicer but not required)

### 4. LOW — Return Path Mechanism Not Specified

The memo says "preserve a clear return path back to the AOI panel" (line 200) but does not specify the mechanism.

The transient compose page is a separate route (`/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker/compose-from-intent`). Browser back-button navigation should work naturally since the user navigated from the AOI panel. But if the compose takes a while and the user refreshes, they lose the back-button history.

**Recommendation** (not blocking): Consider adding an explicit "Back to AOI" link/button on the transient compose page that uses the `projectId` + `thinkerId` to construct the return URL. This is a small UX detail that can be decided during implementation.

---

## Question-by-Question Assessment

### Q1: Is "bounded hot-path launch adoption" the right next contradiction after round 13?

**Yes.** The memo's reasoning is sound.

The program's proof ladder has been:
- Round 11: transient compose works in isolation (backend)
- Round 12: transient compose renders in a real consumer shell (frontend)
- Round 13: source-backed compose works from real saved AOI data (integration)

Each round narrows the gap between "proof sidecar" and "real product." The natural next move is connecting the existing proof surface to the actual user workflow. Draft persistence before adoption would be premature — there's no point making transient pages durable if users can't even reach them from the real AOI flow.

The roadmap vision (`MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`) originally prescribed renderer contracts → consumer consolidation → bounded compose-from-intent. Rounds 11-13 reordered this by pursuing compose-from-intent first. This reordering is tactically defensible (compose-from-intent is narrower and more immediately demonstrable), but the roadmap memo should be updated to reflect the actual execution order. Round 14 continues this reordered trajectory coherently.

### Q2: Is AoiV2ThematicPanel the right launch seam?

**Yes.** This is the correct component.

`AoiV2ThematicPanel` already owns:
- Thinker context (`projectId`, `thinkerId`, `thinkerName` via props)
- Saved-result discovery and selection (via `useBoundedV2Workspace` hook, `savedResults` state)
- Active job tracking and presentation restore
- The canonical AOI v2 user path

Three natural insertion points exist in the current code:
1. **Results header area** (line ~680): alongside Download/Refresh/Clear/Capture buttons — good for "compose from current result"
2. **"Run Again" button area** (line ~534): alongside the execute button — good for an alternative launch path
3. **Saved results list** (line ~773): each saved result could gain a secondary "Compose" action

The most natural seam is (1) — the results header — because it's contextually tied to the currently-loaded presentation, which means the source identity is unambiguous. Option (3) is also valid but introduces per-item actions that increase cognitive load.

The memo correctly identifies `AoiV2ThematicPanel` without prescribing the exact insertion point, leaving implementation flexibility. This is the right level of specificity for a scope memo.

### Q3: Is the saved-result handoff rule sound?

**Mostly sound, with the gap noted in Finding #1.**

The three-tier rule (selected result → newest result → source_analysis_id as key) is correct in intent. The implementation path is clear:

1. **Selected result available**: User already restored a saved result → `savedResults` list has a selected entry → extract its `v2_job_id` or local DB ID → pass as `source_analysis_id`
2. **No selected result**: Take `savedResults[0]` (list is already sorted by recency in `loadSavedResults()`) → same extraction
3. **No saved results at all**: Disable the compose affordance entirely

The handoff payload (`project_id`, `selected_source_thinker_id`, `selected_source_thinker_name`, `source_analysis_id`) aligns with what `composeFromSource()` in `composeFromIntentClient.ts` already accepts.

The memo is right that `source_v2_job_id` should remain a dev/proof-only override, not the normal product path. The product path should use `source_analysis_id` (which the-critic's backend resolves to a `v2_job_id` before proxying to analyzer-v2).

### Q4: Does the memo stay honest about what must remain blocked?

**Yes.** The exclusion list (lines 223-235) is comprehensive and correctly scoped:

- Draft persistence — correct block (lifecycle question unresolved)
- Promoted drafts — correct (depends on persistence)
- Dual-mode AnalysisWorkspacePage — correct (premature)
- Embedding transient inside AoiV2ThematicPanel — correct (lifecycle confusion)
- Default takeover — correct (transient not yet proven at product quality)
- Multi-workflow transient — correct (AOI-only for now)
- Genealogy integration — correct (different workflow entirely)
- Raw source_v2_job_id as main UX — correct (dev override only)
- Analyzer-v2 direct reach into the-critic persistence — correct (boundary violation)

I found no missing exclusions that could cause scope creep.

### Q5: Is the proof standard strong enough?

**Yes, with one strengthening suggestion.**

The six proof criteria (lines 241-247) are well-constructed:

1. Dossier launch from hot path without manual URL — verifies the launch bridge works
2. Comparison launch from hot path without manual URL — verifies both profiles
3. Selected saved result preserved in handoff — verifies context integrity
4. Transient surface on separate route — verifies lifecycle separation
5. Ordinary AOI behavior unchanged — verifies no regression
6. Zero runtime widening of ViewRenderer/V2TabContent/orchestration — verifies boundary discipline

The proof evidence list (lines 249-256) is adequate. The "focused regression covering the hot-path handoff behavior" requirement (line 256) is especially important.

**Strengthening suggestion**: Add a seventh criterion:

> 7. When no saved AOI result exists for the current thinker/project, the compose affordance is visibly disabled or absent rather than launching into a 404/409 error

This addresses the empty-state case more concretely than the general "honest error/empty-state surface" section (lines 207-220).

### Q6: Most important missing failure modes, lifecycle risks, or architecture mismatches?

**Three items worth noting:**

1. **Saved-result identity format mismatch risk**: `AoiV2ThematicPanel` loads saved results from two sources (local GenealogyAnalysisDB + analyzer-v2 discovery). These may have different ID formats. The handoff must ensure that whichever ID type is passed (`source_analysis_id` from local DB, or a v2-native identifier) is correctly handled by the-critic's `_resolve_source_backed_compose_identity()`. The existing code handles both paths, but round 14 should verify this explicitly.

2. **Concurrent state risk**: A user could launch a new AOI v2 analysis run, then while it's executing, click "Compose" from a previously selected saved result. The compose should use the saved result's identity, not the in-flight job's. The panel's state management needs to distinguish between "currently executing job" and "source result for compose." This is likely natural from the existing architecture but should be tested.

3. **Route parameter accumulation**: The transient compose route uses query parameters for context (`selected_source_thinker_id`, `selected_source_thinker_name`, `source_analysis_id`). If `AoiV2ThematicPanel` constructs this URL, it must URL-encode thinker names that contain special characters. This is minor but has caused bugs in similar navigation patterns.

---

## Perspective Documentation Check

I checked for a `Perspectives/` or `perspectives/` folder in both `/home/evgeny/projects/analyzer-v2/` and `/home/evgeny/projects/the-critic/`. **No such folder exists in either repository.** This review is based solely on the referenced memos, code, and documentation.

---

## Assessment Summary

| Aspect | Verdict |
|--------|---------|
| Right next move? | Yes — adoption before persistence is correct |
| Right seam? | Yes — AoiV2ThematicPanel is the canonical surface |
| Handoff rule? | Sound in intent, needs explicit resolution-site amendment |
| Blocked scope? | Comprehensive, no missing exclusions |
| Proof standard? | Strong, one suggested addition |
| Missing risks? | Three minor items, none blocking |

**Overall**: The memo is strategically sound and correctly bounded. The two medium-severity findings (frontend-side "newest" resolution and round 13 pending proof prerequisite) should be addressed in the memo text before implementation begins, but neither changes the fundamental scope or direction.
