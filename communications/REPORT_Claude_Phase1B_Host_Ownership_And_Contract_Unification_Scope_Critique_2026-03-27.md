# Report: Phase 1B Host Ownership And Contract Unification Scope Critique

Date: 2026-03-27
Reviewer: Claude (Opus 4.6)
Artifact reviewed: `communications/MEMO_2026-03-27_phase1b_host_ownership_and_contract_unification_scope.md`

## Verdict

**Approve after revision.**

The memo correctly identifies the right next slice, asks the right questions, and maintains disciplined boundaries. The five hypotheses are well-chosen starting positions. However, the memo has two material gaps and one framing risk that should be addressed before handing it to an implementation session.

---

## Findings

### Finding 1 (High): The memo underspecifies what the call-path inventory must actually capture, risking a shallow output

**Severity**: High — this is the deliverable definition, not a background claim.

The memo's "must land" item 7 requires:

> One current-state inventory of the actual call path for:
> - AOI planner-primary source-backed transient launch
> - one result-backed workspace path

This is correct in scope but underspecified in depth. Having read the live code, the AOI planner-primary path spans at minimum:

1. `AoiV2ThematicPanel.tsx` — row pin, readiness check via `getBoundedV2SourceBackedReadiness`, snapshot warmup via `cacheBoundedV2Presentation`, planner task routing via `routeTask`, planning via `planTask`, navigation state assembly, `navigate()` call
2. `AoiComposeFromIntentPage.tsx` — URL/search-param parsing, `location.state` planner metadata extraction, profile vs. selection dispatch decision, autostart timing
3. `composeFromIntentClient.ts` — host-contract-runtime-backed `dispatchHostProxyRequest` for `source_backed_transient_launch` family or `dispatchAnalyzerDirectRequest` for `transient_compose_from_intent` family
4. `the-critic/api/server.py` — `_resolve_source_backed_compose_identity()` with backfill, v2-job-id validation, project+thinker context enforcement
5. `analyzer-v2/src/orchestrator/task_router.py` — signal-based objective routing
6. `analyzer-v2/src/orchestrator/task_planner.py` — source catalog resolution, LLM-backed source selection, handoff plan assembly
7. `analyzer-v2/src/presenter/compose_from_intent.py` — hardcoded workflow_key + consumer_key validators, view generation, transformation execution, page assembly

The revision should specify that the inventory must name every hop, identity translation, and hardcoded constraint across this full chain — not just a conceptual summary. Otherwise a future implementor will produce a shallow ownership matrix that does not actually answer where `the-critic`-specific law lives versus reusable host law.

### Finding 2 (High): The `registered_corpus` source mode is invisible in the scope

**Severity**: High — silent omission of a live routing path.

The memo frames the source identity question exclusively through the AOI `saved_result` source mode:

- `source_analysis_id` + `source_v2_job_id` dual-id threading
- host continuity alias resolution
- project + thinker scope enforcement

But `taskLaunchRuntime.ts` already defines a second source mode — `RegisteredCorpusSourceHint` — which is live in the router and planner for genealogy `by_ref` flows. That mode uses `consumer_key`, `external_project_id`, `target_external_doc_key`, and `prior_work_external_doc_keys_count` as its identity coordinates, which are entirely different from the AOI saved-result identity model.

If Phase 1B is supposed to decide whether `taskLaunchRuntime` belongs inside the host contract story, and if it is supposed to produce a reusable ownership matrix, it must at least acknowledge that there are two live source identity shapes passing through the same routing/planning contract. The `registered_corpus` mode may end up explicitly out of scope for Phase 1B, but the memo should say so rather than silently omitting it.

**Revision instruction**: Add one explicit scoping note acknowledging the `registered_corpus` source mode. State whether Phase 1B addresses both source modes or defers registered_corpus identity to a later Phase 1C/2 slice.

### Finding 3 (Medium): The `compose_from_intent.py` hardcoded validators are the most concrete entry point for Phase 1A — the Phase 1B memo should name them explicitly

**Severity**: Medium — naming the exact constraints strengthens the invariant list.

The memo correctly identifies that `compose_from_intent.py` hard-validates `workflow_key == AOI_WORKFLOW_KEY` and `consumer_key == the-critic`. But it says this at a high level ("still hard-validates") without locating the exact validators. The live code has three parallel validation functions:

- `_validate_request()` (for plain `compose-from-intent`)
- `_validate_source_request()` (for `compose-from-source`)
- `_validate_selection_request()` (for `compose-from-selection`)

Each independently enforces both constraints. The Phase 1B invariant list should explicitly name these as the boundary that Phase 1A is either allowed to relax or required to replace with a reusable contract check. This is not implementation — it is decision-grade boundary naming.

### Finding 4 (Medium): Hypothesis 5 about `taskLaunchRuntime` absorption is correct in direction but needs a sharper test

**Severity**: Medium — risk of a fuzzy decision that does not actually resolve the adjacency.

Hypothesis 5 says `taskLaunchRuntime` "should not remain a sidecar" and should either be absorbed into Host Contract v2 or form an explicit planner-advisory subcluster.

Having read the code: `taskLaunchRuntime.ts` already imports `dispatchAnalyzerApiRequest` from `hostContractRuntime.ts` and shares the same URL/fetch infrastructure. What it lacks is:

- Family-level dispatch mode checking (`assertDispatchMode`)
- Required-input validation (`validateHostContractInputs`)
- Consumer-key threading (`resolveFamilyConsumerKey`)
- Surface selection integration

So the question is not "should it be absorbed" — it effectively already shares plumbing. The question is whether `route-task` and `plan-task` should become named families in the `HOST_CONTRACT_V1_FAMILIES` array with their own `owner`, `canonical_identity`, `required_inputs`, and `contract_level` entries.

**Revision instruction**: Sharpen Hypothesis 5 into a testable question: "Should `route-task` and `plan-task` become named contract families with explicit ownership, identity, and input requirements in the family table, or should they remain outside the family table as pre-contract advisory calls with their own bounded runtime?"

### Finding 5 (Low): The memo correctly avoids Phase 1A implementation but slightly underweights the `compose-from-source` vs `compose-from-selection` asymmetry

**Severity**: Low — not blocking, but a future implementor will hit this.

The AOI compose path has a real structural asymmetry that the ownership matrix should surface:

- `composeFromSource()` dispatches via `dispatchHostProxyRequest` (host_proxy family) through `the-critic/api/server.py`
- `composeFromSelection()` also dispatches via `dispatchHostProxyRequest` through the same server
- Both routes are AOI-workflow-specific (`/analysis/anxiety_of_influence_thematic_single_thinker/projects/{project_id}/compose-from-source` and `.../compose-from-selection`)
- `composeFromIntent()` dispatches via `dispatchAnalyzerDirectRequest` (analyzer_direct family) directly to analyzer-v2

So the host proxy routes are currently AOI-baked into URL path segments. Phase 1B's ownership decision should note whether the host proxy should keep workflow-specific URL paths or move to a workflow-generic proxy route.

### Finding 6 (Low): No missing recent memos of material importance

I checked:

- Stage 13 minimal generic host contract completion memo (2026-03-24) — already referenced
- Stage 7 planner-to-presentation bridge scope (2026-03-23) — already referenced
- Stage 8 task intake and workflow routing scope (2026-03-23) — already referenced
- Phase 0 active discovery repair completion (2026-03-27)
- Phase 0 prompt budget revision scope (2026-03-27)

The memo's reference list is adequate. The Phase 0 repair memos (active discovery, prompt budget) are operational fixes that do not change boundary ownership, so their omission from the reference list is acceptable.

---

## Assessment: Is Phase 1B the right next slice?

**Yes.** This is the correct move for three reasons:

1. **Phase 0 is honestly closed.** The March 27 closeout decision is backed by real execution evidence. Continuing AOI-specific repair would violate the anti-drift rules in the fixed-direction roadmap.

2. **The ownership questions are now concrete.** Before the typed `hostContractV1.ts`, `hostContractRuntime.ts`, and `taskLaunchRuntime.ts` artifacts existed, the ownership questions would have been abstract. Now they are decidable against live code.

3. **Phase 1A without Phase 1B would reproduce drift.** If an implementor starts relaxing `compose_from_intent.py` validators without first deciding what the host is still allowed to own (identity translation, snapshot warmup, surface selection, navigation), they will accidentally encode new host-local analytical law or create a nominally generic endpoint that still only works for AOI.

The memo is also correctly scoped as decision-only, not implementation. That is the right call — the risk of jumping to code without settling ownership is exactly how the program accumulated sidecar law in the first place.

---

## Assessment: Are the five hypotheses well-chosen?

**Yes, with one sharpening needed** (see Finding 4).

- Hypothesis 1 (source identity stays host-owned): Well-grounded. The `_resolve_source_backed_compose_identity()` function in `server.py` is genuinely host-side contract behavior involving project-scoped saved-result rows, backfill logic, and continuity alias creation. Moving this upstream would embed host persistence concerns inside analyzer-v2.

- Hypothesis 2 (warm snapshot stays host-owned): Correct. `cache_snapshot_warmup` is already modeled as `host_proxy` in the family table. The Phase 0 proof used it exactly that way.

- Hypothesis 3 (surface selection stays host-owned but becomes contract law): Correct and important. Today surface selection is implicit in page routing. Making it explicit in the contract table is the right transition — it makes the host's surface choice auditable without moving it upstream.

- Hypothesis 4 (navigation/launch handoff stays host-owned): Correct. The Phase 0 evidence shows the host assembling URL search params, location state, and navigate() calls. That is inherently browser/page territory.

- Hypothesis 5 (taskLaunchRuntime should not remain sidecar): Directionally correct but needs sharpening per Finding 4.

None of the hypotheses prematurely lock a solution. They are framed as defaults to test, not as conclusions.

---

## Assessment: Is the source-identity problem framed correctly?

**Mostly yes, with one gap.**

The memo correctly synthesizes the three prior doctrines:

- Stage 7's `source_analysis_id`-first host doctrine
- Stage 13's `upstream_v2_job_id` as canonical with `source_analysis_id` as host-local continuity alias
- Phase 0's dual-id proof using both together

The framing of "alias-first vs canonical-id-first vs permanently dual-identity" is the right question.

The gap is that the memo does not note the asymmetry between Phase 0's use of both ids and the host contract's formal modeling. In `hostContractV1.ts`, the `source_backed_transient_launch` family lists `source_analysis_id` and `source_v2_job_id` as "optional continuity selectors, not hard launch requirements" in its notes, but does not list them in `required_inputs` (which only requires `project_id`, `selected_source_thinker_id`, `variant`). So the contract already formally treats them as optional, while the host runtime practically requires at least one to resolve identity. Phase 1B should note this gap between formal contract modeling and actual runtime necessity.

---

## Assessment: Is `taskLaunchRuntime` absorption a category mistake?

**No, it is not a category mistake.** The code confirms that `taskLaunchRuntime` uses the same dispatch infrastructure as the host contract runtime, just without family-level governance. Calling `route-task` and `plan-task` "contract families" is architecturally coherent — they are analyzer-direct calls with specific inputs, identity requirements, and response contracts. Whether they belong in the same family table or in a distinct pre-contract advisory table is a genuine design decision, not a type error.

---

## Assessment: Are the memo's claims about the current live split actually true in code?

**Yes, verified against live code.**

| Memo claim | Code evidence |
|---|---|
| Host Contract v1 is typed but not the full runtime story | `hostContractV1.ts` has 11 families; `hostContractRuntime.ts` provides dispatch, validation, consumer-key resolution — but does not cover routing/planning |
| `taskLaunchRuntime` is live but adjacent | `taskLaunchRuntime.ts` imports from `hostContractRuntime.ts` but dispatches via `dispatchAnalyzerApiRequest` without family-level checks |
| AOI planner-primary path mixes host and analyzer law | `AoiV2ThematicPanel.tsx` owns row pin + readiness + warmup + routing + planning + navigation; `AoiComposeFromIntentPage.tsx` owns URL parsing + profile/selection dispatch |
| Source identity and continuity alias are host-owned | `server.py:_resolve_source_backed_compose_identity()` resolves project/thinker-scoped identity, does backfill, creates local aliases |
| Analyzer transient boundary is AOI-bound and the-critic-bound | `compose_from_intent.py` has three validators all checking `workflow_key == AOI_WORKFLOW_KEY` and `consumer_key == "the-critic"` |

All claims verified.

---

## Assessment: Does the memo keep the right boundaries?

**Yes.** The memo does not silently drift into:

- Phase 1A implementation — explicitly deferred
- Lifecycle — explicitly listed under "must not widen"
- Second-consumer proof — explicitly excluded
- More AOI-local product work — explicitly excluded

The "must not widen" list is comprehensive and well-chosen.

---

## Revision instructions

1. **Specify inventory depth** (Finding 1): The "must land" item 7 should note that the call-path inventory must name every hop, every identity translation point, and every hardcoded constraint across the full host+analyzer chain, not just the conceptual layers.

2. **Acknowledge `registered_corpus` source mode** (Finding 2): Add a scoping note under the source identity section acknowledging that `taskLaunchRuntime` already carries two source modes (`saved_result` and `registered_corpus`) and explicitly stating whether Phase 1B addresses both or defers the registered_corpus identity shape.

3. **Sharpen Hypothesis 5** (Finding 4): Replace the current framing with: "Should `route-task` and `plan-task` become named contract families with explicit ownership, identity, and input requirements in the family table, or should they remain outside the family table as pre-contract advisory calls with their own bounded runtime?"

4. **Name the three compose validators explicitly** (Finding 3): In the section about `compose_from_intent.py` hard-validation, name `_validate_request()`, `_validate_source_request()`, and `_validate_selection_request()` as the specific boundary points that Phase 1A will need to either relax or replace.

5. **Note the formal/practical identity gap** (source-identity assessment): Add one sentence noting that the `source_backed_transient_launch` family's `required_inputs` do not include `source_analysis_id` or `source_v2_job_id`, but the runtime practically requires at least one for identity resolution — this is itself an ownership question Phase 1B should settle.

---

## Summary

The Phase 1B memo is the right next move. It correctly follows from Phase 0 closure, asks the right ownership questions, and maintains clean boundaries. The five hypotheses are well-grounded starting positions that do not prematurely lock solutions. The memo's factual claims about the live codebase are all verified.

The revisions above are about sharpening the deliverable specification and closing two silent gaps (registered_corpus source mode, formal vs. practical identity requirements) that would otherwise surface during implementation as unresolved ambiguities. None of the revisions change the strategic direction — they make it more implementable.
