# Snapshot of the legacy analyzer-mgmt API (2026-09-06)

Read-only export of everything `https://analyzer-mgmt-api.onrender.com/api` still served on 2026-09-06, taken before that service and its Postgres are retired. The Mastermind console (`yauhenio2025/analyzer-mgmt`, https://the-mastermind.onrender.com) reads engines, organs, processes and the rest from the Analyst's API; its Paradigms pages (incl. branching and lineage), Consumers, Changes, Grids, Rhetoric, Pipelines, the engine editor's update/versions/schema/stage-context/restore and the LLM helper buttons still go through this legacy backend (`api.ts`: every `this.get/post` method of `new ApiClient(API_BASE)`).

| file | records | note |
|---|---:|---|
| `grids.json`, `grids_full.json` | 2 | list and full records |
| `pipelines.json`, `pipelines_full.json` | 19 | list and full records (stages included) |
| `rhetoric.json`, `rhetoric_full.json` | 18 | rhetoric schemas; no counterpart in the Analyst |
| `paradigms.json`, `paradigms_full.json` | 5 | the Analyst holds the same five under `src/paradigms/instances/` |
| `engines.json` | 156 | the legacy engine list (analyzer-v2 era); the Analyst's `src/engines/definitions/` is the authority |
| `changes.json`, `consumers.json` | 0 | empty |

Nothing here is read by code. It exists so the database can be deleted without losing the grids, pipelines and rhetoric records.
