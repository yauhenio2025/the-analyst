# Report: Phase E Transient Consumer Identity Generality Scope Critique

Verdict: **Approve with corrections**

Date: 2026-04-01
Reviewer: Claude (Opus 4.6)
Scope Memo Under Review: `communications/MEMO_2026-03-31_phase_e_transient_consumer_identity_generality_scope.md`
Codex Audit For Comparison: `communications/REPORT_Codex_Phase_E_Transient_Consumer_Identity_Generality_Scope_Audit_2026-03-31.md`

## Summary Judgment

The proposed slice is defensible as the next smallest bounded Phase E step, but only because the alternatives (lifecycle widening, source-profile broadening) are demonstrably larger in the current codebase. The memo correctly identifies the remaining variable. However, the memo materially overstates the substance of what a second proof-only consumer key proves. I substantially agree with the Codex audit's finding that this is a narrow residual anti-coupling check, not a meaningful "admission/adaptation generality" proof.

The slice should proceed, but with tighter claims and a clearer acknowledgment that this is close to the thinnest possible Phase E step before the program must move to a structurally stronger question.

## Strategic Objections

### 1. The "consumer-identity generality" framing overpromises

The memo frames the core question as:

> is the transient substrate still effectively special-cased to one proof-only consumer identity, or can analyzer admission/adaptation truth survive one additional admitted proof-only consumer key

But the actual code change required is adding one entry to a hard-coded Python dict:

```python
# src/presenter/compose_from_intent.py:158-179
_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS = {
    "the-critic": frozenset({...}),
    "aoi-canary": frozenset({...}),
    "transient-proof-harness": frozenset({
        _HANDOFF_KIND_DIRECT_SECTIONS,
        _HANDOFF_KIND_SOURCE_SELECTION,
    }),
    # proposed: add "transient-proof-probe" with same frozenset
}
```

This proves that a manually curated allowlist can have N+1 entries. It does not prove that admission is generic, data-driven, or structurally extensible. The consumer JSON definitions in `src/consumers/definitions/` are loaded by `ConsumerRegistry` but that registry is **not the admission authority** for transient compose routes. Admission is a code-level allowlist, not a contract-level gate.

**Strategic concern**: Under the distilled roadmap's Rule 2 ("a bounded proof is useful only if it teaches or ratifies a reusable substrate"), this slice is marginal. It does not ratify a reusable admission substrate. It ratifies that someone can edit a dict. The honest framing should be: "the allowlist is not coupled to exactly one proof-only key" rather than "consumer-identity generality."

### 2. With identical renderer surfaces, the "adaptation" part of "admission/adaptation" is vacuous

The memo proposes the new consumer use "the same renderer capability surface as `transient-proof-harness`." I verified the adaptation path:

- `src/presenter/manifest_builder.py:105-128`: `adapt_renderer_for_consumer` only does meaningful work when the consumer **lacks** a requested renderer (fallback to `raw_json`).
- `src/consumers/definitions/transient-proof-harness.json:6-17`: supports `accordion`, `card_grid`, `tab`, `raw_json` plus four sub-renderers.

If the new consumer mirrors this surface exactly, the adaptation function returns the same renderer unchanged for every view in both proof cases. Zero new adaptation behavior is tested. The word "adaptation" in the scope title is technically accurate (the function runs) but substantively empty (it never adapts).

### 3. This is correct as "next smallest" only because lifecycle is demonstrably larger

The Codex audit correctly identifies the tradeoff at its finding #6:

- The compose-session save/fetch contract is typed around `ComposeFromIntentRequest` (`src/presenter/schemas.py`, `src/presenter/compose_session_store.py`).
- A lifecycle proof over `source_selection` would require widening that contract to also cover `ComposeFromSelectionRequest`.
- That is a larger change with cross-cutting schema implications.

I verified this independently. The compose session store only handles `ComposeFromIntentRequest`-shaped payloads. So lifecycle truly is the next larger step. The proposed slice wins on size, not on substance. The memo should acknowledge this tradeoff.

## Implementation Corrections

### 4. The memo should name the actual admission seam explicitly

The memo says:

> transient admission is still hard-coded in `src/presenter/compose_from_intent.py`

This is correct but underspecified. The actual seams are:

- `compose_from_intent.py:158-179`: `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` dict
- `compose_from_intent.py:180-183`: `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER` dict (must NOT include the new key)
- `compose_from_intent.py:565-585`: `get_transient_handoff_capability_error()` enforcement function

The implementation must touch exactly these three points (add to the first, explicitly exclude from the second, and the third gates automatically).

### 5. Acceptance bar items 2 and 8 need tightening

Item 2 says:

> analyzer-v2 still blocks the new proof-only consumer on `source_profile`

This is necessary but should be strengthened to require:

- the new consumer key is **absent** from `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`
- a test explicitly proves `get_transient_handoff_capability_error(consumer_key="transient-proof-probe", handoff_kind="source_profile", ...)` returns a rejection message
- `source_backed_readiness` also returns blocked for the new key on `source_profile` (this chains through the same gate function, but should be tested)

Item 8 says the render law should be preserved. This is correct but should also explicitly require that the observed consumer_key in each response matches the new key, not the old one. Identity propagation is the actual thing being tested.

### 6. The harness-side acceptance bar needs more precision

The memo says:

> the same standalone harness can successfully exercise both consumer identities without code branching by workflow beyond the existing fixture-kind dispatch

But the current harness has:

- `App.tsx:36`: `const CONSUMER_KEY = 'transient-proof-harness'` (hard-coded)
- `App.tsx:84-87`: identity assertion against that constant
- Fixtures with hard-coded `consumer_key` in the pinned requests

The acceptance bar should explicitly require:

- harness supports consumer selection (URL param, dropdown, or similar)
- fresh fixtures under the new consumer key with identical analytical content (same `planning_decision_id`, same `workflow_key`, same `source_v2_job_id` where applicable)
- the harness identity assertion dynamically matches the selected consumer
- all other proof metadata (expected root renderer, expected raw-json leaf set) stays identical across consumer keys

## Wording/Documentary Corrections

### 7. The title "consumer-identity generality" is too strong

The slice proves consumer-identity plurality on the proof-only line, not generality. "Generality" implies a structural property (any consumer can be admitted by contract). What this proves is that a second specific consumer was manually admitted and worked. A more honest title would be:

> "Phase E Transient Consumer Identity Plurality on the Proof-Only Line"

or simply:

> "Phase E Second Proof-Only Consumer Key"

### 8. The "Recommended Next Claim" section should be more modest

The memo says:

> analyzer transient admission/adaptation is not coupled only to one proof-only consumer identity; the same minimal harness can carry two proof-only consumer keys over the same AOI and non-AOI transient seams

This is acceptable but should drop "adaptation" from the claim (see objection #2). The honest claim is about admission and end-to-end identity propagation, not adaptation.

### 9. The distilled strategic roadmap has a stale subsection

`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:256-260` still mentions "next bounded slice should be: broaden the same second consumer to the remaining AOI `source_profile` preset surface" under the Phase E current status. This is stale (that work was completed in an earlier slice). If the memo references the distilled roadmap as authoritative, it should note this documentary lag. The Codex audit also flagged this at its finding #7.

## Alternative Step Consideration

I considered whether a different narrower/stronger step should come first. The candidates:

1. **Same slice but with a deliberately different renderer surface** (e.g., omit `tab` support to force adaptation fallback). This would actually test adaptation law but adds implementation complexity beyond the current scope.

2. **Move transient admission from hard-coded dicts to consumer-definition-driven lookup.** This would make the consumer JSON the admission authority. But this is borderline "generic consumer registry refactor" which the memo explicitly excludes, and the honest decision rule would trigger.

3. **Lifecycle on the proof-only line.** Demonstrated above to be larger due to compose-session contract widening.

4. **Source-profile broadening on the proof-only harness.** Explicitly excluded and honestly so; `source_profile` on a proof-only harness would need readiness widening.

None of these is clearly smaller while being stronger. The proposed slice is the smallest next step. It is just not a very strong one.

## Verdict Detail

**Approve with corrections** because:

- The slice correctly identifies the remaining anti-coupling variable on the proof-only line.
- The alternatives are demonstrably larger in the current codebase.
- The scope boundaries are clean: same harness, same routes, same renderer surface, same proof cases, only consumer identity varies.
- The fail-closed story on `source_profile` is structurally honest given the current gate code.

But the memo must:

1. Replace "consumer-identity generality" with "consumer-identity plurality" or "second proof-only consumer key" throughout.
2. Drop "adaptation" from the claim unless the new consumer uses a deliberately different renderer surface.
3. Name the actual code-level admission seams (`_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS`, `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`, `get_transient_handoff_capability_error`).
4. Add acceptance criteria for explicit `source_profile` gate tests and readiness gate tests under the new key.
5. Add acceptance criteria requiring the harness parameterizes consumer identity while keeping all other analytical variables fixed.
6. Acknowledge that this is the smallest next step but not the strongest, and that lifecycle on the proof-only line is a more substantive future step.
7. Note the stale subsection in the distilled strategic roadmap.

## Verification

I verified the following code-level facts independently:

- `src/presenter/compose_from_intent.py:158-179`: consumer admission is a hard-coded dict, not driven by consumer JSON definitions
- `src/presenter/compose_from_intent.py:180-183`: `source_profile` is only registered for `the-critic` and `aoi-canary`
- `src/presenter/compose_from_intent.py:565-585`: enforcement function gates on both dicts
- `src/consumers/definitions/transient-proof-harness.json`: renderer surface matches `aoi-canary`
- `src/analysis_products/source_backed_readiness.py:26-28`: readiness imports and calls `get_transient_handoff_capability_error` for its admission gate
- `/home/evgeny/projects/transient-proof-harness/src/App.tsx:36,84-87`: harness hard-codes consumer identity and asserts on response
- `/home/evgeny/projects/transient-proof-harness/src/lib/transientClient.ts`: structurally generic compose client, not consumer-coupled
- `tests/test_transient_proof_harness_contract.py`: both proof bundles verified against current contract truth
