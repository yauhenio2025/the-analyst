# REPORT: Stage 3 Direction Critique

Date: 2026-03-16
Evaluating: `MEMO_2026-03-16_stage3_direction_after_stage2_completion.md`

---

## 1. Verdict

The memo's proposed direction is correct. Lifecycle authority and consumer simplification is the right Stage 3 agenda. The ordering of 3A/3B/3C/3D is also correct in principle. The deferrals (SDK extraction, analyzer-mgmt packaging elevation, generated bespoke apps) are well-justified.

**But the memo has three structural problems that would cause planning failure if left uncorrected:**

1. It still understates the volume and coupling of lifecycle logic in The Critic, which means Stage 3C is larger than the memo implies and contains hidden prerequisites the memo does not name.
2. It treats 3B (result-contract expansion) and 3C (Critic lifecycle displacement) as sequential phases, when they are actually one iterative cycle: each contract expansion enables a specific deletion, and each deletion reveals the next required contract expansion.
3. It does not identify the specific mechanism gap that blocks the most impactful Critic deletions: analyzer-v2 has no job lifecycle event system (no webhooks, no SSE, no push notifications), which means Critic polling threads (~300 LOC of complex state-machine orchestration) cannot be replaced at all, only supplemented.

The memo's arc reconstruction is accurate, its strategic diagnosis is sound, and its instinct to prioritize lifecycle authority over more artifact families is supported by evidence. What it needs is honest sizing, mechanism specificity, and a merged 3B/3C structure.

---

## 2. What The Memo Gets Right

### The March 14-16 arc reconstruction is accurate

I verified the claimed progression against the predecessor memos:

- March 14: AOI as bounded non-genealogy test (`MEMO_2026-03-14_aoi_thematic_port_preplan.md`)
- March 15: AOI canary proved semantic ownership + thin-consumer viability (`MEMO_2026-03-15_next_program_after_aoi_canary.md`)
- March 16 morning: shared-substrate framing corrected to analysis-product layer (`MEMO_2026-03-16_analysis_product_layer_program_basis_after_stage0_reports.md`)
- Stage 1: narrow product layer landed (corpus identity, AOI artifacts, one genealogy seam, first result contract)
- Stage 2: result boundary hardened and extended to three consumer surfaces

Each inflection point is supported by the memo it cites. The narrative is not revisionist.

### Stage 2 did change what the highest-leverage next work is

This is the memo's most important claim, and the code supports it.

Before Stage 2, the system had:
- A non-fatal analysis-product layer that could silently fail
- One consumer surface (genealogy) using the result contract
- Plan-file dependency in the refresh path
- No content_hash persistence in output writes
- Sync/background preparation asymmetry

After Stage 2 (verified against live code):
- `result_contract.py` (359 lines): sophisticated freshness hashing with 6-condition staleness detection, 3-condition product warnings, and explicit result state FSM (`ready` / `stale` / `preparing` / `failed` / `legacy_untracked`)
- `plan_context.py` (67 lines): effective plan fallback system that resolves from `plan_data` first, file-backed plan second, explicit missing state last
- `output_store.py`: content_hash now persisted via SHA256 (line 220)
- Three consumer surfaces now use the result contract: genealogy, AOI v2 thematic, generic analysis workspace
- Genealogy relationship classification materialized at execution-adjacent seam (post phase 1.5), not only at presenter-time

This means adding another genealogy artifact family would not reduce any consumer lifecycle code. But expanding the result contract *would* enable specific Critic deletions. The memo's strategic reasoning is correct: lifecycle authority is now higher leverage than artifact breadth.

### The deferrals are correct and well-grounded

SDK extraction requires a stable product contract to extract against. analyzer-mgmt packaging requires the product layer to be load-bearing. Generated bespoke apps require both. None of these are ready. The code confirms this:

- analyzer-mgmt has zero awareness of the analysis-product layer (no `/v1/results/*` calls, no artifact types, no results router in the backend)
- The result contract, while mature in implementation, is still consumed by only one project (The Critic) and only for freshness/refresh
- No SDK boundary has been designed, let alone extracted

Deferring these is not timidity. It is accurate dependency ordering.

### Stage 3A (observability first) is the correct starting position

There is currently **no way** to inspect the analysis-product layer without database queries:

- No `/v1/admin/artifacts` or health endpoint
- No structured metrics for corpus registration or artifact write rates
- No analyzer-mgmt surface for artifact family state
- The `/health` endpoint (`main.py:320-359`) reports definition registry counts only

The memo is right: a boundary you cannot observe is a boundary you cannot trust, debug, or progressively load.

---

## 3. What It Still Overstates Or Misorders

### Overstatement 1: "bounded consumer switchover on all three v2 surfaces" masks how thin the switchover is

The memo claims The Critic now uses analyzer-v2 as the primary lifecycle contract on genealogy, AOI v2 thematic, and generic analysis workspace. I verified the frontend code:

- `GenealogyPage.tsx`: calls `/v1/results/by-job/{v2JobId}` for freshness, calls `refresh-presentation` when stale. **Real switchover.**
- `AoiV2ThematicPanel.tsx`: uses presenter status + Critic refresh proxy. **Not switched over to result contract.**
- `AnalysisWorkspacePage.tsx`: uses presenter status + Critic refresh proxy. **Not switched over to result contract.**

What actually happened: the Stage 2 completion memo (`MEMO_2026-03-16_stage2_result_boundary_completion.md`) claims the switchover reached all three surfaces. But the code shows only genealogy is wired to the `/v1/results/*` endpoints. AOI and generic workspace still go through the presenter status path and Critic-local refresh. This is the same pattern the Codex Stage 2 audit flagged at `AoiV2ThematicPanel.tsx:205` and `AnalysisWorkspacePage.tsx:292`.

**Impact on Stage 3 planning**: Stage 3C (broader Critic lifecycle displacement) is larger than it appears because the "bounded switchover" on two of three surfaces has not actually happened yet. The Stage 3 plan must include completing the AOI and workspace switchover as prerequisite work, not as already-done baseline.

### Overstatement 2: The memo lists Critic lifecycle responsibilities without sizing them

The memo names: "polling threads, retry and recovery orchestration, resume flows, import behavior, snapshot persistence, some restore authority, AOI request/document handling."

That reads like a checklist. Here is what it actually represents, verified against `server.py` and `analyzer_v2_client.py`:

| Component | Location | LOC | Complexity |
|-----------|----------|-----|------------|
| Polling/status threads | `server.py:17893-19031` | ~300 | Complex state machine: exponential backoff (10s→120s), rescue polling with 90s timeout, per-job cancellation flags, daemon thread lifecycle |
| Retry/recovery | `server.py:18042-18113, 18838-18933` | ~200 | Transient error detection, full re-submission, consecutive error tracking (max 5) |
| Resume orchestration | `server.py:18936-19112` | ~180 | State validation, v2 resume API call, background poll thread spawning |
| Import pipeline | `server.py:19126-19387` | ~260 | Three-stage: metadata check (60s timeout) → presentation assembly (1800s timeout for compose) → DB persistence to `genealogy_analyses` table |
| Snapshot persistence | `server.py:18220-18404` | ~180 | `_save_v2_presentation_to_db`, `_update_v2_presentation_in_db`, `_build_v2_presentation_record` |
| Refresh proxying | `server.py:19389-19463` | ~75 | Fetches page, updates in-memory cache + DB |
| AOI document loading | `server.py:17510-17650` | ~60 | Loads from Critic's `ProjectDocumentDB`, filters by doc_type |
| v2 client lifecycle | `analyzer_v2_client.py:574-968` | ~470 | start_analysis, poll_analysis, resume, fetch_page, version polling daemon |
| Frontend lifecycle | `GenealogyPage.tsx`, `AoiV2ThematicPanel.tsx` | ~300 | Polling, freshness checking, refresh orchestration |

**Total: ~2,025 lines of lifecycle code across backend, client, and frontend.**

The memo treats this as a bounded migration target. It is closer to a medium-sized subsystem rewrite. Stage 3C should not be planned as "broader displacement" — it should be planned as an enumerated sequence of specific deletions, each paired with a specific contract expansion.

### Misordering: 3B and 3C are not sequential; they are iterative

The memo proposes:
- 3B: result-contract and lifecycle expansion
- 3C: broader Critic lifecycle displacement

This implies: expand the contract first, then delete Critic code. In practice, these must interleave:

1. Expand contract to cover AOI/workspace freshness → delete Critic freshness proxies for those surfaces
2. Expand contract to cover restore semantics → delete Critic snapshot persistence as primary restore source
3. Expand contract to cover job status push → delete Critic polling threads (requires mechanism work — see Section 5)
4. Expand contract to cover import persistence → delete Critic import-to-local-DB pipeline

Each expansion creates exactly one deletion opportunity. Each deletion reveals the next constraint. Planning them as separate phases introduces an unnecessary serialization point.

**Recommended correction**: Merge 3B and 3C into a single iterative cycle with named expansion/deletion pairs. Each pair should be a self-contained work unit.

---

## 4. Whether Stage 3 As Proposed Is The Right Next Move

**Yes.** The direction is correct. The alternatives are all worse:

- **Another genealogy artifact seam**: Would not reduce any consumer lifecycle code. The per-work scan artifact family (`genealogy_per_work_scan`) is a reasonable future candidate, but it only matters after consumers depend on the artifact layer for more than freshness. No consumer currently does.

- **SDK extraction**: Requires a stable, load-bearing product contract to extract against. The contract is real but still only consumed for freshness/refresh on one surface (genealogy). Premature extraction would freeze an immature interface.

- **analyzer-mgmt packaging elevation**: analyzer-mgmt has zero knowledge of the analysis-product layer. Elevating it before the layer is authoritative would mean building packaging around a secondary index.

- **Generated bespoke apps**: Requires both a stable SDK and a packaging layer. Both prerequisites are missing.

- **More AOI-only work**: AOI's artifact families are already written at execution time (`chain_runner.py:428-430, 558-560`). The AOI path is further ahead than genealogy. More AOI work is not the bottleneck.

The proposed Stage 3 is the right move because it addresses the actual bottleneck: the result contract is not yet authoritative enough to displace Critic lifecycle code, and until it is, every other expansion builds on a secondary index.

---

## 5. What Must Change Before Planning

### A. Identify the mechanism gap for polling displacement

The single biggest Critic lifecycle surface is its polling thread system (~300 LOC). This code runs `while True` loops with 5-second intervals, exponential backoff, rescue polling, and per-job cancellation via `_GENEALOGY_JOB_CANCELLATION`.

**analyzer-v2 has no push mechanism.** There is no webhook endpoint, no server-sent events, no WebSocket connection, and no callback registration for job state changes. The Critic must poll because there is no alternative.

This means Stage 3C cannot remove Critic polling threads by expanding the result contract alone. It requires a new mechanism in analyzer-v2: at minimum, a job lifecycle event stream or webhook callback. The Stage 3 plan must name this as a prerequisite, estimate its scope, and sequence it correctly (it belongs in 3B, before any polling displacement in 3C).

Without this, the memo's promise of "broader lifecycle displacement" is architecturally impossible for the largest single block of Critic lifecycle code.

### B. Acknowledge the AOI/workspace switchover gap

As noted in Section 3, the switchover on AOI and generic workspace surfaces is not yet complete. The Stage 3 plan must include completing this switchover either as late Stage 3A work (alongside observability) or as the first 3B/3C iteration.

Treating the switchover as already-done baseline will cause the plan to skip prerequisite wiring work.

### C. Name the Critic's document corpus ownership as a prerequisite for AOI displacement

AOI document loading (`_load_aoi_target_documents` at `server.py:17510-17567`, `_load_aoi_prior_works` at `server.py:17588-17650`) loads from Critic's `ProjectDocumentDB`. This data is not in analyzer-v2.

If Stage 3 intends to displace AOI lifecycle logic from The Critic, it must first move corpus document ownership to analyzer-v2's document store. The memo does not mention this prerequisite. It is small (~60 LOC of loading logic) but structurally blocking: you cannot remove AOI request routing from The Critic if The Critic is still the only place that knows what documents belong to an AOI analysis.

### D. Size 3B/3C as an enumerated list, not a direction

The memo says "keep moving result truth upstream" and "good candidates include broader restore authority, parts of polling/status truth, parts of refresh/recovery orchestration."

This is too vague for a Stage 3 implementation plan. The Stage 2 direction critique made this same criticism, and it still applies.

The plan needs an enumerated list of specific contract expansions paired with specific Critic deletions, ordered by dependency. Here is a starting proposal based on code evidence:

| # | Contract Expansion | Critic Deletion Target | Prerequisite |
|---|---|---|---|
| 1 | Wire AOI + workspace to `/v1/results/*` endpoints | Remove Critic freshness proxies for AOI, workspace | Stage 3A observability done |
| 2 | Add restore semantics to result manifest | Reduce Critic snapshot persistence to cache-only (not primary restore source) | #1 complete |
| 3 | Add job lifecycle event mechanism (webhook or SSE) | Remove or simplify Critic polling threads | Design decision required |
| 4 | Add import-to-v2 result persistence | Remove Critic import-to-local-DB pipeline | #2 complete (restore from v2 must work) |
| 5 | Consolidate resume orchestration in v2 | Remove Critic resume + background poll thread spawning | #3 complete (need event push for progress) |

### E. Decide what "observability" means concretely

The memo says Stage 3A should include "explicit operator-visible result/artifact state" and "bounded analyzer-mgmt visibility." But it does not say whether this means:

- (a) New analyzer-v2 API endpoints (e.g., `/v1/admin/artifacts/health/{job_id}`, `/v1/admin/corpora`)
- (b) Structured log events (for log aggregation / alerting)
- (c) analyzer-mgmt UI integration (showing artifact state on the job page)
- (d) All three

The code evidence suggests (a) and (b) are essential, and (c) is trivially cheap once (a) exists (the analyzer-mgmt job page already renders v2 executor data; adding a result manifest tab is ~200 lines of React).

The plan should commit to (a) and (b) as mandatory, and (c) as a companion task. This is the one place where analyzer-mgmt should not be fully deferred: if you build artifact health endpoints but provide no UI to access them, you have built observability that no operator will use.

---

## 6. Recommended Corrected Direction

### Keep from the memo

- Stage 3 is "Lifecycle Authority and Consumer Simplification" — correct
- Observability first (3A) — correct
- Another artifact seam last (3D) — correct
- SDK extraction, packaging, generated apps remain deferred — correct
- `genealogy_per_work_scan` as the most plausible next bounded seam if one is needed — correct

### Change

**1. Merge 3B and 3C into one iterative cycle.**

Do not plan "expand contract, then displace lifecycle." Plan a sequence of paired expansion/deletion units, each self-contained and testable:

- **Cycle 1**: AOI + workspace freshness switchover. Expand the result contract to serve these surfaces. Delete the Critic freshness proxies for them.
- **Cycle 2**: Restore authority. Expand the result manifest to serve as the primary restore source. Reduce Critic snapshot persistence to fallback/cache.
- **Cycle 3**: Job lifecycle events. Add a push mechanism (webhook or SSE) for job state changes. Simplify or remove Critic polling threads.
- **Cycle 4**: Import persistence. Route import results through v2 result persistence. Delete Critic import-to-local-DB pipeline.

Each cycle is bounded and real. Each produces a measurable Critic deletion. The cycles can be evaluated after each one: is the next cycle still the highest-leverage work, or should we pivot to 3D (another artifact seam)?

**2. Include the mechanism prerequisite for polling displacement.**

Stage 3 cannot succeed in its lifecycle displacement goal without a job lifecycle event mechanism in analyzer-v2. The plan must name this, scope it, and sequence it. It belongs in Cycle 3.

If this is judged too large for Stage 3, then Stage 3 should explicitly acknowledge that polling threads will remain in The Critic and set a reduced ambition for lifecycle displacement. The current memo's language ("broader lifecycle displacement") implicitly promises polling displacement without addressing the mechanism gap.

**3. Include bounded analyzer-mgmt observability in 3A.**

Not packaging. Not publication. Just: show the result manifest and artifact family state on the analyzer-mgmt job detail page, using the same `/v1/results/by-job/{job_id}` endpoint that The Critic already consumes. This is ~200 lines of React and requires no analyzer-mgmt backend changes. Deferring this entirely creates a gap between building observability and making it usable by operators.

**4. Size the Critic lifecycle displacement honestly.**

The Critic carries ~2,025 lines of lifecycle code. The Stage 3 plan should state which specific lines it intends to delete or reduce, and which will remain. "Keep migration bounded and real" is the right principle, but it needs line-level specificity to become an actionable plan.

### What this changes vs. the memo

| Aspect | Memo's Position | Correction |
|--------|-----------------|------------|
| 3B/3C structure | Sequential (expand contract, then displace lifecycle) | Iterative (paired expansion/deletion cycles) |
| Polling displacement | Implicitly promised, no mechanism named | Requires explicit job lifecycle event mechanism |
| AOI/workspace switchover | Treated as Stage 2 baseline | Not yet complete; must be included in Stage 3 |
| analyzer-mgmt | Fully deferred | Bounded 3A companion (result manifest on job page) |
| Critic lifecycle sizing | Checklist of responsibilities | ~2,025 LOC across 9 components; needs enumerated deletion plan |
| Document corpus ownership | Not mentioned | AOI displacement prerequisite; Critic still owns document loading |

### Bottom line

The memo's strategic judgment is sound. Lifecycle authority is the right Stage 3 center of gravity. The ordering (observability → contract → displacement → maybe another seam) is correct in direction. The deferrals are correct and well-grounded.

What the memo still lacks is: mechanism specificity for the hardest displacement (polling), honest sizing of what displacement actually means in LOC, acknowledgment that two of three "switched-over" surfaces are not yet switched over, and a merged iterative structure for contract expansion and lifecycle deletion.

Fix those four things and the Stage 3 plan is ready to write.
