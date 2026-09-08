"""Durable question-led research, with method records and source-bounded retrieval.

The engines judge questions, relevance and meaning. This executor searches literal
queries, follows canonical cited-work identities, enforces budgets, verifies
primary quotes and checkpoints artifacts. No research interpretation lives here.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Callable

from src.sources.schemas import SourceSpec

CHAIN = "author_investigation"


def _json(obj):
    return json.dumps(obj, ensure_ascii=False)


def _now():
    return datetime.now(timezone.utc).isoformat()


def _spec(key, text, title=""):
    return SourceSpec(kind="paste", key=key, title=title or key, text=text)


def _field(row, name, default=""):
    return (row.get("fields") or {}).get(name, default)


def _queries(rows):
    seen = set()
    out = []
    for row in rows:
        term = str(_field(row, "query")).strip().strip('"')
        if 2 <= len(term) <= 120 and term.casefold() not in seen:
            seen.add(term.casefold())
            out.append(term)
    return out[:48]


def _eligible(row):
    return row.get("date_scope") != "outside_range" and row.get("body_state") != "excluded"


def search_inventory(primary, bodies, queries):
    """All supplied text is searched; counts are complete, saved hits are bounded."""
    searches = []
    for row in primary:
        body = bodies.get(row["source_key"], "")
        terms = []
        for query in queries:
            hits = []
            count = 0
            if body and _eligible(row):
                for match in re.finditer(re.escape(query), body, re.IGNORECASE):
                    count += 1
                    if len(hits) < 12:
                        lo, hi = max(0, match.start() - 350), min(len(body), match.end() + 700)
                        hits.append({"start": match.start(), "end": match.end(), "context_start": lo,
                                     "context_end": hi, "context": body[lo:hi]})
            if count:
                terms.append({"query": query, "count": count, "hits": hits, "saved_hits": len(hits)})
        searches.append({"uid": row["uid"], "source_key": row["source_key"],
                         "searched_chars": len(body) if _eligible(row) else 0,
                         "state": "searched" if body and _eligible(row) else row.get("body_state", "missing"),
                         "queries_checked": len(queries) if body and _eligible(row) else 0,
                         "matches": terms, "match_count": sum(t["count"] for t in terms)})
    return searches


def citation_paths(primary, searches, queries, seed_uids=()):
    """One bounded hop by canonical work key; relevance stays a model judgment."""
    seeds = set(seed_uids) | {s["uid"] for s in searches if s["match_count"]}
    works = {}
    for row in primary:
        for ref in row.get("citations") or []:
            key = ref.get("key") or ref.get("work_key")
            if key:
                target = works.setdefault(str(key), {}).setdefault(row["uid"], {"row": row, "refs": []})
                target["refs"].append(ref)
    paths = []
    for key, targets in works.items():
        relevant = [uid for uid, t in targets.items() if uid in seeds or
                    any(q.casefold() in _json(t["refs"]).casefold() for q in queries)]
        if not relevant:
            continue
        for uid, target in targets.items():
            refs = target["refs"]
            paths.append({"work_key": key, "from_uids": sorted(relevant), "to_uid": uid,
                          "citation": refs[0], "citation_count": len(refs), "citation_ref_ids": [r.get("ref_id") for r in refs],
                          "basis": "shared_canonical_work", "substantive_relevance": "unjudged"})
    return paths


def citation_catalog(refs):
    """One bibliographic identity per cited work; full event contexts stay frozen."""
    by_key = {}
    for ref in refs:
        key = ref.get("key") or ref.get("work_key") or _json([ref.get("title"), ref.get("authors"), ref.get("year")])
        item = by_key.setdefault(str(key), {k: ref.get(k) for k in ("key", "work_key", "title", "authors", "year", "held_uid", "referee_paper_id")})
        item["citation_count"] = item.get("citation_count", 0) + 1
    return list(by_key.values())


def inspected_ranges(body, search, cap, extra_queries=()):
    """Whole text when it fits; otherwise source-exact, disjoint contextual windows."""
    if len(body) <= cap:
        return [(0, len(body))] if body else []
    centers = [h["start"] for m in search.get("matches", []) for h in m["hits"]]
    for query in extra_queries:
        if len(query.strip()) < 2:
            continue
        centers.extend(m.start() for m in list(re.finditer(re.escape(query.strip()), body, re.IGNORECASE))[:8])
    # Title and conclusion plus middle coverage also allow semantic-only candidates.
    centers += [0, len(body) - 1, len(body) // 2]
    chosen = []
    for center in centers:
        start, end = max(0, center - 1800), min(len(body), center + 3200)
        proposed = sorted(chosen + [(start, end)])
        merged = []
        for lo, hi in proposed:
            if merged and lo <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
            else:
                merged.append((lo, hi))
        if sum(hi - lo for lo, hi in merged) <= cap:
            chosen = merged
    return chosen


def _excerpt(body, ranges):
    return "\n\n".join(f"[SOURCE CHARACTERS {lo}:{hi}]\n{body[lo:hi]}" for lo, hi in ranges)


def _context(packet, bodies, cap=50000, queries=()):
    """Catalogue every prior source; search full bodies, then supply explicit windows."""
    entries = []
    for row in packet.get("secondary") or []:
        key = row["source_key"]
        entries.append({"key": key, "kind": row.get("kind", "secondary"),
                        "text": bodies.get(key, ""), "uid": row["uid"], "title": row.get("title")})
    for kind in ("prior_readings", "prior_investigations", "referee"):
        entries.append({"key": kind, "kind": kind, "text": _json(packet.get(kind) or []), "title": kind})
    for prior in packet.get("resolved_prior_readings") or []:
        entries.append({"key": f"reading:{prior.get('job_id')}:{prior.get('phase')}", "kind": "prior_reading",
                        "title": prior.get("intent") or prior.get("engine") or "Prior source reading", "text": _json(prior)})
    for entry in entries:
        value = entry["text"]
        positions, matched, count = [], [], 0
        for query in queries:
            found = list(re.finditer(re.escape(query), value, re.IGNORECASE))
            if found:
                matched.append(query)
                count += len(found)
                positions.extend(m.start() for m in found[:2])
        entry.update(total_chars=len(value), searched_chars=len(value) if queries else 0,
                     matched_queries=matched, hit_count=count, _positions=positions)
    if queries:
        ranked = sorted(entries, key=lambda e: (-len(e["matched_queries"]), -min(e["hit_count"], 15), e["key"]))
        chosen = set([e["key"] for e in ranked if e["matched_queries"]][:30])
        chosen.update(("prior_readings", "prior_investigations", "referee"))
    else:
        chosen = {e["key"] for e in entries}
    per = max(1, cap // max(1, len(chosen)))
    for entry in entries:
        value, positions = entry.pop("text"), entry.pop("_positions")
        ranges = []
        if entry["key"] in chosen and value:
            if len(value) <= per:
                ranges = [(0, len(value))]
            elif positions:
                width = per // min(3, len(positions))
                for pos in positions[:3]:
                    start = max(0, pos - width // 3)
                    ranges.append((start, min(len(value), start + width)))
                ranges = sorted(ranges)
                merged = []
                for start, end in ranges:
                    if merged and start <= merged[-1][1]:
                        merged[-1] = (merged[-1][0], max(merged[-1][1], end))
                    else:
                        merged.append((start, end))
                ranges = merged
            else:
                ranges = [(0, per)]
        supplied = sum(hi - lo for lo, hi in ranges)
        entry.update(supplied_chars=supplied, inspected_ranges=ranges, truncated=supplied < len(value),
                     text=_excerpt(value, ranges), selected_for_context=entry["key"] in chosen)
    return entries


def hydrate_prior_readings(packet, *, lookup_index, lookup_reading):
    """Resolve supplied job/phase ids to actual saved rows before freezing context."""
    packet = dict(packet)
    resolved, manifest, seen = [], [], set()
    inputs = packet.get("prior_readings") or []
    if isinstance(inputs, dict):
        inputs = inputs.get("readings") or inputs.get("jobs") or []
    for entry in inputs:
        if isinstance(entry, dict) and entry.get("rows") is not None:
            resolved.append(entry)
            manifest.append({"job_id": entry.get("job_id"), "phase": entry.get("phase"), "status": "supplied_rows"})
            continue
        job_id = entry if isinstance(entry, str) else entry.get("job_id") if isinstance(entry, dict) else None
        if not job_id:
            continue
        try:
            entries = [entry] if isinstance(entry, dict) and entry.get("phase") is not None else lookup_index(job=job_id, limit=400).get("readings", [])
            if not entries:
                manifest.append({"job_id": job_id, "status": "no_indexed_rows"})
            for ref in entries:
                phase = str(ref.get("phase", ""))
                identity = (job_id, phase)
                if identity in seen:
                    continue
                seen.add(identity)
                found = lookup_reading(job_id, phase)
                manifest.append({"job_id": job_id, "phase": phase, "status": "resolved" if found else "missing_rows"})
                if found:
                    resolved.append(found)
        except Exception as exc:
            manifest.append({"job_id": job_id, "status": "unavailable", "error_kind": type(exc).__name__})
    packet["resolved_prior_readings"] = resolved
    packet["prior_readings_resolution"] = manifest
    return packet


def run_investigation(packet: dict, bodies: dict, *, call: Callable, save: Callable,
                      state: dict | None = None, check: Callable = lambda: None,
                      spend_cap_usd: float = 8.0) -> dict:
    """Resume from any completed model or deterministic checkpoint without paid repetition."""
    primary = packet["primary"]
    by_uid = {r["uid"]: r for r in primary}
    context = _context(packet, bodies)
    fingerprint = hashlib.sha256(_json(packet).encode()).hexdigest()
    state = state or {"version": 1, "kind": CHAIN, "packet_sha256": fingerprint,
                      "author": packet["author"], "question": packet["question"], "scope": packet.get("scope", {}),
                      "inventory": primary, "context_manifest": [{k: v for k, v in r.items() if k != "text"} for r in context],
                      "prior_readings_resolution": packet.get("prior_readings_resolution", []),
                      "stages": [], "calls": {}, "analysis": {}, "cost_usd": 0.0, "evidence": [], "readings": []}
    if state.get("packet_sha256") != fingerprint:
        raise ValueError("the frozen investigation packet changed; create a new run")

    def checkpoint(stage, **fields):
        state.update(fields, updated_at=_now(), current_stage=stage)
        state.setdefault("stage_status", {})[stage] = "running" if state.get("running_stage") == stage else "complete"
        if stage not in state["stages"]:
            state["stages"].append(stage)
        save(state)

    def engine(stage, key, sources, upstream):
        check()
        if stage in state["calls"]:
            return state["calls"][stage]
        remaining = spend_cap_usd - state["cost_usd"]
        if remaining <= 0:
            checkpoint(stage, paused_reason="spend_cap")
            raise ValueError("investigation spend cap reached; completed artifacts were saved")
        checkpoint(stage, running_stage=stage)
        result = call(key, sources, packet=upstream, depth="surface", spend_cap_usd=remaining, max_chars=650000)
        state["calls"][stage] = result
        state["cost_usd"] += float(result.get("cost_usd") or 0)
        phase_key = str(len(state["analysis"]) + 1)
        state["analysis"][phase_key] = {"phase_number": int(phase_key), "stage": stage, "engine_key": key, "depth": "surface", "final_output": result.get("final_output", ""),
                                    "final_wall": result.get("wall", {}), "cost_usd": result.get("cost_usd"),
                                    "sources": [s.key for s in sources], "finished": _now(), "calls": result.get("calls", [])}
        checkpoint(stage, running_stage=None)
        return result

    common = {"author": packet["author"], "question": packet["question"], "scope": packet.get("scope", {}),
              "as_of": packet.get("created") or packet.get("created_at") or state.setdefault("as_of", _now())}
    summary = [{"uid": r["uid"], "title": r.get("title"), "year": r.get("year"), "date_scope": r.get("date_scope"),
                "profile": _json(r.get("profile") or {})[:1200], "profile_summary_truncated": len(_json(r.get("profile") or {})) > 1200}
               for r in primary]
    plan = engine("plan", "author_investigation_plan", [_spec("investigation-question", _json(common)),
                  _spec("investigation-inventory", _json(summary)), _spec("prior-context", _json(context))], common)
    queries = _queries(plan.get("rows") or [])
    if not queries:
        checkpoint("plan", plan=plan, queries=[], paused_reason="planner_returned_no_queries")
        raise ValueError("investigation planner returned no valid literal search queries; its output was saved")
    context = _context(packet, bodies, queries=queries)
    if "searches" not in state:
        searches = search_inventory(primary, bodies, queries)
        checkpoint("search", plan=plan, queries=queries, searches=searches,
                   context_manifest=[{k: v for k, v in r.items() if k != "text"} for r in context],
                   citation_paths=citation_paths(primary, searches, queries))
    # The planner saw the complete catalog; later engines receive the selected
    # relevant windows. All searched/unselected sources remain in the manifest.
    context = [c for c in context if c["selected_for_context"]]
    search_by = {r["uid"]: r for r in state["searches"]}
    # All profiles enter semantic triage, including lexical misses and missing bodies.
    batches, batch, chars = [], [], 0
    for row in primary:
        search = search_by[row["uid"]]
        # Discovery artifacts stay complete in state; avoid repeating hundreds of
        # overlapping hit windows and full citation contexts in the triage call.
        windows = [h for m in search["matches"] for h in m["hits"][:1]][:12]
        paths = [p for p in state["citation_paths"] if p["to_uid"] == row["uid"]]
        refs = row.get("citations") or []
        item = {"inventory": {**row, "citations": citation_catalog(refs)},
                "search": {**{k: v for k, v in search.items() if k != "matches"},
                           "matches": [{"query": m["query"], "count": m["count"]} for m in search["matches"]],
                           "context_windows": windows, "context_windows_supplied": len(windows)},
                "citation_paths": [{k: p[k] for k in ("work_key", "from_uids", "to_uid")} for p in paths],
                "citation_contexts_in_frozen_packet": True}
        size = len(_json(item))
        if batch and (chars + size > 230000 or len(batch) >= 20):
            batches.append(batch); batch, chars = [], 0
        batch.append(item); chars += size
    if batch:
        batches.append(batch)
    decisions = {}
    for i, batch in enumerate(batches):
        result = engine(f"triage:{i + 1}", "author_investigation_triage",
                        [_spec("inventory-batch", _json(batch)), _spec("prior-context", _json(context))],
                        {**common, "plan": plan.get("final_output"), "queries": queries})
        allowed = {r["inventory"]["uid"] for r in batch}
        for row in result.get("rows") or []:
            uid = str(_field(row, "uid"))
            if uid in allowed and _field(row, "decision") in ("read", "context", "defer", "unavailable"):
                decisions[uid] = {**row, "uid": uid, "decision": _field(row, "decision"), "reason": _field(row, "reason")}
        checkpoint("triage", triage=list(decisions.values()))
    # Omitted decisions are disclosed, and supplied omitted texts receive a bounded fallback reading.
    for row in primary:
        if row["uid"] not in decisions:
            decisions[row["uid"]] = {"uid": row["uid"], "decision": "read" if bodies.get(row["source_key"]) and _eligible(row) else "unavailable",
                                      "reason": "No valid triage row returned; unresolved candidate retained", "fields": {"priority": "5"}, "triage_missing": True}
    selection_inventory = [{"inventory": {k: row.get(k) for k in ("uid", "title", "year", "date_scope", "body_state", "body_chars")},
                            "prior_decision": decisions[row["uid"]]} for row in primary]
    reconciliation = engine("triage-selection", "author_investigation_triage",
                            [_spec("inventory-selection", _json(selection_inventory))],
                            {**common, "plan": plan.get("final_output"), "selection_mode": "reconcile",
                             "limits": packet.get("limits") or {"max_read_texts": 12, "max_primary_chars": 240000}})
    for row in reconciliation.get("rows") or []:
        uid = str(_field(row, "uid"))
        if uid in decisions and _field(row, "decision") in ("read", "context", "defer", "unavailable"):
            decisions[uid] = {**row, "uid": uid, "decision": _field(row, "decision"), "reason": _field(row, "reason"),
                              "prior_decision": decisions[uid]}
    def priority(r):
        try:
            p = max(1, min(5, int(_field(r, "priority", "5"))))
        except ValueError:
            p = 5
        return (p, r["uid"])
    candidates = sorted([r for r in decisions.values() if r["decision"] in ("read", "context")
                         and bodies.get(by_uid[r["uid"]]["source_key"]) and _eligible(by_uid[r["uid"]])], key=priority)
    limits = packet.get("limits") or {}
    max_texts = max(1, min(40, int(limits.get("max_read_texts", 12))))
    max_chars = max(5000, min(480000, int(limits.get("max_primary_chars", 240000))))
    checkpoint("triage", triage=list(decisions.values()),
               citation_paths=citation_paths(primary, state["searches"], queries, [r["uid"] for r in candidates]))
    read_sources, readings, evidence = [], [], []
    consumed = 0
    selected = candidates
    followups = []
    processed = set()
    for candidate_index, candidate in enumerate(selected):
        if len(readings) >= max_texts:
            break
        uid = candidate["uid"]; row = by_uid[uid]; body = bodies[row["source_key"]]
        processed.add(uid)
        remaining = max_chars - consumed
        if remaining < 5000 and len(body) > remaining:
            continue
        remaining_slots = min(max_texts - len(readings), len(selected) - candidate_index)
        allocation = min(60000, remaining // max(1, remaining_slots))
        ranges = inspected_ranges(body, search_by[uid], allocation,
                                  str(_field(candidate, "queries")).split(";"))
        if not ranges:
            continue
        consumed += sum(hi - lo for lo, hi in ranges)
        src = _spec(row["source_key"], _excerpt(body, ranges), row.get("title", uid))
        read_sources.append(src)
        coverage = {"uid": uid, "source_key": row["source_key"], "title": row.get("title"), "year": row.get("year"),
                    "body_sha256": row["body_sha256"], "read_uid": row.get("read_uid"), "date_scope": row.get("date_scope"),
                    "body_chars": len(body), "inspected_chars": sum(hi - lo for lo, hi in ranges), "inspected_ranges": ranges,
                    "reading_mode": "full" if ranges == [(0, len(body))] else "windows"}
        source_metadata = {k: row.get(k) for k in ("bibliographic", "roles", "role", "creators_short", "attribution_required",
                           "profile_provenance", "selection_reason", "selection_status", "chapter_of", "type", "work_id") if k in row}
        coverage["source_metadata"] = source_metadata
        result = engine(f"read:{uid}", "author_investigation_read", [src],
                        {**common, "plan": plan.get("final_output"), "selection": candidate, "coverage": coverage,
                         "profile_as_lead": row.get("profile"), "citations": citation_catalog(row.get("citations", [])),
                         "citation_event_contexts": [ref for ref in row.get("citations", [])
                             if any(str(ref.get(k) or "") and str(ref.get(k)) in src.text for k in ("context", "raw"))][:40],
                         "full_citation_events_in_frozen_packet": len(row.get("citations", [])), "prior_context": context})
        cited_keys = {str(c.get("key") or c.get("work_key")) for c in row.get("citations") or []}
        for lead in result.get("rows") or []:
            work_key = str(_field(lead, "work_key"))
            if lead.get("dim") != "citation_lead" or work_key not in cited_keys:
                continue
            targets = [r for r in primary if any(str(c.get("key") or c.get("work_key")) == work_key
                       for c in r.get("citations") or []) and r["uid"] != uid]
            for target in targets:
                followups.append({"from_uid": uid, "to_uid": target["uid"], "work_key": work_key,
                                  "finding_id": lead.get("id"), "reason": _field(lead, "reason"),
                                  "basis": "close_reading_citation_lead"})
                if target["uid"] not in processed and bodies.get(target["source_key"]) and _eligible(target):
                    existing = next((i for i, c in enumerate(candidates) if c["uid"] == target["uid"]), None)
                    if existing is not None:
                        candidates.pop(existing)
                    # A lead judged useful by a completed reading takes the next
                    # slot, before lower-priority inventory candidates consume it.
                    candidates.insert(candidate_index + 1, {"uid": target["uid"], "decision": "read", "reason": _field(lead, "reason"),
                                       "fields": {"priority": "3"}, "discovered_from": uid, "work_key": work_key})
        readings.append({**coverage, "reading": result.get("prose", ""), "rows": result.get("rows", [])})
        for r in result.get("rows") or []:
            if r.get("dim") != "evidence":
                continue
            quote = str(r.get("anchor") or "")
            positions = [m.start() for m in re.finditer(re.escape(quote), body)] if quote else []
            verified_positions = [pos for pos in positions if any(lo <= pos and pos + len(quote) <= hi for lo, hi in ranges)]
            verified = bool(verified_positions) and r.get("doc") == src.key and _field(r, "uid") == uid
            evidence.append({**r, "uid": uid, "source_key": src.key, "title": row.get("title"), "year": row.get("year"),
                             "source_role": "primary", "date_scope": row.get("date_scope"), "source_metadata": source_metadata,
                             "quote": quote, "quote_verified": verified, "anchor_verified": verified,
                             "quote_start": verified_positions[0] if verified else None,
                             "read_uid": row.get("read_uid"), "body_sha256": row["body_sha256"],
                             "citation_id": f"{uid}/{r.get('id', '')}", "conjecture": not verified})
        checkpoint("reading", readings=readings, evidence=evidence, citation_followups=followups)
    read_uids = {r["uid"] for r in readings}
    coverage = {"inventory_count": len(primary), "searchable_count": sum(bool(s["searched_chars"]) for s in state["searches"]),
                "read_count": len(readings), "full_read_count": sum(r["reading_mode"] == "full" for r in readings),
                "window_read_count": sum(r["reading_mode"] == "windows" for r in readings), "inspected_chars": consumed,
                "missing_uids": [r["uid"] for r in primary if not bodies.get(r["source_key"]) and _eligible(r)],
                "excluded_uids": [r["uid"] for r in primary if not _eligible(r)],
                "undated_uids": [r["uid"] for r in primary if r.get("date_scope") == "undated"],
                "unread_uids": [r["uid"] for r in primary if r["uid"] not in read_uids],
                "deferred_candidates": [r["uid"] for r in candidates if r["uid"] not in read_uids],
                "limits": {"max_read_texts": max_texts, "max_primary_chars": max_chars},
                "absence_claims_supported": False}
    checkpoint("coverage", coverage=coverage, readings=readings, evidence=evidence)
    memo_sources = read_sources or [_spec("investigation-question", _json(common))]
    memo = engine("memo", "author_investigation_memo", memo_sources,
                  {**common, "plan": plan.get("final_output"), "evidence": evidence,
                   "source_readings": [{"uid": r["uid"], "reading": r["reading"], "rows": r["rows"], "source_metadata": r["source_metadata"]} for r in readings],
                   "coverage": coverage, "prior_context": context,
                   "citation_paths": state["citation_paths"][:150],
                   "citation_paths_supplied": min(150, len(state["citation_paths"])), "citation_paths_total": len(state["citation_paths"])})
    prose = memo.get("prose") or memo.get("final_output", "")
    references = re.findall(r"\[([^\[\]\s]+/[A-Z]\d+\.F\d+)\]", prose)
    verified_ids = {e["citation_id"] for e in evidence if e["quote_verified"]}
    unsupported = sorted(set(references) - verified_ids)
    missing_refs = bool(verified_ids) and not references
    validation = {"supported": not unsupported and not missing_refs, "references": references,
                  "unsupported_memo_citations": unsupported, "missing_evidence_citations": missing_refs}
    if not validation["supported"]:
        checkpoint("memo_validation", memo=prose, memo_rows=memo.get("rows", []), memo_validation=validation,
                   complete=False, paused_reason="memo_citation_validation")
        raise ValueError("memo references unknown or unverified evidence, or omits evidence citations; its draft and research were retained")
    checkpoint("done", memo=prose, memo_rows=memo.get("rows", []), memo_validation=validation,
               complete=True, running_stage=None)
    return state


def load_investigation(job_id):
    from src.dossier.blob_store import get_blob
    found = get_blob(f"investigation:{job_id}")
    return json.loads(found[1]) if found else None


def run_job_investigation(job, docs, *, cancel_check=None, persist=None):
    from src.dossier.blob_store import put_blob, get_blob
    from src.dossier.common import DossierCancelled, DossierDraining
    from src.dossier.drain import is_draining
    from src.dossier.engine_call import call_engine
    from src.dossier import events
    from src.readings.registry import index_job, reading, readings_for
    packet = next((json.loads(d.text) for d in docs if d.key == "investigation" and d.role == "plan"), None)
    if not packet or packet.get("kind") != CHAIN:
        raise ValueError("author_investigation recipe requires its frozen source packet")
    frozen = get_blob(f"investigation-context:{job.id}")
    if frozen:
        packet = json.loads(frozen[1])
    else:
        packet = hydrate_prior_readings(packet, lookup_index=readings_for, lookup_reading=reading)
        put_blob(f"investigation-context:{job.id}", "application/json", _json(packet).encode())
    def check():
        if cancel_check and cancel_check():
            raise DossierCancelled("author investigation cancelled between calls")
        if is_draining():
            raise DossierDraining("author investigation checkpoint saved between calls")
    def save(state):
        # Fail before another paid call if durable artifact persistence is unavailable.
        put_blob(f"investigation:{job.id}", "application/json", _json(state).encode())
        job.analysis = state["analysis"]
        from src.dossier.schemas import Receipt
        # Derive accounting from completed checkpoints, so resume cannot double-count.
        receipts = [Receipt(step="analysis", kind="llm", model=result.get("model", ""),
                            label=f"{stage}: {result.get('engine_key', '')}", cost_usd=float(result.get("cost_usd") or 0),
                            input_tokens=sum(int(c.get("input_tokens") or 0) for c in result.get("calls", [])),
                            output_tokens=sum(int(c.get("output_tokens") or 0) for c in result.get("calls", [])))
                    for stage, result in state["calls"].items()]
        job.receipts = receipts
        job.totals.cost_usd = state["cost_usd"]
        job.totals.llm_calls = sum(len(r.get("calls") or [None]) for r in state["calls"].values())
        job.totals.input_tokens = sum(r.input_tokens for r in receipts)
        job.totals.output_tokens = sum(r.output_tokens for r in receipts)
        if persist:
            persist(analysis=job.analysis, receipts=receipts, totals=job.totals)
        index_job({**job.model_dump(), "packet": packet})
        events.emit(job.id, "note", phase="analysis", detail=f"Author investigation: {state['current_stage']}",
                    cost_usd=state["cost_usd"], payload_json={"stage": state["current_stage"], "read_count": len(state.get("readings", []))})
    state = run_investigation(packet, {d.key: d.text for d in docs if d.role == "source"}, call=call_engine, save=save,
                              state=load_investigation(job.id), check=check,
                              spend_cap_usd=job.options.spend_cap_usd if job.options.spend_cap_usd is not None else 8.0)
    return "", state["analysis"]
