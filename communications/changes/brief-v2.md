# brief v2 — the deliverable-first brief (as implemented)

> Branch `feat/brief-v2`, 2026-09-03. Implements `communications/DESIGN_brief_deliverables.md` §B–§E (smallest viable first).
> The owner's rule: *"focus on the deliverables and what it will change in their action, more than anything else."*

**Plain-language summary.** Step 2 of The Analyst no longer offers three topics dressed with engine names at one price. Each option is now a promise about use — *what you get*, *what you will understand*, *what you will be able to do* (each line pointing at the table/section/figure that keeps it), *what it will not tell you* — with its own shape (tables with a row unit, figures with a format), its evidence base, its own priced path, and a recommendation the desk explains in the reader's terms. Three ways in: say what you will use it for; pick the analysis yourself from a purpose-first catalog; let the material decide. Code checks the nine rules and sends violations back once; the arithmetic (prices, caps, references, vocabulary ban-list) is code, the judgment stays in the model.

Samples (real calls): `communications/changes/brief-v2-samples/{fashion,kering,state_capitalism}.json`. Screens: `web/docs/screens/brief-v2-{1-library,2-picker,3-brief}.png`.

---

## 1. Contract as implemented

### 1.1 Schema — `src/dossier/schemas.py`

```
DELIVERABLE_KINDS  stress_test decision_memo briefing playbook comparison watchlist reading_guide decoder risk_register case_file
USE_KINDS          decide brief prepare stress_test compare watch learn argue
ENTRIES            use chosen material
FIGURE_FORMATS     two_axis_grid timeline flow before_after map spectrum stack network scene
STEP_DEPTHS        surface standard deep

ShapeRef      {kind: section|table|figure, index (1-based)}          .label() → "§3" / "T1" / "F2"
SectionSpec   {heading ≤70, answers ≤120}
TableSpec     {title ≤90, row_unit "one row per …" ≤60, columns 3-5, rows_expected "8-10", carried_by [doc_key]}
FigureSpec    {title ≤90, format ∈ FIGURE_FORMATS, scene ≤220}
Shape         {sections 3-6, tables 1-3, figures 0-3}
Promise       {text, supported_by [ShapeRef] ≥1, unsupported: bool (set by the checks)}
CarryingDoc   {doc_key, carries}
EvidenceBase  {carrying_docs [CarryingDoc], thin_or_missing [str ≤140]}
PathStep      {engine_key, plain_name, contributes ≤120, depth ∈ STEP_DEPTHS}
Path          {steps 1-4 (run order), depth ∈ DEPTHS (derived by code from the steps), primitives, chain_key}

BriefOption   version (1 stored v1 / 2), key, title ≤10 words, deliverable_kind, deliverable ≤110, use_kind,
              you_will_understand ×3, you_will_be_able_to 2-3, questions_answered 3-4, not_for 1-3,
              shape, evidence_base, path, best_when ≤140, alternative (lane 2), notes (what the checks changed),
              est_cost_usd / est_minutes / est_llm_calls (code, from the option's OWN path)
              + DERIVED views kept for the downstream steps: telling, engines [{engine_key, why}], output_shape {sections[], tables[], figures[]}
Recommendation {option_key, because ≤220, runner_up, runner_up_because}
Brief         {version, entry, options, recommendation, defaults, notes}   .autopilot_key() / .autopilot_reason()
UseFrame      {use_kind|null, occasion, who_reads, decision}
PathRequest   {steps [{engine_key, depth}], chain_key (recipe), depth}
DossierOptions / CreateDossierRequest gain  entry, use_frame, path  (autopilot kept as the alias of entry = "material")
```

`telling`, `engines`, `output_shape` are **derived** in a `model_validator(mode="after")` whenever `shape` is present (v2), so `plan.py`, `tables.py`, `figures.py`, `compose.py` read what they always read, and they serialise for old clients. A stored v1 option (no `shape`) keeps its own values and stays `version: 1` — every job already in the DB still loads (verified against the three live jobs). A `model_validator(mode="before")` coerces shape-only slips (a promise given as a bare string, a doc key as a string, a section as a string) so they reach the rule checks instead of costing a whole re-ask (the Kering sample's first answer did exactly this).

### 1.2 The purpose-first catalog — `src/dossier/catalog_purpose.json`, `recipes.json`, `catalog.py`

- `catalog_purpose.json`: the 22 executable engines in four purpose groups (Test a position · See the structure · Follow the words · Read it properly) with `plain_name` (executive register), `use_when`, `yields`, `row_unit`, `deliverable_kinds`, `pairs_with`, `fit` (`ok` | `conditional` + `applies_when`), plus the six excluded engines with their reasons and the deliverable-kind → engine hints (§D).
- `recipes.json`: the seven pre-composed paths of §D6 (stress test, pattern & playbook, two-case comparison, vocabulary decoder, reading guide, credibility read, full read). A step may repeat an engine only as a trailing synthesis pass.
- `catalog.py`: `purpose_catalog(audience, corpus_chars, n_docs, same_author)` joins the JSON with the runtime capability registry — an engine without a YAML is dropped, an executable engine the JSON does not know is appended under "More", never hidden. Per-depth `passes` and, when `corpus_chars` is given, `est_cost_usd`/`est_minutes` from `estimate_engine_run`. `fit_for_corpus` turns the conditional flags into `off` for this corpus (`chapter_role_analyzer` on 5 documents; `evolution_tactics_detector` on a mixed-author bundle). Also: `plain_name_for`, `vocabulary_lines`, `ban_terms`/`jargon_hits` (quoted spans exempt), `estimate_path`, `path_depth_from_steps`, `validate_steps`, `resolve_path_request`.

### 1.3 The brief — `src/dossier/brief.py`

- **System prompt**: the nine rules of §B4 verbatim (rule 7 additionally forbids engines marked NOT FOR THIS CORPUS). Translate mode (entry = `chosen`) replaces rule 7 with "THE PATH IS FIXED: …" and asks for two options, `alternative: false/true`.
- **User prompt**: audience register; ~48 vocabulary lines (the ban terms the executive file translates, plus fallback plain equivalents for the theory words the file lacks — `legitimation`, `neoliberal`, `ontology`…); the engine plain names; the use register; REQUESTER'S USE (use_kind, intent, occasion, who reads, decision due); depth/figures preference; corpus; reconnaissance (`compact_profiles`); the executable engines by purpose with passes and fit for this corpus; the recipes.
- **Tool schema**: hand-written (`brief_schema(translate)`), enums for `use_kind`, `deliverable_kind`, `format`, `depth`; no `est_*`, no legacy views.
- **Checks** (`check_brief`, pure, unit-tested) and what happens on failure:

| check | rule | on failure |
|---|---|---|
| use disjointness | three `use_kind`s differ; with `use_frame.use_kind`, `able_to` texts share < 50 % content words pairwise (`overlap()`) | repair round |
| concreteness | each understand/able_to line has a `[DOC_KEY]`, an entity from the profiles, a number/date, or a quoted phrase (double, curly or single quotes; apostrophes are not quotes) | repair round; after it, the line is dropped and noted (never below one line) |
| support refs | every `supported_by` resolves to an existing section/table/figure | repair round; then stripped, promise marked `unsupported` (rendered muted, "unkept") |
| row unit | every table's `row_unit` starts with "one row per" | repair round; then normalised by code and noted |
| vocabulary | executive only: none of the curated theory terms on reader-facing fields (title, deliverable, promises, questions, not_for, best_when, headings, table titles, plain names, contributes) | repair round with the terms listed; then noted on the option |
| lengths | the §B4 rule-8 caps (+ scene ≤220, contributes ≤120, because ≤220) | repair round ("tighten, do not truncate"); then cut at a word boundary with "…" and noted |
| engines | executable keys, unique (trailing synthesis may repeat), 1–4; `plain_name` overwritten from the catalog for the audience | unknown/duplicate dropped; none left → `deep_summarization`, noted |
| weight spread | ≥2 distinct derived `path.depth` labels across the three | note only |
| recommendation | `option_key` exists (after key normalisation) | option 1 recorded, noted |

  One repair round: the violations that need the model are listed under the previous answer ("Return the COMPLETE corrected brief … keeping everything that was right"); the second answer replaces the first only if it has no more violations. Then `apply_code_fixes` settles the rest, `estimate_path` prices each option from its own steps, and the requester's audience/depth/figures win over the model's `defaults`.
- **Events**: the `artifact` payload carries per option `use_kind`, `deliverable_kind`, `deliverable`, `able_to`, `not_for`, `path`, `depth`, `est_*`, `notes`, plus `recommendation`, `entry`, `repaired`; a `note` lists the violations sent to the repair round.

### 1.4 Lanes — runner and plan

- `entry = "material"` (also `autopilot: true`): `runner.py` chooses `brief.autopilot_key()` = `recommendation.option_key` and the note reads *"the material decided: <title> — because <reason>"* (two lines changed in the runner; `payload_json.kind = material_decided`).
- `entry = "chosen"`: `validate_lane` resolves `path` (steps or a recipe via `chain_key`) against the executable catalog at job creation (400 with the reason otherwise); the brief runs in translate mode; the plan honours the path exactly.
- `entry = "use"` (default): three options; the run pauses at `awaiting_brief` as before.
- `plan.py`: `fixed_path(job, option, by_key)` returns the request's path for lane 2, **or the chosen v2 option's own path** (see deviations); `fixed_phases` keeps exactly those steps, in order, at their depths, taking `context_emphasis`/`why` from the planner's matching phase — Sonnet still writes the emphasis, the rationale and the alternatives. Legacy v1 options keep the old `_enforce_policy` planner.

### 1.5 API — `src/api/routes/dossier.py`

- `POST /v1/dossier/jobs`: `entry`, `use_frame`, `path` validated by `validate_lane`; `autopilot` → `entry = "material"`.
- `GET /v1/dossier/catalog?audience=&corpus_chars=&n_docs=&same_author=` → `{audience, groups[{key,title,purpose,engines[…]}], recipes[…], excluded[{engine_key, why}], own_overhead{est_cost_usd, est_minutes, calls}, use_kinds}`.
- `GET /v1/dossier/jobs/{id}/brief` → `{version, entry, options, recommendation, defaults, notes, chosen_option, status}`.
- `POST /v1/dossier/jobs/{id}/brief` `{option_key, overrides}`: `overrides.path` (`{steps:[{engine_key, depth}]}` or a bare list) is resolved, stored on the chosen option (re-priced), and becomes the job's fixed path (`entry = chosen`); `overrides.figures` is now honoured (see bug); `option_key: "own_path"` with a path adds a synthetic "Your own path" option (the fourth card). The response carries the chosen option.

### 1.6 The desk — `web/`

- `types.ts`: `BriefOption` v2 (+ legacy `telling/engines/why/output_shape`), `Recommendation`, `Brief.entry/recommendation/notes`, `UseFrame`, `PathRequest`, the catalog types, `USE_KINDS`, `DELIVERABLE_LABEL`, `refLabel`.
- `lib/api.ts`: `normalizeBriefOption` accepts **v2 and the old shape** (string promises, string refs like "T1", engines as names or objects, output_shape object/string); `normalizeBrief` derives `recommendation` from `defaults.option_key` when absent; `catalog()` added (live + mock).
- `components/DeliverableCard.tsx`: the §B3 anatomy — eyebrow `deliverable · A · stress test`, `★ recommended — because …` / `☆ runner-up`, title, deliverable line, `for: <use>`, YOU WILL UNDERSTAND / YOU WILL BE ABLE TO with `T1 / §5 / F1` chips (hover highlights the row in the shape disclosure), ANSWERS, NOT FOR (always visible), SHAPE and EVIDENCE strips with ▸ disclosures (tables — row unit — rows; figures — format; carrying docs; thin), HOW line (plain names · depth · passes · `edit ▸`) with a "what each step adds" disclosure, price + best when, desk notes. A v1 option falls back to the old telling card.
- `components/CatalogPicker.tsx`: groups as tabs with counts, search, a recipes tab ("use this path"), engine cards (plain name · engine name · use when · yields · row unit · depth chips priced on this corpus · pairs with · fit note; `off` engines greyed), the excluded six listed with reasons, "Your path" (order ↑↓, remove, depth per step, running estimate from the catalog's per-depth prices + own overhead). `estimatePath`/`pathDepth` exported.
- `steps/BriefStep.tsx`: eyebrow per lane (*3 deliverables · your choice* / *your path + the desk's alternative* / *the material decided* with the reason as the lede); cards; `edit ▸` opens the picker pre-loaded with that card's path and re-prices the card client-side (the server confirms on choose); "I know the analysis I want ▸" adds a fourth "Your own path" card; dials shrink to **Figures** and **Written for**; the dock subline adds the chosen deliverable.
- `pages/Library.tsx`: source tabs kept (Paste / Upload / Exemplar); the **use box** (intent + eight use chips + optional occasion / who reads / decision due); **Written for**; the **lane** radio; lane 2 reveals the picker (catalog priced on the chosen bundle's size); an **advanced** fold (depth preference, figures, spend cap, image provider); Start copy per lane.
- Mock: `web/mock/brief.json` is a v2 fixture (Kering; keys unchanged so `jobs.json` still resolves), `web/mock/catalog.json` is the real catalog priced for 61,420 chars (rescaled per corpus in `mock.ts`), autopilot in the mock follows `recommendation.option_key`, `chooseBrief` keeps an edited path. `?mock=1` walks Library → brief → draft.
- `styles.css`: card blocks, picker, use box and lanes (≈130 lines, on the existing tokens).

## 2. Verification

- **Unit tests** (`tests/test_brief_v2_checks.py`, 22 tests, no network): v2 fixture validates and derives the legacy views; v1 keeps its values; every §B5 check on a bad fixture and its code fix; estimates differ light < standard < full; the catalog joins 22 engines / 6 excluded / 7 recipes with fit for the corpus; recipes resolve and bad paths are rejected; `validate_lane`; the plan honours a fixed path exactly (order, depths, passes, phase numbers); bare-string promises are coerced. `pytest tests/test_brief_v2_checks.py tests/test_dossier_llm_shapes.py tests/test_dossier_tables_wall.py` → 32 passed. `python -c "from src.api.main import app"` OK. `cd web && npm run build` clean (strict TS).
- **Three real briefs** (`scripts/brief_v2_sample.py`, saved profiles, entry = use, executive):

| sample | calls | cost | time | options (use · kind · price · path) | recommended — because |
|---|---|---|---|---|---|
| fashion (5 papers, 349K chars, intent stated) | 2 (1 repair) | $0.30 | 246 s | A *Where Our Sustainability Claims Will Be Attacked* · stress_test · $2.59 · claim scorecard → hidden-obligations map; B *How Platform Fast Fashion Undercuts Our Legitimacy* · decide · $2.22 · comparison audit → pattern map; C *Depth-of-Commitment Playbook* · argue · $3.70 · advanced, 4 steps | A — "[U3PWD6J3]'s typology is directly usable as a scorecard and [SG4IGV3Y]'s 10-R…"; runner-up C |
| kering (1 doc, 33K chars) | 3 (1 shape re-ask, 1 repair) | $0.34 | 265 s | A *Where Kering's Meaning System Is Breaking Down* · watch · $0.53 · contradiction map; B *Stress-Testing the Pitch Before the Room* · stress_test · $0.80; C *Which Pitch Angle to Lead With — and Why* · decide · $0.93 · 3 steps | B — "eight named framing risks and explicit [INFERENCE] flags … the 2026-07-22 meeting date" |
| state capitalism (5 papers, 270K chars, **no intent**) | 2 (1 repair) | $0.33 | 269 s | A *How States and Markets Are Rewiring: The Repeating Template* · brief · $2.17 · pattern map → vocabulary decoder; B *Testing the Claims: Where the State-Capitalism Arguments Break* · stress_test · $2.17; C *The Full Picture: State Power, Private Infrastructure…* · decide · $3.10 · advanced, 4 steps | C — "five inter-locking cases with specific numbers (€976m, 12 FTE, 60 % market target, CFIUS 1975), named firms…" |

  Against §E2: fashion A is the expected stress test (recommended, claim types, `not_for` says no house data — the live v1 brief had promised "claim by claim" over a corpus with no house claims); fashion B is the Shein benchmark, as a decision memo rather than a briefing; C came as a playbook (argue) where §E2 imagined a reading guide (learn). State-capitalism A is the §E2 playbook (pattern map → vocabulary decoder, five cases); §E2's "watch: screening perimeter" did not appear (the desk chose a stress test and a full decision memo) but the live v1 promise "where the next boundary moves are likely to land" is now retracted in every `not_for` ("Forecasts of which sectors or countries will be targeted next — the documents only analyse past and current cases"). Kering: §E2's "prepare: the half-sentence that opens the pitch" came as "stress-test the pitch before the room" (recommended) with the Wednesday date on the card. Three different prices in every brief; three different uses in every brief; every `not_for` names a corpus limit; every recommendation names a document or a number.
- **Playwright** (`?mock=1`): Library use box → chips → optional fields → lanes; lane 2 picker (recipe → two steps priced, group cards with depth prices, off engines greyed); Start → reading → brief: three cards with promises + refs, NOT FOR visible, `★ recommended — because…`, `☆ runner-up`, shape/evidence disclosures, how-line; `edit ▸` → picker pre-loaded → reorder → "Use this how-line" re-writes the card's how-line; Write the draft → planning → draft. No console errors from the desk. Screens: `web/docs/screens/brief-v2-1-library.png`, `brief-v2-2-picker.png`, `brief-v2-3-brief.png`.

## 3. Deviations from the design, and why

1. **The plan honours a v2 option's own path in every lane**, not only `entry = "chosen"`. The card prices and promises its steps ("T1 one row per commitment" comes from the hidden-obligations map); letting the planner re-choose engines under the job-level depth policy would break the promise and the price. Sonnet still writes `context_emphasis`, the rationale and the alternatives. Legacy v1 options keep the old planner.
2. **`path.depth` is derived by code from the steps** (simple = 1 step/1 pass, medium ≤ 3 steps/≤ 4 passes, else advanced); the model's label is ignored. Labels are arithmetic, not judgment (§C7).
3. **Length overruns go to the repair round** (the design said "truncate, log"). The samples showed the model overrunning 140-char caps by 50–200 chars on most lines; a truncated promise is a broken promise, so the model is asked once to tighten; code cuts what remains and notes it.
4. **The vocabulary ban-list is a curated list of theory terms** (~60), not the executive file's 1,599 left-hand terms — the raw intersection with the catalog text bans "claim", "evidence", "pattern", "position", which no card can avoid. Quoted spans are exempt (a verbatim phrase is evidence). Terms the file does not translate get fallback plain equivalents in the prompt. After the repair round, leftovers are noted, not rewritten by code (both samples with leftovers: one word each — "discourse", "neoliberalism").
5. **Concreteness accepts a quoted phrase** as concrete (the design listed doc key / entity / number); the model cites verbatim phrases in single quotes constantly ('national security').
6. **Runner**: two lines changed (`brief.autopilot_key()` / `brief.autopilot_reason()`), not a restructure. `STEP_WHY["brief"]` still says "three genuinely different angles" — owned by the runner agent.
7. `tables.py`/`figures.py`/`compose.py` untouched: they keep reading the derived `output_shape` strings, which now carry the row unit and the figure format inline (`"title — one row per …"`, `"title (two_axis_grid): scene"`). Reading `shape.tables[].row_unit` directly is the other agent's step.
8. **Lane 2 in the brief step** ("I know the analysis I want ▸") adds a fourth card and posts `option_key: "own_path"` with the path; the live translate-mode preview card (§C5 step 4) and `POST /brief/preview` are not built. The "Written for" dial no longer changes the cards' register silently: it only affects the draft, and says so; `POST /brief/rewrite` (§C3, step 4) is not built.
9. **Cost**: a v2 brief is ~$0.30 per run (two calls of ~10–20K in / 5–7K out), not the ≈$0.05 of the v1 brief — the answer is five times longer and the repair round fires on every sample so far (7–8 violations each, mostly concreteness and lengths).
10. Picker: reorder by ↑↓ buttons, not drag.

## 4. Bug found on the way

- `POST /jobs/{id}/brief` silently ignored `overrides.figures` (the desk's dial sends `figures` at the top level; the route only merged `output.figures`) — fixed in the route; recorded in `communications/BUG_TRACKING.md`.

## 5. What's left

- `tables.py` / `figures.py` / `compose.py` reading `shape.tables[].row_unit`, `figures[].format`, `sections[].answers` directly (§E1 step 1, other agent).
- `POST /v1/dossier/jobs/{id}/brief/rewrite {audience}` and `POST /v1/dossier/brief/preview` (§C3 step 4); the picker's live preview card.
- The `not_for` learning loop (recurring `not_for` lines → reconnaissance prompts, vision §H10); recipes minted from recurring chosen paths.
- A full lane-2 run (translate mode) and a lane-3 run end-to-end on the live server — only the brief step was exercised with real calls here; the plan's fixed-path branch is unit-tested.
- Concreteness dropped lines that were arguably fine ("Brief communications teams on what we are really agreeing to") — the rule is the design's; if the owner prefers, drop → flag.
- i18n; the Console's planner strip could show `recommended: A — because …` from the artifact payload.

## 6. Entries for the shared docs

### CHANGELOG (Unreleased)
- **Brief v2 — deliverable-first** (`src/dossier/brief.py`, `schemas.py`, `catalog.py`, `catalog_purpose.json`, `recipes.json`, `plan.py`, `runner.py` (2 lines), `src/api/routes/dossier.py`; desk `web/src/{types.ts, lib/api.ts, lib/mock.ts, components/DeliverableCard.tsx, components/CatalogPicker.tsx, steps/BriefStep.tsx, pages/Library.tsx, styles.css}`, `web/mock/{brief.json, catalog.json}`; tests `tests/test_brief_v2_checks.py`; samples `communications/changes/brief-v2-samples/`).
- Fixed: `overrides.figures` ignored on brief choice.

### FEATURES
- **Dossier brief v2 (deliverable-first)** — Status Active — three deliverables differing by use, each with promises verified against its shape, `not_for`, evidence, priced path, and a recommendation; three lanes (use / chosen / material); purpose-first catalog `GET /v1/dossier/catalog`. Entry points: `src/dossier/brief.py`, `src/dossier/catalog.py`, `src/dossier/catalog_purpose.json`, `src/dossier/recipes.json`, `src/dossier/schemas.py` (BriefOption v2), `src/dossier/plan.py` (`fixed_path`), `src/api/routes/dossier.py` (`validate_lane`, `/catalog`, `choose_brief`). Added 2026-09-03.
- **Web · The brief (v2 cards + catalog picker)** — `web/src/components/DeliverableCard.tsx`, `web/src/components/CatalogPicker.tsx`, `web/src/steps/BriefStep.tsx`, `web/src/pages/Library.tsx` (use box, lanes, advanced). Modified 2026-09-03.
