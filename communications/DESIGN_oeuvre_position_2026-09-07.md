# A paper's place in its author's oeuvre — engines, a workflow, actions, and the philosophy behind them

Evgeny, 7 Sep 2026, 07:41, on Brenner 1985, "Marx's First Model of the Transition to Capitalism" (em:CBT7B8CL, one of the 63 Brenner
texts the Stacks hold): *"what kind of a role does it play within Brenner's overall oeuvre? … we need to go through the summaries of
everything that came before and everything that came after, look at citation patterns, changes and anomalies in this paper vis-à-vis
other papers, and activate genealogical engines: read it as a culmination of a research past (as if we didn't know what followed), read
it as a starting point of a journey (as if nothing came before), then read both holistically, as a middle point — and not assume it is
always a middle point: it might be the end of a research agenda and a reorientation. We are fine finding epistemic ruptures; maybe an
epistemic-rupture detector: does it qualify, and between which two halves? Engineer all of this as a series of engines and as a workflow.
Engines are not enough. And make it interactive: if the paper points to literature we never examined, commission harvesting of those
thinkers in the Referee, fetch PDFs, look at whom they cite — break it down into actions tied to analytical operations. The paper is the
entry point into thinking formally about what the Stacks does, what the Referee does, what the Mastermind does, and how to interconnect
them; formalize everything inside the Mastermind so it is transparent, modular and manipulable, and an LLM can suggest modifications
without hunting for the upper-level reasoning blocks inside Python code."*

## 1. The principle (to CLAUDE.md in every organ)

- **The upper-level reasoning lives in the Mastermind as records, never as prose in an organ's code**: methods (engines, with their
  dimensions, answer shapes and method cards), the sequences that compose them (workflows and recipes), the words they answer in
  (vocabularies), how to search (practices), and what an organ can do in response to a finding (actions). An organ reads these records;
  it does not keep its own copy.
- **Each organ does only what it alone can do, and exposes it as routes**: the Stacks — the library, its texts, profiles, citation
  ledgers, bundles; the Referee — thinkers, their works and readers, harvesting and fetching; the Reporter — the open web; the Mastermind —
  engines, workflows, vocabularies, practices, actions, and the walls that check what a model wrote against what a source says.
- **Findings map to actions in other organs**: a row of a kind an action declares it answers (a cited work not held, a thinker unknown to
  the Referee) becomes a suggested action with its inputs filled from the row; the owner clicks or the system runs it under a cap.
- **Everything measured writes back**: a practice's yield, an action's outcome, an engine's receipts, so the next planner weighs them.
- **The walls check shape, never meaning**: code verifies anchors, ids and vocabularies; a model judges the reading against the source.

## 2. The input (the Stacks' half)

For a focal text and its author, the Stacks export one bundle:

| document key | role | content |
|---|---|---|
| `focal:<uid>` | source | the focal text, whole (page-marked) |
| `before:<uid>` … | source | one document per earlier text by the author: its PROFILE rendered as text (title · year · thesis · question · tradition · object · period · concepts with glosses · people with roles and stances · works cited with loci · claims · positions · passages) — the summary, not the text |
| `after:<uid>` … | source | the same for each later text |
| `oeuvre` | plan | the packet: author, focal uid/title/year, the ordered list of texts (uid, year, title, profiled yes/no, held yes/no), the library's cited-works table for the author (work → which texts cite it, held uid or not), the Referee's thinker ids where known |

The prefix on the key is the scope a phase filters on (§4). Today the Stacks' `GET /api/authors/{aid}/works-profile` lists the works
with thesis/tradition per uid and `GET /api/items/{uid}/profile` gives the profile; the export route
(`GET /api/authors/{aid}/oeuvre?focal=<uid>`) composes them. Brenner: 63 texts; the profiles exist for most (the pilot counts them).

## 3. The engines (family `oeuvre`, group "Trace the trajectory")

All corpus-scope readings in one call at surface depth (one call and the critic at standard); the profiles are the witnesses, the focal
text the only full text. Every row anchors verbatim in a profile or in the focal text; the walls check.

| engine | reads | rows |
|---|---|---|
| `oeuvre_trajectory` — the author's research agendas and turns | all | T1 agenda (question · span of works · key concepts · interlocutors) · T2 turn (between which agendas, when, what changed: object, question, method, interlocutors) · T3 place: the focal text's position — opening · culmination · middle · end · reorientation · outlier |
| `citation_shift` — what the focal text cites against the rest | all | C1 first_cited (a work or person cited here for the first time) · C2 dropped (cited before, absent here) · C3 carried · C4 anomaly (a cluster unique to this text) · C5 unexamined (cited here, not held or not a thinker in the Referee) — each with `held: yes|no` and `in_referee: yes|no|unknown` from the packet |
| `retrospective_reading` — the text as the culmination of what came before | focal + before | R1 inheritance (what it takes from which earlier text) · R2 resolution (which earlier problem or tension it answers) · R3 interlocutor (whom it argues with, inherited or new) · R4 verdict: culmination · continuation · departure |
| `prospective_reading` — the text as step one of a journey | focal + after | P1 seed (what in it is developed later, where) · P2 developed_into (which later works take it up, how) · P3 abandoned (what is not taken up) · P4 verdict: origin · way_station · dead_end |
| `epistemic_rupture` — does it mark a rupture, and between which halves | all | E1 continuity (what persists across the text) · E2 break (what changes at it: object, question, method, interlocutors, concepts — the two halves named) · E3 verdict: rupture · reorientation · deepening · continuity · outlier, with `halves: <before-half> vs <after-half>` · E4 test (what would settle it) |
| `oeuvre_position_memo` — the holistic reading | the upstream ledgers + focal | the memo: one paragraph per reading (retrospective, prospective, holistic), the verdicts joined, the three to five texts to read next and why, the actions the findings license (§5); M1 position (the joined verdict) · M2 read_next · M3 open |

Optional steps the recipe can add: `concept_evolution` (the focal text against one earlier work), `revision_presentation` (how later
texts present their revision of it), `evolution_tactics_detector`, `periodization_critic`.

Vocabularies (new, registry-pinned): `oeuvre_positions`, `citation_shift_kinds`, `retrospective_verdicts`, `prospective_verdicts`,
`rupture_verdicts`.

## 4. The workflow (a recipe the dossier lane runs, and a workflow record the Mastermind shows)

Recipe `oeuvre_position` (`src/dossier/recipes.json`): the six engines in order, each step with a `scope` — the key prefixes it reads —
so the retrospective reading never sees a later text and the prospective reading never sees an earlier one. The scope travels from the
path step to the plan phase to the executor (`PhaseExecutionSpec.source_scope`), where the phase runner filters the corpus documents by
prefix before the process runs; a step without a scope reads everything. The same steps are recorded as the workflow
`oeuvre_position` in `src/workflows/definitions/` (the registry the console shows). Posted as an engines-only job (`entry: chosen`,
`path.chain_key: oeuvre_position`, output off), read back as `GET /v1/dossier/jobs/{id}/oeuvre` — the memo and the actions as JSON.

## 5. The actions (the interactive strategy)

An action is a record in the Mastermind (`src/actions/`), registered by the organ that performs it: key · organ · name · when (the
finding kinds that license it, e.g. `citation_shift.unexamined`) · inputs (what the row must supply) · route and method · cost · side
effects · owner · evidence (outcomes written back). The first records: the Referee's thinker lookup, thinker creation, citation harvest,
PDF fetch, cross-citation run; the Stacks' profile a text, bundle texts, citation ledger, explain a citation; the Reporter's person
harvest; the Mastermind's run an engine, run a workflow. `GET /v1/actions?finding=citation_shift.unexamined` answers what can be done
about such a row; the memo renderer fills the inputs from the row (`{thinker: "Guizot, François", work: "…", uid: null}`) and lists the
suggested actions beside the memo; the Stacks' page shows them as buttons; an action run posts its outcome back
(`POST /v1/actions/{key}/outcome`). Nothing runs on its own in the first cut; the owner clicks.

## 6. Order of work

1. This note; the principle into the Mastermind's CLAUDE.md; the Stacks and the Referee asked for theirs.
2. The scope mechanism (path step → plan phase → executor) with a test.
3. The six engines, the five vocabularies, the recipe and the workflow record, the renderer and `/oeuvre`.
4. The actions registry and routes, seeded; the organs register their own.
5. The pilot on Brenner 1985 with the Stacks' profiles (assembled from their local API until their export route exists): all six at
   surface depth; the memo read by the owner; then the Stacks' export route and page.
