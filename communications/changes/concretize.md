# concretize agent (C2) — change note

Branch `feat/concretize`. Phase 0 + Phase 1 of `communications/DESIGN_concretization_passes.md` (§C passes S, E, D, X;
§D implementation map), with de-llm's composition read folded into the spine and "frames written last" folded into the
draft (`STUDY_de-llm_longform.md` §D.1 passes 1 and 4). Owner's words: *"as different parts concretize, the entire
thing gets better … everything should hang together organically; if it doesn't, it's shit."*

## What changed — the pipeline

```
reconnaissance → brief → plan → analysis
  → SPINE       (S)  src/dossier/spine.py      composition read, then: thesis · 3-7 sections with ONE claim each ·
                                              per-section table spec / figure spec · planned anchors · summary job ≠ conclusion job
  → TABLES      (E1) src/dossier/tables.py     exactly the tables the spine commissioned, keyed by section_key, `proves`
  → FIGURES     (E2) src/dossier/figures.py    exactly the diagrams the spine commissioned → the merged diagram pipeline unchanged
                                              → record gains detected / checked_ok; failed check = finding
  → COMPOSE     (D)  src/dossier/compose.py    body written WITH the exhibits (every cell; each picture as actually drawn),
                                              [[table:key]] / [[figure:key]] at the pointer; then summary + close against the body
  → CROSS-CHECK (X)  src/dossier/crosscheck.py the judge over the real things + code clamps → findings ledger with fates;
                                              medium+: one round of safe automatic realizations, re-render only what changed
  → receipts
```

`STEPS = (reconnaissance, brief, plan, analysis, spine, tables, figures, compose, crosscheck, receipts)`; statuses gain
`spine` and `crosscheck`. `src/workflows/definitions/dossier_standard.json` is v2 with ten phases (the console prints
them). Every pass obeys the skip law: `spine_unavailable` sends tables/figures/compose down their legacy paths;
`crosscheck_unavailable` keeps the clamps and proceeds.

## The contract (schemas, `src/dossier/schemas.py`)

- `DossierSpine {round, read: CompositionRead, thesis, reader_question, handle, through_line, summary_job, conclusion_job,
  sections: [SpineSection], exhibits_budget, notes}`; `SpineSection {key, heading, claim, reader_needs_next, evidence_kind,
  table: SpineTableSpec | null, figure: SpineFigureSpec | null, anchors_planned: [Anchor], feeds}`;
  `SpineTableSpec {intent, row_unit, columns, carries_claims}`; `SpineFigureSpec {primitive, visual_format, picture_shows,
  caption_says, why_a_picture}`; `CompositionRead {plain_summary, buried_crux, readers, strands, prose_to_table,
  table_to_prose, figures_earned, figures_dropped, cumulative_direction, form_capacity}`.
- `Table` gains `section_key`, `proves`. `Figure` gains `section_key`, `picture_shows`, `caption_says`, `detected`
  (what the picture ACTUALLY shows, from the check), `checked_ok`. `Section` gains `section_key`, `exhibit_refs
  [{key, sentence, mismatch}]`; paragraphs carry `[[table:key]]` / `[[figure:key]]` tokens. `Sections` gains
  `summary_job_met`, `conclusion_job_met`, `spine_round_consumed`.
- `Finding {id, kind ∈ FINDING_KINDS, where {section_key, table_key, figure_key, paragraph_index, anchor_n}, quote, note,
  affordance ∈ AFFORDANCES, realization, recommended, source ∈ wall|clamp|judge, round, status, fates: [Fate]}`;
  `CrossCheckVerdict {round, hangs_together, summary, findings_minted, clamps, judged, what_changed, realized}`.
- `DossierJob` gains `spine`, `findings`, `crosscheck`; store columns `spine_json`, `findings_json`, `crosscheck_json`
  (guarded `ALTER TABLE` for existing DBs). `GET /v1/dossier/jobs/{id}` returns them (no route change needed).

## Walls (shape only; every wall teaches its exit)

| pass | wall | retry | after the retry |
|---|---|---|---|
| S | 3-7 sections; unique keys; claim = ONE sentence (abbreviations tolerated); thesis one sentence; `caption_says` no digit run; primitive/format in the catalog; table spec 2-6 columns + row unit + carries_claims; anchors verbatim and untrimmed (a fragment is refused); feeds name real keys; summary job ≠ conclusion job; Σ exhibits ≤ budget | one FIELD patch — only failing sections re-asked, merged by key, whole re-validated | code: first sentence kept, digits stripped from a caption or the spec dropped, over-budget exhibits dropped (earliest first), all recorded in `spine.notes` |
| E1 | anchor wall per row; `section_key` ∈ commissioned; ≤ 1 table per section; ≥ 2 rows | re-ask ONCE for the sections that fell short, failed quotes listed, on the cached prefix | `table_unavailable` finding (affordance add_table, realization = the spec); dropped rows → `table_rows_dropped` |
| E2 | `validate_spec` (format, data family, labels, grounding) + primitive as commissioned + caption no digits + ≤ 2 sentences + one format per figure | one repair for the rejected specs | `figure_unavailable` finding; render/check as merged; `checked_ok: false` → `figure_depicts_other` |
| D | section order = spine order; every expected exhibit placed exactly once, never as a section's last thing; unknown tokens refused; no number the material does not carry; claim marks in range; anchors verbatim (fragment = error) | one SECTION-SCOPED patch on the cached prefix | code: re-order, strip duplicates/ghosts, insert a forgotten token in its spine section (+ `exhibit_unpointed`), fragment anchors unfootnoted (+ `anchor_fragment`), writer's `mismatch` → `figure_depicts_other` |
| D frames | close shares < 15 % of its 8-word phrases with the summary; no identical paragraph; no new numbers; title ≤ 12 words | one re-ask | kept; the cross-check's clamp sees it |
| X | kinds/affordances enums; `where` names things on the page; `quote` verbatim on the page (normalized); rewrite cures need a realization; repeats merged into their target; ≤ 20 | none (a failed judge is `crosscheck_unavailable`) | clamps by arithmetic regardless: caption digit, exhibit no token placed, failed picture check, redundant frames; fate completeness — silence ⇒ `persists` by code |

## Realizations (medium+, one round, exhibits first, zero-change gate)

`rewrite_caption` (from `caption_says` or digits stripped) → `drop_table` / `drop_figure` for an unplaced exhibit →
≤ 1 `rerender_figure` / `revise_figure_spec` through `render_figure(…, revision_notes=[the judge's words])` (an added
INPUT; the pipeline is otherwise byte-identical), fates `resolved` / `persists` / `failed` recorded, then `render_all`
only if something changed. `simple`: report only. Phase 2 (revise work order: section rewrites, row revisions,
re-anchoring) and Phase 3 (read-through) are not built.

## Cost accounting

`src/dossier/llm.py`: user prefix can be cached (`cache=True`) with an uncached `user_tail`; images (bytes, mime) ride
between them for vision judges. Receipts price cache reads at 0.1× and writes at 1.25× (`_cached_cost`). Caching is
opt-in for the desks that re-ask (spine, tables, figure specs, draft, frames) — a single-shot call must not pay the
write premium. The live run below still paid it on reconnaissance (the fix landed after the run started).

## Desk + console (`web/src`)

- Rail: ten steps (Decide the argument · Build the tables · Draw the figures · Write with the exhibits · Cross-check the
  whole · Delivered); `STEP_TO_RAIL` maps the backend's step names (`brief`, `plan`, `compose`, `receipts`, `spine`,
  `crosscheck`) onto rail keys — live events used to fold into "Run the analysis" because the web assumed status names.
- Draft page, "the analysis behind it": **The spine** (thesis, one claim per section with its exhibits, the two frame
  jobs, the composition read, what the walls changed) and **Cross-check findings** (species · where · effect and cure ·
  affordance · fate). Dossier page: the cross-check chip with links to both. Console: the passes appear as phases.
- Placement tokens are shown in the desk's prose as *[table key is placed here]* marks; the composed HTML places the
  exhibit there.
- `?mock=1`: `web/src/lib/mock_concretize.ts` adds the spine, three findings with fates, the verdict and the two
  phases' events to the Kering replay (Playwright-checked: draft?item=spine, draft?item=findings, console rail + tree).
  The replay's "Delivered" narration still says "15 calls · $1.52" (fixture text in `web/mock/events.json`, outside
  this branch's paths) while the meter now sums 17 calls · $1.74.

## Tests (no network)

`tests/test_spine_walls.py` (14), `tests/test_exhibits_from_spine.py` (7), `tests/test_compose_tokens.py` (9),
`tests/test_crosscheck_clamps.py` (11). `python -c "from src.api.main import app"` ✓; `cd web && npm run build` ✓.

## Live run — `fashion_bundle.txt`, executive, medium, 2 figures, local server (SQLite)

Job `dossier-59263a6a2227` (local, `data/dossiers/` — not committed). **Title:** "Three Structural Flaws That Will Outlast
Every Sustainability Campaign". The material decided the brief ("Where Our Sustainability Claims Can Be Attacked",
stress_test); the plan ran `argument_architecture@standard → inferential_commitment_mapper@standard` (4 passes).

**How the run went, honestly.** The job ran once end to end and came back at $3.70 with the spine step recording
`spine_unavailable: call_json() got an unexpected keyword argument 'cache'` — I had patched `llm.py` under the live
server (no `--reload`) while `spine.py` was imported lazily, so the new spine met the old `call_json`. The skip law did
exactly what it is for (legacy tables/figures/compose ran; cross-check ran clamps only), but the new passes were not
exercised. Rather than re-buy the $2.3 analysis, I snapshotted that legacy output as a same-analysis baseline, restarted
the server on the committed code, reset the job to `step=spine` and **resumed** — the checkpoint/resume design paid for
itself. On the resume the first tables answer arrived as a JSON *string* with raw newlines in long cells; strict parsing
refused it and the per-exhibit re-ask (a 107K-token cache read, $0.09) rescued all three tables; I cancelled before
figures to fix the parser (`json.loads(strict=False)` first), restarted once more and resumed from `figures`.

**Cost / time of the new passes (the resume):** 12 calls, **$1.76**, ≈ 10.5 min — spine $0.17 (2.0 min) · tables $0.56
($0.47 + $0.09 re-ask on the cache; 2.9 min) · figure specs $0.11 + 2 renders $0.27 + 2 checks $0.02 (1.7 min) · draft
body $0.50 + frames $0.03 + frames re-ask $0.02 (2.9 min) · cross-check $0.08 (1.0 min). The design's estimate was
"≈ +$1.0, +5 min" on top of the old pipeline's tables/figures/compose; measured against the same-analysis legacy pass
($1.30 for tables+figures+compose) the concretization passes cost **+$0.46 and +4.6 min**. Whole job as recorded:
$5.46 / 29.0 min / 23 LLM + 4 image calls — of which $3.70 is the first (legacy) pass and the two restarts are mine.
Baseline `live-dossier-be00c33e5180`: $2.22 / 27.4 min (its brief waited 15 min for a hand).

**Before → after, the same analysis prose (legacy compose vs the passes):**

| | legacy pass (same run, before the resume) | concretization passes |
|---|---|---|
| where exhibits sit | all 4 at SECTION END (§1 fig, §2 table+fig, §3 table) | all 5 at their pointer, mid-paragraph, prose continues after each |
| section claims | none (sections re-derived from prose) | 5, one sentence each, in the spine's order; every table has `proves` |
| tables | 2 (12 rows) | 3 (10 rows, 0 dropped), each commissioned by a claim; a 4th spec dropped by code as over budget |
| figures | 2, ok | 2, ok (16/16 and 5/5 labels legible), each for a named section, captions carry no digits |
| anchors | 12/12 | 16/16 verbatim, 0 fragments (the draft wall's fragment rule never had to fire) |
| summary vs close | 0.00 overlap | 0.00 overlap; jobs declared and met ("the finding and the stakes" / "the decision rule and the go/no-go question") |
| findings | 0 (clamps only, no spine) | 2 open from the judge, 3 dropped by the quote wall, 0 clamps |

**Tokens at the pointer (dossier.md of the resumed job):**
- §2: *"Table 1 maps those dependencies for each of our three principal pledges."* → **Table 1** → *"Reading across
  each row, the pattern is the same: the public commitment sounds self-contained, but the unstated premise and the
  supply-chain requirement it relies on are …"* — the prose argues from the rows it just showed.
- §2: *"Figure 1 shows this relationship as a closed loop."* → **Figure 1** (linear_flowchart, 5/5 labels) → *"The
  return arrow in the diagram is the problem no rewording can close: the fund's growth requires the problem's growth."*
- §3: *"Figure 2 places our sustainability claims on two axes: how material or structural the claim is, and how
  severe the challenge it will face."* → **Figure 2** → *"The upper-right quadrant — high challenge severity, material
  and structural claims — is where our supply-chain commitments sit."*
- §4: *"Table 2 maps each commitment against the two legitimacy criteria and records which exposure trigger …"* →
  **Table 2** → *"The circularity fund was announced in July 2024, directly following IPO approval delays …"*
- §5: *"Table 3 states those questions as pass/fail tests, with the remediation required when a claim fails."* →
  **Table 3** → *"The tests are not interchangeable."*

**Captions matching claims.** Figure 1's spine claim: *"… the circularity pledge contains a structural
self-contradiction: the fund is financed by the same mechanism that generates the waste it claims to address"*;
its caption: *"The return arrow shows where the circularity commitment funds itself through the same activity it claims
to reduce"*; the check's `detected`: *"a vertical cascade flowchart with downward arrows and a feedback loop arrow;
5/5 labels legible: €200M Circularity Fund, Unstated Premise, Supply-Chain Requirement …"*. No digit in either caption
(the baseline's `ten_r_neoliberal_counter` table caption carried one).

**Summary ≠ conclusion.** Summary opens *"Our three principal sustainability commitments — the circularity fund, the
responsible sourcing mandate, and the evoluSHEIN roadmap — engage almost exclusively with the two least demanding
elements of the 10-R framework …"*; the close opens *"Before any new sustainability claim is published, ask three
questions in sequence. First: does the claim address an R-element above Recycle …"*. The frames wall refused the first
frames for a number the body does not carry ("600,000"); the re-ask removed it ($0.018, cache read).

**The cross-check (2 pictures shown as vision input).** Judge summary: *"The dossier is structurally sound and
well-anchored — every major claim traces to a named source, the three-test decision rule is consistent across sections
1–5 and the close, and both tables do the work the spine assigned them."* Two findings kept: a *Workers' Rights Pledge*
point placed in the quadrant's Greenwashing-Risk corner with no sentence in §3 naming it (judge typed it
`table_unreferenced` with cure `rerender_figure` — a kind/affordance mismatch the walls do not yet clamp, so nothing
executed; zero-change gate recorded), and an `anchor_off_claim` in §4 (a Highfield & Miltner platform quote under a
brand-legitimacy sentence; cure `reanchor_claim`). Three judge findings were dropped by the quote-on-page wall: two
quoted diagram labels ("evoluSHEIN Roadmap ●") that the page text did not include — **fixed** in this branch (figure
labels are on the page; marker glyphs stripped) — and one whose quote diverged from the close's wording after its first
70 characters. `hangs_together: false` with two open items is the honest verdict; at medium depth nothing was safe to
execute automatically (no caption digit, no unplaced exhibit, no failed picture check).

**What the run says about the design.** The spine → exhibits → draft chain held without a single patch round on the
draft: five sections, every exhibit placed once where the writer names it, sixteen anchors verbatim. The walls that
fired were the frames' number wall (a real invention caught), the tables' per-exhibit re-ask (a shape failure, now
parsed leniently), and the verdict's quote wall (which was too strict about pictures and is now right). The two open
findings are exactly the Phase 2 work: a section rewrite that names the point the picture already shows, and a
re-anchor — the work order (§C.5) is the next thing to build.

## Deviations from the design, and why

- Tables and figures stay separate steps (the brief's "new step between analysis and tables"); §D's `exhibits` fold is
  not done. Compose = draft + render in one step; cross-check is its own step after it.
- The composition read is the first half of the spine call, not a separate call (one call, the read fields come first
  in the tool schema — the model declares the read before it commits the spine; ≈ $0.15 instead of two calls).
- Exhibit numbers are fixed BEFORE the draft (spine-section order) and the renderer numbers by the same rule, so the
  writer can say "Table 2" and be right; the design's "the desk numbers the exhibits for you" is kept but made
  deterministic.
- A forgotten exhibit is not refused after the patch: code places its token in the spine section that commissioned it
  and mints `exhibit_unpointed` (the design's "refused, not dumped into the last section" — the spine tells us where it
  belongs, so dumping is no longer the alternative).
- A trimmed anchor is an error at the draft wall (the writer gets one chance to copy the sentence), then unfootnoted
  and a finding — as §C.4's anchor law; the legacy path keeps footnoting trimmed anchors as before.
- `redirect_spine`, the findings/recheck routes and every desk action (§C.7) are Phase 4: not built (routes are
  outside this branch's paths).

## CHANGELOG entries (fold into docs/CHANGELOG.md [Unreleased])

### Added
- Concretization passes for the dossier (DESIGN_concretization_passes §C, Phase 0-1): the spine
  ([src/dossier/spine.py](../../src/dossier/spine.py)), spine-driven tables and figure specs
  ([src/dossier/tables.py](../../src/dossier/tables.py), [src/dossier/figures.py](../../src/dossier/figures.py)), the
  draft written with the exhibits in hand with placement tokens and frames last
  ([src/dossier/compose.py](../../src/dossier/compose.py)), the cross-check judge with code clamps, the findings ledger
  and one round of safe realizations ([src/dossier/crosscheck.py](../../src/dossier/crosscheck.py),
  [src/dossier/findings.py](../../src/dossier/findings.py)).
- Schemas: `DossierSpine`, `SpineSection`, `SpineTableSpec`, `SpineFigureSpec`, `CompositionRead`, `Finding`, `Fate`,
  `CrossCheckVerdict`; exhibit fields `section_key`, `proves`, `picture_shows`, `caption_says`, `detected`, `checked_ok`,
  `exhibit_refs` ([src/dossier/schemas.py](../../src/dossier/schemas.py)); store columns `spine_json`, `findings_json`,
  `crosscheck_json` ([src/dossier/store.py](../../src/dossier/store.py)).
- Walls arithmetic: `has_digit_run`, `sentence_count`, `shingle_overlap`, `exhibit_tokens`, `numbers_not_in`
  ([src/dossier/walls.py](../../src/dossier/walls.py)).
- LLM calls: opt-in prompt caching with an uncached tail, image blocks, cache-aware receipts
  ([src/dossier/llm.py](../../src/dossier/llm.py)).
- Desk: `SpineView` / `FindingsView` ([web/src/components/SpineView.tsx](../../web/src/components/SpineView.tsx)); rail
  steps and `STEP_TO_RAIL` ([web/src/lib/run.ts](../../web/src/lib/run.ts)); mock fixtures
  ([web/src/lib/mock_concretize.ts](../../web/src/lib/mock_concretize.ts)).
- Tests: `tests/test_spine_walls.py`, `tests/test_exhibits_from_spine.py`, `tests/test_compose_tokens.py`,
  `tests/test_crosscheck_clamps.py`.

### Changed
- `STEPS` / statuses gain `spine` and `crosscheck`; `runner.py` runs them; workflow definition v2 with ten phases
  ([src/workflows/definitions/dossier_standard.json](../../src/workflows/definitions/dossier_standard.json)).
- The composed HTML/Markdown places tables and figures at their tokens (blocks), numbers them in the spine's order,
  never places a failed figure, and appends the spine and the findings ledger to "How this was made"
  ([src/dossier/templates/dossier.html.j2](../../src/dossier/templates/dossier.html.j2)).
- `render_figure` accepts optional `revision_notes` (the cross-check's words on a redraw).
- Web labels for the new statuses and for the backend's step names ([web/src/lib/format.ts](../../web/src/lib/format.ts)).

## FEATURES entries (fold into docs/FEATURES.md)

### Dossier Spine (pass S)
- **Status**: Active
- **Description**: Composition read + the argument's spine before any exhibit exists: one claim per section, the table
  and diagram each claim needs, planned anchors, distinct jobs for summary and close; walls with field patches.
- **Entry Points**: `src/dossier/spine.py:1-40` (doctrine) · `:44-131` schema · `:133-176` system prompt ·
  `:181-233` inputs · `:238-292` `coerce_spine` · `:295-373` `validate_spine` · `:376-424` `_repair_by_code` ·
  `:440-479` `build_spine` · `:487-505` `run_spine`
- **Added**: 2026-09-03

### Exhibits from the Spine (pass E)
- **Status**: Active
- **Entry Points**: `src/dossier/tables.py:143-256` (`spine_tables_schema`, `_admit`, `run_spine_tables`, `run_tables`) ·
  `src/dossier/figures.py:349-510` (`SPINE_SYSTEM`, `spec_figures_schema`, `validate_spine_spec`, `spec_figures`,
  `detected_sentence`, `enrich_from_spine`, `finding_for_figure`) · `src/dossier/findings.py`
- **Added**: 2026-09-03

### Draft with the Exhibits in Hand (pass D)
- **Status**: Active
- **Entry Points**: `src/dossier/compose.py:160-198` (`DRAFT_SYSTEM`, `FRAMES_SYSTEM`) · `:236-256` `exhibit_numbers` /
  `expected_exhibits` · `:346-401` `validate_body` · `:414-472` `_repair_body_by_code` · `:475-514` `write_body` ·
  `:519-575` frames · `:578-611` `compose_draft` · `:616-720` `_render_context` (blocks)
- **Added**: 2026-09-03

### Cross-check and Findings Ledger (pass X)
- **Status**: Active
- **Entry Points**: `src/dossier/crosscheck.py:78-129` (system prompt) · `:134-160` `page_text` / `quote_on_page` (figure labels count as on the page) ·
  `:238-290` `clamp_findings` · `:300-352` `validate_verdict` · `:369-382` `apply_fates` · `:392-465` `realize` ·
  `:482-540` `run_crosscheck` · `web/src/components/SpineView.tsx` (desk)
- **Added**: 2026-09-03
