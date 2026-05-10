# Audit: Stage 5 AOI Execution-Backed Browser Closeout Scope

Date: 2026-03-25
Auditor: Claude Opus 4.6
Source: `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_browser_closeout_scope.md`
Verdict: **Approve with revisions**

---

## Verdict Rationale

The memo is well-scoped, intellectually honest, and correctly sequenced in the broader program. Its core claim — that the remaining gap is a bounded browser proof on a recovered fresh run, not a new architecture or repair slice — is supported by the codebase and the preceding artifact trail.

Three revisions are needed before execution:

1. Acknowledge and mitigate the row-ordering selection ambiguity
2. Sharpen the "one success = enough for Stage 2?" question into a testable threshold
3. Make the warm-snapshot-to-compose identity continuity check explicit in the counted bundle

---

## Findings (Ordered by Severity)

### Finding 1: Row-ordering selection ambiguity is real but manageable (Medium)

**Problem**: The memo requires "explicit selection of the recovered saved-result row" (Decision 3), but the codebase has an implicit fallback that could silently bind to the wrong row.

`AoiV2ThematicPanel.tsx:254`:
```typescript
const selectedSource = currentSourceResult ?? savedResults[0] ?? null;
```

`savedResults` is sorted by `effective_completed_at` descending (line 132-137), so `savedResults[0]` is the most-recently-completed result. If another AOI result for the same thinker was saved or imported after the recovered fresh run completed (e.g., from a parallel session or a stale import), that newer row would become the default selection, silently binding compose to the wrong source.

The frontend does require `selectedSource.v2_job_id` to be present before the planner-backed handoff fires (line 552-555), and the URL param `source_v2_job_id` is set explicitly from the selected row (line 664). So the identity is preserved downstream once a row is selected. The risk is only in the initial auto-selection fallback.

**Mitigation**: The operator must explicitly click the recovered fresh row rather than relying on auto-selection. The counted proof bundle should capture the selected row's `v2_job_id` and `analysis_id` before compose, and the closeout should confirm these match `job-6ee8b0621177` / `gen-v2-18853b558ef1`.

**Recommended revision**: Add to Decision 3: "The operator must explicitly click/select the recovered fresh result row in the panel and verify its identity before initiating the planner-backed handoff. The artifact bundle must include the pre-compose selected-row identity as a separate verification step, not only the compose request payload."

### Finding 2: `source_v2_job_id` preservation through compose-from-selection is sound (Low / Positive)

The full chain was traced:

1. **Frontend** (`AoiV2ThematicPanel.tsx:575,664`): Sets `source_v2_job_id` from the selected row in both the planner request and the navigation URL params
2. **Compose page** (`AoiComposeFromIntentPage.tsx:233,437`): Reads `source_v2_job_id` from URL and passes it in the `composeFromSelection` POST body
3. **Critic proxy** (`server.py:20911-20925`): Runs `_resolve_source_backed_compose_identity()` which validates the `source_v2_job_id` against the run reference DB, then passes the resolved ID to analyzer-v2 (line 20925)
4. **Analyzer-v2 validation** (`compose_from_intent.py:547-562`): Pydantic validates `source_v2_job_id` is a required non-empty string
5. **Bridge** (`composition_source_bridge.py:297,304,392`): `source_v2_job_id` is stored in `CompositionSourceCatalog` and preserved in trace output

**No rewriting risk exists on the counted path.** The canonical ID is immutable once set. The 409-conflict guards in `_resolve_source_backed_compose_identity` (server.py:18897-18901, 18935-18939) correctly reject mismatched identities.

### Finding 3: Warm snapshot does not rewrite `source_v2_job_id` (Low / Positive)

The local snapshot backfill in `_best_effort_ensure_local_snapshot_analysis_id` (server.py:19029-19120) creates a `GenealogyAnalysisDB` record with `pass_results._v2_job_id` set to the canonical upstream job ID (line 19132). The backfilled analysis ID is stored in `V2RunReferenceDB.local_snapshot_analysis_id` (line 19114).

When compose-from-selection runs, `_resolve_source_backed_compose_identity` receives the explicit `source_v2_job_id` from the frontend. Since the frontend passes both `source_analysis_id` (from the selected row) and `source_v2_job_id` (also from the selected row), the identity resolution validates they match (server.py:18897). The warm snapshot cannot silently substitute a different `source_v2_job_id`.

The memo's Decision 7 stop-rule ("warm snapshot rewrites or drops the canonical `source_v2_job_id`") is already structurally prevented by the code. This is a positive finding.

### Finding 4: The recovered fresh run's durable queryability is verified (Low / Positive)

The recovery summary (`PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`) confirms:

- `job_status = completed`
- `result_state = ready`
- `presentation_status = completed`
- `restore_available = true`
- `critic_saved_result_resolves = true`
- `analysis_id = gen-v2-18853b558ef1`

The Critic job-detail route (server.py:19788-19953) and saved-result route (server.py:20447-20483) both resolve this run. The backfill mechanism created a durable local snapshot. This run is a valid counted source.

### Finding 5: Is one successful browser closeout enough for Stage 2? (Medium — needs sharpening)

The rubric (frozen rubric memo, Stage 2 closure gate) requires:

1. Stage 5 seam gate passes ✓ (already passed)
2. At least one ready case is `execution_backed` or stronger
3. Evidence strong enough to support "repeated bounded AOI transient use rather than fixture-only seam proof"

The memo correctly asks this question in Decision 6 and does not pre-answer it. However, the memo should acknowledge more honestly that one recovered case is a marginal proof for criterion 3. The case proves the path works once on one recovered run. Whether it proves "repeated use" reliability depends on:

- whether the recovered run traversed all the same code paths a future fresh run would
- whether the recovery repairs themselves introduce fragility that a clean first-pass run would not have

The memo should not lower the bar, but it should state these considerations so the closeout decision is made with open eyes.

**Recommended revision**: Add to Decision 6: "The closeout should explicitly assess whether the recovery repairs (auto-presentation fix, local snapshot backfill) introduce transient-only scaffolding that a future clean run would not need, or whether they represent durable infrastructure fixes. If the former, one recovered case may not be strong enough for the 'repeated use' bar even if it passes all rubric dimensions."

### Finding 6: The memo correctly freezes broader scope (Low / Positive)

The decisions to:

- not reopen the frozen four-case pack
- not launch a new AOI run by default
- not reopen selector/provider logic, identity continuity, warm-snapshot durability
- keep Tranche 3 blocked
- require explicit stop-and-revise on drift

are all well-supported by the artifact trail. The Stage 5 seam gate already passed on fixture-backed evidence. The fresh run already exists and is recovered. The only missing element is the counted browser compose bundle on that run. This is the right bounded next step.

### Finding 7: No missing artifact fields detected (Low / Positive)

The proposed deliverable structure (Decision 4) requires cross-linking through:

- recovered live summary (exists: `PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`)
- selected saved-result row identity
- `/compose-from-intent` URL/query state
- `compose-from-selection` request payload
- counted HAR / screenshot

The compose-from-selection request schema (`ComposeFromSelectionRequest` in `src/presenter/schemas.py`) requires `source_v2_job_id` as a mandatory string field. The Critic proxy (server.py:20922-20925) passes the resolved ID. The request artifact will necessarily contain this field if the compose succeeds.

### Finding 8: Browser URL state drift risk is structurally low (Low)

`AoiComposeFromIntentPage.tsx` reads `source_v2_job_id` from URL search params (line 233). The planner-backed flow sets this param explicitly during navigation (line 664 of `AoiV2ThematicPanel.tsx`). The normalization functions (lines 89-127 of `AoiComposeFromIntentPage.tsx`) trim empty strings to `undefined` but do not rewrite non-empty values.

The autostart path (lines 452-484) checks `sourceAnalysisId` but NOT `sourceV2JobId`, meaning autostart could theoretically fire without `source_v2_job_id`. However, the counted path for this slice is planner-backed compose-from-selection (not autostart), so this is not a risk for the current scope.

### Finding 9: The "no new AOI launch by default" freeze is correct (Low / Positive)

The memo's Decision 2 reasoning is sound:

- The recovered fresh run exists and is durable
- Launching another long AOI run (~30-120 min) before testing the browser path on the recovered run would waste time and blur the documentary trail
- If the browser path fails on the recovered run, a revision memo will document why

This is operationally correct. The fresh run is already execution-backed (launched through the real route, produced real outputs). The question is whether the browser path can consume it, not whether the backend can produce it.

---

## Direct Answers to Prompt Questions

### Q1: Does the codebase support the scope as written?

**Yes, with one caveat.** The compose-from-selection identity chain is sound end-to-end. The row-selection fallback (`savedResults[0]`) creates an ambiguity that the memo should acknowledge explicitly (Finding 1). The saved-result row selection, warm snapshot identity, and planner-backed compose routing all work as the memo assumes, provided the operator selects the correct row.

### Q2: Is the recovered fresh run technically and documentarily strong enough to count as `execution_backed`?

**Yes.** The run was launched through the real `POST /api/influence/thinkers/otto_neurath/run-thematic-analysis-v2` route, produced real outputs via `job-6ee8b0621177`, completed with `result_state = ready` and `presentation_status = completed`, and is durably queryable through both Critic job-detail and saved-result routes. The recovery repairs (auto-presentation, local snapshot backfill) fixed infrastructure seams, not the analytical outputs themselves. The run's freshness is documented and cross-linked.

The recovery does not collapse this into "fixture-backed reuse" because the analytical outputs were genuinely produced by this run, not imported from a prior snapshot.

### Q3: Is the memo right to freeze "no new AOI launch by default"?

**Yes.** This is the correct decision. A recovered fresh run already exists. Testing the browser path on it is the right next step before spending another 30-120 minutes on a new launch. If the browser path fails, the revision memo can authorize a new launch with that failure context.

### Q4: Are there hidden operational dependencies?

- **Row ordering / selection ambiguity**: Yes, Finding 1 above. Mitigable by explicit operator row selection.
- **Browser URL state drift**: Low risk (Finding 8). The planner-backed flow sets params explicitly.
- **Local snapshot replacement**: No risk. Snapshot backfill preserves `_v2_job_id` and does not overwrite existing snapshots.
- **Saved-result identity mismatch**: Low risk. `_resolve_source_backed_compose_identity` validates both `source_analysis_id` and `source_v2_job_id` match. Mismatches raise 409.
- **Missing artifact fields**: No risk. `ComposeFromSelectionRequest.source_v2_job_id` is a required Pydantic field.

### Q5: Is one successful browser closeout enough for Stage 2 closure?

**Probably, but the closeout must argue it honestly.** The rubric requires evidence "strong enough to support repeated bounded AOI transient use." One successful browser compose on a recovered run proves the path works once. Whether the recovery-specific scaffolding (auto-presentation fix, snapshot backfill) represents durable infrastructure or transient workarounds determines whether "once" extrapolates to "repeated." The closeout should assess this directly.

The memo correctly does not pre-determine this answer (Decision 6). The revision I recommend (Finding 5) strengthens the closeout by requiring explicit assessment of recovery-repair durability.

### Q6: Is the memo right not to rerun the frozen pack again?

**Yes.** The frozen pack already passed the Stage 5 seam gate. This slice exists to add execution-backed browser evidence on top of that baseline. Rerunning the pack would produce the same fixture-backed result and add no new information.

### Q7: Does the memo keep the roadmap honest?

**Yes.**

- Stage 5 seam gate: already passed (frozen pack, fixture-backed) — correctly stated
- Stage 2: still open until counted browser closeout — correctly stated
- Tranche 3: still blocked until Stage 2 decision — correctly stated

The memo does not inflate progress. It does not conflate "recovered fresh run exists" with "Stage 2 closed." It correctly identifies the browser closeout as the remaining evidence gap.

---

## Recommended Revisions Before Execution

### Revision 1: Acknowledge row-ordering selection ambiguity

In Decision 3, after "the operator must verify that the selected saved-result row is the recovered fresh run," add:

> The AoiV2ThematicPanel auto-selects the most-recently-completed result if no row is explicitly clicked (`savedResults[0]` sorted by `effective_completed_at` descending). If any other AOI result for this thinker was saved or imported after the recovered fresh run completed, that newer row would become the default selection. The operator must therefore explicitly click the recovered fresh row rather than relying on auto-selection. The pre-compose selected-row identity (including `v2_job_id` and `analysis_id`) must be captured as a separate verification artifact before the planner-backed handoff fires.

### Revision 2: Sharpen the "repeated use" assessment requirement

In Decision 6, after the four closeout questions, add:

> The closeout should also assess whether the two recovery repairs — analyzer auto-presentation routing fix and Critic local snapshot backfill — represent durable infrastructure improvements that benefit all future runs, or transient scaffolding specific to this recovered case. If the former, one successful recovered case is stronger evidence for the "repeated use" bar. If the latter, the closeout should state honestly that repeated-use confidence requires at least one clean first-pass run.

### Revision 3: Add explicit warm-snapshot identity verification step

In Deliverable 1, add a sub-bullet:

> - one pre-compose row-identity artifact proving that the selected row in the AoiV2ThematicPanel resolves to `v2_job_id = job-6ee8b0621177` and `analysis_id = gen-v2-18853b558ef1` before the planner-backed handoff is initiated

This prevents a scenario where the compose request is correct but was issued against a different row than the operator thought was selected.
