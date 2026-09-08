# Importing an external reviewed investigation edition

Run on the existing database environment, after the investigation job is `done`
and its checkpoint is `complete` with no `running_stage`:

```bash
python -m scripts.import_reviewed_investigation_edition DOSSIER_JOB_ID --payload reviewed-edition.json
python -m scripts.import_reviewed_investigation_edition DOSSIER_JOB_ID --payload reviewed-edition.json --apply
```

The first command validates without writing. The second atomically stores the
edition, snapshots the original memo, and indexes a separate external review
reading. Neither command starts a model call or changes canonical research or
accounting. The schema must already exist; this utility does not run migrations.
The payload is never a command to modify source text.

## Minimal payload

Replace the example job and hashes with values from the completed investigation
and frozen source metadata. The offset example assumes the frozen body is exactly
`Engine inspected.\nSupplemental source passage.` (46 Unicode characters). Its
supplemental passage starts at character 18 and ends at 46. Use actual frozen
executor text offsets, not PDF byte offsets or offsets in a normalized quotation.
`source_quote` must equal the concatenation of all exact `quote_spans[].text`.

```json
{
  "schema_version": 1,
  "kind": "reviewed_edition",
  "job_id": "dossier-example",
  "packet_sha256": "REPLACE_WITH_FROZEN_PACKET_SHA256",
  "original_memo_sha256": "REPLACE_WITH_UTF8_ORIGINAL_MEMO_SHA256",
  "title": "Source-reviewed edition",
  "reviewed_memo": "A qualified conclusion [referee:488418/Review.SSR-R1].",
  "provenance": {
    "reviewer": "Research desk",
    "reviewed_at": "2026-09-09T10:00:00Z",
    "method": "external_source_review_v1"
  },
  "source_proofs": [
    {
      "id": "SSR-R1",
      "citation_id": "referee:488418/Review.SSR-R1",
      "uid": "referee:488418",
      "source_key": "field:referee:488418",
      "body_sha256": "REPLACE_WITH_FROZEN_UTF8_BODY_SHA256",
      "pdf_sha256": "REPLACE_WITH_FROZEN_PDF_SHA256",
      "quote_spans": [
        {"start": 18, "end": 46, "text": "Supplemental source passage."}
      ],
      "source_quote": "Supplemental source passage.",
      "review_windows": [[18, 46]],
      "finding": "A source passage that qualifies the original conclusion.",
      "qualification": "Exact text matching does not certify the interpretation.",
      "locus": "p. 2"
    }
  ],
  "findings": [
    {
      "id": "R1",
      "kind": "revision",
      "status": "changed",
      "text": "Qualify the original conclusion using the supplemental passage.",
      "support_ids": ["referee:488418/Review.SSR-R1"]
    }
  ]
}
```

For a source without a frozen PDF hash, omit `pdf_sha256` or set it to `null`.
Frozen PDFs usually record that hash under `source_metadata.pdf_sha256`.
Physical page offsets come only from the source's top-level `page_spans`.

`findings` must be a nonempty ledger. Each entry requires a unique `id`,
`kind` (`finding` or `revision`), nonempty `text`, and `support_ids` containing
canonical engine-verified citation IDs or exact supplemental proof citation IDs.
An unsupported entry must use `status: "unresolved"`. Other supplied finding
fields are retained. The `source_proofs` list may be empty when the entire review
uses existing engine-verified evidence.

Proof IDs and proof citation IDs must each be unique. An existing engine-unverified
citation ID can be resolved within this edition by an explicit exact proof using
that ID. Duplicate original variants are grouped: any engine-verified variant
with the matching source identity counts. Original evidence remains unchanged.
Explicit UID/row citations in memo and finding text are checked. Ordinary Markdown
links and notes are allowed; citation resolution does not verify semantic support.

All proof spans must be ordered, nonoverlapping, exact, and inside a single
supplied review window. Multiple fragments separated by omitted text are exposed
as `passage_form: "ordered_discontinuous_fragments"`, `continuous_quote: false`.
They are not certified as one continuous quote or as normalized PDF columns.
The optional input alias `source_spans` is normalized to `quote_spans`.

## Optional visual attestation

A frozen PDF hash alone is reported as `frozen_packet_hash_bound`; it does not
claim anyone visually inspected that PDF. To attach a visual attestation, add
this object to a proof:

```json
{
  "visual_audit": {
    "reviewed_from_pdf": true,
    "pdf_receipt": {"key": "IMMUTABLE_PDF_KEY", "sha256": "PDF_SHA256", "bytes": 12345},
    "audit_receipt": {"key": "IMMUTABLE_AUDIT_KEY", "sha256": "AUDIT_SHA256", "bytes": 456}
  }
}
```

Both blobs must already be durable and match their receipt hashes/byte lengths.
The PDF bytes must match the frozen PDF hash. The audit JSON must bind `uid`,
`body_sha256`, `pdf_sha256`, `reviewed_from_pdf: true`, a nonempty `method`, and
`pages: [{"page": 2}]`. Optional `reviewed_start`/`reviewed_end` character bounds
on each audit page restrict the approved region. Every proof page and fragment
must fit the audit. The resulting status is
`reviewer_attested_with_verified_artifact_hashes`; code checks provenance and
scope, not the accuracy of the reviewer's visual or intellectual judgment.

## Durable and public records

`GET /v1/dossier/jobs/JOB/investigation` exposes `reviewed_editions[]` alongside
the original `memo`. Each edition carries the original payload fields, enriched
`source_proofs`, `verification`, `content_hash`, `imported_at`, `artifact`,
`original_memo_artifact`, and `reading_ref`. Artifact references contain
`key`, `sha256`, and `bytes`. `content_hash` is the SHA256 of the canonical input
JSON (sorted keys, compact separators, Unicode UTF-8, normalized span alias).
The edition artifact's own hash additionally covers derived verification and
its original-memo artifact reference.

Each exposed proof reports `review_quote_verified`, unchanged
`engine_quote_verified` (`true`, `false`, or `null` if absent),
`original_engine_window_coverage`, `quote_spans`, `pages`, `page_urls`,
`passage_form`, `continuous_quote`, and separate text/PDF/visual verification.
The engine-window coverage value is `inside_one_original_window` or
`supplemental_outside_one_original_window`. A new proof never silently changes
engine verification or expands the engine's inspected windows.

`GET /v1/readings/JOB/review:CONTENT_HASH` returns the separate reading with
`engine: "reviewed_edition_import"`, `origin: "external_review"`, zero cost and
no provider calls. It contains the reviewed memo as `prose`, complete edition,
and finding/revision rows. Existing job/person/text indexes discover it, and
passing its `reading_ref` through `prior_readings` hydrates the whole record.
Canonical readings remain independently addressable.

An exact repeat is a no-op. If a shared reading index is later lost, dry-run
reports `would_relink`; `--apply` can restore only missing indexes after checking
the immutable artifacts and canonical state. Conflicting index content is
refused. Every apply reports a separate post-commit `index_verification`, since
older runtime index writers do not all use the advisory lock. A missing or
unavailable post-commit index check exits nonzero and reports that the edition
is durable; rerun `--apply` to restore missing links.
