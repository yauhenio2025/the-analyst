# Held-out Hegel recovery amendment — 2026-09-05

This amendment is recorded **before any pair judgments**. It supplements the [held-out protocol](STUDY_ideas_HEGEL_HELDOUT_PROTOCOL_2026-09-05.md) for two deterministic failures after successful saved read and critic calls. The frozen harness, runtime, prompts, raw responses and original attempts remain unchanged. Offline recovery adds no model calls, new logical-job attempts or source probes. Adoption is a separate, reviewed action after the generation process releases its campaign lock.

The original frozen processing left **two incomplete pairs**: Argument Architecture/Ganzinger and Inferential Commitment Mapper/Ganzinger. This remains an execution-reliability result even if their recovered outputs are adopted. The primary comparison will retain all eight pairs after accepted recovery; a second table will exclude those two pairs and report the remaining six. Both tables separately count agreed previous wins, agreed revised wins, agreed ties, splits and incomplete pairs. A decision counts only when both valid opposite-order judgments agree. This policy is fixed before judging and does not change any judge prompt or decision rule.

## Two separate transformations

**Revised Argument Architecture/Ganzinger**, attempt `c5620c0d97c1`, failed with `Ledger row I4 has repeated anchor fields; use distinct anchor/doc suffixes`. Its critic supplies ordinary F1–F20 rulings, then I1/I3/I4 answers to the requested critical questions, then legitimate additions. The I4 answer repeats the primary anchor field three times. These I IDs are unique, absent from the original ledger and have no `added` status. Frozen `apply_rulings` cannot apply them, but strict parsing fails before that omission can occur.

The first transformation excludes only those unique unknown, non-added row blocks from the exact critic's parsed ledger view. It preserves their raw bytes and hashes in its manifest. It does not rename IDs, reinterpret requested critical questions as optional sections, discard additions, or repair malformed anchors in original/addition rows. Duplicated unknown IDs remain an error because frozen uniqueness checking precedes omission. The original error reproduces without the transformation; all five completed comparison finals and their process receipts reproduce byte for byte with it. The recovered final has 25 rows and 25 verified anchors: 18 confirmed, one weakened and six added; one original row is rejected.

**Previous Inferential Commitment Mapper/Ganzinger**, attempt `1064cbe77bbf`, failed with `revised-finding must be a quoted string`. F16 ends in the exact bare field ` — revised-finding: same finding, anchor‑b corrected`. This is an invalid directive, not replacement finding prose. The second, independent transformation removes only this terminal field after checking the exact saved read/critic hashes, unique F16, `weakened` status, byte-identical original/critic finding head, and explicit expected corrected secondary anchor. Frozen application then keeps the unchanged finding and uses that corrected anchor. The directive is never quoted into a replacement finding. All seven completed comparison finals and process receipts remain byte-identical. The recovered final has 27 rows and 33 verified anchors: 22 confirmed, one weakened and four added, with one proposed addition dropped.

Both methods replay **every saved call** against its exact recomposed full prompt, label, requested/used model, response hash and usage. Partial/failed call receipts and mismatched or missing inputs are refused. Original backend durations and token usage are restored during replay; original failed-attempt elapsed time is retained, and offline CPU time is separate in each manifest. These membership and equivalence checks establish mechanical provenance, not source-interpretation accuracy or full critic ruling coverage. Raw format diagnostics retain both original failures.

## Pinned review artifacts

Artifacts below are ignored local evidence under the [held-out run](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076). Its full identity is `43f051bdd4d890762145163d0e1d41c9be46aa19234f61456962ded883530d7e`; the unchanged harness SHA-256 is `bf781c7202f3e6e22de624bfe9929cfd8402ce0bb2a5a55b8756754ed0190ac1`.

| Artifact | SHA-256 |
|---|---|
| [Argument manifest](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/reader_notes/ruling_recovery/20260905T082845.591540Z/manifest.json) | `ad296c943f5a46e5edcd3e62c8983447bfed826fb8e585859ffa9ce83509c64e` |
| External two-target adoption/report adapter | `245931355cd7325cbcc6cd31e8fa5ca959291a55428881cda40c3523abc02f1f` |
| Argument transformation script | `355ecc93ca6a29cdf4ec46d67576c15d6b306a8731d57f3eb75cf9d1a520ffbf` |
| [Argument recovered output](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/reader_notes/ruling_recovery/20260905T082845.591540Z/recovered.md) | `f8ea7f20250f080f9a6bf1bbaa9cb1780b9602977bcbb698d43abc2a8961b655` |
| [Commitment manifest](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/reader_notes/rewrite_recovery/20260905T084347.772343Z/manifest.json) | `6b7f5e0e02a338d1b006ec8d17e62507ab28800b148ebefc850fb7186dcfed26` |
| Commitment transformation script | `d8e64625ba04dbb0130aff321ca6612284c4d7f208f47505974aec081419199d` |
| [Commitment recovered output](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/reader_notes/rewrite_recovery/20260905T084347.772343Z/recovered.md) | `22f88ea1e4cffe8e373e06294892ea18e96ce1d689d24ab398de1cf4fd1bee6b` |

The second manifest also pins its unchanged replay dependency on the first script. Each bundle preserves original failed-job and plan/results snapshots, target call files, exact removed bytes, original/transformed ledger hashes, final output and process receipts. The external [adoption adapter](../../scripts/adopt_ideas_hegel_recovery_2026_09_05.py) binds its own exact code hash into each adopted record; editing it after adoption invalidates that record's reuse until separately reviewed.

## Adoption and judging lifecycle

The adapter's default is an offline preview. Actual adoption requires the existing exclusive campaign lock, no running result or invocation, an unchanged frozen plan, reviewed manifest hashes, exact replay, and a source-results snapshot concurrency check. It creates the expected final output exclusively and replaces `results.json` atomically. The original failed `receipts/<job>/<attempt>/job.json` and every numeric call receipt remain byte-identical; the new completed result points back to them and to its recovery manifest. Audit snapshots record before/after hashes. Usage is counted once from the existing numeric receipts, including the calls whose postprocessing failed.

After adoption, use this adapter for reports and judges: ordinary harness validation correctly continues to reject the original failed processing. The adapter changes only target-parent validation and report annotations; fresh judge jobs still execute through the unchanged harness, fixed models, exact opposite-order prompts, existing lock, no-retry rule and fresh-study USD 6 admission limit. The merged report exposes both recovery provenance records, both historical postprocessing failures and the eight-versus-six sensitivity counts. `--require-complete` still requires all 16 valid generations and 16 valid judgments.

The following commands are for root's separate review and launch; preparing this amendment does not execute them:

```bash
export TMPDIR=/home/evgeny/projects/the-analyst-wt/ideas-hegel-test-tmp
hegel_run=data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076
hegel_recovery_args=(
  --bundle "$hegel_run/reader_notes/ruling_recovery/20260905T082845.591540Z"
  --manifest-sha256 ad296c943f5a46e5edcd3e62c8983447bfed826fb8e585859ffa9ce83509c64e
  --bundle "$hegel_run/reader_notes/rewrite_recovery/20260905T084347.772343Z"
  --manifest-sha256 6b7f5e0e02a338d1b006ec8d17e62507ab28800b148ebefc850fb7186dcfed26
)
python scripts/adopt_ideas_hegel_recovery_2026_09_05.py "${hegel_recovery_args[@]}"
# Only after the generation process has exited and root accepts both bundles:
python scripts/adopt_ideas_hegel_recovery_2026_09_05.py "${hegel_recovery_args[@]}" --adopt
python scripts/adopt_ideas_hegel_recovery_2026_09_05.py "${hegel_recovery_args[@]}" --phase report
# Root completes the pre-judge source review before this paid launch:
python scripts/adopt_ideas_hegel_recovery_2026_09_05.py "${hegel_recovery_args[@]}" --phase judge --run --budget-usd 6
python scripts/adopt_ideas_hegel_recovery_2026_09_05.py "${hegel_recovery_args[@]}" --phase report --require-complete
```

A crash after exclusive output creation but before the atomic results update leaves an orphan output and the original failed result. A subsequent adoption refuses automatic replacement and requires explicit comparison with the immutable bundle. A completed adoption is idempotent if all bound bytes remain unchanged. Neither path automatically starts a new paid generation attempt.


Offline validation passed 29 focused tests across the two proposal suites and the adoption suite. The latter performs the full two-target preview/adoption/report/idempotent-resume lifecycle only in an isolated artifact copy, with networking denied. It checks unchanged original receipts and cost totals, both merged provenance records, incomplete-pair reporting, lock and paid-retry refusal, and manifest/prompt/output/failed-job/record tamper rejection. Artifact-dependent tests explicitly skip in clean checkouts without the ignored local sources, calibration and reviewed bundles.
