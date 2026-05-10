# Report: Phase 4 Bounded Governance Evaluation Scope Audit

Date: 2026-03-28
Audited memo: `communications/MEMO_2026-03-28_phase4_bounded_governance_evaluation_scope.md`

## Verdict

Approve with scope corrections.

The memo has the right main direction. Phase 4 governance/evaluation is now the correct next line after the March 28 Phase 3 closeout, and analyzer-owned evaluation reports are the right first governance object.

But the first slice is not fully well-bounded as written. The memo understates the inspection/report substrate that already exists in code, and it treats the frozen pack too much like two single subjects instead of two composite evidence packs. The correct first slice is:

- a thin persisted evaluation-report layer
- over existing analyzer-owned manifests, readiness decisions, traces, planning snapshots, and compose sessions
- plus explicit frozen proof-artifact references

not a greenfield governance subsystem that starts as if those seams do not already exist.

## Verified Claims

- Phase ordering is correct. The fixed roadmap now marks Phase 3 as closed, says no analyzer-owned governance/evaluation report substrate exists yet, and makes Phase 4 the next active main line (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:312-330`, `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:401-424`).

- No first-class `evaluation_report` object or persistent evaluation-report store exists in the live codebase. A repo-wide search across `src/` and `tests/` found no `evaluation_report` or `PersistedEvaluationReport`.

- Analyzer-owned durable planning and lifecycle truth already exist and are retrievable:
  `PersistedTaskPlanningDecision` is file-backed and exposed via `/v1/orchestrator/planning-decisions/{planning_decision_id}` plus the lowering seam (`src/orchestrator/planning_decision_store.py:26-58`, `src/orchestrator/planning_decision_store.py:111-120`, `src/orchestrator/task_planning_schemas.py:223-258`, `src/api/routes/orchestrator.py:351-394`).

- Analyzer-owned transient lifecycle persistence already exists:
  `PersistedComposeSession` is file-backed and exposed via `POST /v1/presenter/compose-sessions` and `GET /v1/presenter/compose-sessions/{session_id}` (`src/presenter/compose_session_store.py:30-76`, `src/presenter/schemas.py:737-759`, `src/api/routes/presenter.py:479-520`).

- The codebase already has first-class read-only inspection/report-like seams:
  `AnalysisResultManifest`, result presentation, and `SourceBackedReadinessDecision` are typed analyzer-side inspection objects, not just raw files (`src/analysis_products/result_contract.py:221-355`, `src/analysis_products/source_backed_readiness.py:46-260`, `src/analysis_products/schemas.py:109-124`, `src/api/routes/results.py:50-123`).

- The presenter already exposes data-light and trace inspection surfaces:
  `GET /v1/presenter/manifest/{job_id}` and `GET /v1/presenter/trace/{job_id}` (`src/api/routes/presenter.py:251-300`).

- The frozen AOI subject is present in durable analyzer state. Local read-only invocation of `build_result_manifest('job-744edf255ad5')` returned `result_state=ready`, `presentation_status=completed`, and `restore_available=true`. Local read-only invocation of `build_source_backed_readiness('job-744edf255ad5')` returned `readiness_status=ready` with both AOI profiles allowed. The job also exists in `executor_jobs` with `workflow_key=anxiety_of_influence_thematic_single_thinker`.

- The frozen genealogy source subject is present in durable analyzer state, and the lifecycle subject is present in analyzer-owned saved-session storage. Local read-only invocation of `build_result_manifest('proof-round4-adaptive-balance-final-1774012011')` returned `result_state=ready` and `restore_available=true`. Local read-only invocation of `build_source_backed_readiness('proof-round4-adaptive-balance-final-1774012011')` returned a typed readiness verdict. `src/presenter/compose_sessions/compose-session-0877864dcca7.json` also exists locally and matches the March 28 saved-session proof artifact.

- The older March 19 generic-workspace Phase 4 line is correctly superseded. The canonical roadmap now records Stage 10 readiness inspection as landed and places governance/evaluation after the generalized bridge and bounded lifecycle work, not as another workspace-productization pass (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:358-377`).

## Findings

No high-severity contradiction blocks the memo. The issues are scope precision and evidence-shape precision.

### 1. Medium: the memo is wrong to say there is no first-class inspection surface beyond raw traces, raw proof artifacts, and prose memos

That claim is too absolute.

What already exists in code:

- `GET /v1/results/by-job/{job_id}` returns a typed `AnalysisResultManifest` with result state, restore state, artifact families, and route links including `trace_url` (`src/analysis_products/result_contract.py:221-236`, `src/analysis_products/result_contract.py:240-355`, `src/api/routes/results.py:50-72`).
- `GET /v1/results/by-job/{job_id}/source-backed-readiness` returns a typed `SourceBackedReadinessDecision` with normalized `ready / partially_ready / blocked` verdicts, explicit blockers, downstream contract, and trace (`src/analysis_products/source_backed_readiness.py:46-260`, `src/analysis_products/schemas.py:109-124`, `src/api/routes/results.py:100-123`).
- `GET /v1/presenter/manifest/{job_id}` and `GET /v1/presenter/trace/{job_id}` already provide read-only manifest and decision-trace inspection (`src/api/routes/presenter.py:251-300`).

Why this matters:

- The memo is right that there is no analyzer-owned persisted cross-case evaluation-report object.
- The memo is wrong if read literally as “nothing inspectable exists.”
- If Phase 4 ignores these existing seams, it will duplicate current contracts instead of layering a governance verdict on top of them.

### 2. Medium: the AOI frozen pack is too narrow if it is modeled as only `job-744edf255ad5`

The March 27 AOI closeout did not stand on that one execution-backed job alone.

The closeout memo is explicit that:

- the frozen Stage 5 four-case seam gate is carried forward rather than replaced
- the fresh March 27 execution-backed Otto rerun adds stronger-than-fixture evidence
- the Stage 2 decision passes because of the combined evidence (`communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md:41-54`, `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md:150-158`)

There is also already a frozen AOI rubric and AOI eval-summary artifact family:

- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json`

So the honest AOI case for Phase 4 is:

- primary subject: `job-744edf255ad5`
- supporting frozen evidence: the carried-forward Stage 5 four-case eval pack plus the March 27 execution-backed closeout artifacts

If Phase 4 reduces AOI to the March 27 job and its closeout artifacts only, it drops the blocked-case and non-profile evidence that the Phase 0 closeout explicitly relied on.

### 3. Medium: the genealogy frozen pack must be session-centric and composite, not planning-decision-centric

The memo correctly picks `session_id = compose-session-0877864dcca7` as canonical subject identity for the genealogy lifecycle case.

That is important because the supporting planning identity is not stable enough to be the canonical subject:

- the saved session stored in `src/presenter/compose_sessions/compose-session-0877864dcca7.json` points to `planning-decision-2524994934e0`
- the earlier Phase 2 live proof memo centered `planning-decision-b1600d054991`
- the local planning-decision store contains multiple March 28 planning snapshots for the same genealogy source job

What the code supports:

- `PersistedComposeSession` is the durable lifecycle object (`src/presenter/schemas.py:746-759`)
- `PersistedTaskPlanningDecision` is a durable planner snapshot, not the lifecycle object (`src/orchestrator/task_planning_schemas.py:246-258`)

Why this matters:

- the genealogy pack should use `session_id` as primary subject
- `source_v2_job_id`, `planning_decision_id`, preflight proof, reopen-segment proof, and invalid-session proof should be supporting evidence references
- Phase 4 should not accidentally regress into treating `planning_decision_id` as lifecycle identity

### 4. Medium: evaluation from durable truth plus saved proof artifacts is honest only as retrospective frozen-evidence evaluation

The memo is directionally right to avoid fresh reruns by default.

But the report semantics must stay honest about what this means.

What can be derived from current analyzer-owned durable truth:

- AOI result state, artifact availability, and AOI source-backed readiness over `job-744edf255ad5`
- genealogy result state over `proof-round4-adaptive-balance-final-1774012011`
- genealogy saved-session payload fidelity over `compose-session-0877864dcca7`

What still depends on saved proof artifacts rather than present durable truth alone:

- the AOI browser-path claims: `Clear`, explicit row pin, no legacy fallback, preserved dual identity in the host request, real browser continuity (`communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_decision.md:78-106`)
- the genealogy reopen claims: fresh-navigation reopen, one saved-session GET, zero planner/composition replay, invalid-session fail-closed (`communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_closeout.md`, `communications/PROOF_phase3_bounded_lifecycle_v1_reopen_segment_2026-03-28.json`, `communications/PROOF_phase3_bounded_lifecycle_v1_invalid_session_2026-03-28.json`)

So Phase 4 can honestly evaluate from frozen truth without reruns, but only if the report says what it actually is:

- a verdict over frozen evidence captured on March 27 and March 28
- not a fresh runtime validation of the current head by itself

### 5. Low: the memo overstates the absence of normalized verdict assets

There is still no shared analyzer-owned cross-case persisted evaluation-report substrate. That part is correct.

But “no normalized case verdicts” is too broad:

- AOI already has a frozen rubric and eval-summary JSONs in `communications/`
- Stage 10 already introduced a typed analyzer-owned readiness decision object with normalized status values and blocker structure (`src/analysis_products/schemas.py:109-124`)

The missing thing is not “any normalized verdict asset at all.”
The missing thing is:

- one shared analyzer-owned persisted cross-case governance report object
- plus one shared pack contract that normalizes how those verdicts cite evidence

## Scope Corrections

1. Keep `PersistedEvaluationReport` as the first governance object, but make it a thin verdict layer.

The report should store:

- `evaluation_report_id`
- pack and case identity
- subject identity
- ordered checks
- dimension summaries
- overall verdict
- explicit evidence references

It should not copy full manifests, traces, saved sessions, or proof payloads into a second parallel truth store.

2. Make the frozen evidence-pack contract the first-class foundation of the slice, not an implied side detail.

The implementation needs a typed pack contract that can point to both:

- analyzer-owned objects and routes
- frozen `communications/PROOF_*` artifacts

Without that, “deterministic reports from durable truth and proof artifacts” stays under-specified.

3. Define the AOI pack as a composite evidence pack.

Use:

- primary subject: `job-744edf255ad5`
- supporting evidence: March 27 closeout artifacts
- supporting carried-forward evidence: the Stage 5 AOI rubric and Stage 5 four-case eval-summary artifacts

Also reuse the already-frozen AOI dimensions where possible:

- `selection_fit`
- `rationale_clarity`
- `rendered_usefulness`
- `operational_behavior`

4. Define the genealogy lifecycle pack as a composite evidence pack.

Use:

- primary subject: `compose-session-0877864dcca7`
- supporting source subject: `proof-round4-adaptive-balance-final-1774012011`
- supporting analyzer objects: the saved compose session and the planning snapshot referenced by that saved session
- supporting proof artifacts: preflight, saved-session proof, reopen-segment proof, invalid-session proof

Treat `planning_decision_id` as a provenance reference, not as canonical lifecycle identity.

5. Add explicit retrospective-evidence semantics to the report shape.

The report should say, in fields not just prose:

- evidence observation date
- evidence mode: frozen artifact audit
- whether live rerun was performed
- whether the verdict is retrospective or freshly revalidated

For this slice, retrospective frozen-evidence verdicts are enough. Fresh live reruns should remain out of scope by default.

6. Reuse the existing analyzer inspection seams instead of rebuilding them.

The Phase 4 harness should derive checks from existing truth sources such as:

- `GET /v1/results/by-job/{job_id}`
- `GET /v1/results/by-job/{job_id}/source-backed-readiness`
- `GET /v1/presenter/manifest/{job_id}`
- `GET /v1/presenter/trace/{job_id}`
- `GET /v1/orchestrator/planning-decisions/{planning_decision_id}`
- `GET /v1/presenter/compose-sessions/{session_id}`

Then add exactly one new read-only report retrieval seam on top.

7. Keep the delivery bounded exactly as the memo intends in its anti-widening rules.

The first slice does not need:

- human approval UI
- a new Critic review page
- publish/share workflow
- new consumer registration
- fresh browser reruns by default

The right proof vehicle remains analyzer-owned persisted reports over frozen bounded evidence, but the slice should be framed as extension and normalization of the existing results/readiness/trace substrate, not as a wholly new governance layer from zero.
