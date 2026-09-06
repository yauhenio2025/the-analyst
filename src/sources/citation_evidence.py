"""Unpack supplied citation witnesses without generating evidence or judgments.

An index is a transport envelope, not a third witness. The original A and W
identities remain distinct even when the caller supplies only that envelope.
"""
from __future__ import annotations

import json
import re

FAMILY = {"citation_engagement_map", "citation_fidelity_audit", "citation_reception_map"}


def evidence_indexes(documents: dict[str, str]) -> list[tuple[str, dict]]:
    found = []
    for key, text in documents.items():
        try:
            obj = json.loads(text)
        except (ValueError, TypeError):
            continue
        if isinstance(obj, dict) and (obj.get("role") == "evidence_index" or
                                     {"author", "person", "texts", "checks"} <= obj.keys()):
            if not isinstance(obj.get("texts"), list) or not isinstance(obj.get("checks"), list):
                raise ValueError("citation evidence index requires texts and checks arrays")
            found.append((key, obj))
    return found


def plan_context(documents: dict[str, str]) -> str:
    plans = [obj["plan"] for _, obj in evidence_indexes(documents) if obj.get("plan")]
    if not plans:
        return ""
    return ("UPSTREAM CITATION PLAN (questions, warnings and themes; planning context, not findings). "
            "Use the engagement themes as the reception spine and label readers' additions. "
            "Test the plan's suggestions against the sources.\n" + json.dumps(plans, ensure_ascii=False))


def prepare_citation_sources(engine_key: str, documents: dict[str, str]) -> tuple[dict[str, str], str]:
    if engine_key not in FAMILY:
        return documents, ""
    from src.sources.memo_statements import statements_documents
    documents = statements_documents(documents)   # a memo's statements against its sources arrive as an index (2026-09-06)
    indexes = evidence_indexes(documents)
    if not indexes:
        return documents, ""
    sources = {k: v for k, v in documents.items() if k not in {k for k, _ in indexes}}
    metadata = []
    for _, obj in indexes:
        # Group passages by original source key; repeated quotations never become
        # independent witnesses. Prefer a supplied complete source with that key.
        for text in obj["texts"]:
            key = text.get("uid") or text.get("key")
            if not key:
                raise ValueError("citation text needs an original uid/key")
            if key not in sources:
                parts = [p.get("section") or p.get("window") or
                         "\n".join(p.get(n, "") for n in ("before", "hit", "after"))
                         for p in text.get("passages", [])]
                body = text.get("text") or "\n\n".join(dict.fromkeys(p for p in parts if p.strip()))
                if body.strip():
                    sources[key] = (f"SOURCE ROLE: citing_author\nTITLE: {text.get('title', key)}\n"
                                    f"YEAR: {text.get('year') or 'unknown'}\nCOVERAGE: supplied citation witnesses\n\n{body}")
        for check in obj["checks"]:
            key = (check.get("copy") or {}).get("uid")
            if not key:
                raise ValueError("citation check needs copy.uid (the held witness identity)")
            if any(key == (t.get("uid") or t.get("key")) for t in obj["texts"]):
                raise ValueError("A and W must have distinct source identities")
            parts = []
            for win in check.get("windows", []):
                if win.get("how") not in ("page", "section", "search"):
                    raise ValueError("retrieved window how must be page, section or search")
                if not isinstance(win.get("text"), str) or not win["text"].strip():
                    raise ValueError("retrieved window must carry literal source text")
                parts.append(win["text"])
            if parts and key not in sources:
                sources[key] = (f"SOURCE ROLE: primary_window\nTITLE: {check.get('title', key)}\n"
                                f"COPY: {json.dumps(check.get('copy'), ensure_ascii=False)}\n\n"
                                + "\n\n".join(dict.fromkeys(parts)))
            elif parts:
                # Multiple checks may retrieve different windows of the same work.
                for part in dict.fromkeys(parts):
                    if part not in sources[key]:
                        sources[key] += "\n\n" + part
        slim = {k: v for k, v in obj.items() if k not in ("texts", "checks", "plan")}
        slim["texts"] = [{k: v for k, v in t.items() if k not in ("text", "passages")} |
                         {"passages": [{k: v for k, v in p.items() if k not in
                                        ("section", "window", "before", "hit", "after")}
                                       for p in t.get("passages", [])]} for t in obj["texts"]]
        slim["checks"] = [{k: v for k, v in c.items() if k != "windows"} |
                          {"windows": [{k: v for k, v in w.items() if k != "text"}
                                       for w in c.get("windows", [])]} for c in obj["checks"]]
        metadata.append(slim)
    allowed = {"citation_engagement_map": {"citing_author"},
               "citation_fidelity_audit": {"citing_author", "primary_window"},
               "citation_reception_map": {"citing_author", "secondary_reader"}}[engine_key]
    def in_scope(body):
        role = re.match(r"SOURCE ROLE: (\w+)", body)
        return not role or role[1] in allowed
    sources = {k: v for k, v in sources.items() if in_scope(v)}
    if not sources:
        raise ValueError("citation index supplied no usable witnesses for this engine")
    context = plan_context(documents) + "\n\nCITATION INDEX METADATA (not an anchor source):\n" + json.dumps(metadata, ensure_ascii=False)
    return sources, context


def with_citation_context(call_fn, context):
    """Carry the index's plan through extraction, critique and every synthesis."""
    if not context:
        return call_fn
    def call(system, user, **kwargs):
        return call_fn(system, context + "\n\n=====\n\n" + user, **kwargs)
    return call
