# Memo: Phase E Genealogy V2 Idea Evolution First-Hop Affordance Eligibility V1 Scope

Subtitle: One bounded analyzer-side prerequisite should make `genealogy_idea_evolution` honestly eligible for generic first-hop affordance before the host tries to align its capture path to the landed current-renderer helper seam

Date: 2026-04-03
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Code Completion:
- `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
Superseded Prior Next-Step Scope:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_scope.md`
Blocking Review Context:
- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`

## Purpose

Define the actual next bounded step after the shared current-renderer helper landed.

The rejected host-only `IdeaEvolutionRenderer` scope surfaced one real blocker:

- the host helper correctly requires `_firstHopAffordance?.capturable === true`
- `V2TabContent` only threads what analyzer-v2 emitted
- analyzer-v2 does **not** currently emit `first_hop_affordance` for `genealogy_idea_evolution`

So the next honest step is not host alignment first.
It is one small analyzer-side eligibility slice first.

## Why This Is The Right Next Step

The broader strategic direction did not change:

- `genealogy_idea_evolution` is still the last materially broader current non-AOI renderer outside the landed helper seam

What changed is sequencing.

The code-backed blocker is:

- `currentRendererCapture.ts` fails closed unless `capturable === true`
- `genealogy_idea_evolution` is backed by:
  - `workflow_key = "intellectual_genealogy"`
  - `engine_key = "concept_synthesis"`
- `first_hop_affordance.py` only auto-emits generic first-hop affordance for:
  - approved workflows
  - migrated analytical leaf payloads
- `concept_synthesis` is not in the current migrated family allowlist

That means a host-only helper adoption on this surface would currently remove the existing capture buttons rather than align them honestly.

So the smallest honest next move is:

- make `genealogy_idea_evolution` analyzer-affordance-eligible first

Then the already-scoped host helper adoption can follow honestly.

## Current Boundary

The in-scope view is:

- `view_key = "genealogy_idea_evolution"`
- `workflow_key = "intellectual_genealogy"`
- `engine_key = "concept_synthesis"`

This slice is analyzer-side only.
It is about eligibility to receive the existing generic first-hop affordance object:

- `capturable = true`
- `allowed_destinations = ["arsenal", "research_todo"]`

It is not about:

- host capture UI changes
- `entity_id`
- `source_workflow_key`
- item-level identity
- `specialized_family`

## Proposed Implementation

### 1. Add one bounded eligibility branch in `derive_first_hop_affordance(...)`

Introduce one small explicit eligibility rule for the `genealogy_idea_evolution` leaf, but put it in the shared derivation seam itself:

- `derive_first_hop_affordance(...)`

Do **not** hide this inside:

- `is_migrated_analytical_leaf_payload()`

That existing predicate should stay what it is:

- migrated engine-family leaf detection

This new rule is a separate kind of thing:

- one bounded view-specific eligibility branch

At the implementation site, the effective allow condition should require:

- `payload.view_key == "genealogy_idea_evolution"`
- `payload.engine_key == "concept_synthesis"`
- `payload.children == []`

The workflow gate is already handled upstream by the existing `enabled` flag.
So although the policy is still:

- approved workflow
- this specific view
- this specific engine
- leaf only

the new derivation branch itself should only need the payload-side three-part check above.

This should broaden first-hop eligibility for this one bounded analytical leaf only.

### 2. Do not broaden `concept_synthesis` globally

Do **not** solve this by simply adding `concept_synthesis` to the migrated-family engine allowlist.

That would be a stronger and less honest claim because:

- the current evidence is about one specific live view
- there is no proof yet that every future `concept_synthesis` leaf should be capturable

So this slice should stay view-specific or view+engine specific, not engine-family generic.

### 3. Keep affordance semantics generic-only

If `genealogy_idea_evolution` becomes eligible, it should receive only the existing generic affordance:

- `capturable = true`
- `allowed_destinations = ["arsenal", "research_todo"]`

Do not add:

- `specialized_family`
- item handles
- destination-specific policy

### 4. Let both shared presenter paths inherit the same rule

Because `derive_first_hop_affordance(...)` is shared, this eligibility should apply consistently wherever that view is emitted:

- transient compose path
- job-backed presentation path
- single-view assembly path

But the proof bar is asymmetric and should be named honestly:

- the job-backed line needs mandatory end-to-end proof in this slice because `genealogy_idea_evolution` is definitely live there today
- the transient line should inherit the same rule through the shared derivation seam, but does **not** need a new end-to-end browser proof here
- transient coverage should be contract/unit-level unless a real transient emitter for this exact view is already easy to exercise

The point is contract honesty, not host specificity.

### 5. Leave the host untouched in this slice

Do not change:

- `IdeaEvolutionRenderer`
- `currentRendererCapture.ts`
- `V2TabContent`
- `CaptureContext`

The host follow-on should happen only after analyzer-v2 can honestly provide the affordance field on this view.

## Contract Notes

- This is an additive contract broadening on one bounded genealogy view.
- It changes manifest / presentation contract truth for that view.
- It does **not** change user-visible content payload truth.
- It should therefore behave like the earlier generic first-hop propagation line:
  - contract hash / manifest truth changes
  - content hash does not become a content-diff claim merely because the affordance object now appears

## Test Plan

### Analyzer unit / presenter tests

Add focused tests in analyzer-v2 that prove:

1. `derive_first_hop_affordance(...)` / attached presenter payloads now emit generic first-hop affordance for:
   - `workflow_key = "intellectual_genealogy"`
   - `view_key = "genealogy_idea_evolution"`
   - `engine_key = "concept_synthesis"`
   - leaf payload
2. the same payload still emits no affordance when:
   - workflow is not approved
   - the payload has children
   - the view key differs
   - the engine key differs
3. `genealogy_portrait` and the existing migrated genealogy leaves remain unchanged
4. no `specialized_family` is added on this surface

### Presenter path coverage

Add or extend tests so the new eligibility is proven on:

- `_prepare_page_payloads(...)`
- `assemble_single_view(...)`

Because the derivation rule stays shared, add one transient compose contract/unit-level proof too.

That transient proof should be modest:

- prove the shared derivation seam now allows this exact payload shape when the upstream transient handoff gate is already satisfied

It does **not** need a fresh end-to-end browser/network transient proof in this slice.

### Contract-honesty coverage

Reuse or extend existing first-hop affordance manifest/hash tests only as needed to prove:

- the field is present on this view
- contract truth is visible
- no new specialization semantics are implied

## What This Slice Is Not

This is not:

- the host-side `IdeaEvolutionRenderer` alignment
- generic `concept_synthesis` blessing
- generic renderer-package law
- `entity_id` modeling
- genealogy read-side truth surfacing
- backend or persistence work

It is one small analyzer-side precondition slice so the later host adoption can stay honest.

## Assumptions And Defaults

- `genealogy_idea_evolution` is the only current view-definition user of `engine_key = "concept_synthesis"`.
- The analyzer-v2-as-brain direction is better served by one tiny analyzer-side eligibility rule than by growing helper exceptions or preserving host-local bypasses.
- If review shows `genealogy_idea_evolution` should **not** become affordance-eligible upstream, then the follow-on host idea-evolution alignment should be deferred rather than forced.
- This is a deliberate new dimension in first-hop eligibility:
  - view-key-aware allowance
  - not just engine-family allowance
- That is acceptable here because the evidence base is view-specific, not engine-family wide.
- If a second `concept_synthesis` view later proves the same eligibility honestly, the expected next cleanup is consolidation:
  - promote from view-specific rule to engine-family rule
  - remove the one-off branch rather than accumulating per-view exceptions

## Decision Rule

If the only way to land this slice is to broaden first-hop affordance to all `concept_synthesis` leaves without a stronger evidence base, stop and recalibrate.

The intended result is:

- one bounded view-specific eligibility broadening

not:

- a hidden engine-family policy expansion.
