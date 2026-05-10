# Memo: Phase E AOI V2 Capture Status/Provenance Surfacing V1 Completion

Subtitle: One bounded Critic read-side seam now surfaces passive per-card capture truth back onto AOI `aoi_by_sin_type` after reload using persisted entity/workflow provenance

Date: 2026-04-03
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Prior Code Completion:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_scope.md`
Review Context:
- `communications/REPORT_Codex_Phase_E_AOI_V2_Capture_Status_Provenance_Surfacing_V1_Scope_Audit_2026-04-03.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Record what actually landed in the bounded Critic-side read-back slice after the AOI V2 `aoi_by_sin_type` capture-selection proof and the write-side provenance-persistence closeout.

This memo is about passive read-side surfacing of already-persisted capture truth on one bounded AOI page line.
It is not a claim that:

- generic capture-status law is now solved
- mixed-surface AOI consumers are now solved
- destination deep-linking or repeat-capture policy are now solved
- the genealogy `/api/captures/by-job/{job_id}` seam is now generalized
- analyzer-v2 needed to change again for this slice

## What Landed

One bounded Critic read-side slice is now complete on the same AOI `aoi_by_sin_type` proof line.

The landed behavior is:

1. Critic now has a new project-scoped analysis-compatible read seam:
   - `POST /api/captures/status/by-entity`
2. that route now looks up persisted capture rows by:
   - `source_workflow_key`
   - `source_view_key`
   - `entity_id[]`
   - existing project scope
3. the route excludes rows with null provenance fields and leaves the genealogy `/api/captures/by-job/{job_id}` seam untouched
4. Critic now has one bounded local host hook:
   - `useAnalysisCaptureStatusByEntity`
5. the bounded `AoiSinFindingsRenderer` now uses that hook to surface passive per-card truth on matching findings:
   - `In Arsenal`
   - `Research Answered`
   - `Research To-Do`
6. pill precedence is now explicit and non-contradictory:
   - `Research Answered` suppresses `Research To-Do`
   - `In Arsenal` may coexist with research state
7. the existing capture button behavior remains unchanged
8. a fresh load or revisit of the AOI V2 `aoi_by_sin_type` surface can now show persisted card-level truth without host-local analytical reconstruction

## The Final Boundary

The honest completed claim is:

- the bounded AOI `aoi_by_sin_type` line is now closed on selection creation, write-side persistence, and passive read-side truth surfacing
- the host can now read back persisted capture truth onto the same pure findings surface after reload or revisit using stored `entity_id` and `source_workflow_key`

What this does not mean:

- generic capture-status law now exists across analysis surfaces
- `aoi_by_theme` mixed-surface consumer behavior is now proven
- deep-linking, capture blocking, or repeat-capture policy are now solved
- duplicate-capture semantics are now solved
- the current renderer package generically consumes capture truth
- non-AOI proof value has now been established

## Implementation Shape

The implementation stayed inside Critic.
No analyzer-v2 runtime code changed.

The landed shape is:

- one new project-scoped backend route keyed by persisted analysis truth rather than `genealogy_job_id`
- one new local hook that normalizes entity ids and maps raw rows by `entity_id`
- one bounded local renderer read path inside `AoiSinFindingsRenderer`
- passive pills only; no new destination actions or routing semantics
- explicit older-row honesty:
  - rows with null `entity_id`
  - rows with null `source_workflow_key`
  simply do not match

One closeout correction matters for honesty:

- the first implementation left one medium-severity hook stability gap
- equivalent rebuilt `entity_ids` arrays could re-trigger the same lookup on rerender because the request inputs did not stabilize across render cycles
- the final closeout fixed that by deriving a stable normalized request key in `useAnalysisCaptureStatusByEntity`, so equivalent `entity_ids` sets do not refetch the same payload on every successful rerender

So the final landed claim is stronger than the first pass:

- the bounded read-back seam is now both truthful and render-stable

## Verification

Focused backend verification passed:

- `pytest -q tests/test_capture_status_by_entity.py tests/test_capture_provenance.py`
  - `10 passed`

Focused host verification passed:

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/hooks/useAnalysisCaptureStatusByEntity.test.tsx src/components/renderers/AoiSinFindingsRenderer.test.tsx src/components/V2TabContent.test.tsx src/components/ResearchFlagDialog.test.tsx src/components/renderers/index.test.tsx`
  - `23 passed`

Focused browser verification also passed:

- `npx playwright test tests/aoi-v2-sin-capture.spec.ts --project=chromium`
  - `4 passed`

The browser proof stays at the intended boundary:

- passive card-level truth appears on the bounded AOI V2 `aoi_by_sin_type` surface
- the same truth survives `page.reload()`
- the existing capture-selection handoff behavior remains intact

Two honesty notes matter:

- Jest still prints the repo's existing post-run open-handle warning after the focused frontend batch passes
- the local `./start` flow still surfaces unrelated existing frontend compile errors and warnings outside this slice

## Calibrated Claim

Before this slice, the strongest honest host-side claim was:

- Critic could create and persist truthful bounded AOI capture provenance on `aoi_by_sin_type`

After this slice, the stronger honest claim is:

- Critic can now also read that persisted truth back onto the same bounded AOI V2 pure findings surface after reload or revisit

That is materially stronger because the contract is no longer only:

- consumable at click time
- durable at save time

It is now also:

- visible again on the next read path

The claim is still deliberately local:

- one pure findings surface
- one local renderer override
- one local read hook
- one local route

## Why This Matters

This slice closes the current bounded AOI `aoi_by_sin_type` loop end to end enough to justify moving on.

The progression is now:

1. analyzer-v2 emits bounded affordance and finding-handle truth
2. one live Critic V2 surface consumes that truth to create a correct `CaptureSelection`
3. the current Critic capture pipeline preserves that truth on the write side
4. the current Critic runtime can now read that truth back onto the same surface after reload

That is a real bounded loop.
But it is still a loop on one pure AOI findings surface only.

Reusable-substrate value is therefore stronger than it was before, but still modest:

- the proof is no longer write-only
- but it is still not yet a structurally different surface-family proof

## Next Honest Step

The next bounded Phase E question should stop deepening the same pure-surface AOI line and broaden the matrix honestly:

- can one live Critic V2 mixed surface consume the already-landed analyzer contract on nested findings without overclaiming whole-view semantics or generic renderer law?

The strongest current target is:

- AOI `aoi_by_theme`

Why this is the right next move:

- analyzer-v2 already carries nested `finding_id` on rebuilt `aoi_by_theme` findings
- whole-view `FirstHopAffordance` there intentionally remains generic-only
- the current bounded-V2 host path still does not operationalize those nested finding handles
- another `aoi_by_sin_type` refinement would now broaden the matrix less honestly than one mixed-surface consumer proof

So the next honest step is not:

- another same-surface `aoi_by_sin_type` refinement
- another analyzer-only semantic slice
- generic renderer-package capture law
- non-AOI proof before this mixed-surface AOI gap is answered

It is:

- one bounded AOI V2 mixed-surface nested-finding consumer proof on `aoi_by_theme`
- still host-side in Critic
- still passive-first
- still without new analyzer semantics or generic renderer-package rules
