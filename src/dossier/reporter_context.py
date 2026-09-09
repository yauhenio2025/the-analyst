"""Keep Reporter originals and attribution while deduplicating acquisition records."""
from __future__ import annotations

import copy
import json

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
            for key in ("segments", "transcript_spans"):
                if key in provenance:
                    omit(path + ".source_metadata.provenance." + key, provenance.pop(key),
                         "frozen source_metadata.provenance." + key)

    metadata(packed.get("source_metadata"), "source_metadata")
    for source in packed_sources:
        if source.key == "investigation-question":
            question = json.loads(source.text)
            for key in ("field_collections", "field_gaps"):
                if key in question and question[key] == packed.get(key):
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

    if not omissions:
        return sources, upstream, None
    manifest = {"policy": "reporter_acquisition_context_v1", "stage": stage, "packet_sha256": packet_sha256,
                "original_chars": input_chars(sources, upstream), "packed_chars": input_chars(packed_sources, packed),
                "original_input_sha256": input_hash(sources, upstream), "packed_input_sha256": input_hash(packed_sources, packed),
                "omitted_metadata": omissions, "original_source_bodies_unchanged": True,
                "all_readings_quotes_and_findings_retained": True}
    return packed_sources, packed, manifest
