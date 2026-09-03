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
