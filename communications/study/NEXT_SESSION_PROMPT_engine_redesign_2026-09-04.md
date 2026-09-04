# Next session — redesign the engine process from the ideal output, then run the cost-quality frontier

You are continuing work in ~/projects/the-analyst (FastAPI "engines" run by an executor; console at https://the-mastermind.onrender.com; desk at https://the-analyst-desk.onrender.com). Read first, in this order: `communications/study/STUDY_engine_harness_SYNTHESIS_2026-09-04.md` (three rounds of blind judgments, two readers' memos, the plumbing fixed tonight), `communications/study/STUDY_engine_harness_fable_2026-09-04.md`, `communications/study/STUDY_engine_harness_codex_2026-09-04.md`, and `communications/IMPLEMENTATION_TRACKER.md` §10. Evidence (outputs, judgments, manifest) is under `data/study/` on the desk machine.

## What we know (2026-09-04)
- The engine harness (four re-readings of a text under stances discovery → architecture/inference → confrontation → integration, each pass a diary) does not beat one call with the engine's probing questions on the same model; after the plumbing fixes it ties on Sonnet (position effect) and loses on Fable. The pieces that only the passes found (a causal inversion, a borrowed warrant) show extra work CAN add value when it is different work.
- The definitions are the quality lever: Conditions of Possibility's questions invite intellectual biography from one paper; Argument Architecture's final pass was written for downstream engines. Plumbing is now sound: final pass reader-facing, anchoring + findings-ledger laws on every pass, ledger-first prior context, refusals surfaced with a Sonnet fallback, Fable-safe JSON (commits 424ceb1, ca34fab).
- Cheap models change the economics: through OpenRouter (keyed locally and on Render) a four-pass run on GPT-5.6 Luna ($0.2/$1.2 per M) or DeepSeek V4 Pro ($1.04/$2.08) costs a tenth to a thirtieth of one Fable 5.1 call ($10/$50). Kimi K2.6 $0.95/$4, GPT-5.6 Sol $2/$10, DeepSeek V4 Flash $0.09/$0.18. Fable refuses some prompts over defence material (stop_reason refusal) and rejects forced tool_choice.

## The owner's instruction
Start with an open mind: assume the current engine design is faulty (it was built with a weaker model), and design from the IDEAL OUTPUT backwards. For a method like "conditions of possibility" or "argument architecture": what do we want to understand at the end, what would the best possible reading contain, and what sequence of steps gets there without losing depth, such that cheaper models can do most of the steps? Do this design thinking here, in the session, without API spend; then build and run the frontier study.

## Part 1 — design from the ideal output (no API calls)
For each of the two engines, write `communications/study/REDESIGN_<engine>_2026-09-04.md`:
1. The ideal output: what an expert reader would want to know after this method has run on one paper and on a five-paper corpus; the shape of the artifact (anchored findings, a reading, tables the desks can cite), what "depth" means for it, what a weak output looks like.
2. The questions that actually produce it (rewrite the probing questions to ask about the text, not the authors' biography; drop overlapping dimensions; say what each question's answer looks like when anchored).
3. The step sequence: which steps are extraction (cheap model, parallelizable, per dimension or per document), which are verification (adversarial check of every finding against the source; hunting for misses), which are synthesis (one strong-model call), and what each step hands to the next (the findings ledger: `- [F<n>] finding — anchor: "verbatim" — confidence`). Say where a critic pass earns its cost and where it does not.
4. How the desks consume it: the spine cites findings by id; tables are built from ledger rows; figures from findings with numbers or relations.
5. Lineage and groundings: what Foucault/Skinner or Toulmin/Walton actually make the model DO in a step (a method card, not a name-drop).
Then generalize: a single shape for the estate's analytical methods (extract → verify → synthesize, with per-step model routing), expressed as an operationalization the registry can hold, and the list of engines that are really parameters of the same method.

## Part 2 — build and run the frontier study (API spend ~$60–100, ask the owner before launching)
- Implement the redesigned shape for the two engines as operationalizations (depth key e.g. `dvs`), per-pass model routing in the runner (`run_engine_call_auto(model_hint=...)` per call), and `scripts/study_engine_harness_v3.py` with: conditions (a) one call with the rewritten questions, (b) the fixed four-stance harness, (c) decompose-verify-synthesize, (d) cheap read + strong write; models Fable 5.1, GPT-5.6 Sol, Kimi K2.6, DeepSeek V4 Pro, GPT-5.6 Luna, DeepSeek V4 Flash, Sonnet 4.6 control; two papers (AUKUS `data/study/source_aukus.txt` plus the subsea-cable paper from `GET https://the-analyst-kcuc.onrender.com/v1/story/jobs/story-d3444a230015/sources/up47F76C1E`); two blind judges (Sonnet and GPT-5.6 Sol), both orders, rubric + pairwise against the Fable one-shot baseline; record tokens, cost, seconds.
- Output one table per engine: quality vs cost vs time; the default execution mode and model are read off the frontier.
- Remember: Fable via `call_json` needs the text-JSON path; refusals fall back to Sonnet; OpenRouter models need the `openrouter/` prefix in model_hint.

## Rules
- LLM-first: judgment to the model, plumbing to code; walls check arithmetic (anchors verbatim, ids exist), never meaning.
- Never Veo; Seedance 2.5 for films (not relevant here, but standing).
- Commit and push after each phase; the-analyst master deploys to Render on push (backend restart ~1 min). Update `communications/IMPLEMENTATION_TRACKER.md` and memory.
