Approve

# Stage 13 Minimal Generic Host Contract Scope Audit

Audited memo:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md`

## Findings

### 1. The revised memo now handles the remaining Stage 12 risk honestly enough

This was the main blocking issue in the first pass, and it is now substantially fixed.

The live code still has uneven strictness on authored or no-`composition_mode` restore paths:
- `src/presenter/renderer_contract_enforcement.py:120-173` still falls back to `authored_or_unlisted_combination_warn_only`
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx:189-202` still uses `useBoundedV2Workspace(...)` without `compositionMode`
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx:278-301` still fetches single views directly without threading `composition_mode`
- `webapp/src/pages/GenealogyPage.tsx:441`
- `webapp/src/pages/GenealogyPage.tsx:697-809`
- `webapp/src/pages/GenealogyPage.tsx:885-950`

But the memo now says that explicitly instead of implying those paths are already normalized:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md:82-99`

That is the right level of honesty for approval. The memo now treats Stage 12 as strong enough for the current proof seam, not universally clean.

### 2. The memo now describes consumer coupling asymmetry accurately

The revised memo correctly separates the two cases:
- run/result families accept request-level `consumer_key`
- compose families remain structurally tied to `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"`

That matches the code:
- request-level `consumer_key` on result routes:
  - `src/api/routes/results.py:50-157`
- structural compose constraint:
  - `src/presenter/compose_from_intent.py:445-453`
  - `src/presenter/compose_from_intent.py:482-493`
- AOI readiness also surfaces the same compose-family constraint:
  - `src/analysis_products/source_backed_readiness.py:144-176`

The memo now states this asymmetry directly:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md:197-213`

That closes one of the earlier hidden-assumption problems.

### 3. The Host Contract v1 matrix is now concrete enough for this stage

In the first pass, the matrix was too vague on identity and scope ownership. The revised version now includes the missing columns:
- canonical identity field
- identity authority
- authoritative scope channel
- host-local identity translation
- explicit host-owned surface-selection law

See:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md:215-263`
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md:363-379`

Those additions are supported by the live code, which really does split identity and scope this way:
- upstream `job_id` / `v2_job_id` on run/result families:
  - `webapp/src/lib/boundedV2Client.ts:75-166`
- host-local `analysis_id` on saved snapshot families:
  - `webapp/src/hooks/useBoundedV2Workspace.ts:227-318`
  - `webapp/src/pages/GenealogyPage.tsx:811-944`
  - `api/server.py:20368-20395`
- project scope via `X-Project-ID` plus path/query parameters:
  - `webapp/src/contexts/ProjectContext.tsx:60-79`
  - `api/middleware.py:10-58`
  - `api/server.py:20305-20317`
  - `api/server.py:20368-20389`

This is now specific enough for a bounded v1 artifact.

### 4. The host-consolidation claim is now right-sized against the real current substrate

The revised memo no longer pretends the host is still mostly page-local from scratch. It correctly anchors the claim in the shared substrate that already exists:
- `webapp/src/lib/boundedV2Client.ts:75-179`
- `webapp/src/hooks/useBoundedV2Workspace.ts:51-439`
- `webapp/src/pages/AnalysisWorkspacePage.tsx:296-323`

And it still identifies the remaining bespoke areas honestly:
- `webapp/src/pages/GenealogyPage.tsx:587-950`
- `webapp/src/components/influence/AoiV2ThematicPanel.tsx:278-301`
- `webapp/src/pages/AnxietyOfInfluencePages.tsx:662-705`

The memo now reflects that more accurately:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md:301-341`

That is a meaningful improvement. The stage is now scoped around finishing consolidation, not inventing it.

### 5. The memo now describes the AOI source-backed proxy as real host preparation, not a thin pass-through

This was another prior weakness and it is now fixed.

The live AOI source-backed path is clearly a host-preparation family:
- the host launches from `source_analysis_id`, not just direct `source_v2_job_id`
  - `webapp/src/components/influence/AoiV2ThematicPanel.tsx:437-469`
  - `webapp/src/components/influence/AoiV2ThematicPanel.tsx:472-518`
  - `webapp/src/pages/AoiComposeFromIntentPage.tsx:236-261`
- the backend resolves local identity to upstream identity and validates context:
  - `api/server.py:18621-18705`
  - `api/server.py:20311-20365`
- tests confirm the identity-resolution behavior:
  - `tests/test_aoi_v2_routes.py:531-567`

The memo now says that directly:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md:282-299`

That is an accurate description of the current contract boundary.

### 6. The proof bar is now strong enough for a bounded first slice of Stage 13

The upgraded proof bar is materially better than the original AOI-only version.

It now requires:
- a saved Host Contract v1 artifact
- shared host adapter use across AOI and genealogy
- AOI readiness adoption on a real launch surface
- one genealogy readiness consumption case
- proof that contract-covered pages stop building analyzer URLs ad hoc except for documented out-of-scope families

See:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md:412-436`

That is consistent with the live analyzer readiness seam:
- AOI readiness:
  - `src/analysis_products/source_backed_readiness.py:97-210`
- genealogy readiness:
  - `src/analysis_products/source_backed_readiness.py:213-467`
- public route:
  - `src/api/routes/results.py:100-122`

The host still has no actual readiness adoption today:
- repository search for `source-backed-readiness` under `the-critic/webapp/src`, `the-critic/api`, and `the-critic/tests` returned no live adoption hits

But the memo now treats that as required stage work rather than as an already-solved fact. That is the correct framing.

### 7. Stage ordering remains correct

I do not see a remaining sequencing mistake.

The revised memo is still right to:
- keep Stage 13 ahead of Stage 14 lifecycle/session work
- keep `route-task` and `plan-task` outside mandatory Host Contract v1 adoption for this slice

That matches the code:
- advisory orchestrator seams exist:
  - `src/api/routes/orchestrator.py:301-338`
- the-critic still does not consume them:
  - repository search for `route-task|plan-task` under `the-critic/webapp/src`, `the-critic/api`, and `the-critic/tests` returned no matches

And the memo now makes the host-owned routing/surface-selection boundary more explicit:
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md:343-379`
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_scope.md:381-410`

That is a sound bounded Stage 13 slice.

## Direct Answers To The Prompted Questions

### Is Stage 13 really the next missing seam now that Stage 12 has an explicit served-intent law, or does the memo underplay the remaining Stage 12 risk?

Stage 13 is still the next missing seam, and the revised memo no longer underplays the remaining Stage 12 risk in an approval-blocking way.

### Is the proposed Host Contract v1 matrix concrete enough?

Yes for this bounded slice. The added identity, authority, scope-channel, and surface-selection fields make it concrete enough to implement and review.

### Does the memo now describe the consumer coupling asymmetry honestly?

Yes. The distinction between request-level `consumer_key` on run/result families and structural `the-critic` binding on compose families now matches the code.

### Does the current code actually support consolidation onto one shared host adapter layer across AOI and genealogy, or are the workflows still too different?

Yes, for the result-backed families. The shared substrate is already present in `boundedV2Client.ts` and `useBoundedV2Workspace.ts`. AOI source-backed launch remains a special host-preparation family, and the memo now says so.

### Is the memo now right-sized about what consolidation work remains versus what is already covered by `boundedV2Client` and `useBoundedV2Workspace`?

Yes. This was revised appropriately.

### Is the memo correct to keep `route-task` and `plan-task` outside required host-v1 adoption?

Yes.

### Does the memo handle `project_id`, `consumer_key`, `source_analysis_id`, `source_v2_job_id`, and snapshot caching ownership honestly?

Yes, now sufficiently. The new matrix language and proxy/preparation language close the earlier ambiguity.

### Is adopting `source-backed-readiness` in AOI launch plus one genealogy readiness consumption case now enough, or should the proof bar still require broader host adoption?

Yes, now enough for this bounded first slice, because the proof bar also still requires shared adapter adoption and removal of ad hoc URL construction on contract-covered surfaces.

### Is the proof bar strong enough without a second consumer?

Yes. The memo now explicitly frames this as only the first bounded slice of Stage 13 and keeps Stage 13 `Partial` afterward.

### Does the memo clearly separate host navigation/routing, analyzer task routing, host-owned persistence hooks, and analyzer-owned analytical truth?

Yes, sufficiently for approval.

### Does the memo now make host-side surface selection explicit enough as a host-owned v1 concern?

Yes. That point is now stated clearly and grounded in current workflow experience ownership.

## Additional Relevant Docs Checked

I did find additional materially relevant recent memo-trail documents in `communications/` beyond the explicitly listed set:
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md`
- `communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md`
- `communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_completion.md`
- `communications/MEMO_2026-03-23_round14_aoi_transient_hot_path_launch_completion.md`

I did not find additional materially relevant `docs/` files from the past 48 hours beyond the recent roadmap/memo trail. The relevant additions were in `communications/`, not `docs/`.

## Summary

The revised memo is now approvable.

The main issues from the first pass were addressed:
- Stage 12 partiality is now stated honestly
- the consumer-coupling asymmetry is now explicit
- the Host Contract v1 matrix is now concrete enough on identity and scope
- the shared-host-substrate claim is now right-sized
- the AOI compose-from-source proxy is now correctly described as host preparation
- the proof bar is now cross-workflow and stronger

There are still open implementation gaps in the live codebase, but the memo now describes those as Stage 13 work to be done rather than as already-complete facts. That is the right threshold for approval.
