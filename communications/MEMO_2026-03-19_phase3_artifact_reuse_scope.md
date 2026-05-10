# Memo: Phase 3 Scope - First Artifact Reuse Proof

## Purpose

Define the scope for **Phase 3 / Deliverable C** in the Thin Consumer Platformization program.

This memo should make the next tranche reviewable before it becomes an implementation plan.

It should answer:

1. why Deliverable C is the next step now
2. what exactly the first artifact proof should cover
3. what must remain out of scope
4. what evidence is required for the tranche to count as a real proof

This memo sits beneath:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_roadmap_after_phase2.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/PLAN_2026-03-18_thin_consumer_platformization_implementation.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md`

## Why This Is The Right Next Tranche

Phase 2 proved the host-side contract.
It did **not** prove reusable upstream products.

The current analyzer-v2 substrate already has meaningful artifact machinery:

- a named artifact family for genealogy relationship classification in `src/analysis_products/store.py`
- job-to-corpus registration
- deterministic `corpus_ref` identity
- `(corpus_ref, artifact_family, artifact_slot)` storage identity
- `producer_fingerprint` freshness signaling
- artifact-family summaries in result manifests
- artifact freshness/state aggregation

But the current state is still weaker than the intended platform claim.

What exists now is mostly:

- **job-scoped artifact materialization**

What is still missing is:

- **cross-job reusable artifact resolution**

That is why Deliverable C is next.
Without it, the program remains a thin-host proof over ephemeral job outputs rather than a reusable analysis-product substrate.

## Current Code Reality

The current codebase already tells us where the proof seam lives.

### What already exists

- `src/analysis_products/store.py`
  - defines `GENEALOGY_RELATIONSHIP_ARTIFACT_FAMILY = "genealogy.relationship_classification"`
  - already computes deterministic `corpus_ref` for the bounded analytical situation
  - already keys artifact storage by `corpus_ref + artifact_family + artifact_slot`
  - persists genealogy relationship artifacts via `store_relationship_classification_artifact(...)`
  - already records `producer_fingerprint`
  - exposes corpus lookup and artifact-family summaries
- `src/analysis_products/schemas.py`
  - exposes `AnalysisResultManifest`
  - exposes `ArtifactFamilySummary` and `ArtifactSlotSummary`
- `src/analysis_products/result_contract.py`
  - includes artifact-family summaries in the result manifest
- `src/presenter/presentation_api.py`
  - already knows the genealogy relationship engine and stores relationship artifacts during presentation-side flows

### What does not exist yet

- no consumer-visible reuse contract built on the existing `corpus_ref` seam
- no reuse lookup contract that resolves Job 2 from prior eligible artifacts
- no cross-job lookup helper exposed as a first-class path; the lookup path is new code, not an existing extraction
- no manifest-level reuse observable such as:
  - `reuse_state`
  - `reused_from_job_id`
- no explicit contract-level decision about the current presenter-derived materialization timing
- no bounded two-job proof that reuse actually happened

This is the gap Deliverable C should close.

### Hidden coupling that must be treated explicitly

The most important implementation reality is this:

- genealogy relationship artifacts are currently materialized during presenter-side flows, not as a proven executor-time reuse path

That means the first proof must make an explicit choice.

The default scope choice for this tranche should be:

- prove reuse of the **stored artifact contract**
- not executor-time skipping of the underlying relationship-generation phase

So Job 2 reuse eligibility should depend on the prior artifact row actually existing and being ready/fresh.
If a small local eager-materialization change is needed to make that deterministic, it can be considered as enabling work.
But the tranche should not widen into a broader executor short-circuit design.

## Scope Decision

## In Scope

The tranche should be tightly bounded to one proof:

- **prove cross-job reuse of the stored `genealogy.relationship_classification` artifact**

That proof must include:

1. one explicit reusable identity for this artifact class
2. one freshness rule that decides whether Job 2 may reuse Job 1
3. one lookup path that resolves reuse candidates
4. one explicit manifest-level reuse signal on Job 2
5. tests that prove both hit and miss behavior

The proof should use:

- exactly **two** jobs
- exactly **one** artifact class
- exactly **one** freshness rule
- exactly **one** lookup path
- exactly **one** genealogy prior-work slot in the proof fixture, so the first reuse observable is unambiguous

## Out Of Scope

To keep the tranche honest, the following are out of scope:

- reuse across multiple artifact classes
- a generalized artifact economy for all workflows
- AOI artifact reuse
- presentation-wide or page-wide artifact reuse
- proving that Job 2 skips the underlying phase-1.5 executor computation path
- consumer-contract changes in `the-critic`
- cross-workflow `AnalysisWorkspacePage` proof work
- dynamic composition
- new host-side UI work except what is strictly needed to observe the existing manifest fields

If the implementation starts expanding into any of those, the tranche is drifting.

## Concrete Deliverable

At the end of this tranche, analyzer-v2 should be able to demonstrate the following:

### Job 1

- computes `genealogy.relationship_classification`
- stores it under the reusable identity already implicit in the current substrate:
  - same `corpus_ref`
  - same `artifact_family`
  - same `artifact_slot`

### Job 2

- requests the same bounded analytical situation
- resolves the prior stored artifact through one lookup path
- reuses it if and only if the one freshness rule says it is valid

### Required observable

Job 2 must expose explicit reuse evidence in the result contract for the genealogy relationship artifact proof fixture.

Because `genealogy.relationship_classification` is a multi-slot artifact family, the first proof should use a
single-slot fixture. The reuse observable must be explicit at least for that reused slot and may also be
rolled up to the family level if the roll-up remains truthful.

The target observable is still:

- `reuse_state = "reused"`
- `reused_from_job_id = "<job-1-id>"`

If final field names differ, the same semantics must hold:

- reuse must be explicit in the manifest
- the source job must be explicit in the manifest
- the observable must not hide partial hit/miss behavior behind an ambiguous family-level summary

Logs and inferred behavior are not sufficient.

## Recommended Shape

The first proof should prefer the narrowest possible architecture.

### Layer 1: Stable identity

Do not invent a second identity system for this proof.

The reusable identity should be the existing analyzer-v2 seam:

- same `corpus_ref`
- same `artifact_family`
- same `artifact_slot`

This is stronger than:

- "artifact for this job"

and narrower than:

- "general artifact identity for the whole platform"

The identity should be sufficient to answer:

- what exact bounded analytical situation does this artifact represent?

### Layer 2: Freshness rule

Define one freshness rule only.

The natural first rule is the existing substrate rule:

- artifact row exists
- `state == "ready"`
- `producer_fingerprint` matches the current genealogy relationship fingerprint

That rule already piggybacks on existing code reality.
It should not expand into a broader freshness framework in this tranche.

But the point of the tranche is not to design the perfect freshness theory.
The point is to define one rule that is coherent and testable.

### Layer 3: Lookup path

Define one lookup path only.

This lookup path is new construction.
It is not an existing public seam being extracted.

The lookup path should be:

- direct
- deterministic
- easy to reason about in tests

It should not require a general search framework for all artifact families.

The expected shape is:

- given Job 2's `corpus_ref`
- resolve the row for `artifact_family + artifact_slot`
- accept it only if the freshness rule passes

Reuse hits should not rewrite the authoritative source row in a way that destroys producer provenance.

### Layer 4: Result-contract exposure

The reuse outcome must surface in the analyzer-v2 result contract.

That likely means touching:

- `src/analysis_products/store.py`
- `src/analysis_products/schemas.py`
- `src/analysis_products/result_contract.py`

`src/analysis_products/run_contract.py` should stay out unless a concrete consumer requirement makes it necessary.
`src/presenter/presentation_api.py` should also stay mostly out, except for any strictly local enabling change
needed to make artifact materialization timing deterministic for the bounded proof.

The key requirement is simple:

- consumer-visible proof must come from the contract, not from internal interpretation

## Primary Code Surfaces To Scrutinize

The most important files for this scope review are:

- `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/run_contract.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/presentation_api.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_run_contract.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_presentation_api.py`

These are the surfaces where the current proof seam is already visible.

## Acceptance Criteria

This tranche should be treated as done only if all of the following are true:

1. `genealogy.relationship_classification` has one explicit reusable identity beyond mere job ownership.
   - for this proof, that means `corpus_ref + artifact_family + artifact_slot`
2. There is one explicit freshness rule for reuse eligibility.
3. Job 2 can resolve Job 1's artifact through one real lookup path.
4. The proof fixture uses exactly one genealogy slot, or otherwise exposes slot-level reuse visibility.
5. Job 2 exposes a visible reuse signal in the result manifest for the reused artifact.
6. Reuse hits do not destroy the source-job provenance of the reused artifact row.
7. Tests cover both:
   - reuse hit
   - reuse miss
8. The tranche does not silently broaden into multi-artifact or multi-workflow reuse infrastructure.

## Verification Expectations

The expected verification for this tranche should be:

- targeted analyzer-v2 unit/integration tests
- one bounded two-job proof fixture or equivalent deterministic test setup
- explicit assertion on the Job 2 manifest reuse signal

The verification target is not:

- “reuse probably happened”

It is:

- “Job 2 contractually says it reused Job 1”

## Failure Modes To Watch For

The main ways this tranche can go wrong are:

- defining an identity that is more abstract than the already-existing `corpus_ref` seam
- widening the lookup path into a general artifact search system
- inventing multiple freshness rules instead of proving one
- recording reuse only in logs or internal traces
- hiding multi-slot ambiguity behind an over-broad family-level reuse claim
- rewriting the shared artifact row on a reuse hit and losing source provenance
- proving a presenter-level optimization rather than a reusable analysis-product contract
- trying to prove executor-time recompute avoidance in the same tranche
- broadening the work to AOI or other artifact families before the first genealogy proof lands

## Review Questions For Fresh Sessions

Before implementation planning, fresh reviewers should stress-test this memo on four questions:

1. Is the proposed artifact seam actually real in the code, or only plausible in theory?
2. What is the narrowest stable identity that could work for this proof?
3. What is the biggest risk that the lookup/freshness design expands into open-ended substrate work?
4. Is the proposed manifest-level reuse observable sufficient and in the right contract surface?

## Resulting Program Order

If this tranche is accepted and executed successfully, the next order should remain:

1. close or waive the small Phase 2 manual-verification tail
2. **Phase 3 / Deliverable C**: first artifact reuse proof in `analyzer-v2`
3. **Phase 4 / Deliverable D**: complete the cross-workflow `AnalysisWorkspacePage` proof in `the-critic`
4. write the round-1 proof record

This means Deliverable C should be treated as:

- the artifact proof
- not the cross-workflow proof
- not a generalized artifact-economy buildout

## Final Scope Sentence

If the team needs one operational sentence for the next step, it should be:

- **Prove that `genealogy.relationship_classification` can be reused across exactly two jobs through one explicit lookup/freshness path, and make that reuse visible in the analyzer-v2 result contract.**
