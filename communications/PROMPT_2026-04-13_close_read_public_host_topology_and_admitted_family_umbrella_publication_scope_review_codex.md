Please audit this next-stage scoping memo:

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
- do not assume the configured Render service names are the same as the actually used public hosts
- if local code, render config, and live routes disagree, call that out explicitly

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

Also verify the live deployed state directly. Do not rely only on local code.

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

Audit goals:

1. Stress-test whether the memo identifies the right next operational corridor.
2. Check whether the proposed tranche is concrete enough to implement without scope drift.
3. Evaluate whether the memo preserves analyzer-v2 authority and stays out of unnecessary concept-internal work.
4. Test whether the memo’s assumptions match the live public-host state, local code, and render configuration.
5. Give a clear verdict:
   - approve
   - approve with corrections
   - reject

Please answer these explicitly:

- Does the memo correctly move the roadmap from admitted concept normalization into public host verification/hardening of the `Close Read` umbrella?
- Is the host-topology ambiguity real enough to justify Phase 0 as written, or should the memo now treat `the-critic-1`/`the-critic` as the frozen live pair and focus on browser-truth verification?
- Does the memo keep the admitted family set and submode boundary concrete enough?
- Does it keep family-specific pages and native-route coexistence in the right role, or does it drift toward premature unification?
- Does it keep analyzer-v2 in the right role:
  - semantic authority
  - not the place where this tranche should spend its code budget?
- Is the shared admitted-family product baseline concrete enough to verify?
- Does the memo stay honest about local-vs-live and configured-vs-live divergence?
- Is there any place where the memo overstates or understates what the public product surface already proves, especially where route-level `200` may still be weaker than hydrated browser proof?
- If the larger goal remains `analyzer-v2` as the brain and hosts as thinner shells, is this the right next tranche?

At the top of your output, include a short section called `Context Check` listing every required memo above and confirming you read it.

Save the audit to this exact file:

- `communications/REPORT_Codex_Close_Read_Public_Host_Topology_And_Admitted_Family_Umbrella_Publication_Scope_Audit_2026-04-13.md`
