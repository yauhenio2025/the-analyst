# Critique: Fixed Direction Phased Roadmap From The Brain Audit

Date: 2026-03-26
Reviewer: Claude (Opus 4.6, 1M context)
Document under review: `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
Supporting material reviewed:
- `communications/MEMO_2026-03-26_analyzer_v2_as_brain_direction_audit.md`
- `communications/MASTER_BIG_ROADMAP_MEMO_ANALYZER_V2_AS_THE_BRAIN_FOR_DYNAMIC_BESPOKE_ANALYTICAL_APPS.md`
- `communications/MEMO_2026-03-24_draft_next_platformization_stages_roadmap.md`
- `communications/MEMO_2026-03-24_stage13_minimal_generic_host_contract_completion.md`
- `communications/MEMO_2026-03-24_stage8_9_host_adoption_task_launch_completion.md`

Code inspected:
- `src/api/routes/orchestrator.py`
- `src/orchestrator/task_router.py`
- `src/orchestrator/task_planner.py`
- `src/presenter/compose_from_intent.py`
- `/home/evgeny/projects/the-critic/webapp/src/lib/hostContractV1.ts`
- `/home/evgeny/projects/the-critic/webapp/src/lib/taskLaunchRuntime.ts`
- `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`

---

## Verdict: Approve After Revision

The roadmap is the best strategic document this program has produced. Its phase ordering is sound, its anti-drift rules are the strongest guardrails the program has had, and its core thesis — that AOI exemplar completion should be the last major AOI-specific gate before generalization becomes the main line — is correct.

But the roadmap understates three structural realities that would make literal execution harder than it reads. Those need to be addressed through revision, not by rejecting the document.

---

## Strongest Findings

### 1. Phase 1 is correct but hides at least three distinct engineering problems behind one label

The roadmap says Phase 1 must land:

- removing hard structural dependence on `workflow_key == AOI_WORKFLOW_KEY`
- removing hard structural dependence on `consumer_key == the-critic`
- clearer separation between host-neutral law and composition-facing law
- clearer relation between task-launch and Host Contract v1

That is strategically correct. But code inspection reveals these are not one task. They are three:

**Problem A: Compose-entry generalization.**
`src/presenter/compose_from_intent.py` has explicit `raise ValueError` guards at lines ~497-503, ~534-540, ~548-554 for all three compose entry points (`compose_from_intent`, `compose_from_source`, `compose_from_selection`). Those guards are the simplest to remove mechanically. But behind them sit AOI-specific role-to-pattern mappings (`_LEAF_PATTERN_BY_ROLE` at lines ~61-115), AOI-specific engine-to-role mappings (`_ROLE_FROM_ENGINE_KEY`), and AOI-specific source family constants imported from `composition_source_bridge.py`. Removing the guards without replacing the semantic dispatch would leave a nominally open endpoint that can only compose AOI content. The file contains ~900 lines of deeply AOI-shaped composition logic — "removing the guard" is a one-line change; replacing the semantic dispatch underneath is a substantial refactoring.

**Problem B: Router/planner generalization.**
`src/orchestrator/task_router.py` has hardcoded signal pools at lines ~23-43 (`SUPPORTED_OBJECTIVES = ("influence_thematic", "genealogical")`, plus `AOI_SIGNALS` and `GENEALOGY_SIGNALS` keyword tuples), hardcoded source-mode compatibility rules per objective, and a three-way switch in `_supported_outcome()` and `_build_launch_contract()`. `src/orchestrator/task_planner.py` dispatches on `selected_objective_key == "influence_thematic"` vs `"genealogical"` at lines ~127-141, with entirely different planning paths per objective — including AOI-specific LLM source selection, profile-family compatibility checking (`_AOI_PROFILE_FAMILY_SETS`), and AOI-specific validation and error codes (`_AoiSelectionBlocked`). This is not the same engineering problem as removing the compose-entry guard. Adding a third objective requires touching routing logic, planning logic, source-family definitions, and launch-contract builders at every decision point.

**Problem C: Host Contract v1 / task-launch unification.**
`hostContractV1.ts` documents that `transient_compose_from_intent` and `source_backed_transient_launch` use `structural_constant` consumer-key binding (locked to `the-critic`), while `taskLaunchRuntime.ts` sits beside the host contract as a separate layer. Unifying these is a contract-design problem, not a code-removal problem — changing it requires a v2 host contract, not just a code fix.

**Recommendation:** Phase 1 should be explicitly decomposed into at least two sub-phases: (1a) de-couple compose entry from single-workflow / single-consumer guards, which includes replacing the AOI-specific semantic dispatch with a registry-driven or workflow-parametric dispatch; and (1b) unify task-launch and Host Contract v1 into one coherent analyzer-to-host story. The router/planner generalization may belong in either sub-phase or in Phase 2, depending on whether the program decides the router needs to support a third objective before the second-consumer proof.

Phase 1's "must land" items should also be tiered:
- **Must ship** (code-verifiable): Remove the hard workflow/consumer locks from transient compose.
- **Must decide** (can be a decision memo): What the separation between run/result law and composition law looks like. This does not need to be fully implemented before Phase 1 closes.

### 2. The anti-drift rules are the strongest guardrails the program has had, but Rule 4 needs a time-bound and the rules need a prospective enforcement mechanism

Rule 4 says AOI-specific work is allowed only while it is required to close the Stage 2 honesty gate. But it does not specify what happens if the Stage 2 gate does not close cleanly after the fresh rerun.

The audit correctly identifies that the previous run's recovered payload still contains contradictory raw Phase 1.0 identities and downstream O'Neill-centered prose. If the fresh post-fix rerun produces similar contamination — say from a different source engine or a different context-length bottleneck — the program could re-enter an open-ended AOI repair cycle under the authority of "we need an honest exemplar judgment" without any hard cutoff.

More broadly, the four rules are excellent in content but the memo provides no enforcement mechanism. The program's actual operational pattern is scope memos reviewed by Claude and Codex, followed by implementation sessions. There is no stated mechanism for applying the anti-drift filter *before* a scope memo is written. The practical risk is that a future session sees a real bug, writes a scope memo to fix it, gets two reviewer approvals, implements it, and only realizes afterward that the fix was downstream compensation that should have been an upstream repair.

**Recommendation:**
- Rule 4 should include a time-bound or scope-bound escape clause: if the fresh post-fix rerun does not produce closure-grade evidence after one honest attempt, the Stage 2 decision should still be written — as a documented bounded failure — and the program should proceed to Phase 1 anyway. The exemplar would then be reclassified as "strong bounded proof with known contamination residue" rather than "closure-grade reference." The roadmap should explicitly say that Phase 1 generalization does not require a clean AOI exemplar; it only requires that whatever the exemplar shows is documented honestly.
- Add a meta-rule: "Before writing a scope memo for any proposed slice, apply the four-question prioritization filter from the bottom of this roadmap. If the answer pattern is mostly 'no,' the scope memo should not be written." This converts the rules from retrospective guidance to a prospective gate.
- Add a fifth anti-drift rule addressing *lateral drift*: "Upstream improvements that deepen workflow-specific coupling are not upstream improvements. They are lateral drift that makes future generalization harder." Without this, work that satisfies the letter of "moves analytical decision-making upstream" but does so for a narrow AOI-shaped case (e.g., adding a new AOI-specific source family to the composition bridge) could be defended under Rules 1-4 while actually deepening coupling.

### 3. The roadmap correctly identifies current apps as proving harnesses, but the code reality is that `the-critic` is also the only integration test surface

The roadmap says `the-critic` is a proving harness, not the destination architecture. That is strategically correct.

But the code reality reveals a practical dependency the roadmap underplays: `AoiV2ThematicPanel.tsx` is not just a thin consumer. It is the only place where `routeTask()`, `planTask()`, readiness-gated launch, planner profile law enforcement, and compose-from-selection all converge into a real end-to-end path that a human can exercise in a browser. It contains hardcoded AOI constants (workflow key, page key, phase count, surface key at lines ~35-39), hardcoded `objective_hint: 'influence_thematic'` and `consumer_key: 'the-critic'` in its `routeTask()` calls, and profile-specific launch UI (`ComposeProfile = 'dossier' | 'comparison'`).

If Phase 1 generalizes the upstream substrate without simultaneously maintaining or replacing this integration surface, the program will lose its only honest proof mechanism. The roadmap's "must not widen" constraint on Phase 1 says "do not turn this into 'make all current apps support everything.'" That is correct. But it should also say: "do not break the existing integration test surface without a replacement."

**Recommendation:** Phase 1 should include an explicit exit gate: the de-coupled compose substrate must be exercisable through at least one real browser path (either a slimmed-down `the-critic` path, or a minimal test harness, or a restructured `aoi-canary` path) before it can be declared complete. Otherwise the program will generalize the contract without being able to verify it.

---

## Discussion Of The Five Evaluation Questions

### Q1: Is the phase ordering strategically correct?

**Yes.**

Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 is the right order.

The most tempting wrong move would be jumping from Phase 0 directly to lifecycle (Phase 3) because lifecycle feels like a natural follow-on to "we have one exemplar." The roadmap correctly rejects this because lifecycle semantics would solidify around bounded AOI proof routes rather than around the intended platform.

The second tempting wrong move would be attempting Phase 2 (host-neutral proof) before Phase 1 (bridge generalization). The roadmap correctly rejects this because proving host-neutrality on a structurally AOI-locked substrate would force the second consumer to re-encode AOI assumptions, which is the opposite of generalization.

The roadmap also correctly collapses the older draft's Tranche 1 (Stage 13 Tier A / aoi-canary) out of the critical path, since that tranche is already documentary-closed, and subsumes the older Tranche 2 (AOI exemplar loop) into Phase 0 narrowly.

### Q2: Does the memo correctly distinguish what moved upstream, what is host-owned, and what is accidental coupling?

**Yes, and this is the strongest analytical contribution of the supporting audit.**

The audit's identification of five accidental AOI/the-critic coupling points — all confirmed by code inspection — is honest and precise:

1. `compose_from_intent.py` hard-locks workflow_key (confirmed: `AOI_WORKFLOW_KEY` guard at lines ~497, ~534, ~548)
2. `compose_from_intent.py` hard-locks consumer_key (confirmed: `TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"` at line 54)
3. Task routing resolves to three fixed outcomes for two fixed objectives (confirmed: `SUPPORTED_OBJECTIVES = ("influence_thematic", "genealogical")` in `task_router.py` line ~21)
4. AOI handoff metadata is rich but AOI-shaped (confirmed: `_AOI_PROFILE_FAMILY_SETS`, `_AoiSelectionBlocked` in `task_planner.py`)
5. The-critic still knows it is on an AOI page (confirmed: hardcoded `objective_hint: 'influence_thematic'`, `ComposeProfile = 'dossier' | 'comparison'`, and AOI surface keys in `AoiV2ThematicPanel.tsx`)

The fixed-direction roadmap references these distinctions but does not repeat the specific code locations inline. This matters because Phase 1 targets the accidental coupling, and implementors will need to know exactly which files and lines contain it.

**Recommendation:** Phase 1's scope should include explicit file references or reference the audit's code-backed classification.

### Q3: Are the anti-drift rules strong enough?

**Almost.** Rules 1-3 are strong. Rule 4 needs the time-bound discussed above. The rules collectively need a prospective enforcement mechanism and a lateral-drift guard. See Finding 2.

### Q4: Does the roadmap preserve honest sequencing around the AOI exemplar gate without allowing AOI proof maintenance to consume the whole roadmap?

**Yes, provided the time-bound is adopted.**

Phase 0's scoping is right: one rerun, one honest grade, one decision memo. The exit test correctly admits failure as a valid exit ("either the AOI exemplar is now closure-grade enough to stand as a real bounded reference, or it is not, and the exact reason is documented without softening").

The one weakness is Phase 0's "must not widen" section, which says "do not reopen older host/browser seams unless the fresh rerun exposes a truly new blocking seam." The word "truly" is doing too much work. The program has historically been generous in classifying seams as "truly blocking." Consider tightening this to: "do not reopen older host/browser seams. If the rerun exposes a new seam, document it and defer the repair to Phase 1 or later."

### Q5: Would this roadmap materially increase the chance that analyzer-v2 becomes the brain?

**Yes, if followed literally with the revisions suggested.**

The roadmap's strongest strategic contribution is the explicit rejection of two tempting wrong paths:

1. Continuing AOI/the-critic-specific refinements as the main line after Stage 2
2. Jumping to lifecycle/governance before bridge generalization and host-neutral proof

Both of those paths would lead to the outcome the audit warns about: a stronger downstream presenter rather than the intended host-neutral intelligence layer.

The roadmap's identification of Phase 1 (bridge generalization) as the first major post-exemplar work item is the single most important strategic decision in this document. If the program does that, the trajectory toward "analyzer-v2 as the brain" becomes credible. If it skips or softens Phase 1, the program will likely ossify around a better but still AOI-shaped presentation layer.

---

## Aggressive Challenges

### Is Phase 0 still too much AOI gravity?

**No.** Phase 0 as written is appropriately scoped. One rerun and one honest grade is about as narrow as Phase 0 can get while remaining honest. The risk is not Phase 0's scope but the emotional pull — if the rerun shows residual problems, there will be strong pressure to "just fix one more thing." The must-not-widen section addresses this, but discipline needs to be real.

The exit test should be even more explicit: "This phase closes even if the exemplar is graded as 'bounded repaired proof' rather than 'closure-grade.' The grade itself is the exit evidence, not the quality of the grade."

### Is Phase 1 specific enough?

**No. This is the most important revision needed.** See Finding 1.

Two of Phase 1's four "must land" items are aspirational rather than testable:
- "clearer separation between host-neutral run/result/readiness law and composition-facing transient/source-backed law"
- "clearer relation between task-launch runtime and Host Contract v1"

"Clearer separation" and "clearer relation" are not exit tests — they are aspirations. Compare with the concrete first two bullets, which are verifiable in code (the `compose_from_intent.py` validators either exist or they don't).

### Are current apps being treated honestly as proving harnesses?

**Yes, and this is a genuine strength.** The memo repeatedly and explicitly says the-critic is a proving harness, not the destination. The question is whether future sessions internalize this or treat it as background noise. The anti-drift rules are the enforcement mechanism, and they need the prospective-gate upgrade.

### Is Stage 13 Tier B placed in the right phase?

**Yes.** Stage 13 Tier B (transient/host-neutral proof, not just result-backed) is correctly placed in Phase 2, after Phase 1 removes the structural AOI/the-critic locks. Attempting Tier B before Phase 1 would force the second consumer to re-encode current AOI assumptions, producing a fake proof.

The code makes this constraint concrete: `compose_from_intent.py` hard-rejects any `consumer_key != "the-critic"`. Tier B literally cannot be attempted until Phase 1 ships. The roadmap implies this but should state it explicitly.

### Should lifecycle or governance move earlier?

**No, with one caveat.** The memo's reasoning is correct: lifecycle before bridge generalization would lock semantics around current bounded proof routes.

The caveat: **a minimal lifecycle decision may need to happen before Phase 2** in order to prove host-neutral consumption. If a second consumer cannot launch a transient experience without some lifecycle semantics (ephemeral surface token, session identity), then Phase 2 will be blocked on Phase 3 work. The roadmap should acknowledge this dependency rather than assuming lifecycle can be fully deferred.

### Does the memo understate any code reality?

**Yes, two things.**

**First:** The task router (`task_router.py`) is not just "bounded to AOI and genealogy" — it is fundamentally a keyword-signal-counting heuristic. The `AOI_SIGNALS` and `GENEALOGY_SIGNALS` tuples at lines ~23-43 are its entire understanding of what a task means. Phase 1's bridge generalization will eventually need to address this, but the roadmap does not acknowledge the gap between "de-AOI the compose validators" (concrete, verifiable) and "de-AOI the task understanding layer" (requires a qualitatively different approach). The former is a guard removal; the latter requires replacing a heuristic with something richer.

**Second:** The master roadmap's canonical stage numbering (Stages 0-15) and the fixed-direction roadmap's phase numbering (Phases 0-4) do not map cleanly. Phase 1 spans canonical Stages 7, 8, 9, and 13 (partially). Phase 2 spans canonical Stage 13 (Tier B) plus broader Stage 7 proof. This is not wrong — the fixed-direction roadmap deliberately operates at a higher strategic level — but future sessions need to understand that "Phase 1 is complete" does not mean "Stages 7, 8, 9 are complete." The roadmap should include a mapping note.

---

## Bottom-Line Judgment

This roadmap is the best available direction right now.

It correctly identifies that the program must stop spending its main line on AOI/the-critic-specific repairs after one more honest exemplar judgment, and shift to bridge generalization and host-neutral proof. It correctly rejects the tempting shortcuts of jumping to lifecycle or governance before the structural bridge work is done. It correctly treats current apps as proving harnesses rather than destination products.

If Phase 1 ships with the hard-locks removed and a clear separation between run/result law and composition law, the system will be in a qualitatively different strategic position. The program will have crossed from "better bounded AOI presenter" to "actual generalizable architecture."

The revisions needed are:

1. Decompose Phase 1 into actionable sub-phases with code-verifiable exit tests
2. Add a time-bound escape clause to Rule 4 so Phase 0 cannot re-enter open-ended AOI repair
3. Add a prospective enforcement mechanism for the anti-drift rules (apply before scope memos, not just retrospectively)
4. Add an integration-testability exit gate to Phase 1 (don't break the only browser-exercisable proof path without a replacement)
5. Add a lateral-drift guard to the anti-drift rules
6. Acknowledge the engineering effort profile more honestly — the compose entry has ~900 lines of AOI-specific logic behind the guards, and the router is a keyword heuristic

None of these revisions change the phase ordering or the strategic direction. They make it more executable.

---

## Summary of Recommendations

| # | Recommendation | Priority |
|---|---|---|
| 1 | Decompose Phase 1 into sub-phases (1a: remove hard-locks + replace semantic dispatch, 1b: unify task-launch/host-contract) with tiered must-ship vs must-decide items | High |
| 2 | Add time-bound escape clause to Rule 4: Phase 0 closes on the grade, not on the quality of the grade | High |
| 3 | Convert anti-drift rules into a prospective gate: apply the 4-question filter before writing scope memos | High |
| 4 | Add Phase 1 integration-testability exit gate: don't generalize the contract without a way to verify it | Medium |
| 5 | Add lateral-drift anti-drift rule: upstream improvements that deepen workflow-specific coupling are lateral drift | Medium |
| 6 | Add explicit code file references to Phase 1's scope | Medium |
| 7 | Tighten Phase 0's "truly new blocking seam" language to "document and defer" | Medium |
| 8 | Note that Phase 2 may require a minimal lifecycle decision (technically Phase 3) to prove host-neutral consumption | Low |
| 9 | Add phase-to-canonical-stage mapping note | Low |
| 10 | Note that the task router is a keyword heuristic, not a task-understanding layer — distinct problem from compose-guard removal | Low |
