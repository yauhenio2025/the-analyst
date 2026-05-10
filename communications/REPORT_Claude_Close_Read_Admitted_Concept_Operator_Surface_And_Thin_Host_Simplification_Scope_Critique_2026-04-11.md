# Report: Close Read Admitted Concept Operator Surface And Thin Host Simplification Scope — Critique

Date: 2026-04-11
Reviewer: Claude Opus 4.6
Memo Under Review: `communications/MEMO_2026-04-11_close_read_admitted_concept_operator_surface_and_thin_host_simplification_scope.md`

## Context Check

All required memos were read in full:

| Memo | Status |
|------|--------|
| `MEMO_2026-03-30_distilled_strategic_roadmap.md` | Read in full |
| `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` | Read (first 10K tokens — confirmed strategic direction and Phase E status) |
| `MEMO_2026-04-04_close_read_roadmap_recalibration.md` | Read in full |
| `MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` | Read in full |
| `MEMO_2026-04-11_close_read_temporary_state_snapshot_after_translated_artifact_authority_return.md` | Read in full |
| `MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_completion.md` | Read in full |
| `MEMO_2026-04-11_close_read_roadmap_update_after_concept_translated_artifact_authority_live_closeout.md` | Read in full |
| `MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_scope.md` | Read in full |
| `REPORT_Codex_Close_Read_Concept_Translated_Artifact_Authority_Live_Closeout_Scope_Audit_2026-04-11.md` | Read in full |
| `REPORT_Claude_Close_Read_Concept_Translated_Artifact_Authority_Live_Closeout_Scope_Critique_2026-04-11.md` | Read in full |

All required codebases were inspected:

| Codebase | Method | Key Files |
|----------|--------|-----------|
| `analyzer-v2` | Direct local read + deployed `origin/master` via `git show` | `orchestrator.py` routes, `concept_by_ref.py` |
| `the-critic` | Direct local read + deployed `origin/master` via `git show` | `server.py` (local and deployed `_run_rebased_concept_analysis`, deployed `_validated_translated_concept_artifact`, deployed `_concept_artifact_authority_url`) |
| `analyzer-mgmt` | Direct local read + deployed `origin/master` via `git show` | `frontend/src/pages/jobs/[id].tsx` (local and deployed `ConceptArtifactAuthorityCard`) |

All required live URLs were checked:

| URL | Status | Key Result |
|-----|--------|------------|
| analyzer-v2 exact logical (fresh project, `job-plan-fcc8b88fa4fc`) | **200** | `lookup_mode: exact_run`, `contract_validation_status: passed` |
| analyzer-v2 latest validated logical (fresh project) | **200** | `lookup_mode: latest_validated`, same job id |
| analyzer-v2 exact inferential (fresh project, `job-plan-077aeca1ffc8`) | **200** | `lookup_mode: exact_run`, `contract_validation_status: passed` |
| analyzer-v2 latest validated inferential (fresh project) | **200** | `lookup_mode: latest_validated`, same job id |
| the-critic logical readback + `X-Project-ID` | **200** | `execution_owner: analyzer-v2`, `source_owner: analyzer-v2`, hosted authority URL, `passed` |
| the-critic inferential readback + `X-Project-ID` | **200** | `execution_owner: analyzer-v2`, `source_owner: analyzer-v2`, hosted authority URL, `passed` |
| the-critic scrutiny readback + `X-Project-ID` | **200** | `concept: innovation`, `count: 1`, `argument_id: A1`, `mode: quick` |
| analyzer-mgmt `/jobs/job-plan-fcc8b88fa4fc` | **200** | SPA shell only via WebFetch (expected — requires browser hydration) |
| analyzer-mgmt `/jobs/job-plan-077aeca1ffc8` | **200** | SPA shell only via WebFetch (expected — requires browser hydration) |

---

## Verdict: approve with corrections

The memo is strategically sound and picks the right next corridor. But it materially overstates how much work remains, because it was drafted against local code that is significantly behind the deployed state. The deployed stack already implements much of what the memo proposes to build.

---

## The Central Finding: The Deployed Stack Is Ahead Of The Memo

This is the most important finding in this review.

### Deployed the-critic is already thin on the admitted concept seam

The memo says:

> the-critic still persists compatibility copies, so the law around what that cache may and may not do should be made explicit in code and docs

This is true as a documentation concern. But it understates how much the deployed the-critic has already changed.

**Local checkout** (17 commits behind `origin/master`): `_run_rebased_concept_analysis` at `server.py:3989` still imports and calls `translate_inferential_result` / `translate_logical_result` from `analyzer_v2_recomposition.py` — local translation of raw phase outputs.

**Deployed code** (`origin/master`): `_run_rebased_concept_analysis` at deployed `server.py:4216` has been fully cut over:
1. Launches concept analysis through analyzer-v2 by-ref
2. Polls for completion
3. Calls `fetch_concept_analysis_result_sync()` — reads the **already-translated artifact** from analyzer-v2's authority route (NOT from local translation)
4. Validates through `_validated_translated_concept_artifact()` — fail-closed on any identity mismatch
5. Adds `_artifact_authority` metadata with hosted authority URL and stable artifact hash
6. Persists a compatibility copy

Key deployed commits that accomplished this:
- `f33789f` Cut concept analysis over to analyzer-v2 runtime
- `dc8ed0e` Fetch exact concept artifacts from analyzer-v2
- `7ddcff9` Read concept artifacts through analyzer authority
- `debec5b` Harden translated concept artifact cutover
- `8ecec9d` Fix concept artifact readback authority identity

The deployed `_validated_translated_concept_artifact()` function validates **10 fields** against expected values (consumer_key, external_project_id, concept_name, analysis_mode, workflow_key, engine_or_chain_key, depth, analyzer_v2_job_id, translation_template_key, lookup_mode) and additionally validates provenance fields — fail-closed with RuntimeError on any mismatch.

So the memo's Phase 3 ("simplify the-critic admitted concept seam — remove or gate any dead local recomposition paths, keep read-through semantics explicit") is already **largely deployed**. The remaining work is:
- Dead-code cleanup of `analyzer_v2_recomposition.py` if it still exists but is no longer called from the admitted seam
- Documentation of the compatibility-cache contract
- Possibly guard comments on the cache path

This is real work, but it is documentation and cleanup, not the implementation work the memo's tone implies.

### Deployed analyzer-mgmt already has the concept artifact surface

The memo says:

> job pages are the artifact/operator surface ... the operator surface should be explicit and stable enough that a fresh concept job does not feel like a generic presenter page with a hidden concept add-on

This correctly describes the goal. But the deployed analyzer-mgmt already implements it.

**Local checkout** (3 commits behind `origin/master`): `frontend/src/pages/jobs/[id].tsx` has only the generic `ResultBoundaryTab` — no concept-specific content.

**Deployed code** (`origin/master`, commits `a5bd2af`, `63daa08`, `3d18c2b`): The job page now includes:
- `ConceptArtifactAuthorityCard` component at line 879
- Shows: concept artifact badge, validation status, analysis_mode, lookup_mode, concept name, project id, analyzer_v2_job_id, workflow key, engine/chain key, depth, produced_at, transformation link (navigable), translated artifact preview
- Fetches from analyzer-v2's concept artifact route using `job.analysis_context` (consumer_key, external_project_id, concept_name, analysis_mode)
- **Decoupled from generic result boundary** (commit `63daa08`) — the concept artifact truth does NOT depend on generic presenter status or result-boundary state

The completion memo confirmed this with browser proof:

> analyzer-mgmt job pages, in a hydrated browser session, displayed the concept artifact card and the required authority fields for both fresh analyzer-v2 jobs

So the memo's Phase 2 ("harden the analyzer-mgmt job page concept artifact surface") is already **substantially deployed**. The remaining work is:
- Verification that the deployed surface satisfies the memo's acceptance criteria (it appears to)
- Possibly minor polish if specific field rendering is insufficient
- Documentation of what the operator surface shows and does not show

### What this means for the proposed implementation sequence

The memo proposes four phases:
1. Audit the actual admitted-seam operator and host responsibilities
2. Harden the analyzer-mgmt job page concept artifact surface
3. Simplify the-critic admitted concept seam
4. Rerun a minimal regression proof if code changes were required

Given the deployed state, the honest reading is:
- **Phase 1 (audit)** is the genuinely correct and necessary step — it would discover that most of Phases 2 and 3 are already deployed
- **Phase 2 (analyzer-mgmt hardening)** may reduce to verification + minor polish at most
- **Phase 3 (the-critic simplification)** reduces to dead-code cleanup + documentation + cache-law documentation
- **Phase 4 (regression proof)** may not trigger at all if Phase 2 and 3 produce no code changes, or only dead-code removal

This is not a criticism of the memo's strategic direction. It is a factual correction: the work is smaller than the memo implies, because the implementation has advanced faster than the documentation.

---

## What The Memo Gets Right

### 1. The corridor selection is correct

Moving from "prove the seam works" to "stabilize and document what is already deployed" is exactly the right next move. The distilled strategic roadmap (Phase E generality proof, anti-drift rules) supports this: stabilization of an honestly-proved seam before opening a new corridor.

### 2. The three-service scope is correct

Bounding the tranche to analyzer-v2 + analyzer-mgmt + the-critic for `logical` and `inferential` only is clean and disciplined. The out-of-scope list (new submodes, cross-corpus, standalone extraction, broader UI redesign) is comprehensive and correct.

### 3. The shared authority-field set is concrete and auditable

The field set:
- `analyzer_v2_job_id`
- `concept`
- `analysis_mode`
- `workflow_key`
- `engine_or_chain_key`
- `translation_template_key`
- `depth`
- `produced_at`

plus the-critic-only fields (`authority_url`, `artifact_hash`) is exactly what the deployed code already preserves across all three surfaces. The memo's treatment of these as "law" is appropriate.

### 4. The strategic reading is honest

The memo correctly maintains:
- analyzer-v2 as the brain
- hosts as thinner shells
- Close Read as the app/product layer, not where analytical truth is authored

And it correctly resists:
- treating analyzer-mgmt as optional
- allowing the-critic to remain a shadow semantic author

### 5. The acceptance criteria are testable

All six acceptance criteria can be verified against the live deployed stack today. Most of them already pass.

---

## What The Memo Gets Wrong Or Overstates

### Correction 1: The memo is drafted against local code, not deployed state

This is the root cause of most factual issues.

| Repo | Local behind origin/master | Key consequence |
|------|---------------------------|-----------------|
| analyzer-v2 | 11 commits | Local lacks `concept_artifact_authority.py` authority layer |
| the-critic | 17 commits | Local still does local translation; deployed reads from analyzer-v2 authority |
| analyzer-mgmt | 3 commits | Local lacks `ConceptArtifactAuthorityCard`; deployed has it |

The memo's "current starting point" section says:

> analyzer-mgmt concept artifact display still rides inside a generic presenter shell and can be hydration-laggy on fresh jobs

This is false for the deployed code. The deployed `ConceptArtifactAuthorityCard` is decoupled from the generic result boundary (commit `63daa08` "Decouple concept artifact job view from result boundary"). It fetches directly from analyzer-v2's concept artifact route, independent of generic presenter state.

> the-critic still persists compatibility copies, so the law around what that cache may and may not do should be made explicit in code and docs

The "still persists compatibility copies" is accurate. But the deployed the-critic's compatibility-copy path already carries full authority metadata and is already explicitly non-authoritative in behavior (validated read-through, not local recomposition).

> legacy or dead local concept-authoring paths for admitted modes may still exist in the-critic even if the live happy path no longer uses them

This is an honest concern. The deployed `_run_rebased_concept_analysis` no longer imports local translation, but the `analyzer_v2_recomposition.py` module may still exist as dead code. Verifying and cleaning this up is legitimate Phase 3 work.

**Recommended fix:** Add a preliminary step before Phase 1 that requires source-alignment against deployed `origin/master` for all three repos. The memo already mentions this need in passing ("inspect the live and deployed-source-aligned state") but does not make it a hard prerequisite.

### Correction 2: Phase 2 (analyzer-mgmt hardening) overstates the remaining gap

The memo describes Phase 2 as if the concept artifact surface needs to be built:

> make the job page render the concept artifact section in a more deterministic and explicit way

The deployed job page already:
- Has a dedicated `ConceptArtifactAuthorityCard` component
- Shows all 8 shared authority fields + transformation link + translated artifact preview
- Is decoupled from generic result boundary state
- Gates on `job.analysis_context` (not generic presenter metadata)

What Phase 2 should actually say:
- Verify the deployed `ConceptArtifactAuthorityCard` against the shared authority-field law
- Identify any specific rendering gaps (if any)
- If the surface is already sufficient, document it and mark Phase 2 as verification-only

### Correction 3: Phase 3 (the-critic simplification) should distinguish deployed state from remaining cleanup

The memo describes Phase 3 as:

> remove or gate any dead local recomposition paths
> keep read-through semantics explicit
> preserve project-scoped behavior through `X-Project-ID`
> make the compatibility-cache contract explicit in code and docs

The deployed code already satisfies points 2, 3, and largely point 4. What remains:
- **Point 1** is legitimate: verify whether `analyzer_v2_recomposition.py` (or similar dead-code modules) still exist on deployed `origin/master` and clean them up
- **Point 4** needs one concrete deliverable: a brief documented cache-law section (where it lives, what it may/may not do, what metadata it must preserve)

The memo should frame Phase 3 as "verify-and-document the already-deployed thinning, plus clean up any residual dead code" rather than "simplify the-critic."

### Correction 4: The memo does not acknowledge the completion memo's own browser proof

The completion memo (`MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_completion.md`) already confirmed:

> analyzer-mgmt job pages, in a hydrated browser session, displayed the concept artifact card and the required authority fields for both fresh analyzer-v2 jobs

The scoping memo then says the operator surface "still rides inside a generic presenter shell." These two statements are in tension. The completion memo's browser proof should be cited as evidence that the Phase 2 work may already be done.

---

## Direct Answers To The Explicit Review Questions

### Does the memo correctly treat the current corridor as closed enough to move from proof into stabilization/simplification?

**Yes.** The live evidence is unambiguous:
- Fresh logical and inferential proofs both passed on the fresh closeout project
- analyzer-v2 exact and latest validated authority routes work for both modes
- the-critic readback returns correct authority metadata for both modes
- Scrutiny works on analyzer-v2-backed logical artifacts
- The completion memo documents this cleanly

The corridor is closed. Moving to stabilization is the right posture.

### Is the proposed next tranche the right one, or is it jumping too early beyond the admitted concept seam?

**It is the right next tranche.** Stabilizing the admitted concept seam (documenting the authority-field law, verifying the operator surface, cleaning up dead code) is exactly what should come after a successfully closed proof corridor, before broadening to new families or standalone extraction.

It is **not** jumping too early. If anything, it may slightly overstate how much work remains (see corrections above).

### Does the memo keep the larger direction clear enough?

**Yes.** The three-role architecture is maintained clearly:
- analyzer-v2 as the brain (sole semantic authority for admitted concept modes)
- analyzer-mgmt as operator surface (job-page artifact inspection)
- the-critic as thinner shell (non-authoritative read-through/cache host)

And the memo correctly defers:
- broader Close Read extraction
- standalone app shaping
- new concept submodes
- cross-corpus work

This matches the distilled strategic roadmap's Phase E trajectory and the April 5 default-families memo's reading that concept analysis is the next serious family candidate but hasn't reached the composition-layer question yet.

### Is analyzer-mgmt job-surface hardening the right next operator concern, or is the memo overstating the current job-page gap?

**The memo overstates the gap.** The deployed analyzer-mgmt already has a `ConceptArtifactAuthorityCard` that shows all the required shared authority fields, decoupled from generic result boundary. The completion memo's own browser proof confirmed this.

The honest operator concern is:
- Verify the deployed surface against the shared authority-field law (likely a pass)
- Identify any minor rendering issues (loading states, error states)
- Document the operator surface responsibility

This is verification and documentation work, not implementation work.

### Is the-critic thin-host simplification described concretely enough, or is it still too narrative?

**It is slightly too narrative for what is actually needed.** The deployed the-critic is already materially thin:
- Reads from analyzer-v2 authority (not local translation)
- Validates 10+ fields fail-closed
- Adds `_artifact_authority` metadata with hosted authority URL
- Persists compatibility copy with full provenance

What Phase 3 should concretely deliver:
1. Source-aligned audit of whether `analyzer_v2_recomposition.py` and any other local translation modules are still called from any live code path (likely not for admitted modes, but may still be called for non-admitted modes like `assumption`, `semantic_field`, etc.)
2. If dead for admitted modes: delete or explicitly gate with a clear "not used for admitted modes" guard
3. One brief cache-law document section describing what the compatibility copy is, what it may store, what it may not mutate, and what metadata it must preserve
4. Verification that `X-Project-ID` scoping is correctly enforced on all admitted-mode read paths (likely already the case)

### Does the memo keep the shared authority-field law concrete enough to implement and audit?

**Yes.** The 8 shared fields plus 2 the-critic-only fields are explicitly listed and match what the deployed code already preserves. This is one of the memo's strongest sections.

### Does the memo remain honest about local-vs-live divergence in analyzer-v2 and the-critic?

**No.** This is the memo's weakest point.

The memo acknowledges divergence in the temporary state snapshot and references "deployed-source-aligned state." But the scoping memo itself was clearly drafted against local code that is significantly behind deployed state:
- It describes analyzer-mgmt as needing a concept artifact surface (already deployed)
- It describes the-critic as needing simplification (already materially thinned on deployed `origin/master`)
- It says "legacy or dead local concept-authoring paths for admitted modes may still exist" — implying uncertainty about what's deployed

The memo should have been drafted from deployed `origin/master` inspections, not from local checkouts that are 3-17 commits behind.

### Is there any place where the memo understates or overstates what the live system already proves today?

**Overstates remaining work in two places:**

1. Phase 2 (analyzer-mgmt hardening): The deployed `ConceptArtifactAuthorityCard` already satisfies most of the memo's requirements. The memo frames this as implementation work rather than verification work.

2. Phase 3 (the-critic simplification): The deployed the-critic already reads from analyzer-v2 authority with full identity validation and fail-closed behavior. The memo frames this as simplification work rather than documentation and dead-code cleanup.

**Understates in one place:**

The memo does not acknowledge that the deployed the-critic's `_validated_translated_concept_artifact()` function already has comprehensive fail-closed identity validation covering all 10 expected fields plus provenance fields. This is stronger than the memo's language ("make the compatibility-cache contract explicit in code") implies — the code already makes the contract fairly explicit through the validation function itself.

### If you were protecting roadmap discipline, is this the right next corridor before broader Close Read extraction or new family work?

**Yes, unambiguously.**

The strategic roadmap (April 4 recalibration, April 5 default families memo, distilled roadmap Phase E) all point the same way:
1. Close the current concept authority corridor (**done**)
2. Stabilize and document what was proved (**this tranche**)
3. Only then decide between broader extraction or next family admission

Opening broader Close Read extraction or concept-analysis family expansion before the operator and host responsibilities are frozen would leave ambiguity about who owns what truth — exactly the kind of mess the strategic memos warn against.

The one qualification is that the actual work in this tranche is smaller than the memo implies. If the audit (Phase 1) confirms that the deployed stack already satisfies most acceptance criteria, the tranche may close as a lightweight verification-and-documentation exercise rather than a multi-phase implementation effort.

---

## Code-Backed Evidence Summary

### analyzer-v2 (deployed `origin/master`, 11 commits ahead of local)

| Component | Status | Evidence |
|-----------|--------|----------|
| Concept artifact authority route | **Live, working** | Both `exact_run` and `latest_validated` confirmed for logical and inferential on fresh project |
| `concept_by_ref.py` (launch) | **Live** | Builds plan, stores documents, creates job |
| Authority field set | **Complete** | `workflow_key`, `engine_or_chain_key`, `translation_template_key`, `depth`, `produced_at`, `analyzer_v2_job_id`, `concept_name`, `analysis_mode` — all returned live |

### the-critic (deployed `origin/master`, 17 commits ahead of local)

| Component | Deployed State | Evidence |
|-----------|---------------|----------|
| `_run_rebased_concept_analysis` | **Reads from analyzer-v2 authority** | Calls `fetch_concept_analysis_result_sync` — no local translation |
| `_validated_translated_concept_artifact` | **10-field fail-closed validation** | Validates consumer, project, concept, mode, workflow, engine, depth, job_id, template, lookup_mode |
| `_concept_artifact_authority_url` | **Hosted analyzer-v2 URL** | Uses `ANALYZER_V2_URL` env var, not localhost |
| `_artifact_authority` in readback | **Live, confirmed** | Both logical and inferential return `source_owner: analyzer-v2`, hosted URL, stable hash, `passed` |
| Local translation (`analyzer_v2_recomposition`) | **No longer called from admitted seam** | Deployed `_run_rebased_concept_analysis` does not import local translation |

### analyzer-mgmt (deployed `origin/master`, 3 commits ahead of local)

| Component | Deployed State | Evidence |
|-----------|---------------|----------|
| `ConceptArtifactAuthorityCard` | **Exists, deployed** | Shows all required fields: validation status, lookup mode, analysis mode, concept, project, job id, workflow, engine, depth, produced_at, transformation link, translated artifact preview |
| Decoupled from result boundary | **Yes** | Commit `63daa08` — concept artifact fetch is independent of generic presenter/result state |
| `analysis_context` gating | **Yes** | Concept artifact only fetched when `job.analysis_context` provides consumer_key, external_project_id, concept_name, analysis_mode |
| WebFetch browser proof | **Inconclusive** | WebFetch shows only SPA shell (expected for Next.js) — must use real browser for hydrated proof |

---

## Corrected Acceptance Criteria Assessment

Let me evaluate the memo's acceptance criteria against the current deployed state:

| Criterion | Current State |
|-----------|--------------|
| 1. analyzer-v2 remains sole semantic author for admitted concept artifacts | **Already true on deployed stack** |
| 2. analyzer-mgmt job pages show admitted concept artifact surface clearly | **Already deployed via `ConceptArtifactAuthorityCard`** — needs browser re-verification |
| 3. the-critic admitted concept readback is explicitly non-authoritative and analyzer-v2-derived | **Already true on deployed stack** — `_artifact_authority` metadata confirms this |
| 4. No residual local recomposition path remains live for admitted concept modes | **Likely true on deployed stack** — deployed `_run_rebased_concept_analysis` does not call local translation. Needs verification of whether dead-code modules still exist |
| 5. Shared authority fields consistent across all three surfaces | **Already true for most fields** — needs formal cross-surface audit |
| 6. If code changed, bounded regression proof passes | **May not trigger** — most work may be documentation/cleanup only |

---

## Tightened Bottom Line

**Approve with corrections.**

The memo identifies the right next corridor. Stabilizing the admitted concept seam before opening broader extraction or new family admission is strategically correct and aligns with the full roadmap hierarchy.

The corrections are:

1. **Acknowledge the deployed state honestly.** The memo was drafted against local code 3-17 commits behind `origin/master`. The deployed stack already implements most of what Phases 2 and 3 propose. Reframe Phases 2 and 3 as "verify-and-document the already-deployed state" rather than "build and harden."

2. **Make source-alignment a hard Phase 0 prerequisite.** Before Phase 1 (audit), require explicit alignment of local working trees to deployed `origin/master` for all three repos. The memo references this need but does not make it mandatory.

3. **Reframe Phase 2 as verification, not implementation.** The deployed `ConceptArtifactAuthorityCard` already shows all required fields, decoupled from generic result boundary. Phase 2 should verify this in browser and document the operator surface responsibility, not build a new surface.

4. **Reframe Phase 3 as dead-code cleanup + cache-law documentation.** The deployed the-critic already reads from analyzer-v2 authority with full identity validation and fail-closed behavior. Phase 3 should verify this, clean up any residual dead translation modules, and write the explicit cache-law documentation.

5. **Acknowledge the completion memo's browser proof.** The previous tranche's completion memo already confirmed the analyzer-mgmt concept artifact card works in a hydrated browser session. The scoping memo should cite this evidence rather than describing the surface as if it needs building.

With these corrections, the tranche becomes **smaller but more honest**: a verification-and-documentation exercise that freezes the already-deployed law, cleans up dead code, and writes the authority-field documentation that makes the next corridor's decision surface cleaner.

That is the right shape for a stabilization tranche after a successfully closed proof corridor.
