# Critique: Phase D AOI Standalone Governance Family Scope

Reviewer: Claude Opus 4.6
Date: 2026-03-30
Subject: `communications/MEMO_2026-03-30_phase_d_aoi_standalone_governance_family_scope.md`

---

## Findings (Severity-Ordered)

### Finding 1: The memo is a near-duplicate of the prior Phase 4 scope memo [Medium]

The memo's subtitle claims it is "the first scoping memo grounded explicitly in the distilled strategic roadmap." In substance, it is a copy of `MEMO_2026-03-30_phase4_bounded_aoi_standalone_governance_family_scope.md` with:

- a new title framing (Phase D instead of Phase 4)
- the pack key prefix changed from `phase4_` to `phase_d_`
- a short new "Strategic Framing" section quoting the distilled roadmap
- an "Anti-Drift Justification" section that restates the roadmap's rules

The in-scope deliverables (sections 1-5), the out-of-scope list, and the honest expected outcome are materially identical. The gate, review, and resolution keys are character-for-character the same in both memos.

This is not a defect per se -- re-anchoring under the distilled roadmap is a valid act. But the memo overstates its novelty. It is a relabeling, not a strategic re-derivation.

**Recommendation**: Either (a) acknowledge the prior Phase 4 scope memo as the origin and explain why the relabeling matters, or (b) retire one of the two memos to avoid documentary confusion.

---

### Finding 2: Pack key prefix introduces a naming inconsistency with the existing codebase [Medium]

The memo recommends:

- `evaluation_pack_key = phase_d_aoi_exemplar_governance_v1`

Every existing governance object in the codebase uses the `phase4_` prefix:

- `phase4_frozen_governance_v1` (12 report files, 3 gate files, 2 review files, 2 resolution files, plus definition code)
- `phase4_genealogy_lifecycle_governance_v1` (same)

If the new family uses `phase_d_`, the pack namespace will contain a visible naming inconsistency: two families with `phase4_*` keys and one with `phase_d_*`. This is cosmetically minor but creates real confusion about which naming convention future families should follow.

**Recommendation**: Either use `phase4_aoi_exemplar_governance_v1` (matching the prior Phase 4 scope memo and the existing convention) or rename the existing families to `phase_d_*` at the same time. A mixed namespace is worse than either consistent choice.

---

### Finding 3: The Phase D exit signal is arguably already met in letter [Medium]

The distilled roadmap defines Phase D's exit signal as:

> analyzer-owned reports, gates, reviews, resolutions, and current governance status exist over more than one declared family

The current state already has two declared families:

1. `phase4_frozen_governance_v1` (composite AOI + genealogy)
2. `phase4_genealogy_lifecycle_governance_v1` (genealogy-only)

That is literally "more than one declared family."

The Phase D scope memo does not address this directly. It implicitly relies on the roadmap's "still missing" notes:

> - stronger cross-family reuse over distinct supported evaluator substrates
> - broader proof that governance is not still too coupled to the current proving campaign

Those notes justify the slice, but the memo should be explicit about the gap between the exit signal's letter (already met) and its spirit (not yet met, because both existing families lean on genealogy evidence). Without this, a reader who only checks the exit signal will wonder why Phase D is still open.

**Recommendation**: Add a short section acknowledging that the literal exit signal is met but the spirit demands cross-evaluator-substrate coverage before the claim is honest.

---

### Finding 4: "Broadens representative cross-family evidence" slightly overstates what's new [Low]

The anti-drift justification claims the slice "broadens representative cross-family evidence across the currently supported evaluator families." This is technically true at the family-topology level. But the underlying AOI evidence (`aoi_exemplar_march27_execution_backed`) is already frozen inside `phase4_frozen_governance_v1`.

What the slice actually proves is narrower and more honest: that an AOI-only pack/gate/review/resolution chain can stand alone as a declared governance family -- i.e., topology reuse on the second evaluator substrate, not new evidence territory.

The genealogy-only second family had the same characteristic (reusing evidence already in the composite pack). The memo is honest about this in the genealogy case but slightly less precise when describing the AOI case.

**Recommendation**: Tighten the anti-drift claim to say "proves standalone governance-family reuse over the second evaluator substrate" rather than implying new evidence breadth.

---

### Finding 5: The five deliverables are structurally identical to the genealogy-only slice [Low, informational]

The slice is:

1. One AOI-only frozen pack
2. One AOI-only gate
3. One AOI-only review
4. One AOI-only resolution
5. One real AOI-only chain materialized through the existing builders/routes

This mirrors the genealogy-only second-family slice exactly (pack + gate + review + resolution + chain). The memo does not highlight this structural repetition. This is fine -- it's the expected topology reuse -- but noting it would strengthen the claim that the governance substrate is genuinely parameterized rather than rebuilt each time.

---

### Finding 6: Codebase claims are accurate [Positive]

Verified against the live codebase:

| Claim | Status |
|-------|--------|
| `aoi_exemplar` is a supported evaluator family | TRUE - `frozen_pack_harness.py` lines 77-84 |
| March 27 AOI evidence is already pinned | TRUE - case `aoi_exemplar_march27_execution_backed` in `phase4_frozen_governance_v1` |
| No AOI-only standalone governance family exists yet | TRUE - only composite and genealogy-only packs exist |
| AOI dimensions are `selection_fit`, `rationale_clarity`, `rendered_usefulness`, `operational_behavior` | TRUE - gate_definitions.py lines 30-37 |
| Gate/review/resolution builders are parameterized by family keys | TRUE - verified in gate_builder.py, review_builder.py, resolution_builder.py |
| No new routes needed | TRUE - existing routes accept any valid keys |
| Current governance-status seam already serves both families | TRUE - governance_status.py uses resolution_key + gate_decision_id parameterization |

---

### Finding 7: Phase D vs Phase E distinction is correctly maintained [Positive]

The memo does not claim that this slice proves:

- arbitrary engine/pass composition
- broad routing/planning/composition governance
- anything that belongs to Phase E

The out-of-scope list is clean and correct. The honest expected outcome section explicitly disclaims Phase E territory. The Strategic Framing section correctly quotes the distilled roadmap's Phase D/E boundary.

---

### Finding 8: The slice is the right next bounded step [Positive]

Given the current state:

- Phase D's "still missing" items specifically call for "distinct supported evaluator substrates"
- The two supported substrates are `aoi_exemplar` and `genealogy_lifecycle`
- The genealogy-only standalone family exists; the AOI-only standalone family does not
- The governance builders/routes are already parameterized and should accept the new family without infrastructure changes

This is a clean, low-risk topology test that directly addresses the stated gap. No better next bounded step is obvious within Phase D's scope.

---

## Overall Verdict

The memo is **strategically honest and correctly scoped** for the next Phase D move. It correctly identifies what needs to happen (AOI-only standalone governance family) and correctly avoids claiming Phase E territory.

However, it has three real weaknesses:

1. **It presents itself as a new strategic derivation when it is essentially a relabeling** of the prior Phase 4 scope memo. The documentary lineage should be clearer.
2. **The pack key naming (`phase_d_` vs existing `phase4_`)** creates an unnecessary inconsistency. Pick one convention.
3. **The Phase D exit signal question is unaddressed**. The memo should explicitly state that the exit signal is met in letter but not in spirit, and explain why this slice closes the spirit gap.

None of these are blocking. The slice itself is correct and should proceed. The issues are presentational honesty gaps in the scoping document, not strategic errors.

**Bottom line**: Approve the slice. Fix the naming inconsistency before implementation. Add one paragraph addressing the exit-signal letter/spirit gap.
