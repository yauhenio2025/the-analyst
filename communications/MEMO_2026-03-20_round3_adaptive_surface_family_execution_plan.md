# Memo: Round 3 / Adaptive Surface Family Execution Plan

Date: 2026-03-20
Program: Thin Consumer Platformization
Scope Memo: `communications/MEMO_2026-03-20_round3_adaptive_surface_family_scope.md`

## Purpose

Turn the revised round-3 scope into an execution plan against the code that already exists.

This is not a greenfield build plan.

An adaptive implementation spike already landed in analyzer-v2. The job now is:

1. audit that spike against the revised bounded claim
2. trim or ratify any overreach
3. backfill the missing adaptive-specific proof coverage
4. close the stage with manual evidence and a short proof note

## Current Starting Point

### Already in code

The adaptive spike already provides:

- `composition_mode=adaptive_relationship_surface_v1`
- a bounded target surface:
  - `genealogy_relationship_landscape`
- three concrete runtime surface families in:
  - `src/presenter/bounded_dynamic_composition.py`
- deterministic selection over transformed per-item relationship cards
- one adaptive trace stage:
  - `adaptive_surface_selection`
- focused analyzer-v2 tests for family selection and trace visibility

The Critic host is already composition-mode-aware generically because of round-2 work:

- `AnalysisWorkspacePage` reads `composition_mode`
- the bounded-v2 client threads it to manifest/presentation/refresh/single-view
- the restore path is freshness-sensitive to `composition_mode`
- proof-mode cache warming is already disabled generically

### What is not yet closed

The main remaining gaps are not architectural. They are proof and delta gaps:

1. adaptive-specific route/result-contract coverage is still thinner than bounded-dynamic coverage
2. frontend tests are still written around `bounded_dynamic_genealogy_v1`, not the new adaptive mode
3. no round-3 manual contrast-job proof has been recorded yet
4. no round-3 completion/proof note exists yet

## Execution Strategy

Execute round-3 as a **ratify-and-close tranche**, not a fresh invention tranche.

That means:

1. keep the current adaptive target
2. keep the current three family contracts unless an audit shows one should be trimmed
3. avoid new host code unless a failing test proves it is required
4. spend most of the work on proof tightening, not new scope expansion

## Work Packages

## WP1: Ratify The Current Adaptive Contract

Goal:

- decide whether the existing adaptive spike matches the revised scope closely enough to keep

Files to inspect and, only if necessary, adjust:

- `src/presenter/bounded_dynamic_composition.py`
- `src/presenter/decision_trace.py`
- `src/presenter/presentation_api.py`

Checks:

1. the mode remains independent:
   - `adaptive_relationship_surface_v1` must not stack on `bounded_dynamic_genealogy_v1`
2. the selector reads:
   - `genealogy_relationship_landscape.items[*].structured_data`
   - not raw prose
3. the three family contracts stay concrete and visually distinct:
   - dossier = `accordion`
   - comparison = `table`
   - field map = `accordion`
4. the adaptive surface remains the only runtime-rewritten surface in this mode
5. validation still fails closed and leaves diagnostics visible

Default recommendation:

- ratify the current three families as the round-3 proof contract
- do not reopen family count unless a real review shows the middle family is unusably ambiguous

## WP2: Backfill Adaptive-Specific Analyzer-v2 Proof Coverage

Goal:

- make the analyzer-v2 proof evidence as explicit for adaptive mode as it already is for bounded-dynamic mode

Files:

- `tests/test_presentation_api.py`
- `tests/test_manifest_trace.py`
- `tests/test_analysis_product_contract.py`

Required additions:

### A. Result-manifest / result-presentation / refresh coverage for adaptive mode

Current route-threading tests mostly assert `composition_mode` with:

- `bounded_dynamic_genealogy_v1`

Backfill the same contract using:

- `adaptive_relationship_surface_v1`

Required assertions:

1. result-manifest links preserve the adaptive mode
2. result-presentation threads the adaptive mode into manifest + page assembly
3. refresh-presentation threads the adaptive mode into manifest + page assembly
4. single-view route threads the adaptive mode

### B. Adaptive invalid-path coverage

The current focused tests prove:

- successful selection into all three families
- fail-closed behavior when structured relationship cards are missing

Backfill at least one more adaptive invalid-path test that proves:

1. a runtime family with an invalid renderer/data contract returns `409` at route level
2. trace still returns `200` and shows:
   - `composition_status = invalid`
   - adaptive-stage diagnostics
   - authored pre-composition final manifest retained

### C. Adaptive manifest diff / trace evidence

Extend trace tests so they prove not just stage presence, but the shape of change:

1. authored baseline remains `Relationship Landscape` with `card_grid`
2. adaptive mode can produce:
   - `Relationship Dossier` with `accordion`
   - or another selected family depending on fixture
3. the final manifest reflects the adaptive family only in proof mode

## WP3: Add Minimal Generic-Host Regressions For Adaptive Mode

Goal:

- prove that the Critic generic host consumes adaptive mode without any new workflow-specific behavior

Files:

- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/AnalysisWorkspacePage.integration.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/hooks/useBoundedV2Workspace.test.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.test.ts`

Keep this narrow. Do not add new host code unless a test proves it is required.

Required additions:

1. one page test using:
   - `composition_mode=adaptive_relationship_surface_v1`
   - assert the generic proof label appears
   - assert restore succeeds when the returned view name is `Relationship Dossier` or `Relationship Field Map`
2. one hook/client test proving adaptive mode is treated the same as any other proof mode for:
   - manifest threading
   - snapshot freshness matching
   - skip-cache behavior
3. if needed, one integration test showing a proof-mode adaptive restore reaches the returned family contract without host branching

The important rule here:

- prove the host stays generic
- do not rewrite the host for a backend proof that is already data-driven

## WP4: Manual Contrast-Job Proof

Goal:

- produce the real human evidence the scope memo expects

Manual route:

- `/p/:projectId/analysis/intellectual_genealogy?composition_mode=adaptive_relationship_surface_v1`

Required operator checks:

1. one authored genealogy restore without proof mode
2. one proof-mode genealogy restore for a dominant-field case
3. one proof-mode genealogy restore for a distributed/comparison case
4. one trace inspection per proof-mode job

Preferred contrast pair:

- Markus-like job
- Varoufakis-like job

But the real requirement is not those names specifically.
It is:

- two known genealogy jobs that actually produce different selected families on the same route

Record for each:

- job id
- route used
- selected family
- trace rationale

## WP5: Round-3 Proof Note

Goal:

- close the stage cleanly once the adaptive proof is verified

Create one short proof/closure memo after WP2-WP4 pass.

It should record:

1. exact route used
2. target surface:
   - `genealogy_relationship_landscape`
3. the contrast jobs used
4. the selected family for each
5. the bounded claim being made
6. focused test results
7. manual operator result

Do not let this balloon into another broad roadmap memo.

## Acceptance Checklist For Execution

Treat execution as complete only if all of the following are true:

1. the current adaptive spike is ratified or minimally trimmed to match the revised scope
2. adaptive route/result-contract coverage exists, not just bounded-dynamic coverage
3. adaptive invalid-path and trace-invalid-path behavior are covered explicitly
4. the Critic generic host has at least one adaptive-mode regression proving generic consumption
5. two contrast genealogy jobs are shown to select different families on the same generic route
6. a short round-3 proof note is written

## What Not To Do During Execution

Do not:

- reopen round-2 hierarchy work
- widen to AOI
- add a second adaptive surface in the same tranche
- turn selector thresholds into overclaimed platform doctrine
- add workflow-specific host behavior unless a failing test leaves no alternative
- restart another broad memo cycle before checking the current adaptive code against this plan

## Recommended Immediate Next Step

Start with WP1 and WP2 together:

- audit the current adaptive spike against the revised scope
- patch only the mismatches
- then backfill the missing adaptive-specific analyzer-v2 proof coverage

Only after that should the work move to Critic regressions and manual proof capture.
