Audit this scope memo against the real code and recent strategy trail:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-24_stage13_tier_a_aoi_canary_live_proof_closeout_scope.md`

This is a docs-only audit. Do not change application code.

What to do:

1. Audit the memo’s assumptions against the live codebase in:
   - `/home/evgeny/projects/analyzer-v2`
   - `/home/evgeny/projects/aoi-canary`
   - `/home/evgeny/projects/the-critic` where useful for sequencing comparisons
2. Check whether the memo accurately reflects:
   - the current `aoi-canary` implementation
   - the actual remaining Tier A gap after implementation
   - the live analyzer result-contract route shape
   - the real difference between proof closeout and a new architecture tranche
3. Re-read the relevant recent memos in `communications/` and `docs/`, especially:
   - the canonical roadmap memo
   - the draft next-platformization-stages roadmap memo
   - the Tier A canary scope memo
   - the Tier A canary completion memo
   - recent Stage 13 and AOI-related memos if they materially affect sequencing honesty
4. Evaluate whether this is the right next step, or whether:
   - Tier A should already be considered closed without more live proof
   - the remaining work should be folded into AOI exemplar completion instead
   - the scope omits essential live-proof prerequisites or evidence requirements
   - the negative-proof requirement is under- or over-scoped

Key questions to answer:

- Is the memo honest about what remains after the canary implementation?
- Is a bounded live proof artifact set really the next missing seam?
- Is the discovery-first live path the correct acceptance path?
- Does the scope correctly keep manual `job_id` in debug-only territory?
- Is the `attach-project` pre-proof move framed correctly as limited setup rather than part of the acceptance seam?
- If the intended proof is thinker-scoped, does the memo make that prerequisite explicit enough?
- Is at least one negative-state proof required to support the “no silent artifact fallback” claim?
- Is the evidence set request-specific enough to support later audit, not just screenshot-specific?
- Does the memo draw the right line between proving the contract seam and proving stronger preparation/polish quality?
- Is the proposed evidence set strong enough to justify moving the roadmap’s main line to the AOI exemplar tranche afterward?
- Does the memo avoid accidentally reopening transient, task-launch, or shared-runtime work?

Please save your audit to:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_STAGE13_TierA_AOI_Canary_Live_Proof_Closeout_Scope_Audit_2026-03-24.md`

Preferred output shape:

- overall verdict
- concrete findings with code/memo references
- scope/sequence assessment
- missing assumptions or hidden prerequisites
- recommended revisions before implementation
