"""The macro-actions engine's document and parser (Evgeny, 2026-09-07 18:30: approve once, and the ten are approved). By code: a page's
suggested actions rendered as lines the engine anchors in; the engine's rows turned into macros with the micro actions each enables.
Shape only."""
from __future__ import annotations

import json
import re
from typing import Any, Optional

LEAVE = "leave_for_now"


def render_actions_document(actions: list[dict], context: Optional[dict] = None) -> str:
    """One line per micro action, under its finding's line: what the page offers, as the engine reads it."""
    lines = ["SOURCE ROLE: actions", "THE PAGE'S SUGGESTED ACTIONS (each finding, then the micro actions it licenses)"]
    if context:
        lines.append("CONTEXT: " + "; ".join(f"{k}: {v}" for k, v in context.items() if v not in (None, "", [], {})))
    lines.append("")
    for i, entry in enumerate(actions, start=1):
        finding = entry.get("finding") or f"row {i}"
        head = f"[{finding}] {entry.get('kind', '')}: {entry.get('cited', '')}"
        flags = "; ".join(x for x in (f"held {entry['held']}" if entry.get("held") else "", f"in the Referee {entry['in_referee']}" if entry.get("in_referee") else "") if x)
        if flags:
            head += f" ({flags})"
        if entry.get("used_for"):
            head += f" — used for: {entry['used_for']}"
        pl = entry.get("placement") or {}
        if pl:
            fits = ", ".join(f"{f.get('school_name') or f.get('school')}" for f in pl.get("fits") or [])
            head += f" — placement: {pl.get('verdict', '')}" + (f" ({fits})" if fits else "") + (f"; new school {pl['new_school'].get('name')}" if pl.get("new_school") else "")
        lines.append(head)
        for a in entry.get("actions") or []:
            lines.append(f"  · ready: {a.get('action')} on {a.get('organ')} (cost {a.get('cost', 'none')}; intents {', '.join(a.get('intents') or []) or 'unstated'}) inputs {json.dumps(a.get('inputs') or {}, ensure_ascii=False)[:200]}")
        for w in entry.get("waiting") or []:
            lines.append(f"  · waiting: {w.get('action')} on {w.get('organ')} needs {', '.join(w.get('missing') or [])}")
    return "\n".join(lines)


def _kv(s: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in re.split(r";\s*", s or ""):
        if "=" in part:
            k, v = part.split("=", 1)
            if k.strip() and v.strip().lower() != "none":
                out[k.strip()] = v.strip()
    return out


def parse_macros(rows: list[dict], allowed_intents: list[str]) -> dict:
    """The engine's rows → {macros: [{id, title, intent, says, cost_class, estimate, enables: [{action, organ, inputs, finding}]}],
    unplaced: [micro rows whose macro id matched no macro]}. An intent outside the vocabulary (other than leave_for_now) is kept
    under `intent_raw` and the macro's intent set to leave_for_now, never invented."""
    macros: dict[str, dict] = {}
    for r in rows:
        if (r.get("dim") or "") != "macro":
            continue
        f = r.get("fields") or {}
        intent = (f.get("intent") or "").strip().lower().replace(" ", "_")
        m = {"id": r.get("id"), "title": (r.get("finding") or r.get("text") or "").strip(), "intent": intent if intent in allowed_intents or intent == LEAVE else LEAVE,
             "says": f.get("says", ""), "cost_class": f.get("cost_class", ""), "estimate": f.get("estimate", ""), "anchor": r.get("anchor", ""),
             "conjecture": not r.get("anchor_verified", True), "enables": []}
        if m["intent"] == LEAVE and intent and intent != LEAVE:
            m["intent_raw"] = intent
        macros[r.get("id")] = m
    unplaced = []
    for r in rows:
        if (r.get("dim") or "") != "enables":
            continue
        f = r.get("fields") or {}
        micro = {"id": r.get("id"), "action": f.get("action", ""), "organ": f.get("organ", ""), "inputs": _kv(f.get("inputs", "")), "finding": f.get("finding", ""),
                 "text": (r.get("finding") or r.get("text") or "").strip(), "conjecture": not r.get("anchor_verified", True)}
        target = macros.get((f.get("macro") or "").strip())
        (target["enables"] if target else unplaced).append(micro)
    return {"macros": list(macros.values()), "unplaced": unplaced}
