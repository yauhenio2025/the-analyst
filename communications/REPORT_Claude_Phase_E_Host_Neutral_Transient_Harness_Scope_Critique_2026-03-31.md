# Critique: Phase E Host-Neutral Transient Harness Scope

Date: 2026-03-31
Reviewer: Claude Opus 4.6 (1M context)
Memo Under Review: `communications/MEMO_2026-03-31_phase_e_host_neutral_transient_harness_scope.md`

## Verdict

**Approve with corrections**

The memo correctly identifies the next honest Phase E variable and proposes a bounded, well-scoped slice. The strategic alignment with the distilled roadmap is exact. The two proof cases are the right minimal pair. The decision to keep `consumer_key = aoi-canary` fixed is defensible.

The corrections below address one structural honesty gap, one missing acceptance boundary, and one strategic framing adjustment.

---

## Highest-Signal Findings

### 1. The memo conflates "host-neutral generality" with "different UI shell" — and should be honest about it

This is the most important finding.

The memo frames this harness as proving "host-neutral generality" for the analyzer transient substrate. But the actual analyzer-side generality was already proved by the representative composition matrix (Phase E slice 1) and the aoi-canary second-consumer line (Phase E slices 2-5). The transient compose routes already serve any HTTP caller that sends the correct request shape — they have no knowledge of which UI shell is calling them.

What this harness actually proves is:

- the consumer-side client patterns (fixture loading, compose dispatch, response normalization, structural validation, tab/non-tab rendering) are reusable across UI shells
- the `aoi-canary` shell is not smuggling hidden host-local intelligence through its AOI-branded infrastructure

That is a real and worthwhile proof. But calling it "host-neutral generality" is slightly misleading because it suggests the analyzer side is being tested for a new kind of generality, when in reality the analyzer side stays completely untouched.

**Correction needed**: The memo should be explicit that this harness primarily validates consumer-side pattern reuse and proves that the aoi-canary shell is not hiding host-local analytical intelligence behind its app infrastructure. The analyzer-side generality claim is already closed by earlier slices.

### 2. The existing `transientClient.ts` is already a host-neutral library — the memo should acknowledge this

Codebase evidence: `aoi-canary/src/lib/transientClient.ts` is a pure function library. Every function in it is stateless and host-agnostic:

- `composeFromSelection()` — pure HTTP call, no shell dependency
- `composeFromIntent()` — pure HTTP call, no shell dependency
- `normalizeTransientPresentation()` — pure data transformation
- `validateTransientProofSurface()` — pure structural validation
- `collectRawJsonLeafKeys()` — pure tree walk

Similarly, `RendererHost.tsx` dispatches based on `renderer_type` with no AOI-specific logic. `TabShell.tsx` renders tab-rooted views generically.

A new harness will essentially either import or re-implement these same generic patterns. The memo should acknowledge that the client-side infrastructure is already structurally host-neutral and that the harness proves this fact by extraction, not by inventing new generality.

**Correction needed**: Add one sentence acknowledging that `transientClient.ts` is already structurally host-neutral, and that the harness proves that fact by demonstrating reuse outside the aoi-canary Vite/React shell — not by creating a new client abstraction.

### 3. Missing technology-boundary acceptance criterion

The memo says the harness should be "small, explicit, proof-oriented, structurally generic at the render boundary." It says it should NOT be "a polished product app, a third long-lived consumer architecture, an extension of aoi-canary, or another the-critic proof page."

But it does not say what the harness IS at a technology level. This matters because the honest proof value depends heavily on the implementation boundary:

- If the harness is a copy of aoi-canary with the logo removed → proof theater
- If the harness is a standalone HTML page with vanilla JS that calls the same APIs → strong proof
- If the harness is a minimal React app that imports the renderer package but nothing from aoi-canary → moderate proof

**Correction needed**: Add one acceptance criterion specifying the technology boundary — something like: "The harness must not import code from the aoi-canary repository. Client-side patterns may be independently reimplemented or extracted into a shared utility, but the harness must build and run without any aoi-canary dependency."

### 4. The `consumer_key = aoi-canary` decision is correct but should note the trade-off

Keeping `consumer_key = aoi-canary` is the right call for this slice. It isolates the variable to the proof vehicle without simultaneously widening consumer registration. The consumer adapter registration in `compose_from_intent.py:166-172` already admits `aoi-canary` for all three handoff kinds, so no analyzer-side changes are needed.

But the memo should note that this means the harness does NOT test whether a genuinely new consumer identity works — that remains an unresolved Phase E question for a later slice. Right now `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` in `compose_from_intent.py:158-173` has exactly two registered consumers (`the-critic` and `aoi-canary`). Proving a third consumer key would be a strictly stronger test, but it is correctly deferred here.

**No correction needed** — just flagging this as the next unresolved variable after this harness slice.

### 5. The two proof cases are the correct minimal pair

The memo's choice of `source_selection` and `direct_sections` is well-justified:

1. They use different compose routes: `compose-from-selection` vs `compose-from-intent`
2. They produce different root renderers: `tab` vs `card_grid`
3. They have different raw-json leaf profiles: one leaf vs empty set
4. They are backed by fresh proof bundles with mechanical verification:
   - `PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-31.json` confirms `tab` root with one raw-json leaf
   - `PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.json` confirms `card_grid` root with empty raw-json set

This is the smallest honest AOI + non-AOI pair that covers both compose routes and both major page-shape classes. Adding `source_profile` would add a third compose route but not a new root-renderer shape, so it is correctly excluded.

### 6. No stale assumptions detected in the codebase claims

The memo's codebase claims check out:

- `aoi-canary` consumer registration is open for `direct_sections`, `source_profile`, and `source_selection` — confirmed at `compose_from_intent.py:166-172` ✓
- `ComposeFromSelectionRequest` and `ComposeFromIntentRequest` schemas exist — confirmed at `schemas.py:669` and `schemas.py:613` ✓
- The two compose routes exist — confirmed by the live proof artifacts ✓
- Planning-backed truth with persisted `planning_decision_id` exists — confirmed in both proof bundles ✓
- `aoi-canary` already renders `tab` roots through `TabShell` and non-`tab` roots directly through `RendererHost` — confirmed at `App.tsx` and component source ✓

### 7. Alignment with anti-drift rules

Applying the distilled roadmap's four anti-drift questions:

1. "Does this move intelligence upstream into analyzer-v2?" — No. The analyzer side stays unchanged.
2. "Does this reduce host-specific analytical behavior?" — Indirectly. It proves the existing host behavior is already generic enough to reuse.
3. "Does this strengthen generic law rather than one more special case?" — Yes, by extraction. It proves the client patterns are reusable.
4. "Does this help eventual contract-based generality?" — Marginally. It validates the existing contract surface is sufficient for a minimal standalone consumer.

Score: 2/4 clearly affirmative, 2/4 indirectly affirmative. This is acceptable for a consumer-side proof slice but not as strong as a slice that adds new analyzer-side generality. The memo should be honest about this.

---

## Summary of Required Corrections

1. **Reframe the generality claim**: Acknowledge explicitly that this harness proves consumer-side pattern reuse and host-independence of the aoi-canary shell, not new analyzer-side generality. The analyzer transient compose substrate already serves any HTTP caller generically.

2. **Add technology-boundary acceptance criterion**: The harness must not import from or depend on the aoi-canary repository. This prevents "proof theater" where the harness is just a reskinned copy of the existing app.

3. **Acknowledge existing host-neutrality of transientClient.ts**: Note that the client-side patterns in `transientClient.ts`, `RendererHost.tsx`, and `TabShell.tsx` are already structurally host-neutral. The harness proves this by demonstrating reuse, not by inventing new patterns.

---

## Strategic Assessment

**Is this the right next move?**

Yes. The distilled roadmap, state-of-play memo, and recent completion memos all explicitly name this as the next bounded Phase E variable. The five completed Phase E slices proved composition matrix generality, second-consumer serving, AOI route broadening, and non-AOI path inside the AOI-branded shell. The only remaining Phase E question before the program moves to broader consumer-identity or engine-family generality is whether the current proof is coupled to the aoi-canary app shell itself.

**Should a narrower step come first?**

No. This is already narrow — one harness, two cases, fixture-backed only, no analyzer changes.

**Should a stronger step come instead?**

A case could be made for jumping directly to a new `consumer_key` registration (e.g., `proof-harness`) to test actual consumer-identity generality at the analyzer level. That would be strictly stronger. But it would vary two things at once (proof vehicle + consumer identity), and the memo's argument for isolating variables is sound.

The recommended path is: complete this harness slice, then immediately follow with a slice that registers a new `consumer_key` and replays the same fixtures through it. Together, those two slices would close the Phase E host-neutral generality gap.

---

## Verdict Restatement

**Approve with corrections.** The scope is right. The variable isolation is right. The proof cases are right. The three corrections above (reframe the generality claim, add technology-boundary acceptance, acknowledge existing host-neutrality) will make the memo's honesty match its ambition.
