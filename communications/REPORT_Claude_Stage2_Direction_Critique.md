# REPORT: Stage 2 Direction Critique

Date: 2026-03-16
Evaluating: `MEMO_2026-03-16_context_wrapup_after_stage1_and_stage2_recommendation.md`

---

## 1. Verdict

The memo's reconstruction of the 72-hour arc is accurate. Its diagnosis that the analysis-product layer is the correct architectural center is correct. Its claim that Stage 1 landed real code is verified — roughly 1,000 lines of production implementation across schemas, store, result contract, database tables, API routes, and test coverage.

**But the memo significantly overstates the weight of what was accomplished and proposes the wrong ordering for Stage 2.**

The analysis-product layer as built is an **additive, non-fatal, silently-degradable bolt-on**. Every integration point — corpus registration, AOI artifact writes, genealogy artifact writes, result manifest assembly — is wrapped in `try/except` with warning-level logging. The system operates identically if the entire layer fails. This is architecturally correct for a Stage 1 landing. But it means the layer is not yet load-bearing and cannot yet serve as the foundation the memo claims.

The proposed Stage 2 ordering — harden, then deepen genealogy, then expand the result contract — has the second and third items backwards. The result-contract expansion is prerequisite to genealogy deepening, not a follow-on.

And the memo underestimates the single hardest problem in Stage 2: The Critic still owns an enormous lifecycle surface that the memo's "bounded switchover" language obscures.

---

## 2. What The Memo Gets Right

### The 72-hour narrative is accurate

The progression from AOI proving ground → canary → shared-substrate → analysis-product layer correction is faithfully reconstructed. The predecessor memos confirm each inflection point:

- The March 14 memo correctly scoped AOI as a bounded non-genealogy test
- The March 15 status memo correctly identified that the canary exposed an upstream activation gap, not a consumer-shell gap
- The March 16 program-basis memo correctly diagnosed the missing layer as product identity above execution
- The Stage 1 completion memo correctly described what was built

### Stage 1 is real code, not stubs

Verified against the live repo:

- `src/analysis_products/store.py` (766 lines): 19 production functions including deterministic corpus registration, artifact upsert, artifact-first reads, and manifest summarization
- `src/analysis_products/schemas.py` (62 lines): 4 Pydantic models defining the result contract
- `src/analysis_products/result_contract.py` (177 lines): manifest assembly and presentation refresh
- `src/api/routes/results.py` (51 lines): 2 consumer-facing endpoints, registered in main.py
- Database schema in `src/executor/db.py`: `analysis_corpora` and `analysis_artifacts` tables with full Postgres+SQLite dual-backend support
- `tests/test_analysis_product_contract.py` (296 lines): 5 tests covering determinism, idempotence, round-trip, and manifest freshness

There are zero TODO/FIXME markers. This is production-grade implementation.

### The diagnosis about The Critic as displaced product boundary is correct

The memo is right that The Critic carries too much product-boundary logic and that this should move upstream. This is not in dispute.

### The deferrals are correct

Deferring SDK extraction, analyzer-mgmt packaging elevation, and generated bespoke app work is the right call. None of those become real until the product layer is load-bearing.

---

## 3. Where The Memo Overstates Or Misorders Things

### Overstatement 1: "First real product boundary" is too strong

The memo says Stage 1 "proved a narrow version of [the analysis-product layer] can live inside analyzer-v2." What it actually proved is that a non-fatal, silently-degradable secondary index can be written alongside the existing execution path.

Evidence:

- **Every integration point is non-fatal.** Corpus registration at `pipeline.py:388`, `pipeline.py:422`, and `executor.py:152` is wrapped in try/except with warning logs. AOI artifact writes at `chain_runner.py:428` and `:558` are wrapped in try/except. Genealogy artifact writes at `presentation_api.py:1959` are wrapped in try/except. Materialization at `workflow_runner.py:713` and `preparation_coordinator.py:161` are wrapped in try/except.

- **No execution path depends on analysis_products.** If the entire module is removed, execution proceeds identically. The only consumer-facing change would be the loss of two API endpoints (`/v1/results/by-job/{job_id}` and its refresh variant).

- **The artifact-first read in `aoi/contract.py:132-151` has a full fallback.** It tries the artifact store, then falls back to `phase_outputs`. The fallback is the real path.

This is not a criticism of the implementation. Non-fatal bolt-on is the correct Stage 1 pattern. But the memo's language — "first real product-facing contract," "first live proof that product-boundary responsibilities can move upstream" — implies load-bearing infrastructure. The infrastructure is not yet load-bearing.

### Overstatement 2: "Bounded Critic switchover" obscures how little actually moved

The memo claims The Critic now uses the new contract on "one live path" where:
- snapshot remains the restore-content source
- analyzer-v2 manifest is authoritative for freshness
- analyzer-v2 refresh is authoritative for presentation refresh

I verified this. `GenealogyPage.tsx:549-583` does call `/v1/results/by-job/{v2JobId}` for freshness checking and calls `refresh-presentation` when stale. That code is real.

**But The Critic still owns all of the following, none of which the memo acknowledges:**

| Lifecycle responsibility | Location | Description |
|---|---|---|
| Job polling threads | `server.py:17893-17951` | 5-second polling loop with rescue-timeout logic |
| Failure auto-retry | `server.py:18042-18113` | Detects transient errors, re-submits entire analysis |
| Snapshot persistence | `server.py:18022-18038` | Persists PagePresentation to own DB |
| Resume orchestration | `server.py:18936-19030` | Calls v2 resume, then spawns new polling thread |
| Recovery orchestration | `server.py:18838-18933` | Manual recovery with v2 status fetch and local state update |
| Version polling | `analyzer_v2_client.py:905-938` | 5-minute daemon thread for definition cache invalidation |
| AOI document loading | `server.py:17510-17650` | Loads subject and source corpora from disk |
| AOI request routing | `server.py:17692-17706` | Validates and routes AOI-specific parameters |
| Result interpretation | `server.py:18210` | Extracts thinker identity from PagePresentation |

The "bounded switchover" moved **freshness checking and presentation refresh** for genealogy. It did not move polling, recovery, retry, persistence, document loading, or request routing. Calling this "the first live proof that product-boundary responsibilities can move upstream" overstates what happened. It is more accurately described as: The Critic now checks freshness against a new endpoint before deciding whether to re-fetch.

### Overstatement 3: Genealogy seam maturity

The memo correctly notes that the genealogy seam is "presenter-derived." But it doesn't sufficiently emphasize how indirect that derivation is.

`materialize_stage1_artifacts()` at `presentation_api.py:1991-2007` only runs for `intellectual_genealogy` workflows. It calls `_load_per_item_data()`, which triggers relationship extraction and normalization as a side effect, which in turn calls `store_relationship_classification_artifact()` at `presentation_api.py:1959-1974`.

This means genealogy artifacts are only written **during presentation preparation, not during execution.** If presentation is never prepared (e.g., the job is only polled for status), no genealogy artifacts exist. The artifact layer for genealogy is a side effect of an already-optional presenter path.

### Misordering: Result contract expansion should precede genealogy deepening

The memo proposes:
1. Harden Stage 1
2. Deepen genealogy
3. Expand result contract
4. Keep deferrals

The second and third items should be swapped. Here's why:

**Genealogy deepening means moving artifact writes from the presenter path into the execution path.** But the execution path doesn't yet need to know about artifacts — it works fine with `phase_outputs`. The only reason to move genealogy artifact writes earlier is if something downstream needs them. That "something downstream" is the result contract. Until the result contract is rich enough that consumers actually depend on artifact state for real decisions (not just freshness checks), there is no consumer pull for execution-boundary genealogy artifacts.

Concretely: The Critic's genealogy page currently works by fetching PagePresentation. It does not read individual artifacts. It does not query artifact families. It does not use dependency state. Moving genealogy artifacts upstream does nothing for any real consumer until the result contract tells consumers "here are your artifacts, here is their state."

Therefore: expand the result contract first. That creates the consumer surface that actually demands artifact-boundary moves. Then deepen genealogy because a consumer exists that will use the deeper seam.

---

## 4. Whether Stage 2 As Proposed Is The Right Next Move

**Partially.** The diagnosis is correct: Stage 2 should stay in analyzer-v2 and should continue building the product layer. The deferrals are correct.

But the internal ordering is wrong, and there is one missing prerequisite.

### Missing prerequisite: Make the non-fatal layer observable before hardening it

The memo says "harden Stage 1 in real use" and lists monitoring corpus_ref fill rates, artifact creation rates, staleness behavior, and null-corpus degradation.

There is currently **no way to monitor these things** without querying the SQLite database directly.

- There is no `/v1/analysis-products/health` endpoint
- There is no logging that tracks artifact write success rates per job
- There is no admin surface in analyzer-mgmt that shows corpus or artifact state (analyzer-mgmt's job page shows `artifacts_ready` as a badge, but that's a boolean from the presenter status, not from the analysis_products layer)
- The `try/except` wrappers emit `logger.warning()` messages, but no structured metrics

Hardening an invisible layer is not possible. The first Stage 2 work item should be **observability**, not just "monitoring" — actual endpoints and logging that make the layer's health visible without SSH access to the database.

### Corrected ordering

1. **Observability first** — make the analysis-product layer visible (health endpoints, structured logging, analyzer-mgmt surface)
2. **Expand result contract** — make the contract rich enough that consumers have reason to depend on artifact state for more than freshness
3. **Genealogy execution-boundary move** — once consumers depend on the contract, move genealogy artifacts from presenter-derived to execution-derived
4. **Continue deferrals** — SDK, packaging, generated apps remain later

---

## 5. What Should Change Before Planning

### A. Acknowledge the actual integration topology

The Stage 2 plan must explicitly state that the analysis-products layer is currently non-fatal/optional and that making it load-bearing is the goal of Stage 2, not an already-achieved property from Stage 1.

### B. Size The Critic lifecycle displacement honestly

The memo treats The Critic's remaining lifecycle as small and bounded. It is not. The polling, retry, recovery, persistence, and document-loading responsibilities listed in Section 3 above represent thousands of lines of orchestration code. The Stage 2 plan should identify exactly which of these responsibilities it intends to move, and in what order. A blanket "expand the result contract so more of The Critic can be deleted" is too vague for an implementation plan.

Specific candidates for Stage 2 migration, in order of feasibility:

1. **Freshness and refresh** (already partially done — extend to AOI, not just genealogy)
2. **Result manifest as the canonical restore source** (replace snapshot persistence with manifest-based restore)
3. **Job status polling consolidation** (server-sent events or webhook from analyzer-v2 instead of Critic polling threads)

These are concrete. "More restore truth" and "less consumer-local lifecycle assembly" are not.

### C. Decide whether analyzer-mgmt integration is truly deferred

Analyzer-mgmt already shows `artifacts_ready` on the job inspection page (`pages/jobs/[id].tsx:232,301,502`). It has a `refreshArtifacts()` mutation. But it does not call any `/v1/results/` endpoints and does not display artifact families.

This is a half-integrated surface that will drift further from the actual analysis-products layer if ignored. The Stage 2 plan should either:

- Explicitly include a bounded analyzer-mgmt integration (adding result manifest display to the job page)
- Or explicitly document that the existing partial integration will be removed/frozen until Stage 3

Leaving it ambiguously deferred creates a governance gap.

### D. Specify what "deepen genealogy" actually means in code

The memo says Stage 2 should "deepen genealogy beyond the current presenter-derived seam." That is a design-level statement, not an implementation directive.

In code terms, this means one of:

1. **Move artifact writes into `chain_runner.py`** for the genealogy relationship classification chain, similar to how AOI artifact writes already happen at `chain_runner.py:428`. This requires the chain runner to know about genealogy artifact families, which it currently does not.

2. **Add new genealogy artifact families** beyond `relationship_classification` — e.g., `genealogy.target_profile`, `genealogy.concept_constellation`. This requires defining new families, new write seams, and new schema payloads.

3. **Both.**

The Stage 2 plan must pick one. The memo's current language is too abstract to plan against.

---

## 6. Recommended Corrected Direction

### Keep from the memo

- Stage 2 stays in analyzer-v2
- Stage 2 continues building the product layer
- SDK extraction, packaging, generated apps remain deferred
- No more broad strategy memos — the diagnosis is stable

### Change the ordering to

**Stage 2a: Make the layer observable and trustworthy (1-2 days)**

- Add `/v1/analysis-products/health` endpoint showing corpus count, artifact counts by family, recent write success/failure rates
- Add structured log events for corpus registration and artifact writes (not just warning on failure)
- Add one analyzer-mgmt integration: display artifact family state on the job page by calling `/v1/results/by-job/{jobId}`
- Run 3-5 real jobs and verify artifact fill rates

**Stage 2b: Expand result contract to cover AOI and widen The Critic's dependence (2-3 days)**

- Extend the result manifest to cover AOI workflows (currently it's primarily tested against genealogy)
- Add `restore` semantics to the manifest so The Critic can use it as the canonical restore source instead of local snapshots
- Wire The Critic's AOI path to use the result manifest for freshness (parallel to the existing genealogy freshness path)
- Identify and list the 3-5 specific Critic lifecycle responsibilities that Stage 2b removes or reduces

**Stage 2c: Move genealogy artifacts to execution boundary (2-3 days)**

- Add genealogy relationship artifact writes to `chain_runner.py`, parallel to the existing AOI writes
- Remove or demote the presenter-derived write path in `presentation_api.py:1959` to fallback
- Verify that genealogy artifact-first reads work from the execution-written artifacts
- This is now justified because Stage 2b created consumers that depend on execution-time artifacts

**Stage 2d: Evaluate whether to proceed to Stage 3 or iterate (0.5 days)**

- Assess whether the result contract is rich enough for a second consumer (not The Critic) to use
- Assess whether genealogy's execution-boundary artifacts are stable enough to add a second family
- Decide whether Stage 3 should be SDK/packaging or more product-layer depth

### What this changes vs the memo

1. Observability moves from implicit to the first work item
2. Result contract expansion moves before genealogy deepening
3. Genealogy deepening becomes concrete (execution-boundary writes in chain_runner)
4. Analyzer-mgmt gets a bounded integration instead of full deferral
5. The Critic lifecycle migration gets specific targets instead of vague language

The memo's diagnosis is correct. Its ordering is wrong. The corrected direction keeps the same destination but sequences the work so that each step creates a real consumer need for the next.
