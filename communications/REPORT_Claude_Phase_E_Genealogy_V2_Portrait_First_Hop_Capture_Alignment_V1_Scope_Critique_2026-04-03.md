# Report: Phase E Genealogy V2 Portrait First-Hop Capture Alignment V1 Scope Critique

Date: 2026-04-03
Reviewer: Claude Opus 4.6
Scope Memo: `communications/MEMO_2026-04-03_phase_e_genealogy_v2_portrait_first_hop_capture_alignment_v1_scope.md`

## Verdict: APPROVE

The slice is strategically correct, correctly scoped, and honest about its boundaries.

## Findings

### Finding 1: The Slice Is Strategically Necessary, Not Just Locally Tidy (Strength)

Severity: Strategic (positive)

The distilled roadmap's Rule 4 says "prefer representative matrices over exhaustive workflow theater." The current Phase E consumer matrix is:

| Surface | Workflow | Status |
|---------|----------|--------|
| `aoi_by_sin_type` | AOI | Aligned (pure findings, capture+readback) |
| `aoi_by_theme` | AOI | Aligned (mixed surface, nested findings) |
| `genealogy_portrait` | Genealogy | **GAP: host-local unconditional gating** |
| `genealogy_idea_evolution` | Genealogy | GAP: deferred |

All four current-V2 consumer surfaces are AOI or genealogy. Closing one genealogy surface is a genuine matrix-broadening move because it proves the analyzer-owned first-hop contract works across workflow families, not just within AOI. This is not cleanup; it is the minimum evidence needed to claim the contract is workflow-neutral.

The stronger strategic point, which the memo could be more explicit about: **this slice is a prerequisite for generic custom-renderer contract law extraction.** You cannot honestly extract a generic pattern from one workflow family. After this slice, you have AOI renderers (CardGrid with specialized finding semantics, plus the accordion shim) and one genealogy renderer (SynthesisRenderer with section-level capture) both consuming the same analyzer contract. That gives you two structurally different data points from which to extract a reusable pattern. Without this slice, generic law would be premature.

### Finding 2: All Six Code Claims Are Verified (Strength)

Severity: Evidence (positive)

I verified each of the memo's six evidence claims against the actual code:

1. **analyzer-v2 supports generic first-hop on genealogy**: Confirmed. `src/presenter/first_hop_affordance.py` includes `GENEALOGY_WORKFLOW_KEY = "intellectual_genealogy"` in `FIRST_HOP_AFFORDANCE_ELIGIBLE_WORKFLOW_KEYS`, and `genealogy_final_synthesis` is in `MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS`. The `genealogy_portrait` view definition at `src/views/definitions/genealogy_portrait.json` confirms `engine_key: "genealogy_final_synthesis"` and `workflow_key: "intellectual_genealogy"`.

2. **`genealogy_portrait` is a live current non-AOI V2 surface**: Confirmed. View definition exists, `target_app: "the-critic"`, `status: "active"`.

3. **V2TabContent threads all metadata**: Confirmed. `V2TabContent.tsx` threads `_firstHopAffordance` (line 597), `_workflowKey` (line 580), `_captureViewKey`, `_captureViewName`, `_captureSourceType`, `_captureJobId`, `_captureEntityId` (set to `presentation.job_id`), `_onCapture`, and `_captureMode`.

4. **SynthesisRenderer uses host-local unconditional gating**: Confirmed. `SynthesisRenderer.tsx` gates capture controls with `if (!captureMode || !onCapture) return null` (line 97). It does not read `_firstHopAffordance` from config at all.

5. **SynthesisRenderer omits `source_workflow_key`**: Confirmed. The capture selection object in `renderCaptureBtn` (lines 96-129) includes 10 fields but not `source_workflow_key`. The `CaptureSelection` interface in `CaptureContext.tsx` (line 35) defines `source_workflow_key?: string` and the capture submission at line 114 forwards it: `source_workflow_key: currentSelection.source_workflow_key || null`. The pipe is ready; the renderer just doesn't fill it.

6. **`genealogy_portrait` is smaller than broadening all genealogy renderers**: Confirmed. `IdeaEvolutionRenderer.tsx` is 944 lines with V1/V2 format detection, multi-pass data joining, and both L1_section and L2_element depth levels. SynthesisRenderer is 299 lines with uniform L1_section only. SynthesisRenderer is the unambiguously simpler starting case.

### Finding 3: `entity_id` Semantics Are Honest But Should Be More Explicit (Minor)

Severity: Low

The memo says `entity_id = _captureEntityId || _captureJobId` and warns to "treat entity_id here as bounded run/job identity, not a claim of per-item genealogy identity semantics."

Code confirms `_captureEntityId` is set to `presentation.job_id` in V2TabContent. So `entity_id` will always resolve to `job_id` for genealogy surfaces. This is honest: genealogy sections don't have per-item handles like AOI's `finding_id`.

But the memo could note one consequence more explicitly: this means the `entity_id` on genealogy captures will not distinguish between different sections of the same portrait. Two captures from different sections of the same genealogy run will share the same `entity_id`. That's fine for this slice (the slice doesn't claim per-section identity), but it means future read-side status surfacing on genealogy will need a different disambiguation strategy than AOI's `finding_id`-based approach. This is not a blocker; it's an honest open question the memo should acknowledge rather than leaving implicit.

### Finding 4: The "No Analyzer Changes" Claim Is Correct (Strength)

Severity: Evidence (positive)

The analyzer-v2 first-hop contract is already complete for this surface. `derive_first_hop_affordance` in `first_hop_affordance.py` returns `FirstHopAffordance(capturable=True, allowed_destinations=["arsenal", "research_todo"])` for any migrated leaf payload when the workflow is `intellectual_genealogy`. No `specialized_family` is set (correct - genealogy doesn't have findings-bank semantics).

The presenter already attaches this via `attach_first_hop_affordances()` in `presentation_api.py` (lines 837-840). The manifest builder already serializes it. The gap is purely host consumption.

### Finding 5: Anti-Drift Assessment Is Positive (Strategic)

Severity: Strategic (positive)

Testing against the distilled roadmap's four decision heuristics:

1. *Does this move intelligence upstream into analyzer-v2?* No - the analyzer contract already exists. But this proves the upstream intelligence is consumed. A contract nobody reads is not intelligence; it's aspiration. This slice turns aspiration into evidence.

2. *Does this reduce host-specific analytical behavior?* Yes. The current SynthesisRenderer has host-local unconditional `captureMode && onCapture` gating. After this slice, it consults `_firstHopAffordance.capturable` - an analyzer-owned truth. That is a real reduction in host analytical autonomy.

3. *Does this strengthen generic law rather than one more special case?* Indirectly yes. It creates the second workflow-family data point needed before generic law extraction is honest. One AOI example is a special case. One AOI + one genealogy example is a pattern.

4. *Does this help eventual contract-based generality?* Yes. The first-hop contract is already generic; this slice proves a non-AOI consumer can use it without modification.

Score: 3.5/4 positive. The 0.5 deduction is because the slice doesn't itself create generic law - it creates the prerequisite. But that's the honest order of operations.

### Finding 6: The Alternative Next Moves Are Correctly Deferred (Strategic)

Severity: Strategic (positive)

The memo lists six "not this" alternatives. Each is correctly deferred:

- **Another AOI-only consumer proof**: Correctly rejected. AOI is closed enough. Doing more AOI work is the distilled roadmap's "exhaustive workflow theater."
- **Generic renderer-package law extraction**: Correctly deferred. Cannot honestly extract a pattern from one workflow family. After this slice, extraction becomes defensible.
- **Non-AOI read-side status surfacing first**: Correctly deferred. You cannot read back what has not been correctly captured. Capture correctness must precede readback.
- **Multi-renderer genealogy refactoring**: Correctly deferred. SynthesisRenderer first, IdeaEvolutionRenderer later.
- **Analyzer-side first-hop semantic broadening**: Correctly deferred. The analyzer side is already sufficient; the gap is consumption.
- **Workflow-neutral destination semantics**: Correctly deferred. Too ambitious for this slice.

### Finding 7: The Test Plan Is Adequate But Has One Gap (Minor)

Severity: Low

The test plan covers:
- Capture controls gated on `_firstHopAffordance?.capturable === true` (correct)
- Capture controls hidden when affordance absent (correct)
- Selection includes `source_workflow_key` (correct)
- Selection includes `genealogy_job_id` for backward compat (correct)
- `entity_id` from `_captureEntityId || _captureJobId` (correct)
- Browser proof with Playwright (correct)

One minor gap: the test plan does not explicitly call out testing the **negative case where `_firstHopAffordance` is present but `capturable === false`**. The memo assumes the only states are "present and capturable" or "absent." In practice, `derive_first_hop_affordance` currently only returns `capturable=True` or `None`, so `capturable=false` can't happen today. But the test should still assert that `capturable === false` suppresses controls, because the contract says "show only when capturable is true," not "show when affordance is present." A future analyzer change could emit `capturable=false` for some payloads.

This is a test quality concern, not a scope concern.

### Finding 8: The `context_title` Format Change Is a Silent UX Improvement (Informational)

Severity: Informational

Current SynthesisRenderer: `context_title: 'Synthesis > ${title}'`
Proposed: `context_title: "<_captureViewName>: <section title>"`

This changes the capture breadcrumb from a hard-coded "Synthesis" label to the analyzer-threaded view name. That's correct - it makes the breadcrumb truthful by derivation rather than host assumption. But it's also a visible UX change on existing genealogy captures. The memo doesn't call this out as a behavior change. It's a minor point, but the completion memo should note it.

## Summary Assessment

### What This Slice Would Prove

- The analyzer-owned generic first-hop contract works on one non-AOI current V2 surface
- A genealogy renderer can gate capture on analyzer truth rather than host-local assumptions
- `source_workflow_key` emission works on the genealogy line
- The first-hop contract is not AOI-coupled

### What This Slice Would NOT Prove

- Generic custom-renderer contract law (still requires extraction after this second data point)
- Non-AOI read-side status surfacing (separate later slice)
- Per-item genealogy identity semantics (entity_id is run-level only)
- IdeaEvolutionRenderer alignment (separate later slice)
- Multi-host generality (still one host)

### Is This Genuinely the Right Next Step?

Yes. The reasoning is:

1. The AOI current-consumer line is closed enough (pure + mixed surfaces)
2. The next honest variable to change is workflow family (AOI -> non-AOI)
3. `genealogy_portrait` / SynthesisRenderer is the smallest non-AOI current V2 surface
4. The analyzer contract is already complete; the gap is host consumption
5. This creates the second data point needed for future generic law extraction

No alternative next move is more honest or more strategically productive at this point.

### Concrete Recommendations

1. Add one sentence in the scope noting that this slice is the prerequisite for generic custom-renderer law extraction (the strategic payoff).
2. Note in assumptions that `entity_id` will be shared across sections of the same run, and future read-side disambiguation is a separate question.
3. Add one negative test case for `capturable === false` (defensive, even though current analyzer doesn't emit it).
4. Note the `context_title` format change as a minor visible behavior change.
