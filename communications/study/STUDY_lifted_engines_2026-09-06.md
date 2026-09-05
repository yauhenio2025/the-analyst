# Lifting existing engines under the shape: three cases (2026-09-06)

The consolidation recipe's first step (tracker §11, "existing questions first, rewrite on demonstrated defects") was tried on three engines whose questions Codex's map marked as usable as they stand: A3 `comparative_reasoning_analyzer` (audit comparisons and analogies), C3 `concept_centrality_mapper` (concept dependencies and centrality), S2 `chapter_role_analyzer` (section and chapter functions). `scripts/lift_engine_under_shape.py` turned each engine's analytical dimensions into `process:` dimensions (questions, answer shape, a method card built from the indicators), with the standard modes (surface oneshot, standard oneshot_checked, deep dvs) and routing. No question was rewritten. Runs and ratings by `scripts/study_first_queue.py --engines ...` (production default `checked` = one call on Sol + DeepSeek V4 Pro check; `old` = the engine's original prompt in one call on Sol); independent Sonnet and Sol ratings on the six-criterion reading rubric; anchors verified by code. Raw: `data/study/v5_first_queue/` (outputs, `ratings.json`, `results.json`, `REPORT.md`). Generation USD 1.24, ratings USD 1.37.

| engine | paper | condition | rubric Sonnet / Sol | anchors | rows | chars | $ |
|---|---|---|---|---|---|---|---|
| comparative_reasoning_analyzer | aukus | checked | 6.17 / 9.17 | 100% | 23 | 20.6K | 0.12 |
| comparative_reasoning_analyzer | aukus | old | 6.33 / 9.17 | 100% | 26 | 22.1K | 0.09 |
| comparative_reasoning_analyzer | harris | checked | 5.67 / 9.17 | 93% | 29 | 20.5K | 0.13 |
| comparative_reasoning_analyzer | harris | old | 7.33 / 9.17 | 92% | 25 | 34.4K | 0.10 |
| concept_centrality_mapper | hegel | checked | 6.33 / 8.33 | 95% | 19 | 15.3K | 0.13 |
| concept_centrality_mapper | hegel | old | 7.17 / 9.00 | 92% | 24 | 39.5K | 0.13 |
| concept_centrality_mapper | zambrana | checked | 6.00 / 8.33 | 96% | 22 | 22.2K | 0.11 |
| concept_centrality_mapper | zambrana | old | 7.00 / 8.83 | 88% | 24 | 46.5K | 0.13 |
| chapter_role_analyzer | elling | checked | 7.67 / 9.50 | 100% | 23 | 22.0K | 0.13 |
| chapter_role_analyzer | elling | old | 7.33 / 9.33 | 92% | 26 | 32.6K | 0.11 |
| chapter_role_analyzer | promise | checked | 7.17 / 8.33 | 100% | 22 | 21.4K | 0.12 |
| chapter_role_analyzer | promise | old | 7.00 / 9.33 | 96%* | 26 | 26.9K | 0.09 |

\* The run reported 0%: Sol bolded the quoted text inside every anchor (`“**it can be only a negative one**”`) and the wall read the asterisks as text. `src/dossier/walls.normalize` now strips markdown emphasis on both sides (test in `tests/test_process_shape_2026_09_04.py`); rescanned, 25 of 26 anchors verify. The same wall class as the bolded ids and curly quotes of the frontier study: presentation marks inside the row grammar.

## What the numbers say

1. **Lifting is not a quality lever; it is an anchoring and length lever.** Under the shape the readings are half the length (15–22K vs 22–47K chars), anchored at 93–100% against 88–100%, and carry the check receipt. On Sonnet's reading rubric they score within noise of the originals for the two map methods (concept centrality −0.8/−1.0, chapter roles +0.3/+0.2 — one paper each way) and clearly lower for the comparison audit on Harris (−1.7). Sol rates every output 8.3–9.5 and separates nothing.
2. **Sonnet's reasons are the same for `old` and `checked`:** "taxonomy of rhetorical devices rather than a sustained reading", "exhaustive concept inventory ... fractured into taxonomy trees", "list-of-chapters format fragments rather than synthesizes". These three are structural-map methods; the rubric penalises inventories by construction, as it did for the quantity and event methods. For C3 and S2 the right measures are the desk's: anchor rate, rows, and whether the map is correct against the text; both improve or hold under the shape.
3. **The comparison audit shows a real defect, and lifting reproduced it.** Sonnet on the lifted Harris reading: "the 'findings ledger' framework imposes generic analytical categories (analogical transfer, scalar positioning, dichotomy architecture) that could fit almost any polemical theory paper". The original engine's dimensions are a taxonomy of comparison devices; under the shape those labels become the organising categories of the output. Codex's A3 question ("Do the text's analogies, classifications and rankings support the conclusions drawn from them?") is an audit, which the inherited dimensions never ask. This is the "rewrite on demonstrated defects" case: A3 goes back to the queue for new questions (ideal output first: each comparison the text relies on, what it must carry, whether it carries it), not another lift.
4. **A limitation of the standard mode surfaced twice:** the prose cites rows the critic rejected ("two prose citations to findings the critic rejected"; "'role migration' findings are rightly rejected yet left in the prose"). `oneshot_checked` applies rulings to the ledger and leaves the prose untouched by design; the reader sees a receipt section but not an inline mark. A shape-only fix belongs in the plumbing consolidation: when the prose cites an id the check rejected, tag the citation inline ("[F12, rejected by the check]"). Id membership, not meaning.

## Decisions

- **Keep lifted and live:** `concept_centrality_mapper` (C3) and `chapter_role_analyzer` (S2). Same questions, shorter, better anchored, checked; desks read their ledgers by id.
- **Send back for questions:** `comparative_reasoning_analyzer` (A3). Its lifted block stays in the file (marked "lifted") but the method is listed in the second queue for a rewrite from the ideal output; until then the engine runs as before under the shape (no regression against the original beyond one paper's rubric score, with better anchors).
- **Generator verdict:** `lift_engine_under_shape.py` is the right first step for map and inventory methods whose dimensions face the text; it is the wrong step for any engine whose dimensions are a device taxonomy, because the taxonomy becomes the reading. Read the dimensions before lifting; if they name devices rather than things the text does, write questions instead.

## Reading-guide brief re-rate (S1)

The `deep_summarization` brief now carries one line of argument and entry points as prose. Re-rated on the same two papers (`checked_v2`): Sonnet 6.67 (was 6.50) on AUKUS and 7.50 (was 7.33) on Zambrana; Sol unchanged at 9.33. On Zambrana the guide now edges the original questions (7.00); on AUKUS the original one-call reading still rates higher (8.00). A small, consistent gain, inside the rubric's noise for a single paper. The reading guide stays live as the standard S1.
