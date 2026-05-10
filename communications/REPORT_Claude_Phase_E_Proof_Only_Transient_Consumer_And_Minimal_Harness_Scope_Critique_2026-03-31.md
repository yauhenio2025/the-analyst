# Critique: Phase E Proof-Only Transient Consumer And Minimal Harness Scope

Date: 2026-03-31
Reviewer: Claude (Opus 4.6)
Memo Under Review: `communications/MEMO_2026-03-31_phase_e_host_neutral_transient_harness_scope.md`
Verdict: **Approve with corrections**

## Summary Verdict

The proposed scope is the right next bounded step for Phase E. It correctly identifies the remaining honest gap: the transient substrate has been proved on two different consumer identities but both are hosted inside app shells that were either purpose-built for a specific workflow or carry AOI-branded assumptions. Varying the proof vehicle to one proof-only consumer contract plus a minimal harness is the smallest step that tests whether the dependency is the shell or the consumer contract itself.

The memo's core logic is sound, but it contains several assumptions that need correction, one misleading framing, and two missing acceptance criteria.

---

## Finding 1: The admission logic is already fully open — the memo overstates the analyzer-side contract change

**Issue**: The memo states the scope should "add one proof-only transient consumer definition and admit it only on `source_selection` and `direct_sections`" and explicitly says the new consumer should "stay fail-closed on `source_profile`."

**Codebase reality**: The admission gate in `compose_from_intent.py:148-177` is governed by `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` and `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`. Adding a new consumer to these dicts is a one-line-per-dict change. The memo correctly identifies this is a narrow analyzer-side change.

However, the memo should be explicit that this is a dict entry, not a consumer definition file. The consumer definition file in `src/consumers/definitions/` (like `aoi-canary.json`) is consumed by `ConsumerRegistry` for renderer capability lookups, not by the transient compose admission gate. These are two separate registration systems:

- `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` (Python dict in `compose_from_intent.py`) — governs transient compose admission
- `src/consumers/definitions/*.json` — governs renderer capability declarations

The scope should be explicit about whether the proof-only consumer needs both or only the transient compose admission dict entry.

**Correction needed**: State that the new `transient-proof-harness` consumer needs an entry in `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` scoped to `{direct_sections, source_selection}` only, and clarify whether a `transient-proof-harness.json` consumer definition file is also needed (it likely is, since the compose route passes `consumer_key` to `adapt_renderer_for_consumer` which reads from ConsumerRegistry).

**Severity**: Medium. If the harness sends `consumer_key=transient-proof-harness` and no consumer definition file exists, `adapt_renderer_for_consumer` may fall through to defaults or error. This needs to be designed explicitly.

---

## Finding 2: The "no `source_profile` admission" constraint is correctly scoped

**Verification**: The `_SUPPORTED_HANDOFF_KINDS` dict at line 148-157 already limits `intellectual_genealogy` to `direct_sections` only. The admission gate at line 572-574 checks both the consumer adapter dict and the workflow-level handoff dict. So even if the new consumer were accidentally given all three handoff kinds, the workflow-level gate would still block `source_profile` on genealogy. For AOI, `source_profile` would only pass if the new consumer were registered in `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`.

The fail-closed discipline here is structurally enforced. The memo's constraint is correct.

---

## Finding 3: The "structurally generic" claim about aoi-canary utilities is accurate

**Verification**: I inspected:

- `transientClient.ts` — The `composeFromSelection()`, `composeFromIntent()`, `normalizeTransientPresentation()`, and `validateTransientProofSurface()` functions are genuinely parameterized on fixture identity and response shape. They carry no AOI-specific semantic logic.
- `RendererHost.tsx` — A pure `renderer_type → Component` dispatch map. No workflow awareness.
- `TabShell.tsx` — A pure tab container driven by `renderer_config`. No workflow awareness.
- `App.tsx:1196-1209` — The render path branching is: `rootView.renderer_type === 'tab' ? <TabShell> : <RendererHost>`. This is structurally generic.

The memo's claim that the new harness should treat these as "proof of reusable pattern shape, not as a dependency" is honest and correctly stated. The technology boundary (no imports from `aoi-canary`) is the right constraint.

---

## Finding 4: The fixture-backed-only constraint is correctly bounded

**Verification**: The existing proof bundles at:

- `PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json`
- `PROOF_phase_e_transient_second_consumer_aoi_canary_genealogy_direct_sections_2026-03-31.json`

...contain full `request_json` payloads that can be trivially adapted (changing `consumer_key` from `aoi-canary` to `transient-proof-harness`). The memo correctly identifies these as fixture lineage anchors.

The constraint "must not fetch planning decisions, fetch analyzer lowering routes, discover results, derive requests locally, or reconstruct planner truth" is correct for a proof-only harness.

---

## Finding 5: Missing acceptance criterion — consumer_key in response must match

**Issue**: The memo lists acceptance criteria about root renderer types and raw-json leaf sets, but does not mention that the compose response will carry `consumer_key` and the harness should verify it matches the new proof-only identity.

**Correction needed**: Add one acceptance criterion:
- the compose response `presentation.consumer_key` must equal `transient-proof-harness`, not `aoi-canary` or `the-critic`

This is important because `adapt_renderer_for_consumer` may affect the response shape based on consumer identity.

---

## Finding 6: Missing acceptance criterion — the harness must prove both compose routes, not just rendering

**Issue**: The memo's acceptance criteria focus on rendering outcomes (root renderer, raw-json leaf set) but do not explicitly require proving that both compose routes (`compose-from-selection` and `compose-from-intent`) return 200 under the new consumer identity before rendering.

**Correction needed**: Add explicit acceptance criteria:
- `POST /v1/presenter/compose-from-selection` with `consumer_key=transient-proof-harness` returns 200 on the AOI source_selection fixture
- `POST /v1/presenter/compose-from-intent` with `consumer_key=transient-proof-harness` returns 200 on the genealogy direct_sections fixture
- a request with `consumer_key=transient-proof-harness` and `handoff_kind=source_profile` is rejected (fail-closed proof)

---

## Finding 7: The memo correctly avoids strategic drift

Checked against the distilled strategic roadmap anti-drift rules:

1. **Upstream intelligence over downstream convenience**: This slice moves intelligence upstream (one more proof-only consumer contract in analyzer-v2). The harness is deliberately thin. Pass.

2. **Bounded proof teaching reusable substrate**: This slice tests whether the substrate already generalizes beyond the two existing shells. If it does, that is a reusable finding. Pass.

3. **Governance vs architecture**: This is architecture, not governance. Pass.

4. **Representative matrix over exhaustive theater**: This slice reuses the same two already-proved paths rather than adding new paths. It varies the consumer/vehicle instead of the content. That is the right matrix-broadening dimension. Pass.

---

## Finding 8: The "proof-only" framing slightly understates what will be proved

**Observation**: The memo repeatedly calls the harness and consumer "proof-only" and emphasizes it is not a product. This is correct as a scope boundary. However, the reader should understand that what is being proved is non-trivially strong:

- if the same transient substrate serves two different consumer identities through two different compose routes in a harness that shares zero code with either existing shell, the remaining coupling is genuinely only the consumer definition plus the HTTP contract

That is actually a significant Phase E generality finding, not merely a "proof artifact."

The memo should not change its scope, but it should acknowledge in the "Why this is the next honest broader variable" section that a successful proof here would be substantially stronger evidence for the "analyzer-v2 as the brain" thesis than any of the previous five Phase E slices individually.

---

## Finding 9: The technology boundary is correctly stated

The memo explicitly states: "the new harness must not import from or depend on the `aoi-canary` repo."

This is the right boundary. The harness may reimplement structurally similar patterns (fetch, normalize, validate, dispatch to renderer by type) but must not share code with `aoi-canary`.

---

## Finding 10: Minor phrasing correction — "one proof-only transient consumer contract plus one minimal harness" is long

**Observation**: The phrase "one proof-only transient consumer contract plus one minimal harness" appears 15+ times in the memo. This is accurate but creates readability friction. Consider introducing a shorthand (e.g., "the proof-harness slice") early and using it consistently.

This is a style note, not a correctness finding.

---

## Corrections Required Before Implementation

1. **Clarify dual registration**: Explicitly state whether `transient-proof-harness` needs only a `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` entry or also a `src/consumers/definitions/transient-proof-harness.json` consumer definition file. If both, define the minimal renderer surface for the consumer definition (likely: `accordion`, `card_grid`, `tab`, `raw_json` — same as `aoi-canary`).

2. **Add consumer_key response verification**: The harness must verify that `presentation.consumer_key` in the compose response equals `transient-proof-harness`.

3. **Add explicit compose route acceptance criteria**: Both compose routes must return 200 under the new identity. A `source_profile` request must be rejected.

4. **Clarify the strength of the finding**: Acknowledge that a successful proof-harness slice substantially strengthens the Phase E generality claim beyond any individual previous slice.

---

## Should a narrower step come first?

**No.** The proposed scope is already narrow. The two candidate narrower alternatives would be:

1. **Only the analyzer-side consumer contract, no harness** — This would only prove admission, not rendering. It would leave the "is it the shell or the contract?" question unanswered. Not worth doing alone.

2. **Only one of the two cases (just genealogy or just AOI)** — This would reduce the proof to a single compose route, losing the two-route diversity that makes the finding meaningful. Not worth splitting.

The proposed scope — one consumer + one harness + two cases — is already the minimal honest unit.

---

## Final Assessment

The memo proposes the right next step. It is strategically aligned, correctly bounded, and honest about what it claims and what it does not. The four corrections above should be incorporated before implementation, but none of them change the scope or direction.

**Verdict: Approve with corrections.**
