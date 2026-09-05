# Next argument-family pair: framing and empty-result contract

Design note only. No runtime or definition change is made here. This follows the [prepared dialectical/counterfactual questions](REDESIGN_argument_family_PREPARATION_2026-09-05.md), not a new validation result.

## The inherited framing still predetermines a discovery

[`_framing`](../../src/stages/process_composer.py) at lines 89–98 inserts the **first paragraph** of the capability `problematique` under “The method,” before the process description. Neutral questions later in the prompt therefore do not replace that framing.

The [dialectical capability](../../src/engines/capability_definitions/dialectical_structure.yaml) opens by asserting that every significant work contains unresolved tensions, unrecognized contradictions, and dependencies on positions it opposes. It also describes those dependencies as secret. The next paragraph's “there always is” is not injected by this function, but the injected first paragraph already creates the problem. The prepared questions instead allow qualified compatibility, acknowledged appropriation, and no relevant relation.

The [counterfactual capability](../../src/engines/capability_definitions/counterfactual_analyzer.yaml) opens “Every causal claim harbors a hidden counterfactual,” then turns a causal assertion into a necessary but-for claim. That framing prejudges both the presence of a counterfactual and the particular dependence to extract. It does not fit the prepared distinction among causal counterfactuals, open conditionals, even-if concessions, reductios, and reconstructed conceptual dependencies.

Preserve these original capability texts for their baseline role. A bounded implementation would add an explicit process-level framing override, for example a proposed `process.framing` field, and have `_framing` use it when supplied. Retain the existing fallback for unaffected specifications. Merely appending a neutral description leaves the categorical opening active. The override must be included in the frozen prompt identity used for comparisons.

## Exact proposed process framing

**Dialectical Structure Mapper:**

> Examine which opposed positions or requirements, if any, organize the text's argument. Identify each position's owner, object, scope, modality, and argumentative stage. Determine whether their relation is a contradiction, a performative conflict, a practical tension, or compatibility clarified by a distinction. Trace how the text rejects, revises, mediates, or preserves the relation, and assess the warrant for that response and what remains unresolved. Selective borrowing and differences between stages may be coherent. Report no relevant instance when the inspected material supports that conclusion, stating the scope and limits of the search.

**Counterfactual Analyzer:**

> Examine the suppositions that do argumentative work in the text, if any. Distinguish an explicit counterfactual, an open conditional, an even-if concession, a reductio, and an analyst's reconstruction of a dependency. Preserve who makes the supposition, what is varied or granted, what is held fixed, and what conclusion is claimed. Assess the connecting warrant appropriate to the case: conceptual, causal, historical, or normative. Identify additional assumptions and independent support that survives their removal. Report no relevant instance when the inspected material supports that conclusion, stating the scope and limits of the search.

Both preserve substantive work without requiring a hidden defect. Ganzinger's act/concept contradiction and Elling's even-if concession remain positive cases; the contract must also admit texts without such argumentative operations.

## A negative finding requires its own account

Use a separate outcome record, not a fabricated `[F1]` scenario or contradiction. A proposed record should distinguish:

- **Analytical outcome:** `findings_present`, `no_relevant_instance`, or `inconclusive`.
- **Scope inspected:** source/document keys, dimensions and actual sections inspected; disclose exclusions or truncation.
- **Basis:** the eligibility criterion applied, any nearest candidate and why it does not qualify, and the limits of the conclusion. A nearby quote can support this explanation; it cannot prove universal absence.
- **Review state:** unchecked, supported within the stated scope, or disputed, with the review's own evidence and limits.
- **Execution and evidence state:** completed invocation, parsed response, source access and anchor results remain separate from the analytical outcome.

“No explicit counterfactual wording” is narrower than “no relevant supposition” under the proposed engine. “An apparent contradiction is resolved by a qualification” is normally a substantive dialectical finding, not an empty result. “No unrecognized contradiction” likewise does not mean that the paper contains no relevant opposition.

No parseable rows, truncated/missing source material, and all candidates lost to quote verification must remain distinct failure or inconclusive states. An explicitly reasoned no-instance claim can be unchecked; it cannot become checked merely because there were zero rows to reject. All candidates being rejected can support a negative outcome only where the stated coverage and reasons warrant it, not by row arithmetic alone.

## Required future behavior at the two current boundaries

[`run_oneshot_checked`](../../src/executor/process_runner.py) returns before checking when `not check or not rows` (line 543). A future no-instance route must distinguish “checking not requested” from “checking requested but no parseable findings,” and, when authorized checking is requested, review the negative claim against the inspected source and criteria. Until then, a zero-row response is not a checked absence finding.

Deep verification skips empty per-document rows (line 321), and synthesis raises when no rows survive (365–366). Preserve failures caused by lost evidence or failed extraction. Permit a separate negative-result assembly only after explicit scoped outcomes support it; do not relax the exception into an automatic absence result. In mixed corpora, retain negative, positive, and inconclusive document outcomes separately so that one silent document cannot disappear from the claimed coverage. A successful negative report should state what was sought, what was inspected, why no relevant instance was retained, and the remaining uncertainty, without manufacturing a normal findings ledger.
