# Proof: Stage 7 / AOI Source-To-Composition Bridge

Date: 2026-03-23  
Program: Dynamic Bespoke Apps Platformization  
Scope Memo: `communications/MEMO_2026-03-23_stage7_planner_to_presentation_bridge_scope.md`

## Claim

Stage 7 set out to prove one bounded thing:

- analyzer-v2 can replace hardcoded AOI `profile -> sections` assembly behind `POST /v1/presenter/compose-from-source` with an analyzer-owned source-to-composition bridge that resolves an explicit AOI composition source catalog, selects sources with rationale, materializes deterministic sections, and preserves the public consumer contract

This proof note records the code and focused verification evidence for that claim.

## What Landed

The new bridge is implemented in:

- `src/presenter/composition_source_bridge.py`

The existing source-backed compose path now calls that bridge from:

- `src/presenter/compose_from_intent.py`

The bridge now does all of the following:

1. resolves all expected AOI source families eagerly
2. records per-candidate state as:
   - `available`
   - `unavailable`
   - `invalid`
3. keeps candidate-state capture non-throwing during catalog build
4. distinguishes:
   - artifact-backed AOI sources
   - thematic-report phase-output lookup
   - normalized thematic-report payload materialization
5. applies preset-relative selection for:
   - `dossier`
   - `comparison`
6. records selected and rejected source families with rationale
7. materializes deterministic compose sections in explicit order
8. stamps the source-backed resolver path as:
   - `compose-from-source-v2`
9. prepends bridge trace stages:
   - `source_catalog_resolution`
   - `source_selection`
   - `section_materialization`

## Focused Verification Evidence

### Analyzer verification

Commands run:

- `python -m py_compile src/presenter/composition_source_bridge.py src/presenter/compose_from_intent.py tests/test_composition_source_bridge.py tests/test_compose_from_intent.py`
- `PYTHONPATH=. pytest tests/test_composition_source_bridge.py tests/test_compose_from_intent.py -q`

Observed result:

- compile: clean
- pytest: `20 passed, 2 warnings`

The focused analyzer tests now prove:

- eager catalog resolution over all four AOI families
- non-throwing candidate-state capture during catalog build
- preset-relative requiredness
- deterministic latest thematic-report resolution
- deterministic section materialization order
- `compose-from-source-v2` resolver stamping
- new bridge trace stages
- live-source truth winning over contradictory plan metadata
- merged plan/request-snapshot `objective_key` fallback when effective plan context is missing

### Cross-repo compatibility verification

Because Stage 7 changed the source-backed resolver version, one cross-repo contract pin also had to move.

Command run:

- `cd /home/evgeny/projects/the-critic/webapp && CI=true npm test -- --watch=false src/pages/AoiComposeFromIntentPage.test.tsx`

Observed result:

- `15 passed`

That confirms the Stage 7 resolver-version bump does not break the existing transient page contract expected by the-critic tests.

## What This Proof Does Not Claim

This proof does **not** claim:

1. full planner-to-page-law integration
2. open-ended task intake
3. workflow routing without manual workflow identity
4. cross-workflow source-backed composition
5. richer semantic page planning
6. new consumer runtime behavior

It also does not record a new live browser proof because Stage 7 did not change the the-critic runtime path itself.
The public route and consumer-facing shape stayed stable.
This was an analyzer-side bridge replacement and trace/version change.

## Verdict

The bounded Stage 7 claim is proven at the code-and-contract level:

- `compose-from-source` no longer depends on inline hardcoded AOI section assembly
- analyzer-v2 now owns a real AOI source-to-composition bridge contract behind that route
- the public consumer contract remained stable while the internal bridge became explicit and traceable

This advances roadmap Stage 7 from:

- not started

to:

- partial

It does **not** close the broader planner-to-presentation stage by itself.
