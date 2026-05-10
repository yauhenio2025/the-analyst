# Codex Audit: Close Read Concept Translated Artifact Authority Live Closeout Scope

Date: 2026-04-11
Verdict: approve with corrections
Target memo: `communications/MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_scope.md`

## Context Check

Read in full:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_and_thin_client_cutover_completion.md`
- `communications/MEMO_2026-04-09_close_read_project_scoped_persistence_and_fresh_scrutiny_closure_completion.md`
- `communications/MEMO_2026-04-09_close_read_roadmap_update_after_project_scoped_persistence_and_scrutiny_closure.md`
- `communications/MEMO_2026-04-09_close_read_translated_artifact_authority_return_scope.md`
- `communications/MEMO_2026-04-11_close_read_temporary_state_snapshot_after_translated_artifact_authority_return.md`
- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Translated_Artifact_Authority_Return_Scope_Audit_2026-04-10.md`
- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Translated_Artifact_Authority_Return_Scope_Critique_2026-04-10.md`

Also inspected directly:

- `/home/evgeny/projects/analyzer-v2`
- `/home/evgeny/projects/the-critic`
- `/home/evgeny/projects/analyzer-mgmt`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/jobs/[id].tsx`
- `/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/implementations/[key].tsx`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_by_ref.py`

Live baseline URLs verified directly:

- analyzer-v2 exact logical artifact route
- analyzer-v2 latest validated logical artifact route
- the-critic logical readback with `X-Project-ID: cutover-project-scope-20260409-121336-u`
- the-critic scrutiny results with `X-Project-ID: cutover-project-scope-20260409-121336-u`
- analyzer-mgmt job page for `job-plan-d9ed0f9db367`

## Bottom Line

The memo identifies the right next corridor.

The live system is already materially past “design the authority seam”:

- analyzer-v2 live exact logical lookup works
- analyzer-v2 live latest validated logical lookup works
- the-critic live logical readback is analyzer-v2-backed and exposes `_artifact_authority`
- the-critic live logical scrutiny readback still works
- analyzer-mgmt live job page can show the concept artifact authority card in-browser

But the corridor is still not formally closed:

- there is still no fresh post-fix proof on a brand-new project
- there is still no paired fresh proof for both admitted modes
- the closeout docs are still unwritten
- the analyzer-mgmt browser surface is real, but it is slow/noisy enough that the memo is correct to insist on browser proof rather than trusting raw HTML or route existence

That makes a bounded closeout tranche the correct next move. Jumping to broader architecture now would stack ambiguity on top of an unclosed corridor.

## Local Vs Live Reality

The memo is directionally honest about local/deployed divergence, and the current repos confirm that warning is necessary.

At audit time, the main local trees were not authoritative:

- `analyzer-v2` local `master` was dirty and behind `origin/master` by 11 commits
- `the-critic` local `master` was dirty and behind `origin/master` by 17 commits
- `analyzer-mgmt` local `master` was dirty and behind `origin/master` by 3 commits

For code inspection I therefore treated the following isolated worktrees as the trustworthy source-aligned local references:

- `/tmp/taa-analyzer-v2` at `1b06e0918670d74e85c74fc1b2978236280c7671`
- `/tmp/taa-the-critic` at `8ecec9de26497bf48bf7f25a499ef21a31500bad`
- `/tmp/taa-analyzer-mgmt` at `63daa08ed7e43433bc0d258919b47a22f5720af3`

This matters because the memo is right to require live verification and source alignment before editing.

## Code Reality Check

The inspected code matches the memo’s general description of the corridor.

`analyzer-v2`

- `src/api/routes/orchestrator.py:402-468` exposes the canonical concept by-ref launch route and the canonical concept artifact read route.
- `src/orchestrator/concept_artifact_authority.py:1079-1128` implements the exact-run lookup by `analyzer_v2_job_id` and the latest-validated lookup gated on `contract_validation_status = passed`.
- `src/orchestrator/concept_by_ref.py:173-186` persists the concept job identity context needed for later provenance and authority auditing.

`the-critic`

- `api/server.py:4098-4166` validates returned analyzer-v2 artifact identity and provenance, computes `artifact_hash`, and stores `_artifact_authority`.
- `api/server.py:4216-4305` launches inferential/logical runs through analyzer-v2 and then performs exact artifact lookup by analyzer-v2 job id.
- `api/server.py:4537-4592` now does project-scoped read-through using canonical `db_analysis.concept`, which is why live `/innovation` and `/Innovation` both resolve.

`analyzer-mgmt`

- `frontend/src/pages/jobs/[id].tsx:1003-1028` fetches the concept artifact from `/v1/orchestrator/concept-analysis-by-ref/result` using `job.analysis_context` plus `job.job_id`.
- `frontend/src/pages/jobs/[id].tsx:1045-1069` and `1132-1139` explicitly keep the concept artifact surface independent of generic result/presenter state.
- `frontend/src/pages/jobs/[id].tsx:879-929` renders the concept artifact authority card with validation, lookup mode, provenance fields, and translated artifact preview.
- `frontend/src/pages/implementations/[key].tsx:1001-1008` correctly frames the implementation page as composition metadata, not the operator proof surface. That scoping is important and the memo is right to preserve it.

## Live Verification

### 1. analyzer-v2 baseline logical authority

Verified live against:

- exact: `job-plan-d9ed0f9db367`
- latest validated: same `consumer_key`, `external_project_id`, `concept_name`, `analysis_mode`

Observed:

- exact lookup returned `200`
- latest validated lookup returned `200`
- exact lookup returned `lookup_mode = exact_run`
- latest lookup returned `lookup_mode = latest_validated`
- both returned `contract_validation_status = passed`
- both returned `analyzer_v2_job_id = job-plan-d9ed0f9db367`
- both returned `workflow_key = concept_logical_single_concept`
- both returned `translation_template_key = concept_logical_host_contract_extraction`
- both returned `engine_or_chain_key = concept_analysis_12_phase`
- both returned `depth = deep`

### 2. the-critic logical readback

Verified live against:

- `/api/concept/analyses/innovation?analysis_type=logical`
- `/api/concept/analyses/Innovation?analysis_type=logical`
- header `X-Project-ID: cutover-project-scope-20260409-121336-u`

Observed:

- lowercase and mixed-case routes both returned `200`
- both returned the same `analyzer_v2_job_id = job-plan-d9ed0f9db367`
- both returned the same artifact hash `b88a09733bc86ed793ba03ec0f3d2d29b334370ec07985b9ecbfe0fb00943470`
- `_analysis_provenance.execution_owner = analyzer-v2`
- `_artifact_authority.source_owner = analyzer-v2`
- `_artifact_authority.contract_validation_status = passed`
- `_artifact_authority.authority_url` points at hosted analyzer-v2, not localhost

### 3. the-critic logical scrutiny baseline

Verified live against:

- `/api/scrutiny/results/innovation`
- header `X-Project-ID: cutover-project-scope-20260409-121336-u`

Observed:

- response returned `200`
- top-level `concept = innovation`
- top-level `count = 1`
- first returned row included:
  - `argument_id = ARG-01`
  - `mode = quick`
  - `premise_index = 0`

Important nuance:

- the live scrutiny row does not currently echo `project_id` or `concept` inside each row
- project identity is still enforced by request header, and concept identity is carried by the route/top-level payload

### 4. analyzer-mgmt browser proof

Verified in a real browser, not by HTTP 200 alone.

For `https://analyzer-mgmt-frontend.onrender.com/jobs/job-plan-d9ed0f9db367`, after allowing the page to hydrate, the Result Boundary tab showed:

- `concept artifact`
- `validation passed`
- `lookup exact_run`
- `logical`
- `Concept: innovation`
- `Analyzer job: job-plan-d9ed0f9db367`
- `Workflow: concept_logical_single_concept`
- `Engine/Chain: concept_analysis_12_phase`
- `Depth: deep`
- `Transformation: concept_logical_host_contract_extraction`
- `Translated Host Artifact`

It also showed exactly the negative condition the memo cares about:

- generic run/result state was still `preparing`
- yet the concept artifact authority card still rendered correctly from the separate concept route

That validates the memo’s insistence that concept artifact truth must not be inferred from generic presenter/result state.

For `https://analyzer-mgmt-frontend.onrender.com/implementations/concept_logical_single_concept`, the page does eventually render in-browser as a composition metadata surface and shows:

- `Canonical composition view`
- `concept_logical_single_concept`
- `Linked Transformations`
- `concept_logical_host_contract_extraction`

But this route is slower and noisier than the job page and should not be treated as the closeout operator proof surface. The memo is correct to keep it out of the acceptance path.

## Corrections Needed

### 1. Tighten the scrutiny verification language to match the live payload shape

The memo currently says the fresh scrutiny readback should return a matching row for:

- project id
- concept
- argument id
- premise index
- `mode = quick`

Live baseline scrutiny readback does not echo `project_id` or `concept` inside each result row. Those are carried by request scope and top-level response instead.

Recommended correction:

- verify project identity by the request header used
- verify concept by the route/top-level `concept`
- verify row-level `argument_id`, `premise_index`, and `mode = quick`

Unless the scrutiny route is intentionally expanded first, the current memo wording over-specifies fields that are not actually present live.

### 2. Make the analyzer-mgmt evidence requirement explicitly browser-hydrated, not just browser-opened

The memo already says “browser-backed operator proof,” which is correct. The live UI confirms that this must be interpreted strictly.

Recommended correction:

- require waiting for hydrated content and visible field confirmation on the job page
- do not treat raw route load, raw HTML, or static shell rendering as proof
- preferably capture screenshot evidence for the Result Boundary tab on both fresh jobs

This is not scope drift. It is an operational clarification forced by the actual hosted frontend behavior.

### 3. Clarify what “authority metadata” means on analyzer-mgmt versus the-critic

The memo’s acceptance language says the same analyzer-v2 job ids and authority metadata should be traced across analyzer-v2, analyzer-mgmt, and the-critic.

That is almost right, but it risks implying a UI requirement the current analyzer-mgmt job page does not satisfy.

Current live reality:

- analyzer-v2 route exposes the authoritative artifact/provenance payload
- analyzer-mgmt job page surfaces route-level artifact identity fields
- the-critic readback additionally surfaces `_artifact_authority.authority_url` and `artifact_hash`

Recommended correction:

- define the required cross-surface identity trail as:
  - analyzer-v2 job id
  - concept
  - analysis mode
  - workflow key
  - engine/chain key
  - translation template key
  - depth
  - produced-at
  - translated artifact identity/preview
- require hosted `authority_url` and `artifact_hash` on the-critic readback
- do not implicitly require analyzer-mgmt to display hash/url unless that is intentionally added as extra UI work

## Answers To The Explicit Audit Questions

### Does the memo correctly treat the current state as “substantially implemented but not formally closed,” or is that diagnosis off?

Yes, that diagnosis is substantially correct.

It slightly understates how much is already live for the baseline logical specimen, but it is still honest overall. The seam is materially implemented. What remains open is the fresh post-fix proof for both admitted modes and the documentation freeze.

### Is a closeout tranche the right next move, or should the program already move to a broader next-stage architecture scope?

A closeout tranche is the right next move.

The strategic roadmaps consistently argue for analyzer-v2 as the analytical brain and thinner hosts. The fastest honest move toward that objective is to close the currently admitted concept authority seam cleanly before opening another architecture corridor.

### Does the memo make the fresh proof requirements concrete enough: exact analyzer-v2 lookup, latest validated lookup, the-critic readback, analyzer-mgmt browser proof, one logical scrutiny regression check?

Mostly yes.

It is concrete enough to execute without major scope drift. The only material correction is the scrutiny payload-shape correction above, plus the need to interpret browser proof as hydrated visible proof rather than mere route access.

### Does the memo keep the proof surface properly bounded to logical, inferential, analyzer-mgmt job pages, and the-critic read-through semantics?

Yes.

This is one of the memo’s strengths.

### Does it correctly avoid reopening host persistence/schema work, generic analyzer-v2 substrate invention, broader Close Read UI redesign, and standalone host extraction?

Yes.

That boundedness is aligned with the strategic memos and with the live state of the current corridor.

### Is the analyzer-mgmt role framed correctly, or does the memo still leave operator-surface responsibility too vague?

It is framed correctly now.

The memo properly assigns operator proof responsibility to analyzer-mgmt job pages and explicitly declines to make implementation/detail pages the artifact proof surface for this tranche. The live browser behavior supports that choice.

### Does the memo keep the-critic in the right role: project-scoped read-through host, compatibility cache, not semantic source of truth?

Yes.

The current code and live readback match that framing.

### Is the analyzer-v2 to analyzer-mgmt to the-critic identity trail concrete enough to be audited?

Yes, with the metadata clarification noted above.

The memo already specifies enough shared fields to compare the three surfaces. It should just avoid implying that analyzer-mgmt must surface the-critic-only hash/url metadata unless that is explicitly added.

### Does the memo stay honest about the dirty/divergent local analyzer-v2 tree and the need to verify deployed truth directly?

Yes, in substance.

If anything, the real situation is broader than the memo’s warning: all three local repos were lagging and dirty enough to justify isolated worktrees and live verification.

### Is there any place where the memo overstates or understates what the live deployed system already proves?

Understates:

- the baseline logical seam is already stronger than a speculative “maybe”; analyzer-v2 exact/latest logical authority, the-critic readback, and analyzer-mgmt job-page operator proof all work live

Overstates or risks overstatement:

- scrutiny row-level field expectations are richer than the current live payload
- “authority metadata across all three surfaces” needs a tighter definition so analyzer-mgmt is not accidentally assigned extra UI scope

### If the larger objective remains analyzer-v2 as the brain and hosts as thinner shells, is this the right next tranche?

Yes.

This tranche is exactly the kind of bounded proof-and-freeze move the strategic memos call for: preserve analyzer-v2 semantic authority, keep the-critic thin, verify the operator trail, then write the closeout docs and move on.

## Final Recommendation

Approve this memo with corrections.

Do not widen the tranche.

Before execution, tighten only these points:

- align the scrutiny verification language with the actual live response shape
- define analyzer-mgmt browser proof as hydrated visible proof, not route availability
- define cross-surface “authority metadata” precisely so analyzer-mgmt is not assigned unintended extra UI work

With those corrections, this memo describes the right next operational corridor.
