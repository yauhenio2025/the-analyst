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
