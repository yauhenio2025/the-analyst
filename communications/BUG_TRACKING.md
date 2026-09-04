# Bug Tracking — The Analyst

Problem classes, root causes, files fixed. See global rules.

## SDK timeout object mismatch (2026-09-03)

**Problem Class**: Third-party client constructed with an object from the wrong HTTP library after a major SDK upgrade — fails at request time, not at construction.

**Root Cause**: The shared venv moved to `anthropic` 1.x (built on `httpx2`). `src/llm/backends.py` and `src/llm/client.py` still built clients with `httpx.Timeout(...)`; every request then raised `APIConnectionError: Connection error.` — the executor retried 5× per pass and every engine call failed, while direct `anthropic.Timeout` calls worked.

**Files Fixed**:
- `src/llm/backends.py:188,300` — `httpx.Timeout(` → `anthropic.Timeout(` (sync + streaming clients)
- `src/llm/client.py:46` — same in `get_anthropic_client`

**Pattern to Watch For**: `httpx.Timeout(` passed to `anthropic.Anthropic(...)`. Still present (not on the dossier path, not fixed here): `src/orchestrator/planner.py:130,293,452`, `src/orchestrator/sampler.py:168`. The SDK's typed classes (`anthropic.Timeout`) are the safe spelling.

## Orphaned sub-job re-attach (2026-09-03)

**Problem Class**: A job recorded `running` in the DB whose executing thread died with the process; a resumer that trusts the recorded status waits forever.

**Root Cause**: The executor's startup recovery skips jobs younger than 5 minutes (grace period); the dossier resume re-attached to such a job and polled a thread that no longer existed.

**Files Fixed**:
- `src/dossier/analysis.py:_is_live` / `_resume_sub_job` — check `workflow_runner._active_jobs`; if the sub-job is not live, resume it via `start_resume_thread` (completed passes kept).

**Pattern to Watch For**: any "re-attach to running job" logic must verify liveness in-process (or the job's heartbeat), never only the stored status.

## Inherited gitignore swallows front-end source (2026-09-03)

**Problem Class**: Repo-level ignore rules written for one language (Python `lib/`) silently exclude same-named directories in another toolchain, so a branch that builds locally fails on the deploy host with "Cannot find module".

**Root Cause**: `.gitignore:13` (`lib/`) inherited from analyzer-v2; `web/src/lib/*.ts` never entered git on `feat/web`; Render build of `the-analyst-desk` failed with TS2307 on every `../lib/*` import. Same trap exists in analyzer-mgmt (`frontend/src/lib/`, force-added).

**Files Fixed**:
- `.gitignore` — added `!web/src/lib/` and `!web/src/lib/**`
- `web/src/lib/{api,format,hooks,mock,run}.ts` — committed (cec64e1)

**Pattern to Watch For**: after merging a front-end branch, run `git status --short --ignored <dir> | grep '^!!'` before deploying; any `!!` under a source tree is a missing file.

## Mock-contract drift between parallel agents (2026-09-03)

**Problem Class**: Front end built against a written contract + mocks while the backend was built concurrently; field names and wrapping diverged ({jobs:[...]} vs array, name/document_count/char_count vs key/n_docs/chars, composed sections object vs list, filesystem paths, null-before-step fields).

**Root Cause**: no shared fixture generated from the real API; each agent verified only against its own side.

**Files Fixed**: web/src/lib/api.ts (unwrap, normalizeJob, normalizeExemplar, getDossierHtml URL rewrite), web/src/components/RunRail.tsx, web/package.json (404.html SPA fallback).

**Pattern to Watch For**: after any backend schema change, run one live job and open every desk page with Playwright; keep normalization in api.ts, never in pages. Generate web/mock fixtures from a real job JSON.

## Override key silently ignored on the brief choice (2026-09-03)

**Problem Class**: A request field accepted by the client contract but dropped by a generic "merge known keys" loop on the server — no error, no effect.

**Root Cause**: `POST /v1/dossier/jobs/{id}/brief` merged `overrides` with `elif k in data: data[k] = v` over `DossierOptions.model_dump()`. The desk's figures dial sends `figures` at the top level; `figures` lives at `output.figures`, so the key was not in `data` and was discarded silently. The dial had never worked.

**Files Fixed**:
- `src/api/routes/dossier.py` (`choose_brief`) — `figures` is an explicit alias of `output.figures`; `path` is handled as its own override (resolved and stored on the option).

**Pattern to Watch For**: generic key-merge loops over a model dump (`if k in data`) hide contract drift between client and server; unknown override keys should be either mapped explicitly or rejected with a 400, never dropped.

## Hand-edited workflow JSON silently unloaded a workflow (2026-09-03)

**Problem Class**: A definition file that fails Pydantic validation is skipped by the registry with only a log line; the API keeps serving (health showed workflows_loaded 11→10) and every run that references the workflow fails later with "Workflow not found: dossier_standard".

**Root Cause**: a scripted edit assumed phases were keyed by `key`/`figures` text; it copied the Spine phase (whose description mentions figures) and wrote `depends_on_phases: [null]`.

**Files Fixed**: `src/workflows/definitions/dossier_standard.json` (proper Plates phase 7.5 → `dossier_plates`), `tests/test_workflow_definitions_load.py` (every definition must validate and load; dossier_standard's 11 phases in order).

**Pattern to Watch For**: after editing any `definitions/*.json`, run the loader test; watch `workflows_loaded` in `/health` after deploy; the executor error surfaces only at the analysis step of a live run.

## Rendered bytes lost on deploy (2026-09-04)

**Problem Class**: Ephemeral-disk persistence. Outputs written only to the service filesystem on Render (figures, plates, dossier.html/md/pdf) vanish on every deploy; the job text survived because it was already in Postgres.

**Root Cause**: `src/images/storage.py`, `src/dossier/plates.py` and `src/dossier/compose.py` wrote bytes to `FIGURES_DIR` / `DOSSIER_DIR` only. Three registry deploys on the morning of the demo erased both demo dossiers' plates and figures (plate routes returned 404; the desk showed broken images).

**Files Fixed**:
- `src/dossier/blob_store.py` - new `dossier_blobs` table (Postgres bytea / SQLite blob); `put_blob`, `get_blob`, `ensure_file`, `delete_blob`
- `src/images/storage.py:94-175` - write-through in `save_figure`; `_restore_from_blob` used by `figure_path` / `figure_meta`; `delete_figure` removes the blob
- `src/dossier/plates.py` (kept-plate write) and `src/dossier/compose.py:render_all` - write-through for plates and html/md/pdf
- `src/api/routes/dossier.py` - `_file`, `get_figure`, `get_plate_image` restore from blobs; admin endpoints `PUT /v1/dossier/admin/blobs/{key}`, `PUT /v1/dossier/admin/jobs/{id}` (header `X-Admin-Token` = env `ADMIN_TOKEN`)
- `scripts/rehydrate_blobs.py` - pushes `data/dossiers/live-*/` backups to the live service

**Pattern to Watch For**: any `write_bytes` / `write_text` under `data/` on Render without a DB or object-store twin. The desk's mock fixtures and local runs hide this: it only shows after a deploy. Rule: bytes that a URL serves must have a durable twin.

## Anchor quotes verified but not verbatim (2026-09-04)

**Problem Class**: Verification against a normalized copy, serving the un-normalized claim. The wall proved a quote existed under normalization (NFKC, quote folding, hyphen joins, whitespace) and then served the model's own text of the quote; a consumer with a stricter verbatim law (Wirecut) found 5 of 97 "verified" quotes absent.

**Root Cause**: `src/dossier/walls.verify_anchor` returns the candidate quote, not the source's substring.

**Files Fixed**:
- `src/story/steps.py` - `raw_verbatim` (folded search with an offset map back to the raw text) applied after `verify_anchor` at reading time; `reverify_profiles` for existing jobs; `POST /v1/story/jobs/{id}/rebuild-handoff`

**Pattern to Watch For**: any "verified: true" that does not carry the source's bytes. The dossier tables' anchors have the same shape; apply the same re-cut there when a consumer needs byte-verbatim quotes.
