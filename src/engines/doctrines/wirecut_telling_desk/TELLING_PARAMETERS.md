# The telling as a set of explicit dials — a parameter model for "How should the story be told?"

> Written 2026-09-02 in answer to the operator's question: should each storytelling approach make explicit *how much information to give away straight away, whether it needs more intrigue, whether it needs more set-up*, and so on. This document proposes the dials, the settings the shelf supports, the per-approach defaults, and how the model would be declared and judged inside Wirecut's LLM-first architecture. It is a design, not an implementation.

## 1. Why dials, not more cards

The ten cards fix *where the film enters and what altitude it holds*. Everything else that decides whether a viewer stays — when the outcome is known, how much normal life precedes the break, how many turns there are, how much the other side gets, whether a person carries the stake — is left to the writer's judgment inside a prose contract. The shelf names those decisions one by one (see `SYNTHESIS.md`); the books treat them as *variables a storyteller sets*, not as properties of a genre. McKee's line is the frame: plot is the ordering of emotions, and each of these dials is a choice about that ordering.

Making them explicit buys three things:
1. **Judgeable plans.** A spine that declares "outcome known at the hook; secret is the mechanism; two turns; the other side gets its best case in movement 2" can be checked against the script by the benches, in the source's own terms, without any code scoring merit.
2. **Honest availability.** Each setting has a grounding requirement (a hindsight film needs the record to say what actors believed). The slate can say which settings *this source* affords, the way it already says which cards it affords.
3. **A plain question for the journalist.** Three or four of the dials are exactly the questions an editor asks ("Do we give the answer away up front?"), and they can be shown in the operator's plain language without exposing the machinery.

## 2. The dials

Thirteen, grouped by what they govern. For each: the setting vocabulary, what the shelf says, the grounding requirement, and how the benches would judge it. All judged by models against the plan and the source; none by regex.

### A. Information release

**D1. Disclosure curve** — what the viewer knows, and when.
- *Settings:* `answer_first` (the claim or outcome in the hook; the film proves or explains — the verdict's habit); `question_first` (the paradox or unexplained outcome in the hook; the answer arrives late — need-to-know); `outcome_first_how_later` (the ending known at once; the film is how it came about — hindsight); `staircase` (each beat answers the last question and opens the next — the helicopter's "and why is that?").
- *Sub-fields:* `outcome_known_at` (hook / centre / close), `mechanism_known_at`, `secret` (the one fact held to the end: McKee's "critical facts last… secrets").
- *Shelf:* Price's three rules of release; McKee's paced exposition; Gulino's curiosity-before-exposition. The default failure is `answer_first` by habit.
- *Grounding:* reordering only; the one comprehension fact stays early.
- *Judged by:* Synthesis checklist Q4–Q6.

**D2. Question engine per act** — which tense the tension runs in.
- *Settings:* `mystery` (past: what happened, why — curiosity), `suspense` (future: known stake, uncertain outcome — fearful anticipation), `irony` (viewer ahead of the actors — heightened suspense), `curiosity` (goal unknown), `none` (a plain explanatory act — honest for one act, never for all).
- *Shelf:* Price's three engines; Iglesias's curiosity vs suspense; Gulino's dramatic irony bracketed by revelation and recognition; Hitchcock's fifteen minutes vs ten seconds.
- *Grounding:* `irony` requires the source to report what actors believed at the time; `suspense` requires a stake the source makes credible.
- *Judged by:* Q4, Q7; Synthesis Law 6.

**D3. Telegraphing** — what destination is announced early.
- *Settings:* `deadline` (a dated event the film counts toward), `promise` (an obligatory confrontation announced), `none`.
- *Shelf:* Gulino's telegraphing and ticking clock; Hauge's "show where the story is headed"; McKee's inciting incident projecting the obligatory scene.
- *Grounding:* the date or confrontation must be in the source.
- *Judged by:* Q6.

### B. Set-up and stakes

**D4. Set-up budget** — beats before the complicating event.
- *Settings:* `0` (cold: the first line is the break), `1` (one concrete beat of how things stood, broken by beat two or three — the one-beat normal), `2` (two beats; only above ~2 minutes).
- *Shelf:* Gulino's flow of life vs Bickham's "don't warm up your engines"; Franklin's complicating focus ending on the complicating event; Weiland's orientation questions closed at once.
- *Grounding:* the "normal" must be the source's baseline, not an imagined one.
- *Judged by:* the beat index of the complicating event; Q11 threads.

**D5. Stakes visibility** — when the cost of failure is established, and at which scales.
- *Settings:* `at_hook` / `before_centre` / `late`; scales `systemic`, `human`, `viewer` (Schechter's three parts: many, few, one).
- *Shelf:* "Establish consequences" (starred by the operator); Iglesias's "remind the reader of the stakes"; Bork's life-altering test (stakes present throughout).
- *Grounding:* the consequence must be the source's, ideally its own precedent.
- *Judged by:* Q2.

**D6. Face on the stake** — the person whose fate the outcome decides.
- *Settings:* `named` (a person or community named in the source; on screen before the centre and at the close), `collective` (a group the source describes specifically), `absent_declared` (the source names no one; the film stays systemic and the plan says so).
- *Shelf:* Schechter's stakes character; McKee's three levels of conflict; Iglesias's sympathy categories (used only as reported).
- *Grounding:* no composites; the portrait's "the source cites, it does not follow" refusal applies in miniature.
- *Judged by:* Q3.

### C. Turns

**D7. Turn count and placement** — how many reversals, and where.
- *Settings:* count `1` (≤60s), `2` (≈90s), `3` (2–3min); `centre` required or optional (the midpoint mirror); `catch_at_first_turn` (the first turn written as "they got what they wanted, and…").
- *Shelf:* Gulino's midpoint culmination; Edson's midpoint sequence; Yorke's key knowledge then regression; Truby's frying pan; Chamberlain's Catch.
- *Grounding:* every turn is an outcome the source reports as different from what the actors expected; the record decides the second-act shape (dark/spark, nail, false victory).
- *Judged by:* Q14–Q16.

**D8. Reveal ordering** — the force curve of disclosures.
- *Settings:* `ascending` (each reveal outranks the last; the strongest last-but-one — the only setting the shelf endorses), with the `strongest` reveal named.
- *Shelf:* Truby's gears.
- *Judged by:* Q13.

**D9. Zig before zag** — the confident wrong beat before the turn.
- *Settings:* `on` / `off`. On: the beat before the turn is the one where the wrong expectation is strongest (quoted confidence from the record).
- *Shelf:* Mercurio; Gulino's preparation by contrast.
- *Judged by:* Q15.

### D. Antagonism and meaning

**D10. Antagonism weight and rendering**.
- *Settings:* weight `none` (an explanation with nothing resisting — flag it), `one_beat` (the verdict's current minimum), `distributed` (swings across the film — McKee's idea/counter-idea); rendering `best_case` (as the other side presents itself) vs `stated_flatly` (the shelf calls this a strawman; allowed only when the source itself reports the view that thinly).
- *Shelf:* McKee's principle of antagonism and progressions; Truby's strong-but-flawed argument; Price's equal weight to the anti-theme.
- *Grounding:* swings are the source's own reversals, weighted as the source weights them; no manufactured symmetry.
- *Judged by:* Q18–Q19.

**D11. Ending verdict** — which value wins, and how the close carries it.
- *Settings:* Price's four — `right_wins`, `wrong_fails`, `right_loses` (social criticism), `wrong_wins` (the cynical world); plus the existing presentation contracts (consequence, corrected sentence, return to scene…); plus `controlling_idea` as value + cause with a source anchor.
- *Shelf:* McKee's controlling idea; Price's ending decides the theme; McKee's "never explain".
- *Grounding:* the cause must be asserted by the source; the meaning is stated at most once, late, in the source's words.
- *Judged by:* Q20–Q21.

### E. Texture and voice

**D12. Altitude profile and scenic allowance**.
- *Settings:* per movement `particular` or `claim` (never `middle`); `scenic_beats` count (0–N) with their source anchors; `digression_inside_action` on/off.
- *Shelf:* Hart's ladder and summary/scenic languages; Kramer's digress-in-the-middle; Franklin's threads.
- *Grounding:* scenic only where the source describes process with time, place, actors.
- *Judged by:* Q8–Q11.

**D13. Voice stance, cast and density**.
- *Settings:* narrator `anchor` (recedes) ↔ `classify` (steps forward), `signposts` 0–2, `direct_address` on/off; `cast_max` named actors (default 4) with functions (wanter, opposer, stake, explainer); `longest_beat_is_decisive` on/off; `emotion_promise` (the primary visceral feeling and its sequence across acts — the ordering of emotions).
- *Shelf:* the audio handbook's two narrator functions and Abumrad's arrows; Myers's character = function; Truby's multi-hero drive; Mercurio's density; Iglesias's three Vs and Blacker's plot.
- *Judged by:* Q22–Q24; the register already carries part of this.

## 3. Per-approach defaults

A card becomes a *preset* over the dials. The table gives the shelf-derived default for each card; the writer may override any cell with a source-grounded reason, and the slate may mark a cell `unavailable` for a given source. Only the dials that differ meaningfully across cards are shown; D8 (ascending) and D9 (on where the source has it) are constant.

| Dial | Helicopter | One scene first | The case | The portrait | The timeline | The verdict | Open question | The numbers | The correction | The object |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 disclosure | staircase; secret = the counter-intuitive piece | question_first; secret = what the pull-back reveals | outcome_first_how_later *or* question_first (the record decides) | question_first; secret = the deepest layer | outcome_first (the present stake) then how | **question_first** (paradox hook), never answer_first by default | question_first; secret = the earned answer | question_first (the arresting figure); secret = the figure that breaks the pattern | question_first (the myth under indictment); secret = the break | question_first (the object strange); secret = its transformation |
| D2 engine | mystery (why does this keep happening) | suspense inside the scene → mystery in the argument | irony when outcome is known; suspense otherwise | suspense (what will they do) | irony (we know how the eras end) | mystery (why is the claim true) → suspense (consequence) | mystery per round | mystery (what the series cannot explain) | curiosity → mystery (why it is easy to believe) → revelation | mystery (what happened to it) |
| D3 telegraphing | promise (the mechanism will be shown whole) | promise (we will return here) | deadline (the case's own end date) | promise (the turning point) | **deadline required** (the date the film counts toward) | promise (the consequence) | promise (the answer) | promise (the last figure) | promise (the true sentence) | promise (the object re-seen) |
| D4 set-up | 0 | 1–2 (the scene's normal) | 1 | 1 (mid-act, then the world) | 0–1 | 0 | 0 | 0 | 0 (the myth is the hook) | 0 |
| D5 stakes | at_hook, systemic; human before centre | at_hook, human; systemic at the pull-back | at_hook | at_hook, human | before_centre | at_hook | before_centre | at_hook (what the figure counts) | before_centre (who believes it and pays) | before_centre |
| D6 face | **named or absent_declared** | named (the scene's people) | named (the case's actors) | named (the subject) | named or absent_declared | **named or absent_declared** | named where a candidate concerns a person | **named or absent_declared** | named (who held the belief) | named (whose object) |
| D7 turns | 1–2; centre = the complication | 1 (the pull-back) + return | 2–3; **centre = the mirror**; catch at first turn | 1–2; centre = the turning point as a reported choice | 2; **centre = the era that looked like the reversal** | 1–2; centre = the other side's best case | one per discard; centre = last discard | 1; **centre = the pattern-break** | 1 (the break); centre = the second myth if any | 1–2 (contestation as a value turn) |
| D10 antagonism | distributed (what resists the mechanism) | one_beat (at the pull-back) | distributed (the case's reversals) | distributed (what opposed the person) | one_beat per era at most | **distributed, best_case** | distributed (each candidate is the other side) | one_beat (what the figures do not show) | distributed, best_case (the plausibility act) | one_beat (the contestation) |
| D11 ending | mechanism restated + which value the machine serves | return to scene + right_loses / right_wins as the record says | case generalised + the four-ending verdict | person left + the verdict implicit in where they are left | now in pattern + which value the pattern serves | consequence + **declared verdict** | earned answer + verdict | number transformed + verdict | corrected sentence = controlling idea (value + cause) | object re-seen + verdict |
| D12 altitude | claim rungs with one particular anchor per act; digression_inside_action on | particular → claim → particular | particular (the case) with one claim beat | particular throughout; claim ≤1 per act | particular per era (one event each), claim at the close | claim rungs with one particular per act; **no middle** | varies per round | figure rungs with one particular per act | plausibility act particular; break particular; close claim | particular (the object) with claims around it |
| D13 voice | classify (explains); signposts 1 | anchor in scene, classify at the pull-back | anchor (the clerk) with scenic turns | anchor | anchor; signposts at era turns | classify (prosecutes); direct address on | classify (investigates); direct address on | classify; direct address for the scaling beat | classify; direct address on | anchor (present tense for the object) |

Bold cells are where the shelf most changes the current contract.

## 4. How the dials would live in the system

**Declared in the spine, in plain words.** The spine already declares movements with `zoom`, `attention` (question, withheld, reveal, earned_hold), a `promise`, `pattern_interrupts` and `duration_rhythm`. The dials extend that record: a `telling` block with the settings above and a one-line grounded reason per non-default cell. The writer declares; nothing scores.

**Judged by the benches, never by code.** Each dial has its checklist questions (Synthesis §5). The table read and the screening judge report deviations as findings with the plan's own words quoted; the operator decides. This keeps the LLM-first law: judgment in the prompt, plumbing in code.

**Offered by the slate per source.** The recommended card's slate already says `fit / thin / unavailable` per card. The same three words apply to settings: "hindsight is available (the source reports what the ministry believed in March); a named face on the stake is unavailable (the source names no one)". The slate's `signal` quotes the turn or the belief, not only the material.

**Surfaced to the journalist as three plain questions**, under the operator's UI doctrine (no jargon, ladders not dumps), on the telling card after the approach is chosen:
1. *How much do we give away at the start?* — the answer first / the question first / the ending first, then how it happened.
2. *Who carries the stake?* — a named person from the story / nobody, the story is about the system.
3. *How much does the other side get?* — one honest beat / its full case, run through the film.

Everything else stays a writer's declaration the journalist can read in the "what the desk chose" drawer.

## 5. What the book-mining commission should bring back for this model

Each dial has settings the shelf endorses and settings it warns against; the notebooks captured the operator's first pass. The full books can supply, per dial: the author's explicit rule, the failure it prevents, the exceptions the author grants, and the examples — so that each setting's *doctrine paragraph* can be written from the books rather than from summary. See `BOOK_MINING_PLAN.md` for the brief.

## 6. Dial doctrine from the full books (added 2026-09-02 after the book commission)

Written from §4 of each of the sixteen book documents in `books/`. Per dial, per setting: the rule the books state, the failure it prevents, the exceptions the books grant, and the example. Setting names in code font are the vocabulary the spine would declare; names marked *new* were not in §2 and are argued for in `BOOKS_SYNTHESIS.md` §3. Everything here is judged by a model against the plan and the source; nothing is a score.

### D1. Disclosure curve

`question_first` — *Rule:* open on the sentence the viewer cannot accept — the number that cannot be right, the official's line the outcome contradicts — then let the documented normal tighten like a web (Stein, Quindlen's preface); name the force early in one clause and stage it late (Madden Q131, Ginzburg met last-but-one); who, what, where, when at once, *why* held (Rosenfeld); critical facts last, secrets last of all (McKee). *Failure:* the early gratification — the film's central answer delivered before the middle with nothing open after it (Stein); telling or depicting too much too soon (Madden). *Exceptions:* the one fact the viewer needs to follow enters at once (Madden Q89); withholding is resented unless the narrator's stance makes the holding feel chosen (Madden Q2 — the register does this). *Example:* "Jail is not as bad as you might imagine" → pages of ordinariness → the charge → "I did not kill my mother. I only wished I had."

`outcome_first_how_later` — *Rule:* the outcome in the hook, the mystery in the manner (Stein on Kazan's *The Arrangement*: the crash in line one); hindsight is automatic for a viewer who knows the end — play the actors' recorded confidence straight (McKee, *Character*); the frame is retrospective but the action inside it runs forward as lived (Stein, *Grow* ch. 11). *Failure:* the reference-order film — facts in lookup order, which nonfiction readers forgive and viewers do not feel (Stein's bomb story); the narrator naming the irony (Madden Q136). *Exception:* where the outcome is bad and known, the engine is negative suspense — wanting it not to happen (Stein). *Example:* *Rising Tide* — the levees broke; the film is Eads against Humphreys.

`staircase` — *Rule:* each beat answers the last question and opens the next; a movement's last line both closes its turn and holds the next question (Madden Q76, "Rosemary who?"); set an effect up and postpone its completion so the viewer first recognises and then experiences (Madden Q130); answer the viewer's obvious question when they would ask it — psychological order (Kaplan). *Failure:* the gratified boundary — a movement that answers its own question in its last beat while the next continues in place (Stein). *Example:* Madden's own story paced as a delivery, a call, a delivery, a call.

`answer_first` — *Rule:* the habit the books revise away — the claim or outcome stated, then proved. The lyrical peak in chapter one "ended the novel" (Madden Q76); the death in paragraph one "feels told" (Stein); the opening that gives away the story (Kaplan). *Exception:* when the source *is* the reveal (a leaked memo, a ruling), the reveal is the hook and suspense moves to mechanism or consequence; if the ending is public, withhold something else (Kaplan). *Failure:* nothing left for the middle to release.

*New sub-field* `held` — what is withheld, and until when: `answer` (the film's secret), `observation` (the inspector acted; what she saw waits a beat — Stein's nurse), `identity` (the name for a beat; the eyewitness last — Stein's bus), `opposer_history` (the record's account of the resisting actor, released in the last movement — Madden Q88). `mechanism_known_at` defaults late.

### D2. Question engine

`mystery` — *Rule:* curiosity about the past, what happened and why (McKee); the crash whose *how* is the question (Stein). *Failure:* false mystery — withholding a fact the viewer needs to follow, so confusion is mistaken for curiosity (McKee); a rhetorical question that is the desk's commentary rather than the viewer's next thought (Madden Q31).

`suspense` — *Rule:* the outcome hanging in the balance as long as possible; "keep raising the reader's curiosity and not gratifying it right away" (Stein); the future tense of a prepared past (Madden Q131). *Failure:* the flatline — conflict at one pitch across the film (Stein); resolving problems quickly. *Exception:* rest is needed, and the best rest provokes curiosity for the next clash (Stein).

`irony` — *Rule:* the viewer ahead of the actors (McKee); the double perspective assembled by the viewer, who then re-experiences the scene in a flash (Madden Q136). *Grounding:* both documented halves shown and adjacent; the film never implies the actor knew. *Failure:* the smirk — irony pointed at by the narrator, worst at the end, where it distorts the whole.

`curiosity` — *Rule:* a word or detail that makes the viewer ask why or how (Stein's curiosity adjective); a rest that holds a question or an omen (Stein's leaf). *Failure:* the empty breather.

`none` — *Rule:* honest for one act if declared — some serious writers undermine suspense on purpose to force attention onto other values (Madden Q131). *Failure:* an explainer with no engine anywhere.

*New per-beat instrument* `tension` — two elements pulling the viewer different ways with no plot event: a calm picture under a grave line, music against meaning, the particular against the claim (Madden Q167); tension is proximity and stillness is power (McKee, *Action*); friction plus refusal, brief, lasting only as long as the refusal (Stein, *On Writing* ch. 10) — relocating one sentence raises it with no new words.

### D3. Telegraphing

`deadline` — *Rule:* tension from a date or hour; read dates aloud (Stein, *On Writing* ch. 25; Kaplan's chronological order dated aloud). *Failure:* the date given as reference, not as a count the film runs toward.

`promise` — *Rule:* the obligatory scene projected by the inciting incident (McKee); anticipation as an element deliberately placed so the viewer feels something is sure to come (Madden Q127); Chekhov's shotgun must go off (Q154). *Failure:* the orphaned set-up whose payoff a later pass cut (Q126). *Exception:* the anticipated thing may arrive as its reverse (Madden c13).

`none` — legal where the record has no date and no announced confrontation (the open question); then the turn must be prepared by omens or the film has no forward pull.

*New sub-field* `turn_prepared_by` — `omen` (a documented early detail whose meaning lands later — the cracked levee from the record; Stein's *Magician* opening on snow and the name Sing Sing), `plant` (a recorded detail moved earlier so the decisive beat does not spring from nothing — Madden Q125; c7's transplanted lines), `dated_statement` ("in March the ministry still said…" — the legal plant where the record has no earlier instance), `none`. *Failure:* the telegraph line — narration that names the turn before it happens ("but it would all go wrong"); Stein: telegraphing is "usually to be avoided", the omen is the instrument. Telegraph the *destination*; omen the *turn*.

### D4. Set-up budget

`0` — *Rule:* start with a scene already underway (Stein); the grabber — plunge into the problem (Kaplan). *Failure:* the unmotivated bang — a loss or shock before anyone the source lets us care about is on screen: "the reader must know the people in the car before he sees the car crash" (Stein, *Grow* ch. 3); the setting fallacy is the other failure of the same slot — a skyline carrying "public information" nobody requires (Madden Q107). *Exception:* an author with earned authority may open on the bang (Morrison) — the register, not the desk, earns this.

`1` — *Rule:* when the hook is an event, the one beat before it belongs to the person it lands on; the beat carries a note of mystery, never orientation (Madden c1 — the second glass on the table); the engine starts by beat three (Stein on Lamb). *Failure:* the beat spent on "how things stood" as context; the habitual opening — statements about the protagonist's usual behaviour (Madden Q52).

`2` — *Rule:* only above about two minutes; the teaser — a calm surface with trouble sensed (Kaplan); Stein's own three pages of omens, which he admits was a risk ("a character doing something interesting is a safer way"). *Failure:* the flashback lecture; anything that delays the decisive move (Lawrence's children cut so the mother goes out to search — Madden Q85).

### D5. Stakes visibility

`at_hook` — *Rule:* the hunt test — is the want serious, does getting it mean risk, is success of consequence (Stein); stakes present throughout (Bork). *Requires* the human scale already in frame (D4 = 1 when the hook is an event).

`before_centre` — *Rule:* the cost shown before it is paid — the *warning* midpoint (Rosenfeld); the stake tested in the source's own terms of life and death (Edson).

`late` — legal only where the record itself reveals the cost late (the correction: who pays for the belief).

Scales `systemic` / `human` / `viewer` — the number of a noun sets the scale: "a boat" became "boats against the current" so each moves alone (Madden Q47).

*New* `credible_before_counted` — *Rule:* credibility is tested in the reading, not in life (Madden Q177); the fact the viewer will least believe is prepared before the film leans on it, or the source's own astonishment is quoted; a claim of scale needs its demonstrating particular on screen or is downgraded — the claims fallacy (Q64). *Failure:* the undemonstrated superlative ("unprecedented", "historic"); melodrama — stakes inflated past what the documented facts produce on their own (Stein).

### D6. Face on the stake

`named` — *Rule:* one protagonist, on screen in the first movement so the viewer cannot mistake whose film it is — "This was their inauguration, not his" (Stein, *Grow* ch. 10); whose story it is is the core of meaning (Madden Q165); introduce the person by one or two documented features and repeat them with variation (Q63) — which is also the generated actor's likeness anchor; keep the reported edge — the sworn word, the broken sentence — the tidied person is the flat one (Stein's Hoffa rule). *Failure:* two protagonists; the switch discovered late; the goody-goody; the narrator's "we/our/us" taking the frame (Nick brooding). *Exception:* a witness may carry the telling — hero-witness (Madden Q13) — where the record has one.

`collective` — *Rule:* a group is almost never as effective as one person (Stein); legal only where the source describes the group specifically and no individual acts in the record; Kafka's bureaucracy works as antagonist only because K. strains against it.

`absent_declared` — *Rule:* the film stays systemic *and shorter*; a catastrophe with no one in the car is a statistic and is filmed as a claim, not staged as drama (Stein). *Failure:* the sociology lesson — a force described in the aggregate that never acts through anyone.

*New* `opposer_named` — *Rule:* the resisting force also wears a name and a documented decision (Eads wanted outlets, Humphreys wanted levees, Humphreys won, the levees broke — "nonfiction and not invented"); the adversary on stage before the first turn (Edson); present at the decisive beat (Madden Q92); an opposer seen only through the protagonist's eyes is misjudged — Greene restored the scene that gave Louise her own vantage (Q71). *Failure:* the cartoon villain by adjective; the diffuse antagonist.

*New* `vantage` — *Rule:* the clip's camera takes the physical viewpoint of the person the source shows most affected (Stein; Madden Q104); who watches whom in the first beat is a structural decision (Faulkner reversed it and the novel restructured — Q8); a legal zoom shape is wide → narrow → wider than the opening (Q12). *Grounding:* the physical viewpoint is free; the mind behind it is not. *Failure:* alphabet soup — the aerial, the face and the crowd asked for in one clip; the vantage drifting across clips.

### D7. Turn count and placement

Count — *Rule:* simple plots move most — *Matador* has one turn and both die (Stein); one act for short work (McKee); below four turning points the piece is an explainer, so the four-point shape belongs to films of two minutes and more (Myers). *Failure:* the not-quite-credible turn — a man thrown over a railing, a warning shot to move a helicopter (Stein); a turn resolved by what the source calls chance, unlabelled (Madden Q178).

`centre` — *Rule:* the mirror (Chamberlain's want↔crisis), and two shapes the dial should name — `restatement` (the question re-posed at full weight) and `warning` (the cost shown before it is paid) (Rosenfeld); a scene done too soon spends the climax — move it later and disperse its elements (Madden Q83). 

`catch_at_first_turn` — *Rule:* the first turn *changes* the question rather than advancing it — Fresh News (Edson); "they got what they wanted, and…" (Chamberlain). *Exception:* the reversal that raises a new question instead of closing one is the stronger kind (Madden Q129).

*New* `false_ending_check` and `opposer_present_at_climax` — *Rule:* Madden Q92's four climax defusers: an earlier beat that had the climax's elements ("Oh, I thought that was the end"); a climax out of key with the film (a music swell on a film told plainly); the opposer absent so the confrontation becomes a report; the decisive beat too short — Malamud's begging scene ran six times the length of the climax, and revision made them equal (Q82).

### D8. Reveal ordering

`ascending` — *Rule:* the revelations sequence rises (Truby); exchanges build, never repeat — in life heated exchanges repeat, in a story they build (Stein); the first instance of a recurring element is the sharpest and the last may be the barest (Madden Q128); the confrontation belongs next-to-last (Q131); the last two climaxes carry opposite charges (McKee). *Failure:* the flat sequence — two facts of equal weight in a row; the reveal that outshines the ending; a sensational fact placed wrong that becomes the film's memory instead of its question (Q176). `strongest` is named in the plan and placed where it serves, not where it shocks.

### D9. Zig before zag

`on` — *Rule:* prepare the surprise by contrast — the correct, kindly sergeant before the murder (Stein); the sentence that leads the ear to expect a continuation and reverses it in the last clause (Madden Q28); readers enjoy expectations both gratified and reversed (c13 — Bill at the door when a fourth deliveryman was expected). *Failure:* the give-away — an early appearance of the turning element that spoils its later arrival, cut in revision (Stein, *Grow* ch. 10); the reversal the viewer did not feel because the expectation was never held. *Grounding:* the confident wrong beat is the record's own quoted confidence.

`off` — when the record shows no beat where the actors were most confident before the fall; do not manufacture one.

### D10. Antagonism weight and rendering

`none` — *Rule:* flag it; the conflict must be clearly posed or the viewer spends the film "vaguely wondering what is wrong" (Madden Q77); a force with no agent is a sociology lesson (Stein).

`one_beat` — *Rule:* the verdict's current minimum, and Stein's strawman unless the source itself reports the view that thinly.

`distributed` — *Rule:* idea and counter-idea swing across the film (McKee); the moral argument is *answered* by the opponent, not stated (Truby); Lawrence handed the thematic argument to a character and let the others answer him (Madden Q162). *Exception:* conflict is not a constant — rest is needed, and the rest provokes curiosity (Stein).

`best_case` — *Rule:* think of protagonist and antagonist as two antagonists; "try your damndest to make the other character win the argument" — as a drafting exercise from the source's own reporting, keeping what the source supports, weighted as the source weights it (Stein); Humphreys believed he was saving the population; quote the opponent's own best sentence. *Failure:* the cartoon villain — an opposing actor characterised by adjective ("the negligent ministry"); the foregone contest; sarcasm mistaken for satire (Madden Q140).

`stated_flatly` — legal only when the source itself reports the view that thinly.

*New* `opposer_history_release` — *Rule:* the record's account of what the resisting actor had done or believed, held to the last movement and released as the reframing beat in the record's words — Popeye's childhood inserted eight pages before the end (Madden Q88); the strongest legal form of the other side's honest best. *Grounding:* only a history the source contains; never an editorial softening.

### D11. Ending verdict

`right_wins` / `wrong_fails` / `right_loses` / `wrong_wins` — Price's four (§2), confirmed by the shelf; the ending decides the theme.

*New* `ironic_positive` / `ironic_negative` — *Rule:* both charges are true at the close and the ending leans one way (McKee, *Story* ch. 5 — the ironic climax); Stavros gets America having murdered for it (Stein). *Grounding:* both outcomes documented.

*New* `open_answerable` — *Rule:* the record is suspended; both branches shown (Kaplan); Hardy's readers "can therefore choose between the endings" (Madden Q90). *Failure:* an ending that closes a question the source leaves open, or opens one the source closes (Madden Q153).

Presentation — *Rule:* the ending recapitulates the opening's image or pattern, richer — the fur out of the box, the fur back in (Madden Q94); the film's one charged image returns as a glance, not a restatement (Q141, Q128); the close lands on the concrete with the sentimental and the abstract cut (Stein); strike the last line, then the last beat — better? (Kaplan); end where relations appear to stop — "the rest may be taken up or not, later" (James via Madden Q74); the coda added by convention is a digression (Hardy's Aftercourses, Q90). *New* `charged_image_return` names the object and its two appearances.

`controlling_idea` — *Rule:* stated at most once, earlier than the last image, in the source's words; a thematic *line* survives only as a quoted person's own speech placed as the one high-relief quote (Madden c24); the honest so-what is a documented consequence placed before the last image (Stein). *Failure:* the flag — the moral hoisted at the last opportunity, struck "as he has already struck the weather report out of the first paragraph" (Madden Q163); Madden's own last line that tied up the ends, "my worst error" (c27); Kaplan's seven failures — Message, Deus ex machina, Trick, Smoky, Confusing, Unearned, Explanatory; the spoiled ending — one sentence after the strongest line (Stein); the twist that makes everything before it a pretext (Madden Q150). *Exception:* an internal climax that belongs to the viewer — the realisation of why the story had to be told ("That Evening Sun") — only where the source itself ends open.

### D12. Altitude profile and scenic allowance

`particular` — *Rule:* the names of villages, the numbers of roads and regiments, and the dates are the concrete that has dignity (Hemingway via Madden Q52) — the source's own particulars add no fact; a beat is scenic only if it passes the film test (Stein); rendered as action from a vantage with time and distance declared (Madden Q104–105, Q112); present tense for the documented moment (Q45); one anchoring particular does the work of a list — the ill-fitting jacket, not the suit; the one bent wheel, not the wide crash (Stein).

`claim` — *Rule:* controlled generalisation is a legitimate mark of nonfiction style (Madden Q52) *when anchored by one concrete beside it* — "his hand on the ignition" lets the abstract sentence after it work (c23); summaries very short (Stein); past tense for the record.

never `middle` — *Rule:* scene and summary are each necessary to the other; one powerful scene after another is not desirable (Madden Q80); the middle rung is neither felt nor stated (Hart, §2).

*New* `half_scene` — *Rule:* summary with the key lines quoted — a paragraph of summary, then the two lines that matter (Madden Q80, Miriam's phone call); the grounded desk's workhorse: a summary beat carrying one particular and one verbatim line from the record.

*New* `envelope` — *Rule:* a filmable frame devoid of particulars that the viewer fills from context — "Grandma sat staring out of the window" (Stein); for us, a true absence staged (the unlit window, the empty chair, the closed shutter) where the source describes an outcome but not its scene. *Wall:* the empty chair is fine; the chair overturned is a claim.

`scenic_beats` — *Rule:* at most as often as the record allows and never two in a row; the decisive event is the beat with the most staged detail — zoom in on the moment and leave the rest of the meeting out (Stein). *Failure:* the described explosion — the decisive event summarised while a lesser event gets the picture; the discussion shown whole.

`digression_inside_action` — *Rule:* a hanging question holds while the film explains, and the explanation is tenser for the wait (Stein's Amory); interpolation by dashes drops a contrasting thought into an action (Madden Q30).

*New* `tense_per_movement` — *Rule:* one tense per movement, present for the documented moment and past for the record, with at most one shift at the film's turn as the pattern interrupt — Porter's captive present dropping to past at the very end (Madden Q45); two languages for two rungs — claim beats and particular beats should differ audibly in diction (Q14).

*New* `locations_max` — *Rule:* a short film affords few locations; every new place costs an orientation beat (McKee; Stein's eight-locations demonstration).

*New defect* `still_life` — nothing in the frame moves or is acted upon (Madden Q112–113: the Buchanan room where curtains, dresses and rug all move, and the one static clause cut). Related failures: the inert block; the exhaustive setting from research (Q107); the lighting-a-cigarette fallacy — a trivial documented act staged as momentous (Q50); the shout — a true detail louder than the beat's point (Morris's chamber pot, Q37); stock frames (Kaplan's Always-a-Robin).

### D13. Voice stance, cast and density

`anchor` (default) — *Rule:* the author is most intimate when stylistically most distant (Madden Q10); every evaluative word has an owner — Hardy cut "poor" from "her poor little hands" (Q10–11); "he said" only, never an adverb (Stein); where the fact is grave the narrator recedes — one excess authorises another (Madden Q114). *Failure:* author intrusion — a sentence only the desk could say (Stein); authority confusion — the viewer cannot tell whose evaluation this is (Madden Q11); the tag — "angrily denied", "reluctantly admitted" (Q100); the journalist's own indignation in the script — the me-rack (Q172).

`classify` — *Rule:* legal where the source's own findings are stated once; the ingratiating voice that openly declines to tell everything earns its withholding (Madden Q2). *Failure:* tone drift into the chummy, the sarcastic, the sentimental, the precious, or the prosecutorial in a wire film (Q53).

`signposts` 0–2 — *Rule:* no announced transitions — Kipling slips the Armistice in after a clause about something else (Madden Q84); formal connectives ("thus", "therefore", "nevertheless") are seldom compatible with story and each asserts a cause (Q33, Q42).

`direct_address` — *Rule:* Stein rejects second person as artificial ("Forget second person"); reconciled with §2: a question put to the viewer is a signpost, narrating the viewer into the story is the fault.

`cast_max` 4 with functions — *Rule:* one function per actor — contrast, parallel, alternative, confidante (Madden Q65); two with the same function reduce to one, *cut* never merged (Q66; composites are fabrication); minor actors at lower resolution — Emma reduced to initials and recurring images, and more powerful for it (Q60); names considered against each other — Sarah and Susan confuse (Q69); role tags for the ear.

`longest_beat_is_decisive` — *Rule:* no lesser beat runs longer than the decisive one (Madden Q82); impact is measured in seconds — the decisive act is brief and everything around it earns it (McKee, *Action*); cut whatever delays the decisive move (Q85).

`emotion_promise` — *now per beat.* *Rule:* courtesy — consideration of what the reader feels at every point; a scene outline annotated with "what is this scene doing to the reader's emotions?", written before drafting and re-read cold (Stein, *Grow* ch. 1); revisions aim first at emotion, through it at imagination, and only as an aftereffect at intellect (Madden Q185). *Failure:* the unplanned beat; a first minute that carries no emotion; the fallacy of expressive form — emotion in the author taken for emotion in the viewer (Q174).

*New* `whose_film` — one name from the source, on screen first (Stein; Madden Q165). *New* `handle` — the film in one sentence, written before drafting and used to reject beats; the worst-scene loop — cut the beat that carries least of the handle, re-rank (Stein). *New* `charged_image` — the film's one documented object or figure: found late in drafting, moved into the hook's tail, returned at the close as a glance (Madden Q141 — the green light's history). *New* `we_count` — how often the narration says "we/our/us".

Density — *Rule:* one plus one equals a half — the same matter said twice in different words diminishes both, and a film's four channels (picture, narration, subtitle, card) must not do the same job (Stein); "We know" in the margin is always cut; Kaplan's Law of Words — words not working for you are working against you; one adjective per noun, one verb per action (Madden Q40); the arresting fact at the end of the sentence (Q28); no pronoun crosses a cut (Q41); contractions unless emphasis is meant (Q46, Q101); read aloud once at pace — the sentence that had to be re-read is lost in speech (Q166); write for a monotone reading — the words must carry tone without the typeface (Stein). *Exception:* a motif returning is emphasis, not redundancy — the test is whether the second statement adds meaning (Stein; Madden Q27: it must *work* by ear).

### The journalist's questions, revised

§4's three plain questions become four — see `BOOKS_SYNTHESIS.md` §4c: what the viewer knows at the start (D1); who we meet before anything happens (D4 + D6, the people in the car); who carries the stake (D6); how much the other side gets (D10). "Does it need more intrigue?" is the slate's question (`held`) and the benches' finding, not the journalist's. The per-card intrigue profile that refines §3's table is `BOOKS_SYNTHESIS.md` §4b.
