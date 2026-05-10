# Report: Stage 8 Task Intake And Workflow Routing Scope Audit

Verdict: `Approve after revision`

## Findings

### 1. The memo is directionally right, but it overstates how ready the current orchestrator substrate is for task intake and workflow routing

The larger program direction is correct. The canonical roadmap wants analyzer-v2 to move from user task -> analysis choice -> workflow/engine planning -> UI composition, while consumer apps become thin hosts (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:45-66`, `:989-998`).

But the live code is not yet a task router. It is still mostly a planner/executor stack that assumes workflow or objective identity is already known:

- `src/orchestrator/schemas.py:346-412` still frames planning around a supplied `workflow_key`, and the AOI validator only runs after that workflow is already selected.
- `src/orchestrator/pipeline_schemas.py:121-147` and `:288-335` keep `workflow_key` on both direct and by-ref launch requests, with objective selection remaining optional metadata rather than a routing decision.
- `src/orchestrator/planner.py:266-269` filters the catalog by `request.workflow_key or "intellectual_genealogy"` before planning, and `:338-354` stamps that workflow into the plan.
- `src/orchestrator/adaptive_planner.py:471-481` and `:568-588` plan inside an already-selected objective, then emit `workflow_key=objective.baseline_workflow_key or "adaptive"`. That is objective-conditioned planning, not intake-time workflow routing.
- `src/orchestrator/pipeline.py:121-128` creates jobs with `workflow_key = request.workflow_key or "intellectual_genealogy"`.
- `src/api/routes/orchestrator.py:65-505` exposes `/capability-catalog`, `/plan`, `/analyze`, `/analyze-by-ref`, `/sample`, and `/plan/adaptive`, but no task-intake or `route-task` endpoint exists today.

Revision required:

- Change the memo’s “real routing/planning substrate” claim to “real planning substrate with only partial routing ingredients”.
- Treat Stage 8 as a genuinely new intake/routing layer built on top of existing planning code, not as a near-finished router that only needs a thin wrapper.

### 2. The memo understates how workflow-specific the current downstream launch contract still is

The most important current seam is not just “who picks the workflow.” It is that downstream launch payloads still diverge materially by workflow:

- `src/orchestrator/pipeline_schemas.py:320-335` requires AOI by-ref launches to use `target_chapters`, while genealogy by-ref launches must use `target_chapter_external_doc_keys`.
- `src/orchestrator/by_ref.py:46-62` branches on workflow before chapter refs are even normalized.
- `src/orchestrator/by_ref.py:129-144` applies AOI-only prior-work validation for `selected_source_thinker_id` and `source_document_id`.
- `src/orchestrator/by_ref.py:191-216` forwards the chosen `workflow_key` directly into the plan request.
- `the-critic/api/server.py:17792-17894` builds an AOI-specific registered-corpus payload with a synthetic target, structured target chapters, thinker identity, and source-document inventory.
- `the-critic/api/server.py:17897-18030` builds a different genealogy payload shape from project docs, context docs, prior works, and target chapter external doc keys.
- `the-critic/docs/FEATURES.md:389-401` explicitly says starts still launch through The Critic because project/document loading remains host-owned.

This means the Stage 8 bounded claim is currently too strong at the phrase:

- “return a stable routing contract the host can follow without owning the analytical decision”

That sentence is only safe if “stable routing contract” means:

- the host no longer decides the analytical workflow family
- but the host may still have to satisfy workflow-specific corpus-binding requirements that analyzer-v2 returns explicitly

Revision required:

- Add an explicit distinction between analytical routing and downstream corpus/launch preparation.
- Make the Stage 8 response contract include the currently required downstream contract shape, not just `workflow_key` plus an outcome label.
- Add fields such as:
  - `launch_contract_kind`
  - `required_fields`
  - `required_host_preparation`
  - `source_sufficiency_status`

### 3. The Stage 7 bridge is real, but it should not be used as evidence that general routing/intake is already mostly solved

Stage 7 did land a real AOI bridge. The Stage 7 memo and proof are honest about that bounded claim and equally honest about what remains open (`communications/MEMO_2026-03-23_stage7_aoi_source_to_composition_bridge_completion.md:16-28`, `:112-123`; `communications/PROOF_2026-03-23_stage7_aoi_source_to_composition_bridge.md:89-120`).

However, the live presenter bridge is still tightly bounded:

- `src/presenter/compose_from_intent.py:1` defines itself as “Bounded transient compose-from-intent orchestration for AOI.”
- `src/presenter/compose_from_intent.py:48-53` hard-codes `consumer_key="the-critic"` and AOI-specific resolver versions.
- `src/presenter/compose_from_intent.py:101-112` scopes both source-less and source-backed compose to AOI.
- `src/presenter/compose_from_intent.py:293-341` rejects non-AOI workflows and non-`the-critic` consumers.
- `src/presenter/compose_from_intent.py:391-401` explicitly keeps the page planner flat: one top-level view per section, no parents, no children, no tabs.
- `src/presenter/composition_source_bridge.py:1` is an AOI source-to-composition bridge, not a cross-workflow bridge.
- `src/presenter/composition_source_bridge.py:23`, `:28-97`, `:291-333`, and `:336-381` are built around AOI-only objective fallback, AOI-only source families, and AOI-only preset selectors.
- `src/presenter/composition_source_bridge.py:638-689` enriches trace with plan context, but that is not a general routing trace framework.
- `src/presenter/schemas.py:613-635` still requires `workflow_key` even for transient composition contracts.
- `src/api/routes/presenter.py:368-428` documents both routes as AOI-only.

This also matches the older vision doc’s own scope statement: `communications/DYNAMIC_BESPOKE_APPS_VISION.md:7` explicitly says engine selection and execution are out of scope there.

Revision required:

- Keep Stage 8 framed as “the next upstream seam after a bounded AOI downstream bridge,” not as if downstream AOI composition already gives a general routing substrate.

### 4. Objective metadata exists, but it is not yet strong enough to justify “implementation-ready” routing claims by itself

The repo does contain objective definitions, and they are useful. But they are still planner guidance, not a complete routing ontology:

- `src/objectives/schemas.py:7-66` defines high-level goals, quality criteria, engine affinities, `baseline_workflow_key`, and preferred views. It does not define routing confidence, source sufficiency, or host-contract policy.
- `src/objectives/definitions/genealogical.json:40-46` hard-codes the genealogy baseline workflow.
- `src/objectives/definitions/influence_thematic.json:24-34` hard-codes the bounded AOI single-thinker baseline and explicitly says to keep the selected source thinker fixed.
- `src/objectives/definitions/logical.json:27-28` has `baseline_workflow_key: null` and no preferred views.

So the memo is right that there is substrate. But it is not yet enough to say Stage 8 is implementation-ready just because objectives and workflows both exist.

Revision required:

- Explicitly state that Stage 8 still needs a new intake schema, a bounded routing taxonomy, confidence semantics, and source-sufficiency rules.
- Do not imply that `objective_key` metadata already solves routing.

### 5. Hidden AOI and The Critic coupling is heavier than the memo currently signals

The current thin-host story is still substantially AOI-shaped and The-Critic-shaped:

- `the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:182-195` derives workflow from the URL and requires AOI thinker context from query params.
- `the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:601-648` sends `workflow_key` on launch and adds AOI thinker identity fields only when the workflow is AOI.
- `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:21-24` hard-codes AOI workflow and `consumer_key="the-critic"`.
- `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:59-67` bakes those values into the default transient compose request.
- `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:110-124` reads AOI-specific query params such as `selected_source_thinker_id`, `source_analysis_id`, `source_v2_job_id`, and `profile`.
- `the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx:202-233` always launches the AOI source-backed compose path with thinker identity and preset profile.
- `the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx:472-518` navigates into an AOI-specific compose route carrying AOI-specific query params.
- `the-critic/webapp/src/lib/composeFromIntentClient.ts:149-177` posts to an AOI-specific proxy route.
- `the-critic/webapp/src/types/transientCompose.ts:7-26` keeps workflow identity and AOI-specific source-backed fields in the client contract.
- `the-critic/communications/MASTER_MEMO_CURRENT.md:35-39` explicitly treats the AOI-specific launch route and thinker identity propagation as intentional contract, not accidental implementation detail.

Revision required:

- Add a paragraph in the Stage 8 memo saying current host thinness is only partially generalized.
- Name `selected_source_thinker_id`, AOI-specific source identity, and workflow-specific proxy routes as real current coupling, not incidental residue.

### 6. The memo’s proof standard is not yet strict enough

The existing proof standard in the memo (`communications/MEMO_2026-03-23_stage8_task_intake_and_workflow_routing_scope.md:330-342`) requires AOI routing, genealogy routing, one unsupported case, and saved routing traces.

That is necessary, but not sufficient.

A Stage 8 proof that only shows labels and traces could still hide the real contract gap. The proof also needs to show that the routing response can be turned into a currently valid downstream launch contract without the host re-deciding the workflow analytically.

Additional proof requirements should be added:

1. One AOI task routed without a supplied `workflow_key`, then transformed into a launch contract that matches the live AOI requirements now enforced by `AnalyzeByRefRequest`, `by_ref.py`, and The Critic’s AOI launch builder.
2. One genealogy task routed without a supplied `workflow_key`, then transformed into a launch contract that matches the live genealogy by-ref contract.
3. One insufficient-source case that fails closed specifically because required source bindings are missing, not just because generic confidence is low.
4. Contract-level tests or fixtures proving that returned `required_fields` and `required_host_preparation` match current live downstream routes.

Without that, Stage 8 could produce persuasive routing prose while still leaving the real host seam implicit.

### 7. The memo needs tighter stage-ordering language so Stage 8 does not accidentally claim later-stage work

The roadmap order matters here:

- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:989-998` places task intake/routing before engine-planner generalization, cross-workflow source-backed substrate, rich semantic page planning, and host-contract formalization.
- The stage ledger marks Stage 7, Stage 8, Stage 9, Stage 12, and Stage 13 as only partial today (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1037-1044`).
- `communications/MEMO_2026-03-23_stage7_aoi_source_to_composition_bridge_completion.md:16-28` already says task intake, workflow routing, engine-planning, and page-law integration are still open.
- `docs/MEMO_2026-02-19_orchestrator_vision.md:3-5` is still a planning/requirements memo, not proof that a generalized orchestrator already exists.
- `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md:1-3` is explicitly still a proposal.

So the memo should not let readers infer that Stage 8 delivers:

- general planner-driven execution selection
- cross-workflow source normalization
- rich page law
- a truly stable universal host contract

Revision required:

- Keep “route-first, not full-dispatch-first.” That part is correct.
- But weaken any sentence that sounds like Stage 8 already yields a generally stable host contract.
- Rephrase Stage 8 as the point where the host contract becomes more explicit, not the point where it is effectively solved.

### 8. No relevant Perspective docs folder exists in the inspected repos

I checked for relevant `Perspective` docs/folders in both repos and found none:

- analyzer-v2 search at repo root to max depth 3: no matches
- `/home/evgeny/projects/the-critic` search to max depth 3: no matches

That absence should be stated explicitly in the Stage 8 record, as requested.

## Secondary Summary

The Stage 8 direction is correct and fits the larger program objective. The master roadmap explicitly says the next coherent move after the bounded AOI source-to-composition bridge is to move upstream into composition-facing task intake and workflow routing rather than adding more AOI/the-critic glue (`communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:985-998`).

The problem is not the chosen direction. The problem is precision. The memo currently describes the existing substrate in a way that can be read as “routing is mostly there.” The live code says something narrower:

- planning substrate is real
- AOI composition bridge substrate is real
- workflow routing and stable host-contract expression are still largely to be built
- host-side corpus binding is still workflow-specific

## Recommended Memo Revisions

1. In “What Already Exists,” replace “real routing/planning substrate” with “real planning substrate plus partial routing ingredients.”
2. In the bounded claim, replace “stable routing contract the host can follow” with language that explicitly separates analytical routing from downstream host preparation.
3. In the proposed response contract, add explicit downstream contract fields:
   - `launch_contract_kind`
   - `required_fields`
   - `required_host_preparation`
   - `source_sufficiency_status`
4. Add one paragraph that explicitly says Stage 7 substrate is AOI-only, The-Critic-only, and flat-page-only.
5. Add one paragraph that explicitly says current AOI and genealogy launches still require different host-owned corpus shaping.
6. Expand the proof standard so the returned routing decision must be shown to map onto real current downstream contracts, not only traces and confidence scores.
7. State explicitly that no relevant Perspective docs folder was found.

## Final Assessment

Approve the Stage 8 direction after revision.

It is the right next upstream move, and the memo’s route-first discipline is correct. But it should be revised so it does not overstate current routing readiness, understate AOI/The-Critic coupling, or imply that Stage 8 alone closes the host-contract problem that the roadmap still places later.
