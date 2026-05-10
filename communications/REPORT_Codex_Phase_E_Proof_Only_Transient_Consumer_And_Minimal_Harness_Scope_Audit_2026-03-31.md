# Report: Phase E Proof-Only Transient Consumer And Minimal Harness Scope Audit

Verdict: Approve with corrections

The memo now points at the right next broader Phase E variable. After the representative matrix and the full bounded `aoi-canary` second-consumer proof line, the remaining honest gap is no longer another route widening inside the AOI-branded shell. It is whether the same transient substrate can survive one distinct proof-only consumer contract plus one minimal standalone harness over the smallest honest AOI plus non-AOI pair.

## Highest-Signal Findings

### 1. The memo names the right next broader Phase E question.

This is consistent with the current roadmap stack and with the current repo state.

- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md` already closes the same-consumer matrix over `source_profile`, `source_selection`, and `direct_sections`.
- `communications/MEMO_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion.md` already closes the bounded non-AOI broadening inside `aoi-canary`.
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Those documents now converge on the same strategic point: the next honest Phase E variable is not more `aoi-canary` route or preset broadening, but one proof-only consumer plus one minimal harness beyond the AOI-branded shell.

### 2. The proposed two-case pair is the right minimal pair.

The memo chooses the strongest bounded pair now available:

- AOI `source_selection`
- genealogy `direct_sections`

That choice is codebase-backed and strategically clean.

- `source_selection` exercises `POST /v1/presenter/compose-from-selection`.
- `direct_sections` exercises `POST /v1/presenter/compose-from-intent`.
- the AOI proof surface returns a `tab` root with one bounded `raw_json` leaf, as frozen in `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json` and live-closed in `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-31.json`
- the genealogy proof surface returns a `card_grid` root with an empty `raw_json` leaf set, as frozen in `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_genealogy_direct_sections_2026-03-31.json` and live-closed in `communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.json`

This pair also avoids reopening `source_profile`, which would drag the slice back into AOI-only preset/readiness coupling. `src/analysis_products/source_backed_readiness.py:147-160` only has follow-up consumer gating for `compose-from-source`, so leaving `source_profile` out is the right scope discipline.

### 3. The memo is right to make the new harness fixture-backed only.

That is not a shortcut. It is the correct variable control for this slice.

The planner/lowering side for genealogy `direct_sections` is already separately proved:

- `src/orchestrator/direct_sections_compose_harness.py:17-79`
- `tests/test_phase1c_genealogy_direct_sections.py:52-173`

So the next question should not reopen planning, lowering, discovery, or saved-result reconstruction. The new slice should isolate consumer-contract and harness reuse only.

### 4. The biggest hidden coupling is analyzer-side consumer admission, not the JSON definition file.

This is the main correction the memo needs to make explicit.

The consumer definition JSON is real, but transient route admission is not sourced from it today:

- `src/presenter/compose_from_intent.py:158-176` hard-codes `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` and `_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER`
- `src/presenter/compose_from_intent.py:567-578` enforces the capability gate at request validation time
- `src/analysis_products/source_backed_readiness.py:147-160` reuses the same gate for AOI source-profile follow-up readiness

So "add one proof-only transient consumer definition" is not, by itself, enough. The honest implementation scope is:

- one new proof-only consumer definition in `src/consumers/definitions/`
- one bounded presenter admission change for exactly `source_selection` and `direct_sections`
- focused negative tests proving the new consumer stays fail-closed for `source_profile`

This is still acceptable as a proof-only slice. It just must not be described as if consumer JSON is already the sole authority for transient admission.

### 5. The memo slightly overstates how generic the current `aoi-canary` host pieces already are.

The `aoi-canary` host proves useful pattern shape, but not a reusable host runtime in the broad sense.

- `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx:10-27` only maps `accordion`, `card_grid`, and `raw_json`
- `/home/evgeny/projects/aoi-canary/src/App.tsx:1203-1209` still owns the top-level `tab` versus non-`tab` branch
- `/home/evgeny/projects/aoi-canary/src/components/TabShell.tsx:19-31` depends on current `renderer_config` conventions such as `tab_labels`, `_section_descriptions`, and `_style_overrides`
- `/home/evgeny/projects/aoi-canary/src/App.tsx:171-199` and `/home/evgeny/projects/aoi-canary/src/App.tsx:850-905` are still explicitly AOI-canary proof-shell code

So the honest phrasing is:

- these files prove a reusable pattern for the current two-case surface
- they do not yet prove a general consumer runtime

That does not block the memo. It just means the new harness should re-implement the minimal local equivalents rather than claiming that the current `aoi-canary` utilities are already a generic package.

### 6. The memo does keep a real technology boundary, but the acceptance bar should make that boundary more explicit.

On the current reading, the proposed boundary is real:

- the new harness must not import from or depend on the `aoi-canary` repo
- the harness should depend only on analyzer HTTP routes, its own local code, and shared renderer package dependencies

That is the right boundary.

But the acceptance criteria should explicitly require all of the following:

- the pinned fixtures use the new proof-only `consumer_key`, not `aoi-canary`
- live HAR evidence shows the new proof-only `consumer_key` on the wire
- the transient response returns that same proof-only `consumer_key`
- `compose-from-source` stays fail-closed for the new proof-only consumer
- the harness performs no planning fetch, lowering fetch, discovery call, or local analytical reconstruction
- the harness has zero code import or build dependency on `/home/evgeny/projects/aoi-canary`

Without those checks, the slice could look broader than it is.

### 7. The memo's claim should stay narrower than its current strongest phrasing.

The narrowest honest claim is:

- one proof-only transient consumer contract plus one minimal standalone harness can replay analyzer-owned request fixtures for one AOI `source_selection` path and one genealogy `direct_sections` path, consume the existing transient response law structurally, and do so without host-local analytical reconstruction or dependency on the `aoi-canary` repo

It should not claim:

- new analyzer-side generality
- generic consumer registration
- broad host-neutral productization
- lifecycle/readiness generality
- or that consumer identity no longer matters in general

## Corrections Needed In The Memo

1. State explicitly that this slice requires both:
- a new proof-only consumer definition
- and a bounded presenter admission change in `src/presenter/compose_from_intent.py`

2. Replace any wording that implies the current `aoi-canary` utilities are already broadly generic.
- They are reusable pattern sketches for this exact two-case surface, not a generic host runtime.

3. Add one explicit fail-closed acceptance criterion:
- the new proof-only consumer must reject `source_profile`

4. Add one explicit identity acceptance criterion:
- fresh fixtures, proof bundles, and live HARs must all carry the new proof-only `consumer_key` end to end

5. Add one explicit repo-boundary acceptance criterion:
- no imports, path references, or build dependency on the `aoi-canary` repo

6. Keep the claim tied to consumer-side pattern reuse and bounded host-independence only.
- Do not imply broader analyzer-side generality from this slice.

## Recommendation

Approve the memo with the corrections above.

No narrower or stronger step needs to come first. The only plausible alternative would be to centralize transient capability admission before adding another consumer, but that would be premature generic consumer architecture work. The bounded proof-only consumer plus minimal harness is the right next move as long as it is documented honestly as:

- one more proof consumer
- one more minimal harness
- two already-proved cases
- no new schema family
- no new route family
- no `aoi-canary` dependency

## Verification

Focused local verification passed against the current repo state:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_source_backed_readiness.py tests/test_aoi_canary_contract.py tests/test_phase1c_genealogy_direct_sections.py`
- result: `57 passed, 2 warnings`
