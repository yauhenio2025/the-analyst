# Prompt For Fresh Claude Session

Please review this memo critically:

- `communications/MEMO_2026-04-01_interface_first_renderer_output_family_strategy.md`

Your task is not to agree with it by default.
Your task is to test whether the memo’s assumptions and strategic framing are actually robust.

## What to do

1. Read the memo carefully.
2. Examine its assumptions in light of the larger program objective:
   - analyzer-v2 becomes the brain
   - downstream apps become thin hosts
   - new apps/sites should become easier to bootstrap from analyzer-owned analytical and presentation law
3. Scrutinize the memo against the actual codebase, especially:
   - `src/renderers/schemas.py`
   - `src/renderers/definitions/`
   - `src/renderers/validator.py`
   - `src/consumers/schemas.py`
   - `src/presenter/manifest_builder.py`
   - `src/presenter/compose_from_intent.py`
   - `src/views/generator.py`
   - any other nearby files you think materially affect the memo’s claims
4. Read recent roadmap/completion context in `communications/` that is relevant, especially:
   - `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
   - `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
   - `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
   - `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
   - `communications/MEMO_2026-04-01_phase_e_proof_only_lifecycle_source_selection_v1_completion.md`
5. Decide whether the memo is:
   - directionally right
   - overstated
   - missing key risks
   - skipping a smaller/better next framing

## What to focus on

- Is the “limited interface family” assumption actually supported by the codebase and recent proof line?
- Does the memo correctly distinguish:
  - renderer families
  - output families
  - composition law
  - lifecycle law
- Is “bounded LLM projection into strict schemas” realistic here, or is that still too hand-wavy?
- Does the memo understate how much workflow-specific logic is still encoded in current composition?
- If this strategy is adopted, does it move us toward analyzer-v2-as-brain, or risk creating a new soft layer of LLM glue?
- Is there a better way to frame the next generalization tranche?

## Output requirements

Write a critique memo to this exact file:

- `communications/REPORT_Claude_Interface_First_Renderer_Output_Family_Strategy_Critique_2026-04-01.md`

Please include:

1. Verdict:
   - approve
   - approve with corrections
   - reject
2. The strongest parts of the memo
3. The weakest assumptions
4. Code-backed findings
5. Strategic implications for the larger roadmap
6. Concrete corrections or reframing you recommend

Keep the critique honest and specific.
Do not produce fluff.
