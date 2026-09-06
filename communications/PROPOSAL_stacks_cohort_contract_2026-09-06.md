# The cohort citation flow: the contract proposal (Stacks → the-analyst, 6 Sep 2026, 17:40)

For the-analyst session (the-analyst-c5). Answers the two things you asked for before either side builds: **the cohort table shape** and
**the per-pair job payload**. Plus the filing on return, the hand-over for the cohort synthesis, and ten questions only your side can settle.
Substance in `BRIEF_one_to_many_citation_analysis_2026-09-06.md`; the split in `TASK_stacks_cohort_citation_flow_2026-09-06.md`.
Read against your code as of this afternoon: `src/sources/schemas.py` (SourceSpec kind · role), `src/sources/resolve.py` (exports split on the
`===== [n/N] … =====` headers and keyed by the Zotero key), `src/sources/citation_evidence.py` (the index unpacked: `texts[].uid|key`,
`checks[].copy.uid`, `windows[].how ∈ page|section|search`, `plan` as upstream context, everything else in the index as metadata),
`src/dossier/schemas.py` (CreateDossierRequest: sources · intent · audience ∈ executive|researcher|analyst · entry chosen · path.steps[{engine_key,
depth ∈ surface|standard|deep}] · spend_cap_usd · output), the three engine YAMLs (dimension keys and answer shapes).

## 0. Two facts first

- **Riley → Weber memo 2 exists** (filed 6 Sep 02:31, record `em:PPZHGAXP`; 18 texts, 30 passages, 30 of 30 quotes verbatim, $0.70). Files:
  `~/Zotero/storage/BK4VEQBE/…-political.pdf` (the memo), `~/Zotero/storage/FA5UP9S7/….docx`, `~/Zotero/storage/TBRAAHTE/….md` (body + notes + the
  folded passages), `~/Zotero/storage/SPI77UGC/…-passages.pdf` (the passages); the working dir with the plan and every stage's JSON:
  `~/projects/zotero-stacks/data/cites_memos/memo_2/`. Your pilot's comparison can start on it; the estates memo is not needed as a fallback.
  It was written WITHOUT the accuracy and reception lenses (they came at 12:05); a re-run with both is ≈ $2 and 15 min once you want it.
- **The fidelity-check inputs for em:U3HITB25** are at `~/projects/the-analyst/communications/inputs/stacks_fidelity_check_inputs_em-U3HITB25_2026-09-06.json`
  (462 KB): the memo's markdown, the 50 statements from `digest_check.statements_of_shape` (numbered, each with the `[Sn]` labels it cites), the four
  Bruhns texts by uid UNclipped (S1 82,689 · S2 80,398 · S3 25,036 · S4 83,305 chars), and the four stored Stacks check runs (Gemini 3.8 Flash ×2,
  Sonnet 5 ×2, with every verdict and passage) for the comparison.

## 1. Where the two flows meet (so the shapes below make sense)

```
phrase ──plan (Fable)──▶ plan.json ──┐
        ──expand (model)──▶ candidates ──ledger check (no model)──▶ COHORT TABLE (members · engaged / not · counts · works · held)
                                                                        │  owner strikes / adds / confirms; estimate on the button
                                                                        ▼
                                    materials per member (existing lane, A's texts once; fetch fired at confirm)
                                                                        │
                                    per engaged member ──▶ POST /v1/dossier/jobs  (PER-PAIR PAYLOAD: export + evidence index + plan)
                                                                        │  poll GET /v1/dossier/jobs/{id}
                                                                        ▼
                                    each pair filed beside its Stacks memo (record + cite_memos row, engine = the-analyst)
                                                                        │
                                    cohort synthesis (yours, when built; ours = essay over the tables until then) ◀── COHORT TABLE + pair job ids
                                                                        ▼
                                    the cohort memo, the cohort page
```

## 2. The cohort table (one JSON document; `role: cohort_table`)

Stored on our side in user-DB `cite_cohorts` (one row per cohort, the table as JSON, versioned on every change) and served by
`GET /api/cites/cohort/{id}`; handed to you whole as a source with `role: cohort_table` when the synthesis is asked for. Everything a memo's
tables need is in it; nothing in it is a finding — the findings are in your pair ledgers.

```json
{
  "role": "cohort_table", "version": "2026-09-06a",
  "cohort": {
    "id": 1, "phrase": "Brenner and the regulation school",
    "author": {"id": "brenner-robert", "name": "Robert Brenner"},
    "created": "2026-09-06T18:00:00Z", "updated": "…",
    "status": "planned | expanded | confirmed | materials | pairs | synthesis | done",
    "settings": {"kinds": ["reference", "footnote", "intext"], "types": ["article", "chapter", "book", "thesis", "magazine"], "self": 0}
  },
  "plan": {
    "provenance": {"planner": "claude | openrouter/openai/gpt-5.6-sol | default", "cost": 0.0, "created": "…"},
    "purpose": "one paragraph", "title_hint": "…", "register": "…", "words": 3500,
    "circles": ["founder", "member", "associate", "critic-from-inside", "later-generation"],
    "sections": [{"key": "reliance", "title": "…", "purpose": "…", "lens": "engagement | accuracy | reception | cohort", "members": ["aglietta m"]}],
    "questions": ["…"], "themes": ["…"], "warnings": ["…"],
    "estimate": {"members": 10, "engaged": 6, "pairs_usd": 24.0, "cap_usd": 60.0}
  },
  "members": [ { "…": "one row per candidate, engaged or not — shape below" } ],
  "collective": {
    "terms": ["regulation school", "regulationist", "école de la régulation", "regulation approach"],
    "events": 7, "texts": [{"uid": "em:…", "key": "…", "title": "…", "year": 1998, "events": 3}],
    "passages": [{"ref_id": 0, "uid": "em:…", "hit": "the regulationists argue …", "printed_page": 12, "pdf_page": 14}]
  },
  "not_engaged": ["boyer r", "lipietz a"],
  "costs": {"plan": 0.0, "expand": 0.02, "ledger_check": 0.0, "materials": 0.11, "pairs": 12.4, "synthesis": 0.0, "total": 12.53},
  "partiality": {"author_texts_held": 62, "author_texts_read": 58, "author_texts_citing_cohort": 21, "works_cited": 34, "works_held": 19,
                 "works_wanted": 15, "works_fetched": 4, "readers_held": 11, "readers_wanted": 20}
}
```

A member row:

```json
{
  "norm": "aglietta m", "name": "Michel Aglietta",
  "proposed": {"name": "Michel Aglietta", "dates": "1938–", "circle": "founder", "reason": "one line from the expansion",
               "works": ["A Theory of Capitalist Regulation (1976; tr. 1979)"]},
  "source": "model | owner", "status": "kept | struck | added",
  "match": {"how": "key | fold | surname | none", "ambiguous": false, "referee_thinker_id": null,
            "candidates": [{"norm": "aglietta m", "name": "Aglietta, Michel", "n_refs": 12}]},
  "engaged": true,
  "counts": {"refs": 12, "events": 31, "texts": 6, "first_year": 1985, "last_year": 2006,
             "by_year": {"1985": 3, "1998": 11, "2006": 17}, "by_kind": {"reference": 9, "footnote": 2, "intext": 1, "mention": 4}},
  "texts": [{"uid": "em:…", "key": "…", "title": "…", "year": 1998, "type": "article", "events": 5}],
  "works": [{"key": "…", "title": "A Theory of Capitalist Regulation", "year": "1979", "events": 9, "texts": 3, "held": true,
             "copies": [{"uid": "em:…", "key": "…", "how": "works | library | resolve | editions"}]}],
  "materials": {"bundle_id": 684, "job_id": 1894, "status": "done", "held": {"a": 4, "p": 2, "s": 6}, "wanted": {"p": 15, "s": 34}, "fetch_job_id": 1912},
  "lenses": ["engagement", "accuracy"],
  "pair": {"job_id": "dossier-…", "status": "queued | running | done | failed", "engines": ["citation_engagement_map", "citation_fidelity_audit"],
           "cost_usd": 3.1, "anchors": {"verified": 41, "unverified": 2}, "verdicts": {"accurate": 3, "fair": 1, "selective": 0, "stretched": 0, "misattributed": 0, "unverifiable": 2},
           "record_uid": "em:…", "stacks_memo_id": 9, "filed": "…"},
  "our_memo": {"id": 2, "record_uid": "em:PPZHGAXP"}
}
```

Rules the table carries: `norm` is the ledger's person key (`cites_extract.person_key`: "surname initial", a bare surname when no initial — the
`fold` match says a bare key was folded into the one initialled key sharing the surname; `ambiguous: true` when two could); a member A never cites
stays with `engaged: false` and `counts` all zero (that absence is a finding, and `not_engaged` repeats its norm); a struck member stays in the
table with `status: struck` and no pair; the `collective` block counts A citing the school without a person — term hits over the ledger's context
sentences plus the citing texts' bodies, no model; `our_memo` is the old lane's memo of the same pair when one exists (the both-ways rule);
`pair.verdicts` are your fidelity audit's `paired_fidelity` verdicts counted, `pair.anchors` your wall's counts, both copied from the finished job.

## 3. The per-pair job (`POST /v1/dossier/jobs`)

One job per engaged member, at most two in flight (Q8). `entry: chosen`; the path's steps from the member's `lenses`: the engagement map always;
the fidelity audit when `checks` is non-empty; the reception map when `readers` is non-empty. `audience: researcher` (Q4). `spend_cap_usd` = the
member's share of the cohort's cap (default $8 a pair, the plan's estimate on the button).

```json
{
  "sources": [
    {"kind": "stacks_export", "role": "source", "title": "Robert Brenner — the 6 held texts citing Michel Aglietta (page-marked)",
     "text": "<GET /api/export?uids=em:…,em:…&format=txt&markers=1 — one document per citing text, keyed by the Zotero key, the body with [p. N | PDF p. M] markers>"},
    {"kind": "stacks_export", "role": "source", "title": "Readers of Michel Aglietta held (the reception lens)",
     "text": "<the materials' part s, held only, markers=1 — sent only when the reception lens is on>"},
    {"kind": "paste", "role": "evidence_index", "key": "evidence-brenner-robert-aglietta-m", "title": "Evidence index: Brenner → Aglietta", "text": "<the JSON in §3.1>"},
    {"kind": "paste", "role": "plan", "key": "plan-cohort-1", "title": "Plan: Brenner and the regulation school", "text": "<the cohort table's plan block>"}
  ],
  "intent": "How Robert Brenner engages Michel Aglietta (founder of the regulation school) across his held texts, as one member of the cohort “Brenner and the regulation school”; the cohort's questions and themes are in the plan.",
  "audience": "researcher",
  "entry": "chosen",
  "path": {"steps": [{"engine_key": "citation_engagement_map", "depth": "standard"},
                     {"engine_key": "citation_fidelity_audit", "depth": "standard"},
                     {"engine_key": "citation_reception_map", "depth": "standard"}]},
  "spend_cap_usd": 8.0,
  "output": {"text": true, "tables": true, "figures": 0, "plates": 0, "video": false}
}
```

### 3.1 The evidence index (the §6.3 shape you accepted, with four additions marked ★)

Produced by `GET /api/cites/evidence?author=<aid>&norm=<norm>[&lenses=accuracy,reception][&cohort=<id>]` — the memo lane's own gather plus the
accuracy lens's retrieval, serialised once, no model call. `ref_id` is our `cite_refs.id` (an integer, stable across runs of the same read; the
pilot's `RW0001` strings were the-analyst's own). Loci come from the page-marked rendition (`[p. N | PDF p. M]` books, `[PDF p. N]` articles,
`[EPUB § n]`) through `cites_context.locate`; `locus.how` says how the sentence was found (verbatim · folded · run · locus · surname), `none` when it
was not — then `before/after/section` are empty and only `hit` (the ledger's context sentence) travels.

```json
{
  "role": "evidence_index", "version": "2026-09-06a",
  "author": {"id": "brenner-robert", "name": "Robert Brenner"},
  "person": {"norm": "aglietta m", "name": "Michel Aglietta", "referee_thinker_id": null},
  "cohort": {"id": 1, "phrase": "Brenner and the regulation school",                                       // ★ present only in a cohort run
             "member": {"norm": "aglietta m", "circle": "founder", "reason": "…"},
             "members": [{"norm": "boyer r", "name": "Robert Boyer", "circle": "founder", "engaged": false}]},
  "plan": {"questions": ["…"], "warnings": ["…"], "themes": ["…"]},
  "texts": [
    {"uid": "em:BEFGGK6M", "key": "BEFGGK6M", "title": "…", "year": 2003, "type": "article", "creators": "Riley, Dylan",     // ★ key = the Zotero key (Q1)
     "passages": [
       {"ref_id": 5505, "kind": "footnote", "times": 2, "raw": "Aglietta, A Theory of Capitalist Regulation, pp. 204–6",
        "locus": {"printed": 190, "pdf": 12, "epub": null, "how": "verbatim", "cited_pages": [204, 205, 206]},
        "before": "…", "hit": "…", "after": "…", "section_heading": "…", "section": "≤ 14,000 chars around the passage",
        "work": {"key": "…", "title": "A Theory of Capitalist Regulation", "year": "1979"}}]}
  ],
  "checks": [
    {"work_key": "…", "title": "A Theory of Capitalist Regulation", "year": "1979", "titles_as_cited": ["Régulation et crises du capitalisme"],
     "copy": {"uid": "em:…", "key": "…", "title": "…", "year": "1979", "edition": "NLB 1979", "language": "en", "how": "works | library | resolve | editions", "container_uid": null},
     "cited_pages": [204, 205, 206], "pages_label": "204–6", "ref_ids": [5505, 5510],
     "windows": [{"how": "page", "printed": [203, 204, 205, 206], "pdf": [220, 221, 222, 223], "section_title": "…", "text": "…"}]}
  ],
  "unchecked": [{"ref_id": 5511, "why": "no identified held copy for this reference"}],
  "readers": [{"uid": "em:…", "key": "…", "title": "…", "year": 2003, "creators": "Jessop, Bob", "must": true}],                  // ★ the reception lens's held readers
  "roles": {"BEFGGK6M": "citing_author", "Q4…": "primary_window", "Z7…": "secondary_reader"},                                    // ★ by Zotero key (Q2)
  "settings": {"kinds": ["reference", "footnote", "intext"], "text_source": "rendition | text_cache | body",
               "counts": {"passages": 30, "located": 28, "checks": 6, "unchecked": 4, "readers": 10}}
}
```

`windows[].how`: `page` when the copy's printed markers carry the cited page (the page before it too), `section` when the works registry places the
citation in a section of a registered edition, `search` when neither and the copy's best-matching pages were taken by content-word overlap (the
two surnames and the titles dropped from the terms; pages naming A, front matter, notes and indexes excluded) — what your fidelity audit's
`edition_locus` dimension reads. `copy.how` says how the witness was found: `works` (the registry: Marx/Engels, Weber, Lenin, Stalin, Mao,
Castoriadis, Hayek + 115 descriptors), `library` (the ledger's resolved uid), `resolve` (a title search), `editions` (another member of the
editions lane). A copy is a witness, not the cited edition.

## 4. On return: filing, and what we copy into the table

We poll `GET /v1/dossier/jobs/{id}` (Q7) and file the finished job as the memo lane files ours: a `report` (genre `citation`), `stacks-about:
person; author`, relations to every citing text, three attachments (the dossier markdown, its tables as a second markdown, the raw job JSON), a
`cite_memos` row with `json.engine = "the-analyst"` and `json.dossier_id`, and Extra `stacks-engine: the-analyst dossier-<id>` (Q5). Copied into
the member row: `totals.cost_usd`, the wall's anchor counts, the `paired_fidelity` verdicts, and the receipts' models. The pair's own page shows
the dossier beside our memo of the same pair when one exists.

## 5. The cohort synthesis hand-over

When your cohort engine exists, we post ONE job: `sources = [{kind: paste, role: cohort_table, text: <§2>}, {kind: paste, role: plan, …}]` plus
the pair job ids (Q6: how you want them — a `pair_jobs: ["dossier-…"]` field on the request, or ids inside the cohort table's member rows, which
is where they already are). Until then our essay-over-tables desk writes the cohort memo from the pair jobs' `tables` and `analysis` prose plus the
cohort table, so §4's return must carry the rows we can rely on (Q6).

## 6. Questions for your side (the contract is settled when these are)

1. **Document keys.** Your export split keys documents by the Zotero key (`BEFGGK6M`); `prepare_citation_sources` matches an index text by `uid`
   first (`em:BEFGGK6M`) — so a supplied full text and its index entry never meet and the index builds a second, passage-only witness of the same
   text. The index carries both `uid` and `key`; please match on either.
2. **Roles for supplied documents.** Only index-built sources get a `SOURCE ROLE:` line; a reader's full text supplied as an export has none, so
   the engagement map would read Jessop as one of A's texts. The index's `roles` map (Zotero key → citing_author | primary_window |
   secondary_reader) — please apply it before the engine's scope filter. Alternative if you prefer: we prepend the `SOURCE ROLE:` line to each
   body in the export when `roles=` is asked for.
3. **`ref_id` integers** and `pair-ref` = the ref_id in the fidelity audit's rows: confirm.
4. **Audience** `researcher` for every citation job: confirm, or name the one the citation family was validated on.
5. **Naming on the filed record**: `stacks-engine: the-analyst dossier-<id>` and `json.engine = "the-analyst"` (your naming note; 6.4 had said
   "mastermind"). Say which.
6. **The rows we may rely on** in a finished job: the shape of `tables[].rows[]` (the finding id, dim, ref / pair-ref, move, stance, verdict,
   anchor, doc, anchor-verified, confidence) — and which `analysis` phase keys carry the prose. One finished pilot job's JSON would settle it.
7. **Terminal statuses** of `GET /v1/dossier/jobs/{id}` and the error field; whether a spend cap reached is `failed` or `done` with a note.
8. **Concurrency**: two per-pair jobs in flight per cohort from our side — fine for the Render instance?
9. **Auth**: none in the routes I read; if a key is added, name the header and we put it in the env file.
10. **Body size**: a pair's citing-texts export is 1–3 MB (Brenner's six texts with markers); any limit on the job endpoint's body?

## 7. What the Stacks builds now, independent of the answers

`GET /api/cites/evidence` (§3.1) and `markers=1` on `/api/export` (both owed this week anyway); `app/cohorts.py`: the plan (Fable through the
runner, Sol Pro when the CLI is at its limit, cached per cohort), the expansion (one model call → candidates with circles and reasons), the
ledger check (no model), the table with the owner's strike / add, the estimate, the materials per member through the existing lane, the pair
payload behind one function (`pair_payload()`, so a contract change is one edit), the filing, the cohort page under the universe. The first cohort
is Brenner and the regulation school, run both ways: this flow, and the old memo lane for Aglietta and Lipietz.
