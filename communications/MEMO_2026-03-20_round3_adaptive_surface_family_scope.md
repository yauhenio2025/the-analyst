# Memo: Next Stage Scope - Round 3 / Adaptive Surface Family Proof

Date: 2026-03-20

## Purpose

Define the next bounded stage after:

- round-1 thin-consumer proof closure
- round-2 bounded dynamic-composition implementation

This memo is the corrected scope document for round-3.

It exists to answer:

1. what the last 96 hours actually established
2. what meaningful platform gap remains
3. what the next proof should be if the goal is still beautiful-by-default thin consumers
4. what the next proof should and should not attempt
5. how to interpret the unexpected adaptive-composition spike that already landed in code

This is still a scope memo, not an execution plan.

## Basis For This Revision

The governing record for this stage is now:

- `communications/MEMO_2026-03-16_aoi_strategic_reassessment_after_parity_work.md`
- `communications/MEMO_2026-03-16_beautiful_by_default_surfaces_platform_gap.md`
- `communications/MEMO_2026-03-18_post_stage9_next_steps.md`
- `communications/MEMO_2026-03-18_thin_consumer_platformization_execution_brief.md`
- `communications/PROOF_2026-03-19_thin_consumer_platformization_round1.md`
- `communications/MEMO_2026-03-19_round2_bounded_dynamic_composition_scope.md`
- `communications/MEMO_2026-03-20_round2_bounded_dynamic_composition_completion.md`
- `communications/REPORT_Claude_Round3_Adaptive_Surface_Family_Scope_Critique_2026-03-20.md`
- `communications/REPORT_Codex_Round3_Adaptive_Surface_Family_Scope_Audit_2026-03-20.md`
- `the-critic/communications/NEXT_SESSION_DYNAMIC_COMPOSITION_AUDIT.md`

Two important facts changed since the first draft of this memo:

1. the round-2 documentary gap has now been closed by:
   - `communications/MEMO_2026-03-20_round2_bounded_dynamic_composition_completion.md`
2. the requested Codex scope audit was not delivered as asked; instead an adaptive implementation spike landed in code

That spike is useful feasibility evidence, but it is not by itself the governing plan.

This revised memo absorbs the useful parts of the critique and the spike so the planning state matches repo reality.

## Current Program Position

As of 2026-03-20:

- round-1 is documented and proved at the thin-host / shared-contract / first-artifact level
- round-2 is implemented, tested, and now documentary-closed enough for the next stage to be scoped cleanly
- the generic host boundary is strong enough that further strategic progress should now come from upstream composition quality rather than more host plumbing

What is still not true:

- two substantively different genealogy jobs still risk receiving structurally similar surfaces unless analyzer-v2 changes the returned contract
- round-2 proved bounded runtime regrouping, but it did not yet prove content-sensitive editorial family selection inside a single authored location

That remaining gap is exactly what the recent audit highlighted:

- distinct jobs can still flow through essentially the same renderer family and section structure

So the next step should not be:

- more AOI plumbing
- more generic-host refactoring
- a generalized app generator
- a return to broad dormant refinement work

It should be:

- one bounded proof that analyzer-v2 can choose a different surface family for the same generic route based on already-available structured signals

## Recommended Label

Use:

- **Thin Consumer Platformization Round 3**

More specifically:

- **Adaptive Surface Family Proof**

Do not call this Stage 10.

## Round-2 Documentary Gate

The first draft said round-3 should not start without one short round-2 completion/proof note.

Owner of that gate:

- the maintainer preparing round-3 execution planning

Status:

- satisfied by `communications/MEMO_2026-03-20_round2_bounded_dynamic_composition_completion.md`

This means documentary cleanup should no longer block round-3 execution planning.

## Core Strategic Judgment

The right next proof is still not another whole-page regrouping pass.

Round-2 already proved:

- bounded runtime hierarchy generation

Round-3 should isolate the next missing variable:

- bounded, content-sensitive surface-family selection

That means the next proof should keep:

- one existing generic route
- one existing workflow
- one bounded analytical surface
- one explicit composition mode
- multiple prevalidated surface-family variants
- one deterministic selector over existing structured signals
- no new workflow-specific host code

This is the smallest next proof that actually advances the beautiful-by-default platform thesis.

## Recommended Proof Target

The first adaptive surface-family proof should target:

- `genealogy_relationship_landscape`

Activation contract:

- `/p/:projectId/analysis/intellectual_genealogy?composition_mode=adaptive_relationship_surface_v1`

This remains the best bounded target because:

1. the authored baseline is visibly static
2. the underlying relationship cards already exist in machine-readable form
3. the adaptive proof can stay local to one surface instead of regenerating the whole page
4. the Critic host can remain unchanged
5. this directly addresses the recent "same structure across unlike jobs" complaint

## Hard Scope Rules

### 1. Round-3 mode is independent from round-2 mode

`adaptive_relationship_surface_v1` is a distinct proof mode.

Hard rule:

- do not stack it with `bounded_dynamic_genealogy_v1`
- do not require the round-2 generated-parent proof to be active at the same time

The round-3 claim is:

- one authored-location surface can become content-sensitive under explicit runtime contracts

not:

- multiple proof modes can be layered at once

### 2. The selector reads transformed structured cards, not raw prose

The selector must aggregate across the collection of already-transformed relationship cards exposed on:

- `genealogy_relationship_landscape.items[*].structured_data`

It must not:

- add a new LLM scoring pass
- parse raw prose directly
- push selection logic into the host

This keeps the proof inside the presentation layer and makes the result inspectable.

### 3. The generic host stays unchanged

Round-3 succeeds only if the adaptive result appears because analyzer-v2 changed the returned surface contract.

It does not count as success if The Critic learns genealogy-specific adaptive behavior.

## In Scope

Round 3 should prove one bounded thing:

- analyzer-v2 can choose among a small set of prevalidated surface families for `genealogy_relationship_landscape`, based on deterministic signals derived from the transformed relationship-card collection, and the existing generic host can consume the result unchanged

That includes:

1. one new proof-mode activation:
   - `composition_mode=adaptive_relationship_surface_v1`
2. one workflow only:
   - `intellectual_genealogy`
3. one adaptive target surface only:
   - `genealogy_relationship_landscape`
4. exactly three allowed runtime surface families
5. one deterministic selector using existing structured signals
6. one inspectable trace stage showing:
   - target surface
   - signal summary
   - selected family
   - rejected families
   - rationale
7. explicit renderer/data validation for the selected runtime family

## Out Of Scope

To keep this proof honest, the following remain out of scope:

- AOI adaptive composition
- multi-surface adaptive composition in the same tranche
- whole-page topology regeneration
- a generalized composition framework for all workflows
- reactivating broad LLM refinement as the default path
- host-side workflow-specific composition logic
- new standalone app shells
- replacing the authored catalog
- broad renderer-library expansion

If the work starts turning into adaptive everything, the scope has drifted.

## Concrete Surface-Family Contracts

The original memo draft was too vague here.

The proof must now be judged against concrete renderer-level family contracts.

At least one family must use a different top-level renderer type from the others. The current recommended baseline is:

### Family A: `relationship_profile_dossier`

Use when:

- one relationship clearly dominates the field

Minimum contract:

- top-level renderer: `accordion`
- required sections:
  - `focus_summary` via `prose_block`
  - `dominant_relationship` via `mini_card_list`
  - `supporting_relationships` via `mini_card_list`
  - `field_snapshot` via `key_value_table`
  - `dominant_evidence` via `evidence_trail`
  - `counterfactual_focus` via `prose_block`

Intended reading shape:

- one dominant precursor
- supporting context
- field summary
- evidence and counterfactual implication

### Family B: `relationship_comparison_review`

Use when:

- several relationships remain materially comparable

Minimum contract:

- top-level renderer: `table`
- required columns:
  - `work_title`
  - `relationship_type`
  - `strength`
  - `channels`
  - `why_it_matters`

Intended reading shape:

- side-by-side comparison
- sortable review of several comparable predecessors

### Family C: `relationship_field_map`

Use when:

- the predecessor field is more distributed or heterogeneous

Minimum contract:

- top-level renderer: `accordion`
- required sections:
  - `field_summary` via `prose_block`
  - `field_snapshot` via `key_value_table`
  - one or more relationship-type band sections via `mini_card_list`

Intended reading shape:

- field-level summary
- grouped relationship bands
- distributed map rather than single dominant lineage

These contracts are concrete enough that a reviewer can tell whether the family genuinely changed.

## Selector Design

The selector must be deterministic and must operate on the aggregated transformed relationship-card collection.

Allowed signal classes:

- relationship count
- distinct relationship-type count
- strength concentration / top-share shape
- dominance gap between top and next relationship
- relationship-type distribution
- simple derived labels such as dominant work title and dominant relationship type

Not allowed:

- new LLM scoring pass
- raw-prose heuristics
- hidden refinement logic that is not surfaced in trace

The practical review question should be:

- "why did this job get `relationship_profile_dossier` rather than `relationship_field_map`?"

and the system should be able to answer it deterministically.

## Inspectability And Trace

Round-3 should add one bounded diagnostic stage:

- `adaptive_surface_selection`

That stage should expose:

1. target surface
2. signal summary
3. selected family
4. rejected families
5. rationale

If adaptive validation fails:

- the trace must stay visible
- the invalid path must remain inspectable
- authored pre-composition state should remain explicit

## Relationship To The Existing Adaptive Spike

A feasibility spike already exists in code and tests, primarily in:

- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`
- `tests/test_presentation_api.py`
- `tests/test_manifest_trace.py`

That spike is useful because it already demonstrates:

- a distinct `composition_mode=adaptive_relationship_surface_v1`
- selection over transformed relationship-card collections
- three concrete family contracts
- trace-level inspectability

But it should not be treated as scope authority by itself.

The next step is to evaluate that spike against this memo's bounded claim and either:

- ratify it as-is, or
- trim/adjust it in the execution plan

## Acceptance Criteria

Round 3 should be treated as successful only if all of the following are true:

1. analyzer-v2 supports `composition_mode=adaptive_relationship_surface_v1` only for `intellectual_genealogy`
2. the default authored route remains unchanged when the mode is absent
3. exactly one target surface is adaptive:
   - `genealogy_relationship_landscape`
4. the selector chooses among exactly three explicitly allowed families
5. the selector is deterministic and uses no new LLM pass
6. the selector reads the aggregated transformed relationship-card collection, not raw prose
7. at least one family uses a different top-level renderer type from the others
8. the selected family is validated by explicit renderer/data contracts
9. invalid adaptive payloads fail closed with an inspectable error path
10. the presentation trace shows the adaptive-family selection stage and selected family
11. `AnalysisWorkspacePage` consumes the resulting presentation with no new workflow-specific code
12. at least two contrast jobs can be shown to select different surface families on the same generic route
13. one short proof/closure memo records:
    - the exact route used
    - the contrast jobs used
    - the selected family for each job
    - the final bounded claim being made

## Verification Expectations

### Automated

- analyzer-v2 tests for adaptive-family selection logic
- analyzer-v2 tests for family contract validation
- analyzer-v2 tests for trace diagnostics
- focused Critic tests proving generic host consumption remains unchanged

### Manual

- one authored genealogy restore without proof mode
- two proof-mode genealogy restores on contrasting jobs using:
  - `/p/:projectId/analysis/intellectual_genealogy?composition_mode=adaptive_relationship_surface_v1`
- one trace inspection for each proof-mode job

### Documentary

- one short proof or completion memo naming:
  - the route
  - the target surface
  - the chosen family for each contrast job
  - the final bounded claim

## Failure Modes To Watch For

The main ways this stage can still go wrong are:

1. making the host smarter instead of changing the returned surface contract
2. reopening AOI or multi-surface adaptation immediately
3. changing only descriptive text while the actual surface contract stays effectively the same
4. quietly reintroducing hidden inference or refinement logic
5. claiming the spike proves more than it actually does
6. letting documentary cleanup lag behind implementation again

## Final Recommendation

The next meaningful move is now clear:

- use this revised memo as the operative round-3 scope document
- treat the existing adaptive spike as feasibility evidence, not as self-ratifying scope
- write the execution plan as an audit of that spike against this bounded claim rather than starting from a blank slate

One operational sentence:

- **Prove one bounded adaptive surface family by making analyzer-v2 choose a different `genealogy_relationship_landscape` family for contrasting genealogy jobs on the same generic route, using deterministic signals from transformed relationship cards and concrete renderer contracts while keeping the host unchanged.**
