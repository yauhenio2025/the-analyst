# Review: Close Read Concept-Analysis Fresh-Project Runtime Scope

Reviewer: Claude (Opus 4.6)
Date: 2026-04-06
Memo Under Review: `communications/MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md`

## Context Check

Confirmed read in full:

- `MEMO_2026-04-06_close_read_concept_analysis_fresh_project_runtime_scope.md` — the scope memo under review
- `MEMO_2026-04-05_close_read_concept_analysis_family_implementation_scope.md` — the UI/family implementation scope that shipped the concept family host shell
- `MEMO_2026-04-05_close_read_concept_analysis_family_boundary_memo.md` — the product boundary that froze inferential + logical as the first admitted core
- `MEMO_2026-04-05_close_read_concept_analysis_family_admission_audit.md` — the family inventory that mapped old concept estate to analyzer-v2
- `MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` — the roadmap clarification: default families first, composition layer later
- `MEMO_2026-04-05_close_read_multi_engine_v1_5_boundary_memo.md` — the multi-engine boundary: genealogy + AOI as first umbrella families
- `MEMO_2026-04-05_close_read_multi_engine_v1_5_coexistence_scope.md` — the umbrella coexistence implementation scope
- `MEMO_2026-04-01_close_read_direction_dictation_reference.md` — the original user dictation establishing Close Read direction
- `MEMO_2026-04-01_close_read_direction_change_and_implications.md` — the implications memo: missing operation layer, Close Read as flagship

Confirmed code inspection:

- `/home/evgeny/projects/the-critic/api/server.py` — API server, concept analysis thread, persistence paths, load_documents
- `/home/evgeny/projects/the-critic/api/database.py` — database abstraction with SQLite/PostgreSQL dual backend
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_inferential.py` — inferential analyzer, hardcoded Benanav corpus
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_logical.py` — logical analyzer, hardcoded Benanav corpus via extract_all_documents
- `/home/evgeny/projects/the-critic/analyzer/analyze_concept_generic.py` — generic analyzer, already project-aware via load_documents
- `/home/evgeny/projects/the-critic/analyzer/extract.py` — document extraction, hardcoded Benanav/Morozov file patterns
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadConceptPages.tsx` — concept family pages, already shipped
- `/home/evgeny/projects/the-critic/webapp/src/pages/closeReadConceptRuntime.ts` — concept runtime helpers, already shipped
- `/home/evgeny/projects/the-critic/webapp/src/pages/CloseReadLandingPage.tsx` — umbrella landing, concept card already present
- `/home/evgeny/projects/the-critic/webapp/src/components/CloseReadFamilySwitcher.tsx` — family switcher, concept family already included

Note: `DYNAMIC_BESPOKE_APPS_VISION.md` was also assigned but did not affect the analysis materially beyond what the dictation reference and implications memo already cover.

---

## Verdict

**Approve with corrections.**

The scope memo is overwhelmingly correct in its diagnosis, its proposed implementation shape, and its strategic framing. It identifies the right blocker, names the right two seams, and correctly avoids reopening product boundaries that were already frozen. The corrections below are material but bounded — they sharpen the scope rather than redirect it.

---

## Detailed Assessment

### 1. Is the memo right that the current blocker is runtime enablement rather than more Close Read concept UI work?

**Yes.** This is the memo's strongest claim and the code conclusively proves it.

The concept family host shell already exists and is functional:

- `CloseReadConceptPages.tsx` — full index and detail page, 944 lines
- `closeReadConceptRuntime.ts` — summary loading, grouping, slug resolution, detail fetch, 156 lines
- `CloseReadLandingPage.tsx` — concept card already in the umbrella landing, discovery wired up
- `CloseReadFamilySwitcher.tsx` — concept family already in the switcher

The UI is complete enough to render concept results if they existed. What does not exist yet is a path to produce those results for a fresh project. So the memo's claim that the blocker is runtime truth, not UI, is correct.

### 2. Does the memo correctly identify two separate seams?

**Yes, and this is precisely confirmed by the code.**

#### Seam 1: Project-awareness of inferential/logical

In `server.py`, the concept analysis thread at line 3900-3910:

```python
if analysis_type == AnalysisType.INFERENTIAL.value:
    result = run_inferential_analysis(concept)  # NO project_id, NO documents
elif analysis_type == AnalysisType.LOGICAL.value:
    result = run_logical_analysis_with_progress(concept, ...)  # NO project_id, NO documents
```

Both call `extract_all_documents()` in `extract.py`, which searches for hardcoded filenames:

```python
("beyond_capitalism_1", ["Aaron Benanav, Beyond Capitalism 1, NLR 153..."]),
("beyond_capitalism_2", ["Aaron Benanav, Beyond Capitalism 2, NLR 154..."]),
("benanav_response", ["Benanav_dft2.docx", ...]),
("morozov_essay", ["Evgeny Morozov - Socialism After AI", ...]),
```

Compare with the generic path at line 3923-3931, which correctly passes `project_id`:

```python
result = run_generic_analysis(concept, "concept_semantic_field", project_id)
```

And inside `run_generic_analysis`, it calls `load_documents(project_id)` which queries the database for project documents. This is exactly the seam the memo proposes following.

#### Seam 2: Backend-neutral persistence

In `server.py`, `_save_concept_analysis_to_db` (line 3826-3873) uses raw `psycopg2`:

```python
import psycopg2
database_url = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(database_url, connect_timeout=30)
cur.execute("INSERT INTO concept_analyses ...")
```

And `_run_concept_detection_sync` (line 3558-3767) also uses raw `psycopg2` for concept detection persistence.

Meanwhile, `database.py` already provides a backend-neutral sync session factory:

```python
sync_session_maker = sessionmaker(sync_engine, class_=Session, ...)
def get_sync_session() -> Session:
    return sync_session_maker()
```

This factory works with both SQLite and PostgreSQL. The raw `psycopg2` calls bypass it entirely and will fail on SQLite. So the persistence blocker is real and precisely as the memo describes.

### 3. Is it correct to keep the current Close Read concept route contract fixed in this tranche?

**Yes.** The route contract and UI are already shipped and working. The pages correctly handle missing results with bounded empty states, links back to the umbrella, and links to native `/concept-analysis`. The issue is not that the routes are wrong — it is that nothing populates them for new projects. Keeping routes fixed is the right call.

### 4. Does the memo correctly reject "just switch local development to Postgres" as a sufficient product/runtime fix?

**Yes, emphatically.** The code proves this is not merely a philosophical point:

1. `database.py` already has a real SQLite fallback path (lines 22-28) that fires when `DATABASE_URL` is absent or matches the old default.
2. The async API routes work on SQLite because they use `async_session_maker`.
3. But background threads doing concept work bypass this and use raw `psycopg2`, which will crash on SQLite with an import error or a connection string mismatch.

This is not an edge case. It is a hard crash on the path the memo targets. "Just use Postgres locally" would suppress the symptom but leave the architectural gap unaddressed. Production (Render) happens to use Postgres, but the codebase explicitly supports SQLite and many local development paths depend on it.

### 5. Is the proposed reuse seam correct?

**Yes.** The proposed pattern — load documents via `load_documents(project_id)`, inject them into the core analyzers, avoid teaching analyzers to query the database — is exactly the pattern the generic path already follows. The generic analyzer (`analyze_concept_generic.py`) takes an optional `documents` parameter and falls back to `load_documents(project_id)` if not provided. The inferential and logical analyzers should follow the same pattern.

The specific seam is also correct because `load_documents` is already backend-neutral (it uses SQLAlchemy sessions for non-default projects) and already handles document metadata (`doc_type`, `engagement_type`, `is_primary`).

### 6. Does the memo overstate how easy it is to genericize the current inferential/logical prompts away from the Benanav/Morozov corpus?

**Slightly, yes. This is a correction.**

The inferential prompt in `analyze_concept_inferential.py` is deeply Benanav-specific across ~230 lines of prompt text:

- "Benanav" appears 25+ times in the prompt template
- Fixed references: "Beyond Capitalism" Parts 1 & 2, NLR 153-154, "Response to Morozov"
- Document assembly is hardcoded: `for key in ['beyond_capitalism_1', 'beyond_capitalism_2']`
- JSON output schema references: `"source": "NLR 153|NLR 154|Response"`

The logical analyzer (`analyze_concept_logical.py`) delegates to `ConceptAnalyzerOrchestrator` which itself calls `prepare_documents_dict()` — also hardcoded to the same four Benanav/Morozov document keys. The 12-phase orchestrator likely has Benanav-specific framing in individual phase prompts as well.

The memo says "genericize them enough that they can analyze arbitrary project corpora truthfully" and lists expected minimum changes. That list is correct but understates the effort:

- The inferential prompt requires author-name substitution across ~25 occurrences
- The document assembly in both analyzers needs to accept arbitrary document sets
- The JSON output schema source labels need to become dynamic
- The 12-phase logical orchestrator has its own document-preparation function that also needs this treatment
- Phase-specific prompts inside the orchestrator may also reference Benanav/Morozov

None of this is architecturally hard — it is a find-and-replace-plus-parameterize operation. But the memo should acknowledge that the prompt genericization is a non-trivial editing pass across at least 3-4 files and possibly 12+ phase prompt templates, not a single-point change.

**Recommended correction:** Add a note under Section C that the prompt genericization pass should budget for editing the `ConceptAnalyzerOrchestrator` phase prompts as well, not just the top-level analyzer entry points. Verify which phases reference Benanav/Morozov directly before starting implementation.

### 7. Is the memo right to keep this tranche narrower than a full analyzer-v2-native migration?

**Yes.** The admission audit (`MEMO_2026-04-05`) already established the three-way migration split: legacy-local (inferential/logical), external-bridge (assumption), and analyzer-v2-backed generic (semantic_field/causal/metaphorical). The inferential and logical analyzers are deep legacy-local code with substantial operational logic. A full rewrite into analyzer-v2-native chains would be a much larger effort and would risk destabilizing the concept family that was just shipped.

The "minimal genericization" approach — accept `project_id` and documents, replace Benanav-specific framing with project-metadata-driven framing, preserve output schemas — is the correct next step. It makes the existing runtime work for fresh projects without requiring a migration that would touch the 12-phase logical orchestrator's internal phase design.

### 8. Should scrutiny persistence be included in this same runtime-normalization pass?

**Yes, it should be in scope. This is a correction.**

The memo conditionally defers scrutiny persistence: "only if needed to keep logical-only Close Read scrutiny honest on the active local stack." But the code shows it IS needed:

`_save_scrutiny_to_db` at server.py line 6488 also uses raw `psycopg2`:

```python
import psycopg2
conn = psycopg2.connect(database_url, connect_timeout=30)
```

The concept family's logical surface explicitly admits scrutiny (per the boundary memo). The `CloseReadConceptDetailContent` component wires up `useCloseReadLogicalScrutiny` which polls scrutiny endpoints. If scrutiny generation and persistence fail on the local SQLite stack, the logical surface's most distinctive feature is broken for fresh projects.

Since this tranche's goal is "make the existing Close Read concept family work on new uploaded projects," and the logical surface includes scrutiny, scrutiny persistence normalization should be unconditionally in scope — not conditional.

**Recommended correction:** Promote scrutiny persistence from conditional/deferred to in-scope. The normalization is the same pattern as concept-analysis persistence: replace raw `psycopg2` with `get_sync_session()` from `database.py`.

### 9. Is the fresh-project acceptance path concrete enough?

**Mostly, but needs one addition.**

The acceptance path (Section E) correctly lists the essential user steps: create project, upload PDF, detect concepts, run admitted core analysis, confirm appearance on `/close-read/concepts`, confirm detail route. This is clear and testable.

However, the path should also include:

- **Step 4b**: On the logical surface, trigger at least one scrutiny operation and confirm the scrutiny result persists and renders.

This is needed because scrutiny is admitted in the concept family's logical surface and is part of what distinguishes the concept family from a read-only surface. If the acceptance path does not test scrutiny, the tranche could pass acceptance while scrutiny is still broken on the local stack.

**Recommended correction:** Add scrutiny generation/rendering verification to the fresh-project acceptance path.

### 10. Does this scope preserve the roadmap distinction between default family completion, later composition-layer work, and later standalone-host work?

**Yes, cleanly.** The scope explicitly lists as non-goals:

- analyzer-v2-native rewrite (this would be composition-layer territory)
- admission of deferred submodes (family expansion)
- broader composition-layer work
- standalone Close Read host work
- general UI redesign

The roadmap memo (`MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md`) established three horizons:
1. Default families (genealogy, AOI, concept analysis)
2. Composition layer for bespoke modules
3. Standalone host

This tranche operates entirely within horizon 1: completing the concept-analysis default family by making its runtime honest for fresh projects. It does not step into horizon 2 or 3. The explicit non-goals list correctly guards against scope drift.

---

## Summary of Corrections

### Mandatory corrections (include before implementation):

1. **Promote scrutiny persistence to in-scope.** The boundary memo admits logical scrutiny. The scrutiny persistence path uses the same raw `psycopg2` pattern as concept analysis/detection persistence. If it is not normalized, the logical surface's most distinctive feature is broken for fresh projects. This is not conditional — it is a direct consequence of the tranche's own success criteria.

2. **Add scrutiny verification to the acceptance path.** The fresh-project acceptance path should include triggering a scrutiny operation on the logical surface and confirming it persists and renders.

### Recommended additions (improve implementation clarity):

3. **Acknowledge prompt genericization scope explicitly.** The memo should note that the inferential prompt is ~230 lines of Benanav-specific text, and the logical orchestrator has 12 phase prompts that may also reference Benanav/Morozov. The implementation should audit all phase prompts in `analyzer/concept_analyzer/` before starting the genericization pass.

4. **Name the existing sync session abstraction.** The implementation shape section correctly identifies `database.py` as the reuse target but does not name the specific seam: `get_sync_session()` and `sync_session_maker` already exist in `database.py` and provide backend-neutral synchronous sessions suitable for background threads. Naming this explicitly would prevent implementors from inventing a new abstraction.

### Not corrections (affirmations):

- The "runtime truth, not UI hardening" framing is correct
- The two-seam diagnosis is code-backed and precise
- The route/UI contract freeze is correct
- Rejecting "just use Postgres" is correct
- The `load_documents(project_id)` reuse seam is correct
- Keeping the tranche narrower than analyzer-v2-native migration is correct
- The explicit non-goals list correctly guards scope

---

## Final Assessment

This is a well-crafted scope memo that correctly identifies the blocker exposed by fresh-project testing, diagnoses its root causes against the actual codebase, and proposes a bounded implementation that addresses the immediate runtime gap without reopening product boundaries or jumping to premature migrations.

The two corrections (scrutiny persistence in scope, scrutiny verification in acceptance) are logical consequences of the memo's own decisions and the boundary memo it references. The prompt genericization note is a practical improvement for implementation planning.

The memo's strategic framing — that this is a runtime-enablement tranche, not UI work, and not a full migration — is correct and well-aligned with the broader Close Read roadmap.
