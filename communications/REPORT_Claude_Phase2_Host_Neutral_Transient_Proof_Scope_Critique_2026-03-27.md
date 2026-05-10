# Critique: Phase 2 Host-Neutral Transient Proof Scope

Date: 2026-03-28
Reviewer: Claude (Opus 4.6)
Memo Under Review: `communications/MEMO_2026-03-27_phase2_host_neutral_transient_proof_scope.md`

## Verdict: Approve After Revision

The memo is strategically sound, well-sequenced, and correctly identifies what the program needs next. But it has one hidden implementation blocker and two assumptions that need to be made explicit before safe implementation can begin.

---

## Finding 1 (CRITICAL): Consumer adapter registration will reject any new proof harness consumer_key

The memo claims the proof harness should be host-neutral and outside the current AOI / `the-critic` path. But the current code will reject any consumer_key other than `"the-critic"` at the transient compose boundary.

Evidence:

```python
# src/presenter/compose_from_intent.py:54
TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"

# src/presenter/compose_from_intent.py:158
_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS = frozenset({TRANSIENT_COMPOSE_CONSUMER_KEY})

# src/presenter/compose_from_intent.py:528
if consumer_key not in _REGISTERED_TRANSIENT_CONSUMER_ADAPTERS:
    raise ComposeFromIntentClientError(
        f"{route_label} only supports registered consumer adapters; got '{consumer_key}'"
    )
```

This means the proof chain described in the memo (steps 1-6) will fail at step 5 (`POST /v1/presenter/compose-from-intent`) if the proof harness passes its own consumer_key.

Phase 1A replaced the old hardcoded AOI workflow/consumer validators with registry-based handoff capability validation (`_SUPPORTED_HANDOFF_KINDS`). But it kept the consumer adapter registration as a separate frozenset gate. That gate is still single-consumer-only.

**Required revision**: The memo must acknowledge this constraint and decide one of:

- (a) Register the proof harness consumer_key in `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` as part of Phase 2 scope (narrow: add one string to a set).
- (b) Replace the frozenset gate with the existing `ConsumerRegistry` lookup (broader: make consumer validation registry-based like handoff validation already is).
- (c) Pass `consumer_key="the-critic"` from the proof harness and accept that as a known limitation — but then document honestly that the proof does not yet prove consumer-neutral compose entry.

Option (b) is the cleanest and most aligned with the Phase 1A direction. Option (c) is dishonest relative to the memo's stated ambition. Option (a) is the pragmatic minimum.

**Severity**: This is not a scope or sequencing mistake. It is a concrete implementation blocker that would surprise the implementor. The memo must name it so the implementation plan can address it cleanly.

---

## Finding 2 (MODERATE): Default `consumer_key="the-critic"` in multiple Pydantic schema classes

Beyond the explicit adapter gate, many Pydantic request schemas default `consumer_key` to `"the-critic"`:

- `src/presenter/schemas.py:410` — `ComposeFromIntentRequest`
- `src/presenter/schemas.py:494` — `ComposeFromSourceRequest`
- `src/presenter/schemas.py:533, 540, 556, 576` — additional request models
- `src/presenter/composition_resolver.py:140, 252`
- `src/presenter/recommendation_defaults.py:52`
- `src/presenter/presentation_api.py:1349`
- `src/presenter/renderer_contract_enforcement.py:182`

If the proof harness passes its own consumer_key explicitly, these defaults should not fire. But any code path that constructs a request model without explicitly setting `consumer_key` will silently default to `"the-critic"`.

**Required revision**: The memo should note that the proof must explicitly thread `consumer_key` through every request in the chain, and that the implementation should verify no silent default fallback to `"the-critic"` occurs in the proof path. This is not a blocker, but it is a trap that would undermine the honesty of the proof if missed.

---

## Finding 3 (MODERATE): The bridge reads executor database state — the memo's anti-dependency claim is correct but needs clarification

The memo correctly says the proof "must not silently fall back to `/v1/executor/jobs`." The proof chain does not create or start a new executor job. But the genealogy saved-result bridge does read from the executor database:

```python
# src/orchestrator/genealogy_saved_result_bridge.py:63-75
job = get_job(source_v2_job_id)  # reads from executor DB
...
if (job.get("status") or "") != "completed":
    raise GenealogySavedResultBridgeError(...)

# src/orchestrator/genealogy_saved_result_bridge.py:103
latest_outputs = _latest_phase_outputs_by_engine(source_v2_job_id)
# -> calls load_phase_outputs(job_id=source_v2_job_id) from executor.output_store
```

This means the proof requires a pre-existing completed `intellectual_genealogy` job in the executor database. The proof itself never calls `POST /v1/executor/jobs`, but it consumes the output of a prior execution.

This is semantically correct — the whole point of `saved_result` is reading from prior execution truth. But the memo should be explicit that:

- The proof requires at least one completed genealogy job to exist
- The proof harness must supply a real `source_v2_job_id` pointing to that job
- This is a data prerequisite, not a hidden execution dependency

**Required revision**: Add one sentence to the "must land" section clarifying that the proof requires a pre-existing completed genealogy result (and cannot be run in a vacuum). This is not a scope problem — it is a setup requirement that the implementor needs to know.

---

## Finding 4 (LOW): Module naming and docstring residue in `compose_from_intent.py`

The module docstring at `src/presenter/compose_from_intent.py:1` still reads:

```python
"""Bounded transient compose-from-intent orchestration for AOI."""
```

And the file's top-level constants and role mappings already include genealogy engine keys (`genealogy_relationship_classification`, `genealogy_final_synthesis`, etc.) at lines 115-118. The code is already more general than the docstring claims.

This is cosmetic and not a blocker. But it signals that Phase 1A landed the generalization in behavior without updating the identity of the module. A proof harness running against this module might confuse future reviewers who read the docstring and conclude it is AOI-only.

**No required revision** to the Phase 2 scope memo. Optionally fix the docstring during implementation.

---

## Direct Answers to the Nine Questions

### 1. Is the memo correct that the main missing proof after Phase 1C is stronger host-neutral transient consumption, not more bridge generalization?

**Yes.** Phase 1C closed the structural single-workflow asymmetry at the planner/router/lowering layer. The code now has:

- Two routing outcomes (`aoi_transient_source_backed`, `genealogy_transient_source_backed`) at `task_routing_schemas.py:61-66`
- Two composition-facing handoff plans (`aoi_composition_handoff_plan`, `direct_sections_composition_handoff_plan`) at `task_planning_schemas.py:30-37`
- A shared handoff executor keyed by `workflow_key + handoff_kind` at `compose_from_intent.py:148-157`
- Immutable planning snapshots that round-trip both handoff types through `planning_decision_store.py`

The bridge is structurally no longer single-workflow-only. The remaining gap is consumption, not structure.

### 2. Is the memo right to choose a minimal dedicated proof harness as the default vehicle rather than extending the current AOI `the-critic` path again?

**Yes.** Extending `the-critic` would prove that `the-critic` can consume the bridge — which is already known. The value of Phase 2 is proving that something *else* can consume it. The memo's anti-drift rule ("do not treat `aoi-canary` result-backed proof as if it already answered the transient question") is correct because `aoi-canary` only exercises result-backed contracts (`results/discovery`, `results/by-job`, `results/presentation`) — it never touches the transient compose/planner boundary.

### 3. Is `genealogy + saved_result + direct_sections_composition_handoff_plan` the right bounded first transient target?

**Yes, with one caveat.** This is the right choice because:

- It exercises the Phase 1C generalized path (not the already-proven AOI path)
- It uses the thinnest public boundary (`compose-from-intent`)
- It avoids the complex AOI source-selection LLM pipeline
- The bridge code already exists and is tested (`genealogy_saved_result_bridge.py`, `direct_sections_compose_harness.py`)

The caveat: the proof requires a pre-existing completed genealogy job (Finding 3). The memo should name this explicitly so the implementation knows to set up test fixtures or use existing production data.

### 4. Does the code actually support the memo's claim that this proof can avoid `the-critic` AOI proxy routes, `/v1/executor/jobs`, and host-local section reconstruction?

**Partially.**

- **Avoiding `the-critic` AOI proxy routes**: Yes. `compose-from-intent` is served directly by analyzer-v2 at `POST /v1/presenter/compose-from-intent`. The `the-critic` proxy routes at `server.py:21452` and `server.py:21514` are for `compose-from-source` and `compose-from-selection` only.
- **Avoiding `/v1/executor/jobs`**: Yes, for job creation. The proof chain does not start new execution. But the bridge reads from executor data (Finding 3). This is correct for `saved_result` semantics.
- **Avoiding host-local section reconstruction**: Yes. Sections are derived entirely in `genealogy_saved_result_bridge.py` from analyzer-owned result truth. The proof harness would receive them pre-composed.

**However**: the consumer adapter gate (Finding 1) currently blocks any consumer_key other than `"the-critic"`. So the proof cannot currently avoid `the-critic` identity even though it avoids `the-critic` infrastructure.

### 5. Is the memo honest about what `aoi-canary` does and does not already prove?

**Yes.** The memo correctly identifies `aoi-canary` as a "result-backed second-consumer proof, not a transient one." The code confirms: `aoi-canary`'s `resultsClient.ts` only calls `results/discovery`, `results/by-job/{id}`, and `results/by-job/{id}/presentation`. It never touches route-task, plan-task, planning-decisions, or compose-from-intent.

### 6. Is there any hidden blocker that would force this slice to reopen planner/router contracts, presenter boundary shape, host ownership doctrine, or lifecycle/session semantics?

**One hidden blocker**: The consumer adapter gate (Finding 1) forces either a narrow code change (registering a new consumer_key) or a broader one (moving to registry-based consumer validation). Neither reopens Phase 1 contracts, but the broader option touches the same file that Phase 1A generalized, so it must be acknowledged.

**No other hidden blockers.** The route-task, plan-task, and planning-decision-store paths are already generic. The lowering harness already works for `direct_sections`. The presenter boundary (`ComposeFromIntentRequest`) stays thin.

### 7. Is the optional ephemeral token/session borrow well-bounded, or does it risk sneaking Phase 3 into Phase 2?

**Well-bounded.** The constraints are explicit:

- ephemeral only
- proof-scoped only
- no draft/session/share semantics
- no automatic promotion into Phase 3 lifecycle law

And the default is "if the proof does not actually require that token, do not invent it." The genealogy `saved_result` proof path likely does not require it — the proof can thread `planning_decision_id` (which is already durable) and `source_v2_job_id` (which is the canonical identity) without needing an ephemeral surface token. The memo correctly defers this decision to implementation.

### 8. Does the memo stay properly bounded relative to the larger sequence?

**Yes.** The memo:

- Does not reopen Phase 1 planner/router generalization
- Does not reopen Phase 1B ownership doctrine
- Does not attempt lifecycle/session semantics
- Does not attempt a polished end-user app
- Does not confuse result-backed proof with transient proof
- Keeps "must not widen" constraints explicit and correct

### 9. Is it concrete enough to guide safe implementation?

**Almost.** The proof chain (steps 1-6 in the "must land" section) is clear and executable. The exit test is testable. The "must not widen" constraints are specific.

What is missing for safe implementation:

1. Acknowledgment of the consumer adapter registration blocker (Finding 1)
2. Explicit note that `consumer_key` must be threaded through every request to avoid silent `"the-critic"` defaults (Finding 2)
3. Explicit note that the proof requires a pre-existing completed genealogy job (Finding 3)

---

## Is this the right next honest step?

**Yes.** The memo correctly reads the program state after Phase 1C. The bridge is generalized but consumption is still single-consumer. The right next step is to prove that the bridge can be consumed by something other than the current AOI / `the-critic` page stack. The genealogy `saved_result` + `direct_sections` target is the simplest honest non-AOI chain available.

## Does the memo stay properly bounded?

**Yes.** It is one of the most disciplined scope memos in the trail. It avoids the recurring temptation to widen into lifecycle, polish, or re-architecture. The "must not widen" list is concrete and correct. The optional ephemeral token borrow has explicit guardrails.

## Concrete Revisions Needed Before Implementation

1. **Add Finding 1 to the scope**: Name the `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` gate explicitly. Decide whether the proof harness will register its own consumer_key (option a), move to registry-based consumer validation (option b), or honestly use `consumer_key="the-critic"` and document the limitation (option c). Recommend option (a) or (b).

2. **Add a data prerequisite note**: State explicitly that the proof requires at least one completed `intellectual_genealogy` job in the executor database. This is a setup requirement, not a scope change.

3. **Add a consumer_key threading note**: State that the proof must explicitly pass consumer_key at every hop in the chain to avoid falling into `"the-critic"` defaults in the Pydantic request schemas.

These three additions can each be one sentence. They do not change the scope or the strategic direction. They make the scope safe to implement without surprises.
