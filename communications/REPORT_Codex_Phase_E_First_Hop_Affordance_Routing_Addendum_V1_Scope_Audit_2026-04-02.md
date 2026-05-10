# Report: Phase E First-Hop Affordance Routing Addendum V1 Scope Audit

## 1. Verdict

**Approve with corrections.**

The memo has the right sequencing. After composition-metadata extraction and bridge-hint consolidation, the next honest analyzer-side move is an additive transient-compose contract slice over first-hop semantics, not more bridge cleanup, not destination lifecycle, and not broader Close Read product law. `TransientIntentView` is also the right public attachment seam.

But the memo is too aggressive in one place and too loose in two others:

- `capturable` plus bounded destination eligibility are well-backed by current code and runtime evidence
- generic `commentable` is **not** yet equally well-backed on the current transient analytical compose line
- the memo does not make the leaf-vs-container emission rule concrete enough
- the acceptance bar omits the fact that new transient-view metadata must participate in transient presentation hashes and related proof coverage

The strongest corrected version of this slice is:

- additive first-hop metadata on `TransientIntentView`
- emitted only on current analytical leaf views
- v1 truth centered on `capturable` and bounded `allowed_destinations`
- `commentable` either deferred to the next micro-slice or carried only as a conservative optional/false-default field, not as a broadly emitted positive claim

## Short Answers To The Prompt Questions

- **Is a first-hop affordance/routing addendum the right immediate next analyzer-side slice after bridge-hint consolidation?**
  - Yes.

- **Is `TransientIntentView` the right first attachment surface?**
  - Yes. It is the public transient-compose response seam in `src/presenter/schemas.py:689-735`. It is smaller and stronger than job-backed `PagePresentation` / manifest work, and more honest than hiding semantics inside `renderer_config`, trace payloads, or generated definitions.

- **Does the memo correctly keep the v1 affordance family bounded to `capturable`, `commentable`, and bounded `allowed_destinations`?**
  - Partly. `capturable` and bounded `allowed_destinations` are defensible. Generic `commentable` is not yet equally well-supported for the current transient analytical surfaces.

- **Are `arsenal` and `research_todo` the right only allowed destinations for this first slice?**
  - Yes for the generic first-hop tranche. `outline` is runtime-real in `the-critic`, but it is comment-specific and should stay out of this first generic capture/routing slice.

- **Does the memo correctly defer destination lifecycle, findings-specific flows, research-answer-specific routing, and host UX?**
  - Yes.

- **Does it preserve thin-host architecture honestly?**
  - Yes, if the affordance stays explicit on the transient view contract and hosts remain responsible for UX and local workflow execution.

- **Is the proposed leaf-surface / container-surface distinction concrete enough to implement and test?**
  - Not yet. The codebase has a concrete distinction, but the memo should name it explicitly.

- **Does the memo preserve output shapes and current proof surfaces honestly enough?**
  - Mostly, but it should explicitly require hash/test updates for the new additive field.

- **Is there a smaller and stronger immediate slice than this one?**
  - Yes: capture eligibility plus bounded destination eligibility only.

- **What should change in roadmap ordering after the bridge-hint consolidation closeout?**
  - No major reorder. The only correction is to split “first-hop affordance/routing” into:
    1. capture/destination eligibility
    2. later comment/text-anchor semantics

## 2. The Memo's Strongest Code-Backed Points

- `TransientIntentView` is the right attachment point. The transient compose contract is defined in `src/presenter/schemas.py:689-735`, while job-backed surfaces remain separate in `src/presenter/manifest_builder.py` and `src/presenter/presentation_api.py`. That matches the memo’s “transient compose only” boundary.

- The current compose path already has a concrete analyzer-owned leaf/container structure that can support conservative emission:
  - `_plan_page_structure(...)` in `src/presenter/compose_from_intent.py:687-731` creates either a flat leaf set or one synthetic parent tab shell.
  - `_build_transient_payload(...)` in `src/presenter/compose_from_intent.py:1169-1210` emits leaf payloads with real `engine_key` and no children.
  - `_build_parent_transient_payload(...)` in `src/presenter/compose_from_intent.py:1254-1298` emits synthetic container payloads with `engine_key=None` and nested children.
  - `_to_transient_view(...)` in `src/presenter/compose_from_intent.py:1369-1385` is the final public conversion seam.

- The product evidence really does support a bounded generic first-hop routing family centered on capture:
  - `CaptureSelection` in `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:17-35` already carries the core analyzer-relevant surface identity fields: `source_view_key`, `source_renderer_type`, `content_type`, `selected_text`, `structured_data`, `context_title`, `depth_level`, and optional parent context.
  - `submitCapture(...)` in `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:87-166` routes that capture to exactly two generic first-hop destinations: `arsenal` and `research_todo`.
  - `CaptureActionBar` in `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:50-153` exposes those two generic first-hop actions on an active selection.
  - `ResearchFlagDialog` in `/home/evgeny/projects/the-critic/webapp/src/components/ResearchFlagDialog.tsx:69-168` shows that research-todo creation from a captured selection is runtime-real, not aspirational.

- The host side is already thin enough that explicit analyzer-owned view metadata is the honest next seam. `AoiComposeFromIntentShell` simply adapts and renders `response.presentation.views` in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx:51-118`, and `transientComposeAdapters.ts` passes transient view metadata through without host-side semantic reconstruction in `/home/evgeny/projects/the-critic/webapp/src/lib/transientComposeAdapters.ts:15-58`.

- Keeping job-backed page/manifest propagation out of scope is correct. Nothing in the current code requires touching `PagePresentation`, `EffectivePresentationManifest`, or the job-backed presenter routes to prove this first transient-only seam.

## 3. The Memo's Weakest Or Overstated Assumptions

- The memo overstates how well generic `commentable` is supported on the **current transient analytical compose line**.
  - The strongest runtime-real comment persistence seam I found is research-answer comment persistence:
    - selection capture for comment text anchor in `/home/evgeny/projects/the-critic/webapp/src/pages/research/ResearchCard.tsx:86-126`
    - follow-on routing from that popup to Arsenal / research todo in `/home/evgeny/projects/the-critic/webapp/src/pages/research/ResearchCard.tsx:128-165`
  - That seam is research-specific, item-level, and depends on text-anchor context (`quoted_text`, `text_prefix`, `text_suffix`, `todo_id`), not just a generic boolean commentability claim.
  - Findings-page comment persistence is also runtime-real, but it is host-local and finding-specific, not a generic transient analytical leaf contract. The inventory memo itself described `commentable` as part of a **candidate hypothesis set**, while the stronger recommendation was “capture/routing eligibility on rendered analytical surfaces.”

- The memo does not define the leaf/container rule concretely enough. The codebase can support a real rule, but the memo should say it plainly:
  - emit only on transient views with a real `engine_key` and no `children`
  - do not emit on synthetic parent tab shells with `engine_key=None`
  - do not infer affordances from internal renderer substructure

- The memo understates the contract-identity consequences of adding the field. `presentation_hash` and `presentation_content_hash` are derived in `src/presenter/compose_from_intent.py:1449-1501`, and the current identity/content rows do **not** include any future affordance metadata. If the new field lands but hashes do not incorporate it, compose-session identity and proof artifacts will silently miss the contract change.

- The memo should be more explicit that this tranche is analyzer metadata only, not a current user-visible host capability. The current AOI transient compose host in `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx:25-118` renders views directly and does not wire capture/comment UX into that transient shell today.

## 4. Factual Discrepancies I Found

- The memo treats `commentable` as if it belongs in the same first-confidence tier as `capturable`. The audited code does not support that strongly enough for the current transient analytical compose surfaces.
  - `capturable` is backed by a generic host-level capture contract.
  - `commentable` is backed by narrower research-answer and findings-specific seams.
  - That is an evidence asymmetry the memo should acknowledge.

- The memo’s acceptance language implies “no contract change” too broadly. In strict code terms, adding an affordance object to `TransientIntentView` **is** a public response-contract expansion in `src/presenter/schemas.py:689-735`, even if it is backward-compatible and route/lifecycle preserving.

- The memo’s current acceptance bar misses a real code obligation: new transient-view metadata must be reflected in hash behavior and related tests.
  - The transient-hash test in `tests/test_compose_from_intent.py:1964-2049` currently proves hash sensitivity for renderer changes, but not for future affordance metadata.
  - Compose-session tests in `tests/test_compose_sessions.py:54-145` persist and round-trip the transient hashes directly.

## 5. What This Changes For The Larger Roadmap

- It does not change the major order. The major order still looks right:
  1. composition metadata extraction
  2. bridge-hint consolidation
  3. transient first-hop affordance/routing addendum

- It does tighten the next slice into a better sub-order:
  1. transient capture eligibility plus bounded destination eligibility
  2. later comment/text-anchor semantics
  3. only later output-specific routes and destination lifecycle

- That correction makes the roadmap more honest with the current evidence:
  - generic capture is already real
  - research-todo routing from a captured selection is already real
  - generic comment semantics across transient analytical surfaces are **not** yet equally uniform

- The larger “analyzer-v2 as the brain” direction remains intact. This still begins analyzer-owned semantic-affordance truth, but it does so at the strongest currently evidenced layer rather than baking a weak commentability generalization too early.

## 6. The Most Defensible Next Move After This Memo

- Approve the tranche after tightening it.

- Implement one additive transient-view affordance object on `TransientIntentView`, but keep the first emission rule narrower than the memo currently says:
  - `capturable: bool`
  - `allowed_destinations: ["arsenal"] | ["research_todo"] | ["arsenal", "research_todo"] | []`
  - `commentable` either omitted from v1 emission or kept strictly optional/false-default until a later text-anchor/comment tranche

- Make the emission rule explicit and testable:
  - only views emitted from `_build_transient_payload(...)`
  - never synthetic parents emitted from `_build_parent_transient_payload(...)`

- Keep the rest fixed:
  - no job-backed page/manifest propagation
  - no destination lifecycle
  - no findings-specific Arsenal promotion law
  - no research-answer-specific popup routing law
  - no host UX requirement in this slice

- Add focused verification for the real contract boundary:
  - schema accepts the new optional field on `TransientIntentView`
  - affordance metadata is absent on synthetic parent views
  - affordance metadata is present only on current analytical leaf views
  - transient presentation hashes change when affordance metadata changes
  - representative matrix / proof harness / compose-session tests still pass after the additive field lands

## Verification

This was a docs-and-code audit. I inspected the cited analyzer and `the-critic` files directly but did **not** run tests.
