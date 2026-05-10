# Critique: Round 3 / Adaptive Surface Family Scope

Date: 2026-03-20
Reviewer: Claude (Opus 4.6, 1M context)
Memo under review: `communications/MEMO_2026-03-20_round3_adaptive_surface_family_scope.md`

---

## Summary

The memo correctly identifies the next missing variable in the Thin Consumer Platformization program and chooses the right proving target. The strategic progression from round-1 (thin host boundary) through round-2 (bounded runtime hierarchy) to round-3 (content-sensitive surface-family selection) is logically sound and well-grounded in the memo trail. The scope is appropriately tight. The main risk is not strategic direction but insufficient specification of what the three families actually produce at the renderer/section contract level — without that, the proof could degenerate into "a string field changed while the actual surface stayed the same," which the memo itself names as failure mode #3 but does not yet prevent structurally.

---

## Corrections Needed

### 1. The three families need concrete renderer-level contracts, not just editorial intent descriptions

The memo defines Family A/B/C at the narrative level ("focused predecessor dossier," "side-by-side comparison," "clusters and bands") but does not specify what these mean in terms of `renderer_type`, `renderer_config`, `section_renderers`, or card template slots. Without this, the proof cannot be verified against failure mode #3.

The current `genealogy_relationship_landscape` view definition (`src/views/definitions/genealogy_relationship_landscape.json`) uses:
- `renderer_type: "card_grid"`
- `group_by: "relationship_type"`
- `columns: 1`
- A rich card_template with badge_row, heading, prose, chip_list, evidence_trail

If all three families still use `card_grid` with the same card template and just vary `group_by` or `columns`, the proof would be trivially true but strategically meaningless. The memo should require that at least one family use a materially different renderer_type or section hierarchy — not merely different config parameters within the same renderer.

**Recommendation**: Add a section specifying the minimum renderer-level contract difference between families. For example:
- Family A (`relationship_profile_dossier`): `accordion` renderer with one dominant-precursor section and supporting-context sections
- Family B (`relationship_comparison_review`): `card_grid` with `columns: 2` or `group_by` variant + comparison summary prose
- Family C (`relationship_field_map`): `card_grid` with cluster grouping + a field-level prose summary section

### 2. The selector operates on aggregated per-item data — this should be explicit

The relationship_landscape view has `scope: "per_item"`, meaning the presentation layer generates one structured card per prior work. The selector needs to aggregate across all items for a job to compute signals like "one dominant precursor vs. distributed field." The memo should state explicitly that the selector reads the **collection** of relationship extraction outputs, not individual cards. This is architecturally non-trivial: the selector must run before or alongside the per-item view assembly, not after.

In the current codebase, per-item transformation happens in `presentation_bridge.py` where `_build_transformation_tasks` generates one task per `work_key`. The selector must either:
- read the raw phase outputs for phase 1.5 directly (before transformation), or
- read the already-transformed presentation_cache entries (after transformation)

The memo should specify which.

### 3. The memo should name the composition_mode string value

The memo says the proof should activate via `composition_mode=adaptive_relationship_surface_v1`. Good. But it should also confirm that the implementation should follow the existing pattern in `bounded_dynamic_composition.py`, where a new constant and validation check are added. The round-2 code already established this pattern (`COMPOSITION_MODE_BOUNDED_DYNAMIC_GENEALOGY_V1`). The memo should state whether round-3 composition stacks on top of round-2 or is independent. The current recommendation ("do not require the round-2 generated-parent proof mode to be active at the same time") is correct but should be elevated to a hard rule.

### 4. The round-2 documentary gate is described but has no owner or deadline

The memo correctly says "the team should write one short round-2 completion/proof note" before starting round-3. But there is no existing round-2 closure memo in the communications folder. The gate should name who writes it and whether it blocks implementation planning (it should not) or only implementation execution (it should).

---

## What The Memo Gets Right

### 1. The strategic progression is sound and well-argued

The memo correctly builds on the trail: round-1 proved the host can be thin, round-2 proved runtime hierarchy generation works, round-3 isolates the next variable (content-sensitive family selection). This is genuinely the right next question.

### 2. Genealogy relationship_landscape is the right proving target

The audit evidence from `NEXT_SESSION_DYNAMIC_COMPOSITION_AUDIT.md` shows that Markus (3 prior works, distributed field) and Varoufakis (5 prior works but 1 dominant card) currently receive identical treatment. The relationship_landscape is exactly the surface where different analytical situations should produce visibly different presentations. The memo's reasoning for preferring this over `dynamic_genealogy_trajectory`, `genealogy_conditions`, or AOI is convincing.

### 3. Deterministic selection over LLM is correct

The structured data from relationship extraction already includes `relationship_type`, `relationship_strength`, item count, and `influence_channels`. These are sufficient signals for deterministic family selection. A fresh LLM pass would be overkill and would violate the inspectability requirement.

### 4. The trace/diagnostic requirement is strong

The `adaptive_surface_selection` trace stage (showing signals read, family chosen, rejected families, and reason) is the right diagnostic contract. It directly supports the inspectability requirement and prevents the failure mode where "the model somehow chose a different layout."

### 5. The host-neutrality constraint is verified by the codebase

My inspection confirms that `AnalysisWorkspacePage.tsx` already passes `composition_mode` through to all presenter API calls generically. The `V2TabContent.tsx` rendering pipeline is fully data-driven and has no composition_mode branching. A new composition_mode requires zero host code changes. The memo's host-neutrality requirement is not aspirational — it is already architecturally guaranteed.

### 6. The scope exclusions are honest and specific

The out-of-scope list is well-targeted. Excluding AOI, multi-surface adaptation, whole-page regeneration, and generalized framework work keeps the proof bounded. The warning about scope drift ("if the work starts turning into adaptive everything") is the right guardrail.

### 7. The acceptance criteria are measurable

Criterion 10 ("at least two contrast jobs can be shown to select different surface families on the same generic route") is the right binary test. Combined with criterion 6 (family validation by explicit renderer/data contracts), this prevents both false positives and trivially-true proofs.

---

## Recommended Scope Adjustments

### 1. Add a "Family Contract Minimum" section

Between the current "Proposed Surface Families" and "Surface-Family Contract" sections, add a concrete minimum contract for each family. This does not need to be a full implementation plan, but it should specify:
- The renderer_type for each family
- Whether the family is a single view or a multi-section view
- At least one structural difference from the other families that a human reviewer can verify visually

### 2. Specify that the selector reads from already-available structured data, not raw prose

The memo says "already-available analytical signals" but should clarify: the selector should read from the presentation_cache entries (post-transformation structured JSON), not from raw phase_output prose. This is important because the structured data already contains `relationship_type`, `relationship_strength`, and item count in machine-readable form.

### 3. Add one constraint: the three families must not all use the same renderer_type

This prevents the proof from degenerating into a config-only variation. At least one family should use a different renderer_type from the other two. This is the cheapest structural constraint that makes the proof meaningful.

### 4. Consider reducing from three families to two for the first proof

The memo allows "2 or 3" but recommends three. Two families would be simpler, easier to contrast, and sufficient for the bounded claim. Three families risk introducing a middle category that is hard to distinguish from both extremes. If three are kept, the acceptance criteria should require at least two jobs to select different families — which is easier with two families than three.

### 5. The documentary gate for round-2 should be light

The gate is correct but should explicitly say: a 10-line note naming the route, the bounded claim, the renderers exercised, and the final verification result is sufficient. Do not let the gate become its own project.

---

## Verdict

**Approve after revision.**

The strategic direction is correct. The proving target is well-chosen. The scope constraints are honest and appropriate. The host-side architecture already supports the proof without changes. The main revision needed is concrete renderer-level specification for the three families — without that, the proof risks proving a selection mechanism while failing to prove actual surface-family differentiation. With the family contracts specified at even a minimal level, this memo is ready to become the operative scope document for round-3.

Do not redirect. Do not expand scope. Add the family contracts and proceed.
