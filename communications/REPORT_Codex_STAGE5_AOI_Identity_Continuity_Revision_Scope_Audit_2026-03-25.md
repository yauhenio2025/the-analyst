# Audit: Stage 5 AOI Identity Continuity Revision Scope

Date: 2026-03-25
Reviewer: Codex
Memo under review: `communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md`

## Verdict

Approve with revisions.

## Findings

### 1. Medium: the memo should explicitly include canonical `source_v2_job_id` handoff in the scoped seam, not just warmed `source_analysis_id`

The live proof shows that planning is keyed by canonical upstream identity, but the planner-backed launch drops that identity before compose. The authoritative artifact keeps `source_v2_job_id` in the routed/planned saved-result context, then the final browser URL and host compose request carry only `source_analysis_id` and no `source_v2_job_id` in [PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json#L12) and [PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json#L744). The current host code does exactly that in [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L653), while the compose page would forward `source_v2_job_id` if present in [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L230) and [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L429). This omission is not hypothetical; it is currently test-enshrined in [AoiV2ThematicPanel.test.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx#L396).

Implication: the memo's "compose proxy validation" bucket is directionally right, but it should name panel-to-compose canonical identity propagation explicitly. Otherwise the implementation can fix warmup persistence yet leave a known host-side identity-loss point undocumented and untested.

### 2. Medium: warmup is not the first broken hop; the first broken durable hop is `v2_run_references`

The memo frames the seam partly as "how `the-critic` warms a local AOI snapshot" in [MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md#L55). The code is more specific: warmup already copies thinker identity from `v2_run_references` into the local snapshot in [server.py](/home/evgeny/projects/the-critic/api/server.py#L20001), and the compose validator then checks either persisted snapshot identity or run-ref identity in [server.py](/home/evgeny/projects/the-critic/api/server.py#L18721) and [server.py](/home/evgeny/projects/the-critic/api/server.py#L18790). The run-ref writer already has the right columns in [server.py](/home/evgeny/projects/the-critic/api/server.py#L18627).

Direct SQLite inspection of `/home/evgeny/projects/the-critic/data/the_critic.db` confirmed the proof row for `v2_job_id = proof-round5-adaptive-aoi-dossier-final-1774100000` has blank `selected_source_thinker_id` and `selected_source_thinker_name`, and the warmed snapshots `gen-v2-c03d584f4a4f` and `gen-v2-c85ddc22fe95` also have blank thinker fields in `genealogy_analyses.pass_results`.

Implication: the memo should tell the implementor to repair durable run-ref truth first, then ensure warmup projects that truth into `pass_results`. If the implementation only rewrites warmup mechanics, it risks fixing the wrong layer.

### 3. Medium: the regression section is still too loose to prevent this seam from reopening through the current host behavior

The memo's regression requirement in [MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md#L97) is pointed in the right direction, but it is not yet concrete enough for the actual failure shape.

Current coverage proves only part of the seam:
- the backend covers `_resolve_source_backed_compose_identity` conflict handling and proxy payload wiring in [test_aoi_v2_routes.py](/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py#L534) and [test_aoi_v2_routes.py](/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py#L573)
- the frontend currently asserts the normal launch path omits `source_v2_job_id` in [AoiV2ThematicPanel.test.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx#L396)
- warmup tests only assert that an `analysis_id` comes back, not that thinker identity survives into the persisted snapshot in [AoiV2ThematicPanel.test.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx#L1040)

Direct DB inspection also showed many warmed AOI snapshots for the same proof job, all missing thinker identity. Because `_resolve_latest_saved_aoi_result` chooses the newest matching saved result in [server.py](/home/evgeny/projects/the-critic/api/server.py#L18749), the regression story should cover repeated warmup/latest-snapshot behavior, not just one happy-path cache call.

Implication: the memo should require both backend ownership in `the-critic/tests/test_aoi_v2_routes.py` and at least one frontend test proving planner-backed navigation preserves canonical source identity across the page handoff.

### 4. Low: the memo is otherwise correctly refusing to reopen selector/provider scope and correctly preserves program order

The proof artifact shows `timeout_s = 45`, `max_retries = 0`, `exception_class_name = null`, and `provider_outcome = success` in [PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_diagnostic_requests_2026-03-25.json#L18). That matches the landed analyzer code and tests in [task_planner.py](/home/evgeny/projects/analyzer-v2/src/orchestrator/task_planner.py#L727), [llm/client.py](/home/evgeny/projects/analyzer-v2/src/llm/client.py#L31), and [test_task_planner.py](/home/evgeny/projects/analyzer-v2/tests/test_task_planner.py#L565). The memo is therefore right not to reopen selector/provider work by default.

The roadmap call is also right. The draft roadmap already says the immediate move is one more bounded Stage 5 continuity repair slice and explicitly says this is recalibration, not reorder, in [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L181). The canonical ledger says the same in [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1167) and [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1265).

## Direct Answers

1. Does the codebase evidence support treating host-side AOI identity continuity as the real current blocker?

Yes, with one important nuance: the first broken durable hop is `v2_run_references`, and the current planner-backed host handoff also drops canonical `source_v2_job_id`.

2. Is the memo correctly refusing to reopen selector/provider scope by default?

Yes.

3. Is the planned fix surface bounded enough?

Yes, if revised to say the bounded seam includes:
- run-ref identity truth/backfill
- snapshot projection of that truth into local `pass_results`
- planner-backed handoff preserving canonical `source_v2_job_id`
- compose proxy validation over those identities

That is still a bounded Stage 5 repair slice, not analyzer-v2 rework and not Tranche 3.

4. Is the required regression coverage concrete enough to prevent this seam from silently reopening?

Not yet. It needs the revisions below.

5. Does the memo preserve the right program order?

Yes.
- Update the roadmap slightly: yes
- Recalibrate the immediate plan: yes
- Not pivot phases: yes

6. Is there any hidden dependency or code-path wrinkle?

Yes.
- The host currently knows the canonical `source_v2_job_id` during planning but intentionally drops it on navigation.
- Repeated warmup creates many local snapshots for the same proof job, so newest-snapshot behavior needs explicit coverage.

7. Is the memo honest that even after this fix, Stage 5 may still fail later for other reasons?

Yes. Its caveat at [MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_identity_continuity_revision_scope.md#L34) is appropriately honest.

## Recommended Revisions Before Implementation

1. Revise the scope text so the seam is named as `run_ref truth -> warmed snapshot projection -> panel/compose canonical-id handoff -> compose validation`, not just "snapshot warmup / local identity / validation."
2. Add an implementation note that the first diagnostic check is whether the local `v2_run_references` row for the proof source already exists and whether its AOI thinker fields are null.
3. State test ownership explicitly: the new regression tests belong in `the-critic`, primarily `/home/evgeny/projects/the-critic/tests/test_aoi_v2_routes.py`, with one frontend handoff test in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx`.
4. Add one required regression proving planner-backed navigation carries canonical `source_v2_job_id` into `/compose-from-intent`, and one required regression proving the newest warmed AOI snapshot for a repeated warmup sequence retains thinker identity and passes compose validation.
