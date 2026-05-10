# Verdict

Approve with scope corrections.

The memo chooses the right next Stage 15 slice. The live Phase 4 stack now has persisted analyzer-owned reports, persisted gate decisions over exact report ids, and persisted review decisions over exact gate ids. What still does not exist is any analyzer-owned object that answers the next governance question: which exact persisted review is the currently adopted stance. On that main point, the memo is right.

But the scope is not fully tight yet. Two gaps remain:

- the proposed persisted object omits `resolution_key` even though the memo also proposes a code-defined resolution definition
- the proposed “current adopted stance” law is still too implicit, because it relies on newest-first resolution history without defining one authoritative current-resolution accessor and one explicit resolution scope

# Verified Claims

- The recent program record supports bounded current-disposition resolution as the next honest Phase 4 seam.
  - `communications/MEMO_2026-03-29_phase4_bounded_review_disposition_v1_completion.md` says review decisions are now landed and explicitly names current-disposition resolution as the next missing object.
  - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md` now says the next active Phase 4 line is one bounded analyzer-owned current-disposition resolution seam over exact persisted review decisions.
  - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` still marks Stage 15 as partial and names broader current-disposition-resolution as the remaining gap after reports, gates, and reviews landed.

- The lower governance stack is real in the live codebase.
  - Reports exist in `src/evaluations/schemas.py`, `src/evaluations/report_store.py`, `src/evaluations/frozen_pack_definitions.py`, and `src/evaluations/frozen_pack_harness.py`.
  - Gates exist in `src/evaluations/gate_schemas.py`, `src/evaluations/gate_store.py`, `src/evaluations/gate_definitions.py`, and `src/evaluations/gate_builder.py`.
  - Reviews exist in `src/evaluations/review_schemas.py`, `src/evaluations/review_store.py`, `src/evaluations/review_definitions.py`, and `src/evaluations/review_builder.py`.
  - Read-only evaluation inspection exists in `src/api/routes/evaluations.py` and is mounted under `/v1` in `src/api/main.py`.

- No current-disposition resolution layer exists today.
  - Repo search found no evaluation resolution schema, store, builder, definition, or route under `src/evaluations/` or `src/api/routes/`.
  - The current evaluation routes stop at:
    - `GET /v1/evaluations/reports`
    - `GET /v1/evaluations/gates`
    - `GET /v1/evaluations/reviews`

- Historical accumulation is already real, so a distinct “current” governance object is justified.
  - The repo currently contains 12 persisted evaluation reports in `src/evaluations/reports/`.
  - The repo currently contains 2 persisted gate decisions in `src/evaluations/gates/`.
  - The repo currently contains 1 persisted review decision in `src/evaluations/reviews/`.
  - `list_evaluation_gate_decisions(...)` and `list_evaluation_review_decisions(...)` sort newest-first but define no active/current concept.

- Exact-id authority is already the established Phase 4 contract pattern.
  - `build_evaluation_gate_decision(...)` consumes exact persisted `evaluation_report_id` inputs by `case_key`.
  - `build_evaluation_review_decision(...)` consumes one exact `gate_decision_id` and derives gate-linked truth from the loaded gate instead of accepting duplicated reviewer input.
  - The checked-in review `review-decision-21edf9b955ee` cites exact `gate-decision-745c2cb7e090`, and that gate cites exact report ids by case.

- The existing review subsystem already constrains any resolution design more than the memo fully reflects.
  - `PersistedEvaluationReviewDecision` already carries `review_key`, `review_definition_version`, `gate_decision_id`, `gate_key`, `gate_definition_version`, `evaluation_pack_key`, `disposition`, `observed_gate_verdict`, `contains_live_revalidation`, `observed_gate_blocking_reasons`, and `waiver_reasons`.
  - `build_evaluation_review_decision(...)` fails closed when the loaded gate mismatches the targeted review definition on `gate_key`, `gate_definition_version`, or `evaluation_pack_key`.
  - That means the resolution layer is not starting from a loose review record. It is already sitting on a tightly keyed compatibility contract.

- CLI/harness write plus read-only HTTP inspection is the right first boundary.
  - That matches the already-landed report, gate, and review pattern.
  - There is no live host-side governance UI or multi-user workflow in the current codebase that would justify widening the mutation surface now.

- Focused verification passed during this audit.
  - `PYTHONPATH=. pytest -q tests/test_evaluation_review_store.py tests/test_evaluation_review_routes.py tests/test_bounded_review_disposition.py tests/test_evaluation_gate_store.py tests/test_evaluation_gate_routes.py tests/test_bounded_release_gate.py`
  - result: `33 passed, 2 warnings`

# Findings

- High: the proposed persisted object is missing `resolution_key`.
  - The memo proposes `resolution_definition_version` but not `resolution_key`, even though it also proposes one code-defined resolution definition such as `bounded_platform_readiness_resolution_v1`.
  - That breaks the pattern already established by the gate and review layers, where the persisted object carries both the bounded law key and the version used.
  - Without `resolution_key`, the object cannot fully identify which resolution law produced it, and future resolution families would be ambiguous even if `resolution_definition_version` is present.

- High: the memo does not yet make “current adopted stance” authoritative enough to avoid a new silent latest-record convention.
  - The memo says the current stance is “the newest persisted resolution for the same review scope.”
  - But it does not define “same review scope” as a first-class persisted key, and it only proposes generic get/list inspection routes.
  - If callers have to list resolutions newest-first and choose the first row themselves, the system has only moved the implicit convention from “latest review wins” to “latest resolution row wins.”
  - The first slice needs one analyzer-owned current-resolution law in one place, such as a store/helper accessor and an explicit read seam that returns the current adopted stance for a declared scope.

- Medium: exact `review_decision_id` is the right external mutation input, but it is not a sufficient read/query boundary by itself.
  - The write path should stay exact-id and derive all lower-layer fields from the referenced review.
  - But the read side also needs explicit scope fields aligned with the already-enforced review compatibility contract: `review_key`, `review_definition_version`, `gate_key`, `gate_definition_version`, and `evaluation_pack_key`.
  - The memo’s proposed list route filters by `review_decision_id`, `gate_decision_id`, and `evaluation_pack_key`, but not by `review_key` or the resolution law itself. That is too weak once more than one review or resolution family exists.

# Scope Corrections

- Keep bounded current-disposition resolution as the next Stage 15 slice. Do not reopen lifecycle design, host UI, auth, or fresh live-proof work.

- Add `resolution_key` to the persisted object, summary object, store, and definition API. The resolution layer should mirror the existing Phase 4 object pattern: exact object id, bounded law key, law version, and derived lower-layer linkage.

- Define the resolution scope explicitly and centrally. At minimum, the current-resolution law should be keyed by the same compatibility fields already enforced at review build time:
  - `review_key`
  - `review_definition_version`
  - `gate_key`
  - `gate_definition_version`
  - `evaluation_pack_key`
  - plus the new `resolution_key`

- Preserve exact `review_decision_id` as the only external write input. The resolver should still load that one review, derive its gate/pack-linked truth, and fail closed on definition mismatch or blank resolver metadata.

- Add one authoritative current-resolution accessor in v1.
  - `GET /v1/evaluations/resolutions/{resolution_id}` and a generic list route are not enough by themselves.
  - The first slice should also expose one canonical way to answer the actual governance question, for example a dedicated “current resolution for scope X” retrieval seam or an equivalent analyzer-owned helper that the HTTP layer uses.

- Keep the object thin. Do not duplicate the full review or gate payload into a second truth store. Persist only the resolution law identity, exact adopted review identity, derived compatibility fields, resolver identity, note, and the small set of copied honesty labels already justified by the current review/gate design.
