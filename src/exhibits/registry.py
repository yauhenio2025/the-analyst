"""The exhibits registry: the presentation elements a page can show, held in the Mastermind beside the engines, the
vocabularies, the practices and the actions (Evgeny, 2026-09-07 09:31: a memo must not be a wall of text; the elements
that help a reader grasp it — timelines, idea maps, split panels, chips, sidebars, tables, images — should be visible
categories in the Mastermind, "inspirational seeds an LLM can extrapolate for a particular use case").

An exhibit is a record: key · name · when (the finding kinds or memo parts it serves) · inputs (the rows or fields it draws
on) · medium (html · svg · image · table · box · prose) · renderer (a Mastermind renderer / sub-renderer key, or a figure
primitive) · shape (what it shows and how) · didactic (what the reader should grasp at a glance) · cost · owner · example ·
evidence (which pages used it, and what the reviewer said). A page planner chooses among them; a reviewer's verdicts write
back. Nothing here renders anything. Design: communications/DESIGN_presentation_exhibits_2026-09-07.md.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

DEFINITIONS = Path(__file__).parent / "definitions"
KEY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MEDIA = ("html", "svg", "image", "table", "box", "prose")
BLOB_PREFIX = "exhibit:"


class ExhibitUse(BaseModel):
    page: str                              # the page or job that used it
    organ: str = ""
    verdict: str = ""                      # the reviewer's verdict: keep | simplify | replace | drop | move (page_review_verdicts)
    note: str = ""
    recorded: str = ""


class Exhibit(BaseModel):
    key: str
    name: str
    when: list[str] = Field(default_factory=list)      # "<engine>.<dimension>", "<engine>.*", a memo part ("memo.verdicts"), or "*"
    inputs: list[str] = Field(default_factory=list)    # rows or fields it draws on
    medium: str = "html"
    renderer: str = ""                                 # a renderer / sub-renderer key, or a figure primitive
    shape: str = ""                                    # what it shows and how, one paragraph
    didactic: str = ""                                 # what the reader should grasp at a glance
    placement: str = "after"                           # where it sits by default (exhibit_placements): before (chips only) | beside | after | folded
    cost: str = "none"                                 # none | cents (an image, a model call)
    owner: str = "the-mastermind"
    version: str = ""
    example: str = ""                                  # the first page that carried it
    evidence: list[ExhibitUse] = Field(default_factory=list)
    note: str = ""

    def serves(self, kind: str) -> bool:
        eng = kind.split(".", 1)[0]
        return any(w == kind or w == f"{eng}.*" or w == "*" for w in self.when)


def _durable_put(e: Exhibit) -> bool:
    try:
        from src.dossier.blob_store import put_blob_safe
        return put_blob_safe(BLOB_PREFIX + e.key, "application/json", json.dumps(e.model_dump(), ensure_ascii=False).encode("utf-8"))
    except Exception:
        return False


def _durable_all() -> dict[str, Exhibit]:
    try:
        from src.dossier.blob_store import get_blob, list_keys
        out = {}
        for row in list_keys(BLOB_PREFIX):
            key = (row.get("blob_key") or row.get("key") or "") if isinstance(row, dict) else (row[0] if row else "")
            got = get_blob(key)
            if got:
                e = Exhibit.model_validate(json.loads(got[1].decode("utf-8")))
                out[e.key] = e
        return out
    except Exception:
        return {}


class ExhibitRegistry:
    def __init__(self, path: Path = DEFINITIONS, durable: bool = True):
        self.path = path
        self.durable = durable
        self.last_durable = False
        self._items: dict[str, Exhibit] = {}
        for f in sorted(path.glob("*.json")):
            e = Exhibit.model_validate(json.loads(f.read_text()))
            self._items[e.key] = e
        if durable:
            for key, e in _durable_all().items():
                old = self._items.get(key)
                if old is None:
                    self._items[key] = e
                    continue
                # the file is the record (edited here, persisted through GitHub); the blob only adds the uses it has seen since
                # (2026-09-07: a blob with more evidence had replaced the file whole, losing a redrawn shape and the placement field)
                seen = {(u.page, u.recorded, u.verdict) for u in old.evidence}
                old.evidence.extend(u for u in e.evidence if (u.page, u.recorded, u.verdict) not in seen)

    def list(self) -> list[Exhibit]:
        return list(self._items.values())

    def get(self, key: str) -> Optional[Exhibit]:
        return self._items.get(key)

    def for_kind(self, kind: str) -> list[Exhibit]:
        return [e for e in self._items.values() if e.serves(kind)]

    def for_medium(self, medium: str) -> list[Exhibit]:
        return [e for e in self._items.values() if e.medium == medium]

    def kinds(self) -> list[str]:
        return sorted({w for e in self._items.values() for w in e.when})

    def upsert(self, e: Exhibit) -> Exhibit:
        if not KEY.match(e.key):
            raise ValueError(f"exhibit key must be lower-case words and hyphens, not {e.key!r}")
        if not e.name.strip() or not e.when or not e.shape.strip() or not e.didactic.strip():
            raise ValueError("an exhibit needs name, when, shape and didactic")
        if e.medium not in MEDIA:
            raise ValueError(f"medium must be one of {MEDIA}")
        old = self._items.get(e.key)
        if old is not None and old.owner != e.owner:
            raise PermissionError(f"exhibit {e.key} is {old.owner}'s; {e.owner} may not overwrite it")
        if old is not None and not e.evidence:
            e.evidence = old.evidence
        if not e.version:
            e.version = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._items[e.key] = e
        self.file_for(e.key).write_text(json.dumps(e.model_dump(), ensure_ascii=False, indent=2) + "\n")
        self.last_durable = _durable_put(e) if self.durable else False
        return e

    def add_use(self, key: str, use: ExhibitUse) -> Exhibit:
        e = self._items.get(key)
        if e is None:
            raise KeyError(f"no exhibit {key}")
        if not use.recorded:
            use.recorded = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        e.evidence.append(use)
        self.file_for(key).write_text(json.dumps(e.model_dump(), ensure_ascii=False, indent=2) + "\n")
        self.last_durable = _durable_put(e) if self.durable else False
        return e

    def file_for(self, key: str) -> Path:
        return self.path / f"{key}.json"


def planner_block(exhibits: list[Exhibit]) -> list[dict]:
    """What a page planner's packet carries: records, not prose."""
    return [{"exhibit": e.key, "name": e.name, "when": e.when, "inputs": e.inputs, "medium": e.medium, "renderer": e.renderer, "shape": e.shape,
             "didactic": e.didactic, "placement": e.placement, "cost": e.cost, "uses": len(e.evidence)} for e in exhibits]


_registry: Optional[ExhibitRegistry] = None


def get_exhibit_registry() -> ExhibitRegistry:
    global _registry
    if _registry is None:
        _registry = ExhibitRegistry()
    return _registry
