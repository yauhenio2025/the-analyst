# Study: de-llm's long-form structural program — the restructuring process, for The Analyst's dossier composition

> Written 2026-09-03 for the dossier-composition design memo. Read from
> `/home/evgeny/projects/de-llm` at commit `15b3cf3` (2026-09-03): `CLAUDE.md`,
> `communications/LONG_FORM_RESTRUCTURING_MEMO_2026-08-30.md` (the design memo, 1,035 lines),
> `communications/engineering/LONGFORM_BUILD_RETROSPECTIVE_2026-09-02.md`,
> `communications/audit-2026-09-02-creativity/{SYNTHESIS,D-bold-counterproposals}.md`,
> `communications/LONGFORM_OWNER_BRIEF_2026-09-02.md`,
> `communications/NARRATIVE_STANCE_DIMENSIONS_2026-09-03.md`, `communications/IMPLEMENTATION_TRACKER.md`,
> `docs/FEATURES.md` §"Long-form structural program", `docs/CHANGELOG.md`, and every module of
> `delm/longform/` (`prompts.py`, `program.py`, `realize.py`, `audit.py`, `integrity.py`, `resolve.py`,
> `orchestrator.py`, `memo.py`, `stance.py`, `tree.py`, `model.py`) plus `web/longform.{html,js}`. Nothing
> in de-llm was edited. Line numbers below are from that commit.
>
> Counterpart read in this repo: `src/dossier/{compose,plan,brief,tables,figures,analysis,runner,llm,schemas,common,walls}.py`.

---

## A. What de-llm is, and what "long form" produces

**de-llm** is Evgeny's editing studio for prose that LLMs touched: it harvests and curates "tells" of
LLM-written text and — the larger part by now — runs *structural editing programs* over an author's
draft, grounded in twelve craft books distilled into rule packs (`structural-lenses` 54 rules,
`operations-foundations` 21, `document-foundations` 27, `narrative-foundations` 42; ids like
`SHAPE_BRAIDED_STRANDS`, `OP_COMPRESS`, `DOC_RETITLE_AFTER_ARCHITECTURE_STABILIZES`,
`NAR_EMPLOT_AS_DETECTION` — `data/rule_packs/`). The essay-scale program (`delm/structural_program.py`,
unit = paragraph, ≤48 paragraphs) came first; the **long-form program** (`delm/longform/`, 30 Aug – 3 Sep
2026, ~13,000 lines, 19 stages) is "the essay-scale loop one level up: the unit is the heading-bounded
section" (`delm/longform/__init__.py:1-8`), designed for 150-page reports and verified on a 10,000-word
journal article and a 36,000-word manuscript. Its doctrine is "LLM-first": "code in this package owns
shape, sequence, arithmetic and lifecycle recording only; every judgment is a model call" (`__init__.py:7-8`;
design memo §10 `LONG_FORM_RESTRUCTURING_MEMO_2026-08-30.md:999-1017`).

**Inputs → outputs.** In: one document (Markdown, DOCX, PDF best-effort, or a headingless capture the
"section finder" partitions), an *aim* ("what should the restructured document do for its readers?"), an
*ambition* (tidy · rebuild · open), constraints ("must not be lost"), optional reading notes, an audience,
and an optional *narrative stance* (sixteen dimensions of how the argument is told). Out, in order:
(1) **memo 1 — choose**: a letter plus one card per candidate architecture (3–5, "different by strategy",
at least two re-foundings, one always "rebuilt from the cards"), with three *trial leads* and the model's
comparative recommendation; (2) **memo 2 — approve**: the section-by-section realization plan the author
signs (every removal, compression and rebuild decided explicitly, each new unit accepted or declined,
each query answered or deferred); (3) the **rewritten document** (MD/DOCX/PDF) generated one section per
call in the *new* reading order with a live seam and a thread ledger, then frames written last, then
retitled, mechanically reassembled (floats renumbered by first mention, cross-references rewritten,
contents regenerated), audited by seven diagnosis-only judges, repaired in bounded rounds; (4) a
**closing memo** opening with "What changed in your article" (numbers, outline before/after, every changed
passage old beside new) and the checker's remaining doubts; (5) a **resolution gate** where the author
settles each open doubt (keep the rewrite / restore the source / own wording / go further) and the
document is re-made. Every stage checkpoints to a run directory and resumes without re-buying
(`orchestrator.py:4-6`, `:64`).

---

## B. The pass ledger

Stage order is code-enforced: `STAGES = ("ingest", "read", "deep_read", "cards", "style_sheet",
"architecture", "memo1", "choice", "plan", "memo2", "approval", "generate", "units", "retitle",
"assemble", "screens", "audit", "repair", "finalize")` (`orchestrator.py:64`), grouped in the UI as
Reading · Architecture · Your gates · Writing · Checks · Finish (`web/longform.js:13-20`). Every model
call shares a **cached prefix** = the whole source document + a one-line-per-section index
(`program.py:163-173`, `prompts.py:18-21`), with `cache_control` ttl 1h (`model.py:292`). Every model
answer is strict JSON validated for *shape only*; "on a shape failure the model gets one corrective re-ask
with the exact failures, then the stage surfaces" (`program.py:3-7`, `:497-535`; `prompts.py:615-620`).
Prose bounds **heal**, structure **fails**: "A prose field that runs past its guide is KEPT WHOLE and
noted: cutting a model's sentence in the middle edits its argument for the author" (`program.py:370-386`).

### B.0 · ingest → tree (0 calls)
- **Reads** the file. **Writes** `source.md`, `tree.json`: byte-exact blocks, a heading tree, unit sections
  chosen at the heading level whose count is log-closest to ~60 (`tree.py:619-641`), section *kinds*
  (contents · executive_summary · abstract · policy_box · back_matter · front_matter · references · annex ·
  introduction · conclusion · body; `tree.py:649-660`), apparatus nodes (tables, figures, footnotes) that
  no stage rewrites, references-out, signposts, a pre-flight manifest (floats by first mention, unresolved
  references, head logic, "not final" signals).
- **Move:** none — but it fixes the unit of restructuring and marks what is *not prose*.
- **Judge:** a mechanical boundary screen (mid-sentence section seams) and, for flat captures, the
  SECTION FINDER call: "Recover the document's OWN structure; do not invent a better one — that is a later
  stage's job, and it belongs to the author" (`prompts.py:983-985`).

### B.1 · read — the whole before the parts (1 call, thinking on)
- **Reads** the cached document + settings. **Writes** `read.json`.
- **Move:** *plain summary first, then what the structure buries.* "PLAIN SUMMARY FIRST (Lanham): in at
  most four sentences, what a competent outsider would accept as what this document says … Then BURIED OR
  UNSTATED: what the document's structure buries, delays, or never states plainly — the thing its readers
  actually need to decide or are afraid of — with where it currently hides" (`prompts.py:37-42`).
  Then "WHO READS IT AND HOW … whether each reads straight through or consults section by section"
  (`:43-46`); the governing contract (one point, question answered, who speaks, register, scope; `:47-48`);
  "THE READER JOURNEY AS IT ACTUALLY RUNS … including where the order is the order the research was done
  in, or a funder's template" (`:49-51`); strongest asset / costliest choice quoting the author (`:52-53`);
  STRANDS "INCLUDING accidental recurrences the author may not have noticed (Gardner …) Mark accidental
  ones" (`:54-57`); form capacity (`:58-60`); provenance (`:61-64`); an APPARATUS census and GAPS — "a
  table doing in prose what a table should do" (`:65-67`); the current shape named and honestly assessed
  (`:68-69`); the home GENRE, which "sets the defaults of how the argument is told" (`:70-76`).
- **Judge:** none; this read "is the *frame* every later call inherits" (design memo `:248`).

### B.2 · deep_read — what the document runs on (1 call)
- **Reads** the read + a "DEEP STRUCTURE GUIDE (distilled from 28 enduring nonfiction books)"
  (`program.py:711`). **Writes** `deep_read.json`.
- **Move:** declares twelve elements (master dichotomy, causal mechanism, master metaphor, taxonomy,
  temporal framework, ontology, scale-shifting, agency, emplotment, affective arc, myth demolished,
  prescription; `delm/deep_structure.py:36-49`) each "stated / implicit / absent" with quotes, five tests,
  where the structure is THIN, and — the generative part — what is **LATENT**: "elements the material
  would support that the document never states — a mechanism implicit in its cases, a dichotomy the cases
  share, a parable case that contains the whole argument … The latent list is the raw material of
  re-founding" (`prompts.py:132-137`).

### B.3 · cards — one card per section, in parallel (N calls, thinking off)
- **Reads** the read digest + ONE section's full text with its neighbours and mechanical signals.
  **Writes** `cards.json` incrementally (resume-safe; `orchestrator.py:496-507`).
- **Move:** turns every section into a movable card — "McPhee's index card, Williams' point outline,
  Stein's triage map" (`prompts.py:165-166`): `actual_job` "what the section actually does for the reader
  (not what its heading promises)"; `point` "quoted verbatim if one exists, else 'buried at paragraph N'
  or 'absent'"; `frame_verdict` "whether the point leads, lands late, or is absent" (`:172-175`); `cast`;
  `claims` (≤5); `evidence`; `terms_introduced`; `references_out`; `depends_on` / `prepares_for`;
  `mobility` "'anchored' if chronology, causation, or dependency fixes its position, else 'mobile'";
  `path_function` "'body' … 'front_frame' if orientation, 'annex' if deepening but distracting (Einsohn's
  test; an annex deepens, it is never leftovers)" (`:184-187`); `strands`; `proportion_note` "its space
  against its consequence — crowded, leaped, right"; `owes_the_reader` "what the reader wants next when
  this section ends, and whether its ending throws forward" (`:190-192`); `sibling_kind` "so comparable
  siblings can be recognized" (`:193-194`).

### B.4 · style_sheet (1 call)
- **Writes** `style_sheet.json`: terminology variants and the preferred form, capitalization, numbers and
  units, abbreviations with where first expanded, headings/citations/captions style, spelling variety,
  voice, "notes on anything a rewriter must not change" (`prompts.py:229-264`). Travels in the cached
  prefix of every generation call; deviations are counted, never enforced (`integrity.py:325-336`).

### B.5 · architecture — imagine, in four kinds of call (≈ 1 + 1 + 3–6 + 1 calls)
All receive the **lens material** — "the books, not the taxonomy: principle, rationale, preserve,
sources and one worked example travel with every rule" (`program.py:187-211`, `:214-234`) — under a
shared doctrine (`prompts.py:270-336`):

> "Your job is to show the authors what their document is doing and what it could do instead. You are not
> auditing for defects and not asked whether change is warranted … Moving one or two sections, or adding
> a bridge, is a REPAIR, not an architecture; the authors have cheaper tools for repairs. The document's
> MATERIAL is your limit, never its current arrangement: treat the draft as raw material that could be
> rebuilt from the ground up" (`:271-279`).

> "a report's current order is usually the order the research was done in, or the funder's template —
> neither is an architecture … Chronology wins by default; the re-founding signal is themes that 'cry out
> to be collected' against it (McPhee). If the current axis is chronological or narrative, imagine the
> coordinate or logical one and price what changes … Do NOT over-tidy — a long work built as prettily as a
> teacup is not of much use (Gardner): perfectly parallel sections are a smell, not a virtue. A candidate
> is SETTLED when its charged adjacency has been found and the remaining units assemble around it without
> forcing (McPhee) — name that adjacency" (`:281-293`).

> "'radical' is a re-founding — a reader would recognize the result as a different document … 'moderate'
> is a genuine strategy change that keeps most of the current material where it stands. Declare depth
> honestly; beside your label the server reports what actually changes" (`:295-302`).

> "Preserve nothing about the current order, length, or wording for its own sake; preserve the authors'
> claims, facts, qualifications, chronology, citations, data, and stance in every architecture you
> propose … Do not write replacement prose, headings, or transitions here — the trial leads in the payload
> are the only prose this stage drafts" (`:331-336`).

- **B.5a diagnosis** (1 call, `prompts.py:338-426`; validated `program.py:940-987`). Re-diagnoses the
  current shape, then "choose three to five STRATEGY FAMILIES this material genuinely supports — different
  BY STRATEGY, not by degree" from thirteen: emphasis_order · governing_axis · container_or_frame ·
  carrier · proportion ("the same claims in 50–70 % of the space") · rebuild_from_cards ("throw the
  current order away: deal the section cards on the table, anchor what chronology or dependency fixes,
  and build the strongest architecture the material supports whatever the present sequence") ·
  scene_and_summary · borrowed_form ("a case file, a decision memo, a trial, a field guide") ·
  re_found_on_mechanism · re_found_on_metaphor · retime · demolish_then_build · emplot (`:356-387`).
  Hard rules: "At least two families must be radical, one family must be rebuild_from_cards (it exists so
  the authors always see what the material would become with no allegiance to the present order), and at
  least one family must re-found the deep structure … when the deep read found a latent element … No two
  families may share a primary strategy or an opening section. Each family must either repair the weakness
  named in honest_assessment or protect the asset named there" (`:392-400`). Code fails the answer
  otherwise: "a set of timid variations is not an answer" (`program.py:977-982`).
- **B.5b trial leads** (1 call, `prompts.py:428-446`): "McPhee's instrument: when the structure will not
  come, write the lead, because a lead that is true to the material commits the whole to a shape. … Write
  one lead for each of three DIFFERENT families … 120–220 words, in the authors' register, built ONLY from
  the document's own material … Say in commits_the_whole_to what following it would oblige the rest of the
  document to do." An instrument, never a gate: a failed leads call is dropped and candidates proceed
  (`program.py:1303-1304`).
- **B.5c candidates** (one call per family, in parallel, `prompts.py:448-558`; validated
  `program.py:1068-1198`). Each builds a complete architecture: `thesis_of_change` "doing three things —
  the different journey the reader lives; at least one concrete visible consequence naming sections by
  heading and position …; and a final sentence beginning 'Choose this if …'" (`:459-463`);
  `settled_adjacency`; `adopted_trial_lead`; `deep_structure` "what the document would RUN ON under this
  shape … A shape whose every element is 'kept' is a rearrangement — say so honestly" (`:466-471`); a
  `stance` over the ten dimensions a shape decides (`:473-490`); `stage_skeleton` "3–14 stages, each with
  a label, its reader-facing job, and existing_section_ids in intended reading order. EVERY unit section
  id … must appear in exactly one stage — none missing, none repeated; a stage may consume sections by
  merging, rebuilding or retiring them … and marks where new material is needed … describe its job and its
  material, do not draft it" (`:491-497`; coverage check `program.py:1137-1142`); `path_plan`
  (front_frame / annex / retired), `apparatus_plan` ("the executive summary's role (a self-contained
  decision document, written last)"), `strand_schedule` ("each return larger than the last, timed before
  the set piece"), `sibling_groups` ("parallel sections that should answer one shared question"),
  `operations_sketch` (honest counts incl. rebuilds, compressions, inserts), `author_cost` with
  `reader_gain` and "the political trade-off (Lanham: a clear architecture can expose that a
  recommendation is contentious or that a part says little — name it)" (`:504-517`). Genre placement:
  "the ABSTRACT states the finding and stays first; acknowledgements, funding, endnotes and references stay
  last. Everything else is material" (`:532-536`). Code then computes per candidate `order_disruption` /
  `displaced` (share of section transitions that change; `program.py:1201-1221`) and a `change_profile`
  sentence — "opens on … · moves N of M sections · changes what it runs on · rebuilds · merges ·
  compresses · writes N new · cuts · annexes" — "A description, never a score" (`program.py:282-343`).
- **B.5d rank** (1 call, `prompts.py:560-613`). "Rank every candidate by what the READER gains toward the
  stated aim under the authors' declared ambition. Never rank by least work, and never treat displacement
  or the amount of rewriting as a cost — the authors asked for a restructuring; how much changes is what
  they will weigh" (`:574-577`). Consulting readers are "a design requirement the candidate meets or
  fails, not a reason a bold shape loses" (`:580-586`). "recommendation_reasoning is comparative, written
  for the authors, not a defense of the winner: name each rival and, in one or two sentences each, what it
  does better than the winner and why that still loses" (`:588-592`). Ranks must be a permutation and the
  recommended must be rank 1 (`program.py:1384-1415`).

### B.6 · memo1 → choice (1 call + author)
- `write_memo_letter(kind="choice")` writes a letter and one card per option over a mechanical record
  (`memo.py:359`, `orchestrator.py:543-567`); `render_memo_v1` composes "The options on one screen" with
  the change-profile sentence, "It would run on", "Stance", journey / what moves / written new / what it
  costs you / choose this if / craft sources, and the adopted trial lead ("It could open like this")
  (`memo.py:618-690`). Vocabulary rule for every memo: "no section ids, no hashes, no rule ids, no
  'disposition', 'retain', 'reframe', 'drift', 'adjudication', 'seam' … Say 'unchanged', 'first and last
  lines rewritten', 'rewritten', 'rebuilt', 'moved', 'cut', 'written new'" (`prompts.py:1039-1045`).
- **Gate:** the author chooses (or a policy: `recommended`, or `boldest` = "the candidate whose described
  change is largest — moves, rebuilds, merges, compressions, new material, cuts — not the one that merely
  re-routes the most seams", `realize.py:99-112`). The choice carries the candidate's stance forward.

### B.7 · plan — realize the chosen architecture section by section (1 call, thinking on, up to 3 attempts)
- **Reads** cached document + style sheet + OPERATIONS MATERIAL (the 21 `OP_*` rules and, when present,
  the narrative pack), plus the read, cards, chosen architecture, trial leads, deep read, stance
  (`realize.py:589-608`). **Writes** `plan.json`.
- **Move:** one directive per section with a **disposition** from twelve — "retain (byte-preserved) ·
  move_only · reframe (its opening and closing paragraphs change for the new place; the middle stays …
  unless the brief names a change inside it) · rewrite · compress (rewritten to a length_target_words BELOW
  three quarters of its present length — every claim, citation and qualification survives in less space;
  the authors sign every compression) · rebuild (this section is rebuilt into a NEW argument from its own
  material plus the sections that merge_into it — a re-founding of a group, not an edit) · restructure
  (its internal paragraph order is rebuilt by the paragraph-level program) · merge_into · split · cut (a
  removal the authors sign explicitly — never by default) · to_annex · to_front" (`prompts.py:647-664`).
  "A section relocated into position 1, the final position, or the opening or closing of a stage from
  elsewhere changes role: it may NOT carry retain or move_only" (`:665-666`; enforced
  `realize.py:352-359`). "A stage whose reader-facing job promises a verdict stated once, a case told as a
  scene, a synthesis, a cut to proportion, or a new opening needs a directive or a new unit that BUILDS
  it — rewrite, compress, rebuild, or a new unit — never a retain with a new heading" (`:667-670`).
  Per directive: `brief` "complete, because the writer receives it whole"; `new_role` "its FRAME
  requirement (the point sentence and the themes it forecasts — Williams) and its EXIT requirement (the
  ending throws forward to what follows — Stein's chapter contract)" (`:671-676`); `builds_element`
  (`:676-681`); `length_target_words`, `must_seed` / `must_pay_off`, `first_mentions_moving`,
  `refs_to_reanchor`, `preserves` (`:682-686`).
  **Register control:** "ENACTED, NOT ANNOUNCED: a brief asks for transitions that perform the move (the
  seam grows from the previous closing; the case is told as a case), never for sentences that announce it
  ('name this as Test Two', 'state that the law is confirmed a third time') — unless the genre expects
  signposts (a report, a manual, a brief). Stage labels are the plan's vocabulary, not the reader's"
  (`:697-701`).
  **New units** in two families: "BODY units, written IN READING ORDER during generation with the live
  seam and the thread ledger … lead … verdict_page (the finding and its limits stated once, plainly) …
  body_section (a synthesis, a comparison, a counter-case, a scene built from the cards …). FRAME units,
  written AFTER the body exists: executive_summary (states what the body now argues, written last),
  part_introduction, bridge, apparatus (a glossary, a list of abbreviations, a table the material needs)"
  — each with `distinct_job` "the reader's job that NO existing section already does. Never a table that
  restates an existing table" (`:730-747`).
  `job_carriers`: "for EVERY stage, name what DELIVERS its reader-facing job … A carrier section's
  disposition must be able to alter content … retain and move_only cannot build a promise. Declare 'as_is'
  ONLY when the existing text already performs the job unchanged … A stage job that names relocated or
  front-loaded content with no carrier is the defect this field exists to prevent" (`:756-763`; validated
  `realize.py:420-459`). Also `sibling_contracts` (Zinsser's one question), bounded `author_queries` with
  strict `if_unanswered` semantics (`:765-780`), `parking_lot` ("doubtful changes you declined to make,
  noted for the authors (Stein)"), `cut_negotiation` ("McPhee's two directions — restore into the new
  skeleton, or trim from the full"), `retitle_intent` (`:781-785`).
- **Judge (code, pure comparison):** every section placed once or explicitly removed; target order is a
  permutation of survivors; stages contiguous; stage labels echo the candidate's; **skeleton deviations
  declared == computed** ("placement:<id>", "stage_count"; `realize.py:175-192`, `:360-380`); **depth
  codes** — "a code depth:<kind> for every kind of operation the chosen option's operations sketch counted
  more of than the plan realizes … the codes make that shortfall a declared, explained departure the
  authors read in memo 2" (`realize.py:155-172`; prompt `:720-728`: "a shortfall without a reason the
  authors would accept is a failed plan, not a cautious one"); a rewrite target under 75 % is *renamed* a
  compression rather than raised to a floor (`realize.py:195-218`); the abstract may only be reframed and
  must stay before the body (`:274-300`).

### B.8 · memo2 → approval (1 call + author)
- The approval letter says "what will happen to the document in reading order … and what the authors must
  decide (each removal, each new unit, each question)" (`prompts.py:1068-1072`). The UI lists "Removals —
  each needs your decision", "Compressions and rebuilds — approving the plan signs these", "New sections
  the plan would write", "Questions for you", "Order of the surviving sections" (`web/longform.html:186-201`).
- **Gate:** `normalize_approval` refuses an approval with any undecided removal (`realize.py:705-716`);
  `default_approval` for headless runs *requires* an explicit adopt/reject policy ("signed removals are
  never decided by a default in either direction", `:668-676`); a deferred query returns its sections to
  their original wording AND place (`:771-788`). `effective_program` is the program generation executes.

### B.9 · generate — sections in the new reading order (≈ 1 call per changed section, thinking off)
- **Reads** cached document + style sheet + APPROVED PLAN (thesis, deep structure, stage jobs, target
  order, all directives, new units, sibling contracts, stance); per call the directive, source text,
  absorbed sections, the **live seam** ("the closing paragraphs of the section the reader has just
  finished in the NEW order, already rewritten"), what follows next with its new role, the **thread
  ledger**, constraints, answered queries, a `max_chars` cap (`realize.py:1007-1022`, `:1119-1135`).
  **Writes** one artifact per section under `sections/` (checkpoint), `generation.json`.
- **Move (prompt `prompts.py:823-907`):** "Do exactly the directive's disposition, at the ambition the
  approved plan set — the authors chose this architecture; a timid execution that leaves the section as it
  was fails the directive as surely as an invention does" (`:836-838`); compress: "McPhee's greening: meet
  the quota from the middle, not the end" (`:840-842`); rebuild: "a re-founding, not a stitching"
  (`:842-843`); "Preserve every claim, fact, number, date, name, quotation, citation mark, table, figure,
  footnote reference and qualification … Tables and figures are reproduced verbatim where the section
  carries them; you may move a reference to one, never its content … Restating, relocating or condensing
  a claim the plan ordered is not a loss; inventing one is" (`:853-858`); "Honor the FRAME requirement …
  and the EXIT requirement … honor must_seed and must_pay_off; re-introduce a term or figure the ledger
  shows as anchored far back (readers do not 'still remember what was once explained'); repair the seam so
  this opening grows from the previous closing; reanchor the references … refer to sections by their
  headings, never 'above/below', never a number that may change" (`:865-870`); the stance block incl.
  "Where steering is 'continuous': ENACT, NEVER ANNOUNCE — the document must not narrate its own
  structure … a label the plan uses internally (Stage, Test, Case) never enters the prose … The mechanism
  is stated once, where the plan places it; everywhere else it is used, not restated" (`:873-889`); "If
  the brief cannot be honored without invention, do what can be done and put the rest in queries"
  (`:890-891`). The answer returns the body plus a `ledger_delta` (terms introduced, promises opened /
  paid, floats referenced, cross-references emitted), a `preserved` inventory, `queries`, `notes`
  (`:898-907`).
- The **ThreadLedger** is "model-declared entries, code-kept positions and distances": every call sees
  `terms_anchored` with `words_since_anchor`, `promises_open` with `words_since`, floats referenced,
  the last eight headings done (`realize.py:909-949`); the seam is the previous section's last two
  paragraphs, ≤1,500 chars (`:952-958`). Body units (lead, verdict page, body section) are written
  **inline at their anchor** in the same pass with the same seam and ledger (`:1032-1077`). A `restructure`
  runs the paragraph-scale program inside the section with a rewrite fallback disclosed as such
  (`:961-984`, `:1181-1187`). A declined or twice-malformed section never kills the run: the author's text
  stands, flagged as a blocking doubt (`:1143-1168`).
- **Judge (code):** a reframe whose middle changed is *kept and flagged* `reframe_exceeded` for the
  plan-aware adjudicator, never spliced back (`realize.py:875-893`); a rewrite under 75 % of source words
  is flagged `fidelity_check_required`, "a screen, not a failure" (`:863-868`); length overruns up to 1.5×
  are accepted with a note (`:869-874`).

### B.10 · units — the frames pass, executive summary last (≤ a few calls)
- Frame units are written **after** the body exists, each seeing the assembled document so far, sorted so
  the executive summary is last (`realize.py:1293-1337`, `:1310`). Prompt (`prompts.py:909-952`): "an
  executive summary states what the body now argues, in the body's proportions, with the body's
  qualifications, so a busy reader can decide without reading further (Einsohn); a part introduction is a
  short frame that states the part's point and forecasts its themes before the longer body (Williams); a
  bridge is the smallest seam the join truly needs"; "a lead opens the document on the material's most
  charged moment or its verdict … and commits the whole to the chosen shape"; "a verdict page states the
  finding AND its limits once, plainly … so a reader who stops there leaves with the honest whole".
  Mechanical hygiene inside the prompt: "Tables are GitHub pipe tables and EVERY row begins with a pipe
  character" (`:937-938`).

### B.11 · retitle (1 call)
- After the body stabilizes, one call proposes every heading (document, stage, section, unit):
  "each heading carries its section's key themes (Williams), siblings are balanced in length and parallel
  in grammar (Einsohn), the document title is not the subject's bare name, and nothing is renamed for its
  own sake: keep a heading that already does its job. A section or new unit never repeats the heading of
  the part that contains it … Headings carry the section's themes, never the plan's scaffold: no 'Test
  One:', 'Stage 2', 'Part I: The Law' prefixes unless the genre expects signposts" (`prompts.py:954-973`;
  validation `realize.py:1340-1373`). A second retitle pass is triggered by cold-reader *legibility*
  findings: "A cold reader could not recover the architecture from the headings and openings … Propose
  every requested heading so that the stage sequence and each section's question are visible from the
  headings alone" (`realize.py:1406`; `orchestrator.py:848-860`).

### B.12 · assemble + screens (0 calls)
- `assemble_with_integrity` (`integrity.py:72-276`): numbered stages and sections; a single-member stage
  collapses into one heading ("no lone children, no stacked heads", `:119-146`); cross-references rewritten
  through the old→new number map with unresolved ones listed (`:189-206`); "floats: renumber simple
  integer labels by order of first mention in the new text" (`:208-222`); **conservation** — "every source
  section is either a unit in the program …, absorbed into a merge, apparatus the assembly places …, or
  ABSENT — and absence is a named defect, never silent" (`:224-237`); the contents page regenerated only
  when the source had one or the program asked (`:242-251`); back matter byte-preserved at the end.
- `document_screens` (`:344-377`): the output's own tree signals, per-section content inventory
  (dropped / reworked / introduced sentences, facts missing / introduced), style deviations, whole-document
  inventory, boundary defects, residual boilerplate, proportion before/after with largest growth/shrink.
  "Nothing here judges a rewrite; the screens produce SIGNALS the audits and the closing memo show the
  author" (`:6-7`). `audit_copy` tags every heading with its id for the audits (`:380-402`).

### B.13 · audit — seven diagnosis-only judges over the clean copy (≈ 5 + N calls)
All read "the ASSEMBLED NEW DOCUMENT … It is a clean copy: the edit history is invisible … Diagnose;
never propose wording" (`audit.py:63-68`). Run in `orchestrator.py:744-817`; all findings merge into one
list (`:812`).
1. **Coherence audit** (`audit.py:70-139`, `:614-683`). Receives the chosen architecture's stage jobs,
   the read, mechanical screens, the document rules, and the **approved plan in digest** — "A change the
   plan ordered is the authors' decision, never a defect: judge whether it was done well for the reader,
   not whether it should have been done. A section compressed to its target is not 'proportion drift'; a
   verdict stated once where the plan put it is not 'repetition' when it is echoed as the plan said"
   (`:80-85`). Nine categories "EACH ACROSS EVERY PART (a sixty-section document is not audited by twelve
   findings)": argument_progression; seams_and_references ("every backward-pointing reference against what
   the reader has actually been given by that point in the NEW order"); chronology/attribution/citations/
   numbering/promises; repetition_and_proportion "including Pinker's cumulative direction: across a span of
   pages, which way does the verbiage push the reader's belief, and does that match the stated claim;
   counter-evidence quarantined in its own bounded section or bleeding through; proportion drift after
   cuts; duplicated jobs across sections"; voice_stance_and_qualification (the unity walk);
   opening_and_closing_contract ("the close pays the opening off without a recap-and-moral wrap-up");
   long_range_threads_and_payoffs ("readers do not remember what was explained forty pages earlier");
   executive_summary_and_frames; apparatus_and_navigation ("signposting as an order symptom (thickets mean
   reorder, not reword)") (`:87-111`). Each finding has severity, `repair_route` "repairable_in_place ·
   needs_new_material · needs_author" (`:118-121`), and judgment calls go to advisory observations
   (implied value distribution, credible counterpressure, retitle, form capacity, political trade-off).
   Max findings = 3 × stage count, ≥12, ≤60 (`:616`).
2. **Cold-reader skeleton reconstruction + compare** (`:141-182`, `:686-773`). Call A sees "ONLY the
   document's navigational surface — its title, contents, every heading … and the first and last
   paragraph of each section — never the bodies" and must "write the outline it implies …; state the
   document's claim …; pose the five or six questions such a reader would bring and say where you would
   go to find each answered — or that you could not tell". Call B compares with the intended
   architecture: "Where the reader's outline, claim, or answers diverge … that is a recoverability
   finding: the structure is not legible from the surface. Where the reader recovered the plan but
   noticed the diagram, that is an invisibility failure."
3. **Strand audit** (`:184-204`, `:776-808`): "For each strand, read its sections consecutively, as one
   piece, and report: drift …, dead returns (a return that repeats without developing), dosage (each
   return larger than the last, or cooling), and where it pays off. Then judge the opening-to-ending
   correlation: what the first tenth of the document invests in must matter at the close."
4. **Reanchor sweep** (`:206-220`, `:811-848`) over every *changed seam* with the thread ledger: "trace
   every pronoun, definite reference, compressed event label ('the collapse', 'the decision'),
   abbreviation, and 'as discussed above' back to an antecedent that precedes it in the NEW order; a true
   first mention must use introducing form."
5. **Drift adjudication** per rewritten section, in parallel (`:222-264`, `:877-968`) — "IN THE LIGHT OF
   THE APPROVED PLAN … material the approved directive ordered compressed, relocated, restated, reframed,
   merged or rebuilt is NOT a loss — rule it 'planned' … Rule on every flag — real_loss · planned ·
   benign_relocation (the content lives elsewhere in the new document; say where) · faithful_rework ·
   noise … isolate the SMALLEST unsupported assertion (a count, a date, a causal link), never a whole
   sentence that is otherwise supported … A sentence that condenses claims the source makes in several
   hedged places is a synthesized_claim, not an invented_fact — the author verifies the synthesis; reserve
   invented_fact for content with no source support at all". "YOU declare the weight of every item,
   because you read both texts" — severity, route, and whether the section BLOCKS adoption (`:249-254`).
   Code adds a **relocation screen** before any real-loss ruling stands: quoted material found verbatim
   elsewhere in the assembled document is downgraded to benign_relocation (`:855-874`), and turns rulings
   into findings with the adjudicator's declared weight (`fidelity_findings`, `:971-1029`).
6. **Deep-structure audit** (advisory, `:299-326`): what the document NOW runs on, six checks
   (dichotomy_visible_early, mechanism_stated_once, metaphor_before_use, demolition_before_construction,
   prescription_honest, promise_kept) and the five tests; "nothing here blocks".
7. **Independent reader** (`prompts.py:1094-1141`, `audit.py:519-611`) — "its editor, reading it cold.
   You have not seen any earlier version, any plan, any options, or any other audit, and you must not
   guess at them". Categories: self_reference ("the document talking about itself instead of its
   subject"), scaffolding ("structure announced instead of enacted — labels in prose or headings ('Test
   One', 'Case Two', 'Stage 3'), verdicts declared before or after a part …, a mechanism restated at every
   seam. A report or a brief expects signposts; an essay does not — judge by the genre"), repetition
   ("quote the first eight words of each occurrence"), seam ("a join where the previous ending and the next
   opening say the same thing, or a section that opens by announcing what it will do"), layout_artifact,
   typo, stance (where the delivered text sits on each dimension vs the declared position). Then a memo:
   "whether the first page earns the reader or briefs them; whether a reader would finish; the two or
   three moves that most reward the reader and must be protected; and the single change that would most
   improve the document. Be direct; prefer quoting to characterizing." Optionally a different model
   (`DELM_LONGFORM_READER_MODEL`, `orchestrator.py:306-314`) "reads more independently".
- **Code-authored findings** added to the same list: conservation (a source section absent from assembly),
  source-integrity boundary defects, executed_disposition ("You approved a paragraph-order rebuild …; it
  was executed as a wholesale rewrite") (`orchestrator.py:769-811`). A finding whose quoted passage is
  verbatim in BOTH source and output is marked source-owned: "this is a defect to settle in the source,
  not a change the program made" — never blocking (`audit.py:406-429`).

### B.14 · repair — the bounded polish loop (≤ 2 rounds by default)
- `select_repairs`: "Material first, then notices; skip recurrences and churned sections"; only
  `repairable_in_place` findings; legibility findings are "routed to retitle" (`audit.py:1036-1062`).
- `repair_sections` (`:1065-1156`): one call per implicated section with all its findings, its approved
  directive and stage job, its neighbours' text read-only (previous 3,000 chars / next 3,000), a cap from
  max(source, current). Byte-preserved retained sections are **protected** — "the author kept this
  section byte-for-byte; a repair may not rewrite it" (`:1077-1079`). Prompt (`:266-296`): "A finding from
  the independent reader … is executed even where the sentence it removes was planned: the plan wanted
  the structure, not its narration — remove the announcement, keep the move, keep the mechanism stated
  where the plan placed it once. Otherwise: The approved plan stands: a repair never undoes what the
  directive ordered … If a finding can only be satisfied by undoing the plan, decline it with the reason
  'conflicts with the approved plan' and the authors decide. Repair the named problems and nothing else."
- `repair_until_clean` (`:1159-1243`): after each round → reassemble → coherence re-check + independent
  reader re-read → re-adjudicate the repaired sections' fidelity; non-coherence findings persist until
  repaired; declined findings go to the author with the reason; **stop rules**: clean · "no repairable
  finding remains" · "recurrence or churn valve" (a finding recurring after its own repair; a section
  repaired 3 times) · ceiling; a **convergence** rule — "a section already re-adjudicated once keeps
  producing new wording nits each round — after the second look, the author reads it once"
  (`:1217-1222`). Every stop reason is recorded.

### B.15 · finalize — closing memo and "What changed" (1 call)
- `what_changed_record` (`memo.py:221-353`) computes mechanically: numbers (words/minutes before and
  after, sections moved/changed/unchanged/new/removed, paragraphs unchanged, "model_words" vs
  "your_words"), an outline **before beside after** with one plain note per row ("rewritten · moved (was
  4) · absorbs X · 3 of 5 paragraphs unchanged · touched by the checker"), what is gone, and every
  changed passage old beside new. The closing letter says "what the article now does for a reader that it
  did not do before …; what was NOT touched; then, honestly, what the checker still doubts and where (by
  heading), and what the authors should read themselves before using it" plus `still_look_at` "three to
  eight plain sentences, each pointing to one place" (`prompts.py:1074-1083`). `final.json` carries
  `adoptable` = no blocking finding (`orchestrator.py:900-905`).

### B.16 · resolution gate (post-finalize; 1 call per changed section)
- "Four actions per finding, none preselected: keep_rewrite … restore_source — a bounded model call
  reinstates the source material the finding names, verbatim where quoted; a mechanical check verifies the
  quote landed. replace — the author supplies wording; the call must carry it verbatim. go_further — the
  section is written AGAIN, more boldly, to its approved brief, with the finding and the previous attempt
  as context (the author judged the first execution too timid). The only action that moves forward"
  (`resolve.py:4-11`). Labels obey the destructive-label rule: "Discard my original here — keep the new
  wording" / "Discard the new wording — put my original back" (`web/longform.js:698-700`). Stale findings
  (their quoted text no longer exists) close silently (`resolve.py:64-79`). After resolutions: reassemble,
  re-screen, re-export, recompute `adoptable`, re-render the closing memo (`:324-352`).

### B.17 · lifecycle: checkpoint, resume, rewind, refusal
- One artifact per stage keyed to the source/read/deck/plan hashes; "A stage whose artifact exists for the
  same source hash is reused, never re-bought" (`orchestrator.py:4-6`, e.g. `:456-462`, `:660-668`).
  `rewind_run` "forgets a stage and everything after it … a rewind is a rollback, never a deletion; the
  earlier attempt stays readable beside the new one" (`:279-303`). A refused call (`stop_reason=refusal`)
  is retried once on a fallback model (`model.py:423-432`). A plain-number consent estimate precedes the
  first paid call (`:199-233`).

### B.18 · how the process evolved (git)
- `444c49a` 08-30 strategy memo ("fractal loop at section scale, memo v1/v2 gates, corpus scan of all 12
  books") → `4c7d0b6`/`7709bd8`/`e147e41` P0–P2 the same day → `a6e6deb` 08-31 routes + page.
- 08-31: first real run; `1c0102f` fix sweep; `00829eb` "reframe heals instead of failing"; `004b648`
  "prose-length overruns up to 1.5x the cap are accepted"; `0467fdc` Find the sections.
- 09-01: `59c227b` relocation screen ("5 of run 2's 6 'blocking' findings were relocation-blind");
  `2379cbe` job_carriers ("the root cause of runs 2-3's architecture-as-wrapper-headings"); `7d48ad6`
  resolution gate ("the run ends with a finished document, not homework").
- 09-02: `3516f74` creativity audit ("run 4 was 90 % identical … the pipeline imagines expensively,
  executes the minimum, then verifies back toward the source") → `c2a09b1`/`322f469` creativity rebuild
  (ambition, trial leads, compress/rebuild/inline units, plan-aware audit, memos as letters, go-further)
  → `37002ab`/`dfcc601` deep structure → `7d7a5a1` narrative pack → `6c4459d` memo sub-tabs.
- 09-03: `9816998` "the frame stops narrating itself — ENACT, NEVER ANNOUNCE … an independent reader
  stage (cold, plan-blind)"; `79cb305` essay form; `b70e3bc`/`30e76c7`/`15b3cf3` narrative stance.

---

## C. The creative restructuring moves — a catalogue

Each: **name** · when it fires · what it changes · the language that triggers it.

1. **Whole before parts, plain summary first.** Fires before any section is judged. Produces the frame
   every later call inherits: four-sentence plain summary, then the *buried crux*. "what the document's
   structure buries, delays, or never states plainly — the thing its readers actually need to decide or
   are afraid of — with where it currently hides" (`prompts.py:38-42`).
2. **Reader-mode declaration.** In the read; consumed by rank and audit. Straight-through vs consulting
   readers become a *design requirement*: "for readers who CONSULT … an architecture that relocates the
   payoff must say how those readers still find it" (`prompts.py:580-586`).
3. **The journey as it actually runs, with the honest admission.** "including where the order is the
   order the research was done in, or a funder's template" (`prompts.py:49-51`); "a report's current order
   is usually the order the research was done in … neither is an architecture" (`:281-283`).
4. **Accidental recurrences as candidate threads.** Read stage: "STRANDS … INCLUDING accidental
   recurrences the author may not have noticed … Mark accidental ones" (`:54-57`). Later the strand audit
   reads each strand consecutively.
5. **Apparatus gaps: what should be a table.** Read stage: "GAPS — apparatus the material needs and lacks
   (a glossary, a list of abbreviations, a table doing in prose what a table should do)" (`:65-67`);
   candidates carry an `apparatus_plan` with `apparatus_gaps`; the plan may propose an `apparatus` unit
   "a table the material needs", but "Never a table that restates an existing table, never a second
   consolidation of material already consolidated" (`:740-744`).
6. **The card deck: actual job vs promised job; anchored vs mobile; body / front frame / annex.** One
   call per section; the deck is the working vocabulary of imagination. "actual_job: what the section
   actually does for the reader (not what its heading promises)" (`:172-173`); "mobility: 'anchored' if
   chronology, causation, or dependency fixes its position, else 'mobile'" (`:184-185`); "path_function
   … 'annex' if deepening but distracting (… an annex deepens, it is never leftovers)" (`:185-187`);
   "owes_the_reader: what the reader wants next when this section ends" (`:191-192`).
7. **"What does the reader need next" as a contract at every seam.** `owes_the_reader` on the card;
   `new_role` on the directive: "its EXIT requirement (the ending throws forward to what follows — Stein's
   chapter contract)" (`:674-676`); the writer must "Honor the FRAME requirement (the point and forecast
   up front) and the EXIT requirement (throw forward to what follows)" (`:865-866`).
8. **Deep read → latent elements as re-founding material.** "what is LATENT: elements the material would
   support that the document never states … The latent list is the raw material of re-founding"
   (`:132-137`); a candidate may add an element "only from the deep read's latent list or the document's
   own material" (`:469-470`); "A shape whose every element is 'kept' is a rearrangement — say so
   honestly" (`:470-471`).
9. **Strategy families, different by strategy not degree.** Diagnosis names 3–5 of thirteen moves; hard
   constraints force range: "At least two families must be radical, one family must be rebuild_from_cards
   …, and at least one family must re-found the deep structure … No two families may share a primary
   strategy or an opening section" (`:392-398`). Code rejects otherwise (`program.py:977-984`).
10. **Repair vs architecture.** "Moving one or two sections, or adding a bridge, is a REPAIR, not an
    architecture; the authors have cheaper tools for repairs" (`prompts.py:275-277`). The essay-scale
    parent: "a set of timid variations is rejected whole" (`delm/structural_program.py:310`).
11. **Rebuild from cards.** A mandatory family: "throw the current order away: deal the section cards on
    the table, anchor what chronology or dependency fixes, and build the strongest architecture the
    material supports whatever the present sequence (McPhee's card table)" (`prompts.py:368-370`).
12. **Trial leads.** Three openings written from the material before any skeleton: "a lead that is true
    to the material commits the whole to a shape … Say in commits_the_whole_to what following it would
    oblige the rest of the document to do" (`:430-441`); later a body unit of kind `lead` may grow from
    the adopted one (`realize.py:1035-1036`, `:1052`).
13. **The settled adjacency.** "A candidate is SETTLED when its charged adjacency has been found and the
    remaining units assemble around it without forcing (McPhee) — name that adjacency" (`:291-293`);
    `settled_adjacency` per candidate; `seed_adjacency` per family.
14. **Stage skeleton with a reader-facing job and complete coverage.** "3–14 stages, each with a label,
    its reader-facing job, and existing_section_ids in intended reading order. EVERY unit section id …
    must appear in exactly one stage" (`:491-494`); "A stage may hold a single section or a single new
    unit when that unit does a distinct job (a lead, a verdict page, a decision page): one member is not a
    defect" (`:497-499`).
15. **Path plan: promote to the front, demote to an annex, retire.** `path_plan.front_frame / annex /
    retired`; "a load-bearing introduction is chapter one" (`:504-506`); dispositions `to_front` /
    `to_annex` require the opening to be reframed "so the section stands alone" (`:849-850`).
16. **Front/back matter as the only fixed points.** "the ABSTRACT states the finding and stays first;
    acknowledgements, funding, endnotes and references stay last. Everything else is material — a policy
    box, a summary box, an introduction, a methods note are the material a shape may relocate, absorb,
    rebuild around, or open with" (`:532-536`). (The creativity audit found the earlier "genre lock"
    had frozen an extraction artefact — `SYNTHESIS.md:48-52`.)
17. **Escalation of a buried point: the verdict page and the front-loaded finding.** Body unit
    `verdict_page`: "the finding and its limits stated once, plainly, where the architecture puts it"
    (`:734-735`); the executive summary "states what the body now argues" (`:738-739`); `OP_PROMOTE_OR_
    DEMOTE_CLAIM` in the operations material. The realized examples: D-bold-counterproposals' "Calais
    Brief" opens on a scene then "states the complete two-part verdict in the paragraph after it"
    (`D-bold-counterproposals.md:15`, `:34-44`).
18. **Sibling contracts: comparable parts by construction.** `sibling_groups` on the candidate and
    `sibling_contracts` on the plan: "the one question every member must answer (Zinsser's method), so
    siblings become comparable by construction" (`:765-766`).
19. **Strand schedule with dosage.** "each strand's returns in order with the dosage (McPhee: each return
    larger than the last, timed before the set piece; Gardner: space returns so no line cools)"
    (`:508-510`); audited by the strand audit ("dead returns", "cooling").
20. **Compression as a signed operation, never a silent floor.** "compress (rewritten to a length_target
    _words BELOW three quarters of its present length — every claim, citation and qualification survives
    in less space; the authors sign every compression in memo v2, so say why)" (`:652-654`); code renames
    a sub-75 % rewrite to a compression instead of raising it (`realize.py:195-218`); the writer:
    "McPhee's greening: meet the quota from the middle, not the end" (`:840-842`).
21. **Merging (absorb) and rebuilding a group into a new argument.** `merge_into` + `rebuild`: "this
    section is rebuilt into a NEW argument from its own material plus the sections that merge_into it — a
    re-founding of a group, not an edit; the brief states the argument the rebuilt section makes and the
    claims from every source's card it must carry" (`:654-657`); the adjudicator is given "for a rebuild
    the claims every source card carries" (`audit.py:228-229`).
22. **Splitting where one job ends.** `split`: "its material becomes two or more titled sub-parts at its
    place" (`:660-661`); `OP_SPLIT — Split a unit where one job ends and another begins`.
23. **Role-changing movers may not be byte-preserved.** "A section relocated into position 1, the final
    position, or the opening or closing of a stage from elsewhere changes role: it may NOT carry retain
    or move_only" (`:665-666`; `realize.py:352-359`).
24. **Architecture promises must name their builders (job carriers).** "for EVERY stage, name what
    DELIVERS its reader-facing job … retain and move_only cannot build a promise … A stage job that names
    relocated or front-loaded content with no carrier is the defect this field exists to prevent"
    (`:756-763`). Born from runs 2–3, where "Plans satisfied placement checks while no directive delivered
    any stage's promised job" (`LONGFORM_BUILD_RETROSPECTIVE_2026-09-02.md:73-75`).
25. **Depth held to the card.** "a section the option said would be rebuilt is not quietly reframed …
    a shortfall without a reason the authors would accept is a failed plan, not a cautious one"
    (`:720-728`; `realize.py:155-172`).
26. **Argument threading: seed, pay off, first mentions moving, references to reanchor.** Per directive
    `must_seed / must_pay_off for preparations and payoffs across the new order; first_mentions_moving for
    terms whose introduction changes home; refs_to_reanchor for references the new order breaks;
    preserves for the facts, claims and qualifications this section must carry through" (`:682-686`).
27. **The live seam and the thread ledger (reader memory).** Generation is sequential in the *new* order;
    each call sees the previous section's closing paragraphs and a code-kept ledger of terms anchored
    (with words since), promises open, floats referenced (`realize.py:909-958`); "re-introduce a term or
    figure the ledger shows as anchored far back (readers do not 'still remember what was once
    explained'); repair the seam so this opening grows from the previous closing" (`:866-869`).
28. **Frames written last, top-down.** Body units inline in reading order; frame units (executive
    summary, part introductions, bridges, apparatus) after the body, "executive summary last"
    (`realize.py:1303-1310`); "an executive summary states what the body now argues, in the body's
    proportions, with the body's qualifications" (`:928-930`). Design memo: Williams' descending schedule,
    "get beginnings straight" (`LONG_FORM_RESTRUCTURING_MEMO_2026-08-30.md:78-81`, `:459-465`).
29. **Retitle after the architecture stabilizes; headings carry themes, never scaffold.** (`:954-973`)
    plus the second legibility pass driven by the cold reader (`realize.py:1406`).
30. **Register / tone control: ENACT, NEVER ANNOUNCE, keyed to genre.** Plan (`:697-701`), writer
    (`:875-882`), unit (`:941-946`), retitle (`:965-967`), and the independent reader's `self_reference`
    and `scaffolding` categories (`:1102-1107`). Steering has three positions — signposted (report /
    brief), one_brilliance, continuous (essay) — with genre defaults (`stance.py:50-63`, `:258-263`).
31. **Narrative stance as explicit choices.** Sixteen dimensions with poles, a middle, costs, and genre
    defaults: thesis placement, reader steering, mode, opening ethos, epistemic status of examples,
    concepts vs cast, narrator function, certainty (hedges standing / declared / smoothed), spine, scene
    ratio, revelation schedule, carrier, ending (summary / verdict-then-image / resonance), proportion,
    coined terms, genre expectation (`stance.py:33-248`; `NARRATIVE_STANCE_DIMENSIONS_2026-09-03.md`).
    The architect declares ten per candidate so "Options must differ in STANCE and not only in order"
    (`prompts.py:481-483`); the writer is held to eight; the cold reader reports where the text actually
    sits and breaches become findings (`audit.py:583-597`).
32. **Prose vs apparatus decisions.** Tables and figures are protected nodes: "Tables and figures are
    reproduced verbatim where the section carries them; you may move a reference to one, never its
    content" (`:855-856`); floats renumbered by first mention at assembly (`integrity.py:208-222`);
    "the table above/below" is a smell counted mechanically (`integrity.py:23-26`); the read names tables
    the prose is doing (`:65-67`); an apparatus unit may be proposed with a `distinct_job` (`:740-744`).
33. **Redundancy collapse.** Coherence category `repetition_and_proportion` ("duplicated jobs across
    sections"; `audit.py:94-97`); the independent reader's `repetition` ("a paragraph that restates what
    the reader just read (quote the first eight words of each occurrence)") and `seam` ("the previous
    ending and the next opening say the same thing"); the writer's "The mechanism is stated once, where
    the plan places it; everywhere else it is used, not restated" (`:882-883`); the run-4 lesson: the aim
    "stated once, never restated wholesale" was failed by wrapper headings (`SYNTHESIS.md:25-27`).
34. **Cumulative direction.** "across a span of pages, which way does the verbiage push the reader's
    belief, and does that match the stated claim; counter-evidence quarantined in its own bounded section
    or bleeding through" (`audit.py:94-97`).
35. **Cold-reader reconstruction from the navigational surface.** The judge that catches architecture
    that exists only in the plan (`audit.py:141-182`, `:686-773`): "recoverable but invisible" is the
    target; legibility findings route to retitle, not to body rewrites (`audit.py:1046-1050`).
36. **Plan-aware judging; the plan stands in repair.** The 09-02 correction to a loop that "verifies back
    toward the source" (`SYNTHESIS.md:65-67`): drift rules `planned` (`audit.py:232-237`), repair
    "never undoes what the directive ordered" (`:280-284`), but reader findings about narration are
    executed regardless (`:276-279`).
37. **Relocation-blind judges get a mechanical whole-document check.** (`audit.py:855-874`;
    retrospective §4.5 `:67-68`.)
38. **Synthesized claim ≠ invented fact.** (`audit.py:243-246`.)
39. **Bounded repair with stop rules and a churn valve; declines go to the author.** (`audit.py:1036-1062`,
    `:1159-1243`.)
40. **The author's two directions of cut negotiation.** "restore into the new skeleton, or trim from the
    full — described so the authors pick the direction" (`:782-784`; design memo `:410-415`).
41. **Parking lot and queries instead of silent decisions.** "parking_lot: doubtful changes you declined
    to make, noted for the authors (Stein)" (`:781`); queries are "bounded, evidence-citing … with options
    and what happens if unanswered" and "A query never commissions new writing" (`:767-780`).
42. **Go further.** The only resolution action that moves forward: "the section is written AGAIN, more
    boldly, to its approved brief, with the finding and the previous attempt as context" (`resolve.py:9-11`;
    the writer prompt: "the authors judged it too timid — execute the brief more boldly, and say in notes
    what you did differently", `:850-852`).
43. **Change described, never scored; ranking by reader gain under declared ambition.** `change_profile`
    "A description, never a score" (`program.py:282-285`); `AMBITIONS` tidy / rebuild / open
    (`program.py:79-83`); "Never rank by least work" (`prompts.py:574-577`). The earlier "damage meter"
    ("re-routes 0 % of seams") was found to make the model and the author minimise change
    (`D-bold-counterproposals.md:158`).
44. **Memos as letters with before/after on the first page.** `MEMO_LETTER_SYSTEM` and
    `what_changed_record`: numbers, outline before beside after, changed passages old beside new
    (`memo.py:221-353`); the audit that demanded it: "No memo shows a before and after anywhere: no old
    outline beside new, no changed passage quoted, no diff" (`SYNTHESIS.md:88-90`).
45. **Bounds heal, structure fails; one corrective re-ask with the exact failures.** (`program.py:353-386`,
    `:497-535`; retrospective §4.1 `:53-55`.)
46. **Frozen architecture during generation.** "a problem a section call discovers with the plan becomes a
    query or a parking-lot note for the author, never a mid-run plan change" (design memo `:447-451`).

---

## D. What to lift into The Analyst's dossier composition — and what not

### D.0 Where the dossier pipeline stands (read from `src/dossier/`)

Eight steps: reconnaissance → brief (three tellings; the author's gate) → plan (engines) → analysis
(executor phases, each reading the previous phases' prose) → tables (2–3, every row behind the verbatim
anchor wall) → figures (1–4 depictable scenes) → **compose** → receipts (`runner.py:22-35`). Compose is
**one Sonnet call** (`compose.py:92-94`) that returns title, subtitle, a 1–3-paragraph executive summary,
3–7 sections of 1–6 paragraphs each with anchored claims, a 1–3-paragraph conclusion, and the placement of
every table and figure by key (`SECTIONS_SCHEMA`, `compose.py:35-59`; system prompt `:61-67`). The whole
corpus (≤500K chars), the analysis prose, the profiles and the table/figure descriptors go in the user
message (`:70-89`). Anything unplaced lands in the last section (`:179-189`). There is no outline pass, no
per-section call, no seam or ledger, no frames-after-bodies, no retitle, no coherence or cold-reader
judge, no repair loop, no before/after record; the brief's `output_shape.sections` are "suggested"
headings (`:80`, `:86`), and the prose-vs-table decision is made *before* composition by the tables desk
from the analysis (`tables.py:46-51`), not by the composer with the reader's route in view.

Everything below keeps the dossier's own protections (anchors and the wall, engine-derived material only,
audience registers, autopilot-first for the demo) and adds de-llm's coherence-seeking loop **at the scale
of a 5–9-section dossier**, which means a handful of extra calls, not a hundred.

### D.1 The lifted process, in order (draft → restructure → write parts against the whole → judge → repair)

**Pass 1 — Composition read (1 call, new: `src/dossier/compose_read.py`).** Before any section is
written, over the analysis prose + profiles + verified tables + figure briefs (the corpus available for
anchors). Lift moves C.1, C.2, C.4, C.5, C.34. Draft system prompt:

```
You are the READ of The Analyst's writing desk: the first pass over everything the analysis produced
before any section of the dossier is written. Nothing is written here. Declare, for the stated audience:
1. PLAIN SUMMARY FIRST: in at most four sentences, what this dossier says — its subject, its finding,
   what it wants the reader to do. Then BURIED OR UNSTATED: what the analysis phases carry but never state
   plainly — the decision the reader actually needs, the disagreement between the documents, the caveat
   that changes the finding — with where it hides (which phase, which table row).
2. WHO READS IT AND HOW: the reader types (from the audience register), whether each reads straight
   through or consults (summary, one table, the recommendations), what each wants to leave with.
3. THE GOVERNING CONTRACT: the one point, the question the dossier answers, who speaks, the register.
4. STRANDS: the through-lines that run across phases, tables and figures — named cases, actors, tensions,
   numbers — INCLUDING accidental recurrences (the same example used by two phases). Mark accidental ones.
5. WHAT SHOULD BE A TABLE, A FIGURE, OR PROSE: every enumeration the analysis makes in prose that a table
   would show better (name its rows and columns from the material); every verified table that is really
   one claim and should become a sentence; which figure ideas earn their place and which are decoration.
6. CUMULATIVE DIRECTION: across the analysis as a whole, which way does the evidence push the reader's
   belief, and does that match the finding the brief promised? Where is the counter-evidence, and does it
   need its own bounded section?
7. FORM CAPACITY: does this material fill a 5–9-section dossier, or is it two sections and a table?
Return strict JSON only: {plain_summary, buried_or_unstated, readers:[{type, mode, wants}],
governing_contract:{one_point, question_it_answers, register}, strands:[{name, carried_by:[phase|table|figure keys], accidental, note}],
apparatus:{prose_to_table:[{what, rows, columns, from}], table_to_prose:[table_key], figures_earned:[key], figures_dropped:[{key, why}]},
cumulative_direction:{push, matches_finding, counter_evidence_where}, form_capacity:{verdict, reasoning}}
```

**Pass 2 — Architecture: the outline as a stage skeleton with job carriers (1 diagnosis+candidates
call, or 1 call per candidate; new: `src/dossier/architecture.py`).** The brief already chose a telling,
so this pass realizes it structurally rather than re-choosing the angle — but it should still offer **two
skeletons different by strategy** (lift C.9, C.10 in a small form: emphasis_order, governing_axis,
container/borrowed form — decision memo, case file — carrier, proportion) and a `rebuild_from_cards`
variant that ignores the brief's suggested headings, then rank by the reader's gain; autopilot takes rank 1,
the desk may show both as cards (the brief page already has the card grammar). Lift C.13, C.14, C.15,
C.17, C.18, C.19, C.24, C.32. Draft:

```
You are the ARCHITECTURE stage of The Analyst's writing desk. The READ, the chosen telling, the audience,
the analysis prose per phase, the verified tables (with their rows) and the figure briefs are in the
payload. You are not writing prose; you are deciding what the dossier IS.
The material is your limit, never the analysis's order: the phases ran in the order the engines were
chained, and that is not a reading order. Build TWO candidate skeletons different BY STRATEGY (what the
reader meets first · the governing axis: decision order, mechanism, case, question-chain · the container:
decision memo, case file, briefing, comparison · what carries it: a case, an actor, a number), one of
them built with no allegiance to the brief's suggested headings. A candidate whose sections merely
re-label the analysis phases is a repair, not an architecture.
For each candidate: name; thesis_of_change (the route the reader lives; one visible consequence naming
material — "the Orange hedge from phase 4.2 becomes the opening"; a final "Choose this if …");
settled_adjacency (the two pieces of material whose placement side by side the whole is built around);
stage_skeleton: 4–9 stages, each with a label, its reader_facing_job, the MATERIAL it draws on (phase
keys, table keys, figure keys, profile claims) and its job_carrier — which of those pieces actually DELIVERS
the job (a table cannot carry an argument; a phase's prose cannot carry a comparison a table shows);
apparatus_plan: where each verified table goes and what it proves there, which enumeration becomes a new
table (rows and columns named from the material, anchors required), which table becomes a sentence, which
figure goes where and what it makes visible; strand_schedule for every strand from the READ (its returns
in order, each larger than the last); sibling_groups (parallel sections that must answer one shared
question); new_material: a lead, a verdict paragraph stated once, a bridge — its job and its material, not
its text; author_cost.reader_gain (the concrete thing the reader can now do or see); stance for this
audience: thesis stated|promised|discovered · steering signposted|one_brilliance|continuous · examples
proof|test|clue · ending summary|verdict_then_image|resonance.
Every table and every earned figure appears in exactly one stage. The executive summary is a FRAME written
after the body and is not a stage. Then rank the two by what the reader gains toward the telling; never by
least work. recommendation_reasoning names what the loser does better and why it still loses.
Return strict JSON only: {candidates:[…], ranking:[{ref, rank}], recommended_ref, recommendation_reasoning}
```

Code (shape only): every table and figure key placed once; stage labels unique; the recommended is rank 1;
a `job_carrier` must be a piece the stage lists; compute and show "opens on … · N tables placed · N new
tables · N figures kept/dropped" as the description beside each card (lift C.43).

**Pass 3 — Section writing in reading order with a live seam and a ledger (1 call per stage; rewrite
of `compose.write_sections`).** Lift C.7, C.26, C.27, C.30, C.32, C.33. Each call sees: the READ, the
chosen skeleton, THIS stage's job / carrier / material (the phase prose it draws on, the table rows, the
figure caption), the previous section's closing paragraphs as written, what follows and its job, the
ledger (terms introduced with words since; promises open; tables and figures already referenced by
number; named documents already introduced), the audience register, a `max_words`, and the corpus for
anchors. Draft:

```
You write ONE section of the dossier for its place in the chosen architecture. The payload carries this
stage's reader-facing job, the material that carries it, the LIVE SEAM (the closing paragraphs of the
section the reader has just finished), what follows next and its job, the THREAD LEDGER (terms and
documents already introduced and how far back; promises the earlier sections opened; tables and figures
already referred to), the audience register, and the DOCUMENT TEXT for anchors.
Rules: do this stage's job and nothing else — a section that restates the executive summary or the
previous section's point fails its job. Open by growing from the seam, never by announcing what the
section will do; for the executive audience one signpost per section at most, in the register; for
researchers, state the section's question once in its first sentence. State the finding once, where the
architecture places it; everywhere else USE it, do not restate it. Honor the frame requirement (the point
and what the section forecasts, early) and the exit requirement (the ending throws forward to what
follows). Pay off what the ledger shows open when this is the section that earns it; re-introduce a
document or a term the ledger shows anchored far back. Refer to a table or figure by the name in the
ledger ("Table 2") and say in one sentence what the reader should take from it; never restate its rows in
prose, never "the table below". Every claim that rests on a passage carries an anchor copied
character-for-character from the DOCUMENT TEXT (40–200 chars); mark it {{n}} after its sentence. Never
introduce a fact the documents and the analysis do not carry; if the job cannot be done without one, put
the gap in queries. Stay within max_words; compress from the middle, not the end.
Return strict JSON only: {section:{heading, paragraphs:[…], claims:[{text, anchor}], table_keys, figure_keys,
ledger_delta:{terms_introduced, documents_introduced, promises_opened, promises_paid, floats_referenced},
queries:[…], notes}}
```

Code keeps the ledger (lift `ThreadLedger`, `realize.py:909-949`, shrunk: terms, documents, promises,
floats), the seam (`:952-958`), the anchor wall per section as now, and a per-section checkpoint.

**Pass 4 — Frames last (1–2 calls).** After the body: the executive summary — "states what the body now
argues, in the body's proportions, with the body's qualifications, so a busy reader can decide without
reading further" — and the closing "what this means", written against the assembled body, never before it.
Lift C.28 verbatim from `prompts.py:928-930`. Draft user instruction: "Write the executive summary from the
ASSEMBLED DOSSIER below, in 1–3 paragraphs: the finding and its limits once; the decision the reader can
take; nothing the body does not carry; no sentence that restates a section's opening line."

**Pass 5 — Retitle (1 call, cheap).** Lift C.29: "each heading carries its section's key themes …
siblings balanced … nothing renamed for its own sake … no 'Section 3:' scaffold"; keep it for the executive
register where headings are navigation.

**Pass 6 — Mechanical assembly and screens (0 calls).** Already partly in `_render_context`: number
tables/figures by **first mention in the prose** rather than by section order (lift `integrity.py:208-222`);
resolve "Table N" mentions to the final numbers; count relative references ("the table below"); compute
a repetition screen (sentences ≥ 8 words that recur, first-eight-words fingerprint), a proportion profile
(words per section vs the skeleton's intended weight), unplaced tables/figures (today silently dumped into
the last section — make it a named finding, lift C.24/"conservation"), and the existing anchor counts.
Signals only.

**Pass 7 — Two judges over the clean copy (2 calls; optional 3rd).** Lift C.33–C.36 in a small form:

- *Coherence audit* (adapted from `audit.py:70-139`): the assembled dossier with headings tagged, the
  skeleton's stage jobs, the READ, the screens. Categories, each across every section: argument_progression
  (does each section advance the finding; does the order realize the skeleton's jobs); seams_and_references
  (every backward reference against what the reader has by then; first mentions of documents and terms);
  repetition_and_proportion (the finding restated wholesale; a table's rows narrated in prose; cumulative
  direction vs the stated finding; counter-evidence bleeding or quarantined); executive_summary_and_frames
  (does the summary state what the body now argues, in its proportions, with its qualifications);
  apparatus_and_navigation (every table and figure referred to before it appears, said what it proves;
  headings that carry themes; no "table below"). Each finding: section ids, diagnosis with a quote,
  reader_effect, severity notice|material, repair_route repairable_in_place|needs_new_material|needs_author.
  "A change the architecture ordered is the desk's decision, never a defect: judge whether it was done well
  for the reader." Cap ≈ 3 findings per section.
- *Independent reader* (lift `prompts.py:1094-1141` nearly verbatim, minus stance/layout): a model that
  sees only the dossier and its audience — self_reference, scaffolding, repetition, seam, typo — plus the
  memo: "whether the first page earns the reader or briefs them; whether a reader would finish; the two or
  three moves that most reward the reader and must be protected; and the single change that would most
  improve the dossier." Use a different model than the writer if available.
- Optional *cold-reader reconstruction* (headings + first/last paragraphs only → outline as read → compare
  with the skeleton): the one judge that catches "wrapper headings"; cheap (two small calls).

**Pass 8 — Bounded repair (≤ 2 rounds, 1 call per implicated section).** Lift `select_repairs` and
`repair_until_clean` stop rules (`audit.py:1036-1062`, `:1159-1243`): material first, repairable_in_place
only, skip a finding that recurs after its own repair, hand a section to the author after 3 repairs, round
ceiling, then re-audit. The repair call carries the section's stage job, its neighbours read-only, the
findings, the anchor rule: "Repair the named problems and nothing else … a reader finding about
self-reference or scaffolding is executed even where the sentence was planned — remove the announcement,
keep the move" (`audit.py:276-284`). Declined findings surface in the "How this was made" appendix with
the reason.

**Pass 9 — "What changed / what the checker still doubts" record (0–1 calls).** Extend the existing
"How this was made" appendix and the desk's DraftStep with a mechanical record modelled on
`what_changed_record` (`memo.py:221-353`): the outline as planned beside the outline as delivered with a
note per row; findings repaired / declined / open; anchors kept / dropped; tables placed by first mention;
the reader memo's "protect these moves" and "the single change". A one-call closing letter is optional
(`MEMO_LETTER_SYSTEM`, `prompts.py:1074-1083`), useful for the executive audience.

**Optional gate — resolution in the desk.** The DraftStep already has "regenerate/sharpen per item"; add
de-llm's four actions on each open doubt with **no default**, especially *go further* ("write this section
again, more boldly, to its job, with the finding and the previous attempt as context", `resolve.py:9-11`,
`prompts.py:850-852`) — it is the one action that increases ambition instead of converging back.

Call budget for a medium dossier: today 1 compose call → ~1 read + 1–2 architecture + 6–9 sections + 2
frames + 1 retitle + 2–3 judges + ≤4 repairs ≈ 15–22 calls, all on cached prefixes; wall-clock dominated by
the sequential section writes (each small). Keep the single-call compose as the `simple` depth path.

### D.2 Doctrine to lift with the passes

- **Shape in code, judgment in the model; bounds heal, structure fails; one corrective re-ask with the
  exact failures** (`program.py:353-386`, `:497-535`). `call_json` already re-asks once on schema failure
  (`src/dossier/llm.py:227-264`); add the *heal* side: never truncate prose to a guide, only note it.
- **Detection without routing is useless**: every finding enters the repair loop or the author's screen;
  nothing is merely printed (retrospective §4.4 `:64-66`).
- **Judges must know the plan**, or they converge the text back to the source (`SYNTHESIS.md:65-67`;
  `audit.py:80-85`). The dossier's analogue: the coherence judge sees the skeleton's stage jobs and the
  apparatus plan.
- **Relocation-blind judges** get a mechanical whole-document check before a "lost" ruling stands
  (`audit.py:855-874`) — for the dossier: a claim "missing" from a section that lives in the table or in
  another section is benign.
- **Description, never a score, beside every option; rank by the reader's gain** (`program.py:282-343`,
  `prompts.py:574-577`).
- **Executive summary and conclusion are frames, written last** (`realize.py:1303-1310`).
- **ENACT, NEVER ANNOUNCE, keyed to the audience** (`prompts.py:697-701`, `:875-882`): for executives one
  signpost per section; for researchers the question stated once; never "this section will".
- **Checkpoint per section; resume without re-buying** (`orchestrator.py:659-684`) — the dossier runner
  already persists per step; persist per section inside compose.

### D.3 What NOT to lift, and why

- **The three mandatory author gates (choice, approval, resolution) as stops.** de-llm is an editing
  studio over an author's own manuscript; the gates are its ethics ("a re-imagining is proposed and
  queried, never applied", design memo `:64-68`). The dossier is autopilot-first for the demo; the brief is
  its one gate. Keep architecture cards and resolution as *optional* desk affordances.
- **The twelve dispositions and byte-preservation.** They exist to protect an author's wording
  (retain/move_only byte-exact, reframe with a preserved middle, signed cuts). The dossier writes from
  analysis, not from a manuscript; there is no author text to preserve byte-for-byte. Use only:
  write / compress (a stage whose material is over-weighted) / merge (two stages doing one job) /
  split / cut (a stage with no carrier). Keep `compress` signed in the desk if the user asked for
  length.
- **The style sheet as a stage.** Valuable when rewriting a 60-section manuscript in parts; for a
  5–9-section dossier written in one sitting, fold a small conventions register (document labels, the
  audience's do-not-say words, number style, table/figure naming) into the ledger's first entry.
- **The deep read of twelve elements and the 28-book corpus.** Heavy and essay-oriented. Lift only
  "mechanism stated once, where the plan places it" and "cumulative direction" into the read and the
  coherence audit; do not carry the corpus.
- **Sixteen stance dimensions.** Lift four that decide a dossier's register (thesis placement, steering,
  status of examples, ending), defaulted from the audience (executive ≈ de-llm's `brief` defaults:
  stated · signposted · proof · summary, `stance.py:262`; researcher ≈ `paper`). The rest are essay craft.
- **PDF ingest, the section finder, DOCX, pandoc.** The Analyst's sources module already resolves documents.
- **The paragraph-scale `restructure` leg** (`run_structural_revision` inside a section) — de-llm's own
  data shows it silently fell back to a rewrite for its first two days (`retrospective:76-78`); a dossier
  section is 1–6 paragraphs and a rewrite is the right tool.
- **Rewind archives, review bundles, the operator token, consent estimates.** The dossier has receipts,
  events/SSE, and a spend cap already.
- **Thirteen strategy families and 3–5 candidates.** At dossier scale two candidates (one "rebuild from
  the material") and one rebuild policy suffice; the families that matter here are emphasis order,
  governing axis (decision order · mechanism · case), borrowed form (decision memo · case file), carrier
  and proportion.
- **The essay-form output (headings dropped)** and **retitle-as-second-pass triggered by legibility** —
  keep the single retitle call; the executive audience wants navigation.
- **The 1.5× length tolerance as a rule.** Dossiers have a reader's time budget; enforce `max_words` per
  stage from the skeleton's proportion plan and let the audit flag proportion, not the writer's cap.

### D.4 The order to build it (each step verifiable alone)

1. Composition read + ledger-aware per-section writing + frames last (replaces the one-call compose behind
   `depth != simple`); verify: no section restates the summary; every table referenced before it appears;
   anchors ≥ today's rate.
2. Architecture pass with job carriers and the apparatus plan; verify: at least one enumeration in the
   analysis becomes a table with anchored rows, and one figure is dropped as decoration on the fashion bundle.
3. Assembly screens (first-mention numbering, repetition, proportion, unplaced items as findings).
4. Coherence audit + independent reader + bounded repair; verify on a stored job that the reader's
   `scaffolding` and `repetition` findings drop to zero after ≤ 2 rounds and nothing invented enters
   (anchor wall unchanged).
5. "What changed / still look at" on the DossierStep; optional go-further on a section.

---

## E. Citations block (exact paths and line ranges)

de-llm (`/home/evgeny/projects/de-llm`, commit `15b3cf3`):

- `CLAUDE.md:1-95` — project overview; long-form packs, deep structure, narrative stance (`:32-52`);
  design rules (`:79-91`).
- `communications/LONG_FORM_RESTRUCTURING_MEMO_2026-08-30.md` — §0 twelve-line answer `:36-116`;
  §2 "the loop is fractal" `:155-199`; §3 stage contracts L0 `:208-296`, L1 `:298-352`, L2 `:354-369`,
  L3 `:371-419`, L4 `:421-479` (frozen architecture `:447-451`, frames top-down `:459-465`),
  L5 `:481-547`, L6 `:549-559`; §4 "why many calls" `:561-596`; §5 apparatus table `:598-612`;
  §7 rules per stage `:630-644`; §8.4 verdict `:859-904`; §10 determinism ledger `:999-1017`.
- `communications/engineering/LONGFORM_BUILD_RETROSPECTIVE_2026-09-02.md` — stages `:24-30`; four
  runs `:37-47`; nine failure classes `:49-85`; the product turn `:100-115`.
- `communications/audit-2026-09-02-creativity/SYNTHESIS.md` — verdict `:10-31`; five locks `:32-71`;
  memos read like audits `:84-99`; what to change `:117-144`.
- `communications/audit-2026-09-02-creativity/D-bold-counterproposals.md` — three restructurings
  `:13-127`; why wrapper headings `:146-162`; the choice screen `:166-185`.
- `communications/LONGFORM_OWNER_BRIEF_2026-09-02.md:1-17`.
- `communications/NARRATIVE_STANCE_DIMENSIONS_2026-09-03.md:1-160` (dimensions 1–6 read in full).
- `communications/IMPLEMENTATION_TRACKER.md:1-140` — stance plug-in table; deep-structure steps;
  creativity rebuild phases A–E.
- `delm/longform/__init__.py:1-19`.
- `delm/longform/prompts.py` — `COMMON_PREAMBLE :11-21`; `DOCUMENT_READ_SYSTEM :27-103`;
  `DEEP_READ_SYSTEM :109-157`; `SECTION_CARD_SYSTEM :163-223`; `STYLE_SHEET_SYSTEM :229-264`;
  `_ARCHITECTURE_DOCTRINE :270-336`; `ARCHITECTURE_DIAGNOSIS_SYSTEM :338-426`; `TRIAL_LEADS_SYSTEM
  :428-446`; `ARCHITECTURE_CANDIDATE_SYSTEM :448-558`; `ARCHITECTURE_RANK_SYSTEM :560-613`;
  `CORRECTIVE_SUFFIX :615-620`; `REALIZATION_PLAN_SYSTEM :627-817`; `SECTION_REWRITE_SYSTEM :823-907`;
  `NEW_UNIT_SYSTEM :909-952`; `RETITLE_SYSTEM :954-973`; `SECTION_FINDER_SYSTEM :976-1012`;
  `RESOLUTION_SYSTEM :1015-1028`; `MEMO_LETTER_SYSTEM :1035-1087`; `INDEPENDENT_READER_SYSTEM :1094-1141`.
- `delm/longform/program.py` — `AMBITIONS :79-83`; `RunSettings :86-139`; `prefix_blocks :163-173`;
  `_rule_projection :187-211`; `lens_material :214-234`; `STRATEGIES :254-255`; `renumber_case_labels
  :264-279`; `change_profile :282-343`; `_Check._too_long :370-386`; `_call_with_correction :497-535`;
  `_validate_read :542-622`; `deep_read_document :700-727`; `build_card_deck :784-862`;
  `declare_style_sheet :917-933`; `_validate_diagnosis :940-987`; `_validate_trial_leads :990-1013`;
  `_validate_candidate :1068-1198`; `measure_disruption :1201-1221`; `imagine_architecture :1229-1456`.
- `delm/longform/realize.py` — dispositions and kinds `:39-52`; `record_choice :99-132`;
  `computed_depth_codes :155-172`; `computed_deviation_codes :175-192`; `declare_compression :195-218`;
  `_validate_plan :223-567` (role-changing movers `:352-359`, deviations `:360-380`, job carriers
  `:420-459`); `plan_realization :570-634`; `default_approval :668-702`; `normalize_approval :705-751`;
  `effective_program :754-818`; `_cap_for :834-840`; `_validate_section_output :843-902`;
  `ThreadLedger :909-949`; `_seam :952-958`; `_restructure_leg :961-984`; `generate_document :987-1195`;
  `assemble_document :1246-1290`; `write_new_units :1293-1337`; `validate_retitle :1340-1373`;
  `retitle_document :1376-1417`.
- `delm/longform/audit.py` — `_AUDIT_PREAMBLE :63-68`; `COHERENCE_AUDIT_SYSTEM :70-139`;
  `SKELETON_RECONSTRUCTION_SYSTEM :141-162`; `SKELETON_COMPARE_SYSTEM :164-182`; `STRAND_AUDIT_SYSTEM
  :184-204`; `REANCHOR_SWEEP_SYSTEM :206-220`; `DRIFT_ADJUDICATION_SYSTEM :222-264`;
  `REPAIR_SECTION_SYSTEM :266-296`; `DEEP_STRUCTURE_AUDIT_SYSTEM :299-326`; `screen_source_owned
  :406-429`; `finding_fingerprint :473-482`; `plan_digest :489-512`; `independent_reader :519-611`;
  `coherence_audit :614-683`; `navigational_surface :686-714`; `skeleton_reconstruction :717-773`;
  `strand_audit :776-808`; `changed_seams :811-823`; `reanchor_sweep :826-848`;
  `apply_relocation_screen :855-874`; `drift_adjudication :877-968`; `fidelity_findings :971-1029`;
  `select_repairs :1036-1062`; `repair_sections :1065-1156`; `repair_until_clean :1159-1243`.
- `delm/longform/integrity.py` — `AssemblyReport :30-56`; `assemble_with_integrity :72-276`;
  `section_screens :283-322`; `style_deviations :325-336`; `document_screens :344-377`; `audit_copy
  :380-402`.
- `delm/longform/resolve.py` — doctrine `:1-19`; `RESOLUTION_ACTIONS :37`; `is_blocking :56-61`;
  `stale_reason :64-79`; `apply_resolutions :150-352` (go further `:257-322`).
- `delm/longform/orchestrator.py` — `STAGES :64`; `consent_estimate :199-233`; `rewind_run :279-303`;
  `_reader_layer :306-314`; `run_longform :317-938` (read `:455-474`, deep read `:476-488`, cards
  `:490-513`, style `:515-525`, architecture `:527-541`, memo 1 `:543-567`, choice `:569-591`, plan
  `:593-605`, memo 2 `:607-629`, approval `:631-657`, generate `:659-684`, units `:686-697`, retitle
  `:699-709`, assemble `:711-730`, audit `:732-819`, repair `:821-876`, finalize `:878-931`).
- `delm/longform/memo.py` — `what_changed_record :221-353`; `write_memo_letter :359`; `render_memo_v1
  :618-700`.
- `delm/longform/stance.py` — `DIMENSIONS :33-248`; keys `:249-254`; `DEFAULTS :258-263`.
- `delm/longform/tree.py` — `choose_unit_level :619-641`; `_KIND_HINT_RES :649-660`; `Section :694-720`.
- `delm/longform/model.py` — `ModelLayer :232-244`; cache_control `:292`; thinking per call `:338-365`;
  refusal fallback `:423-432`.
- `delm/structural_program.py` — `STRUCTURAL_ARCHITECTURE_SYSTEM :263-330` (the essay-scale parent;
  "a set of timid variations is rejected whole" `:310`); `STRUCTURAL_COHERENCE_REPAIR_ALTERNATIVES_SYSTEM
  :720-760` (three distinct repair variants).
- `delm/deep_structure.py:36-57` — the twelve elements and five tests.
- `data/rule_packs/{structural-lenses,operations-foundations,document-foundations,narrative-foundations}.json`
  — rule ids cited in the prompts.
- `web/longform.html:147-229` (run, choice, approval, finish screens); `web/longform.js:10-20`
  (stages, labels, phases), `:698-700` (resolution radios).
- Git: `444c49a`, `4c7d0b6`, `7709bd8`, `e147e41`, `a6e6deb`, `1c0102f`, `59c227b`, `2379cbe`, `7d48ad6`,
  `3516f74`, `c2a09b1`, `322f469`, `37002ab`, `7d7a5a1`, `9816998`, `15b3cf3`.

The Analyst (`/home/evgeny/projects/the-analyst`, commit `95896c9`):

- `src/dossier/runner.py:22-35` (steps, why); `src/dossier/compose.py:35-59` (schemas), `:61-67`
  (system), `:70-89` (user), `:92-121` (`write_sections`), `:129-217` (`_render_context`, unplaced items
  `:179-189`); `src/dossier/brief.py:50-54`; `src/dossier/plan.py:43-46`; `src/dossier/tables.py:46-51`,
  `:74-123`; `src/dossier/figures.py:39-41`; `src/dossier/llm.py:227-264` (`call_json` re-ask);
  `src/dossier/walls.py:1-60`; `src/dossier/schemas.py:174-194`; `src/dossier/common.py:17-35`.
