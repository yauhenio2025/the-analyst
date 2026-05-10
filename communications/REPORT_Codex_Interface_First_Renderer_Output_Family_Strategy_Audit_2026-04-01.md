# Codex Audit: Interface-First Renderer / Output-Family Strategy

## Verdict

approve with corrections

The memo is directionally right about where to attack the next layer of generalization. The current codebase already treats consumer capability, renderer choice, and served-payload validation as analyzer-owned seams, which supports moving further upstream rather than building per-engine app shells. But the memo overstates how close the code is to a true renderer/output-family law. Current composition is still bounded, workflow-shaped, and partially manual.

## Findings

1. The strongest evidence for the memo is real: analyzer-v2 already owns the renderer/consumer boundary more than the host does.

   `src/consumers/schemas.py:46-56` models consumer support as `supported_renderers` and `supported_sub_renderers`. `src/presenter/manifest_builder.py:105-135` adapts unsupported renderers at assembly time. `src/presenter/renderer_contract_enforcement.py:128-135` makes transient compose outputs strict and `src/presenter/renderer_contract_enforcement.py:209-242` fails closed on contract issues. This supports the claim that future work should continue upstream.

   Correction: the inversion is not complete. `src/renderers/schemas.py:107-111` still carries legacy `supported_apps`, and `src/renderers/registry.py:120-148` still falls back to it.

2. The renderer catalog is small at the top level, but not at the full interface level.

   There are 9 top-level renderer definitions in `src/renderers/definitions/`, 6 reusable view patterns in `src/views/patterns/`, and 20 sub-renderer definitions in `src/sub_renderers/definitions/`. `src/sub_renderers/schemas.py:1-6` makes sub-renderers first-class catalog entries, so they are part of the real UI vocabulary, not implementation noise. Git history since 2026-03-01 shows the top-level renderers mostly hardened rather than expanded, while sub-renderers are still being added. So the memo is plausible if "family" means a smaller abstraction over these keys, not if it means the current key list is already frozen.

3. Current composition law has reusable seeds, but it is still too workflow-shaped to treat output-family/placement-family generalization as already achieved.

   `src/presenter/compose_from_intent.py:72-82` hard-limits transient planning to 5 allowed patterns and 4 allowed renderer types. `src/presenter/compose_from_intent.py:148-189` hard-codes supported handoff kinds and per-consumer admission. `src/presenter/compose_from_intent.py:703-747` only knows one parent-grouping law: mixed working content plus closeout becomes a `tab` parent. `src/presenter/compose_from_intent.py:778-800` resolves semantic role through `composition_role_hint`, engine-key maps, and title-token heuristics. `src/presenter/bounded_dynamic_composition.py:66-83` still binds composition modes directly to AOI/genealogy workflows. This is a strong bounded substrate, not a generic family contract layer yet.

4. "One extra LLM call to fit data into the interface" is not a sound description of current risk.

   `src/views/generator.py:322-348` uses an LLM to generate each view definition. `src/transformations/executor.py:139-154` and `src/transformations/executor.py:241-298` usually use another LLM pass to extract renderer-shaped structured data, plus optional JSON repair. The current transient path can therefore be multiple LLM steps per section, not one extra adapter call.

   The validation layer is helpful but not strong enough to erase this risk. `src/renderers/definitions/card_grid.json`, `src/renderers/definitions/accordion.json`, `src/renderers/definitions/tab.json`, `src/renderers/definitions/prose.json`, and `src/renderers/definitions/evidence_trail.json` mostly validate broad shapes, not deep semantic correctness; `src/renderers/definitions/raw_json.json` accepts anything; `src/renderers/definitions/evidence_trail.json` explicitly allows arbitrary extra fields. `src/presenter/renderer_contract_enforcement.py:209-242` proves fail-closed contract shape, not stable semantic projection quality.

5. Current consumer adaptation is still crude.

   `src/presenter/manifest_builder.py:122-135` only falls back to `raw_json` when a consumer cannot render a view. That is a useful safety seam, but it is not yet family-aware graceful degradation. The AOI canary proofs explicitly rely on this bounded raw-json fallback for the report leaf in transient mode (`tests/test_aoi_canary_contract.py:130-218`). That means consumer plurality has been proved more than consumer adaptation generality has.

6. The repo already has a natural place for the metadata the memo wants.

   `src/engines/schemas_v2.py:327-366` already exposes `composability` and `output_contract` on capability definitions. AOI capability definitions already use them; for example `src/engines/capability_definitions/aoi_thematic_synthesis.yaml:67-111` declares shared dimensions and a JSON output contract. But a repo scan shows only 4 of 28 capability definitions currently declare `output_contract`, and all 4 are AOI definitions. That is the clearest sign that the interface-first direction is promising but not yet broadly encoded.

## Code-Backed Confirmations

The larger strategic framing in the roadmap is aligned with this memo. The canonical target remains analyzer-v2 as the brain and hosts as thin shells in:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

The current code already proves several important interface-first seams:

- Consumer capability is modeled upstream in `src/consumers/schemas.py:46-56`.
- Transient compose outputs are strict at the served boundary in `src/presenter/renderer_contract_enforcement.py:128-135` and `src/presenter/renderer_contract_enforcement.py:209-242`.
- Tree-aware transient planning exists, including parent/child tab shells and hashed contract/content manifests, in `src/presenter/compose_from_intent.py:369-552` and `src/presenter/compose_from_intent.py:1452-1519`.
- AOI source-backed composition already uses bounded source families and composition-role hints in `src/presenter/composition_source_bridge.py:33-102` and `src/presenter/composition_source_bridge.py:223-316`.
- Thin-host proof consumers really are thin at the declared renderer surface level; for example `src/consumers/definitions/aoi-canary.json:1-31` only declares a small renderer set and no AOI-local analytical logic.

Focused verification also passed on the current worktree:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py tests/test_served_renderer_contract_policy.py tests/test_representative_composition_matrix.py`
- Result: `57 passed, 2 warnings`

## Overstatements Or Missing Risks

The memo understates how bounded the current transient planner still is. `src/presenter/compose_from_intent.py:606-609` caps requests at 4 prose sections. That is a proof constraint, not a general output-family substrate.

The memo treats the live renderer catalog as the main UI bound, but the actual rendered surface depends heavily on 20 sub-renderers and their configs. Any serious output-family program needs an explicit stance on whether those sub-renderers collapse into a smaller leaf-family taxonomy or remain open-ended.

The memo also skips a lifecycle stability seam that matters if output families become first-class. `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_v1_completion.md` correctly notes that analyzer-side save does not enforce `compose_request == persistable_compose_request`; the code in `src/presenter/compose_session_store.py:79-105` confirms that only workflow/consumer/hash consistency is validated today.

Finally, the current proof matrix is still narrow. `tests/test_representative_composition_matrix.py:46-147` covers three cases: AOI `source_profile`, AOI `source_selection`, and genealogy `direct_sections`, all on the same primary consumer key. That is enough to justify the next abstraction step, but not enough to claim the abstraction step is already ratified.

The biggest unstated assumptions are:

- future engines will collapse into a few reusable families without a large new wave of sub-renderer growth
- consumer adaptation will stay simple even though current adaptation is mostly `raw_json` fallback
- lifecycle and persistence semantics will survive a move from request-family logic to output-family logic
- non-AOI engines can be brought onto explicit `output_contract` metadata without a more disruptive engine-definition rewrite

## Strategic Recommendation

Proceed with the direction, but narrow the claim. The right verdict is not "future engine growth is now basically a renderer problem." The right verdict is "the next generalization tranche should formalize renderer/output families because the current bounded proof line has reached the point where that abstraction is testable."

The concrete next tranche should be:

1. Extend capability definitions, not host code. Add declarative fields beside `composability` / `output_contract` for `output_family`, `composition_role`, `preferred_renderer_family`, `fallback_renderer_family`, `placement_policy`, and `persistence_class`.
2. Move the current hard-coded AOI/genealogy maps out of `src/presenter/compose_from_intent.py` and `src/presenter/composition_source_bridge.py` into registry-backed family definitions. `_ROLE_FROM_ENGINE_KEY`, `_PROFILE_SELECTION_PRESETS`, and the handoff/consumer allowlists are the first targets.
3. Tighten renderer and sub-renderer contracts before leaning harder on LLM projection. In particular, reduce permissive schemas, make `raw_json` fallback more explicit as a degraded state, and add analyzer-side equality enforcement for persisted lowered requests.
4. Prove one new matrix case that is not already inside the AOI bounded family, and one consumer case whose renderer support differs enough to exercise real adaptation instead of the same surface plus `raw_json` fallback.
5. Keep the framing deterministic-first. Use preserved structured artifacts or declared output contracts whenever possible, and use LLM projection only after a family has already been chosen and the target schema is tight.

If those corrections are made, the memo is strategically useful and worth treating as the next platformization lens. Without them, it risks sounding more generalized than the current substrate actually is.
