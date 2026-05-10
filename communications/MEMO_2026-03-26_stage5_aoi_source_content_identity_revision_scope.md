# Memo: Stage 5 AOI Source-Content Identity Revision Scope

Date: 2026-03-26
Status: Draft scope memo for implementation review
Program: Dynamic Bespoke Apps Platformization
Supersedes:
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_scope.md`
  - but only as the immediate next-step memo; the browser rerun itself is now complete and remains part of the proof trail
Depends on:
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_recovery_completion.md`
- `communications/MEMO_2026-03-26_stage5_aoi_local_snapshot_idempotence_revision_completion.md`
- `communications/MEMO_2026-03-26_stage5_aoi_execution_backed_browser_closeout_rerun_completion.md`
- `communications/PROOF_stage5_aoi_evolution_ready_execution_backed_recovery_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_preflight_identity_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_precompose_pin_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_requests_2026-03-26.json`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_session_2026-03-26.har`
- `communications/PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_state_2026-03-26.png`
Roadmap sources:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

## Summary

The counted planner-primary browser rerun is no longer the missing step.

That rerun is now complete and structurally sound on the repaired host path for:

- upstream counted source: `job-6ee8b0621177`
- current canonical local alias: `gen-v2-9e3e5ad74dbb`
- selected source thinker at the host/browser boundary: `otto_neurath`

The remaining blocker is content integrity inside the recovered execution-backed AOI source itself.

Observed contradiction:

- the saved AOI result for nominal Otto Neurath source `job-6ee8b0621177` / `gen-v2-9e3e5ad74dbb` still contains Phase `1.0` preview content with `selected_source_thinker = john_oneill`
- the same recovered payload still includes downstream report language framing Benanav's project as an operationalization of John O'Neill's reconstruction of Otto Neurath

Most important current diagnosis signal:

- the first real contradiction is already visible upstream in raw Phase `1.0` `aoi_thematic_synthesis` output for the recovered run
- the strongest primary suspect is capability-definition example contamination:
  - `src/engines/capability_definitions/aoi_thematic_synthesis.yaml`
  - injected verbatim into prompts by `src/stages/capability_composer.py`

So the next honest step is one bounded diagnosis-and-repair slice on AOI source-content identity integrity.

This is not another host/browser repair pass, not another browser rerun by default, and not a Tranche 3 pivot.

## Why This Is Now The Next Honest Step

Current program state is:

- the frozen Stage 5 seam gate already passed on fixture-backed evidence
- one fresh `execution_backed` AOI run exists and has been recovered to durable upstream truth
- the repaired host/browser path now preserves:
  - explicit row pinning after `Clear`
  - canonical local snapshot reuse under repeated `cache-v2`
  - preserved `source_v2_job_id`
  - preserved host-boundary `source_analysis_id`
  - successful planner-backed `compose-from-selection`
- Stage 2 still remains open only because the recovered AOI payload is not yet content-trustworthy enough

The open question is no longer:

- can the host/browser path consume the recovered source honestly?

It is now:

- where does the recovered AOI source-content identity drift enter, and can that drift be repaired or convincingly explained without widening scope dishonestly?

That is the right next bounded question.

## Bounded Claim

This slice should do one thing:

- determine where source-thinker identity drift enters the recovered AOI result and repair only the minimal AOI single-thinker seams required so selected-source truth is preserved or contradictions fail closed

This slice should not reopen:

- host snapshot idempotence
- browser proof capture
- planner-backed compose identity continuity
- fresh AOI launch by default
- frozen four-case pack reruns
- roadmap order
- Tranche 3 generalization

## Scope Decisions

### Decision 1: Treat this as analyzer-side/source-content integrity work, not host/browser work

The counted browser rerun already proved the repaired host path structurally.

Do not reopen:

- AOI panel row-pinning law
- `cache-v2` reuse/idempotence
- `compose-from-selection` identity continuity

Unless the diagnosis proves those are somehow causally implicated in the content contradiction, they are closed baseline for this slice.

### Decision 2: Keep the recovered execution-backed source fixed for diagnosis

The fixed validation source remains:

- `source_v2_job_id = job-6ee8b0621177`

Prefer diagnosing the already-recovered source first.

Do not launch a new AOI run by default just to get a “cleaner” artifact trail.

If the defect turns out to live in immutable raw outputs such that the existing run cannot be rehabilitated honestly in place, say that explicitly in closeout and only then authorize a fresh rerun as a follow-on step.

### Decision 3: Diagnose the seam across the full AOI identity chain

The diagnosis must trace source-thinker identity across all of these layers:

1. launch / plan / source-corpus selection truth
   - selected thinker in plan data
   - prior-work/source-document scoping
2. phase prompt / raw engine-output truth
   - AOI source-corpus prompt assembly
   - engine contract examples / sample payloads
   - raw phase outputs and stored `final_output_preview`
   - cross-phase context propagation through `context_broker`
3. AOI normalization truth
   - thematic synthesis normalization
   - engagement/sin/report cross-phase use of prior normalized data
4. saved-result / presentation truth
   - result metadata
   - structured payloads
   - saved-result detail
   - presentation/compose surfaces

The diagnosis must name the first layer where the contradiction becomes real.

Current expectation from the evidence trail:

- the first real contradiction is likely raw Phase `1.0` AOI thematic output, not presentation
- later layers may either propagate that contradiction through raw cross-phase context or partially mask it through normalization

The implementation closeout must say explicitly whether that expectation was confirmed or disproved.

### Decision 4: Distinguish hard identity contradiction from analytically acceptable mention

These are not the same:

- a hard identity contradiction:
  - explicit `selected_source_thinker = john_oneill` in a nominal Otto Neurath run
  - source-document inventory or selected-source metadata pointing to the wrong thinker
  - theme-level provenance fields pointing to works outside the selected thinker corpus
  - representative-quote provenance fields pointing to the wrong thinker corpus
- an analytically acceptable mention:
  - report prose that references John O'Neill as an intermediary interpreter while still preserving Otto Neurath as the selected source thinker everywhere identity is explicit

This slice must decide which observed outputs are:

- truly invalid identity drift
- defensible interpretive mention
- or ambiguous enough to require a guardrail anyway

Operational rule:

- any explicit identity-bearing field that contradicts plan-selected thinker truth is invalid
- prose mention of John O'Neill is only acceptable when it does not create any explicit identity contradiction anywhere in the structured payload or persisted AOI artifact chain

### Decision 5: Keep the repair minimal and AOI-specific

The likely seam family is bounded, but not all loci are equally likely.

Primary suspect to inspect first:

- capability-definition example contamination in `aoi_thematic_synthesis`
  - `src/engines/capability_definitions/aoi_thematic_synthesis.yaml`
  - injected via `src/stages/capability_composer.py`

Potential repair loci include:

- AOI capability definition examples / output-contract samples
- raw cross-phase propagation through `context_broker`
- AOI normalization / contract validation
  - especially the current mixed-truth artifact seam where top-level selected-source truth is overwritten from plan context while deeper theme provenance may remain polluted
- phase-preview generation or persistence
- result/presentation guardrails over contradictory selected-source identity

Important constraint:

- fixing the capability definition alone only prevents future Phase `1.0` contamination
- the recovered run may still carry downstream raw contamination in Phases `2.0`-`4.0` if those phases consumed contaminated upstream raw outputs through `context_broker`

The slice should not widen into:

- general engine prompting redesign
- generalized cross-workflow semantic validation
- model swaps or tuning experiments
- a broad presenter rewrite

### Decision 6: Add explicit fail-closed or override law for selected-source identity

After this slice, AOI single-thinker runs must not silently carry contradictory explicit source-thinker identity.

For any AOI surface that presents explicit selected-source identity:

- either the identity must match plan-selected thinker truth
- or the surface must fail closed / suppress the contradictory field rather than persisting it as if valid

The closeout must state which policy was implemented:

- strict fail-closed
- canonical override from plan context
- or a narrower mixed rule with justification

This decision applies not only to top-level `selected_source_thinker`, but also to:

- source-document inventory
- theme-level provenance
- representative-quote provenance
- any other persisted explicit identity-bearing AOI field

### Decision 7: Keep the recovered-run reuse question explicit

The closeout must answer separately:

- can the recovered run `job-6ee8b0621177` be made honest in place by bounded refresh/reprojection over correct identity law?
- or does the defect live in immutable raw phase output such that a fresh execution-backed rerun becomes mandatory after the repair?

Do not blur those together.

Additional clarification:

- “display-safe” recovery is not enough for closure-grade evidence
- if the repair only suppresses or corrects preview/presentation leakage while raw AOI outputs remain materially contradictory, the recovered run may become display-safe but still not closure-grade
- if structured artifacts can be corrected in place but report prose remains contaminated because downstream phases were generated from bad upstream raw context, the recovered run may be artifact-safe yet still not prose-safe
- if report-summary or engagement-pattern prose cannot be rehabilitated honestly in place, closure-grade recovery may require bounded partial re-execution after the upstream contamination path is fixed
- closure-grade rehabilitation requires that the persisted AOI artifact chain itself no longer carries explicit contradictory selected-source identity

### Decision 8: Keep roadmap order fixed

Stage 2 still remains open.
Tranche 3 still remains blocked.

This slice exists to answer whether the exemplar’s remaining problem is a bounded AOI content-integrity seam.

It does not authorize:

- Stage 2 closure by implication
- another browser rerun by default
- a Tranche 3 pivot

### Decision 9: Use explicit stop-and-revise rules

Stop and write a revision memo if any of these turn out to be true:

- the real defect is that the selected source corpus itself was wrong upstream
- the contradiction is not AOI-specific and would require a cross-workflow contract redesign
- the recovered run cannot be rehabilitated honestly in place and a fresh rerun becomes necessary for reasons broader than this bounded slice
- the supposed John O'Neill contradiction is actually downstream artifact noise while another deeper seam is responsible for closure failure

## Code Areas To Inspect First

At minimum:

- `src/executor/phase_runner.py`
- `src/aoi/contract.py`
- `src/analysis_products/store.py`
- `src/analysis_products/result_contract.py`
- `src/executor/context_broker.py`
- `src/presenter/composition_source_bridge.py`
- `src/presenter/view_refiner.py`
- `src/executor/workflow_runner.py`
- `src/engines/capability_definitions/aoi_thematic_synthesis.yaml`
- `src/engines/capability_history/aoi_thematic_synthesis_snapshot.json`
- `src/stages/capability_composer.py`

Likely tests:

- `tests/test_aoi_contract.py`
- `tests/test_registered_corpus_launch.py`
- `tests/test_compose_from_intent.py`
- `tests/test_presentation_api.py`

## Proposed Deliverables

### 1. One diagnosis artifact bundle

At minimum:

- one source-identity trace artifact showing:
  - plan-selected thinker truth
  - raw Phase `1.0` output / preview truth
  - normalized AOI metadata truth
  - Phase `4.0` thematic report payload truth
  - saved-result/presentation truth
- one short root-cause note naming the first layer where contradiction enters

### 2. Focused regression coverage

At minimum, the new coverage should prove:

- a nominal Otto Neurath AOI single-thinker run cannot persist explicit `selected_source_thinker = john_oneill`
- capability/example contamination cannot leak into normalized AOI selected-source identity unchecked
- contradictory raw Phase `1.0` selected-source identity cannot survive into persisted AOI artifacts silently
- any explicit selected-source identity surfaced in saved AOI artifacts is consistent with plan context or fails closed
- theme-level provenance cannot name works outside the selected thinker corpus silently
- representative-quote provenance cannot preserve mismatched thinker/work identity silently
- if preview/state is still exposed for AOI single-thinker runs, it cannot contradict the selected thinker truth silently

### 3. One closeout memo

Produce one of:

- success: `communications/MEMO_<actual-date>_stage5_aoi_source_content_identity_revision_completion.md`
- failure/revision: `communications/MEMO_<actual-date>_stage5_aoi_source_content_identity_revision.md`

That memo must state:

- the root cause
- exactly which layer was repaired
- whether the recovered run can now be trusted in place
- whether a fresh execution-backed rerun is still required after the repair
- whether Stage 2 status changed

## Verification Expectation

Run focused analyzer verification against the actual seam.

At minimum:

- `PYTHONPATH=. pytest -q tests/test_aoi_contract.py tests/test_registered_corpus_launch.py tests/test_presentation_api.py tests/test_compose_from_intent.py`

If the implemented repair lands in a different bounded file/test set, the closeout should record the exact substituted command and why it is the real seam.

## Status Implications

This slice does not close Stage 2 by itself.

Success for this slice means only:

- the remaining blocker is accurately diagnosed
- the bounded AOI source-content identity seam is repaired or explicitly narrowed
- the program knows honestly whether the recovered run can be trusted in place or whether a fresh rerun is still required

Stage 2 closes only after that repaired state is evaluated honestly against the frozen rubric.
