# Report: Stage 5 AOI Exemplar Diagnostic And Rerun Scope Audit

Date: 2026-03-25
Auditor: Codex
Verdict: **Approve with revisions**

## Findings

### 1. Medium: The memo is right about sequencing, but the diagnostic artifact spec is still slightly too loose for the selector hardening it wants to verify

- The revision slice added the exact selector-trace facts the diagnosis needs: `timeout_s`, `retry_policy`, `exception_class_name`, `provider_outcome`, and blocked reason fields in `src/orchestrator/task_planner.py:1094-1132`.
- The selector call now uses env-configurable timeout and `max_retries=0`, with explicit timeout/provider classification in `src/orchestrator/task_planner.py:40-41` and `src/orchestrator/task_planner.py:727-804`. Targeted tests assert those behaviors in `tests/test_task_planner.py:565-639`.
- But the memo only requires a saved `plan-task` JSON excerpt plus a short diagnosis note in `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:100-118`. If that excerpt is abbreviated the wrong way, later audit can lose the very fields that distinguish timeout budget, retry policy, and provider failure.

This is a memo-quality gap, not a sequencing gap. The next step is still the diagnostic spot-check, but the memo should explicitly require the saved `plan-task` artifact or diagnosis note to preserve the source-selection trace details containing:

- `timeout_s`
- `retry_policy.max_retries`
- `exception_class_name`
- `provider_outcome`
- `blocked_reason_code`
- `blocked_reason_detail`

### 2. Medium: The stop rule is conceptually honest, but it should name compose-path failures explicitly rather than leaving them implicit

- The memo correctly says to stop and write a new revision memo if the spot-check exposes a new code/product-path failure that the revision slice did not close in `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:122-128`.
- That matters because the repaired host now genuinely reaches a planner-backed continuation path: the panel retains `plannerDecision`, shows blocked and ready planner state, and launches the planner-backed compose page via navigation state in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:179-180`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:256-264`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:610-623`, and `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:665-680`.
- The compose page then calls `composeFromSelection(...)` through the explicit planner-backed path in `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:238-258` and `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:414-443`.
- Stage 5 `rendered_usefulness` still requires that this compose step succeeds, not merely that planning succeeds, per the frozen rubric in `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md:77-92`.

So the memo should say explicitly that:

- spot-check reaches `aoi_composition_handoff_plan` but planner-backed `compose-from-selection` fails
- or planner-backed flow reaches the compose page but only legacy/debug profile controls make progress

also counts as a stop-and-revise condition, not as a green light for the full rerun.

### 3. Medium: The memo is honest that Stage 5 may pass while Stage 2 stays open, but the rerun deliverables should force that evidence to stay machine-auditable

- The memo correctly keeps the fixed pack and Stage 2 bar intact in `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:65-78` and `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:139-153`.
- The frozen rubric still requires at least one `execution_backed` ready case for Stage 2 closure in `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md:128-132`.
- The previous proof summary recorded per-case `fixture_strength` explicitly in `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json:6-8` and `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json:194-197`.

But the new memo's full-rerun deliverables at `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:166-185` do not explicitly say the rerun summary must preserve:

- per-case fixture-strength labels
- whether any case was intentionally upgraded to `execution_backed`
- exact environment changes, if any, between spot-check attempts and rerun

Without that, a later reader can still blur:

- Stage 5 pass vs Stage 2 open
- code fix vs environment-only fix
- frozen fixture-backed rerun vs mixed-strength rerun

### 4. Low: No stronger Tranche 3 blocker surfaced; the remaining Tranche 3 pressure is real but already known and correctly fenced off from this immediate step

- The draft and master roadmaps both say Tranche 3 stays blocked until the repaired Stage 5 path gets its diagnostic spot-check and rerun in `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:181-185` and `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1167-1170`.
- The current code still has known Tranche 3 locks: `compose-from-selection` only supports AOI plus `the-critic` in `src/presenter/compose_from_intent.py:547-555`, and the compose page still carries planner state through `location.state` while exposing legacy/debug profile buttons in `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:238-258` and `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:640-659`.
- But those are already the named reasons for later de-AOI / de-`the-critic` substrate work in `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:226-250`, not newly surfaced blockers for the current Stage 5 proof step.

This is not a reason to pivot phases now. It is a reason to keep the rerun honest and keep Tranche 3 behind it.

### 5. Low: The codebase evidence supports treating this as an operational proof step rather than another immediate coding slice

- `analyzer-v2` really did land the bounded selector hardening: env timeout default `45.0`, no retries, explicit timeout/provider mapping, and richer trace details in `src/orchestrator/task_planner.py:40-41`, `src/orchestrator/task_planner.py:727-804`, and `src/orchestrator/task_planner.py:1094-1132`.
- The test pack directly covers those behaviors in `tests/test_task_planner.py:565-639`.
- `the-critic` really did land structured planner-outcome retention: `plannerDecision` is separate from `pageError`, blocked banner renders from structured planner state, auto-load refresh keeps planner outcome by default, and clear points are limited to new planning, explicit dismiss, source switch, and active-job reset in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:179-180`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:283-287`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:388-490`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:540-624`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:803-818`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:944-946`, `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:1063-1133`, and `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:1395`.
- The frontend tests now cover refresh churn, task-text edits, delayed initial auto-load race, and ready-handoff survival in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx:642-864`.

That is enough evidence that the immediate uncertainty is live behavior on the repaired path, not a missing implementation slice.

## Direct Answers

### 1. Is the memo correctly keeping roadmap order intact rather than pivoting phases?

Yes.

The current program record still treats the Stage 5 diagnostic plus rerun as the blocker before Tranche 3 becomes the main line in:

- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:181-185`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md:219-224`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1167-1170`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1255-1264`

### 2. Is the memo correctly narrowing the next move to one diagnostic `evolution_ready` spot-check and then the same frozen rerun and nothing broader?

Yes.

That is now the right scope boundary. The revision slice is in code, and the frozen rubric and pack remain the right gate in:

- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:20-35`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:90-128`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md:11-17`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md:118-134`

The only revisions needed are tighter artifact and stop-rule wording, not broader scope.

### 3. Does the codebase evidence support treating this as an operational proof step rather than another immediate coding slice?

Yes.

The bounded repair slice described in `communications/MEMO_2026-03-25_stage5_aoi_exemplar_revision_slice_completion.md:28-94` is visible in the live code and tests cited in Finding 5. The remaining uncertainty is runtime proof behavior on the repaired path.

### 4. Is the branch rule honest enough about when to stop and write a new revision memo instead of forcing a full rerun?

Mostly yes.

`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:122-128` already contains the right principle. It should be revised only to make two stop cases explicit:

- planner handoff succeeds but planner-backed `compose-from-selection` fails
- an "environment-only" fix is applied without recording exactly what changed

### 5. Is the memo explicit enough about likely Stage 5 pass / Stage 2 still-open outcomes?

Yes in prose, not quite enough in artifact discipline.

`communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:139-153` is the correct substantive stance. The remaining gap is that the rerun summary should explicitly preserve per-case `fixture_strength` and any `execution_backed` upgrade so later readers cannot silently collapse Stage 5 pass into Stage 2 closure.

### 6. Is there any hidden dependency that makes Tranche 3 pressure stronger than the memo admits?

No stronger phase-pivot dependency surfaced.

The remaining Tranche 3 dependencies are real but already known:

- `compose-from-selection` is still AOI-only and `the-critic`-only in `src/presenter/compose_from_intent.py:547-555`
- the compose page still depends on planner state handoff plus legacy/debug residual controls in `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:238-258` and `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:640-659`

Those are reasons not to overclaim after the rerun. They are not reasons to reverse tranche order before the rerun.

### 7. Are the required artifacts and deliverables concrete enough for later audit?

Mostly, but not fully.

The file names and artifact categories are concrete in `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md:155-185`. The remaining auditability gaps are:

- require the `plan-task` trace details that prove timeout/retry/classification behavior
- require exact environment-change logging between attempts
- require per-case fixture-strength recording in the rerun summary

## Program Recommendation

- Update the roadmap slightly: yes, but only as a clarification that a Stage 5 rerun pass still does not close Stage 2 unless an `execution_backed` ready case is intentionally nominated and recorded.
- Recalibrate the immediate plan: yes, tighten the artifact and stop-rule wording, then do exactly one diagnostic `evolution_ready` spot-check and, if earned, the same frozen rerun.
- Do not pivot phases: yes.

## Concrete Revisions Before Implementation

1. Revise the diagnostic artifact requirement so the saved `plan-task` response excerpt or diagnosis note must preserve:
   - `timeout_s`
   - `retry_policy.max_retries`
   - `exception_class_name`
   - `provider_outcome`
   - `blocked_reason_code`
   - `blocked_reason_detail`

2. Revise the branch rule to say explicitly that:
   - successful planning followed by planner-backed `compose-from-selection` failure
   - or any fallback that relies on legacy/debug profile controls

   is a stop-and-revise outcome, not a rerun-green-light outcome.

3. Revise the artifact policy so any environment-only fix between spot-check attempts is recorded explicitly:
   - what changed
   - when it changed
   - whether any code changed as well

4. Revise the rerun summary / closeout requirements so they record per case:
   - `fixture_strength`
   - whether any case was upgraded to `execution_backed`
   - separate Stage 5 and Stage 2 decisions

## Bottom Line

The memo has the right immediate sequencing and the right broader-program stance.

The codebase and recent record support exactly what it proposes:

- do the live diagnostic first
- rerun the same frozen gate if the spot-check earns it
- keep Tranche 3 blocked
- allow Stage 5 pass while Stage 2 stays open if the evidence remains fixture-backed

That is the right next move. The revisions above are about proof quality and audit honesty, not about changing the plan.
