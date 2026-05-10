Verdict: reject

## Findings

1. Critical: the memo's primary diagnosis is not supported by the current live specimen.
   On 2026-04-09, `GET https://the-critic.onrender.com/api/concept/jobs/concept-1775529506826-c585ea` returns `status: "failed"`, not `running`. The failure is explicit and host-side: `concept analysis persistence failed ... duplicate key value violates unique constraint "uq_concept_analysis_type"`. On the same date, `GET https://analyzer-v2.onrender.com/v1/executor/jobs/job-plan-936b5b61e93f` returns `status: "completed"`, with `completed_at: "2026-04-07T03:05:54.273464"`. The memo says the live logical run is blocked upstream in analyzer-v2 completion; the live evidence now says the opposite.

2. Critical: the stronger diagnosis is a host persistence/schema bug, not an analyzer-v2 completion stall.
   Two independent analyzer-v2 logical runs completed and produced exact translated artifacts with `contract_validation_status: "passed"`:
   `job-plan-03f3e58a8ac6` for project `cutover-artifact-authority-20260406-162636`
   `job-plan-936b5b61e93f` for project `cutover-logical-readback-closure-20260407-023428`
   Both are readable through `GET /v1/orchestrator/concept-analysis-by-ref/result?...&analyzer_v2_job_id=...`. The host read model is still empty for both later projects, and the current specimen now shows the concrete reason: the host persistence write fails after upstream completion.

3. Critical: the live failure is systemic, not specimen-specific.
   `/home/evgeny/projects/the-critic/api/server.py` reads and writes concept analyses by `(project_id, concept, analysis_type)`, but the live database still enforces the older global uniqueness constraint on `(concept, analysis_type)` named `uq_concept_analysis_type`. That mismatch means any fresh project that reuses the same concept and analysis type can fail on insert after upstream success. This is a multi-project schema bug, not a one-off execution stall.

4. Major: the memo overfits to a transient mid-flight observation.
   The likely sequence was:
   analyzer-v2 was still `running` when first observed
   analyzer-v2 completed at `2026-04-07T03:05:54.273464`
   the translated artifact was produced at `2026-04-07T03:05:52.104728`
   the-critic failed persistence and marked the local job `failed` at `2026-04-07T03:05:58.471482`
   That is a post-completion host failure, not an upstream non-completion seam. The memo froze the diagnosis before the specimen reached terminal state.

5. Major: there is no current evidence that host polling semantics are masking a completed upstream state.
   `/home/evgeny/projects/the-critic/api/server.py` polls analyzer-v2 until executor `status == "completed"`, then fetches phase outputs, translates, persists, and marks the host job completed only after persistence succeeds. If persistence raises, the local job is marked `failed`. That means the earlier silent-success bug is materially closed; the remaining host bug is the persistence/schema boundary.

6. Moderate: analyzer-v2 latency may still deserve scrutiny, but it is secondary to the blocking bug.
   The two logical runs took roughly 23-27 minutes on tiny corpora. That is longer than ideal, but it is not a completion-stall proof. If latency is unacceptable, it should be scoped as a performance tranche after the host persistence path is repaired.

## Live-Verified Facts

- `GET https://the-critic.onrender.com/api/concept/jobs/concept-1775529506826-c585ea` on 2026-04-09 returns:
  `status: "failed"`
  `error: duplicate key value violates unique constraint "uq_concept_analysis_type"`
  `progress.current_phase_display: "Translated Host Artifact"`
  `progress.completed_phases: ["1.0: Logical Concept Analysis"]`

- `GET https://analyzer-v2.onrender.com/v1/executor/jobs/job-plan-936b5b61e93f` returns:
  `status: "completed"`
  `workflow_key: "concept_logical_single_concept"`
  `completed_at: "2026-04-07T03:05:54.273464"`

- `GET https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?consumer_key=the-critic&external_project_id=cutover-logical-readback-closure-20260407-023428&concept_name=innovation&analysis_mode=logical&analyzer_v2_job_id=job-plan-936b5b61e93f` returns:
  `lookup_mode: "exact_run"`
  `contract_validation_status: "passed"`
  a translated logical artifact with `_analysis_provenance.execution_owner = "analyzer-v2"`

- `GET https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical` with header `X-Project-ID: cutover-logical-readback-closure-20260407-023428` returns `404`.

- `GET https://the-critic.onrender.com/api/projects/cutover-logical-readback-closure-20260407-023428/documents` returns four uploaded documents. The corpus is duplicated, but analyzer-v2 still completed and produced a valid artifact, so duplication is not the first failing seam.

- The earlier artifact-authority specimen shows the same pattern:
  `GET https://analyzer-v2.onrender.com/v1/executor/jobs/job-plan-03f3e58a8ac6` returns `status: "completed"`.
  `GET https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?...analyzer_v2_job_id=job-plan-03f3e58a8ac6` returns `contract_validation_status: "passed"`.
  `GET https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical` with `X-Project-ID: cutover-artifact-authority-20260406-162636` returns `404`.

- The older project `cutover-live-tiny-20260406` still returns a persisted logical result for the same concept `innovation`, which is exactly the pattern the global uniqueness bug would produce: first project succeeds, later fresh projects for the same `(concept, analysis_type)` fail to persist.

## Code-Backed Findings

- `/home/evgeny/projects/the-critic/api/server.py`
  `_run_rebased_concept_analysis(...)` polls analyzer-v2 until `state == "completed"`, then fetches phase outputs and translates them locally.
  `run_concept_analysis_thread(...)` calls `_save_concept_analysis_to_disk(...)`, then `_save_concept_analysis_to_db(...)`, and only then marks the host job `completed`.
  If persistence raises, the exception path marks the job `failed`.
  This code matches the current live job behavior and contradicts the memo's upstream-stall diagnosis.

- `/home/evgeny/projects/the-critic/api/server.py`
  `_save_concept_analysis_to_db(...)` looks up an existing row by `(concept, analysis_type, project_id)` and inserts if none exists for that project.
  That logic is correct for multi-project semantics only if the database uniqueness rule also includes `project_id`.

- `/home/evgeny/projects/the-critic/api/models_db.py`
  `ConceptAnalysis` currently declares `project_id`, `concept`, `analysis_type`, and an index on `(concept, analysis_type)`, but no ORM-level unique constraint.
  The local model does not expose the live database's older uniqueness rule, which increases the risk of reasoning from code alone and missing the real deployed constraint.

- `/home/evgeny/projects/the-critic/api/alembic/versions/001_initial_schema.py`
  creates `uq_concept_analysis_type` as `UniqueConstraint('concept', 'analysis_type', ...)`.

- `/home/evgeny/projects/the-critic/api/alembic/versions/017_add_multi_project_support.py`
  adds `project_id` to `concept_analyses` but does not drop or replace `uq_concept_analysis_type`.
  That is the missing migration step that explains the live duplicate-key failure.

- `/home/evgeny/projects/analyzer-v2/src/executor/workflow_runner.py`
  sets executor job status to `completed` once the sole workflow phase returns successfully.
  There is no obvious local completion-state bug in this path, and the live executor job status confirms completion.

- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/concept_logical_single_concept.json`
  defines a single-phase workflow using `concept_analysis_12_phase` with linked transformation `concept_logical_host_contract_extraction`.
  This matches the live artifact provenance and supports the conclusion that the logical workflow reached its intended translated-artifact boundary.

- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
  includes `concept_synthesis` as the final engine, but the live failures occur after analyzer-v2 completion, not inside this chain.

## Remaining Uncertainty

- The deployed code revision on Render may not be byte-identical to the local checkout, but the live responses and migration files are sufficient to establish the current blocker.

- There may still be a secondary latency/performance issue in analyzer-v2 logical execution on tiny corpora. Current evidence supports "slow but completes," not "stalls and never completes."

- Scrutiny could still have a downstream issue after logical persistence is fixed, but current evidence does not justify leading with scrutiny or analyzer-v2 execution before restoring successful logical persistence.

## Direct Answers

1. Is the memo right to supersede the readback-first scope?
   No. The memo moves away from the host-side seam too early. The earlier scope should be narrowed and corrected, not superseded by an analyzer-v2-first stall theory.

2. Is the current live evidence enough to justify an analyzer-v2-first stall-closure tranche?
   No. The current live evidence justifies a host persistence/schema tranche first.

3. Is anything critical missing from the scope for a real implementation pass?
   Yes. The scope misses the live database constraint mismatch and the need for a migration that aligns uniqueness with multi-project semantics, plus any required backfill/repair for rows blocked by the old constraint.

4. Is there any sign the memo is overfitting to one live specimen instead of the true systemic cause?
   Yes. It appears to freeze the diagnosis while the specimen was still in flight and before terminal state exposed the actual persistence failure. The code and schema evidence indicate a systemic multi-project bug.

5. What precise corrections would make it tighter?
   Replace the primary diagnosis with: "Analyzer-v2 logical execution completes and produces a valid translated artifact; the first failing seam is the-critic concept-analysis persistence on a live global uniqueness constraint that still ignores project_id."
   Replace the implementation order with:
   1. verify and fix the `concept_analyses` uniqueness/migration mismatch so writes are unique per `(project_id, concept, analysis_type)`
   2. rerun a fresh logical proof on a fresh project using the same concept to confirm persistence/readback now closes
   3. only if analyzer-v2 then fails to reach `completed`, open a separate executor/performance investigation
   4. only after logical persistence closes, re-run scrutiny and scope any scrutiny-specific residue
   Add an explicit note that duplicate documents in the April 7 project are adjacent evidence, not the root blocker.
   Add an explicit note that the host persistence correctness fix is only partially complete: silent success is fixed, but persistence schema alignment is not.

## Tightened Bottom Line

The memo should not frame the immediate blocker as "analyzer-v2 logical completion stall." The stronger live-supported diagnosis is:

`analyzer-v2 completes logical execution and exact translated artifact production, but the-critic still fails to persist project-scoped concept analyses because the live database uniqueness constraint remains global on (concept, analysis_type).`

That is the tranche that should be closed first.
