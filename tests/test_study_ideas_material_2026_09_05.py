"""Offline guardrails for a study that launches paid calls only after explicit approval."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import study_ideas_material as study


@pytest.fixture
def source_dir(tmp_path):
    root = tmp_path / "sources"
    root.mkdir()
    for filename in list(study.PAPERS.values()) + [f for group in study.CORPORA.values() for f in group]:
        (root / filename).write_text(f"The source contains a sufficiently long quotation for this test. {filename}")
    return root


def response(content="A reading\n\n## Findings ledger\n- [F1] A finding — anchor: \"The source contains a sufficiently long quotation for this test.\" — confidence: high", **kwargs):
    return {"content": content, "model_used": study.ROUTING["strong"], "input_tokens": 100,
            "output_tokens": 20, **kwargs}


def output_record(output_dir, key, text="valid output"):
    path = output_dir / "outputs" / f"{key}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return {"status": "complete", "output": str(path.relative_to(output_dir)),
            "output_sha256": study.digest(path.read_bytes())}


def test_default_and_explicit_dry_run_never_call_or_write(source_dir, tmp_path, monkeypatch, capsys):
    def forbidden(*args, **kwargs):
        pytest.fail("A dry run attempted paid execution")
    monkeypatch.setattr(study, "execute", forbidden)
    monkeypatch.setattr(study, "run_engine_call_auto", forbidden)
    monkeypatch.setattr(study, "run_engine_call", forbidden)
    out = tmp_path / "not-created"
    for mode in ([], ["--dry-run"]):
        assert study.main(["--source-dir", str(source_dir), "--output-dir", str(out), *mode]) == 0
        printed = capsys.readouterr().out
        assert "28 generations, 24 Sonnet judgments" in printed
        assert "144 planned base calls" in printed
        assert "judge__epistemological_method_detector__chen__checked_first" in printed
        assert "conditions_of_possibility_analyzer__deep__deutschmann" in printed
        assert not out.exists()


def test_full_matrix_and_source_hash_identity(source_dir):
    plan, sources = study.build_plan(source_dir)
    assert len(plan["generations"]) == 28 and len(plan["judgments"]) == 24
    assert {j["source"] for j in plan["judgments"]} == set(study.PAPERS)
    assert all(len(sources[key]) == 3 for key in study.CORPORA)
    assert len(set(sources["deutschmann"])) == 3
    assert plan["identity"] == study.build_plan(source_dir)[0]["identity"]
    (source_dir / study.PAPERS["harris"]).write_text("Revised source.")
    changed, _ = study.build_plan(source_dir)
    assert changed["identity"] != plan["identity"]
    assert len({j["key"] for j in plan["generations"] + plan["judgments"]}) == 52


def test_run_requires_explicit_finite_budget(source_dir, monkeypatch):
    monkeypatch.setattr(study, "execute", lambda *a: pytest.fail("launched without budget"))
    for args in ([], ["--budget-usd", "0"], ["--budget-usd", "nan"], ["--budget-usd", "inf"]):
        with pytest.raises(SystemExit):
            study.main(["--run", "--source-dir", str(source_dir), *args])


def test_call_receipt_survives_partial_response_and_stops_budget(tmp_path, monkeypatch):
    monkeypatch.setattr(study, "run_engine_call_auto", lambda **kw: response(partial=True))
    invoke = study.Recorder(tmp_path, tmp_path / "receipts/job/attempt", 1)
    with pytest.raises(ValueError, match="partial"):
        invoke("system", "source", model_hint=study.ROUTING["strong"])
    summary = study.receipts_summary(tmp_path)
    assert summary == {"calls": 1, "cost_usd": .0004, "input_tokens": 100,
                       "output_tokens": 20, "uncosted_calls": 0, "retry_calls": 0, "failed_calls": 1}
    receipt = json.loads((tmp_path / "receipts/job/attempt/call-0001.json").read_text())
    assert receipt["partial"] is True and receipt["status"] == "failed"
    assert (tmp_path / "receipts/job/attempt/call-0001.md").exists()
    invoke.budget_usd = .0004
    monkeypatch.setattr(study, "run_engine_call_auto", lambda **kw: pytest.fail("budget ignored"))
    with pytest.raises(study.BudgetReached):
        invoke("system", "source", model_hint=study.ROUTING["strong"])
    assert study.receipts_summary(tmp_path)["calls"] == 1


def test_provider_error_is_unknown_cost_not_free(tmp_path, monkeypatch):
    def failed(**kw):
        raise RuntimeError("provider disconnected")
    monkeypatch.setattr(study, "run_engine_call_auto", failed)
    invoke = study.Recorder(tmp_path, tmp_path / "receipts/job/attempt", 1)
    with pytest.raises(RuntimeError, match="disconnected"):
        invoke("system", "source", model_hint=study.ROUTING["strong"])
    assert study.receipts_summary(tmp_path)["uncosted_calls"] == 1


def test_failed_process_retains_earlier_successful_call(tmp_path, monkeypatch):
    def broken(cap, spec, documents, *, call_fn, **kwargs):
        call_fn("system", "source", model_hint=study.ROUTING["strong"])
        raise RuntimeError("critic failed later")
    monkeypatch.setattr(study, "run_oneshot_checked", broken)
    monkeypatch.setattr(study, "run_engine_call_auto", lambda **kw: response())
    job = next(j for j in study.generation_jobs() if j["condition"] == "checked")
    record = study.run_job(job, {"doc": "source"}, tmp_path, {}, 1)
    assert record["status"] == "failed" and "critic failed" in record["error"]
    assert study.receipts_summary(tmp_path)["calls"] == 1
    assert study.receipts_summary(tmp_path)["cost_usd"] > 0
    assert not study.completed(record, tmp_path)


def test_checked_run_without_check_is_not_complete(tmp_path, monkeypatch):
    def unchecked(*a, **kw):
        return SimpleNamespace(final_content=response()["content"], receipts=lambda: {}, calls_for=lambda key: [])
    monkeypatch.setattr(study, "run_oneshot_checked", unchecked)
    job = next(j for j in study.generation_jobs() if j["condition"] == "checked")
    record = study.run_job(job, {"doc": "source"}, tmp_path, {}, 1)
    assert record["status"] == "failed" and "no check call" in record["error"]


def test_corpus_uses_deep_production_chain_with_all_three_docs(tmp_path, monkeypatch):
    seen = {}
    def chain(cap, spec, documents, **kwargs):
        seen.update(documents=documents, **kwargs)
        return SimpleNamespace(final_content=response()["content"], receipts=lambda: {})
    monkeypatch.setattr(study, "run_process", chain)
    job = next(j for j in study.generation_jobs() if j["kind"] == "corpus")
    docs = {f"doc{i}": "The source contains a sufficiently long quotation for this test." for i in range(3)}
    record = study.run_job(job, docs, tmp_path, {}, 1)
    assert record["status"] == "complete"
    assert seen["documents"] == docs and seen["depth"] == "deep"
    assert seen["tier_overrides"] == study.ROUTING and seen["parallelism"] == 1


@pytest.mark.parametrize("raw", ['{}', '{"winner": "unknown"}', '[{"winner": "A"}]', 'not JSON',
                                 '{"winner": "A"}', '{"winner": "A", "margin": "clear", "why": " "}'])
def test_malformed_judge_is_never_a_tie(raw):
    with pytest.raises((ValueError, json.JSONDecodeError)):
        study.parse_judgment(raw, {"A": "old", "B": "checked"})


def test_both_order_agreement_excludes_position_splits_and_incomplete(tmp_path):
    engine, paper = study.ENGINES[0], "harris"
    jobs = [j for j in study.judgment_jobs() if j["engine"] == engine and j["source"] == paper]
    results = {}
    assert study.agreement(engine, paper, results, tmp_path) == "incomplete"
    for side in ("A", "B"):
        results[jobs[0][side]] = output_record(tmp_path, jobs[0][side])
    for job in jobs:
        results[job["key"]] = {**output_record(tmp_path, job["key"]), "judgment": {"winner": job["A"]}}
    assert study.agreement(engine, paper, results, tmp_path) == "split (excluded)"
    results[jobs[0]["key"]]["judgment"]["winner"] = jobs[1]["A"]
    assert study.agreement(engine, paper, results, tmp_path) == "checked"
    results[jobs[0]["A"]]["status"] = "failed"
    assert study.agreement(engine, paper, results, tmp_path) == "incomplete"


def test_changed_dependency_or_corrupt_output_invalidates_reuse(tmp_path):
    base = output_record(tmp_path, "old")
    judged = output_record(tmp_path, "judge")
    judged["inputs_sha256"] = {"old": base["output_sha256"]}
    assert study.completed(judged, tmp_path)
    (tmp_path / "outputs/old.md").write_text("regenerated output")
    assert not study.completed(judged, tmp_path)
    assert not study.completed(base, tmp_path)


def test_successful_generation_resumes_without_another_call(tmp_path, source_dir, monkeypatch):
    plan, sources = study.build_plan(source_dir)
    plan["generations"] = plan["generations"][:1]
    plan["judgments"] = []
    monkeypatch.setattr(study, "run_engine_call_auto", lambda **kw: response())
    first = study.execute(plan, sources, tmp_path / "out", 1)
    monkeypatch.setattr(study, "run_engine_call_auto", lambda **kw: pytest.fail("successful run was repeated"))
    assert study.execute(plan, sources, tmp_path / "out", 1) == first
    assert study.receipts_summary(tmp_path / "out")["calls"] == 1
    assert "Complete 1/1; failed 0" in (tmp_path / "out/REPORT.md").read_text()
