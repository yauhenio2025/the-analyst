Approve

# Stage 8/9 Host Adoption Task Launch Scope Audit

Audited memo:
- `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_scope.md`

## Verdict

Approve.

The revised memo now matches the live code and the current strategy ledger closely enough to function as the next executable scope document. The core recommendation should stand.

## Findings

### 1. High: the memo's main diagnosis is still correct, and the code evidence remains direct

`analyzer-v2` exposes both task-advisory seams:

- `src/api/routes/orchestrator.py:301-326` exposes `POST /v1/orchestrator/route-task` and `POST /v1/orchestrator/plan-task`
- `src/orchestrator/task_routing_schemas.py:104-122` defines the public task envelope
- `src/orchestrator/task_planning_schemas.py:132-192` defines the public planning boundary

The-critic still does not use either seam anywhere:

- repo search across `the-critic/api`, `the-critic/webapp`, and `the-critic/analyzer` found no references to `route-task` or `plan-task`
- AOI source-backed launch logic still branches locally in `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:488-535`
- AOI transient compose still launches locally in `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:202-261`
- genealogy launch mode is still chosen in backend host code in `the-critic/api/server.py:447-456` and executed in `the-critic/api/server.py:18059-18318`

So the memo is right that analyzer-owned task routing and planning exist, while the live host still owns too much launch intelligence locally.

### 2. High: the revised memo now describes the AOI seam and genealogy seam honestly

This was the most important scope correction, and it is now in good shape.

The AOI seam is now explicitly framed as the thinner proof:

- the memo says the host is already on an AOI-specific surface by URL routing
- it limits AOI value here to contractual consolidation, analyzer-owned handoff metadata, and host obedience to planner truth

That matches the code:

- AOI source-backed launch is still host-bounded through `the-critic/api/server.py:20311-20365`
- AOI readiness/launch behavior is already fairly constrained in `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:498-533`
- `composeFromSource(...)` is already a dedicated AOI proxy launch client in `the-critic/webapp/src/lib/composeFromIntentClient.ts:64-103`

The genealogy seam is now explicitly framed as the stronger proof because it removes real host-owned execution-path choice. That also matches live code:

- backend host code currently chooses `reuse_plan` vs `by_ref` vs `inline` in `the-critic/api/server.py:447-456`
- it then builds different payloads and dispatches different helpers in `the-critic/api/server.py:18059-18318`

This revised framing is materially more honest than the prior version.

### 3. High: the memo now describes genealogy `plan-task` precisely enough as advisory-for-dispatch but not read-only

The revised Decision 6 is correct and concrete:

- `route-task` is advisory and read-only
- `plan-task` is advisory with respect to dispatch
- genealogy `plan-task` is not read-only and should be treated as a commit-like launch-preparation step

That matches live analyzer behavior:

- inline planning uploads/materializes documents in `src/orchestrator/pipeline.py:102-119`
- by-ref planning resolves registered documents and materializes `document_ids` in `src/orchestrator/by_ref.py:494-510`
- the Stage 9 planner returns executor followup contracts in `src/orchestrator/task_planner.py:333-356`
- the Stage 9 completion memo explicitly records that genealogy planning can create persisted plans and hydrated document records even when no execution follows

So the revised memo no longer blurs advisory planning with speculative preview behavior or lifecycle law. It now names the real semantics.

### 4. Medium: the memo now avoids the major architectural trap of creating a third disconnected client/runtime layer

This was the other major revision, and it lands.

The revised memo now says the task-launch layer must:

- not become a third disconnected client stack beside `boundedV2Client.ts` and `composeFromIntentClient.ts`
- chain into the existing Host Contract v1 runtime and existing launch helpers
- be consumed by backend host launch code as well as frontend code

That is the correct bounded shape against the live host substrate:

- result-backed helpers already run through `the-critic/webapp/src/lib/boundedV2Client.ts:12-18`
- transient helpers already run through `the-critic/webapp/src/lib/composeFromIntentClient.ts:7-17`
- both dispatch through the shared runtime in `the-critic/webapp/src/lib/hostContractRuntime.ts:182-191`

There is still implementation risk if the tranche drifts, but the memo itself now points in the right direction and no longer scopes a disconnected parallel client family.

### 5. Medium: the memo still correctly claims both proposed proof seams are feasible without analyzer API changes

The helper substrate already exists.

Current host/analyzer execution helpers:

- `orchestrator/analyze`
  - `the-critic/analyzer/concept_analyzer/analyzer_v2_client.py:329-434`
- `orchestrator/analyze-by-ref`
  - `the-critic/analyzer/concept_analyzer/analyzer_v2_client.py:780-835`
- `executor/jobs`
  - `the-critic/analyzer/concept_analyzer/analyzer_v2_client.py:1027-1066`
  - current host `reuse_plan_id` path in `the-critic/api/server.py:18193-18215`
  - current API request support in `the-critic/api/models_genealogy.py:26-43`
  - current frontend submit path in `the-critic/webapp/src/pages/GenealogyPage.tsx:1030-1032`
- `compose-from-source`
  - `the-critic/webapp/src/lib/composeFromIntentClient.ts:64-103`
  - `the-critic/api/server.py:20311-20365`
  - `the-critic/analyzer/concept_analyzer/analyzer_v2_client.py:1248-1267`

Given those helpers, the revised memo is right:

- AOI can adopt `route-task` plus `plan-task` and still follow the existing source-backed proxy launch
- genealogy can adopt `route-task` plus `plan-task` and still execute the returned plan through the existing `executor/jobs` path

No analyzer API widening is required for the bounded tranche described here.

### 6. Medium: a separate bounded task-launch contract remains cleaner than widening Host Contract v1

That claim still holds after revision.

Host Contract v1 remains about the bounded run/result/readiness/transient family set:

- `the-critic/webapp/src/lib/hostContractV1.ts:6-18`
- `the-critic/webapp/src/lib/hostContractV1.ts:87-245`

`route-task` and `plan-task` are different in kind:

- advisory seams
- optional prior-routing reuse
- planning-context hydration
- no automatic dispatch

So a bounded adjacent task-launch contract is cleaner than overloading Host Contract v1 right now. The memo also now correctly says that this new layer should chain into the existing runtime instead of floating beside it.

### 7. Low: the roadmap argument is now presented honestly enough

The revised memo now states that this is a prioritization judgment after the Stage 13 second slice, not a claim that the canonical roadmap had already precommitted this exact tranche shape.

That is the correct way to read the current ledger:

- the roadmap still says Stage 8 and Stage 9 remain partial because host adoption is open at `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1173-1174`
- it also records that the honest move after the first Stage 13 slice was the second Stage 13 slice at `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1234`
- the broader assessment still says the hard remaining problem is upstream planning generalization and bridging at `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:102-109`

So the revised memo no longer overclaims roadmap inevitability. It makes a defensible next-step judgment.

## Open Assumptions

- The cleanest genealogy proof will likely land through shared backend task-launch/runtime adoption in `the-critic/api/server.py`, not only through frontend pages. The revised memo points this way, but implementation discipline will matter.
- The AOI proof still depends on canonical `source_v2_job_id` being available or resolvable from saved-result identity. That is feasible today, but the final implementation should make the fallback path explicit.
- A future broader host-contract pass may still fold task-launch seams into a wider host contract. The revised memo is correct to avoid that widening in this bounded tranche.

## Recommendation

The memo's recommendation should stand.

It should not be replaced, and it does not need another scope revision before approval. The remaining concerns are implementation risks, not memo-level strategy or contract-shape problems.
