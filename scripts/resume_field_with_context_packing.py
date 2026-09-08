"""Resume a field job stopped before spending at the final-context size guard.

Dry-run emits a preflight receipt. --apply requires that receipt plus explicit
--competing-resumes-disabled coordination. The patched modules load only in this
admin process; the normal synchronous dossier runner owns all calls, receipts,
status transitions, finalization and indexing. No app file is replaced or deployed.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import sys
import types
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from src.dossier import blob_store as blobs
from src.executor import db


def _require(ok, message):
    if not ok:
        raise ValueError(message)


def _json(value):
    return json.dumps(value, ensure_ascii=False).encode()


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _hash(value):
    return _sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode())


def _blob(cursor, key):
    found = blobs.get_blob_in_cursor(cursor, key)
    _require(found is not None, "required checkpoint artifact is missing")
    return found[1]


def _column(cursor, raw):
    value = json.loads(raw) if isinstance(raw, str) else raw
    if isinstance(value, dict) and "__analyst_dossier_json_blob_v1__" in value:
        data = _blob(cursor, value["__analyst_dossier_json_blob_v1__"])
        _require(_sha(data) == value["sha256"] and len(data) == value["bytes"], "job JSON artifact changed")
        return json.loads(data)
    return value


def _snapshot(cursor, job_id, *, lock=False):
    sql = "SELECT status,step,analysis_json,receipts_json,totals_json FROM dossier_jobs WHERE id=%s"
    if lock and db._is_postgres():
        sql += " FOR UPDATE"
    cursor.execute(sql if db._is_postgres() else sql.replace("%s", "?"), (job_id,))
    row = cursor.fetchone()
    _require(row is not None, "job is missing")
    if lock and db._is_postgres():
        cursor.execute("SELECT blob_key FROM dossier_blobs WHERE blob_key=%s FOR UPDATE", ("investigation:" + job_id,))
    raw = _blob(cursor, "investigation:" + job_id)
    state = json.loads(raw)
    packet = json.loads(_blob(cursor, "investigation-context:" + job_id))
    _require(_sha(_json(packet)) == state["packet_sha256"], "frozen source packet changed")
    analysis, receipts, totals = [_column(cursor, v) for v in row[2:]]
    _require(analysis == state["analysis"], "job/checkpoint analysis differ")
    call_cost = sum(Decimal(str(c.get("cost_usd") or 0)) for c in state["calls"].values())
    _require(abs(call_cost - Decimal(str(state["cost_usd"]))) < Decimal('0.00000001') and
             abs(call_cost - Decimal(str(totals["cost_usd"]))) < Decimal('0.00000001'), "saved call costs do not reconcile")
    result = {"job_id": job_id, "status": row[0], "step": row[1], "checkpoint_sha256": _sha(raw),
              "packet_sha256": state["packet_sha256"], "cached_call_count": len(state["calls"]),
              "cached_calls_sha256": _hash(state["calls"]), "read_inputs_sha256": _hash(state["read_inputs"]),
              "analysis_sha256": _hash(analysis), "receipts_sha256": _hash(receipts), "totals_sha256": _hash(totals),
              "cost_usd": state["cost_usd"], "paused_stage": state.get("current_stage")}
    return result, state


def _guard(receipt, state):
    _require(receipt["status"] == "failed" and receipt["step"] == "analysis", "job must be failed at analysis before recovery")
    _require(state.get("kind") == "field_investigation" and state.get("paused_reason") == "input_limit" and
             state.get("running_stage") is None and state.get("complete") is False, "checkpoint must be idle at a pre-call input limit")
    stage = state.get("current_stage", "")
    _require(stage.split(":", 1)[0] in ("adjudication", "memo") and stage not in state["calls"], "recovery requires an unpaid final stage")
    _require(state.get("call_input_manifests", {}).get(stage, {}).get("chars", 0) > 640000, "missing original input-limit manifest")


def _code(module_dir):
    result = {}
    for name in ("context_packing", "field_investigation"):
        path = Path(module_dir) / (name + ".py")
        raw = path.read_bytes()
        compile(raw, str(path), "exec")
        result[name] = (path, raw)
    return result


def _code_receipt(code):
    return {"module_sha256": {name: _sha(raw) for name, (_, raw) in code.items()},
            "admin_script_sha256": _sha(Path(__file__).read_bytes())}


@contextlib.contextmanager
def _modules(code):
    previous = {}
    try:
        for short, (path, raw) in code.items():
            name = "src.dossier." + short
            previous[name] = sys.modules.get(name)
            module = types.ModuleType(name)
            module.__file__, module.__package__ = str(path), "src.dossier"
            sys.modules[name] = module
            exec(compile(raw, str(path), "exec"), module.__dict__)
        yield
    finally:
        for name, module in previous.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


def _run_normal(job_id):
    # _run is the exact synchronous worker used by runner.resume/start. Calling
    # it here avoids exiting while a daemon thread still owns paid work.
    from src.dossier import runner
    _require(not runner.is_draining(), "admin process is draining")
    with runner._lock:
        _require(job_id not in runner._running, "job is already running in this process")
        runner._running.add(job_id)
        runner._cancel.discard(job_id)
    runner._run(job_id)


def resume(job_id, module_dir, *, apply=False, expected=None, competing_resumes_disabled=False):
    code = _code(module_dir)
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY" if db._is_postgres() else "BEGIN")
        receipt, state = _snapshot(cursor, job_id)
        _guard(receipt, state)
        receipt.update(_code_receipt(code))
        conn.rollback()
    if not apply:
        return {"status": "ready", "applied": False, "preflight": receipt}
    _require(competing_resumes_disabled, "disable competing app/monitor resumes before applying")
    _require(expected == receipt, "preflight checkpoint or approved module hashes changed; run dry-run again")
    with _modules(code), db.get_connection() as lock_conn:
        cursor = lock_conn.cursor()
        sqlite_lock, pg_locked, launched = None, False, False
        try:
            if db._is_postgres():
                cursor.execute("SELECT pg_try_advisory_lock(hashtext(%s))", ("field-admin-continuation:" + job_id,))
                pg_locked = bool(cursor.fetchone()[0])
                _require(pg_locked, "another admin continuation owns this job")
                lock_conn.commit()
            else:
                import fcntl
                path = str(db.SQLITE_PATH) + "." + _sha(job_id.encode())[:16] + ".resume-lock"
                sqlite_lock = open(path, "a")
                try:
                    fcntl.flock(sqlite_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError:
                    raise ValueError("another admin continuation owns this job") from None
                cursor.execute("BEGIN IMMEDIATE")
            actual, before = _snapshot(cursor, job_id, lock=True)
            _guard(actual, before)
            actual.update(_code_receipt(code))
            _require(actual == expected, "checkpoint changed while acquiring the recovery lock")
            key = f"investigation-admin-continuation:{job_id}:{actual['checkpoint_sha256']}"
            checkpoint_raw = _blob(cursor, "investigation:" + job_id)
            _require(_sha(checkpoint_raw) == actual["checkpoint_sha256"], "checkpoint changed before archival")
            checkpoint_ref = {"key": key + ":checkpoint", "sha256": actual["checkpoint_sha256"], "bytes": len(checkpoint_raw)}
            if not blobs.put_blob_in_cursor(cursor, checkpoint_ref["key"], "application/json", checkpoint_raw, overwrite=False):
                _require(_blob(cursor, checkpoint_ref["key"]) == checkpoint_raw, "immutable checkpoint archive collision")
            launch = {"kind": "field_context_continuation", "preflight": actual, "checkpoint_artifact": checkpoint_ref,
                      "started_at": datetime.now(timezone.utc).isoformat(), "competing_resumes_disabled": True}
            _require(blobs.put_blob_in_cursor(cursor, key, "application/json", _json(launch), overwrite=False),
                     "this checkpoint already has a launch receipt; inspect the earlier attempt before retrying")
            sql = "UPDATE dossier_jobs SET status='analysis',error=NULL WHERE id=%s AND status='failed'"
            cursor.execute(sql if db._is_postgres() else sql.replace("%s", "?"), (job_id,))
            _require(cursor.rowcount == 1, "job changed before launch")
            lock_conn.commit()
            launched = True
            _run_normal(job_id)
            after_receipt, after = _snapshot(cursor, job_id)
            _require(all(after["calls"].get(k) == v for k, v in before["calls"].items()), "saved call prefix changed during recovery")
            _require(all(after["analysis"].get(k) == v for k, v in before["analysis"].items()), "saved phase prefix changed during recovery")
            _require(after["read_inputs"] == before["read_inputs"] and after["packet_sha256"] == before["packet_sha256"],
                     "frozen packet or source windows changed during recovery")
            result = {"status": after_receipt["status"], "applied": True, "job_id": job_id, "launch_artifact": key,
                      "complete": after.get("complete") is True, "checkpoint_artifact": checkpoint_ref, "saved_call_prefix_unchanged": True,
                      "saved_phase_prefix_unchanged": True, "read_inputs_unchanged": True,
                      "additional_calls": len(after["calls"]) - len(before["calls"]),
                      "cost_before_usd": before["cost_usd"], "cost_after_usd": after["cost_usd"],
                      "after": after_receipt, "finished_at": datetime.now(timezone.utc).isoformat()}
            blobs.put_blob_in_cursor(cursor, key + ":result", "application/json", _json(result), overwrite=False)
            lock_conn.commit()
            return result
        except Exception:
            lock_conn.rollback()
            if launched:
                sql = "UPDATE dossier_jobs SET status='failed',error='admin continuation interrupted; inspect launch receipt' WHERE id=%s AND status='analysis'"
                cursor.execute(sql if db._is_postgres() else sql.replace("%s", "?"), (job_id,))
                lock_conn.commit()
            raise
        finally:
            if sqlite_lock:
                sqlite_lock.close()
            if pg_locked:
                # get_connection returns pooled connections: release the session
                # lock explicitly before returning this one to the pool.
                try:
                    lock_conn.rollback()
                    cursor.execute("SELECT pg_advisory_unlock(hashtext(%s))", ("field-admin-continuation:" + job_id,))
                    lock_conn.commit()
                except Exception:
                    lock_conn.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_id")
    parser.add_argument("--module-dir", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--preflight", type=Path, help="JSON output from the matching dry-run")
    parser.add_argument("--competing-resumes-disabled", action="store_true")
    args = parser.parse_args(argv)
    try:
        expected = json.loads(args.preflight.read_text())["preflight"] if args.preflight else None
        result = resume(args.job_id, args.module_dir, apply=args.apply, expected=expected,
                        competing_resumes_disabled=args.competing_resumes_disabled)
    except ValueError as exc:
        parser.exit(1, f"Continuation refused: {exc}\n")
    except Exception as exc:
        parser.exit(1, f"Continuation stopped ({type(exc).__name__}); inspect durable job and launch receipts before retrying.\n")
    print(json.dumps(result, indent=2))
    if args.apply and not (result["status"] == "done" and result["complete"]):
        parser.exit(1, "Normal runner stopped before completion; completed calls and receipts remain durable.\n")


if __name__ == "__main__":
    main()
