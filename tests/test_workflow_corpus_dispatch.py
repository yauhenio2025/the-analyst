"""Offline dispatch regressions: source scope survives workflow, process and desk adapters."""
import json
import re
import time
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from src.aoi.constants import AOI_WORKFLOW_KEY
from src.executor import chain_runner as cr, phase_runner as pr
from src.executor.document_ids import normalize_document_ids
from src.executor.ledger_walls import parse_rows, render_rows
from src.orchestrator.schemas import PhaseExecutionSpec
from src.sources.schemas import Document
from src.stages.process_composer import LEDGER_HEADING
from src.workflows.schemas import WorkflowPhase

ENGINE = "conditions_of_possibility_analyzer"
SECOND = "inferential_commitment_mapper"
ALPHA = "The first source makes a claim supported by explicit evidence."
BETA = "The second source revises that claim using a different method."


@pytest.fixture(autouse=True)
def no_provider_calls(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("offline test attempted a provider call")
    monkeypatch.setattr("src.executor.engine_runner.get_backend", forbidden)
    monkeypatch.setattr("src.executor.process_runner._default_call", forbidden)


@pytest.fixture
def source_job(monkeypatch):
    plan = {
        "workflow_key": AOI_WORKFLOW_KEY, "target_work": {"title": "Target title"},
        "selected_source_thinker_id": "chosen", "selected_source_thinker_name": "Chosen Thinker",
        "prior_works": [
            {"title": "A-B", "source_thinker_id": "chosen", "source_document_id": "source_a"},
            {"title": "A B", "source_thinker_id": "chosen", "source_document_id": "source_b"},
            {"title": "Other", "source_thinker_id": "other", "source_document_id": "other"},
        ],
    }
    texts = {"doc-target": "Target source text.", "doc-a": ALPHA, "doc-b": BETA, "doc-other": "Other thinker text."}
    ids = {"Target title": "doc-target", "A-B": "doc-a", "A B": "doc-b", "Other": "doc-other"}
    monkeypatch.setattr(pr, "get_job", lambda _: {"plan_data": plan})
    monkeypatch.setattr(pr, "get_document_text", texts.get)
    monkeypatch.setattr("src.executor.document_inputs.get_document_text", texts.get)
    return plan, texts, ids


def _phase(number, **kwargs):
    return PhaseExecutionSpec(phase_number=number, phase_name="test phase", engine_key=ENGINE, **kwargs)


def _run_phase(plan, ids, **kwargs):
    wf = WorkflowPhase(phase_number=plan.phase_number, phase_name=plan.phase_name,
                       engine_key=ENGINE, depends_on_phases=plan.depends_on or [])
    return pr.run_phase(wf, plan, job_id="offline-job", document_ids=ids, **kwargs)


def _capture_dispatch(monkeypatch):
    calls = []
    def run(**kwargs):
        calls.append(kwargs)
        return {"engine_results": {}, "final_output": "Primary generated output", "total_tokens": 0}
    monkeypatch.setattr(pr, "run_chain", run)
    monkeypatch.setattr(pr, "run_single_engine", run)
    return calls


@pytest.mark.parametrize("number,keys", [(1.0, {"source_a", "source_b"}),
                                        (3.0, {"target", "source_a", "source_b"}), (2.0, {"target"})])
def test_standard_scope_and_supplementary_share_selected_sources(monkeypatch, source_job, number, keys):
    _, _, ids = source_job
    calls = _capture_dispatch(monkeypatch)
    result = _run_phase(_phase(number, iteration_mode="single", supplementary_chains=["supplement"]), ids)
    assert result.status == "completed", result.error
    assert len(calls) == 2
    for call in calls:
        assert set(call["documents"]) == keys
        assert "Other thinker" not in " ".join(call["documents"].values())
        assert "Primary generated output" not in " ".join(call["documents"].values())
    assert "Primary generated output" in calls[1]["upstream_context"]


def test_snapshot_and_aliases_do_not_inflate_corpus(source_job, monkeypatch):
    plan, _, ids = source_job
    plan["workflow_key"] = "intellectual_genealogy"
    monkeypatch.setattr(pr, "get_job", lambda _: {"plan_data": {"_type": "request_snapshot", "plan_request": plan}})
    normalized = normalize_document_ids(ids, {"plan_request": plan})
    assert pr._get_standard_phase_sources(normalized, "job", 1).documents == {"target": "Target source text."}
    assert pr._get_target_work_title("job") == "Target title"


@pytest.mark.parametrize("distilled,independent", [(True, False), (False, True), (False, False)])
def test_per_work_raw_sources_and_scope_context(monkeypatch, source_job, distilled, independent):
    plan, _, ids = source_job
    plan["workflow_key"] = "intellectual_genealogy"
    calls = _capture_dispatch(monkeypatch)
    summary = "Generated target analysis is not a source quotation."
    monkeypatch.setattr(pr, "assemble_phase_context", lambda **_: summary if distilled else "")
    result = _run_phase(_phase(2.0, iteration_mode="per_work", depends_on=[] if independent else [1.0]),
                        ids, prior_work_titles=["A-B"])
    assert result.status == "completed", result.error
    call, = calls
    expected = {"source_a": ALPHA}
    if not distilled and not independent:
        expected = {"target": "Target source text.", **expected}
    assert call["documents"] == expected
    assert summary not in " ".join(call["documents"].values())
    if distilled:
        assert summary in call["document_context"] and call["upstream_context"] == ""
    if not independent:
        assert "TARGET WORK: Target title" in call["document_context"]
        assert "PRIOR WORK: A-B" in call["document_context"]


def test_explicit_independent_scope_overrides_template_dependencies(monkeypatch, source_job):
    _, _, ids = source_job
    calls = _capture_dispatch(monkeypatch)
    assembled = []
    def upstream(**kwargs):
        assembled.append(kwargs)
        return "Generated target analysis inherited from the template"
    monkeypatch.setattr(pr, "assemble_phase_context", upstream)
    phase = _phase(2.0, iteration_mode="per_work", depends_on=[])
    template = WorkflowPhase(phase_number=2.0, phase_name="template", engine_key=ENGINE, depends_on_phases=[1.0])
    result = pr.run_phase(template, phase, job_id="job", document_ids=ids, prior_work_titles=["A-B"])
    assert result.status == "completed", result.error
    assert assembled == []
    # Even a direct caller supplying existing upstream text cannot override
    # explicit independent profiling with the distilled comparison path.
    result = pr._run_per_work_phase(template, phase, "job", ids, ["A-B"], upstream(), None, None, time.time())
    assert result.status == "completed", result.error
    assert len(calls) == 2
    for call in calls:
        assert call["documents"] == {"source_a": ALPHA}
        assert "Target title" not in call["document_text"]
        assert "Pair Scope Contract" not in call["document_context"]
        assert "Generated target analysis" not in call["document_context"]


@pytest.mark.parametrize("uploaded", [True, False])
def test_chapter_source_excludes_summary_and_rest_of_book(monkeypatch, source_job, uploaded):
    _, texts, ids = source_job
    texts["doc-target"] = "BEFORE|selected chapter|AFTER"
    if uploaded:
        ids["chapter:target:ch1"] = "doc-chapter"
        texts["doc-chapter"] = "selected chapter"
    calls = _capture_dispatch(monkeypatch)
    monkeypatch.setattr(pr, "assemble_phase_context", lambda **_: "Generated book summary")
    phase = _phase(2.0, document_scope="chapter", depends_on=[1.0], chapter_targets=[
        {"chapter_id": "ch1", "start_char": 7, "end_char": 23},
    ])
    result = _run_phase(phase, ids)
    assert result.status == "completed", result.error
    call, = calls
    assert list(call["documents"].values()) == ["selected chapter"]
    assert "Generated book summary" in call["document_context"]
    assert "BEFORE" not in str(call["documents"]) and "AFTER" not in str(call["documents"])


def test_stored_alias_dedup_does_not_merge_colliding_titles(source_job):
    plan, _, ids = source_job
    ids["alias"] = "doc-a"
    sources = pr._get_process_sources(ids, plan, works=["A-B", "A B", "alias"])
    assert sources.documents == {"source_a": ALPHA, "source_b": BETA}
    plan["prior_works"] = []
    ids.update({"A/B": "doc-a", "A:B": "doc-b"})
    assert pr._sanitize_work_key("A/B") == pr._sanitize_work_key("A:B")
    assert set(pr._get_process_sources(ids, plan, works=["A/B", "A:B"]).documents) == {"doc-a", "doc-b"}


@pytest.fixture
def persistence(monkeypatch):
    saved = []
    monkeypatch.setattr(cr, "save_output", lambda **kw: saved.append(kw) or "out")
    monkeypatch.setattr(cr, "update_job_tokens", lambda *a, **kw: None)
    monkeypatch.setattr(cr, "get_completed_passes", lambda _: set())
    monkeypatch.setattr(cr, "build_aoi_output_metadata", lambda **kw: {})
    monkeypatch.setattr("src.analysis_products.store.record_aoi_artifact_from_metadata", lambda **kw: None)
    return saved


def _fake_process_model(log):
    def call(system, user, *, label, model_hint, **kwargs):
        log.append((system, user, label, kwargs))
        if "| extract |" in label:
            prefix = re.search(r"^- \[([^\]]+)\.F1\]", system, re.M).group(1)
            if "cross-document findings" in system:
                content = (f'- [{prefix}.F1] Paired finding — anchor: "{ALPHA}" — doc: source_a '
                           f'— anchor-b: "{BETA}" — doc-b: source_b — confidence: high')
            else:
                key = re.search(r"SOURCE \[([^\]]+)\]", user).group(1)
                text = ALPHA if key == "source_a" else BETA
                content = f'- [{prefix}.F1] Local finding — anchor: "{text}" — doc: {key} — confidence: high'
        elif "| verify" in label or "| check" in label:
            rows = parse_rows("\n".join(line for line in user.splitlines() if line.startswith("- [")))
            for row in rows:
                row.status = "confirmed"
            content = render_rows(rows, heading="")
        elif "| oneshot" in label:
            content = (f'- [F1] Paired reading — dim: path_dependence — anchor: "{ALPHA}" — doc: source_a '
                       f'— anchor-b: "{BETA}" — doc-b: source_b — confidence: high')
        else:
            content = (f'- [F1] Synthesized pair — anchor: "{ALPHA}" — doc: source_a '
                       f'— anchor-b: "{BETA}" — doc-b: source_b — from: P6.F1 — confidence: high')
        return {"content": LEDGER_HEADING + "\n" + content, "model_used": model_hint,
                "input_tokens": 10, "output_tokens": 10, "thinking_tokens": 0, "duration_ms": 1, "retries": 0}
    return call


@pytest.mark.parametrize("depth", ["surface", "standard", "deep"])
@pytest.mark.parametrize("through_chain", [False, True])
def test_real_process_modes_receive_keyed_sources_and_persist_walls(monkeypatch, source_job, persistence, depth, through_chain):
    _, _, ids = source_job
    log = []
    monkeypatch.setattr("src.executor.process_runner._default_call", _fake_process_model(log))
    # A low legacy chunk threshold must not turn process sources into pseudo-documents.
    monkeypatch.setattr("src.executor.engine_runner.CHUNK_THRESHOLD", 1)
    if through_chain:
        chain = SimpleNamespace(engine_keys=[ENGINE])
        monkeypatch.setattr(cr, "get_chain_registry", lambda: SimpleNamespace(get=lambda _: chain))
        phase = _phase(1, depth=depth, chain_key="test-chain")
        phase.engine_key = None
    else:
        phase = _phase(1, depth=depth)
    result = _run_phase(phase, ids)
    assert result.status == "completed", result.error
    final = persistence[-1]
    assert final["metadata"]["wall"]["verified"] == 1
    assert final["metadata"]["wall"]["verified_anchors"] == 2
    assert all("doc-other" not in user and "Target source text" not in user for _, user, _, _ in log)
    if depth == "deep":
        extracted = [row for row in persistence if row["metadata"].get("kind") == "extract"]
        assert {row["metadata"]["doc"] for row in extracted} == {"source_a", "source_b", ""}
        assert any(row["metadata"]["dimension"] == "path_dependence" for row in extracted)
        assert "[P6.F1]" in log[-1][1]
    else:
        assert "SOURCE [source_a]" in log[0][1] and "SOURCE [source_b]" in log[0][1]


def test_chain_engine_fallback_and_legacy_single_source(monkeypatch, persistence):
    monkeypatch.setattr(cr, "get_chain_registry", lambda: SimpleNamespace(get=lambda _: None))
    seen = []
    def process(cap, spec, documents, **kwargs):
        seen.append((documents, kwargs["upstream_context"]))
        return SimpleNamespace(calls=[], cost_usd=0, seconds=0, final_wall={})
    monkeypatch.setattr("src.executor.process_runner.run_process", process)
    cr.run_chain(ENGINE, "legacy raw source", job_id="job", phase_number=1, depth="deep", work_key="ordinary")
    cr.run_chain(ENGINE, "legacy combined prompt", job_id="job", phase_number=1, depth="deep",
                 documents={"a": ALPHA, "b": BETA}, document_context="Source scope")
    assert seen == [({"ordinary": "legacy raw source"}, ""), ({"a": ALPHA, "b": BETA}, "Source scope")]


@pytest.mark.parametrize("documents", [{}, {"a": ALPHA, "b": ""}, {"a": "  "}])
def test_explicit_missing_sources_fail_before_models(documents, persistence):
    with pytest.raises(ValueError, match="non-empty selected source"):
        cr.run_single_engine(ENGINE, "legacy fallback", documents=documents, job_id="job", phase_number=1, depth="deep")


def test_legacy_engine_keeps_existing_text_chunking(monkeypatch, persistence):
    monkeypatch.setattr(cr, "get_operationalization_registry", lambda: SimpleNamespace(get=lambda _: None))
    monkeypatch.setattr(cr, "compose_all_pass_prompts", lambda **_: [])
    monkeypatch.setattr("src.stages.capability_composer.compose_capability_prompt", lambda **_: SimpleNamespace(prompt="legacy"))
    monkeypatch.setattr("src.executor.engine_runner.CHUNK_THRESHOLD", 1)
    seen = []
    def chunk(**kwargs):
        seen.append(kwargs["user_message"])
        return {"content": "legacy result", "model_used": "fake", "input_tokens": 1, "output_tokens": 1,
                "thinking_tokens": 0, "duration_ms": 0, "retries": 0}
    monkeypatch.setattr("src.executor.engine_runner._run_chunked", chunk)
    cr.run_single_engine(ENGINE, "unaltered legacy combined text", documents={"a": ALPHA, "b": BETA},
                         document_context="only process context", job_id="job", phase_number=1)
    assert seen == ["unaltered legacy combined text"]


def test_dossier_bindings_survive_snapshot_resume_and_match_desk_keys(monkeypatch, source_job):
    from src.dossier.analysis import _resume_sub_job, _store_source_bindings
    plan, texts, ids = source_job
    plan["workflow_key"] = "intellectual_genealogy"
    docs = [Document(key="DOC1", title="A-B", text=ALPHA), Document(key="DOC2", title="A B", text=BETA)]
    job = SimpleNamespace(documents=[{"key": "DOC1", "executor_doc_id": "doc-a"}, {"key": "DOC2", "executor_doc_id": "doc-b"}])
    bindings = _store_source_bindings(job, docs)
    ids = {"target": "doc-target", "Target title": "doc-target", **bindings}
    captured = []
    monkeypatch.setattr("src.executor.workflow_runner.start_resume_thread", lambda *a: captured.append(a))
    _resume_sub_job({"job_id": "sub", "plan_data": json.dumps(plan), "document_ids": json.dumps(ids)})
    resumed_ids = normalize_document_ids(captured[0][2], captured[0][1])
    assert pr._get_standard_phase_sources(resumed_ids, "sub", 1).documents == {"DOC1": ALPHA, "DOC2": BETA}
    assert pr._get_standard_phase_sources({"target": "doc-target"}, "legacy", 1).documents == {"target": texts["doc-target"]}


def test_dossier_start_persists_exact_source_bindings(monkeypatch):
    from src.dossier.analysis import _start_sub_job
    plan = SimpleNamespace(workflow_key="intellectual_genealogy", model_dump=lambda: {"workflow_key": "intellectual_genealogy"})
    monkeypatch.setattr("src.orchestrator.planner.load_plan", lambda _: plan)
    saved, started = [], []
    monkeypatch.setattr("src.executor.job_manager.create_job", lambda *a, **kw: saved.append(kw))
    monkeypatch.setattr("src.executor.workflow_runner.start_execution_thread", lambda **kw: started.append(kw))
    ids = {"target": "flattened", "corpus:DOC1": "doc-a", "corpus:DOC2": "doc-b"}
    _start_sub_job(SimpleNamespace(), "plan", ids)
    assert saved[0]["document_ids"] == ids == started[0]["document_ids"]


@pytest.mark.parametrize("missing", [None, ""])
def test_missing_explicit_dossier_binding_refuses_smaller_corpus(monkeypatch, source_job, persistence, missing):
    plan, texts, ids = source_job
    plan["workflow_key"] = "intellectual_genealogy"
    ids.update({"corpus:DOC1": "doc-a", "corpus:DOC2": "doc-missing"})
    if missing is not None:
        texts["doc-missing"] = missing
    result = _run_phase(_phase(1, depth="deep"), ids)
    assert result.status == "failed"
    assert "non-empty selected source" in result.error
    assert "DOC2" in result.error
    assert persistence == []


@pytest.mark.parametrize("missing_timestamp", [False, True])
def test_collection_keeps_final_engine_wall_and_corpus_lineage_aligned(monkeypatch, missing_timestamp):
    from src.dossier.analysis import _collect
    from src.dossier.common import analysis_ledger
    broken_pair = LEDGER_HEADING + f'\n- [F14] Descendant — anchor: "{ALPHA}" — doc: DOC1 — from: X6.F1'
    rows = [
        {"phase_number": 1, "pass_number": 1, "engine_key": SECOND, "content": broken_pair, "metadata": {"wall": {"verified": 0}},
         "created_at": datetime(2026, 9, 5, 2, tzinfo=timezone.utc)},
        {"phase_number": 1, "pass_number": 20, "engine_key": ENGINE, "content": "Earlier long engine", "metadata": {"wall": {"verified": 9}},
         "created_at": None if missing_timestamp else "2026-09-05T01:00:00"},
    ]
    monkeypatch.setattr("src.executor.output_store.load_all_job_outputs", lambda *a, **kw: rows)
    monkeypatch.setattr("src.dossier.analysis.record", lambda *a: None)
    monkeypatch.setattr("src.dossier.analysis.make_receipt", lambda **kw: {})
    job = SimpleNamespace(id="dossier")
    job.analysis = _collect(job, "sub", [{"phase_number": 1, "engine_key": ENGINE}])
    final = job.analysis["1.0"]
    if missing_timestamp:
        assert final["engine_key"] == ENGINE and final["final_wall"] == {"verified": 9}
    else:
        assert final["engine_key"] == SECOND and final["final_wall"] == {"verified": 0}
        desk = analysis_ledger(job, [Document(key="DOC1", title="a", text=ALPHA), Document(key="DOC2", title="b", text=BETA)])
        assert "[F14]" not in desk.split("Rows whose anchors are unverified")[0]
        assert "[F14]" in desk.split("Rows whose anchors are unverified")[1]
