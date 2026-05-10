# Review: Stage 5 / AOI Exemplar Exit Gate Scope (Second Pass)

Reviewer: Claude Opus 4.6
Date: 2026-03-24
Memo under review: `communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md`
Prior review: First pass on same date, all six findings addressed in this revision.

---

## Verdict

**Approved.**

The revised memo closes every gap identified in the first-pass review. The six revisions are well-integrated: fixture-strength tiers are sharp, Stage 2 non-closure conditions are concrete, the rubric timing is honest, the latency decomposition is operationally useful, the locked non-profile readiness caveat is explicit, and the artifact-capture method is concrete enough to execute. The four-case eval pack — including the upgrade from generic "blocked/ambiguous" to real `aoi_selection_blocked` — is the right shape.

No further revisions are required before implementation.

---

## Findings (Ordered by Severity)

### 1. OBSERVATION — The `aoi_selection_blocked` case is operationally feasible and correctly specified

Verified against `task_planner.py`. The `aoi_selection_blocked` outcome is reachable through five distinct reason codes:

- `no_usable_source_families` — catalog resolution finds zero available candidates
- `llm_timeout` — LLM selection call exceeds 10s timeout
- `llm_provider_failure` — API key missing or provider error
- `llm_invalid_output` — LLM returns unparseable JSON
- `llm_selection_failed_validation` — LLM selection fails post-parse validation

The `no_usable_source_families` code is the most natural for a proof case. Crucially, `route-task` can succeed (it only checks that `source_v2_job_id` exists as a field, not that it points to a job with available AOI outputs), and then `plan-task` discovers the block. This is the correct seam separation: routing succeeds, planning fails closed.

The memo's upgrade from "blocked or ambiguous" to "one real planner-primary `aoi_selection_blocked`" is a meaningful improvement. It forces the eval to exercise the actual selector-path failure envelope rather than a generic routing-level rejection.

**No action needed.** This is a confirmation.

### 2. OBSERVATION — The locked non-profile readiness caveat is correctly scoped

The revised Decision 3 now explicitly says:

> this locked eval case should run through direct planner-to-compose continuation from `plan-task` into `compose-from-selection`

This is the right call. Verified: the readiness-discovery API (`source_backed_readiness.py`) returns `allowed_selectors` as profile names only. The `compose-from-selection` path in `composition_source_bridge.py:456-517` accepts arbitrary explicit selections without referencing `_PROFILE_SELECTION_PRESETS`. The planner in `task_planner.py` can generate a `thematic_synthesis + engagement_mapping + thematic_report` selection and `_infer_legacy_profile_equivalent()` will return `None` for it.

The caveat correctly preserves the option to add a readiness-surface fix if the implementor chooses, without requiring it.

**No action needed.**

### 3. OBSERVATION — Fixture-strength tiers are sharp and the Stage 2 gate is honest

The three tiers (`fixture_backed`, `execution_backed`, `user_initiated`) are clearly defined. The Stage 2 gate — "Stage 2 should not be documentary-closed unless at least one ready case is `execution_backed` or stronger" — is the right threshold.

The four concrete non-closure conditions in revised Decision 5 are all operationally testable:

- all ready cases only fixture-backed → checkable by tier label
- locked non-profile cannot be demonstrated → checkable by eval outcome
- negative case is not a real `aoi_selection_blocked` → checkable by outcome type
- eval pack cannot show repeated bounded AOI transient use → checkable by case count

**No action needed.**

### 4. OBSERVATION — The rubric timing and threshold shape resist self-certification

The revised Decision 9 requires:
- rubric written before grading
- explicit pass/fail boundaries per dimension
- minimum threshold shape that differentiates ready cases from the blocked case

The threshold shape is well-chosen: requiring `operational_behavior` for all cases, `selection_fit` and `rendered_usefulness` for ready cases, and "honest blocked visibility and auditability" for the `aoi_selection_blocked` case correctly adapts the rubric to what each case type can demonstrate.

**No action needed.**

### 5. OBSERVATION — The artifact-capture method is concrete and executable

The default capture method (browser HAR + JSON excerpts for `route-task`, `plan-task`, host compose request, analyzer compose response) is realistic given the current code. The `the-critic` host proxy at `server.py:20568-20616` validates and forwards `compose-from-selection` with enough logging points to extract the required artifacts.

One practical note: the HAR capture for the `aoi_selection_blocked` case will show a shorter request chain (route + plan, no compose), which is correct — the blocked case should not reach the compose step.

**No action needed.** This is just a note for the implementor.

### 6. LOW — Host-side `aoi_selection_blocked` display specificity is not addressed

The memo requires saving the blocked case's "rendered blocked state." The host (`AoiV2ThematicPanel.tsx`) handles planner outcomes and shows them, and `taskLaunchRuntime.ts` types the `aoi_selection_blocked_reason_code` field. But the memo does not specify whether the host must display the *specific* blocked reason code (e.g., `no_usable_source_families`) or whether a generic "planning blocked" state is sufficient.

This is not a blocker. The existing host code does type these fields, and the eval pack can capture whatever the host currently displays. But if the rubric's `operational_behavior` dimension is meant to assess blocked-outcome clarity, the implementor should know whether "blocked" is enough or whether the specific reason code must be visible.

**Suggestion for implementor:** When writing the rubric's `operational_behavior` pass/fail boundary for the blocked case, state explicitly whether the blocked reason code must be user-visible or only captured in the saved artifact trail.

---

## Open Questions

1. **Should the `aoi_selection_blocked` case use `no_usable_source_families` specifically?** This is the most deterministic and "real" reason code (it reflects actual source-catalog state rather than LLM infrastructure failure). But `llm_selection_failed_validation` tests more of the selector path. The memo correctly leaves this choice to the implementor, but the closeout should record which reason code was exercised.

2. **Will the evolution-focused and engagement-focused ready cases produce `legacy_profile_equivalent` values?** Based on `_infer_legacy_profile_equivalent()` in `composition_source_bridge.py:789`, if the evolution case selects `thematic_synthesis + thematic_report` it will map to `"dossier"`, and if the engagement case selects `engagement_mapping + sin_findings + thematic_report` it will map to `"comparison"`. This is fine — the memo requires awareness ("whether any ready case still mapped to `legacy_profile_equivalent`") without prohibiting it. The locked non-profile case is the one that must not map.

---

## Judgment on Sequencing and Bigger-Picture Fit

### Sequencing

Stage 5 remains unambiguously the right next step. The draft roadmap's Tranche 2 (complete the AOI exemplar) explicitly places the Stage 5 eval gate as a precondition for Tranche 3 (de-AOI the transient substrate). The Milestone A completion memo names Stage 5 as the immediate next gate. No intervening structural work is needed or justified.

### Evidence-vs-architecture posture

The memo correctly maintains its identity as an evidence-and-evaluation tranche throughout. The revision did not introduce any scope creep. The "allowed exception" (one small compatibility fix) remains properly bounded. Decision 1 still defaults to evaluating rather than redesigning.

### Stage 2 honesty

The revision strengthens Stage 2 handling materially. The non-closure conditions are concrete and verifiable. The `execution_backed` minimum for Stage 2 closure is the right bar — it prevents closing Stage 2 on pure fixture recomposition while keeping the gate achievable.

### Broader platform fit

The memo's non-goals and bounded-claim sections remain correctly scoped. The exit evidence section names exactly what this does not prove. The strategic importance section correctly frames this as turning an architectural cutover into an empirically supported exemplar — which is the honest bridge to later transient-substrate generalization.

### Fixture-backed proof acceptability

Fixture-backed cases are acceptable for seam audit within this exit gate. The fixture-strength tier model provides the right transparency layer. The Stage 2 closure gate ensures that the program cannot claim full transient MVP closure on fixtures alone.

---

## Concrete Revisions Recommended Before Implementation

**None.**

The revised memo is ready for implementation. The observations above are notes for the implementor, not scope revisions.
