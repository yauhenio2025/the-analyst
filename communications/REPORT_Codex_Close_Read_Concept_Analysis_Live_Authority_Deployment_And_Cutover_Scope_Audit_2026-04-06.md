# Report: Close Read Concept Analysis Live Authority Deployment And Cutover Scope Audit

Date: 2026-04-06
Auditor: Codex
Verdict: `approve with corrections`

## Context Check

I read each required document in full:

- `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_deployment_and_cutover_scope.md` — read in full
- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md` — read in full
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_runtime_authority_and_analyzer_mgmt_visibility_scope.md` — read in full
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_local_visibility_and_operator_trail_completion.md` — read in full
- `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md` — read in full
- `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md` — read in full
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_local_analyzer_v2_visibility_slice.md` — read in full
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` — read in full
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md` — read in full
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md` — read in full
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md` — read in full
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md` — read in full
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md` — read in full

## Verdict

The memo has the right strategic center: the next honest gap is now live deployment, live authority validation, and bounded host cutover, not more local concept-runtime invention.

I am not rejecting it because the local code now materially supports that reading:

- analyzer-v2 has the local by-ref route, bounded workflow wrappers, and host-contract transformations
- analyzer-mgmt has the local workflow-to-transformation and jobs/result-boundary operator trail
- the Critic already has a bounded analyzer-v2-backed inferential/logical cutover seam

But the memo still needs corrections before it should be treated as the tranche charter, because the live Render state is materially behind local state and one narrow host-law point remains under-specified.

## Required Corrections

### 1. Make “land committed code” an explicit hard gate across all three repos

The memo says this in spirit, but it should say it more concretely.

As audited on 2026-04-06:

- in `analyzer-v2`, `src/orchestrator/concept_by_ref.py` is untracked, both concept workflow JSONs are untracked, both concept host-contract transformation JSONs are untracked, and the route/schema/registry files are modified
- in `analyzer-mgmt`, the relevant API/types/workflow/implementation files are modified and `frontend/src/pages/jobs/[id].tsx` is untracked
- in `the-critic`, `analyzer/concept_analyzer/analyzer_v2_recomposition.py` is untracked and `api/server.py` is modified

The memo should therefore say plainly:

- no live-authority acceptance work starts until the analyzer-v2, analyzer-mgmt, and Critic changes are all landed in git, pushed, and actually deployed

### 2. Tighten the analyzer-mgmt operator-console requirement

The memo is right that analyzer-mgmt belongs inside scope, not as cleanup.

But the live check shows a sharper issue than the memo currently stresses:

- live analyzer-v2 already serves `inferential_commitment_mapper`
- live analyzer-v2 already serves `concept_analysis_12_phase`
- live analyzer-v2 already serves `/v1/operationalizations/inferential_commitment_mapper`
- yet live analyzer-mgmt still shows `Engine not found` for the inferential engine page
- and live analyzer-mgmt still shows `Failed to load chain` for the concept chain page

So the memo should state explicitly:

- fixing live analyzer-mgmt visibility for already-live engine/chain/operator assets is a prerequisite for claiming analyzer-mgmt as the canonical operator console for this tranche

### 3. Strengthen the live acceptance path with provenance and result-boundary checks

The current acceptance path is close, but not fully strong enough to prove analyzer-v2 is the real authority.

It should require not only:

- one live inferential run
- one live logical run
- correct rendering in native concept pages and `Close Read`

It should also require:

- opening analyzer-mgmt `jobs/[id]` for the resulting run
- verifying the result-boundary/run-boundary trail
- verifying the implementation/workflow/transformation linkage from that job/result boundary
- verifying analyzer-v2 execution provenance is visible for the run that produced the rendered host artifact

Without that, the browser proof can still demonstrate “rendered output exists” without fully proving “analyzer-v2 is the admitted authority.”

### 4. Tighten the logical scrutiny cutover sentence

The memo is right to keep scrutiny host-local for now.

But the local Critic code does not yet enforce, at the API boundary, that scrutiny inputs came from translated analyzer-v2-backed logical output. The host currently accepts a logical payload and runs scrutiny over that payload.

So the memo should add one precise requirement:

- scrutiny request assembly must derive from persisted translated logical output only, or the host must validate analyzer-v2-backed provenance before scrutiny runs

That keeps the cutover bounded while making the host-law honest.

## Local Evidence

### analyzer-v2 local authority slice is real

The local code directly supports the memo’s “deployment, not more invention” reading:

- `src/orchestrator/pipeline_schemas.py:339` defines a bounded `ConceptAnalysisByRefRequest` limited to `inferential` and `logical`, and forces the workflow key to match the admitted mode
- `src/api/routes/orchestrator.py:501` exposes the local `POST /v1/orchestrator/concept-analysis-by-ref` route
- `src/orchestrator/concept_by_ref.py:87` and `src/orchestrator/concept_by_ref.py:152` build a single-phase analyzer-v2 execution plan over ordered registered documents and launch the executor thread
- `src/workflows/schemas.py:169` adds `linked_transformation_keys` to workflow definitions and `src/workflows/registry.py:55` carries that field into list summaries
- `src/workflows/definitions/concept_inferential_single_concept.json` defines the inferential bounded workflow and links it to `concept_inferential_host_contract_extraction`
- `src/workflows/definitions/concept_logical_single_concept.json` defines the logical bounded workflow and links it to `concept_logical_host_contract_extraction`
- `src/transformations/definitions/concept_inferential_host_contract_extraction.json` and `src/transformations/definitions/concept_logical_host_contract_extraction.json` define explicit host-contract extraction templates rather than leaving translation implicit in the host

This is exactly the correct analyzer-v2 type discipline:

- engines
- operationalizations
- chains
- workflows
- transformations

The local tranche does not invent a new analyzer-v2 top-level type.

### analyzer-mgmt local operator-console law is concrete

The memo’s operator-console law is materially reflected in local analyzer-mgmt code:

- `frontend/src/lib/api.ts:469` and `frontend/src/lib/api.ts:494` normalize `linked_transformation_keys` from live workflow list/detail payloads
- `frontend/src/types/index.ts:364` and `frontend/src/types/index.ts:380` carry `linked_transformation_keys` in both `Workflow` and `WorkflowSummary`
- `frontend/src/pages/workflows/[key].tsx:378` explicitly tells operators to use `implementations/[key]` as the canonical composition view for chain-backed workflows
- `frontend/src/pages/workflows/[key].tsx:468` renders the linked transformations block on the workflow detail page
- `frontend/src/pages/implementations/[key].tsx:1004` explicitly declares the implementation page the canonical composition surface for chain-backed workflows
- `frontend/src/pages/implementations/[key].tsx:1100` renders linked transformations on the implementation page
- `frontend/src/pages/jobs/[id].tsx:1046` links the result boundary back to `/implementations/${workflowKey}`
- `frontend/src/pages/jobs/[id].tsx:1062` surfaces linked transformations on the result-boundary header card
- `frontend/src/lib/api.ts:828` and `frontend/src/lib/api.ts:852` fetch analyzer-v2 result-boundary and run-boundary state directly

So locally the memo is right that:

- `implementations/[key]` is the canonical composition page for this tranche
- workflow-to-transformation linkage is explicit
- jobs/result-boundary is folded back into the same operator trail

### the Critic cutover is locally bounded to the admitted seams

The local Critic code also supports the memo’s bounded cutover framing:

- `the-critic/api/server.py:3963` defines `_run_rebased_concept_analysis(...)`, which syncs project documents to analyzer-v2, launches `concept-analysis-by-ref`, polls analyzer-v2 executor state, fetches phase outputs, and translates them
- `the-critic/api/server.py:4087` routes only `inferential` and `logical` through that rebased analyzer-v2 path
- `the-critic/api/server.py:4103` to `the-critic/api/server.py:4123` leaves `assumption`, `semantic_field`, `causal`, and `metaphorical` on other paths
- `the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py:96` translates inferential outputs through `concept_inferential_host_contract_extraction`
- `the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py:130` translates logical outputs through `concept_logical_host_contract_extraction`
- `the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py:119` and `the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py:153` stamp `_analysis_provenance` with analyzer-v2 workflow, engine-or-chain key, depth, analyzer job id, and transformation template

This is strong evidence that the memo is right to keep the cutover tightly bounded to:

- `inferential`
- `logical`

and to defer:

- cross-corpus concept work
- broader cache cleanup
- broader concept-estate migration

## Local Verification

I ran the following local checks on 2026-04-06:

- `pytest -q tests/test_concept_by_ref_launch.py` — passed
- `python -m py_compile src/orchestrator/concept_by_ref.py src/api/routes/orchestrator.py src/workflows/schemas.py src/workflows/registry.py src/orchestrator/pipeline_schemas.py` — passed
- `python -m py_compile /home/evgeny/projects/the-critic/api/server.py` — passed
- `python -m py_compile /home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py` — passed
- `npm run type-check` in `/home/evgeny/projects/analyzer-mgmt/frontend` — passed

I also confirmed locally that the workflow registry loads the two new concept workflows and their linked transformation keys.

## Live Render Evidence

I verified the deployed public Render state directly through the live URLs named in the prompt.

### analyzer-v2 live state is still behind local state

On 2026-04-06:

- `https://analyzer-v2.onrender.com/v1/meta/definitions-version` reported `workflow_count: 8`
- the local workflow registry loads `10` workflows, including the two concept workflows
- `https://analyzer-v2.onrender.com/v1/workflows` does not include `concept_inferential_single_concept`
- `https://analyzer-v2.onrender.com/v1/workflows` does not include `concept_logical_single_concept`
- direct live GETs to `/v1/workflows/concept_inferential_single_concept` and `/v1/workflows/concept_logical_single_concept` return `404`
- `https://analyzer-v2.onrender.com/v1/transformations` does not include `concept_inferential_host_contract_extraction`
- `https://analyzer-v2.onrender.com/v1/transformations` does not include `concept_logical_host_contract_extraction`
- direct live GETs to `/v1/transformations/concept_inferential_host_contract_extraction` and `/v1/transformations/concept_logical_host_contract_extraction` return `404`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref` returns `404` for both GET and POST

So the memo is correct that the missing live layer is still:

- workflow wrappers
- host-contract transformations
- bounded by-ref orchestrator seam

### the live capability primitives are partly there

The live analyzer-v2 stack is not empty. On 2026-04-06:

- `https://analyzer-v2.onrender.com/v1/engines/inferential_commitment_mapper` returned `200`
- `https://analyzer-v2.onrender.com/v1/chains/concept_analysis_12_phase` returned `200`
- `https://analyzer-v2.onrender.com/v1/operationalizations/inferential_commitment_mapper` returned `200`

That matters because it confirms the memo’s larger reading:

- the live problem is not missing primitive capability invention
- the live problem is missing deployed workflow/translation/launch authority and missing operator-console fidelity

### analyzer-mgmt live operator visibility is still not trustworthy enough

The live analyzer-mgmt frontend is still materially behind the local operator-console law:

- `https://analyzer-mgmt-frontend.onrender.com/engines/inferential_commitment_mapper` shows `Engine not found`
- `https://analyzer-mgmt-frontend.onrender.com/chains/concept_analysis_12_phase` shows `Failed to load chain`
- `https://analyzer-mgmt-frontend.onrender.com/workflows/concept_inferential_single_concept` shows `Failed to load workflow`
- `https://analyzer-mgmt-frontend.onrender.com/workflows/concept_logical_single_concept` shows `Failed to load workflow`
- `https://analyzer-mgmt-frontend.onrender.com/implementations/concept_inferential_single_concept` shows `Failed to load implementation`
- `https://analyzer-mgmt-frontend.onrender.com/implementations/concept_logical_single_concept` shows `Failed to load implementation`
- `https://analyzer-mgmt-frontend.onrender.com/transformations` shows `0 reusable transformation recipes`
- the transformation detail pages for the concept host-contract templates load an editor shell with blank identity fields rather than a real fetched template

This is the strongest live reason to keep analyzer-mgmt deployment inside scope rather than treating it as follow-up cleanup.

## Explicit Answers

- Does the codebase support the claim that the missing work is now live deployment and cutover, not more local concept-runtime invention?
  - Yes. The local analyzer-v2 route, workflows, transformations, analyzer-mgmt linkage surfaces, and bounded Critic cutover seam are now real enough that the next gap is deployment and authority proof, not another round of local concept-runtime design.

- Is the memo right to treat deployment of analyzer-v2 and analyzer-mgmt as scope, not follow-up cleanup?
  - Yes. The live stack currently lacks the concept workflows, host-contract transformations, and by-ref route, and live analyzer-mgmt is still failing even on existing concept engine/chain pages. Deployment and live console repair are core scope.

- Does the memo correctly preserve `implementations/[key]` as the canonical composition page until workflow detail is fully sufficient?
  - Yes. That matches the local analyzer-mgmt code exactly and is the right frozen rule for this tranche.

- Does it make workflow-to-transformation linkage concrete enough?
  - Mostly yes. The local workflow schema, registry, workflow definitions, and analyzer-mgmt pages are concrete. The memo should only add stricter live acceptance language around the exact implementation/workflow/transformation/result-boundary checks.

- Does it correctly fold jobs/result-boundary into the operator trail requirement?
  - Yes. That requirement is justified by the local jobs page implementation and should stay in scope.

- Is the bounded Critic cutover scoped tightly enough to `inferential` and `logical`, with cross-corpus and broader cache cleanup deferred?
  - Yes, with one correction. The scope boundary itself is right, but the memo should explicitly require scrutiny to consume translated analyzer-v2-backed logical output only, not merely rely on host convention.

- Does the memo stay properly narrower than broader Close Read composition-layer work and UI expansion?
  - Yes. It stays inside the admitted concept family and avoids reopening broader module-composition or UI-expansion work.

- Is there any place where the memo quietly assumes the Render deployment has already happened?
  - No quiet assumption is doing major damage here. The memo generally preserves the distinction between local truth and live truth. The only adjustment needed is to stress more explicitly how broken the live analyzer-mgmt detail surfaces still are.

- Is the live browser-acceptance path concrete enough to prove analyzer-v2 is truly the authority for the admitted concept submodes?
  - Not quite. It should add explicit analyzer-mgmt job/result-boundary/provenance checks so the acceptance path proves authority, not just rendering.

## Final Call

`approve with corrections`

The memo is strategically right and locally well-supported. The next honest tranche is indeed live deployment, live authority validation, and bounded thin-client cutover for `inferential` and `logical`.

But before freezing it as-is, add the four corrections above:

- make committed-and-deployed code a three-repo hard gate
- make live analyzer-mgmt engine/chain visibility repair an explicit prerequisite
- require result-boundary/provenance checks in browser acceptance
- require scrutiny to derive from translated analyzer-v2-backed logical output only

With those corrections, the scope is disciplined, justified by the local code, and aligned with the actual live Render gap.
