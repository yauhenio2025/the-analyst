---
name: zotero-and-idea-texts
description: Where the owner's papers live — Zotero at ~/Zotero/zotero.sqlite (52K items, PDFs under ~/Zotero/storage/<attachment key>/), idea-centred markdown texts in ~/projects (Deutschmann, Castoriadis), and the assembled ideas corpus for engine checks
metadata:
  type: reference
---

Zotero: `~/Zotero/zotero.sqlite` (copy before querying; 52,641 items; collections such as `radical philosophy`, `hegel`, `castoriadis_primary`, `marx & engels collected works`, `platform_capitalism`); PDFs at `~/Zotero/storage/<attachment item key>/<filename>` (the `itemAttachments.path` is `storage:<filename>`; the folder is the attachment's own key, not the parent's). `pdftotext -enc UTF-8` extracts cleanly. Ready markdown texts in `~/projects/`: Deutschmann 2001 ×2 and 2022 (capitalism as religion), Castoriadis 1984/1990/1997 essays; `~/projects/markus/` has Márkus PDFs; `~/projects/echeverria/` extracted texts.

Assembled ideas corpus for engine checks: `~/projects/the-analyst/data/study/sources_ideas/` with `PROVENANCE.md` (untracked; regenerate from the keys there).

**How to apply:** when the owner asks to test engines on "material about ideas rather than geopolitics", start from that folder; for new material query the Zotero copy by title keywords and collection. Related: [[engine-redesign-process-shape]].
