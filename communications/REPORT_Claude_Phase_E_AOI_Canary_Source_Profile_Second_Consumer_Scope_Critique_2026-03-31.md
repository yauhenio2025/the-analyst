# Critique: Phase E AOI Canary Source-Profile Second-Consumer Scope

**Verdict: Approve with revisions**

Date: 2026-03-31
Reviewer: Claude (Opus 4.6)
Memo Under Review: `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_second_consumer_scope.md`

---

## Strategic Assessment

### The memo is strategically correct on the core question

The next bounded Phase E step **should** be broadening `aoi-canary` from AOI `source_selection` to AOI `source_profile`. The memo's reasoning is sound:

1. `source_profile` is the remaining AOI compose family already live on `the-critic`.
2. The coupling is concrete and analyzer-owned — two explicit code gates, not diffuse architecture.
3. Keeping the consumer fixed while varying the compose family is the smallest honest next variable.
4. Jumping to non-AOI second-consumer proof or a third consumer before covering both AOI families on the existing canary would be premature and dishonest about what has actually been tested.

No better alternative next step exists within Phase E. The memo's exclusion list (no non-AOI, no third consumer, no generic architecture, no planner integration in canary) is exactly right.

### The scope is appropriately bounded

The memo correctly treats `compose-from-source` and `source_backed_readiness` as one truthful path (Decision 1). This is important: broadening only the presenter route while leaving readiness stale would create an internally inconsistent analyzer contract — readiness would still say "blocked" for `aoi-canary` while the route itself would succeed. The memo catches this.

---

## Implementation-Critical Findings

### Finding 1: The canary needs a NEW client function, not just a new fixture

**Severity: Implementation-critical omission**

The memo assumes that adding a pinned fixture and reusing the existing `transient_proof` mode (Decision 3) is sufficient. But the current `aoi-canary` transient infrastructure has **no `compose-from-source` client function at all**:

- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts` only exports `composeFromSelection()`, which POSTs to `/v1/presenter/compose-from-selection`.
- `compose-from-source` is a **different endpoint** (`POST /v1/presenter/compose-from-source`) with a **different request schema** (`ComposeFromSourceRequest` vs `ComposeFromSelectionRequest`).

The key schema difference:
```
ComposeFromSourceRequest: { workflow_key, consumer_key, source_v2_job_id, profile, user_intent?, style_school? }
ComposeFromSelectionRequest: { workflow_key, consumer_key, source_v2_job_id, selection[], user_intent, selection_summary?, legacy_profile_equivalent?, style_school? }
```

`source_profile` uses a `profile` enum field (e.g. `"dossier"`) instead of a `selection[]` array. The memo should explicitly acknowledge that `transientClient.ts` needs a second thin function (`composeFromSource()`) and that the fixture format will differ structurally from the existing `source_selection` fixture.

This doesn't change the scope's boundaries — it's still bounded canary work — but the memo's omission of this could cause an implementor to underestimate the canary-side surface area.

### Finding 2: The `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` change is one line

**Severity: Informational (memo is correct but could be more precise)**

The analyzer-side admission fix is mechanical. In `compose_from_intent.py` line 163:

```python
"aoi-canary": frozenset({_HANDOFF_KIND_SOURCE_SELECTION}),
```

becomes:

```python
"aoi-canary": frozenset({_HANDOFF_KIND_SOURCE_SELECTION, _HANDOFF_KIND_SOURCE_PROFILE}),
```

The memo identifies this coupling but doesn't name the exact code location. This is fine for a scope memo, but an implementor should know that the admission gate is at `compose_from_intent.py:163` and the validation enforcement is at `_validate_handoff_capability()` (lines 530-550).

### Finding 3: The `source_backed_readiness` coupling is also one surgical change

**Severity: Informational (memo is correct)**

In `source_backed_readiness.py` lines 147-150:

```python
if consumer_key != TRANSIENT_COMPOSE_CONSUMER_KEY:
    followup_blockers.append(
        f"compose-from-source only supports consumer_key='{TRANSIENT_COMPOSE_CONSUMER_KEY}' in v1"
    )
```

This guard needs to become consumer-aware rather than single-consumer-only. The honest fix is either:
- (a) Check against the same `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` registry that `compose_from_intent.py` already uses, or
- (b) Maintain a parallel allowlist in `source_backed_readiness.py`.

Option (a) is better because it keeps the consumer admission truth in one place. The memo doesn't prescribe how to fix this — it just says to remove the blocker — which is appropriate for a scope memo.

### Finding 4: The `transient_proof` mode needs a sub-mode selector

**Severity: Minor omission**

The memo's Decision 3 says "add one AOI `source_profile` proof fixture selector or equivalent narrow mode choice" but doesn't specify the UX shape. Currently `transient_proof` mode in `App.tsx` unconditionally loads the `source_selection` fixture and calls `composeFromSelection()`. Adding `source_profile` requires either:

- A mode selector within `transient_proof` (e.g., dropdown or toggle choosing which proof to replay), or
- A second mode constant (e.g., `transient_proof_source_profile`).

The "equivalent narrow mode choice" phrasing is vague enough to allow either approach. An implementor should choose the first approach (sub-selector) to keep the mode count small and avoid proliferating top-level mode constants.

---

## Claims Verified Against Codebase

### Claim: "`compose-from-source` only supports `consumer_key='the-critic'` in v1" — CONFIRMED

Two independent gates enforce this:
1. `compose_from_intent.py:163` — `aoi-canary` registered only for `source_selection`, not `source_profile`
2. `source_backed_readiness.py:147-150` — explicit blocker for any consumer that isn't `the-critic`

Both must be widened. The memo correctly identifies both.

### Claim: "aoi-canary is admitted only for source_selection" — CONFIRMED

`_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` at `compose_from_intent.py:158-167` shows:
- `the-critic`: `{direct_sections, source_profile, source_selection}`
- `aoi-canary`: `{source_selection}` — only `source_selection`

### Claim: The default source identity `job-744edf255ad5` is valid for `source_profile` — PLAUSIBLE BUT UNVERIFIED

The memo reuses the same job ID from the `source_selection` proof. This job ID was valid for `source_selection` — but `compose-from-source` with `profile=dossier` calls `build_source_composition_bridge()` which resolves a source catalog from the job's stored results. Whether `job-744edf255ad5` has the right stored artifacts for the `dossier` profile to succeed is not guaranteed by the scope memo. The implementor should verify this at implementation time (or the acceptance bar will catch it).

### Claim: The canary consumer definition supports this work — CONFIRMED

`src/consumers/definitions/aoi-canary.json` declares `status: "active"` with renderers `[accordion, card_grid, tab, raw_json]`. This matches the transient compose output shape. The consumer definition itself needs no changes.

---

## Broader Strategic Context Check

### Alignment with distilled strategic roadmap — ALIGNED

The distilled roadmap (`MEMO_2026-03-30_distilled_strategic_roadmap.md`) lists the next Phase E slice as "broaden same consumer to remaining AOI compose family (source_profile, compose-from-source)". This scope memo is exactly that.

### Alignment with fixed-direction roadmap — ALIGNED

The fixed-direction roadmap's anti-drift rules apply cleanly:
- This is upstream analyzer work (not downstream app polish) — rule 3 satisfied
- This removes explicit `the-critic` coupling — rule 2 satisfied (codifies stable host contract)
- This is AOI work only while required to close the consumer-generalization seam — rule 4 satisfied

### Alignment with master roadmap vision — ALIGNED

The master roadmap calls for de-criticizing the transient consumer contract. This scope memo is exactly one bounded step in that direction: it removes the last AOI-specific `the-critic` coupling from the compose-from-source path, proving that the canary can consume both AOI compose families.

---

## What the Memo Gets Right

1. **Smallest honest next variable** — correctly identified as `source_profile` on same consumer, not a new consumer or new workflow.
2. **Two coupling points identified** — both `compose_from_intent.py` admission and `source_backed_readiness.py` blocker are real and must both change.
3. **Fixture-backed canary** — Decision 2 is exactly right; the canary must not derive profile truth locally.
4. **Live proof bar** — Decision 4's acceptance bar is mechanically verifiable and non-negotiable.
5. **Explicit scope exclusions** — The "Must Not Widen" section prevents the predictable scope creep paths.

## What the Memo Should Revise

1. **Acknowledge the new client function requirement** — `transientClient.ts` needs `composeFromSource()` targeting `/v1/presenter/compose-from-source`. The fixture format differs structurally from the existing `source_selection` fixture (uses `profile` enum, not `selection[]` array). This is bounded work but the memo should name it explicitly.

2. **Specify the sub-mode UX shape** — Decision 3's "equivalent narrow mode choice" is too vague. State explicitly whether this is a fixture-selector within `transient_proof` or a separate mode.

3. **Add a validation step for the source job ID** — The acceptance bar should include a step 0: "the pinned `source_v2_job_id` must resolve a valid source catalog for the `dossier` profile on `compose-from-source`". If the existing `job-744edf255ad5` doesn't have the right stored artifacts for `dossier`, the implementor needs to know early.

## What the Memo Should NOT Change

- The strategic direction (correct)
- The consumer choice (correct — keep `aoi-canary`)
- The compose family choice (correct — `source_profile`)
- The proof discipline (correct — live browser/network evidence)
- The exclusion list (correct and necessary)

---

## Verdict Summary

**Approve with revisions.** The strategic direction is exactly right and the scope boundaries are sound. The three revisions above are implementation-detail corrections, not strategic objections. The memo can proceed to implementation after acknowledging the `transientClient.ts` new-function requirement, specifying the sub-mode shape, and adding source-job-ID validation to the acceptance bar.
