# Audit: Round 3 / Adaptive Surface Family Scope

Date: 2026-03-20
Reviewer slot: Codex audit slot repaired
Memo under review: `communications/MEMO_2026-03-20_round3_adaptive_surface_family_scope.md`

Note:

- the originally requested Codex audit was not delivered
- an implementation spike landed instead
- this file reconstructs the missing audit from direct inspection of the memo trail, the current code, and the adaptive spike so the planning record is complete

## Findings

### 1. The original memo's biggest gap was real: the family contracts were too editorially vague

The first draft correctly chose the strategic target but under-specified what the three families would actually render.

That gap is now concretely answerable from the spike in:

- `src/presenter/bounded_dynamic_composition.py:543`
- `src/presenter/bounded_dynamic_composition.py:664`
- `src/presenter/bounded_dynamic_composition.py:707`

The current feasible minimum family contracts are:

- `relationship_profile_dossier` -> `accordion` with dossier-style sections, including dominant relationship, field snapshot, evidence, and counterfactual
- `relationship_comparison_review` -> `table` with side-by-side rows for work, relationship, strength, channels, and why-it-matters
- `relationship_field_map` -> `accordion` with field summary, field snapshot, and per-relationship-type bands rendered as `mini_card_list`

This materially fixes the memo's earlier failure mode #3 risk. At least one family now uses a different top-level renderer type (`table`), so the proof is not just "same contract, different label."

### 2. The selector should be defined as aggregation across transformed per-item cards, not raw prose

This is now clear in the spike:

- `src/presenter/bounded_dynamic_composition.py:392`
- `src/presenter/bounded_dynamic_composition.py:408`
- `src/presenter/bounded_dynamic_composition.py:822`

The selector reads the collection of already-transformed relationship cards from:

- `genealogy_relationship_landscape.items[*].structured_data`

That is the right architectural choice. It keeps round-3 inside the presentation layer and avoids reopening raw phase-output interpretation or adding a new inference pass.

The memo should state this as a hard rule, not just an implication.

### 3. Round-3 composition should be independent from round-2, and the current code already models it that way

The clean activation shape is now visible in:

- `src/presenter/bounded_dynamic_composition.py:14`
- `src/presenter/bounded_dynamic_composition.py:23`
- `src/presenter/bounded_dynamic_composition.py:213`

`adaptive_relationship_surface_v1` is a distinct `composition_mode`, not a stacked extension of `bounded_dynamic_genealogy_v1`.

That should remain a hard rule in the memo:

- one proof mode at a time
- no requirement that the round-2 generated-parent hierarchy be active simultaneously

This keeps the round-3 claim narrow and inspectable.

### 4. The proposed target is still the right bounded proof surface

The authored baseline for `genealogy_relationship_landscape` is still:

- one `card_grid`
- `group_by = relationship_type`
- `columns = 1`
- one repeated card template

See:

- `src/views/definitions/genealogy_relationship_landscape.json:9`

That makes it the strongest next proof target because:

1. the baseline is visibly static
2. the structured relationship cards already exist
3. the adaptive proof can stay local to one authored surface
4. the host can remain unchanged

I do not see a smaller target with a better combination of visible variance, low host risk, and available structured signals.

### 5. The host can stay unchanged for this proof

The Critic side already threads `composition_mode` generically and renders from the returned presentation tree:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:155`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:285`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:354`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:117`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:155`

There is no hidden host blocker here comparable to the round-2 generated-top-level-key problem. This proof should succeed or fail upstream.

### 6. The implementation spike is useful evidence, but it does not replace scope review

The spike added:

- adaptive composition-mode support in `src/presenter/bounded_dynamic_composition.py`
- adaptive trace output in `src/presenter/decision_trace.py:212`
- focused tests in `tests/test_presentation_api.py:333` and `tests/test_manifest_trace.py:817`

That is good feasibility evidence.

It is not the same thing as an independent audit. Planning should absorb the useful parts of the spike, then explicitly decide whether to ratify that exact proof shape.

## Open Questions / Weak Assumptions

### 1. Three families are now feasible, but two might still be enough

The spike shows three concrete families are viable. That said, the middle family (`relationship_comparison_review`) may be the hardest to distinguish semantically from the other two in weak data. If the goal is the narrowest first proof, two families would still be a defensible reduction.

### 2. The current selector thresholds are code-level heuristics, not yet an endorsed program contract

The spike currently uses dominance and diffusion thresholds in:

- `src/presenter/bounded_dynamic_composition.py:460`

That is fine for a bounded proof, but the memo should be careful not to overclaim those exact thresholds as platform policy. The real bounded claim is:

- deterministic selection from existing structured signals

not:

- these exact numeric thresholds are final

### 3. The round-2 documentary gate needed an owner

The earlier memo correctly named the gate but did not assign it. That gap should now be closed explicitly by naming the maintainer preparing round-3 execution planning as the owner of the short round-2 completion note.

## What The Memo Gets Right

### 1. The strategic progression is correct

The memo trail is coherent:

- round-1 proved the thin host boundary and first reusable seam
- round-2 proved bounded runtime hierarchy composition
- round-3 should isolate content-sensitive surface-family selection

That is the right next question.

### 2. Deterministic selection is the right next proving method

The available signals in the transformed relationship cards are enough. A new LLM scoring/refinement pass would add ambiguity and weaken inspectability.

### 3. The inspectability requirement is strong

The `adaptive_surface_selection` trace stage is the right diagnostic contract. The current spike already shows that shape is feasible in:

- `src/presenter/decision_trace.py:214`

### 4. The target surface is well chosen

`genealogy_relationship_landscape` is the best bounded target because it stays local, already carries the needed structured relationship cards, and directly addresses the "same structure across unlike jobs" complaint in `the-critic/communications/NEXT_SESSION_DYNAMIC_COMPOSITION_AUDIT.md`.

## Verdict

The strategic direction is right and the proving target is right. The original memo needed tightening around renderer-level family contracts, selector input source, round-2 independence, and documentary ownership. The current adaptive spike now provides concrete evidence for those corrections. After revising the memo to absorb those four points and closing the round-2 completion note, the scope becomes execution-ready. The next step should be an execution-plan pass that audits the existing adaptive spike against that revised bounded claim, not another broad rescoping cycle.
