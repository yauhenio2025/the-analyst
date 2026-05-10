# Memo: Stage 5 AOI Execution-Backed Evolution-Ready Scope

Date: 2026-03-25
Status: Draft scope memo
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_completion.md`
- `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json`
- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_completion.md`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Summary

The frozen Stage 5 AOI pack now passes on the repaired planner-primary path.

That means the next honest move is no longer another seam repair and no longer another fixture-only rerun.

The remaining gap is evidence strength:

- Stage 5 seam behavior is now proven on `fixture_backed` evidence
- Stage 2 still remains open because the rubric requires at least one ready case to be `execution_backed` or stronger
- `execution_backed` is not runtime-enforced by the product path, so freshness must be proven by a tightly cross-linked artifact bundle rather than assumed from one field

So the next step should be one bounded evidence-upgrade slice:

- intentionally upgrade `evolution_ready` from `fixture_backed` to `execution_backed`
- use the real AOI launch route in `the-critic` to produce fresh outputs
- then run the same planner-backed `evolution_ready` compose path against that newly produced result
- decide Stage 2 separately from the already-recorded Stage 5 pass

## Why This Is The Next Honest Step

The code path that previously blocked the exemplar has already been repaired and rechecked:

- selector/provider hardening is landed
- AOI identity continuity is landed
- warm-snapshot durability is landed
- analyzer-side selection-compose contract alignment is landed
- the live repaired `evolution_ready` rerun passed
- the same frozen four-case Stage 5 pack passed

So the unresolved question is no longer:

- does the seam work at all?

It is now:

- is there at least one fresh end-to-end AOI ready case strong enough to support Stage 2 documentary closure honestly?

That is an evidence question, not a new architecture question.

## Bounded Claim

This slice should only do one thing:

- produce one fresh `execution_backed` `evolution_ready` AOI case on the counted planner-primary path

This slice should not reopen:

- the frozen four-case Stage 5 pack by default
- selector/provider logic
- AOI identity continuity
- warm-snapshot durability
- analyzer transient compose shaping
- roadmap order
- Tranche 3 generalization
- lifecycle/governance work

## Scope Decisions

### Decision 1: Treat this as an evidence-upgrade step, not a new repair tranche

The previous Stage 5 implementation blockers are now closed baseline for this step.

If a fresh execution-backed run exposes a genuinely new product-path seam, stop and write a new revision memo.
Do not pretend this memo authorizes speculative widening in advance.

### Decision 2: Use `evolution_ready` as the default upgrade candidate

Default candidate remains:

- case: `evolution_ready`
- project: `round5-proof-dossier-final-1774100000`
- thinker: `otto_neurath`
- task: `Show how Aaron Benanav's use of Otto Neurath's planning argument evolves across the corpus.`

Reason:

- this is already the best-understood ready case in the current artifact trail
- it already proved the repaired planner-backed path end to end
- earlier review notes already named it as the default `execution_backed` upgrade candidate

Do not silently substitute another case unless the closeout memo explicitly explains why.

### Decision 3: Define `execution_backed` strictly

For this step, `execution_backed` means:

- a fresh AOI thematic run is launched through the real `the-critic` route:
  - `POST /api/influence/thinkers/{thinker_id}/run-thematic-analysis-v2`
- the resulting outputs are newly produced in this run
- the subsequent planner-backed compose proof uses that fresh result's `source_v2_job_id`

It does **not** count as `execution_backed` if the run reuses only previously saved result outputs as the authoritative source.

Freshness must therefore be proven documentarily.

Required proof bundle must cross-link the same fresh job through:

- launch response
- active-run discovery or equivalent active boundary proof
- completed job detail
- completed result detail
- counted planner-backed compose request/response

On this v2-backed AOI route, the Critic-visible `job_id` is the analyzer-v2 job id.
The docs should preserve that single identity consistently rather than implying two distinct fresh ids.

### Decision 4: Preserve the counted planner-primary path exactly

After the fresh run completes, the counted proof branch must remain:

- AOI panel
- planner-backed continue
- `/compose-from-intent`
- `compose-from-selection`
- canonical `source_v2_job_id` preserved end to end

No legacy/profile fallback may count toward acceptance.
This explicitly excludes the profile/autostart branch that can drop `source_v2_job_id`.

### Decision 5: Make preflight prerequisites explicit

This step assumes a real local execution environment, not just saved-result recomposition.

Required preconditions include:

- the project and thinker exist locally
- uploaded reference texts exist for the target thinker
- analyzer-v2 is reachable from the-critic on the actual resolved local port
- selector/provider credentials are available in the live analyzer environment
- the actual resolved Critic backend and webapp ports are recorded in the artifact bundle

If these are not true, the proof is not yet runnable and should not be described as ready to execute.

### Decision 6: Reuse the passed frozen pack as baseline rather than rerunning it again by default

The frozen four-case pack already passed.

This step should therefore add stronger evidence on top of that baseline rather than rerunning the whole pack again unless the fresh run exposes a new seam that makes a broader rerun necessary.

### Decision 7: Keep Stage 5 and Stage 2 decisions separate

The closeout for this step must say separately:

- Stage 5 seam gate already passed on fixture-backed evidence
- whether this new execution-backed case is strong enough to close Stage 2 honestly

Do not collapse those into one claim.

The closeout must also answer the rubric’s stronger qualitative bar directly:

- whether this one clean execution-backed case is strong enough to support repeated bounded AOI transient use rather than only one-off success

### Decision 8: Use explicit stop-and-revise rules

Stop and write a new revision memo if any of the following happen:

- the fresh AOI launch route fails before a real run is created
- the known preflight prerequisites are missing and the proof cannot even start honestly
- the fresh run never reaches a durable completed result
- the fresh result does not expose the expected AOI ready-case material
- planner-backed continuation drifts off the counted path
- canonical `source_v2_job_id` is dropped or rewritten
- `compose-from-selection` fails on the fresh result
- success can be claimed only by falling back to fixture-backed or legacy behavior

## Proposed Deliverables

### 1. One execution-backed proof bundle

At minimum:

- one launch artifact preserving the fresh returned `job_id`
- one active boundary artifact
- one completed job/result boundary artifact proving the same job remained the authoritative source
- one request JSON artifact for the planner-backed `evolution_ready` compose flow labeled `execution_backed`
- one browser HAR
- one UI screenshot

The smoke script may contribute to the boundary bundle, but it does not by itself prove the counted browser compose path.

### 2. One execution-backed diagnosis note

Produce a short note that states:

- whether the case was truly `execution_backed`
- what fresh job/result ids were used and how they cross-link
- whether the counted planner-primary path held
- whether the ready case satisfied the `evolution_ready` minimum shape
- whether the evidence is strong enough to support Stage 2 closure
- whether the evidence is strong enough to support repeated bounded AOI transient use under the current rubric

### 3. One closeout memo

Produce one of:

- success: `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_completion.md`
- failure/revision: `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_revision.md`

That memo must also update the current roadmaps if the Stage 2 decision changes.

## Acceptance Criteria

This scope is successful only if one of these is true:

1. one fresh `execution_backed` `evolution_ready` case is captured on the counted planner-primary path, uses newly produced AOI outputs, and gives a real Stage 2 closure decision
2. the attempt exposes a new blocker, but that blocker is documented honestly in a revision memo without pretending the evidence bar was met

This scope does **not** count as successful if:

- the case is still effectively `fixture_backed`
- the proof drifts onto legacy/profile controls
- the fresh run exists but the counted planner-backed compose path is not re-proven
- the closeout quietly upgrades Stage 2 without preserving the stronger-tier evidence trail

## Status Implications

Until this step lands successfully:

- Stage 5 seam gate remains passed on fixture-backed evidence
- Stage 2 remains open
- Tranche 3 remains blocked

If this step succeeds:

- Stage 2 may be honestly documentary-closed
- the roadmap may then move Tranche 3 to the front of the program line
- but only after that decision is written explicitly in the closeout
