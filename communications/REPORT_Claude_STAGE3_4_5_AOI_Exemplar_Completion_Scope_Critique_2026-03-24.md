# Review (Pass 2): Stage 3/4/5 AOI Exemplar Completion Scope

Date: 2026-03-24
Reviewer: Claude Opus 4.6 (1M context)
Memo under review: `communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md` (revised)
Prior review: Pass 1 review against the pre-revision memo

---

## Verdict

**Approved.**

The revised memo addresses every finding from the first review. Stage 2 subsumption is now explicit. The planner-contract framing is corrected. The public compose contract lock is named as a real implementation constraint. Host residuals are named. The evaluation/readiness distinction is drawn. Planner-primary is clarified as recommended/confirmed, not blind auto-execution. Concrete task examples exist.

I have no remaining revisions that would block implementation.

I do have observations that the implementation team should keep in mind, and one open question that should be resolved early in implementation rather than deferred.

---

## Findings (Ordered by Severity)

### 1. LOW — The concrete task examples still map to the existing two profiles

The memo adds two concrete examples (lines 289-290):

> - "Show how Thinker X's concept of Y evolves across the corpus" → selects relevant AOI source/product mix
> - "Show where Thinker X most directly engages, contests, or reframes peer positions on Y" → foregrounds engagement- and findings-oriented materials

These are well-chosen and illustrate the right direction. However, the first example maps naturally to the `dossier` profile shape (thematic_synthesis + thematic_report), and the second maps naturally to the `comparison` profile shape (engagement_mapping + sin_findings + thematic_report).

The memo handles this honestly at line 292-293:

> If the resulting downstream shape is still literally one of the two current public profiles, the closeout should say so plainly. If the tranche wants a proof case beyond those two shapes, public contract widening is required.

That is the right escape clause. But the implementation team should be aware that a genuinely non-dossier/non-comparison shape would require either:
- A third profile (e.g., "overview" = synthesis + engagement, no report)
- Or the contract widening path described in Decision 5A (planner-resolved downstream compose that does not re-enter the profile enum)

The risk is that implementation lands task-first UX that is visually task-driven but structurally still resolves to one of the two existing profiles. That would be a real advance over the current profile-button UX, but the closeout should not overclaim it as Stage 4 source-selection law if the downstream contract didn't change.

**No revision needed.** The memo already handles this with the exit-note requirement at line 406.

### 2. LOW — Host-proxy identity translation is a deeper residual than it appears

The memo names host-proxy identity translation as a continuity residual (Decision 6A, lines 241-242). Code verification confirms this is real and load-bearing:

- `hostContractV1.ts:223` sets `host_local_identity_translation_before_launch: true` for the transient source-backed compose family
- `AoiV2ThematicPanel.tsx:505-512` performs snapshot warmup to resolve `analysisId` before navigation
- `AoiV2ThematicPanel.tsx:547` passes `source_analysis_id` from the host's resolved identity into the planner context

This is not a cosmetic residual. The host is performing real identity resolution (`project_id + thinker_id → analysis_id → v2_job_id`) that the planner then consumes. If the tranche makes the planner the primary authority, the question becomes: should the planner accept `v2_job_id` directly (already resolved upstream by the host's warmup step), or should the planner resolve the source identity itself from higher-level project/thinker coordinates?

The memo correctly allows this residual to remain (Decision 6A), and the exit-note requirement (line 405) will force the closeout to name it. That is sufficient for this tranche. But the implementation team should expect this to become a structural question for the de-AOI generalization tranche that follows.

**No revision needed.**

### 3. LOW — The six residuals listed are actually five plus one that is really about the host

Residuals 1-5 (lines 262-267) are about the analyzer/composition contract seam. Residual 6 ("no saved AOI exemplar eval pack") is about evaluation infrastructure. These are cleanly separated.

But there's a subtle seventh residual that the memo mentions only in the preamble (line 68) and Decision 6A (lines 241-242) but not in the numbered list:

- Host-proxy identity translation and snapshot warmup on the proof path

Since the exit-note requirement (line 405) already requires the closeout to name remaining host residuals, this is not a gap in the memo — it's just a numbering choice. Noting for completeness.

**No revision needed.**

### 4. OBSERVATION — The `compose-from-source` contract widening is the hardest implementation decision

Decision 5A (lines 204-215) is the most consequential implementation choice in the tranche. The current public contract:

```python
ComposeFromSourceProfile = Literal["dossier", "comparison"]  # schemas.py:624
```

is a hard `Literal` enum. Any third composition shape requires either:
- Extending this enum (which means all downstream composition logic must handle the new shape)
- Or adding a parallel contract (e.g., `compose-from-plan` or `compose-from-selection`) that bypasses the profile enum entirely

The memo correctly does not freeze this choice. But the implementation team should resolve this early — it gates the entire "not reducible to dossier/comparison" proof case.

**No revision needed.** This is implementation guidance, not a memo gap.

### 5. OBSERVATION — Stage 2 subsumption via the evaluation pack is elegant

Decision 1A (lines 113-122) and Deliverable 4 (lines 338-342) together create a clean path:

- Stage 2 exit evidence = documented AOI transient MVP criteria + proof of repeated use on real inputs
- Deliverable 4 = evaluation pack with rubric, task cases, and repeated bounded AOI transient use

The evaluation pack naturally produces the Stage 2 exit evidence as a side-effect. This is the right structure.

---

## Open Questions

### Q1: Should the planner use LLM reasoning for source selection within this tranche?

The current `_plan_aoi()` in `task_planner.py:369-483` is fully deterministic — it resolves the source catalog and checks profile feasibility without any LLM call. The task router (`route-task`) uses pattern matching for workflow selection.

True task-driven source selection (where natural-language task text influences *which* source families are foregrounded) would likely need LLM-based reasoning. The memo's concrete examples ("concept evolution" → synthesis-oriented, "engagement/contest" → comparison-oriented) suggest the planner should interpret task semantics.

This question should be resolved early in implementation:
- **Deterministic rule-based**: Map task keywords/patterns to source family weightings. Simpler, cheaper, testable, but may not feel genuinely "task-first."
- **LLM-assisted**: Pass the task text to a bounded LLM call that selects source families with rationale. More aligned with the "analyzer as brain" thesis, but adds latency and cost.
- **Hybrid**: Deterministic for clear cases, LLM for ambiguous ones.

The memo does not need to resolve this — it's an implementation choice. But the evaluation pack (Deliverable 4) should assess whichever approach is chosen.

### Q2: What is the expected effort split between analyzer-v2 and the-critic?

The likely implementation seams (lines 358-378) list roughly equal numbers of files in both repos. But the *nature* of the work differs:
- Analyzer-side: contract widening, planner logic changes, evaluation artifacts
- Consumer-side: threading richer metadata through location.state, compose page UX changes, legacy control de-emphasis

The compose page UX work could expand significantly if the goal is to make the planner-primary path feel meaningfully different from the current profile-button path. The tranche should have a clear implementor assignment or at least a note about which repo is primary.

---

## Judgment on Sequencing and Bigger-Picture Fit

### Sequencing remains correct (confirmed from pass 1)

The revised memo strengthens the sequencing argument by:
1. Explicitly handling Stage 2, which removes the "skipped stage" objection
2. Naming the compose-contract widening requirement, which prevents implementation from producing a superficially task-first path that is structurally unchanged
3. Requiring the closeout to name what the proof path actually used (existing profiles vs. widened contract), which forces honesty at exit

### The tranche is now well-scoped

The combination of Stages 3/4/5 into one tranche remains the right call. The revised memo adds enough specificity (concrete examples, contract widening acknowledgment, planner-primary definition, host residual naming) to make implementation actionable without being over-prescriptive.

### The strategic risk is adequately bounded

The big roadmap memo warns against staying in AOI/the-critic territory too long. This tranche stays there, but:
- The evaluation pack (Deliverable 4) creates the exit evidence that later generalization needs
- The non-goals are explicit and well-drawn
- The deferral of de-AOI/transient generalization is correct given the current profile-first residuals

One more AOI-focused tranche is justified if it produces the exemplar that all subsequent tranches will generalize from.

---

## Concrete Revisions Recommended Before Implementation

**None.** The memo is ready for implementation planning.

The observations above (particularly about the compose-contract widening decision and the LLM-vs-deterministic planner question) should be resolved early in the implementation plan, but they do not require memo-level revision.

---

## What Changed Between Pass 1 and Pass 2

| Pass 1 Finding | Resolution in Revised Memo |
|---|---|
| Stage 2 silently skipped | Decision 1A explicitly subsumes Stage 2; Deliverable 4 absorbs Stage 2 exit evidence |
| Planner contract richer than claimed | Decision 5 reframed: backend is richer, host-consumed seam is the gap |
| "Not reducible to dossier/comparison" needs examples | Lines 289-293 add concrete task examples with honest escape clause |
| Existing readiness gate vs. missing eval pack | Decision 6 distinguishes operational readiness gate from Stage 5 evaluation pack |
| Legacy controls need visual distinction | Decision 3 specifies planner-primary as recommended/confirmed; host should not re-ask the analytical choice |
| Planner-primary definition unclear | Lines 152-158 define recommended/confirmed composition, not blind auto-execution |
| Host residuals unnamed | Decision 6A names host-proxy identity translation and snapshot warmup explicitly |

All six recommended revisions from pass 1 are addressed.
