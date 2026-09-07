"""A workflow step's scope (Evgeny, 2026-09-07: the retrospective reading of a paper must not see what followed it): a
recipe step names the key prefixes it reads; the scope travels from the path to the plan phase to the executor phase,
where the phase runner keeps only the corpus documents whose keys carry a prefix."""
import pytest

from src.dossier.schemas import PathRequest, PathStepRequest


def test_a_step_scope_travels_from_the_request_to_the_executor_phase(monkeypatch):
    from src.dossier import catalog as C
    monkeypatch.setattr(C, "load_recipes", lambda: [{"key": "two_scoped", "steps": [
        {"engine_key": "argument_architecture", "depth": "surface", "scope": ["focal:", "before:"]},
        {"engine_key": "counterfactual_analyzer", "depth": "surface"}]}])
    path = C.resolve_path_request(PathRequest(chain_key="two_scoped", steps=[PathStepRequest(engine_key="dialectical_structure", scope=["after:"])]), "researcher")
    assert [s.scope for s in path.steps] == [["focal:", "before:"], [], ["after:"]]
    from src.dossier.plan import fixed_phases
    by_key = {k: {"engine_name": k} for k in ("argument_architecture", "counterfactual_analyzer", "dialectical_structure")}
    monkeypatch.setattr("src.dossier.plan.passes_for", lambda e, d: 1)
    phases = fixed_phases(path, [], by_key)
    assert [p.scope for p in phases] == [["focal:", "before:"], [], ["after:"]]


def test_the_phase_runner_keeps_only_the_scoped_corpus_documents(monkeypatch):
    from src.executor import phase_runner as PR
    from src.executor.document_ids import CORPUS_DOCUMENT_PREFIX
    texts = {"d-focal": "the focal text", "d-b1": "an earlier profile", "d-a1": "a later profile", "d-target": "corpus"}
    monkeypatch.setattr(PR, "get_document_text", lambda doc_id: texts.get(doc_id, ""))
    ids = {"target": "d-target", CORPUS_DOCUMENT_PREFIX + "focal:em:1": "d-focal", CORPUS_DOCUMENT_PREFIX + "before:em:2": "d-b1", CORPUS_DOCUMENT_PREFIX + "after:em:3": "d-a1"}
    everything = PR._get_process_sources(ids, {}, include_target=True)
    assert set(everything.documents) == {"focal:em:1", "before:em:2", "after:em:3"}
    scoped = PR._get_process_sources(ids, {}, include_target=True, key_prefixes=["focal:", "before:"])
    assert set(scoped.documents) == {"focal:em:1", "before:em:2"} and any("scope: focal:, before:" in l for l in scoped.labels)
    with pytest.raises(ValueError):
        PR._get_process_sources(ids, {}, include_target=True, key_prefixes=["nothing:"])
    monkeypatch.setattr(PR, "_get_plan_data", lambda job_id: {})
    assert set(PR._get_standard_phase_sources(ids, "job", 4.1, source_scope=["after:"]).documents) == {"after:em:3"}


def test_the_executor_phase_carries_the_scope():
    from src.orchestrator.schemas import PhaseExecutionSpec
    ph = PhaseExecutionSpec(phase_number=4.1, phase_name="x", depth="surface", engine_key="argument_architecture", source_scope=["focal:"])
    assert ph.source_scope == ["focal:"] and PhaseExecutionSpec(phase_number=4.2, phase_name="y", depth="surface").source_scope is None
