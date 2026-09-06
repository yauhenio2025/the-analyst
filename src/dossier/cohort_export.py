"""The Mastermind job-store adapter for the cohort packet (cohort-packet/v1; Codex's design of 2026-09-06,
`communications/study/cohort_2026_09_06/DESIGN_cohort_dimension_and_synthesis_2026-09-06.md`, "Mastermind job-store adapter
specification").

The Stacks send a cohort table, a plan and pair job ids; the Mastermind assembles the packet from its own job records. This
module exports ONE completed pair job as the generator's normalized envelope `{job_id, author, pair, source_documents}` plus a
receipt (`scripts/build_citation_cohort_fixture_2026_09_06.py` assembles envelopes into a packet and
`scripts/validate_citation_cohort_2026_09_06.py` admits it). Pure: it takes the job record as a dict (the store's or the
API's `model_dump`), the memo markdown and the source texts; `gather_local` fetches those from this instance's stores.

What today's record gives and what it does not: `analysis[phase].final_output` is the engine's assembled reading with its
ledger rows in the answer shape (the retained rows after the critic's rulings were applied); `final_wall` carries the wall's
verdict on those rows (failed anchor ids); the critic's rejected rows are not in the final output and are reported as a gap in
the receipt until the pass outputs are exported too. Every exported row is the exact line of the artifact.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any, Optional

ENGINES = ("citation_engagement_map", "citation_fidelity_audit", "citation_reception_map")
FID = "citation_fidelity_audit"
REC = "citation_reception_map"
FIELD = re.compile(r" — ([a-z][a-z0-9-]*): ")
EVENT_FIELDS = ("ref", "pair-ref", "refs", "passage", "passages", "index-id", "event", "events")
FINDING_REF = re.compile(r"\[((?:[A-Z]\d\.)?F\d+)(?:,[^\]]*)?\]")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def packet_uid(uid: str) -> str:
    """The packet's uid rule (Codex, cohort-packet/v1): a prefix like em: is fine, but no whitespace, `__` or `::`. The
    Stacks' person keys are "surname initial" ("lachmann r"): a space becomes a hyphen; the given form stays in the receipt."""
    u = re.sub(r"\s+", "-", (uid or "").strip())
    return u.replace("__", "-").replace("::", "-")


def fields_of(raw: str) -> dict[str, str]:
    """Every `— name: value` field of an answer-shape row, in order; the head before the first field is the finding."""
    parts = FIELD.split(raw)
    out: dict[str, str] = {}
    for i in range(1, len(parts) - 1, 2):
        out[parts[i]] = parts[i + 1].strip()
    return out


def _strip_quotes(s: str) -> str:
    return s.strip().strip('"“”').strip()


def _event_ids(fields: dict[str, str], known: set[str]) -> list[str]:
    out: list[str] = []
    for name in EVENT_FIELDS:
        v = fields.get(name)
        if not v:
            continue
        for tok in re.split(r"[,;\s]+", v):
            tok = tok.strip("[]()")
            if tok and tok in known and tok not in out:
                out.append(tok)
    return out


def _locus(fields: dict[str, str]) -> dict[str, Any]:
    how = fields.get("how", "").split(",")[0].strip().lower()
    pdf = re.search(r"PDF p(?:p|\.)?\s*\.?\s*(\d+)", fields.get("edition-locus", "") + " " + fields.get("locus", ""), re.I)
    printed = re.search(r"\bp(?:p)?\.\s*(\d+)", fields.get("locus", "") + " " + fields.get("edition-locus", ""))
    return {"printed_page": printed.group(1) if printed else None, "pdf_page": int(pdf.group(1)) if pdf else None,
            "section_uid": None, "section_title": fields.get("section") or None,
            "edition": fields.get("edition-locus") or fields.get("edition") or None,
            "how": how if how in ("page", "section", "search") else None}


def rows_of(final_output: str, *, pair_key: str, engine: str, failed_ids: set[str], known_events: set[str]) -> list[dict]:
    from src.executor.ledger_walls import parse_rows

    lines = {m.group(1): line for line in final_output.splitlines() for m in [re.match(r"^\s*(?:[-*]\s+)?\[((?:[A-Z]\d\.)?F\d+)\]", line)] if m}
    out = []
    for r in parse_rows(final_output):
        raw = lines.get(r.id)
        if raw is None:
            continue
        raw = raw.strip()
        fields = fields_of(raw)
        head = raw.split(" — ", 1)[0]
        claim = re.sub(r"^\s*(?:[-*]\s+)?\[[^\]]+\]\s*", "", head).strip()
        anchors = []
        for i, a in enumerate(r.anchors):
            q = _strip_quotes(a.quote)
            if not q:
                continue
            if q not in raw:                       # keep the exact carried text: re-find it in the raw row
                m = re.search(re.escape(q[:40]), raw)
                q = raw[m.start():m.start() + len(q)] if m else q
            voice = "A" if i == 0 else ("B" if engine == REC else "W")
            anchors.append({"text": q, "source_doc_key": a.doc or r.doc or "", "locus": _locus(fields), "voice": voice})
        own_status = (r.status or "").lower()
        status = "rejected" if own_status in ("rejected", "reject") else "confirmed"
        anchor_status = "failed" if r.id in failed_ids else ("verified" if anchors else "unverifiable")
        if anchor_status == "failed":
            status = "unresolved"
        out.append({"row_id": r.id, "ref": f"{pair_key}::{engine}::{r.id}", "dimension": r.dim or fields.get("dim", ""),
                    "claim": claim, "raw_row": raw, "status": status, "anchor_status": anchor_status, "canonical_ref": None,
                    "event_ids": _event_ids(fields, known_events), "anchors": anchors,
                    "fields": {k: v for k, v in fields.items() if not k.startswith("anchor") and k not in ("doc", "doc-b", "dim")}})
    return out


_QUOTES = "\"'“”‘’«»"


def norm_for_anchor(s: str) -> str:
    """The walls' law for a verbatim quotation, as the packet applies it (stdlib, mirrored in the validator): whitespace
    folded to one space, quotation marks and soft hyphens dropped, a hyphen at a line break closed, dashes unified."""
    s = (s or "").replace("\u00ad", "")
    s = re.sub(r"-\s*\n\s*", "", s)
    s = re.sub(r"[\u2010-\u2015]", "-", s)
    s = "".join(c for c in s if c not in _QUOTES)
    return re.sub(r"\s+", " ", s).strip()


def anchor_refound(text: str, source: str) -> bool:
    return bool(text) and bool(source) and norm_for_anchor(text) in norm_for_anchor(source)


def check_anchors(rows: list[dict], witnesses: dict[str, str]) -> dict:
    """A citable row whose anchor cannot be re-found in its witness under the walls' law is downgraded to
    unresolved/unverifiable (never dropped: the raw row stays; the anchor text stays as the row carried it)."""
    counts = {"checked": 0, "refound": 0, "downgraded": 0}
    def witness(key):
        for k in (key, f"em:{key}", key[3:] if key.startswith("em:") else key):
            if witnesses.get(k):
                return witnesses[k]
        return ""
    for row in rows:
        ok = True
        for a in row["anchors"]:
            counts["checked"] += 1
            if anchor_refound(a["text"], witness(a["source_doc_key"])):
                counts["refound"] += 1
            else:
                ok = False
        if not ok and row["status"] == "confirmed" and row["anchor_status"] == "verified":
            row["status"], row["anchor_status"] = "unresolved", "unverifiable"; counts["downgraded"] += 1
    return counts


def witnesses_for(engine: str, source_texts: dict[str, str], index: Optional[dict]) -> dict[str, str]:
    """The documents exactly as the engine received them: the supplied texts plus the index's witnesses (page windows,
    passage-only citing texts), through the same unpacking the runner uses."""
    from src.sources.citation_evidence import prepare_citation_sources

    documents = dict(source_texts)
    if index:
        documents["__index__"] = json.dumps(index, ensure_ascii=False)
    try:
        wit, _ = prepare_citation_sources(engine, documents)
    except Exception:
        wit = dict(source_texts)
    return wit


def table_markdown(t: dict) -> str:
    cols = t.get("columns") or []
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n" if cols else ""
    body = "\n".join("| " + " | ".join(str((c or {}).get("value", "")) for c in (row.get("cells") or [])) + " |" for row in t.get("rows") or [])
    cap = f"**{t.get('caption', '')}**\n\n" if t.get("caption") else ""
    return cap + head + body + (f"\n\n{t['note']}" if t.get("note") else "")


def export_pair(job: dict, *, author: dict, member_uid: str, memo_markdown: str, source_texts: dict[str, str],
                index: Optional[dict] = None, canonical_uri: str = "") -> dict:
    """One completed pair job → {job_id, author, pair, source_documents, receipt}."""
    if job.get("status") != "done":
        raise ValueError(f"job {job.get('id')} is {job.get('status')}, not done")
    given = {"author_uid": author.get("uid", ""), "member_uid": member_uid}
    author = {**author, "uid": packet_uid(author.get("uid", ""))}
    member_uid = packet_uid(member_uid)
    pair_key = f"{author['uid']}__{member_uid}"
    known_events: set[str] = set()
    for t in (index or {}).get("texts", []) or []:
        for p in t.get("passages", []) or []:
            if p.get("ref_id") is not None:
                known_events.add(str(p["ref_id"]))
    path_engines = [s.get("engine_key") for s in ((job.get("options") or {}).get("path") or {}).get("steps", []) or []]
    analysis = job.get("analysis") or {}
    ledgers, phases = [], []
    witnesses: dict[str, str] = {}
    for pn in sorted(analysis, key=lambda k: float(k)):
        ph = analysis[pn]
        engine = ph.get("engine_key")
        if engine not in ENGINES or any(l["engine_key"] == engine for l in ledgers):
            continue
        text = ph.get("final_output") or ""
        wall = ph.get("final_wall") or {}
        failed = set(wall.get("failed_ids") or [])
        rows = rows_of(text, pair_key=pair_key, engine=engine, failed_ids=failed, known_events=known_events) if text else []
        wit = witnesses_for(engine, source_texts, index)
        for k, v in wit.items():
            witnesses.setdefault(k, v)
        relocation = check_anchors(rows, wit)
        artifact_id = f"{job['id']}:phase:{pn}:final"
        ledger = {"engine_key": engine, "artifact_id": artifact_id, "artifact_sha256": sha(text), "artifact_text": text,
                  "rows": rows, "reviewed_empty": not rows}
        if not rows:
            ledger["empty_reason"] = "no ledger rows in the phase's final output" if text else "phase has no final output"
        ledgers.append(ledger)
        phases.append({"phase_number": ph.get("phase_number", pn), "engine_key": engine, "depth": ph.get("depth", ""),
                       "passes": ph.get("passes", []), "artifact_sha256": sha(text), "wall": wall, "anchor_check": relocation})
    ran = {l["engine_key"] for l in ledgers}
    lens_status = {e: ("run" if e in ran else ("unavailable" if e in path_engines else "not_run")) for e in ENGINES}
    refs_by_id = {row["row_id"]: row["ref"] for l in ledgers for row in l["rows"]}
    tables = []
    for t in job.get("tables") or []:
        md = table_markdown(t)
        cited = [refs_by_id[i] for i in dict.fromkeys(FINDING_REF.findall(md + " " + json.dumps(t.get("rows") or [], ensure_ascii=False))) if i in refs_by_id]
        tables.append({"table_key": t.get("key") or "", "markdown": md, "row_refs": cited})
    docs = [d for d in job.get("documents") or [] if isinstance(d, dict) and d.get("role", "source") == "source"]
    cited = {a["source_doc_key"] for l in ledgers for r in l["rows"] for a in r["anchors"]}
    def witness_of(key):
        for k in (key, f"em:{key}", key[3:] if key.startswith("em:") else key):
            if witnesses.get(k):
                return witnesses[k]
        return None
    source_documents = {}
    for k in sorted(cited | set(source_texts)):
        v = witness_of(k)
        if v:
            source_documents[k] = {"text": v, "sha256": sha(v)}      # under the key the rows cite
    missing_sources = sorted(k for k in cited if k not in source_documents)
    pair = {"pair_key": pair_key, "doc_key": f"pair::{pair_key}", "author_uid": author["uid"], "member_uid": member_uid,
            "fixture_only": False, "ledgers": ledgers, "lens_status": lens_status, "tables": tables,
            "memo": {"markdown": memo_markdown, "canonical_uri": canonical_uri or f"/v1/dossier/jobs/{job['id']}/dossier.md"}}
    gaps = ["the critic's rejected rows are not exported (only the retained rows of the final output; the pass outputs carry the rulings)"]
    if missing_sources:
        gaps.append(f"source texts missing for {missing_sources}")
    if not known_events:
        gaps.append("no evidence index with ref_ids: rows carry no event_ids")
    receipt = {"job_id": job["id"], "status": job.get("status"), "updated_at": job.get("updated_at"), "identities_given": given,
               "analysis_job_id": job.get("analysis_job_id"), "phases": phases, "documents": [d.get("key") for d in docs],
               "totals": job.get("totals"), "exported_at": datetime.now(timezone.utc).isoformat(), "gaps": gaps}
    return {"job_id": job["id"], "author": author, "pair": pair, "source_documents": source_documents, "receipt": receipt}


def gather_local(job_id: str) -> tuple[dict, str, dict[str, str], Optional[dict]]:
    """The job record, its memo markdown, its source texts and its evidence index from this instance's stores."""
    from pathlib import Path

    from src.dossier.store import get_job
    from src.executor.document_store import get_document_text

    job = get_job(job_id)
    if job is None:
        raise ValueError(f"no job {job_id}")
    record = job.model_dump(mode="json")
    md_path = (job.paths or {}).get("md") if getattr(job, "paths", None) else None
    memo = Path(md_path).read_text(encoding="utf-8") if md_path and Path(md_path).exists() else ""
    texts, index = {}, None
    for d in record.get("documents") or []:
        did = d.get("executor_doc_id")
        text = get_document_text(did) if did else None
        if not text:
            continue
        if d.get("role", "source") == "source":
            texts[d["key"]] = text
        elif d.get("role") == "evidence_index" and index is None:
            try:
                index = json.loads(text)
            except ValueError:
                index = None
    return record, memo, texts, index


def gather_remote(base_url: str, job_id: str, timeout: int = 60) -> tuple[dict, str, dict[str, str], Optional[dict]]:
    """The same four things from a live instance's API (the Stacks' pairs run on Render, not here)."""
    import httpx

    base = base_url.rstrip("/")
    with httpx.Client(timeout=timeout) as c:
        record = c.get(f"{base}/v1/dossier/jobs/{job_id}").raise_for_status().json()
        memo = ""
        r = c.get(f"{base}/v1/dossier/jobs/{job_id}/dossier.md")
        if r.status_code == 200:
            memo = r.text
        texts, index = {}, None
        for d in record.get("documents") or []:
            did = d.get("executor_doc_id")
            if not did:
                continue
            r = c.get(f"{base}/v1/executor/documents/{did}")
            if r.status_code != 200:
                continue
            body = r.json()
            text = body.get("text") or body.get("content") or ""
            if not text:
                continue
            if d.get("role", "source") == "source":
                texts[d["key"]] = text
            elif d.get("role") == "evidence_index" and index is None:
                try:
                    index = json.loads(text)
                except ValueError:
                    index = None
    return record, memo, texts, index
