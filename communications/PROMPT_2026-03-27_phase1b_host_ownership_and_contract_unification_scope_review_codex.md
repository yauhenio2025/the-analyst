# Prompt For Codex: Audit The Phase 1B Host Ownership / Contract Unification Scope Memo

Audit a newly drafted Phase 1B scope memo in the `analyzer-v2` workspace.

## Primary artifact to audit

- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_scope.md`

## Audit objective

Determine whether this memo is the correct bounded next step after Phase 0 closure and whether its claims are actually supported by the current codebase and recent planning documents.

## Required work

Before writing your report, do all of the following:

1. Read the Phase 1B memo carefully.
2. Check it against the active strategic docs:
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`
3. Search `communications/` and `docs/` for any additional recent memos or reports that materially bear on:
   - host contract
   - planner-to-presentation bridge
   - task routing / task planning
   - source identity
   - continuity alias / warm snapshot
   - surface selection
   - launch handoff semantics
4. Audit the memo’s concrete claims against the live code, especially:
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

## Questions to answer explicitly

1. Is the memo correct that the current contract story is split across:
   - Host Contract v1 / hostContractRuntime
   - `taskLaunchRuntime`
   - page-local launch and navigation code
   - host proxy identity resolution?
2. Does the memo correctly identify the four ownership decisions that Phase 1B must settle?
3. Is the memo’s treatment of canonical identity versus host continuity alias technically coherent?
4. Is the proposed relation between `taskLaunchRuntime` and Host Contract v2 sound, or does it blur distinct layers incorrectly?
5. Is anything in the memo contradicted by the code?
6. Is anything important missing that would make the Phase 1B decision under-specified?
7. Is this scope narrow enough to be executable as a decision slice, rather than turning back into a broad roadmap?

## Output requirements

Write your audit to exactly this file:

- `communications/REPORT_Codex_Phase1B_Host_Ownership_And_Contract_Unification_Scope_Audit_2026-03-27.md`

The audit should include:

1. A verdict:
   - `Approve`
   - `Approve with revisions`
   - `Reject`
2. Findings ordered by severity.
3. Concrete code-path verification or contradiction for the memo’s main claims.
4. A judgment on whether this is the right next step in the larger program sequence.
5. Any required revisions to make the memo solid enough for future implementation planning.

Do not edit the memo.
Do not make code changes.
This is a documentation/code-path audit only.
