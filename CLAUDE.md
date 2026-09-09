# The Analyst — the Mastermind's API

The Analyst is the API behind the Mastermind: the records that hold the house's reasoning (engines, workflows and recipes, vocabularies,
practices, actions, exhibits), the walls that check what a model wrote against what a source says (shape, never meaning), the dossier
runner that executes a recipe over sources and keeps its rows, and the ledgers that remember what was read and what we did. The organs
(the Stacks, the Referee, the Reporter, gs_revamp) read the records over the API and post their outcomes back. Python 3.11+, FastAPI,
Pydantic v2; records as JSON/YAML files persisted through GitHub; jobs, blobs and ledgers in the executor database (Postgres on Render,
SQLite locally). The Mastermind console (a separate Next.js repo, below) reads all of it.

## Research activities release candidate (2026-09-09)

`release/research-activities-2026-09-09` combines master `c8526042` with constructive
inquiry and question development (`e3b7b0f5`). Integration fix `ab0799e0` makes strict
reading transactions and immutable receipts use the shared compressed blob format;
184 tests across nine focused suites pass. Deployment is authorized and pending.
The primary checkout remains `/home/evgeny/projects/the-analyst`; release integration
is isolated in `/home/evgeny/projects/the-analyst-research-release`. Preserve the primary
checkout's unrelated untracked research artifacts. The two activity design notes and
the Stacks [release record](/home/evgeny/projects/zotero-stacks/communications/2026-09-09_research_activities_release.md)
retain validation and eventual live-verification details.

## Definition of done for research output (standing rule, 2026-09-10)

An inquiry, memo, brief or release is not accepted until a reader who did not produce it has read the answer
against the question and written three lines: the best idea in it; whether that idea is developed with the case
evidence or merely named; what a good answer would say that this one does not. Passing tests, matching hashes,
retained citation counts, deployment receipts and "acceptance receipts" are evidence of transport, not of quality,
and do not close a commission. A review of a review is not a reading. No new gate, receipt or hash check unless it
retires one. Diagnosis and the next experiment: `/home/evgeny/projects/the-reporter/communications/DIAGNOSIS_2026-09-10_why_quality_stalls.md`.

## How we work: where the reasoning lives (Evgeny, 2026-09-07)

- **The upper-level reasoning lives here, in the Mastermind, as records — never as prose scattered in an organ's Python.** Methods
  are engines (`src/engines/capability_definitions` + `src/operationalizations/definitions`: dimensions, answer shapes, method cards);
  the sequences that compose them are workflows and recipes (`src/workflows/definitions`, `src/dossier/recipes.json`, a step may carry a
  `scope` of the sources it reads); the words they answer in are vocabularies (`src/vocabularies`); how to search is practices
  (`src/practices`); what an organ can do in response to a finding is actions (`src/actions`). An organ reads these records over the API
  and keeps no copy; an LLM improves the system by editing a record, not by hunting through code.
- **Each organ does only what it alone can do, and exposes it as routes**: the Stacks — the library, its texts, profiles, citation
  ledgers, bundles; the Referee — thinkers, their works and readers, harvesting and fetching; the Reporter — the open web; gs_revamp —
  paper discovery; the Mastermind — engines, workflows, vocabularies, practices, actions, and the walls that check what a model wrote
  against what a source says (shape, never meaning).
- **Findings map to actions in other organs**: a row of a kind an action declares (a cited work not held, a person unknown to the
  Referee) becomes a suggested action with its inputs filled from the row (`POST /v1/actions/suggest`); the owner clicks, or the system
  runs it under a cap; the organ posts the outcome back.
- **Everything measured writes back** — a practice's yield, an action's outcome, an engine's receipts — where the next planner reads it.
- **Presentation is records too** (Evgeny, 2026-09-07 09:31: a memo must not be a wall of text): the exhibits a page can show — timelines, idea maps, split panels, chips, sidebars, tables, images — are records with when · inputs · medium · renderer · didactic aim, seeds an LLM extrapolates for a new workflow; a planner commissions them from a memo's rows and a reviewer sends back what fails (too intimidating, too detailed, repeats the text) for revision over several rounds, optimising one thing: time to clarity at depth — the reader grasps the argument on the first pass and keeps a model of it; placement is a rule (Evgeny, 11:45: the text is the main dish; only verdict chips stand before the first paragraph, a wide reference folds under a titled line or opens as a modal, never a stack of exhibits at the top); the figure pipeline (primitives, styles, the image fleet in `src/images/providers.py`) and the renderer catalogue (`src/renderers`, `src/sub_renderers`, `src/views/patterns`; built for the Critic and the Visualizer, never fully operationalised — untested until a page uses one) are the means. Design: `communications/DESIGN_presentation_exhibits_2026-09-07.md`.
- **The vision (Evgeny, 2026-09-07 13:55): automate so that he thinks rather than checks and remembers.** "I have a lot of ideas; I draw connections really well, identify new patterns. What we need to be doing is follow-up: due diligence to check whether my hunch is actually developed, and understanding what I would need to move to the next step in my theorizing. When I see a pattern of similarity between two or three thinkers, or my emerging position is about to collide with the position of another thinker — when we see such emergence, we should accelerate it (accelerate the contradictions): make them explicit, make sure I do not miss an encounter with the other party. I need to articulate my position informed by the positions of others, in full awareness of where I am taking a different position than they do. Prefashioning and prestructuring the thinking environment in which this thinking and sharpening happens is exactly what the LLM-driven structuring and background activity should focus on." The July 2026 dictations hold the vision this realises in part: `communications/vision_2026-07/INDEX.md` (verbatim copies; the live corpus is `~/projects/oaas/communications/dictations/`). The distinction maker built from them: `communications/DESIGN_distinction_maker_2026-09-07.md`.
- **Every heavy reading leaves its rows behind, attached to the thinker and the texts (Evgeny, 2026-09-07 18:30: "every time we do a massive API call on primary sources and get only some high-level analysis from it, we should always be saving it and attaching it to this thinker, so that later sessions can skim through it and have a map of what is where — a bottom-up RAG").** The rows a run produces (with their anchors, loci and the texts read) are indexed by person and by text in the readings ledger (`src/readings`, `GET /v1/readings?person=|text=|job=`) the moment a phase finishes; a planner reads the ledger before it spends, feeds what is there as context, and reads only what is new; the Stacks attach the same rows to the author's and the text's records. Design: `communications/DESIGN_readings_and_macro_actions_2026-09-07.md`.
- **The system narrates what we are doing, so that we approve at the level of intent (Evgeny, 18:30: "a self-constructing narrative that always narrates what we do so that macro actions become possible, sparing us the trouble of conducting micro actions… we approve once and that enables ten, fifteen, twenty actions in the background — this is what raising productivity is").** Actions are grouped under intents (expand the network around a thinker, expand the library, expand our horizons, sharpen a position, verify holdings…); an action register holds what we did and what came of it; a narrative engine reads the register and writes the trajectory as a record every session; a macro-actions engine reads a page's suggested actions against the trajectory and the intents and proposes three to five macro actions, each naming the micro actions it enables and their cost; one approval runs them under a cap and their outcomes feed the register. The organs' pages show macro actions first; the micro list folds under them.
- **The move an engine performs has a name (Evgeny, 2026-09-07 19:05: "does this move up the ladder of abstraction have a name/place in the Mastermind's taxonomy?").** Every engine record may carry `operation`, a word from the `operations` vocabulary: `ascent` (many concrete items lifted to a few wholes, each carrying the meaning that licenses the grouping, so one decision at the top covers the many below — a page's sixteen actions as four approvals; his July "buckets"), `descent` (a whole unfolded into its items), `reading`, `placement`, `distinction`, `narration`, `verification`, `composition`; `kind` says how an engine is built, `operation` what it does to its input, and the catalogue can be read by move.
- **Mirrored enumerations change on their owner's word first** (the Referee's, the Stacks'); the registry carries the owner.
- The same principles stand in the Stacks' and the Referee's CLAUDE.md in their words. Design of the first workflow built this way:
  `communications/DESIGN_oeuvre_position_2026-09-07.md`.

## The organs and their seams

- **Research capability programme:** the Stacks repository's `communications/RESEARCH_CAPABILITIES_ROADMAP.md` preserves the original chat-derived A–G recommendations and July additions. Local delivery checkout: `../zotero-stacks-constructive-inquiry`. This organ's `communications/DESIGN_constructive_inquiry_2026-09-08.md` links the current implementation and real-case trial; the first inquiry is not completion of the wider programme.

- **The Stacks** (`~/projects/zotero-stacks`, local at http://127.0.0.1:8765): the library, texts, profiles, citation ledgers, bundles, memos,
  the Brief (dictation, exchange, references, distinction challenges), the oeuvre page. Sends `role: oeuvre` bundles and `role: statements`
  files (a turn or memo against the texts it cites, windowed); reads `/oeuvre`, `/distinctions`, `/encounter`, `/page`, `/readings`,
  `/actions`; posts action outcomes. Several Stacks sessions run at once; each owns lanes — ask before assuming.
- **The Referee** (https://referee-api.onrender.com; keyless `GET /api/public/schools?members=N`, 401 schools): thinkers, works, readers,
  harvesting, fetching, schools and their candidates queues (`POST /api/schools/{id}/candidates` with `evidence` as an object). Owns ten
  action records here (`referee.*`), re-posted on its word; optional inputs end in `?`.
- **The Reporter**: the open web; its practices' yields write back here; its deploy gate (`deploy_when_idle.py`, another machine) deploys
  any head when this API looks idle by `GET /v1/dossier/jobs` statuses — a running page loop shows there as `composing` so idle means idle.
- **gs_revamp**: paper discovery; holds Render API access for this workspace and reads the service events when a deploy needs explaining.
- **The Mastermind console**: https://github.com/yauhenio2025/analyzer-mgmt (Next.js), deployed as https://the-mastermind.onrender.com; its
  legacy FastAPI + Postgres (`analyzer-mgmt-api`, `theorist-db`, Render project `the-theorist`) still serve its Paradigms, Consumers,
  Changes, Grids, Rhetoric, Pipelines pages and the engine editor's update/versions/schema calls — retirement parked (memory note).
- Sessions coordinate over `SendMessage` (ListAgents names them); an organ edits its own CLAUDE.md only on the owner's word in that session.

## What lives here (counts on 2026-09-07)

**Records.** Engines: 273 legacy JSON (`src/engines/definitions`, prompts and schemas of the August catalogue; `home_organ` explicit on 70)
and 86 capability YAMLs (`src/engines/capability_definitions`: problematique, dimensions; `kind` says how an engine is built, `operation`
what it does — the `operations` vocabulary; 24 tagged) with 83 operationalizations (`src/operationalizations/definitions`: the process
with dimensions, answer shapes, method cards, routing by tier) — the families built as records this week: **oeuvre** (7 engines),
**distinction** (interlocutor_position · distinction_draft · distinction_settle · encounter_map · encounter_draft · impact_scan),
**governance** (trajectory_narrative · macro_actions), the **citation** family, the **page** engines (page_planner · page_prose ·
page_reviewer), reference_reread, citation_explainer, hypothesis_evidential_frame. Recipes: 12 in `src/dossier/recipes.json` (a step
may carry `scope`; a sole step may carry `context`); workflows: 20 (`src/workflows/definitions`). Vocabularies: 80 (`src/vocabularies`;
owners the-mastermind 52, the-stacks 17, the-referee 11; a value may carry `routes` per organ; enumerated fields pin to them in the wall
as `vocabulary_drift`, `src/vocabularies/pins.py`). Practices: 34 (`src/practices`; search craft by task kind; yields write back).
Actions: 18 (`src/actions`; referee 10, stacks 5, mastermind 2, reporter 1; `intents` on each; `suggest()` fills a row's inputs; the
register `src/actions/register.py`; macro grouping `src/actions/macro.py`). Exhibits: 9 (`src/exhibits`; placement rules; makers and SVG
by code). Doctrines: `src/engines/doctrines` (hash-pinned prompt files of mirrored organs and this desk's).

**The runner** (`src/dossier`, 35 modules): `POST /v1/dossier/jobs` with sources by role — `source · evidence_index · plan · profile ·
statements · oeuvre` (`src/sources`; the oeuvre door expands a Stacks bundle into focal:/before:/after: documents and the packet with
persons, schools, prior readings; the statements door windows a long source around its statements' terms, `how: search`); the fast lane
runs an engines-only fixed path without reconnaissance or a planner call; the walls (`src/executor/ledger_walls.py`, `process_runner.py`)
verify anchors and report drift; `POST /jobs/{id}/steps` adds one engine to a finished job over its own documents (the caller's documents
and packet blocks ride beside; the recipe's earlier rows travel as `upstream_findings`; a 1.5M-char cap); the blob store keeps pages,
readings, the register; the print desks (spine, tables, figures, plates, compose) and the image fleet (`src/images/providers.py`) are
optional outputs. Renderers by code: `oeuvre.py`, `distinctions.py`, `encounter.py`, `reread.py`, `explainer.py`.

**Presentation** (`src/dossier/page_loop.py`, `src/exhibits`): plan → make → write → review → revise, durable in the blob store and
resumable after a restart; the composer enforces the placement rules by code (text first; chips only before the first paragraph; wide
exhibits folded; ids on hover; the loop's notes folded); `POST /page/recompose` rebuilds a page without a model call; the encounter page
(`encounter_page.py`) is composed by code from rows.

**Memory of the house.** The readings ledger (`src/readings`: every finished phase's rows by person, surname, text and job; an added step
carries `prior_readings`); the action register and the trajectory (`GET /v1/register`, `GET /v1/trajectory?block=1`: what we are doing,
narrated for any organ's planner). Studies: `communications/study/*` (each run's memos, rows in words, pages); designs:
`communications/DESIGN_*.md`; the vision: `communications/vision_2026-07/INDEX.md`.

## Routes that matter (the rest: 390 routes across 39 routers, read `src/api/main.py`)

```
# runs
POST /v1/dossier/jobs {sources[{kind, role, key, title, text}], intent, audience, depth, entry: chosen, path{steps[{engine_key, depth, scope}]}, spend_cap_usd}
GET  /v1/dossier/jobs · /jobs/{id} · /jobs/{id}/ledger · /receipts · /events · /resume · /cancel
POST /v1/dossier/jobs/{id}/steps {engine_key, depth?, packet?, sources?[{key, title, text}], spend_cap_usd?}   # add one engine to a finished job
POST /v1/engines/{key}/call {sources, packet?, depth, model?, spend_cap_usd}                                   # a light call, no job (400K chars)
# renders (JSON by code; the Stacks' pages consume them)
GET  /v1/dossier/jobs/{id}/oeuvre · /distinctions · /encounter?thinker= · /encounter/page · /reread · /frame · /profiles?shape=
GET  /v1/dossier/jobs/{id}/exhibits · /exhibits/{key}.svg · POST|GET /page {audience, rounds, resume?} · /page.json · /page/status · POST /page/recompose
# records
GET  /v1/engines?family=&organ= · /v1/engines/{key}/capability-definition · /doctrine · /v1/operationalizations/{key}
GET  /v1/vocabularies · /{key} · /for-engine/{engine} · GET|POST /v1/practices · /{key}/evidence · GET|POST /v1/exhibits · /{key}/use
GET  /v1/actions?finding=&organ= · POST /v1/actions/suggest {finding, fields} · POST /v1/actions/{key}/outcome {status, inputs, batch?, intent?} · POST /v1/actions/macro {actions, context?}
# memory
GET  /v1/readings?person=|text=|job= · /v1/readings/{job}/{phase} · POST /v1/readings/index/{job}
GET  /v1/register?since=&kind= · POST /v1/register/backfill?refresh= · GET /v1/trajectory · ?block=1 · POST /v1/trajectory/narrate
# health
GET  /health (commit, counts) · GET /v1/meta/definitions-version (github_enabled) · PUT /v1/dossier/admin/blobs/{key} (X-Admin-Token)
```

## Legacy holdings — served, not exercised (say so before building on them)

Built in August 2026 for the Critic and the Visualizer and still mounted: paradigms (5, preloaded, no runner reads them), chains (27, read
by `chain_runner`), audiences (5, read by the catalog and the stage composer), views (33) and patterns (6), renderers (9), sub_renderers
(20), consumers (6), transformations (26), styles, primitives, display, functions (24), objectives (3), projects, variants, feedback, the
presenter (39 modules, 18 routes), the orchestrator (22 modules, 16 routes), results and runs, the story desk (13 routes). None has been
exercised by a page since the Stacks became operational; the page loop uses its own makers. `src/organs` (15 records) and `src/primitives`
are read only by their routes; `src/evaluations` (19 modules) has a router that is **not mounted** — unreachable over HTTP, its tests import
the handlers directly. The `?family=` filter on `/v1/engines` reads the legacy JSON's family (203 of 273 default to analytical), not the
YAMLs'. `docs/CURRENT-TASKS.md` (2026-01) and its "phases" are history; `docs/FEATURES.md` and `docs/CHANGELOG.md` are August inventories.
Retire or re-purpose any of this on the owner's word; until then it is not a place to add.

## Working rules

- **Heavy work goes to Codex Astra in ultra mode** (Evgeny, 2026-09-07 19:45, on the move from Fable to Opus: "utilize codex astra ultra more"): a written brief under `communications/CODEX_PROMPT_*.md`, its own git worktree when a run is live, the review and the records here. In-session: design, records, wiring, coordination.
- Commit per phase, in the house style (a sentence saying what and why; the owner's words and time where a rule came from them). Tests:
  `pytest tests/` (136 files; baseline on this machine ~12 failures and 8 ImportError collections in old modules, none from this week).
- **Deploys**: Render, CAII workspace, project `the-analyst`: `the-analyst` (this API, https://the-analyst-kcuc.onrender.com; `/health`
  reports the commit), `the-analyst-desk` (static, from `web/`), `the-analyst-db` (Postgres 16). `autoDeploy` is ON (since 2026-09-07
  00:45Z): a push to `master` restarts the API; dossier jobs pause at a checkpoint and resume, but a light call or an added step in flight
  dies — batch pushes while anything runs; `[skip render]` on a docs or registry commit is honoured by Render but the Reporter's deploy
  gate also deploys skipped heads when the API looks idle (its fix, the-reporter PR #3, must be pulled on that machine); one mechanism
  or the other is the owner's decision, deferred. Check `/health`'s commit before assuming a change is live.
- **Definition edits persist through GitHub** (`GITHUB_TOKEN` + `GITHUB_REPO=yauhenio2025/the-analyst` on the service; `/v1/meta/
  definitions-version` shows `github_enabled`); the organs' registry write-backs arrive as commits on master — pull before you push.
- **DO NOT TOUCH** the gsi workspace (client production): analyzer-43fk, visualizer-alu5, analyzer-v2-3blo (branch `client-frozen-2026-09-03`).
- Secrets live in this repo's ignored `.env` (the image fleet's keys copied from the Referee's and veo2's `.env` on the owner's word); never
  print them. Never `pkill` with a literal that matches your own command line.
- The walls check shape, never meaning; an LLM improves the system by editing a record; a value outside its vocabulary is drift, reported.
- Spend: the owner said not to worry about cost for proofs of concept; a full oeuvre run is ~$11, a light call cents to a dollar; say what
  a run cost.

## Read next

`communications/IMPLEMENTATION_TRACKER.md` (every arc, dated; read first) · `communications/BUG_TRACKING.md` · the designs
(`DESIGN_oeuvre_position`, `DESIGN_presentation_exhibits`, `DESIGN_distinction_maker`, `DESIGN_readings_and_macro_actions`, all
2026-09-07) · the studies under `communications/study/` (oeuvre_brenner_1985, distinction_turn11, encounter_hintze, trajectory) · the July
vision (`communications/vision_2026-07/INDEX.md`) · the auto-memory (`~/.claude/projects/-home-evgeny-projects-the-analyst/memory/`).
