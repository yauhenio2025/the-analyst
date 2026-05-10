# Memo: Phase E Genealogy V2 Idea Evolution First-Hop Affordance Eligibility V1 Completion

Subtitle: One bounded analyzer-side view+engine+leaf rule now makes `genealogy_idea_evolution` honestly eligible for generic first-hop affordance without globally blessing `concept_synthesis` or touching the host

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
Most Recent Prior Code Completion:
- `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`
Completed Scope:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_scope.md`
Scope Review Context:
- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Affordance_Eligibility_V1_Scope_Audit_2026-04-03.md`
- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Idea_Evolution_First_Hop_Affordance_Eligibility_V1_Scope_Critique_2026-04-03.md`
Analyzer Codebase:
- `/home/evgeny/projects/analyzer-v2`

## Purpose

Record what actually landed after the `IdeaEvolutionRenderer` follow-on was blocked honestly in review.

The blocker was real:

- `currentRendererCapture.ts` fails closed unless `_firstHopAffordance?.capturable === true`
- `genealogy_idea_evolution` did not receive `first_hop_affordance`
- a host-only helper adoption would therefore have hidden the existing idea-card capture controls rather than aligned them truthfully

So this slice was the bounded prerequisite:

- make `genealogy_idea_evolution` affordance-eligible upstream first

## What Landed

One bounded analyzer-side eligibility broadening is now complete in [first_hop_affordance.py](/home/evgeny/projects/analyzer-v2/src/presenter/first_hop_affordance.py#L17).

The landed shape is:

1. the migrated-family predicate stayed unchanged:
   - `is_migrated_analytical_leaf_payload(...)` still means only migrated engine-family leaves
2. one new bounded helper now exists:
   - `is_genealogy_idea_evolution_first_hop_eligible_leaf(...)`
3. that helper is deliberately narrow:
   - `view_key == "genealogy_idea_evolution"`
   - `engine_key == "concept_synthesis"`
   - `children == []`
4. `derive_first_hop_affordance(...)` now has a second eligibility branch:
   - migrated-family analytical leaf
   - or this new genealogy view+engine+leaf case
5. workflow gating still stays upstream through the existing `enabled` flag
6. the emitted affordance remains generic-only:
   - `capturable = true`
   - `allowed_destinations = ["arsenal", "research_todo"]`
7. no `specialized_family` was added on this surface
8. no host code changed

## Final Boundary

The honest completed claim is:

- analyzer-v2 now treats `genealogy_idea_evolution` as one bounded generic first-hop-affordance-eligible leaf through a view+engine+leaf-specific rule in the shared derivation seam

What this does mean:

- the blocker for truthful host helper adoption on `IdeaEvolutionRenderer` is now removed
- job-backed presentation can now emit generic first-hop affordance on that view
- transient compose inheritance can now emit the same generic affordance on that exact payload shape

What this does not mean:

- all `concept_synthesis` leaves are now eligible
- the migrated-family allowlist changed
- specialization semantics changed
- item handles or `entity_id` semantics changed
- host-side capture alignment is already done
- generic renderer-law or destination-policy depth is now proven

## Implementation Shape

The key implementation decision was where **not** to put the rule.

The new behavior did **not** go into:

- `is_migrated_analytical_leaf_payload()`

That was important because this slice is not an engine-family promotion.
It is a bounded exception in the shared derivation seam.

So the landed code keeps two distinct ideas separate:

1. migrated engine-family leaf eligibility
2. one bounded genealogy view+engine+leaf eligibility precedent

That keeps the result fail-closed and reviewable.

## Verification

Direct policy-seam verification passed:

- `PYTHONPATH=. pytest -q tests/test_first_hop_affordance.py`
  - `2 passed`

Focused presenter-path verification passed:

- `PYTHONPATH=. pytest -q tests/test_presentation_api.py -k 'first_hop_affordance'`
  - `9 passed`

That focused presenter coverage now explicitly proves:

- positive job-backed emission on `genealogy_idea_evolution`
- `specialized_family is None` on that bounded genealogy case
- fail-closed presenter-path negatives for:
  - wrong `view_key`
  - wrong `engine_key`
  - parent payload with children

Focused transient/shared-derivation verification also passed:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py -k 'first_hop_affordance'`
  - `17 passed`

Environment honesty note:

- the focused pytest runs still emit the existing Pydantic deprecation warnings; this slice did not change that repo-wide noise

## Calibrated Claim

Before this slice:

- `genealogy_idea_evolution` was still outside analyzer-owned generic first-hop affordance truth
- the intended host follow-on on `IdeaEvolutionRenderer` would have failed closed for the wrong reason

After this slice:

- the host-side follow-on can now be scoped honestly as a host-only alignment question again

That is a meaningful Phase E move because it broadens the proof matrix on the analyzer-owned contract line without broadening policy dishonestly.

But it is still narrow.

The right framing is:

- one bounded view+engine+leaf-specific eligibility precedent is now proven

not:

- generic `concept_synthesis` eligibility is solved

## Why This Matters

This slice matters because it removes a real upstream blocker rather than compensating for it downstream.

It improves the analyzer-v2-as-brain posture in the right direction:

- the host no longer needs to preserve a local bypass on this surface just because analyzer-v2 omitted the field
- the current-renderer helper seam can stay fail-closed without becoming dishonest

That is the correct trade:

- one tiny analyzer-side rule
- instead of one more host-side exception

## Next Honest Step

The next honest question is now back on the host side:

- can `IdeaEvolutionRenderer` consume the already-landed `currentRendererCapture.ts` seam plus the now-truthful generic first-hop affordance on `genealogy_idea_evolution`, while staying narrow about coverage, identity, and browser-proof claims?

That next slice should stay bounded:

- host-only in Critic
- idea-card buttons only
- no analyzer changes
- no backend or persistence changes
- no generic renderer-package law
- no genealogy read-side truth surfacing

The key question is no longer upstream eligibility.
That is now answered.

The next question is whether the last materially broader current non-AOI renderer can consume the already-landed seam honestly without forcing helper exceptions or overclaiming generic law.
