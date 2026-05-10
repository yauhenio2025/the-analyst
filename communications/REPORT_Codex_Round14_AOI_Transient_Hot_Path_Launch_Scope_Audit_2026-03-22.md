Approve

# Round 14 Scope Audit

## Findings

No blocking findings remain after revision.

The memo now locks the three scope seams that were previously too loose:

- the launch seam is explicitly inside [`AoiV2ThematicPanel`](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L85), not vaguely page-level ([`MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md#L154))
- source selection is now explicitly panel-local, based on current selected source state plus deterministic sorting of the already-loaded saved-results list before any "newest" fallback becomes product law ([`MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md#L177))
- the transient route handoff is now explicitly one-click, with `profile`, `source_analysis_id`, thinker context, return target/backlink, and auto-run on landing all in scope ([`MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md#L212))

The revision also closes two planning gaps that mattered:

- it now states the round-13 browser-proof gap honestly and gives an explicit disposition rule for whether round 14 must capture it first or subsume it in the round-14 artifact bundle ([`MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md#L27))
- it now makes blocking-loading and no-saved-result empty-state behavior explicit enough for execution planning without reopening streaming/polling scope ([`MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md#L243))

## Direct Answers

1. Is hot-path transient launch adoption the right next bounded move, or is the stronger next tranche actually transient-to-authored promotion or something else?

Yes. Hot-path transient launch adoption is still the right next bounded move.

The round-13 completion memo already says the next question after source-backed launch is how to adopt the transient experience from the real AOI user path without collapsing lifecycle law too early ([`MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_completion.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_completion.md#L157)). Promotion remains a larger tranche because the transient compose pipeline is still explicitly transient: it generates ephemeral views with `save=False`, normalizes them onto `compose_from_intent_transient`, flattens them to top-level views, and marks them `status="draft"` rather than turning them into a durable authored object ([`compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L601), [`compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L642)).

2. Does the memo put the launch seam in the right place?

Yes now.

The revision removes the earlier ambiguity and explicitly fixes the seam inside [`AoiV2ThematicPanel`](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L85), which matches the live ownership boundary: the panel already owns AOI result discovery and restore behavior, while the parent thinker page only owns thinker/project routing context ([`AnxietyOfInfluencePages.tsx`](/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx#L738), [`AnxietyOfInfluencePages.tsx`](/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePages.tsx#L833)).

3. Is `source_analysis_id` the right normal UI handoff key, with raw `source_v2_job_id` kept out of the normal product path?

Yes.

The backend already treats `source_analysis_id` as the product-grade identity key: it validates that the saved result belongs to the current project + thinker, extracts the persisted `_v2_job_id`, rejects mismatches, and only then proxies the analyzer request ([`server.py`](/home/evgeny/projects/the-critic/api/server.py#L18621), [`server.py`](/home/evgeny/projects/the-critic/api/server.py#L20311)). That remains the right normal doctrine.

Residual note, not a blocker: the execution plan should still confirm how the panel resolves `source_analysis_id` for any upstream-restored row that lacks a local snapshot id today. That can stay an implementation note rather than a scope change.

4. Does the memo correctly preserve the lifecycle boundary between job-backed AOI workspace law and transient compose law?

Yes.

The revision keeps the transient runtime on its own dedicated route and shell, requires one-click navigation into that route rather than embedding the transient shell inside the AOI panel, and keeps the job-backed workspace untouched ([`MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md#L212)). That still matches the live code split:

- the-critic resolves identity and proxies the source-backed launch ([`server.py`](/home/evgeny/projects/the-critic/api/server.py#L20311))
- analyzer-v2 reconstructs bounded sections and reuses the transient compose flow ([`compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L119))
- the dedicated transient route remains separate from the job-backed workspace route ([`routes.tsx`](/home/evgeny/projects/the-critic/webapp/src/routes.tsx#L254))

5. What assumptions are too loose, too optimistic, or contradicted by the code?

No blocking contradictions remain after the revision.

The memo now matches the live repo seams well enough for execution planning. The only residual implementation caveat is the upstream-only `analysis_id` edge case noted above, which is narrower than a scope objection.

6. What should the execution plan lock down explicitly if the scope is directionally right?

The memo now already locks the important scope decisions. The execution plan mainly needs to carry them through concretely:

- explicit panel state for the currently selected source identity
- deterministic sorting of panel saved results before fallback launch
- exact route/query/backlink contract for one-click launch
- explicit proof-note disposition for the pending round-13 browser artifacts versus round-14 subsumption
- focused tests for identity preservation, deterministic fallback, fail-closed no-result behavior, and no runtime widening

## Residual Notes

- The revised memo is correct to treat round-14 proof as optionally subsuming the pending round-13 browser proof, but the execution plan and the eventual proof note should pick one disposition explicitly and not leave that ambiguous at closeout ([`MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round14_aoi_transient_hot_path_launch_scope.md#L27)).
- The scope is now strong enough for planning, but implementation should still verify how `source_analysis_id` is resolved for any upstream-restored row that does not already carry a local snapshot match in panel state.

## Docs Note

No relevant "Perspective" docs folder exists in either workspace root.

I checked both `/home/evgeny/projects/analyzer-v2` and `/home/evgeny/projects/the-critic` for directories or files matching `*Perspective*`, and nothing relevant exists. The materially relevant documents for this decision remained the round-8 roadmap vision, the dynamic-bespoke vision document, the round-11/12/13 completion trail, the current AOI hot-path memo in the-critic, and the Stage 9 AOI cutover runbook.

## Bottom Line

The revised memo is now technically grounded and execution-plan ready.

It chooses the right next move, puts the launch seam in the right place, preserves the lifecycle boundary, and is explicit enough about source identity, deterministic fallback, one-click handoff, and proof discipline to earn approval.
