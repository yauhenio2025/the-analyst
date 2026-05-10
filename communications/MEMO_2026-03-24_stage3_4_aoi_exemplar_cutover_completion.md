# Memo: Stage 3/4 AOI Exemplar Cutover Completion

Date: 2026-03-24
Scope Memo: `communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md`
Program: Dynamic Bespoke Apps Platformization

## Summary

Milestone A of the broader AOI exemplar tranche is now implemented.

What landed is the Stage 3/4 cutover:

- one planner-primary AOI proof path in `the-critic`
- bounded LLM-first AOI source/product selection inside `plan-task`
- a new selection-backed compose contract instead of stretching `dossier | comparison`
- explicit fail-closed AOI blocked outcomes
- a widened host contract/runtime path that can launch source-backed transient compose by `profile` or by explicit `selection`

This materially advances canonical Stage 3 and Stage 4.

It does **not** close the broader Stage 2/3/4/5 tranche.

Still open after this memo:

- Stage 5 AOI evaluation/ops gate
- Stage 2 documentary closure
- planner-backed refresh/deep-link continuity
- remaining host continuity residuals on the proof path

So the next immediate step is not another architecture tranche.
It is the Stage 5 AOI exemplar exit gate.

## What Landed

### In `analyzer-v2`

- `src/orchestrator/task_router.py`
  - AOI routing now points to a planner handoff seam rather than telling the host to choose a profile and call `compose-from-source`
- `src/orchestrator/task_planning_schemas.py`
  - AOI planning outcomes now explicitly include:
    - `aoi_composition_handoff_plan`
    - `aoi_selection_blocked`
- `src/orchestrator/task_planner.py`
  - AOI planning now:
    - resolves the AOI source catalog deterministically
    - runs one bounded LLM selector over the resolved catalog
    - emits explicit `selected_sources`, `rejected_sources`, `selection_summary`, `resolved_intent_seed`, and `legacy_profile_equivalent`
    - fails closed with explicit blocked reason codes when selection cannot be used safely
- `src/presenter/schemas.py`
  - a new `compose-from-selection` request/response shape exists
  - AOI selection inputs are validated more strictly than the old profile-only path
- `src/presenter/composition_source_bridge.py`
  - selection-backed materialization now bypasses `_PROFILE_SELECTION_PRESETS`
  - the bridge consumes explicit source-family selection order instead of needing a synthetic profile
- `src/presenter/compose_from_intent.py`
  - `compose-from-selection` now uses required `user_intent`
  - planner-authored `selection_summary` and `legacy_profile_equivalent` are preserved into compose traces
- `src/api/routes/presenter.py`
  - `POST /v1/presenter/compose-from-selection` is now a real public presenter route

### In `the-critic`

- `webapp/src/lib/hostContractV1.ts`
  - `source_backed_transient_launch` is now a discriminated union:
    - `variant: "profile"`
    - `variant: "selection"`
- `webapp/src/lib/hostContractRuntime.ts`
  - runtime validation and dispatch now support the selection-backed transient launch variant
- `webapp/src/lib/taskLaunchRuntime.ts`
  - richer AOI planner handoff payloads are now typed and consumed by the host
- `webapp/src/lib/composeFromIntentClient.ts`
  - selection-backed AOI compose is now a real client path
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx`
  - planner-backed AOI is now the primary proof control
  - the panel shows:
    - planner summary
    - selected sources
    - rejected sources
    - required host preparation
  - legacy profile controls remain only in collapsed `Legacy / Debug`
- `webapp/src/pages/AoiComposeFromIntentPage.tsx`
  - planner-backed mode now:
    - consumes navigation-state planner payload
    - pre-fills the planner-generated intent seed
    - launches via `compose-from-selection`
    - hides dossier/comparison choice on the proof path
- `api/server.py`
  - the host proxy now supports `compose-from-selection`
  - planner summary and legacy-profile-equivalent audit metadata are forwarded to analyzer-v2
- `analyzer/concept_analyzer/analyzer_v2_client.py`
  - the critic’s analyzer client now supports the widened AOI selection-backed path

## Behavioral Outcome

The AOI proof path is now materially different from the earlier bounded handoff slice.

Before:

- planner-backed AOI still resolved into profile-shaped host choice
- the host still re-exposed dossier/comparison as the main downstream decision
- the public source-backed compose seam was still fundamentally profile-first

Now:

- `route-task` stays generic
- `plan-task` owns AOI selection
- planner-backed AOI produces explicit selected and rejected source-family law
- the host shows that law to the user
- the user confirms once
- the downstream proof path launches through `compose-from-selection`

The planner-primary path also now skips `source_backed_readiness`.

That gate remains intact only for legacy/debug profile paths.
On the proof path, `plan-task` is the authoritative readiness-and-selection gate.

This keeps the bounded claim honest:

- the host is no longer the real profile chooser on the proof path
- but the tranche is still not claiming full lifecycle or host-neutral transient closure

## Fail-Closed Selection Behavior

AOI blocked outcomes are now explicit, additive, and auditable.

The planner can return:

- `unsupported`
- `insufficient_context`
- `aoi_selection_blocked`
- `aoi_composition_handoff_plan`

`aoi_selection_blocked` is distinct from routing to the wrong workflow.

Current blocked reason codes:

- `no_usable_source_families`
- `llm_timeout`
- `llm_provider_failure`
- `llm_invalid_output`
- `llm_selection_failed_validation`

The planner also now records selection provenance strongly enough for later Stage 5 review:

- prompt version
- model
- timeout
- provider outcome
- validator version

That provenance is saved on blocked outcomes as well as ready outcomes.

## Post-Review Hardening

After the first implementation pass, one review identified two real gaps:

1. blocked AOI planning outcomes did not yet retain selector provenance strongly enough for eval/audit use
2. selection validation still allowed incomplete or low-quality `rejected_sources` output

Those gaps are now closed.

What changed:

- blocked AOI decisions now append a `source_selection` trace entry even when selection fails
- blocked traces now preserve:
  - prompt version
  - model
  - timeout
  - provider outcome
  - validator version
  - blocked reason metadata
- AOI selection validation now requires:
  - non-blank selected-source rationale
  - non-blank rejected-source reason
  - rejected-source coverage for every unselected available family
  - no rejected families outside the resolved available catalog
  - no duplicate rejected families
- compose traces now preserve planner-authored:
  - `selection_summary`
  - `legacy_profile_equivalent`

So the Milestone A seam is now stronger than the first implementation pass and is better prepared for the Stage 5 eval gate.

## Verification

Analyzer-focused verification:

- `PYTHONPATH=. pytest -q tests/test_task_router.py tests/test_task_planner.py tests/test_composition_source_bridge.py tests/test_compose_from_intent.py`

Result:

- `53 passed`

Current-consumer verification:

- `/home/evgeny/projects/the-critic/webapp/node_modules/.bin/tsc -p /home/evgeny/projects/the-critic/webapp/tsconfig.json --noEmit`
- `CI=true npm --prefix /home/evgeny/projects/the-critic/webapp test -- --runInBand --watchAll=false src/lib/taskLaunchRuntime.test.ts src/lib/composeFromIntentClient.test.ts src/lib/hostContractRuntime.test.ts src/lib/hostContractV1.test.ts src/pages/AoiComposeFromIntentPage.test.tsx src/components/influence/AoiV2ThematicPanel.test.tsx`
- `PYTHONPATH=. pytest -q tests/test_aoi_v2_client.py tests/test_aoi_v2_routes.py`

Result:

- frontend focused pack: `67 passed`
- backend focused pack: `42 passed`

Known warnings still present but non-failing:

- existing React `act(...)` warnings in AOI panel tests
- existing FastAPI deprecation warnings
- existing SQLAlchemy relationship warnings

## Boundaries

This memo is an implementation completion memo for Milestone A.
It is not the final closeout for the broader AOI exemplar tranche.

What remains out of scope here:

- the Stage 5 AOI evaluation/ops pack
- documentary closure of Stage 2
- removal of host-proxy identity translation from the proof path
- removal of snapshot warmup from the proof path
- planner-backed refresh/deep-link continuity
- de-AOI / de-`the-critic` transient generalization
- lifecycle reopening

The planner-backed proof path still carries these explicit continuity residuals:

- host-proxy identity translation
- snapshot warmup

Those were allowed by scope and remain honest residuals rather than hidden analytical law.

## Status

The honest ledger after Milestone A is:

- Stage 2: still `In progress`
- Stage 3: `Partial`, materially stronger
- Stage 4: `Partial`, materially stronger
- Stage 5: still open and now the immediate next gate
- Stage 13: still `Partial`

So the main structural next step is:

- Stage 5 AOI exemplar exit gate

That next step is where the program should decide:

- whether the AOI exemplar is stable enough to stand as a real platform reference
- whether Stage 2 can now be documentary-closed as a side-effect
- what remains open before any broader transient-substrate generalization
