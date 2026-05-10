Verdict: Approve with corrections

The memo is basically right about ordering. After the April 1 interface-first review, the Close Read direction change, and the completed operations/routing inventory, the next analyzer-side move should still be a behavior-preserving extraction of composition law out of `compose_from_intent.py`, not a host build, not lifecycle broadening, and not premature affordance schema design. But the memo needs tighter honesty in three places: the current metadata seam is real but uneven, the genealogy legacy-key story is not closed yet, and `composition_role` is the one upstream seam that is already visibly present in code.

**The Memo's Strongest Code-Backed Points**

1. The immediate blocker is still central composition law inside [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L82). The current transient compose path still hard-codes `_LEAF_PATTERN_BY_ROLE`, `_PRESENTATION_STANCE_BY_ROLE`, and `_ROLE_FROM_ENGINE_KEY` in [compose_from_intent.py:82](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L82) and resolves semantic role through a central hint-or-engine-key matcher in [compose_from_intent.py:778](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L778). That is exactly the right place to attack next.

2. The memo correctly separates this extraction from admission policy, lifecycle broadening, and affordance/routing work. The hard-coded transient admission surface is a different seam in [compose_from_intent.py:145](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L145), and workflow-shaped parent grouping/title policy is a different seam in [compose_from_intent.py:703](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L703). Leaving those out of v1 is disciplined.

3. The codebase does already contain real metadata-shaped footholds for this tranche. AOI source-backed composition already carries analyzer-owned `composition_role_hint` values in [_SOURCE_FAMILY_DEFINITIONS](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L45) and threads them into `CompositionMaterializedSection` in [composition_source_bridge.py:540](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L540). Genealogy saved-result handoff already carries `role_hint` for both canonical and legacy outputs in [genealogy_saved_result_bridge.py:33](/home/evgeny/projects/analyzer-v2/src/orchestrator/genealogy_saved_result_bridge.py#L33), and lowering fails closed if that role truth would be lost in [direct_sections_compose_harness.py:27](/home/evgeny/projects/analyzer-v2/src/orchestrator/direct_sections_compose_harness.py#L27). So there is already a live analyzer-side concept of semantic role upstream of rendering.

4. The memo is also right to preserve current proof surfaces and avoid host changes. The representative matrix is still the three bounded cases in [tests/test_representative_composition_matrix.py:46](/home/evgeny/projects/analyzer-v2/tests/test_representative_composition_matrix.py#L46), [tests/test_representative_composition_matrix.py:69](/home/evgeny/projects/analyzer-v2/tests/test_representative_composition_matrix.py#L69), and [tests/test_representative_composition_matrix.py:109](/home/evgeny/projects/analyzer-v2/tests/test_representative_composition_matrix.py#L109). Served-renderer policy is already split strict/shadow/warn and transient compose is already strict in [tests/test_served_renderer_contract_policy.py:92](/home/evgeny/projects/analyzer-v2/tests/test_served_renderer_contract_policy.py#L92). This slice should stay analyzer-side.

**The Memo's Weakest Or Overstated Assumptions**

5. The current codebase provides a plausible metadata-bearing seam, but not a ready-made one. `CapabilityEngineDefinition` exposes `composability`, `legacy_engine_key`, and `output_contract` in [schemas_v2.py:328](/home/evgeny/projects/analyzer-v2/src/engines/schemas_v2.py#L328), but none of those fields currently mean `composition_role`, `preferred_pattern_key`, or `preferred_presentation_stance`. `ComposabilitySpec` in [schemas_v2.py:124](/home/evgeny/projects/analyzer-v2/src/engines/schemas_v2.py#L124) is about context sharing, not presentation law. So the memo should say more explicitly that this tranche must either extend the capability schema or add an adjacent composition-metadata registry.

6. The memo overstates readiness for the genealogy half of the engine set. A repo scan shows `output_contract` exists in only 4 of 28 capability definitions, and all 4 are the AOI files:
   - `aoi_thematic_synthesis`
   - `aoi_engagement_mapping`
   - `aoi_sin_findings`
   - `aoi_thematic_report`

   Those AOI definitions are genuinely structured in [aoi_thematic_synthesis.yaml:90](/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/aoi_thematic_synthesis.yaml#L90), [aoi_engagement_mapping.yaml:80](/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/aoi_engagement_mapping.yaml#L80), [aoi_sin_findings.yaml:89](/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/aoi_sin_findings.yaml#L89), and [aoi_thematic_report.yaml:72](/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/aoi_thematic_report.yaml#L72). The genealogy capability definitions do have canonical YAMLs plus `legacy_engine_key` bridges in [genealogy_relationship_classification.yaml:535](/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/genealogy_relationship_classification.yaml#L535) and [genealogy_final_synthesis.yaml:684](/home/evgeny/projects/analyzer-v2/src/engines/capability_definitions/genealogy_final_synthesis.yaml#L684), but they do not currently expose the same structured output-contract seam.

7. Legacy genealogy engine keys are not handled honestly enough in the memo as written. The memo includes both canonical and legacy keys in scope, but the compose-adjacent code does not currently resolve capability metadata through legacy aliases. The alias bridge exists in [discovery.py:59](/home/evgeny/projects/analyzer-v2/src/engines/discovery.py#L59), but `dynamic_prompt.py` still does exact-key `get_capability_definition(...)` lookup in [dynamic_prompt.py:67](/home/evgeny/projects/analyzer-v2/src/presenter/dynamic_prompt.py#L67), and `views/generator.py` does the same in [views/generator.py:25](/home/evgeny/projects/analyzer-v2/src/views/generator.py#L25). So if the extraction stores metadata only on canonical YAML capability definitions, `genealogy_pass1b_relationship_classification` and `genealogy_pass7_final_synthesis` will not automatically benefit on the compose path.

8. The memo is slightly too engine-centric about all three extracted values. The current code already treats `composition_role` as the upstream semantic hint seam, while pattern and stance are still role-level planner law. AOI source-backed materialization and genealogy saved-result handoff both propagate role hints only, not pattern/stance hints, in [composition_source_bridge.py:45](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L45) and [genealogy_saved_result_bridge.py:33](/home/evgeny/projects/analyzer-v2/src/orchestrator/genealogy_saved_result_bridge.py#L33). That suggests the most honest design is:

- engine metadata declares `composition_role`
- a small role-level composition registry derives pattern/stance

not necessarily duplicating every preference directly onto every engine definition.

**Factual Discrepancies**

9. The memo implies the current proved engine set is uniformly metadata-ready. It is not. AOI has capability definitions with structured output contracts; genealogy currently has canonical capability definitions plus legacy aliases, but not the same structured output-contract layer, and the compose path is not alias-aware today.

10. The memo understates how bounded the current proof claim still is. The matrix only proves AOI `source_profile`, AOI `source_selection`, and genealogy `direct_sections` on the same main consumer surface in [tests/test_representative_composition_matrix.py:46](/home/evgeny/projects/analyzer-v2/tests/test_representative_composition_matrix.py#L46). That is enough to justify this extraction tranche, but not enough to speak as if the future family law is already broadly ratified.

11. The memo should acknowledge more explicitly that strict renderer law already exists at the served boundary. The transient compose boundary is strict in [tests/test_served_renderer_contract_policy.py:92](/home/evgeny/projects/analyzer-v2/tests/test_served_renderer_contract_policy.py#L92), strict genealogy served modes already fail closed in [tests/test_served_renderer_contract_policy.py:147](/home/evgeny/projects/analyzer-v2/tests/test_served_renderer_contract_policy.py#L147), and shadow validation is already real in [tests/test_served_renderer_contract_policy.py:156](/home/evgeny/projects/analyzer-v2/tests/test_served_renderer_contract_policy.py#L156). So the correction is not “host changes are needed.” The correction is “keep this tranche entirely upstream because the served boundary is already there.”

**What This Changes For The Larger Roadmap**

12. The completed operations/routing inventory changes the rationale, not the order. The roadmap and completion memos still point to extraction first, then one bounded post-extraction affordance/routing addendum over first-hop operations only, then only later broader product or taxonomy work. The ordering remains explicit in [MEMO_2026-03-30_distilled_strategic_roadmap.md:340](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-30_distilled_strategic_roadmap.md#L340), [MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:397](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md#L397), and [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1376](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1376).

13. The roadmap change I would make is narrower than the memo implies: add one explicit subtask inside this tranche for alias-aware composition metadata resolution across canonical and legacy genealogy keys. Without that, the tranche will either quietly exclude real proved legacy paths or duplicate metadata inconsistently.

**The Most Defensible Next Move**

14. The most defensible next move is still `Phase E Composition Metadata Extraction V1`, but with four corrections:

- make `composition_role` the primary extracted analyzer-owned field
- either derive `preferred_pattern_key` and `preferred_presentation_stance` from a tiny role registry or store them in an adjacent composition-metadata layer, rather than assuming current capability schema already supports them
- add alias-aware metadata lookup for `genealogy_pass1b_relationship_classification` and `genealogy_pass7_final_synthesis`, using the same canonical/legacy bridge idea that already exists in [discovery.py:59](/home/evgeny/projects/analyzer-v2/src/engines/discovery.py#L59)
- preserve bounded fallback for unmigrated engines and keep all host/harness code unchanged

15. I do not see a meaningfully stronger immediate analyzer-side tranche than this one. The only smaller candidate would be a `composition_role`-only extraction, because role hints are already propagated upstream. But that would leave the authoritative pattern/stance choice in the same central compose file and would stop short of the real authority move this Phase E slice is supposed to prove. So the memo's tranche is still the right next slice, just with tighter honesty about seam readiness and legacy-key handling.

**Bottom Line**

Approve the memo after correction, not as written. The order is right. The extraction target is right. The separation from taxonomy, admission, lifecycle broadening, and affordance/routing work is right. The two necessary fixes are:

- state plainly that current metadata readiness is asymmetric across AOI vs genealogy
- make legacy-key resolution an explicit acceptance item rather than an implicit assumption

With those corrections, this is the most defensible next Phase E code move.

**Verification Note**

This was a docs-and-code audit tranche. No tests were run.
