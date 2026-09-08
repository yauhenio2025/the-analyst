"""Reviewed editions remain separate, exact, atomic, discoverable, and reusable."""
import copy
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import pytest

from scripts import import_reviewed_investigation_edition as utility
from src.dossier import blob_store as blobs
from src.executor import db
from src.readings import registry

JOB = "dossier-review-test"
UID = "referee:488418"
KEY = "field:" + UID
BODY = "First engine-inspected paragraph.\n\fSupplemental α finding on page two.\nOther omitted text."
PDF = b"%PDF-1.7\nimmutable test PDF bytes"


def raw(value):
    return json.dumps(value, ensure_ascii=False).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def state():
    return json.loads(blobs.get_blob("investigation:" + JOB)[1])


def snapshot():
    return (db.execute("SELECT * FROM dossier_jobs", fetch="all"),
            db.execute("SELECT * FROM executor_documents", fetch="all"),
            db.execute("SELECT * FROM dossier_blobs ORDER BY blob_key", fetch="all"),
            db.execute("SELECT * FROM dossier_blob_chunks ORDER BY blob_key,chunk_index", fetch="all"))


def save_state(value):
    blobs.put_blob("investigation:" + JOB, "application/json", raw(value))


@pytest.fixture
def stored(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DATABASE_URL", "")
    monkeypatch.setattr(db, "SQLITE_PATH", tmp_path / "review.sqlite")
    monkeypatch.setattr(blobs, "_ready", False)
    blobs.ensure_table()
    db.execute("CREATE TABLE dossier_jobs (id TEXT PRIMARY KEY,status TEXT,analysis_json TEXT,documents_json TEXT,receipts_json TEXT,totals_json TEXT,updated_at TEXT)")
    db.execute("CREATE TABLE executor_documents (doc_id TEXT PRIMARY KEY,text TEXT,text_encoding TEXT,char_count INTEGER,content_hash TEXT)")
    source = {"uid": UID, "source_key": KEY, "body_chars": len(BODY), "body_sha256": sha(BODY.encode()),
              "source_metadata": {"pdf_sha256": sha(PDF), "pdf_url": "https://example.org/source.pdf",
                                  "page_spans": [{"page": 999, "start": 0, "end": len(BODY)}]},
              "page_spans": [{"page": 1, "start": 0, "end": BODY.index("\f") + 1},
                             {"page": 2, "start": BODY.index("\f") + 1, "end": len(BODY)}]}
    packet = {"kind": "field_investigation", "author": {"id": "riley-dylan", "name": "Riley, Dylan"},
              "field": [source], "primary": [], "secondary": []}
    evidence = [{"citation_id": UID + "/F1", "uid": UID, "source_key": KEY, "body_sha256": source["body_sha256"],
                 "quote_verified": True, "source_quote": BODY[:5]},
                {"citation_id": UID + "/F2", "uid": UID, "source_key": KEY, "body_sha256": source["body_sha256"],
                 "quote_verified": False, "model_quote": "Supplemental finding"}]
    analysis = {"1": {"engine_key": "field_investigation_field_read", "final_output": "Original paid reading"}}
    checkpoint = {"kind": "field_investigation", "complete": True, "running_stage": None,
                  "packet_sha256": sha(raw(packet)), "analysis": analysis, "calls": {"read:" + KEY: {"cost_usd": 0.2}},
                  "cost_usd": 0.2, "memo": "Original memo [" + UID + "/F1].", "memo_validation": {"supported": True},
                  "readings": [{"source_key": KEY, "uid": UID, "body_sha256": source["body_sha256"],
                                "inspected_ranges": [[0, BODY.index("\f")]], "reading": "Original reading"}],
                  "evidence": evidence, "updated_at": "before"}
    lo = BODY.index("Supplemental")
    hi = BODY.index("\n", lo)
    proof = {"id": "proof-1", "citation_id": UID + "/Review.SSR-R1", "uid": UID, "source_key": KEY,
             "body_sha256": source["body_sha256"], "pdf_sha256": sha(PDF),
             "quote_spans": [{"start": lo, "end": hi, "text": BODY[lo:hi]}], "source_quote": BODY[lo:hi],
             "review_windows": [[lo, len(BODY)]], "finding": "A supplemental point", "locus": "p. 2",
             "qualification": "Source text verified; interpretation is external review."}
    payload = {"schema_version": 1, "kind": "reviewed_edition", "job_id": JOB,
               "packet_sha256": checkpoint["packet_sha256"], "original_memo_sha256": sha(checkpoint["memo"].encode()),
               "title": "Reviewed memo", "reviewed_memo": "Original support [" + UID + "/F1]; supplemental [" + proof["citation_id"] + "].",
               "provenance": {"reviewer": "Research desk", "reviewed_at": "2026-09-09T10:00:00Z", "method": "external_source_review_v1"},
               "source_proofs": [proof], "findings": [{"id": "R1", "kind": "revision", "status": "changed",
                   "text": "Qualified the original claim.", "support_ids": [proof["citation_id"]], "qualification": "Do not generalize."}]}
    blobs.put_blob("investigation-context:" + JOB, "application/json", raw(packet))
    save_state(checkpoint)
    db.execute("INSERT INTO executor_documents VALUES (%s,%s,%s,%s,%s)", ("doc-test", BODY, "", len(BODY), sha(BODY.encode())))
    db.execute("INSERT INTO dossier_jobs VALUES (%s,%s,%s,%s,%s,%s,%s)",
               (JOB, "done", json.dumps(analysis), json.dumps([{"key": KEY, "role": "source", "executor_doc_id": "doc-test"}]),
                '[{"kind":"llm","cost_usd":0.2}]', '{"llm_calls":1,"cost_usd":0.2}', "before"))
    canonical = {"job_id": JOB, "phase": "1", "engine": "field_investigation_field_read", "when": "2026-09-09T09:00:00Z",
                 "n_rows": 1, "cost_usd": 0.2, "renders": [], "intent": "Canonical reading", "persons": ["Riley, Dylan"],
                 "texts": [UID], "rows": [{"text": "Original row"}]}
    registry.save_reading(canonical, strict=True)
    return {"payload": payload, "packet": packet, "checkpoint": checkpoint, "canonical_reading": canonical}


def test_dry_run_has_no_writes(stored, monkeypatch):
    before = snapshot()
    monkeypatch.setattr(blobs, "put_blob_in_cursor", lambda *a, **kw: pytest.fail("dry-run wrote"))
    result = utility.import_edition(JOB, stored["payload"])
    assert result["status"] == "would_apply" and not result["applied"]
    assert result["new_provider_calls"] == 0 and result["cost_change_usd"] == 0
    assert snapshot() == before


def test_import_preserves_every_canonical_field_and_accounting(stored):
    before = snapshot()
    checkpoint = state()
    result = utility.import_edition(JOB, stored["payload"], apply=True)
    after = state()
    for k, v in checkpoint.items():
        if k != "updated_at":
            assert after[k] == v
    assert snapshot()[:2] == before[:2]
    assert registry.reading(JOB, "1") == stored["canonical_reading"]
    edition = after["reviewed_editions"][0]
    assert edition["reviewed_memo"] == stored["payload"]["reviewed_memo"]
    assert edition["findings"] == stored["payload"]["findings"]
    assert blobs.get_blob(edition["original_memo_artifact"]["key"])[1] == checkpoint["memo"].encode()
    assert sha(blobs.get_blob(edition["artifact"]["key"])[1]) == edition["artifact"]["sha256"]
    proof = edition["source_proofs"][0]
    assert proof["quote_spans"] == stored["payload"]["source_proofs"][0]["quote_spans"]
    assert proof["qualification"] and proof["locus"] == "p. 2"
    assert proof["pages"] == [2] and proof["page_urls"] == ["https://example.org/source.pdf#page=2"]
    assert proof["original_engine_window_coverage"] == "supplemental_outside_one_original_window"
    assert proof["engine_quote_verified"] is None and proof["review_quote_verified"] is True
    assert proof["pdf_verification"] == "frozen_packet_hash_bound" and proof["visual_verification"] == "not_claimed"
    reading = registry.reading(JOB, result["reading_ref"]["phase"])
    assert reading["origin"] == "external_review" and reading["engine"] == "reviewed_edition_import"
    assert reading["cost_usd"] == 0 and reading["provider_calls"] == []
    assert reading["prose"] == edition["reviewed_memo"] and reading["rows"][0]["fields"] == edition["findings"][0]
    committed = snapshot()
    assert utility.import_edition(JOB, stored["payload"], apply=True)["status"] == "already_applied"
    assert utility.import_edition(JOB, stored["payload"])["status"] == "already_applied"
    assert snapshot() == committed


def test_discoverable_in_existing_api_and_hydrates_as_separate_prior_reading(stored, monkeypatch):
    result = utility.import_edition(JOB, stored["payload"], apply=True)
    phase = result["reading_ref"]["phase"]
    for filters in ({"person": "Riley, Dylan"}, {"person": "Riley"}, {"text": UID}, {"job": JOB}):
        entries = registry.readings_for(**filters)["readings"]
        assert {e["phase"] for e in entries} == {"1", phase}
        assert next(e for e in entries if e["phase"] == phase)["intent"].startswith("External reviewed edition")
    from src.dossier.investigation import hydrate_prior_readings
    hydrated = hydrate_prior_readings({"prior_readings": [result["reading_ref"]]}, lookup_index=registry.readings_for, lookup_reading=registry.reading)
    assert hydrated["resolved_prior_readings"][0]["edition"]["source_proofs"][0]["review_quote_verified"] is True
    from src.api.routes import dossier
    monkeypatch.setattr(dossier, "_load", lambda _: SimpleNamespace(status="done", error=None,
        options=SimpleNamespace(path=SimpleNamespace(chain_key="field_investigation")),
        totals=SimpleNamespace(model_dump=lambda: {"cost_usd": 0.2})))
    answer = dossier.get_investigation(JOB)
    assert answer["memo"] == stored["checkpoint"]["memo"]
    assert answer["reviewed_editions"][0]["content_hash"] == result["content_hash"]
    assert "calls" not in answer and "analysis" not in answer


@pytest.mark.parametrize("condition", ["running", "incomplete", "active_stage"])
def test_refuses_nonterminal_or_active_checkpoint(stored, condition):
    if condition == "running":
        db.execute("UPDATE dossier_jobs SET status='analysis'")
    else:
        current = state(); current["complete" if condition == "incomplete" else "running_stage"] = False if condition == "incomplete" else "memo"
        save_state(current)
    before = snapshot()
    with pytest.raises(ValueError, match="done|complete and idle"):
        utility.import_edition(JOB, stored["payload"], apply=True)
    assert snapshot() == before


@pytest.mark.parametrize("corruption", ["memo", "packet", "body", "pdf", "offset", "quote", "fragments", "cross_window", "unknown_citation", "unverified_citation", "unknown_support", "duplicate_proof", "duplicate_finding", "source_identity"])
def test_rejects_bad_provenance_and_unsupported_citations_without_mutation(stored, corruption):
    payload = copy.deepcopy(stored["payload"]); proof = payload["source_proofs"][0]
    if corruption == "memo": payload["original_memo_sha256"] = "0" * 64
    elif corruption == "packet": payload["packet_sha256"] = "0" * 64
    elif corruption == "body": proof["body_sha256"] = "0" * 64
    elif corruption == "pdf": proof["pdf_sha256"] = "0" * 64
    elif corruption == "offset": proof["quote_spans"][0]["start"] += 1
    elif corruption == "quote": proof["quote_spans"][0]["text"] += "invention"
    elif corruption == "fragments": proof["source_quote"] += "invention"
    elif corruption == "cross_window":
        lo, hi = proof["quote_spans"][0]["start"], proof["quote_spans"][0]["end"]
        proof["review_windows"] = [[lo, lo + 5], [lo + 5, hi]]
    elif corruption == "unknown_citation": payload["reviewed_memo"] += " [referee:999/F1]"
    elif corruption == "unverified_citation": payload["reviewed_memo"] += " [" + UID + "/F2]"
    elif corruption == "unknown_support": payload["findings"][0]["support_ids"] = [UID + "/missing"]
    elif corruption == "duplicate_proof": payload["source_proofs"].append(copy.deepcopy(proof))
    elif corruption == "duplicate_finding": payload["findings"].append(copy.deepcopy(payload["findings"][0]))
    else: proof["citation_id"] = "referee:other/F1"
    before = snapshot()
    with pytest.raises(ValueError):
        utility.import_edition(JOB, payload, apply=True)
    assert snapshot() == before


def test_existing_unverified_id_upgrades_only_within_review_edition(stored):
    payload = stored["payload"]
    old = payload["source_proofs"][0]["citation_id"]
    payload["source_proofs"][0]["citation_id"] = UID + "/F2"
    payload["reviewed_memo"] = payload["reviewed_memo"].replace(old, UID + "/F2")
    payload["findings"][0]["support_ids"] = [UID + "/F2"]
    utility.import_edition(JOB, payload, apply=True)
    current = state()
    assert current["evidence"][1]["quote_verified"] is False
    proof = current["reviewed_editions"][0]["source_proofs"][0]
    assert proof["review_quote_verified"] is True and proof["engine_quote_verified"] is False


def test_exact_disjoint_fragments_and_engine_window_coverage(stored):
    proof = stored["payload"]["source_proofs"][0]
    proof["quote_spans"] = [{"start": 0, "end": 5, "text": BODY[:5]}, {"start": 10, "end": 20, "text": BODY[10:20]}]
    proof["source_quote"] = BODY[:5] + BODY[10:20]
    proof["review_windows"] = [[0, 30]]
    utility.import_edition(JOB, stored["payload"], apply=True)
    found = state()["reviewed_editions"][0]["source_proofs"][0]
    assert found["original_engine_window_coverage"] == "inside_one_original_window"
    assert found["quote_spans"] == proof["quote_spans"]
    assert found["pages"] == [1]


def test_markdown_links_notes_and_citation_punctuation(stored):
    stored["payload"]["reviewed_memo"] += "\n[Note 1](https://example.com/referee:999/F1) and [^1], [section/notes], bare " + UID + "/F1."
    utility.import_edition(JOB, stored["payload"])
    assert utility._memo_ids("[referee:488418/Review.SSR-R1](https://example.org)") == [UID + "/Review.SSR-R1"]


def test_visual_audit_requires_both_durable_artifacts_and_source_binding(stored):
    audit = {"uid": UID, "body_sha256": sha(BODY.encode()), "pdf_sha256": sha(PDF),
             "reviewed_from_pdf": True, "method": "manual_pdf_review", "pages": [{"page": 2}]}
    audit_raw = raw(audit)
    pdf_ref, audit_ref = utility._reference("test-pdf", PDF), utility._reference("test-audit", audit_raw)
    stored["payload"]["source_proofs"][0]["visual_audit"] = {"reviewed_from_pdf": True, "pdf_receipt": pdf_ref, "audit_receipt": audit_ref}
    with pytest.raises(ValueError, match="artifact is missing"):
        utility.import_edition(JOB, stored["payload"])
    blobs.put_blob("test-pdf", "application/pdf", PDF)
    blobs.put_blob("test-audit", "application/json", audit_raw)
    utility.import_edition(JOB, stored["payload"], apply=True)
    assert state()["reviewed_editions"][0]["source_proofs"][0]["visual_verification"] == "reviewer_attested_with_verified_artifact_hashes"


def test_concurrent_imports_create_exactly_one_edition_and_reading(stored):
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: utility.import_edition(JOB, stored["payload"], apply=True), range(2)))
    assert sorted(r["status"] for r in results) == ["already_applied", "applied"]
    assert len(state()["reviewed_editions"]) == 1 and registry.readings_for(job=JOB)["count"] == 2


def test_failure_after_staging_readings_rolls_back_all_artifacts_and_chunks(stored):
    current = state(); current["preserved_data"] = os.urandom(1200000).hex(); save_state(current)
    db.execute("CREATE TRIGGER fail_review BEFORE UPDATE ON dossier_blobs WHEN NEW.blob_key='investigation:" + JOB + "' BEGIN SELECT RAISE(ABORT, 'injected review failure'); END")
    before = snapshot()
    with pytest.raises(Exception, match="injected review failure"):
        utility.import_edition(JOB, stored["payload"], apply=True)
    assert snapshot() == before


def test_multiple_editions_preserve_original_snapshot_and_prior_readings(stored):
    first = utility.import_edition(JOB, stored["payload"], apply=True)
    second_payload = {**stored["payload"], "title": "Second external edition"}
    second = utility.import_edition(JOB, second_payload, apply=True)
    assert first["original_memo_artifact"] == second["original_memo_artifact"]
    assert len(state()["reviewed_editions"]) == 2 and registry.readings_for(job=JOB)["count"] == 3
    assert utility.import_edition(JOB, stored["payload"], apply=True)["status"] == "already_applied"


def test_partial_or_tampered_import_is_refused(stored):
    result = utility.import_edition(JOB, stored["payload"], apply=True)
    blobs.put_blob("reading:" + JOB + ":" + result["reading_ref"]["phase"], "application/json", b"{}")
    before = snapshot()
    with pytest.raises(ValueError, match="reading changed"):
        utility.import_edition(JOB, stored["payload"], apply=True)
    assert snapshot() == before


def test_compressed_document_decode_uses_existing_cursor(stored, monkeypatch):
    capsule = raw({"text": BODY})
    blobs.put_blob("executor-document:" + sha(BODY.encode()), "application/json", capsule)
    db.execute("UPDATE executor_documents SET text=%s,text_encoding='blob-json-v1'", ("executor-document:" + sha(BODY.encode()),))
    monkeypatch.setattr(blobs, "get_blob", lambda *a, **kw: pytest.fail("nested blob connection"))
    utility.import_edition(JOB, stored["payload"], apply=True)


def test_cli_defaults_to_dry_run_and_reports_metadata_only(stored, tmp_path, capsys):
    path = tmp_path / "payload.json"; path.write_text(json.dumps(stored["payload"]))
    before = snapshot()
    utility.main([JOB, "--payload", str(path)])
    output = capsys.readouterr().out
    assert json.loads(output)["status"] == "would_apply" and "Supplemental α" not in output
    assert snapshot() == before


def test_duplicate_citation_variants_use_any_verified_source_positive_row(stored):
    current = state()
    positive = current["evidence"][0]
    current["evidence"] += [copy.deepcopy(positive), {**positive, "quote_verified": False, "doc": ""}]
    save_state(current)
    payload = stored["payload"]
    p = copy.deepcopy(payload["source_proofs"][0]); p.update(id="engine-proof", citation_id=UID + "/F1",
        quote_spans=[{"start": 0, "end": 5, "text": BODY[:5]}], source_quote=BODY[:5], review_windows=[[0, 20]])
    payload["source_proofs"].append(p)
    utility.import_edition(JOB, payload, apply=True)
    assert state()["evidence"] == current["evidence"]
    imported = state()["reviewed_editions"][0]
    assert imported["source_proofs"][1]["engine_quote_verified"] is True
    assert next(c for c in imported["verification"]["citation_support"] if c["citation_id"] == UID + "/F1")["engine_verification"] == "verified"


def test_gapped_fragments_are_explicitly_discontinuous(stored):
    proof = stored["payload"]["source_proofs"][0]
    proof["quote_spans"] = [{"start": 0, "end": 5, "text": BODY[:5]}, {"start": 10, "end": 20, "text": BODY[10:20]}]
    proof["source_quote"] = BODY[:5] + BODY[10:20]; proof["review_windows"] = [[0, 30]]
    proof.update(quote_start=0, quote_end=20, quote_verified=True, quote_match="pdf_column_layout")
    utility.import_edition(JOB, stored["payload"], apply=True)
    exposed = state()["reviewed_editions"][0]["source_proofs"][0]
    assert exposed["passage_form"] == "ordered_discontinuous_fragments" and exposed["continuous_quote"] is False
    assert "quote_start" not in exposed and "quote_end" not in exposed and "quote_verified" not in exposed
    assert exposed["quote_match"] == "review_exact_source_fragments" and exposed["normalization"] == "none"
    assert exposed["source_quote"] not in BODY


def test_large_edition_uses_bounded_chunks_and_round_trips(stored):
    payload = stored["payload"]
    payload["reviewed_memo"] += "\n" + os.urandom(900000).hex()
    result = utility.import_edition(JOB, payload, apply=True)
    assert state()["reviewed_editions"][0]["reviewed_memo"] == payload["reviewed_memo"]
    assert registry.reading(JOB, result["reading_ref"]["phase"])["prose"] == payload["reviewed_memo"]
    assert db.execute("SELECT MAX(length(data)) AS size FROM dossier_blob_chunks", fetch="one")["size"] <= 512 * 1024
    assert db.execute("SELECT MAX(length(data)) AS size FROM dossier_blobs", fetch="one")["size"] <= 512 * 1024


def test_legacy_source_spans_alias_normalizes_to_same_idempotent_edition(stored):
    payload = stored["payload"]
    result = utility.import_edition(JOB, payload, apply=True)
    alias = copy.deepcopy(payload)
    p = alias["source_proofs"][0]; p["source_spans"] = p.pop("quote_spans")
    assert utility.import_edition(JOB, alias, apply=True)["content_hash"] == result["content_hash"]
    assert len(state()["reviewed_editions"]) == 1


def test_finding_text_cannot_hide_an_unsupported_inline_citation(stored):
    stored["payload"]["findings"][0]["text"] += " [referee:unknown/F1]"
    with pytest.raises(ValueError, match="finding text has unresolved citations"):
        utility.import_edition(JOB, stored["payload"])


def test_missing_shared_index_relinks_without_changing_edition_or_research(stored):
    utility.import_edition(JOB, stored["payload"], apply=True)
    before_state = blobs.get_blob("investigation:" + JOB)[1]
    key = registry._index_key("text", UID)
    original_index = blobs.get_blob(key)[1]
    entries = [e for e in json.loads(original_index) if not e["phase"].startswith("review:")]
    blobs.put_blob(key, "application/json", raw(entries))
    before = snapshot()
    result = utility.import_edition(JOB, stored["payload"])
    assert result["status"] == "would_relink" and result["index_verification"]["missing_keys"] == [key]
    assert snapshot() == before
    repaired = utility.import_edition(JOB, stored["payload"], apply=True)
    assert repaired["status"] == "relinked" and repaired["index_verification"]["status"] == "present"
    assert blobs.get_blob("investigation:" + JOB)[1] == before_state
    assert json.loads(blobs.get_blob(key)[1]) == json.loads(original_index)


def test_conflicting_index_entry_is_not_silently_overwritten(stored):
    utility.import_edition(JOB, stored["payload"], apply=True)
    key = registry._index_key("text", UID)
    entries = json.loads(blobs.get_blob(key)[1]); entries[-1]["engine"] = "fabricated_engine"
    blobs.put_blob(key, "application/json", raw(entries))
    before = snapshot()
    with pytest.raises(ValueError, match="conflicting content"):
        utility.import_edition(JOB, stored["payload"], apply=True)
    assert snapshot() == before


def test_postcommit_index_race_reports_durable_result_and_relink_instruction(stored, tmp_path, monkeypatch, capsys):
    path = tmp_path / "payload.json"; path.write_text(json.dumps(stored["payload"]))
    monkeypatch.setattr(utility, "_verify_indexes", lambda *a: {"status": "missing", "missing_keys": ["readings:text:" + UID], "conflicting_keys": []})
    with pytest.raises(SystemExit) as raised:
        utility.main([JOB, "--payload", str(path), "--apply"])
    assert raised.value.code == 1
    captured = capsys.readouterr()
    assert json.loads(captured.out)["status"] == "applied"
    assert "Edition is durable" in captured.err and "--apply" in captured.err
    assert len(state()["reviewed_editions"]) == 1


def test_visual_audit_cannot_extend_approval_to_an_unreviewed_region(stored):
    audit = {"uid": UID, "body_sha256": sha(BODY.encode()), "pdf_sha256": sha(PDF),
             "reviewed_from_pdf": True, "method": "manual_pdf_review", "pages": [{"page": 2, "reviewed_start": len(BODY) - 5, "reviewed_end": len(BODY)}]}
    audit_raw = raw(audit)
    blobs.put_blob("test-pdf", "application/pdf", PDF)
    blobs.put_blob("test-audit", "application/json", audit_raw)
    stored["payload"]["source_proofs"][0]["visual_audit"] = {"reviewed_from_pdf": True,
        "pdf_receipt": utility._reference("test-pdf", PDF), "audit_receipt": utility._reference("test-audit", audit_raw)}
    with pytest.raises(ValueError, match="visually reviewed page region"):
        utility.import_edition(JOB, stored["payload"])
