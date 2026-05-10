Please review this next-stage scoping memo in full:

- `communications/MEMO_2026-04-13_close_read_public_host_topology_and_admitted_family_umbrella_publication_scope.md`

Before concluding, read all of these in full. Do not skip any:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-05_close_read_post_v1_recalibration_multi_engine_boundary.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- `communications/MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_completion.md`
- `communications/MEMO_2026-04-13_close_read_admitted_concept_operator_surface_and_thin_host_simplification_completion.md`
- `communications/MEMO_2026-04-13_close_read_roadmap_update_after_admitted_concept_operator_surface_and_thin_host_simplification_completion.md`

Inspect these codebases directly:

- `/home/evgeny/projects/analyzer-v2`
- `/home/evgeny/projects/the-critic`
- `/home/evgeny/projects/analyzer-mgmt`

Important operational rule:

- do not assume the main local checkouts match deployed truth
- do not assume `render.yaml` reflects the actual public deployment topology without verification
- if local, configured, and live topology diverge, call that out explicitly

Inspect at least these files directly:

- `/home/evgeny/projects/the-critic/render.yaml`
- `/home/evgeny/projects/the-critic/webapp/public/_redirects`
- `/home/evgeny/projects/the-critic/webapp/src/routes.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadAoiPages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/closeReadConceptRuntime.ts`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`

Also inspect the live deployed state directly. Do not rely only on local code.

Check these public and API URLs explicitly:

- stale-config candidates:
  - `https://benanav-web.onrender.com/p/cutover-concept-artifact-closeout-20260411-090918/close-read`
  - `https://benanav-api.onrender.com/api/concept/analyses/innovation?analysis_type=logical`
- actual live host candidates established by the April 13 reviews:
  - `https://the-critic-1.onrender.com/p/cutover-concept-artifact-closeout-20260411-090918/close-read`
  - `https://the-critic-1.onrender.com/p/cutover-concept-artifact-closeout-20260411-090918/close-read/genealogy`
  - `https://the-critic-1.onrender.com/p/cutover-concept-artifact-closeout-20260411-090918/close-read/aoi`
  - `https://the-critic-1.onrender.com/p/cutover-concept-artifact-closeout-20260411-090918/close-read/concepts`
- `https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical` with header `X-Project-ID: cutover-concept-artifact-closeout-20260411-090918`
- `https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=inferential` with header `X-Project-ID: cutover-concept-artifact-closeout-20260411-090918`
- `https://the-critic.onrender.com/api/scrutiny/results/innovation` with header `X-Project-ID: cutover-concept-artifact-closeout-20260411-090918`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?consumer_key=the-critic&external_project_id=cutover-concept-artifact-closeout-20260411-090918&concept_name=innovation&analysis_mode=logical&analyzer_v2_job_id=job-plan-fcc8b88fa4fc`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?consumer_key=the-critic&external_project_id=cutover-concept-artifact-closeout-20260411-090918&concept_name=innovation&analysis_mode=inferential&analyzer_v2_job_id=job-plan-077aeca1ffc8`

What I need from you:

1. Test the robustness of the memo’s assumptions.
2. Examine them in light of the bigger `analyzer-v2 as the brain` objective and the broader Close Read roadmap.
3. Scrutinize the memo’s claims against the codebase and the live deployed stack.
4. Evaluate whether this is the right next tranche after the admitted concept normalization completion.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Does the memo correctly move the roadmap from admitted concept normalization into public Close Read surface verification/hardening, or is that transition premature?
- Is the public-host-topology audit genuinely the first necessary step, or should the memo now treat the host pair as already established and move immediately to browser-truth verification on `the-critic-1`?
- Does the memo keep the larger direction clear enough:
  - analyzer-v2 as the brain
  - analyzer-mgmt as operator console
  - the-critic webapp as the current Close Read product shell
  - broader standalone extraction later?
- Is the admitted family set correctly frozen here, or is the memo still too loose about family admission?
- Does the memo keep family-specific pages and native-route coexistence in the right role, or is it drifting toward premature shell unification?
- Is the shared admitted-family baseline concrete enough to implement and audit?
- Does the memo stay honest about local-vs-live and configured-vs-live topology divergence?
- Is there any place where the memo overstates or understates what the public product surface already proves today, especially given that route-level `200` may still be weaker than hydrated browser proof?
- If you were protecting roadmap discipline, is this the right next corridor before broader Close Read extraction or a new family/submode line?

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the review to this exact file:

- `communications/REPORT_Claude_Close_Read_Public_Host_Topology_And_Admitted_Family_Umbrella_Publication_Scope_Critique_2026-04-13.md`
