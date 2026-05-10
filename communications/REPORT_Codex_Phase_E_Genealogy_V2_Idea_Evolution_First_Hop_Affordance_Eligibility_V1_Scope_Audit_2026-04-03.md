# Report: Phase E Genealogy V2 Idea Evolution First-Hop Affordance Eligibility V1 Scope Audit

Date: 2026-04-03

## Verdict

`approve with corrections`

The memo is directionally right.

Its central blocker diagnosis is correct:

- `genealogy_idea_evolution` is not first-hop-affordance-eligible today
- the host helper now fails closed on `_firstHopAffordance?.capturable === true`
- a host-only follow-on would therefore be dishonest until analyzer-v2 broadens eligibility upstream

But two calibrations are needed:

1. the proposed rule should not force unnecessary `workflow_key` threading through `derive_first_hop_affordance(...)` if the same outcome can be achieved by a payload predicate plus the existing `enabled` gate
2. the shared derivation should stay common across transient and job-backed presenter paths, but only the job-backed line currently has a concrete `genealogy_idea_evolution` surface that must be proven end to end

## The Memo's Strongest Code-Backed Points

### 1. The blocker diagnosis is correct

The analyzer does not currently emit generic first-hop affordance for this view.

- `derive_first_hop_affordance(...)` only returns an affordance when `enabled` is true and `is_migrated_analytical_leaf_payload(payload)` is true (`src/presenter/first_hop_affordance.py:43-60`)
- `is_migrated_analytical_leaf_payload(...)` is keyed to `MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS` plus leaf-ness (`src/presenter/first_hop_affordance.py:43-47`)
- `concept_synthesis` is not in that family allowlist (`src/presenter/first_hop_affordance.py:20-35`)
- `genealogy_idea_evolution` is currently defined on `engine_key = "concept_synthesis"` (`src/views/definitions/genealogy_idea_evolution.json:15-20`)

I also verified this directly with a local one-off check: constructing a `ViewPayload` for `genealogy_idea_evolution` with `engine_key="concept_synthesis"` and calling `derive_first_hop_affordance(..., enabled=True)` returns `None`.

### 2. The memo is right that the host should not go first

The landed host helper now hard-requires analyzer-owned capturability truth.

- `resolveCurrentRendererCaptureRuntime(...)` returns `null` unless `_firstHopAffordance?.capturable === true` (`/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:26-63`)
- `V2TabContent` only threads whatever `payload.first_hop_affordance` analyzer-v2 emitted (`/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:588-597`)
- `IdeaEvolutionRenderer` still uses local `captureMode && onCapture` gating and local provenance literals today (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:380-386`, `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:555-570`)

So the host-side helper adoption is still blocked upstream.

### 3. Rejecting a global `concept_synthesis` allowlist broadening is the right call

This is the most important scoping choice in the memo.

Today, the only current view definition using `engine_key = "concept_synthesis"` is `genealogy_idea_evolution`.
But the affordance law is not consumed only by view definitions.
`compose_from_intent.py` also calls the same derivation logic for transient views (`src/presenter/compose_from_intent.py:1375-1419`).

So adding `concept_synthesis` to `MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS` would be a broader semantic claim than "make this one current genealogy view eligible":

- it would broaden generic affordance eligibility for any transient or future leaf payload carrying `engine_key="concept_synthesis"`
- existing transient first-hop tests prove that listed engine families are treated generically at the derivation layer (`tests/test_compose_from_intent.py:753-832`)

That is a stronger policy than the current evidence supports.

### 4. The analyzer-side-only boundary is mostly honest

The memo is right to keep this slice out of:

- host renderer changes
- backend or persistence work
- `entity_id`
- `specialized_family`

The current first-hop contract already supports generic affordance without specialization (`src/presenter/first_hop_affordance.py:50-60`), and the only specialization today is the AOI findings-bank path (`src/presenter/first_hop_affordance.py:87-96`).

## The Memo's Weakest Or Overstated Assumptions

### 1. The proposed explicit `workflow_key` condition is over-specified

The memo says the intended allow condition should require:

- `workflow_key == "intellectual_genealogy"`
- `payload.view_key == "genealogy_idea_evolution"`
- `payload.engine_key == "concept_synthesis"`
- `payload.children == []`

That is directionally fine as policy, but not the smallest code shape.

Today:

- workflow gating already happens outside the payload predicate through `workflow_supports_first_hop_affordance(...)` and the `enabled` argument in the job-backed path (`src/presenter/first_hop_affordance.py:39-40`, `src/presenter/first_hop_affordance.py:63-86`)
- the transient path also reuses `derive_first_hop_affordance(...)` behind its own route gating (`src/presenter/compose_from_intent.py:1375-1419`)

If the goal is one shared derivation rule across both presenter lines, the smaller change is:

- keep the existing `enabled` gate
- add one explicit payload predicate for `view_key + engine_key + leaf`
- call that from `derive_first_hop_affordance(...)`

Threading `workflow_key` into `derive_first_hop_affordance(...)` would be a larger API change than the memo needs.

### 2. The transient-path requirement should be softer than the memo implies

The memo is right that the derivation rule should stay shared if it can.
But the current evidence base is asymmetric:

- job-backed presentation definitely serves `genealogy_idea_evolution` through the view registry
- the current transient genealogy proof only exercises `genealogy_final_synthesis`, not `concept_synthesis` or `genealogy_idea_evolution` (`tests/test_compose_from_intent.py:702-750`, `tests/test_compose_from_intent.py:753-832`)

So the rule should still live in the shared derivation seam.
But the mandatory proof bar for this slice should be:

- job-backed `_prepare_page_payloads(...)`
- job-backed `assemble_single_view(...)`
- one unit-level shared-derivation proof on the transient seam if we keep the rule in `derive_first_hop_affordance(...)`

It should not require a new end-to-end transient surface proof unless a real transient emitter for this view exists.

### 3. "View-specific or view+engine-specific" needs one calibration

Pure view-specific gating would likely work today.
But `view + engine + leaf` is better calibrated and more fail-closed.

Why:

- it preserves the memo's intent not to globalize `concept_synthesis`
- it also fails closed if the view definition is ever repointed to a different engine without revisiting the affordance policy

So the memo's more constrained version is preferable.
The only correction is that the workflow part should be left to the existing `enabled` gate, not forced into a wider derivation API unless implementation truly needs it.

## Factual Discrepancies I Found

### 1. `genealogy_idea_evolution` is definitely not eligible today

This is the key fact, and the memo gets it right.

The evidence chain is:

- allowlist-based generic derivation in `first_hop_affordance.py` (`src/presenter/first_hop_affordance.py:20-60`)
- `genealogy_idea_evolution` mapped to `concept_synthesis` (`src/views/definitions/genealogy_idea_evolution.json:15-20`)
- host helper fail-closed gate on `capturable === true` (`/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:42-53`)

### 2. There is no current test coverage for this exact `concept_synthesis` case

Existing affordance tests cover:

- approved migrated families in the job-backed path (`tests/test_presentation_api.py:1274-1655`)
- approved migrated families in the transient path (`tests/test_compose_from_intent.py:753-832`)

They do not currently include:

- `view_key="genealogy_idea_evolution"`
- `engine_key="concept_synthesis"`

So the memo is right to require new focused tests.

### 3. The roadmap context already assumes this sequencing

This is not a contradiction in the new memo, but it matters for honesty:

- the current state-of-play memo already says the next bounded scope should target one analyzer-side first-hop affordance eligibility slice for `genealogy_idea_evolution` before host helper adoption (`communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:226-235`, `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:432-475`)
- the fixed-direction roadmap says the same thing and explicitly prefers upstream fixes over downstream compensation (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:76-80`, `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:525-528`)

So the memo is aligned with the broader roadmap rather than trying to invent a new direction.

## What This Would Change For The Larger Roadmap

This slice would strengthen the roadmap in the right way, but only modestly.

What it would prove:

- analyzer-v2 can broaden first-hop semantic truth for one more bounded non-AOI analytical leaf
- the remaining `IdeaEvolutionRenderer` host work can then become a truthful consumer-alignment slice rather than a host exception
- the analyzer-v2-as-brain direction remains intact because the blocker is removed upstream, not papered over in Critic

What it would not prove:

- generic `concept_synthesis` capturability law
- generic renderer-package law
- non-AOI read-side truth surfacing
- broader genealogy identity semantics
- end-to-end host adoption on `IdeaEvolutionRenderer`

That calibration matches the strategic roadmap:

- analyzer-v2 should remain the intelligence layer
- hosts should stay thin (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:26-39`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:43-56`)
- representative generality matters more than cheap per-engine theater (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:61-71`)

This is a representative-matrix broadening step, not a platform-end-state claim.

## The Most Defensible Next Move After This Memo

The most defensible next move is:

1. Land one tiny shared derivation change in `src/presenter/first_hop_affordance.py`.
2. Keep it bounded to:
   - `payload.view_key == "genealogy_idea_evolution"`
   - `payload.engine_key == "concept_synthesis"`
   - `not payload.children`
   - existing `enabled` gate remains the workflow guard
3. Do not add `concept_synthesis` to the migrated engine-family allowlist.
4. Do not add `specialized_family`.
5. Do not touch host code in this tranche.

The most natural implementation shape is:

- add a small helper such as `_is_genealogy_idea_evolution_first_hop_leaf(payload)`
- update `derive_first_hop_affordance(...)` to allow:
  - current migrated analytical leaves
  - or that one explicit genealogy leaf

The test plan should be:

1. Add job-backed presenter tests proving `_prepare_page_payloads(...)` emits generic affordance for this exact leaf and still fails closed for wrong engine, wrong view, or parent payload.
2. Add `assemble_single_view(...)` coverage for the same leaf.
3. Add one shared-derivation unit proving the transient seam inherits the same rule if the payload appears there.
4. Keep the assertion explicitly generic-only:
   - `capturable = true`
   - `allowed_destinations = ["arsenal", "research_todo"]`
   - no `specialized_family`

After that lands, the next memo should return to the host side:

- align `IdeaEvolutionRenderer` to `currentRendererCapture.ts`
- require real analyzer-owned capturability truth
- keep capture coverage limited to the existing idea-card buttons

## Verification Notes

I verified the current state with:

- `PYTHONPATH=. pytest -q tests/test_presentation_api.py -k 'first_hop_affordance'` -> `4 passed`
- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py -k 'first_hop_affordance'` -> `16 passed`
- one direct local `derive_first_hop_affordance(...)` check for a `genealogy_idea_evolution` / `concept_synthesis` leaf -> `None`
