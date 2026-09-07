# The Analyst (formerly Analyzer v2) — multi-phase meaning-making service

> Lightweight service serving analytical definitions without execution logic

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
- **Mirrored enumerations change on their owner's word first** (the Referee's, the Stacks'); the registry carries the owner.
- The same principles stand in the Stacks' and the Referee's CLAUDE.md in their words. Design of the first workflow built this way:
  `communications/DESIGN_oeuvre_position_2026-09-07.md`.

## Overview

Analyzer v2 extracts pure analytical definitions from the current Analyzer service:
- **Engine definitions**: Prompts, schemas, and metadata for 160+ analysis engines
- **Paradigm definitions**: 4-layer ontology structures (IE schema)
- **Engine chains**: Multi-engine composition specifications
- **Audience definitions**: Rich multi-section profiles for 5 audience types

This is the "reversed approach" - instead of moving process code TO Visualizer, we extract definitions OUT of Analyzer into this clean service.

## Tech Stack
- Python 3.11+ with FastAPI
- Pydantic v2 for schemas
- JSON files for definitions (no database)
- Anthropic SDK for LLM features (optional, requires ANTHROPIC_API_KEY)

## Quick Reference
- Start: `./start` or `uvicorn src.api.main:app --reload --port 8001`
- Test: `pytest tests/`
- API Docs: http://localhost:8001/docs

## Architecture Notes

```
analyzer-v2/
├── src/
│   ├── engines/           # Engine definitions
│   │   ├── schemas.py     # EngineDefinition Pydantic model
│   │   ├── registry.py    # EngineRegistry - loads from JSON
│   │   └── definitions/   # 160+ JSON files (one per engine)
│   │
│   ├── paradigms/         # Paradigm definitions (IE 4-layer)
│   │   ├── schemas.py     # ParadigmDefinition model
│   │   ├── registry.py    # ParadigmRegistry
│   │   └── instances/     # JSON files (marxist.json, etc.)
│   │
│   ├── chains/            # Engine chain specifications
│   │   ├── schemas.py     # EngineChainSpec model
│   │   ├── registry.py    # ChainRegistry
│   │   └── definitions/   # JSON files
│   │
│   ├── audiences/         # Audience definitions (first-class entity)
│   │   ├── schemas.py     # AudienceDefinition model (8 sub-models)
│   │   ├── registry.py    # AudienceRegistry (CRUD + guidance/vocab/weight)
│   │   └── definitions/   # 5 JSON files (analyst, executive, researcher, activist, social_movements)
│   │
│   ├── views/             # View definitions (rendering layer)
│   │   ├── schemas.py     # ViewDefinition, DataSourceRef, TransformationSpec
│   │   ├── registry.py    # ViewRegistry (CRUD + compose_tree)
│   │   ├── pattern_schemas.py  # ViewPattern reusable templates
│   │   ├── pattern_registry.py # PatternRegistry
│   │   ├── definitions/   # 21 JSON files (genealogy views)
│   │   └── patterns/      # 6 JSON files (reusable view patterns)
│   │
│   ├── renderers/         # Renderer definitions (first-class catalog)
│   │   ├── schemas.py     # RendererDefinition, RendererSummary, SectionRendererHint
│   │   ├── registry.py    # RendererRegistry (CRUD + for_stance/for_data_shape/for_app via ConsumerRegistry)
│   │   └── definitions/   # 9 JSON files (accordion, card_grid, prose, table, etc.)
│   │
│   ├── sub_renderers/     # Sub-renderer definitions (atomic UI components)
│   │   ├── schemas.py     # SubRendererDefinition model
│   │   ├── registry.py    # SubRendererRegistry (for_parent/for_data_shape)
│   │   └── definitions/   # 11 JSON files (chip_grid, mini_card_list, etc.)
│   │
│   ├── consumers/         # Consumer app capability declarations
│   │   ├── schemas.py     # ConsumerDefinition model
│   │   ├── registry.py    # ConsumerRegistry (renderers_for_consumer)
│   │   └── definitions/   # 3 JSON files (the-critic, visualizer, analyzer-mgmt)
│   │
│   ├── orchestrator/      # LLM-powered plan generation (Milestone 1)
│   │   ├── schemas.py     # WorkflowExecutionPlan, PhaseExecutionSpec
│   │   ├── catalog.py     # Parameterized capability catalog assembly
│   │   ├── planner.py     # Templated system prompt + Claude plan generation
│   │   └── plans/         # File-based plan storage (JSON)
│   │
│   ├── executor/          # Plan-driven workflow execution (Milestone 2)
│   │   ├── schemas.py     # ExecutorJob, PhaseResult, EngineCallResult
│   │   ├── db.py          # Dual-backend DB (Postgres + SQLite)
│   │   ├── engine_runner.py  # Atomic LLM calls with streaming/retry
│   │   ├── context_broker.py # Cross-phase context assembly
│   │   ├── chain_runner.py   # Sequential chain execution
│   │   ├── phase_runner.py   # Phase resolution + per-work iteration
│   │   ├── workflow_runner.py # DAG execution with parallel phases
│   │   ├── job_manager.py    # Job lifecycle + cancellation
│   │   ├── output_store.py   # Prose output persistence
│   │   └── document_store.py # Document text storage
│   │
│   └── api/               # FastAPI application
│       ├── main.py        # App entry point
│       └── routes/        # Endpoint handlers
│
└── scripts/
    └── extract_engines.py # Script to extract from current Analyzer
```

## API Endpoints

```
GET  /v1/engines                     # List all engines (has_profile flag)
GET  /v1/engines/{key}               # Full engine definition
GET  /v1/engines/{key}/extraction-prompt
GET  /v1/engines/{key}/curation-prompt
GET  /v1/engines/{key}/schema
GET  /v1/engines/{key}/profile       # Get engine profile/about
PUT  /v1/engines/{key}/profile       # Save engine profile
DELETE /v1/engines/{key}/profile     # Delete engine profile
GET  /v1/engines/category/{category}

GET  /v1/paradigms                   # List all paradigms
GET  /v1/paradigms/{key}             # Full paradigm (4-layer)
GET  /v1/paradigms/{key}/primer      # LLM-ready text
GET  /v1/paradigms/{key}/engines
GET  /v1/paradigms/{key}/critique-patterns

GET  /v1/chains                      # List chains
GET  /v1/chains/{key}                # Chain specification

GET  /v1/audiences                   # List all audiences
GET  /v1/audiences/{key}             # Full audience definition
GET  /v1/audiences/{key}/identity    # Identity/profile section
GET  /v1/audiences/{key}/engine-affinities
GET  /v1/audiences/{key}/visual-style
GET  /v1/audiences/{key}/textual-style
GET  /v1/audiences/{key}/curation
GET  /v1/audiences/{key}/vocabulary
GET  /v1/audiences/{key}/guidance    # Composed guidance block
GET  /v1/audiences/{key}/translate/{term}
GET  /v1/audiences/{key}/engine-weight/{engine_key}
PUT  /v1/audiences/{key}             # Update audience
POST /v1/audiences                   # Create audience
DELETE /v1/audiences/{key}           # Delete audience

GET  /v1/views                         # List all views (with ?app=X&page=Y)
GET  /v1/views/{key}                   # Single view definition
GET  /v1/views/compose/{app}/{page}    # Tree of views for a page (primary consumer endpoint)
GET  /v1/views/for-workflow/{wf_key}   # Views referencing a workflow
POST /v1/views                         # Create view
PUT  /v1/views/{key}                   # Update view
DELETE /v1/views/{key}                 # Delete view
POST /v1/views/generate                # LLM-powered view generation from pattern + engine

GET  /v1/views/patterns                  # List view pattern summaries
GET  /v1/views/patterns/{key}            # Full view pattern
GET  /v1/views/patterns/for-renderer/{type}  # Patterns by renderer
GET  /v1/views/patterns/for-data-shape/{shape}  # Patterns by data shape

# Transformations
GET  /v1/transformations                    # List templates (?type=&tag=)
GET  /v1/transformations/{key}              # Full template
GET  /v1/transformations/for-engine/{key}   # Templates for engine
GET  /v1/transformations/for-renderer/{type}  # Templates for renderer
GET  /v1/transformations/for-primitive/{key}  # Templates for primitive
GET  /v1/transformations/for-pattern        # Cross-domain query (?domain=&data_shape=&renderer_type=)
POST /v1/transformations                    # Create template
PUT  /v1/transformations/{key}              # Update template
DELETE /v1/transformations/{key}            # Delete template
POST /v1/transformations/generate           # LLM-powered template generation (v2: rich metadata)
POST /v1/transformations/execute            # Execute transformation on data

GET  /v1/renderers                       # List all renderers (summary)
GET  /v1/renderers/{key}                 # Full renderer definition
GET  /v1/renderers/for-stance/{stance}   # Renderers by stance affinity
GET  /v1/renderers/for-app/{app}         # Renderers supported by app (via ConsumerRegistry)
POST /v1/renderers                       # Create renderer
PUT  /v1/renderers/{key}                 # Update renderer
DELETE /v1/renderers/{key}               # Delete renderer

GET  /v1/sub-renderers                   # List sub-renderer summaries
GET  /v1/sub-renderers/{key}             # Full sub-renderer definition
GET  /v1/sub-renderers/for-parent/{type} # Sub-renderers for a parent renderer
GET  /v1/sub-renderers/for-data-shape/{shape}  # Sub-renderers by data shape

GET  /v1/consumers                       # List consumer summaries
GET  /v1/consumers/{key}                 # Full consumer definition
GET  /v1/consumers/{key}/renderers       # Supported renderer definitions

GET  /v1/operations/stances            # List stances (with ?type=analytical|presentation)
GET  /v1/operations/stances/{key}      # Get stance
GET  /v1/operations/stances/{key}/renderers  # Preferred renderers for a stance

GET  /v1/llm/status                  # Check LLM availability
POST /v1/llm/profile-generate        # Generate profile with AI
POST /v1/llm/profile-suggestions     # Get AI suggestions for profile
POST /v1/chains/recommend            # LLM recommends chain

# Orchestrator
GET  /v1/orchestrator/capability-catalog  # Full capability catalog
POST /v1/orchestrator/plan                # Generate new plan (Claude Opus)
GET  /v1/orchestrator/plans               # List plans
GET  /v1/orchestrator/plans/{plan_id}     # Get plan
PUT  /v1/orchestrator/plans/{plan_id}     # Update plan
POST /v1/orchestrator/plans/{plan_id}/refine  # LLM-assisted refinement

# Executor
POST /v1/executor/jobs                    # Start execution from plan_id
GET  /v1/executor/jobs                    # List jobs
GET  /v1/executor/jobs/{job_id}           # Poll status + progress
POST /v1/executor/jobs/{job_id}/cancel    # Cancel running job
GET  /v1/executor/jobs/{job_id}/results   # Phase output summaries
GET  /v1/executor/jobs/{job_id}/phases/{n}  # Full phase prose
DELETE /v1/executor/jobs/{job_id}         # Delete completed job
POST /v1/executor/documents               # Upload document text
GET  /v1/executor/documents               # List documents
GET  /v1/executor/documents/{doc_id}      # Retrieve document
DELETE /v1/executor/documents/{doc_id}    # Delete document

# Runs (Stage 4 unified run contract)
GET  /v1/runs/by-job/{job_id}                        # Joined run detail: executor + preparation + result state (?consumer_key=)
GET  /v1/runs/discovery                              # Batch run discovery (?project_id=&workflow_key=&consumer_key=&scope=active|recent|all&selected_source_thinker_id=&limit=)

# Results (Stage 3 restore/discovery authority)
GET  /v1/results/by-job/{job_id}                    # Consumer-facing result manifest
GET  /v1/results/by-job/{job_id}/presentation       # Manifest + assembled presentation (read-only)
POST /v1/results/by-job/{job_id}/refresh-presentation  # Refresh presentation without re-executing
GET  /v1/results/discovery                           # Discover completed results (?project_id=&workflow_key=&consumer_key=&selected_source_thinker_id=&limit=)
POST /v1/results/by-job/{job_id}/attach-project      # Attach project_id to external/imported job

# Organs, doctrine, story desk (The Mastermind, 2026-09-04)
GET  /v1/organs · /v1/organs/by-layer · /v1/organs/{key} · /v1/organs/{key}/engines
GET  /v1/engines?family=&organ=          # families: analytical, storytelling, editing, restructuring, search, rendering, composition, quality, imagination, governance
GET  /v1/engines/{key}/doctrine          # hash-pinned prompt/doctrine files (mirrored organs + the Analyst's desks)
POST /v1/engines/{key}/call              # a light engine call in the request, no dossier job (2026-09-06): sources[] + packet + depth surface|standard + model + spend_cap_usd → rows with the wall's verdicts, receipts, and the engine's shaped JSON (citation_explainer → the Stacks' How / Why here / In the argument)
POST /v1/story/jobs · GET /v1/story/jobs/{id} · GET|POST /v1/story/jobs/{id}/brief · GET /v1/story/jobs/{id}/handoff
GET  /v1/story/handoff-schema · /v1/story/demands
GET  /v1/dossier/jobs/{id}/profiles?shape=shared|native   # reconnaissance profiles in the shared work-profile shape (2026-09-06)
GET  /v1/dossier/jobs/{id}/ledger · /v1/dossier/jobs/{id}/frame · /v1/dossier/jobs/{id}/reread   # every phase's ledger rows parsed by code; the evidential frame as JSON; the owner's references re-read (engine reference_reread over a role=statements source: verdicts holds · holds_in_part · diverges · not_in_text · unverifiable, follow-up questions)
GET  /v1/vocabularies · /v1/vocabularies/{key} · /v1/vocabularies/for-engine/{engine_key}   # the enumerated values the engines answer in (moves, stances, verdicts, kinds, circles), with glosses; consumers read columns from here, never from copies (src/vocabularies/)
GET  /v1/actions[?finding=&organ=] · /v1/actions/finding-kinds · /v1/actions/{key} · POST /v1/actions · POST /v1/actions/suggest {finding, fields} · POST /v1/actions/{key}/outcome   # what an organ can DO in response to a finding (owner 2026-09-07): records with the finding kinds they answer, inputs, route, cost class, gate; suggest() fills a row's inputs (src/actions/)
GET  /v1/dossier/jobs/{id}/oeuvre               # a paper's place in its author's oeuvre (recipe oeuvre_position over a role=oeuvre source: the Stacks' GET /api/authors/{aid}/oeuvre?focal=): verdicts, agendas and turns, citation shifts, the readings, the reading route, the actions the findings license; since 12:45 also `placements`: where the cited persons the Referee does not know belong (engine thinker_placement, the recipe's seventh step: a Referee school by id with evidence, a new school with candidates, or not a candidate), and the suggested actions in the owner's terms (a held work or a known person: nothing; an unknown person: add, placed)
GET  /v1/practices[?task=] · /v1/practices/task-kinds · /v1/practices/{key} · POST /v1/practices (an organ registers a practice its planner knows; only its owner may overwrite it) · POST /v1/practices/{key}/evidence   # how to SEARCH, beside the engines (owner 2026-09-07: 'such tricks have to start living in the Mastermind'): records a planner's packet carries (when · shape · ingredients · yields · misses · evidence), by task kind (person-harvest, paper-discovery, pdf-fetch, work-identity, institution-harvest); a run's yield writes back (src/practices/)
# Dossier source roles: source | evidence_index | plan | profile (a Stacks WorkProfile: the desk starts from it) | statements (a memo's numbered statements against the sources they cite: the fidelity audit's second input) | oeuvre (the Stacks' bundle around a focal text, expanded at the door into focal:/before:/after: documents and the packet)
POST /v1/dossier/jobs/{id}/steps {engine_key, depth?, model?, spend_cap_usd?}   # add one engine step to a finished job: a light call over the job's own documents, its phase appended to the analysis (2026-09-07; thinker_placement over run 3)
PUT  /v1/dossier/admin/blobs/{key} · /v1/dossier/admin/jobs/{id}   # re-hydration (X-Admin-Token)

# Presenter
POST /v1/presenter/refine-views          # Refine view recommendations
POST /v1/presenter/prepare               # Run transformations
GET  /v1/presenter/page/{job_id}         # Complete page presentation
GET  /v1/presenter/view/{job_id}/{view_key}  # Single view data
GET  /v1/presenter/status/{job_id}       # Presentation readiness
POST /v1/presenter/compose               # All-in-one pipeline
POST /v1/presenter/polish                # View-level visual polish
POST /v1/presenter/polish-section        # Per-section polish with user feedback
```

## Documentation
- **CURRENT TASKS**: `docs/CURRENT-TASKS.md` - **READ THIS FIRST** for implementation roadmap
- Feature inventory: `docs/FEATURES.md` (read on demand)
- Change history: `docs/CHANGELOG.md` (read on demand)

## Deployment
- **Render, CAII workspace, project `the-analyst`** (created 2026-09-03): `the-analyst` (this API, Python; https://the-analyst-kcuc.onrender.com; `/health` reports the deployed commit), `the-analyst-desk` (static site built from `web/`; https://the-analyst-desk.onrender.com), `the-analyst-db` (PostgreSQL 16). Repo: https://github.com/yauhenio2025/the-analyst (forked from analyzer-v2 @4d7bb5b). The blueprint `render.yaml` documents the API service; the services were created in the dashboard.
- **The Mastermind** (governance console: the registry of methods, organs, engine editing) is a separate repo, https://github.com/yauhenio2025/analyzer-mgmt (Next.js), deployed as `the-mastermind` (https://the-mastermind.onrender.com). It reads engines, organs, processes and the rest from this API. Its legacy FastAPI + Postgres (`analyzer-mgmt-api` + `theorist-db`, Render project `the-theorist`) still serve its Paradigms pages (incl. branching and lineage), Consumers, Changes, Grids, Rhetoric, Pipelines, the engine editor's update/versions/schema/stage-context calls and its LLM helper buttons (`frontend/src/lib/api.ts`: every `this.get/post` method). Retire only after those are repointed at this API or dropped; data snapshot in `communications/legacy_mgmt_api_snapshot_2026-09-06/`.
- **DO NOT TOUCH** the gsi workspace (client production): analyzer-43fk, visualizer-alu5, analyzer-v2-3blo (pinned to branch `client-frozen-2026-09-03`).
- **Deploys**: `autoDeploy` is ON for `the-analyst` since 2026-09-07 00:45Z (the owner's decision; before that every deploy had been API-triggered by an earlier session, and pushes between 00:12Z and 00:38Z did not deploy). A push to `master` now restarts the API (SIGTERM; in-flight dossier jobs pause at a checkpoint and resume on the new instance), so batch pushes while a job is mid-engine; registry write-back commits carry `[skip render]` and do not deploy. Check `/health`'s commit before assuming a change is live.
- **Definition edits persist through GitHub**: `GITHUB_TOKEN` + `GITHUB_REPO` on the API service (`src/persistence/github_client.py`); `GITHUB_REPO` must be `yauhenio2025/the-analyst`. Set on the CAII service on 2026-09-07 (they were missing since its creation: writes had died at each deploy); `GET /v1/meta/definitions-version` shows `github_enabled`; an env change there needs a manual deploy. The practices registry also writes the executor database, so its records survive a deploy either way.
- **Implementation plan**: `communications/IMPLEMENTATION_TRACKER.md` — READ FIRST. Bugs: `communications/BUG_TRACKING.md`.

## Implementation Roadmap (See docs/CURRENT-TASKS.md for details)

| Phase | Status | Description |
|-------|--------|-------------|
| 1. Create Analyzer v2 | ✓ DONE | FastAPI service, 123 engines, deployed |
| 2. Complete Paradigms | ✓ DONE | 4 paradigms (marxist, brandomian, hegelian_critical, pragmatist_praxis), 12 engines linked |
| 3. Engine Chains | DEFERRED | More chains, LLM recommendation |
| 4. Wire Current Analyzer | ✓ DONE | v2 client added, caching, prompt loading modified |
| 5. Consumer Integration | ✓ DONE | Visualizer MCP paradigm support, IE API client |

**All core phases complete!** The disaggregation is operational.

## Related Projects
- **Current Analyzer**: `/home/evgeny/projects/analyzer` - Will call this v2 API
- **Visualizer**: `/home/evgeny/projects/visualizer` - MCP server, will use paradigms
- **IE**: `/home/evgeny/projects/ie` - Source of paradigm data (mockParadigmData.js)
- **Critic**: Consumer of engine definitions

## Code Conventions
- Use Pydantic v2 models for all data structures
- JSON files for definitions (easy to edit, version control)
- No database - all state from files
- No execution logic - just definitions
