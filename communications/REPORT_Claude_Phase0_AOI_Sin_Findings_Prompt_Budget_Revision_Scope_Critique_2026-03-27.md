# Critique: Phase 0 AOI Sin-Findings Prompt-Budget Revision Scope

Date: 2026-03-27
Reviewer: Claude Opus 4.6
Status: Scope critique with codebase verification

## Verdict: Approve after revision

The memo correctly identifies the next honest step and stays properly bounded. The diagnosis of the failing seam is accurate. However, the memo is missing a critical structural observation about prompt composition that would significantly simplify the repair, and it over-reads the historical plan precedent in a way that could misguide implementation.

---

## Finding 1: The memo underspecifies the dominant inflation source (Severity: High)

The memo identifies `requires_full_documents = true` as part of the seam but does not trace through the code to explain what that flag actually causes for Phase 3.0.

In `phase_runner.py:875-881`, Phase 3.0's document text assembly is hardcoded:

```python
if phase_number == 3.0:
    return (
        f"# Subject Corpus: {target_title}\n\n{target_text}\n\n"
        f"---\n\n"
        f"# Selected Source Thinker: {selected_source_thinker_name}\n\n"
        f"{source_corpus}"
    )
```

This concatenates:
- Benanav target corpus: ~274K chars (~68K tokens)
- Full Neurath source corpus (4 volumes): ~3.6M chars (~900K tokens)

So the `user_message` alone is ~3.9M chars (~968K tokens). Add the system prompt (~1K tokens), upstream context from Phase 1.0 and 2.0 (~25K tokens at 50K chars/block × 2), and inner-pass context — and the total exceeds 1M tokens.

The dominant source of inflation is not generic context assembly or plan defaults. It is the hardcoded Phase 3.0 branch in `_get_standard_phase_document_text()` that sends the entire raw source corpus as part of the user message.

**Why this matters for the repair**: The memo lists several possible repair loci (plan generation, phase-execution input shaping, context assembly, engine input contract) without ranking them. The codebase makes it clear that the single most impactful lever is whether Phase 3.0 receives the raw source corpus at all. Upstream Phase 1.0 has already synthesized the source corpus into a thematic inventory, and Phase 2.0 has already mapped engagement patterns. Phase 3.0 may not need to re-read 3.6M chars of raw source text to produce honest sin findings — it could work from the pre-digested upstream outputs plus the 274K-char target text alone.

**Recommended revision**: Add a specific diagnostic question to Decision 4: "Does Phase 3.0 genuinely need the raw 3.6M-char source corpus for sin-finding provenance, or can it produce honest findings from the Phase 1.0 thematic synthesis + Phase 2.0 engagement map + the target text alone?" If the answer is "upstream context suffices," the repair is a one-line change: set `requires_full_documents = false` for Phase 3.0 in the plan.

## Finding 2: The historical plan precedent is over-read (Severity: Medium)

The memo claims that `plan-12e3db25fb90` "inserted source-corpus profiling because the same Neurath corpus was too large for raw whole-corpus handling."

This is partially correct but misleading. Reading both plans side by side:

- **plan-12e3db25fb90** added Phase 0.5 "Source Corpus Profiling" (`iteration_mode: "per_work"`) to pre-digest each Neurath volume for Phase 1.0's thematic synthesis. This solved Phase 1.0's context problem.
- **plan-12e3db25fb90** still set Phase 3.0 with `requires_full_documents: true`, `chapter_targets: null`, `document_scope: "whole"` — identical to plan-54b6f075fdf2.

So the earlier plan would likely have hit the same 1M-token ceiling at Phase 3.0. The precedent proves the planner was aware of corpus scale for Phase 1.0, but it does NOT prove the planner solved the Phase 3.0 budget problem. The two plans differ in Phase 0.5 strategy (source profiling vs. target profiling) but converge on the same Phase 3.0 configuration that blew up.

**Recommended revision**: Weaken the precedent claim. Replace "the same Neurath corpus was too large for raw whole-corpus handling" with "the earlier plan recognized the corpus was too large for Phase 1.0 raw handling but still sent the full corpus to Phase 3.0 — suggesting the planner does not yet reason about per-phase prompt budgets."

## Finding 3: Multi-pass amplification is unmentioned (Severity: Medium)

The `aoi_sin_findings` operationalization at `deep` depth runs 3 passes (`aoi_sin_findings.yaml:54-67`):

1. Pass 1: `discovery` (consumes_from: [])
2. Pass 2: `inference` (consumes_from: [1])
3. Pass 3: `integration` (consumes_from: [1, 2])

Each pass receives the same `document_text` as the `user_message` (`chain_runner.py:365`). The budget failure occurs at Pass 1 (Finding Discovery), so Passes 2 and 3 are never reached. But if the repair reduces document text just enough for Pass 1 to succeed, Pass 3 would receive the same document text PLUS inner context from Passes 1 and 2, potentially re-exceeding the budget.

The memo does not mention this secondary amplification risk.

**Recommended revision**: Add a note in Decision 5 that the repair must be validated against all 3 passes at deep depth, not just Pass 1.

## Finding 4: Upstream context cap is already bounded but still contributes (Severity: Low)

`context_broker.py:22` sets `MAX_CHARS_PER_BLOCK = 50_000`. Phase 3.0 depends on Phase 1.0 and Phase 2.0 (`plan-54b6f075fdf2`, line 152-155). So upstream context adds at most ~100K chars (~25K tokens).

This is a secondary contributor — the dominant issue is the ~3.9M-char document text — but it still matters at the margin. The total is: 968K (document) + 25K (upstream) + ~1K (system) ≈ 994K tokens, which alone should be under 1M. The measured value of 1,037,154 tokens suggests the actual upstream context or system prompt may be larger than the caps imply, or the token-to-char ratio for this content is higher than 4:1.

The memo correctly identifies upstream context shaping as a possible lever but does not do the arithmetic to show its relative contribution.

**Recommended revision**: No change needed, but the implementation should log the exact char counts at each component (system prompt, upstream context, document text) before the LLM call to enable precise diagnosis.

## Finding 5: The document assembly function has no plan-level control (Severity: Medium)

The `_get_standard_phase_document_text()` function in `phase_runner.py:827-883` uses hardcoded `if phase_number == 1.0` / `if phase_number == 3.0` branches to decide what documents to include. There is no mechanism for the plan to control document assembly per phase.

This means:
- Setting `requires_full_documents = false` in the plan for Phase 3.0 would not automatically remove the source corpus from Phase 3.0's document text — the hardcoded branch at line 875 triggers on `phase_number == 3.0` regardless of `requires_full_documents`.
- Actually: looking more carefully, the `requires_full_documents` flag only affects whether the 1M context beta is used (`config["use_1m_context"]` in `engine_runner.py:136`). It does NOT control what text is assembled.

**This is critical**: The memo assumes `requires_full_documents` controls document assembly, but in the code it only controls whether to use the 1M-token Anthropic beta endpoint. The actual document assembly is hardcoded by phase number. Setting `requires_full_documents = false` would just switch to the standard 200K context window while still sending 3.9M chars of text — making the failure even worse (rejected at 200K instead of 1M).

**Recommended revision**: Add this observation explicitly. The repair must touch either `_get_standard_phase_document_text()` to change what text Phase 3.0 receives, or the plan shape to bypass the hardcoded Phase 3.0 branch.

## Finding 6: Chunking is disabled but exists as a fallback (Severity: Low)

`engine_runner.py:98`: `CHUNK_THRESHOLD = 999_999_999` — effectively disabled. The code comment explains: "whole-book approach is ~13x FASTER than chunking."

Re-enabling chunking for Phase 3.0 would be a valid repair path but has quality implications: chunked extraction splits the source corpus into pieces and synthesizes results, potentially losing cross-document provenance that the sin-findings engine needs. The memo does not mention chunking as a repair lever.

This is fine — chunking is probably the wrong approach for this engine. But the implementation team should be aware it exists if other approaches fail.

## Finding 7: The fail-fast law (Decision 6) is well-motivated but underspecified (Severity: Low)

The memo correctly identifies that `engine_runner.py:301-302` only catches `prompt is too long` after the provider rejects the request. Decision 6 asks for an earlier fail-fast.

The natural place for this is at the top of `run_engine_call()` (after line 229 where `total_input_chars` is already computed). A simple `chars // 4 > 900_000` check would catch the most obvious budget overruns. The memo leaves this as "one of these should be true" without specifying where the guard should live.

**Recommended revision**: Specify that the fail-fast check should go in `engine_runner.py` at the existing `total_input_chars` computation point (line 209), using a conservative token estimate.

---

## Direct Answers

### Is this now the right next honest step?

**Yes.** The discovery seam is repaired. The browser/host seams are closed baseline. The failing seam is unambiguously in analyzer-side prompt composition for Phase 3.0. No other path makes progress toward an honest Phase 0 closure.

### Does the memo stay properly bounded?

**Yes, with the revision.** The boundary constraints (Decisions 1-3, 5, 7) are well-drawn. The only scope risk is that the memo's repair lever list is too broad — it could invite open-ended exploration across planner, executor, and engine prompt composition when the actual dominant repair is narrower (what document text Phase 3.0 receives).

### Is this the right sequencing relative to Phase 1?

**Yes.** Phase 0 cannot close until Phase 3.0 succeeds. Phase 1 should not start before Phase 0 closes. The memo holds this boundary explicitly.

---

## Concrete Memo Revisions Before Implementation

1. **Add the arithmetic** to Decision 4: state explicitly that the dominant inflation source is the hardcoded Phase 3.0 document assembly in `phase_runner.py:875-881`, which sends ~3.9M chars (~968K tokens) of raw document text before any upstream context is added.

2. **Correct the `requires_full_documents` misconception**: Note that this flag controls the 1M beta endpoint selection, not document assembly. Document assembly for Phase 3.0 is hardcoded by phase number.

3. **Weaken the plan-12e3db25fb90 precedent**: That plan also sent full documents to Phase 3.0 and would likely have hit the same ceiling.

4. **Add multi-pass validation requirement**: The repair must survive all 3 passes at deep depth (discovery, inference, integration), not just the first pass.

5. **Rank the repair levers**: The most impactful and simplest lever is changing what document text Phase 3.0 receives. If the sin-findings engine can produce honest findings from upstream thematic synthesis + engagement map + target text (without re-reading the raw 3.6M-char source corpus), the repair is minimal. If it genuinely needs raw source passages for provenance, a more involved pre-digestion or selective-document approach is needed.

6. **Specify the fail-fast location**: `engine_runner.py` line ~209, using the existing `total_input_chars` computation.
