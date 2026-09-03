# DESIGN — Concretization passes for The Analyst (text ↔ tables ↔ figures)

> Process analysis, 2026-09-03. Status: DESIGN — nothing here is commissioned;
> the owner's word turns a phase of §D into a commission.
>
> Trigger — the owner, 2026-09-03: *"in Wirecut we really have multiple steps
> of revising things as they become more concrete and as different parts
> concretize; the entire thing gets better. As we need to integrate text and
> images, we need to do it in multiple steps, same with tables. As we have the
> first draft of the text and the image, maybe now that we have the text, the
> image should actually look different; then we have the image, and maybe the
> text should look different. Everything should hang together organically — if
> it doesn't, it's shit."*
>
> Read for this memo (whole files unless noted): Wirecut `CLAUDE.md`,
> `README.md`, `LLM-FIRST-DOCTRINE.md`, `communications/{SCRIPT_FIRST_PROGRAM,
> SIX_LAWS_TRACKER, WORK_ORDER_STRATEGY, SCREENING_ROOM_MEMO, RETRO_LOOP_TRACKER,
> PROMPT_HOW_IT_WORKS_DECK}`, `BUG_TRACKING.md` (pass-related entries),
> `web/src/HowMap.tsx` (the system map), every prompt in `engine/prompts/` named
> below, and the engine modules `spine, telling, screenwriter, storyboard
> (retry driver, walls, generate/redirect/regenerate), pacing, prompt_bench,
> scratch_vo, dailies, screening, targets, workorder, retrospective, loop, ops,
> receipts, truth, acts, iterate, pipeline`; `web/src/steps/ReviewStep.tsx`,
> `web/src/steps/MakeStep.tsx` (Fix everything), `web/src/ScreeningRoom.tsx`.
> The Analyst: `src/dossier/*` (all 15 modules + template), `src/api/routes/
> dossier.py`, `web/src/steps/{DraftStep,DossierStep}.tsx`, and the real run
> `data/dossiers/live-dossier-dce25aeed631/{dossier.md,job.json,figure-*.jpg}`.

---

## A. Wirecut's pass ledger

### A.1 The passes, in the order a film meets them

Column key — **reads**: which earlier records ride the call; **writes**: the
record it leaves; **may revise**: which EARLIER decision it is allowed to
re-open, and the rule; **judge gist**: the prompt's own words (verbatim where
quoted); **wall / law**: what code refuses or enforces (shape/arithmetic/
sequence only — never merit); **retry**: the repair road; **receipt**: the
ledger event(s). File refs are `engine/<module>.py:<line>`.

| # | Pass (where) | Reads | Writes | May revise | Judge gist | Wall / law | Retry | Receipt |
|---|---|---|---|---|---|---|---|---|
| 1 | **The spine** — `spine.generate_spine` :827, `prompts/spine_doctrine.md` | full source, style preset, target length, language, director's notes verbatim; on redirect: the previous spine + the editor's notes | `board.spine` (round n): arc/movements each with an attention plan, motif plant→payoff, color script, hook, closing, promise setup→payoff, pattern interrupts, duration rhythm, approach + runner-up, type mood | nothing earlier. Is itself re-opened by `redirect_spine` :997 (operator notes) → the board goes **stale by arithmetic** (`spine_round_consumed ≠ spine.round`, `spine_stale` :712) | "Your answer — the SPINE — is the one artifact every later judgment consumes: the storyboard executes it beat by beat, the dailies review checks the footage against its color script, the composer reads its musical arc. Plan the film, not the paragraphs." | `validate_spine` :570 — presence, closed enums, authored bounds (2–5 movements, 2–4 phases), unique names (they become enums clips declare); approach window arithmetic; type-accent contrast ≥3:1 | `_call_with_shape_retry` retries=4 with **FIELD patches** (`_spine_patch_trio` :764): only failing fields are re-asked, merged, the whole re-judged | `spine_generated` / `spine_redirected`; `spine_redirect_stored` keeps the old spine in detail |
| 2 | **The telling desk** — `telling.attach_telling` :362, `prompts/telling_desk.md` | the accepted spine + approach contract + source | `spine.telling` (question, handle, whose film, face, opposer, disclosure, held, engine, reveals, ending verdict, controlling idea, charged image, stance) | nothing; declared OVER the accepted spine | "declare THE TELLING — the film's plan for what the viewer knows, feels and wants, beat by beat — in plain words, over the spine's own movements, anchored in the source" | shape + membership (centre/charged image name real movements) | retries=3; **skip law**: failure records `telling_skipped`, "the spine stands, the write never blocks here" | `telling_declared` |
| 3 | **The screenwriter DRAFT** — `screenwriter.write_script` :846, `prompts/screenwriter_doctrine.md` | spine JSON whole (telling included), approach contract, register, director's notes, source; word budget taught upfront | `script` draft: beats (lines, seconds, held_question, answers_beat, movement), time_claims with verbatim anchors, read_notes, myth_holder | nothing earlier; the spine's order is law ("a script may not defect from the plan it was commissioned against") | "write the COMPLETE narration … as ONE continuous spoken piece … Then you cut that finished read into beats … Nobody downstream may rewrite you" | `validate_script` :544 — every wall EXCEPT total length: beat index/seconds/word caps, debt pairing (unpaid question = refused), movement membership + order + coverage, verbatim time-claim anchors; `repair_script_shape` :203 repairs shape trivia by code (split, re-point, drop stale claim) and records it | retries=5; adjudicator for settings collisions; `reconcile_clock` :103 fits seconds to words mechanically | `script_written`, `script_shape_repaired` |
| 4 | **The CUT** — `_cut_to_length` :1171, `prompts/script_cut.md` | the accepted draft only | replacement beats/time_claims/read_notes (approach card carried verbatim) | the draft's words — **deletion only**; debts stay paid; claims re-declared | "CUT. Delete clauses, sentences, adjectives — or drop whole beats … NEVER add new facts, images, quotes, or fresh phrasings" | the FULL walls incl. the length band; error text does the beat arithmetic for the model | retries=6; **adoption law**: the second out-of-band declaration is adopted and recorded (`declared_length_adopted`) unless the operator pinned the length | `script_cut` |
| 5 | **The POLISH** — `_polish_language` :1294, `prompts/script_polish.md` | the settled read | only lines that carry a tell; everything else resent verbatim | words only; "the clock and the debts are SETTLED" | "hunting exactly one disease: MACHINE DICTION … touch only the lines that carry a tell; resend every clean line VERBATIM" | same beat count, seconds/flags identical per beat, words never grow, no beat past its seconds, every time-claim anchor survives | retries=3; **improver, never a gate**: a failing polish is skipped on the record (`script_polish_skipped`) and the unpolished read ships | `script_language_polished` (before/after per beat) |
| 6 | **The LOCK** — `write_script` tail :1150 | — | `script_locked` with debts, claims, repairs, adoption | — | — | — | — | `script_locked` |
| 7 | **The board** — `storyboard._generate_board` :3251 with `script_board_section` :1445 | the LOCKED script, spine, source, preset, register, assets | clips: visual_prompt, provider, durations, continuity in/out, text_layer, movement/color_phase | **may not touch the words**: `stamp_locked_script` :1492 COPIES narration + debt flags onto clips by code ("transcription of a locked artifact is plumbing, not judgment"); the one wall left is the count (one clip per beat) | "The words are WRITTEN; your job is the pictures. Plan EXACTLY one clip per beat, in order: clip N's `narration` is beat N's lines VERBATIM — never rewritten, tightened, or redistributed" | `_validate_storyboard` :2451 (shape, enums, spine membership, `movement_order_errors` :2705 — movements are contiguous runs), `validate_planned_length` band −7/+10%, verbatim chips (dropped after two refusals: "an absent chip is honest, a rewritten one is not") | **clip-scoped PATCH retries** (`_clip_scoped_indexes` :3142): "The board is judged whole; only the failing clips are asked for again"; retry memory is monotone ("a mistake you fixed once must STAY fixed") | `storyboard_generated/_stored`, `unverbatim_chips_dropped`, `declared_length_adopted` |
| 8 | **The pacing editor** — `pacing.run_pacing` :447, `prompts/pacing_pass.md` | the settled plan as lines (narration, seconds, act boundaries, held questions, breathers) | `board.pacing_edges` (sparse seams), breather verdicts, line trims | breather clips (shorten / **remove** via `acts.remove_breather`), narration (**trim only**: new words ≤ old — "the clock is already reconciled"), edges | "You rule on TIME — the seams between clips and the empty seconds the plan spends on them … A well-paced plan changes nothing." | index bounds; act-boundary-only treatments; every breather ruled; trim never grows a line | skip law (`pacing_skipped`) — "the write never blocks on this pass" | `pacing_judged`, `pacing_applied` (trims/shortened/replaced/seams) |
| 9 | **The prompt bench** — `prompt_bench.run_prompt_bench` :331, `prompts/prompt_bench.md` | every clip's narration + visual_prompt, the telling lines, the source | revised `visual_prompt` in place, `seam_notes` (the sentence each doubtful cut implies) | picture prompts only; "You do not touch the narration, the durations, the order of clips or the telling" | "does each prompt describe, or does it merely gesture? … Rewrite whole, keep the skeleton … A clean board changes nothing … an unnecessary rewrite is itself a defect" | facets (SETTING/CAMERA/LIGHTING/AUDIO) and the fixed no-text tail survive; a "revision" identical to the original refused; `clean` ⇒ empty revisions | skip law (`prompt_bench_skipped`); a clean bench leaves the board byte-identical | `prompt_bench_judged`, `_applied` (before/after per clip) / `_clean` |
| 10 | **The table read** — `scratch_vo.review_scratch` :767, `prompts/scratch_review.md` + `script_pass.md` | every line synthesized and MEASURED (free voice), the spine's pace brief, per-beat speech window; the whole narration as one text with on-screen chips | scratch round: per-beat verdict keep/revise_line/revise_delivery/revise_voice/revise_duration (+ ear flags, marks, pronunciation risks); `script_pass` issues (11 species) with `revised_narration`; auto-minted pronunciation rules | durations — applied **by declaration inside the round** ("durations update only by declaration, before render"); lines/delivery/voice — proposals the operator applies one-click (`apply_revision` :1141, `apply_script_revision` :1241) | "does this line, in this voice, at this pace, carry this beat — before the newsroom spends money filming footage to fit it?" / script pass: "you are the first to read the whole thing as one text — the way a viewer will hear it … you leave everything else alone" | shape; duration membership against the provider contract; staleness key `scratch_state` :72 = exact per-clip (narration, voice, delivery, marks, lexicon) | a failed judge is recorded `unavailable` — "no substitute verdict, no automatic retry" | `scratch_round`, `scratch_duration_applied`, `scratch_revision_applied`, `script_revision_applied` |
| 11 | **Grounding check** — `storyboard.review_grounding` :4132, `prompts/grounding_review.md` | source + board | a report per clip: anchored?, evidence, problems; taught-concept glosses; approach checks | nothing — "You report; you do not block. The operator decides what to do." | "is this clip anchored in the source document, or did it drift?" | shape | one re-ask | `review_json` on the board |
| 12 | **Sharpen (line / shot)** — `sharpen_clip_line` :5617, `sharpen_clip_shot` :5826 | the whole source + the whole board (+ frames of the current take for shots) | N variants with a craft note each; **nothing applied** until the operator clicks "Use this line" | one clip's words (or one clip's picture); everything else fixed; stale when the line on the board moved (`SharpenTray` stale flag) | "Read the whole narration as one text before you touch the line: your variants must sound like they were always part of THIS film" | shape; variants must be different MOVES (judge); marks clamped to the words | one re-ask | `clips[i].sharpen` round |
| 13 | **Re-plan one clip** — `regenerate_clip` :4743 | source + the COMPLETE current board + the editor's guidance verbatim | one replacement clip (keeps `beat_id`, voice casting, asset link); the outgoing clip is kept as a version | one slot wholesale; its takes drop ("they described the old plan") | "Re-plan ONLY clip index N … stay inside the established style bible, honor continuity with the neighboring clips" | per-clip walls + spine membership | shape retry | `clip_replan_stored` (old + new clip) |
| 14 | **Harmonize ("smooth the cut")** — `harmonize_board` :6021 | the whole board | rewrites only `visual_prompt`/`continuity_in/out` across clips | pictures + hand-offs, never words | — | the patched board must pass `_validate_storyboard` whole | shape retry | `board_harmonized`, `harmonize_stored` |
| 15 | **Repair desk** — `repair.repair_job` :353, `prompts/rewrite_doctrine.md` | the provider's refusal verbatim, the prompt, the narration | a rewritten visual prompt (`changes_made`, `preserved_elements`) | the picture only: "The narration is untouchable. It is the journalism" | "Read the rejection … Remove or generalize exactly that; don't sand down the whole prompt" | technical elements kept | 3 rewrites, then engine switch | `job` rows + ledger |
| 16 | **Dailies** — `dailies.review_reel` :1171, `prompts/dailies.md` | a contact sheet of REAL frames per clip, style bible, narration, prompt, authored hand-offs, color script, **prior rounds verbatim**, same-plan roll counts, **open targets**, screening signals on paired slots | per clip: style/face/text/content_sane/disposition accept·rerender(+revised_prompt)·replan·cut; per boundary: edit_edge; reel: palette drift, motif, rhythm, reel_coherent; `target_outcomes` (one fate per open target), `what_changed`, insertions | at LOOK: recommendations only; at ITERATE: dispositions EXECUTE inside the cap (`iterate.run_loop`); paired review moves the pointer only by exact take id | "Until now every coherence judgment in this pipeline was made against an imagined film. Yours is the first made against the real one." / "a diagnosed plan is never re-rolled bare" / "Never omit a target: an unanswered contract is how problems slip through builds" | shape, enums, index bounds, fate completeness (`targets.validate_outcomes`), act-treatment placement clamp | a failed judge is recorded `unavailable`; the build then PARKS on the operator (`reel_unjudged`) — "the build does not proceed silently" | dailies round row; `target_minted`; `dailies_skipped` on practice footage |
| 17 | **Text re-fit / re-author** — `textlayer.ensure_text_refit` (sequence gate in `pipeline._assemble_step` :684) | dailies text-zone verdicts, **open TYPE targets quoted verbatim** (BUG 2026-08-07: "the fix never heard the complaint") | on-screen text placement / wording | designed type only | — | verbatim chip walls; bounds law | shape retry | text pass rows (`changed`/`total`) |
| 18 | **Assembly** — `assemble` | takes on file, **the board's current narration** (BUG 2026-07-17: "WORDS follow the board"), edges by precedence (operator > fresh dailies > pacing), music plan | the build (assembly row, manifest, params) | nothing; packages what the record says | — | text-only fast path is arithmetic over the record | — | `assemblies` row |
| 19 | **Screening** — `screening.review_assembly` :976, `prompts/screening.md` | the assembled video (frame strip or `video_native` with sound), a brief with THE AUTHORED PLAN, THE SPINE'S PROMISE, THE TELLING, THE FILM'S BREATH, dwell table, THE DAILIES RECORD, **PRIOR SCREENINGS verbatim**, RECORDED PASSES SINCE, **OPEN PUNCH TARGETS** | punch list (each item: timeline seconds, channel, ONE affordance: refilm/replan/cut/insert/fix_narration/reauthor_text/refit_text/regenerate_music/reassemble/none), `ship_ready`, `what_changed`, `prior_fates` | nothing directly — items become **targets**; a linked item re-aims its target's instrument (`refresh_instruments_from_screening` :294) | "every defect a viewer would actually notice, located in timeline seconds, each mapped to the ONE one-click fix that addresses it … An empty punch list is a legitimate verdict" / "Never close a punch item by silence" / DEFER/DEFY when a better-sensed round closed it | shape + fate completeness; `clamp_punch_targets`; **`clamp_frame_grace`** — a code-known fact overrides the judge's impression ("A judge's verdict that contradicts recorded arithmetic must lose to the record — loudly, with both kept"); the **publish gate** withholds until `ship_ready` or a recorded override (sequence, never content) | recorded `unavailable`; auto-screen after every real build (`maybe_autoscreen` :1229) | `screening_reviews` row, `target_minted`, `target_instrument_updated`, `publish_override` |
| 20 | **Seam ear** — `seam_ear`, `prompts/seam_ear.md` | the COMPLETE mixed audio + recorded cut times, edge treatments, music sections, authored seam intent | per-boundary proposals (type, seconds, pause, music, drop_ambience) with `heard`/`why`/`worth_fixing` | edges only, and only by the operator's apply; "overrule intent knowingly" | "Propose ONLY moves the desk can actually make … never invent a hand that doesn't exist" | shape | — | `seam_reviews` row; `seam_stale` when a newer build exists |
| 21 | **Clip-note dispatch** — `prompts/clip_note_dispatch.md` | the operator's note verbatim + the clips' facts as built | ONE instrument + a draft realization, on the ledger as a target (`origin='clip_note'`) | nothing executes; "The operator's note is sovereign" | "One note, one instrument — the sharpest single cure" | shape; `clip_index` ∈ the note's clips | — | target row; rides the next work order |
| 22 | **Arrival** — `prompts/arrival.md` | incumbent vs the take(s) just bought, the linked complaint verbatim | prefers/reason/answers_complaint/pick_take_id | nothing — "You move nothing" | "Keeping the current take is a legitimate verdict … Answer from the frames, never from the prompt's intentions" | shape | — | arrival verdict on the bench |
| 23 | **The work order** — `workorder.draft` :188 / `realize` :1513 / `execute` :1760 | the open, actionable punch targets; (semi mode) one drafting call realizes each item; at execute: **the target's CURRENT instrument** ("heal-at-execute", BUG 2026-08-30) | `work_orders` row (items, coalesced groups, price); execution steps; the closing screening = **the report card** (fates) | executes exactly the visible list: cut → replan → re-film → paired review (→ one automatic escalation replan→refilm→re-judge) → text re-fit against final footage → music → rebuild → closing screening | — (the drafter's system prompt carries "THE CUT ROOM'S MECHANICS" and the NO SILENT NO-OPS law) | coalescing law (all text items → ONE pass); cap arithmetic before the first submit; zero-change gate before the rebuild; drafted changes validated against the SAME walls the applier enforces | pauses, never silent exits; "every automated loop must name its continuation on FAILURE" | `work_order_drafted/approved/step/reaimed/done` |
| 24 | **The loop position** — `loop.loop_position` :40 | recorded facts only (round, fates, open targets, order status, bench, exports, seam staleness) | stations screen→fix→report→ears→publish + the ONE next action | — | (no model: "No LLM is consulted to say where a film stands") | pure arithmetic | — | — |
| 25 | **The retrospective** — `retrospective.run_retrospective` :350, `prompts/retrospective.md` | the film's WHOLE recorded life (history, take lineages, interventions + outcomes, target ledger, seam listens, builds, money) | trajectory (converging/oscillating/regressing/churning/mixed), intervention audit, 3–7 lessons each with `evidence_refs`, a paragraph for the journalist | nothing — "You execute nothing, select nothing, publish nothing" | "did the interventions actually move toward the goal? … Name what was never re-checked … A lesson without evidence is an opinion; do not write those" | evidence refs must exist in the record; lesson count bounds | retries=2; **autorun** after every build (`maybe_autorun` :420) as its own op; pulled into the next Claude Code session (`scripts/pull_retro_feedback.py`) | `retrospective_stored`, `retrospective_autorun` |

Two mechanical facts about the loop that no row above shows: the desk's **UI**
re-checks "the whole" after a local edit only by **staleness badges**, never by
a heuristic — the scratch round shows `stale` when any clip's narration/voice/
marks moved (`scratch_state`), the spine panel shows `stale` when the round
outran the board, the sharpen tray shows `⚠ stale` when the line on the board
no longer matches the round it sharpened (`ReviewStep.tsx` :1592), the seam
listen is `seam_stale` against a newer build, the work order is `wo_stale`
against a newer build. The operator's one button that re-checks the whole is a
**new judged round** (a table read, a dailies round, a screening), and its
memory (prior rounds + open targets) is what makes it a re-check rather than a
first impression.

### A.2 The principles that make it cohere

1. **Script-first, then distribute.** The disease was named in code before it
   was cured: *"every generative doctrine and every hard wall currently guards
   the picture or repairs the words after the fact; no call ever WRITES the
   narration as one continuous spoken object"* (SCRIPT_FIRST_PROGRAM §0). The
   cure: write the whole read as ONE object, wall it, lock it, and let the next
   pass **distribute** it — *"The words are WRITTEN; your job is the pictures …
   never rewritten, tightened, or redistributed (checked mechanically)"*
   (`script_board_section`). When the board changes, words are not rewritten
   by the board model; they are *stamped by code* onto the clips
   (`stamp_locked_script`), and any re-plan of the whole re-derives the script
   from source + notes (*"the script is derived state … never carried over from
   the old board ('the fix hears the complaint')"*, `redirect_storyboard`).

2. **One pass, one constraint; improvers are never gates.** *"Total-length
   arithmetic is not a writing-time constraint a model can hold"* — so the
   DRAFT clears every wall except length, the clock is fitted by arithmetic,
   the CUT is a single deletion-only task, and the POLISH hunts one disease
   with the clock frozen. Each later pass is allowed to touch strictly less than
   the one before it (draft: everything; cut: delete; polish: substitute; pacing:
   trim; bench: pictures only). A pass that cannot clear its walls is *skipped
   on the record* (`telling_skipped`, `pacing_skipped`, `prompt_bench_skipped`,
   `script_polish_skipped`) — *"the write never blocks here"*.

3. **Walls hold shape, never merit; shape trivia is repaired by code and
   recorded; the retry is a patch, with memory.** *"Walls that trip on SHAPE
   TRIVIA now repair BY CODE instead of refusing — code's sanctioned roles only
   (shape + arithmetic; the words and every judgment stay the model's,
   untouched)"* (`repair_script_shape`). Retries ask only for the failing
   entries and re-judge the merged whole (*"The board is judged whole; only the
   failing clips are asked for again"*, HowMap); the correction carries every
   error ever rejected in the request (*"a mistake you fixed once must STAY
   fixed"*), and every wall *teaches its exit* (*"Blind walls don't converge"*).

4. **Judge → punch list → work order → report card. Code never closes an item
   by silence.** Every judge answers through a typed tool whose items each map
   to ONE one-click affordance; items become durable **targets** with an
   append-only fate history; the next judged round receives the open targets
   and MUST declare a fate for each (*"Never close a punch item by silence — an
   unanswered target stays open, and the record will say so"*); a repair call
   receives the judge's words verbatim (*"If a judge wrote it down and a fix
   button exists, the executing pass must receive the judge's words"*, BUG
   2026-08-07); the work order coalesces items by channel, executes exactly the
   visible list, re-derives each item's instrument at run time (*"never run
   yesterday's verdict silently"*), and ends in a closing round whose fates ARE
   the report card.

5. **The record is the truth; staleness is arithmetic; everything is
   narrated.** *"Facts in → station out"* — the loop position, the publish
   gate, and every stale badge are exact comparisons over recorded rows, never
   a judgment about whether things still fit. Every model call leaves a receipt
   (payload hash, prompt-library manifest, result, cost); every pass emits its
   own status line to the waiting screen (*"the writer is on pass 2"*); the
   operator's edits are sovereign facts (*"WORDS follow the board"*).

6. **The picture is read as a description before a dollar is spent; the
   caption is not the argument.** The prompt bench reads each prompt against
   the grammar of description with the telling in hand (*"does each prompt
   describe, or does it merely gesture?"*), the dailies judge the real frames
   against the words (*"content_sane — read the clip's NARRATION … then look at
   the frames as an ordinary viewer would"*), and the screening names the
   *duplicated channel* (a card that says what the narration says) and the
   *echo accent* as defects. Words and pictures are checked against each other
   twice: once as plans, once as rendered things.

7. **Operator verdicts propagate and outrank; nothing structural executes
   unattended.** Director's notes ride every call verbatim; a spine redirect
   makes the board stale rather than silently regenerating it; one-click
   applies are recorded declarations; *"the click authorizes a visible list,
   never an open mandate"*; a drafted change *"must (a) validate … against the
   SAME walls the applier enforces AND (b) know the change's runtime
   preconditions — 'applies cleanly' is not 'takes effect'"* (BUG 2026-07-29).

8. **Better senses and recorded facts outrank a judge's impression.** *"A
   verdict reached with better senses outranks a re-reading made without them"*
   (DEFER/DEFY); *"any new judge criterion whose ground truth is (sometimes)
   derivable from recorded params: split the criterion — the derivable arm is a
   CODE clamp with the fact quoted; only the residue stays with the judge"*
   (`clamp_frame_grace`).

9. **The retrospective closes the loop across films.** *"You judge the
   TRAJECTORY, not the current cut … Name what was never re-checked"* — it runs
   by itself after every build and its lessons are pulled into the next coding
   session.

---

## B. Where The Analyst's dossier does NOT hang together today

The pipeline today is one forward pass (`src/dossier/runner.py` STEPS):
reconnaissance → brief → plan → analysis → tables → figures → compose →
receipts. No pass reads an earlier artifact *back* against a later one; no pass
reads the finished dossier as one text; the only cross-artifact check is the
anchor wall (verbatim membership). Evidence from the owner's first real run,
`dossier-dce25aeed631` ("When Governments Say 'Strategic,' Follow the Money",
$2.58, 17.2 min):

**B.1 Figures were planned before the text existed, against a rule the plan
ignored.** The brief's `output_shape.figures` (job.json) asked for *"A
corporate beneficiary web showing how state funds flow … to named firms
(Lockheed Martin, Microsoft, Andreessen Horowitz, HMN Tech, BDC)"* and *"A
side-by-side visual: official job-creation headline numbers vs. FTE figures
found in underlying official documents"* — both need names and numbers. The
figure desk's law is *"NO words, letters, logos, charts or labels in the
image"*. The compliance check (`src/images/compliance.py`) then said, of
`jobs_promised_vs_delivered`: *"No numbers or contrasting figures appear on
either plaque — the core visual story (large announced number vs. small FTE
number) is entirely absent"*; of `state_funds_flow_to_firms`: *"Rendered
text/stamps visible on the manila envelopes and folders … Gold bars replace
the expected flow of banknotes"*. Both figures shipped as `status: generated`
with the verdict parked in `note`; nothing re-specified, nothing re-rendered,
and the compose call was told only ``figure `key` (generated): caption`` — the
compliance verdict never reached the writer. Figure 1 (viewed): two podiums, a
blank gold plaque, a clerk with papers — while its caption asserts *"300 jobs
announced, roughly 12 FTE per data centre found in the state's own paperwork"*.

**B.2 Captions are written as arguments, then the prose echoes them (the
duplicated channel).** Figure 3's caption: *"Behind the geopolitical language
of 'strategic assets' and 'network sovereignty' are ordinary industrial workers
whose jobs become bargaining chips. France's nationalisation of Alcatel
Submarine Networks was triggered not by grand strategy alone but by the
immediate threat of the Calais cable-manufacturing plant closing …"*. Section 4,
paragraph 4: *"Behind the geopolitical language of 'strategic assets' and
'network sovereignty,' Abels shows us ordinary industrial workers whose jobs
become bargaining chips. France's nationalisation of ASN was not driven by
grand strategy alone; it was triggered by the immediate threat of the Calais
plant closing."* The writer was handed the caption and wrote around it, so the
reader reads the same sentence twice (three times in Markdown, where the
caption is also the alt text). Figure 1's caption repeats section 1's
300-vs-12 line the same way.

**B.3 Tables are pointed at but not woven in.** Section 3 says *"The table
below decodes the key terms and what each one signals in practice."* — and is
followed by a further paragraph on Alami's 500-year sketch, THEN Table 2,
because the schema places tables *"at the end of this section"*
(`compose.py` :164–177). No section refers to a table by number ("Table 2")
because numbers are assigned at render time. Sections 2, 4 and 5 carry no
table; section 5 — the "Implications for Luxury" that the executive audience is
paying for — carries neither table nor figure. Only 2 tables survived the wall
after a re-ask (the tables step cost $0.67 — second only to analysis).

**B.4 Anchors that pass the wall but do not support the claim (the inverse of
"the judge blessed a mechanically-known defect": here code blessed what only a
judge can check).** The trim-to-a-verified-prefix wall (`walls.verify_anchor`
:62) produced footnotes such as `[^13]` *"France's efforts to maintain a
balanced stance are also"* (anchoring "France still constrained by US
sanctions…"), `[^17]` *"Despite being regulated by national legislation and
priorities, and having over 100"*, `[^31]` *"the Minister for Digital
Governance, Dimitris Papastergiou, recently convened with"* (anchoring
"due-diligence windows compress"), `[^34]` *"These training projects,
therefore, risk limiting"*, `[^42]` *"reports in the business press of the US
pressuring 'connector"*; and `[^20]` anchors the cell *"No domestic community
promise stated — security framing required none"* with a quote about *China*
aiming to capture 60% of the market. Six of 43 anchors are fragments; the
appendix line reads "Walls: 10 table rows kept, 0 dropped".

**B.5 Rows and claims do not share a spine.** Table 1 is keyed by "five cases"
(one of them "US / SeaMeWe-6", the second row drawn from Abels; Alami supplies
none) while the summary's "five cases" list and the reconnaissance's five
*documents* are different sets; section 1's claims are keyed by document
quotes. Tables, figures and sections each re-derived "the pattern" from 60K
chars of analysis prose independently (`tables._user`, `figures.plan_figures`,
`compose._user` all read `analysis_prose(job)`), so their granularity
disagrees by construction.

**B.6 The summary and the conclusion do the same job.** Three paragraphs each,
same three moves (pattern → "not accidental" → luxury implication); "6. What
this means" restates section 5. No pass ever read the dossier as one text
(Wirecut's `script_pass` species *tic*, *register*, *capsule_rhythm* have no
counterpart), and no pass judged executive usefulness.

**B.7 The figure count came from a dial, not from the argument.**
`options.output.figures = 3` while the brief planned 2 ideas; the third figure
(`calais_plant_workers`) was invented from the prose, then placed in section 4
with the echo in B.2. The analysis itself is organized per document ("Document
1 … Document 5"), the dossier per pattern — a legitimate transformation that
nothing checks.

**B.8 Process facts.** Compliance verdicts are recorded and ignored; the anchor
wall is the only cross-artifact law; there is no staleness, no targets ledger,
no work order, no way to re-check the whole after an edit, and the desk
(`DossierStep.tsx`, 99 lines) offers the finished HTML, downloads and receipts
— no per-item action at all.

---

## C. The design — a concretization loop for text ↔ tables ↔ figures

### C.0 The shape of it

```
reconnaissance → brief → plan → analysis
   → SPINE        (what the dossier argues: sections, ONE claim each, the exhibits each claim needs)
   → EXHIBITS     (tables and figure specs derived FROM the spine; figures rendered + checked)
   → DRAFT        (the text written WITH the exhibits on the desk, referencing them by key)
   → CROSS-CHECK  (judge: does each figure depict what its section argues? do the rows match the claims?
                   is anything asserted that no table/figure/anchor backs? → findings with ONE affordance each)
   → REVISE       (work order: revise figure spec + re-render / rewrite section / add·drop rows / re-anchor;
                   exhibits first, then text against the final exhibits; re-render only what changed)
   → READ-THROUGH (judge: coherence, redundancy, register, executive usefulness → line edits under walls)
   → compose (render) → receipts (+ optional retrospective)
```

The mapping to Wirecut's principles: SPINE is the script-first move (the
argument is written as ONE object before any exhibit exists, and later passes
*distribute* it); EXHIBITS and DRAFT are the board and the assembly (they
consume the spine verbatim and must reference it by key — membership walls,
never re-litigation); CROSS-CHECK is dailies + screening (the first judgment
made against the *real* rendered things, with a punch list and a target
ledger); REVISE is the work order (coalescing law, exhibits-then-text order,
zero-change gate, report card); READ-THROUGH is the table read's whole-script
pass + polish (an improver under frozen walls, never a gate). The skip law
holds for every new pass: a failed judge records `<pass>_unavailable` and the
run proceeds; a failed improver records `<pass>_skipped` and the unimproved
artifact ships.

**Budget (medium depth):** three new judged/planning calls (spine, cross-check,
read-through) ≈ $0.15 + $0.30 + $0.20, plus a revision round of at most 2
targeted calls + 1 figure re-render ≈ $0.40. Net **≈ +$1.0, +5 min** on the
$2.58 / 17 min baseline. The existing tables, figure-plan and compose calls
change their inputs but not their count.

**By depth:** `simple` — SPINE on (it is the load-bearing change and cheap),
CROSS-CHECK on but with **revision budget 0** (findings are recorded and shown
on the desk as a punch list; nothing executes), READ-THROUGH off. `medium` —
all on; one revision round (≤ 2 rewrite calls, ≤ 1 re-render). `advanced` —
two revision rounds and a second cross-check after the first round (the report
card, with fates).

### C.1 Pass S — THE SPINE (`src/dossier/spine.py`, new)

**Purpose.** Decide what the dossier argues before a word of it is written, and
what each section needs on the desk to prove its claim — so tables and figures
are *derived from* the argument instead of guessed from the prose in parallel.
The brief's `output_shape` stops being the authority and becomes advisory
input (the difference is recorded).

**Inputs.** Chosen brief option (title, telling, output_shape), the analysis
prose (every phase, ≤ 80K chars each as today), the reconnaissance profiles
with their verified anchors, the audience register, `options.output` (table/
figure budget), intent.

**Output schema (`DossierSpine`, `schemas.py`).**

```
DossierSpine {
  round: int,                                  # 1; +1 on every redirect (arithmetic)
  thesis: str,                                 # ONE sentence — the dossier's claim
  reader_question: str,                        # what this audience needs answered
  handle: str,                                 # the dossier in one line a reader can repeat
  through_line: str,                           # the object/example that returns (Wirecut's motif)
  summary_job: str, conclusion_job: str,       # what the summary does vs what the close does — different jobs
  sections: [ {
     key: str (snake_case, unique), heading: str,
     claim: str,                               # ONE sentence this section proves
     evidence_kind: enum(case_comparison | mechanism | vocabulary | cost_ledger | chronology | implication),
     table: null | { intent: str,              # what rows × columns would PROVE the claim
                     row_unit: str,            # "one row = one case / one term / one actor"
                     columns: [str] },
     figure: null | { picture_shows: str,      # a depictable scene WITHOUT text or numbers
                      caption_says: str,       # ≤ 2 sentences; what the reader is to take from it
                      why_a_picture: str },    # why prose/table cannot do this job
     anchors_planned: [ {doc_key, quote} ],    # 2–4 verified quotes this section will lean on
     feeds: [section_key]                      # which later section builds on this one
  } ],
  exhibits_budget: { tables: int, figures: int }
}
```

**Judge prompt (draft, `prompts/dossier_spine.md`).**

> You are the structure editor of The Analyst. The analysis is done and nothing
> of the dossier is written. Before a word is written you decide what the
> dossier ARGUES and what each part of it needs on the desk to prove its point.
> Your answer — the SPINE — is the one artifact every later desk consumes: the
> tables desk builds exactly the tables you specify, the figures desk draws
> exactly the pictures you specify, the writer proves exactly the claims you
> name, in your order, and the cross-check judges the finished dossier against
> your words. Plan the argument, not the paragraphs.
>
> — One claim per section. A section that proves two things is two sections;
> a section that proves none is cut. Write the claim as the sentence a reader
> would repeat.
> — An exhibit is commissioned by a claim, never by a dial. Ask for a table
> only where a row set PROVES the claim (say what one row is); ask for a
> picture only where a picture does a job prose and tables cannot (a place, a
> material, a scale, a contrast the reader must SEE) — and say in
> `picture_shows` only what an image model can render without a single word,
> number, label or logo. The caption is not the argument: `caption_says` tells
> the reader what to take from the picture in at most two sentences and never
> carries a number — numbers live in the prose and the tables.
> — The exhibits budget is a ceiling, not a target: fewer, load-bearing exhibits
> beat the budget filled.
> — Ground everything: every section names 2–4 verified quotes from the
> reconnaissance it will lean on; a claim the documents cannot carry is not
> planned. Write in the audience's register; for an executive the last section
> is the one they act on — give it the strongest exhibit, not none.
> — The summary and the conclusion do DIFFERENT jobs; declare each in one line
> (e.g. summary = the finding and the stakes; conclusion = the decision rule
> and the question to ask). A close that restates the summary is a defect.
> — When THE PREVIOUS SPINE and THE EDITOR'S NOTES ride the request, honor the
> notes; keep what they do not touch.

**Walls (code, shape only).** 3–7 sections; unique keys; `claim` non-empty
single sentence (one terminal punctuation — arithmetic); Σ tables ≤ budget, Σ
figures ≤ budget; `caption_says` carries **no digit runs** (the caption-number
law — numbers are the prose's and the tables' job); `anchors_planned` pass the
anchor wall (membership; a fragment-trim is refused here, not accepted — see
C.4's anchor law); `feeds` name existing keys. Retry: `_call_with_shape_retry`
pattern with FIELD patches (only `sections[k]` entries that failed are
re-asked; merged whole re-validated) — port of `spine._spine_patch_trio`.

**May revise.** Nothing earlier. Is itself re-opened only by the operator's
redirect (`POST /jobs/{id}/spine/redirect` with notes → round n+1); every
later artifact records `spine_round_consumed` and goes stale by arithmetic.

**Cost / latency.** ~60K chars in (analysis abridged + profiles), ~3K out:
≈ $0.12–0.18, 45–70 s.

**Console / desk.** Narration: *"Deciding what the dossier argues — 5 sections,
each with one claim; 2 tables and 2 pictures commissioned by the argument."*
Artifact `kind: spine` (sections: key, claim, exhibits planned). Desk: a
"Plan" drawer listing each section's claim and its exhibits, a redirect-notes
box priced at one call, a `stale` badge on exhibits/draft when the round moved.

### C.2 Pass E — EXHIBITS (tables + figure specs FROM the spine; `tables.py`, `figures.py` amended)

**Purpose.** Build exactly the exhibits the spine commissioned, keyed to the
sections that need them, with the rendered figure judged against its own spec
and the verdict kept as a *target*, not a note.

**E1 Tables (`tables.run_tables`).** The prompt is spine-driven: for every
section with a `table`, the call receives the section's claim, `table.intent`,
`row_unit`, `columns`, its planned anchors, the analysis prose and the corpus
(as today). Output schema adds `section_key` (required, enum of the spine's
table-bearing sections) and `proves` (one sentence: what the row set shows
about the claim). Walls: existing anchor wall per row; `section_key`
membership; at most one table per section; **skip law per exhibit** — a table
whose rows fall below `MIN_ROWS` records `table_unavailable {section_key,
failed_quotes}` and the section proceeds without it (today the whole step
re-asks and then gives up silently on `tables_short`). Re-ask once with the
failed quotes, as today.

**E2 Figure specs (`figures.plan_figures`).** No longer "plan N figures from
the prose": for every section with a `figure`, one brief per spec — inputs
are `picture_shows`, `caption_says`, `why_a_picture`, the section's claim and
the audience. Output adds `section_key`; `caption` must equal (or only tighten)
`caption_says`; `scene` elaborates `picture_shows`. Walls: `section_key`
membership; the caption-number law (no digit runs); `scene` non-empty.

**E3 Render + check (`figures._generate_one`).** As today, plus: the
compliance verdict becomes a **finding** on the job's ledger (`kind:
figure_depicts_other`, `where: {figure_key, section_key}`, `problem: issues
verbatim`, `desired_change: recommendation verbatim`, `affordance:
rerender_figure` when the recommendation is a prompt change, `revise_figure_spec`
when the check says the core story is absent). At medium+, **the intervention
ladder**: one automatic re-render with the recommendation folded into the
prompt (recorded as `figure_rerendered {before_prompt, after_prompt,
compliance_before, compliance_after}`); the second verdict stands. A figure is
never "generated and forgotten": `status` gains `checked_ok: bool`, and the
`detected` sentence ("what the image actually shows") is kept — it is what the
writer will be handed.

**Cost / latency.** Tables as today (≈ $0.35–0.65); figure plan smaller than
today (specs, not ideas: ≈ $0.03); renders as today (+ ≤ 1 re-render ≈ $0.13).

**Console / desk.** *"Building the exhibits the argument asked for — Table 1
for section 1 (5 rows verified), picture for section 4: checked — 2 issues,
redrawing once."* Artifacts: `table` (with `section_key`, `proves`), `figure`
(with `detected`, `checked_ok`), `figure_rerendered`. Desk: exhibits listed
under their section; a picture-check chip (green / the issues).

### C.3 Pass D — THE DRAFT (text written WITH the exhibits in hand; `compose.write_sections` amended)

**Purpose.** Write the dossier as a proof of the spine, with the finished
exhibits on the desk — every table's rows, every figure's *actual* content —
so the prose can point at them exactly and never restate them.

**Inputs.** The spine (whole), the tables in full (every cell + its anchor,
not the first column as today), the figures with `caption`, `picture_shows`,
`detected` (what the picture actually shows) and `checked_ok`, the analysis
prose, the profiles, the corpus (as today), the audience register.

**Output schema (`Sections`, amended).** `sections[k].section_key` (required;
must equal the spine's keys in the spine's order), paragraphs carrying
placement tokens `[[table:key]]` / `[[figure:key]]` at the sentence where the
reader should look (the renderer places the exhibit THERE, not at the section's
end), `exhibit_refs: [{key, sentence}]` (the sentence that names what the
reader will see: "Table 2 decodes the five terms…"), `claims` as today,
`summary`, `conclusion`, plus `summary_job_met` / `conclusion_job_met` (one
line each — what the summary and the close did, judged later against the
spine's declaration).

**Prompt additions (system).**

> You write with the exhibits ON THE DESK. Each table is given whole; each
> picture is given as what it ACTUALLY shows (the checked description), not as
> what it was meant to show. Prove each section's claim in the spine's order.
> Point at an exhibit exactly once, where the reader should look, with the
> token `[[table:key]]` or `[[figure:key]]` placed right after the sentence
> that says what they will see ("As Table 2 shows, every term does one job")
> — the desk numbers the exhibits for you. Never restate a caption or a
> table's note in the prose; never put in a caption what the prose says; put
> numbers in the prose and the tables, never in captions. If a picture does
> not show what the section argues, do not pretend it does — say what it does
> show and flag it in `exhibit_refs` with `mismatch: true`; the cross-check
> will act on it. The summary and the conclusion have the jobs the spine
> declared; write each to its job and nothing else.

**Walls.** `section_key` sequence equals the spine's (membership + order —
the movement-order wall); every table and figure key referenced by exactly one
token (a forgotten exhibit is refused, not dumped into the last section as
today); the anchor wall on claims as today; **anchor law amended** (see C.4):
a trimmed anchor is *recorded* `trimmed: true` but no longer counts as
verified for a claim — the claim stays, unfootnoted, and becomes a finding
candidate. Retry: **section-scoped patch retries** ("section {key}: …" errors
→ resend only those sections; merged whole re-validated) — port of
`storyboard._clip_scoped_indexes` / `_board_patch_tool` / `_board_patch_merge`.

**May revise.** Nothing earlier; it may *flag* an exhibit (`mismatch: true`).

**Cost / latency.** As today's compose (≈ $0.35–0.45, ~2 min); the fuller
table input adds ~2K tokens.

**Console / desk.** *"Writing the dossier with the exhibits on the desk —
section 3 of 5, pointing at Table 2."* Artifact `draft` (sections with
exhibit_refs, mismatches flagged).

### C.4 Pass X — THE CROSS-CHECK (`src/dossier/crosscheck.py`, new; the judge)

**Purpose.** The first judgment made against the *real* things: the draft
text, the actual table rows, the rendered pictures — read together as one
dossier. It answers the owner's three questions verbatim: does each figure
depict what its section argues? does each table's row set match the section's
claims? is anything asserted that no table, figure or anchor backs? — and it
delivers a punch list where every item maps to ONE one-click fix.

**Inputs.** The spine; the draft (sections with tokens and claims); the tables
in full; the figures — caption, `picture_shows`, `detected`, compliance issues,
and **the rendered image as a vision input** (medium+; text-only at simple);
the anchor list with the sentence each anchors (footnote number, quote, doc,
the claim text); the audience register; on a re-check: **prior findings and
their fates**, and the passes recorded since (exhibits-first order, what
changed).

**Output schema (`CrossCheckVerdict`).**

```
CrossCheckVerdict {
  hangs_together: bool,
  summary: str,                                   # 2–3 sentences, executive-readable, verdict first
  findings: [ {
     id: str,
     kind: enum(figure_depicts_other | caption_restates_text | caption_carries_number |
                table_rows_off_claim | table_unreferenced | exhibit_pointer_wrong |
                claim_unbacked | anchor_fragment | anchor_off_claim | number_drift |
                section_off_spine | redundant_summary_conclusion | register_break |
                jargon_unglossed | exhibit_missing_where_claim_needs_one),
     where: { section_key?, table_key?, figure_key?, paragraph_index?, anchor_n? },
     quote: str,                                  # the offending words, verbatim from the draft/caption/cell
     note: str,                                   # plain language for the desk: effect on the reader, then the cure
     affordance: enum(revise_figure_spec | rerender_figure | drop_figure |
                      rewrite_section | rewrite_paragraph | revise_table_rows | add_table | drop_table |
                      reanchor_claim | drop_anchor | rewrite_caption | merge_summary_conclusion | none),
     realization: str | null,                     # the drafted change: new caption / scene, replacement paragraph,
                                                  # rows to add or drop, the sentence to re-anchor and to what
     recommended: bool,
     target_id: str | null                        # links a standing finding on a re-check
  } ],
  prior_fates: [ { target_id, fate: enum(resolved | persists | regressed | superseded), rationale } ],
  what_changed: str | null                        # required when priors exist
}
```

**Judge prompt (draft, `prompts/dossier_crosscheck.md`).**

> You are the cross-check desk of The Analyst — the first reader who sees the
> dossier the way its reader will: the text, the tables with their rows, and
> the pictures as actually drawn, all at once, against the spine the desk
> planned. Until now every desk worked on one part. You judge whether the parts
> hang together. Judge only what is on the page; answer through the
> `crosscheck_verdict` tool, nothing else.
>
> Read the spine first. Then, section by section, ask:
> — **Does each picture depict what its section argues?** Compare the image you
> are shown (and the checked description) with the section's claim and the
> caption. A picture that shows a blank plaque under a caption about "300 jobs
> vs 12 FTE" depicts something else — `figure_depicts_other`. Decide the cure
> honestly: when a better SCENE would carry the claim without words, numbers
> or labels, draft it (`revise_figure_spec`, realization = the new
> `picture_shows` + `caption_says`); when the plan is right and the render
> missed it, `rerender_figure`; when no picture can do this job, `drop_figure`
> and say what the prose should carry instead.
> — **Does each table's row set match the section's claims?** One row = the
> unit the spine named; rows that argue a different thing, a claim in the prose
> that the table beside it contradicts or does not contain, a table no sentence
> points at (`table_unreferenced`), a pointer that says "the table below" where
> the table is not (`exhibit_pointer_wrong`) — name them. Cures: `revise_table_rows`
> (realization = rows to add/drop, in the table's own columns), `add_table` (the
> spine's intent for a section that argues by comparison and has none),
> `drop_table`.
> — **Is anything asserted that nothing backs?** A sentence stating a fact,
> number, name or causal claim with no anchor, no table cell and no figure
> behind it is `claim_unbacked`. An anchor that is a cut-off fragment ("France's
> efforts to maintain a balanced stance are also") is `anchor_fragment`; an
> anchor whose quote does not support the sentence it footnotes (a quote about
> China under a claim about the United States) is `anchor_off_claim`. A number
> that differs between the prose, a cell and a caption is `number_drift`. Cures:
> `reanchor_claim` (realization = the sentence and the passage that actually
> supports it, verbatim from the documents), `drop_anchor`, `rewrite_paragraph`.
> — **Does the prose say what the exhibit already says?** A paragraph that
> restates a caption or a table note is `caption_restates_text`; a caption that
> carries the argument (numbers, causes) is `caption_carries_number` /
> `rewrite_caption`. The picture carries what the reader must SEE; the caption
> says what to take from it; the prose argues.
> — **The whole.** A section that proves something other than its spine claim
> is `section_off_spine`; a conclusion that restates the summary is
> `redundant_summary_conclusion` (`merge_summary_conclusion` or
> `rewrite_section`); a load-bearing term the audience is never told the
> meaning of is `jargon_unglossed`; a register break is `register_break`.
>
> Laws: quote the offending words verbatim — the desk checks that they are on
> the page. One finding, one cure — the sharpest single instrument. Draft the
> realization for every cure that rewrites something; the desk applies it under
> the same walls the original desk obeyed. Be concrete and unsparing; do not
> pad the list to look thorough, and do not swallow a real problem to be
> polite. A dossier that hangs together gets `hangs_together: true` and an
> empty list — that is a legitimate and common verdict.
>
> Your memory: when prior findings ride the request you are the same desk on a
> revised dossier. Declare one fate per standing finding (resolved / persists /
> regressed / superseded — say why), link a repeat to its `target_id`, and say
> in `what_changed` what actually moved. Never close a finding by silence.
>
> The register: your reader is an executive's analyst with no view of this
> system's insides. Name sections and exhibits as the page shows them ("section
> 3", "Table 2", "the picture in section 4"); name the problem by its effect on
> the reader, then the plain cure; no pass names, no keys in prose.

**Walls.** Shape and enums; `where` references exist (membership); `quote`
appears verbatim in the named section/caption/cell (membership over the draft —
the judge's evidence must be on the page); `realization` required for every
rewrite/re-spec/re-anchor affordance; a `reanchor_claim` realization's passage
passes the anchor wall; findings ≤ 20; `prior_fates` complete when priors
exist (`validate_outcomes` port). **Code clamps that outrank the judge** (the
`clamp_frame_grace` law): an anchor the wall recorded `trimmed: true` is a
finding by arithmetic whether or not the judge named it (`anchor_fragment`,
quoted fact first, the judge's impression kept after it); a caption containing
a digit run is `caption_carries_number` by arithmetic; a table key with no
placement token is `table_unreferenced` by arithmetic; a figure with
`checked_ok: false` and no finding from the judge gets one minted from the
compliance issues.

**Ledger.** Findings become **targets** (`findings_json` on the job; id,
kind, where, problem = note verbatim, desired change = realization, fates
append-only). Open until a later cross-check declares `resolved` or
`superseded`. Code never infers resolution from absence.

**May revise.** Nothing itself. It drafts the work order (C.5).

**Cost / latency.** ~35–45K tokens in (draft + tables + specs + 2–3 images),
~3K out: ≈ $0.25–0.35, 60–90 s. Recorded `crosscheck_unavailable` on failure;
the run proceeds to compose with the fact on the record and the desk's
"Re-check" button lit.

**Console / desk.** *"Reading the dossier as one thing — do the pictures show
what the text argues? 4 findings: the picture in section 1 shows a blank
plaque, Table 2 is pointed at a paragraph early, two anchors are fragments."*
Artifact `crosscheck` (summary, findings count by kind). Desk: the punch list
(one row per finding: where · effect · cure · price · [Fix] [Skip]), a
"Fix everything ($x)" button, the `hangs_together` chip.

### C.5 Pass R — REVISE (`src/dossier/revise.py`, new; the work order executor — mechanics)

**Purpose.** Act on the cross-check at one recorded click (autopilot) or after
the operator ticks the list (desk), in the order that keeps the whole
coherent: **exhibits first, then text against the final exhibits**, then a
render of only what changed.

**Draft (arithmetic, no model).** From open, recommended findings: line items
`{target_id, affordance, where, realization, price}`; **coalescing law** —
all `rewrite_paragraph`/`rewrite_section`/`reanchor_claim` items on ONE section
→ ONE section rewrite call carrying every finding's words verbatim ("the fix
hears the complaint"); `revise_figure_spec` + `rerender_figure` on one figure →
one re-spec (when a realization exists it is applied as a board write, no
call) + one render + check; `revise_table_rows`/`add_table`/`drop_table` on one
table → one scoped tables call; `drop_anchor`/`drop_figure`/`drop_table`/
`rewrite_caption` with a realization → mechanical board writes under the walls
(no call). `none` items are advisory and never enter. Price from the receipts'
own arithmetic (`estimate_engine_run`); cap-gated against `spend_cap_usd`
before the first call; the medium budget is ≤ 2 rewrite calls + ≤ 1 render
(extra items stay open on the desk with their price).

**Execute (sequence).**
1. Exhibits: figure re-spec → render → compliance (finding re-checked by the
   check's `detected`); table row revisions through `tables.revise_rows`
   (the section's claim + the finding + the rows to add/drop; the anchor wall
   as ever); drops applied.
2. Text: per-section rewrite through `compose.rewrite_section(section_key,
   findings)` — the whole dossier, the spine and the (now final) exhibits in
   context; only that section's paragraphs/claims/exhibit_refs may change;
   the section-scoped walls apply; an operator-authored paragraph is
   untouchable (C.7).
3. **Zero-change gate**: if no board write happened, skip the re-render and
   say so ("the batch changed nothing — the findings stay open").
4. Render (compose) — only figure files that changed are re-written; the
   document is re-rendered always ($0).
5. Report card (advanced, or on the desk's "Re-check"): a second cross-check
   with priors → fates; the batch's result line is the fates line ("bought 3
   resolved, 1 persists").

**Walls.** Every realization is applied through the SAME walls its artifact
was born under (anchor wall, section-key/order wall, caption-number law,
token-once law) — "a drafted change that cannot take effect is the same bug
as a silent no-op". Pauses, never silent exits: a failed step records
`revision_step_failed` with the continuation named (re-run / fix by hand).

**Cost / latency.** Bounded by the round budget: ≤ 2 × ~$0.15 + ~$0.13 ≈
$0.45, ~2–3 min at medium.

**Console / desk.** *"Fixing what the cross-check found: redrawing the picture
in section 1 from a new scene, rewriting section 3 around Table 2, dropping
two fragment anchors."* Events `revision_drafted/approved/step/done`; the desk
shows the order (ticks, prices, the coalescing honestly: "one rewrite answers
these 3 items").

### C.6 Pass T — THE READ-THROUGH (`src/dossier/readthrough.py`, new; the final judge, an improver)

**Purpose.** Read the finished dossier once, start to finish, the way the
executive will — and tighten the lines that need it without touching the
structure, the exhibits or the anchors. Wirecut's whole-script pass and polish,
for prose.

**Inputs.** The rendered Markdown (what the reader sees: headings, prose with
footnote marks, tables, captions, table notes, the summary and the close), the
spine's thesis and job declarations, the audience register.

**Output schema (`ReadThroughVerdict`).**

```
ReadThroughVerdict {
  ready: bool,
  summary: str,
  executive_usefulness: { verdict: enum(usable_as_is | usable_with_edits | not_yet), note: str },
  line_edits: [ { section_key, paragraph_index,
                  before: str,                   # verbatim, one sentence or clause on the page
                  after: str,
                  kind: enum(redundancy | register | slop_tell | jargon | pointer | transition | tic) } ],
  structural: [ { kind: enum(section_order | missing_so_what | over_long | under_evidenced), note: str } ]
}
```

**Judge prompt (draft, `prompts/dossier_readthrough.md`).**

> You are the copy chief of The Analyst, reading the finished dossier once, as
> its reader will. The argument is settled, the exhibits are placed, the
> anchors are verified — you are not here to re-plan or re-prove anything. You
> hunt exactly these species and leave everything else alone:
> — **redundancy**: a sentence that says what a caption, a table note, the
> summary or an earlier paragraph already said; the close that restates the
> summary;
> — **register**: a paragraph whose voice breaks the audience's register
> (lecturing, theory jargon, hedging where a decision is wanted);
> — **slop_tell**: the negation frame ("this is not X — it is Y"), the
> totalizing flourish ("the whole story", "everything changed"), throat-clearing
> ("crucially", "in fact"), the fake aphorism at the close, "not only… but also"
> as filler;
> — **jargon**: a load-bearing term the reader is never told the meaning of;
> — **pointer**: a sentence that points at an exhibit that is not where it says
> ("the table below"), or that names an exhibit's content wrongly;
> — **transition / tic**: three paragraphs opening the same way, a section that
> starts without picking up what the last one left.
> For each: `before` verbatim from the page, `after` the replacement — same
> facts, same footnote marks, no new numbers, no new claims; polish by
> substitution and deletion, never growth. Most paragraphs in a good dossier are
> clean; touching three to eight lines is a typical pass; touching none is a
> legal answer. Structural complaints (a section in the wrong place, a missing
> "so what", a section twice too long) are NOT line edits — put them in
> `structural` for the desk. Then say, as the executive's analyst would at the
> door: usable as is, usable with these edits, or not yet — and why in one
> sentence.

**Walls.** `before` appears verbatim in the named paragraph (membership);
`after` carries every footnote mark `{{n}}` that `before` carried and no new
ones (membership); `after` introduces no digit run absent from `before`
(arithmetic — no new numbers); total words never grow beyond +2% (arithmetic);
≤ 12 edits. Applied by substitution; `structural` items become open targets on
the desk, never auto-executed. Skip law: a failing pass records
`readthrough_skipped`; the unpolished dossier ships.

**Cost / latency.** ~25K tokens in, ~2K out: ≈ $0.15–0.20, ~45 s.

**Console / desk.** *"Reading it once through as the executive will — 6 lines
tightened; usable as is."* Artifact `readthrough` (usefulness verdict, edits
count). Desk: a diff drawer (before → after per edit, each revertible), the
usefulness chip on the cover.

### C.7 The desk loop — "Fix everything" for a dossier, and how edits propagate

The rule from Wirecut, kept whole: *per-item instruments + one whole-dossier
re-check*, everything recorded, nothing structural unattended.

**Per item (desk actions; each priced before the click).**
- **Sharpen a paragraph** (`POST /jobs/{id}/sections/{key}/paragraphs/{i}/sharpen`):
  three variants built on different MOVES (scene first / number first /
  decision first), the whole dossier and the spine in context, facts fixed,
  footnote marks preserved (wall); nothing applied until "Use this one"
  (recorded). Stale when the paragraph on the job moved.
- **Regenerate a section** (`…/sections/{key}/regenerate` with guidance):
  re-plan ONE section against its spine claim with the whole dossier in
  context; the outgoing section kept as a version (`section_versions`).
- **Re-spec a figure** (`…/figures/{key}/respec` with a note): a new
  `picture_shows`/`caption_says` under the caption-number law → render →
  check; the old file kept; the finding (if any) linked.
- **Re-derive a table** (`…/tables/{key}/revise` with a note): scoped tables
  call, anchor wall.
- **Cut / insert an exhibit**: drop a figure/table (mechanical, recorded, the
  pointer sentence flagged for the next re-check); insert a table into
  section k from a one-line brief (one scoped call).
- **Edit in place** (`PUT …/sections/{key}`): the operator's paragraph or
  caption edit is written through the same walls (anchor marks must still
  resolve; caption-number law) and stamped `authored_by: operator`.

**The whole.** After ANY change, the cover shows `re-check owed` (arithmetic:
the latest cross-check predates the latest write); **"Re-check the whole"** runs
a cross-check with priors → fates; **"Fix everything ($x)"** drafts the work
order from the open recommended findings, shows the list and the price, and
executes on one click (the fast mode); ticking/untucking and editing
realizations is the semi mode (the same order object read at a different level
of attention). The loop strip on the cover is pure arithmetic over the record:
`draft → check → fix → report → read-through → deliver`.

**Propagation of operator edits (all mechanical).**
- A paragraph or caption marked `authored_by: operator` is **sovereign**: the
  read-through skips it, a section rewrite may not replace it (the wall refuses
  a realization that touches it; the desk says so), a re-check may still flag it
  (advisory, `none`).
- A spine redirect (notes) bumps the round; exhibits and the draft show
  `stale`; "Apply the new plan" rebuilds only what the round changed —
  per-section **claim equality** (exact string) decides whether a section's
  exhibits and text are kept or rebuilt (the `spine_round_consumed` /
  `scratch_state` idiom).
- A figure re-spec makes its section's pointer sentence and the last
  cross-check stale; a table revision does the same; the cover says which.
- Every apply is a ledger event with before/after; the receipts price every
  call; the job's `findings` carry the fates.

### C.8 Determinism ledger (per the LLM-first doctrine — every mechanism, classified)

- Spine/section/exhibit schemas, key uniqueness, section order equality,
  exhibit-token-once, caption-no-digits, anchor membership, `quote`-on-page,
  fate completeness — **shape**.
- Spine before exhibits before draft before cross-check before revise before
  read-through; publish (render) never waits on a judge; skip law per pass —
  **sequence**.
- Rounds, `spine_round_consumed`, per-section claim equality, `re-check owed`
  (latest check < latest write), zero-change gate, budgets and caps, prices,
  receipts, the loop strip — **arithmetic / truth**.
- Findings minted from judge verdicts, fates recorded as declared, operator
  applies and `authored_by` stamps, `figure_rerendered` records — **lifecycle
  recording**.
- Code clamps (a `trimmed` anchor is a finding; a caption digit is a finding;
  an unplaced table is a finding; a failed picture check is a finding) quote a
  recorded fact and keep the judge's impression beside it — **arithmetic that
  outranks impression**, the `clamp_frame_grace` precedent. Nothing here scores
  prose, ranks exhibits, or decides "good enough".

---

## D. Implementation map (in order; smallest viable first)

Every phase ships alone, with a $0 gate (fake transport, fixtures) in the
style of `tests/test_dossier_tables_wall.py`, and the CHANGELOG/FEATURES
entries. File paths are absolute under `/home/evgeny/projects/the-analyst/`.

**Phase 0 — the smallest viable version (one session): the spine, exhibits
from it, the draft with exhibits in hand, placement at the pointer.**
1. `src/dossier/schemas.py` — add `DossierSpine` (+ `SpineSection`,
   `TableSpec`, `FigureSpec`); `Table.section_key`, `Table.proves`;
   `Figure.section_key`, `Figure.picture_shows`, `Figure.caption_says`,
   `Figure.detected`, `Figure.checked_ok`; `Section.section_key`,
   `Section.exhibit_refs`; `Sections.summary_job_met/conclusion_job_met`;
   `DossierJob.spine`, `DossierJob.spine_round_consumed`; STEPS →
   `("reconnaissance","brief","plan","analysis","spine","exhibits","draft",
   "compose","receipts")` (tables+figures fold into `exhibits`; `compose`
   becomes render-only).
2. `src/dossier/spine.py` (new) — `run_spine(job, docs)`: prompt
   `prompts/dossier_spine.md`, `SPINE_SCHEMA`, `validate_spine` (walls in
   C.1), field-patch retry (port `_spine_patch_trio` idiom onto
   `llm.call_json` — add `patch_scope/patch_tool/patch_merge` kwargs to
   `call_json`), `redirect_spine(job, notes)`.
3. `src/dossier/walls.py` — `has_digit_run(text)`; `verify_anchor` returns
   `trimmed` (already) — callers decide: the spine and the draft treat
   `trimmed` as *not verified for a claim* (kept, recorded).
4. `src/dossier/tables.py` — `_user` takes the spine's table specs; schema
   adds `section_key` enum + `proves`; per-exhibit skip (`table_unavailable`);
   `revise_rows(job, docs, table_key, findings)` (Phase 2 uses it).
5. `src/dossier/figures.py` — `plan_figures` becomes `spec_figures(job)` over
   the spine's figure specs (schema adds `section_key`; caption-number wall);
   `_generate_one` keeps `detected`/`checked_ok`, mints the compliance finding
   (Phase 1 adds the ledger; Phase 0 keeps it as a typed note) and, at medium+,
   one re-render with the recommendation (`figure_rerendered`).
6. `src/dossier/compose.py` — `_user` passes the spine, full tables, figures
   with `detected`; `SECTION_SCHEMA` adds `section_key` + `exhibit_refs`;
   `write_sections` walls (order, token-once) with section-scoped patch
   retries; `_render_context` places exhibits at tokens (`_CLAIM_MARK` sibling
   `_EXHIBIT_MARK = r"\[\[(table|figure):([a-z0-9_]+)\]\]"`) and numbers them
   in reading order; `render_markdown` prints each caption once; the
   "forgotten exhibit → last section" fallback becomes a wall.
7. `src/dossier/runner.py` — `STATUS_FOR_STEP`, `STEP_WHY` (narration lines
   from C.1–C.3), `_run_step` branches for `spine`, `exhibits` (tables then
   figures), `draft`; `compose` = render only.
8. `src/dossier/store.py` — `JSON_COLUMNS` + `spine_json`; `COLUMN_FOR_FIELD`;
   DDL migration (`ALTER TABLE … ADD COLUMN` guarded).
9. `src/workflows/definitions/dossier_standard.json` — phases 4.5 Spine, 5
   Exhibits, 6 Draft, 7 Compose, 8 Receipts (phase names are what the
   analyzer-mgmt console prints).
10. `web/src/steps/DraftStep.tsx` (`buildRail`) — rail steps from STEPS;
    `web/src/steps/DossierStep.tsx` — a "Plan" drawer (spine sections + claims
    + exhibits) above the rendered HTML.
11. Gates: `tests/test_dossier_spine_walls.py` (bounds, keys, caption-number
    law, anchors), `tests/test_dossier_compose_placement.py` (tokens place
    exhibits, forgotten exhibit refused, section order wall, markdown caption
    once).
    Proof: re-run the `fashion_bundle` exemplar at medium and diff the
    exhibit placement and captions against `live-dossier-dce25aeed631`.

**Phase 1 — the cross-check (report only) + the findings ledger.**
- `src/dossier/crosscheck.py` (new): `run_crosscheck(job, docs, priors)` with
  `prompts/dossier_crosscheck.md`, `CROSSCHECK_SCHEMA`, `validate_verdict`
  (quote-on-page, where-exists, realization-required, fate completeness),
  the code clamps (trimmed anchor, caption digit, unplaced table, failed
  picture check), vision input of the rendered figures (reuse
  `images.compliance._prepare`).
- `src/dossier/findings.py` (new; the target ledger): mint from verdict,
  `open_findings`, `record_fates`, `signals_for_judge`; store column
  `findings_json`.
- `runner.py` STEPS gains `crosscheck` after `draft`; skip law
  (`crosscheck_unavailable`).
- `routes/dossier.py`: `GET /jobs/{id}/findings`, `POST /jobs/{id}/recheck`.
- Desk: punch list on `DossierStep.tsx` (row grammar from Wirecut's
  `MakeStep` punch rows: where · effect · cure · price), `hangs_together`
  chip, "Re-check the whole" button.
- Gate: `tests/test_dossier_crosscheck_walls.py` (quote-on-page refused,
  clamps mint findings, fates required with priors).

**Phase 2 — revise (the work order) + the report card.**
- `src/dossier/revise.py` (new): `draft_order(job)` (coalescing, prices,
  cap), `execute(job, order, ticks)` (exhibits → text → zero-change gate →
  render → optional re-check), events `revision_*`.
- `compose.rewrite_section(job, docs, section_key, findings)`;
  `figures.respec(job, figure_key, realization)`; `tables.revise_rows`.
- `runner.py`: `revise` step after `crosscheck` at medium+ (budget from
  `DEPTH_POLICY`: simple 0, medium 1 round, advanced 2 rounds + report card).
- `routes/dossier.py`: `POST /jobs/{id}/orders` (draft), `POST
  /jobs/{id}/orders/{oid}/execute {ticks, edits}`; desk "Fix everything
  ($x)" with the visible list.
- Gate: `tests/test_dossier_revise.py` (coalescing, order, zero-change gate,
  walls re-applied to realizations, pause on failure names its continuation).

**Phase 3 — the read-through.**
- `src/dossier/readthrough.py` (new) with `prompts/dossier_readthrough.md`,
  walls (before-on-page, marks preserved, no new digits, +2% cap), mechanical
  application, `structural` → findings (`none` affordance).
- `runner.py`: `readthrough` step before `compose` (off at simple); skip law.
- Desk: diff drawer (revertible per edit), usefulness chip on the cover.
- Gate: `tests/test_dossier_readthrough_walls.py`.

**Phase 4 — the desk loop and propagation.**
- `routes/dossier.py`: sharpen / regenerate / respec / revise-table / cut /
  insert / `PUT` edit endpoints; `spine/redirect`; versions
  (`section_versions_json`).
- `authored_by` stamps and the sovereign-paragraph wall; `re-check owed` and
  `stale` arithmetic in one place (`src/dossier/loop.py`, a pure function over
  recorded rounds — the `loop.loop_position` idiom) used by the API and the
  cover.
- `DossierStep.tsx`: per-section/exhibit action trays (Wirecut's
  `SharpenTray` grammar: estimate → run → options → "Use this one"), stale
  badges, the loop strip.
- Playwright walk of the desk (mandatory before "done").

**Phase 5 (optional) — the retrospective for dossiers.** One priced call over
the job's record (spine rounds, findings + fates, revision steps, receipts) →
trajectory + 3–5 lessons with evidence refs; autorun after `done`; pulled into
the next session like Wirecut's `pull_retro_feedback.py`.

**What this design deliberately does not touch:** reconnaissance, the brief's
three angles, the plan/executor analysis, the anchor wall's verbatim law, the
images contract. The failure is concentrated where no pass currently looks —
between the finished parts — and the fix is concentrated there.
