# Memo: Close Read Concept-Analysis Logical Execution Completion Stall Closure Scope

Subtitle: Supersede the readback-first diagnosis by closing the fresh logical execution stall on the admitted logical seam before rerunning final host readback and scrutiny proof

Date: 2026-04-07
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Close Read Roadmap Context:
- `communications/MEMO_2026-04-04_close_read_roadmap_recalibration.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- `communications/MEMO_2026-04-06_close_read_roadmap_update_after_live_concept_authority_cutover.md`
Immediate Scope Predecessor:
- `communications/MEMO_2026-04-07_close_read_concept_analysis_logical_readback_and_scrutiny_closure_scope.md`
Immediate Architectural Predecessor:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_translated_artifact_authority_scope.md`
Relevant Completion Context:
- `communications/MEMO_2026-04-06_close_read_concept_analysis_live_authority_and_thin_client_cutover_completion.md`
Primary Live Evidence:
- `https://the-critic.onrender.com/api/concept/jobs/concept-1775529506826-c585ea`
- `https://the-critic.onrender.com/api/projects/cutover-logical-readback-closure-20260407-023428/documents`
- `https://the-critic.onrender.com/api/concept/analyses/innovation?analysis_type=logical`
- `https://analyzer-v2.onrender.com/v1/executor/jobs/job-plan-936b5b61e93f`
Primary Code Evidence:
- `/home/evgeny/projects/analyzer-v2/src/orchestrator/concept_by_ref.py`
- `/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py`
- `/home/evgeny/projects/analyzer-v2/src/executor/workflow_runner.py`
- `/home/evgeny/projects/analyzer-v2/src/workflows/definitions/concept_logical_single_concept.json`
- `/home/evgeny/projects/analyzer-v2/src/chains/definitions/concept_analysis_12_phase.json`
- `/home/evgeny/projects/the-critic/api/server.py`

## Purpose

Supersede the earlier April 7 readback-first scope with the live reality now visible after the deployed host persistence fix:

- the-critic no longer falsely marks the fresh logical job completed while readback is empty
- the fresh proof project is real and has no logical persisted result yet
- the active blocker is that the backing analyzer-v2 logical run is still in-flight or stalled upstream

So the next bounded tranche is:

1. close the fresh logical execution completion stall in analyzer-v2
2. rerun the fresh logical proof on the same admitted seam
3. only then re-evaluate host readback and scrutiny closure

This tranche is not about new concept capability or new host design.

## Bottom Line

The earlier April 7 memo was reasonable from the first failed specimen, but it is no longer the best active diagnosis.

The newly deployed host behavior shows something more precise:

- fresh logical concept job on the-critic remains `running`
- fresh logical readback remains `404`
- backing analyzer-v2 logical job is also still `running`
- therefore the host readback path is not yet the operative blocker on the current fresh specimen

The exact live specimen is:

- project: `cutover-logical-readback-closure-20260407-023428`
- critic logical job: `concept-1775529506826-c585ea`
- analyzer-v2 logical job: `job-plan-936b5b61e93f`

Current live state:

- the-critic job remains `running`
- analyzer-v2 job remains `running`
- analyzer-v2 progress detail has advanced as far as `Engine 12/12: concept_synthesis`
- `GET /api/concept/analyses/innovation?analysis_type=logical` still returns `404`
- this is expected while no completed persisted logical result exists

So the next honest gap is:

- analyzer-v2 logical completion stall or extreme-duration behavior on a tiny fresh proof corpus

not:

- host-side silent persistence swallow
- host-side false-completed readback closure

## What Is Already True

### 1. The host persistence correctness bug is closed

The deployed the-critic now fails closed on concept-analysis DB persistence errors.

That means the host should now do one honest thing or the other:

- complete and persist a logical result, or
- fail the job explicitly

The fresh specimen is currently doing neither because the upstream analyzer-v2 run has not yet completed.

### 2. The fresh proof project is valid

The current fresh project has real uploaded documents and no existing logical result:

- subject + response documents are present
- logical readback remains empty

So the proof surface is still usable for completion-stall diagnosis, even if the duplicate uploads make it less ideal as the final certification corpus.

### 3. The logical seam is now blocked before readback

The host and analyzer-v2 job states agree:

- both still report `running`
- the host is not fabricating a completed logical result
- no persisted logical result exists yet

That narrows the active diagnosis upstream to analyzer-v2 execution completion.

## Scope Summary

Implement one narrow completion-stall tranche:

1. trace the live fresh logical run through analyzer-v2 execution state, especially the tail end of `concept_logical_single_concept`
2. determine why the run remains in `running` on a tiny two-document corpus
3. fix the analyzer-v2-side completion stall or extreme-duration issue
4. rerun the fresh logical proof to true completion
5. only after true completion, verify host readback and then scrutiny readback on the same fresh project or on one final clean replacement project

## Key Decisions To Freeze

### 1. Do not reopen the host persistence fix first

The host save-path correction has already been deployed and the current live specimen no longer exhibits the original silent-success symptom.

Do not start by adding more the-critic persistence/readback code unless the analyzer-v2 job genuinely completes and the host still fails afterward.

### 2. Treat analyzer-v2 execution completion as the default diagnosis

The default assumption should now be:

- analyzer-v2 launch works
- analyzer-v2 translation path is configured
- the run is stalling or taking pathologically long inside the logical workflow/chain

Only after direct trace evidence should this widen to:

- executor state-machine bug
- transformation handoff bug at completion boundary
- host fetch/readback bug after true upstream completion

### 3. Keep the seam bounded to `logical`

Inferential remains out of scope unless a discovered analyzer-v2 executor bug is clearly shared across both admitted modes.

### 4. Preserve the architectural corridor

This tranche is still subordinate to the broader corridor frozen in the April 6 roadmap update:

- analyzer-v2 as runtime authority
- then analyzer-v2 as translated artifact authority
- then thinner host posture

Do not let this stall fix drift into:

- new concept submodes
- analyzer-mgmt redesign
- broader Close Read host work
- generic executor refactors beyond what the logical stall strictly requires

### 5. Use live evidence as the primary truth source

The active diagnosis should be grounded first in the live specimen:

- `concept-1775529506826-c585ea`
- `job-plan-936b5b61e93f`

and only secondarily in local source inspection.

## Implementation Sequence

### Phase 1: Trace the current live logical stall end to end

Use the current specimen:

- project `cutover-logical-readback-closure-20260407-023428`
- critic job `concept-1775529506826-c585ea`
- analyzer-v2 job `job-plan-936b5b61e93f`

Trace:

- executor job status
- per-engine or per-phase progression if available
- last successful engine boundary
- whether `concept_synthesis` itself is slow, looping, retrying, or blocked
- whether the workflow is waiting on transformation/extraction completion that never finalizes

This phase should end with one explicit root-cause statement.

### Phase 2: Repair the analyzer-v2 completion stall

Fix only the identified analyzer-v2-side seam.

Likely surfaces include:

- logical workflow wrapper
- chain execution boundary
- synthesis step
- workflow runner completion semantics
- transformation-at-end handoff

Do not change host code unless the trace proves the host is the active blocker after true upstream completion.

### Phase 3: Rerun fresh logical proof

After the analyzer-v2-side fix:

1. rerun fresh logical on the current project if the corpus is still usable, or
2. create one final clean project with exactly one subject doc and one response doc if duplicate documents make the current project unsuitable for certification

Record:

- critic logical job id
- analyzer-v2 logical job id

Require:

- analyzer-v2 job reaches `completed`
- the-critic job reaches `completed`
- `GET /api/concept/analyses/:concept` returns the fresh logical result
- persisted logical result carries `_analysis_provenance.execution_owner == "analyzer-v2"`

### Phase 4: Scrutiny closure only after true logical completion

Only once fresh logical completion and readback are real:

- launch one fresh logical scrutiny run
- verify scrutiny result persistence/readback

If scrutiny still fails after true logical completion, scope a final tiny scrutiny-specific closure slice.
Do not assume scrutiny is the active blocker before logical completion exists.

## Public Interfaces / Behavioral Expectations

No new user-facing routes are required by default.

The target behavioral outcome is:

- logical jobs should either complete or fail honestly
- they should not remain indefinitely `running` on a tiny fresh proof corpus
- once completed, host readback should resume its existing contract without further redesign

## Test Plan

### 1. Live-stall diagnosis

Using the current specimen:

- verify analyzer-v2 job state progression
- identify the exact last live engine/phase boundary
- confirm whether the stall is inside logical execution or between logical execution and translated artifact finalization

### 2. Focused local regression tests

Add or update only the narrow tests needed to prove the repaired completion path.

That may include:

- logical workflow completion on a minimal corpus
- completion-state transition after synthesis
- end-of-workflow artifact finalization if that is the failing seam

### 3. Fresh hosted proof

On a fresh clean project:

- launch logical
- wait for true completion
- verify logical readback
- verify analyzer-v2 provenance on the persisted result
- then launch scrutiny
- verify scrutiny readback

## Out Of Scope

This tranche should not include:

- inferential changes unless forced by a clearly shared executor bug
- analyzer-mgmt UI work
- concept host-contract redesign
- broader translated artifact authority redesign
- Close Read UI changes
- new concept families or submodes

## Roadmap Implication

The near-term corridor should now read:

1. live authority and thin-client posture: materially established
2. host persistence correctness: materially corrected
3. fresh logical execution completion stall on analyzer-v2: immediate blocker
4. then final logical readback + scrutiny closure proof
5. then resume the broader translated-artifact-authority corridor

So the next serious move is not another host-side patch by default.
It is:

- **close the analyzer-v2 logical completion stall on the fresh proof corpus**

Only after that should the program return to the broader architectural corridor of making analyzer-v2 the full translated-artifact authority.
