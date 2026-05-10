# Report: Phase E Bridge Hint Consolidation V1 Scope Audit

## 1. Verdict

**Approve with corrections.**

The memo is directionally right. After the April 1 extraction closeout, the next honest analyzer-side slice is still one behavior-preserving bridge-hint consolidation step, not analyzer-side affordance/routing attachment, not lifecycle broadening, and not broader output-family taxonomy work. But the memo should be tightened in two places:

- the duplicated seam is real, but it is less operationally dangerous than the memo implies because the current codebase already keeps those literals aligned with capability metadata through focused tests
- the proposed helper should probably be a thin validated bridge-role resolver built on top of existing alias-aware capability discovery, not a new metadata-return subsystem

## Short Answers To The Prompt Questions

- **Is bridge-hint consolidation the right immediate next analyzer-side slice after extraction?**
  - Yes.
- **Does the memo correctly identify the remaining duplicated authority seam?**
  - Mostly yes. In live source code, the remaining migrated semantic-role literals are in `src/presenter/composition_source_bridge.py` and `src/orchestrator/genealogy_saved_result_bridge.py`.
- **Is it correct to keep analyzer-side affordance/routing attachment out of scope for one more bounded step?**
  - Yes.
- **Does the helper really need canonical capability resolution for both canonical and legacy keys?**
  - Yes for genealogy alias handling, but it should reuse `src/engines/discovery.py` instead of inventing a new lookup mechanism.
- **Are the AOI and genealogy bridge seams the right exact targets?**
  - Yes.
- **Is fail-closed behavior for missing or invalid metadata on migrated bridge-backed keys the right bar?**
  - Yes.
- **Does the memo preserve output shapes and proof surfaces honestly enough?**
  - Yes, with the caveat that the change is authority cleanup, not user-visible behavior change.
- **Is there a smaller and stronger immediate slice than this one?**
  - Not at the scope level. There is only a smaller implementation shape: reuse existing alias-aware discovery and add a thin validated bridge-role helper.
- **What should change in roadmap ordering?**
  - No major reordering. Insert this as the narrow post-extraction Phase E sub-slice, then do the first-hop affordance/routing addendum.

## 2. The Memo's Strongest Code-Backed Points

- `src/presenter/compose_from_intent.py` no longer carries a `_ROLE_FROM_ENGINE_KEY` authority map. For migrated AOI and genealogy keys, `_resolve_semantic_role(...)` now checks bridge hints first, then canonical capability metadata via `resolve_capability_definition(...)`, and fails closed when migrated-family metadata is missing or invalid. That makes the bridge literals the last remaining live duplicate authority seam, not one of many.

- The exact duplicate seam is real in code:
  - `src/presenter/composition_source_bridge.py:45-69` hard-codes `composition_role_hint` for the four migrated AOI source families.
  - `src/presenter/composition_source_bridge.py:559-733` repeatedly re-emits those hard-coded values into `CompositionSourceCandidate`.
  - `src/orchestrator/genealogy_saved_result_bridge.py:33-49` hard-codes `role_hint` for the two genealogy section specs, including legacy aliases.

- The memo is right that affordance/routing attachment should wait one more bounded step. The completed product-side inventory is evidence, not contract, and the current analyzer-side code still treats semantic role as the immediate presentation-law seam:
  - `src/presenter/compose_from_intent.py:734-755`
  - `src/presenter/composition_role_registry.py:18-58`

- The AOI and genealogy seams are the right exact targets. A repository scan did not show any other live source files hard-coding migrated role hints besides those two bridge modules. The other role hits are:
  - canonical `composition_role` metadata in capability YAMLs
  - presenter role-registry entries
  - heuristic fallback tokens for non-migrated cases
  - generated artifacts and stored traces, which are outputs, not live authority

- The fail-closed bar is consistent with the extraction tranche. For migrated families, the matcher already fails closed on missing or invalid `composition_role` metadata in `src/presenter/compose_from_intent.py:766-780`, and genealogy lowering already treats role drift as an error in `src/orchestrator/direct_sections_compose_harness.py:43-54`.

## 3. The Memo's Weakest Or Overstated Assumptions

- The memo slightly overstates the immediate correctness risk. The duplicate bridge literals are real, but they are already guarded by tests:
  - `tests/test_compose_from_intent.py:1799-1817` asserts AOI source-bridge role hints match capability metadata.
  - `tests/test_genealogy_saved_result_bridge.py:121-133` asserts genealogy bridge role hints match canonical and legacy capability resolution.
  - `tests/test_genealogy_saved_result_bridge.py:110-118` plus `src/orchestrator/direct_sections_compose_harness.py:43-54` already fail if genealogy bridge-emitted `role_hint` would diverge from the semantic matcher.

  So the real problem is remaining duplicate authority and maintenance burden, not an entirely unguarded runtime hole.

- The memo over-specifies the helper shape. The repository already has canonical-or-legacy capability lookup in `src/engines/discovery.py:59-71`, and adjacent seams already use it:
  - `src/presenter/compose_from_intent.py:766`
  - `src/presenter/dynamic_prompt.py:75`
  - `src/views/generator.py:27-58`

  The needed helper is therefore narrower than the memo suggests: one bridge-facing resolver that reuses `resolve_capability_definition(...)`, validates `composition_role`, and returns a single allowed role.

- The memo should state more explicitly that the alias requirement matters mainly for genealogy. AOI source-bridge families already point at canonical engine keys. The canonical-or-legacy requirement is necessary because genealogy saved results and tests still support:
  - `genealogy_pass1b_relationship_classification`
  - `genealogy_pass7_final_synthesis`

- The memo should keep the fail-closed requirement scoped to migrated bridge-backed keys only. The extraction tranche deliberately preserved heuristic fallback for non-migrated engines, and this slice should not silently widen migrated-family strictness into a global bridge policy.

## 4. Factual Discrepancies I Found

- The memo implies a new canonical-or-legacy metadata helper needs to be created from scratch. That is not factually true. The codebase already has alias-aware canonical capability resolution in `src/engines/discovery.py:59-71`.

- The memo implicitly treats the duplicate seam as if it were still a broader presenter-level authority issue. That is no longer accurate after extraction. `src/presenter/compose_from_intent.py:759-782` already resolves migrated semantic role from canonical capability metadata when bridge hints are absent, and role-level pattern/stance/description/rationale law already lives in `src/presenter/composition_role_registry.py:18-58`.

- I did not find any additional live migrated semantic-role literal seam in source code beyond:
  - `src/presenter/composition_source_bridge.py`
  - `src/orchestrator/genealogy_saved_result_bridge.py`

  On that point, the memo is accurate rather than incomplete.

## 5. What This Changes For The Larger Roadmap

- It does not justify a roadmap reorder. The larger order remains:
  1. extraction closeout
  2. bridge-hint consolidation
  3. bounded analyzer-side affordance/routing addendum over first-hop operations only

- The April 1 roadmap stack is already broadly aligned with that order:
  - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
  - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
  - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
  - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`

- The only roadmap correction I would make is to describe this slice more narrowly:
  - not “new capability metadata plumbing”
  - not “begin affordance law”
  - but “remove the final bridge-local migrated role literals by deriving them from already-landed canonical metadata”

- The Close Read inventory still changes rationale, not order. It gives the later affordance/routing tranche a better evidence base, but it does not outrank this consolidation step.

## 6. The Most Defensible Next Move After This Memo

- Approve one analyzer-side bridge-hint consolidation slice targeting only:
  - `src/presenter/composition_source_bridge.py`
  - `src/orchestrator/genealogy_saved_result_bridge.py`

- Implement it with the smallest honest mechanism:
  - reuse `resolve_capability_definition(...)`
  - add one thin validated helper that returns a legal `composition_role` for a canonical or legacy engine key
  - derive emitted `composition_role_hint` / `role_hint` from that helper
  - fail closed when migrated bridge-backed metadata is missing or invalid

- Keep everything else fixed:
  - no host changes
  - no harness changes
  - no route changes
  - no request/response shape changes
  - no new affordance/routing fields yet
  - no broader bridge redesign

- Preserve the current proof surfaces and add only focused verification:
  - AOI bridge hints are derived from canonical metadata
  - genealogy bridge hints are derived from canonical metadata for both canonical and legacy keys
  - missing/invalid metadata on migrated bridge-backed keys fails closed
  - representative matrix, transient proof harness, and compose-session tests remain unchanged

## Verification

Focused verification against the cited surfaces passed locally:

- `PYTHONPATH=. pytest -q tests/test_composition_source_bridge.py tests/test_genealogy_saved_result_bridge.py tests/test_compose_from_intent.py tests/test_representative_composition_matrix.py tests/test_transient_proof_harness_contract.py tests/test_compose_sessions.py`
  - `72 passed, 2 warnings`
