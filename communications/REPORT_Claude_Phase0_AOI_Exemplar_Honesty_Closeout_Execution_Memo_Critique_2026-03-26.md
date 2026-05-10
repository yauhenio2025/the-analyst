# Report: Critique Of Phase 0 AOI Exemplar Honesty Closeout Execution Memo

Date: 2026-03-26
Reviewer: Codex
Primary document reviewed: `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md`

## Verdict

Approve after revision

## Executive Judgment

This is basically the right immediate Phase 0 artifact.

It is much better scoped than the earlier Stage 5 execution memo and it is directionally aligned with the current strategic order: finish the AOI exemplar honestly, write the Stage 2 decision, then move the main line to de-AOI / de-`the-critic` planner-to-presentation generalization rather than more AOI-only repair (`communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:114-170`, `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1132-1141`).

The memo also mostly stays out of Phase 1 design. Its main problem is not future-phase sprawl. Its main problem is that a few operational assumptions are still too loose for an honest closeout memo:

- the closure basis is compressed too aggressively
- the supposedly fixed corpus is not actually pinned tightly enough
- host-local `source_analysis_id` is treated too close to canonical truth
- the browser proof still needs one more anti-fallback artifact because the planner page exposes legacy/debug affordances in the same UI

## Strongest Findings

### 1. The memo under-specifies the closure basis and makes the Stage 2 decision too easy to collapse into “fresh rerun grade”

The memo is right that Phase 0 should close on the grade itself, not on whether the grade is flattering (`communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md:53-56`, `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:94-96`).

But the frozen rubric still says Stage 2 documentary closure requires three things together:

- the Stage 5 seam gate passes
- at least one ready case is `execution_backed` or stronger
- the combined evidence is strong enough to support repeated bounded AOI transient use

That is explicit in `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md:120-132`.

The new memo asks for one fresh rerun, one browser proof, and then one binary decision memo (`communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md:103-109`, `281-288`). That is close, but it no longer explicitly requires the closeout memo to restate:

- that the frozen four-case Stage 5 seam gate remains passed on carried-forward evidence
- that the fresh run is truly `execution_backed`
- that the combined baseline-plus-fresh evidence does or does not justify repeated bounded AOI transient use

The March 25 execution-backed plan did require those distinctions explicitly (`communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md:291-296`). This memo should keep them. Otherwise the closeout can become rhetorically binary while still being documentary-soft.

Revision needed:

- Require the final decision memo to state separately:
- Stage 5 seam gate status as carried-forward baseline evidence
- whether the fresh run is truly `execution_backed`
- whether the combined evidence supports repeated bounded AOI transient use
- then the Stage 2 verdict: `closure-grade exemplar achieved` or `bounded repaired proof only`

### 2. The “fixed target” is not fixed enough at the corpus boundary

The memo freezes project, thinker, task, workflow, and fixture strength (`communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md:58-80`). That is directionally correct and stabilizing.

But it only checks whether Otto texts exist and uploads the known local Otto PDF set if none exist (`communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md:173-185`).

That is too weak for this exact decision. The real launch route only blocks when zero texts exist:

- `POST /api/influence/thinkers/{thinker_id}/run-thematic-analysis-v2` refuses launch if no texts are present
- it does not verify that the present texts are the exact intended Otto corpus

See `/home/evgeny/projects/the-critic/api/server.py:14085-14095`.

The reference-text route can already enumerate the actual corpus inventory:

- `GET /api/influence/thinkers/{thinker_id}/texts`

See `/home/evgeny/projects/the-critic/api/server.py:12054-12095`.

For a memo whose whole point is “same Otto Neurath documents, fresh post-fix rerun,” “texts exist” is not enough. If unexpected extra texts, renamed uploads, or altered source-document assignments are already present in the project, the rerun stops answering the intended question.

Revision needed:

- Record the exact reference-text inventory before launch:
- filename
- original filename
- `source_document_id`
- text count
- If the inventory is not the expected Otto set, stop and write a revision memo instead of treating “some Otto texts exist” as sufficient.

### 3. The memo over-elevates `source_analysis_id` relative to the live host contract and the larger architecture

The memo requires both:

- `source_v2_job_id` preserved end to end
- host-boundary `source_analysis_id` preserved end to end

See `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md:250-256`.

That is slightly misleading relative to the live contract.

In Host Contract v1:

- `source_backed_transient_launch` is still `owner: 'host_proxy'`
- canonical identity is `upstream_v2_job_id`
- `source_analysis_id` and `source_v2_job_id` are explicitly described as optional continuity selectors, not hard launch requirements

See `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts:215-239`.

The live AOI panel and compose page also show the hierarchy:

- the panel plans against `source_v2_job_id` and carries `source_analysis_id` as host continuity context (`/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:595-637`, `686-717`)
- the compose page passes both to the host proxy on planner-backed launch (`/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:429-443`)
- the server then resolves or backfills identity and forwards only canonical `source_v2_job_id` upstream (`/home/evgeny/projects/the-critic/api/server.py:19192-19299`, `21532-21555`)

So yes, host-local alias continuity still matters for this bounded proof because recent bugs lived there. But no, it should not be phrased as co-equal truth with canonical upstream identity.

If the memo does that, it subtly centers Phase 0 on host-local alias discipline instead of analyzer-owned source identity. That is exactly the wrong architectural center of gravity for a program whose stated aim is “analyzer-v2 as the brain; downstream apps as thin hosts.”

Revision needed:

- State explicitly that `source_v2_job_id` is the canonical proof identity.
- Treat `source_analysis_id` as supporting host continuity evidence that must remain stable enough not to corrupt or misroute the proof, but not as primary analytical identity law.

### 4. The planner-primary browser proof still needs one more explicit anti-fallback artifact

The memo is correct to require planner-primary only:

- no legacy dossier/comparison fallback
- no profile/autostart shortcut as substitute

See `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md:241-265`.

That matches the real UI.

The AOI panel does the planner-primary path by:

- calling `routeTask(...)`
- calling `planTask(...)`
- carrying planner-selected sources and intent seed into `/compose-from-intent`

See `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:573-660`, `672-717`.

The compose page then has a real planner-backed `composeFromSelection(...)` path:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:414-449`

But the same page also still exposes:

- legacy/debug source-backed profile buttons on planner-backed launches
- autostart profile flow for `dossier` / `comparison`

See `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:368-412`, `452-477`, `612-659`.

So the memo is right to ban fallback branches, but the current artifact list is still slightly under-specified. HAR plus final response shell are not enough on their own to prove the operator did not use the on-page debug path.

Revision needed:

- Require one pre-submit compose-page artifact that shows:
- the planner-backed selection summary
- the selected/rejected source list
- the button used was `Compose planned AOI selection`
- Require that artifact before the compose request is fired, not only after the shell renders.

## What The Memo Gets Right

### 1. This is the right immediate Phase 0 vehicle

The memo is substantially aligned with the current roadmap order:

- Phase 0: one fresh post-fix AOI rerun and explicit Stage 2 decision
- then Phase 1: planner-to-presentation bridge generalization

See `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:114-170`, `337-360` and `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1128-1141`.

It is not trying to turn this slice into another Tranche 3 planning memo. That is good.

### 2. Its claims about the real Critic route are accurate

The memo is accurate that the fresh run should go through:

- `POST /api/influence/thinkers/{thinker_id}/run-thematic-analysis-v2`

That route exists and is the real AOI launch entrypoint. It checks thinker existence, verifies texts exist, and launches through the v2-backed genealogy path:

- `/home/evgeny/projects/the-critic/api/server.py:14062-14105`

It is also accurate that on this v2-backed path the returned Critic `job_id` is the upstream analyzer-v2 job id, not a distinct fresh local identity:

- `/home/evgeny/projects/the-critic/api/server.py:20299-20319`
- `/home/evgeny/projects/the-critic/api/server.py:20372-20379`

### 3. Its claims about the planner-primary path are accurate

The memo says the real browser proof should stay on the planner-primary branch. That is correct.

The live stack is:

- analyzer route boundary: `/v1/orchestrator/route-task` (`src/api/routes/orchestrator.py:301-318`)
- analyzer plan boundary: `/v1/orchestrator/plan-task` (`src/api/routes/orchestrator.py:321-338`)
- router outcomes are still bounded to AOI transient source-backed or genealogy job-backed (`src/orchestrator/task_router.py:387-428`)
- AOI planning produces `aoi_composition_handoff_plan` with followup contract `/v1/presenter/compose-from-selection` (`src/orchestrator/task_planner.py:533-583`)
- upstream compose still remains explicitly AOI- and `the-critic`-bounded (`src/presenter/compose_from_intent.py:496-560`)

So the memo’s operational picture of the current product path is honest.

### 4. It correctly treats inherited smoke scripts as supplemental only

The memo is right not to let inherited Stage 5 scripts substitute for the counted browser proof.

That caution matches the scripts themselves:

- `test-stage5-direct-poll-smoke.sh` mainly validates analyzer discovery/detail and optional host import/refresh/cache seams, not the full planner-backed compose proof (`/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh:169-266`)
- `test-stage5-aoi-landing-smoke.js` only verifies AOI landing/redirect, not planner-backed composition semantics (`/home/evgeny/projects/the-critic/test-stage5-aoi-landing-smoke.js:58-69`)

The memo’s “supplemental, not substitute” framing is therefore correct.

## Bigger-Picture Objective

The larger program objective remains:

- analyzer-v2 owns analytical understanding, routing, planning, and presentation law
- downstream apps become thin hosts rather than workflow-specific analytical controllers

That framing is explicit in:

- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:14-18`
- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md:10-15`

This memo mostly preserves that objective because it tries to make AOI the last bounded honesty gate instead of another long AOI branch.

The remaining risk is subtler than “it contains future-phase prose.” The real risk is:

- leaving corpus identity too loose
- centering host alias continuity too strongly
- allowing a browser proof that is still vulnerable to same-page fallback ambiguity

If those remain, Phase 0 can still end up as another AOI/the-critic ritual rather than a clean last gate before de-AOI / de-`the-critic` generalization.

If those are tightened, the memo becomes a proper closeout instrument rather than another AOI sink.

## Bottom Line

This is the right immediate Phase 0 vehicle, but not yet strict enough to be the final execution memo as written.

Approve after revision.

The revisions should be narrow:

- explicitly carry forward the frozen Stage 5 seam-gate basis in the decision memo
- pin the exact Otto corpus, not just text existence
- demote `source_analysis_id` to supporting continuity evidence under canonical `source_v2_job_id`
- require one explicit pre-submit planner-backed compose-page artifact so the no-fallback claim is documentary, not inferred

With those changes, the memo would support an honest Phase 0 closeout while still protecting the larger objective that analyzer-v2 becomes the intelligence layer and downstream apps remain thin hosts.
