"""The readings ledger (Evgeny, 2026-09-07 18:30: "every time we do a massive API call on primary sources and get only some high-level
analysis from it, we should always be saving it and attaching it to this thinker, so that later sessions can skim through it and have a
map of what is where — a bottom-up RAG").

A READING is one engine's rows over primary sources: the job, the phase, the engine, when, the cost, the rows (id · dim · text · anchor ·
doc · locus · the shape fields), the texts read (doc keys and uids), the persons the rows name. The ledger indexes readings by person
(every name a row carries: interlocutor · person · thinker · opponent · cited when a person · author) and by text (every doc key or text
uid a row anchors in or names), written by code the moment a phase or an added step finishes. Durable in the blob store; readable at
GET /v1/readings?person=|text=|job=. Shape only: nothing here judges a row.
"""
from __future__ import annotations

import json
import re
import time
from typing import Any, Iterable, Optional

PERSON_FIELDS = ("interlocutor", "person", "thinker", "opponent", "author", "thinker_name", "person_name")   # never `name`: an agenda's or a school's name is not a person
TEXT_FIELDS = ("text", "ref", "source", "cited_text", "before", "after")
UID = re.compile(r"(em:[A-Za-z0-9]{6,})")


def _put(key: str, mime: str, data: bytes) -> None:
    from src.dossier.blob_store import put_blob_safe
    put_blob_safe(key, mime, data)


def _get(key: str) -> Optional[bytes]:
    from src.dossier.blob_store import get_blob
    got = get_blob(key)
    return got[1] if isinstance(got, tuple) else got


def slug(name: str) -> str:
    """'North, Douglass C.' → 'north-douglass-c'; 'Hintze' → 'hintze'."""
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").lower().replace("ʼ", "").replace("’", "")).strip("-")
    return s[:80]


def surname(name: str) -> str:
    n = (name or "").strip()
    return (n.split(",", 1)[0] if "," in n else n.split()[-1] if n.split() else n).strip().lower()


def _is_name(v: str) -> bool:
    """A person's name, not a list, a phrase or an id: at most five words and one comma, no 'and', not a uid or a row id."""
    v = (v or "").strip()
    if not v or len(v) > 60 or v.startswith("em:") or re.match(r"^[A-Z]\d\.F\d+$", v):
        return False
    if v.count(",") > 1 or len(v.split()) > 5 or re.search(r"\b(and|or|of the|the)\b", v.lower()):
        return False
    return v.lower() not in ("none", "unknown", "")


def persons_of(fields: dict, row_text: str = "") -> set[str]:
    out = set()
    for k in PERSON_FIELDS:
        v = (fields.get(k) or "").strip()
        if _is_name(v):
            out.add(v)
    if (fields.get("kind") or "").lower() == "person" and _is_name(fields.get("cited") or ""):
        out.add(fields["cited"].strip())
    for k in ("candidates", "interlocutors"):
        for part in re.split(r"[;|]", fields.get(k) or ""):
            if _is_name(part):
                out.add(part.strip())
    return out


def texts_of(fields: dict, doc: str = "") -> set[str]:
    out = set()
    for m in UID.finditer(doc or ""):
        out.add(m.group(1))
    for k in TEXT_FIELDS:
        for m in UID.finditer(str(fields.get(k) or "")):
            out.add(m.group(1))
    return out


def reading_from_phase(job: dict, phase_key: str, phase: dict) -> Optional[dict]:
    """One phase → one reading, or None when the phase has no rows."""
    from src.dossier.explainer import rows_with_fields
    engine = phase.get("engine_key")
    out = phase.get("final_output") or ""
    if not engine or not out:
        return None
    failed = set((phase.get("final_wall") or {}).get("failed_ids") or [])
    rows = rows_with_fields(out, failed, engine_key=engine)
    if not rows:
        return None
    persons: dict[str, int] = {}; texts: dict[str, int] = {}
    slim = []
    for r in rows:
        f = r["fields"]
        for p in persons_of(f, r["text"]):
            persons[p] = persons.get(p, 0) + 1
        for t in texts_of(f, r.get("doc", "")):
            texts[t] = texts.get(t, 0) + 1
        slim.append({"id": r["id"], "dim": r["dim"], "text": r["text"][:400], "anchor": (r.get("anchor") or "")[:240], "doc": r.get("doc", ""), "locus": f.get("locus", ""),
                     "conjecture": r["conjecture"], "fields": {k: v for k, v in f.items() if k not in ("anchor", "doc", "dim") and len(str(v)) < 300}})
    for a in job_authors(job):   # the run's author (the oeuvre packet's author) is indexed under the person too (the Stacks, 2026-09-07 19:30)
        persons[a] = persons.get(a, 0) + 100
    when = _stamp(phase.get("finished") or job.get("updated_at") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    return {"job_id": job.get("id"), "phase": str(phase_key), "engine": engine, "when": when, "cost_usd": phase.get("cost_usd"), "depth": phase.get("depth"),
            "intent": (job.get("options") or {}).get("intent", "")[:300], "rows": slim, "n_rows": len(slim), "n_conjectural": sum(1 for r in slim if r["conjecture"]),
            "persons": sorted(persons, key=lambda p: -persons[p]), "texts": sorted(texts, key=lambda t: -texts[t]),
            "sources": [s.key if hasattr(s, "key") else s for s in (phase.get("sources") or [])], "renders": _renders(engine, job.get("id"))}


def _stamp(when: str) -> str:
    """A naive stamp is the desk's UTC clock: say so with a Z (the Stacks read a naive one as local and put a job in the future)."""
    w = str(when or "")
    return w if (w.endswith("Z") or re.search(r"[+-]\d\d:\d\d$", w) or not w) else w + "Z"


def name_from_author_id(aid: str) -> str:
    """'brenner-robert' → 'Brenner, Robert' (the Stacks' author id is surname-given, hyphenated)."""
    parts = [x for x in aid.split("-") if x]
    if len(parts) < 2:
        return aid
    return f"{parts[0].capitalize()}, {' '.join(x.capitalize() for x in parts[1:])}"


def job_authors(job: dict) -> list[str]:
    """The author(s) a run is about: the oeuvre packet's author.name (the plan document), else the packet a caller kept on the job."""
    import json as _json, os
    names: list[str] = []
    pk = job.get("packet") if isinstance(job.get("packet"), dict) else None
    if pk and isinstance(pk.get("author"), dict):
        if pk["author"].get("name"):
            names.append(pk["author"]["name"])
        elif pk["author"].get("id"):
            names.append(name_from_author_id(str(pk["author"]["id"])))
    if not names:
        try:
            from src.executor.document_store import get_document_text
            for d in job.get("documents") or []:
                if d.get("role") == "plan" and d.get("executor_doc_id"):
                    obj = _json.loads(get_document_text(d["executor_doc_id"]) or "{}")
                    a = obj.get("author")
                    if isinstance(a, dict) and a.get("name"):
                        names.append(a["name"])
                    elif isinstance(a, dict) and a.get("id"):
                        names.append(name_from_author_id(str(a["id"])))     # the Stacks' author ids are surname-given ("brenner-robert")
                    elif isinstance(a, str) and a:
                        names.append(name_from_author_id(a) if re.match(r"^[a-z]+(-[a-z]+)+$", a) else a)
        except Exception:
            pass
    return names


PUBLIC_BASE = __import__("os").environ.get("PUBLIC_BASE_URL", "https://the-analyst-kcuc.onrender.com").rstrip("/")


def _renders(engine: str, job_id: Optional[str]) -> list[str]:
    base = f"{PUBLIC_BASE}/v1/dossier/jobs/{job_id}"   # absolute: a render may live on another host one day (the Stacks, 19:30)
    if engine in ("oeuvre_trajectory", "citation_shift", "retrospective_reading", "prospective_reading", "epistemic_rupture", "oeuvre_position_memo", "thinker_placement"):
        return [f"{base}/oeuvre", f"{base}/page"]
    if engine in ("interlocutor_position", "distinction_draft", "distinction_settle", "impact_scan"):
        return [f"{base}/distinctions"]
    if engine in ("encounter_map", "encounter_draft"):
        return [f"{base}/encounter", f"{base}/encounter/page"]
    if engine == "reference_reread":
        return [f"{base}/reread"]
    return [f"{base}/ledger"]


def _index_key(kind: str, value: str) -> str:
    return f"readings:{kind}:{slug(value) if kind == 'person' else value}"


def _load_list(key: str) -> list[dict]:
    raw = _get(key)
    if not raw:
        return []
    try:
        return json.loads(raw.decode("utf-8"))
    except ValueError:
        return []


def _entry(reading: dict) -> dict:
    return {"job_id": reading["job_id"], "phase": reading["phase"], "engine": reading["engine"], "when": reading["when"], "n_rows": reading["n_rows"],
            "cost_usd": reading.get("cost_usd"), "renders": reading["renders"], "intent": reading.get("intent", "")}


def save_reading(reading: dict, *, strict: bool = False) -> None:
    """The reading itself, and its entry on every person's and text's index (replacing an earlier entry for the same job and phase)."""
    if not strict:
        _save_reading(reading, _put, _get)
        return
    # External imports acknowledge durable reading/index writes together. Serialise
    # their read/modify/write operations so concurrent receipts do not lose entries.
    from src.dossier.blob_store import _bin, ensure_table
    from src.executor.db import _is_postgres, get_connection
    ensure_table()
    postgres = _is_postgres()
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            if postgres:
                cursor.execute("SELECT pg_advisory_xact_lock(hashtext('readings-ledger-index'))")
            else:
                cursor.execute("BEGIN IMMEDIATE")

            def run(sql, values):
                cursor.execute(sql if postgres else sql.replace("%s", "?"), values)

            def get(key):
                run("SELECT data FROM dossier_blobs WHERE blob_key=%s", (key,))
                row = cursor.fetchone()
                return bytes(row[0]) if row else None

            def put(key, mime, data):
                run("INSERT INTO dossier_blobs (blob_key,mime,size,data,created_at) VALUES (%s,%s,%s,%s,%s) "
                    "ON CONFLICT (blob_key) DO UPDATE SET mime=EXCLUDED.mime,size=EXCLUDED.size,"
                    "data=EXCLUDED.data,created_at=EXCLUDED.created_at",
                    (key, mime, len(data), _bin(data), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))

            _save_reading(reading, put, get)
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def _save_reading(reading: dict, put, get) -> None:
    def load_list(key):
        raw = get(key)
        if not raw:
            return []
        try:
            return json.loads(raw.decode("utf-8"))
        except ValueError:
            return []

    put(f"reading:{reading['job_id']}:{reading['phase']}", "application/json", json.dumps(reading, ensure_ascii=False).encode("utf-8"))
    entry = _entry(reading)
    for kind, values in (("person", reading["persons"]), ("text", reading["texts"])):
        for v in values:
            key = _index_key(kind, v)
            lst = [e for e in load_list(key) if not (e["job_id"] == entry["job_id"] and e["phase"] == entry["phase"])]
            lst.append({**entry, "name": v} if kind == "person" else entry)
            put(key, "application/json", json.dumps(lst[-400:], ensure_ascii=False).encode("utf-8"))
    for v in reading["persons"]:
        sk = f"readings:surname:{surname(v)}"
        lst = [e for e in load_list(sk) if not (e["job_id"] == entry["job_id"] and e["phase"] == entry["phase"] and e.get("name") == v)]
        lst.append({**entry, "name": v}); put(sk, "application/json", json.dumps(lst[-400:], ensure_ascii=False).encode("utf-8"))
    jobs = [e for e in load_list(f"readings:job:{reading['job_id']}") if e["phase"] != entry["phase"]] + [entry]
    put(f"readings:job:{reading['job_id']}", "application/json", json.dumps(jobs, ensure_ascii=False).encode("utf-8"))


def index_job(job: dict, only_phases: Optional[Iterable[str]] = None) -> list[dict]:
    """Every phase with rows (or the named phases) → readings saved and indexed. Returns the readings' entries."""
    out = []
    for k, ph in (job.get("analysis") or {}).items():
        if only_phases is not None and str(k) not in {str(x) for x in only_phases}:
            continue
        r = reading_from_phase(job, k, ph)
        if r:
            save_reading(r); out.append(_entry(r))
    return out


def readings_for(person: Optional[str] = None, text: Optional[str] = None, job: Optional[str] = None, limit: int = 50) -> dict:
    """The index entries for a person (by slug, with a surname fallback), a text uid, or a job; `full=` fetches the readings."""
    entries: list[dict] = []
    if person:
        entries = _load_list(_index_key("person", person))
        if len(person.split()) == 1 and "," not in person:   # a bare surname gathers every form: 'Brenner' and 'Brenner, Robert' alike
            seen = {(e["job_id"], e["phase"]) for e in entries}
            entries = entries + [e for e in _load_list(f"readings:surname:{surname(person)}") if (e["job_id"], e["phase"]) not in seen]
    elif text:
        m = UID.search(text or "")
        entries = _load_list(_index_key("text", m.group(1) if m else text))
    elif job:
        entries = _load_list(f"readings:job:{job}")
    entries = sorted(entries, key=lambda e: e.get("when", ""), reverse=True)[:limit]
    return {"person": person, "text": text, "job": job, "readings": entries, "count": len(entries)}


def reading(job_id: str, phase: str) -> Optional[dict]:
    raw = _get(f"reading:{job_id}:{phase}")
    result = json.loads(raw.decode("utf-8")) if raw else None
    if result and str(result.get("receipt_id", "")).startswith("inquiry-"):
        # Feedback events are authoritative. A concurrent receipt-index refresh
        # can retain an older snapshot, but readers must always see every event.
        from src.inquiries.service import feedback_for
        result["author_feedback"] = feedback_for(result["receipt_id"])
    return result


def prior_block(persons: Iterable[str] = (), texts: Iterable[str] = (), limit: int = 12) -> Optional[dict]:
    """What a planner reads before it spends: the readings already made about these persons and texts (entries, not rows)."""
    seen = {}
    for p in persons:
        for e in readings_for(person=p)["readings"]:
            seen[(e["job_id"], e["phase"])] = {**e, "about": p}
    for t in texts:
        for e in readings_for(text=t)["readings"]:
            seen.setdefault((e["job_id"], e["phase"]), {**e, "about": t})
    if not seen:
        return None
    lst = sorted(seen.values(), key=lambda e: e.get("when", ""), reverse=True)[:limit]
    return {"note": "readings already made about these persons and texts: read them (GET /v1/readings?job=<job_id>) before reading the texts again; cite their rows by job and id; read only what is new", "readings": lst}
