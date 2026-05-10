# Critique: Stage 5 AOI Source-Content Identity Revision Scope

Date: 2026-03-26
Reviewer: Claude (Opus 4.6)
Document reviewed: `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_scope.md`

## Verdict: Approve after revision

The memo correctly identifies the next honest step, correctly keeps the scope bounded, and correctly keeps the roadmap honest. However, it underspecifies the primary contamination source that the codebase already reveals, which risks a wider diagnostic sweep than necessary.

---

## Findings

### Finding 1 (High): The primary contamination source is already identifiable from the codebase — the memo should name it

The memo lists four "potential repair loci" (Decision 5) without prioritizing. But the codebase evidence already narrows the root cause to a single definitive entry point:

**`src/engines/capability_definitions/aoi_thematic_synthesis.yaml:92-94`** hardcodes:

```yaml
output_contract:
  selected_source_thinker:
    thinker_id: "john_oneill"
    thinker_name: "John O'Neill"
```

This output_contract is injected verbatim into the LLM prompt by `src/stages/capability_composer.py:343-347`:

```python
if getattr(cap_def, "output_contract", None):
    lines.extend([
        "**JSON contract**:",
        "```json",
        json.dumps(cap_def.output_contract, indent=2),
        "```",
    ])
```

When the LLM generates the Phase 1.0 thematic synthesis output for any thinker, it sees `john_oneill` / `John O'Neill` as the example `selected_source_thinker` and echoes it in the raw output. The proof confirms this: the `final_output_preview` for the Otto Neurath run (`PROOF_stage5_aoi_execution_backed_browser_closeout_rerun_requests_2026-03-26.json`, around line 5706) shows:

```json
"final_output_preview": "...\"selected_source_thinker\": {\"thinker_id\": \"john_oneill\", \"thinker_name\": \"John O'Neill\"}..."
```

**Why this matters for the memo**: The memo should explicitly name this capability-definition example contamination as the primary suspect rather than treating all four loci as equally likely. A diagnosis slice that doesn't start here risks wasting time on secondary effects.

**Recommended revision**: Add a "Primary Suspect" subsection to Decision 3 or Decision 5 that names `aoi_thematic_synthesis.yaml` output_contract as the first inspection target, with the capability_composer injection path as the contamination mechanism.

### Finding 2 (Medium): The normalization layer already partially defends — the memo should acknowledge this

`src/aoi/contract.py:97` already overrides `selected_source_thinker` in the normalized metadata from plan context:

```python
return {
    ...
    "selected_source_thinker": plan_context["selected_source_thinker"],
    "normalized": normalized,
    ...
}
```

This means the structured artifacts persisted via `analysis_products/store.py` (the `aoi.source_thematic_map`, `aoi.engagement_map`, `aoi.findings_bank` families) already carry the correct thinker identity at the top-level metadata wrapper.

The contamination that survives lives in two specific places:

1. **`final_output_preview`** — stored by `src/executor/workflow_runner.py:535` as `result.final_output[:500]`. This is the raw LLM output, not the normalized output. The normalization in `contract.py` only runs on the metadata attached to the persisted output, not on the preview string stored in the phase result.

2. **Report prose** — if the Phase 4.0 thematic report engine output also references "John O'Neill" in its narrative body (which is likely given the upstream contamination), that text becomes part of the `thematic_report` normalized payload's `report_sections` content, which flows through `composition_source_bridge.py` into compose surfaces.

The memo should distinguish these two contamination survival paths explicitly. The `final_output_preview` is a display artifact that can be suppressed or regenerated without re-execution. Report prose contamination may or may not be recoverable in place.

### Finding 3 (Medium): The recovered-run rehabilitation question (Decision 7) has a plausible answer the memo should foreshadow

Given Finding 2 above:

- The **structured normalized artifacts** (`aoi.source_thematic_map`, etc.) should already carry correct identity from `contract.py`'s plan-context override.
- The **`final_output_preview`** contamination is a display-layer issue that can be corrected without re-execution (either by suppressing the preview, regenerating it from normalized data, or stripping the example-contaminated identity fields).
- The **report prose** contamination is the open question. If the Phase 4.0 report merely mentions John O'Neill as an intermediary interpreter of Neurath (which is historically accurate — John O'Neill did write extensively on Neurath), that could fall under "analytically acceptable mention" (Decision 4). If the report explicitly attributes selected-source authority to John O'Neill, that is a hard identity contradiction that cannot be repaired without re-execution.

The memo should foreshadow these three tiers so the implementor knows where to check first and what threshold determines "rehabilitation in place" vs. "fresh rerun required."

### Finding 4 (Low): The capability definition snapshot also carries the contamination

`src/engines/capability_history/aoi_thematic_synthesis_snapshot.json:131-134` carries the same `john_oneill` identity. If the repair changes the YAML definition, the snapshot should be regenerated too, or at least noted in the closeout as needing update. The memo's "Code Areas To Inspect First" section does not mention the capability_history directory.

### Finding 5 (Low): Decision 4's distinction is well-framed but needs one operational clarification

The memo correctly distinguishes between hard identity contradiction and analytically acceptable mention. However, John O'Neill (the philosopher) genuinely is a major secondary interpreter of Otto Neurath's work. So the report prose may legitimately reference O'Neill as an intellectual intermediary between Neurath and Benanav — and that would be analytically correct, not contamination.

The operational clarification needed: the implementor must distinguish between:
- `selected_source_thinker = john_oneill` appearing in **explicit identity fields** (hard contradiction)
- "John O'Neill" appearing in **report narrative prose** as a referenced interpreter (potentially acceptable)
- "John O'Neill's reconstruction of Otto Neurath" framing the entire analysis (ambiguous — could be contamination from the example, could be legitimate analytical framing)

The memo gestures at this but should make the decision rule concrete: **only explicit identity field contamination requires repair; prose references require judgment per finding.**

### Finding 6 (Informational): The test suite already uses `john_oneill` as a fixture identity

`tests/test_aoi_contract.py` (lines 39-65) and `src/aoi/fixture_profiles.py:66-68` use `john_oneill` / `John O'Neill` as the fixture profile identity. This is correct and expected — the Benanav/O'Neill analysis is a legitimate AOI case. The tests are not contamination sources; they are separate fixture-backed test paths. The repair should not break these tests.

---

## Direct Answers to Prompt Questions

### 1. Is the memo right that the next honest move is analyzer-side/source-content diagnosis?

**Yes.** The browser proof passed structurally. The host identity chain now works. The remaining blocker is definitively source-content level: the LLM's raw output carries example-contaminated identity from the capability definition. This is analyzer-v2 code, not host/browser code.

### 2. Is keeping `job-6ee8b0621177` as the fixed diagnosis source honest?

**Yes.** The run completed successfully with correct plan context (`selected_source_thinker_id = otto_neurath`). The contamination entered through the capability definition example, not through incorrect plan data. Diagnosing against this fixed source is the most honest approach because it isolates the capability-definition contamination path from any plan-data issues.

### 3. Does the memo distinguish clearly enough between hard contradiction, acceptable mention, and preview leakage?

**Mostly yes, but needs operational clarity.** Decision 4 frames the categories correctly. What's missing is a concrete decision rule: which fields are "explicit identity" (hard contradiction) vs. "narrative context" (judgment call). The implementor needs to know that `selected_source_thinker` in JSON metadata is hard identity, while "O'Neill" in report prose text is judgment territory.

### 4. Are the proposed seam families technically plausible?

**Yes, all four are plausible**, but they are not equally likely:

- **Capability-definition sample contamination**: This is the confirmed primary cause. The `output_contract` in `aoi_thematic_synthesis.yaml` hardcodes `john_oneill` and the capability_composer injects it into the prompt verbatim.
- **AOI normalization not defending against contradictory explicit identity**: Partially true — `contract.py:97` does override at the metadata wrapper level, but the raw LLM output inside `normalized.themes[*].source_documents[*]` etc. may still echo the example identity in sub-fields that aren't overridden.
- **Raw phase preview persistence**: Confirmed — `workflow_runner.py:535` stores raw output as `final_output_preview`, which carries the LLM's contaminated identity.
- **Result/presentation guardrails**: Plausible for the thematic report prose path, but this depends on whether the report engine also picks up the example contamination (likely, since upstream Phase 1.0 output is in its context).

### 5. Is the memo too broad or too narrow about likely repair loci?

**Slightly too broad.** The memo treats four loci as equally likely when the codebase evidence already points to the capability-definition example as the primary cause. This risks a wider diagnostic sweep than necessary. The repair should start at the YAML definition, trace through the prompt-injection path, and then check downstream contamination survival — in that order, not in parallel.

### 6. Does the memo keep the roadmap honest?

**Yes.** The memo correctly states:
- Browser proof passed structurally (accurate — proved by the rerun completion memo and proof artifacts)
- Stage 2 still open (accurate — content integrity is unresolved)
- Tranche 3 still blocked (accurate — depends on Stage 2)
- This slice does not close Stage 2 by itself (accurate)

### 7. Does the memo force an explicit answer on rehabilitation vs. fresh rerun?

**Yes, through Decision 7.** The closeout is required to answer separately whether the recovered run can be trusted in place or whether a fresh rerun is necessary. This is well-designed. The Finding 3 above gives the implementor a head start: structured artifacts likely survive, previews can be corrected in place, report prose is the open question.

---

## Recommended Revisions Before Implementation

1. **Name the primary suspect explicitly.** Add to Decision 3 or Decision 5: "The first inspection target should be `src/engines/capability_definitions/aoi_thematic_synthesis.yaml` output_contract (lines 92-94), which hardcodes `john_oneill` / `John O'Neill` as the example selected_source_thinker. The prompt injection path through `src/stages/capability_composer.py:343-347` feeds this example to the LLM verbatim."

2. **Acknowledge the existing normalization defense.** Note that `src/aoi/contract.py:97` already overrides `selected_source_thinker` from plan context in normalized metadata. The contamination that survives is: (a) raw `final_output_preview` in `workflow_runner.py:535`, and (b) potentially report prose. This narrows the repair surface.

3. **Add the capability_history directory to "Code Areas To Inspect."** `src/engines/capability_history/aoi_thematic_synthesis_snapshot.json:131-134` also carries the example contamination and should be updated if the YAML definition changes.

4. **Sharpen Decision 4 with an operational rule.** Specify that contamination is measured by: explicit identity fields (`selected_source_thinker`, `thinker_id`, `thinker_name` in JSON metadata) must match plan context. Prose references to real intellectual relationships are judgment calls, not automatic contamination.

5. **Foreshadow the three contamination tiers.** In Decision 7, hint that structured artifacts, previews, and report prose represent three distinct rehabilitation questions with different difficulty levels, so the implementor knows what order to check.

---

## Summary Assessment

The memo is substantively sound. It correctly identifies that the work has moved from host/browser territory to analyzer-side source-content integrity. The scope boundaries are tight and the stop-and-revise rules are well-calibrated. The main weakness is underspecification of the already-identifiable primary contamination source, which could lead to unnecessary diagnostic breadth. With the five revisions above, the memo becomes a clean bounded implementation scope.

The program sequencing is honest: Stage 2 remains open, Tranche 3 remains blocked, and this slice exists to diagnose and repair a specific content-integrity seam rather than to claim closure.
