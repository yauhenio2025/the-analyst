"""The page loop (Evgeny, 2026-09-07 09:45): plan → make → write → review → revise, over a finished oeuvre job, optimising time to
clarity at depth. The planner (engine page_planner) reads the memo as a document and the exhibits registry as records and writes
the plan as rows; the makers (code) build every exhibit from the rows; the prose desk (engine page_prose) writes the sections to
the plan's budgets; the composer (code) assembles the page; the reviewer (engine page_reviewer) reads it as the stated reader and
sends verdicts back; a second round re-plans with the verdicts. Walls by code at every seam: an exhibit kind must be in the
registry, a section must exist, a cited row must exist. Each round's page and record are kept in the blob store and served by
GET /v1/dossier/jobs/{id}/page[.json]. The reviewer's verdicts write back on the exhibits' evidence.
"""
from __future__ import annotations

import html
import json
import logging
import re
import threading
import time
from typing import Any, Callable, Optional

from src.dossier.explainer import CITED_ID, rows_with_fields

logger = logging.getLogger(__name__)
ROW_ID = re.compile(r"\b([a-z_]+/(?:[A-Z]\d\.)?F\d+)\b")
WIDE_KINDS = {"oeuvre-timeline", "two-halves", "shift-table", "idea-map"}
ORGANS = {"the Referee": "the citation-analysis engine that holds thinkers, their works and who cites them", "the Stacks": "the library: the texts, their profiles and citation ledgers",
          "the Mastermind": "the registry of methods, vocabularies and actions the organs read", "the Reporter": "the open-web harvester"}


# ── the memo as a document ────────────────────────────────────────────────────────────────────────────────────────

def memo_document(o: dict) -> str:
    """The oeuvre answer as the text the planner, the prose desk and the reviewer read: verdicts, the memo prose, every row."""
    v = o.get("verdicts") or {}
    parts = ["THE VERDICTS", *(f"- {k}: {v.get(k) or 'not given'}" for k in ("position", "retrospective", "prospective", "rupture", "place")),
             f"- halves: {v.get('halves', '')}", f"- warrant: {v.get('warrant', '')}", "", "THE MEMO", o.get("memo") or "", "", "THE ROWS (id · dimension · finding · fields)"]
    for group, engine in (("agendas", "oeuvre_trajectory"), ("turns", "oeuvre_trajectory"), ("place", "oeuvre_trajectory"), ("shifts", "citation_shift"),
                          ("retrospective", "retrospective_reading"), ("prospective", "prospective_reading"), ("rupture", "epistemic_rupture"),
                          ("read_next", "oeuvre_position_memo"), ("open", "oeuvre_position_memo")):
        for r in o.get(group) or []:
            fields = "; ".join(f"{k}: {str(val)[:160]}" for k, val in r.items() if k not in ("id", "dim", "text", "anchor", "doc", "conjecture", "confidence", "from", "status", "reason") and val)
            parts.append(f"[{engine}/{r['id']}] ({r.get('dim')}) {r.get('text', '')}" + (f" — {fields}" if fields else "") + (" — (anchor not verified)" if r.get("conjecture") else ""))
    return "\n".join(parts)


# ── the plan ──────────────────────────────────────────────────────────────────────────────────────────────────────

def parse_plan(final_output: str, registry_keys: set[str], row_ids: set[str], failed: set[str] = frozenset()) -> dict:
    """The planner's rows → {sections[], exhibits[], cuts[], rejected[]}; the walls: a kind must be in the registry, a section must
    exist, a cited row must exist (unknown ids are dropped from the list and noted)."""
    rows = rows_with_fields(final_output, failed)
    sections, exhibits, cuts, rejected = [], [], [], []
    for r in rows:
        f = r["fields"]
        if r["dim"] == "section":
            try:
                order = int(re.search(r"\d+", f.get("order", "") or "").group(0))
            except Exception:
                order = len(sections) + 1
            try:
                words = int(re.search(r"\d+", f.get("words", "") or "").group(0))
            except Exception:
                words = 250
            sections.append({"id": r["id"], "heading": r["text"], "order": order, "words": min(max(words, 60), 600), "grasp": f.get("grasp", ""), "from": ROW_ID.findall(f.get("from", "") or "")})
        elif r["dim"] == "exhibit":
            kind = (f.get("kind") or "").strip().strip("`'\"")
            ids = [i for i in ROW_ID.findall(f.get("rows", "") or "")]
            missing = [i for i in ids if i not in row_ids]
            if kind not in registry_keys:
                rejected.append({"id": r["id"], "why": f"kind {kind!r} is not in the exhibits registry"}); continue
            exhibits.append({"id": r["id"], "kind": kind, "text": r["text"], "section": (f.get("section") or "").strip(), "rows": [i for i in ids if i in row_ids], "missing_rows": missing,
                             "placement": (f.get("placement") or "after").strip(), "aim": f.get("aim", "")})
        elif r["dim"] == "cut":
            cuts.append({"id": r["id"], "what": r["text"], "why": f.get("why", ""), "kept_in": f.get("kept_in", "")})
    sections.sort(key=lambda s: s["order"])
    sec_ids = {s["id"] for s in sections}
    for e in list(exhibits):
        if e["section"] not in sec_ids:
            e["section"] = sections[0]["id"] if sections else ""
            e["note"] = "section not in the plan; placed first"
    seen: set[tuple[str, str]] = set()
    for e in list(exhibits):
        k = (e["kind"], e["section"])
        if k in seen:
            exhibits.remove(e); rejected.append({"id": e["id"], "why": f"a second {e['kind']} in section {e['section']}"})
        seen.add(k)
    return {"sections": sections, "exhibits": exhibits[:8], "cuts": cuts, "rejected": rejected}


def parse_prose(final_output: str, sections: list[dict]) -> dict[str, str]:
    """The prose desk's reading → {section id: the section's text}, matched by heading (exact, then loose)."""
    from src.executor.context_broker import split_ledger
    prose, _ = split_ledger(final_output)
    chunks = re.split(r"^#{1,4}\s+", prose, flags=re.M)
    got: dict[str, str] = {}
    def norm(s: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    heads = {norm(s["heading"]): s["id"] for s in sections}
    for ch in chunks[1:]:
        title, _, body = ch.partition("\n")
        t = norm(title)
        sid = heads.get(t) or next((sid for h, sid in heads.items() if h and (h in t or t in h)), None)
        if sid and sid not in got:
            got[sid] = body.strip()
    return got


def parse_review(final_output: str) -> dict:
    rows = rows_with_fields(final_output)
    verdicts = [{"id": r["id"], "element": (r["fields"].get("element") or "").strip(), "verdict": (r["fields"].get("verdict") or "").strip(), "reason": r["fields"].get("reason", ""), "fix": r["fields"].get("fix", ""), "text": r["text"]} for r in rows if r["dim"] == "verdict"]
    clarity = [{"id": r["id"], "section": (r["fields"].get("section") or "").strip(), "first_pass": (r["fields"].get("first_pass") or "").strip(), "why": r["fields"].get("why", ""), "text": r["text"]} for r in rows if r["dim"] == "clarity"]
    from src.executor.context_broker import split_ledger
    prose, _ = split_ledger(final_output)
    return {"verdicts": verdicts, "clarity": clarity, "summary": CITED_ID.sub("", (prose or "").strip())[:1200]}


# ── the page ──────────────────────────────────────────────────────────────────────────────────────────────────────

CSS = """<style>
:root{color-scheme:light dark}
body{margin:0;font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:16px;line-height:1.5;color:#0b0b0b;background:#fcfcfb}
.page{max-width:1080px;margin:0 auto;padding:28px 24px 60px}
h1{font-size:26px;line-height:1.2;margin:0 0 4px}.sub{color:#52514e;margin:0 0 18px}
h2{font-size:19px;margin:34px 0 8px}.grasp{color:#52514e;font-size:14px;margin:0 0 10px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.chip{border:1px solid #dad9d4;border-radius:999px;padding:4px 12px;font-size:14px;background:#f4f3f0}.chip .k{color:#52514e;margin-right:4px}
.halves{margin:6px 0 0;font-size:14px;color:#52514e}.halves .k{font-weight:600;margin-right:6px}
.box{border:1px solid #dad9d4;background:#f4f3f0;border-radius:8px;padding:10px 14px;font-size:14px;margin:12px 0}.box h4{margin:0 0 6px;font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:#52514e}.box ul{margin:0;padding-left:18px}.box.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.glossary dl{margin:0}.glossary dt{font-weight:600}.glossary dd{margin:0 0 6px;color:#52514e}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin:12px 0}.card{display:flex;gap:10px;border:1px solid #dad9d4;border-radius:8px;padding:10px;font-size:14px;background:#f4f3f0}.card .rank{font-size:22px;font-weight:700;color:#52514e}.card .t{font-weight:600}.card .why{color:#52514e}.card .meta{font-size:12px;color:#52514e}
table.shift{border-collapse:collapse;width:100%;font-size:13px;margin:12px 0}table.shift th,table.shift td{border-bottom:1px solid #dad9d4;padding:6px 8px;text-align:left;vertical-align:top}table.shift th{color:#52514e;font-weight:600}
blockquote.pull{border-left:3px solid #2a78d6;margin:14px 0;padding:6px 16px;font-size:18px;line-height:1.35;color:#0b0b0b}blockquote.pull footer{font-size:12px;color:#52514e;margin-top:6px}
.rid{font-size:11px;color:#8a8985}.beside{float:right;width:38%;margin:0 0 12px 18px}.exhibit{margin:14px 0}.exhibit svg{max-width:100%;height:auto}
details.folded{border:1px solid #dad9d4;border-radius:8px;background:#f4f3f0;padding:0 14px;margin:14px 0}details.folded summary{cursor:pointer;padding:10px 0;font-weight:600;font-size:14px;list-style:none}details.folded summary::-webkit-details-marker{display:none}details.folded summary .hint{float:right;font-weight:400;color:#52514e;font-size:12px}details.folded[open] summary .hint{display:none}details.folded>*:not(summary){margin-bottom:12px}
figure.pending{border:1px dashed #dad9d4;padding:10px;color:#52514e;font-size:13px}
.cap{font-size:12px;color:#52514e;margin:6px 0 0}figure.exhibit{margin:14px 0}
details.about{border-top:1px solid #dad9d4;margin-top:40px;padding-top:10px;font-size:13px;color:#52514e}details.about summary{cursor:pointer;color:#8a8985}details.about p{margin:8px 0}
@media (prefers-color-scheme: dark){body{color:#fff;background:#1a1a19}.sub,.grasp,.halves,.box h4,.glossary dd,.card .rank,.card .why,.card .meta,table.shift th,blockquote.pull footer,.cap,details.about{color:#c3c2b7}.chip,.box,.card,details.folded{background:#242422;border-color:#3a3a37}details.folded summary .hint{color:#c3c2b7}table.shift th,table.shift td{border-color:#3a3a37}figure.pending{border-color:#3a3a37}}
</style>"""


def _e(s: Any) -> str:
    return html.escape(str(s or ""), quote=True)


def _md_inline(text: str) -> str:
    t = _e(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t); t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    t = re.sub(r"\[([a-z_]+/(?:[A-Z]\d\.)?F\d+(?:[,;\s]+[a-z_]+/(?:[A-Z]\d\.)?F\d+)*)\]", r'<span class="rid">[\1]</span>', t)
    return t


def _paras(text: str) -> str:
    out = []
    for p in re.split(r"\n\s*\n", text or ""):
        p = p.strip()
        if not p:
            continue
        if p.startswith("- ") or p.startswith("* "):
            out.append("<ul>" + "".join(f"<li>{_md_inline(li[2:].strip())}</li>" for li in p.splitlines() if li.strip()) + "</ul>")
        else:
            out.append(f"<p>{_md_inline(p)}</p>")
    return "\n".join(out)


def compose_page(title: str, subtitle: str, plan: dict, prose: dict[str, str], exhibits: dict[str, dict], review: Optional[dict], round_no: int) -> tuple[str, str]:
    """The page HTML and its description (what the reviewer reads): sections in the plan's order, each exhibit placed as planned."""
    by_sec: dict[str, list[dict]] = {}
    first_section = plan["sections"][0]["id"] if plan.get("sections") else None
    verdicts = {v["element"]: v["verdict"] for v in (review or {}).get("verdicts", [])}
    dropped = {k for k, v in verdicts.items() if v == "drop"}
    plan["exhibits"] = [e for e in plan["exhibits"] if e["id"] not in dropped]        # a drop verdict on the round shown is applied, not merely printed (the owner, 16:39)
    for e in plan["exhibits"]:
        if verdicts.get(e["id"]) == "move" and e["placement"] != "before":
            e["placement"] = "folded"
        # the text is the main dish (the owner, 2026-09-07 11:45): a wide exhibit is never floated and never the lead; it folds
        if e["placement"] == "beside" and e["kind"] in WIDE_KINDS:
            e["placement"] = "folded"; e["note"] = (e.get("note") or "") + " folded (a wide exhibit is never floated)"
        if e["placement"] == "before" and e["kind"] != "verdict-chips":
            e["placement"] = "folded" if e["kind"] in WIDE_KINDS else "after"
            e["note"] = (e.get("note") or "") + f" moved {e['placement']} (only verdict chips stand before a section's text)"
        if e["section"] == first_section and e["placement"] != "before" and e["kind"] in WIDE_KINDS:
            e["placement"] = "folded"
        by_sec.setdefault(e["section"], []).append(e)
    body = [f"<h1>{_e(title)}</h1><p class='sub'>{_e(subtitle)} · page round {round_no}</p>"]
    desc = [f"PAGE: {title} — {subtitle}"]
    # the chips first when planned anywhere
    for s in plan["sections"]:
        exs = by_sec.get(s["id"], [])
        before = [e for e in exs if e["placement"] == "before"]; beside = [e for e in exs if e["placement"] == "beside"]; after = [e for e in exs if e["placement"] not in ("before", "beside")]
        body.append(f"<section id='{_e(s['id'])}'><h2>{_e(s['heading'])}</h2><p class='grasp'>{_e(s.get('grasp'))} <span class='rid'>[{_e(s['id'])}]</span></p>")
        desc.append(f"\n[{s['id']}] SECTION: {s['heading']} — grasp: {s.get('grasp')} — budget {s.get('words')} words")
        def place(e):
            m = exhibits.get(e["id"]) or {}
            title = (m.get("title") or e.get("aim") or e["kind"].replace("-", " ")).strip()
            if e["placement"] == "folded":   # a reference exhibit: a titled line the reader opens; the text is never hidden behind it
                body.append(f"<details class='exhibit folded' id='{_e(e['id'])}' title='{_e(e['id'])} · {_e(e['kind'])}'><summary>{_e(title)}<span class='hint'>open</span></summary>{m.get('html', '')}</details>")
            else:   # the caption is the aim in words; the plan id and the kind ride on hover, never on the face (the owner, 16:39)
                cls = "exhibit beside" if e["placement"] == "beside" else "exhibit"
                body.append(f"<figure class='{cls}' id='{_e(e['id'])}' title='{_e(e['id'])} · {_e(e['kind'])}'>{m.get('html', '')}<figcaption class='cap'>{_e(e.get('aim'))}</figcaption></figure>")
            desc.append(f"[{e['id']}] EXHIBIT {e['kind']} ({e['placement']}{', shown as a titled line the reader opens' if e['placement'] == 'folded' else ''}) — aim: {e.get('aim')} — shows: {m.get('description', '(not made)')}")
        for e in before: place(e)
        for e in beside: place(e)
        text = prose.get(s["id"], "")
        body.append(_paras(text) if text else "<p class='grasp'>(no prose written for this section)</p>")
        desc.append(f"PROSE ({len(text.split())} words): {text}")
        for e in after: place(e)
        body.append("</section>")
    notes = []   # the loop's working notes fold at the foot: the reader's page is the essay, not the desk's ledger (the owner, 16:39)
    if plan.get("cuts"):
        notes.append("<p><b>Left out of the page:</b> " + "; ".join(f"{_e(c['what'])} ({_e(c['why'])})" for c in plan["cuts"]) + "</p>")
    if review:
        notes.append("<p><b>The reviewer's verdicts on this round:</b> " + "; ".join(f"{_e(v['element'])} {_e(v['verdict'])} — {_e(v['reason'])}" for v in review.get("verdicts", [])) + "</p>")
    if notes:
        body.append("<details class='about'><summary>How this page was made</summary>" + "".join(notes) + "</details>")
    return "<!doctype html><html><head><meta charset='utf-8'><title>" + _e(title) + "</title>" + CSS + "</head><body><div class='page'>" + "\n".join(body) + "</div></body></html>", "\n".join(desc)


# ── the loop ──────────────────────────────────────────────────────────────────────────────────────────────────────

def run_page_loop(job_id: str, o: dict, packet: dict, *, audience: str = "researcher", rounds: int = 2, model: str = "anthropic/claude-sonnet-5",
                  call_fn: Optional[Callable] = None, on_round: Optional[Callable[[dict], None]] = None, exhibit_registry=None, prior: Optional[dict] = None) -> dict:
    """Plan → make → write → review, `rounds` times; the second round plans with the verdicts. Returns the record of every round."""
    from src.dossier.engine_call import call_engine
    from src.exhibits.makers import make
    from src.exhibits.registry import get_exhibit_registry, planner_block
    from src.sources.schemas import SourceSpec

    reg = exhibit_registry or get_exhibit_registry()
    memo = memo_document(o)
    row_ids = set(ROW_ID.findall(memo))
    title = f"{(packet.get('focal') or {}).get('title') or 'the focal text'} ({(packet.get('focal') or {}).get('year') or ''}) in {(packet.get('author') or {}).get('name') or 'the oeuvre'}"
    subtitle = f"what role the paper plays in the oeuvre · for a {audience}"
    src = [SourceSpec(kind="paste", key="memo", title=f"The memo: {title}", text=memo)]
    record = {"job_id": job_id, "title": title, "audience": audience, "rounds": [], "cost_usd": 0.0}
    review = None
    if prior and prior.get("rounds"):   # a loop interrupted by a restart continues from its last finished round (2026-09-07)
        record = {**record, **{k: prior[k] for k in ("rounds", "cost_usd") if k in prior}}
        review = record["rounds"][-1].get("review")
    for n in range(len(record["rounds"]) + 1, rounds + 1):
        t0 = time.time()
        packet_plan = {"audience": audience, "exhibits": planner_block(reg.list()), "previous_review": review, "round": n,
                       "note": "Use only the exhibit keys listed; cite row ids exactly as they appear in the memo document (engine/F<n>). The text is the main dish: only verdict chips stand before the first section's text; a wide exhibit (timeline, two-halves, shift-table, idea-map) is folded (a titled line the reader opens) or after its section, never beside and never the lead. In a second round, act on every verdict that is not keep."}
        planned = call_engine("page_planner", src, packet=packet_plan, depth="surface", model=model, spend_cap_usd=3.0, call_fn=call_fn)
        plan = parse_plan(planned["final_output"], {e.key for e in reg.list()}, row_ids, set(planned["wall"]["failed_ids"]))
        made = {e["id"]: (make(e["kind"], o, rows=e["rows"], packet=packet) or {"html": "", "description": "no maker"}) for e in plan["exhibits"]}
        packet_prose = {"audience": audience, "plan": {"sections": plan["sections"], "exhibits": [{"id": e["id"], "kind": e["kind"], "section": e["section"], "shows": made[e["id"]]["description"][:600]} for e in plan["exhibits"]]},
                        "glossary": ORGANS, "note": "Gloss a system's name (the Referee, the Stacks) in one clause on its first use; use each verdict word the plan names at least once, with its gloss."}
        written = call_engine("page_prose", src, packet=packet_prose, depth="surface", model=model, spend_cap_usd=3.0, call_fn=call_fn)
        prose = parse_prose(written["final_output"], plan["sections"])
        page_html, page_desc = compose_page(title, subtitle, plan, prose, made, None, n)
        rsrc = [SourceSpec(kind="paste", key="page", title=f"The page, round {n}: {title}", text=page_desc)]
        reviewed = call_engine("page_reviewer", rsrc, packet={"audience": audience, "plan_aims": [{"id": s["id"], "grasp": s["grasp"]} for s in plan["sections"]]}, depth="surface", model=model, spend_cap_usd=3.0, call_fn=call_fn)
        review = parse_review(reviewed["final_output"])
        page_html, _ = compose_page(title, subtitle, plan, prose, made, review, n)
        cost = round(planned["cost_usd"] + written["cost_usd"] + reviewed["cost_usd"], 4)
        rnd = {"round": n, "plan": plan, "prose": prose, "exhibits": {k: {"kind": next((e["kind"] for e in plan["exhibits"] if e["id"] == k), ""), "description": v["description"]} for k, v in made.items()},
               "review": review, "html": page_html, "description": page_desc, "cost_usd": cost, "seconds": round(time.time() - t0, 1),
               "receipts": {"planner": planned["calls"], "prose": written["calls"], "reviewer": reviewed["calls"]}}
        record["rounds"].append(rnd); record["cost_usd"] = round(record["cost_usd"] + cost, 4)
        if on_round:
            on_round(rnd)
        # the reviewer's verdicts write back on the exhibits they judged
        for v in review.get("verdicts", []):
            kind = next((e["kind"] for e in plan["exhibits"] if e["id"] == v["element"]), None)
            if kind and v["verdict"] in ("keep", "simplify", "replace", "drop", "move"):
                try:
                    from src.exhibits.registry import ExhibitUse
                    reg.add_use(kind, ExhibitUse(page=f"{job_id}/round{n}", organ="the-mastermind", verdict=v["verdict"], note=v.get("reason", "")[:200]))
                except Exception as exc:
                    logger.debug(f"exhibit use not recorded: {exc}")
        if all(v["verdict"] == "keep" for v in review.get("verdicts", [])) and review.get("verdicts"):
            break
    record["final_html"] = record["rounds"][-1]["html"] if record["rounds"] else ""
    return record


# ── storage and background runs ──────────────────────────────────────────────────────────────────────────────────

def _blob_key(job_id: str, what: str) -> str:
    return f"page:{job_id}:{what}"


def _put(key: str, content_type: str, data: bytes) -> None:
    from src.dossier.blob_store import put_blob_safe
    put_blob_safe(key, content_type, data)


def _get(key: str) -> Optional[bytes]:
    from src.dossier.blob_store import get_blob
    got = get_blob(key)
    return got[1] if isinstance(got, tuple) else got


def save_page(job_id: str, record: dict, status: Optional[dict] = None) -> None:
    """The record (slim: no html per round), the final html, each round's html — and the loop's status, so a restart cannot erase
    a running loop (2026-09-07: the Reporter's deploy gate restarted the API mid-loop and the loop vanished)."""
    slim = {**record, "rounds": [{k: v for k, v in r.items() if k != "html"} for r in record.get("rounds", [])]}
    _put(_blob_key(job_id, "record"), "application/json", json.dumps(slim, ensure_ascii=False).encode("utf-8"))
    if record.get("final_html"):
        _put(_blob_key(job_id, "html"), "text/html", record["final_html"].encode("utf-8"))
    for r in record.get("rounds", []):
        if r.get("html"):
            _put(_blob_key(job_id, f"round{r['round']}.html"), "text/html", r["html"].encode("utf-8"))
    if status is not None:
        save_status(job_id, status)


def save_status(job_id: str, status: dict) -> None:
    _put(_blob_key(job_id, "status"), "application/json", json.dumps(status).encode("utf-8"))


def load_page(job_id: str, what: str = "html") -> Optional[bytes]:
    return _get(_blob_key(job_id, what))


_running: dict[str, dict] = {}


def start_page_loop(job_id: str, o: dict, packet: dict, *, resume: bool = False, **kw) -> dict:
    if job_id in _running and _running[job_id].get("status") == "running":
        return _running[job_id]
    prior = None
    if resume:
        raw = load_page(job_id, "record")
        try:
            prior = json.loads(raw.decode("utf-8")) if raw else None
        except ValueError:
            prior = None
        for r in (prior or {}).get("rounds") or []:      # the rounds' html is kept apart
            h = load_page(job_id, f"round{r['round']}.html")
            r["html"] = h.decode("utf-8") if h else ""
    state = {"job_id": job_id, "status": "running", "started": time.time(), "rounds_done": len((prior or {}).get("rounds") or []), "error": None, "resumed": bool(prior)}
    _running[job_id] = state
    save_status(job_id, state)

    def _go():
        try:
            partial = {"job_id": job_id, "rounds": list((prior or {}).get("rounds") or []), "cost_usd": (prior or {}).get("cost_usd", 0.0)}
            def on_round(r):
                state["rounds_done"] = r["round"]
                partial["rounds"].append(r); partial["cost_usd"] = round(partial["cost_usd"] + r.get("cost_usd", 0), 4)
                save_page(job_id, partial, status=state)      # every finished round survives a restart
            rec = run_page_loop(job_id, o, packet, on_round=on_round, prior=prior, **kw)
            state.update(status="done", cost_usd=rec["cost_usd"], rounds_done=len(rec["rounds"]))
            save_page(job_id, rec, status=state)
        except Exception as exc:
            logger.exception(f"page loop {job_id} failed")
            state.update(status="failed", error=f"{type(exc).__name__}: {exc}")
            save_status(job_id, state)
    threading.Thread(target=_go, name=f"page-loop-{job_id}", daemon=True).start()
    return state


def page_status(job_id: str) -> Optional[dict]:
    """This process's loop, else the stored status: a stored 'running' with no thread here is a loop a restart killed — `interrupted`,
    resumable with POST /page {resume: true}."""
    st = _running.get(job_id)
    if st is not None:
        return st
    raw = load_page(job_id, "status")
    if not raw:
        return None
    try:
        stored = json.loads(raw.decode("utf-8"))
    except ValueError:
        return None
    if stored.get("status") == "running":
        stored = {**stored, "status": "interrupted", "note": "the API restarted while the loop ran; POST /page {resume: true} continues from the last finished round"}
    return stored


def active_page_loops() -> list[dict]:
    """The loops running in this process, as job-like rows for the jobs listing (a deploy gate that reads statuses sees them: `composing`)."""
    return [{"id": f"page:{jid}", "kind": "page_loop", "job_id": jid, "status": "composing", "step": "page", "rounds_done": st.get("rounds_done"), "started": st.get("started")}
            for jid, st in _running.items() if st.get("status") == "running"]


def recompose_page(job_id: str, o: dict, packet: dict, exhibit_registry=None) -> Optional[dict]:
    """Rebuild the stored page from its record with the current makers and composer (a design change never needs a paid rerun,
    2026-09-07 16:39): the last round's plan, prose and review; the exhibits re-made from the job's rows; the html saved in place."""
    raw = load_page(job_id, "record")
    if not raw:
        return None
    rec = json.loads(raw.decode("utf-8"))
    rounds = rec.get("rounds") or []
    if not rounds:
        return None
    r = rounds[-1]
    plan = json.loads(json.dumps(r["plan"]))   # compose mutates placements
    made = {e["id"]: (make(e["kind"], o, rows=e.get("rows"), packet=packet) or {"html": "", "description": "no maker"}) for e in plan["exhibits"]}
    html, desc = compose_page(rec.get("title") or "", f"{rec.get('audience', '')} · page round {r['round']}", plan, r.get("prose") or {}, made, r.get("review"), r["round"])
    r["html"] = html; r["description"] = desc; rec["final_html"] = html; rec["recomposed"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save_page(job_id, rec)
    return {"job_id": job_id, "round": r["round"], "exhibits": [(e["kind"], e["placement"]) for e in plan["exhibits"]], "chars": len(html)}

