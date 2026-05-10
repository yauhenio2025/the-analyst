# Memo: Phase E Genealogy V2 Portrait First-Hop Capture Alignment V1 Completion

Subtitle: One bounded live non-AOI current V2 renderer now consumes analyzer-owned generic first-hop capture truth and emits a less renderer-coupled genealogy `CaptureSelection` without reopening analyzer or backend semantics

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
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_scope.md`
Review Context:
- `communications/REPORT_Codex_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Scope_Audit_2026-04-03.md`
- `communications/REPORT_Claude_Phase_E_Genealogy_V2_Portrait_First_Hop_Capture_Alignment_V1_Scope_Critique_2026-04-03.md`
Host Codebase:
- `/home/evgeny/projects/the-critic`

## Purpose

Record what actually landed on the bounded non-AOI current-V2 proof line after the AOI pure-surface and mixed-surface consumer proofs.

This slice is about one live genealogy renderer consuming already-threaded analyzer-owned capture truth more honestly.
It is not a claim that:

- generic custom-renderer capture law now exists
- genealogy read-side truth surfacing now exists
- finer-grained genealogy identity semantics now exist
- non-AOI persistence semantics needed to change
- analyzer-v2 needed new first-hop semantics

## What Landed

One bounded host-side alignment slice is now complete on the live non-AOI `genealogy_portrait` surface in Critic.

The landed behavior is:

1. `SynthesisRenderer` no longer treats section capture as purely host-local unconditional behavior
2. section capture now renders only when the existing threaded runtime config is present and the analyzer-owned generic first-hop affordance says the surface is capturable
3. the renderer now uses config-threaded values rather than local hardcoded literals for:
   - `source_type`
   - `source_view_key`
   - `context_title`
   - `source_workflow_key`
   - `entity_id`
4. genealogy compatibility fields remain intact:
   - `genealogy_job_id`
   - `source_renderer_type = "synthesis"`
   - `content_type = "section"`
   - `depth_level = "L1_section"`
5. section coverage stayed intentionally narrow:
   - capture remains available only on:
     - `exec_summary`
     - `portrait`
     - `key_findings`
   - capture was not broadened to:
     - author profile
     - methodological notes
     - idea genealogy summaries
6. the proof boundary remains the existing `CaptureActionBar`
7. no analyzer-v2 runtime changes landed
8. no backend or persistence changes landed

## The Final Boundary

The honest completed claim is:

- one live non-AOI current V2 renderer now consumes analyzer-owned generic first-hop truth instead of relying only on host-local unconditional capture assumptions
- the resulting `CaptureSelection` is more truthful about workflow, entity, and view provenance than the prior renderer-local implementation, while becoming less renderer-coupled about `source_type` and title composition

What this does not mean:

- genealogy capture identity is now item-level or section-disambiguating
- non-AOI read-side status surfacing now exists
- generic custom-renderer law is now proven
- allowed-destination policy is now consumed end to end on this renderer
- all genealogy renderers now consume first-hop truth
- `IdeaEvolutionRenderer` is solved
- any downstream `/captures` or destination semantics changed in this tranche

## Implementation Shape

The implementation stayed local to Critic and local to the current genealogy portrait renderer path.

The landed shape is:

- `V2TabContent` continues to thread the capture/runtime metadata it already had:
  - `_firstHopAffordance`
  - `_workflowKey`
  - `_captureViewKey`
  - `_captureViewName`
  - `_captureSourceType`
  - `_captureJobId`
  - `_captureEntityId`
- `SynthesisRenderer` now consumes that threaded truth directly
- section capture is now gated on:
  - capture mode
  - handler presence
  - required threaded config presence
  - `_firstHopAffordance?.capturable === true`
- emitted selections now include:
  - `source_workflow_key`
  - `entity_id = _captureEntityId || _captureJobId`
  - config-derived `context_title`
  - config-derived `source_type`

Three calibration details matter:

1. **`source_type` is now composable, not system-truth-redefined**

The renderer now consumes `_captureSourceType` rather than hardcoding `"genealogy"`.
On this path, `V2TabContent` still resolves that value to the same downstream string:

- `"genealogy"`

So this slice improves composability and reduces renderer-local coupling without breaking the current capture route expectation.
But it does **not** mean system-level `source_type` truth was redesigned here:

- `V2TabContent` still derives `_captureSourceType` using the existing `workflowKey?.includes('genealogy')` heuristic

2. **This slice consumes the shallowest first-hop signal**

What was consumed here is:

- `_firstHopAffordance?.capturable === true`

That is real analyzer-owned truth and worth aligning to.
But it is also the shallowest current first-hop signal in the proof matrix.
This slice did **not** consume:

- `allowed_destinations` as renderer policy
- deeper surface-specific semantics
- richer item-level identity semantics

3. **`entity_id` is still bounded run/job identity only**

On `genealogy_portrait`, `entity_id` is:

- `_captureEntityId || _captureJobId`

That is useful and more truthful than omitting it.
But it does **not** mean:

- section-level identity is now solved
- two captured sections from the same genealogy run are disambiguated by `entity_id`

That remains a later question if genealogy read-back or finer-grained non-AOI identity becomes necessary.

One small visible UX delta was accepted in this slice:

- `context_title` now uses the truthful config-derived `"<_captureViewName>: <section title>"`
- instead of the older renderer-local `Synthesis > ...` title shape

That is a bounded presentation change in service of contract truth, not a redesign.
One known artifact remains:

- the portrait section currently produces `Genealogical Portrait: Genealogical Portrait`

That redundancy is acceptable for this bounded alignment pass, but it should be named honestly rather than treated as invisible.

## Verification

Focused host unit verification passed:

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/components/renderers/SynthesisRenderer.test.tsx src/components/V2TabContent.test.tsx src/contexts/CaptureContext.test.tsx`
  - `22 passed`

Focused browser verification also passed:

- `npx playwright test tests/genealogy-v2-portrait-capture.spec.ts --project=chromium`
  - `1 passed`

The browser proof stayed at the intended boundary:

- live `genealogy_portrait` content renders
- entering capture mode exposes the bounded section capture controls
- clicking a section reaches the existing `CaptureActionBar`
- the action bar shows:
  - title
  - preview text
  - depth badge
  - action buttons

No breadcrumb requirement was baked into the live proof because this slice does not need `parent_context` for top-level section capture.

Two environment honesty notes matter:

- Jest still prints the repo's existing post-run open-handle warning after the focused frontend batch passes
- Playwright still requires the dev server to be started with compile-on-error flags because the repo has unrelated existing TypeScript warnings outside this slice

## Calibrated Claim

Before this slice, the strongest honest non-AOI current-renderer claim was:

- `genealogy_portrait` could create section captures, but it did so from host-local assumptions rather than explicit analyzer-owned first-hop truth

After this slice, the stronger honest claim is:

- one live non-AOI current renderer now consumes the already-landed analyzer-owned generic first-hop contract and emits a more truthful workflow/view/entity selection record, while using config-composed `source_type` rather than a local literal, without any analyzer or backend expansion

That is materially better because the proof matrix now includes:

- AOI pure findings
- AOI mixed surface nested findings
- non-AOI current section renderer

The claim is still deliberately local:

- one genealogy renderer
- one host-only alignment seam
- no generic extraction yet

The proof value is therefore mostly:

- surface-family breadth

not:

- contract-depth coverage

## Why This Matters

This slice broadens the evidence base in the right direction.

It shows that the already-landed analyzer contract is not only consumable:

- on AOI surfaces
- on findings-shaped cards

but also:

- on a structurally different current non-AOI renderer that emits section-level captures

That matters because it reduces host analytical autonomy further:

- the host no longer has to decide on its own that this surface is capturable
- the host no longer has to hardcode workflow and title composition locally

But the reusable-substrate value is still bounded.
This is one more necessary non-AOI current-renderer data point toward generic selection-emission parameterization.
It is not the parameterization itself.

## Next Honest Step

The next honest question is no longer whether one live non-AOI current renderer can consume the generic first-hop contract.
That is now proven on `genealogy_portrait`.

The next step should therefore be a calibration step rather than a reflexive genericization claim.

The real question now is:

- is the current evidence base finally strong enough for a narrow generic selection-emission parameterization seam
- or is one more structurally different non-AOI renderer proof still needed first

The strongest likely next candidates are:

- a scoped extraction memo for the smallest honest generic selection-emission parameterization seam
- or one more bounded non-AOI renderer proof on a materially different surface such as `IdeaEvolutionRenderer`, which would test a different dimension:
  - multi-depth capture rather than only L1 section capture

What should **not** happen next:

- another AOI-only consumer refinement
- another analyzer-only first-hop semantic slice
- a premature claim that generic renderer-package law is already settled

So the completion changes the roadmap posture in one specific way:

- the next move should be about whether to extract generic current-renderer selection-emission parameterization honestly
- not about proving yet another AOI-only host consumer
