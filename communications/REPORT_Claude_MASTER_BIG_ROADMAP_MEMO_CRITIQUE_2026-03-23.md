# Review: MASTER BIG ROADMAP MEMO — ANALYZER-V2 AS THE BRAIN FOR DYNAMIC BESPOKE ANALYTICAL APPS

Reviewer: Claude Opus 4.6 (1M context)
Date: 2026-03-23
Primary document reviewed: `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

## Verdict: Approve After Revision

The memo is strategically sound and directionally honest. Its separation of "what is real" from "what is aspirational" is the strongest quality of the document. The round-by-round progress documentation is code-grounded and verifiable.

However, the memo has four material problems that need correction before it should be treated as the canonical reference:

1. A document governance violation that contradicts its own central rule
2. A significant understatement of existing upstream infrastructure
3. A stage ordering error
4. An unintegrated prior proposal that matters to the vision

---

## FINDINGS (Ordered by Severity)

### FINDING 1 — CRITICAL: Two documents both claim canonical status

The memo declares as its first rule: "This document is now the canonical roadmap memo for this program" and "one document should say where we are."

But a second file exists with nearly identical content and scope:

- `communications/MASTER_BIG_ROADMAP_MEMO_DYNAMIC_BESPOKE_APPS_PLATFORMIZATION.md` (1043 lines)

This second file also claims canonical status: "This document is now the canonical program-tracking memo for the dynamic bespoke apps effort."

Both documents are dated 2026-03-23. Both are untracked (git status shows `??`). Both cover the same strategic territory with minor wording differences.

This is not a minor hygiene issue. The memo's entire governance thesis rests on "one document should say where we are." Having two near-duplicate canonical documents violates that thesis on day one.

**Required action**: Delete or explicitly deprecate one of the two files. There must be exactly one canonical roadmap memo.

### FINDING 2 — SIGNIFICANT: The memo substantially understates existing orchestrator/planner infrastructure

The memo's Stages 7–9 describe "Generic task-intake contract," "Task-to-workflow planner," and "Task-to-engine/chain planner" as if they would be built from scratch. Each stage's description uses language like "build" and "introduce."

But the codebase already contains ~5,171 lines of orchestrator code:

| Module | Lines | Capability |
|--------|-------|------------|
| `src/orchestrator/planner.py` | 541 | LLM-powered plan generation from capability catalog |
| `src/orchestrator/adaptive_planner.py` | 680 | Adaptive plan generation with objective-driven engine selection |
| `src/orchestrator/pipeline.py` | 582 | End-to-end pipeline: documents → plan → execution → presentation |
| `src/orchestrator/catalog.py` | 638 | Planner-readable capability catalog assembly |
| `src/orchestrator/schemas.py` | 547 | WorkflowExecutionPlan, PhaseExecutionSpec, full plan schemas |
| `src/orchestrator/pipeline_schemas.py` | 336 | AnalyzeRequest with target work, prior work, objective |
| `src/orchestrator/plan_revision.py` | 493 | Mid-course plan revision |
| `src/orchestrator/sampler.py` | 321 | Source material sampling |

This infrastructure already does most of what Stages 7–9 describe:

- **Task intake** — `AnalyzeRequest` already accepts objective, target work, prior work, workflow key, audience, and a `skip_plan_review` flag. This is not zero.
- **Engine/chain planning** — `generate_plan()` and `generate_adaptive_plan()` already produce multi-phase `WorkflowExecutionPlan` structures with engine selection, sequencing, and data dependencies.
- **Workflow routing** — The adaptive planner already selects engines based on objective definitions.

The real gap is not "build" but **"generalize and connect"**:

1. The orchestrator currently produces job-backed execution plans. The compose-from-intent system produces transient pages. These two systems are disconnected.
2. The orchestrator currently serves genealogy and AOI workflows. The vision needs it to serve arbitrary tasks.
3. The planner's capability catalog does not yet feed into compose-from-intent's page-structure planning.

This distinction matters because it changes the estimated difficulty and the stage descriptions. "Build a task-to-engine planner" sounds like a 6-month project. "Generalize the existing planner and bridge it to transient composition" is more like a 2-month project.

**Impact on the 35–45% estimate**: The full-vision completion percentage should be revised upward to approximately 45–55% once the existing orchestrator infrastructure is honestly accounted for.

### FINDING 3 — SIGNIFICANT: Stage 5 (Lifecycle Decision) is ordered before Stage 6 (Evaluation Guardrails)

The memo places the lifecycle decision (ephemeral-only vs. draft/session persistence) at Stage 5, before building evaluation and quality guardrails at Stage 6.

This is backwards. The lifecycle decision should be informed by:

- How well the system performs in practice (needs evaluation)
- What latency/cost profile the transient path has (needs profiling)
- Whether the transient experience is useful enough to persist (needs user evidence)

Making the lifecycle decision before having evaluation evidence risks either:
- Committing to persistence infrastructure prematurely, or
- Locking in "ephemeral only" before knowing whether users would benefit from persistence

**Recommended fix**: Swap Stages 5 and 6. Build evaluation/guardrails first, then make the lifecycle decision with evidence.

### FINDING 4 — MODERATE: Semantic Visual Matcher proposal is acknowledged but not integrated

The memo lists `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md` as an important prior document and mentions it in Stage 11 as "potentially integration with ideas from…"

But the Semantic Visual Matcher addresses a fundamental quality gap: the system currently matches renderers by data structure, not analytical meaning. The proposal shows concretely how a `feedback_loop_mapper` gets rendered as a generic radial diagram instead of a causal loop diagram because the curation layer asks "what data structure?" instead of "what analytical concept?"

If the full vision is truly about **bespoke** analytical experiences — surfaces shaped by analytical meaning, not just data shape — then semantic visual matching is not optional decoration for Stage 11. It is a prerequisite for the "bespoke" claim itself.

The memo should either:
- Give the Semantic Visual Matcher its own bounded stage (probably between current Stages 9 and 10), or
- Explicitly scope it into Stage 11 as a required deliverable, not a "potentially"

### FINDING 5 — MODERATE: compose_from_intent.py is not just "bounded" — it is fundamentally AOI-coupled

The memo describes compose-from-intent as "bounded and AOI-specific in practice" (Section 5, point 4). The code is more tightly coupled than that characterization suggests:

- **Hardcoded workflow**: `_validate_request()` rejects anything except `AOI_WORKFLOW_KEY` (line 294)
- **Hardcoded consumer**: rejects anything except `the-critic` (line 298)
- **Hardcoded profile mapping**: `dossier` → exactly `[aoi_thematic_synthesis, aoi_thematic_report]`; `comparison` → exactly `[aoi_engagement_mapping, aoi_sin_findings, aoi_thematic_report]` (lines 366–417)
- **Hardcoded pattern/renderer allowlist**: only `prose_narrative`, `accordion_sections`, `card_grid_simple`, `card_grid_grouped` patterns; only `prose`, `accordion`, `card_grid` renderer types (lines 69–77)
- **Hardcoded section cap**: max 4 sections (line 307)

This is not "bounded." It is bespoke to one workflow family's specific output structure. The generalization challenge is substantially harder than the memo implies because the compose-from-intent module needs to handle:

- Arbitrary engine output shapes (not just 4 AOI engine types)
- Arbitrary renderer families (not just 3)
- Arbitrary section counts and hierarchies
- Source material from workflows with different artifact structures

The roadmap should explicitly acknowledge this coupling and estimate the generalization effort honestly.

### FINDING 6 — MODERATE: The stage count (15+) risks roadmap fatigue

The roadmap contains 16 stages (0–15), of which 11 are "Not started." Only 3 are in progress and 1 is partial.

This creates two risks:
1. **Motivational fatigue**: 11 "Not started" stages can feel overwhelming and reduce momentum
2. **False granularity**: Some stages can likely be combined or parallelized

For example:
- Stages 7 + 8 (generic task-intake + task-to-workflow planner) are tightly coupled and should probably be one stage
- Stages 12 + 13 (universal renderer law + minimal host contract) could be parallel workstreams
- Stage 0 ("keep the roadmap current") is a meta-discipline, not a stage with exit criteria

Consider condensing to ~10 stages that map more naturally to implementation rounds.

### FINDING 7 — MINOR: No "Perspective" docs folder exists

The prompt asked to inspect relevant documents in a "Perspective" docs folder. No such folder was found in either `analyzer-v2/docs/` or `the-critic/docs/`. This is stated explicitly rather than implied.

---

## STRATEGIC ASSESSMENT

### Is the memo's strategic assessment honest?

**Yes, substantially.** The separation of "what is real" from "what is aspirational" is genuine. The code confirms all six claims in Section 4. The "what is not true yet" section (Section 5) is appropriately blunt.

However, the 35–45% full-vision estimate is probably too conservative given the existing orchestrator infrastructure (Finding 2). A more honest estimate is 45–55%.

### Was the last week directionally correct?

**Yes, strongly.** Rounds 9–14 followed a coherent dependency chain: renderer contracts → consumer consolidation → transient composition → source-backed composition → hot-path adoption. Each round built on the previous one without thickening the consumer. The code confirms this.

### Is the memo underestimating any major missing piece?

**Yes.** The memo underestimates two things:

1. **The existing orchestrator infrastructure** — which means the upstream planning gap is narrower than described but requires a different kind of work (generalization + bridging, not greenfield construction)

2. **The semantic matching gap** — the difference between "select renderer by data structure" and "select renderer by analytical meaning" is fundamental to the bespoke-app vision. The Semantic Visual Matcher proposal addresses this directly and should be integrated into the roadmap, not deferred as a "potentially."

### Is the stage breakdown complete?

**Mostly.** The stages cover the right territory. But a stage or explicit sub-stage for semantic visual matching is missing, and some stages should be consolidated (see Finding 6).

### Is the ordering right?

**Mostly.** One swap is needed: Stage 5 (lifecycle decision) and Stage 6 (evaluation guardrails) should be reordered (see Finding 3). The overall macro-ordering — finish AOI MVP, then shift upstream to planning/orchestration — is correct.

### Is the memo overfitting to AOI / the-critic?

**Yes, but it knows this.** The memo correctly identifies this as the main strategic risk (Section 7). The concern is real and well-articulated. However, the memo then proceeds to define Stages 2–4 as further AOI-specific work before any generalization happens (Stages 7+). That means the program could spend another 3–4 rounds on AOI-specific work before confronting generalization. This is too long. Consider abbreviating the AOI-specific tail and pulling generalization forward.

### Biggest strategic risk?

The memo correctly identifies it: **continuing to optimize the AOI pilot instead of generalizing the platform.** But there is a subtler version of this risk the memo doesn't call out: the compose-from-intent module's deep AOI coupling (Finding 5) means that generalization is not a matter of "removing a few allowlists." It requires restructuring the composition pipeline's source-material contract, planner interface, and pattern/renderer selection logic. If the program treats generalization as a light parametrization task, it will underestimate the work and stall.

---

## RECOMMENDED MEMO REVISIONS

1. **Delete one of the two canonical roadmap memos.** Choose one file. Delete the other. This is non-negotiable given the memo's own governance rule.

2. **Revise Stages 7–9 to acknowledge existing orchestrator infrastructure.** Change language from "build" to "generalize and bridge." Update the stage descriptions to reference the existing 5K-line orchestrator module. Revise the full-vision percentage estimate upward.

3. **Swap Stages 5 and 6.** Evaluation guardrails first, lifecycle decision second.

4. **Promote the Semantic Visual Matcher from "potentially" to "required."** Either give it a bounded stage or scope it explicitly into Stage 11 as a must-land deliverable.

5. **Add a note to Stage 3 or 4 about the compose-from-intent coupling depth.** The generalization path is harder than "removing bounded constraints." The hardcoded profile mappings, engine keys, section caps, and pattern allowlists in `compose_from_intent.py` represent substantial structural coupling, not just configuration.

6. **Consider consolidating 16 stages to ~10–12.** Merge Stages 7+8, consider parallelizing 12+13, demote Stage 0 to a meta-discipline footnote.

7. **Add a "prior infrastructure inventory" section** to the memo that lists existing capabilities (orchestrator, planner, adaptive planner, execution pipeline, transformation generator, view generator) so future sessions understand what already exists before assuming greenfield work.

---

## BEST NEXT STAGE

The single highest-leverage next stage after documentary closure on rounds 13 and 14 is:

**A bounded generalization pilot that connects the existing orchestrator pipeline to the compose-from-intent system for one non-AOI workflow.**

Rationale:

- The downstream composition stack is proved (rounds 9–14)
- The upstream orchestrator infrastructure already exists (~5K lines)
- The biggest strategic gap is the bridge between them
- Doing this for a **second workflow** (e.g., genealogy) would simultaneously:
  1. Force generalization of compose-from-intent beyond AOI-specific coupling
  2. Prove that the orchestrator's plan output can feed the composition pipeline
  3. Create the first evidence that the platform thesis holds beyond one workflow
  4. Expose which parts of the compose-from-intent module are genuinely reusable vs. AOI-bespoke
  5. Provide the evaluation evidence needed for the lifecycle decision

This is more valuable than further AOI MVP polish (Stage 2) or further AOI-specific task-driven composition (Stages 3–4) because it directly attacks the biggest strategic risk the memo itself identifies: overfitting to the AOI pilot.

The most honest formulation:

> **Bridge the existing orchestrator to compose-from-intent for one second workflow, forcing generalization of the source-material contract, planner interface, and renderer selection logic.**

That single move would advance Stages 7, 8, 10, and 12 simultaneously while providing evidence for Stage 5/6 decisions. It is the highest-leverage intervention available.

---

## FILES INSPECTED

### Documents
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` — primary
- `communications/MASTER_BIG_ROADMAP_MEMO_DYNAMIC_BESPOKE_APPS_PLATFORMIZATION.md` — duplicate canonical
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md`
- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
- `communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md`
- `communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_completion.md`
- `communications/MEMO_2026-03-23_round14_aoi_transient_hot_path_launch_completion.md`
- `docs/MEMO_2026-02-19_orchestrator_vision.md`
- `docs/MEMO_2026-02-23_dynamic_generation_implementation.md`
- `docs/SEMANTIC_VISUAL_MATCHER_PROPOSAL.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md` (AOI V2 Hot-Path Cutover)
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`

### Code seams
- `src/presenter/compose_from_intent.py` (1122 lines, full read)
- `src/presenter/renderer_contract_enforcement.py` (146 lines, full read)
- `src/api/routes/presenter.py` (referenced, not fully read due to size)
- `renderers-ui/src/registry.ts` (29 lines, full read)
- `src/orchestrator/planner.py`, `adaptive_planner.py`, `pipeline.py`, `catalog.py`, `schemas.py`, `pipeline_schemas.py`, `plan_revision.py`, `sampler.py` (5,171 lines total, read headers and key functions)
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx` (251 lines, full read)
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx` (85 lines, full read)
- `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx` (543 lines, full read)
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx` (100 lines read, header and structure)

### Not found
- No "Perspective" docs folder exists in either `analyzer-v2/docs/` or `the-critic/docs/`
