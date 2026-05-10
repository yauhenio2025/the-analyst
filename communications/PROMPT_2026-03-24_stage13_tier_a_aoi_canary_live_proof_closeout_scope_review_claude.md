Please review this scope memo:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`

This is a docs-only strategy/code review. Do not modify application code.

Your task:

1. Test the robustness of the scope memo’s assumptions.
2. Evaluate whether this is the right immediate next step after the Tier A canary implementation.
3. Scrutinize the memo’s claims against the live codebase in:
   - `/home/evgeny/projects/analyzer-v2`
   - `/home/evgeny/projects/aoi-canary`
   - `/home/evgeny/projects/the-critic` where relevant for broader sequencing or comparison
4. Re-read the most relevant recent memo trail:
   - the canonical roadmap memo
   - the draft next-platformization-stages roadmap memo
   - the Tier A canary scope memo
   - the Tier A canary completion memo
   - any obviously relevant recent AOI or Stage 13 memos in `communications/`
5. Decide whether this scope is:
   - approved
   - approved after revision
   - not approved

Focus especially on:

- whether the memo is right to treat the remaining gap as proof closeout rather than another architecture tranche
- whether discovery-first live proof is the correct acceptance seam
- whether the proposed live evidence set is strong enough to count as Tier A closeout
- whether the evidence set is specific enough at the request level, not only at the screenshot/memo level
- whether one negative-state proof is necessary and sufficient
- whether the allowed out-of-band data-prep move (`attach-project`) is framed honestly as limited pre-proof setup rather than part of the acceptance seam
- whether thinker-scoped discovery needs to be explicit if the proof aims to reproduce a pinned thinker path
- whether the memo is honest about the difference between proving the contract seam and proving stronger preparation/polish quality
- whether the memo is too narrow and risks producing “memo closure” without real proof
- whether the memo is too broad and risks drifting into Tranche 2 AOI exemplar work
- whether any hidden live-environment or data prerequisites are missing
- whether the roadmap sequencing is right:
  - close Tier A live proof first
  - then move the main structural line to AOI exemplar completion

Please save your review to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_STAGE13_TierA_AOI_Canary_Live_Proof_Closeout_Scope_Critique_2026-03-24.md`

Preferred output shape:

- verdict
- findings ordered by severity
- open questions
- judgment on whether this is the right immediate next step
- concrete revisions recommended before implementation
