# Memo: Stage 7 / Planner-To-Presentation Bridge Scope

Subtitle: Bounded AOI Source-To-Composition Bridge Slice

Date: 2026-03-23
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Purpose

Define the next stage-specific engineering scope after the canonical roadmap revision.

This memo is about the next **platform** move, not just the next AOI UX tweak.

The target is the stage now named in the canonical roadmap as:

- `STAGE 7: FORMALIZE THE PLANNER-TO-PRESENTATION BRIDGE`

This memo exists because the codebase is no longer in the state described by the original March 8 vision doc.

Two things are now simultaneously true:

1. analyzer-v2 already has substantial orchestrator / adaptive-planner infrastructure
2. analyzer-v2 also now has a real AOI transient composition path

What does **not** yet exist is the bridge between them.

That bridge is the next meaningful engineering stage.

This memo is deliberately narrower than the full stage name sounds.

It does **not** yet wire planner output directly into page law.
What it does scope is the bounded prerequisite slice:

- an analyzer-owned **source-to-composition bridge**

That is why the stage name and the implementation scope need to be read carefully:

- roadmap stage name:
  - planner-to-presentation bridge
- concrete bounded implementation in this memo:
  - AOI source-to-composition bridge as the first slice of that larger bridge

## Why This Stage Now

The master roadmap now makes three claims that should be treated as binding:

1. downstream AOI transient composition is real enough that more consumer-side AOI glue is no longer the highest-leverage move
2. upstream planning is not greenfield, because the repo already contains real orchestrator infrastructure
3. the next missing seam is the analyzer-owned contract that connects plan/result truth to composition-ready source selection and page planning

This stage is therefore the right next move because it attacks the actual gap:

- not “build planning from zero”
- not “add more AOI app code”
- not “jump to cross-workflow generalization immediately”

But:

- formalize the analyzer-owned source-selection bridge between existing run/result truth and dynamic composition

## Relationship To Roadmap Stages 3 And 4

This stage overlaps materially with what the canonical roadmap currently calls:

- `STAGE 3: MOVE AOI FROM FIXED PROFILES TO AOI TASK-DRIVEN COMPOSITION`
- `STAGE 4: ADD AOI ENGINE/SOURCE-SELECTION LAW`

That overlap should be treated as intentional, not as a contradiction.

If this stage lands as scoped here, the roadmap should be updated like this:

- Stage 7 closes the **infrastructure and contract** needed for source selection
- Stage 3 then reduces to:
  - replace `profile` as the primary selector input with bounded AOI task-driven selector input
- Stage 4 then reduces to:
  - broaden the selector from two fixed preset bundles to richer AOI reasoning over source families

So this memo does not eliminate stages 3-4, but it does front-load the bridge substrate they depend on.

## Current Code Reality

### What already exists

The orchestrator side is real:

- `src/orchestrator/planner.py`
- `src/orchestrator/adaptive_planner.py`
- `src/orchestrator/pipeline.py`
- `src/orchestrator/catalog.py`
- `src/orchestrator/pipeline_schemas.py`
- `src/api/routes/orchestrator.py`
- `src/objectives/definitions/influence_thematic.json`

The composition side is also real:

- `src/presenter/compose_from_intent.py`
- `src/presenter/schemas.py`
- `src/api/routes/presenter.py`

The source-backed transient path is real:

- `POST /v1/presenter/compose-from-source`

The consumer render path is real:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

### What does not yet exist

`compose-from-source` still bridges source truth to composition through hardcoded AOI profile assembly inside:

- `src/presenter/compose_from_intent.py`

Today that code does this:

- validate `workflow_key == anxiety_of_influence_thematic_single_thinker`
- accept `profile = dossier | comparison`
- load a fixed AOI source bundle for that profile
- serialize those sources into `ComposeFromIntentSectionInput[]`
- hand that to the transient page planner

That means the current path is real, but it is still missing the formal bridge contract.

There is no analyzer-owned structure that says:

- what composition-eligible source families exist for this result
- which were selected
- which were rejected
- why
- how those sources became composition-ready sections

That is the seam this stage should close.

## Strategic Decision

This stage should be:

- AOI-only
- analyzer-owned
- bridge-first
- minimally disruptive to the existing consumer path

This stage should **not** try to do all of the following at once:

- generic task-intake
- cross-workflow source generalization
- second-workflow composition
- lifecycle reopening
- richer page hierarchy
- consumer-side product redesign

Those are later stages.

## Bounded Claim For This Stage

This stage should prove one bounded thing:

- analyzer-v2 can resolve an analyzer-owned **composition source catalog** from real AOI run/result truth and use that catalog to drive `compose-from-source`, with explicit selected/rejected source rationale and trace, instead of hardcoded `profile -> sections` assembly

The public consumer path may remain the same.
The point is that the internal bridge becomes real.

## What This Stage Should Realize

### 1. A formal analyzer-owned composition source catalog

Add an internal analyzer-side source-catalog layer for AOI source-backed composition.

The source catalog should be built from analyzer-owned truth, not from saved Critic presentation internals.

Required inputs:

- `source_v2_job_id`
- effective plan context if available
- objective metadata if available
- analyzer-owned AOI artifacts
- analyzer-owned phase-output metadata for the thematic report
- analysis product / result contract metadata where useful

Resolution policy in stage 7 should be explicit:

- the catalog builder resolves **all expected AOI candidate families at catalog-build time**
- artifact-backed candidates are loaded through the existing normalized artifact path
- report-backed candidates are loaded through the existing phase-output metadata path
- candidate availability is **not** deferred to section materialization

The catalog must explicitly distinguish at least these states:

- `available`
- `unavailable`
- `invalid`

Where:

- `unavailable` means the expected source was not found
- `invalid` means the source was found but is structurally unusable
  - for example, malformed normalized payload
  - missing report sections
  - unparsable metadata

Each candidate source in the catalog should have enough information to support selection and traceability.

Minimum candidate metadata should include:

- stable source family key
- engine key or producer identity
- source kind:
  - normalized artifact
  - phase output metadata
  - normalized report payload
- provenance pointer
  - job id
  - artifact family or phase output ref
- composition role hint
- whether the source is required, optional, or unavailable for the current result
- candidate state:
  - `available`
  - `unavailable`
  - `invalid`
- enough summary/shape metadata for selection logic

For stage 7, the mixed AOI source backends should be represented explicitly in the catalog:

- `artifact`
- `phase_output_metadata`
- `normalized_report_payload`

Do not flatten these into one fake universal backend.

The resolution policy for current AOI families should be:

- thematic synthesis:
  - normalized artifact
- engagement mapping:
  - normalized artifact
- sin findings:
  - normalized artifact
- thematic report:
  - latest `aoi_thematic_report` phase output, then normalized report payload / report sections from metadata

This contract should be analyzer-owned and internal in stage 7.
Do not push it into the consumer yet.

### 2. A bounded AOI source-selection seam

Add a bounded source selector over the source catalog.

For stage 7, it is acceptable for the request to remain:

- `profile = dossier | comparison`

But the important change is:

- `profile` is no longer a hardcoded section bundle
- `profile` becomes an input to analyzer-owned source selection over a formal catalog

The selector should output:

- selected source families
- rejected source families
- rationale for both
- materialization order into composition sections

This selection should be traceable and explicit.

Stage-7 failure policy should also be explicit:

- if any **required** candidate is `unavailable` or `invalid`, abort the composition with the existing source-resolution `409`
- partial composition from reduced candidate sets is **not** part of stage 7
- graceful degradation across incomplete candidate sets belongs to later stages

### 3. A section-materialization layer

After selection, add one explicit step that turns selected source candidates into:

- `ComposeFromIntentSectionInput[]`

This step should be separate from raw source selection so the bridge is legible:

1. source catalog resolution
2. source selection
3. section materialization
4. existing transient page planning / view generation / transformation / adaptation / validation

That separation matters because stage 8 and stage 10 will likely reuse it.

### 4. A new source-backed resolver version

This stage should bump the source-backed resolver version from:

- `compose-from-source-v1`

to:

- `compose-from-source-v2`

Reason:

- the public response contract can stay stable
- but the internal bridge semantics will have materially changed
- proof artifacts and regressions should be able to distinguish the hardcoded profile era from the catalog/selection era

Both:

- `response.presentation.resolver_version`
- `response.trace.resolver_version`

should reflect the new version.

### 5. A richer source-backed trace

The source-backed response trace should prepend explicit bridge stages before the existing transient composition stages.

Required new trace stages:

- `source_catalog_resolution`
- `source_selection`
- `section_materialization`

The existing transient stages should remain after that:

- `page_plan`
- `view_generation`
- `transformation_execution`
- `consumer_adaptation`
- `contract_validation`

The new trace should remain summary-sized.
Do not dump full raw source payloads into the runtime trace.

The trace should also record:

- whether effective plan context was found
- whether objective metadata came from run-specific truth or workflow fallback
- which required candidates were resolved from which backend kind

## Architecture Decisions

### Decision 1: Keep the public route stable

Keep:

- `POST /v1/presenter/compose-from-source`

The consumer does not need a new entrypoint for this stage.

This keeps round-13/14 adoption paths stable while the analyzer internals improve.

### Decision 2: Keep the consumer unchanged unless a real compatibility bug is found

The-critic should not become the place where source-catalog reasoning lives.

Default expectation:

- no runtime the-critic changes

Allowed exception:

- a narrow compatibility patch if the new analyzer trace or error detail changes break an existing client assumption

But do not scope the stage around frontend work.

### Decision 3: Use plan/objective context when available, but do not block stage 7 on universal plan-context availability

The bridge should prefer:

- effective plan context
- stored `objective_key`
- workflow-owned objective metadata

But it should not fail just because the result lacks perfect plan-context richness.

Bounded fallback is acceptable if recorded explicitly in trace, for example:

- use workflow default objective metadata when run-specific objective metadata is missing

For stage 7, “use plan/objective context” should mean these concrete fields:

- `objective_key`
- `workflow_key`
- selected thinker identity when present
  - `selected_source_thinker_id`
  - `selected_source_thinker_name`
- phase execution specs from effective plan context
  - especially whether expected producer phases were skipped or absent

Stage 7 should **not** claim to consume the full planner output as page law.
In particular, it should not yet treat:

- `WorkflowExecutionPlan.recommended_views`

as authoritative page-plan input.

That is later work.

What is not acceptable:

- silent fallback to saved Critic `raw_prose`
- consumer-owned source reconstruction

### Decision 4: Keep stage 7 AOI-only

The reviewers were right that a second-workflow bridge is strategically attractive.

But stage 7 should still stay AOI-only.

Reason:

- the point of stage 7 is to formalize the bridge seam itself
- not to simultaneously generalize source-material law across workflows

Cross-workflow generalization belongs in later stages after the bridge contract exists.

### Decision 5: Do not remove `profile` yet

Stage 7 is not the same as AOI task-driven composition.

For this stage:

- `profile` may remain in the request
- but it becomes a bounded selector input over the source catalog
- it must stop being the hidden hardcoded source bundle itself

Removing `profile` entirely belongs later.

The memo should be read as downgrading `profile` to:

- a bounded preset selector over analyzer-owned source selection

It should no longer be treated as:

- the hidden source bundle itself

### Decision 6: Preserve the existing host contract

The host contract already has a real product-facing identity seam:

- project id
- thinker id
- saved result identity / `source_analysis_id`

This stage must preserve that doctrine.

Analyzer-facing resolution may still use:

- `source_v2_job_id`

But stage 7 must not force the consumer to promote raw analyzer job identity into the product contract.

## What This Stage Must Not Become

This stage must not dissolve into:

- another AOI panel UX round
- a second thin-consumer cleanup round
- generic task-intake redesign
- lifecycle reopening
- full semantic page-planning broadening
- cross-workflow source generalization
- a “second workflow” expedition just because it sounds strategically impressive

Those are adjacent stages, not this one.

## Proposed Implementation Shape

### analyzer-v2 only, by default

Expected write scope should be primarily:

- `src/presenter/compose_from_intent.py`
- `src/presenter/schemas.py`
- one new small presenter-side bridge module, likely something like:
  - `src/presenter/composition_source_bridge.py`
  - or `src/presenter/composition_source_catalog.py`

Potential secondary touch points if needed:

- `src/analysis_products/result_contract.py`
- `src/executor/plan_context.py`
- AOI artifact helpers if the current load path is too narrow
- `src/analysis_products/schemas.py` only if a tiny shared internal contract type becomes useful

### Internal bridge objects

Suggested internal objects:

- `CompositionSourceCandidate`
- `CompositionSourceCatalog`
- `CompositionSourceSelection`
- `CompositionMaterializedSection`

These do not need to become public API models in stage 7 unless that makes testing dramatically cleaner.

### Current AOI candidate families

The initial AOI source catalog will likely include at least:

- thematic synthesis
- engagement mapping
- sin findings
- thematic report sections

Potentially later:

- additional AOI families if they become durable and composition-relevant

### Bounded selection policy

For stage 7:

- `dossier` should still select a synthesis-led + report-closing bundle
- `comparison` should still select an engagement-led + findings-led + report-closing bundle

But those outcomes should now emerge through:

- explicit source candidates
- explicit selection
- explicit rejected candidates

not through an inline `if profile == ...` section builder.

This is why the most honest name for the concrete implementation is:

- source-to-composition bridge

The larger planner-to-presentation bridge remains the roadmap stage this slice belongs to.

## Test Plan

### analyzer-v2 backend

Add focused tests for:

- source catalog resolution from a valid AOI source-backed job
- candidate family presence for:
  - synthesis
  - engagement mapping
  - sin findings
  - thematic report
- report candidate sourced from phase-output normalized metadata, not artifact lookup
- candidate state distinguishes:
  - `available`
  - `unavailable`
  - `invalid`
- objective/plan-context enrichment when available
- explicit fallback behavior when plan/objective metadata is missing
- phase-skip / missing-plan-context behavior is recorded explicitly
- `dossier` selection emits selected + rejected rationale
- `comparison` selection emits selected + rejected rationale
- section materialization order is deterministic
- `compose-from-source` response uses `compose-from-source-v2`
- trace begins with:
  - `source_catalog_resolution`
  - `source_selection`
  - `section_materialization`
- final transient response contract remains unchanged
- final renderer-contract invalid still uses the existing nested `409` issues envelope
- source-material failure still returns plain source-resolution `409` where appropriate
- required invalid candidate returns source-resolution `409`, not partial success

### regressions

Keep existing round-11/13/14 AOI source-backed regression green.

The important regression claim is:

- the consumer should not need to change to benefit from the new analyzer-owned bridge

### frontend

No frontend implementation is expected.

At most:

- rerun the focused transient client/page tests if the response trace or error detail shape requires a compatibility confirmation

## Proof Standard

Proof should use the already-real AOI source-backed path, not fixtures.

Required proof evidence:

- one real source-backed `dossier` run
- one real source-backed `comparison` run
- saved trace JSONs showing the new bridge stages
- saved proof artifact showing selected and rejected source families
- zero final renderer-contract issues

If round-13 and round-14 documentary tails are still not closed when this stage is implemented, the proof note for this stage must say one of two things explicitly:

1. it subsumes those tails, or
2. it does not, and those tails still remain open

Do not let documentary status become vague.

## Exit Criteria

This stage is complete only if all of the following are true:

1. `compose-from-source` no longer hardcodes `profile -> sections` as the primary bridge
2. analyzer-v2 builds a real AOI composition source catalog from run/result truth
3. source selection is explicit and traceable
4. section materialization is explicit and deterministic
5. source-backed responses advertise `compose-from-source-v2`
6. the public consumer route and render path remain compatible without new consumer intelligence
7. proof artifacts show the new bridge stages and selected/rejected rationale

## Naming Note

The roadmap may continue to call this stage:

- planner-to-presentation bridge

But the bounded implementation in this memo should be read more precisely as:

- AOI source-to-composition bridge

That is not a contradiction.
It is the first concrete slice of the larger bridge.

## What Comes Next If This Stage Lands

If stage 7 lands cleanly, the next high-value move should be:

- bounded AOI task-driven composition over that bridge

That would mean:

- `profile` stops being the primary organizer
- the system begins to choose among AOI source families in response to bounded composition tasks

But that should happen **after** the bridge exists, not before.

## Open Question To Force In Review

Reviewers should be asked to challenge one thing directly:

- should this stage stay AOI-only, or is the higher-leverage move to force the bridge on a second workflow immediately?

My current answer is:

- stay AOI-only for stage 7
- use stage 10 for cross-workflow source-backed generalization

But that assumption should be tested rather than silently accepted.
