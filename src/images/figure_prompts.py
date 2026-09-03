"""Scene prose → image-model prompt for analytical figures.

Lifts, in order of assembly:
  1. veo2 docs/visual-doctrine/TAXONOMY.md register openers (enforcement
     keywords stated verbatim, never paraphrased) — adapted from motion to
     still figures, plus two registers The Analyst needs (photographic,
     archival).
  2. analyzer src/renderers/gemini_image.py `_build_style_guide_directive`
     (MANDATORY STYLE OVERRIDE block, precedence rule) and its closing
     reinforcement ("sandwich" — 0/39 images followed a palette with only
     the opening block).
  3. analyzer format-enforcement simplicity rules (MAX 8 elements, MAX 3
     levels, generous whitespace, one message) and GLOBAL_PROHIBITIONS,
     re-cut for editorial figures: metaphor is allowed here (it is the
     point), but dramatic effects, disaster imagery, water-mass crowds,
     charts-with-axes and photoreal identifiable people are not.
  4. veo2 NO-TEXT closer, extended with the mandarin-videos NO_TEXT_RULE
     ("signs, screens, pages, plaques are blank") because Qwen and Seedream
     invent in-scene signage otherwise.

`declutter_scene` is the optional Sonnet pass (analyzer's declutter step)
that turns list-like analytic content into ONE depictable scene.
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger("images.prompts")

# ---------------------------------------------------------------------------
# Registers — openers are pasted verbatim at the top of every prompt
# ---------------------------------------------------------------------------

REGISTERS: dict[str, dict[str, Any]] = {
    "editorial": {
        "label": "Editorial illustration",
        "opener": (
            "Hand-drawn editorial illustration: ink outlines, watercolor washes, "
            "visible paper texture, restrained muted palette, sketch-faced drawn "
            "characters — never photorealistic humans."
        ),
        "strengths": "lived settings, hidden forces inside everyday scenes, chronology, one anchor metaphor",
        "avoid": [
            "photorealistic rendering or photographic textures",
            "glossy 3D render, airbrush, neon glow",
            "detailed realistic facial features",
        ],
    },
    "diagrammatic": {
        "label": "Flat vector diagram",
        "opener": (
            "Clean flat vector diagram: flat iconographic shapes, pictogram figures "
            "instead of people, restrained flat palette on a plain light studio "
            "background, generous whitespace — no photorealistic humans."
        ),
        "strengths": "structure, hierarchy, flows, networks, levels, mechanism — relationships shown through position, size, adjacency, containment and plain connecting lines",
        "avoid": [
            "charts with axes, gridlines, tick marks or labeled bars — use textless pictorial twins (fields of icons, growing stacks, nested shapes)",
            "3D isometric render, drop shadows, bevels",
            "photographic or painterly textures",
            "dense network webs with more than ~8 nodes",
        ],
    },
    "photographic": {
        "label": "Documentary photograph",
        "opener": (
            "Editorial documentary photograph: natural light, restrained color "
            "grading, real materials and textures, shallow depth of field; objects, "
            "spaces, hands and backs of figures rather than faces — no identifiable "
            "real persons, no staged stock-photo poses."
        ),
        "strengths": "materials, places, artefacts, atmosphere, the texture of a practice",
        "avoid": [
            "recognizable faces or likenesses of real people (mimetic substitution is forbidden)",
            "stock-photo smiles, handshakes, pointing-at-whiteboard poses",
            "brand logos, product marks, real signage",
            "HDR, lens flare, cinematic teal-orange grading",
        ],
    },
    "archival": {
        "label": "Paper cutout / archival collage",
        "opener": (
            "Paper cutout collage: layered torn-edge paper and archival print "
            "textures, visible shadows between layers, cream, aged-yellow, "
            "institutional-blue and ink-black palette with red-stamp accents, "
            "cut-paper figures whose features are abstracted by the medium — never "
            "photorealistic humans."
        ),
        "strengths": "institutions, governance, paper trails, provenance, corkboard networks, document-flavored material",
        "avoid": [
            "photorealistic rendering",
            "fabricated legible documents, stamps with readable words, forged records",
            "glossy or digital textures",
        ],
    },
}

DEFAULT_REGISTER = "editorial"

# ---------------------------------------------------------------------------
# Universal rules (all registers)
# ---------------------------------------------------------------------------

SIMPLICITY_RULES = [
    "ONE clear scene with ONE message — not a collage of many ideas",
    "MAX 8 distinct visual elements (figures, objects, shapes, groups)",
    "MAX 3 levels of hierarchy or nesting",
    "GENEROUS whitespace; publication quality; readable at a glance",
    "Composed for the stated aspect ratio; the subject fills the frame with intent",
]

# Re-cut from analyzer GLOBAL_PROHIBITIONS + veo2 TAXONOMY §1 for figures
# that are illustrations, not data-viz. Metaphor is allowed; melodrama is not.
FIGURE_PROHIBITIONS = [
    "Dramatic visual effects: lightning, explosions, fractures, cracks, energy bursts, cosmic imagery — even if the topic says 'tension', 'rupture' or 'collision'",
    "Natural-disaster metaphors: storms, earthquakes, fires, tidal waves, volcanoes",
    "Water-mass metaphors for people (waves, floods, streams of humans); crowds as undifferentiated mass — prefer ONE stylized individual with posture and agency",
    "Photorealistic identifiable people, real leaders, real institutions as cute characters — use neutral stylized or geometric stand-ins",
    "Real brand logos, trademarks, product packaging, corporate wordmarks",
    "Charts with axes, gridlines, tick marks, legends or labeled bars",
    "UI chrome, screenshots, badges, watermarks, frames or borders around the image",
    "Busy or textured backgrounds that swallow the subject; more than one focal point",
    "Physical-object clichés as containers for ideas: cardboard boxes, gift packages, jigsaw puzzles, lightbulbs, gears-in-a-head",
]

# veo2 ⟦NO-TEXT⟧ closer (verbatim first sentence), extended with the
# mandarin-videos NO_TEXT_RULE and the Qwen "blank signage" clause.
NO_TEXT_CLOSER = (
    "No on-screen text, no captions, no subtitles, no signs, no lettering. "
    "The image must contain NO text of any kind: no letters, no numbers, no words, "
    "no labels, no annotations, no speech bubbles, no watermarks, no logos, no "
    "typographic marks in any script. Any signs, screens, pages, book spines, "
    "plaques, tags or frames that appear in the scene are BLANK."
)

# Used only when the caller explicitly allows rendered text (no_text=False).
TEXT_LEGIBILITY_RULES = [
    "Minimum 14pt-equivalent font size (readable without zooming)",
    "High contrast with background (≥ 4.5:1); dark on light OR light on dark",
    "Placed on clean, uncluttered areas; never overlapping other elements",
    "Only the words given in the scene description — invent no other words, names, dates or numbers",
    "Spell every word exactly; if a word cannot be rendered cleanly, omit it rather than garble it",
]


# ---------------------------------------------------------------------------
# Style override (lifted from analyzer gemini_image.py:2640-2757 + closing)
# ---------------------------------------------------------------------------

STYLE_KEYS = (
    "background", "primary_color", "accent_color", "secondary_accent", "text_color",
    "typography", "signature_shapes", "register", "palette_description",
    "no_dark_backgrounds", "no_gradients", "no_shadows", "forbidden",
)

_RULE = "═" * 79


def build_style_override(style: dict[str, Any] | None) -> str:
    """MANDATORY STYLE OVERRIDE block (top of prompt). '' when no style."""
    if not style or not isinstance(style, dict):
        return ""
    lines = [
        _RULE,
        "                  MANDATORY STYLE OVERRIDE — READ BEFORE ALL ELSE",
        _RULE,
        "",
        "The caller has supplied a STRUCTURED STYLE GUIDE that REPLACES any "
        "background, palette, typography, or aesthetic directive that may appear "
        "elsewhere in this prompt. If any later instruction conflicts with the "
        "directives in this section, the directives in THIS section win. The "
        "caller's style is non-negotiable.",
        "",
    ]
    if style.get("background"):
        lines.append(f"BACKGROUND (mandatory): {style['background']}")
        lines.append(
            "  → IGNORE any 'dark background', 'noir', 'gradient', or atmospheric "
            "background directive that may appear elsewhere. Use ONLY the background above."
        )
    color_lines = []
    if style.get("primary_color"):
        color_lines.append(f"  Primary: {style['primary_color']}")
    if style.get("accent_color"):
        color_lines.append(f"  Accent: {style['accent_color']}")
    if style.get("secondary_accent"):
        color_lines.append(f"  Secondary accent: {style['secondary_accent']}")
    if style.get("text_color"):
        color_lines.append(f"  Text: {style['text_color']}")
    if color_lines:
        lines.append("")
        lines.append("PALETTE (mandatory — use these exact colors, no substitutions):")
        lines.extend(color_lines)
    if style.get("typography"):
        lines.append("")
        lines.append(f"TYPOGRAPHY (mandatory): {style['typography']}")
    if style.get("signature_shapes"):
        lines.append("")
        lines.append(f"SIGNATURE SHAPES: {style['signature_shapes']}")
    if style.get("register"):
        lines.append(f"REGISTER / TONE: {style['register']}")
    if style.get("palette_description"):
        lines.append("")
        lines.append("PALETTE DESCRIPTION (mandatory, overrides any other palette):")
        lines.append(str(style["palette_description"]))
    prohibitions = []
    if style.get("no_dark_backgrounds"):
        prohibitions.append("dark backgrounds (use the mandated background only)")
    if style.get("no_gradients"):
        prohibitions.append("gradients (use flat colors)")
    if style.get("no_shadows"):
        prohibitions.append("drop shadows, bevels, or 3D effects")
    forbidden = style.get("forbidden")
    if isinstance(forbidden, list):
        prohibitions.extend(str(f) for f in forbidden)
    if prohibitions:
        lines.append("")
        lines.append("FORBIDDEN (do not use any of these):")
        lines.extend(f"  • {p}" for p in prohibitions)
    lines += [
        "",
        "PRECEDENCE RULE: when this style guide conflicts with anything else in this "
        "prompt, follow the style guide. The scene text below describes WHAT to depict; "
        "the style guide above describes HOW IT MUST LOOK. Both must be honored, but on "
        "visual conflict, this section wins.",
        _RULE,
        "",
    ]
    return "\n".join(lines)


def build_style_closing(style: dict[str, Any] | None) -> str:
    """Compact closing reinforcement (end of prompt) — exploits recency bias."""
    if not style or not isinstance(style, dict):
        return ""
    lines = ["", _RULE, "           FINAL STYLE OVERRIDE (REPEATED — DO NOT IGNORE)", _RULE, ""]
    lines.append(
        "Before you generate the image, reconfirm the following style requirements. "
        "These OVERRIDE any palette, background, atmosphere, or aesthetic directive "
        "that appeared earlier in this prompt. If your draft uses different colors or "
        "a different background, REJECT your draft and regenerate it to match:"
    )
    lines.append("")
    if style.get("background"):
        lines.append(f"  ✓ BACKGROUND MUST BE: {style['background']} — fills the entire canvas, solid, uniform.")
    if style.get("primary_color"):
        lines.append(f"  ✓ PRIMARY ACCENT COLOR (emphasis): {style['primary_color']}")
    if style.get("accent_color"):
        lines.append(f"  ✓ SECONDARY ACCENT (contrast / categorical): {style['accent_color']}")
    if style.get("secondary_accent"):
        lines.append(f"  ✓ TERTIARY ACCENT: {style['secondary_accent']}")
    if style.get("text_color"):
        lines.append(f"  ✓ TEXT COLOR: {style['text_color']}")
    if style.get("palette_description"):
        lines.append(f"  ✓ PALETTE: {style['palette_description']}")
    if style.get("no_dark_backgrounds"):
        lines.append("  ✗ NO DARK BACKGROUNDS. Reject navy, black, charcoal, slate, midnight, noir themes.")
    if style.get("no_gradients"):
        lines.append("  ✗ NO GRADIENTS. Flat, solid colors only.")
    if style.get("no_shadows"):
        lines.append("  ✗ NO DROP SHADOWS, BEVELS, GLOWS, or 3D EFFECTS. Pure flat 2D.")
    lines.append("")
    lines.append(
        "PALETTE CHECK BEFORE FINAL RENDER: scan your draft; if it contains a color, "
        "background or effect not permitted above, fix it before rendering."
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# The figure prompt
# ---------------------------------------------------------------------------

def register_opener(register: str) -> str:
    try:
        return REGISTERS[register]["opener"]
    except KeyError:
        raise ValueError(
            f"unknown register {register!r}; known: {sorted(REGISTERS)}"
        ) from None


def build_figure_prompt(
    scene: str,
    *,
    register: str = DEFAULT_REGISTER,
    palette: str | None = None,
    caption: str | None = None,
    no_text: bool = True,
    extra_prohibitions: list[str] | None = None,
    aspect: str | None = None,
    style: dict[str, Any] | None = None,
) -> str:
    """Compose the full prompt for one analytical figure.

    Order (each block validated in its source project):
      style override (if any) → register opener → SCENE → palette → caption
      context → composition rules → register avoid-list + universal
      prohibitions + extras → text rule (NO-TEXT closer or legibility rules)
      → style closing (if any).
    """
    scene = (scene or "").strip()
    if not scene:
        raise ValueError("scene must be a non-empty description")
    reg = REGISTERS.get(register)
    if reg is None:
        raise ValueError(f"unknown register {register!r}; known: {sorted(REGISTERS)}")

    parts: list[str] = []
    style_open = build_style_override(style)
    if style_open:
        parts.append(style_open)

    parts.append(reg["opener"])
    parts.append("")
    parts.append("SCENE (depict exactly this, as one coherent picture):")
    parts.append(scene)
    parts.append("")
    if palette:
        parts.append(f"PALETTE (mandatory): {palette}")
    if aspect:
        parts.append(f"FRAME: compose for a {aspect} aspect ratio.")
    if caption:
        parts.append(
            "CONTEXT: the surrounding document will print this caption beneath the "
            f"figure — “{caption.strip()}”. The caption is set by the document, NOT "
            "inside the image; use it only to understand what the picture must convey."
        )
    parts.append("")
    parts.append(f"REGISTER STRENGTHS to lean on: {reg['strengths']}.")
    parts.append("")
    parts.append("COMPOSITION RULES:")
    parts.extend(f"  ✓ {r}" for r in SIMPLICITY_RULES)
    parts.append("")
    parts.append("DO NOT (any of these is a failed image):")
    parts.extend(f"  ✗ {a}" for a in reg["avoid"])
    parts.extend(f"  ✗ {p}" for p in FIGURE_PROHIBITIONS)
    for p in extra_prohibitions or []:
        p = str(p).strip()
        if p:
            parts.append(f"  ✗ {p}")
    parts.append("")
    if no_text:
        parts.append(NO_TEXT_CLOSER)
    else:
        parts.append("TEXT RULES (text is permitted ONLY as specified in the scene):")
        parts.extend(f"  ✓ {r}" for r in TEXT_LEGIBILITY_RULES)
    style_close = build_style_closing(style)
    if style_close:
        parts.append(style_close)
    return "\n".join(parts).strip() + "\n"


def ensure_no_text(prompt: str) -> str:
    """Append the NO-TEXT closer if the prompt does not already carry it."""
    if NO_TEXT_CLOSER.split(".")[0] in prompt:
        return prompt
    return prompt.rstrip() + "\n\n" + NO_TEXT_CLOSER + "\n"


# ---------------------------------------------------------------------------
# Declutter (optional, key-gated Sonnet pass — analyzer's declutter step)
# ---------------------------------------------------------------------------

DECLUTTER_MODEL = "claude-sonnet-4-6"

DECLUTTER_PROMPT = """You are turning analytical content into ONE depictable scene for an illustrator.

The illustrator cannot render text, lists, tables, labels, numbers or names. Everything
must be conveyed by what is VISIBLE: subjects, objects, spatial arrangement, scale,
adjacency, containment, posture, light, material, palette.

STRATEGY (hierarchical compression with the analysis preserved):
- Identify the single most important relationship or structure in the content
- Choose ONE anchor image for it (a lattice, a workshop, a hand passing a garment, a
  corridor of doors, nested rooms, a procession...) — concrete, not a cliché
  (no lightbulbs, gears, puzzle pieces, bridges, storms, explosions)
- Express hierarchy through position and size; flow through direction; tension through
  distance, not through cracks or lightning
- MAX 8 distinct visual elements — COUNT them; merge or drop the rest
- NEVER write "[N items]" or enumerate list items — translate them into visible things
- NO numbers, percentages, scores, dates, names or words meant to be read in the image
- Keep the register neutral: describe the scene, not the style (style is added later)

CONTENT:
---
{content}
---

Return ONLY the scene description as a single paragraph of 60-140 words. No preamble,
no headings, no bullet points, no quotation marks."""


def declutter_scene(
    scene: str,
    *,
    model: str = DECLUTTER_MODEL,
    api_key: str | None = None,
    max_tokens: int = 600,
) -> str:
    """Compress text-heavy analytic content into a single depictable scene.

    Key-gated and fail-safe: without ANTHROPIC_API_KEY (or on any error) the
    input is returned unchanged, so callers can always chain it.
    """
    scene = (scene or "").strip()
    if not scene:
        return scene
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        logger.info("declutter_skipped", extra={"reason": "no ANTHROPIC_API_KEY"})
        return scene
    try:
        import anthropic  # local import: optional dependency at runtime

        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": DECLUTTER_PROMPT.format(content=scene)}],
        )
        text = "".join(getattr(b, "text", "") for b in resp.content).strip()
        if not text:
            return scene
        text = text.strip('"“”').strip()
        logger.info(
            "declutter_complete",
            extra={"model": model, "in_chars": len(scene), "out_chars": len(text)},
        )
        return text
    except Exception as exc:  # noqa: BLE001 — declutter is best-effort by design
        logger.warning("declutter_failed", extra={"error": str(exc)[:300]})
        return scene
