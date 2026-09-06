# The citation family: three engines seeded by the Stacks' prompts, validated on Riley → Weber (2026-09-06)

Owner's go (15:30): the three questions the Stacks' Citation Universe answers with hand-built prompts become Mastermind engines ahead of the remaining map questions; the Riley → Weber pilot is written both ways. Codex (gpt-6-astra) designed and built the three methods, the pilot corpus and the frozen conditions (`REDESIGN_citation_family_2026-09-06.md`, `PROTOCOL_*`, commits 76ee088, e8d37d8), then hit its usage limit mid-validation with the temp filesystem full. Claude finished the runs from the paid responses (reused by prompt hash), wrote the source reads, ran the independent ratings, applied two card rules to the fidelity audit and re-ran its condition, and judged under the owner's first-queue standard. This report says which judgments are whose.

## Conditions and results

| condition | engine · mode · corpus | rows | anchors | Sonnet / Sol (mean of six) | source read | cost |
|---|---|---|---|---|---|---|
| ENG__dvs | engagement map · deep · 27 Riley texts citing Weber | 24 at the synthesis (320 extracted, 315 verified through the critic) | 24/24; 3 corpus rows with two keys | 7.50 / 7.33 | Claude: release | $4.97 |
| G8__dvs | reception map · deep · 8 held Weber readers + Riley's texts | 30 | 30/30; 4 corpus rows with two keys | 7.33 / 6.50 | Claude: release | $6.59 |
| G6__index_only | fidelity audit · standard · evidence index only, original framing | 25 | 24/25 (F4: OCR window) | 7.67 / 6.50 | Claude: superseded by the repair | $0.71 + recovery |
| G6__index_only_repair | fidelity audit · standard · index only, repaired framing | 29 | 26/29 (three tagged and dropped by the desks: two OCR windows, one memory quote) | attempt 2 unscored; the card-rules re-run: 8.33 / 7.83 | Claude: release (re-run 27/28 anchors, verdict and how as fields) | $1.77 + $2.06 |
| G6__checked | fidelity audit · standard · full sources, original framing | 0 findings | — | 6.83 / 2.83 | Codex: withhold (the reader refused; per-document scope JSON) | $8.87 |

Known cost of the family through the ratings: $30.87 plus $1.67 reserved for calls whose usage was not returned (`calls.json`), of which $8.87 is the refused full-source condition and about $5 is the two recoveries' re-paid calls after the temp-filesystem failure. Guidance was $20; the owner's rule is that caps are guidance.

## What the engines do, on this corpus

**Engagement map.** A position map of the 27 citing texts (central claim, Weber's role, a qualification each) that refuses the easy overstatement (marks where "Weberian" is only a label, where the return to Weber is Biernacki's proposal under review, where Weber is named without a locus), 24 synthesised findings all anchored, three trajectory rows pairing texts across years (2011 Judt → 2023 Brown on responsibility; 2020 Faultlines → 2025 Long Downturn on political capitalism). The per-passage inventory (315 verified rows) lives in the step ledgers; the synthesis brief should carry it as a table for the Stacks' Memos tab (design note). Source read: `source_memos/ENG__dvs.md`.

**Reception map.** A position table over eight readers with the theme's origin marked (`plan_spine` / `reader addition`, the Stacks' requirement), Riley among them: consonant with Wright on class versus status, with Rundell and Ganev on politically constituted power and profit; the formalist objection he never engages (Love: tax farming is not capitalist in Weber's formal sense) named as such. The "most-cited citers Riley does not cite" column needs the Stacks' ledger counts. Source read: `source_memos/G8__dvs.md`.

**Fidelity audit.** Reads the evidence index alone (the single-engine call the Stacks asked for): 29 pairs, verdicts sound on six of seven pairs read against the witnesses (the seventh judged without a witness in hand, the defect the card rules address), unverifiable pairs stated with the reason rather than judged. Two shape defects fixed by card rules: the verdict folded into the finding sentence instead of the `verdict:` field, and `how:` not carried. The full-source condition refused to produce findings under the original framing (Codex's read, `source_memos/G6__checked.md`); the repaired framing is the one released. Source reads: `source_memos/G6__index_only_repair.md`, `G6__index_only.md`.

## Decisions (Claude, under the owner's standard; Codex absent)

- **Released and offered** under a new purpose group "Trace the citations": `citation_engagement_map`, `citation_reception_map`.
- **Fidelity audit**: released on the re-run with the card rules (27/28 anchors, every pair with `verdict:` and `how:`, the once memory-judged pair now unverifiable; Sonnet 8.33, Sol 7.83, the highest in the family; read in `source_memos/G6__index_only_repair.md`). Offered under "Trace the citations" beside the other two.
- **Design notes for the next revision**: the passage inventory as a table in the engagement map's synthesis; reference-point rows marked in the reception table; the ledger's citation counts for "never engages"; a cohort dimension for one-to-many runs (`TASK_stacks_cohort_citation_flow_2026-09-06.md`); the Stacks' `digest_check` as the fidelity audit's second input.

## Plumbing changed by this family's runs

Walls strip quotation marks (a model writes ‘Power’ where the page has Power); the corpus synthesis contract records and tags after its bounded repair instead of aborting (a paid fidelity audit had died on three legitimately unverifiable quotes); duplicate ids re-keyed; the study plan re-frozen with a revision note when the runner changed under it. Two lessons for the bridge: page windows from pdftotext are OCR-noisy on Economy and Society (two of three anchor failures), so the Stacks' page-marked rendition matters; and a retrieval that lands in a volume's notes section must be reported as no witness.

## Addendum: the card-rules re-run

The two card rules (verdict and how as fields; no witness → unverifiable, never from memory) were applied to the operationalization and the condition re-run at $2.06: 28 pairs, 27 anchors verified, verdicts accurate 5 · fair 9 · selective 5 · stretched 1 · unverifiable 8, `how` page 21 · search 7. The one wall failure is an OCR-corrected quote the wall rightly refuses; the row is tagged and dropped by the desks.

## The pilot both ways

Not run in this session: the Mastermind memo is `scripts/pilot_dossier_inprocess.py` over the pilot corpus (in the repo under `pilot_corpus/`), the Stacks' memo is with the Stacks session; the next session runs it on the machine where both live (`NEXT_SESSION_PROMPT_new_machine_2026-09-06.md`).
