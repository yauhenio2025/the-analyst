"""The makers: each exhibit kind the registry seeds, built by code from an oeuvre answer's rows (2026-09-07). HTML for chips,
sidebars, cards, tables, glossary and pull quotes; SVG for the timeline and the two halves (src/exhibits/svg.py); the idea map
is an image commission (the figure pipeline) and is described here until it is drawn. A maker returns {html, description}:
the html the page places, the description the reviewer reads (what it shows, from which rows). No model call.
"""
from __future__ import annotations

import html
import re
from typing import Any, Optional

from src.exhibits.svg import timeline_svg, two_halves_svg

SENTENCE_END = re.compile("[.!?\u2026][\"'\u201d\u2019)]*$")


def _e(s: Any) -> str:
    return html.escape(str(s or ""), quote=True)


def _rows_by_id(o: dict) -> dict[str, dict]:
    out = {}
    for group, engine in (("agendas", "oeuvre_trajectory"), ("turns", "oeuvre_trajectory"), ("place", "oeuvre_trajectory"), ("shifts", "citation_shift"),
                          ("retrospective", "retrospective_reading"), ("prospective", "prospective_reading"), ("rupture", "epistemic_rupture"),
                          ("read_next", "oeuvre_position_memo"), ("open", "oeuvre_position_memo")):
        for r in o.get(group) or []:
            out[f"{engine}/{r['id']}"] = {**r, "engine": engine, "group": group}
    return out


def _pick(o: dict, ids: list[str], group: Optional[str] = None) -> list[dict]:
    by = _rows_by_id(o)
    got = [by[i] for i in ids if i in by]
    if group:
        got = [r for r in got if r["group"] == group]
    return got


_VOCAB = {"position": "oeuvre_positions", "place": "oeuvre_positions", "retrospective": "retrospective_verdicts", "prospective": "prospective_verdicts", "rupture": "rupture_verdicts"}


def _gloss(key: str, value: Optional[str]) -> str:
    """The vocabulary's gloss for a verdict value (the reviewer flagged an unglossed label)."""
    try:
        from src.vocabularies.registry import get_vocabulary_registry
        voc = get_vocabulary_registry().get(_VOCAB.get(key, ""))
        for x in (voc.values if voc else []):
            if x.value == value:
                return x.gloss
    except Exception:
        pass
    return "not given" if not value else ""


def verdict_chips(o: dict, **_) -> dict:
    v = o.get("verdicts") or {}
    order = [("position", "read whole"), ("retrospective", "looking back"), ("prospective", "looking forward"), ("rupture", "rupture?"), ("place", "place")]
    chips = "".join(f'<span class="chip" title="{_e(_gloss(key, v.get(key)))}"><span class="k">{_e(lab)}</span> {_e(v.get(key) or "not given")}</span>' for key, lab in order)
    halves = f'<div class="halves"><span class="k">the two halves</span> {_e(v.get("halves"))}</div>' if v.get("halves") else ""
    return {"html": f'<div class="chips">{chips}</div>{halves}', "description": "Five verdict chips, each with its gloss on hover: " + "; ".join(f"{lab} = {v.get(key) or 'not given'} ({_gloss(key, v.get(key))})" for key, lab in order) + (f". The two halves: {v.get('halves')}" if v.get("halves") else "")}


def persists_breaks_sidebar(o: dict, rows: Optional[list[str]] = None, **_) -> dict:
    rup = o.get("rupture") or []
    cont = [r for r in rup if r.get("dim") == "continuity"][:3]; brk = [r for r in rup if r.get("dim") == "break"][:3]
    def li(r, kind):
        return f'<li><b>{_e(r.get("what"))}</b> {_e(r.get("text"))} <span class="rid">[epistemic_rupture/{_e(r["id"])}]</span></li>'
    h = f'<aside class="box two"><div><h4>What persists</h4><ul>{"".join(li(r, "p") for r in cont)}</ul></div><div><h4>What breaks</h4><ul>{"".join(li(r, "b") for r in brk)}</ul></div></aside>'
    return {"html": h, "description": "Sidebar, two boxes. Persists: " + "; ".join(f"{r.get('what')} — {r.get('text')}" for r in cont) + ". Breaks: " + "; ".join(f"{r.get('what')} — {r.get('text')}" for r in brk)}


def reading_route_cards(o: dict, **_) -> dict:
    cards = []
    for r in o.get("read_next") or []:
        cards.append(f'<div class="card"><div class="rank">{_e(r.get("rank") or "")}</div><div class="body"><div class="t">{_e(r.get("text"))}</div><div class="why">{_e(r.get("why"))}</div><div class="meta">held {_e(r.get("held"))} · <span class="rid">[oeuvre_position_memo/{_e(r["id"])}]</span></div></div></div>')
    return {"html": f'<div class="cards">{"".join(cards)}</div>', "description": "Reading route cards, ranked: " + "; ".join(f"{r.get('rank')}. {r.get('text')} — {r.get('why', '')} (held {r.get('held')})" for r in o.get("read_next") or [])}


def shift_table(o: dict, **_) -> dict:
    kinds = ["first_cited", "dropped", "carried", "anomaly", "unexamined"]
    rows = [s for s in o.get("shifts") or [] if s.get("dim") in kinds]
    trs = "".join(f'<tr class="{_e(s["dim"])}"><td>{_e(s["dim"].replace("_", " "))}</td><td>{_e(s.get("cited") or s.get("text")[:60])}</td><td>{_e(s.get("kind") or "")}</td><td>{_e(s.get("for") or s.get("used_for") or s.get("silence") or s.get("use_here") or "")[:120]}</td><td>{_e(s.get("held") or "")}</td><td>{_e(s.get("in_referee") or "")}</td><td class="rid">citation_shift/{_e(s["id"])}{" · not verified" if s.get("conjecture") else ""}</td></tr>' for s in rows)
    h = f'<table class="shift"><thead><tr><th>kind</th><th>cited</th><th>work / person</th><th>for</th><th>held</th><th>in the Referee</th><th>row</th></tr></thead><tbody>{trs}</tbody></table>'
    return {"html": h, "description": f"Table of {len(rows)} citation shifts (kind · cited · for · held · in the Referee): " + "; ".join(f"{s['dim']}: {s.get('cited') or s.get('text')} — {s.get('for') or s.get('used_for') or s.get('silence') or ''} (held {s.get('held')}, Referee {s.get('in_referee')})" for s in rows)}


def glossary_box(o: dict, **_) -> dict:
    terms: list[tuple[str, str]] = []
    for a in o.get("agendas") or []:
        for t in re.split(r"[;,]\s*", a.get("concepts") or ""):
            t = t.strip()
            if t and t.lower() not in {x.lower() for x, _ in terms}:
                terms.append((t, a.get("text", "")[:90]))
    terms = terms[:5]
    h = '<aside class="box glossary"><h4>The five terms</h4><dl>' + "".join(f'<dt>{_e(t)}</dt><dd>{_e(g)}</dd>' for t, g in terms) + '</dl></aside>'
    return {"html": h, "description": "Glossary box: " + "; ".join(t for t, _ in terms)}


def pull_quote(o: dict, rows: Optional[list[str]] = None, **_) -> dict:
    cands = _pick(o, rows or []) or [r for r in _rows_by_id(o).values() if r.get("anchor") and not r.get("conjecture")]
    cands = [r for r in cands if r.get("anchor") and not r.get("conjecture")]
    whole = [r for r in cands if SENTENCE_END.search(r["anchor"].strip())]   # a quote that ends a sentence; a fragment cut at the wall's 200 characters states no claim
    cands = whole or cands
    if not cands:
        return {"html": "", "description": "no verified anchor to quote"}
    r = cands[0]
    h = f'<blockquote class="pull">“{_e(r["anchor"])}”<footer>{_e(r.get("doc"))} · <span class="rid">[{_e(r["engine"])}/{_e(r["id"])}]</span></footer></blockquote>'
    return {"html": h, "description": f"Pull quote from {r.get('doc')}: “{r['anchor']}”"}


def oeuvre_timeline(o: dict, packet: Optional[dict] = None, **_) -> dict:
    return {"html": timeline_svg(o, packet or {}, width=1040), "description": "Timeline (SVG): the author's texts as ticks on a year axis; the agendas as lanes from their first to their last text, each lane labelled with the agenda's first words and its full row on hover: " + "; ".join(f"{a['id']} — {a.get('text', '')} ({a.get('span', '')})" for a in o.get("agendas") or []) + ". The focal text marked with its year and title. The turns as cuts between their two texts, one row each: " + "; ".join(f"{t['id']} at {t.get('at', '')} — changed {t.get('changed', '')}" for t in o.get("turns") or [])}


def two_halves(o: dict, **_) -> dict:
    v = o.get("verdicts") or {}
    return {"html": two_halves_svg(o, width=1040), "description": f"Split panel: verdict {v.get('rupture')}, halves {v.get('halves')}; persisting lines cross the seam (" + ", ".join(r.get("what", "") for r in o.get("rupture") or [] if r.get("dim") == "continuity") + "); breaking lines stop at it (" + ", ".join(r.get("what", "") for r in o.get("rupture") or [] if r.get("dim") == "break") + ")"}


def idea_map(o: dict, **_) -> dict:
    seeds = [r for r in o.get("prospective") or [] if r.get("dim") == "seed"][:5]; inh = [r for r in o.get("retrospective") or [] if r.get("dim") == "inheritance"][:5]
    desc = "Idea map (an image commission through the figure pipeline; not yet drawn on this page, shown as its caption): in — " + "; ".join(r.get("what") or r.get("text") for r in inh) + "; out — " + "; ".join(r.get("what") or r.get("text") for r in seeds)
    return {"html": f'<figure class="pending"><figcaption>{_e(desc)}</figcaption></figure>', "description": desc}


MAKERS = {"verdict-chips": verdict_chips, "persists-breaks-sidebar": persists_breaks_sidebar, "reading-route-cards": reading_route_cards, "shift-table": shift_table,
          "glossary-box": glossary_box, "pull-quote": pull_quote, "oeuvre-timeline": oeuvre_timeline, "two-halves": two_halves, "idea-map": idea_map}


def make(kind: str, o: dict, *, rows: Optional[list[str]] = None, packet: Optional[dict] = None) -> Optional[dict]:
    fn = MAKERS.get(kind)
    if fn is None:
        return None
    return fn(o, rows=rows, packet=packet)
