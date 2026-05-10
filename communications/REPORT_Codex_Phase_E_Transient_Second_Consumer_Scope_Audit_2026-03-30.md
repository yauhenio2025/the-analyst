# Report: Codex Audit Of Phase E Transient Second-Consumer Scope

Scope memo:
- `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`

Related materials reviewed:
- `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

Code reviewed:
- `src/presenter/compose_from_intent.py`
- `src/presenter/manifest_builder.py`
- `src/consumers/definitions/aoi-canary.json`
- `src/consumers/definitions/analyzer-mgmt.json`
- `src/consumers/definitions/visualizer.json`
- `src/consumers/registry.py`
- `src/api/routes/presenter.py`
- `src/analysis_products/source_backed_readiness.py`
- `tests/test_compose_from_intent.py`
- `tests/test_representative_composition_matrix.py`
- `tests/test_aoi_canary_contract.py`
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts`
- `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx`
- `/home/evgeny/projects/aoi-canary/src/test/resultsClient.test.ts`
- `/home/evgeny/projects/aoi-canary/README.md`

Verification run:
- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_representative_composition_matrix.py tests/test_aoi_canary_contract.py`
  - result: `34 passed`
- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
  - result: passed
- `npm --prefix /home/evgeny/projects/aoi-canary run test`
  - result: `13 passed`

## Verdict

`Approve with corrections`

## Bottom Line

This is the right next Phase E slice.
The roadmap stack is internally consistent that the first matrix already answered the handoff-family question on the current transient consumer surface, and that the remaining bounded Phase E variable is consumer-surface generality (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:228-252`, `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:298-330`, `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:186-207`, `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:342-354`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1346-1350`).

The live code agrees with that framing.
The representative matrix is still pinned to `consumer_key == the-critic` in proof and runtime assumptions (`tests/test_representative_composition_matrix.py:31-43`, `tests/test_representative_composition_matrix.py:52-106`, `tests/test_representative_composition_matrix.py:118-147`), and transient compose still hard-gates on one registered consumer adapter (`src/presenter/compose_from_intent.py:54-59`, `src/presenter/compose_from_intent.py:148-158`, `src/presenter/compose_from_intent.py:521-599`).

`aoi-canary` is the right bounded target.
It is the only real existing second consumer already proved on analyzer-owned result contracts (`communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md:11-18`, `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md:150-159`) and its local boundary is intentionally thin (`/home/evgeny/projects/aoi-canary/README.md:5-23`, `/home/evgeny/projects/aoi-canary/README.md:54-68`).

The memo is mostly strategically honest.
The needed corrections are narrower:

- keep `AOI source_selection` as the clear default path
- do not present `source_profile` as an equally cheap fallback
- say explicitly that analyzer-side work is slightly larger than “add one consumer to the allowlist” if the slice wants the `source_profile` or readiness-facing story to remain honest
- treat `prose -> raw_json` as a limited fallback, not a strong proof shape in itself

## Strongest Confirmed Claims

- The Phase E ordering is correct. After the representative matrix, the next honest variable is no longer handoff-family breadth on `the-critic`; it is whether the same transient compose substrate can serve one real second consumer (`communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md:160-179`, `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md:181-196`).
- The current runtime is still structurally single-consumer at the transient compose boundary. `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"` and `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` contains only that key, with all three transient routes validating against that closed set (`src/presenter/compose_from_intent.py:54-59`, `src/presenter/compose_from_intent.py:148-158`, `src/presenter/compose_from_intent.py:521-599`).
- `aoi-canary` is already a real second consumer over analyzer-owned result contracts. Its live path is `result_discovery -> result_manifest -> result_presentation`, not `presenter/page`, and its tests enforce that boundary (`/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts:45-99`, `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:115-184`, `/home/evgeny/projects/aoi-canary/src/test/resultsClient.test.ts:23-65`).
- `AOI source_selection` is the strongest bounded transient default because it is already the richer planner-backed AOI transient path and has explicit four-family contract coverage (`tests/test_representative_composition_matrix.py:69-106`, `tests/test_compose_from_intent.py:1537-1692`).
- Analyzer-side renderer adaptation already exists and is recursive, so a bounded second-consumer proof does not need to invent a new adaptation substrate (`src/presenter/manifest_builder.py:105-135`, `src/presenter/compose_from_intent.py:473-500`, `src/presenter/compose_from_intent.py:1261-1310`).

## Audit Questions

### 1. Is a bounded transient second-consumer proof the right next Phase E slice after the representative composition matrix landed?

Yes.

The strategic memos all converge on the same sequence:

- the matrix proved the currently live handoff-family substrate on the current consumer surface
- the remaining bounded unresolved variable is consumer-surface generality
- the next slice should therefore vary the consumer once while keeping the transient compose substrate fixed

That is stated directly in the roadmap stack (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:241-252`, `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:302-330`, `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:331-357`, `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:342-354`) and is reinforced by the matrix completion memo itself (`communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md:160-196`).

I do not see a cleaner Phase E question remaining ahead of this one.
Another same-consumer matrix would be weaker.
Another governance family would be Phase D drift.

### 2. Is `aoi-canary` the right second-consumer target, or is the memo ignoring a better existing consumer surface?

`aoi-canary` is the right target.

Why it is the best existing fit:

- it is a separate real repo with a real browser host
- it already carries `consumer_key = aoi-canary` through analyzer-owned result contracts (`communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md:150-159`)
- its local rules explicitly forbid AOI-specific semantic joins or reconstruction (`/home/evgeny/projects/aoi-canary/README.md:54-68`)
- it already has focused tests around that result-backed boundary (`/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:115-184`, `/home/evgeny/projects/aoi-canary/src/test/resultsClient.test.ts:23-65`)

Why the obvious alternatives are worse:

- `visualizer` is defined as an `mcp_server`, not as a browser thin-host consumer surface (`src/consumers/definitions/visualizer.json:2-21`), and its live repo documentation is about Claude Code setup, engine execution, and result downloads rather than analyzer-owned presentation hosting (`/home/evgeny/projects/visualizer/mcp_server/README.md:1-46`)
- `analyzer-mgmt` is defined as a management/catalog browser with pages like `engines`, `views`, and `consumers`, not as a proved analysis-consumption host (`src/consumers/definitions/analyzer-mgmt.json:2-45`); I found evidence that it depends on the renderer package (`/home/evgeny/projects/analyzer-mgmt/frontend/package.json:12-24`), but not evidence that it is already a live thin analysis host

So there is no better existing bounded second-consumer target in the current repo stack.

### 3. Is AOI `source_selection` the right default proof path, or should the scope prefer `source_profile`, both, or something else?

`source_selection` is the right default proof path.

Reasons:

- it is already the planner-backed AOI transient path the matrix used as the richer AOI case (`communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md:34-40`, `tests/test_representative_composition_matrix.py:69-106`)
- it already has explicit four-family preserved-data contract coverage (`tests/test_compose_from_intent.py:1537-1692`)
- it tests more of the analyzer-owned planning/handoff law than `source_profile`

I would not prefer “both” in this slice.
That widens the proof unnecessarily.

`source_profile` should remain secondary only.
The memo is directionally right to demote it, but it understates an important asymmetry:
`source_backed_readiness` still reports AOI `compose-from-source` as blocked for any consumer other than `the-critic` (`src/analysis_products/source_backed_readiness.py:144-176`).
So `source_profile` is not merely a lighter alternate AOI path.
If used as the main proof path, it drags in extra analyzer-side uncoupling work around readiness/followup honesty.

### 4. Does the memo stay honest about the real analyzer-side work required?

Mostly yes, but it needs one correction.

The memo is correct that this is not already consumer-neutral and that real analyzer runtime work is required (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md:114-131`).
The code confirms that:

- transient compose is explicitly pinned to `the-critic` by constant and allowlist (`src/presenter/compose_from_intent.py:54-59`, `src/presenter/compose_from_intent.py:148-158`)
- all three transient routes validate against that gate (`src/presenter/compose_from_intent.py:521-599`)

So the memo is strategically honest about the need for analyzer-side work.

The correction is this:

- for the minimal `source_selection` proof, “expand the transient consumer allowlist/registration surface” is an honest summary
- for any `source_profile` fallback or readiness-facing acceptance story, that summary is incomplete because `source_backed_readiness` still hardcodes `compose-from-source` to `the-critic` in v1 (`src/analysis_products/source_backed_readiness.py:144-176`)

So the analyzer-side work is not just one gate change if the scope expects `source_profile` to remain an equally honest backup path.

### 5. Is analyzer-side fallback such as `prose -> raw_json` an acceptable bounded proof for this slice, or does it weaken the claim too much?

It is acceptable only in a bounded, explicitly weakened form.

Why it is acceptable:

- the adaptation is analyzer-side, not host-side (`src/presenter/manifest_builder.py:105-135`, `src/presenter/compose_from_intent.py:1261-1310`)
- `aoi-canary` already visibly supports `raw_json` and visibly fails unsupported renderers rather than papering over them (`src/consumers/definitions/aoi-canary.json:6-17`, `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx:10-37`)
- that still preserves the core Phase E claim if the host renders analyzer-owned payloads without reconstructing analytical meaning locally

Why it weakens the claim:

- `aoi-canary` does not support top-level `prose` (`src/consumers/definitions/aoi-canary.json:6-17`)
- the strongest existing canary contract test is specifically the pinned AOI result-backed surface that avoids `raw_json` adaptation (`tests/test_aoi_canary_contract.py:44-93`)

So the right calibration is:

- acceptable as a bounded fallback for one unsupported closeout surface
- not acceptable as a proof where most of the meaningful page collapses into `raw_json`

If the transient proof succeeds only by degrading the page wholesale to `raw_json`, the claim becomes too weak.
If it preserves the main analytical surfaces on native renderers and only adapts the unsupported prose closeout, the slice still counts.

### 6. Does the memo keep the strategic claim calibrated?

Yes.

This is one of the memo’s strongest qualities.
It repeatedly excludes:

- generic consumer plugin architecture
- arbitrary engine/pass combinatorics
- multi-consumer productization
- broad consumer generality claims

and it states the non-claims cleanly (`communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md:34-45`, `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md:193-214`, `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md:216-239`).

I do not see strategic overclaim in the memo.

## Strategic Disagreement

- None.

## Scope Corrections

- Keep `AOI source_selection` as the only named default proof path. Do not let `source_profile` read as an equally cheap substitute, because the AOI source-backed readiness seam still declares `compose-from-source` blocked for non-`the-critic` consumers (`src/analysis_products/source_backed_readiness.py:144-176`).
- Expand the analyzer-side work description slightly. For the minimal proof, the real runtime seam is the registered transient consumer gate in `src/presenter/compose_from_intent.py:54-59`, `src/presenter/compose_from_intent.py:148-158`, `src/presenter/compose_from_intent.py:521-599`. If the slice touches `source_profile` or readiness, it also has to remove the extra `the-critic` coupling above.
- Tighten the fallback wording. Allow `prose -> raw_json` only as a limited analyzer-side fallback for unsupported prose surfaces, not as blanket degradation of the transient proof path (`src/presenter/manifest_builder.py:105-135`, `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx:10-37`).

## Implementation Caution

- `aoi-canary` is not already transient-capable. Its live mode currently imports and uses only result-contract fetchers plus secondary `trace/status`, not any transient compose client (`/home/evgeny/projects/aoi-canary/src/App.tsx:11-19`, `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts:45-99`, `/home/evgeny/projects/aoi-canary/README.md:13-23`). So this slice needs real canary-side transient intake work, not only analyzer changes.
- The canary’s local renderer host is intentionally narrow. It dispatches only `accordion`, `card_grid`, and `raw_json`, with the root tab shell handled locally (`/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx:10-59`). That is fine for a bounded AOI proof, but renderer compatibility needs to be checked deliberately rather than assumed from the registry entry alone.
- The consumer registry is broad, but the transient proof boundary is not. Consumer definitions are loaded generically from JSON (`src/consumers/registry.py:22-62`), yet transient compose still enforces a closed runtime adapter set (`src/presenter/compose_from_intent.py:148-158`, `src/presenter/compose_from_intent.py:521-599`). The proof should describe that asymmetry explicitly.

## Final Recommendation

Proceed with this slice.

But proceed with three explicit clarifications:

1. `source_selection` is the default and preferred proof path.
2. `source_profile` is only a weaker backup and is not analyzer-cheap if readiness/followup honesty matters.
3. `raw_json` fallback is acceptable only as a limited bounded adaptation, not as the dominant rendered outcome.

With those corrections, the memo is strategically sound, codebase-accurate enough, and properly calibrated for Phase E.
