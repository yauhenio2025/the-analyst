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
