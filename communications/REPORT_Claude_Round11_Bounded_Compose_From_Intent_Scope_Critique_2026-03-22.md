# Review: Round 11 / Bounded Compose-From-Intent Scope

Reviewer: Claude Opus 4.6
Date: 2026-03-22
Documents Reviewed:
- `communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_scope.md`
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `communications/MEMO_2026-03-21_round9_renderer_contract_validation_completion.md`
- `communications/MEMO_2026-03-22_round10_consumer_consolidation_completion.md`
Code Seams Inspected:
- `src/api/routes/presenter.py`, `src/api/routes/views.py`, `src/api/routes/view_patterns.py`
- `src/api/routes/renderers.py`, `src/api/routes/transformations.py`
- `src/presenter/schemas.py`, `src/presenter/presentation_api.py`, `src/presenter/manifest_builder.py`
- `src/views/generator.py`, `src/views/pattern_schemas.py`, `src/views/patterns/*.json`
- `renderers-ui/src/index.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/ViewRenderer.tsx`

Perspective docs: No dedicated Perspective folder or documentation exists in or near this repo.

---

## Verdict: Approve after revision

The direction is right, the timing is right, and the hard stops are well-placed. This is the correct next move per the roadmap, and the memo is honest about the current codebase in most respects.

But the memo underestimates the engineering surface of the new orchestration layer it requires, and leaves two structural questions unresolved that will block planning if not addressed in the scope memo itself.

---

## What The Memo Gets Right

**1. Roadmap sequencing is exactly correct.**

The post-round-8 roadmap said: renderer contracts → consumer consolidation → bounded compose-from-intent. Rounds 9 and 10 closed the first two. Round 11 targeting compose-from-intent is on schedule and on trajectory. No intervening step was skipped.

**2. The transient-contract decision is the single most important call in the memo, and it is correct.**

`PagePresentation` is deeply job-bound. Its required fields include `job_id`, `plan_id`, `prepared_at`, `execution_summary`, `refinement_applied`, and `refinement_summary`. The assembly path (`assemble_page()` in `presentation_api.py`) takes `job_id` as its primary argument and loads from `phase_outputs`, `presentation_cache`, and artifact stores — all job-scoped.

Stuffing synthetic values into these fields would be technically possible but architecturally dishonest. A sibling contract that is explicitly non-job-backed is the right call. This prevents compose-from-intent from corrupting the meaning of the existing presenter API surface.

**3. The existing primitives inventory is accurate.**

The memo correctly identifies what already exists:
- `POST /v1/transformations/execute` is truly stateless (accepts raw `data`, no job dependency)
- `POST /v1/views/generate` is single-view, pattern-based, ephemeral by default (`save=false`)
- `POST /v1/renderers/recommend` is LLM-powered and already returns scored recommendations
- The six view patterns listed (`accordion_sections`, `card_grid_grouped`, `card_grid_simple`, `prose_narrative`, `tab_with_children`, `timeline_sequential`) match the repo exactly
- `POST /v1/presenter/compose` means something entirely different (job-bound refine + prepare + assemble)

The memo does not overstate what exists.

**4. The "not yet real" list is accurate and complete.**

The memo correctly identifies four gaps:
- No `compose-from-intent` endpoint
- Existing compose is job-bound
- No transient page-assembly contract
- Narrow pattern coverage (six generic patterns)

All four are real.

**5. Hard stops are well-placed and the right ones.**

Blocking genealogy compose-from-intent, engine selection, job creation, persistence, auto-polish, style-token unification, and broad "ephemeral apps" claims is exactly right. Each of these is a real drift risk for this kind of round.

**6. AOI is the correct proof slice.**

AOI has round-9 renderer-contract enforcement, round-10 package-backed consumption, and the generic bounded-v2 workspace. Genealogy still carries unresolved sub-renderer-law and view-key override questions. No other proof surface exists where compose-from-intent can land without collateral risk.

---

## Findings

### Finding 1 (High): The memo underestimates the multi-view orchestration layer

The memo frames compose-from-intent as "orchestration glue plus one bounded transient assembly seam" (line 140). This is directionally true but understates the engineering surface.

**What the existing primitives actually do:**

| Primitive | Scope | What it does NOT do |
|---|---|---|
| `POST /v1/views/generate` | Generates **one** view from **one** pattern + **one** engine | Does not plan a multi-view page structure |
| `POST /v1/renderers/recommend` | Recommends renderers for **one** view context | Does not coordinate across multiple sections |
| `POST /v1/transformations/execute` | Transforms **one** data payload | Does not batch N transformations for N views |
| `build_effective_manifest()` | Builds manifest for job-sourced payloads | Does not accept externally-assembled payloads |

**What compose-from-intent actually requires:**

1. **Page-structure planning**: Given N prose sections with engine provenance, decide how many views to generate, which patterns to use for each, and how to structure the parent-child hierarchy. This is a new LLM orchestration call — not a primitive that exists today.

2. **Multi-view generation**: Call `generate_view()` N times (or in parallel) with appropriate pattern assignments from step 1. The current generator is single-view; the batch loop is new.

3. **Multi-view transformation**: For each generated view, transform the corresponding prose section into structured data matching the view's renderer expectations. N transformation calls. The existing execute endpoint handles one at a time.

4. **Transient page assembly**: Collect the generated views + transformed data into a view tree with parent-child relationships, apply consumer adaptation, run renderer-contract validation. The existing assembly path is job-bound; the transient assembly is new.

The memo acknowledges this implicitly ("orchestration glue") but the word "glue" understates it. Step 1 — the page-structure planning call — is a real architectural decision and likely an LLM call of its own. The memo should name it explicitly and decide whether it belongs in the presenter layer or in a new orchestration module.

**Required revision:** Add a section that names the page-structure planning step as the primary new component, not just "glue." Clarify whether this planning step is LLM-driven (likely) or heuristic-only (unlikely to be sufficient).

### Finding 2 (High): ViewPayload reuse is under-specified

The transient contract needs to return render-ready views. The memo says the shape should be "presenter-facing and render-ready, view-tree based, consumer-adapted, renderer-contract validated" (lines 213-217).

The current `ViewPayload` (in `src/presenter/schemas.py`) is the natural candidate for the view-level unit inside the transient contract. Its fields are mostly render-focused: `view_key`, `view_name`, `renderer_type`, `renderer_config`, `structured_data`, `children`, etc.

But `ViewPayload` also carries job-bound fields:
- `phase_number: Optional[float]`
- `engine_key: Optional[str]`
- `chain_key: Optional[str]`
- `scope: str = "aggregated"`
- `raw_prose: Optional[str]`
- `prose_ref_view_key: Optional[str]`
- `items: Optional[list]`

The memo should decide:

(a) **Reuse ViewPayload as-is** for the transient contract, allowing job-bound fields to be `None`/default. Pragmatic, avoids type proliferation, but muddies the contract.

(b) **Define a narrower TransientViewPayload** that carries only the render-essential fields. Cleaner contract, but more new code.

(c) **Use ViewPayload internally but serialize to a narrower response shape.** Best of both worlds but requires an explicit mapping.

This is a planning-phase decision, but the scope memo should state the tradeoff explicitly so the planner knows what to propose.

**Required revision:** Name this decision as one the execution plan must resolve. State the tradeoff.

### Finding 3 (Medium): The proof standard needs to specify prose sourcing

The proof standard requires "at least two AOI control requests: one dossier-like / narrative-heavy input, one comparison-like / structured multi-section input" (lines 315-318).

But compose-from-intent takes raw prose sections as input. Where do these come from?

Options:
1. **Extract from existing AOI job outputs** — take the round-5/6 control job prose and feed it back through compose-from-intent as if it were fresh input
2. **Synthetic canned prose** — write test prose sections for the pilot
3. **Live engine execution** — run AOI engines on a document and use the output (but the memo blocks job creation / engine execution as out of scope)

Option 1 is the natural choice — it reuses existing documented control material and makes the proof comparable to rounds 9 and 10. But the memo should state this explicitly, or the planning phase will need to invent a sourcing strategy.

**Required revision:** Specify that the documentary proof should reuse prose from existing AOI control jobs (or state the alternative).

### Finding 4 (Medium): Consumer adaptation path needs acknowledgment

The existing consumer adaptation path (`adapt_renderer_for_consumer()` + `ConsumerRegistry`) is wired into `build_effective_manifest()`, which is job-bound. The transient compose-from-intent path still needs consumer adaptation — the whole point is that the output is consumer-ready.

The memo says the transient contract should be "consumer-adapted" (line 215) but does not acknowledge that the existing adaptation machinery will need to be extracted or called from a new context. This is not a large amount of code, but it is a real integration point that the execution plan needs to account for.

### Finding 5 (Medium): Renderer-contract enforcement on the transient path needs explicit mention

Round 9 added serve-time renderer-contract enforcement in `build_effective_manifest()`. The memo says the transient contract should be "renderer-contract validated" (line 216). Good — but the enforcement is currently wired into the job-bound manifest builder. The execution plan will need to either:

- Extract the enforcement helper into a shared function callable from both the job-bound and transient paths
- Or duplicate it (bad)

`src/presenter/renderer_contract_enforcement.py` already exists as a somewhat standalone helper, but its current allowlist is mode-based (`adaptive_aoi_theme_report_suite_v1`). The transient path needs its own enforcement entry or a generalized allowlist strategy.

The memo should flag this as a known integration point.

### Finding 6 (Low): The `timeline_sequential` pattern caveat is reasonable but conservative

The memo says `timeline_sequential` should only be included if the proof slice requires it (lines 256-257). This is fine for scoping, but the AOI proof slice is unlikely to exercise timeline rendering. Keeping it available as an allowed pattern costs nothing and lets the LLM page-planner use it if the input prose sections suggest temporal structure.

This is a minor point — the execution plan can decide.

### Finding 7 (Low): No Perspective docs exist

No dedicated Perspective folder or documentation exists in `/home/evgeny/projects/analyzer-v2/` or `/home/evgeny/projects/`. The term "perspective" appears in the codebase only as a synonym for analytical stance, not as a formal entity type.

---

## Bottom Line

The memo is directionally right on all major calls:

- Compose-from-intent is the correct next move after rounds 9 and 10
- The transient-contract decision is the most important scoping call and it is correct
- AOI is the right proof slice
- The hard stops are well-placed
- The primitives inventory is accurate

The memo needs three revisions before turning into an execution plan:

1. **Name the page-structure planning step explicitly.** This is the primary new component — an LLM call that takes N prose sections and produces a page plan (which patterns, which views, what hierarchy). Calling it "glue" understates it. The execution plan cannot be written without knowing this step exists and what it requires.

2. **State the ViewPayload reuse tradeoff.** The transient contract needs render-ready views. Should it reuse `ViewPayload` with nullable job fields, define a narrower type, or serialize differently? This is a planning decision, but the scope memo should name the tradeoff.

3. **Specify prose sourcing for the documentary proof.** The natural choice is reusing prose from existing AOI control jobs. State this explicitly so the proof is reproducible and comparable to rounds 9-10.

With those three additions, the memo is ready for an execution plan. The round is well-scoped, well-timed, and honest about the current state of the codebase.
