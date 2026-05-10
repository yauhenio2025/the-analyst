# Review: Phase E Proof-Only Lifecycle Direct-Sections Scope

Verdict: **Approve with corrections**

Date: 2026-04-01
Reviewer: Claude Opus 4.6
Memo under review: `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_scope.md`

## Summary

This is a well-scoped, correctly reasoned next step. The memo identifies the right variable to change (lifecycle), keeps the right things fixed (harness, consumer identity, compose route), and makes an honest claim about what the proof would establish. The code backing is solid. I have no strategic objections, two implementation corrections, and three documentary notes.

---

## Strategic Assessment

### 1. Is `direct_sections` truly the smallest honest lifecycle target on the proof-only line?

**Yes.** This was verified against the actual code.

The compose-session persistence schema in `src/presenter/schemas.py:737-759` is hard-typed:

- `ComposeSessionSaveRequest.compose_request: ComposeFromIntentRequest` (line 740)
- `PersistedComposeSession.compose_request: ComposeFromIntentRequest` (line 758)

The `direct_sections` proof path uses `POST /v1/presenter/compose-from-intent` and sends a `ComposeFromIntentRequest` payload. This fits the existing compose-session contract exactly.

Any other lifecycle target on the standalone harness would require schema changes first:

- `source_selection` uses `ComposeFromSelectionRequest` (line 669), which has different fields (`source_v2_job_id`, `selection`, `selection_summary`, `legacy_profile_equivalent`). Saving this through the current compose-session schema would require a union type or a parallel schema family.
- `source_profile` is already explicitly out of scope and not admitted on the standalone harness consumers.

So `direct_sections` is the only proof-only lifecycle target that fits the codebase as it actually exists today. The memo's reasoning here is correct and code-backed.

### 2. Would `source_selection` lifecycle silently require compose-session schema widening?

**Yes.** The memo correctly identifies this.

`ComposeFromSelectionRequest` (lines 669-679) has a materially different shape from `ComposeFromIntentRequest` (lines 613-621). The current `ComposeSessionSaveRequest` cannot accept a `ComposeFromSelectionRequest` without one of:

- widening `compose_request` to `ComposeFromIntentRequest | ComposeFromSelectionRequest`
- creating a parallel `ComposeFromSelectionSessionSaveRequest`
- introducing a generic union envelope

Any of these is a materially larger step than what this scope memo proposes. The memo is honest about this.

### 3. Is keeping consumer identity fixed the right isolation discipline?

**Yes.** Consumer-key plurality was just proved in the immediately prior slice. The correct scientific discipline is to fix the variable you just proved and vary only the next untested variable. The memo applies this correctly:

- fixed: harness (`transient-proof-harness`)
- fixed: consumer key (`transient-proof-harness`)
- fixed: compose route (`compose-from-intent`)
- varied: lifecycle (save/reopen)

### 4. Does the memo overstate what a proof-only lifecycle direct-sections slice would prove?

**No.** The "Honest Claim If Completed" section (lines 269-280) is appropriately narrow. It explicitly lists four things the proof would NOT mean:

- lifecycle law not generalized across all transient request families
- AOI `source_selection` save/reopen not solved
- consumer identity not irrelevant for lifecycle
- generic reusable app/session lifecycle architecture does not exist

This is the right level of honesty.

### 5. Does the March 28 Phase 3 bounded lifecycle proof make this next slice too weak, or does the standalone harness boundary make it materially stronger?

**The standalone harness boundary makes it materially stronger.**

The Phase 3 proof (March 28) ran on:

- `the-critic` webapp (heavyweight existing consumer app)
- `GenealogyTransientProofPage.tsx` (a page with full `the-critic` infrastructure: `hostContractV2.ts`, `composeFromIntentClient.ts`, project routing, React dev patterns)
- consumer key: `the-critic`
- inside the same codebase that owns the compose-session client runtime

This new slice would run on:

- `transient-proof-harness` (a minimal standalone proof app with ~295 lines in `App.tsx`)
- no host contract runtime
- no compose-from-intent client library
- consumer key: `transient-proof-harness`
- a separate repo that does NOT own any compose-session client code

The delta is real. The Phase 3 proof showed lifecycle works inside the host that designed it. This proof would show lifecycle works in a host that has no prior lifecycle capability and no inherited client infrastructure for compose-session save/fetch.

This is the right kind of strengthening for Phase E.

---

## Implementation Corrections

### Correction 1: The compose-session GET route requires explicit `consumer_key` parameter

The memo's section 2 (lines 139-167) says reopen should fetch via:

> `GET /v1/presenter/compose-sessions/{session_id}`

But the actual route at `src/api/routes/presenter.py:507-535` has a `consumer_key` query parameter that defaults to `the-critic`:

```python
async def get_compose_session_endpoint(
    session_id: str,
    consumer_key: str = DEFAULT_CONSUMER_KEY,  # "the-critic"
):
```

If the session was saved under `consumer_key=transient-proof-harness`, the GET request must include `?consumer_key=transient-proof-harness` or the route will return 409 (consumer mismatch). This is tested at `tests/test_compose_sessions.py:154-176`.

**The scope memo should explicitly call out that the harness's reopen request must pass `consumer_key=transient-proof-harness` as a query parameter.** Omitting this will cause a 409 on the first reopen attempt, which may look like a bug rather than a missed parameter.

### Correction 2: The harness currently has no compose-session client functions

The memo treats the existing compose-session save/fetch routes as ready to use. They are — on the analyzer side. But the standalone harness at `/home/evgeny/projects/transient-proof-harness/src/lib/transientClient.ts` currently has:

- `composeFromSelection()` — POST to compose-from-selection
- `composeFromIntent()` — POST to compose-from-intent
- `normalizeTransientPresentation()` — normalize response to PagePresentation
- `validateTransientProofSurface()` — validate proof shape

It does NOT have:

- `saveComposeSession()` — POST to compose-sessions
- `fetchComposeSession()` — GET compose-sessions/{session_id}

The implementor will need to add these two client functions to `transientClient.ts`. This is not a scope objection — it is expected work for the slice — but the memo should mention it under required harness changes so the implementor's scope is explicit.

---

## Documentary Corrections

### Note 1: Acceptance bar item 6 should specify which fidelity field comes from where

Acceptance bar item 6 (lines 238-243) says the reopened payload should preserve fidelity fields including `consumer_key`, `workflow_key`, etc. This is correct, but it would be stronger if it specified that these must come from the `PersistedComposeSession` fields (which are derived from `compose_response.presentation`) and not from the fixture or any client-local state. The Phase 3 closeout memo was explicit about this ("These fields came from the fetched saved-session record, not from planner replay and not from host-local reconstruction"). This memo should carry the same precision.

### Note 2: The proof artifact family naming uses `2026-04-01` but execution may shift

The recommended naming family in section 5 (lines 212-215) hard-codes `2026-04-01` in the filenames. If implementation extends into the next day, the artifacts should use the actual execution date, not the scope-memo date. This is a minor cosmetic point — just note it for the implementor.

### Note 3: Missing mention of the ComposeFromIntentApiResponse type gap in the harness

The harness's `ComposeFromIntentApiResponse` type (in `transientClient.ts:75-89`) does not currently carry `presentation_hash` or `presentation_content_hash`. These fields are present in the real API response (as shown in the proof bundles) but the TypeScript type doesn't declare them. The save client function will need to send the full response JSON including these fields. The implementor should either widen the TypeScript type or send the raw response JSON directly.

---

## Is a Different Next Step Better?

**No.** I explicitly checked:

1. **Another consumer-identity variation?** — No. Plurality is already proved. More consumer keys would be repetitive, not strengthening.

2. **Source-selection lifecycle first?** — No. As analyzed above, this would require compose-session schema widening, which is a bigger step.

3. **Source-profile lifecycle?** — No. Source profiles aren't even admitted on the standalone harness consumers. That would require admission widening plus compose-session schema widening.

4. **Broader Phase E matrix widening?** — No. The distilled strategic roadmap (lines 336-346) explicitly says the next Phase E variable is lifecycle on the standalone harness, not another matrix broadening step.

5. **Skip directly to generic session-schema union?** — No. That would skip the bounded proof that motivates the union. The honest order is: prove lifecycle on the seam that already fits → then decide whether the union is needed to extend lifecycle to other seams.

The memo correctly identifies this as the next smallest honest step.

---

## Conclusion

**Approve with corrections.** The scope is the right size, the reasoning is correct, the code backing is honest, and the honest-claim section is appropriately narrow. The two implementation corrections (explicit `consumer_key` query param on GET, and missing harness client functions) should be addressed in the scope memo or in the implementor handoff to prevent avoidable first-attempt failures. The three documentary notes are advisory.
