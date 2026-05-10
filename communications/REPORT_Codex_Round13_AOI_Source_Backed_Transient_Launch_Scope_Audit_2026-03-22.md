Approve

# Round 13 Scope Audit

## Findings

No blocking findings remain after revision.

The main architectural error in the earlier memo is now corrected:

- the-critic is limited to saved-result identity resolution and proxying
- analyzer-v2 owns the actual AOI source-result-to-compose mapping by upstream `v2_job_id`

That matches the current implementation seams much better than the previous version.

## Direct Answers

1. Does the memo correctly identify the hardcoded-example dependency as the main remaining contradiction after round 12?
Yes.

That contradiction is real in the current proof host: the transient page still initializes from checked-in dossier/comparison fixture requests and submits explicit `prose_sections` to `POST /v1/presenter/compose-from-intent` ([`AoiComposeFromIntentPage.tsx`](/home/evgeny/projects/the-critic/webapp/src/pages/AoiComposeFromIntentPage.tsx#L51), [`composeFromIntentExamples.ts`](/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentExamples.ts#L5), [`composeFromIntentClient.ts`](/home/evgeny/projects/the-critic/webapp/src/lib/composeFromIntentClient.ts#L107)).

2. Is a bounded the-critic backend proxy actually the right implementation seam, given where the saved AOI result data lives today?
Yes, after the revision, because the memo no longer makes the-critic the home of AOI mapping logic.

The revised split is coherent with the live repos:

- the-critic already resolves thinker/project-scoped AOI results and recovers `v2_job_id` from upstream discovery plus local fallback ([`AoiV2ThematicPanel.tsx`](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L94), [`AoiV2ThematicPanel.tsx`](/home/evgeny/projects/the-critic/webapp/src/components/influence/AoiV2ThematicPanel.tsx#L259), [`boundedV2Client.ts`](/home/evgeny/projects/the-critic/webapp/src/lib/boundedV2Client.ts#L94))
- analyzer-v2 already owns the durable AOI run/result substrate and compose-from-intent orchestration ([`result_contract.py`](/home/evgeny/projects/analyzer-v2/src/analysis_products/result_contract.py#L275), [`compose_from_intent.py`](/home/evgeny/projects/analyzer-v2/src/presenter/compose_from_intent.py#L85))

3. Are the bounded `dossier` / `comparison` source profiles realistic from the current persisted AOI result payloads, or is the memo assuming source fields that are not actually durable?
Yes, they are realistic now that the memo explicitly roots them in analyzer-v2 artifacts and phase-output metadata rather than Critic `_presentation` snapshots.

Repo facts:

- the AOI workflow phases are exactly thematic synthesis, engagement mapping, sin findings, and thematic report ([`anxiety_of_influence_thematic_single_thinker.json`](/home/evgeny/projects/analyzer-v2/src/workflows/definitions/anxiety_of_influence_thematic_single_thinker.json#L8))
- raw engine outputs are persisted in `phase_outputs` and retrievable by job/phase ([`output_store.py`](/home/evgeny/projects/analyzer-v2/src/executor/output_store.py#L21), [`executor.py`](/home/evgeny/projects/analyzer-v2/src/api/routes/executor.py#L385))
- normalized AOI artifacts already exist for thematic synthesis, engagement mapping, and sin findings ([`store.py`](/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py#L24), [`store.py`](/home/evgeny/projects/analyzer-v2/src/analysis_products/store.py#L648))
- thematic report normalization already exists in AOI output metadata and presenter reuse paths even though it is not yet a Stage-1 artifact family ([`aoi/contract.py`](/home/evgeny/projects/analyzer-v2/src/aoi/contract.py#L82), [`aoi/contract.py`](/home/evgeny/projects/analyzer-v2/src/aoi/contract.py#L329), [`presentation_api.py`](/home/evgeny/projects/analyzer-v2/src/presenter/presentation_api.py#L1809))

That is enough to support:

- `dossier` from thematic synthesis + thematic report
- `comparison` from engagement mapping + sin findings + thematic report

with honest failure when one of those sources is missing.

4. Does the memo understate any risk of consumer re-thickening by moving result-to-compose mapping into the-critic?
No. The revision fixes that risk explicitly.

The memo now says the-critic should not become the permanent home of AOI result-to-compose mapping, and that analyzer-v2 should own reconstruction from its own durable AOI outputs ([`MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md#L162), [`MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md#L189)).

That is aligned with the larger roadmap:

- analyzer-v2 as central composition brain
- consumers getting thinner, not smarter

([`MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-21_round8_and_beyond_roadmap_vision.md#L208), [`DYNAMIC_BESPOKE_APPS_VISION.md`](/home/evgeny/projects/analyzer-v2/communications/DYNAMIC_BESPOKE_APPS_VISION.md#L128)).

5. Is there a narrower or cleaner next move the memo should choose instead?
No narrower move is clearly better at the current seam.

The revised memo now chooses the clean bounded move:

- keep the round-12 transient shell
- remove fixture-backed launch inputs
- resolve source identity in the-critic
- reconstruct compose inputs in analyzer-v2
- stay out of persistence, workspace unification, and multi-workflow widening

That is the right immediate continuation of round 11 and round 12 ([`MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round11_bounded_compose_from_intent_completion.md#L17), [`MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round12_transient_consumer_adoption_completion.md#L16)).

6. Is the proof standard strong enough, and does it avoid silently falling back to round-12 hardcoded fixtures?
Yes, at scope level.

The memo now explicitly requires:

- successful source-backed `dossier` and `comparison` launches
- no hardcoded proof payloads as source of truth
- deterministic, code-owned mapping
- honest failure when required source material is missing
- saved proof artifacts including source identity, resolved upstream `v2_job_id`, exact launch requests, response JSONs, rendered shell evidence, and focused regression

([`MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md`](/home/evgeny/projects/analyzer-v2/communications/MEMO_2026-03-22_round13_aoi_source_backed_transient_launch_scope.md#L330))

That is strong enough for planning. Implementation still needs to capture those proof artifacts honestly.

## Residual Notes

- The memo is right to call the analyzer-side input `source_job_id`, but implementation should stay concrete that this is the upstream AOI `v2_job_id`, not a Critic-local snapshot id. The scope text mostly does this already; keep it precise in the execution plan.
- The report path is correctly scoped as metadata/phase-output-backed rather than a Stage-1 artifact family. If legacy AOI jobs lack the needed report metadata, the implementation must fail honestly rather than widen the tranche into report backfill work.
- The dedicated Critic resolver route is acceptable as a bounded host seam, but route placement is still secondary. The architectural doctrine is the important part: Critic resolves identity; analyzer-v2 resolves content.

## Docs Note

The extra docs materially reinforce the revised conclusion.

- [`CHANGELOG.md`](/home/evgeny/projects/the-critic/docs/CHANGELOG.md#L19) and [`FEATURES.md`](/home/evgeny/projects/the-critic/docs/FEATURES.md#L389) both confirm the active bounded contract is upstream analyzer-v2 run/result truth, not richer Critic-side ownership.
- [`STAGE9_AOI_CUTOVER_RUNBOOK.md`](/home/evgeny/projects/the-critic/docs/STAGE9_AOI_CUTOVER_RUNBOOK.md#L66) reinforces that AOI truth is already being reasoned about in terms of upstream result identity, `corpus_ref`, and proving artifacts.
- `/home/evgeny/projects/the-critic/webapp/docs` does not materially change the conclusion; it only contains `CLAUDE.md`.

## Bottom Line

The memo is now technically grounded and execution-plan ready.

It chooses the right next move, puts the source mapping seam on the analyzer side where the durable AOI data actually lives, keeps the-critic thin, and defines a proof standard that is strong enough to close the fixture-backed gap honestly.
