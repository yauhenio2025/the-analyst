# Review: Phase 4 Bounded Review Disposition Scope

Date: 2026-03-29
Reviewer: Claude (Opus 4.6)
Memo Under Review: `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_scope.md`

---

## 1. Verdict

**The memo is directionally correct and honest about its boundary.** Bounded review/disposition over exact `gate_decision_id` is genuinely the right next Stage 15 slice. The progression reports -> gates -> review/disposition is logically sound and each layer builds cleanly on the one below.

However, the memo has **three material gaps** that should be addressed before implementation:

1. It does not define **disposition-to-verdict alignment law** -- the rules about which dispositions are valid given the gate's actual verdict
2. It does not specify whether `contains_live_revalidation` is **derived from the referenced gate** or independently set by the reviewer (the latter is a dishonesty vector)
3. It does not name a **code-defined review definition** analogous to `gate_definitions.py`, despite implying one through the `review_definition_version` field

None of these gaps invalidate the scope direction. All three can be addressed in the implementation plan without widening.

---

## 2. Findings

### 2.1 Codebase claims are accurate

Every file path and capability claim in the memo checks out against the codebase:

- `src/evaluations/schemas.py` -- exists, defines `PersistedEvaluationReport` with the properties described
- `src/evaluations/report_store.py` -- exists, file-backed persistence with `list_evaluation_reports` newest-first
- `src/evaluations/frozen_pack_definitions.py` -- exists, defines `phase4_frozen_governance_v1`
- `src/evaluations/frozen_pack_harness.py` -- exists, deterministic CLI harness
- `src/evaluations/gate_schemas.py` -- exists, defines `PersistedEvaluationGateDecision` with `gate_decision_id`, `overall_verdict`, `rule_table`, `case_summaries`, `blocking_reasons`
- `src/evaluations/gate_store.py` -- exists, file-backed persistence at `src/evaluations/gates/`
- `src/evaluations/gate_definitions.py` -- exists, defines `bounded_platform_readiness_v1` over `phase4_frozen_governance_v1`
- `src/evaluations/gate_builder.py` -- exists, CLI harness with `--gate-key`, `--pack-key`, `--report-id`, `--generate-pack-reports`
- `src/api/routes/evaluations.py` -- exists, read-only routes for both reports and gates
- Two real persisted gate decisions exist: `gate-decision-22daa53ac747.json` and `gate-decision-745c2cb7e090.json`

The memo's "what does not yet exist" claims are also accurate: there is no review/disposition object, store, write path, or inspection route anywhere in the codebase.

### 2.2 The progression is structurally sound

The three-layer governance stack is clean:

| Layer | Object | Authority | Status |
|-------|--------|-----------|--------|
| Evidence | `PersistedEvaluationReport` | Machine (deterministic checks) | Exists |
| Enforcement | `PersistedEvaluationGateDecision` | Machine (deterministic rule table) | Exists |
| Disposition | `PersistedEvaluationReviewDecision` | Human/operator | **Proposed** |

Each layer cites exact ids from the layer below. Reports cite evidence refs. Gates cite exact report ids. Reviews would cite exact gate decision ids. This is honest layering.

### 2.3 Including `waive` in v1 is correct

The memo asks whether `waive` should be in the first slice or deferred.

**`waive` is required in v1.** Without it, the disposition law is incomplete for the most important real-world case: the gate fails, but the operator consciously decides to proceed anyway with written rationale.

- `accept` a failing gate would be dishonest
- `reject` a failing gate only says "not good enough" -- it doesn't say "I know it's not passing, but I'm proceeding anyway for these reasons"
- `waive` with mandatory rationale is the honest bounded path for that case

The three-value law `{accept, reject, waive}` is the minimum complete set. Removing `waive` would create pressure to dishonestly use `accept` on non-passing gates.

### 2.4 CLI-only write + read-only HTTP is the right first boundary

This matches the established pattern:

- `frozen_pack_harness.py` -- CLI only, no HTTP mutation route
- `gate_builder.py` -- CLI only, no HTTP mutation route
- Both have read-only HTTP inspection via `src/api/routes/evaluations.py`

The review disposition is different (human-originated vs machine-generated), but the CLI-first boundary is still correct for v1 because:

- It preserves the deliberate write-path discipline
- It avoids auth/identity product work
- It keeps the first slice inspectable without building UI
- HTTP mutation can be added later as a separate bounded follow-on

### 2.5 The retrospective frozen-pack honesty framing is adequate

The memo is explicit that this is still retrospective frozen-pack governance, not fresh live release approval. The `contains_live_revalidation: bool` label carries forward from the gate. The "must not widen" section correctly excludes fresh live-rerun campaigns.

This is honest enough -- but see Finding 2.6 for the gap about how that label should propagate.

### 2.6 GAP: Disposition-to-verdict alignment law is missing

This is the memo's most significant gap.

The memo says the review object should carry "observed gate verdict at decision time" but does not define **which dispositions are valid for which verdicts.** Without this, the disposition law has a dishonesty vector.

Proposed bounded alignment law:

| Gate Verdict | `accept` | `reject` | `waive` |
|-------------|----------|----------|---------|
| `pass` | Valid | Valid | Invalid (nothing to waive) |
| `fail` | Invalid (dishonest) | Valid | Valid (requires rationale) |
| `error` | Invalid (dishonest) | Valid | Valid (requires rationale) |

The write path should enforce this at creation time, not leave it to convention.

This is not a scope widening -- it is a required completeness property of the disposition law. Without it, the first review decision could be `accept` on a failing gate, which undermines the entire governance stack.

### 2.7 GAP: `contains_live_revalidation` should be derived, not independently set

The memo lists `contains_live_revalidation` as a required property of the review object and describes it as "an honesty label." But it does not specify whether the reviewer sets this independently or whether it is derived from the referenced gate decision.

Looking at the persisted gate `gate-decision-745c2cb7e090.json` (line 12), the gate already carries `contains_live_revalidation: true`. The review object should **derive this from the referenced gate**, not allow the reviewer to set it independently.

If the reviewer could set `contains_live_revalidation: false` on a review targeting a gate that carries `contains_live_revalidation: true`, that is a dishonesty vector. The write path should read the gate's value and copy it into the review, not accept it as a freeform input.

### 2.8 GAP: No code-defined review definition named

The memo specifies a `review_definition_version` field on the review object but does not name a code-defined review definition analogous to `gate_definitions.py` (`src/evaluations/gate_definitions.py:14-52`).

The existing pattern is:

- `frozen_pack_definitions.py` defines packs
- `gate_definitions.py` defines gates with `EvaluationGateDefinition` objects

The review slice should follow this pattern with one code-defined review definition, for example:

- `src/evaluations/review_definitions.py`
- One definition like `bounded_platform_readiness_review_v1` over `bounded_platform_readiness_v1`

This definition should encode:

- The `review_definition_version`
- The target `gate_key`
- The disposition-to-verdict alignment law from Finding 2.6
- Whether rationale is required per disposition

Without this, `review_definition_version` is a free string with no source of truth.

### 2.9 Reviewer identity is underspecified

The memo says `reviewer_identity` is a required property but does not specify its shape. In v1 this should be a simple structured object (not a free string), at minimum:

- `reviewer_name: str`
- `reviewer_role: str` (e.g., "operator", "developer", "reviewer")

This keeps it thin without requiring auth infrastructure, but prevents completely anonymous or untraceable dispositions.

### 2.10 Accumulation policy is clear and correct

The memo correctly specifies:

- Multiple dispositions over the same `gate_decision_id` are allowed
- Newest-first ordering
- No "active reviewer" model in v1

This matches the accumulation pattern in both `report_store.py` and `gate_store.py`. The implementation should follow the same `list -> sort -> limit` pattern.

### 2.11 Anti-drift filter passes

Testing the memo against the fixed-direction prioritization filter from `MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`:

1. **Does this move analytical decision-making upstream into analyzer-v2?** Yes -- governance disposition recording stays analyzer-owned
2. **Does this reduce consumer-owned workflow-specific intelligence?** Yes -- no host UI needed
3. **Does this generalize beyond AOI or beyond the-critic?** Yes -- the review object targets gate decisions, which already span both AOI and genealogy cases
4. **If we fully replaced the current app later, would this work still matter?** Yes -- the review/disposition substrate is host-independent

All four pass. This is not drift.

---

## 3. Open Questions

### 3.1 Should the first review definition be scoped to one specific gate key?

The gate definitions are scoped: `bounded_platform_readiness_v1` applies only to `phase4_frozen_governance_v1`. Should the first review definition similarly be scoped to only `bounded_platform_readiness_v1`, or should it accept any valid `gate_decision_id`?

**Recommendation**: Scope it. One review definition targeting one gate key, just like the gate definitions. This prevents the first slice from accidentally becoming a generic review platform.

### 3.2 Should `waive` require minimum rationale length?

The memo says `waive` records "one explicit bounded exception against the gate outcome with written rationale." But it doesn't specify a minimum rationale length or quality bar. In v1, should the write path reject empty rationale on `waive`?

**Recommendation**: Yes, require non-empty rationale for `waive`. No length minimum -- just not empty. This is a simple validation, not a scope widening.

### 3.3 Should the review object carry the full observed gate verdict snapshot or just the verdict string?

The memo says "observed gate verdict at decision time." Should this be just `overall_verdict: str`, or should it also capture the per-case summaries from the gate?

**Recommendation**: Just the overall verdict plus `gate_key`, `gate_definition_version`, and `evaluation_pack_key` -- enough to verify alignment, but not a second truth store. The full gate payload is already in the referenced `gate_decision_id`.

### 3.4 Should blocking/waiver reasons be structured or free-text?

The memo says "ordered blocking or waiver reasons where relevant." The gate `blocking_reasons` are structured strings. Should review `waiver_reasons` follow the same pattern?

**Recommendation**: Free-text list of strings, same shape as `blocking_reasons` on the gate. No structured schema needed in v1.

---

## 4. Concrete Revisions

The following revisions should be applied to the scope memo before implementation planning:

### Revision 1: Add disposition-to-verdict alignment law

In section "2. One fixed bounded disposition law," add:

> The disposition law should enforce alignment with the observed gate verdict:
>
> - `accept` is valid only when the observed gate verdict is `pass`
> - `reject` is valid for any gate verdict
> - `waive` is valid only when the observed gate verdict is not `pass`, and requires non-empty rationale
>
> The write path must fail closed if the disposition violates this alignment.

### Revision 2: Specify `contains_live_revalidation` as derived

In section "1. One analyzer-owned review/disposition object and store," change:

> `contains_live_revalidation`

to:

> `contains_live_revalidation` -- derived from the referenced gate decision at write time, not independently settable by the reviewer

### Revision 3: Name the code-defined review definition

Add to section "2. One fixed bounded disposition law":

> The disposition law should be encoded in one code-defined review definition, for example in `src/evaluations/review_definitions.py`, parallel to `gate_definitions.py`. The definition should encode the target `gate_key`, the disposition-to-verdict alignment law, and the `review_definition_version`. The `review_definition_version` field on the persisted object should cite this definition, not be a freeform string.

### Revision 4: Specify minimum reviewer identity shape

In section "1. One analyzer-owned review/disposition object and store," expand `reviewer_identity` to:

> `reviewer_identity` -- a thin structured object with at minimum `reviewer_name: str` and `reviewer_role: str`, not a bare freeform string

### Revision 5: Add "must land" item for disposition-to-verdict enforcement

Add to the "Must land" section:

> 6. the write path fails closed if the disposition violates the disposition-to-verdict alignment law (e.g., `accept` on a non-passing gate, `waive` without rationale)

### Revision 6: Add "must not widen" item for reviewer identity

Add to the "Must not widen" section:

> - do not build auth, identity management, or multi-user reviewer workflow in this slice; reviewer identity is a thin self-reported structured label

---

## Summary

The memo correctly identifies review/disposition as the next governance seam. The three-value disposition law `{accept, reject, waive}` is the right minimum complete set. CLI-only write with read-only HTTP inspection matches the established pattern and is the honest first boundary.

The three material gaps (disposition-to-verdict alignment law, derived `contains_live_revalidation`, code-defined review definition) are all addressable without scope widening. With the six revisions above applied, this memo is ready for implementation planning.
