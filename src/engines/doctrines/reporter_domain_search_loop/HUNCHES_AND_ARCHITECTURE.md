# The Reporter — hunches and architecture (2026-09-03)

Written from the owner's dictation (`dictations/DICTATION_2026-09-03_the_reporter_VERBATIM.md`) and two code studies (`STUDY_websaver_archivist_oaas.md`, `STUDY_reader_referee_gsrevamp.md`), plus the Syllabus corpus memo (`.secrets/`). Hunches are marked H#; each says what would confirm or kill it.

## 1. What The Reporter is, in one sentence
A **commissionable organ** that answers "what has the press said about X, and what does it mean for me" with a brief that shows its sources, its gaps and its analysis — the news counterpart of the Referee (scholarship) and The Analyst (analysis), triggered from either.

## 2. Hunches
- **H0 — The loop is the product.** (Owner, after reading the first draft: "the most important part is being able to conduct searches on Google inside the domain… dynamic search where we figure out what terms represent the topic, do different combinations, evaluate the results, figure out what other terms to plug based on those results, and so forth — LLM-powered, context-sensitive search with us evaluating the results.") Websaver's stored data is incidental; its adaptive-exhaustion loop and gs_revamp's lane/effector/budget loop are the lineage. Confirm: on the demo topic the loop harvests terms the operator did not seed (e.g. named disputes, company names, dates) and the judged slate beats a one-shot query on precision and coverage.
- **H1 — Disaggregate by function, not by product.** The owner: "it's a bunch of functions, and maybe we need to disaggregate them into several services." Functions: *recall* (stored), *search* (fresh), *fetch* (entitled full text), *catalog*, *analyse* (Analyst), *present* (library), *film* (Wirecut). The Reader stays "a parcel of newsletters"; the Archivist's press stack becomes the Reporter's core; Websaver is not revived, only mined. Confirm: one brief flows through all lanes with separate receipts per lane.
- **H2 — Free recall before paid search pays for itself.** Three stored sources exist already (Reader 151K appearances; Syllabus corpus 446K long-form articles incl. FT 4.5K, WSJ 3.7K, Economist 1.6K, Bloomberg 518; Archivist bodies). For most topics the recall set is enough for a first brief; fresh search fills the last months. Confirm: measure recall/paid ratio on the demo topic.
- **H3 — Full text with entitlements only works from a machine that is logged in.** Websaver proved cookie re-injection fails; the Archivist's daemon ladder (web-auth providers via the Oxylabs Unblocking Browser, else a copied cookie profile) is the only road that worked. So the fetch lane runs on desktop-proper as a timer/daemon, not on Render. Kill: if the Syllabus web-auth providers cover FT/Economist/Bloomberg/NYT/WSJ headlessly, the daemon can move to Render.
- **H4 — The Analyst is the analysis; the Reporter only feeds it a bundle.** The headed-bundle shape (stacks export) is already the Analyst's native input; briefs are dossiers whose sources are press items. Confirm: one recall set → one dossier with diagrams via the public API, no Reporter-side prompts about content.
- **H5 — The Referee's Study lane is the button.** `compose_query_brief` → `POST /runs` → signed webhook is a proven contract; clone it, change the payload (papers, date window, sites). Confirm: click → brief link on the query page within one poll cycle.
- **H6 — Historical depth is the differentiator.** The Syllabus corpus reaches the 1950s (NYRB, The Nation, New Yorker, LRB, Commentary). A brief on "labour protest and AI" can show how the argument has been made about automation since the 1960s — nobody else in the room has that. Requires the jina embedding sidecar. Confirm: a decade-bucketed recall on the demo topic returns readable articles per decade.
- **H7 — Honest gaps are the product.** Like the Archivist's Assignment Loop: what was searched, found, parked behind paywalls, skipped, and why. Executives trust a brief that names what it could not read.

## 3. Sources and their limits (from the studies)
| Source | Access | Limits |
|---|---|---|
| The Reader | Basic-auth JSON API | newsletter prose only (never the linked article); FTS is AND-of-terms; snapshot frozen 2026-08-29; WSJ/Economist absent |
| Syllabus corpus | prod Postgres (read-only) | needs the jina model to embed queries; no tsvector on chunks (ILIKE times out); 13% undated |
| Archivist bodies | its Postgres + `/search` | 426 bodies; `GET /` 500; PDF→S3 unwired |
| Fresh SERP | Oxylabs URL-mode (works), Apify (Scholar actor only today) | no `site:` code yet in gs_revamp; Apify web-SERP actor unverified |
| Entitled fetch | desktop daemon ladder | WSJ banned a VM IP once; Bloomberg/WSJ/NYT need desktop cookies; teasers must be parked |

## 4. Contracts (draft)
- `POST /v1/briefs` → 202 `{brief_id}`; body: `{objective, papers[{title,authors,year,venue,doi,abstract,link}], date_window{from,to}, sites[], budgets{serp_queries,fetches,usd}, sources{reader,corpus,archivist,web}, audience, deliverables{webhook_url,secret}, caller{system,ref}}`.
- `GET /v1/briefs/{id}` → `{status, plan, lanes{reader,corpus,archivist,web:{searched,found,kept,parked,skipped}}, items[], analyst{job_id,dossier_url}, receipts, totals, brief_url}`.
- Webhook `POST {deliverables.webhook_url}` signed `X-Reporter-Signature: sha256=HMAC(secret, body)`.
- Events: reuse The Analyst's `run_events` shape (seq, kind, phase, detail, narrator, cost) so one console can show both.
- Analyst handoff: `POST /v1/dossier/exemplars {name: "brief-<id>.txt", text: <headed bundle>}` then `POST /v1/dossier/jobs {sources:[{kind:"exemplar",name}], entry:"use", intent:<objective>, audience, depth, output{figures:2}}`.

## 5. Demo slice for the client-type audience
Objective: "labour protest and AI — what the NYT, FT, Economist and Bloomberg have said, 2023–2026, against the 15 papers from the Referee." Show: (1) the button on the Referee query; (2) the Reporter's plan (angles, outlets, budgets); (3) recall counts per lane incl. decade buckets from the corpus; (4) fresh items with full text where entitled and parked teasers named; (5) The Analyst's dossier with a spectrum/flow diagram; (6) the brief in the library with receipts. Pre-bake one brief; run one live recall in the room.

## 6. Open questions for the owner
1. Should the Reader get a Gmail worker now (it is frozen at 2026-08-29)?
2. Which outlets are entitled today, and on which machine are the logins (desktop-proper)? Confirm the Syllabus web-auth provider list covers FT/Economist/Bloomberg/NYT/WSJ.
3. Rotate the Websaver-era subscription secrets before anything ships beyond the owner.
4. Wirecut integration: is there an HTTP entry for "make a film from this text" or only the desk?
5. Name in the room: "The Reporter" (default) or "the news desk".
