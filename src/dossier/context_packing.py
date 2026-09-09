"""Deterministic final-stage packing; every supplied research text stays intact."""
from __future__ import annotations

import copy
import hashlib
import json

from src.sources.schemas import SourceSpec

POLICY = "field_final_context_v1"
TRIGGER_CHARS = 520000


def _json(value):
    return json.dumps(value, ensure_ascii=False)


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def input_chars(sources, upstream):
    # Match the light-call context serializer; formatting spaces are not data.
    return sum(len(s.text or "") for s in sources) + len(json.dumps(upstream, ensure_ascii=False, separators=(',', ':')))


def input_hash(sources, upstream):
    return _sha(_json({"sources": [s.model_dump() for s in sources], "upstream": upstream}))


def pack_final_context(stage, sources, upstream, *, packet_sha256):
    """Return new inputs plus a durable manifest, leaving caller objects intact.

    Only acquisition/coverage metadata is omitted from the model input. Its full
    value and hash are retained in the returned manifest, which the caller saves
    with the phase before spending. Texts, quotes, findings, drafts, and support
    IDs are never shortened. The remaining size guard remains authoritative.
    """
    original_chars = input_chars(sources, upstream)
    if stage.split(":", 1)[0] not in ("adjudication", "memo") or original_chars <= TRIGGER_CHARS:
        return sources, upstream, None
    packed_sources = copy.deepcopy(sources)
    packed = copy.deepcopy(upstream)
    omissions, preserved_texts = [], []

    def omit(path, value, retained_in):
        omissions.append({"path": path, "value": copy.deepcopy(value), "sha256": _sha(_json(value)),
                          "chars": len(_json(value)), "also_retained_in": retained_in})

    # One exact copy of the entire argument map remains an anchor source.
    maps = [s for s in packed_sources if s.key == "field-argument-map"]
    if len(maps) == 1 and isinstance(packed.get("field_map"), str) and maps[0].text == packed["field_map"]:
        value = packed.pop("field_map")
        packed["field_map_source"] = "field-argument-map"
        preserved_texts.append({"original_path": "field_map", "source_key": "field-argument-map", "sha256": _sha(value), "chars": len(value)})

    # Full seed/fetch details are acquisition records. Keep collection identity,
    # focus, status and counts; retain every omitted record in the manifest.
    collections = packed.get("field_collections")
    if isinstance(collections, list):
        for i, collection in enumerate(collections):
            if not isinstance(collection, dict):
                continue
            for key in ("seeds",):
                if isinstance(collection.get(key), list):
                    values = collection.pop(key)
                    omit(f"field_collections[{i}].{key}", values, f"packet.field_collections[{i}].{key}")
                    collection["seed_record_count"] = len(values)
            status = collection.get("pdf_status")
            if isinstance(status, dict) and isinstance(status.get("seeds"), list):
                values = status.pop("seeds")
                omit(f"field_collections[{i}].pdf_status.seeds", values, f"packet.field_collections[{i}].pdf_status.seeds")
                status["seed_status_record_count"] = len(values)

    # Every prior text (including the entire supplied baseline memo/review) stays
    # byte-for-byte identical. This removes repeated search bookkeeping only.
    priors = packed.get("prior_context")
    if isinstance(priors, list):
        keep = {"key", "kind", "title", "inspected_ranges", "truncated", "text"}
        for i, prior in enumerate(priors):
            if not isinstance(prior, dict):
                continue
            if isinstance(prior.get("text"), str):
                text = prior["text"]
                proof = {"original_path": f"prior_context[{i}].text", "sha256": _sha(text), "chars": len(text)}
                if len(text) >= 8000:
                    # Large JSON-embedded baseline memos need not be escaped a
                    # second time. PLAN preserves their non-anchor context role.
                    key = f"prior-context-text:{i}:{_sha(text)[:12]}"
                    if any(source.key == key for source in packed_sources):
                        raise ValueError("prior context source key collision")
                    packed_sources.append(SourceSpec(kind="paste", role="plan", key=key,
                                                     title=prior.get("title") or key, text=text))
                    prior["text"] = {"context_source_key": key, "sha256": _sha(text), "chars": len(text)}
                    proof["context_source_key"] = key
                preserved_texts.append(proof)
            removed = {k: prior.pop(k) for k in list(prior) if k not in keep}
            if removed:
                omit(f"prior_context[{i}].metadata", removed, f"state.context_manifest[{i}]")
        fields = ["key", "kind", "title", "inspected_ranges", "truncated", "text"]
        if len(priors) >= 32 and all(isinstance(p, dict) and set(p) == set(fields) for p in priors):
            packed["prior_context"] = {"fields": fields, "rows": [[p[k] for k in fields] for p in priors]}
        packed["prior_context_representation"] = (
            "All supplied prior texts and titles are unchanged. If tabular, rows follow the named fields in order. "
            "Large text references resolve to labeled PLAN context sources, never new anchor sources. "
            "Inspected ranges/truncation flags remain. Complete omitted metadata is in this call's durable manifest; "
            "prior excerpts do not establish new source inspection.")

    for src in packed_sources:
        if src.key != "primary-readings":
            continue
        readings = json.loads(src.text)
        if not isinstance(readings, list):
            raise ValueError("primary reading context must remain an array")
        for i, reading in enumerate(readings):
            if not isinstance(reading, dict):
                raise ValueError("primary reading context must contain objects")
            metadata = reading.get("source_metadata")
            if isinstance(metadata, dict):
                keep = {"uid", "source_key", "source_role", "title", "year", "date_scope", "body_sha256", "body_chars", "read_uid"}
                removed = {k: metadata.pop(k) for k in list(metadata) if k not in keep}
                if removed:
                    omit(f"primary-readings[{i}].source_metadata", removed, f"state.readings[uid={reading.get('uid')}].source_metadata")
            if isinstance(reading.get("reading"), str):
                preserved_texts.append({"original_path": f"primary-readings[{i}].reading", "sha256": _sha(reading["reading"]), "chars": len(reading["reading"])})
        src.text = _json(readings)

    # Evidence and adjudication/repair drafts retain their exact complete values.
    for key in ("evidence", "adjudication", "previous_draft", "validation_errors"):
        if packed.get(key) != upstream.get(key):
            raise ValueError("final-context packing changed research support")
    manifest = {"policy": POLICY, "stage": stage, "packet_sha256": packet_sha256,
                "original_chars": original_chars, "packed_chars": input_chars(packed_sources, packed),
                "original_input_sha256": input_hash(sources, upstream), "packed_input_sha256": input_hash(packed_sources, packed),
                "preserved_texts": preserved_texts, "omitted_metadata": omissions,
                "evidence_sha256": _sha(_json(upstream.get("evidence"))),
                "all_evidence_quotes_and_findings_retained": True,
                "all_prior_texts_retained": True, "all_primary_reading_texts_retained": True,
                "all_adjudication_and_repair_texts_retained": True}
    if manifest["packed_chars"] >= original_chars:
        return sources, upstream, None
    return packed_sources, packed, manifest
