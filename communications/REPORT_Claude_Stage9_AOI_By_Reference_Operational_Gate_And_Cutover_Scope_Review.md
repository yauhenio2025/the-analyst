# Report: Stage 9 AOI By-Reference Operational Gate and Cutover Scope Review

Date: 2026-03-18
Reviewer: Claude Opus 4.6
Primary artifact reviewed: `MEMO_2026-03-18_stage9_direction_aoi_by_reference_operational_gate_and_cutover.md`

## 1. Findings

### Finding 1: Compounding operational debt is undersized in the memo

**Severity: HIGH**

**Problem**: The memo correctly identifies the remaining risk as operational rather than architectural. But it frames the unrun Stage 7 and Stage 8 live gates as though they were simple verification checks (section 9A lists seven conditions as a flat bullet list). In reality, the project has accumulated **two unapplied Critic database migrations**, **zero deployed by-ref workflow proof** across either genealogy or AOI, and **zero production evidence** of rollout provenance. That is not a checklist — it is the entire operational program from Stages 6-8 compressed into one gate.

**Why it matters**: If migration 031 (source_document_id backfill) fails or reveals data quality issues, Stage 9 cannot proceed to cutover at all. The memo does not acknowledge this risk explicitly. It says "if those conditions are not true, the next work is still operational stabilization rather than cutover" — but it treats that stabilization path as an exception case rather than a real probability that should shape the stage plan.

**Concrete basis**:
- Migration 030 (`api/alembic/versions/030_add_v2_run_reference_rollout_provenance.py`): Adds nullable columns to `v2_run_references`. Additive and safe, but still not applied.
- Migration 031 (`api/alembic/versions/031_add_source_document_id_to_influence_reference_texts.py`): Involves a Python-based backfill that derives slugs from filenames with collision suffixing. The Stage 8 completion memo notes "a regression test now proves that the migration backfill helper and runtime `_build_source_document_id()` agree on representative names" — but representative names are not all names. Production data may contain edge cases the test fixtures did not cover.
- The Stage 8 completion memo itself says "the Critic model still tolerates a null `source_document_id` at runtime" — meaning the code path works without the migration, but **corpus_ref parity depends on it**.

---

### Finding 2: The AOI proving smoke's data dependency is unaddressed

**Severity: HIGH**

**Problem**: The memo proposes a deployed AOI proving smoke (section 9B) without addressing the nontrivial data setup it requires. Unlike genealogy (where a project with uploaded documents is sufficient), AOI by-reference needs:

- A Critic project with subject/response documents uploaded
- At least one `InfluenceThinkerDB` record with `InfluenceReferenceTextDB` rows
- Those reference text rows need persisted `source_document_id` (i.e., migration 031 must have run)
- The Critic must successfully compose a synthetic target from project documents
- The selected thinker must have enough source texts for a meaningful corpus

That is a substantially more complex test fixture than the genealogy cutover smoke, which only needed a project with chapters.

**Why it matters**: If the AOI smoke cannot set up its own test data cleanly against the deployed system, it either depends on pre-existing production data (fragile, non-reproducible) or requires a setup script that is itself nontrivial Stage 9 scope the memo does not mention.

**Concrete basis**:
- Stage 7 genealogy cutover smoke (`test-stage7-genealogy-cutover-smoke.sh`) creates a run via the Critic's existing API and asserts `launch_mode` and `corpus_ref` backfill. It works because Critic already has genealogy project setup paths.
- AOI thematic launch requires `_build_aoi_registered_corpus_launch_payload()` in `api/server.py` (lines ~17779-17881), which calls `_load_aoi_target_documents()` and `_load_aoi_prior_works()`. These load from `ProjectDocumentDB` and `InfluenceReferenceTextDB` respectively. A smoke test either needs to populate both tables or rely on existing data.

---

### Finding 3: Parity proof methodology and runtime cost are unspecified

**Severity: MEDIUM**

**Problem**: The memo makes inline/by-ref `corpus_ref` parity the hard gate before the AOI default flip (section 9C). That is the right decision. But it does not specify:

1. How the parity proof is actually conducted: Same project? Same thinker? Same moment? Or recorded baseline vs. live comparison?
2. What counts as "the same semantic corpus_ref" — exact string equality? Or structural membership equality?
3. What the runtime cost of the proof is.

**Why it matters**: The AOI workflow has 4 engine phases. At current throughput (~0.5 tokens/sec for large inputs), a single AOI run can take 2+ hours. Proving parity requires **two complete runs** (one inline, one by-ref) with the same input data, plus time to compare. That is 4+ hours of deployed compute for one parity check, not counting setup time or retries. The memo should size this honestly so the stage plan allocates realistic time.

**Concrete basis**:
- The AOI corpus builder (`store.py` lines ~168-243) produces a deterministic fingerprint from qualifiers (`selected_source_thinker_id`, `selected_source_thinker_name`, `workflow_key`, `objective_key`) plus members sorted by `source_document_id` then title. If the same `source_document_id` values are used by both paths, the fingerprint should match — but only if the member sets agree exactly.
- The inline path builds the corpus from plan_data that receives source_document_id from `_load_aoi_prior_works()`, which now reads persisted values from `InfluenceReferenceTextDB.source_document_id`.
- The by-ref path builds the corpus from plan_data that receives source_document_id from `external_document_bindings.source_document_id`, which was synced from the Critic.
- If migration 031's backfill and the Critic's upload-time assignment produce different values for the same source text row, parity fails silently.

---

### Finding 4: The transition window between AOI opt-in and default is underspecified

**Severity: MEDIUM**

**Problem**: The memo proposes retiring `AOI_THEMATIC_V2_BY_REF` and adding `AOI_THEMATIC_V2_INLINE=1` as the explicit rollback control (section 9D). This mirrors the Stage 7 genealogy pattern. But it does not address the deployment window behavior.

During Stage 9 deployment:
- Old code recognizes `AOI_THEMATIC_V2_BY_REF=1` as an opt-in. If the env has this set, old code does by-ref.
- New code makes by-ref the default and ignores `AOI_THEMATIC_V2_BY_REF`. If the env still has this flag set, new code logs a deprecation warning (following the Stage 7 pattern).
- But if someone had `AOI_THEMATIC_V2_BY_REF=0` or absent (meaning "keep AOI inline"), deploying new code silently changes the behavior to by-ref.

This is expected behavior for a default flip. But the memo should state explicitly that any AOI runs started during the deployment window (between analyzer-v2 deploy and Critic deploy) will follow whatever the currently-deployed Critic code says. If Critic deploys before analyzer-v2, and the new Critic code immediately tries AOI by-ref, but analyzer-v2 hasn't been updated yet — does the by-ref request still work? Yes, because Stage 8 already added AOI support to analyzer-v2. So the deploy order is actually: either order works. But the memo should say so.

**Concrete basis**:
- Launch mode selection in `api/server.py` line ~442: `return "by_ref" if _is_aoi_thematic_v2_by_ref_enabled() else "inline"` — currently AOI defaults to inline.
- Stage 7 genealogy precedent in same file line ~445: `return "inline" if _is_genealogy_v2_inline_forced() else "by_ref"` — genealogy already flipped.
- analyzer-v2 `AnalyzeByRefRequest` already accepts AOI workflow_key (`pipeline_schemas.py` lines ~308-336). No analyzer-v2 code change is needed for the cutover.

---

### Finding 5: The recovery/resume proof gap is real but bounded

**Severity: MEDIUM**

**Problem**: The memo's proposed proving surface (section 9B) covers: inline launch, by-ref launch, selected thinker identity, provenance, completion, and semantic `corpus_ref` parity. It does not explicitly require proving AOI by-ref recovery (what happens if the background thread dies mid-execution and the job resumes from snapshot).

**Why it matters**: The Stage 8 completion memo explicitly states that AOI snapshot enrichment and recovery metadata preservation were part of the build. If Stage 9 doesn't prove recovery works in deployment, the by-ref default flip could create a class of "started but unrecoverable" AOI jobs.

**Concrete basis**:
- `by_ref.py` `_store_by_ref_snapshot()` (lines ~333-371) stores `prior_binding_metadata` with source_thinker_id/name/source_document_id.
- `_build_plan_inputs_from_snapshot()` (lines ~267-330) reconstructs from snapshot metadata, not from re-loaded bindings.
- The existing tests (`test_registered_corpus_launch.py` lines ~569-714) prove this in unit tests.
- But no deployed smoke currently proves that a killed-and-resumed AOI by-ref job preserves thinker identity through recovery.

**Mitigation**: This is bounded because recovery uses the same snapshot mechanism genealogy already uses, and genealogy recovery has been code-proven. A unit-test-only proof is probably sufficient for Stage 9 if the proving smoke is otherwise adequate.

---

### Finding 6: The genealogy live gate may need re-verification after Stage 8 code changes

**Severity: LOW**

**Problem**: Stage 8 modified `api/server.py` and `api/models_db.py` in the Critic. These are the same files that carry the genealogy by-ref launch path. If the Stage 7 genealogy live gate is run after Stage 8 code is deployed, it is testing Stage 8 code, not Stage 7 code. The memo implicitly assumes this is fine (and it probably is — Stage 8's changes to `server.py` added AOI branches that should not affect genealogy branches). But it should state this explicitly.

**Why it matters**: The genealogy launch path in `server.py` is the same function that dispatches on `launch_mode`. Stage 8 added new AOI branches within that function. If a bug in the AOI branch affects the common dispatch path, it would break genealogy too.

**Concrete basis**: The launch mode selector `_select_genealogy_v2_launch_mode()` dispatches on `workflow_key`. AOI and genealogy are separate branches. Stage 8 did not modify the genealogy branch. Risk is low.

---

### Finding 7: The memo correctly identifies the AOI-as-Stage-7-analogue framing

**Severity: LOW (positive finding)**

**Problem**: None — this is a confirmation finding.

The code evidence strongly supports the memo's claim that Stage 8 was the AOI analogue of Stage 6 and Stage 9 should be the AOI analogue of Stage 7. The concrete evidence:

- Stage 6 (genealogy): built external bindings, sync, by-ref launch. Stage 7 (genealogy): flipped default, added provenance, added cutover smoke.
- Stage 8 (AOI): extended by-ref request for AOI, added thinker consistency validation, added snapshot metadata preservation, added AOI corpus builder. Stage 9 (AOI): proposed to flip default, verify provenance, add cutover smoke.

The structural parallel is exact.

---

## 2. Big-Picture Verdict

**Mostly yes, but the operational prerequisite burden needs honest sizing.**

The memo has the right next stage boundary. The code evidence confirms:

- The AOI by-ref substrate is code-complete across both repos
- The remaining gaps are operational (migrations, deployment, smoke tests), not architectural
- The Stage 6→7→8→9 parallel is structurally sound
- The cutover policy mirrors Stage 7's genealogy pattern exactly

But the memo presents the operational prerequisites (section 9A) as a checklist to be verified, when in practice they are the most time-consuming and failure-prone part of the stage. The two unapplied migrations, the unproven genealogy live path, and the AOI smoke data setup collectively represent more effort than the cutover itself.

The memo should be understood as:

- **70% operational prerequisites** (migrations, live gates, smoke setup)
- **20% proving work** (inline/by-ref parity, cutover smoke execution)
- **10% cutover mechanics** (default flip, flag retirement, env control)

That is still the right next stage. But framing it as "gates first, then cutover" understates the gate weight.

---

## 3. Scope Corrections

### Absolutely belongs in Stage 9:

1. Apply Critic migration 030 (rollout provenance columns)
2. Apply Critic migration 031 (source_document_id backfill) with production data validation
3. Run genealogy live gate (Stage 7 operational proof) — deferred too long already
4. Build and run AOI by-ref proving smoke
5. AOI inline/by-ref corpus_ref parity proof
6. AOI default cutover: retire `AOI_THEMATIC_V2_BY_REF`, flip to by-ref default, add `AOI_THEMATIC_V2_INLINE=1` as rollback
7. Verify rollback works (launch with `AOI_THEMATIC_V2_INLINE=1` and confirm inline behavior)

### Absolutely does not belong:

1. Multi-thinker AOI generalization
2. Broad Critic compatibility/dual-write cleanup
3. New analyzer-v2 binding-role semantics for AOI target members
4. Packaging, SDK, or generated-app work
5. Dashboards, analytics, or metrics infrastructure
6. Removing the inline AOI path entirely

### Should be treated as prerequisite rather than stage scope:

1. **Migration 030 and 031 application** — These are Stage 7 and Stage 8 completion tasks, respectively. The memo correctly lists them in 9A as prerequisites, but the stage plan should treat them as a Phase 0 before Stage 9 proper begins. If migration 031 backfill produces bad data, Phase 0 becomes a stabilization detour, and Stage 9 cutover does not start.

2. **Genealogy live gate execution** — This is Stage 7 follow-through. It should be completed before Stage 9 is claimed to have started. The memo already says this, but the implementation plan should enforce it as a hard checkpoint.

3. **AOI smoke test data setup** — The proving smoke needs project + thinker + reference text data. Setting up that data (or identifying suitable existing data) is a prerequisite to running the smoke, not part of the smoke itself.

---

## 4. Hidden Operational / Migration Cost

### 4.1 Live migration application order

The correct deployment and migration order is:

1. Deploy analyzer-v2 (already has AOI by-ref support from Stage 8 — purely additive)
2. Apply Critic migration 030 (nullable columns on `v2_run_references` — safe, no backfill)
3. Apply Critic migration 031 (backfill `source_document_id` on `influence_reference_texts`)
4. **Validate migration 031 output**: Check that backfilled `source_document_id` values match what the runtime `_build_source_document_id()` helper would produce for each row. If they don't match, corpus_ref parity is broken before any smoke runs.
5. Deploy Critic with Stage 8 code (AOI by-ref opt-in already present)
6. Run genealogy live gate (Stage 7 proof)
7. Run AOI by-ref proving smoke (with `AOI_THEMATIC_V2_BY_REF=1`)
8. Compare inline vs. by-ref corpus_ref
9. If parity passes: deploy new Critic with AOI by-ref default

Step 4 is the hidden cost. The memo does not mention it.

### 4.2 Rollback control semantics

The transition from `AOI_THEMATIC_V2_BY_REF` (opt-in) to `AOI_THEMATIC_V2_INLINE` (rollback) is clean in steady state. During the transition:

- If the env has `AOI_THEMATIC_V2_BY_REF=1` when new code deploys: works, because by-ref is now the default anyway. The flag is ignored with a deprecation warning.
- If the env has no AOI flag: old code does inline, new code does by-ref. This is the intended default flip.
- Rollback: set `AOI_THEMATIC_V2_INLINE=1` on new code, or revert to old code. Both work.

The hidden cost is operator communication: someone needs to know that `AOI_THEMATIC_V2_BY_REF` is deprecated and `AOI_THEMATIC_V2_INLINE` is the new rollback lever. The memo should specify whether this is documented in a deployment runbook or just in the code.

### 4.3 AOI proving smoke logistics

The genealogy cutover smoke (`test-stage7-genealogy-cutover-smoke.sh`) is a bash script that:
- Creates a run via Critic API
- Asserts `launch_mode` in the response
- Optionally waits for completion and checks `corpus_ref` backfill

An AOI equivalent needs to:
- Identify or create a project with subject/response documents
- Identify or create a thinker with reference texts
- Ensure those reference texts have persisted `source_document_id` (migration 031)
- Start an inline AOI run, wait for completion, capture `corpus_ref`
- Start a by-ref AOI run (with `AOI_THEMATIC_V2_BY_REF=1`), wait for completion, capture `corpus_ref`
- Compare the two `corpus_ref` values

That is at minimum a 2-4 hour runtime (two complete AOI workflow executions). And it requires either:
- A known test project with the right data shape (fragile across environments)
- A setup phase that creates test data via API (more work but reproducible)

The memo should specify which approach and acknowledge the runtime cost.

### 4.4 Parity proof burden

The `corpus_ref` comparison is the critical gate. It works only if:

1. The same `source_document_id` values flow through both paths (depends on migration 031 correctness)
2. The same member set is included (depends on `_load_aoi_prior_works()` inline selection matching the sync+resolve by-ref selection)
3. The same qualifiers are present (`selected_source_thinker_id`, `selected_source_thinker_name`, `workflow_key`, `objective_key`)

If parity fails, the debugging surface is:
- Inline: `store.py:_build_aoi_corpus_payload()` using plan_data from inline request
- By-ref: same function using plan_data from by-ref snapshot/plan-request
- Differences could come from: member ordering, `source_document_id` derivation, thinker name normalization, chapter ID representation

The memo's assumption that parity "should work because both paths now share the same persisted `source_document_id` rule" is reasonable but unproven. Stage 9 should budget for one debugging iteration if the first parity check fails.

### 4.5 Operator-visible provenance sufficiency

The memo says Stage 9 should "verify and surface what already exists" rather than "invent another AOI-specific provenance store." The code already has:

- `V2RunReferenceDB.launch_mode` (will show `"by_ref"` for AOI after cutover)
- `V2RunReferenceDB.registered_corpus_scope` (will show AOI binding scope)
- `V2RunReferenceDB.sync_summary` (will show sync stats)
- `V2RunReferenceDB.corpus_ref` (backfilled from result manifest)

For AOI, the additional operator question is: **which thinker was selected?** That is in the plan_data but not surfaced on `V2RunReferenceDB`. The Critic job-detail read would need to extract `selected_source_thinker_id` from the plan_data to surface it. This is a small enhancement the memo should acknowledge.

### 4.6 Coexistence window behavior

Between "proving starts" and "default flip," any production AOI runs use the inline path. After the flip, new AOI runs use by-ref. Old inline results and new by-ref results coexist in the same discovery/result surface. That is fine — they carry different `launch_mode` provenance. But the memo should acknowledge that the first by-ref AOI results will exist alongside inline-era results with no `launch_mode` provenance (since Stage 7 provenance only applies to runs started after the migration). Those older runs will have `launch_mode = null`.

---

## 5. Recommended Next Memo Correction

The memo is close to being a good planning baseline. The minimum corrections before it becomes one:

### 5A. Add explicit migration validation as a Phase 0 gate

Before the "Stage 9 begins" line, add:

> Migration 031 backfill output must be validated against a sample of production rows. Specifically: for N representative `InfluenceReferenceTextDB` rows, the backfilled `source_document_id` must match what the runtime `_build_source_document_id()` helper would produce for the same row. If it doesn't, the Stage 9 proving pass will produce a false parity failure.

### 5B. Size the operational prerequisites honestly

Replace the flat bullet list in section 9A with a phased breakdown:

- **Phase 0 (prerequisite)**: Apply migrations, validate backfill, deploy both repos
- **Phase 1 (genealogy gate)**: Run genealogy live gate, verify genealogy inline rollback
- **Phase 2 (AOI proving)**: Run AOI smoke with opt-in flag, compare inline/by-ref corpus_ref
- **Phase 3 (cutover)**: Flip AOI default, verify rollback, retire old flag

And acknowledge that Phase 0 alone may take a session, and Phase 2 requires 4+ hours of deployed compute.

### 5C. Specify the AOI proving smoke data strategy

Add one of:
- "The AOI smoke will use project X which has the right data shape"
- "The AOI smoke includes a setup phase that creates test data via Critic API"
- "The AOI smoke requires a precondition script that verifies suitable test data exists"

### 5D. Address selected-thinker provenance surfacing

Add: "Stage 9 may need one small Critic job-detail enhancement to surface `selected_source_thinker_id` from plan_data, so operators can see which thinker was used in an AOI by-ref run without inspecting raw plan data."

### 5E. Acknowledge parity debugging budget

Add: "If the first inline/by-ref corpus_ref comparison fails, Stage 9 should budget one debugging iteration. The most likely failure cause is a `source_document_id` derivation mismatch between the migration backfill and the sync-time assignment."

---

With those five corrections, the memo becomes a solid planning baseline for an implementation pass. The stage boundary is right. The sequencing is right. The out-of-scope decisions are right. What needs tightening is honest sizing of the operational work that precedes the actual cutover.
