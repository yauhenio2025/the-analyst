# Report: Codex Close Read V1 Product Memo Audit

Date: 2026-04-05
Audited memo: `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
Verdict: `approve`

## Context Check

- `communications/MEMO_2026-04-04_close_read_v1_scope.md` — read in full
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md` — read in full
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_completion.md` — read in full
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md` — read in full
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md` — read in full
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md` — read in full
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md` — read in full
- `communications/REPORT_Claude_Close_Read_V1_Scope_Critique_2026-04-04.md` — read in full
- `communications/REPORT_Codex_Close_Read_V1_Scope_Audit_2026-04-04.md` — read in full
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md` — read in full
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` — read in full
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` — read in full
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` — read in full

Direct code inspection completed for:

- `src/views/definitions/genealogy_target_profile.json`
- `src/views/definitions/genealogy_per_work_scan.json`
- `src/views/definitions/genealogy_portrait.json`
- `src/views/definitions/genealogy_idea_evolution.json`
- `/home/evgeny/projects/the-critic/webapp/package.json`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/InstalledPackageNestedCapture.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts`

## Verdict

`approve`

This memo now does the job the roadmap needed it to do. It freezes a bounded product boundary without pretending the renderer/package corridor solved product law automatically, and it stays aligned with both the runtime evidence and the larger analyzer-v2-as-brain direction.

The important read is:

- this is no longer a vision memo
- this is not yet an implementation plan
- this is a product-freeze memo that is now stable enough to hand off into a bounded implementation-planning step

## Explicit Answers

- Is the bounded Critic-hosted pilot the smallest honest delivery posture?
  - Yes.
  - The current proved runtime path is still Critic: `CaptureContext` owns submission/routing, `CaptureActionBar` owns the visible first-hop shell, `V2TabContent` threads capture metadata, and the installed `0.6.6` package proves nested genealogy capture on the live host path.

- Is the exact V1 surface set calibrated correctly, especially primary versus supporting genealogy surfaces?
  - Yes.
  - The split is well calibrated and matches the actual view definitions:
    - primary: `genealogy_portrait`, `genealogy_idea_evolution`
    - supporting/detail: `genealogy_target_profile`, `genealogy_per_work_scan`
  - The view metadata itself supports that distinction: `genealogy_portrait` and `genealogy_idea_evolution` are marked `Essential`, while `genealogy_target_profile` and `genealogy_per_work_scan` are marked `Secondary`.

- Is capture-and-route only the right V1 first-hop family?
  - Yes.
  - The broader runtime inventory still contains other first-hop seams, but the memo is right to freeze V1 around one operation family instead of importing outline, comment, findings-bank, or research-answer flows into the first Close Read cut.

- Is the memo's app-layer eligibility policy honest about the current split across raw package capture, `currentRendererCapture`, and `CaptureActionBar`?
  - Yes.
  - The memo is explicit about the real split:
    - raw package capture only needs `_captureMode` and `_onCapture`
    - `currentRendererCapture` additionally requires `_firstHopAffordance.capturable === true`
    - `CaptureActionBar` exposes the two host actions once a selection exists
  - That is an honest product policy over a non-converged substrate, not an overstatement that runtime law is already unified.

- Is the Arsenal / Research todo destination set the right exact V1 routed boundary?
  - Yes.
  - `CaptureContext` still routes only to `/to-arsenal` and `/to-research-todo`, and `CaptureActionBar` still exposes exactly those two actions. The memo correctly frames this as an intentional V1 boundary, not as the totality of all runtime-real seams in the app estate.

- Does any part of the memo still overclaim product readiness, substrate convergence, or destination law?
  - No material overclaim remains.
  - The memo is careful about what is proved versus what is merely frozen as product policy.
  - It does not claim generic capture-law convergence, permanent Critic hosting, generic destination law, or completion of the broader analyzer-v2-as-brain objective.

## Code-Backed Rationale

### 1. Host posture is grounded in the real delivery path

- Critic still consumes the local packed renderer artifact at `@the-syllabus/analysis-renderers` `0.6.6` in `/home/evgeny/projects/the-critic/webapp/package.json:10`.
- The live first-hop routes are still in `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:88-147`.
- The visible action shell is still in `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-153`.
- Capture metadata and analyzer affordance threading are still in `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:588-597`.

That is enough to justify the memo's bounded Critic-hosted pilot posture and not enough to justify any broader host-generalization claim.

### 2. The surface freeze matches both product shape and current proof

- `genealogy_portrait` is the final synthesis and is marked `Essential` in `src/views/definitions/genealogy_portrait.json:4-5` and `src/views/definitions/genealogy_portrait.json:32-33`.
- `genealogy_idea_evolution` is described as the core genealogical product and is marked `Essential` in `src/views/definitions/genealogy_idea_evolution.json:4-5` and `src/views/definitions/genealogy_idea_evolution.json:47-48`.
- `genealogy_target_profile` is described as a currently invisible intermediate product and marked `Secondary` in `src/views/definitions/genealogy_target_profile.json:4-5` and `src/views/definitions/genealogy_target_profile.json:60-61`.
- `genealogy_per_work_scan` is described as only partially surfaced and marked `Secondary` in `src/views/definitions/genealogy_per_work_scan.json:4-5` and `src/views/definitions/genealogy_per_work_scan.json:79-80`.
- Installed-package proof exists for the two supporting nested surfaces in `/home/evgeny/projects/the-critic/webapp/src/components/renderers/InstalledPackageNestedCapture.test.tsx:119-148`.
- Current-renderer capture proof remains aligned for the primary surfaces through `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:61-114` and `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:380-408` plus `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:577-592`.

So the memo's primary-versus-supporting split is not just rhetorically plausible. It is the shape the current view system and host behavior already suggest.

### 3. The eligibility section is honest precisely because it does not pretend the split is solved

- Raw package capture in `renderers-ui` checks only `_captureMode` and `_onCapture` in `renderers-ui/src/utils/captureBase.ts:22-39`.
- `currentRendererCapture` requires `capturable === true` but does not enforce `allowed_destinations` in `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:26-63`.
- `CaptureActionBar` then presents the two current host actions once a selection exists in `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-153`.
- Analyzer-side affordance derivation still defaults eligible genealogy/AOI leaves to `["arsenal", "research_todo"]` in `src/presenter/first_hop_affordance.py:60-73`.

That means the memo is correct to call the current V1 rule an app-layer surface whitelist policy over a split substrate. The memo is freezing product law above current runtime seams, not misdescribing those seams as already converged.

### 4. The destination freeze is the right product boundary

- Runtime routing still terminates only in Arsenal or Research todo through `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:133-147`.
- The visible UI still offers only `Send to Arsenal` and `Research Question` through `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-139`.
- The broader runtime inventory still documents other artifact seams, but the memo explicitly treats those as out of V1 rather than nonexistent.

So the memo's destination freeze is narrow, intentional, and honest.

## Roadmap Read

This memo is aligned with the sequence established in:

- the 2026-04-04 Close Read scope memo
- the 2026-04-04 roadmap recalibration memo
- the 2026-03-30 distilled/state-of-play roadmap memos
- the 2026-03-26 fixed-direction memo
- the master analyzer-v2-as-brain roadmap

The strategic pattern across those documents is consistent:

1. clear the renderer/package corridor
2. freeze the Close Read V1 product boundary
3. then move into bounded implementation planning

This product memo now satisfies step 2.

## Execution Consequence

This memo is safe to turn into a plan.

The next artifact should be a bounded implementation plan for the Critic-hosted `Close Read V1` pilot. That plan should treat the memo's five frozen decisions as inputs, not reopen them.

The concrete execution work now looks implementation-shaped:

- enforce the four-surface V1 eligibility boundary on the current host
- preserve the primary/supporting genealogy surface posture in UX
- keep first-hop scope limited to capture-and-route
- keep routed destinations limited to Arsenal and Research todo
- add focused verification around the split host/package capture boundary

## Verification Note

This audit was docs-and-code backed.

Focused non-destructive verification was rerun on the current checkout:

- `CI=true npm test -- --runInBand --watch=false src/components/renderers/InstalledPackageNestedCapture.test.tsx` — passed
- `CI=true npm test -- --runInBand --watch=false src/contexts/CaptureContext.test.tsx` — passed
- `CI=true npm test -- --runInBand --watch=false src/components/V2TabContent.test.tsx` — passed

`V2TabContent.test.tsx` emitted a Jest open-handles warning after completion. That is a test-harness cleanup issue, not evidence against the memo's product boundary.
