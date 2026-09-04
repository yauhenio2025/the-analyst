# Engine harness study — synthesis (2026-09-04 evening)

> Question: does the multi-level engine harness beat a one-shot with a strong model, and what in the well-developed engines should change? Readers: Fable 5.1 agent, Codex gpt-5.6 (their memos sit beside this file). This synthesis is the session's.

## 1. What was run
One source (the AUKUS paper, 85,852 chars). Two engines: Conditions of Possibility Analyzer, Argument Architecture Mapper. Conditions: `harness` (the executor's own code path, depth deep, four passes with stances discovery → architecture/inference → confrontation → integration, each pass reading the prior ones); `oneshot` (one call, one-paragraph expert prompt); `oneshot_questions` (one call carrying the engine's probing questions, no passes or stances). Models: Sonnet 4.6 (production) and Fable 5.1. Judge: Sonnet 4.6 with forced structured output, blind, both orders for every pair.

| engine | condition | model | chars | passes | spec / anchor / non-obv / coherence / useful / halluc (10 = none) |
|---|---|---|---|---|---|
| argument_architecture | harness | fable-5-1 | 40,835 | 4 | 9 / 7 / 9 / 8 / 7 / 8 |
| argument_architecture | oneshot | fable-5-1 | 12,570 | 1 | 9 / 9 / 8 / 8 / 8 / 9 |
| argument_architecture | oneshot_questions | fable-5-1 | 16,300 | 1 | 9 / 8 / 9 / 9 / 7 / 8 |
| argument_architecture | harness | sonnet-4-6 | 100,123 | 4 | 8 / 6 / 8 / 7 / 6 / 7 |
| argument_architecture | oneshot | sonnet-4-6 | 17,815 | 1 | 9 / 8 / 8 / 8 / 7 / 8 |
| conditions_of_possibility | harness | fable-5-1 | 74,677 | 4 | 8 / 6 / 9 / 7 / 6 / 5 |
| conditions_of_possibility | oneshot | fable-5-1 | 12,262 | 1 | 9 / 8 / 9 / 8 / 7 / 7 |
| conditions_of_possibility | oneshot_questions | fable-5-1 | 14,658 | 1 | 9 / 7 / 9 / 8 / 7 / 6 |
| conditions_of_possibility | harness | sonnet-4-6 | 95,121 | 4 | 9 / 7 / 9 / 8 / 7 / 7 |
| conditions_of_possibility | oneshot | sonnet-4-6 | 13,713 | 1 | 7 / 5 / 8 / 8 / 6 / 5 |

## 2. What the judge said
- **Whole harness output (four passes concatenated) vs one-shot:** the one-shot wins 12 of 12 pairings, both orders, every margin "clear". The concatenation is four to seven times longer, repeats itself across passes, and scores lower on anchoring and hallucination risk.
- **Harness integration pass alone vs one-shot** (the fair comparison, because production hands the next desk only the last pass: `src/executor/chain_runner.py:667`, `src/dossier/analysis.py:142`): **split by engine.** Conditions of Possibility: the integration pass wins 4 of 4 (both models, both orders, clear). Argument Architecture: the one-shot wins 4 of 4 (clear).
- **Probing questions without passes** (`oneshot_questions`): on the rubric they match or beat the plain one-shot on both engines, at one-shot cost.

## 3. What that means (the session's reading, before the two memos)
1. The harness is not a uniform win or loss. It earns its keep where the method is genuinely sequential — a genealogical reading that must first find the conditions, then structure them, then confront them, then judge — and it loses where the task is a well-defined mapping a strong model can do in one pass (Toulmin/Walton structure). That is a property of each engine's definition, not of the harness.
2. The definitions' most valuable content is the probing questions: they lift a one-shot to near-harness quality for a fraction of the cost. Lineage and capability groundings, which do not enter the prompt today, are unmeasured; the question is whether they would add what the questions do not.
3. The four-pass concatenation should never be what a consumer reads; production is right to hand only the integration pass, and the desk's "under the hood" should show the passes as receipts, not as the product.
4. Cost and time: a deep harness run is four calls and 5–10 minutes per engine per document; the one-shot is one call and about two minutes. For a five-document corpus the difference compounds across phases.
5. Three tooling faults surfaced, none a harness verdict. Fable rejects forced tool use (every desk built on `call_json` cannot run on Fable as written). The "empty responses" from Fable were **refusals** (`stop_reason: refusal`, 0 output tokens in 2 seconds: the run-events ledger for job `study-fable`) on the pass-1 discovery prompts over a defence-industry paper; the executor retried five times and reported "empty response" without ever surfacing the stop reason, and no fallback model was tried. Later passes and the one-shots on the same text were not refused, so the trigger is the prompt framing, not the material alone. Any production path that may run on Fable needs the stop reason logged, a refusal treated as a distinct outcome, and a fallback to Sonnet.

## 4. Readers' memos

### 4a. Fable 5.1 (`STUDY_engine_harness_fable_2026-09-04.md`)
Verdict: the harness earns its keep on one engine and not the other; do not keep investing in a 275-engine registry, and do not retreat to a bare one-shot; invest in a small set whose *kind* decides whether an engine runs as one call with probing questions (mapping, extraction) or as passes (synthesis, judgment); fix three cheap prompt bugs; give every pass a model-declared, wall-checked findings ledger the spine can cite.

What it found in the code, verified by the session:
- `src/stages/capability_composer.py:357-360` tells every pass, including the last, that "the next analytical pass" will read it; the final pass therefore writes for a machine.
- `capability_composer.py:365-372` renders the composability `shares_with` lines whenever a key substring-matches a focus dimension. Argument Architecture's keys equal its dimension keys, so its final pass is told to surface material "for the next pass" and ends with hand-off sections; Conditions of Possibility's keys match nothing, so its final pass writes for a reader. This alone can explain the split.
- `src/executor/chain_runner.py:359-367` rebuilds each `PassDefinition` with `description=""`, so the operationalization's per-pass description never reaches the model.
- No pass prompt asks for verbatim anchors (the composer contains no such instruction); the one-shot prompt does, and anchoring was the judge's first criterion.
- No condition used extended thinking; depth changes only the pass count and one guidance sentence.
- The Fable harness runs were missing passes (pass 1 returned nothing on both engines, pass 2 on Argument Architecture): a 3-pass and a 2-pass run that still split the same way, which favours the engine-level explanation over a model-level one.

Ranked proposals: (1) fix the final-pass prompt (desk-facing last pass, no `shares_with` tail there, anchoring line on every pass, pass the description through), then rerun the eight integration-only pairings; (2) route by kind (`execution_mode` on the operationalization: single call for mapping/extraction, passes for synthesis/judgment; let `deep` set effort); (3) a findings ledger per pass with verbatim anchors, wall-checked, read by the spine; (4) render the method card (intellectual grounding and indicators for the pass's capabilities, carried in the composer but never rendered) and prune Conditions of Possibility to five dimensions; (5) instrument empty responses (log stop reason, raise on empty).

### 4b. Codex gpt-5.6 (`STUDY_engine_harness_codex_2026-09-04.md`)
Verdict: "not in its present form". Keep the analytical methods; replace the 200-plus-engine, fixed-pass apparatus with roughly a dozen method families: a strong-model, structured, source-anchored one-shot by default, with a targeted critic and a final synthesis only when the planning model judges the material warrants them. The exception worth preserving is the conditions engine's final integration, which contains a synthesis the one-shot did not reach (the causal inversion seen as "one hole", the repair in the paper's own vocabulary).

What it adds to Fable's reading:
- `consumes_from` hands whole prior prose, untruncated, to later passes (`src/executor/context_broker.py:108-152`); integration consumes every prior pass in both deep sequences. It should carry a compact finding ledger, counter-evidence and open questions, not research diaries.
- Depth is mechanically real (pass sequence, dimension guidance, model routing) but analytically unvalidated; the conditions YAML advertises three deep passes while the operationalization executes four.
- Definitions: in Conditions of Possibility, unacknowledged debts overlaps cross-domain transfer, alternative paths overlaps the counterfactual, synthetic judgment is an output stage not a dimension; the questions invite unsupported intellectual biography when only one paper is present.
- Discovery is explicitly told not to compress or organize for a consumer (`src/operations/definitions/stances.yaml:21-40`), which costs coherence downstream.
- The study cannot quantify money (costs were not recorded); time and length it can: four to five times longer, six to seven times more prose.

Ranked proposals: (1) make anchored findings the engine contract; (2) default to one analytical call, let a planning model request one targeted critic or integration call; (3) fix handoff plumbing and failure semantics (descriptions, ledger instead of diaries, empty content as a distinct outcome); (4) judge the artifact the dossier consumes, with a read-through desk; (5) collapse the registry into method families plus backend capability metadata.

## 5. Where the two readers agree, and the session's recommendation

Both readers, independently and from the same evidence, converge on five things:
1. **The contract should be anchored findings, not prose.** Every pass returns model-declared findings with verbatim anchors, wall-checked, and the spine cites them; the prose stays as the receipt.
2. **One call by default; passes by kind.** Mapping and extraction engines run as one structured, anchored call carrying their probing questions (which the study shows lift a one-shot to harness quality at one-shot cost); synthesis and judgment engines keep a sequence, but a short one whose last pass writes for the reader.
3. **Fix the plumbing before judging the method.** The blank pass description, the "next pass will read this" line on the final pass, the composability tail rendered on the last pass, the untruncated prior-pass context, no anchoring instruction, refusals reported as "empty". These are hours of work and they confound every comparison made so far.
4. **Judge what the dossier consumes.** The 12/12 loss was of an artifact nobody reads; the split result is of the artifact the spine reads. Any further study, and the cross-check itself, should judge that.
5. **A smaller set of methods.** 275 registered, 28 executable, 22 offered, two of them studied: the registry as a catalogue of names is not where quality lives. Both readers would rather have a dozen method families with parameters and real definitions than two hundred labels.

They differ on how much of the multi-pass structure survives: Fable keeps it for synthesis and judgment methods on the strength of the Conditions of Possibility result (4/4 for the integration pass); Codex keeps only a planner-requested critic and final synthesis. The session's view is that this is the same design seen from two ends, and the plumbing fixes decide it: rerun the eight integration-only pairings after fix 3, and let that result set the default for the synthesis family.

**Recommendation to the owner.** Do not put more work into the engines as a catalogue. Do the plumbing fixes this week (a day), make anchored findings the contract (two to three days, because the spine and tables must learn to cite them), and re-run this study on two more engines and one more document set before deciding the pass structure. Keep The Mastermind as the registry of methods and grammars; what it should list is a dozen method families with their definitions, lineage rendered as a method card in the prompt, and the executable ones marked, rather than 275 engines of which two have been tested.

## 6. Files
- Brief: `communications/study/STUDY_BRIEF_engine_harness_2026-09-04.md`; runners: `scripts/study_engine_harness.py` (part 1), `_part2.py` (superseded), `_part3.py` (Fable harness via the dossier caller, Sonnet judge), `_part4.py` (integration-only fairness check).
- Evidence (untracked, on this machine): `data/study/manifest.json`, `SUMMARY.md`, `outputs/*.md`, `judgments.json`, `judgments_integration_only.json`, `source_aukus.txt`, run-events for jobs `study-fable`, `study-judge`.
- Memos: `STUDY_engine_harness_fable_2026-09-04.md`, `STUDY_engine_harness_codex_2026-09-04.md`.


## 7. Retest after the plumbing fixes (same evening)

Fixed: pass descriptions carried; the final pass told it is the product; anchoring law and findings-ledger law on every pass; prior-pass context handed as ledgers plus capped prose; refusals surfaced with a Sonnet fallback (Fable refused pass 1 on both engines again, and the fallback fired both times); Fable-safe JSON. Every pass of every run now ends with a findings ledger. Judged on the final pass, against the same one-shots.

| engine | model | final pass chars | passes | est. cost | time | spec / anchor / non-obv / coherence / useful / halluc |
|---|---|---|---|---|---|---|
| conditions_of_possibility | sonnet-4-6 | 28,040 | 4 | $0.75 | 613.4s | 9 / 8 / 9 / 8 / 6 / 7 |
| conditions_of_possibility | fable-5-1 | 22,243 | 4 | $0.72 | 589.4s | 8 / 7 / 8 / 7 / 5 / 6 |
| argument_architecture | sonnet-4-6 | 26,752 | 4 | $0.76 | 623.6s | 9 / 8 / 9 / 8 / 7 / 7 |
| argument_architecture | fable-5-1 | 25,927 | 4 | $0.72 | 593.4s | 9 / 9 / 9 / 8 / 7 / 9 |

| engine | model | A | B | winner | margin |
|---|---|---|---|---|---|
| conditions_of_possibility | sonnet-4-6 | harness_v2_final | oneshot | oneshot | clear |
| conditions_of_possibility | sonnet-4-6 | oneshot | harness_v2_final | harness_v2_final | clear |
| conditions_of_possibility | fable-5-1 | harness_v2_final | oneshot | oneshot | clear |
| conditions_of_possibility | fable-5-1 | oneshot | harness_v2_final | oneshot | clear |
| conditions_of_possibility | fable-5-1 | harness_v2_final | oneshot_questions | oneshot_questions | clear |
| conditions_of_possibility | fable-5-1 | oneshot_questions | harness_v2_final | oneshot_questions | clear |
| argument_architecture | sonnet-4-6 | harness_v2_final | oneshot | oneshot | clear |
| argument_architecture | sonnet-4-6 | oneshot | harness_v2_final | harness_v2_final | clear |
| argument_architecture | fable-5-1 | harness_v2_final | oneshot | oneshot | clear |
| argument_architecture | fable-5-1 | oneshot | harness_v2_final | oneshot | slight |
| argument_architecture | fable-5-1 | harness_v2_final | oneshot_questions | oneshot_questions | clear |
| argument_architecture | fable-5-1 | oneshot_questions | harness_v2_final | oneshot_questions | clear |

Reading of the retest:
- **On Sonnet outputs the judge split 1-1 on both engines with "clear" both ways: a position effect, so a tie.** On Fable-written outputs the one-shot won both orders on both engines (one margin "slight"), and the one-shot carrying the probing questions won both orders on both engines.
- The fixed harness's final pass is now a reader-facing document (22-28K chars, anchored, with a ledger), and its rubric scores are level with or above the pre-fix integration pass on anchoring and hallucination risk. But it does not beat a one-shot of 12-18K chars at a quarter of the cost and time on this material, and the judge's reasons repeat one line: the harness's reading of Conditions of Possibility "performs meta-commentary on the paper's intellectual genealogy as an abstract exercise" and makes claims about the authors' intentions the text does not support. That is the definition (Codex's point: the questions invite intellectual biography from one paper), not the plumbing.
- The earlier 4/4 win for the pre-fix Conditions of Possibility integration pass did not survive the retest; on one document and one judge it should be read as variance until a fixed-versus-pre-fix comparison and a second document say otherwise. (The fixed-vs-pre-fix pairings are in `judgments_v2_fixed_vs_prefix.json`.)

What this settles, and what it does not:
- Settled: the plumbing was broken and is fixed; production prompts now carry the laws; refusals no longer masquerade as empties; every pass yields an anchored ledger the spine can cite. Retest runner: `scripts/study_engine_harness_v2.py`.
- Settled: on this material, four passes do not buy a better final reading than one call with the probing questions. The cost of the harness is real (four calls, about ten minutes, roughly four times the tokens) and the benefit is not visible to this judge.
- Not settled: whether a two-pass shape (one reading call with the questions, one critic/integration call fed by its ledger) beats the one-shot, which is what both readers proposed; whether the definitions, rewritten to stop inviting biography, change the result; and whether a second document and a second judge agree.

**Recommendation, revised.** Make the one-shot-with-questions the default execution mode for every engine (it is the cheapest condition that matched or beat everything else), keep the anchoring and ledger laws on it, and offer a second pass (critic or integration, fed by the first pass's ledger) as the depth dial rather than four stances. Rewrite the two studied definitions so the questions ask about the text rather than the authors' biography. Then rerun this study on two documents with two judges. That is a week's work, most of it definitions, not code.
