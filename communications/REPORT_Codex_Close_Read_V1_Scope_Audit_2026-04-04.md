# Report: Codex Close Read V1 Scope Audit

Date: 2026-04-04
Audited memo: `communications/MEMO_2026-04-04_close_read_v1_scope.md`
Verdict: `approve with corrections`

## Context Check

- `communications/MEMO_2026-04-04_close_read_v1_scope.md` — read in full
- `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_completion.md` — read in full
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md` — read in full
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md` — read in full
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md` — read in full
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md` — read in full
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md` — read in full
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md` — read in full
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md` — read in full
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` — read in full
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` — read in full

## Verdict

`approve with corrections`

The scope memo is directionally correct and substantially honest. It chooses the right next question for the program: not more renderer/package cleanup, but one bounded product memo that fixes the V1 boundary, host posture, and first-hop policy explicitly.

The needed corrections are about precision, not direction. The memo should tighten two claims:

1. It should not say or imply that Arsenal and Research todo are the only runtime-real downstream artifacts in the current app estate. They are the right V1 routed destinations to keep in scope, but the runtime inventory also documents other real first-hop artifact seams such as outline talking points and annotation/comment persistence.
2. It should distinguish genealogy as the strongest honest Close Read center of gravity from the stronger claim that all four genealogy surfaces are equally core V1 surfaces. The code supports genealogy as the best product cluster, but the actual likely core is narrower than the whole four-view proof set.

## Explicit Answers

- Is genealogy truly the strongest honest V1 center of gravity, or does the proved surface set suggest a different boundary?
  - Yes, genealogy is still the strongest honest Close Read V1 center of gravity.
  - But the honest reason is product shape plus contiguous proof across one workflow, not that genealogy is already the strongest first-hop policy surface in every dimension.
  - The strongest comparator is AOI `aoi_by_sin_type`, which currently has more specialized first-hop semantics than genealogy, but it is not the better Close Read boundary.

- Is a bounded Critic-hosted pilot the smallest honest host-delivery posture?
  - Yes.
  - The current packed dependency, capture routing, action bar, research-todo flow, and installed-package nested genealogy proof all live on the Critic path today.
  - A thinner or more generic host posture would be aspirational, not code-backed.

- Does the memo stay grounded in current real first-hop operations and current real destinations?
  - Mostly yes.
  - The memo is correct to keep V1 bounded to currently real routed operations and to exclude Book Modeler and lifecycle/taxonomy broadening.
  - The wording should be tightened from “current real destinations only” to “the V1 destination set should intentionally be limited to Arsenal and Research todo,” because the runtime inventory documents other real first-hop artifact seams in Critic.

- Does the memo place first-hop eligibility policy at the right layer?
  - Yes.
  - That is the strongest and most important part of the memo.
  - The code still splits responsibility across analyzer-owned `first_hop_affordance`, Critic-local `currentRendererCapture`, raw package capture in `renderers-ui`, and the universal `CaptureActionBar`, so product law is not yet settled by substrate alone.

- Does any part of the memo still overclaim product readiness or substrate convergence?
  - Only mildly.
  - It does not materially overclaim product readiness.
  - The correction needed is to say more plainly that current evidence proves capture reachability and routing on the current host path, not converged per-surface destination policy and not shared host/package capture law.

- Does the next-step recommendation still hold after inspecting both code and recent memos?
  - Yes.
  - One lean Close Read V1 scope memo is still the correct next move after tightening the wording above.

## Required Corrections

### 1. Tighten the destination claim

Replace the strong assumption that “current real destinations remain Arsenal and Research todo only” with a narrower statement:

- Arsenal and Research todo are the current routed destinations that Close Read V1 should include.
- Other runtime-real first-hop artifact seams exist in Critic, but they are intentionally out of scope for this V1.

That keeps the memo aligned with the routing inventory instead of sounding like the broader runtime inventory says less than it actually does.

### 2. Distinguish core genealogy surfaces from the broader genealogy proof set

The memo is right to default to genealogy, but it should not blur:

- likely primary V1 surfaces:
  - `genealogy_portrait`
  - `genealogy_idea_evolution`
- likely secondary/detail surfaces:
  - `genealogy_target_profile`
  - `genealogy_per_work_scan`

That distinction is already hinted by the view definitions themselves:

- `genealogy_target_profile` is described as a “currently invisible intermediate product”
- `genealogy_per_work_scan` is described as “currently only partially surfaced”

So the scope memo should preserve genealogy as the center of gravity while still allowing the resulting product memo to keep the minimum required V1 surface set narrower than all four views.

### 3. Make the policy gap explicit, not implicit

The memo already says policy belongs at the app layer. It should add one sharper sentence explaining why:

- raw package nested capture does not consume analyzer `first_hop_affordance`
- current custom-renderer capture only gates on `capturable`, not on `allowed_destinations`
- the current `CaptureActionBar` still exposes both host actions whenever a selection is active

That is the actual code-backed reason the next memo must define policy explicitly instead of inheriting it from substrate behavior.

## Code-Backed Rationale

### Why Critic-hosted pilot is the smallest honest host posture

- Critic consumes the refreshed local packed renderer artifact directly through `@the-syllabus/analysis-renderers` `0.6.6` in `/home/evgeny/projects/the-critic/webapp/package.json:10`.
- Critic owns the live first-hop routes through `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:88-147`.
- Critic owns the current user-facing action bar through `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-153`.

That is enough to support a bounded Critic-hosted pilot posture, but not enough to justify a broader thin-host delivery claim.

### Why genealogy is the strongest honest Close Read cluster

- The genealogy views span one contiguous workflow/product stack:
  - `genealogy_target_profile` phase 1 in `src/views/definitions/genealogy_target_profile.json:42-49`
  - `genealogy_per_work_scan` phase 2 in `src/views/definitions/genealogy_per_work_scan.json:54-60`
  - `genealogy_idea_evolution` phase 3 in `src/views/definitions/genealogy_idea_evolution.json:15-21`
  - `genealogy_portrait` phase 4 in `src/views/definitions/genealogy_portrait.json:15-21`
- Installed-package nested proof now exists for:
  - `genealogy_target_profile`
  - `genealogy_per_work_scan`
  - shown in `/home/evgeny/projects/the-critic/webapp/src/components/renderers/InstalledPackageNestedCapture.test.tsx:119-148`
- Host-side current-renderer capture proof exists for:
  - `genealogy_portrait` via `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:61-114`
  - `genealogy_idea_evolution` via `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:380-408` and `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:577-592`

That is the strongest coherent Close Read cluster in current code.

### Why first-hop eligibility must be resolved at the app layer

- `V2TabContent` injects both raw capture config and analyzer `first_hop_affordance` into rendered views in `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:588-597`.
- Raw package capture in `renderers-ui` only checks `_captureMode` and `_onCapture`; it does not read `first_hop_affordance` or `allowed_destinations` in `renderers-ui/src/utils/captureBase.ts:22-39`.
- Critic-local `currentRendererCapture` does read `capturable`, but it does not enforce `allowed_destinations` in `/home/evgeny/projects/the-critic/webapp/src/lib/currentRendererCapture.ts:26-63`.
- `CaptureActionBar` then always offers both current host actions in `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-153`.
- Analyzer-side affordance derivation currently defaults to `["arsenal", "research_todo"]` for eligible genealogy/AOI leaves in `src/presenter/first_hop_affordance.py:60-73`.
- The one genuinely specialized first-hop law currently visible in code is AOI findings-bank Arsenal specialization in `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:51-57` and `/home/evgeny/projects/the-critic/webapp/src/components/renderers/AoiSinFindingsRenderer.tsx:110-113`.

So the memo is correct: current substrate does not yet yield one converged Close Read eligibility law automatically.

## Bottom Line

The scope memo passes the main strategic test. It is aligned with the roadmap recalibration, aligned with the recent package/host completion state, and aligned with the larger analyzer-v2-as-brain objective because it keeps this move product-bounded instead of pretending broader convergence has already happened.

The right read is:

- keep the next move as one Close Read V1 scope memo
- make it Critic-hosted
- keep genealogy as the product center of gravity
- state the first-hop eligibility policy explicitly at the app layer
- correct the memo so it does not overstate destination exclusivity or blur primary genealogy surfaces with the larger proof set

## Verification Note

This audit was code-and-docs backed.
No new tests were run.
