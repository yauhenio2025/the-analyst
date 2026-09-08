"""Import an external reviewed edition after completion, without model calls.

Dry-run: python -m scripts.import_reviewed_investigation_edition JOB --payload FILE
Apply:   python -m scripts.import_reviewed_investigation_edition JOB --payload FILE --apply

Requires the existing database schema. The canonical memo, phases, evidence,
readings and accounting remain intact. A separate reading and a full edition in
state.reviewed_editions are exposed by the existing investigation/readings APIs.
Offsets are Python Unicode character offsets in the frozen executor source text.
Source matching and citation resolution do not certify a reviewer's conclusions.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from scripts.reconcile_superseded_investigation_call import _blob, _column_json, _json, _require, _sha
from src.dossier import blob_store as blobs
from src.executor import db
from src.executor.document_store import decode_document_text
from src.readings import registry


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def _protected(state):
    return _sha(canonical_json({k: v for k, v in state.items() if k not in ("reviewed_editions", "updated_at")}))


def _reference(key, raw):
    return {"key": key, "sha256": _sha(raw), "bytes": len(raw)}


def _checked_receipt(cursor, receipt):
    _require(isinstance(receipt, dict) and set(receipt) == {"key", "sha256", "bytes"}, "invalid artifact receipt")
    raw = _blob(cursor, receipt["key"])
    _require(_sha(raw) == receipt["sha256"] and len(raw) == receipt["bytes"], "artifact receipt mismatch")
    return raw


def _ranges(value, length, label):
    _require(isinstance(value, list), label + " must be a list")
    result = []
    for span in value:
        _require(isinstance(span, (list, tuple)) and len(span) == 2 and
                 all(type(n) is int for n in span), "invalid " + label)
        lo, hi = span
        _require(0 <= lo < hi <= length, label + " exceeds the frozen body")
        _require(not result or result[-1][1] <= lo, label + " must be ordered without overlap")
        result.append([lo, hi])
    return result


def _proof(cursor, proof, packet, documents, state):
    uid, key = proof["uid"], proof["source_key"]
    matches = [(role, row) for role in ("primary", "field", "secondary") for row in packet.get(role, [])
               if row.get("uid") == uid and row.get("source_key") == key]
    _require(len(matches) == 1, "proof source is not unique in the frozen packet")
    role, source = matches[0]
    _require(proof["citation_id"].startswith(uid + "/"), "proof citation does not identify its source")
    docs = [d for d in documents if d.get("key") == key and d.get("role") == "source"]
    _require(len(docs) == 1 and docs[0].get("executor_doc_id"), "proof source document is missing or ambiguous")
    sql = "SELECT text,text_encoding,char_count,content_hash FROM executor_documents WHERE doc_id=%s"
    cursor.execute(sql if db._is_postgres() else sql.replace("%s", "?"), (docs[0]["executor_doc_id"],))
    row = cursor.fetchone()
    _require(row is not None, "proof executor source is missing")
    body = decode_document_text(row[0], row[1], cursor=cursor)
    digest = _sha(body.encode())
    _require(digest == proof["body_sha256"] == source["body_sha256"] == row[3] and
             len(body) == source["body_chars"] == row[2], "proof frozen source hash or length changed")
    pdf_hash = source.get("pdf_sha256") or (source.get("source_metadata") or {}).get("pdf_sha256")
    _require(proof.get("pdf_sha256") == pdf_hash, "proof PDF hash differs from frozen metadata")
    windows = _ranges(proof["review_windows"], len(body), "review windows")
    _require(bool(windows), "proof requires an explicit review window")
    spans = proof["quote_spans"]
    _require(isinstance(spans, list) and bool(spans), "proof requires exact source spans")
    coords = _ranges([[s["start"], s["end"]] for s in spans], len(body), "source spans")
    _require(all(body[lo:hi] == s["text"] for s, (lo, hi) in zip(spans, coords)), "proof source fragment differs from frozen text")
    _require(proof["source_quote"] == "".join(s["text"] for s in spans), "proof source quote must retain every exact fragment")
    # Disjoint spans remain explicit; never imply text between them was quoted.
    _require(any(all(lo <= a and b <= hi for a, b in coords) for lo, hi in windows),
             "proof fragments cross separate review windows")
    readings = [r for r in state.get("readings", []) if r.get("source_key") == key]
    _require(len(readings) <= 1, "canonical source reading is ambiguous")
    engine_windows = []
    if readings:
        _require(readings[0].get("body_sha256") == digest, "canonical reading source hash differs")
        engine_windows = _ranges(readings[0].get("inspected_ranges", []), len(body), "engine windows")
    covered = any(all(lo <= a and b <= hi for a, b in coords) for lo, hi in engine_windows)
    engine = [e for e in state.get("evidence", []) if e.get("citation_id") == proof["citation_id"]]
    positive_engine = [e for e in engine if e.get("quote_verified") is True]
    _require(all(e.get("uid") == uid and e.get("source_key") == key and
                 e.get("body_sha256") == digest for e in positive_engine), "proof citation conflicts with canonical source identity")
    pages = sorted({p["page"] for p in source.get("page_spans", [])
                    if any(p["start"] < hi and lo < p["end"] for lo, hi in coords)})
    visual = proof.get("visual_audit")
    visual_status = "not_claimed"
    if visual is not None:
        _require(pdf_hash and visual.get("reviewed_from_pdf") is True, "visual review requires a frozen PDF identity")
        pdf = _checked_receipt(cursor, visual["pdf_receipt"])
        _require(_sha(pdf) == pdf_hash and pdf.startswith(b"%PDF-"), "visual review PDF receipt differs from source")
        audit = json.loads(_checked_receipt(cursor, visual["audit_receipt"]))
        _require(audit.get("uid") == uid and audit.get("body_sha256") == digest and
                 audit.get("pdf_sha256") == pdf_hash and audit.get("reviewed_from_pdf") is True and
                 bool(audit.get("method")), "visual audit does not bind this frozen source")
        reviewed_pages = {p["page"]: p for p in audit.get("pages", [])}
        _require(bool(pages) and set(pages) <= reviewed_pages.keys(), "visual audit does not cover the proof pages")
        for page in source.get("page_spans", []):
            for lo, hi in coords:
                if page["start"] < hi and lo < page["end"]:
                    approved = reviewed_pages[page["page"]]
                    _require(approved.get("reviewed_start", page["start"]) <= max(lo, page["start"]) and
                             min(hi, page["end"]) <= approved.get("reviewed_end", page["end"]),
                             "proof exceeds the visually reviewed page region")
        visual_status = "reviewer_attested_with_verified_artifact_hashes"
    return {"proof_id": proof["id"], "citation_id": proof["citation_id"], "source_role": role,
            "body_sha256": digest, "pdf_sha256": pdf_hash, "pages": pages,
            "page_urls": [f"{pdf_url.split(chr(35))[0]}#page={page}" for page in pages] if
                         (pdf_url := source.get("pdf_url") or (source.get("source_metadata") or {}).get("pdf_url")) else [],
            "review_quote_verified": True, "quote_match": "review_exact_source_fragments", "normalization": "none",
            "engine_quote_verified": bool(positive_engine) if engine else None,
            "passage_form": "single_contiguous_passage" if all(a[1] == b[0] for a, b in zip(coords, coords[1:])) else "ordered_discontinuous_fragments",
            "continuous_quote": all(a[1] == b[0] for a, b in zip(coords, coords[1:])),
            "fragment_join": "exact_concatenation_with_explicit_spans",
            "original_engine_window_coverage": "inside_one_original_window" if covered else "supplemental_outside_one_original_window",
            "review_verification": "exact_frozen_source_fragments",
            "engine_verification": "verified" if positive_engine else
                                   "unverified" if engine else "not_in_engine_evidence",
            "engine_inspection": "inside_one_original_window" if covered else "supplemental_outside_one_original_window",
            "engine_inspected_ranges": engine_windows,
            "pdf_verification": "frozen_packet_hash_bound" if pdf_hash else "no_frozen_pdf_hash",
            "visual_verification": visual_status, "semantic_verification": "reviewer_responsibility"}


def _memo_ids(memo):
    # Preserve link labels (which may cite evidence), ignore URL destinations and
    # plain URLs. Ordinary Markdown notes, paths and section labels are not IDs.
    without_urls = re.sub(r"https?://[^\s<>\]]+", "", memo)
    return sorted({value.rstrip(".:") for value in re.findall(
        r"(?<![\w:])[A-Za-z][\w-]*:[\w.-]+/[A-Za-z][\w.:-]*", without_urls)})


def _validate_payload(cursor, payload, packet, documents, state):
    _require(payload.get("schema_version") == 1 and payload.get("kind") == "reviewed_edition", "unsupported reviewed edition schema")
    _require(isinstance(payload.get("title"), str) and bool(payload["title"].strip()), "review title is required")
    _require(isinstance(payload.get("reviewed_memo"), str) and bool(payload["reviewed_memo"].strip()), "reviewed memo is required")
    provenance = payload.get("provenance")
    _require(isinstance(provenance, dict) and all(isinstance(provenance.get(k), str) and provenance[k].strip()
                 for k in ("reviewer", "reviewed_at", "method")), "review provenance is required")
    stamp = datetime.fromisoformat(provenance["reviewed_at"].replace("Z", "+00:00"))
    _require(stamp.tzinfo is not None, "review timestamp requires a timezone")
    proofs = payload.get("source_proofs")
    _require(isinstance(proofs, list), "source_proofs must be a list")
    for key in ("id", "citation_id"):
        _require(all(isinstance(p.get(key), str) and p[key] for p in proofs) and
                 len({p[key] for p in proofs}) == len(proofs), "proof IDs and citation IDs must be unique")
    proof_checks = [_proof(cursor, p, packet, documents, state) for p in proofs]
    canonical = {}
    for e in state.get("evidence", []):
        cid = e.get("citation_id")
        if cid and e.get("quote_verified") is True:
            if cid in canonical:
                _require(all(canonical[cid].get(k) == e.get(k) for k in ("uid", "source_key", "body_sha256")),
                         "engine-verified citation has conflicting source identities")
            canonical[cid] = e
    exact = {p["citation_id"]: p for p in proof_checks}
    supported = canonical.keys() | exact.keys()
    memo_ids = _memo_ids(payload["reviewed_memo"])
    _require(not set(memo_ids) - supported, "reviewed memo has unresolved or engine-unverified citations")
    findings = payload.get("findings")
    _require(isinstance(findings, list) and findings, "a finding/revision ledger is required")
    _require(all(isinstance(f.get("id"), str) and f["id"] for f in findings) and
             len({f["id"] for f in findings}) == len(findings), "finding IDs must be unique")
    for f in findings:
        _require(f.get("kind") in ("finding", "revision") and isinstance(f.get("text"), str) and f["text"].strip(), "invalid review finding")
        ids = f.get("support_ids")
        _require(isinstance(ids, list) and all(isinstance(i, str) for i in ids) and not set(ids) - supported,
                 "finding has unresolved support IDs")
        _require(ids or f.get("status") == "unresolved", "unsupported findings must be explicitly unresolved")
        _require(not set(_memo_ids(f["text"])) - supported, "finding text has unresolved citations")
    used = sorted(set(memo_ids) | {i for f in findings for i in f["support_ids"]})
    return {"source_proofs": proof_checks, "citation_support": [
                {"citation_id": cid, "engine_verification": "verified" if cid in canonical else
                    exact[cid]["engine_verification"], "review_verification": "exact_frozen_source_fragments" if cid in exact else "canonical_engine_evidence",
                 "proof_id": exact[cid]["proof_id"] if cid in exact else None} for cid in used],
            "memo_citations": memo_ids, "citation_resolution": "passed", "semantic_verification": "reviewer_responsibility",
            "engine_memo_validation": copy.deepcopy(state.get("memo_validation")),
            "engine_evidence_unchanged": True, "new_provider_calls": 0}


def import_edition(job_id: str, payload: dict, *, apply: bool = False) -> dict:
    """Validate and import atomically; repeats are no-ops, conflicts are refused."""
    payload = copy.deepcopy(payload)
    for proof in payload.get("source_proofs", []):
        if "source_spans" in proof:
            _require("quote_spans" not in proof or proof["quote_spans"] == proof["source_spans"], "conflicting quote span aliases")
            proof["quote_spans"] = proof.pop("source_spans")
    payload = json.loads(canonical_json(payload))
    digest = _sha(canonical_json(payload))
    phase = "review:" + digest
    state_key = "investigation:" + job_id
    with db.get_connection() as conn:
        try:
            cursor, pg = conn.cursor(), db._is_postgres()
            cursor.execute(("SET TRANSACTION ISOLATION LEVEL READ COMMITTED" if apply else
                            "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY") if pg else
                           ("BEGIN IMMEDIATE" if apply else "BEGIN"))
            sql = "SELECT status,analysis_json,documents_json FROM dossier_jobs WHERE id=%s"
            if pg and apply:
                sql += " FOR UPDATE"
            cursor.execute(sql if pg else sql.replace("%s", "?"), (job_id,))
            row = cursor.fetchone()
            _require(row is not None and row[0] == "done", "job must be done before review import")
            if pg and apply:
                cursor.execute("SELECT blob_key FROM dossier_blobs WHERE blob_key=%s FOR UPDATE", (state_key,))
                cursor.execute("SELECT pg_advisory_xact_lock(hashtext('readings-ledger-index'))")
            state = json.loads(_blob(cursor, state_key))
            _require(state.get("complete") is True and state.get("running_stage") is None,
                     "investigation checkpoint must be complete and idle")
            _require(_column_json(cursor, row[1]) == state["analysis"], "job and checkpoint analysis differ")
            protected = _protected(state)
            packet = json.loads(_blob(cursor, "investigation-context:" + job_id))
            _require(payload.get("job_id") == job_id and payload.get("packet_sha256") == state["packet_sha256"] == _sha(_json(packet)),
                     "review job or frozen packet hash differs")
            memo = state["memo"].encode()
            _require(bool(memo) and payload.get("original_memo_sha256") == _sha(memo), "original memo hash differs")
            verification = _validate_payload(cursor, payload, packet, _column_json(cursor, row[2]), state)
            original_ref = _reference(f"investigation-original-memo:{job_id}:{_sha(memo)}", memo)
            edition = {"payload": payload, "verification": verification, "original_memo": original_ref}
            edition_bytes = canonical_json(edition)
            edition_ref = _reference(f"investigation-reviewed-edition:{job_id}:{digest}", edition_bytes)
            entry = {**payload, "content_hash": digest, "artifact": edition_ref, "original_memo_artifact": original_ref,
                     "source_proofs": [{**{k: v for k, v in proof.items() if k not in ("quote_start", "quote_end", "quote_verified")}, **check}
                                       for proof, check in zip(payload["source_proofs"], verification["source_proofs"])],
                     "verification": verification, "reading_ref": {"job_id": job_id, "phase": phase}}
            reading = {"job_id": job_id, "phase": phase, "engine": "reviewed_edition_import", "kind": "reviewed_edition",
                       "origin": "external_review", "when": payload["provenance"]["reviewed_at"], "cost_usd": 0.0,
                       "provider_calls": [], "depth": None, "intent": "External reviewed edition: " + payload["title"],
                       "prose": payload["reviewed_memo"], "edition": entry,
                       "rows": [{"id": f["id"], "dim": f["kind"], "text": f["text"], "anchor": "", "doc": "",
                                 "locus": "", "conjecture": f.get("status") == "unresolved", "fields": copy.deepcopy(f)} for f in payload["findings"]],
                       "n_rows": len(payload["findings"]), "n_conjectural": sum(f.get("status") == "unresolved" for f in payload["findings"]),
                       "persons": registry.job_authors({"packet": packet}),
                       "texts": sorted({p["uid"] for p in payload["source_proofs"]} | {c["citation_id"].split("/", 1)[0] for c in verification["citation_support"]}),
                       "sources": sorted({p["source_key"] for p in payload["source_proofs"]}),
                       "renders": [f"{registry.PUBLIC_BASE}/v1/dossier/jobs/{job_id}/investigation"]}
            editions = state.get("reviewed_editions", [])
            _require(isinstance(editions, list), "invalid reviewed edition ledger")
            existing = [e for e in editions if e.get("content_hash") == digest]
            _require(len(existing) <= 1, "duplicate reviewed edition")
            existing_reading = blobs.get_blob_in_cursor(cursor, f"reading:{job_id}:{phase}")
            _require(bool(existing) == bool(existing_reading), "partial reviewed edition import")
            pending, missing_indexes, index_expected = {}, set(), {}

            def original_get(key):
                found = blobs.get_blob_in_cursor(cursor, key)
                raw = found[1] if found else None
                if raw is not None and key.startswith("readings:"):
                    _require(isinstance(json.loads(raw), list), "invalid existing reading index")
                return raw

            def get(key):
                return pending[key][1] if key in pending else original_get(key)

            def put(key, mime, data):
                previous = original_get(key)
                if key.startswith("readings:"):
                    index_expected[key] = [e for e in json.loads(data) if e.get("job_id") == job_id and e.get("phase") == phase]
                if existing:
                    # Index order may change after other readings are indexed.
                    if key.startswith("readings:"):
                        expected = [e for e in json.loads(data) if e.get("job_id") == job_id and e.get("phase") == phase]
                        actual = [e for e in json.loads(previous or b"[]") if e.get("job_id") == job_id and e.get("phase") == phase]
                        _require(not actual or actual == expected, "review reading index has conflicting content")
                        if not actual:
                            missing_indexes.add(key)
                    else:
                        _require(previous == data, "review reading changed after import")
                elif key.startswith("readings:") and previous:
                    _require(not any(e.get("job_id") == job_id and e.get("phase") == phase for e in json.loads(previous)),
                             "partial review reading index")
                pending[key] = (mime, data)

            registry._save_reading(reading, put, get)
            for ref, mime, raw in ((original_ref, "text/markdown", memo), (edition_ref, "application/json", edition_bytes)):
                previous = get(ref["key"])
                _require(previous is None or previous == raw, "immutable review artifact collision")
                if existing:
                    _require(previous == raw, "review artifact missing after import")
                pending[ref["key"]] = (mime, raw)
            result = {"status": "already_applied" if existing else "applied" if apply else "would_apply",
                      "applied": bool(apply and not existing), "job_id": job_id, "content_hash": digest,
                      "artifact": edition_ref, "original_memo_artifact": original_ref, "reading_ref": entry["reading_ref"],
                      "proof_count": len(payload["source_proofs"]), "finding_count": len(payload["findings"]),
                      "canonical_research_sha256": protected, "new_provider_calls": 0, "cost_change_usd": 0.0}
            if existing:
                _require({k: v for k, v in existing[0].items() if k != "imported_at"} == entry, "review edition changed after import")
                if missing_indexes:
                    result.update(status="relinked" if apply else "would_relink", applied=apply)
                if apply and missing_indexes:
                    for key in sorted(missing_indexes):
                        mime, raw = pending[key]
                        blobs.put_blob_in_cursor(cursor, key, mime, raw)
                    conn.commit()
                else:
                    conn.rollback()
                result["index_verification"] = _verify_indexes(index_expected, job_id, phase)
                return result
            now = datetime.now(timezone.utc).isoformat()
            state["reviewed_editions"] = editions + [{**entry, "imported_at": now}]
            state["updated_at"] = now
            _require(_protected(state) == protected, "canonical research changed during review import")
            if apply:
                for key, (mime, raw) in pending.items():
                    immutable = key in (original_ref["key"], edition_ref["key"], f"reading:{job_id}:{phase}")
                    created = blobs.put_blob_in_cursor(cursor, key, mime, raw, overwrite=not immutable)
                    if immutable and not created:
                        _require(_blob(cursor, key) == raw, "immutable review artifact collision")
                blobs.put_blob_in_cursor(cursor, state_key, "application/json", _json(state))
                conn.commit()
            else:
                conn.rollback()
            result["index_verification"] = _verify_indexes(index_expected, job_id, phase) if apply else {"status": "would_index", "keys": sorted(index_expected)}
            return result
        except Exception:
            conn.rollback()
            raise


def _verify_indexes(expected, job_id, phase):
    """Read after commit; a legacy non-locking index writer can still race us."""
    try:
        missing, conflicting = [], []
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY" if db._is_postgres() else "BEGIN")
            for key, entries in expected.items():
                found = blobs.get_blob_in_cursor(cursor, key)
                actual = [e for e in json.loads(found[1] if found else b"[]")
                          if e.get("job_id") == job_id and e.get("phase") == phase]
                if not actual:
                    missing.append(key)
                elif actual != entries:
                    conflicting.append(key)
            conn.rollback()
        return {"status": "conflicting" if conflicting else "missing" if missing else "present",
                "missing_keys": missing, "conflicting_keys": conflicting}
    except Exception as exc:
        return {"status": "unavailable", "error_kind": type(exc).__name__}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_id")
    parser.add_argument("--payload", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="apply once; default validates without writing")
    args = parser.parse_args(argv)
    try:
        result = import_edition(args.job_id, json.loads(args.payload.read_text()), apply=args.apply)
    except ValueError as exc:
        parser.exit(1, f"Review import refused: {exc}\n")
    except Exception as exc:
        parser.exit(1, f"Review import failed ({type(exc).__name__}); transaction rolled back.\n")
    print(json.dumps(result, indent=2))
    if result["index_verification"]["status"] in ("missing", "conflicting", "unavailable"):
        parser.exit(1, "Edition is durable; index verification needs attention. Rerun --apply to restore missing indexes; conflicting indexes require review.\n")


if __name__ == "__main__":
    main()
