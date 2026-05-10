Review this memo critically:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md`

Treat this as a codebase-grounded architecture audit.

Goals:

1. pressure-test the memo’s assumptions against the actual implementation seams
2. check whether the proposed round-13 move is the best next step in light of the roadmap and recent completed rounds
3. identify any hidden coupling, missing prerequisite, or proof-hole that would make the scope misleading
4. verify whether recent docs and memos support or contradict the memo’s framing

You should inspect at least these materials:

- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`
- `/home/evgeny/projects/analyzer-v2/communications/DYNAMIC_BESPOKE_APPS_VISION.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`
- `/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md`
- `/home/evgeny/projects/the-critic/communications/MASTER_MEMO_CURRENT.md`
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`

And you should check these code seams directly:

- analyzer-v2 compose-from-intent route / contract
  - `/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py`
  - `/home/evgeny/projects/analyzer-v2/src/presenter/schemas.py`
- the-critic transient consumer adoption surface
  - `/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts`
  - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiComposeFromIntentShell.tsx`
- the-critic AOI v2 source/result seams
  - `/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx`
  - `/home/evgeny/projects/the-critic/webapp/src/utils/resultContract.ts`
  - `/home/evgeny/projects/the-critic/api/server.py`

Audit questions:

1. Does the memo correctly identify the hardcoded-example dependency as the main remaining contradiction after round 12?
2. Is a bounded the-critic backend proxy actually the right implementation seam, given where the saved AOI result data lives today?
3. Are the bounded `dossier` / `comparison` source profiles realistic from the current persisted AOI result payloads, or is the memo assuming source fields that are not actually durable?
4. Does the memo understate any risk of consumer re-thickening by moving result-to-compose mapping into the-critic?
5. Is there a narrower or cleaner next move the memo should choose instead?
6. Is the proof standard strong enough, and does it avoid silently falling back to round-12 hardcoded fixtures?

Instructions:

- Cite files and repo facts.
- Be blunt about missing prerequisites or architectural drift.
- If the memo is mostly right but needs tightening, say “Approve after revision”.
- If you find relevant material in `/home/evgeny/projects/analyzer-v2/docs`, `/home/evgeny/projects/the-critic/docs`, or `/home/evgeny/projects/the-critic/webapp/docs`, use it.
- If those docs folders do not materially change your conclusion, say so.

Save your audit to this exact file:

- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Codex_Round13_AOI_Source_Backed_Transient_Launch_Scope_Audit_2026-03-22.md`

Do not modify code. Do not modify the scope memo. Only write the audit report.
