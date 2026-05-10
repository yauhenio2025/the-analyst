# Review: Phase 4 Bounded Disposition Resolution Scope

Reviewer: Claude Opus 4.6
Date: 2026-03-29
Memo under review: `communications/MEMO_2026-03-29_phase4_bounded_disposition_resolution_scope.md`

---

## 1. Verdict

**The memo is directionally correct but has one structural gap that should be named before implementation.**

The proposed bounded current-disposition resolution object is the right next governance seam. The layering is sound: reports -> gates -> reviews -> resolution. The memo correctly avoids widening into product UI, broad override frameworks, or silent latest-wins conventions. The codebase claims are accurate and the anti-drift filter passes.

However, the memo does not sufficiently confront one question: **what does "current adopted governance stance" actually unlock or change in the system's behavior?** The resolution object records that someone adopted a review as current, but nothing in the codebase or in the memo consumes that resolution to gate any downstream behavior. That makes the resolution object honest-but-inert in exactly the same way that the review object is honest-but-inert: it exists, it records intent, but nothing reads it to make a decision.

This is not a fatal problem. The governance stack is being built bottom-up, and it is legitimate to land the recording layer before adding consumption. But the memo should say so explicitly rather than leaving the reader to infer what "current adopted governance stance" means operationally.

---

## 2. Findings

### 2.1 Codebase claims are accurate

Every file path claimed in the memo exists and matches what the code contains:

- `src/evaluations/review_schemas.py` -- `PersistedEvaluationReviewDecision` with all claimed fields (verified)
- `src/evaluations/review_store.py` -- file-backed persistence under `src/evaluations/reviews/` (verified)
- `src/evaluations/review_definitions.py` -- `bounded_platform_readiness_review_v1` targeting `bounded_platform_readiness_v1` gate (verified)
- `src/evaluations/review_builder.py` -- CLI write path with exact-id contract, disposition-to-verdict alignment, fail-closed on mismatch (verified)
- `src/api/routes/evaluations.py` -- read-only routes at `/v1/evaluations/reviews/{id}` and `/v1/evaluations/reviews?...` (verified)
- `src/evaluations/reviews/review-decision-21edf9b955ee.json` -- real persisted accepting review over `gate-decision-745c2cb7e090` (verified)

The memo's claim that "no analyzer-owned current-disposition resolution object" exists is also confirmed: no `resolution` files, schemas, or stores exist anywhere in `src/evaluations/`. The word "resolution" does not appear in any evaluations module file.

### 2.2 The layering is sound and the next-slice argument is persuasive

The governance stack has grown in a clean bottom-up sequence:

1. **Reports** -- `PersistedEvaluationReport` (frozen-pack evidence)
2. **Gates** -- `PersistedEvaluationGateDecision` (deterministic machine verdict over reports)
3. **Reviews** -- `PersistedEvaluationReviewDecision` (human/operator disposition over one gate)
4. **Resolution** -- (proposed) current-stance adoption over one review

Each layer cites the exact id of the layer below. Each derives truth from the referenced object rather than accepting freeform input. This pattern is consistent and the memo correctly extends it.

The argument that "the system can list historical reviews but cannot say which is currently adopted" is real. There is only one persisted review right now (`review-decision-21edf9b955ee`), but the accumulation policy explicitly allows multiple reviews over the same gate, so the "which one is current?" question will become structurally ambiguous as soon as a second review is recorded.

### 2.3 The resolution object is honest-but-inert, and the memo should say so

This is the most important finding.

The existing review decision (`review-decision-21edf9b955ee`) already records `disposition: "accept"`. That acceptance is already an explicit human judgment. The proposed resolution object would record: "this specific review is the one we're currently standing behind."

But nothing in the system reads or consumes that resolution:

- No downstream route gates behavior on resolution state
- No composition, presentation, or lifecycle path checks "is there a current resolution?"
- No host contract exposes resolution-aware readiness
- The memo does not propose that the resolution unlock or prevent anything

This means the resolution object is a governance-recording layer, not a governance-enforcement layer. That is a legitimate architectural choice -- land the recording object first, wire consumption later -- but the memo positions the resolution as if it fills a functional gap ("the system cannot say which review is currently adopted"). In practice, the system also cannot *do* anything different based on that answer.

**Recommended revision**: Add an explicit subsection acknowledging that the resolution is recording-only in v1 and that no downstream consumption path is proposed in this slice. This is the same honesty discipline the review scope memo applied to `waive` ("recording-only in v1").

### 2.4 "Current adopted stance" needs a clearer operational definition

The memo uses "current adopted governance stance" and "currently adopted as the governing stance" but does not define what this means operationally beyond "the newest persisted resolution for the same review scope."

Questions the memo should answer explicitly:

- **What is "the same review scope"?** Is it scoped by `gate_decision_id`? By `gate_key`? By `evaluation_pack_key`? The memo says "multiple resolutions over the same `gate_decision_id` are allowed" but also says "the current adopted stance is the newest persisted resolution for the same review scope." These need to be the same thing or the difference needs to be named.

- **Is the "current" derivation a query-time convention or a persisted flag?** The memo says "current = newest for the same scope" which is a query-time derivation. That's fine, but it means the resolution object does not itself carry a `is_current: true` flag. This should be stated explicitly to prevent an implementor from adding one.

- **What happens when a resolution over review-A exists, then a new review-B is recorded, then someone resolves review-B?** Is the old resolution over review-A now stale? Is it superseded? The accumulation policy says "newest persisted resolution" is current, but the two resolutions point to different reviews which point to the same gate. This is the actual ambiguity the memo should nail down.

### 2.5 The anti-drift filter passes, but barely

The memo correctly applies the four-question filter from the fixed-direction roadmap. But question 4 is worth stress-testing:

> "If we fully replaced the current app later, would this work still matter?"

The honest answer is: maybe. A resolution object over frozen-pack retrospective governance for `phase4_frozen_governance_v1` is tightly coupled to the specific proof campaign that produced this exact governance pack. A replacement app would likely bring its own governance needs rather than inheriting resolution decisions over a frozen AOI exemplar closeout pack.

The resolution object *structure* and *pattern* would transfer. The specific resolution *instance* (`bounded_platform_readiness_resolution_v1` over `bounded_platform_readiness_review_v1` over `bounded_platform_readiness_v1` over `phase4_frozen_governance_v1`) is almost certainly a dead-end artifact of the current proving campaign.

This is acceptable -- the review and gate objects have the same characteristic -- but the memo should be honest that the transferable value is the resolution *pattern*, not the specific frozen-pack resolution instance.

### 2.6 CLI-only write path with read-only HTTP is the right boundary

The memo's proposal to keep mutation in the CLI/harness and expose only read-only HTTP routes is consistent with the pattern established by the gate builder and review builder. Both `gate_builder.py` and `review_builder.py` are CLI-only write paths. The evaluations routes file is purely read-only. This is honest and appropriate for v1.

### 2.7 The proposed field list is mostly right but has one redundancy question

The proposed resolution object fields include both `review_decision_id` and derived fields like `review_key`, `review_definition_version`, `gate_decision_id`, `gate_key`, `gate_definition_version`, `evaluation_pack_key`. This is consistent with how the review object derives gate-linked fields.

However, the resolution also proposes:

- `derived reviewed disposition at resolution time`
- `derived observed gate verdict at resolution time`
- `derived contains_live_revalidation`

These are reasonable for auditability. But the memo should note explicitly that these are snapshot copies, not live lookups, to prevent confusion about whether the resolution "knows" the current state of the review versus the state at resolution time.

### 2.8 The compatibility validation is right

The proposed fail-closed rule: "a resolution is valid only when the referenced review matches the targeted `review_key`, `review_definition_version`, `gate_key`, and `evaluation_pack_key`" is consistent with how `review_builder.py:_validate_gate_against_review_definition` works for reviews over gates. The pattern transfers cleanly.

---

## 3. Open Questions

1. **What does "current resolution" unlock operationally?** If the answer is "nothing in v1, it's a recording layer," that is fine but should be stated. If the answer is "it will gate something later," what is that thing?

2. **What is the precise scope key for "current"?** Is a resolution "current" per `gate_decision_id`, per `gate_key`, per `evaluation_pack_key`, or per some combination? The memo should fix this before implementation.

3. **Can a resolution be recorded for a review with `disposition: "reject"`?** The memo says the resolution "adopts this exact review decision as the current governing stance." If the review disposition is `reject`, does adopting that rejection as the current stance mean "we currently reject the gate"? That would be valid governance recording, but the memo should be explicit about whether all three dispositions (`accept`, `reject`, `waive`) are resolvable.

4. **Is one review definition the only resolution target, or should the resolution definition target a `gate_key` that could have multiple review definitions?** Right now there is only one review definition (`bounded_platform_readiness_review_v1`), so this is moot. But the memo should state whether the resolution definition is 1:1 with a review definition or 1:1 with a gate definition.

5. **Does the resolution need a `resolution_action` field?** The memo says the bounded shape is "adopt this exact review decision as the current governing stance." Is that the only resolution action, or could there be others (e.g., "supersede," "rescind")? If it's always "adopt," the field is unnecessary. If multiple actions are foreseeable, the memo should say whether they're in or out of v1.

---

## 4. Concrete Revisions

### Revision 1: Add an explicit "recording-only in v1" honesty statement

After the resolution law section, add:

> This slice lands the resolution as a recording-only governance object. No downstream route, composition path, lifecycle operation, or host contract consumes the resolution to gate or change system behavior in v1. The resolution records which review is considered current; it does not enforce consequences of that currency. Downstream consumption is a legitimate future slice but is explicitly out of scope here.

This mirrors the honesty discipline applied to `waive` in the review scope memo.

### Revision 2: Define "same review scope" precisely

Replace the ambiguous "the current adopted stance is the newest persisted resolution for the same review scope" with something like:

> The current adopted stance for a given `gate_decision_id` is the newest persisted resolution whose `gate_decision_id` matches. Resolutions over different `gate_decision_id` values are independent.

Or if the intent is broader (per `gate_key` or per `evaluation_pack_key`), say so. Pick one and be explicit.

### Revision 3: State whether all three dispositions are resolvable

Add a sentence clarifying:

> A resolution may adopt any review decision regardless of its `disposition`. Adopting a `reject` review means "the current governance stance is rejection." Adopting a `waive` review means "the current governance stance is the recorded waiver." The resolution does not reinterpret the disposition.

Or if only `accept` reviews are resolvable, say that and state why.

### Revision 4: State that "current" is a query-time derivation, not a persisted flag

Add:

> The "current" resolution is determined by query-time ordering (newest-first for a given scope), not by a mutable `is_current` flag on the resolution object. There is no supersession mutation in v1.

### Revision 5: Acknowledge that transferable value is the pattern, not the instance

In the anti-drift section or the strategic decision, add one sentence:

> The transferable value of this slice is the resolution pattern and store, not the specific `bounded_platform_readiness_resolution_v1` instance, which is tightly coupled to the current frozen proving campaign.

---

## Summary

The memo is well-structured, codebase-accurate, and correctly extends the governance stack. The main weakness is that it positions the resolution as filling a functional gap without acknowledging that the gap is informational (recording "which review is current") rather than operational (nothing consumes that answer to change behavior). Making that distinction explicit would bring the memo to the same honesty standard the prior review-disposition scope memo achieved.

The five concrete revisions above are all additive -- none changes the proposed scope or architecture, they only tighten the memo's self-awareness about what the resolution object actually is and is not in v1.
