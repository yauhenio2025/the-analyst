"""Expand a frozen Stacks investigation packet without losing missing inventory entries."""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy

from src.sources.schemas import Document


def expand_author_investigation(text: str) -> list[Document]:
    packet = json.loads(text)
    if not isinstance(packet, dict) or not isinstance(packet.get("question"), str) or not packet["question"].strip():
        raise ValueError("author_investigation requires a question")
    if not isinstance(packet.get("author"), dict) or not packet["author"].get("id"):
        raise ValueError("author_investigation requires author.id")
    if not isinstance(packet.get("primary"), list) or not packet["primary"]:
        raise ValueError("author_investigation requires the complete primary inventory")
    packet = deepcopy(packet)
    packet["kind"] = "author_investigation"
    docs, seen = [], set()
    for role in ("primary", "secondary"):
        if not isinstance(packet.get(role, []), list):
            raise ValueError(f"{role} must be an inventory list")
        for row in packet.get(role) or []:
            if not isinstance(row, dict):
                raise ValueError(f"each {role} entry must be an object")
            uid = str(row.get("uid") or "").strip()
            key = f"{role}:{uid}"
            if not uid or key in seen:
                raise ValueError(f"missing or duplicate {role} uid: {uid}")
            seen.add(key)
            body = row.pop("body", None)
            if body is None:
                body = row.pop("text", "")
            row.pop("text", None)
            if not isinstance(body, str):
                raise ValueError(f"body must be a string: {key}")
            row["body_chars"] = len(body)
            row["body_sha256"] = hashlib.sha256(body.encode()).hexdigest() if body else None
            row.setdefault("body_state", "available" if body else "missing")
            row["source_key"] = key
            if body:
                docs.append(Document(key=key, title=row.get("title") or uid, text=body,
                                     creators=packet["author"].get("name", "") if role == "primary" else "",
                                     year=str(row.get("year") or ""), role="source"))
    inventory = {"question": packet["question"], "author": packet["author"], "scope": packet.get("scope", {}),
                 "primary": packet["primary"]}
    docs.insert(0, Document(key="investigation-inventory", title="Question and primary inventory (metadata and profiles)",
                           text=json.dumps(inventory, ensure_ascii=False), role="source"))
    docs.append(Document(key="investigation", title="Frozen investigation context", role="plan",
                         text=json.dumps(packet, ensure_ascii=False)))
    return docs
