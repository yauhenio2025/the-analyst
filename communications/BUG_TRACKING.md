# Bug Tracking — The Analyst

Problem classes, root causes, files fixed. See global rules.

## Immediate SystemExit on SIGTERM in a process that hosts job threads (2026-09-05, evening)

**Problem Class**: immediate `SystemExit` on SIGTERM in a process that hosts job threads. The web process runs dossier (and executor) jobs as daemon threads; Render sends SIGTERM to the old instance on every push to master (12 deploys on 2026-09-05) and the handler exited at once, so every thread died mid-LLM-call and boot recovery had to redo the whole step (reconnaissance restarted at 1 of 195 profiles before the checkpoint fix; after it, still lost the call in flight plus any step without a checkpoint).

**Root Cause**: the handler treated SIGTERM as "exit now" instead of "stop taking work, finish the unit in hand, then exit"; nothing in the job loops could observe that a shutdown was coming; `render.yaml` left Render's grace period at its 30 s default, so even a polite drain would have been killed.

**Files Fixed**:
- `render.yaml` — `maxShutdownDelaySeconds: 300` (Render's maximum) on the API web service.
- `src/dossier/drain.py` (new) — process-wide flag: `request_drain`, `is_draining`, `reset_drain` (tests), `wait_for_idle(timeout_s, running_count=…)` with a progress log every 15 s; imports nothing from dossier/executor so both can import it.
- `src/api/main.py` — `_sigterm_handler`: request drain, wait up to 270 s for `runner.running_count()` to reach 0 ("SIGTERM: draining N running dossier job(s), up to 270 s" / "drain complete" / "drain timed out; N job(s) resume on the next instance"), second SIGTERM exits at once.
- `src/dossier/runner.py` — `running_count`; `start` returns False while draining; `_pause_for_drain` emits the `drain_pause` note and leaves the status alone; `_run` checks the flag between steps (recording the next step) and catches `DossierDraining`.
- `src/dossier/reconnaissance.py` — drain check between documents and before the corpus map, raising `DossierDraining` right after the per-document checkpoint.
- `src/dossier/common.py` — `DossierDraining`. Tests: `tests/test_sigterm_drain.py`.

**Pattern to Watch For**: a signal handler that raises `SystemExit` in a process with worker threads; a long loop with no shutdown check between units; a deploy platform's grace period left at default. Every unit of work should be able to see "shutting down" and stop after its checkpoint; the handler should wait for the count of running units to hit zero (bounded under the grace period) and log while it waits. Not done here: the executor's own pass loops do not check the flag yet — they rely on `recover_orphaned_jobs` and per-pass persistence.

## Dossier threads die with the instance, nothing resumes them (2026-09-05)

**Problem Class**: long-running work in daemon threads of an auto-deployed web process, without startup recovery for that job family. The executor had `recover_orphaned_jobs`; dossiers did not. A deploy (SIGTERM, new instance) left dossier jobs in `reconnaissance` / `analysis` indefinitely; the caller (The Reporter) saw silence and had to nudge or give up.

**Root Cause**: recovery written for one job family only; long steps with no intermediate checkpoint (195 profiles, one call each, restarted from 1 on resume); cancellation checked only between steps.

**Files Fixed**:
- `src/dossier/runner.py` — `recover_orphaned_dossiers`, `ACTIVE_STATUSES`, `RECOVER_MAX_AGE_HOURS`; `DossierCancelled` handled as a quiet stop.
- `src/api/main.py` — startup hook after the executor recovery.
- `src/dossier/reconnaissance.py` — per-document checkpoint (`partial=True`), resume from it, cancel check per document.
- `src/dossier/common.py` — `DossierCancelled`; `src/dossier/schemas.py` — `Reconnaissance.partial`.

**Pattern to Watch For**: any background thread whose state lives only in the process. Every job family needs: a persisted step, a checkpoint inside any step longer than a minute, and a boot-time sweep that restarts or names what the last instance was doing. Verified live: the first boot after the fix resumed `dossier-c9cead36b44b` and it finished in 11 minutes.

---

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

## Plate wall refusals that one repair cannot cure (2026-09-04)

**Problem Class**: Shape validation stricter than the planner's habits, with a repair pass that re-asks for the whole spec instead of patching the named fields. A commission of two plates (scorecard, timeline_of_shifts) on `dossier-43f34a0abe5c` produced zero plates: `canonical.marks[2]` not `{quadrant, kind, label?}` for the scorecard; title 121 chars (max 120) and narrative sentence count for the timeline; both "still rejected after repair".

**Root Cause**: `src/dossier/plates.py` plate wall + one whole-spec repair; the planner's scorecard marks and long titles recur; the repair does not trim titles mechanically before re-asking.

**Files to Fix** (open): `src/dossier/plates.py` — trim titles to the limit and normalise scorecard marks in code before the wall (shape, not judgment), and make the repair field-scoped like the storyboard patch retry in Wirecut.

**Pattern to Watch For**: a wall that refuses on arithmetic (length, enum, count) should fix the arithmetic itself; judgment repairs are for meaning. Families that passed today: register, flow_map, power_map, framework_map (Kering run), layer_stack (untested).

## Corpus dimensions bypassed by workflow text flattening (2026-09-05, fixed)

**Problem Class**: A multi-document runner receives a single concatenated string through its workflow adapter, so its document-count dispatch silently selects single-document work.

**Root Cause**: `src/executor/chain_runner.py:_run_engine_process` passes `{work_key or "document": document_text}` to both process modes. Corpus extraction in `run_process` requires two or more dictionary entries. Workflow headers inside the string do not preserve that structure.

**Fix and validation**: Carry selected raw-source maps through standard, per-work and chapter phases, chain and single-engine dispatch; keep generated summaries in context. Dossiers persist original document-key bindings alongside the legacy target so resume and desk anchors use the same identities. Missing explicit sources fail before model calls. Final dossier output, engine identity and wall metadata stay aligned by creation time when timestamps are complete. **189 distinct offline tests passed**, including 28 new dispatch regressions. This validates the application path with fake model responses; no paid application corpus run or live deployment observation is claimed. [Implementation and limits](study/FIX_workflow_CORPUS_DISPATCH_2026-09-05.md).

**Pattern to Watch For**: an end-to-end test of the inner runner with a dictionary does not test an outer adapter that flattens the dictionary into text.


## Ideas ledger parser and critic handoff defects (2026-09-05, fixed)

**Problem**: Saved study responses exposed soft-hyphen wraps becoming false spaces, ignored supported counter-anchors, disappearing trim history, ignored explicit weakened-finding replacements, and auxiliary references treated as duplicate or rejected rulings. The quote parser could accept a prefix ending at an internal quotation mark while leaving the displayed remainder unchecked. Desk re-verification could lose the required pair on a corpus-derived finding whose dimension label changed.

**Fix**: Join explicit discretionary wraps before normalization; tokenize declared fields outside quoted prose; require supported complete quotation forms, preserve malformed findings visibly unverified, verify counter-anchors and retain document bindings; apply and serialize explicit critic replacements with original-finding provenance; stop at the requested auxiliary sections; carry declared corpus namespaces through desk ancestry checks. The receipt states when the ledger changes but preceding prose remains original. Future study fingerprints include the shared normalizer. These changes leave semantic support to models/readers and retain the existing deliberate prefix-trimming policy.

**Validation**: 186 affected-path tests plus 13 study-script guard tests passed after exact combined-patch application. Saved-artifact compatibility covers the baseline's 115 corpus calls and 28 final desk handoffs, with separately documented stricter quotation results. [Full audit and replay evidence](study/STUDY_ideas_ANCHOR_AUDIT_2026-09-05.md). The workflow document-map dispatch issue was subsequently fixed and tested separately above.

## Executor result selection and key collisions (2026-09-05, existing, open)

**Problem**: Per-work result keys use `_sanitize_work_key`, so distinct titles can collide in result/presenter keys. Separately, `get_latest_output_for_phase` in `src/executor/output_store.py` orders by pass number even though numbering restarts at each engine; an earlier long engine can outrank a later short engine.

**Scope**: The corpus-dispatch fix uses stable document identities for raw sources and chronological selection inside dossier collection. It does not change these wider result/presenter contracts. Audit their callers and persisted compatibility before repairing them; source-map tests do not establish that output selection elsewhere is fixed.

## Length-clipped anchors lose shortening provenance (2026-09-05, fixed)

**Problem**: Ledger and dossier quote verification clipped anchors to 200 characters before setting `trimmed=False`, so an exact prefix match could appear unshortened. Dossier re-verification also discarded an existing shortening marker. The held-out Hegel run exposed 214→200 and 204→200 cuts, including a word cut in half.

**Fix**: Initialize shortening provenance from original length and retain existing dossier history. Matching and selected prefix text are unchanged; the marker now discloses the cut. **182 affected tests passed**, including four new provenance regressions. The held-out study remains on its archived runtime and original counters. [Evidence and validation](study/FIX_anchor_length_PROVENANCE_2026-09-05.md).

## Completed critic call hid incomplete original-finding coverage (2026-09-05)

**Problem Class:** A completed review call and carried findings can be mistaken for explicit confirmation when the critic omits or renames original IDs.

**Root Cause:** Application defaults carry unmentioned rows and retain separate addition counters, without a dedicated exact-ID coverage measure. In the held-out Conditions/Elling revision, all 28 original IDs were renamed and carried; the prior condition also had one mistyped ID.

**Files Fixed:** `src/executor/ruling_coverage.py` diagnoses exact, unique, valid-status original rulings; `src/executor/process_runner.py` persists the diagnostic for checked and deep paths and adds an incomplete-check notice to checked products. Tests cover both actual ID failure patterns and end-to-end persistence. Existing application rules and prompts are unchanged; this fix exposes incomplete review rather than inventing missing rulings.

**Validation:** 188 affected offline tests passed. See [coverage fix](study/FIX_critic_RULING_COVERAGE_2026-09-05.md). Frozen study receipts retain their original counters.

## Connection pool exhausted under parallel process runs (2026-09-06)

**Problem Class**: A fixed-size resource pool that fails fast under a burst of legitimate parallel work.

**Root Cause**: `psycopg2.pool.ThreadedConnectionPool(maxconn=5)` raises `PoolError` immediately when empty. The deep process mode runs five extraction threads, each persisting events and outputs through `get_connection()`, while the main runner thread and the API's job polling also take connections. Live dossier job `dossier-8577d8159b38` (Deutschmann pair, `revision_presentation` at deep) failed at the analysis step with `PoolError: connection pool exhausted`.

**Files Fixed**:
- `src/executor/db.py:32-33` - `POOL_MAX` (env `DB_POOL_MAX`, default 20) and `POOL_WAIT_SECONDS` (default 60)
- `src/executor/db.py:_getconn_waiting` - waits with backoff for a connection, then raises the original error
- `tests/test_db_pool_wait_2026_09_06.py` - regression tests

**Pattern to Watch For**: any per-call `with get_connection()` inside a `ThreadPoolExecutor` worker; any pool or semaphore whose acquire fails fast rather than waiting; a job status that flips to failed with a resource error while the model calls themselves succeeded.

## Plan lost across a deploy (2026-09-06)

**Problem Class**: State kept on an ephemeral filesystem that a durable record depends on.

**Root Cause**: `src/orchestrator/plans/*.json` is the only store the dossier's analysis step read a plan from (`load_plan`), while Render wipes the disk on every deploy. Live job `dossier-8577d8159b38` failed at phase 4.2 (pool), was resumed after a redeploy, and died with `executor plan not found: plan-b9f1f866bb40` although the executor job row held the full `plan_data`.

**Files Fixed**:
- `src/orchestrator/planner.py:load_plan` - falls back to the executor job's `plan_data` (`job_manager.find_job_by_plan`) and re-materializes the file; invalid data behaves as missing
- `src/dossier/analysis.py:run_analysis` - a failed sub-job with `plan_data` is resumed through `start_resume_thread` (completed passes kept) instead of a fresh sub-job
- `tests/test_plan_durability_2026_09_06.py`

**Pattern to Watch For**: any `Path(__file__).parent / "..."` store written at runtime (plans, planning_decisions, figures, plates) that a later step must read; on Render only the database and blob store persist across deploys.

## Wall that fails a run on a shape collision it could repair (2026-09-06)

**Problem Class**: A shape check raising a fatal error for a condition that arithmetic can resolve.

**Root Cause**: `_require_unique_ids` raised whenever merged ledgers shared an id. Independent critics (per document and across the corpus) both add misses under `V.DOC<n>.F<m>`, so a collision is ordinary. Live job `dossier-8577d8159b38` lost a 33-minute deep phase to `duplicate ledger ids: V.DOC2.F1`.

**Files Fixed**:
- `src/executor/process_runner.py:_dedupe_ids` - later duplicates re-keyed to the next free number of their prefix, `rekeyed-from:` on the row, pairs on the synthesis wall
- `src/executor/process_runner.py:_drop_duplicate_rulings` - a second ruling on one id is dropped and recorded
- `tests/test_corpus_ledger_2026_09_05.py`, `tests/test_anchor_repairs_2026_09_05.py`

**Pattern to Watch For**: any `raise` in a wall for a condition that code could resolve by renaming, dropping or tagging; walls decide shape, they do not abort paid work.

## 2026-09-07 — GitHub persistence is OFF on the live API (writes vanish at the next deploy)

`GET /v1/meta/definitions-version` on https://the-analyst-kcuc.onrender.com reports `persistence: {github_enabled: false}`: `GITHUB_TOKEN` /
`GITHUB_REPO` are not set on the CAII `the-analyst` service (CLAUDE.md's Deployment section says they should be; the service was created
2026-09-03 and the env did not follow). Consequence: every write route — engine profiles, definition edits from the Mastermind console,
and tonight the practices registry (gs_revamp's eight records, `POST /v1/practices`, answered 201 with `persisted: null`) — lands on the
instance's disk only and is wiped by the next deploy. Found 2026-09-07 01:30 when the eight records did not appear in the repo; they were
pulled out of the live API and committed by hand (0967238). Fix: the owner sets `GITHUB_TOKEN` (fine-grained PAT, contents: write on
yauhenio2025/the-analyst) and `GITHUB_REPO=yauhenio2025/the-analyst` on the service. Mitigation shipped tonight: the practices registry also
writes to the executor database (Postgres on Render), which survives deploys, and reads it over the files on load.

RESOLVED 2026-09-07 02:20: at Evgeny's ask the gs_revamp session set `GITHUB_TOKEN` (his gh login token, scope repo) and
`GITHUB_REPO=yauhenio2025/the-analyst` on Render service srv-dacfq315efls73e9hohg and redeployed; `/v1/meta/definitions-version`
reports github_enabled true, and a no-change re-register answered persisted.success with commit a2c648d on master. Env changes on
that service need a manual deploy. A fine-grained PAT can replace the login token later (PUT on the service's GITHUB_TOKEN + redeploy).

## 2026-09-07 — pushes do not deploy the-analyst: autoDeploy was never on

Found when the actions routes did not appear twenty minutes after their push (the Referee session noticed): `/health` stayed at d0d635d
while master was five commits ahead. The gs_revamp session read the Render service: `autoDeploy: no`, and every deploy in its history is
`trigger=api` — an earlier analyst session with Render API access (its Render MCP) was triggering a deploy after each push, which is why
they looked automatic; that stopped at 00:12Z. gs_revamp deployed 090e2d9 by API at 00:38Z. Decision for the owner: turn autoDeploy on
(every push restarts the API; `[skip render]` on registry commits then matters) or keep API-triggered deploys on request. CLAUDE.md's
Deployment section now says so.
