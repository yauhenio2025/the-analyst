"""Sources carry a role: `source` for the desks and the engines, `evidence_index` / `plan` for context supplied with the
job (the Stacks bridge, 2026-09-06): not profiled, not in the corpus, appended to every phase's upstream context."""
from src.sources.schemas import SourceSpec
from src.sources.resolve import resolve_sources


def test_resolve_sources_keeps_the_role_and_defaults_to_source():
    docs = resolve_sources([SourceSpec(kind="paste", title="Paper", text="A paper about estates in Weber."),
                            SourceSpec(kind="paste", role="evidence_index", title="Riley on Weber: evidence", text='{"checks": []}'),
                            SourceSpec(kind="paste", role="plan", title="Plan", text="Questions: ...")])
    assert [d.role for d in docs] == ["source", "evidence_index", "plan"]
    assert all("role" in d.meta() for d in docs)


def test_desks_see_only_sources_and_bindings_split_by_role(monkeypatch):
    from src.dossier import analysis
    from src.dossier.runner import source_docs
    from src.sources.schemas import Document
    docs = [Document(key="paper", title="Paper", text="text", role="source"), Document(key="evidence", title="Evidence", text="{}", role="evidence_index")]
    assert [d.key for d in source_docs(docs)] == ["paper"]
    stored = iter(["doc-1", "doc-2"])
    monkeypatch.setattr("src.executor.document_store.store_document", lambda **kw: next(stored))
    class Job:
        id = "dossier-t"; documents = []
        class options: intent = "x"
    bindings = analysis._store_source_bindings(Job(), docs)
    assert bindings == {"corpus:paper": "doc-1", "context:evidence": "doc-2"}


def test_context_documents_join_the_upstream_context(monkeypatch):
    from src.executor import phase_runner
    monkeypatch.setattr(phase_runner, "get_document_text", lambda doc_id: {"doc-2": "{\"checks\": [1]}"}.get(doc_id, ""))
    out = phase_runner._with_context_documents("PRIOR PHASE PROSE", {"corpus:paper": "doc-1", "context:evidence": "doc-2"})
    assert out.startswith("PRIOR PHASE PROSE") and "CONTEXT SUPPLIED WITH THE JOB [evidence]:" in out and '{"checks": [1]}' in out
    assert phase_runner._with_context_documents("", {"corpus:paper": "doc-1"}) == ""
