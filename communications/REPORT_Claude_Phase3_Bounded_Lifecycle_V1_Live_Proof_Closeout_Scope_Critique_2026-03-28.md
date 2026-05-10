# REPORT: Phase 3 Bounded Lifecycle V1 Live Proof Closeout Scope Critique

Date: 2026-03-28
Evaluating: `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md`
Reviewer: Claude (Opus 4.6)
Method: Code-path inspection + memo-trail verification + roadmap alignment + test coverage audit

---

## 1. Verdict

**Approve**

The memo is strategically correct, properly bounded, and honestly sequenced. It identifies the right next step: close Phase 3 with live evidence, not more implementation and not Phase 4 governance. The code fully supports all claims made in the memo. The implementation is clean and the evidence gap is genuine.

The memo makes no false claims about code state, draws the analyzer/host ownership line correctly, and stays bounded away from all the scope drift risks it names.

Three findings follow. None are blocking. Two are low-severity sharpening suggestions. One is observational.

---

## 2. Findings (ordered by severity)

### Finding 1 (LOW): The proof page UI header still says "Phase 2 Proof" — cosmetic residual that could weaken the screenshot artifact

The implementation completion memo already noted this residual:

> one minor UI label residual remains: the proof page header still says `Phase 2 Proof`

File: `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx:218`

```tsx
<p className="compose-from-intent-page__eyebrow">Phase 2 Proof</p>
```

The closeout memo does not mention whether this should be fixed before the live proof run. Since the closeout requires a "rendered screenshot or equivalent rendered-state artifact after reopen" (memo line 215), a screenshot labeled "Phase 2 Proof" could be confusing to a future reviewer inspecting Phase 3 documentary evidence.

**Recommendation**: Fix the label to "Phase 3 Lifecycle Proof" (or similar) before running the live proof. This is a one-line change that strengthens the artifact honesty. It is not a blocker.

### Finding 2 (LOW): The "no-recomputation proof" evidence shape relies on HAR absence — consider specifying the verification method

The memo requires (line 175-181):

> The closeout must make it obvious that reopen did not call:
> - `route-task`
> - `plan-task`
> - `planning_decision_fetch`
> - `planning_decision_compose_request`
> - `POST /v1/presenter/compose-from-intent`

The required evidence shape names a HAR (line 216). HARs capture all network traffic, so the absence of these calls would be demonstrated by not finding them in the HAR entries.

The code does correctly implement this — the reopen path (`GenealogyTransientProofPage.tsx:60-97`) clears all prior state and only calls `getComposeSession(sessionId, TRANSIENT_CONSUMER_KEY)`. The test at `GenealogyTransientProofPage.test.tsx:266-281` explicitly asserts `not.toHaveBeenCalled()` for all five endpoints.

**Recommendation**: The closeout executor should grep the HAR JSON for the five forbidden endpoint patterns and include the grep result (showing zero matches) in the proof artifact set. This makes the "no recomputation" claim machine-inspectable rather than only human-inspectable.

### Finding 3 (OBSERVATION): The proof page preflight does not programmatically assert all five readiness fields the memo requires

The memo's Must Land item #1 requires the preflight to confirm:

- `workflow_key = intellectual_genealogy`
- `status = completed`
- `result_state = ready`
- `presentation_status = completed`
- `restore_available = true`

The current proof page code (`GenealogyTransientProofPage.tsx:125-135`) only programmatically asserts the first two:

```tsx
if (nextRunDetail.workflow_key !== GENEALOGY_WORKFLOW_KEY) { throw ... }
if (nextRunDetail.status !== 'completed') { throw ... }
```

The remaining three fields (`result_state`, `presentation_status`, `restore_available`) are present in the run detail response but not programmatically validated by the proof page.

**Assessment**: This is not a code bug. The proof page renders the full run detail JSON in the trace section (`GenealogyTransientProofPage.tsx:300-303`), so a human reviewer can verify all five fields in the saved trace artifact. The Phase 2 proof artifacts already showed these fields present.

For the Phase 3 closeout, the trace JSON will contain the full run detail. The closeout evidence should explicitly note the values of these five fields rather than relying on implicit presence.

**Not a blocker**. The code is correct; the evidence annotation can be done at closeout time.

---

## 3. Direct answers to the nine questions

### Q1: Is a Phase 3 live proof closeout now the right next honest step?

**Yes.** The code is implemented. Tests pass (12 analyzer-side, 23 host-side). The evidence gap is genuinely evidentiary, not implementation. The memo is not prematurely blocking — it is correctly identifying the one remaining Phase 3 obligation before Phase 4.

### Q2: Is the memo right to keep the closeout on the existing genealogy proof page?

**Yes.** The genealogy proof page:
- sits on the thinnest generalized transient substrate already proved in Phase 2
- tests lifecycle where it was actually implemented
- avoids AOI source-backed proxy complexity as the first lifecycle proof burden
- already has the save/reopen UI controls implemented (`GenealogyTransientProofPage.tsx:187-208, 272-281`)

Widening to a new proof surface or AOI proxy lifecycle would be scope drift.

### Q3: Does the code support the memo's claim that lifecycle save/reopen is implemented but still lacks recorded live proof?

**Yes, unambiguously.**

Implemented and tested:
- `compose_session_store.py`: file-backed JSON persistence with `save_compose_session` / `load_compose_session`
- `presenter.py:479-535`: save and fetch routes with validation (400 bad request, 404 missing, 409 consumer mismatch)
- `schemas.py:746-759`: `PersistedComposeSession` model with all required fidelity fields
- `hostContractV2.ts:32-33`: `transient_compose_session_save` and `transient_compose_session_fetch` families
- `composeFromIntentClient.ts:85-168`: `saveComposeSession` and `getComposeSession` runtime helpers
- `GenealogyTransientProofPage.tsx:60-97`: reopen mode clears state and fetches only saved session
- `GenealogyTransientProofPage.test.tsx:266-293`: reopen and fail-closed tests

No live proof:
- `src/presenter/compose_sessions/` directory contains zero JSON files (confirmed by glob)
- No PROOF_phase3_* artifacts exist in `communications/`

### Q4: Is the memo drawing the analyzer/host ownership line clearly enough?

**Yes, with one minor clarification needed.**

The ownership split is clear:
- **Analyzer owns**: saved session truth, `session_id` generation, reopen payload truth, fidelity fields
- **Host owns**: `session_id` navigation (URL query param), reopen triggering, rendering, UI state clearing

One clarification: the fetch route defaults `consumer_key` to `"the-critic"` (`presenter.py:510`). The proof page explicitly passes `TRANSIENT_CONSUMER_KEY` (`GenealogyTransientProofPage.tsx:80`), so this default is not exercised in the proof path. The memo correctly treats `consumer_key` as host-threaded rather than defaulted, and the code matches.

The `session_id` handling is clean:
- Analyzer generates it at save time (`compose_session_store.py:27`)
- Host receives it from save response and writes it to URL (`GenealogyTransientProofPage.tsx:202`)
- Reopen reads it from URL search params (`GenealogyTransientProofPage.tsx:45`)
- Host does not generate or modify `session_id`

Browser navigation:
- Save updates URL via `setSearchParams({ session_id: saved.session_id })` — replaces all search params with just `session_id`
- Reopen triggers via `useEffect` on `sessionId` change
- This means deep-link by URL with `?session_id=<id>` works identically to save-then-reopen

### Q5: Is the memo correct that `planning_decision_id` remains provenance only and cannot substitute for lifecycle identity?

**Yes.** The code enforces this cleanly:

- `PersistedComposeSession.planning_decision_id` is `Optional[str]` (`schemas.py:753`) — it is metadata, not identity
- `session_id` is generated independently by `_build_session_id()` (`compose_session_store.py:27`) using `uuid4`
- The save route does not look up or validate `planning_decision_id` — it is stored as-is
- The fetch route keys on `session_id` only — `planning_decision_id` plays no role in retrieval
- The proof page's reopen path never calls `getPlanningDecision` or any planning endpoint

There is no code path where `planning_decision_id` could accidentally become lifecycle identity.

### Q6: Is the required evidence shape strong enough to prove "no recomputation on reopen"?

**Yes, if the HAR is verified.**

The evidence requirements are:
1. Trace JSON showing the compose-save-reopen chain
2. Screenshot after reopen
3. HAR for the browser session
4. Saved session payload with fidelity fields
5. Invalid session negative proof

The HAR is the key proof instrument for no-recomputation. It must show:
- One `POST /v1/presenter/compose-sessions` (save)
- One `GET /v1/presenter/compose-sessions/{session_id}` (reopen)
- Zero requests to the five forbidden endpoints

The test suite already asserts the forbidden-endpoint absence in mock (`test.tsx:275-280`). The live HAR would confirm this in production.

Per Finding 2, a scripted grep of the HAR for the forbidden endpoints would strengthen the evidence from "reviewer must inspect" to "machine-verified."

### Q7: Does the memo stay properly bounded away from out-of-scope work?

**Yes.** The "Must not widen" section (lines 200-208) explicitly blocks:
- Phase 4 governance/evaluation
- Lifecycle schema redesign
- Publish/share semantics
- Auto-save
- New transient consumer registration
- `planning_decision_id` as fake lifecycle identity
- AOI source-backed proxy as the closeout target

Each of these is a real temptation at this stage. The memo names them correctly and rejects them.

### Q8: Is anything in the memo contradicted by the live code?

**No.** Every claim in the memo has been verified against the codebase:

| Memo claim | Code confirmation |
|---|---|
| Save route exists at `POST /v1/presenter/compose-sessions` | `presenter.py:479` |
| Fetch route exists at `GET /v1/presenter/compose-sessions/{session_id}` | `presenter.py:507` |
| Analyzer generates `session_id` | `compose_session_store.py:27` |
| Save is explicit, not automatic | `GenealogyTransientProofPage.tsx:272-281` — save button, user-initiated |
| Reopen clears prior state | `GenealogyTransientProofPage.tsx:69-76` |
| Reopen fetches only saved session | `GenealogyTransientProofPage.tsx:78-93` |
| Invalid session fails closed | `presenter.py:517-521` returns 404 |
| Consumer mismatch fails with 409 | `presenter.py:522-529` |
| URL changes to `?session_id=<id>` | `GenealogyTransientProofPage.tsx:202` |
| `planning_decision_id` is provenance only | `schemas.py:753` — Optional, not used for lookup |

### Q9: Is anything important missing that would make the scope under-specified or unsafe to execute?

**No material gaps.** The scope is well-specified for execution.

Two minor execution-time suggestions (not blocking):

1. The proof page header label fix (Finding 1) should happen before the live proof run to avoid a confusing artifact.

2. The trace JSON artifact should explicitly annotate the five preflight readiness fields (Finding 3) rather than relying on their implicit presence in the run detail dump.

Neither of these requires a scope revision. Both can be handled during closeout execution.

---

## 4. Is this now the right next honest step?

**Yes.** The program state is:

- Phase 0: closed (AOI exemplar closure-grade)
- Phase 1: closed (planner-to-presentation bridge generalized)
- Phase 2: closed (host-neutral transient proof with live evidence)
- Phase 3 implementation: landed (code + tests pass)
- Phase 3 evidence: **missing** (no live proof artifacts)

The memo correctly identifies that the program cannot honestly claim Phase 3 is closed without one recorded live proof of compose → save → reopen-by-session_id. Moving to Phase 4 without this evidence would mean building governance on unproved lifecycle claims.

The bounded closeout is the right granularity: not more implementation, not a schema redesign, not Phase 4 — just one honest evidence run.

---

## 5. Does the memo stay properly bounded?

**Yes.** The memo exhibits strong scope discipline:

- Targets the existing proof page, not a new surface
- Uses the existing consumer registration, not a new one
- Requires evidence of what already exists in code, not new features
- Explicitly defers Phase 4, publish/share, auto-save, and AOI productization
- Names the acceptance bar in falsifiable terms (five enumerated conditions)
- Provides a clear fallback: "If any one of those is missing, do not mark Phase 3 closed. Write a bounded revision memo instead."

The scope is tight enough to execute in a single focused session and strict enough to produce genuine evidence.

---

## 6. Concrete revisions needed before execution

**None required.** The memo can proceed to execution as written.

**Recommended (not required) pre-execution touch-ups:**

1. Fix the proof page header label from "Phase 2 Proof" to "Phase 3 Lifecycle Proof" — one-line change in `GenealogyTransientProofPage.tsx:218`
2. During closeout, grep the captured HAR for the five forbidden endpoint patterns and include the zero-match result in the proof artifacts
3. During closeout, explicitly annotate the five preflight readiness field values in the trace artifact

These are execution-quality improvements, not scope revisions.
