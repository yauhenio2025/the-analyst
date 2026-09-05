# Held-out Hegel definition comparison — 2026-09-05

This is one fresh, user-authorized comparison of the revised four ideas engines on two held-out papers. It has a separate USD 6 admission ceiling. The harness is a no-call preview by default. Root reviews the frozen harness and generation outputs before launching the separate judging phase. No results or source-specific probes are supplied to the models from the earlier evaluation memos.

## Treatment and fixed conditions

The `previous` condition uses the **production operationalization YAML at `11beb77be8de7544be019237f512a56d9b5cd30a`**, verified byte-for-byte against the original study's `c19513884a5453f54073e38cbabf2c6e7d5cfd28` definitions. The `revised` condition uses the operationalization YAML at **`d9cfc6e4569d237a30174446f5c6a25e31f05f98`**.

Both use `run_oneshot_checked` at standard depth and the same capability definitions, repaired runtime, composer, critic application and JSON quote contract from `d9cfc6e`. Both receive identical source bytes, separately pinned below. Only the process definition changes. This estimates a definition-package effect under the repaired runtime, not the benefit of the runtime repairs or any individual question. The corpus-only P6/X6 dimensions are not exercised by these single-paper inputs. There is no Luna extraction stage.

| Stage | Requested model | Invocations |
|---|---|---:|
| Checked reading | `openrouter/openai/gpt-5.6-sol` | 16 |
| Critic | `openrouter/deepseek/deepseek-v4-pro` | 16 |
| Pair judgment | `claude-sonnet-4-6` | 16 |

Four engines—Conditions of Possibility, Argument Architecture, Inferential Commitment Mapper, and Epistemological Method Detector—each run both conditions on both papers: **16 checked outputs, eight pairs**. Each pair then receives two judgments with A/B order reversed, using the original study's unchanged source-aware Sonnet pair prompt. A winner or tie counts only when both valid orders agree after mapping letters back to conditions. Splits and incomplete pairs remain separate. Visible format, length, and check receipts may influence the judge; opposite ordering tests position sensitivity but does not remove these cues. This small comparison does not establish broad generalization.

## Frozen inputs

Sources are full local text files, including substantive notes, under [sources_ideas](../../data/study/sources_ideas). The harness loads exact UTF-8 bytes without normalization or excerpting.

| Paper/file | Bytes | Characters | SHA-256 |
|---|---:|---:|---|
| Ganzinger, `hegels_concept_of_the_concept_2026.txt` | 83,984 | 82,582 | `ccff7540fcabac9ab2159273fec32c7c50d89e36e9c75415b12b9c8fa316b29e` |
| Elling, `elling2025_amphibian_habits_hegel_second_nature.txt` | 84,566 | 84,005 | `3d1c2855afc1ea1bb0449876dd5a4a202aa42a20efe93c61d9d1f0920ba96a66` |

The detached preparation checkout is `/home/evgeny/projects/the-analyst-wt/ideas-hegel-heldout-2026-09-05`. Every invocation of the harness imports an independent archive of the pinned commit's `src` and `scripts`; main-tree adapter edits cannot change trial behavior. Sources, calibration receipts, credentials, and result artifacts use the main repository. The project `.env` is loaded with `override=False` before runtime imports; no credential values are printed or recorded.

The plan binds the runtime archive, harness, both YAML definitions, capability/process contents, sources, model routing, transport settings, common anchoring/judge contracts, read prompt hashes, and calibration inputs. Full dynamic critic and judge prompts are saved with each invocation. The critic prompt is composed from that condition's actual parsed reading by the frozen runtime, with no posthoc source probes.

## Budget and stopping rules

The no-call preview estimates **USD 5.366146**: reads **2.002238**, critics **1.205588**, judgments **2.158320**; headroom to USD 6 is **0.633854**. These figures use the prior completed baseline's 24 read, 12 critic, and 24 judge receipts, not model-price discovery. Per-role input envelopes use the maximum observed input tokens per character × 1.10; output envelopes use maximum observed output tokens × 1.25. Critic/judge previews use prior maximum ledger/final lengths. These size placeholders only estimate cost and are never sent to a model.

Repository input/output prices per million tokens are Sol USD 2/10, DeepSeek V4 Pro USD 1.042/2.085, and Sonnet USD 3/15. Each actual call recalculates its admission estimate using its exact composed prompt. The harness refuses a new invocation when cumulative known cost across identities of this fresh held-out study plus that envelope exceeds the chosen limit, or any existing invocation has unknown cost. Prior study spend is excluded. This is an admission ceiling, not a guaranteed billing cap: a long response, hidden provider charges, or retries inside the frozen backend can exceed an estimate in flight. Requested-versus-used routing, usage, reported retries, partial responses, errors, and unknown metadata are retained and reported.

Execution is sequential, with exactly one planned read and critic per generation and one invocation per judgment. The harness does not automatically retry a failed parser, response, or API attempt, nor silently accept a fallback model. An existing invocation under any held-out identity blocks a new paid attempt for that logical job. A crash leaving a running job/receipt must receive explicit offline review: it is not automatically replayed as a new paid call. A crash before any invocation can safely restart; a completed-but-uncommitted response requires separate provenance-preserving recovery, which this harness deliberately does not implement.

## Execution and audit

Run from the main checkout with a home-backed temporary directory:

```bash
export TMPDIR=/home/evgeny/projects/the-analyst-wt/ideas-hegel-test-tmp
python scripts/study_ideas_hegel_heldout_2026_09_05.py
# Root launches only after harness review:
python scripts/study_ideas_hegel_heldout_2026_09_05.py --run --phase generate --budget-usd 6
# Root reads all sixteen outputs and preserves pre-judge source assessments before:
python scripts/study_ideas_hegel_heldout_2026_09_05.py --run --phase judge --budget-usd 6
python scripts/study_ideas_hegel_heldout_2026_09_05.py --phase report --require-complete
```

Artifacts go under main `data/study/ideas_hegel_heldout_2026_09_05/<identity-prefix>/`: full plan, atomic results records, raw responses, full prompt JSON, per-invocation receipts, final outputs, and a JSON report. An exclusive study lock prevents concurrent launches. Completed generation reuse verifies every receipt/prompt/raw-response hash and replays both saved calls through the frozen runtime, requiring exact recomposed prompts, labels, routing and final output bytes. Judgment reuse validates both parents, reconstructs A/B, and compares the raw parsed verdict with both the saved output and record. Changed or missing artifacts fail validation. Failures and partial response usage survive in their attempt folders; no baseline artifacts are changed.

The report gives costs/tokens/time and known/unknown routing/retry metadata by role; both-order outcomes; final process walls; and diagnostics on the **raw Sol and DeepSeek responses before sanitization**. Canonical JSON string quoting is counted separately from legacy-but-parseable quote fields and malformed fields. Raw membership walls separately count parsed rows/anchors and source-matching anchors. A parseable or matching quote is not evidence that its interpretation, attribution, or inferred commitment is correct. A carried row is not a critic confirmation. Null partial/stop metadata remains unknown rather than an affirmative provider completion signal.

Offline validation: `python -m pytest tests/test_study_ideas_hegel_heldout_2026_09_05.py -q`. All backend functions in execution tests are replaced with local fake responses; preview never launches or writes study output.
