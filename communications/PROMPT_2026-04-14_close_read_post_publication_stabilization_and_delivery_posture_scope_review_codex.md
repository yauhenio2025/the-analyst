# Prompt For Codex: Audit Close Read Post-Publication Stabilization And Delivery Posture Scope

Audit this scope memo:

- `communications/MEMO_2026-04-14_close_read_post_publication_stabilization_and_delivery_posture_scope.md`

Use the recent Close Read memo chain as context, especially:

- `communications/MEMO_2026-04-13_close_read_public_host_topology_and_admitted_family_umbrella_publication_completion.md`
- `communications/MEMO_2026-04-13_close_read_roadmap_update_after_public_host_topology_and_admitted_family_umbrella_publication_completion.md`
- `communications/NOTE_2026-04-13_close_read_public_host_topology_evidence.md`
- `communications/NOTE_2026-04-13_close_read_public_route_matrix_and_browser_diagnosis.md`
- `communications/MEMO_2026-04-11_close_read_admitted_concept_operator_surface_and_thin_host_simplification_scope.md`
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- plus any other relevant recent memos in `communications/` or nearby docs folders from roughly the last 7-10 days

Audit goals:

1. test the robustness of the assumptions behind the memo
2. judge the memo against the broader roadmap and product objectives
3. scrutinize its claims against the actual codebase
4. check whether the memo is using the right source of truth:
  - live public state
  - deployed `origin/master`
  - local dirty trees

Specific checks:

- Is “bounded Critic-host stabilization first” the right next default, or is there stronger evidence that standalone extraction should now be the next corridor?
- Is the memo right to keep family expansion out of scope?
- Is the known genealogy console-noise residual actually the leading public defect?
- Is the proposed repo-owned browser-proof harness appropriately bounded and useful?
- Does the codebase support the memo’s claim that the remaining work is post-publication stabilization/posture rather than publication?
- Is the memo missing any important residual on the public Close Read surface, deployment/config truth, or repo divergence?
- Does it keep analyzer-v2 and analyzer-mgmt out of scope honestly?

Important audit rules:

- Do not assume local dirty trees equal deployed truth.
- Compare local code, deployed `origin/master`, and live public behavior when the distinction matters.
- Treat hydrated browser proof as stronger than static HTML or route-level `200`.
- Call out stale docs or stale assumptions explicitly.

Deliverable:

- write one audit report to:
  - `communications/REPORT_Codex_Close_Read_Post_Publication_Stabilization_And_Delivery_Posture_Scope_Audit_2026-04-14.md`

The report should include:

- verdict: approve / approve with corrections / reject
- key findings
- concrete corrections, if any
- brief note on whether the memo is ready to execute
