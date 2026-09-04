"""What the downstream passes need from the sources.

The registry is the source of truth (EngineDefinition.source_demands on the Wirecut
engines); this module holds the defaults the generator writes there and composes the
demand block of the reading prompt from whatever the registry currently says.
"""
from __future__ import annotations

DEMANDS: dict[str, list[str]] = {
    "wirecut_telling_desk": [
        "the question the source raises or answers (kind: question)",
        "faces: named people or groups with a stake, what they chose, and whether they are public figures (kind: face)",
        "facts a verdict could rest on (kind: reveal or number)",
    ],
    "wirecut_spine": [
        "turns: a value before and after, and what turned it (kind: turn)",
        "recurring objects, images or phrases that could be planted early and paid off late (kind: motif)",
        "the strongest opening fact in the source (any kind, intensity 5)",
        "the question the source leaves unresolved (kind: question)",
    ],
    "wirecut_screenwriter": [
        "facts in the order a viewer must learn them; intensity marks how early the viewer needs to know",
        "lines quotable as narration, verbatim (kind: quotable)",
        "numbers with their unit and what they measure (kind: number)",
    ],
    "wirecut_storyboard": [
        "filmable places, objects, people and scenes, each with its visual form (kind: filmable)",
        "named public figures who would appear on screen (kind: face, detail.public = yes)",
    ],
    "wirecut_text_layer": [
        "verbatim phrases and numbers short enough to stand as on-screen titles (kind: quotable / number)",
    ],
    "wirecut_grounding_review": [
        "a verbatim quote from the source on every element; nothing without an anchor",
    ],
    "wirecut_pacing_editor": [
        "the intensity of each element, 1 to 5, so the film's clock can be cut from the material",
    ],
    "wirecut_music_brief": [
        "where the material itself rises and settles: contradictions, reveals and reversals as the loud parts",
    ],
}


def registry_demands() -> list[tuple[str, str, list[str]]]:
    """(engine_key, engine_name, demands) from the registry, falling back to the defaults above."""
    out: list[tuple[str, str, list[str]]] = []
    try:
        from src.engines.registry import get_engine_registry

        reg = get_engine_registry()
        reg.load()
        for key, fallback in DEMANDS.items():
            e = reg.get(key)
            demands = list(getattr(e, "source_demands", None) or []) if e else []
            out.append((key, e.engine_name if e else key, demands or fallback))
    except Exception:  # noqa: BLE001 — the registry never blocks a read
        out = [(k, k, v) for k, v in DEMANDS.items()]
    return out


def demand_block() -> str:
    lines = ["The passes downstream have declared what they need from every source. Read for exactly these:"]
    for key, name, demands in registry_demands():
        lines.append(f"\n{name} ({key}):")
        lines += [f"  - {d}" for d in demands]
    return "\n".join(lines)
