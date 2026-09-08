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
    if not isinstance(packet.get("author"), dict) or not packet["author"].get("id"):
        raise ValueError("field_investigation requires author.id")
    packet = deepcopy(packet)
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
        if not isinstance(rows, list) or (role != "secondary" and not rows):
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
