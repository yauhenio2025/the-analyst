# Critique: Stage 12 / Cross-Workflow Renderer Law Generalization Scope (Round 2)

Reviewer: Claude Opus 4.6
Date: 2026-03-24
Round: 2 (post-revision)
Target: `communications/MEMO_2026-03-24_stage12_cross_workflow_renderer_law_generalization_scope.md`

## Verdict: Approve

The revised memo addresses all five findings from the first review pass. The revisions are substantive, not cosmetic — they add concrete mechanism specifications, acknowledge real risks, and tighten the proof bar. The memo is now specific enough to be implementable by independent sessions.

---

## Resolution of Round 1 findings

### Finding 1 (was HIGH): served-contract policy concreteness — RESOLVED

Decision 2 now specifies:

- a concrete function signature: `resolve_served_renderer_contract_policy(*, workflow_key, consumer_key, route_kind, composition_mode, is_transient) -> ServedRendererContractPolicy`
- a return shape: `mode: strict | shadow | warn` plus `coverage_key` and `reason`
- an explicit initial decision matrix covering transient routes, AOI bounded-contract surfaces, genealogy composition modes, and default/restore surfaces

This is concrete enough that two independent implementors would produce compatible decisions. The `shadow` mode is a smart addition — it enables safe cutover without pretending warn-only surfaces are strict-ready.

### Finding 2 (was HIGH): genealogy data shape violation risk — RESOLVED

New Decision 3 carries an explicit 4-step cutover strategy:

1. introduce the served-policy layer for all relevant paths
2. run genealogy in `shadow` mode
3. fix or narrow the mode set until at least one non-AOI surface can go `strict`
4. widen strict coverage mode by mode

The "what is not yet real" section (line 121-122) now explicitly calls out "no serve-time sub-renderer law yet" and "genealogy normalization and warn-mode handling that show pre-existing shape-risk on job-backed surfaces." This is honest about the state of the world.

### Finding 3 (was MEDIUM): serve-time sub-renderer law gap — RESOLVED

Decision 5 is retitled "make serve-time sub-renderer law a new final-boundary build, not a wiring exercise" and now plainly states: "Serve-time sub-renderer law does not really exist today." It reframes the work as building new serve-time validation that reuses design-time helpers (`runtime_override_validator.py`, `view_contract_validator.py`) as templates. This is the correct framing.

### Finding 4 (was MEDIUM): tab vs accordion container model — RESOLVED

New Decision 6 explicitly separates the two container models:

- accordion and nested-sections → section/sub-renderer law
- tab parents → child-container law over synthetic container data, child payload legality, and payload-tree integrity

It cites `tab.json`'s `available_section_renderers: []` as the structural reason. This prevents the implementation from forcing tab containers through a section-renderer validation model that doesn't fit.

### Finding 5 (was MEDIUM): non-AOI fail-closed proof — RESOLVED

Decision 11 proof item 3 now requires "one real fail-closed case from a previously warn-only non-AOI surface." New item 5 adds: "if some genealogy surfaces remain in shadow, explicit proof of that policy state rather than pretending universal strict cutover." This prevents another AOI-heavy proof pass and keeps the genealogy cutover honest.

---

## Remaining observations (none blocking)

### Observation A (LOW): shadow-mode violation recording is unspecified

The `shadow` mode is well-designed for safe cutover, but the memo does not specify where shadow-mode violations get recorded — in trace artifacts, in logs, in a new shadow-mode report, or in the served response itself. This is a narrow implementation detail that can be resolved during the implementation session. Not blocking.

### Observation B (LOW): "historically normalization-heavy" is soft

The initial decision matrix says: "default authored or restore surfaces that are still historically normalization-heavy -> `warn` unless explicitly promoted." What counts as "historically normalization-heavy" is somewhat subjective. In practice, the `_normalize_view_structured_data` function in `presentation_api.py` and its per-view-key branches are the operational definition — an implementor can use the presence of per-view normalization code as the test. Not blocking, but worth noting.

### Observation C (LOW): the memo now has 11 decisions

The expansion from 9 to 11 decisions is justified by the added specificity. Each decision is well-bounded and serves a clear purpose. The numbering is clean and non-overlapping. No issue.

---

## What the revised memo gets right

- The served-policy layer is now concrete enough to implement: function signature, return shape, and initial decision matrix
- The `shadow` mode enables safe genealogy cutover without binary strict/warn
- The sub-renderer law gap is now honestly framed as a new build
- The tab/accordion structural distinction is explicit
- The proof bar now prevents AOI-heavy evidence inflation
- The scope boundaries (no Stage 11 grouping, no Stage 13 host contract, no new renderers) remain clean
- The sequencing argument (Stage 12 before 13) remains well-supported by code evidence
- The bounded claim is honest about what Stage 12 does and does not prove
- Decision 4's addendum about job-backed law not being fully symmetric with transient semantics is good honest scoping

---

## No additional relevant documents found

I did not find any recent documents in `communications/` or `docs/` beyond the standard corpus that materially bear on the revised Stage 12 scope. The same set of stage completion memos, proof artifacts, and roadmap documents from the first review remain the relevant context.

---

## Summary

The revised memo is approved for implementation. All five Round 1 findings are substantively resolved. The remaining observations are implementation-level details, not scope-level gaps.
