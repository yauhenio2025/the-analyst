# Memo: Stage 5 AOI Identity Continuity Revision Scope

Date: 2026-03-25

## Summary

The Stage 5 diagnostic spot-check no longer fails in AOI selector/provider planning.

It now fails later, on the real planner-backed compose path, because the host-side AOI source identity continuity seam is incomplete across:

- durable `v2_run_references` AOI thinker identity truth
- snapshot warmup
- local persisted snapshot identity
- planner-backed page handoff of canonical source identity
- planner-backed compose proxy validation

This memo scopes the next bounded fix slice around that exact seam.

## Why This Is The Right Immediate Step

The diagnostic evidence now shows:

- `route-task` succeeds
- `plan-task` succeeds
- the repaired selector trace is healthy
- browser navigation reaches planner-backed compose
- the compose proxy returns `409 source_analysis_id does not belong to the current project + thinker context`

That means:

- the frozen rerun was not earned
- the next move is not another generic AOI planning change
- the next move is not Tranche 3
- the next move is one bounded Stage 5 continuity repair

It also means this slice should stay epistemically narrow:

- it only needs to remove the current continuity blocker honestly
- it does **not** imply that Stage 5 is otherwise close to passing
- after continuity is fixed, the frozen rerun may still surface later `selection_fit`, usefulness, or render-path issues

## Decision 1: Keep The Stage 5 Gate Frozen

Do not change:

- the four-case pack
- the rubric
- the pass/fail thresholds
- the Stage 2 closure bar

The same `evolution_ready` diagnostic case must be used again after this slice lands.

## Decision 2: Scope The Problem As Host Identity Continuity

The bounded fix surface is:

- whether the local `v2_run_references` row for the proof source already exists and whether its AOI thinker identity fields are null
- how `the-critic` warms a local AOI snapshot from a durable analyzer-v2 result
- how that warmed snapshot persists AOI thinker/source identity
- how the planner-backed panel-to-compose handoff preserves canonical `source_v2_job_id`
- how planner-backed compose resolves and validates source identity

The fix should be strong enough that the same planner-backed AOI source can survive:

- saved result selection
- durable run-ref lookup / truth
- snapshot warmup
- compose page handoff
- compose proxy validation

Without:

- requiring legacy/debug fallback
- changing the Stage 5 case set
- widening AOI planner contracts again

The fix should be treated as data-plumbing / continuity work, not an architectural redesign.

Implementation note:

- the first diagnostic fork for the implementor should be the local `v2_run_references` row for source job `proof-round5-adaptive-aoi-dossier-final-1774100000`
- if that row is missing AOI thinker identity, warmup may already be behaving correctly relative to bad durable truth
- the slice should therefore repair the first broken durable hop before assuming warmup itself is the root cause

## Decision 3: Preserve The Planner/Selector Boundary

This slice should not reopen AOI selector/provider work unless new evidence forces it.

The current diagnostic already showed:

- `aoi_composition_handoff_plan`
- `timeout_s = 45`
- `max_retries = 0`
- `provider_outcome = success`

So planner/selector repair should be treated as landed baseline, not reopened scope.

## Decision 4: Preserve The Environment Baseline Explicitly

Use the same local environment that produced the authoritative diagnostic:

- local `analyzer-v2` on `:8002`
- local `the-critic` API/webapp
- `ANALYZER_V2_URL=http://127.0.0.1:8002` for the Critic backend

Environment changes must continue to be recorded in any follow-up diagnostic artifacts.

## Decision 5: Add Direct Regression Coverage For This Exact Seam

This slice should add focused regression coverage for the continuity failure that was just observed.

Minimum expected coverage:

- backend ownership should live primarily in `the-critic/tests/test_aoi_v2_routes.py`
- a host/backend test proving durable `v2_run_references` AOI thinker identity is preserved or backfilled for the planner-backed proof source
- a host/backend test proving snapshot warmup projects that AOI thinker identity onto the local warmed snapshot for a planner-backed AOI source
- a host/backend test proving planner-backed `compose-from-selection` accepts a warmed local snapshot when the persisted AOI thinker identity matches the current project + thinker context
- a frontend ownership point should live in `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`
- a frontend test proving planner-backed navigation preserves canonical `source_v2_job_id` into `/compose-from-intent` rather than dropping it at handoff
- a backend or integration test proving repeated warmup / latest-snapshot behavior still preserves thinker identity and does not regress into the same `409` seam
- if the final implementation preserves truth in both `genealogy_analyses.pass_results` and `v2_run_references`, at least one test should make that continuity explicit instead of only asserting the final HTTP status

The goal is to prevent this exact stop condition from silently reappearing after the next rerun attempt.

## Intended Outcomes

This slice should aim to make the following true on the next `evolution_ready` spot-check:

- planning succeeds
- planner-backed continue path succeeds
- compose proxy no longer fails on AOI source identity validation
- the ready case reaches honest planner-backed compose/render without legacy fallback

If that happens, the same frozen four-case Stage 5 rerun becomes meaningful again.

## Acceptance Evidence

Minimum required evidence after this slice:

- one new `evolution_ready` diagnostic HAR
- one new diagnostic request/response JSON artifact
- one new diagnostic screenshot
- one updated diagnosis note stating whether the continuity fix resolved the stop condition
- focused regression coverage showing the identity continuity seam is now preserved in code, not just in one live run

Only after that should the frozen four-case rerun be attempted again.

## Out Of Scope

- rubric changes
- case changes
- Stage 2 closure language changes
- Tranche 3 work
- lifecycle work
- new AOI planner architecture

## Completion Condition

This scope is complete only when one of these is true:

1. the repaired continuity path passes the same `evolution_ready` diagnostic and the frozen rerun is honestly re-attempted
2. the continuity slice still fails, and a narrower follow-up memo is written from fresh evidence instead of consuming the rerun dishonestly
