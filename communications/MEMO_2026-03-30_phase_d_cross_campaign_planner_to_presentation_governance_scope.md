# Memo: Phase D Cross-Campaign Planner-To-Presentation Governance Scope

Subtitle: A second broader planner-to-presentation governance family proving the stack is not artifact-identity-coupled to one proof campaign

Date: 2026-03-30
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Immediate Prior Completion:
- `communications/MEMO_2026-03-30_phase_d_planner_to_presentation_governance_family_v1_completion.md`

## Purpose

Define the next bounded Phase D step after the first planner-to-presentation governance family.

On the distilled roadmap, we are still:

- in `Phase D: Governance And Accountability`

The next slice should keep strengthening analyzer-owned governance honestly without pretending we have already moved into:

- `Phase E: Generality Proof`

## Strategic Framing

The planner-to-presentation governance completion means the governance stack now has:

- one composite AOI-plus-genealogy family
- one declared genealogy-only family
- one declared AOI-only family
- one upstream routing/planning governance family
- one upstream planner-to-presentation governance family

So the remaining open Phase D question is no longer:

- whether governance can stand over planner-to-presentation composition surfaces at all

The remaining open Phase D question is:

- whether the same governance law is still too coupled to the March 27-30 AOI proof bundle plus the March 28 genealogy transient trace, or whether it can survive one second fresher paired proof lineage without changing the governance substrate

That is why the next honest Phase D move is not:

- UI or review-product expansion
- downstream enforcement or unlock/deny behavior
- broader pack-global currentness law
- a premature jump into Phase E matrix proof

It is:

- one second planner-to-presentation governance family over a fresh paired AOI/genealogy current-contract proof campaign

This is still Phase D work.
It is still retrospective governance over frozen proof artifacts, not live governance over the current planner/presenter.
It is still not a generic evaluator-extensibility or arbitrary-engine composition proof.

## Why This Is The Right Next Phase D Slice

Analyzer-v2 already has the relevant substrate in repo:

- immutable planning-decision persistence
- planner-to-presentation handoff models
- analyzer-owned presenter composition routes
- one landed `planner_presentation_decision` evaluator branch
- one landed planner-to-presentation governance family and semantic status seam

And the current Phase D gap is now narrower:

- governance reaches downstream result/lifecycle families
- governance reaches standalone AOI and genealogy families
- governance reaches one upstream routing/planning family
- governance reaches one upstream planner-to-presentation family
- but governance is still anchored to one bounded proof campaign and one mixed-vintage genealogy trace line

So the cleanest next bounded step is:

- prove that the same planner-to-presentation governance law survives a second fresh paired proof campaign without changing route shapes, schema shapes, or governance-status law

That advances the strategic question directly:

- is the governance stack already reusable enough to survive a second upstream proof family, or is it still only a wrapper around the current proving dossier?

One implementation consequence should be named explicitly:

- this slice should reuse the existing `planner_presentation_decision` evaluator family
- but reuse does not mean unchanged harness code
- new case keys will require new case-spec entries and bounded extraction work inside `src/evaluations/frozen_pack_harness.py`
- a fresher genealogy proof bundle will likely need an explicit new extraction branch unless it intentionally preserves the old trace shape

That is acceptable.
It is still a bounded reuse proof, not a new evaluator-family program.

## Scope Decision

### In scope

#### 1. One fresh paired AOI and genealogy current-contract proof campaign

Add one new paired proof campaign under `communications/`.

Both sides should be captured fresh and hash-pinned:

- one fresh AOI transient compose bundle
- one fresh genealogy transient compose bundle

Both bundles must carry, on frozen proof surfaces:

- planning decision evidence
- persisted planning snapshot evidence
- compose request evidence
- compose response evidence
- stable `planning_decision_id` agreement between persisted planning truth and compose execution

Important anti-coupling rule:

- the new family should not reuse the first planner-to-presentation pack’s exact proof files
- the point is to prove the same evaluator/gate/review/resolution/status substrate over a second artifact lineage, not to restate the first lineage under new keys

Important anti-drift rule:

- keep the evidence `communications/`-scoped and hash-pinned
- do not point pack artifacts directly at live persisted planning files under `src/orchestrator/planning_decisions`
- do not build a generic proof-capture framework for this slice
- capture the fresh paired campaign once, commit it, and pin hashes

Recommended AOI boundary:

- keep the current AOI bundle shape:
  - planning decision
  - planning snapshot
  - `compose-from-selection` request
  - `compose-from-selection` response

Recommended genealogy boundary:

- prefer a fresh dedicated genealogy transient compose bundle over continued reliance on the March 28 multi-surface trace
- the fresh genealogy bundle must carry explicit bundle-level `planning_decision_id` binding metadata because `/v1/presenter/compose-from-intent` does not carry `planning_decision_id` natively in its public request contract
- if the fresh genealogy bundle needs a slightly different extraction path from AOI, keep that asymmetry explicit
- decide the genealogy bundle shape explicitly rather than leaving it implicit:
  - either preserve the existing logical surfaces
    - `planning_decision`
    - `planning_snapshot`
    - compose request
    - compose response
    - bundle-level `planning_decision_id`
  - or say clearly that bounded extractor adaptation is in scope

The honest claim after implementation should be:

- the same planner-to-presentation governance law is not artifact-identity-coupled to only one proof lineage

It should not be:

- governance now generalizes over arbitrary proof shapes or arbitrary evaluator families

#### 2. One second planner-to-presentation governance family reusing the existing evaluator family

Add one second pack definition using the already-landed evaluator family:

- `evaluator_key = planner_presentation_decision`

Recommended pack identity:

- `evaluation_pack_key = phase4_planner_to_presentation_cross_campaign_governance_v1`

Recommended cases:

- `aoi_compose_selection_current_contract_fresh_campaign`
- `genealogy_direct_sections_compose_current_contract_fresh_campaign`

Add one second gate/review/resolution family on top of that pack:

- `gate_key = bounded_planner_to_presentation_cross_campaign_readiness_v1`
- `review_key = bounded_planner_to_presentation_cross_campaign_review_v1`
- `resolution_key = bounded_planner_to_presentation_cross_campaign_resolution_v1`

The second family should reuse unchanged:

- the four planner-to-presentation dimensions:
  - `handoff_contract_fidelity`
  - `planner_presentation_agreement`
  - `presentation_contract_fidelity`
  - `composition_trace_integrity`
- the existing `accept / reject / waive` review law
- the existing recording-only resolution law
- the existing semantic governance-status seam

Important implementation boundary:

- do not add a new evaluator family unless a concrete proof-shape requirement forces it
- the default assumption is that this should be one second family on the existing `planner_presentation_decision` evaluator substrate
- but say this honestly:
  - expect new `_PLANNER_PRESENTATION_CASE_SPECS` entries
  - expect bounded new extraction handling in `_extract_planner_presentation_evidence(...)`
  - do not describe this as definition-only reuse or unchanged harness execution

#### 3. One real second cross-campaign governance chain

Materialize one real second planner-to-presentation governance chain using the existing builders and routes:

- two fresh reports
- one gate
- one `accept` review
- one resolution

Read semantic status through the unchanged route:

- `GET /v1/evaluations/governance-status/current`

The real chain should be framed honestly as:

- retrospective cross-campaign planner-to-presentation governance proof
- not live governance
- not a Phase E generality claim

#### 4. Focused regression coverage on anti-coupling

Extend the existing governance suites rather than creating a new harness family.

Required coverage:

- the second pack loads by key and contains exactly the two declared cases
- the second family reuses `planner_presentation_decision`, not a new evaluator family by default
- the fresh AOI bundle ties one stable `planning_decision_id` across planning snapshot and compose evidence
- the fresh genealogy bundle also ties one stable `planning_decision_id` across planning snapshot and compose evidence through explicit bundle-level binding metadata
- the second family produces two passing reports and one passing gate
- the unchanged review and resolution builders succeed for the new keys
- the unchanged semantic status route returns:
  - `200`
  - `effective_governance_status = approved`
  - nested resolution linkage to the second family keys
- the first planner-to-presentation family still passes unchanged
- the older standalone and routing/planning families still pass unchanged

One explicit anti-coupling regression should be present:

- the second family must pass on its own pinned artifact paths and hashes without reusing the first family’s exact proof files

### Out of scope

- generic proof-capture tooling
- live governance policy
- human-facing governance UI
- downstream enforcement or unlock/deny behavior
- generic evaluator-plugin architecture
- Phase E representative matrix proof

## Decision Rule

This slice is worth doing only if it proves something the first planner-to-presentation family did not.

That means:

- a second declared pack alone is not enough
- a renamed copy of the March 27-30 / March 28 proof files is not enough
- the slice earns its keep only if it demonstrates the same governance law over a genuinely fresher paired proof lineage

## What Success Would Mean

If this slice lands cleanly, the honest claim becomes:

- governance now stands over the planner-to-presentation layer across more than one bounded proof lineage and is not artifact-identity-coupled to only one dossier

That still does not mean:

- Phase D is automatically closed
- Phase E has started in earnest

But it would materially strengthen the case that the governance substrate is not just a wrapper around one frozen proving dossier.

One strategic limit should also be explicit:

- if this slice starts demanding broad harness redesign, new evaluator-family architecture, or a large amount of campaign-specific extraction work, that is likely a sign the program should stop extending Phase D and pivot to a minimal Phase E matrix instead of deepening governance-specific accretion

## Review Questions

1. Is a second fresh planner-to-presentation proof campaign the right next bounded Phase D step after the first landed family?
2. Is reusing `planner_presentation_decision` the right default, or does the memo underestimate fresh genealogy proof-shape friction?
3. Does the memo keep the anti-coupling claim honest without slipping into Phase E language?
4. Is there a smaller alternative that would still prove governance is not too tied to the current proving campaign?
