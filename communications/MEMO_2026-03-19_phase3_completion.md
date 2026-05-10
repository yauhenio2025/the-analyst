# Memo: Phase 3 / Deliverable C Completion

## Purpose

Record the outcome of **Phase 3 / Deliverable C: First Artifact Reuse Proof** in the Thin Consumer Platformization program.

This memo is the closeout for the tranche scoped in:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-19_phase3_artifact_reuse_scope.md`

It should answer:

1. what work actually landed
2. what this tranche did and did not prove
3. what verification is complete
4. what the next program step should be

## Scope Closed In This Tranche

This tranche was intended to prove one bounded thing:

- **cross-job reuse of the stored `genealogy.relationship_classification` artifact on the existing `corpus_ref` seam**

More specifically, the tranche was meant to:

- add a write-side guard that preserves source-job provenance when a fresh artifact already exists
- add read-side reuse detection in the artifact summary layer
- expose `reuse_state` and `reused_from_job_id` on the result-contract `ArtifactSlotSummary`
- prove reuse hit, reuse miss, and provenance durability in a two-job single-slot fixture

This tranche was **not** intended to prove:

- executor-time phase-1.5 skipping
- multi-artifact or multi-workflow reuse
- AOI artifact reuse
- presentation-wide or page-wide reuse
- any host-side UI or `the-critic` changes
- a broader artifact-identity or artifact-economy framework

## Completed Work

### Write-side guard in `store_relationship_classification_artifact`

`src/analysis_products/store.py:698-708`

Before calling `upsert_analysis_artifact`, the function now:

1. Calls `ensure_job_corpus(job_id)` to get the `corpus_ref`
2. Loads the existing artifact row for `corpus_ref + genealogy.relationship_classification + work_key`
3. If the row exists with `state == "ready"` and `producer_fingerprint == GENEALOGY_RELATIONSHIP_FINGERPRINT`, returns it unchanged

This guard prevents Job 2's materialization path from overwriting Job 1's artifact row. The reuse signal is therefore durable — it survives Job 2's full presenter pipeline, not just a controlled test fixture.

### Read-side reuse detection in `_summarize_artifacts_for_job`

`src/analysis_products/store.py:834-845`

During artifact summarization, for each genealogy relationship slot:

- If the stored row is ready, fingerprint-current, and was produced by a different job (`row.job_id != current_job_id`):
  - `reuse_state = "reused"`
  - `reused_from_job_id = row["job_id"]`
- Otherwise: both fields are `None`

This detection uses the already-loaded `stored_artifacts` rows. No additional per-slot queries were added.

### Additive schema fields

`src/analysis_products/schemas.py:17-18`

```python
class ArtifactSlotSummary(BaseModel):
    slot: str
    state: str
    artifact_ref: Optional[str] = None
    source_output_id: Optional[str] = None
    reuse_state: Optional[str] = None
    reused_from_job_id: Optional[str] = None
```

Both fields are optional and default to `None`. This is a backward-compatible additive change. No family-level rollup was added.

### What was NOT touched

- `src/analysis_products/run_contract.py` — unchanged
- `src/analysis_products/result_contract.py` — unchanged (already wires `artifact_families` from `summarize_job_artifacts`)
- `src/presenter/presentation_api.py` — unchanged
- `src/executor/workflow_runner.py` — unchanged
- No `the-critic` changes
- No new database tables
- No reuse-event logging or row-copy behavior

## Scope-Discipline Note

The working tree still contains unrelated local edits outside the Phase 3 seam, including files under
`src/presenter/` and `src/executor/`.

This memo's "what was not touched" claim is narrower:

- no code changes for this tranche were required in `presentation_api.py`, `workflow_runner.py`, `run_contract.py`, or `the-critic`

That should not be confused with a claim that the surrounding worktree was globally clean.

## Verification

### Phase 3 proof tests

Three new tests in `tests/test_analysis_product_contract.py:268`:

1. **Reuse hit** (`test_result_manifest_slot_exposes_reuse_hit_for_same_corpus`)
   - Two jobs with identical plan_data and document_ids share the same `corpus_ref`
   - Single-slot genealogy fixture (one prior work)
   - Artifact stored for Job 1 only
   - Job 2's manifest exposes `reuse_state == "reused"` and `reused_from_job_id == job1`

2. **Reuse miss from stale fingerprint** (`test_result_manifest_slot_omits_reuse_when_fingerprint_is_stale`)
   - Same two-job setup
   - Artifact row mutated to have a non-current `producer_fingerprint`
   - Job 2's manifest shows `state == "stale"`, `reuse_state is None`, `reused_from_job_id is None`

3. **Provenance durability** (`test_store_relationship_classification_preserves_source_provenance_on_reuse`)
   - Same two-job setup
   - Artifact stored for Job 1
   - `store_relationship_classification_artifact` called for Job 2 — returns Job 1's row unchanged
   - Direct DB row check confirms `job_id == job1` and `source_output_id == "phase-output-1"`
   - Job 2's manifest still shows `reuse_state == "reused"` and `reused_from_job_id == job1`

### Regression suite

- `tests/test_analysis_product_contract.py`: 20 tests passed (17 prior + 3 new)
- `tests/test_run_contract.py`: 3 tests passed (unchanged)
- `tests/test_presentation_api.py` (relationship artifact regression): 2 tests passed

Total: 25 tests passed, 0 failures.

## What This Tranche Actually Proved

Phase 3 now proves:

1. **The `corpus_ref` seam is a real reusable identity.** Two jobs with the same analytical situation share the same `corpus_ref` and therefore resolve to the same artifact row.
2. **Reuse is visible in the result contract.** Job 2's manifest explicitly says `reuse_state = "reused"` and names the source job.
3. **Provenance is preserved.** The write-side guard prevents Job 2 from overwriting Job 1's artifact row. The authoritative row stays with its original producer.
4. **The freshness rule works.** Stale-fingerprint artifacts are correctly excluded from reuse.

## What This Tranche Still Does Not Prove

Phase 3 does **not** yet prove:

1. Executor-time skipping of the phase-1.5 relationship computation. Job 2 may still generate prose; the proof is only that the stored artifact is not overwritten and the contract surfaces reuse.
2. Multi-artifact or multi-slot reuse rollups. The proof uses a single slot per fixture.
3. AOI artifact reuse.
4. Cross-workflow generic workspace proof (Deliverable D).
5. That the broader platform vision is complete.

## Acceptance Criteria Disposition

| Criterion | Status |
|---|---|
| Explicit reusable identity beyond job ownership (`corpus_ref + family + slot`) | PASS |
| One explicit freshness rule (`state == ready`, `producer_fingerprint` current) | PASS |
| Job 2 resolves Job 1's artifact through one lookup path | PASS |
| Single-slot fixture with slot-level reuse visibility | PASS |
| Manifest-level reuse signal on Job 2 | PASS |
| Reuse hits do not destroy source-job provenance | PASS |
| Reuse hit test | PASS |
| Reuse miss test | PASS |
| No silent broadening into multi-artifact or multi-workflow work | PASS |

## Recommended Next Move

The next program step should remain the one named in the execution brief and roadmap:

- **Phase 4 / Deliverable D: cross-workflow `AnalysisWorkspacePage` proof in `the-critic`**

Specifically:

- make `AnalysisWorkspacePage` capable of carrying both `intellectual_genealogy` and `anxiety_of_influence_thematic_single_thinker` through the same generic consumption model
- use the shared bounded-v2 consumer contract from Phase 2

Why this is next:

1. The execution brief requires both the artifact proof (now done) and the cross-workflow workspace proof before the program can be declared complete.
2. The proving vehicle for the workspace proof lives in `the-critic`, not `analyzer-v2`.
3. The artifact proof gives the substrate more substance — the generic workspace now rides on top of a reusable analysis-product layer, not just ephemeral job outputs.

## Final Status Sentence

If the team needs one operational sentence for the state after this tranche, it should be:

- **The first artifact reuse proof is now real in `analyzer-v2`; the next remaining proof is the cross-workflow `AnalysisWorkspacePage` proof in `the-critic`.**
