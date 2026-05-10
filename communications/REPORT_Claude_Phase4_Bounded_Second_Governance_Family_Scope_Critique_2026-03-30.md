# Critique: Phase 4 Bounded Second Governance Family Scope

Date: 2026-03-30
Reviewer: Claude Opus 4.6
Subject: `communications/MEMO_2026-03-30_phase4_bounded_second_governance_family_scope.md`
Program: Dynamic Bespoke Apps Platformization

---

## 1. Verdict

**Conditionally approve with one structural revision and one honesty sharpening.**

The memo correctly identifies that the governance substrate is still single-family and that the next honest slice is not another new governance object type. The discipline against widening into product UI, downstream enforcement, or fresh live campaigns is well-applied and consistent with the program's anti-drift filter.

However, the proposed second family is weaker than the memo lets on. The proposed `phase4_genealogy_lifecycle_governance_v1` pack would evaluate the exact same frozen evidence (`compose-session-0877864dcca7`), the same frozen artifacts (the same four SHA-256-pinned proof files), and use the same evaluator implementation (`genealogy_lifecycle` at `frozen_pack_harness.py:85-92`) as the existing case already does inside `phase4_frozen_governance_v1`. The "second family" is a re-packaging of a subset of the first family's evidence under a different pack key, not a governance act over genuinely new territory.

That is still a valid architectural test: it proves the substrate is not topology-locked to one two-case composite. But the memo should not claim it proves "family-level reuse" without being explicit about what it does and does not test.

The memo should survive review and proceed to implementation, provided:

1. The honesty framing is revised to say this is a **topology and definition-reuse test**, not a "second governance campaign."
2. The Stage 15 closeout judgment is revised: landing this slice is necessary but probably not sufficient to close the bounded current Stage 15 line. The honest residual after this slice is that the governance stack has never governed a scope that was not already frozen evidence from the March 27-28 proving campaign.

---

## 2. What The Memo Gets Right

### 2.1 The substrate IS genuinely generic

This is the memo's strongest structural bet, and the codebase confirms it.

Verified against live code:

- `governance_status.py:25-94` is fully parameterized by `resolution_key` and `gate_decision_id`. No family-specific names appear.
- `gate_builder.py:26-88` takes `gate_key` and `evaluation_pack_key` as parameters. Loads definitions dynamically. No hardcoding.
- `review_builder.py:23-86` takes `review_key` and `gate_decision_id` as parameters. Fully data-driven.
- `resolution_builder.py:24-73` takes `resolution_key` and `review_decision_id` as parameters. Fully data-driven.
- All four stores (`gate_store.py`, `review_store.py`, `resolution_store.py`, `report_store.py`) support multi-family coexistence through field-level filtering, not pack-level namespacing.
- All API routes in `evaluations.py` are parameterized by query params, not hardcoded to specific definition keys.

This means the memo is correct that adding a second family is mostly a matter of adding new definitions to the `_PACKS`, `_GATE_DEFINITIONS`, `_REVIEW_DEFINITIONS`, and `_RESOLUTION_DEFINITIONS` dictionaries. The runtime infrastructure does not need structural changes.

### 2.2 Correct refusal to widen

The memo's "must not widen" list (no new persisted status layer, no UI, no downstream enforcement, no pack-global latest-governance law, no lifecycle or host-contract reopening) is directly aligned with the fixed-direction roadmap's anti-drift rules. Each of those would violate Rule 1 ("do not spend major effort polishing app-local behavior that is expected to disappear") or Rule 6 ("upstream accretion is still drift if it deepens coupling").

### 2.3 Correct refusal of new governance object types

The memo explicitly says the next step should not be "another new governance object type." This is the right call. The object chain (report -> gate -> review -> resolution -> status) is now complete as a vertical stack. The missing proof is horizontal reuse, not vertical depth.

### 2.4 Correct identification of what changed on March 30

The completion-memo chain is consistent: each slice (evaluation -> gate -> review -> resolution -> governance-status) advanced the boundary and each one correctly stated it did not close Phase 4. The March 30 current-governance-status completion did close the last vertical gap. The memo correctly reads the residual boundary as horizontal (one family only) rather than vertical (missing governance layers).

### 2.5 Evaluator dispatch works for the proposed case

The proposed second pack reuses the `genealogy_lifecycle_march28_session_reopen` case with `evaluator_key="genealogy_lifecycle"`. The harness dispatch at `frozen_pack_harness.py:85-92` already handles this evaluator. No new evaluator implementation is needed. The memo does not explicitly call this out but the choice avoids the one hardcoded bottleneck in the substrate.

---

## 3. Findings

### Finding 1: The "second family" reuses identical frozen evidence, which limits what it actually proves

**Severity: Structural honesty concern**

The proposed second pack `phase4_genealogy_lifecycle_governance_v1` would contain one case: `genealogy_lifecycle_march28_session_reopen`. That case is already one of the two cases in `phase4_frozen_governance_v1` (see `frozen_pack_definitions.py:91-126`).

The same frozen artifacts (SHA-256 hashes pinned at `frozen_pack_definitions.py:103-124`), the same `compose-session-0877864dcca7` subject, the same evaluator implementation, the same four genealogy dimensions (`identity_integrity`, `saved_truth_fidelity`, `reopen_integrity`, `boundary_observance`) would be evaluated by the harness.

What this proves:
- The definition layer accepts a different pack topology (single-case vs. two-case composite)
- The gate/review/resolution builders can be instantiated over different definition keys without code changes
- The governance-status seam can serve a second family without family-specific route modifications
- The substrate is not implicitly hardcoded to the AOI-plus-genealogy composite shape

What this does NOT prove:
- That the governance stack can evaluate genuinely new evidence
- That the stack works across different evaluator implementations
- That the gate substrate handles different dimension sets correctly (the proposed gate uses the same four genealogy dimensions)
- That the governance stack works on evidence from a scope other than the March 27-28 proving campaign

The memo's framing ("proving family-level reuse") is stronger than what the slice actually delivers. The honest framing is: proving definition-level and topology-level reuse of an already-exercised evaluator and evidence set.

### Finding 2: The Phase 4 exit test is broader than two-family existence

**Severity: Scope/closeout concern**

The fixed-direction roadmap's Phase 4 exit test (lines 431-433) says:

> This phase is complete only when governance sits on top of a genuinely more general analyzer-owned platform rather than just a complex AOI proving harness.

And the Phase 4 "must land" section (lines 421-424) says:

> - reviewable traces for routing/planning/composition decisions
> - bounded evaluation harnesses for routing, planning, readiness, and composition quality
> - explicit human override or inspection seams where they are required

The proposed second-family slice addresses only one dimension of the exit test: proving the governance definitions are reusable. It does not address:

- Governance over routing/planning/composition decisions (the current packs only govern frozen retrospective evidence, not live decision traces)
- Broader evaluation harnesses for different domains (routing quality, planning quality, composition quality)
- Whether the "explicit human override or inspection seams" are sufficient beyond the bounded recording-only review/resolution

So the memo's closing claim that "if that second-family slice lands honestly, it is the likely bounded closeout seam for the current Stage 15 line" is probably premature. A second pack from the same proving campaign is necessary but not sufficient for the Phase 4 exit test.

### Finding 3: The current roadmap already updated to prescribe exactly this slice

**Severity: Observation (positive)**

The fixed-direction roadmap was updated on March 30 (after the governance-status completion) to say at lines 337-339:

> - the next active main line remains Phase 4:
>   - one bounded second governance-family slice over a different declared pack/scope
> - do not reopen lifecycle design, revive the March 19 workspace line, or jump to override/product UI...

So this scope memo is directly aligned with the roadmap's current prescription. The memo is not making an independent strategic argument; it is filling in the concrete shape of an already-approved next step. That reduces strategic risk but also means the memo inherits the roadmap's own optimism about what a second family proves.

### Finding 4: The evaluator dispatch is the one non-generic seam, and the memo avoids it by design

**Severity: Observation (structural)**

The frozen pack harness at `frozen_pack_harness.py:77-93` is the one place in the substrate that hardcodes evaluator implementations:

```python
if case_definition.evaluator_key == "aoi_exemplar":
    return _evaluate_aoi_case(...)
if case_definition.evaluator_key == "genealogy_lifecycle":
    return _evaluate_genealogy_case(...)
raise ValueError(f"Unknown evaluator_key: {case_definition.evaluator_key}")
```

By choosing a genealogy-lifecycle-only second pack, the memo avoids needing to add a new evaluator implementation. This is pragmatically correct for a bounded slice. But it also means the second family does not test whether the harness is extensible to new evaluator types. The memo should acknowledge this as a known remaining gap for any future third-family consideration.

### Finding 5: The proposed gate dimensions are identical to the existing genealogy dimensions

**Severity: Minor honesty concern**

The memo proposes the second gate (`bounded_genealogy_lifecycle_readiness_v1`) require the same four dimensions already proven by the genealogy case in the first gate:

> - `identity_integrity`
> - `saved_truth_fidelity`
> - `reopen_integrity`
> - `boundary_observance`

This means the gate evaluation logic follows the same code paths with the same dimension names. It tests gate-definition instantiation but not gate-dimension-handling diversity. Again: a definition/topology test, not a substantive governance expansion.

### Finding 6: "Keeping Stage 15 open on one-family-only grounds" is honest

**Severity: Positive validation**

The memo's premise that Stage 15 should remain open because only one governance family exists is the correct read of the current boundary. The governance stack was built in a tightly coupled vertical chain over `phase4_frozen_governance_v1`. Every single persisted governance object (reports, gates, reviews, resolutions) references that one pack. Without at least one second family, there is no empirical evidence that the definition-driven design actually works for a second set of keys.

The alternative would be to argue that the substrate's generic code structure is sufficient evidence of reusability without a second materialized family. That argument is too weak. Generic-looking code that has never been exercised on a second input is unproven code.

---

## 4. Recommended Revisions

### Revision 1: Sharpen the honesty framing about what the second family proves

The memo should not say "proving family-level reuse" without qualification. It should say something closer to:

> This slice proves definition-level and topology-level reuse of the governance substrate. It does not prove that the stack can govern a genuinely new scope, new evidence, or new evaluator type. It proves the substrate is not structurally locked to one pack key, one gate key, one review key, and one resolution key. That is a necessary but not maximally ambitious proof.

This revision matters for documentary honesty. Future sessions that read only the completion memo should not believe the governance stack has been proven on a second independent governance campaign.

### Revision 2: Revise the Stage 15 closeout claim

The memo's final sentence says:

> If that second-family slice lands honestly, it is the likely bounded closeout seam for the current Stage 15 line.

This should be revised to:

> If this slice lands honestly, it closes the "single-family-only" criticism. But the Phase 4 exit test is broader: governance must sit on top of a genuinely more general platform. A second pack from the same proving campaign addresses definition reuse but does not address governance over live routing/planning/composition decisions, or broader evaluation domains. Stage 15 may need one additional honest boundary assessment after this slice lands before claiming bounded closeout.

### Revision 3: Acknowledge the evaluator-dispatch non-test

Add one sentence to the "current code-backed boundary" section acknowledging that the proposed case reuse deliberately avoids exercising the evaluator dispatch extensibility. This is fine for a bounded slice. But it should be visible so future sessions know the harness has not been proven extensible to a third evaluator type.

### Revision 4: Consider whether the materialization step needs a stronger signal

The memo says the slice must include "one real second-family materialization" (section 5). This is correct and necessary. But the memo should be more specific about what makes the materialization a meaningful test rather than a tautology.

Specifically: the materialization is meaningful because it proves that:
- `gate_builder.py` resolves a different gate definition against a different pack and produces a valid `PersistedEvaluationGateDecision`
- `review_builder.py` resolves a different review definition against the new gate decision
- `resolution_builder.py` resolves a different resolution definition against the new review decision
- `governance_status.py` derives status for the new resolution_key/gate_decision_id pair without family-specific code

The memo should call these out as the concrete verification criteria, not just "one report, one gate, one review, one resolution, one status read."

### No revision needed: the genealogy lifecycle choice is the right thin target

Despite the limitations above, the memo is correct that `genealogy_lifecycle_march28_session_reopen` is the right first second-family target. It is the thinnest existing evaluation case. An AOI-only pack would require the same evaluator dispatch and the same frozen evidence. Creating genuinely new evidence is explicitly and correctly out of scope. The only realistic bounded choices are subsets of existing frozen evidence, and a single-case genealogy pack is the cleanest topology change.

The alternative of waiting for genuinely new evidence before landing a second family would block this slice indefinitely and prevent the definition-reuse proof from happening at all. The memo makes the right pragmatic trade-off here.
