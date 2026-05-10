# Review: Phase 4 Bounded Current Governance Status Scope

Reviewer: Claude Opus 4.6
Date: 2026-03-29
Subject: `communications/MEMO_2026-03-29_phase4_bounded_current_governance_status_scope.md`

---

## 1. Verdict

**Conditionally approve with significant scope tightening.**

The memo correctly identifies that the next governance seam should be a thin derived status object rather than a new write layer or enforcement system. The honesty framing is sound. But the memo overstates the "stitching problem" that justifies a new object, because the existing `/v1/evaluations/resolutions/current` endpoint already serves almost everything the proposed status object would contain. The real incremental value is narrower than the memo admits: runtime chain-existence verification and a more semantically explicit retrieval shape. That narrower value is still worth landing, but the memo should be honest about what it actually adds versus what already exists.

---

## 2. Findings

### 2.1 The "stitching problem" is largely already solved

The memo's central justification is that callers currently need to "stitch together multiple persisted governance objects locally" (line 3, section "Why this is now the right next slice"). This claim is substantially overstated.

The existing endpoint `GET /v1/evaluations/resolutions/current?resolution_key=...&gate_decision_id=...` (registered at `src/api/routes/evaluations.py:138-164`) already returns a `PersistedEvaluationDispositionResolution` that contains:

- `adopted_review_disposition` (the effective stance)
- `observed_gate_verdict` (the gate outcome)
- `review_decision_id`, `gate_decision_id` (the exact backing chain)
- `review_key`, `gate_key`, `review_definition_version`, `gate_definition_version`
- `evaluation_pack_key`
- `contains_live_revalidation` (the honesty marker)

Verified in the live persisted object (`src/evaluations/resolutions/resolution-4738c6e0efab.json`): this is already one thin object that a caller can read without stitching reports, gates, reviews, and resolutions separately.

A caller hitting `/resolutions/current` today already gets the effective current governance stance, the exact backing chain identities, and the honesty marker. The only "stitching" they'd need to do is if they wanted the full review rationale or full gate case summaries — but the proposed status object explicitly says it won't duplicate those payloads either (line 179: "should not duplicate full resolution, review, or gate payloads").

**The memo should be rewritten to acknowledge that the current resolution endpoint already solves most of the stitching problem, and reframe the status object's value around what it genuinely adds.**

### 2.2 What the status object genuinely adds (narrower than claimed)

After code verification, the real incremental value of the proposed status seam is:

1. **Runtime chain-existence verification**: The current `/resolutions/current` endpoint returns the resolution object without re-verifying that the referenced review and gate still exist. The proposed derivation law would load the review and gate at retrieval time and fail closed if either is missing. This is a real (if small) correctness improvement.

2. **Runtime chain-consistency verification**: The resolution stores derived fields (`review_key`, `gate_key`, etc.) copied at write time. The proposed derivation would re-verify these match the underlying objects. In practice, the only way they could diverge is data corruption (manual file edits or file deletion), not normal operation — because the builder already enforces consistency at write time (`src/evaluations/resolution_builder.py`). Still, having a retrieval-time consistency check is a legitimate defense-in-depth measure.

3. **An explicit scope/honesty label in the served object**: The resolution definition carries `scope_label: "retrospective_frozen_pack_resolution"` (`src/evaluations/resolution_definitions.py:17`), but this label is not surfaced in the served resolution object. The proposed status object would make this visible to callers. This is a genuine if minor improvement.

4. **Semantic path clarity**: `GET /v1/evaluations/governance-status/current` is more legible to future consumers than `GET /v1/evaluations/resolutions/current`. The former says "what is the current governance situation?" while the latter says "what is the current resolution?" — slightly different semantic registers.

None of these are wrong to pursue. But the memo frames this as closing a major "still missing" gap, when the real gap is incremental hardening and semantic clarity over an already-functional seam.

### 2.3 Derived-only is unambiguously correct

The memo's decision to make the status object derived rather than persisted (line 153: "derived, not persisted as a new write-layer truth object") is correct for a clear reason: the status is a projection of already-persisted truth. If a new resolution is recorded, the status should automatically reflect it. Persisting the status would create a cache-coherence problem where the persisted status could become stale relative to the underlying resolution. The memo got this right.

### 2.4 The fail-closed chain consistency check needs sharper specification

The memo says the derivation should "fail closed if the chain is inconsistent" on `resolution_key`, `review_key`, `review_definition_version`, `gate_key`, `gate_definition_version`, and `evaluation_pack_key` (lines 191-198).

But it does not specify what "inconsistent" means in practice. There are two possible interpretations:

**Interpretation A**: The resolution's stored fields don't match the referenced review/gate objects on disk. This could only happen through data corruption, since the builder enforces consistency at write time. The check would be: load the review by `review_decision_id`, confirm its `review_key == resolution.review_key`, etc.

**Interpretation B**: The resolution definition's declared chain doesn't match the resolution's stored chain. This would be: load `EvaluationDispositionResolutionDefinition` by `resolution_key`, confirm its `review_key == resolution.review_key`, etc.

The memo should specify which interpretation applies. Given that the resolution definition is code-defined and immutable (`src/evaluations/resolution_definitions.py`), Interpretation B is a static check that should always pass for any correctly-built resolution. Interpretation A is the runtime check that provides real defense-in-depth.

### 2.5 `resolution_key + gate_decision_id` remains the correct scope

The memo proposes keeping `resolution_key + gate_decision_id` as the scope boundary for the first governance-status seam. This is correct. It matches the existing current-resolution accessor (`src/evaluations/resolution_store.py:51-76`). The alternative — broadening scope to `evaluation_pack_key` or something wider — would require multi-gate resolution semantics that don't exist yet and shouldn't be introduced in this slice.

### 2.6 The proposed field list is mostly redundant with the current resolution

Comparing the proposed status fields (lines 162-176) with `PersistedEvaluationDispositionResolution` (`src/evaluations/resolution_schemas.py:16-32`):

| Proposed status field | Already on resolution? |
|---|---|
| `resolution_key` | Yes |
| `gate_decision_id` | Yes |
| `current_resolution_id` | Yes (it IS the resolution_id) |
| `current_review_decision_id` | Yes (`review_decision_id`) |
| `current_gate_decision_id` | Yes (`gate_decision_id`) |
| `resolution_definition_version` | Yes |
| `review_key` | Yes |
| `review_definition_version` | Yes |
| `gate_key` | Yes |
| `gate_definition_version` | Yes |
| `evaluation_pack_key` | Yes |
| `adopted_review_disposition` | Yes (`adopted_review_disposition`) |
| `observed_gate_verdict` | Yes |
| `contains_live_revalidation` | Yes |
| **scope/honesty label** | **No** (only on definition) |

The only genuinely new field is the explicit scope/honesty label. Everything else is either identical to or a trivial rename of existing resolution fields.

### 2.7 The honesty framing is sound

The memo is consistently honest that this is:
- descriptive, not enforcement (lines 37-39)
- read-only in v1 (line 138)
- retrospective frozen-pack governance (line 176)
- not an override system, not a deploy/unlock gate (lines 248-254)

This framing is appropriate and the anti-drift filter application is correct.

### 2.8 The memo does not address whether this closes Phase 4

Review question 5 in the memo asks: "whether Stage 15 could close after this seam, or whether the memo is still missing another prerequisite."

The memo does not attempt to answer this question. The fixed-direction roadmap (`MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`, Phase 4 exit test, line 432) says Phase 4 is complete when "governance sits on top of a genuinely more general analyzer-owned platform rather than just a complex AOI proving harness."

By that standard, Phase 4 cannot close after just this seam, because the entire evaluation/governance infrastructure is still scoped to exactly one frozen pack (`phase4_frozen_governance_v1`) with exactly one gate, one review, and one resolution definition. There is no second pack, no second gate definition, no second scope that would prove the governance substrate generalizes. The memo should acknowledge this instead of leaving the question open.

---

## 3. Open Questions

1. **Is the marginal value of a new route over the existing `/resolutions/current` endpoint large enough to justify a new substrate layer?** The retrieval-time chain verification could instead be added directly to the existing `/resolutions/current` endpoint as a hardening pass, without a new object type or route.

2. **Should the chain-consistency check load the underlying review and gate objects, or only verify they exist?** Full field-comparison is more defensive but also more I/O. Existence-only is cheaper but less thorough. The memo should decide.

3. **What happens when the status derivation fails closed — does the route return 404, 409, or 500?** Missing resolution is clearly 404. But "chain inconsistent" (resolution references a review that has a different `review_key` than expected) is a data-corruption signal, not a "not found" situation. The memo should specify the error shape.

4. **Would adding the scope/honesty label to the existing `EvaluationCurrentDispositionResolutionResponse` instead of building a new object achieve 80% of the goal at 20% of the cost?** The existing response type (`src/evaluations/resolution_schemas.py:55-58`) could be extended with `scope_label` and `chain_verified: bool` fields without creating a new governance-status concept.

5. **After this seam lands, what is the next Phase 4 slice?** The memo says "next artifact" but doesn't give direction on whether Phase 4 is approaching closure or still has significant remaining work. The fixed-direction roadmap's exit test suggests the latter.

---

## 4. Concrete Revisions

### Revision 1: Reframe the justification honestly

Replace the "callers currently need to stitch multiple objects" argument with a more honest framing:

> The current `/v1/evaluations/resolutions/current` endpoint already serves the effective stance and full chain identity in one object. The governance-status seam adds retrieval-time chain verification (fail closed when referenced review or gate is missing or inconsistent) and an explicit scope/honesty label in the served object. It does not solve a stitching problem that still exists — it hardens a seam that already works.

### Revision 2: Specify the chain-consistency check precisely

Add to section 2 (derivation law):

- Load the review by `current_resolution.review_decision_id`; if missing, fail closed
- Load the gate by `current_resolution.gate_decision_id`; if missing, fail closed
- Verify `resolution.review_key == loaded_review.review_key`; if mismatch, fail closed
- Verify `resolution.gate_key == loaded_gate.gate_key`; if mismatch, fail closed
- Specify the HTTP error code for chain-inconsistency failures (recommend 409 Conflict, not 500)

### Revision 3: Acknowledge the overlap with the existing current-resolution response

The memo should have a section titled "Relation to existing `/resolutions/current` seam" that explicitly says:

- The existing seam already serves the current resolution with full chain identity
- The proposed status seam adds: (a) chain-existence verification, (b) chain-consistency verification, (c) the scope/honesty label as a first-class field
- Future consumers should use the governance-status route for the authoritative "what is the governance situation?" query, and the resolution route for direct resolution inspection

### Revision 4: Drop redundant fields from the proposed object

Instead of listing 16+ fields that are mostly copied from the resolution, the status object should either:

- **Option A**: Embed the full `PersistedEvaluationDispositionResolution` by reference (as the existing `EvaluationCurrentDispositionResolutionResponse` already does) plus the new `scope_label` and `chain_verified_at` fields
- **Option B**: Be defined as a thin wrapper: `{ scope_label, chain_verified_at, resolution: PersistedEvaluationDispositionResolution }`

Defining 16 fields that are identical copies of the resolution creates redundant schema surface for no gain.

### Revision 5: Add a Phase 4 closure horizon statement

The memo should explicitly say whether this seam is expected to close Phase 4 or whether further slices are anticipated. Based on the fixed-direction roadmap's exit test, it clearly cannot close Phase 4 alone. That's fine, but the memo should say so rather than leaving the question implicit.

### Revision 6: Consider the lighter alternative

Before committing to a new object type and route, the memo should explicitly evaluate whether extending the existing `EvaluationCurrentDispositionResolutionResponse` with `scope_label` and chain-verification logic achieves the same goal with less surface area. If the lighter alternative is rejected, the memo should state why.
