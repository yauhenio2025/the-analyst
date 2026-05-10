# Memo: Close Read Concept-Analysis Live Authority Deployment And Thin-Client Cutover Scope

Subtitle: Turn the already-landed local concept-runtime authority slice into live Render truth, then complete the bounded Critic thin-client cutover for the admitted `inferential` and `logical` concept submodes

Date: 2026-04-06
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Roadmap Context:
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_local_analyzer_v2_visibility_slice.md`
Immediate Scope Predecessor:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_runtime_authority_and_analyzer_mgmt_visibility_scope.md`
Immediate Completion Predecessor:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_local_visibility_and_operator_trail_completion.md`
Runtime Recomposition Context:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md`
Fresh-Project Runtime Context:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`
Primary Local Evidence:
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_by_ref.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/concept_inferential_single_concept.json`
- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/concept_logical_single_concept.json`
- `/home/evgeny/projects/analyzer-v2/src/transformations/definitions/concept_inferential_host_contract_extraction.json`
- `/home/evgeny/projects/analyzer-v2/src/transformations/definitions/concept_logical_host_contract_extraction.json`
- `/home/evgeny/projects/analyzer-v2/src/workflows/schemas.py`
- `/home/evgeny/projects/analyzer-v2/src/workflows/registry.py`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/implementations/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/workflows/[key].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/jobs/[id].tsx`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py`

## Purpose

Define the next operational tranche after the local visibility/operator-trail completion:

- land the local analyzer-v2 concept-runtime authority assets in git
- deploy analyzer-v2 and analyzer-mgmt so the authority layer is live on Render
- validate the live analyzer-v2 and analyzer-mgmt stack against the frozen operator law
- complete the bounded Critic cutover so the admitted concept submodes consume live analyzer-v2 translated artifacts as thin-client host behavior

This is the stage where local proof must become live truth.

## Bottom Line

The decisive next gap is no longer local concept-runtime design.

It is:

1. deployment
2. live validation
3. bounded host cutover

So this tranche should not open any new product or substrate questions.
It should simply make the already-chosen architecture true on the deployed stack.

## What Is Already True Locally

Locally we already have:

- bounded by-ref concept orchestration
- concept inferential workflow
- concept logical workflow
- concept inferential host-contract transformation
- concept logical host-contract transformation
- explicit workflow-to-transformation linkage
- analyzer-mgmt implementation/workflow/jobs visibility consistent with the frozen operator law
- local Critic recomposition path for analyzer-v2-backed inferential/logical concept runs

That local state is enough to stop doing more speculative design.

## What Is Still False Live

As of the last live Render check in the predecessor memo:

- analyzer-v2 on Render did not yet expose the bounded concept by-ref route
- analyzer-v2 on Render did not yet expose the new concept workflows
- analyzer-v2 on Render did not yet expose the new concept host-contract transformations
- analyzer-mgmt on Render was not yet reliably the canonical concept operator console for this slice

That is the actual next problem.

## Scope Summary

Implement one bounded live-authority tranche:

1. `git add`, commit, and push the local analyzer-v2 concept-runtime assets and analyzer-mgmt visibility repair
2. deploy analyzer-v2 and analyzer-mgmt to Render
3. validate the live Render analyzer-v2/analyzer-mgmt stack against the frozen operator law
4. complete the bounded Critic cutover for live analyzer-v2 translated-artifact consumption on `inferential` and `logical`
5. deploy the-critic as a separate dependency for the live host cutover
6. prove the full path through one live browser-tested concept example

## Key Decisions To Freeze

### 1. No new analyzer-v2 substrate types

Stay entirely inside:

- engines
- operationalizations
- chains
- workflows
- transformations

If anything is missing, solve it by repairing or deploying those existing types, not by inventing a new layer.

### 2. The canonical operator surface stays concrete

Freeze this rule for the live tranche:

- `implementations/[key]` remains the canonical composition page until `workflows/[key]` is fully chain-aware enough to replace it
- workflow **or** implementation detail must expose the underlying engine/chain composition
- workflow-to-transformation linkage must be explicit
- jobs/result-boundary must link back into the same operator trail

### 3. Critic cutover stays bounded to the admitted seams

This tranche only thins Critic on:

- `inferential`
- `logical`

It explicitly does **not** widen into:

- `assumption`
- `semantic_field`
- `causal`
- `metaphorical`
- cross-corpus concept analysis
- broader concept-estate cache cleanup

### 4. Live deployment is part of scope, not an afterthought

This tranche is not complete if the code exists only locally.

Success requires live Render evidence.

And the deployment gate is three-repo real:

- analyzer-v2 code must be added, committed, pushed, and deployed
- analyzer-mgmt code must be added, committed, pushed, and deployed
- the-critic host cutover, where changed, must be added, committed, pushed, and deployed separately

## Implementation Sequence

### Phase 1: Land and deploy the authority assets

`git add`, commit, push, and deploy:

- analyzer-v2 concept by-ref orchestrator code
- analyzer-v2 concept workflow definitions
- analyzer-v2 concept host-contract transformation definitions
- analyzer-v2 workflow linkage metadata
- analyzer-mgmt workflow/implementation/jobs visibility repair

Hard stop:

- untracked local files do not count as landed work
- committed local files do not count as deployed authority
- deployment claims are not valid until the relevant repos are pushed and the hosted services are updated

### Phase 2: Validate live analyzer-v2 authority

On Render, verify:

- `/v1/workflows` includes:
  - `concept_inferential_single_concept`
  - `concept_logical_single_concept`
- `/v1/transformations` includes:
  - `concept_inferential_host_contract_extraction`
  - `concept_logical_host_contract_extraction`
- `POST /v1/orchestrator/concept-analysis-by-ref` exists and launches both admitted modes

### Phase 3: Validate live analyzer-mgmt visibility

On Render, verify:

- existing concept engine pages render real content in the browser
- existing concept chain pages render real content in the browser
- transformations list/detail render real content in the browser
- new concept workflows appear on workflows/implementations surfaces
- implementation or workflow detail exposes the workflow-to-transformation linkage
- jobs/result-boundary preserves the same operator trail
- if engine/chain visibility is still broken on Render, fix that before treating analyzer-mgmt as the canonical live operator console for this slice

The point is not merely “the SPA shell returns HTTP 200.”
The point is that a human operator can inspect the live composition without reading Critic code.

### Phase 4A: Complete the bounded Critic execution cutover

On the admitted concept paths only:

- Critic launches live analyzer-v2 concept runs
- Critic polls live analyzer-v2 status
- Critic fetches analyzer-v2-translated host-contract artifacts
- Critic renders them without reasserting local semantic authority

Keep Critic-local follow-up bounded:

- no local semantic translation may remain the authority path
- logical scrutiny UI/workflow may remain host-local
- but scrutiny must read only translated analyzer-v2-backed logical output

### Phase 4B: Complete the bounded Critic scrutiny cutover

On the logical surface only:

- prove scrutiny derives from translated analyzer-v2-backed logical output
- prove scrutiny does not depend on old local-runtime-only logical fields
- verify persisted logical result provenance records analyzer-v2 as execution owner before scrutiny is treated as valid on the live path

### Phase 4C: Deploy the-critic host cutover

This is a separate deployment dependency from analyzer-v2 and analyzer-mgmt.

The tranche is not live-complete until the-critic deployment reflects the bounded cutover and is exercised against the live analyzer-v2/analyzer-mgmt stack.

### Phase 5: Live browser acceptance

Use a live or at least deployment-real stack to prove:

1. inferential live concept run succeeds
2. logical live concept run succeeds
3. both appear correctly in native concept pages and `Close Read`
4. one logical scrutiny flow succeeds against translated analyzer-v2-backed logical output
5. the persisted logical result used by scrutiny records `_analysis_provenance.execution_owner == "analyzer-v2"`
6. job/result-boundary/operator links in analyzer-mgmt point back to the correct implementation and linked transformations

## Public Interfaces / Non-Changes

Do not change:

- current Close Read concept routes
- current native concept routes
- current admitted concept submodes
- broader Close Read UI structure

Do not expose raw analyzer-v2-native schemas directly to the frontend in this tranche.

Do not widen into broader composition-layer work.

## Acceptance Criteria

### Live analyzer-v2 authority

On Render:

- concept workflows are present
- concept transformations are present
- concept by-ref route is present
- inferential and logical can be launched through analyzer-v2 as the live authority runtime

### Live analyzer-mgmt operator truth

On Render:

- engine/chain/transformation pages render real concept-asset content in the browser, not merely shell responses
- implementations/workflows surfaces show the concept workflows
- workflow-to-transformation linkage is explicit
- implementation or workflow detail remains a concrete composition page
- jobs/result-boundary links back into the same operator surface

### Thin-host truth

In Critic:

- inferential/logical concept runs no longer depend on Critic-local semantic authority
- Critic renders analyzer-v2-produced translated artifacts
- logical scrutiny reads translated logical output only
- the logical result used by scrutiny carries analyzer-v2 execution provenance

## Risks And Hard Stops

### 1. Do not claim completion on local-only proof

If analyzer-v2 and analyzer-mgmt on Render do not reflect the assets, the tranche is not done.

### 2. Do not reopen the substrate question

If the implementation starts inventing new top-level analyzer types, the tranche has drifted.

### 3. Do not let Critic quietly remain the semantic authority

If Critic still reconstructs inferential/logical meaning locally after the live cutover, the architecture has not really changed.

## Recommended Next Artifact After This Scope

After this tranche is complete, the next useful memo should probably be:

- a bounded closeout memo proving the live Render authority cutover

Only after that should the roadmap reopen:

- broader Close Read family expansion
- broader concept-estate migration
- composable module work beyond the admitted concept seams
