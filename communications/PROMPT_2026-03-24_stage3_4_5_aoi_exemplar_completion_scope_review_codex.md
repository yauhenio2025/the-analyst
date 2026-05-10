Audit this scope memo against the real code and recent strategy trail:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage3_4_5_aoi_exemplar_completion_scope.md`

This is a docs-only audit. Do not change application code.

What to do:

1. Audit the memo's assumptions against the live codebase in:
   - `/home/evgeny/projects/analyzer-v2`
   - `/home/evgeny/projects/the-critic`
   - `/home/evgeny/projects/aoi-canary` where useful for sequencing comparison
2. Check whether the memo accurately reflects:
   - the current AOI planner-backed seam
   - the residual profile-first behavior still visible in the-critic
   - the actual limits of `taskLaunchRuntime.ts` and the current AOI handoff contract
   - the difference between the richer backend AOI handoff schema and the thinner host-consumed seam
   - the absence or presence of AOI evaluation/ops infrastructure
   - the real difference between AOI exemplar completion and later transient-substrate generalization
3. Re-read the relevant recent memos in `communications/` and `docs/`, especially:
   - the canonical roadmap memo
   - the draft next-platformization-stages roadmap memo
   - the Stage 8/9 host-adoption completion memo
   - the Stage 13 Tier A second-consumer completion memo
   - the Stage 13 Tier A live proof closeout proof note
   - the dynamic bespoke apps vision memo
   - any recent AOI or Stage 3/4/5 related memo that materially affects sequencing honesty
4. Evaluate whether this is the right next phase, or whether:
   - the tranche should be split before implementation
   - Stage 3 should be scoped without Stage 4/5
   - Stage 5 guardrails should be deferred
   - de-AOI transient generalization should come first instead
   - the memo overstates what the current AOI substrate can support

Key questions to answer:

- Is the memo honest about the current AOI residuals in code?
- Is one planner-primary AOI proof path the right bounded deliverable?
- Does the memo now handle canonical Stage 2 honestly?
- Is the effective host-consumed `allowed_profiles` / `blocked_profiles` seam still too thin to count as Stage 3/4 closure even though the backend schema is richer?
- Does the memo draw the right line between bounded AOI source/product-selection law and broader engine-graph planning?
- Is the memo explicit enough that any proof case not reducible to `dossier` / `comparison` requires public contract changes?
- Is it correct to treat Stage 5 evaluation/ops work as part of this tranche rather than a later cleanup?
- Is keeping legacy AOI controls outside the proof slice the right bounded transition strategy?
- Does the memo now name hidden prerequisites in analyzer-v2 or the-critic clearly enough, especially:
  - host-proxy identity translation
  - snapshot warmup
  - compose-from-source contract locks
- Does this sequencing fit the larger platform objective, or is there a stronger alternative next move?
- Is the exit evidence strong enough and specific enough?
- Is the memo honest about what remains open even after this tranche lands?

Please save your audit to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_STAGE3_4_5_AOI_Exemplar_Completion_Scope_Audit_2026-03-24.md`

Preferred output shape:

- overall verdict
- concrete findings with code/memo references
- scope/sequence assessment
- missing assumptions or hidden prerequisites
- recommended revisions before implementation
