# Prompt For Claude: Review The Phase 1B Host Ownership / Contract Unification Scope Memo

You are reviewing a new bounded scope memo inside the `analyzer-v2` workspace.

## Primary artifact to review

- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_scope.md`

## Your task

Test whether this memo is actually the right next Phase 1B slice after honest Phase 0 closure.

You should do all of the following before writing your output:

1. Read the Phase 1B memo closely.
2. Examine the bigger-picture strategy and current program state in at least:
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
3. Look through any other recent memos or reports in `communications/` or `docs/` that materially bear on:
   - host contract
   - planner-to-presentation bridge
   - task intake / routing / planning
   - source identity
   - warm snapshot / continuity alias
   - surface selection
   - transient compose
4. Scrutinize the memo’s claims against the live codebase, especially:
   - `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractRuntime.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
   - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
   - `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
   - `/home/evgeny/projects/the-critic/api/server.py`
   - `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_router.py`
   - `/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py`

## Questions you must answer

1. Is Phase 1B, as framed here, actually the right next slice after Phase 0 closeout, or is the memo still too abstract or too large?
2. Are the five working hypotheses well chosen, or is one of them prematurely locking a solution?
3. Is the source-identity problem framed correctly in light of:
   - Stage 7’s `source_analysis_id`-first host doctrine
   - Stage 13 Host Contract v1’s upstream canonical identity model
   - the March 27 Phase 0 closeout evidence that used both ids
4. Is it correct to treat `taskLaunchRuntime` as something that should likely be absorbed into Host Contract v2, or is that a category mistake?
5. Are the memo’s claims about the current live split between:
   - typed host contract
   - shared runtime
   - task launch runtime
   - page-local launch/navigation logic
   actually true in code?
6. Does the memo keep the right boundaries, or is it silently drifting into:
   - Phase 1A implementation
   - lifecycle
   - second-consumer proof
   - more AOI-local product work
7. What important recent memo, report, or code seam is missing from the scope if any?

## Output requirements

Write your review to exactly this file:

- `communications/REPORT_Claude_Phase1B_Host_Ownership_And_Contract_Unification_Scope_Critique_2026-03-27.md`

Your report should include:

1. A clear verdict:
   - `Approve`
   - `Approve after revision`
   - `Reject`
2. Findings ordered by severity, with concrete file references where possible.
3. A direct assessment of whether this memo is the right next move in light of the broader roadmap.
4. A direct assessment of whether the memo’s assumptions are robust enough to hand to a future implementation session.
5. Any revision instructions needed to make the memo decision-complete.

Do not edit the scope memo itself.
Do not make code changes.
Your job is critique, validation, and strategic pressure-testing.
