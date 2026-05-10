# Critique: Stage 5 AOI Exemplar Revision Slice Scope

Date: 2026-03-24
Reviewer: Claude (Opus 4.6)
Memo under review: `communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md`

## Verdict

**Approved after revision**

The memo is structurally sound, correctly scoped, and aligned with both the AOI exemplar objective and the broader platformization program. But the selector/provider diagnosis (Decision 3) can already be materially narrowed from evidence in the codebase and the eval artifacts, and the host-visibility workstream (Decision 4) should name the actual mechanism more precisely. The revisions are small.

---

## Findings

### 1. The selector/provider failure class is already narrowable — the memo should say so

**Importance: High**

The memo correctly insists on diagnosing before widening behavior (Decision 3). But the evidence already available narrows the failure class significantly. The memo should incorporate this rather than leaving it fully open.

**Evidence from the codebase:**

- `src/orchestrator/task_planner.py:40` sets `AOI_SELECTION_TIMEOUT_S = 10.0`. This is a hardcoded 10-second httpx read timeout passed to `get_anthropic_client(read_timeout_s=AOI_SELECTION_TIMEOUT_S)` at line 713.
- `src/llm/client.py:44-52` configures `httpx.Timeout(connect=60, read=10, write=60, pool=60)` — the read timeout is uniquely tight compared to every other timeout dimension.
- The eval summary (`PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json`) records the `evolution_ready` plan-task request/response at `15:20:53` → `15:21:25` (≈32s wall clock). The error detail is: *"AOI selector provider call failed: Request timed out or interrupted. This could be due to a network timeout, dropped connection, or request cancellation."*
- This error text matches the Anthropic SDK's `APIConnectionError` or upstream gateway timeout pattern, not a clean `httpx.TimeoutException`. That is why the exception handler at lines 738–757 classified it as `llm_provider_failure` rather than `llm_timeout`.

**What this means:**

- **Environment/config is almost certainly ruled out.** The ANTHROPIC_API_KEY is present and valid — `route-task` succeeds for all four cases, and the plan-task request is accepted and processed by the Anthropic API (the response took 32s, not 0s). The client initializes successfully.
- **Timeout budget is the primary failure class.** A 10-second httpx read timeout for a synchronous `messages.create()` call to Claude Sonnet is extremely tight. Any non-trivial generation that doesn't produce response bytes within 10 continuous seconds will trigger a connection interruption. Compare this to the extraction pipeline, which uses a configurable 180s default (`ANTHROPIC_EXTRACTION_READ_TIMEOUT_S`).
- **Provider-path fragility is a secondary but real issue.** The exception classification at lines 738–757 checks for `httpx.TimeoutException | TimeoutError` but the Anthropic SDK raises `APIConnectionError` for connection-level interruptions (including those caused by the client's own read timeout). So timeout-caused failures are misclassified as generic provider failures.

**Suggested revision:**

Decision 3 should include a "working hypothesis" subsection stating:

> The working hypothesis, based on codebase and eval-artifact evidence, is that this is primarily a timeout-budget issue (10s httpx read timeout at `task_planner.py:40`) with a secondary exception-classification gap. Environment/config failure is ruled out by the successful route-task path. The diagnosis step should confirm or refute this hypothesis, not start from a blank slate.

This doesn't violate the memo's "decide from evidence, not guesswork" principle — it accelerates it.

### 2. The host visibility failure is a state-retention bug, not a missing-state bug — the memo should say so

**Importance: High**

The memo correctly characterizes this as a "proof-surface bug" (Decision 4). But the codebase shows the error IS being set — it's just not persisting. The memo should name this mechanism.

**Evidence from the codebase:**

- `AoiV2ThematicPanel.tsx:587-601`: When `planning_outcome_kind === 'aoi_selection_blocked'`, the code throws an Error with the blocked reason. The catch at line 600 calls `setPageError(error.message)`. The error banner at lines 985–995 renders `pageError ?? lifecycleError`.
- The eval summary records a non-null `planner_banner` field with the full error text — meaning the Playwright automation DID capture the error text somewhere in the DOM or network. But `blocked_reason_visible: false` means the screenshot didn't show it as a stable visible state.
- There are 13 call sites in the panel that set `pageError(null)`: lines 373 (loadSelection), 534 (handlePlannerBackedPlan start), 625 (launchPlannerBackedCompose start), 690, 813, 862, 879, 904, 1209. If any effect or callback fires after the error is set — for example, if auto-discovery polling or a saved-result refresh runs — the error could be cleared.

**What this means:**

The error is being set correctly. Something else is clearing it before the screenshot captures it. This is a **state-retention bug** (the error exists transiently but is overwritten), not a **missing-state bug** (the code doesn't produce the error at all).

**Suggested revision:**

Decision 4 should add:

> The codebase evidence shows that `setPageError` IS called with the blocked reason at `AoiV2ThematicPanel.tsx:601`. The likely mechanism is that another callback or effect calls `setPageError(null)` after the blocked-error state is set. The fix should identify which re-render path clears the error and prevent it from doing so while a planner-blocked result is the active state.

### 3. The `AOI_SELECTION_TIMEOUT_S` should become environment-configurable

**Importance: Medium**

The memo's "Allowed outcomes" includes "bounded timeout adjustment." The implementation should not just increase the hardcoded constant — it should make it environment-configurable, matching the pattern already used for `AOI_SELECTION_MODEL` (line 39: `os.environ.get("AOI_SELECTION_MODEL", GENERATION_MODEL)`) and `ANTHROPIC_EXTRACTION_READ_TIMEOUT_S` (client.py:210).

A reasonable default would be 30–60s. The selector prompt is small (bounded source catalog, not large documents), but the LLM still needs to reason about family selection, produce rationale, and serialize JSON output.

This is not scope creep — it's the minimum necessary fix to unblock the rerun.

### 4. The memo is correctly refusing a phase pivot

**Importance: High (positive)**

The memo's reasoning here is exactly right and well-supported:

- Route-task works for all four cases.
- Plan-task is reached and processes correctly (source catalog resolution, routing reuse, candidate scoring all succeed — visible in the trace).
- The blocked-case fixture is valid and produces the correct `no_usable_source_families` outcome.
- The failure is localized to the LLM selector call (timeout/connection) and the host error-state retention.

These are operational defects, not architectural mismatches. Pivoting to Tranche 3 because of a 10-second timeout would be a category error.

### 5. Keeping the pack and rubric frozen is the right discipline

**Importance: High (positive)**

The rubric was written before grading. The eval pack has fixed cases. Changing either after a failure would undermine the program's credibility. The memo is explicit about this (Decision 5) and the reasoning is sound.

### 6. The `messages.create()` vs streaming question deserves a note

**Importance: Low-Medium**

The AOI selector at `task_planner.py:728` uses synchronous `client.messages.create()`. For the extraction pipeline, there is already a documented principle in the project memory that streaming is more robust for large inputs.

The selector prompt is small, so the input-size concern doesn't apply here. But `messages.create()` non-streaming means the entire response must be generated before any bytes are returned. If the Anthropic API or any intermediate proxy has a gateway timeout shorter than the generation time, the request fails.

The memo doesn't need to prescribe switching to streaming — that would be scope creep. But the diagnosis note (Deliverable 1) should record whether the failure happens before or after the first response byte, since that determines whether streaming would help.

### 7. The exception type classification gap should be hardened as part of the fix

**Importance: Medium**

The current code at `task_planner.py:738-757` distinguishes `httpx.TimeoutException | TimeoutError` from other exceptions. But the Anthropic SDK's `APIConnectionError` (which is raised for connection interruptions including timeout-triggered disconnects) does not inherit from either. So timeout-caused failures are systematically misclassified as `llm_provider_failure`.

The bounded fix should also catch `anthropic.APIConnectionError` and `anthropic.APITimeoutError` explicitly in the timeout branch, or at minimum record the actual exception class name in the trace for diagnosis.

This is within the "bounded provider-path hardening" allowed outcome.

---

## Alignment With Bigger-Picture Objective

### Frame 1: Is this the right immediate next step for the AOI exemplar?

**Yes, clearly.** The exit gate failed. The failures are concrete and bounded. The memo correctly identifies the two failure classes, refuses to change the test, and insists on rerunning the same pack. This is exactly what an honest exemplar process requires.

### Frame 2: Is this the right immediate next step for the platformization effort?

**Yes.** The broader program needs the AOI exemplar to be credible before generalizing. A platform claim built on an exemplar that failed its own exit gate is weaker than a platform claim built on an exemplar that failed, was fixed, and then passed. The memo explicitly holds Stage 2 open, holds the pack frozen, and refuses to advance to Tranche 3. This is the right call for program integrity.

The two fixes required (timeout adjustment + error-state retention) are also generalizable lessons:
- Timeout budget for LLM-backed planning seams will matter for every future workflow, not just AOI
- Host-state retention for blocked planner outcomes will matter for every future consumer, not just the-critic

So this revision slice is doing platform-relevant hardening, not just AOI-local patching.

---

## Roadmap Recalibration Assessment

The memo proposes:

- **Update slightly**: yes — one bounded revision slice inside the existing tranche
- **Recalibrate immediate plan**: yes — adds diagnosis + fix + rerun before any advancement
- **Do not pivot phases**: yes — keeps AOI exemplar before Tranche 3

This is correct. The evidence supports all three positions.

---

## Concrete Revisions Before Implementation

1. **Decision 3 should include the working hypothesis** that this is primarily a timeout-budget issue (10s read timeout at `task_planner.py:40`), with environment/config already ruled out by the successful route-task path. The diagnosis step should confirm this, not start from scratch.

2. **Decision 4 should name the specific mechanism**: `setPageError` IS called at `AoiV2ThematicPanel.tsx:601`, so the issue is state-retention (something clears the error), not state-production (the code doesn't generate the error). The fix should trace what clears the error.

3. **The "Allowed outcomes" in Decision 3 should explicitly include** making `AOI_SELECTION_TIMEOUT_S` environment-configurable, matching the existing pattern for `AOI_SELECTION_MODEL`.

4. **The "Allowed outcomes" in Decision 3 should explicitly include** hardening the exception classification to catch `anthropic.APIConnectionError`/`anthropic.APITimeoutError` as timeout-class failures, not just `httpx.TimeoutException`.

These four revisions are small, evidence-based, and do not change the memo's structure or scope. They accelerate the diagnosis step rather than widening the revision slice.
