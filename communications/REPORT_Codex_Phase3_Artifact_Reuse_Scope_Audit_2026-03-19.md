# Report: Phase 3 Artifact Reuse Scope Audit

Date: 2026-03-19

## Findings

1. High: the memo understates how much reusable identity already exists, and the cleanest first proof should build on that instead of inventing a second identity layer.

Current analyzer-v2 code already has a deterministic cross-job key shape:

- `corpus_ref` is derived from workflow/objective/qualifiers/member fingerprints at `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:341`
- relationship artifacts are keyed by `(corpus_ref, artifact_family, artifact_slot)` at `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:494`
- the DB already enforces that exact uniqueness at `/home/evgeny/projects/analyzer-v2/src/executor/db.py:295`
- artifact freshness already has one concrete signal available in `producer_fingerprint` at `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:500` and `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:725`

So the first proof does not need a new abstract “artifact identity” system. The narrow implementable identity is:

- same `corpus_ref`
- same `artifact_family`
- same `artifact_slot`
- same current `producer_fingerprint`

If Deliverable C starts by inventing a broader reusable-identity framework beyond that, it will drift into a general artifact-economy rewrite.

2. High: the memo’s wording about “reuses it instead of recomputing it” is wider than the current seam actually supports.

Today the genealogy relationship artifact is materialized after phase execution and during presentation preparation:

- post-phase materialization trigger in `/home/evgeny/projects/analyzer-v2/src/executor/workflow_runner.py:509`
- auto-presentation materialization trigger in `/home/evgeny/projects/analyzer-v2/src/executor/workflow_runner.py:726`
- relationship artifact write inside presentation assembly helpers at `/home/evgeny/projects/analyzer-v2/src/presenter/presentation_api.py:1987`
- bounded materializer entrypoint at `/home/evgeny/projects/analyzer-v2/src/presenter/presentation_api.py:2020`

What does not exist yet is any executor-time artifact consumption path that lets Job 2 skip the phase-1.5 relationship-generation work because a prior artifact is already available. The current reuse seam is artifact lookup/storage, not engine short-circuiting.

That means the proof is implementable without reopening host work only if the scope is tightened to:

- cross-job resolution of the stored `genealogy.relationship_classification` artifact
- one freshness decision
- one manifest-visible reuse signal

If the tranche insists on proving that Job 2 avoids recomputing the underlying relationship phase output, it silently expands into broader executor/workflow-runner machinery.

3. High: the required observable needs tightening because `genealogy.relationship_classification` is a multi-slot family, not a single blob.

Current genealogy artifact summaries are slot-based:

- slot schema lives at `/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py:12`
- family schema lives at `/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py:19`
- genealogy expected slots are derived from prior works at `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:715`
- genealogy family summaries are assembled from those slots at `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:767`

The memo’s proposed observable:

- `reuse_state = "reused"`
- `reused_from_job_id = "<job-1-id>"`

is not quite sufficient if it exists only at the family level, because a family can contain multiple slots and, in principle, mixed hit/miss behavior.

For the first proof, tighten one of these two ways:

- constrain the proof fixture to exactly one prior-work slot, so a family-level reuse signal is unambiguous, or
- add reuse fields at the slot level and optionally roll them up at the family level

Without that tightening, Job 2 can claim family-level reuse while hiding partial misses.

4. Medium: the current row shape has a provenance-overwrite trap, and the first proof should not “record reuse” by rewriting the shared artifact row.

The artifact table stores one authoritative row per `(corpus_ref, artifact_family, artifact_slot)`:

- schema at `/home/evgeny/projects/analyzer-v2/src/executor/db.py:251`
- unique key at `/home/evgeny/projects/analyzer-v2/src/executor/db.py:295`
- write path deletes and reinserts the row at `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:505`

That row also contains only one `job_id` column:

- `/home/evgeny/projects/analyzer-v2/src/executor/db.py:260`

So if Job 2 “reuses” Job 1 by upserting the same artifact row again, the source provenance is destroyed and `reused_from_job_id` becomes unrecoverable.

For the first proof, the safe shape is:

- treat the prior artifact row as the authoritative source row
- resolve reuse by exact lookup
- surface `reused_from_job_id` in Job 2’s manifest from the looked-up row
- do not rewrite the row on a reuse hit

5. Medium: the boundary should stay concentrated in `store.py`, `schemas.py`, and `result_contract.py`; `run_contract.py` and `presentation_api.py` should stay mostly out.

The right ownership split for the first proof is:

- `store.py`: exact lookup helper, freshness predicate, and any reuse-summary assembly over existing artifact rows; current summary seam already lives at `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py:767`
- `schemas.py`: optional reuse fields for slot/family summaries; current contract shapes are at `/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py:12`
- `result_contract.py`: inject reuse evidence into the result manifest when building Job 2’s consumer-visible contract; current manifest assembly is at `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py:257`

What should stay out:

- general cross-family search systems
- AOI reuse machinery
- host/UI work in `the-critic`
- reuse lookup logic embedded in `presentation_api.py`
- reuse mirroring in `run_contract.py` unless a later consumer requirement makes it unavoidable

The current run contract only derives lifecycle fields from artifact summaries at `/home/evgeny/projects/analyzer-v2/src/analysis_products/run_contract.py:97`. The required observable for Deliverable C is on the result manifest, not on live-run discovery, so adding run-contract surface now would be scope drift.

## Implementability Without Reopening Host-Side Work

Yes, but only with scope changes.

This is implementable without reopening `the-critic` if the proof is defined as:

- reuse of the stored genealogy relationship artifact through one exact corpus/slot lookup
- one freshness rule based on the current producer fingerprint
- one explicit manifest-visible reuse signal on Job 2

No host-side work is required for that. The current result contract already carries artifact-family summaries at `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py:291`, and the targeted proof can be verified directly in analyzer-v2 tests or API inspection.

What is not implementable within this narrow scope is a stronger claim that Job 2 avoids recomputing the underlying relationship phase output. That would require new executor-time artifact-consumption behavior outside the memo’s intended boundary.

## Observable Call

The required observable is directionally right, but it needs tightening.

As stated, a family-level:

- `reuse_state`
- `reused_from_job_id`

is only sufficient if the proof fixture guarantees a single-slot genealogy case.

If the proof uses the normal multi-slot genealogy shape, the observable should surface at least slot-level reuse metadata. Otherwise the first proof can pass while masking partial reuse behavior.

## Scope Call

The scope should stay on `genealogy.relationship_classification` only.

It does not need broader artifact machinery if it is kept to:

- one family
- two jobs
- one exact lookup path
- one freshness rule
- one manifest-visible reuse signal

It does silently depend on broader machinery only if the team tries to prove executor-time recomputation avoidance, family-agnostic search, or multi-workflow reuse in the same tranche.

## Targeted Verification Performed

I inspected the required memo/code surfaces and ran:

- `PYTHONPATH=. pytest -q tests/test_analysis_product_contract.py tests/test_run_contract.py`
  - result: `17 passed`
- `PYTHONPATH=. pytest -q tests/test_presentation_api.py -k 'load_per_item_data_persists_relationship_artifact_with_winning_output_id or load_per_item_data_read_only_does_not_persist_relationship_artifact'`
  - result: `2 passed`

Those tests confirm the current store/result/run seams are stable enough for a narrow Deliverable C proof, and that relationship artifacts are currently persisted from presentation-side flows rather than consumed during execution.

## Verdict

Proceed with scope changes.
