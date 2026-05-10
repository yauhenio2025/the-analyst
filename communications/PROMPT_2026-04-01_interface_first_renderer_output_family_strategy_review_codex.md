# Prompt For Fresh Codex Session

Review this strategy memo critically:

- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`

You are not being asked to restate it.
You are being asked to audit whether it is technically and strategically sound.

## Required tasks

1. Read the memo.
2. Verify its claims against the actual codebase.
3. Check relevant recent roadmap and completion memos in `communications/`.
4. Stress-test the memo’s assumptions against the program’s larger objective:
   - analyzer-v2 as the brain
   - thin hosts
   - faster bootstrap of new analytical apps/sites without per-engine host architecture

## Code areas to inspect

At minimum, inspect:

- `src/renderers/schemas.py`
- `src/renderers/definitions/`
- `src/renderers/validator.py`
- `src/consumers/schemas.py`
- `src/consumers/registry.py`
- `src/presenter/manifest_builder.py`
- `src/presenter/compose_from_intent.py`
- `src/views/generator.py`

Also inspect any adjacent code you think materially changes the memo’s truth conditions.

## Context docs to inspect

At minimum, inspect:

- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_v1_completion.md`

## Audit questions

Please answer these concretely:

1. Does the current codebase support the memo’s claim that the problem may be better attacked from the renderer/interface side rather than from per-engine app architecture?
2. Is the existing renderer catalog actually small and stable enough to make this plausible?
3. Does current composition law already look like it could be generalized into output-family / placement-family contracts, or is it still too workflow-shaped?
4. Is “one extra LLM call to fit data into the interface” a sound framing, or does it hide major validation and stability risk?
5. What are the memo’s biggest unstated assumptions?
6. If the memo is directionally right, what concrete next tranche would you recommend?

## Output file

Write your audit to this exact file:

- `communications/REPORT_Codex_Interface_First_Renderer_Output_Family_Strategy_Audit_2026-04-01.md`

## Expected structure

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. Findings, ordered by importance
3. Code-backed confirmations
4. Overstatements or missing risks
5. Strategic recommendation

Be direct.
Avoid generic praise.
