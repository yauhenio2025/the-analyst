# Report: Phase E AOI Canary Genealogy Direct-Sections Second-Consumer V1 Completion Audit

Verdict: Approve with corrections

## Highest-Signal Findings

1. The bounded completion claim is substantively earned, but the memo outruns the current roadmap ledger unless it says so explicitly.

The codebase and proof artifacts support the narrow technical claim that one existing second consumer can now carry one bounded non-AOI `direct_sections` compose path without host-local analytical reconstruction. Analyzer admission is real and narrow in `src/presenter/compose_from_intent.py:148-176`, `src/presenter/compose_from_intent.py:559-579`, and `src/presenter/compose_from_intent.py:582-643`. The canary-side proof path is real in `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:44-59`, `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:69-77`, `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:163-239`, `/home/evgeny/projects/aoi-canary/src/App.tsx:188-199`, `/home/evgeny/projects/aoi-canary/src/App.tsx:850-923`, and `/home/evgeny/projects/aoi-canary/src/App.tsx:1203-1209`. The frozen proof and live closeout also match that story: `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_genealogy_direct_sections_2026-03-31.json`, `communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.json`, and `/home/evgeny/projects/aoi-canary/src/fixtures/transient-genealogy-direct-sections.json:2-27`.

The documentary problem is sequencing, not substance. The current roadmap docs still name `aoi-canary` / AOI `source_profile:comparison` as the next bounded Phase E step in `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:256-260`, `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:313-349`, `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:229-236`, `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:367-405`, `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:505-510`, and `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1238-1243`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1361-1365`. The repo does contain comparison proof artifacts and tests, so this non-AOI memo is directionally plausible, but it should say explicitly that it depends on a now-landed comparison slice that the canonical roadmap/state-of-play ledger has not yet been updated to narrate.

2. The live-closeout artifact list is factually wrong as written.

`communications/MEMO_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion.md:127-132` lists `communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.md`, but that file is not present in the repo. The actual frozen artifact set for that prefix is `.json`, `.har`, and `.png`. This is a documentation error, not a code or proof failure, but it needs correction because the memo currently overstates the frozen evidence bundle.

3. The capability summary is slightly too broad unless it is scoped to transient-proof compose mode.

`communications/MEMO_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion.md:187-191` says `aoi-canary` now carries AOI `source_selection`, AOI `source_profile:dossier`, AOI `source_profile:comparison`, and one bounded non-AOI `direct_sections` path. That phrasing is only safe if it is read as fixture-backed transient compose proof coverage. In code, the non-AOI addition lives inside `transient_proof` mode and its explicit case registry, not as a broad live/result-backed app capability: `/home/evgeny/projects/aoi-canary/src/App.tsx:171-185`, `/home/evgeny/projects/aoi-canary/src/App.tsx:188-199`, and `/home/evgeny/projects/aoi-canary/src/App.tsx:850-923`. The canary still defaults its live/result-backed flow to AOI and still uses a pinned request fixture for the genealogy slice rather than a second-consumer planner/result launch path. The memo should tighten this to "inside `transient_proof`" or "in bounded fixture-backed transient compose proof mode."

4. The memo is strategically honest only because it stays at pinned-request compose scope, not broader non-AOI consumer generality.

That boundary is backed by the implementation. The direct-sections fixture carries the exact request plus `planning_decision_id` identity in `/home/evgeny/projects/aoi-canary/src/fixtures/transient-genealogy-direct-sections.json:2-27`. The client simply posts that request to `POST /v1/presenter/compose-from-intent` in `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:163-177`. The app then validates only the returned surface shape and renders it directly, with no planner fetch, no lowering fetch, and no host-local semantic reconstruction in `/home/evgeny/projects/aoi-canary/src/App.tsx:863-906`. That is the right bounded proof for this slice, but it is not a proof of non-AOI planner-backed launch, non-AOI result discovery, or generic consumer architecture. The memo mostly says this already; keep that caveat explicit wherever the prose starts sounding broader.

## Verification

I reran the memo's claimed verification surfaces against the current repo state:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_source_backed_readiness.py tests/test_aoi_canary_contract.py tests/test_representative_composition_matrix.py`
  - result: `56 passed, 2 warnings`
- `npm --prefix /home/evgeny/projects/aoi-canary run type-check`
  - result: passed
- `npm --prefix /home/evgeny/projects/aoi-canary run test -- --run`
  - result: `26 passed`

Those counts match the memo's verification section. The direct-sections proof assertions are also mechanically covered in `tests/test_compose_from_intent.py:832-877`, `tests/test_aoi_canary_contract.py:221-238`, `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts:284-305`, `/home/evgeny/projects/aoi-canary/src/test/transientClient.test.ts:356-439`, and `/home/evgeny/projects/aoi-canary/src/test/App.test.tsx:520-585`.

## Required Corrections

- Add a short status note near the top saying this memo depends on the already-landed AOI `source_profile:comparison` slice, while the canonical roadmap/state-of-play memos still need to be updated to narrate that before this becomes the official next-step ledger entry.
- Fix the live-closeout artifact list at `communications/MEMO_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion.md:127-132` by removing the nonexistent `.md` file or adding the missing proof note.
- Tighten the "aoi-canary now carries" language at `communications/MEMO_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion.md:187-191` so it is explicitly scoped to `transient_proof` / bounded fixture-backed transient compose proof mode.
- Keep the completion claim phrased as one bounded non-AOI compose-path proof. Do not let it drift into implying non-AOI planner/result integration on the second consumer, because the current implementation still proves the slice through a pinned `ComposeFromIntentRequest`, not through a broader second-consumer launch chain.

## Bottom Line

The memo earns its bounded completion claim after correction. It is not too weak. It is slightly too strong only where it skips the roadmap-ratification caveat, overstates the frozen artifact set, and uses app-capability wording that is broader than the actual transient-proof-only implementation.
