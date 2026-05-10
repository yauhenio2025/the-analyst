# MASTER BIG ROADMAP MEMO: ANALYZER-V2 AS THE BRAIN FOR DYNAMIC BESPOKE ANALYTICAL APPS

Date: 2026-04-03  
Status: Canonical program roadmap and progress ledger; updated after April 3 AOI V2 mixed-surface consumer-proof closeout  
Scope: Strategic audit + completed-stage ledger + future-stage breakdown  
Audience: Human decision-makers, future Claude sessions, future Codex sessions, cross-repo implementors

## NON-NEGOTIABLE RULE

This document is now the canonical roadmap memo for this program.

It supersedes the older duplicate draft:

- `communications/MASTER_BIG_ROADMAP_MEMO_DYNAMIC_BESPOKE_APPS_PLATFORMIZATION.md`

That duplicate should not be updated further.

This file is the only canonical strategy/roadmap ledger for the dynamic bespoke-apps program.
That does **not** mean every repo-specific operational master memo must disappear.
For example:

- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`

can remain as an AOI cutover implementation memo, but it is not the canonical cross-program roadmap.

Future sessions should update this file instead of creating another parallel “big picture” memo unless there is a deliberate reason to fork strategy. If strategy changes materially, update this file first and record the change in the decision-revision section.

The point is simple:

- one document should say where we are
- one document should say what is actually done
- one document should say what the next stages are
- one document should say what remains blocked

If future sessions do not keep this memo current, the program will lose coherence.

---

## 1. WHAT THIS PROGRAM IS ACTUALLY TRYING TO BECOME

The real end state is larger than the bounded AOI work of the last week.

The intended system is:

1. a user gives analyzer-v2 a task or analytical goal
2. analyzer-v2 determines what kind of analysis is needed
3. analyzer-v2 selects or plans the right workflows, engines, sequencing, and transformations
4. analyzer-v2 determines what UI surfaces are appropriate for those outputs
5. analyzer-v2 composes the rendered analytical experience
6. a consumer app acts as a thin host that can display the result without needing workflow-specific intelligence

In plain language:

- analyzer-v2 should become the intelligence layer
- consumer apps should become thin host shells
- analytical meaning, surface choice, renderer choice, shaping, and presentational law should live upstream

The strongest version of the thesis is not literally “consumer apps have zero code.”
That is too absolute and not operationally useful.

The realistic target is:

- no analytical expectations placed on the app
- minimal stable host obligations only
- apps provide routing, auth, project shell, and a place to render
- apps do not decide analytical sequencing, engine selection, or visual meaning

That is the right interpretation of “no expectations placed on those apps.”

---

## 2. THE STRATEGIC AUDIT: WHERE WE ARE RIGHT NOW

### Short answer

Yes, the last rounds were directionally correct.

They did not solve the whole vision, but they solved the right downstream half first:

- stronger presentation law
- thinner consumer ownership
- transient composition upstream in analyzer-v2
- source-backed recomposition from real AOI results
- real consumer rendering of that transient path
- real AOI hot-path access to that transient path

This is coherent progress, not random motion.

### Blunt assessment

Against the narrower vision in `communications/DYNAMIC_BESPOKE_APPS_VISION.md`, which explicitly focused on UI composition after engine prose already exists, the program is now in strong shape for one bounded AOI slice.

Against the broader end-state described above, where the system takes a task and decides engines plus UI plus rendering with almost no app-side assumptions, the program is only partway there.

My best honest estimate now needs to separate substrate progress from exemplar ratification:

- for the bounded AOI transient-composition substrate itself: roughly 75-85% of the way
- for the AOI exemplar loop actually ratified end to end: roughly 55-65% of the way
- for the full task -> engines -> bespoke app platform: roughly 30-40% of the way

That gap matters, and it explains why the memo count can make the program feel more complete than it is.

The recent deliverables are not fake progress.
But many of the last Stage 5 slices have been blocker-retirement inside one still-open exemplar gate, not the closure of new platform layers.

So the honest reading is:

- the downstream substrate is materially real
- the first exemplar loop is still not ratified
- the broader platform is still well short of finished

The hard remaining problem is no longer mainly renderer hosting or consumer thinness.
The hard remaining problem is upstream planning **generalization and bridging**:

- task understanding
- workflow routing beyond bounded current objectives
- planner-to-presentation bridging
- engine-chain planning for dynamic composition rather than only job-backed execution
- cross-workflow source-material normalization
- semantic page planning beyond one bounded AOI slice

---

## 3. WHAT HAS ACTUALLY BEEN ACCOMPLISHED

### 3.1 Foundation already present before the last week

Before rounds 9-14, the program had already built meaningful substrate:

- engine definitions and schemas
- transformation templates and dynamic transformation generation
- view generation from patterns
- presenter pipeline
- shared renderer package
- style schools and design-token machinery
- generic workspace proof work
- bounded adaptive/declarative surface-family selection work
- a substantial orchestrator/adaptive-planner substrate

That last bullet needs to be called out explicitly because it changes the roadmap materially.

The current repo already contains a real upstream planning substrate:

- `src/orchestrator/planner.py`
- `src/orchestrator/adaptive_planner.py`
- `src/orchestrator/pipeline.py`
- `src/orchestrator/catalog.py`
- `src/orchestrator/schemas.py`
- `src/orchestrator/pipeline_schemas.py`
- `src/orchestrator/plan_revision.py`
- `src/orchestrator/sampler.py`
- `src/api/routes/orchestrator.py`
- `src/objectives/definitions/`

Important prior planning docs:

- `docs/MEMO_2026-02-19_orchestrator_vision.md`
- `docs/MEMO_2026-02-23_dynamic_generation_implementation.md`
- `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`

Those documents already contained the real long-term signal:

- don’t make the app smarter
- move intelligence upstream
- eventually reopen compose-from-intent
- eventually confront planning/orchestration

Just as importantly, the code already contains nontrivial planning machinery:

- planner-readable capability catalog assembly
- objective-driven adaptive planning
- multi-phase engine/chain execution plans
- revision/replanning logic
- by-reference analysis paths

So the remaining upstream gap is **not** pure greenfield “build a planner from nothing.”
The remaining upstream gap is:

- generalize the current planner
- bridge it into dynamic composition
- formalize source-selection and page-planning contracts on top of it

### 3.2 What the last week actually delivered

#### Round 9

Closed serve-time renderer-contract law for a bounded AOI proof slice.

Meaning:

- final served `renderer_config` and `structured_data` are no longer just best-effort
- they can fail closed at presenter serve time
- the existing `CompositionIssue` / `BoundedCompositionValidationError` envelope remained sufficient

Primary seams:

- `src/presenter/renderer_contract_enforcement.py`
- `src/presenter/manifest_builder.py`
- `src/presenter/presentation_api.py`

#### Round 10

Removed consumer-owned generic runtime renderer registration from the generic bounded-v2 path.

Meaning:

- generic renderer authority moved further into shared package code
- the-critic no longer needs runtime `init / registry / dispatch` ownership for generic AOI rendering

Primary seams:

- `renderers-ui/src/registry.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/renderers/index.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`

#### Round 11

Added real transient compose-from-intent in analyzer-v2.

Meaning:

- analyzer-v2 can accept bounded AOI intent + prose sections
- analyzer-v2 can plan a flat transient page
- analyzer-v2 can generate view definitions, transform data, adapt for the consumer, and validate the final served contract
- this happens without a job-backed `PagePresentation` fiction

Primary seams:

- `src/presenter/compose_from_intent.py`
- `src/presenter/schemas.py`
- `src/api/routes/presenter.py`

#### Round 12

Proved a thin consumer can render that transient response honestly.

Meaning:

- the-critic does not need to pretend transient pages are ordinary job-backed workspace presentations
- a separate transient contract plus local adapter is enough
- unchanged generic `ViewRenderer` can render the resulting views

Primary seams:

- `/home/evgeny/projects/the-critic/webapp/src/types/transientCompose.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/transientComposeAdapters.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`

#### Round 13

Replaced fixture-backed transient launch with source-backed transient launch from real AOI saved-result identity.

Meaning:

- the-critic resolves which saved result to use
- analyzer-v2 reconstructs source material from analyzer-owned truth keyed by `v2_job_id`
- transient recomposition is no longer mainly a checked-in-fixture trick

Primary seams:

- `src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_client.py`

#### Round 14

Made the AOI transient path reachable from the real AOI hot path.

Meaning:

- a real AOI user can launch source-backed transient compose from the actual AOI panel
- the transient experience remains a separate route and lifecycle
- the system did not collapse transient and job-backed workspace law into one confused thing

Primary seams:

- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`

#### Stage 7 Slice

Landed the first bounded analyzer-owned planner-to-presentation bridge slice:

- AOI source-to-composition bridge behind `compose-from-source`

Meaning:

- analyzer-v2 no longer assembles `profile -> sections` through inline hardcoding alone
- analyzer-v2 now resolves an explicit AOI composition source catalog
- analyzer-v2 records selected and rejected source families with rationale
- analyzer-v2 materializes deterministic compose sections from that bridge contract
- the public `compose-from-source` route stayed stable while its internal resolver contract moved to `compose-from-source-v2`

Primary seams:

- `src/presenter/composition_source_bridge.py`
- `src/presenter/compose_from_intent.py`
- `tests/test_composition_source_bridge.py`

#### Stage 8 Slice

Landed the first bounded analyzer-owned composition-facing task router:

- advisory workflow routing over existing downstream analyzer contracts

Meaning:

- analyzer-v2 can now accept a bounded composition-facing task envelope without a required workflow key
- analyzer-v2 can deterministically choose among:
  - `aoi_transient_source_backed`
  - `genealogy_job_backed`
  - `unsupported`
- analyzer-v2 returns analyzer-native downstream contracts rather than blending host proxy shapes into fake unified launch law
- AOI `source_analysis_id` is now explicitly treated as host-side preparation, not downstream analyzer contract law
- cross-signal AOI tasks with genealogy-shaped source modes fail closed instead of being coerced into genealogy
- the new route is advisory only and never dispatches into execution or composition

Primary seams:

- `src/orchestrator/task_routing_schemas.py`
- `src/orchestrator/task_router.py`
- `src/api/routes/orchestrator.py`
- `tests/test_task_router.py`

#### Stage 9 Slice

Landed the first bounded analyzer-owned route-plus-hydrate-plus-plan seam:

- `plan-task` over the existing orchestrator substrate

Meaning:

- analyzer-v2 can now accept the Stage 8 task envelope plus planner-ready context and normalize the outcome into:
  - a persisted genealogy execution plan with executor-ready `document_ids`
  - a bounded AOI composition handoff plan over the Stage 7 source bridge
  - `insufficient_context`
  - `unsupported`
- the new planning boundary reruns canonical routing internally while allowing optional prior-routing validation in trace
- genealogy planning reuses the existing inline and by-ref planner substrate instead of inventing a second planner
- AOI planning stays honest and narrow:
  - handoff metadata only
  - no profile automation
  - no automatic compose dispatch

Primary seams:

- `src/orchestrator/task_planning_schemas.py`
- `src/orchestrator/task_planner.py`
- `src/orchestrator/pipeline.py`
- `src/orchestrator/by_ref.py`
- `src/api/routes/orchestrator.py`
- `tests/test_task_planner.py`

#### Stage 10 Slice

Landed the first read-only results-layer source-backed readiness seam across AOI and genealogy:

- `GET /v1/results/by-job/{job_id}/source-backed-readiness`

Meaning:

- analyzer-v2 can now inspect workflow-owned selector feasibility over durable result truth without mutating presenter-owned state
- AOI readiness reports bounded `profile` feasibility over the live Stage 7 source catalog and keeps `compose-from-source` consumer coupling explicit
- genealogy readiness reports bounded `composition_mode` feasibility over result-manifest gating plus read-only copied-payload runtime inspection
- ordinary readiness blockers now return explicit `ready / partially_ready / blocked` results instead of leaking the existing presentation-route `409` behavior
- genealogy readiness inspection stays read-only and does not persist new `genealogy.relationship_classification` artifacts

Primary seams:

- `src/analysis_products/source_backed_readiness.py`
- `src/api/routes/results.py`
- `src/presenter/bounded_dynamic_composition.py`
- `tests/test_source_backed_readiness.py`

#### Stage 11 Slice

Landed the first bounded AOI-first rich semantic page-planning seam across analyzer-v2 and the-critic:

- hierarchical transient compose behind `compose-from-intent-v2` and `compose-from-source-v3`

Meaning:

- analyzer-v2 now plans bounded parent/child transient trees instead of only flat one-section-per-top-level pages
- source-backed transient compose now threads Stage 7 source-family and role metadata into an internal semantic planner context rather than flattening away the matching signals
- semantic matching is now deterministic and fail-closed inside a bounded AOI-local family:
  - `synthesis_primary -> accordion_sections`
  - `comparison_map -> card_grid_grouped`
  - `findings_bank -> accordion_sections`
  - `report_closeout -> prose_narrative`
  - deterministic inventory/listing titles -> `card_grid_simple`
- mixed working-content plus closeout sets can now synthesize one `tab_with_children` parent shell, while all-closeout and all-working-content sets stay flat in this slice
- transient consumer adaptation, served-payload normalization, contract validation, hashing, and `view_count` are now tree-aware rather than top-level-only
- parent `tab` payloads now satisfy analyzer-side renderer contract law via synthetic deterministic container data
- the-critic's AOI transient shell now preserves and renders returned child views instead of explicitly dropping them

Primary seams:

- `src/presenter/compose_from_intent.py`
- `src/presenter/composition_source_bridge.py`
- `src/presenter/renderer_contract_enforcement.py`
- `tests/test_compose_from_intent.py`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/TransientComposeOverviewPanel.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/transientComposeAdapters.ts`

#### Stage 12 Slice

Landed the first analyzer-owned cross-workflow served-renderer-law generalization seam:

- explicit served-intent policy over shared manifest/page/view assembly helpers

Meaning:

- analyzer-v2 no longer decides final renderer strictness from one `composition_mode` allowlist alone
- shared assembly helpers now receive explicit served intent per helper call, so identical payload classes do not drift into different law based on outer route shape
- transient compose remains strict, current AOI job-backed adaptive surfaces are now strict through the shared served boundary, and genealogy now has one real strict served mode plus explicit shadow coverage for the remaining runtime modes
- final serve-time renderer law now includes recursive payload-tree enforcement plus served sub-renderer/container law where container configs actually depend on it
- `tab` child-container law is now explicit and separate from accordion-style section/sub-renderer law
- support and inspection callers like status, trace fallback, polish-source fetch, delivery-style seeding, scaffold generation, variant generation, discovery preview, and orchestrator preview now stay explicitly non-strict instead of inheriting route behavior by accident
- `POST /v1/presenter/compose` now maps strict renderer-law failures to `409` instead of leaking them as generic errors

Primary seams:

- `src/presenter/renderer_contract_enforcement.py`
- `src/presenter/manifest_builder.py`
- `src/presenter/presentation_api.py`
- `src/analysis_products/result_contract.py`
- `src/api/routes/presenter.py`
- `tests/test_served_renderer_contract_policy.py`

### 3.3 What that means strategically

The recent rounds have established a real downstream composition stack for one bounded workflow family:

1. strict rendered-contract law
2. thin consumer renderer ownership
3. transient analyzer-side page composition
4. thin consumer transient rendering
5. source-backed recomposition from real results
6. product-reachable launch path

That is real progress.

---

## 4. WHAT IS TRUE TODAY

These claims are now materially true in code:

1. analyzer-v2 can compose bounded AOI transient pages upstream
2. analyzer-v2 can source those transient pages from real AOI result identity, not just fixtures
3. the-critic can render transient pages through a thin generic renderer host
4. the-critic does not need to own generic runtime renderer registration on the bounded AOI path
5. final served renderer contracts can be enforced at serve time for the bounded AOI proof slice
6. the AOI hot path can reach transient compose without embedding transient rendering inside the normal job-backed workspace
7. analyzer-v2 now has a real AOI source-to-composition bridge contract with explicit catalog resolution, selected/rejected source rationale, and deterministic section materialization behind `compose-from-source`
8. analyzer-v2 now has a real bounded advisory task-routing contract that can choose AOI transient source-backed versus genealogy job-backed without the host deciding the workflow analytically
9. analyzer-v2 now has a bounded planning boundary that can turn routed task plus hydration context into either a real genealogy execution plan or a bounded AOI handoff plan without dispatching execution
10. analyzer-v2 now has a bounded cross-workflow readiness contract over durable results that can report AOI `profile` feasibility and genealogy `composition_mode` feasibility without mutating presenter state
11. analyzer-v2 now has an explicit served-intent renderer-law policy over current transient and job-backed AOI/genealogy presentation seams, with one strict genealogy served mode and shadow coverage for the remaining genealogy runtime modes

These are not just planning claims anymore.

They are grounded in:

- `src/presenter/compose_from_intent.py`
- `src/presenter/renderer_contract_enforcement.py`
- `renderers-ui/src/registry.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

---

## 5. WHAT IS NOT TRUE YET

These stronger claims are still not true and should not be pretended into existence:

1. analyzer-v2 does not yet take an open-ended task and decide the full workflow/engine plan end to end
2. analyzer-v2 does not yet generate arbitrary “critic-like apps” with near-zero host assumptions across workflows
3. the consumer apps are thinner, but they still own meaningful host concerns:
   - routing
   - project context
   - saved-result identity discovery
   - proxying
   - product launch UX
4. compose-from-intent is still AOI-specific by explicit validation, allowlist, and source policy, not just by current habit
5. source-backed compose is still AOI-specific by explicit profile mapping and source reconstruction policy
6. renderer-law enforcement is stronger on AOI than on the system as a whole
7. the page planner is still narrow:
   - flat page
   - bounded pattern set
   - bounded renderer family
   - no general hierarchy invention
8. the system still lacks a broad/general composition-facing task-intake -> workflow-routing -> planner-to-presentation bridge across workflows, even though Stage 8 routing, Stage 9 bounded planning decision normalization, and Stage 10 bounded results-layer readiness now exist for the current AOI/genealogy slice
9. there is still no final decision on the lifecycle of dynamic surfaces:
   - ephemeral only
   - draft/session persistence
   - publication/share semantics

This is the key strategic distinction:

The platform has advanced a long way on downstream presentation composition.
It has also advanced meaningfully on upstream planning infrastructure.
What it does **not** yet have is a clean bridge between those two worlds.

---

## 6. WAS THE LAST WEEK THE RIGHT DIRECTION?

Yes.

It was the right direction for three reasons.

### 6.1 It followed the proof ladder instead of skipping ahead

The roadmap memo in `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md` argued that after declarative/adaptive proof work, the next serious moves should be:

- renderer contract validation
- consumer consolidation
- bounded compose-from-intent

That is exactly what rounds 9-11 did.

Then rounds 12-14 took the same platform thread and made it consumer-real without thickening the app again.

### 6.2 It solved the downstream half first

That was necessary.

If the system cannot:

- produce contract-valid transient pages
- render them through a thin host
- reach them from a real product path

then any upstream “task planner” would be planning into a weak or fake downstream substrate.

The recent rounds made the downstream target much more credible.

### 6.3 It did not cheat by making the app smarter

This is the most important strategic positive.

The work generally respected the doctrine:

- keep intelligence upstream
- keep the host thin
- use the consumer as a launch shell, not as the analytical brain

That is the correct direction.

---

## 7. THE MAIN STRATEGIC RISK FROM HERE

The main risk now is not that the program is going in the wrong direction.

The main risk is that it keeps moving in the same local AOI/the-critic direction for too long and starts optimizing the pilot instead of generalizing the platform.

In blunt terms:

- more AOI app glue is not the same thing as more platform
- more the-critic UX polish is not the same thing as more analyzer intelligence
- more bounded source/profile hardcoding is not the same thing as task-driven composition

The downstream side is now strong enough that the center of gravity should gradually shift toward:

- planning
- orchestration
- general source-material contracts
- broader semantic page planning
- cross-workflow generalization

If that shift does not happen, the program risks building a very sophisticated AOI transient sidecar rather than a genuine dynamic bespoke-app platform.

---

## 8. WHAT THE FULL VISION STILL REQUIRES

The full vision requires all of the following layers to exist, not just some of them.

### Layer A: Task understanding

The system needs to understand:

- what the user is asking
- what kind of analysis that implies
- what level of depth is needed
- what audience/style constraints are relevant

### Layer B: Workflow and engine planning

The system needs to decide:

- which workflow family is appropriate
- whether one workflow is enough or several are needed
- which engines or capabilities to activate
- in what order
- with what data dependencies

### Layer C: Source-material normalization

The system needs durable contracts for turning workflow outputs into reusable source material for composition:

- not only AOI artifacts
- not only AOI phase outputs
- not only one profile mapping

### Layer D: Semantic page planning

The system needs to determine:

- what surfaces are needed
- what hierarchy is needed
- what renderer families are appropriate
- what evidence/stylistic stance is appropriate
- what should be foregrounded versus tucked away

This also requires a stronger semantic-matching layer:

- the system must choose surfaces based on analytical meaning, not just data shape
- the proposal in `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md` is therefore not optional decoration
- some version of that idea is core to the “bespoke” claim

### Layer E: Render law and shaping

The system needs strong contracts so that composed surfaces are valid:

- input schemas
- config schemas
- served-shape normalization
- fail-closed validation

### Layer F: Thin host consumption

The consumer app should need only:

- route + auth + project context
- generic rendering host
- a small number of stable launch and persistence hooks

This host contract is not hypothetical anymore.
It already exists implicitly across analyzer-v2 and the-critic.
The problem is that it remains under-documented and only partially formalized.

### Layer G: Lifecycle and governance

The system eventually needs a stable answer for:

- ephemeral-only experiences
- draft/session persistence
- sharing/publishing
- review/approval
- evaluation and cost/latency guardrails

All of those layers still matter.

---

## 9. FUTURE STAGES REQUIRED TO ACHIEVE THE FULL VISION

The stages below are the complete strategic breakdown as of 2026-03-23.

These are not promises that each stage must map one-to-one to a numbered “round.”
They are the strategic sequence that future rounds should cash out.

### STAGE 0: KEEP THE CANONICAL ROADMAP CURRENT

Goal:

- prevent strategy drift

Why it matters:

- the program now spans multiple repos, multiple proof notes, and multiple partially-closed rounds
- without a canonical ledger, future sessions will optimize local tasks and lose the global target

Must land:

- this memo remains current
- every future implementation memo references this memo
- each session records what stage it advanced and what it did not change

Exit evidence:

- future round memos explicitly update the stage ledger below

### STAGE 1: CLOSE THE DOCUMENTARY TAIL ON ROUNDS 13 AND 14

Goal:

- close the remaining browser-proof/documentary gap on the AOI source-backed and hot-path seams

Why it matters:

- code-complete is not the same thing as documentary-closed
- the roadmap should not build further assumptions on unclosed operational proof seams

Must land:

- live source-backed dossier browser proof
- live source-backed comparison browser proof
- live hot-path dossier browser proof
- live hot-path comparison browser proof
- saved screenshots, URLs, response JSONs, and proof notes
- explicit statement whether round-14 proof subsumes round-13 proof

Still blocked / do not widen:

- no new architecture
- no new lifecycle semantics

Exit evidence:

- round-13 and round-14 proof notes saved and linked here

### STAGE 2: COMPLETE THE AOI MVP AS A GENUINE TRANSIENT ANALYTICAL EXPERIENCE

Goal:

- move AOI transient compose from “proof-host sidecar” to “credible bounded AOI product capability”

Why it matters:

- the current AOI transient path is real but still narrow and profile-driven
- the MVP is not fully closed until AOI transient compose is useful without being overfitted

Must land:

- decide whether AOI transient compose remains explicitly sidecar or becomes a first-class mainstream AOI option
- tighten latency/error UX for real use
- define success metrics for the AOI transient experience
- make the transient path usable enough to compare meaningfully against the job-backed AOI path

Still blocked / do not widen:

- do not turn this into generic cross-workflow productization yet
- do not add persistence by reflex

Exit evidence:

- documented AOI transient MVP criteria
- proof that users can repeatedly launch and use it on real AOI inputs

### STAGE 3: MOVE AOI FROM FIXED PROFILES TO AOI TASK-DRIVEN COMPOSITION

Goal:

- stop relying only on hardcoded `dossier` / `comparison` source-backed profile mappings

Why it matters:

- the current source-backed path is real, but it is still a narrow curated mapping
- this is the first place where “planning” must start to become real even within AOI

Must land:

- AOI task-intake contract beyond two fixed launch labels
- planner that can decide which AOI source sections belong in a transient page
- bounded policy for when to use synthesis, findings, engagement mapping, report, or other AOI outputs
- planner trace that explains why those choices were made

Still blocked / do not widen:

- do not jump straight to cross-workflow orchestration
- do not collapse this into unrestricted generic prompting

Exit evidence:

- AOI task-based transient requests that are not reducible to only `dossier` or `comparison`
- saved proof cases with planner rationale

### STAGE 4: ADD AOI ENGINE/SOURCE-SELECTION LAW

Goal:

- let AOI choose analytical inputs more intelligently rather than assuming a fixed profile bundle

Why it matters:

- true task-driven composition requires some task-driven source/engine selection
- otherwise the system is still composing from a fixed menu rather than actually planning

Must land:

- bounded AOI source-selection planner
- explicit allowed AOI engine/source catalog for composition
- rules for selecting from:
  - thematic synthesis
  - thematic report
  - engagement mapping
  - sin findings
  - potentially future AOI engines
- traceable rejected/selected reasoning

Still blocked / do not widen:

- no full cross-workflow planner yet
- no unconstrained engine graph search yet

Exit evidence:

- AOI planner can choose among multiple possible source combinations for different requests

### STAGE 5: BUILD AOI EVALUATION, QUALITY, AND OPERATIONAL GUARDRAILS

Goal:

- make AOI transient composition measurable instead of only impressive

Why it matters:

- valid pages are not enough
- lifecycle, persistence, and platform-expansion decisions should be informed by evidence rather than instinct

Must land:

- repeatable AOI evaluation fixtures
- explicit quality rubric:
  - engine/source choice quality
  - page plan quality
  - renderer correctness
  - user usefulness
- latency and cost profiling
- failure taxonomy

Still blocked / do not widen:

- do not assume one good demo equals a platform

Exit evidence:

- saved evaluation reports and decision thresholds

### STAGE 6: MAKE THE LIFECYCLE DECISION EXPLICIT

Goal:

- decide whether dynamic surfaces are ephemeral only or have draft/session/publish semantics

Why it matters:

- eventually the platform cannot avoid this question
- sidecar transient routes and persisted analytical workspaces have different laws
- this decision should be made after evaluation evidence exists

Must land:

- one explicit policy:
  - ephemeral-only for now
  - or bounded draft/session persistence
- if persistence is reopened:
  - ownership rules
  - editing rules
  - regeneration rules
  - provenance rules

Still blocked / do not widen:

- do not half-persist without a model
- do not pretend transient and job-backed presentations are the same thing

Exit evidence:

- one memo and implementation path that makes lifecycle law explicit

### STAGE 7: FORMALIZE THE PLANNER-TO-PRESENTATION BRIDGE

Goal:

- connect the existing planning/result substrate to dynamic composition in a reusable way

Why it matters:

- this is the real missing seam between the current orchestrator and the current transient-composition stack
- without it, the system has planning on one side and page composition on the other, but no durable contract between them

Must land:

- analyzer-owned contract that says:
  - what source families are eligible for composition
  - which sources were selected
  - which were rejected
  - how those sources become composition-ready sections
  - how page planning reasons over them
- bounded trace for source-selection and page-plan decisions
- first bridge from existing planner/result truth into dynamic composition

Still blocked / do not widen:

- do not hide this bridge inside consumer code
- do not treat AOI profile bundles as if they were already the general answer

Exit evidence:

- one reusable bridge contract used by at least one bounded planner-to-compose path

### STAGE 8: GENERALIZE TASK INTAKE AND WORKFLOW ROUTING

Goal:

- move from bounded current request/objective shapes toward a real composition-facing task-intake and workflow-routing layer

Why it matters:

- some intake and routing substrate already exists, but it is still bounded by current workflow/objective assumptions
- the broader vision requires a host-callable contract that does not depend on manual workflow selection

Must land:

- composition-facing task/request envelope
- fields for:
  - objective
  - audience
  - desired depth
  - style expectations
  - source constraints
  - workflow hints if any
- workflow capability registry that is planner-readable
- policy for selecting one or more workflows from task semantics
- bounded planner trace
- confidence/fail-closed behavior when the task does not map cleanly

Still blocked / do not widen:

- do not hide workflow selection inside app-specific code
- do not rely only on manually chosen workflow keys

Exit evidence:

- task requests can map to workflow choices without the consumer app deciding

### STAGE 9: GENERALIZE THE EXISTING ENGINE / CHAIN PLANNER FOR DYNAMIC COMPOSITION

Goal:

- make the already-existing engine/chain planner serve the broader dynamic-composition vision rather than only today’s bounded execution paths

Why it matters:

- the bigger vision has always depended on context-driven orchestration
- a substantial planner substrate already exists, so the real work is generalization, objective coverage, and planner/composition integration

Must land:

- planner-readable engine capability metadata
- engine compatibility / dependency model
- broader bounded execution-plan synthesis
- criteria for when an engine output feeds later phases
- trace grammar for engine-plan reasoning
- clean handoff from engine-plan output to composition source selection and page planning

Still blocked / do not widen:

- do not permit unbounded planner freedom without evals and safety
- do not overfit to one AOI path

Exit evidence:

- analyzer-v2 can synthesize nontrivial engine plans from a higher-level task envelope

### STAGE 10: GENERALIZE SOURCE-BACKED COMPOSITION ACROSS WORKFLOWS

Goal:

- replace AOI-specific source reconstruction with a reusable source-backed composition substrate

Why it matters:

- right now AOI has a handcrafted bridge from durable analysis outputs to composition-ready source sections
- the broader platform needs a general source-material contract

Must land:

- workflow-owned source-material adapters or registries
- consistent normalized output contracts for composition
- documented source families per workflow
- failure behavior when source truth is incomplete

Still blocked / do not widen:

- do not force every workflow into the AOI artifact pattern if it does not fit

Exit evidence:

- at least one second workflow can compose from durable source truth without AOI-specific hacks

### STAGE 11: EXPAND PAGE PLANNING FROM FLAT AOI PAGES TO RICHER SEMANTIC SURFACES

Goal:

- move beyond flat page planning with a narrow renderer family

Why it matters:

- the current transient planner is deliberately bounded
- the full vision requires richer semantic surface composition

Must land:

- hierarchy planning
- tab/container law
- broader renderer family support
- stronger semantic mapping from analytical meaning to visual form
- a required semantic visual matching layer informed by `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`, not just data-shape-based renderer choice

Still blocked / do not widen:

- do not reintroduce loose renderer behavior without stronger law

Exit evidence:

- planner can generate richer yet valid page structures under contract validation

### STAGE 12: MAKE RENDERER LAW UNIVERSAL, NOT JUST AOI-STRONG

Goal:

- make renderer contracts and served-shape normalization a platform law across workflows

Why it matters:

- dynamic composition is only credible if the renderer boundary is real everywhere that matters

Must land:

- broader renderer `input_data_schema` coverage
- sub-renderer law where necessary
- cross-workflow contract validation
- stronger preflight and CI checks

Still blocked / do not widen:

- do not assume AOI-proof-mode validation means the platform is universally safe

Exit evidence:

- multiple workflows with fail-closed served renderer law

### STAGE 13: DEFINE AND FORMALIZE THE MINIMAL GENERIC HOST CONTRACT

Goal:

- make the thin-app thesis operational across consumers

Why it matters:

- “apps are disposable shells” only becomes credible if there is a stable minimal host contract
- some of that contract already exists implicitly in analyzer-v2 result/run contracts and the-critic launch/proxy behavior, so the work here is partly formalization, not pure invention

Must land:

- one documented host contract for:
  - routing
  - auth
  - project identity
  - result discovery
  - transient/draft launch
- clearer separation between what the app must own and what analyzer-v2 must own
- removal or isolation of remaining workflow-specific consumer glue where feasible

Still blocked / do not widen:

- do not keep solving platform gaps with another bespoke app seam

Exit evidence:

- second consumer or generic host proof without rebuilding intelligence locally

### STAGE 14: DEFINE DYNAMIC APP / SESSION LIFECYCLE

Goal:

- decide what a dynamically composed “app” actually is as a runtime object

Why it matters:

- the full vision implies more than one-off transient pages
- eventually the system needs stable semantics for:
  - launch
  - revisit
  - save
  - share
  - compare

Must land:

- session/draft/publish model if reopened
- ownership and retention rules
- migration path from transient proof hosts to durable dynamic surfaces if desired

Still blocked / do not widen:

- do not blur “ephemeral proof route” and “persistent user-facing surface”

Exit evidence:

- a lifecycle memo plus one implemented bounded lifecycle path

### STAGE 15: ADD GOVERNANCE, REVIEW, AND HUMAN OVERRIDE

Goal:

- keep dynamic composition auditable and governable

Why it matters:

- a system that plans engines and surfaces dynamically needs review and override seams

Must land:

- trace review tools
- composition approval or inspection flows where needed
- policy for unsafe/low-confidence plans
- eval datasets and release gates

Exit evidence:

- documented governance loop and concrete enforcement points

---

## 10. RECOMMENDED ORDER FROM HERE

If the program wants to stay aligned with the full vision, the recommended order is:

1. finish the AOI exemplar honestly with one fresh post-fix execution-backed rerun and an explicit Stage 2 decision
2. close that AOI phase on the grade itself, not on whether the grade is flattering, so the program does not re-enter open-ended AOI repair by default
3. make planner-to-presentation bridge generalization the main line:
   - de-AOI the transient composition substrate
   - de-`the-critic` the transient consumer contract
   - add one reusable handoff contract that is not AOI semantic law in disguise
   - make explicit ownership decisions for source identity translation, warm-snapshot/continuity behavior, surface selection, and navigation / launch handoff
   - reconcile `taskLaunchRuntime` and Host Contract v1 into one coherent analyzer-to-host story or explicitly stabilize their separation
4. prove stronger host-neutral or second-consumer transient consumption only after that bridge work is real
5. make lifecycle decisions only after the bridge and host-neutral proof are strong enough, except for any narrow ephemeral identity needed to prove Phase 4 honestly
6. add governance, review, and evaluation infrastructure only after the generalized bridge and lifecycle semantics are materially real

That is the coherent path.

Not coherent:

- more and more AOI/the-critic glue without moving upstream
- jumping to “apps on the fly” marketing language before task/workflow/engine planning is real
- prematurely merging transient and job-backed lifecycle law

---

## 11. WHAT SHOULD REMAIN EXPLICITLY BLOCKED FOR NOW

The following should stay blocked unless a later update deliberately reopens them:

1. pretending the consumer app should own analytical orchestration
2. reopening thick consumer workflow logic as the main path
3. treating AOI source-backed compose as if it already generalizes system-wide
4. claiming that renderer-law strength on AOI implies universal platform readiness
5. persisting transient pages by accident rather than by lifecycle decision
6. turning the roadmap into another endless proof-token branch
7. confusing nicer AOI product UX with the completion of the actual orchestration vision

---

## 12.5 FIXED-DIRECTION NOTE FROM THE MARCH 26 BRAIN AUDIT

The March 26 brain-direction audit and phased-roadmap review changed one important ordering judgment:

- lifecycle and governance should not stay ahead of planner-to-presentation bridge generalization and stronger host-neutral transient proof

The reason is simple:

- current code has real bounded upstream routing, planning, readiness, and composition progress
- but the transient composition seam is still materially AOI-shaped and `the-critic`-shaped
- and the host still owns meaningful launch, identity, and surface behavior

So the fixed direction from here is:

1. finish the AOI exemplar honestly
2. then generalize the bridge and ownership boundaries
3. then prove stronger host-neutral transient consumption
4. only then define broader lifecycle law
5. only then build governance and evaluation around that more general architecture

This note should be treated as active canonical guidance, not as a draft sidecar.

---

## 12. STAGE LEDGER

Use this section as the canonical “where are we now?” tracker.

| Stage | Name | Status | Notes |
|---|---|---|---|
| 0 | Keep canonical roadmap current | In progress forever | This memo begins that discipline |
| 1 | Close round-13/14 documentary tails | In progress | Code complete; browser-proof artifacts still need closure |
| 2 | Complete AOI transient MVP | Complete (bounded) | The frozen Stage 5 seam gate remains passed on fixture-backed evidence, and the March 27 fresh Otto rerun `job-744edf255ad5` now completes on the real `the-critic` route, passes thinker-scoped active discovery, reaches durable ready presentation state, and passes the counted planner-primary browser proof on the fresh run. The explicit Stage 2 decision is now `closure-grade exemplar achieved`. This is still bounded current-consumer AOI proof, not planner-to-presentation generalization |
| 3 | AOI task-driven composition | Partial | One planner-primary AOI compose-through-selection proof path now exists in the current consumer and has now been exercised both on the fixed Stage 5 seam-gate pack and on one fresh March 27 `execution_backed` Otto rerun through the real host path. Broader workflow and host-neutral generalization remain open |
| 4 | AOI source/engine-selection law | Partial | Bounded LLM-first AOI source/product-selection law now exists in `plan-task` and feeds a selection-backed compose path; broader AOI/generalized law remains open |
| 5 | AOI evaluation/ops guardrails | Complete (bounded) | The repaired planner-primary path passes the frozen four-case Stage 5 pack on fixture-backed evidence, and the March 27 fresh `execution_backed` Otto rerun now adds thinker-scoped active discovery, durable completed-boundary proof, explicit row-pinned planner-primary browser proof, stable local snapshot reuse, and a successful fresh `compose-from-selection` request/HAR bundle. One legacy AOI landing helper still points Playwright at the wrong host/path, but that helper defect does not block the bounded AOI closeout |
| 6 | Lifecycle decision | Deferred | Should follow evaluation evidence |
| 7 | Planner-to-presentation bridge | Partial | Host Contract v2 now unifies planner-advisory plus delivery/runtime law in the current consumer, immutable planning snapshots stabilize AOI planner-backed recovery, and the shared transient presenter executor now supports both AOI and one bounded non-AOI `direct_sections` planner-to-presentation path. The bridge is now generalized enough to close Phase 1, but stronger host-neutral transient proof remains open |
| 8 | Task intake and workflow routing | Partial | `POST /v1/orchestrator/route-task` now supports one bounded AOI saved-result seam, one bounded genealogy `registered_corpus` execution seam, and one bounded genealogy `saved_result` composition-facing seam. Broader host adoption and objective coverage remain open |
| 9 | Engine / chain planner generalization | Partial | `POST /v1/orchestrator/plan-task` now bridges routed task + hydration into bounded genealogy execution plans, AOI handoff plans, and one generic `direct_sections_composition_handoff_plan` that round-trips through immutable `planning_decision_id` snapshots. Broader planner coverage and stronger host-neutral proof remain open |
| 10 | Cross-workflow source-backed substrate | Partial | `GET /v1/results/by-job/{job_id}/source-backed-readiness` now normalizes AOI profile readiness and genealogy composition-mode readiness over durable results; generalized selector law and broader workflow coverage remain open |
| 11 | Rich semantic page planning | Partial | AOI-first transient compose now supports bounded semantic parent/child trees behind `compose-from-intent-v2` / `compose-from-source-v3`; broader workflow coverage and richer grouping law remain open |
| 12 | Universal renderer law | Partial | Explicit served-intent law now governs transient + current AOI/genealogy served seams; one genealogy mode is strict and the remaining genealogy runtime modes are shadow |
| 13 | Minimal generic host contract | Partial | Host Contract v2 now makes planner-advisory plus delivery/runtime families runtime-authoritative for the bounded current consumer surface set, `aoi-canary` provides the closed Tier A result-backed second-consumer proof plus bounded transient proof on AOI `source_selection`, AOI `source_profile:dossier`, AOI `source_profile:comparison`, and one bounded non-AOI genealogy `direct_sections` path, March 28 Phase 2 provides the stronger current-consumer host-neutral proof page over `run_detail -> route-task -> plan-task(persist_decision=true) -> planning_decision_fetch -> analyzer-owned lowering -> compose-from-intent` with no AOI proxy compose routes and no `/v1/executor/jobs`, March 31 adds one proof-only transient consumer contract plus one standalone minimal harness over AOI `source_selection` and genealogy `direct_sections`, and April 1 closes two further bounded harness seams: one second proof-only consumer identity over that same harness and same two transient seams, plus AOI `source_selection` save/reopen lifecycle through analyzer-owned lowered-request persistence truth with explicit `session_id` identity and zero second compose call on reopen. The next honest gap on this line is no longer another harness proof. It is analyzer-side extraction of the first workflow-shaped composition maps out of central presenter code while preserving the existing proof surfaces |
| 14 | Dynamic app/session lifecycle | Complete (bounded) | March 28 Phase 3 closed one bounded genealogy transient surface that can compose, save into analyzer-owned `compose_session` truth, and reopen by analyzer-generated `session_id` on fresh navigation with zero planner/composition replay on reopen, and April 1 carried that same bounded lifecycle law across the standalone proof-only harness boundary on genealogy `direct_sections` with explicit `session_id` identity and zero second compose call on reopen. Publish/share, broader request-family lifecycle policy, and broader consumer registration remain open |
| 15 | Governance/review/evals | Complete (bounded) | March 30 Phase 4 now lands analyzer-owned persisted evaluation reports, one frozen AOI-plus-genealogy governance pack, one standalone genealogy-only governance family, one standalone AOI-only governance family, one upstream routing/planning governance family over frozen analyzer-owned decision artifacts, one upstream planner-to-presentation governance family over frozen analyzer-owned composition artifacts, one second upstream planner-to-presentation governance family over a fresh paired proof campaign, one deterministic frozen-pack harness with `aoi_exemplar`, `genealogy_lifecycle`, `routing_planning_decision`, and `planner_presentation_decision` branches, one bounded persisted release gate over exact report ids, one bounded persisted review/disposition layer over exact gate ids, one bounded persisted current-disposition resolution layer over exact review ids, canonical current-resolution lookup by `resolution_key + gate_decision_id`, one derived semantic current-governance-status seam with fail-closed chain verification, and read-only report/gate/review/resolution/governance-status inspection routes. Stage 15 is now complete in bounded form; the next active main line is Phase E generality proof over representative composition matrices rather than more governance accretion |

---

## 13. UPDATE PROTOCOL FOR FUTURE SESSIONS

Every future session that materially changes the program should update this document.

Minimum required edits:

1. update the date at the top if the memo changed materially
2. update the stage ledger statuses if any stage advanced
3. add one bullet under “decision revisions” if strategy changed
4. add one bullet under “latest accomplished work” with:
   - what landed
   - which stage it advanced
   - what evidence exists
5. if a stage was intentionally deferred, say so explicitly

### Latest accomplished work log

- 2026-04-01: The bounded Phase E standalone-harness lifecycle proof over genealogy `direct_sections` is now complete. The proof-only harness at `/home/evgeny/projects/transient-proof-harness` now supports `compose -> explicit save -> fresh-navigation reopen by session_id` under `consumer_key=transient-proof-harness` on the pinned genealogy `direct_sections` case, using the existing analyzer-owned compose-session save/fetch routes without widening the public save schema. Fresh saved-session, reopen-segment, invalid-session, HAR, and rendered-screenshot artifacts show planning provenance present, `source_v2_job_id` omitted for this case, one saved-session GET on reopen, zero second `compose-from-intent` calls on reopen, and fail-closed invalid-session behavior. A post-audit hardening pass then made `session_id` visibly primary immediately after save while keeping `planning_decision_id` provenance-only on the harness UI.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_direct_sections_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one standalone-harness AOI `source_selection` lifecycle proof through analyzer-owned lowered-request persistence truth, because the current public save seam still persists intent-shaped requests and the current source-selection response does not expose exact lowered prose bodies to the host
- 2026-04-01: The bounded Phase E transient consumer identity plurality slice is now complete. Analyzer-v2 now defines a second proof-only consumer key, `consumer_key=transient-proof-probe`, with the same renderer surface as `transient-proof-harness`, and the hard-coded transient admission seam now admits it only on `source_selection` and `direct_sections` while keeping `source_profile` fail-closed and readiness blocked there. The standalone harness now parameterizes consumer identity across the same two already-proved proof cases without changing any analytical variables, and fresh analyzer proof bundles plus fresh live browser/network closeouts now exist for both AOI `source_selection` and genealogy `direct_sections` under the probe identity, each recording exact request equality, `200` responses, correct returned `presentation.consumer_key`, and the same pinned returned surface law as the original harness key.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-04-01_phase_e_transient_consumer_identity_plurality_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one standalone-harness lifecycle proof over the already-proved `direct_sections` seam, with explicit `session_id` identity and no recomputation on reopen
- 2026-03-31: The bounded Phase E proof-only transient consumer and minimal harness slice is now complete. Analyzer-v2 now serves a new proof-only `consumer_key=transient-proof-harness` admitted only on `source_selection` and `direct_sections`, `source_profile` remains fail-closed including negative readiness regression coverage, and a new standalone repo `/home/evgeny/projects/transient-proof-harness` now proves the same transient substrate outside both `the-critic` and `aoi-canary` through two fixture-backed cases only: AOI `source_selection` and genealogy `direct_sections`. Fresh analyzer proof bundles and fresh live browser/network closeouts exist for both cases under the new consumer identity, each recording exact request equality, `200` responses, correct resolver versions, correct returned `presentation.consumer_key`, and the pinned returned surface law (`tab` plus bounded raw-json leaf set for AOI, `card_grid` plus empty raw-json leaf set for genealogy).
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-31_phase_e_transient_proof_harness_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded consumer-identity plurality slice over the same standalone harness and same two transient seams before broader lifecycle widening
- 2026-03-31: The bounded Phase E `aoi-canary` / AOI `source_profile:dossier` second-consumer slice is now complete. Analyzer-v2 now admits `consumer_key=aoi-canary` on `POST /v1/presenter/compose-from-source` in bounded dossier-only form, `source_backed_readiness` now mirrors that same dossier-only truth for the pinned AOI source job, `aoi-canary` now carries a second fixture-backed transient proof case over `compose-from-source`, and the slice is closed by both a frozen analyzer proof bundle and a real browser/network live closeout with exact wire-request equality, one `200` response on `compose-from-source-v3`, and no forbidden analytical upstream calls in the captured proof window. A follow-up hardening pass then made the analyzer-side scope fully honest by fail-closing `profile=comparison` for `aoi-canary` and aligning readiness output to that same policy.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_dossier_second_consumer_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded broadening from `source_profile:dossier` to the remaining `source_profile:comparison` surface on the same second consumer
- 2026-03-31: The bounded Phase E transient second-consumer live closeout is now complete. The already-landed `aoi-canary` / AOI `source_selection` path now has one real browser/network proof over `POST /v1/presenter/compose-from-selection`, with a frozen HAR, screenshot, proof note, and JSON summary. The observed wire request matches the pinned analyzer-owned fixture request exactly, the captured live response returns `200` with `resolver_version=compose-from-selection-v1`, no forbidden analytical upstream calls appear in the success path, and the bounded adaptation-quality law still holds live with one closeout-only `raw_json` leaf. No analyzer or canary runtime code changes were needed in this closeout pass.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded broadening of the already-live-proved second consumer from AOI `source_selection` to the remaining AOI `source_profile` compose family plus the matching `source_backed_readiness` consumer coupling
- 2026-03-30: The bounded Phase E transient second-consumer implementation slice is now landed and test-clean. Analyzer-v2 now admits `consumer_key=aoi-canary` on AOI `source_selection` through the existing `compose-from-selection` route while still failing closed for `source_profile` and `direct_sections`, and `aoi-canary` now carries a bounded `transient_proof` mode over a pinned analyzer-owned `ComposeFromSelectionRequest` fixture with a thin field-only normalization adapter and a measurable no-root-`raw_json` / one-leaf-only degradation law. Focused analyzer verification passed (`38 passed, 2 warnings`), canary type-check passed, and canary tests passed (`18 passed`). The remaining gap is evidentiary rather than architectural: the frozen proof JSON is an honest deterministic replay surface, not yet a fresh browser/network live capture, because direct live proof capture hit an unrelated engine-definition load error.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md`
  - Did strategy change? yes
  - Remaining gap: one narrow live-proof closeout over the already-landed `aoi-canary` / AOI `source_selection` transient path
- 2026-03-30: The first bounded Phase E representative composition matrix is now landed and verified without runtime code changes. Analyzer-v2 now has three committed proof bundles covering the full currently live transient compose substrate on the existing transient consumer surface: AOI `source_profile` via `compose-from-source`, AOI `source_selection` via planner-backed `compose-from-selection`, and genealogy `direct_sections` via planner-backed lowering into `compose-from-intent`. One dedicated `tests/test_representative_composition_matrix.py` seam now mechanically proves request/response contract validity, resolver-version correctness, view-count agreement, AOI handoff-plan request derivation, and exact genealogy `lowering_response_json == request_json`.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded transient second-consumer proof over the already-proved transient compose substrate
- 2026-03-30: Phase D planner-to-presentation governance family v1 is now landed and verified. Analyzer-v2 now defines one upstream planner-to-presentation governance family over frozen composition decision artifacts: `phase4_planner_to_presentation_governance_v1`, `bounded_planner_to_presentation_readiness_v1`, `bounded_planner_to_presentation_review_v1`, and `bounded_planner_to_presentation_resolution_v1`. This slice added one fresh AOI transient compose proof bundle under `communications/`, one deterministic `planner_presentation_decision` evaluator branch inside the frozen-pack harness, one real upstream report/gate/review/resolution chain served successfully through `/v1/evaluations/governance-status/current`, and one follow-up hardening pass that tightened genealogy `planner_presentation_agreement` from count-only agreement to full intent-plus-section-payload equality.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase_d_planner_to_presentation_governance_family_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one second fresher planner-to-presentation proof campaign before Stage 15 can make a stronger claim that governance is not still tied to one proving dossier
- 2026-03-30: Phase D routing/planning governance family v1 is now landed and verified. Analyzer-v2 now defines one upstream routing/planning governance family over frozen analyzer-owned decision artifacts: `phase4_routing_planning_governance_v1`, `bounded_routing_planning_readiness_v1`, `bounded_routing_planning_review_v1`, and `bounded_routing_planning_resolution_v1`. This slice added one fresh AOI current-contract route/planning/snapshot proof bundle under `communications/`, one exported genealogy planning-snapshot proof artifact under `communications/`, and one new deterministic `routing_planning_decision` evaluator branch inside the frozen-pack harness. One real upstream report/gate/review/resolution chain is now materialized and served successfully through `/v1/evaluations/governance-status/current`.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase_d_routing_planning_governance_family_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one broader governance family over upstream planner-to-presentation composition decision surfaces before Stage 15 can make a stronger claim that governance sits on top of a more general analyzer-owned platform
- 2026-03-30: Phase D AOI standalone governance family v1 is now landed and verified. Analyzer-v2 now defines one standalone AOI-only governance family on the already-supported `aoi_exemplar` evaluator substrate: `phase4_aoi_exemplar_governance_v1`, `bounded_aoi_exemplar_readiness_v1`, `bounded_aoi_exemplar_review_v1`, and `bounded_aoi_exemplar_resolution_v1`. The existing frozen-pack harness, gate/review/resolution builders, canonical current-resolution accessor, and semantic governance-status seam all serve the new keys unchanged. One real AOI-only report/gate/review/resolution chain is now materialized and served successfully through `/v1/evaluations/governance-status/current`.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase_d_aoi_standalone_governance_family_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one broader governance family over upstream routing/planning/composition decision surfaces before Stage 15 can make a stronger claim that governance sits on top of a more general analyzer-owned platform
- 2026-03-30: Phase 4 bounded second-governance-family v1 is now landed and verified. Analyzer-v2 now defines one additional standalone genealogy-only governance family on the already-supported `genealogy_lifecycle` evaluator substrate: `phase4_genealogy_lifecycle_governance_v1`, `bounded_genealogy_lifecycle_readiness_v1`, `bounded_genealogy_lifecycle_review_v1`, and `bounded_genealogy_lifecycle_resolution_v1`. The existing frozen-pack harness, gate/review/resolution builders, canonical current-resolution accessor, and semantic governance-status seam all serve the new keys unchanged. One real second-family report/gate/review/resolution chain is now materialized and served successfully through `/v1/evaluations/governance-status/current`.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase4_bounded_second_governance_family_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one standalone AOI governance family over the already-supported `aoi_exemplar` evaluator before Stage 15 can make a stronger cross-family reuse claim
- 2026-03-30: Phase 4 bounded current-governance-status v1 is now landed and verified. Analyzer-v2 now serves one derived semantic governance-status read model at `/v1/evaluations/governance-status/current`, reuses canonical current-resolution selection for `resolution_key + gate_decision_id`, reloads and validates the linked review/gate chain fail-closed, maps adopted review disposition to analyzer-owned `effective_governance_status`, and serves the inherited resolution `scope_label`. Follow-up hardening also closed unknown-definition `500 -> 409` leakage and added `resolution_definition_version` drift checks.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase4_bounded_current_governance_status_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded second governance-family slice over a different declared pack/scope before Stage 15 can close honestly
- 2026-03-29: Phase 4 bounded disposition-resolution v1 is now landed and verified. Analyzer-v2 now persists `PersistedEvaluationDispositionResolution` objects over exact `review_decision_id`, derives the full linked review/gate chain from the referenced persisted review instead of resolver input, exposes a canonical current-resolution accessor for `resolution_key + gate_decision_id`, and exposes read-only inspection routes at `/v1/evaluations/resolutions`. The real resolution builder now materializes one passing persisted resolution over `review-decision-21edf9b955ee`.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-29_phase4_bounded_disposition_resolution_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded analyzer-owned current-governance-status seam over the current resolution/review/gate chain before Stage 15 can close honestly
- 2026-03-29: Phase 4 bounded review/disposition v1 is now landed and verified. Analyzer-v2 now persists `PersistedEvaluationReviewDecision` objects over exact `gate_decision_id`, derives gate-linked truth from the referenced persisted gate instead of reviewer input, enforces the bounded `accept / reject / waive` law fail-closed, and exposes read-only inspection routes at `/v1/evaluations/reviews`. The real review builder now materializes one passing persisted review decision over `gate-decision-745c2cb7e090`.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded analyzer-owned current-disposition resolution seam over persisted review decisions before Stage 15 can close honestly
- 2026-03-29: Phase 4 bounded release gate v1 is now landed and verified. Analyzer-v2 now persists `PersistedEvaluationGateDecision` objects over exact input `evaluation_report_id` mappings by `case_key`, inlines the bounded frozen-pack rule table used for the decision, derives `contains_live_revalidation`, rejects duplicate explicit CLI case inputs, and exposes read-only inspection routes at `/v1/evaluations/gates`. The real gate harness now materializes one passing pack-level decision over freshly generated frozen-pack reports.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-29_phase4_bounded_release_gate_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded analyzer-owned review/disposition seam over persisted gate decisions before Stage 15 can close honestly
- 2026-03-29: Phase 4 bounded governance/evaluation v1 is now landed and verified. Analyzer-v2 now persists `PersistedEvaluationReport` objects over a frozen AOI exemplar + genealogy lifecycle evidence pack, validates pinned frozen proof artifacts by SHA-256, normalizes unlike evidence paths into one shared per-check verdict substrate, and exposes read-only report inspection routes at `/v1/evaluations/reports`. The real frozen-pack harness now persists passing reports for both frozen cases.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-29_phase4_bounded_governance_evaluation_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded pack-level gate/enforcement slice over persisted evaluation reports before Stage 15 can close honestly
- 2026-03-28: Phase 3 bounded lifecycle v1 now closes honestly. The existing genealogy transient proof page has now been live-proved on the fixed saved-result target through `compose -> explicit save -> fresh-navigation reopen by session_id`, the reopened page now serves saved compose-session truth from analyzer-owned storage with zero planner/composition replay, and invalid `session_id` fails closed. Two bounded proof-time repairs were needed: a page-label fix so screenshot evidence is not mislabeled and a client-side concurrent session-fetch dedupe so React dev double-effect does not starve fresh-navigation reopen rendering.
  - Stage(s) advanced: 14
  - Evidence: `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`
  - Did strategy change? yes
  - Remaining gap: Phase 4 bounded governance/evaluation infrastructure over the now-frozen AOI exemplar and genealogy lifecycle cases
- 2026-03-28: Phase 3 bounded lifecycle v1 is now implemented and focused verification passes, but Phase 3 is not yet documentary-closed. Analyzer-v2 now has analyzer-owned `compose_session` persistence with explicit presenter save/fetch routes, Host Contract v2 now exposes lifecycle save/fetch as delivery/runtime families, and the existing non-AOI genealogy proof page can now save a composed transient surface and reopen it by `session_id` without rerunning planning or composition in code. The honest remaining gap is now one live save/reopen closeout on that same proof page, not a jump to Phase 4 governance/evaluation.
  - Stage(s) advanced: 14
  - Evidence: `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_implementation_completion.md`
  - Did strategy change? yes
  - Remaining gap: one bounded live `compose -> save -> reopen by session_id` proof plus one fail-closed invalid-session proof before Phase 3 can close honestly
- 2026-03-28: Phase 2 host-neutral transient proof is now landed, verified, and live-proved. Analyzer-v2 now exposes one analyzer-owned lowering route from persisted planning truth into the thin `compose-from-intent` request, Host Contract v2 and `taskLaunchRuntime` now expose that lowering surface as planner-advisory runtime law, and `the-critic` now has a dedicated non-AOI proof page outside the AOI page/controller stack. The live March 28 proof starts from completed genealogy saved result `proof-round4-adaptive-balance-final-1774012011`, stays on `run_detail -> route-task -> plan-task(persist_decision=true) -> planning_decision_fetch -> compose-from-intent-request -> compose-from-intent`, and records both `observed_no_executor_jobs = true` and `observed_no_aoi_proxy_compose = true`. Invalid planning identity at the lowering route also fails closed with `404`.
  - Stage(s) advanced: 13
  - Evidence: `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`, `communications/PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`, `communications/PROOF_phase2_host_neutral_transient_proof_rendered_2026-03-28.png`, `communications/PROOF_phase2_host_neutral_transient_proof_session_2026-03-28.har`, `communications/PROOF_phase2_host_neutral_transient_proof_invalid_planning_identity_2026-03-28.json`
  - Did strategy change? yes
  - Remaining gap: Phase 3 bounded lifecycle v1 on top of the now-proved transient planner-to-presentation substrate
- 2026-03-27: Phase 1C bounded router/planner generalization is now landed and verified. `route-task` can now route one bounded genealogy `saved_result` seam to advisory `planner.direct_sections_compose_handoff`, `plan-task` can now emit and persist one generic `direct_sections_composition_handoff_plan`, the analyzer-side genealogy saved-result bridge can derive 1-4 truthful direct sections from durable result truth only, and a thin fail-closed lowering harness now proves a full non-AOI planner-to-presentation chain through the existing public `compose-from-intent` boundary. The older genealogy `registered_corpus -> genealogy_execution_plan -> /v1/executor/jobs` path remains unchanged.
  - Stage(s) advanced: 7, 8, 9, 13
  - Evidence: `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
  - Did strategy change? no
  - Remaining gap: Phase 2 stronger host-neutral transient proof beyond the current AOI / `the-critic` surface
- 2026-03-27: Phase 1A bridge implementation is now landed and verified. Host Contract v2 now owns planner-advisory runtime law in the current consumer, analyzer-v2 now persists immutable planning snapshots for durable AOI planner-backed recovery, the AOI compose path now recovers by `planning_decision_id` instead of semantic `location.state`, and the transient presenter entry now runs through a shared workflow/handoff capability model with one bounded non-AOI genealogy `direct_sections` materialization path through the same executor.
  - Stage(s) advanced: 7, 9, 13
  - Evidence: `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
  - Did strategy change? no
  - Remaining gap: Phase 1C bounded router/planner generalization for one non-AOI composition-facing path, then the end-of-phase browser/harness proof
- 2026-03-27: The bounded analyzer prompt-budget repair plus guard recalibration is now sufficient for the fixed Otto Phase 0 rerun to complete honestly on the live path. Fresh run `job-744edf255ad5` passed thinker-scoped active discovery, reached durable ready presentation state, passed the completed-boundary core proof, and then passed the counted planner-primary browser proof on the real AOI V2 thematic page with explicit `Clear -> row pin -> plan-task -> compose-from-selection` continuity on the same fresh run. The explicit Phase 0 / Stage 2 decision is now `closure-grade exemplar achieved`, so the exemplar loop is closed and the main line moves to Phase 1B.
  - Stage(s) advanced: 2, 3, 5
  - Evidence: `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_active_boundary_2026-03-27.json`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_completed_boundary_core_2026-03-27.json`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_ready_manifest_2026-03-27.json`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_row_pin_2026-03-27.json`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_requests_2026-03-27.json`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_session_2026-03-27.har`
  - Did strategy change? yes
  - Remaining gap: Phase 1B host ownership decisions and contract unification before Phase 1A bridge implementation
- 2026-03-27: The bounded analyzer-side active-discovery repair is now landed. `build_discovery_summaries` now unwraps `by_ref_request_snapshot` for thinker extraction, the full affected analyzer test files pass (`84 passed`), and a fresh Otto Phase 0 rerun through the real `the-critic` route proves thinker-filtered active discovery on running job `job-226f65f43a3b`. The same rerun then stops honestly at Phase `3.0 / aoi_sin_findings / Finding Discovery` with `prompt is too long: 1037154 tokens > 1000000 maximum`, so no completed-boundary artifact, browser proof, or Stage 2 grade exists yet.
  - Stage(s) advanced: 2, 5
  - Evidence: `communications/MEMO_2026-03-27_phase0_aoi_active_discovery_repair_completion.md`, `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_revision_after_active_discovery_repair.md`, `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_active_boundary_2026-03-27.json`, `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_terminal_failure_2026-03-27.json`
  - Did strategy change? no
  - Remaining gap: one bounded Phase `3.0 / aoi_sin_findings` prompt-budget repair on the fixed Otto target, then another fresh Phase 0 rerun and honest Stage 2 decision
- 2026-03-21: round 9 closed bounded AOI serve-time renderer contract enforcement
- 2026-03-22: round 10 closed generic consumer renderer consolidation on the bounded AOI path
- 2026-03-22: round 11 closed bounded AOI compose-from-intent in analyzer-v2
- 2026-03-22: round 12 closed thin consumer transient rendering on a dedicated AOI route
- 2026-03-22: round 13 implemented source-backed transient launch from real AOI result identity; documentary proof still pending
- 2026-03-23: round 14 implemented AOI hot-path launch into the source-backed transient route; documentary proof still pending
- 2026-03-23: Stage 7 landed the AOI source-to-composition bridge behind `compose-from-source-v2`, with explicit source catalog resolution, selected/rejected rationale, deterministic materialization, and focused analyzer verification
- 2026-03-23: Stage 8 landed `POST /v1/orchestrator/route-task`, a bounded advisory router over analyzer-native AOI/genealogy downstream contracts, with saved decision artifacts and focused analyzer verification
- 2026-03-23: Stage 9 landed `POST /v1/orchestrator/plan-task`, a bounded route-plus-hydrate-plus-plan seam over analyzer-native routing and existing planner substrate, with saved planning decision artifacts and focused analyzer verification
- 2026-03-23: Stage 9 AOI handoff readiness was hardened so `ready_for_aoi_compose_handoff` now requires at least one profile-feasible AOI compose path against the live source catalog, with explicit blocked-profile reasons and refreshed proof artifacts
- 2026-03-23: Stage 10 landed `GET /v1/results/by-job/{job_id}/source-backed-readiness`, a read-only readiness contract over durable AOI/genealogy result truth that reports feasible and blocked selectors without mutating presenter artifacts, with saved readiness decision artifacts and focused analyzer verification
- 2026-03-24: Stage 11 landed bounded AOI-first semantic parent/child transient planning behind `compose-from-intent-v2` / `compose-from-source-v3`, with tree-aware analyzer contract semantics, deterministic semantic matching, real the-critic child rendering, saved proof artifacts, and focused analyzer + host verification
- 2026-03-24: Stage 11 closeout was hardened with a valid public-route fail-closed proof case and an explicit all-working-content-flat proof boundary, leaving Stage 11 cleanly closed for the bounded slice that was actually scoped
- 2026-03-24: Stage 12 landed an explicit served-intent renderer-law policy across shared manifest/page/view assembly seams, with recursive final-boundary enforcement, explicit support-intent non-strict routing, one strict genealogy served mode, shadow coverage for the remaining genealogy runtime modes, and a corrected `POST /v1/presenter/compose -> 409` error path
- 2026-03-24: Stage 12 closed cleanly after broader verification (`417 passed, 3 failed`) confirmed the remaining failures were pre-existing database-state and variant-generation issues rather than served-intent renderer-law regressions
- 2026-03-24: Stage 13 first slice landed a typed Host Contract v1 plus generated JSON artifact, AOI readiness-backed source launch, genealogy readiness-backed blocked-mode fallback over the shared workspace hook, and broader shared-client adoption across the-critic proof seams, with focused host verification (`129 passed`)
- 2026-03-24: Stage 13 post-review closure corrected the AOI source-backed proxy contract inputs, fixed blocked genealogy lazy single-view fallback to use effective display mode, refreshed the generated Host Contract v1 artifact, and reran focused host verification (`131 passed`)
- 2026-03-24: Stage 8/9 host adoption landed in the current consumer as a bounded AOI planner-backed handoff seam and a bounded genealogy registered-corpus task-planned execution seam, with explicit host-boundary enforcement, non-URL AOI task handoff, and focused frontend/backend verification (`165` frontend tests, `38` backend tests)
- 2026-03-26: Stage 5 source-content identity repair landed in `analyzer-v2`: the AOI thematic-synthesis contamination vector was removed, AOI normalization now suppresses contradictory structured provenance while flagging residual identity contradiction explicitly, focused analyzer verification passed (`111 passed`), and the recovered execution-backed run was traced honestly enough to show that a fresh post-fix rerun is still required
- 2026-03-24: Stage 8/9 post-review closeout carried analyzer-approved AOI allowed/blocked profile law through the compose-page handoff, fail-closed blocked planner-backed autostarts after navigation, added direct runtime/component/backend negative-path coverage for `unsupported`, `insufficient_context`, and bad genealogy followup contracts, and reran verification (`171` frontend tests, `40` backend tests)
- 2026-03-24: Stage 13 Tier A implementation landed in `aoi-canary` as a result-contract-first live path over `result_discovery -> result_manifest -> result_presentation`, with a typed local result client, reducer-driven live states, no silent artifact fallback, and focused canary plus analyzer contract verification (`13` canary tests, `1` analyzer contract test)
- 2026-03-24: Stage 13 Tier A live proof closeout captured a real `aoi-canary` browser-network ready-state seam over `result_discovery -> result_manifest -> result_presentation`, a `discovery_empty` negative proof with no silent artifact fallback, and explicit evidence that `presenter/page` is absent from the success path; the local round-5 dossier target remains a contract-seam proof rather than a stronger preparation/polish-quality proof
- 2026-03-24: Stage 3/4 Milestone A landed a planner-primary AOI compose-through-selection proof path in `the-critic`, a bounded LLM-first AOI selector inside `plan-task`, a new `compose-from-selection` presenter contract, explicit `aoi_selection_blocked` outcomes, and post-review hardening for blocked-path selector provenance plus strict rejected-source coverage, with focused analyzer and host verification (`53` analyzer tests, `67` frontend tests, `42` backend tests)
- 2026-03-23: duplicate canonical roadmap draft deprecated in favor of this file; upstream planning stages revised to reflect the existing orchestrator substrate rather than a fictional greenfield gap

### Decision revisions

- 2026-04-03: The bounded Phase E genealogy `genealogy_idea_evolution` first-hop affordance eligibility slice is now complete. In `analyzer-v2`, `derive_first_hop_affordance(...)` now has one bounded second eligibility branch for the `genealogy_idea_evolution` / `concept_synthesis` / leaf case, while the migrated-family predicate stays unchanged and workflow gating remains upstream through the existing `enabled` path. The landed contract is deliberately generic-only: `capturable = true`, `allowed_destinations = ["arsenal", "research_todo"]`, and no `specialized_family`. Focused closeout also added the direct policy unit, presenter-path positive and negative coverage, and transient shared-derivation proof. This removes the real blocker that made the earlier host-only `IdeaEvolutionRenderer` scope dishonest. The next honest gap is now back on the host side: whether `IdeaEvolutionRenderer` can consume the already-landed `currentRendererCapture` seam plus the now-truthful generic first-hop affordance without widening semantics or overclaiming generic law.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded host-only `IdeaEvolutionRenderer` first-hop capture-alignment slice on `genealogy_idea_evolution`, reusing the landed helper seam, keeping idea-card coverage narrow, and deferring generic renderer-package law, non-AOI read-side truth surfacing, backend changes, and broader genealogy cleanup  
- 2026-04-03: The bounded Phase E current-renderer selection-emission parameterization slice is now complete. On the Critic side, the three already-proved current custom renderers (`AoiSinFindingsRenderer`, `AoiThemeFindingsMiniCardList`, and `SynthesisRenderer`) now share one narrow internal helper seam, `currentRendererCapture.ts`, that centralizes runtime-resolution and the shared `CaptureSelection` shell without forcing unified identity semantics, preview logic, or generic renderer-package law. The helper stays deliberately small: it only reads already-threaded capture runtime config, gates on generic first-hop capturability plus configurable workflow/job requirements, and assembles only the shared selection shell. The final closeout preserved the one behaviorally important AOI exception: `AoiSinFindingsRenderer` still allows capture when `_workflowKey` is missing and still emits `source_workflow_key: undefined` rather than suppressing capture. Follow-up scope review then surfaced one real blocker on the intended next renderer: `genealogy_idea_evolution` still does not receive analyzer-owned `first_hop_affordance`, so a host-only helper adoption there would currently fail closed and hide the existing buttons. The next honest code gap is therefore no longer immediate host adoption on that renderer. It is one bounded analyzer-side eligibility slice that makes `genealogy_idea_evolution` genuinely first-hop-affordance-eligible before the host follow-on.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-03_phase_e_current_renderer_selection_emission_parameterization_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded analyzer-side first-hop affordance eligibility slice for `genealogy_idea_evolution`, staying view-specific or view+engine specific, keeping semantics generic-only, and deferring the host helper adoption, generic renderer-package law, genealogy read-side truth surfacing, backend/analyzer changes, and broader genealogy cleanup  
- 2026-04-03: The bounded Phase E genealogy `genealogy_portrait` first-hop capture-alignment slice is now complete. On the Critic side, `SynthesisRenderer` now consumes analyzer-owned generic first-hop capturability and config-threaded workflow/view provenance instead of relying only on host-local unconditional capture assumptions. The landed slice stayed intentionally narrow: only `exec_summary`, `portrait`, and `key_findings` are capturable; `genealogy_job_id` remains intact; `entity_id` remains job/run identity only; and the browser proof stopped at `CaptureActionBar` handoff rather than claiming backend or read-side semantics. The closeout also clarified the strategic meaning honestly: the value here is surface-family breadth on one live non-AOI current renderer, not deep contract consumption or generic law extraction. The next honest code gap after that slice was therefore not another AOI refinement. It was whether the already-proved current-renderer consumers now justified one smallest honest shared selection-emission parameterization seam.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap at that point: scope and execute one bounded host-only current-renderer selection-emission parameterization slice over the three already-proved current custom renderers, staying below generic renderer-package law and below `IdeaEvolutionRenderer` broadening  
- 2026-04-04: The bounded Phase E genealogy V2 idea-evolution first-hop capture-alignment slice is now complete. On the Critic side, `genealogy_idea_evolution` now consumes the already-landed `currentRendererCapture` seam plus analyzer-owned generic first-hop capturability on idea cards only, with helper-built `context_title`, preserved `genealogy_job_id`, and renderer-local `entity_id = idea.idea_id`. The implementation stayed deliberately narrow: no analyzer change, no backend change, no read-side status work, and no coverage broadening beyond existing idea-card buttons. The next honest code gap is therefore no longer another current-renderer outlier. It is whether the now-four-adopter `currentRendererCapture` seam should remain Critic-local or is honest enough for bounded promotion beyond the host without false generic renderer-law or unified identity claims.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-04_phase_e_genealogy_v2_idea_evolution_first_hop_capture_alignment_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and evaluate one bounded current-renderer shared-seam promotion-readiness slice over `currentRendererCapture` and its four adopters, staying below generic renderer-package law, automatic package extraction, unified identity semantics, destination policy depth, and read-side status expansion  
- 2026-04-04: The bounded Phase E current-renderer shared-seam promotion-readiness slice is now complete. The code-backed verdict is intentionally not a rubber stamp: `currentRendererCapture` is not honest for shared-package promotion unchanged because it carries Critic-local typed `CaptureSelection`, `_firstHopAffordance` fail-closed gating, and workflow/job policy that the shared package does not currently share. But the calibration also identified a smaller reusable layer as the next honest extraction candidate: one package-neutral raw capture-base shell aligned to `renderers-ui`'s existing `config._onCapture` plus `Record<string, unknown>` architecture. The next honest cross-repo move is therefore not helper promotion. It is one bounded `renderers-ui` generic capture-base shell extraction slice that keeps first-hop/workflow policy, `source_workflow_key`, `genealogy_job_id`, and renderer-specific identity/preview law local.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-04_phase_e_current_renderer_selection_emission_shared_seam_promotion_readiness_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded `renderers-ui` generic capture-base shell extraction slice, staying below unchanged helper promotion, generic renderer-package law, unified identity semantics, destination policy depth, and read-side status expansion  
- 2026-04-04: The bounded Phase E `renderers-ui` generic capture-base shell extraction slice is now complete. In `renderers-ui`, one smaller internal raw capture-base utility now exists in real package code and is adopted by the bounded top-level trio of `AccordionRenderer`, `CardRenderer`, and `CardGridRenderer`. The implementation preserved package-native behavior exactly: raw `captureMode && onCapture` gating only, raw string-or-default semantics, `>` title composition, no empty-segment filtering, and raw `captureEntityId || captureJobId || ''` identity fallback when no explicit entity is supplied. The slice stayed strictly below Critic-local law: no `currentRendererCapture` promotion, no `_firstHopAffordance`, no workflow/job requiredness, no `source_workflow_key`, no `genealogy_job_id`, and no typed host `CaptureSelection` import. The result is a real top-level package pilot, not package-wide capture convergence. `SubRenderers` and the nested forwarding asymmetries remain deliberately deferred.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-04_phase_e_renderers_ui_generic_capture_base_shell_extraction_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded `renderers-ui` `SubRenderers` capture-base shell adoption slice, staying below forwarding normalization, package-wide convergence claims, generic renderer-package law, Critic typing, host first-hop/workflow policy, and analyzer/backend widening  
- 2026-04-04: The bounded Phase E `renderers-ui` `SubRenderers` capture-base shell adoption slice is now complete. In `renderers-ui`, the already-landed smaller internal raw capture-base utility is now adopted across the eight current inline capture-enabled `SubRenderers` builders: `DefinitionList`, `MiniCardList`, `ComparisonPanel`, `IntensityMatrix`, `MoveRepertoire`, `DialecticalPair`, `RichDescriptionList`, and `PhaseTimeline`. The implementation remained a package-local mechanical refactor only. It preserved the current raw gate, raw string-or-default semantics, `>` title composition, no empty-segment filtering, deeper 2/3/4-segment title chains, explicit-entity-first identity precedence, and the current forwarded defaults already seen on nested paths. It did not normalize forwarding asymmetries, did not widen package law, and did not import Critic-local first-hop/workflow/type semantics into `renderers-ui`. The result is stronger package-base reuse on the dominant current inline builder surface, not broader nested runtime convergence.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-04_phase_e_renderers_ui_subrenderers_capture_base_shell_adoption_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded nested capture forwarding-normalization decision slice to determine whether current forwarded defaults are already sufficient before lean `Close Read V1` scoping, or whether one bounded normalization patch is still required first  
- 2026-04-04: The roadmap is now explicitly recalibrated toward `Close Read` as an actual near-term build target rather than only a distant proving-ground abstraction. This does not reverse the current next code move. It sharpens its purpose. The honest corridor is now: finish the dominant deferred `SubRenderers` capture-base adoption surface, decide whether one bounded forwarding-normalization slice is still required as the last clear package-internal capture-runtime gate, and then scope a lean `Close Read V1` product memo bounded to runtime-real first-hop operations and current real destinations only. That product memo must still resolve host-delivery posture and app-layer first-hop eligibility explicitly, because package substrate convergence alone does not settle them. This keeps the product vector explicit without pretending that destination lifecycle, workflow-neutral taxonomy, Book Modeler integration, full super-app generality, or generic renderer-package capture law are ready now.  
  - Stage(s) advanced: post-15 / Phase E strategic calibration  
  - Evidence: `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: resolve the remaining forwarding-normalization decision gate honestly, then scope one lean `Close Read V1` memo that is explicit about host-delivery posture and app-layer first-hop eligibility before any larger destination-lifecycle or taxonomy push  
- 2026-04-04: The bounded Phase E nested capture forwarding-normalization decision slice is now complete. The decision was grounded in direct inspection of the current package forwarding sites, the package-native `captureBase` shell, near-term genealogy surfaces that materially matter for a lean `Close Read` path, and the host seams that define the boundary of package sufficiency. The verdict is not `good enough`. `AccordionRenderer` still drops `_captureSourceType` and `_captureEntityId`, which degrades provenance truth on genealogy nested accordion captures by falling back to package defaults. `CardRenderer` still forwards no capture runtime on any nested subsection dispatch branch, which functionally removes nested capture availability on real current surfaces such as `genealogy_per_work_scan`. So the package-internal gate is now closed, but the answer is `patch required`, not `Close Read V1 next`. This still does not settle packed-host integration readiness, host-delivery posture, app-layer first-hop eligibility, or generic renderer-package capture law.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_decision_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded nested capture forwarding-normalization implementation slice, then revisit lean `Close Read V1` scoping with host-delivery posture and app-layer first-hop eligibility still explicit  
- 2026-04-04: The bounded Phase E nested capture forwarding-normalization implementation slice is now also complete in local `renderers-ui` source. `AccordionRenderer` now reads and forwards `_captureSourceType` / `_captureEntityId`, `AccordionRenderer` now threads capture runtime through the previously missing `nested_sections` and fallback `GenericSectionRenderer` paths, `CardRenderer` now builds and forwards subsection capture runtime across its subsection dispatch branches, and `GenericSectionRenderer` now accepts bounded pass-through `captureConfig`. The remaining live consequence is no longer missing package-source behavior. It is that Critic still consumes a stale packed `@the-syllabus/analysis-renderers` artifact via its `0.6.5` local tarball dependency, so the installed package under `node_modules` still reflects the older omission paths.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-04_phase_e_renderers_ui_nested_capture_forwarding_normalization_implementation_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded `renderers-ui` release-artifact refresh plus focused Critic host-verification slice, then revisit lean `Close Read V1` scoping with host-delivery posture and app-layer first-hop eligibility still explicit  
- 2026-04-04: The bounded Phase E `renderers-ui` release-artifact refresh plus focused Critic host-verification slice is now also complete. The already-landed forwarding patch is now live on the real host path through a traceable `0.6.6` packed artifact, Critic now consumes that refreshed tarball through both manifest and lockfile, the installed package under `node_modules` reflects the forwarding additions, and the two material nested genealogy consequences are re-proved on the real installed package path through `genealogy_target_profile` and `genealogy_per_work_scan`. The renderer-substrate corridor is therefore no longer blocked by either package-source drift or packed-host drift. The next honest move is now product scoping: one lean `Close Read V1` memo grounded in current real first-hop operations, current real destinations, and already-proved surfaces, while explicitly resolving host-delivery posture and app-layer first-hop eligibility policy rather than pretending the substrate alone settles them.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-04_phase_e_renderers_ui_release_artifact_refresh_and_critic_host_verification_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope one lean `Close Read V1` memo that chooses a bounded host-delivery posture, a bounded initial surface set, and an explicit app-layer first-hop eligibility policy while leaving destination-lifecycle unification, workflow-neutral taxonomy, Book Modeler, generic renderer-package law, and multi-user architecture deferred  
- 2026-04-05: The bounded `Close Read V1` product memo is now complete, and the next product recalibration memo now also freezes the first honest multi-engine `Close Read V1.5` boundary. The genealogy-first pilot is still treated as a successful bounded corridor proof, not as a mistaken slice. But `Close Read` is no longer read as “the genealogy pilot page only.” It is now frozen as a Critic-hosted umbrella area with family-specific pages, first admitting genealogy and `anxiety_of_influence_thematic_single_thinker`, while explicitly deferring AOI compose-from-intent, logic/premise-scrutiny admission, generic cross-family operation law, and standalone-host questions. The next honest move is therefore no longer another product-boundary memo. It is one bounded `Close Read V1.5` coexistence implementation scope over umbrella routing/nav, genealogy + AOI coexistence, the shared baseline of result-backed reading/work plus capture-and-route into `Arsenal` / `Research todo`, and family-specific page bodies.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`; `communications/MEMO_2026-04-05_close_read_post_v1_recalibration_multi_engine_boundary.md`; `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded `Close Read V1.5` coexistence tranche that makes `Close Read` an umbrella area with family-specific genealogy and AOI pages while preserving the shared capture/provenance baseline and deferring AOI compose-from-intent, broader family admission, and standalone-host questions  
- 2026-04-03: The bounded Phase E AOI V2 mixed-surface nested-finding consumer proof slice is now complete. On the Critic side, `aoi_by_theme` now has one bounded dispatcher-plus-shim path that consumes generic whole-view `FirstHopAffordance` plus nested `finding_id` on the findings-bearing family only, creates correct thematic-finding `CaptureSelection` objects, preserves inherited accordion header behavior, and keeps out-of-scope adaptive families unchanged. The final closeout also corrected the one remaining local-host risk on that shim path: non-findings subsection renderers now resolve through Critic's local sub-renderer registry rather than the package resolver directly. The next honest code gap is therefore no longer another AOI mixed-surface question. It is whether one live current non-AOI V2 surface, `genealogy_portrait`, can consume the already-landed analyzer-owned generic first-hop contract and truthful workflow provenance instead of relying on host-local unconditional capture assumptions.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-03_phase_e_aoi_v2_mixed_surface_nested_finding_consumer_proof_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded non-AOI current-V2 first-hop capture-alignment slice on `genealogy_portrait`, staying host-only in Critic, using already-threaded `_firstHopAffordance` and `_workflowKey`, and deferring `IdeaEvolutionRenderer`, generic custom-renderer law, non-AOI read-side status surfacing, and analyzer/back-end changes  
- 2026-04-03: The bounded Phase E AOI V2 capture-status/provenance surfacing slice is now complete. On the Critic side, the already-proven AOI `aoi_by_sin_type` line now has a project-scoped read seam, `POST /api/captures/status/by-entity`, plus one local hook and one local renderer read path that can surface passive per-card capture truth (`In Arsenal`, `Research Answered`, `Research To-Do`) after reload or revisit using persisted `entity_id` and `source_workflow_key`. The final closeout fixed the only meaningful implementation gap in the first pass: equivalent rebuilt `entity_ids` sets in the host hook no longer refetch the same payload on every successful rerender. The next honest code gap is therefore no longer read-side visibility on the same pure findings surface. It is whether one current mixed AOI V2 surface, `aoi_by_theme`, can consume the already-landed generic whole-view affordance plus nested `finding_id` contract on thematic findings without overclaiming whole-view specialization or generic renderer-package law.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_status_provenance_surfacing_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded AOI V2 mixed-surface nested-finding consumer proof on `aoi_by_theme`, staying local to the findings-bearing family, keeping whole-view semantics generic-only, and deferring generic renderer-package law, mixed-surface status surfacing, non-AOI proof, and analyzer semantic broadening  
- 2026-04-03: The bounded Phase E AOI V2 capture-provenance persistence slice is now complete. On the Critic side, the already-proven AOI `aoi_by_sin_type` capture-selection line now preserves analyzer `entity_id` and truthful workflow-type provenance through capture creation, capture persistence, routed Arsenal and research-todo source snapshots, and the direct AOI research-question save path. The final closeout fixed the only serious gap in the first pass: direct `POST /api/research-todos` with `capture_id` now normalizes `workflow_key`, `source_workflow_key`, and `entity_id` from the persisted linked capture rather than trusting client-supplied provenance, and `ResearchFlagDialog` no longer issues a follow-up `/captures/{id}/to-research-todo` call that could create a second todo. The next honest code gap is therefore no longer write-side provenance truth. It is whether the current Critic runtime can read that persisted truth back onto the same bounded AOI V2 surface after reload or revisit without pretending generic capture-status law is solved.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded AOI V2 capture-status/provenance surfacing slice on the same `aoi_by_sin_type` line, using persisted `entity_id` and `source_workflow_key` to surface passive card-level destination/status truth after reload or revisit while keeping generic `/api/captures/by-job` generalization, workflow-neutral destination semantics, mixed-surface consumer work, and analyzer semantic broadening deferred  
- 2026-04-03: The bounded Phase E AOI V2 sin-findings capture-selection consumer proof is now complete. On the Critic side, one current specialized V2 findings surface, `aoi_by_sin_type`, now consumes the already-landed analyzer contract (`first_hop_affordance` plus `finding_id`) through the real shared V2 renderer-config seam and one local renderer override, and turns eligible card clicks into well-formed `CaptureSelection` objects handed off into the shared `CaptureActionBar`. The proof is intentionally narrow and honest: it proves capture-selection sufficiency only, not end-to-end Arsenal mutation parity, generic renderer-package consumption, or mixed-surface consumer behavior. The next honest code gap is therefore no longer whether a live host can do something real with the analyzer contract at all. It is whether the existing `/captures` pipeline can preserve analyzer item identity and truthful analysis workflow provenance once that now-proven selection is submitted.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-03_phase_e_aoi_v2_sin_findings_capture_selection_consumer_proof_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded capture-provenance persistence slice on the same AOI `aoi_by_sin_type` line, carrying `entity_id` and truthful source workflow provenance through the current `/captures` create-and-route seam while keeping generic capture-status law, workflow-neutral mutation taxonomy, mixed-surface consumer work, and analyzer semantic broadening deferred  
- 2026-04-02: The Phase E findings-bank Arsenal-promotion affordance tranche is now complete. `FirstHopAffordance` can now carry one bounded specialized semantic family, `findings_bank_arsenal_promotion_v1`, on the pure AOI `aoi_by_sin_type` surface only, while the generic first-hop contract (`capturable` plus bounded `allowed_destinations=["arsenal","research_todo"]`) remains unchanged everywhere else. The supporting AOI contract now carries `finding_id` on `aoi_by_sin_type` cards, both identity serializers exclude unset `specialized_family` to avoid generic hash churn, and the closeout fix now fail-closes specialization on actual payload truth: older or malformed `aoi_by_sin_type` payloads stay generic unless every emitted card proves a non-empty `finding_id`. The next honest code gap is no longer another pure-surface specialization. It is whether analyzer-v2 can carry minimal finding-level handles on one mixed analyzer-known AOI surface, `aoi_by_theme`, without overclaiming whole-view findings semantics or inventing a generic item-level affordance subsystem.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded mixed-surface nested finding-handle propagation slice on AOI `aoi_by_theme`, while keeping whole-view specialization, destination lifecycle, outline-routing, and generic item-schema work deferred  
- 2026-04-02: The Phase E job-backed first-hop affordance propagation tranche is now complete. The bounded first-hop affordance contract is now shared across transient and job-backed presenter surfaces via `FirstHopAffordance`, and the same narrow semantic family (`capturable` plus bounded `allowed_destinations=["arsenal","research_todo"]`) now survives on `TransientIntentView`, `ViewPayload`, `EffectiveManifestView`, `PagePresentation.views`, and `EffectivePresentationManifest.views`. The shared job-backed helper now runs in `_prepare_page_payloads(...)`, the non-composition lazy single-view path was explicitly brought into parity, `_manifest_identity_row(...)` now carries the field for contract-hash honesty, `presentation_content_hash` still ignores it as non-content metadata, and `_diff_snapshots(...)` now makes affordance-only contract changes visible rather than silent. The next honest code gap is no longer surface propagation. It is one output-specific first-hop affordance family on one analyzer-known analytical surface.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded findings-bank Arsenal-promotion affordance slice on the AOI `aoi_by_sin_type` surface while destination lifecycle, broader taxonomy work, and host-UX expansion stay deferred  
- 2026-04-02: The Phase E first-hop affordance/routing addendum on the transient compose line is now complete. `ComposeFromIntentResponse.presentation.views` can now carry one bounded analyzer-owned first-hop affordance object on the approved analytical leaf surfaces only: AOI `source_profile`, AOI `source_selection`, and genealogy `direct_sections`. The landed field family is intentionally narrow (`capturable` plus bounded `allowed_destinations=["arsenal","research_todo"]`), parent/container views remain unannotated, AOI `direct_sections` was corrected back out of scope during closeout, and the representative composition matrix proof bundles plus transient hash law were refreshed so the new field is contract-honest rather than a ghost annotation. The next honest code gap is no longer whether analyzer-v2 can attach first-hop affordance hints at all. It is whether the same already-landed bounded hint family can propagate onto the mainstream job-backed presentation line without changing the semantics or pulling host UX upstream.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded job-backed first-hop affordance propagation slice over `ViewPayload`, `EffectivePresentationManifest`, and `PagePresentation`, while keeping richer output-specific semantics and destination lifecycle deferred  
- 2026-04-02: The Phase E bridge-hint consolidation tranche is now complete. The migrated AOI and genealogy bridge-backed paths no longer carry independent bridge-local semantic-role literals: AOI source-bridge candidates now derive `composition_role_hint` from canonical capability metadata before artifact/report lookup, and genealogy saved-result traces now derive `role_hint` from canonical capability metadata after the concrete matched row is known, including legacy-key matches. The downstream compose matcher, dynamic prompt seam, and view generation seam remain intentionally unchanged in this cleanup slice. The next honest code gap is no longer bridge authority cleanup; it is one bounded first-hop affordance/routing addendum on the transient compose line itself.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-02_phase_e_bridge_hint_consolidation_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bounded analyzer-side first-hop affordance/routing addendum over transient compose surfaces only, starting with surface-level `capturable`, `commentable`, and bounded `allowed_destinations` hints while destination lifecycle stays deferred  
- 2026-04-01: The Phase E composition metadata extraction tranche is now complete. Analyzer-v2 now carries a shared `CompositionRole` type, canonical capability-definition `composition_role` metadata for the proved AOI/genealogy engine family, and a presenter-side role registry for pattern / stance / description / rationale. `compose_from_intent.py` now resolves migrated semantic role from canonical capability metadata for canonical and legacy keys, fails closed when migrated-family metadata is absent or invalid, and no longer relies on `_ROLE_FROM_ENGINE_KEY`. Alias-aware hardening also now reaches the adjacent dynamic-prompt and view-generation seams touched by the tranche. The next honest code gap is no longer extraction itself; it is the remaining bridge-local duplication of semantic-role hints in the AOI source bridge and genealogy saved-result bridge.  
  - Stage(s) advanced: post-15 / Phase E  
  - Evidence: `communications/MEMO_2026-04-01_phase_e_composition_metadata_extraction_v1_completion.md`  
  - Did strategy change? yes, slightly  
  - Remaining gap: scope and execute one bridge-hint consolidation slice so the migrated line stops carrying bridge-local semantic-role authority before analyzer-side affordance/routing attachment begins  
- 2026-04-01: The runtime-first Close Read operations and routing inventory companion tranche is now complete. It confirms that the strongest current downstream product evidence is not just rendered analysis but concrete first-hop operations and artifact-routing seams already embodied in `the-critic`, while destination-internal lifecycle needs separate treatment and `analyzer-mgmt` remains secondary intent/schema evidence only. This strengthens the case for `Close Read` as the best current flagship proving ground, but it does not change the immediate analyzer-side code move at that point in the sequence. The next honest implementation step remained composition metadata extraction first, with analyzer-side affordance/routing attachment deferred until after the composition authority line was cleaned.
  - Stage(s) advanced: post-15 / Phase E companion discovery
  - Evidence: `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
  - Did strategy change? yes, slightly
  - Remaining gap at that time: execute extraction, then scope one post-extraction affordance/routing addendum over first-hop operations only
- 2026-04-01: The bounded Phase E proof-only lifecycle `source_selection` slice is now complete. The standalone proof harness can now carry AOI `source_selection` through `compose -> explicit save -> fresh-navigation reopen by session_id` on the existing analyzer-owned compose-session seam, because `compose-from-selection` now returns one analyzer-owned `persistable_compose_request` field carrying the exact lowered `ComposeFromIntentRequest` used for composition. The harness persists that exact lowered request plus raw compose response and truthful provenance (`planning_decision_id`, `source_v2_job_id`), then reopens through one saved-session GET with zero second compose calls. This does not yet mean source-profile lifecycle is solved, generic request-family persistence exists, or analyzer save-store validation enforces `compose_request == persistable_compose_request` whenever present. The next honest Phase E question is therefore no longer AOI `source_selection` lifecycle. It is whether lifecycle should broaden any further on the proof-only line, especially to source-backed `source_profile`, or whether lifecycle broadening should pause until the analyzer save contract is cleaner and more general.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope one explicit post-source-selection lifecycle decision slice on the proof-only line, including whether source-backed `source_profile` lifecycle is honest on the current save seam and whether analyzer-side persistence hardening should land first
- 2026-04-01: The interface-first strategy review tightened the next move again. The renderer-family direction is still strategically correct, but current composition remains too workflow-shaped to jump straight to taxonomy design or further lifecycle widening. The next honest Phase E step is therefore one analyzer-side, behavior-preserving composition metadata extraction tranche over the currently proved engine set: move the first hard-coded role / pattern / stance maps out of `compose_from_intent.py` and into metadata, preserve existing runtime behavior, and keep host/harness code unchanged. This is the right prerequisite before stronger output-family taxonomy claims or any further source-profile lifecycle broadening.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one behavior-preserving composition metadata extraction slice over the currently proved engine set
- 2026-04-01: The bounded Phase E transient consumer identity plurality slice is now complete, so the honest next Phase E variable is no longer proof-only consumer identity on the standalone harness line. The next bounded variable is whether the already-proved analyzer-owned `direct_sections` lifecycle law can survive the standalone proof-only harness boundary with explicit `session_id` identity and zero recomputation on reopen. This is stronger than the March 28 current-consumer lifecycle proof because it re-proves the same law through the thinner standalone harness, while still staying smaller than any source-selection lifecycle widening because the public compose-session save seam remains `ComposeFromIntentRequest`-shaped in `src/presenter/schemas.py`.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-04-01_phase_e_transient_consumer_identity_plurality_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one standalone-harness lifecycle proof on the `direct_sections` seam
- 2026-03-31: The bounded Phase E proof-only transient consumer and minimal harness slice is now complete, so the honest next Phase E variable is no longer harness boundary. The next bounded variable is consumer-identity plurality at the hard-coded analyzer admission layer: whether one additional proof-only consumer identity can ride the same standalone harness and same already-proved AOI `source_selection` plus genealogy `direct_sections` seams, while `source_profile` stays fail-closed and lifecycle still stays out of scope.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-31_phase_e_transient_proof_harness_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded consumer-identity plurality slice over the existing standalone proof harness
- 2026-03-31: The bounded Phase E `aoi-canary` transient second-consumer surface is now complete across AOI `source_selection`, AOI `source_profile:dossier`, AOI `source_profile:comparison`, and one bounded non-AOI genealogy `direct_sections` path. The honest next Phase E variable is therefore no longer more route or preset broadening inside the same AOI-branded shell. It is whether the already-proved transient substrate can now be consumed by one proof-only transient consumer contract plus one minimal harness over AOI `source_selection` and genealogy `direct_sections`, without depending on the `aoi-canary` repo and without reopening generic consumer registration prematurely.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-31_phase_e_aoi_canary_genealogy_direct_sections_second_consumer_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: now superseded by the proof-only transient consumer and minimal harness completion
- 2026-03-31: The bounded Phase E `aoi-canary` / AOI `source_profile:dossier` second-consumer slice is now complete, so the program no longer has only one AOI transient route family live-proved on the second consumer. The current honest bounded claim is stronger but still not full AOI profile-set generality: `aoi-canary` now live-proves AOI `source_selection` and AOI `source_profile:dossier`, while `source_profile:comparison` remains fail-closed by explicit analyzer policy and readiness truth. The next honest Phase E variable is therefore the remaining `comparison` preset on the same route family, not a premature jump to non-AOI second-consumer proof or broader consumer architecture.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-31_phase_e_aoi_canary_source_profile_dossier_second_consumer_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded `aoi-canary` / AOI `source_profile:comparison` second-consumer proof plus the matching readiness broadening
- 2026-03-31: The bounded Phase E transient second-consumer live closeout is now complete, so the `aoi-canary` / AOI `source_selection` path is no longer only a test-backed or replay-backed claim. The program now has code-backed, test-backed, and live browser/network proof for one bounded second-consumer transient seam. The next honest Phase E variable is therefore no longer evidentiary closeout on that same path. It is the remaining AOI compose-family seam still structurally tied to `the-critic`: `source_profile` via `compose-from-source` and the matching `source_backed_readiness` followup law.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-31_phase_e_transient_second_consumer_live_closeout_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded `aoi-canary` / AOI `source_profile` second-consumer proof plus the matching readiness uncoupling
- 2026-03-30: The bounded Phase E transient second-consumer implementation slice is now landed and verified, but the stronger documentary bar for that slice is not yet closed. The program now has a real analyzer-side second transient consumer admission on `aoi-canary` for AOI `source_selection`, a thin canary transient mode, and focused test-backed proof that no host-local analytical reconstruction is required on that path. But the frozen proof JSON is still deterministic replay rather than a fresh browser/network live capture because an unrelated engine-definition load error blocked the direct live probe. The next honest Phase E step is therefore not a third consumer, not a broader consumer-generalization tranche, and not more governance. It is one narrow live-proof closeout over the already-landed `aoi-canary` / AOI `source_selection` path.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_v1_implementation_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded live browser/network closeout for the already-landed second-consumer transient path
- 2026-03-30: The first bounded Phase E representative composition matrix is now complete. The program has now proven the full currently live handoff-family substrate (`source_profile`, `source_selection`, `direct_sections`) on the current transient consumer surface without runtime code changes. The next honest Phase E variable is no longer handoff-family breadth on `the-critic`; it is bounded transient second-consumer proof, with `aoi-canary` as the default target.
  - Stage(s) advanced: post-15 / Phase E
  - Evidence: `communications/MEMO_2026-03-30_phase_e_representative_composition_matrix_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded transient second-consumer proof over the already-proved transient compose substrate
- 2026-03-30: Phase D exit signal is now met in bounded form. The cross-campaign planner-to-presentation governance family is complete, so the next honest main line is no longer inside Stage 15. The next active line is Phase E generality proof, beginning with one representative composition matrix over the currently live analyzer-owned handoff families (`source_profile`, `source_selection`, `direct_sections`) on the existing consumer surface.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase_d_cross_campaign_planner_to_presentation_governance_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute the first bounded Phase E representative composition matrix
- 2026-03-30: Phase D no longer begins with “add one bounded governance family over upstream planner-to-presentation composition decision surfaces.” That slice is now complete. The next honest main line inside Stage 15 is one second, fresher planner-to-presentation governance family over a distinct paired AOI/genealogy proof campaign using the already-landed evaluator and governance substrate, not a jump to product UI, downstream enforcement, or a premature Phase E claim.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase_d_planner_to_presentation_governance_family_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one second cross-campaign planner-to-presentation governance family over a distinct paired AOI/genealogy proof bundle
- 2026-03-30: Phase D no longer begins with “add one bounded governance family over upstream routing/planning decision surfaces.” That slice is now complete. The next honest main line inside Stage 15 is one bounded governance family over upstream planner-to-presentation composition decision surfaces using the existing AOI and genealogy transient proof line, not a jump to product UI, downstream enforcement, or live-governance policy.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase_d_routing_planning_governance_family_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded planner-to-presentation composition governance family over upstream analyzer-owned decision surfaces
- 2026-03-30: Phase D no longer begins with “add one standalone AOI governance family.” That slice is now complete. The next honest main line inside Stage 15 is one bounded governance family over upstream routing/planning decision surfaces using the existing Stage 8/9 proof line, not a jump to product UI, downstream enforcement, or live-governance policy.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase_d_aoi_standalone_governance_family_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded routing/planning governance family over upstream analyzer-owned decision surfaces
- 2026-03-30: Phase 4 no longer begins with “add one bounded second governance family.” That slice is now complete. The next honest main line inside Stage 15 is one standalone AOI governance family over the already-supported `aoi_exemplar` evaluator substrate, not a jump to product UI or downstream enforcement and not a premature claim that multi-family topology alone closes Phase 4.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase4_bounded_second_governance_family_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one AOI-only standalone governance family over distinct existing AOI frozen evidence
- 2026-03-30: Phase 4 no longer begins with “add a bounded current-governance-status seam.” That slice is now complete. The next honest main line inside Stage 15 is one bounded second governance-family slice over a different declared pack/scope using the already-landed report/gate/review/resolution/status substrate, not a jump to product UI, downstream enforcement, or a broad override system.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-30_phase4_bounded_current_governance_status_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one second code-defined governance family beyond `phase4_frozen_governance_v1`
- 2026-03-29: Phase 4 no longer begins with “add a bounded review/disposition seam.” That slice is now complete. The next honest main line inside Stage 15 is a bounded analyzer-owned current-disposition resolution seam over persisted review decisions, not a jump straight to human approval UI, not a broad override product, and not a silent “latest review wins” convention.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded current-disposition resolution slice over exact `review_decision_id`
- 2026-03-29: Phase 4 no longer begins with “build a bounded release gate.” That slice is now complete. The next honest main line inside Stage 15 is a bounded analyzer-owned review/disposition seam over persisted gate decisions, not a jump straight to human approval UI and not a broad override product.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-29_phase4_bounded_release_gate_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded review/disposition slice over exact `gate_decision_id`
- 2026-03-29: Phase 4 no longer begins with “build governance reports.” That slice is now complete. The next honest main line inside Stage 15 is a bounded analyzer-owned pack-level gate over persisted evaluation reports, not a revival of the old March 19 workspace proof line and not a jump straight to human approval UI.
  - Stage(s) advanced: 15
  - Evidence: `communications/MEMO_2026-03-29_phase4_bounded_governance_evaluation_v1_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded release-gate/enforcement slice over the frozen evaluation pack
- 2026-03-28: Phase 2 now closes honestly. The program has one stronger bounded transient proof beyond the AOI page/controller path: a non-AOI genealogy saved-result proof page in the current host runtime that consumes analyzer-owned planning, persisted planning snapshots, analyzer-owned lowering, and transient presenter law without AOI proxy compose routes or `/v1/executor/jobs`. The next honest main line is now Phase 3 bounded lifecycle v1, not more proof-surface widening or premature new transient consumer registration.
  - Stage(s) advanced: 13
  - Evidence: `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`, `communications/PROOF_phase2_host_neutral_transient_proof_trace_2026-03-28.json`, `communications/PROOF_phase2_host_neutral_transient_proof_invalid_planning_identity_2026-03-28.json`
  - Did strategy change? yes
  - Remaining gap: scope and execute one bounded lifecycle v1 save/reopen slice
- 2026-03-27: Phase 1 now closes honestly. The bridge is no longer structurally AOI-only at the planner-to-presentation boundary: AOI retains the real browser-exercisable current-consumer path, and genealogy now has one bounded saved-result composition-facing planner path proved through a deliberate analyzer-side harness. The next honest main line is Phase 2 stronger host-neutral transient proof, not more current-consumer bridge reshaping.
  - Stage(s) advanced: 7, 8, 9, 13
  - Evidence: `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
  - Did strategy change? yes
  - Remaining gap: scope and execute the Phase 2 host-neutral transient proof slice
- 2026-03-27: Phase 0 now closes honestly. The frozen Stage 5 seam gate remains passed on fixture-backed evidence, and one fresh post-fix `execution_backed` Otto rerun now completes and passes the counted planner-primary browser proof on the real AOI V2 thematic path. The next honest main line is Phase 1B host ownership decisions and contract unification, not more AOI-specific repair.
  - Stage(s) advanced: 2, 5
  - Evidence: `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_terminal_state_2026-03-27.json`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_completed_boundary_core_2026-03-27.json`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_row_pin_2026-03-27.json`, `communications/PROOF_phase0_aoi_execution_backed_after_guard_recalibration_requests_2026-03-27.json`
  - Did strategy change? yes
  - Remaining gap: write and execute the bounded Phase 1B ownership/contract-unification slice before broader planner-to-presentation implementation
- 2026-03-27: After the March 27 fresh Phase 0 rerun, the remaining exemplar blocker should now be named explicitly as analyzer-side Phase `3.0 / aoi_sin_findings / Finding Discovery` prompt-budget overflow on the fixed Otto corpus. Do not reopen thinker-scoped discovery, browser-source pinning, or other host continuity work unless a later fresh rerun proves they are causally implicated again.
  - Stage(s) advanced: 2, 5
  - Evidence: `communications/MEMO_2026-03-27_phase0_aoi_active_discovery_repair_completion.md`, `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_revision_after_active_discovery_repair.md`, `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_terminal_failure_2026-03-27.json`
  - Did strategy change? yes
  - Remaining gap: bounded prompt-budget repair at Phase `3.0`, then a fresh Otto rerun and the honest Stage 2 decision
- 2026-03-23: The program should now gradually shift from downstream AOI/the-critic adoption work toward upstream planning/orchestration work. More consumer-side AOI glue is no longer the highest-leverage move.
- 2026-03-23: Future roadmap work should treat task intake, workflow routing, and engine planning as partially existing infrastructure that needs generalization and a planner-to-presentation bridge, not as a pure greenfield build.
- 2026-03-23: Stage 7 should now be treated as partially advanced, because the AOI source-to-composition bridge landed as the first real analyzer-owned planner-to-presentation slice without yet solving composition-facing task intake or general planner-driven page law.
- 2026-03-23: Stage 8 confirmed that advisory routing must speak analyzer-native downstream contracts rather than host proxy shapes; AOI `source_analysis_id` remains host preparation, not downstream analyzer contract law.
- 2026-03-23: Stage 9 confirmed that the missing seam is not direct `route-task -> plan-task`, but `route-task -> hydration -> planning decision`, and that genealogy execution plans should be normalized around the existing `WorkflowExecutionPlan` rather than a shadow planner object.
- 2026-03-23: Stage 9 AOI planning readiness must be derived from live per-profile feasibility over the resolved source catalog, not from generic source-family availability.
- 2026-03-23: Stage 10 should normalize one shared readiness shape while keeping selector law workflow-owned: AOI remains profile-based and consumer-coupled to `compose-from-source`, while genealogy readiness stays restore/runtime-based rather than pretending to be AOI-style source reconstruction.
- 2026-03-24: Stage 11 should treat transient parent tabs as analyzer-valid container payloads and host-rendered navigation shells at the same time; there is no hidden analyzer/host contract carveout for hierarchy in this slice.
- 2026-03-24: After Stage 11, the next platform-strengthening move should be Stage 12 renderer-law generalization before Stage 13 host-contract formalization; the thin-host thesis is still downstream of a stronger cross-workflow served renderer boundary.
- 2026-03-24: Stage 12 strictness must be resolved per internal served intent rather than per outer HTTP route, so multi-artifact routes and inspection/support callers can share helper code without silently inheriting the wrong renderer law.
- 2026-03-24: After Stage 12, the next missing seam is not more bespoke AOI/genealogy law, but an explicit minimal host contract over the analyzer-native run/result/readiness/transient surfaces and the host-owned project/proxy hooks that already exist implicitly today.
- 2026-03-24: The first honest Stage 13 move is a code-authoritative host contract plus bounded cross-workflow readiness adoption inside the current consumer; that improves the thin-host proof materially, but does not by itself satisfy the roadmap’s stronger second-consumer or host-neutral exit bar.
- 2026-03-24: The next honest move after the first Stage 13 slice is not Stage 14 lifecycle; it is a second Stage 13 slice that operationalizes Host Contract v1 over transient compose and executable host-surface selection strongly enough to deliver a materially harder generic-host proof without rebuilding analyzer intelligence locally.
- 2026-03-24: Stage 13 second slice made Host Contract v1 runtime-authoritative for the bounded 11-family surface set, unified transient compose into the shared host runtime, and turned the three current proof seams into executable host-surface lookup law.
  - Stage(s) advanced: 13
  - Evidence: `communications/MEMO_2026-03-24_stage13_second_slice_harder_generic_host_proof_completion.md`, `communications/PROOF_2026-03-24_stage13_second_slice_harder_generic_host_proof.md`, `communications/PROOF_stage13_second_slice_runtime_summary_2026-03-24.json`
  - Did strategy change? no
  - Remaining gap: proof is still current-consumer-only and AOI source-backed transient launch remains explicitly host-bounded
- 2026-03-24: Stage 13 Tier A is now fully closed for the bounded result-backed second-consumer slice. The `aoi-canary` implementation plus live proof artifacts are sufficient for the cheap honest second-consumer bar, so the main structural next line should now move to AOI exemplar completion rather than another Tier A closeout pass.
  - Stage(s) advanced: 13
  - Evidence: `communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_second_consumer_completion.md`, `communications/PROOF_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout.md`, `communications/PROOF_stage13_tier_a_aoi_canary_live_proof_summary_2026-03-24.json`, `communications/PROOF_stage13_tier_a_aoi_canary_ready_session_2026-03-24.har`, `communications/PROOF_stage13_tier_a_aoi_canary_discovery_empty_session_2026-03-24.har`
  - Did strategy change? yes
  - Remaining gap: Stage 13 overall remains partial because Tier B and transient/stronger host-neutral proof remain open
- 2026-03-24: Stage 3/4 AOI exemplar Milestone A is now implemented, but the broader Stage 2/3/4/5 tranche is not closed yet. The next honest move is the Stage 5 AOI exit gate, and Stage 2 should not be marked documentary-closed until that evaluation/ops pack actually lands.
  - Stage(s) advanced: 3, 4
  - Evidence: `communications/MEMO_2026-03-24_stage3_4_aoi_exemplar_cutover_completion.md`, `communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md`
  - Did strategy change? yes
  - Remaining gap: Stage 5 evaluation/ops evidence, Stage 2 documentary closure, and the remaining planner-backed continuity residuals are still open
- 2026-03-26: Once the repaired host/browser path proves the counted execution-backed AOI rerun structurally, the next blocker should be named for what it actually is: source-content integrity inside the recovered AOI payload, not “missing browser proof” anymore. Do not spend another round on browser reruns or host pinning unless the content-level source-identity contradiction is first explained or repaired.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_preflight_identity_2026-03-26.json`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_precompose_pin_2026-03-26.json`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_requests_2026-03-26.json`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_session_2026-03-26.har`
  - Did strategy change? yes
  - Remaining gap: diagnose and repair or convincingly explain the recovered-source thinker-identity drift before any honest Stage 2 closure or Tranche 3 move
- 2026-03-24: Stage 5 AOI exemplar exit gate was executed and did not pass. All four product-path cases reached planning, but the three required ready cases blocked with `llm_provider_failure`, the real blocked case returned `no_usable_source_families`, and the current AOI host surface did not stably surface blocked planner outcomes in the UI. Stage 2 therefore remains open and the next honest move is a bounded Stage 5 revision slice.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`, `communications/PROOF_2026-03-24_stage5_aoi_exemplar_eval_pack.md`, `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-24.json`, `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_revision.md`
  - Did strategy change? no
  - Remaining gap: planner-primary AOI host visibility for blocked/ready outcomes, selector/provider reliability on ready cases, Stage 2 documentary closure, and a successful rerun of the frozen Stage 5 pack before Tranche 3
- 2026-03-25: The bounded Stage 5 revision slice is now implemented. AOI selector timeout/retry/classification hardening is landed in `analyzer-v2`, AOI planner outcome retention is now structured in `the-critic`, and the follow-up tightening pass removed task-edit invalidation while adding direct coverage for the delayed initial hydrate race. Stage 5 still remains open until a live diagnostic `evolution_ready` spot-check and the same frozen four-case rerun are executed.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-25_stage5_aoi_exemplar_revision_slice_completion.md`, `communications/MEMO_2026-03-24_stage5_aoi_exemplar_revision_slice_scope.md`
  - Did strategy change? no
  - Remaining gap: live selector/provider diagnosis on the repaired path, a full rerun of the frozen Stage 5 pack, and the Stage 2 closure decision
- 2026-03-25: The Stage 5 `evolution_ready` diagnostic spot-check was executed on the repaired local path. The selector/provider repair held and planning now returns a real AOI handoff plan, but the frozen rerun was not earned because planner-backed `compose-from-selection` fails with `409 source_analysis_id does not belong to the current project + thinker context`. The next honest move is one more bounded Stage 5 identity-continuity repair slice rather than a Tranche 3 pivot.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-25_stage5_aoi_diagnostic_stop_completion.md`, `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`, `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`, `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_session_2026-03-25.har`, `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_revision.md`, `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md`
  - Did strategy change? no
  - Remaining gap: host-side AOI source identity continuity across snapshot warmup -> compose proxy validation, a successful rerun of the frozen Stage 5 pack, and the Stage 2 closure decision
- 2026-03-25: The bounded Stage 5 AOI identity-continuity repair slice is now implemented in `the-critic`. The host now repairs/persists AOI thinker identity through `v2_run_references` and warmed local snapshots, planner-backed handoff now preserves canonical `source_v2_job_id`, fail-closed `409` mismatch handling is explicit, and focused regression coverage now includes missing-row repair plus repeated latest-snapshot continuity. Stage 5 still remains open because the repaired path has not yet been re-diagnosed live after this slice and the frozen rerun still has not been reconsumed.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_completion.md`, `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md`, `communications/MEMO_2026-03-25_stage5_aoi_exemplar_diagnostic_rerun_scope.md`
  - Did strategy change? no
  - Remaining gap: one fresh `evolution_ready` diagnostic on the repaired path, then the same frozen Stage 5 rerun if that diagnostic passes, and only then the Stage 2 closure decision
- 2026-03-25: The fresh post-identity-repair `evolution_ready` diagnostic was executed on the repaired planner-backed path. The selector/provider repair held, the planner-backed path stayed on `compose-from-selection`, canonical `source_v2_job_id` was preserved, and `compose-from-source` stayed unused, but the rerun was still not earned because planner-backed compose now fails with `404 Saved AOI result not found: gen-v2-3834f733047a`. Local evidence shows the returned warmed `source_analysis_id` was not durably present in `genealogy_analyses` while sibling saves in the same window succeeded and server logs recorded `database is locked` save failures, so the next honest move is a bounded host warm-snapshot durability repair slice rather than a Tranche 3 pivot.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_diagnostic_stop_completion.md`, `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`, `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json`, `communications/PROOF_stage5_aoi_evolution_ready_diagnostic_session_2026-03-25.har`, `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_revision.md`, `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md`
  - Did strategy change? no
  - Remaining gap: host-side warm snapshot save durability / returned `source_analysis_id` truth, then one more fresh `evolution_ready` diagnostic, then only if that passes the same frozen Stage 5 rerun, and only then the Stage 2 closure decision
- 2026-03-25: Recent Stage 5 memo/completion churn should be interpreted as blocker-retirement inside one still-open exemplar gate, not as evidence that the full platform is near completion. The downstream substrate is materially real, but AOI exemplar ratification is still incomplete and Tranche 3 should stay blocked until the Stage 5 rerun actually passes.
  - Stage(s) advanced: none
  - Evidence: this roadmap memo, `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_diagnostic_stop_completion.md`, `communications/MEMO_2026-03-25_stage5_aoi_snapshot_durability_revision_scope.md`
  - Did strategy change? yes
  - Remaining gap: finish ratifying the exemplar loop before treating platform generalization as the main line
- 2026-03-25: The bounded analyzer selection-compose contract repair is now implemented, the repaired live `evolution_ready` rerun passed end to end, and the same frozen four-case Stage 5 AOI pack was rerun successfully. The Stage 5 seam gate now passes on fixture-backed evidence, but Stage 2 still remains open because no ready case has yet been intentionally upgraded to `execution_backed` or stronger. The next honest move is one bounded execution-backed `evolution_ready` proof step rather than another fixture rerun or a Tranche 3 pivot.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_completion.md`, `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_completion.md`, `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json`, `communications/PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json`
  - Did strategy change? yes
  - Remaining gap: one `execution_backed` ready AOI case on the planner-primary path, then an explicit Stage 2 closure decision while Tranche 3 stays blocked until that decision is honest
- 2026-03-25: One fresh execution-backed AOI `evolution_ready` run was launched through the real `the-critic` route and completed, but the first live proof attempt exposed two bounded seams: analyzer auto-presentation was bypassing the presentation coordinator and dropping `consumer_key`, and the-critic completed-job AOI detail responses were not backfilling a durable local snapshot `analysis_id` for fresh restorable v2 runs. Both seams are now repaired, and the fresh run `job-6ee8b0621177` is durably queryable as local AOI result `gen-v2-18853b558ef1`. Stage 2 still remains open because the counted planner-backed browser compose bundle on that fresh run has not yet been captured.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`, `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`
  - Did strategy change? no
  - Remaining gap: capture the counted planner-backed `compose-from-selection` request/HAR/screenshot on the recovered fresh run and then write the honest Stage 2 closure decision, or stop with a revision memo if that fresh browser proof fails
- 2026-03-26: The counted browser-closeout attempt on the recovered execution-backed run did not pass. The host never reached an honest pinned-row planner-primary compose proof because completed-job reads and repeated `cache-v2` requests were minting fresh local snapshot ids for the same upstream `job-6ee8b0621177`, and the AOI panel’s auto-load/latest behavior therefore could not stabilize on one durable recovered local source. Stage 2 remains open and the next honest move is one bounded host-side repair for local snapshot idempotence and stable browser-source pinning.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_revision.md`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_precompose_pin_2026-03-26.json`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_requests_2026-03-26.json`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_session_2026-03-26.har`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_state_2026-03-26.png`
  - Did strategy change? no
  - Remaining gap: make completed-run local snapshot reuse idempotent for one upstream `v2_job_id`, then rerun the counted browser closeout honestly before any Stage 2 closure decision
- 2026-03-26: The bounded host-side local-snapshot-idempotence repair is now implemented in `the-critic`. Completed-job detail, generic AOI `cache-v2`, `refresh-v2`, and `import-v2` now converge on one canonical local snapshot path under `v2_run_references`; AOI results listing prefers the canonical local row; and post-`Clear` source-backed launches now require explicit row reselection instead of silently falling back to the latest saved result. Focused route-level repeated/concurrent `cache-v2` and `refresh-v2` regressions now pass, together with the AOI panel regressions. Stage 2 still remains open because the counted planner-primary browser closeout on the repaired recovered source has not yet been rerun.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_completion.md`
  - Did strategy change? no
  - Remaining gap: rerun the counted planner-backed browser closeout on recovered source `job-6ee8b0621177`, then write the explicit Stage 2 closure decision if it holds, or stop with a fresh revision memo if a new seam appears
- 2026-03-26: The counted planner-primary browser closeout rerun on recovered source `job-6ee8b0621177` now passes structurally on the repaired host path. The AOI panel required explicit row pinning after `Clear`, repeated warmup traffic converged on the same canonical local `analysis_id`, `/compose-from-intent` preserved both ids, and the host `compose-from-selection` request body also preserved both ids while returning a `200` five-view shell. Stage 2 still remains open because the recovered AOI payload itself still carries unresolved content-level source-identity drift: the nominal Otto Neurath result preview names `john_oneill` inside Phase 1.0 and downstream report language.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_preflight_identity_2026-03-26.json`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_precompose_pin_2026-03-26.json`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_requests_2026-03-26.json`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_session_2026-03-26.har`, `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_state_2026-03-26.png`
  - Did strategy change? yes
  - Remaining gap: one bounded AOI source-content identity diagnosis/repair slice on the recovered execution-backed source before any honest Stage 2 closure or Tranche 3 move
- 2026-03-26: The bounded analyzer-side AOI source-content identity repair is now implemented. The thinker-specific `aoi_thematic_synthesis` contamination vector has been removed from the live definition and capability-history snapshot, AOI normalization now suppresses contradictory structured provenance and records explicit identity-integrity status, and focused analyzer verification now passes. The recovered execution-backed run `job-6ee8b0621177` has also been traced across plan truth, raw Phase `1.0`, stored artifacts, report payload, and presentation truth. That trace shows the current repaired contract is better for future runs, but the recovered run still is not display-safe, artifact-safe, or closure-grade because raw Phase `1.0` contradiction and downstream O'Neill-centered prose remain in stored outputs.
  - Stage(s) advanced: 5
  - Evidence: `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_completion.md`, `communications/PROOF_stage5_aoi_source_content_identity_trace_2026-03-26.json`
  - Did strategy change? yes
  - Remaining gap: one fresh post-fix execution-backed AOI rerun on the same Otto Neurath documents before any honest Stage 2 closure or Tranche 3 move

### Template for future updates

Use this exact template at the bottom of this section:

```md
- YYYY-MM-DD: [short description]
  - Stage(s) advanced:
  - Evidence:
  - Did strategy change? yes/no
  - Remaining gap:
```

---

## 14. FINAL STRATEGIC JUDGMENT

The program is not lost.

The last week was largely correct and materially productive.
It built the downstream half of the vision in a disciplined way.

But the program should now be clear-eyed about the distinction between:

- “we can compose and render one bounded AOI transient analytical experience through a thin host”

and:

- “we have built a general system that can take a task, choose engines, choose UI, and produce a bespoke analytical app with minimal app assumptions”

The first claim is now real enough to defend.
The second claim is not yet real enough to defend.

The correct next move is not to panic or reverse course.

The correct next move is:

- finish the AOI/documentary tail honestly
- then use the planner substrate that already exists to build a bounded planner-to-presentation bridge
- then generalize from AOI toward cross-workflow dynamic composition

That is how analyzer-v2 becomes the actual brain rather than just a better downstream presenter.
