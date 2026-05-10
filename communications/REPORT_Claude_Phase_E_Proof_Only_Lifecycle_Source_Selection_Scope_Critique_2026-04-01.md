# Review: Phase E Proof-Only Lifecycle Source-Selection Scope

Reviewer: Claude Opus 4.6
Date: 2026-04-01
Memo Under Review: `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_scope.md`

## Verdict: Approve with corrections

The memo correctly identifies the next smallest honest Phase E step, correctly diagnoses the contractual gap, and proposes the right general direction. The corrections below are implementation-level refinements, not strategic objections.

---

## Code-Backed Verification of Memo Claims

### Claim 1: "The public save seam still only persists `ComposeFromIntentRequest`"

**Verified: TRUE**

- `src/presenter/schemas.py:740`: `ComposeSessionSaveRequest.compose_request: ComposeFromIntentRequest`
- `src/presenter/schemas.py:758`: `PersistedComposeSession.compose_request: ComposeFromIntentRequest`
- `src/presenter/compose_session_store.py:31-32`: function signature takes `compose_request: ComposeFromIntentRequest`

The save seam is rigidly intent-shaped. No union, no optional alternative shape.

### Claim 2: "`compose_from_selection()` already lowers into an internal `ComposeFromIntentRequest`"

**Verified: TRUE**

- `src/presenter/compose_from_intent.py:319-327`:
  ```python
  intent_request = ComposeFromIntentRequest.model_validate(
      {
          "workflow_key": request.workflow_key,
          "consumer_key": request.consumer_key,
          "user_intent": request.user_intent.strip(),
          "prose_sections": [section.model_dump() for section in sections],
          "style_school": request.style_school,
      }
  )
  ```

The lowered request is a fully populated `ComposeFromIntentRequest` with real `prose_sections` materialized from the selection bridge. It is then passed to `_compose_handoff_sections()` which produces the response. The lowered object exists in memory during the call but is never exposed to the caller.

### Claim 3: "The current source-selection response truth does not expose the exact lowered `prose_sections`"

**Verified: TRUE**

- `src/presenter/schemas.py:729-734`: `ComposeFromIntentResponse` contains `presentation`, `generated_view_definitions`, and `trace`
- The trace includes `section_materialization` stage with `to_trace_dict()` output for each materialized section, but this is diagnostic metadata (engine_key, title, lineage info), not the exact prose bodies
- The response has no field that carries the lowered `ComposeFromIntentRequest` object

Even if the trace happened to include prose excerpts, it would be architecturally wrong for the harness to reconstruct the lowered request from trace metadata. The memo's insistence on analyzer-owned truth is correct.

### Claim 4: "The current compose-from-selection response type is `ComposeFromIntentResponse`"

**Verified: TRUE**

- `src/presenter/compose_from_intent.py:308`: `def compose_from_selection(request: ComposeFromSelectionRequest) -> ComposeFromIntentResponse:`
- `src/api/routes/presenter.py:446`: `@router.post("/compose-from-selection", response_model=ComposeFromIntentResponse)`

Both the implementation and the route annotation use `ComposeFromIntentResponse` as the return type.

### Claim 5: "AOI `source_selection` is the next smallest honest lifecycle target"

**Verified: TRUE**

- `App.tsx:92`: `const lifecycleEnabled = consumerKey === 'transient-proof-harness' && proofCase === 'genealogy_direct_sections'`
- The harness has exactly two transient proof cases: `source_selection` and `genealogy_direct_sections`
- `direct_sections` lifecycle is now complete (proved in `PROOF_phase_e_proof_only_lifecycle_direct_sections_saved_session_2026-04-01.json`)
- `source_selection` is the only remaining transient family on the same harness line

No other lifecycle target exists on this harness that would be smaller. `source_profile` goes through a completely different compose route (`compose-from-source`) and is correctly excluded.

### Claim 6: "Keeping consumer identity fixed at `transient-proof-harness` is the right discipline"

**Verified: TRUE**

Plurality was proved earlier (`MEMO_2026-04-01_phase_e_transient_consumer_identity_plurality_v1_completion.md`). The variable being tested here is lifecycle broadening across compose request families, not consumer identity. Varying both simultaneously would conflate the experimental variable.

---

## Strategic Assessment

### Is this the right next step for Phase E?

**Yes.** The distilled strategic roadmap (`MEMO_2026-03-30_distilled_strategic_roadmap.md`) explicitly names this as the current active question:

> "how does AOI `source_selection` broaden into save/reopen honestly on that same line without host-local lowered-request reconstruction and without turning the current save seam into a generic union by default?"

The memo's diagnosis aligns perfectly with the program trajectory. The step moves intelligence upstream (the analyzer exposes its own lowered truth) rather than downstream (the harness reconstructing it locally). This satisfies the distilled roadmap's Rule 1: "Prefer upstream intelligence over downstream convenience."

### Is there a smaller honest step that should come first?

**No.** I examined three alternatives:

1. **Another consumer-identity variation** — already proved, would be regression
2. **A different workflow family** — no other transient family exists on this harness
3. **A schema-widening-only step** — would be architecturally larger, not smaller

The memo's scoping is the minimum honest next step.

---

## Implementation Corrections

### Correction 1: The memo should specify the concrete mechanism for exposing the lowered request

The memo says "expose one analyzer-owned persistable lowered request alongside the compose-from-selection response truth" but leaves the implementation mechanism ambiguous. There are three possible designs:

**Option A: Add an optional field to `ComposeFromIntentResponse`**
```python
class ComposeFromIntentResponse(BaseModel):
    presentation: TransientIntentPagePresentation
    generated_view_definitions: list[ViewDefinition] = Field(default_factory=list)
    trace: ComposeFromIntentTrace
    persistable_intent_request: Optional[ComposeFromIntentRequest] = None  # NEW
```

Populated by `compose_from_selection()`, left `None` by `compose_from_intent()`.

**Option B: Create a separate `ComposeFromSelectionResponse` wrapper**
```python
class ComposeFromSelectionResponse(BaseModel):
    response: ComposeFromIntentResponse
    lowered_intent_request: ComposeFromIntentRequest
```

**Option C: Return the lowered request only through a separate fetch endpoint**

**Recommendation: Option A is the smallest honest implementation.** It requires:
- One new optional field on the existing response schema
- One line in `compose_from_selection()` or `_compose_handoff_sections()` to inject the lowered request into the response
- One harness-side change to read `response.persistable_intent_request` for the save call
- The field is self-documenting: it's `None` for intent-family (where the caller already owns the request) and populated for selection-family (where the analyzer owns the lowering)

Option B changes the response type for compose-from-selection, which would be a larger API contract change. Option C adds a round trip. Option A adds zero new endpoints, zero new response types, and one optional field.

The memo should name Option A (or whichever design is chosen) explicitly to prevent implementation ambiguity.

### Correction 2: The harness save call must change shape for `source_selection`

Currently (App.tsx:240-245), the save call sends `activeFixture.request` as the compose request:
```typescript
const session = await saveComposeSession({
    baseUrl: analyzerBaseUrl,
    composeRequest: activeFixture.request,  // <-- this is the wrong shape for source_selection
    composeResponse: state.response,
    planningDecisionId: activeFixture.planning_decision_id,
})
```

For `source_selection`, `activeFixture.request` is a `ComposeFromSelectionRequestPayload`, not a `ComposeFromIntentRequestPayload`. The save seam rejects this shape.

After the analyzer exposes the lowered request in the response, the harness save call must send `response.persistable_intent_request` (or equivalent) as the compose request. The memo should note this explicitly to prevent the implementor from trying to save the original selection request through the intent-shaped seam.

### Correction 3: The `saveComposeSession` TypeScript function signature needs attention

`transientClient.ts:152-178` types `composeRequest` as `ComposeFromIntentRequestPayload`. This is correct for the save call, but the harness currently only constructs this from `activeFixture.request`. For source_selection lifecycle, the harness will need to extract the lowered request from the compose response. The TS type `ComposeFromIntentApiResponse` at line 87-94 does not currently include a `persistable_intent_request` field. The type definition will need updating alongside the schema change.

### Correction 4: `source_v2_job_id` provenance must be included in the save call

The memo correctly notes (section 2, line 143-148) that provenance should include both `planning_decision_id` and `source_v2_job_id` for source_selection. The current `handleSaveSession` in App.tsx (line 240-245) omits `source_v2_job_id`. The implementation must ensure the harness sends `sourceV2JobId` from the fixture for AOI source_selection saves. The fixture already carries `source_v2_job_id = "job-744edf255ad5"` (visible in the proof bundle).

---

## Wording / Documentary Corrections

### Correction 5: Section 1 title is slightly misleading

The section says "Add one analyzer-owned lowered-request persistence bridge for `source_selection`." The word "bridge" might suggest a separate endpoint or intermediary. If the implementation is a single response field (Option A above), calling it a "persistence bridge" overstates it. Suggest: "Expose the analyzer-owned lowered intent request in the `compose-from-selection` response."

### Correction 6: The "acceptable fallback" framing is backwards

The memo says the preferred path is "expose one analyzer-owned persistable lowered request alongside the compose-from-selection response truth" and the fallback is "one tiny analyzer-owned save bridge dedicated to source_selection." In practice, the response-field approach IS the tiny dedicated bridge. They are the same thing, not alternatives. The fallback language creates unnecessary ambiguity.

### Correction 7: The memo should note that `lifecycleEnabled` gating in App.tsx will need broadening

Currently App.tsx:92 gates lifecycle to exactly `consumerKey === 'transient-proof-harness' && proofCase === 'genealogy_direct_sections'`. This slice must broaden that gate to also include `source_selection` while keeping the same consumer key constraint. This is a small but explicit code change that the memo should mention.

---

## What I Did NOT Find

- No evidence that a different step should come first
- No evidence that the save schema needs to become a union for this slice
- No evidence that `source_profile` should be in scope
- No evidence that the harness should locally reconstruct the lowered request
- No evidence that consumer identity should vary in this slice

---

## Bottom Line

The memo's diagnosis is sound, the strategic ordering is correct, and the scope boundaries are honest. The corrections above are all implementation-level: specify the concrete response-field design, ensure the harness save call sends the lowered request (not the original selection request), update TS types, include `source_v2_job_id` provenance, and broaden the `lifecycleEnabled` gate. None of these change the strategic direction.
