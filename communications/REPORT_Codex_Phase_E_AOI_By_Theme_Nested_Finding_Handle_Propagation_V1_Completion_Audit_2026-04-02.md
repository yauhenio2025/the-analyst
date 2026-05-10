# Report: Phase E AOI By-Theme Nested Finding Handle Propagation V1 Completion Audit

Date: 2026-04-02

## Verdict

`approve with corrections`

The memo is substantially accurate about the landed analyzer-side code boundary.

The needed corrections are about calibration, not direction:

- it should be even blunter that this slice advances mixed-surface payload truth, not current bounded-V2 mixed-surface operations
- the next move should probably be a bounded consumer-side proof of the already-landed contract before another analyzer-only specialization question

## The Memo's Strongest Code-Backed Points

### 1. `aoi_by_theme` really did gain nested `finding_id`, and the change is narrowly localized

The landed seam is real and small.

- `src/aoi/contract.py:333-336` still normalizes AOI findings with analyzer-owned `finding_id`
- `src/aoi/contract.py:639-647` now copies that `finding_id` onto nested cards only while building `aoi_by_theme`
- `src/aoi/contract.py:737-751` shows `_finding_card()` itself remains unchanged

So the memo is correct that the mixed-surface broadening landed in one local analyzer contract seam rather than as a generalized helper rewrite.

### 2. `aoi_by_theme` remains a mixed surface and whole-view affordance remains generic-only

The surface distinction is plain in the view definitions and the affordance gate.

- `src/views/definitions/aoi_by_theme.json:9-47` defines an accordion with mixed thematic content: `overview`, `engagement`, `key_claims`, `philosophical_commitments`, `argumentative_moves`, `source_documents`, and nested `findings`
- `src/views/definitions/aoi_by_sin_type.json:9-18` is the pure findings surface: a `card_grid`
- `src/presenter/first_hop_affordance.py:87-96` only assigns `specialized_family` for `view_key == "aoi_by_sin_type"` and `engine_key == "aoi_sin_findings"`
- `tests/test_presentation_api.py:1397-1481` explicitly preserves generic-only `FirstHopAffordance` on `aoi_by_theme` while allowing nested `finding_id`

So the memo is right that `aoi_by_theme` now carries nested item identity while the whole view still remains generic-only.

### 3. The persisted-payload caveat is accurate

This is one of the memo's strongest honesty points.

- `src/presenter/presentation_api.py:1825-1830` prefers persisted `structured_payloads[view_key]` verbatim when metadata already contains a saved structured payload
- `src/presenter/presentation_api.py:123-170` only performs renderer-facing normalization such as stripping `_section_*` meta keys and rebuilding accordion section config
- there is no repair-on-load path that backfills missing nested `finding_id`
- `tests/test_presentation_api.py:1484-1518` proves that saved `aoi_by_theme` payloads that lack nested `finding_id` remain handle-less when served

So the memo is correct that already-persisted `aoi_by_theme` payloads stay unchanged until rebuilt through the updated analyzer contract.

### 4. The memo is honest that analyzer `finding_id` is not Critic `db_id`

The product code confirms the distinction cleanly.

- the legacy thematic AOI UI uses string `finding_id` for identity in `ThemeSynthesisCard.tsx:286-297`
- the older Anxiety of Influence findings view also keys expansion state by `finding_id` in `AnxietyOfInfluencePage.tsx:1056-1060` and `AnxietyOfInfluencePage.tsx:1278-1313`
- `types.ts:3094-3119` defines `ThematicFinding.finding_id` as `string`
- the Arsenal mutation path in `FindingsPage.tsx:641-679` and `FindingsPage.tsx:1626-1821` still depends on numeric `db_id`

So the memo's framing is right: analyzer `finding_id` is an opaque analyzer-owned handle, not drop-in parity with Critic's numeric Arsenal identity.

### 5. The memo's verification claims check out

Re-running the memo's exact verification lines in the current repo still produces the same outcomes:

- `python -m compileall src/aoi/contract.py tests/test_aoi_contract.py tests/test_presentation_api.py` passes
- `PYTHONPATH=. pytest -q tests/test_aoi_contract.py tests/test_presentation_api.py` returns `83 passed, 2 warnings`
- `PYTHONPATH=. pytest -q tests/test_manifest_trace.py tests/test_analysis_product_contract.py tests/test_representative_composition_matrix.py tests/test_transient_proof_harness_contract.py tests/test_compose_sessions.py` returns `130 passed, 13 warnings`

## The Memo's Weakest Or Overstated Assumptions

### 1. It slightly overstates how much this advances mixed-surface semantics

What landed is mixed-surface identity propagation on analyzer payloads.

What did not land is mixed-surface operational semantics on the current bounded-V2 host path.

The current V2 thematic route still runs through:

- `AoiV2ThematicPanel.tsx:1423-1429`
- `V2TabContent.tsx:279-289`
- `ViewRenderer.tsx:165-176`

That is still the generic renderer path. I also found no consumer of `first_hop_affordance`, `allowed_destinations`, or `specialized_family` anywhere under `/home/evgeny/projects/the-critic/webapp/src`.

So the strongest truthful formulation is:

- this slice broadens analyzer payload truth on one mixed surface
- it does not yet prove current bounded-V2 mixed-surface finding operations

### 2. The host-evidence line is honest, but it should be even more explicit that it is legacy evidence

The memo says the strongest downstream evidence comes from the legacy Critic thematic UI, not from current bounded-V2 operations.

That is correct.

But the sharper version is:

- `ThemeSynthesisCard` and the older AOI findings page prove that theme-nested findings are meaningful item identities in legacy Critic code
- they do not prove that the bounded-V2 `aoi_by_theme` served surface already consumes the new nested `finding_id`

That distinction matters because it limits how much this slice can be credited as a product/runtime advance.

### 3. The stated next move is defensible, but not obviously the cleanest one

The memo proposes the next question as:

- is one mixed-surface specialized family defensible on `aoi_by_theme`, or should the line pivot elsewhere?

That is a defensible next analyzer-side question.

But because the current V2 host path does not yet consume the already-landed first-hop affordance family or the new nested thematic `finding_id`, there is a smaller and cleaner follow-on available:

- prove one bounded consumer-side usage of the current contract first

That would test whether the analyzer-owned contract is already materially useful to a thin host before adding more analyzer-only semantic refinement.

## Factual Discrepancies I Found

No major factual contradiction undermines the memo.

The main calibration issue is this:

- the memo should describe this as a proof of nested identity preservation on one mixed analyzer-known surface
- it should not let readers infer that bounded-V2 mixed-surface operations are now materially further along than they are

Everything else important checks out:

- `_finding_card()` really did stay unchanged
- `aoi_by_theme` whole-view affordance really is still generic-only
- older persisted payloads really do remain handle-less until rebuilt
- analyzer `finding_id` really is not Critic `db_id`
- the reported verification commands and counts are accurate

## What This Changes For The Larger Roadmap

This completion is legitimate Phase E matrix broadening, but its effect is narrower than a product-semantic reading might suggest.

What it really adds:

- analyzer-v2 can now preserve item identity on both a pure findings surface (`aoi_by_sin_type`) and one mixed surface (`aoi_by_theme`)
- it proves that mixed surfaces do not require whole-view overclaim in order to carry analyzer-owned nested identity

What it does not yet add:

- a proved mixed-surface operation family
- a bounded-V2 host that consumes `first_hop_affordance` or nested thematic `finding_id`
- generic item-affordance law

This is still aligned with the current roadmap documents.

- `MEMO_2026-03-30_distilled_strategic_roadmap.md:388-400`
- `MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:406-418`
- `MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:514-521`
- `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md:1376-1380`

All of them already framed this as the next bounded move and explicitly deferred whole-view specialization, outline-routing, destination lifecycle, and generic item taxonomy.

So the most defensible roadmap interpretation after this completion is:

- one real mixed-surface analyzer contract gap is now closed
- the broader analyzer-v2-as-brain claim is only modestly stronger until a thin host actually uses the emitted contract

## The Most Defensible Next Move After This Memo

The cleanest next move is:

- one bounded consumer-side proof that the already-landed analyzer contract is operationally usable on the V2 path

Concretely:

- pick one AOI V2 surface
- consume existing analyzer-owned identity and/or first-hop metadata without inventing a new semantic family
- prove one thin-host action seam end to end

Why this is cleaner than another immediate analyzer-only specialization question:

- it tests whether the current analyzer contract is actually serving the thin-host objective
- it avoids inventing more semantic law before the already-landed law is consumed anywhere
- it keeps the program tied to the real `Close Read` direction rather than analyzer-only contract accumulation

If the program insists on staying analyzer-only for one more slice, then the memo's proposed next question is still acceptable:

- evaluate whether `aoi_by_theme` merits any bounded mixed-surface specialized family

But that should be treated as second-best to proving that the current affordance and handle contracts already matter to a real host path.
