# Memo: Next Stage Scope - Round 2 / Bounded Dynamic Composition Entry

## Purpose

Define the **next stage after round-1 proof-record closure** in the Thin Consumer Platformization program.

This memo is meant to answer:

1. where the program actually stands right now
2. what the next stage should be after round-1 is formally closed
3. what that next stage should and should not attempt
4. what proof would be required before broader “apps on the fly” claims become credible

This memo does **not** treat round-1 as already documentary-closed.
It defines the next stage **after** that closure step is completed.

This memo sits beneath:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase0_phase1a_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase2_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase4_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_round1_proof_record_scope.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_round1_proof_record_evidence_readiness.md`

## Current Program Position

As of 2026-03-20, the program stands here:

- Deliverable A: completed in substance
- Deliverable B: completed in substance; the small manual tail has already been waived in the round-1 proof record
- Deliverable C: completed in substance, with deterministic documentary evidence now available
- Deliverable D: completed in substance, with a manual-tail decision still required
- Round-1 proof record: written
- Round-1 closure: still not complete because the Phase 4 manual disposition remains pending

Put differently:

- the thin-host boundary is real enough
- the shared consumer contract is real enough
- the first reusable artifact proof is real enough
- the cross-workflow generic workspace proof is real enough
- the proof record already exists
- what remains for round-1 is final manual-disposition closure, not another product tranche

That means the program is **not** yet ready to begin the next stage as active implementation work.
It is ready to define it.

## Why This Is The Right Next Stage

The 2026-03-18 strategy memo was explicit about the order:

1. thin the host boundary
2. make the consumer contract real
3. prove one reusable artifact seam
4. only then reopen dynamic composition beyond the fixed page/view catalog

The 2026-03-19 memo trail shows that steps 1 through 3 and the proving-vehicle step are now complete in substance.

So the next stage after round-1 proof closure should **not** be:

- more host thinning
- more consumer-contract extraction
- another first-artifact proof
- broad AOI enrichment
- a full bespoke-app generator

The next stage should be:

- **one bounded reopening of dynamic composition**

That is the real deferred layer from the Stage 9 strategy trail.

## Recommended Label

Use:

- **Thin Consumer Platformization Round 2**

More specifically:

- **Bounded Dynamic Composition Entry**

Do **not** call this Stage 10 yet.

Reason:

- the local memo trail still defines the work best in program terms, not stage terms
- the next proof should stay narrow enough that a premature stage label would encourage overclaiming

## Gate Before This Stage May Start

This next stage should not begin until the following are closed in writing:

1. the round-1 proof record exists at:
   - `/home/evgeny/projects/analyzer-v2/communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
2. the Phase 2 manual tail is recorded as waived in the round-1 proof record
3. the Phase 4 manual tail is recorded as:
   - performed, or
   - waived
4. the proof record's gate/disposition language is updated to reflect the final manual decisions
5. the round-1 exit criteria have explicit final disposition

If those are not done, the team should finish round-1 closure before opening round-2 implementation.

## Scope Decision

## In Scope

Round 2 should be constrained to **one bounded proof**:

- prove that analyzer-v2 can compose **one temporary page/view hierarchy** for **one bounded analytical situation**
- and that the existing thin host can render it without new workflow-specific Critic code

The intended proof shape is:

1. one generic host path:
   - `/p/:projectId/analysis/:workflowKey`
2. one proving vehicle:
   - `AnalysisWorkspacePage`
3. one workflow family only for the first proof:
   - `intellectual_genealogy`
4. one dynamic composition path in analyzer-v2 that can assemble a bounded page hierarchy when the fixed catalog is deliberately bypassed or insufficient for the proof
5. one explicit renderer-contract layer for only the renderers used by that proof

This stage should prove:

- dynamic composition of page structure
- renderer selection under explicit input contracts
- continued thin-host consumption of the resulting presentation

It should **not** try to prove all possible dynamic app generation at once.

## Why Genealogy Should Be First

The first round-2 proof should use `intellectual_genealogy`, not AOI.

Why:

1. Round-1 already proved cross-workflow host genericity. Round-2 should isolate the **composition** variable, not add a second proof variable.
2. Genealogy already has the most concrete reusable-artifact seam from round-1.
3. AOI adds thinker-context and bespoke-surface complexity that is strategically lower-value for the first composition proof.
4. If dynamic composition cannot be made credible on the simpler genealogy proving surface, it is too early to widen to AOI.

AOI can remain a later expansion or regression canary.

## Concrete Deliverable

At the end of this stage, the platform should be able to demonstrate:

### 1. Analyzer-v2 can build one bounded generated page hierarchy

For one genealogy analytical situation, analyzer-v2 should be able to:

- decide on a page structure
- choose from an explicitly allowed renderer set
- emit a presentation/page hierarchy that was not simply copied from the fixed authored catalog

### 2. Generated views are contract-checked

Each renderer used in the proof should have a real, enforceable input contract.

For this first proof, the contract requirement should remain narrow:

- validate only the renderers actually used by the generated page
- fail closed if the generated payload does not satisfy the renderer contract

### 3. The existing thin host can consume the generated page

`AnalysisWorkspacePage` should render the generated presentation without:

- workflow-specific new Critic route logic
- bespoke genealogy-only host code
- a second consumer contract

### 4. The fixed catalog remains intact

This stage should not require deleting or replacing the authored view/page catalog.

The bounded proof is:

- generated composition can work

not:

- authored views must disappear

## Recommended Shape

### Layer 1: Dynamic page assembly in analyzer-v2

Keep the first generated composition proof narrow.

Prefer:

- one bounded planner/presenter entry path
- one generated page hierarchy
- one known renderer allowlist

Do not begin with:

- a general arbitrary-app generator
- unconstrained LLM-driven renderer selection
- multiple page families at once

### Layer 2: Renderer contracts

The strategy memo correctly identified renderer contracts as the missing guardrail.

For this stage:

- add explicit contracts for only the renderers in the proof slice
- validate generated payloads against those contracts
- surface invalid composition as an inspectable failure, not silent degradation

### Layer 3: Host neutrality

Do not let the proof “succeed” by sneaking new workflow-specific logic into The Critic.

The proof should stand only if:

- analyzer-v2 emits the generated presentation
- the existing generic host consumes it

## Out Of Scope

To keep round-2 honest, the following are out of scope:

- reopening Deliverables A through D
- any new artifact-economy expansion beyond the round-1 proof
- multi-workflow dynamic composition
- AOI-first dynamic composition
- generalized “app generator” claims
- new standalone app shells
- broad route generation
- broad form/schema-driven workflow input generation
- replacing the fixed authored catalog entirely
- large renderer-library expansion
- style-system or visual-polish work as the main line
- calling the stage complete because one internal demo worked once

If the work starts turning into “generate any app from anything,” the scope has drifted.

## Acceptance Criteria

Round 2 should be treated as done only if all of the following are true:

1. round-1 proof closure was completed first
2. analyzer-v2 can emit one bounded generated page/view hierarchy for genealogy
3. the generated hierarchy uses only an explicitly allowed renderer set
4. renderer payloads are validated by explicit contracts
5. invalid generated payloads fail closed with an inspectable error path
6. `AnalysisWorkspacePage` renders the generated presentation without new workflow-specific Critic code
7. the existing authored catalog path still works and is not broken by the proof
8. automated verification exists for:
   - generated page assembly
   - renderer contract validation
   - generic host consumption
9. one short proof record or completion memo captures:
   - the exact route used
   - the exact generated page proof
   - the exact renderer contracts exercised
   - the final bounded claim being made

## Verification Expectations

The expected verification for this stage should be:

### Automated

- analyzer-v2 tests for generated page/view assembly
- analyzer-v2 tests for renderer input-contract validation
- focused `the-critic` tests proving the generic workspace consumes the generated presentation with no workflow-specific host additions

### Manual

- one manual run or restore through `AnalysisWorkspacePage` using the generated genealogy page proof

### Documentary

- one short proof memo naming:
  - the generated route
  - the generated page proof target
  - the renderer set used
  - the pass/fail disposition of the bounded claim

## Failure Modes To Watch For

The main ways this stage can go wrong are:

1. opening round-2 before the round-1 proof record is actually closed
2. proving only that a hand-authored page still works, which would not test dynamic composition at all
3. adding workflow-specific Critic glue and then calling the result “generic”
4. letting generated renderer payloads bypass validation
5. widening immediately to AOI or multiple workflows before one genealogy proof is stable
6. conflating bounded generated-page proof with broad “apps on the fly” success

## Final Recommendation

If the team needs one operational sentence for the next stage, it should be:

- **After round-1 is formally closed, reopen exactly one narrow dynamic-composition proof: make analyzer-v2 generate one bounded genealogy page hierarchy under explicit renderer contracts, and prove the existing generic workspace can consume it without new host-specific glue.**
