# Memo: Phase E AOI By-Theme Nested Finding Handle Propagation V1 Scope

Subtitle: Carry minimal finding-level handles on one mixed analyzer-known AOI surface without overclaiming whole-view findings semantics

Date: 2026-04-02
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
Fixed-Direction Roadmap:
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Most Recent Code Completion:
- `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_completion.md`
Immediate Prior Scope:
- `communications/MEMO_2026-04-02_phase_e_findings_bank_arsenal_promotion_affordance_v1_scope.md`
Review Context:
- `communications/REPORT_Claude_Phase_E_Findings_Bank_Arsenal_Promotion_Affordance_V1_Scope_Critique_2026-04-02.md`
- `communications/REPORT_Codex_Phase_E_Findings_Bank_Arsenal_Promotion_Affordance_V1_Scope_Audit_2026-04-02.md`
Companion Product Evidence:
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory_v1_completion.md`
- `communications/MEMO_2026-04-01_close_read_operations_and_routing_inventory.md`
- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`
Strategy Context:
- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`

## Purpose

Define the next bounded analyzer-side Phase E slice after the pure-surface findings-bank specialization on AOI `aoi_by_sin_type`.

The `aoi_by_sin_type` question is now answered.
That surface is a pure findings bank, so whole-view specialization was honest there.

The next honest question is harder and more useful:

- can analyzer-v2 carry minimal finding-level handles on one mixed analyzer-known surface where findings are nested inside broader thematic content, without pretending the whole surface is itself a findings bank?

This memo therefore scopes:

- one mixed-surface contract broadening step
- on one analyzer-known AOI surface only
- with no new whole-view specialization family
- and no generic item-level affordance subsystem

It does **not** scope:

- another whole-view `specialized_family`
- outline-routing
- destination lifecycle
- host-side capture UX
- legacy payload repair across all stored AOI jobs

## Strategic Decision

The next concrete move should be:

- one bounded nested finding-handle propagation slice on AOI `aoi_by_theme`

not:

- broadening `findings_bank_arsenal_promotion_v1` to `aoi_by_theme`
- inventing a generic nested item-affordance schema
- switching immediately to outline-routing
- broadening destinations or lifecycle again
- building a generalized operation-family taxonomy

The reason is straightforward:

- `aoi_by_sin_type` already proved the pure findings-surface case
- `aoi_by_theme` is the strongest current mixed analyzer-known findings surface because it is built from the same normalized AOI findings family
- the view definition already declares nested findings explicitly under each theme
- the legacy Critic thematic UI already treats those nested findings as item-level entities keyed by `finding_id`
- the current analyzer contract still drops that handle on `aoi_by_theme`
- whole-view findings-bank specialization would overclaim on `aoi_by_theme` because the surface also contains overview, engagement, claims, commitments, and moves

This keeps the next step small and honest:

- vary surface shape difficulty
- keep specialization claims narrow
- carry one minimal handle only

## Current Evidence Base

Four repo facts make this a credible next slice:

1. the generic first-hop affordance seam is already proven on both transient and job-backed presentation lines
2. one pure-surface specialized findings-bank family is already proven on AOI `aoi_by_sin_type`
3. `aoi_by_theme` is a real analyzer-known mixed surface:
   - `view_key = "aoi_by_theme"`
   - `engine_key = "aoi_sin_findings"`
   - `renderer_type = "accordion"`
   - nested `findings` are explicitly part of the view contract
4. AOI normalization already computes stable analyzer `finding_id` values upstream

There is also one important host/runtime signal:

- the legacy Critic thematic UI already treats theme-nested AOI findings as distinct items keyed by `finding_id`

That evidence needs to be read carefully:

- it is evidence of real downstream thematic finding identity
- it is **not** proof that the current bounded-V2 `aoi_by_theme` served surface already operationalizes finding-level behavior in the host
- the current V2 `mini_card_list` path does not yet consume `finding_id`

So the remaining gap is not:

- invent mixed-surface finding identity from scratch

It is:

- stop dropping one already-known finding handle on one mixed analyzer-known surface

## Scope

### In scope

1. **One mixed-surface handle propagation change**

Carry `finding_id` onto nested `findings[]` items on AOI `aoi_by_theme`.

The landed contract should be:

- every `aoi_by_theme` theme section still carries its existing mixed content
- each nested finding card may additionally carry:
  - `finding_id`

This is a content-level contract change on one surface.
It is not a new presenter-level affordance family.

2. **Keep whole-view affordance generic**

Do **not** add a second whole-view specialized marker on `aoi_by_theme`.

That means:

- `FirstHopAffordance` remains whatever the already-landed generic first-hop line says it is for that view
- no `specialized_family` is added on `aoi_by_theme`

The reason is honesty:

- `aoi_by_theme` is a mixed surface, not a pure findings bank
- only the nested `findings[]` items are findings-like
- the surrounding view content is not itself a finding-level promotion surface

3. **Keep the behavioral scope narrow, even if the helper implementation is centralized**

The behavioral boundary should remain:

- `aoi_by_theme` newly gains nested `finding_id`
- `aoi_by_sin_type` keeps the same handle behavior it already has today
- no other surface semantics broaden

The implementation may therefore take either of two forms:

- add `finding_id` only inside `_build_by_theme_payload(...)`
- or centralize the same non-empty-handle carry-through in `_finding_card(...)` if that is demonstrably smaller and behaviorally equivalent for the current two AOI callers

What matters here is the boundary of **surface behavior**, not preserving duplication for its own sake.

4. **Keep analyzer handle semantics explicit**

The analyzer-side `finding_id` being propagated here must be described carefully:

- opaque analyzer handle
- suitable for per-item identity inside the analyzer-owned AOI contract
- not Critic's numeric `db_id`
- not a promise of host mutation parity
- not a cross-run identity guarantee

Known boundary:

- job-scoped or output-scoped identity is the honest claim
- if AOI findings reorder or materially change on re-execution, hosts must not assume durable cross-run identity continuity

5. **Be honest about legacy payloads**

This slice should broaden newly built analyzer contract truth on `aoi_by_theme`.

- Existing persisted `structured_payloads.aoi_by_theme` blobs loaded from saved output metadata will remain handle-less until those jobs are rebuilt through the updated analyzer contract.

This slice does **not** need to promise:

- automatic repair of every already-persisted legacy AOI payload on load

If legacy repair is not naturally available at the chosen seam, this memo prefers honesty over hidden compensation logic.

### Explicitly out of scope

- adding `specialized_family` to `aoi_by_theme`
- changing `allowed_destinations`
- changing the base `FirstHopAffordance`
- generic nested item-affordance schema
- `aoi_by_sin_type` broadening beyond what already landed
- transient compose changes
- outline-routing
- research-answer or research-todo specialization
- destination lifecycle
- host-side mutation behavior

## Population And Contract Shape

The implementation should stay minimal and surface-specific.

Expected analyzer-side shape:

- keep `FirstHopAffordance` unchanged
- keep `aoi_by_sin_type` specialization unchanged
- add `finding_id` only to `aoi_by_theme[*].findings[]`

Expected implementation seam:

- `src/aoi/contract.py::_build_by_theme_payload(...)`
- optionally `src/aoi/contract.py::_finding_card(...)` as a smaller internal carry-through helper, if and only if the behavioral surface boundary above stays unchanged

The change should work like this:

- build the existing mixed theme section payload as before
- when constructing nested finding cards under `findings`, copy through the normalized upstream `finding_id` if present and non-empty
- do not recompute a new identifier there

Because this is a structured-data content change rather than a contract-only metadata change, the supporting consequences should stay explicit:

- newly built `aoi_by_theme` payload content will change
- both page/manifest content truth and hash truth for affected rebuilt outputs will change accordingly
- if pinned AOI proof fixtures include `aoi_by_theme` payload truth, they may need refresh

## Acceptance Bar

This slice should count as complete only if all of the following are true:

1. `aoi_by_theme` nested `findings[]` items can carry `finding_id`
2. `aoi_by_sin_type` behavior remains unchanged
3. `aoi_by_theme` whole-view `FirstHopAffordance` remains generic-only
4. no new `specialized_family` is emitted on `aoi_by_theme`
5. no generic item-level affordance schema is introduced
6. the analyzer handle is documented as opaque and non-equivalent to Critic's numeric `db_id`
7. the memo stays explicit that the strongest current thematic-item identity evidence comes from the legacy Critic thematic UI, not an already-operational bounded-V2 thematic finding seam
8. existing persisted `aoi_by_theme` payloads are explicitly allowed to remain handle-less until rebuilt
9. no new destination or lifecycle contract is added
10. affected rebuilt payloads remain hash/content-honest as a real structured-data change
11. no host code changes are required for correctness of the analyzer-side contract

## Test Plan

### Primary analyzer verification

Add or extend focused tests for:

- `tests/test_aoi_contract.py`
  - `aoi_by_theme` nested findings now carry `finding_id`
  - the value is passed through from normalized AOI findings, not recomputed
  - `aoi_by_sin_type` remains behaviorally unchanged if the implementation chooses the smaller `_finding_card(...)` centralization route
- `tests/test_presentation_api.py`
  - rebuilt job-backed `aoi_by_theme` payloads/pages/manifests preserve the new nested `finding_id`
  - the whole-view `FirstHopAffordance` remains generic-only on `aoi_by_theme`
  - `aoi_by_sin_type` specialization remains unchanged
  - older saved payloads loaded verbatim remain handle-less unless the job is rebuilt
- `tests/test_manifest_trace.py`
  - if current trace snapshots cover `aoi_by_theme` payload truth, nested `finding_id` survives onto the manifest/page line and appears as ordinary structured-data change, not ghost metadata

### Stability / regression

Keep these lines unchanged except for the new additive nested handle on rebuilt `aoi_by_theme` payloads where applicable:

- `tests/test_analysis_product_contract.py`
- `tests/test_compose_from_intent.py`
- `tests/test_representative_composition_matrix.py`
- `tests/test_transient_proof_harness_contract.py`
- `tests/test_compose_sessions.py`

## Honest Claim If Completed

If this slice closes honestly, the claim should remain narrow:

- analyzer-v2 can now preserve minimal finding-level identity on one mixed analyzer-known AOI surface by carrying `finding_id` through to nested `aoi_by_theme` findings, while keeping whole-view first-hop affordance semantics generic and deferring any generic nested item-affordance schema
- the strongest current downstream thematic-item identity evidence still comes from the legacy Critic thematic UI rather than an already-operational bounded-V2 thematic finding action seam

It would **not** yet mean:

- mixed surfaces now have a generalized findings-bank specialization family
- outline-routing is solved
- generic item-level operation contracts are solved
- older persisted AOI outputs are all transparently repaired
- host mutation semantics are upstream-owned

## What Comes After This

If this slice lands cleanly, the next honest follow-on should be one of these:

- evaluate whether one bounded mixed-surface specialized family is now defensible on `aoi_by_theme`
- or pivot to one separate bounded outline-routing family if the mixed-surface semantics still look too host-shaped

What should **not** happen next:

- broadening destinations again
- jumping to destination lifecycle
- pretending `aoi_by_theme` proves a generic nested item-affordance taxonomy
