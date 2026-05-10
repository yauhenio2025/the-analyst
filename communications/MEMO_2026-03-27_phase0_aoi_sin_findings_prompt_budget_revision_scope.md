# Memo: Phase 0 AOI Sin-Findings Prompt-Budget Revision Scope

Date: 2026-03-27
Status: Draft scope memo for implementation review
Program: Dynamic Bespoke Apps Platformization
Depends on:
- `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md`
- `communications/MEMO_2026-03-27_phase0_aoi_active_discovery_repair_completion.md`
- `communications/MEMO_2026-03-27_phase0_aoi_exemplar_honesty_closeout_revision_after_active_discovery_repair.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_active_boundary_2026-03-27.json`
- `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_terminal_failure_2026-03-27.json`

## Summary

The March 27 fresh Phase 0 rerun proves that thinker-scoped live discovery is fixed, but it also proves that Phase 0 still cannot close.

The new blocker is narrower and more upstream:

- fresh job: `job-226f65f43a3b`
- plan: `plan-54b6f075fdf2`
- failing phase: `3.0`
- failing engine: `aoi_sin_findings`
- failing pass: `Finding Discovery`
- exact provider rejection: `prompt is too long: 1037154 tokens > 1000000 maximum`

The current code and plan shape support that diagnosis:

- the executed March 27 job `job-226f65f43a3b` persisted a six-phase `plan_data`, not just the on-disk `plan-54b6f075fdf2.json` template:
  - `0.5` Target Work Profiling
  - `1.0` Source Thematic Synthesis
  - `1.5` Source Work Profiling
  - `2.0` Engagement Mapping
  - `3.0` AOI Sin Findings
  - `4.0` Thematic AOI Report
- that executed `plan_data` also makes `1.0` depend on `1.5`, and the same failed job persisted `20` `phase_outputs` rows for `1.5`
- the executor assembles upstream Phase `1.0` and `2.0` prose context for Phase `3.0`, and it loads all pass-level saved outputs for those phases rather than only each phase's final output
- `context_broker` still defaults to `50_000` chars per upstream block unless a per-phase override exists
- the executed Phase `3.0` plan still sets:
  - `requires_full_documents = true`
  - `document_scope = whole`
  - `chapter_targets = null`
  - `max_context_chars_override = null`
- the dominant Phase `3.0` inflation source is the hardcoded document assembly in `phase_runner`, which concatenates:
  - the full Benanav target corpus
  - the full selected Otto source corpus
- `requires_full_documents` only controls 1M-endpoint selection; it does not control what text Phase `3.0` assembles
- `engine_runner` treats `prompt is too long` as a non-retry terminal error after the provider already rejected the request

There is also an important planning precedent in the repo:

- earlier AOI plan `plan-12e3db25fb90` recognized that the same Neurath corpus is about `3.6M` chars and inserted source-corpus profiling to make Phase `1.0` tractable
- but that earlier plan still sent full documents to Phase `3.0`, so it should be treated as corroborating precedent, not as proof that the Phase `3.0` budget problem was already solved historically

### Measured March 27 baseline volumes

The following are the canonical before-fix reference volumes for this slice, measured from the failed `job-226f65f43a3b` run:

- Phase `3.0` document_text (target + full source corpus): `3,901,990` chars
- Phase `3.0` shared context (upstream Phase 1.0 + 2.0 prose): `250,836` chars
- Reconstructed pass-1 total (document_text + shared context + system prompt): ~`4,160,195` chars
- Provider-reported token count: `1,037,154` tokens (exceeds 1M maximum)

The eventual implementation completion or revision memo must carry these three before-fix numbers for explicit before/after comparison.

So the next honest step is one bounded analyzer-side prompt-budget repair for Phase `3.0`, then one fresh Phase 0 rerun on the same fixed Otto target.

This is not host/browser work, not discovery work, and not a Phase 1 generalization slice.

## Bounded Claim

This slice should do one thing:

- make the fixed Otto `evolution_ready` Phase `3.0 / aoi_sin_findings` path complete without exceeding the model prompt budget, while preserving the same project, thinker, workflow, task, and honest proof bar

More specifically, the live failing contract that must be repaired is:

- full target corpus
- full selected-source corpus
- all pass-level upstream prose from Phases `1.0` and `2.0`
- then, at deep depth, later Phase `3.0` passes also inherit inner-pass context on top

This slice should not:

- change the fixed corpus to make the run cheaper
- change the fixed task to something easier
- reopen host/browser continuity
- reopen thinker-scoped discovery
- treat weaker AOI output as acceptable just because it fits
- pivot into Phase 1 bridge generalization

## Why This Is Now The Next Honest Step

Current program state is:

- the frozen Stage 5 seam gate already passed on fixture-backed evidence
- the planner-primary host/browser path already passed structurally on the recovered execution-backed proof
- the source-content contamination repair is already landed for future runs
- the by-ref live-discovery seam is now repaired and proven on a fresh March 27 rerun

So the open question is no longer:

- can the host find and pin the fresh AOI run honestly?

It is now:

- can the analyzer execute Phase `3.0 / aoi_sin_findings` on the fixed Otto corpus without overrunning the prompt budget?

That is the only bounded question this slice should answer.

## Scope Decisions

### Decision 1: Treat this as analyzer-side prompt-budget work, not host/browser work

The fresh rerun already proves the discovery seam moved upstream.

Do not reopen:

- AOI panel source pinning
- local snapshot continuity
- compose-page launch semantics
- thinker-scoped live discovery

Unless the next fresh rerun proves one of those seams is causally implicated again, they are closed baseline for this slice.

### Decision 2: Keep the validation target fixed

The fixed validation target remains:

- project: `round5-proof-dossier-final-1774100000`
- thinker: `otto_neurath`
- workflow: `anxiety_of_influence_thematic_single_thinker`
- task: `Show how Aaron Benanav's use of Otto Neurath's planning argument evolves across the corpus.`
- corpus: the same four Otto Neurath PDFs already pinned in the Phase 0 execution memo

Do not silently switch:

- project
- thinker
- workflow
- task
- corpus size
- rubric strength

If the only way to stay under budget is to weaken that fixed target dishonestly, stop and write a revision memo.

### Decision 3: Diagnose against the failed March 27 plan, but validate on a fresh rerun

Use the failed March 27 run as the diagnosis source:

- job: `job-226f65f43a3b`
- plan: `plan-54b6f075fdf2`

That is the right artifact to inspect because it is the first fresh post-discovery-repair Phase 0 attempt on the fixed Otto target.

But do not treat successful diagnosis alone as completion.

The repair only counts if a fresh rerun is launched after the repair and the Phase `3.0` budget failure no longer occurs.

### Decision 4: Treat current plan shape as part of the seam

The March 27 failure is not just a generic provider accident.

The executed March 27 job explicitly sends Phase `3.0` down a maximal path:

- full documents enabled
- whole-document scope
- no chapter targeting
- no per-phase context-char override

There is also codebase precedent that this corpus needed pre-digestion at least for Phase `1.0`:

- `plan-12e3db25fb90` inserted source-corpus profiling because the same Neurath corpus was too large for raw Phase `1.0` whole-corpus handling
- the executed March 27 job had already moved in that direction by adding `1.5` Source Work Profiling and still failed at `3.0`

So the repair may belong partly in:

- plan generation / plan defaults
- phase-execution input shaping
- context assembly
- or a narrower Phase `3.0` engine input contract

Do not assume the only honest repair locus is the `aoi_sin_findings` prompt text itself.
Also do not assume that changing `requires_full_documents` alone changes Phase `3.0` document assembly, because in current code it does not.

### Decision 5: Keep the repair minimal and phase-specific

Allowed repair shapes include only the minimal combination required to make Phase `3.0` honest and tractable on the fixed Otto target, for example:

- changing what document text Phase `3.0` receives
- phase-specific source-corpus pre-digestion or staging
- bounded chapter/document targeting for Phase `3.0` if that still preserves honest AOI finding quality
- phase-specific upstream-context shaping or stricter pass-through limits
- executor-side or planner-side prompt-budget preflight so the run fails before an Anthropic `400` if the assembled payload is impossible

Important constraint:

- the slice should preserve the analytical contract of AOI sin findings
- it must not solve the problem by silently dropping the very provenance-bearing evidence the phase is supposed to produce

First diagnostic question:

- does Phase `3.0` genuinely need the raw `~3.6M`-char Otto source corpus when Phase `1.0` already synthesized it and Phase `2.0` already mapped engagement?

If upstream context plus the target corpus is sufficient for honest sin findings, the simplest repair lever is Phase `3.0` document assembly.

### Decision 6: Validate against all deep Phase `3.0` passes, not only Pass 1

The March 27 failure happened on:

- Pass `1`
- `Finding Discovery`

But deep `aoi_sin_findings` is a three-pass phase:

- `discovery`
- `inference`
- `integration`

Later passes inherit:

- the same shared upstream context
- plus inner-pass context from earlier passes

So a pass-1-only repair is not sufficient.

The repaired scope must stay under budget across the full deep Phase `3.0` execution shape, not just its first pass.

### Decision 7: Add explicit fail-fast law for impossible prompt shapes

Right now `engine_runner` treats `prompt is too long` as a non-retry terminal failure only after the provider rejects the request.

That is too late for an honest Phase 0 proof loop.

After this slice, the system should make one of these true:

- the prompt shape is reduced enough that the provider accepts it
- or the executor/planner fails earlier with an explicit budget diagnosis before making the impossible provider call

The closeout must say which law was implemented.

Preferred implementation location for any pre-provider fail-fast law:

- the existing `total_input_chars` computation path in `engine_runner`

### Decision 8: Quarantine post-`3.0` Phase `4.0` artifacts from seam diagnosis

The March 27 artifact trail looks misleading because the executor currently allows Phase `4.0` to run after a failed Phase `3.0`.

Program rule for this slice:

- post-`3.0` Phase `4.0` artifacts on the failed March 27 job are not trustworthy seam-location evidence
- the blocker remains Phase `3.0 / aoi_sin_findings / Finding Discovery`

I do not want to widen this slice into a general workflow-runner dependency-gating repair by default.
But the memo must explicitly quarantine downstream Phase `4.0` output from diagnosis.

### Decision 9: Keep the slice out of general prompt-framework redesign

This slice should not widen into:

- model-swap experiments
- broad chunking-framework redesign
- generalized cross-workflow context-budget architecture
- AOI host/product work
- lifecycle work
- roadmap reordering

If diagnosis proves the seam is broader than this bounded slice, stop and write a revision memo instead of pretending the scope stayed narrow.

### Decision 10: Force an explicit closeout answer on where the real seam lived

The implementation closeout must answer explicitly:

1. Was the dominant seam in plan generation, executor input shaping, engine prompt composition, or some combination?
2. Is source-corpus pre-digestion now required for this Otto AOI shape, or was a smaller bounded repair enough?
3. Did the fresh rerun actually clear Phase `3.0`, or did it reveal a different bounded blocker?
4. Were any Phase `4.0` artifacts produced after a failed dependency, and if so, were they correctly quarantined from diagnosis?

Do not blur those answers together.

## Proposed Deliverables

### 1. Bounded analyzer repair

One analyzer-side repair slice that makes the fixed Otto Phase `3.0` path tractable.

Likely ownership areas:

- `/home/evgeny/projects/analyzer-v2/src/orchestrator/`
- `/home/evgeny/projects/analyzer-v2/src/executor/`
- `/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/`
- `/home/evgeny/projects/analyzer-v2/src/operationalizations/definitions/`

### 2. Focused regression coverage

At minimum, the regression story should prove the seam that was actually fixed.

Examples:

- plan-generation/config regression if the repair changes Phase `3.0` plan shape
- executor/context-budget regression if the repair changes upstream context assembly or fail-fast budgeting
- engine-level regression if the repair changes Phase `3.0` prompt composition or staged execution

Required regression minimum:

- one regression for pre-provider budget failure or preflight budget diagnosis
- one regression for the specific narrowing lever that was actually chosen:
  - document assembly narrowing
  - upstream context narrowing
  - pass-level staging
  - or a combination

Suggested test ownership:

- `/home/evgeny/projects/analyzer-v2/tests/test_adaptive_planner.py`
- `/home/evgeny/projects/analyzer-v2/tests/test_adaptive_execution_target_normalization.py`
- a new focused executor test module if existing files are the wrong fit

### 3. Fresh rerun artifacts

After the repair, execute one fresh Phase 0 rerun again on the same fixed Otto target.

Required minimum evidence:

- launch artifact
- active-boundary artifact
- terminal proof that Phase `3.0` no longer fails with `prompt is too long`

If the rerun completes, continue the existing Phase 0 execution memo honestly.

If the rerun fails on a new seam, stop with a new revision memo instead of fabricating completion.

## Acceptance Criteria

This scope is successful only if one of these is true:

1. the repaired path survives Phase `3.0` on a fresh fixed-target rerun, and Phase 0 can continue honestly to completed-boundary and browser-proof work
2. the repaired path exposes a different bounded blocker, but the new seam is documented honestly with a revision memo and without reopening old host/browser work by inertia

This scope does not count as successful if:

- the only reason the run fits is that the fixed target was quietly weakened
- the repair simply suppresses too much evidence to make AOI sin findings honest
- the fix reopens unrelated host/browser or lifecycle work
- the provider still rejects the same path with the same prompt-budget failure

Implementation closeout must also record, at minimum:

- Phase `3.0` `document_text` chars before and after
- assembled shared-context chars before and after
- deep-pass count / shape used for Phase `3.0`
- whether the provider call was accepted
- whether the chosen repair was phase-specific only or reusable more broadly

## Status Implications

Until this slice lands and a fresh rerun clears Phase `3.0`:

- Phase 0 remains open
- Stage 2 remains open
- Tranche 3 remains blocked
- Phase 1 should not become the main implementation line yet
