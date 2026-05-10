# Review: Phase 4 Bounded Release Gate Scope

Reviewer: Claude (Opus 4.6, 1M context)
Date: 2026-03-29
Memo under review: `communications/MEMO_2026-03-29_phase4_bounded_release_gate_scope.md`

## 1. Verdict

**Accept with revisions.**

The memo identifies the correct next slice. A bounded analyzer-owned gate decision over persisted evaluation reports is the natural successor to the report substrate that now exists. The alternatives (review/override UI, fresh live-rerun campaign, workspace revival) are all correctly rejected as premature or off-direction.

The memo's strategic reasoning is sound and its anti-drift filter application is honest. However, the scope has several under-specified areas that will create ambiguity at implementation time. These are mostly about the rule table shape, the report-accumulation problem, and the honesty labeling of mixed-mode evidence inheritance.

None of these are blockers to the direction. All of them should be named explicitly in the scope before implementation planning begins.

## 2. Findings

### 2.1 The direction is correct

Examined against the fixed-direction roadmap (`MEMO_2026-03-26`) and the canonical master roadmap, a gate decision object is the natural missing enforcement point.

The current state is:
- reports exist (`src/evaluations/schemas.py:49-62`, `PersistedEvaluationReport`)
- reports are persisted (`src/evaluations/report_store.py`)
- reports are inspectable (`src/api/routes/evaluations.py`)
- reports carry per-check evidence mode and per-case dimension summaries
- but no object says "the pack as a whole passes/fails for release purposes"

A gate decision is the smallest object that fills that gap. This passes the anti-drift filter: it moves governance upstream, it does not add consumer-owned logic, it generalizes across the two frozen cases, and it would survive host replacement.

### 2.2 Generate-then-gate is the right default, but the memo is ambiguous about its mechanics

The memo says the harness should "materialize the frozen report set for the named pack" and then "persist one gate decision over those exact report ids." This is the right default: deterministic one-shot gate runs that don't silently consume stale reports.

But the current harness (`frozen_pack_harness.py:36-44`) always generates *new* reports with fresh `evaluation_report_id` values. Each run produces new report files. The report store (`report_store.py`) does not have any deduplication, replacement, or "latest for pack" semantics.

This means:
- 8 reports already exist in `src/evaluations/reports/` from multiple harness runs
- a gate harness that calls `run_frozen_pack()` will produce 2 more reports each time
- the gate decision will cite the freshly-generated report ids, not the older ones

The memo should decide explicitly:
1. Does the gate harness re-invoke the report harness (generating fresh reports each time)?
2. Or does it consume the most recent reports for the pack from the store?
3. If (1), does the gate harness need a report-cleanup or replacement semantic?

The memo currently implies (1) but does not name the accumulation consequence. This is not a design flaw -- generate-then-gate is cleaner for auditability -- but it should be stated.

### 2.3 The rule table shape needs more explicit specification

The memo lists the default rule (lines 169-174):
- AOI case report must be `pass`
- genealogy case report must be `pass`
- all required dimensions on both reports must be `pass`
- any required `error` yields gate `error`
- any required `fail` yields gate `fail`
- only all-required-pass yields gate `pass`

But the two cases have **unlike dimension sets**:

AOI dimensions (from the persisted report `evaluation-report-48208f4ba042`):
- `selection_fit`
- `rationale_clarity`
- `rendered_usefulness`
- `operational_behavior`

Genealogy dimensions (from the persisted report `evaluation-report-f5f45e18d2d0`):
- `identity_integrity`
- `saved_truth_fidelity`
- `reopen_integrity`
- `boundary_observance`

The memo says the gate should list "required dimensions by case_key" but does not specify:
- which of the 8 total dimensions are required vs. optional at the gate level
- whether the gate rule table uses the dimensions already present in the reports, or defines its own required subset
- whether a dimension present in the report but absent from the gate's required list is silently ignored or treated as informational

For the bounded first gate this is likely "all dimensions required for both cases," but that should be stated explicitly so the gate definition in code is deterministic rather than ambiguous.

### 2.4 Mixed-mode evidence semantics are inherited but not explicitly acknowledged

The existing reports mix evidence modes at the check level:
- AOI check `executor_job_completed`: `live_revalidation_performed: true`
- AOI check `result_manifest_ready`: `live_revalidation_performed: true`
- AOI check `source_backed_readiness_ready`: `live_revalidation_performed: true`
- AOI checks for Stage 5 artifacts: `live_revalidation_performed: false` (frozen)
- Genealogy check `compose_session_exists`: `live_revalidation_performed: true`
- Genealogy checks for frozen artifacts: `live_revalidation_performed: false`

The memo says the gate "should remain retrospective and frozen-pack-scoped" and "must not be misrepresented as a fresh live release decision over arbitrary current head behavior." This is good.

But a gate decision that cites these reports inherits their mixed-mode character. Some checks in those reports read live state (executor DB, compose session store, result manifest) while others read frozen artifacts. The gate decision should carry an explicit field acknowledging whether its input reports contain any live-revalidation checks, so a future reader can tell the difference between "gate over purely frozen evidence" and "gate over mixed frozen + live-at-generation-time evidence."

This is an honesty-labeling issue, not a blocking design flaw. The fix is one field on the gate decision object (e.g., `contains_live_revalidation: bool`).

### 2.5 The read-only inspection seam is correctly scoped

The proposed endpoints:
- `GET /v1/evaluations/gates/{gate_decision_id}`
- `GET /v1/evaluations/gates?gate_key=...&evaluation_pack_key=...&limit=...`

These parallel the existing report inspection seam and are appropriate for v1. No mutation API is needed.

### 2.6 No review/override surface is needed yet

The memo correctly defers review/override tooling. A gate decision must exist before anyone can review or override it. Building review UI before the gate object exists would be premature abstraction.

### 2.7 The gate definition structure should be versioned

The memo proposes one gate definition `bounded_platform_readiness_v1` applying to pack `phase4_frozen_governance_v1`. This is the right scope.

However, the gate definition carries a rule table (required verdicts, required dimensions). If the rule table changes later, old gate decisions become incomparable to new ones. The gate definition should carry an explicit version or rule-table hash so gate decisions remain interpretable even after rule changes.

### 2.8 Report-to-gate evidence linkage is correctly required

The memo correctly requires that the gate decision record "exact input report ids by case_key." This is the critical audit property: the gate must cite the specific reports it evaluated, not just "the latest reports." The current harness architecture supports this cleanly since `run_frozen_pack()` returns the report objects with their ids.

## 3. Open Questions

### 3.1 Should the gate store be parallel to the report store?

The memo says "stored analyzer-side in file-backed JSON parallel to evaluation reports." Should gate decisions live in `src/evaluations/gates/` alongside `src/evaluations/reports/`? Or in a separate top-level path? The parallel structure is the obvious default but should be confirmed.

### 3.2 What happens with multiple gate decisions for the same pack?

If the gate harness is run twice for `phase4_frozen_governance_v1`, there will be two gate decisions (each citing different report ids from their respective harness runs). Is this expected behavior? Should the list endpoint return all of them? Should there be a "latest gate decision" convenience accessor? The memo should decide.

### 3.3 Should the gate decision carry the rule table it used, or just a reference?

Two options:
1. **Inline**: the gate decision JSON contains the full rule table (required cases, required dimensions per case, required verdict policy). Self-contained and auditable.
2. **Reference**: the gate decision JSON contains only a `gate_definition_key` that points to the code-defined gate. Smaller but requires the code to remain stable for interpretation.

For the bounded first slice, inline is safer because the gate decision remains self-interpretable even if the gate definition code changes later. But the memo should state the choice.

### 3.4 Does the gate harness need to verify report freshness or consistency?

If the gate consumes reports it just generated (generate-then-gate), freshness is guaranteed. But should the gate harness verify that the reports it generated are internally consistent (e.g., that both reports reference the same `evaluation_pack_key`)? This is probably already guaranteed by the harness flow, but an explicit consistency check would make the gate more defensible.

## 4. Concrete Revisions

### Revision 1: Specify the generate-then-gate mechanics explicitly

Add a section after "One deterministic gate harness" (section 3) that says:

> The gate harness should re-invoke the report harness internally, producing fresh reports and then evaluating them in one atomic run. It should not consume arbitrary pre-existing reports from the store. Each gate run produces its own paired report set and gate decision. Old reports from prior harness runs remain in the store as historical artifacts but are not consumed by new gate decisions.

### Revision 2: List required dimensions per case in the gate definition

Add to the gate definition section (section 2):

> The first gate definition should explicitly enumerate required dimensions per case:
>
> - AOI case: `selection_fit`, `rationale_clarity`, `rendered_usefulness`, `operational_behavior` -- all required
> - genealogy case: `identity_integrity`, `saved_truth_fidelity`, `reopen_integrity`, `boundary_observance` -- all required
>
> A dimension listed as required must be `pass` in the report for the case to pass at the gate level. A missing required dimension yields gate `error`.

### Revision 3: Add evidence-mode honesty label to the gate decision object

Add to the gate decision object properties (section 1):

> - `contains_live_revalidation: bool` -- true if any input report contains checks where `live_revalidation_performed` is true. This prevents a gate over mixed frozen+live evidence from being silently read as a gate over purely frozen evidence.

### Revision 4: Add rule-table versioning to the gate definition

Add to the gate definition section:

> The gate definition should carry a `gate_definition_version` (e.g., `"v1"`) that is recorded on every gate decision it produces. This allows future rule-table changes without making old gate decisions uninterpretable.

### Revision 5: Decide on gate decision storage path and accumulation policy

Add a brief note:

> Gate decisions should be persisted in `src/evaluations/gates/` as file-backed JSON, parallel to `src/evaluations/reports/`. Multiple gate decisions for the same pack and gate key are expected (one per harness run). The list endpoint should return them newest-first. No "one active gate" constraint is imposed in v1.

### Revision 6: Prefer inline rule table in the gate decision object

Add to section 1 properties:

> The gate decision should inline the rule table it evaluated against (required case keys, required dimensions per case, required verdict policy) rather than only referencing the gate definition key. This makes each gate decision self-interpretable without reading the gate definition code.

---

End of review.
