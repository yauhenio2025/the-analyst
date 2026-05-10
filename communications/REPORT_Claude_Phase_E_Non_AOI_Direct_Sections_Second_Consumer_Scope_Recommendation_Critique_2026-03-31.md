# Critique Report: Phase E Non-AOI Direct Sections Second-Consumer Scope Recommendation

Date: 2026-03-31
Reviewer: Claude Opus 4.6
Scope Memo Under Review: `communications/MEMO_2026-03-31_phase_e_non_aoi_direct_sections_second_consumer_scope_recommendation.md`
Prompt: `communications/PROMPT_2026-03-31_phase_e_non_aoi_direct_sections_second_consumer_scope_recommendation_review_claude.md`

---

## Verdict: Approve with revisions

The strategic direction is correct. This is the right next bounded Phase E step after AOI `source_profile:comparison` closeout. The revisions required are implementation-critical constraint sharpening, not strategic redirections.

---

## Strategic Assessment

### Where the memo is right

1. **Fixed consumer, broader variable.** Keeping `aoi-canary` as the consumer while broadening from AOI-only to one non-AOI path is the smallest honest next broader variable. The alternatives — a third consumer, generic consumer architecture, or further AOI preset work — are either too broad, too narrow, or lateral.

2. **Genealogy `direct_sections` is the right target.** It already has current-consumer proof (`PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json`). It exercises a genuinely different page shape (`card_grid` root, empty raw-json leaf set). It uses the already-proved `compose-from-intent` route. This is not a speculative target — it is a proved-on-current-consumer path that the second consumer does not yet exercise.

3. **Anti-scope-creep boundaries are well-drawn.** The stop conditions (no third consumer, no generic consumer architecture, no planner integration in canary, no multiple non-AOI workflows) are correct and important. The "stop and rescope" escape hatch is appropriate.

4. **The proof bar is mechanically auditable.** The expected conditions — observed request equals pinned fixture, `card_grid` root, empty raw-json leaf set, no forbidden upstream calls — are all mechanically verifiable. This is strong.

5. **Alignment with distilled roadmap.** The distilled strategic roadmap's Rule 2 ("do not confuse bounded proof with generalized architecture") is correctly honored. This is a bounded proof that teaches a real variable: can a second consumer accept a non-AOI page shape?

### Where the memo is overstated

1. **"It may need to stop assuming the root renderer is always tab" is too soft.** This is not a "may need to." The current `validateTransientProofSurface` function in `transientClient.ts:182-183` hard-gates on `tab`:
   ```typescript
   if (rootView.renderer_type !== 'tab') {
       return `Transient proof requires a tab root renderer; got ${rootView.renderer_type}.`
   }
   ```
   And the rendering gate in `App.tsx:1185-1193` shows an error state for any non-`tab` root:
   ```tsx
   rootView.renderer_type !== 'tab' ? (
       <div className="empty-state">
           <h2>Unexpected root renderer</h2>
   ```
   Both of these will reject the `card_grid` root that genealogy `direct_sections` returns. This is a definite blocker, not a possibility. The memo should state it as such.

2. **"Reuses an already-proved analyzer-owned non-AOI transient path" is slightly overstated.** The existing matrix proof proved `direct_sections` on `consumer_key=the-critic`. The proof that it works on `consumer_key=aoi-canary` is exactly what this slice needs to prove. The analyzer-side path is proved; the consumer-side path is not.

### Where the memo is too timid

1. **The memo should be more explicit about the fixture type system change.** The current `TransientProofFixture` type union in `transientClient.ts:53-55` only has two variants:
   ```typescript
   export type TransientProofFixture =
     | SourceSelectionTransientProofFixture
     | SourceProfileTransientProofFixture
   ```
   A third variant is needed for `compose-from-intent`. The memo says "add one pinned `ComposeFromIntentRequest` fixture" but does not acknowledge that the fixture type system itself needs a new discriminated-union arm. This is not a major change, but naming it explicitly would prevent the implementor from trying to squeeze the new case into an existing variant.

2. **The memo should name the transient identity generation question.** The current `normalizeTransientPresentation` in `transientClient.ts:138-141` generates identities as:
   ```typescript
   const transientIdentity = isSourceSelectionFixture(fixture)
       ? fixture.planning_decision_id
       : `${fixture.request.source_v2_job_id}:${fixture.request.profile}`
   ```
   For a `direct_sections` fixture that has a `planning_decision_id`, the identity should follow the same pattern as `source_selection`. The memo should state this decision explicitly so the implementor does not invent a new identity scheme.

### Where the memo is missing implementation-critical constraints

1. **The App.tsx dispatch logic needs a third branch.** The transient compose dispatch at `App.tsx:850-859` currently branches on `request_kind`:
   ```typescript
   const requestPromise =
     activeTransientFixture.request_kind === 'source_selection'
       ? composeFromSelection(...)
       : composeFromSource(...)
   ```
   A `direct_sections` case requires calling `composeFromIntent(...)`, which is a different client function hitting a different endpoint (`/v1/presenter/compose-from-intent`) with a different request schema (`ComposeFromIntentRequest` with `prose_sections`). The memo should enumerate this as a distinct implementation step, not leave it implicit under "extend the proof-case model."

2. **The `TransientProofCaseKey` type union needs a new arm.** Currently at `App.tsx:39-42`:
   ```typescript
   type TransientProofCaseKey =
     | 'source_selection'
     | 'source_profile_dossier'
     | 'source_profile_comparison'
   ```
   Adding `'genealogy_direct_sections'` is required. The memo says "add one new transient proof case" but doesn't name the TypeScript type that needs changing.

3. **The `TRANSIENT_PROOF_CASE_LABELS` and related copy functions are AOI-specific.** The strategy copy at `App.tsx:435-452` and surface messages at `App.tsx:398-433` hard-code AOI-specific text like "Replaying the pinned AOI source-selection request fixture." The memo correctly says "generalize proof labels, status copy, and strategy copy so they are case-aware instead of AOI-only" but this deserves a concrete stop condition: the copy must not say "AOI" for the genealogy case.

4. **The analyzer-side consumer adapter gate change is exactly one line.** The `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` in `compose_from_intent.py:166-171`:
   ```python
   "aoi-canary": frozenset(
       {
           _HANDOFF_KIND_SOURCE_PROFILE,
           _HANDOFF_KIND_SOURCE_SELECTION,
       }
   ),
   ```
   Becomes:
   ```python
   "aoi-canary": frozenset(
       {
           _HANDOFF_KIND_DIRECT_SECTIONS,
           _HANDOFF_KIND_SOURCE_PROFILE,
           _HANDOFF_KIND_SOURCE_SELECTION,
       }
   ),
   ```
   The workflow-level gate in `_SUPPORTED_HANDOFF_KINDS` already supports `direct_sections` for `intellectual_genealogy`. The memo should confirm this is already true (it is) to prevent unnecessary exploratory work.

---

## Codebase Verification of Key Claims

| Claim in memo | Verified | Evidence |
|---|---|---|
| `aoi-canary` currently fails closed on `direct_sections` | Yes | `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS["aoi-canary"]` only has `source_profile` and `source_selection` (`compose_from_intent.py:166-171`) |
| There is no `composeFromIntent()` client | Yes | `transientClient.ts` only exports `composeFromSelection` and `composeFromSource` |
| Transient proof cases are still AOI-only | Yes | `TransientProofCaseKey` union in `App.tsx:39-42` has only AOI cases |
| Root rendering still assumes `tab` | Yes | `App.tsx:1185-1193` and `transientClient.ts:182-183` both hard-gate on `tab` |
| Genealogy `direct_sections` returns `card_grid` root with empty raw-json leaves | Yes | `PROOF_phase_e_matrix_genealogy_direct_sections_2026-03-30.json` (captured on current consumer) has `card_grid` root, verified in matrix proof |
| The route `POST /v1/presenter/compose-from-intent` exists | Yes | Registered in `src/api/routes/presenter.py` |
| The `ComposeFromIntentRequest` schema exists and includes `prose_sections` | Yes | `src/presenter/schemas.py:613-621` |
| Genealogy `direct_sections` is already in `_SUPPORTED_HANDOFF_KINDS` | Yes | `compose_from_intent.py:156`: `GENEALOGY_WORKFLOW_KEY: frozenset({_HANDOFF_KIND_DIRECT_SECTIONS})` |
| `source_v2_job_id = proof-round4-adaptive-balance-final-1774012011` is a valid proof lineage | Yes | Confirmed in matrix proof JSON |
| `planning_decision_id = planning-decision-5f5b0182f2f9` is a valid proof lineage | Yes | Confirmed in matrix proof JSON |

---

## Is This the Right Next Move?

**Yes, with the implementation constraints sharpened.**

The alternative candidates considered and rejected:

1. **More AOI preset work on `aoi-canary`** — All three AOI presets are now closed (source_selection, source_profile:dossier, source_profile:comparison). There is no more AOI-local broadening to do without repeating proved variables.

2. **A third consumer** — Premature. The second consumer hasn't yet proved non-AOI compatibility. Adding a third before that broadening exists would skip a load-bearing proof step.

3. **Generic consumer registration architecture** — Premature. The current explicit consumer adapter registry is still earning its keep as a proving harness. Generalizing it before a non-AOI second-consumer proof exists would remove the fail-closed gate before the gate has been tested on the broader variable.

4. **Non-consumer platform work (lifecycle, governance)** — Different axis. The current Phase E line is about composition generality, not governance. This is correctly scoped.

5. **A different non-AOI workflow** — There is no other live-proved non-AOI workflow. Genealogy `direct_sections` is the only viable target.

So: genealogy `direct_sections` on `aoi-canary` is the only defensible next step. The memo is correct.

---

## Specific Corrections Needed in the Memo

1. Replace "it may need to stop assuming the root renderer is always `tab`" with "it MUST stop assuming the root renderer is always `tab`" and name the two hard gates: `validateTransientProofSurface` in `transientClient.ts` and the root rendering branch in `App.tsx`.

2. Add an explicit implementation step for the third dispatch branch in the App.tsx transient compose effect (calling `composeFromIntent()` for `direct_sections` fixtures).

3. Add an explicit note that the fixture type system (`TransientProofFixture` discriminated union) needs a new arm, not just a new fixture file.

4. Add a note confirming that the workflow-level gate (`_SUPPORTED_HANDOFF_KINDS`) already admits `direct_sections` on `intellectual_genealogy`, so no change is needed there — only the consumer adapter gate needs updating.

5. Name the transient identity scheme decision: `direct_sections` fixtures should carry `planning_decision_id` and follow the `source_selection` identity pattern.

---

## Summary

The strategic recommendation is correct. This is the smallest honest broader Phase E question after AOI-local preset work closes on the second consumer. The target, the proof bar, and the stop conditions are well-chosen. The revisions needed are about sharpening implementation constraints so the implementor does not rediscover already-known blockers. No change in strategic direction is recommended.
