# Constructive inquiry: the first portable worker seam

The Stacks supplies selected commitments, a live question and held case texts. The
Analyst owns `constructive_inquiry` and `constructive_retest` as ordinary capability
and operationalization records. Their framing, questions, method cards and synthesis
briefs supply both the external worker prompt and the existing engine/dossier path.
The Stacks owns accepted Brief state and executes the subscription worker. A proposed
account is explicitly a proposal; source quote matches never establish attribution
or semantic validity.

`POST /v1/inquiries/prepare` accepts the `PrepareRequest` in
`src/inquiries/schemas.py`. It freezes the normalized contract, exact source texts,
source hashes, central method records, structured result schema and composed prompts
in the existing blob store. Its deterministic preparation ID binds the full source
and context identity to a method fingerprint. The response includes `system_prompt`,
`user_prompt` (all input plus output schema), `output_schema`, `source_manifest`,
`prepared_id`, `input_fingerprint` and `method_fingerprint`. Missing method records
produce 503; there is no local reasoning fallback. No model is called by this route.

`POST /v1/inquiries/complete` accepts those three identity fields, `input` (the exact
prepare request), `result` (worker JSON) and `execution` (provider, model, local job,
charged cost, elapsed seconds and optional subscription list price). It checks the
frozen input and method identity, result shape and references, then each quote in
its named source. Quotes are normalized with the existing wall's normalizer but
are never silently trimmed or moved to a different source. Failed and short quotes
remain in the answer with `verified: false` and an `anchor_status`; every match means
quote presence only. An initial inquiry cannot claim a returned test outcome. A
retest requires a selected test copied exactly from its previous result and returns
an outcome for that test ID. The owning app binds that supplied prior result to its
authoritative inquiry history.

The immutable receipt ID is `inquiry-<preparation hash>`. Database uniqueness handles
concurrent or repeated imports: the same completed result replays, a different one
conflicts (409). Receipt durability and the reading index are acknowledged together;
retrying repairs an interrupted index write. Strict external reading imports serialize their index
updates inside one database transaction; feedback reads resolve immutable events so
concurrent snapshot refreshes cannot hide a correction. Source/context snapshots and
method fingerprints remain in central reading memory, indexed under every supplied text and
the supplied source authors. A later method edit does not invalidate an already
prepared reading: completion uses its frozen method. A caller that changes source,
context or fingerprints receives 409 and must prepare a new reading.

`GET /v1/inquiries/receipts/{receipt_id}` returns the shaped result, validation report,
execution metadata, source manifest, reading reference and author feedback.
`POST /v1/inquiries/receipts/{receipt_id}/feedback` accepts an immutable `feedback_id`,
`text`, optional `decision` and optional proposed `revision_id`. Retries deduplicate;
changed content under an existing ID conflicts. Explicit corrections and decisions
are also attached to the central reading. These are evidence for future evaluated
method improvement; no autonomous method learning or acceptance is claimed.

The existing `/v1/engines/{key}/call` surface path and dossier oneshot path can use
the same records through their normal anchored ledger format. They do not produce
this JSON receipt automatically. All declared method depths use oneshot; the older
light-call implementation nevertheless adds its critic at standard depth. The pilot
consumer uses the prepare/complete seam to retain subscription execution and central
validation and memory.

The accompanying oeuvre fix places prior-reading hints inside the serialized source
where the adapter reads them. The adapter accepts old job-ID strings and portable
`{job_id, phase}` references, resolves entries from central memory, and exposes
unavailable references. This does not make an empty lookup proof that no prior
reading exists.

Validation is deterministic with isolated SQLite and mocked execution. It covers
initial construction, returned retest, malformed/unknown references, wrong-source
and invented quotations, stale input, missing methods, frozen method revisions,
concurrent conflicting completions, index-repair retries and immutable feedback.
These deterministic checks make no model calls and use isolated test state.

The subsequent local subscription smoke completed both the initial inquiry and a returned
retest through the real central validation and receipt paths. Whitespace counts over the
returned JSON were 3,471 words initially and 7,528 in the retest, despite the synthetic
case material consisting of two one-sentence sources. The readings repeatedly restated
provenance and caveats across fields. These counts include JSON field names and other
structural text; they are not a measurement of original narrative alone. Both completions
returned 200; the source wall matched three and five quotations respectively, with no
failed anchors. Those checks establish transport and quote-presence behavior, not the
intellectual quality of the accounts.

This evidence prompted presentation tuning in the two central operationalizations'
framing and synthesis briefs. They now guide the writer toward 60-90-word summaries,
compact account/derivation/mechanism/scope fields, an outcome explanation around 150
words, and about 1,200-1,800 words of original narrative overall, with much less for
short material. These are contextual writing guides, not quotas, hard truncation or
semantic validation. Distinct evidence, contrary readings and inferential limits remain
required; general caveats belong once where they help the reader. The change is owned
by the method records and applies to new preparations through their changed method
fingerprints. The completed smoke retains its frozen earlier method.

The tuned records have not yet been evaluated in a model run. A real-case evaluation
must test whether they improve clarity while preserving source coverage, meaningful
alternatives and the inferential detail needed to assess a construction. The synthetic
smoke motivates this tuning; it does not establish that the new guidance achieves it.
