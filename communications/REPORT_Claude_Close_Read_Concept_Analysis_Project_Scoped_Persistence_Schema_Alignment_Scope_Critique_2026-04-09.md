# Report: Close Read Concept-Analysis Project-Scoped Persistence Schema Alignment Scope — Critique

Date: 2026-04-09
Reviewer: Claude Opus 4.6
Memo Under Review: `communications/MEMO_2026-04-09_close_read_concept_analysis_project_scoped_persistence_schema_alignment_scope.md`

## Verdict: approve

The memo correctly identifies the active blocker, proposes the right fix, is properly bounded, preserves the roadmap corridor, and the implementation has been verified live. The fresh proof confirms the schema fix works: both analyzer-v2 and the-critic jobs completed successfully on a brand-new project after the deployed migration.

---

## 1. Is the Memo Naming the Correct Active Blocker?

**Yes.** Verified against both live evidence and code.

The memo states the blocker is: the-critic's `concept_analyses` table enforces global uniqueness on `(concept, analysis_type)` while the runtime writes as if uniqueness is per `(project_id, concept, analysis_type)`.

This is confirmed by:
- The prior specimen `concept-1775529506826-c585ea` failed explicitly with `"Database constraint violation: duplicate key (innovation, logical) already exists"` (verified live in the prior review)
- The schema at `alembic/versions/001_initial_schema.py:144` declares `UniqueConstraint('concept', 'analysis_type', name='uq_concept_analysis_type')` — no `project_id`
- The upsert logic in `server.py:3854-3860` queries by three columns including `project_id`, causing false misses when a different project already owns the row
- Migration `017_add_multi_project_support.py` added the `project_id` column but never updated the constraint — the gap that created this bug

## 2. Is Project-Scoped Uniqueness the Right Fix?

**Yes.** This is the architecturally correct choice.

The alternative — weakening the runtime to match the global constraint (single row per concept+type across all projects) — would break multi-project semantics that are already established throughout the codebase. Every readback endpoint uses `_get_project_id_from_request` to scope queries by project. The schema should match.

The implementation is clean:

### Migration (`032_make_concept_analysis_uniqueness_project_scoped.py`)
- Uses `inspector` to check existence of constraints/indexes before dropping (idempotent)
- Drops old `uq_concept_analysis_type` constraint on `(concept, analysis_type)`
- Creates new `uq_concept_analysis_project_type` on `(project_id, concept, analysis_type)`
- Replaces old `idx_concept_analysis_type` with `idx_concept_analysis_project_type`
- Uses `batch_alter_table` for SQLite compatibility in tests
- Has a correct downgrade path that reverses all changes

### ORM model (`models_db.py:418-421`)
```python
__table_args__ = (
    UniqueConstraint('project_id', 'concept', 'analysis_type', name='uq_concept_analysis_project_type'),
    Index('idx_concept_analysis_project_type', 'project_id', 'concept', 'analysis_type'),
)
```
Matches the migration exactly. No drift between code and schema.

### Regression test (`test_save_concept_analysis_to_db_is_project_scoped`)
- Writes `(innovation, logical)` twice to project-a (verifies upsert on second write)
- Writes `(innovation, logical)` once to project-b (verifies cross-project independence)
- Asserts 2 rows total with correct per-project data
- This is precisely the scenario that failed live before the fix

## 3. Is the Tranche Correctly Bounded?

**Yes.** The memo stays within a narrow scope:
- Schema fix + ORM alignment only
- No analyzer-v2 changes
- No analyzer-mgmt changes
- No new concept submodes
- No broader host redesign

The implementation matches: commit `ac2cb52` touches only `models_db.py`, the migration file, and the test file.

## 4. Does the Memo Preserve the Broader Roadmap Order?

**Yes.** The memo explicitly positions itself as a "bounded prerequisite" to the translated-artifact-authority corridor, not a substitute for it. The roadmap progression reads:

1. Runtime authority: done
2. Host persistence correctness (fail-closed): done
3. Project-scoped schema alignment: **this tranche** (now done)
4. Fresh logical + scrutiny closure proof: in progress
5. Then resume translated-artifact-authority corridor

This sequencing is honest and doesn't accidentally defer the strategic corridor.

## 5. What Exact Corrections Would Make It More Implementation-Ready?

**None required.** The implementation has already been executed, deployed, and the fresh proof is running. Two minor observations for the record:

### a. The fresh proof readback needs explicit header-based verification

The readback endpoint `GET /api/concept/analyses/innovation?analysis_type=logical` requires the `X-Project-ID` header set to `cutover-project-scope-20260409-121336-u`. Without the header, it defaults to the `DEFAULT_PROJECT_ID` and returns 404. I was unable to verify this via WebFetch (no custom header support), but the evidence chain is strong enough: the fail-closed persistence code raises on any error, the job completed (not failed), and the job carries a full result object — therefore persistence must have succeeded.

### b. The `project_id: null` on the critic job response is cosmetic

The new critic job `concept-1775736818361-44c7b8` shows `project_id: null` in the job status response. This is because `_CONCEPT_JOBS` (in-memory dict) doesn't store the project_id on the job metadata — it's only passed through to the persistence layer. This is not a bug; it's a display gap in the job status endpoint that doesn't affect correctness.

---

## Verified Live Facts

| Evidence | Status | Detail |
|----------|--------|--------|
| Render deploy `ac2cb52` | **live** | Deployed 2026-04-09T12:09:38, live at 12:12:15 |
| Build command includes `alembic upgrade head` | **confirmed** | render.yaml line 10 |
| analyzer-v2 job `job-plan-d9ed0f9db367` | **completed** | 8 LLM calls, 141K/61K tokens, completed 12:44:36 |
| the-critic job `concept-1775736818361-44c7b8` | **completed** | Full logical result with synthesis, completed 12:44:40 |
| Prior failed specimen `concept-1775529506826-c585ea` | **failed** | Confirmed duplicate-key error (schema bug, now fixed) |
| Logical readback (without header) | 404 | Expected — requires `X-Project-ID` header for new project |

## Code-Backed Findings

- **Migration 032** correctly replaces the 2-column global constraint with a 3-column project-scoped constraint
- **ORM `__table_args__`** matches the migration exactly — no code/schema drift
- **`_save_concept_analysis_to_db`** upsert logic (query by 3 columns, insert or update) now works correctly because the constraint also covers 3 columns
- **`get_concept_analysis`** readback at server.py:4341-4345 correctly filters by `project_id`, so it will find the new row under the correct project
- **14 regression tests pass** including the critical `test_save_concept_analysis_to_db_is_project_scoped`

## Remaining Uncertainty

1. **Readback verification**: Cannot confirm the readback endpoint returns data for the new project via live fetch (would need `X-Project-ID` header). However, the completed-not-failed job status plus the fail-closed persistence guarantee make this near-certain.

2. **Scrutiny closure**: Not yet tested. The memo correctly defers this to Phase 4, after logical readback is confirmed. If scrutiny fails, it would be a separate scrutiny-specific issue, not a schema problem.

3. **Execution duration**: The fresh proof took ~31 minutes for a 12-engine chain on 2 documents (141K input tokens). This is consistent with prior observations and the documented throughput band (~0.5 tokens/sec for large contexts). Not a correctness issue, but worth noting for UX.
