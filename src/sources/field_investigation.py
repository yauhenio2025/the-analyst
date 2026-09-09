"""Freeze two distinct source populations for a thinker/field investigation."""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy

from src.sources.schemas import Document


def expand_field_investigation(text: str) -> list[Document]:
    packet = json.loads(text)
    if not isinstance(packet, dict) or not isinstance(packet.get("question"), str) or not packet["question"].strip():
        raise ValueError("field_investigation requires a question")
    institutional = packet.get("inquiry_type") == "institutional"
    if not institutional and (not isinstance(packet.get("author"), dict) or not packet["author"].get("id")):
        raise ValueError("field_investigation requires author.id")
    packet = deepcopy(packet)
    transport = packet.get('research_transport')
    if transport:
        if transport.get('version') != 1 or transport.get('policy') != 'exact_prior_source_metadata_factoring':
            raise ValueError('Unsupported retained-research metadata transport')
        records = packet.get('retained_research_metadata')
        if not isinstance(records, dict):
            raise ValueError('Retained research metadata records are missing')
        for ident, record in records.items():
            encoded = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
            if hashlib.sha256(encoded.encode()).hexdigest() != ident:
                raise ValueError('Retained research metadata hash mismatch')
        def validate_references(value):
            if isinstance(value, dict):
                if set(value) == {'retained_source_metadata_ref'}:
                    if value['retained_source_metadata_ref'] not in records:
                        raise ValueError('Unresolved retained research metadata reference')
                else:
                    for child in value.values():
                        validate_references(child)
            elif isinstance(value, list):
                for child in value:
                    validate_references(child)
        for key in ('parent_investigation', 'prior_research', 'prior_investigations'):
            validate_references(packet.get(key))
    if institutional:
        if packet.get("author") or packet.get("primary") or packet.get("secondary"):
            raise ValueError("institutional inquiry must be author-independent; commission a separate comparison")
        packet["author"] = None
        packet["primary"] = []
    from src.engines.methods import validate_contract
    validate_contract(packet)
    packet["kind"] = "field_investigation"
    parent = packet.get("parent_investigation")
    if parent is not None:
        if not isinstance(parent, dict):
            raise ValueError("parent_investigation must be a sourced prior investigation object")
        priors = packet.get("prior_investigations") or []
        if isinstance(priors, dict):
            priors = [priors]
        if not isinstance(priors, list):
            raise ValueError("prior_investigations must be a list or object")
        packet["prior_investigations"] = [parent] + [p for p in priors if p != parent]
    docs, seen = [], set()
    for role in ("primary", "field", "secondary"):
        rows = packet.setdefault(role, [])
        if not isinstance(rows, list) or (not rows and (role == "field" or role == "primary" and not institutional)):
            raise ValueError(f"field_investigation requires a {role} inventory list")
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError(f"each {role} entry must be an object")
            uid = str(row.get("uid") or "").strip()
            if not uid or uid in seen or any(c in uid for c in "/[] \t\r\n,;"):
                raise ValueError(f"missing, unsafe or duplicate inventory uid: {uid}")
            seen.add(uid)
            row["uid"] = uid
            body = row.pop("body", None)
            if body is None:
                body = row.pop("text", "")
            row.pop("text", None)
            if not isinstance(body, str):
                raise ValueError(f"body must be a string: {uid}")
            row.update(source_key=f"{role}:{uid}", source_role=role, body_chars=len(body),
                       body_sha256=hashlib.sha256(body.encode()).hexdigest() if body else None)
            row.setdefault("body_state", "available" if body else "missing")
            last_end = 0
            spans = row.get("page_spans", [])
            if not isinstance(spans, list):
                raise ValueError(f"page_spans must be a list: {uid}")
            for span in spans:
                if not isinstance(span, dict) or type(span.get("start")) is not int or type(span.get("end")) is not int:
                    raise ValueError(f"invalid page span: {uid}")
                if not span.get("page") or not 0 <= last_end <= span["start"] < span["end"] <= len(body):
                    raise ValueError(f"page spans must be ordered exact body ranges: {uid}")
                last_end = span["end"]
            if body:
                creators = packet["author"].get("name", "") if role == "primary" else row.get("authors", "")
                if isinstance(creators, list):
                    creators = "; ".join(str(a) for a in creators)
                docs.append(Document(key=row["source_key"], title=row.get("title") or uid, text=body,
                                     creators=str(creators), year=str(row.get("year") or ""), role="source"))
    docs.append(Document(key="investigation", title="Frozen thinker and field investigation", role="plan",
                         text=json.dumps(packet, ensure_ascii=False)))
    return docs
