# Codex Audit Report: Stage 5 AOI Source-Content Identity Revision Scope

Date: 2026-03-26
Auditor: Codex
Input memo: `communications/MEMO_2026-03-26_stage5_aoi_source_content_identity_revision_scope.md`
Verdict: `Approve with revisions`

## Findings

### 1. Critical: the memo does not state clearly enough that the first real contradiction is already present in raw Phase 1.0 AOI output

This is the most important correction.

The current memo correctly says the remaining blocker is content integrity, but it still frames the John O'Neill contradiction too loosely, as if it were mainly a saved-result or preview-surface problem. The local execution store shows the contradiction becomes real upstream in raw Phase `1.0` engine output for the fixed source run `job-6ee8b0621177`.

Observed local evidence:

- `executor_jobs.plan_data` for `job-6ee8b0621177` selects `otto_neurath`
- the same plan data lists Otto Neurath prior works, for example:
  - `Economic Writings Selections 1904 1945   Otto Neurath   Vienna Circle Collection   2004`
  - `Empiricism and Sociology   Otto Neurath   Vienna Circle Collection   1973`
  - `Modern Man in the Making   Otto Neurath   A. A. Knopf   1939`
- raw Phase `1.0` JSON outputs for `aoi_thematic_synthesis` include explicit contradictory identities:
  - `po-51c6f42e5434` has `selected_source_thinker.thinker_id = john_oneill`
  - `po-f2ad0c300c93` has `selected_source_thinker.thinker_id = aaron_benanav`
- those same rows already carry Otto at metadata-normalized top level, which proves the contradiction is not introduced first by presentation

This matters because the memo must tell implementers where to start. The first seam is not “presentation drift.” It is upstream AOI generation and/or prompt/example contamination, with later layers only propagating or masking it.

### 2. High: the memo under-specifies the normalization seam, which currently produces a mixed-truth artifact

The memo mentions normalization and contract validation, but it does not describe the most dangerous failure mode precisely enough.

`src/aoi/contract.py:167-210` rewrites top-level `selected_source_thinker` and top-level `source_documents` from plan truth, while separately normalizing theme-level `source_documents` and quotes from whatever the model emitted. In practice that creates a mixed artifact:

- top level says `otto_neurath`
- top-level source inventory is rewritten to Otto documents
- theme-level provenance can still point at wrong works or collapse to `unknown`

Observed local evidence:

- `analysis_artifacts` row `artifact-81ad935fe62dd5f017301bc3` for `job-6ee8b0621177` and family `aoi.source_thematic_map` has:
  - top-level `selected_source_thinker.thinker_id = otto_neurath`
  - top-level first source document title = `Economic Writings Selections 1904 1945   Otto Neurath   Vienna Circle Collection   2004`
  - theme-level source titles still include `beyond_capitalism_1` and `real_political_economy_technology`
- `phase_outputs` row `po-51c6f42e5434` has normalized theme source titles `oneill_market_1998` and `oneill_cost_benefit_1996`

That is not just a missing guardrail. It is a masking seam. The memo should name it directly.

### 3. High: the seam family is real and bounded, but the memo should separate three repair targets instead of grouping them too loosely

The memo is directionally right that this is a bounded AOI-specific slice. The likely seams are also real. But the repair plan should distinguish:

- upstream prompt/example contamination
- normalization fail-closed or contradiction suppression
- downstream report-summary semantic drift

Evidence for the upstream seam is especially strong:

- `src/engines/capability_definitions/aoi_thematic_synthesis.yaml:91-111` hard-codes `john_oneill` in the `output_contract`
- `src/stages/capability_composer.py:333-351` and `src/stages/capability_composer.py:500-523` inject that contract verbatim into the model prompt

Evidence for the downstream propagation claim is also strong:

- `src/presenter/composition_source_bridge.py:553-616` loads normalized AOI artifacts directly into `materialization_payload`
- `src/presenter/compose_from_intent.py:871-884` preserves source-family JSON as-is for structured views

So presentation may still need a fail-closed rule, but it is not the first cause.

### 4. Medium: the memo is not yet strict enough about explicit selected-source identity

Decision 4 is correct in principle, but it needs a harder definition.

The acceptable/invalid boundary should be:

- invalid:
  - explicit `selected_source_thinker` mismatch
  - explicit source-document inventory mismatch
  - theme-level provenance mismatch
  - representative quote provenance mismatch
- potentially acceptable:
  - prose mention of John O'Neill as an interpreter, only if no explicit identity-bearing field contradicts plan truth

Without that stricter rule, the memo risks allowing a report to look “mostly Otto” while still carrying contradictory provenance inside theme data.

### 5. Medium: the memo should make recovered-run reuse criteria more explicit

Decision 7 is right to keep reuse separate from rerun authorization, but it should say more clearly:

- if the fix is only projection-time suppression or presentation-time fail-closed behavior, the recovered run may become display-safe without becoming closure-grade evidence
- if raw Phase `1.0` AOI output remains materially wrong, an honest Stage 2 closeout likely still requires a post-repair fresh rerun

That distinction matters because the current artifact trail already shows the raw seam upstream.

### 6. Low: Stage 2 / Tranche 3 sequencing remains honest

The memo is sound on program order.

The supporting roadmap and rubric materials are consistent with:

- browser/host continuity now being sufficiently evidenced
- content-level selected-source integrity remaining the actual Stage 2 blocker
- Tranche 3 still being blocked until this AOI exemplar seam is either repaired or explicitly re-scoped

I found no evidence that this memo is smuggling in a premature Stage 2 closure or Tranche 3 pivot.

## Direct Answers

### Is this the right next honest step?

Yes.

Another browser-host slice is not the next honest step. The evidence already shows the repaired host path preserves row pinning, cache reuse, source job identity, and compose continuity. The remaining blocker is source-content identity integrity inside the AOI artifact chain.

### Is the fixed-source rule sound?

Yes.

Keeping diagnosis pinned to `job-6ee8b0621177` is technically sound because the local stored evidence is already sufficient to identify the first real seam and measure how it propagates.

### Are the seam families real and bounded?

Yes, with one addition and one sharper separation.

Real bounded seams:

- capability/example contamination in AOI thematic synthesis prompting
- AOI normalization and artifact persistence behavior
- report-summary semantic drift
- presentation fail-closed behavior for contradictory explicit identity

Missing explicit seam:

- top-level override masking that rewrites selected-source truth at the artifact top level while leaving deeper provenance polluted

### Is the memo strict enough about explicit selected-source identity?

No.

It is close, but not yet strict enough about theme-level provenance, representative quotes, and any other explicit identity-bearing fields below the top-level selected thinker field.

### Are deeper seams missing?

Yes, two are missing or under-described:

- raw Phase `1.0` contradiction as the first true seam
- mixed-artifact normalization masking as a distinct failure mode

### Is the Stage 2 / Tranche 3 sequencing honest?

Yes.

### Is the scope technically bounded and implementation-worthy?

Yes, with revisions.

This is a bounded implementation slice. It is narrow enough to execute without reopening host/browser proof, generalized prompting redesign, or Tranche 3 scope.

## Required Memo Revisions

### 1. Revise the summary and Decision 3 to name the first real seam explicitly

Add a direct statement that the first observed contradiction is already present in raw Phase `1.0` `aoi_thematic_synthesis` outputs for `job-6ee8b0621177`, not first in presentation.

### 2. Add a distinct seam family for normalization masking

State explicitly that current normalization:

- overwrites top-level selected thinker and top-level source inventory from plan truth
- does not guarantee theme-level provenance consistency
- can therefore create a mixed-truth artifact that looks repaired at top level while remaining semantically corrupted underneath

### 3. Tighten the explicit identity rule

Replace the current broad distinction with a stricter test:

- any explicit selected-source field, source-document inventory, theme provenance field, or representative quote provenance that contradicts plan truth is invalid
- interpretive prose mention of another thinker is only acceptable when it does not create any explicit identity contradiction anywhere in the structured payload

### 4. Separate repair targets in the implementation section

Do not treat all likely fixes as one bucket. Require the implementation closeout to say which of these was actually repaired:

- prompt/example contamination
- normalization/persistence contradiction handling
- report-summary drift
- presentation fail-closed guardrail

### 5. Strengthen the diagnosis artifact requirement

Require one trace artifact that compares, for the same fixed run:

1. plan-selected thinker and source-corpus truth
2. raw Phase `1.0` AOI thematic output
3. normalized thematic artifact
4. Phase `4.0` report summary payload
5. composed presentation payload

The goal is to force an explicit statement of where contradiction first appears and how later layers transform it.

### 6. Expand regression expectations

Add test cases proving:

- contradictory raw `selected_source_thinker` cannot survive normalization silently
- theme-level `source_documents` cannot name works outside the selected thinker corpus without fail-closed behavior
- representative quotes cannot preserve mismatched `source_work_title` provenance silently
- report payloads cannot preserve explicit selected-source contradiction through normalization

### 7. Clarify recovered-run reuse criteria

State that:

- display-safe reprojection is not the same as closure-grade rehabilitation
- if the raw stored AOI outputs are materially wrong, a fresh execution-backed rerun is likely still required after the bounded repair

## Approval Decision

`Approve with revisions`

This is the right next bounded implementation slice, the fixed-source rule is sound, and the program sequencing is honest. But the memo should be revised before implementation so it accurately names the first real seam, explicitly describes normalization masking, and tightens the definition of invalid explicit selected-source identity.
