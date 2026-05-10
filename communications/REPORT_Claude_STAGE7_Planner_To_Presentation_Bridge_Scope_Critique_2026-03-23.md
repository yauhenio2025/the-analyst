# Review: Stage 7 / Planner-To-Presentation Bridge Scope

Reviewer: Claude Opus 4.6
Date: 2026-03-23
Memo Under Review: `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`
Canonical Roadmap: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

---

## VERDICT: Approve after revision

The memo is strategically sound, correctly scoped, and grounded in real code seams. The revisions needed are clarifications, not directional changes.

---

## FINDINGS (ordered by severity)

### Finding 1 (HIGH): Stage 7 Substantially Overlaps Roadmap Stages 3-4

The roadmap defines three distinct stages:

- **Stage 3**: Move AOI from fixed profiles to task-driven composition
- **Stage 4**: Add AOI engine/source-selection law
- **Stage 7**: Formalize the planner-to-presentation bridge

The memo's proposed deliverables — a formal source catalog, explicit source selection with selected/rejected rationale, deterministic section materialization — are operationally identical to what Stages 3-4 describe. The memo builds "AOI source-selection law" and replaces "fixed profile→section bundles" with catalog-driven selection. That IS Stages 3-4 work under the Stage 7 label.

This is not necessarily wrong — the roadmap's recommended order (Section 10) already puts the bridge work third, before task-driven composition. But the memo should acknowledge the overlap explicitly and state whether Stage 7 completion partially or fully closes Stages 3-4, or whether those stages still have distinct residual work.

If Stage 7 lands as described, Stage 3 reduces to: "replace `profile` with task-based selector input." And Stage 4 reduces to: "allow the selector to reason dynamically beyond two fixed bundles." The memo should say this.

### Finding 2 (HIGH): Source Catalog Resolution Mixes Two Fundamentally Different Source Kinds Without Specification

The current code in `compose_from_intent.py:359-417` loads sources from two different backends:

1. **Artifact-based sources** (`load_aoi_normalized_artifact`) — for synthesis, engagement mapping, sin findings
2. **Phase-output-based sources** (`load_phase_outputs` + metadata parsing) — for the thematic report

The memo's candidate metadata schema acknowledges this with `source_kind: normalized_artifact | phase_output_metadata | normalized_report_payload`. But it does not specify:

- Whether the catalog resolution step queries both backends unconditionally or lazily
- Whether a candidate's availability is checked at catalog-build time or deferred to materialization
- How a phase-output-based candidate is validated for structural completeness (the current `_load_required_report_sections` does deep JSON parsing with multiple failure points)

This matters because the catalog must distinguish "source exists but is structurally broken" from "source does not exist." The current code collapses both into `ComposeFromSourceResolutionError`. The new catalog should separate these states in its candidate metadata.

### Finding 3 (MEDIUM): Plan-Context Usage Is Specified as "When Available" Without Defining What Fields

The memo says:

> Required inputs: source_v2_job_id, effective plan context if available, objective metadata if available

`load_effective_plan_context()` in `src/executor/plan_context.py` already returns structured plan context. The memo should specify which plan-context fields the source catalog resolution actually uses. Candidates include:

- `objective_key` — to know what the analysis was trying to achieve
- `workflow_key` — already available from the job itself
- `thinker_name`, `selected_source_thinker_id/name` — from plan_data
- Phase execution specs — which engines actually ran vs. were skipped

Without this, "use plan context when available" becomes an implementation-time guess rather than a specified contract.

### Finding 4 (MEDIUM): Missing Failure Mode — Partially Available Source Candidates

The memo describes two failure states:

- Source resolution 409 (already exists)
- Final renderer-contract 409 (already exists)

But it does not address the case where the source catalog resolves successfully (all expected candidate families are found) but one or more candidates are structurally invalid — e.g., the synthesis artifact exists but contains an empty or malformed payload.

The current code raises `ComposeFromSourceResolutionError` for any single source failure, which aborts the entire composition. The new catalog layer should decide:

- Does one invalid candidate abort the whole catalog? (Current behavior)
- Or can the selector downgrade it from "required" to "unavailable" and proceed with a reduced composition?

For Stage 7, either policy is acceptable. But the memo should name the policy explicitly rather than leaving it implicit.

### Finding 5 (MEDIUM): The Memo Names This "Planner-To-Presentation Bridge" But the Implementation Is "Source-To-Composition Bridge"

The roadmap's Stage 7 description says: "connect the existing planning/result substrate to dynamic composition in a reusable way." The memo references the planner/orchestrator infrastructure (planner.py, adaptive_planner.py, pipeline.py) in its "What already exists" section.

But the actual proposed implementation does not touch or use the planner/orchestrator infrastructure. It replaces hardcoded logic inside `compose_from_intent.py` with a catalog/selector/materializer chain. The inputs are `source_v2_job_id` + `profile`, not a planner-generated execution plan.

This is the correct bounded scope for this stage. But the memo should be honest that what it builds is a **source-to-composition bridge**, not yet a planner-to-presentation bridge. The true planner-to-presentation bridge (where the orchestrator/adaptive planner's output drives composition) is a later concern that requires the source bridge to exist first.

### Finding 6 (LOW): "compose-from-source-v2" Version Bump Is Correct But the Trace Should Version Independently

The memo proposes versioning both the response and trace to `compose-from-source-v2`. This is correct for regression distinguishability.

One improvement: the trace format is additive (prepending new stages before existing ones). If a future v3 changes the trace format again, downstream consumers need to know which trace format they're reading. Consider adding `trace_format_version` separately from `resolver_version`, or at minimum note that the trace contract is now versioned by the resolver_version field.

### Finding 7 (LOW): No Perspective Docs Folder Found

Confirmed: no "Perspective" documentation folder exists in either `/home/evgeny/projects/analyzer-v2/` or `/home/evgeny/projects/the-critic/`. The prompt asked me to report this explicitly.

---

## STRATEGIC ASSESSMENT

### The Diagnosis Is Correct

The memo correctly identifies the actual gap in the codebase. The `_build_source_sections()` function in `compose_from_intent.py:359-417` is exactly the hardcoded bridge that needs replacement. It does `if profile == "dossier"` → fixed artifact bundle, `else` → different fixed bundle. The source material load paths (`load_aoi_normalized_artifact`, `load_phase_outputs`) are inline, the selection rationale is implicit, and no trace stage exists for source resolution.

### The Scope Is Correctly Bounded

The memo is right to:

1. **Stay AOI-only** — generalizing source catalogs before proving the pattern on one workflow is premature
2. **Keep the consumer unchanged** — the-critic should not own source-catalog reasoning
3. **Keep `profile` as input** — removing it requires task-intake redesign (a later concern)
4. **Keep the public route stable** — POST /v1/presenter/compose-from-source stays as-is
5. **Version-bump the resolver** — allows regression tracking

### The Architecture Is In The Right Place

The bridge belongs in `src/presenter/` inside analyzer-v2. The memo correctly proposes one new module (`composition_source_bridge.py` or similar) plus modifications to `compose_from_intent.py` and `schemas.py`. The secondary touch points (`result_contract.py`, `plan_context.py`) are reasonable.

### The Existing Infrastructure Is Acknowledged But Not Over-Relied Upon

The memo correctly lists the existing orchestrator infrastructure but does not overreach by trying to wire it into this stage's deliverables. The adaptive planner, pipeline, and execution infrastructure exist for job-backed execution. This stage's bridge sits in the transient composition path, which is a different lifecycle. The connection between these two worlds is a later stage concern.

### The Strategic Risk Is Honest

The canonical roadmap warns: "more AOI app glue is not the same thing as more platform." This stage does not violate that warning — it moves internal bridge quality upstream rather than adding consumer-side glue. But the memo should be explicit that this stage is still AOI-specific and that the "reusable bridge" claim is architectural intention, not yet cross-workflow proof.

---

## RECOMMENDED MEMO REVISIONS

### Revision 1 (Required): Acknowledge Overlap with Stages 3-4

Add a section that explicitly states:

- Stage 7 subsumes the catalog/selection infrastructure that Stages 3-4 would need
- After Stage 7, Stage 3 reduces to replacing `profile` with task-driven selector input
- After Stage 7, Stage 4 reduces to broadening the selector's reasoning beyond two fixed bundles
- Update the roadmap's stage ledger accordingly when this stage lands

### Revision 2 (Required): Specify Source-Kind Resolution Policy

Add to the "formal analyzer-owned composition source catalog" section:

- Artifact-based candidates are resolved from `load_aoi_normalized_artifact`
- Phase-output-based candidates are resolved from `load_phase_outputs` with metadata parsing
- Availability is checked at catalog-build time (not deferred to materialization)
- A candidate that exists but is structurally invalid should be marked `state: invalid` in the catalog, not treated as missing
- If any required candidate is `invalid` or `unavailable`, the response should use the existing `ComposeFromSourceResolutionError` → 409 envelope, but now with the specific candidate key and failure reason

### Revision 3 (Required): Define Which Plan-Context Fields Feed Resolution

Replace "effective plan context if available" with a concrete field list:

- `objective_key` — used to enrich candidate composition-role hints
- `workflow_key` — used to select the candidate family registry
- Phase completion metadata — used to mark candidates from skipped phases as `unavailable`

State that missing plan context degrades catalog richness (fewer composition-role hints) but does not prevent resolution.

### Revision 4 (Recommended): Rename the Deliverable Honestly

The heading "Planner-To-Presentation Bridge" sets expectations that the orchestrator/planner infrastructure will be directly wired into composition. This stage does not do that — it builds a source-to-composition bridge. Consider:

- Rename to "Source-To-Composition Bridge" in the implementation scope
- Keep "Planner-To-Presentation Bridge" as the roadmap stage name (since the source bridge is a prerequisite step in that larger bridge)
- Explicitly state that the planner-to-composition connection is a subsequent deliverable that requires this source bridge to exist first

### Revision 5 (Recommended): State Partial-Availability Policy

Add one sentence: "For Stage 7, a composition that cannot resolve all required candidates for the selected profile is an error. Partial composition from reduced candidate sets is a Stage 3-4 concern."

---

## BEST NEXT MOVE

Write the execution plan from this memo as-is with the five revisions above applied.

The implementation should start by defining the `CompositionSourceCandidate` and `CompositionSourceCatalog` Pydantic models in a new `src/presenter/composition_source_bridge.py`, then refactor `_build_source_sections()` to use them. The refactoring should be incremental: first build the catalog from the same backends the current code uses, then add the selection/rejection trace, then add the materialization step, then version-bump.

The proof artifacts should be one real dossier run and one real comparison run through `compose-from-source-v2`, with the new trace stages visible in the saved JSON.

The documentary tail on rounds 13-14 should be explicitly addressed: either this stage's proof subsumes them or it does not. Do not leave that vague.

---

## ANSWERS TO FORCED QUESTIONS

### Q1: Is this actually the right next stage?
Yes, with the caveat that it substantially overlaps Stages 3-4 and the memo should acknowledge that. The roadmap's recommended order already puts bridge work third. Stages 1-2 are partially closed and this work does not conflict with closing them.

### Q2: Should it stay AOI-only?
Yes. The memo is correct. A second-workflow bridge requires generalizing source catalog schemas before the AOI catalog contract is even proven. That generalization is Stage 10 work.

### Q3: Is keeping compose-from-source stable the right bounded call?
Yes. The consumer should not need to change. The internal bridge improvement is invisible to the-critic.

### Q4: Is the bridge correctly in analyzer-v2?
Yes. Unambiguously. Source-catalog reasoning must not live in the consumer.

### Q5: Is keeping `profile` the right scoping decision?
Yes. `profile` as a bounded selector input over a formal catalog is the correct intermediate step. Removing `profile` requires a task-intake replacement that is Stages 3-4 work.

### Q6: Is the contract defined concretely enough to write an execution plan?
Almost. The candidate metadata schema, selection output, and materialization chain are clear enough. The missing pieces are: (a) source-kind resolution policy for artifacts vs phase outputs, (b) exact plan-context fields used, (c) partial-availability policy. With the five revisions above, the contract is sufficient.

### Q7: What is the biggest missing failure mode?
Partially available or structurally invalid source candidates. The current code treats missing and invalid the same way (abort with 409). The new catalog layer should distinguish these states even if the response is the same for Stage 7.

### Q8: What one revision would most improve the memo?
Revision 2: Specify source-kind resolution policy. This is the most implementation-critical gap because it determines how `CompositionSourceCatalog` actually resolves its candidates from two different backends.
