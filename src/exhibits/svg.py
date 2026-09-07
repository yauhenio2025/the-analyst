"""Exhibits drawn by code from a finished oeuvre job's rows (2026-09-07; redrawn the same day after the owner's audit: "clumsy and
crowded, ids instead of titles"): the oeuvre timeline (the author's texts on a year axis, the agendas as named lanes, the focal text
marked with its title, the turns as named cuts) and the two-halves panel (the verdict as a seam; what persists crossing it, what
breaks stopping at it, each line a sentence with its two texts named by year and title). No model call; every mark comes from a
row or the packet; a row's id lives in the hover title, never on the face. The dataviz reference palette; light and dark selected.
"""
from __future__ import annotations

import html
import re
from typing import Any, Optional

SERIES_LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
SERIES_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]
STYLE = """<style>
.viz{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:13px}
.viz .t1{fill:#0b0b0b}.viz .t2{fill:#52514e}.viz .t3{fill:#8a8985}.viz .grid{stroke:#e5e4e0;stroke-width:1}.viz .axis{stroke:#c9c8c3;stroke-width:1}
.viz .surface{fill:#fcfcfb}.viz .seam{stroke:#0b0b0b;stroke-width:2}.viz .box{fill:#f4f3f0;stroke:#dad9d4}.viz .tick{stroke:#8a8985}.viz .focal{stroke:#0b0b0b;fill:#0b0b0b}
%s
@media (prefers-color-scheme: dark){.viz .t1{fill:#ffffff}.viz .t2{fill:#c3c2b7}.viz .t3{fill:#8a8985}.viz .grid{stroke:#333331}.viz .axis{stroke:#4a4946}
.viz .surface{fill:#1a1a19}.viz .seam{stroke:#ffffff}.viz .box{fill:#242422;stroke:#3a3a37}.viz .tick{stroke:#8a8985}.viz .focal{stroke:#ffffff;fill:#ffffff} %s}
</style>"""
UID_YEAR = re.compile(r"(em:[A-Z0-9]+)/(\d{4})")
UID = re.compile(r"em:[A-Z0-9]+")


def _esc(s: Any) -> str:
    return html.escape(str(s or ""), quote=True)


def _style() -> str:
    light = "".join(f".viz .s{i}{{fill:{c};stroke:{c}}}" for i, c in enumerate(SERIES_LIGHT))
    dark = "".join(f".viz .s{i}{{fill:{c};stroke:{c}}}" for i, c in enumerate(SERIES_DARK))
    return STYLE % (light, dark)


def _short(text: str, n: int) -> str:
    t = re.sub(r"\s+", " ", text or "").strip()
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def _wrap(text: str, width: int, max_lines: int = 3) -> list[str]:
    """Words into lines of at most `width` characters; the last line ends with … if cut."""
    words = re.sub(r"\s+", " ", text or "").strip().split(" ")
    lines: list[str] = []
    cur = ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) > width and cur:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
        if len(lines) == max_lines:
            break
    if len(lines) < max_lines and cur:
        lines.append(cur)
    if len(" ".join(lines)) < len(" ".join(words)) and lines:
        lines[-1] = _short(lines[-1], width - 1) + "…" if not lines[-1].endswith("…") else lines[-1]
    return lines


def _tspans(lines: list[str], x: float, y: float, dy: int, cls: str = "t2", size: int = 12, anchor: str = "start") -> str:
    return "".join(f'<text x="{x:.1f}" y="{y + i * dy:.1f}" class="{cls}" font-size="{size}" text-anchor="{anchor}">{_esc(l)}</text>' for i, l in enumerate(lines))


def agenda_name(a: dict) -> str:
    """The agenda's name: the engine's `name` field when it gave one, else derived from the sentence ('The transition agenda explains …'
    → 'the transition agenda'; else its first concept)."""
    if a.get("name"):
        return a["name"].strip().rstrip(".")
    text = a.get("text") or ""
    m = re.match(r"^(The [\w\-' ]{2,40}? agenda)\b", text)
    if m:
        return m.group(1)[0].lower() + m.group(1)[1:]
    concepts = [c.strip() for c in re.split(r"[;,]", a.get("concepts") or "") if c.strip()]
    if concepts:
        return concepts[0]
    return _short(text, 40)


def turn_name(t: dict) -> str:
    """The turn's name: the engine's `name` when given; else 'to <its to-field>' (a lineage id like CHECK.T2.F1 is not a name); else
    the sentence's own 'turns to …' clause; else the sentence."""
    if t.get("name"):
        return t["name"].strip().rstrip(".")
    to = (t.get("to") or "").strip()
    if to and not re.match(r"^(CHECK\.)?[A-Z]\d\.F\d+$", to):
        return "to " + to.rstrip(".")
    text = t.get("text") or ""
    m = re.search(r"turns? (?:from .+? )?(?:toward|to|into)\s+(.+?)(?:\.|$)", text)
    if m:
        return "to " + m.group(1).rstrip(".")
    return text.rstrip(".")


def _span_years(span: str) -> tuple[Optional[int], Optional[int]]:
    years = [int(y) for _, y in UID_YEAR.findall(span or "")]
    return (min(years) if years else None, max(years) if years else None)


def _texts_by_uid(packet: Optional[dict]) -> dict[str, dict]:
    out = {}
    for t in (packet or {}).get("texts") or []:
        out[t.get("uid", "")] = t
    f = (packet or {}).get("focal") or {}
    if f.get("uid"):
        out[f["uid"]] = {**f, "side": "focal"}
    return out


def _cite(ref: str, texts: dict[str, dict], width: int = 42) -> str:
    """'em:27CQX9UR/1976' → '1976 · Agrarian Class Structure …' when the packet knows the text; else the ref as given."""
    m = UID_YEAR.search(ref or "")
    if m and m.group(1) in texts:
        return f"{m.group(2)} · {_short(texts[m.group(1)].get('title', ''), width)}"
    return _short(ref or "", width + 8)


# ── the timeline ──────────────────────────────────────────────────────────────────────────────────────────────────

def timeline_svg(oeuvre: dict, packet: dict, *, width: int = 1100) -> str:
    texts = [t for t in (packet.get("texts") or []) if str(t.get("year") or "").isdigit()]
    focal = packet.get("focal") or {}
    author = (packet.get("author") or {}).get("name") or (packet.get("author") or {}).get("id") or "the author"
    agendas = [a for a in oeuvre.get("agendas") or [] if a.get("span")]
    turns = oeuvre.get("turns") or []
    years = [int(t["year"]) for t in texts] + ([int(focal["year"])] if str(focal.get("year") or "").isdigit() else [])
    if not years:
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="60" class="viz">{_style()}<text x="10" y="30" class="t2">no dated texts</text></svg>'
    y0, y1 = min(years), max(max(years), min(years) + 1)
    left, right = 250, width - 30                     # a name column on the left; the year axis to the right
    top = 58
    lane_h, lane_gap = 22, 8
    lanes_top = top + 26
    lanes_h = len(agendas[:8]) * (lane_h + lane_gap)
    axis_y = lanes_top + lanes_h + 30
    turn_rows = min(len(turns), 8)
    height = axis_y + 44 + turn_rows * 18 + 30
    def X(year: float) -> float:
        return left + (right - left) * (year - y0) / (y1 - y0)
    name_display = author.split(",")[0] if "," in author else author
    if "," in author:
        last, first = [x.strip() for x in author.split(",", 1)]
        name_display = f"{first} {last}"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" class="viz" role="img" aria-label="The oeuvre on one line">',
           _style(), f'<rect class="surface" x="0" y="0" width="{width}" height="{height}"/>',
           f'<text x="24" y="26" class="t1" font-size="16" font-weight="600">{_esc(name_display)}’s oeuvre, {y0}–{y1}: {len(agendas)} research agendas and the {_esc(focal.get("year") or "focal")} paper</text>',
           f'<text x="24" y="46" class="t2">lanes: an agenda from its first text to its last · ticks: the texts, the marked one the paper · cuts below the axis: the turns, each between two texts · hover anything for its finding</text>']
    for yr in range(((y0 + 4) // 5) * 5, y1 + 1, 5):
        x = X(yr)
        out.append(f'<line class="grid" x1="{x:.1f}" y1="{lanes_top - 4}" x2="{x:.1f}" y2="{axis_y + 8}"/>')
        out.append(f'<text x="{x:.1f}" y="{axis_y + 24}" class="t2" text-anchor="middle">{yr}</text>')
    for i, a in enumerate(agendas[:8]):
        ya, yb = _span_years(a["span"])
        if ya is None:
            continue
        y = lanes_top + i * (lane_h + lane_gap)
        xa, xb = X(ya), X(max(yb, ya + 0.6))
        name = agenda_name(a)
        n_texts = re.search(r"(\d+)\s+(?:principal\s+)?texts?", a.get("span") or "")
        out.append(f'<g><title>{_esc(a["id"])} — {_esc(a.get("text"))} — {_esc(a["span"])}</title>'
                   f'<text x="{left - 12}" y="{y + 15}" class="t1" font-size="13" text-anchor="end">{_esc(_short(name, 30))}</text>'
                   f'<rect class="s{i}" x="{xa:.1f}" y="{y}" width="{max(xb - xa, 6):.1f}" height="{lane_h}" rx="5" opacity="0.85"/>'
                   + (f'<text x="{xa + 8:.1f}" y="{y + 15}" class="t1" font-size="12" fill-opacity="0.95">{ya}–{yb}{" · " + n_texts.group(1) + " texts" if n_texts else ""}</text>' if (xb - xa) > 120 else "")
                   + "</g>")
    for t in texts:
        yr = int(t["year"]); x = X(yr)
        is_focal = t.get("uid") == focal.get("uid")
        out.append(f'<g><title>{yr} — {_esc(t.get("title"))}</title><line class="{"focal" if is_focal else "tick"}" x1="{x:.1f}" y1="{axis_y - (20 if is_focal else 11)}" x2="{x:.1f}" y2="{axis_y}" stroke-width="{3 if is_focal else 1.5}" opacity="{1 if is_focal else 0.75}"/></g>')
    out.append(f'<line class="axis" x1="{left}" y1="{axis_y}" x2="{right}" y2="{axis_y}"/>')
    if str(focal.get("year") or "").isdigit():
        xf = X(int(focal["year"]))
        label = f'{focal.get("year")} · {focal.get("title", "")}'
        lx = min(xf + 10, right - 8 * len(_short(label, 70)) * 0.62)
        out.append(f'<circle cx="{xf:.1f}" cy="{axis_y - 30}" r="6" class="s3"/><text x="{lx:.1f}" y="{axis_y - 26}" class="t1" font-weight="600">{_esc(_short(label, 70))}</text>')
    for k, t in enumerate(turns[:8]):
        hits = UID_YEAR.findall(t.get("at") or "")
        if len(hits) < 2:
            continue
        ya, yb = int(hits[0][1]), int(hits[1][1])
        xa, xb = X(ya), X(yb)
        ym = axis_y + 44 + k * 18
        label = f'{ya}→{yb} {turn_name(t)}'
        out.append(f'<g><title>{_esc(t["id"])} — {_esc(t.get("text"))} — at {_esc(t.get("at"))} — changed: {_esc(t.get("changed"))}</title>'
                   f'<line x1="{xa:.1f}" y1="{ym}" x2="{xb:.1f}" y2="{ym}" stroke="#8a8985" stroke-width="1.5" stroke-dasharray="3 3"/>'
                   f'<line x1="{xb:.1f}" y1="{ym - 5}" x2="{xb:.1f}" y2="{ym + 5}" class="seam" stroke-width="2"/>'
                   f'<text x="{left - 12}" y="{ym + 4}" class="t2" font-size="11" text-anchor="end">{_esc(_short(label, 38))}</text></g>')
    out.append("</svg>")
    return "\n".join(out)


# ── the two halves ────────────────────────────────────────────────────────────────────────────────────────────────

def two_halves_svg(oeuvre: dict, *, width: int = 1100, packet: Optional[dict] = None) -> str:
    """Before and after as two columns with the paper as a thin gutter between them (redrawn 2026-09-07 after the owner's audit:
    the earlier seam-with-lines form ran its lines through the text). One row per finding: what persists (a filled marker) and
    what changes (a hollow marker, tagged where the change happens); each row names its two texts by year and title."""
    rup = oeuvre.get("rupture") or []
    verdict = next((r for r in rup if r.get("dim") == "verdict"), {})
    cont = [r for r in rup if r.get("dim") == "continuity"]
    brk = [r for r in rup if r.get("dim") == "break"]
    texts = _texts_by_uid(packet)
    focal = (packet or {}).get("focal") or {}
    halves = (verdict.get("halves") or "").split(" vs ", 1)
    before_h = halves[0].strip() if halves else "before"
    after_h = halves[1].strip() if len(halves) > 1 else "after"
    v = (oeuvre.get("verdicts") or {}).get("rupture") or verdict.get("verdict") or ""
    gloss = {"rupture": "the object, question, method or interlocutors change at it", "reorientation": "the object stays; the question or the method changes",
             "deepening": "a change of topic within the same problematic", "continuity": "nothing consequential changes at it", "outlier": "a text neither side takes up"}.get(v, "")
    yr = focal.get("year") or ""
    gutter = 96
    margin = 40                      # the row marker sits in the left margin, never over the text
    col_w = (width - margin - 24 - gutter) // 2
    lx, rx = margin, margin + col_w + gutter
    chars = int((col_w - 24) / 6.9)
    bl, al = _wrap(before_h, chars, 3), _wrap(after_h, chars, 3)
    head_h = 16 * max(len(bl), len(al), 1) + 16
    y = 60 + head_h + 26
    rows = [(r, True) for r in cont] + [(r, False) for r in brk]
    # measure each row: the sentence wraps across the full width in the label line; the two texts sit in their columns
    blocks = []
    for r, persists in rows:
        what = (r.get("what") or "").strip()
        tag = "persists" if persists else {"yes": "changes at the paper", "partly": "changes partly at the paper"}.get((r.get("at_focal") or "").lower(), "changes later")
        sent = _wrap(r.get("text", ""), int((width - margin - 24) / 7.2), 2)
        b_ref, a_ref = r.get("before") or "", r.get("after") or ""
        b_txt = _cite(b_ref, texts, 2 * chars) if UID_YEAR.search(b_ref) else b_ref
        a_txt = _cite(a_ref, texts, 2 * chars) if UID_YEAR.search(a_ref) else a_ref
        bw, aw = _wrap(b_txt, chars, 2), _wrap(a_txt, chars, 2)
        h = 16 * len(sent) + 14 * max(len(bw), len(aw), 1) + 22
        blocks.append((r, persists, what, tag, sent, bw, aw, h))
    height = y + sum(b[-1] for b in blocks) + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" class="viz" role="img" aria-label="Before and after the paper">',
           _style(), f'<rect class="surface" x="0" y="0" width="{width}" height="{height}"/>',
           f'<text x="24" y="26" class="t1" font-size="16" font-weight="600">Does the {_esc(yr)} paper mark a break? Verdict: {_esc(v or "not given")}{" — " + _esc(gloss) if gloss else ""}</text>',
           f'<text x="24" y="46" class="t2">left: the texts before the paper · right: the texts after · a filled mark: this persists across the paper · a hollow mark: this changes · hover a row for its finding</text>',
           f'<rect class="box" x="{lx}" y="58" width="{col_w}" height="{head_h}" rx="6"/>' + _tspans(bl, lx + 12, 78, 16, "t1", 12),
           f'<rect class="box" x="{rx}" y="58" width="{col_w}" height="{head_h}" rx="6"/>' + _tspans(al, rx + 12, 78, 16, "t1", 12),
           f'<text x="{width // 2}" y="{58 + head_h // 2 + 5}" class="t1" text-anchor="middle" font-weight="600" font-size="12">{_esc(yr)}</text>']
    for r, persists, what, tag, sent, bw, aw, h in blocks:
        cls = "s2" if persists else "s1"
        out.append(f'<g><title>{_esc(r["id"])} — {_esc(r.get("text"))} — before: {_esc(r.get("before"))} — after: {_esc(r.get("after"))}</title>')
        out.append(f'<line class="grid" x1="{lx}" y1="{y - 6}" x2="{width - 24}" y2="{y - 6}"/>')
        out.append(f'<circle cx="{margin // 2}" cy="{y + 10}" r="5" class="{cls}"' + ("" if persists else ' fill="none" stroke-width="2"') + "/>")
        out.append(f'<text x="{lx}" y="{y + 14}" class="t1" font-size="12"><tspan font-weight="600">{_esc(tag)} · {_esc(what)}.</tspan> {_esc(sent[0] if sent else "")}</text>')
        yy = y + 14
        for line in sent[1:]:
            yy += 16; out.append(f'<text x="{lx}" y="{yy}" class="t2" font-size="12">{_esc(line)}</text>')
        yy += 18
        out.append(_tspans(bw, lx, yy, 14, "t3", 11) + _tspans(aw, rx, yy, 14, "t3", 11))
        out.append("</g>")
        y += h
    out.append(f'<text x="{margin}" y="{height - 14}" class="t2" font-size="11">{len(cont)} things persist across the paper · {len(brk)} change, {sum(1 for r in brk if (r.get("at_focal") or "").lower() in ("yes", "partly"))} of them at the paper itself</text>')
    out.append("</svg>")
    return "\n".join(out)


MAKERS = {"oeuvre-timeline": "timeline", "two-halves": "halves"}


def exhibit_svg(key: str, oeuvre: dict, packet: Optional[dict]) -> Optional[str]:
    if key == "oeuvre-timeline":
        return timeline_svg(oeuvre, packet or {})
    if key == "two-halves":
        return two_halves_svg(oeuvre, packet=packet)
    return None
