"""Keep Reporter originals and attribution while deduplicating acquisition records."""
from __future__ import annotations

import copy
import json
from collections import Counter

from src.dossier.context_packing import _json, _sha, input_chars, input_hash


def pack_reporter_context(stage, sources, upstream, *, packet_sha256):
    if not any(c.get("kind") == "reporter" for c in upstream.get("field_collections", []) if isinstance(c, dict)):
        return sources, upstream, None
    packed_sources, packed = copy.deepcopy(sources), copy.deepcopy(upstream)
    omissions = []

    def omit(path, value, retained_in):
        omissions.append({"path": path, "value": value, "sha256": _sha(_json(value)),
                          "also_retained_in": retained_in})

    def metadata(row, path):
        if not isinstance(row, dict):
            return
        native = row.get("source_metadata")
        if not isinstance(native, dict) or native.get("provider") != "reporter":
            return
        spans = native.get("spans")
        if isinstance(spans, list):
            if row.get("passage_spans") == spans:
                omit(path + ".passage_spans", row.pop("passage_spans"), "frozen source passage_spans")
            omit(path + ".source_metadata.spans", native.pop("spans"), "frozen source_metadata.spans")
            # The original source body is supplied separately. Keep exact native
            # offsets/times and every attribution field; repeated cue text, raw
            # caption text and per-cue retrieval URLs remain in the receipt.
            fields = ["char_start", "char_end", "start_seconds", "end_seconds", "page",
                      "speaker", "speaker_role", "role", "epistemic_role"]
            native["native_passages"] = {"fields": fields, "rows": [[s.get(k) for k in fields] for s in spans]}
            native["native_passage_note"] = (
                "Rows follow the named fields; character offsets refer to the frozen original body. "
                "Null speakers and times are unknown. Exact cue text and source URLs remain in the frozen record.")
        provenance = native.get("provenance")
        if isinstance(provenance, dict):
            pages = provenance.get("page_spans")
            if isinstance(pages, list):
                # PDF extraction repeats the entire original in this receipt.
                # Keep native page offsets; the reading source supplies its text.
                omit(path + ".source_metadata.provenance.page_spans", pages,
                     "frozen source_metadata.provenance.page_spans")
                provenance["page_spans"] = [
                    {k: v for k, v in page.items() if k not in ("text", "raw_text")}
                    for page in pages]
            for key in ("segments", "transcript_spans"):
                if key in provenance:
                    omit(path + ".source_metadata.provenance." + key, provenance.pop(key),
                         "frozen source_metadata.provenance." + key)
            # A publisher transcript's raw JSON (every word with its timing) or any other bulky acquisition record is a
            # receipt, not reading material: the body carries the text. (Odd Lots, 2026-09-10: 853,000 characters of
            # original_text beside a 42,000-character transcript pushed one reading past the input guard.)
            for key, value in list(provenance.items()):
                if key in ("original_text", "original_json", "raw", "words", "captions") or len(_json(value)) > 20000:
                    omit(path + ".source_metadata.provenance." + key, provenance.pop(key),
                         "frozen source_metadata.provenance." + key)
                    provenance[key + "_omitted"] = {"chars": len(_json(value)), "note": "retained in the frozen record and the call manifest"}

    metadata(packed.get("source_metadata"), "source_metadata")
    if input_chars(sources, upstream) > 520000:
        # Research over an already frozen collection needs its coverage and
        # identity decisions, not every directory profile used to shortlist it. These are
        # selection context, never publication evidence or analytical findings.
        for i, collection in enumerate(packed.get("field_collections", [])):
            records = ((collection.get("institutional_context") or {}).get("plan") or {}).get("registry_records", [])
            for j, record in enumerate(records):
                removed = {k: record.pop(k) for k in ("description", "topics", "business_model") if k in record}
                if removed:
                    omit(f"field_collections[{i}].institutional_context.plan.registry_records[{j}].directory_profile",
                         removed, "frozen collection institutional_context.plan.registry_records")
            if records:
                collection["directory_profile_note"] = (
                    "Directory descriptions, topics and business-model labels are retained in the frozen collection "
                    "and this call's packing receipt. Candidate identities, classification evidence, selection and "
                    "search outcomes remain supplied. Directory profiles are not institutional positions.")
    for source in packed_sources:
        if source.key == "investigation-question":
            question = json.loads(source.text)
            for key in ("field_collections", "field_gaps"):
                if key in question and question[key] == upstream.get(key):
                    omit("investigation-question." + key, question.pop(key), "current call packet." + key)
            source.text = _json(question)
        elif source.key == "field-readings":
            rows = json.loads(source.text)
            for i, item in enumerate(rows):
                metadata(item.get("reading", {}).get("source_metadata"), f"field-readings[{i}].reading.source_metadata")
            source.text = _json(rows)

    coverage = packed.get("coverage")
    if (isinstance(coverage, dict) and "field_gaps" in coverage
            and coverage["field_gaps"] == packed.get("field_gaps")):
        # Final research supplies the same complete gap list both directly and
        # inside coverage. Keep the direct copy, with an explicit reference.
        omit("coverage.field_gaps", coverage.pop("field_gaps"), "current call packet.field_gaps")
        coverage["field_gaps_reference"] = "The complete field_gaps list in this call's packet"

    # Organizational originals recur in every source's frozen admission receipt
    # and the collection's registry history. Supply each exact record once, with
    # resolvable references; retain every word and the unmodified input in receipts.
    registry = {}
    def shared(value, path, key=''):
        if isinstance(value, dict):
            if key in ('registry_record', 'original') and len(_json(value)) > 1000:
                ident = _sha(_json(value))
                omit(path, value, 'current call packet.institutional_metadata_records.' + ident)
                if ident not in registry:
                    registry[ident] = copy.deepcopy(value)
                return {'institutional_metadata_ref': ident}
            return {k: shared(v, path + '.' + k, k) for k,v in value.items()}
        if isinstance(value, list):
            return [shared(v, f'{path}[{i}]', 'registry_record' if key == 'registry_records' else key) for i,v in enumerate(value)]
        return value
    packed = shared(packed, 'packet')
    for source in packed_sources:
        if source.key == 'field-readings':
            rows = json.loads(source.text)
            for i, row in enumerate(rows):
                reading = row.get('reading') or {}
                if isinstance(reading.get('source_metadata'), dict):
                    reading['source_metadata'] = shared(reading['source_metadata'], f'field-readings[{i}].reading.source_metadata')
            source.text = _json(rows)
    if registry:
        packed['institutional_metadata_records'] = registry
        packed['institutional_metadata_format'] = 'institutional_metadata_ref resolves to the complete unchanged original record in institutional_metadata_records.'

    # Hundreds of unsearched candidates repeat identical coverage fields. Share
    # those exact values; retain every candidate, count, outcome and exception.
    # This changes representation only, after the initial planning call.
    if stage != 'plan':
        for i, collection in enumerate(packed.get('field_collections', [])):
            context = collection.get('institutional_context') or {}
            rows = context.get('coverage')
            if not isinstance(rows, list) or len(rows) < 20 or not all(isinstance(r, dict) for r in rows):
                continue
            keys = set.intersection(*(set(r) for r in rows))
            defaults = {}
            for key in sorted(keys):
                encoded, count = Counter(_json(r[key]) for r in rows).most_common(1)[0]
                if count > len(rows) // 2:
                    defaults[key] = json.loads(encoded)
            compact = {'defaults': defaults, 'rows': [
                {k: v for k, v in row.items() if k not in defaults or _json(v) != _json(defaults[k])}
                for row in rows]}
            if len(_json(compact)) < len(_json(rows)):
                omit(f'field_collections[{i}].institutional_context.coverage', rows,
                     'frozen collection coverage; current input reconstructs each row as defaults overlaid by row fields')
                context['coverage'] = compact
                context['coverage_format'] = 'For each coverage record, overlay the row fields on defaults. All original records, values and exceptions are retained; an omitted row field inherits its default.'

    if not omissions:
        return sources, upstream, None
    manifest = {"policy": "reporter_acquisition_context_v1", "stage": stage, "packet_sha256": packet_sha256,
                "original_chars": input_chars(sources, upstream), "packed_chars": input_chars(packed_sources, packed),
                "original_input_sha256": input_hash(sources, upstream), "packed_input_sha256": input_hash(packed_sources, packed),
                "omitted_metadata": omissions, "original_source_bodies_unchanged": True,
                "all_readings_quotes_and_findings_retained": True}
    return packed_sources, packed, manifest
