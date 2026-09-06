"""The practices registry: how to SEARCH, held in the Mastermind beside the engines (Evgeny, 2026-09-07 00:10, on the
Riley harvest missing a page his own query found with "dylan * riley" "new left review": 'such tricks have to start
living in the Mastermind, in parallel with the engines — best practices or something like that — and the Reporter will
be able to go and pick the right ones to tackle the task at hand, but so will the other agents').

Engines read; practices search. A practice is a small record, not prose: name, the task kinds it serves, when it
applies, the shape of the query, the ingredients a library supplies, what it yields, what it misses, and the evidence
runs have written back (a planner declares the practice each query deploys; a retrospective seat posts the yield). The
Reporter's planner, gs_revamp's, the Referee's fetch pool and the Stacks' resolvers read the same records for their
task kinds. Design: ~/projects/zotero-stacks/communications/2026-09-07_search_craft_as_practices.md §3.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

import re

DEFINITIONS = Path(__file__).parent / "definitions"
KEY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class PracticeEvidence(BaseModel):
    run: str                                  # the run id in the organ that scored it (a Reporter harvest, a Stacks resolve)
    organ: str = ""                           # the-reporter | the-stacks | the-referee | gs-revamp | the-mastermind
    queries: int = 0                          # queries that deployed the practice in that run
    new_relevant: int = 0                     # relevant pages those queries found that no other query had
    note: str = ""
    recorded: str = ""


class Practice(BaseModel):
    key: str
    name: str
    task_kinds: list[str] = Field(default_factory=list)   # person-harvest | paper-discovery | pdf-fetch | work-identity | institution-harvest …
    when: str = ""                                          # the situation the practice answers
    shape: str = ""                                         # the query's shape, as a template
    ingredients: list[str] = Field(default_factory=list)   # what the library must supply (name forms, anchors, venues, held titles)
    yields: str = ""                                        # what it finds that a plain search does not
    misses: str = ""                                        # what it is known to miss
    origin: str = ""                                        # where the craft was first measured (a planner's prose, a run)
    owner: str = "the-mastermind"
    version: str = ""
    evidence: list[PracticeEvidence] = Field(default_factory=list)
    note: str = ""

    def yield_totals(self) -> dict:
        return {"runs": len(self.evidence), "queries": sum(e.queries for e in self.evidence), "new_relevant": sum(e.new_relevant for e in self.evidence)}


class PracticeRegistry:
    def __init__(self, path: Path = DEFINITIONS):
        self.path = path
        self._items: dict[str, Practice] = {}
        for f in sorted(path.glob("*.json")):
            p = Practice.model_validate(json.loads(f.read_text()))
            self._items[p.key] = p

    def list(self) -> list[Practice]:
        return list(self._items.values())

    def get(self, key: str) -> Optional[Practice]:
        return self._items.get(key)

    def for_task(self, task_kind: str) -> list[Practice]:
        return [p for p in self._items.values() if task_kind in p.task_kinds or "*" in p.task_kinds]

    def task_kinds(self) -> list[str]:
        return sorted({t for p in self._items.values() for t in p.task_kinds if t != "*"})

    def add_evidence(self, key: str, ev: PracticeEvidence) -> Practice:
        """Append a run's yield to a practice and write its file (the caller persists the file through GitHub on Render)."""
        p = self._items.get(key)
        if p is None:
            raise KeyError(f"no practice {key}")
        if not ev.recorded:
            ev.recorded = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        p.evidence.append(ev)
        self.file_for(key).write_text(json.dumps(p.model_dump(), ensure_ascii=False, indent=2) + "\n")
        return p

    def upsert(self, practice: Practice) -> Practice:
        """Create a practice or update one; the record's evidence is kept when the poster sends none (an organ registers
        what its planner already knows; the runs' yields stay). An organ may not overwrite another organ's record."""
        if not KEY.match(practice.key):
            raise ValueError(f"practice key must be a slug of lower-case words and hyphens, not {practice.key!r}")
        if not practice.task_kinds or not practice.when.strip() or not practice.shape.strip() or not practice.yields.strip():
            raise ValueError("a practice needs task_kinds, when, shape and yields")
        old = self._items.get(practice.key)
        if old is not None and old.owner != practice.owner:
            raise PermissionError(f"practice {practice.key} is {old.owner}'s; {practice.owner} may not overwrite it")
        if old is not None and not practice.evidence:
            practice.evidence = old.evidence
        if not practice.version:
            practice.version = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._items[practice.key] = practice
        self.file_for(practice.key).write_text(json.dumps(practice.model_dump(), ensure_ascii=False, indent=2) + "\n")
        return practice

    def file_for(self, key: str) -> Path:
        return self.path / f"{key}.json"


def packet_block(practices: list[Practice]) -> list[dict]:
    """The PRACTICES block a planner's packet carries: records, not prose (the family's measured lesson is that feeds and
    schema fields change an agent's behaviour where prompt prose barely does)."""
    return [{"practice": p.key, "name": p.name, "task_kinds": p.task_kinds, "owner": p.owner, "when": p.when, "shape": p.shape,
             "ingredients": p.ingredients, "yields": p.yields, "misses": p.misses, "evidence": p.yield_totals()} for p in practices]


_registry: Optional[PracticeRegistry] = None


def get_practice_registry() -> PracticeRegistry:
    global _registry
    if _registry is None:
        _registry = PracticeRegistry()
    return _registry
