# Memo: Draft Roadmap For The Next Platformization Stages

Date: 2026-03-26
Status: Draft strategic roadmap for review, not yet canonical
Audience: Human decision-makers, future Claude sessions, future Codex sessions, cross-repo implementors

## Purpose

Record a draft view of what should come next after the last five days of implementation across:

- Stage 8 / advisory task intake and workflow routing
- Stage 9 / bounded route-plus-hydrate-plus-plan normalization
- Stage 10 / cross-workflow source-backed readiness
- Stage 11 / rich semantic transient page planning
- Stage 12 / cross-workflow served renderer law
- Stage 13 first and second slices / minimal generic host contract plus runtime authority
- Stage 8/9 host adoption / real AOI and genealogy task-planned seams in the current consumer

This memo is intentionally a draft.

The goal is not to freeze strategy prematurely.
The goal is to state one plausible next-stage sequence clearly enough that it can be pressure-tested against:

- the codebase
- the roadmap trail
- the last five days of scope/completion memos
- the larger “analyzer-v2 as the brain” objective

## Current Strategic Position

The program has moved much further than a thin-host proof.

What is now materially true:

- analyzer-v2 owns bounded task routing, bounded planning, bounded readiness, bounded semantic transient composition, and explicit served renderer law
- the-critic now consumes a typed plus runtime-authoritative Host Contract v1 for the bounded run/result/readiness/transient family set, instead of relying on scattered page-local assumptions
- the Stage 8/9 host-adoption work now uses analyzer-owned `route-task` and `plan-task` in one AOI seam and one genealogy seam inside the live current consumer
- transient compose is no longer a fixture-only proof; it is source-backed, planner-aware, and reachable from a real AOI surface
- `aoi-canary` already exists as a real thin second consumer over analyzer-v2 presenter output for read-only/result-backed surfaces

What is still not true:

- there is no complete Stage 13 exit proof across the full surface set
- Host Contract v1/runtime is not the whole host-neutral story yet, because task-launch adoption currently lives beside it rather than inside it
- the transient/source-backed composition substrate is still structurally AOI-bound and `the-critic`-bound
- the planner-to-presentation bridge is still bounded and AOI-heavy on the composition side
- AOI still is not a fully task-driven exemplar loop end to end
- lifecycle law for dynamic surfaces is still intentionally unresolved
- governance, evaluation, and override seams are still too weak for broad platform claims

So the honest state is:

- the architecture is now credible
- the program is strong against the narrower UI-composition vision for one bounded slice
- the program is still incomplete against the broader analyzer-as-brain multi-app platform vision
- the next work should concentrate on the remaining structural gaps rather than add more bespoke proof tokens

A more honest progress read after the latest Stage 5 stop is:

- bounded AOI transient-composition substrate: roughly 75-85% of the way
- AOI exemplar ratification as an end-to-end platform reference: roughly 55-65% of the way
- full analyzer-as-brain multi-app platform: roughly 30-40% of the way

The memo count can make the program feel more complete than it is.
The better interpretation is that the last several slices have mostly retired blockers inside one still-open Tranche 2 gate rather than closing new higher-level platform tranches.

## Lessons From The Last Five Days

### 1. Bounded explicit contracts beat abstract platform claims

The biggest gains came from:

- `route-task`
- `plan-task`
- source-backed readiness
- served-intent renderer law
- Host Contract v1
- task-launch adoption

That is a strong signal for the next stages:

- keep adding explicit, inspectable seams
- avoid “the host is thin now” claims that are not tied to concrete contracts

### 2. The hard problem is now the bridge, not the renderer host

The renderer/consumer proof ladder is strong enough.

The remaining high-value gap is:

- how a task becomes planning truth
- how planning truth becomes presentation truth
- how that happens without host-local analytical reconstruction

More precisely, the missing bridge now includes:

- de-AOI-ing the transient/source-backed composition substrate
- de-`the-critic`-ing the transient consumer contract
- generalizing beyond AOI handoff metadata into reusable composition law
- proving at least one non-AOI composition-facing seam

### 3. AOI and genealogy together were necessary

AOI alone would have overfit to composition.
Genealogy alone would have overfit to execution.

Together they proved:

- composition-facing seams
- execution-facing seams
- shared host/runtime law
- cross-workflow readiness and renderer enforcement

That should continue to shape prioritization.

### 4. Lifecycle should remain deferred until the bridge is stronger

If lifecycle is defined too early, the program will risk solidifying semantics around bounded proof routes rather than around a genuinely reusable platform contract.

That remains the right reason to keep Stage 14 behind the next structural stages.

## Draft Next Tranches

This draft roadmap now proposes six next tranches.

They are called tranches deliberately.
They map onto the canonical stage numbers, but they are meant to describe likely near-term sequencing rather than replace the canonical numbering system.

### Tranche 1: Stage 13 Exit Tier A Using `aoi-canary`

Canonical mapping:

- Stage 13 / Minimal generic host contract

Goal:

- close the cheapest honest part of the Stage 13 exit bar using the already-existing second consumer

Why this comes first:

- `aoi-canary` already exists as a thin read-only second consumer
- the cheapest remaining proof is not hypothetical; it is to harden that consumer into a result-backed Host Contract v1 proof
- this closes a long-deferred credibility gap without requiring the transient substrate to be generalized first

Tier A scope:

- result-backed only
- read-only consumption is acceptable
- use analyzer-owned discovery/manifest/presentation seams without rebuilding workflow-specific intelligence locally

Must land:

- explicit assessment of `aoi-canary` against Host Contract v1
- one result-backed proof seam through the same analyzer-native contract families already used in the-critic
- any Host Contract v1 revision needed to make that proof honest

Must not widen:

- do not claim transient coverage yet
- do not reopen lifecycle
- do not force task-launch adoption into `aoi-canary` unless that becomes clearly necessary for the proof

Exit evidence:

- one `aoi-canary`-based second-consumer proof artifact for result-backed surfaces
- an explicit Stage 13 Tier A closure or revision memo

Current status after implementation and live proof closeout:

- the bounded `aoi-canary` implementation is now landed and documentary-closed:
  - result-contract-first live mode
  - analyzer-owned `result_discovery -> result_manifest -> result_presentation`
  - reducer-driven explicit live-state model
  - no silent artifact fallback
  - real browser-network proof for the ready-state acceptance seam
  - `discovery_empty` negative proof
- so Tranche 1 can now be treated as closed for the bounded Tier A slice
- Stage 13 overall still remains partial because Tier B transient/host-neutral proof is still open

### Tranche 2: Complete The AOI Exemplar Loop

Canonical mapping:

- Stage 3 / AOI task-driven composition
- Stage 4 / AOI source and engine-selection law
- Stage 5 / AOI evaluation and ops guardrails

Current proximity:

- Stage 3 is materially advanced because one planner-primary AOI compose-through-selection seam now exists in the current consumer
- Stage 4 is materially advanced because bounded LLM-first AOI source/product-selection law now exists in `plan-task`
- Stage 5 is now materially stronger: the analyzer-side selection-compose contract repair is landed, the repaired live `evolution_ready` diagnostic passed end to end, and the same frozen four-case Stage 5 pack has now been rerun successfully on fixture-backed evidence
- one fresh `execution_backed` `evolution_ready` AOI run has now also been launched and recovered to durable result truth, including analyzer presentation readiness and Critic local snapshot resolution
- the bounded host-side local-snapshot-idempotence repair is now landed in `the-critic`: completed-job detail, generic AOI `cache-v2`, `refresh-v2`, and `import-v2` now converge on one canonical local snapshot path, AOI results listing prefers the canonical row, and post-`Clear` source-backed launch now requires explicit reselection
- the counted planner-primary browser closeout rerun on the repaired recovered source has now been executed successfully at the structural host/product-path level
- the bounded analyzer-side source-content identity repair is now landed: the thinker-specific `aoi_thematic_synthesis` contamination vector has been removed from the live definition and capability-history snapshot, and the AOI contract now suppresses contradictory structured provenance while flagging residual identity contradiction explicitly
- the repaired trace over recovered source `job-6ee8b0621177` now shows the remaining truth clearly: the first real contradiction is raw Phase `1.0`, downstream O'Neill-centered prose still survives in the stored recovered run, and that existing run is still not `display-safe`, not `artifact-safe`, and not `closure-grade`
- the roadmap should therefore remain recalibrated, not reordered: Tranche 3 stays blocked until one fresh post-fix `execution_backed` AOI rerun on the same documents is evaluated honestly, and the Stage 2 decision is written explicitly

Goal:

- turn AOI from a strong bounded proof surface into the first genuinely task-driven exemplar app loop on top of analyzer-v2

Why this still comes early:

- AOI remains the strongest composition-facing exemplar
- it still has visible residual profile-first and host-known behavior
- evaluation and operational guardrails should be established before broader bridge generalization

Must land:

- one real AOI task-first flow, not just planner-backed handoff beside legacy controls
- bounded analyzer-owned source/profile/engine-selection law strong enough to reduce remaining AOI host-local analytical assumptions
- explicit AOI evaluation and ops guardrails:
  - launch-quality checks
  - blocked/ambiguous path visibility
  - proof-path observability
  - regression discipline around task-driven AOI behavior

Must not widen:

- do not treat AOI completion as proof that all workflows are solved
- do not turn AOI into a sprawling bespoke UI rewrite
- do not reopen lifecycle through AOI drafts/publishing by accident

Exit evidence:

- one AOI flow where task input, planning, handoff, compose, and displayed result are all visibly analyzer-driven
- saved evidence that remaining host logic is mostly shell/UX continuity rather than analytical decision-making
- a bounded AOI eval/guardrails memo proving the exemplar is stable enough to stand as a platform reference

Sequencing note:

- the AOI eval/guardrails exit here should be treated as a precondition for Tranche 3 becoming the main program line; otherwise the transient-substrate generalization work will proceed without a stable exemplar reference
- after Tranche 1 closeout and Stage 3/4 Milestone A implementation, the bounded Stage 5 revision slice is now landed in code and the first repaired-path diagnostic has been executed
- that repaired path has now been re-diagnosed successfully end to end, including preserved planner-backed `compose-from-selection`, canonical `source_v2_job_id`, and durable local warm-snapshot truth
- the same frozen four-case Stage 5 rerun has also now passed on fixture-backed evidence, so the seam gate itself is no longer the active blocker
- the bounded execution-backed proof attempt did produce one fresh completed AOI run plus two bounded recovery repairs: analyzer auto-presentation recovery and Critic live local snapshot backfill
- that host-side local-snapshot-idempotence seam is now repaired, including route-level repeated/concurrent `cache-v2` and `refresh-v2` convergence plus post-`Clear` explicit source reselection in the AOI panel
- the counted browser closeout rerun has now also been executed on the repaired recovered source `job-6ee8b0621177`, with explicit row pinning, stable host reuse under repeated `cache-v2`, preserved `source_v2_job_id`, preserved host-boundary `source_analysis_id`, and successful `compose-from-selection` request-body proof
- that rerun changed the remaining blocker: it is no longer missing browser evidence, but unresolved content-level source-identity drift inside the recovered execution-backed AOI payload
- that bounded diagnosis-and-repair slice is now implemented in `analyzer-v2`: the prompt contamination vector is removed, AOI normalization now suppresses contradictory structured provenance, and residual report-level contradiction is surfaced explicitly instead of being masked
- the recovered run trace now shows the remaining blocker honestly: the existing recovered run still carries contradictory raw Phase `1.0` identities and downstream O'Neill-centered prose, so it cannot support closure-grade Stage 2 evidence in place
- the immediate next step inside this tranche is therefore one fresh post-fix `execution_backed` AOI rerun on the same Otto Neurath documents, not another browser rerun by default, not another host repair, not a frozen-pack rerun, and not a Tranche 3 pivot
- only after that fresh post-fix rerun is graded honestly should the final Stage 2 closure decision be written
- this remains a recalibration of the immediate plan, not a pivot to a different phase or tranche order

### Tranche 3: De-AOI And De-`the-critic` The Transient Composition Substrate

Canonical mapping:

- Stage 7 / Planner-to-presentation bridge
- Stage 13 / Minimal generic host contract

Goal:

- remove the most important structural blockers that currently make transient/source-backed composition AOI-specific and `the-critic`-specific

Why this needs its own tranche:

- the reviews were right that “generic host proof” is too broad a label for the real missing work
- the real missing work is more specific:
  - transient compose still hard-locks `workflow_key`
  - transient compose still hard-locks `consumer_key='the-critic'`
  - AOI planning still mostly stops at handoff metadata rather than reusable composition law

Must land:

- a clear contract decision for transient compose consumer admission beyond `the-critic`
- at least one non-AOI or more consumer-neutral composition-facing seam
- clearer relation between Host Contract v1/runtime and the separate task-launch layer
- explicit separation of:
  - host-neutral run/result/readiness contract law
  - composition-facing transient/source-backed contract law

Must not widen:

- do not attempt arbitrary workflow generation
- do not flatten all transient composition into one vague generic endpoint
- do not pretend task-launch is already fully inside Host Contract v1 if it is not

Exit evidence:

- the transient/source-backed substrate is no longer structurally single-consumer-only
- one composition-facing proof seam no longer depends on AOI-only or `the-critic`-only law

### Tranche 4: Stage 13 Exit Tier B Plus Broader Planner-To-Presentation Proof

Canonical mapping:

- Stage 13 / Minimal generic host contract
- Stage 7 / Planner-to-presentation bridge

Goal:

- earn the stronger Stage 13 proof and move beyond the AOI-heavy bridge at the same time

Why this follows Tranche 3:

- Tier B should only be attempted after the transient/source-backed substrate is no longer structurally single-consumer-only
- once that happens, the next real platform proof is a broader planner-to-presentation seam across more than one workflow family

Tier B scope:

- include transient surfaces, not only result-backed ones
- prove either:
  - a stronger `aoi-canary` second-consumer path, or
  - a more genuinely host-neutral proof harness over the transient/source-backed seam

Must land:

- at least two workflow families using the same planner-to-presentation discipline
- one non-AOI composition-facing proof seam
- one stronger Stage 13 proof that includes transient behavior rather than only result-backed rendering

Must not widen:

- do not collapse execution planning and presentation planning into one opaque blob
- do not let “generic host proof” become a demo shell with hidden workflow intelligence

Exit evidence:

- a candid Stage 13 Tier B proof artifact
- one proof that analyzer-v2 can take task/planning truth into presentation truth across more than one workflow family without requiring workflow-specific page intelligence in the host

### Tranche 5: Define Dynamic Surface Lifecycle

Canonical mapping:

- Stage 14 / Dynamic app/session lifecycle

Goal:

- decide what dynamically composed surfaces are as runtime objects

Why this still stays behind the earlier tranches:

- lifecycle semantics should rest on proven host and planner/presentation structure
- otherwise the system risks persisting proof artifacts rather than coherent platform objects

Must land:

- explicit semantics for:
  - ephemeral launch
  - draft/session persistence
  - revisit
  - share/publish if allowed
- ownership and retention rules
- explicit separation between transient proof routes and durable user-facing dynamic surfaces

Must not widen:

- do not fold every existing result-backed presentation into the lifecycle model automatically
- do not treat “save this transient page” as sufficient lifecycle law

Exit evidence:

- one lifecycle memo with one implemented bounded path
- clear documented boundaries for what is still transient-only

### Tranche 6: Add Governance, Review, And Evaluation Infrastructure

Canonical mapping:

- Stage 15 / Governance, review, and human override

Goal:

- make dynamic planning and composition auditable enough for broad platform claims

Why this is last in this draft:

- governance matters most once the system has stronger host neutrality, a broader planner-to-presentation bridge, clearer lifecycle semantics, and an honest exemplar-evaluation baseline

Must land:

- reviewable traces for dynamic routing/planning/composition decisions
- bounded approval or inspection flows where needed
- evaluation harnesses for task-routing, planning, readiness, and composition quality
- explicit human override seams

Must not widen:

- do not invent heavyweight enterprise workflow just because the system has become more general
- do not let governance become a substitute for making the contracts themselves clearer

Exit evidence:

- a review/evals memo plus one implemented bounded governance path

## Why This Sequence, Not Another One

This revised draft makes four ordering claims:

1. close the cheap part of the Stage 13 proof first because `aoi-canary` already exists
2. finish one exemplar loop before broad generalization
3. give the transient/source-backed substrate its own de-AOI/de-`the-critic` tranche instead of hiding that work inside generic host-proof language
4. keep lifecycle and governance behind stronger structural evidence

The main alternative sequences would be:

- jump directly to lifecycle
- jump directly to broad planner-to-presentation generalization
- or claim Stage 13 exit first without first distinguishing Tier A from Tier B

This draft rejects all three.

Why not lifecycle next:

- lifecycle would lock semantics before the host-neutral/platform-neutral shape is proved

Why not broad generalization next:

- the strongest current composition exemplar is still AOI
- finishing that loop gives the program a cleaner reference point for what generalization should preserve

Why not a monolithic Stage 13 exit first:

- because `aoi-canary` makes result-backed host-neutral proof relatively cheap
- but transient/source-backed composition is still structurally AOI- and `the-critic`-bound
- so the honest move is a tiered Stage 13 exit, not one oversized “generic host proof” tranche

## What Would Count As “Vision Achieved”

The vision should not be considered complete merely because the-critic is now much thinner.

The honest “close enough to the vision” bar is something more like:

- analyzer-v2 can accept bounded task input and own the key analytical decisions
- more than one consumer or one clearly generic host can use that intelligence without rebuilding it locally
- the planner-to-presentation bridge works across more than one workflow family
- dynamic surfaces have explicit lifecycle semantics
- the system has review/eval/override seams strong enough to trust those dynamic decisions

This draft roadmap therefore assumes:

- we are much closer than before
- but we are not done

One more distinction matters:

- against the narrower UI-composition vision, the platform is already in strong shape for one bounded slice
- against the broader analyzer-as-brain multi-app platform vision, the remaining bridge, host-neutrality, lifecycle, and governance work is still substantial

## Open Questions To Stress-Test

The following should be challenged aggressively in review:

1. Is the Stage 13 Tier A / Tier B split the right one?
2. Is `aoi-canary` enough for Tier A, or does Tier A still need more than result-backed proof?
3. Should Tranche 2 and Tranche 3 be reversed, or is AOI exemplar completion still the better precursor?
4. Is the de-AOI/de-`the-critic` transient-substrate tranche specific enough, or does it still hide multiple unrelated gaps?
5. Are Stage 14 and Stage 15 correctly deferred, or is there some lifecycle/governance minimum that should move earlier?
6. Is a second-consumer proof strictly necessary for the broader platform claim, or would a truly host-neutral transient/result harness be sufficient?

## Draft Judgment

If the last five days were about making the architecture real, the next stages should be about proving it general enough to deserve the platform claim.

That means the likely priorities are:

1. close the cheap result-backed second-consumer gap
2. finish one exemplar loop cleanly
3. remove the AOI/`the-critic` structural lock from transient/source-backed composition
4. then earn the stronger bridge and host-neutral proof
5. only then define lifecycle and governance on top

This should be treated as a draft strategic sequence, not yet as the canonical roadmap.
