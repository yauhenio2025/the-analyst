# Memo: Distilled Strategic Roadmap

Subtitle: The durable roadmap we should use to orient future work and update progress

Date: 2026-04-13
Program: Dynamic Bespoke Apps Platformization
Status: Strategic guidance memo
Companion Docs:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`

## Purpose

This memo is the simpler strategic roadmap.

It exists because the detailed stage ledger is useful for evidence and history, but too noisy to act as the day-to-day strategic compass.

This document should answer four questions quickly:

1. what are we actually trying to build?
2. what phase are we in?
3. what does “done” mean for each phase?
4. what kinds of work are progress versus drift?

## Core Thesis

The target is still:

- analyzer-v2 is the brain
- apps like the Critic are thin hosts

More concretely:

1. analyzer-v2 should understand the task
2. analyzer-v2 should plan workflows, engines, passes, and sequencing
3. analyzer-v2 should decide presentation structure and UI surfaces
4. analyzer-v2 should compose the rendered analytical experience
5. the host app should mostly route, authenticate, persist project context, and render what analyzer-v2 serves

The destination is not:

- one hand-built proof per engine
- one custom app page per workflow
- one governance workflow that substitutes for missing architecture

The destination is:

- generic composition by contract
- representative proof by substrate
- minimal host intelligence

## What Will Count As Convincing End-State Evidence

We should be explicit about this now, because it prevents wasted work.

The convincing proof will not be:

- proving 100+ engines one by one

The convincing proof will be:

- analyzer-v2 can operate over engine and output contracts generically
- renderer and presentation contracts are formal enough to fail closed
- planning and composition work across representative workflow/output families without host-specific logic
- adding a new engine or pass does not require new app intelligence
- a thin but varied proof matrix demonstrates the generic law honestly

So the standard is:

- representative generality, not exhaustive per-engine theater

## Anti-Drift Rules

Future slices should be judged by these rules first.

### Rule 1: Prefer upstream intelligence over downstream convenience

Good work:

- task understanding
- routing/planning generalization
- presentation law
- renderer contracts
- host-neutral serving contracts

Usually drift:

- app-local workflow behavior
- UI polish that does not encode reusable contract law
- host-side compensation for missing analyzer structure

### Rule 2: Do not confuse bounded proof with generalized architecture

A bounded proof is useful only if it teaches or ratifies a reusable substrate.

Bad sign:

- a slice works only because one app already “knows” what to do

Good sign:

- a slice works because analyzer-owned contracts and generic host behavior are sufficient

### Rule 3: Do not confuse governance with architecture

Governance is downstream of architecture.

It helps us:

- inspect
- evaluate
- review
- resolve

It does not by itself create:

- planner generality
- UI composition generality
- host thinness

### Rule 4: Prefer representative matrices over exhaustive workflow theater

If we have to choose between:

- one more narrow proof on one familiar seam
- or one proof that broadens the contract matrix honestly

we should usually choose the matrix-broadening proof.

## The Strategic Phases

These are the durable phases.
They are intentionally simpler than the detailed stage ledger.

### Phase A: Honest Reference Cases

Goal:

- establish trustworthy bounded exemplars so later generalization is not built on fiction

Exit signal:

- at least one real reference case is documentary-stable and honest enough to anchor later work

Current status:

- substantially done in bounded form

What this phase delivered:

- AOI exemplar honesty closeout
- bounded real proofs instead of purely notional architecture claims

### Phase B: Analyzer-Owned Planning And Composition Spine

Goal:

- move task understanding, routing, planning, and planner-to-presentation handoff upstream into analyzer-v2

Exit signal:

- analyzer-v2 can own a bounded but real planner-to-presentation chain without relying on app-local workflow intelligence

Current status:

- done in bounded form

What this phase delivered:

- routing and task planning seams
- bounded non-AOI planner-to-presentation proof
- analyzer-owned lowering/handoff structure

### Phase C: Thin-Host Serving And Lifecycle

Goal:

- make host apps genuinely thinner and move transient serving/lifecycle truth into analyzer-v2

Exit signal:

- a host can render analyzer-owned transient truth and lifecycle state without re-deriving analytical meaning locally

Current status:

- done in bounded form

What this phase delivered:

- analyzer-owned transient composition
- thin-host rendering
- analyzer-owned session/save/reopen lifecycle

### Phase D: Governance And Accountability

Goal:

- make the bounded analyzer-owned substrate reviewable, inspectable, and governable

Exit signal:

- analyzer-owned reports, gates, reviews, resolutions, and current governance status exist with standalone coverage across the currently supported evaluator substrates, at least one broader upstream governance family beyond downstream proof bundles, and one second materially distinct proof campaign showing the governance stack is not only a wrapper around one frozen dossier

Current status:

- exit signal met in bounded form

What this phase delivered:

- evaluation reports
- gates
- review/disposition
- disposition resolution
- current governance status
- multi-family governance at the definition/topology level
- standalone governance coverage across the two currently supported evaluator substrates
- one upstream routing/planning governance family over frozen analyzer-owned decision artifacts
- one upstream planner-to-presentation governance family over frozen analyzer-owned composition artifacts
- one second upstream planner-to-presentation governance family over a fresh paired proof campaign, proving the governance stack is not artifact-identity-coupled to only one proof lineage

What is still bounded:

- both proof campaigns use the same two workflow families and the same consumer
- true proof-shape generality across different workflow families remains a Phase E question
- no broader review/override product flow or downstream enforcement exists yet

### Phase E: Generality Proof

Goal:

- prove that analyzer-v2 can compose across arbitrary engine/pass combinations by contract, not by custom host behavior or per-engine demos

Exit signal:

- a representative matrix shows that planning, composition, and rendering law generalize across engine/output families without workflow-specific host intelligence

Current status:

- active
- first bounded slice is now complete:
  - one representative composition matrix over the currently live handoff families:
    - `source_profile`
    - `source_selection`
    - `direct_sections`
- second bounded slice is now complete and live-proved:
  - one bounded transient second-consumer proof on:
    - `aoi-canary`
    - AOI `source_selection`
- third bounded slice is now complete and live-proved:
  - one bounded second-consumer broadening slice on:
    - `aoi-canary`
    - AOI `source_profile`
    - `profile = dossier`
  - with matching dossier-only `source_backed_readiness` truth
- fourth bounded slice is now complete and live-proved:
  - one bounded second-consumer broadening slice on:
    - `aoi-canary`
    - AOI `source_profile`
    - `profile = comparison`
  - with matching truthful `source_backed_readiness` law
- fifth bounded slice is now complete and live-proved:
  - one bounded non-AOI second-consumer broadening slice on:
    - `aoi-canary`
    - genealogy `direct_sections`
- sixth bounded slice is now complete and live-proved:
  - one proof-only transient consumer contract plus one standalone minimal harness on:
    - AOI `source_selection`
    - genealogy `direct_sections`
- seventh bounded slice is now complete and live-proved:
  - one additional proof-only consumer identity over that same standalone harness and same two proof seams
- eighth bounded slice is now complete:
  - one standalone-harness lifecycle proof on:
    - genealogy `direct_sections`
- ninth bounded slice is now complete:
  - one standalone-harness lifecycle proof on:
    - AOI `source_selection`
    - via analyzer-owned `persistable_compose_request` truth
- one runtime-first product-side companion tranche is now complete:
  - one Close Read operations/routing inventory over the strongest current Critic runtime evidence
  - one separate matrix appendix that splits:
    - first-hop routing
    - destination-internal lifecycle
    - intent-only evidence
- one analyzer-side composition metadata extraction tranche is now also complete:
  - semantic role for the proved AOI / genealogy family now comes from capability metadata plus a presenter role registry rather than central hard-coded maps
- one analyzer-side bridge-hint consolidation tranche is now also complete:
  - AOI source-bridge and genealogy saved-result role hints now derive from canonical capability metadata instead of bridge-local literals
- one analyzer-side first-hop affordance/routing transient addendum tranche is now also complete:
  - one bounded analyzer-owned first-hop affordance object now survives on the approved transient analytical leaf views
- one analyzer-side job-backed first-hop affordance propagation tranche is now also complete:
  - the same bounded field family now survives on `ViewPayload`, `PagePresentation.views`, and `EffectivePresentationManifest.views`
- one bounded output-specific first-hop semantics tranche is now also complete:
  - `aoi_by_sin_type` can now carry `specialized_family = "findings_bank_arsenal_promotion_v1"` when the emitted cards prove complete `finding_id` coverage
- one bounded mixed-surface nested finding-handle propagation tranche is now also complete:
  - rebuilt `aoi_by_theme` nested findings can now carry `finding_id` while whole-view affordance stays generic-only
- one bounded host-side AOI V2 capture-selection consumer proof tranche is now also complete:
  - one live Critic surface can create a correct `CaptureSelection` on `aoi_by_sin_type`
- one bounded host/backend AOI V2 capture-provenance persistence tranche is now also complete:
  - the current `/captures` line now preserves `entity_id` and truthful workflow-type provenance on that same pure findings surface
- one bounded host/backend AOI V2 capture-status/provenance surfacing tranche is now also complete:
  - the current Critic runtime can now read that persisted truth back onto the same `aoi_by_sin_type` surface after reload or revisit
- one bounded host-side AOI V2 mixed-surface nested-finding consumer proof tranche is now also complete:
  - one current mixed AOI V2 surface, `aoi_by_theme`, can now create correct thematic-finding `CaptureSelection` objects on the findings-bearing family while preserving inherited section behavior and leaving whole-view semantics generic-only
- one bounded non-AOI current-V2 first-hop capture-alignment tranche is now also complete:
  - one live current non-AOI renderer, `genealogy_portrait`, now consumes generic first-hop capturability and less renderer-coupled workflow/view provenance
- one bounded host-only current-renderer selection-emission parameterization tranche is now also complete:
  - the three already-proved current custom renderers now share one smallest honest helper seam for runtime resolution and shared selection-shell assembly
- one bounded analyzer-side first-hop affordance eligibility tranche is now also complete:
  - `genealogy_idea_evolution` now receives generic first-hop affordance through one bounded view+engine+leaf rule without globally blessing `concept_synthesis`
- one bounded host-side non-AOI current-V2 idea-card capture-alignment tranche is now also complete:
  - one live current non-AOI renderer, `genealogy_idea_evolution`, now consumes generic first-hop capturability plus the shared current-renderer seam on idea cards only, with item-level `entity_id` and helper-built title composition
- one bounded public Close Read host/publication tranche is now also complete:
  - the real public host pair is frozen as `the-critic-1` plus `the-critic`
  - the admitted-family Close Read umbrella and family/detail routes are browser-proved on the live frontend
  - the narrow AOI detail, concept detail, and stale genealogy public-law seams were cleared in `the-critic`
- next bounded question is now:
  - now that all four current custom-renderer capture consumers share the same local seam, is that seam honest enough for promotion beyond Critic-local ownership, or is the local helper still the right ceiling?

Important note:

- this is where the real “analyzer-v2 as the brain” claim becomes much stronger
- this phase is not the same as Stage 15

### Phase F: Productization And Operational Consumption

Goal:

- turn the generalized substrate into something that can support real product behavior safely

Potential contents later:

- stronger operational override/enforcement
- live governance policy
- broader host integration
- richer management and inspection surfaces

Current status:

- clearly future

## Current Position

As of 2026-04-03:

- Phase A:
  - closed in bounded form
- Phase B:
  - closed in bounded form
- Phase C:
  - closed in bounded form
- Phase D:
  - exit signal met in bounded form
- Phase E:
  - active
  - first bounded slice complete
  - second bounded slice complete and live-proved
  - third bounded slice complete and live-proved in bounded dossier-only form
  - fourth bounded slice complete and live-proved on the remaining AOI `source_profile:comparison` surface
  - fifth bounded slice complete and live-proved on one bounded non-AOI `direct_sections` path inside the same second-consumer shell
  - sixth bounded slice complete and live-proved on one proof-only consumer contract plus one standalone minimal harness
  - seventh bounded slice complete and live-proved on one additional proof-only consumer identity over that same harness
  - eighth bounded slice complete on one standalone-harness lifecycle proof over genealogy `direct_sections`
  - ninth bounded slice complete on one standalone-harness lifecycle proof over AOI `source_selection`
  - one runtime-first product-side companion inventory now complete
  - one analyzer-side composition metadata extraction tranche now complete
  - one analyzer-side bridge-hint consolidation cleanup tranche now complete
  - one analyzer-side first-hop affordance/routing transient addendum tranche now complete
  - one analyzer-side job-backed first-hop affordance propagation tranche now complete
  - one bounded pure-surface findings-bank specialization tranche now complete
  - one bounded mixed-surface nested finding-handle propagation tranche now complete
  - one bounded host-side AOI V2 capture-selection consumer proof tranche now complete
  - one bounded host/backend AOI V2 capture-provenance persistence tranche now complete
  - one bounded host/backend AOI V2 capture-status/provenance surfacing tranche now complete
  - one bounded host-side AOI V2 mixed-surface nested-finding consumer proof tranche now complete
  - one bounded host-side non-AOI current-V2 idea-card capture-alignment tranche now complete
  - one bounded public Close Read host/publication tranche now complete
- Phase F:
  - future

In plain language:

- the current bounded roadmap has reached all of its early bounded exits through Phase D, and Phase E is now materially underway
- the broad analyzer-v2-as-brain destination still requires Phase E generality proof

## The Current Active Strategic Question

2026-04-13 update:

The older product-boundary question in this section has now been answered in bounded form by the April 5-13 `Close Read` memo chain:

- the genealogy-first boundary was frozen
- the multi-engine/admitted-family boundary was frozen
- the admitted concept seam was live-proved
- the admitted concept seam was then operationally normalized across analyzer-mgmt, the-critic, and analyzer-v2 docs

That public-product question is now also answered in bounded form:

- the real public pair is `the-critic-1` plus `the-critic`
- the admitted-family `Close Read` umbrella is browser-proved on that live frontend
- the narrow AOI detail, concept detail, and stale genealogy public-law seams were fixed in the host frontend

So the current active question is now one layer later:

- what is the smallest honest post-publication `Close Read` corridor:
  - bounded public-product stabilization on the live Critic host
  - or a delivery-posture move such as standalone extraction
  - before any new family admission or broader concept expansion?

That is no longer mainly a publication question.
It is now a post-publication product-posture question.

The previous Phase D question (whether governance is artifact-identity-coupled to one proof lineage) was answered by the cross-campaign planner-to-presentation governance family.
The first Phase E question (whether the current live handoff-family substrate already generalizes across a representative matrix on the current transient consumer surface) was answered by the representative composition matrix.
The second bounded Phase E question (whether one second consumer can be admitted cleanly on one transient AOI path without host-local analytical reconstruction) is now answered through code, focused verification, and live browser/network proof on the `aoi-canary` / AOI `source_selection` path.
The third bounded Phase E question (whether that same second consumer can be broadened to the remaining AOI transient route family in a smaller dossier-first form) is now also answered through code, focused verification, and live browser/network proof on the `aoi-canary` / AOI `source_profile:dossier` path.
The fourth bounded Phase E question (whether that same second consumer can be broadened to the remaining AOI `source_profile:comparison` preset while preserving truthful readiness law) is now also answered through code, focused verification, and live browser/network proof on the `aoi-canary` / AOI `source_profile:comparison` path.
The fifth bounded Phase E question (whether that same AOI-branded second-consumer shell can carry one bounded non-AOI compose path without host-local analytical reconstruction) is now also answered through code, focused verification, and live browser/network proof on the `aoi-canary` / genealogy `direct_sections` path.
The sixth bounded Phase E question (whether the same transient substrate can be consumed outside both existing shells by one proof-only consumer contract plus one standalone minimal harness over the already-proved AOI `source_selection` and genealogy `direct_sections` paths) is now also answered through code, focused verification, and live browser/network proof on the `transient-proof-harness` consumer and `/home/evgeny/projects/transient-proof-harness`.
The seventh bounded Phase E question (whether a second proof-only consumer identity can ride that same harness and same two seams) is now also answered through code, focused verification, and live browser/network proof on `transient-proof-probe`.
The eighth bounded Phase E question (whether the standalone harness can carry analyzer-owned save/reopen lifecycle on genealogy `direct_sections`) is now also answered through code, focused verification, and fresh-navigation save/reopen proof.
The ninth bounded Phase E question (whether that same standalone harness can broaden lifecycle to AOI `source_selection` through analyzer-owned lowered-request persistence truth rather than host reconstruction) is now also answered through code, focused verification, and fresh-navigation save/reopen proof.
The tenth bounded Phase E question (whether the transient compose response itself can carry one bounded analyzer-owned first-hop affordance/routing hint family on the approved analytical leaf surfaces without widening semantics or host responsibility) is now also answered through code, focused verification, and refreshed representative proof bundles.
The eleventh bounded Phase E question (whether the same bounded first-hop contract can propagate honestly onto the mainstream job-backed presentation line) is now also answered through code, focused verification, and contract/hash/trace closeout.
The twelfth bounded Phase E question (whether one pure analyzer-known findings surface can carry one bounded specialized findings-bank semantic family without overclaiming host mutation semantics) is now also answered through code, focused verification, and fail-closed handle gating.
The thirteenth bounded Phase E question (whether one mixed analyzer-known AOI surface can carry nested finding handles without overclaiming whole-view findings semantics) is now also answered through code and focused verification on `aoi_by_theme`.
The fourteenth bounded Phase E question (whether one live Critic V2 surface can consume the already-landed analyzer contract and create a well-formed `CaptureSelection` on a specialized findings surface) is now also answered through code, focused host verification, and browser proof on AOI `aoi_by_sin_type`.
The fifteenth bounded Phase E question (whether the existing Critic capture pipeline can preserve analyzer `entity_id` and truthful workflow-type provenance on that same AOI `aoi_by_sin_type` line through both live capture/save paths) is now also answered through code, focused host/backend verification, browser/network proof, and final server-side normalization of direct research-todo provenance from the persisted linked capture.
The sixteenth bounded Phase E question (whether the current Critic runtime can read that newly truthful persisted capture/provenance state back onto the same bounded AOI V2 pure findings surface after reload or revisit) is now also answered through code, focused backend/frontend verification, browser proof, and final hook-stability hardening so equivalent rebuilt `entity_ids` sets do not refetch the same payload on every rerender.
The seventeenth bounded Phase E question (whether one current mixed AOI V2 surface can consume generic whole-view affordance plus nested `finding_id` on thematic findings while preserving inherited section behavior and leaving whole-view semantics generic-only) is now also answered through code, focused host verification, browser proof, and final closeout hardening on `aoi_by_theme`.
The eighteenth bounded Phase E question (whether one live non-AOI current V2 renderer can consume analyzer-owned generic first-hop capturability and less renderer-coupled workflow/view provenance on `genealogy_portrait`) is now also answered through code, focused host verification, and browser proof.
The nineteenth bounded Phase E question (whether the already-proved current custom-renderer consumers now support one smallest honest shared selection-emission parameterization seam without forcing identity unification or generic renderer-law claims) is now also answered through code, focused helper/adopter verification, and rerun browser proof on the three touched lines.
The twentieth bounded Phase E question (whether the bounded analyzer-side first-hop affordance family should broaden just enough to make `genealogy_idea_evolution` an affordance-eligible `concept_synthesis` leaf without globally blessing `concept_synthesis`) is now also answered through code, focused analyzer verification, and presenter-path hardening.
The twenty-first bounded Phase E question (whether the last materially broader current non-AOI renderer can consume the already-landed helper seam plus generic first-hop capturability on bounded idea-card coverage without widening analyzer, backend, or read-side semantics) is now also answered through code, focused host verification, fresh component-test scaffolding, and browser proof on `genealogy_idea_evolution`.

## What Comes Next

The governance line is now mature enough to survive more than one proof campaign.
The proof-only harness line is now mature enough to carry bounded lifecycle on the current proved seams.
The runtime-first Close Read operations/routing inventory companion is now also complete.

The promotion-readiness question is now also closed.
The top-level package pilot question is now also closed.

Its honest verdict is:

- do not promote `currentRendererCapture` unchanged
- the current helper is only ready for a narrower package-neutral shell

That kept the work in Phase E, and it changed the next bounded step.

That `SubRenderers` slice is now also complete.

The forwarding decision slice is now also complete.

Its honest verdict is:

- one bounded normalization patch is genuinely required first

That bounded release-artifact refresh plus focused Critic host-verification slice is now also complete.

Its honest result is:

- Critic now consumes the refreshed `0.6.6` artifact
- the material nested genealogy host consequences are already cleared on the real installed package path

The genealogy-first `Close Read V1` product memo is now complete.

The post-V1 multi-engine recalibration and boundary-freeze memo are now also complete.

That bounded public-host topology and admitted-family umbrella tranche is now also complete.

The next bounded step should therefore be:

- one bounded post-publication `Close Read` scope
- it should decide the next honest move between:
  - bounded public-product stabilization/hardening on the live Critic host
  - host-delivery posture questions such as standalone extraction
  - later family/submode expansion
- it should keep the admitted family set frozen while that decision is scoped:
  - genealogy
  - `anxiety_of_influence_thematic_single_thinker`
  - concept analysis:
    - `inferential`
    - `logical`
- it should keep analyzer-v2 concept internals, analyzer-mgmt, and generic cross-family operation-law redesign deferred unless the post-publication scope proves a direct blocker

If the strategic intent is now to actually build `Close Read`, the next slice should be read as the first coexistence implementation tranche in that corridor, not as more open-ended platform cleanup.

That corridor is:

1. complete the dominant deferred `SubRenderers` capture-base adoption surface
2. close the forwarding decision gate and accept its `patch required` verdict
3. land the bounded forwarding-normalization patch in local package source
4. refresh the packed artifact into Critic and verify the affected nested genealogy surfaces on the live host path
5. then scope one lean `Close Read V1` product memo bounded to runtime-real first-hop operations and current real destinations, while explicitly resolving host-delivery posture and app-layer first-hop eligibility policy rather than pretending the substrate alone settles them
6. then freeze the first honest multi-engine `Close Read V1.5` boundary around a Critic-hosted umbrella with family-specific genealogy and AOI pages, while deferring AOI compose-from-intent and broader family admission
7. then scope one bounded `Close Read V1.5` coexistence implementation tranche over umbrella routing/nav, genealogy + AOI coexistence, shared capture/provenance baseline, and family-specific page bodies

This changes the Phase E variable honestly:

- the first slice kept the consumer fixed and varied the composition/handoff family
- the second slice kept the transient compose substrate fixed and varied the consumer surface once
- the third slice kept that same consumer fixed and broadened it to the smaller `source_profile:dossier` surface while preserving truthful readiness law
- the fourth slice kept that same consumer and route family fixed and broadened the remaining `comparison` preset surface
- the fifth slice kept that AOI-branded second consumer fixed and broadened it to one bounded non-AOI `direct_sections` path
- the sixth slice kept the already-proved transient substrate fixed and varied the proof vehicle from the AOI-branded shell to one proof-only transient consumer contract plus one standalone minimal harness over AOI `source_selection` and genealogy `direct_sections`
- the seventh slice then kept that harness fixed and varied only consumer identity at the analyzer admission layer, proving bounded proof-only plurality rather than broad generality
- the eighth slice then kept that harness and consumer identity fixed and re-proved the already-earned `direct_sections` lifecycle law across the standalone proof-harness boundary with explicit `session_id` identity and no recomputation on reopen
- the ninth slice then kept that same harness fixed and broadened lifecycle to AOI `source_selection` through analyzer-owned lowered-request persistence truth
- the just-completed companion inventory then mapped the strongest current downstream first-hop operations and routing seams without turning them into premature analyzer schema
- the extraction tranche then externalized the first hard-coded composition maps into metadata for the currently proved engine set, with fail-closed migrated-family enforcement and alias-aware hardening on adjacent compose/view seams
- the bridge-hint consolidation slice then removed the last migrated bridge-local semantic-role literals without changing host or proof behavior
- the first-hop transient addendum then proved that analyzer-v2 can attach one bounded first-hop semantic-affordance/routing hint family to approved transient analytical leaf views, with route-aware gating and hash-honest proof coverage
- the job-backed propagation slice then kept the semantics fixed and proved that the same bounded hint family can survive the mainstream job-backed presentation line with hash and trace honesty intact
- the pure-surface findings slice then proved one bounded specialized findings-bank semantic family on `aoi_by_sin_type`, fail-closed on actual per-card handles rather than workflow/view identity alone
- the mixed-surface finding-handle slice then broadened that same analyzer line on `aoi_by_theme` while keeping whole-view specialization generic-only
- the bounded host-side consumer proof then proved one live Critic V2 surface can already turn the analyzer contract on `aoi_by_sin_type` into a correct `CaptureSelection`
- the next slice then proved that the existing Critic capture pipeline can preserve analyzer `entity_id` and truthful workflow-type provenance through capture creation, persistence, routed source snapshots, and the direct AOI research-question save path
- the just-completed read-side slice then proved that the same bounded pure findings surface can read that persisted truth back after reload or revisit through one project-scoped route, one local hook, and one local renderer seam
- the just-completed mixed-surface slice then proved that one current AOI thematic surface can consume generic whole-view capturability plus nested `finding_id` on the findings-bearing family while preserving inherited section behavior
- the next slice then broadened beyond AOI by proving one current non-AOI V2 surface can consume already-threaded generic first-hop truth on `genealogy_portrait`, while keeping generic custom-renderer law, non-AOI read-side status surfacing, backend/analyzer changes, and broader genealogy renderer work deferred
- the just-completed current-renderer parameterization slice then extracted the smallest honest shared runtime-resolution and shared selection-shell seam across the three already-proved current custom renderers without forcing unified identity semantics or package-generic law
- the just-completed analyzer-side eligibility slice then made `genealogy_idea_evolution` affordance-eligible in one bounded view+engine+leaf-specific way, clearing the real upstream blocker without globally blessing `concept_synthesis`
- the just-completed host-side `IdeaEvolutionRenderer` slice then aligned the last materially broader current non-AOI renderer to the already-landed helper seam and the now-truthful generic first-hop affordance, while keeping idea-card coverage narrow and deferring generic renderer-package law, read-side truth surfacing, and backend/analyzer changes
- the next slice then calibrated the now-four-adopter Critic helper honestly, rejecting unchanged shared-package promotion and identifying one smaller package-native capture-base shell as the next honest candidate
- the next slice then proved that smaller shell in real package code on the top-level package trio while keeping `SubRenderers` and forwarding asymmetries deferred
- the just-completed follow-on then proved the same shell across the dominant inline `SubRenderers` builder surface while preserving current forwarded defaults and leaving nested forwarding asymmetries explicit
- the just-completed decision slice then proved that the remaining `AccordionRenderer` and `CardRenderer` asymmetries still materially block near-term Close Read surfaces, so a bounded normalization patch is required before a lean `Close Read V1` memo
- the just-completed implementation slice then landed that bounded forwarding normalization in local package source, and the next slice should now refresh the packed artifact into Critic while keeping package-wide convergence, generic law claims, destination policy, broader host-delivery posture, and read-side expansion deferred

## How To Update This Memo In The Future

Keep updates short and strategic.

After any material slice:

1. update `Date`
2. update `Current Position`
3. update the relevant phase’s `Current status`
4. add one short note under that phase describing what changed
5. if the active strategic question changed, update that section too

Do not turn this memo into a changelog.
That is what the detailed roadmap and completion memos are for.

## Decision Heuristic For New Work

Before approving a new slice, ask:

1. does this move intelligence upstream into analyzer-v2?
2. does this reduce host-specific analytical behavior?
3. does this strengthen generic law rather than one more special case?
4. does this help eventual contract-based generality rather than just another bounded proof artifact?

If the answer pattern is mostly “no,” the work is probably drift.

## Bottom Line

The pure strategic roadmap is:

1. honest reference cases
2. analyzer-owned planning/composition spine
3. thin-host serving and lifecycle
4. governance and accountability
5. generality proof
6. productization and operational consumption

We are currently here:

- Phase D exit signal met; Phase E is active, its first twenty-three bounded proof/code slices plus one bounded readiness-calibration slice are complete, one runtime-first operations/routing inventory companion is complete, one analyzer-side behavior-preserving composition metadata extraction tranche is complete, one analyzer-side bridge-hint consolidation cleanup tranche is complete, one bounded forwarding decision slice is now also complete, one bounded forwarding-normalization implementation slice is now also complete in local package source, one bounded release-artifact refresh plus focused Critic host-verification slice is now also complete on the live host path, the bounded genealogy-first `Close Read V1` product memo is complete, the bounded post-V1 multi-engine boundary memo is complete, and the next honest gap is one bounded `Close Read V1.5` coexistence implementation scope

We are not yet here:

- Phase E generality proof

That is the cleanest strategic reading of the program.
