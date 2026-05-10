# Critique: Phase E Genealogy V2 Idea Evolution First-Hop Affordance Eligibility V1 Scope

Date: 2026-04-03
Reviewer: Claude (Opus 4.6)

Scope Under Review:
- `communications/MEMO_2026-04-03_phase_e_genealogy_v2_idea_evolution_first_hop_affordance_eligibility_v1_scope.md`

## Verdict

**Approve with corrections.**

The memo correctly identifies the blocker that the prior rejected host-only scope missed, and proposes a defensible sequencing fix. The core claim — that analyzer-side eligibility must precede host-side helper adoption — is code-backed and honest. But several implementation details need tightening and one structural question is left underdeveloped.

## Strongest Parts

### 1. The blocker diagnosis is accurate and code-backed

The memo's central claim holds:

- `currentRendererCapture.ts:45` hard-gates on `firstHopAffordance?.capturable !== true` → returns `null`
- `V2TabContent.tsx:597` threads `payload.first_hop_affordance ?? null` without invention
- `first_hop_affordance.py:43-47` only returns a `FirstHopAffordance` when `engine_key in MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS` and no children
- `MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS` (lines 20-36) lists six engine families; `concept_synthesis` is not among them
- `genealogy_idea_evolution.json:18` declares `engine_key = "concept_synthesis"`

So the helper adoption would indeed suppress all capture buttons on this surface. The memo is right that this must be fixed first.

### 2. The refusal to globally bless `concept_synthesis` is the right instinct

The memo explicitly says (Section 2): do not solve this by adding `concept_synthesis` to `MIGRATED_COMPOSITION_ENGINE_FAMILY_KEYS`. This is defensible because:

- `concept_synthesis` appears in multiple chains (e.g., `concept_analysis_12_phase.json`, `genealogy_synthesis_chain.json`) and could surface in future views with different semantics
- The current evidence is about one specific live view on one workflow
- A global blessing would make every future `concept_synthesis` leaf capturable by default, which is a stronger claim than the evidence supports

### 3. The three-part allow condition is appropriately narrow

Requiring all of `workflow_key == "intellectual_genealogy"`, `view_key == "genealogy_idea_evolution"`, `engine_key == "concept_synthesis"`, and `children == []` is a genuinely tight gate. It prevents accidental leakage into future `concept_synthesis` usages on other workflows.

### 4. The "both presenter paths should inherit the same rule" point is correct

Because `derive_first_hop_affordance(...)` is the shared entry point consumed by both:
- `attach_first_hop_affordances(...)` on the job-backed page path (`presentation_api.py:837`)
- `_derive_first_hop_affordance(...)` on the transient compose path (`compose_from_intent.py:1412-1420`)

A change inside `derive_first_hop_affordance` or `is_migrated_analytical_leaf_payload` naturally flows through both paths. The memo is right that this is about contract honesty, not host specificity.

### 5. The "not" list is accurate and comprehensive

No host change, no `entity_id`, no `specialized_family`, no backend. This is the correct scope boundary.

## Weakest Assumptions / Overclaims

### 1. The implementation shape is underspecified — where exactly does the new rule go?

The memo says "add one bounded eligibility seam in `first_hop_affordance.py`" (Section 1) but does not say whether it goes:

(a) Inside `is_migrated_analytical_leaf_payload()` as a second OR clause
(b) Inside `derive_first_hop_affordance()` as a second eligibility branch
(c) As a new function checked alongside the existing `is_migrated_analytical_leaf_payload` guard

This matters because:

- Option (a) would make the view-specific rule look like a migrated-engine-family assertion — semantically dishonest
- Option (b) is the most natural place — a separate `elif` that short-circuits for this one view
- Option (c) is cleaner but adds more surface area

The memo should specify option (b) or (c) and rule out (a) explicitly, to prevent the implementor from accidentally creating the global blessing the memo says to avoid.

### 2. The view-key check requires `payload.view_key` but the function signature only has `payload: ViewPayload`

`derive_first_hop_affordance` currently reads `payload.engine_key` and `payload.children`. The memo proposes also checking `payload.view_key`. That field exists on `ViewPayload` (confirmed by the schema), so this is feasible. But the memo should acknowledge that this adds a view-key coupling to what was previously an engine-only eligibility check. That is a deliberate design choice, and the right one, but it should be named as a new dimension rather than treated as trivially equivalent to the existing check.

### 3. The memo does not say whether the transient compose path can actually surface this view today

Section 4 says "let both shared presenter paths inherit the same rule" and then says "if the view can appear on the transient compose line, add the matching transient contract test there too. If it cannot currently appear there, say so explicitly."

The answer is: it depends on the handoff kind. `compose_from_intent.py:121-126` shows that `(GENEALOGY_WORKFLOW_KEY, "direct_sections")` is eligible for first-hop affordance on the transient path. If `genealogy_idea_evolution` appears in a `direct_sections` handoff, the transient path would flow through `_derive_first_hop_affordance(...)` → `derive_first_hop_affordance(...)`, and the new rule would apply.

However, the transient first-hop eligibility is gated by **handoff kind**, not just workflow key. The job-backed path uses `attach_first_hop_affordances(...)` which only checks the workflow key. So the transient path has an additional gate that the memo does not discuss. The memo should say:

- On the job-backed path, the new rule applies if `workflow_key == "intellectual_genealogy"` (always true for this view)
- On the transient path, the new rule applies only if the handoff kind is `"direct_sections"` (which is the only genealogy-eligible handoff kind today)
- This is consistent and does not need special handling

### 4. "The memo should say more clearly whether this broadening affects only job-backed presentation or also transient compose surfaces" — per the prompt's explicit ask

This is the prompt's sharpest question, and the memo partially addresses it (Section 4) but does not resolve it. The answer is: the change naturally affects both, because both paths delegate to `derive_first_hop_affordance(...)`. The job-backed path applies it unconditionally for approved workflow keys; the transient path additionally gates on handoff kind. But the view-specific rule fires inside the shared derivation function, so the two paths will produce identical affordance decisions for identical payloads. The memo should state this explicitly.

### 5. The assumption that `genealogy_idea_evolution` is the only `concept_synthesis` view is true today but fragile

Confirmed: only `src/views/definitions/genealogy_idea_evolution.json` has `"engine_key": "concept_synthesis"`. But `concept_synthesis` appears in chains (`genealogy_synthesis_chain.json`, `concept_analysis_12_phase.json`) and could easily acquire new view definitions. The three-part check (workflow + view_key + engine_key) mitigates this, but the memo should name the mitigation strategy explicitly: "if a new `concept_synthesis` view is created, it will not receive affordance unless its view_key is also added to the eligibility rule."

## Code-Backed Findings

### Finding 1: The implementation path is clean and narrow

The change needs to touch exactly one function area in `first_hop_affordance.py`. The cleanest implementation is to add a second eligibility predicate in `derive_first_hop_affordance()`:

```python
def derive_first_hop_affordance(payload, *, enabled):
    if not enabled:
        return None
    if is_migrated_analytical_leaf_payload(payload):
        return FirstHopAffordance(...)
    if _is_idea_evolution_eligible_leaf(payload):
        return FirstHopAffordance(...)
    return None
```

Where `_is_idea_evolution_eligible_leaf` checks all four conditions (workflow can't be checked here — it's in the `enabled` flag already). Actually, looking more carefully, `derive_first_hop_affordance` receives only `payload` and `enabled`. The workflow_key check is handled upstream: `workflow_supports_first_hop_affordance("intellectual_genealogy")` is already `True` because `GENEALOGY_WORKFLOW_KEY` is in `FIRST_HOP_AFFORDANCE_ELIGIBLE_WORKFLOW_KEYS` (line 17-19).

So the workflow check is already satisfied. The new rule only needs to add a view_key + engine_key + leaf check as a second branch inside `derive_first_hop_affordance`. This is even narrower than the memo implies.

### Finding 2: The `enabled` flag already covers the workflow check

The memo says the allow condition should require `workflow_key == "intellectual_genealogy"`. But `derive_first_hop_affordance` receives `enabled: bool`, which is already `True` only for approved workflows. So the function does not need to re-check `workflow_key` — the workflow gate is upstream. The view-specific rule only needs to check `view_key`, `engine_key`, and `children`. The memo's four-part condition is effectively three parts at the implementation site.

### Finding 3: No `specialized_family` contamination risk

The specialized family logic at lines 87-96 only fires for the AOI `aoi_by_sin_type` / `aoi_sin_findings` combination. The new eligibility rule would produce a plain generic `FirstHopAffordance(capturable=True, allowed_destinations=[...])` without specialization. The specialization check is gated by `workflow_key == AOI_WORKFLOW_KEY` which is `"aoi_v2"`, never `"intellectual_genealogy"`. So there is no contamination path.

### Finding 4: The contract hash claim is accurate

Adding `first_hop_affordance` to a view payload that previously lacked it will change the manifest/contract truth (the affordance field appears where it didn't before). It will not change content hashes because `first_hop_affordance` is a presentation contract field, not content data. This is consistent with prior first-hop broadening behavior.

## Strategic Implications

### 1. This is the right sequencing fix for the rejected scope

The Codex audit rejected the prior host-only scope because it missed the upstream affordance gap. This memo is the direct, correct response: fix the upstream gap first. The program now has an honest two-step path: (1) analyzer eligibility, (2) host helper adoption.

### 2. The view-specific approach is a strategic precedent

This is the first time a view-specific (not engine-family) eligibility rule would enter `first_hop_affordance.py`. That is a deliberate design choice. It is the right one for now because the evidence is view-specific. But it sets a pattern: future one-off views may each need their own eligibility rule. The memo should acknowledge this precedent and state that the expectation is consolidation (promoting to engine-family level) once multiple views on the same engine prove eligibility.

### 3. The slice is genuinely small

This is one predicate function, one or two test files, and zero host changes. It is the smallest defensible unit of work to unblock the next host alignment slice.

### 4. Risk of the "one more tiny prerequisite" anti-pattern

The program has been through many "one more tiny prerequisite" cycles. This one is defensible because it was surfaced by code-backed review, not by scope inflation. But the memo should commit to a clear next step: once this lands, the host-only `IdeaEvolutionRenderer` alignment scope becomes immediately executable without further analyzer work.

## Concrete Corrections

1. **Specify the implementation site explicitly.** Add a new second-branch eligibility predicate in `derive_first_hop_affordance()`, not inside `is_migrated_analytical_leaf_payload()`. Name this as a view-specific eligibility check, separate from the engine-family migrated check.

2. **Acknowledge that the workflow check is already handled upstream.** `derive_first_hop_affordance` receives `enabled: bool` which is `True` only for approved workflows. The four-part condition in the memo is effectively three parts at the implementation site: `view_key + engine_key + leaf`. The memo's explicit `workflow_key == "intellectual_genealogy"` condition should clarify this is enforced by the `enabled` flag, not re-checked in the predicate.

3. **State the transient-path answer explicitly.** Both paths delegate to `derive_first_hop_affordance(...)`. The new rule applies identically on both. On the transient path, an additional handoff-kind gate exists upstream (`compose_from_intent.py:121-126`), but the view-specific rule fires inside the shared derivation function. No special handling is needed.

4. **Name the view-key coupling as a deliberate new dimension.** The existing eligibility check is engine-only. This will be the first view-key-aware check. That is correct but should be named as a design precedent, with the expectation that view-specific rules consolidate to engine-family rules once evidence supports it.

5. **Clarify the test plan's transient coverage.** The memo says to add transient compose path tests "if the view can appear there." It can, via the `(GENEALOGY_WORKFLOW_KEY, "direct_sections")` handoff. State this explicitly and include a transient compose path test.

6. **Add the consolidation expectation.** State that if a second `concept_synthesis` view proves eligibility, the two view-specific rules should be consolidated into an engine-family promotion. This prevents the "one rule per view" pattern from accumulating indefinitely.
