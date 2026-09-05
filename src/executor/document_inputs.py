"""Raw source identity for process dispatch, separate from legacy prompt text."""

from dataclasses import dataclass, field

from src.executor.document_store import get_document_text


@dataclass
class ProcessDocumentInput:
    documents: dict[str, str] = field(default_factory=dict)
    labels: list[str] = field(default_factory=list)
    _stored_ids: set[str] = field(default_factory=set)

    def add(self, key: str, stored_id: str | None, label: str) -> None:
        """Deduplicate storage aliases, never distinct documents with similar titles."""
        if stored_id and stored_id in self._stored_ids:
            return
        if not key or key in self.documents:
            raise ValueError(f"Conflicting process source key: {key!r}")
        # Empty/missing selected texts fail at process dispatch. Legacy engines
        # still use their existing placeholder text and behavior.
        self.documents[key] = (get_document_text(stored_id) or "") if stored_id else ""
        self.labels.append(f"- [{key}] {label}")
        if stored_id:
            self._stored_ids.add(stored_id)

    @property
    def context(self) -> str:
        return "## Selected source identities\n\n" + "\n".join(self.labels)
