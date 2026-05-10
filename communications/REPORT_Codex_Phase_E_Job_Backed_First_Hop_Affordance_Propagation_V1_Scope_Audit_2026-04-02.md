# Report: Phase E Job-Backed First-Hop Affordance Propagation V1 Scope Audit

## 1. Verdict

**Approve with corrections.**

The memo is directionally right. After the transient first-hop affordance closeout, the smallest honest next analyzer-side variable is surface propagation onto the mainstream job-backed presenter line, not richer output-specific semantics, not destination lifecycle, and not host UX work.

The core reason is code-backed:

- the transient line already proved the semantic object and the contract/content hash split in `src/presenter/compose_from_intent.py:1392-1559`
- the job-backed line already has one shared page/manifest seam in `src/presenter/manifest_builder.py:152-263`
- `build_presentation_manifest(...)` and `assemble_page(...)` already converge there in `src/presenter/presentation_api.py:838-979`

But the memo needs tightening in four places before it should be treated as the exact implementation brief:

1. it needs a concrete **job-backed** emission predicate, not just a restatement of the transient boundary
2. it needs to state the `build_presentation_trace(...)` consequences more carefully
3. it should describe manifest propagation as mainly **contract-honesty/future-proofing**, not current host-facing value
4. shared-model generalization should stay minimal rather than turning into a broader affordance extraction exercise

## 2. The Memo's Strongest Code-Backed Points

- `ViewPayload` and `EffectiveManifestView` are the right attachment surfaces.
  - `PagePresentation.views` is a tree of `ViewPayload` objects in `src/presenter/schemas.py:191-297`.
  - `EffectivePresentationManifest.views` is a flat list of `EffectiveManifestView` objects in `src/presenter/schemas.py:298-344`.
  - Those are the public job-backed view contracts today.

- One shared job-backed population seam already exists.
  - `build_effective_manifest(...)` iterates the flat `payloads` set, derives each `EffectiveManifestView`, and then mutates the same `ViewPayload` objects with final contract-resolved metadata in `src/presenter/manifest_builder.py:171-218`.
  - `build_presentation_manifest(...)` and `assemble_page(...)` both call that same helper in `src/presenter/presentation_api.py:862-885` and `src/presenter/presentation_api.py:926-979`.
  - That makes `build_effective_manifest(...)` the right exact seam for one shared affordance-population helper.

- The job-backed hash substrate already matches the transient honesty rule.
  - Transient affordance metadata already changes `presentation_hash` but not `presentation_content_hash` in `src/presenter/compose_from_intent.py:1511-1529` and `src/presenter/compose_from_intent.py:1537-1559`, with direct coverage in `tests/test_compose_from_intent.py:2169-2225`.
  - Job-backed manifest hashing already has the same contract/content split in `src/presenter/manifest_builder.py:236-263`.
  - So this slice does not need a new hash philosophy; it only needs to apply the existing one consistently.

- Page/manifest/trace parity is already a real job-backed invariant.
  - `tests/test_manifest_trace.py:847-867` proves that the final trace snapshot equals the manifest and that page hashes equal manifest hashes.
  - That is exactly why the affordance cannot be page-only. If it lands on `PagePresentation.views`, it also needs to land on manifest views and hash identity.

- The bounded field family is supported by current runtime evidence.
  - Critic’s generic capture system is explicitly bounded to `arsenal` and `research_todo` in `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:37-38` and `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx:130-144`.
  - The workspace action bar exposes those same two first-hop actions in `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx:117-152`.
  - That makes the memo’s fixed v1 family:
    - `capturable`
    - `allowed_destinations=["arsenal","research_todo"]`
    the strongest currently evidenced generic first-hop contract.

- The memo keeps thin-host ownership honest.
  - The job-backed workspace already wraps `PagePresentation.views` in `CaptureProvider` and `CaptureActionBar` in `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:995-1142`.
  - `V2TabContent` threads generic capture hooks into renderers through `_captureMode` / `_onCapture` in `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:579-587`.
  - Renderer components operationalize the actual UX locally, for example in `/home/evgeny/projects/the-critic/webapp/src/components/renderers/SynthesisRenderer.tsx:96-113` and `/home/evgeny/projects/the-critic/webapp/src/components/renderers/IdeaEvolutionRenderer.tsx:555-571`.
  - So analyzer-side propagation would add upstream semantic truth without pulling button placement, annotation flows, or routing lifecycle into analyzer-v2.

## 3. The Memo's Weakest Or Overstated Assumptions

- The memo says it preserves the same narrow emission boundary, but the **job-backed** code path does not have the same route primitive as transient compose.
  - The transient implementation has a real route gate:
    - `_handoff_supports_first_hop_affordance(...)` in `src/presenter/compose_from_intent.py:1388-1439`
  - The job-backed presenter path has no `handoff_kind`; it is view-definition-driven and job/workflow-driven.
  - So “same boundary” cannot literally mean “reuse the same gate.”
  - The memo should specify a concrete job-backed eligibility rule such as:
    - current migrated AOI/genealogy workflows only
    - `payload.engine_key` in the migrated engine family
    - `payload.children == []`
    - parent/container views omitted even if they carry structured parent data

- `EffectivePresentationManifest.views` is not currently a mainstream host-consumed rendering surface in Critic.
  - Critic uses `getBoundedV2ResultManifest(...)` mainly for freshness / restore decisions in `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:282-315`, `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:365-369`, and `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:409-421`.
  - Its local `V2ResultManifest` type does not even model manifest views in `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts:39-52`.
  - So manifest propagation is still correct, but mainly because:
    - it keeps hash identity honest
    - it keeps trace/final-manifest parity honest
    - it prevents page-only metadata drift
  - It should not be sold as an immediate host-visible product win.

- `build_presentation_trace(...)` is only partly automatic.
  - The trace endpoint gets its `final_manifest` from `build_presentation_manifest(...)` in `src/presenter/decision_trace.py:73-91`, so the final manifest and final snapshot will inherit the new field.
  - But the earlier stage snapshots are reconstructed independently through `_build_stage_snapshot(...)` and explicit `EffectiveManifestView(...)` creation in `src/presenter/decision_trace.py:142-203` and `src/presenter/decision_trace.py:444-465`.
  - If the slice wants stage-level affordance provenance or non-`None` affordance values before the final stage, that is additional work and should stay deferred.

- Shared affordance-model generalization is justified only in the smallest form.
  - One shared nested schema reused by transient and job-backed contracts is reasonable.
  - A broader rename/extraction toward a general “affordance framework” is not justified yet.
  - The memo should say “share the two-field nested model,” not imply a larger generalization program.

## 4. Factual Discrepancies I Found

- The roadmap documents cited as context are not independent evidence for this memo.
  - They have already been updated after the transient closeout to say that job-backed propagation is next:
    - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md:375-391`
    - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md:404-417`
    - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md:517-519`
  - Those documents are useful for ordering, but the real independent support is the live presenter/host code.

- Current host code still does not consume the already-landed transient affordance field.
  - `TransientComposeView` in `/home/evgeny/projects/the-critic/webapp/src/types/transientCompose.ts:71-98` does not include `first_hop_affordance`.
  - `adaptTransientViews(...)` in `/home/evgeny/projects/the-critic/webapp/src/lib/transientComposeAdapters.ts:15-58` does not thread it through either.
  - So the transient affordance closeout already proved a contract seam without any host adoption.
  - The job-backed memo should keep the same honesty: this slice is additive contract propagation, not immediate UX exposure.

- Current job-backed host types also omit any affordance field.
  - Critic’s local `ViewPayload` type in `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:58-83` has no affordance field.
  - That again supports the memo’s “no host changes required for correctness” claim.
  - But it also means the field will be silent until a later host-adoption slice.

- The memo is right that `PagePresentation` is the mainstream job-backed rendering surface, but it should be more precise about `EffectivePresentationManifest`.
  - `AnalysisWorkspacePage` renders `PagePresentation.views` directly in `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:1118-1137`.
  - The current host does not render manifest views.
  - So page propagation has immediate contract relevance to the main runtime surface; manifest propagation is primarily a correctness consequence of the existing hash/trace architecture.

## 5. What This Changes For The Larger Roadmap

- No major reorder is needed.
  - The next bounded analyzer-side move should still be job-backed propagation of the already-landed first-hop family.

- But the roadmap should describe this slice more narrowly than the memo currently does.
  - This is a **surface-propagation and contract-honesty** slice.
  - It is not the slice where affordance semantics become richer.
  - It is not the slice where hosts become affordance-driven.

- The next semantic broadening should come only after this propagation slice lands cleanly.
  - The first meaningful semantic follow-on should be one output-specific family that actually varies by surface.
  - The strongest candidates remain:
    - findings-bank promotion semantics
    - one bounded outline-routing family
  - Destination lifecycle should remain later than both.

- Host adoption should stay a separate later step.
  - Current Critic capture behavior is still driven by host-local renderer/config heuristics, not analyzer-owned affordance fields.
  - That is acceptable now.
  - It should just be described honestly in the roadmap.

## 6. The Most Defensible Next Move After This Memo

- Approve the slice after tightening the implementation brief.

- Keep the semantics fixed:
  - `capturable`
  - `allowed_destinations=["arsenal","research_todo"]`

- Reuse one minimal shared nested model across:
  - `TransientIntentView`
  - `ViewPayload`
  - `EffectiveManifestView`

- Populate it through one helper invoked from the `build_effective_manifest(...)` path.
  - That is the strongest exact seam because:
    - `build_presentation_manifest(...)` converges there
    - `assemble_page(...)` converges there
    - `get_presentation_status(...)` also converges there
    - single-view fetches also run through the same contract-resolution helper path in `src/presenter/presentation_api.py:1003-1028` and `src/presenter/presentation_api.py:1075-1091`

- Make the job-backed emission rule explicit and testable.
  - Do not just say “same narrow boundary.”
  - State the concrete predicate for job-backed payloads.

- Treat contract identity explicitly:
  - `presentation_hash` changes when the affordance contract changes
  - `presentation_content_hash` does not change when only the affordance object changes
  - final manifest/page parity remains intact
  - final trace manifest/snapshot remain aligned
  - stage-level affordance provenance remains deferred

- Focus verification on the real affected seams:
  - `tests/test_manifest_trace.py`
  - `tests/test_presentation_api.py`
  - `tests/test_analysis_product_contract.py`
  - plus a focused job-backed hash test and page/manifest parity test for the new field

## Bottom Line

This is the right next analyzer-side slice, and it is smaller and stronger than jumping straight to one output-specific affordance family.

But the memo should be corrected before implementation starts:

- define the job-backed eligibility predicate concretely
- describe manifest propagation as contract-honesty, not current UX value
- state the `build_presentation_trace(...)` limitation explicitly
- keep the shared-model generalization minimal

With those corrections, the memo becomes a defensible next-step brief.

## Verification Note

This was a docs-and-code audit tranche. I inspected the cited analyzer-v2 and Critic files directly and did **not** run tests.
