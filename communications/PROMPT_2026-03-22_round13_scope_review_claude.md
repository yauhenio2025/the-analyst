Review this memo critically:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md`

Your job is to act as an external architecture reviewer, not a rubber stamp.

Goals:

1. test the robustness of the memo’s assumptions
2. examine whether the round-13 direction fits the larger thin-consumer / analyzer-as-brain roadmap
3. scrutinize the memo’s claims against the actual codebase
4. read any relevant recent memos or docs that materially bear on the decision
5. identify what should be revised before anyone writes an execution plan

You should inspect at least these references:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `/home/evgeny/projects/analyzer-v2/communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`

And inspect the code seams most relevant to the memo’s assumptions:

- analyzer-v2 transient compose route and transient contract
  - `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
  - `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- the-critic transient proof host
  - `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentExamples.ts`
- the-critic AOI v2 saved-result / thinker-context seams
  - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts`
  - `/home/evgeny/projects/the-critic/api/server.py`

Questions to answer explicitly:

1. Is “source-backed transient launch” really the next contradiction, or is the memo skipping a more urgent seam?
2. Is the proposed consumer-side proxy / bridge the right boundary, given that saved AOI results live in the-critic today?
3. Are the memo’s assumptions about saved AOI source material actually being available for the `dossier` and `comparison` profiles supported by the current code and persisted result shapes?
4. Does the memo stay honest about what remains blocked: persistence, workspace unification, genealogy, and generic multi-workflow source bridging?
5. Does the proposal fit the larger platform direction, or does it risk re-thickening the consumer in a way the memo is underestimating?
6. Are there missing failure modes, lifecycle concerns, or proof-standard requirements that should be explicit before implementation planning?

Instructions:

- Be concrete and cite files.
- Prioritize bugs, architectural contradictions, and unstated dependencies over stylistic commentary.
- If you think the memo is directionally right but needs revision, say “Approve after revision” and list the revisions.
- If you think the scope is wrong, say so plainly.
- If there are relevant docs in `/home/evgeny/projects/analyzer-v2/docs`, `/home/evgeny/projects/the-critic/docs`, or `/home/evgeny/projects/the-critic/webapp/docs`, use them.
- If you inspect those docs folders and find nothing materially relevant beyond the files above, say that explicitly.

Save your review to this exact file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Round13_AOI_Source_Backed_Transient_Launch_Scope_Critique_2026-03-22.md`

Do not modify code. Do not modify the scope memo. Only write the review report.
