# Report: Close Read Concept-Analysis Translated Artifact Authority Return Scope Audit

## Context Check

- `communications/MEMO_2026-04-09_close_read_translated_artifact_authority_return_scope.md` — read in full
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md` — read in full
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` — read in full
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md` — read in full
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` — read in full
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_live_concept_authority_cutover.md` — read in full
- `communications/MEMO_2026-04-06_close_read_concept_analysis_translated_artifact_authority_scope.md` — read in full
- `communications/MEMO_2026-04-09_close_read_project_scoped_persistence_and_fresh_scrutiny_closure_completion.md` — read in full
- `communications/MEMO_2026-04-09_close_read_roadmap_update_after_project_scoped_persistence_and_scrutiny_closure.md` — read in full
- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Project_Scoped_Persistence_Schema_Alignment_Scope_Critique_2026-04-09.md` — read in full
- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Logical_Execution_Completion_Stall_Closure_Scope_Audit_2026-04-07.md` — read in full

## Verdict

`approve with corrections`

The memo is directionally right. The live stack now justifies moving roadmap energy away from host-persistence/scrutiny debugging and back toward analyzer-v2 translated-artifact authority. The tranche is also bounded correctly around `inferential` and `logical`, and it is aligned with the larger “analyzer-v2 as the brain, hosts as thin shells” objective.

The corrections matter, though:

1. the memo overstates current analyzer-mgmt/operator readiness for this concept seam
2. it should acknowledge that analyzer-v2 already has a live dedicated translated-artifact read route, so the next tranche is partly a consolidation/cutover/alignment tranche rather than invention from zero
3. it should explicitly call out local-code alignment, because the live route is not visible in the audited local analyzer-v2 files

## Live-Verified Facts

1. The dedicated analyzer-v2 concept artifact route is live and working.
   - `GET /v1/orchestrator/concept-analysis-by-ref/result?...&analyzer_v2_job_id=job-plan-d9ed0f9db367` returned:
   - `lookup_mode = "exact_run"`
   - `contract_validation_status = "passed"`
   - `translation_template_key = "concept_logical_host_contract_extraction"`
   - a full translated logical artifact with analyzer-v2 provenance

2. The same route also supports project/concept/mode read authority without a job id.
   - `GET /v1/orchestrator/concept-analysis-by-ref/result?...` without `analyzer_v2_job_id` returned:
   - `lookup_mode = "latest_validated"`
   - the same job id `job-plan-d9ed0f9db367`
   - `contract_validation_status = "passed"`

3. The analyzer-v2 executor job completed successfully.
   - `GET /v1/executor/jobs/job-plan-d9ed0f9db367` returned:
   - `status = "completed"`
   - `workflow_key = "concept_logical_single_concept"`
   - `completed_at = "2026-04-09T12:44:36.781949"`
   - progress detail `Materializing translated host artifact`

4. The-critic logical host readback works on the fresh proof project when the project header is supplied.
   - `GET /api/concept/analyses/innovation?analysis_type=logical` with `X-Project-ID: cutover-project-scope-20260409-121336-u` returned the logical artifact with:
   - `_analysis_provenance.execution_owner = "analyzer-v2"`
   - `_analysis_provenance.workflow_key = "concept_logical_single_concept"`
   - `_analysis_provenance.translation_template_key = "concept_logical_host_contract_extraction"`

5. The same the-critic readback still fails without project scoping.
   - `GET /api/concept/analyses/innovation?analysis_type=logical` without `X-Project-ID` returned `404`
   - This means the closure is real, but the header-sensitive host contract remains important and should stay explicit.

6. Hosted scrutiny closure is live enough for the corridor decision.
   - `GET /api/scrutiny/results/innovation` with `X-Project-ID: cutover-project-scope-20260409-121336-u` returned `count = 1`
   - The returned row matches `argument_id = ARG-01`, `premise_index = 0`, `mode = quick`
   - The scrutiny read model is still thin, but the persistence/readback seam is closed enough for roadmap purposes.

7. Analyzer-mgmt’s generic job/result surfaces are not yet aligned to this concept seam.
   - `GET /v1/results/by-job/job-plan-d9ed0f9db367?consumer_key=the-critic` returned:
   - `result_state = "preparing"`
   - `corpus_ref = null`
   - `artifacts_ready = false`
   - `presentation_status = "not_started"`
   - `artifact_families = []`
   - even though the dedicated concept artifact route is already validated live

8. The generic presenter status is actively misaligned on this concept job.
   - `GET /v1/presenter/status/job-plan-d9ed0f9db367?consumer_key=the-critic` returned `artifacts_ready = true`, but the surfaced view inventory is genealogy-shaped:
   - `genealogy_text_profiling`
   - `genealogy_tp_deep_summary`
   - `genealogy_target_profile`
   - etc.
   - That is not a trustworthy operator surface for concept translated-artifact inspection.

9. The analyzer-mgmt frontend pages are live as pages, but that is weaker than operator readiness.
   - `https://analyzer-mgmt-frontend.onrender.com/jobs/job-plan-d9ed0f9db367` returns `200`
   - `https://analyzer-mgmt-frontend.onrender.com/implementations/concept_logical_single_concept` returns `200`
   - But the backing analyzer-v2 APIs above show that the current job/operator data model is still generic-result/presenter oriented rather than concept-translated-artifact oriented.

## Code-Backed Findings

### 1. The-critic still materially owns the translated host-artifact seam

This is the strongest code-backed reason the memo’s architectural diagnosis is correct.

- In `the-critic`, `_run_rebased_concept_analysis(...)`:
  - syncs project documents into analyzer-v2
  - launches analyzer-v2 by ref
  - polls the raw executor job
  - fetches raw phase outputs from `/v1/executor/jobs/{job_id}/phases/1.0`
  - then locally translates those outputs via `translate_inferential_result(...)` / `translate_logical_result(...)`
  - see `api/server.py:3989-4091`

- The translation helpers in `analyzer_v2_recomposition.py` still execute the transformation locally from the-critic, then validate locally, then attach provenance locally.
  - see `analyzer_v2_recomposition.py:96-161`

- The-critic still persists the final translated artifact locally in its own DB and serves readback from that DB.
  - save path: `api/server.py:3842-3901`
  - local DB readback path: `api/server.py:4327-4354`

That is exactly the semantic ownership the memo is trying to reduce.

### 2. The memo is right that the next tranche should stay inside existing substrate, not invent a new layer

The analyzer-v2-side files support a bounded extension approach:

- concept by-ref launch already exists as a workflow/orchestrator/executor path
  - `src/orchestrator/concept_by_ref.py:152-210`
  - `src/api/routes/orchestrator.py:501-545`

- executor persistence is still phase-output oriented plus presentation cache, not a separate concept-only host-artifact subsystem
  - `src/executor/output_store.py:21-120`
  - `src/executor/output_store.py:301-390`

- live Render already proves there is some analyzer-v2 translated-artifact read surface for this seam
  - the dedicated `/v1/orchestrator/concept-analysis-by-ref/result` route is live and works for both exact and latest validated lookup

So the correction is not “invent a new substrate.”
It is:

- formalize concept translated artifacts as first-class analyzer-owned outputs/read models inside the existing analyzer-v2 result/output/orchestrator surfaces
- then cut the-critic and analyzer-mgmt over to those surfaces

### 3. Analyzer-mgmt is not yet concrete enough to serve as the operator surface for this tranche

This is the main reason the verdict is not plain `approve`.

The named analyzer-mgmt pages do useful workflow/composition inspection, but they do not yet amount to a concept translated-artifact operator console.

- The implementation page is explicitly the “canonical composition surface for chain-backed workflows” and focuses on workflow metadata, chains, engines, and linked transformations.
  - `frontend/src/pages/implementations/[key].tsx:1001-1131`

- The workflow page is explicitly the simpler phase/prompt view and also focuses on workflow metadata and linked transformations.
  - `frontend/src/pages/workflows/[key].tsx:377-490`

- The job page tabs are:
  - `Summary`
  - `Manifest`
  - `Decision Trace`
  - `Page Structure`
  - `The-Critic Steering`
  - `Result Boundary`
  - `frontend/src/pages/jobs/[id].tsx:39-54`

- The manifest and result-boundary sections are presenter/result-manifest oriented, not concept translated-artifact oriented.
  - manifest tab shows views, renderer, parent, structuring, derivation
  - result boundary shows result state, artifact families, hashes, links, and linked transformations
  - `frontend/src/pages/jobs/[id].tsx:301-430`
  - `frontend/src/pages/jobs/[id].tsx:945-1210`

- The page does not surface:
  - raw phase 1.0 outputs for the concept run
  - the analyzer-v2 translated host artifact itself
  - `contract_validation_status` from the dedicated concept route
  - concept-specific provenance linkage as a first-class panel

The live APIs confirm the mismatch:

- generic result/run surfaces still show this concept job as effectively unprepared
- generic presenter status surfaces genealogy views on a concept logical job

So analyzer-mgmt is not “already concrete enough.”
It needs explicit tranche work.

### 4. The memo keeps the tranche bounded and preserves analyzer-v2 type discipline

On the main scoping questions, the memo is strong:

- it freezes current inferential/logical host contracts rather than reopening host UI shapes
- it scopes the tranche to `inferential` and `logical`
- it defers new concept submodes, cross-corpus work, broader Close Read UI work, and standalone Close Read host work
- it centers provenance and validation rather than vague host-side convenience

That matches both the strategic roadmap and the actual current technical bottleneck.

## Corrections Needed

1. Reframe analyzer-v2 read authority as consolidation of an already-live seam.
   - The memo currently reads too much like the read surface is entirely future work.
   - Better framing: analyzer-v2 already has a live dedicated concept translated-artifact read route; the next tranche should formalize it, align the local codebase to it, and make it the authoritative path that hosts and analyzer-mgmt actually consume.

2. Make analyzer-mgmt deliverables explicit and page-specific.
   - The memo should say where each responsibility lands:
   - raw phase outputs
   - translated artifact
   - validation status
   - provenance linkage
   - Without that, “analyzer-mgmt should show it” is directionally right but not implementation-ready.

3. Acknowledge local/live alignment work explicitly.
   - In the audited local analyzer-v2 files, I can see the launch path, but not the live dedicated `/result` read route.
   - The tranche should therefore include repo alignment/documentation so the local implementation story matches what is already live.

4. Keep the host contract note concrete.
   - The-critic readback is still project-header scoped.
   - That does not reopen host-correctness as the main roadmap line, but it should stay explicit so this tranche does not accidentally blur the current host contract.

## Direct Answers

### Does the live stack now support the claim that host persistence and scrutiny closure are complete enough to stop spending roadmap energy there?

Yes.

Fresh logical execution closes live, project-scoped host readback closes live, and scrutiny persistence/readback closes live on the same proof project. The remaining issues are not roadmap-dominant blockers. They are residual UX/read-model thinness, not closure failure.

### Is the memo right that the-critic still owns too much of the translated host-artifact seam?

Yes.

The-critic still does the translation/revalidation step itself, persists the translated result locally, and serves local DB readback. That is still too much semantic ownership for the target architecture.

### Does the current codebase support moving more translated-artifact authority into analyzer-v2 without inventing a new substrate layer?

Yes, with a correction.

Use existing workflows, transformations, executor outputs, orchestrator/read surfaces, and analysis-product/result surfaces. Do not invent a new substrate. But explicitly align the local codebase to the already-live dedicated analyzer-v2 concept artifact route.

### Does the memo keep the current host contracts fixed clearly enough?

Yes.

It correctly keeps current inferential/logical host contracts fixed and relocates authority rather than redesigning host rendering.

### Is the proposed analyzer-v2 read/authority boundary concrete enough to be implementable?

Yes.

The live route already proves the key identity model:

- consumer
- project
- concept
- mode
- optional exact analyzer-v2 job id

That is concrete enough for implementation.

### Does the memo make analyzer-v2 provenance and validation ownership concrete enough?

Yes.

The proposed metadata is the right set, and the live dedicated analyzer-v2 route already returns most of it.

### Does it make analyzer-mgmt’s operator responsibility concrete enough:

No, not yet.

- raw phase outputs: No. The named pages do not currently surface them.
- translated artifact: No. The concept translated artifact is not currently surfaced as the operator object on the named pages.
- validation status: Partially. It exists on the dedicated analyzer-v2 route live, but not on the current analyzer-mgmt concept job surface.
- provenance linkage: Partially. Workflow/transformation linkage exists, but concept-artifact provenance is not shown coherently on the live job surface.

### Does it correctly constrain the-critic to a thinner read-through role on `inferential` and `logical` only?

Yes.

That is the right bounded cutover target.

### Does it properly defer:

- new concept submodes
- cross-corpus concept work
- broader Close Read UI work
- standalone Close Read host work

Yes.

Those deferrals are correct and necessary to keep the tranche honest.

### Is there any place where the memo overstates what analyzer-v2 or analyzer-mgmt already expose live today?

Yes.

The overstatement is mainly on analyzer-mgmt/operator readiness, not on analyzer-v2.

- analyzer-mgmt/job/result surfaces are not yet concept-artifact-ready live
- generic result/run/presenter surfaces are still misaligned for this concept seam

The memo also slightly understates analyzer-v2’s live state:

- analyzer-v2 already has a working dedicated concept translated-artifact read route on Render

### Is this the right next tranche if the larger architectural objective remains analyzer-v2 as the brain and hosts as thin shells?

Yes.

This is the right next tranche, provided the corrections above are applied.

## Tightened Bottom Line

Approve the tranche, but tighten the memo to say:

- host persistence and scrutiny closure are sufficiently complete live; stop spending primary roadmap energy there
- the-critic still materially owns translation/persistence/readback and should be thinned
- analyzer-v2 already has a live dedicated concept translated-artifact read seam; the next tranche should formalize and cut consumers over to it
- analyzer-mgmt is not yet the operator surface for this seam, so the tranche must include explicit analyzer-mgmt page/API work for raw outputs, translated artifact, validation, and provenance

That keeps the tranche both honest and implementable.
