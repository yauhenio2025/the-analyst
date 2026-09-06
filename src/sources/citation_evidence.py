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


def _bare(k) -> str:
    k = str(k or "")
    return k[3:] if k.startswith("em:") else k


def _same(a, b) -> bool:
    return bool(a) and bool(b) and _bare(a) == _bare(b)


def _alias_index(sources: dict[str, str]) -> dict[str, str]:
    """Every name a supplied document answers to (its key, with and without the em: prefix, and a ZOTERO UID line
    in its header) → its key in `sources`."""
    out = {}
    for k, body in sources.items():
        for alias in {k, _bare(k), f"em:{_bare(k)}"}:
            out.setdefault(alias, k)
        m = re.search(r"^ZOTERO UID: (\S+)", body[:600], re.M)
        if m:
            for alias in {m.group(1), _bare(m.group(1)), f"em:{_bare(m.group(1))}"}:
                out.setdefault(alias, k)
    return out


def _meet(supplied: dict[str, str], *names) -> str:
    for n in names:
        if not n:
            continue
        for alias in (str(n), _bare(n), f"em:{_bare(n)}"):
            if alias in supplied:
                return supplied[alias]
    return ""


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
    supplied = _alias_index(sources)
    for _, obj in indexes:
        # The index's `roles` map (Zotero key → citing_author | primary_window | secondary_reader) labels supplied
        # documents that carry no SOURCE ROLE line of their own, before the scope filter below (2026-09-06, the Stacks' Q2).
        for rk, role in (obj.get("roles") or {}).items():
            sk = supplied.get(rk) or supplied.get(f"em:{rk}")
            if sk and role in ("citing_author", "primary_window", "secondary_reader") and not re.match(r"SOURCE ROLE: \w+", sources[sk]):
                sources[sk] = f"SOURCE ROLE: {role}\n" + sources[sk]
        # Group passages by original source key; repeated quotations never become
        # independent witnesses. Prefer a supplied complete source with that key —
        # matched by uid OR key, with or without the em: prefix (2026-09-06, the Stacks' Q1).
        for text in obj["texts"]:
            key = text.get("uid") or text.get("key")
            if not key:
                raise ValueError("citation text needs an original uid/key")
            met = _meet(supplied, text.get("uid"), text.get("key"))
            if met:
                text["supplied_as"] = met
                scope = text.get("scope") or {}
                if scope.get("sliced") and "COVERAGE:" not in sources[met][:800]:
                    # a sliced citing text (the Stacks send the pages around the located citations for long texts,
                    # 2026-09-06) is a witness of those pages, not of the whole text: say so in the header the engines read
                    line = (f"COVERAGE: sliced — {scope.get('pages_kept') or '?'} of {scope.get('pages') or '?'} pages kept around the located "
                            f"citations ({scope.get('chars') or '?'} of {scope.get('of_chars') or '?'} chars); the argument of the whole text is "
                            f"not in evidence here unless a work profile supplies it")
                    body = sources[met]
                    sources[met] = (body.replace("\n", "\n" + line + "\n", 1) if body.startswith("SOURCE ROLE:") else line + "\n" + body)
            if not met and key not in sources:
                parts = [p.get("section") or p.get("window") or
                         "\n".join(p.get(n, "") for n in ("before", "hit", "after"))
                         for p in text.get("passages", [])]
                body = text.get("text") or "\n\n".join(dict.fromkeys(p for p in parts if p.strip()))
                if body.strip():
                    sources[key] = (f"SOURCE ROLE: citing_author\nTITLE: {text.get('title', key)}\n"
                                    f"YEAR: {text.get('year') or 'unknown'}\nCOVERAGE: supplied citation witnesses\n\n{body}")
        for check in obj["checks"]:
            copy = check.get("copy") or {}
            key = copy.get("uid")
            if not key:
                raise ValueError("citation check needs copy.uid (the held witness identity)")
            if any(_same(key, t.get("uid")) or _same(key, t.get("key")) for t in obj["texts"]):
                raise ValueError("A and W must have distinct source identities")
            met = _meet(supplied, copy.get("uid"), copy.get("key"))
            if met:
                check["supplied_as"] = met
                key = met
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
