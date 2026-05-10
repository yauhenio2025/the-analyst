# Prompt For Claude: Phase 2 Host-Neutral Transient Proof Scope Critique

Critique the newly drafted Phase 2 scope memo:

- `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`

Your job is to test the robustness of the assumptions behind that memo against:

- the actual current codebase in `analyzer-v2`, `the-critic`, and `aoi-canary`
- the recent March 24-27 roadmap and memo trail
- the bigger program objective of making `analyzer-v2` the analytical brain while downstream apps become thin hosts

## Bigger-picture objective

Evaluate the memo in light of the real target:

- analyzer-v2 should own analytical understanding, routing, planning, composition law, and presentation law
- current apps should be proving harnesses, not long-term workflow-specific controllers
- Phase 1 should close bridge generalization before Phase 2 tries to prove broader host-neutral transient consumption

So judge the memo both as:

1. a bounded next implementation scope after verified Phase 1C completion
2. a sequencing decision about how to earn stronger transient proof without drifting into lifecycle or new consumer-local intelligence

## What to inspect first

Read these docs before writing your critique:

- `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`
- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`
- `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_scope.md`

Then search `communications/` and `docs/` for any additional recent memos or reports that materially bear on:

- host-neutral proof
- transient compose
- planning snapshots
- Host Contract v2
- `aoi-canary`
- genealogy saved-result direct-sections planning

## Code paths to inspect

Analyzer:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_routing_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_router.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planning_schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/direct_sections_compose_harness.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/genealogy_saved_result_bridge.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`

Current consumer and comparison surfaces:

- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/aoi-canary/src/App.tsx`
- `/home/evgeny/projects/aoi-canary/src/lib/resultsClient.ts`

## Questions to answer directly

1. Is the memo correct that the main missing proof after Phase 1C is stronger host-neutral transient consumption, not more bridge generalization?
2. Is the memo right to choose a minimal dedicated proof harness as the default vehicle rather than extending the current AOI `the-critic` path again?
3. Is `genealogy + saved_result + direct_sections_composition_handoff_plan` the right bounded first transient target, or is the memo choosing the wrong seam?
4. Does the code actually support the memo’s claim that this proof can avoid:
   - `the-critic` AOI proxy routes
   - `/v1/executor/jobs`
   - host-local section reconstruction
5. Is the memo honest about what `aoi-canary` does and does not already prove?
6. Is there any hidden blocker that would force this slice to reopen:
   - planner/router contracts
   - presenter boundary shape
   - host ownership doctrine
   - lifecycle/session semantics?
7. Is the optional ephemeral token/session borrow well-bounded, or does it risk sneaking Phase 3 into Phase 2?
8. Does the memo stay properly bounded relative to the larger sequence:
   - completed Phase 1
   - still-open Phase 2
   - deferred Phase 3 lifecycle
9. Is it concrete enough to guide safe implementation, or does it still leave critical boundary choices unresolved?

## Output requirements

Write your critique to exactly this file:

- `communications/REPORT_Claude_Phase2_Host_Neutral_Transient_Proof_Scope_Critique_2026-03-27.md`

Your output should include:

1. A verdict:
   - `Approve`
   - `Approve after revision`
   - `Do not approve`
2. Findings first, ordered by severity.
3. Specific file/line references where relevant.
4. A direct answer to whether this is now the right next honest step.
5. A direct answer to whether the memo stays properly bounded.
6. Any concrete revisions needed before implementation.

Prioritize hidden assumptions, codebase mismatches, scope drift, and roadmap mis-sequencing over general summary.

Do not edit the memo.
Do not make code changes.
This is a documentation/code-path critique only.
