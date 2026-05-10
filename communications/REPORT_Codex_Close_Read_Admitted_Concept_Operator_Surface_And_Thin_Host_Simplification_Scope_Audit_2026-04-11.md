# Codex Audit: Close Read Admitted Concept Operator Surface And Thin Host Simplification Scope

Date: 2026-04-11
Verdict: approve with corrections
Target memo: `communications/MEMO_2026-04-11_close_read_admitted_concept_operator_surface_and_thin_host_simplification_scope.md`

## Context Check

Read in full:

- `communications/MEMO_2026-04-11_close_read_admitted_concept_operator_surface_and_thin_host_simplification_scope.md`
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-11_close_read_temporary_state_snapshot_after_translated_artifact_authority_return.md`
- `communications/MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_completion.md`
- `communications/MEMO_2026-04-11_close_read_roadmap_update_after_concept_translated_artifact_authority_live_closeout.md`
- `communications/MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_scope.md`
- `communications/REPORT_Codex_Close_Read_Concept_Translated_Artifact_Authority_Live_Closeout_Scope_Audit_2026-04-11.md`
- `communications/REPORT_Claude_Close_Read_Concept_Translated_Artifact_Authority_Live_Closeout_Scope_Critique_2026-04-11.md`

Inspected directly:

- `/home/evgeny/projects/analyzer-v2`
- `/home/evgeny/projects/the-critic`
- `/home/evgeny/projects/analyzer-mgmt`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/jobs/[id].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/implementations/[key].tsx`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_by_ref.py`

Verified live directly:

- analyzer-v2 exact and latest logical artifact routes for `job-plan-fcc8b88fa4fc`
- analyzer-v2 exact and latest inferential artifact routes for `job-plan-077aeca1ffc8`
- the-critic logical and inferential readback on project `cutover-concept-artifact-closeout-20260411-090918`
- the-critic scrutiny readback on the same project
- analyzer-mgmt live job pages for both fresh analyzer-v2 jobs
- analyzer-mgmt live implementation page for `concept_logical_single_concept`

## Bottom Line

The memo picks the right next corridor.

The transition from proof into normalization is not premature on April 11, 2026. The admitted seam is already live and real in deployed behavior:

- analyzer-v2 exact-run lookup passes for both `logical` and `inferential`
- analyzer-v2 latest-validated lookup passes for both `logical` and `inferential`
- the-critic readback is analyzer-v2-backed for both admitted modes and exposes `_artifact_authority`
- the-critic scrutiny still works on the fresh logical artifact
- analyzer-mgmt already shows a real concept-artifact authority card on the Result Boundary tab for both fresh jobs

What remains unnormalized is also real:

- analyzer-mgmt generic result-boundary state still says `preparing` / `artifacts pending` / `presentation not_started` while the concept-artifact card already shows `validation passed` and `lookup exact_run`
- the Result Boundary tab is hydration-laggy enough that route existence or static HTML is not proof
- the dirty local trees diverge sharply from deployed truth, including the repo that this tranche mainly wants to touch: `analyzer-mgmt`

So the next honest move is not another proof tranche and not broader Close Read extraction.
It is exactly this narrower operator-surface and thin-host normalization tranche.

## Local Vs Live Reality

The memo is correct to warn about local/deployed divergence, but it underspecifies the operational problem.

At audit time on 2026-04-11:

- `analyzer-v2` local `HEAD = 01427880e1c4c5ddb896b8b0c7fb8c74f6b228c9`, `origin/master = 1b06e0918670d74e85c74fc1b2978236280c7671`, behind by `11` commits, dirty in `1184` paths
- `the-critic` local `HEAD = 6b41312b6d46fea1c112ac629f90dc43268e5ed0`, `origin/master = 8ecec9de26497bf48bf7f25a499ef21a31500bad`, behind by `17` commits, dirty in `301` paths
- `analyzer-mgmt` local `HEAD = 650016c261047b0b4b446a78dd2ec9f9607b805f`, `origin/master = 63daa08ed7e43433bc0d258919b47a22f5720af3`, behind by `3` commits, dirty in `25` paths

That matters because the main local trees materially disagree with deployed behavior on the exact seam this memo wants to normalize.

Concrete examples:

- local `analyzer-v2` has the POST by-ref launch route, but its main checkout does not have the deployed translated-artifact authority file and does not persist `_concept_by_ref_context` in `concept_by_ref.py`
- local `the-critic` still shows the older “poll executor -> fetch phase outputs -> local translation” path in `_run_rebased_concept_analysis(...)`
- local `analyzer-mgmt` job page lacks the deployed concept-artifact authority card entirely, and local frontend API/types also lack the deployed concept-artifact lookup contract

So the memo must not frame the divergence warning as only an `analyzer-v2` / `the-critic` issue.
For this tranche, `analyzer-mgmt` must be included explicitly in the same non-negotiable rule.

## Deployed-Source-Aligned Code Check

The deployed-source-aligned code matches the memo’s intended architecture.

`analyzer-v2`

- `origin/master:src/api/routes/orchestrator.py:402-470` exposes both the by-ref launch route and `GET /concept-analysis-by-ref/result`
- `origin/master:src/orchestrator/concept_by_ref.py:173-186` persists `_concept_by_ref_context` into `plan_data`
- `origin/master:src/orchestrator/concept_artifact_authority.py:968-1007` extracts analyzer-side concept job context for downstream consumers
- `origin/master:src/orchestrator/concept_artifact_authority.py:1079-1128` implements exact-run lookup by `analyzer_v2_job_id` and latest-validated lookup gated on `contract_validation_status = passed`

`the-critic`

- `origin/master:api/server.py:4030-4169` defines the exact contract for admitted logical vs inferential artifact identity and computes `_artifact_authority`
- `origin/master:api/server.py:4172-4213` does project-scoped analyzer-v2 read-through on concept readback
- `origin/master:api/server.py:4216-4305` launches through analyzer-v2 and then reads the translated artifact from analyzer-v2 exact authority, not from a live local semantic recomposition path
- `origin/master:api/server.py:4537-4592` refreshes cached concept results through analyzer-v2 authority during project-scoped readback

`analyzer-mgmt`

- `origin/master:frontend/src/pages/jobs/[id].tsx:879-930` defines `ConceptArtifactAuthorityCard`
- `origin/master:frontend/src/pages/jobs/[id].tsx:1003-1029` fetches the concept artifact from analyzer-v2 using `job.analysis_context` plus `job.job_id`
- `origin/master:frontend/src/pages/jobs/[id].tsx:1045-1070` keeps the concept-artifact line explicitly separate from generic result-boundary availability
- `origin/master:frontend/src/pages/jobs/[id].tsx:1132-1139` renders the concept-artifact card on the Result Boundary tab
- `origin/master:frontend/src/pages/implementations/[key].tsx:1001-1008` explicitly frames the implementation page as the canonical composition surface, not the operator artifact-truth surface

This is the right architecture for the tranche the memo wants:

- analyzer-v2 owns semantic authority
- the-critic is a project-scoped read-through/cache host
- analyzer-mgmt is the operator-facing job surface
- implementation/detail pages stay in the composition metadata role

## Live Verification

### 1. analyzer-v2 fresh project authority is live for both admitted modes

Verified on project `cutover-concept-artifact-closeout-20260411-090918`.

Logical:

- exact lookup for `job-plan-fcc8b88fa4fc` returned `200`
- latest lookup returned `200`
- `workflow_key = concept_logical_single_concept`
- `engine_or_chain_key = concept_analysis_12_phase`
- `translation_template_key = concept_logical_host_contract_extraction`
- `depth = deep`
- `contract_validation_status = passed`
- exact `lookup_mode = exact_run`
- latest `lookup_mode = latest_validated`

Inferential:

- exact lookup for `job-plan-077aeca1ffc8` returned `200`
- latest lookup returned `200`
- `workflow_key = concept_inferential_single_concept`
- `engine_or_chain_key = inferential_commitment_mapper`
- `translation_template_key = concept_inferential_host_contract_extraction`
- `depth = standard`
- `contract_validation_status = passed`
- exact `lookup_mode = exact_run`
- latest `lookup_mode = latest_validated`

### 2. the-critic is live as a project-scoped read-through host, not the semantic source

Logical readback with header `X-Project-ID: cutover-concept-artifact-closeout-20260411-090918` returned:

- `_analysis_provenance.execution_owner = analyzer-v2`
- `_analysis_provenance.analyzer_v2_job_id = job-plan-fcc8b88fa4fc`
- `_artifact_authority.source_owner = analyzer-v2`
- hosted analyzer-v2 `authority_url`
- `artifact_hash = c48edc96ba79f7a3db93e0d1f1ab0eaca4edc3243a68cd0d6d7bdcb624c32658`
- `contract_validation_status = passed`

Inferential readback returned the same pattern, with:

- `_analysis_provenance.analyzer_v2_job_id = job-plan-077aeca1ffc8`
- `artifact_hash = 8ab53412ea2d4274d896706d07005a61c8afec71e79225471fadfd178e64efc2`

Without the `X-Project-ID` header, logical readback returned `404`.
That is the right project-scoped host behavior.

### 3. scrutiny still works on the analyzer-v2-backed logical artifact

`GET /api/scrutiny/results/innovation` with the same project header returned:

- `concept = innovation`
- `count = 1`
- first row `argument_id = A1`
- first row `premise_index = 0`
- first row `mode = quick`

### 4. analyzer-mgmt already has the operator-facing concept-artifact card live

Live browser verification on April 11, 2026 showed:

- `https://analyzer-mgmt-frontend.onrender.com/jobs/job-plan-fcc8b88fa4fc`
- `https://analyzer-mgmt-frontend.onrender.com/jobs/job-plan-077aeca1ffc8`

On the Result Boundary tab, after allowing the page to hydrate, both fresh jobs showed a concept-artifact authority card with:

- `concept artifact`
- `validation passed`
- `logical` or `inferential`
- `lookup exact_run`
- `Concept: innovation`
- `Project: cutover-concept-artifact-closeout-20260411-090918`
- `Analyzer job: ...`
- `Workflow: ...`
- `Engine/Chain: ...`
- `Depth: ...`
- `Transformation: ...`
- `Translated Host Artifact`

Important live nuance:

- the same Result Boundary tab also still showed generic result-boundary state such as `preparing`, `artifacts pending`, `presentation inactive`, `restore unavailable`, and `preparation not_run`
- for the logical job, staleness reasons included `missing_corpus_ref` and `preparation_not_run`

That means the memo is directionally right:

- analyzer-mgmt already has the right operator surface
- but the generic result-boundary state is still not aligned with the concept-artifact truth
- that mismatch is a real hardening target

### 5. implementation pages are live as composition metadata, not operator artifact truth

Live browser verification on:

- `https://analyzer-mgmt-frontend.onrender.com/implementations/concept_logical_single_concept`

showed:

- `Canonical composition view`
- workflow metadata
- `Linked Transformations`
- pipeline flow

This is the right role.
The implementation page is not the artifact/operator proof surface.

## What The Memo Gets Right

### 1. It correctly moves the roadmap from proof into normalization

The current seam is already live enough that another broad proof tranche would be drift.
The fresh April 11 project already proved both admitted modes, scrutiny, the-critic authority readback, and analyzer-mgmt job-surface visibility.

### 2. It chooses the right next operator tranche

Analyzer-mgmt job-surface hardening is the right next bounded move because the live job surface already exists but still carries generic-state ambiguity.

### 3. It keeps implementation/detail pages in the right role

The memo is right to keep implementation pages as workflow/composition metadata surfaces.
The live implementation page and the deployed code both support that reading.

### 4. It keeps the-critic in the right role

The live system now supports exactly the role the memo describes:

- project-scoped read-through host
- compatibility cache
- not the semantic source of truth

### 5. It stays bounded to admitted modes

The memo does not drift into:

- new concept submodes
- broader Close Read extraction
- cross-corpus concept work
- standalone host work

That boundedness is correct.

## Corrections Required

### 1. Add `analyzer-mgmt` to the non-negotiable local-vs-live rule

Right now the memo explicitly warns against trusting main local `analyzer-v2` and `the-critic`.
That is not enough.

For this tranche, `analyzer-mgmt` must be named explicitly in the same rule because its main local tree is also dirty, behind deployed-source-aligned `origin/master`, and missing the live concept-artifact surface.

### 2. Reframe analyzer-mgmt work as hardening of an already-live surface, not first-time invention

The deployed job page already has the concept-artifact authority card and the separate query path to analyzer-v2 authority.

So the work should be framed as:

- normalize loading/error/hydration behavior
- align generic result-boundary state with concept-artifact truth
- improve explicit operator clarity

Not:

- build the surface from scratch

### 3. Tighten the shared authority-field law

The memo’s field list is close, but it should explicitly freeze:

- `consumer_key`
- `external_project_id`
- `concept_name`
- `analysis_mode`
- `analyzer_v2_job_id`
- `workflow_key`
- `engine_or_chain_key`
- `translation_template_key`
- `depth`
- `produced_at`
- `contract_validation_status`
- `lookup_mode`

It is still correct to leave these as the-critic-local compatibility fields:

- `authority_url`
- `artifact_hash`

### 4. Clarify the-critic cleanup so it does not widen into fake work

The active deployed path is already analyzer-v2 exact-read-through plus identity validation.

So any cleanup item should be phrased as:

- remove or gate dead admitted-mode local branches that are no longer part of the live path

Not:

- reopen live semantic-authoring work that is already cut over in deployed code

### 5. Name the live operator inconsistency explicitly

The live issue is not only “hydration lag.”
It is the concrete mismatch:

- concept-artifact card says `validation passed` and `lookup exact_run`
- generic result-boundary state still says `preparing`, `artifacts pending`, `presentation not_started`

That should be named directly as the hardening target.

## Answers To The Explicit Questions

- Does the memo correctly move the roadmap from proof into normalization, or is that transition premature?
  - Yes. It is not premature. The live seam already proves enough to justify normalization.

- Is analyzer-mgmt job-surface hardening the right next bounded operator tranche?
  - Yes. But it should be framed as hardening an already-live concept-artifact card plus generic-state cleanup, not greenfield page creation.

- Does the memo keep implementation/detail pages in the right role, or does it leave artifact/operator responsibility too vague?
  - It keeps them in the right role. Implementation pages are composition metadata surfaces; job pages are the artifact/operator surface.

- Does the memo keep the-critic in the right role: project-scoped read-through host, compatibility cache, not semantic source of truth?
  - Yes. That is exactly what the deployed code and live behavior now show.

- Is the shared authority-field law concrete enough to audit across analyzer-v2, analyzer-mgmt, and the-critic?
  - Mostly. Add `consumer_key`, `external_project_id`, `contract_validation_status`, and `lookup_mode` explicitly.

- Does the memo keep the scope tightly bounded to admitted concept modes without drifting into broader Close Read extraction?
  - Yes.

- Does it stay honest about the dirty/divergent local trees and the need to check deployed truth directly?
  - Partly. It must explicitly include `analyzer-mgmt`, not only `analyzer-v2` and `the-critic`.

- Is there any place where the memo overstates or understates what the live deployed system already proves?
  - It understates two things:
    - deployed analyzer-mgmt already has the concept-artifact card live
    - deployed the-critic is already on exact analyzer-v2 translated-artifact read-through with identity validation
  - It mildly overstates one risk:
    - live admitted-mode recomposition risk in the-critic is now mostly a stale-local-tree problem, not the active deployed path

- If the larger goal remains `analyzer-v2` as the brain and hosts as thinner shells, is this the right next tranche?
  - Yes. This tranche directly sharpens that split without reopening broader architecture.

## Final Recommendation

Approve with corrections.

Do not widen the tranche.

The next honest move is:

1. start from deployed-source-aligned truth across all three repos
2. freeze the shared authority identity fields more explicitly
3. harden analyzer-mgmt’s already-live job surface so the generic boundary state stops contradicting the concept-artifact truth
4. keep the-critic cleanup limited to admitted-mode dead branches and compatibility-cache explicitness

That is the right bounded step if the program still means:

- analyzer-v2 as the brain
- hosts as thinner shells
- operator truth visible without semantic ambiguity
