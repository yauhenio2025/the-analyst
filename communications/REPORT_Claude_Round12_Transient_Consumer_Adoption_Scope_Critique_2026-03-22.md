# Scope Critique: Round 12 — AOI Transient Consumer Adoption

**Verdict: Approve after revision**

The round-12 direction is correct and timely. The dedicated transient shell is the right architectural choice over retrofitting `AnalysisWorkspacePage`. However, the memo is underspecified on three material implementation seams that, if left vague, will cause mid-implementation scope drift or force ad-hoc decisions that weaken the proof.

---

## Findings (ordered by severity)

### 1. CRITICAL — Shape mismatch between `TransientIntentView` and frontend `ViewPayload` is unaddressed

The memo states the transient shell should "accept the round-11 transient response shape directly" and "reuse the existing generic renderer path through `ViewRenderer`." These two claims are in tension.

`ViewRenderer` accepts a `ComposedView` (from `useViewDefinitions`) and `data: unknown`. It does not accept `TransientIntentView` directly.

`V2TabContent` defines a frontend `ViewPayload` interface with 22 fields (`V2TabContent.tsx:58-83`). The backend `TransientIntentView` (`schemas.py:631-647`) has only 13 fields and is missing:

- `priority` (required `string` in frontend)
- `data_quality` (required `string`)
- `source_parent_view_key`
- `phase_number` (required `number | null`)
- `chain_key` (required `string | null`)
- `scope` (required `string`)
- `raw_prose` (required `string | null`)
- `prose_ref_view_key`
- `tab_count` (required `number | null`)

Several of these fields are actively used in `V2TabContent`'s rendering logic — `data_quality` controls empty-state behavior (line 721), `raw_prose` drives prose resolution (lines 216, 653, 659, 672), `source_parent_view_key` drives promoted-child collection (line 250).

**Impact**: If the transient shell tries to pass `TransientIntentView` through `ViewRenderer` or any code path that expects `ViewPayload`, it will crash on missing fields or produce incorrect rendering.

**What should be tightened**: The memo must specify whether the transient shell:
- (a) maps `TransientIntentView` → frontend `ViewPayload` with safe defaults before passing to `ViewRenderer`, or
- (b) uses `ViewRenderer` with a thinner adapter type that does not pretend to be `ViewPayload`

Option (a) is simpler and reuses more of the existing path. Option (b) is more honest but creates a second rendering contract. The memo should pick one and state it.

---

### 2. HIGH — Request duration and loading UX unspecified

`compose_from_intent.py` is synchronous — it calls `asyncio.run()` inside a sync function at lines 402 and 480, meaning each LLM call blocks the request thread. The route makes at minimum 1 planner call + N view generation calls + N transformation calls. For a 2-section AOI request, that is 5+ serial LLM calls.

Based on prior project evidence (memory note on output speed: ~35 min for 183K-token inputs), even with smaller inputs the round-trip for this route is likely 30-90 seconds.

The memo specifies "loading / error / retry state local to the transient page" but does not address:

- Whether the frontend should show per-stage progress (the trace stages are only available after the full response returns)
- Whether the request should use a streaming contract or a polling pattern instead of a blocking POST
- What the user sees during 30-90 seconds of waiting

**Impact**: Without specifying this, the implementor will either build a spinner (poor UX for 60+ second waits), invent a streaming protocol (scope creep), or accidentally widen scope by adding a polling mechanism.

**What should be tightened**: The memo should explicitly state: "round-12 uses a blocking POST with a simple loading state. Per-stage progress is out of scope. The proof standard does not require sub-30-second responses." This bounds the UX expectation and prevents scope creep toward SSE/polling.

---

### 3. HIGH — Prose section origin in consumer input UX is handwaved

The memo says the input surface should include "1 to 4 prose sections" and may include "load dossier example" / "load comparison example" helper affordances.

But the `ComposeFromIntentSectionInput` schema requires `engine_key`, `title`, and `prose` (all non-empty strings, validated at `compose_from_intent.py:237-249`). The `prose` field contains full engine output text — typically thousands of words of structured analysis.

No user will type this into a text area. The only realistic input path is:

- paste from clipboard, or
- load from a previous job's phase output, or
- use the pinned round-11 control payloads

The memo mentions "proof inputs should still be pinned to the round-11 AOI control requests" but doesn't clarify whether "load dossier example" means:

- (a) hardcoded JSON payloads shipped with the frontend bundle, or
- (b) fetched from a previous completed job's outputs via the executor API, or
- (c) pasted by the user from the round-11 proof JSON files

**Impact**: If the implementor interprets (b), they will build a job-result browser for selecting previous outputs — significant scope creep that violates "without faking job semantics." If they interpret (c), the proof is only usable by someone with access to the proof JSON files.

**What should be tightened**: The memo should state explicitly: "The round-12 input surface ships 2 hardcoded example payloads (the round-11 dossier and comparison requests). Free-text prose input is out of scope. Loading from previous job results is out of scope."

---

### 4. MEDIUM — Memo accurately describes the consumer gap but understates `ViewRenderer`'s transient readiness

The memo says `ViewRenderer` "is generic enough to render transient returned views." This is correct but imprecise.

Looking at `ViewRenderer.tsx:96-100`, the `jobId` prop is already optional:

```typescript
interface ViewRendererProps {
  view: ComposedView;
  data: unknown;
  jobId?: string;    // ← optional
  scaffold?: ...;
  ...
}
```

When `jobId` is undefined, the renderer still works — it just omits `_jobId` from the config object (line 114-116). This means `ViewRenderer` is already transient-ready with zero changes.

The gap is not in `ViewRenderer` — it's in the data types (`ComposedView` vs `TransientIntentView`) and in `V2TabContent` which wraps `ViewRenderer` with job-dependent orchestration. The memo conflates "V2TabContent is not transient-ready" (true) with implying `ViewRenderer` needs work (false).

**What should be tightened**: The memo should state: "ViewRenderer requires zero changes. The transient shell must map the response shape to `ComposedView` + `data` before calling ViewRenderer."

---

### 5. MEDIUM — No mention of the-critic's existing MASTER_MEMO_CURRENT.md

The-critic already has an active `MASTER_MEMO_CURRENT.md` focused on "AOI V2 Hot-Path Cutover." Round 12 adds a new the-critic page/component. The memo should acknowledge whether round-12 work in the-critic conflicts with or depends on the hot-path cutover work.

If round 12 is meant to be implemented as a standalone proof branch in the-critic without coordinating with the cutover memo, the scope doc should say so explicitly.

---

### 6. LOW — The `400 / 502 / 503 / 409` error contract is backend-only; frontend mapping unspecified

The memo specifies the backend error surface (400 client error, 502 upstream, 503 dependency unavailable, 409 contract invalid) and says the transient page should preserve this distinction. But the memo doesn't specify how the frontend should display these different error classes.

A minimal mapping would be:
- 400 → user-correctable input error with inline feedback
- 502/503 → system error with retry affordance
- 409 → diagnostic message with trace data

This is minor but worth a one-line specification so the implementor doesn't flatten all errors into a generic alert.

---

### 7. LOW — Dedicated route URL format has implicit assumptions

The proposed route `/p/:projectId/analysis/anxiety_of_influence_thematic_single_thinker/compose-from-intent` hardcodes the workflow key in the URL path. This is fine for a bounded proof, but it means the route definition in React Router will either be:

- a literal string match (brittle, duplicates routing logic), or
- a `:workflowKey` param with a guard (more generic than the memo intends)

The memo should state which pattern is expected to prevent over-generalization.

---

## Assessment of Memo Claims

| Claim | Accurate? | Notes |
|-------|-----------|-------|
| V2TabContent is not transient-ready | **Yes** | 14+ job_id references, `PagePresentation.job_id` is required |
| AnalysisWorkspacePage is job-lifecycle bound | **Yes** | Job launch, polling, saved results, refresh all present |
| ViewRenderer is generic enough | **Yes** | `jobId` already optional, works without it |
| Round 12 is the right next move | **Yes** | Backend proof without frontend adoption is incomplete |
| Dedicated shell over retrofit | **Yes** | Retrofitting would mean optionalizing 14+ job_id paths |
| AOI is the only honest proof surface | **Yes** | Rounds 9-11 all closed seams on AOI specifically |

---

## Perspective Docs Search

No dedicated "Perspective" project, component, or documentation was found in `/home/evgeny/projects/`. The word appears only in audience vocabulary translations (e.g., `analyst.json`: "marginalized perspective" → "outlier data point"). No sibling-repo Perspective docs are materially relevant to round 12.

The most relevant external document is `communications/DYNAMIC_BESPOKE_APPS_VISION.md`, which articulates the long-term vision of analyzer-v2 as the brain with consumer apps as ephemeral shells. Round 12 is the first concrete realization of this vision on a real consumer surface.

---

## Summary of Required Revisions Before Execution Plan

1. **Specify shape mapping strategy**: `TransientIntentView` → frontend rendering type (map to `ViewPayload` with defaults, or introduce thin adapter type?)
2. **Specify request duration expectation**: blocking POST, simple loading state, no sub-minute guarantees
3. **Specify prose section input source**: hardcoded example payloads, not job-result browser
4. **Clarify ViewRenderer needs zero changes**: transient shell does the mapping, ViewRenderer stays generic
5. **Acknowledge the-critic's existing MASTER_MEMO_CURRENT.md**: state whether round-12 is independent of or sequenced with hot-path cutover
6. **One-line error display mapping**: which HTTP status codes get which UX treatment
