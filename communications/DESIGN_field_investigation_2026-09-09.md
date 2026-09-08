# Develop a position through a thinker and a research field

The reusable question is bilateral: what does a thinker's account clarify about a topical research field, and what do the field's competing arguments, mechanisms, cases and evidence require the researcher to revise? The motivating Riley/tech-worker case is an instance. The method works independently or as a sourced follow-up to a prior author investigation.

## Request contract

Create an engines-only dossier with `entry: chosen`, `path.chain_key: field_investigation`, exactly one paste source with `role: field_investigation`, and `output: {text:false,tables:false,figures:0,plates:0}`. Its text is a JSON packet:

```json
{
  "kind": "field_investigation",
  "author": {"id": "thinker-id", "name": "Thinker name"},
  "question": "What should the researcher now conclude about this bilateral question?",
  "scope": {"context": "Research scope and historical distinctions"},
  "primary": [{"uid":"em:SOURCE01","title":"Author work","body":"Source text","profile":{}}],
  "field": [{"uid":"referee:67","title":"Field paper","authors":["Field author"],"body":"Field text","referee_paper_id":67,"pdf_url":"https://example.org/paper.pdf","page_spans":[{"page":1,"start":0,"end":10}]}],
  "prior_investigations": [],
  "prior_readings": [],
  "limits": {"max_field_texts":80,"max_field_chars":3000000,"max_primary_texts":12,"max_primary_chars":240000}
}
```

The displayed page span is illustrative; real half-open offsets must match the exact supplied body. UIDs are globally unique across primary, field and optional secondary inventories. Missing or excluded entries remain metadata rows. Exclude unverified PDF identities with `body_state: excluded` and an explicit reason. Bodies, rendition hashes, source URLs, external reference IDs, authors, editions, dates, original-date uncertainty, Referee metadata and exact page spans survive freezing. The adapter never fetches replacements or treats a book container as proof of chapter authorship.

`primary` is the complete author inventory, not a bridge-selected shortlist. `field` is the selected topical bundle: every eligible supplied field body receives an actual reading. Missing field bodies are explicit gaps. Optional prior investigations hold the actual memo, source identities and any separately labeled reviewed source passages. A singular `parent_investigation` object is retained and normalized to the front of this baseline list, preserving the reviewed memo and older interpretive lineage. Prior job/phase pointers resolve through the existing reading registry before the context packet is frozen. The prior baseline receives its own 200,000-character allowance; embedded prior answer/search artifacts become an explicit lineage/coverage manifest while the actual memo and source reviews retain priority; other prior context receives 40,000 characters. Any context windowing is disclosed and the full supplied context remains stored. No prior investigation means standalone mode; the method must not invent an earlier position.

## Method and execution

Seven executable capability/operationalization records, a workflow and a dossier recipe hold the reasoning:

1. `field_investigation_plan` formulates bilateral questions, rival mechanisms, discriminating tests and literal reading queries.
2. `field_investigation_field_read` reads each available field text in its own terms: argument, mechanism, evidence, method, cases, scale, contrary findings and qualifications. Each field author retains an independent position.
3. `field_investigation_field_map` identifies disagreements and compatible claims across those readings. Field reading/evidence bundles above 200,000 characters are mapped separately and then reconciled globally. Complete per-source readings and all batch maps remain persisted; final synthesis consumes the explicitly identified argument maps. Downstream evidence selects their original cited support IDs. If repeated field quotations would push a request past 520,000 characters, a disclosed reference index preserves every selected field evidence ID and verified role beside the complete argument maps; primary quotations remain in the attribution context. Per-call manifests retain representation, all supplied IDs and input size. Requests above 640,000 characters after packing stop before another paid call.
4. `field_investigation_author_select` receives every full author profile, compact canonical citation metadata and search leads in batches of at most 20 rows/180,000 characters, guided by the field map and prior context. A global reconciliation orders the author core under the reading cap. Missing model decisions remain marked unjudged; missing/excluded sources stay visible. Selection comes from semantic method decisions, not title or UID order.
5. `field_investigation_author_read` recovers the thinker's actual sourced position against those questions, distinguishing primary attribution from this inquiry's extension.
6. `field_investigation_adjudicate` judges actual tensions, scope/scale mismatches, empirical versus normative claims, counterevidence, warranted revisions and unresolved tests.
7. `field_investigation_memo` writes the research memo with supported answers and explicit changed, retained, new and unresolved positions. The baseline is the supplied prior memo or explicitly standalone. Revising the researcher's account is not a historical change in the thinker.

All eligible field texts are read, up to 80. Field allowance defaults to 3M inspected characters, hard ceiling 8M; any one text receives at most 100,000 characters. The author core defaults to 12 texts/240,000 characters, configurable up to 40/960,000. Short texts are read whole when they fit; oversized texts receive disjoint exact contextual windows. Allocation plans prefer reading works of at most 100,000 characters whole when the cap permits, reserving actual reading room for every longer selected work. Remaining allowance is shared among those longer texts; tighter budgets use a bounded fair allocation. The complete allocation plan and exact reading ranges are frozen for resume. Coverage separately records field and primary inventory, full/window reads, inspected characters and missing/excluded/unread IDs. Whole-body lexical searches are distinct from model reading; no absence claim across unread material is supported.

## Safeguards and memory

The custom executor shares the existing author investigation's durable job shell: compressed blobs, prior hydration, phase indexing, accounting, cancellation/drain checks and resume. Every provider output is checkpointed before the next call, with numeric analysis phases and exact frozen read inputs. Resume reuses completed calls and rejects changed packets or source renditions. Costs derive from completed checkpoints. A process killed after a provider response but before checkpoint persistence still has the existing unavoidable exactly-once billing boundary.

Large source documents also require compression before SQL adaptation. A live 30.21MB frozen plan caused the 256MB PostgreSQL backend to be killed during its initial `executor_documents` insert, before an investigation job existed. Document storage now uses explicit `text_encoding`: small compressed values use the lossless JSON gzip codec in base64 TEXT; larger values become content-addressed blob references in the same transaction. Dossier JSON columns likewise replace values above 512KiB, including the complete frozen source request and growing analysis, with checksum-verified references. Encoded blobs above 512KiB use a small explicit manifest and ordered chunks of at most 512KiB, with atomic replacement and one-snapshot reads. Length, count and encoded/decoded checksums detect damaged or missing chunks. Reading-index and immutable-inquiry writers use the same transaction-aware blob primitive. Source hashes and character counts always describe the original text. Document getters, registered-corpus reads and hash backfills decode transparently and validate compressed source identity. Existing literal and gzip rows remain readable; corrupt or unknown encodings fail instead of returning invented or empty source content. This protects the existing database plan without discarding any frozen source or intermediate research.

The dossier routes accept ordinary JSON compressed with `Content-Encoding: gzip` and `Content-Type: application/json`. This reduces large packet upload time without changing the request schema, frozen source string or source hashes. Decompression checks the complete gzip stream before the route executes; corrupt/trailing streams return 400 and requests exceeding the default 128MiB inflated limit return 413. `DOSSIER_MAX_INFLATED_REQUEST_BYTES` configures that ceiling. Plain JSON remains supported.

Quoted evidence is verified against the original body and actually inspected ranges. Exact/whitespace-only matching records original offsets, original source quotation, SHA-256, source role and optional PDF page anchors. Invented quotations remain conjectures. External source identities such as `referee:67` now enter the text reading index alongside Zotero IDs.

Field-map, adjudication and memo claim ledgers validate source support identities. `thinker_position` requires verified primary evidence; `field_finding` requires verified field evidence; `comparison` requires both; `unresolved` cannot masquerade as established support. Memo inline citations must resolve to verified evidence and revisions must name the correct prior/standalone baseline. These checks establish identity and source-role discipline, not semantic entailment; attribution and interpretation remain method obligations. One bounded repair may reconsider a failed map, adjudication or memo against the same evidence; the original paid draft remains cached separately. Failed validation preserves the draft and every completed research artifact.

Use `GET /v1/dossier/jobs/{id}/investigation` for current or partial artifacts, including field maps, decisions, source readings, evidence, revised memo and coverage. Standard job/ledger/readings endpoints retain complete paid outputs and reusable per-text rows. No paid production run is part of mechanical validation; source preparation, live budget, deployment and report rendering are coordinated with the Stacks.

## Validation

The focused field and author suites exercise 47 field texts with 115 author profiles, full-inventory semantic selection, standalone/follow-up baselines, long contextual windows, external IDs/PDF anchors, source hash changes, fabricated quotations, provenance failures, cap/cancel behavior, interruption/resume and no repeated paid calls, large-field map batching, registry/API dispatch, durable accounting and reading indexes. Commands and release results are recorded with the delivery commit.

Delivery validation: `python -m pytest -q tests/test_field_investigation_2026_09_09.py tests/test_author_investigation_2026_09_08.py tests/test_transactional_blob_compression_2026_09_09.py tests/test_oeuvre_position_2026_09_07.py tests/test_constructive_method_records_2026_09_08.py` — 77 passed, including bounded repair with both paid drafts retained and no repeated calls on resume, reviewed-parent lineage, 1,104 retained field evidence rows under the input ceiling, and conflicting/cap-deferred author decisions.

A no-charge mechanical rehearsal on the actual 63-row Referee field packet (7.0M supplied body characters), with injected engines and a synthetic 115-row author inventory, read all 46 eligible field works. After exact page-marker conversion in memory, it retained 32 full field readings and 14 contextual readings, verified 46 injected source quotations, and disclosed 16 missing works plus one excluded duplicate. The source artifacts were not mutated. This validates mechanics, not scholarly findings.

The complete 45.2MB live commission packet also passes a no-charge rehearsal with injected engines: 115 real primary inventory rows, 63 real field rows, 231 contextual sources, all 46 eligible field works read and all author profiles triaged. Maximum request size was 573,110 characters across 80 injected calls. Its reviewed parent held 8.1MB of prior answer artifacts, a 20KB memo and 123KB of source reviews; explicit answer-manifest packing preserves the complete memo/reviews in context. Missing collection 90 is carried into plan, memo and coverage as a collection gap.

Large-packet storage release rehearsal: the exact frozen request passes the real gzip dossier creation route with the runner mocked and an isolated SQLite database. All 369 stored documents round-trip with unchanged original hashes and lengths. The frozen source column is 214 bytes; the largest document column is 418,764 bytes, blob manifest 246 bytes, and chunk 524,288 bytes. No model calls run. Focused storage, compression, source, workflow, registry and dossier suites cover 141 cases.
