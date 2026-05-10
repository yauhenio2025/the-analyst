# REPORT: Stage 0 — Analysis-Product Schema Design

Date: 2026-03-16
Designer: Claude Opus 4.6 (1M context)
Scope: analyzer-v2 only as primary system; The Critic and analyzer-mgmt as constraints/consumers

---

## 1. Design Verdict

The analysis-product layer requires **three new tables** and **zero changes** to the existing execution hot path for Stage 1. The design is additive — it sits on top of `phase_outputs`, `executor_documents`, and `executor_jobs` without modifying their schemas or query patterns.

The three core identifiers are:

1. **Corpus Reference** (`corpus_ref`) — content-addressed identity for a set of documents under analysis
2. **Analytical Artifact** (`artifact`) — a typed, normalized, addressable analytical product derived from one or more phase outputs
3. **Analysis Product** (`analysis_product`) — a named result envelope that groups artifacts, links to a corpus, and provides the consumer-neutral retrieval contract

These three identifiers solve the three scoping walls identified in the prior audit: job-scoped (artifacts break free), workflow-scoped (products are workflow-neutral), consumer-scoped (products are consumer-neutral).

---

## 2. Existing Code Constraints

### 2.1 Tables that MUST NOT be modified (they work)

| Table | Why leave it | What it provides to the product layer |
|-------|-------------|--------------------------------------|
| `phase_outputs` | Live execution hot path. Every `save_output()` call goes here. | **Provenance source** — artifacts point back to specific phase_output rows |
| `executor_jobs` | Job lifecycle is stable. 10+ callers depend on its schema. | **Execution provenance** — products point to the job that produced them |
| `executor_documents` | Document storage works. 200-500K char texts live here. | **Raw corpus content** — corpus references point to document sets |
| `presentation_cache` | Transformation cache works within jobs. | **Stays as-is** — a per-job optimization distinct from cross-job artifacts |
| `presentation_artifacts` | Rendering cache for scaffolds/polish. Job-scoped by design. | **Stays as-is** — presentation layer, not product layer |

### 2.2 Schemas that seed the product model

**`phase_outputs.metadata` JSONB** (`src/aoi/contract.py:91-100`):
AOI already stores normalized structured data in metadata:
```json
{
  "contract_family": "aoi_thematic_single_thinker",
  "contract_version": 1,
  "workflow_key": "anxiety_of_influence_thematic_single_thinker",
  "engine_key": "aoi_thematic_synthesis",
  "selected_source_thinker": {"thinker_id": "...", "thinker_name": "..."},
  "normalized": { /* themes, source_documents, etc. */ },
  "structured_payloads": { /* aoi_source_documents, aoi_by_theme, etc. */ }
}
```
This IS the artifact content — just trapped in a JSONB column keyed only by `job_id`.

**Capability `shares_with` / `consumes_from`** (`src/engines/schemas_v2.py:132-139`):
Already declares the artifact dependency graph per engine:
```yaml
# aoi_thematic_synthesis
shares_with:
  themes: "Stable theme inventory with theme names and claims"
  source_documents: "Explicit list of source documents"
consumes_from: {}

# aoi_engagement_mapping
shares_with:
  engagements: "Theme-keyed engagement objects"
consumes_from:
  themes: "Requires the source thinker's thematic synthesis"

# aoi_sin_findings
shares_with:
  findings: "Flat AOI findings keyed by theme and sin type"
consumes_from:
  themes: "Requires the upstream theme inventory"
  engagements: "Requires the upstream engagement map"
```
These become the artifact type declarations. No new metadata invention required.

**`WorkflowExecutionPlan`** (`src/orchestrator/schemas.py:428-462`):
Plans already carry thinker identity, target work, prior works, workflow key, objective key. The product layer inherits these as its context.

**`executor_documents`** (`src/executor/db.py:359-367`):
Documents already have `doc_id`, `title`, `author`, `role`, `char_count`. But no content fingerprint — same book uploaded twice gets two `doc_id` values.

### 2.3 Code paths that constrain the design

**`build_aoi_output_metadata()`** (`src/aoi/contract.py:33-100`) — Called from `chain_runner.py:406` and `chain_runner.py:520`. This is where artifact extraction happens today. The product layer hooks in HERE, after the existing metadata save, to also persist a first-class artifact.

**`_load_previous_normalized()`** (`src/aoi/contract.py:132-146`) — Loads the prior engine's normalized output from `phase_outputs.metadata` using `job_id` + `engine_key`. This is the cross-artifact dependency read path. In the product layer, this should first check the artifact store, then fall back to metadata.

**`assemble_phase_context()`** (`src/executor/context_broker.py:24-105`) — Assembles prose context from upstream phases within a job. The product layer does NOT replace this — it runs alongside it for the structured artifact path.

**`PagePresentation`** (`src/presenter/schemas.py:256-294`) — The consumer-facing page payload. The product layer's result manifest lives ABOVE this — it's metadata about what exists, whether it's stale, and where to fetch it. The PagePresentation remains the render-ready payload.

---

## 3. Proposed Core Identifiers

### 3.1 Corpus Reference

**What it answers**: "What exact set of documents does this analysis refer to?"

**Identity model**: Content-addressed hash of the document set.

```
corpus_ref_id = sha256(
    sorted([
        sha256(doc_text) for doc in documents
    ]) + workflow_key + objective_key
)
```

**Why include workflow_key and objective_key**: The same documents analyzed under different objectives produce different analysis products. A genealogical analysis of Varoufakis and an AOI analysis of Varoufakis-vs-Marx are different corpus references even if the documents overlap.

**What it points to**:
- An ordered set of `(doc_id, role, title, content_hash)` tuples
- The `thinker_name` and `target_work` metadata from the plan
- For AOI: `selected_source_thinker_id` and `selected_source_thinker_name`

**What it does NOT own**: The document text itself. That stays in `executor_documents`.

### 3.2 Analytical Artifact

**What it answers**: "What typed analytical product was produced, from what input, by what engine?"

**Identity model**: `(artifact_type, corpus_ref_id, engine_key, work_key?)` — unique per type+corpus+engine.

An artifact_type maps directly to the `shares_with` keys from capability definitions:
- `aoi:themes` — from `aoi_thematic_synthesis.shares_with.themes`
- `aoi:source_documents` — from `aoi_thematic_synthesis.shares_with.source_documents`
- `aoi:engagements` — from `aoi_engagement_mapping.shares_with.engagements`
- `aoi:findings` — from `aoi_sin_findings.shares_with.findings`
- `aoi:report` — from `aoi_thematic_report.shares_with.report`
- `genealogy:target_profile` — (future) from target profiling chain
- `genealogy:relationship_classification` — (future) per-work, from Phase 1.5

**Payload**: Structured JSON. For AOI, this is the `normalized` dict from `contract.py`. For genealogy (future), this would be a new normalization contract.

**Provenance**: Points back to the specific `phase_output.id` row and `job_id` that produced it.

### 3.3 Analysis Product

**What it answers**: "What complete analysis result exists for this corpus, and what is its status?"

**Identity model**: `(corpus_ref_id)` — one product per corpus reference. A new job for the same corpus updates the product, not creates a new one.

**What it contains**:
- Links to all artifacts produced for this corpus
- Status: `complete`, `partial`, `stale`, `superseded`
- The `job_id` of the latest producing job
- A lightweight result manifest (list of artifact types available, staleness flags)
- Consumer-neutral metadata: `thinker_name`, `workflow_key`, `objective_key`

---

## 4. Proposed Tables / Records

### 4.1 `corpus_refs` — Corpus identity

```sql
CREATE TABLE IF NOT EXISTS corpus_refs (
    corpus_ref_id   VARCHAR(64) PRIMARY KEY,   -- sha256 fingerprint
    workflow_key    VARCHAR(100) NOT NULL,
    objective_key   VARCHAR(100) DEFAULT '',
    thinker_name    VARCHAR(500) NOT NULL,
    target_work_title VARCHAR(500) NOT NULL,
    target_work_hash VARCHAR(64) NOT NULL,      -- sha256 of target document text
    document_set    JSONB NOT NULL,             -- [{doc_id, role, title, content_hash}]
    -- AOI-specific (nullable for non-AOI)
    source_thinker_id   VARCHAR(200),
    source_thinker_name VARCHAR(500),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

**Why a separate table** (not a column on `executor_jobs`):
- Multiple jobs can reference the same corpus. The corpus reference must outlive any single job.
- Consumers need to look up "does an analysis exist for these documents?" without knowing a job_id.

**How it gets populated**: When `pipeline.py:run_analysis_pipeline()` uploads documents and creates a job, it also computes and persists the corpus_ref. This is a one-line addition to the pipeline, not a refactor.

### 4.2 `analytical_artifacts` — First-class analytical products

```sql
CREATE TABLE IF NOT EXISTS analytical_artifacts (
    artifact_id         VARCHAR(100) PRIMARY KEY,    -- art-{uuid12}
    artifact_type       VARCHAR(100) NOT NULL,       -- 'aoi:themes', 'aoi:findings', etc.
    corpus_ref_id       VARCHAR(64) NOT NULL REFERENCES corpus_refs(corpus_ref_id),
    engine_key          VARCHAR(100) NOT NULL,
    work_key            VARCHAR(200) DEFAULT '',      -- for per-work artifacts (genealogy Phase 2.0)
    -- Content
    content             JSONB NOT NULL,               -- the normalized structured data
    content_hash        VARCHAR(64) NOT NULL,          -- sha256 of content for staleness
    payload_shape       VARCHAR(20) NOT NULL DEFAULT 'structured',  -- 'structured' or 'prose_derived'
    -- Provenance
    producing_job_id    VARCHAR(100) NOT NULL REFERENCES executor_jobs(job_id),
    source_output_id    VARCHAR(100),                  -- FK to phase_outputs.id (nullable for composite)
    phase_number        FLOAT,
    contract_family     VARCHAR(100) DEFAULT '',        -- 'aoi_thematic_single_thinker', etc.
    contract_version    INTEGER DEFAULT 1,
    model_used          VARCHAR(100) DEFAULT '',
    -- Dependency
    depends_on          JSONB DEFAULT '[]',            -- list of artifact_ids this was derived from
    stale               BOOLEAN DEFAULT FALSE,
    stale_reason        VARCHAR(200) DEFAULT '',
    -- Timestamps
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    superseded_at       TIMESTAMPTZ                    -- set when a newer version replaces this
);

CREATE INDEX IF NOT EXISTS idx_artifacts_type_corpus
    ON analytical_artifacts(artifact_type, corpus_ref_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_corpus
    ON analytical_artifacts(corpus_ref_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_job
    ON analytical_artifacts(producing_job_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_artifacts_natural_key
    ON analytical_artifacts(artifact_type, corpus_ref_id, engine_key, work_key)
    WHERE superseded_at IS NULL;
```

**The natural key** is `(artifact_type, corpus_ref_id, engine_key, work_key)` with a partial unique index on non-superseded rows. This means:
- Only one active `aoi:themes` artifact per corpus reference
- Re-running the AOI workflow supersedes the old artifact, not duplicates it
- Old artifacts are preserved for audit (with `superseded_at` set)

**`depends_on`**: Stores the artifact_ids of upstream artifacts. For AOI:
- `aoi:themes` depends on: `[]` (root)
- `aoi:engagements` depends on: `[art-id-of-themes]`
- `aoi:findings` depends on: `[art-id-of-themes, art-id-of-engagements]`
- `aoi:report` depends on: `[art-id-of-themes, art-id-of-engagements, art-id-of-findings]`

This mirrors exactly the `consumes_from` declarations in capability definitions.

### 4.3 `analysis_products` — Result envelope

```sql
CREATE TABLE IF NOT EXISTS analysis_products (
    product_id      VARCHAR(100) PRIMARY KEY,     -- prod-{uuid12}
    corpus_ref_id   VARCHAR(64) NOT NULL UNIQUE REFERENCES corpus_refs(corpus_ref_id),
    -- Identity
    workflow_key    VARCHAR(100) NOT NULL,
    objective_key   VARCHAR(100) DEFAULT '',
    thinker_name    VARCHAR(500) NOT NULL,
    target_work_title VARCHAR(500) NOT NULL,
    -- Status
    status          VARCHAR(20) NOT NULL DEFAULT 'partial', -- partial, complete, stale
    -- Latest execution
    latest_job_id   VARCHAR(100) REFERENCES executor_jobs(job_id),
    latest_plan_id  VARCHAR(100),
    -- Manifest (lightweight summary of what's available)
    artifact_manifest JSONB DEFAULT '{}',         -- {artifact_type: {artifact_id, stale, created_at}}
    -- Consumer retrieval
    page_presentation_ready BOOLEAN DEFAULT FALSE,
    presentation_hash VARCHAR(64) DEFAULT '',      -- hash of last PagePresentation
    -- Timestamps
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    completed_at    TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_products_thinker
    ON analysis_products(thinker_name);
CREATE INDEX IF NOT EXISTS idx_products_workflow
    ON analysis_products(workflow_key);
CREATE INDEX IF NOT EXISTS idx_products_status
    ON analysis_products(status);
```

**`artifact_manifest`** is the consumer-facing "what exists" summary:
```json
{
  "aoi:themes": {
    "artifact_id": "art-a1b2c3d4e5f6",
    "stale": false,
    "created_at": "2026-03-16T15:00:00Z"
  },
  "aoi:engagements": {
    "artifact_id": "art-b2c3d4e5f6a7",
    "stale": false,
    "created_at": "2026-03-16T15:05:00Z"
  },
  "aoi:findings": null,
  "aoi:report": null
}
```

A `null` value means that artifact type has not been produced yet. `stale: true` means upstream dependencies changed.

---

## 5. Proposed Result Manifest Contract

### 5.1 Consumer retrieval — the API contract

The Critic currently does:
1. `POST /v1/orchestrator/analyze` → get `job_id`
2. `GET /v1/executor/jobs/{job_id}` → poll status
3. `GET /v1/presenter/page/{job_id}` → get PagePresentation
4. Save snapshot to local `genealogy_analyses` table

The product layer adds a consumer-neutral alternative:

```
GET /v1/products?thinker_name=X&workflow_key=Y
  → list of analysis_products matching the query

GET /v1/products/{product_id}
  → product metadata + artifact_manifest

GET /v1/products/{product_id}/artifacts
  → list of all artifacts for this product

GET /v1/products/{product_id}/artifacts/{artifact_type}
  → specific artifact content (e.g., aoi:themes)

GET /v1/products/{product_id}/presentation
  → PagePresentation (same as current presenter, but keyed by product not job)

GET /v1/products/{product_id}/status
  → {status, stale_artifacts: [...], last_updated, latest_job_id}
```

### 5.2 Refresh contract

When a consumer detects staleness (or the user requests refresh):

```
POST /v1/products/{product_id}/refresh
  → creates a new job targeting the same corpus_ref
  → the new job's artifacts supersede old ones on completion
  → returns {job_id, expected_phases}
```

The consumer does NOT need to re-upload documents or re-specify the thinker. The corpus reference carries all of that.

### 5.3 What The Critic can stop doing

Once this contract exists, The Critic can replace:
- `_save_v2_presentation_to_db()` → stop persisting local snapshots; query the product API instead
- `_V2_JOB_MAPPINGS` → stop maintaining its own job mapping; the product_id is the stable handle
- `poll_analysis_sync()` → still poll by job_id, but use product_id for result retrieval
- `fetch_page_presentation_sync()` → use `GET /v1/products/{product_id}/presentation`

### 5.4 What The Critic KEEPS doing

- UX for selecting thinker/works/documents (consumer-specific)
- Displaying the PagePresentation (consumer-specific rendering)
- Authentication and user sessions (consumer-specific)
- Editorial workflows (consumer-specific)

---

## 6. Staleness / Invalidation Model

### 6.1 Design principle: stale flags, not cascade deletes

When an upstream artifact changes, downstream artifacts are marked `stale = TRUE` but not deleted. The consumer sees the stale flag in the artifact manifest and can decide whether to refresh.

### 6.2 When staleness propagates

Staleness triggers when:
1. A new job completes and produces a new version of an artifact (the old artifact gets `superseded_at` set)
2. The new artifact's `content_hash` differs from the old artifact's `content_hash`
3. All artifacts whose `depends_on` list includes the superseded artifact_id get `stale = TRUE`

### 6.3 Staleness propagation function

```python
def mark_downstream_stale(superseded_artifact_id: str) -> int:
    """Mark all artifacts that depend on a superseded artifact as stale."""
    count = execute_write(
        """UPDATE analytical_artifacts
           SET stale = TRUE, stale_reason = 'upstream_superseded'
           WHERE superseded_at IS NULL
             AND depends_on::jsonb @> %s::jsonb""",
        (json.dumps([superseded_artifact_id]),),
    )
    return count
```

### 6.4 When staleness does NOT propagate

- If the new artifact has the same `content_hash` as the old one (content-identical re-run), downstream artifacts are NOT marked stale. This prevents unnecessary recomputation after deterministic re-runs.

### 6.5 What this does NOT do (yet)

- No automatic re-execution of stale artifacts. The consumer must explicitly call `/refresh`.
- No expiration-based staleness. Only dependency-based.
- No partial refresh (re-running just one phase). That's a Stage 3+ concern.

---

## 7. AOI Pilot Fit

### 7.1 What gets promoted to artifacts

| Current location | Artifact type | Content | Source engine |
|-----------------|--------------|---------|--------------|
| `metadata.normalized` in Phase 1.0 output | `aoi:themes` | `{themes: [...], source_documents: [...], overall_synthesis: "..."}` | `aoi_thematic_synthesis` |
| `metadata.structured_payloads.aoi_source_documents` | `aoi:source_documents` | `[{source_document_id, title, subtitle, description, badge}]` | `aoi_thematic_synthesis` |
| `metadata.normalized` in Phase 2.0 output | `aoi:engagements` | `{engagements: [...], engagement_pattern: "...", themes_engaged: N, ...}` | `aoi_engagement_mapping` |
| `metadata.normalized` in Phase 3.0 output | `aoi:findings` | `{findings: [...], findings_by_theme: {...}, findings_by_sin_type: {...}}` | `aoi_sin_findings` |
| `metadata.structured_payloads.aoi_by_theme` | `aoi:by_theme_payload` | Pre-built presentation payload | `aoi_sin_findings` |
| `metadata.structured_payloads.aoi_by_sin_type` | `aoi:by_sin_type_payload` | Pre-built presentation payload | `aoi_sin_findings` |
| `metadata.normalized.report_sections` in Phase 4.0 | `aoi:report` | `{summary, engagement_pattern, key_divergences, sin_distribution, reading_implications}` | `aoi_thematic_report` |

### 7.2 Hot path integration point

In `src/executor/chain_runner.py`, after `build_aoi_output_metadata()` returns and the result is saved to `phase_outputs.metadata`, add a call to the artifact store:

```python
# chain_runner.py line ~412 (after existing metadata save)
output_metadata = build_aoi_output_metadata(...)
# ... existing save_output() call with metadata ...

# NEW: promote to artifact store
if output_metadata and output_metadata.get("normalized"):
    from src.artifacts.store import save_artifact_from_aoi_metadata
    save_artifact_from_aoi_metadata(
        job_id=job_id,
        corpus_ref_id=corpus_ref_id,   # passed down from workflow_runner
        engine_key=cap_def.engine_key,
        output_id=output_id,           # from save_output() return value
        phase_number=phase_number,
        metadata=output_metadata,
    )
```

This is **dual-write**: both the existing metadata path and the new artifact path get written. The metadata path remains the fallback; the artifact path enables cross-job lookup.

### 7.3 Dependency wiring

The `depends_on` list for each AOI artifact is computed from the capability definition's `consumes_from`:

```python
def compute_aoi_depends_on(engine_key: str, corpus_ref_id: str) -> list[str]:
    """Look up active artifacts this engine consumes from."""
    cap_def = get_capability_definition(engine_key)
    depends_on = []
    for consumed_key in cap_def.composability.consumes_from:
        # Map consumed dimension → artifact type
        artifact_type = f"aoi:{consumed_key}"  # e.g., "themes" → "aoi:themes"
        upstream = load_active_artifact(artifact_type, corpus_ref_id)
        if upstream:
            depends_on.append(upstream.artifact_id)
    return depends_on
```

### 7.4 What `_load_previous_normalized()` becomes

Currently:
```python
def _load_previous_normalized(job_id, engine_key):
    outputs = load_phase_outputs(job_id=job_id, engine_key=engine_key)
    # ... extract from metadata
```

With artifact store (preferred path, fallback to existing):
```python
def _load_previous_normalized(job_id, engine_key, corpus_ref_id=None):
    # Try artifact store first (cross-job capable)
    if corpus_ref_id:
        artifact_type = _engine_to_artifact_type(engine_key)
        artifact = load_active_artifact(artifact_type, corpus_ref_id)
        if artifact:
            return artifact.content

    # Fall back to job-scoped metadata (existing behavior)
    outputs = load_phase_outputs(job_id=job_id, engine_key=engine_key)
    # ... existing logic
```

---

## 8. Genealogy Pilot Fit

### 8.1 The target profile seam

The strongest genealogy pilot candidate is the Phase 1.0 **target work profile** — the distilled analysis produced by the `genealogy_target_profiling` chain (4 engines: `conceptual_framework_extraction` → `concept_semantic_constellation` → `inferential_commitment_mapper` → `concept_evolution`).

**Why this seam**:
- It's the largest single LLM cost in a genealogy run (~35 min with Opus on 183K token input)
- Its output is reused by Phase 1.5, 2.0, and 3.0
- Same target work + same chain = same profile (deterministic given same documents)
- Skipping Phase 1.0 on re-run saves ~40% of total execution cost

### 8.2 What the artifact looks like

Unlike AOI's structured JSON, the target profile is **concatenated prose** from 4 engine outputs. The artifact would be:

```json
{
  "artifact_type": "genealogy:target_profile",
  "payload_shape": "prose_derived",
  "content": {
    "prose": "... 50-150K chars of concatenated profiling ...",
    "engine_outputs": {
      "conceptual_framework_extraction": "output_id_1",
      "concept_semantic_constellation": "output_id_2",
      "inferential_commitment_mapper": "output_id_3",
      "concept_evolution": "output_id_4"
    },
    "total_chars": 120000
  }
}
```

The `prose_derived` payload_shape tells consumers this is not structured JSON but rich prose with metadata headers. The `engine_outputs` map provides provenance back to individual phase_output rows.

### 8.3 Why this proves a different artifact shape

AOI artifacts are structured JSON with typed fields and stable IDs. The genealogy target profile is prose-rich analysis with implicit structure. Supporting both in the same `analytical_artifacts` table (via the `payload_shape` discriminator and flexible JSONB `content` column) proves the schema handles both shapes.

### 8.4 Reuse mechanism

When `workflow_runner.execute_plan()` reaches Phase 1.0, it can check:

```python
existing_profile = load_active_artifact("genealogy:target_profile", corpus_ref_id)
if existing_profile and not existing_profile.stale:
    logger.info(f"Reusing target profile artifact {existing_profile.artifact_id}")
    # Inject into context broker as if Phase 1.0 completed
    # Skip to Phase 1.5
```

This is optional reuse — the job still works without it. But when the artifact exists and is fresh, Phase 1.0 is skipped entirely.

---

## 9. Risks / Open Decisions

### 9.1 RISK: Corpus fingerprint instability

If a user re-uploads the same book with minor whitespace differences, the `content_hash` changes and a new `corpus_ref` is created. This prevents artifact reuse for what is semantically the same document.

**Mitigation**: Normalize document text before hashing (strip leading/trailing whitespace, normalize Unicode, collapse multiple newlines). This makes the hash more stable without losing meaningful content differences.

**Open decision**: How aggressive should normalization be? Too aggressive and different editions hash the same. Too conservative and minor formatting changes break reuse.

### 9.2 RISK: AOI dual-write adds latency to execution

Writing to both `phase_outputs.metadata` and `analytical_artifacts` on every engine completion adds ~2-10ms per write (Postgres INSERT). For a 4-phase AOI workflow with 4 engine completions, this is ~8-40ms total — negligible against the 10-35 min per engine call.

**Verdict**: Not a real risk. Proceed with dual-write.

### 9.3 RISK: `depends_on` becomes a maintenance burden

If the capability definitions change their `consumes_from` declarations, existing artifact dependency chains become inconsistent.

**Mitigation**: `depends_on` is a snapshot at artifact creation time. It doesn't need to stay in sync with changing capability definitions. The dependency graph is frozen when the artifact is created.

### 9.4 OPEN DECISION: Should `corpus_ref_id` include the `objective_key`?

**Argument for**: A genealogical analysis and an AOI analysis of the same documents are different products. Including `objective_key` in the corpus fingerprint ensures they get separate artifact namespaces.

**Argument against**: Some artifacts (e.g., a deep text profiling of the target work) are objective-neutral. Including `objective_key` prevents reuse of a text profile across genealogy and AOI.

**Proposed resolution**: Include `objective_key` in the corpus_ref fingerprint for now. Objective-neutral artifacts (like deep_text_profiling) can be stored with `objective_key = ''` and shared. This trades a small amount of potential reuse for clean separation. Revisit after both pilots.

### 9.5 OPEN DECISION: Should the product layer own PagePresentation generation?

Currently, `PagePresentation` is assembled on-the-fly by `presentation_api.py` from `phase_outputs` + `presentation_cache`. The product layer could cache a serialized PagePresentation on the `analysis_products` row.

**Proposed resolution**: NOT yet. Keep PagePresentation assembly in the presenter. The product layer provides the artifact manifest and status; the presenter assembles the page from artifacts + views + transformations. Merging them would over-couple the layers.

### 9.6 OPEN DECISION: Per-engine vs per-phase artifact granularity

AOI produces one artifact per engine (per phase). Genealogy chains produce one concatenated output per phase from multiple engines. Should a chain's output be one artifact or N artifacts (one per engine)?

**Proposed resolution**: One artifact per engine for AOI (each engine has its own `shares_with`). One artifact per chain output for genealogy Phase 1.0 (the target profile is the unit of reuse, not individual engine outputs within it). The `artifact_type` namespace distinguishes: `aoi:themes` (per-engine) vs `genealogy:target_profile` (per-chain).

### 9.7 OPEN DECISION: Artifact type namespace convention

Proposed convention: `{domain}:{artifact_name}` where domain is derived from the workflow/objective family.

- AOI: `aoi:themes`, `aoi:engagements`, `aoi:findings`, `aoi:report`, `aoi:source_documents`
- Genealogy: `genealogy:target_profile`, `genealogy:relationship_classification`, `genealogy:synthesis`
- Shared: `profiling:deep_text_profile` (objective-neutral)

This is extensible without schema changes. New artifact types are just new string values.

---

## 10. Supplementary Evidence (from parallel audits)

### 10.1 The Critic's actual identity model

The Critic resolves "does this analysis exist?" using three keys (`the-critic/api/server.py:13950-13993`):
- `project_id` — which project owns this analysis
- `workflow_key` — which analysis type (`intellectual_genealogy`, `anxiety_of_influence_thematic_single_thinker`)
- `selected_source_thinker_id` — for AOI only, which source thinker

It stores the **entire** `PagePresentation` as a JSONB blob inside `genealogy_analyses.pass_results` (via `_build_v2_presentation_record()` at line 18220-18236):
```json
{
  "_output_mode": "v2_presentation",
  "_v2_job_id": "job-abc123",
  "_presentation": { /* full PagePresentation */ },
  "selected_source_thinker_id": "thinker_123",
  "selected_source_thinker_name": "John O'Neill"
}
```

**Design implication**: The `corpus_refs` table's identity model (`workflow_key + objective_key + document_set_hash`) captures the same identity that The Critic currently builds from `project_id + workflow_key + thinker_id`. The product layer replaces The Critic's consumer-side snapshot with a platform-side record.

**What The Critic also stores** (`the-critic/api/models_db.py:2359-2381`):
- `genealogy_analyses` table: `id, project_id, job_id, mode, pass_results, final_synthesis, ideas_analyzed, prior_works_scanned, tactics_detected, status, workflow_key`
- `genealogy_pass_cache` table: `(project_id, pass_num, suffix)` — incremental per-pass caching
- `analysis_outputs` table: prose outputs with `parent_id` lineage tracking

All of these are consumer-side persistence that the product layer replaces:
- `genealogy_analyses.pass_results` → `analysis_products.artifact_manifest` + `GET /v1/products/{id}/presentation`
- `genealogy_pass_cache` → `analytical_artifacts` (incremental artifact creation during execution)
- `analysis_outputs` → already exists in `phase_outputs` on the platform side

### 10.2 All 28 engines with artifact declarations

The `shares_with`/`consumes_from` metadata is far broader than just AOI. **28 engines** have explicit declarations across the entire engine catalog:

**AOI pipeline** (4 engines): themes → engagements → findings → report

**Genealogy target profiling** (3 engines):
- `conceptual_framework_extraction` shares: {conceptual_vocabulary, framework_architecture, ...}
- `concept_semantic_constellation` shares: {semantic_field_maps, ...}; consumes: {vocabulary_profile}
- `inferential_commitment_mapper` shares: {commitment_structures, ...}; consumes: {conceptual_vocabulary}

**Prior work analysis** (4 engines):
- `genealogy_relationship_classification` shares: {relationship_classification}; consumes: {target_work_profile}
- `concept_evolution` shares: {dimensional_comparisons, ...}; consumes: {target_work_profile, relationship_classification}
- `concept_appropriation_tracker` shares: {migration_evidence, ...}; consumes: {dimensional_comparisons}
- `concept_synthesis` shares: {evolution_timelines, ...}; consumes: {concept_evolution, concept_appropriation_tracker}

**Logic/argument** (6 engines), **epistemology** (3 engines), **structural** (5 engines), **synthesis** (3 engines) — all with similar declarations.

**Design implication**: The `artifact_type` namespace (`aoi:themes`, `genealogy:target_profile`, etc.) is not invented — it's derived from existing `shares_with` dimension keys. The 28-engine inventory provides the complete artifact type catalog when the system scales beyond the two pilot domains.

**Current limitation**: The dimension keys across engines are **string-keyed and not formally coordinated**. For example, `conceptual_framework_extraction` shares `conceptual_vocabulary` and `concept_semantic_constellation` consumes `vocabulary_profile` — these refer to the same dimension but use different names. Stage 1 should not attempt to unify these names; Stage 2+ can introduce a formal dimension registry if needed.

---

## 11. Recommended Stage 1 Start

### 11.1 Session 1: Schema + store (4 hours)

1. Add the three tables to `src/executor/db.py` (Postgres and SQLite DDL + migrations)
2. Create `src/artifacts/` package:
   - `schemas.py` — Pydantic models for CorpusRef, AnalyticalArtifact, AnalysisProduct
   - `store.py` — CRUD functions: `save_corpus_ref()`, `save_artifact()`, `load_active_artifact()`, `save_product()`, `update_product_manifest()`
   - `staleness.py` — `mark_downstream_stale()`, `check_artifact_freshness()`
3. Create `src/api/routes/products.py` — minimal endpoints: `GET /v1/products`, `GET /v1/products/{id}`, `GET /v1/products/{id}/artifacts`

### 11.2 Session 2: AOI artifact extraction (4 hours)

1. In `pipeline.py:run_analysis_pipeline()`, compute `corpus_ref_id` from uploaded documents and persist `corpus_refs` row
2. Thread `corpus_ref_id` through `execute_plan()` → `run_phase()` → `run_chain()` / `run_single_engine()`
3. In `chain_runner.py`, after `build_aoi_output_metadata()`, dual-write to `analytical_artifacts`
4. After job completion, update `analysis_products` row with artifact manifest

### 11.3 Session 3: Cross-job lookup proof (2 hours)

1. Run an AOI analysis → verify artifacts are created
2. Run the same AOI analysis again (same documents, same thinker)
3. Verify the second run can detect existing artifacts via `corpus_ref_id` match
4. Verify `_load_previous_normalized()` falls through to artifact store

### 11.4 What NOT to do in Stage 1

- Do not modify `phase_outputs` schema
- Do not modify `PagePresentation` assembly
- Do not modify The Critic's polling or retrieval patterns
- Do not implement automatic Phase skipping based on artifact reuse
- Do not implement the `/refresh` endpoint
- Do not implement genealogy artifacts

These are Stage 2+ concerns. Stage 1 proves the schema works and artifacts get created alongside existing execution.
