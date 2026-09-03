# plates agent (V1) — change note

Branch `feat/plates`. Owner of `src/dossier/plates.py`, `src/dossier/plate_store.py`,
`src/dossier/templates/plates_appendix.html.j2`, the plates routes appended to `src/api/routes/dossier.py`,
`web/src/pages/Plates.tsx` (+ the plates entries in `types.ts`, `lib/api.ts`, `lib/mock.ts`, `router.ts`,
`App.tsx`, one link in `steps/DossierStep.tsx`, `web/mock/plates/plate-1.svg`), `tests/test_plates_spec.py`,
`communications/changes/plates-process.md` (the v1 process as extracted before coding) and this note.
Nothing in `src/dossier/{runner,compose,tables,spine,crosscheck}.py` or the workflow JSON was touched.

## What a plate is, and what changed

The owner's words (2026-09-03): the v1 renders "work not just as pieces to insert into a report — they also
work at the level of being the report itself … sometimes we want to generate both the report AND the huge
visualization so that we can actually see what's going on and where."

A **plate** is one dense 4K image that *is* the analysis. It is not a figure (a figure is one diagram inside
a section, ≤ 30 six-word labels); a plate carries 30–110 text elements — panels with full-clause items,
nodes with one-line definitions, labelled relations, stations with tributaries and locked-in branches,
register rows scored across typed columns — and is read instead of the memo. The process v1 used to make
them (reconnaissance → extraction → strategist perspective map → per-perspective render → vision check) is
written up stage by stage in `plates-process.md`; this branch ports it as a **standalone capability over a
finished dossier job**:

```
plan (Sonnet, forced-tool JSON)  →  PlateSpec[]     src/dossier/plates.plan_plates   (+ validate_plate_spec = the wall)
spec → declutter → prose lines   →  list[str]       declutter_plate / plate_content_lines   (code, no LLM; sizes as words)
prose → prompt                   →  str             build_plate_prompt   (v1's assembly order, see below)
prompt → 4K image                →  bytes           src.images.adapter.generate_image(gemini_pro, size="4K", aspect per family)
image × spec → verdict           →  dict            check_plate   (overview + 4 quarter tiles to Claude vision; label manifest; leak scan)
not ok → re-render ONCE with the reviewer's notes; keep the better attempt; both attempts, both verdicts, every receipt on the record
```

### Prompt assembly (v1's order, `build_plate_prompt`)

1. opening line + **READ FIRST** — v1's `QUALITY_PREAMBLE` rules that carry weight (text accuracy character
   for character; never print bracketed annotations, colour codes or decimals; mandatory title; no small text
   with the 4K minima; format compliance is auto-fail; Tufte; "senior executives who will immediately notice
   text errors")
2. `src.display.enforcement.enforcement_block(format)` — v1's MANDATORY FORMAT block verbatim
   (must_have / must_not / GLOBAL_PROHIBITIONS / legibility)
3. **PLATE LAYOUT GRAMMAR** — the family's mandatory structure (v1's `VISUAL_FORMAT_INSTRUCTIONS` re-cut per
   family; the register grammar carries the client renders' navy header / badge pill / glyph / strength-bar
   grammar; the scorecard the green/red panel grammar with the ↑/↓ glyphs and the translucent red X)
4. `build_style_override(style_for_school(school))` — the style sandwich's opening (semantic colours in the
   grammar win over the palette for those elements)
5. **CONTENT TO RENDER** — the canonical spelled out line by line by the family renderer; every size, position
   and strength as a *word* after a dash ("draw in very large type", "drawn as a thick band"), never a number
6. **LABEL MANIFEST** — every rendered string once
7. **TITLE** (+ "under the title: nothing"), a one-line CONTEXT (not rendered)
8. **TEXT RULES** — the figures' rules plus: whole strings, no "…" cut-offs, no truncation notes, no colour codes
9. **FRAME** (aspect at 4K) and **DENSITY** ("this is a plate, not a slide … no region is empty and no region
   is crowded")
10. **REVISION NOTES** (retry only) → closer + **FINAL REMINDER: LAYOUT IS MANDATORY** → style closing

### The leak class, closed

plate_a printed `[SIZE_GUIDE: 0.9]` after every item; r1 printed `truncass to 100 chars`; r3 printed
`#1e40af` as a badge — all three are a *rendering instruction printed as content*. Here: sizes live in
numeric keys (`size`, `x`, `y`, `strength`) that the label walker never renders; the renderers emit words;
`LEAK_RE` (brackets, braces, hex codes, decimals, `size guide`, `trunc…`, `weight:` …) rejects any planned
string at the wall, is asserted over the assembled CONTENT section before money is spent, and is run over
the vision verdict's `extra_text` — a leaked token in the image fails the attempt and becomes a revision
note ("REMOVE the leaked token …").

## PlateSpec — the contract (`src/dossier/plates.py`)

```python
class PlateSpec(BaseModel):
    key: str
    family: str                 # scorecard | framework_map | flow_map | power_map | timeline_of_shifts | register | layer_stack | argument_tree
    visual_format: str          # the enforcement format the family maps to (structured_diagram, network_graph, sankey_diagram,
                                #   positioning_map, timeline, matrix, conceptual_layers, argument_tree) — filled by the wall
    perspective: str            # "Scorecard of theoretical shifts", "Stakeholder power map" …
    title: str                  # <= 90 chars, rendered at the top
    canonical: dict             # the plate's ENTIRE content in the family's shape (below); sizes as NUMBERS 0..1
    narrative: str              # 3-5 sentences the reader needs; printed beside the plate, never in it
    size_guides: dict[str, float]   # label -> 0..1, extracted from canonical; kept out of the image
    style_school: str           # chosen in code from src/styles affinities (audience + engines + format)
    why_this_perspective: str
    claimed_territory: str      # v1's territory separation
    excludes: list[str]         # what the OTHER plates cover
    abstraction_level: int      # v1's 1 helicopter … 5 granular; distinct across a plan
    aspect: str                 # 16:9 | 4:3 | 3:4 | 1:1 … (family default when empty)
    anchors: list[FigureAnchor] # optional verbatim quotes; verified by the wall

class Plate(PlateSpec):         # the record (row in dossier_plates)
    figure_id, url, path, provider, model, prompt, width, height, cost_usd (images + checks), status
    (planned | generated | skipped | failed), note, compliance (the kept attempt's verdict), attempts[],
    receipts[] (every image and check receipt), grounding, declutter, created_at
```

### The eight families (`PLATE_FAMILIES`) — shape, rule, grammar

| family | enforcement format | aspect | canonical shape (keys ending ? optional) |
|---|---|---|---|
| scorecard | structured_diagram | 16:9 | `{quadrants:[{label, tone: gain|loss|neutral, items:[{label, note?, size}]}] (2-4 × 2-8), marks?:[{quadrant, kind: cross|check|arrow, label?}], links?:[{from,to,label}]}` |
| framework_map | network_graph | 16:9 | `{regions:[{label, note?, nodes:[{label, definition, size}]}] (1-3 × 2-7), relations:[{from,to,label}] (2-16), bridges?:[{from,to,label}], side_boxes?:[{label, items[2-6], region?}]}` |
| flow_map | sankey_diagram | 16:9 | `{current:{label, stations:[{label, note?, feeds?[≤4], drains?[≤3], size}] (3-9)}, branches?:[{label, from, steps[1-4], terminal}] (≤4)}` |
| power_map | positioning_map | 16:9 | `{x_axis, y_axis:{label,low,high}, quadrants?, actors:[{label, note?, x, y, size, group?}] (5-16), relations?:[{from,to,label}] (≤12)}` |
| timeline_of_shifts | timeline | 16:9 | `{tracks?[1-4], periods?:[{label,span}] (≤6), events:[{date,label,note?,track?,size}] (5-16), shifts?:[{from,to,label}] (≤6)}` |
| register | matrix | 3:4 | `{columns:[{label, kind: text|badge|glyph|number|bar}] (3-10), rows:[{label, starred?, cells[= columns]}] (3-12), legend?:[{badge,meaning,tone?}]}` — badge ≤ 3 words; glyph ∈ serial|convergent|linked|divergent|circular|none; bar a percentage |
| layer_stack | conceptual_layers | 4:3 | `{spine?, layers:[{label, note?, items:[{label, note?, size}]}] (3-7 × 1-6)}` |
| argument_tree | argument_tree | 4:3 | `{claim:{label,note?}, premises:[{label, note?, evidence?[≤4], rebuttal?, strength}] (2-6), verdict?}` |

Every string is rendered: labels ≤ 14 words / 100 chars, notes and definitions ≤ 24 words / 160 chars,
register cells ≤ 18 words / 120 chars; 16 ≤ text elements ≤ 110.

### The wall (`validate_plate_spec`)

Runs the declutter first (exact repeats removed, over-long notes/cells trimmed to the cap, the lowest-size
items dropped beyond the density ceiling — recorded on the plate), then rejects: unknown family; a shape
that does not fit; fewer than 16 or more than 110 text elements; a label over 14 words; a leaked token or an
ellipsis in any string; snake_case in printed text; a title over 90 chars; a narrative outside 2-7 sentences;
an abstraction level outside 1-5; a second plate in an already-used family or (n ≥ 2) at an already-used
level; and **ungrounded** content — fewer than 40 % of the short labels found in the material (verbatim, or
every significant word present; notes are the planner's paraphrases and are not held to this). Rejected
plates are re-asked once with the errors verbatim; still-rejected ones are `plate_skipped`, never fatal.

### The verdict (`check_plate`)

Five images go to Claude vision (`claude-sonnet-4-6`): the whole plate and its four quarters, each ≤ 1568 px —
a 4K plate downscaled once hides exactly the text a plate is made of. The answer is reconciled against the
manifest: `{ok, format_ok, detected_format, title_found, labels_found[], labels_missing[], misspelled[],
illegible[], prohibited_elements[], leaked_tokens[], extra_text[], density (sparse|adequate|dense),
legible_at_4k, suggestion, confidence, checked, model, usage, n_labels, issues[]}`.
`ok` = format_ok ∧ nothing prohibited ∧ nothing leaked ∧ not sparse ∧ no invented sentence ∧
missing+misspelled+illegible ≤ max(2, 20 % of the strings). Fail-open without a key (`checked=False`).

## Store, API, desk, appendix

- `src/dossier/plate_store.py`: table `dossier_plates(job_id, key, status, spec_json, figure_id, url, path,
  narrative, compliance_json, receipts_json, attempts_json, cost_usd, created_at, updated_at; PK (job_id,key))`,
  created lazily through `src.executor.db.execute`; `upsert_plate` (planned → generated/failed, after every
  plate — incremental), `list_plates`, `get_plate`, `delete_plates`; an in-process run registry
  (`mark_running` / `mark_done` / `run_state`). `dossier_jobs` is untouched; receipts still go through
  `src.dossier.receipts.record` onto the job (so the job's totals include the plates).
- `src/api/routes/dossier.py` (append only):
  `POST /v1/dossier/jobs/{id}/plates {n?: 1-3, perspectives?: [...], provider?}` → 202, runs `run_plates` in a
  daemon thread (409 when a run is in flight or the job has no analysis; 400 on n/provider);
  `GET /v1/dossier/jobs/{id}/plates` → `{job_id, running, run, plates[]}` (prompt replaced by `prompt_chars`);
  `GET /v1/dossier/jobs/{id}/plates/{key}.jpg` → the kept render; `DELETE …/plates`. Events under the job id,
  phase `plates` (`phase_started`, `call_started/finished/failed` per attempt and per check, `note` for the
  wall and the verdicts, `artifact` per plate and for the plan, `phase_finished`).
- `web/src/pages/Plates.tsx` at `/d/:id/plates`: record tiles (plates, passed the check, spent, run state), the
  make-plates form (1-3, optional named perspectives, one per line), one full-width card per plate (image →
  opens the 4K; perspective / family · format / level / verdict chips; title; narrative; why; record line
  with size, aspect, style, attempts, time, cost; **Download 4K**), polling every 3 s while a run is in
  flight. One link on the dossier step: "Plates — the analysis as one 4K diagram →". `?mock=1` replays one
  fixture plate on the seeded delivered job and simulates a run (planned ~4 s → generated).
  Screenshot: `web/docs/screens/07-plates.png` (mock).
- `src/dossier/templates/plates_appendix.html.j2` + `plates.appendix_context(plates, src_for)` /
  `render_appendix_html`: the "Plates" appendix the composer can `{% include %}` later — each plate
  full-width with its narrative and record line; renders nothing without plates.

## Samples (real renders)

_(filled in below as the renders land — plan, prompt, verdict and ≤ 600 KB copy of each plate under
`communications/changes/plate-samples/`)_

## Cost

_(filled in below)_

## What to integrate into the run later (not done here — another agent owns runner/compose)

1. A `plates` step after `crosscheck` in `src/dossier/runner.py` (`STEPS`, `STATUS_FOR_STEP["plates"] = "figures"`
   or its own `plating` status, `STEP_WHY`): `run_plates(job, job.options.output.plates, persist=upsert)`; the
   skip law already holds inside `run_plates`.
2. `OutputOptions.plates: int = 0` (and the brief's dial) — `output.plates` in the brief shape, alongside
   `figures`; the desk's Draft step shows "N plates" once the option exists.
3. `compose.py`: `{% include "plates_appendix.html.j2" %}` before "How this was made", with
   `plates=appendix_context(list_plates(job.id), src_for=...)["plates"]` in the render context; the PDF path
   copies each plate's kept render into `job_dir/plates/` (already where `render_plate` writes it) so the
   relative `src` resolves; `dossier.md` gets a "## Plates" section with the image link and the narrative.
4. The spine: when a job carries a section spine, `plate_material` already includes it (`_spine_text`); the
   planner can then be told which section each plate condenses (`condenses: [section numbers]`) so the
   composer can place a plate at the head of its section instead of only in the appendix.
5. Events: the desk's run rail (`web/src/lib/run.ts` `RAIL_STEPS`) gets a "Draw the plates" step keyed on
   phase `plates` once the runner emits it inside a run.
