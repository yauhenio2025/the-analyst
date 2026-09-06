# Codex, resume: finish the cohort design run (6 Sep 2026, 18:15)

Your previous run (`CODEX_PROMPT_cohort_dimension_2026-09-06.md`) ended abruptly after writing patches 030 and 031. Your worktree is
`/tmp/the-analyst-cohort-2026-09-06` on branch `codex/cohort-design-2026-09-06`; Claude committed your uncommitted files there as they were
(fixtures, build_fixtures.py, patches 030/031, the harness test). Work THERE (`cd /tmp/the-analyst-cohort-2026-09-06`), on that branch.

The same hard constraint holds: the Riley → Weber pilot (now `dossier-bdc5eb48c407`) is in its analysis phase in the main tree; its later
phases read the citation engine YAMLs when they start. Do not modify any existing file under `src/executor/`, `src/dossier/`,
`src/engines/`, `src/operationalizations/`, `src/sources/` or `scripts/` in either tree. New files under `communications/study/cohort_2026_09_06/`
(and patches for the rest) only. Commit per phase on your branch; do not push; do not merge.

Remaining deliverables, in order:

1. The deferred design-note patches your memo lists but did not write: `patches/010_engagement_design_notes.patch`,
   `patches/011_reception_design_notes.patch`, `patches/012_fidelity_design_notes.patch` (each against both the capability and the
   operationalization YAML of its engine, rationale paragraph first, generated against the main tree's current HEAD for those files — they have
   not changed since ca27e95), and `patches/090_catalogue_offer_after_validation.patch` (the `src/dossier/catalog_purpose.json` entry).
2. Two facts you should know for the input contract: (a) the Stacks will send the cohort table + plan + the pair job ids only; the
   Mastermind assembles `cohort-packet/v1` from its own job store (ledgers with wall status and critic rulings, tables, memo markdown, source
   documents) — write the adapter's specification as a section in the design memo (what the dossier job record must export, field by field,
   and where today's record falls short: `job.analysis[phase].final_output` is the engine's assembled prose with its ledger rows in the
   answer shape, `final_wall` the wall's rulings, `job.tables` the desk tables, receipts the models; there is no structured row export yet);
   (b) `SourceRole` on the main tree now has `profile` and `statements`; add `cohort` to your patch list as a one-line addition to
   `src/sources/schemas.py` rather than assuming it.
3. The closing section of the design memo: actual provider cost of both runs (`data/study/cohort_2026_09_06/costs.json` if you kept one;
   otherwise say unmeasured), what you could not do under the constraint, and what Claude must do next in order.
4. Run the tests you wrote in the worktree and record the result in the memo.

Guidance for this resume: USD 5.
