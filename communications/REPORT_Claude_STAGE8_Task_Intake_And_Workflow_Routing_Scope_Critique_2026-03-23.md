# Critique: Stage 8 / Task Intake And Workflow Routing Scope

Date: 2026-03-23
Reviewer: Claude (Opus 4.6)
Target Memo: `communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_scope.md`
Verdict: **Approve after revision**

---

## Summary Judgment

The memo is strategically sound, disciplined, and correctly scoped as a routing-only contract rather than a union execution endpoint. The core thesis — that analyzer-v2 should own workflow routing so the host no longer decides analytically — is the right next upstream move after the Stage 7 bridge.

However, the memo has one structural deficiency that must be resolved before implementation planning: **the two non-unsupported routing outcomes demand radically different intake shapes and downstream lifecycle regimes, and the memo does not confront this asymmetry.** If this gap is not addressed, the routing contract will either be dishonest (routing to genealogy without a credible follow-on) or will force a premature lifecycle merge.

---

## Findings (ordered by importance)

### 1. STRATEGIC — The two routing outcomes are not peers; the downstream launch contracts are fundamentally asymmetric

This is the most important issue.

**`aoi_transient_source_backed`** means: the caller already has a saved analysis result (identified by `source_v2_job_id` or a higher-level result/project identity), and the router confirms that transient recomposition from that saved truth is the right move. The follow-on is `POST /v1/presenter/compose-from-source` — fast, synchronous, no LLM execution.

**`genealogy_job_backed`** means: the caller needs to launch a full analysis pipeline — document upload, plan generation (15-30s LLM call), execution (5-60+ minutes of multi-phase LLM work), then presentation assembly. The follow-on is `POST /v1/orchestrator/analyze` or `POST /v1/orchestrator/analyze-by-ref`.

These are not two flavors of the same operation. They differ in:

- intake shape (saved-result identity vs. document texts + thinker metadata)
- latency (seconds vs. tens of minutes)
- lifecycle regime (transient recomposition vs. durable job-backed execution)
- what the host must provide (a result reference vs. a corpus)

The memo's proposed `CompositionTaskRequest` tries to unify these under one envelope with `source_constraints`, but this field would need to mean completely different things depending on the routing outcome. For AOI transient: "here is the saved result to recompose from." For genealogy: "here is the document set to analyze from scratch."

**What must change**: The memo should explicitly acknowledge this asymmetry and decide one of:

1. Stage 8 routing is advisory only — it tells the host *which* downstream contract to follow, and the host still calls the appropriate endpoint with the appropriate payload shape. The `CompositionTaskRequest` is a lightweight pre-dispatch inquiry, not the intake for the actual work.

2. Stage 8 routing is pre-dispatch that returns a structured `downstream_launch_contract` describing exactly what the host needs to call next and what payload shape to use, without trying to unify those payloads into one envelope.

Option (1) is simpler and more honest for a bounded stage. Option (2) is more useful but risks scope creep.

### 2. STRATEGIC — The genealogy routing outcome is hollow until a genealogy composition path exists

The memo proposes routing to `genealogy_job_backed` as one of the three outcomes. But today there is no genealogy equivalent of AOI source-backed transient composition. Genealogy has job-backed PagePresentation via `GET /v1/presenter/page/{job_id}`, which is the legacy presentation path — not the transient composition stack that Stage 7 formalized.

This means the routing contract would say "this task belongs to genealogy" and then hand back a launch contract that bypasses the entire composition bridge that Stages 7-11 are building. The host would call `POST /v1/orchestrator/analyze` with full documents, get a `job_id`, and poll for completion — exactly what it already does today without any router.

This doesn't make the genealogy outcome *wrong*, but it does make it less valuable than the memo implies. The routing decision for genealogy adds little that the host doesn't already know: if you have documents to analyze and no saved AOI result, the answer is obviously genealogy.

**What must change**: The memo should explicitly state that the genealogy routing outcome in Stage 8 is primarily a proof-of-routing-generality, not a composition-equivalent path. The downstream launch contract for genealogy will be the existing `analyze` or `analyze-by-ref` intake. This is acceptable for the bounded stage, but the memo should be honest about it.

### 3. ARCHITECTURAL — Objective definitions already encode workflow routing, and the memo does not leverage this

The existing objective definitions in `src/objectives/definitions/` already contain a `baseline_workflow_key` field:

- `influence_thematic.json` → `"baseline_workflow_key": "anxiety_of_influence_thematic_single_thinker"`
- `genealogical.json` → `"baseline_workflow_key": "intellectual_genealogy"`

This is already a near-1:1 objective-to-workflow mapping. The proposed routing logic could use this as the primary deterministic routing signal: if the router can classify the task into an objective, the workflow follows from `baseline_workflow_key`.

Additionally, the workflow definitions themselves carry `category` fields (`"influence"`, `"genealogy"`, `"synthesis"`, etc.) and descriptive metadata that could inform routing.

**What must change**: The memo should explicitly reference these existing assets and describe how Stage 8 routing will leverage `objective_key → baseline_workflow_key` as the primary routing mechanism, potentially enriched by source-constraint shape analysis.

### 4. ARCHITECTURAL — The memo should clarify whether routing uses an LLM or is deterministic

For a bounded 3-outcome routing space, deterministic routing (task keyword matching + source-constraint shape analysis + objective classification) is almost certainly sufficient and dramatically simpler than an LLM call.

The existing pipeline already defaults `workflow_key` to `intellectual_genealogy` and only uses AOI when explicitly selected. The routing heuristic for Stage 8 could be as simple as:

- If source constraints indicate a saved AOI result identity → `aoi_transient_source_backed`
- If source constraints indicate documents to analyze + task semantics match genealogy-style inquiry → `genealogy_job_backed`
- Otherwise → `unsupported`

The memo is silent on this question.

**What must change**: The memo should state explicitly that Stage 8 routing should be deterministic (no LLM call), with structured trace explaining the classification. LLM-assisted routing belongs to later stages when the outcome space is richer.

### 5. ARCHITECTURAL — Relationship to existing `analyze` and `analyze-by-ref` endpoints is unclear

The orchestrator already has:

- `POST /v1/orchestrator/analyze` — full pipeline with inline documents
- `POST /v1/orchestrator/analyze-by-ref` — full pipeline with pre-registered documents

Both require `workflow_key` (defaulting to `intellectual_genealogy`). The new `POST /v1/orchestrator/route-task` would be a pre-dispatch step before these.

The memo should clarify: does `route-task` *replace* the caller's need to choose between `analyze` and `compose-from-source`? Or is `route-task` an optional advisory step that returns a recommendation, and the caller still calls the appropriate existing endpoint?

For a bounded stage, the advisory pattern is cleaner — it avoids creating a fourth pipeline entry point that duplicates existing logic.

**What must change**: State whether `route-task` is advisory (returns routing decision, host follows up with existing endpoints) or dispatch (triggers the downstream action). Advisory is recommended for Stage 8.

### 6. PROOF/EVIDENCE — The genealogy routing proof case is easy to pass but not very meaningful

The memo's proof standard requires:

> one genealogy task request routed to `genealogy_job_backed` without a consumer-supplied workflow key

This is easy to satisfy but proves little. If the task says "trace the genealogy of ideas in this author's work" and provides document references without a saved AOI result, of course the router will pick genealogy. The routing intelligence is minimal — it's pattern matching on task text and source-constraint shape.

The more valuable proof would show **a genuinely ambiguous task** where the router must reason about whether AOI or genealogy is more appropriate, and either routes correctly with explicit rationale or returns `unsupported` with honest confidence.

**What must change**: Add a proof case for a genuinely ambiguous or borderline task (e.g., "analyze how Author X engages with Thinker Y's ideas" — which could plausibly be AOI or genealogy depending on the source constraints). This tests the router's actual discriminative power.

### 7. STRATEGIC — The 8-workflow inventory is broader than the memo acknowledges

The workflow registry contains 8 definitions:

- `intellectual_genealogy` (active, fully execution-ready)
- `anxiety_of_influence_thematic_single_thinker` (active, fully execution-ready)
- `lines_of_attack` (active but narrower)
- `anxiety_of_influence` (legacy/broader variant)
- `outline_editor` (different domain)
- `decider_answer_processing`, `decider_onboarding`, `decider_question_lifecycle` (decision-support domain)

The memo proposes a 2+1 routing space (AOI, genealogy, unsupported). That is correctly bounded for Stage 8. But the memo should acknowledge that `lines_of_attack` exists as a third potentially-routable analytical workflow and state explicitly that it is out of scope for Stage 8 but will not be forgotten in Stage 9+.

### 8. MINOR — The namespace decision is correct

Placing `route-task` under `orchestrator` rather than `presenter` is the right call. Routing is pre-composition, pre-presentation. The orchestrator namespace already owns planning and pipeline dispatch.

### 9. MINOR — The memo's "fail-closed" discipline is commendable

The explicit requirement for `unsupported` as a first-class outcome, with confidence scores and rejection rationale, is exactly right. Many routing systems fail by silently coercing ambiguous inputs into the nearest supported path. The memo avoids this. No change needed.

---

## What Is Right

1. **Routing-only, not union-dispatch**: This is the correct bounded decision. A union execution endpoint would blur lifecycle regimes prematurely.
2. **Analyzer-owned**: The host should not decide the workflow analytically. Moving that decision upstream is the correct strategic direction.
3. **Bounded outcome set**: Three outcomes (aoi, genealogy, unsupported) is the minimum honest routing space.
4. **Fail-closed behavior**: First-class `unsupported` outcome with confidence and rejection rationale.
5. **Explicit trace**: Routing traces with selected/rejected candidates mirror the Stage 7 bridge pattern well.
6. **Discipline against scope creep**: The "What Stage 8 Must Not Do" section is clear and correct.
7. **Correct sequencing**: This is the right next upstream move after the Stage 7 source-to-composition bridge.

---

## What Must Change Before Implementation Planning

| # | Category | Issue | Required Change |
|---|----------|-------|-----------------|
| 1 | Strategic | Asymmetric downstream lifecycles | Explicitly confront AOI-transient vs genealogy-job-backed asymmetry; decide whether `route-task` is advisory or dispatch; acknowledge the genealogy outcome's limited value in Stage 8 |
| 2 | Strategic | Hollow genealogy composition path | State that genealogy routing in Stage 8 is a proof-of-generality, not a composition-equivalent path |
| 3 | Architectural | Existing `baseline_workflow_key` not leveraged | Reference objective definitions as the primary routing signal |
| 4 | Architectural | LLM vs deterministic unspecified | State that Stage 8 routing is deterministic, no LLM call |
| 5 | Architectural | Relationship to existing endpoints unclear | Clarify whether `route-task` is advisory or dispatch |
| 6 | Proof | Ambiguous task proof case missing | Add a borderline/ambiguous proof requirement |

---

## No Relevant Perspective Docs Folder

After checking the repository, no `Perspective` or `perspectives` directory exists anywhere in the analyzer-v2 codebase.

---

## Conclusion

The memo is strategically correct and well-disciplined. The routing-only framing, the fail-closed behavior, and the explicit scope boundaries are all right.

The revision needed is not a fundamental rethinking — it is an honest confrontation with the fact that the two non-unsupported routing outcomes live in fundamentally different lifecycle regimes, and the routing contract must describe that asymmetry rather than paper over it. The existing objective and workflow metadata in the codebase already provides the routing signal; the memo should build on it explicitly.

Once revised, this scope is implementation-ready.
