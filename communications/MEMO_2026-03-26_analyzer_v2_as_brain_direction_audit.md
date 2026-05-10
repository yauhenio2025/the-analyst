# Memo: Analyzer-v2 As The Brain Direction Audit

Date: 2026-03-26
Status: Strategic audit of current direction
Program: Dynamic Bespoke Apps Platformization
Audience: Human decision-makers, future Claude sessions, future Codex sessions, cross-repo implementors

## Purpose

Assess whether the recent tranche of work is actually moving the program toward the stated end state:

- analyzer-v2 owns analytical understanding, routing, planning, sequencing, and presentation law
- downstream apps such as `the-critic` act mainly as thin hosts
- host apps render analyzer-owned decisions and content instead of reconstructing analytical meaning locally

This memo reviews:

- the canonical roadmap
- the current draft roadmap
- recent completion and scope memos
- the relevant analyzer-v2 and the-critic code seams
- the visible git history

## Executive Judgment

The current direction is coherent, but only partially convergent with the ultimate vision.

The honest read is:

- recent work has genuinely moved important bounded decisions upstream into analyzer-v2
- recent work has also retired a long sequence of real AOI exemplar blockers
- but most of that progress is still inside one bounded AOI / `the-critic` exemplar gate
- the program is not yet at the point where external apps can honestly be described as mostly thin shells for analyzer-owned analytical decisions

So the answer is:

- yes, the work is directionally correct
- no, the work is not yet sufficient to claim the full “analyzer-v2 is the brain” architecture has been achieved

If the program continues doing only AOI / `the-critic`-specific blocker retirement after the required fresh post-fix execution-backed rerun, it risks hardening into a stronger downstream presenter rather than the intended host-neutral intelligence layer.

## What Has Genuinely Moved Upstream

The recent record does contain real upstream movement.

### 1. Analyzer-v2 now owns bounded task routing and bounded planning

This is not a prose claim only. The analyzer now exposes real orchestration seams:

- `POST /v1/orchestrator/route-task`
- `POST /v1/orchestrator/plan-task`

Those routes are live in `src/api/routes/orchestrator.py`.

The routing layer in `src/orchestrator/task_router.py` now decides, in bounded form:

- whether a task should follow AOI transient source-backed handling
- whether a task should follow genealogy job-backed execution
- which downstream launch contract the host should follow

The planning layer in `src/orchestrator/task_planner.py` now owns real AOI composition-handoff decisions:

- source-family selection
- allowed/blocked profile law
- handoff notes
- compose followup contract

That is genuine upstream intelligence, not just better host wiring.

### 2. Analyzer-v2 now owns bounded readiness and bounded compose contracts

The presenter/orchestrator side now owns:

- source-backed readiness
- bounded transient compose contracts
- analyzer-side selection-backed composition handoff

This is real progress toward the target architecture because the host is no longer supposed to decide which analytical source families or profiles make sense on its own.

### 3. Host Contract v1 is a meaningful upstream/downstream clarification

The Stage 13 work is materially important.

`communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md` and `the-critic/webapp/src/lib/hostContractV1.ts` show that the program now has an explicit, typed statement of:

- which families are analyzer-direct
- which families are host-proxy
- what identities are authoritative upstream
- where local continuity aliases are still tolerated

That is real architectural consolidation. It makes the thin-host claim inspectable instead of rhetorical.

### 4. The-critic now asks analyzer-v2 for bounded routing/planning truth in live seams

The Stage 8/9 host-adoption tranche is also real progress.

`communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md` plus `the-critic/webapp/src/lib/taskLaunchRuntime.ts` show that the-critic now calls analyzer-owned:

- `route-task`
- `plan-task`

in at least two real seams:

- AOI planner-backed handoff
- genealogy registered-corpus task-planned execution

This is not the whole vision, but it is exactly the kind of change that should exist if analyzer-v2 is actually becoming the brain.

### 5. The recent Stage 5 repair chain was not fake work

The long Stage 5 chain did not generalize the whole platform, but it did retire real blocker classes that had to be retired:

- durability / local snapshot truth
- selection-compose contract failures
- host-side idempotence and browser-source pinning
- AOI source-content identity contamination

Those were necessary if the AOI exemplar was going to be an honest proving ground instead of a paper proof.

## What Is Still Host-Owned

This is the most important limiting fact.

The host is thinner than before, but it still knows too much.

### 1. Source identity resolution and continuity alias handling still live in the host path

Host Contract v1 explicitly records this.

In `the-critic/webapp/src/lib/hostContractV1.ts`:

- `source_backed_transient_launch` is still `owner: 'host_proxy'`
- `cache_snapshot_warmup` is still `owner: 'host_proxy'`
- the notes explicitly say the host resolves project/thinker-scoped identity before forwarding source-backed transient compose

That means the host still owns part of the identity-resolution bridge between analyzer truth and local continuity truth.

### 2. AOI page sequencing and navigation are still page-local host logic

`the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx` still owns:

- saved-result loading and row selection
- explicit `routeTask(...)` and `planTask(...)` invocation timing
- AOI-specific blocked-state handling
- `warmSnapshotForSource(...)`
- navigation into `/compose-from-intent`
- planner-selected-source handoff through navigation state

That is better than fully local planning, but it is not yet “the app just renders analyzer decisions.”

### 3. Surface selection still lives in host-owned rules

Host Contract v1 explicitly encodes host surface-selection rules.

That is acceptable for a bounded v1 contract, but it is still host ownership.

The target end state says apps should provide routing and a place to render, not decide analytical surface semantics. The current system is not there yet.

### 4. Task-launch adoption sits beside Host Contract v1 instead of fully inside it

The draft roadmap says this explicitly, and it is correct.

The host has:

- Host Contract v1
- task-launch adoption

but those two stories are not yet one fully unified host-neutral contract story.

That matters because it means the system still has two adjacent pieces of truth rather than one coherent analyzer-to-host lifecycle law.

## What Is Accidental AOI / The-Critic Coupling

This is the strongest evidence that the program is not yet at the generalized platform stage.

### 1. Transient compose is still structurally AOI-bound

`src/presenter/compose_from_intent.py` still hard-restricts:

- `workflow_key == AOI_WORKFLOW_KEY`
- `consumer_key == TRANSIENT_COMPOSE_CONSUMER_KEY`

for:

- `compose-from-intent`
- `compose-from-source`
- `compose-from-selection`

That means the transient composition substrate is still not generalized presentation law. It is bounded AOI law with a thin analyzer-owned interface.

### 2. Transient compose is still structurally bound to `the-critic`

The same validator path in `src/presenter/compose_from_intent.py` hard-locks `consumer_key` to the-critic.

So even where composition has moved upstream, it is still upstream logic shaped around one specific consumer.

That is acceptable for a proving tranche, but it is not the final architecture.

### 3. Task routing outcomes are still bounded to AOI and genealogy

`src/orchestrator/task_router.py` currently resolves supported outcomes into a small fixed family:

- AOI transient source-backed handoff
- genealogy analyze-by-ref
- genealogy inline analyze

That is real planning substrate, but it is not yet general task-to-workflow intelligence across multiple downstream app experiences.

### 4. AOI handoff metadata is still not reusable composition law

The AOI planner handoff is currently rich and useful, but it remains AOI-shaped:

- selected source families
- allowed/blocked AOI profiles
- AOI-specific selection semantics

That is a strong bounded bridge, but it is not yet the general planner-to-presentation bridge described in the broader roadmap.

### 5. The-critic still knows it is on an AOI page

This is not just incidental UI code.

The host still contains AOI-specific:

- source constraints
- blocked-state display logic
- planner-backed launch sequencing
- saved-result interpretation
- navigation semantics

That is exactly the class of app-specific intelligence the end-state wants to move upstream or reduce sharply.

## What The Commit History Suggests

The visible `git log` is not the best record of the current strategic movement.

The recent head history is noisy and still reads largely as:

- renderer polish
- AOI canary styling
- presenter fixes
- older AOI consumer work

It does not tell the recent Stage 8/9, Stage 13, and late Stage 5 tranche story cleanly.

That means:

- the communications ledger is currently more authoritative than git history for understanding the current strategic arc
- the program is still in an active proving-and-revision phase rather than a cleanly consolidated product/platform phase

This is not a disaster, but it is a warning sign: if the strategic story only lives in memos and not eventually in a cleaner code/commit topology, the program will become harder to reason about honestly.

## What Must Happen Next If Analyzer-v2 Really Is The Brain

The immediate next operational step remains unchanged:

- run the fresh post-fix execution-backed AOI rerun on the same Otto Neurath documents
- write the Stage 2 decision honestly from that result

But strategically, that is not enough.

If analyzer-v2 is really meant to become the brain, the next non-optional program move after that rerun is Tranche 3 style generalization work.

### 1. De-AOI the transient composition substrate

The compose pipeline cannot remain hard-bound to AOI-only request validation if it is meant to become reusable presentation law.

The next work has to separate:

- bounded AOI-specific materialization logic
- generic composition-entry contracts
- generic planner-to-presentation law

### 2. De-the-critic the transient consumer contract

The current `consumer_key == the-critic` lock is acceptable as a tranche guardrail.

It is not acceptable as the long-term architecture.

At least one second consumer or neutralized consumer contract has to prove that transient composition is not secretly just “analyzer-owned the-critic support code.”

### 3. Prove one non-AOI composition-facing seam

The roadmap is already correct on this.

Without one non-AOI composition-facing proof, the program cannot honestly claim that the planner-to-presentation bridge is general rather than AOI-special.

### 4. Unify task-launch and host-contract stories

The system needs one coherent story for:

- route
- plan
- readiness
- launch
- result discovery
- result presentation
- transient composition

Right now those pieces are adjacent and improving, but they are not yet one clean host-neutral lifecycle law.

### 5. Keep host obligations minimal and explicit

The host should end up owning only stable obligations such as:

- auth
- project shell
- routing shell
- thin transport/proxy where unavoidable
- user input capture
- rendering analyzer-owned results

The host should not continue owning:

- analytical source resolution semantics
- AOI-specific launch law
- workflow-specific surface meaning
- hidden continuity-repair behavior that reintroduces app-local analytical expectations

## Final Strategic Call

The program is not drifting randomly.

It is building the right downstream half first:

- stronger analyzer-owned planning seams
- stronger analyzer-owned presentation seams
- thinner consumer runtime behavior
- more explicit host contracts

But it is still only a bounded proof of the bigger thesis.

The most honest current statement is:

- analyzer-v2 is increasingly telling the host what to do
- analyzer-v2 is not yet the fully generalized brain for dynamic bespoke analytical apps

That distinction matters.

If the program uses the next post-fix AOI rerun as the last major AOI-specific gate before de-AOI / de-the-critic bridge generalization, then the current work is a strong foundation for the real vision.

If the program keeps spending the next rounds only on AOI / `the-critic` local refinements, then the architecture will drift toward a better downstream AOI presenter instead of the intended multi-app analyzer-owned intelligence layer.

