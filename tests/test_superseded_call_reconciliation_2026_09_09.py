"""Actual transactions, immutable-source validation, and resume-safe accounting."""
import copy
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import pytest

from scripts import reconcile_superseded_investigation_call as utility
from src.dossier import blob_store as blobs
from src.dossier.schemas import DossierJob, Receipt, Totals
from src.dossier.store import compute_totals
from src.executor import db

JOB = "dossier-reconciliation-test"
UID = "referee:436379"
STAGE = "read:field:" + UID


def raw(value):
    return json.dumps(value, ensure_ascii=False).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def state():
    return json.loads(blobs.get_blob("investigation:" + JOB)[1])


def job():
    return db.execute("SELECT * FROM dossier_jobs WHERE id=%s", (JOB,), fetch="one")


def snapshot():
    return (job(), db.execute("SELECT * FROM dossier_blobs ORDER BY blob_key", fetch="all"),
            db.execute("SELECT * FROM dossier_blob_chunks ORDER BY blob_key,chunk_index", fetch="all"))


@pytest.fixture
def stored(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "reconcile.sqlite")
    monkeypatch.setattr(blobs, "_ready", False)
    blobs.ensure_table()
    db.execute("CREATE TABLE dossier_jobs (id TEXT PRIMARY KEY,status TEXT,receipts_json TEXT,totals_json TEXT,analysis_json TEXT,updated_at TEXT)")
    packet = {"kind": "field_investigation", "field": [{"uid": UID, "source_key": "field:" + UID,
               "body_sha256": digest(b"Original source") }], "primary": []}
    provider = {"model_used": "openrouter/openai/gpt-5.6-sol", "input_tokens": 36799,
                "output_tokens": 4660, "cost_usd": 0.1202, "duration_ms": 75955}
    old = {"phase_number": 23, "stage": STAGE, "engine_key": "field_investigation_field_read",
           "depth": "surface", "final_output": "The complete old paid response.", "final_wall": {},
           "cost_usd": 0.1202, "sources": ["field:" + UID], "finished": "2026-09-08T21:38:26+00:00",
           "calls": [provider]}
    old_output_hash = digest(old["final_output"].encode())
    original_snapshot = raw({"23": old})
    original_key = "dossier-json:" + digest(original_snapshot)
    blobs.put_blob(original_key, "application/json", original_snapshot)
    canonical = {"engine_key": old["engine_key"], "model": provider["model_used"],
                 "cost_usd": 0.1201, "final_output": "The canonical new paid response.",
                 "calls": [{**provider, "cost_usd": 0.1201, "output_tokens": 4651}]}
    analysis = {"23": {**old, **canonical}}
    checkpoint = {"kind": "field_investigation", "complete": True, "running_stage": None,
                  "packet_sha256": digest(raw(packet)), "calls": {STAGE: canonical},
                  "cost_usd": 0.1201, "analysis": analysis, "readings": [{"uid": UID, "reading": "Canonical reading"}],
                  "evidence": [{"citation_id": UID + "/F1", "quote": "Original source"}], "memo": "Unchanged memo.",
                  "updated_at": "before", "current_stage": "done", "coverage": {"read_count": 1}}
    archive = {"job_id": JOB, "kind": "superseded_reading", "packet_sha256": checkpoint["packet_sha256"],
               "source_uid": UID, "stage": STAGE, "extra_cost_usd": 0.1202,
               "reading": {**packet["field"][0], "source_role": "field"},
               "accounting_adjustment": {"cost_usd": 0.1202, "input_tokens": 36799, "output_tokens": 4660, "llm_calls": 1},
               "raw_provider_output_recovery": {"status": "complete", "raw_phase": old,
                    "raw_output_sha256": old_output_hash, "snapshot_sha256": digest(original_snapshot),
                    "immutable_blob_key": original_key}}
    archive_key = f"investigation-superseded-reading:{JOB}:{UID}:{old_output_hash}"
    archive_bytes = raw(archive)
    blobs.put_blob(archive_key, "application/json", archive_bytes)
    storage_receipt = {"key": archive_key, "sha256": digest(archive_bytes), "bytes": len(archive_bytes),
                       "archived_full_provider_output": True, "extra_cost_usd": 0.1202}
    blobs.put_blob("investigation-context:" + JOB, "application/json", raw(packet))
    blobs.put_blob("investigation:" + JOB, "application/json", raw(checkpoint))
    receipts = [Receipt(step="analysis", kind="llm", model=provider["model_used"],
                        **utility._receipt_for(STAGE, canonical), ts="2026-09-08T21:39:20+00:00").model_dump()]
    totals = compute_totals(receipts, {"duration_ms": 123456, "step_durations_ms": {"analysis": 123456}})
    db.execute("INSERT INTO dossier_jobs VALUES (%s,%s,%s,%s,%s,%s)",
               (JOB, "done", json.dumps(receipts), json.dumps(totals), json.dumps(analysis), "before"))
    return {"receipt": storage_receipt, "archive": archive, "packet": packet, "checkpoint": checkpoint}


def test_dry_run_is_read_only_and_describes_exact_adjustment(stored, monkeypatch):
    before = snapshot()
    monkeypatch.setattr(blobs, "put_blob_in_cursor", lambda *a, **k: pytest.fail("dry-run wrote a blob"))
    result = utility.reconcile(JOB, stored["receipt"])
    assert result["status"] == "would_apply" and not result["applied"]
    assert result["before_cost_usd"] == 0.1201 and result["after_cost_usd"] == 0.2403
    assert (result["added_provider_calls"], result["added_input_tokens"], result["added_output_tokens"]) == (1, 36799, 4660)
    assert snapshot() == before


def test_apply_is_atomic_idempotent_and_preserves_canonical_research(stored):
    before = state()
    before_row = job()
    result = utility.reconcile(JOB, stored["receipt"], apply=True)
    after = state()
    assert result["status"] == "applied"
    for key in ("analysis", "readings", "evidence", "memo", "coverage", "packet_sha256"):
        assert after[key] == before[key]
    assert after["calls"][STAGE] == before["calls"][STAGE]
    assert after["calls"][result["ledger_key"]]["final_output"] == stored["archive"]["raw_provider_output_recovery"]["raw_phase"]["final_output"]
    assert job()["analysis_json"] == before_row["analysis_json"]
    totals = json.loads(job()["totals_json"])
    assert totals["cost_usd"] == after["cost_usd"] == 0.2403
    assert totals["llm_calls"] == 2 and totals["input_tokens"] == 73598 and totals["output_tokens"] == 9311
    assert totals["step_costs_usd"]["analysis"] == 0.2403
    assert totals["duration_ms"] == 123456 and totals["step_durations_ms"] == {"analysis": 123456}
    receipt = json.loads(job()["receipts_json"])[-1]
    assert receipt["result_hash"] == stored["archive"]["raw_provider_output_recovery"]["raw_output_sha256"]
    assert receipt["duration_ms"] == 75955
    committed = snapshot()
    assert utility.reconcile(JOB, stored["receipt"], apply=True)["status"] == "already_applied"
    assert utility.reconcile(JOB, stored["receipt"])["status"] == "already_applied"
    assert snapshot() == committed


@pytest.mark.parametrize("condition", ["running", "incomplete", "active_stage"])
def test_refuses_before_terminal_completion(stored, condition):
    if condition == "running":
        db.execute("UPDATE dossier_jobs SET status='analysis'")
    else:
        current = state()
        current["complete" if condition == "incomplete" else "running_stage"] = False if condition == "incomplete" else STAGE
        blobs.put_blob("investigation:" + JOB, "application/json", raw(current))
    before = snapshot()
    with pytest.raises(ValueError, match="done|complete and idle"):
        utility.reconcile(JOB, stored["receipt"], apply=True)
    assert snapshot() == before


@pytest.mark.parametrize("corruption", ["receipt_hash", "packet", "source_hash", "raw_output", "snapshot", "usage", "receipt_usage", "total", "analysis"])
def test_rejects_conflicting_hashes_usage_and_receipts(stored, corruption):
    receipt = copy.deepcopy(stored["receipt"])
    archive = copy.deepcopy(stored["archive"])
    if corruption == "receipt_hash":
        receipt["sha256"] = "0" * 64
    elif corruption == "packet":
        packet = {**stored["packet"], "changed": True}
        blobs.put_blob("investigation-context:" + JOB, "application/json", raw(packet))
    elif corruption in ("source_hash", "raw_output", "usage"):
        if corruption == "source_hash": archive["reading"]["body_sha256"] = "0" * 64
        elif corruption == "raw_output": archive["raw_provider_output_recovery"]["raw_phase"]["final_output"] += " changed"
        else: archive["accounting_adjustment"]["input_tokens"] += 1
        data = raw(archive)
        blobs.put_blob(receipt["key"], "application/json", data)
        receipt.update(sha256=digest(data), bytes=len(data))
    elif corruption == "snapshot":
        blobs.put_blob(archive["raw_provider_output_recovery"]["immutable_blob_key"], "application/json", b"{}")
    elif corruption == "receipt_usage":
        rows = json.loads(job()["receipts_json"]); rows[0]["input_tokens"] += 1
        db.execute("UPDATE dossier_jobs SET receipts_json=%s", (json.dumps(rows),))
    elif corruption == "total":
        totals = json.loads(job()["totals_json"]); totals["cost_usd"] += 1
        db.execute("UPDATE dossier_jobs SET totals_json=%s", (json.dumps(totals),))
    else:
        db.execute("UPDATE dossier_jobs SET analysis_json='{}'")
    before = snapshot()
    with pytest.raises(ValueError):
        utility.reconcile(JOB, receipt, apply=True)
    assert snapshot() == before


def test_row_failure_rolls_back_large_checkpoint_chunks_and_receipts(stored):
    current = state(); current["evidence"][0]["large_preserved_payload"] = os.urandom(1_200_000).hex()
    blobs.put_blob("investigation:" + JOB, "application/json", raw(current))
    assert db.execute("SELECT COUNT(*) AS n FROM dossier_blob_chunks WHERE blob_key=%s", ("investigation:" + JOB,), fetch="one")["n"] > 1
    db.execute("CREATE TRIGGER fail_reconciliation BEFORE UPDATE OF receipts_json ON dossier_jobs BEGIN SELECT RAISE(ABORT, 'injected failure'); END")
    before = snapshot()
    with pytest.raises(Exception, match="injected failure"):
        utility.reconcile(JOB, stored["receipt"], apply=True)
    assert snapshot() == before


def test_concurrent_applies_charge_once(stored):
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: utility.reconcile(JOB, stored["receipt"], apply=True), range(2)))
    assert sorted(r["status"] for r in results) == ["already_applied", "applied"]
    assert json.loads(job()["totals_json"])["cost_usd"] == 0.2403


def test_large_referenced_receipts_use_same_transaction_and_bounded_blobs(stored):
    rows = json.loads(job()["receipts_json"])
    rows.append(Receipt(step="figures", kind="image", label=os.urandom(600000).hex(), cost_usd=0.5).model_dump())
    totals = compute_totals(rows, json.loads(job()["totals_json"]))
    with db.get_connection() as conn:
        c = conn.cursor()
        encoded = utility._store_column(c, rows)
        c.execute("UPDATE dossier_jobs SET receipts_json=?,totals_json=?", (encoded, json.dumps(totals)))
        conn.commit()
    assert utility.REF in json.loads(job()["receipts_json"])
    utility.reconcile(JOB, stored["receipt"], apply=True)
    with db.get_connection() as conn:
        restored = utility._column_json(conn.cursor(), job()["receipts_json"])
    assert restored[:-1] == rows
    assert json.loads(job()["totals_json"])["cost_usd"] == 0.7403
    assert db.execute("SELECT MAX(length(data)) AS size FROM dossier_blob_chunks", fetch="one")["size"] <= 512 * 1024


def test_partial_previous_accounting_is_rejected(stored):
    applied = utility.reconcile(JOB, stored["receipt"], apply=True)
    current = state(); del current["accounting_reconciliations"][applied["ledger_key"]]
    blobs.put_blob("investigation:" + JOB, "application/json", raw(current))
    before = snapshot()
    with pytest.raises(ValueError, match="partial or conflicting"):
        utility.reconcile(JOB, stored["receipt"], apply=True)
    assert snapshot() == before


def test_previously_added_untracked_analysis_receipt_cannot_be_billed_again(stored):
    rows = json.loads(job()["receipts_json"])
    rows.append(Receipt(step="analysis", label="manual extra call", cost_usd=0.1202,
                        input_tokens=36799, output_tokens=4660).model_dump())
    totals = compute_totals(rows, json.loads(job()["totals_json"]))
    db.execute("UPDATE dossier_jobs SET receipts_json=%s,totals_json=%s", (json.dumps(rows), json.dumps(totals)))
    before = snapshot()
    with pytest.raises(ValueError, match="outside the call ledger"):
        utility.reconcile(JOB, stored["receipt"], apply=True)
    assert snapshot() == before


def test_existing_runtime_save_preserves_reconciled_call_accounting(stored, monkeypatch):
    utility.reconcile(JOB, stored["receipt"], apply=True)
    from src.dossier import investigation, events
    from src.readings import registry
    monkeypatch.setattr(registry, "index_job", lambda *a, **k: None)
    monkeypatch.setattr(events, "emit", lambda *a, **k: None)
    record = DossierJob(id=JOB, status="done", totals=Totals(**json.loads(job()["totals_json"])))
    captured = []
    def cached_executor(packet, bodies, *, call, save, state, **kwargs):
        # Invoke the actual runtime accounting callback with the saved ledger.
        save(state)
        return state
    docs = [SimpleNamespace(key="investigation", role="plan", text=raw(stored["packet"]).decode())]
    investigation.run_job_investigation(record, docs, chain="field_investigation", executor=cached_executor,
                                       persist=lambda **fields: captured.append(fields))
    fields = captured[-1]
    assert fields["totals"].cost_usd == 0.2403 and fields["totals"].llm_calls == 2
    assert fields["totals"].input_tokens == 73598 and fields["totals"].output_tokens == 9311
    assert len(fields["receipts"]) == 2
    db.execute("UPDATE dossier_jobs SET receipts_json=%s,totals_json=%s", (
        json.dumps([r.model_dump() for r in fields["receipts"]]), json.dumps(fields["totals"].model_dump())))
    assert utility.reconcile(JOB, stored["receipt"], apply=True)["status"] == "already_applied"


def test_cli_defaults_to_dry_run(stored, tmp_path, monkeypatch, capsys):
    receipt_file = tmp_path / "receipt.json"; receipt_file.write_text(json.dumps(stored["receipt"]))
    called = []
    monkeypatch.setattr(utility, "reconcile", lambda job_id, receipt, *, apply: called.append(apply) or {"applied": apply})
    utility.main([JOB, "--receipt", str(receipt_file)])
    utility.main([JOB, "--receipt", str(receipt_file), "--apply"])
    assert called == [False, True]
    assert "sha256" not in capsys.readouterr().out
