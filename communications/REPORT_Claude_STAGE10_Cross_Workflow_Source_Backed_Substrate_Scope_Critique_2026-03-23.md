# Critique: Stage 10 / Cross-Workflow Source-Backed Substrate Scope

Date: 2026-03-23
Reviewer: Claude (skeptical strategic review)
Target Memo: `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md`

## Verdict

**Approve**

Post-revision note:

- After reviewing the revised `communications/MEMO_2026-03-23_stage10_cross_workflow_source_backed_substrate_scope.md`, the earlier blockers are now closed at the memo level.
- The revised memo now says concretely what the genealogy implementation does, drops the premature registry framing in favor of a shared readiness schema with separate implementations, carries the AOI/the-critic coupling explicitly, and raises the proof bar with a genealogy-specific data-insufficient selector case.
- The findings below remain the rationale for why the earlier draft needed revision before approval.

The memo is strategically well-positioned and architecturally restrained. Its core insight — that the next missing seam is source-backed substrate normalization rather than page planning or host cutover — is correct. The boundary discipline is real: it explicitly excludes Stages 11/13 work and refuses to fake a shared selector enum.

---

## Findings (ordered by importance)

### 1. ARCHITECTURAL: The memo does not specify what "source-backed composition" means for genealogy — and the two workflows have fundamentally different downstream architectures

**Severity: High — must be resolved before implementation**

This is the single most important finding.

The memo correctly observes that AOI has a real source-backed composition bridge and genealogy does not yet participate in it. But it then proposes a "shared source-backed adapter layer" without confronting a fundamental asymmetry the codebase makes very clear:

**AOI's source-backed path** (`composition_source_bridge.py` → `compose_from_intent.py`):
- Starts from a completed job
- Extracts durable artifacts into a formal source catalog
- Selects source families via profile presets
- Materializes source sections into compose-ready input
- Runs the transient compose pipeline to produce a *new* page

**Genealogy's downstream path** (`presentation_api.py:assemble_page()` → `bounded_dynamic_composition.py`):
- Starts from a completed job
- Loads existing prepared view payloads
- Applies runtime surface selection via `composition_mode` at serve time
- Returns an *already-prepared* page with different surface emphasis

These are architecturally different flows. AOI's bridge *reconstructs source material* from durable outputs to *generate a new transient experience*. Genealogy's `composition_mode` *selects among pre-prepared surfaces* within an existing presentation.

The memo says genealogy should participate in a "source-backed adapter" — but it never says whether genealogy's participation means:

a) Genealogy should also extract outputs into source sections and recompose through a transient pipeline (the AOI model)
b) Genealogy should expose its existing `composition_mode` surface-selection through a normalized readiness/inspection contract (a weaker claim)
c) Something in between

This matters because option (a) would be large, novel work that goes well beyond "wrapping existing substrate." Option (b) would make "source-backed" an overstatement — `composition_mode` selection is presentation-time surface switching, not source reconstruction. Option (c) needs to be specified.

**Recommendation**: The memo should explicitly state what the genealogy adapter *does*. If it wraps `composition_mode` selection behind a normalized readiness/inspection response, say that. If it proposes real source-material extraction from genealogy outputs (analogous to AOI's artifact-to-section bridge), say that and acknowledge the work involved.

### 2. STRATEGIC: The adapter registry pattern may be premature abstraction over two radically different architectures

**Severity: Medium — strategic risk**

The memo proposes a "source-backed adapter registry" (Decision 1) with normalized:
- source readiness
- source families
- allowed selectors
- blocked selectors
- downstream contract kind

This pattern makes architectural sense when there are 3+ workflows with meaningfully similar downstream structures. With exactly two workflows whose downstream architectures are fundamentally different (Finding 1), the registry risks becoming a leaky abstraction where:

- The AOI adapter does real source catalog resolution, artifact extraction, and section materialization
- The genealogy adapter does little more than check whether a prepared presentation exists and which `composition_mode` values are available
- The "normalized output shape" is so generic it adds indirection without real normalization

The canonical roadmap's Stage 10 exit evidence says: "at least one second workflow can compose from durable source truth without AOI-specific hacks." The question is whether wrapping genealogy's `composition_mode` behind an adapter constitutes "composing from durable source truth" or is really a relabeling of existing presentation-time surface selection.

**Recommendation**: Consider whether the bounded Stage 10 should instead:
1. Add the normalized inspection/readiness endpoint (Decision 5) directly, without requiring a full adapter registry
2. Let the AOI adapter and genealogy adapter be separate implementations behind a shared response schema
3. Defer the registry pattern until a third workflow makes the abstraction non-premature

### 3. STRATEGIC: The memo underplays the-critic coupling in the source-backed composition path

**Severity: Medium**

The memo says (Decision 6) to keep AOI's `compose-from-source` route alive and add adapters below it. But the code reveals deeper coupling:

- `compose_from_intent.py:49`: `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"` — hardcoded
- `compose_from_intent.py:64-71`: `_ALLOWED_PATTERN_KEYS` and `_ALLOWED_RENDERER_TYPES` are AOI+the-critic-specific allowlists
- The entire `compose_from_source` flow resolves to a `ComposeFromIntentRequest` that passes through an AOI-only validation gate

If Stage 10 adds a genealogy adapter that claims normalized source-backed readiness, but the only consumer path for *acting on* that readiness is the AOI-only `compose-from-source` route, then the genealogy adapter is an inspection-only seam with no composition followup path of its own.

This is not necessarily wrong — the memo explicitly says Stage 10 "should not try to unify the entire downstream presenter implementation behind one new mega-route." But the memo should be honest that the genealogy adapter's downstream followup will point to `assemble_page(..., composition_mode=...)` rather than anything source-backed in the AOI sense.

**Recommendation**: State explicitly that the genealogy adapter's downstream followup contract points to existing `GET /v1/presenter/page/{job_id}?composition_mode=X` rather than to `compose-from-source`. This is honest and keeps the stage real.

### 4. ARCHITECTURAL: The "allowed selectors" and "blocked selectors" normalization is underspecified for genealogy

**Severity: Medium**

For AOI, the memo's candidate public shape makes sense: `allowed_profiles` and `blocked_profiles` map directly to `evaluate_compose_profile_feasibility()` (which is already hardened in Stage 9).

For genealogy, the analogous concept would be: which `composition_mode` values are valid for this job, and which are blocked? But the codebase shows `validate_requested_composition_mode()` (`bounded_dynamic_composition.py:267-279`) validates only against a static mode-to-workflow mapping — it does not check whether the actual data supports a particular mode. For example, `adaptive_relationship_surface_v1` requires relationship classification data; if that data is missing from the presentation, the mode will fail at runtime rather than at readiness inspection time.

So a genealogy adapter that reports "these composition_modes are allowed" would either:
- Report all genealogy-compatible modes as allowed (which is what the static validation does today), giving false confidence
- Need to inspect actual prepared-presentation data to determine feasibility (which is real new work analogous to `evaluate_compose_profile_feasibility`)

**Recommendation**: The proof bar should require that at least one genealogy blocked-selector case demonstrates a mode that is *statically valid* but *data-insufficient*, not just one that fails the workflow-key check.

### 5. PROOF/EVIDENCE: The proof bar is sound but should add one genealogy negative case

**Severity: Low-medium**

The proof bar (Section "Proof Bar") requires:
1. One AOI case wrapping the existing bridge
2. One genealogy case proving second-workflow participation
3. One fail-closed case for incomplete source truth
4. Selector asymmetry evidence

This is reasonable. But case 3 could be satisfied by a trivially blocked case (e.g., unknown workflow key). The proof should require:

- One genealogy-specific blocked case where the workflow is valid but the source truth is incomplete for the requested downstream composition (e.g., a genealogy job whose relationship classification artifacts are still pending, making `adaptive_relationship_surface_v1` infeasible while `bounded_dynamic_genealogy_v1` remains available)

That would prove the adapter actually inspects data rather than just checking workflow compatibility.

### 6. STRATEGIC: Genealogy is the right second workflow — this is well-justified

**Severity: Positive finding**

The memo's choice of genealogy is well-grounded:

- `store.py` already builds corpus registrations for both AOI and genealogy (`_build_aoi_corpus_payload` and `_build_genealogy_corpus_payload`)
- `result_contract.py:52`: `SUPPORTED_PRODUCT_WORKFLOWS = {AOI_WORKFLOW_KEY, GENEALOGY_WORKFLOW_KEY}`
- `bounded_dynamic_composition.py`: 5 genealogy composition modes, 2 AOI composition modes
- Genealogy has real artifact storage (`store_relationship_classification_artifact`)
- No other workflow has comparable downstream substrate

The `logical` objective exists in `src/objectives/definitions/logical.json`, but it has no corresponding workflow definition in `src/workflows/definitions/` — so it is genuinely not ready.

### 7. STRATEGIC: The stage-ordering discipline is correct

**Severity: Positive finding**

The memo is right to exclude:
- Stage 11 page planning
- Stage 13 host-contract cutover
- Task-driven selector planning

The codebase confirms these exclusions are honest: `compose_from_intent.py` has bounded allowlists, `presentation_api.py:assemble_page()` has no task-driven surface selection, and the host contract is implicit. Widening Stage 10 into any of these would collapse multiple unsolved problems into one stage.

### 8. ARCHITECTURAL: Decision 4 (reuse durable result/presentation substrate) is correct

**Severity: Positive finding**

The memo correctly identifies that `build_result_manifest()`, `get_result_presentation()`, `assemble_page()`, and `validate_requested_composition_mode()` already serve both workflows. Inventing a second restore system would be a real mistake.

### 9. ARCHITECTURAL: Decision 2 (normalize outputs, not selector vocabulary) is the right call

**Severity: Positive finding**

The codebase confirms the selector semantics are genuinely asymmetric:

- AOI: `ComposeFromSourceProfile = Literal["dossier", "comparison"]` (`schemas.py:624`)
- Genealogy: 5 `composition_mode` values like `adaptive_relationship_surface_v1`, `declarative_genealogy_relationship_conditions_suite_v1`

Forcing these into one shared enum would be a premature false unification. The memo's approach of keeping them as a discriminated union in the response is architecturally sound.

---

## Perspective Docs Folder

No relevant Perspective docs folder exists in analyzer-v2 or the-critic. This fact should remain explicit so nobody assumes a missing design corpus is silently driving the architecture.

---

## Summary of Required Revisions

Before implementation, the memo should:

1. **Specify what the genealogy adapter actually does** — is it wrapping `composition_mode` surface selection or proposing real source-material extraction? Be concrete about the downstream followup contract for genealogy.

2. **State that the genealogy adapter's downstream followup points to `assemble_page` with `composition_mode`**, not to `compose-from-source`. This keeps the claim honest.

3. **Strengthen the proof bar** with a genealogy-specific data-insufficient blocked case that proves the adapter inspects real data, not just workflow-key validity.

4. **Consider whether the adapter registry is premature** — a shared response schema with separate implementations may be better than a registry pattern for exactly two workflows with different architectures.

The strategic direction is sound. The stage boundary is right. The revisions are about specificity, not direction.
