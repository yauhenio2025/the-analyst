"""Doctrine files served by the registry, used to compose the story desk's prompts."""
from __future__ import annotations

import hashlib
from pathlib import Path

DOCTRINES = Path(__file__).resolve().parents[1] / "engines" / "doctrines"


def doctrine(engine_key: str, name: str, max_chars: int = 40_000) -> tuple[str, str]:
    """(text, sha256) of a doctrine file of an engine; empty when absent."""
    p = DOCTRINES / engine_key / name
    if not p.is_file():
        return "", ""
    data = p.read_bytes()
    text = data.decode("utf-8", "replace")
    return text[:max_chars], hashlib.sha256(data).hexdigest()
