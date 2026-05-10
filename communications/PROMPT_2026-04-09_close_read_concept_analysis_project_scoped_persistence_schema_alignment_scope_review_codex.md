Please audit this scope memo in full:

- `communications/MEMO_2026-04-09_close_read_concept_analysis_project_scoped_persistence_schema_alignment_scope.md`

Read these for context first:

- `communications/REPORT_Codex_Close_Read_Concept_Analysis_Logical_Execution_Completion_Stall_Closure_Scope_Audit_2026-04-07.md`
- `communications/REPORT_Claude_Close_Read_Concept_Analysis_Logical_Execution_Completion_Stall_Closure_Scope_Critique_2026-04-07.md`
- `communications/MEMO_2026-04-07_close_read_concept_analysis_logical_readback_and_scrutiny_closure_scope.md`
- `communications/MEMO_2026-04-06_close_read_concept_analysis_translated_artifact_authority_scope.md`
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_live_concept_authority_cutover.md`

Verify the live evidence directly:

- `https://the-critic.onrender.com/api/concept/jobs/concept-1775529506826-c585ea`
- `https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical` with header `X-Project-ID: cutover-logical-readback-closure-20260407-023428`
- `https://analyzer-v2.onrender.com/v1/executor/jobs/job-plan-936b5b61e93f`
- `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?consumer_key=the-critic&external_project_id=cutover-logical-readback-closure-20260407-023428&concept_name=innovation&analysis_mode=logical&analyzer_v2_job_id=job-plan-936b5b61e93f`

Inspect the relevant code:

- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/api/models_db.py`
- `/home/evgeny/projects/the-critic/api/alembic/versions/001_initial_schema.py`
- `/home/evgeny/projects/the-critic/api/alembic/versions/017_add_multi_project_support.py`
- `/home/evgeny/projects/the-critic/render.yaml`

Audit objectives:

1. Test whether the memo’s primary diagnosis is actually supported by current live evidence.
2. Check whether `(project_id, concept, analysis_type)` is the correct target uniqueness contract.
3. Examine whether the implementation sequence is the right one:
   - migration + ORM alignment
   - redeploy
   - fresh logical proof
   - fresh scrutiny proof
4. Evaluate whether anything is missing for a real implementation tranche.
5. Check whether the memo stays aligned with the larger analyzer-v2-as-brain corridor.

Questions to answer directly:

1. Is the memo correct that the active blocker is host persistence schema mismatch?
2. Is the proposed schema fix the right one?
3. Is there any narrower or safer alternative that should be preferred?
4. Is the tranche properly bounded?
5. What exact corrections would make it tighter?

Deliverable:

- Save your audit to:
  - `communications/REPORT_Codex_Close_Read_Concept_Analysis_Project_Scoped_Persistence_Schema_Alignment_Scope_Audit_2026-04-09.md`

Format:

- Start with a verdict:
  - `Verdict: approve`
  - or `Verdict: approve with corrections`
  - or `Verdict: reject`
- Findings first, ordered by severity.
- Distinguish:
  - live-verified facts
  - code-backed findings
  - remaining uncertainty
