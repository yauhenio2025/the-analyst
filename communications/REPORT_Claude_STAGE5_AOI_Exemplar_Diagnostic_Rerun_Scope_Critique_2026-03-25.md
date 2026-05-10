# Critique: Stage 5 AOI Exemplar Diagnostic And Rerun Scope

Date: 2026-03-25
Reviewer: Claude Opus 4.6
Status: Scope critique
Memo under review: `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`

## Verdict

**Approve**

The memo is honest, sequentially correct, and well-scoped. It asks for the right next step — one live diagnostic spot-check followed by a frozen rerun — rather than inventing more code to write. The branch rule is real. The roadmap order is preserved. The platform objective is served because an un-ratified exemplar is worse than a delayed one.

---

## Findings

### Finding 1: The revision-slice code is genuinely landed and structurally sound (confirms memo claim)

Severity: confirmation

The memo claims the revision slice is implemented. Code inspection confirms:

**Analyzer-v2:**

- `src/orchestrator/task_planner.py:40-41`: `AOI_SELECTION_TIMEOUT_S_DEFAULT = 45.0` and `AOI_SELECTION_MAX_RETRIES = 0` — the old 10s hardcoded timeout and default SDK retry behavior are gone.
- `src/orchestrator/task_planner.py:84-85`: timeout is env-configurable via `AOI_SELECTION_TIMEOUT_S`.
- `src/orchestrator/task_planner.py:727-825`: The `_call_aoi_selection_llm` function now passes `max_retries=AOI_SELECTION_MAX_RETRIES` (0) to the client constructor, and the exception handler at lines 763-805 explicitly distinguishes `anthropic.APITimeoutError` / `httpx.TimeoutException` / `TimeoutError` (→ `llm_timeout`) from `anthropic.APIConnectionError` (→ `llm_provider_failure`) from all other exceptions (→ `llm_provider_failure` with class name in trace). This directly addresses the original failure where timeout-shaped provider failures were collapsed into `llm_provider_failure`.
- `src/llm/client.py:31-56`: `get_anthropic_client` now accepts `max_retries` and passes it through to the Anthropic constructor, without changing default behavior for other callers.

**The Critic:**

- `AoiV2ThematicPanel.tsx:179`: `plannerDecision` is now structured state (`useState<TaskPlanningDecision | null>`), not ephemeral `pageError` text.
- Lines 610-613: Blocked outcomes set `plannerDecision` and explicitly null out `pageError`, so the structured decision is the source of truth.
- Lines 622: Ready outcomes also set `plannerDecision`.
- Lines 283-287: `plannerDecision` is cleared on active-job start (correct).
- Lines 393-394: `loadSelection` with `clearPlannerOutcome: true` clears it on explicit source switch (correct).
- Line 489: Initial auto-load passes `clearPlannerOutcome: false`, so the delayed hydrate race no longer wipes planner state (this was the exact bug).
- Line 560: New planning attempt clears prior decision (correct).
- Lines 944-946: Explicit dismiss clears it (correct).

The test file confirms direct regression coverage:
- Line 642: `planner-backed blocked outcome survives refresh churn until explicitly dismissed`
- Line 709: `planner-backed blocked outcome survives task-text edits until explicitly dismissed`
- Line 802: `planner-backed blocked outcome survives the delayed initial auto-load race`

**Assessment**: The memo's claim that the revision slice is "now implemented" is honest and code-backed. The two failure classes from the first gate run (selector/provider reliability and host blocked-state visibility) are both materially addressed.

---

### Finding 2: The `evolution_ready` spot-check is the right first case (confirms memo choice)

Severity: confirmation

The memo proposes running `evolution_ready` as the diagnostic spot-check before the full rerun. This is the right choice for three reasons:

1. `evolution_ready` was the leading ready case in the first pack — its failure is the most representative of the timeout/classification issue.
2. Its expected source families (`thematic_synthesis` + `thematic_report`) are the simplest selection shape — if the LLM selector can't produce this, the harder cases won't pass either.
3. `engagement_ready` includes `sin_findings` and `non_profile_ready` requires an explicit rejection of `sin_findings` — both add selection complexity that could confuse a diagnostic.

No hidden dependency makes another case a better first probe.

---

### Finding 3: The branch rule is honest enough (confirms memo design)

Severity: confirmation

The memo's Decision 4 states three branches:

1. Spot-check passes credibly → proceed to full rerun.
2. Environment-only issue → fix environment, re-spot-check, then rerun.
3. New code/product-path failure → stop and write a new revision memo.

This is the right structure. The third branch is particularly important — it prevents the program from consuming a full rerun dishonestly when the underlying repair didn't actually close the gap. The memo is explicit that "this keeps the rerun honest."

One minor observation: branch 2 (environment-only issue) could mean anything from a missing API key to a network timeout from a cold provider start. The memo should not require that the implementor distinguish these with certainty before proceeding — a reasonable judgment call after one retry should be enough. The current text is loose enough to allow that.

---

### Finding 4: One real risk the memo should acknowledge more explicitly — the 45s timeout may still not be enough

Severity: low

The old timeout was 10s. The revision slice raised it to 45s (configurable). The original first-gate-run artifacts showed ~32s wall-clock for the blocking `plan-task` response, but that was with the old 10s timeout **plus retry amplification** (SDK default retries).

With `max_retries=0` and a 45s timeout, a single attempt should have enough room. But the 45s budget is not generous for a cold-start Sonnet call with a moderately complex prompt. If the spot-check still shows a timeout at 45s, the diagnosis note should record whether the actual wall-clock was close to the limit or whether the failure was something else.

The memo's artifact requirements (exception class, elapsed time, retry count, reason code) are sufficient to surface this. But the memo does not flag this as a known risk to watch for. Adding one sentence to Decision 3 noting "if the spot-check still shows a timeout-shaped failure at the new 45s budget, the diagnosis should propose a timeout adjustment rather than a new code tranche" would make the branch rule more actionable.

This is a minor observation, not a blocking issue.

---

### Finding 5: The memo correctly keeps roadmap order intact (answers question 1)

Severity: confirmation

The memo explicitly states:

- Do not change the case set.
- Do not change the rubric.
- Do not change the roadmap order.
- Do not change the Stage 2 closure bar.

The draft roadmap in `MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md` places Tranche 2 (AOI exemplar completion, including Stages 3/4/5) as a precondition for Tranche 3 (de-AOI / de-`the-critic` transient generalization). The diagnostic rerun memo stays inside Tranche 2 and does not claim to advance Tranche 3.

The sequencing note at line 223-224 of the draft roadmap explicitly says "the immediate next step inside this tranche is no longer another repair slice by default; it is one live diagnostic `evolution_ready` spot-check and then the same frozen Stage 5 rerun." The memo under review is exactly that step.

---

### Finding 6: The memo is sufficiently explicit about Stage 5 vs Stage 2 likely outcomes (answers question 4)

Severity: confirmation

Decision 6 in the memo states:

- Stage 5 may pass.
- Stage 2 may still remain open.

It correctly notes that Stage 2 closure requires at least one `execution_backed` ready case, and the current pack is `fixture_backed`. It offers `evolution_ready` as the default upgrade candidate but does not force that upgrade.

This is the right level of explicitness. The rubric at `MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md` lines 128-133 confirms: Stage 2 documentary closure requires the Stage 5 gate to pass AND at least one ready case to be `execution_backed` or stronger.

---

### Finding 7: No hidden dependency makes the rerun less meaningful than the memo claims (answers question 6)

Severity: confirmation

I checked for hidden dependencies:

1. **No code drift since the revision slice**: The completion memo reports `56 passed` (analyzer), `90 passed` (frontend), `42 passed` (backend). The memo under review says "If no code changes are made before the spot-check, verification can rely on the already-green focused confidence pack." This is correct — the test suite was run after the revision slice, not before.

2. **No schema or contract change between analyzer and host**: The `TaskPlanningDecision` schema referenced by both `task_planner.py` and `taskLaunchRuntime.ts` has not changed since the revision slice. The `planTask` / `routeTask` calls in `AoiV2ThematicPanel.tsx` (lines 563-603) still match the analyzer API contract.

3. **No environment drift**: The memo targets local `analyzer-v2` + local `the-critic`, the same proof environment used in the first run. No deployment step is needed.

4. **The frozen rubric still applies**: The rubric at `MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md` was written before the first gate run and has not been modified. The case set is unchanged.

5. **No stage 8/9/10/11/12/13 code changes interfere**: The Stage 8/9 host-adoption work (task routing + planning) is the code that will be exercised. The revision slice hardened it. No parallel work has modified those paths since.

---

### Finding 8: The memo preserves the broader platform objective (answers question 7)

Severity: confirmation

The broader objective from the master roadmap is: make analyzer-v2 the brain for dynamic bespoke analytical apps, with `the-critic` as the proving ground.

The memo preserves this because:

1. It does not overfit to AOI proof maintenance — it proposes exactly one diagnostic and one rerun, not an open-ended repair cycle.
2. It explicitly blocks Tranche 3 generalization until the exemplar passes, which prevents generalizing from un-ratified substrate.
3. It keeps Stage 2 honest — no premature closure language.
4. The acceptance criteria at lines 200-203 require either an honest pass or an honest failure, not a forced pass.

The risk of overfitting to AOI proof maintenance would arise if the program entered a third revision slice. The memo's branch rule (branch 3: "stop and write a new revision memo rather than pretending the full rerun is meaningful") appropriately addresses this — it does not pre-authorize another code tranche.

---

## Program-Level Recommendation

The program should:

- **Not pivot phases.** The roadmap order is correct. Tranche 2 (AOI exemplar) must complete before Tranche 3 (transient generalization).
- **Recalibrate the immediate plan only.** The immediate next step is the diagnostic spot-check and frozen rerun, not more code.
- **Not update the roadmap.** The draft roadmap already records this as the correct next step inside Tranche 2.

---

## Concrete Revisions Recommended Before Implementation

1. **Optional (low priority)**: Add one sentence to Decision 3 or Decision 4 noting that if the spot-check still shows a timeout at the 45s budget, the diagnosis note should propose a timeout adjustment as an environment fix (branch 2) rather than a new code tranche (branch 3), unless the wall-clock evidence shows the failure is not timeout-shaped.

No other revisions are needed. The memo is ready for implementation as written.

---

## Summary Table

| Question | Answer |
|----------|--------|
| 1. Roadmap order intact? | Yes |
| 2. Right next move? | Yes |
| 3. Branch rule honest? | Yes |
| 4. Stage 5 vs Stage 2 explicit? | Yes |
| 5. `evolution_ready` the right first case? | Yes |
| 6. Hidden dependency? | None found |
| 7. Platform objective preserved? | Yes |
