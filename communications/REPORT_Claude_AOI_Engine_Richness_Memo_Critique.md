# REPORT: Claude AOI Engine Richness Memo Critique

Date: 2026-03-16

Memo under review: `MEMO_2026-03-16_aoi_engine_richness_in_analyzer_mgmt_and_remaining_operationalization_program.md`

---

## 1. Thesis Verdict

**The memo's core thesis is architecturally correct but factually stale and structurally incomplete.**

The claim that analyzer-mgmt is generic and that the blocker is analyzer-v2 packaging is confirmed by code inspection. But the memo was written as if none of the recommended work had started, when in fact the current working tree already contains:

- 4 AOI operationalization YAMLs (untracked, `src/operationalizations/definitions/aoi_*.yaml`)
- 1 AOI objective definition (untracked, `src/objectives/definitions/influence_thematic.json`)

The memo also misses a critical architectural distinction: **the planner path is already capability-first**, while only the engine discovery/detail API is legacy-first. These are separate systems, and the memo treats them as one problem.

---

## 2. Confirmed Findings

### 2a. analyzer-mgmt IS structurally generic — CONFIRMED

Evidence from `analyzer-mgmt/frontend`:

- `src/pages/engines/[key].tsx` decides rendering path based on whether `capabilityDef` exists, not on category or workflow type. No hardcoded genealogy branches.
- `src/pages/implementations/[key].tsx` renders phases generically with null-safe optional chaining (`capDef?.problematique ?? ''`). Works with 0 phases or N phases, any workflow category.
- `src/lib/api.ts` treats genealogy as one `WorkflowCategory` among six (`synthesis | influence | outline | analysis | genealogy | decision_support`).
- No genealogy-specific components, no category-based filtering, no environment variable assumptions.

The frontend uses a dual-mode architecture: legacy tabs vs. capability tabs, decided entirely by data presence. If AOI engines had capability definitions visible on the API, they'd get the same rich rendering as genealogy engines automatically.

### 2b. Capability-only AOI engines ARE invisible on the engine list/detail API — CONFIRMED

Evidence from `src/engines/registry.py` and `src/api/routes/engines.py`:

- `registry._engines` (JSON) and `registry._capability_engines` (YAML) are separate dicts with separate loaders.
- `list_all()` returns `list(self._engines.values())` — JSON only.
- `get(engine_key)` returns `self._engines.get(engine_key)` — JSON only.
- `GET /v1/engines` (line 82) calls `registry.list_all()`. AOI thematic engines have no JSON files → not listed.
- `GET /v1/engines/{key}` (line 223) calls `registry.get(key)`. Returns None for AOI engines → 404.
- No fallback from `get()` to `get_capability_definition()` anywhere in the route handlers.

The only way to reach AOI engines is via the separate endpoint `GET /v1/engines/{key}/capability-definition`, which uses a different response schema (`CapabilityEngineDefinition` vs `EngineDefinition`).

### 2c. AOI capability definitions exist — CONFIRMED

Four files in `src/engines/capability_definitions/`:
- `aoi_thematic_synthesis.yaml`
- `aoi_engagement_mapping.yaml`
- `aoi_sin_findings.yaml`
- `aoi_thematic_report.yaml`

### 2d. Genealogy has fuller packaging — CONFIRMED

| Component | Genealogy | AOI Thematic |
|-----------|-----------|--------------|
| Workflows | 1 (5 phases) | 1 (4 phases) |
| Chains | 3 (10 engines total) | 0 |
| Capability defs | 2 dedicated + 20 shared engines | 4 |
| Operationalizations | 2 + 12 shared | 0 committed (4 untracked) |
| Legacy engine JSONs | 2 | 0 |
| Objectives | 1 (`genealogical.json`) | 0 committed (1 untracked) |

---

## 3. Overstatements or Weak Claims

### 3a. "AOI has no operationalization YAMLs" — STALE

The memo states this as current fact. But 4 AOI operationalization files already exist as untracked files in the working tree:

```
?? src/operationalizations/definitions/aoi_engagement_mapping.yaml
?? src/operationalizations/definitions/aoi_sin_findings.yaml
?? src/operationalizations/definitions/aoi_thematic_report.yaml
?? src/operationalizations/definitions/aoi_thematic_synthesis.yaml
```

These are well-formed (verified: `aoi_thematic_synthesis.yaml` has discovery/inference/integration stance operationalizations with focus_dimensions and focus_capabilities). So Step 2 of the memo's recommended program is **already substantially done** in the working tree, just uncommitted.

### 3b. The memo conflates the engine discovery API gap with the planner gap — MISLEADING

The memo implies that AOI being invisible on `GET /v1/engines` means AOI is invisible to the *whole system*. This is wrong.

The orchestrator/planner (`src/orchestrator/catalog.py`) builds its capability catalog from `registry.list_capability_definitions()`, NOT from `registry.list_all()`. This means:

- **AOI engines ARE already visible to the planner.** The planner reads only capability definitions (YAML), not legacy definitions (JSON).
- **AOI engines ARE already plannable.** An AOI plan can be generated today if you provide the right objective.
- **The gap is only on the discovery/detail API** consumed by analyzer-mgmt's engine list and engine detail pages.

This is a critical distinction the memo glosses over. The "engine API unification" needed is narrower than the memo suggests — it's a UI discovery problem, not a system-wide invisibility problem.

### 3c. "Only then revisit objective/planner parity" understates current readiness — WRONG ORDER

An AOI objective definition (`influence_thematic.json`) already exists as an untracked file. It has:
- `primary_goals`, `quality_criteria`, `planner_strategy`
- `baseline_workflow_key: "anxiety_of_influence_thematic_single_thinker"`
- `preferred_views: ["aoi_thematic_analysis"]`

So the memo's Step 4 is also already substantially done. The memo's proposed ordering (Steps 1→2→3→4) misrepresents what's been built.

### 3d. The memo overstates the "first-class on engine API" urgency relative to execution readiness

The memo frames engine API unification as Step 1 because it's the "most important hidden gap." But the *execution* path (planner → executor → capability_composer) already works with capability-only engines. The only consumer that needs legacy-style engine visibility is analyzer-mgmt's engine index page.

If the goal is *running AOI analyses*, the API unification is cosmetic. If the goal is *managing AOI engines via analyzer-mgmt*, it's necessary. The memo doesn't distinguish these goals.

---

## 4. Missing Considerations

### 4a. The `/src/aoi/` module is not mentioned

The memo ignores `src/aoi/contract.py` (28KB), which defines AOI's entire data model: sin types, finding structures, engagement mappings, fixture profiles. This is a substantial implementation layer that genealogy doesn't have (genealogy uses generic schemas). The AOI runtime is more specialized than the memo acknowledges.

### 4b. The legacy AOI workflow is broken, not just "not the right parity target"

`src/workflows/definitions/anxiety_of_influence.json` references 5 engines (`influence_pass1_*` through `influence_pass5_*`) that exist as legacy JSON stubs but have no capability definitions, no operationalizations, and no meaningful prompts. This workflow is dead code. The memo calls it "not the right parity target" — more precisely, it's non-functional.

### 4c. No discussion of the AOI contract test suite

`tests/test_aoi_contract.py` exists (modified in the working tree). The memo doesn't mention whether AOI's data contract is tested or how it relates to the operationalization work. This matters for assessing readiness.

### 4d. No discussion of view definitions for AOI

The memo mentions that analyzer-mgmt already shows workflow and implementation views, but doesn't inventory whether AOI-specific view definitions exist in `src/views/definitions/`. Without AOI views, the presenter layer can't render AOI results even if the engine/operationalization/chain layers are complete.

### 4e. The memo doesn't distinguish "legacy engine JSON" from "engine definition with full stage_context"

Some legacy JSON engines in `src/engines/definitions/` are rich (full prompts, stage_context, canonical_schema). Others are stubs. The memo treats all 123+ legacy engines as equivalent, but the richness gap between a well-defined legacy engine and a capability-only engine is not uniform.

---

## 5. Best Alternative Framing

The memo's framing is:

> "AOI is packaged as workflow + capability defs, while genealogy is packaged as engine + operationalization + chain."

This is correct but incomplete. A better framing:

**There are three independent API surfaces in analyzer-v2, and AOI has different visibility on each:**

| Surface | What it serves | AOI status |
|---------|---------------|------------|
| **Engine discovery API** (`/v1/engines`) | analyzer-mgmt engine index/detail | INVISIBLE — no legacy JSON, no fallback |
| **Capability catalog** (orchestrator) | Planner plan generation | VISIBLE — 4 YAML capability defs loaded |
| **Execution path** (executor) | Running analyses | FUNCTIONAL — capability_composer handles AOI engines, operationalizations exist (uncommitted) |

The memo treats these as one problem. They're three problems with different urgency:

1. **Execution readiness**: Mostly done (capability defs + operationalizations + objective exist, just uncommitted)
2. **Planner readiness**: Done (catalog already sees AOI capability engines)
3. **Management UI discoverability**: Not done (engine list/detail API still legacy-only)

The right framing is: **AOI is execution-ready but management-invisible.** The packaging gap is narrower than the memo claims.

---

## 6. Recommended Corrections To The Memo

1. **Update the inventory.** The memo says "AOI has no operationalizations" and "only then revisit objective/planner parity." Both are now false. Acknowledge the 4 untracked operationalizations and the untracked objective definition, and resequence accordingly.

2. **Distinguish the three API surfaces.** The memo's "engine API path" discussion conflates analyzer-mgmt discoverability with planner/executor readiness. Separate them.

3. **Reframe Step 1.** "Make capability-only engines first-class on the engine API path" is the right step, but it should be framed as a *management UI discoverability* fix, not as a prerequisite for execution. AOI analyses can already run without this step.

4. **Acknowledge `/src/aoi/contract.py`.** This module means AOI has a dedicated runtime data model that genealogy doesn't need. The memo's "AOI is packaging-thin" claim understates AOI's implementation depth.

5. **Mark the legacy AOI workflow as dead code.** Don't call it "not the right parity target" — call it non-functional and recommend deletion or archival.

6. **Add a Step 0: commit the existing untracked work.** Before planning new work, the 4 operationalizations, 1 objective, and any related changes should be committed and deployed. Otherwise the memo is planning work that's already done.

---

## 7. Recommended Next Move

Given what actually exists in the working tree, the correct program is:

### Step 0: Commit existing work (immediate)
- Commit and push the 4 AOI operationalization YAMLs
- Commit and push `influence_thematic.json` objective
- Commit and push any related test changes (`test_aoi_contract.py`)
- Deploy to Render

### Step 1: Unify engine discovery API (the only real remaining gap)
- Modify `GET /v1/engines` to include capability-only engines alongside legacy engines
- Modify `GET /v1/engines/{key}` to fall back to capability definition if no legacy JSON exists
- Decision point: return a unified response model, or return `CapabilityEngineDefinition` directly?
- This is purely a management UI fix — execution doesn't depend on it

### Step 2: Verify AOI operationalizations work end-to-end
- Run a test AOI plan generation using the `influence_thematic` objective
- Execute the plan and verify that `capability_composer.compose_all_pass_prompts()` picks up the AOI operationalizations
- Verify that the presenter can render results (check if AOI view definitions exist)

### Step 3: Decide on AOI chains (design review)
- The memo's Step 3 is correctly deferred. AOI's 4-phase workflow is cleanly bounded.
- Chains would only matter if individual phases need multi-engine composition, which the current AOI design doesn't require.

### Step 4: Clean up dead code
- Archive or delete `anxiety_of_influence.json` (legacy 5-pass workflow)
- Archive or delete the 5 `influence_pass*` legacy engine stubs

**Bottom line: the memo is directionally correct but is planning work that's partially already done. Commit the existing work first, then the only engineering task is engine API unification for management UI discoverability.**
