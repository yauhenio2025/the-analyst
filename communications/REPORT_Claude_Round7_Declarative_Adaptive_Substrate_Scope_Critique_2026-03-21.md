# Claude Critique: Round 7 / Declarative Adaptive Substrate Scope

Date: 2026-03-21
Reviewed memo: `communications/MEMO_2026-03-21_round7_declarative_adaptive_substrate_scope.md`

---

## Verdict

**Approve after revision**

The memo identifies the right next variable to isolate and the right first pilot target. The strategic judgment is sound: `genealogy_relationship_landscape` is the simplest mature adaptive seam, and making only the decision ladder declarative while keeping the signal extractor and builder templates in code is the correct minimum scope.

But the memo is too loose in five specific places that would cause friction or ambiguity during execution. Those need tightening before an execution plan can be written.

---

## Findings

### Finding 1: The "signal extractor" is not one function — it is a three-step pipeline, and the memo hides this behind a single key (Severity: Medium)

The memo proposes `signal_extractor_key` as a single field in the declarative spec, implying one named function that the runtime dispatches to.

In practice, the signal extraction for `genealogy_relationship_landscape` is three entangled steps:

1. **Card extraction**: `_extract_relationship_cards()` (line 1999) iterates `payload.items`, pulls `structured_data` from each item, and normalizes `work_title`.
2. **Card decoration**: `_decorate_relationship_card()` (line 2247) computes `_adaptive_score` using hardcoded weight tables (`_RELATIONSHIP_TYPE_WEIGHTS`, `_RELATIONSHIP_STRENGTH_WEIGHTS`), adds derived labels (`relationship_type_label`, `centrality_excerpt`), and generates `comparison_excerpt`.
3. **Signal aggregation**: Lines 634-656 of `_select_adaptive_relationship_surface()` rank cards by score, compute `score_total`, `top_share`, `score_gap`, count relationship types and strengths, and assemble the `signal_summary` dict.

The declarative spec's `signal_extractor_key: "relationship_cards"` would need a registry mapping that dispatches to this entire pipeline. That is a new abstraction layer — a signal extractor registry — that the memo does not acknowledge, let alone scope.

**Why this matters**: If execution begins without deciding whether the signal extractor is a single callable or a pipeline descriptor, the implementor will either (a) build an over-engineered registry or (b) hardcode the dispatch and undermine the "declarative" claim.

**What should change**: The memo should explicitly state that the signal extractor stays as a single named callable that performs all three steps, and that `signal_extractor_key` is a simple dispatch key to that callable — not a pipeline description. No signal extractor registry in round 7.

### Finding 2: The rationale strings are dynamic f-strings with interpolated signal values — not static templates (Severity: Medium)

The memo proposes `trace_rationale_template` and `description_template` as fields in the family catalog. This implies static strings.

The actual rationale construction (lines 1018-1081 of `_choose_relationship_surface_family`) uses Python f-strings with 3-5 interpolation variables:

```python
f"{dominant_work} clearly dominates the relationship field "
f"({round(top_share * 100)}% of weighted relationship strength, "
f"{score_gap} points ahead of the next work), so a single-work dossier is the clearest surface."
```

A declarative spec cannot reproduce these with static strings. It needs either:

1. A simple template syntax (e.g., `"{dominant_work} clearly dominates..."` with named placeholders)
2. The runtime to produce the rationale from a template + signal dict

Option 1 is the right choice for round 7 — it keeps the substrate bounded. But the memo needs to say this explicitly, including:
- What template syntax is used (Python `.format()` placeholders? Mustache? Something simpler?)
- What keys are available for interpolation (the `signal_summary` dict)
- How template rendering errors are handled (fail-closed with a fallback string, or validation error?)

Without this, the implementor has to invent a template rendering contract during execution.

### Finding 3: The rejected-family rationales are also dynamic and carry rejection-specific reasoning (Severity: Low-Medium)

Each return path in `_choose_relationship_surface_family` also returns a tuple of `AdaptiveRejectedFamily` instances with hardcoded reason strings:

```python
AdaptiveRejectedFamily(
    family=RELATIONSHIP_COMPARISON_REVIEW,
    reason="No side-by-side cluster is close enough to displace the dominant relationship.",
)
```

The memo's `families[]` spec doesn't mention rejected-family rationale templates. But the trace schema includes rejected families with reasons (visible in proof artifacts: `PROOF_round3_dossier_final_trace_2026-03-20.json`).

For trace equivalence, the declarative spec needs to declare what rejection reason each non-selected family should carry when a given decision rule fires. This could be a `rejection_reason` field on each family entry, or a per-rule rejected-family reason map.

The memo should add this to the family or rule schema. Without it, trace equivalence on rejected-family reasons is impossible.

### Finding 4: The config loading infrastructure does not exist yet, and the memo does not specify where the spec lives or how it is loaded (Severity: Medium)

The memo says "repo-tracked static configuration" but does not specify:

- **File location**: Is this `src/presenter/compositions/declarative_relationship_surface_v1.json`? A new `src/compositions/` folder? Inside `src/presenter/`?
- **File format**: JSON? YAML?
- **Loading mechanism**: Is it loaded at startup? Lazily on first request? Is there a registry pattern or just a direct file read?
- **Schema validation**: What validates that the loaded config has the required fields and legal values before it reaches the runtime?

The codebase has well-established registry patterns (engines, views, renderers, consumers — all follow the same JSON-file-in-definitions-folder + registry.py loader pattern). Round 7 should either reuse that pattern explicitly or state why it deviates.

**What should change**: The memo should specify one sentence on file location and one on the loading pattern. Recommend: `src/presenter/adaptive_specs/definitions/declarative_relationship_surface_v1.json` loaded by a thin `AdaptiveSpecRegistry` that validates the schema at load time with a Pydantic model. This keeps it consistent with the rest of the codebase.

### Finding 5: The comparison family is the default fallback, not a positive rule — the decision ladder is actually rule-rule-else, not rule-rule-rule (Severity: Low)

The memo says "one ordered decision ladder over supported metric predicates" with "first-match wins." The actual code has:

1. **Dossier**: `relationship_count == 1 or (top_share >= 0.45 and score_gap >= 5)` → `relationship_profile_dossier`
2. **Field map**: `relationship_count >= 5 or (count >= 4 and top_share < 0.5) or (count >= 4 and distinct_types >= 3)` → `relationship_field_map`
3. **Comparison**: anything else → `relationship_comparison_review` (default)

The "ordered first-match" framing is correct for rules 1 and 2, but rule 3 is an implicit else/default, not a predicate match. The declarative spec needs to declare which family is the default fallback. The memo's `decision_rules[]` should specify a `default_family` field separate from the predicate-based rules, or document that the last rule with no predicates is the fallback.

This is low severity because any reasonable implementation will handle it, but the memo should be explicit to prevent the implementor from inventing a "match-all predicate" hack.

### Finding 6: The equivalence standard references round-3 fixtures but no automated test path exists for them (Severity: Medium)

The memo proposes using `proof-round3-adaptive-dossier-final-1774002300` and `proof-round3-adaptive-comparison-final-1774002300` as the control pair.

But:

1. **No pytest integration tests reference these fixtures.** The existing tests in `test_manifest_trace.py` (lines 1056-1169) use heavily mocked unit tests with synthetic payloads, not the real fixtures.
2. **The round-3 proof was browser-automated** against the live local stack, not via pytest.
3. The fixtures live in the executor SQLite database, which is not committed to the repo.

So "test against round-3 fixtures" means one of:
- Writing new integration tests that load the fixtures from the database (requires the executor DB to be seeded — a prerequisite the memo doesn't mention)
- Repeating the browser-automation proof process
- Writing snapshot-style tests that compare hardcoded-mode output vs. declarative-mode output on in-memory synthetic payloads that reproduce the round-3 signal shapes

The third option is the most realistic for a bounded proof round. The memo should specify that equivalence testing uses **synthetic payloads that reproduce the round-3 signal distribution** (dossier-like signals for one, comparison-like signals for the other), not the literal database fixtures.

### Finding 7: The memo omits a preflight gate — the declarative spec schema must be reviewed before implementation (Severity: Low)

The memo sketches a shape (`composition_mode`, `workflow_key`, `target_surface`, `families[]`, `decision_rules[]`) but defers the precise schema to the execution plan.

Given that the schema IS the primary deliverable of round 7 (the runtime changes are straightforward), the schema should be a **preflight gate**: designed and reviewed as a separate artifact before any implementation begins. Otherwise the execution plan will bury the schema design inside a code task, and any review feedback on the schema will cascade into rework.

---

## What The Memo Gets Right

1. **Strategic judgment is correct.** After six rounds of proving adaptive behavior, the next meaningful variable is whether that behavior can be expressed declaratively. This is not another workflow expansion — it is a structural advancement.

2. **Pilot target is correct.** `genealogy_relationship_landscape` is the simplest mature seam: single surface, stable signals, three well-exercised families, no cross-surface coordination. The memo's reasoning for why NOT to start with a suite mode or AOI is sound.

3. **Scope discipline is excellent.** The memo explicitly rejects arbitrary expression languages, Python eval from config, JMESPath, user-authored code, and generated config. It explicitly keeps signal extraction, builder templates, validation, trace emission, and error mapping in code. This is the right level of ambition.

4. **The "what stays hardcoded" section is the strongest part of the memo.** It correctly identifies that the proof is not "can we data-drive everything" but "can we lift one decision pattern into config without weakening the runtime contract." That framing prevents scope creep.

5. **The equivalence standard is the right test type.** Behavioral equivalence against a known control is more meaningful than a novelty demonstration.

6. **The Critic boundary is correct.** One generic proof label, no workflow-specific host logic.

7. **The activation contract (`declarative_relationship_surface_v1` as a new independent mode token) is clean.** It doesn't stack with existing proof modes and doesn't replace them.

---

## What Must Be Revised Before Execution Planning

1. **Specify that `signal_extractor_key` is a simple dispatch key to a single callable, not a pipeline descriptor.** State: no signal extractor registry in round 7.

2. **Define the rationale template syntax.** At minimum: Python `.format()`-style named placeholders interpolated from the `signal_summary` dict. State how template rendering errors are handled (e.g., fallback to a static default string).

3. **Add rejected-family rationale to the spec shape.** Each family entry or each decision rule should declare what rejection reason applies for non-selected families. Without this, trace equivalence on rejected-family reasons is impossible.

4. **Specify file location, format, and loading mechanism for the declarative spec.** Recommend: JSON file in `src/presenter/adaptive_specs/definitions/`, loaded by a Pydantic-validated registry consistent with the existing codebase pattern.

5. **Clarify that the decision ladder has a default/fallback family, not just predicate rules.** Add a `default_family` field or document that the last entry with no predicates is the fallback.

6. **Specify the equivalence testing approach.** Recommend: synthetic payloads in pytest that reproduce the round-3 signal distributions, not dependency on the executor database fixtures.

7. **(Optional but recommended) Add a preflight gate**: declare that the Pydantic schema for the composition spec file is a reviewable artifact before code begins.

---

## Bottom Line

The memo identifies the right next variable, the right pilot target, and the right scope boundary. The strategic judgment is sound and the "what stays hardcoded" section is well-reasoned.

But the memo is too vague on five specific engineering questions (signal extractor abstraction, rationale templates, rejected-family reasons, config loading, equivalence testing) that would force the implementor to make design decisions during execution. Those decisions should be made in the scope memo, not discovered at implementation time.

With the seven revisions above, this becomes an execution-ready scope. Without them, it is a solid directional memo that will produce unnecessary rework in the first implementation session.
