"""Build the Analyst's field-investigation packet from a base packet and a frozen Reporter snapshot, the way the Stacks does.

Used for the end-to-end Tether test: the primary (thinker) rows, bodies, question, scope and prior context come from the saved
packet; the field rows come from a new frozen Reporter collection; the research state is attached. Writes an `analyst-job.json`
the trial tool can load. The mapping mirrors zotero-stacks `app/reporter_collections.py load_collections` and the primary-copy
exclusion in `app/field_investigations.py augment_packet`; `--check-against` verifies it against a packet the Stacks built.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def field_rows_from_snapshot(snapshot: dict) -> dict:
    """{'field': rows, 'collections': [...], 'gaps': [...]} from one snapshot response ({snapshot_id, collection_id, packet_sha256, packet})."""
    ref = {k: snapshot[k] for k in ("snapshot_id", "collection_id", "packet_sha256")}
    packet = snapshot["packet"]
    collection = packet["collection"]
    membership = {"kind": "reporter", **ref, "name": collection["name"], "source_url": collection["source_url"]}
    docs = {d["source_id"]: d for d in packet["documents"]}
    out = {"field": [], "collections": [{**membership, "readiness": packet["readiness"], "discovery_context": packet["discovery_context"],
                                          "interpretation_rules": packet["interpretation_rules"], "analytical_methods": packet.get("analytical_methods", []),
                                          "source_policy": packet.get("source_policy", {}), "institutional_context": packet.get("institutional_context", {})}],
           "gaps": [{"kind": "reporter", "collection_id": ref["collection_id"], "message": gap} for gap in packet["gaps"]]}
    for member in packet["members"]:
        source = docs.get(member["source_id"], member)
        body = source.get("supplied_text", "")
        spans = source.get("spans", [])
        uid = "reporter:" + source["source_id"]
        metadata = {k: v for k, v in source.items() if k not in ("supplied_text", "page_text")}
        metadata.update(provider="reporter", entity_type="source_collection", **ref)
        state = "available" if body else "excluded" if member.get("text_available") else "missing"
        pages = [{"page": s["page"], "start": s["char_start"], "end": s["char_end"]} for s in spans if s.get("page")]
        row = {"uid": uid, "title": source["title"], "authors": source.get("authors", []),
               "year": (source.get("published_at") or "")[:4] or None,
               "body": body, "body_state": state, "body_chars": len(body), "body_sha256": _hash(body), "source_role": "field", "role": "field",
               "source_url": source.get("canonical_url") or source.get("url"), "source_metadata": metadata,
               "page_spans": pages, "passage_spans": spans, "collection_memberships": [membership],
               "selection_reason": "Frozen original source" if body else "Not selected or duplicate evidence" if state == "excluded" else "Original text unavailable; discovery lead only"}
        out["field"].append(row)
        out["gaps"].extend({"kind": "reporter", "uid": uid, "title": row["title"], "body_state": state, "message": gap} for gap in source.get("gaps", []))
    return out


def exclude_primary_copies(field_rows: list[dict], primary: list[dict]) -> list[dict]:
    """A field row that is the thinker's own text (same uid or same body) cannot be independent field testimony."""
    primary_uids = {t["uid"] for t in primary}
    primary_bodies = {t.get("hash") or _hash(t.get("body", "")): t["uid"] for t in primary if t.get("body")}
    out = []
    for raw in field_rows:
        t = dict(raw)
        digest = _hash(t["body"])
        primary_uid = t["uid"] if t["uid"] in primary_uids else primary_bodies.get(digest) if t["body"].strip() else None
        if primary_uid:
            if t["uid"] in primary_uids:
                t.update(record_uid=t["uid"], uid="field-copy:" + t["uid"])
            t.update(primary_uid=primary_uid, body="", page_spans=[], body_state="excluded", body_sha256=_hash(""), body_chars=0,
                     selection_reason="Already represented among the target author's works")
        t["hash"] = _hash(t["body"])
        out.append(t)
    return out


def select_by_bearing(field_rows: list[dict], bearings: list[dict] | None, max_field: int | None) -> list[dict]:
    """Read the sources that bear on an explanation first (supports, then undercuts, then context), within the reading cap; the rest
    stay in the packet as leads with the reason. The Reporter's per-hit bearing is the ranking; nothing here judges relevance."""
    if not max_field:
        return field_rows
    rank = {"supports": 0, "undercuts": 0, "context": 2, None: 3, "": 3}
    by_url = {}
    for h in bearings or []:
        for u in (h.get("url"), h.get("canonical_url")):
            if u:
                by_url[u] = min(by_url.get(u, 9), rank.get(h.get("bearing"), 3))
    available = [r for r in field_rows if r["body_state"] == "available"]
    def key(r):
        urls = [r.get("source_url"), (r.get("source_metadata") or {}).get("url"), (r.get("source_metadata") or {}).get("canonical_url")]
        return (min([by_url.get(u, 3) for u in urls if u] or [3]), -r["body_chars"])
    ordered = sorted(available, key=key)
    keep = {r["uid"] for r in ordered[:max_field]}
    out = []
    for r in field_rows:
        if r["body_state"] == "available" and r["uid"] not in keep:
            r = {**r, "body": "", "body_chars": 0, "body_sha256": _hash(""), "page_spans": [], "body_state": "excluded",
                 "selection_reason": f"Not read under the field reading cap of {max_field}: no supporting or undercutting bearing in discovery; retained as a lead"}
        out.append(r)
    return out


def build(base_packet: dict, snapshot: dict, research_state: dict | None, *, bearings: list[dict] | None = None, max_field: int | None = None) -> dict:
    loaded = field_rows_from_snapshot(snapshot)
    packet = {k: v for k, v in base_packet.items() if k not in ("field", "field_collections", "field_gaps", "reporter_snapshots", "research_state", "research_program")}
    packet["field"] = select_by_bearing(exclude_primary_copies(loaded["field"], base_packet.get("primary") or []), bearings, max_field)
    packet["field_collections"] = loaded["collections"]
    packet["field_gaps"] = loaded["gaps"]
    packet["reporter_snapshots"] = [{k: snapshot[k] for k in ("snapshot_id", "collection_id", "packet_sha256")}]
    packet["method_contract"] = {"key": "field-critical-methods", "version": 1}
    if research_state:
        packet["research_state"] = research_state
    return packet


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base-archive", required=True, type=Path, help="directory with the saved analyst-job.json (primary rows, bodies, question, scope)")
    ap.add_argument("--snapshot", required=True, type=Path, help="snapshot response JSON: {snapshot_id, collection_id, packet_sha256, packet}")
    ap.add_argument("--research-state", type=Path, default=None)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--check-against", type=Path, default=None, help="a packet the Stacks built from the same snapshot: compare the field rows")
    ap.add_argument("--bearings", type=Path, default=None, help="JSON list of the discovery's hits with url/canonical_url/bearing, to read bearing sources first")
    ap.add_argument("--max-field", type=int, default=None, help="how many field bodies to read; the rest stay as leads")
    args = ap.parse_args()
    job = json.loads((args.base_archive / "analyst-job.json").read_text())
    base = json.loads(job["sources"][0]["text"])
    snapshot = json.loads(args.snapshot.read_text())
    rs = json.loads(args.research_state.read_text()) if args.research_state else None
    bearings = json.loads(args.bearings.read_text()) if args.bearings else None
    packet = build(base, snapshot, rs, bearings=bearings, max_field=args.max_field)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "analyst-job.json").write_text(json.dumps({"sources": [{"kind": "paste", "role": "field_investigation", "key": "investigation",
                                                                        "title": f"{base['author']['name']}: {base['question'][:120]}",
                                                                        "text": json.dumps(packet, ensure_ascii=False)}]}, ensure_ascii=False))
    available = [r for r in packet["field"] if r["body_state"] == "available"]
    report = {"field_rows": len(packet["field"]), "available": len(available), "available_chars": sum(r["body_chars"] for r in available),
              "excluded_primary_copies": sum(1 for r in packet["field"] if r.get("primary_uid")), "gaps": len(packet["field_gaps"]),
              "not_read_under_cap": sum(1 for r in packet["field"] if "reading cap" in (r.get("selection_reason") or "")),
              "read_hosts": sorted({(r.get("source_metadata") or {}).get("publication") or "" for r in available})[:40],
              "snapshot": packet["reporter_snapshots"][0], "research_state": bool(rs)}
    if args.check_against:
        other = json.loads(json.loads((args.check_against / "analyst-job.json").read_text())["sources"][0]["text"])
        mine = {r["uid"]: r for r in packet["field"]}
        theirs = {r["uid"]: r for r in other["field"]}
        report["check"] = {"same_uids": set(mine) == set(theirs),
                           "same_available": {u for u, r in mine.items() if r["body_state"] == "available"} == {u for u, r in theirs.items() if r["body_state"] == "available"},
                           "same_body_hashes": all(mine[u]["body_sha256"] == theirs[u]["body_sha256"] for u in mine if u in theirs),
                           "same_states": sum(1 for u in mine if u in theirs and mine[u]["body_state"] == theirs[u]["body_state"]), "of": len(theirs)}
    (args.out / "build-report.json").write_text(json.dumps(report, indent=2, default=str))
    print(json.dumps(report, default=str))


if __name__ == "__main__":
    main()
