# Report: Phase E Genealogy V2 Portrait First-Hop Capture Alignment V1 Completion Audit

Date: 2026-04-03

## Verdict

`approve with corrections`

The memo is substantially accurate about the landed code boundary.

The needed corrections are mostly about calibration:

- `SynthesisRenderer` now consumes analyzer-owned capturability truth, but not the full first-hop destination-policy contract
- `source_type` now comes from threaded config, but that config value is still host-derived in `V2TabContent`, not analyzer-emitted
- `entity_id = _captureEntityId || _captureJobId` is correct, but on this path both values are currently the same `presentation.job_id`

## The Memo's Strongest Code-Backed Points

### 1. The landed renderer boundary is real and narrow

The memo is right that the completed slice stayed local to the current genealogy portrait renderer path.

- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:57-82` now reads `_captureMode`, `_onCapture`, `_captureViewKey`, `_captureViewName`, `_captureSourceType`, `_captureEntityId`, `_workflowKey`, and `_firstHopAffordance`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:73-82` gates section capture on required threaded config plus `_firstHopAffordance?.capturable === true`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:155-181` only renders capture controls on:
  - `exec_summary`
  - `portrait`
  - `key_findings`

So the memo's narrow section-coverage claim is accurate.

### 2. The emitted `CaptureSelection` is materially more truthful than the prior local literal version

The renderer now emits the provenance fields the memo says it does.

- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:120-132` includes:
  - `source_type`
  - `source_view_key`
  - `source_section_key`
  - `context_title`
  - `genealogy_job_id`
  - `entity_id`
  - `source_workflow_key`
  - `depth_level`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:97-115` forwards `genealogy_job_id`, `entity_id`, and `source_workflow_key` into `POST /api/captures`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.test.tsx:153-220` asserts the new selection shape directly

So the memo is correct that the current renderer no longer relies only on a host-local unconditional capture assumption and that the emitted selection is more provenance-complete.

### 3. The analyzer-side genealogy affordance claim is correct, but leaf-conditional

The underlying analyzer contract does support this surface.

- `src/presenter/first_hop_affordance.py:17-19` includes `intellectual_genealogy` in eligible workflow keys
- `src/presenter/first_hop_affordance.py:20-35` includes `genealogy_final_synthesis` in the migrated composition family
- `src/presenter/first_hop_affordance.py:43-60` only emits the generic affordance for migrated analytical leaf payloads
- `src/views/definitions/genealogy_portrait.json:15-20` binds `genealogy_portrait` to `workflow_key = "intellectual_genealogy"` and `engine_key = "genealogy_final_synthesis"`

So the memo is right that `SynthesisRenderer` now consumes the already-landed generic genealogy first-hop seam.
It should just keep the leaf qualifier explicit.

### 4. The verification claims reproduce cleanly

I reran the memo's cited focused verification surfaces against the current repo state:

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/components/renderers/SynthesisRenderer.test.tsx src/components/V2TabContent.test.tsx src/contexts/CaptureContext.test.tsx`
  - result: `22 passed`
- `npx playwright test tests/genealogy-v2-portrait-capture.spec.ts --project=chromium`
  - result: `1 passed`

The memo's two environment-honesty notes are also still correct:

- Jest still prints the repo's existing open-handle warning after the focused batch passes
- the browser proof still needs the frontend started with `TSC_COMPILE_ON_ERROR=true DISABLE_ESLINT_PLUGIN=true npm start` because unrelated TypeScript warnings still surface in `CrossConceptPanel.tsx`, `DualAxisView.tsx`, and `ConceptsPanel.tsx`

## The Memo's Weakest Or Overstated Assumptions

### 1. It slightly blurs analyzer-owned truth with host-derived config truth

The renderer no longer hardcodes `source_type`, which is an improvement.
But the source of that value is still host-side config derivation, not analyzer output.

- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:591-597` sets:
  - `_captureSourceType: workflowKey?.includes('genealogy') ? 'genealogy' : 'analysis'`
  - `_captureEntityId: presentation.job_id || ''`

So the honest formulation is:

- `SynthesisRenderer` now consumes threaded config instead of local hardcoded literals
- only the capturability gate itself is analyzer-owned in the strong sense

### 2. "Consumes analyzer-owned generic first-hop truth" is accurate only for capturability, not full destination policy

`SynthesisRenderer` consults `firstHopAffordance?.capturable`.
It does not consume `allowed_destinations`.

- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:73-82` uses only `capturable === true`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-135` still always renders both:
  - `Send to Arsenal`
  - `Research Question`

That is not a current genealogy bug because the analyzer affordance on this path still emits both destinations.
But it does mean the memo should avoid sounding like full generic first-hop routing policy is now consumed end to end.

### 3. The memo is right about `entity_id` calibration, but it should be even blunter

The memo correctly says `entity_id` is useful run/job identity and not section-disambiguating identity.
The sharper code-backed version is:

- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:591-595` sets both `_captureJobId` and `_captureEntityId` to `presentation.job_id`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:129-130` emits `genealogy_job_id` and `entity_id` from those values

So on the current genealogy path the fallback expression is real, but the two operands are presently the same value.
This slice improves contract honesty and downstream compatibility more than it adds new identity entropy.

### 4. The memo is mostly calibrated on generic custom-renderer readiness, but that readiness is still modest

The memo does say this is "one more data point" and "not the extraction itself."
That is basically right.

What keeps readiness modest is:

- the current proof is still one local renderer implementation in Critic
- `source_type` remains host-derived
- full `allowed_destinations` policy is not consumed
- the next obvious genealogy follow-on, `IdeaEvolutionRenderer`, is still materially broader and still uses `captureMode && onCapture` plus hardcoded genealogy provenance in `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:380-386` and `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:555-570`

So the memo should keep generic-law language explicitly tentative.

## Factual Discrepancies I Found

No major factual contradiction undermines the memo.

The concrete corrections I would make are:

1. Replace any wording that implies `source_type` is analyzer-owned truth.
   - It is config-derived in the renderer, but host-resolved in `V2TabContent`.

2. Replace any wording that implies full first-hop contract consumption.
   - The current slice consumes generic capturability truth, not destination-policy truth.

3. Tighten the `entity_id` framing.
   - The formula is correct, but on the current genealogy path `_captureEntityId` and `_captureJobId` both resolve to the same job id.

## What This Changes For The Larger Roadmap

This completion does materially strengthen the Phase E matrix.

The strongest honest new statement is:

- one live current non-AOI V2 renderer in Critic now obeys analyzer-owned generic capturability truth at the capture gate and emits more truthful workflow/view/job provenance on the selection it hands to the existing capture pipeline

That matters because the current consumer proof matrix is no longer AOI-only.
It now spans:

- one pure AOI findings surface
- one mixed AOI thematic surface
- one non-AOI current section renderer

But this is still not generic custom-renderer law.

Why not:

- the new proof is still renderer-local
- the host still derives some provenance fields itself
- the shared action bar still ignores `allowed_destinations`
- no non-AOI read-side truth or per-section identity semantics exist yet

So the strongest roadmap interpretation after this completion is:

- the "can one current non-AOI renderer consume the generic first-hop seam at all?" question is now answered
- the "is there a stable reusable custom-renderer capture helper/law?" question is now the real open question

## The Most Defensible Next Move After This Memo

The memo's suggested posture is defensible, but there is a smaller and cleaner immediate follow-on than jumping straight to `IdeaEvolutionRenderer`.

The cleanest next move is:

- one short extraction-calibration memo that compares the three current live consumer patterns:
  - `AoiSinFindingsRenderer`
  - the `aoi_by_theme` findings-bearing shim path
  - `SynthesisRenderer`

That memo should answer one narrow question:

- is there now a smallest honest shared seam for current custom-renderer capture that covers:
  - capturability gating from `_firstHopAffordance?.capturable`
  - required threaded provenance fields
  - renderer-local responsibility for section/item identity and selected payload shape

Why this is cleaner than going directly to `IdeaEvolutionRenderer`:

- it tests whether the current evidence base is actually enough for a reusable seam
- it avoids widening into a much larger non-AOI item-level surface prematurely
- `IdeaEvolutionRenderer` is still 943 lines versus 319 for `SynthesisRenderer`, and its current capture path is still more host-local

If that extraction-calibration memo cannot define one stable shared seam without an exception list, then the next code move should be one more bounded non-AOI proof on `IdeaEvolutionRenderer`.
But the immediate next move should be the calibration memo first, not a reflexive genericization claim and not an immediate larger renderer implementation.
