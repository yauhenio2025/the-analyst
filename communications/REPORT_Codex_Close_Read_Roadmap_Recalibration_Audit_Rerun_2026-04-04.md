# Close Read Roadmap Recalibration Audit Rerun

## Context Check
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md` — read in full
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md` — read in full
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` — read in full
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` — read in full
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` — read in full
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md` — read in full
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md` — read in full
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md` — read in full
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md` — read in full
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_scope.md` — read in full

Additional audit inputs inspected directly:
- `renderers-ui/src/renderers/AccordionRenderer.tsx`
- `renderers-ui/src/renderers/CardRenderer.tsx`
- `renderers-ui/src/renderers/CardGridRenderer.tsx`
- `renderers-ui/src/sub-renderers/SubRenderers.tsx`
- `renderers-ui/src/utils/captureBase.ts`
- `renderers-ui/scripts/check-capture-base.mjs`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`

Focused verification rerun:
- `renderers-ui`: `npm run build` — passed
- `renderers-ui`: `node scripts/check-capture-base.mjs` — passed
- `the-critic/webapp`: `CI=true npm test -- --watchAll=false --runInBand src/lib/currentRendererCapture.test.ts src/components/V2TabContent.test.tsx` — passed

## Verdict
`approve with corrections`

The memo is directionally right about one thing: if the program now wants an actual `Close Read` build, the roadmap should stop treating it as indefinitely postponed and should describe a bounded corridor from current Phase E work to a lean product memo.

But the memo compresses that corridor too aggressively. The forwarding-normalization decision is the last clearly identified package-internal capture-runtime gate, not the last prerequisite of any kind before honest `Close Read V1` scoping.

## Core Findings

### 1. The memo is mostly honest on package-source state, but it blurs source completion and host-integrated runtime state

The April 4 package work is real in `analyzer-v2` source:
- `renderers-ui/src/utils/captureBase.ts:22-53` now defines the raw package capture shell.
- `renderers-ui/src/sub-renderers/SubRenderers.tsx:538`, `721`, `1366`, `1848`, `2119`, `2348`, `2777`, `3024` show the eight adopted inline builders.

The completion memos are also explicit that no Critic refresh happened:
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_completion.md:169-173`
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md:145-149`

But `the-critic` is still pinned to the packed renderer artifact, not direct source:
- `/home/evgeny/projects/the-critic/webapp/package.json:10`

And the installed package in `the-critic` still shows the pre-extraction/pre-adoption inline capture code rather than the new `captureBase` utility:
- `/home/evgeny/projects/the-critic/webapp/node_modules/@the-syllabus/analysis-renderers/src/sub-renderers/SubRenderers.tsx:536-544`

So the memo should distinguish:
- `renderers-ui` source-side completion: true
- `the-critic` integrated runtime adoption of that package slice: not yet true

### 2. The forwarding-normalization gate is real, but it is not the only missing prerequisite before honest lean `Close Read V1` scoping

The named forwarding gap is real and code-backed:
- `renderers-ui/src/renderers/AccordionRenderer.tsx:515-523` forwards `_captureMode`, `_onCapture`, `_captureJobId`, `_captureViewKey`, and parent-section context, but still omits `_captureSourceType` and `_captureEntityId`.
- `renderers-ui/src/renderers/CardRenderer.tsx:340-378` does not thread capture runtime into nested subsection renderers at all.

That makes the memo correct that forwarding is the remaining package-internal runtime decision gate.

But another prerequisite is still materially missing before honest product scoping:
- the current host/runtime split between raw package capture and Critic-local first-hop policy is still unresolved
- the current host still consumes an older package artifact

Evidence:
- `renderers-ui/src/utils/captureBase.ts:22-53` is intentionally raw: no `_firstHopAffordance`, no workflow/job requiredness, no host policy.
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:26-63` is stricter and host-local: it requires non-empty view metadata and `firstHopAffordance.capturable === true`.
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:588-597` threads `_firstHopAffordance` into renderer config.
- `renderers-ui` package renderers do not consume `_firstHopAffordance`; they only consume the raw package capture shell.

That means the current system is still split across:
- raw package capture emission
- Critic-local current-renderer capture law
- a separate host action bar/context flow

That split is not fatal, but it is still a real prerequisite boundary the memo should name.

### 3. The product-facing routing layer is still more host-local than the memo implies

The memo is careful not to claim generic downstream law. That is good.

But it still leans too close to “after forwarding, write the product memo” without naming that current destination policy is still host-local:
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:88-141` always supports both routed destinations through the generic capture path.
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-135` always renders both `Send to Arsenal` and `Research Question`.
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:40-46` checks only `capturable`; it does not enforce `allowed_destinations`.

So what is proved today is:
- runtime-real first-hop routing to Arsenal and research todo exists

What is not proved today is:
- integrated analyzer-grounded destination policy on package-backed renderers

For an honest lean `Close Read V1` memo, that can be handled in one of two ways:
- explicitly scope V1 around current host-local routing behavior
- or require a small host/package consumption alignment first

The current memo does not make that choice explicit enough.

### 4. The memo remains well aligned with the larger roadmap if it stays clearly below productization claims

This recalibration is broadly compatible with the larger roadmap:
- the strategic docs still place Phase E as active and Phase F productization as future
- they also explicitly allow a `Close Read`-oriented corridor as a bounded product-facing consequence of current Phase E work

The memo stays mostly within those lines because it still defers:
- lifecycle unification
- taxonomy unification
- Book Modeler
- full multi-user architecture
- generic downstream operation law

That is the right strategic posture.

The correction is narrower:
- the memo should not treat forwarding-normalization as the only remaining step before product scoping
- it should treat it as the last identified package-internal gate before one more explicit host-integration/policy check

## Explicit Answers

### Does the memo calibrate correctly between product pull and substrate honesty?

Mostly yes, but not fully.

It calibrates product pull correctly by refusing to jump to full `Close Read` productization and by keeping the scope on first-hop operations plus current real destinations.

It misses full substrate honesty in two places:
- it does not clearly separate `renderers-ui` source completion from `the-critic` integrated runtime state
- it treats forwarding-normalization as the last prerequisite before product memoing, when host/runtime capture-policy integration is still materially unresolved

### Is it true that a lean `Close Read V1` can be scoped honestly after the forwarding-normalization decision, or is another prerequisite still materially missing?

Another prerequisite is still materially missing.

Minimum missing prerequisite:
- refresh/integrate the updated `renderers-ui` package into `the-critic` and reverify the affected nested surfaces there

If the product memo wants analyzer-grounded first-hop semantics rather than “current host behavior as-is,” one further clarification is also needed:
- either consume `allowed_destinations` in the host flow
- or explicitly state that V1 is still using host-local universal Arsenal/Research routing rather than analyzer-owned destination law

### Does the memo stay grounded in current real destinations and runtime-real first-hop operations?

Yes, mostly.

Its destination set stays correctly bounded to:
- Arsenal
- Research

And it keeps lifecycle/taxonomy widening out of scope.

### Does any part of the memo still overclaim convergence in `renderers-ui` or `the-critic`?

Yes, slightly.

It overclaims by implication if read as current integrated completion state:
- `renderers-ui` source is ahead of the package artifact actually consumed by `the-critic`
- `the-critic` still has a split first-hop policy stack across raw package capture, current-renderer helper law, and a universal action bar/context route

### Does the next-step recommendation still hold after inspecting both code and recent memos?

Yes, with one correction.

The next step can still be:
- one bounded forwarding-normalization decision slice

But the corrected corridor after that should be:
1. decide whether one bounded forwarding-normalization patch is required
2. refresh the updated `renderers-ui` package into `the-critic`
3. run focused host verification on the affected nested surfaces
4. then write the lean `Close Read V1` scope memo

If the program wants that product memo to claim analyzer-grounded first-hop semantics, add one explicit host-side affordance/destination-policy clarification before step 4.

## Recommended Memo Corrections

Replace the current bottom-line framing with something closer to:

- the dominant deferred package-local builder surface is complete in `renderers-ui` source
- one bounded forwarding-normalization decision remains as the last identified package-internal capture-runtime gate
- after that, refresh/integrate the package into `the-critic` and verify the affected nested surfaces
- then write a lean `Close Read V1` memo grounded in runtime-real first-hop operations, current real destinations, and explicitly stated host-local versus analyzer-owned policy boundaries

That version preserves the memo’s strategic value while bringing it back into line with the actual codebase.
