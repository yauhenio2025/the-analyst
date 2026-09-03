# Plates — the v1 process, extracted before porting

Branch `feat/plates` (PLATES agent, V1). Written 2026-09-03 before any code, from a full read of
analyzer v1's `src/workers/pipeline.py:process_multi_visual_job` (2067-3794), the renderer
`src/renderers/gemini_image.py`, `src/core/visualization_palettes.py`, `src/core/unified_strategist.py`,
`src/core/opus_gatekeeper.py`, `src/renderers/declutterer.py`, and the seven reference renders the owner
pointed at (`v1-plates/plate_{a,b,c}` and the four 2026-08-24 client renders `recent/r1..r4`).

## What a plate is (the register study)

A **plate** is one dense 4K image that *is* the analysis: the reader reads it instead of the memo.

| render | size | what it is | text elements | grammar |
|---|---|---|---|---|
| plate_a | 5504×3072 | **Scorecard of theoretical shifts** — 2×2 panels GAINS / LOSSES × two eras; 4 items per panel, each a full clause; a red X across the failed quadrant; up/down arrows per item; an arrow "EVOLVED TENSIONS" linking the loss panels; source line | ~22 | green panels for gains, red for losses; bold panel headers on tinted bands |
| plate_b | 5504×3072 | **Two-paradigm conceptual framework** — dashed frame; two tinted halves (blue AGENTIAL REALISM / orange CRITICAL REALISM); 4 nodes per half, each with a CAPS title and a one-line definition inside the node; labelled relations on the edges (ENABLES, CONTRASTS WITH, MUTUALLY CONSTITUTIVE, RECOGNIZES DISTINCTNESS, CHARACTERIZED BY); a double arrow "DIFFERING ONTOLOGICAL ASSUMPTIONS" across the divide; APPLICATIONS and LIMITATIONS lists in grey boxes | ~45 | rounded nodes, thick coloured outlines, CAPS titles, sentence-case definitions |
| plate_c | 5504×3072 | **River / flow map of evidential foundations** — a main current with 7 named stations; tributaries (claims) feeding each station from above and below; three downstream "conceptual commitments" branching off, each with 2-3 consequences ending in "Locked In" | ~40 | soft gradient ground, flowing bands, text on the bands' banks |
| r1–r4 | 3584×4800 portrait | **Argument-architecture registers** — a dark navy header band; columns ID · ★ · CONCLUSION · CERTAINTY · TYPE · INFERENCE PATTERN · STRUCTURE · PREMISES · WARRANT (· EXPLICITNESS · CASCADE RISK · DOCS · STRENGTH); badge pills with a fixed colour code (HIGH/PROB/POSS in blues; IND green, ABD rust, CAUS red, DEFIN grey, STAT blue, AUTH purple, NORM pink); structure glyphs (serial →→, convergent ⇒, linked ⊕); starred rows tinted warm; strength bars with a percentage | 60–90 | table grammar, tabular density, one message per row |

**The leak bugs to design against** (all three are the same class: a *rendering instruction* printed as *content*):
- plate_a prints `[SIZE_GUIDE: 0.9]` after every item — v1's `_format_citations` and siblings append
  `[SIZE_GUIDE: … - use for node size, don't display]` to the content lines (gemini_image.py:3990), and the
  QUALITY_PREAMBLE's "Any text in square brackets is for YOUR visual encoding decisions only" is not enough.
- r1 prints `truncass to 100 chars` under a conclusion — a truncation *instruction* from the table formatter.
- r3 prints `#1e40af` as a badge — a palette hex code passed as text.

The port keeps every number, size and colour instruction **out of the content block**: sizes are spelled
as words in the layout lines, hex codes never touch the content, and a regex leak scan runs over the
assembled prompt (unit-tested) and over the vision verdict's `extra_text` (a leaked token fails the plate).

## The v1 pipeline, stage by stage (what each contributes)

`process_multi_visual_job` (pipeline.py) — the multi-visual job that made plates a/b/c:

1. **Reconnaissance** (2344): `run_reconnaissance_if_enabled` reads the collection first — collection type,
   unifying theme, key tensions, per-document summaries, a reality-sampling pass that corrects the strategy —
   and yields `reconnaissance_guidance` + `field_priorities` that steer extraction. *Contribution: the
   corpus is characterised before anything is drawn.* → The Analyst already has this as step 1
   (`job.profiles`: profiles + corpus map); plates read it.
2. **Extraction** (2427): per-document engine extraction with the recon guidance; fail-fast when every
   document failed. → The Analyst's engines produce prose (`job.analysis`), not canonical JSON; plates read
   the prose, the verified tables and the composed sections.
3. **StrategicAnalyzer** (2570, optional): over raw extractions, identifies distinct analytical
   *territories* and assigns one per output BEFORE curation, so curation preserves diversity
   (`curation_focus_gaps`, `validate_abstraction_diversity`). *Contribution: territory separation
   decided early.*
4. **Curation** (2650): `curate_extractions` merges the per-document extractions into one canonical dataset
   + a legend, guided by the focus gaps.
5. **Guidance verification** (2686): `verify_extraction_compliance` scores how well the curated data honoured
   the recon guidance (compliance score, high-priority fields checked).
6. **Pattern detection** (2740): `detect_patterns` — universal + domain detectors over canonical; the findings
   (and a narrative arc from `structural_pattern_detector`: dominant structure, arc stages, thematic
   progression) ground the strategy.
7. **Abstraction evaluation** (2798, "Option E"): `run_abstraction_evaluation` checks the
   abstraction/precision balance of the canonical data and fills gaps from the documents (passes, items
   added).
8. **UnifiedStrategist perspective map** (3007-3055): the heart. `StrategyConfig(include_text=False,
   image_count, table_count, target_audience, emphasis_hint, use_iterative_generation=True,
   use_creative_phase=True, diversity_threshold=0.65)`. Two phases:
   - *creative analysis* (unified_strategist.py:855): "You are a creative strategist analyzing document
     analysis results … identify what visualization approaches would be most effective" → JSON with
     `visual_opportunities[{data_key, why_visual, suggested_format, arc_position}]`, `narrative_themes`,
     `recommended_ordering`, `synergy_ideas`.
   - *iterative per-visual generation* (1189): one call per visual with everything already claimed in
     context ("Already Covered — Territories / Data keys used / Terms used"), a **mandatory abstraction-level
     diversity rule** ("HARD RULE: You CANNOT use a level that already appears N+ times … Level 1
     (Helicopter): Systemic patterns, paradigm competition, field-wide dynamics; Level 2 (Framework):
     Theoretical structures, categorical relationships, type hierarchies; Level 3 (Analytical): Specific
     mechanisms, causal chains, detailed comparisons; Level 4 (Evidential): Concrete examples, case studies,
     empirical instances; Level 5 (Granular): Direct quotes, specific data points, textual evidence"), a
     format guide that **prefers spatial formats** ("KEY PRINCIPLE: Prefer SPATIAL PROPERTIES (proximity,
     size, containment) over arrows"), and an aspect guide ("3:4 portrait for VERTICAL structures … 16:9
     for HORIZONTAL … 1:1 for RADIAL/CENTERED"). Output per visual: `{visual_id, data_key, focus_area,
     story_angle, visual_format, why_visual_helps, claimed_territory, excludes[], aspect_ratio,
     pdf_scale, abstraction_level}` → `PerspectiveSpec` (multi_output_strategist.py:50): `output_id,
     output_type, perspective_name, focus_area, data_keys, story_angle, claimed_territory, excludes,
     format_hint, format_description, aspect_ratio, pdf_scale, why_image_not_table,
     palette_visualization_id, abstraction_level`.
   - a diversity score, term coverage, a redundancy audit ("how each pair differs") and a synergy plan
     (narrative groupings: foundational first, development middle, synthesis last).
   *Contribution: N perspectives that each own a territory, at different abstraction levels, in different
   formats, with a stated question each answers.*
9. **Enrichment** (3075, optional): `run_enrichment_pass` goes back to the source documents to extract
   perspective-specific content so sibling outputs overlap less (<40% entity overlap); optionally re-curates
   and re-runs the strategist.
10. **OpusGatekeeper** (3263, optional): an Opus audit of the strategy against five desiderata before any
    render — *label uniqueness, territory separation, format diversity (VIOLATION if >50% of images use the
    same format), prompt clarity, coverage completeness* — with HIGH/MEDIUM/LOW violations and a revision
    pass ("PASS the strategy only if there are NO HIGH-severity violations and at most 2 MEDIUM").
11. **Per-perspective render** (3369-3483): for each `PerspectiveSpec` a `visual_assignment`
    (`focus=story_angle, show_elements=focus_area, primary_data_keys=data_keys, exclude_elements=excludes,
    format_hint, aspect_ratio, pdf_scale, visual_emphasis=perspective_name, palette_visualization_id`) →
    `GeminiImageRenderer.render(canonical, legend, config)`; tables go to `SmartTableRenderer`. Each output
    is enriched with `perspective_title, visual_format, story_angle, abstraction_level`. Render errors skip
    the output and continue.
12. **Narrative** (3516): `TextRenderer.render` writes the prose that sits beside the outputs
    (`text_assignment`, `perspective_map`, `narrative_groupings`).
13. **Gallery / PDF** (3549): `IntegratedReportAssembler.assemble(assembly_mode="gallery", embed_images=False)`
    → HTML + PDF; result JSON to S3.

### How `viz_spec` was produced

`visualization_palettes.py` defines, per engine, a `VisualizationPalette(engine_key, visualizations=[VisualizationSpec], tables=[TableSpec], max_visualizations, max_tables, selection_guidance)`. Each
`VisualizationSpec(id, name, insight, visual_metaphor, visual_format: VisualFormat, prompt_template,
complexity, required_data, optional_focus, philosophical_grounding)`. The strategist picks
`palette_visualization_id`s; the renderer then injects (gemini_image.py:3153)
`## PALETTE-SPECIFIC VISUAL FORMAT — VISUALIZATION TYPE / PRIMARY INSIGHT TO REVEAL / VISUAL STRUCTURE
(FOLLOW THIS) / LAYOUT REQUIREMENTS (MANDATORY) = VISUAL_FORMAT_INSTRUCTIONS[format] / CRITICAL OVERRIDE:
IGNORE any later instructions about 'choosing visualization type based on data' … This visualization MUST
use X layout - NOT a network diagram, NOT a generic chart. Failure to follow this layout is an automatic
failure.` plus "OTHER VISUALIZATIONS IN THIS SET (use different visual approach)".

`VISUAL_FORMAT_INSTRUCTIONS` (palettes.py:50-290) is the per-format "VISUAL STRUCTURE (MANDATORY)" block —
e.g. QUADRANT_GRID: "Draw a 2x2 GRID with clear dividing lines / LABEL each quadrant clearly / Items placed
INSIDE their respective quadrants / Quadrants should be: gains/losses or +/- structure / Use color coding:
green for positive, red for negative" (this is plate_a's grammar); TWO_COLUMN_SPLIT: "Draw a VERTICAL LINE or
WALL down the center … Use contrasting colors: e.g., blue territory vs orange territory" (plate_b's halves);
RIVER_TRIBUTARIES: "Multiple SOURCES at the TOP … Streams FLOW DOWNWARD and MERGE … Use flowing curved
lines, not angular arrows / Label each tributary with its source type" (plate_c). Size guides came from the
content formatters: numeric scores in canonical were either converted to words by the Haiku formatter
("Convert numeric scores (0.0-1.0) to semantic descriptions: 0.9+ = very high …; NEVER include the word
'score' or show decimal numbers") or, in the legacy hardcoded formatters, emitted as
`[SIZE_GUIDE: … don't display]` — the bug.

### The renderer's assembly order (gemini_image.py `render`, 1753-2520)

1. `data_for_viz` = canonical filtered to the perspective's `primary_data_keys` (+ meta) — one perspective,
   one slice of the data (2106-2130).
2. Source-attribution scrub of the data (`_sanitize_canonical_for_source_suppression`).
3. **Scene prose** (`_format_content_for_prompt_async`, 3507): Haiku turns the JSON into
   "DATA FOR VISUALIZATION: (NOTE: Importance levels are for VISUAL ENCODING - sizing, positioning,
   emphasis. Do NOT display them as text labels.)" + sections with bullets, 10-15 items per section,
   snake_case → Title Case, no IDs, no decimals; hardcoded per-engine formatters as fallback.
4. **Declutter** (`declutterer.declutter_content`, max_elements=10 default, strategy by engine archetype):
   Sonnet compresses with **named preservation** — "NEVER output '[3 categories]' or '[N items]' - ALWAYS
   list the actual names"; argumentative = hierarchical compression keeping all claim names; network = top-N
   named nodes; temporal = period clustering with key events named.
5. `prompt = QUALITY_PREAMBLE + template.format(content)`. QUALITY_PREAMBLE (gemini_image.py:42-113),
   the load-bearing text rules: "ONLY use text EXACTLY as provided in the data below - character for
   character … If you cannot render exact text clearly, OMIT the element entirely … NEVER show any
   bracketed annotations containing internal instructions / NEVER show decimal numbers like 0.75, 0.9, 0.85
   anywhere in the image / NEVER show technical labels like 'THICKNESS', 'WEIGHT', 'STRENGTH', 'CONFIDENCE',
   'SIZE' with numbers … MANDATORY TITLE … NO SMALL TEXT RULE: ALL text must be clearly readable - minimum
   14pt equivalent at 4K; If text would be too small to read comfortably, OMIT IT ENTIRELY … FORMAT
   COMPLIANCE (AUTO-FAIL IF VIOLATED) … AUDIENCE: Senior executives who will immediately notice text errors."
6. SPECIFIC FOCUS block (the story angle) wrapping the prompt.
7. `_build_multi_output_context` (3250): "MULTI-OUTPUT COORDINATED REPORT CONTEXT — This is output X of N
   … YOUR ASSIGNED TERRITORY: Focus Area / Story Angle / Claimed Territory … WHAT YOU MUST AVOID (covered by
   other outputs) … DETAILED SIBLING ANALYSIS … ACTIVE DIFFERENTIATION REQUIRED … Show ONLY what falls within
   your claimed territory."
8. Palette focus instructions (above) prepended; then the **format enforcement block**
   (`get_format_enforcement_prompt`, ported verbatim to `src/display/enforcement.enforcement_block`:
   MANDATORY FORMAT / REQUIRED ELEMENTS / ABSOLUTE PROHIBITIONS / UNIVERSAL DATA VISUALIZATION RULES =
   GLOBAL_PROHIBITIONS / TEXT LEGIBILITY IS NON-NEGOTIABLE) and the content-format conflict warning.
9. **Style guide sandwich** (`_build_style_guide_directive` 2640 → top, `_build_style_guide_closing_directive`
   2759 → bottom; ported as `build_style_override` / `build_style_closing`): "the TOP-only placement was
   losing to engine-specific palette directives in 100% of cases".
10. Source attribution block; `_strip_source_leaks`; **FINAL REMINDER: LAYOUT IS MANDATORY** at the very end
    (recency).
11. `client.generate_image(prompt, aspect_ratio, output_format="png")` — `src/llm/gemini.py:223`
    `image_size="4K"` default ("uppercase K required!"), 600 s timeout, retry when the model answers with
    text instead of an image.
12. **Claude-vision compliance** (`validate_format_compliance`, 1604): pass_if / fail_if criteria per format
    → `{compliant, confidence, detected_format, issues[], recommendation}`; a failed check is logged, not
    retried, in v1. (The Analyst's figures step added the retry-once-with-the-reviewer's-notes.)

## What the port keeps, and what it changes

| v1 | plates (this branch) |
|---|---|
| canonical JSON per engine + legend | the job's analysis prose, verified tables, profiles, composed sections, the chosen telling (and the spine when a job has one) |
| UnifiedStrategist: N perspectives, territories, abstraction levels, format + aspect per perspective, excludes, redundancy audit | `plan_plates`: ONE Sonnet forced-tool call that returns 1-3 `PlateSpec`s with the same fields (perspective, claimed territory, excludes, abstraction level, family/format, aspect) **and the complete canonical content model filled in** — the strategist and the content formatter collapsed into one grounded pass, because the material is prose, not a schema |
| OpusGatekeeper desiderata | code: distinct families per plate, distinct abstraction levels where n ≥ 2, density floor, label/definition length caps, leak scan, grounding of content labels in the material (the figures wall's `label_in_material`) |
| Haiku scene prose + Sonnet declutter | deterministic: each plate family has a prose renderer that spells the layout out line by line with sizes as words; `declutter_plate` dedupes, trims and drops the lowest-size items beyond the family cap, and records what it dropped (no LLM between the grounded spec and the image — the leak class dies here) |
| QUALITY_PREAMBLE + format enforcement + palette focus + style sandwich + FINAL REMINDER | same order: plate preamble (v1's text rules, verbatim where they matter) → `enforcement_block(format)` → PLATE LAYOUT GRAMMAR (v1's VISUAL_FORMAT_INSTRUCTIONS re-cut per family, with the client renders' badge/header grammar for registers) → style override → CONTENT lines → LABEL MANIFEST → TITLE → TEXT RULES (+ no brackets / no hex / no "truncated") → FRAME → REVISION NOTES → closer + FINAL REMINDER → style closing |
| Gemini 4K | `generate_image(provider="gemini_pro", size="4K", aspect=family aspect, no_text=False)` — $0.24/plate |
| one vision check, no retry | overview + four quadrant tiles to Claude vision (a 4K plate downscaled to 1568 px hides its labels), leak scan on `extra_text`, one revision with the reviewer's notes, keep the better attempt; both attempts, both verdicts and every receipt on the record |
| gallery HTML/PDF | `plates_appendix.html.j2` partial + `GET /plates` gallery on the desk; the composer includes the partial later |
