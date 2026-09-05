# Adopting the two offline recoveries

**Prepared; adoption has not been executed.** Wait for live execution session `29306` to end before using the commands below. The live runtime, original failed receipts, and results remain untouched by this preparation.

The accepted [recovery manifest](../../data/study/ideas_2026_09_05/374325c24e6b10a1/reader_notes/auxiliary_recovery/20260905T045321.120955Z/manifest.json) pins the two artifacts, original raw responses/prompts, frozen runtime, transformation script, and all 10 byte-identical completed checked outputs. Its SHA-256 is `84b58c975f296dc7c72cb49baacb23e631a06d622c6b6192cf01da4e5f394195`. The transformation bounds `_ledger_text` at exact requested auxiliary headings; it makes no broader quotation or semantic repair.

The new [adoption script](../../scripts/adopt_ideas_auxiliary_recovery_2026_09_05.py) is outside the live plan's `CODE_FILES`. It defaults to a preview and never launches a model. Before adoption, it checks:

- No study-runner process, running result, or running invocation remains.
- The accepted manifest, transformation, artifacts, and original failed attempts retain their hashes; all 10 compared completed outputs remain unchanged.
- Current code still matches the pinned judge-resume runtime. A temporary `c19513884a5453f54073e38cbabf2c6e7d5cfd28` archive reproduces the complete plan identity and each recovered output from its exact saved prompts, models, responses, usage, and durations.
- Exactly the four judgments dependent on Argument/Chen and Epistemology/Harris remain incomplete. Other incomplete or stale judgments cause refusal.

Run from the repository root, **after the live session ends**:

```bash
# Offline guard tests; these have passed during preparation.
python scripts/adopt_ideas_auxiliary_recovery_2026_09_05.py --self-test

# Offline validation and concrete preview.
python scripts/adopt_ideas_auxiliary_recovery_2026_09_05.py

# Explicitly install the reviewed recoveries after inspecting the preview.
python scripts/adopt_ideas_auxiliary_recovery_2026_09_05.py --adopt
```

Adoption creates exactly `outputs/argument_architecture__checked__chen.md` and `outputs/epistemological_method_detector__checked__harris.md`. Atomic link creation refuses to overwrite any existing output. The frozen runtime recomputes their final wall and source coverage. Complete records include explicit recovery provenance and retain the original failed record, attempt ID, original elapsed time, raw-response hashes, transformation hash, artifact hash, and separate offline CPU times. Original `job.json` and invocation receipts retain their failed-attempt history.

An adoption audit under `reader_notes/auxiliary_recovery/adoptions/<timestamp>/` preserves the original results snapshot, proposed results, installed payloads, and before/after hashes. The script guards the source results snapshot immediately before atomically replacing `results.json`; it also refuses changed billing receipts. A lock serializes adoption scripts. The unchanged study runner does not participate in that lock, so do not start it until adoption exits successfully.

No call receipts are duplicated. The original invocation receipts remain the sole billing source; the recovery adds zero model calls and zero API cost. Original failed-attempt elapsed time and saved model-call durations remain distinct from offline recovery and adoption CPU times.

After successful adoption, root can resume the existing approved study budget with:

```bash
python scripts/study_ideas_material.py --run --budget-usd 20 --phase judge
```

This uses the unchanged judge and skips its 20 already completed judgments. Only the two orders for Argument/Chen and Epistemology/Harris should run. The `$20` gate is cumulative across the study's original receipts; it is not a fresh allowance. Do not use `--phase all` for this resume. The adoption script itself does not issue this command.
