# Critique: Phase 2 Scope — Consumer Contract / Host Adapter

**Reviewer**: Claude Opus 4.6
**Date**: 2026-03-19
**Primary memo under review**: `MEMO_2026-03-19_phase2_consumer_contract_scope.md`
**Background**: Post-Stage-9 next steps, thin consumer platformization execution brief, implementation plan, Phase 0 / Phase 1A completion memo
**Inspection targets**: `AnalysisWorkspacePage.tsx`, `AoiV2ThematicPanel.tsx`, `GenealogyPage.tsx`, `resultContract.ts`, `presentationFreshness.ts`

---

## Finding 1: The extraction seam is real and strongly confirmed by the code (Severity: Positive / Foundational)

The memo claims the duplicated behaviors include `fetchResultPresentation`, `fetchRunStatus`, `cacheV2Presentation`, `refreshStoredV2Presentation`, local-saved-result restore fallback, upstream restore attempt, and result-state notice logic. This is accurate.

All three surfaces contain near-identical implementations of:

| Behavior | AnalysisWorkspacePage | AoiV2ThematicPanel | GenealogyPage |
|---|---|---|---|
| `fetchResultPresentation` | :458–466 | :285–293 | :701–709 |
| `fetchRunStatus` | :468–476 | :295–303 | :711–719 |
| `cacheV2Presentation` | :478–483 | :305–310 | :721–726 |
| `refreshStoredV2Presentation` | :486–570 (~85 lines) | :312–402 (~90 lines) | :728–813 (~85 lines) |
| `loadLocalSavedResult` / `loadLocalResultDetail` | :572–630 | :404–460 | :816–869 |
| `loadSavedResult` | :632–694 | :462–521 | :889–952 |
| saved-result list merge (local + upstream) | :346–424 | :523–603 | :585–667 |
| active run discovery | :426–456 | :664–713 | :669–699 |
| `toAnalysisJob` / `toGenealogyJob` | :119–149 | :148–179 | ~parallel function |
| `shouldPollJob` | :151–160 | :113–122 | ~parallel function |
| polling effect | ~:730–750 | :643–662 | ~parallel location |

The total duplicated lifecycle code is roughly **250–300 lines per surface**, with the three surfaces collectively carrying **~800 lines** of near-identical bounded-v2 client/restore logic. The extraction seam is not speculative; it is one of the clearest duplication targets I have seen in this codebase.

---

## Finding 2: The `setActiveTab` / presentation-loaded callback is embedded in the extraction target and creates a design friction the memo does not acknowledge (Severity: Medium)

The memo correctly excludes "active-tab state" and "tab default selection" from the extraction scope. However, inside `AoiV2ThematicPanel`, calls like `setActiveTab(getDefaultPresentationTab(presentation))` are embedded within:

- `refreshStoredV2Presentation` (:348, :384)
- `loadLocalSavedResult` (:420, :444)
- `loadSavedResult` (:480)
- `fetchJobStatus` (:618)

These are all in-scope extraction targets. `AnalysisWorkspacePage` does not use `getDefaultPresentationTab` — it uses a different tab selection mechanism (URL-driven `useTabUrl` and `useDeepLink`).

This means the shared contract cannot simply return presentation data and let the caller ignore it. Every caller needs a callback hook — something like `onPresentationLoaded(presentation)` — where each surface wires in its own tab management. The extraction is still feasible, but the memo should acknowledge this boundary explicitly. Without it, the implementor may either:

- accidentally pull tab state into the shared layer (scope drift), or
- produce a shared layer that doesn't call back at the right moments, requiring the caller to re-wrap every lifecycle operation anyway (defeating the purpose).

**Recommendation**: Add one sentence to the "Recommended Shape / Layer 2" section acknowledging that the hook must expose a `onPresentationLoaded` (or equivalent) callback rather than managing tab state directly.

---

## Finding 3: `AoiV2ThematicPanel` has no dedicated tests — regression verification will lack a pre-extraction baseline (Severity: Medium)

The existing test file `AnxietyOfInfluencePages.test.tsx` mocks out `AoiV2ThematicPanel` entirely (line :25–30). There are no dedicated tests for `AoiV2ThematicPanel`'s internal lifecycle logic (restore-first, polling, saved-result merge, refresh).

The memo's acceptance criteria (items 1–4) and verification expectations ("targeted frontend tests for the shared client / host-adapter behavior", "updated page/component tests proving the shared layer is used") are correct. But the implementor should be warned: there is no pre-extraction regression baseline for `AoiV2ThematicPanel`. Writing tests for the shared contract requires simultaneously establishing the first behavioral test coverage for this surface.

This is not a scope problem. It is a risk the implementor should budget for.

**Recommendation**: Note in the memo that AoiV2ThematicPanel currently lacks lifecycle-level test coverage and that this tranche should establish it via the shared contract tests, not as a separate pre-extraction task.

---

## Finding 4: `selected_source_thinker_id` filtering is a real asymmetry between the two adoption targets (Severity: Low-Medium)

`AoiV2ThematicPanel` filters run discovery, result discovery, and saved-result lists by `selected_source_thinker_id`. It has a dedicated `matchesThinker` helper (:137–146) that does not exist in `AnalysisWorkspacePage`.

`AnalysisWorkspacePage` does not filter by thinker at all — its discovery calls do not include `selected_source_thinker_id`.

The shared contract will need to handle `selected_source_thinker_id` as an optional filter parameter. The memo's recommended shape for Layer 2 (`useBoundedV2Workspace`) already lists "bounded run polling support" but does not explicitly mention the thinker-scoping dimension.

This is solvable — it is an optional parameter — but the implementor should know it exists before reaching the second adoption target and discovering it mid-extraction.

**Recommendation**: Mention in the memo that `AoiV2ThematicPanel` requires thinker-scoped discovery and the shared contract must parameterize this.

---

## Finding 5: The `toAnalysisJob` / `toGenealogyJob` conversion function is duplicated but not mentioned in the extraction scope (Severity: Low)

All three surfaces have a `V2RunDetail → local AnalysisJob/GenealogyJob` conversion function (~30 lines each). These are structurally identical — same field mappings, same fallback logic. GenealogyPage names it `toGenealogyJob`; the other two name it `toAnalysisJob`.

The memo lists "response-shape parsing" as a Layer 1 responsibility. The conversion function fits naturally there. But it is not explicitly called out, and the implementor might miss it.

**Recommendation**: No memo change needed — this falls under "response-shape parsing." But the implementor should be aware.

---

## Finding 6: `GenealogyPage` exclusion is correct but the memo could be firmer about why (Severity: Low)

The memo treats `GenealogyPage` as "optional follow-on." The code confirms this is the right call:

- `GenealogyPage` has genealogy-specific saved-result fields (`ideas_analyzed`, `prior_works_scanned`, `tactics_detected`) in its `SavedResult` interface that don't exist in the other surfaces.
- It has a `viewingResult` state and a legacy prose-rendering fallback path (lines :815–870+) that the other surfaces do not have.
- Its `loadLocalResultDetail` function has extra branching for prose-mode injection (`:868+`) not present in the other surfaces.

Including `GenealogyPage` in this tranche would force the implementor to either generalize the saved-result type (premature abstraction) or add genealogy-specific branching to the shared contract (scope creep). The memo's decision to exclude it is sound.

---

## Finding 7: The existing shared utilities (`resultContract.ts`, `presentationFreshness.ts`) are already correctly composed into all three surfaces (Severity: Positive)

All three surfaces import from `resultContract.ts` (`describeResultState`, `needsResultTransitionPolling`, `prefersServerPresentation`, `prefersSnapshotFallback`) and from `presentationFreshness.ts` (`isFreshnessCurrent`). The memo's instruction that the new contract should import and compose these helpers rather than redefine them is not aspirational — it describes how the code already works. The shared contract would be a natural higher-level composition over these existing helpers.

---

## Finding 8: No analyzer-v2 changes appear to be required — the memo's criterion 5 is likely to hold (Severity: Positive)

The duplicated client calls all target existing analyzer-v2 API endpoints:

- `GET /v1/runs/by-job/{job_id}`
- `GET /v1/runs/discovery`
- `GET /v1/results/by-job/{job_id}`
- `GET /v1/results/by-job/{job_id}/presentation`
- `POST /v1/results/by-job/{job_id}/refresh-presentation`
- `GET /v1/results/discovery`

None of these need modification for the extraction. The only Critic-backend-facing call is `cacheV2Presentation`, which routes through `API_BASE` and is workflow-parameterized already. The memo's expectation that no analyzer-v2 changes are required is realistic.

---

## Finding 9: The memo does not mention `handleCancelJob` / `handleResumeJob` extraction, but these are in scope via Layer 1 (Severity: Informational)

Both `AnalysisWorkspacePage` and `AoiV2ThematicPanel` implement nearly identical `handleCancelJob` and `handleResumeJob` callbacks that route through `API_BASE`. The memo's Layer 1 scope ("cancel wrapper", "resume wrapper") covers this. No memo change needed — just confirming coverage.

---

## Assessment of Non-Goals

The non-goals list is well-calibrated:

- **active-tab state**: Correct exclusion, though the callback boundary needs acknowledgment (Finding 2).
- **tab default selection**: Correct — this is page-specific.
- **view lazy-loading**: Correct — the lazy-load effect in `AoiV2ThematicPanel` (:220–283) is tightly coupled to tab/presentation state and should stay local.
- **workflow-specific saved-result list row types**: Correct — `GenealogyPage`'s extra fields confirm this.
- **AOI-specific launch payload assembly**: Correct — `handleRunAnalysis` in `AoiV2ThematicPanel` routes through a Critic-backend endpoint (`/influence/thinkers/.../run-thematic-analysis-v2`) that is irreducibly AOI-specific.
- **page-specific empty states and explanatory copy**: Correct.

The non-goals are neither too broad nor too narrow.

---

## Verdict

**Proceed.**

The extraction seam is real, confirmed by ~800 lines of near-identical lifecycle code across three surfaces. The scope is well-bounded. The two adoption targets (`AnalysisWorkspacePage` as proving vehicle, `AoiV2ThematicPanel` as required second consumer) are the right pair. The `GenealogyPage` exclusion is correct. The non-goals prevent the tranche from drifting.

Two minor scope clarifications should be added before implementation begins:

1. Acknowledge the `onPresentationLoaded` callback boundary between the shared contract and per-surface tab management.
2. Note that `AoiV2ThematicPanel` requires `selected_source_thinker_id` scoping in discovery calls and that this must be parameterized in the shared contract.

Neither of these changes the scope decision. They are implementor guidance, not scope expansions.

Phase 2 / Deliverable B should be the next tranche.
