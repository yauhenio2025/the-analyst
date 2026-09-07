"""Exhibits drawn by code from a finished oeuvre job's rows (2026-09-07): the oeuvre timeline (the author's texts on a year
axis, the agendas as lanes spanning their first and last text, the focal text marked, the turns as cuts) and the two-halves panel
(the rupture verdict as a seam, what persists as lines crossing it, what breaks as lines that stop at it). No model call; every
mark comes from a row or the packet, and every text carries its row id in a hover title. The palette is the dataviz reference
palette (validated categorical slots in fixed order; text in text tokens; light and dark selected, never flipped).
"""
from __future__ import annotations

import html
import re
from typing import Any, Optional

SERIES_LIGHT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
SERIES_DARK = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300", "#9085e9", "#e66767"]
STYLE = """<style>
.viz{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:12px}
.viz .t1{fill:#0b0b0b}.viz .t2{fill:#52514e}.viz .grid{stroke:#e5e4e0;stroke-width:1}.viz .axis{stroke:#c9c8c3;stroke-width:1}
.viz .surface{fill:#fcfcfb}.viz .seam{stroke:#0b0b0b;stroke-width:2}.viz .box{fill:#f4f3f0;stroke:#dad9d4}
%s
@media (prefers-color-scheme: dark){.viz .t1{fill:#ffffff}.viz .t2{fill:#c3c2b7}.viz .grid{stroke:#333331}.viz .axis{stroke:#4a4946}
.viz .surface{fill:#1a1a19}.viz .seam{stroke:#ffffff}.viz .box{fill:#242422;stroke:#3a3a37} %s}
</style>"""


def _esc(s: Any) -> str:
    return html.escape(str(s or ""), quote=True)


def _series_css() -> tuple[str, str]:
    light = "".join(f".viz .s{i}{{fill:{c};stroke:{c}}}" for i, c in enumerate(SERIES_LIGHT))
    dark = "".join(f".viz .s{i}{{fill:{c};stroke:{c}}}" for i, c in enumerate(SERIES_DARK))
    return light, dark


def _style() -> str:
    l, d = _series_css()
    return STYLE % (l, d)


UID_YEAR = re.compile(r"(em:[A-Z0-9]+)/(\d{4})")


def _span_years(span: str) -> tuple[Optional[int], Optional[int], list[str]]:
    """'em:A/1972 … em:B/2021; 16 principal texts' → (1972, 2021, [uids])."""
    hits = UID_YEAR.findall(span or "")
    years = [int(y) for _, y in hits]
    return (min(years) if years else None, max(years) if years else None, [u for u, _ in hits])


def _short(text: str, n: int) -> str:
    t = re.sub(r"\s+", " ", text or "").strip()
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def timeline_svg(oeuvre: dict, packet: dict, *, width: int = 1100) -> str:
    """The oeuvre on one line: agendas as lanes (first → last text), the texts as ticks by year, the focal text marked, the turns
    as cuts between the two dated texts that show them."""
    texts = [t for t in (packet.get("texts") or []) if str(t.get("year") or "").isdigit()]
    focal = packet.get("focal") or {}
    agendas = [a for a in oeuvre.get("agendas") or [] if a.get("span")]
    turns = oeuvre.get("turns") or []
    years = [int(t["year"]) for t in texts] + [int(focal["year"])] if focal.get("year") else [int(t["year"]) for t in texts]
    if not years:
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="60" class="viz">{_style()}<text x="10" y="30" class="t2">no dated texts</text></svg>'
    y0, y1 = min(years), max(years)
    y1 = max(y1, y0 + 1)
    left, right, top = 40, width - 200, 44
    lane_h, lane_gap = 18, 10
    lanes_top = top + 30
    lanes_h = len(agendas) * (lane_h + lane_gap)
    ticks_y = lanes_top + lanes_h + 24
    height = ticks_y + 60 + 14 * min(len(turns), 8) + 24
    def X(year: float) -> float:
        return left + (right - left) * (year - y0) / (y1 - y0)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" class="viz" role="img" aria-label="The oeuvre on one line">',
           _style(), f'<rect class="surface" x="0" y="0" width="{width}" height="{height}"/>',
           f'<text x="{left}" y="24" class="t1" font-size="15" font-weight="600">{_esc(packet.get("author", {}).get("name") or packet.get("author", {}).get("id") or "the author")}: the oeuvre on one line</text>',
           f'<text x="{left}" y="{top - 4}" class="t2">agendas as lanes from their first to their last text · the texts as ticks · the focal text marked · the turns as cuts</text>']
    # decade grid
    for yr in range((y0 // 5) * 5, y1 + 1, 5):
        if yr < y0:
            continue
        x = X(yr)
        out.append(f'<line class="grid" x1="{x:.1f}" y1="{lanes_top - 6}" x2="{x:.1f}" y2="{ticks_y + 14}"/>')
        out.append(f'<text x="{x:.1f}" y="{ticks_y + 30}" class="t2" text-anchor="middle">{yr}</text>')
    # agenda lanes
    for i, a in enumerate(agendas[:8]):
        ya, yb, _ = _span_years(a["span"])
        if ya is None:
            continue
        y = lanes_top + i * (lane_h + lane_gap)
        xa, xb = X(ya), X(max(yb, ya + 0.5))
        label = _short(a.get("text", ""), 70)
        out.append(f'<g class="s{i}"><title>{_esc(a["id"])}: {_esc(a.get("text"))} — {_esc(a["span"])}</title>'
                   f'<rect x="{xa:.1f}" y="{y}" width="{max(xb - xa, 6):.1f}" height="{lane_h}" rx="4" opacity="0.85"/></g>')
        out.append(f'<text x="{right + 12}" y="{y + 13}" class="t2" font-size="11"><tspan class="t1" font-weight="600">{_esc(a["id"])}</tspan> {_esc(_short(label, 26))}</text>')
        out.append(f'<text x="{xa + 4:.1f}" y="{y + 13}" class="t1" font-size="11" fill-opacity="0.9">{_esc(_short(a.get("text", ""), int((xb - xa) / 6.2)))}</text>' if (xb - xa) > 80 else "")
    # text ticks
    for t in texts:
        yr = int(t["year"]); x = X(yr)
        is_focal = t.get("uid") == focal.get("uid")
        h = 22 if is_focal else 12
        cls = "t1" if is_focal else "t2"
        out.append(f'<g><title>{_esc(t.get("uid"))}/{yr}: {_esc(t.get("title"))}</title>'
                   f'<line x1="{x:.1f}" y1="{ticks_y - h}" x2="{x:.1f}" y2="{ticks_y}" stroke="{"#0b0b0b" if is_focal else "#8a8985"}" stroke-width="{3 if is_focal else 1.5}" opacity="{1 if is_focal else 0.8}"/></g>')
    if focal.get("year"):
        xf = X(int(focal["year"]))
        out.append(f'<circle cx="{xf:.1f}" cy="{ticks_y - 28}" r="6" class="s3"/><text x="{xf + 10:.1f}" y="{ticks_y - 24}" class="t1" font-weight="600">{_esc(focal.get("year"))} · {_esc(_short(focal.get("title", ""), 44))}</text>')
    out.append(f'<line class="axis" x1="{left}" y1="{ticks_y}" x2="{right}" y2="{ticks_y}"/>')
    # turns as cuts
    for k, t in enumerate(turns[:8]):
        hits = UID_YEAR.findall(t.get("at") or "")
        if len(hits) < 2:
            continue
        ya, yb = int(hits[0][1]), int(hits[1][1])
        xa, xb = X(ya), X(yb)
        ym = ticks_y + 46 + k * 14                                   # one row per turn: no two labels share a line
        lx = max(left, min(xa, right - 220))                          # the label starts at the turn's first text, kept on the canvas
        out.append(f'<g><title>{_esc(t["id"])}: {_esc(t.get("text"))} — at {_esc(t.get("at"))} — changed: {_esc(t.get("changed"))}</title>'
                   f'<line x1="{xa:.1f}" y1="{ym}" x2="{xb:.1f}" y2="{ym}" stroke="#8a8985" stroke-width="1.5" stroke-dasharray="3 3"/>'
                   f'<line x1="{xb:.1f}" y1="{ym - 5}" x2="{xb:.1f}" y2="{ym + 5}" class="seam" stroke-width="2"/>'
                   f'<text x="{lx:.1f}" y="{ym - 3}" class="t2" font-size="10">{_esc(t["id"])} {ya}→{yb} · {_esc(_short(t.get("changed", ""), 40))}</text></g>')
    out.append(f'<text x="{left}" y="{height - 6}" class="t2" font-size="10">rows: {_esc(", ".join(a["id"] for a in agendas))} (agendas) · {_esc(", ".join(t["id"] for t in turns))} (turns) · the packet\'s texts; hover a mark for its row</text>')
    out.append("</svg>")
    return "\n".join(x for x in out if x)


def two_halves_svg(oeuvre: dict, *, width: int = 1100) -> str:
    """The two halves and the seam: the verdict labels the seam; continuity rows cross it; break rows stop at it."""
    rup = oeuvre.get("rupture") or []
    verdict = next((r for r in rup if r.get("dim") == "verdict"), {})
    cont = [r for r in rup if r.get("dim") == "continuity"]
    brk = [r for r in rup if r.get("dim") == "break"]
    halves = (verdict.get("halves") or "").split(" vs ", 1)
    before_h = halves[0].strip() if halves else "before"
    after_h = halves[1].strip() if len(halves) > 1 else "after"
    v = (oeuvre.get("verdicts") or {}).get("rupture") or verdict.get("verdict") or ""
    rows_n = max(len(cont) + len(brk), 1)
    row_h = 26
    top = 92
    height = top + rows_n * row_h + 60
    mid = width // 2
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" class="viz" role="img" aria-label="The two halves and the seam">',
           _style(), f'<rect class="surface" x="0" y="0" width="{width}" height="{height}"/>',
           f'<text x="24" y="24" class="t1" font-size="15" font-weight="600">The two halves and the seam · verdict: {_esc(v or "not given")}</text>',
           f'<text x="24" y="42" class="t2">what persists crosses the seam; what breaks stops at it; hover a line for its row</text>',
           f'<rect class="box" x="24" y="52" width="{mid - 48}" height="30" rx="6"/><text x="36" y="72" class="t1" font-size="12">{_esc(_short(before_h, 92))}</text>',
           f'<rect class="box" x="{mid + 24}" y="52" width="{mid - 48}" height="30" rx="6"/><text x="{mid + 36}" y="72" class="t1" font-size="12">{_esc(_short(after_h, 92))}</text>',
           f'<line class="seam" x1="{mid}" y1="52" x2="{mid}" y2="{height - 40}"/>',
           f'<text x="{mid}" y="{height - 24}" class="t1" text-anchor="middle" font-weight="600">the focal text · {_esc(v)}</text>']
    y = top
    for r in cont:
        what = r.get("what") or ""; b = r.get("before") or ""; a = r.get("after") or ""
        out.append(f'<g class="s2"><title>{_esc(r["id"])}: {_esc(r.get("text"))} — before {_esc(b)} — after {_esc(a)}</title>'
                   f'<line x1="60" y1="{y + 12}" x2="{width - 60}" y2="{y + 12}" stroke-width="2"/>'
                   f'<circle cx="60" cy="{y + 12}" r="4"/><circle cx="{width - 60}" cy="{y + 12}" r="4"/></g>')
        out.append(f'<text x="70" y="{y + 8}" class="t1" font-size="11"><tspan font-weight="600">persists · {_esc(what)}</tspan> <tspan class="t2">{_esc(_short(r.get("text", ""), max(20, int((mid - 90) / 6.4) - len(what) - 12)))}</tspan></text>')
        out.append(f'<text x="70" y="{y + 22}" class="t2" font-size="10">{_esc(_short(b, 40))}</text><text x="{width - 70}" y="{y + 22}" class="t2" font-size="10" text-anchor="end">{_esc(_short(a, 40))}</text>')
        y += row_h
    for r in brk:
        what = r.get("what") or ""; b = r.get("before") or ""; a = r.get("after") or ""; at = (r.get("at_focal") or "").lower()
        stop = mid - 8 if at in ("yes", "partly") else mid + 8
        out.append(f'<g class="s1"><title>{_esc(r["id"])}: {_esc(r.get("text"))} — before: {_esc(b)} — after: {_esc(a)} — at the focal text: {_esc(at)}</title>'
                   f'<line x1="60" y1="{y + 12}" x2="{stop}" y2="{y + 12}" stroke-width="2"/><circle cx="60" cy="{y + 12}" r="4"/>'
                   f'<line x1="{mid + 8 if at in ("yes", "partly") else stop}" y1="{y + 12}" x2="{width - 60}" y2="{y + 12}" stroke-width="2" stroke-dasharray="4 4" opacity="0.7"/><circle cx="{width - 60}" cy="{y + 12}" r="4" fill="none" stroke-width="2"/></g>')
        out.append(f'<text x="70" y="{y + 8}" class="t1" font-size="11"><tspan font-weight="600">breaks · {_esc(what)}{" · at the focal text" if at == "yes" else (" · partly at the focal text" if at == "partly" else " · later")}</tspan></text>')
        out.append(f'<text x="70" y="{y + 22}" class="t2" font-size="10">{_esc(_short(b, 60))}</text><text x="{width - 70}" y="{y + 22}" class="t2" font-size="10" text-anchor="end">{_esc(_short(a, 60))}</text>')
        y += row_h
    out.append(f'<text x="24" y="{height - 6}" class="t2" font-size="10">rows: {_esc(verdict.get("id", ""))} (verdict) · {_esc(", ".join(r["id"] for r in cont))} (continuity) · {_esc(", ".join(r["id"] for r in brk))} (break)</text>')
    out.append("</svg>")
    return "\n".join(out)


MAKERS = {"oeuvre-timeline": "timeline", "two-halves": "halves"}


def exhibit_svg(key: str, oeuvre: dict, packet: Optional[dict]) -> Optional[str]:
    if key == "oeuvre-timeline":
        return timeline_svg(oeuvre, packet or {})
    if key == "two-halves":
        return two_halves_svg(oeuvre)
    return None
