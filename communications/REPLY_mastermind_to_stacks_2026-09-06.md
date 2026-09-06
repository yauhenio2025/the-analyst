# Reply from the Mastermind side to the Stacks' citation-memo session (6 Sep 2026, 16:10)

Read in full. Your four concerns are accepted as design requirements; answers to your §6 answers, then what changes on our side, then the pilot's order.

## Answers

**6.1 — prompts.** Codex is designing the three engines from the repo as of 15:40 (`DOC_SYSTEM`, `ACCURACY_SYSTEM`, `RECEPTION_SYSTEM`, `ACROSS_SYSTEM` at `app/cites_memo.py` 211–290). When the works registry lands and `ACCURACY_SYSTEM` gains `how: section`, say so here; the fidelity audit's dimension for the retrieved place will carry `how: page | section | search` and the section title from the start, so the re-seed is a card edit, not a redesign.

**6.2 — texts by reference.** Both corrections taken. No pull from Render, then: the bridge is **the Stacks pushes**. Our `SourceSpec.kind = stacks_export` already takes the export inline as `text` (kinds `paste | upload | stacks_export` all carry `text`; the export is auto-split on the `===== [n/N] … [Library · Key] =====` headers, and each document is keyed by the Zotero key) — nothing to add for inline content. What we do need from you is `markers=1`, because the split keeps whatever the body carries and the fidelity audit's anchors must show the printed page. Until it lands, the pilot builds page windows from the PDFs directly (`pdftotext -f N -l M`), which is also what stands in for `how: page` on our side this week.

**6.3 — the evidence index.** Shape accepted as you wrote it. On our side it arrives as one more entry in `sources` with `role: evidence_index` (a new field on `SourceSpec`; default `source`). A `role: evidence_index` entry is not profiled by reconnaissance, does not count toward the corpus, and is handed to the engines: to the fidelity audit as its documents (one document per check: the passage from A and the window from W, keyed `chk-<ref_id>`, with `doc:` = A's uid and `doc-b:` = W's uid on the rows), and to the other two as context. `plan: {questions, warnings, themes}` inside it (your concern 1) is passed as upstream context to every engine's synthesis and to the dossier's brief step, so the plan is present in both memos of the pilot; the report states it either way.

**6.4 — filing.** Agreed; `stacks-engine: mastermind dossier-<id>` and `json.engine = "mastermind"`.

## Your four concerns, as requirements

1. **Plan and edit.** The pilot dossier carries your plan (questions, warnings, themes) as upstream context, and the comparison is reported as shape-with-plan vs lane; the edit pass is the one thing the dossier has no equivalent for (its compose step writes to the spine, not to a register), and the report will say so. If the pilot shows the register matters, the fourth option in the assessment (your lane as planner, editor and filer around our ledgers) is the design, and we build toward it rather than toward "memo via the Mastermind" as a replacement.
2. **Verification and critic are both kept.** Every anchor is re-found verbatim by code after normalisation (quotes, hyphenation, markdown emphasis, split words); a row whose anchor is not found stays in the ledger tagged `anchor-verified: no` and is not citable by any desk (spine, tables, figures drop it); the critic rules on the readings and can re-anchor, never overrule the wall. This is already how every released engine runs.
3. **Reception themes.** The plan's themes are the spine and the readers' themes are additions, both labelled; passed to Codex as a design requirement for the reception map.
4. **One engine at a time.** A chosen path can be one step, so the Stacks can post the evidence index and ask for the fidelity audit alone; the executor API also runs a single engine without the desks. Codex validates "the fidelity audit alone from an evidence index" as its own condition.

## What changes on our side, in order

1. Codex: the three engines (running now), with the requirements above; then E3.
2. Claude: `SourceSpec.role`, the evidence index handled as described (not profiled; split into checks for the audit; plan as upstream context), tested offline with a hand-made index; then a local dossier over the pilot corpus through the three engines (the desk on Render is not needed for the pilot).
3. The pilot both ways from the same materials, after your `/api/cites/evidence` and `markers=1`; owner's read first, then Sonnet in both orders.

The cost concern is right and settled by the pilot: if the lane-as-planner-around-ledgers option wins, the bridge is engine calls with the evidence index, not whole dossiers.
