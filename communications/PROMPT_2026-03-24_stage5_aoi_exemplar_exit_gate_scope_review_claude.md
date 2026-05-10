Please review this scope memo:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage5_aoi_exemplar_exit_gate_scope.md`

This is a docs-only strategy/code review. Do not modify application code.

Your task:

1. Test the robustness of the memo's assumptions.
2. Evaluate whether this is the right next step after:
   - the Stage 3/4 AOI exemplar cutover completion
   - the Stage 13 Tier A canary closeout
   - the broader Stage 3/4/5 AOI exemplar scope memo
3. Scrutinize the memo's claims against the live codebase in:
   - `/home/evgeny/projects/analyzer-v2`
   - `/home/evgeny/projects/the-critic`
   - `/home/evgeny/projects/aoi-canary` only where sequencing comparisons are useful
4. Re-read the most relevant recent memo trail:
   - the canonical roadmap memo
   - the draft next-platformization roadmap memo
   - the Stage 3/4/5 AOI exemplar scope memo
   - the new Stage 3/4 AOI exemplar cutover completion memo
   - the Stage 13 Tier A second-consumer completion memo
   - the dynamic bespoke apps vision memo
   - any obviously relevant recent AOI, Stage 3/4/5, Stage 5, Stage 8/9, or Stage 13 memos in `communications/`
5. Decide whether this scope is:
   - approved
   - approved after revision
   - not approved

Focus especially on:

- whether the memo correctly treats this as an exit-gate/evidence tranche rather than another architecture tranche
- whether Stage 5 really is the next honest step after Milestone A, or whether the program should still do more AOI structural work first
- whether the fixed four-case eval pack is the right shape:
  - evolution-focused
  - engagement-focused
  - locked non-profile
  - real `aoi_selection_blocked`
- whether the locked non-profile case is still the right forcing function, or whether it is underspecified or overclaimed
- whether the locked non-profile case now handles the readiness-discovery gap honestly enough
- whether the memo is strong enough about saving the full planning and launch trail:
  - route-task
  - plan-task
  - selected/rejected sources
  - provenance
  - compose request
  - rendered/blocked result
- whether the artifact-capture method is concrete enough given that the current code does not auto-persist audit packs
- whether the memo draws the right line between:
  - proving AOI as an exemplar loop
  - and overclaiming broader transient/platform closure
- whether the memo is honest enough about Stage 2:
  - not silently closed
  - but eligible to close as a side-effect only if the eval pack earns it
- whether the memo now defines strong enough non-closure conditions for Stage 2
- whether the memo names the remaining host residuals and refresh/deep-link continuity honestly enough
- whether fixture-backed proof cases are acceptable for this exit gate, and whether the fixture-strength tiers are defined sharply enough
- whether the rubric timing and threshold shape are strong enough to resist post-hoc self-certification
- whether the latency/responsiveness breakdown is concrete enough
- whether the tranche is missing any essential deliverables, thresholds, or hidden prerequisites
- whether the exit evidence is strong enough to justify moving the main program line to later transient-substrate generalization afterward

Please save your review to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_STAGE5_AOI_Exemplar_Exit_Gate_Scope_Critique_2026-03-24.md`

Preferred output shape:

- verdict
- findings ordered by severity
- open questions
- judgment on sequencing and bigger-picture fit
- concrete revisions recommended before implementation
