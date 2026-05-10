# REPORT: Claude AOI vs Genealogy Meta-Layer Critique

Date: 2026-03-16
Reviewer: Claude Opus 4.6
Source memo: `MEMO_2026-03-16_aoi_vs_genealogy_meta_layer_parity_gap.md`

---

## 1. Thesis Verdict

**The memo's core diagnosis is directionally correct but contains a significant blind spot.**

The memo is right that genealogy has a partially real analyzer-v2 meta-layer that AOI lacks. But the memo overstates the significance of the objective/operationalization gap as AOI's *biggest* problem, and it underreports a more acute issue: **the thematic AOI workflow references four engine definitions that do not exist**. AOI's most critical gap is not meta-layer depth — it's that the canonical thematic workflow is broken at the engine level.

The memo also conflates two different kinds of "sophistication":

1. **Execution-path significance** — operationalizations in analyzer-v2 that actually control multi-pass prompt composition and execution order (real, verified)
2. **Catalog/management UI richness** — analyzer-mgmt screens for objectives, operationalizations, pipeline visualization that are editing/browsing surfaces over analyzer-v2 definitions (real but decorative within mgmt itself)

The memo treats these as one thing. They are not. The execution-path significance lives entirely in analyzer-v2's executor/planner/composer. analyzer-mgmt is a catalog editor that happens to store definitions to analyzer-v2 — it doesn't consume them.

---

## 2. Confirmed Findings

### 2a. Genealogy's operationalization layer is genuinely execution-critical

**Evidence** (strongest claim in the memo):

The operationalization layer is not metadata decoration. It is the actual execution specification for multi-pass engine runs.

Execution chain:
1. `executor/chain_runner.py:242-246` calls `compose_all_pass_prompts()` with `use_operationalizations=True`
2. `stages/capability_composer.py:227-244` checks operationalization FIRST, falls back to inline engine passes only if absent
3. Operationalization YAML files define: pass ordering per depth (surface/standard/deep), stance per pass, focus dimensions, focus capabilities, and `consumes_from` DAG between passes
4. Each pass gets its prompt shaped by the operationalization's stance description, dimensions, and capabilities

**Fallback behavior**: Without an operationalization, the executor falls back to the engine's inline depth_levels (capability_composer.py:246-270). So the operationalization is a behavioral override, not just annotation.

**Genealogy operationalizations**: 14 YAML files in `src/operationalizations/definitions/`, including `concept_appropriation_tracker.yaml`, `genealogy_relationship_classification.yaml`, `genealogy_final_synthesis.yaml`, and others.

**AOI operationalizations**: Zero files.

### 2b. Genealogy's objective layer drives adaptive planning

**Evidence**:

- `src/objectives/definitions/genealogical.json` contains 2,300+ characters of `planner_strategy` text
- `src/orchestrator/adaptive_planner.py:262-333` embeds the objective into the LLM planning prompt: primary goals, quality criteria, deliverables, preferred engines/categories, and the planner_strategy as "PLANNING STRATEGY GUIDELINES"
- `src/api/routes/orchestrator.py:463-505` loads the objective and passes it to plan generation

The objective is the primary driver of what phases the planner generates. Without it, the planner has a catalog but no "why."

**AOI objectives**: None exist. Only `genealogical.json` and `logical.json` are defined.

### 2c. The Critic's AOI is entirely bespoke

**Evidence**:

- `the-critic/analyzer/analyze_influence.py`: 2,248 lines, zero references to analyzer-v2
- `the-critic/api/server.py:11232-16261`: 60+ custom `/api/influence/*` endpoints, all calling local analyzer functions
- `the-critic/webapp/src/pages/AnxietyOfInfluencePage.tsx`: 103KB, all API calls to local `/api/influence/*`, no `ANALYZER_V2_URL` import
- No use of `V2TabContent` component, no `PagePresentation` consumption, no `objective_key` parameter

**Genealogy by contrast**: `analyze_genealogy.py` (1,557 lines) fetches workflow definitions from analyzer-v2 (`f"{ANALYZER_V2_URL}/v1/workflows/intellectual_genealogy"`), fetches engine definitions, and stores results as `PagePresentation` objects consumed by `V2TabContent`. Still a hybrid, but directionally v2-native.

### 2d. The two AOI workflows represent different abstractions

**Evidence**:

- `anxiety_of_influence.json` (v2): 5-phase legacy flow (identification → hypotheses → sampling → deep engagement → synthesis)
- `anxiety_of_influence_thematic_single_thinker.json` (v1): 4-phase bounded thematic flow (thematic synthesis → engagement mapping → sin findings → thematic report)

These are structurally different. The legacy flow is an app-shaped pipeline copied from The Critic's habits. The thematic flow is closer to an analyzer-v2-native semantic surface.

---

## 3. Overstatements or Weak Claims

### 3a. CRITICAL: The thematic AOI workflow is broken, not just meta-layer-deficient

The memo identifies the missing objective/operationalization layers as AOI's biggest gap. **This is wrong about the priority.**

The thematic workflow (`anxiety_of_influence_thematic_single_thinker.json`) references four engines:
- `aoi_thematic_synthesis` (Phase 1.0)
- `aoi_engagement_mapping` (Phase 2.0)
- `aoi_sin_findings` (Phase 3.0)
- `aoi_thematic_report` (Phase 4.0)

**None of these engine definitions exist in `src/engines/definitions/`.** The workflow references engine keys that resolve to nothing in the registry. This means the thematic AOI workflow **cannot execute at all** — not because it lacks meta-layer depth, but because it lacks basic engine definitions.

The memo proposes "canonicalize thematic AOI first" without noting that the thing to be canonicalized is currently non-functional. Adding objectives and operationalizations on top of missing engines would be building a meta-layer over a void.

### 3b. The memo overstates how "real" genealogy's analyzer-mgmt sophistication is

The memo says (Section 1): "The kinds of screens visible in analyzer-mgmt — objectives, operationalizations, capability/depth/dimensions tabs, pipeline visualization — are not just decorative for genealogy."

This is misleading. Within analyzer-mgmt, they ARE purely decorative:

- analyzer-mgmt's API backend (`api/main.py`) has NO routes for objectives or operationalizations
- analyzer-mgmt's database has NO models for these entities
- All objective/operationalization API calls go directly from the frontend to `ANALYZER_V2_URL` (`frontend/src/pages/objectives/index.tsx:133`, `frontend/src/pages/operationalizations/[key].tsx`)
- analyzer-mgmt is a CRUD editor that stores to analyzer-v2 and reads back from it

The sophistication IS real — but it's real in analyzer-v2's executor, not in analyzer-mgmt. The memo should distinguish: "analyzer-mgmt is a rich editor for definitions that are consumed by analyzer-v2's execution engine." Instead, it implies analyzer-mgmt itself carries execution significance.

### 3c. "Genealogy is increasingly analyzer-v2-native" overstates current state

The Critic's genealogy analyzer (`analyze_genealogy.py`, 1,557 lines) fetches definitions from analyzer-v2, but still:
- Runs its own LLM calls locally
- Has its own prompt composition logic
- Manages its own job lifecycle
- Falls back to built-in prompts for passes not yet deployed to analyzer-v2

The direction is correct, but the current state is **hybrid, not native**. The Critic's genealogy is "increasingly fetches-from-v2" rather than "delegates-to-v2."

### 3d. The memo underweights the chain gap

The memo mentions AOI chains only in passing (Section 3: "no comparable AOI planner-governed objective story"). But genealogy has three dedicated chains:
- `genealogy_target_profiling_chain.json`
- `genealogy_prior_work_scanning_chain.json`
- `genealogy_synthesis_chain.json`

AOI has zero chains. Chains are how multi-engine composition is specified. Without chains, even if AOI had engine definitions, it couldn't compose them into the multi-engine phases that genealogy uses.

---

## 4. Best Alternative Framing

**If the memo is wrong, the strongest alternative diagnosis is:**

> AOI's gap is not primarily about meta-layer depth (objectives/operationalizations). It's about **completeness of the basic layer**. The thematic AOI workflow was never finished: four engine definitions are missing, zero chains exist, and the workflow cannot execute. The meta-layer gap is a second-order problem that becomes relevant only after the first-order gap (missing engines and chains) is closed.

Under this framing, the closure path changes:

| Memo's Framing | Alternative Framing |
|---|---|
| 1. Add AOI objective | 1. Create the 4 missing engine definitions |
| 2. Add AOI operationalizations | 2. Create at least 1 AOI chain for multi-engine composition |
| 3. Expose in analyzer-mgmt | 3. Verify the thematic workflow can execute end-to-end |
| 4. Decide fate of legacy 5-pass | 4. THEN add objective + operationalizations |
| | 5. THEN decide legacy 5-pass fate |

The memo's recommended program (Direction A: "Make AOI meta-layer real") would be premature if the engines don't exist yet. You can't operationalize an engine that isn't defined.

**However**, this is a priority correction, not a rejection of the memo's diagnosis. The meta-layer gap IS real. It's just not the FIRST thing to fix.

---

## 5. Recommended Next Move

Based on the evidence, the closure path should be **bottom-up, not top-down**:

### Phase 1: Make thematic AOI executable (BLOCKING)

1. Create `src/engines/definitions/aoi_thematic_synthesis.json`
2. Create `src/engines/definitions/aoi_engagement_mapping.json`
3. Create `src/engines/definitions/aoi_sin_findings.json`
4. Create `src/engines/definitions/aoi_thematic_report.json`
5. Verify: `GET /v1/engines/aoi_thematic_synthesis` returns 200

### Phase 2: Add composition layer

6. Create at least one AOI chain (e.g., `aoi_thematic_chain.json`) that composes the four engines
7. Update the thematic workflow to reference the chain
8. Verify: the workflow can be loaded and visualized in analyzer-mgmt

### Phase 3: Add meta-layer (the memo's Direction A)

9. Create `src/objectives/definitions/influence_thematic.json`
10. Create operationalization YAMLs for the 4 AOI engines
11. Verify: `POST /v1/orchestrator/plan/adaptive` with `objective_key="influence_thematic"` generates a coherent plan

### Phase 4: Decide legacy fate (the memo's Direction C)

12. With the thematic AOI fully functional and meta-layer-backed, evaluate whether the 5-pass legacy flow should be:
    - Retired
    - Kept as intake/discovery
    - Reauthored

The memo's Hypothesis 2 (canonicalize thematic AOI) and Hypothesis 5 (reframe legacy as intake) are probably correct, but should wait until the thematic slice actually works.

---

## 6. Open Questions

### Q1: Were the four missing AOI engine definitions ever created and lost, or were they never written?

The thematic workflow exists and references them by key. Either:
- They were planned but never created (likely — the workflow is a spec, not a deployed artifact)
- They existed and were accidentally deleted (unlikely but worth checking git history)

This matters because if they were created, the prompts/schemas might be recoverable.

### Q2: How much of the legacy 5-pass AOI logic should inform the new engine definitions?

`analyze_influence.py` (2,248 lines) and `prompts_influence.py` contain substantial domain knowledge about how to:
- Identify intellectual influences
- Generate hypotheses about appropriation
- Sample textual evidence
- Conduct deep engagement analysis
- Synthesize findings

The thematic engines should probably extract prompt logic from these files rather than starting from scratch.

### Q3: Does genealogy's hybrid state (fetches from v2, executes locally) represent the target architecture or a waypoint?

If the target is full delegation to analyzer-v2's executor, then genealogy itself is incomplete. If the target is "definition-native but execution-hybrid," then genealogy is closer to done. The memo doesn't address this, but the answer changes what AOI parity means.

### Q4: Is the operationalization layer actually used by any live consumer today?

The executor code path is wired (`chain_runner.py:242-246`), but has a live consumer (The Critic genealogy, or any other app) actually triggered a job that exercised the operationalization fallback? Or is the code path real but untested end-to-end?

### Q5: Should the "catalog richness vs execution significance" distinction be made explicit in the platform's own vocabulary?

The memo, and possibly the team's mental model, conflates "has a rich definition in analyzer-v2" with "is execution-significant." Making this distinction first-class (e.g., a "readiness" or "execution-wired" flag per entity) would prevent future parity assessments from confusing metadata presence with behavioral depth.

### Q6: What is the actual user-facing value of closing this gap?

The memo is architecturally thorough but doesn't state who benefits and how. If The Critic's bespoke AOI works well for users today, the parity gap is an engineering concern, not a user-facing one. If the goal is to enable new AOI consumers (beyond The Critic), or to enable mixed AOI+genealogy workflows, the urgency changes.

---

## Methodology

This report is based on direct code inspection across three codebases:

| Codebase | Files Inspected | Key Paths |
|---|---|---|
| **analyzer-v2** | 30+ files | `src/objectives/`, `src/operationalizations/`, `src/workflows/`, `src/engines/`, `src/views/`, `src/orchestrator/`, `src/executor/`, `src/stages/`, `src/api/routes/` |
| **the-critic** | 8+ files | `analyzer/analyze_influence.py`, `analyzer/analyze_genealogy.py`, `api/server.py`, `webapp/src/pages/AnxietyOfInfluencePage.tsx`, `webapp/src/pages/GenealogyPage.tsx`, `webapp/src/components/V2TabContent.tsx` |
| **analyzer-mgmt** | 10+ files | `frontend/src/pages/objectives/`, `frontend/src/pages/operationalizations/`, `frontend/src/pages/workflows/`, `frontend/src/components/Layout.tsx`, `api/main.py`, `api/models/` |

All claims in this report are backed by specific file paths and line numbers identified during investigation. Inferences are marked as such.
