# Audit: Phase 0 AOI Exemplar Honesty Closeout Execution Memo

Date: 2026-03-26
Auditor: Claude (Codex-role audit)
Document under review: `communications/MEMO_2026-03-26_phase0_aoi_exemplar_honesty_closeout_execution_memo.md`

## Verdict

**Approve with revisions**

The memo is the right immediate Phase 0 artifact. It is well-bounded, operationally specific, and correctly refuses to widen into repair or strategic redesign. The codebase claims are accurate where they can be verified. Two findings require revision before execution; the remainder are advisory improvements that would make the proof more robust but are not blocking.

---

## Findings (ordered by severity)

### Finding 1 — MEDIUM: The rubric application is narrowed to a single ready case without acknowledging the rubric's full case-set expectation

The frozen rubric (`MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`) defines four required cases:

1. `evolution_ready`
2. `engagement_ready`
3. `non_profile_ready`
4. `selection_blocked`

and states that the Stage 5 seam gate passes only if **every** case passes `operational_behavior` and every ready case passes `selection_fit` / `rendered_usefulness`.

The Phase 0 memo scopes to one fresh post-fix rerun and one counted browser proof without naming which case that rerun represents. By implication this is `evolution_ready` (the fixed task text — "Show how Aaron Benanav's use of Otto Neurath's planning argument evolves across the corpus" — matches the evolution_ready definition). But the memo does not explicitly say so.

More importantly, the memo's Step 6 says "grade at minimum: selection_fit, rationale_clarity, rendered_usefulness, operational_behavior" — which is the correct set for a single ready case. But the rubric's Stage 2 documentary closure gate requires:

- at least one ready case is `execution_backed` or stronger
- the Stage 5 seam gate passes (which requires all four cases)

So the memo's "closure-grade exemplar achieved" outcome could only honestly mean "the execution-backed evolution_ready case itself is closure-grade." It cannot mean the full Stage 5 seam gate has passed, because the other three cases are not being re-run.

**Revision needed**: The memo should explicitly state:
- This is the `evolution_ready` case only.
- The Stage 2 decision from this memo is bounded to the evidence this one fresh case generates plus the pre-existing fixture-backed pack results for the other three cases.
- The closure/non-closure judgment should be framed accordingly — it either upgrades the evolution_ready case to execution-backed within the already-passed fixture pack, or it does not. It does not independently satisfy the full rubric's four-case requirement.

### Finding 2 — MEDIUM: The memo assumes the reference-text upload route is multipart but does not specify the exact contract

Section "Preflight Contract §5" says:

> If no texts exist, upload the known Otto PDF set from:
> `/home/evgeny/projects/the-critic/others/influences/otto-neurath/`

But does not specify the exact upload route, expected content-type, or how many files are expected. This was identified as a known blocker in the older proof plan (`MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`, §Preflight step 7) which noted:

> On the default local SQLite fallback, uploaded reference text count is `0`

The Critic backend's upload route (`POST /api/influence/thinkers/{thinker_id}/texts`) expects multipart file upload. The memo should preserve the older proof plan's specificity here rather than leaving the upload path underspecified, because a failed upload silently becomes a Closeout C (invalid attempt) instead of the intended Closeout A or B.

**Revision needed**: Add the exact upload route and a note that the executor should verify the text count is nonzero after upload before proceeding to Step 1.

### Finding 3 — LOW: The "Fixed Target" task text is correct but should be cross-referenced to the rubric case name

The memo's fixed task text:

> `Show how Aaron Benanav's use of Otto Neurath's planning argument evolves across the corpus.`

This is the same text used in prior proof runs. It matches the `evolution_ready` case shape. Explicitly naming the rubric case would make the grading step less ambiguous.

### Finding 4 — LOW: The memo does not specify what "durable completed" means operationally

Step 3 says "poll the generic AOI job-detail route until the fresh run reaches durable `completed` or a hard timeout." The memo should clarify which status field and which endpoint counts as the authoritative completion signal. Based on codebase inspection, the relevant endpoint is:

```
GET /api/analysis/anxiety_of_influence_thematic_single_thinker/jobs/{job_id}
```

and the authoritative field is `status == "completed"`. The older proof plan was more specific on this point.

### Finding 5 — LOW: Existing helper script invocation examples should match the actual script interface

The memo references two helper scripts and correctly notes they are supplemental. However, the direct-poll smoke script's actual interface (verified at `/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh`) uses `--project-id` as a required option and defaults to `--workflow-key intellectual_genealogy`, not the AOI key. The older proof plan's invocation examples were correct. The Phase 0 memo should either:

- include the correct invocation shape (matching the older plan)
- or simply reference the older plan's invocation examples by filename

This is low severity because the scripts are explicitly supplemental, not the counted proof.

### Finding 6 — INFORMATIONAL: The AOI_WORKFLOW_KEY and compose validator claims are accurate

Verified against the actual codebase:

- `src/presenter/compose_from_intent.py:497` — `_validate_request` hard-checks `request.workflow_key != AOI_WORKFLOW_KEY`
- `src/presenter/compose_from_intent.py:501` — same function hard-checks `request.consumer_key != TRANSIENT_COMPOSE_CONSUMER_KEY` (which is `"the-critic"`)
- Same pattern at lines 534, 538, 548, 552 for `_validate_source_request` and `_validate_selection_request`

The direction audit's claim that transient compose is structurally AOI-bound and the-critic-bound is codebase-accurate.

### Finding 7 — INFORMATIONAL: The Critic launch route claim is accurate

Verified at `/home/evgeny/projects/the-critic/api/server.py:14063`:

```python
@app.post(
    "/api/influence/thinkers/{thinker_id}/run-thematic-analysis-v2",
    response_model=GenealogyJobResponse,
)
```

The route checks for thinker existence and reference-text presence (raising 400 if none), then delegates to `start_genealogy_analysis`. The memo's claim about `POST /api/influence/thinkers/{thinker_id}/run-thematic-analysis-v2` is correct.

### Finding 8 — INFORMATIONAL: The planner-primary browser path claim is accurate

Verified in `AoiV2ThematicPanel.tsx`:
- Lines 596-599: `routeTask(...)` call with `consumer_key: 'the-critic'`, `workflow_hint: AOI_WORKFLOW_KEY`
- Lines 616-621: `planTask(...)` call with matching parameters

Both functions are imported from `taskLaunchRuntime.ts` which dispatches to `POST /v1/orchestrator/route-task` and `POST /v1/orchestrator/plan-task` respectively. These analyzer-v2 endpoints exist at `src/api/routes/orchestrator.py:301` and `:321`.

### Finding 9 — INFORMATIONAL: The helper scripts exist and are executable

Both scripts confirmed present and executable:
- `/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh` (9203 bytes)
- `/home/evgeny/projects/the-critic/test-stage5-aoi-landing-smoke.js` (2062 bytes)

### Finding 10 — INFORMATIONAL: The source-content identity repair claims are accurate

The source-content identity revision completion memo's claims check out:
- `src/aoi/contract.py` — the repair target — exists and is modified in the working tree
- `src/engines/capability_definitions/aoi_thematic_synthesis.yaml` — the contamination vector removal — exists and is modified
- `src/engines/capability_history/aoi_thematic_synthesis_snapshot.json` — snapshot update — exists and is modified

The tests pass per the completion memo (111 passed).

---

## Discussion of the bigger-picture goal

The memo correctly positions itself as the narrowest possible honest gate between the current Stage 5 / Stage 2 repair chain and the strategic pivot to Phase 1 bridge generalization described in the fixed-direction roadmap.

**The strategic value of this memo is not the proof itself.** The strategic value is that Phase 0 closure — whether the grade is flattering or not — unlocks the program to stop spending its main line on AOI-specific repair. The direction audit, the fixed-direction roadmap, and the master roadmap are all aligned on this: after Phase 0, the main line shifts to de-AOI / de-the-critic bridge generalization.

The memo correctly enforces this by:
1. Explicitly refusing to reopen host/browser repair
2. Explicitly refusing to pivot to Phase 1 before the decision memo is written
3. Accepting non-closure as a valid outcome that still closes Phase 0
4. Treating Closeout B (non-closure but honestly gradable) as still moving the program forward

This is the right shape. The only risk is if the executor interprets "closure-grade exemplar achieved" as requiring the full four-case rubric to pass, which would make Phase 0 impossible to close in one session. Finding 1 addresses this.

---

## Question-by-question answers

### 1. Is this memo the right immediate Phase 0 artifact?

**Yes.** It is correctly shaped as a single-execution proof memo with explicit closeout branches, not a repair scope or architectural redesign memo. It is the right next step after the source-content identity repair.

### 2. Are the operational assumptions strong enough?

**Mostly yes**, with the two medium-severity caveats above. The preflight contract is thorough. The reference-text upload step needs more specificity (Finding 2). The rubric application needs explicit scoping to one case (Finding 1).

### 3. Does the memo correctly separate preconditions / proof steps / closeout outcomes / out-of-scope widening?

**Yes, cleanly.** The five-step preflight, seven-step execution, three closeout shapes, and explicit "must not widen" list are all well-separated. The closeout shapes are honest — they accept non-closure and they accept infrastructure failure as distinct outcomes. The "must not widen" list correctly prevents Phase 0 from becoming another open-ended repair branch.

### 4. Are the codebase-backed claims accurate?

**Yes.** All verifiable codebase claims were confirmed:
- The Critic launch route exists and has the documented signature (Finding 7)
- The planner-primary browser path exists and calls the documented analyzer-v2 endpoints (Finding 8)
- The helper scripts exist and are executable (Finding 9)
- The compose validators hard-check AOI_WORKFLOW_KEY and the-critic consumer_key (Finding 6)
- The source-content identity repair files are modified in the working tree (Finding 10)

### 5. What is missing or prematurely fixed?

**Missing:**
- Explicit rubric case name for the fresh run (Finding 1)
- Explicit upload route for reference texts (Finding 2)
- Explicit completion-status field and polling endpoint (Finding 4)

**Not prematurely fixed:**
- The memo correctly does not attempt to fix the transient compose AOI-binding or the-critic-binding — those are Phase 1 work
- The memo correctly does not attempt to re-grade the other three rubric cases — they already have fixture-backed evidence
- The memo correctly treats the recovered run `job-6ee8b0621177` as background evidence only, not as the proof source

---

## Bottom line

This memo is the right immediate Phase 0 vehicle. It is bounded, operationally honest, and correctly structured to generate the one piece of evidence the program actually needs: a fresh post-fix execution-backed AOI grade on the evolution_ready case that either closes the exemplar gate or documents why it does not.

The two medium-severity revisions (explicit rubric case scoping, reference-text upload specificity) should be applied before execution to prevent ambiguous grading and avoidable preflight failure. The low-severity findings are nice-to-have improvements that would make the proof more robust but are not blocking.

After those revisions, the memo is ready for execution.
