# Live dossier check on the desk (2026-09-06)

Job `dossier-8b315f26f34e` on https://the-analyst-kcuc.onrender.com: two papers (Wijaya's AUKUS paper and Abels' subsea-cable paper, 161K chars), executive audience, medium depth, intent "What do these two papers establish about how states redirect private capital and networks?". Script `scripts/live_dossier_check.py` (creates, answers the brief, polls, reports). Purpose: exercise, on the deployed desk, the spine reading the findings ledger by id, the table walls, and the two "Count and date" engines offered since 2026-09-06.

## What happened

| step | seconds | what |
|---|---|---|
| reconnaissance | 100 | 2 profiles, 16 anchored claims (anchor wall 16/16) |
| brief | 145 | two options; the check chose `fixed_path_numbers_and_sequence` (the desk's recommendation) over `alt_contradiction_and_instruments` |
| plan | 45 | three phases: 4.1 statistical_evidence (Quantities and Their Meaning), 4.2 event_timeline_causal (Events and Supported Causal Links), 4.3 argument_architecture — the planner chose both new engines on its own for a numbers-and-sequence brief |
| analysis | 913 | each engine at standard depth = one call on Sol + DeepSeek V4 Pro check + rulings applied (pass 1 read / pass 2 check / pass 3 checked) |
| spine | 116 | 5 sections, every section carrying `finding_ids` (8 each: quantity_ledger F2 F3 F5 F7 F8 F11 F12 F13; event_timeline F3 F4 F5 F6 F7 F9 F10 F11; claim_scorecard F8 F9 F10 F12 F13 F15 F17 F18; two per-paper breakdowns) — spine wall 5 sections, 0 errors |
| tables | 104 | three tables from the spine: key figures' evidential weight (9/9 rows kept), SeaMeWe-6/AUKUS sequence (9/9), cause-effect claim scorecard (7/7); 0 dropped, 0 trimmed, 0 re-keyed |
| compose | 159 | 5 sections drafted; draft wall 0 errors; 20 claims anchored, 0 unfootnoted |
| crosscheck | 22 | "the dossier hangs together"; one standing cosmetic finding (a table caption carries the date 15 September 2021) |

Thesis produced: most figures the two papers cite (AUD 4.1B, USD 400B, $600M) are government targets or fund aggregates, not confirmed spending; the SeaMeWe-6 cable case is the only fully traced causal chain. That is the reading the quantity and event engines were built to make possible.

## Cost and two plumbing findings

Recorded total $1.57 over 18 calls, but the nine analysis passes were written into the receipts as `[UNPRICED]` $0.00 while the event stream priced the same calls (Sol $0.16–0.19 each, DeepSeek $0.07–0.08 each, $0.77 together): the desk's receipts priced through a lookup that did not know `openrouter/<vendor>/<model>` ids. Real cost ≈ $2.34. Fixed the same day (receipts now price through `src.events.pricing.estimate_cost`, which strips the prefix). Second: the call narration labelled every standard-depth run "process dvs" although the mode was `oneshot_checked`; the label now names the mode actually run.

## Deploys and in-flight jobs

The job ran while three pushes redeployed the service (06:03–06:06 local). It was not interrupted: the analysis calls continued through the deploys, and the desk also has a drain handler and a startup recovery that resumes orphaned jobs (`recover_orphaned_dossiers`, 24 h grace). The earlier tracker note calling the job orphaned was wrong; a step that takes fifteen minutes does not update the job's timestamp, which is what looked like a stall.

## Verdict

The desk consumes the checked ledger by id end to end on the live deployment: spine sections cite finding ids, tables lift rows that the anchor wall verifies verbatim, the crosscheck reads them, and the two inventory engines are chosen by the planner and produce desk-ready tables. Nothing to change in the shape.
