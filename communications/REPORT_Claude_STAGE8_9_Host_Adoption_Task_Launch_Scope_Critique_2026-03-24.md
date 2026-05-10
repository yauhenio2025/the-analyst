# Stage 8/9 Host Adoption Task Launch Scope Critique

> Reviewer: Claude (Opus 4.6)
> Date: 2026-03-24
> Memo Reviewed: `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_scope.md`
> Cross-Referenced: Master Roadmap, Dynamic Bespoke Apps Vision, Stage 8/9/10/11/12/13 completion memos, live codebase in analyzer-v2 and the-critic

---

## Verdict: Approve After Revision

The memo is directionally correct. The genealogy host-adoption seam is the strongest deliverable and genuinely reduces host-owned analytical intelligence. The AOI proof seam is honest about its boundaries but overstates how much analytical intelligence it actually removes from the host. Three concrete issues need revision before this should be executed.

---

## Key Findings (Ordered by Severity)

### FINDING 1 — HIGH: The AOI Proof Seam Is Thinner Than The Memo Implies

The memo claims the AOI proof should show "the host no longer decides locally that the next move is source-backed transient compose." But in practice the AOI proof operates inside pages that already know they are AOI surfaces.

What the host currently does for AOI source-backed launch (`AoiV2ThematicPanel.tsx:488-555`):

1. Host is already ON the AOI thematic panel (URL routing decided this)
2. Host checks profile readiness via `getBoundedV2SourceBackedReadiness()`
3. Host warms snapshot if ready
4. Host navigates to compose page

What the memo proposes with route-task + plan-task:

1. Host sends task to route-task (but the host is STILL on the AOI panel — it already knows the context)
2. Receives routing confirmation "yes this is AOI source-backed transient"
3. Receives plan-task handoff with allowed/blocked profiles
4. Presents profiles to user
5. Launches compose via existing helper

The routing step is **ceremonial** in the AOI case because the host's URL routing already determined that this is an AOI surface. The analytical intelligence being "removed" is the host's knowledge that it is on an AOI path — but the host already possesses that knowledge from the URL alone.

The plan-task handoff returning allowed/blocked profiles is genuinely useful — but it is functionally equivalent to the existing Stage 10 readiness API that the host already calls. The `AoiCompositionHandoffPlan` schema provides richer source-family metadata, but for the bounded proof seam, the host only needs the profile feasibility answer, which it already gets from readiness.

**Revision needed**: The memo should acknowledge that the AOI route-task proof is mainly a contractual normalization step (useful for future undifferentiated-entry scenarios), not a real analytical intelligence reduction. The plan-task AOI proof is stronger if framed as "consolidating the readiness + source-bridge check into one advisory call" rather than "removing host analytical decision-making."

### FINDING 2 — HIGH: Risk of a Third Disconnected Client Layer

The Stage 13 second-slice review (`REPORT_Claude_STAGE13_Second_Slice_Harder_Generic_Host_Proof_Scope_Critique_2026-03-24.md`) already identified a structural problem: `composeFromIntentClient.ts` sits outside the shared `boundedV2Client.ts` stack with separate URL construction, error handling, and no shared constants.

The memo proposes adding "one shared typed task-launch client/runtime layer" as a **new** module. This creates a risk of three parallel client stacks in the-critic:

1. `boundedV2Client.ts` — result-backed families
2. `composeFromIntentClient.ts` — transient compose families
3. new task-launch client — route-task + plan-task families

The memo says "land this through shared host runtime, not page-local fetches" (Decision 7), which is correct in principle. But it does not address whether the task-launch client should unify or sit alongside the existing two client stacks.

**Revision needed**: The memo should make an explicit decision: either (a) the task-launch layer becomes the new unified entry point that subsumes the existing advisory calls in `boundedV2Client.ts` and `composeFromIntentClient.ts`, or (b) it is a separate advisory-only layer that chains into the existing client stacks for downstream launch. Option (b) is more honest for a bounded slice but the memo should acknowledge the structural debt.

### FINDING 3 — MEDIUM: plan-task Genealogy Side Effects Are Unaddressed

Verified in code: `plan-task` for genealogy is NOT purely advisory. It has real side effects:

- Uploads documents to the document store via `_upload_documents()` (both inline and by-ref paths)
- Generates a full `WorkflowExecutionPlan` via LLM (Claude Opus call)
- Returns `hydrated_document_ids` from the uploads

If the host calls `plan-task` speculatively, retries on transient failure, or calls it twice during a slow UI interaction, it will create duplicate documents and orphaned plans. The memo says "analyzer returns advisory routing and bounded planning decisions" (Decision 6) but plan-task for genealogy is not advisory in the side-effect sense.

**Revision needed**: The memo should either (a) specify idempotency guardrails for plan-task genealogy (e.g., dedup by task+document hash), or (b) acknowledge the side effects and specify that the host must treat plan-task as a commit step rather than a probe, or (c) require a separate dry-run mode for genealogy planning that does not upload documents.

### FINDING 4 — MEDIUM: The Memo's Proof Bar Has An Internal Tension On AOI Auto-Selection

Proof bar item 2 says: "one AOI task where analyzer-owned planning returns allowed/blocked profiles and required host preparation, and the host follows that result rather than inferring it locally."

But the current host does not "infer" profiles locally. It calls the Stage 10 readiness API (`getBoundedV2SourceBackedReadiness`) which already returns analyzer-owned profile feasibility. The host then follows that result.

So the proof bar as stated is already partly satisfied by the existing readiness flow. The delta from plan-task is that it consolidates routing + readiness + source-bridge metadata into one response — but it does not change the fundamental interaction pattern (host asks analyzer, analyzer says which profiles work, host follows).

**Revision needed**: Tighten proof bar item 2 to specify what plan-task adds beyond the existing readiness check. If the answer is "source-bridge metadata plus required host preparation steps," say that explicitly. If the answer is "nothing material beyond existing readiness," then either drop the AOI proof bar to one item or reframe it as a contractual consolidation proof.

### FINDING 5 — LOW: The Genealogy Proof Seam Is Genuinely Strong

This is the strongest part of the memo and the codebase evidence confirms it.

Currently the host locally decides:
- Whether to call `analyze` (inline documents) or `analyze-by-ref` (registered corpus)
- What document context to assemble
- How to structure the execution request

With route-task + plan-task, the host would:
- Send the task + source constraints
- Receive a routing decision (genealogy job-backed) and a real `WorkflowExecutionPlan`
- Execute the returned plan through existing `POST /v1/executor/jobs`

This genuinely removes ~100-150 lines of analytical decision code from the host and shifts workflow selection and document hydration upstream.

The existing execution helpers in the-critic (`boundedV2Client.ts` wrappers around `orchestrator/analyze` and `orchestrator/analyze-by-ref` and `executor/jobs`) provide a natural integration substrate.

**No revision needed.** This seam is honest and high-leverage.

### FINDING 6 — LOW: Lifecycle Deferral Is Correct

The memo's argument for deferring Stage 14 lifecycle is well-grounded:

- Without host adoption of task routing/planning, lifecycle decisions would build on unclear boundaries
- The master roadmap Stage 6 (lifecycle) explicitly says "this decision should be made after evaluation evidence exists"
- The current program still lacks the proof that "the host can ask analyzer what the next move should be" — landing that first is the right order

### FINDING 7 — LOW: Not-A-Second-Consumer Reasoning Is Correct

The argument that a second-consumer push is premature is sound. The master roadmap Stage 13 exit evidence requires "second consumer or generic host proof without rebuilding intelligence locally." But that exit bar is not achievable until the current host actually demonstrates consuming analyzer-owned task intelligence. Adding a second consumer on top of host-owned analytical decisions would prove duplication, not maturity.

---

## Open Assumptions

### Assumption 1: Route-task + plan-task two-step is better than a single combined call

The memo argues for both steps (Decision 3). The reasoning about route visibility and debugging seams is valid. But the host adding two sequential API calls for every task launch (route → plan → execute) may create latency overhead, especially since plan-task genealogy involves an LLM call. The memo should acknowledge this tradeoff and consider whether route-task results could be cached or coalesced in common paths.

### Assumption 2: The current AOI outcome set is sufficient for a bounded host proof

Route-task currently supports exactly three outcomes: `aoi_transient_source_backed`, `genealogy_job_backed`, `unsupported`. For the bounded proof, this is fine. But if the host adoption proof only covers paths that the host already knows from URL routing, the "advisory" claim is weaker than it appears. The real test of advisory value would be an undifferentiated entry point where the host sends a task without pre-knowing the workflow — but the memo explicitly says that is not in scope. This is honest but should be acknowledged.

### Assumption 3: Host Contract V1 stability is achievable alongside a task-launch layer

The memo argues (Decision 2) that Host Contract V1 stays focused on run/result/readiness/transient delivery and the task-launch layer sits on top. Verified in code: `hostContractV1.ts` defines 11 families focused on delivery, not advisory routing. This separation is clean in principle. The risk is that the task-launch layer's followup contracts (the `downstream_followup_contract` in plan-task responses) will effectively re-derive Host Contract V1 family dispatch, creating a parallel dispatch path. The memo should specify that the task-launch layer's followup contracts must map onto existing Host Contract V1 families, not create shadow dispatch.

---

## Should The Next Phase Stay As Proposed Or Be Reframed?

**Stay as proposed, with revisions.** The genealogy seam is the right next move. The AOI seam is worth doing for contractual consolidation but should be framed more honestly.

The alternative considered — going directly to Stage 3 (AOI task-driven composition beyond fixed profiles) — would be higher-risk and would skip the host-adoption proof that the memo correctly identifies as missing. The master roadmap §7 warns about "optimizing the pilot instead of generalizing the platform," but making the current host consume analyzer advisory seams IS generalization work, not pilot optimization.

The other alternative — unifying client layers first (closing the `composeFromIntentClient.ts` / `boundedV2Client.ts` split before adding task-launch) — has merit but is lower leverage. Client unification can happen during or after the task-launch layer lands.

**Recommended revisions before execution:**

1. Reframe the AOI proof bar to acknowledge that route-task provides contractual normalization (not analytical intelligence reduction) for the AOI case
2. Specify whether the task-launch client unifies, subsumes, or sits alongside the existing two client stacks
3. Address plan-task genealogy side effects (idempotency, retry safety, or explicit commit semantics)
4. Specify that downstream followup contracts must map onto existing Host Contract V1 families
5. Acknowledge the two-call latency tradeoff and consider whether route-task caching or coalescing is in scope

---

## Summary

| Aspect | Assessment |
|--------|-----------|
| **Directionally correct?** | Yes |
| **Genealogy seam honest?** | Yes — genuinely reduces host analytical intelligence |
| **AOI seam honest?** | Partially — honest about boundaries but overstates analytical intelligence reduction |
| **Host Contract V1 stability?** | Correct — clean separation from task-launch layer |
| **Lifecycle deferral?** | Correct |
| **Second-consumer deferral?** | Correct |
| **Proof bar?** | Needs tightening on AOI items 1-2 |
| **Client-layer risk?** | Unaddressed — needs explicit decision |
| **Side-effect risk?** | Unaddressed — plan-task genealogy is not purely advisory |
| **Overall verdict** | **Approve after revision** |
