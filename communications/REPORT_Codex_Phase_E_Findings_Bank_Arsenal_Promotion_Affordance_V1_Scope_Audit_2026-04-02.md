# Codex Audit: Phase E Findings-Bank Arsenal Promotion Affordance V1 Scope

## Verdict

**approve with corrections**

The sequencing is right. After the generic `FirstHopAffordance` seam now survives on both transient and job-backed presenter surfaces, the next smallest honest analyzer-side variable is semantics, not more surface propagation. The memo is also right to keep `aoi_by_theme`, transient compose parity, destination lifecycle, and host UX expansion out of scope.

The correction is important, though: the proposed `specialized_family` marker is not sufficient by itself to support the specific runtime-real operation the memo is trying to mirror. The chosen AOI surface is semantically cleaner than `aoi_by_theme`, but the current analyzer payload does **not** expose the card-level identity/handle that Critic’s real "finding promotion to Arsenal" flow depends on. So the memo is directionally right but currently overclaims what a marker-only contract would mean.

## The Memo's Strongest Code-Backed Points

### 1. The next honest variable really is semantics, not propagation

That part is correct.

- The shared first-hop contract is already live and narrow:
  - `FirstHopAffordance` currently carries only `capturable` plus `allowed_destinations` in [src/presenter/schemas.py](src/presenter/schemas.py):695-702.
  - The shared helper already attaches it on the job-backed path in [src/presenter/first_hop_affordance.py](src/presenter/first_hop_affordance.py):33-83 and [src/presenter/presentation_api.py](src/presenter/presentation_api.py):808-841.
- The public job-backed contracts already carry it:
  - `ViewPayload.first_hop_affordance` in [src/presenter/schemas.py](src/presenter/schemas.py):250-255
  - `PagePresentation.views` in [src/presenter/schemas.py](src/presenter/schemas.py):258-296
  - `EffectiveManifestView.first_hop_affordance` in [src/presenter/schemas.py](src/presenter/schemas.py):299-321
- Contract/content honesty is already real on the job-backed line:
  - manifest view population in [src/presenter/manifest_builder.py](src/presenter/manifest_builder.py):188-209
  - manifest identity hashing in [src/presenter/manifest_builder.py](src/presenter/manifest_builder.py):277-300
  - trace diff visibility in [src/presenter/decision_trace.py](src/presenter/decision_trace.py):532-575
- Focused tests already prove the generic rule:
  - page payload attachment in [tests/test_presentation_api.py](tests/test_presentation_api.py):1224-1349
  - manifest hash/content-hash split and trace diff in [tests/test_manifest_trace.py](tests/test_manifest_trace.py):881-956

So the memo is right that the surface-propagation question is answered. The next variable is output-specific meaning.

### 2. `aoi_by_sin_type` is a better first specialization target than `aoi_by_theme`

This is also correct.

- `aoi_by_sin_type` is a curated AOI child surface with one clear findings-bank orientation:
  - `view_key="aoi_by_sin_type"`
  - `renderer_type="card_grid"`
  - grouped by `_category`
  - `group_style_map="sin_type"`
  in [src/views/definitions/aoi_by_sin_type.json](src/views/definitions/aoi_by_sin_type.json):2-18.
- Its payload builder is taxonomy-led and materially flatter:
  - `_build_by_sin_type_payload(...)` groups the same finding set by `sin_type` in [src/aoi/contract.py](src/aoi/contract.py):669-680.
- `aoi_by_theme` is clearly more mixed and nested:
  - accordion sections
  - overview
  - engagement
  - claims / commitments / moves
  - nested `mini_card_list` findings
  - secondary sources from other phases
  in [src/views/definitions/aoi_by_theme.json](src/views/definitions/aoi_by_theme.json):2-75 and [src/aoi/contract.py](src/aoi/contract.py):618-665.

If one analyzer-known AOI surface is going to carry a first specialized findings-family hint, `aoi_by_sin_type` is the cleaner choice.

### 3. Keeping analyzer ownership bounded is the right discipline

The host/runtime split in the memo is basically right.

- Critic’s generic workspace currently provides generic selection capture, not analyzer-owned destination behavior:
  - `CaptureContext` owns `submitCapture('arsenal' | 'research_todo')` in [/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx](/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx):17-145
  - `CaptureActionBar` exposes the two generic actions in [/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx](/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx):50-152
  - `AnalysisWorkspacePage` wraps the generic workspace in `CaptureProvider` / `CaptureActionBar` in [/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx):1128-1210
  - `V2TabContent` threads only generic capture props like `_captureViewKey`, `_captureViewName`, `_onCapture` in [/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx](/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx):575-587
- Critic’s current workspace `ViewPayload` type does not even include `first_hop_affordance` yet, let alone a specialized marker, in [/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx](/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx):58-83.

So the analyzer should still only declare semantics. It should not pretend to own button behavior or mutation flows.

## The Memo's Weakest Or Overstated Assumptions

### 1. The chosen AOI surface does not yet expose the operation handle that real Arsenal promotion uses

This is the main problem.

- The normalized AOI findings model does generate a stable `finding_id` at the internal contract layer in [src/aoi/contract.py](src/aoi/contract.py):333-356.
- But `_finding_card(...)`, which is what both `aoi_by_theme` and `aoi_by_sin_type` actually expose to the renderer-facing surface, drops that identity and emits only display/provenance fields in [src/aoi/contract.py](src/aoi/contract.py):723-736.
- By contrast, Critic’s current runtime-real finding-to-Arsenal flow is explicitly keyed by a concrete finding id:
  - Arsenal status is loaded by `item.finding_id` in [/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx):632-642
  - `toggleArsenal(...)` posts `{"finding_id": findingId}` in [/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx):652-679
  - the UI only exposes the button when `finding.db_id` exists in [/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx):1166-1175 and [/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx):1589-1596

So the memo’s intended family name, `findings_bank_arsenal_promotion_v1`, overstates the current analyzer-side substrate. Today’s `aoi_by_sin_type` contract gives the host a findings-bank **display** surface, not yet a direct per-finding promotion handle comparable to the runtime-real Critic path.

### 2. The evidence base is partly real, but partly from a different product seam

The memo relies on true runtime evidence, but it slides between two different things:

- generic workspace selection capture, which is already real on V2 job-backed surfaces
- direct finding promotion, which is runtime-real only on the legacy `FindingsPage`

Those are not the same seam.

The generic workspace path is selection-based and posts captures via `/captures` in [/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx](/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx):103-145. The direct finding-promotion path bypasses capture creation and posts straight to `/arsenal` with a finding id in [/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx):652-679.

That means the runtime evidence is good enough to justify "Arsenal promotion is a real first-hop operation in Critic", but not yet good enough to justify "this AOI card surface already exposes the same operation semantically".

### 3. `specialized_family` alone is too weak unless the slice also exposes a minimal item handle

I do not think the field itself is the problem. A single optional literal added to `FirstHopAffordance` is still the right level of schema restraint.

The weakness is that the marker would otherwise be pure labeling:

- it would tell the host that promotion semantics exist
- but it would not tell the host which exact card can be promoted by which stable handle

So the family name is acceptable only if the same slice also adds one minimal, explicit, analyzer-owned per-card promotion handle on `aoi_by_sin_type` only.

### 4. The current shared-type cleanup is not fully reflected in code comments

This is minor, but real.

`FirstHopAffordance` is now used on both transient and job-backed surfaces, yet its docstring still says "transient analytical views" in [src/presenter/schemas.py](src/presenter/schemas.py):695-699.

That does not invalidate the memo, but it is one more sign that the system is only just now cleanly shared and should not absorb an overstated specialization claim.

## Factual Discrepancies I Found

1. The memo treats `aoi_by_sin_type` as if its current public payload already carries enough structure for direct finding promotion. It does not. The internal normalized finding has `finding_id`, but the public renderer-facing card drops it in [src/aoi/contract.py](src/aoi/contract.py):333-356 and [src/aoi/contract.py](src/aoi/contract.py):723-736.

2. The memo leans on runtime-real Critic finding promotion as if it were already aligned with the V2 AOI workspace contract. It is not. The real Critic route is bound to `finding.db_id` and `POST /api/arsenal {finding_id}` in [/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx):652-679 and [/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/FindingsPage.tsx):1166-1175.

3. Host adoption is even more deferred than the memo implies. The current Critic workspace `ViewPayload` type does not include `first_hop_affordance` at all in [/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx](/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx):58-83. So a new specialized marker would definitely remain analyzer-only until later host work.

## What This Changes For The Larger Roadmap

It does **not** change the ordering judgment.

The roadmap remains right that:

- the next bounded Phase E variable is semantics rather than more propagation
- `aoi_by_sin_type` is still the strongest single analyzer-known AOI findings surface
- `aoi_by_theme`, transient parity, destination lifecycle, and broad taxonomy work should stay deferred
- this is still smaller and cleaner than jumping to outline-routing first

What changes is the minimum viable honesty bar.

The next slice cannot honestly be:

- "add one marker and we now express findings-bank Arsenal promotion"

It has to be one of these:

1. add one marker **plus** one minimal card-level promotion handle on `aoi_by_sin_type` only
2. or deliberately weaken the claim and name so it no longer implies direct promotion parity

Without that correction, the slice risks becoming a Critic-local label with no reusable operational law, which cuts against the broader analyzer-v2-as-brain objective.

## The Most Defensible Next Move After This Memo

Keep the direction. Narrow the claim.

The smallest defensible correction is:

1. Keep `specialized_family` additive on `FirstHopAffordance`.
2. Keep the generic first-hop contract unchanged.
3. Keep scope pinned to job-backed AOI `aoi_by_sin_type` only.
4. Keep `aoi_by_theme`, transient compose, destination lifecycle, and host UX out of scope.
5. But add one minimal analyzer-owned per-card promotion handle on `aoi_by_sin_type` if the family is going to claim direct Arsenal promotion semantics.

That handle does **not** need a generalized cross-renderer operation schema.
It only needs to be explicit enough for a host to distinguish:

- generic text capture
- from direct per-finding promotion on this one surface

If the team does **not** want to expose any card-level handle yet, then the family should be renamed/weakened so it does not claim "Arsenal promotion". In that case the next slice is really a findings-bank capture specialization, not a promotion specialization.

So the best next move is:

- approve the memo’s sequencing and target surface
- correct the scope so the public contract is strong enough to earn the family name it wants to introduce
