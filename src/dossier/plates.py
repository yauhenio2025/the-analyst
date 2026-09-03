"""Plates — one dense 4K diagram that IS the analysis (analyzer v1's multi-visual "perspective" renders).

    plan (Sonnet, forced-tool JSON)  →  PlateSpec[]        plan_plates      (+ validate_plate_spec = the wall)
    spec → prose lines               →  list[str]          plate_content_lines   (deterministic; sizes as words)
    prose → prompt                   →  str                build_plate_prompt    (v1's assembly order)
    prompt → 4K image                →  bytes              src.images.adapter.generate_image(gemini_pro, "4K")
    image × spec → verdict           →  dict               check_plate (overview + 4 tiles, leak scan)
    not ok → re-render ONCE with the reviewer's notes; keep the better attempt; both on the record

The process this ports, stage by stage, is written up in communications/changes/plates-process.md.
A plate differs from a figure (src/dossier/figures.py) in kind, not in degree: a figure is one
diagram inserted into a section; a plate is the report — 40-110 text elements, one-line definitions
on the nodes, labelled relations, quadrants with items, stations with tributaries, register rows with
badges — read instead of the memo. Plates never touch the dossier run (runner/compose); they are a
standalone capability over a finished job, invoked from the API or the CLI below.

Skip law: a plate that cannot be planned or rendered is recorded as skipped/failed with its reason;
the batch continues and never raises past `run_plates`.
"""
from __future__ import annotations

import argparse
import base64
import json
import logging
import os
import re
import threading
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Optional

from pydantic import BaseModel, Field

from src.display.enforcement import GLOBAL_PROHIBITIONS, check_criteria, enforcement_block, format_entry, normalize_format_key
from src.dossier import events
from src.dossier.common import AUDIENCE_REGISTER, analysis_prose, compact_profiles, job_dir
from src.dossier.receipts import make_receipt, record
from src.dossier.schemas import DossierJob, FigureAnchor
from src.dossier.walls import normalize

logger = logging.getLogger(__name__)

STEP = "plates"
DEFAULT_PROVIDER = "gemini_pro"          # Nano Banana Pro is the only fleet member that renders 4K text
RENDER_SIZE = "4K"
RENDER_TIMEOUT_S = 900
MAX_RENDER_ATTEMPTS = 2                  # first render + one revision (v1's retry, figures' law)
MAX_PLATES = 3
MIN_TEXT_ELEMENTS = 16                   # below this it is a figure, not a plate
MAX_TEXT_ELEMENTS = 110
MAX_TITLE_CHARS = 120   # two lines at 4K
MAX_LABEL_WORDS, MAX_LABEL_CHARS = 24, 170   # plate_a's items are full clauses; one line of a panel
MAX_NOTE_WORDS, MAX_NOTE_CHARS = 24, 160
MAX_CELL_WORDS, MAX_CELL_CHARS = 16, 110
MIN_GROUNDED_FRACTION = 0.4              # plates paraphrase definitions; labels still use the material's words
MATERIAL_MAX_CHARS = 140_000
CHECK_MODEL = "claude-sonnet-4-6"
ASPECTS = ("16:9", "4:3", "3:4", "1:1", "9:16", "3:2", "2:3")

# The leak class (plate_a's "[SIZE_GUIDE: 0.9]", r1's "truncass to 100 chars", r3's "#1e40af"): a rendering
# instruction printed as content. Any string that matches never reaches the image model.
LEAK_RE = re.compile(
    r"\[[^\]]*\]|\{\{|\}\}|#[0-9a-fA-F]{6}\b|(?<![\d.])\b0\.\d+\b"
    r"|\b(?:size[_ ]guide|trunc\w*|lorem ipsum|placeholder|tbd)\b|\b(?:weight|score|thickness|confidence)\s*:",
    re.IGNORECASE,
)
_ELLIPSIS_RE = re.compile(r"(\.\.\.|…)\s*$")


# ══════════════════════════════════════════════════════════════════════════
# Models
# ══════════════════════════════════════════════════════════════════════════

class PlateSpec(BaseModel):
    """One perspective that deserves a whole plate, fully specified before rendering."""
    key: str
    family: str = Field("", description="one of PLATE_FAMILIES")
    visual_format: str = Field("", description="canonical enforcement format the family maps to")
    perspective: str = Field("", description="the perspective's name, e.g. 'Scorecard of theoretical shifts'")
    title: str = Field("", description=f"<= {MAX_TITLE_CHARS} chars; rendered at the top")
    canonical: dict[str, Any] = Field(default_factory=dict, description="the plate's entire content in the family's shape")
    narrative: str = Field("", description="3-5 sentences the reader needs to read the plate (not rendered)")
    size_guides: dict[str, float] = Field(default_factory=dict, description="label -> 0..1 emphasis, kept out of the image")
    style_school: str = ""
    why_this_perspective: str = ""
    claimed_territory: str = ""
    excludes: list[str] = Field(default_factory=list)
    abstraction_level: int = Field(3, description="v1's 1 helicopter … 5 granular")
    aspect: str = ""
    anchors: list[FigureAnchor] = Field(default_factory=list)

    def labels(self) -> list[str]:
        return collect_plate_labels(self.canonical)


class Plate(PlateSpec):
    figure_id: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    prompt: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    cost_usd: float = 0.0
    status: str = "planned"              # planned | generated | skipped | failed
    note: str = ""
    compliance: Optional[dict[str, Any]] = None
    attempts: list[dict[str, Any]] = Field(default_factory=list)
    receipts: list[dict[str, Any]] = Field(default_factory=list)
    grounding: Optional[dict[str, Any]] = None
    declutter: Optional[dict[str, Any]] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ══════════════════════════════════════════════════════════════════════════
# Label walking (what is rendered), sizes as words, leak scan
# ══════════════════════════════════════════════════════════════════════════

_LABEL_KEYS = {"label", "title", "badge", "date", "span", "header", "terminal", "meaning", "low", "high", "verdict", "spine"}
_NOTE_KEYS = {"definition", "note"}
_CONTROL_KEYS = {"size", "x", "y", "tone", "kind", "group", "track", "starred", "weight", "from", "to", "quadrant",
                 "of", "station", "level", "status", "strength", "region", "likelihood"}
_SIZE_WORDS = ((0.3, "very small"), (0.5, "small"), (0.7, "medium"), (0.85, "large"), (1.01, "very large"))


def _s(v: Any) -> str:
    return str(v).strip() if v is not None else ""


def size_word(v: Any) -> str:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return "medium"
    for cut, word in _SIZE_WORDS:
        if f < cut:
            return word
    return "very large"


def _walk(obj: Any, key: Optional[str], out: list[tuple[str, str]]) -> None:
    """Every rendered string as (kind, text): kind ∈ label | note | cell."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in _CONTROL_KEYS and not isinstance(v, (dict, list)):
                continue
            _walk(v, k, out)
    elif isinstance(obj, list):
        for v in obj:
            _walk(v, key if key in ("cells", "items", "steps", "feeds", "drains", "evidence") else key, out)
    elif isinstance(obj, str):
        text = obj.strip()
        if not text or key in _CONTROL_KEYS:
            return
        if key in _NOTE_KEYS:
            out.append(("note", text))
        elif key == "cells":
            out.append(("cell", text))
        else:
            out.append(("label", text))


def rendered_strings(canonical: dict[str, Any]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    _walk(canonical or {}, None, out)
    return out


def collect_plate_labels(canonical: dict[str, Any]) -> list[str]:
    """Every rendered string (labels, notes, cells), deduped, in content order — the manifest."""
    seen, out = set(), []
    for _, text in rendered_strings(canonical):
        k = text.lower()
        if k not in seen:
            seen.add(k)
            out.append(text)
    return out


def content_labels(canonical: dict[str, Any]) -> list[str]:
    """Short labels only (the grounding wall checks these; notes are the planner's paraphrases)."""
    seen, out = set(), []
    for kind, text in rendered_strings(canonical):
        if kind == "label" and text.lower() not in seen:
            seen.add(text.lower())
            out.append(text)
    return out


def leak_scan(text: str) -> list[str]:
    """Tokens that must never be printed: bracketed annotations, hex codes, decimals, instruction words."""
    return [m.group(0) for m in LEAK_RE.finditer(text or "")]


def extract_size_guides(canonical: dict[str, Any]) -> dict[str, float]:
    out: dict[str, float] = {}

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            lab = _s(obj.get("label") or obj.get("title"))
            if lab and obj.get("size") is not None:
                try:
                    out[lab] = max(0.0, min(1.0, float(obj["size"])))
                except (TypeError, ValueError):
                    pass
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(canonical or {})
    return out


# ══════════════════════════════════════════════════════════════════════════
# The families — content model, validator, prose renderer, layout grammar
# ══════════════════════════════════════════════════════════════════════════

def _req_list(d: dict, key: str, lo: int, hi: int, e: list[str], where: str = "canonical") -> list:
    items = d.get(key)
    if not isinstance(items, list) or not items:
        e.append(f"{where}.{key} must be a non-empty list")
        return []
    if len(items) < lo:
        e.append(f"{where}.{key} needs at least {lo} items (got {len(items)}) — a plate is dense")
    if len(items) > hi:
        e.append(f"{where}.{key} must have at most {hi} items (got {len(items)})")
    return items


def _lab(item: Any, e: list[str], where: str, key: str = "label") -> str:
    if isinstance(item, str):
        return item.strip()
    if isinstance(item, dict):
        v = _s(item.get(key))
        if not v:
            e.append(f"{where}: missing '{key}'")
        return v
    e.append(f"{where}: expected an object with '{key}'")
    return ""


def _num(v: Any, lo: float, hi: float) -> Optional[float]:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if lo <= f <= hi else None


def _axis(d: dict, key: str, e: list[str]) -> dict:
    ax = d.get(key)
    if not isinstance(ax, dict) or not _s(ax.get("label")) or not _s(ax.get("low")) or not _s(ax.get("high")):
        e.append(f"canonical.{key} must be {{label, low, high}}")
        return {}
    return ax


def _size_ok(item: Any, e: list[str], where: str) -> None:
    if isinstance(item, dict) and item.get("size") is not None and _num(item.get("size"), 0, 1) is None:
        e.append(f"{where}.size must be a NUMBER between 0 and 1 (got {item.get('size')!r})")


# --- scorecard -------------------------------------------------------------

def _v_scorecard(d: dict, e: list[str]) -> None:
    quads = _req_list(d, "quadrants", 2, 4, e)
    names = []
    for i, q in enumerate(quads):
        w = f"canonical.quadrants[{i}]"
        names.append(_lab(q, e, w))
        if isinstance(q, dict):
            if _s(q.get("tone")).lower() not in ("gain", "loss", "neutral"):
                e.append(f"{w}.tone must be gain | loss | neutral")
            items = q.get("items")
            if not isinstance(items, list) or not (2 <= len(items) <= 10):
                e.append(f"{w}.items must list 2-10 items")
            else:
                for j, it in enumerate(items):
                    _lab(it, e, f"{w}.items[{j}]")
                    _size_ok(it, e, f"{w}.items[{j}]")
    for i, m in enumerate(d.get("marks", []) or []):
        if not isinstance(m, dict) or _s(m.get("quadrant")) not in names or _s(m.get("kind")).lower() not in ("cross", "check", "arrow"):
            e.append(f"canonical.marks[{i}] must be {{quadrant: a quadrant label, kind: cross|check|arrow, label?}}")
    for i, ln in enumerate(d.get("links", []) or []):
        if not isinstance(ln, dict) or _s(ln.get("from")) not in names or _s(ln.get("to")) not in names or not _s(ln.get("label")):
            e.append(f"canonical.links[{i}] must be {{from, to (quadrant labels), label}}")


def _r_scorecard(d: dict) -> list[str]:
    quads = d["quadrants"]
    layout = {2: "two panels side by side", 3: "three panels side by side", 4: "a 2x2 grid of four panels"}.get(len(quads), "a grid of panels")
    out = [f"  Layout: {layout}. Panels in reading order:"]
    for q in quads:
        tone = _s(q.get("tone")).lower()
        out.append(f"  Panel '{q['label']}' ({tone.upper()} panel — {'green' if tone == 'gain' else 'red' if tone == 'loss' else 'grey'} band and tint):")
        for it in q.get("items", []):
            glyph = "↑" if tone == "gain" else "↓" if tone == "loss" else "•"
            note = f" — beneath it, smaller: {it['note']}" if isinstance(it, dict) and it.get("note") else ""
            sz = f" — draw in {size_word(it.get('size'))} type" if isinstance(it, dict) and it.get("size") is not None else ""
            out.append(f"      {glyph} {_lab(it, [], '')}{note}{sz}")
    for m in d.get("marks", []) or []:
        kind = {"cross": "a large translucent red X across the whole panel", "check": "a large translucent green check across the panel",
                "arrow": "a bold arrow glyph in the panel corner"}[_s(m.get("kind")).lower()]
        out.append(f"  Mark on panel '{m['quadrant']}': {kind}" + (f", captioned in small caps: {m['label']}" if m.get("label") else ""))
    for ln in d.get("links", []) or []:
        out.append(f"  Curved labelled arrow from panel '{ln['from']}' to panel '{ln['to']}': {ln['label']}")
    return out


# --- framework_map ---------------------------------------------------------

def _v_framework(d: dict, e: list[str]) -> None:
    regions = _req_list(d, "regions", 1, 3, e)
    nodes: list[str] = []
    rnames: list[str] = []
    for i, r in enumerate(regions):
        w = f"canonical.regions[{i}]"
        rnames.append(_lab(r, e, w))
        if isinstance(r, dict):
            ns = r.get("nodes")
            if not isinstance(ns, list) or not (2 <= len(ns) <= 7):
                e.append(f"{w}.nodes must list 2-7 nodes")
            else:
                for j, n in enumerate(ns):
                    lab = _lab(n, e, f"{w}.nodes[{j}]")
                    nodes.append(lab)
                    if isinstance(n, dict) and not _s(n.get("definition")):
                        e.append(f"{w}.nodes[{j}].definition is required (one line inside the node)")
                    _size_ok(n, e, f"{w}.nodes[{j}]")
    rels = _req_list(d, "relations", 2, 16, e)
    for i, rl in enumerate(rels):
        if not isinstance(rl, dict) or _s(rl.get("from")) not in nodes or _s(rl.get("to")) not in nodes or not _s(rl.get("label")):
            e.append(f"canonical.relations[{i}] must be {{from, to (node labels), label}}")
    for i, b in enumerate(d.get("bridges", []) or []):
        if not isinstance(b, dict) or _s(b.get("from")) not in rnames or _s(b.get("to")) not in rnames or not _s(b.get("label")):
            e.append(f"canonical.bridges[{i}] must be {{from, to (region labels), label}}")
    for i, sb in enumerate(d.get("side_boxes", []) or []):
        if not isinstance(sb, dict) or not _s(sb.get("label")) or not isinstance(sb.get("items"), list) or not (2 <= len(sb["items"]) <= 6):
            e.append(f"canonical.side_boxes[{i}] must be {{label, items: 2-6 strings, region?}}")
    if len(nodes) != len(set(nodes)):
        e.append("node labels must be unique across regions")


def _r_framework(d: dict) -> list[str]:
    regions = d["regions"]
    tints = ["cool blue", "warm orange", "muted green"]
    out = [f"  Layout: {len(regions)} tinted region(s) side by side, each under a large header band."]
    for i, r in enumerate(regions):
        out.append(f"  Region '{r['label']}' ({tints[i % 3]} tint)" + (f" — subtitle line: {r['note']}" if r.get("note") else "") + ":")
        for n in r.get("nodes", []):
            sz = size_word(n.get("size")) if n.get("size") is not None else "medium"
            out.append(f"      Node, drawn {sz}. TITLE: {n['label']} — DEFINITION inside the node: {n['definition']}")
    for rl in d["relations"]:
        style = "dashed" if re.search(r"contrast|tension|oppos|conflict|versus", rl["label"], re.I) else "solid"
        out.append(f"  Relation ({style} labelled arrow): {rl['from']} → {rl['to']} — label: {rl['label']}")
    for b in d.get("bridges", []) or []:
        out.append(f"  Bridge (wide double-headed arrow across the divide) between '{b['from']}' and '{b['to']}': {b['label']}")
    for sb in d.get("side_boxes", []) or []:
        where = f" in region '{sb['region']}'" if sb.get("region") else ""
        out.append(f"  Side box '{sb['label']}'{where}: " + "; ".join(map(_s, sb["items"])))
    return out


# --- flow_map --------------------------------------------------------------

def _v_flow(d: dict, e: list[str]) -> None:
    cur = d.get("current")
    if not isinstance(cur, dict) or not _s(cur.get("label")):
        e.append("canonical.current must be {label, stations: [...]}")
        return
    stations = _req_list(cur, "stations", 3, 9, e, "canonical.current")
    snames = []
    for i, st in enumerate(stations):
        w = f"canonical.current.stations[{i}]"
        snames.append(_lab(st, e, w))
        if isinstance(st, dict):
            for k in ("feeds", "drains"):
                v = st.get(k, []) or []
                if not isinstance(v, list) or len(v) > 4 or not all(isinstance(x, str) and x.strip() for x in v):
                    e.append(f"{w}.{k} must be a list of at most 4 strings")
            _size_ok(st, e, w)
    for i, b in enumerate(d.get("branches", []) or []):
        w = f"canonical.branches[{i}]"
        if not isinstance(b, dict) or not _s(b.get("label")) or _s(b.get("from")) not in snames:
            e.append(f"{w} must be {{label, from: a station label, steps: 1-4 strings, terminal}}")
            continue
        steps = b.get("steps", []) or []
        if not isinstance(steps, list) or not (1 <= len(steps) <= 4) or not all(isinstance(x, str) for x in steps):
            e.append(f"{w}.steps must list 1-4 strings")
        if not _s(b.get("terminal")):
            e.append(f"{w}.terminal is required (e.g. 'Locked In')")
    if len(d.get("branches", []) or []) > 4:
        e.append("canonical.branches: at most 4")


def _r_flow(d: dict) -> list[str]:
    cur = d["current"]
    out = [f"  Main current '{cur['label']}': a wide band flowing LEFT to RIGHT across the upper part of the canvas; its stations in order:"]
    for st in cur["stations"]:
        sz = f", drawn as a {size_word(st.get('size'))} node" if st.get("size") is not None else ""
        out.append(f"      Station: {st['label']}{sz}" + (f" — note beside it: {st['note']}" if st.get("note") else ""))
        for f in st.get("feeds", []) or []:
            out.append(f"          tributary joining from ABOVE, labelled: {f}")
        for dr in st.get("drains", []) or []:
            out.append(f"          band leaving BELOW, labelled: {dr}")
    for b in d.get("branches", []) or []:
        out.append(f"  Branch '{b['label']}' peels off DOWNWARD from station '{b['from']}', passing through: "
                   + " → ".join(map(_s, b["steps"])) + f" → terminal marker: {b['terminal']}")
    return out


# --- power_map -------------------------------------------------------------

def _v_power(d: dict, e: list[str]) -> None:
    _axis(d, "x_axis", e)
    _axis(d, "y_axis", e)
    q = d.get("quadrants")
    if q is not None and (not isinstance(q, dict) or any(k not in ("top_left", "top_right", "bottom_left", "bottom_right") for k in q)):
        e.append("canonical.quadrants must map top_left/top_right/bottom_left/bottom_right to labels")
    actors = _req_list(d, "actors", 5, 16, e)
    names = []
    for i, a in enumerate(actors):
        w = f"canonical.actors[{i}]"
        names.append(_lab(a, e, w))
        if isinstance(a, dict) and (_num(a.get("x"), 0, 1) is None or _num(a.get("y"), 0, 1) is None):
            e.append(f"{w} needs x and y NUMBERS in 0..1")
        _size_ok(a, e, w)
    for i, rl in enumerate(d.get("relations", []) or []):
        if not isinstance(rl, dict) or _s(rl.get("from")) not in names or _s(rl.get("to")) not in names or not _s(rl.get("label")):
            e.append(f"canonical.relations[{i}] must be {{from, to (actor labels), label}}")
    if len(d.get("relations", []) or []) > 12:
        e.append("canonical.relations: at most 12")


def _hpos(x: float) -> str:
    return ("at the far left" if x < 0.2 else "left of centre" if x < 0.4 else "at the horizontal centre" if x <= 0.6
            else "right of centre" if x <= 0.8 else "at the far right")


def _vpos(y: float) -> str:
    return ("at the very bottom" if y < 0.2 else "in the lower half" if y < 0.4 else "at mid-height" if y <= 0.6
            else "in the upper half" if y <= 0.8 else "at the very top")


def _r_power(d: dict) -> list[str]:
    xa, ya = d["x_axis"], d["y_axis"]
    out = [f"  X axis: {xa['label']} (left = {xa['low']}, right = {xa['high']})",
           f"  Y axis: {ya['label']} (bottom = {ya['low']}, top = {ya['high']})"]
    for k in ("top_left", "top_right", "bottom_left", "bottom_right"):
        if (d.get("quadrants") or {}).get(k):
            out.append(f"  Quadrant {k.replace('_', '-')} label: {d['quadrants'][k]}")
    for a in d["actors"]:
        grp = f", group: {a['group']}" if a.get("group") else ""
        sz = size_word(a.get("size")) if a.get("size") is not None else "medium"
        note = f" — note beneath: {a['note']}" if a.get("note") else ""
        out.append(f"  Actor '{a['label']}' — a {sz} labelled circle placed {_hpos(float(a['x']))}, {_vpos(float(a['y']))}{grp}{note}")
    for rl in d.get("relations", []) or []:
        out.append(f"  Relation arrow {rl['from']} → {rl['to']}, labelled: {rl['label']}")
    out.append("  (placements and sizes are instructions for you; print NO coordinates or numbers next to actors)")
    return out


# --- timeline_of_shifts ----------------------------------------------------

def _v_timeline(d: dict, e: list[str]) -> None:
    tracks = d.get("tracks")
    if tracks is not None and (not isinstance(tracks, list) or not (1 <= len(tracks) <= 4) or not all(isinstance(t, str) and t.strip() for t in tracks)):
        e.append("canonical.tracks must be 1-4 track labels")
    for i, p in enumerate(d.get("periods", []) or []):
        if not isinstance(p, dict) or not _s(p.get("label")) or not _s(p.get("span")):
            e.append(f"canonical.periods[{i}] must be {{label, span}}")
    if len(d.get("periods", []) or []) > 6:
        e.append("canonical.periods: at most 6")
    evs = _req_list(d, "events", 5, 16, e)
    names = []
    for i, ev in enumerate(evs):
        w = f"canonical.events[{i}]"
        names.append(_lab(ev, e, w))
        if isinstance(ev, dict):
            if not _s(ev.get("date")):
                e.append(f"{w}.date is required (a year, a period or an era)")
            if tracks and _s(ev.get("track")) and _s(ev.get("track")) not in tracks:
                e.append(f"{w}.track must be one of canonical.tracks")
            _size_ok(ev, e, w)
    for i, sh in enumerate(d.get("shifts", []) or []):
        if not isinstance(sh, dict) or _s(sh.get("from")) not in names or _s(sh.get("to")) not in names or not _s(sh.get("label")):
            e.append(f"canonical.shifts[{i}] must be {{from, to (event labels), label}}")
    if len(d.get("shifts", []) or []) > 6:
        e.append("canonical.shifts: at most 6")


def _r_timeline(d: dict) -> list[str]:
    out = []
    if d.get("tracks"):
        out.append("  Tracks (stacked top to bottom, each labelled at the left): " + "; ".join(d["tracks"]))
    for p in d.get("periods", []) or []:
        out.append(f"  Period band '{p['label']}' spanning {p['span']}")
    for ev in d["events"]:
        tr = f", on track {ev['track']}" if ev.get("track") else ""
        sz = f", {size_word(ev.get('size'))} marker" if ev.get("size") is not None else ""
        note = f" — note beneath: {ev['note']}" if ev.get("note") else ""
        out.append(f"  {ev['date']} — {ev['label']}{tr}{sz}{note}")
    for sh in d.get("shifts", []) or []:
        out.append(f"  Shift (curved labelled arrow) from '{sh['from']}' to '{sh['to']}': {sh['label']}")
    return out


# --- register (the client's argument-architecture tables) ------------------

_CELL_KINDS = ("text", "badge", "glyph", "number", "bar")
_GLYPHS = {"serial": "→→", "convergent": "⇒", "linked": "⊕", "divergent": "⇆", "circular": "↻", "none": "—"}


def _v_register(d: dict, e: list[str]) -> None:
    cols = _req_list(d, "columns", 3, 10, e)
    kinds = []
    for i, c in enumerate(cols):
        _lab(c, e, f"canonical.columns[{i}]")
        k = _s(c.get("kind")).lower() if isinstance(c, dict) else "text"
        if k not in _CELL_KINDS:
            e.append(f"canonical.columns[{i}].kind must be one of {_CELL_KINDS}")
        kinds.append(k)
    rows = _req_list(d, "rows", 3, 12, e)
    for i, r in enumerate(rows):
        w = f"canonical.rows[{i}]"
        _lab(r, e, w)
        cells = r.get("cells") if isinstance(r, dict) else None
        if not isinstance(cells, list) or len(cells) != len(cols) - 1:
            e.append(f"{w}.cells must have exactly {len(cols) - 1} strings — the row label fills the FIRST column, cells fill the remaining {len(cols) - 1}")
            continue
        for j, (cell, k) in enumerate(zip(cells, kinds[1:]), start=1):
            cell = _s(cell)
            if k == "badge" and len(cell.split()) > 3:
                e.append(f"{w}.cells[{j}] is a badge: at most 3 words (got '{cell}')")
            if k == "glyph" and cell.lower() not in _GLYPHS:
                e.append(f"{w}.cells[{j}] is a glyph: one of {sorted(_GLYPHS)}")
            if k == "number" and not re.fullmatch(r"[\d.,%+−-]+|—", cell):
                e.append(f"{w}.cells[{j}] is a number cell: digits only (got '{cell}')")
            if k == "bar" and not re.search(r"\d{1,3}\s*%", cell):
                e.append(f"{w}.cells[{j}] is a bar: a percentage like '78%' (got '{cell}')")
    for i, lg in enumerate(d.get("legend", []) or []):
        if not isinstance(lg, dict) or not _s(lg.get("badge")) or not _s(lg.get("meaning")):
            e.append(f"canonical.legend[{i}] must be {{badge, meaning, tone?}}")
    if len(d.get("legend", []) or []) > 12:
        e.append("canonical.legend: at most 12")


def _r_register(d: dict) -> list[str]:
    cols = d["columns"]
    out = ["  Header band (dark navy, white caps), columns left to right: " + " | ".join(f"{c['label']} — a {_s(c.get('kind') or 'text')} column" for c in cols)]
    for r in d["rows"]:
        star = " ★ (starred row: warm tint, red star in the first cell)" if r.get("starred") else ""
        cells = []
        for c, cell in zip(cols[1:], r["cells"]):
            k = _s(c.get("kind") or "text").lower()
            cell = _s(cell)
            if k == "badge":
                cells.append(f"badge pill '{cell}'")
            elif k == "glyph":
                cells.append(f"glyph icon {_GLYPHS.get(cell.lower(), '—')} ({cell})")
            elif k == "bar":
                cells.append(f"strength bar {cell}")
            elif k == "number":
                cells.append(f"numeral {cell}")
            else:
                cells.append(cell)
        out.append(f"  Row — first column '{r['label']}'{star}; then: " + " | ".join(cells))
    if d.get("legend"):
        out.append("  Legend strip (bottom): " + "; ".join(f"{lg['badge']} = {lg['meaning']}" for lg in d["legend"]))
    return out


# --- layer_stack -----------------------------------------------------------

def _v_layers(d: dict, e: list[str]) -> None:
    layers = _req_list(d, "layers", 3, 7, e)
    for i, layer in enumerate(layers):
        w = f"canonical.layers[{i}]"
        _lab(layer, e, w)
        if isinstance(layer, dict):
            items = layer.get("items")
            if not isinstance(items, list) or not (1 <= len(items) <= 6):
                e.append(f"{w}.items must list 1-6 items")
            else:
                for j, it in enumerate(items):
                    _lab(it, e, f"{w}.items[{j}]")
                    _size_ok(it, e, f"{w}.items[{j}]")


def _r_layers(d: dict) -> list[str]:
    out = []
    if d.get("spine"):
        out.append(f"  Vertical caption at the left edge (top to bottom): {d['spine']}")
    for i, layer in enumerate(d["layers"], 1):
        out.append(f"  Layer {i} ({'top' if i == 1 else 'bottom' if i == len(d['layers']) else 'middle'}) '{layer['label']}'"
                   + (f" — subtitle: {layer['note']}" if layer.get("note") else "") + ":")
        for it in layer["items"]:
            note = f" — beneath it: {it['note']}" if isinstance(it, dict) and it.get("note") else ""
            sz = f", {size_word(it.get('size'))} box" if isinstance(it, dict) and it.get("size") is not None else ""
            out.append(f"      Box: {_lab(it, [], '')}{note}{sz}")
    return out


# --- argument_tree ---------------------------------------------------------

def _v_argument(d: dict, e: list[str]) -> None:
    claim = d.get("claim")
    if not isinstance(claim, dict) or not _s(claim.get("label")):
        e.append("canonical.claim must be {label, note?}")
    prem = _req_list(d, "premises", 2, 6, e)
    for i, p in enumerate(prem):
        w = f"canonical.premises[{i}]"
        _lab(p, e, w)
        if isinstance(p, dict):
            ev = p.get("evidence", []) or []
            if not isinstance(ev, list) or len(ev) > 4 or not all(isinstance(x, str) for x in ev):
                e.append(f"{w}.evidence must be a list of at most 4 strings")
            if p.get("strength") is not None and _num(p.get("strength"), 0, 1) is None:
                e.append(f"{w}.strength must be a NUMBER between 0 and 1")


def _r_argument(d: dict) -> list[str]:
    c = d["claim"]
    out = [f"  CLAIM (large box at the top): {c['label']}" + (f" — beneath it: {c['note']}" if c.get("note") else "")]
    for p in d["premises"]:
        st = f" — {size_word(p.get('strength'))} support, box width follows" if p.get("strength") is not None else ""
        out.append(f"  Premise box: {p['label']}{st}" + (f" — beneath it: {p['note']}" if p.get("note") else ""))
        for ev in p.get("evidence", []) or []:
            out.append(f"      evidence box beneath it: {ev}")
        if p.get("rebuttal"):
            out.append(f"      rebuttal (rose box linked to the premise): {p['rebuttal']}")
    if d.get("verdict"):
        out.append(f"  Verdict line at the bottom: {d['verdict']}")
    return out


PLATE_FAMILIES: dict[str, dict[str, Any]] = {
    "scorecard": {
        "name": "Scorecard of shifts (gains / losses panels)", "format": "structured_diagram", "aspect": "16:9",
        "perspective": "what was gained and what was lost, era by era or position by position — plate_a's grammar",
        "template": {"quadrants": [{"label": "GAINS: …", "tone": "gain|loss|neutral", "items": [{"label": "…", "note?": "…", "size": 0.9}]}],
                     "marks?": [{"quadrant": "a quadrant label", "kind": "cross|check|arrow", "label?": "…"}],
                     "links?": [{"from": "quadrant label", "to": "quadrant label", "label": "…"}]},
        "rule": "2-4 panels of 2-10 full-clause items; tone gain|loss|neutral; size numbers 0-1",
        "validate": _v_scorecard, "render": _r_scorecard,
        "grammar": [
            "A GRID of large labelled PANELS filling the whole canvas (2x2 when four, side by side when two or three), separated by thick dividing lines",
            "Each panel has a bold HEADER BAND printing its label: GAIN panels get a green band and a pale green tint, LOSS panels a red band and a pale rose tint, NEUTRAL panels grey",
            "Inside each panel the items are stacked as full lines of large text, one item per line, with an ↑ glyph beside gains and a ↓ glyph beside losses",
            "Type size follows the size word given per item (very large … small) but never drops below the legibility minimum",
            "Marks: a large translucent red X across a panel marked 'cross'; a translucent green check across a panel marked 'check'; a labelled curved arrow between panels for each link",
            "No chart axes, no scatter points: this is a scorecard of statements",
        ],
    },
    "framework_map": {
        "name": "Conceptual framework map (regions, defined nodes, labelled relations)", "format": "network_graph", "aspect": "16:9",
        "perspective": "how the concepts of one, two or three frameworks/camps relate — plate_b's grammar",
        "template": {"regions": [{"label": "…", "note?": "…", "nodes": [{"label": "…", "definition": "one line", "size": 0.8}]}],
                     "relations": [{"from": "node label", "to": "node label", "label": "ENABLES"}],
                     "bridges?": [{"from": "region label", "to": "region label", "label": "…"}],
                     "side_boxes?": [{"label": "APPLICATIONS", "items": ["…"], "region?": "region label"}]},
        "rule": "1-3 regions of 2-7 nodes each with a one-line definition; 2-16 labelled relations; side boxes of 2-6 items",
        "validate": _v_framework, "render": _r_framework,
        "grammar": [
            "The canvas is divided into the regions side by side, each a large tinted area under a header band naming it (contrasting tints: cool blue, warm orange, muted green)",
            "Each node is a rounded rectangle with a thick coloured outline; it prints its TITLE in bold capitals and, beneath, its one-line DEFINITION in smaller sentence-case text — both inside the node",
            "Relations are labelled arrows between nodes with the label set in small capitals on the arrow: solid for enables/produces/supports, dashed for contrasts/tensions, double-headed for mutual relations",
            "A bridge is a wide double-headed arrow across the divide between two regions carrying its label in the middle",
            "Side boxes are grey rounded boxes titled in capitals with bulleted items, placed in the empty corner of their region",
            "Node size follows the size word; the largest node of each region sits nearest its centre; a dashed outer frame encloses the whole plate",
        ],
    },
    "flow_map": {
        "name": "Flow map of commitments (a main current with stations, tributaries and locked-in branches)", "format": "sankey_diagram", "aspect": "16:9",
        "perspective": "how claims feed a line of argument and which commitments it locks in downstream — plate_c's grammar",
        "template": {"current": {"label": "…", "stations": [{"label": "…", "note?": "…", "feeds?": ["claim"], "drains?": ["consequence"], "size": 0.7}]},
                     "branches?": [{"label": "…", "from": "station label", "steps": ["…"], "terminal": "Locked In"}]},
        "rule": "3-9 stations with up to 4 feeding claims and 3 draining consequences each; up to 4 downstream branches",
        "validate": _v_flow, "render": _r_flow,
        "grammar": [
            "ONE MAIN CURRENT: a wide band flowing left to right across the upper two-thirds of the canvas; each STATION is a labelled widening of the band, in order, its label set in bold on the band",
            "Tributaries are thinner bands joining the main current at their station from above; drains are thinner bands leaving it below; each carries its label beside it, on the band's bank",
            "Each branch peels off downward from its station as its own band, passes through its labelled steps and ends in a labelled terminal marker (e.g. a small circle labelled 'Locked In') at the right edge",
            "Band width follows the size word; a soft two-tone gradient background; NO realistic water, rivers, boats, landscapes or scenery — abstract flowing bands only",
        ],
    },
    "power_map": {
        "name": "Stakeholder power map (two axes, placed actors, relations)", "format": "positioning_map", "aspect": "16:9",
        "perspective": "who holds what power and interest, and who leans on whom",
        "template": {"x_axis": {"label": "…", "low": "…", "high": "…"}, "y_axis": {"label": "…", "low": "…", "high": "…"},
                     "quadrants?": {"top_left": "…", "top_right": "…", "bottom_left": "…", "bottom_right": "…"},
                     "actors": [{"label": "…", "note?": "…", "x": 0.8, "y": 0.7, "size": 0.9, "group?": "…"}],
                     "relations?": [{"from": "actor", "to": "actor", "label": "…"}]},
        "rule": "two labelled axes; 5-16 actors placed by x,y numbers in 0..1 with a size number; up to 12 labelled relations",
        "validate": _v_power, "render": _r_power,
        "grammar": [
            "Two labelled axes with their low and high ends printed; quadrant labels in the four corners in capitals",
            "Actors are labelled circles placed by their given position, circle size by the size word, the label in bold beside or inside the circle and the note beneath it in smaller text",
            "Relations are labelled arrows between actors; groups are colour-coded with a legend in a corner",
            "A clean grid background; no geography, no photographs, no pictograms of people",
        ],
    },
    "timeline_of_shifts": {
        "name": "Timeline of shifts (dated events, period bands, labelled shift arrows)", "format": "timeline", "aspect": "16:9",
        "perspective": "how positions moved over time and what each shift was",
        "template": {"tracks?": ["…"], "periods?": [{"label": "…", "span": "1990-1994"}],
                     "events": [{"date": "1992", "label": "…", "note?": "…", "track?": "…", "size": 0.8}],
                     "shifts?": [{"from": "event label", "to": "event label", "label": "…"}]},
        "rule": "5-16 dated events (tracks optional, up to 4); up to 6 period bands; up to 6 labelled shift arrows",
        "validate": _v_timeline, "render": _r_timeline,
        "grammar": [
            "A horizontal time axis across the canvas with the dates marked (stacked labelled tracks sharing one axis when tracks are given)",
            "Periods are shaded bands along the axis with their labels; events are labelled markers at their dates with the note beneath in smaller text; marker size follows the size word",
            "Shifts are labelled curved arrows from one event to another above the axis",
            "No scene illustrations of the period, no photographs; a clean chart",
        ],
    },
    "register": {
        "name": "Register (a dense badge-and-glyph table — the client's argument-architecture grammar)", "format": "matrix", "aspect": "3:4",
        "perspective": "one row per item (argument, risk, case, actor) scored across typed columns — r1-r4's grammar",
        "template": {"columns": [{"label": "the row-label column", "kind": "text"}, {"label": "…", "kind": "text|badge|glyph|number|bar"}],
                     "rows": [{"label": "fills the first column", "starred?": True, "cells": ["one string per REMAINING column (columns minus one)"]}],
                     "legend?": [{"badge": "HIGH", "meaning": "…", "tone?": "blue"}]},
        "rule": "3-10 typed columns × 3-12 rows; the row label IS the first column, so each row has columns-minus-one cells; text cells ≤ 16 words; badge cells ≤ 3 words; glyph cells one of serial|convergent|linked|divergent|circular|none; bar cells a percentage",
        "validate": _v_register, "render": _r_register,
        "grammar": [
            "A full-width TABLE with a dark navy header band and white capital column headers; alternating pale rows; column widths by content; the first column in bold",
            "Starred rows carry a red ★ in the star column and a warm pale tint across the row",
            "BADGE cells are rounded coloured pills with the badge word in white capitals — one consistent colour per badge word across the whole plate (blues for likelihood grades, green/rust/red/grey/purple for type and warrant families)",
            "GLYPH cells are circular icons with the arrow glyph (serial →→, convergent ⇒, linked ⊕, divergent ⇆, circular ↻) and the word beneath in small text",
            "NUMBER cells are large numerals; BAR cells are a segmented strength bar with the percentage printed beneath it",
            "Text cells wrap in sentence case at a size that stays legible; a row is as tall as its longest cell needs — NEVER cut a cell short, NEVER shorten it with '…' and NEVER print a note about shortening",
            "A legend strip at the bottom explains the badges",
        ],
    },
    "layer_stack": {
        "name": "Layer stack (assumptions and foundations, abstract on top, concrete below)", "format": "conceptual_layers", "aspect": "4:3",
        "perspective": "what rests on what — the strata of assumptions beneath the claims",
        "template": {"spine?": "abstract → concrete", "layers": [{"label": "…", "note?": "…", "items": [{"label": "…", "note?": "…", "size": 0.7}]}]},
        "rule": "3-7 layers of 1-6 items, each item may carry a one-line note",
        "validate": _v_layers, "render": _r_layers,
        "grammar": [
            "Horizontal stacked bands from top to bottom, each with a bold label at its left edge and its subtitle beneath the label; the tint deepens toward the bottom",
            "Items sit inside their band as labelled rounded boxes with the note beneath in smaller text; box size follows the size word",
            "NO arrows between layers — the relation is resting-upon; a thin vertical caption at the left edge when a spine is given",
        ],
    },
    "argument_tree": {
        "name": "Argument tree (claim, premises with notes, evidence, rebuttals)", "format": "argument_tree", "aspect": "4:3",
        "perspective": "how one master conclusion is held up, by what, and where it is attacked",
        "template": {"claim": {"label": "…", "note?": "…"}, "premises": [{"label": "…", "note?": "…", "evidence?": ["…"], "rebuttal?": "…", "strength": 0.8}], "verdict?": "…"},
        "rule": "one claim; 2-6 premises with notes, up to 4 evidence boxes and a rebuttal each; strength numbers 0-1",
        "validate": _v_argument, "render": _r_argument,
        "grammar": [
            "The CLAIM in a large box across the top with its note beneath the label; the premises in a row beneath it, each a box titled with the premise and its note in smaller text; box width follows the strength word",
            "Evidence boxes hang beneath their premise; rebuttals are rose-tinted boxes linked to the premise they attack",
            "Support lines point UPWARD from evidence to premise to claim; a verdict line runs along the bottom",
        ],
    },
}

FAMILY_ALIASES = {"gains_losses": "scorecard", "quadrant_scorecard": "scorecard", "framework": "framework_map", "conceptual_framework": "framework_map",
                  "river": "flow_map", "river_map": "flow_map", "flow": "flow_map", "commitments": "flow_map", "flow_of_commitments": "flow_map",
                  "stakeholder_map": "power_map", "stakeholder_power_map": "power_map", "power_interest": "power_map",
                  "timeline": "timeline_of_shifts", "shifts": "timeline_of_shifts", "table": "register", "matrix": "register", "risk_register": "register",
                  "argument_register": "register", "layers": "layer_stack", "assumptions": "layer_stack", "assumption_stack": "layer_stack",
                  "argument": "argument_tree", "tree": "argument_tree"}


def normalize_family(value: str) -> Optional[str]:
    key = re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")
    if key in PLATE_FAMILIES:
        return key
    return FAMILY_ALIASES.get(key)


def family_entry(family: str) -> dict[str, Any]:
    canon = normalize_family(family)
    if canon is None:
        raise KeyError(f"unknown plate family {family!r}")
    return PLATE_FAMILIES[canon]


def families_text() -> str:
    lines = ["PLATE FAMILIES (pick the one whose perspective the material supports; `canonical` must take exactly its shape — keys ending in ? are optional):"]
    for key, f in PLATE_FAMILIES.items():
        lines.append(f"- {key} — {f['name']}. For: {f['perspective']}. Rule: {f['rule']}. Aspect {f['aspect']}.\n"
                     f"  shape: {json.dumps(f['template'], ensure_ascii=False)}")
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════
# The wall (shape, density, lengths, leaks, grounding) and the declutter pass
# ══════════════════════════════════════════════════════════════════════════

def validate_canonical(family: str, canonical: Any) -> list[str]:
    """Shape errors (never raises). Empty list = the shape holds."""
    errors: list[str] = []
    canon = normalize_family(family)
    if canon is None:
        return [f"family {family!r} is not one of {list(PLATE_FAMILIES)}"]
    if not isinstance(canonical, dict) or not canonical:
        return ["canonical must be a non-empty object in the family's shape"]
    try:
        PLATE_FAMILIES[canon]["validate"](canonical, errors)
    except Exception as exc:  # a malformed shape is an error, not a crash
        errors.append(f"canonical does not fit the {canon} shape: {exc.__class__.__name__}: {exc}")
    if errors:
        return errors
    strings = rendered_strings(canonical)
    n = len(collect_plate_labels(canonical))
    if n < MIN_TEXT_ELEMENTS:
        errors.append(f"only {n} text elements: too thin for a plate (minimum {MIN_TEXT_ELEMENTS}); a plate is read instead of the memo — fill it")
    if n > MAX_TEXT_ELEMENTS:
        errors.append(f"{n} text elements is too many for one plate (maximum {MAX_TEXT_ELEMENTS}); condense")
    for kind, text in strings:
        words, chars = len(text.split()), len(text)
        cap_w, cap_c = {"label": (MAX_LABEL_WORDS, MAX_LABEL_CHARS), "note": (MAX_NOTE_WORDS, MAX_NOTE_CHARS), "cell": (MAX_CELL_WORDS, MAX_CELL_CHARS)}[kind]
        if words > cap_w or chars > cap_c:
            errors.append(f"{kind} too long ({words} words / {chars} chars, max {cap_w} words / {cap_c} chars): '{text[:70]}'")
        leaks = leak_scan(text)
        if leaks:
            errors.append(f"leaked rendering tokens in a {kind} (never print numbers, brackets, hex codes or instructions): {leaks[:3]} in '{text[:60]}'")
        if _ELLIPSIS_RE.search(text):
            errors.append(f"{kind} ends in an ellipsis — print whole strings, never truncations: '{text[:60]}'")
        if re.search(r"_[a-z]", text) and " " not in text:
            errors.append(f"{kind} looks like snake_case (rendered text must be prose): '{text}'")
    return errors


# Per-family list caps (the family rules); a longer list keeps its largest-size items and records the rest.
_LIST_CAPS: dict[str, dict[str, int]] = {
    "scorecard": {"items": 8, "quadrants": 4, "marks": 6, "links": 6},   # a 9-item panel rendered 7: eight is the ceiling at 4K
    "framework_map": {"nodes": 7, "regions": 3, "relations": 16, "bridges": 3, "side_boxes": 4, "items": 6},
    "flow_map": {"stations": 9, "feeds": 4, "drains": 3, "branches": 4, "steps": 4},
    "power_map": {"actors": 16, "relations": 12},
    "timeline_of_shifts": {"events": 16, "periods": 6, "shifts": 6, "tracks": 4},
    "register": {"rows": 12, "columns": 10, "legend": 12},
    "layer_stack": {"layers": 7, "items": 6},
    "argument_tree": {"premises": 6, "evidence": 4},
}


def declutter_plate(canonical: dict[str, Any], family: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """v1's declutter step, done in code: dedupe exact repeats, trim over-long notes/cells to the cap, cut
    lists to the family's caps (keeping the largest-size items) and drop the lowest-size items beyond the
    density ceiling. Records what it changed. Never invents."""
    report: dict[str, Any] = {"deduped": 0, "trimmed": 0, "dropped": []}
    seen: set[str] = set()
    caps = _LIST_CAPS.get(normalize_family(family) or "", {})

    def cap_list(key: Optional[str], items: list, path: str) -> list:
        cap = caps.get(key or "")
        if not cap or len(items) <= cap:
            return items
        if all(isinstance(x, dict) for x in items):
            order = sorted(range(len(items)), key=lambda i: -(float(items[i].get("size")) if items[i].get("size") is not None else 0.5))
            keep = sorted(order[:cap])
            for i in range(len(items)):
                if i not in keep:
                    report["dropped"].append({"path": f"{path}.{key}", "label": _s(items[i].get("label") or items[i].get("title"))})
            return [items[i] for i in keep]
        for x in items[cap:]:
            report["dropped"].append({"path": f"{path}.{key}", "label": _s(x)})
        return items[:cap]

    def trim(text: str, cap_w: int, cap_c: int) -> str:
        words = text.split()
        if len(words) > cap_w or len(text) > cap_c:
            report["trimmed"] += 1
            cut = " ".join(words[:cap_w])
            while len(cut) > cap_c and " " in cut:
                cut = cut.rsplit(" ", 1)[0]
            return cut
        return text

    def walk(obj: Any, key: Optional[str]) -> Any:
        if isinstance(obj, dict):
            out = {}
            for k, v in obj.items():
                if k in _NOTE_KEYS and isinstance(v, str):
                    out[k] = trim(v.strip(), MAX_NOTE_WORDS, MAX_NOTE_CHARS)
                else:
                    out[k] = walk(v, k)
            return out
        if isinstance(obj, list):
            if key == "cells":
                return [trim(v.strip(), MAX_CELL_WORDS, MAX_CELL_CHARS) if isinstance(v, str) else v for v in obj]
            obj = cap_list(key, obj, "")
            kept = []
            for v in obj:
                if isinstance(v, str) and key in ("items", "feeds", "drains", "evidence", "steps"):
                    k = v.strip().lower()
                    if k in seen:
                        report["deduped"] += 1
                        continue
                    seen.add(k)
                    kept.append(v.strip())
                elif isinstance(v, dict) and key in ("items", "nodes", "actors", "events", "stations"):
                    lab = _s(v.get("label")).lower()
                    if lab and lab in seen:
                        report["deduped"] += 1
                        continue
                    if lab:
                        seen.add(lab)
                    kept.append(walk(v, key))
                else:
                    kept.append(walk(v, key))
            return kept
        return obj

    out = walk(canonical, None)
    # dangling edges (an endpoint that names no node/quadrant/actor/event/station) are dropped, not re-asked
    names = {_s(x).lower() for x in collect_plate_labels(out)}
    for key in ("relations", "links", "shifts", "bridges"):
        edges = out.get(key)
        if isinstance(edges, list):
            kept_edges = []
            for ed in edges:
                if isinstance(ed, dict) and (_s(ed.get("from")).lower() not in names or _s(ed.get("to")).lower() not in names):
                    report["dropped"].append({"path": f".{key}", "label": f"{_s(ed.get('from'))} → {_s(ed.get('to'))} ({_s(ed.get('label'))})", "why": "dangling endpoint"})
                    continue
                kept_edges.append(ed)
            out[key] = kept_edges
    # density ceiling: drop the smallest-size items from the longest lists until under the cap
    def lists_of_items(obj: Any, path: str = "") -> list[tuple[str, list]]:
        found = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, list) and v and all(isinstance(x, dict) for x in v) and k in ("items", "nodes", "actors", "events", "rows"):
                    found.append((f"{path}.{k}", v))
                found.extend(lists_of_items(v, f"{path}.{k}"))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                found.extend(lists_of_items(v, f"{path}[{i}]"))
        return found

    guard = 0
    while len(collect_plate_labels(out)) > MAX_TEXT_ELEMENTS and guard < MAX_TEXT_ELEMENTS * 4:
        guard += 1
        candidates = [(p, lst) for p, lst in lists_of_items(out) if len(lst) > 2]
        if not candidates:
            break
        path, lst = max(candidates, key=lambda pl: len(pl[1]))
        victim = min(range(len(lst)), key=lambda i: float(lst[i].get("size")) if lst[i].get("size") is not None else 0.5)
        report["dropped"].append({"path": path, "label": _s(lst[victim].get("label"))})
        del lst[victim]
    return out, report


_STOP = {"the", "and", "for", "with", "from", "into", "that", "this", "than", "over", "under", "your", "their", "have", "been", "were",
         "what", "when", "where", "which", "while", "after", "before", "between", "about", "each", "every", "more", "most", "less",
         "very", "only", "also", "then", "them", "they", "will", "would", "could", "should", "does", "onto", "upon", "toward", "towards",
         "versus", "gains", "losses", "gain", "loss", "high", "low", "locked", "into"}


def label_in_material(label: str, material_norm: str) -> bool:
    """Verbatim, or every significant word (≥4 letters, not a stopword) present — paraphrase of the material's
    vocabulary is allowed, invented names and terms are not (the figures wall's rule)."""
    n = normalize(label)
    if len(n) >= 4 and n in material_norm:
        return True
    tokens = [t for t in re.findall(r"[a-z0-9][a-z0-9&'.+-]*", n) if len(t) >= 4 and t not in _STOP]
    numbers = re.findall(r"\d[\d,.]*", n)
    if not tokens and not numbers:
        return False
    return all(t in material_norm for t in tokens) and all(x in material_norm for x in numbers)


def validate_plate_spec(spec: PlateSpec, material_norm: str = "") -> tuple[list[str], dict[str, Any]]:
    """The wall: family + shape + density + lengths + leaks + title/narrative + grounding. (errors, grounding)."""
    errors: list[str] = []
    fam = normalize_family(spec.family)
    if fam is None:
        errors.append(f"family {spec.family!r} must be one of: {', '.join(PLATE_FAMILIES)}")
    else:
        spec.family = fam
        spec.visual_format = normalize_format_key(spec.visual_format) or PLATE_FAMILIES[fam]["format"]
        if not spec.aspect or spec.aspect not in ASPECTS:
            spec.aspect = PLATE_FAMILIES[fam]["aspect"]
    if not spec.title:
        errors.append("title is required")
    elif len(spec.title) > MAX_TITLE_CHARS:
        errors.append(f"title is {len(spec.title)} chars; max {MAX_TITLE_CHARS}")
    if leak_scan(spec.title):
        errors.append(f"title carries leaked tokens: {leak_scan(spec.title)}")
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", (spec.narrative or "").strip()) if s]
    if len(sentences) < 2:
        errors.append("narrative must be 3-5 sentences the reader needs to read the plate")
    elif len(sentences) > 7:
        errors.append(f"narrative is {len(sentences)} sentences; keep it to 3-5")
    if not (1 <= int(spec.abstraction_level or 0) <= 5):
        errors.append("abstraction_level must be 1..5")
    if fam and isinstance(spec.canonical, dict) and spec.canonical:
        spec.canonical, report = declutter_plate(spec.canonical, fam)
        spec.__dict__["_declutter"] = report
    if fam:
        errors.extend(validate_canonical(fam, spec.canonical))
    labels = collect_plate_labels(spec.canonical) if isinstance(spec.canonical, dict) else []
    content = content_labels(spec.canonical) if isinstance(spec.canonical, dict) else []
    grounding: dict[str, Any] = {"checked": bool(material_norm), "labels": len(labels), "content_labels": len(content), "grounded": 0,
                                 "ungrounded": [], "anchors": len(spec.anchors), "anchors_verified": 0}
    if material_norm and not errors:
        verified: set[str] = set()
        for a in spec.anchors:
            q = normalize(a.quote)
            a.verified = bool(q) and len(q) >= 6 and q in material_norm
            if a.verified:
                grounding["anchors_verified"] += 1
                verified.add(normalize(a.label))
        for lab in content:
            if normalize(lab) in verified or label_in_material(lab, material_norm):
                grounding["grounded"] += 1
            else:
                grounding["ungrounded"].append(lab)
        frac = grounding["grounded"] / len(content) if content else 1.0
        grounding["fraction"] = round(frac, 2)
        if content and frac < MIN_GROUNDED_FRACTION:
            errors.append(f"ungrounded: only {grounding['grounded']}/{len(content)} labels use the material's own words "
                          f"(names, terms, cases, dates exactly as written). Ungrounded: " + "; ".join(grounding["ungrounded"][:10]))
    spec.size_guides = extract_size_guides(spec.canonical) if isinstance(spec.canonical, dict) else {}
    return errors, grounding


# ══════════════════════════════════════════════════════════════════════════
# Material and the planner (v1's UnifiedStrategist + content formatter, one grounded pass)
# ══════════════════════════════════════════════════════════════════════════

def _tables_text(job: DossierJob) -> str:
    parts = []
    for t in job.tables:
        parts.append(f"### Table `{t.key}` — {t.caption}\n| " + " | ".join(t.columns) + " |")
        for r in t.rows:
            parts.append("| " + " | ".join((c.value or "").replace("|", "/") for c in r.cells) + " |")
        if t.note:
            parts.append(f"note: {t.note}")
    return "\n".join(parts) if parts else "(no tables)"


def _sections_text(job: DossierJob, max_chars: int = 30_000) -> str:
    s = job.sections
    if s is None:
        return "(not composed yet)"
    parts = [f"# {s.title}", s.subtitle, "", "## Executive summary", *s.executive_summary]
    for sec in s.sections:
        parts.append(f"\n## {sec.number}. {sec.heading}")
        parts.extend(re.sub(r"\{\{\s*\d+\s*\}\}", "", p) for p in sec.paragraphs)
    if s.conclusion:
        parts.append("\n## What this means")
        parts.extend(s.conclusion)
    text = "\n".join(parts)
    return text if len(text) <= max_chars else text[:max_chars] + "\n[… truncated …]"


def _spine_text(job: DossierJob) -> str:
    spine = getattr(job, "spine", None)
    if not spine:
        return ""
    try:
        data = spine.model_dump() if hasattr(spine, "model_dump") else spine
        text = json.dumps(data, ensure_ascii=False, indent=1)
        return text[:20_000]
    except Exception:
        return ""


def plate_material(job: DossierJob, max_chars: int = MATERIAL_MAX_CHARS) -> str:
    """Everything a plate may stand on: the chosen telling, the composed dossier, the tables, the analysis prose, the profiles, the spine."""
    from src.dossier.plan import chosen_option

    opt = chosen_option(job)
    telling = f"{opt.title}\n{opt.telling}" if opt else (job.options.intent or "")
    tables = _tables_text(job)
    sections = _sections_text(job)
    profiles = compact_profiles(job.profiles)[:12_000]
    spine = _spine_text(job)
    budget = max(30_000, max_chars - len(tables) - len(sections) - len(profiles) - len(telling) - len(spine))
    analysis = analysis_prose(job, max_chars_per_phase=budget // max(1, len(job.analysis) or 1))[:budget]
    parts = [f"ANGLE (the chosen telling):\n{telling}", f"THE COMPOSED DOSSIER (the report the plate replaces):\n{sections}",
             f"TABLES (verified rows):\n{tables}", f"ANALYSIS PROSE:\n{analysis}", f"PROFILES:\n{profiles}"]
    if spine:
        parts.insert(2, f"SECTION SPINE:\n{spine}")
    return "\n\n".join(parts)


PLATE_ITEM_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["key", "family", "perspective", "title", "abstraction_level", "claimed_territory", "excludes",
                 "why_this_perspective", "narrative", "canonical"],
    "properties": {
        "key": {"type": "string", "description": "snake_case identifier"},
        "family": {"type": "string", "description": "one of the plate families"},
        "perspective": {"type": "string", "description": "the perspective's name in reader terms, <= 8 words"},
        "title": {"type": "string", "description": f"<= {MAX_TITLE_CHARS} characters; rendered at the top of the plate"},
        "visual_format": {"type": "string", "description": "leave empty; the family decides"},
        "abstraction_level": {"type": "integer", "description": "1 helicopter, 2 framework, 3 analytical, 4 evidential, 5 granular"},
        "claimed_territory": {"type": "string", "description": "what this plate uniquely covers"},
        "excludes": {"type": "array", "items": {"type": "string"}, "description": "what the OTHER plates cover and this one leaves out"},
        "why_this_perspective": {"type": "string", "description": "one or two sentences: why this perspective deserves a whole plate for this material"},
        "narrative": {"type": "string", "description": "3-5 sentences the reader needs to read the plate; printed beside it, never in it"},
        "canonical": {"type": "object", "additionalProperties": True,
                      "description": "the plate's ENTIRE content in the family's JSON shape; sizes as NUMBERS 0-1; every string is printed"},
        "aspect": {"type": "string", "description": "16:9 | 4:3 | 3:4 | 1:1 (the family's default when omitted)"},
        "anchors": {"type": "array", "maxItems": 20,
                    "items": {"type": "object", "additionalProperties": False, "required": ["label", "quote", "source"],
                              "properties": {"label": {"type": "string"}, "quote": {"type": "string", "description": "verbatim 20-200 chars from the material"},
                                             "source": {"type": "string", "description": "analysis | table | profile | dossier"}}}},
    },
}
PLATES_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["plates"],
                 "properties": {"plates": {"type": "array", "minItems": 1, "maxItems": MAX_PLATES + 1, "items": PLATE_ITEM_SCHEMA}}}

SYSTEM = """You are the plates desk of The Analyst. A PLATE is one dense 4K image that IS the analysis: an executive reads
it instead of the memo. It is a LABELLED ANALYTICAL DIAGRAM of enormous density — a scorecard whose panels spell out
every gain and loss; a framework map whose nodes carry one-line definitions and whose arrows are labelled with the
relation; a flow map whose stations, tributaries and locked-in branches are all named; a register whose rows are
scored across typed columns — never an illustration, never a scene, never a metaphor.
PREFER the diagrammatic families (framework map, flow map, power map, layer stack, argument tree, timeline of shifts,
scorecard): the dossier's tables already carry the tabular reading, so a plate earns its place by showing STRUCTURE —
nodes, relations, currents, levels — not another grid. Use the register only when the requester asks for one.

You choose the PERSPECTIVES that each deserve a whole plate for this material, and for each you write the plate's
COMPLETE content model in its family's shape. The rules of the desk:
1. Each plate takes a DIFFERENT family and a DIFFERENT abstraction level (1 helicopter: systemic patterns, paradigm
   competition; 2 framework: theoretical structures, categorical relationships; 3 analytical: mechanisms, causal chains,
   detailed comparisons; 4 evidential: cases, examples, instances; 5 granular: quotes, data points). Each plate claims
   a territory and lists what it leaves to the others.
2. DENSITY. A plate carries 30-90 text elements. Fill every panel, region, station and row from the material; a thin
   plate is rejected. Respect the counts in the family's rule exactly (a longer list is cut to its largest items; a
   shorter one is rejected). Prefer the concrete — named actors, cases, terms, dates, amounts, exactly as the material writes
   them — over abstractions. Nothing invented, nothing vague.
3. Labels are statements of at most 24 words (panel items, station claims and premises are full clauses; node titles,
   headers and badges are short); definitions and notes are one line (at most 24 words) and paraphrase what the
   material says about the item. Register cells at most 16 words. Titles at most 120 characters.
4. Sizes, positions and strengths are NUMBERS between 0 and 1 in the `size`/`x`/`y`/`strength` keys — never inside a
   label. NEVER put numbers, scores, brackets, colour codes or instructions inside any printed string; never end a
   string with an ellipsis; never write snake_case in printed text.
5. The narrative (3-5 sentences) tells the reader how to read the plate and what it shows; it is printed beside the
   plate, never inside it.
6. The plate must be readable on its own: a reader who has NOT read the memo must get the analysis from the plate."""


def _snake(value: str, fallback: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")
    return key or fallback


def _coerce_spec(raw: dict[str, Any], index: int) -> PlateSpec:
    canonical = raw.get("canonical")
    if isinstance(canonical, str):
        try:
            canonical = json.loads(canonical)
        except Exception:
            canonical = {}
    anchors = []
    for a in raw.get("anchors", []) or []:
        if isinstance(a, dict) and _s(a.get("label")):
            anchors.append(FigureAnchor(label=_s(a.get("label")), quote=_s(a.get("quote")), source=_s(a.get("source")).lower()))
    try:
        level = int(raw.get("abstraction_level") or 3)
    except (TypeError, ValueError):
        level = 3
    excludes = raw.get("excludes") or []
    if isinstance(excludes, str):
        excludes = [excludes]
    return PlateSpec(
        key=_snake(str(raw.get("key", "")), f"plate_{index}"),
        family=_s(raw.get("family")), visual_format=_s(raw.get("visual_format")),
        perspective=_s(raw.get("perspective")), title=_s(raw.get("title")),
        canonical=canonical if isinstance(canonical, dict) else {},
        narrative=_s(raw.get("narrative")), why_this_perspective=_s(raw.get("why_this_perspective")),
        claimed_territory=_s(raw.get("claimed_territory")), excludes=[str(x) for x in excludes],
        abstraction_level=level, aspect=_s(raw.get("aspect")), anchors=anchors,
    )


def _plan_user(job: DossierJob, n: int, material: str, perspectives: Optional[list[str]] = None,
               replace: Optional[list[tuple[PlateSpec, list[str]]]] = None, keep: Optional[list[PlateSpec]] = None) -> str:
    engines = ", ".join(f"{p.engine_key}@{p.depth}" for p in job.plan.phases) if job.plan else "(none)"
    head = (f"Plan exactly {n} plate(s), each a whole perspective in a DIFFERENT family at a DIFFERENT abstraction level.\n"
            f"AUDIENCE: {job.options.audience} — {AUDIENCE_REGISTER.get(job.options.audience, '')}\n"
            f"ENGINES that produced the analysis: {engines}\n")
    if perspectives:
        head += "The requester asked for these perspectives, in this order — honour them, choosing the family that fits each:\n" + \
                "\n".join(f"  {i}. {p}" for i, p in enumerate(perspectives, 1)) + "\n"
    if replace:
        kept = "; ".join(f"`{s.key}` ({s.family}, level {s.abstraction_level})" for s in (keep or [])) or "(none)"
        fixes = "\n".join(f"- `{s.key}` ({s.family}): " + " | ".join(errs[:8]) for s, errs in replace)
        head += (f"\nYOUR PREVIOUS ANSWER WAS PARTLY REJECTED BY THE WALL. Plates kept as they are: {kept}.\n"
                 f"Return ONLY {len(replace)} replacement plate(s) for the rejected ones, fixing these errors "
                 f"(or choose a different family/perspective that the material can fill densely):\n{fixes}\n")
    return head + f"\n{families_text()}\n\nMATERIAL (the only ground for every printed string):\n{material}"


def choose_style_school(job: DossierJob, format_key: str) -> str:
    try:
        from src.dossier.figures import choose_style_school as _choose

        return _choose(job, format_key)
    except Exception as exc:
        logger.info(f"style affinities unavailable ({exc}); default school")
        return "explanatory_narrative"


def plan_plates(job: DossierJob, n: int = 2, audience: Optional[str] = None, perspectives: Optional[list[str]] = None) -> list[PlateSpec]:
    """N PlateSpecs through the wall; rejected ones are re-asked once. May return fewer than N."""
    from src.dossier.llm import call_json

    if audience and audience != job.options.audience:
        job = job.model_copy(deep=True)
        job.options.audience = audience
    if perspectives:
        n = max(1, min(MAX_PLATES, len(perspectives)))
    n = max(1, min(MAX_PLATES, int(n or 1)))
    material = plate_material(job)
    material_norm = normalize(material)
    raw, _ = call_json(job.id, STEP, label=f"plate plan ({n} perspectives)", system=SYSTEM,
                       user=_plan_user(job, n, material, perspectives), tool_name="record_plate_plan", schema=PLATES_SCHEMA,
                       model_cls=None, max_tokens=24000)
    accepted: list[PlateSpec] = []
    rejected: list[tuple[PlateSpec, list[str]]] = []
    used_families: set[str] = set()
    used_levels: set[int] = set()

    def admit(items: list[dict[str, Any]]) -> None:
        for i, item in enumerate(items, start=len(accepted) + len(rejected) + 1):
            try:
                spec = _coerce_spec(item, i)
            except Exception as exc:
                logger.warning(f"plate spec unreadable: {exc}")
                continue
            errors, grounding = validate_plate_spec(spec, material_norm)
            if not errors and spec.family in used_families:
                errors.append(f"family {spec.family} is already used by another plate; choose a different family")
            # The register is a table-plate. When the dossier already carries anchored tables, a plate must add a
            # DIFFERENT reading — a map, a flow, a scorecard, a stack, a tree — unless the requester asked for a register.
            if not errors and spec.family == "register" and len(getattr(job, "tables", None) or []) >= 2 \
                    and not any("register" in (p or "").lower() for p in (perspectives or [])):
                errors.append("the dossier already has anchored tables; a register plate would repeat them — choose a diagrammatic family "
                              "(framework_map, flow_map, power_map, layer_stack, argument_tree, timeline_of_shifts, scorecard)")
            if not errors and n > 1 and spec.abstraction_level in used_levels:
                errors.append(f"abstraction level {spec.abstraction_level} is already taken by another plate; choose a different level")
            spec.__dict__["_grounding"] = grounding
            if errors:
                rejected.append((spec, errors))
                events.emit(job.id, "note", phase=STEP, detail=f"plate wall rejected `{spec.key}` ({spec.family}): " + " | ".join(errors[:3]),
                            payload_json={"kind": "plate_rejected", "key": spec.key, "errors": errors, "grounding": grounding, "spec": spec.model_dump()})
            else:
                spec.style_school = choose_style_school(job, spec.visual_format)
                used_families.add(spec.family)
                used_levels.add(spec.abstraction_level)
                accepted.append(spec)
                events.emit(job.id, "note", phase=STEP,
                            detail=f"plate wall passed `{spec.key}`: {spec.perspective} → {spec.family}/{spec.visual_format}, level {spec.abstraction_level}, "
                                   f"{grounding.get('labels', 0)} text elements, {grounding.get('grounded', 0)}/{grounding.get('content_labels', 0)} labels grounded; style {spec.style_school}",
                            payload_json={"kind": "plate_accepted", "key": spec.key, "grounding": grounding})

    admit((raw or {}).get("plates", [])[: n + 1])
    if rejected and len(accepted) < n:
        need = min(n - len(accepted), len(rejected))
        raw2, _ = call_json(job.id, STEP, label=f"plate plan repair ({need})", system=SYSTEM,
                            user=_plan_user(job, need, material, perspectives, replace=rejected[:need], keep=accepted),
                            tool_name="record_plate_plan", schema=PLATES_SCHEMA, model_cls=None, max_tokens=24000)
        rejected = []
        admit((raw2 or {}).get("plates", [])[:need])
        for spec, errors in rejected:
            events.emit(job.id, "note", phase=STEP, detail=f"plate_skipped `{spec.key}`: still rejected after repair — " + " | ".join(errors[:2]),
                        payload_json={"kind": "plate_skipped", "key": spec.key, "reason": errors, "spec": spec.model_dump()})
    plan_plates.last_rejected = [(s.model_dump(), e) for s, e in rejected]   # for the CLI's rejected.json
    return accepted[:n]


# ══════════════════════════════════════════════════════════════════════════
# Prompt assembly (v1's order) — scene prose, format enforcement, grammar, style sandwich
# ══════════════════════════════════════════════════════════════════════════

# v1 QUALITY_PREAMBLE (gemini_image.py:42-113), the lines that carry weight, verbatim where they matter.
PLATE_PREAMBLE = [
    "TEXT ACCURACY IS NON-NEGOTIABLE: ONLY use text EXACTLY as provided in the CONTENT below — character for character. "
    "DO NOT invent, hallucinate, or approximate ANY text labels, names, or terms. DO NOT 'improve' or 'clarify' text.",
    "NEVER show any bracketed annotations, instructions, colour codes or decimal numbers anywhere in the image. "
    "Size words, placement words and colour words in the CONTENT are instructions for HOW to draw — never printed.",
    "MANDATORY TITLE: the plate has one prominent title at the top, exactly the TITLE given, larger than any other text.",
    "NO SMALL TEXT: every label is legible at 4K without zooming (labels ≥ 1.4% of the image height, notes ≥ 1.0%, the title ≥ 3%). "
    "Never shrink text to fit — wrap it, or use the space the plate has.",
    "FORMAT COMPLIANCE (AUTO-FAIL IF VIOLATED): the MANDATORY FORMAT and the PLATE LAYOUT GRAMMAR below are hard requirements, not suggestions.",
    "QUALITY STANDARD: Edward Tufte principles — maximize data-ink, clear hierarchy, elegant density. AUDIENCE: senior executives who will immediately notice text errors.",
]

PLATE_TEXT_RULES = [
    "Every label at least 1.4% of the image height (≈ 40 px on a 3072 px tall plate); notes ≥ 1.0%; the title ≥ 3%; nothing needs zooming",
    "High contrast with its background (≥ 4.5:1); dark on light OR light on dark; never on a busy texture",
    "Each string on a clean area, never overlapping a line, an arrow, a band or another string",
    "Only the strings in the CONTENT block and the TITLE — invent no other words, names, dates or numbers",
    "Spell every string exactly as written; never abbreviate, never paraphrase, never garble; print each string WHOLE — no '…' cut-offs",
    "No underscores or snake_case in visible text; Title Case for labels, sentence case for definitions and notes",
    "Never print raw decimals, weights, scores, coordinates, sizes or colour codes (0.85, 'weight: 3', '#1e40af', 'size guide') — encode them visually",
    "No logos, bylines, source lines, credits, watermarks, page numbers, dates or publication marks",
    "No subtitle, no callout boxes, no 'insight' / 'conclusion' / 'key finding' notes, no explanatory sentences of your own: the ONLY text is the title and the CONTENT strings",
    "Never print a note about shortening, truncation, or what was omitted",
]

PLATE_CLOSER = ("A single dense diagram on a clean background that a reader studies instead of the memo — "
                "no scenery, no metaphors, no photographs, no 3D objects, no people.")


def plate_content_lines(spec: PlateSpec) -> list[str]:
    """The canonical spelled out as layout lines for the image model (assumes the shape holds)."""
    fam = family_entry(spec.family)
    try:
        return fam["render"](spec.canonical)
    except Exception:
        return ["  " + json.dumps(spec.canonical, ensure_ascii=False)]


def build_plate_prompt(spec: PlateSpec, *, revision_notes: Optional[list[str]] = None) -> str:
    """Order (v1's): preamble → MANDATORY FORMAT block (must_have / must_not / GLOBAL_PROHIBITIONS / legibility) →
    PLATE LAYOUT GRAMMAR → style override → CONTENT → LABEL MANIFEST → TITLE → TEXT RULES → FRAME → DENSITY →
    REVISION NOTES → closer + FINAL REMINDER → style closing."""
    from src.images.figure_prompts import build_style_closing, build_style_override, style_for_school

    fam_key = normalize_family(spec.family)
    if fam_key is None:
        raise ValueError(f"unknown plate family {spec.family!r}")
    fam = PLATE_FAMILIES[fam_key]
    fmt = normalize_format_key(spec.visual_format) or fam["format"]
    entry = format_entry(fmt)
    title = (spec.title or "").strip()
    if not title:
        raise ValueError("spec.title is required (it is rendered)")
    errors = validate_canonical(fam_key, spec.canonical)
    if errors:
        raise ValueError("spec.canonical does not fit the family: " + "; ".join(errors[:5]))
    labels = collect_plate_labels(spec.canonical)
    aspect = spec.aspect if spec.aspect in ASPECTS else fam["aspect"]
    style = style_for_school(spec.style_school or None)
    lines = plate_content_lines(spec)
    n_lines = len(lines)

    parts: list[str] = [
        f"Create a PLATE — a single, dense, publication-grade 4K LABELLED ANALYTICAL DIAGRAM that IS the analysis. "
        f"Its family is {fam['name'].upper()}; its title is: {title}",
        "It is a data visualization of the CONTENT below, the kind a consulting graphics desk publishes as a full-page plate: "
        "flat shapes, bands, boxes, arrows and text. It is NOT a picture, a scene, an object or a metaphor. "
        "A reader who has not read the report must get the whole analysis from this one image.",
        "",
        "READ FIRST:",
        *[f"  ★ {r}" for r in PLATE_PREAMBLE],
        "",
        enforcement_block(fmt).strip(),
        "",
        f"PLATE LAYOUT GRAMMAR ({fam['name']}) — the mandatory structure, on top of the format rules above:",
        *[f"  ▸ {g}" for g in fam["grammar"]],
        "",
    ]
    if style:
        parts.append(build_style_override(style).rstrip())
        parts.append(f"STYLE SCHOOL: {spec.style_school} (the palette/typography above). Apply it to a DIAGRAM: colours on panels, "
                     "bands, boxes, badges, arrows and labels — never as illustration. Semantic colours named in the grammar "
                     "(green gains, red losses, navy header, badge families) take precedence over the palette for those elements.")
        parts.append("")
    parts.append(f"CONTENT TO RENDER — this is the ENTIRE content of the plate ({n_lines} layout lines, {len(labels)} distinct strings). "
                 "Render every string exactly as written; the phrases after a dash or a comma that describe placement, size, tone or role "
                 "(draw in large type, drawn as a thick band, a badge column, on track …) are drawing instructions and are NOT printed:")
    parts.extend(lines)
    parts.append("")
    parts.append(f"LABEL MANIFEST — each of these {len(labels)} strings must appear exactly once, legibly, spelled as written:")
    parts.extend(f"  • {lab}" for lab in labels)
    parts.append("")
    parts.append(f"TITLE (render exactly this text once, at the top, larger than any other text, WITHOUT quotation marks): {title}")
    parts.append("Under the title: nothing. No subtitle, no byline, no source line, no logo, no watermark, no page furniture.")
    if spec.why_this_perspective:
        parts.append(f"CONTEXT (do NOT render): this plate shows — {spec.why_this_perspective.strip()}")
    parts.append("")
    parts.append("TEXT RULES:")
    parts.extend(f"  ✓ {r}" for r in PLATE_TEXT_RULES)
    parts.append("")
    parts.append(f"FRAME: compose for a {aspect} aspect ratio at 4K; the plate fills the frame with even margins; nothing is cropped at the edges.")
    parts.append(f"DENSITY: this is a plate, not a slide. All {len(labels)} strings are rendered; balance the canvas so that no region is empty "
                 "and no region is crowded; where the content is long, the plate is dense and orderly, like a printed reference sheet.")
    notes = [str(n).strip() for n in (revision_notes or []) if str(n).strip()]
    if notes:
        parts.append("")
        parts.append("REVISION NOTES from the reviewer of the previous attempt — fix ALL of these:")
        parts.extend(f"  ! {n}" for n in notes)
    parts.append("")
    parts.append(PLATE_CLOSER)
    parts.append(f"FINAL REMINDER: LAYOUT IS MANDATORY. You MUST use the {entry['name'].upper()} layout under the {fam['name'].upper()} grammar "
                 "as specified above. DO NOT substitute a generic network diagram, a freestyle chart, a slide or an illustration. "
                 "DO NOT print any bracketed token, colour code or number that is not a content string.")
    if style:
        parts.append(build_style_closing(style).rstrip())
    return "\n".join(parts).strip() + "\n"


def prompt_content_section(prompt: str) -> str:
    """The part of a prompt the image model copies text from (CONTENT … TITLE line) — what the leak test scans."""
    start = prompt.find("CONTENT TO RENDER")
    end = prompt.find("Under the title:")
    return prompt[start:end] if start >= 0 and end > start else prompt


# ══════════════════════════════════════════════════════════════════════════
# The vision check — overview + four tiles, the label manifest, the leak scan
# ══════════════════════════════════════════════════════════════════════════

PLATE_CHECK_PROMPT = """You are reviewing a rendered PLATE for an analytical dossier — one dense 4K diagram meant to be read instead of the
memo. Image 1 is the whole plate; images 2-5 are its top-left, top-right, bottom-left and bottom-right quarters at
higher resolution (read the small text there).

It was supposed to be a {format_name} under the "{family_name}" grammar, titled “{title}”.

FORMAT CHECK — the image SHOULD show: {pass_if}; and follow this grammar: {grammar}.
It should NOT show: {fail_if}.
It must be a FLAT LABELLED DIAGRAM (shapes, bands, boxes, arrows, text), not an illustration: no scenery, no physical
objects, no people, no metaphors, no photographs, no 3D. If it is a picture of something instead of a diagram of the
content, format_ok is false.

REQUIRED STRINGS — each must appear in the image, legible, spelled as written:
{labels}

LEAK CHECK — these must NOT appear anywhere: square-bracket tokens like "[SIZE_GUIDE: 0.9]", curly-brace tokens,
colour codes like "#1e40af", bare decimals like "0.85", the words "size guide", "weight:", "score:", "truncated",
"truncate to N chars", "placeholder", "lorem", or any sentence that reads as an instruction to the illustrator.

Inspect all five images carefully. Read every piece of text. Then answer in this exact JSON and nothing else:
{{
  "format_ok": true/false,
  "detected_format": "what the image actually is, in a few words",
  "title_found": true/false,
  "labels_found": ["required strings that appear, spelled correctly and legible"],
  "labels_missing": ["required strings that do not appear at all"],
  "misspelled": [{{"expected": "required string", "seen": "what is printed instead"}}],
  "illegible": ["required strings present but too small, cut off, overlapped or low-contrast"],
  "prohibited_elements": ["scenery, objects, metaphors, photos, 3D, dramatic effects, logos, bylines, source lines — if any"],
  "leaked_tokens": ["any leaked instruction tokens, colour codes, decimals or truncation notes printed in the image"],
  "extra_text": ["words in the image that are NOT required strings, the title, legend entries, axis ticks, glyphs or +/- marks (i.e. invented content)"],
  "density": "sparse | adequate | dense — sparse means large empty areas or fewer than half the required strings",
  "legible_at_4k": true/false,
  "confidence": "high" | "medium" | "low",
  "suggestion": "one concrete change to the prompt that would fix the worst problem, or null"
}}"""


def _norm_label(s: str) -> str:
    return " ".join(str(s or "").lower().replace("’", "'").split())


def _tiles(image_bytes: bytes, max_edge: int = 1568) -> list[tuple[bytes, str]]:
    """Overview + four quarter tiles as JPEG ≤ max_edge (the vision model resizes above that anyway)."""
    from PIL import Image  # type: ignore

    out: list[tuple[bytes, str]] = []
    with Image.open(BytesIO(image_bytes)) as im:
        im = im.convert("RGB")
        w, h = im.size
        boxes = [(0, 0, w, h), (0, 0, w // 2, h // 2), (w // 2, 0, w, h // 2), (0, h // 2, w // 2, h), (w // 2, h // 2, w, h)]
        for box in boxes:
            tile = im.crop(box)
            tw, th = tile.size
            scale = min(1.0, max_edge / max(tw, th))
            if scale < 1.0:
                tile = tile.resize((max(1, int(tw * scale)), max(1, int(th * scale))))
            buf = BytesIO()
            tile.save(buf, format="JPEG", quality=86)
            out.append((buf.getvalue(), "image/jpeg"))
    return out


def invented_sentences(verdict: dict[str, Any]) -> list[str]:
    return [str(t) for t in (verdict.get("extra_text") or []) if len(str(t).split()) >= 4]


def plate_verdict_ok(verdict: dict[str, Any], n_labels: int) -> bool:
    """Right format, nothing prohibited, nothing leaked, not sparse, no invented sentences, and at most
    max(2, 20%) of the strings missing/misspelled/illegible."""
    if not verdict.get("format_ok"):
        return False
    if verdict.get("prohibited_elements") or verdict.get("leaked_tokens"):
        return False
    if invented_sentences(verdict):
        return False
    if str(verdict.get("density") or "").lower().startswith("sparse"):
        return False
    bad = len(verdict.get("labels_missing") or []) + len(verdict.get("misspelled") or []) + len(verdict.get("illegible") or [])
    return bad <= max(2, n_labels // 5)


def check_plate(image_bytes: bytes, spec: PlateSpec, *, model: str = CHECK_MODEL, api_key: Optional[str] = None,
                max_tokens: int = 4000) -> dict[str, Any]:
    """Claude-vision verdict on a rendered plate against its spec. Never raises; without a key → checked=False."""
    fam_key = normalize_family(spec.family) or ""
    fam = PLATE_FAMILIES.get(fam_key, {})
    fmt = normalize_format_key(spec.visual_format) or fam.get("format") or ""
    labels = collect_plate_labels(spec.canonical)
    base: dict[str, Any] = {
        "ok": None, "format_ok": None, "detected_format": None, "title_found": None, "labels_found": [], "labels_missing": [],
        "misspelled": [], "illegible": [], "prohibited_elements": [], "leaked_tokens": [], "extra_text": [], "density": None,
        "legible_at_4k": None, "suggestion": None, "confidence": "low", "checked": False, "model": model, "usage": None,
        "n_labels": len(labels), "issues": [],
    }
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        base["issues"] = ["check skipped: no ANTHROPIC_API_KEY"]
        return base
    if not image_bytes:
        base.update({"ok": False, "issues": ["empty image"]})
        return base
    try:
        import anthropic
        from src.images.compliance import _extract_json

        entry = format_entry(fmt) if fmt else {"name": "diagram"}
        pass_if, fail_if = check_criteria(fmt) if fmt else ([], [])
        prompt = PLATE_CHECK_PROMPT.format(
            format_name=entry["name"], family_name=fam.get("name", spec.family), title=spec.title,
            pass_if="; ".join(pass_if) or "the named format", fail_if="; ".join(fail_if) or "anything pictorial",
            grammar=" / ".join(fam.get("grammar", [])[:4]),
            labels="\n".join(f"  {i}. {lab}" for i, lab in enumerate(labels, 1)) or "  (none)",
        )
        content: list[dict[str, Any]] = []
        for data, media in _tiles(image_bytes):
            content.append({"type": "image", "source": {"type": "base64", "media_type": media, "data": base64.b64encode(data).decode("ascii")}})
        content.append({"type": "text", "text": prompt})
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(model=model, max_tokens=max_tokens, messages=[{"role": "user", "content": content}])
        raw = "".join(getattr(b, "text", "") for b in resp.content)
        usage = {"input_tokens": getattr(resp.usage, "input_tokens", None), "output_tokens": getattr(resp.usage, "output_tokens", None)}
        try:
            v = _extract_json(raw)
        except Exception:
            base.update({"issues": ["could not parse plate verdict"], "checked": True, "raw": raw[:500], "usage": usage})
            return base

        def _strs(k: str) -> list[str]:
            return [str(x) for x in (v.get(k) or []) if str(x).strip()]

        found_norm = {_norm_label(x) for x in _strs("labels_found")}
        listed_missing = {_norm_label(x) for x in _strs("labels_missing")}
        manifest_norm = {_norm_label(lab) for lab in labels}
        # a misspelling must name a manifest string (the reviewer sometimes files its own commentary here)
        misspelled = [m for m in (v.get("misspelled") or []) if isinstance(m, dict) and m.get("expected")
                      and _norm_label(m["expected"]) in manifest_norm and _norm_label(m.get("seen", "")) != _norm_label(m["expected"])]
        misspelled_norm = {_norm_label(m["expected"]) for m in misspelled}
        illegible = _strs("illegible")
        illegible_norm = {_norm_label(x) for x in illegible}
        missing = [lab for lab in labels if _norm_label(lab) not in found_norm
                   and (_norm_label(lab) in listed_missing or (_norm_label(lab) not in misspelled_norm and _norm_label(lab) not in illegible_norm))]
        leaked = _strs("leaked_tokens")
        result: dict[str, Any] = {
            "ok": None, "format_ok": bool(v.get("format_ok")), "detected_format": v.get("detected_format"),
            "title_found": bool(v.get("title_found")),
            "labels_found": [lab for lab in labels if _norm_label(lab) in found_norm],
            "labels_missing": missing, "misspelled": misspelled, "illegible": illegible,
            "prohibited_elements": _strs("prohibited_elements"), "leaked_tokens": sorted(set(leaked)),
            "extra_text": _strs("extra_text"), "density": v.get("density"), "legible_at_4k": v.get("legible_at_4k"),
            "suggestion": v.get("suggestion") or None, "confidence": v.get("confidence") or "low",
            "checked": True, "model": model, "usage": usage, "n_labels": len(labels),
        }
        return rescore_verdict(result, labels)
    except Exception as exc:  # noqa: BLE001 — never block rendering on the checker
        logger.error(f"plate check failed: {exc}")
        base["issues"] = [f"check error: {str(exc)[:200]}"]
        return base


def rescore_verdict(verdict: dict[str, Any], labels: list[str]) -> dict[str, Any]:
    """Re-apply the manifest-aware reconciliation and the acceptance rule to a stored verdict (no vision call):
    extra text that is or contains a manifest string is not invented; a misspelling must name a manifest string."""
    v = dict(verdict or {})
    if not v.get("checked"):
        return v
    import difflib

    manifest_norm = {_norm_label(lab) for lab in labels}
    by_norm = {_norm_label(lab): lab for lab in labels}
    misspelled = [m for m in (v.get("misspelled") or []) if isinstance(m, dict) and m.get("expected")
                  and _norm_label(m["expected"]) in manifest_norm and _norm_label(m.get("seen", "")) != _norm_label(m["expected"])]
    known_seen = {_norm_label(m.get("seen", "")) for m in misspelled}
    extra: list[str] = []
    for t in v.get("extra_text") or []:
        raw = re.sub(r"\s*\((?:[^()]|\([^()]*\))*\)\s*$", "", str(t)).strip()   # the reviewer's commentary goes
        core = _norm_label(raw)
        if not core or core in manifest_norm or core in known_seen or any(lab in core or core in lab for lab in manifest_norm if len(lab) >= 12):
            continue
        near = difflib.get_close_matches(core, list(manifest_norm), n=1, cutoff=0.8)   # a misspelt manifest string, not invention
        if near:
            misspelled.append({"expected": by_norm[near[0]], "seen": raw})
            known_seen.add(core)
            continue
        extra.append(raw)
    v["extra_text"] = extra
    v["misspelled"] = misspelled
    v["leaked_tokens"] = sorted(set([str(x) for x in (v.get("leaked_tokens") or []) if leak_scan(str(x))] + [t for t in extra if leak_scan(t)]))
    v["ok"] = plate_verdict_ok(v, len(labels))
    issues = []
    if not v.get("format_ok"):
        issues.append(f"wrong format: looks like {v.get('detected_format')}")
    if v.get("prohibited_elements"):
        issues.append("prohibited: " + "; ".join(v["prohibited_elements"][:3]))
    if v.get("leaked_tokens"):
        issues.append("leaked tokens: " + "; ".join(v["leaked_tokens"][:4]))
    if str(v.get("density") or "").lower().startswith("sparse"):
        issues.append("sparse: the plate is not dense enough")
    if v.get("labels_missing"):
        issues.append(f"{len(v['labels_missing'])} string(s) missing: " + "; ".join(v["labels_missing"][:4]))
    if v.get("misspelled"):
        issues.append(f"{len(v['misspelled'])} misspelled: " + "; ".join(f"{m['expected']}→{m.get('seen', '?')}" for m in v["misspelled"][:3]))
    if v.get("illegible"):
        issues.append(f"{len(v['illegible'])} illegible: " + "; ".join(v["illegible"][:3]))
    inv = invented_sentences(v)
    if inv:
        issues.append(f"{len(inv)} invented sentence(s): " + "; ".join(t[:60] for t in inv[:2]))
    v["issues"] = issues
    return v


def revision_notes(verdict: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    if not verdict.get("format_ok"):
        notes.append(f"The previous image was NOT the required layout (it looked like: {verdict.get('detected_format')}). Draw the mandated grammar exactly.")
    for p in verdict.get("prohibited_elements") or []:
        notes.append(f"Remove: {p}")
    for t in verdict.get("leaked_tokens") or []:
        notes.append(f"REMOVE the leaked token “{t}” — bracketed tokens, colour codes, decimals and truncation notes are never printed")
    if str(verdict.get("density") or "").lower().startswith("sparse"):
        notes.append("The plate was SPARSE — render every string in the manifest and fill the canvas evenly; no empty regions")
    if verdict.get("labels_missing"):
        notes.append("These strings were MISSING — render each of them: " + "; ".join(verdict["labels_missing"][:16]))
    for m in verdict.get("misspelled") or []:
        notes.append(f"Spell exactly “{m.get('expected')}” (the previous image printed “{m.get('seen')}”)")
    if verdict.get("illegible"):
        notes.append("These strings were illegible (too small / overlapped / cut off) — make them large and clear: " + "; ".join(verdict["illegible"][:10]))
    if verdict.get("extra_text"):
        notes.append("Remove invented text that is not in the content: " + "; ".join(verdict["extra_text"][:6]))
    if not verdict.get("title_found"):
        notes.append("The title was missing — render it at the top.")
    if verdict.get("legible_at_4k") is False:
        notes.append("Increase every text size: labels ≥ 1.4% of the image height, notes ≥ 1.0%")
    if verdict.get("suggestion"):
        notes.append(str(verdict["suggestion"]))
    return notes


def _attempt_score(verdict: Optional[dict[str, Any]]) -> tuple[int, int, int, int]:
    """Lower is better: (format/prohibited/leak, sparse, strings missing+misspelled+illegible, unchecked)."""
    if not verdict or not verdict.get("checked"):
        return (1, 1, 999, 1)
    bad_format = 0 if (verdict.get("format_ok") and not verdict.get("prohibited_elements") and not verdict.get("leaked_tokens")) else 1
    sparse = 1 if str(verdict.get("density") or "").lower().startswith("sparse") else 0
    bad = len(verdict.get("labels_missing") or []) + len(verdict.get("misspelled") or []) + len(verdict.get("illegible") or [])
    return (bad_format, sparse, bad, 0)


# ══════════════════════════════════════════════════════════════════════════
# Render: spec → prompt → 4K image → check → (one revision) → save; every receipt on the record
# ══════════════════════════════════════════════════════════════════════════

def _render_once(job_id: str, spec: PlateSpec, prompt: str, aspect: str, provider: str, attempt: int):
    from src.images.adapter import generate_image

    return generate_image(prompt, provider=provider, size=RENDER_SIZE, aspect=aspect, no_text=False, timeout_s=RENDER_TIMEOUT_S), provider


def render_plate(job: DossierJob, spec: PlateSpec, out_dir: Path, provider: Optional[str] = None,
                 on_attempt: Optional[Callable[[dict[str, Any]], None]] = None, max_attempts: int = MAX_RENDER_ATTEMPTS) -> Plate:
    """spec → declutter → prompt → 4K render → check (tiles) → retry once → save. Returns the Plate record.

    Raises only when no image could be produced at all; the caller applies the skip law."""
    from src.images.storage import figure_url, save_figure

    provider = provider or DEFAULT_PROVIDER
    fam = family_entry(spec.family)
    spec.family = normalize_family(spec.family) or spec.family
    spec.visual_format = normalize_format_key(spec.visual_format) or fam["format"]
    aspect = spec.aspect if spec.aspect in ASPECTS else fam["aspect"]
    spec.aspect = aspect
    if not spec.style_school:
        spec.style_school = choose_style_school(job, spec.visual_format)
    canonical, declutter_report = declutter_plate(spec.canonical, spec.family)
    spec.canonical = canonical
    spec.size_guides = extract_size_guides(canonical)
    for k, v in (spec.__dict__.get("_declutter") or {}).items():   # the wall's own trims travel with the record
        if k == "dropped":
            declutter_report["dropped"] = list(v) + declutter_report["dropped"]
        else:
            declutter_report[k] = declutter_report.get(k, 0) + v
    plate = Plate(**spec.model_dump(), grounding=spec.__dict__.get("_grounding"), declutter=declutter_report)
    if declutter_report.get("dropped") or declutter_report.get("trimmed") or declutter_report.get("deduped"):
        events.emit(job.id, "note", phase=STEP, detail=f"{spec.key}: declutter trimmed {declutter_report['trimmed']}, deduped {declutter_report['deduped']}, "
                    f"dropped {len(declutter_report['dropped'])} item(s)", payload_json={"kind": "plate_declutter", "key": spec.key, **declutter_report})
    out_dir.mkdir(parents=True, exist_ok=True)
    attempts: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    revision: list[str] = []
    label = f"plate {spec.key}"
    n_labels = len(collect_plate_labels(canonical))

    for attempt in range(1, max(1, int(max_attempts or 1)) + 1):
        prompt = build_plate_prompt(spec, revision_notes=revision or None)
        leaks = leak_scan(prompt_content_section(prompt))
        if leaks:  # the content block is clean by construction; this is the last wall before money is spent
            raise RuntimeError(f"prompt content carries leak tokens: {leaks[:5]}")
        events.emit(job.id, "call_started", phase=STEP, model=provider, label=f"{label} (attempt {attempt})",
                    detail=f"rendering {spec.key} as {spec.family}/{spec.visual_format} ({RENDER_SIZE}, {aspect}, {n_labels} strings, style {spec.style_school})",
                    prompt_excerpt=events.excerpt(prompt, 600))
        started = time.time()
        try:
            result, provider_used = _render_once(job.id, spec, prompt, aspect, provider, attempt)
        except Exception as exc:
            events.emit(job.id, "call_failed", phase=STEP, label=f"{label} (attempt {attempt})", detail=f"{spec.key}: render failed: {exc}")
            if attempts:
                break
            raise
        duration_ms = int((time.time() - started) * 1000)
        image_bytes: bytes = getattr(result, "image_bytes", b"") or b""
        mime = str(getattr(result, "mime_type", "image/png") or "image/png")
        model_used = str(getattr(result, "model", "") or "")
        cost = float(getattr(result, "cost_usd", 0.0) or 0.0)
        if not image_bytes:
            raise RuntimeError("image provider returned no bytes")
        rec = make_receipt(step=STEP, kind="image", model=model_used or provider_used, label=f"{label} (attempt {attempt})",
                           duration_ms=duration_ms, prompt_text=prompt, cost_usd=cost)
        record(job.id, rec)
        receipts.append(rec.model_dump())
        events.emit(job.id, "call_finished", phase=STEP, model=model_used or provider_used, label=f"{label} (attempt {attempt})",
                    cost_usd=cost, duration_ms=duration_ms,
                    detail=f"{spec.key} attempt {attempt} rendered by {provider_used} at {getattr(result, 'width', '?')}x{getattr(result, 'height', '?')} in {duration_ms/1000:.0f}s (${cost:.3f})")

        verdict = check_plate(image_bytes, spec)
        usage = verdict.get("usage") or {}
        if verdict.get("checked") and usage.get("input_tokens"):
            crec = make_receipt(step=STEP, kind="llm", model=str(verdict.get("model") or ""), label=f"plate check {spec.key} (attempt {attempt})",
                                input_tokens=int(usage.get("input_tokens") or 0), output_tokens=int(usage.get("output_tokens") or 0))
            record(job.id, crec)
            receipts.append(crec.model_dump())
        ext = {"image/jpeg": "jpg", "image/webp": "webp"}.get(mime, "png")
        local = out_dir / f"{spec.key}.attempt{attempt}.{ext}"
        local.write_bytes(image_bytes)
        meta = {"prompt": prompt, "prompt_sent": getattr(result, "prompt_sent", prompt), "provider": provider_used, "model": model_used,
                "cost_usd": cost, "size": RENDER_SIZE, "aspect": aspect, "caption": spec.narrative[:300], "register": "plate", "scene": "",
                "compliance": verdict, "latency_ms": duration_ms, "dossier_job_id": job.id, "title": spec.title, "family": spec.family,
                "visual_format": spec.visual_format, "perspective": spec.perspective, "style_school": spec.style_school, "attempt": attempt}
        figure_id = None
        try:
            figure_id = save_figure(image_bytes, mime, job_id=job.id, name=f"plate-{spec.key}" + (f"-a{attempt}" if attempt > 1 else ""), meta=meta)
        except Exception as exc:
            events.emit(job.id, "note", phase=STEP, detail=f"{spec.key}: save_figure failed ({exc}); keeping the local copy only")
        arec = {"n": attempt, "provider": provider_used, "model": model_used, "cost_usd": cost, "latency_ms": duration_ms, "figure_id": figure_id,
                "path": str(local), "prompt_chars": len(prompt), "width": getattr(result, "width", None), "height": getattr(result, "height", None),
                "compliance": verdict, "revision_notes": list(revision)}
        attempts.append(arec)
        summary = ("ok" if verdict.get("ok") else ("not checked" if not verdict.get("checked") else "not ok: " + "; ".join(verdict.get("issues", [])[:3])))
        events.emit(job.id, "note", phase=STEP, detail=f"plate check {spec.key} attempt {attempt}: {summary}",
                    payload_json={"kind": "plate_check", "key": spec.key, "attempt": attempt, "verdict": verdict})
        if on_attempt:
            try:
                on_attempt(arec)
            except Exception:
                pass
        if verdict.get("ok") or not verdict.get("checked"):
            break
        revision = revision_notes(verdict)

    best = min(attempts, key=lambda a: _attempt_score(a.get("compliance")))
    for a in attempts:
        a["kept"] = a is best
    kept_path = Path(best["path"])
    final = out_dir / f"{spec.key}{kept_path.suffix}"
    final.write_bytes(kept_path.read_bytes())
    plate.figure_id = best["figure_id"]
    plate.path = str(final)
    plate.url = f"/v1/dossier/jobs/{job.id}/plates/{spec.key}.jpg"
    plate.provider = best["provider"]
    plate.model = best["model"] or None
    plate.prompt = build_plate_prompt(spec, revision_notes=best["revision_notes"] or None)
    plate.width, plate.height = best.get("width"), best.get("height")
    plate.cost_usd = round(sum(float(r.get("cost_usd") or 0.0) for r in receipts), 4)
    plate.compliance = best["compliance"]
    plate.attempts = attempts
    plate.receipts = receipts
    plate.status = "generated"
    v = best["compliance"] or {}
    if v.get("checked") and not v.get("ok"):
        plate.note = "compliance: " + "; ".join(v.get("issues", [])[:3])
    events.emit(job.id, "artifact", phase=STEP, detail=f"plate {spec.key}: {spec.title} — {spec.family}/{spec.visual_format} (level {spec.abstraction_level}), "
                f"{len(attempts)} attempt(s), kept #{best['n']}" + (f" — {plate.note}" if plate.note else ""),
                payload_json={"kind": "plate", "key": spec.key, "url": plate.url, "path": plate.path, "figure_id": plate.figure_id,
                              "provider": plate.provider, "cost_usd": plate.cost_usd, "family": spec.family, "visual_format": spec.visual_format,
                              "perspective": spec.perspective, "title": spec.title, "attempts": len(attempts), "kept": best["n"], "compliance": v})
    return plate


# ══════════════════════════════════════════════════════════════════════════
# The batch (plan → render each → persist each) — the skip law throughout
# ══════════════════════════════════════════════════════════════════════════

# One 4K render (plus its vision check) at a time per process: two concurrent plate runs OOM-killed the 512 MB
# instance on 2026-09-03 (exit 137). Plate runs from different jobs queue here instead of racing.
_RENDER_GATE = threading.Semaphore(1)


def run_plates(job: DossierJob, n: int = 2, perspectives: Optional[list[str]] = None, provider: Optional[str] = None,
               persist: Optional[Callable[[Plate], None]] = None, specs: Optional[list[PlateSpec]] = None) -> list[Plate]:
    """Plan N plates over a finished job and render them; `persist` is called after every plate (incremental)."""
    started = time.time()
    events.emit(job.id, "phase_started", phase=STEP,
                detail=f"Planning {n} plate(s) — perspectives that each deserve a whole 4K diagram — then rendering and checking them.")
    plates: list[Plate] = []
    if specs is None:
        try:
            specs = plan_plates(job, n, perspectives=perspectives)
        except Exception as exc:
            logger.warning(f"plate planning failed: {exc}", exc_info=True)
            events.emit(job.id, "call_failed", phase=STEP, label="plate plan", detail=f"plates_skipped: planning failed ({exc.__class__.__name__}: {exc})",
                        payload_json={"kind": "plates_skipped", "reason": str(exc)[:300]})
            events.emit(job.id, "phase_finished", phase=STEP, duration_ms=int((time.time() - started) * 1000), detail="plates: planning failed; nothing rendered")
            return []
    events.emit(job.id, "artifact", phase=STEP, detail=f"plate plan: {len(specs)} perspective(s) — " + ", ".join(f"{s.key}={s.family}" for s in specs),
                payload_json={"kind": "plate_plan", "plates": [s.model_dump() for s in specs]})
    out_dir = job_dir(job.id) / "plates"
    for spec in specs:
        planned = Plate(**spec.model_dump(), status="planned", grounding=spec.__dict__.get("_grounding"))
        if persist:
            try:
                persist(planned)
            except Exception as exc:
                logger.debug(f"persist planned plate failed: {exc}")
        try:
            with _RENDER_GATE:
                plate = render_plate(job, spec, out_dir, provider, on_attempt=None)
        except Exception as exc:
            logger.warning(f"plate {spec.key} failed: {exc}", exc_info=True)
            events.emit(job.id, "call_failed", phase=STEP, label=f"plate {spec.key}", detail=f"plate_failed {spec.key}: {exc}",
                        payload_json={"kind": "plate_failed", "key": spec.key, "reason": str(exc)[:300]})
            plate = Plate(**spec.model_dump(), status="failed", note=str(exc)[:300], grounding=spec.__dict__.get("_grounding"))
        plates.append(plate)
        if persist:
            try:
                persist(plate)
            except Exception as exc:
                logger.warning(f"persist plate failed: {exc}")
    total = round(sum(p.cost_usd for p in plates), 4)
    ok = sum(1 for p in plates if p.status == "generated" and (p.compliance or {}).get("ok"))
    events.emit(job.id, "phase_finished", phase=STEP, duration_ms=int((time.time() - started) * 1000),
                detail=f"plates done: {len(plates)} plate(s), {ok} passed the check, ${total:.2f}",
                payload_json={"kind": "plates_done", "count": len(plates), "ok": ok, "cost_usd": total})
    return plates


# ══════════════════════════════════════════════════════════════════════════
# The appendix partial (the composer includes it later; standalone render here)
# ══════════════════════════════════════════════════════════════════════════

TEMPLATES_DIR = Path(__file__).parent / "templates"


def appendix_context(plates: list[Plate], src_for: Optional[Callable[[Plate], Optional[str]]] = None) -> dict[str, Any]:
    """The `plates` list the partial reads: index, title, src, narrative, perspective, family/format, level, check line."""
    out = []
    for i, p in enumerate([p for p in plates if p.status == "generated"], start=1):
        v = p.compliance or {}
        if not v.get("checked"):
            check = "not checked"
        elif v.get("ok"):
            check = f"passed — {len(v.get('labels_found') or [])}/{v.get('n_labels')} strings found"
        else:
            check = "flagged — " + "; ".join(v.get("issues", [])[:2])
        src = src_for(p) if src_for else (f"plates/{Path(p.path).name}" if p.path else p.url)
        out.append({"index": i, "key": p.key, "title": p.title, "src": src, "narrative": p.narrative, "perspective": p.perspective,
                    "family": p.family, "visual_format": p.visual_format, "level": p.abstraction_level, "why": p.why_this_perspective,
                    "style_school": p.style_school, "attempts": len(p.attempts), "check": check, "cost_usd": p.cost_usd,
                    "width": p.width, "height": p.height})
    return {"plates": out}


def render_appendix_html(plates: list[Plate], src_for: Optional[Callable[[Plate], Optional[str]]] = None) -> str:
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=select_autoescape(["html", "j2"]))
    return env.get_template("plates_appendix.html.j2").render(**appendix_context(plates, src_for))


# ══════════════════════════════════════════════════════════════════════════
# CLI: plan and/or render against a saved job.json (no server needed)
# ══════════════════════════════════════════════════════════════════════════

def _main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m src.dossier.plates", description="Plan plates from a saved dossier job.json and render them at 4K.")
    ap.add_argument("--job", required=True, help="path to a dossier job.json")
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--out", required=True, help="output directory (specs, prompts, images, verdicts)")
    ap.add_argument("--job-id", default=None, help="job id to record receipts/events under (default: sample-<id>)")
    ap.add_argument("--provider", default=None)
    ap.add_argument("--perspective", action="append", default=None, help="a requested perspective (repeatable)")
    ap.add_argument("--plan-only", action="store_true")
    ap.add_argument("--specs", default=None, help="render these saved specs (JSON list) instead of planning")
    ap.add_argument("--only", default=None, help="render only this spec key")
    ap.add_argument("--persist", action="store_true", help="upsert each plate into dossier_plates under --job-id (the API and the desk then serve it)")
    ap.add_argument("--max-attempts", type=int, default=MAX_RENDER_ATTEMPTS, help="render attempts per plate (1 = no revision pass)")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING, format="%(asctime)s %(name)s %(levelname)s %(message)s")

    job = DossierJob.model_validate(json.loads(Path(args.job).read_text("utf-8")))
    job.id = args.job_id or f"sample-{job.id}"
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if args.specs:
        specs = [PlateSpec.model_validate(s) for s in json.loads(Path(args.specs).read_text("utf-8"))]
        material_norm = normalize(plate_material(job))
        for s in specs:
            errors, grounding = validate_plate_spec(s, material_norm)
            s.__dict__["_grounding"] = grounding
            if errors:
                print(f"[{s.key}] wall errors: {errors}")
            if not s.style_school:
                s.style_school = choose_style_school(job, s.visual_format)
    else:
        specs = plan_plates(job, args.n, perspectives=args.perspective)
        rejected = getattr(plan_plates, "last_rejected", [])
        if rejected:
            (out / "rejected.json").write_text(json.dumps(rejected, ensure_ascii=False, indent=2), "utf-8")
    if args.only:
        specs = [s for s in specs if s.key == args.only]
    (out / "specs.json").write_text(json.dumps([s.model_dump() for s in specs], ensure_ascii=False, indent=2), "utf-8")
    for s in specs:
        g = s.__dict__.get("_grounding", {})
        print(f"[{s.key}] {s.perspective!r} → {s.family}/{s.visual_format} L{s.abstraction_level} {s.aspect} | {s.title!r} | "
              f"{g.get('labels')} strings, {g.get('grounded')}/{g.get('content_labels')} grounded | style {s.style_school}")
    if args.plan_only:
        return 0
    total = 0.0
    for s in specs:
        try:
            plate = render_plate(job, s, out, args.provider, max_attempts=args.max_attempts)
        except Exception as exc:
            print(f"[{s.key}] FAILED: {exc}")
            continue
        total += plate.cost_usd
        if args.persist:
            from src.dossier.plate_store import upsert_plate

            upsert_plate(job.id, plate)
        (out / f"{s.key}.prompt.txt").write_text(plate.prompt or "", "utf-8")
        (out / f"{s.key}.verdict.json").write_text(json.dumps({"spec": s.model_dump(), "compliance": plate.compliance, "attempts": plate.attempts,
                                                               "grounding": plate.grounding, "declutter": plate.declutter, "cost_usd": plate.cost_usd,
                                                               "provider": plate.provider, "model": plate.model, "path": plate.path,
                                                               "width": plate.width, "height": plate.height}, ensure_ascii=False, indent=2), "utf-8")
        v = plate.compliance or {}
        print(f"[{s.key}] {plate.path} {plate.width}x{plate.height} | attempts {len(plate.attempts)} | ok={v.get('ok')} format_ok={v.get('format_ok')} "
              f"found={len(v.get('labels_found') or [])}/{v.get('n_labels')} missing={len(v.get('labels_missing') or [])} "
              f"illegible={len(v.get('illegible') or [])} leaked={v.get('leaked_tokens')} density={v.get('density')} | ${plate.cost_usd:.3f}")
    print(f"total cost (images + checks): ${total:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
