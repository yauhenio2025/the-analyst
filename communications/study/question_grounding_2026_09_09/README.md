# Question grounding: controlled discovery comparison, 9 September 2026

The revised method requested primary evidence for the Riley question with both
the original and enriched context. The original method chose a conceptual
prerequisite in both conditions. Enriched context improved the specificity of the
revised reading plan, but did not by itself change the original method's decision.
Two conceptual controls stayed source-free under the revised method.

These are six completed local subscription runs, with one observation per condition.
They diagnose this instance; they do not establish a general success rate, an author's
accepted judgment, or the quality of a subsequent reading.

## What was held fixed

Every run used Codex `gpt-6-astra`, ultra effort, a fresh temporary directory and the
same instruction to use only the supplied local prompt. No network, connectors,
external research or production preparation/completion calls were authorized for
these comparisons. The central preparation function composed the revised prompts
with its blob reads and writes patched to an in-memory dictionary. The Stacks runner
executed the six workers; no question job or reading-ledger import ran.

The original input and system prompt come directly from the saved discovery prompt
of Stacks question 1, attempt 1. The fresh old-method/original-context prompt is
byte-for-byte identical to that saved prompt. Within each context condition both
methods receive identical input JSON. All six cases use the same output-schema hash,
`b707cff4ebfba471184ccb843481c378afb10dddc7b7a9f998b5771634677995`.
Thus the method comparison changes the central method prose, not the output contract.

The enriched condition adds only `context.preparation.source_landscape` to the
original input. It contains 40 bounded catalogue candidates drawn from all five
attached Brief bundles and labelled secondary previews of earlier Riley
investigations. It discloses truncation, omissions and coverage. It contains no
primary-source passages. Other differences in the context helper's returned object
were deliberately excluded, preserving the original question, commitments and author
responses exactly.

## Observations

| Method | Context | Primary sources needed | What the plan does | Seconds |
| --- | --- | --- | --- | ---: |
| Original | Original | No | Develops a generic prerequisite about politically organized growth; postpones assessing Riley. | 131.5 |
| Original | Enriched | No | Uses catalogue/earlier analyses as context but again postpones comparison with Riley. | 120.1 |
| Revised | Original | Yes | Requests bounded passages to test whether growth contradicts a necessary premise, changes a contingent diagnosis, or is already accommodated. | 141.2 |
| Revised | Enriched | Yes | Names held leads and earlier investigations; preserves an actual correction about solidarity and organization; requests contrary passages. | 144.4 |
| Revised | Conceptual brainstorming | No | Develops possible meanings of growth and development without empirical or author-specific claims. | 92.5 |
| Revised | Incidental author mention | No | Develops conceptual alternatives for solidarity; explicitly excludes interpreting Riley. | 90.6 |

All six outputs are valid JSON and satisfy the unchanged output schema. The historical
saved observation also chose no sources; its answer and execution metadata are retained
separately from the fresh rerun in `historical_observation.json`.

The old outputs are candid about their limits and do not invent Riley's position.
Their problem is substitution of a preliminary conceptual task for the requested
source-dependent development. The enriched old-method run actually inspected the
supplied landscape and earlier analyses in its local command trace, so its unchanged
decision cannot simply be explained by failure to open the enriched input.

Both revised Riley plans preserve the actual target: which connections in Riley's
account would have to change, and what follows for class politics and solidarity.
They keep the growth premise conditional and distinguish necessary premises from
contingent diagnoses. The enriched plan identifies *The Thesis of Political
Capitalism*, *Seven Theses on American Politics* and *The Long Downturn and Its
Political Results: A Reply to Critics* as catalogue leads. It uses *Material Interests*
for interest formation and makes *The New Durkheim: Bourdieu and the State* conditional
on unresolved state causality. Those are proposed reading priorities, not established
attributions or proof of adequate coverage.

The enriched revised plan also uses `stacks:investigation:1` and
`stacks:investigation:2` as locating context and preserves the latter's correction
that organization and solidarity may be achievements, rather than prerequisite
checklists. This is a useful consequence of carrying the earlier research forward;
the earlier model analysis remains secondary context rather than primary evidence.

The two controls provide narrow evidence against an indiscriminate “always search”
rule. Both explicitly ask for conceptual work, so they do not establish performance
on more ambiguous or mixed requests. All outputs maintain the distinction between
available metadata, prior interpretation and actual primary evidence.

## Interpretation and limits

In this case, the method revision changed the decision even without enriched
context; context enrichment alone did not. That supports correcting the method and
its input flow before changing the model. The enriched revised plan is more concrete
and reuses an author correction, which supports supplying existing holdings and
memory before deciding whether source work is needed.

There was one fresh run per condition, no randomized execution order and no blind
independent assessment. Model variation and other uncontrolled execution effects
remain possible. The controls are deliberately clear cases. No author accepted a
question or supplied a new correction during the evaluation. A `needs_sources: true`
plan is still only preparation: selection, source reading, interpretation, coverage
and the merit of the resulting question require their own evaluation. The subsequent
bounded reading trial is outside these six discovery comparisons.

The workers reported no separately billed API usage; they ran under the existing
subscription. Execution files preserve durations and any reported list-price
equivalents; token usage is retained in execution events. The retained command events
show local prompt inspection and answer writing/validation. This harness relies on
the worker instruction for the research boundary; it is not a network sandbox.

## Artifacts and reproduction

- `manifest.json` records method/input origins, model, limits and case names.
- Each case directory contains the exact `PROMPT.md`, `ANSWER.json`, hashes in
  `case.json`, `execution.json` and retained command/usage events.
- `source_landscape.json` holds the exact enrichment actually added to the input.
- `original_capability.yaml`, `original_process.yaml`, `revised_capability.yaml` and
  `revised_process.yaml` preserve the compared method records. Frozen prompts remain
  authoritative for the precise instructions executed.
- `historical_observation.json` preserves the original live discovery result without
  treating it as a new evaluation call. `results.json` collects the six fresh runs.

To prepare new comparison files without invoking a worker:

```sh
python tools/evaluate_question_grounding.py \
  --original-prompt communications/study/question_grounding_2026_09_09/old_method_old_context/PROMPT.md \
  --landscape-json communications/study/question_grounding_2026_09_09/source_landscape.json \
  --brief communications/CODEX_PROMPT_question_grounding_2026-09-09.md \
  --output-dir /var/tmp/evgeny/question-grounding-reproduction
```

The harness defaults to preparation only. `--run` explicitly invokes up to six
subscription evaluations, two at a time, and reuses completed case results when
their frozen prompts match. Use a new output directory for a changed method or a
new stochastic observation. It never calls a live Analyst preparation/completion
endpoint or imports results into application state.
