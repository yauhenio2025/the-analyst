# Memo: Phase 3 Bounded Lifecycle V1 Scope

Subtitle: Define explicit save/reopen law for transient analytical surfaces after the verified Phase 2 proof

Date: 2026-03-28
Program: Dynamic Bespoke Apps Platformization
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Immediate Prior Completion: `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`
Relevant Prior Memos:
- `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`
- `communications/MEMO_2026-03-27_phase1c_bounded_router_planner_generalization_completion.md`
- `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_decision.md`
- `communications/MEMO_2026-03-27_phase1a_planner_to_presentation_bridge_completion.md`
- `communications/MEMO_2026-03-19_phase3_artifact_reuse_scope.md` as an older superseded Phase 3 line, not the active roadmap
- `communications/PLAN_Stage3_Lifecycle_Authority.md` as older result-contract lifecycle work that is orthogonal to this transient compose session question

## Purpose

Define the next bounded implementation slice after the verified March 28 Phase 2 closeout.

The missing seam is no longer:

- AOI-only planner-to-presentation glue
- non-AOI planner asymmetry
- host-neutral transient proof outside the current AOI page/controller path

The missing seam is now:

- explicit lifecycle law for dynamic analytical surfaces

This memo should scope the first honest lifecycle slice without drifting into publish/share, consumer proliferation, or productization.

## Current code-backed boundary

### What now exists

The current codebase already has:

- immutable analyzer-owned planning snapshots keyed by `planning_decision_id`
- transient compose entrypoints that can render real presentation payloads
- one bounded AOI planner-backed browser path in the current consumer
- one bounded non-AOI transient proof page outside the AOI page/controller stack
- analyzer-owned lowering from persisted planning truth into the thin public `compose-from-intent` request

Primary files carrying that reality:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/planning_decision_store.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV2.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/GenealogyTransientProofPage.tsx`

### What does not exist yet

For transient compose surfaces, the current codebase does not yet have:

- a first-class lifecycle object for a transient analytical surface
- an explicit save action that turns one transient compose result into a durable reopenable object
- a fetch/reopen route keyed by `session_id`
- a law that distinguishes:
  - unsaved transient compose response
  - saved lifecycle object
- a reopen path that returns the previously saved surface without rerunning:
  - `route-task`
  - `plan-task`
  - analyzer-owned lowering
  - `compose-from-intent`

Important negative facts:

- there are already job-backed restore surfaces and host-local snapshot caches elsewhere in the system, but those are not first-class save/reopen objects for transient compose surfaces
- `planning_decision_id` is existing planner snapshot identity used for reload/deep-link recovery, not truthful lifecycle identity for a saved transient surface
- the current AOI compose page recovers planning truth, but still composes transiently on demand
- the current genealogy proof page proves the transient chain, but does not save or reopen the resulting surface
- the current transient compose path returns presentation truth to the caller, but does not persist that final transient response or presentation snapshot as a reopenable lifecycle object

## Strategic decision

The first lifecycle slice should target the generalized transient substrate, not the AOI source-backed proxy stack.

Default first target:

- generic `compose-from-intent`
- `direct_sections`
- bounded non-AOI proof surface first

Why this is the right first lifecycle target:

1. It sits on the thinnest generalized planner-to-presentation substrate that is already proved live.
2. It avoids reopening AOI-specific proxy identity and continuity behavior as the place where lifecycle law is first defined.
3. It keeps the lifecycle question honest:
   - what object is saved?
   - what object is reopened?
   - what provenance must persist?
4. It lets Phase 3 attach lifecycle semantics to analyzer-owned transient presentation truth before adding workflow-specific page affordances.

Default proof vehicle:

- the existing genealogy transient proof page in `the-critic`, or a very close sibling over the same generic transient runtime law

This should remain a proof-oriented surface first, not a polished product surface.

## Scope decision

Phase 3 should define one bounded lifecycle object and one bounded save/reopen law.

The likely lifecycle object for this slice should be one analyzer-owned `compose_session`-style object.
The exact schema names may vary, but the following semantics must hold.

## Must land

### 1. One explicit persistence substrate

The slice must say where the lifecycle object lives.

Default honest choice for v1:

- analyzer-owned durable file-backed JSON storage, mirroring the bounded persistence pattern already used by `planning_decision_store.py`

Why this is the right bounded default:

- it keeps session truth analyzer-owned rather than browser-owned
- it avoids prematurely entangling lifecycle v1 with executor DB/project lifecycle
- it supports the bounded retention rule cleanly

This slice should not hide lifecycle truth in:

- browser state
- host-local cache truth
- planner snapshot files

### 2. One explicit lifecycle object

The slice must introduce one saved lifecycle object for transient compose outputs.

Minimum semantic content:

- `session_id`
- `saved_at`
- `workflow_key`
- `consumer_key`
- saved compose request snapshot
- saved exact final `ComposeFromIntentResponse` or exact final `TransientIntentPagePresentation` snapshot
- saved response fidelity fields:
  - `presentation_hash`
  - `presentation_content_hash`
  - `resolver_version`
- enough provenance to explain where the surface came from
- optional link back to `planning_decision_id` or `source_v2_job_id` where relevant

The lifecycle object must be analyzer-owned durable truth, not browser-only state.

Identity law:

- `session_id` is generated by analyzer at save time
- the host must not provide canonical lifecycle identity
- `planning_decision_id` may remain a provenance link, but it is not the lifecycle object id

### 3. One explicit save action

The slice must define one explicit action that saves an already-materialized transient surface into the lifecycle object.

Important law:

- do not auto-persist every transient compose response
- save must be deliberate
- save must persist the exact final response/presentation snapshot, not only the compose request or planning identity
- the slice earns credit only if it preserves the distinction between:
  - unsaved transient response
  - explicitly saved lifecycle object

Bounded v1 rule:

- save should be synchronous
- save should generate a new `session_id` each time rather than deduplicating “equivalent” surfaces

### 4. One reopen path by `session_id`

The slice must define one fetch/reopen path keyed by `session_id`.

Reopen law:

- reopen must return the previously saved lifecycle object
- reopen must not rerun:
  - `route-task`
  - `plan-task`
  - `planning_decision_fetch`
  - lowering
  - `compose-from-intent`

If truthful reopen requires storing the final transient presentation payload, that storage must be explicit.
Do not pretend `planning_decision_id` alone is enough.

### 5. Clear ownership split

Ownership should be explicit:

- analyzer owns saved session truth and reopen payload truth
- host owns route semantics, `session_id` navigation, and bounded reopen presentation
- host must not reconstruct a saved session by replaying planner law or re-lowering planning snapshots
- save/reopen reuses the `consumer_key` already present on the saved compose truth
- this slice does not reopen transient consumer registration or independently re-run transient adapter registration questions on reopen

### 6. One bounded proof surface

The first lifecycle proof should be executed on top of the generic direct-sections transient path, not on AOI source-backed proxy compose.

Default first proof:

- start from one completed genealogy saved result
- run the existing bounded transient chain
- save the resulting transient surface explicitly
- reopen it by `session_id`
- prove the reopened surface is served from saved lifecycle truth, not recomputation

### 7. One explicit retention rule

Retention must be defined, even if minimal.

Default bounded rule for Phase 3 v1:

- saved compose sessions are retained indefinitely in this slice
- delete/archive/cleanup policy is deferred
- no publish/share semantics are introduced
- indefinite retention here means analyzer-owned durable storage, not browser state and not host-local cache truth

## Must not widen

- do not turn `planning_decision_id` into a fake lifecycle substitute
- do not auto-save all transient surfaces
- do not add publish/share semantics
- do not reopen AOI-specific source-backed proxy lifecycle as the first lifecycle substrate
- do not add new transient consumer registration here
- do not widen into edit-in-place authoring, revision history, or collaborative drafting
- do not reopen `/v1/executor/jobs` or result-contract displacement as if that were the same question

## Required evidence shape

For this slice to count, the implementation must produce evidence of:

1. one transient compose result generated on the bounded generic direct-sections path
2. one explicit save action that returns a real `session_id`
3. one reopen-by-`session_id` success path
4. one fail-closed negative path for invalid `session_id`
5. one trace proving reopen did not rerun planning or composition
6. saved-payload fidelity showing that reopen serves the exact saved response/presentation snapshot rather than a fresh compose result that merely looks similar

The required reopen proof should show no calls to:

- `route-task`
- `plan-task`
- `GET /v1/orchestrator/planning-decisions/{id}`
- `GET /v1/orchestrator/planning-decisions/{id}/compose-from-intent-request`
- `POST /v1/presenter/compose-from-intent`

## Default surface shape

The likely honest API shape for this slice is:

- one analyzer save route for transient compose sessions
- one analyzer fetch route for saved compose sessions by `session_id`

This memo does not force exact endpoint names yet, but the save/fetch pair must be explicit and must treat saved session truth as a presenter-owned lifecycle contract, not as a side effect of planning persistence.

Older result-contract lifecycle work remains orthogonal:

- that line is about job-backed restore authority
- this line is about transient compose session lifecycle

## Why this is the right next honest step

Phase 2 proved that the generalized transient substrate can now drive a real non-AOI transient proof outside the AOI controller path.

That means the next question is no longer:

- can the system produce a stronger transient proof?

It is now:

- what exactly is a dynamic analytical surface once the user wants to keep it?

Phase 3 should answer that with one bounded save/reopen law before anything broader is attempted.
