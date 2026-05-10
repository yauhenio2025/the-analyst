# Context Check

All required documents below were read in full on 2026-04-06.

- Read `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_runtime_authority_and_analyzer_mgmt_visibility_scope.md`
- Read `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
- Read `communications/MEMO_2026-04-06_close_read_concept_analysis_analyzer_v2_recomposition_scope.md`
- Read `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`
- Read `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`
- Read `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- Read `communications/MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md`
- Read `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- Read `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- Read `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- Read `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- Read `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- Read `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

# Verdict

**Approve with corrections.**

The memo’s core diagnosis is correct: the live problem is not missing concept-analysis primitives, and the next honest move is to make analyzer-v2 the deployed runtime authority for bounded concept workflows plus host-contract transformations. The corrections are about precision and operator-surface honesty, not about the memo’s main direction.

# Direct Answers

- Does the live Render server already prove that the core concept-analysis primitives exist?
  Yes. Live analyzer-v2 already serves the `inferential_commitment_mapper` engine, its operationalization, and the `concept_analysis_12_phase` chain, along with the constituent concept-analysis engines.

- Is the memo right that the missing live layer is concept workflows, concept host-contract transformations, and a bounded concept orchestrator route rather than missing engines/chains?
  Yes. That is the live gap. Engines/chains are already deployed; the concept workflows, host-contract transformations, and concept by-ref orchestrator route are not.

- Does the memo correctly avoid inventing new substrate types?
  Yes. The proposed move stays inside existing analyzer-v2 types: engines, operationalizations, chains, workflows, and transformations.

- Is the proposed analyzer-mgmt visibility law concrete enough, or does it still leave an ambiguous operator surface?
  It still leaves an ambiguous operator surface. analyzer-mgmt has the right broad surfaces, but the memo should specify which page is canonical for composition visibility and require concrete fixes for chain-backed workflows and workflow-to-transformation linkage.

- Does the memo correctly identify what Critic should still own versus stop owning?
  Mostly yes, but it should be tightened. Critic should still own document sync initiation, launch bridging, polling, rendering, and a temporary host-local scrutiny/runtime seam. It should stop owning canonical execution semantics, workflow composition, transformation-template ownership, and semantic-contract authority.

- Is the “analyzer-v2 produces translated host-contract artifacts” move the right next step, or does the code suggest a more prior blocker?
  It is the right next architectural step, but there is a more prior operational blocker: those concept workflows, transformation templates, and the concept by-ref route are still local-only and not deployed on Render. A second correction is that analyzer-mgmt needs minor but real visibility fixes before it can honestly be called the canonical operator console.

- Does the memo stay properly narrower than broader module-composition work, new Close Read UI work, and standalone Close Read host work?
  Yes. It stays properly narrower than all three and is consistent with the prior family-boundary and roadmap memos.

- Is there any place where the memo quietly treats local code existence as equivalent to deployed analyzer authority?
  Slightly, but only around analyzer-mgmt readiness. The memo is mostly disciplined about distinguishing local code from live authority. The slippage is that existing analyzer-mgmt route shells are treated as equivalent to concrete operator visibility, even though the live concept workflow pages currently fail and the local workflow detail page is not chain-aware.

# Why The Core Thesis Holds

The memo is right on the main point because the live server already proves the concept-analysis capability bricks exist.

Live evidence checked directly on 2026-04-06:

- `GET https://analyzer-v2.onrender.com/v1/meta/definitions-version` returned `200` with `engine_count: 202`, `chain_count: 26`, `workflow_count: 8`, and `last_modified: 2026-03-18 13:44:31 UTC`.
- `GET https://analyzer-v2.onrender.com/v1/engines` returned `200` and includes `inferential_commitment_mapper` plus concept-analysis engines such as `concept_argument_formalization`, `concept_vulnerability_inferential_gaps`, and `concept_synthesis`.
- `GET https://analyzer-v2.onrender.com/v1/engines/inferential_commitment_mapper` returned `200`.
- `GET https://analyzer-v2.onrender.com/v1/chains` returned `200` and includes `concept_analysis_12_phase` and `concept_analysis_suite`.
- `GET https://analyzer-v2.onrender.com/v1/chains/concept_analysis_12_phase` returned `200`.
- `GET https://analyzer-v2.onrender.com/v1/operationalizations` redirected, then returned `200`, and `GET https://analyzer-v2.onrender.com/v1/operationalizations/inferential_commitment_mapper` returned the full stance/depth structure.

Local code inspection matches that live proof:

- `src/engines/definitions/inferential_commitment_mapper.json:2-10` defines the engine and its canonical inferential schema.
- `src/operationalizations/definitions/inferential_commitment_mapper.yaml:3-128` defines the four stances `discovery`, `confrontation`, `dialectical`, `integration` and the three depth profiles `surface`, `standard`, `deep`.
- `src/chains/definitions/concept_analysis_12_phase.json:2-99` defines the full 12-phase logical/concept chain.

That means the memo is correct to say the missing live layer is composition and authority, not primitive capability invention.

# Where The Live Gap Actually Is

The missing live layer is exactly the one the memo identifies.

Live deployment evidence:

- `GET https://analyzer-v2.onrender.com/v1/workflows` returned `200`, but only 8 workflows are live, and neither `concept_inferential_single_concept` nor `concept_logical_single_concept` is present.
- `GET https://analyzer-v2.onrender.com/v1/workflows/concept_inferential_single_concept` returned `404`.
- `GET https://analyzer-v2.onrender.com/v1/workflows/concept_logical_single_concept` returned `404`.
- `GET https://analyzer-v2.onrender.com/v1/transformations` returned `200`, but only 24 templates are live, and neither concept host-contract extraction template is present.
- `GET https://analyzer-v2.onrender.com/v1/transformations/concept_inferential_host_contract_extraction` returned `404`.
- `GET https://analyzer-v2.onrender.com/v1/transformations/concept_logical_host_contract_extraction` returned `404`.
- `GET`, `POST`, and `OPTIONS` against `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref` all returned `404`, so the concept by-ref route is not live on Render.

Local code shows those missing live resources do already exist locally:

- `src/workflows/definitions/concept_inferential_single_concept.json:2-31`
- `src/workflows/definitions/concept_logical_single_concept.json:2-31`
- `src/transformations/definitions/concept_inferential_host_contract_extraction.json:2-123`
- `src/transformations/definitions/concept_logical_host_contract_extraction.json:2-156`
- `src/api/routes/orchestrator.py:501-530`
- `src/orchestrator/concept_by_ref.py:152-210`

The local/live mismatch is also concrete numerically:

- Local workflow definition files: `10`
- Live workflows in Render definitions: `8`
- Local transformation definition files: `26`
- Live transformations in Render: `24`

On 2026-04-06 the relevant local analyzer-v2 files are also not all cleanly landed: `git status --short` shows the concept workflow files, transformation files, and `src/orchestrator/concept_by_ref.py` as untracked, with `src/api/routes/orchestrator.py` modified. So local existence is especially not equivalent to deployed authority here.

# What Critic Still Owns, And Should Stop Owning

The memo’s direction is right, but the boundary should be stated more precisely.

What Critic is already doing in the rebased path:

- `the-critic/api/server.py:3963-4058` launches analyzer-v2 by synced registered corpus, polls analyzer-v2 jobs, fetches analyzer-v2 phase outputs, and translates them through analyzer-v2-backed templates.
- `the-critic/analyzer/concept_analyzer/analyzer_v2_client.py:838-880` is already wired to `POST /v1/orchestrator/concept-analysis-by-ref`.
- `the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py:11-12` and `:96-156` treat the host-contract translation templates as analyzer-v2 assets and validate them against Critic result contracts.

What Critic still owns today and should keep only temporarily:

- Document sync initiation and registered-corpus launch bridging.
- Polling and host-facing job state.
- Local result persistence in the Critic DB/disk read model: `the-critic/api/server.py:4131-4134`.
- Logical scrutiny follow-up execution and persistence: `the-critic/api/server.py:6724-6905`.

What Critic should stop owning as canonical truth:

- Inferential/logical execution semantics.
- Workflow/chain composition authority.
- Transformation-template ownership.
- Semantic host-contract materialization as the authority layer.

So the memo is right that Critic should become thin, but it should say explicitly that the remaining Critic obligations are a launch/render bridge plus transitional local read-model and scrutiny seams until analyzer-v2 is serving the authoritative translated artifacts.

# The analyzer-mgmt Correction

The memo is directionally right to treat analyzer-mgmt as the right console, and it is right not to invent a separate admin layer. But the current operator surface is not yet concrete enough to call “canonical” without correction.

What is already true:

- analyzer-mgmt is built to call analyzer-v2 directly on Render, not a parallel store: `frontend/src/lib/api.ts:83`, `:465-565`, `:676-856`, `:1953-2039`.
- Engine detail already cross-links to operationalizations: `frontend/src/pages/engines/[key].tsx:778-789` and `:1329-1334`.
- Transformation detail is a real editable/testable surface with create, update, delete, execute-test, applicability, and primitive-affinity controls: `frontend/src/pages/transformations/[key].tsx:418-520` and `:520-900`.
- Jobs already expose result-boundary, run-boundary, presenter status, trace, and page data: `frontend/src/lib/api.ts:696-856`; `frontend/src/pages/jobs/[id].tsx:1295-1459`.

What is still wrong or ambiguous:

- The workflow detail page is not chain-aware. It always renders `phase.engine_key` and links to `/engines/${phase.engine_key}`. That means a chain-backed workflow such as `concept_logical_single_concept` cannot be represented honestly there: `frontend/src/pages/workflows/[key].tsx:96-106`. There is no `chain_key` handling in that file.
- The implementations detail page is closer to the right composition view, but its chain link is wrong. It links a chain-backed phase to `/workflows/${phase.chain_key}` instead of `/chains/${phase.chain_key}`: `frontend/src/pages/implementations/[key].tsx:686-694`.
- Neither the workflow detail page nor the implementations detail page surfaces workflow-to-transformation linkage. So the operator still cannot see, from one canonical page, “this workflow produces raw analyzer output, then this host-contract transformation.”
- The jobs page is useful but still leaves `workflow_key` as plain text rather than a navigable workflow detail link: `frontend/src/pages/jobs/[id].tsx:1311-1317`.
- On live Render, the concept workflow detail page already fails because the upstream workflow is missing. `https://analyzer-mgmt-frontend.onrender.com/workflows/concept_inferential_single_concept` and `.../concept_logical_single_concept` both render a failure state.

So the memo should require a concrete visibility law, not just “existing surfaces” in the abstract.

The missing concrete law is:

- `engines/[key]` plus `operationalizations/[key]` remain the inferential capability-definition anchors.
- `chains/[key]` remains the logical capability-definition anchor.
- `implementations/[key]` should be the canonical composition page for a workflow, not `workflows/[key]`, unless `workflows/[key]` is made chain-aware.
- `transformations/[key]` should be the canonical host-contract extraction page.
- `jobs/[id]` should be the canonical runtime/result-boundary page.
- Workflow pages must explicitly link to their transformation templates, and job pages should link back to workflow and transformation pages.

# Does The Memo Stay Narrow Enough?

Yes.

Relative to the prior memos, this memo stays properly narrower than:

- broader default-family plus bespoke composition-layer work
- new Close Read UI design work
- standalone Close Read host work

That narrowness is one of the memo’s strengths. It correctly treats this as the operational completion of the recomposition story, not as a new product-boundary expansion.

# Final Call

Approve with corrections.

The memo is substantively right about the live strategic diagnosis:

- live Render already proves the concept-analysis primitives exist
- the missing live layer is workflows, host-contract transformations, and the concept by-ref route
- no new analyzer-v2 substrate types are needed
- Critic should be reduced toward a thin host
- analyzer-mgmt is the right console family, not a new admin app

But the corrected version should say three things more explicitly:

1. The concept workflows, host-contract transformations, and concept by-ref route are local-only on 2026-04-06 and not live on Render.
2. analyzer-mgmt needs a concrete canonical operator law, because the current workflow surface is not chain-aware and does not expose workflow-to-transformation linkage.
3. Critic still keeps a temporary sync/launch/render/scrutiny bridge until analyzer-v2 is actually serving translated host-contract artifacts as the authority layer.

With those corrections, this is the right next scope.
