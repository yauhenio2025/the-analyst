# REPORT: Phase 3 Bounded Lifecycle V1 Scope Critique

Date: 2026-03-28
Evaluating: `communications/MEMO_2026-03-28_phase3_bounded_lifecycle_v1_scope.md`
Reviewer: Claude (Opus 4.6)
Method: Code-path inspection + memo-trail verification + roadmap alignment

---

## 1. Verdict

**Approve after revision**

The memo is strategically correct, properly sequenced, and honestly bounded. Lifecycle law for dynamic analytical surfaces is the right next question now that Phase 2 transient proof is closed. The decision to target generic `direct_sections + compose-from-intent` rather than AOI proxy compose is the right first substrate.

However, the memo has **four findings that need revision** before implementation planning, one of which is architecturally load-bearing. None of them change the strategic direction; all of them sharpen the scope enough to make the implementation unambiguous.

---

## 2. Findings (ordered by severity)

### Finding 1 (HIGH): The memo does not specify WHERE the lifecycle object is stored or what persistence substrate it uses

The memo says the lifecycle object must be "analyzer-owned truth, not browser-only state" (line 127) and must contain a "saved compose response / presentation snapshot" (line 123). But it never addresses the persistence mechanism.

The current codebase has two file-backed persistence patterns that are relevant:

- `planning_decision_store.py` — writes JSON files to `src/orchestrator/planning_decisions/` (line 19, line 54-56)
- `project_manager.py` — writes to the executor database (Postgres + SQLite dual-backend via `src/executor/db.py`)

The compose response (`ComposeFromIntentResponse` at `src/presenter/schemas.py:729-735`) contains a full `TransientIntentPagePresentation` with views carrying `structured_data`, `items`, and nested children. This is a large payload — potentially hundreds of KB per session.

**The memo must decide:**
- File-backed (like planning decisions)? Simple but no query/filter capability.
- Database-backed (like jobs/projects)? Queryable but requires schema migration.
- A new dedicated store? Adds surface area but keeps lifecycle separate from planning and execution.

This is architecturally load-bearing because the reopen path's performance and the retention rule both depend on it. If the store is file-backed, indefinite retention is easy. If database-backed, it interacts with existing cleanup/archive cycles.

**Recommended revision:** Add one explicit "persistence substrate" decision to the memo. File-backed JSON (mirroring `planning_decision_store.py`) is the honest minimal choice for this slice — it avoids executor DB entanglement, supports the bounded retention rule (indefinite, no cleanup), and keeps the lifecycle object clearly separate from execution truth.

### Finding 2 (MEDIUM): The compose request snapshot alone is insufficient — the memo should name the EXACT schema boundary of the saved lifecycle object

The memo lists minimum semantic content (lines 117-126) but does not clarify the most important question: does the lifecycle object save the **compose request** or the **compose response** or both?

Looking at the current schemas:

- `ComposeFromIntentRequest` (`schemas.py:613-621`) — thin: just `workflow_key`, `consumer_key`, `user_intent`, `prose_sections`, `style_school`, `audience`
- `ComposeFromIntentResponse` (`schemas.py:729-735`) — rich: contains `TransientIntentPagePresentation` (full view tree with structured_data) plus `generated_view_definitions` plus `ComposeFromIntentTrace`

For the reopen law to be honest (must not rerun `compose-from-intent`), the lifecycle object **must** include the compose response, not just the request. The request alone would require re-composition on reopen, violating the stated reopen law.

The memo hints at this ("saved compose response / presentation snapshot" at line 123) but does not make it a hard requirement with the same clarity as the reopen prohibition.

**Recommended revision:** State explicitly that the saved lifecycle object must include the serialized `ComposeFromIntentResponse` (or its `TransientIntentPagePresentation` payload at minimum). The compose request is provenance; the compose response is the reopenable truth.

### Finding 3 (MEDIUM): The memo does not address the `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` constraint for the proof surface

The Phase 2 scope memo (`MEMO_2026-03-27`, lines 97-106) explicitly named the constraint: transient compose still validates `consumer_key` against `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS`, which today is only `{"the-critic"}` (confirmed at `compose_from_intent.py:158`).

The Phase 3 memo says the proof vehicle should be "the existing genealogy transient proof page in `the-critic`, or a very close sibling" (lines 100-101). This is fine. But the save and reopen routes themselves may need to thread `consumer_key` for validation, and the memo does not specify whether the lifecycle layer should enforce the same transient consumer registration constraint or be open to any `consumer_key`.

**Recommended revision:** State explicitly that the save/reopen lifecycle layer does NOT require new transient consumer registration — it reuses the already-registered `consumer_key` from the compose response. The lifecycle layer validates `consumer_key` for fetch authorization but does not independently enforce the transient-compose adapter registry. This keeps Phase 3 bounded away from transient consumer registration expansion, which the memo already prohibits.

### Finding 4 (LOW): The older "Phase 3" label collision should be named explicitly

The memo references `MEMO_2026-03-19_phase3_artifact_reuse_scope.md` at line 15 as "an older superseded Phase 3 line, not the active roadmap." This is correct. But the earlier `PLAN_Stage3_Lifecycle_Authority.md` (dated 2026-03-16) also uses "Stage 3" for lifecycle authority work that overlaps with this memo's scope.

The older Stage 3 plan targeted a *different* lifecycle question: result-contract authority displacement and Critic snapshot deletion. That plan is about making `analyzer-v2` the restore authority for job-backed results. This Phase 3 memo is about save/reopen law for transient compose surfaces — a fundamentally different lifecycle layer.

**Recommended revision:** Add one sentence explicitly noting that the older Stage 3 lifecycle work (result-contract restore authority) is orthogonal to this Phase 3 (transient compose session lifecycle) and that neither supersedes the other. They address different persistence objects.

---

## 3. Direct answers to the review questions

### Q1: Is lifecycle the right next phase?

**Yes.** Phase 2 proved transient compose works outside the AOI controller path. The memo correctly identifies that the next honest question is no longer "can the system produce a transient surface?" but "what happens when the user wants to keep one?" No other Phase 3 candidate (governance, broader consumer registration, more proof surfaces) makes sense before this question is answered.

### Q2: Is targeting generic `direct_sections + compose-from-intent` first correct?

**Yes.** The AOI proxy compose stack (`compose-from-source`, `compose-from-selection`) carries AOI-specific identity, source-family, and profile semantics that would contaminate a first lifecycle definition. The generic `compose-from-intent` path through `direct_sections` is the thinnest substrate and the right place to first define lifecycle. Confirmed by code: `compose-from-intent` at `schemas.py:613-621` has the cleanest request shape.

### Q3: Is `planning_decision_id` insufficient as a lifecycle object?

**Yes, confirmed by code.** `planning_decision_store.py` stores a `PersistedTaskPlanningDecision` that contains the task request, routing decision, and planning decision — all immutable planning artifacts. It does NOT contain:
- The compose request actually sent to the presenter
- The compose response / presentation payload
- The trace from composition

The planning snapshot enables *replaying* the compose chain, but replaying is exactly what the reopen law prohibits. So `planning_decision_id` is provenance, not lifecycle truth. The memo is correct on this point.

### Q4: Does the code support the claim that no save/reopen lifecycle object exists?

**Yes, confirmed comprehensively:**
- No `compose_session` or `session_store` files exist anywhere in `src/`
- `ComposeFromIntentResponse` is returned to the caller and never persisted
- `GenealogyTransientProofPage.tsx` renders each step's output in React state — debug/proof UI only, no persistence
- `AoiComposeFromIntentPage.tsx` uses `planning_decision_id` for *recovery* (refetch the planning snapshot), but the compose output itself is ephemeral
- `composeFromIntentClient.ts` returns the response to the caller — no storage hook
- No endpoint in `routes/orchestrator.py` or `routes/presenter.py` accepts or returns a saved compose session

The gap is real and precisely where the memo says it is.

### Q5: Is the ownership split clear enough?

**Mostly yes, with one gap.** The memo clearly says:
- Analyzer owns saved session truth and reopen payload truth (line 161)
- Host owns route semantics, `session_id` navigation, and bounded reopen presentation (line 162)
- Host must not reconstruct by replaying planner law (line 163)

The gap: the memo does not explicitly state who **generates** the `session_id`. Given the pattern in `planning_decision_store.py` where `planning_decision_id` is generated analyzer-side (line 34: `f"planning-decision-{uuid4().hex[:12]}"`), the natural choice is analyzer-generated `session_id` returned on save. But the memo should state this explicitly to prevent a host-generated `session_id` pattern where the host sends an arbitrary ID and the analyzer merely stores it.

**Minor revision needed:** State that `session_id` is generated by analyzer on save, not provided by the host.

### Q6: Is the bounded retention rule honest enough?

**Yes for a first slice.** "Retained indefinitely, cleanup deferred" is the only honest retention rule for a slice that introduces a new persistence object. Premature cleanup policy would require defining session value, staleness, and user intent — all of which are Phase 4+ concerns. The memo correctly names this as a minimal rule and defers the hard questions.

One implicit consequence: if the persistence substrate is file-backed, indefinite retention means unbounded disk growth. This is fine for a proof slice but should be noted.

### Q7: Does the memo stay properly bounded?

**Yes.** The "must not widen" list (lines 190-196) is comprehensive and correctly blocks:
- Fake lifecycle substitution via `planning_decision_id`
- Auto-save
- Publish/share
- AOI proxy lifecycle
- New consumer registration
- Edit-in-place authoring
- Executor job displacement

I verified each against the codebase:
- The `planning_decision_id` temptation is real (it already looks like a session ID but isn't one)
- Auto-save would be trivial to implement but would fundamentally change the transient/saved distinction
- AOI proxy compose has additional `source_family_key`, `profile`, and `selection` semantics that don't belong in a first lifecycle definition

The boundedness is genuine, not ceremonial.

### Q8: Is anything contradicted by live code?

**One minor inaccuracy.** The memo says at line 76: "`compose_from_intent.py` can emit `draft`-status views inside a transient payload." I searched for `draft` status semantics in the actual `TransientIntentView` schema (`schemas.py:689-705`) and in `compose_from_intent.py`. The `TransientIntentView` has no `status` field — it has `visibility` (`"if_data_exists"` default) and `has_structured_data`. There is no `draft` enum or status concept in the transient view schemas.

This may refer to informal use of the word "draft" in view descriptions or rationales rather than a formal status field. The claim is directionally correct (the compose response carries provisional views) but technically misleading if read as implying a formal draft/published lifecycle concept already exists in the schema.

### Q9: Is anything important missing?

**Two items:**

1. **The memo does not specify whether the save action is synchronous or asynchronous.** Given the payload size (a full `TransientIntentPagePresentation` with structured data in views), save should be synchronous and blocking — the user waits for confirmation before navigating away. But this should be stated.

2. **The memo does not address idempotency of the save action.** If the user clicks "save" twice on the same transient surface, should it create two sessions or return the existing one? The simplest honest rule for v1 is "always create a new session" (no deduplication), which avoids defining equivalence semantics. But the memo should say so explicitly.

---

## 4. Summary judgment

This is the right next honest step. The memo:

- Follows verified Phase 2 completion with the correct next question
- Targets the thinnest generalized substrate first
- Stays properly bounded away from prohibited widening
- Correctly identifies the gap between planning persistence and lifecycle persistence
- Defines clear reopen law that is code-verifiable

The four required revisions are:

1. **Persistence substrate decision** (file-backed JSON recommended)
2. **Explicit compose response inclusion** in saved object (not just request)
3. **Consumer registration constraint** clarification (reuse existing, don't gate on registry)
4. **`session_id` generation authority** (analyzer-generated, not host-provided)

The two optional additions:

5. Save action synchronicity (synchronous recommended)
6. Save idempotency rule (always-new-session for v1)

After these revisions, the memo is ready for implementation planning.
