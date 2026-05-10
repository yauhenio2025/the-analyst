# REPORT: Shared Substrate Addendum Implementation Audit

Date: 2026-03-16
Auditor: Claude Opus 4.6 (1M context)
Source: `communications/MEMO_2026-03-16_shared_substrate_addendum_after_reviews.md`

---

## 1. Claim Check

Each addendum claim is tested against actual code.

### Claim 1: "analyzer-v2's strongest current asset is the definition/execution substrate, not an artifact economy"

**Verdict: TRUE. Evidence is unambiguous.**

The codebase has a rich definition layer:
- 160+ engine definitions in `src/engines/definitions/`
- 14+ operationalizations in `src/operationalizations/definitions/` (including 4 AOI-specific)
- 8 workflow definitions in `src/workflows/definitions/`
- 25 chain definitions in `src/chains/definitions/`
- 21+ view definitions in `src/views/definitions/`
- 3 analysis objectives in `src/objectives/definitions/`
- 5 audience profiles in `src/audiences/definitions/`

Execution is real and functional:
- `src/executor/workflow_runner.py` — DAG-ordered phase execution with parallelism, mid-course revision
- `src/executor/chain_runner.py` — sequential multi-engine chain execution
- `src/executor/phase_runner.py` — per-phase resolution (engine vs chain, single vs per_work)
- `src/executor/engine_runner.py` — atomic LLM calls with streaming, retry, partial salvage
- `src/orchestrator/adaptive_planner.py` — LLM-based adaptive plan generation

**What it does NOT have**: any concept of "analytical artifact" distinct from a phase output or presentation cache entry. The word "artifact" in the codebase refers exclusively to `presentation_artifacts` — job-scoped rendering cache entries in `src/presenter/artifact_store.py`.

### Claim 2: "A first-class analytical artifact layer is the main missing abstraction"

**Verdict: TRUE. The gap is structural, not cosmetic.**

Evidence:

**DB schema** (`src/executor/db.py:288-328`): The `phase_outputs` table is the only place analytical content is persisted. Its primary query paths are:
- `job_id` (required for every query)
- `phase_number` (secondary filter)
- `engine_key` (secondary filter)
- `work_key` (secondary filter)

There is NO column for: artifact type, artifact identity, document identity, thinker identity, or any key that would enable cross-job lookup.

**Output store** (`src/executor/output_store.py`): Every function signature starts with `job_id: str`. The functions are:
- `save_output(job_id, ...)` — line 22
- `load_phase_outputs(job_id, ...)` — line 67
- `load_all_job_outputs(job_id, ...)` — line 104
- `load_outputs_for_context(job_id, ...)` — line 136
- `get_latest_output_for_phase(job_id, ...)` — line 178

There is literally no function that accepts anything other than `job_id` as the primary lookup key.

**Context broker** (`src/executor/context_broker.py:24-47`): `assemble_phase_context()` takes `job_id` and `upstream_phases` — it can only assemble context from phases within the same job. No mechanism for pulling context from a different job's outputs.

**Variant system** (`src/api/routes/variants.py:90`): Explicitly guards against cross-job access: `"Enforce job_id matches the variant set's job — prevents cross-job pollution"`.

### Claim 3: "Current outputs are still too job-scoped / workflow-scoped / consumer-scoped for cross-objective reuse"

**Verdict: TRUE. Three distinct scoping walls confirmed.**

1. **Job-scoped**: All `phase_outputs` queries require `job_id`. No cross-job query exists anywhere.

2. **Workflow-scoped**: AOI normalization in `src/aoi/contract.py` embeds workflow-specific stitching:
   - `_load_previous_normalized(job_id, engine_key)` (line 132) loads the previous engine's normalized output to feed into the next normalization step
   - Theme IDs, engagement IDs, finding IDs are all generated within a single job's execution scope
   - The normalization builds `structured_payloads` (by_theme, by_sin_type) that are specific to the AOI workflow structure

3. **Consumer-scoped**: View definitions hardcode their consumer: `"target_app": "the-critic"` (see `src/views/definitions/aoi_thematic_analysis.json:7`). Auto-presentation in `workflow_runner.py` defaults to `consumer_key="the-critic"` (confirmed by earlier audit at dirty-main line 696).

### Claim 4: "The Critic still contains important lifecycle and delivery responsibilities that have not been moved into analyzer-v2"

**Verdict: TRUE. Confirmed by deep audit of The Critic codebase.**

The Critic contains a 968-line analyzer-v2 client (`the-critic/analyzer/concept_analyzer/analyzer_v2_client.py`) that reimplements platform logic:

**Platform-generic logic currently in The Critic** (should move to analyzer-v2 SDK):
- **Job submission**: `start_analysis_sync()` (lines 574-666) — constructs payload, submits to orchestrator pipeline
- **Job polling**: `poll_analysis_sync()` (lines 669-707) — with custom long_timeout mode for cross-region latency
- **Job resume**: `resume_analysis_sync()` (lines 759-792) — resume from checkpoint after failure
- **Fallback presentation fetch**: `fetch_page_presentation_sync()` (lines 710-737) — 300s timeout workaround when orchestrator times out
- **Version polling thread**: (lines 905-969) — polls `/v1/meta/definitions-version` every 5 minutes for cache invalidation
- **Transient failure retry**: (`server.py:18058-18110`) — detects "instance recycled" errors and auto-retries
- **Job ID mapping**: `_V2_JOB_MAPPINGS` (`server.py:17875`) — maintains Critic job_id ↔ v2 job_id mapping

**Consumer-specific logic that should stay in The Critic**:
- Result persistence to `genealogy_analyses` table (`server.py:18239-18328`) — Critic's own schema
- Thinker identity extraction from v2 results (`server.py:18209-18230`)
- Project scoping and document loading (`server.py:18423-18509`)

**Key finding**: The Critic implements its own polling loop (`server.py:17904-18040`) that sleeps, checks cancellation, polls analyzer-v2, handles failures (up to 10 consecutive), translates progress, and manages completion. This entire loop is consumer-generic — any consumer needs the same pattern. It should be in an analyzer-v2 client library, not reimplemented per consumer.

### Claim 5: "analyzer-mgmt is not yet a packaging/publication layer"

**Verdict: TRUE. It is an inspection and editing UI.**

Based on the API routing pattern documented in project memory: analyzer-mgmt's frontend has TWO API targets:
- `API_BASE` (mgmt-api backend) — for engines, paradigms, pipelines, consumers, changes, grids, LLM
- `ANALYZER_V2_URL` — for definitions that live in analyzer-v2: styles, primitives, display, rhetoric, audiences

The mgmt-api backend provides:
- CRUD for engine definitions, paradigm definitions
- Pipeline management
- Consumer configuration browsing
- Change tracking
- Grid configuration

It does NOT provide:
- Artifact browsing or versioning
- Cross-job output inspection
- Publication or packaging workflows
- Consumer contract management

### Claim 6: "AOI is a good bounded artifact pilot"

**Verdict: TRUE, with a significant qualification.**

AOI is a good pilot because:

1. **It already has structured normalization**: `src/aoi/contract.py` (698 lines) is literally a hand-built artifact normalization layer. It takes raw LLM JSON, normalizes it into typed structures (themes, engagements, findings, reports), assigns stable IDs (`theme_id`, `engagement_id`, `finding_id`), and stitches cross-phase references.

2. **Its outputs have clear identity**: Themes have `theme_id`, findings have `finding_id`, source documents have `source_document_id`. These are already artifact-shaped.

3. **Its pipeline is sequential and bounded**: 4 phases, each consuming the prior's normalized output. No parallel branching complexity.

4. **Its operationalizations are clean**: 4 YAML files in `src/operationalizations/definitions/aoi_*.yaml` with clear stance/depth sequences.

**Qualification**: The AOI contract layer is currently embedded in the executor's hot path via `chain_runner.py`. Making AOI the pilot means refactoring this bespoke normalization into the new artifact layer — which is exactly the right test, but it touches a live execution path.

### Claim 7: "Genealogy is the right chain-rich artifact pilot after AOI"

**Verdict: TRUE, but harder than the addendum implies.**

Genealogy evidence:
- 3 dedicated chains: `genealogy_target_profiling_chain`, `genealogy_prior_work_scanning_chain`, `genealogy_synthesis_chain`
- Each chain composes 3-5 engines sequentially
- The `genealogy_synthesis_chain` alone chains: `concept_synthesis` → `concept_taxonomy_argumentative_function` → `evolution_tactics_detector` → `conditions_of_possibility_analyzer`
- 14 genealogy-specific operationalizations in `src/operationalizations/definitions/`
- 21+ genealogy view definitions in `src/views/definitions/`
- Rich planner strategy in `src/objectives/definitions/genealogical.json` (massive planner_strategy field with supplementary chain selection, per-work routing, chapter targeting, model routing guidance)

Why it's harder:
- Genealogy outputs are primarily **prose**, not structured JSON. The context broker concatenates prose blocks with markdown formatting. There is no normalization layer like AOI's `contract.py`.
- The intermediate products (target profile, relationship classifications, evolution timelines) would need new normalization contracts to become first-class artifacts.
- Genealogy has **per-work iteration** (Phase 2.0 runs once per prior work), which adds a `work_key` dimension that AOI doesn't have.
- The presenter has genealogy-specific repair logic (scaffold contracts, manifest builder) that would also need to be addressed.

### Claim 8: "Generated bespoke apps should be treated as a later consequence, not the next direct tranche"

**Verdict: TRUE. The infrastructure gap is real.**

Auto-presentation currently hardcodes `consumer_key="the-critic"`. Views hardcode `target_app: "the-critic"`. The presenter's dynamic prompt composition and transformation execution are consumer-aware but not consumer-neutral — they assume a specific rendering target.

Generating bespoke apps requires:
1. An artifact layer (doesn't exist)
2. A consumer-neutral delivery contract (doesn't exist — consumer identity is baked in)
3. A view generation mechanism that isn't hardcoded to The Critic's page structure (partially exists in view patterns, but not tested with a second consumer)

---

## 2. Current Architectural Reality

### Hot Path Diagram

```
User Request
    │
    ▼
pipeline.py:run_analysis_pipeline()
    ├── document_store.store_document()      ── Documents go into executor_documents table
    ├── adaptive_planner.generate_plan()     ── Plan goes into orchestrator/plans/ JSON files
    └── workflow_runner.execute_plan()
            │
            ├── for each phase group (DAG order):
            │       │
            │       ├── phase_runner.run_phase()
            │       │       │
            │       │       ├── context_broker.assemble_phase_context(job_id, upstream_phases)
            │       │       │       └── output_store.load_outputs_for_context(job_id, phase_numbers)
            │       │       │               └── SELECT * FROM phase_outputs WHERE job_id = ? AND phase_number IN (?)
            │       │       │
            │       │       ├── [if chain] chain_runner.run_chain()
            │       │       │       └── for each engine in chain:
            │       │       │               engine_runner.run_engine_call()
            │       │       │                   └── Claude/Gemini API call
            │       │       │               output_store.save_output(job_id, phase, engine, content)
            │       │       │                   └── INSERT INTO phase_outputs (job_id, ...)
            │       │       │               [if AOI] aoi.contract.build_aoi_output_metadata()
            │       │       │                   └── Normalize → store in metadata JSONB
            │       │       │
            │       │       └── [if engine] similar, without chain wrapper
            │       │
            │       └── job_manager.save_phase_result()
            │
            └── _run_auto_presentation()
                    ├── view_refiner.refine_views()
                    └── presentation_bridge.prepare_presentation()
                            └── For each view:
                                    ├── Find matching phase_output (by job_id + engine_key)
                                    ├── Find transformation template (or dynamic prompt)
                                    └── Save to presentation_cache (by output_id + section)
```

### Key Tables and Their Scoping

| Table | Primary Key | Scope | Cross-Job? |
|-------|-------------|-------|------------|
| `executor_jobs` | `job_id` | per-plan | No |
| `phase_outputs` | `id` (uuid), indexed by `job_id` | per-job | No |
| `presentation_cache` | `output_id + section` | per-output | No |
| `presentation_artifacts` | `job_id + view_key + artifact_kind + version + hash` | per-job+view | No |
| `executor_documents` | `doc_id` | global | Yes (but disconnected) |
| `projects` | `project_id` | organizational | Groups jobs, no artifact sharing |

### The One Cross-Job Table

`executor_documents` is the only table that stores content independently of a job. Documents have their own `doc_id` and are linked to jobs via the `document_ids` JSONB column in `executor_jobs`. But this is upload storage — there is no mechanism to say "this analysis of document X exists and can be reused by another job."

---

## 3. What The Addendum Correctly Fixes

### 3.1 Corrects the "we're almost there" framing

The original shared substrate memo implied proximity to generated bespoke apps. The addendum correctly identifies that **the artifact layer is the missing center**, not a nice-to-have. Without it, "shared substrate" is just "good code organization."

### 3.2 Correctly sequences artifact-first, then consumer-neutral, then generated apps

The 6-stage sequence (artifact schemas → AOI pilot → genealogy pilot → consumer-neutral SDK → analyzer-mgmt packaging → generated apps) is architecturally sound. Each stage builds on the prior. Skipping to generated apps without the artifact layer would reproduce The Critic's pattern in new wrappers.

### 3.3 Correctly identifies AOI contract.py as trapped artifact logic

The AOI `contract.py` (698 lines) is literally a hand-built artifact layer: it assigns stable IDs, normalizes LLM JSON into typed structures, stitches cross-phase references, and builds presentation payloads. This code is doing artifact work without artifact infrastructure. The addendum correctly identifies that this pattern should be generalized.

### 3.4 Correctly downgrades analyzer-mgmt's current role

analyzer-mgmt is inspection/editing. Calling it a "packaging layer" before the artifact layer exists would create premature responsibilities.

---

## 4. What Is Still Missing Or Mis-Sequenced

### 4.1 The addendum doesn't address the prose vs structured divide

AOI outputs are structured JSON that gets normalized by `contract.py`. Genealogy outputs are prose blobs that get concatenated by `context_broker.py`. These are fundamentally different artifact shapes.

The addendum treats "artifact" as if it's one thing. In practice:
- **AOI artifacts** = structured JSON with typed fields, stable IDs, and cross-phase references
- **Genealogy artifacts** = rich prose with embedded reasoning, textual evidence chains, and implicit structure

An artifact layer that works for AOI's structured JSON won't automatically work for genealogy's prose. The addendum should explicitly address this divide and decide whether genealogy artifacts are:
- Extracted structured data (like AOI's normalization)
- Annotated prose blocks (with metadata headers and cross-references)
- Both (with different artifact subtypes)

### 4.2 The pilot sequencing (AOI first, genealogy second) is defensible but debatable

The addendum recommends AOI first because "its contracts are already relatively structured." A counterargument exists: genealogy is more mature (7+ operationalized engines, 15+ views, 3 composable chains vs AOI's 4 engines, 5 views, 0 chains) and would better demonstrate that the artifact layer handles sophisticated composition.

**Why AOI first is still correct**: AOI already has `src/aoi/contract.py` — 698 lines of hand-built normalization that assigns stable IDs, normalizes JSON, and stitches cross-phase references. This IS the trapped artifact layer. Genealogy has no equivalent normalization contract; its outputs are prose blocks concatenated by the generic context broker. Starting with AOI means extracting existing artifact-like code into the new layer, not writing new normalization from scratch.

**The addendum is right**: start with the case where artifact-shaped code already exists (AOI), then tackle the case where it doesn't yet exist (genealogy).

### 4.3 The addendum underestimates The Critic's remaining role

The addendum says "too much platform behavior still lives in The Critic" and proposes extracting a consumer-neutral SDK in Stage 4. But it doesn't specify which responsibilities move and which stay. Based on code:

- **Must move**: Job polling patterns, result restoration contracts, presentation cache access patterns
- **Should stay**: UX-specific layout decisions, visual theme, user authentication, editorial workflows
- **Gray area**: Document upload UX, plan review/approval flow, analysis configuration

Without this specificity, Stage 4 will be underscoped.

### 4.4 The addendum doesn't address the `content_hash` / invalidation problem

`phase_outputs` already has a `content_hash` column (`src/executor/db.py:219`). This was added for stale-detection in presentation cache. But for a real artifact layer, invalidation is harder:

- If you re-run an engine with different input documents, the old artifact should be invalidated
- If an upstream artifact changes (e.g., themes change), downstream artifacts (engagements, findings) become stale
- The current system has no cascade invalidation — each cache check is local

The addendum lists "artifact invalidation" as a requirement but doesn't address the cascade problem.

### 4.5 The addendum doesn't mention the `shares_with` / `consumes_from` metadata in capability definitions

The dirty-main audit found that capability definitions already have `shares_with` and `consumes_from` fields (e.g., `aoi_thematic_synthesis.yaml:67`, `aoi_engagement_mapping.yaml:57`). These are currently prompt/planner metadata, not runtime routing. But they are the natural place to declare artifact contracts. The addendum should reference these as the starting point for artifact identity, not propose a wholly new schema.

### 4.6 The addendum doesn't address the operationalization→artifact bridge

Operationalizations define how an engine processes content through stance sequences with multi-pass depth. The artifact question is: at what granularity does an artifact get created?

- Per-phase? (current model — one blob per phase)
- Per-engine? (finer — one artifact per engine invocation)
- Per-pass? (finest — one artifact per stance pass within an engine)

The AOI contract normalizes at the per-engine level. But the operationalization structure supports per-pass accumulation (`consumes_from` in depth sequences). The addendum should take a position on this.

---

## 5. Minimal Corrected Program

Accept the addendum's direction but tighten the scope.

### Stage 0: Artifact Schema Design (1-2 sessions)

Before writing code, answer these questions:
1. What is the primary key of an artifact? (Proposal: `artifact_type + source_document_fingerprint + engine_key + version`)
2. Is an artifact a structured JSON blob, a prose block, or both?
3. What is the relationship between an artifact and a phase_output? (Proposal: an artifact is a **derived, typed, indexable view** of one or more phase_outputs — not a replacement)
4. How does invalidation cascade? (Proposal: artifact has a `depends_on` list of upstream artifact IDs; when an upstream changes, downstream artifacts are marked stale)

### Stage 1: Artifact Table + Store (1 session)

Add to `src/executor/db.py`:

```sql
CREATE TABLE IF NOT EXISTS analytical_artifacts (
    artifact_id    VARCHAR(100) PRIMARY KEY,
    artifact_type  VARCHAR(100) NOT NULL,  -- 'aoi_themes', 'aoi_findings', 'target_profile', etc.
    job_id         VARCHAR(100) NOT NULL,  -- provenance (which job created this)
    document_fingerprint VARCHAR(64),      -- content-addressable document identity
    engine_key     VARCHAR(100),
    version        INTEGER DEFAULT 1,
    content        JSONB NOT NULL,         -- the normalized structured data
    prose_source_id VARCHAR(100),          -- FK to phase_outputs.id (original prose)
    depends_on     JSONB DEFAULT '[]',     -- upstream artifact IDs
    content_hash   VARCHAR(64) NOT NULL,   -- for staleness detection
    stale          BOOLEAN DEFAULT FALSE,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_artifacts_type_doc ON analytical_artifacts(artifact_type, document_fingerprint);
CREATE INDEX idx_artifacts_job ON analytical_artifacts(job_id);
```

Create `src/artifacts/store.py` with:
- `save_artifact(artifact_type, content, job_id, engine_key, document_fingerprint, depends_on) -> artifact_id`
- `load_artifact(artifact_type, document_fingerprint, engine_key) -> artifact | None`
- `load_artifacts_for_job(job_id) -> list[artifact]`
- `invalidate_downstream(artifact_id) -> int` (cascade stale flag)

### Stage 2: AOI Pilot — Extract contract.py into artifact store (2-3 sessions)

Refactor `src/aoi/contract.py` to:
1. After normalizing output, call `save_artifact(artifact_type="aoi_themes", content=normalized, ...)` instead of (or in addition to) storing in metadata JSONB
2. When `_load_previous_normalized()` is called, first check artifact store, then fall back to metadata
3. Make `structured_payloads` (by_theme, by_sin_type) also first-class artifacts

Hot path changes:
- `src/executor/chain_runner.py` — after saving output, check if artifact normalization applies
- `src/aoi/contract.py` — refactor `build_aoi_output_metadata()` to also persist artifacts

### Stage 3: Prove cross-job AOI artifact reuse (1 session)

Add an API endpoint:
```
GET /v1/artifacts?type=aoi_themes&document_fingerprint=XXX
```

Run two AOI jobs with the same source thinker documents. Demonstrate that the second job can discover and optionally reuse the first job's thematic synthesis artifact.

### Stage 4: Genealogy artifact pilot (2-3 sessions)

Pick ONE genealogy intermediate — likely `target_profile` from Phase 1.0's genealogy_target_profiling chain — and:
1. Design a normalization contract (similar to AOI's contract.py but for prose-derived structured data)
2. Persist as an artifact after Phase 1.0 completes
3. Demonstrate that a new job for the same target work can skip Phase 1.0 if a valid target_profile artifact exists

### Stage 5: Consumer-neutral delivery (2-3 sessions)

- Remove hardcoded `consumer_key="the-critic"` from auto-presentation
- Make `target_app` in view definitions a recommendation, not a constraint
- Extract a thin SDK/client contract from The Critic's API interaction patterns

### Stage 6: analyzer-mgmt artifact browsing (1-2 sessions)

Add artifact browsing to analyzer-mgmt:
- List artifacts by type
- Inspect artifact content
- View artifact provenance (which job, which engine, which document)
- Mark artifacts as stale

---

## 6. Concrete Deliverables

| Deliverable | Stage | Files Touched | New Files |
|-------------|-------|--------------|-----------|
| Artifact schema design doc | 0 | None | `communications/ARTIFACT_SCHEMA_DESIGN.md` |
| `analytical_artifacts` table | 1 | `src/executor/db.py` | `src/artifacts/store.py`, `src/artifacts/schemas.py` |
| Artifact API routes | 1 | `src/api/main.py` | `src/api/routes/artifacts.py` |
| AOI contract → artifact store | 2 | `src/aoi/contract.py`, `src/executor/chain_runner.py` | None |
| Cross-job artifact lookup | 3 | `src/artifacts/store.py` | None |
| Genealogy target_profile normalization | 4 | `src/executor/chain_runner.py` | `src/genealogy/contract.py` |
| Consumer-neutral auto-presentation | 5 | `src/executor/workflow_runner.py`, `src/presenter/presentation_bridge.py`, `src/views/definitions/*.json` | None |
| Client SDK (extract from The Critic) | 5 | `the-critic/analyzer/concept_analyzer/analyzer_v2_client.py` | `src/sdk/client.py` (polling, resume, version sync) |
| analyzer-mgmt artifact browser | 6 | analyzer-mgmt frontend + mgmt-api | New routes + pages |

---

## 7. Risks

### 7.1 Building the artifact layer too generally too early

**Risk**: Designing an abstract artifact system that handles "any analytical product" before having two concrete pilot implementations. This leads to over-engineering and premature abstraction.

**Mitigation**: Start with AOI's concrete normalization patterns. Let the artifact schema be shaped by what AOI actually produces. Only generalize after the genealogy pilot confirms or challenges the schema.

### 7.2 Breaking live AOI execution by refactoring contract.py

**Risk**: `contract.py` is called from `chain_runner.py` in the executor hot path. Refactoring it to use a new artifact store could break live AOI jobs.

**Mitigation**: Add artifact persistence alongside metadata storage (dual-write), not as a replacement. The metadata path remains the fallback. Only remove it after the artifact path is proven in production.

### 7.3 Artifact invalidation cascade complexity

**Risk**: Cascade invalidation (theme changes → engagement stale → findings stale → report stale) is hard to get right, especially with concurrent jobs.

**Mitigation**: Start with manual invalidation (mark stale, don't auto-delete). Add cascade only after the identity model is stable. For v1, a stale flag is enough.

### 7.4 Cross-job artifact reuse creating incorrect analysis

**Risk**: Reusing a "target profile" artifact from a previous job might skip important profiling that depends on different prior works or different analysis objectives.

**Mitigation**: Artifact identity must include enough context to distinguish meaningfully different analyses. The `document_fingerprint` alone is not enough — the artifact key should also include the analysis objective and relevant configuration parameters.

### 7.5 Genealogy prose outputs may resist artifact treatment

**Risk**: Genealogy outputs are rich prose, not structured JSON. Forcing them into artifact schemas may lose the nuance that makes them valuable, or require expensive re-extraction.

**Mitigation**: Accept that genealogy artifacts may be "annotated prose" (prose + metadata headers + cross-references) rather than "structured JSON." Design the artifact schema to support both shapes from the start.

### 7.6 Premature consumer-neutral delivery

**Risk**: Extracting a consumer-neutral SDK before having a second consumer to test it against risks building to an imagined contract.

**Mitigation**: Keep Stage 5 narrow: remove hardcoded `the-critic` references and make consumer_key configurable. Don't build a full SDK until there's a second consumer to validate it.

---

## 8. Open Questions

1. **Artifact identity granularity**: Should artifacts be per-engine (AOI model) or per-chain (genealogy model)? The AOI contract normalizes per-engine; genealogy chains produce a single output from 4 engines. These are different granularities.

2. **Document identity**: `executor_documents` stores document text with a `doc_id`, but there's no content-addressable fingerprinting. If the same book is uploaded twice, it gets two `doc_id` values. Should artifact identity be tied to document content hash rather than document ID?

3. **Artifact versioning semantics**: If a new engine version produces a different analysis of the same document, is that a new artifact or a new version of the same artifact? The `content_hash` column can detect changes, but the identity model needs a clear versioning policy.

4. **The `shares_with` / `consumes_from` bridge**: Capability definitions already declare what engines share and consume. Should the artifact store enforce these contracts at runtime (rejecting artifacts that don't match the declared schema), or should it be permissive?

5. **Project-level vs global artifact scope**: Should artifacts be scoped to a project (like jobs are), or should they be global? Project scoping prevents accidental cross-project contamination but limits reuse. Global scope maximizes reuse but requires careful identity management.

6. **What exactly moves from The Critic?**: The addendum says "too much platform behavior still lives in The Critic" but doesn't enumerate it. Before Stage 5, someone needs to audit The Critic's codebase and produce a specific list of responsibilities to extract. The AOI view definitions' `target_app: "the-critic"` is one signal, but the full inventory of consumer-side platform logic is unknown without that audit.

7. **Does the artifact layer change the planner?**: If the planner knows that a valid `target_profile` artifact already exists for a document, should it skip Phase 1.0? This is a significant change to the adaptive planner's prompt and the plan schema. It should be designed but deferred to after Stage 3 proves cross-job reuse.

8. **What is the right persistence backend?**: Artifacts are structured JSON. They could live in the same Postgres database as phase_outputs, or they could be a separate store (e.g., object storage for large artifacts, DB for metadata). For the pilot stages, the same database is sufficient — but the schema should be designed to support migration later.

---

## Summary Judgment

The addendum is **directionally correct and the right basis for the next refactoring program**, with three caveats:

1. **It underspecifies the artifact schema.** The program needs a Stage 0 design phase before coding begins.
2. **It doesn't address the prose vs structured divide.** Genealogy artifacts are fundamentally different from AOI artifacts. The program needs to handle both shapes.
3. **It's vague about The Critic's remaining responsibilities.** Stage 4 (consumer-neutral delivery) needs a specific inventory of what moves, not a general aspiration.

The minimal corrected program above (Stages 0-6) is the smallest credible implementation that follows the addendum's direction while addressing these gaps. It can be executed in approximately 10-15 focused sessions.
