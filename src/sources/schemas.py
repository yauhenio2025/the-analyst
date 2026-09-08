"""Source specs and resolved documents (see communications/IMPLEMENTATION_TRACKER.md §2)."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

SourceKind = Literal["paste", "upload", "stacks_export", "stacks_view", "stacks_uids", "exemplar"]
# source: a text the desks read and the engines analyse. evidence_index / plan: supplied with the job as context
# (the Stacks bridge, 2026-09-06): not profiled, not counted in the corpus, handed to every engine as upstream context.
SourceRole = Literal["source", "evidence_index", "plan", "profile", "statements", "cohort", "oeuvre", "author_investigation", "field_investigation"]


class SourceSpec(BaseModel):
    """One input to a dossier run.

    kind=paste|upload|stacks_export carry `text` (a stacks export is auto-split
    on its `===== [n/N] … =====` headers). kind=stacks_view|stacks_uids call the
    local stacks service. kind=exemplar names a bundled file under
    data/exemplars/ so a front end can start a run with one click.
    """

    kind: SourceKind = "paste"
    role: SourceRole = "source"
    title: Optional[str] = None
    text: Optional[str] = None
    key: Optional[str] = None
    view_id: Optional[str] = None
    uids: Optional[list[str]] = None
    name: Optional[str] = Field(default=None, description="exemplar file name")


class Document(BaseModel):
    key: str
    title: str
    creators: str = ""
    year: str = ""
    publication: str = ""
    library: str = ""
    stacks_key: str = ""
    text: str = ""
    char_count: int = 0
    role: str = "source"

    def label(self) -> str:
        bits = [b for b in (self.creators, f"({self.year})" if self.year else "") if b]
        head = " ".join(bits)
        return f"{head} — {self.title}" if head else self.title

    def meta(self) -> dict:
        return self.model_dump(exclude={"text"})
