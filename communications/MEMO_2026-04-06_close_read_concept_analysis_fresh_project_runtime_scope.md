# Memo: Close Read Concept-Analysis Fresh-Project Runtime Scope

Subtitle: Enable freshly uploaded non-Benanav projects to produce persisted core concept-analysis results for the existing `Close Read` concept family

Date: 2026-04-06
Program: Dynamic Bespoke Apps Platformization
Strategic Roadmap:
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
Canonical Roadmap:
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
State Of Play:
- `communications/MEMO_2026-03-30_state_of_play_roadmap_where_we_are.md`
Vision Context:
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
Close Read Direction Context:
- `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
Current Close Read Product Boundary:
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
Current Concept Family Scope:
- `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`
Primary Runtime Evidence:
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/pages/closeReadConceptRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx`
- `/home/evgeny/projects/the-critic/webapp/src/components/CloseReadFamilySwitcher.tsx`
- `/home/evgeny/projects/the-critic/api/server.py`
- `/home/evgeny/projects/the-critic/api/database.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py`
- `/home/evgeny/projects/the-critic/analyzer/extract.py`

## Purpose

Write the next concrete implementation scope for the blocker exposed immediately after the first `Close Read` concept family tranche shipped:

- the host routes and family shell now exist
- but freshly uploaded non-Benanav projects still cannot reliably produce persisted admitted-core concept-analysis results

This memo should freeze the next runtime-enablement tranche, not reopen the concept-family product boundary.

Its job is to make the existing `Close Read` concept family work on new uploaded projects such as:

- `walter-rhetm-18422-20260406`

without pretending that the broader analyzer-v2-native concept migration is already done.

## Bottom Line

The immediate blocker is not the `Close Read` concept UI.

The blocker is runtime truth:

1. the concept family host surfaces are live
2. the generic concept-analysis path is only partially project-aware
3. the admitted core submodes that `Close Read` depends on, `inferential` and `logical`, are still tied to the old fixed Benanav/Morozov corpus loaders
4. the current concept detection and concept-analysis persistence paths still assume a PostgreSQL-style `DATABASE_URL` / `psycopg2` path rather than the API's actual active database abstraction
5. the admitted logical-only scrutiny feature still persists and reads through the same raw PostgreSQL-style path, so fresh-project logical `Close Read` is not fully truthful on the active local SQLite-backed stack until scrutiny persistence is normalized too

So the next honest implementation tranche is:

- make core concept analysis project-aware for fresh uploaded projects
- make concept detection, concept-analysis persistence, and scrutiny persistence/readback follow the API's active database backend
- do this without reopening routes, family boundaries, or standalone-host questions

## What The Walter Test Actually Revealed

The fresh-project test was useful because it separated host readiness from runtime readiness.

Observed local behavior:

- project creation worked
- PDF upload worked
- the new `Close Read -> Concept Analysis` family rendered correctly
- but the family stayed empty because no admitted-core concept analyses existed

The attempted fresh-project flow then exposed three concrete seams:

### 1. Concept detection persistence is not backend-neutral

`/home/evgeny/projects/the-critic/api/server.py`

The concept detection thread uses raw `psycopg2` / `DATABASE_URL` assumptions when persisting detected concepts.

That means:

- local create/upload can work on SQLite fallback
- but background concept detection can still fail or fail to persist because it bypasses the current database abstraction

### 2. Core concept analyzers are not yet project-aware

`/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`

`/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`

`/home/evgeny/projects/the-critic/analyzer/extract.py`

The admitted `Close Read` core submodes still call the old fixed-corpus extraction logic:

- `beyond_capitalism_1`
- `beyond_capitalism_2`
- `benanav_response`
- `morozov_essay`

So the API may accept `project_id`, but the actual inferential/logical analysis body still does not honestly analyze an arbitrary uploaded project corpus.

### 3. Logical scrutiny persistence is not backend-neutral either

`/home/evgeny/projects/the-critic/api/server.py`

The admitted logical-only scrutiny path still uses the same raw `psycopg2` / `DATABASE_URL` persistence and readback pattern.

That means:

- even if a fresh-project logical analysis runs
- the logical-only follow-up operation already admitted in the concept-family boundary can still fail to persist or read correctly on the active local SQLite-backed stack

So scrutiny persistence/read is not optional cleanup here.
It is part of making the already-admitted logical surface truthful.

### 4. The generic path already shows the intended seam

`/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py`

The generic concept path already follows the right basic pattern:

- accept `project_id`
- optionally accept preloaded `documents`
- load documents through the project-aware server path if needed

That means the next tranche should not invent a new architecture.
It should bring the admitted core submodes up to that same minimum runtime truth.

## Scope Summary

Implement a bounded runtime-enablement slice for the existing `Close Read` concept family.

This tranche should:

- keep the current `Close Read` concept routes and host shell unchanged
- make `inferential` and `logical` actually operate on the selected project's documents
- make concept detection persistence, concept-analysis persistence, and logical scrutiny persistence/readback work against the API's active database backend
- make a fresh uploaded project capable of producing admitted-core results that appear in:
  - `/p/:projectId/close-read/concepts`
  - `/p/:projectId/close-read/concepts/:conceptSlug`

This tranche should not:

- redesign the concept-family UI
- migrate `inferential` or `logical` fully into analyzer-v2-native engines/chains
- reopen the concept-family boundary memo
- add concept launch/detection UI under `Close Read`
- admit deferred concept submodes
- jump to the broader composition-layer problem

## Key Decisions To Freeze

### 1. The next slice is runtime enablement, not UI hardening

Do not center this tranche on visual polish.

The host/UI family is already sufficiently live to expose the real blocker:

- fresh-project concept runtime

### 2. Keep the current Close Read concept host contract

Do not change:

- `/p/:projectId/close-read/concepts`
- `/p/:projectId/close-read/concepts/:conceptSlug`
- current concept-family landing/detail law
- current admitted submode set:
  - `inferential`
  - `logical`

This tranche is specifically about making those existing surfaces materially usable on new projects.

### 3. Make persistence backend-neutral to the currently active API database

The concept runtime should persist through the same database backend the API is actually serving, whether that is:

- local SQLite fallback
- PostgreSQL

The scope should therefore reject any solution that merely says:

- "start local development on Postgres and leave the code alone"

That is not a product/runtime fix.
That is a local-environment workaround.

### 4. Make admitted core analyzers project-aware before attempting analyzer-v2-native migration

The next honest step is not a full rewrite of inferential/logical around analyzer-v2 definitions.

The next honest step is narrower:

- inject project-aware documents and project metadata into the existing inferential/logical analyzers
- genericize their prompt framing enough that they are no longer hardcoded to the Benanav/Morozov corpus
- preserve their current output schemas closely enough that the newly shipped `Close Read` concept family keeps working

Analyzer-v2-native migration remains a later step.

### 5. Fresh-project acceptance must be explicit

This tranche is not complete unless it proves the full intended user path on a newly created project with uploaded source material.

The memo should therefore require one real fresh-project acceptance run, not only unit tests.

## Implementation Shape

### A. Persistence seam normalization

Fix all three:

- detected-concept persistence
- concept-analysis result persistence
- scrutiny persistence and scrutiny result readback

so they use the same active database abstraction as the serving API.

Likely correct seam:

- reuse the existing database/session layer in:
  - `/home/evgeny/projects/the-critic/api/database.py`
- specifically:
  - `get_sync_session()`
  - `sync_session_maker`
- use sync SQLAlchemy session access for background-thread compatibility

This tranche should not require raw `psycopg2` as the only persistence path for concept detection, concept analysis, or scrutiny.

Scope answer:

- concept detection persistence: in scope
- concept-analysis persistence: in scope
- scrutiny persistence/readback: in scope

### B. Project-aware core concept analyzers

Bring the admitted core analyzers up to the minimum genericity already present in the generic concept path.

Required outcome:

- `run_inferential_analysis(...)` can accept project-aware documents and project metadata
- `run_logical_analysis_with_progress(...)` can accept project-aware documents and project metadata
- the API concept-analysis thread passes the selected project's documents into those analyzers instead of relying on fixed-corpus extraction

The correct seam is likely:

- load documents once in the API server via `load_documents(project_id)`
- pass them into the analyzer functions
- keep output structure stable for current web rendering

This is preferable to:

- teaching the analyzers to query the database directly
- or leaving them coupled to `extract_all_documents()`

### C. Prompt genericization, not wholesale prompt redesign

The inferential/logical prompts currently speak in Benanav-specific terms.
This is not one small string edit.

The scope should acknowledge the real editing surface:

- a large Benanav-specific inferential prompt body in:
  - `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py`
- plus deeper Benanav/NLR/Response hardcodings inside the 12-phase logical pipeline, including:
  - `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py`
  - `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py`
  - multiple phase prompt files under:
    - `/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/`

This tranche should genericize them enough that they can analyze arbitrary project corpora truthfully.

Expected minimum changes:

- remove fixed references to Benanav, Morozov, NLR, or specific named texts
- use project metadata such as:
  - `subject_author`
  - `subject_name`
  - document labels / doc types
- normalize logical phase/source labeling away from hardcoded `NLR 153` / `NLR 154` / `Response` assumptions where those labels currently shape prompts or output expectations
- preserve the same broad analytical intent:
  - inferential role / commitment mapping
  - logical structure / vulnerability mapping

This tranche should not yet try to solve:

- final analyzer-v2-native prompt ownership
- final concept-suite composition design
- final schema harmonization across old and new concept modes

### D. Fresh-project concept-detection path

Keep the existing endpoint contract:

- `POST /api/concepts/detect`
- `GET /api/concepts/detect/job/:jobId`
- `GET /api/concepts`

But make it honest on the current stack:

- detection jobs should run and persist concepts for the active project
- the result should not depend on a hidden PostgreSQL-only assumption

### E. Close Read acceptance path

The scope should require proving this exact user path:

1. create a new project
2. upload a new subject PDF
3. run concept detection successfully
4. run at least one admitted core concept analysis successfully:
   - `inferential` or `logical`
5. confirm the concept appears in:
   - `/close-read/concepts`
6. confirm the detail route renders:
   - `/close-read/concepts/:conceptSlug`
7. if the fresh-project concept has a logical result with scrutinizable premises, run one logical scrutiny job and confirm persisted readback works on the active stack

This is the acceptance path that converts the concept family from:

- "host route works only for legacy seeded data"

to:

- "host route works on a genuinely new uploaded corpus"

## Route / UI Contract

Do not change the public route contract in this tranche.

Keep:

- `/p/:projectId/close-read/concepts`
- `/p/:projectId/close-read/concepts/:conceptSlug`

Keep:

- current family switcher
- current landing card behavior
- current detail-page submode logic
- current result-backed-only posture

Do not add:

- concept launch form under `Close Read`
- concept detection button under `Close Read`
- concept dashboard chrome under `Close Read`

Those remain on native `/concept-analysis` routes.

## Explicit Non-Goals

This scope does not include:

- analyzer-v2-native rewrite of `inferential`
- analyzer-v2-native rewrite of `logical`
- admission of `assumption`
- admission of `semantic_field`
- admission of `causal`
- admission of `metaphorical`
- ammunition integration
- send-to-outline
- big-picture
- cross-concept
- broader composition-layer work
- standalone `Close Read` host work
- general UI redesign of the concept family

## Validation / Acceptance

This scope is complete only if all of the following are true:

### Runtime truth

- concept detection persists correctly on the active API database backend
- concept analyses persist correctly on the active API database backend
- scrutiny results persist and read back correctly on the active API database backend
- the serving API can list those results via existing endpoints

### Core analyzer truth

- `inferential` analyzes the selected project corpus, not the old Benanav fixed corpus
- `logical` analyzes the selected project corpus, not the old Benanav fixed corpus
- prompt framing is generic enough that the analysis is truthful for non-Benanav projects

### Fresh-project user path

- a brand-new uploaded project produces at least one admitted-core concept result
- the concept appears on `/close-read/concepts`
- the detail route renders under `Close Read`
- a logical scrutiny result can be created and read back for that same fresh-project concept when the logical surface exposes a scrutinizable premise

### Regression truth

- existing concept-family landing/detail route behavior remains intact
- native `/concept-analysis` routes remain intact
- current Close Read genealogy/AOI/concept coexistence still works

## Assumptions

- The current `Close Read` concept family host shell is sufficient to expose the runtime blocker.
- Project-aware genericization of the legacy core analyzers is the right next step before analyzer-v2-native migration.
- Persistence normalization should target the current active API database abstraction rather than mandate a specific local DB deployment posture.
- Fresh-project enablement is a more important next step than concept-family UI hardening.
- Analyzer-v2-native concept-family migration remains a later memo and implementation tranche.
