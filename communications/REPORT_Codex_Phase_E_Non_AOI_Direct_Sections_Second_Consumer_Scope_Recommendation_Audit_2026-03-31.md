# Report: Phase E Non-AOI Direct Sections Second-Consumer Scope Recommendation Audit

Verdict: Approve

The revised memo now names the right next broader Phase E question and keeps the claim honest. After the AOI `source_profile:comparison` closeout, one bounded non-AOI `direct_sections` proof on the already-live-proved second consumer is the strongest next matrix-broadening move that does not jump prematurely to a third consumer or generic consumer architecture.

## Highest-Signal Findings

### 1. The memo now correctly treats AOI `source_profile:comparison` as closed in code and proof, while also acknowledging roadmap lag.

That is consistent with the actual repo state:

- `src/presenter/compose_from_intent.py:158-176` now admits `aoi-canary` on both `source_selection` and `source_profile`, with both `dossier` and `comparison` registered for `aoi-canary`
- `src/analysis_products/source_backed_readiness.py:147-160` uses the same capability gate, so readiness truth is aligned in code
- `/home/evgeny/projects/aoi-canary/src/App.tsx:39-43` and `/home/evgeny/projects/aoi-canary/src/App.tsx:185-193` already include the `source_profile_comparison` transient proof case
- the proof set already includes:
  - `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_profile_comparison_2026-03-31.json`
  - `communications/PROOF_phase_e_aoi_canary_source_profile_comparison_live_closeout_2026-03-31.md`

So the memo is now using the codebase truth rather than the stale roadmap wording as its basis.

### 2. The lineage caveat is now honest.

The revised memo correctly states that the existing genealogy proof lineage is still current-consumer lineage:

- `communications/PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json`
- `consumer_key = the-critic`

That matters because the lowering path is consumer-bound in code:

- `src/orchestrator/direct_sections_compose_harness.py:57-79`
- `src/api/routes/orchestrator.py:364-394`

The memo now makes the right narrower claim:

- the existing genealogy bundle can seed analyzer-owned substrate truth and fixture source material
- it cannot itself serve as the final `aoi-canary` proof artifact
- the second-consumer slice still requires one fresh `aoi-canary`-specific proof bundle and one fresh live closeout

That closes the biggest accuracy gap from the previous draft.

### 3. The memo now scopes the analyzer-side change precisely.

This is now framed correctly.

The workflow-level `direct_sections` path already exists:

- `src/presenter/compose_from_intent.py:148-157`

What remains fail-closed today is consumer admission for `aoi-canary` on that handoff:

- `src/presenter/compose_from_intent.py:166-171`
- `tests/test_compose_from_intent.py:831-843`

So the recommended analyzer change is now described accurately as:

- consumer-adapter admission broadening at the existing registration seam

not:

- a workflow-law redesign
- a new public interface
- or a new capability architecture

### 4. The memo now names the real canary blockers concretely rather than hypothetically.

The revised draft correctly calls out the exact host assumptions that still block the slice:

- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:174-185` still rejects any non-`tab` root
- `/home/evgeny/projects/aoi-canary/src/App.tsx:1185-1197` still errors on non-`tab` roots
- `/home/evgeny/projects/aoi-canary/src/App.tsx:850-859` still dispatches only `compose-from-selection` or `compose-from-source`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:53-59` still has no `direct_sections` arm in `TransientProofFixture`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:138-141` still assumes transient identity is either `planning_decision_id` or `source_v2_job_id:profile`

That is the right bounded host scope.

It is also consistent with the analyzer truth for the target case:

- `communications/PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json`
- root renderer is `card_grid`
- raw-json leaf set is empty

### 5. The memo now keeps the success claim narrow enough to stay strategically honest.

This point is now stated correctly.

`aoi-canary` remains AOI-branded in both consumer definition and app shell:

- `src/consumers/definitions/aoi-canary.json`
- `/home/evgeny/projects/aoi-canary/src/App.tsx:992-999`

So a successful genealogy `direct_sections` slice would prove:

- one bounded non-AOI compose path works inside the existing `aoi-canary` shell without host-local analytical reconstruction

It would not prove:

- broad host-neutral generality
- a generic cross-workflow consumer
- full de-AOI-ification of the canary shell

That narrower claim is still the right Phase E step.

## Recommendation

Approve the revised recommendation memo.

The next bounded Phase E move should be:

1. admit `aoi-canary` on `direct_sections` at the existing analyzer consumer-registration seam
2. freeze one pinned `ComposeFromIntentRequest` fixture from analyzer-owned direct-sections truth, with `planning_decision_id` carried as identity
3. broaden the canary transient shell just enough to:
   - add a `composeFromIntent()` branch
   - add a `direct_sections` proof-case arm
   - accept a top-level `card_grid` root without wrapping it in a synthetic `tab`
4. close the slice with one fresh `aoi-canary`-specific proof bundle and one live browser/network proof

## Residual Note

The broader roadmap docs are still stale relative to the code/proof state on AOI `source_profile:comparison`, but the revised memo now names that catch-up debt honestly. That is no longer a blocker to approving this recommendation memo as a recommendation.
