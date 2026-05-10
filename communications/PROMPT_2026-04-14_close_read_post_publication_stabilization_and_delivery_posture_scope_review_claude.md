# Prompt For Claude: Review Close Read Post-Publication Stabilization And Delivery Posture Scope

Please review this scope memo:

- `communications/MEMO_2026-04-14_close_read_post_publication_stabilization_and_delivery_posture_scope.md`

And evaluate it against the recent Close Read chain, especially:

- `communications/MEMO_2026-04-13_close_read_public_host_topology_and_admitted_family_umbrella_publication_completion.md`
- `communications/MEMO_2026-04-13_close_read_roadmap_update_after_public_host_topology_and_admitted_family_umbrella_publication_completion.md`
- `communications/NOTE_2026-04-13_close_read_public_host_topology_evidence.md`
- `communications/NOTE_2026-04-13_close_read_public_route_matrix_and_browser_diagnosis.md`
- `communications/MEMO_2026-04-11_close_read_admitted_concept_operator_surface_and_thin_host_simplification_scope.md`
- `communications/MEMO_2026-04-05_close_read_v1_product_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- any other relevant recent Close Read memos in `communications/` or nearby docs folders from roughly the last 7-10 days

Your job:

1. test the robustness of the memo’s assumptions
2. examine the memo in light of the larger roadmap and overall objectives
3. scrutinize the memo’s claims against the actual codebase and current live/public product reality
4. identify any place where the memo is too broad, too narrow, stale, or framed against the wrong source of truth

Specific questions to answer:

- Is the memo right to treat bounded Critic-host stabilization as the default next move, rather than standalone extraction or family expansion?
- Is the known genealogy `ERR_CONNECTION_REFUSED` residual the right lead residual, or is the memo missing a more important post-publication defect?
- Is adding one repo-owned browser-proof harness the right next hardening move, or does that overfit the current product state?
- Does the memo keep analyzer-v2 and analyzer-mgmt properly out of scope, or is there a real blocker in those repos that the memo is ignoring?
- Is the delivery-posture decision framed honestly enough, or does the memo smuggle in “stay on Critic” too strongly?
- Does the codebase support the memo’s claim that the public Close Read surface is already real and that the next question is stabilization/posture rather than publication?
- Are there any recent memos or docs that materially change the answer?

Important review rules:

- Do not assume the dirty local checkout is the same as deployed truth.
- Check local-vs-live divergence where relevant, especially in `the-critic`.
- If you use live checks, treat hydrated browser truth as stronger than route-level `200`.
- Distinguish clearly between:
  - current live truth
  - current local code
  - historical/stale documentary records

Deliverable:

- write one critique report to:
  - `communications/REPORT_Claude_Close_Read_Post_Publication_Stabilization_And_Delivery_Posture_Scope_Critique_2026-04-14.md`

The report should include:

- verdict: approve / approve with corrections / reject
- key findings
- exact corrections needed, if any
- brief note on whether this is ready to execute
