# The Analyst — web

The front end for The Analyst: documents in → a dossier (text, tables, figures) out, with every model call on the record. Four numbered steps (Your documents · The brief · The draft · Your dossier), a library, and an "under the hood" console per job.

Vite + React 18 + TypeScript. No UI framework, no router library — `src/router.ts` treats the URL as truth. Styling is plain CSS on tokens (`src/tokens.css`), in the dark editorial register of the Kering "Backstage" prototype.

## Run

```bash
cd web
npm install
npm run dev            # http://127.0.0.1:5174 against VITE_API_BASE
npm run dev:mock       # same, replaying the fixture job — no server needed
```

Environment (`.env.local` or the shell):

| var | default | meaning |
|---|---|---|
| `VITE_API_BASE` | `https://the-analyst-kcuc.onrender.com` | the API (local: `http://127.0.0.1:8013`) |
| `VITE_MOCK` | unset | `1` builds a mock-only bundle |
| `VITE_MOCK_SPEED` | `1` | replay speed multiplier for the mock |

Mock mode can also be switched on at run time on any build: open `/?mock=1` (it sticks in `localStorage.analyst.mock`; `/?mock=0` clears it). This is the demo insurance if the backend lags.

## Build

```bash
npm run build          # → web/dist  (Render static site; public/_redirects sends every path to index.html)
npm run preview
```

## Layout

```
src/
  App.tsx           shell: masthead, step tabs, page switch
  router.ts         URL-as-truth pushState router
  tokens.css        the only file with literal values
  styles.css        every rule, on tokens
  types.ts          API types (contract in communications/IMPLEMENTATION_TRACKER.md §4)
  lib/api.ts        fetch client + SSE watcher with poll fallback; mock seam
  lib/mock.ts       fixture replay (timed, persisted per session)
  lib/run.ts        rail model + console tree, derived from events
  lib/hooks.ts      useJob (polled) / useEvents (replay + live)
  components/       RunRail, OutcomeButton, StatusChip, Record, TableView, FigureView, Md, Chips
  pages/            Library, Console
  steps/            SourcesStep, BriefStep, DraftStep, DossierStep
mock/               fixtures: one full job (events replay, profiles, brief, tables, figures, sections, receipts, plan, executor, dossier.html)
docs/screens/       Playwright screenshots
```

## Routes

- `/` library
- `/d/:id/sources` · `/d/:id/brief` · `/d/:id/draft?item=` · `/d/:id/dossier`
- `/console/:id?node=&view=executive`
