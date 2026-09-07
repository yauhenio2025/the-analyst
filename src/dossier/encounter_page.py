"""The encounter as a page the owner can read whole (Evgeny, 2026-09-07 18:28: "where do I see more data on Hintze? that rows file is a
wall of text"): composed by code from the encounter's rows — the thinker's positions with their loci, the axes with his side and yours,
what you take, whom he argues against, the questions back, the route in. The text leads; ids ride on hover; the engines' own prose folds
at the foot. No model call: a design change never costs a rerun."""
from __future__ import annotations

import html
import re
from typing import Any, Optional

from src.dossier.page_loop import CSS, _paras


def _e(s: Any) -> str:
    return html.escape(str(s or ""), quote=True)


def _name(ref: str, texts: dict[str, dict], width: int = 90) -> str:
    """'em:JZJL34ZJ' or 'em:X/1929' → '1929 · Title' when the job knows the text; else the ref as given."""
    m = re.match(r"^(em:[A-Za-z0-9]+)(?:/(\d{4}))?$", (ref or "").strip())
    if m and m.group(1) in texts:
        t = texts[m.group(1)]; title = (t.get("title") or "").strip(); year = t.get("year") or m.group(2) or ""
        title = title if len(title) <= width else title[:width - 1].rstrip() + "…"
        return f"{year} · {title}" if year else title
    return ref or ""


def _card(label: str, body: str, meta: str = "") -> str:
    return f"<div class='card'><div class='body'><div class='t'>{_e(label)}</div><div class='why'>{body}</div>" + (f"<div class='meta'>{_e(meta)}</div>" if meta else "") + "</div></div>"


def compose_encounter_page(enc: dict, texts: dict[str, dict], *, turn: str = "", prose: Optional[dict[str, str]] = None, cost_usd: Optional[float] = None) -> str:
    """enc: render_encounter's output; texts: uid → {title, year, creators} for the job's texts; prose: the engines' own prose by engine."""
    who = enc.get("thinker") or "the thinker"
    positions, concepts, opponents = enc.get("positions") or [], enc.get("concepts") or [], enc.get("opponents") or []
    silences, takes, route, asks = enc.get("silences") or [], enc.get("takes") or [], enc.get("read_next") or [], enc.get("challenges") or []
    short = {}
    for x in positions + concepts:
        short[x["id"].split("/", 1)[1]] = x
    read = sorted({p.get("ref") for p in positions if p.get("ref")})
    body = [f"<h1>Your encounter with {_e(who)}</h1><p class='sub'>{_e(turn or 'the deep operation around one thinker')} · read across {len(read)} text{'s' if len(read) != 1 else ''} of his</p>"]
    # the lead, from the rows
    lead = (f"On {len({p.get('question') for p in positions})} of your questions {_e(who)} takes a position in the held texts; {len(concepts)} of his concepts carry them"
            + (f"; he argues against {', '.join(_e(o.get('opponent')) for o in opponents[:4])}" if opponents else "")
            + (f"; on {len(silences)} of your questions the held texts are silent" if silences else "") + ". The meeting runs on "
            + f"{len(enc.get('axes') or [])} ax{'es' if len(enc.get('axes') or []) != 1 else 'is'}; you take {len(takes)} of his elements one way or another; {len(asks)} question{'s' if len(asks) != 1 else ''} wait for you on the Brief.")
    body.append(f"<p>{lead}</p>")
    if read:
        body.append("<p class='grasp'>The texts read: " + "; ".join(_e(_name(r, texts)) for r in read) + ".</p>")
    # the axes: the meeting, one section each
    for a in enc.get("axes") or []:
        ax = a["axis"]; rels = a.get("relations") or []
        body.append(f"<section><h2 title='{_e(ax['id'])}'>{_e(ax['text'].split(':', 1)[0])}</h2>")
        if ":" in ax["text"]:
            body.append(f"<p class='grasp'>{_e(ax['text'].split(':', 1)[1].strip())}</p>")
        for r in rels:
            word = (r.get("relation") or "").replace("_", " ")
            parts = ", ".join(str(x) for x in re.findall(r"\d+", r.get("bears_on") or ""))
            body.append("<div class='box two'>"
                        f"<div><h4>{_e(who)}</h4><p>{_e(r.get('theirs'))}</p></div><div><h4>You</h4><p>{_e(r.get('ours'))}</p></div></div>")
            body.append(f"<p><b>Yours {_e(word)} his.</b> " + (f"Bridge: {_e(r.get('bridge'))}. " if r.get("bridge") and r.get("bridge").lower() != "none" else "") + (f"Bears on part{'s' if ',' in parts else ''} {parts}." if parts else "") + "</p>")
        gathered = a.get("positions") or []
        if gathered:
            body.append("<ul>" + "".join(f"<li title='{_e(p['id'])}'><b>{_e(_name(p.get('ref'), texts, 70))}</b>" + (f", {_e(p.get('locus'))}" if p.get("locus") else "") + f": {_e(p['text'])}" + (f" <span class='rid'>“{_e(p['anchor'][:160])}”</span>" if p.get("anchor") else "") + "</li>" for p in gathered) + "</ul>")
        for x in a.get("route") or []:
            body.append(f"<p class='grasp'>Read next for this axis: {_e(_name(x.get('ref'), texts))} — {_e(x.get('why'))} ({'in the library' if (x.get('held') or '').lower() == 'yes' else 'not in the library'}).</p>")
        body.append("</section>")
    # what you take
    if takes or concepts:
        body.append("<section><h2>What you take from him, and what you refuse</h2>")
        rows = []
        for t in takes:
            el = short.get(t.get("element", ""), {})
            label = el.get("concept") or el.get("text", "")[:90] or t.get("element", "")
            into = t.get("into") if (t.get("into") or "").lower() not in ("", "none") else ""
            rows.append(f"<tr><td><b>{_e(t.get('take'))}</b></td><td>{_e(label)}</td><td>{_e(el.get('text', '') if el.get('concept') else '')}</td><td>{_e(into)}</td><td class='rid'>{_e(t.get('text'))}</td></tr>")
        body.append("<table class='shift'><tr><th>you</th><th>his element</th><th>in his system</th><th>into ours</th><th>why</th></tr>" + "".join(rows) + "</table>")
        untaken = [c for c in concepts if c["id"].split("/", 1)[1] not in {t.get("element") for t in takes}]
        if untaken:
            body.append("<p class='grasp'>Concepts of his the draft did not decide on: " + "; ".join(f"<b>{_e(c.get('concept'))}</b> ({_e(c.get('puts_to_owner'))}?)" for c in untaken) + ".</p>")
        body.append("</section>")
    if opponents or silences:
        body.append("<section><h2>Whom he argues against, and where he is silent</h2>")
        if opponents:
            body.append("<div class='chips'>" + "".join(f"<span class='chip' title='{_e(o['id'])}'><span class='k'>against</span>{_e(o.get('opponent'))}" + (" · shared with you" if (o.get("shared") or "").lower() == "yes" else "") + "</span>" for o in opponents) + "</div>")
            body.append("<ul>" + "".join(f"<li>{_e(o['text'])}</li>" for o in opponents) + "</ul>")
        if silences:
            body.append("<p>" + " ".join(_e(s_["text"]) + "." if not s_["text"].endswith(".") else _e(s_["text"]) for s_ in silences) + "</p>")
        body.append("</section>")
    if asks:
        body.append("<section><h2>The questions back to you</h2><ol>" + "".join(f"<li title='{_e(c['ask']['id'])}'><b>{_e(c['ask']['kind'])}</b> — {_e(c['ask']['text'])}" + (f" <span class='rid'>{' | '.join(_e(o) for o in c['ask']['options'])}</span>" if c["ask"].get("options") else "") + "</li>" for c in asks) + "</ol><p class='grasp'>Answer them on the Brief; each is filed there as a distinction challenge.</p></section>")
    if route:
        body.append("<section><h2>The route into him</h2><div class='cards'>" + "".join(f"<div class='card' title='{_e(x['id'])}'><div class='rank'>{_e(x.get('rank'))}</div><div class='body'><div class='t'>{_e(_name(x.get('ref'), texts))}</div><div class='why'>{_e(x.get('why'))}</div><div class='meta'>{'in the library' if (x.get('held') or '').lower() == 'yes' else 'not in the library' if (x.get('held') or '').lower() == 'no' else 'holding unknown'}</div></div></div>" for x in route) + "</div></section>")
    notes = [f"<p>{enc.get('rows')} rows read by code, {enc.get('conjectures')} of them unanchored" + (f"; ${cost_usd:.2f}" if cost_usd is not None else "") + ".</p>"]
    for k, v in (prose or {}).items():
        if v:
            notes.append(f"<h4>{_e(k)}'s own reading</h4>" + _paras(v[:6000]))
    body.append("<details class='about'><summary>How this page was made</summary>" + "".join(notes) + "</details>")
    return "<!doctype html><html><head><meta charset='utf-8'><title>" + _e(f"Your encounter with {who}") + "</title>" + CSS + "</head><body><div class='page'>" + "\n".join(body) + "</div></body></html>"


def texts_of_job(job: dict, get_text) -> dict[str, dict]:
    """uid → {title, year, creators} from the job's statements document (the Stacks' sources) and its document list."""
    import json
    out: dict[str, dict] = {}
    for d in job.get("documents") or []:
        key = str(d.get("key") or "")
        m = re.search(r"(em:[A-Za-z0-9]+)", key)
        if m:
            out[m.group(1)] = {"title": d.get("title") or key, "year": d.get("year") or "", "creators": d.get("creators") or ""}
        if d.get("role") in ("statements", "evidence_index") and d.get("executor_doc_id"):
            try:
                obj = json.loads(get_text(d["executor_doc_id"]) or "{}")
            except ValueError:
                continue
            for s_ in obj.get("sources") or []:
                if s_.get("uid"):
                    out[s_["uid"]] = {"title": s_.get("title") or s_["uid"], "year": s_.get("year") or "", "creators": s_.get("creators") or ""}
    return out
