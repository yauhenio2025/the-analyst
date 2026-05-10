# Stage 11 Rich Semantic Page Planning Scope Audit

Verdict: `Approve`

Post-revision note:

- The revised `communications/MEMO_2026-03-23_stage11_rich_semantic_page_planning_scope.md` addresses the main blocking issues from the earlier draft.
- It now distinguishes the first honest Stage-11 slice from the full eventual stage, carries the narrow `the-critic` transient-host delta explicitly, narrows the semantic matcher to analyzer-owned AOI-local rules rather than missing AOI `semantic_visual_intent`, and frames the work as a real `compose_from_intent.py` refactor rather than a planner-schema swap.
- The remaining issues are implementation cautions, not scope blockers.

## Findings

1. **No blocking scope mismatch remains between the revised memo and the live codebase.**
Evidence: the revised memo now matches the actual split in the repo. `src/presenter/compose_from_intent.py` is still flat and AOI-scoped, while authored/result-restore paths in `src/presenter/presentation_api.py`, `src/presenter/bounded_dynamic_composition.py`, and `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx` already prove that the broader presenter/host stack can serve parent/child trees elsewhere. The memo now states that Stage 11 is the bounded move from the former toward the latter, not a claim that transient hierarchy is already done.
Impact: the memo is now describing a real missing seam rather than renaming current behavior.

2. **The AOI-local matcher is now concrete enough, but the memo should be read as requiring internal signal threading, not merely new rules.**
Evidence: the signals the memo now relies on are real, but they are split across current seams. `ComposeFromIntentSectionInput` only carries `engine_key`, `title`, and `prose` in `src/presenter/schemas.py`, while `source_family_key`, `profile`, and `composition_role_hint` live in the source bridge and trace material in `src/presenter/composition_source_bridge.py` and the `compose_from_source(...)` prefix trace in `src/presenter/compose_from_intent.py`. They are not currently passed into the flat planner input shape.
Impact: implementation must explicitly thread those AOI-local signals into the internal semantic page-plan or matcher context. Without that, the revised matcher could still collapse back to title/prose heuristics. This is an implementation requirement implied by the memo, not a reason to reject it.

3. **The proof bar is materially stronger now, but child-contract proof should be treated as part of “valid hierarchy,” not as an optional testing detail.**
Evidence: current transient compose still validates only the top-level adapted payload list in `src/presenter/compose_from_intent.py` and `src/presenter/renderer_contract_enforcement.py`, and still reports `view_count` from top-level ordered views even though child content can appear in content hashing. The revised memo now requires live child rendering and fail-closed hierarchy cases, which is the right direction, but the current code shows why recursive adaptation/validation/count behavior must be part of that proof.
Impact: Stage 11 should only be considered complete if child payloads are adapted, validated, and counted under contract law rather than merely rendered by a permissive host path.

## Direct Answers

- **Is the proposed Stage 11 seam really “hierarchical semantic page planning,” or is the memo just renaming a slightly richer compose-from-intent allowlist?**
The revised memo now describes a real hierarchical semantic page-planning slice. It is no longer just an allowlist expansion because it explicitly requires bounded parent/child planning, host-backed child rendering, semantic surface routing, and a distributed compose-module refactor.

- **Does the repo actually have enough reusable hierarchy/scaffold law to support this stage honestly, or would the planner still be inventing structure the presenter does not really own?**
Partially, and the revised memo now states that honestly. The repo has enough hierarchy/payload law on presenter and result-host paths to make the stage real, but not enough transient-compose-owned law to make it trivial. The planner will still need to add real transient tree ownership, while scaffold reuse should stay bounded and opportunistic rather than be treated as broad existing rollout.

- **Is AOI-first the right bounded implementation target, or does it defer the cross-workflow proof burden too far?**
AOI-first is the right target. The revised memo now uses genealogy as a contract reference rather than pretending genealogy is already a second transient planner consumer, which removes the earlier false symmetry.

- **Is the semantic matcher requirement concrete enough to be implemented inside analyzer-v2 without quietly depending on the external visualizer proposal?**
Yes, with one condition: Stage 11 must explicitly thread AOI-local bridge signals such as `source_family_key`, `profile`, and `composition_role_hint` into the planner or matcher context. With that condition, the revised memo is concrete enough and no longer depends on the external proposal or missing AOI `semantic_visual_intent`.

- **Is the proof bar strong enough to distinguish semantic planning from generic layout churn?**
Mostly yes after revision. It now requires live hierarchy, live host rendering, semantic-family choice, fail-closed behavior, and traces. The one thing that should stay explicit during implementation is recursive child adaptation and contract validation, because the current transient path is still top-level-only there.

- **Does the revised memo now describe the transient-host requirement honestly, or is it still smuggling Stage 13 host work into Stage 11 without naming it?**
It now describes that requirement honestly. The host ask is clearly bounded to the current AOI transient shell or reuse of the existing result-tree seam, and it no longer reads like a claim that generic host law is solved.

- **Are the AOI-local semantic rules concrete enough to drive real planning now, given the absence of AOI `semantic_visual_intent`?**
Yes, if the implementation uses the real current AOI signals the memo names and explicitly threads them into the internal planning context. The absence of AOI `semantic_visual_intent` is no longer a blocker for this bounded slice.

## Checked Absence

I did not find additional materially relevant design docs beyond the usual `communications/` and `docs/` materials. The other markdown files outside those directories are outputs, package metadata, or local notes, and they do not materially change this assessment.

## Residual Implementation Notes

1. Treat source-bridge metadata threading as part of the Stage-11 contract.
The matcher should not rely only on `engine_key`, `title`, and serialized `prose`; it should receive the AOI-local source-family/profile/role signals the memo now names.

2. Treat recursive child adaptation and validation as exit evidence.
The current transient path is still top-level-only in those seams, so the final proof should demonstrate that child payloads are not bypassing contract law.

## Secondary Summary

The revised memo is now aligned with the live codebase and the larger program objective. It scopes an honest AOI-first Stage-11 slice, carries the narrow transient-host requirement explicitly, and narrows the semantic matcher to signals analyzer-v2 can actually own now. The remaining work is implementation precision, not a memo-level scope problem.
