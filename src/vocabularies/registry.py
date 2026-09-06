"""The vocabulary registry: the enumerated values an engine's rows answer in (moves, stances, verdicts, kinds…), one JSON
per vocabulary with glosses and the engine fields that use it. The engines' answer shapes carry the same lists in their
prompts; a test keeps the two identical, and consumers (the Stacks' tables, the desks) read the lists from here rather
than keeping copies (the owner, 2026-09-06: 'we don't leave those bits and pieces inside the actual software; we
slowly aggregate this stuff inside the Mastermind')."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

DEFINITIONS = Path(__file__).parent / "definitions"


class VocabularyValue(BaseModel):
    value: str
    gloss: str = ""


class VocabularyUse(BaseModel):
    engine_key: str                  # an engine key, or the desk / schema / external record that carries the field
    dimension: str = "*"
    field: str
    kind: str = "engine"             # engine | desk | schema | external — only engine uses are pinned to an answer shape


class Vocabulary(BaseModel):
    key: str
    name: str
    family: str = ""
    owner: str = "the-mastermind"
    version: str = ""
    values: list[VocabularyValue] = Field(default_factory=list)
    used_by: list[VocabularyUse] = Field(default_factory=list)
    note: str = ""

    def value_list(self) -> list[str]:
        return [v.value for v in self.values]


class VocabularyRegistry:
    def __init__(self, path: Path = DEFINITIONS):
        self._items: dict[str, Vocabulary] = {}
        for f in sorted(path.glob("*.json")):
            v = Vocabulary.model_validate(json.loads(f.read_text()))
            self._items[v.key] = v

    def list(self) -> list[Vocabulary]:
        return list(self._items.values())

    def get(self, key: str) -> Optional[Vocabulary]:
        return self._items.get(key)

    def for_engine(self, engine_key: str) -> list[Vocabulary]:
        return [v for v in self._items.values() if any(u.engine_key == engine_key for u in v.used_by)]

    def values_for(self, engine_key: str, field: str) -> Optional[list[str]]:
        for v in self._items.values():
            if any(u.engine_key == engine_key and u.field == field for u in v.used_by):
                return v.value_list()
        return None


_registry: Optional[VocabularyRegistry] = None


def get_vocabulary_registry() -> VocabularyRegistry:
    global _registry
    if _registry is None:
        _registry = VocabularyRegistry()
    return _registry


def values(key: str, fallback: Optional[list[str]] = None) -> list[str]:
    """The value list of a vocabulary, for code that must not keep its own copy (the desks' tuples)."""
    v = get_vocabulary_registry().get(key)
    if v is None:
        if fallback is None:
            raise KeyError(f"no vocabulary {key}")
        return list(fallback)
    return v.value_list()
