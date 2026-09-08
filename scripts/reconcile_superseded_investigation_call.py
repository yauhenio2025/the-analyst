"""Reconcile one archived provider call after completion; dry-run unless --apply.

Run with the existing executor database environment, without starting the API:
  python -m scripts.reconcile_superseded_investigation_call JOB --receipt FILE
  python -m scripts.reconcile_superseded_investigation_call JOB --receipt FILE --apply

Only accounting is changed. Canonical phases, readings, evidence, source packets,
and memo stay intact. No registry indexing, rendering, or model calls occur.
The completed job's existing schema must already be initialized.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from src.dossier import blob_store as blobs
from src.dossier.schemas import Receipt
from src.dossier.store import compute_totals
from src.executor import db

REF = "__analyst_dossier_json_blob_v1__"


def _require(ok, message):
    if not ok:
        raise ValueError(message)


def _json(value):
    return json.dumps(value, ensure_ascii=False).encode()


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _money(value):
    amount = Decimal(str(value or 0))
    _require(amount.is_finite() and amount >= 0, "invalid recorded cost")
    return amount


def _sum_cost(rows):
    return sum((_money(r.get("cost_usd")) for r in rows), Decimal(0))


def _same_cost(a, b):
    return abs(_money(a) - _money(b)) < Decimal("0.00000001")


def _blob(cursor, key):
    found = blobs.get_blob_in_cursor(cursor, key)
    _require(found is not None, "required durable artifact is missing")
    return found[1]


def _column_json(cursor, raw):
    value = json.loads(raw) if isinstance(raw, str) else raw
    if isinstance(value, dict) and REF in value:
        _require(set(value) == {REF, "sha256", "bytes"}, "invalid JSON storage reference")
        data = _blob(cursor, value[REF])
        _require(_sha(data) == value["sha256"] and len(data) == value["bytes"],
                 "JSON storage reference changed")
        value = json.loads(data)
    return value


def _store_column(cursor, value):
    raw = _json(value)
    if len(raw) <= 512 * 1024:
        return raw.decode()
    digest = _sha(raw)
    key = "dossier-json:" + digest
    if not blobs.put_blob_in_cursor(cursor, key, "application/json", raw, overwrite=False):
        _require(_blob(cursor, key) == raw, "content-addressed JSON collision")
    return _json({REF: key, "sha256": digest, "bytes": len(raw)}).decode()


def _research_hash(state):
    excluded = {"calls", "cost_usd", "updated_at", "accounting_reconciliations"}
    return _sha(json.dumps({k: v for k, v in state.items() if k not in excluded},
                           sort_keys=True, ensure_ascii=False).encode())


def _receipt_for(stage, call):
    return {"label": f"{stage}: {call.get('engine_key', '')}",
            "cost_usd": float(_money(call.get("cost_usd"))),
            "input_tokens": sum(int(c.get("input_tokens") or 0) for c in call.get("calls", [])),
            "output_tokens": sum(int(c.get("output_tokens") or 0) for c in call.get("calls", []))}


def _check_accounting(state, receipts, totals):
    _require(_same_cost(state["cost_usd"], _sum_cost(state["calls"].values())),
             "checkpoint call costs do not reconcile")
    for stage, call in state["calls"].items():
        expected = _receipt_for(stage, call)
        found = [r for r in receipts if r.get("label") == expected["label"]]
        _require(len(found) == 1 and found[0].get("kind") == "llm" and
                 found[0].get("step") == "analysis", "missing or duplicate call receipt")
        _require(_same_cost(found[0].get("cost_usd"), expected["cost_usd"]) and
                 all(found[0].get(k) == expected[k] for k in ("input_tokens", "output_tokens")),
                 "call receipt usage does not reconcile")
    _require(sum(r.get("kind") == "llm" and r.get("step") == "analysis" for r in receipts) ==
             len(state["calls"]), "analysis contains receipts outside the call ledger")
    derived = compute_totals(receipts, totals)
    _require(_same_cost(totals["cost_usd"], derived["cost_usd"]) and
             all(totals.get(k) == derived[k] for k in
                 ("input_tokens", "output_tokens", "llm_calls", "image_calls")),
             "job receipt totals do not reconcile")


def reconcile(job_id: str, storage_receipt: dict, *, apply: bool = False) -> dict:
    """Validate first; atomically add the real superseded call exactly once.

    PostgreSQL row locks serialize concurrent applies. SQLite uses BEGIN
    IMMEDIATE for the same purpose. Dry-run uses a read-only PG transaction and
    does not initialize tables or invoke any mutation helper.
    """
    with db.get_connection() as conn:
        try:
            cursor = conn.cursor()
            pg = db._is_postgres()
            if pg:
                cursor.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED" if apply else
                               "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY")
            else:
                cursor.execute("BEGIN IMMEDIATE" if apply else "BEGIN")
            sql = "SELECT status, receipts_json, totals_json, analysis_json FROM dossier_jobs WHERE id=%s"
            if pg and apply:
                sql += " FOR UPDATE"
            cursor.execute(sql if pg else sql.replace("%s", "?"), (job_id,))
            row = cursor.fetchone()
            _require(row is not None and row[0] == "done", "job must be done before reconciliation")
            state_key = "investigation:" + job_id
            if pg and apply:
                cursor.execute("SELECT blob_key FROM dossier_blobs WHERE blob_key=%s FOR UPDATE", (state_key,))
            state = json.loads(_blob(cursor, state_key))
            _require(state.get("complete") is True and state.get("running_stage") is None,
                     "investigation checkpoint must be complete and idle")
            receipts = _column_json(cursor, row[1])
            totals = _column_json(cursor, row[2])
            analysis = _column_json(cursor, row[3])
            _require(analysis == state["analysis"], "job and checkpoint analysis differ")
            protected = _research_hash(state)
            archive_key = storage_receipt["key"]
            raw = _blob(cursor, archive_key)
            _require(_sha(raw) == storage_receipt["sha256"] and len(raw) == storage_receipt["bytes"] and
                     storage_receipt.get("archived_full_provider_output") is True, "archive receipt mismatch")
            archive = json.loads(raw)
            _require(archive.get("job_id") == job_id and archive.get("kind") == "superseded_reading",
                     "archive is for another job or artifact kind")
            packet = json.loads(_blob(cursor, "investigation-context:" + job_id))
            _require(_sha(_json(packet)) == state["packet_sha256"] == archive["packet_sha256"],
                     "frozen source packet changed")
            source = archive["reading"]
            matches = [r for name in ("field", "primary") for r in packet.get(name, [])
                       if r.get("uid") == archive["source_uid"] and r.get("source_key") == source["source_key"]]
            _require(len(matches) == 1 and source["body_sha256"] == matches[0]["body_sha256"] and
                     source["uid"] == archive["source_uid"], "archived source identity or hash changed")
            recovery = archive["raw_provider_output_recovery"]
            phase = recovery["raw_phase"]
            output_hash = _sha(phase["final_output"].encode())
            _require(recovery.get("status") == "complete" and output_hash == recovery["raw_output_sha256"],
                     "archived raw provider output changed")
            _require(archive_key == f"investigation-superseded-reading:{job_id}:{source['uid']}:{output_hash}",
                     "archive key does not identify this output")
            snapshot = _blob(cursor, recovery["immutable_blob_key"])
            _require(_sha(snapshot) == recovery["snapshot_sha256"] and
                     recovery["immutable_blob_key"] == "dossier-json:" + _sha(snapshot),
                     "original immutable snapshot changed")
            _require(json.loads(snapshot).get(str(phase["phase_number"])) == phase,
                     "raw phase differs from the original immutable snapshot")
            stage = archive["stage"]
            _require(stage == phase["stage"] == "read:" + source["source_key"] and
                     phase.get("sources") == [source["source_key"]], "archived stage source changed")
            canonical = state["calls"].get(stage)
            _require(canonical is not None and canonical.get("engine_key") == phase["engine_key"] and
                     _sha(canonical["final_output"].encode()) != output_hash,
                     "archive does not describe a superseded canonical call")
            provider_calls = phase.get("calls", [])
            _require(len(provider_calls) == 1, "this utility requires one archived provider call")
            usage = provider_calls[0]
            for field in ("input_tokens", "output_tokens", "duration_ms"):
                _require(type(usage.get(field)) is int and usage[field] >= 0, "invalid archived provider usage")
            adjustment = archive["accounting_adjustment"]
            cost = _money(phase["cost_usd"])
            _require(cost > 0 and all(_same_cost(cost, value) for value in
                     (usage["cost_usd"], adjustment["cost_usd"], archive["extra_cost_usd"],
                      storage_receipt["extra_cost_usd"])) and adjustment["llm_calls"] == 1 and
                     all(adjustment[k] == usage[k] for k in ("input_tokens", "output_tokens")),
                     "archived usage, adjustment, and receipt disagree")
            ledger_key = f"superseded:{stage}:{output_hash}"
            reference = {"key": archive_key, "sha256": storage_receipt["sha256"],
                         "raw_output_sha256": output_hash, "source_uid": source["uid"]}
            call = {"engine_key": phase["engine_key"], "model": usage["model_used"],
                    "depth": phase["depth"], "final_output": phase["final_output"],
                    "wall": phase.get("final_wall", {}), "cost_usd": float(cost),
                    "calls": provider_calls, "superseded_stage": stage, "archive": reference}
            receipt = Receipt(step="analysis", kind="llm", model=usage["model_used"],
                              **_receipt_for(ledger_key, call), duration_ms=usage["duration_ms"],
                              result_hash=output_hash, ts=phase["finished"], source_job_id=job_id).model_dump()
            markers = state.get("accounting_reconciliations", {})
            _require(isinstance(markers, dict), "invalid reconciliation ledger")
            prior_receipts = [r for r in receipts if r.get("label") == receipt["label"] or
                              r.get("result_hash") == output_hash]
            existing = ledger_key in state["calls"]
            if existing or ledger_key in markers or prior_receipts:
                _require(existing and state["calls"][ledger_key] == call and
                         markers.get(ledger_key, {}).get("archive") == reference and
                         len(prior_receipts) == 1 and
                         prior_receipts[0].get("result_hash", "") in ("", output_hash),
                         "partial or conflicting accounting reconciliation")
                _check_accounting(state, receipts, totals)
                conn.rollback()
                return {"status": "already_applied", "job_id": job_id, "ledger_key": ledger_key,
                        "cost_usd": totals["cost_usd"], "applied": False, "archive": reference}
            _check_accounting(state, receipts, totals)
            before_cost = totals["cost_usd"]
            state["calls"][ledger_key] = call
            state["cost_usd"] = float(_sum_cost(state["calls"].values()))
            now = datetime.now(timezone.utc).isoformat()
            state.setdefault("accounting_reconciliations", {})[ledger_key] = {
                "archive": reference, "cost_usd": float(cost), "input_tokens": usage["input_tokens"],
                "output_tokens": usage["output_tokens"], "llm_calls": 1, "applied_at": now}
            state["updated_at"] = now
            receipts = receipts + [receipt]
            totals = compute_totals(receipts, totals)
            _check_accounting(state, receipts, totals)
            _require(_research_hash(state) == protected, "canonical research changed during reconciliation")
            result = {"status": "applied" if apply else "would_apply", "applied": apply,
                      "job_id": job_id, "ledger_key": ledger_key, "archive": reference,
                      "extra_cost_usd": float(cost), "before_cost_usd": before_cost,
                      "after_cost_usd": totals["cost_usd"], "added_provider_calls": 1,
                      "added_input_tokens": usage["input_tokens"], "added_output_tokens": usage["output_tokens"],
                      "canonical_research_sha256": protected}
            if apply:
                blobs.put_blob_in_cursor(cursor, state_key, "application/json", _json(state))
                receipt_json, total_json = _store_column(cursor, receipts), _store_column(cursor, totals)
                sql = "UPDATE dossier_jobs SET receipts_json=%s, totals_json=%s, updated_at=%s WHERE id=%s AND status='done'"
                cursor.execute(sql if pg else sql.replace("%s", "?"), (receipt_json, total_json, now, job_id))
                _require(cursor.rowcount == 1, "job changed before reconciliation could commit")
                conn.commit()
            else:
                conn.rollback()
            return result
        except Exception:
            conn.rollback()
            raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_id")
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="apply once; otherwise validate without writing")
    args = parser.parse_args(argv)
    try:
        result = reconcile(args.job_id, json.loads(args.receipt.read_text()), apply=args.apply)
    except ValueError as exc:
        parser.exit(1, f"Reconciliation refused: {exc}\n")
    except Exception as exc:
        # Do not print database exception strings or connection configuration.
        parser.exit(1, f"Reconciliation failed ({type(exc).__name__}); transaction rolled back.\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
