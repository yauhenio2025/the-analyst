# A question across an author's accumulated work

The author's question is the entry point. The existing `oeuvre_position` recipe asks where one focal paper belongs in an author's trajectory; this workflow instead asks what the author says about a subject across the held corpus. Riley on worker organizing, labor resistance and protest is the motivating case. This does not run a Riley investigation or claim an answer from unexamined material.

The Brenner/Regulation study contributes a strict distinction between inventory, citation identity, engagement and absence; the Riley/Weber pilot contributes primary passages kept beside the memo. The new method keeps those disciplines while allowing direct topic discovery and semantic profile triage independently of citation matches. Existing citation and oeuvre engines remain unchanged.

## Contract

Create an engines-only dossier:

```json
{
  "entry": "chosen",
  "path": {"chain_key": "author_investigation"},
  "intent": "Does Riley discuss worker organizing, labor struggle or resistance?",
  "audience": "researcher",
  "sources": [{"kind": "paste", "role": "author_investigation", "key": "investigation", "text": "JSON packet"}],
  "output": {"text": false, "tables": false, "figures": 0, "plates": 0},
  "spend_cap_usd": 8
}
```

The packet contains `kind`, `author:{id,name}`, `question`, `scope:{year_from,year_to,historical_context,context}`, complete `primary` inventory, `secondary`, `prior_readings`, `prior_investigations`, `referee`, and `limits:{max_read_texts,max_primary_chars}`. Every primary row has `uid,title,year,body,read_uid,profile,citations`, optionally bibliographic date/edition metadata, `body_state`, `in_scope`, `date_scope` and an exclusion reason. Missing/excluded bodies remain inventory rows. Secondary rows have `uid,title,kind,body`. Citation rows carry canonical `key`/`work_key`, context and holding/Referee identities supplied by Stacks.

The source adapter separates original bodies into stored `primary:<uid>` / `secondary:<uid>` documents and stores the full metadata packet as a plan. It computes a SHA-256 for each supplied rendition. It neither fetches replacement bodies nor assumes that a book container is a contributor's own text. Stacks owns authorship/date/holding selection.

Read every checkpoint with `GET /v1/dossier/jobs/{id}/investigation`, including failed, cancelled and in-progress jobs. The standard job endpoints provide errors, cancellation and resumption.

## Execution and persistence

Four registered method records and a workflow/recipe drive a dedicated dossier executor:

1. `author_investigation_plan` reads the question, compact inventory summaries and bounded prior context. It produces subquestions, expanded literal search phrases and reuse/gap leads.
2. Code searches every eligible supplied primary body, saves complete per-query counts with up to twelve contextual matches per query/text, and follows canonical cited-work identities one hop. These are discovery leads, never engagement findings. `author_investigation_triage` sees **every full supplied primary profile**, including lexical misses and missing/excluded/undated rows. Triage batches reduce repeated search/citation contexts; complete artifacts remain in the frozen packet and research state. A compact global reconciliation with the same registered engine compares all prior decisions across subquestions and date scopes before selecting the route.
3. `author_investigation_read` reads selected primary texts whole when they fit, otherwise exact disjoint context windows around hits, the triage engine's proposed terms and structural samples. The default allowance is twelve texts and 240,000 inspected primary characters; hard ceilings are forty texts and 480,000 characters. Every reading records the precise half-open character ranges and rendition hash. The remaining character allowance is divided across the remaining intended reading slots so large books cannot consume the whole budget first. New canonical citation leads from readings take the next available reading slot under the same cap. Missing/external works become retained follow-up leads.
4. `author_investigation_memo` receives primary excerpts, reusable readings, validated evidence and coverage. It writes a qualified answer to the question, including contrary evidence, historical versus contemporary contexts and unresolved cases. Evidence ids are namespaced by source (`em:UID/E1.F1`) for memo citations.

The durable blob `investigation:<job_id>` is saved before/after each call and after deterministic discovery/coverage operations. It contains all completed call outputs, plan, search matches, citation paths, decisions, readings, evidence, inspected ranges, cost and memo. Supplied prior-reading job/phase IDs resolve to actual saved rows; the enriched context is frozen in `investigation-context:<job_id>` before spending. Every secondary body is searched with the expanded queries, and relevant windows are selected under an explicit allowance; the complete secondary catalog and search/inspection manifest remain available. The job's numeric analysis phases mirror engine output for existing ledger readers. Resume reuses completed calls; it refuses a changed frozen packet. Like any provider call, a process killed after receiving a response but before committing its checkpoint cannot guarantee exactly-once billing.

Each phase enters the existing readings index under the author and anchored text. Thus the memo and granular research are available independently, including after a later phase fails. Cost is reconstructed from checkpointed calls, avoiding duplicate receipt totals on resume. The caller must persist the packet and can retain/download the result before any separate Zotero filing action.

## Evidential limits

Search counts report the entire supplied body; retained windows and model readings are separately bounded. A zero hit is never a negative claim about unread text. Missing, excluded, undated, deferred and partially inspected works remain explicit. `absence_claims_supported` is false for this retrieval workflow.

Profiles, secondary analyses, conversations and Referee descriptions guide discovery. Primary quote rows are rechecked against the original body and actually inspected ranges; invented quotes remain conjectures. Memo citation IDs must resolve to retained verified evidence: unknown, unverified or missing support IDs leave a draft with a validation failure, preserving all research. Original authorship, speaker, edition dates and discussed historical period are explicit method obligations. A reprint date does not create a new intervention.

Referee access is supplied read-only context. This executor does not harvest, purchase, fetch external PDFs or mutate thinker records. A future workflow can add registered actions under a separately bounded intent. All upper-level questions and interpretive obligations live in method records, not Stacks prompt strings.

## Validation and release

`python -m pytest -q tests/test_author_investigation_2026_09_08.py tests/test_oeuvre_position_2026_09_07.py tests/test_cohort_export_2026_09_06.py` exercises packet identity, full inventory triage, lexical misses, citation follow-ups, quote checks, windows, caps, cancellation, interruption/resume, partial HTTP artifacts, real dossier dispatch/accounting and reading indexes with injected engines. A mechanical run over the real 21 MB Riley packet (115 primary inventory rows, 227 secondary sources) retained all supplied bodies, searched 11.16 million secondary/context characters, triaged every profile and allocated twelve readings under the 240,000-character limit. With injected engines it needed 31 calls; the largest supplied request was 417,633 characters against the 650,000-character ceiling. No paid call is needed for these mechanical checks. Model quality on the real Riley material still needs a source-read pilot; passing mocked orchestration does not establish the quality of an unrun memo.

Render workspace `caii`, service `the-analyst`, git `yauhenio2025/the-analyst` master, auto deploy on push; `/health` exposes the deployed commit. Coordinate a release with Stacks after checking running jobs; the parent authorized rollout after integration checks, coordinated with the Stacks release.
