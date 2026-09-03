# diagrams agent (D1) — change note

Branch `feat/diagrams`. Owner of `src/display/enforcement.py`, `src/dossier/figures.py`, the figure
schemas in `src/dossier/schemas.py`, the diagram half of `src/images/figure_prompts.py` and
`src/images/compliance.py`, `tests/test_diagram_prompts.py`, `tests/test_figure_spec_validation.py`.
Verified live 2026-09-03 on the owner's two dossier runs.

## State — 2026-09-03 (WIP commit 0f80662 on feat/diagrams)

**Done**: enforcement catalog (v1 port + 64 formats), FigureSpec contract, planner + wall, prompt builder,
render → check → one revision, compose/template updates, 63 unit tests, CLI, samples with verdicts.
**Sample verdicts**: 5/5 final renders pass the vision check (15/15, 19/19, 14/14, 22/22, 17/17 labels found;
format ok; no prohibited elements) and my own eye; 2 first attempts were rejected and fixed by the revision pass.
**Cost**: $1.47 images (11 renders) + ≈ $0.7 Sonnet planning/checking ≈ $2.2 total.
**Remains**: the bar-format numeric-cell wall rule is committed but not re-rendered; docs/CHANGELOG.md and
docs/FEATURES.md entries are drafted below for the reconciler to fold in. Two `tests/test_manifest_trace.py`
cases (`proof-round5-adaptive-aoi-*`) fail in this fresh worktree with "Job not found" — they read
`executor_jobs` from local DB state that the owner's main checkout has and a new worktree does not; nothing
in this branch touches the presenter or the executor DB.

## The problem, and what changed

The dossier's figure step produced metaphorical illustrations (a wooden table with manila folders and
gold bars, a bridge, a shelf) — exactly what analyzer v1 forbids in `GLOBAL_PROHIBITIONS`. Every figure
is now a **labelled analytical diagram** — Sankey, quadrant, timeline, grouped bars, Venn, network, cycle,
matrix, argument tree … — chosen through the analytical **primitive** the analysis exhibits, filled with
the analysis's own labels, rendered by Nano Banana Pro under v1's per-format must_have/must_not rules,
and checked by Claude vision against its own label manifest (with one revision pass, v1's retry).

```
plan (Sonnet, forced-tool JSON)  →  FigureSpec[]            src/dossier/figures.plan_figures   (+ validate_spec = the wall)
spec → prompt                    →  str                     src/images/figure_prompts.build_diagram_prompt
prompt → image                   →  bytes                   src/images/adapter.generate_image  (gemini_pro, 2K, aspect per format, no_text=False)
image × spec → verdict           →  dict                    src/images/compliance.check_diagram
not ok → re-render ONCE with the reviewer's notes; keep the better attempt; both receipts + both verdicts on the record
```

`render_figure(job, spec, out_dir, provider)` is independent of where the spec came from: the later
"spine" pass can hand it specs derived from section claims unchanged. `run_figures(job, docs)` keeps its
signature; `src/dossier/runner.py` changed by one line (the step's "why").

## FigureSpec — the contract (src/dossier/schemas.py:153-207)

```python
class FigureAnchor(BaseModel):
    label: str                 # a label from data
    quote: str = ""            # verbatim phrase from the analysis prose / a table cell / a profile
    source: str = ""           # analysis | table | profile
    verified: bool = False     # set by the wall

class FigureSpec(BaseModel):
    key: str
    primitive: str             # one of the 12 in src/primitives/definitions/primitives.json
    visual_format: str         # canonical key in src/display/enforcement.FORMAT_ENFORCEMENT (64 formats)
    title: str                 # <= 70 chars, rendered at the top of the image
    data: dict                 # the diagram's ENTIRE content in the format family's JSON shape
    caption: str               # the analytic point, one sentence (digits must exist in data)
    why_this_format: str
    style_school: str          # chosen in code from src/styles affinities (audience + engines + format)
    anchors: list[FigureAnchor]
    scene: str = ""            # legacy, old records still load
    visual_register: str = "diagram"

FigureBrief = FigureSpec       # old name kept

class Figure(FigureSpec):      # the record on the job
    figure_id, url, path, provider, model, prompt, aspect, cost_usd (sum over attempts)
    status: planned | generated | skipped | failed ; note
    compliance: dict           # the kept attempt's verdict (below)
    attempts: list[dict]       # [{n, provider, model, cost_usd, latency_ms, figure_id, path, prompt_chars,
                               #   compliance, revision_notes, kept}]
    grounding: dict            # {labels, content_labels, grounded, ungrounded[], anchors, anchors_verified, anchors_failed[], fraction}
```

### Data families (the shape `data` must take — src/display/enforcement.DATA_SHAPES, 28 families)

| family | formats | shape |
|---|---|---|
| steps | flowchart, linear_flowchart, process_flow, value_stream_map, commitment_cascade | `{steps:[{label}], branches?:[{from,label,to}]}` 3-10 |
| sets | venn_diagram, euler_diagram | `{sets:[{label,items?}], intersections:[{of:[…],label}]}` 2-4 sets |
| quadrant | quadrant_chart, positioning_map, bubble_chart | `{x_axis:{label,low,high}, y_axis:{…}, quadrants?:{top_left…}, items:[{label,x,y,group?}]}` 4-10 |
| events | timeline, parallel_timelines | `{events:[{date,label,track?}], tracks?}` 3-12 |
| flows | sankey_diagram, alluvial_diagram, chord_diagram, river_tributaries, stock_flow_diagram | `{nodes?:[{label,stage?}], flows:[{source,target,weight 1-5,label?}]}` |
| network | network_graph, force_directed, constellation_map | `{nodes:[{label,group?,size?}], edges:[{source,target,label?}]}` 4-12 nodes |
| cycle | cycle_diagram, causal_loop_diagram | `{stages:[{label}], links?:[{from,to,polarity?}], loop_type?}` |
| matrix | matrix, matrix_heatmap, ach_matrix, evidence_quality_matrix, grouped_bar_chart*, stacked_bar*, marimekko* | `{rows, columns, cells[][]}` (*numeric cells) |
| tree | hierarchical_tree, containment_nesting, sunburst, assumption_web, path_branching_tree, forced_fork | `{root:{label,children:[…]}}` ≤3 levels |
| argument | argument_tree | `{claim, premises:[{label,evidence?[],rebuttal?}]}` |
| layers / columns / concentric / spectrum / bars / regions / radar / hub / gantt / waterfall / indicators / gap / before_after / toulmin / dialectic / square / force_field / scenarios | … | see `DATA_SHAPES[...]["template"]` |

Every string in `data` is rendered: ≤ 6 words / 48 chars (`MAX_LABEL_WORDS`). Structural strings (axis
names, quadrant names, the measure, track names — `STRUCTURAL_KEYS`) are the planner's own; content
strings must use the material's words. Magnitudes and positions are spelled to the image model in words
("thick band", "at the far left, in the upper half") so nothing numeric leaks into the picture.

### The wall (`validate_spec`, src/dossier/figures.py:163-238)

Rejects: unknown format/primitive; empty data; data that does not fit the family; any label > 6 words;
title > 70 chars; caption digits absent from data; a second figure in an already-used format; and
**ungrounded** data — fewer than 50 % of content labels found in the material (verbatim, or every
significant word of the label present) or no verified verbatim anchor. Rejected figures are re-asked once
with the errors verbatim (kept figures stay); still-rejected ones are `figure_skipped`, never fatal.

### The verdict (`check_diagram`, src/images/compliance.py:233-350)

`{ok, format_ok, detected_format, title_found, labels_found[], labels_missing[], misspelled[{expected,seen}],
illegible[], prohibited_elements[], extra_text[], suggestion, confidence, checked, model, usage, n_labels, issues[]}`

`ok` = format_ok ∧ no prohibited elements ∧ no invented sentence (extra_text ≥ 4 words) ∧
missing+misspelled+illegible ≤ max(1, 20 % of labels). Labels the model neither found nor listed count as
missing. Fail-open without a key (`checked=False`, the figure is kept unchecked).

## What was ported from analyzer v1 (`src/display/enforcement.py`)

- `GLOBAL_PROHIBITIONS` — verbatim (gemini_image.py:1039-1052), plus the legibility block.
- `FORMAT_ENFORCEMENT` — all 16 v1 entries verbatim (flowchart, timeline, sankey→`sankey_diagram`,
  structured_diagram, network_graph, treemap, matrix, heatmap→`matrix_heatmap`, conceptual_landscape,
  conceptual_layers, venn_conceptual→`venn_diagram`, constellation_map, weight_mass, radial_hierarchy,
  spectrum_gradient, containment_nesting), each with the "McKinsey/BCG slide" must_have and the
  anti-dramatic must_not lists; `FORMAT_VALIDATION_CRITERIA` as `pass_if`/`fail_if`.
- The diagram-shaped v1 `VISUAL_FORMAT_INSTRUCTIONS` as entries (concentric_circles, linear_flowchart,
  two_column_split, comparison_boxes, quadrant_grid→`quadrant_chart`, river_tributaries, ledger_before_after,
  delta_transform, radiating_exposure, forced_fork). The metaphor formats (bridge_diagram, stress_fracture,
  reflexive_loop, parallax_view, inheritance_chain, bundled_box, horizon_fade) are **not** ported; they alias
  to their nearest diagram.
- `get_format_enforcement_prompt` → `enforcement_block()` (same box, same ✓ / ✗ / ⛔ lines).
- `_build_style_guide_directive` was already ported as `build_style_override`; `style_for_school()` feeds it
  a school's palette/typography with the illustration-pulling modifier lines filtered out (headline, callout,
  annotation, metaphor, lighting, attribution …) and a categorical series so diagrams are never monochrome.
- New rules for every v2 catalog format v1 lacked (chord, hierarchical/radial tree, force-directed,
  alluvial, process flow, value stream, gantt, parallel timelines, cycle, sparklines, radar, bar/grouped/dot,
  sunburst, stacked, waterfall, marimekko, euler, positioning, bubble, ACH, confidence scale, evidence
  quality, indicator dashboard, gap analysis, argument tree, toulmin, dialectical map, assumption web,
  scenario cone) and for the primitives' forms (causal loop, stock-flow, semiotic square, force field,
  path-branching tree, commitment cascade). 64 canonical formats, 50 aliases, 12 primitives → formats.

Prompt order (`build_diagram_prompt`): opening line + title → enforcement block (must_have / must_not /
GLOBAL_PROHIBITIONS / legibility) → MANDATORY STYLE OVERRIDE for the school → CONTENT TO RENDER (the data
spelled out) + LABEL MANIFEST → TITLE placement (no quotes, nothing under it) → TEXT RULES (≥14pt, contrast,
only these words, no decimals/coordinates, no callouts) → FRAME aspect → REVISION NOTES (retry only) →
"A single clean diagram on a plain background — no scenery, no metaphors, no photographs, no 3D objects."
→ FINAL REMINDER: LAYOUT IS MANDATORY → style closing. ~10-15K chars.

## Samples (communications/changes/diagram-samples/, ≤ 210 KB each, with `.prompt.txt` + `.verdict.json`)

Owner's run `live-dossier-dce25aeed631` (5 papers on state capitalism, executive, N = 3):

| file | primitive → format | labels | attempts | verdict | my eye |
|---|---|---|---|---|---|
| `state-beneficiary_flow_web.jpg` | flow_transformation → sankey_diagram | 15/15 | 2 (kept #2) | ok | announcement → 5 cases → named firms, colored ribbons, HMN Tech a red sliver. Attempt 1 (`…rejected-attempt1.jpg`) split "Greece / Microsoft" into two nodes — caught, fixed by the revision. |
| `state-government_vocabulary_decoder_map.jpg` | rhetorical_architecture → quadrant_chart | 19/19 | 1 | ok | terms placed on scope × scrutiny with four named quadrants; clean |
| `state-jobs_promised_vs_documented.jpg` | comparative_positioning → grouped_bar_chart | 14/14 | 2 (kept #2) | ok | announced vs documented pairs with legend. Attempt 1 drew two separate columns (wrong format) — caught, fixed. **Weak**: bar lengths encode qualitative statements; the wall now requires numeric cells for bar formats, so this content will go to `gap_analysis` next time. |

Fashion run `live-dossier-be00c33e5180` (executive, N = 2):

| file | primitive → format | labels | attempts | verdict | my eye |
|---|---|---|---|---|---|
| `fashion-claim_lifecycle_timeline.jpg` | temporal_evolution → timeline | 22/22 | 1 | ok | four parallel tracks, staged events, interventions aligned; the "dates" are stage numbers because the material has none |
| `fashion-legitimacy_risk_grid.jpg` | comparative_positioning → quadrant_chart | 17/17 | 1 | ok | coherence × motive, brands placed, colored groups, no coordinates printed |

5 of 5 finals pass both the check and my eye (before the round-1 prompt fixes: 4 of 4 were diagrams but
two carried invented "Insight/Conclusion" callouts from the style school's modifiers, one printed item
coordinates, one copied the title's quotation marks — all fixed in the prompt and now caught by the check).

## Cost

11 Gemini 3 Pro Image renders at $0.134 = **$1.47** (round 1: 4; round 2: 7 incl. 2 retries). Planner
calls (Sonnet 4.6, ~21K tokens in): 6 × ≈ $0.10 = $0.62; vision checks 11 × ≈ $0.01. Total ≈ **$2.2**;
image budget was ≤ $3. Per dossier at N = 3: ≈ $0.10-0.20 planning + $0.13-0.27 per figure.

## What still looks weak

- **Bar formats with prose values** — fixed by the wall (numeric cells) but not yet re-rendered; expect the
  planner to choose `gap_analysis` / `comparison_boxes` for "announced vs documented" content.
- **Grounding is lexical**: a label passes if its significant words occur in the material. Invented names
  are caught; a wrong *placement* (which quadrant an item sits in) is not — that is the analysis's claim, and
  the caption/anchors are the only trace. The spine pass should give each placed item an anchor.
- **The style school is always `explanatory_narrative` for executive dossiers** (audience affinity dominates).
  Diagrams look consistent but samey; a per-figure school (format affinity weighted higher) is one constant.
- **Timeline "dates"** default to stage labels when the material has no chronology; a flowchart may be the
  better format there — the planner prompt could say so.
- The planner rejects ~1 in 3 first-pass figures for label length; the repair usually fixes it, at ≈ $0.08.
  Cheaper: cap words in code by asking for `short_label` fallbacks — not done, the wall is honest as is.
- Sankey band widths are ordinal words (thin … very thick), not the material's amounts.

## CHANGELOG entries (fold into docs/CHANGELOG.md [Unreleased])

### Added
- Format enforcement catalog for labelled diagrams: v1 `GLOBAL_PROHIBITIONS` + `FORMAT_ENFORCEMENT`
  ported verbatim and extended to 64 formats with data-shape families, validators, prose renderers,
  label collection and the planner catalog ([src/display/enforcement.py](../../src/display/enforcement.py)).
- `FigureSpec` / `FigureAnchor` and the extended `Figure` record (primitive, visual_format, title, data,
  why_this_format, style_school, anchors, attempts, grounding) ([src/dossier/schemas.py](../../src/dossier/schemas.py)).
- Diagram figure step: Sonnet plan under a strict schema, the spec wall (shape + grounding + one re-ask),
  render → check → one revision → keep the better attempt, incremental persistence, CLI
  `python -m src.dossier.figures --job job.json --n 3 --out DIR [--plan-only|--specs specs.json]`
  ([src/dossier/figures.py](../../src/dossier/figures.py)).
- `build_diagram_prompt(spec, *, style_school, aspect, revision_notes)` and `style_for_school()`
  ([src/images/figure_prompts.py](../../src/images/figure_prompts.py)).
- `check_diagram(image_bytes, spec)` — format + label-manifest verdict, `diagram_verdict_ok`
  ([src/images/compliance.py](../../src/images/compliance.py)).
- Tests (no network): `tests/test_diagram_prompts.py` (14), `tests/test_figure_spec_validation.py` (49, incl.
  stubbed `render_figure` retry loop).
- Samples: `communications/changes/diagram-samples/` (5 finals + 2 rejected attempts, prompts, verdicts).

### Changed
- Dossier HTML/Markdown: figure captions carry the diagram title; "How this was made" lists each figure's
  primitive, format, style school, attempts and check verdict ([src/dossier/compose.py](../../src/dossier/compose.py),
  [src/dossier/templates/dossier.html.j2](../../src/dossier/templates/dossier.html.j2)).
- `src/dossier/runner.py`: the figures step's one-line "why".
- `build_figure_prompt` (scene registers, NO-TEXT) is kept for the old register but the dossier no longer uses it.

## FEATURES entries (fold into docs/FEATURES.md)

### Diagram Format Enforcement
- **Status**: Active
- **Description**: Per-format must_have/must_not rules (v1 port + v2 catalog), data-shape families with
  validators and renderers, label collection, planner catalog text.
- **Entry Points**:
  - `src/display/enforcement.py:36-49` — `GLOBAL_PROHIBITIONS` (v1 verbatim); `:51-57` `LEGIBILITY_RULES`
  - `src/display/enforcement.py:84-796` — `FORMAT_ENFORCEMENT` (64 formats; `source` = v1 | v1-palette | v2)
  - `src/display/enforcement.py:798-858` — `FORMAT_ALIASES`, `normalize_format_key`, `format_entry`, `aspect_for`
  - `src/display/enforcement.py:861-916` — `enforcement_block` (v1 get_format_enforcement_prompt), `check_criteria`
  - `src/display/enforcement.py:938-981` — `STRUCTURAL_KEYS`, `collect_labels`, `content_labels`
  - `src/display/enforcement.py:1604-1665` — `DATA_SHAPES` (28 families: template, rule, validate, render)
  - `src/display/enforcement.py:1667-1707` — `NUMERIC_CELL_FORMATS`, `validate_data`, `render_data`
  - `src/display/enforcement.py:1734-1764` — `primitive_formats`, `catalog_text`
- **Dependencies**: `src/primitives/definitions/primitives.json`
- **Added**: 2026-09-03

### Dossier Figures (labelled diagrams)
- **Status**: Active
- **Description**: Plans N diagram specs from analysis + tables + profiles, walls them, renders with
  Nano Banana Pro, checks with Claude vision, retries once, records both attempts.
- **Entry Points**:
  - `src/dossier/schemas.py:153-207` — `FigureAnchor`, `FigureSpec`, `Figure`
  - `src/dossier/figures.py:67-102` — planner tool schema + system prompt
  - `src/dossier/figures.py:107-129` — `tables_text`, `material_text`
  - `src/dossier/figures.py:163-238` — `validate_spec` (the wall), `label_in_material`
  - `src/dossier/figures.py:242-262` — `choose_style_school` (audience + engine + format affinities)
  - `src/dossier/figures.py:296-347` — `plan_figures` (one repair round)
  - `src/dossier/figures.py:383-517` — `_revision_notes`, `render_figure` (prompt → render → check → retry → save)
  - `src/dossier/figures.py:520-563` — `run_figures` (skip law, incremental persist)
  - `src/dossier/figures.py:566-626` — CLI
- **Dependencies**: anthropic, google-genai, Pillow; env `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`
- **Added**: 2026-09-03

### Diagram Prompt and Check
- **Status**: Active
- **Entry Points**:
  - `src/images/figure_prompts.py:449-473` — `DIAGRAM_CLOSER`, `DIAGRAM_TEXT_RULES`, `_STYLE_LINE_DROP`
  - `src/images/figure_prompts.py:476-529` — `style_for_school`
  - `src/images/figure_prompts.py:532-614` — `build_diagram_prompt`
  - `src/images/compliance.py:182-231` — `DIAGRAM_CHECK_PROMPT`, `invented_sentences`, `diagram_verdict_ok`
  - `src/images/compliance.py:233-350` — `check_diagram`
- **Added**: 2026-09-03

## Notes for the integrator
- Old job records (scene figures) still load: `scene` / `visual_register` are optional on `FigureSpec`;
  the web `DossierFigure` type uses only key/caption/url/provider/cost_usd/prompt — unchanged.
- The figures step persists after every figure (`update_job(figures=…)`), so a killed run keeps its rendered diagrams.
- Attempts are saved as `figures/<key>.attempt<n>.<ext>` beside the served `figures/<key>.<ext>`; every attempt
  also lands in `FIGURES_DIR` with its own content-addressed `figure_id` (`<key>` and `<key>-a2`).
- 8 test files fail to collect and 11 tests fail on master already (unrelated modules); this branch adds no failures.
