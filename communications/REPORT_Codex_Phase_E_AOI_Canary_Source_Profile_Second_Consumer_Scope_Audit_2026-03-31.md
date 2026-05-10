# Approve with corrections

The proposed `aoi-canary` / AOI `source_profile` slice is the right next bounded Phase E move, but the memo is slightly too narrow about where the remaining work lives.

At the analyzer boundary, the claimed blocker is real and explicit: `aoi-canary` is still excluded from `source_profile` in `src/presenter/compose_from_intent.py:158-167`, `compose-from-source` still fails closed for that consumer in `src/presenter/compose_from_intent.py:588-597`, and AOI readiness still reports a `the-critic`-only followup blocker in `src/analysis_products/source_backed_readiness.py:144-177`. That matches the memo's main strategic claim. It also fits the current Phase E sequence in the roadmap docs: the representative matrix already proved the full live handoff family on the current consumer surface, and the March 31 closeout already live-proved `aoi-canary` on `source_selection`, so broadening the same second consumer to the remaining AOI family is the smallest honest next variable (`communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`, `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`, `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`).

## High-signal findings

1. The analyzer-side consumer gate is real, explicit, and narrow.

- `src/presenter/compose_from_intent.py:158-167` registers `aoi-canary` only for `source_selection`.
- `tests/test_compose_from_intent.py:836-838` explicitly locks in that `compose_from_source(... consumer_key="aoi-canary")` must currently fail.
- `src/analysis_products/source_backed_readiness.py:147-150` hard-codes the AOI followup blocker string `compose-from-source only supports consumer_key='the-critic' in v1`.
- `tests/test_source_backed_readiness.py:181-204` encodes that blocker as the expected current behavior.

This means the memo is correct that the remaining unresolved analyzer seam is concrete, bounded, and already isolated in code.

2. `dossier` is the right narrower `source_profile` target.

- The frozen `source_profile` matrix bundle already shows the `dossier` route shape is small: one `tab` parent with two children, `accordion` synthesis plus `prose` report closeout (`communications/PROOF_phase_e_matrix_aoi_source_profile_dossier_2026-03-30.json`).
- `aoi-canary` already supports `tab`, `accordion`, and `raw_json` in `src/consumers/definitions/aoi-canary.json:6-17`.
- Unsupported renderers already degrade through the existing consumer adaptation law in `src/presenter/manifest_builder.py:105-135`, which means the only new unsupported leaf on the `dossier` path is the same kind of prose closeout fallback the canary is already built to tolerate.

So the memo is right to choose `dossier` rather than `comparison` as the first `source_profile` proof. `comparison` would widen the proof surface unnecessarily.

3. The memo understates the canary-side implementation surface.

The canary is not currently "one generic transient proof host with a different fixture." It is selection-shaped end to end:

- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:3-85` only defines a `ComposeFromSelectionRequestPayload` and a `composeFromSelection()` client.
- `/home/evgeny/projects/aoi-canary/src/App.tsx:7,14,175,785-800` imports only `transient-aoi-source-selection.json` and always calls `composeFromSelection()` in `transient_proof` mode.
- `/home/evgeny/projects/aoi-canary/src/App.tsx:366,393,935` still describes the proof surface as "source-selection".
- `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts:86-108` and `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:183-229` only assert the `compose-from-selection` route.

So the next slice is still bounded, but it is not just:

- admit `aoi-canary` in analyzer
- remove one readiness blocker
- drop in a new fixture

It also requires a narrow canary-side route client, fixture/plumbing split, copy updates, and test expansion.

4. The readiness contract is slightly staler than the memo admits.

- AOI readiness currently reports `selector_lifecycle_phase="source_selection"` in `src/analysis_products/source_backed_readiness.py:178-210`.
- The schema only allows `source_selection | restore_runtime` in `src/analysis_products/schemas.py:74-124`.

That does not invalidate the proposed slice, but it does mean "remove the `the-critic` blocker string" is not the full truth-preservation task if the memo wants readiness to describe a `source_profile` followup path honestly. Either:

- the memo should explicitly treat profile presets as a bounded form of source selection and keep the current label on purpose, or
- the slice should include a small naming/schema cleanup so the readiness contract does not keep advertising the AOI branch as `source_selection` while the proof claim is specifically `source_profile`.

5. The acceptance bar should explicitly preserve the already-closed `source_selection` proof instead of replacing it.

- The current analyzer proof record is pinned to `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_2026-03-30.json`.
- The current canary proof fixture is pinned to `/home/evgeny/projects/aoi-canary/src/fixtures/transient-aoi-source-selection.json`.
- Existing canary contract tests in both repos assert that exact proof lineage (`tests/test_aoi_canary_contract.py:11-14,103-127`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:183-229`).

So the right bounded move is to add a second proof fixture and proof bundle in parallel, not overwrite the existing `source_selection` evidence path.

## Corrections needed in the memo

1. Expand the scope statement to include the real canary-side work.

The memo should say explicitly that the slice includes:

- one new `compose-from-source` client path or equivalent route switch in `aoi-canary`
- one new pinned `source_profile` fixture
- one narrow `transient_proof` case selector or equivalent proof-mode split
- focused canary test updates for the new route

without broadening into planner integration or generalized host architecture.

2. Tighten the acceptance bar around regression preservation.

Add a criterion that the already-closed `aoi-canary` / `source_selection` proof remains reproducible and test-covered after the new `source_profile` path lands.

3. Tighten the readiness criterion.

Criterion 2 should not only say "the blocker string is gone." It should require that the returned readiness contract is still semantically truthful for the `source_profile` followup path, including any lifecycle-phase naming the implementation decides to keep or update.

4. Make the proof fixture requirement parallel rather than replacement-oriented.

The memo currently gestures in this direction, but it should say plainly that the new `source_profile` proof fixture lives alongside the existing `source_selection` fixture and does not replace it.

5. Keep `dossier` as the first proof target and say why.

The memo should explicitly note that `dossier` is preferred because it is the smallest `source_profile` surface already visible in the frozen matrix proof: synthesis plus report closeout, not the broader three-family comparison surface.

## Verdict on next step

Approve with corrections.

I do not see a stronger narrower slice that should come first. The representative matrix already answered the "does the live substrate support this handoff family on the current consumer surface?" question. The March 31 live closeout already answered the "can one real second consumer consume one AOI transient path without host-local analytical reconstruction?" question. The remaining honest question is exactly the one this memo targets:

- can the same second consumer consume the remaining AOI `source_profile` transient path, with analyzer-owned source reconstruction and truthful readiness semantics, without making the canary analytically smart?

That is the right next bounded Phase E step.

## Calibrated implementation implication

The slice is still small enough to be worth doing now, but it should be described as four coordinated bounded changes, not two:

1. analyzer admission for `aoi-canary` on `compose-from-source`
2. truthful AOI readiness followup behavior for that consumer/path
3. a second pinned canary transient proof path for `source_profile`
4. one new live browser/HAR/screenshot closeout bundle that preserves the earlier `source_selection` proof intact

That framing keeps the memo honest and prevents the next pass from discovering "hidden" work that is already visible in the current repos.
