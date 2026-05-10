# Stage 12 Cross-Workflow Renderer Law Generalization Scope Audit

Audited document: `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`

## Verdict

`Approve after revision`

## Findings

### 1. Stage 12 is the right next seam, but the memo overstates how much served-law substrate already exists

The ordering claim is basically right: after Stage 11, the next missing seam is stronger analyzer-owned served renderer law, not Stage 13 host-contract formalization. The roadmap already points in that order, and the route/result envelopes already know how to surface `BoundedCompositionValidationError` as HTTP 409 without new APIs.

But the memo currently reads too close to "the renderer-law substrate is already present and only needs broadening." That is not quite true in code:

- `src/presenter/renderer_contract_enforcement.py` only turns on strict final payload enforcement through `is_renderer_contract_enforced_mode(composition_mode)`, which still gates on a narrow `composition_mode` allowlist.
- `src/presenter/presentation_api.py` still does assembly-time payload validation in `ValidationMode.WARN` through `_validate_payload_data(...)`.
- `src/presenter/manifest_builder.py` still ties final strictness to `composition_mode`, not to a richer served-policy concept.

So Stage 12 is not just "generalize the existing law." It has to introduce a new analyzer-owned served-contract policy layer beyond `composition_mode`.

### 2. The memo calls the renderer-law substrate more universal than the current job-backed code really is

The transient Stage 11 path is now meaningfully recursive and tree-aware. The job-backed path is not yet symmetric with that.

Current partial seams:

- `src/presenter/manifest_builder.py` includes `child_view_keys` in manifest identity rows, but `content_manifest` is still built from flat top-level payload content rather than recursive child content.
- `src/presenter/manifest_builder.py` still sets `view_count=len(manifest_views)`, which is a flat manifest notion, not the Stage 11 transient tree-count semantics.
- `src/presenter/presentation_api.py` has real tree assembly in `_build_view_tree(...)`, but `_synthesize_container_payload(...)` is still chain-container-specific rather than general renderer-law infrastructure.
- `src/presenter/presentation_api.py` still leaves `tab_count=None` in `_build_view_payload(...)`, which is another sign that served container semantics are still partial.

That means the memo should stop short of calling the substrate "universal" or "already cross-workflow" today. Stage 12 should be framed as the first bounded generalization pass over a still-partial job-backed surface.

### 3. The proposed sub-renderer law is directionally correct, but still not concrete enough as written

Right now the codebase splits related concerns across three different layers:

- `src/presenter/view_contract_validator.py` validates authored curated view/template contracts and recurses into section/sub-renderer hints, but it is not a final served-boundary validator. It also still resolves effective contracts with `consumer_key="the-critic"`, so it is not universal consumer law.
- `src/presenter/runtime_override_validator.py` cleans and bounds runtime overrides, including consumer support checks for section/sub-renderer overrides. This is a preflight cleaning layer, not final served fail-closed law.
- `src/presenter/renderer_contract_enforcement.py` validates final payload `renderer_type`, `renderer_config`, and structured data recursively, but it does not itself define a general served-policy model for sub-renderer legality across workflows/consumers.

So the memo is right to say sub-renderer/container law belongs in Stage 12, but it needs a more explicit statement of what the new final law actually is:

- what inputs decide whether strict served-law applies
- what consumer support facts are consulted
- what final payload properties must be checked at serve time beyond ordinary schema validation
- how this final law relates to, but does not collapse into, authored contract validation or override cleaning

Without that, Stage 12 risks sounding more unified than the real seams are.

### 4. AOI plus genealogy is a defensible Stage 12 proof matrix, but only as a bounded first slice

The repo has enough cross-workflow truth to justify AOI plus genealogy as the Stage 12 proof matrix:

- Stage 10 readiness and downstream presentation truth are materially centered on AOI and genealogy.
- Result routes and presenter routes already exercise real page/manifest/result serving paths for those workflows.

That is enough for a first cross-workflow renderer-law slice. But it is not enough to justify universal platform language. The memo should say explicitly that AOI plus genealogy is a bounded proof matrix because they are the workflows with current downstream truth, not because the full renderer-law substrate is already workflow-agnostic.

### 5. The proof bar is still too weak if it can be satisfied mostly by saved success JSON

The memo is correct that Stage 12 needs stronger proof than another saved success case, but the current proof bar should be tightened further.

For this stage, the proof set should require:

- one AOI job-backed success on a real served route under the new Stage 12 policy
- one genealogy job-backed success on a real served route under the new Stage 12 policy
- one real fail-closed served-route case returning HTTP 409 on a renderer-law violation that previously would have stayed warn-only or only been cleaned opportunistically
- CI/preflight evidence showing the new served-law matrix is actually enforced in tests

If trace behavior remains non-fatal while page/manifest/result serving fails closed, that behavior split should also be documented explicitly instead of left implicit.

## Direct Answers

### Is Stage 12 really the next missing seam, or is the memo underplaying remaining Stage 13 host-contract work?

Stage 12 is the right next seam. The current analyzer-side served contract is still too partial to make Stage 13 host-contract generalization the next step. But the memo should keep saying that explicitly and avoid any implication that Stage 12 itself solves host-contract generalization.

### Does the codebase actually support richer served-contract policy beyond `composition_mode`, or would the memo need more incremental shape?

No. The codebase does not yet have a richer served-contract policy beyond `composition_mode`. Stage 12 needs to create that layer explicitly rather than assuming it already exists in near-finished form.

### Is the proposed sub-renderer law concrete enough given the split between view-contract validation, runtime override cleaning, and final payload validation?

Not yet. The memo identifies the right seam, but it still needs a more explicit model for how final served sub-renderer/container legality is decided and where that decision lives.

### Does the repo already have enough cross-workflow truth to justify AOI plus genealogy as the Stage 12 proof matrix?

Yes, as a bounded first slice. No, if the memo tries to treat that matrix as proof that renderer-law generalization is already universal.

### Is the memo keeping Stage 11 surface-planning work and Stage 13 host work out of scope?

Mostly yes. The memo should keep Stage 11 semantic grouping and Stage 13 host-contract formalization explicitly out of scope and avoid wording that pulls either back in through the side door.

### Is the proof bar strong enough to distinguish real fail-closed renderer law from another saved-JSON success case?

Not yet. It needs explicit served-route 409 evidence and CI/preflight enforcement evidence.

### Additional relevant docs beyond the usual materials?

I did not find additional materially relevant design docs beyond the usual `communications/` and `docs/` materials. The other files outside those directories were tool output, local notes, or auxiliary context, not primary scope-setting documents for this audit.

## Required Revisions

1. Reframe Stage 12 as creation of a new analyzer-owned served-contract policy layer, not just broadening the current `composition_mode` gate.
2. Remove or soften any wording that presents the current renderer-law substrate as already universal across served workflows.
3. Make the job-backed asymmetries explicit:
   - warn-only assembly validation still exists
   - manifest content semantics are still flatter than Stage 11 transient tree semantics
   - container synthesis still has chain-container-specific seams
4. Define the Stage 12 sub-renderer/container law more concretely across:
   - authored contract validation
   - override cleaning
   - final served payload enforcement
5. State that AOI plus genealogy is the bounded proof matrix because those workflows have current downstream truth, not because the platform is already universally generalized.
6. Raise the proof bar to require route-level success and route-level fail-closed evidence, plus CI/preflight enforcement evidence.

## Summary

The memo has the right strategic direction: Stage 12 should come before Stage 13, and the missing seam is stronger analyzer-owned served renderer law across current job-backed workflows. But it currently overstates how general the substrate already is, understates the need for a new served-policy layer beyond `composition_mode`, and leaves the final sub-renderer law too implicit. With those revisions, the scope would be ready to approve.
