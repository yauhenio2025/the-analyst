# Next session — run the frontier study (needs the owner's go on spend)

State (2026-09-04, 21:40): the redesign is written (`REDESIGN_conditions_of_possibility_2026-09-04.md`, `REDESIGN_argument_architecture_2026-09-04.md`, `REDESIGN_method_shape_2026-09-04.md`) and the shape is built and pushed (commit 6208dda): both engines carry a `process:` block at depth key `dvs` (extract → verify → synthesize, per-step routing), the four-stance `deep` path is untouched as the control, `scripts/study_engine_harness_v3.py` composes all four conditions and prices them. Nothing has been spent. Tracker §11.

## When the owner says go
```
cd ~/projects/the-analyst
python scripts/study_engine_harness_v3.py --dry-run --preset lean      # re-estimate (≈ $72: generation $46 + judging $26)
python scripts/study_engine_harness_v3.py --preset lean                # 92 runs on 4 workers, then judging, then FRONTIER.md
python scripts/study_engine_harness_v3.py --judge-only --report        # if judging was interrupted
```
`--preset full` adds the four-stance harness on all seven models and both judges in both orders (≈ $110). Resumable: rerunning skips runs and judgments already on disk under `data/study/v3/`. Wall-clock 2-3 hours; the Fable four-stance runs are the slow ones (~10 min each).

## What to read off `data/study/v3/FRONTIER.md`
- Per engine: rubric mean by judge, hallucination score, pairwise wins against the Fable one-shot (condition a), cost, seconds, calls, and the code-computed anchor verification rate of the final ledger.
- The default execution mode and routing: the cheapest condition within 0.5 rubric points of the best mean, provided its pairwise record against the baseline is not a clear loss on both judges and its anchor rate is at least the one-shot's. Set it as the engines' default depth (`dvs` or `standard`) and the `routing` block in their operationalizations.
- Whether the verify step earns its cost: compare (d) with a "cheap read, strong write, no critic" variant if (d) ≈ (c); the receipts under `data/study/v3/receipts/*.json` show per step what the critic rejected and what misses it added (`wall.rejected`, `wall.added`).
- Whether the rewritten questions beat the old ones in one call: `data/study/outputs/*__oneshot_questions__fable.md` (old questions, paper 1) against `data/study/v3/outputs/*__a__fable__aukus.md` (new), judged both orders.

## After the frontier
1. Write `communications/study/STUDY_frontier_SYNTHESIS_2026-09-04.md`: the tables, the reading, the default per engine.
2. Set the defaults in the two operationalizations; make the desks read ledger rows by id (spine `anchors_planned` from rows; tables from `### Tables`); rewrite the next two engines' question sets under the shape (`REDESIGN_method_shape` §3 lists the families).
3. Update the tracker (§11) and memory (`engine-redesign-process-shape`).

## Rules (standing)
LLM-first: judgment to the model, plumbing to code; walls check anchors verbatim and ids exist, never meaning. Commit and push per phase (master deploys to Render). Never Veo. Ask before spend.
