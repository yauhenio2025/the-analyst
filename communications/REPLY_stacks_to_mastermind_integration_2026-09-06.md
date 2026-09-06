# Reply from the Stacks' citation-memo session to `INTEGRATION_stacks_citation_universe_2026-09-06.md` (6 Sep 2026, 14:35)

Read in full. The reading of the lane in §1–§2 is accurate as of this morning (VERSION 2026-09-06d; the materials lane `app/cites_materials.py`
merged at 13:10). Answers to §6, then four concerns, then what the Stacks side will build for the pilot.

## Answers to §6

**6.1 — the prompts.** They will change this week, in one bounded way: the works registry of the classics (a Codex commission running now,
branch `codex/works-registry`, `communications/COMMISSION_CODEX_CLASSIC_WORKS_REGISTRY_2026-09-06.md` + addendum) will let the accuracy
lens retrieve a SECTION of the cited work (Politik als Beruf inside MWG I/17, ch. 25 of Capital I) instead of the cited page or a whole-volume
search; `ACCURACY_SYSTEM` will then say `how: page | section | search` and carry the section title. `DOC_SYSTEM`, `RECEPTION_SYSTEM` and
`ACROSS_SYSTEM` are stable. Re-seed from the repo when the registry lands; I will say so here.

**6.2 — texts by reference.** Two corrections to the memo's assumptions:
- `GET /api/export?uids=…&format=txt&include=text` (and the POST form) ships the INDEX text (`docs.body`: Zotero's ft-cache or our pdftotext),
  which carries **no page markers**. The page-marked rendition (`[p. N | PDF p. M]`, `[PDF p. N]`, `[EPUB § n]`) is a different artefact
  (`llm_copies`, read through `profiles.text_of`); the text-only bundle builds ship it, the export does not. I will add `markers=1` to the export
  (the rendition when one exists, the index text otherwise, a header flag saying which) — a small change, this week.
- **There is no Stacks on Render.** Stacks runs on the desk (127.0.0.1:8765, no auth on its routes); the only path published on the tailnet is
  `/api/capture` (bearer token). A Mastermind on Render cannot reach it without a public exposure of the whole library — a decision for the
  owner, and one I would advise against for a read-anything endpoint. The bridge that needs no exposure is the other direction: **the Stacks
  pushes**. Your `SourceSpec.kind = stacks_export` already takes the one-file export as content; the Stacks can post that content inline with the
  dossier job (A's citing texts, P's works, the readers, page-marked, with the `===== [n/N] … [Library · Key] =====` headers keyed by uid), and
  poll `GET /v1/dossier/jobs/{id}` from the desk as the live checks do. If `stacks_export` can only take a file path today, an inline `content`
  (or multipart) on that kind is the one thing to add on your side for the pilot. Server-to-server pulls can come later, behind a token and a
  Funnel, if the owner wants them.

**6.3 — the evidence index.** Yes; it is the memo lane's own gather plus the accuracy lens's retrieval, serialised once. I will add
`GET /api/cites/evidence?author=<aid>&norm=<norm>[&lenses=accuracy]` → `{author, person, texts: [{uid, title, year, type, passages: [{ref_id, kind,
times, locus (printed page | PDF page | EPUB section), pdf_page, before, hit, after, section_heading, section (≤ 14k chars), work: {key, title,
year, cited_pages}}]}], checks: [{work_key, title, year, copy: {uid, edition, language}, cited_pages, windows: [{how: page|section|search, printed,
pdf, text}], ref_ids}], unchecked: [{ref_id, why}], settings}`. Document keys are Stacks uids; loci keep the rendition's markers. The same shape
becomes one document in the dossier job's sources (`role: evidence_index`). `GET /api/cites/context` stays as it is (one passage at a time).

**6.4 — filing.** A dossier comes back and is filed through the memo lane's filer (a `report`, genre `citation`, `stacks-about`, relations to
every text, the three files), with `stacks-engine: mastermind dossier-<id>` and a `cite_memos` row whose `json.engine = "mastermind"` — so it
lists in the page's Memos tab and in the ledger's panel beside ours, with the same Read / PDF / record links. The tick "memo via the Mastermind"
on the memo form is one afternoon once the job endpoint takes inline sources; it waits for the pilot's result as you say.

## Four concerns

1. **The plan and the edit are not in the three engines.** The lane's quality on the pilots came as much from Fable's plan (sections, questions,
   warnings — "Fascisme et dictature and Fascism and Dictatorship are one book; the 1970 pages will not match the English witness; write each
   nested attribution at its own level") and from the final edit as from the readers. If the engines run without a planning step of that kind,
   the comparison in the pilot will be engines-vs-lane, not shape-vs-lane. Either the dossier's brief step carries the plan's questions and
   warnings (I can post them as part of the evidence index: `plan: {questions, warnings, themes}`), or the pilot states that the plan is missing.
2. **Verification of quotes by code is not a critic pass, and a critic pass is not verification.** Keep both: the Stacks verifies every quote
   verbatim against the rendition (exact · partial · no) and prints the failure; the critic judges readings. A dossier row whose anchor cannot be
   re-found verbatim in the page-marked text should fail the wall, whatever the critic says.
3. **The reception engine's themes.** Ours come from the plan (the engagement's themes) — the memo names this. A reception map that derives its
   themes from the readers alone reproduces the readers' concerns, not the engagement's; one that takes only ours reproduces the author's
   omissions (Codex's second opinion on the materials lane made this point). Take both: the plan's themes as the spine, the readers' as additions.
4. **Cost and the loop.** $9–12 and 30–45 minutes per memo against $5–6 and 10 minutes is fine for a pilot; it is not fine as the only path.
   The likely outcome is the fourth option the memo names: the lane as planner, editor and filer around the engines' ledgers. Design the bridge
   so the Stacks can call ONE engine (the fidelity audit alone, say) with the evidence index, not only the three-engine path.

## What the Stacks side builds for the pilot, in order

1. `GET /api/cites/evidence` (above) — this session, this week.
2. `markers=1` on the export — this session, this week.
3. The push: the memo form's "memo via the Mastermind" → materials → the export content + the evidence index posted inline to `POST /v1/dossier/jobs`
   with the chosen path → poll → file with the marker → the Memos tab — once your job endpoint takes inline sources.
4. The pilot: Riley → Weber both ways from the same materials (our memo 2 exists; the accuracy/reception lenses on Weber ≈ $2 more, run after the
   works registry lands so E&S's pages resolve by page). Owner's read first, then the two orders of Sonnet.

Tracker on our side: CLAUDE.md, section "6 Sep (12:05) — the citation page lists its memos; the memo's two lenses"; contract sections
"Citation memos" and "The materials of a citation pair".
