# Memo: Snapshot After Stage 9

Date: 2026-03-18

## Purpose

This memo records the actual state of the program after the Stage 9 AOI by-reference cutover work.

It is meant to answer:

- what Stage 9 was trying to do
- what actually completed across `the-critic` and `analyzer-v2`
- what is now true in live deployment
- what is still incomplete or messy
- whether Stage 9 should be treated as closed
- how this affects the broader thin-app / dynamic-bespoke-app vision

This is a snapshot memo, not a new planning memo.

## Executive Status

The right current status call is:

- **Stage 9 is functionally complete**
- **AOI thematic v2 is now by-reference by default on the live Critic path**
- **rollback via `AOI_THEMATIC_V2_INLINE=1` has been proved**
- **analyzer-v2 is now load-bearing for AOI result restoration and presentation**
- **the broader dynamic-bespoke-app vision is still only partially realized**

There is currently **no Stage 10 document** in the local docs/communications trail.

The next work should therefore not be framed as "continue Stage 9" or "obviously move to Stage 10."
It should be framed as:

- close out Stage 9 cleanly
- decide the next platform program explicitly

## What Stage 9 Was

Stage 9 was the AOI analogue of the earlier genealogy cutover work.

Its job was to move bounded AOI thematic execution from:

- inline/default-host-owned semantics

to:

- by-reference/default analyzer-v2-backed semantics

while proving all of the following in production-like conditions:

1. Critic migrations landed and were valid
2. inline and by-reference AOI runs produced the same semantic `corpus_ref`
3. rollout provenance was visible
4. the by-reference path became the default
5. inline rollback could still be forced

The primary runbook for this work is:

- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`

## Source Artifacts Reviewed For This Snapshot

Primary operational documents:

- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md`
- `/home/evgeny/projects/the-critic/docs/STAGE9_AOI_MIGRATION_VALIDATION.sql`
- `/home/evgeny/projects/analyzer-v2/communications/REPORT_Claude_Stage9_AOI_By_Reference_Operational_Gate_And_Cutover_Scope_Review.md`

Primary evidence artifacts:

- `/home/evgeny/projects/the-critic/smoke-artifacts/stage9/20260318T031033Z/inline-baseline.json`
- `/home/evgeny/projects/the-critic/smoke-artifacts/stage9/20260318T081653Z/inline-baseline.json`
- `/home/evgeny/projects/the-critic/smoke-artifacts/stage9/20260318T081653Z/by-ref-canary.json`

Primary live-state references:

- Render deploy state for `the-critic`
- Render deploy state for `analyzer-v2`
- Critic Postgres migration and rollout-provenance checks
- analyzer-v2 result/presentation readiness for the late post-cutover AOI jobs

## What Actually Completed

### 1. Critic Stage 9 code landed

The relevant Critic deploy sequence on `origin/master` was:

- `e544323` `Harden Critic rollout migrations for live bootstrap state`
- `fc25b1b` `Land by-ref cutover, provenance, and AOI rollout support`
- `d5b9111` `Fix AOI by-ref provenance and corpus parity`

The live Critic service is currently on:

- `d5b9111`

The decisive Stage 9 launch-mode semantics are now live in:

- `/home/evgeny/projects/the-critic/api/server.py`

Specifically:

- legacy `AOI_THEMATIC_V2_BY_REF` is treated as ignored-after-cutover
- `AOI_THEMATIC_V2_INLINE=1` is the rollback lever
- ordinary AOI thematic v2 launches now default to `by_ref`

### 2. analyzer-v2 Stage 8/9 substrate plus post-cutover hotfixes landed

The relevant analyzer-v2 deploy sequence on `origin/master` was:

- `f90525d` `Land analysis-product and by-ref rollout substrate`
- `5dba381` `Fix adaptive phase chain/engine normalization`
- `c099f48` `Fix AOI presentation refresh and artifact backfill`
- `138a485` `Use effective plan fallback for presenter refresh`
- `d0f016c` `Accept read-only presenter calls in result delivery`

The live analyzer-v2 service is currently on:

- `d0f016c`

This matters because Stage 9 did not end cleanly at first. The AOI analysis runs completed, but the result preparation / presentation layer failed and had to be hotfixed after the cutover proof runs were already in flight.

### 3. Critic migrations are live and validated

The Critic database is now on migration:

- `031`

The Stage 9 migration checks are satisfied at the database level:

- rollout-provenance columns exist on `v2_run_references`
- `influence_reference_texts.source_document_id` is fully populated
- `SELECT COUNT(*) ... WHERE source_document_id IS NULL` returned `0`

This means the main migration prerequisite that could have invalidated corpus parity is no longer a blocker.

### 4. AOI parity proof was completed

The recorded proving sequence was:

1. Early inline baseline:
   - job `job-4565f0dc699f`
   - launch mode `inline`
   - `corpus_ref=corp-32e6ddf26c4de38ba3dc36f6`

2. Post-fix inline baseline:
   - job `job-e8b20785ea10`
   - launch mode `inline`
   - `corpus_ref=corp-542872538489ad893b13a682`

3. By-reference canary:
   - job `job-0a40ddd22ca5`
   - launch mode `by_ref`
   - `corpus_ref=corp-542872538489ad893b13a682`

The important point is:

- parity was not just assumed
- it failed earlier in the day
- it was fixed
- it was then re-proved with matching `corpus_ref`

The canonical post-fix parity value is:

- `corp-542872538489ad893b13a682`

### 5. Default-by-reference and rollback proof both happened

After parity passed, three more manual proving runs were launched:

- `job-d1de8435431e` `by_ref`
- `job-be4a3c614ad7` `by_ref`
- `job-1cf7f775be2e` `inline`

These represent:

- two default-path by-reference checks
- one explicit rollback-path inline check

All three completed successfully.

All three resolved to the same semantic corpus identity:

- `corp-542872538489ad893b13a682`

That is enough to treat the default flip plus rollback proof as operationally successful.

### 6. The post-run preparation failure was diagnosed and fixed

Immediately after the proving runs completed, the result preparation layer did not finish.

The failure was not "slow background work." It was a real preparation/presentation fault:

- refresh requests were failing
- the presentation bridge was using the wrong event-loop behavior
- AOI artifact backfill and effective-plan fallback also needed patching

This was then fixed in the live analyzer-v2 deploy sequence listed above.

After those hotfixes:

- all three late AOI runs became restorable
- presentation delivery succeeded again
- analyzer-v2 returned usable AOI presentations for them

This means Stage 9 required both:

- cutover proof
- immediate post-cutover stabilization

The stabilization is now part of the real Stage 9 story and should not be mentally separated from it.

## What Is True In Live Production Right Now

### AOI launch semantics

For ordinary bounded AOI thematic v2 launches in The Critic:

- default mode is `by_ref`
- rollback mode is forced by `AOI_THEMATIC_V2_INLINE=1`

### AOI result truth

For bounded AOI v2 surfaces:

- analyzer-v2 is the live source of run/result/presentation truth
- The Critic is no longer the semantic authority for those bounded surfaces

### AOI path maturity

AOI is now materially closer to genealogy in analyzer-v2-native execution terms than it was before Stage 9.

That does **not** mean AOI and genealogy are fully equivalent in platform maturity.
It does mean AOI is no longer merely "possible through v2 in principle."
It is now a real live path that has survived proving, cutover, rollback, and a preparation-layer failure.

### Stage 9 runbook status

The practical runbook answer is:

- the main proving and cutover goals were achieved
- the evidence exists, but it is spread across repo artifacts, live deploy history, database state, and hotfix context rather than one clean closure memo

## What Is Still Incomplete Or Messy

### 1. Stage 9 is complete, but not elegantly documented yet

There was no final single closure memo written during the live sequence.

Instead, the evidence is distributed across:

- the runbook
- smoke artifacts
- Render deploy history
- database checks
- the hotfix commit trail

This memo exists partly to fix that documentation gap.

### 2. One operator-surface bookkeeping inconsistency remains

The three late post-cutover jobs are healthy upstream and have working presentations, but their Critic-side `v2_run_references.corpus_ref` rows still show `NULL`.

That means:

- semantic truth exists upstream
- restoration works
- presentation works
- but one Critic-side rollout-provenance/backfill surface is lagging for those late jobs

This is a real cleanup item, but not a Stage 9 blocker.

### 3. The legacy-warning evidence item was not explicitly captured

The Stage 9 runbook includes:

- observe the legacy `AOI_THEMATIC_V2_BY_REF` warning after cutover

The live log review did not surface a recorded warning event.

This means the cutover semantics are present in code, but one runbook evidence checkbox was not explicitly captured in the operational record.

### 4. No Stage 10 has been defined

There is currently no local document that defines a Stage 10.

So any statement like:

- "we are now in Stage 10"

would be fiction unless a new stage memo is written first.

## Stage 9 Closure Dispositions

The residual tail has now been converted from open checklist items into explicit dispositions.

| Item | Owner | Disposition | Note |
|---|---|---|---|
| Critic-side `v2_run_references.corpus_ref` gap for `job-d1de8435431e`, `job-be4a3c614ad7`, `job-1cf7f775be2e` | `the-critic` maintainer | **Written waiver** | No cheap/local deterministic backfill was available from this repo-only tranche. Upstream analyzer-v2 manifest truth remains sufficient for Stage 9 closeout, and Critic durable-read paths now perform best-effort `corpus_ref` backfill when the manifest is available. |
| Legacy `AOI_THEMATIC_V2_BY_REF` warning evidence | Stage 9 operator | **Written waiver** | The live warning event was not captured during the cutover window. The warning path remains in code and is covered by unit tests, but no new live verification run was forced into this tranche. |
| Stage 9 closure record linked from the operational evidence home | repo maintainer | **Fixed** | `docs/STAGE9_AOI_CUTOVER_RUNBOOK.md` now links this snapshot memo and the post-Stage-9 next-steps memo directly from the evidence home. |

With those dispositions recorded, Stage 9 can be treated as cleanly closed at the documentation boundary: one linkage item fixed, two residual evidence items explicitly waived.

## What Stage 9 Does And Does Not Prove About The Bigger Vision

### Stage 9 does prove

- AOI can now travel the live path through analyzer-v2 by reference
- bounded v2 surfaces can rely on analyzer-v2 for real run/result/presentation truth
- rollout provenance and rollback controls can be made real for a second major objective family

### Stage 9 does not prove

- that apps can now be generated completely on the fly
- that consumer apps are fully disposable shells with near-zero bespoke work
- that analyzer-v2 now has a full artifact economy
- that dynamic whole-page composition is solved
- that beautiful-by-default thin apps are generalized across surfaces

Stage 9 was an operational cutover stage.
It was not the final proof of the March 13 north-star architecture.

## Final Status Call

The cleanest current statement is:

- **Stage 9 should be treated as closed in functional terms**
- **Stage 9 still has a small documentation/cleanup tail**
- **the next program should not be framed as "more Stage 9"**
- **the next program should be explicitly defined from here**

If someone asks, "Where are we right now?" the answer is:

- AOI by-reference cutover succeeded
- rollback was proved
- analyzer-v2 post-cutover prep faults were fixed
- the bounded v2 AOI live path is real
- the broader thin-app platform vision is still ahead of us
