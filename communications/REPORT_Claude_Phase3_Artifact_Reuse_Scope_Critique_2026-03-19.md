# Phase 3 Scope Review: First Artifact Reuse Proof

**Reviewer**: Claude Opus 4.6 (automated code-level review)
**Date**: 2026-03-19
**Memo under review**: `communications/MEMO_2026-03-19_phase3_artifact_reuse_scope.md`

---

## Findings (ordered by severity)

### 1. CRITICAL — The artifact-reuse seam is real but the memo underestimates a hidden coupling

The memo correctly identifies `store.py` as the primary proof surface. But it under-describes a structural coupling that will control the difficulty of the proof:

**Genealogy relationship artifacts are materialized inside `presenter/presentation_api.py`, not during executor workflow execution.**

Specifically, `store_relationship_classification_artifact()` is called from `presentation_api.py:1988-1996` — inside `_load_per_item_data()` — and only when `read_only=False` and the relationship engine key is in the output set. This means:

- The artifact does not exist after Job 1's executor phase completes
- The artifact exists only after Job 1's presentation pipeline has run (specifically `prepare_presentation` or `assemble_page` with `read_only=False`)
- Job 2's reuse lookup would therefore depend on Job 1 having completed the **full presenter materialization cycle**, not just executor completion

This coupling is real and consequential. The freshness rule and lookup path must account for it, or the proof will silently depend on presentation-pipeline timing rather than on a clean executor-to-artifact contract.

**Recommendation**: The scope memo should explicitly name this dependency. The freshness rule must include a check that Job 1's artifact row exists in `analysis_artifacts` (state=ready), not merely that Job 1's executor status is "completed." The `materialize_stage1_artifacts` function (`presentation_api.py:2020`) exists and could be called eagerly in the executor post-completion hook, which would decouple materialization from the read-only presentation path. If the tranche decides to keep the current presenter-derived materialization, that decision must be stated explicitly.

**Severity**: Critical because it determines whether the "one lookup path" is actually deterministic or is a race condition against presentation timing.

### 2. HIGH — The reuse lookup has no existing seam; it must be built from scratch

The memo states "one lookup path that resolves reuse candidates." But the code today has **zero** cross-job artifact resolution. Every artifact access function is either:

- `load_job_artifact(job_id, ...)` — job-scoped
- `load_analysis_artifact(corpus_ref=..., ...)` — corpus-scoped but never called from outside `store.py`
- `list_job_artifacts(job_id, ...)` — job-scoped

No function currently takes a corpus_ref (or any other cross-job identifier) from outside `store.py` and returns artifacts from a **different** job. The closest thing is `load_analysis_artifact`, which queries by `corpus_ref + artifact_family + artifact_slot`. But today:

- It's a private helper called only from `load_job_artifact` and `upsert_analysis_artifact`
- Nothing exposes "give me the artifact for this corpus regardless of which job produced it"
- No code path does "Job 2 wants to check if a prior artifact exists for the same analytical situation"

This means the "one lookup path" is entirely new code, not an extraction or refinement of an existing seam. The memo should acknowledge this more clearly. It is not a large amount of code, but the memo's tone suggests the seam is partially in place — it is not.

**Recommendation**: Be explicit that the lookup path is new construction. The natural shape is: given Job 2's `corpus_ref`, query `analysis_artifacts` for `corpus_ref + artifact_family + state=ready` and return the match if the freshness rule passes. The database schema already supports this (the `idx_analysis_artifacts_family_slot` unique index is on `(corpus_ref, artifact_family, artifact_slot)`), so the storage seam is real even if the query path is not.

### 3. HIGH — The `corpus_ref` identity is the right anchor, but the memo doesn't name it explicitly enough

The memo talks about "one stable reusable identity" and "the identity should be sufficient to answer: what exact bounded analytical situation does this artifact represent?" The answer is already in the code: **`corpus_ref`**.

`corpus_ref` is a deterministic SHA-256-based hash of:
- workflow_key
- objective_key
- qualifiers (including `selected_source_thinker_id` for AOI)
- content-hashed member fingerprints (document content hashes, not upload-time doc IDs)

This is explicitly designed to be upload-order-independent and re-run-stable (`test_corpus_registration_ignores_upload_time_doc_ids_and_input_order` proves this). Two jobs with the same documents and the same analytical situation will produce the same `corpus_ref`.

The memo's "Layer 1: Stable identity" section describes this without naming it. The tranche should explicitly state: **`corpus_ref` is the reusable identity for this proof.** Not inventing a new identity system.

**Recommendation**: Name `corpus_ref` as the anchor. This removes ambiguity about whether a new identity scheme is needed (it is not).

### 4. MEDIUM — The `producer_fingerprint` already exists and is the natural freshness check

The memo's "Layer 2: Freshness rule" says "define one freshness rule only." The code already has a partial freshness mechanism:

- `GENEALOGY_RELATIONSHIP_FINGERPRINT = "genealogy.relationship_classification:v1"` (`store.py:37`)
- `_current_fingerprint()` returns the current expected fingerprint for each artifact family (`store.py:725-730`)
- `_summarize_artifacts_for_job()` already checks `row.get("producer_fingerprint") != current_fingerprint` and marks the artifact as `stale` if they differ (`store.py:806`)

The natural freshness rule for the first proof is: **an artifact is fresh if `producer_fingerprint == GENEALOGY_RELATIONSHIP_FINGERPRINT` and `state == "ready"`**. This is already partially implemented for staleness reporting. The tranche just needs to use it in the reuse lookup.

**Recommendation**: The freshness rule should piggyback on the existing `producer_fingerprint` mechanism rather than inventing a new one. This keeps the tranche minimal and leverages existing infrastructure.

### 5. MEDIUM — The result-contract reuse signal has no natural home yet

The memo requires `reuse_state` and `reused_from_job_id` to be visible in the result manifest for the genealogy relationship artifact family. Today, `ArtifactFamilySummary` has:

```python
class ArtifactFamilySummary(BaseModel):
    artifact_family: str
    state: str
    format: str
    total_slots: int
    ready_slots: int
    ...
    slots: list[ArtifactSlotSummary]
```

And `ArtifactSlotSummary`:

```python
class ArtifactSlotSummary(BaseModel):
    slot: str
    state: str
    artifact_ref: Optional[str]
    source_output_id: Optional[str]
```

Neither schema has `reuse_state` or `reused_from_job_id`. Adding these fields is straightforward but is a real schema change to the result contract. The memo correctly identifies this (`src/analysis_products/schemas.py`) but doesn't flag that it's a contract-level schema addition visible to all consumers, not an internal-only change.

**Recommendation**: Acceptable scope. Add `reuse_state` and `reused_from_job_id` to `ArtifactFamilySummary` (or to `ArtifactSlotSummary` if per-slot reuse granularity is desired). Default both to `None`/`""` so existing consumers aren't broken. This is a backward-compatible additive change.

### 6. LOW — The `analysis_artifacts.job_id` column creates a subtle ambiguity for reused artifacts

When Job 2 reuses Job 1's artifact, what happens to `analysis_artifacts.job_id`? Today, `upsert_analysis_artifact` writes the producing job's ID. If reuse means "don't re-create the artifact row," then the row's `job_id` stays as Job 1's. But `list_job_artifacts(job_id=job2)` goes through `corpus_ref` — so if both jobs share the same corpus, they'll find the same artifact row.

This actually works correctly by accident: the unique index `(corpus_ref, artifact_family, artifact_slot)` means one corpus gets one artifact row. If Job 2 has the same `corpus_ref`, it sees Job 1's artifact. The `job_id` column on the artifact row is the producer's job_id, which is the reuse source.

**Recommendation**: This is not a bug but should be documented. The `job_id` on the artifact row is the **producer** job, and this becomes the `reused_from_job_id` signal. This is cleaner than storing a separate reuse pointer.

### 7. LOW — Test coverage is strong for the existing machinery, not for the reuse path

The existing tests (`test_analysis_product_contract.py`, `test_run_contract.py`) verify:
- Deterministic corpus registration (both AOI and genealogy)
- Round-trip artifact storage
- Manifest freshness and staleness
- Result discovery with thinker filtering
- Run detail with progress aliases

None of them test cross-job artifact resolution. This is expected — the feature doesn't exist yet. But the test infrastructure is well-set-up for the two-job proof fixture the memo describes: `create_job`, `register_job_corpus`, `store_relationship_classification_artifact` are all exercised in existing tests.

**Recommendation**: No action needed; the existing test infrastructure is adequate for extending into reuse tests.

---

## Strongest arguments against this scope

1. **The presenter-derived materialization coupling** makes the "two-job proof" less clean than the memo implies. The proof must either decouple materialization from the presenter or explicitly depend on the presenter pipeline completing for Job 1 before Job 2 can reuse. Either path adds work the memo doesn't account for.

2. **The lookup path is 100% new code**, not a refinement. The memo reads as though an existing seam is being extended; in reality, the cross-job resolution function does not exist. This isn't fatal but the implementation estimate should account for it.

3. **The "exactly one freshness rule" constraint is already naturally satisfied** by the existing `producer_fingerprint` mechanism, which reduces the design freedom but also reduces the risk of over-engineering. The tranche should acknowledge that the freshness rule is "match the current `producer_fingerprint` and `state == ready`" and move on.

---

## Hidden coupling assessment

### Corpus identity → Artifact storage

**Coupling is clean.** `corpus_ref` is computed deterministically from plan_data + document content hashes. The artifact table is keyed by `(corpus_ref, artifact_family, artifact_slot)`. Two jobs with the same analytical situation get the same corpus_ref and therefore resolve to the same artifact row. This is well-designed for reuse.

### Artifact storage → Presenter materialization

**Coupling is real and consequential.** Genealogy relationship artifacts are produced inside `presentation_api.py:_load_per_item_data()` during presenter assembly, not during executor workflow completion. `materialize_stage1_artifacts()` exists as an eager path but is called from the `preparation_coordinator`, which runs after the job completes. The reuse proof must account for this: Job 2 cannot resolve Job 1's artifact if Job 1's presentation has not been prepared.

### Presenter materialization → Result-contract exposure

**Coupling is minimal.** `summarize_job_artifacts()` reads from `analysis_artifacts` and computes family summaries. Adding reuse fields to the summary is additive. The result manifest (`build_result_manifest` in `result_contract.py`) already includes `artifact_families`. No deep restructuring is needed.

---

## Should the bounded proof be narrower?

No. The memo is already narrow — one artifact class, two jobs, one freshness rule, one lookup path. Narrowing further would risk producing a proof that doesn't actually demonstrate cross-job resolution (e.g., narrowing to "just add the schema fields" without a working lookup would be scope theater).

The only refinement I'd suggest is: **explicitly decide whether to decouple artifact materialization from the presenter pipeline** as part of this tranche. If yes, that's ~20-30 lines of code in `workflow_runner.py` or `preparation_coordinator.py`. If no, the freshness rule must include a presenter-completion check. Either way, the decision should be scoped, not deferred.

---

## Should Deliverable C come before Deliverable D?

**Yes, unambiguously.** The roadmap memo's argument is correct:

1. Deliverable D (cross-workflow `AnalysisWorkspacePage` proof) without Deliverable C would prove only that one UI shell can read two workflow families. That's a host-side win but not a platform-substrate win.

2. Deliverable C proves that the substrate can store and resolve reusable artifacts across jobs. This is the harder and more valuable proof.

3. Deliverable C does not depend on Deliverable D. Deliverable D benefits from C (the generic workspace becomes more meaningful when it can surface reuse signals).

4. The code surfaces for Deliverable C are entirely in `analyzer-v2`. Deliverable D requires `the-critic`. Doing C first keeps the work focused in one repo.

---

## Verdict

**Proceed with scope changes.**

The memo is well-scoped and the artifact-reuse seam is real in the code — not just plausible on paper. The `corpus_ref` identity, `producer_fingerprint` freshness mechanism, and `(corpus_ref, artifact_family, artifact_slot)` unique index provide the right database-level foundation.

However, the implementation plan should explicitly address three things the current memo leaves implicit:

1. **Name `corpus_ref` as the stable reusable identity.** Don't leave it abstract.
2. **Decide on the presenter-materialization coupling** before starting implementation. Either eagerly materialize in the post-completion hook (recommended, ~30 lines) or add a presenter-completion guard to the freshness rule.
3. **Acknowledge the lookup path is new construction**, not an extraction from existing code.

With those three clarifications, the tranche is ready to become an implementation plan.
