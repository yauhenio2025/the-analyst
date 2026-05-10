# Memo: Phase E AOI V2 Capture Provenance Persistence V1 Completion

Subtitle: One bounded Critic capture slice now preserves analyzer item identity and truthful workflow provenance through both live AOI `aoi_by_sin_type` capture paths

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
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_scope.md`
Review Context:
- `communications/REPORT_Codex_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Audit_2026-04-03.md`
- `communications/REPORT_Claude_Phase_E_AOI_V2_Capture_Provenance_Persistence_V1_Scope_Critique_2026-04-03.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Record what actually landed in the bounded Critic-side provenance-persistence slice after the AOI V2 `aoi_by_sin_type` capture-selection consumer proof.

This memo is about persisted provenance truth on the current capture line.
It is not a claim that:

- routed workflow semantics are now workflow-neutral
- Arsenal stream naming is no longer genealogy-shaped
- exact source-run identity is now preserved
- generic capture-status surfacing is now solved
- analyzer-v2 needed to change again for this slice

## What Landed

One bounded Critic host/backend slice is now complete on the same AOI `aoi_by_sin_type` proof line.

The landed behavior is:

1. the bounded AOI renderer path now emits both:
   - `entity_id`
   - `source_workflow_key`
2. `CaptureContext.submitCapture(...)` now forwards those fields to `POST /api/captures` while preserving the existing genealogy `entity_id -> genealogy_job_id` fallback
3. direct AOI research-question save in `ResearchFlagDialog` now also forwards the same provenance on:
   - direct `POST /api/captures`
   - direct `POST /api/research-todos`
4. capture records now persist:
   - `entity_id`
   - `source_workflow_key`
5. routed downstream `source_snapshot` truth now uses persisted provenance rather than hard-coded genealogy workflow assumptions:
   - `workflow_key`
   - `source_workflow_key`
   - `entity_id`
6. the direct `POST /api/research-todos` path now normalizes those same three provenance fields from the linked persisted capture when `capture_id` is present
7. `ResearchFlagDialog` no longer issues the follow-up `/captures/{id}/to-research-todo` call, so the direct research path no longer risks creating a duplicate todo
8. an Alembic migration now adds nullable persisted columns for:
   - `entity_id`
   - `source_workflow_key`

## The Final Boundary

The honest completed claim is:

- the current Critic capture pipeline can now preserve analyzer item identity and truthful workflow-type provenance on the bounded AOI `aoi_by_sin_type` line
- that truth now survives through:
  - capture creation
  - capture persistence
  - capture response truth
  - routed Arsenal source snapshots
  - routed research-todo source snapshots
  - direct research-todo creation when a linked capture exists

What this does not mean:

- `workflow_key` naming across the broader product is now cleaned up
- capture routing semantics are now workflow-neutral
- exact source-run identity is now preserved
- generic read-side capture status for analysis surfaces is now solved
- current mixed-surface AOI V2 consumers are now proven
- end-to-end Arsenal product behavior is now fully proven

## Implementation Shape

The implementation stayed inside Critic.
No analyzer-v2 runtime code changed.

The landed shape is:

- host selection creation on `aoi_by_sin_type` now includes `source_workflow_key` alongside `entity_id`
- `CaptureContext` persists both fields while preserving the current genealogy fallback
- `ResearchFlagDialog` now treats direct `POST /api/research-todos` as the authoritative research-question save path
- the follow-up `capture_to_research_todo(...)` call was removed from that dialog path to avoid duplicate todo creation
- `GenealogyCaptureDB`, `CaptureCreateRequest`, and `CaptureResponse` were widened additively
- routed downstream snapshot building in `capture_to_arsenal(...)` and `capture_to_research_todo(...)` now uses persisted capture provenance
- direct `create_research_todo(...)` now rewrites client-supplied provenance fields from the linked capture record when `capture_id` is present

One closeout correction matters for honesty:

- the first implementation left one high-severity gap on the direct `POST /api/research-todos` path
- when `capture_id` was present, the server still trusted mismatched client-supplied provenance fields in `source_snapshot`
- the final closeout fixed that by normalizing:
  - `workflow_key`
  - `source_workflow_key`
  - `entity_id`
  from the persisted linked capture before saving the todo

So the final landed claim is stronger than the first pass:

- both live AOI capture/save paths now preserve persisted provenance truth

## Verification

Focused host verification passed on the bounded AOI V2 line:

- `CI=1 npm test -- --runInBand --runTestsByPath src/components/renderers/AoiSinFindingsRenderer.test.tsx src/components/V2TabContent.test.tsx src/contexts/CaptureContext.test.tsx src/components/ResearchFlagDialog.test.tsx src/components/renderers/index.test.tsx`
  - `20 passed`
- `CI=1 npm test -- --runInBand --runTestsByPath src/components/influence/AoiV2ThematicPanel.test.tsx src/components/V2TabContent.test.tsx src/components/renderers/AoiSinFindingsRenderer.test.tsx src/contexts/CaptureContext.test.tsx src/components/ResearchFlagDialog.test.tsx`
  - `39 passed`

Focused backend verification passed:

- `pytest -q tests/test_capture_provenance.py`
  - `6 passed`
- `pytest -q tests/test_aoi_v2_routes.py tests/test_capture_provenance.py`
  - `57 passed`

Focused browser verification also passed:

- `npx playwright test tests/aoi-v2-sin-capture.spec.ts --project=chromium`
  - `3 passed`

The browser proof stays at the intended boundary:

- request truth on the capture path
- request truth on the direct research-question save path
- no follow-up `/captures/{id}/to-research-todo` request after direct save

Two honesty notes matter:

- the migration was verified by code and test inspection, but not by applying an Alembic upgrade against a live database in this closeout
- broader frontend batches still carry pre-existing open-handle and `act(...)` warnings unrelated to this provenance slice

## Calibrated Claim

Before this slice, the strongest honest host-side claim was:

- Critic can consume the analyzer contract on `aoi_by_sin_type` and produce a correct `CaptureSelection`

After this slice, the stronger honest claim is:

- Critic can now preserve that bounded analyzer provenance truth after submission/save on both live AOI `aoi_by_sin_type` capture paths

That is materially stronger because the contract is no longer only consumable at click time.
It is now also durable in persisted capture truth and downstream source snapshots.

The claim is still deliberately narrower than full routed semantics:

- prompts remain genealogy-shaped
- Arsenal stream naming remains genealogy-shaped
- the persisted truth is workflow-type truth, not run-identity truth
- no current host surface yet proves that persisted capture truth is read back and surfaced after reload on the AOI V2 page

## Why This Matters

This slice closes the write-side half of the bounded AOI V2 loop.

The progression is now:

1. analyzer-v2 emits bounded first-hop affordance and handle truth
2. one live Critic V2 surface consumes that truth to create a correct `CaptureSelection`
3. the existing Critic capture pipeline now preserves that truth on the write side after submission/save

That is a real advance, but it is still AOI-local and still mostly about write-path truth.
Reusable substrate value is stronger than it was before, but not yet proven on the read side or beyond AOI.

## Next Honest Step

The next bounded question should stay on the same AOI `aoi_by_sin_type` line and move to the read side:

- can the current Critic runtime read that newly truthful persisted capture/provenance state back onto the page after reload or revisit?

The current obstacle is concrete:

- `V2TabContent` already threads `_captureStatusMap`
- `useCaptureStatus(...)` already exists
- but the only shared read seam is still:
  - genealogy-job keyed
  - section-level
- the bounded AOI proof line is now:
  - analysis workflow keyed
  - `entity_id` keyed
  - card-level

So the next honest step is not:

- another analyzer-only specialization
- another AOI-only payload shape
- generic workflow-neutral capture law

It is:

- one bounded AOI V2 capture-status/provenance surfacing slice
- still host/backend only in Critic
- still on `aoi_by_sin_type`
- proving that persisted capture truth can be read back and surfaced on the same bounded card surface without widening into generic capture-status law or broader product semantics
