# Source read: citation fidelity audit, index-only condition, repaired framing with the two card rules (Claude, 2026-09-06 night)

Output: `data/study/citation_family_2026_09_06/repairs/outputs/G6__index_only_repair.md` (the re-run after the card rules; four calls, $2.06). Output SHA256: 011654d0e2ae968ecb65478efb5854d02267cb76b387aecce7eb8c2670348de9. Written before any score. This supersedes the read of the earlier attempt (kept below the line as the record of what the card rules fixed).

**Walls.** 28 rows, 27 verified; every row is a cross-document pair with two keys. The one failure, F19, is the pair the previous attempt judged from memory: it is now `verdict: unverifiable` with `how: page`, and its Weber anchor is a faithful copy of the OCR-garbled page ("the prillcipk ,)f official jurisdictional ar-eas") that fails only because the model silently corrected the page's first word ("tilere" → "There"). The wall is right to refuse a corrected quote; the row is tagged and the desks drop it; the verdict stands as unverifiable, which is what the card rule asked for.

**The card rules held.** Every paired_fidelity row carries `verdict:` as a field (accurate 5, fair 9, selective 5, stretched 1, unverifiable 8) and `how:` (page 21, search 7). No row judges a place the window does not carry: the eight unverifiable verdicts name the reason (editorial matter retrieved, the wrong pages for a locus, an edition mismatch, the cited work not held).

**Against the earlier attempt.** The verdict distribution is stable on the checked pairs read before: RW0016 stretched, RW0045 fair, RW0048 selective, RW0076 accurate, RW0085 fair; RW0042 (the patrimonial office) stays accurate with its anchor now verifying; RW0078 moves from a memory-based "selective" to unverifiable. The sample-practice row names the one expressly marked adaptation and confines itself to the checked sample. Eight unverifiable pairs out of twenty-eight is the honest count for this corpus: three cited works are not held, two loci are outside the copies' editions, and the pdftotext windows of Economy and Society are OCR-noisy.

**Disposition.** Release under the standard: 27/28 anchors with the failure tagged and dropped by the desks; no fabrication or attribution reversal in the rows read; an inventory judged by rows, anchors and this read; nothing rejected reaches a table cell. Design notes carry over: the Stacks' page-marked rendition instead of pdftotext windows; sections from the works registry when it lands.

---

## Earlier attempt (before the card rules)

### Source read: citation fidelity audit, index-only condition with the repaired framing (Claude, 2026-09-06 evening)

Output: `data/study/citation_family_2026_09_06/repairs/outputs/G6__index_only_repair.md` (assembled from the last raw response `0004.md` after the contract change; no new call). Written before any score. Codex is at its usage limit; this read and the disposition are mine.

**Walls.** 29 rows, 26 verified after the quotation-mark fix to the normaliser (before it, 23: the model writes ‘Power’ where the page has Power). The three that fail: F10 (Weber's patrimonial-office sentence, quoted by Riley verbatim and copied by the reader; not found in the page window because the pdftotext of Economy and Society is OCR-noisy on that page), F14 (the Tolstoy question from *Science as a Vocation*, quoted in the other translation, from memory), F19 (Weber on patriarchal domination, quoted from memory because the retrieval for printed p. 956 landed in the volume's notes section). All three are tagged `anchor-verified: no` and `unverified` where cited; the desks drop them.

**Seven pairs read against the index's A passage and W window.**

| pair | Riley's use | the audit's verdict | my read |
|---|---|---|---|
| RW0016 (F7) | *Routes or Rivals?* 2013: political capitalism's higher returns are "the key to understanding imperialism", quoting E&S 919 | stretched: the window supports imperialist profitability and the prognosis, not declining returns in rational capitalism | holds. Weber's 918–919 gives the profit interests of war suppliers and the prognosis; the declining-returns contrast is Riley's reconstruction. "Selective" would also be defensible; "stretched" is not wrong |
| RW0045 (F11) | *Faultlines* 2020: "Adapting Weber's concept of Roman 'imperialist capitalism'" → political capitalism, E&S 917 | fair, expressly marked adaptation | holds; the audit rightly credits the explicit marking |
| RW0048 (F12) | *Social Foundations of Positivism* 2021: Weber 1978: 86–90 listed among "externalists" who tie positivism to industrialization | selective | holds, and is generous: pp. 85–90 are formal and substantive rationality of economic action; nothing there ties positivism to industrialization. "Stretched" is arguable |
| RW0076 (F17) | *Relational Power Theory* 2024: Weber's definition of power, E&S 53 | accurate | holds; the witness carries the definition word for word |
| RW0042 (F10) | *What Is Trump?* 2018: Trump as patrimonial household head, quoting E&S 1028–31 on the patrimonial office | accurate | holds on substance; the anchor fails only because the OCR'd window does not carry the sentence cleanly. A limit of my page windows, not of the reading |
| RW0078 (F19) | *Relational Power Theory* 2024: formal vs informal power, citing E&S 956, 1006, 1112 | selective | **does not hold as given**: the retrieved window for 956 is the notes section, so the reader had no witness for the claim and supplied Weber's words from memory. The right verdict was unverifiable. The judgment may be correct, but it is not evidenced |
| RW0085 (F26) | *Rise of Political Capitalism* 2025: workers organising by ethnicity or credential form an "estate" (Weber 1922: 180) | fair, preserving non-reduction to class | holds; MWG I/23 §2 (Klassenlage) at the marginal page carries Weber's class/estate distinction; the credential example is Riley's application |

**What the output does well.** The position map over Riley's thirty texts is accurate where I could check it (the 2013, 2018, 2020, 2021, 2024, 2025 rows); unverifiable pairs are stated as such with the reason (editorial matter retrieved, wrong edition, uncited work not held) rather than judged; the practice conclusion is confined to the checked sample and names the one expressly marked adaptation. This is an audit a scholar of Riley could use.

**Defects.** (1) Judging without a witness: F19, and the audit should treat "window does not carry the cited matter" as unverifiable by rule, never quote the cited author from memory. (2) Shape: the verdict lives inside the finding sentence ("fairly", "accurately", "stretched") rather than in the `verdict:` field the answer shape asks for, and `how: page | section | search` is not carried; the desks lift fields, so both must be fields. (3) OCR: two of three anchor failures come from my pdftotext windows; the Stacks' page-marked rendition should be cleaner, which is one more reason for the bridge's `markers=1`.

**Disposition.** Release after two card lines (no witness → `unverifiable`, never from memory; verdict and how as fields) and one re-run of this condition; anchors 26/29 with the failures tagged and dropped by the desks meets (a); no fabrication survives untagged (b); this is an inventory judged by rows, anchors and this read (c); no rejected row reaches a table cell (d). Cost of this condition so far: $1.77 (four calls) plus the $8.87 full-source condition that refused and stays withheld as a condition, not a method.
