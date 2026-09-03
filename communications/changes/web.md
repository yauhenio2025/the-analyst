# web/ — change notes (agent W1, branch `feat/web`)

> Front end of The Analyst. Everything below lives under `web/`; nothing outside it was touched except this file.

## CHANGELOG — [Unreleased]

### Added
- `web/` — Vite + React 18 + TypeScript app, no UI framework, hand-rolled URL-as-truth router lifted from Wirecut (`web/src/router.ts`). Build → `web/dist` (Render static site; `web/public/_redirects` sends every path to `index.html`). Run/build instructions in `web/README.md`.
- Design tokens in the Kering "Backstage" register (`web/src/tokens.css`): near-black ground `#181b19`, warm off-white serif display, mono small-caps eyebrows, gold `#b3985f` hairlines, sage/sienna verdict inks, zero radius. All rules on tokens in `web/src/styles.css`.
- Pages (`web/src/pages/`, `web/src/steps/`):
  - `/` Library — dossiers grouped Today / This week / Earlier (title, status chip, step, cost); paste-and-go box (textarea or exemplar-bundle cards from `GET /v1/dossier/exemplars`), dials depth / figures / audience, autopilot toggle, `Start · you'll review the brief first`.
  - `/d/:id/sources` Step 1 · Your documents — sources list, per-document profile cards (genre · year · chars, title, author, thesis, three key claims with verbatim quotes), compact run rail; Next enabled at `awaiting_brief`.
  - `/d/:id/brief` Step 2 · The brief — three telling cards (radio; telling paragraph; engines as mono chips; est cost / minutes / output shape; "recommended" from `brief.defaults`), dials, OutcomeButton `Write the draft · ~$X · ~Y min · every step recorded`.
  - `/d/:id/draft` Step 3 · The draft — waiting screen narrated live (RunRail 1–8 with pips, latest narration/detail + last call's model/tokens under the active step, running cost meter, "you can leave"); when delivered, master–detail: left index (sections / tables / figures / analysis phases), right the selected item (Markdown or HTML section, table with anchored cells — hover shows the quote, click pins it in an "on the record" card — figure with caption + provider + cost). `?item=` carries the selection. "Open the console" link.
  - `/d/:id/dossier` Step 4 · Your dossier — record strip (spent / calls / tokens / duration), downloads PDF · MD · HTML, composed HTML in a sandboxed iframe (`srcdoc` from `GET …/dossier.html`), receipts ledger (one row per call) with totals.
  - `/console/:id` Under the hood — header (job, status, analysis sub-job, totals), planner strip (`strategy_rationale` / `decision_trace.overall_strategy_rationale` + alternatives), phase tree phases → chains → engines → passes → calls with live pips (built from events; the mirrored analysis sub-job's events are grafted under "Run the analysis"), node detail with prompt excerpt | output excerpt, model, tokens, cost, duration, per-node event list; timeline (events by seq, kind-coloured); `?view=executive` hides hashes/JSON and shows the run rail + narration + step names + cost. Falls back to `GET /v1/executor/jobs/{id}` when the id is a bare executor job.
- Shared components (`web/src/components/`): `RunRail` (+ `CostMeter`, `Pip`), `OutcomeButton`, `StatusChip`, `Record` (fact tiles), `TableView`, `FigureView`, `Md` (tiny Markdown renderer), `Chips`.
- Data layer (`web/src/lib/`): `api.ts` (fetch client, `API_BASE` from `VITE_API_BASE`, SSE watcher `watchSse` with `?after=` poll fallback, mock seam), `hooks.ts` (`useJob` polls every 2.5 s until done/failed; `useEvents` replays `GET /v1/events/{id}?after=0` then watches the stream), `run.ts` (rail model + console tree derived from events and job status), `format.ts`.
- Mock mode (`VITE_MOCK=1`, or at run time `/?mock=1` → `localStorage.analyst.mock`): `web/src/lib/mock.ts` replays fixtures from `web/mock/` as a timed run — stage A (read + brief, ~8 s) on creation, stage B (plan → analysis → tables → figures → compose, ~46 s) after the brief is chosen; created jobs persist in `sessionStorage` so a reload re-attaches; `VITE_MOCK_SPEED` scales time. Fixtures: `events.json` (64 RunEvents incl. narration, prompt/output excerpts, mirrored sub-job markers), `profiles.json`, `brief.json` (3 tellings), `tables.json` (2 tables, 7 anchors), `figures/fig-1.svg`, `fig-2.svg`, `sections.json` (5), `receipts.json` (15), `plan.json` (2 phases, chain + engines + passes, decision trace), `executor.json`, `exemplars.json` (3 bundles), `jobs.json` (4 seeded shelf rows: done ×2, awaiting_brief, failed), `dossier.html`.
- Screenshots: `web/docs/screens/` (see list below).

### Contract assumptions (verify against the dossier/events agents)
- `GET /v1/dossier/jobs/{id}.profiles[]` = `{doc_key, title, year?, author?, genre?, chars?, thesis, key_claims[{claim, quote}]}`.
- `brief.defaults` = `{option_key?, audience?, depth?, figures?}`; `POST …/brief` body `{option_key, overrides:{audience, depth, figures}}` and it returns the updated `DossierJob`.
- `receipts[]` rows carry `{seq, ts, phase, engine, model, input_tokens, output_tokens, cost_usd, duration_ms, prompt_hash}` (rendered defensively — any missing field shows "—").
- `paths.{html,pdf,md}` are absolute or `/v1/...` paths; absent → `/v1/dossier/jobs/{id}/dossier.{ext}`.
- Dossier-level events carry the status name in `phase` (`reconnaissance`, `awaiting_brief`, `planning`, `analysis`, `tables`, `figures`, `composing`); any event with an engine/chain/pass but a non-status phase folds into "Run the analysis". Mirrored analysis sub-job events are fetched separately from `/v1/events/{analysis_job_id}` and grafted under that step on the console (deduped by kind+engine+pass+ts).
- `call_started` carries `prompt_excerpt`/`prompt_hash`; `call_finished` carries `output_excerpt` + tokens/cost/duration. `artifact` events carry `payload_json` like `{"table_key":"t1"}` / `{"figure_key":"f1"}`.
- SSE: `GET /v1/events/{id}/stream?after=N`, event name `run_event` (also accepts unnamed `message`); the stream closes after `job_finished`/`job_failed`; on transport error the client polls `GET /v1/events/{id}?after=`.
- Sources of kind `exemplar` (`{kind:"exemplar", key}`) are sent as-is; the paste fallback is not yet implemented (see "left").
- Orchestrator plan read defensively: `strategy_rationale ?? decision_trace.overall_strategy_rationale ?? strategy_summary`; alternatives from `alternatives_considered ?? decision_trace.phase_decisions[].alternatives_considered`.
- `API_BASE` default `https://the-analyst-kcuc.onrender.com` (per coordinator, 2026-09-03); local `http://127.0.0.1:8013`.

### Verified (Playwright, mock mode, 2026-09-03)
- 1280×900: library → paste → sources (profiles + rail) → brief (cards, dials, priced button) → draft (waiting screen narrated live; then master–detail; table anchor hover/pin) → dossier (iframe, downloads, receipts) → console (tree, node detail, strategy strip, timeline, executive toggle). No console errors, no horizontal scroll on any page.
- 390×844: library, brief, draft (table), dossier, console — no horizontal scroll (wide tables scroll inside `.table-scroll`).
- `npm run build` succeeds (dist ≈ 300 KB; mock chunk code-split).

### Fixed during verification
- Brief → draft redirect race: the router store renders synchronously on `navigate()`, so the landing check saw the stale job and bounced back to `/brief`; the chosen job is now committed with `flushSync` before navigating (`web/src/App.tsx`).
- Console pass/call detail showed the prompt as "—": the prompt rides `call_started`, the output `call_finished` (`web/src/pages/Console.tsx`).
- Sticky action dock overlapped the dials in full-page views — removed sticky (`web/src/styles.css`).
- Mock: a stopped run kept step 1; it now keeps the step it stopped in. Pasted-paragraph fallback title stops at the first sentence.
- Phone width: shelf rows wrap badges to a second line; titles wrap instead of ellipsising.

### Left / next
- Exemplar-source 400 fallback (paste the bundle text) — needs `GET /v1/dossier/exemplars/{key}` or a text field on the exemplar; not in the contract yet.
- Upload (.pdf/.docx) and stacks view/uids pickers in Step 1 (P1 in the tracker).
- Per-item "sharpen / regenerate" on the draft; figure A/B; spend cap dial.
- Live SSE tested against the mock only — the real `run_event` framing should be smoke-tested once `feat/events` lands.
- i18n (EN/FR) not started.

## FEATURES (entries for docs/FEATURES.md)

### Web · Library
- **Status**: Active · **Entry points**: `web/src/pages/Library.tsx`, `web/src/App.tsx` (shell) · **Added**: 2026-09-03
### Web · Four steps (sources / brief / draft / dossier)
- **Status**: Active · **Entry points**: `web/src/steps/SourcesStep.tsx`, `BriefStep.tsx`, `DraftStep.tsx`, `DossierStep.tsx`; router `web/src/router.ts` · **Added**: 2026-09-03
### Web · Run rail + live narration
- **Status**: Active · **Entry points**: `web/src/components/RunRail.tsx`, `web/src/lib/run.ts` (`buildRail`), `web/src/lib/hooks.ts` (`useEvents`), `web/src/lib/api.ts` (`watchSse`) · **Added**: 2026-09-03
### Web · Console (under the hood)
- **Status**: Active · **Entry points**: `web/src/pages/Console.tsx`, `web/src/lib/run.ts` (`buildTree`) · **Added**: 2026-09-03
### Web · Mock replay
- **Status**: Active · **Entry points**: `web/src/lib/mock.ts`, fixtures `web/mock/*` · **Added**: 2026-09-03

## Screenshots (`web/docs/screens/`)
- `01-library.png` — the shelf + paste-and-go box (1280)
- `02-brief.png` — three tellings, dials, priced button (1280)
- `03-draft-waiting.png` — live narrated waiting screen, rail with pips, cost meter (1280)
- `04-draft-table.png` — master–detail, table with a pinned anchor quote (1280)
- `05-dossier.png` — record strip, downloads, composed HTML, receipts (1280)
- `06-console.png` — phase tree, node prompt|output, planner strip (1280)
