# Review (Pass 2): Draft Roadmap For The Next Platformization Stages

Reviewer: Claude Opus 4.6
Date: 2026-03-24
Pass: Second review (after revision incorporating first-pass feedback)
Draft under review: `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
Canonical roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

---

## Verdict

**Approved.**

The revised draft is now structurally sound, honestly scoped, and actionable. The six-tranche sequence is the right order. The tiered Stage 13 approach is the right structural decision. The "tranche" naming avoids canonical-number collision. The explicit de-AOI/de-`the-critic` tranche fills the most important gap from the first draft.

Two findings below should inform implementation scoping but do not block the draft from influencing the canonical roadmap.

---

## Findings (ordered by severity)

### Finding 1: Tranche 1 (Tier A) is real work, not a quick checkbox — MODERATE

**Severity**: Moderate (scope risk, not directional risk)

The draft says aoi-canary "already exists as a thin read-only second consumer" and frames Tier A as "the cheapest honest part." This is directionally correct, but the live codebase reveals that aoi-canary is further from a Host Contract v1 proof than the draft's framing suggests.

Current aoi-canary state:

- Uses **presenter convenience endpoints** (`/v1/presenter/page/{jobId}`), not the Host Contract v1 result families (`/v1/results/by-job/{job_id}/presentation`)
- Has **no Host Contract v1 infrastructure** — no typed contract, no runtime dispatch, no shared adapter layer
- Has **no run or result discovery** — takes a hardcoded `job_id` as input
- Has **no readiness checks** of any kind
- Implements only **3 of 7+ renderers** found in its own test fixtures (missing `rich_description_list`, `annotated_prose`, `mini_card_list`, `chip_grid`)
- Has **zero task-launch capability** (which is fine for Tier A but should be explicit)

So Tier A is not "just verify the existing canary against Host Contract v1." Tier A requires:

1. Switch data source from presenter endpoints to result-backed families
2. Add a minimal Host Contract v1 typed layer
3. Add result discovery or at least project-scoped result selection
4. Add the missing renderers (or fail closed honestly on unsupported types)
5. Thread consumer_key through all result-family calls (already done for presenter calls)

This is bounded and honest work — likely 2-3 sessions — but the draft should not let future sessions mistake it for a quick stamp.

**Recommended action**: Add a "known prerequisites" subsection under Tranche 1 listing the concrete gaps. This protects against an implementor reading "aoi-canary already exists" and expecting a 2-hour proof.

---

### Finding 2: The evaluation gate between Tranche 2 and Tranche 3 is implicit — MODERATE

**Severity**: Moderate (sequencing risk)

Tranche 2 (AOI exemplar) maps to canonical Stages 3+4+5, with Stage 5 being evaluation/ops guardrails. Tranche 3 (de-AOI substrate) begins bridge generalization.

The draft's exit evidence for Tranche 2 includes "a bounded AOI eval/guardrails memo proving the exemplar is stable enough to stand as a platform reference." This is the right bar.

But the draft does not explicitly state that **Tranche 3 should not begin until Tranche 2's evaluation gate is passed**. Without that gate, Tranche 3 could start while AOI exemplar quality is unmeasured, which risks generalizing a bridge whose reference exemplar is untested.

**Recommended action**: Add one sentence under Tranche 3: "This tranche should not begin until the AOI evaluation gate from Tranche 2 confirms that the exemplar is stable enough to serve as the reference for generalization."

---

### Finding 3: The Tier A / Tier B split is the right structural decision — POSITIVE

**Severity**: Positive

The tiered approach solves three problems at once:

1. **Credibility**: Tier A closes the long-deferred second-consumer gap without waiting for transient substrate generalization.
2. **Scope control**: Tier A is bounded enough to complete without reopening AOI composition or lifecycle.
3. **Honest dependency**: Tier B explicitly depends on Tranche 3 (de-AOI substrate), making the dependency chain visible instead of hiding it inside one oversized "generic host proof" tranche.

The split also correctly recognizes that result-backed and transient surfaces have different generalization paths. Result-backed rendering is already consumer-neutral in the API contracts (consumer_key is a request parameter). Transient compose is structurally locked to `the-critic`.

---

### Finding 4: `aoi-canary` is correctly treated as an existing near-ready second consumer — POSITIVE

**Severity**: Positive

The revised draft acknowledges aoi-canary explicitly and uses it as the vehicle for Tier A. This is the right call because:

- aoi-canary is registered in analyzer-v2 as `consumer_key: "aoi-canary"` with explicit renderer support
- aoi-canary already renders presenter output in a thin shell
- the consumer-adaptation machinery in analyzer-v2 already knows how to produce aoi-canary-compatible payloads

The remaining gap is infrastructure (switching from presenter to result-backed endpoints, adding Host Contract v1 layer), not analytical intelligence.

---

### Finding 5: The de-AOI/de-`the-critic` tranche (Tranche 3) is specific enough — POSITIVE

**Severity**: Positive

The first-pass review asked whether this tranche was specific enough. The revised draft lists four concrete deliverables:

1. Contract decision for transient compose consumer admission beyond `the-critic`
2. At least one non-AOI or more consumer-neutral composition-facing seam
3. Clearer relation between Host Contract v1/runtime and the task-launch layer
4. Explicit separation of host-neutral vs. composition-facing contract law

These are specific and testable. The first item directly targets the `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"` hard-lock in `compose_from_intent.py`. The third item addresses the honest gap that task-launch lives beside Host Contract v1 rather than inside it.

One observation: the tranche could be even more specific by naming the concrete code-level blockers (the consumer allowlist in `compose_from_intent.py`, the AOI-only workflow check, the hard-coded semantic role mappings). But that level of detail is appropriate for a scope memo, not a strategic roadmap.

---

### Finding 6: AOI exemplar completion is correctly placed before the de-AOI tranche — POSITIVE

**Severity**: Positive

The draft asks (open question #3) whether Tranche 2 and Tranche 3 should be reversed. The current ordering is correct:

1. **Reference quality**: Generalizing the substrate (Tranche 3) should be informed by what the AOI exemplar actually looks like when it is complete. If Tranche 3 goes first, it risks abstracting away AOI-specific patterns that turn out to be important.

2. **Evaluation evidence**: Tranche 2 includes evaluation and quality guardrails. That evidence should exist before deciding which patterns to generalize and which to discard.

3. **Regression anchor**: A complete, evaluated AOI exemplar serves as a regression anchor during substrate generalization. If something breaks during de-AOI work, the exemplar tests catch it.

---

### Finding 7: Lifecycle/governance deferral is correctly placed — POSITIVE

**Severity**: Positive

The draft correctly keeps lifecycle (Tranche 5) and governance (Tranche 6) behind structural work. The reasoning — "lifecycle semantics should rest on proven host and planner/presentation structure" — is sound and consistent with the canonical roadmap's own ordering.

The transient ephemeral-only constraint is now implicit in Tranche 1's "do not reopen lifecycle" guardrail. That is sufficient for the draft's purpose.

---

### Finding 8: The draft no longer overstates what has been proved — POSITIVE

**Severity**: Positive

The revised "Current Strategic Position" section now:

- Explicitly calls out that Host Contract v1/runtime "is not the whole host-neutral story yet"
- Notes that "task-launch adoption currently lives beside it rather than inside it"
- Distinguishes the narrower UI-composition vision from the broader analyzer-as-brain platform vision
- Acknowledges the transient substrate as "still structurally AOI-bound and `the-critic`-bound"

This is honest and matches the codebase evidence.

---

### Finding 9: A second-consumer proof is necessary, and the draft handles this correctly — POSITIVE

**Severity**: Positive (answering open question #6)

The draft asks whether a second-consumer proof is strictly necessary. Yes, it is. The reasoning from the first review remains valid:

- The program has been built on concrete proof discipline. An abstract harness would break that discipline at the moment of the central architectural claim.
- aoi-canary makes the proof feasible without large scope.
- A real second consumer exercising real contracts reveals real gaps that an abstract harness might miss.

---

## Open Questions

1. **Should Tranche 1 list its concrete prerequisites?** The draft frames Tier A as cheap, but aoi-canary needs non-trivial infrastructure work (result-backed endpoints, Host Contract v1 layer, discovery, missing renderers). A "known prerequisites" section would help implementors scope the work honestly.

2. **Is the evaluation gate between Tranche 2 and Tranche 3 hard or soft?** Should Tranche 3 be strictly blocked on Tranche 2's evaluation evidence, or can exploratory de-AOI substrate work begin in parallel?

3. **Should canonical Stage 3 be re-assessed as partially advanced in the stage ledger?** The Stage 8/9 host adoption already landed a planner-backed AOI handoff seam with profile law enforcement. The canonical ledger still says "Not started."

---

## Judgment on Proposed Sequence

The six-tranche sequence — Tier A proof → AOI exemplar → de-AOI substrate → Tier B proof + bridge → lifecycle → governance — is **correct, honest, and ready to influence the canonical roadmap**.

The strongest aspects:

- The tiered Stage 13 approach avoids the false choice between "rush a monolithic proof" and "defer the proof again."
- The de-AOI/de-`the-critic` tranche makes the real substrate work visible instead of hiding it behind generic language.
- The evaluation gate inside the AOI exemplar tranche prevents premature generalization.

The only risk is underestimating Tranche 1 scope. The draft should signal that Tier A is real bounded work (2-3 sessions), not a quick checkbox.

---

## Concrete Revisions Recommended Before Canonical Influence

1. **Add a "known prerequisites" list under Tranche 1** with the concrete aoi-canary gaps: result-backed endpoints, Host Contract v1 layer, discovery, missing renderers. This prevents scope surprise.

2. **Add one sentence under Tranche 3** making the evaluation gate from Tranche 2 an explicit precondition.

3. **Update the canonical stage ledger** (in the big roadmap memo) to mark canonical Stage 3 as partially advanced, referencing the Stage 8/9 host adoption completion memo.

These are minor refinements. The draft is ready to be promoted to canonical influence after these edits.

---

## Summary Table

| Tranche | Canonical Map | Verdict | Risk Level |
|---|---|---|---|
| 1: Tier A (aoi-canary result-backed) | Stage 13 | Correct, underestimates scope slightly | Low |
| 2: AOI exemplar loop | Stages 3+4+5 | Correct placement and breakdown | Low |
| 3: De-AOI/de-the-critic substrate | Stage 7 + Stage 13 | Correct, specific enough | Low |
| 4: Tier B + broader bridge | Stage 13 + Stage 7 | Correct, depends on Tranche 3 | Medium (hardest tranche) |
| 5: Lifecycle | Stage 14 | Correctly deferred | Low |
| 6: Governance | Stage 15 | Correctly placed last | Low |

---

*End of second-pass review.*
