# Critique: Stage 5 AOI Execution-Backed Evolution-Ready Scope

Date: 2026-03-25
Reviewer: Claude (Opus 4.6)
Docs reviewed:
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_scope.md`
- `communications/MEMO_2026-03-25_stage5_aoi_execution_backed_evolution_ready_proof_plan.md`
- `communications/MEMO_2026-03-25_stage5_aoi_exemplar_rerun_completion.md`
- `communications/PROOF_stage5_aoi_exemplar_eval_summary_2026-03-25.json`
- `communications/PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json`
- `communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`
- `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_completion.md`
- `communications/MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`

Code inspected:
- `/home/evgeny/projects/the-critic/api/server.py` (launch route, job polling, result routes, reference text checks)
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx` (planner-backed flow)
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx` (compose-from-selection)
- `/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh` (smoke test flags)
- `/home/evgeny/projects/the-critic/test-stage5-aoi-landing-smoke.js` (Playwright smoke)
- `/home/evgeny/projects/the-critic/data/the_critic.db` (reference text state)
- `src/api/routes/presenter.py` (compose endpoints)
- `src/presenter/compose_from_intent.py` (source-family preservation, reconciliation)
- `src/orchestrator/task_planner.py` (AOI planning, handoff plan)
- `tests/test_task_planner.py` (planner test coverage)
- `tests/test_compose_from_intent.py` (compose regression tests)

---

## Verdict

**Approve after revision.**

The scope is honest, appropriately narrow, and correctly sequenced. The proof plan structure matches the codebase. But one critical hidden operational prerequisite will cause the proof to dead-end at Step 1 as currently written, and two lesser prerequisites are under-specified.

---

## Findings

### Finding 1 (CRITICAL): Reference texts do not exist — proof plan will fail at Step 1

**Severity: Blocker.**

The proof plan's Step 1 calls:

```bash
curl -fsS \
  -X POST \
  -H 'X-Project-ID: round5-proof-dossier-final-1774100000' \
  http://127.0.0.1:5555/api/influence/thinkers/otto_neurath/run-thematic-analysis-v2
```

This route (`server.py:14060-14103`) performs a reference text check at lines 14083-14093:

```python
texts_result = await session.execute(
    select(InfluenceReferenceTextDB).where(
        InfluenceReferenceTextDB.project_id == project_id,
        InfluenceReferenceTextDB.thinker_id == thinker_id,
    )
)
if not texts_result.scalars().first():
    raise HTTPException(
        status_code=400,
        detail="No reference texts uploaded for this thinker. Upload texts first.",
    )
```

Direct inspection of `/home/evgeny/projects/the-critic/data/the_critic.db` shows:

- The thinker `otto_neurath` exists in project `round5-proof-dossier-final-1774100000` (passes the thinker existence check).
- The `influence_reference_texts` table contains **zero rows** for this project/thinker combination.

**Result:** The launch route will return HTTP 400 `"No reference texts uploaded for this thinker. Upload texts first."` before any run is created.

The proof plan's preflight section (line 66-67) acknowledges this as a possible stop condition:

> 5. If the fresh launch route returns `400 No reference texts uploaded for this thinker`, stop. That is a real precondition failure for this proof.

But the plan treats this as a contingency rather than addressing it as a **known fact**. The reference texts are not there. This is not a maybe — it is a certainty.

**Why previous fixture-backed evidence did not expose this:** All fixture-backed tests reuse already-saved AOI results. They never call the launch route. The fixture-backed pack exercises the planner-backed compose path against existing result artifacts, not against a freshly launched run. So the reference text precondition was never tested.

**Recommended revision:** The proof plan must add an explicit preflight step to upload or verify reference texts for `otto_neurath` before Step 1. This step should specify:

- What reference texts are needed (primary literature by/about Otto Neurath, secondary literature by Aaron Benanav referencing Neurath's planning argument)
- Where to source them (existing project corpora, manual upload, or re-use from another project)
- The upload route (`POST /api/influence/thinkers/otto_neurath/reference-texts` or equivalent)
- Verification that the upload succeeded before proceeding

The scope memo's Decision 7 (stop-and-revise rules) should also be updated to distinguish between "the launch route failed because of a known fixable precondition" (which is this case) and "the launch route failed because of a genuinely new product-path seam."

### Finding 2 (MODERATE): Run duration expectations are absent

**Severity: Operational gap.**

A real AOI thematic analysis run against analyzer-v2 involves multiple sequential LLM calls across engine phases. Based on the project memory for this codebase, large-input engine calls produce ~3.5K chars in ~35 minutes at 183K+ token inputs. A full thematic analysis may include 4+ engine phases.

The proof plan's Step 3 says:

> Poll the generic AOI job detail endpoint until the fresh run completes

This step could take 30-120+ minutes depending on corpus size and engine count. The plan does not:

- Set duration expectations
- Specify polling interval
- Define a timeout beyond which the run is considered failed
- Clarify whether the proof executor should wait passively or perform other preflight checks during polling

**Recommended revision:** Add a note to Step 3 that a real run may take 30-120+ minutes. Specify a maximum acceptable wait (e.g., 180 minutes) before treating the run as failed. This is not scope-changing — it is operational honesty about what "execution-backed" actually costs in wall-clock time.

### Finding 3 (MODERATE): Database concurrency risk from earlier diagnosis is not addressed

**Severity: Latent risk.**

The earlier evolution_ready diagnosis (`MEMO_2026-03-25_stage5_aoi_evolution_ready_diagnosis.md`) documented a `"database is locked"` failure in `_save_v2_presentation_to_db(...)` that caused warm snapshot durability failures. The snapshot durability repair was reported as landed (per the rerun completion memo).

However, the execution-backed proof introduces a different concurrency scenario: a real long-running AOI analysis run will be producing database writes over an extended period while the local SQLite database may also be handling concurrent read/poll requests from the smoke test scripts and browser. The snapshot durability fix targeted one specific code path (`_save_v2_presentation_to_db`), but the underlying SQLite concurrency limitation remains.

**Recommended revision:** The preflight section should include a note that if `"database is locked"` errors recur during the fresh run or during the subsequent warm-snapshot/compose path, this is a recurrence of the known database concurrency issue — not a new seam. The stop-and-revise rules should classify this distinctly from a "genuinely new product-path seam."

### Finding 4 (LOW): Smoke test script does not fully match the proposed invocation

**Severity: Minor mismatch.**

The proof plan Step 2 proposes:

```bash
/home/evgeny/projects/the-critic/test-stage5-direct-poll-smoke.sh \
  --analyzer-url http://127.0.0.1:8002 \
  --critic-url http://127.0.0.1:5555 \
  --workflow-key anxiety_of_influence_thematic_single_thinker \
  --consumer-key the-critic \
  --project-id round5-proof-dossier-final-1774100000 \
  --thinker-id otto_neurath \
  --run-job-id <fresh_local_job_id>
```

The smoke script (`test-stage5-direct-poll-smoke.sh`) uses `--run-job-id` to check active discovery via `GET /v1/runs/discovery?...&scope=active`. This validates that the active run appears in discovery results.

However, the launch route (`server.py:19614-19635`) creates the in-memory job with `job_id` set to the **upstream v2 job id** (the analyzer-v2 executor job id), not a separate local id. The proof plan's language ("returned local `job_id`") is slightly misleading — the returned job_id IS the upstream v2_job_id for v2-backed runs. This matters because:

- The `--run-job-id` value and the `--result-job-id` value in Steps 2 and 4 will be the same identifier (the v2 job id)
- The active-run boundary check in Step 2 hits analyzer-v2's `/v1/runs/discovery` which uses this same id

This is not wrong — it's how the code works — but the proof plan's language about "fresh local job id" vs "fresh upstream source_v2_job_id" conflates them. The plan should clarify that for v2-backed runs, these are the same value.

### Finding 5 (LOW): Port assumption fragility

**Severity: Minor.**

The earlier diagnosis ran on non-standard ports (5556/3457) because preferred ports were occupied. The proof plan assumes standard ports (5555/3456/8002). This is fine as a default, but the proof plan should note that if ports are occupied, using alternative ports is acceptable and does not invalidate the proof — as long as both services point at each other correctly.

---

## Direct Answers to Review Questions

### Q1: Is one bounded execution_backed evolution_ready case really the right next move, or is some other prerequisite still missing?

**Yes, this is the right next move** — the logic chain is sound: seam gate passed on fixture-backed evidence, rubric requires execution-backed evidence for Stage 2, therefore one execution-backed case is the minimal next step.

**But there IS a missing prerequisite:** reference texts for `otto_neurath` must be uploaded before the proof can begin. This is a data setup step, not an architecture gap. Once reference texts exist, the proof plan's structure is correct.

### Q2: Is evolution_ready still the right default upgrade candidate?

**Yes.** It has the strongest artifact trail, the best-understood compose path (four-family selection: thematic_synthesis + engagement_mapping + sin_findings + thematic_report), and was already named as the default execution-backed upgrade candidate in earlier review notes. The alternatives (engagement_ready, non_profile_ready) have narrower or more constrained selection shapes that would give less evidence about the planner-backed compose path.

### Q3: Is the memo's definition of execution_backed strict enough?

**Yes.** Decision 3 in the scope memo is well-defined:

- Fresh run through real launch route (not saved-result shortcut)
- Newly produced outputs (not reuse of previous outputs)
- Subsequent compose proof uses fresh result's `source_v2_job_id`
- Does not count if only previously saved result outputs are the authoritative source

This is strict enough to prevent disguised fixture reuse. The only way to cheat this definition would be to claim "execution_backed" while actually using a previously completed run, which the proof plan's artifact trail (launch response JSON with `created_at` timestamp) would make detectable.

### Q4: Does the proof plan actually match the codebase?

**Mostly yes, with one critical data gap:**

| Element | Plan assumption | Codebase reality | Match? |
|---------|----------------|-------------------|--------|
| Launch route | `POST /api/influence/thinkers/{thinker_id}/run-thematic-analysis-v2` | Exists at `server.py:14060-14103` | Yes |
| Project-id handling | `X-Project-ID` header | `_get_project_id_from_request()` at `server.py:2042-2047` | Yes |
| Reference text check | Acknowledged as possible stop | **Will definitely fail** — zero rows in DB | **No (data gap)** |
| Polling route | `GET /api/analysis/{workflow_key}/jobs/{job_id}` | Exists at `server.py:20641-20644`, delegates to `get_genealogy_job()` | Yes |
| v2_job_id exposure | Expected in poll response | Returned via `v2_job_id` field at `server.py:19718-19719` | Yes |
| Compose-from-selection | Frontend calls `composeFromSelection(...)` | `AoiComposeFromIntentPage.tsx:414-450`, routes to `presenter.py:444-474` | Yes |
| Source-family preservation | Expected to preserve structured data | `compose_from_intent.py:871-884` (source family shortcut) | Yes |
| Contract enforcement | Expected to pass | Reconciliation at `compose_from_intent.py:1027-1060` + 4 regression tests | Yes |
| Smoke test scripts | Expected flags match | `test-stage5-direct-poll-smoke.sh` accepts all proposed flags | Yes |

### Q5: Is one successful execution_backed ready case really enough for honest Stage 2 closure under the frozen rubric?

**Technically yes, but barely.**

The rubric (`MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md`, lines 127-133) says Stage 2 documentary closure requires:

> - the Stage 5 seam gate passes
> - at least one ready case is `execution_backed` or stronger
> - the exemplar evidence is strong enough to support repeated bounded AOI transient use rather than fixture-only seam proof

The first two conditions are objective and would be met by one successful execution-backed case.

The third condition — "strong enough to support repeated bounded AOI transient use" — is subjective. One fresh run proves the path works once end-to-end. Whether one successful execution proves "repeated bounded use" is a judgment call. The scope memo is honest about this being a minimum bar, not a comprehensive proof. The closeout memo should explicitly address this third condition and explain why one case is sufficient (or flag it as a known limitation).

### Q6: Are there hidden operational prerequisites?

**Yes, three:**

1. **Reference texts (CRITICAL):** Zero reference texts exist for `otto_neurath` in `round5-proof-dossier-final-1774100000`. The launch route will return 400 before any run is created. This must be fixed in the proof plan.

2. **Run duration (MODERATE):** A real AOI thematic run may take 30-120+ minutes. The proof plan sets no duration expectations or timeout policy.

3. **SQLite concurrency (LATENT):** The earlier `"database is locked"` failure during warm snapshot could recur under the different concurrency profile of a real long-running run. The snapshot durability fix targeted one specific path, but the underlying SQLite limitation persists.

### Q7: Does the updated roadmap now tell the truth?

**Yes.**

Both the master roadmap (`MASTER_BIG_ROADMAP_MEMO...`, Section 2, lines 96-104) and the draft next-stages roadmap (`MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`, Tranche 2 sequencing note, lines 192-236) now correctly state:

- Stage 5 seam gate passed on fixture-backed evidence (true)
- Stage 2 is still not documentary-closed because no ready case has been upgraded to execution_backed (true)
- Tranche 3 remains blocked until one bounded execution-backed case is captured and the Stage 2 closure decision is written (true)

The master roadmap's honest progress estimate (75-85% for bounded AOI substrate, 55-65% for AOI exemplar ratification, 30-40% for full platform) is also well-calibrated. The memo count does not inflate the stage closure picture.

### Q8: Is the new step appropriately narrow, or is it smuggling in broader platform closure by implication?

**It is appropriately narrow.**

The scope memo's Decision 6 explicitly separates Stage 5 and Stage 2 decisions. Decision 1 treats this as an evidence-upgrade, not a new architecture step. The "status implications" section (lines 193-205) correctly states that Tranche 3 remains blocked even if this step succeeds — the closeout must write the Stage 2 decision explicitly, and that decision is separate from Stage 5.

The scope does not claim that one execution-backed case closes Stage 3, 4, or 5 entirely, nor does it imply that Stage 2 closure automatically unblocks Tranche 3 without an explicit written decision.

---

## Recommended Revisions Before Execution

### Revision 1 (Required): Add reference text upload to proof plan preflight

Insert between current Preflight steps 4 and 5:

> 4a. Upload reference texts for `otto_neurath` in the `round5-proof-dossier-final-1774100000` project.
>
> Required: at minimum, one or more primary-literature documents by or about Otto Neurath, and one or more secondary-literature documents by Aaron Benanav that reference Neurath's planning argument. These must cover the corpus that the `evolution_ready` task expects to reason over.
>
> Upload via the reference text upload route (e.g., `POST /api/influence/thinkers/otto_neurath/reference-texts` with `X-Project-ID` header).
>
> Verify the upload succeeded:
> ```bash
> curl -fsS \
>   -H 'X-Project-ID: round5-proof-dossier-final-1774100000' \
>   http://127.0.0.1:5555/api/influence/thinkers/otto_neurath/reference-texts
> ```
>
> If reference texts cannot be sourced or uploaded, stop. This is a data prerequisite, not a product-path seam failure.

### Revision 2 (Required): Update scope memo Decision 7 stop-and-revise rules

Add a clause distinguishing data-prerequisite failures from product-path seam failures:

> If the launch fails because of a known fixable data prerequisite (e.g., missing reference texts, missing thinker record), fix the prerequisite and retry — do not treat this as a new seam that requires a revision memo. Only write a revision memo if the launch fails on a genuinely new product-path seam after all data prerequisites are met.

### Revision 3 (Recommended): Add run duration expectation to Step 3

> Note: A real AOI thematic analysis run may take 30-120+ minutes depending on corpus size and engine phase count. Poll at 30-60 second intervals. If the run has not completed after 180 minutes, treat it as a failure and write a revision note.

### Revision 4 (Recommended): Add note on port flexibility

> If preferred ports (5555/3456/8002) are occupied, alternative ports are acceptable for this proof as long as both services are correctly pointed at each other. Update the curl commands and smoke test flags accordingly. Non-standard ports do not invalidate the proof.

### Revision 5 (Recommended): Clarify job_id semantics

In Step 1, clarify:

> For v2-backed runs, the returned `job_id` IS the upstream v2 job id — these are the same value, not two separate identifiers. The proof plan refers to this single identifier in some places as "local job_id" and in others as "source_v2_job_id"; they resolve to the same value for this run type.

---

## Summary Judgment

The scope memo is honest, disciplined, and correctly sequenced. The proof plan's structure matches the actual codebase paths. The definition of `execution_backed` is strict enough. The roadmap tells the truth. The scope does not smuggle in broader claims.

The single critical gap is that the proof **will not start** without reference texts being uploaded first. This is a data prerequisite, not an architecture problem — but it must be addressed in the proof plan before execution begins. Without this revision, the proof plan will dead-end at Step 1 and produce a misleading "stop" artifact that looks like a product-path failure when it is actually a missing-data setup step.

After the required revisions (reference text preflight and stop-rule clarification), the proof plan is ready to execute.
