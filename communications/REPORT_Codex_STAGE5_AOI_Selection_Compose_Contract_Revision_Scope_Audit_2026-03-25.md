# Audit: Stage 5 AOI Selection-Compose Contract Revision Scope

Date: 2026-03-25
Reviewer: Codex
Memo under review: `communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md`

## Verdict

Approve with revisions.

## Findings

### 1. Medium: the memo’s bounded implementation surface is slightly too narrow because the most promising bounded fix path may start at bridge input selection, not only transient transform loss

The memo is right that the new blocker is inside `analyzer-v2` and that the live `409` now comes after the repaired host path. The authoritative rerun proves the counted path stays on planner-backed `compose-from-selection`, preserves canonical `source_v2_job_id`, and fails on analyzer-side contract validation in [PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json#L19), [PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json#L755), and [PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json#L799).

But the memo’s Decision 4 currently frames the bounded seam mainly as “bridge-produced AOI payloads survive transient compose” in [MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md#L90). The codebase already has a more specific bounded option available:

- AOI normalization already emits per-view `structured_payloads` for `aoi_source_documents`, `aoi_by_theme`, `aoi_by_sin_type`, and `aoi_thematic_report` in [contract.py](/home/evgeny/projects/analyzer-v2/src/aoi/contract.py#L64) and [contract.py](/home/evgeny/projects/analyzer-v2/src/aoi/contract.py#L357)
- the ordinary presenter path already prefers those persisted `structured_payloads` in [presentation_bridge.py](/home/evgeny/projects/analyzer-v2/src/presenter/presentation_bridge.py#L337) and [presentation_api.py](/home/evgeny/projects/analyzer-v2/src/presenter/presentation_api.py#L1818)
- the selection bridge, however, currently loads only normalized artifacts via [store.py](/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py#L725), materializes those payloads in [composition_source_bridge.py](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L520), and then sends them through `_transform_section_prose(...)` in [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L851)

That means the likely seam is narrower than “generic transient compose design problem,” but also slightly broader than the memo’s current file list. The first bounded diagnostic branch should explicitly ask whether `compose-from-selection` should reuse existing AOI `structured_payloads` for the affected families before re-extracting from normalized artifacts.

Implication: revise the memo so the bounded in-scope surface includes whatever minimal accessor is needed to reach persisted AOI `structured_payloads` if that turns out to be the narrowest fix. Without that revision, the implementor may spend time hardening generic extraction while bypassing already-validated AOI view payloads.

### 2. Medium: the suggested regression ownership misses the bridge-level seam and points one analyzer test bucket at the wrong file

The memo’s regression section names [test_compose_from_intent.py](/home/evgeny/projects/analyzer-v2/tests/test_compose_from_intent.py), [test_analysis_product_contract.py](/home/evgeny/projects/analyzer-v2/tests/test_analysis_product_contract.py), and [test_served_renderer_contract_policy.py](/home/evgeny/projects/analyzer-v2/tests/test_served_renderer_contract_policy.py) in [MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md#L131). That is directionally close, but it is not aligned to the actual seam.

Current test ownership is split differently:

- explicit `compose-from-selection` endpoint/error mapping already lives in [test_compose_from_intent.py](/home/evgeny/projects/analyzer-v2/tests/test_compose_from_intent.py#L1089)
- bridge selection/materialization behavior lives in [test_composition_source_bridge.py](/home/evgeny/projects/analyzer-v2/tests/test_composition_source_bridge.py#L185)
- persisted AOI `structured_payloads` law is already asserted in [test_aoi_contract.py](/home/evgeny/projects/analyzer-v2/tests/test_aoi_contract.py#L270)
- final served contract strictness lives in [test_served_renderer_contract_policy.py](/home/evgeny/projects/analyzer-v2/tests/test_served_renderer_contract_policy.py#L175)

I also reran the focused analyzer suites in the current workspace:

- `PYTHONPATH=. pytest -q tests/test_compose_from_intent.py` -> `23 passed`
- `PYTHONPATH=. pytest -q tests/test_composition_source_bridge.py` -> `4 passed`
- `PYTHONPATH=. pytest -q tests/test_served_renderer_contract_policy.py` -> `10 passed`

Implication: the memo should explicitly add `/home/evgeny/projects/analyzer-v2/tests/test_composition_source_bridge.py` as required regression ownership, and if the repair reuses persisted AOI view payloads it should also name `/home/evgeny/projects/analyzer-v2/tests/test_aoi_contract.py`. Otherwise the suite can go green without proving the bridge is feeding the right payload family into compose.

### 3. Medium: counted-path host smoke should be mandatory, not “only if needed,” because the non-counted fallback path still exists

The memo correctly insists that the counted path must stay on planner-backed `compose-from-selection` with preserved `source_v2_job_id` in [MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md#L79). But the deliverables make host smoke optional in [MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md#L138).

That is too loose for this gate. The live proof path still coexists with a non-counted profile/autostart route:

- planner-backed navigation preserves `source_v2_job_id` in [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L655) and [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L428)
- the profile/autostart route still omits canonical `source_v2_job_id` in [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L744) and [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L474)
- the counted planner-backed handoff is explicitly test-enshrined in [AoiV2ThematicPanel.test.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx#L434)

The Stage 5 rubric also treats product-path discipline as mandatory, not optional, in [MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_rubric.md#L98).

Implication: revise the memo so at least one host counted-path smoke is required, even if no host code changes are expected. That keeps the analyzer repair from “passing” through an unnoticed path drift.

### 4. Medium: the scope memo’s progress read is honest, but the authoritative roadmap documents are now one blocker behind and need to be updated alongside implementation

At the slice level, the memo is telling the truth: the host durability seam held, and the new blocker is the analyzer-side `409` contract failure in [MEMO_2026-03-25_stage5_aoi_selection_compose_contract_diagnosis.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_diagnosis.md#L91).

But the program-level roadmap docs are stale:

- the draft roadmap still says the immediate blocker is host warm snapshot durability in [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L192) and [MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md#L231)
- the master roadmap latest concrete blocker entry still ends on the same warm-snapshot seam in [MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md](/home/evgeny/projects/analyzer-v2/communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md#L1285)

Implication: approve the implementation scope, but require one small documentary update so the roadmap trail reflects that the durability slice is now closed baseline and the current blocker is selection-compose contract alignment. Otherwise the immediate memo is honest while the program ledger is not current.

## Direct Answers

1. Does the codebase evidence support treating analyzer-side `compose-from-selection` contract alignment as the first broken hop?

Yes, with one nuance: the first broken hop is inside `analyzer-v2`, but it may sit across `composition_source_bridge` input selection plus transient compose transformation, not only inside `_transform_section_prose(...)`.

The live proof shows the counted path stays on planner-backed `compose-from-selection` and fails with analyzer-side `bounded_dynamic_composition_validation_failed` in [PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json#L755). The missing keys line up with AOI view contracts, not host continuity, in [PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json#L799). The code path then runs through [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L256), [composition_source_bridge.py](/home/evgeny/projects/analyzer-v2/src/presenter/composition_source_bridge.py#L295), and [compose_from_intent.py](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L851).

2. Is the memo right to keep host warm-snapshot durability and identity continuity out of scope by default?

Yes.

The host baseline is currently supported by both proof and code. The rerun artifact shows preserved `source_v2_job_id`, planner-backed `compose-from-selection`, and no `compose-from-source` usage in [PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_evolution_ready_live_rerun_2026-03-25_requests.json#L19). The planner-backed host path preserves those fields in [AoiV2ThematicPanel.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L655) and [AoiComposeFromIntentPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L428), with regression coverage in [AoiV2ThematicPanel.test.tsx](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.test.tsx#L434).

3. Is the proposed bounded implementation direction technically coherent, or is it masking a broader transient compose design problem?

It is technically coherent if revised to state one explicit first branch: check whether the affected AOI families should reuse already-persisted AOI `structured_payloads` before doing more generic transient extraction work.

That is not evidence that the whole transient compose substrate needs redesign. It is evidence that this selection-backed path may currently bypass a narrower, already-existing AOI normalization law in [contract.py](/home/evgeny/projects/analyzer-v2/src/aoi/contract.py#L64), [presentation_bridge.py](/home/evgeny/projects/analyzer-v2/src/presenter/presentation_bridge.py#L337), and [presentation_api.py](/home/evgeny/projects/analyzer-v2/src/presenter/presentation_api.py#L1818).

4. Are the regression obligations concrete enough to prove:

- the real four-family `evolution_ready` selection shape now returns `200`
- the repaired AOI thematic-synthesis and sin-findings transient views are contract-valid
- the counted path still uses planner-backed `compose-from-selection` with preserved `source_v2_job_id`

Not yet.

They are directionally right, but they need three revisions:

- make `/home/evgeny/projects/analyzer-v2/tests/test_composition_source_bridge.py` explicit ownership for the bridge seam
- if persisted AOI `structured_payloads` are reused, also name `/home/evgeny/projects/analyzer-v2/tests/test_aoi_contract.py`
- make one host counted-path smoke mandatory rather than optional

5. Is the rerun branch rule still strict enough to stop dishonest consumption of the frozen Stage 5 pack?

Yes.

The memo still requires the same live `evolution_ready` diagnostic first and the frozen pack only after end-to-end success in [MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-25_stage5_aoi_selection_compose_contract_revision_scope.md#L115). The pack summary confirms that the frozen rerun remains unconsumed after the current failure in [PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json](/home/evgeny/projects/analyzer-v2/communications/PROOF_stage5_aoi_pack_rerun_summary_2026-03-25.json#L4).

6. Does the revised roadmap now tell the truth about how far along the program really is?

Not yet at the authoritative roadmap-document level.

The scope memo itself tells the truth about the current blocker. But the draft roadmap and master roadmap still describe the previous host durability seam as current. That needs one small documentary update before the program ledger is fully honest again.

7. Is there any hidden dependency or code-path wrinkle that makes the next slice riskier, narrower, or broader than the memo claims?

Yes, two:

- AOI normalization already persists per-view `structured_payloads`, and ordinary presenter flows already prefer them, while the selection bridge currently bypasses them
- the non-counted host autostart/profile path still exists and still omits `source_v2_job_id`, so counted-path proof must remain explicitly guarded even if no host code changes are expected

## Program Decision

The program should:

- keep the roadmap order
- keep Tranche 3 blocked
- treat the new slice-level progress read as honest, but update the authoritative roadmap docs because they are currently one blocker behind

This is still blocker retirement inside one open exemplar gate, not a reason to reorder phases or promote Tranche 3.

## Recommended Revisions Before Implementation

1. Revise Decision 4 so the first bounded diagnostic branch is: reuse existing AOI `structured_payloads` for the affected families if possible, then fall back to deterministic normalization, and only then consider broader extraction changes.
2. Expand the in-scope file surface slightly to allow the minimal accessor needed for persisted AOI `structured_payloads` if that proves to be the narrowest repair path.
3. Replace the current regression ownership list with an explicit split:
   - `/home/evgeny/projects/analyzer-v2/tests/test_compose_from_intent.py` for end-to-end `compose-from-selection`
   - `/home/evgeny/projects/analyzer-v2/tests/test_composition_source_bridge.py` for bridge payload materialization/preservation
   - `/home/evgeny/projects/analyzer-v2/tests/test_served_renderer_contract_policy.py` for final contract enforcement
   - `/home/evgeny/projects/analyzer-v2/tests/test_aoi_contract.py` if the repair relies on persisted AOI `structured_payloads`
4. Make one host counted-path smoke mandatory, not optional, so the repair cannot silently pass through path drift onto `compose-from-source` or profile/autostart controls.
5. Update the draft roadmap and master roadmap immediately after approving this scope so the documentary trail reflects that warm snapshot durability is now closed baseline and the live blocker is analyzer-side selection-compose contract alignment.
