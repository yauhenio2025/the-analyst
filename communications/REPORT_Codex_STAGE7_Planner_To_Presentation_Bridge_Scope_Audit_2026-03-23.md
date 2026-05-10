# Audit: Stage 7 Planner-To-Presentation Bridge Scope

Date: 2026-03-23
Auditor: Codex

## VERDICT

The memo is directionally right, but it is still mislabeled at the most important seam.

It is correct that this is not a greenfield planning problem. `analyzer-v2` already has real planning substrate: plan requests and persisted plans, AOI-specific plan validation, adaptive objective-driven planning, decision traces, all-in-one pipeline execution, and by-reference launch paths. The code proves that clearly in [`src/orchestrator/schemas.py`](/home/evgeny/projects/analyzer-v2/src/orchestrator/schemas.py#L313), [`src/orchestrator/adaptive_planner.py`](/home/evgeny/projects/analyzer-v2/src/orchestrator/adaptive_planner.py#L36), [`src/orchestrator/pipeline.py`](/home/evgeny/projects/analyzer-v2/src/orchestrator/pipeline.py#L49), and [`src/api/routes/orchestrator.py`](/home/evgeny/projects/analyzer-v2/src/api/routes/orchestrator.py#L96).

But the stage as scoped is still much closer to a bounded AOI result-to-composition bridge than a true planner-to-presentation bridge. The current public request is still just `source_v2_job_id + profile`, and the proposed implementation still lives almost entirely inside the presenter. If Stage 7 lands without explicitly binding existing plan/objective truth and the already-real host/result contract into source selection, it will ship a cleaner AOI source resolver and still miss the actual planner bridge.

So:

- Yes, the memo is right that the next gap is a bridge, not greenfield planning.
- Yes, it is right to keep the bridge analyzer-owned and consumer-light.
- No, it is not too conservative to stay AOI-only for this stage.
- Yes, leaving `profile` in place is a smart bounded move, but only if it is clearly demoted to a preset selector.
- Yes, `compose-from-source-v2` is the right resolver bump.
- The single biggest thing the memo still gets wrong is that it does not specify how planner truth and host-contract truth actually enter the bridge. Without that, "planner-to-presentation" is just stage branding.

No relevant `Perspective` docs folder exists in either repo.

## FINDINGS

1. High: the memo still scopes a presenter-side AOI source resolver more clearly than it scopes a planner bridge.

The live source-backed request model is still only `workflow_key`, `consumer_key`, `source_v2_job_id`, `profile`, optional `user_intent`, and optional `style_school` in [`src/presenter/schemas.py`](/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py#L624). The current `compose_from_source()` path immediately rewrites that request into a plain `ComposeFromIntentRequest` after `_build_source_sections()` in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L119). There is no current seam where `WorkflowExecutionPlan.recommended_views`, planner `decision_trace`, or any composition-facing planner contract enters the source-backed path, even though those structures already exist in [`src/orchestrator/schemas.py`](/home/evgeny/projects/analyzer-v2/src/orchestrator/schemas.py#L428) and [`src/orchestrator/adaptive_planner.py`](/home/evgeny/projects/analyzer-v2/src/orchestrator/adaptive_planner.py#L437).

That means the memo is only half-right on question 1. This is not greenfield planning. But the stage, as currently written, is still mostly a result-to-composition refactor with optional plan enrichment, not yet a real planner-to-presentation bridge.

2. High: the current `compose-from-source` path is exactly as hardcoded as the memo says, and the missing contract is obvious in code.

The hardcoding is not subtle:

- `compose-from-source` still stamps `compose-from-source-v1` in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L56).
- The trace prefix is only `source_profile_resolution` in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L137).
- `_build_source_sections()` is an inline `if profile == "dossier"` / else builder over fixed AOI engine bundles in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L359).
- The report is loaded specially from latest phase-output metadata, while the other sources are loaded through AOI artifact lookup in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L420) and [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L434).
- The tests explicitly lock the exact dossier and comparison bundles in [`tests/test_compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/tests/test_compose_from_intent.py#L260).

There is still no analyzer-owned object that records candidate source families, selected families, rejected families, rejection reasons, or materialization rationale. So question 6 has a clear answer: the memo is right about the current hardcoding, and the code proves it directly.

3. High: a meaningful host contract already exists, and the memo still underspecifies it.

The host contract is not hypothetical anymore. `analyzer-v2` already exposes stable run/result surfaces with explicit restore semantics and links:

- `AnalysisResultManifest`, `DiscoverySummary`, `RunSummary`, and their `restore_available`, `restore_reason`, thinker identity, and link fields are in [`src/analysis_products/schemas.py`](/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py#L41), [`src/analysis_products/schemas.py`](/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py#L82), and [`src/analysis_products/schemas.py`](/home/evgeny/projects/analyzer-v2/src/analysis_products/schemas.py#L133).
- Those are served through real routes in [`src/api/routes/results.py`](/home/evgeny/projects/analyzer-v2/src/api/routes/results.py#L44) and [`src/api/routes/runs.py`](/home/evgeny/projects/analyzer-v2/src/api/routes/runs.py#L19).
- The manifest logic already computes staleness, restoreability, and plan-context presence in [`src/analysis_products/result_contract.py`](/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py#L220) and [`src/analysis_products/run_contract.py`](/home/evgeny/projects/analyzer-v2/src/analysis_products/run_contract.py#L97).

The-critic is already coded against that reality:

- `AoiV2ThematicPanel` uses `restore_available` and local snapshot warmup to get a stable `analysis_id` before transient launch in [`AoiV2ThematicPanel.tsx`](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L437).
- The hot path launches with `source_analysis_id`, not raw `source_v2_job_id`, in [`AoiV2ThematicPanel.tsx`](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L472).
- `AoiComposeFromIntentPage` consumes that public shape and only forwards `source_v2_job_id` when present as an override in [`AoiComposeFromIntentPage.tsx`](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L202).
- The-critic backend validates project + thinker + analysis identity before resolving the analyzer call in [`server.py`](/home/evgeny/projects/the-critic/api/server.py#L18621) and [`server.py`](/home/evgeny/projects/the-critic/api/server.py#L20311).

So question 7 also has a clear answer: the meaningful host contract already exists. Stage 7 should preserve it explicitly instead of pretending the only real public coupling is `profile`.

4. Medium: keeping the stage analyzer-owned and consumer-light is the correct call.

The current split is already healthy:

- analyzer-v2 owns source reconstruction and transient composition in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L119)
- the-critic owns source identity resolution, snapshot warmup, routing, and proxying in [`server.py`](/home/evgeny/projects/the-critic/api/server.py#L18621), [`server.py`](/home/evgeny/projects/the-critic/api/server.py#L20311), and [`AoiV2ThematicPanel.tsx`](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L472)

That is already thin-host law. Moving source catalog reasoning into the-critic would be a regression. The memo is right on question 2.

5. Medium: staying AOI-only is not too conservative for this stage.

The AOI bounding is real in code, not just cultural:

- AOI-only validation for source-backed compose lives in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L330).
- The transient page planner is still flat, bounded, and AOI-only in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L475).
- AOI single-thinker planner and pipeline contracts are enforced in [`src/orchestrator/pipeline_schemas.py`](/home/evgeny/projects/analyzer-v2/src/orchestrator/pipeline_schemas.py#L168) and [`src/orchestrator/schemas.py`](/home/evgeny/projects/analyzer-v2/src/orchestrator/schemas.py#L364).

There is no second workflow with the same source-backed transient maturity right now. Forcing cross-workflow generalization into Stage 7 would conflate bridge formalization with workflow normalization. The memo is right on question 3.

6. Medium: leaving public `profile` in place is a good bounded move, but only if its status is explicitly downgraded.

`profile` is clearly part of the current public launch path:

- the-critic hot path sends `profile` in [`AoiV2ThematicPanel.tsx`](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L483)
- the transient proof page reads `profile` from the URL and autostarts on it in [`AoiComposeFromIntentPage.tsx`](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L120) and [`AoiComposeFromIntentPage.tsx`](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L236)
- analyzer request validation still hardcodes `Literal["dossier", "comparison"]` in [`src/presenter/schemas.py`](/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py#L624)

So question 4 is best answered this way: keep `profile` for Stage 7, but only as a preset selector over an analyzer-owned catalog. If Stage 7 leaves `profile` as the hidden source-bundle law, it preserves the wrong coupling. If Stage 7 demotes it to a bounded selection hint, it is the right temporary compromise.

7. Low: `compose-from-source-v2` is the right resolver/version bump, and the existing tests show why.

The semantic behavior is changing materially while the outer route can remain stable. That is exactly what resolver versions are for. It also gives proof artifacts and regressions a clean boundary between hardcoded profile resolution and catalog-backed selection. The current code and tests still pin `compose-from-source-v1` in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L56) and [`AoiComposeFromIntentPage.test.tsx`](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.test.tsx#L33), so the version bump is both justified and operationally useful. That answers question 5: yes, it makes sense.

8. Low: no relevant `Perspective` docs folder exists in either repo.

I checked both `/home/evgeny/projects/analyzer-v2` and `/home/evgeny/projects/the-critic` for directories matching `*perspective*` or `*Perspective*` and found nothing relevant.

## CODE-GROUNDED CORRECTIONS

- Change the memo's central claim from "this stage formalizes the planner-to-presentation bridge" to "this stage formalizes an AOI composition-source bridge with explicit planner hooks." That wording matches the actual request shape and current write scope.

- Add one explicit requirement: the bridge must record whether `load_effective_plan_context()` was used, whether plan context was missing, and whether objective metadata came from run-specific truth or workflow defaults. The supporting seam already exists in [`src/executor/plan_context.py`](/home/evgeny/projects/analyzer-v2/src/executor/plan_context.py#L23).

- Add one explicit non-goal: Stage 7 does not yet consume `WorkflowExecutionPlan.recommended_views` as authoritative page law. Right now the transient planner is still its own bounded planner in [`src/presenter/compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L475). If that is meant to change, the memo needs to say so directly.

- Tighten the `profile` language. The memo should say: `profile` remains public only as a bounded preset over source selection. It is not the composition task contract, and it is not the source bundle itself.

- Add one host-contract preservation rule: the stable product identity remains project + thinker + saved result identity on the-critic side. `source_v2_job_id` can stay the analyzer-facing resolver input, but Stage 7 must not force the consumer to promote raw analyzer job identity into the product contract. The current seams proving this are in [`server.py`](/home/evgeny/projects/the-critic/api/server.py#L18621), [`server.py`](/home/evgeny/projects/the-critic/api/server.py#L20311), and [`AoiV2ThematicPanel.tsx`](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L437).

- Keep the `compose-from-source-v2` bump. Also update the tests in both repos that currently hardcode `compose-from-source-v1`, because the existing fixtures already treat resolver version as stable behavior.

- Consider one small analyzer-side contract extension outside the presenter module. The host/result contract already knows artifact families, restore state, and thinker identity in [`src/analysis_products/result_contract.py`](/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py#L273). Stage 7 does not need to expose the whole catalog publicly, but pretending the bridge is purely a presenter-private concern leaves useful upstream truth unused.

## WHAT THE MEMO GETS RIGHT

- It is correct that the next real gap is a bridge, not "build planning from zero." The orchestrator substrate is already real.

- It is correct to keep this stage analyzer-owned and consumer-light. The-critic should not become the source-catalog brain.

- It is correct not to widen into cross-workflow generalization yet. The code is still too AOI-bounded for that to be a clean Stage 7 move.

- It is correct to keep the public route stable. The consumer already depends on that path operationally.

- It is correct to separate source catalog resolution, source selection, and section materialization. That is the missing legibility seam in the current code.

- It is correct to prefer plan/objective truth when available but not block on universal plan-context richness. The code already has mixed plan-context availability, and the bridge must survive that honestly.

## BEST NEXT MOVE

Implement Stage 7 as a bounded AOI composition-source bridge, but stop pretending that presenter-internal cleanup alone is enough.

The concrete next move should be:

- keep `POST /v1/presenter/compose-from-source` and keep `profile` as a bounded preset
- replace `_build_source_sections()` with an analyzer-owned catalog -> selection -> materialization pipeline
- make the trace explicitly show candidate families, selected families, rejected families, and whether plan/objective context participated
- stamp `compose-from-source-v2`
- preserve the current the-critic host contract, especially the `source_analysis_id`-first launch doctrine

If the stage does that, it is a good Stage 7. If it only replaces inline `if profile == ...` with a fancier presenter helper and never specifies how planner truth or host-contract truth enters the flow, then it is not really the planner-to-presentation bridge. It is just AOI source-backed compose cleanup with better trace labels.
