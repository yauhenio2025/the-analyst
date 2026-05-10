# Approve with corrections

The proposed `aoi-canary` / AOI `source_profile:comparison` slice is the right next bounded Phase E move, but the memo is slightly too optimistic about how little real work remains in the canary repo and slightly too loose about the exact proof shape that has to stay honest.

Strategically, the memo is aligned with the current roadmap, not drifting from it. The distilled roadmap explicitly says the next bounded Phase E slice should broaden the same second consumer to the remaining AOI `source_profile` preset while preserving truthful readiness law (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:26-71`, `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:122-129`). The state-of-play memo says the current remaining bounded limitation is exactly that `aoi-canary` is still dossier-only on `source_profile` (`communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:182-220`). That fits the broader program direction as well: the canonical roadmap still wants thin hosts and analyzer-owned composition, while warning that the real unsolved problem is upstream planning/bridging, not endless AOI-local app work (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:43-68`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:112-120`).

## High-signal findings

1. The memo’s core assumption is correct: the remaining analyzer-side blocker is explicit consumer/profile gating, not missing AOI source feasibility.

- `ComposeFromSourceRequest` already supports both `dossier` and `comparison` at the contract level in `src/presenter/schemas.py:624-666`.
- The AOI source bridge already defines both presets, and `comparison` is not a speculative future preset. It is a live preset selecting `engagement_mapping`, `sin_findings`, and `thematic_report` in `src/presenter/composition_source_bridge.py:72-102`.
- The actual blocking seam is the consumer-profile gate in `src/presenter/compose_from_intent.py:173-176`, enforced through `get_transient_handoff_capability_error()` and `_validate_source_request()` in `src/presenter/compose_from_intent.py:558-626`.
- The current tests lock that fail-closed behavior in place for `aoi-canary` + `profile='comparison'` in `tests/test_compose_from_intent.py:990-1001`.

I also validated the pinned source job directly in the local repo. `resolve_source_catalog('job-744edf255ad5')` returns all four AOI source families as `available`, with `plan_source_mismatches=[]`, and `evaluate_compose_profile_feasibility(...)` returns `['dossier', 'comparison']`. So the pinned-job assumption is robust: today, `comparison` is blocked for `aoi-canary` by policy, not because the job cannot support it.

2. Readiness truth is already mechanically tied to that same gate, so broadening route truth and readiness truth together is the right bounded move.

- AOI readiness resolves real catalog feasibility first, then applies the same transient handoff capability gate through `get_transient_handoff_capability_error()` in `src/analysis_products/source_backed_readiness.py:127-165`.
- The current readiness contract for `aoi-canary` therefore exposes `allowed_selectors=['dossier']` and blocks `comparison` only because the consumer gate still rejects it in `src/analysis_products/source_backed_readiness.py:167-199`.
- The current readiness tests lock that exact state in `tests/test_source_backed_readiness.py:264-289`.

That means the memo is right to keep presenter and readiness in the same slice. If only `compose-from-source` broadens, the repo immediately becomes internally stale again.

3. The canary surface is bounded, but the memo understates the hidden coupling inside `App.tsx`.

- The shared transient client is already generic enough for this slice. `composeFromSourceRequestPayload` already supports `'dossier' | 'comparison'`, and `normalizeTransientPresentation()` already derives identity from `source_v2_job_id + profile` in `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:20-27`, `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:118-151`.
- But the app shell is still two-case-specific, not truly open-ended within `request_kind='source_profile'`:
  - the proof-case union is only `'source_selection' | 'source_profile_dossier'` in `/home/evgeny/projects/aoi-canary/src/App.tsx:37-38`
  - the fixture imports and case map only know the dossier fixture in `/home/evgeny/projects/aoi-canary/src/App.tsx:7-8`, `/home/evgeny/projects/aoi-canary/src/App.tsx:180-188`
  - status/copy logic assumes every non-selection source-profile case is dossier in `/home/evgeny/projects/aoi-canary/src/App.tsx:363-430`
  - the proof selector UI iterates only those two keys in `/home/evgeny/projects/aoi-canary/src/App.tsx:1040-1058`
- Test coverage is equally two-case-specific:
  - only selection and dossier fixtures are imported in `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:5-7`
  - only selection and dossier proof flows are exercised in `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:233-350`
  - only selection and dossier transient normalization/proof-surface tests exist in `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts:3-4`, `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts:166-233`

So this is still the right next slice, but the memo should not describe it as if adding one fixture and one allowlist entry is the whole story. The real bounded work is still small, but it spans analyzer gate, readiness truth, canary case plumbing, copy, and tests.

4. The comparison proof surface is not identical to dossier, and the memo should name that explicitly.

- The source-profile comparison preset is a three-section shape, not the two-section dossier shape, in `src/presenter/composition_source_bridge.py:85-100`.
- The existing comparison tree proof already shows the expected AOI comparison structure on `compose-from-source-v3`: tab parent, `engagement_mapping`, `sin_findings`, and `thematic_report`, with `view_count=4` and report closeout as `compose_intent_03_aoi_thematic_report` in `communications/PROOF_stage11_comparison_tree_2026-03-24.json:8-146`.
- `aoi-canary` supports `tab`, `card_grid`, `accordion`, and `raw_json`, but not `prose`, in `src/consumers/definitions/aoi-canary.json:6-17`.
- Unsupported renderers are adapted to `raw_json` when the consumer supports it in `src/presenter/manifest_builder.py:105-135`.

So the slice remains mechanically safe, but the proof expectation is not just “same as dossier with a different profile.” The new fixture/test/proof bundle should pin the expected closeout fallback leaf for the comparison shape, which is likely `compose_intent_03_aoi_thematic_report`, not the dossier leaf `compose_intent_02_aoi_thematic_report`.

5. The memo is strategically sound only if it is treated as closure of the current AOI second-consumer family, not as justification for more AOI-local accretion after this.

- The larger roadmap still says the durable target is analyzer-owned composition with minimal host intelligence, not one AOI proof after another (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:26-52`, `communications/DYNAMIC_BESPOKE_APPS_VISION.md:13-42`).
- The canonical roadmap also says the hard remaining problem is upstream planning/orchestration and bridge generalization, not more current-app smarts (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:112-120`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:163-179`).
- The original orchestrator vision says the long-term gap is context-driven engine/sequence/view choice upstream, not user- or app-side workflow intelligence in the host (`docs/MEMO_2026-02-19_orchestrator_vision.md:33-61`).

So this slice is justified because it closes the remaining preset-level gap inside an already-open AOI second-consumer family. It would become drift if it turned into broader AOI canary intelligence, more consumer-local launch logic, or a new round of AOI-only productization after `comparison` parity closes.

## Corrections needed in the memo

1. Tighten the canary-side scope statement.

The memo should say explicitly that the comparison slice still includes:

- one new comparison fixture
- one third proof-case key in `/home/evgeny/projects/aoi-canary/src/App.tsx`
- copy/status-message generalization so source-profile cases are not dossier-hardcoded
- focused canary test expansion in both `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx` and `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts`

That keeps the scope honest without widening into any new host architecture.

2. Add a concrete analyzer regression criterion, not only a generic “proof paths remain intact” criterion.

The memo should explicitly require:

- updating the current fail-closed analyzer test in `tests/test_compose_from_intent.py:990-1001`
- updating the current readiness blocker test in `tests/test_source_backed_readiness.py:264-289`
- preserving explicit fail-closed coverage for unsupported combinations after `comparison` becomes allowed

Right now the acceptance bar gestures at this, but the existing repo makes the exact regression seams visible enough to name them.

3. Tighten the proof-surface acceptance bar to the exact comparison closeout leaf.

The current acceptance bar says “at most one `raw_json` leaf” and “report leaf only,” which is directionally right but less precise than the actual proof harness. Because the canary proof law is fixture-driven, the memo should require the new comparison fixture to pin the exact expected `raw_json` leaf key and the tests to validate that exact set, just as the current harness already does.

4. Keep the readiness naming decision explicit and intentional.

The memo already chooses to keep `selector_lifecycle_phase="source_selection"`. That is a reasonable bounded choice, but it should say more directly that this is a deliberate semantic compromise in v1, not a naturally self-explanatory name for the `source_profile` path. Otherwise later readers may misread it as stale terminology rather than an intentional bounded decision.

5. Make the post-slice strategic boundary explicit.

After this slice, the memo trail should say plainly that the current AOI `source_profile` second-consumer family is closed in bounded form and that the next move should not be another AOI-local proof unless it teaches a stronger cross-workflow or upstream generalization lesson.

## Verdict on next step

Approve with corrections.

I do not see a stronger narrower slice that should come first. The matrix proof already answered “does the current transient substrate support this route family on the current consumer surface?” The March 31 live proofs already answered “can one real second consumer consume `source_selection` and then bounded `source_profile:dossier` without host-local analytical reconstruction?” The remaining bounded question is exactly the one this memo names:

- can the same second consumer close the remaining AOI `source_profile` preset gap, with analyzer-owned source reconstruction and truthful readiness semantics, without making the canary analytically smart?

That is the right next bounded Phase E step.

The only correction is to describe it as what it really is:

- parity closeout for the existing AOI `source_profile` second-consumer family
- not a new architecture milestone
- not a reason to keep growing AOI-specific app behavior after this parity closes
