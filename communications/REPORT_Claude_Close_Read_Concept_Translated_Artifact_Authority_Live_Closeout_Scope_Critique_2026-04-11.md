# Report: Close Read Concept Translated Artifact Authority Live Closeout Scope — Critique

Date: 2026-04-11
Reviewer: Claude Opus 4.6
Memo Under Review: `communications/MEMO_2026-04-11_close_read_concept_translated_artifact_authority_live_closeout_scope.md`

## Context Check

All required memos were read in full:

| Memo | Status |
|------|--------|
| `MEMO_2026-03-30_distilled_strategic_roadmap.md` | Read (via background agent) |
| `MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md` | Read (via background agent) |
| `MEMO_2026-04-04_close_read_roadmap_recalibration.md` | Read (via background agent) |
| `MEMO_2026-04-05_close_read_roadmap_default_families_and_composable_modules.md` | Read (via background agent) |
| `MEMO_2026-04-06_close_read_concept_analysis_live_authority_and_thin_client_cutover_completion.md` | Read (via background agent) |
| `MEMO_2026-04-09_close_read_project_scoped_persistence_and_fresh_scrutiny_closure_completion.md` | Read (via background agent) |
| `MEMO_2026-04-09_close_read_roadmap_update_after_project_scoped_persistence_and_scrutiny_closure.md` | Read (via background agent) |
| `MEMO_2026-04-09_close_read_translated_artifact_authority_return_scope.md` | Read (via background agent) |
| `MEMO_2026-04-11_close_read_temporary_state_snapshot_after_translated_artifact_authority_return.md` | Read in full |
| `REPORT_Codex_Close_Read_Concept_Analysis_Translated_Artifact_Authority_Return_Scope_Audit_2026-04-10.md` | Read in full |
| `REPORT_Claude_Close_Read_Concept_Analysis_Translated_Artifact_Authority_Return_Scope_Critique_2026-04-10.md` | Read in full |

All required codebases were inspected:

| Codebase | Method | Key Files |
|----------|--------|-----------|
| `analyzer-v2` | Direct code read + deployed `origin/master` via `git show` | `orchestrator.py` routes, `concept_artifact_authority.py`, `concept_by_ref.py` |
| `the-critic` | Direct code read + deployed `origin/master` via `git show` | `server.py` (concept analysis flow, artifact authority validation, DB save), `analyzer_v2_recomposition.py` |
| `analyzer-mgmt` | Direct code read | `frontend/src/pages/jobs/[id].tsx`, `frontend/src/pages/implementations/[key].tsx` |

All required live URLs were checked:

| URL | Status | Result |
|-----|--------|--------|
| analyzer-v2 `/concept-analysis-by-ref/result` (exact job, logical) | **200** | `lookup_mode: "exact_run"`, `contract_validation_status: "passed"`, full translated artifact |
| analyzer-v2 `/concept-analysis-by-ref/result` (latest validated, logical) | **200** | `lookup_mode: "latest_validated"`, same job_id `job-plan-d9ed0f9db367` |
| the-critic `/api/concept/analyses/innovation?analysis_type=logical` + header | **200** | Full logical artifact with `_analysis_provenance.execution_owner: "analyzer-v2"` and `_artifact_authority.source_owner: "analyzer-v2"` |
| the-critic `/api/scrutiny/results/innovation` + header | **200** | `count: 1`, argument_id ARG-01, premise_index 0, mode quick |
| analyzer-mgmt `/jobs/job-plan-d9ed0f9db367` | **200** | SPA shell loaded; no server-side content (expected for Next.js) |
| analyzer-v2 `/concept-analysis-by-ref/result` (inferential, same project) | **404** | `"Translated concept artifact not found"` — no inferential proof exists |

---

## Verdict: approve with corrections

The memo is strategically sound, architecturally aligned, and correctly scoped. It reads the current situation honestly and proposes the right next move. The corrections are factual, not directional.

---

## What the Memo Gets Right

### 1. The "substantially implemented but not yet cleanly closed" framing is materially correct

This is the most important strategic claim in the memo, and it survives scrutiny.

**Live evidence confirms it:**

- analyzer-v2 exact-run authority route: live, returning `passed` artifacts with full provenance
- analyzer-v2 latest-validated route: live, returning the same artifact by identity
- the-critic readback: live, returning `_analysis_provenance` and `_artifact_authority` with hosted analyzer-v2 authority URL and stable artifact hash
- the-critic scrutiny: live, returning scrutiny results for the baseline logical specimen
- the-critic fail-closed behavior: confirmed (404 without project header)

All of this works on the April 9 baseline project. What is missing is: (a) a fresh post-fix proof on a brand-new project, (b) inferential proof (confirmed: no inferential artifact exists on the baseline project — returned 404), and (c) formal closeout documentation.

The framing is honest. It is neither "we haven't started" nor "we're done." It is "the corridor is built, the last mile is a clean closeout proof."

### 2. The closeout framing (not greenfield) is the right strategic posture

The memo explicitly says: "Do not write this tranche as if analyzer-v2 translated-artifact authority still needs to be invented from scratch." This is a direct response to the corrections from both April 10 reviews (Codex and Claude), which flagged that the previous scope memo understated what was already deployed.

The April 11 memo gets this right. It starts from deployed reality and proposes verification, not invention.

### 3. The brand-new project proof is the correct closeout requirement

Reusing the April 9 specimen would be circular. The post-fix code changes (authority URL canonicalization, concept identity normalization) need their own clean proof. A fresh project avoids stale-artifact contamination and proves the system works end-to-end under current deployed conditions.

### 4. The inferential proof requirement is genuine, not redundant

Live verification confirms there is **no existing inferential proof artifact** on the baseline project. The inferential mode has never been proven end-to-end through the translated-artifact-authority path on a real project. This is a real gap, not make-work.

### 5. The scoping boundaries are clean and disciplined

The memo correctly keeps:
- Only `inferential` and `logical` in scope
- No new concept submodes
- No cross-corpus work
- No standalone Close Read extraction
- No broader analyzer-mgmt console redesign
- No host-local scrutiny architecture reopening
- Scrutiny bounded to one fresh quick run as regression check

This matches the larger roadmap discipline. The program should resist the temptation to widen scope during closeout.

### 6. The "fix only the seam that breaks" principle is architecturally correct

Phase 5's graduated fix strategy (analyzer-v2 → the-critic → analyzer-mgmt, based on which layer fails) prevents scope creep during closeout. The priority order is correct: fix the innermost failure first.

### 7. The strategic reading is honest

The memo correctly identifies the two common mistakes to resist:
1. Reopening already-cleared host debugging corridors
2. Jumping to larger Close Read extraction before closing the current authority corridor

This matches the trajectory from April 4 (Close Read became the explicit product target) through April 9 (host persistence closed) to now (artifact authority closeout).

---

## What the Memo Gets Wrong or Overstates

### Correction 1: "analyzer-mgmt already has a concept-artifact-specific job-level surface" is overstated

**Evidence:**

The analyzer-mgmt job page (`/jobs/[id].tsx`) has these tabs:
- Summary, Manifest, Decision Trace, Page Structure, The-Critic Steering, Result Boundary

None of these tabs contain concept-specific or artifact-authority-specific content. The page is a generic executor job viewer. It does not currently surface:
- `contract_validation_status`
- `lookup_mode`
- `analysis_mode`
- concept name
- `_artifact_authority` metadata
- translated host artifact preview
- translation template linkage

Furthermore, the April 10 Codex review confirmed that the generic result/run surfaces show this concept job as "preparing" with `artifacts_ready = false` and `artifact_families = []`, and the generic presenter status misleadingly surfaces genealogy-shaped views for a concept logical job.

**Impact on the memo:**

Phase 4 lists specific "required fields on the job page" (validation status, lookup mode, analysis mode, concept, analyzer-v2 job id, etc.) and says "verify in browser." But these fields don't exist on the current page. Phase 4 is actually "build and verify," not just "verify."

The memo should acknowledge this explicitly. It does partially hedge with "fix only the narrow seam that the failure identifies," but the Phase 4 description reads as if the concept-artifact surface already exists and just needs checking.

**Recommended fix:** Change Phase 4's framing from "verify in browser that the analyzer-mgmt job page shows concept artifact authority correctly" to "extend the analyzer-mgmt job page to surface concept artifact authority metadata, then verify in browser." This is still bounded work — it's adding a card or panel to an existing page, not a redesign.

### Correction 2: The memo should explicitly acknowledge the deployed the-critic cutover state

**Critical finding:** The-critic's `origin/master` (deployed on Render) is **17 commits ahead** of the local HEAD. The deployed code includes:

| Commit | Description |
|--------|-------------|
| `f33789f` | Cut concept analysis over to analyzer-v2 runtime |
| `dc8ed0e` | Fetch exact concept artifacts from analyzer-v2 |
| `7ddcff9` | Read concept artifacts through analyzer authority |
| `debec5b` | Harden translated concept artifact cutover |
| `8ecec9d` | Fix concept artifact readback authority identity |
| `ac2cb52` | Align concept analysis uniqueness with project scope |

The deployed the-critic code:
1. Launches concept analysis through analyzer-v2 by-ref
2. After job completion, reads the **already-translated artifact** from analyzer-v2's authority route (not from local translation)
3. Validates the artifact identity through `_validated_translated_concept_artifact()` — fail-closed on any mismatch
4. Adds `_artifact_authority` metadata with hosted authority URL and stable artifact hash
5. Persists a compatibility copy to local DB

This is a **materially thinner** host than what the previous reviews described. The deployed the-critic no longer runs local translation from raw phase outputs. It reads pre-translated artifacts from analyzer-v2 and validates them.

The memo says "the-critic already reads through analyzer-v2 authority for the admitted seam" — this is correct. But it doesn't specify that the deployed code already includes the full identity-validated read-through path. The memo should be more precise: the-critic's cutover is **already deployed**, not pending.

### Correction 3: Local-vs-live divergence is more severe than the memo acknowledges

The memo correctly warns about local/live divergence in Phase 1 and Decision 1. But the actual divergence is larger than implied:

| Repo | Local HEAD behind origin/master | Dirty working tree |
|------|--------------------------------|-------------------|
| analyzer-v2 | 11 commits | 125 files, ~11,765 insertions |
| the-critic | 17 commits | 59 files, ~11,605 insertions |
| analyzer-mgmt | 0 commits | 13 files, ~1,138 insertions |

All three repos have dirty working trees. The analyzer-v2 and the-critic local checkouts are significantly behind their deployed state. The deployed code contains the concept-artifact-authority implementation that the local code does not.

**Operational implication:** The memo's Phase 1 instruction to "use isolated worktrees or deployed-source-aligned branches" is absolutely correct and should be treated as non-negotiable. Running the fresh proof from the dirty local trees would be working against outdated code.

### Correction 4: The April 10 reviews' code-backed findings about the-critic are partially stale

Both the Codex and Claude April 10 reviews described the-critic as "still owning translation/persistence/readback" with local `analyzer_v2_recomposition.py` doing the translation. That was accurate for the **local checkout** at the time, but the **deployed code** (origin/master) had already been cut over by then (commits like `f33789f`, `7ddcff9` are on origin/master).

The April 11 memo should acknowledge this explicitly: the code-backed critique from April 10 was based on local code that was already behind the deployed state. The deployed the-critic is thinner than those reviews described.

---

## Direct Answers to Requested Questions

### Does the memo correctly read the current state as "substantially implemented but not yet cleanly closed," or is that framing materially wrong?

**Correct.** The live stack confirms: exact-run authority works, latest-validated authority works, the-critic read-through works with full `_artifact_authority` metadata, scrutiny works. What's missing is a fresh proof on a new project (especially inferential, which has never been proven), and formal closeout docs. "Substantially implemented but not yet cleanly closed" is the honest reading.

### Is the proposed next tranche correctly scoped as a live closeout tranche rather than new architecture invention?

**Yes.** The memo explicitly starts from deployed reality and proposes proof-and-verification, not invention. The one exception is the analyzer-mgmt job page, which genuinely needs new surface work (see Correction 1). But even that is bounded: adding a concept-artifact panel to an existing page, not building a new console.

### Does the memo keep the larger Close Read direction clear enough?

**Yes.** The memo maintains:
- analyzer-v2 as the brain: confirmed by the live translated-artifact authority route
- hosts as thinner shells: confirmed by the deployed the-critic cutover to read-through authority
- Close Read as the app/product layer: correctly deferred to after closeout

The strategic hierarchy is intact: close the current corridor before opening the next.

### Is a fresh brand-new project proof the right next requirement, or does the memo over-index on reproving work that is already sufficiently closed?

**It is the right requirement.** Three reasons:

1. Post-fix code changes (authority URL canonicalization, concept identity normalization in commits `8ecec9d`, `1b06e09`) have not been proven on a fresh project
2. Inferential mode has **never been proven through the translated-artifact-authority path** — confirmed by live 404 on the baseline project
3. The April 9 specimen was created before the final authority-URL and canonical-concept fixes

A fresh proof is not redundant. It is the minimum honest closeout evidence.

### Does the memo keep the tranche bounded tightly enough to `inferential`, `logical`, analyzer-mgmt job surfaces, and the-critic read-through semantics?

**Yes.** The boundaries are explicit and correct. No new concept submodes, no cross-corpus work, no broader console redesign, no standalone extraction. The out-of-scope list is comprehensive.

### Does it avoid reopening already-closed host persistence and scrutiny diagnosis unnecessarily?

**Yes.** Scrutiny is bounded to one fresh quick run as a regression check. Host persistence is treated as closed. The memo explicitly warns against "reopening already-cleared host debugging corridors."

### Is the analyzer-mgmt responsibility framed correctly?

**Partially.** The framing of "job pages as the proof surface, implementation pages as composition metadata" is correct. But the current job page does not have the concept-artifact surface the memo assumes. Phase 4 should be reframed as "build and verify" rather than just "verify." This is still tightly bounded work — not a redesign.

### Does the memo make the analyzer-v2 to analyzer-mgmt to the-critic identity/provenance trail concrete enough to implement and verify?

**Yes.** The identity model is concrete and already proven live:
- analyzer-v2: `consumer_key`, `external_project_id`, `concept_name`, `analysis_mode`, `analyzer_v2_job_id` → translated artifact with `contract_validation_status`, `produced_at`, workflow/chain/template provenance
- the-critic: reads from analyzer-v2 authority, validates identity match, adds `_artifact_authority` with `authority_url`, `artifact_hash`, and full provenance
- analyzer-mgmt: should surface these fields on the job page (currently missing — see Correction 1)

### Does the memo remain honest about local-vs-live divergence in analyzer-v2?

**It acknowledges the issue but understates its severity.** The divergence is not just "dirty trees" — all three repos have their local checkouts significantly behind the deployed code. The concept-artifact-authority implementation exists on deployed origin/master but not in local checkouts. The memo should quantify this (see Correction 3).

### Is there any place where the memo understates or overstates what is already live today?

**Two places:**

1. **Overstates analyzer-mgmt:** Claims "analyzer-mgmt already has a concept-artifact-specific job-level surface" — the current job page is generic with no concept-specific fields.

2. **Slightly understates the-critic thinning:** The deployed the-critic is already materially thinner than implied. It already reads pre-translated artifacts from analyzer-v2 authority with identity validation and fail-closed behavior. This is not pending work — it's deployed reality.

### If you were trying to keep roadmap discipline, is this the right next move before any broader Close Read extraction or new family work?

**Yes.** This is exactly the right move. The corridor is 90% built. Closing it cleanly before opening a new one is the disciplined choice. Jumping to broader extraction or new family work would leave an almost-closed corridor in an ambiguous state, which makes future roadmap questions harder.

---

## Code-Backed Findings Summary

### analyzer-v2 (deployed on `origin/master`, 11 commits ahead of local)

| Component | Status | Evidence |
|-----------|--------|----------|
| `concept_artifact_authority.py` | **Deployed, live** | ~1200 lines: full translation, normalization, persistence, read authority |
| `concept_host_contracts.py` | **Deployed** | Pydantic models for `InferentialAnalysisResult`, `LogicalAnalysisResult` |
| `concept_translated_artifacts` table | **Deployed, populated** | Live route returns artifact for baseline specimen |
| `/concept-analysis-by-ref/result` route | **Live, working** | Both `exact_run` and `latest_validated` confirmed |
| `concept_by_ref.py` (launch) | **Live** | Builds plan, stores documents, creates job |

### the-critic (deployed on `origin/master`, 17 commits ahead of local)

| Component | Status | Evidence |
|-----------|--------|----------|
| `_validated_translated_concept_artifact()` | **Deployed** | Reads from analyzer-v2 authority, validates identity, adds `_artifact_authority` |
| `_concept_artifact_authority_url()` | **Deployed** | Builds hosted analyzer-v2 authority URL |
| `_run_rebased_concept_analysis()` | **Deployed, cut over** | Launches → polls → fetches from analyzer-v2 authority (NOT local translation) |
| `_artifact_authority` in readback | **Live, confirmed** | Hash: `b88a09...`, `source_owner: "analyzer-v2"`, hosted authority URL |
| Fail-closed validation | **Deployed** | Mismatches on consumer, project, concept, mode, job_id, or provenance raise RuntimeError |

### analyzer-mgmt (local matches deployed)

| Component | Status | Evidence |
|-----------|--------|----------|
| Jobs page (`/jobs/[id].tsx`) | **Generic** | Tabs: Summary, Manifest, Decision Trace, Page Structure, Steering, Result Boundary — no concept-specific fields |
| Implementations page (`/implementations/[key].tsx`) | **May fail** for concept workflows (Codex April 10 reported "Failed to load implementation" for `concept_logical_single_concept`) |
| Concept artifact surface | **Does not exist** | No current page shows translated artifacts, validation status, or artifact-authority metadata |

---

## What This Means for Implementation Sequence

The memo's 6-phase sequence is structurally sound but should be adjusted:

**Phase 1 (baseline verification and source alignment):** Correct and important. Must use clean worktrees aligned to deployed `origin/master` for all three repos. The dirty local trees cannot be trusted.

**Phase 2 (fresh logical proof):** Correct. No changes needed. This is genuine new proof work.

**Phase 3 (fresh inferential proof):** Correct and genuinely new. No inferential artifact exists on any project through the authority path. This is the most valuable new evidence in the tranche.

**Phase 4 (analyzer-mgmt browser-backed proof):** Needs reframing. The required concept-artifact fields do not exist on the current job page. This phase must include building the surface, not just verifying it. This is still bounded — it's a concept-artifact card on an existing page, not a console redesign.

**Phase 5 (fix seams):** Correct. The graduated fix strategy is sound.

**Phase 6 (closeout docs):** Correct. Essential for roadmap discipline.

---

## Tightened Bottom Line

**Approve with corrections.**

The memo is the right next move. It reads the current state honestly, proposes the right closeout discipline, and maintains the larger "analyzer-v2 as the brain, hosts as thin shells" trajectory. The corrections are:

1. **Reframe analyzer-mgmt Phase 4 as "build and verify"** — the concept-artifact surface does not exist yet and must be created before it can be verified in browser. This is bounded work (a card/panel on an existing page), not a redesign.

2. **Acknowledge the deployed the-critic cutover explicitly** — the deployed the-critic already reads from analyzer-v2 authority with full identity validation and fail-closed behavior. This is not future work. The fresh proof will exercise this already-deployed path.

3. **Quantify the local-vs-live divergence** — analyzer-v2 is 11 commits behind, the-critic is 17 commits behind, both have massive dirty working trees. The Phase 1 instruction to use isolated worktrees is non-negotiable.

4. **Note that the April 10 review findings about the-critic are partially stale** — both reviews described the-critic as still owning local translation, but the deployed code had already been cut over. The April 11 memo's assessment of the-critic's deployed state is more accurate than the April 10 reviews' code-backed findings.

With these corrections, the tranche is honest, bounded, and implementable. It closes the current corridor cleanly and creates the stable precedent needed for future Close Read work.
