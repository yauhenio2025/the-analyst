# Engine-catalogue triage: rubric review (Codex, 2026-09-05)

The rubric asks the right broad questions, but **the current run cannot be described as neutral judgment with shape-only validation**. The most consequential issues are a forced consolidation size, code-authored replacement verdicts, insufficient evidence for duplicates outside a batch, and cards that omit the active redesigned questions. Fix the rubric and its evidence contract before treating the resulting table as a migration or retirement decision.

I reviewed [the rubric](TRIAGE_rubric_2026-09-05.md) and [Claude's script](../../scripts/triage_engine_catalogue.py) as files only. I did not import or run the script, call a model/API, change it, or edit definitions/operationalizations. The script changed during review; the reviewed 202-line revision has SHA-256 `d40ced196c6f0336cf473c870642f9b26b311385192bcb95d7ae13c1e6fab705`. The rubric hash is `875e655d4b50a6ede6fd7d05df87073c0a9a405932e39a6997f5cda999962fe1`. Findings below refer to that snapshot, not an assertion that every generated artifact used that prompt. Companion: [demand memo](TRIAGE_demand_memo_codex_2026-09-05.md).

## 1. Does it answer the five required questions?

| Required judgment | Present support | Limitation / concrete edit |
|---|---|---|
| **(a) Reader question** | `use` asks what the reader learns; `unclear` is allowed. This is a useful starting point. | `distinctive_value` asks for something a “careful general reading ... would not” find. That penalizes reproducible inventories, focused reading and useful specialization. Ask what reusable answer it produces and what would be lost if folded into a neighboring method; novelty beyond a skilled reader is not required. Add expected input and output unit. |
| **(b) Family** | Ten allowed families include `other`; the model chooses rather than a keyword classifier. | The list mixes subject/method families with corpus scope. Permit a primary family, optional secondary family and separate scope; explain uncertain placement in `family_reason`. Category is background metadata, not the answer. An invalid family is a validation error, not a code-assigned `other`. |
| **(c) Duplicates** | `overlaps_with`, `distinctive_value`, `merge_into`, then consolidation. | Pass A sees up to five cards from one existing category and only keys for the rest. A key is insufficient evidence of duplication. Distinguish equivalent, subset/superset, partial overlap, complementary and unassessed; require evidence from both inspected cards before a merge. Pass B must see nominated cross-family neighbors. |
| **(d) Text versus unavailable evidence** | The rubric names biography, school checklist, off-genre demands, mixed work and non-analytical work explicitly. | One exclusive label and one decisive phrase lose useful versus defective parts. Require field/dimension-specific evidence and a repair for mixed cards; distinguish missing inputs from inherently unavailable claims. Legitimate method standards are not a checklist merely because a school is named. Absence of experiments in conceptual philosophy is not itself a defect. |
| **(e) Keep under the shape / merge / rewrite / retire** | All four verdicts are available and have short definitions. | `keep` presumes an undefined shape and active questions the cards may not contain. `retire` conflates lack of distinct use with workflow-specific work. Define the shape, preserve separate existing-workflow value, make verdicts provisional when evidence is incomplete, and remove code substitutions and forced method counts. |

## 2. Changes to the supplied evidence and prompt

### A. Show the questions that actually run, with provenance

`build_cards` reads legacy JSON plus capability YAML `analytical_dimensions[].probing_questions`. It does **not** read `process.dimensions[].questions`, answer shapes or method cards in the operationalizations. This particularly affects the four engines already under the shape. For example, the Conditions capability still asks what an author's prior work makes possible and about intellectual biography, while its [active process](../../src/operationalizations/definitions/conditions_of_possibility_analyzer.yaml) states “The text is the archive” and prohibits motive/career/knowledge claims. [process_runner](../../src/executor/process_runner.py) calls [compose_oneshot_prompt](../../src/stages/process_composer.py), which renders `spec.dimensions` and their method cards. A judgment of the legacy card is not a judgment of that executed reading.

Proposed card change: attach labeled `legacy_definition`, `capability_definition`, and, when present, `active_process_questions`/`answer_shapes`/`method_cards`, with source paths and hashes. Ask the model to distinguish a documentation mismatch from a defective active method. If the intended triage object is deliberately only the definition, label its verdict `definition_only` and prohibit claims about deployed quality. `UNDER_THE_SHAPE` is currently saved in cards but not displayed by `card_text`; adding a badge alone would not fix the missing questions.

The script also clips descriptions to 700 characters, problematiques to 900, dimension descriptions to 220, questions to six per dimension, extraction steps to eight and their displayed text to 120 characters, and schema keys to ten with at most six nested keys. These may remove qualifications or the output relation that distinguishes two methods. Preserve full questions and scope/answer contracts; if any clipping remains, record fields/counts omitted and allow “insufficient card evidence.” A short schema-key list is not evidence that a declared relation cannot be emitted.

Fix `excluded_reason` to read **`why`**, the actual key in `catalog_purpose.json`, rather than `reason`. Otherwise the six workflow exclusions lose their explanations. Report current availability as context, not a presumption that offered engines deserve retention or unoffered engines deserve retirement. `offered_in_group` is a purpose-file lookup, not the runtime capability join; that happens to identify the same 22 engines in this snapshot, but should be labeled accordingly.

### B. Remove the forced answer in family consolidation

The reviewed `B_SYSTEM` adds requirements absent from the rubric file:

> “a family has 3 to 8 methods”

and directs that variants such as a concept's causal relations as cause/effect/bidirectional **“are one method.”** These lead the model toward a predetermined granularity. A family may need two methods, nine, or no standalone method. The causal variants may turn out to be one method, but that is the judgment being commissioned. The five-critic-skills cap may also hide a material recurring duty; use brevity guidance rather than a substantive quota.

Replace that part of `B_SYSTEM` with:

```text
Choose the number of methods warranted by the reader questions and the cards.
There is no target count or compression ratio. For each proposed combination,
say what is shared, what distinct questions would remain as dimensions, and
what would be lost. For each proposed separation, state the distinct reader
question. Revise pass-A placements or verdicts when the fuller comparison
warrants it; name the revision and its evidence. A family is a reporting aid,
not a barrier to a cross-family overlap.
```

Keep the requirement to account for every engine once as a **disposition**. Add `unresolved` accounting for incomplete evidence; otherwise “one method or retire” forces false finality. A method may draw reusable dimensions from other engines even when each engine has only one primary disposition.

### C. Make duplicates a comparison of definitions, not names

Replace the rubric's “in the batch or known to you from the catalogue list” with:

```text
Use inspected definition content to assess overlap. Catalogue keys alone may
nominate a comparison to inspect; they do not establish duplication. Record
the relation and direction: equivalent, narrower_than, broader_than,
partial_overlap, complementary, or unassessed. Cite the question/dimension
from each inspected card and state the remaining difference. A merge needs
a named destination and an account of the valuable questions it preserves.
```

In Pass A, retain an `overlap_candidates` list for unseen cards. Deterministically retrieve the requested cards for the relevant consolidation inputs; code chooses them by the model's IDs, without guessing similarities. Pass B currently receives only the cards assigned to its own family, plus pass-A judgments. It therefore cannot reliably adjudicate a merge into a neighboring family. Either include those nominated destination cards and an explicit cross-family disposition, or leave those proposals unresolved. No extra paid calls are performed or authorized by this review.

## 3. Concrete replacement rubric language

Insert this scope paragraph before the pass-A fields:

```text
Judge the definition and supplied active questions, not the engine's name,
prestige, present availability, development status or measured performance.
The reader task is to answer a question about supplied material using
attributable findings, with evidence and limits. The shared execution shape
can produce a reading with a ledger, add a critic, or extract/check/synthesize;
an engine contributes its questions, answer shapes and method-specific duties.
The critic judges support and misses; code checks declared structure and
quotation occurrence. Neither a schema nor a matching quote proves meaning.

Inventories, source comparisons and supported negative results are legitimate
answers. Do not require a surprising finding, a minimum number of positive
findings, or a critique of every source. Do not infer implementation quality
from the definition. State missing evidence rather than completing the card
from the engine's name or your memory.
```

Revise/add these fields; the exact field names can be adapted without changing their purpose:

| Field | Proposed instruction |
|---|---|
| `use` + `use_basis` | One reader question in plain language, plus the supplied question/focus that licenses it. `unclear` is allowed, with why. |
| `inputs_and_scope` | What must be supplied: one text, a long work, comparable texts, ordered works of one author, prior analytical findings, selected actors, or other material. State missing context rather than assuming it. |
| `answer_unit` | What a reusable answer contains: claim and support relation, inventory item, concept dependency, attributed comparison, temporal change, or another stated unit. May be unclear; do not impose one universal positive-finding form. |
| `family` + `family_reason` | Primary family from the declared list, optionally a secondary family. Choose from the reader question; explain ambiguity. Record document/corpus scope separately. |
| `text_facing` + `scope_assessment` | Keep the short label for reporting, but list decisive field/question, quoted phrase, what can be observed, what cannot, conditions that make it answerable, and any needed rewrite. For `mixed`, identify both the valuable and problematic components. |
| `overlaps_with` + comparison evidence | Relations and evidence as in §2C. Distinguish partial overlap from duplication and an uninspected candidate from a finding. |
| `distinctive_value` | What focused answer, organization, coverage or relation this method contributes, and what would be lost on merging it. A careful reader could also find it; that is not a defect. |
| `verdict`, `merge_into`, `reason`, `needed_change` | Model-authored disposition under the definitions below. State concrete changes for rewrite/merge; the reason cites supplied content. |
| `assessment_status` + `uncertainty` | Whether evidence is sufficient or the verdict is provisional because cards, inputs or comparisons are missing. This is distinct from a semantic verdict. |

Replace the text-facing definitions with these boundary clarifications:

- **Text:** what the supplied material says, does, presupposes or supports; textual evidence can support a qualified interpretation without literal keyword matching. What a text reports about an author is a report, not independent proof of a motive or mental state.
- **Author biography:** asks the model to establish private motives, awareness, career causes or intentional concealment that the supplied archive cannot establish. Distinguish this from comparing two supplied works or analyzing explicit autobiographical claims.
- **School checklist:** demands conformity to a named school regardless of the text's question, commitments or genre. A named tradition's useful operation or an expressly adopted methodological standard is not automatically a defect.
- **Off-genre demand:** demands an evidential form inappropriate to the claim/genre. A philosophical derivation is not refuted by missing experiments, and a genuine inferential counterexample need not use literal if–then syntax. Still allow the model to find an unsupported empirical claim inside a philosophical paper. Distinguish unsuitable demands from relevant evidence simply missing from the supplied inputs.
- **Mixed:** identify the actual components and what survives a rewrite; do not classify an entire method from its most provocative phrase.
- **Not analytical:** distinguish an engine that belongs to another organ/workflow from one with no useful task. “Not for this dossier” does not entail estate-wide retirement.

Use these verdict definitions:

```text
keep: Retain the reader task and its supplied active question set under the
shared shape. Explain its fit and any input prerequisites. This is a
definition-level recommendation, not proof that execution works.

merge: Preserve the useful questions in a named existing destination because
the inspected definitions support the combination; state preserved dimensions,
residual differences and any destination rewrite required.

rewrite: Retain the reader task, but identify the questions, scope or answer
contract that need changing and propose concrete replacement wording.

retire: Remove this standalone analytical offering because no useful reader
task remains after the comparison, or because it belongs elsewhere. Say
whether its questions move to a shared card, critic duty or another workflow.
Do not use retirement merely for missing capability YAML, weak sample usage,
a supported negative result, or a definition whose intended use is unclear.
```

Keep `keep` as the JSON spelling if compatibility matters; display it as **keep under the shape**. The model can express an uncertain/provisional verdict through `assessment_status`; code must not invent the missing disposition.

For consolidation, add `preserved_questions`, `scope`, `answer_contract`, `changes_from_pass_a`, `unresolved`, and separate `shared_method_cards` from `critic_duties`. The model should decide whether a repeated practice is an analytical deliverable, a reading operation or a verification duty. A causal chain may be the deliverable; checking that a quoted opponent was not attributed to the author is a shared duty. An evidence inventory may be useful; merely verifying its quotations is not a new content engine.

## 4. What code should check, and where the script currently exceeds or misses that boundary

| Location / observed behavior | Required plumbing-only edit |
|---|---|
| `pass_a`: invalid family becomes `other`; invalid text-facing label becomes `mixed`; invalid verdict becomes `rewrite` | Preserve raw output, report the offending field as invalid, and leave the item incomplete. `other`, `mixed` and `rewrite` are meaningful judgments, not parser defaults. |
| `pass_a`: unknown merge target is emptied, then `merge` changes to `rewrite` with a code-written reason | Check target existence, self-merge, and consistency of `merge_into` with the verdict. Report invalid linkage; do not change the judgment or append a semantic reason. |
| `pass_a`: accepts a subset or repeated judgments; no complete field/type check | Require an object with one judgment per expected key, correct field types and enumerations. Track missing, duplicate, unknown and malformed entries separately. Do not count response-list length as coverage. |
| `pass_a` resume: any missing member requeues the whole original batch; results are appended | Resume by missing/invalid IDs with provenance, or replace the relevant batch atomically while retaining attempt history. Avoid duplicate judgments, cost shares and family inputs. |
| `pass_b`: assigns `r['family'] = fam`, then stores the unvalidated result | Validate returned family rather than overwriting it. Validate methods, keys in `folds_in`/`retire`/`questions_source`, field types and each engine's unique primary disposition. Check unknown/self/cyclic merge references as structural errors; do not choose their resolution. |
| `pass_b` completeness and resume | Do not mark a family complete merely because an object exists. Bind its result to the exact card set and pass-A judgment hashes; invalidate the completion status if its inputs change. Carry unresolved/missing cases explicitly. |
| `call_json`: if parsed output is a list, selects its first dictionary | Accept only a documented unambiguous wrapper repair. Otherwise retain the unexpected shape as invalid; never silently discard other proposed judgments. |
| `call_json` retries parse failures; saved judgment cost shares reflect only the returned attempt | Save every raw response and receipt, including failed parsing attempts, actual model and available usage. Report cost as recorded attempts, with unknowns explicit; this does not require any new calls. |
| Report uses `len(J)` as judged count; dictionaries collapse duplicate keys elsewhere; printed reasons are clipped | Report distinct valid keys against expected keys, duplicates/invalid/missing separately, and family completeness. Preserve full reasons in JSON and link them from the report. Truncation in a summary must not masquerade as missing analysis. |
| Shared `data/study/triage` caches are reused after rebuilding cards | Bind a manifest to card bytes, source paths/hashes, rubric, both system prompts, model route and batches. Keep judgments tied to the inputs they saw; do not attach cached judgments to changed definitions. |

The script's declared metadata filter—include JSON definitions whose `family` is absent, empty or `analytical`—is a legitimate scope choice, not code judging content. In this checkout that is **203 of 273 JSON definitions**, with **28 developed capability cards and 22 purpose-listed offers**. State those counts and the exclusions, rather than carrying forward the historical 275-engine estate count. If a mis-tagged workflow card enters this declared set, let the model identify the mismatch.

These validators may check IDs, JSON, family names, field types, reference membership, coverage and cache identity. They may not use keyword lists, score thresholds, current offering status, minimum method counts, or “looks like biography” heuristics to choose families, merges or verdicts. No runtime validation test here would certify semantic usefulness; this review performed static source inspection only.

## 5. How demand should enter the final decision

Preserve an independent account of what each definition answers, then put the [demand mapping](TRIAGE_demand_memo_codex_2026-09-05.md) beside the consolidation. Ask the model to record which reader promises each retained method serves and which remain unsupported. Do not turn recipe membership or the 14 reported jobs into a numerical retention score.

The immediate demand distinctions are case comparison versus comparison audit, cross-source reconciliation versus one-author conceptual development, and textual commitments versus unsupplied business obligations. The reusable reading duties are attribution, scope, genre-appropriate evidence, modal force, support in context, counter-evidence and valid absence. The [argument-family study](STUDY_argument_family_RESULTS_2026-09-05.md) shows that a critic can get these wrong even with valid quotes and strong ratings. The [frontier study](STUDY_frontier_SYNTHESIS_2026-09-05.md) supports checking and structured findings, not automatic retention of old questions.

Priority order for Claude's next revision: **remove the method quota and pre-decided causal merge; stop code-authored judgments; identify the active question set; provide evidence for nominated duplicates; validate complete, versioned dispositions.** Then the output can support the owner's whole-catalogue decision without silently deciding it in the prompt or parser.
