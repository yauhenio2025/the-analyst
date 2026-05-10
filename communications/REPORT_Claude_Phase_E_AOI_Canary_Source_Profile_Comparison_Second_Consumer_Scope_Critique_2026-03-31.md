# Critique: Phase E AOI Canary Source-Profile Comparison Second-Consumer Scope

Reviewer: Claude Opus 4.6
Date: 2026-03-31
Memo Under Review: `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_comparison_second_consumer_scope.md`

## Verdict: Approve

The memo is strategically sound, technically accurate against the codebase, well-scoped, and correctly sequenced within the Phase E generality proof line. The implementation gap is small and well-defined. Minor corrections and one implementation-critical constraint are noted below.

---

## Strategic Assessment

### Where the memo is strategically right

1. **Correct next step in the Phase E sequence.** The distilled strategic roadmap (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`, lines 256-260) explicitly names this exact slice as the next bounded step. The master roadmap's latest decision revision also calls for exactly this broadening. There is no misalignment between the memo and the strategic guidance.

2. **Correct priority over alternatives.** The memo is right that this is more honest than jumping to a non-AOI consumer proof or generic consumer architecture. Phase E's purpose is generality proof by representative substrate, and the current AOI `source_profile` route family still has an open preset gap. Closing the open gap on the same consumer, same route family, and same workflow before changing any of those three axes is the smallest variable change with the highest marginal proof value.

3. **Correct application of the "prefer representative matrices" rule.** Distilled roadmap Rule 4 says prefer matrix-broadening proofs. This slice broadens the profile-preset axis of the existing second-consumer proof matrix from 1/2 to 2/2. That is genuine matrix broadening, not exhaustive per-engine theater.

4. **Correct framing of what this does not prove.** The memo explicitly excludes non-AOI proof, compose-from-intent on aoi-canary, third consumers, and generic consumer-discovery. These are the right exclusions.

### Where the memo is overstated

1. **"Materially stronger than dossier because it exercises the broader AOI source-profile surface" (Section "Why comparison is the right next step", point 5).** This is true but somewhat overstated. The comparison profile requires 3 source families (`engagement_mapping`, `sin_findings`, `thematic_report`) vs. dossier's 2 (`thematic_synthesis`, `thematic_report`), so it does exercise more source diversity. But the *composition substrate* — the planner, view tree builder, and transient response normalization — is the same code path. The structural broadening is at the input/feasibility layer, not at the composition law layer. The claim is not wrong, but "materially stronger" is stronger language than warranted. More accurate: "exercises a broader source-family feasibility surface, which strengthens the proof that the composition law works across different source-family sets."

### Where the memo is too timid

1. **The memo does not state what closing this slice means for Phase E progress.** After this slice, the entire currently-defined AOI `source_profile` preset set (`dossier` + `comparison`) will be covered on the second consumer. The memo should state clearly what the *next* Phase E question is after this — whether that is a non-AOI second-consumer proof, a broader consumer architecture step, or closing Phase E entirely. Without that forward pointer, the next scope memo will repeat the same strategic orientation work.

---

## Codebase Verification

### Claim: "aoi-canary still rejects profile='comparison'"

**Verified correct.**

`src/presenter/compose_from_intent.py:173-176`:
```python
_REGISTERED_TRANSIENT_SOURCE_PROFILES_BY_CONSUMER = {
    TRANSIENT_COMPOSE_CONSUMER_KEY: frozenset({"dossier", "comparison"}),
    "aoi-canary": frozenset({"dossier"}),
}
```

The `comparison` profile is explicitly excluded from `aoi-canary`. The `get_transient_handoff_capability_error` function at line 558-578 checks this registry and returns a blocking error message when `profile='comparison'` is requested for `consumer_key='aoi-canary'`.

### Claim: "allowed_selectors for consumer_key=aoi-canary currently stop at ['dossier']"

**Verified correct.**

The `_build_aoi_readiness` function in `source_backed_readiness.py` iterates all profiles (line 141) and calls `get_transient_handoff_capability_error` (line 147-153) for each. Since comparison is blocked at the consumer adapter registry, `allowed_selectors` will contain only `['dossier']` for `aoi-canary`.

The dossier completion memo confirms the readiness output:
- `profile='dossier'` → `allowed_selectors=['dossier']`, `readiness_status=ready`
- `profile='comparison'` → `blocked_selectors['comparison']=["compose-from-source does not support consumer_key='aoi-canary' for profile='comparison'"]`

### Claim: "No third proof selector case exists in aoi-canary App.tsx"

**Verified correct.**

`aoi-canary/src/App.tsx:38`:
```typescript
type TransientProofCaseKey = 'source_selection' | 'source_profile_dossier'
```

Only two cases exist in `TRANSIENT_PROOF_CASES` (lines 181-184) and `TRANSIENT_PROOF_CASE_LABELS` (lines 185-188).

### Claim: "No pinned comparison fixture exists"

**Verified correct.**

Only one source-profile fixture exists: `src/fixtures/transient-aoi-source-profile-dossier.json`. No `*comparison*` fixture exists under `src/fixtures/`.

### Claim: "This slice does not need a new top-level canary mode, a new client architecture, or a new readiness concept"

**Verified correct.**

The existing `transientClient.ts` already has `composeFromSource()` (line 118-132) and `ComposeFromSourceRequestPayload` (lines 20-27) with `profile: 'dossier' | 'comparison'`. The `SourceProfileTransientProofFixture` type (line 51) is profile-agnostic. The canary's compose client is already general enough for comparison.

---

## Implementation-Critical Constraints

### 1. Canary-side binary branching logic is profile-unaware (CRITICAL)

The memo correctly identifies the four implementation gaps but misses a fifth: several functions in `aoi-canary/src/App.tsx` use binary branching that assumes the only source_profile case is dossier.

**`buildTransientStatusLabel` (line 367-368)**:
```typescript
const proofLabel = TRANSIENT_PROOF_CASE_LABELS[
  fixture.request_kind === 'source_selection' ? 'source_selection' : 'source_profile_dossier'
]
```

This maps ALL non-source_selection fixtures to the `source_profile_dossier` label. A comparison fixture would display the wrong label.

**`buildTransientSurfaceMessage` (lines 389-392)**:
```typescript
const requestDescription =
  fixture.request_kind === 'source_selection'
    ? 'compose-from-selection request fixture'
    : 'compose-from-source dossier request fixture'
```

This hardcodes "dossier" in the description for all source_profile fixtures.

**Correction needed in the memo**: Add a note under "What is still missing" that these binary-branching functions must be refactored to use the fixture's actual `request.profile` field instead of a binary `request_kind` check. This is not architectural — it is a straightforward labeling fix — but it will cause confusing proof output if overlooked.

### 2. Comparison needs different source families than dossier — verify pinned job up front

The memo correctly identifies this at Decision 5, but the specific risk is worth quantifying:

- **Dossier** requires: `thematic_synthesis` + `thematic_report` (2 families)
- **Comparison** requires: `engagement_mapping` + `sin_findings` + `thematic_report` (3 families)

The comparison profile needs `engagement_mapping` and `sin_findings`, neither of which is used by dossier. If the pinned job `job-744edf255ad5` does not have those families in an `available` state, the readiness layer will correctly report the profile as blocked, but the proof will fail.

The memo's Decision 5 handles this well. No correction needed — just emphasis that this validation is the critical-path gating step.

### 3. Expected raw_json leaf keys will likely differ

The dossier proof has `expected_raw_json_view_keys = ["compose_intent_02_aoi_thematic_report"]`. The comparison profile composes a different view tree (engagement_mapping + sin_findings + thematic_report) with different semantic roles, so the raw_json fallback leaf set may differ.

The fixture's `expected_raw_json_view_keys` must be determined empirically from the first successful compose-from-source call for comparison, not copied from the dossier fixture.

---

## Minor Corrections

1. **Fixture path in the memo uses "for example" language** (Decision 4): `transient-aoi-source-profile-comparison.json`. This is fine as a suggestion, but the implementor should keep the naming convention consistent with the existing `transient-aoi-source-profile-dossier.json`.

2. **Acceptance bar item 9** references "at most one raw_json leaf" and "the closeout/report leaf only." For comparison, the raw_json leaf identity may not be only the closeout — it depends on whether the card_grid_grouped renderer covers engagement_mapping and the accordion covers findings_bank. This acceptance criterion is still correct in spirit (bounded degradation law) but the specific leaf identity should be empirically validated.

---

## Assessment of Scope Decisions

| Decision | Assessment |
|----------|------------|
| 1: Broaden presenter and readiness together | Correct. The dossier slice proved these must move together. |
| 2: Keep readiness naming stable | Correct. Reopening naming is orthogonal drift. |
| 3: Reuse existing canary proof shell | Correct. No new mode needed. |
| 4: Keep fixture contracts distinct | Correct. Collapsing would lose type safety. |
| 5: Validate pinned job up front | Critical and correct. |
| 6: Keep proof bar live | Correct. Matches prior closeout standard. |

---

## Summary

The memo is approved as-is. The one correction that should be made before implementation is adding the canary-side binary-branching label logic to the "What is still missing" section, since overlooking it would produce misleading proof output. The implementation gap is otherwise small, well-defined, and correctly scoped.

The strategic direction is right: close the remaining preset on the same second consumer before changing any other axis. After this slice closes, the memo author should state what the next Phase E question is — the current memo ends without a forward pointer, which will cost orientation time in the next scope memo.
