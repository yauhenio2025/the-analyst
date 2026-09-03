# Dossier agent (E3) — change notes

> Branch `feat/dossier`. Product: "document(s) in → multi-step meaning-making → text + tables + figures out",
> every step recorded. Contract: `communications/IMPLEMENTATION_TRACKER.md` §2/§4 and the E3 brief.

## Changelog

### Added
- **Dossier workflow (8 recorded steps)** — `src/dossier/runner.py` runs reconnaissance → brief → plan → analysis →
  tables → figures → compose → receipts in a daemon thread; the job row is persisted after every step and
  `resume(job_id)` restarts from the recorded step (veo2 `ops` pattern: params stored verbatim).
- **Executor-backed analysis** — `src/dossier/analysis.py` stores the corpus as one target document, creates an
  executor job from the saved `WorkflowExecutionPlan` (in-process `create_job` + `start_execution_thread`, the same
  path as `POST /v1/executor/jobs`), polls it every 2 s, mirrors its events into the dossier stream
  (`payload_json.source_job_id`), and turns every `phase_outputs` row into a receipt.
- **Executable-engine planning** — `src/dossier/plan.py` enumerates engines with capability YAML at runtime
  (`EngineRegistry.list_capability_definitions`, minus `aoi_*`/`genealogy_*` which presume a source-thinker
  structure), lets Sonnet pick from that list under a JSON schema, and code-enforces the depth policy
  (simple = 1 engine × 1 pass, medium = 2-3 engines chained @surface, advanced = 3-4 engines @standard + synthesis).
  Analysis phases are numbered 4.1, 4.2, … with `depends_on` chaining so the context broker feeds each phase the prior prose.
- **Anchor walls** — `src/dossier/walls.py`: normalized (NFKC, quotes/dashes, whitespace, line-break hyphenation)
  substring test; trims a failing quote from the end down to 6 words/40 chars; re-keys a quote found in another
  document; drops table rows with no verified anchor (`rows_dropped` recorded) and un-footnotes prose claims.
- **Compose** — `src/dossier/compose.py` + `templates/dossier.html.j2`: sections call (anchored claims, `{{n}}`
  markers) → print-friendly serif HTML with real `<table>`/`<figure>`, an "Anchors" list and a "How this was made"
  appendix (steps, engines, models, tokens, cost) → PDF via weasyprint → Markdown. Files under
  `DOSSIER_DIR/<job_id>/` (default `data/dossiers/`).
- **Receipts** — `src/dossier/receipts.py` (lifted from veo2): one row per LLM/image call with prompt/result hashes,
  a price table (Sonnet 4.6 std + long-context tiers, Haiku, Opus, Gemini; unknown models flagged UNPRICED), totals per step.
- **Events wrapper** — `src/dossier/events.py`: lazy import of `src.events.store.append_event/list_events`;
  in-memory fallback so runs and tests never depend on the events package.
- **Sources** — `src/sources/{schemas,stacks,resolve}.py`: `SourceSpec` (paste|upload|stacks_export|stacks_view|
  stacks_uids|exemplar), stacks `POST {STACKS_URL}/api/export` with a clear `StacksUnavailable` when the local
  service is unreachable, `split_stacks_export` on the `===== [n/N] … =====` headers (CONTENTS block skipped,
  duplicates deduped), auto-split of pasted exports.
- **API** — `src/api/routes/dossier.py`: `POST/GET /v1/dossier/jobs`, `GET /jobs/{id}`, `GET/POST /jobs/{id}/brief`,
  `GET /jobs/{id}/events?after=` (JSON poll), `GET /jobs/{id}/receipts`, `GET /jobs/{id}/dossier.{html,pdf,md}`,
  `GET /jobs/{id}/figures/{filename}`, `POST /jobs/{id}/cancel`, `POST /jobs/{id}/resume`, `GET /exemplars`.
- **Workflow definition** — `src/workflows/definitions/dossier_standard.json` (8 `function_key` phases; phase 4
  carries `context_parameters.executor_sub_plan`) — appears in `GET /v1/workflows`.
- **Tests** — `tests/test_sources_split.py` (3-item header fixture, tolerant header parsing, paste auto-split),
  `tests/test_dossier_tables_wall.py` (normalization, exact/typography/line-break anchors, re-keying, trimming, row dropping).
- `data/exemplars/README.md` (exemplar texts themselves are git-ignored).

### Changed
- `.gitignore`: `data/*` ignored except `data/exemplars/README.md`.

## FEATURES (file:line)
| Feature | Entry points |
|---|---|
| Dossier job model / statuses | `src/dossier/schemas.py` (`DossierJob`, `STATUSES`, `STEPS`) |
| Job store (`dossier_jobs` table, both DB backends) | `src/dossier/store.py:ensure_table`, `create_job`, `get_job`, `list_jobs`, `update_job`, `append_receipt` |
| Runner (thread, resume, cancel) | `src/dossier/runner.py:start`, `resume`, `cancel`, `_run_step` |
| Step 1 reconnaissance | `src/dossier/reconnaissance.py:run_reconnaissance` |
| Step 2 brief | `src/dossier/brief.py:run_brief`, `estimate_option` |
| Step 3 plan | `src/dossier/plan.py:run_plan`, `_enforce_policy`, `build_executor_plan` |
| Step 4 analysis (executor) | `src/dossier/analysis.py:run_analysis`, `_start_sub_job`, `_mirror_events`, `_collect` |
| Step 5 tables | `src/dossier/tables.py:run_tables` |
| Step 6 figures | `src/dossier/figures.py:plan_figures`, `_generate_one`, `run_figures` |
| Step 7 compose | `src/dossier/compose.py:write_sections`, `render_html`, `render_markdown`, `render_all` |
| Step 8 receipts | `src/dossier/runner.py` (`receipts` branch), `src/dossier/store.py:compute_totals` |
| LLM helper (forced-tool JSON, 1M path, events+receipts) | `src/dossier/llm.py:call_json`, `call_text` |
| Walls | `src/dossier/walls.py:verify_anchor`, `verify_table` |
| Sources | `src/sources/stacks.py:split_stacks_export`, `export_view`, `export_uids`; `src/sources/resolve.py:resolve_sources`, `list_exemplars` |
| Routes | `src/api/routes/dossier.py` |
| Workflow definition | `src/workflows/definitions/dossier_standard.json` |

## Dependencies
No new Python packages: Jinja2, weasyprint, anthropic, httpx were already in `requirements.txt`.
Env: `ANTHROPIC_API_KEY`, `DOSSIER_MODEL` (default `claude-sonnet-4-6`), `DOSSIER_DIR`, `EXEMPLARS_DIR`,
`STACKS_URL`, `DOSSIER_ANALYSIS_TIMEOUT_S` (default 5400), plus the images package's `FIGURES_DIR` and provider keys.

## Timings / costs
(filled in below after the verification runs)

## Deviations from the contract
- `FigureBrief.register` is stored as `visual_register` (Pydantic v2 warns that `register` shadows `ABCMeta.register`);
  the LLM tool schema still uses `register`, and it is coerced to one of the images package's known registers.
- Source kind `exemplar` (+ `name`) added so the front end can start a run from `GET /v1/dossier/exemplars` with one click.
- `GET /v1/dossier/jobs/{id}/events` is a JSON poll (`?after=seq`), not SSE — SSE belongs to the events agent's route;
  this endpoint reads the same store (or the in-memory fallback when the store is absent).
- Status while the brief is being written is `reconnaissance` (step = `brief`) — the contract's status list has no
  `brief` value; `awaiting_brief` follows when not on autopilot.
- Medium depth runs each engine at `surface` (1 pass) so 2-3 engines chain in ~8-12 min on a 350K-char corpus;
  advanced uses `standard` (2 passes) with a pass budget of 10.
- Sub-job event mirroring: when `src.events.store` is absent, `phase_outputs` rows and executor progress-detail changes
  are mirrored as `call_finished` / `narration` events instead, so the console still sees passes land.
