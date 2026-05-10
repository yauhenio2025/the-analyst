# Report: Close Read Concept Analysis Fresh Project Runtime Scope Audit

## Context Check

- Read in full: `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md`
- Read in full: `communications/MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md`
- Read in full: `communications/MEMO_2026-04-01_close_read_direction_dictation_reference.md`
- Read in full: `communications/MEMO_2026-04-01_close_read_direction_change_and_implications.md`
- Read in full: `communications/DYNAMIC_BESPOKE_APPS_VISION.md`

## Verdict

**approve with corrections**

The memo identifies the right next blocker and preserves the right roadmap ordering. The `Close Read` concept host tranche is already live enough on the Critic side: the umbrella routes exist, the family switcher includes `Concept Analysis`, the landing page computes concept-family availability, and the concept family pages are already result-backed and wired into logical scrutiny and capture ([routes.tsx](/home/evgeny/projects/the-critic/webapp/src/routes.tsx#L261), [CloseReadFamilySwitcher.tsx](/home/evgeny/projects/the-critic/webapp/src/components/CloseReadFamilySwitcher.tsx#L4), [CloseReadLandingPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx#L106), [closeReadConceptRuntime.ts](/home/evgeny/projects/the-critic/webapp/src/pages/closeReadConceptRuntime.ts#L57), [CloseReadConceptPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx#L482), [CloseReadConceptPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx#L594)).

The missing piece for fresh uploaded projects is runtime truth, not another host-shell tranche. The two corrections are:

- the memo under-specifies how deep the `logical` genericization must go
- scrutiny persistence should be explicitly included if the tranche still claims truthful local `Close Read` logical scrutiny

## Core Judgment

The memo is right about the main blocker.

- The host shell is already real. Route registration is present for `/p/:projectId/close-read/concepts` and `/p/:projectId/close-read/concepts/:conceptSlug` ([routes.tsx](/home/evgeny/projects/the-critic/webapp/src/routes.tsx#L263)).
- The umbrella landing already checks concept-family availability by loading concept-analysis summaries and grouping admitted `inferential`/`logical` results ([CloseReadLandingPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx#L138)).
- The concept family runtime already loads persisted analyses from the existing API, resolves slugs, and renders only the admitted core submodes ([closeReadConceptRuntime.ts](/home/evgeny/projects/the-critic/webapp/src/pages/closeReadConceptRuntime.ts#L57), [CloseReadConceptPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx#L609)).
- There is test coverage for the landing and concept-family shell, including admitted-submode behavior and unavailable-state handling ([CloseReadLandingPage.test.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.test.tsx#L92), [CloseReadConceptPages.test.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.test.tsx#L173)).

That means the current failure mode for a fresh project is not “no host family exists.” It is:

- no persisted detected concepts if concept detection is run on the local SQLite-backed stack
- no truthful `inferential`/`logical` analysis over uploaded project documents

## Corrections Required

### 1. The `logical` seam is deeper than the memo currently freezes

Passing project-loaded documents into `run_logical_analysis_with_progress(...)` is the correct top-level seam, but it is not sufficient by itself.

The current `logical` pipeline still hardcodes the Benanav/Morozov corpus at several layers:

- `prepare_documents_dict()` always calls `extract_all_documents()` and assigns fixed source labels `NLR 153`, `NLR 154`, `Response`, `Morozov` ([analyze_concept_logical.py](/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py#L50)).
- `PhaseBase` has a fixed `doc_key_map` for `NLR 153` / `NLR 154` / `Response` and only renders documents in `beyond_capitalism_1`, `beyond_capitalism_2`, `benanav_response`, `morozov_essay` order ([phase_base.py](/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py#L231), [phase_base.py](/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py#L364)).
- Phase 3 hardcodes `sub_passes = ["NLR 153", "NLR 154", "Response"]` and builds argument IDs and prompts around those names ([p03_argument_formalization.py](/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p03_argument_formalization.py#L19)).
- Phase 10 assumes an `NLR` versus `Response` comparison and explicitly frames the task as “Response to Morozov” ([p10_cross_text_comparison.py](/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p10_cross_text_comparison.py#L39)).
- Phase 12 synthesis still asks how Benanav defended against Morozov ([p12_synthesis.py](/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p12_synthesis.py#L38)).
- Some concept-analyzer Pydantic models still constrain sources to `NLR 153`, `NLR 154`, `Response` ([arguments.py](/home/evgeny/projects/the-critic/analyzer/concept_analyzer/models/arguments.py#L26), [quotes.py](/home/evgeny/projects/the-critic/analyzer/concept_analyzer/models/quotes.py#L12)).

Correction:

- keep the API-side seam the memo proposes
- explicitly include logical-pipeline source abstraction in scope:
  - dynamic source labels
  - dynamic per-document phase splitting
  - removal of Benanav/Morozov-specific comparison/synthesis law
  - widening source enums/models so non-default projects validate cleanly

Without that correction, the memo would understate the real work for `logical`.

### 2. Scrutiny persistence should be explicitly in scope if local-stack truth still matters

The current Close Read logical surface is not scrutiny-free. It loads saved scrutiny results on page mount and launches new scrutiny jobs from the family detail page ([CloseReadConceptPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx#L170), [CloseReadConceptPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx#L380), [CloseReadConceptPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx#L922)).

But scrutiny persistence still bypasses the API database abstraction:

- `_save_scrutiny_to_db(...)` uses raw `psycopg2` and direct `os.environ["DATABASE_URL"]` ([server.py](/home/evgeny/projects/the-critic/api/server.py#L6487))
- `GET /api/scrutiny/results/{concept}` does the same ([server.py](/home/evgeny/projects/the-critic/api/server.py#L6824))
- the `scrutiny_results` table already exists in the SQLAlchemy model layer and uses the cross-backend `JSONB` type ([models_db.py](/home/evgeny/projects/the-critic/api/models_db.py#L1147), [database.py](/home/evgeny/projects/the-critic/api/database.py#L40))

Correction:

- if this tranche still claims that the admitted logical `Close Read` surface is honest on the active local stack, make scrutiny save/read normalization explicitly in scope
- if not, defer it explicitly and remove scrutiny truth from the acceptance claim

Because the logical family already exposes scrutiny, I recommend including scrutiny persistence normalization in the same pass.

## Persistence Assessment

The memo is right that the current persistence split is dishonest relative to the API’s active database abstraction.

What already uses the abstraction:

- `database.py` provides SQLite fallback, async sessions, and sync sessions for background threads ([database.py](/home/evgeny/projects/the-critic/api/database.py#L18), [database.py](/home/evgeny/projects/the-critic/api/database.py#L82), [database.py](/home/evgeny/projects/the-critic/api/database.py#L108))
- the `concept_analyses`, `detected_concepts`, and `scrutiny_results` tables already exist in SQLAlchemy models ([models_db.py](/home/evgeny/projects/the-critic/api/models_db.py#L401), [models_db.py](/home/evgeny/projects/the-critic/api/models_db.py#L1147), [models_db.py](/home/evgeny/projects/the-critic/api/models_db.py#L2213))
- `GET /api/concept/analyses` and `GET /api/concept/analyses/{concept}` already read through `AsyncSession` and ORM models ([server.py](/home/evgeny/projects/the-critic/api/server.py#L4051), [server.py](/home/evgeny/projects/the-critic/api/server.py#L4095))

What still bypasses it:

- concept detection background persistence ([server.py](/home/evgeny/projects/the-critic/api/server.py#L3558))
- concept-analysis background persistence ([server.py](/home/evgeny/projects/the-critic/api/server.py#L3826))
- scrutiny save/read persistence ([server.py](/home/evgeny/projects/the-critic/api/server.py#L6487), [server.py](/home/evgeny/projects/the-critic/api/server.py#L6824))

So the right bounded fix is not “add Postgres-only workarounds.” It is:

- use the existing database abstraction
- use sync SQLAlchemy session access for background threads
- persist via ORM models or SQLAlchemy Core against the existing tables

That is the strongest bounded alternative. A weaker alternative would be adding more one-off `sqlite3`/`psycopg2` branching. The memo should not take that weaker path.

## Explicit Answers

### Is the memo right that the current `Close Read` concept family host shell is live enough, and that the missing piece is fresh-project runtime?

**Yes.** The host family already exists in routes, landing, switcher, summary grouping, detail-page loading, and tests ([routes.tsx](/home/evgeny/projects/the-critic/webapp/src/routes.tsx#L261), [CloseReadLandingPage.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx#L138), [CloseReadConceptPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx#L496), [CloseReadConceptPages.test.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.test.tsx#L173)). The missing piece is runtime truth for fresh uploaded projects.

### Does the code support the memo’s claim that `inferential` and `logical` are still fixed-corpus analyzers while the generic concept path is already project-aware?

**Yes, with a nuance.**

- `inferential` is fixed-corpus: it calls `extract_all_documents()`, hardcodes Benanav/Morozov framing in the prompt, and manually assembles `beyond_capitalism_*`, `benanav_response`, `morozov_essay` ([analyze_concept_inferential.py](/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py#L33), [analyze_concept_inferential.py](/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py#L233)).
- `logical` is fixed-corpus: it does the same at entry and then carries those assumptions deeper into the 12-phase pipeline ([analyze_concept_logical.py](/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py#L50), [phase_base.py](/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phase_base.py#L364), [p03_argument_formalization.py](/home/evgeny/projects/the-critic/analyzer/concept_analyzer/phases/p03_argument_formalization.py#L19)).
- the generic path is already project-aware at the document-loading seam: it accepts `project_id`, optionally accepts preloaded `documents`, and if needed loads project documents through `api.server.load_documents(project_id)` ([analyze_concept_generic.py](/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py#L24), [server.py](/home/evgeny/projects/the-critic/api/server.py#L1787)).

The nuance is that the generic path is project-aware primarily through document loading and ordering, not through richer project metadata such as `subject_author` / `subject_name`.

### Is using the API’s current database abstraction the right persistence fix, or is there a stronger bounded alternative?

**Yes, it is the right fix.** The strongest bounded form of that fix is:

- use `get_sync_session()` or the sync session factory from `database.py` for background threads ([database.py](/home/evgeny/projects/the-critic/api/database.py#L82))
- persist via `DetectedConceptDB`, `ConceptAnalysis`, and `ScrutinyResult` instead of raw driver SQL ([models_db.py](/home/evgeny/projects/the-critic/api/models_db.py#L401), [models_db.py](/home/evgeny/projects/the-critic/api/models_db.py#L1147), [models_db.py](/home/evgeny/projects/the-critic/api/models_db.py#L2213))

There is no stronger bounded alternative than using the abstraction that already exists.

### Does the memo correctly distinguish product/runtime repair from local-environment workaround?

**Yes.** The current broken paths are real code-path defects, not merely local setup preferences. `database.py` can already fall back to SQLite, but the concept-detection, concept-analysis, and scrutiny save/read code still look directly at `os.environ["DATABASE_URL"]` and assume `psycopg2` ([database.py](/home/evgeny/projects/the-critic/api/database.py#L18), [server.py](/home/evgeny/projects/the-critic/api/server.py#L3572), [server.py](/home/evgeny/projects/the-critic/api/server.py#L3834), [server.py](/home/evgeny/projects/the-critic/api/server.py#L6835)). Telling developers to “just use Postgres locally” would mask the defect instead of fixing runtime truth.

### Is passing project-loaded documents into the core analyzers the right seam, or should the fix happen elsewhere?

**Yes, that is the right seam.** The API should own:

- project lookup
- document loading
- persistence

The analyzers should receive prepared runtime inputs rather than query the database directly. That matches the generic concept path and keeps the fix bounded. The only adjustment is that `logical` needs more than bare documents: it also needs dynamic source labeling and source-model widening.

### Does the memo need to freeze more about prompt genericization, or is the current level of scope detail sufficient?

**It needs a bit more freeze for `logical`.**

The current memo is sufficient for `inferential` at a high level. It is not sufficient for `logical`, because the issue is not only prose wording; it is also fixed source taxonomy and phase structure. The scope should explicitly freeze:

- dynamic source labels instead of `NLR 153` / `NLR 154` / `Response`
- dynamic per-document phase splitting instead of fixed three-document sub-passes
- removal of Benanav/Morozov-specific synthesis and comparison law

### Should scrutiny persistence be explicitly in scope together with concept detection / concept analysis persistence, or is the conditional framing adequate?

**It should be explicitly in scope if the tranche still claims truthful local logical `Close Read`.**

The current conditional framing is too weak because the logical `Close Read` family already loads saved scrutiny results and launches new scrutiny jobs ([CloseReadConceptPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx#L170), [CloseReadConceptPages.tsx](/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx#L380)). If the active local stack matters, scrutiny persistence/read normalization belongs in the same repair pass.

### Is the fresh-project acceptance path concrete and testable enough to justify implementation?

**Mostly yes.** The path is concrete. I would add three explicit assertions so the acceptance test proves the actual blocker is fixed:

- after detection, `GET /api/concepts` returns detected concepts for the fresh project
- after analysis, `GET /api/concept/analyses` and `GET /api/concept/analyses/{concept}` return persisted admitted-core results on the active backend
- if scrutiny remains in scope, `GET /api/scrutiny/results/{concept}` round-trips after a logical scrutiny run

With those additions, the acceptance path is concrete and testable.

### Does the memo preserve the right bigger-picture ordering relative to current default-family work, later analyzer-v2-native migration, later composition-layer work, and later standalone Close Read host work?

**Yes.** The memo stays aligned with the 2026-04-05 roadmap stack:

- current default-family work first
- fresh-project runtime repair before analyzer-v2-native migration
- composition-layer work still later
- standalone `Close Read` host still later

That ordering is consistent with the broader `Close Read` roadmap and the larger `Dynamic Bespoke Apps` direction.

## Final Recommendation

Ship this memo as the next implementation scope **after** making the two corrections above:

1. explicitly widen the `logical` genericization sub-scope beyond top-level document passing
2. explicitly include scrutiny persistence/read normalization if the local logical `Close Read` surface is still part of the truthful accepted product

With those corrections, the memo is the right bounded next move.
