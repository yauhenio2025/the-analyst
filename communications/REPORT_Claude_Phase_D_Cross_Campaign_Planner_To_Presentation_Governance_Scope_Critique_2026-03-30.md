# Review: Phase D Cross-Campaign Planner-To-Presentation Governance Scope

Date: 2026-03-30
Reviewer: Claude Opus 4.6
Memo Under Review: `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_scope.md`

## Verdict: Approve With Revisions

The memo is honest, well-bounded, and strategically self-aware. It correctly identifies the next Phase D question as anti-coupling rather than capability existence. But it underestimates two things: (1) the real code-level cost of a "fresh campaign" on the genealogy side, and (2) the diminishing strategic return of staying in Phase D governance when the distilled roadmap's own anti-drift rules suggest it may be time to pivot toward Phase E.

The revisions needed are not rejections of the approach. They are corrections that would make the scope memo more honest about what "reusing the existing evaluator branch" actually means in the current codebase, and more explicit about the strategic opportunity cost.

---

## What The Memo Gets Right

### 1. Correct identification of the remaining Phase D question

The memo is right that the open question is no longer "can governance stand over planner-to-presentation surfaces" (that was answered by the first family). The remaining question is whether the governance law is too coupled to one specific proving-campaign lineage. That is a real Phase D question, not a disguised Phase E question.

### 2. Honest framing of what this is not

The memo is unusually careful about what it does not claim:

- not Phase E
- not a generic evaluator-plugin proof
- not a premature jump to matrix proof
- not live governance

That restraint is the right posture. The program has a recent history of governance slices accumulating faster than they advance the strategic line, and this memo avoids inflating its own claims.

### 3. The anti-coupling rule is the right test

The decision rule at the end (lines 241-247) is correctly stated: a renamed copy of the old proof files is not enough. The slice earns its keep only if it demonstrates the same governance law over a genuinely fresher proof campaign. That is the right standard.

### 4. Scope exclusions are appropriate

The out-of-scope list is correct: no generic proof-capture tooling, no live governance policy, no enforcement, no UI, no Phase E matrix. Those exclusions are exactly what the program needs to hold.

---

## Concrete Findings And Corrections

### Finding 1: "Reusing the existing evaluator branch" is softer than it appears (Implementation correction)

The memo says (line 91):

> this slice should reuse the existing `planner_presentation_decision` evaluator family

And (line 185):

> do not add a new evaluator family unless a concrete proof-shape requirement forces it

This claim is honest at the evaluator-key level but misleading at the code level.

The current `planner_presentation_decision` evaluator dispatches internally by **case_key strings**:

- `_PLANNER_PRESENTATION_CASE_SPECS` (frozen_pack_harness.py:137-177) is a hard-coded dict keyed by case_key
- `_extract_planner_presentation_evidence` (frozen_pack_harness.py:1555-1635) branches on case_key with entirely different extraction logic per branch
- The `_evaluate_planner_presentation_case` function (frozen_pack_harness.py:1170-1240) has an `if case_key == "aoi_compose_selection_current_contract": ... else: ...` dispatch

A "second fresh campaign" with new case_keys will require:

1. Two new entries in `_PLANNER_PRESENTATION_CASE_SPECS` with new expected values
2. Two new extraction branches in `_extract_planner_presentation_evidence` (especially if the fresh genealogy bundle has a different shape than the March 28 multi-surface trace)
3. The evaluator dispatch logic may need widening if the new case_keys don't match the existing if/else pattern

This is not "reusing unchanged." It is "extending the evaluator with new case-specific code." That distinction matters because:

- If the fresh genealogy bundle is a dedicated single-surface compose bundle (which the memo recommends on line 140), the extraction logic will be structurally different from the current genealogy path that reads from a multi-surface trace artifact
- The spec objects will need different `source_v2_job_id`, `compose_resolver_version`, and potentially different `compose_trace_stages`

**Revision needed**: The memo should acknowledge that "reusing the evaluator family" means adding new case entries and potentially new extraction branches, not running the existing code unchanged. This is still a much smaller lift than a new evaluator family, but the memo should not create the impression that zero evaluator code changes are expected.

### Finding 2: The fresh genealogy bundle will likely force a meaningful extraction redesign (Risk assessment)

The memo's recommended genealogy boundary (lines 140-141):

> prefer a fresh dedicated genealogy transient compose bundle over continued reliance on the March 28 multi-surface trace

This is the right recommendation, but the memo does not adequately reckon with the implementation consequence.

The current genealogy extraction (frozen_pack_harness.py:1609-1635) reads from:

- `trace_artifact.get("planning_decision", {})`
- `trace_artifact.get("planning_snapshot", {})`
- `trace_artifact.get("lowered_compose_request", {})`
- `trace_artifact.get("compose_response", {})`
- Plus a separate `snapshot_artifact` from the exported planning snapshot

A fresh dedicated genealogy compose bundle would need to supply these same surfaces but in a new JSON shape. Either:

- The fresh bundle uses the same top-level keys as the Phase 2 multi-surface trace (in which case the extraction works, but the bundle is essentially a structural copy of the old trace shape, weakening the "genuinely fresher" claim)
- The fresh bundle uses a different shape (in which case extraction code must change)

**Revision needed**: The memo should explicitly state whether the fresh genealogy compose bundle is expected to match the Phase 2 multi-surface trace shape or use a new shape. If the former, the memo should acknowledge that this weakens the "genuinely fresher" anti-coupling claim. If the latter, the memo should scope one bounded extraction adaptation as in-scope work.

### Finding 3: The anti-coupling proof is narrower than it sounds (Strategic assessment)

The memo frames this as proving that "the same governance law survives a second materially distinct proof campaign." But consider what "materially distinct" actually means here:

- Same two workflow families: `anxiety_of_influence_thematic_single_thinker` + `intellectual_genealogy`
- Same consumer: `the-critic`
- Same four governance dimensions: `handoff_contract_fidelity`, `planner_presentation_agreement`, `presentation_contract_fidelity`, `composition_trace_integrity`
- Same gate/review/resolution law
- Same governance-status derivation

The only things that differ are:

- Different artifact file names and hashes
- Different `planning_decision_id` values
- Different `source_v2_job_id` values
- Potentially different captured timestamps

This means the anti-coupling proof is really: "governance definitions can be parameterized by different artifact identities on the same proof shape." That is a valid proof, but it is a weaker form of anti-coupling than the memo's language suggests. True anti-coupling would survive a different proof *shape* — different workflow families, different compose entry paths, different dimension relevance.

**This is not a rejection.** The proof is still worth doing. But the honest claim afterward should be calibrated:

- Accurate: "governance law is not hard-wired to specific artifact identities"
- Too strong: "governance law survives materially distinct proof campaigns"

The latter requires different proof *families*, which is Phase E territory.

### Finding 4: The distilled roadmap's own rules suggest a pivot may be overdue (Strategic disagreement)

The distilled roadmap (which this memo cites as authoritative) contains four anti-drift rules:

1. Rule 1: Prefer upstream intelligence over downstream convenience
2. Rule 2: Do not confuse bounded proof with generalized architecture
3. Rule 3: Do not confuse governance with architecture
4. **Rule 4: Prefer representative matrices over exhaustive workflow theater**

This slice, measured against those rules:

- Rule 1: Neutral. This is neither upstream intelligence nor downstream convenience; it is governance verification.
- Rule 2: Passes. The memo is clear this is bounded.
- Rule 3: **Borderline.** The slice spends more program time on governance verification without creating new architectural capability. Rule 3 explicitly warns that governance "does not by itself create planner generality, UI composition generality, host thinness."
- Rule 4: **Fails.** A second campaign on the same two workflow families is closer to "exhaustive workflow theater" than "representative matrix broadening." A broader proof campaign across different workflow/output families would be more strategically aligned.

The Decision Heuristic (distilled roadmap lines 326-331) asks four questions before approving new work:

1. Does this move intelligence upstream into analyzer-v2? **No.**
2. Does this reduce host-specific analytical behavior? **No.**
3. Does this strengthen generic law rather than one more special case? **Marginally.**
4. Does this help eventual contract-based generality? **Only indirectly.**

By the roadmap's own filter, the answer pattern is "mostly no."

**This is a strategic disagreement, not an implementation correction.** The memo is well-crafted within its own frame. But the strategic question is whether Phase D has reached sufficient governance maturity to justify pivoting to Phase E, where anti-coupling would be proven as a natural byproduct of generality proof rather than as an isolated governance exercise.

---

## Answers To The Six Review Questions

### 1. Is this the right next Phase D slice, or is it drifting?

It is a valid Phase D slice. It is not drifting in the sense of being off-topic or inflated. But it is at the boundary where continuing to polish governance evidence before starting the generality proof risks becoming a form of strategic delay. The work is defensible but may not be the highest-value next step.

### 2. Is the memo honest about the distinction between anti-coupling proof and Phase E generality proof?

Yes, at the framing level. The memo is careful not to claim Phase E. However, it does not fully reckon with how narrow the anti-coupling proof is when both campaigns use the same workflow families, consumer, and governance dimensions. The claim should be calibrated to "governance is not artifact-identity-coupled" rather than "governance survives materially distinct campaigns."

### 3. Are the codebase claims and proof-surface claims accurate?

Mostly accurate with one important correction:

- **Accurate**: The governance-status derivation (`governance_status.py`) is genuinely generic. The gate/review/resolution chain is reusable. The proof artifacts exist and are hash-pinned.
- **Needs correction**: The claim that the slice "reuses the existing evaluator branch unchanged" is misleading. The evaluator dispatches by case_key, and new case_keys require new spec entries, new extraction branches, and potentially new dispatch logic. This is extension, not reuse.

### 4. Is reusing `planner_presentation_decision` the right default, or does the fresh genealogy side likely force a larger redesign?

Reusing the evaluator family is the right default. But the memo underestimates the code cost on the genealogy side. If the fresh genealogy bundle uses a different shape from the Phase 2 multi-surface trace, the extraction function will need a new branch. That is not a "larger redesign" but it is more than zero code change. The memo should scope this explicitly.

### 5. Is a fresh paired AOI+genealogy proof campaign the smallest honest next move?

It is the smallest honest next move *within the current governance line*. But it may not be the smallest honest next move *for the program*. A reasonable alternative is to declare Phase D "sufficiently advanced for bounded form" and begin Phase E with a minimal representative matrix, where the governance anti-coupling question would be answered by attempting governance over genuinely different proof families rather than the same families with different identities.

### 6. Is there a smaller or cleaner next step that would better serve the program?

Yes: declare Phase D "advanced enough" and begin a minimal Phase E proof that tests one new workflow family (not AOI, not genealogy) through the existing planner-to-presentation bridge. That would simultaneously:

- Prove governance anti-coupling (different proof family)
- Prove planner generality (new workflow)
- Advance the strategic line toward "analyzer-v2 as the brain"
- Satisfy the distilled roadmap's Rule 4 (matrix broadening over theater)

The cost is higher uncertainty — a new workflow family might expose contract gaps that force bridge repairs. But that is exactly the kind of work Phase E is designed for, and the current governance substrate is strong enough to survive it.

---

## Summary Of Required Revisions

If the slice proceeds as proposed:

1. **Acknowledge evaluator extension cost**: The memo should state that "reusing the evaluator" means adding new case spec entries and extraction branches, not running existing code unchanged.
2. **Decide the genealogy bundle shape question**: State explicitly whether the fresh genealogy bundle will match the Phase 2 multi-surface trace shape or use a new shape, and scope the extraction work accordingly.
3. **Calibrate the anti-coupling claim**: The honest claim after implementation should be "governance is not artifact-identity-coupled" rather than "governance survives materially distinct campaigns."

## Strategic Recommendation

The stronger move for the program is to consider whether Phase D can be declared "advanced enough in bounded form" and whether the next slice should be an early Phase E minimal matrix proof, where governance anti-coupling would be proven as a byproduct of genuine generality rather than as a standalone governance exercise. This is not a rejection of the current memo — it is a flag that the program may be spending governance time where it should be spending generality time.
