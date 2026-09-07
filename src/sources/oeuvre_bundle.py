"""The Stacks' oeuvre bundle → the documents the oeuvre engines read (Evgeny, 2026-09-07: a paper's place in its author's
oeuvre). One `role: oeuvre` source carries {author, focal, before[], after[]} (the Stacks' GET /api/authors/{aid}/oeuvre?focal=);
at the door it becomes: `focal:<uid>` — the focal text whole; `before:<uid>` / `after:<uid>` — one document per other text with
its PROFILE rendered as text (thesis · question · object · tradition · concepts · people · works cited · claims · positions ·
verified passages) and its ledger (works and persons cited, with counts, held, Referee ids); and `oeuvre` (role plan) — the
packet: the ordered list of texts, the author's cited-works table with held / in_referee. The prefixes are the scopes a workflow
step filters on. No judgment here: the profiles are the Stacks' records, quoted as such; the walls anchor rows in these texts.
"""
from __future__ import annotations

import json
import re
from typing import Any, Optional

from src.sources.schemas import Document

BUNDLE_KEYS = {"focal", "before", "after"}


def is_oeuvre_bundle(obj: Any) -> bool:
    return isinstance(obj, dict) and isinstance(obj.get("focal"), dict) and isinstance(obj.get("before"), list) and isinstance(obj.get("after"), list)


def _s(v: Any, n: int = 400) -> str:
    return re.sub(r"\s+", " ", str(v or "")).strip()[:n]


def _year(t: dict) -> str:
    y = t.get("year") or ((t.get("profile") or {}).get("year")) or ""
    return str(y)[:4] if y else "n.d."


def _creators(t: dict) -> str:
    return _s(t.get("creators") or t.get("author") or t.get("creators_short") or "", 120)


def render_profile(t: dict, side: str) -> str:
    """One text's profile and ledger as the document the engines read; every list bounded so an oeuvre of sixty stays readable."""
    p = t.get("profile") or {}
    L = [f"SOURCE ROLE: {side}_text", f"UID: {t.get('uid', '')}", f"TITLE: {_s(t.get('title'), 200)}", f"YEAR: {_year(t)}",
         f"CREATORS: {_creators(t)}", f"TYPE: {_s(t.get('item_type') or t.get('type'), 40)}", ""]
    for k, label in (("thesis", "THESIS"), ("question", "QUESTION"), ("object", "OBJECT"), ("tradition", "TRADITION"), ("contribution", "CONTRIBUTION"), ("period", "PERIOD")):
        if p.get(k):
            L.append(f"{label}: {_s(p[k], 900)}")
    if p.get("cases"):
        L.append("CASES: " + "; ".join(_s(c, 80) for c in p["cases"][:12]))
    if p.get("concepts"):
        L.append("CONCEPTS: " + "; ".join(f"{_s(c.get('term'), 60)} (weight {c.get('weight', '')}): {_s(c.get('gloss'), 200)}" if isinstance(c, dict) else _s(c, 80) for c in p["concepts"][:12]))
    if p.get("people"):
        L.append("PEOPLE: " + "; ".join(f"{_s(x.get('name'), 60)} [{_s(x.get('role'), 20)}] {_s(x.get('stance'), 160)}" if isinstance(x, dict) else _s(x, 80) for x in p["people"][:14]))
    if p.get("works_cited"):
        L.append("WORKS CITED: " + "; ".join(f"{_s(w.get('author'), 50)}, {_s(w.get('title'), 90)} ({_s(w.get('year'), 12)}) [{_s(w.get('role'), 20)}; {'held ' + str(w.get('uid')) if w.get('uid') else 'not held'}]" if isinstance(w, dict) else _s(w, 100) for w in p["works_cited"][:24]))
    if p.get("claims"):
        L.append("CLAIMS:\n" + "\n".join(f"- [{_s(c.get('kind'), 20)}] {_s(c.get('claim'), 400)}" + (f" — against: {_s(c.get('against'), 120)}" if c.get('against') else "") if isinstance(c, dict) else f"- {_s(c, 400)}" for c in p["claims"][:10]))
    if p.get("positions"):
        L.append("POSITIONS:\n" + "\n".join(f"- {_s(x.get('debate'), 160)}: {_s(x.get('side'), 300)}" + (f" — against: {_s(x.get('against'), 160)}" if x.get('against') else "") if isinstance(x, dict) else f"- {_s(x, 300)}" for x in p["positions"][:10]))
    if p.get("passages"):
        L.append("VERIFIED PASSAGES:\n" + "\n".join(f"- \"{_s(x.get('quote'), 400)}\" ({_s(x.get('locus'), 40)}; {_s(x.get('why'), 120)})" if isinstance(x, dict) else f"- \"{_s(x, 400)}\"" for x in p["passages"][:6] if not isinstance(x, dict) or x.get("verified", True)))
    led = t.get("ledger") or {}
    if led.get("works"):
        L.append("LEDGER, WORKS CITED: " + "; ".join(f"{_s(w.get('authors') or w.get('author'), 50)}, {_s(w.get('title'), 90)} ({_s(w.get('year'), 12)}) ×{w.get('n_events', w.get('n', ''))} [{'held ' + str(w.get('held')) if w.get('held') else 'not held'}]" for w in led["works"][:30]))
    if led.get("persons"):
        L.append("LEDGER, PERSONS CITED: " + "; ".join(f"{_s(x.get('name'), 60)} ×{x.get('n_events', x.get('n', ''))}" + (f" modes {json.dumps(x.get('modes'))}" if x.get('modes') else "") + (f" [referee {x.get('referee_thinker_id')}]" if x.get('referee_thinker_id') else " [not in referee]") for x in led["persons"][:30]))
    return "\n".join(L)


def packet_of(obj: dict) -> dict:
    """The plan packet: the texts in order with years, held and profiled flags; the cited-works table with held / in_referee."""
    focal = obj["focal"]; before = obj["before"]; after = obj["after"]
    def row(t, side):
        return {"uid": t.get("uid"), "year": _year(t), "title": _s(t.get("title"), 160), "side": side, "profiled": bool(t.get("profile")),
                "held": bool(t.get("text") or t.get("profile"))}
    texts = [row(t, "before") for t in before] + [row(focal, "focal")] + [row(t, "after") for t in after]
    cited: dict[str, dict] = {}
    for side, ts in (("before", before), ("focal", [focal]), ("after", after)):
        for t in ts:
            led = t.get("ledger") or {}
            for w in (led.get("works") or []) + [{"title": w.get("title"), "authors": w.get("author"), "year": w.get("year"), "held": w.get("uid")} for w in ((t.get("profile") or {}).get("works_cited") or []) if isinstance(w, dict)]:
                key = (w.get("key") or f"{_s(w.get('authors') or w.get('author'), 40)}|{_s(w.get('title'), 80)}").lower()
                c = cited.setdefault(key, {"title": _s(w.get("title"), 120), "authors": _s(w.get("authors") or w.get("author"), 60), "year": _s(w.get("year"), 12), "held": bool(w.get("held")), "cited_in": {"before": [], "focal": [], "after": []}})
                c["held"] = c["held"] or bool(w.get("held"))
                if t.get("uid") not in c["cited_in"][side]:
                    c["cited_in"][side].append(t.get("uid"))
            for x in led.get("persons") or []:
                key = "person|" + _s(x.get("norm") or x.get("name"), 60).lower()
                c = cited.setdefault(key, {"person": _s(x.get("name"), 60), "in_referee": bool(x.get("referee_thinker_id")), "referee_thinker_id": x.get("referee_thinker_id"), "cited_in": {"before": [], "focal": [], "after": []}})
                c["in_referee"] = c["in_referee"] or bool(x.get("referee_thinker_id"))
                if t.get("uid") not in c["cited_in"][side]:
                    c["cited_in"][side].append(t.get("uid"))
    def _dedupe(rows):
        seen, out = set(), []
        for v in rows:
            name = re.sub(r"[^a-z0-9]+", " ", (v.get("person") or v.get("title") or "").lower()).strip()[:60]
            if name and name not in seen:
                seen.add(name); out.append(v)
        return out
    first = _dedupe([v for v in cited.values() if v["cited_in"]["focal"] and not v["cited_in"]["before"]])
    dropped = _dedupe(sorted([v for v in cited.values() if v["cited_in"]["before"] and not v["cited_in"]["focal"]], key=lambda v: -len(v["cited_in"]["before"])))
    author = obj.get("author") if isinstance(obj.get("author"), dict) else {"id": obj.get("author")}
    return {"role": "plan", "kind": "oeuvre", "author": author, "focal": {"uid": focal.get("uid"), "title": _s(focal.get("title"), 200), "year": _year(focal)},
            "texts": texts, "counts": {"before": len(before), "after": len(after), "profiled": sum(1 for t in texts if t["profiled"])},
            "settings": obj.get("settings") or {}, "undated": [row(t, "undated") for t in obj.get("undated") or []],
            "cited_first_in_focal": first[:60], "cited_before_not_in_focal": dropped[:60], "cited_table_size": len(cited),
            "notes": ["Keys focal:<uid>, before:<uid>, after:<uid> are the documents; a step's scope names the prefixes it reads.",
                      "held and in_referee come from the Stacks' ledger and the Referee ids they carry; a row must copy them, never guess them.",
                      "Same-year texts are unordered; input order proves no sequence."]}


def expand_oeuvre_bundle(text: str, key_hint: str = "oeuvre") -> list[Document]:
    """The bundle JSON → Documents: focal:<uid> (role source, the body), before:/after:<uid> (role source, the profile as text), and
    the packet (role plan)."""
    obj = json.loads(text)
    if not is_oeuvre_bundle(obj):
        raise ValueError("an oeuvre bundle needs `focal` (an object) and `before` / `after` (lists)")
    focal = obj["focal"]
    body = focal.get("text") or ""
    if isinstance(body, (list, tuple)):
        body = max((x for x in body if isinstance(x, str)), key=len, default="")
    if not body.strip():
        raise ValueError("the focal text needs its body under focal.text")
    docs = [Document(key=f"focal:{focal.get('uid')}", title=f"{_creators(focal)} ({_year(focal)}) — {_s(focal.get('title'), 160)}", creators=_creators(focal), year=_year(focal),
                     stacks_key=str(focal.get("uid") or ""), text=f"SOURCE ROLE: focal_text\nUID: {focal.get('uid')}\nTITLE: {_s(focal.get('title'), 200)}\nYEAR: {_year(focal)}\n\n{body}", char_count=len(body), role="source")]
    for side in ("before", "after"):
        for t in obj[side]:
            if not t.get("profile"):
                continue
            rendered = render_profile(t, side)
            docs.append(Document(key=f"{side}:{t.get('uid')}", title=f"{_creators(t)} ({_year(t)}) — {_s(t.get('title'), 160)} [profile]", creators=_creators(t), year=_year(t),
                                 stacks_key=str(t.get("uid") or ""), text=rendered, char_count=len(rendered), role="source"))
    packet = packet_of(obj)
    docs.append(Document(key=key_hint if key_hint != "oeuvre" else "oeuvre", title=f"The oeuvre packet: {packet['focal']['title']}", text=json.dumps(packet, ensure_ascii=False, indent=1), char_count=0, role="plan"))
    return docs
