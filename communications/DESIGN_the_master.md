# The Master — design memo (2026-09-04)

> Owner's ask, morning of the Kering meeting: fold the engine catalogue into a place where clients can see "how the entire workflow is structured… the multiple steps and procedures and operations involved", and set up "the master… where we keep track of all of the processes and all of the engines and all of the big brain operations… a repository of best practices and methods… the central place to which all of those engines connect to get their methods from." Constraints he added: do not scratch what exists; give it an evolutionary door; storytelling, editing, restructuring and search engines must live there just like analysis; preserve The Analyst's running workflows; make it clear we improve processes centrally "without needing to go and edit individual services."

## 1. The decision: evolve the console into The Master, keep The Analyst API as its store

Not a new repo. Three reasons.

1. **The registry already exists and is good.** The Analyst API (`the-analyst`, formerly analyzer-v2) is a pure definitions service: 203 analytical engines as JSON with lineage, dimensions, capabilities, composability and stage context; 11 workflows; 27 chains; 5 paradigms; 5 audiences; 13 stances; and the whole presentation grammar. The console (`analyzer-mgmt`) already renders all of it with editing. Rebuilding a browser would have been the wrong kind of work on demo day and a second source of truth afterwards.
2. **The July-10 dictation named this exact thing** and put it in the analyzer: "a repository of best practices and techniques… tapped from various services." The Master is that repository grown past analysis. Renaming the console is truer than inventing a sibling.
3. **The evolutionary door is a schema, not a UI.** What lets the Master grow is that a method from any organ can be registered with the same record, and that organs can read their methods from it. Both are API-level properties of the registry, so that is where the work went.

So: **The Master = the console (face) + The Analyst API's definitions half (store)**. The Analyst stays the organ that runs dossiers; its desk is untouched; its workflows are the same files they were yesterday.

## 2. What changed today (all additive)

Registry (`the-analyst`):
- `EngineFamily`: analytical · imagination · search · storytelling · editing · restructuring · rendering · composition · quality · governance. `EngineDefinition` and `EngineSummary` gained `family` (default analytical), `home_organ` (default the-analyst), `runs_at`, `lineage_refs`, `status` (live | pilot | designed | frozen), `sync` (native | mirrored | planned). Eleven new `EngineCategory` members for the non-analytical families. `GET /v1/engines?family=&organ=`.
- New entity **organs** (`src/organs/`, `GET /v1/organs`, `/by-layer`, `/{key}`, `/{key}/engines`): fifteen services by layer (sources → search → reasoning → composition → creative → consumers → governance) with role, contributions, families, counts, URLs, status, sync, dependencies and lineage.
- Sixty-five registered methods via `scripts/register_estate_engines.py`: 18 Wirecut passes, 21 de-llm operations, 13 Referee search methods, 1 Reporter loop (designed), 10 of The Analyst's own process engines (reconnaissance, brief, plan, spine, tables, figure planner, plate planner, compose, cross-check, receipts), and 5 imagination/governance engines from the July dictations (generativity module, residual/emergent lens, meta-bridging, moves registry, feedback engine).
- Seven cross-organ **processes** as workflow definitions with `category: process | rendering` and `source_project`: Wirecut broadcast (10 phases), de-llm long-form program (10), the Referee's search loop (8), the Reporter's news brief (6, planned), The Analyst's figure and plate pipelines, and v1's frozen per-image pipeline. Phases link to registered engines.
- Composed-prompt routes return 404 with the lineage for mirrored engines instead of composing nonsense. The dossier catalogue and the orchestrator capability catalogue only ever offered executable (YAML) engines, so planning is unaffected; verified after the change.

Console (`analyzer-mgmt`): wordmark "The Master · method registry"; ESTATE section (Map, Organs, Processes); the Map as landing page (live counts, organs by layer with reachability, "how a dossier is made", processes); organ and process pages; family strip and mirrored badges on engines; a lineage banner on mirrored engine pages.

## 3. The method record (what every engine in the estate shares)

| Field | Meaning |
|---|---|
| `engine_key`, `engine_name`, `description`, `researcher_question` | what it does and the question it answers |
| `family`, `category`, `kind` | coarse family, finer category, operation kind |
| `home_organ`, `runs_at`, `status`, `sync` | who executes it, where, whether it is live, and whether the registry or the organ holds the source |
| `lineage_refs` | `repo:path[:line]` of the doctrine, prompt or code |
| `stage_context`, `canonical_schema`, capability YAML | the analytical machinery (only native engines have real ones) |
| `extraction_focus`, `primary_output_modes` | what comes out |

`sync` is the honest marker of the migration: **native** engines are read from the registry at run time (The Analyst, The Critic); **mirrored** ones are documented here while Wirecut, de-llm and the Referee still read their own files; **planned** ones exist as design.

## 4. The door: how organs come to read from the Master

Phase A (done): mirror. Every method visible, named, linked to its source.
Phase B: **doctrine endpoint** (step 1 DONE 2026-09-04: `scripts/import_doctrines.py` imports every Markdown doctrine named in `lineage_refs` from the organ repos into `src/engines/doctrines/<key>/`, records `doctrine_files` with sha256, and `GET /v1/engines/{key}/doctrine` serves the text; 37 files across 28 engines, mostly Wirecut's prompt library plus the LLM-first doctrines). Step 2: the organs read from here. Wirecut already hashes every `engine/prompts/*.md` into its receipts (`engine/receipts.py:44`); de-llm projects rule packs mechanically; the Referee's doctrine addenda are versioned. Each organ swaps its file read for a registry read behind a flag, keeping the hash in its receipts. Then "modifying them there directly" is literally true.
Phase C: **durable edits**. Console saves currently write JSON to the service's disk and survive only until the next deploy. Add a Postgres overlay table (`definition_overrides`: entity, key, json, author, ts) applied on registry load, with a "promote to git" action. The Analyst already has Postgres.
Phase D: **activity-driven activation** (the OaaS trinity): an activity record chooses which methods to activate and in what output form, as the July-10 dictation asks.
Phase E: the imagination and governance engines stop being design and get capability YAML like the analytical ones (generativity module first; the pilot exists).

## 5. What not to do
- Do not move Wirecut's or de-llm's prompts into the registry by copy-paste; import them at build time from the repos so the source of truth moves only when the organ starts reading from here.
- Do not let the orchestrator plan over mirrored engines; the executable set stays the YAML capability definitions.
- Do not rename Render services before the meeting; the console URL stays `analyzer-mgmt-frontend.onrender.com` until a `the-master` service is created and DNS settled.

## 6. Lineage
- `oaas/communications/dictations/DICTATION_2026-07-10_analyzer_VERBATIM.md` (the centralized brain; theory/activity/ecology; the visualizer's generic rendering steps)
- `oaas/communications/dictations/DICTATION_2026-07-15_process_engines_VERBATIM.md` and its ACTIONS ledger (imagination engines, generativity, moves registry, feedback engine, meta-session)
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` (analyzer-v2 as the intelligence layer; consumers as thin hosts)
- `the-reporter/communications/HUNCHES_AND_ARCHITECTURE.md` (the search loop as the Reporter's core)
- Inventories taken this morning of veo2, de-llm and gs_revamp (engines, pipelines, registries, doctrines) are summarized in the organ and engine definitions.
