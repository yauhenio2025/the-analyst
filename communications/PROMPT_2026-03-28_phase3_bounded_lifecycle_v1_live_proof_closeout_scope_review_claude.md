# Prompt For Claude: Phase 3 Lifecycle Live Proof Closeout Scope Critique

Critique the newly drafted Phase 3 live-proof closeout memo:

- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md`

Your job is to test the robustness of the assumptions behind that memo against:

- the actual current codebase in `analyzer-v2`, `the-critic`, and any relevant current supporting surfaces
- the recent March 27-28 roadmap and memo trail
- the bigger program objective of making `analyzer-v2` the analytical brain while downstream apps become thin hosts

## Bigger-picture objective

Evaluate the memo in light of the real target:

- analyzer-v2 should now own not only analytical understanding, routing, planning, composition law, and presentation law, but also the saved truth of reopenable transient analytical surfaces where lifecycle is reopened
- downstream apps should stay thin hosts that carry navigation and bounded runtime execution, not become lifecycle truth authorities
- Phase 4 governance/evaluation should sit on top of a live-proved lifecycle path, not substitute for missing lifecycle evidence

So judge the memo both as:

1. the bounded next execution scope after the Phase 3 lifecycle implementation landed
2. a sequencing decision about whether the program is actually ready to move from implementation into honest closeout

## What to inspect first

Read these docs before writing your critique:

- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_live_proof_closeout_scope.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_implementation_completion.md`
- `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`
- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
- `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`
- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

Then search `communications/` and `docs/` for any additional recent memos or reports that materially bear on:

- lifecycle closeout
- save/reopen law
- compose sessions
- planning snapshots versus lifecycle identity
- proof artifacts
- governance/evaluation sequencing

## Code paths to inspect

Analyzer:

- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_session_store.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/presenter.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`

Current consumer / proof surface:

- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.test.tsx`

## Questions to answer directly

1. Is a Phase 3 live proof closeout now the right next honest step, or is the memo prematurely blocking on evidence that the code already makes unnecessary?
2. Is the memo right to keep the closeout on the existing genealogy proof page rather than widening into a new proof surface or AOI proxy lifecycle?
3. Does the code support the memo’s claim that lifecycle save/reopen is implemented but still lacks recorded live proof?
4. Is the memo drawing the analyzer/host ownership line clearly enough for:
   - saved session truth
   - reopen payload truth
   - `session_id` handling
   - browser navigation?
5. Is the memo correct that `planning_decision_id` remains provenance only and cannot substitute for lifecycle identity?
6. Is the required evidence shape strong enough to prove “no recomputation on reopen”?
7. Does the memo stay properly bounded away from:
   - Phase 4 governance/evaluation
   - publish/share
   - auto-save
   - new transient consumer registration
   - AOI-specific productization?
8. Is anything in the memo contradicted by the live code?
9. Is anything important missing that would make the scope under-specified or unsafe to execute?

## Output requirements

Write your critique to exactly this file:

- `communications/REPORT_Claude_Phase3_Bounded_Lifecycle_V1_Live_Proof_Closeout_Scope_Critique_2026-03-28.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether this is now the right next honest step.
5. A direct answer to whether the memo stays properly bounded.
6. Any concrete revisions needed before execution.

Prioritize hidden assumptions, codebase mismatches, scope drift, and roadmap mis-sequencing over general summary.

Do not edit the memo.
Do not make code changes.
This is a documentation/code-path critique only.
