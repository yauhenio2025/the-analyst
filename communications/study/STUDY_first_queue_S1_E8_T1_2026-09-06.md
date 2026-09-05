# First queue, Claude's three: reading guide (S1), quantities (E8), events (T1) — validation memo (2026-09-06)

Ten readings on GPT-5.6 Sol (the production default: one call plus the DeepSeek check; the engine's original questions in one call where an original exists), two papers each; independent scores by Sonnet and Sol; anchors verified by code; two outputs read against the source by hand. Cost $2.51. Per-run table: `STUDY_first_queue_runs_2026-09-06.md`; outputs under `data/study/v5_first_queue/`. Definitions: `REDESIGN_reading_guide_2026-09-06.md`, `REDESIGN_quantities_2026-09-06.md`, `REDESIGN_events_2026-09-06.md`.

## What the hand check found

**Quantities (AUKUS).** 34 rows, every quote verbatim. The ledger separates pledged, awarded and promised sums from disbursement (the AUD 840 million Arafura package is "promised"; the USD 1.28 billion is a loan pledge; the AUD 4.1 billion "would be dispensed"); catches the paper's one clean comparison (US chip share 12% against 37% in 1990) and its non-commensurable juxtaposition (129 vehicles beside a 19.1% share-price rise, plus a currency conversion without a rate); flags the double-counting risk between the Arafura package and the AUD 6 billion facility it draws on; names the comparisons the paper withholds (announced against disbursed, AUKUS-linked against total defence spending, recipient firms against eligible firms); and lists the words doing quantitative work without numbers ("severe delays", "huge capital injection"). One imprecision: row F17 says three itemised grants "total the displayed AUD 27 million"; they sum to 26.78 million, which the paper rounds; the row should say so. The critic confirmed all 30 original rows and added 4.

**Events (AUKUS).** 37 rows, every quote verbatim. Each causal link is typed from the paper's own connective ("led to" as cause, "enables" as enabling condition); on the paper's central chain (AUKUS → reduced polarisation → bipartisanship) the row records that the support is sequence only and that the text itself names alternative causes (prior ties, the fear of being "wedged"), the catch the earlier studies made expensively. One imprecision: the prose groups a February 2024 event (SkyWater's CHIPS application) into a "January–March 2024" span; the ledger row keeps the month. The critic confirmed 29 of 30, weakened 1, added 7.

## What the raters said, and how to read them

| method | paper | Sonnet new / old | Sol new / old | anchors new / old |
|---|---|---|---|---|
| reading guide | AUKUS | 6.50 / 8.00 | 9.33 / 9.33 | 100% / 100% |
| reading guide | Zambrana | 7.33 / 7.00 | 9.00 / 9.33 | 96% / 100% |
| events | AUKUS | 6.00 / 6.67 | 8.33 / 7.67 | 100% / 100% |
| events | subsea | 6.50 / 6.67 | 9.00 / 8.17 | 94% / 89% |
| quantities | AUKUS | 6.33 / — | 9.33 / — | 100% / — |
| quantities | subsea | 6.00 / — | 9.00 / — | 87% / — |

Sonnet's reasons are one complaint repeated: "structured inventory rather than argument", "ledger format fragments coherence", "non-obvious insights buried in an inventory". That is the frontier's reading rubric doing what it was written to do, and it is the wrong yardstick for the quantity and event methods, whose product is table rows for the desks; the same rubric marked the old event mapper down for the same reason. Sol's scores are high across the board, as in every study so far, but its reasons did the useful work (the two imprecisions above, "trimmed anchors" on the subsea paper). For inventory methods the measures that matter are the ones code and a source check give: 87–100% of quotes verbatim, 30–37 rows a run, two minor imprecisions in two hand-checked outputs, no invented figures or dates.

The reading guide is a different case. Sonnet prefers the old `deep_summarization` one call on AUKUS (8.0 to 6.5) because the new guide reads as "a pedagogical outline rather than a single expert interpretation"; on Zambrana it slightly prefers the new one. The guide was designed as a guide (route, terms, evidence, entry points) for a reader who has not read the text, and that is what Sonnet penalises. Candidate tweak, untested: ask the synthesis to carry one line of argument through the six sections and to put the entry points last as prose, not as a list.

## Decisions
- **Quantities and Their Meaning** and **Events and Supported Causal Links**: offer them, as inventory methods whose value is desk-ready rows; keep the check (it added 4–7 rows a run and confirmed the rest). Registered in the catalogue under a new purpose group "Count and date" (this commit). Two fixes to their briefs for a later pass: state rounding when a sum is compared to a rounded total; keep month precision in the prose where the text gives it.
- **Reading guide**: keep under the shape (the desks need its rows and it is the default synthesis engine), apply the brief tweak above, and re-rate on two papers before calling it settled.
- Judging inventory methods: anchor rate, row count and a source check; the reading rubric only for readings.
