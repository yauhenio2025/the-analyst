# Audit: Phase 0 AOI Sin-Findings Prompt-Budget Revision Scope

## Findings

### 1. Critical: the memo diagnoses the right seam family, but it leans on the wrong authoritative March 27 plan artifact

The memo treats `src/orchestrator/plans/plan-54b6f075fdf2.json` as if it were the failed live plan shape. That file shows only five phases and no `1.5` source-work profiling phase (`src/orchestrator/plans/plan-54b6f075fdf2.json:57-188`). But the actual failed March 27 job `job-226f65f43a3b` stored in local `src/executor/executor.db` used a six-phase `plan_data` with:

- `0.5` Target Work Profiling
- `1.0` Source Thematic Synthesis
- `1.5` Source Work Profiling
- `2.0` Engagement Mapping
- `3.0` AOI Sin Findings
- `4.0` Thematic AOI Report

That stored `plan_data` also makes `1.0` depend on `1.5`, and the same job persisted 20 `phase_outputs` rows for `1.5`. So the live failed run had already incorporated a planning-side source-profiling mitigation before it hit the prompt-budget stop.

Why this matters:

- `plan-12e3db25fb90` is still relevant precedent, but it is not merely a historical analogy.
- The live March 27 run had already moved in that same direction and still failed at `3.0`.
- The memo should therefore ground its diagnosis first in executed `executor_jobs.plan_data` plus live `phase_outputs`, then use `plan-12e3db25fb90` as corroborating precedent.

Without that revision, the memo slightly overstates how much of the planning/config seam is still only hypothetical.

### 2. Critical: the actual failing Phase 3 contract is “full target + full source corpus + all pass-level upstream prose,” not merely “the provider disliked a long prompt”

The current executor contract for Phase `3.0` is materially broader than the memo states.

What the code actually does:

- `_get_standard_phase_document_text()` concatenates the full target corpus and the full selected-source corpus for Phase `3.0` (`src/executor/phase_runner.py:827-883`).
- `load_outputs_for_context()` loads all saved outputs for upstream phases, ordered by `phase_number, pass_number`, not just each phase's final output (`src/executor/output_store.py:137-176`).
- `assemble_phase_context()` then formats every returned block and truncates each one at the default `50_000` chars (`src/executor/context_broker.py:20-29`, `src/executor/context_broker.py:59-105`).
- `chain_runner` injects that entire assembled context into the system prompt and passes the entire phase document bundle as the user message (`src/executor/chain_runner.py:328-383`).

Measured locally on the failed job `job-226f65f43a3b`:

- Phase `3.0` `document_text`: `3,901,990` chars
- Assembled upstream context from Phases `1.0` and `2.0`: `250,836` chars
- All five upstream outputs were over `50,000` chars, so the broker hit the cap on every block
- Reconstructed Phase `3.0` pass-1 prompt shape: about `4,160,195` chars total, roughly `1.04M` tokens by the repo's own char-to-token heuristic

That reconstruction is directionally consistent with the proof artifact's exact provider rejection:

- `prompt is too long: 1037154 tokens > 1000000 maximum`
- See `communications/PROOF_phase0_aoi_execution_backed_after_active_discovery_repair_terminal_failure_2026-03-27.json`

So the memo should say explicitly that the dominant live contract is:

- all target text
- all selected-source text
- all pass-level outputs from Phase `1.0`
- all pass-level outputs from Phase `2.0`

That is a stronger and more honest formulation than “Phase 3 prompt budget overflow” alone. It also means the repair locus cannot be framed as prompt-text trimming only. It has to include one or more of:

- upstream context assembly
- Phase `3.0` document shaping
- pass-level staging / narrowing

### 3. High: hidden multi-pass amplification is real and should be named as part of the seam, not left implicit

The memo gestures at engine input contract and full-document settings, but it does not say clearly enough that deep `aoi_sin_findings` is a three-pass phase:

- deep depth runs `discovery -> inference -> integration` (`src/operationalizations/definitions/aoi_sin_findings.yaml:54-67`)
- later passes consume earlier pass outputs (`src/operationalizations/definitions/aoi_sin_findings.yaml:59-67`)
- `chain_runner` re-injects the full upstream shared context on every pass and then adds inner-pass context on top (`src/executor/chain_runner.py:313-360`)

The March 27 provider rejection happened on pass `1`, so the run never reached passes `2` and `3`. But the code path makes those later passes strictly at-risk as well. A narrow pass-1-only fix could still leave the deep path unstable.

The memo should therefore require one of these explicitly:

- pass-aware prompt budgeting across all Phase `3.0` passes
- a shallower/staged Phase `3.0` execution shape
- a contract that narrows what later passes inherit

Otherwise the scope remains slightly too vague about where the real budget pressure lives.

### 4. High: the memo is correct that the blocker is Phase `3.0`, not Phase `4.0`, but it misses the execution-law bug that creates the misleading `4.0` alias

The memo is right to reject `progress.current_phase = 4.0` as the seam locator. But the reason is deeper than a documentary alias.

The executor currently keeps running later phase groups even after an earlier phase fails:

- `_build_execution_order()` builds later groups from declared dependencies before any results exist (`src/executor/workflow_runner.py:550-613`)
- the main execution loop does not stop when a phase fails; it marks the job failed only after all groups finish (`src/executor/workflow_runner.py:353-366`)

That matches the live March 27 job state:

- local `executor_jobs.phase_results` show `3.0 = failed`
- the same job also shows `4.0 = completed`
- the failure proof artifact still reports the real cause at `3.0 / aoi_sin_findings / Finding Discovery`

Implications:

- the memo is still correct about the real blocker
- but post-failure Phase `4.0` artifacts are not trustworthy seam evidence
- this adjacent execution-law issue should be named explicitly so closeout does not accidentally lean on downstream synthetic report output after a core analytical phase already failed

I would not widen this slice into a general workflow-runner repair by default. But the memo should explicitly quarantine post-`3.0` artifacts from seam diagnosis.

### 5. Medium: the memo rightly asks for fail-fast budget law, but it should tighten the regression story and separate the real blocker from adjacent drift

The fail-fast claim is technically sound:

- `engine_runner` only converts `prompt is too long` into a terminal error after the provider rejects the call (`src/executor/engine_runner.py:295-304`)
- document chunking is effectively disabled via `CHUNK_THRESHOLD = 999_999_999` (`src/executor/engine_runner.py:92-99`, `src/executor/engine_runner.py:316-359`)

The testing story is not yet commensurate with the proposed seam:

- the named tests cover discovery/result contracts and plan-key normalization
- they do not cover context assembly shape, budget preflight, or “do not run downstream phase after failed dependency”

One adjacent drift item exists but does not look causal for this failure:

- the model labels are slightly misleading because both `"opus"` and `"sonnet"` currently resolve to `claude-sonnet-4-6` (`src/executor/engine_runner.py:49-61`)

That label drift is worth cleaning up eventually, but it does not explain the March 27 overflow. The prompt-volume evidence already explains it.

## Verdict

Approve with revisions

## Direct Answers

### 1. Is this now the right next honest step?

Yes.

The codebase and proof artifacts support the memo's larger directional claim:

- discovery was repaired and proven on the fresh March 27 run
- the fresh run reached the real analyzer execution path
- the provider stop is now in `Phase 3.0 / aoi_sin_findings / Finding Discovery`
- I do not see evidence that more host/browser or thinker-discovery work is the honest next move

So the next honest move is a bounded analyzer-side prompt-budget repair on the fixed Otto target, followed by a fresh rerun.

### 2. Is the real blocker Phase `3.0`, not Phase `4.0`?

Yes, with one important caveat.

The real blocker is definitely Phase `3.0`. The `4.0` signal is downstream contamination caused by the current workflow runner continuing after a failed dependency phase. The memo is substantively right about seam location, but it should name this adjacent execution-law problem explicitly.

### 3. Is the fixed-target rule technically sound and honestly sequenced?

Yes.

The roadmap and the March 26/27 memos are aligned that Phase 0 must close honestly on the fixed Otto `evolution_ready` case before Phase 1 becomes the main line. The memo is also right not to weaken project, thinker, task, or corpus boundaries to make the run cheaper.

### 4. Are the memo's likely seam families real and well-bounded?

Mostly yes.

These seam families are real:

- plan shape / plan-generation law
- upstream context assembly
- full-document execution settings
- Phase `3.0` engine input contract
- missing fail-fast budget guard

Two additional adjacent seam families should be named explicitly:

- all-pass upstream-context amplification
- downstream phase execution after failed dependencies

### 5. Is `plan-12e3db25fb90` relevant enough to justify treating planning/config as part of the seam?

Yes, but it should not be the memo's primary evidence.

`plan-12e3db25fb90` is a valid precedent because it explicitly recognized the same Neurath corpus-scale problem and inserted profiling to stay within practical context limits (`src/orchestrator/plans/plan-12e3db25fb90.json:57-107`).

But the stronger evidence is the live March 27 job itself: its stored `plan_data` already introduced a `1.5` source-work profiling phase and still failed at `3.0`. That makes planning/config part of the seam even without the older precedent.

### 6. Is the memo missing any deeper or adjacent seam?

Yes.

These are real and currently undernamed:

- duplicate document loading
- over-large capability prompt context
- hidden multi-pass amplification
- downstream execution continuing after a failed dependency

I do not see a standalone analyzer/provider configuration mismatch as the main causal seam for March 27. The failure is already explained by the assembled prompt volume. The `"opus"`/`"sonnet"` label drift is real, but secondary.

### 7. Does the memo keep Stage 2 / Phase 1 sequencing honest?

Yes.

It correctly refuses to reopen host/browser work by inertia, and it correctly refuses to pivot into Phase 1 bridge generalization before Phase 0 is closed honestly.

### 8. Is the scope technically bounded and implementation-worthy?

Yes, but not as written.

It becomes implementation-worthy once revised to name the actual live contract precisely. As written, it is still slightly too vague about whether the repair is expected to land in:

- context assembly
- Phase `3.0` document shaping
- pass-level staging
- or some combination

My best technical judgment is that a purely cosmetic prompt-text trim is unlikely to be enough. The measured live volumes suggest the real repair will probably need at least a combination of:

- stricter upstream-context narrowing
- and narrower Phase `3.0` source/target input shaping

That is an inference from the live job measurements, not a directly executed counterfactual.

### 9. Does the memo force an explicit enough closeout on where the real seam lived after implementation?

Not yet.

It is close, but the closeout should require measured before/after prompt-shape evidence, not just a narrative answer.

## Recommended Memo Revisions Before Execution

1. Replace the memo's March 27 plan-shape evidence with the executed `executor_jobs.plan_data` and `phase_outputs` for `job-226f65f43a3b`.

2. State explicitly that the live failed run already had a `1.5` source-work profiling phase, so the diagnosis is not “we have not tried planning/config mitigation yet.” It is “we tried one planning-side mitigation and the live Phase `3.0` contract is still too large.”

3. Add one concrete description of the current failing Phase `3.0` contract:
   full target corpus + full Otto source corpus + all pass-level outputs from Phases `1.0` and `2.0`, with the deep `aoi_sin_findings` operationalization repeating that shared context across multiple passes.

4. Add one explicit caveat that current Phase `4.0` artifacts after a Phase `3.0` failure are downstream contamination from executor behavior and must not be used to relocate the blocker.

5. Tighten the “likely repair shapes” section so it says the slice may repair:
   context assembly only,
   document shaping only,
   pass sequencing/depth only,
   or a minimal combination of those.
   It should also say that a prompt-text-only edit is not presumed sufficient.

6. Strengthen the acceptance criteria so implementation closeout records at least:
   `document_text` chars before and after,
   assembled shared-context chars before and after,
   pass count / depth used for Phase `3.0`,
   whether the provider call was accepted,
   and whether the fix was phase-specific or reusable.

7. Require at least one regression for pre-provider budget failure and one regression for context-assembly narrowing.

8. Optionally, but preferably, record the adjacent workflow-runner dependency-failure issue as explicitly out-of-slice unless the repair work touches execution gating anyway.
