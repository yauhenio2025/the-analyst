# Memo: Phase E Genealogy V2 Portrait First-Hop Capture Alignment V1 Scope

Subtitle: Prove that one live non-AOI current V2 surface can consume analyzer-owned generic first-hop capture truth and truthful workflow provenance instead of relying on host-local unconditional capture assumptions

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
Most Recent Code Completion:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_completion.md`
Immediate Prior Host-Side AOI Scope:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`
Related Current-Consumer AOI Completions:
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Define the next bounded Phase E slice after the completed AOI mixed-surface consumer proof on `aoi_by_theme`.

The AOI current-consumer line is now strong enough:

- one pure findings surface is closed on selection, write-side provenance truth, and read-side truth surfacing
- one mixed AOI surface now consumes generic whole-view capturability plus nested `finding_id`

The next honest question is no longer another AOI-only consumer proof.
It is:

- can one live current non-AOI V2 surface consume the already-landed analyzer-owned generic first-hop contract instead of relying on host-local unconditional capture assumptions?

This memo therefore scopes:

- one bounded host-side non-AOI current-V2 alignment slice in Critic
- on `genealogy_portrait`
- using already-threaded `_firstHopAffordance` and `_workflowKey`
- with no analyzer or backend changes

## Strategic Decision

The next concrete move should be:

- one bounded non-AOI current-V2 first-hop capture-alignment proof on `genealogy_portrait`

not:

- another AOI-only consumer proof
- generic renderer-package law extraction
- non-AOI read-side status surfacing first
- multi-renderer genealogy refactoring
- analyzer-side first-hop semantic broadening
- workflow-neutral destination semantics

The reasoning is straightforward:

- `genealogy_portrait` is already a live current non-AOI surface in Critic
- the renderer already creates section-level captures, so the host proof surface exists
- analyzer-v2 already emits generic first-hop truth for the eligible genealogy migrated leaf family
- the current host still does not consume that analyzer-owned truth explicitly on this surface
- the current capture pipeline already supports `source_workflow_key`, so host alignment can broaden the matrix without reopening backend or analyzer work
- this gives the program a second workflow-family current-renderer data point before generic custom-renderer law extraction is attempted

This changes the Phase E variable honestly:

- keep the analyzer contract fixed
- keep the capture pipeline fixed
- move from AOI-only current-surface proofs to one current non-AOI surface

## Current Evidence Base

Six concrete repo facts make `genealogy_portrait` the right next slice:

1. analyzer-v2 already supports generic first-hop affordance on the genealogy line:
   - `workflow_key = "intellectual_genealogy"`
   - migrated eligible leaf family includes `genealogy_final_synthesis`
   - attachment is still leaf-conditional, and the current `genealogy_portrait` served path is expected to satisfy that condition
   - see `src/presenter/first_hop_affordance.py`
2. `genealogy_portrait` is a live current non-AOI V2 surface in Critic with a dedicated local renderer:
   - `view_key = "genealogy_portrait"`
   - local renderer: `SynthesisRenderer`
3. `V2TabContent.tsx` already threads all runtime metadata needed for a bounded host-side proof:
   - `_firstHopAffordance`
   - `_workflowKey`
   - `_captureViewKey`
   - `_captureViewName`
   - `_captureSourceType`
   - `_captureJobId`
   - `_captureEntityId`
   - `_onCapture`
   - `_captureMode`
4. the current `SynthesisRenderer` still uses host-local capture assumptions rather than consuming the already-threaded runtime truth:
   - `captureMode && onCapture`
   - hardcoded `source_type = "genealogy"`
   - hardcoded `context_title = "Synthesis > ..."`
   - no `entity_id`
   - no `source_workflow_key`
   - it does not consult `_firstHopAffordance`
5. the current capture-provenance substrate already supports the missing truthful fields:
   - `source_workflow_key`
   - `entity_id`
   so the gap is renderer-side config consumption, not backend or analyzer capability
6. `genealogy_portrait` is smaller and more honest than broadening all genealogy renderers at once:
   - `IdeaEvolutionRenderer` remains a later, structurally different non-AOI case

## Scope

### In scope

1. **One bounded non-AOI current-V2 host alignment slice**

Keep the work local to Critic.
Do not add analyzer-v2 runtime changes.
Do not add backend changes.

The target is:

- `genealogy_portrait`
- local renderer: `SynthesisRenderer`

2. **Make section capture explicitly consume analyzer-owned generic first-hop truth**

The current renderer already has bounded section capture controls.
This slice should align that behavior with analyzer-owned contract truth.

Concretely:

- show section capture controls only when all are true:
  - capture mode is on
  - `_onCapture` is present
  - `_captureViewKey`, `_captureViewName`, `_captureSourceType`, `_workflowKey`, and `_captureJobId` are present
  - `_firstHopAffordance?.capturable === true`

Do not require:

- `specialized_family`
- AOI-specific semantics
- item-level `finding_id`

This is a generic non-AOI first-hop proof, not a findings-bank proof.

3. **Consume the full already-threaded host config truthfully on the selection**

The renderer should stop hardcoding capture truth that `V2TabContent` already threads.
It should keep its existing genealogy compatibility fields, but emit the already-supported workflow truth explicitly.

On click, the `CaptureSelection` should include:

- `source_type = _captureSourceType`
- `source_view_key = _captureViewKey`
- `source_section_key = <portrait section key>`
- `source_renderer_type = "synthesis"`
- `content_type = "section"`
- `selected_text = bounded section preview`
- `structured_data = section payload`
- `context_title = "<_captureViewName>: <section title>"`
- `genealogy_job_id = _captureJobId`
- `entity_id = _captureEntityId || _captureJobId`
- `source_workflow_key = _workflowKey`
- `depth_level = "L1_section"`

Two honesty notes matter:

- keep `genealogy_job_id` for backward compatibility with the existing genealogy capture route/hook assumptions
- treat `entity_id` here as bounded run/job identity, not a claim of per-item genealogy identity semantics
- `entity_id` on this slice will not distinguish different sections within the same genealogy run; that remains a later read-side identity question

One small visible behavior change is acceptable in this slice:

- `context_title` should move from hardcoded `Synthesis > ...` to the truthful config-derived `"<_captureViewName>: <section title>"`
- that is a bounded UX delta in service of contract truth, not a redesign

4. **Keep the surface passive-first**

Outside capture mode, or when generic first-hop capturability is absent, the surface should remain the same readable genealogical portrait.

Do not redesign:

- the narrative rendering
- section layout
- prose extraction behavior
- existing capture action bar

5. **Stop at selection correctness**

This slice is about host-side contract alignment and correct selection creation.
It is not a new write-side or read-side persistence tranche.

The proof boundary is:

- the existing `CaptureActionBar`

### Out of scope

- `IdeaEvolutionRenderer`
- genealogy read-side status surfacing
- genealogy deep-linking changes
- new analyzer first-hop semantics
- new backend provenance schema
- generic custom-renderer contract law
- mixed-surface AOI follow-on work

## Test Plan

### Frontend unit tests in Critic

1. `SynthesisRenderer` tests:
   - capture controls render only when `_firstHopAffordance?.capturable === true`
   - capture controls stay hidden when generic first-hop affordance is absent
   - capture controls stay hidden when `_firstHopAffordance` is present but `capturable === false`
   - clicking capture emits the expected `CaptureSelection`
   - `source_workflow_key` is present
   - `genealogy_job_id` remains present
   - `entity_id` is emitted from `_captureEntityId || _captureJobId`
   - `source_type` and `context_title` come from config rather than hardcoded genealogy-only literals

2. `V2TabContent.test.tsx`:
   - no new threading should be needed
   - keep existing assertions honest if the local renderer now reads `_firstHopAffordance` and `_workflowKey`

3. Keep the existing genealogy renderer batch green.

### Browser proof

Add one focused Playwright spec on the live genealogy page.

Verify:

- on a `genealogy_portrait` presentation with generic first-hop capturability, entering capture mode shows the existing section capture controls
- clicking one reaches the existing `CaptureActionBar`
- breadcrumb, title, preview text, and action buttons are correct

Keep the negative no-affordance proof calibrated:

- do not promise that both positive and negative paths are available on the untouched live genealogy page
- the positive path should be live-page browser proof
- the no-affordance negative should be covered either:
  - in focused unit tests
  - or in a mocked / fixture-backed Playwright presentation
  where `genealogy_portrait` is deliberately served without capturability

The browser proof stops at selection creation and handoff.
It does not treat downstream `/captures` success as the thing this slice proves.

## Assumptions and Defaults

- `genealogy_portrait` is the smallest honest non-AOI current-surface step because it already has a local renderer and bounded section capture behavior.
- The analyzer-owned generic first-hop contract is already sufficient here; the current gap is host consumption, not analyzer semantics.
- The strategic payoff is bounded but real: this would create the second workflow-family current-renderer data point needed before generic custom-renderer capture-law extraction becomes honest.
- `entity_id` on this slice is bounded run/job identity only, not a new genealogy item-handle taxonomy.
- `IdeaEvolutionRenderer`, generic custom-renderer law, and non-AOI read-side truth surfacing remain later questions.
