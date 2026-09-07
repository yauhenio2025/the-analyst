# The distinction maker: thinking with and against others, as records (Evgeny, 2026-09-07 13:34)

## 0. The ask, in his words

"A lot of the stuff I do and think about is in distinction to other people. I'm trying to understand what they are doing to
position myself vis-à-vis them… build a formal, powerful distinction-maker engine where, on fetching the texts of those guys, we
would read them through whatever my working hypothesis is across the entire model, and say: on the questions you are arguing,
what they argue is this, this and this; your position seems to be this; is it correct? do you want to restate? how could you
elaborate? Then I respond, and my distinction against them becomes part and parcel of my own theory. We use them as crutches:
they have articulated something; I can articulate something of my own against it, or use it to focus and sharpen what has been
germinating in my head all along." The occasion: his answer on the Brief (turn 11, 13:07) to a challenge on the state's logic,
arguing against Brenner (2006 on Harvey, 1999 reply to critics, 2005 reply to Panitch and Gindin), with Hintze (via Perry
Anderson) and Arrighi (2005, 2006, The Long Twentieth Century) as the way out — a turn whose references the Stacks resolved to
ten held texts (bundle 694).

## 1. The philosophy, from the July dictations (`/home/evgeny/projects/oaas/communications/dictations/`)

- Theory-making IS distinction: "that's what theory-making is: the perpetual production of difference between us and something
  else" (2026-07-11, l. 13). "The function of your distinctiveness is really a function of your understanding of the inner
  workings of those other discourses" (2026-07-24, rec. 208, l. 20) — hence the texts must be read, not remembered.
- A foil is a tactical use of a thinker; an encounter is the deep operation around one thinker (2026-07-15, l. 742). Both
  start from the other's articulation: "we want to start with other thinkers as a foil that's actually productive for us"
  (07-11, l. 13).
- Only the dimensions that matter: "we don't need to specify distinctions from them on every single dimension, only on
  dimensions that matter for specific projects" (07-11, l. 258).
- A conveyor belt, not a fixed output: "unearthing statements and summarizations of statements that would be maximally
  efficient in provoking our commentary; it's our commentary then that will provide the fuel on which we codify what makes our
  own position distinct" (07-13, l. 23). The loop he asked for today is verbatim in 07-16 (l. 14): "'Look, there is a way to
  think about it coming from pragmatic sociology in France… Does it sound like something you agree with?' Based on that, we
  would be able to make a distinction."
- Two activities kept apart: making distinctions, and sharpening one's own formulations (07-13, l. 49). The first feeds the
  second; the desk must not fuse them into one edit.
- Absorption is a relation too: "occasionally incorporating their thought fully while saying that within our framework, due
  to the availability of extra concepts, we can take the analysis even further" (07-15, l. 629).

## 2. What exists

- **OAAS, `factory/distinction_module/`** (rec. 208, July 24): a foil registry (`foils.py`), per-thinker foil dossiers from
  held sources (logical · historical · rhetorical), `run_contrast.py` (a dictation × a focus × foils), verdicts **parallel ·
  collides · overlaps-then-diverges** on an axis with an ours/theirs pair, a why, a bridge and a confidence, then distinction
  propositions ("distinct from…", "what becomes sayable…"). Older: `review_pilot/distinctions.py`, a first-class Distinction
  (target · axis · position) with a reframe and a dependency-impact scan over the theory base.
- **The Stacks' Brief** (session c7, today): dictation with a name-check pass (library authors, ledger persons, the Brief's
  names; DeepSeek Flash picks among candidates); references resolved per turn into a bundle of held texts; the exchange hands a
  reader PROMPT.md (the parts, the challenge, the thread, his answer, rules) and takes ANSWER.json (reading · effects · edits ·
  follow-ups · new challenges · hunches · references); a statements file (his comment as the document under test, each
  reference a statement with who · clue, the texts as sources) already travels to the Analyst for the re-read; a challenge kind
  can carry a structured payload in inputs_json; a challenge to a part not yet his is held until he approves the part.
- **The Mastermind**: nothing reads the owner's hypothesis against an interlocutor. Neighbours: `reference_reread` (his
  references against the texts), `dialectical_structure`, `rival_explanations` (inside one text), `citation_engagement_map`.
  The statements door now windows a long source around the passages its statements name (turn 11 shipped three Hintze volumes
  whole and the executor refused 4.6M chars).

## 3. The design: the OAAS module ported as records

The Mastermind holds the reading as engines with vocabularies and a recipe; the Stacks hold the turn, the texts, the parts, the
challenge and the settled distinction as a part of the argument; the Referee holds the interlocutors as thinkers and schools.

**Vocabulary `distinction_relations`** (from the OAAS verdicts, plus his two): parallel (they answer the same question the
same way, in other words) · collides (they answer it against us) · overlaps_then_diverges (agreement up to an axis, then a
fork) · absorbs (we take theirs whole and go further with a concept they lack) · irrelevant (a disagreement on a dimension that
does not matter for this argument). **Vocabulary `interlocutor_roles`**: foil · encounter · ally · source.

**Engine `interlocutor_position`** (family distinction). Documents: his turn and references as a `statements` source (windowed
texts), the argument's parts as a `role: argument` document. Dimensions: I1 `question` — the questions his turn is arguing, in
his words, anchored in the turn; I2 `their_claim` — per interlocutor × question, what the text argues, anchored in the text with
its locus, and the role the turn gives them (foil · encounter · ally · source); I3 `their_silence` — a question the text does
not address (never invented: "not in the held text").

**Engine `distinction_draft`** (over the upstream rows, the turn and the parts). D1 `your_position` — his position per question
as best inferred from the turn and the parts, anchored in his words, with confidence; D2 `relation` — per interlocutor ×
question: the relation from the vocabulary, the axis, ours / theirs in one clause each, the bridge (what would reconcile or
what forbids it); D3 `question_back` — the question to him: is this right · restate · elaborate, concrete, with options where
a choice is real. The Stacks render D1–D3 as a challenge of kind `distinction` (inputs_json: interlocutor · their_claim with uid
and locus · your_position · relation · axis · question); his answer is an exchange turn as today.

**Engine `distinction_settle`** (after his answer). S1 `distinction` — the settled proposition: distinct from whom, on which
axis, holding what, because; what becomes sayable; S2 `effect` — which parts it moves · supports · complicates · contradicts;
S3 `open` — what remains to test and which text would decide it (a fetch or a re-read the actions registry can license). The
Stacks write S1 as a version of the part or a new part with the interlocutor's text cited; the Referee can take the
interlocutor as a thinker with the relation as evidence of a school.

**Recipe `distinction_round`**: interlocutor_position → distinction_draft, scoped (the first reads the texts; the second the
rows, the turn and the parts). `distinction_settle` runs alone on the answer. All at surface first; checked when the pilot says.

**Actions and practices.** A turn that points at prior analysis ("we also have it somewhere in the memos; search for Brenner,
Arrighi, Hintze, Harvey") is a finding kind `reference.pointer_to_prior_analysis` licensing `stacks.search-analyses`: the
Stacks' memos and conversations and the projects' communications folders (today the corpus is `~/projects/arrighi-nlr/
communications/` and `~/projects/oaas/communications/`, not the Stacks' memos — the owner, 13:42: "we have to build up this
capacity"); a practice `analysis-search` records where such analyses live and how to search them. The foils he names ("10 or 15
thinkers that we know are a perfect foil for us") become a `foils` record when he names them; until then the turn's references
and the Brief's named interlocutors are the foils.

## 4. The seams, as payloads

- Stacks → Mastermind: `POST /v1/dossier/jobs` with sources [{role: statements (the turn, references, windowed texts)},
  {role: argument (the parts, numbered, each with its state: his / desk draft)}], entry chosen, path [interlocutor_position,
  distinction_draft]; or the light call per engine for a single interlocutor.
- Mastermind → Stacks: `GET /v1/dossier/jobs/{id}/distinctions`: per interlocutor × question the rows of both engines joined —
  their claim (uid, locus, anchor), your position (anchor in the turn), relation · axis · ours · theirs · bridge, the question
  back (kind, text, options) — ready to file as challenges of kind `distinction`.
- His answer → `POST /v1/dossier/jobs` with the answer as statements plus the prior rows as context → `distinction_settle` →
  the settled proposition with effects, which the Stacks write as a version of the part.

## 5. First steps

1. Today: the two vocabularies, the three engines, the recipe, the `/distinctions` rendering; tests. 2. Pilot on turn 11 (Brenner
· Hintze · Arrighi · Harvey · Anderson, bundle 694) with windowed texts, surface depth, as a light call per interlocutor; the
rows to the Stacks for the challenge kind. 3. The Stacks: the `distinction` challenge, the feed-back of his answer into
`distinction_settle`, the search-analyses capacity. 4. The foils record when he names them; the Referee's thinkers as a
name-check source. 5. The impact scan (OAAS review_pilot) as a later engine over the parts: what a settled distinction changes
elsewhere in the argument.

## 6. The first round, and what it took (2026-09-07 15:35)

The round ran on the owner's turn 11 over the Stacks' re-read job (ten held texts windowed, 584k chars) with the parts beside: 32
rows, every one anchored, $0.31; Brenner collides (independent state rationality under structural dependence), Hintze parallel,
Arrighi overlaps then diverges, Anderson absorbed; six questions back, filed on part 6 of Brief 1 by the Stacks (three in the day's
review slots, three waiting). Rows: `communications/study/distinction_turn11_2026_09_07/README.md`.

Seams a new engine family must cross to read a statements source: membership in the citation FAMILY (`src/sources/
citation_evidence.py`), so the source unpacks into the turn and the witnesses instead of riding as raw context; an entry in the
family's per-engine scope table naming the roles it may read (the turn as citing_author, the texts as primary_window, the parts as
argument, the answer as answer); an added step's cap above the light route's (a step reads what the job read; what a cap leaves out
is named); and the latest phase of an engine as the upstream of the next.

The Referee's shape for a relation posted as candidate evidence (the-referee-48, 15:05): POST /api/schools/{id}/candidates with
evidence {relation, axis, clause, finding, run, text} and source_ref "distinction:<run>"; the operator judges in the queue.

## 7. The encounter (Evgeny, 17:40: "encounter, then impact scan")

His July distinction (2026-07-15, l. 742): a foil is tactical, "very useful towards the end when it comes to narrating things"; an
encounter is "a much deeper operation around single thinkers". The distinction round is the foil: one turn, several interlocutors,
one question each. The encounter is one thinker, several of their texts, the owner's whole model.

**Engine `encounter_map`** (family distinction; reads the thinker's texts as witnesses, the owner's turn as the text under audit,
the parts as `argument`, his hunches as `hunches`): E1 `position` — the thinker's position on an owner's question per text or
period, with locus; E2 `concept` — the load-bearing concept, what it does in their system, and the choice it puts to the owner
(absorb · translate · refuse); E3 `opponent` — whom the thinker argues against, and whether the owner shares the opponent; E4
`turn` — where the thinker moved between texts; E5 `silence`. **Engine `encounter_draft`** (over the map and his model): X1 `axis`
— the two to four axes that organise the whole meeting; X2 `relation` per axis (distinction_relations) with ours, theirs, bridge,
bears_on; X3 `take` (vocabulary `encounter_takes`: absorb · translate · refuse · defer) per concept or position, with the concept of
ours it translates into; X4 `question_back`; X5 `read_next` — the thinker's texts to read next, ranked, held or not. Recipe
`encounter_round`; the settle is `distinction_settle` (its context now includes the encounter's rows). `GET /v1/dossier/jobs/{id}/
encounter?thinker=` renders it per axis with the challenges (`encounter: true`) and the route in. The Stacks file the questions as
distinction challenges as before; the route goes to the references lane (a text not held is a fetch the actions registry licenses).

The impact scan follows (his order): after a distinction or an encounter settles, re-read the whole argument for the parts it
changes (OAAS review_pilot's dependency-impact scan as an engine).

## 8. The impact scan (his order: after the encounter)

OAAS review_pilot's dependency-impact scan as an engine. **`impact_scan`** reads the argument's parts (and his hunches when supplied)
against the settled distinctions (S1 rows, via the recipe's context, or an encounter's draft): P1 `impact` — a part touched directly,
with the effect (argument_effects: moves · supports · complicates · contradicts) and the change in one clause; P2 `dependency` — a
part that rests on a touched part (as premise · term · ground) and so changes at one remove; P3 `retest` — what must run again
(vocabulary `retest_runs`: hunch_test · reread · frame · distinction_round). Every row anchored in the part or the hunch it names;
never a rewrite — the desk proposes versions, the owner clicks. `GET /distinctions` carries it as `impact`; the Stacks' ledger takes
P1/P2 as effects with reach from the reading (bears_on) and P3 as `next` under the reaction-follow-up practice.

