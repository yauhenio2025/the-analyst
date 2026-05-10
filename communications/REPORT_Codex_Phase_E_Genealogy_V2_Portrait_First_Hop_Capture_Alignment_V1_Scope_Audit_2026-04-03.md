# Report: Codex Audit Of Phase E Genealogy V2 Portrait First-Hop Capture Alignment V1 Scope

Date: 2026-04-03
Subject memo: `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_scope.md`
Verdict: `Approve with corrections`

## Reviewed Materials

- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_scope.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_completion.md`
- `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_scope.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Code Reviewed

- `src/presenter/first_hop_affordance.py`
- `src/presenter/presentation_api.py`
- `src/views/definitions/genealogy_portrait.json`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiThemeFindingsMiniCardList.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.test.tsx`

## Verification Run

- `CI=1 npm test -- --watchAll=false --runInBand --runTestsByPath src/components/V2TabContent.test.tsx src/contexts/CaptureContext.test.tsx`
  - result: `2 passed, 12 tests passed`
  - note: existing Jest open-handle warning still prints after completion

## Findings

### 1. The proposed negative browser proof is overstated as written

The memo says one focused Playwright spec on the live genealogy page should verify both:

- capture controls appear when `genealogy_portrait` is generically capturable
- no capture controls appear on the same surface when first-hop capturability is absent

The first half is fine.
The second half is not honest as a live-page claim without a mocked or fixture-backed presentation.

Current analyzer rules attach generic `first_hop_affordance` whenever:

- the workflow key is eligible, including `intellectual_genealogy` (`src/presenter/first_hop_affordance.py:17-19`)
- the emitted payload is a migrated analytical leaf (`src/presenter/first_hop_affordance.py:43-60`)

`genealogy_portrait` is defined on `workflow_key = "intellectual_genealogy"` and `engine_key = "genealogy_final_synthesis"` (`src/views/definitions/genealogy_portrait.json:2-20`), and first-hop affordances are attached on job-backed presentation payloads before they are returned (`src/presenter/presentation_api.py:829-840`, `1079-1083`).

So the memo should change the proof plan to one of:

- positive path on the live genealogy page, plus negative path in unit tests
- positive path on the live genealogy page, plus negative path in a mocked Playwright fixture

It should not promise that both sides are directly available on the untouched live page.

### 2. The memo correctly names the main host gap, but it understates how much of `SynthesisRenderer` is still host-local capture logic

The memo is right that `SynthesisRenderer` still gates on host-local assumptions and omits `source_workflow_key`.
But the current gap is slightly broader:

- capture UI appears on `captureMode && onCapture` only (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:57-99`)
- the emitted selection hardcodes `source_type: "genealogy"` instead of consuming `_captureSourceType` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:101-112`)
- the emitted title hardcodes `Synthesis > ...` instead of consuming `_captureViewName` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:108`)
- the emitted selection does not send `entity_id` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:101-112`)
- the emitted selection does not send `source_workflow_key` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:101-112`)

That matters because `V2TabContent` already threads the exact metadata the renderer should consume:

- `_workflowKey`
- `_captureViewKey`
- `_captureViewName`
- `_captureSourceType`
- `_captureEntityId`
- `_captureJobId`
- `_firstHopAffordance`

See `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:568-598`, with existing contract coverage in `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.test.tsx:380-445`.

The memo's scoped fix is still right.
It should just describe the gap more precisely as "consume already-threaded analyzer/host metadata truthfully" rather than only "add `_firstHopAffordance` gating and `source_workflow_key`."

### 3. The analyzer-side eligibility claim is correct, but it should be phrased as leaf-conditional

The memo says analyzer-v2 already emits generic first-hop truth on the eligible genealogy migrated leaf family.
That is correct in substance, but the actual rule is:

- eligible workflow key
- migrated engine family
- no child payloads

See `src/presenter/first_hop_affordance.py:39-60`.

That is not a blocker here.
`genealogy_portrait` is a live active view bound to `genealogy_final_synthesis` on `intellectual_genealogy` (`src/views/definitions/genealogy_portrait.json:2-20`), and Critic already treats it as a dedicated local current surface (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts:19-24`).
I found no contrary evidence that the current served `genealogy_portrait` path is non-leaf.

But the memo should say "when emitted as the migrated genealogy leaf payload" rather than stating the affordance as unconditional law.

## Direct Answers To The Review Questions

### 1. Does `genealogy_portrait` actually receive generic `FirstHopAffordance` under the current analyzer rules?

Yes, conditionally, and the condition matches this slice.

- `intellectual_genealogy` is an eligible workflow (`src/presenter/first_hop_affordance.py:10`, `17-19`)
- `genealogy_final_synthesis` is in the migrated engine family (`src/presenter/first_hop_affordance.py:20-35`)
- affordance attachment happens on job-backed presentations (`src/presenter/presentation_api.py:837-840`, `1081-1083`)
- the only qualifier is that the emitted payload must be a leaf (`src/presenter/first_hop_affordance.py:43-60`)

So the memo is directionally correct.
It should just keep the leaf qualifier explicit.

### 2. Is this slice genuinely matrix-broadening, or just host cleanup on an already-capturable surface?

It is matrix-broadening through host alignment, not analyzer broadening.

Analyzer-side capturability is already there.
What is missing is a current non-AOI V2 consumer that actually obeys that analyzer-owned contract.
Given the roadmap's current open question is "move from AOI-only current-consumer proofs to one current non-AOI surface" (`communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`, Phase E section), this host-only cleanup is exactly the honest matrix-broadening move.

### 3. Is the proposed use of `entity_id` on this non-AOI slice honest?

Yes, if it remains explicitly job/run identity only.

`CaptureContext` and `ResearchFlagDialog` already treat genealogy `entity_id` as a fallback source for `genealogy_job_id` when an explicit genealogy job id is absent (`/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:97-114`, `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx:109-126`).

So using `entity_id = _captureEntityId || _captureJobId` is honest for this bounded slice as long as the memo keeps saying:

- this is not per-section or per-idea identity semantics
- this proof stops at selection correctness, not read-side status semantics

### 4. Is the memo honest that this would prove non-AOI host alignment only, not generic custom-renderer law or non-AOI read-side truth?

Yes.

The memo is appropriately bounded.
This slice would prove:

- one live non-AOI current V2 custom renderer can consume analyzer-owned generic capturability truth
- the same renderer can emit truthful workflow provenance into the existing capture pipeline

It would not prove:

- generic custom-renderer contract law
- generic non-AOI read-back/status surfacing
- section-level identity taxonomy
- analyzer or backend semantic broadening

### 5. Is `genealogy_portrait` really smaller and cleaner than `IdeaEvolutionRenderer` for the next proof?

Yes.

`SynthesisRenderer` is smaller because it is already a bounded section-capture surface with simple prose/section data handling (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:48-129`).

`IdeaEvolutionRenderer` is materially broader:

- multi-source data adaptation
- expansion state
- optional follow-up fetch for functional extraction
- item-level capture semantics on idea cards

See `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:372-585`.

So the memo is right to defer `IdeaEvolutionRenderer`.
That renderer is a later non-AOI item-identity question, not the smallest first non-AOI alignment proof.

### 6. Does the memo correctly identify the real current host gap?

Mostly yes.

It correctly identifies the two most important facts:

- `SynthesisRenderer` still gates capture locally rather than consulting `_firstHopAffordance` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:96-99`)
- it omits `source_workflow_key` (`/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:101-112`)

The correction is that the renderer also still hardcodes other capture truth:

- hardcoded `source_type`
- hardcoded title shape
- omitted `entity_id`

So the memo should describe the gap as broader config-consumption alignment inside the renderer, not only one omitted field.

### 7. Is a host-only alignment slice the right next move?

Yes.

It fits the anti-drift rules in `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`:

- it consumes analyzer-owned truth that already exists
- it broadens the current proof matrix beyond AOI-only current consumers
- it does not reopen analyzer semantics, backend schema, or generic renderer-package law

I do not see a cleaner next step in the reviewed context.
Jumping straight to generic custom-renderer law or non-AOI read-side surfacing would widen the variable set too early.

## What This Slice Would And Would Not Prove

If implemented as scoped, this slice would prove:

- one live non-AOI current V2 surface in Critic can obey analyzer-owned generic first-hop capture truth
- one current non-AOI renderer can emit truthful `source_workflow_key` and bounded identity into the existing capture pipeline
- the current host does not need new analyzer semantics to make that non-AOI selection truthful

It would not prove:

- generic custom-renderer law across Critic
- generic non-AOI read-side capture status surfacing
- section-unique or item-unique identity semantics for genealogy
- any new analyzer or backend substrate
- anything about `IdeaEvolutionRenderer`

So this is a real analyzer-v2-as-brain strengthening step, but still a bounded one.

## Most Defensible Next Move

Proceed with this slice, with two corrections to the memo:

1. Keep the implementation local to `SynthesisRenderer`.
   - Do not widen into `IdeaEvolutionRenderer`.
   - Do not widen into generic renderer-package law.

2. Gate capture controls on the full truthful config set the memo already names:
   - `_captureMode`
   - `_onCapture`
   - `_captureViewKey`
   - `_captureViewName`
   - `_captureSourceType`
   - `_workflowKey`
   - `_captureJobId`
   - `_firstHopAffordance?.capturable === true`

3. Emit the bounded truthful selection the memo proposes:
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

4. Keep verification honest:
   - unit tests for both positive and negative capture gating
   - live Playwright proof for the positive path
   - mocked or fixture-backed proof, or unit tests only, for the no-affordance negative path

## Final Recommendation

Approve this as the right next bounded Phase E step, but revise the memo before implementation.

The strategic move is correct:
after the AOI pure-surface and mixed-surface proofs, the next honest unresolved question is current non-AOI host alignment on a live V2 surface.
`genealogy_portrait` is the smallest defensible target.

The required corrections are narrow:

- describe the current host gap as broader capture-config truth consumption, not only `_firstHopAffordance` plus `source_workflow_key`
- stop promising that the no-affordance path can be proven directly on the untouched live genealogy page

With those corrections, the memo is technically sound, strategically aligned, and properly bounded for the analyzer-v2-as-brain objective.
