# Critique: Phase E AOI V2 Capture Provenance Persistence V1 Scope

Date: 2026-04-03
Reviewer: Claude Opus 4.6
Scope Memo: `communications/MEMO_2026-04-03_phase_e_aoi_v2_capture_provenance_persistence_v1_scope.md`

## Verdict

**Approve with corrections.**

The scope identifies the correct next bounded slice. The concrete loss is real, code-backed, and the smallest honest intervention that varies the proof boundary without inflating analyzer semantics. Three corrections are needed before implementation.

---

## Strongest Parts

### 1. Strategic sequencing is exactly right

The memo correctly identifies that the program should now vary the proof boundary (test the pipeline), not the proof surface (more analyzer shapes). The logic chain is sound:

- Selection-creation sufficiency: proven
- Analyzer contract consumability: proven
- Pipeline truth-preservation: **not proven, and visibly broken**

Pushing deeper on the same `aoi_by_sin_type` line before widening to mixed surfaces or second consumers is the defensible move. Each prior review (Claude and Codex, 2026-04-02) converged on exactly this recommendation.

### 2. The five evidence points are code-accurate

Every factual claim in the "Current Evidence Base" section checks out against the live codebase:

| Memo Claim | Code Evidence |
|---|---|
| `entity_id` exists on `CaptureSelection` | `CaptureContext.tsx:34` — `entity_id?: string` |
| `submitCapture` drops `entity_id` from POST body | `CaptureContext.tsx:105-123` — constructs request body without `entity_id` |
| `CaptureCreateRequest` lacks `entity_id` | `server.py:1284-1298` — 14 fields, no `entity_id` |
| `GenealogyCaptureDB` does not persist it | `models_db.py:2666-2703` — 27 columns, no `entity_id` |
| `capture_to_arsenal` hardcodes genealogy workflow | `server.py:22746` — `'workflow_key': 'intellectual_genealogy'` |

### 3. Out-of-scope list is honest and well-calibrated

The explicit deferrals are correct:

- `GenealogyCaptureDB` renaming: orthogonal to truth-preservation
- `captures/by-job` generalization: separate indexing question
- Arsenal stream taxonomy: broader mutation-layer redesign
- `aoi_by_theme` consumer work: premature without depth proof on one line

Each deferral has a clear reason that is not just "we'll do it later" but "it is a different kind of question."

### 4. Acceptance bar is testable

All 11 acceptance criteria are concrete and binary. No subjective quality gates or "feels right" criteria.

---

## Weakest Assumptions

### 1. `entity_id` dual-purpose is not acknowledged (CORRECTION NEEDED)

The memo treats `entity_id` as a clean opaque analyzer handle. But the current code at `CaptureContext.tsx:96-101` uses `entity_id` as a **fallback for `genealogy_job_id`**:

```typescript
// Current logic (paraphrased):
if (source_type === 'genealogy' && !genealogy_job_id) {
    genealogy_job_id = entity_id  // <-- dual purpose
}
```

This means `entity_id` currently does double duty:
- It is the opaque analyzer handle (what the memo wants to persist)
- It is also a genealogy-job-id fallback (what the existing code uses it for)

The implementation must not break this fallback while adding the new persistence path. The memo should acknowledge this tension explicitly and state that the existing derivation behavior stays untouched while the **new** code additionally sends `entity_id` as a separate field.

### 2. `source_workflow_key` value source is underspecified

The memo says `V2TabContent.tsx` threads `_workflowKey` and the renderer "already has" the value. This is true — but the memo does not state **what that value actually is** for the AOI proof line or where it originates.

From the code: `V2TabContent.tsx` receives `workflowKey` from the run context and threads it as `_workflowKey` in the renderer config. For AOI runs this would be something like `"aoi"` or the specific AOI workflow key from the orchestrator plan.

The implementation should confirm the exact string value and whether it is stable across re-runs of the same workflow type. If the value is a plan-specific UUID rather than a stable workflow-type key, persisting it as `source_workflow_key` has different provenance semantics than the memo implies.

### 3. Source-snapshot asymmetry between route legs is not discussed

The memo correctly says both `capture_to_arsenal` and `capture_to_research_todo` should carry provenance. But it does not note that the two existing source_snapshot constructions are **structurally different**:

**Arsenal** (`server.py:22737-22747`):
```python
{
  'context_title', 'selected_text', 'source_view_key',
  'source_section_key', 'depth_level', 'parent_context',
  'captured_at', 'structured_data_preview', 'workflow_key'
}
```

**Research todo** (`server.py:22876`):
```python
{
  'selected_text', 'structured_data', 'depth_level'
}
```

The arsenal snapshot is already richer and already has a `workflow_key` field (currently hardcoded). The research todo snapshot has no workflow key at all. The implementation needs guidance on whether to:

- Add `entity_id` and `source_workflow_key` to both snapshots identically
- Or harmonize the two snapshot shapes first

The correct v1 answer is: add to both identically, do not harmonize. But the memo should say so explicitly.

---

## Code-Backed Findings

### Finding 1: The POST body construction is the real seam

`CaptureContext.tsx:105-123` builds the request body by explicitly listing fields. The `entity_id` omission is not accidental — it is a structural absence in the request construction. Adding it requires:

1. Including `entity_id` in the POST body at `CaptureContext.tsx:~115`
2. Adding `entity_id` to `CaptureCreateRequest` at `server.py:~1298`
3. Persisting it on `GenealogyCaptureDB` at `models_db.py:~2686`
4. Returning it in `_capture_to_response` at `server.py:~22590`
5. Adding it to `CaptureResponse` at `server.py:~1320`

This is a clean additive path with no existing field conflicts. **Confirmed feasible.**

### Finding 2: `source_workflow_key` is net-new everywhere

Unlike `entity_id` (which exists client-side), `source_workflow_key` does not exist anywhere in the Critic codebase. It must be:

1. Added to the renderer selection-creation seam in `AoiSinFindingsRenderer.tsx`
2. Added to `CaptureSelection` interface
3. Threaded through `submitCapture` POST body
4. Added to all backend models (`CaptureCreateRequest`, `GenealogyCaptureDB`, `CaptureResponse`)
5. Read from persisted capture record in both route legs

This is still additive and optional, but involves more seams than `entity_id`. **Confirmed feasible but slightly larger surface than the memo implies.**

### Finding 3: The route legs are POST-only with minimal request bodies

Both `capture_to_arsenal` (`server.py:22657`) and `capture_to_research_todo` (`server.py:22787`) accept only `user_annotation` in their request bodies. All provenance comes from the **persisted capture record**, not from the route request.

This means the implementation path is:
- Persist `entity_id` and `source_workflow_key` at capture-creation time
- Read them back from the DB record in the route handlers
- Include them in the constructed source_snapshot

The memo's description of the architecture is correct: fix persistence, and routing inherits the truth.

### Finding 4: DB migration is needed

`GenealogyCaptureDB` maps to a real Postgres/SQLite table (`genealogy_captures`). Adding two nullable columns requires a migration. The memo does not mention this. For the Critic codebase this is typically an Alembic migration. The implementation should note:

- Two new nullable `String` columns: `entity_id`, `source_workflow_key`
- No default values needed (nullable)
- No backfill of existing rows (old captures stay null)

---

## Strategic Implications

### This slice is still Critic-local, and that is acceptable

The memo is honest that this is host-pipeline work, not platform-layer work. The strategic justification holds: proving that analyzer truth survives through a real host pipeline teaches more about reusable law than proving the same truth on a second analyzer surface.

However, the program should be aware of accumulating Critic-specific debt. After this slice, the honest next question should be whether the persistence pattern generalizes or whether it is creating Critic-only plumbing that a second host would need to re-derive.

### The genealogy naming debt is growing but still manageable

`GenealogyCaptureDB`, `genealogy_job_id`, `genealogy_captures` table — this naming is increasingly misleading as the capture model broadens to carry AOI workflow provenance. The memo correctly defers renaming, but the program should note that this is the **last** defensible slice before the naming becomes actively confusing rather than merely legacy.

### The `structured_data` field already carries rich analyzer output

`GenealogyCaptureDB.structured_data` (JSONB) persists the full structured data from the selection. For AOI `aoi_by_sin_type` findings, this already contains the card's analytical content. The new `entity_id` field adds the **identity** dimension that `structured_data` lacks — knowing *which* finding was captured, not just *what* it contained. This is the correct separation.

---

## Concrete Corrections

### Correction 1: Acknowledge `entity_id` dual-purpose

Add to the "Population And Contract Shape" section:

> The existing `CaptureContext` code (lines 96-101) uses `entity_id` as a fallback for `genealogy_job_id` when `source_type === 'genealogy'` and no explicit job ID is provided. This dual-purpose derivation must remain untouched. The new persistence path sends `entity_id` as its own field alongside the existing `genealogy_job_id` derivation.

### Correction 2: Specify `source_workflow_key` value contract

Add to the "Population And Contract Shape" section:

> The implementation should confirm that `_workflowKey` as threaded through `V2TabContent.tsx` is a **stable workflow-type identifier** (e.g., `"aoi"` or a canonical workflow key), not a plan-specific or run-specific UUID. If the value is run-specific, the provenance semantics differ from what this memo intends.

### Correction 3: Note source-snapshot treatment for both legs

Add to scope item 3:

> The two existing source_snapshot constructions differ structurally (arsenal is richer, research todo is minimal). This slice adds `entity_id` and `source_workflow_key` to both snapshots identically. It does not harmonize the two snapshot shapes — that is a separate concern.

### Correction 4 (minor): Note DB migration requirement

Add to the "Population And Contract Shape" section or a new "Migration" subsection:

> Adding `entity_id` and `source_workflow_key` to `GenealogyCaptureDB` requires a schema migration (two new nullable String columns, no backfill).

---

## Is There A More Defensible Next Step?

No. The alternatives are all either premature or orthogonal:

| Alternative | Why Not Now |
|---|---|
| `aoi_by_theme` consumer proof | Should prove depth on one line before width |
| Generic renderer-package consumption | Architectural redesign, not a bounded slice |
| Capture-status generalization | Indexing question, not provenance question |
| Arsenal stream taxonomy | Mutation-layer redesign, depends on provenance being solved first |
| Second non-AOI workflow proof | Premature without proving the pipeline carries truth on the first line |

The memo's choice is the smallest move that varies a new dimension (pipeline truth) while holding the proven dimension (surface contract) fixed. That is correct experimental design.

---

## Summary

The scope is right-sized, code-backed, and strategically sequenced. The four corrections above are implementation-grade clarifications, not design objections. Once the corrections are incorporated, this scope is ready for implementation.
