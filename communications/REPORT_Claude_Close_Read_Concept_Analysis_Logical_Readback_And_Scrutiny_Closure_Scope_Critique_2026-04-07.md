# Critique: Close Read Concept-Analysis Logical Readback And Scrutiny Closure Scope

**Reviewer**: Claude (Opus 4.6)
**Date**: 2026-04-07
**Memo Under Review**: `communications/MEMO_2026-04-07_close_read_concept_analysis_logical_readback_and_scrutiny_closure_scope.md`
**Verdict**: **Approve with corrections**

---

## What the Memo Gets Right

### 1. The asymmetry diagnosis is honest and correctly bounded

The memo correctly identifies that:

- fresh inferential is closed end to end (confirmed by the completion predecessor)
- fresh logical execution completes but readback does not close
- the remaining gap is narrower than "logical execution is broken"

This is verified against the code. Both `inferential` and `logical` go through the same `_run_rebased_concept_analysis()` entry point (`server.py:3963`), the same `_save_concept_analysis_to_db()` persistence path (`server.py:3842`), and the same readback query (`server.py:4293`). The code paths are symmetric by construction, which means the failure is behavioral, not structural.

### 2. "Treat the remaining bug as a host read-model closure bug" is the correct default

This assumption is warranted. The code evidence shows:

- The readback route (`GET /api/concept/analyses/{concept}`, server.py:4293) queries by `(concept, analysis_type, project_id)` against the database
- The 404 means no row was found for `(innovation, logical, cutover-artifact-authority-20260406-162636)`
- The critic job shows as "completed" in memory, meaning `_run_rebased_concept_analysis()` returned successfully
- Therefore the problem is almost certainly in the persistence step, not the execution or translation step

### 3. Appropriate strategic narrowing

The out-of-scope exclusions are well-calibrated. This tranche correctly avoids:

- reopening artifact-authority design
- widening into inferential
- drifting into analyzer-mgmt work
- new concept submodes

This fits the "close the gap before moving the boundary" discipline the program needs.

### 4. The completion condition is honest and testable

Requiring all three properties (logical execution, logical readback, scrutiny) to close on a brand-new project ID is the right proof standard. It prevents the common failure mode of validating against stale data.

---

## Corrections Needed Before Implementation

### 1. CRITICAL: `concept_artifact_authority.py` does not exist

The memo lists this as "Primary Code Evidence":

> `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_artifact_authority.py`

This file does not exist in the codebase. The actual file is:

> `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_by_ref.py`

`concept_by_ref.py` handles concept-analysis launch (building the plan, registering documents, starting the execution thread). There is no `concept_artifact_authority.py` — the concept-analysis path does not use the structured artifact store (`src/analysis_products/store.py`) at all. Concept results are stored entirely within the-critic's PostgreSQL database and disk, not in analyzer-v2's artifact system.

**Correction**: Replace the file reference with `concept_by_ref.py`. Acknowledge explicitly that the concept path does not yet use analyzer-v2's artifact store — this matters for understanding which codebase owns the bug.

### 2. CRITICAL: The `concept-analysis-by-ref/result` endpoint does not exist

The memo cites this as Primary Live Evidence:

> `https://analyzer-v2.onrender.com/v1/orchestrator/concept-analysis-by-ref/result?consumer_key=the-critic&...`

This endpoint does not exist in the codebase. The only concept-analysis-by-ref endpoint is:

- `POST /v1/orchestrator/concept-analysis-by-ref` (orchestrator.py:501) — for launching

There is no `GET /concept-analysis-by-ref/result` for reading translated artifacts back from analyzer-v2. The memo's claims about `lookup_mode = "exact_run"` and `contract_validation_status = "passed"` reference an interface that has not been implemented.

This means the "exact lookup by analyzer_v2_job_id" claim for inferential cannot be verified against actual code. If inferential was proven through a different mechanism (e.g., direct phase-output fetch plus host-local translation), the memo should say so honestly.

**Correction**: Remove or correct the result-endpoint live evidence. Clarify exactly how the inferential proof was read back — was it through the-critic's local persistence after completion, not through an analyzer-v2 result endpoint?

### 3. The most probable root cause should be named explicitly

The code reveals a specific smoking gun that the memo should have identified:

`_save_concept_analysis_to_db()` (server.py:3842-3875) **silently swallows database persistence errors**:

```python
except Exception as e:
    logger.warning(f"Failed to save concept analysis to database: {e}")
```

This means:
1. The logical analysis completes and translates successfully
2. `_save_concept_analysis_to_db()` fails for some reason
3. The error is caught and logged as a warning only
4. The job proceeds to `_CONCEPT_JOBS[job_id]["status"] = "completed"` (server.py:4136)
5. The in-memory job shows "completed" but the database has no row
6. The readback route queries the database → 404

This is the most likely explanation for the observed behavior. The memo's Phase 1 (trace the completed fresh logical run) should start here.

**Correction**: Add this as the leading hypothesis in the "most likely one of" list. Phase 1 should explicitly check the Render logs for the `"Failed to save concept analysis to database"` warning message for the logical run.

### 4. The completion predecessor contradicts the "logical readback fails" claim

The completion memo (`MEMO_2026-04-06_close_read_concept_analysis_live_authority_and_thin_client_cutover_completion.md`) explicitly states that logical readback **was proven on a previous project**:

- Project: `cutover-live-tiny-20260406`
- Critic job: `concept-1775483282630-a0a4aa`
- `GET /api/concept/analyses/innovation` returned a persisted logical artifact with `_analysis_provenance.execution_owner = "analyzer-v2"`

But the new scope memo says logical readback fails on:

- Project: `cutover-artifact-authority-20260406-162636`

So logical readback **worked once and then stopped working** on a different project. This is an important distinction the memo does not surface. The root cause is not "logical readback was never wired" — it's "logical readback is fragile and breaks under certain conditions."

**Correction**: Acknowledge the regression character of this failure. The implementation should investigate what differs between the two projects/runs, not just fix the symptom. This may be a transient database connectivity issue on Render, a JSONB serialization edge case triggered by different input data, or a schema migration gap.

---

## Hidden Risks

### 1. Silent error swallowing pattern is systemic

The `_save_concept_analysis_to_db` error swallowing is not unique to logical analysis. It affects ALL analysis types equally. If the fix is narrow (e.g., adding a specific retry for logical), it leaves the silent-failure pattern in place for every other mode.

**Recommendation**: Phase 2 should harden the DB save to propagate errors, or at minimum mark the job as "completed_with_warnings" rather than silently succeeding.

### 2. Phase 3 (scrutiny) may be unnecessary

Scrutiny is completely decoupled from the concept analysis mode (confirmed in the code — `ScrutinizePremiseRequest` has no `analysis_mode` field). If the logical result is properly persisted (fixing Phase 2), scrutiny should derive from it without any code changes to the scrutiny path itself.

The memo should make Phase 3 conditional: "Only repair scrutiny derivation if Phase 2 persistence fix does not automatically resolve scrutiny readback."

### 3. Terminology overload: "artifact authority" vs actual architecture

The memo uses "translated artifact authority" language from the structured-artifact world (AOI, genealogy). But the concept-analysis path does not use analyzer-v2's artifact store at all. Concepts are translated in the-critic's memory using analyzer-v2 transformation templates, then persisted directly to the-critic's database.

This is not a bug — it may be the intended intermediate state. But calling it "artifact authority" when there is no artifact store involvement risks confusing the implementor into looking at the wrong layer.

### 4. The Render deployment state may not match the codebase

The git status shows extensive uncommitted changes. The deployed Render service may be running code that differs from the local working tree. The implementor should verify which commit is deployed before debugging.

---

## Strategic Positioning

### Does this tranche fit the "analyzer-v2 as the brain" objective?

Yes, properly. This is a necessary closure step before the broader artifact-authority relocation can proceed. You cannot move translated-artifact authority into analyzer-v2 if the host-local persistence of those artifacts is broken. The correct sequence is:

1. Fix host-local persistence/readback (this tranche)
2. Then move the authority boundary upstream (the translated-artifact authority tranche)

Reversing this order would compound the debugging surface.

### Is this local patching that should be handled at a higher layer?

No. The fix is properly local. The failure is in the-critic's persistence path, and the fix should stay there. Promoting this into an architectural refactoring would be premature given that the host-local pattern is the current operational contract.

---

## Summary of Required Corrections

| # | Severity | Correction |
|---|----------|------------|
| 1 | Critical | Replace `concept_artifact_authority.py` reference with `concept_by_ref.py` |
| 2 | Critical | Remove or correct the non-existent `concept-analysis-by-ref/result` endpoint reference |
| 3 | Important | Name `_save_concept_analysis_to_db` silent error swallowing as leading root-cause hypothesis |
| 4 | Important | Acknowledge regression character — logical readback worked previously on a different project |
| 5 | Minor | Make Phase 3 conditional on Phase 2 not automatically resolving scrutiny |
| 6 | Minor | Clarify that the concept path does not use analyzer-v2's artifact store |

---

## Verdict: Approve with Corrections

The tranche is correctly scoped, strategically sound, and bounded. The completion condition is honest. The four corrections above should be applied before implementation begins, primarily because the current live-evidence references point to non-existent code and the root-cause hypothesis can be significantly narrowed using the code evidence already available. None of these corrections require expanding the scope — they sharpen it.
