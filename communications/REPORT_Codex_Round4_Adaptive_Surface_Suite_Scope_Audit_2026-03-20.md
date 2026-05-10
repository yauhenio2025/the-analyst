# Audit: Round 4 / Adaptive Surface Suite Scope

Date: 2026-03-20
Memo under review: `communications/MEMO_2026-03-20_round4_adaptive_surface_suite_scope.md`

## Findings

### 1. The proposed `genealogy_conditions` families are still not contract-complete enough to implement fail-closed validation

The memo is directionally right about the target, but the runtime family contracts are still too loose at the renderer/data-mapping level.

- `conditions_balance_sheet` names renderers, but it does not specify the actual field mappings needed for `mini_card_list` and `key_value_table`. In the current schema, enabling rows expose fields like `description`, `condition_type`, `essentiality`, `how_it_enables`, while constraining rows expose `description`, `constraint_type`, `binding_force`, `how_navigated` (`src/engines/definitions/conditions_of_possibility_analyzer.json:11-32`; `src/views/definitions/genealogy_cop_enabling_conditions.json:9-35`; `src/views/definitions/genealogy_cop_constraining_conditions.json:9-35`).
- `conditions_path_dependency_matrix` is more under-specified. The proposed columns are not a direct fit for the current structured payloads. `path_dependencies` rows provide `description`, `chain`, `if_absent`, `is_acknowledged`; `alternative_paths` rows provide `branching_point`, `path_not_taken`, `why_not_taken`, `implications`; debts rows provide `creditor_work`, `what_is_owed`, `possible_reasons` (`src/engines/definitions/conditions_of_possibility_analyzer.json:34-71`; `src/views/definitions/genealogy_cop_path_dependencies.json:9-22`; `src/views/definitions/genealogy_cop_alternative_paths.json:9-29`; `src/views/definitions/genealogy_cop_unacknowledged_debts.json:9-29`).
- That means columns like `source_work_or_chain`, `stakes`, and `acknowledged` require explicit normalization rules. Without those rules, “validate and fail closed” becomes weak, because the current table validator only checks for generic row-object shape, not semantics (`src/renderers/definitions/table.json:7-79`).

This is the main execution-readiness gap. The memo needs exact field-level contracts and selector thresholds, not just family labels plus intended reading shapes.

### 2. The signals for `genealogy_conditions` are available without a new inference pass, but the memo points at the wrong seam

The strongest signal source is not a re-aggregation of child payloads. It is the existing top-level `genealogy_conditions` payload itself.

- The parent view already targets the full engine output with `result_path = ""` on the aggregated `conditions_of_possibility_analyzer` payload (`src/views/definitions/genealogy_conditions.json:71-76`).
- The child views are thin slices of that same blob via specific `result_path` keys like `enabling_conditions`, `path_dependencies`, and `synthetic_judgment` (`src/views/definitions/genealogy_cop_enabling_conditions.json:30-35`; `src/views/definitions/genealogy_cop_path_dependencies.json:17-22`; `src/views/definitions/genealogy_cop_synthesis.json:14-19`).
- In presenter assembly, `_build_view_payload()` loads the parent aggregated structured data directly and only applies `result_path` slicing when a view actually declares a non-empty result path (`src/presenter/presentation_api.py:1637-1665`).
- `genealogy_conditions` is also not one of the chain-container parents whose root payload is deferred to child synthesis. That path only applies when a view has `chain_key` and no `engine_key` (`src/presenter/view_hierarchy.py:24-35`).
- The engine schema already exposes the useful summary fields the memo cares about, including counts and `overall_balance`, inside `meta` (`src/engines/definitions/conditions_of_possibility_analyzer.json:63-71`).

So the answer to question 1 is yes: the needed signals already exist in current structured payloads. But the smallest and strongest implementation seam is `payloads["genealogy_conditions"].structured_data`, with child payloads as optional convenience views, not as the primary aggregation source.

### 3. The generic host can stay generic in rendering terms, but not literally unchanged

The core host boundary is still sound. A second adaptive surface does not require workflow-specific rendering logic.

- `composition_mode` is already threaded generically through result links and manifest/presentation/refresh routes (`src/analysis_products/result_contract.py:220-237`; `src/analysis_products/result_contract.py:273-315`; `src/api/routes/results.py:44-116`; `src/api/routes/presenter.py:142-287`).
- The Critic client and workspace hook also treat `composition_mode` as an opaque token and use it consistently for manifest reads, presentation restore, refresh, and single-view loading (`/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts:117-165`; `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:74-76`; `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:165-205`; `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.ts:233-318`).
- `V2TabContent` already works from the returned tree and `source_parent_view_key`, so preserving the same view keys for `genealogy_relationship_landscape` and `genealogy_conditions` keeps the host generic (`/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:238-255`; `/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:963-987`).

But two small codepaths are still hard-coded around the current proof shape:

- The header proof label in `AnalysisWorkspacePage` only knows two explicit composition-mode values today (`/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:77-87`; `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:790-793`).
- The trace-stage reason builder still assumes one `selected_family` rather than a per-surface decision list (`src/presenter/decision_trace.py:214-235`).

So the host can stay generic in the important sense, but the memo should not describe it as literally unchanged.

### 4. The proposed proof token is workable, but it is broader than the current code’s contract style

The current system does not have a reusable “suite” abstraction. It has explicit proof-mode enums.

- Backend composition dispatch is a closed set of named constants (`src/presenter/bounded_dynamic_composition.py:14-26`; `src/presenter/bounded_dynamic_composition.py:199-229`).
- The frontend proof label is also per-token, not generic (`/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.tsx:77-87`).

Because of that, `composition_mode=adaptive_genealogy_surface_suite_v1` will work technically, but it overstates what the current contract means. A narrower token such as `adaptive_genealogy_relationship_conditions_v1` would fit the actual implementation pattern better and avoid implying a reusable suite framework that does not exist yet.

## Open Questions / Weak Assumptions

### 1. Should the conditions selector use `meta` when present, or derive everything from section arrays?

The top-level engine schema already includes `meta.enabling_conditions_count`, `meta.constraining_conditions_count`, `meta.path_dependencies_count`, and `meta.overall_balance` (`src/engines/definitions/conditions_of_possibility_analyzer.json:63-71`). Using those fields is the smallest path. If the program wants the selector to stay independent of engine-side summary drift, the memo should say so explicitly and require array-derived fallbacks.

### 2. Should `genealogy_conditions` keep all current child views visible as deep dives under the adaptive family?

The existing host already knows how to expose linked children generically (`/home/evgeny/projects/the-critic/webapp/src/components/V2TabContent.tsx:238-255`). If round 4 keeps adaptation bounded to the top-level parent payload and preserves child availability, host risk stays low. If the proof starts removing or re-parenting the child views, that is a larger contract change than the memo currently acknowledges.

### 3. A suite-level trace stage is the right shape, but it should carry per-surface decisions explicitly

`DecisionTraceEntry.details` is already flexible enough to hold a structured decision list (`src/presenter/schemas.py:372-398`). The clean shape is one `adaptive_surface_suite_selection` stage with something like `surface_decisions[]`, each block keyed by `target_surface`. Reusing the round-3 singular `selected_family` semantics will get awkward immediately.

## What The Memo Gets Right

### 1. The next missing variable really is coordinated multi-surface adaptation on the same generic route

The memo is correct that round 1 proved the boundary, round 2 proved bounded regrouping, and round 3 proved one adaptive surface family. The next meaningful question is whether two high-leverage surfaces can vary together without reopening host-specific logic.

### 2. `genealogy_conditions` is the right second target

I do not see a stronger smaller target in the real codebase.

- `genealogy_tactics` is smaller, but it is another single `card_grid` over one list (`src/views/definitions/genealogy_tactics.json:9-110`). That would give a weaker proof of coordinated page-level divergence.
- `genealogy_idea_evolution` is more central and more entangled with secondary sources and child tabs (`src/views/definitions/genealogy_idea_evolution.json:15-36`), so it is a riskier tranche.
- `genealogy_conditions` already has rich multi-regime structured output and existing renderer diversity (`src/views/definitions/genealogy_conditions.json:9-69`; `src/engines/definitions/conditions_of_possibility_analyzer.json:11-71`).

### 3. No new inference pass is needed

That is the right discipline. The current relationship and conditions payloads already expose enough structured signal for deterministic selection (`src/presenter/bounded_dynamic_composition.py:392-457`; `src/engines/definitions/conditions_of_possibility_analyzer.json:11-71`).

### 4. A single suite-level trace stage is cleaner than separate per-surface stages

For this bounded proof, one runtime-composition stage with per-surface decisions is cleaner and lower-risk than pretending the two surface rewrites are separate sequential passes.

## Verdict

The memo is pointed in the right direction and chooses the right second target, but it still needs tightening before it is execution-ready. The key revisions are: use the top-level `genealogy_conditions` payload as the primary signal source, define exact field mappings and deterministic thresholds for both conditions families, and acknowledge the small trace/label updates implied by a new proof token. With those corrections, the scope becomes a credible bounded round-4 proof.
