# The Analyst — Implementation Tracker

> Written 2026-09-03 (geekom-mini session). Demo to Kering executives is 2026-09-04.
> This file moves to `the-analyst/communications/IMPLEMENTATION_TRACKER.md` once the repo exists.
> Study reports backing every claim here: `scratchpad/study/{oaas-vision,analyzer-v2,analyzer-mgmt,client-production,veo2,image-models,ganrl-dossiefier-critic,oaas-code}.md`.

## 0. Ground truth (verified 2026-09-03)

| Thing | Where | State |
|---|---|---|
| Client production | Render `gsi` (`tea-d7skqqegvqtc739qibbg`) | `analyzer-43fk`, `analyzer-worker`, `visualizer-alu5`, `analyzer-v2-3blo` (auto-deploys analyzer-v2 `master`, live 4d7bb5b). FROZEN. |
| Analyzer v1 → v2 dependency | `analyzer/src/core/extraction.py:68-118`, `curation.py:111-190`, `src/clients/analyzer_v2.py` | v2 prompts are priority 1 (31K-char composed prompt vs 3K hardcoded). 24h TTL, `None` on error. 17 production engines + `marxist` primer. |
| Client's real usage | gsi `analyzer-db` | 4,827 jobs; mostly `stakeholder_power_interest`, `argument_architecture` as `integrated_report`; `inferential_commitment_mapper` only 27×. Images = `gemini-3-pro-image-preview` 4K via `src/renderers/gemini_image.py:2439`. |
| analyzer-mgmt | Render `caii`, `analyzer-mgmt-frontend` (Next.js) + `analyzer-mgmt-api` | Frontend built with dead default `https://analyzer-v2.onrender.com` (`frontend/src/lib/api.ts:83-84`); `NEXT_PUBLIC_ANALYZER_V2_URL` never set. 17 sidebar pages + Jobs hit v2 directly; 7 hit mgmt-api. |
| analyzer-v2 engines | `src/engines/definitions/*.json` (203) vs `src/engines/capability_definitions/*.yaml` (28) | Executor runs YAML engines only (`chain_runner.py:176-178` skips missing). `concept_analysis_12_phase`: 9/12 engines missing. |
| Runnable workflows | `src/workflows/definitions/` (10) | End-to-end: `intellectual_genealogy` (5 phases, 11 engines, ~30 calls, ~1h/book), `anxiety_of_influence_thematic_single_thinker`, `concept_inferential_single_concept` (Brandomian, 4 phases). |
| Under-the-hood data | `/v1/orchestrator/plans/{id}` (rationale, alternatives, decision_trace), `/v1/orchestrator/plans/{id}/pipeline-visualization`, `/v1/executor/jobs/{id}/results`, `/phases/{n}`, `phase_outputs` table | Exists. No per-call event log, no SSE, no console page. |
| Image adapter | `veo2/engine/images.py:45-289` | `generate(provider_key, prompt, *, aspect_ratio, reference_images) -> (bytes, cost)`; Gemini `gemini-3-pro-image`, Seedream `doubao-seedream-5-0-pro-260628`, Qwen `qwen-image-2.0[-pro]`. Keys on this machine: `GOOGLE_VEO_API_KEY`/`GEMINI_API_KEY`, `ARK_API_KEY`, `DASHSCOPE_API_KEY`. |
| Per-image pipeline | `analyzer/src/renderers/gemini_image.py:1753-2549` | scene prose → declutter → style guide/format enforcement → 4K → Claude-vision compliance → R2. |
| Front-end template | `veo2/web/` (`App.tsx`, `router.ts`, `tokens.css`, `steps/*`), `veo2/engine/{ops.py,receipts.py,api.py:5171 SSE}` | Four steps + Library + rooms; ops append `op_events`, SSE `watchOperation`; receipts hash payload/prompt/tool/result/cost. |
| Live phase tree UI | `the-critic/webapp/src/components/PipelineVisualization.tsx`, `components/provenance/*`, `hooks/useBoundedV2Workspace.ts` | phases→chains→engines→passes with live pips, per-pass LLM-call cards, provenance badges. |
| Sources | stacks `POST /api/export` (uids or `view=<id>` search) → text with per-paper headers; virtual views = "bundles" | Bundles in stacks ≈ cross-entity queries in the referee (`backend/app/routers/cross_entity_triage.py`, `cross_query_studies.py`). Both resolve to a set of papers. |
| Kering material | `oaas/communications/kering/*`, `oaas/frontend/public/{kering-backstage,kering-fourthfield,practice}.html` (all live on oaas-frontend.onrender.com) | Pitch: "follow the meaning", backstage only, no theory vocabulary for designers, do-not-say card. |

## 1. Decisions (owner) — RESOLVED 2026-09-03

1. DONE — name is **The Analyst**; repo https://github.com/yauhenio2025/the-analyst; Postgres `the-analyst-db` (dpg-dacfn3ijnfac73cddr2g-a) + web service on CAII via mcp__render (owner's personal Render key is gsi-only).
   ORIGINAL: Create private GitHub repo `yauhenio2025/the-analyst` (fork of analyzer-v2 with history) + CAII services `the-analyst` (web, starter), `the-analyst-db` (Postgres basic-256mb), `the-analyst-web` (static site). ≈ $20/mo.
2. DONE — branch pushed and `analyzer-v2-3blo` pinned via REST PATCH (200) on 2026-09-03.
   ORIGINAL: Freeze gsi: push branch `client-frozen-2026-09-03` (= 4d7bb5b) to analyzer-v2; pin `analyzer-v2-3blo` to it (Render dashboard → Settings → Branch, or REST `PATCH /v1/services/srv-d9ph2gdbedkc73c3967g {"branch": ...}` with an API key).
3. Product working name (default: "The Analyst").
4. DONE — owner wants MULTIPLE inputs per run; exemplar = 5 fashion papers from the stacks (`scratchpad/exemplars/fashion_bundle.txt`, 355K chars): Dholakia & Ziliberberg 2024, Kuang et al. 2024, Özdil & Konuralp 2025, Nassar et al. 2021, Hewitt et al. 2024 — theme: how fashion brands legitimate themselves under sustainability and platform pressure. Bundles in the stacks ≈ cross-entity queries in the referee.
   ORIGINAL: Exemplar inputs (default: `oaas/communications/kering/KERING_STUDY_2026-07-19.md` + one fashion-theory article).

## 2. Architecture (target)

```
the-analyst/                      (fork of analyzer-v2 @4d7bb5b; prune later)
├── src/
│   ├── events/                   NEW  per-call event ledger + SSE
│   │   ├── schemas.py            RunEvent{job_id, seq, ts, kind, phase, chain, engine, pass, stance, work_key,
│   │   │                                  model, input_chars, output_chars, input_tokens, output_tokens, cost_usd,
│   │   │                                  prompt_hash, prompt_excerpt, output_excerpt, detail, narrator}
│   │   ├── store.py              table run_events (Postgres/SQLite via executor/db.py); append(), list(job, after_seq)
│   │   ├── narrator.py           Haiku one-liner "what this step is doing and why" from plan rationale + phase spec
│   │   └── sse.py                GET /v1/executor/jobs/{id}/events (SSE, replay from ?after=)
│   ├── images/                   NEW  lifted from veo2/engine/images.py + analyzer gemini_image.py prompt logic
│   │   ├── providers.py          PROVIDERS registry (gemini_pro, gemini_flash, seedream_5_pro, qwen_image_2_pro)
│   │   ├── adapter.py            ImageProvider.generate(prompt, size, aspect, refs, style) -> ImageResult; edit()
│   │   ├── figure_prompts.py     scene prose → declutter → style directive → NO-TEXT closer (lifted templates)
│   │   ├── compliance.py         Claude-vision check (lift analyzer gemini_image.py:1604)
│   │   └── storage.py            local disk + Render persistent disk or R2 (env-gated); serves /v1/figures/{id}
│   ├── sources/                  NEW  input adapters
│   │   ├── schemas.py            SourceSpec = {kind: paste|upload|stacks_view|stacks_uids|referee_query|url, ...}
│   │   ├── stacks.py             POST {STACKS_URL}/api/export (uids | view) → split by per-paper header → documents
│   │   ├── referee.py            STUB: cross-entity query → paper list → stacks export / fetch
│   │   └── resolve.py            SourceSpec → list[Document] (uses executor/document_store)
│   ├── dossier/                  NEW  the meaning-making workflow ("document(s) → text + tables + figures")
│   │   ├── schemas.py            DossierJob, Brief, BriefOption, DossierPlan, Section, Table{caption, columns,
│   │   │                           rows[{cells[{value, anchor{doc, quote}}]}]}, Figure{caption, prompt, provider, url}
│   │   ├── reconnaissance.py     step 1: Sonnet → DocumentProfile (genre, claims, entities, candidate engines/angles)
│   │   ├── brief.py              step 2: Sonnet → 3 tellings/angles (cards) + audience + output shape defaults
│   │   ├── plan.py               step 3: orchestrator adaptive_planner over EXECUTABLE engines only, depth simple|medium|advanced
│   │   ├── analysis.py           step 4: executor job (workflow_runner) — passes, context_broker chaining
│   │   ├── tables.py             step 5: Haiku/Sonnet JSON tables with verbatim anchors; shape walls
│   │   ├── figures.py            step 6-7: figure plan (2-3) → images/adapter → compliance → storage
│   │   ├── compose.py            step 8: sections + tables + figures → HTML (Jinja) → PDF (weasyprint) → MD
│   │   ├── runner.py             DossierRunner: threads, op_events → events/store, resumable from stored params
│   │   └── receipts.py           lifted veo2/engine/receipts.py: payload/prompt/tool hash, cost, verbatim result
│   ├── api/routes/
│   │   ├── dossier.py            NEW  POST /v1/dossier/jobs {sources, brief_choice?, options}; GET /{id}; GET /{id}/brief;
│   │   │                              POST /{id}/brief {choice}; GET /{id}/events (SSE); GET /{id}/dossier.{html,pdf,md}
│   │   ├── figures.py            NEW  GET /v1/figures/{id}
│   │   └── (existing 27 route families untouched — mgmt console depends on them)
│   └── workflows/definitions/dossier_standard.json   NEW  8-phase workflow (functions + engine phases)
├── web/                          NEW  front end (veo2 shell)
│   ├── src/App.tsx, router.ts, tokens.css   copied from veo2/web/src, restyled dark editorial (Kering Backstage register)
│   ├── src/pages/Library.tsx     slate: dossiers Today/Week/Earlier + paste-and-go autopilot box
│   ├── src/steps/SourcesStep.tsx  1 · Your documents (paste / upload / stacks view picker / referee query stub)
│   ├── src/steps/BriefStep.tsx    2 · The brief (3 telling cards from LLM + audience + output shape + depth + spend cap; OutcomeButton)
│   ├── src/steps/DraftStep.tsx    3 · The draft (SSE narrated waiting → master-detail: sections, tables, figures; regenerate/sharpen per item)
│   ├── src/steps/DossierStep.tsx  4 · Your dossier (rendered HTML, downloads PDF/MD, receipts, "open console")
│   ├── src/pages/Console.tsx      /console/{job}: phase tree (lift the-critic PipelineVisualization), per-pass prompt|output,
│   │                              tokens/cost/duration, planner rationale + alternatives, narrator line per step, receipts ledger
│   └── src/lib/api.ts, sse.ts
├── communications/IMPLEMENTATION_TRACKER.md (this file), BUG_TRACKING.md
└── docs/FEATURES.md, CHANGELOG.md
```

analyzer-mgmt (CAII, separate repo):
- Set `NEXT_PUBLIC_ANALYZER_V2_URL=https://the-analyst-kcuc.onrender.com` on `analyzer-mgmt-frontend`; change default in `frontend/src/lib/api.ts:84` and the 5 page-level re-declarations; commit `render.yaml`.
- Cherry-pick `c365b2c` (Plans → Jobs tab, `annotated_prose`) with client-side `plan_id` filter (executor list ignores `plan_id`, `src/api/routes/executor.py:188`).
- Add `pages/jobs/index.tsx` (Runs) + sidebar entry; add `pages/jobs/[id]/console.tsx` = same Console component as `web/` (shared package or copied).

## 3. Phases

### P0 — demo-critical (today)
| # | Task | Files | Verify |
|---|---|---|---|
| P0.1 | Freeze gsi | analyzer-v2 branch `client-frozen-2026-09-03`; Render branch pin | `get_service srv-d9ph2gdbedkc73c3967g` shows branch; `curl analyzer-v2-3blo/v1/engines/argument_architecture/extraction-prompt` length unchanged (23,906 chars) |
| P0.2 | the-analyst repo + CAII deploy | fork; `render.yaml` (web + db); env: `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `ARK_API_KEY`, `DASHSCOPE_API_KEY`, `DATABASE_URL`, `STACKS_URL` | `GET /v1/engines` = 207; `GET /v1/workflows` = 10; a `concept_inferential_single_concept` job completes |
| P0.3 | Events ledger + SSE | `src/events/*`; hook `engine_runner.run_engine_call` and `chain_runner._run_engine_passes` to append before/after each call; `workflow_runner` phase start/end | `curl -N /v1/executor/jobs/{id}/events` streams during a run; replay works |
| P0.4 | Image adapter | `src/images/*` | `python -m src.images.adapter --provider gemini_pro "..."` writes PNG; cost recorded |
| P0.5 | Dossier workflow v0 | `src/dossier/*`, `dossier_standard.json`, `api/routes/dossier.py` | Kering study → brief (3 cards) → 2 engine passes → 2 tables → 2 figures → HTML+PDF in < 12 min at "medium" |
| P0.6 | mgmt repoint + Runs + Console | analyzer-mgmt frontend as above | Engines page loads; Runs lists v3 jobs; Console shows phase tree + pass prompt/output live |
| P0.7 | web/ front end | `web/*` | Playwright: paste → brief → draft (SSE narration) → dossier download; console link |
| P0.8 | Exemplars | 2-3 finished dossier jobs + 1 genealogy-style multi-phase job on v3 db | Library shows them; console replays |

### P1 — this week
- Stacks picker in SourcesStep (`GET /api/views`, `POST /api/export view=`), referee cross-entity query adapter, gs_revamp v2 fetch adapter, archivist.
- Wirecut handoff: "Make a video of this dossier" → `POST veo2/api/...` with composed narrative (video as one more output form).
- Depth modes on engines (simple/medium/advanced) with LLM routing; per-run spend cap + OutcomeButton pricing.
- Meta-analysis export back to stacks (MD with per-paper anchors).

### P2 — consolidation
- Engine hygiene: LLM-generate YAML capability definitions for the 9 missing concept-chain engines and the 17 client engines from their JSON definitions; consolidate clusters (concept micro-engines 39→~12, `*_advanced` ×10, metaphor ×5, genealogy_pass ×8).
- Prune v3 of v1 stage prompts, the-critic-specific composition stack, unmounted evaluations router; fix the 8 failing test imports.
- mgmt sidebar regroup (Story / Methodology / Presentation / Catalog / Admin) + executive mode; retire mgmt-api (move Paradigms/Rhetoric/Grids into v3).
- Blind-spot declarations + two-witness verification (lift `oaas/spine/{registry,verification,tray}.py`).

## 4. API contracts (new)

```
POST /v1/dossier/jobs
  {sources: [{kind:"paste", title, text} | {kind:"stacks_view", view_id} | {kind:"stacks_uids", uids:[...]}],
   intent?: string, audience?: "executive"|"researcher"|"analyst", depth?: "simple"|"medium"|"advanced",
   output?: {text:true, tables:true, figures: 0-4, video:false}, spend_cap_usd?: number, autopilot?: bool}
  → {job_id, status:"reconnaissance", console_url}
GET  /v1/dossier/jobs/{id}         → DossierJob (status, step, brief?, plan?, sections?, tables?, figures?, receipts_total)
GET  /v1/dossier/jobs/{id}/brief   → {options:[{key,title,angle,engines[],why,est_cost_usd,est_minutes}], defaults}
POST /v1/dossier/jobs/{id}/brief   {option_key, overrides?} → resumes at plan
GET  /v1/dossier/jobs/{id}/events  → SSE RunEvent stream (also /v1/executor/jobs/{id}/events for analysis sub-job)
GET  /v1/dossier/jobs/{id}/dossier.html|pdf|md
GET  /v1/figures/{figure_id}
```

## 5. Do-not-break checklist (re-verify before every deploy)
- Never push to analyzer-v2 `master`. gsi services untouched. New services carry their own DB, keys, `API_KEYS` consumer id.
- `curl https://analyzer-v2-3blo.onrender.com/v1/engines/inferential_commitment_mapper/extraction-prompt | wc -c` = 31,437 before/after.
- MCP tool names/params in `visualizer/mcp_server/mcp_server.py` unchanged (we do not touch visualizer).

---

## 6. SESSION HANDOFF — 2026-09-03 (written mid-build; next session starts here)

**Read also:** the memory files `render-workspaces-and-machines` and `the-analyst-project` (Claude memory), and `communications/changes/*.md` (per-agent change notes).

### Done (verified)
- gsi `analyzer-v2-3blo` pinned to branch `client-frozen-2026-09-03` (client production frozen). NEVER push to analyzer-v2 master.
- Repo `yauhenio2025/the-analyst` (public for now — Render GitHub app on CAII only sees selected repos; add it in GitHub → Settings → Applications → Render, then flip back to private).
- CAII services: web `the-analyst` https://the-analyst-kcuc.onrender.com (srv-dacfq315efls73e9hohg, auto-deploys master, env vars set incl. corrected ANTHROPIC_API_KEY, FIGURES_DIR, DOSSIER_DIR); Postgres `the-analyst-db` (dpg-dacfn3ijnfac73cddr2g-a) — **EXECUTOR_DATABASE_URL NOT YET SET** (need the Internal Database URL from the Render dashboard or a CAII workspace API key; until then SQLite on ephemeral disk → runs vanish on redeploy).
- analyzer-mgmt-frontend (CAII) env `NEXT_PUBLIC_ANALYZER_V2_URL=https://the-analyst-kcuc.onrender.com` set and rebuilt → Engines page loads 207 engines (verified with Playwright). Its master still has the dead default in code; branch `feat/the-analyst-console` (in `~/projects/_study/analyzer-mgmt-master`) fixes the default and adds Runs + Run Console.
- `feat/images` MERGED into master: `src/images/*`, `/v1/figures/*`, tests (31 pass), samples in `communications/changes/images-samples/`. Providers live-tested: gemini_pro ($0.13, 33 s), seedream_5_pro ($0.06, 66 s), gemini_flash, qwen_image_2_pro.
- Exemplars staged (NOT in git): five-paper fashion bundle + Kering study, see the-analyst-project memory; the dossier agent also keeps a copy under `data/exemplars/` in its worktree.

### MERGED into master since the handoff was first written
- `feat/events` (a75cf78) and `feat/dossier` (0aa3818) are merged; conflicts in src/llm/{backends,client}.py resolved toward `sdk_timeout()`; 57 tests pass (`tests/test_events_store.py test_images_storage.py test_figure_prompts.py test_sources_split.py test_dossier_tables_wall.py`). The dossier agent may push more commits to `feat/dossier` (timings) — `git merge origin/feat/dossier` again.

### In flight at handoff (branches, merge in this order)
1. `feat/events` — MERGED. (worktree `~/projects/the-analyst-wt/events`): run_events table + `src/events/{store,schemas,pricing,context,narrator}.py`, hooks in engine_runner/chain_runner/workflow_runner, `/v1/events/{job}`, `/summary`, `/stream` (SSE) + executor aliases. Sample run job-plan-d87b85c590db; transcript `communications/changes/events-sample.jsonl`.
2. `feat/dossier` — MERGED (re-merge for late commits). (worktree `.../dossier`): `src/dossier/*`, `src/sources/*`, `/v1/dossier/*`, workflow `dossier_standard`. First full run on the bundle: reconnaissance 158 s/$0.38 (29/35 claims verified), brief 43 s/$0.05 (autopilot chose "Where Your Sustainability Claims Will Be Challenged"), then plan → executor analysis → tables → figures → compose.
3. `feat/web` — MERGED (e3c891b). Static site **https://the-analyst-desk.onrender.com** (srv-dacg7u15efls73eb2b40, build `cd web && npm ci && npm run build`, publish `web/dist`, env VITE_API_BASE). Mock demo insurance: append `?mock=1` to any page. (worktree `.../web`): `web/` Vite+React front end (Library, 4 steps, /console/:id), mock mode `VITE_MOCK=1`, screenshots in `web/docs/screens/`.
4. analyzer-mgmt `feat/the-analyst-console` — FAST-FORWARDED TO MASTER (cbe4736) and auto-deploying to https://analyzer-mgmt-frontend.onrender.com: repoint default, Runs page (`/jobs`), Run Console (`/jobs/{id}/console`, `?fixture=1&replay=1` for a synthetic replay, executive toggle), Settings page with health probes, render.yaml, design tokens on Layout/Runs/Console. SSE/polling against the REAL ledger not yet exercised — first thing to verify next session with a live the-analyst job.

### Also done after handoff
- `src/executor/executor.db` UNTRACKED (c519dc2): schema is created on boot; the dossier agent had committed its local job rows, which showed up as a stuck job on the live service. Live SQLite resets on every deploy until EXECUTOR_DATABASE_URL is set.
- Live smoke (2026-09-03 05:20 UTC): `/v1/figures/providers` lists 4 providers; `/v1/dossier/*` and `/v1/events/*` routes served; `/v1/dossier/exemplars` is EMPTY on Render (exemplar texts are not in git — repo is public; next session: upload endpoint or private repo + commit `data/exemplars/`).

### LIVE VERIFICATION (2026-09-03 06:20-06:35 UTC, after re-login)
- Exemplars now live in the executor DB via `POST /v1/dossier/exemplars` (src/sources/exemplar_store.py). Uploaded `fashion_bundle.txt` (5 docs) and `kering_study.md`. **Wiped on every backend redeploy until EXECUTOR_DATABASE_URL is set** -> re-upload with the snippet in section 7.
- LIVE RUN on the deployed stack: `dossier-9b0dc7a31701` from exemplar `fashion_bundle.txt`, depth simple, autopilot -> **done in 13m31s, $2.38, 9 LLM + 1 image call, 578K in / 34K out; brief chose "Where Your Sustainability Story Will Be Attacked"; 2 tables (8-row Legitimacy Attack Matrix), 1 Gemini figure, 5 sections + summary + conclusion, 13-page A4 PDF.** Outputs saved at `data/dossiers/live-dossier-9b0dc7a31701/` (git-ignored) - the pre-baked demo artefact if the live DB is lost.
- Desk verified live with Playwright: Library shelf, draft waiting screen (rail 1-8, narration, live call, meter), dossier page (totals, downloads, inline HTML), console (phase tree, node detail, timeline). mgmt console Runs page lists dossier runs.
- Client fixes shipped for real-vs-mock contract drift: wrapped lists, null fields, exemplar naming, job title, composed `sections` object -> list, API-absolute figure URLs in inline HTML, filesystem `paths` dropped, SPA 404 fallback, duplicate narration.
- Known cosmetic: mgmt Runs page says "ledger not available" (probe logic); desk `?mock=1` still uses its own fixtures.

### FINAL STATE AT SESSION END (2026-09-03 ~05:50 UTC)
- Desk static site LIVE at https://the-analyst-desk.onrender.com after fixing the `lib/` gitignore trap (cec64e1; see BUG_TRACKING). Not yet smoke-tested against real backend jobs — `?mock=1` replay verified by the web agent only.
- ALL FOUR BRANCHES MERGED to the-analyst master (events, images, dossier, web) and pushed; 61 tests pass; analyzer-mgmt master = console branch, live.
- First complete dossier run (local, simple depth): `dossier-000b84458ab4` — $2.07, 8 LLM + 1 image call, 3 tables/16 rows, 1 figure, 5 sections, PDF. Outputs preserved at `~/projects/the-analyst/data/dossiers/dossier-000b84458ab4/` (git-ignored) and the worktree's SQLite copy at `data/dossier-worktree-executor.db`.
- Medium run `dossier-16f2f9a2d89f` left in `analysis` in the dossier worktree DB; resume: boot server in that worktree, `POST /v1/dossier/jobs/dossier-16f2f9a2d89f/resume`.
- NEXT SESSION, in order: (1) set EXECUTOR_DATABASE_URL on srv-dacfq315efls73e9hohg; (2) get exemplar texts onto the live service (upload endpoint or private repo + commit data/exemplars); (3) run the bundle at medium on the LIVE service (pre-baked demo) + Kering study at simple (live demo); (4) verify the desk (https://the-analyst-desk.onrender.com) and console (/jobs/{id}/console) against those live jobs incl. real SSE; (5) fix the compliance re-render loop and spend cap if time; (6) rehearse the demo checklist below.

### Merge recipe
```
cd ~/projects/the-analyst && git fetch origin
git merge --no-edit origin/feat/events && git merge --no-edit origin/feat/dossier && git merge --no-edit origin/feat/web
# conflicts expected only in requirements.txt / src/api/main.py include lines — keep both
source ~/projects/analyzer-v2/venv/bin/activate && pip install -r requirements.txt -q
python -c "from src.api.main import app" && python -m pytest tests/test_events_store.py tests/test_images_storage.py tests/test_figure_prompts.py tests/test_sources_split.py tests/test_dossier_tables_wall.py -q
git push origin master   # deploys the-analyst
```
Then: fold `communications/changes/*.md` into docs/CHANGELOG.md + docs/FEATURES.md; create the CAII static site for `web/` (mcp__render create_static_site: repo the-analyst, build `cd web && npm ci && npm run build`, publish `web/dist`, env VITE_API_BASE=https://the-analyst-kcuc.onrender.com); set EXECUTOR_DATABASE_URL; run the exemplar bundle at depth medium on the live service (pre-baked demo run) + the Kering study at depth simple (fast live run); merge the console branch and verify Runs/Console against a live job.

### Demo checklist (2026-09-04)
1. Library → exemplar bundle card → brief (3 angles) → draft waiting screen narrated live (fast run on the Kering study, depth simple) → dossier with tables + figures → PDF.
2. Console (`/console/{job}` in the web app, or analyzer-mgmt Runs → Run Console) on the pre-baked medium run: phase tree, prompt|output per pass, cost meter, planner rationale, executive view.
3. Wirecut first, then The Analyst: same four-step skeleton.

## 7. Snippets

Re-upload exemplars after a backend redeploy (until Postgres is wired). Texts: session scratchpad `exemplars/` or `~/projects/the-analyst-wt/dossier/data/exemplars/`.

    python3 reupload_exemplars.py   # see scripts/reupload_exemplars.py (reads EXEMPLARS_SRC dir, posts fashion_bundle.txt + kering_study.md)

Pre-baked demo run: POST /v1/dossier/jobs with sources [{"kind":"exemplar","name":"fashion_bundle.txt"}], depth medium, audience executive, output.figures 2, autopilot true (about 14 min, about $3).
Fast live run: same with kering_study.md at depth simple (about 6 min, about $1).

### Demo runs (started 2026-09-03 06:44 UTC, live SQLite — do not push before the demo)
- medium, fashion bundle, 2 figures: `dossier-3190021326bf`
- simple, Kering study, 1 figure: `dossier-e004a67a75fe`

### Upload files as a bundle (2026-09-03 07:25 UTC)
- `POST /v1/dossier/uploads` (multipart `files[]`, optional `title`): pdf/md/txt -> text (pypdf) -> Haiku reads the opening page for title/creators/year/venue (`src/sources/uploads.py`) -> one bundle in the stacks-export header shape, stored in the exemplar store under `upload-<date>-<hash>.txt` -> job source `{"kind":"exemplar","name":...}`. Desk: "Upload files" tab in Library (`web/src/pages/Library.tsx`, `api.uploadBundle`).
- Deps added: pypdf, python-multipart.
- DATA ISSUE (owner): stacks item em:WUPV36YG ("Fashionable altruism", Hewitt et al.) carries the wrong PDF — Highfield & Miltner 2023 "Platformed solidarity" (hashflags). The `fashion_bundle.txt` exemplar therefore has that paper as #5; the dossiers cite it. Fix the Zotero attachment and re-export.
- Deploy lesson: Render QUEUES backend deploys (start can lag a push by minutes) and each one wipes SQLite; before seeding/running, confirm `list_deploys` shows the intended commit `live` (a marker exemplar that disappears is a reliable signal).

### Infra wired (2026-09-03 08:55 UTC) — with the owner's CAII-workspace Render API key (in chat, not stored)
- `EXECUTOR_DATABASE_URL` = internal URL of `the-analyst-db` set on the backend; Postgres verified locally for run_events / dossier_exemplars / dossier_jobs (external access needed a temporary ipAllowList entry for geekom-mini — REMOVE it when done: `PATCH /v1/postgres/dpg-dacfn3ijnfac73cddr2g-a {"ipAllowList":[]}`).
- Build filters: backend `ignoredPaths: web/**, communications/**, docs/**, *.md`; desk `paths: web/**`. Front-end and docs pushes no longer redeploy (and no longer wipe) the backend. Jobs/exemplars now persist across backend deploys.
- Brief page fix (2c6bb49): brief options normalized (engine objects → names, string estimates → numbers, output_shape → summary).
- IN PROGRESS: `feat/diagrams` — figures rebuilt as labelled analytical diagrams (v1 process: primitive → visual format → FORMAT_ENFORCEMENT + GLOBAL_PROHIBITIONS + style school → Gemini Pro → Claude-vision compliance → one retry). Owner critique 2026-09-03: "not at all like what we used to generate in visualizer/analyzer v1 — DIAGRAMS, FLOWS, VENN DIAGRAMS".
- Owner's first real run: `dossier-dce25aeed631` (5 uploaded PDFs on state capitalism) → "When Governments Say 'Strategic,' Follow the Money", 17 pages, $2.58; backup under data/dossiers/live-dossier-dce25aeed631/.

### 2026-09-03 09:30 UTC — Postgres live; studies delivered; rebuilds in flight
- Backend now on Postgres (deploy dep-dacjpo0jo6nc738fg3eg, triggered via REST — note: PUT env-var via REST does NOT auto-deploy; POST /deploys does). Exemplars seeded into the DB: fashion_bundle.txt, kering_study.md, state_capitalism_bundle.txt (owner's 5 PDFs, salvaged from the executor document store), fashion_pdf_bundle_3.txt. Local copies: data/exemplars/ (git-ignored).
- Design memos (read before touching the pipeline): `communications/DESIGN_concretization_passes.md` (Wirecut pass ledger + the S/E/D/X/R/T loop), `communications/STUDY_de-llm_longform.md` (19-stage long-form program; what to lift), `communications/DESIGN_brief_deliverables.md` (BriefOption v2, three entry lanes, purpose-first catalog).
- Branches in flight: `feat/diagrams` (figures as labelled diagrams, v1 process), `feat/brief-v2` (deliverable-first brief). NEXT after diagrams merge: `feat/concretize` = Phase 0–1 of DESIGN_concretization_passes (spine → spine-driven exhibits → draft with exhibits → cross-check + findings ledger), with de-llm's composition read and frames-last folded in.
- Session-limit note: agents can be killed by the account's session limit (429); relaunch with the same brief after cleaning worktrees (`git worktree remove --force`, `git branch -D`).

### 2026-09-03 10:40 UTC — handoff point (owner switching accounts)
- Brief v2 MERGED and live (b1e0d7a); verified on `dossier-afede514d4cf` (parked, intent-led, 3 deliverable cards). Chip-overlap CSS fix 9a30c1e.
- `feat/diagrams` has a WIP push from the diagram agent (see `communications/changes/diagrams.md` on that branch for what works / what remains). NEXT SESSION: `git fetch origin && git checkout feat/diagrams` in a worktree, read diagrams.md, finish (real renders judged by eye + `check_diagram`, tests), merge to master, then launch `feat/concretize` (Phase 0–1 of DESIGN_concretization_passes.md + de-llm composition read / frames-last), then rerun the demo dossiers so figures are diagrams.
- Postgres is live; exemplars seeded (4); parked jobs: dossier-2df7253360b8 (Kering, v1 brief), dossier-afede514d4cf (state capitalism, v2 brief). Backend redeploys no longer wipe anything.

### 2026-09-03 10:55 UTC — diagrams MERGED (a4f0870)
- Figures are now labelled analytical diagrams: Sonnet planner → primitive → catalog format → labelled data → `src/display/enforcement.py` (v1 GLOBAL_PROHIBITIONS + FORMAT_ENFORCEMENT verbatim, 64 formats) → style school → Nano Banana Pro 2K → `check_diagram` (Claude vision, every label) → one revision. Samples in `communications/changes/diagram-samples/` (sankey, quadrant, grouped bars, parallel timeline, risk grid — 5/5 pass). CLI: `python -m src.dossier.figures --job job.json --n 3 --out DIR`.
- Known weak spots (from `communications/changes/diagrams.md`): bar formats need numeric cells; grounding is lexical (placements not verified — the spine pass should anchor each placed item); executive audience always gets `explanatory_narrative`; timelines invent stage labels when there is no chronology; ~1/3 first-pass specs rejected for label length ($0.08 repair).
- NEXT (launch first thing next session, one agent in a worktree `feat/concretize`): implement Phase 0–1 of `communications/DESIGN_concretization_passes.md` — S (spine: sections with ONE claim each + per-section table/figure specs), E (exhibits derived from the spine, figure specs → the new diagram pipeline), D (draft written with exhibits in hand, `[[table:key]]`/`[[figure:key]]` placement tokens), X (cross-check judge + findings ledger with code clamps) — and fold in de-llm's composition read (buried crux, strands, what should be table/figure/prose) before S and "frames last" (summary + conclusion after the body) in D; keep the one-call compose as the `simple` path; walls + skip law throughout; events/narration per pass; desk: run rail shows the new passes, draft page shows findings. Verify on `data/dossiers/live-dossier-dce25aeed631/job.json` and one live run. Then Phase 2–3 (revise work order, read-through) and the desk "Fix everything" loop.
- After the deploy of a4f0870 is live: rerun demo dossiers on Postgres so figures are diagrams (fashion medium, Kering simple, state-capitalism with the intent lane).

### 2026-09-03 11:40 UTC — diagram-era demo runs on Postgres (durable)
- `dossier-afede514d4cf` "Partnership Risk Register: Flagging Offers Before They Land" (state capitalism, v2 brief lane=use, 3 engines) — $3.58, 2 tables, spectrum + linear flowchart, both compliance-ok.
- `dossier-0520c472a9e6` "Where Our Sustainability Claims Will Be Attacked" (fashion, lane=material → authenticity_stress_test) — $3.49, 2 tables, 1 bubble chart (second figure skipped; reason not surfaced on the job — the cross-check findings ledger in feat/concretize should carry figure skips).
- Parked for the demo: `dossier-2df7253360b8` (Kering, v1 brief, awaiting_brief). Backups under data/dossiers/live-*/.
- THE REPORTER (separate product, owner dictation 2026-09-03): work lives in ~/projects/the-reporter — dictation verbatim, two study memos (websaver/archivist/oaas; reader/referee/gs_revamp), a Syllabus embed-corpus memo in .secrets/ (read-only prod creds; 446K articles, pgvector), and BOOTSTRAP_PROMPT.md for the next session.

### 2026-09-03 12:20 UTC — plates (report-as-diagram) commissioned; v1 evidence gathered
- Owner: v1/visualizer produced "diagrams of enormous complexity that work as the report itself"; The Analyst must offer BOTH the memo and the huge visualization. Branch `feat/plates` (agent V1): standalone `src/dossier/plates.py` (UnifiedStrategist-style perspective map → PlateSpec with canonical content → v1 prompt stack → Nano Banana Pro 4K → compliance → revision), `dossier_plates` table, `POST/GET /v1/dossier/jobs/{id}/plates`, desk gallery `/d/:id/plates`. Integration as a run step after cross-check comes after `feat/concretize` merges.
- Evidence (session scratchpad `v1-plates/`, copies worth keeping under `communications/changes/plate-samples/reference/` on the branch): desktop-proper `~/visualizer-results/` (152 folders, 6.4 GB; 5504×3072 plates: gains/losses scorecard; two-paradigm framework diagram; river map of evidential foundations) and the client's S3 bucket `em-visualizer-bucket` (eu-central-1; 15,375 objects, 8,454 images, newest 2026-08-24; portrait 3584×4800 "smart table" plates for `argument_architecture`). v1 bugs to avoid: leaked `[SIZE_GUIDE: 0.9]` and "truncass to 100 chars" instruction text in renders.
- Client usage last 60 days (gsi analyzer-db, 462 completed jobs, avg $1.96): `stakeholder_power_interest` 107 and `argument_architecture` 106 as `structured_text_report`; `resource_flow_asymmetry`, `unearned_certainty_detector`, `institutional_capture_detector`, `power_interest_subtext`, `event_timeline_causal`, `dialectical_structure`…; `smart_table` 15; `gemini_image` last used 2026-07-23. These are the engines whose YAML capability definitions The Analyst should have (17 production engines).

### 2026-09-03 13:10 UTC — concretization passes MERGED (e7e26da)
- Pipeline is now: reconnaissance → brief (v2) → plan → analysis → SPINE (composition read + one claim per section + commissioned exhibits) → TABLES/FIGURES from the spine → COMPOSE with exhibits in hand ([[table:key]]/[[figure:key]] at the pointer; frames last) → CROSS-CHECK (judge with rendered diagrams as vision input + code clamps → findings ledger, one round of safe realizations at medium+) → receipts. 10 phases in `dossier_standard.json`; desk rail shows 10 steps; SpineView/FindingsView on the draft page. 147 tests pass. Details + live evidence: `communications/changes/concretize.md` (run dossier-59263a6a2227: +$0.46 / +4.6 min over legacy for the new passes).
- Left: Phase 2 (revise work order, report card), Phase 3 (read-through), Phase 4 (desk "Fix everything" / redirect_spine routes); kind↔affordance clamp for judge findings; fold `communications/changes/{concretize,diagrams,brief-v2,plates}.md` into docs/CHANGELOG.md + FEATURES.md.
- NEXT: merge `feat/plates` (report-as-diagram, standalone endpoints) → wire a `plates` step after crosscheck when `output.plates > 0` (runner `_run_step` dispatch; brief output shape) → rerun one dossier on the live stack with a plate for the shelf.

### 2026-09-03 15:40 UTC — plates MERGED and WIRED (e55259e)
- `feat/plates` merged (13 commits): PlateSpec families scorecard | framework_map | flow_map | power_map | timeline_of_shifts | register | layer_stack | argument_tree; v1 assembly order; tiled vision check; leak scan. Samples: `communications/changes/plate-samples/` (register 3584×4800, scorecard + framework map 5504×3072; 2/3 executive-grade). ≈$0.45–0.65 per plate.
- Wired: STEPS = … figures → **plates** → compose → crosscheck → receipts; `OutputOptions.plates` (0–2, default 0); Library dial; rail step 8 "Draw the plates"; `plates_appendix_html` included in the dossier template; workflow JSON 11 phases. 224 tests pass.
- Live ten-phase verification run on the deployed stack: `dossier-0d3a0a532864` (state capitalism, use lane, chose "Which Partnership Offers to Treat as Risks") — in flight during the e55259e deploy; if it stalls, `POST /v1/dossier/jobs/dossier-0d3a0a532864/resume`.
- NEXT: run one dossier with `output.plates=1` on the live stack for the demo shelf; Phase 2–3 of concretization; cross-check should also judge plates; the `?mock=1` fixtures for plates/spine exist.

### 2026-09-03 15:50 UTC — incident: dossier_standard unloaded (fixed 2af91b3)
- Cause: the plates-wiring commit's scripted JSON edit produced a phase with `depends_on_phases: [null]` → the registry skipped `dossier_standard` (health `workflows_loaded` 11→10) → every live run failed at analysis with "Workflow not found: dossier_standard". Jobs `dossier-0d3a0a532864` (verification) and `dossier-bdb59693892e` (Kering + plate) FAILED for this reason; ignore/delete them.
- Fix: proper Plates phase 7.5 (`dossier_plates`, depends on 7.0), `tests/test_workflow_definitions_load.py` (all definitions must validate + load; 11 phases in order), BUG_TRACKING entry. Also: `POST /resume` ignores `from_step` (always resumes from the recorded step) — Phase 2 item.
- After 2af91b3 is live: rerun Kering (material lane, medium, figures 1, plates 1) and state capitalism (use lane, medium, figures 2, plates 1) one at a time.

### 2026-09-03 16:18 UTC — first full eleven-phase run with a plate, on the live stack
- `dossier-4c95b7a70a57` (Kering study, material lane → pitch_stress_test): "Six Angles, Four Verdicts: What Survives de Meo on Wednesday" — spine 5 sections, 2 tables, 1 quadrant figure, 1 register PLATE (4K, 2 attempts, compliance ok), cross-check 0 findings; 18 LLM + 3 image calls, $2.60, 27 min. Backup: data/dossiers/live-dossier-4c95b7a70a57/ (plate-1.jpg 3584×4800). Desk: /d/dossier-4c95b7a70a57/{draft,dossier,plates}, /console/dossier-4c95b7a70a57.
- Started `dossier-43f34a0abe5c` (state capitalism, use lane, figures 2, plates 1) — parks at the brief; choose the recommendation via POST /brief.

### 2026-09-03 16:55 UTC — demo shelf final (both runs done on the eleven-phase pipeline, Postgres)
- `dossier-4c95b7a70a57` Kering: "Six Angles, Four Verdicts: What Survives de Meo on Wednesday" — 2 tables, 1 quadrant, 1 register plate, 0 findings, $2.60, 27 min.
- `dossier-43f34a0abe5c` state capitalism (use lane → partnership_risk_decision_memo): "Every 'Strategic' Government Offer Hides an Obligations Ledger You Cannot Renegotiate" — 3 tables, 1 register plate (first attempt ok), 0 figures kept, 3 findings (2× exhibit_missing_where_claim_needs_one → rerender_figure, 1× caption_carries_number), $4.54, 34 min.
- Figure issue to fix (Phase 2): spec `offer_type_lock_in_map` PASSED the wall but no figure was kept → the render/check path dropped it silently (look at figures.py keep-better-attempt); second spec rejected only for "format already used by another figure" — the spine should not commission two positioning maps, or the wall should offer the primitive's next format instead of rejecting. Cross-check correctly minted the findings but its one realization round did not restore a figure.
- Shelf for the demo: the two above + `dossier-afede514d4cf` (risk register, spectrum + flowchart) + `dossier-0520c472a9e6` (fashion, bubble quadrant) + parked briefs `dossier-2df7253360b8` / `dossier-895f95ce879f`-era items (v1) — all durable on Postgres. Backups under data/dossiers/live-*/.

### 2026-09-03 17:50 UTC — plates: OOM incident, planner bias fix
- Owner: the live plates were both `register` (table-plates); the wild v1-style diagrams were missing. Fixes pushed (1b3b641): planner prefers diagrammatic families and REFUSES a register plate when the dossier already has ≥2 anchored tables (unless the requester names one); `POST /plates {"perspectives":[...]}` honours named perspectives (used to commission framework/flow/power maps).
- INCIDENT: two concurrent plate runs (2× 4K render + vision tiling) OOM-killed the 512 MB starter instance (Render event `server_failed` exit 137 at 17:43); in-memory plate plans were lost. Fix: process-wide render gate (one 4K render at a time). Render REST `PATCH /services/{id}` plan change returned 500 twice — UPGRADE THE BACKEND TO `standard` (2 GB) IN THE DASHBOARD before running plates for several jobs at once.
- Pending: re-commission plates on `dossier-4c95b7a70a57` (framework_map + flow_map) and `dossier-43f34a0abe5c` (flow_map + power_map), one job at a time, after 1b3b641 is live.

### 2026-09-03 17:55 UTC — the wild plates exist (demo-ready)
- Kering `dossier-4c95b7a70a57` now has 3 plates: register (table-plate), **framework_map** "Kering's Meaning-System Lattice…" (3 levels, labelled relations, empty-node gap, verdict panels), **flow_map** "Six Pitch Angles, Four Verdicts: The Claim-to-Collapse Current" (river with 6 tributaries → 3 stations → 4 verdict channels). Both first attempt, compliance ok, ≈$0.55 each. 4K files: `/v1/dossier/jobs/dossier-4c95b7a70a57/plates/{kering_meaning_lattice,pitch_claim_current}.jpg`. Local copies under data/dossiers/live-dossier-4c95b7a70a57/.
- Recipe for more: `POST /v1/dossier/jobs/{id}/plates {"perspectives":["FRAMEWORK MAP (family framework_map): …", …]}` — naming the family in the perspective steers the planner. State-capitalism flow_map + power_map commissioned 17:53.
- State capitalism `dossier-43f34a0abe5c` now has 3 plates: register, **flow_map** "Private Deal to Strategic Liability: Five Cases, One Current" (first attempt), **power_map** "Leverage Architecture: Who Controls What in Each Government Offer" (2 attempts, ok). 4K: `/v1/dossier/jobs/dossier-43f34a0abe5c/plates/{deal_to_liability_flow,power_leverage_map}.jpg`. Local copies under data/dossiers/live-dossier-43f34a0abe5c/.
- DEMO SHELF COMPLETE (2026-09-04): two eleven-phase dossiers each with a register + two diagrammatic plates, plus the earlier risk-register and fashion dossiers with inline diagrams, plus parked briefs. Reminder: upgrade `the-analyst` to Standard in the Render dashboard before the demo (4K renders near the 512 MB ceiling).

## 8. The Master (2026-09-04, morning of the meeting)

Owner: centralize every engine and process of the estate (analysis AND storytelling, editing, restructuring, search, rendering) in one editable brain, show clients the multi-step method, keep The Analyst's workflows intact, evolve rather than scratch the console. Decision and design: `communications/DESIGN_the_master.md`.

- Registry (this repo, additive): `EngineFamily` + `family/home_organ/runs_at/lineage_refs/status/sync` on engines; 11 estate categories; organs entity (`src/organs`, `/v1/organs`, 15 organs by layer); 65 mirrored/native process engines via `scripts/register_estate_engines.py` (Wirecut 18, de-llm 21, Referee 13, Reporter 1, Analyst process engines 10, imagination/governance 5); 7 cross-organ processes as workflows (`category: process|rendering`, `source_project`); `?family=&organ=` filters; composed-prompt routes 404 for mirrored engines. Dossier catalogue and orchestrator capability catalogue verified unaffected (executable YAML set only).
- Console (`analyzer-mgmt`): rebranded The Master; ESTATE section (Map landing, Organs, Processes); family strip and mirrored badges on engines; lineage banner on mirrored engine pages. Built by agent; Playwright-verified; pushed to master → Render.
- Phase B step 1 DONE: `GET /v1/engines/{key}/doctrine` serves hash-pinned doctrine files imported from the organ repos (37 files / 28 engines; `scripts/import_doctrines.py`).
- Next (memo §4): organs read their prompts from the doctrine endpoint (Phase B step 2); Postgres overlay for durable console edits (Phase C); activity-driven activation (Phase D); capability YAML for the imagination engines (Phase E).

- INCIDENT 2026-09-04 ~08:00 local: the three registry deploys wiped every figure, plate and PDF (disk-only). Fixed durably in 264cb46: `src/dossier/blob_store.py` (Postgres blobs, disk as cache, write-through + restore-on-read), admin re-hydration endpoints (ADMIN_TOKEN set on Render), `scripts/rehydrate_blobs.py` run from the local backups (`data/dossiers/live-*/`). See BUG_TRACKING.md. Live dossiers for the demo: Kering `dossier-4c95b7a70a57` (3 plates + 1 figure), state capitalism `dossier-43f34a0abe5c` (3 plates), the owner's five-PDF run `dossier-dce25aeed631` (re-imported from job.json; 3 figures).
- Console live as The Master (analyzer-mgmt e78be33): Map, Organs, Processes, family strip, mirrored banners, Doctrine section. Playwright-verified live: map, /engines/wirecut_spine, /processes/dossier_standard.
- Multi-source storytelling designed at the owner's request (not urgent): `communications/DESIGN_multisource_storytelling.md`; registered as engines `story_reconnaissance`, `story_map`, `story_brief` (designed) and process `wirecut_multisource_story` (planned). Principle: the reading pass extracts against the declared demands of the downstream passes; anchors everywhere; harvest-on-demand ledger. First build path: run steps 1–5 as a dossier-shaped job in The Analyst and hand the chosen spine to Wirecut.

## 9. The story desk (2026-09-04, after the Master)

Owner: "go ahead on all fronts" for multi-source storytelling (memo `communications/DESIGN_multisource_storytelling.md`). Split at the seam: The Analyst reads, maps, briefs and writes the spine; Wirecut consumes a `StoryHandoff`.

- Contract: `communications/STORY_HANDOFF_SCHEMA.json` (from `src/story/schemas.py:StoryHandoff`), `communications/STORY_HANDOFF_EXAMPLE.json`; live `GET /v1/story/handoff-schema`.
- Wirecut session brief (paste-ready): `communications/BRIEF_WIRECUT_multisource_intake.md`.
- Analyst half: `src/story/` (schemas, store `story_jobs`, demands, doctrine loader, prompts, steps, runner) + `src/api/routes/story.py` (`/v1/story/*`). Steps: reconnaissance (one call per source, elements typed by the downstream passes' demands, anchor wall) → map (through-lines with tributaries, coverage matrix computed) → approaches (Wirecut's twelve, doctrine served by the registry) → brief (three deliverable-first options, gate) → spine (sources as tributaries, spine + telling-desk doctrine) → handoff. Receipts route to `story_jobs` (`src/dossier/receipts.py` dispatch). Registry: `EngineDefinition.source_demands` set on eight Wirecut engines from `src/story/demands.py`; `GET /v1/story/demands`.
- Desk: story pages under `/s/{id}` (agent build, Playwright-verified) + "Make a film" lane in the Library.
- First real run: state_capitalism_bundle.txt (5 papers), local API; job id recorded below when it finishes.
- First real run (local API, SQLite): `story-3813ecd195ee` over the five state-capitalism papers, $1.13, 8 calls. 124 anchored elements (11 dropped by the wall), 4 through-lines, 3 options (verdict / case / numbers), chosen option_a → 4 movements with sources as tributaries, motif "the word 'strategic'" planted 1 paid off 4, hook an intensity-5 quotable. Real handoff saved: `communications/STORY_HANDOFF_REAL_story-3813ecd195ee.json` (4 sources, 99-element ledger, doctrine hashes).
- LIVE run on the Analyst API: `story-d3444a230015` (from_job dossier-43f34a0abe5c, the same five papers), $1.24, done. Handoff: https://the-analyst-kcuc.onrender.com/v1/story/jobs/story-d3444a230015/handoff (4 movements, 97-element ledger, 4 sources, approach the_case). Desk: https://the-analyst-desk.onrender.com/s/story-d3444a230015 (stations: /sources /reading /map /brief /spine /handoff). Desk pages by agent (commits 09d8c66, 72081de), Playwright-verified on the local run.
- Wirecut took the handoff in (veo2 c1fa35f): 19 clips, all anchored, from story-d3444a230015. Its note (`veo2/communications/NOTE_TO_ANALYST_multisource_2026-09-04.md`) answered in `communications/NOTE_TO_WIRECUT_from_analyst_2026-09-04.md`: byte-verbatim anchors (`raw_verbatim`, rebuild-handoff route), approach windows in the registry and obeyed by brief/spine, all sources listed with `used`, spine doctrine re-pinned (bb8246e7).
- Live handoff `story-d3444a230015` rebuilt after the fixes: 97/97 ledger quotes byte-verbatim in the served texts, 5 sources listed (`up4E97C254` used=false), coverage keys match, spine doctrine bb8246e7. Regression caught and fixed on the way (8777fc6: the STEP table lost in the verbatim rewrite; smoke tests added).
- Owner (afternoon): cleanse the app of documents referencing Kering or de Meo. Admin scan/purge routes added (4834f02); scan → purge → rescan recorded below.
- CLEANSE DONE (2026-09-04 ~14:00): scan for "Kering" / "de Meo" found 6 dossier jobs (all built on kering_study.md: e004a67a75fe, 5cdf8f1a470f, 10656694ada2, 4c95b7a70a57 with its 3 plates, bdb59693892e, 2df7253360b8), the exemplar kering_study.md and 5 stored documents; nothing in the fashion or state-capitalism runs, nothing in story jobs. All purged (plates, blobs, events, executor sub-runs, documents); rescan clean; 13 dossiers remain. Local backups under data/dossiers/live-* and data/exemplars/ are outside the app and untouched.
- RENAME: The Master → **The Mastermind**, own service https://the-mastermind.onrender.com (srv-dad5rblg1s2s73f62rmg, analyzer-mgmt master, same env). Organ key `the-mastermind`; desk and docs point at the new URL; analyzer-mgmt-frontend.onrender.com still serves the same app until suspended.
- Mastermind live at https://the-mastermind.onrender.com (066923d rename, eab3fd9 wordmark stacked, b112f94 Plans pages null-safe: dossier-made plans carry no cost estimate and crashed `/plans` with "reading 'toFixed'"). Scrub of named third parties from fixtures/tests/doctrine copies: d27fc8a, 072bd2e (importer strips names on every import).
- Mastermind sweep (31 pages, Playwright): no client crashes after b112f94. mgmt-api CORS allowlist lacked the new origin (six mgmt-backed pages loaded empty) → analyzer-mgmt 9a3e51b adds https://the-mastermind.onrender.com to `api/main.py` allow_origins.
- END-TO-END FILM (2026-09-04 15:13 local): five papers → story job `story-3f5149582332` (90 s asked, the_verdict, 4 movements, 106 elements, $1.19) → Wirecut corpus intake → board `sb_a879453ed293` (15 clips, coherence off, style documentary_calm) → produce on Seedance 2.5 → assembly `asm_fa188e2554f5` "What Was Promised / What Was Built", 121 s adopted, 1280×720, 27.6 MB (+ WhatsApp export 15.7 MB), Wirecut estimate $13.11. Local copy: `data/films/story-3f5149582332_what-was-promised.mp4`. Driver: session scratchpad `wirecut_drive.py` (preview → write → produce → download → export; Wirecut basic-auth password from the veo2 service env).
- Plates re-commissioned on `dossier-43f34a0abe5c` (15:29 local): `cost_transfer_mechanisms` (framework_map, "How a 'Strategic' Label Transfers Cost: Four Mechanisms, Four Cases", 5504×3072, first attempt) and `lock_in_layer_stack` (layer_stack, "The Lock-In Stack: What Each Layer Removes from the Partner's Exit Options", 4800×3584, first attempt), $0.88; five plates on the dossier. Known cosmetic on the framework map: a stray opening quote before two column headers, one misspelt connector label, title says four mechanisms but three columns are drawn (the fourth folded into the reversibility box).
- Owner feedback on the film (photoreal by default; wants the look chosen, animated preferred; a "run until the judge approves" condition): brief for the veo2 session `communications/BRIEF_WIRECUT_look_and_approval_2026-09-04.md` (also copied to veo2/communications). Analyst half on branch `look-recommendation` (d746464): Wirecut's 16 presets mirrored into the registry as `wirecut_storyboard/style_presets.json`, `Look` on brief options, spine and handoff (`handoff.look`), the owner's preference in the brief/spine prompts, engines `wirecut_look_desk` and `wirecut_approval_loop` registered as designed. Merge + push after the meeting (the API restarts for a minute on deploy). Driver now sends `style_preset` from the handoff and `length_pinned: true`.

## 10. Engine harness study (2026-09-04 evening)

Owner: does the multi-level engine harness beat a one-shot with a strong model? What in the well-developed engines can be improved (process, definitions, workflows)? Decide afterwards: more work on the engines, or something else.
- Brief for both readers: `communications/study/STUDY_BRIEF_engine_harness_2026-09-04.md`. Runner: `scripts/study_engine_harness.py` (production-faithful harness at deep depth vs one-shot vs one-shot-with-questions; sonnet-4-6 and fable-5-1; blind rubric + pairwise judging by fable). Material: the AUKUS paper (`data/study/source_aukus.txt`). Outputs under `data/study/` (untracked), memos under `communications/study/`.
- Readers: a Fable 5.1 agent here and Codex gpt-5.6 (xhigh) via `codex exec`; then the session's synthesis.
- STUDY DONE (20:15 local): `communications/study/STUDY_engine_harness_SYNTHESIS_2026-09-04.md` (+ Fable and Codex memos). Headline: the four-pass concatenation loses 12/12 blind pairings to a one-shot, but production hands the spine only the last pass, and on that artifact the result splits: Conditions of Possibility's integration pass wins 4/4, Argument Architecture's loses 4/4; a one-shot carrying the probing questions matches or beats the plain one-shot. Both readers converge: anchored findings as the contract; one call by default, passes by kind; fix the composer/chain-runner plumbing (blank pass description, final pass written "for the next pass", composability tail on the last pass, untruncated prior context, no anchoring line, refusals logged as "empty"); judge what the dossier consumes; a dozen method families rather than 275 labels. Owner decision pending: plumbing fixes → anchored findings → rerun on two more engines.
- PLUMBING FIXES (owner: "fix all that plumbing and keep fixing until we are ready to retest"): `capability_composer.py` — the final pass is told it is the engine's product for the desks and a reader (no "next pass" line, no composability tail), every pass carries the anchoring law and the findings-ledger law, the operationalization's pass description is rendered; `PassPrompt` gains `description` and `is_final`; `chain_runner.py` passes both through (the description used to be blanked); `context_broker.py` hands later passes each prior pass's ledger in full and its prose capped (20K latest, 6.6K earlier); `llm/backends.py` raises `ModelRefusal` on `stop_reason=refusal` and reports the stop reason on empties; `engine_runner.py` never retries a refusal and falls back once to Sonnet; `dossier/llm.py` emits `call_refused`, falls back to the house model, and answers JSON as text for models that reject forced tools (Fable); `events/schemas.py` adds `call_refused`. Tests: `tests/test_plumbing_2026_09_04.py`. Retest runner: `scripts/study_engine_harness_v2.py` (judges the final pass, records cost).
- RETEST (20:45 local, `scripts/study_engine_harness_v2.py`, judged on the final pass): Sonnet outputs split 1-1 both engines (position effect); Fable outputs: one-shot wins both orders on both engines, one-shot-with-questions wins both orders on both engines. Every pass now produces an anchored ledger; refusal fallback fired twice. Revised recommendation in the synthesis §7: one-shot-with-questions as the default execution mode, a second critic/integration pass as the depth dial, rewrite the two definitions to ask about the text not the authors' biography, rerun on two documents with two judges.
- Fixed-vs-pre-fix final pass (8 pairings): Argument Architecture fixed wins 3/4 (the plumbing was its defect); Conditions of Possibility pre-fix wins 3/4 (its defect is the definition). Study closed for tonight; next step is the owner's call on the revised recommendation (one-shot-with-questions default, one critic/integration pass as the depth dial, rewrite the two definitions, rerun on two documents with two judges).

## 11. Engine redesign from the ideal output, and the frontier study (2026-09-04 night)

Owner's instruction: assume the current engine design is faulty (built for a weaker model, and for an author's corpus); design from the ideal output backwards; build the shape; run the cost-quality frontier.
- DESIGN DONE (no API spend): `communications/study/REDESIGN_conditions_of_possibility_2026-09-04.md`, `REDESIGN_argument_architecture_2026-09-04.md`, `REDESIGN_method_shape_2026-09-04.md`. Conditions of Possibility: 8 dimensions → 5 text-facing (givens, inheritance, apparatus, visibility, rivals) + 1 corpus (path dependence) + synthesis; every question about what the text presupposes, cites, borrows, dismisses, brackets, renames; provenance tagged hypothesis, no motives; method cards (Foucault archaeology/genealogy, Skinner, Lovejoy) as imperatives. Argument Architecture: 6 → 5 (claims; grounds/warrants/suppressed premises; schemes with the critical questions listed and run; dialectic and burden; omissions and strongest form) + corpus exchange + synthesis; stable ids C/G/S/I; legal standards dropped for the text's own verbs. One shape: extract (cheap, parallel per dimension) → verify (mid, rule every row, hunt misses) → synthesize (strong, cite by id); ledger as hand-off; walls check anchors and ids only. 28 capability engines sorted into five families that are parameters of the shape.
- BUILT (no API spend): schema (`ProcessSpec` on the operationalization, `DepthSequence.process`), both engines' `process:` blocks at depth key `dvs` (the four-stance `deep` untouched as the control), composer, ledger walls, routed runner with receipts, chain-runner dispatch, API `GET /v1/operationalizations/{key}/process` + `process-preview`, pricing rows for Fable ($10/$50) and the OpenRouter frontier models, `scripts/study_engine_harness_v3.py` with `--dry-run`, tests (7, all green). Paper two on disk: `data/study/source_subsea.txt` (Abels 2026, Global Policy, 77K chars).
- FRONTIER STUDY — AWAITING THE OWNER'S GO (spend). Dry run, lean preset: 92 generation runs ≈ $46 (a $3.4, b $16 on fable/sonnet/sol/luna only, c $21, d $6), judging with Sonnet and Sol, split orders ≈ $26; total ≈ $72. Full preset (b on all seven, both judges both orders) ≈ $110. Command: `python scripts/study_engine_harness_v3.py --preset lean` (resumable; `--judge-only --report` afterwards; `--dry-run` to re-estimate). Output: `data/study/v3/FRONTIER.md`, `manifest.json`, `judgments.json`, `receipts/`. Expect 2-3 hours wall-clock at 4 workers (Fable four-stance runs are ~10 min each).
- Open risks to watch in the run: OpenRouter streaming heartbeat is 120s (long silent reasoning on Sol could trip it; the runner retries); Fable refusals on pass 1 of (b) fall back to Sonnet (recorded in `models_used`); cheap extractors may return ledgers with few verbatim anchors (the anchor rate per run is in the manifest, by code).
- FRONTIER STUDY RUN (owner's go 22:16 on 2026-09-04; done 02:25 on 2026-09-05): 91 runs, $87.41 ($58.56 generation, $28.85 judging). Synthesis `communications/study/STUDY_frontier_SYNTHESIS_2026-09-05.md`; per-run table `STUDY_frontier_runs_2026-09-05.md`; aggregates `scripts/study_frontier_analysis.py`. Headline: the four-stance harness loses on every measure and Fable refuses all its passes on both papers; the one call with the redesigned questions is best or tied-best (chains −0.1 to −0.3 rubric at 3–16× the cost); the chain's value is the contract (97–99% verified rows, critic rejects 4–8 and adds 5–10 rows a run, 2.5–5.7 reach the reading); cheap read + strong write matches the same-model chain at 40–45% of its cost; GPT-5.6 Sol at $0.10 is the value pick on both engines, Kimi K3 second, Sonnet level with them, Luna for previews, Fable the ceiling on argument mapping. Sol as a pairwise judge is a position effect (80/87 first-seen) — Sonnet's judgments carry the result.
- DECISIONS (pending the owner's confirmation): default execution mode = one call (`compose_oneshot_prompt`); default model for a read reading = Sol (Kimi K3 second; Sonnet acceptable); desks-facing runs = depth `dvs` routed Luna / DeepSeek Pro / Sol; retire the four-stance default; judging = both orders on Sonnet. Changes during the run: Kimi K2.6 → K3 (owner); five ledger-wall shape fixes (bolded ids, page refs after quotes, bare rows, quote-in-finding, spaced hyphens) with tests; `--skip`, `--rescan`, "ran on" column; `LLM_SYNC_HARD_TIMEOUT_SECONDS=1500` for Fable's critic.
- NEXT: wire the defaults (one-call mode as the engines' default depth; routing block; `execution_mode` on the plan), make the desks read ledger rows by id, and bring the next two engines under the shape (`REDESIGN_method_shape` §3). Prompt: `communications/study/NEXT_SESSION_PROMPT_after_frontier_2026-09-05.md`.
