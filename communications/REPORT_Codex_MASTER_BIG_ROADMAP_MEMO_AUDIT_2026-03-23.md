# Audit: MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS

Date: 2026-03-23
Auditor: Codex

## VERDICT

The memo is strategically useful and mostly right about the downstream state of the AOI transient program. The code really does prove a credible AOI-only delivery stack: stricter renderer law on bounded slices, shared-package default renderer ownership, transient compose routes in analyzer-v2, source-backed recomposition from saved AOI truth, and a real hot-path launch from the-critic.

The memo's main distortion is upstream. It talks as if task intake, planning, and engine-chain synthesis are still mostly future work. That is not true of the current repo. `analyzer-v2` already has a substantial orchestrator surface, adaptive objective-driven planner, book sampler, plan review/refinement flow, by-reference launch path, and all-in-one pipeline. The real gap is not "planning does not exist." The real gap is "existing planning is not yet bridged into dynamic composition, source selection, page planning, and a formal minimal host contract."

So the roadmap should be kept, but corrected. Stages 7 and 9 are not "not started." Stage 8 is only partially absent. Stage 13 is more operationally real than the memo admits. Also: there is no relevant `Perspective` or `perspective` docs folder in either repo.

## FINDINGS

1. High: the memo materially understates how much upstream planning already exists in code.
   Evidence:
   - `src/api/routes/orchestrator.py:96` exposes plan generation.
   - `src/api/routes/orchestrator.py:296` exposes the all-in-one analysis pipeline.
   - `src/api/routes/orchestrator.py:333` exposes `analyze-by-ref`.
   - `src/api/routes/orchestrator.py:505` exposes adaptive planning from `objective_key`.
   - `src/orchestrator/adaptive_planner.py:36` defines an LLM planner that reads objectives, book samples, and the full engine/chain catalog, then emits phase-level `chain_key` / `engine_key` plans with decision traces.
   - `src/orchestrator/pipeline.py:49` already runs upload -> plan -> execute, and `src/orchestrator/pipeline.py:219` already does pre-execution revision.
   - `src/objectives/definitions/influence_thematic.json:2` and `src/objectives/schemas.py:7` show a real objective layer, not just a memo placeholder.
   Why this matters:
   - The stage ledger's "Stage 7 not started" and "Stage 9 not started" claims are false against the live code.
   - The planning gap is real, but it is an integration/generalization gap, not a greenfield gap.

2. High: the memo is still too optimistic about "minimal app expectations."
   Evidence:
   - `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:327` merges upstream analyzer discovery with local saved-result snapshots.
   - `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:437` performs snapshot warmup to manufacture a local `analysis_id` before transient launch.
   - `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:472` constructs the hot-path query contract and navigation semantics.
   - `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:110` owns autostart, `return_to`, source-backed launch UI, retry behavior, and developer fallback fixtures.
   - `the-critic/api/server.py:18621` resolves saved-result identity and validates current project/thinker context.
   - `the-critic/api/server.py:20311` proxies source-backed compose to analyzer-v2 and preserves status classes.
   - `the-critic/webapp/src/components/renderers/index.ts:18` still owns view-key and type-level renderer overrides.
   Why this matters:
   - The app is no longer the analytical brain, but it still owns meaningful AOI-specific launch, restore, proxy, and exception-handling logic.
   - Stage 13 is not just a late future formalization problem. The host contract is already implicit in code and should be documented sooner.

3. High: the transient composition path is AOI-bounded by explicit code law, not just by current habit.
   Evidence:
   - `src/presenter/compose_from_intent.py:53` hardcodes `consumer_key = "the-critic"`.
   - `src/presenter/compose_from_intent.py:69` allowlists only four pattern keys.
   - `src/presenter/compose_from_intent.py:77` allowlists only `prose`, `accordion`, and `card_grid`.
   - `src/presenter/compose_from_intent.py:293` rejects any workflow except `anxiety_of_influence_thematic_single_thinker`.
   - `src/presenter/compose_from_intent.py:306` caps requests at four sections.
   - `src/presenter/compose_from_intent.py:359` hardcodes `dossier` and `comparison` source bundle mappings to AOI artifacts.
   - `src/presenter/compose_from_intent.py:509` forces a flat page with one top-level view per section and explicitly blocks parents, children, and tabs.
   - `the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx:35` explicitly says round 12 renders top-level views only.
   Why this matters:
   - The memo says compose-from-intent is AOI-specific "in practice." The stronger code-grounded statement is: it is AOI-specific by validation, allowlist, and source-policy.

4. Medium: the memo is right that downstream composition is farther along than dynamic app composition planning, but it frames the upstream gap too bluntly.
   Evidence for downstream strength:
   - `src/api/routes/presenter.py:368` and `src/api/routes/presenter.py:398` expose transient compose routes.
   - `src/presenter/compose_from_intent.py:263` performs fail-closed contract validation on the transient payloads.
   - `renderers-ui/src/registry.ts:10` centralizes default renderer ownership in the shared package.
   - `the-critic/webapp/src/components/ViewRenderer.tsx:140` renders through shared-package defaults first, with only explicit local seams.
   Evidence for upstream maturity:
   - `src/orchestrator/adaptive_planner.py:44` already selects engines/chains from catalog.
   - `src/orchestrator/by_ref.py:219` already uses adaptive planning on registered corpora.
   What is actually missing:
   - A bridge from existing planning/output contracts into composition source selection and page planning.
   - Today `compose-from-source` still bypasses planner intelligence with fixed profile bundles.

5. Medium: the stage ordering is partly wrong for the code as it exists.
   Evidence:
   - Stage 7/9 work already exists in `src/orchestrator/`.
   - Stage 13 host obligations already exist in `src/api/routes/runs.py:19`, `src/api/routes/results.py:44`, `src/analysis_products/run_contract.py:49`, and `src/analysis_products/result_contract.py:220`.
   - The AOI transient delivery path is already product-reachable from `AoiV2ThematicPanel.tsx:764`.
   Correction:
   - Stage 1 documentary closure is fine as operational cleanup.
   - But the next meaningful code tranche is not more shell work. It is bounded AOI planning for source selection and page composition, using the planner substrate that already exists.
   - The host contract should be formalized earlier, not after the platform pretends to have solved every cross-workflow composition problem.

6. Medium: the stage breakdown misses one concrete platform requirement: a planner-to-presentation bridge contract.
   Evidence:
   - `src/analysis_products/run_contract.py` and `src/analysis_products/result_contract.py` already define consumer-facing run/result contracts.
   - `src/presenter/compose_from_intent.py:359` still reconstructs composition inputs through hardcoded AOI profile bundles instead of a reusable plan/result-to-compose contract.
   Why this matters:
   - The codebase already has analysis planning and already has consumer/result contracts.
   - What it lacks is an analyzer-owned contract that says: given a result and a composition task, what source families are eligible, which were selected, which were rejected, and how does that become a page plan.

7. Low: there is no relevant `Perspective` docs folder in either repo.
   Evidence:
   - No `Perspective` or `perspective` directory exists under the inspected top-level trees for `/home/evgeny/projects/analyzer-v2` or `/home/evgeny/projects/the-critic`.

## CODE-GROUNDED CORRECTIONS

- Replace "Stage 7: Generic task-intake contract — Not started" with: partial. `AnalyzeRequest` and `AnalyzeByRefRequest` already carry task-ish fields such as `research_question`, `depth_preference`, `focus_hint`, `objective_key`, and AOI thinker constraints (`src/orchestrator/pipeline_schemas.py:81`, `src/orchestrator/pipeline_schemas.py:268`). What is missing is a composition-facing generic intake contract with audience/style/source constraints that thin hosts can call directly.

- Replace "Stage 8: Task-to-workflow planner — Not started" with: limited or early partial at best. The system does not yet infer workflow families from open-ended task semantics. `AnalyzeByRefRequest` only accepts genealogy or bounded AOI (`src/orchestrator/pipeline_schemas.py:308`), and the AOI adaptive objective hardcodes `baseline_workflow_key` (`src/objectives/definitions/influence_thematic.json:31`).

- Replace "Stage 9: Task-to-engine / engine-chain planner — Not started" with: partial and already executable. `src/orchestrator/adaptive_planner.py:44` through `src/orchestrator/adaptive_planner.py:126` is already a real engine/chain planner, and `src/orchestrator/pipeline.py:203` already runs it in production code paths.

- Tighten "compose-from-intent is AOI-specific in practice" to: compose-from-intent and compose-from-source are AOI-specific by request validation, allowed renderer/pattern policy, source artifact mapping, and consumer allowlisting (`src/presenter/compose_from_intent.py:53`, `src/presenter/compose_from_intent.py:293`, `src/presenter/compose_from_intent.py:359`, `src/presenter/compose_from_intent.py:509`).

- Add a missing requirement/stage: formalize the planner-to-presentation bridge. The code already has planner outputs and already has run/result manifests; it needs a stable contract that maps planned analysis artifacts into composition-ready source bundles with traceable selected/rejected rationale.

- Pull host-contract formalization forward. The analyzer-side discovery/result contract and the-critic's launch/snapshot/proxy behavior already form a real host contract; leaving that implicit until very late is a mistake.

## WHAT THE MEMO GETS RIGHT

- The memo is right that the last week mostly solved the downstream AOI delivery half first. Round 9 renderer enforcement, round 10 package-backed renderer resolution, round 11 transient compose, round 13 source-backed reconstruction, and round 14 hot-path launch are all visible in code (`src/presenter/renderer_contract_enforcement.py:16`, `renderers-ui/src/registry.ts:10`, `src/api/routes/presenter.py:368`, `the-critic/api/server.py:20311`, `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:764`).

- The memo is right that the consumer app should not get smarter again. The strongest current code seams do keep orchestration in analyzer-v2 and keep the-critic as a host/proxy/launch shell rather than a second analytical planner.

- The memo is right that renderer law is not universal yet. Mainline serve-time enforcement is still allowlisted to a bounded composition mode in `src/presenter/renderer_contract_enforcement.py:16`, even though the transient route validates its own payloads directly.

- The memo is right that lifecycle law is unresolved and should not be blurred. The transient page is still a separate route and separate contract, not a fake job-backed `PagePresentation` (`src/presenter/schemas.py:664`, `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:298`).

- The memo is right that more AOI/the-critic product polish is not the same as more platform. The code already has enough downstream proof to justify shifting engineering weight upstream.

## BEST NEXT STAGE

Best next engineering stage: build a bounded AOI planner-to-compose bridge.

That means:

- keep the workflow fixed to AOI for now
- replace `profile = dossier|comparison` as the primary composition selector with a bounded AOI composition task/request
- reuse the existing `objective_key = influence_thematic` and adaptive-planner substrate instead of pretending planning starts from zero
- introduce an analyzer-owned AOI source catalog for composition, with selected/rejected rationale across synthesis, engagement mapping, findings, report sections, and future AOI artifacts
- emit a composition trace that explains both source selection and page-plan decisions
- formalize the minimal host launch contract at the same time, because the-critic already depends on it operationally

If you mean operational hygiene rather than engineering leverage, close the round-13/14 browser proof tails first. If you mean the next code stage that actually advances the platform, it is not more renderer work and not more transient-page shell work. It is bounded AOI planning that connects the existing orchestrator/result substrate to dynamic composition.
