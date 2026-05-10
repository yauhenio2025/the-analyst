# Critique: Phase E Job-Backed First-Hop Affordance Propagation V1 Scope

Reviewer: Claude (Opus 4.6, fresh session)
Date: 2026-04-02
Subject Memo: `communications/MEMO_2026-04-02_phase_e_job_backed_first_hop_affordance_propagation_v1_scope.md`

---

## 1. Verdict

**Approve with corrections.**

The sequencing is right. This is the correct immediate next analyzer-side slice after the transient first-hop affordance closeout. The strategic logic — vary the surface contract while keeping semantics fixed — is the smallest honest next variable. The scope boundaries are disciplined. The hash/contract distinction is correctly framed.

But the memo has three mechanical gaps and one design ambiguity that should be resolved before implementation begins. None of them change the strategic decision; they change how the implementation lands.

---

## 2. Strongest Parts Of The Memo

### A. The surface-generalization thesis is correct and well-argued

The memo's central argument is clean:

- the transient line already proved the seam
- the next honest variable is whether the same bounded hint family survives the mainstream job-backed contracts
- this is smaller and stronger than inventing richer semantics on the next move

That is exactly right. The alternative paths (findings-specific affordances, research-answer routing, outline routing) all introduce non-uniform semantics AND broader output-family law. This slice introduces neither. It is a pure surface propagation step.

### B. ViewPayload and EffectiveManifestView are the right attachment surfaces

Code-confirmed:

- `ViewPayload` (`src/presenter/schemas.py:191-254`) is the internal payload that both `build_presentation_manifest()` and `assemble_page()` operate on
- `EffectiveManifestView` (`src/presenter/schemas.py:298-319`) is the data-light semantic contract exposed through the manifest
- `PagePresentation.views` is typed as `list[ViewPayload]` and is populated from the same payloads dict
- So populating the affordance on `ViewPayload` naturally flows through to `PagePresentation` without duplication

This is the cleanest pair of attachment surfaces on the job-backed line.

### C. The hash honesty framing is correct

The memo says:

- contract hash includes the affordance object
- content hash does not treat it as analytical content

That matches the existing discipline on both surfaces:

- Transient: `_transient_identity_row()` includes `first_hop_affordance`, while `_transient_content_row()` does not (`src/presenter/compose_from_intent.py:1535-1565`)
- Job-backed: `_manifest_identity_row()` determines contract hash input (`manifest_builder.py:276-294`), while the content manifest uses output hashes and structured_data (`manifest_builder.py:241-253`)

The same contract/content distinction is ready to carry the new field.

### D. The emission boundary is correctly conservative

Keeping emission to migrated-family analytical leaf views only, while leaving parent/container views and non-proved workflows unannotated, is the right discipline. The transient line already established this rule and the job-backed line should not broaden it.

### E. The out-of-scope list is right

Every deferred item (`commentable`, findings-specific promotion, research-answer routing, outline routing, destination lifecycle, host UX) is correctly held back. These are all later questions that should not be absorbed into a surface-propagation slice.

---

## 3. Weakest Assumptions

### A. The memo does not address how workflow_key gates emission on the job-backed line

This is the most important mechanical gap.

On the transient line, emission is gated by `_handoff_supports_first_hop_affordance(*, workflow_key, handoff_kind)` — a check against a `frozenset` of approved `(workflow_key, handoff_kind)` pairs. That function lives in `compose_from_intent.py:1388-1393`.

On the job-backed line, there is no `handoff_kind` concept. The gating must use `workflow_key` from the job record. But:

- `build_effective_manifest()` (`manifest_builder.py:152-273`) does **not** currently receive `workflow_key`
- The function's signature is: `build_effective_manifest(*, job_id, plan_id, consumer_key, served_intent, composition_mode, thinker_name, strategy_summary, payloads, all_outputs, job)`
- `workflow_key` is available via `job.get("workflow_key")` or from the plan, but the function doesn't currently extract or use it

So the implementation needs either:

a. Pass `workflow_key` into `build_effective_manifest()` and gate affordance there
b. Populate affordance on ViewPayloads **before** `build_effective_manifest()` is called, using `workflow_key` from `_prepare_page_payloads()`

Option (b) is cleaner — it keeps `build_effective_manifest()` focused on manifest construction, and the affordance population becomes a pre-processing step. But the memo should say which path it intends.

### B. The memo says "one shared helper on the job-backed ViewPayload line used by build_effective_manifest" but this phrasing is ambiguous

It could mean:

1. A helper that runs **inside** `build_effective_manifest()` during the per-payload loop
2. A helper that runs **before** `build_effective_manifest()` to annotate ViewPayloads

The code structure suggests option (2) is better, because:

- `_prepare_page_payloads()` (`presentation_api.py:807-835`) is the single function that prepares both the payloads dict and the outputs cache
- Both `build_presentation_manifest()` and `assemble_page()` call `_prepare_page_payloads()` first, then `build_effective_manifest()` second
- `_prepare_page_payloads()` already has `workflow_key` available
- Annotating payloads after `_prepare_page_payloads()` but before `build_effective_manifest()` keeps the manifest builder ignorant of affordance logic

But the actual cleanest seam may be inside `_prepare_page_payloads_for_recommendations()` (`presentation_api.py:658-804`), which is where payloads are built and `workflow_key` is already resolved. Adding affordance annotation at the end of that function, after payloads are constructed, would centralize the logic.

### C. EffectiveManifestView needs an explicit new field, but the memo does not name the field type or its interaction with decision-trace diffing

Adding an affordance field to `EffectiveManifestView` has two consequences the memo doesn't address:

**1. Decision-trace _diff_snapshots field list**

`decision_trace.py:540-552` defines the fields that get diffed between trace snapshots:

```python
fields = (
    "renderer_type",
    "renderer_config",
    "presentation_stance",
    "selection_priority",
    "navigation_state",
    "promoted_to_top_level",
    "display_parent_view_key",
    "structuring_policy",
    "derivation_kind",
    "semantic_scaffold_type",
    "scaffold_hosting_mode",
)
```

If `EffectiveManifestView` gains a `first_hop_affordance` field (or whatever it's named), that field should be added to this tuple, or the decision trace will silently ignore affordance changes between stages. The memo's out-of-scope item "trace-only affordance propagation" is about a different concern (trace-only metadata, not trace diffing of the affordance field).

**2. _manifest_identity_row needs the new field**

`_manifest_identity_row()` (`manifest_builder.py:276-294`) determines what goes into the contract hash. The new affordance field must be added there explicitly. The memo's acceptance criterion #8 implies this but doesn't name the function.

### D. The shared model naming is not addressed

The current transient affordance model is named `TransientFirstHopAffordance`. If it is reused on job-backed surfaces, the "Transient" prefix becomes misleading. The memo says "normalize the model into one shared presenter-side type" but doesn't name it or say whether the current `TransientFirstHopAffordance` should be renamed.

This is a minor point but it affects import paths and test readability across the codebase. A rename to `FirstHopAffordance` (dropping the `Transient` prefix) would be the natural move, and the memo should say so explicitly.

---

## 4. Code-Backed Findings

### Finding 1: build_effective_manifest already has the right loop structure for propagation

`manifest_builder.py:171-218` iterates over payloads, builds manifest views, and writes back enriched fields to the payload:

```python
for payload in ordered_payloads:
    # ... derive various fields ...
    manifest_view = EffectiveManifestView(...)
    manifest_views.append(manifest_view)

    # Write enriched values back to payload
    payload.selection_priority = manifest_view.selection_priority
    payload.navigation_state = manifest_view.navigation_state
    # ... etc ...
```

If affordance were populated on the `ViewPayload` before this loop, the loop could simply pass it through to `EffectiveManifestView`. No duplication needed. If affordance were populated inside the loop, the pattern already supports it. Either way, the code structure is ready.

### Finding 2: No affordance-related code exists anywhere on the job-backed presenter path

A search for `first_hop` and `affordance` across `src/presenter/` finds hits only in:

- `compose_from_intent.py` (transient line)
- `schemas.py` (TransientFirstHopAffordance, TransientIntentView)

Nothing in `presentation_api.py`, `manifest_builder.py`, or `decision_trace.py` touches affordance. This confirms the propagation is additive — no existing logic conflicts.

### Finding 3: No test coverage for affordance on job-backed surfaces

- `tests/test_manifest_trace.py`: 0 hits for `first_hop` or `affordance`
- `tests/test_presentation_api.py`: 0 hits
- `tests/test_analysis_product_contract.py`: 0 hits

All existing affordance tests are in `tests/test_compose_from_intent.py` and `tests/test_representative_composition_matrix.py`, which cover only the transient line. The test plan in the scope memo correctly identifies the right verification surfaces, but the gap is real: everything must be new tests.

### Finding 4: The host does not currently consume any affordance field from job-backed surfaces

From the-critic codebase:

- `V2TabContent.tsx` renders ViewPayload from PagePresentation
- Capture is entirely host-driven via `CaptureContext.tsx`
- No code reads a `first_hop_affordance` field from ViewPayload or PagePresentation
- `boundedV2Client.ts` fetches the full page but doesn't extract affordance

This confirms acceptance criterion #11 is achievable: "no host code changes are required for correctness." The field will flow through to the host as additive optional metadata that the host can ignore until it chooses to consume it.

### Finding 5: The population seam question is concretely answerable

Looking at the two call sites:

**build_presentation_manifest** (`presentation_api.py:838-885`):
```python
page_inputs = _prepare_page_payloads(...)
manifest = build_effective_manifest(..., payloads=page_inputs["payloads"], ...)
```

**assemble_page** (`presentation_api.py:888-980`):
```python
page_inputs = _prepare_page_payloads(...)
manifest = build_effective_manifest(..., payloads=payloads, ...)
return PagePresentation(..., views=styled_views, ...)
```

Both share `_prepare_page_payloads()`. The affordance helper should run **after** `_prepare_page_payloads()` returns and **before** `build_effective_manifest()` processes the payloads. This is the single narrowest seam where both paths converge and where `workflow_key` is available from `page_inputs["workflow_key"]`.

The helper would look like:

```python
def _annotate_first_hop_affordances(
    payloads: dict[str, ViewPayload],
    *,
    workflow_key: str,
) -> None:
    ...
```

Called in both `build_presentation_manifest()` and `assemble_page()` before `build_effective_manifest()`.

### Finding 6: The leaf vs container check on the job-backed line differs from the transient line

On the transient line, `_derive_first_hop_affordance()` checks:

- `payload.children` is empty (leaf)
- `payload.engine_key` is in `_MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS`

On the job-backed line, `payload.children` is populated by `_build_view_tree()` in `presentation_api.py`. So the same check (`payload.children` empty + engine_key in migrated family) should work. But the tree is already built by the time `_prepare_page_payloads()` returns, so the leaf check is safe.

However, on the job-backed line, views also have `source_parent_view_key` and nested `children` through the view hierarchy module. A view without children in its `ViewPayload.children` list is a leaf. This is straightforward.

---

## 5. Strategic Implications For The Roadmap

### A. This slice completes the surface-coverage step

If this lands, the honest claim becomes:

- analyzer-v2 can carry the same bounded first-hop affordance object on BOTH the transient compose line and the mainstream job-backed presentation line

That is a complete surface-coverage step. The next honest question shifts from "can we propagate the same hints?" to "can we produce non-uniform hints?" — which is the output-specific affordance family question.

### B. The follow-on order is correctly framed

After this slice:

1. Output-specific first-hop affordance family (findings-bank promotion, outline routing)
2. Non-uniform destination sets (some views get `["arsenal"]` only, some get more)
3. Eventually: destination lifecycle

This matches the distilled strategic roadmap and the Close Read flagship direction.

### C. The shared model move is strategically correct but needs naming discipline

Unifying `TransientFirstHopAffordance` into a shared `FirstHopAffordance` type is the right move. But when this lands, the transient line's tests and code will need to import the renamed type. The memo should note that the transient test files (`test_compose_from_intent.py`, `test_representative_composition_matrix.py`) will need import updates.

### D. The decision-trace gap is real but bounded

Adding the field to `EffectiveManifestView` without adding it to the trace diff fields tuple is a latent correctness gap. It won't break anything — traces will simply be blind to affordance changes. But it should be fixed in this slice because:

- it is a one-line addition to the fields tuple
- leaving it for later means traces silently under-report contract changes
- the memo already says this is a contract-level field, and the trace is designed to track contract changes

---

## 6. Concrete Corrections Or Reframing

### Correction 1: Name the workflow_key gating mechanism explicitly

Add to the design section:

> On the job-backed line, there is no handoff_kind concept. Emission gating should use `workflow_key` from the job record. The affordance annotation helper should receive `workflow_key` as a parameter and check it against the same approved workflow family as the transient line (AOI, genealogy). Non-proved workflows should remain unannotated.

This is the most important correction because without it, the implementation could accidentally annotate all job-backed views regardless of workflow.

### Correction 2: Specify the population seam more precisely

Replace:

> one shared helper on the job-backed `ViewPayload` line used by `build_effective_manifest(...)`

With:

> One shared affordance annotation helper called after `_prepare_page_payloads()` returns and before `build_effective_manifest()` processes the payloads, in both `build_presentation_manifest()` and `assemble_page()`. This keeps affordance population out of the manifest builder itself and positions it where `workflow_key` is available from `page_inputs["workflow_key"]`.

### Correction 3: Add decision-trace field propagation to acceptance criteria

Add an acceptance criterion:

> 12. The decision-trace `_diff_snapshots` field list includes the new affordance field so that trace diffing correctly reports affordance changes between trace stages.

Without this, the trace would silently ignore affordance changes even though it tracks every other contract-level field.

### Correction 4: Add _manifest_identity_row to the hash acceptance criteria

The memo says "effective manifest hash identity" but doesn't name the function. Clarify:

> `_manifest_identity_row()` in `manifest_builder.py` must include the new affordance field, so that the contract hash changes when the affordance contract changes.

### Correction 5: Name the shared model

Add to the design section:

> The current `TransientFirstHopAffordance` should be renamed to `FirstHopAffordance` (or equivalent) to reflect its shared status. The `TransientFirstHopDestination` type literal should similarly become `FirstHopDestination`. Existing transient-line code and tests should update their imports accordingly.

### Correction 6: Explicitly note that the transient line's tests need import updates but not behavior changes

The test plan says transient tests should stay "unchanged except for the new additive metadata." More precisely: tests in `test_compose_from_intent.py` and `test_representative_composition_matrix.py` may need import path changes if the model is renamed, but their behavioral assertions should remain identical. The memo should distinguish import updates from behavior changes.

---

## 7. Is There A Smaller Or Stronger Slice?

No. This is the smallest honest next slice on the analyzer side.

The alternatives considered:

- **Output-specific affordance family first**: This requires introducing non-uniform semantics and output-family law. That is strictly larger than surface propagation with fixed semantics.
- **Only add the field to ViewPayload, not EffectiveManifestView**: This would be incomplete — the manifest is the data-light semantic contract and it should carry the same metadata. Splitting across surfaces creates an inconsistency that the next consumer would immediately notice.
- **Skip job-backed entirely and go to output-specific on transient**: This would leave the mainstream presentation line unaware of affordances indefinitely. Since job-backed is the primary long-lived rendering surface, deferring it would mean the most-used surface never carries the hint.

The proposed slice is the right size.

---

## Bottom Line

Approve after the six corrections above. The strategic logic is the strongest part of the memo — vary the surface, keep semantics fixed. The mechanical gaps (workflow_key gating, population seam precision, decision-trace field propagation, _manifest_identity_row, shared model naming, import update discipline) are all fixable within the existing scope without changing the strategic claim.

This is the most defensible immediate next analyzer-side code move after the transient first-hop affordance closeout.

**Verification Note**

This was a docs-and-code audit. The following files were inspected directly:

- `src/presenter/schemas.py` (full)
- `src/presenter/manifest_builder.py` (full)
- `src/presenter/presentation_api.py` (key functions: `_prepare_page_payloads`, `_prepare_page_payloads_for_recommendations`, `build_presentation_manifest`, `assemble_page`)
- `src/presenter/decision_trace.py` (full)
- `src/presenter/compose_from_intent.py` (via agent: full analysis of affordance flow)
- `tests/test_compose_from_intent.py` (affordance-related tests)
- `tests/test_manifest_trace.py` (function list, no affordance tests found)
- `tests/test_presentation_api.py` (no affordance tests found)
- `tests/test_analysis_product_contract.py` (no affordance tests found)
- `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx` (via agent)
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx` (via agent)
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts` (via agent)
- `/home/evgeny/projects/the-critic/webapp/src/contexts/CaptureContext.tsx` (via agent)
- `/home/evgeny/projects/the-critic/webapp/src/components/CaptureActionBar.tsx` (via agent)
- All referenced communications memos and review reports

No tests were run.
