# Report: Phase E AOI By-Theme Nested Finding Handle Propagation V1 Scope Audit

Date: 2026-04-02

## Verdict

`approve with corrections`

The memo is directionally right.

- Yes, `aoi_by_theme` nested finding-handle propagation is the right immediate next analyzer-side slice after the completed `aoi_by_sin_type` specialization.
- Yes, `aoi_by_theme` should stay whole-view generic-only.
- Yes, keeping `_finding_card()` unchanged and adding `finding_id` only inside `_build_by_theme_payload(...)` is the right scope discipline.

The needed correction is mostly one of calibration, not direction:

- be more explicit that the runtime evidence for nested finding identity comes from the legacy AOI thematic UI, not from an already-proven bounded-V2 themed finding operation seam
- be more explicit that older persisted `aoi_by_theme` payloads loaded from saved `structured_payloads` will remain handle-less until rebuilt or regenerated

## The Memo's Strongest Code-Backed Points

### 1. `aoi_by_theme` really is the mixed-surface case, not another pure findings bank

That is plain in the current view contract.

- `src/views/definitions/aoi_by_theme.json:2-90` defines `aoi_by_theme` as `renderer_type: "accordion"`
- its section schema includes `overview`, `engagement`, `key_claims`, `philosophical_commitments`, `argumentative_moves`, `source_documents`, and nested `findings`
- by contrast, `src/views/definitions/aoi_by_sin_type.json:2-44` is a `card_grid` of findings regrouped by sin type

So the memo is right about the pure-versus-mixed distinction. `aoi_by_theme` is the next harder variable because it carries findings inside a broader thematic surface instead of being a whole-view findings bank.

### 2. The analyzer already computes `finding_id` upstream and currently drops it on `aoi_by_theme`

The current AOI contract already normalizes findings with analyzer-owned `finding_id` values in `src/aoi/contract.py:333-367`.

But the renderer-facing `aoi_by_theme` payload still drops that handle:

- `src/aoi/contract.py:608-666` builds `aoi_by_theme`
- the nested `findings` list is currently produced by `_finding_card(finding)` at `src/aoi/contract.py:662-664`
- `_finding_card(...)` at `src/aoi/contract.py:730-744` does not include `finding_id`

So the memo identifies a real contract gap, not an invented one.

### 3. Keeping `aoi_by_theme` whole-view affordance generic-only is the honest choice

The current presenter line already distinguishes the pure-surface case:

- `src/presenter/first_hop_affordance.py:87-96` attaches `specialized_family` only to AOI `aoi_by_sin_type`
- that specialization is fail-closed on complete materialized card handles via `_payload_has_complete_findings_bank_handles(...)` at `src/presenter/first_hop_affordance.py:105-123`
- tests explicitly keep `aoi_by_theme` generic-only in `tests/test_presentation_api.py:1372-1410`

That is the right boundary. Only the nested `findings[]` items on `aoi_by_theme` are findings-like; the surrounding theme section is not itself a findings bank.

### 4. Keeping `_finding_card()` unchanged is the right implementation discipline

This is also backed by the current code shape.

- `_finding_card(...)` is shared surface logic in `src/aoi/contract.py:730-744`
- `aoi_by_sin_type` already follows the narrow pattern by adding `finding_id` only in `_build_by_sin_type_payload(...)` at `src/aoi/contract.py:669-688`
- current tests already assert that `aoi_by_theme` findings do not carry `finding_id` while `aoi_by_sin_type` cards do in `tests/test_aoi_contract.py:307-333`

So the memo's proposed discipline is coherent: do on `aoi_by_theme` exactly what the completed `aoi_by_sin_type` slice already did for its own surface, instead of widening the shared helper.

### 5. This is smaller and stronger than jumping to outline-routing next

The Close Read operations matrix still supports that ordering.

- `communications/APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md:23-25` shows finding promotion as a first-hop seam keyed by finding identity
- the outline seam at `...matrix.md:25` requires selected text plus `section_id` and comment-modal flow

That makes outline-routing more host-shaped and more context-heavy. By comparison, `aoi_by_theme` nested handle propagation is just one analyzer-known mixed-surface identity pass-through on a surface built from the same normalized AOI findings family.

## The Memo's Weakest Or Overstated Assumptions

### 1. The runtime evidence is real, but it is legacy thematic AOI evidence, not bounded-V2 proof

The memo says the Critic thematic UI already treats nested findings as item-level entities keyed by `finding_id`. That is true, but it needs more careful framing.

- `ThemeSynthesisCard` keys expansion and rendering by `finding.finding_id` in `/home/evgeny/projects/the-critic/webapp/src/components/influence/ThemeSynthesisCard.tsx:286-379`
- the older AOI findings page also expands items by `finding.finding_id` in `/home/evgeny/projects/the-critic/webapp/src/pages/AnxietyOfInfluencePage.tsx:1056-1060` and `:1278-1313`
- `ThematicFinding` itself requires `finding_id: string` in `/home/evgeny/projects/the-critic/webapp/src/types.ts:3093-3118`

But the bounded-V2 `aoi_by_theme` surface is still just a generic accordion contract. The memo should not imply that a current bounded-V2 themed-finding operation seam is already live.

### 2. The analyzer handle framing is honest, but it must stay explicit

The memo is right that analyzer `finding_id` is not Critic's legacy Arsenal mutation identity.

- legacy Arsenal promotion on `FindingsPage` still uses numeric `db_id` and posts `{"finding_id": <number>}` in `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx:652-679`
- the button itself is guarded on `finding.db_id` in `/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx:1166-1175`

So the memo is correct to frame analyzer `finding_id` as an opaque analyzer handle, not mutation parity. That point should remain prominent because it is the main place a reader could otherwise over-infer.

### 3. The legacy-payload caveat needs one more sentence of bluntness

The memo gestures at this, but it should say the consequence plainly.

- `src/presenter/presentation_api.py:1825-1830` prefers persisted `structured_payloads[view_key]` verbatim when present

So older saved AOI outputs with `aoi_by_theme` payloads that were built before nested `finding_id` propagation will remain handle-less until rebuilt or regenerated. Unlike the `aoi_by_sin_type` specialization slice, there is no whole-view `specialized_family` here that would overclaim in the meantime. That makes the omission tolerable, but it should be stated directly.

## Factual Discrepancies I Found

No major code contradiction undermines the memo's direction.

The only material calibration issue is this:

- the memo's product evidence is strongest in legacy AOI thematic UI code, not in a currently live bounded-V2 themed-finding operation seam

That does not invalidate the slice. It just means the memo should present the runtime evidence as adjacent product proof for finding-level identity on mixed thematic surfaces, not as proof that bounded-V2 `aoi_by_theme` already has per-item operations.

## What This Changes For The Larger Roadmap

This is a good Phase E generality-proof move.

- It broadens the proof matrix from pure-surface whole-view specialization to mixed-surface nested item identity.
- It moves more semantic truth upstream into analyzer-v2 by preserving analyzer-known finding identity on an analyzer-known mixed surface.
- It reduces the need for consumers to reconstruct item identity from display fields.

That is aligned with the current roadmap, not drift.

- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:519-521` already names completed `aoi_by_sin_type` specialization first and `aoi_by_theme` nested finding-handle propagation as the next bounded move
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md:303-317` says analyzer-v2 needs analyzer-owned semantic affordances and routing hints, but only on a cleaner substrate

What it does **not** change:

- this is still AOI-local proof, not generic item-affordance law
- it does not solve outline-routing
- it does not solve destination lifecycle
- it does not yet prove multi-consumer downstream item-operation generality

## The Most Defensible Next Move After This Memo

Implement exactly the narrow slice the memo describes, with two wording corrections carried into the completion claim.

1. Add `finding_id` only to `aoi_by_theme[*].findings[]` in `src/aoi/contract.py::_build_by_theme_payload(...)`.
2. Leave `_finding_card()` unchanged.
3. Keep `aoi_by_theme` whole-view `FirstHopAffordance` generic-only.
4. Add focused tests proving rebuilt `aoi_by_theme` payloads now carry nested `finding_id` while `aoi_by_sin_type` specialization behavior remains unchanged.
5. State plainly in docs/tests that older persisted `aoi_by_theme` payloads loaded from saved `structured_payloads` remain handle-less until rebuilt.
6. State plainly that the runtime evidence for nested finding identity comes from the legacy thematic AOI UI, while host-side bounded-V2 themed finding operations remain a later question.

If that lands cleanly, the next honest decision point is:

- either test whether one bounded mixed-surface specialized family is now actually defensible on `aoi_by_theme`
- or pivot to a separate outline-routing family if product pressure makes that more urgent

What should not happen next is still the same:

- no generic nested item-affordance taxonomy
- no new destination/lifecycle broadening
- no pretending this slice alone solves `Close Read`
