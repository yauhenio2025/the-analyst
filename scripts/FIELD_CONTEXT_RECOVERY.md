# Recovering a final-context input-limit stop

This package changes no deployed application file. Stage these three files in an
isolated admin directory on the current service instance:

- `src/dossier/context_packing.py`
- `src/dossier/field_investigation.py`
- `scripts/resume_field_with_context_packing.py`

Keep the first two files together in a `modules` subdirectory. Run the script
from the deployed repository working directory with `PYTHONPATH=.`. It loads only
these two patched modules into the standalone process, then uses the normal
synchronous dossier runner worker. That worker owns document loading, cached
checkpoint reuse, real calls, receipt derivation, status changes, indexing, and
finalization. The admin process stays alive until the worker returns.

First wait for the original job to report `failed`, step `analysis`, with an idle
checkpoint paused for `input_limit` at an unpaid `adjudication` or `memo` stage.
Do not interrupt an in-flight call. Disable competing monitor/API resumes and
avoid a service restart for the duration; the legacy app runner does not honor
this utility's advisory lock. The explicit coordination flag records this
operational prerequisite.

```bash
PYTHONPATH=. python /tmp/field-context-release/resume_field_with_context_packing.py dossier-db7217a78054 --module-dir /tmp/field-context-release/modules > /tmp/field-context-release/preflight.json
PYTHONPATH=. python /tmp/field-context-release/resume_field_with_context_packing.py dossier-db7217a78054 --module-dir /tmp/field-context-release/modules --apply --preflight /tmp/field-context-release/preflight.json --competing-resumes-disabled > /tmp/field-context-release/result.json
```

Dry-run does not mutate the database or launch a model call. It pins the exact
checkpoint, frozen packet, all cached calls, all read-input windows, canonical
phase outputs, receipts/totals, and both module/script hashes. Apply rechecks the
same receipt under a process lock, atomically archives the exact original checkpoint
(including its failed input manifest), records an immutable launch receipt linking
that archive by key/hash/byte length, and sets
the same status the normal resume API sets. PostgreSQL uses a session advisory
lock, explicitly released before its connection returns to the pool. SQLite
uses a local file lock. A previous launch for the identical checkpoint is refused
until its outcome has been inspected; the utility never blindly retries a call.

The packing policy runs only on new final-stage calls over 520k characters:

- One exact global-map copy remains in its existing named source.
- Seed/fetch acquisition records move to the durable call manifest, with full
  values, hashes, and frozen-packet references; collection focus/status/counts stay.
- Every supplied prior text and title stays. Repeated metadata moves to the full
  durable manifest; inspected windows/truncation flags remain. Large prior memos
  become labeled PLAN context sources, and sufficiently large entry lists use an
  explicit field-order table. These are not new anchor sources.
- Primary reading prose remains exact; extra source metadata moves to the same
  durable manifest while frozen identity/date/span provenance stays in context.

Full field and primary quotations/findings remain protected at final stages.
The existing field-reference fallback is restricted to earlier field-map stages.
Adjudication, repair drafts, validation errors, and prior text are never truncated.
If the request still cannot fit, the guard stops before spending again.

Every packed call has original/final input hashes, exact character counts,
retained text hashes, complete omitted metadata, and the final evidence
representation in `call_input_manifests`. After the normal runner returns, the
utility verifies the cached call and phase prefixes, source packet, original
read-input windows, and accounting, and stores an immutable result receipt next
to the launch receipt. A failure remains visible and exits nonzero.
