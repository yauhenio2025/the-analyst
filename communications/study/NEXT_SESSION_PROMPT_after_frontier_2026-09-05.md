# Next session — act on the frontier (2026-09-05)

Read first: `communications/study/STUDY_frontier_SYNTHESIS_2026-09-05.md` (§4 results, §5 decisions), then `REDESIGN_method_shape_2026-09-04.md`, then tracker §11. State: the study is done ($87.41); the shape is built and deployed at depth key `dvs` for the two engines; production defaults are unchanged.

## Done since (2026-09-05 morning)
Decisions 1, 2 and 4 below are wired and live (commit edd4fd2+): `DepthSequence.mode`; both engines surface = oneshot, standard = oneshot_checked (one call + critic, rulings applied by code), deep = dvs; strong tier Sol, critic DeepSeek V4 Pro. The check study (synthesis §8) confirmed the check: 41/58 blind pairs. Remaining: decision 3 (desks read rows by id; skip rows tagged `anchor-verified: no`), decision 5 is a rule.

## Decisions (1, 2, 4 done; 3 remaining)
1. **Default execution mode = the one call** with the redesigned question sets and method cards. Wire: an `execution_mode: oneshot | dvs | stances` on the operationalization (default `oneshot` for engines with a `process`), honoured by `chain_runner._run_engine_passes` via `compose_oneshot_prompt`; the plan's `depth` maps surface/standard → oneshot, deep → dvs.
2. **Default model for a reading a person reads = GPT-5.6 Sol** (`openrouter/openai/gpt-5.6-sol`), Kimi K3 second, Sonnet acceptable, Luna for previews; Fable only when asked. Wire: the process `routing.strong` and the executor's `MODEL_CONFIGS` tier for phase 1.0 when the engine carries a process; keep the refusal fallback.
3. **Desks-facing runs = `dvs` routed Luna / DeepSeek V4 Pro / Sol.** Wire: the spine reads ledger rows by id (`anchors_planned` copied from rows), the tables desk builds from `### Tables` row sets, figures from rows with relations; "under the hood" shows extraction and critic ledgers as receipts.
4. **Retire the four-stance default** (keep the YAML for reference; the desk's depth dial stops offering it). Fable refuses it on any material.
5. **Judging** in every future study: both orders on Sonnet, or two judges both orders; never split orders with an unchecked judge.

## Then
- Bring the next two engines under the shape (one genealogy, one logic: e.g. `inferential_commitment_mapper`, `concept_evolution`), rewriting their questions to ask about the text, and run the one call + `dvs`-routed pair on the same two papers with Sonnet judging both orders (≈ $10).
- Harden the OpenRouter path: detect truncated streams (`finish_reason`), retry once; DeepSeek Flash is too slow for chains (13–38 min).
- Tests to keep green: `tests/test_process_shape_2026_09_04.py`, `tests/test_plumbing_2026_09_04.py`.

## Rules (standing)
LLM-first: judgment to the model, plumbing to code; walls check anchors verbatim and ids exist, never meaning. Commit and push per phase (master deploys to Render). Never Veo. Ask before spend.
