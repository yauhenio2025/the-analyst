# Recheck: Phase 4 Bounded Governance Evaluation Scope — Post-Revision

Date: 2026-03-29
Reviewer: Claude (Opus 4.6, 1M context)
Subject: Revised `communications/MEMO_2026-03-28_phase4_bounded_governance_evaluation_scope.md`
Prior reviews:
- `communications/REPORT_Claude_Phase4_Bounded_Governance_Evaluation_Scope_Critique_2026-03-28.md`
- `communications/REPORT_Codex_Phase4_Bounded_Governance_Evaluation_Scope_Audit_2026-03-28.md`

---

## Verdict

**Approve. The revision resolves all required corrections from both review threads.** The scope is now ready for implementation planning.

---

## Review thread resolution

### Claude review — required revisions

| # | Finding | Status |
|---|---------|--------|
| 4.1 | Name evidence surfaces per case | **RESOLVED** — Lines 102-110 make the AOI/genealogy asymmetry explicit. Lines 178-203 detail per-case evidence sources. The AOI case now names executor DB, typed result/readiness/manifest truth, and carried-forward Stage 5 artifacts. The genealogy case now names compose-session store, planning snapshot, and lifecycle closeout artifacts. |
| 4.2 | Add executor database to primary code surfaces | **RESOLVED** — Lines 77-80 add `src/executor/db.py`, `src/executor/executor.db`, `src/api/routes/executor.py` to the "what already exists" section. Lines 292-294 add them to the scrutiny list. |
| 4.3 | Require explicit evidence manifest in pack | **RESOLVED at scope level** — The pack is now modeled as "composite evidence packs" (line 208) with required supporting evidence references per case. Implementation details appropriately deferred to the implementation plan. |
| 4.4 | Authorize case-specific evidence access in rubric | **RESOLVED** — Lines 246-253 explicitly list which API routes/DB reads the harness should use, including "executor DB/API reads for the AOI exemplar case where no planning/session store object exists." |
| 4.5 | Report should embed vs reference evidence | **RESOLVED** — Lines 168-170 choose the reference-with-citation approach: "thin verdict layer...should summarize and cite the evidence...should not duplicate full manifests, full traces, full session payloads, or full proof bundles." |

### Codex review — scope corrections

| # | Finding | Status |
|---|---------|--------|
| 1 | Existing inspection surfaces understated | **RESOLVED** — Lines 71-76 now list `result_contract.py`, `source_backed_readiness.py`, and the routes that expose them. Lines 246-253 require the harness to reuse these seams. The memo no longer reads as if nothing inspectable exists. |
| 2 | AOI pack too narrow if modeled as just one job ID | **RESOLVED** — Lines 183-190 now define the AOI pack as composite: primary subject `job-744edf255ad5` plus executor-database truth, typed result/readiness/manifest truth, March 27 closeout artifacts, AND the carried-forward Stage 5 AOI rubric and eval-summary artifact family. |
| 3 | Genealogy pack must be session-centric | **RESOLVED** — Line 195 uses `session_id = compose-session-0877864dcca7` as primary subject. Line 203 explicitly states "planning_decision_id is provenance for this case, not lifecycle identity." |
| 4 | Retrospective frozen-evidence semantics | **RESOLVED** — Lines 155-157 add `evidence_mode`, `evidence_observed_at`, `live_revalidation_performed` as required report properties. Lines 231-237 require reports to be labeled as retrospective frozen-evidence verdicts, not misrepresented as fresh live reruns. |
| 5 | Overstated absence of normalized verdicts | **RESOLVED** — The revised memo identifies the gap precisely: no cross-case evaluation-report object, no frozen evaluation-pack contract, no harness, no report retrieval seam. It no longer overstates as "nothing normalized exists at all." |
| 6 | Thin verdict layer over existing substrate | **RESOLVED** — Lines 129, 163-170 frame the report as extending the existing results/readiness/manifest/trace/planning-decision/compose-session substrate. The "must not widen" section (line 278) adds an explicit guard against silently inventing a fake normalization layer. |

---

## New issues introduced by revision

**None found.** The revision adds clarity without introducing new contradictions or scope creep.

---

## Spot-check: codebase truth still consistent

Verified that the codebase state matches the revised memo's claims:

| Claim | Verified |
|-------|----------|
| `src/analysis_products/result_contract.py` exists | Yes |
| `src/analysis_products/source_backed_readiness.py` exists | Yes |
| `/v1/results/by-job/{job_id}/source-backed-readiness` route exists | Yes — `src/api/routes/results.py:100` |
| AOI job `job-744edf255ad5` exists in executor DB with status=completed | Yes — confirmed via SQLite query |
| AOI job has 36 phase outputs and presentation_runs status=completed | Yes |
| No `PersistedTaskPlanningDecision` exists for AOI job | Yes — no match in `src/orchestrator/planning_decisions/` |
| No `PersistedComposeSession` exists for AOI job | Yes — no match in `src/presenter/compose_sessions/` |
| Genealogy compose session `compose-session-0877864dcca7.json` exists in store | Yes — 27KB file with all expected fields |
| Stage 5 AOI rubric and eval-summary artifacts exist in communications/ | Yes — `MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`, `PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json` |
| Phase 0 AOI closeout artifacts exist (15 files) | Yes |
| Phase 3 lifecycle closeout artifacts exist (7 files) | Yes |

---

## One observation for the implementation plan

The harness will operate in two evidence modes simultaneously:

1. **Live reads from existing API seams** — querying `/v1/results/by-job/...`, `/v1/presenter/compose-sessions/...`, etc. These reflect current store state at report-generation time.
2. **File reads from frozen communications proof artifacts** — HAR files, JSON dumps, PNGs captured during the original proof sessions. These are immutable.

The `evidence_observed_at` field captures when the harness ran. The `evidence_mode` field should distinguish whether a given check derived its truth from a live API read or a frozen artifact read. The implementation plan should make this per-check, not just per-report, since a single report will mix both modes.

This is not a scope problem — it's a design detail for the implementation plan to resolve.

---

## Summary

The revised scope is clean, honest, and implementation-ready. All major concerns from both review threads are addressed. The evidence asymmetry is named. The executor database is in the surfaces list. The packs are composite. The genealogy case is session-centric. Retrospective semantics are required fields. The anti-widening guards are comprehensive.

Ready for implementation planning.
