# Critique: Phase E First-Hop Affordance Routing Addendum V1 Scope

Reviewer: Claude (Opus 4.6, fresh session)
Date: 2026-04-02
Subject Memo: `communications/MEMO_2026-04-02_phase_e_first_hop_affordance_routing_addendum_v1_scope.md`

---

## 1. Verdict

**Approve with corrections.**

The sequencing is right: after bridge-hint consolidation landed, this is the correct next analyzer-side slice. The strategic framing is disciplined. The scope boundaries are well-drawn. But the memo has one serious conceptual weakness and two mechanical gaps that should be fixed before implementation starts.

The serious weakness: the proposed v1 field family (`capturable`, `commentable`, `allowed_destinations`) will produce **trivially uniform values** across all proved analytical leaf surfaces. Every AOI and genealogy leaf view on the current transient compose line would get `{capturable: true, commentable: true, allowed_destinations: ["arsenal", "research_todo"]}`. That means v1 adds metadata with zero discriminating information content. The memo needs to be honest about this: v1 is valuable for establishing the **attachment seam and ownership boundary**, not for producing semantically interesting annotations. If that is the real claim, it should be stated that way.

---

## 2. Strongest Parts Of The Memo

### A. The sequencing argument is code-backed and correct

The memo correctly identifies this as the next step after the completed three-step near-term sequence:

1. composition metadata extraction (landed)
2. bridge-hint consolidation (landed)
3. bounded first-hop affordance/routing addendum ← THIS

Both prior reviews (Claude and Codex on the bridge-hint scope) agreed this was the right follow-on. The bridge-hint consolidation completion memo explicitly named this step. The Close Read operations/routing inventory already provided the evidence base. The ordering is sound.

### B. The scope boundaries are disciplined

The out-of-scope list is strong:

- job-backed page/manifest affordance propagation
- destination-internal lifecycle
- research queue / lookup / refresh
- outline upgrade / extract lifecycle
- findings-specific Arsenal promotion
- research-answer specific routing
- premise-scrutiny / logic-gap affordances
- NotebookLM or Book Modeler routing
- host UX changes

That is the right list. The memo resists absorbing destination lifecycle, host UX, and output-specific operation families. Each of those is a later question that should be addressed separately.

### C. The ownership split is correctly framed

The memo's strongest conceptual contribution is the ownership split:

- **analyzer-v2** annotates semantic affordances and destination eligibility
- **hosts** operationalize the actual UX and post-click behavior

This is exactly right and aligns with the distilled strategic roadmap's core thesis: analyzer-v2 is the brain, hosts are thin. The affordance/routing layer is the first step toward making that thesis concrete beyond composition and rendering.

### D. The "what comes after" framing is honest

The memo correctly identifies two candidate follow-on paths:

1. broaden to one output-specific operation family
2. propagate the same hints onto job-backed surfaces

And correctly defers:

- destination lifecycle
- pretending Close Read is now fully scoped
- reopening composition-authority cleanup

The prioritization discipline is sound.

---

## 3. Weakest Assumptions

### A. The v1 values will be trivially uniform — the memo does not acknowledge this

This is the most important gap.

Looking at the current proved transient compose surfaces:

| Surface | Engine family | Would get `capturable` | Would get `commentable` | Would get `allowed_destinations` |
|---------|--------------|------------------------|------------------------|-------------------------------|
| AOI source_selection leaf views | `aoi_thematic_synthesis`, `aoi_engagement_mapping`, `aoi_sin_findings`, `aoi_thematic_report` | `true` | `true` | `["arsenal", "research_todo"]` |
| AOI source_profile leaf views | same | `true` | `true` | `["arsenal", "research_todo"]` |
| Genealogy direct_sections leaf views | `genealogy_relationship_classification`, `genealogy_final_synthesis` | `true` | `true` | `["arsenal", "research_todo"]` |
| All parent/container views | n/a | unannotated | unannotated | unannotated |

Every single proved analytical leaf view gets identical hints. The only variation is binary: leaf vs container.

From the Critic runtime evidence:

- `CaptureContext.tsx:17-35`: `CaptureSelection` accepts `source_type: 'genealogy' | 'research' | 'analysis'` — all analytical surfaces are capturable
- `CaptureActionBar.tsx:50-66`: Arsenal and Research buttons appear for ALL active selections
- `ResearchCard.tsx:149-164`: Research answers also route to Arsenal and Research Todo through the same capture system

So the host already knows all analytical surfaces are capturable and commentable with the same two destinations. The analyzer annotation adds no new discriminating signal in v1.

**Why this matters**: If the honest claim is "we're establishing the attachment seam," the memo should say so explicitly. If the claim is "we're adding semantically informative annotations," that claim is false for v1. The distinction matters for what the acceptance bar should actually test.

### B. `commentable` is ambiguous across current surfaces

"Commentable" means different things on different Critic surfaces:

- **Findings**: `CommentModal` with `selectedText`, `textField`, `commentText`, QA state persistence via `POST /api/annotations` (`FindingsPage.addComment`)
- **Research answers**: `ResearchCommentPopup` with `quoted_text`, `text_prefix`, `text_suffix`, persisted via `POST /api/research-comments` (`ResearchCard.handleCommentSave`)
- **Genealogy/AOI rendered views**: No comment system evidenced on the transient compose line itself; comments exist only when those views are rendered inside Findings or Research contexts

So `commentable: true` on a transient compose view would be asserting commentability that is actually an artifact of the host rendering context, not of the analytical output itself. The analyzer doesn't actually know whether the host will render this view inside a comment-capable container.

**Correction needed**: Either scope `commentable` out of v1 entirely (start with just `capturable` + `allowed_destinations`), or be explicit that `commentable` is a semantic hypothesis the analyzer emits about the output's suitability for annotation, not a guarantee that the host supports it.

### C. The memo does not specify how all three compose entry points populate the hints

The scope says the attachment surface is `TransientIntentView` inside `ComposeFromIntentResponse.presentation.views`. But three distinct compose functions produce that response:

1. `compose_from_intent` (line 234) — direct sections
2. `compose_from_source` (line 244) — AOI source bridge
3. `compose_from_selection` (line 292) — explicit planner selection

All three converge through `_compose_handoff_sections` and then `_to_transient_view` (line 1369). The hint population would need to happen either:

- In `_to_transient_view` (the conversion point from `ViewPayload` to `TransientIntentView`)
- Earlier, during `_match_section_to_planner_row` or `_build_transient_presentation`
- Or in the bridge layers before compose

The memo should specify which path. The cleanest option is `_to_transient_view`, since it is the single conversion point shared by all three compose paths. But the memo says nothing about this.

---

## 4. Code-Backed Findings

### Finding 1: `TransientIntentView` is the right model, and `_to_transient_view` is the right attachment point

`src/presenter/compose_from_intent.py:1369-1385`:
```python
def _to_transient_view(payload: ViewPayload) -> TransientIntentView:
    return TransientIntentView(
        view_key=payload.view_key,
        ...
        children=[_to_transient_view(child) for child in payload.children],
    )
```

This is the single function that converts `ViewPayload` into `TransientIntentView` for all three compose paths. Adding an optional affordance field to `TransientIntentView` and populating it here is the minimal, non-disruptive approach.

The `TransientIntentView` schema (`src/presenter/schemas.py:689-705`) currently has 13 fields plus `children`. Adding one optional field is backward-compatible: existing consumers that don't read it won't break.

### Finding 2: No existing affordance/routing fields exist anywhere on the transient compose line

A codebase search for `capturable`, `commentable`, and `allowed_destinations` across `src/` finds zero hits related to this concept (only unrelated uses of "affordance" in engine names and style definitions). This confirms the memo is proposing a genuinely new annotation layer, not consolidating existing scattered hints.

### Finding 3: The Critic's capture system is generic across ALL analytical surfaces

`CaptureContext.tsx:14`: `CaptureSourceType = 'genealogy' | 'research' | 'analysis'`
`CaptureContext.tsx:37`: `CaptureIntent = 'arsenal' | 'research_todo'`
`CaptureActionBar.tsx:50-66`: Both Arsenal and Research buttons appear for every active selection.

The capture system does not differentiate by engine type, output family, or semantic role. It is uniformly available on any rendered analytical surface. This confirms that v1 affordance hints will be uniform.

### Finding 4: The inventory's first-hop matrix actually shows THREE runtime-real destinations, not two

From `APPENDIX_2026-04-01_close_read_operations_and_routing_inventory_matrix.md`:

1. `arsenal` — via `CaptureContext.submitCapture('arsenal')`
2. `research_todo` — via `CaptureContext.submitCapture('research_todo')` and `ResearchFlagDialog`
3. `outline_talking_point` — via `FindingsPage.handleAddToOutline` → `POST /api/outline/talking-points`

The scope memo correctly defers outline talking-point routing. But it should note that the bounded `allowed_destinations: ["arsenal", "research_todo"]` is a deliberate subset of runtime-real destinations, not the exhaustive set. This matters for the honest claim.

### Finding 5: The genealogy bridge already derives role hints from capability metadata post-consolidation

`src/orchestrator/genealogy_saved_result_bridge.py:184-191`:
```python
def _resolve_section_role_hint(engine_registry: Any, engine_key: str) -> str:
    try:
        return resolve_composition_role(engine_registry, engine_key)
    except CapabilityMetadataResolutionError as exc:
        raise GenealogySavedResultBridgeError(...)
```

The bridge-hint consolidation is fully landed. The bridge now uses canonical capability metadata. This confirms the prerequisite for this slice is met.

### Finding 6: `ViewPayload` (job-backed) carries more metadata than `TransientIntentView` (transient)

Comparing the two models:

- `ViewPayload` (`schemas.py:191-254`): 30+ fields including `selection_priority`, `navigation_state`, `structuring_policy`, `semantic_scaffold_type`, `scaffold_hosting_mode`, `derivation_kind`
- `TransientIntentView` (`schemas.py:689-705`): 13 fields, deliberately thin

The transient model is intentionally smaller. Adding an affordance field here is consistent with the model's philosophy: carry only what the consumer needs for immediate rendering.

---

## 5. Strategic Implications For The Roadmap

### A. This slice establishes the attachment seam, not the semantic vocabulary

The real strategic value of this slice is not the three boolean/list fields. It is:

1. Proving that `TransientIntentView` can carry optional analyzer-owned metadata beyond composition/rendering
2. Establishing the derivation path: analyzer logic → structured annotation → host consumption
3. Creating the extension point for later non-uniform annotations (output-specific affordances)

The roadmap should treat this slice as "seam establishment" rather than "affordance coverage."

### B. The next follow-on should produce non-uniform annotations

If v1 produces uniform `{capturable: true, commentable: true, allowed_destinations: ["arsenal", "research_todo"]}` for all leaf views, then the first follow-on must produce annotations that actually VARY:

- Different engines or output families having different allowed destinations
- Some views being `capturable: false` (metadata-only container views, or structural views)
- Output-specific affordances like `promotable_to_arsenal` or `supports_premise_scrutiny`

Without that follow-on, the affordance layer remains a dead letter.

### C. The Close Read inventory remains the evidence base, not the specification

The scope memo correctly draws from the inventory's first-hop evidence without claiming the inventory is an analyzer-side contract. That relationship is right and should be preserved: the inventory tells us what's runtime-real in current hosts; the analyzer annotation tells hosts what the analyzer considers structurally supportable.

### D. Propagation to job-backed surfaces is the correct follow-on, not a v1 concern

The memo correctly defers job-backed `PagePresentation` and `EffectivePresentationManifest` propagation. Those surfaces have different lifecycle, caching, and validation constraints. Keeping v1 on transient-only is the right boundary.

---

## 6. Concrete Corrections Or Reframing

### Correction 1: Acknowledge that v1 values will be trivially uniform

Add a section to the memo that states:

> For the current proved engine family, all analytical leaf views on the transient compose line will receive the same affordance hints. The primary value of this slice is establishing the attachment seam and ownership boundary, not producing semantically discriminating annotations. The first follow-on should extend the vocabulary to produce non-uniform values.

This prevents the completion memo from overclaiming.

### Correction 2: Drop or reframe `commentable` from the v1 field family

`commentable` is host-context-dependent, not analyzer-output-dependent. Whether a rendered view supports comments depends on whether the host renders it inside a comment-capable container (`FindingsPage` vs `ResearchCard` vs a standalone transient view).

Two options:

a. **Drop it**: Start with only `capturable` and `allowed_destinations`. Add `commentable` when the analyzer can actually distinguish commentable from non-commentable outputs.

b. **Reframe it**: Rename to `annotation_eligible` or keep `commentable` but document that it means "this output's structure is suitable for host-side annotation" rather than "the host will definitely render comments." The analyzer is asserting structural suitability, not host capability.

Option (a) is smaller and more honest. The memo claims to want the "smallest honest starting set" — `commentable` does not meet that bar if its value is uniformly `true` and its semantics are ambiguous.

### Correction 3: Specify the population path through `_to_transient_view`

Add to the design section:

> The hint population should happen in `_to_transient_view` (`compose_from_intent.py:1369`), which is the single conversion point from `ViewPayload` to `TransientIntentView` shared by all three compose entry points. This keeps the derivation in one place and avoids duplicating logic across `compose_from_intent`, `compose_from_source`, and `compose_from_selection`.

The derivation logic itself can live in a small helper (e.g., `_derive_first_hop_affordance(engine_key, is_leaf)`) that checks whether the view is an analytical leaf and returns the bounded hints or `None`.

### Correction 4: Note that `allowed_destinations` is a deliberate subset, not the full set

The inventory shows three runtime-real first-hop destinations: `arsenal`, `research_todo`, and `outline_talking_point`. The memo bounds to two. That's a valid scope decision but should be stated as deliberate subsetting, not as if only two destinations are real.

Add:

> The bounded `allowed_destinations` set (`arsenal`, `research_todo`) is a deliberate v1 subset. The inventory also evidences `outline_talking_point` as a runtime-real first-hop destination, deferred from this slice because it routes through findings comments and involves a different host-local interaction model.

### Correction 5: Address non-proved transient compose surfaces

The memo says hints should stay on "the currently proved transient compose line only" — AOI source_selection, AOI source_profile, genealogy direct_sections. But `compose_from_intent` can also handle non-AOI, non-genealogy workflows (the `_HANDOFF_KIND_DIRECT_SECTIONS` path is generic).

What should happen when a non-proved workflow passes through `compose_from_intent`? Options:

a. All leaf views on any transient compose path get the same hints (simplest)
b. Only views from the migrated engine family get hints (most honest)

The memo should state which. Option (b) is more disciplined and avoids overclaiming for workflows the system hasn't proved yet.

---

## Bottom Line

Approve the memo after the five corrections above. The sequencing is right, the scope boundaries are disciplined, and the ownership framing is the strongest part. The main weakness is that the memo presents v1 as a semantic annotation when it is really a seam-establishment exercise — the values will be trivially uniform across all proved surfaces. Being honest about this changes nothing about the execution plan but changes the honest claim and acceptance bar significantly. Drop `commentable` from v1 to reach the true smallest starting set, specify the `_to_transient_view` population path, and acknowledge the uniform-value reality.

This is the most defensible immediate next analyzer-side code move after bridge-hint consolidation.

**Verification Note**

This was a docs-and-code audit tranche. No tests were run.
