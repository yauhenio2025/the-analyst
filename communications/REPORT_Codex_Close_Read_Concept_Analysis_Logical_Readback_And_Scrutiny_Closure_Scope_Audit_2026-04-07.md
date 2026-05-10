# Report: Close Read Concept Analysis Logical Readback And Scrutiny Closure Scope Audit

Date: 2026-04-07
Auditor: Codex
Verdict: `approve with corrections`

## Findings

### 1. The memo overstates the status of translated-artifact authority relative to both the recent memo trail and the checked-in code

This is the most important correction.

The immediate 2026-04-06 memo trail does not treat translated-artifact authority as already closed. It treats it as the next tranche:

- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_live_concept_authority_cutover.md` says translated host-artifact authority migration into analyzer-v2 is next.
- `communications/MEMO_2026-04-06_close_read_concept_analysis_translated_artifact_authority_scope.md` scopes that migration as work to do, not work completed.
- `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_and_thin_client_cutover_completion.md` explicitly says the previous completion does not mean analyzer-v2 already owns translated artifact persistence/read authority.

The current code agrees with that narrower reading:

- analyzer-v2 exposes a launch route at `src/api/routes/orchestrator.py:501`, and `src/orchestrator/concept_by_ref.py` builds and launches the bounded by-ref run.
- the current checkout does not contain the memo-cited `src/orchestrator/concept_artifact_authority.py`.
- the current checkout does not expose a local `GET /v1/orchestrator/concept-analysis-by-ref/result` route.
- in the-critic, `_run_rebased_concept_analysis` still launches analyzer-v2, polls the executor job, fetches raw phase outputs, and then translates locally (`/home/evgeny/projects/the-critic/api/server.py:3963`, `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_client.py:838`, `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_client.py:922`, `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/analyzer_v2_recomposition.py:79`).

So the memo should not freeze “logical artifact authority exists upstream” as a code-backed baseline. The correct wording is narrower:

- live evidence may indicate an upstream exact-artifact path exists
- but the repo state still shows the-critic owning the translation-and-persist step
- therefore Phase 1 must re-verify that assumption before treating the remaining bug as purely downstream

### 2. The code makes host persistence failure a stronger default diagnosis than generic readback/filtering failure

The memo is directionally right that the remaining problem is post-completion rather than analyzer-v2 execution.

But the sharper code-backed default diagnosis is not “readback probably queries the wrong thing.” It is:

- logical translation/persistence on the-critic may be failing after successful analyzer-v2 completion
- or the deployed path is diverging from the repo path

Why this is the stronger default:

- the-critic persists concept analyses through `_save_concept_analysis_to_db` (`/home/evgeny/projects/the-critic/api/server.py:3842`)
- that function catches and suppresses exceptions with only a warning log (`/home/evgeny/projects/the-critic/api/server.py:3874`)
- `run_concept_analysis_thread` still marks the job completed after calling that save path (`/home/evgeny/projects/the-critic/api/server.py:4127`)
- `GET /api/concept/analyses/{concept}` is a straightforward ORM read on `project_id`, `analysis_type`, and case-insensitive concept name (`/home/evgeny/projects/the-critic/api/server.py:4293`)

That means the live symptom set described in the memo:

- analyzer-v2 job completed
- critic job completed
- concept readback returned `404`

fits a silent host persistence failure very cleanly.

The memo should therefore change its default assumption from:

- “host read-model closure bug”

to:

- “host post-completion closure bug, most likely at translation/persistence unless direct evidence points to readback filtering”

That is a materially better implementation starting point.

### 3. Scrutiny closure is adjacent to the logical seam, but it is not powered by the same storage/read path the memo implies

The memo currently groups logical readback and scrutiny closure too tightly under one presumed read-model bug.

The code splits them:

- `GET /api/concept/analyses/{concept}` reads `DBConceptAnalysis` from the database (`/home/evgeny/projects/the-critic/api/server.py:4293`)
- scrutiny result readback reads `DBScrutinyResult` from the database (`/home/evgeny/projects/the-critic/api/server.py:7018`)
- but scrutiny generation itself loads logical context from the logical result file on disk, not from concept-analysis DB readback (`/home/evgeny/projects/the-critic/analyzer/analyze_scrutinize_premise.py:50`, `/home/evgeny/projects/the-critic/analyzer/analyze_scrutinize_premise.py:132`)

That matters for diagnosis:

- if a logical job completed, the code saves the logical result to disk before attempting DB persistence (`/home/evgeny/projects/the-critic/api/server.py:4131`)
- so a missing concept-analysis DB row does not by itself prove the scrutiny engine cannot see the logical artifact
- `count = 0` on `/api/scrutiny/results/{concept}` may simply mean no scrutiny job was successfully launched or no scrutiny result was persisted

So the memo should separate:

- logical concept-analysis readback closure
- scrutiny input derivation/launch closure
- scrutiny result persistence/readback closure

Those can still belong in one tranche, but they should not be treated as one already-proven root cause.

### 4. analyzer-mgmt is adjacent evidence, not a critical-path dependency of this particular closure bug

I checked analyzer-mgmt because the prompt asked for it.

The relevant page here is the job/result-boundary operator surface, which links result boundaries back to workflow implementations and linked transformations (`/home/evgeny/projects/analyzer-mgmt/frontend/src/pages/jobs/[id].tsx:1046`).

That is useful operator context, but it is not part of the failing persistence/readback path itself. The critical runtime seam remains:

- analyzer-v2 by-ref launch and executor outputs
- the-critic translation/persistence
- the-critic concept-analysis and scrutiny readbacks

So the memo is right not to widen this tranche into analyzer-mgmt repair work. The broader “operator-console truth” concern remains strategically relevant, but it is not on the critical path for this specific bug.

## Strongest Things The Memo Gets Right

- It keeps the tranche bounded to the remaining logical post-completion seam instead of reopening broader concept-family, UI, or cross-corpus work.
- It correctly treats analyzer-v2 execution itself as likely already working for the failing specimen, because the described failure occurs after analyzer-v2 job completion and after the-critic marks the concept job completed.
- The final rerun design is strong. Using a brand-new project id is the right way to exclude stale-data false positives.
- The tranche still fits the larger “analyzer-v2 as the brain, host as thin consumer” direction, as long as it does not prematurely assume artifact-authority closure that the current repo state does not yet show.

## Open Questions / Assumptions

- Does the deployed analyzer-v2 service actually have an exact translated-artifact read route that is not represented in this checkout, or is the memo relying on live-only behavior that has not been merged back into the repo?
- Was a scrutiny run actually attempted on the failing fresh logical project after the logical concept job completed, or is `count = 0` only showing that no scrutiny result exists yet?
- For the cited failing logical run, did the-critic write the logical disk artifact successfully while failing DB persistence, or did the failure occur earlier in the local translation path?

## Readiness Summary

The memo is close, but not implementation-ready exactly as written.

It becomes ready if it makes three corrections:

1. Soften the claim that translated-artifact authority is already a settled baseline, and require Phase 1 to verify that assumption directly.
2. Reframe the default diagnosis from generic host readback/filtering failure to host post-completion persistence closure, unless direct trace evidence falsifies that.
3. Split scrutiny closure into:
   - scrutiny launch/input derivation
   - scrutiny result persistence/readback
   rather than assuming both are the same seam as concept-analysis readback.

With those corrections, the tranche is properly bounded, strategically coherent, and worth executing next.
