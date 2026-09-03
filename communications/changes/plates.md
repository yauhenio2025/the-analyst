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

Each sample directory holds `specs.json` (the plan), `<key>.prompt.txt` (the exact prompt sent),
`<key>.verdict.json` (spec, both attempts' verdicts, grounding, declutter report, cost) and `<key>.jpg` (a
≤ 600 KB copy; the 4K original lives in `data/dossiers/<job>/plates/` where `GET /plates/<key>.jpg` serves it).

### 1. `plate-samples/risk/partnership_risk_register` — job `dossier-afede514d4cf` (partnership risk register, 5 papers, advanced)

Requested perspective: "a partnership risk register: one row per state-type partnership … scored across typed
columns". Family **register** (matrix, 3:4), level 3; 8 typed columns (text ×5, badge ×2, bar) × 4 rows (2 starred),
7 legend badges — **50 strings**; planned in two Sonnet calls (the first answer wrote `80` in a bar cell instead of
`80%`; the repair fixed it). Rendered once by `gemini_pro` at **3584×4800** in 52 s; check: `ok`, format_ok
("dense badge-and-glyph table / register with dark navy header band, alternating pale rows, coloured pill badges,
and bar-glyph exposure scores"), **45/50 strings found**, 0 misspelled, 0 illegible, 0 leaked, 0 prohibited,
density dense, legible at 4K.

**My verdict against r1–r4: a plate I would show an executive.** It is the client register grammar realised —
navy header, one colour per badge word across the whole plate (POLITICAL blue, FINANCIAL rust, INSTITUTIONAL grey,
INDUSTRIAL purple; CONDITIONAL orange, CAUTION yellow, DECLINE red), segmented strength bars with the percentage,
starred rows tinted warm, a legend strip; every cell is legible in the quarter tile. The narrative beside it is
what an executive needs to read it. Two flaws, both traced to the contract and fixed in code the same hour:
(a) the planner wrote 8 cells for 8 columns although the row label already fills the first column, so the model
dropped one orphan cell per row — the four "Reversal constraint" explanations are the strings the check
counted missing → the register contract now says *cells = columns − 1* and the validator enforces it;
(b) four 16–18-word text cells are cut at the row boundary ("…liability across the entire") — no "…", no
truncation note (the two client bugs did not recur), but the row was not allowed to grow → the grammar now says
"a row is as tall as its longest cell needs — never cut a cell short" and cells are capped at 16 words.

### 2. `plate-samples/state/sovereign_investment_scorecard` — job `dossier-dce25aeed631` (who wins when states back tech and defence, 5 papers, medium)

Perspective "What governments promise versus what they deliver"; family **scorecard** (structured_diagram, 16:9),
level 4. Four panels — GAINS: Named Corporate Winners (9 items), LOSSES: Community Promises vs. Documented Reality
(6), NEUTRAL: Regulatory Instruments That Made Transfers Possible (5), LOSSES: Costs Left on Public Balance Sheet
(5) — each item a full clause with a one-line source note; a check mark across the gains panel, a red X across
the promises panel, two labelled link arrows; **55 strings**. Planned in two calls (a 112-char title and a
26-word item were repaired). Rendered once at **5504×3072** in ≈ 90 s; check: format_ok ("2x2 grid of labelled
panels with colour-coded header bands and stacked text items with arrow glyphs"), **52/55 strings found**, 1
misspelling (undersved), 0 illegible, 0 leaked, 0 prohibited, density adequate, legible at 4K. After the
manifest-aware rescoring (the two mark banners the checker filed as "extra text" are manifest strings): **ok**.

**My verdict against plate_a: a plate I would show an executive, and a better plate_a than plate_a.** Same
grammar — green/red header bands, ↑/↓/• glyphs, the translucent check and X, the labelled curved links between
panels — with the source line under every item and no `[SIZE_GUIDE: 0.9]` anywhere. Flaws: the 9-item gains
panel rendered 7 (Lockheed Martin/Raytheon, the AUKUS VC network and Andreessen Horowitz/Sequoia were dropped
for room — eight is the ceiling, and the declutter now caps scorecard panels at 8); one item is cut at a dash
("…via Microsoft 365 and Azure —"); one misspelling.

### 3. `plate-samples/state/government_vocabulary_framework_map` — same job

Perspective "How government vocabulary moves a deal from announcement to capture"; family **framework_map**
(network_graph, 16:9), level 2. Three regions (STAGE 1 — FOUNDATION, STAGE 2 — RECLASSIFICATION, STAGE 3 —
DEFENCE) of 4 / 5 / 4 nodes, each node a CAPS title with a one-line definition inside; 14 labelled relations
(LICENSES, DESIGNATES, ENABLES, ACTIVATES, RECLASSIFIES INTO, JUSTIFIES, TRIGGERS, CONVERTS INTO, PERFORMS AS,
DEMANDS, PROTECTS, LEGITIMISES, PAIRED WITH, ANCHORS); two bridges; two side boxes of six bullets ("EXECUTIVE
SIGNALS: What Each Term Means in Practice", "DOCUMENTED CASES WHERE TERMS WERE DEPLOYED") — **62 strings**.
Rendered once at **5504×3072**; check: format_ok ("labelled network relationship graph with tinted regional bands,
rounded-rectangle nodes, and directed labelled arrows"), **59/62 strings found**, 0 leaked, 0 prohibited,
density dense, legible at 4K; 1 misspelling (depondency; the checker's "DEMANES" entry named no manifest string
and is dropped by the rescoring), 1 illegible, 3 missing. After rescoring: **ok**.

**My verdict against plate_b: near executive-grade; one revision away.** The grammar is plate_b's, denser —
dashed frames, tinted regions with subtitle lines, definitions inside every node, small-caps relation labels,
both side boxes. Flaws a reader would notice: the "De-risking" node was dropped and "STRATEGIC PARTNERSHIP" is
drawn twice in its place (the model filled a 2×2 slot); "DEMANES" for DEMANDS on one arrow; the second bridge
label is missing. These are exactly what the revision pass is for — `revision_notes` would have said "render
De-risking; spell DEMANDS; render the bridge label" — and the render was run at `--max-attempts 1` to stay
within budget. Recorded as such rather than re-rendered.

**Overall: 2 of 3 plates are ones I would show an executive as rendered (register, scorecard); the third would
be after the revision the design already provides.** None leaked a token, none drew a metaphor, all three carry
the analysis as one image.

### What the planning rounds taught (the wall's evolution, in the order the evidence arrived)

The planner's answers were dense and grounded from the first call; every rejection was the wall being stricter
than the register the owner pointed at. Each round cost ≈ $0.16–0.32 (23–31K input tokens, two calls), so the
rule became: **a marginal overrun is repaired in code, never re-asked**.

| round | what the wall rejected | what the v1 plates say | fix |
|---|---|---|---|
| state #1, risk #1 | a 14-word panel header (cap 12), a note of 163 chars (cap 160), a panel of 9 items (cap 8) | plate_a's items are 8–12-word clauses; its panels hold 4, the planner fills 6–9 | labels 14 words; notes and cells trimmed by the declutter before the wall; per-family list caps enforced by the declutter (keep the largest-size items, record the drops) |
| state #2 | `USD 1.28 billion` flagged as a leaked decimal; 15–19-word statements | the leak class is `0.x` scores, not amounts | decimal rule narrowed to `0\.\d+`; labels are statements: 20 words |
| state #3 | 22–23-word statements; one relation whose endpoint named no node | a plate line can run to ~24 words at 4K | labels 24 words / 170 chars; a dangling edge is dropped by the declutter, not re-asked; rejected specs are recorded (`rejected.json`, event payload) so a failed plan is never lost |
| risk #2 | `80` in a bar cell | r3's bars print `78%` | (planner error, repaired by the re-ask as designed) |
| state #4 | a 112-char title; a 26-word statement | a two-line title at 4K is fine | titles 120 chars (the 26-word statement was rightly re-asked) |
| the renders | the checker filed the mark banners and its own commentary ("DEMANES (appears to be…)") as *extra text*, failing two good plates | — | one manifest-aware `rescore_verdict`: stripped commentary; a string that is or contains a manifest string is not invention; a near-match (difflib ≥ 0.8) is a misspelling; `check_plate` reuses it, and stored verdicts can be re-scored without a vision call |
| the renders | a 9-item scorecard panel rendered 7; an 8-cell register row for 8 columns dropped a cell | plate_a holds 4–8 per panel; r1–r4 rows fill columns−1 cells | declutter caps scorecard panels at 8; register contract `cells = columns − 1` |

## Cost

| item | calls | USD |
|---|---|---|
| risk register — planning (2 rounds × 2 calls; the first round under the too-strict wall) | 4 Sonnet | 0.56 |
| risk register — render (1 attempt, 3584×4800) + check (5 tiles) | 1 image + 1 vision | 0.29 |
| state — planning rounds #1–#3 under the evolving wall (all rejected) | 6 Sonnet | 0.98 |
| state — planning round #4 under the corrected wall (1 repair) | 2 Sonnet | 0.33 |
| state — two renders (1 attempt each, 5504×3072) + checks | 2 images + 2 vision | 0.58 |
| unit tests, mock desk, API proof, rescoring | 0 | 0.00 |
| **total** | 12 Sonnet, 3 images, 3 vision | **2.74** |

Against the $2.50 budget: **$0.24 over**, all of it planning rounds spent while the wall was stricter than the
register the owner pointed at (≈ $1.30 of the $1.87 planning bill produced no accepted spec). With the corrected
wall a plan costs $0.16–0.33 and a plate $0.29 rendered and checked; the revision pass, when taken, adds $0.29.
A three-plate run over a finished job should now cost ≈ $1.2–1.5.

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
