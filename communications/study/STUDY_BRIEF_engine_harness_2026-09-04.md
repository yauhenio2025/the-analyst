# Study brief — does the engine harness earn its keep? (2026-09-04)

Owner's question, verbatim in spirit: "Shouldn't we be asking what in the well-developed engines can be made better, in terms of process, definitions, workflows? Does this harnessing work at all? Would we be better off with a simpler prompt and letting a strong model figure out the 'conditions of possibility'? It's possible our multi-level structure produces superior results to a one-shot model, but I'm not sure, and I'm not sure we have the best possible engine set-up. Let's try on a couple of engines and see where we end up; then we decide: more work on the engines, or something else."

Two readers answer independently (a Claude Fable 5.1 agent and a Codex gpt-5.6 agent), from the same evidence, then the session synthesizes. Argue from the outputs and the code, not from taste; where you speculate, say so.

## The evidence on disk (read all of it)
- `data/study/manifest.json` — every run: engine, condition, model, cost, seconds, output file.
- `data/study/outputs/*.md` — the analyses. Conditions per engine:
  - `harness`: production path — `compose_all_pass_prompts` → per pass `compose_pass_prompt` (framing, stance, focus dimensions with probing questions, prior-pass context, pass description) → `run_engine_call_auto`; depth `deep`; the same code the executor runs.
  - `oneshot`: one call, a plain expert prompt naming the task in one paragraph, no dimensions, no stances, no passes.
  - `oneshot_questions`: one call carrying the engine's probing questions but no stances, no passes, no framing.
  Each on two models where run: `claude-sonnet-4-6` (production) and `claude-fable-5-1`.
- `data/study/judgments.json` — blind pairwise judgments by a judge model on a fixed rubric (specificity to the text; anchoring in quotes; non-obviousness; coherence of the whole; usefulness to an executive reader; hallucination risk), with reasons.
- The source: `data/study/source.txt` (one paper from the state-capitalism corpus) and its story profile if useful.

## The code to read
- Engine definitions: `src/engines/capability_definitions/conditions_of_possibility_analyzer.yaml`, `argument_architecture.yaml` (lineage, dimensions, probing questions, capabilities, depth levels, passes with stances and consumes_from, composability).
- The harness: `src/stages/capability_composer.py` (compose_all_pass_prompts, compose_pass_prompt, the framing/stance/dimension sections), `src/operations/` stance registry, `src/executor/chain_runner.py` (pass loop, inner-pass and chain context), `src/executor/context_broker.py`, `src/executor/engine_runner.py` (model routing, chunking, thinking).
- What the prompt actually carries: the study session found that lineage (Foucault, Skinner…) and the capabilities' groundings (Toulmin, Walton…) are NOT in the composed prompt; dimensions, probing questions, stance and depth are.
- The doctrine the owner holds us to: `communications/DESIGN_concretization_passes.md`, `communications/STUDY_de-llm_longform.md`, and the LLM-first doctrine (`~/projects/veo2/LLM-FIRST-DOCTRINE.md`: judgment to the model, plumbing to code; no thresholds masquerading as judgment).

## Questions to answer, in this order
1. **Does the harness beat the one-shot on this material?** Use the blind judgments and your own reading. Where it wins, say which mechanism did the work (the probing questions? the stance sequence? the pass-to-pass context? the depth?). Where it loses or ties, say what the harness cost in coherence, repetition, length or money.
2. **Is the multi-pass structure the right structure?** Look at what pass 2 and 3 add over pass 1 in the harness outputs. Are stances doing anything a good prompt would not? Does consumes_from carry the right things? Is depth (surface/standard/deep) a real dial or a label?
3. **Definitions.** For each of the two engines: are the dimensions distinct and load-bearing, or overlapping? Are the probing questions the ones an expert would ask, or generic? What is missing that the lineage names (what would Foucault or Toulmin actually make the model do)? Should lineage and groundings enter the prompt, and how (a paragraph, a method card, a worked example)?
4. **Process and workflows.** Where in the dossier process do engine outputs matter (spine, tables, figures read the analysis prose)? Is the prose the right handoff, or should engines return structured findings with anchors that the spine can cite? What would you change first in the chain (order, context handoff, the judge)?
5. **The set-up as a whole.** 275 registered, 28 executable, 22 offered. Is a registry of 200-plus analytical engines the right unit, or are there a dozen real methods with parameters? Say plainly whether you would invest in the engines, in a smaller set with better definitions, or in the one-shot with a strong model plus the desk's walls.
6. **A concrete proposal.** Three to five changes, each with: what, where (file), why (evidence), how to test it. Rank them.

## Deliverable
One memo, `communications/study/STUDY_engine_harness_<reader>_2026-09-04.md` (reader = fable | codex), under 2,500 words, with a verdict in the first paragraph. Cite output files and line numbers. Do not modify any code.
