# Architecture Review: Round 13 / AOI Source-Backed Transient Launch Scope

**Reviewer**: Claude Opus 4.6
**Date**: 2026-03-22
**Memo under review**: `communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md`
**Review pass**: 2 (post-revision)

---

## Verdict: Approve

The revised memo resolves the primary weakness identified in pass 1. The two-step bridge architecture — the-critic resolves saved-result identity, analyzer-v2 owns source-result-to-compose mapping by `v2_job_id` — is the right structural split. The explicit choice of normalized AOI artifacts and phase-output metadata as the source contract (rather than saved `PagePresentation.raw_prose`) is architecturally sound and grounded in code that already exists.

Two minor items remain for the execution plan to address, but neither blocks scope approval.

---

## What Changed Between Pass 1 and Pass 2

The memo was revised structurally. The key corrections:

1. **Two-step bridge architecture**: the-critic resolves which saved AOI result / `v2_job_id` to use. analyzer-v2 reconstructs compose-ready sections from its own durable artifacts and phase outputs. This eliminates the underspecified "derive a bounded compose request" black box.

2. **Explicit rejection of raw_prose path**: Line 238: "do not treat saved `PagePresentation` `raw_prose` as the primary source contract." This addresses the primary weakness from pass 1.

3. **Analyzer-owned source mapping route**: A new bounded analyzer-v2 route keyed by `source_job_id` + `profile` that owns the actual section reconstruction. This keeps analytical intelligence in analyzer-v2.

4. **Result resolution rule**: Lines 184-187 specify newest completed/restorable with optional explicit override.

5. **Tight no-fallback doctrine**: Line 294: "do not silently fall back from analyzer-owned source reconstruction to saved presentation `raw_prose`."

---

## Assessment Against The Six Review Questions

### 1. Is "source-backed transient launch" really the next contradiction?

**Yes.** Unchanged from pass 1. After rounds 11 and 12, the transient shell and compose-from-intent route are both real. The proof host still depends on hardcoded payloads from `composeFromIntentExamples.ts` (`/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentExamples.ts`). Source-backed launch is the smallest honest step toward a real user path.

No more urgent seam exists. Persistence before source-backed launch is still upside down.

### 2. Is the proposed consumer-side proxy / bridge the right boundary?

**Yes.** The revised memo improves this from pass 1 by splitting the bridge into two clearly separated responsibilities:

- **the-critic**: resolve saved result identity where it already lives. Accept project + thinker context. Find the newest completed result. Extract `v2_job_id`. Forward to analyzer-v2.
- **analyzer-v2**: own the actual source-to-compose mapping. Load normalized artifacts and phase outputs by `v2_job_id`. Reconstruct sections. Call compose-from-intent internally.

This split is well-grounded. The source-mapping intelligence stays in analyzer-v2, where:
- `load_aoi_normalized_artifact(job_id, engine_key)` already exists (`src/analysis_products/store.py:725-733`)
- `AOI_ARTIFACT_FAMILY_BY_ENGINE` already maps `aoi_thematic_synthesis` → `aoi.source_thematic_map`, `aoi_engagement_mapping` → `aoi.engagement_map`, `aoi_sin_findings` → `aoi.findings_bank` (store.py:24-28)
- Phase-output metadata is already loadable by job_id + phase_number

The consumer stays thin — it's plumbing (result identity → upstream handle), not brain.

### 3. Are the memo's assumptions about saved AOI source material supported by the code?

**Yes, with one nuance the execution plan must address.**

The three first-class AOI normalized artifacts are real and loadable:
- `aoi_thematic_synthesis` → `aoi.source_thematic_map` artifact family
- `aoi_engagement_mapping` → `aoi.engagement_map` artifact family
- `aoi_sin_findings` → `aoi.findings_bank` artifact family

These are persisted via `record_aoi_artifact_from_metadata()` (store.py:648-685) during AOI execution and loaded via `load_aoi_normalized_artifact()` (store.py:725-733).

**The nuance**: `aoi_thematic_report` is NOT in `AOI_ARTIFACT_FAMILY_BY_ENGINE` (store.py:24-28). It does not have a first-class normalized artifact. The memo acknowledges this with the language "thematic report normalized/metadata-backed output" (lines 229, 234). The execution plan will need to resolve the thematic report from phase outputs or output metadata rather than from the artifact store. This is feasible — phase outputs are durable and loadable by `job_id` — but it's a different code path than the other three engines.

This is not a scope blocker. It's an implementation detail the execution plan should name explicitly.

### 4. Does the memo stay honest about what remains blocked?

**Yes.** The not-in-scope list (lines 312-328) is comprehensive. The failure doctrine (lines 272-294) is now explicit about:
- No silent fallback to hardcoded examples
- No silent fallback from analyzer-owned source reconstruction to saved presentation `raw_prose`
- Honest 409 when the upstream job cannot satisfy the requested profile

The decision rule (lines 397-412) is realistic and properly bounded.

### 5. Does the proposal fit the larger platform direction?

**Yes.** Unchanged from pass 1. The revised split actually strengthens the platform alignment:

- The-critic stays thinner (resolves identity, proxies request)
- Analyzer-v2 gains a new source-backed composition capability that could later serve other consumers
- The compose-from-intent route is reused internally, not duplicated
- No re-thickening risk in either repo

The one long-term architectural concern: the per-profile section mapping in analyzer-v2 is hardcoded to two profiles for this bounded round. If future rounds add more profiles, this should evolve into a profile registry rather than growing as conditional branches. But for two profiles in a bounded round, hardcoding is the right call.

### 6. Are there missing failure modes, lifecycle concerns, or proof-standard requirements?

Two minor items remain:

**a. Multiple saved results for the same thinker/project.** The memo now specifies "default newest completed/restorable" (line 186) with optional override (line 187). This is sufficient for the bounded round. The execution plan should confirm that the-critic's saved-result list endpoint supports the necessary filtering and ordering.

**b. Proof evidence for the source-data intermediate.** The proof standard (lines 342-351) now includes the resolved upstream `v2_job_id`. Good. It would be even stronger to include the reconstructed sections (engine_key + prose) that were fed to compose-from-intent, so any mismatch between source material and final output is auditable. This is a proof-discipline recommendation, not a scope blocker.

---

## Pass 1 Revisions: Disposition

| Pass 1 Revision | Status | Notes |
|------------------|--------|-------|
| Revision 1 (Critical): Specify source data path | **Resolved** | Memo now explicitly chooses analyzer-side normalized artifacts + phase-output metadata. Rejects raw_prose from saved presentations. |
| Revision 2 (Important): Specify result resolution rule | **Resolved** | Lines 184-187: newest completed/restorable with optional explicit override. |
| Revision 3 (Important): Add diagnostic requirement | **Substantially resolved** | The failure doctrine (lines 272-294) covers this. The analyzer-owned route will know whether artifacts exist for the requested profile. No separate diagnostic needed beyond what the route itself reports. |
| Revision 4 (Minor): Clarify ViewRenderer constraint | **Unchanged** | Still implicit. Not material. |

---

## Items for the Execution Plan (Not Scope Blockers)

1. **`aoi_thematic_report` source path**: Not a first-class artifact. The execution plan must specify which phase-output or metadata path provides the thematic report prose for compose-from-intent sections. Phase outputs are durable and loadable — this is a code-path decision, not a design gap.

2. **Proof evidence granularity**: Consider saving the reconstructed compose sections (engine_key + extracted prose) alongside the compose-from-intent request/response, for auditability of the source-to-compose mapping.

---

## Items Inspected

### Code seams (materially relevant)

- `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py` — compose-from-intent orchestration, request validation, engine key validation against registry + capability definitions
- `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py` — `ComposeFromIntentRequest`, `TransientIntentPagePresentation`, `ComposeFromIntentResponse`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py` — `AOI_ARTIFACT_FAMILY_BY_ENGINE`, `load_aoi_normalized_artifact()`, `record_aoi_artifact_from_metadata()`
- `/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py` — `get_result_presentation()`, `assemble_page(read_only=True)` (no slim=True, so raw_prose is populated — but the memo correctly rejects this path anyway)
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx` — thinker-scoped result discovery, `loadLocalSnapshot`, `matchesThinker` filtering
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts` — typed fetch to analyzer-v2 compose-from-intent
- `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentExamples.ts` — hardcoded proof payloads (the thing round 13 replaces)
- `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts` — V2 result types, discovery summaries, restore logic
- `/home/evgeny/projects/the-critic/api/server.py` — `_save_v2_presentation_to_db`, `_build_v2_presentation_record`, result detail endpoint, `get_result_presentation_sync`
- `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_client.py` — `get_result_presentation_sync()` → `GET /v1/results/by-job/{job_id}/presentation`

### Reference documents (inspected)

- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md` — roadmap sequencing, post-round-8 direction
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md` — platform thesis, gap analysis, priority ordering
- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md` — compose-from-intent route, transient contract, engine fallback
- `communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md` — consumer proof host, browser proof artifacts
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md` — AOI v2 hot-path cutover, thinker identity propagation
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md` — deployment order, migration validation

### Items NOT materially relevant

- `/home/evgeny/projects/the-critic/docs/` — CURRENT-TASKS.md (empty), architecture docs focused on genealogy. Nothing bearing on this scope decision beyond the Stage 9 runbook.
- `/home/evgeny/projects/analyzer-v2/docs/` — CURRENT-TASKS.md and architecture docs focused on pipeline data flow. Already covered by the vision doc.

---

## Summary

| Question | Answer |
|----------|--------|
| Right next contradiction? | Yes |
| Right boundary for bridge? | Yes — improved with two-step split |
| Source material assumptions supported? | Yes — normalized artifacts for 3/4 engines, phase-output path for thematic report |
| Honest about blocked items? | Yes |
| Fits platform direction? | Yes, no re-thickening risk |
| Missing failure modes? | None blocking — 2 minor items for execution plan |
| Verdict | **Approve** |
