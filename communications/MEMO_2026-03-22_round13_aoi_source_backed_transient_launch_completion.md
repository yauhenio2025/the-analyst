# Memo: Round 13 / AOI Source-Backed Transient Launch Completion

Date: 2026-03-22
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md`

## Result

Round 13 implementation is complete.

This memo closes the implementation and focused verification record for the round-13 source-backed bridge.

It does **not** claim final live documentary closure yet.
One operational proof step still remains outside this memo:

- rerun the source-backed dossier and comparison launches from a real saved AOI result in a live browser session
- save the resulting request / response / screenshot artifacts
- write the matching round-13 proof note

So the honest status is:

- code-complete
- focused tests complete
- live source-backed proof artifacts still pending

## Bounded Claim Landed In Code

Round 13 set out to prove one bounded thing:

- the-critic can launch the existing AOI transient compose shell from a real saved AOI v2 result for the current project + thinker, while keeping saved-result identity resolution in the-critic and source-result-to-compose mapping in analyzer-v2

That bounded architecture is now implemented.

## What Landed

### analyzer-v2

Round 13 added a source-backed transient route parallel to round 11:

- `POST /v1/presenter/compose-from-source`

The source-backed path now:

- accepts `workflow_key`, `consumer_key`, `source_v2_job_id`, `profile`, optional `user_intent`, and optional `style_school`
- reconstructs bounded compose sections inside analyzer-v2 rather than in the-critic
- uses deterministic profile mapping:
  - `dossier`
    - `aoi_thematic_synthesis`
    - `aoi_thematic_report`
  - `comparison`
    - `aoi_engagement_mapping`
    - `aoi_sin_findings`
    - `aoi_thematic_report`
- loads the thematic report from latest `aoi_thematic_report` phase-output metadata rather than pretending it is a Stage-1 artifact family
- applies code-owned default intents when `user_intent` is omitted
- reuses the round-11 transient compose orchestration internally
- stamps both response and trace with:
  - `compose-from-source-v1`

### the-critic backend

Round 13 added one narrow proxy seam on the-critic backend that now:

- resolves source identity for the current project + thinker
- supports bounded override handling:
  - `source_analysis_id`
  - `source_v2_job_id`
- proxies the source-backed request to analyzer-v2 with a long timeout
- preserves analyzer status classes on pass-through

The important doctrine is now real in code:

- the-critic resolves result identity
- analyzer-v2 resolves source content

### the-critic frontend

Round 13 changed the transient proof host from fixture-primary to source-backed-primary:

- source-backed dossier / comparison launch actions are now the main path
- thinker context comes from route query params
- fixtures remain only as secondary developer fallback
- the existing transient shell remains the render surface
- `ViewRenderer` still requires zero runtime changes

### Default-Resolution Hardening

One real backend bug surfaced in review after implementation:

- default source resolution could skip the newest matching saved AOI result if that row lacked `_v2_job_id`
- that could silently drift to an older saved result or fall through to `404`

That is now fixed.

The default path now treats the newest matching saved AOI result as authoritative even when it is broken, so the promised broken-saved-result `409` can surface honestly.

## Verification

### analyzer-v2

Focused analyzer verification completed:

- `PYTHONPATH=. pytest tests/test_compose_from_intent.py tests/test_presentation_api.py -q`
  - result: `76 passed`
- `PYTHONPATH=. pytest tests/test_compose_from_intent.py -q`
  - result: `17 passed`
- `python -m py_compile src/presenter/compose_from_intent.py src/presenter/schemas.py src/api/routes/presenter.py`
  - result: clean

### the-critic backend

Focused backend verification completed:

- `python -m py_compile /home/evgeny/projects/the-critic/api/server.py /home/evgeny/projects/the-critic/api/models_genealogy.py /home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_client.py`
  - result: clean
- `pytest /home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py -q -k "source_backed_identity_default_resolution_surfaces_missing_v2_job_id_on_newest_saved_result or get_analysis_result_detail_includes_aoi_thinker_identity"`
  - result: `2 passed`

### the-critic frontend

Focused frontend verification completed:

- `cd /home/evgeny/projects/the-critic/webapp && npx tsc --noEmit --pretty false --incremental false`
  - result: clean
- focused Jest slices for:
  - `composeFromIntentClient`
  - `AoiComposeFromIntentPage`
  - `ViewRenderer`
  - transient isolation guard
  - route wiring
  - result: all passed

## What Round 13 Now Proves

Round 13 now proves in code:

1. fixture-backed launch is no longer the primary transient path
2. analyzer-v2 can reconstruct bounded AOI compose sections from durable upstream AOI truth keyed by `v2_job_id`
3. the-critic can stay thin by resolving source identity and proxying rather than parsing saved presentation internals
4. source-backed transient launch now distinguishes:
   - source resolution failures
   - source material failures
   - final renderer-contract failures
5. the default saved-result path now fails honestly on a broken newest saved result instead of silently selecting an older one

## What Round 13 Did Not Yet Close

Round 13 did **not** yet close these operational proof items in this memo:

1. live browser dossier launch from a real saved AOI result
2. live browser comparison launch from a real saved AOI result
3. saved round-13 request / response / screenshot artifacts
4. a round-13 proof note that records those artifacts

Those are documentary closure tasks, not remaining architecture or code gaps.

## Program Position After Round 13

The transient path has now crossed a more important boundary:

- it no longer depends on checked-in example payloads as its main source of truth
- it now has a real bridge from saved AOI result identity to analyzer-owned source reconstruction

That means the next program question is no longer:

- can source-backed transient launch be made real?

It is now closer to:

- how should this transient experience be adopted from the real AOI user path without collapsing transient and job-backed lifecycle law into one thing too early?
