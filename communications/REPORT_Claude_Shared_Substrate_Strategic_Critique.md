# REPORT: Shared Substrate Strategic Critique

**Date**: 2026-03-16
**Reviewer**: Claude Opus 4.6 (automated architectural review)
**Memo Under Review**: `MEMO_2026-03-16_shared_substrate_for_bespoke_analysis_apps.md`

---

## 1. Thesis Verdict

**The strategic direction is correct. The architectural claims are overstated by roughly 18 months of work.**

The memo identifies the right long-term destination: a shared analytical substrate from which bespoke analysis apps can be assembled with minimal per-objective frontend work. This is genuinely the economically rational direction given the growing number of objectives (genealogy, AOI, logical, hermeneutic, critique, extrapolation).

But the memo conflates three things:

1. **What the definition catalog already supports** (composable engine/chain/operationalization selection) — this is real and working
2. **What the executor can do today** (run plans to completion with context threading within a single job) — this is real but job-scoped
3. **What would be required for the substrate economy the memo describes** (reusable intermediate artifacts, dynamic view composition, consumer SDK) — this does not exist in code

The memo reads as if the system is 80% of the way to the substrate vision. A code-grounded assessment puts it closer to 40%. The definition layer and orchestration are strong. The artifact layer, composition language, and consumer integration are absent.

---

## 2. Confirmed Architectural Strengths

### 2.1. The engine/chain/operationalization separation IS the correct skeleton

**Evidence**: `src/operationalizations/definitions/` contains 20+ YAML files, each mapping stances to engine-specific focus dimensions and depth sequences. `src/stages/capability_composer.py` composes prompts from this three-layer structure (stance + engine + depth). This is not a stub — it's operational and used in every executor run.

The separation works because:
- Engines define WHAT to analyze (analytical dimensions, capabilities)
- Stances define HOW to think (discovery, confrontation, dialectical, integration)
- Operationalizations bridge them with engine-specific prose and focus

This gives real combinatorial leverage. Adding a new stance to an existing engine requires one YAML entry, not new code.

### 2.2. The adaptive planner IS genuinely compositional

**Evidence**: `src/orchestrator/adaptive_planner.py:414-657` generates bespoke pipelines from objectives + book samples + the full capability catalog. It is not template replay — the LLM can add, remove, reorder phases, assign different chains per work, and select supplementary chains based on the thinker's profile.

Key proof: `src/orchestrator/adaptive_planner.py:132-254` contains auto-correction logic for LLM mistakes (engine in chain field, compound chain keys). You don't build correction code for a system that only replays templates.

### 2.3. The executor DOES thread context across phases

**Evidence**: `src/executor/context_broker.py:24-105` assembles prior phase outputs into downstream context with configurable char limits. `src/executor/phase_runner.py:119-126` injects context_emphasis from the plan. Phase 2.0 genuinely receives Phase 1.0's analytical prose, not just a flag.

This is the seed of the substrate threading the memo describes. It works within a single job execution.

### 2.4. Genealogy DOES demonstrate multi-layer composition

The intellectual genealogy workflow genuinely composes reusable capability engines (`conceptual_framework_extraction`, `inferential_commitment_mapper`, `concept_evolution`) with genealogy-specific closure engines (`genealogy_relationship_classification`, `conditions_of_possibility_analyzer`). The structure matches the memo's "shared substrate + objective closure" pattern.

### 2.5. The Critic's frontend HAS evolved toward generic consumption

**Evidence**: `the-critic/webapp/src/components/V2TabContent.tsx` renders any analyzer-v2 `PagePresentation` with zero per-workflow React code. `AnalysisWorkspacePage.tsx` (~480 lines) works for any workflow_key. 17 sub-renderers dispatch based on data shape, not analysis type. This is a genuine step toward "thin consumer apps."

---

## 3. Overstatements or Weak Claims

### 3.1. OVERSTATEMENT: "analyzer-mgmt as authoring, inspection, and packaging layer"

**Code reality**: analyzer-mgmt is a **read-heavy dashboard**, not a packaging/authoring layer.

**Evidence**:
- `analyzer-mgmt/frontend/src/lib/api.ts` has two targets: `API_BASE` (mgmt backend) and `ANALYZER_V2_URL` (v2 direct). Most entity pages are read-only views of v2 definitions.
- There is NO workflow composer, NO pipeline DAG builder, NO objective editor that triggers planning.
- Workflows are authored by editing JSON files in `analyzer-v2/src/workflows/definitions/` — not via any UI.
- The objectives page (`analyzer-mgmt/frontend/src/pages/objectives/[key].tsx`) has CRUD but cannot trigger orchestration or link to execution.
- The plans page shows orchestrator-generated plans but cannot edit or create them.

**Memo impact**: The memo positions analyzer-mgmt as co-equal to analyzer-v2 in the "reusable brain." In reality, analyzer-v2 is the brain; analyzer-mgmt is the diagnostic display. This matters because the memo's vision of LLM-assembled bespoke apps implies a composition tool, and that tool does not exist anywhere.

### 3.2. OVERSTATEMENT: "the system already supports" substrate composition

The memo says (Section "What the Current Architecture Already Supports") that the system already "cleanly distinguishes analytical levels" and "the planner already has room to compose, not just replay templates."

**What's actually true**: The planner CAN compose. The definition catalog IS compositional. But the **execution outputs are not substrates** — they are ephemeral, job-scoped prose blobs.

**Evidence**: `src/executor/output_store.py:21-63` saves outputs keyed by `(job_id, phase_number, engine_key, work_key, pass_number)`. The `job_id` is the primary scope. There is:
- No content-addressable identity for outputs
- No cross-job lookup ("give me the last concept_evolution output for Thinker X")
- No staleness detection ("has this input changed since the cached output?")
- No artifact versioning

The context_broker (`context_broker.py:24-105`) only reads outputs within the same job_id. Cross-job reuse is architecturally blocked by the current storage model.

**Memo impact**: The memo correctly identifies reusable intermediate artifacts as "the most important missing concept" — but understates how far the current storage model is from supporting them. It's not a matter of adding a cache layer; it requires a fundamentally different identity model for outputs.

### 3.3. OVERSTATEMENT: "AOI already demonstrates bounded objective closure"

The memo says AOI proves "the platform can support a distinct objective and presenter surface without downstream semantic improvisation."

**Code reality**: AOI's v2 integration is still in progress. As of 2026-03-16:
- The Critic's active `MASTER_MEMO_CURRENT.md` is literally titled "AOI v2 hot-path cutover" — it's not done
- `src/aoi/contract.py` in the dirty backup shows AOI using `_load_previous_normalized()` to thread phase outputs — but this is a bespoke function, not the generic context_broker
- The AOI thematic workflow (`anxiety_of_influence_thematic_single_thinker.json`) exists as a definition, but the frontend integration uses legacy `DualAxisView` components
- `AoiV2ThematicPanel.tsx` in the-critic is an emerging component, not yet proven

**Memo impact**: AOI is better described as a proof-in-progress, not a completed proof. Using it as evidence for "bounded objective closure" is premature.

### 3.4. OVERSTATEMENT: Implied proximity to "LLM-assembled bespoke apps"

The memo's Section "Role of the LLM" describes the LLM as "objective interpreter, planner, substrate selector, closure selector, presentation selector." Of these five roles:

| Role | Status | Evidence |
|------|--------|----------|
| Objective interpreter | Exists | Adaptive planner reads `AnalysisObjective` definitions |
| Planner | Exists | `adaptive_planner.py` generates phase DAGs |
| Substrate selector | Partial | Planner selects engines/chains but cannot select cached artifacts |
| Closure selector | Partial | Planner can add objective-specific phases |
| Presentation selector | Stub | Planner includes `view_recommendations` in plan, but these are suggestions, not executable compositions |

The gap between "planner suggests views" and "LLM assembles a bespoke analysis site" is enormous. It requires:
- A view composition runtime (not just static definitions)
- Dynamic page layout generation
- Frontend code generation or a sufficiently powerful template system
- Consumer app bootstrapping from a specification

None of this exists in any of the four codebases.

### 3.5. WEAK CLAIM: "chains should be objective-agnostic substrate chains"

The memo says chains like `deep_text_profiling` and `argument_analysis_chain` are "not genealogy chains in spirit."

**Code reality**: Looking at `src/chains/definitions/`, many chains were designed for genealogy and carry genealogy assumptions:
- `genealogy_target_profiling` — name is genealogy-specific
- `genealogy_preliminary` — genealogy-specific
- Engine keys within chains reference genealogy-oriented capabilities

Some chains genuinely are substrate-level (`deep_text_profiling`, `argument_analysis_chain`). But the claim that existing chains are already substrate-ready requires renaming, documentation, and in some cases restructuring to remove genealogy assumptions from their prompts.

---

## 4. Missing Constraints or Missing Abstractions

### 4.1. MISSING: Artifact identity and persistence model

This is the memo's own identified gap, but the memo understates the engineering required.

A reusable intermediate artifact needs:
1. **Stable identity**: Content-addressable hash or input-addressable key (e.g., `(engine_key, input_hash, stance_key, depth)`)
2. **Staleness detection**: If the input text or engine definition changes, the cached artifact is invalid
3. **Cross-job query API**: "Give me the latest concept_evolution for input X" — currently impossible
4. **Versioning**: Multiple runs may produce different outputs; the system must track which version downstream consumers used
5. **Garbage collection**: Old artifacts must be expirable

The current `output_store.py` has none of these. It's a write-once, read-within-job store. Moving to reusable artifacts requires either:
- A new table/store with a different identity model, or
- An artifact registry that sits above the output store

**This is the single highest-leverage missing abstraction**, and the memo is correct to identify it.

### 4.2. MISSING: Consumer SDK / integration contract

The Critic has reimplemented significant infrastructure for consuming analyzer-v2:

- `analyzer_v2_client.py` (900 lines): HTTP client with caching, version polling, async wrappers
- Job management: `_GENEALOGY_JOBS` dict, `run_genealogy_v2_thread()`, polling endpoints, cancellation
- Result persistence: `_save_v2_presentation_to_db()`, separate database tables per workflow
- Frontend integration: `useWorkflowMetadata`, `useViewDefinitions`, dual endpoint config

**None of this is reusable by the next consumer app.** If a "hermeneutic reading" app needs to consume analyzer-v2, it would have to reimplement all of this.

The memo's vision of "thin downstream apps" requires a **consumer SDK** that provides:
- Standard client for orchestrator/executor APIs
- Job lifecycle management (start, poll, cancel, resume)
- Result caching and persistence
- Frontend component library for rendering PagePresentations

This SDK does not exist and is not mentioned in the memo.

### 4.3. MISSING: Composition language for new objectives

Today, defining a new objective requires:
1. Write JSON in `src/objectives/definitions/` (objective definition)
2. Write JSON in `src/workflows/definitions/` (workflow template, optional but common)
3. Write YAML in `src/operationalizations/definitions/` (for any new engines)
4. Edit JSON in `src/engines/definitions/` (for any new engines)
5. Write JSON in `src/views/definitions/` (view definitions for presentation)
6. Write JSON in `src/chains/definitions/` (for any new chains)
7. Push to git, redeploy

There is no UI, no API, and no LLM-assisted workflow for creating a new objective end-to-end. The adaptive planner can compose phases from existing definitions, but it cannot create new definitions.

The memo's vision of "future objectives begin with 'what shared substrate does this objective need?'" implies a higher-level composition workflow that does not exist.

### 4.4. MISSING: The Critic's database normalization

The Critic has separate database tables per workflow type:
- `InfluenceThinkerDB`, `InfluenceReferenceTextDB` (AOI)
- `GenealogyAnalysisDB` (genealogy)
- `CorpusDiscoveryDB` (corpus analysis)

If The Critic is to become a thin consumer, its database needs to consolidate to something like `WorkflowAnalysisDB(workflow_key, job_id, v2_job_id, result_json)`. The memo doesn't address this migration, but it's a prerequisite for treating The Critic as a generic consumer rather than a workflow-specific app.

### 4.5. PARTIALLY MISSING: View generation vs. view selection

The memo treats views as something the planner can "select." The current system supports this — `view_recommendations` in the plan can suggest views. But the view definitions themselves are static JSON files, manually authored.

For the substrate vision to work at scale, the system needs either:
- Enough pre-authored views that most objectives can be served by selection (library approach)
- LLM-assisted view generation from patterns + engine output shapes (generative approach)

`POST /v1/views/generate` exists as an endpoint (LLM-powered view generation from pattern + engine), which is promising. But view patterns (`src/views/patterns/` — 6 files) are genealogy-focused. New objectives would need new patterns or a more flexible generation system.

---

## 5. Best Alternative Framing

The memo's framing of "shared substrate + objective closure" is directionally correct but imprecise. It conflates the definition catalog (which IS shared) with execution artifacts (which are NOT shared).

**Stronger framing**: **"Definition catalog + LLM orchestration + artifact economy + consumer contract"**

This separates the four layers more honestly:

| Layer | Current Status | What's Needed |
|-------|---------------|---------------|
| **Definition catalog** | Strong. 160+ engines, 19 chains, 20+ operationalizations, 8 workflows, 3 objectives, 21 views. | More substrate-labeled chains, more objective definitions, view patterns for non-genealogy objectives. |
| **LLM orchestration** | Strong. Adaptive planner generates bespoke phase DAGs from catalog + objectives. | Artifact-aware planning: "reuse existing concept_evolution output if fresh enough." |
| **Artifact economy** | Missing. Outputs are job-scoped ephemera. | Content-addressable artifact store, cross-job lookup, staleness detection, versioning. |
| **Consumer contract** | Missing. Each app reimplements client, job management, result persistence. | SDK/library: standard client, job lifecycle, result caching, rendering components. |

The memo's "substrate" language is appealing but masks the fact that the system currently has a **definition substrate** (strong) but no **artifact substrate** (missing). The former lets you compose PLANS efficiently. The latter would let you compose RESULTS efficiently. Both are needed for the full vision.

An alternative governing principle:

> **"Shared definitions compose plans; shared artifacts compose results; shared consumer contracts compose apps."**

This is more operational than "shared substrate first, bespoke closure last" because it identifies three distinct sharing mechanisms, each requiring different engineering.

---

## 6. Recommended Correction To The Memo

### 6.1. Separate "definition reuse" from "artifact reuse"

The memo conflates these. Definition reuse (engines, chains, operationalizations) is real and working. Artifact reuse (cached analytical outputs) does not exist. The memo should have two sections: one celebrating the definition layer, one honestly scoping the artifact layer as a new engineering effort.

### 6.2. Downgrade analyzer-mgmt's role

The memo positions it as co-equal. It should say: "analyzer-mgmt is currently a diagnostic dashboard for definitions. For the substrate vision, it must evolve into a composition tool — or a new composition layer must be built." Don't claim what isn't there.

### 6.3. Mark AOI as proof-in-progress, not completed proof

Replace "AOI demonstrates bounded objective closure" with "AOI is testing whether the platform's objective closure model works for a second objective type. Results are pending."

### 6.4. Add a "what's actually required" section

The memo ends with "open questions" but doesn't enumerate the concrete engineering requirements. It should list:
1. Artifact identity model and store
2. Cross-job artifact lookup API
3. Consumer SDK (client, job management, result persistence, rendering)
4. Database normalization in The Critic
5. Non-genealogy view patterns
6. Composition UI or LLM-assisted objective definition workflow

### 6.5. Drop the implication that the system is 80% there

The definition and orchestration layers are strong (perhaps 80% of the definition/planning vision). The artifact, consumer, and composition layers are 0-10% implemented. The overall system is roughly 40% of the way to the described vision. The memo should say this clearly to set correct expectations for refactoring scope.

### 6.6. Address The Critic's coupling honestly

The memo says "treat current apps as proofs." But The Critic has 19 legacy analysis types, a per-workflow database schema, and 4,000+ lines of API server code with workflow-specific endpoints. "Treating it as a proof" requires either deprecating most of this code or migrating it. The memo should acknowledge this cost.

---

## 7. Recommended Next Move

Given the gap analysis above, the highest-leverage moves in priority order:

### Move 1: Artifact Identity Model (Highest Leverage)

Design and implement a content-addressable artifact store alongside or above the current output_store.

**Minimum viable artifact**:
```python
class AnalyticalArtifact:
    artifact_id: str          # UUID
    artifact_key: str         # (engine_key, input_hash, stance_key, depth) → deterministic
    engine_key: str
    input_hash: str           # SHA256 of input text
    stance_key: Optional[str]
    depth: str
    content: str              # The analytical prose
    content_hash: str         # SHA256 of output
    created_at: datetime
    source_job_id: str        # Which job produced this
    version: int              # Increments if re-run with same input
    metadata: dict            # Engine-specific metadata
```

**API**:
```
POST /v1/artifacts                     # Store artifact (from executor)
GET  /v1/artifacts?engine_key=X&input_hash=Y  # Cross-job lookup
GET  /v1/artifacts/{artifact_id}       # Direct retrieval
GET  /v1/artifacts/freshness?artifact_id=X     # Staleness check
```

This unblocks the entire "artifact economy" the memo envisions.

### Move 2: Consumer Integration Contract

Extract The Critic's `analyzer_v2_client.py` + job management into a reusable package.

**Deliverable**: A Python package (`analyzer-v2-client`) that any consumer app can install, providing:
- Typed client for all v2 endpoints
- Job lifecycle management (start, poll, cancel, resume)
- Result caching with TTL
- Event hooks (on_phase_complete, on_job_complete)

**Frontend deliverable**: A React component library (`@analyzer-v2/react`) providing:
- `V2TabContent` equivalent
- Sub-renderer dispatch
- Job status polling hook
- Provenance display

### Move 3: Substrate Chain Reclassification

Audit all 19 chains. For each, answer: "If three future objectives needed this, would we be happy it lived as a shared asset?"

Predicted classification:
- **Substrate**: `deep_text_profiling`, `argument_analysis_chain`, `concept_exploration_chain`
- **Rename**: `genealogy_target_profiling` → `target_work_profiling`
- **Objective-specific**: `genealogy_preliminary` (may need splitting)
- **Review**: chains with genealogy-specific prompts baked into engine definitions

### Move 4: Non-Genealogy View Patterns

Currently 6 view patterns, all genealogy-focused. For the substrate vision, create patterns for:
- Thematic analysis (AOI-style: theme inventory, engagement mapping, findings)
- Logical analysis (argument structure, inference chains, contradiction detection)
- Generic comparison (multi-work comparison grids, difference detection)

### Move 5: Composition Workflow (Longer Term)

Build an LLM-assisted "new objective" workflow, either in analyzer-mgmt or as a CLI tool:
1. User describes objective in natural language
2. LLM recommends: which substrate chains to reuse, which new closure engines to create, which view patterns to apply
3. System generates skeleton definitions (objective JSON, workflow JSON, view JSONs)
4. User reviews and refines
5. Definitions committed and deployed

This is the path to "bespoke analysis apps without hand-authoring each one" — not the current state, but a realistic next step after Moves 1-4.

---

## Appendix: Key File Evidence

| Claim Tested | File | Finding |
|---|---|---|
| Adaptive planner composes dynamically | `src/orchestrator/adaptive_planner.py:414-657` | Confirmed: LLM generates bespoke phase DAGs |
| Outputs are reusable artifacts | `src/executor/output_store.py:21-63` | Refuted: outputs keyed by job_id, no cross-job lookup |
| analyzer-mgmt is an authoring layer | `analyzer-mgmt/frontend/src/lib/api.ts` | Refuted: read-heavy dashboard, no composition tools |
| AOI proves bounded closure | `the-critic/communications/MASTER_MEMO_CURRENT.md` | Partial: AOI v2 cutover still in progress |
| Context threads across phases | `src/executor/context_broker.py:24-105` | Confirmed: within-job context assembly works |
| Consumer SDK exists | `the-critic/analyzer/concept_analyzer/analyzer_v2_client.py` | Refuted: bespoke 900-line client, not reusable |
| View composition is dynamic | `src/views/definitions/` (21 files) | Partial: static definitions, not runtime composition |
| Chains are substrate-ready | `src/chains/definitions/` | Partial: some genuinely reusable, some genealogy-branded |
| The Critic is a thin consumer | `the-critic/api/server.py` (4000+ lines) | Refuted: thick app with per-workflow DB tables and legacy analyses |
