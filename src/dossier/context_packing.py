"""Deterministic final-stage packing; every supplied research text stays intact."""
from __future__ import annotations

import copy
import hashlib
import json

from src.sources.schemas import SourceSpec

POLICY = "field_final_context_v2"
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


def expand_evidence_rows(value):
    if not isinstance(value, dict) or value.get('format') != 'grouped_evidence_v1':
        return value
    rows = [None] * value['count']
    for group in value['groups']:
        for index, values in zip(group['indices'], group['rows']):
            row = {**group['defaults'], **dict(zip(group['columns'], values))}
            if group['field_defaults']:
                row['fields'] = {**group['field_defaults'], **row['fields']}
            rows[index] = row
    return rows


def _group_evidence(rows):
    if not isinstance(rows, list) or len(rows) < 20 or not all(isinstance(r, dict) for r in rows):
        return rows
    groups = {}
    for index, row in enumerate(rows):
        groups.setdefault((row.get('uid'), tuple(sorted(row))), []).append((index, row))
    encoded = []
    for items in groups.values():
        records = [r for _, r in items]
        defaults = {k: records[0][k] for k in sorted(records[0]) if k != 'fields' and all(r[k] == records[0][k] for r in records)}
        field_defaults = {}
        if all(isinstance(r.get('fields'), dict) for r in records):
            for k in sorted(set.intersection(*(set(r['fields']) for r in records))):
                if all(r['fields'][k] == records[0]['fields'][k] for r in records):
                    field_defaults[k] = records[0]['fields'][k]
        columns = [k for k in sorted(records[0]) if k not in defaults]
        values = []
        for row in records:
            values.append([{k: v for k, v in row[c].items() if k not in field_defaults}
                           if c == 'fields' and field_defaults else row[c] for c in columns])
        encoded.append({'defaults': defaults, 'field_defaults': field_defaults, 'columns': columns,
                        'indices': [i for i, _ in items], 'rows': values})
    result = {'format': 'grouped_evidence_v1', 'count': len(rows), 'groups': encoded,
              'decoding': 'Each row follows its group columns and overlays group defaults. For fields, overlay the row fields on field_defaults. Indices preserve the original order. Every citation ID, quotation, finding, attribution, value and missing field is unchanged.'}
    if expand_evidence_rows(result) != rows:
        raise ValueError('evidence grouping changed a source record')
    return result if len(_json(result)) < len(_json(rows)) else rows


def _factor_prior_text(text):
    """Share exact repeated memo strings inside our JSON baseline context."""
    if not text.startswith('[SOURCE CHARACTERS '):
        return text
    header, _, body = text.partition('\n')
    try:
        records = json.loads(body)
    except (ValueError, TypeError):
        return text
    counts, texts = {}, {}
    collision = False
    def scan(value):
        nonlocal collision
        if isinstance(value, str) and len(value) >= 8000:
            ident = _sha(value); counts[ident] = counts.get(ident, 0) + 1; texts[ident] = value
        elif isinstance(value, dict):
            collision |= 'retained_text_ref' in value
            for v in value.values(): scan(v)
        elif isinstance(value, list):
            for v in value: scan(v)
    scan(records)
    shared = {k: texts[k] for k, n in counts.items() if n > 1}
    if not shared or collision:
        return text
    def encode(value):
        if isinstance(value, str) and len(value) >= 8000 and _sha(value) in shared:
            return {'retained_text_ref': _sha(value)}
        if isinstance(value, dict): return {k: encode(v) for k, v in value.items()}
        if isinstance(value, list): return [encode(v) for v in value]
        return value
    encoded = encode(records)
    def decode(value):
        if isinstance(value, dict):
            if set(value) == {'retained_text_ref'}: return shared[value['retained_text_ref']]
            return {k: decode(v) for k, v in value.items()}
        if isinstance(value, list): return [decode(v) for v in value]
        return value
    if decode(encoded) != records:
        raise ValueError('prior text factoring changed retained research')
    packed = header + '\n' + _json({'format': 'shared_prior_text_v1', 'records': encoded, 'texts': shared,
        'decoding': 'Replace each retained_text_ref with the complete unchanged string in texts. Every original JSON value remains. The header ranges refer to the original prior context, retained in the packing receipt. This is retained analysis, not a new quotation source.'})
    return packed if len(packed) < len(text) else text


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
            plan = (collection.get('institutional_context') or {}).get('plan')
            if isinstance(plan, dict) and isinstance(plan.get('registry_records'), list):
                records = plan.pop('registry_records')
                omit(f'field_collections[{i}].institutional_context.plan.registry_records', records,
                     'frozen collection registry; candidate names and all search outcomes remain in coverage')
                plan['registry_record_count'] = len(records)
            discovery = collection.get('discovery_context')
            if isinstance(discovery, dict):
                for key in ('identity_method_snapshot', 'method_snapshot', 'report'):
                    if key in discovery:
                        value = discovery.pop(key)
                        omit(f'field_collections[{i}].discovery_context.{key}', value, 'frozen discovery receipt')
                        discovery[key + '_sha256'] = _sha(_json(value))

    # Registry profiles removed above can leave shared acquisition records with
    # no input references. Keep classification decisions, exact proof quotes and
    # original URLs, but archive their complete repeated page bodies in receipts.
    registry = packed.get('institutional_metadata_records')
    if isinstance(registry, dict):
        references = set()
        def refs(value):
            if isinstance(value, dict):
                if 'institutional_metadata_ref' in value:
                    references.add(value['institutional_metadata_ref'])
                for v in value.values():
                    refs(v)
            elif isinstance(value, list):
                for v in value:
                    refs(v)
        refs({k: v for k, v in packed.items() if k != 'institutional_metadata_records'})
        for source in packed_sources:
            for ident in registry:
                if ident in (source.text or ''):
                    references.add(ident)
        summaries = []
        for ident in list(registry):
            if ident in references:
                continue
            record = registry.pop(ident)
            omit('institutional_metadata_records.' + ident, record, 'frozen institutional registry record')
            summary = copy.deepcopy(record)
            identity = summary.get('identity_evidence') or {}
            for original in [identity.get('original'), *(identity.get('originals') or [])]:
                if isinstance(original, dict) and 'text' in original:
                    original['text_sha256'] = _sha(original.pop('text'))
            summary['full_registry_record_sha256'] = ident
            summaries.append(summary)
        if summaries:
            packed['institution_classification_receipts'] = summaries
        if not registry:
            packed.pop('institutional_metadata_records')
            packed.pop('institutional_metadata_format', None)

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
        if src.key.startswith('prior-context-text:') and src.role == 'plan':
            factored = _factor_prior_text(src.text)
            if factored != src.text:
                omit('context_source.' + src.key, src.text, 'full prior context in frozen packet and this receipt')
                src.text = factored
                for proof in preserved_texts:
                    if proof.get('context_source_key') == src.key:
                        proof.update(encoding='shared_prior_text_v1', supplied_context_sha256=_sha(factored),
                                     original_context_retained_in_receipt=True)
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

    if 'evidence' in packed:
        packed['evidence'] = _group_evidence(packed['evidence'])
    route = packed.get('support_route')
    if isinstance(route, dict) and 'origins' in route:
        origins = route.pop('origins')
        omit('support_route.origins', origins, 'saved support_routes; all eligible source IDs and original evidence remain supplied')
        route['origins_receipt_sha256'] = _sha(_json(origins))
    if isinstance(route, dict) and isinstance(route.get('eligible_ids'), list):
        supplied_ids = [e.get('citation_id') for e in expand_evidence_rows(packed.get('evidence', []))
                        if e.get('source_role') == 'field']
        if set(supplied_ids) == set(route['eligible_ids']):
            ids = route.pop('eligible_ids')
            omit('support_route.eligible_ids', ids, 'citation_id of every supplied field-role evidence record')
            route['eligible_ids_reference'] = 'All field-role evidence records supplied in evidence; no source IDs omitted.'
    coverage = packed.get('coverage')
    if isinstance(coverage, dict):
        for key in ('missing_uids', 'excluded_uids', 'unread_uids'):
            if (key in coverage and isinstance(coverage.get('field'), dict) and isinstance(coverage.get('primary'), dict)
                    and coverage[key] == coverage['field'].get(key, []) + coverage['primary'].get(key, [])):
                omit('coverage.' + key, coverage.pop(key), 'same lists in coverage.field and coverage.primary')
                coverage[key + '_reference'] = 'Concatenate the same-named field and primary coverage lists.'
    if expand_evidence_rows(packed.get('evidence')) != upstream.get('evidence'):
        raise ValueError('final-context packing changed evidence')
    # Adjudication and repair drafts retain their exact complete values.
    for key in ("adjudication", "previous_draft", "validation_errors"):
        if packed.get(key) != upstream.get(key):
            raise ValueError("final-context packing changed research support")
    manifest = {"policy": POLICY, "stage": stage, "packet_sha256": packet_sha256,
                "original_chars": original_chars, "packed_chars": input_chars(packed_sources, packed),
                "original_input_sha256": input_hash(sources, upstream), "packed_input_sha256": input_hash(packed_sources, packed),
                "preserved_texts": preserved_texts, "omitted_metadata": omissions,
                "evidence_sha256": _sha(_json(upstream.get("evidence"))),
                "evidence_record_encoding": 'grouped_evidence_v1' if isinstance(packed.get('evidence'), dict) and packed['evidence'].get('format') == 'grouped_evidence_v1' else 'original',
                "all_evidence_quotes_and_findings_retained": True,
                "all_prior_texts_retained": True, "all_primary_reading_texts_retained": True,
                "all_adjudication_and_repair_texts_retained": True}
    if manifest["packed_chars"] >= original_chars:
        return sources, upstream, None
    return packed_sources, packed, manifest
