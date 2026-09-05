# Process framing and scoped empty outcomes

Date: 2026-09-05. Review state: independently reviewed, applied to main, and tested in a fresh main interpreter. The implementation was prepared in the isolated worktree `argument-outcomes-2026-09-05`. No candidate is registered or certified by this change. No model or provider calls were made.

The worktree began at `3426419` and was deliberately updated to `12d7a3c` to retain the new ruling-coverage diagnostics. The four overlapping runner hunks preserve both functions: positive-row ruling coverage remains distinct from a scope review. Existing production operationalizations are unchanged.

## Explicit activation

`ProcessSpec` now accepts two independent fields:

```yaml
process:
  framing: >-
    Do not presuppose a qualifying instance. Apply the eligibility criterion
    stated in this framing and in each method card.
  scoped_outcomes: true
```

`framing: null` preserves the capability opening. An explicit string replaces that opening in extraction, verification, synthesis and oneshot prompts, including the system prompt reused for re-anchoring. Description, questions and method cards remain explicit process inputs. The code does not select an eligibility criterion from an engine name or judge whether the criterion fits a source.

`scoped_outcomes` defaults to false. Enabling it removes positive row minima and makes a separate scope report mandatory. The candidate YAML files' proposed metadata must be deliberately moved into these supported process fields after acceptance; arbitrary metadata is not activation. No production registry entry changes here.

## Scope contract

The model returns a separate `## Scope outcomes` JSON array alongside a possibly empty findings ledger. Each object identifies one dispatched document/dimension scope; a corpus dimension names the supplied document keys. Objects report `findings_present`, `no_relevant_instance` or `inconclusive`, inspected sections, reported coverage (`complete`, `partial`, `unknown`), eligibility criterion, basis, limitations and finding IDs. A review additionally supplies `review_state` and a distinct `review_basis`.

The reader cannot certify its own assessment: its review state and review basis are reset before the critic sees them. The critic must explicitly review each scoped claim, including zero-row claims. Missing records or review reasons remain unchecked and inconclusive. Code checks record shape, exact document/dimension identity and surviving evidence references. Missing or unknown row dimensions cannot silently coexist with a supported negative in the same source scope. Finding references cannot borrow another document's evidence. Cross-document findings continue through the existing wall that checks every required document-keyed anchor.

Coverage is a reader/reviewer report. Source availability and successful quote matching do not establish whole-paper inspection. Every displayed negative is expressly limited to its reported inspected sections. The initial corpus extraction receives earlier ledgers and scope reports; its receipt explicitly identifies that indirect material. A corpus critic subsequently receives the source texts.

Malformed or missing scope JSON, malformed empty extraction, known partial/error responses, and lost anchor evidence produce visible inconclusive records. A failure assigned to document A does not invalidate document B's same-dimension scope. Unassigned evidence is treated conservatively in the affected source scopes. Missing or empty selected source text is refused before a call. Known `partial`, `stop_reason`, `error` and `connection_error` values are captured before the invocation result is discarded. A re-anchor response and its invocation flags remain in the extraction receipt.

## Empty and mixed execution

With this explicit opt-in, oneshot checking runs even with zero finding rows. Deep verification similarly runs for empty document and corpus scopes. Synthesis may proceed without surviving positive rows when it has the scope inventory; ordinary processes retain their prior empty-extraction guard and oneshot call count.

Deep synthesis receives all retained positive findings plus the full scope inventory. It cannot replace or upgrade those recorded assessments. The product appends a deterministic plain-language scope report, so omitted negative or inconclusive documents remain visible even when the model's synthesis discusses only a positive document. Multiline model-supplied report text is rendered on one line per field so it cannot become an apparent ledger row. Original JSON and raw response text remain in receipts.

The chain adapter saves the derived scoped product after the raw calls, as it already does for an applied checked ledger. This adds no model call or token charge. Raw `StepCall.content` is preserved. A zero-row checked product says that there were no original finding rows and points to the scope review; it does not print a misleading “0 of 0” incomplete-check warning. The generic positive-row coverage helper and its diagnostic fact remain unchanged.

## Evidence and limits

The focused command was:

```bash
TMPDIR=/home/evgeny/projects/the-analyst-wt/ideas-test-tmp python -m pytest -q \
  tests/test_scoped_outcomes_2026_09_05.py \
  tests/test_process_shape_2026_09_04.py \
  tests/test_corpus_ledger_2026_09_05.py \
  tests/test_anchor_repairs_2026_09_05.py \
  tests/test_ruling_coverage_2026_09_05.py \
  tests/test_workflow_corpus_dispatch.py --disable-warnings --maxfail=3
```

Result: **235 passed, 91 warnings**. There are 51 new scoped-outcome cases, including 68 full composed-prompt hashes for the four current production engines under one- and two-document inputs. All 68 match the pre-change `3426419` baseline. Existing wall, ruling-coverage and workflow-dispatch cases pass after integration with `12d7a3c`. The tests forbid real provider access and exercise both runner boundaries, mixed corpus, raw/persisted output distinctions, scope identities and paired anchors.

This implementation does not establish semantic absence, actual full-text inspection, or a model's honest application of its eligibility criterion. Unknown upstream source truncation cannot be inferred from a supplied string. Known provider interruption is retained; absent invocation metadata stays unknown. Earlier malformed-record or lost-evidence limitations propagate conservatively, even if a subsequent reviewer asserts a negative; there is no automatic semantic recovery or extra adjudication call.

Recognizable Scope outcomes headings, including malformed fences under those headings, are removed from the derived reader product and retained raw. Completely unrecognizable malformed response material can remain in the original reading; this is not a general prose sanitizer. The accompanying assessment remains inconclusive when its required scope records cannot be parsed. Synthesis prose can still contradict a scope report or misuse a source; the report prevents omission and records limits, but does not semantically rewrite prose. Final synthesis invocation problems and wall failures remain in its receipt. Desks continue to use anchored ledger findings; scope records are reports, not new citable claims.

## Main acceptance

Root reviewed the runtime, composer, persistence and scope-validation changes; a second reader independently checked negative-scope promotion. The accepted patch SHA-256 is `83606290ea04267e483c974416e375ece023a19efdf1479955fbce99a5550b5e`, based on `12d7a3c`. All eight applied file hashes matched the review manifest before this acceptance note was added. The same 235-test command passed in a fresh main interpreter, and a separate composer-first import check confirmed the default opt-in fields remain disabled. The 68 existing production prompt hashes still match. No paid call or production engine activation occurred.
