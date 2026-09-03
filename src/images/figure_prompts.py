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


# ---------------------------------------------------------------------------
# Diagram prompts — The Analyst's figure step (labelled analytical diagrams)
#
# Assembled in analyzer v1's order (gemini_image.py render(): format enforcement
# block → style guide directive → content → final layout reminder), with the
# labelled data spelled out from the FigureSpec so the image model has nothing
# to invent. `build_figure_prompt` above is the old scene/register register and
# is NOT used by the dossier's figure step any more.
# ---------------------------------------------------------------------------

DIAGRAM_CLOSER = (
    "A single clean diagram on a plain background — no scenery, no metaphors, "
    "no photographs, no 3D objects."
)

DIAGRAM_TEXT_RULES = [
    "Every label at least 14pt-equivalent; titles larger; nothing that needs zooming",
    "High contrast with its background (≥ 4.5:1); dark on light OR light on dark",
    "Each label on a clean area, never overlapping a line, an arrow or another label",
    "Only the words in the CONTENT block and the TITLE — invent no other words, names, dates or numbers",
    "Spell every label exactly as written; never abbreviate, never paraphrase, never garble",
    "No underscores or snake_case in visible text; Title Case for labels",
    "Never print raw decimals, weights or scores (0.85, 'weight: 3'); encode them visually (position, width, size)",
    "No logos, bylines, source lines, credits, watermarks, dates or publication marks",
    "No subtitle, no callout boxes, no 'insight' / 'conclusion' / 'key finding' notes, no explanatory sentences: "
    "the ONLY text in the image is the title and the content labels",
    "Never print coordinates, positions, percentages, widths or sizes next to items — placement instructions in "
    "the content (left/right, top/bottom, thick/thin, large/small) are for you, not for the reader",
]

# Lines in a school's gemini_modifiers that would pull a diagram back toward illustration.
_STYLE_LINE_DROP = ("metaphor", "dramatic", "lighting", "attribution", "social media", "byline",
                    "source", "fill the frame", "logo", "line chart", "photograph", "hang on a wall",
                    "headline", "annotation", "callout", "teaching", "how to read", "narrative", "subtitle",
                    "insight", "call to action", "position", "urgency", "small multiples")


def style_for_school(school: str | None) -> dict[str, Any]:
    """Style dict (for build_style_override / build_style_closing) from a style school
    in src/styles: palette, typography, register, filtered gemini_modifiers."""
    if not school:
        return {}
    try:
        from src.styles.registry import get_style_registry
        from src.styles.schemas import StyleSchool

        guide = get_style_registry().get_style(StyleSchool(str(school)))
    except Exception as exc:  # unknown school or registry unavailable: no style, not a failure
        logger.info("style_school_unavailable", extra={"school": school, "error": str(exc)[:200]})
        return {}
    if guide is None:
        return {}
    pal, typ = guide.color_palette, guide.typography
    modifiers = [ln.strip() for ln in (guide.gemini_modifiers or "").splitlines()
                 if ln.strip() and not any(w in ln.lower() for w in _STYLE_LINE_DROP)]
    principles = [p for p in guide.layout_principles if not any(w in p.lower() for w in _STYLE_LINE_DROP)]
    palette_desc = "\n".join(modifiers[:14])
    series = list(pal.series_palette or []) or [c for c in (pal.primary, pal.accent, pal.accent_alt, pal.positive,
                                                            pal.highlight, pal.secondary, pal.negative) if c]
    palette_desc += ("\nCATEGORICAL COLORS (use these, in order, to color-code the diagram's groups, ribbons, "
                     "boxes or series — a diagram must never be monochrome): " + ", ".join(series[:7]))
    if principles:
        palette_desc += "\nLayout principles: " + "; ".join(principles[:8])
    layout_text = " ".join(guide.layout_principles).lower()
    style: dict[str, Any] = {
        "background": pal.background,
        "primary_color": pal.primary,
        "accent_color": pal.accent,
        "secondary_accent": pal.secondary,
        "text_color": pal.text,
        "typography": (f"titles in {typ.title_font}; labels in {typ.primary_font}; "
                       f"title weight {typ.title_weight}; every label >= 14pt equivalent"),
        "register": f"{guide.name}: {guide.philosophy.split('.')[0].strip()}.",
        "palette_description": palette_desc,
        "no_shadows": "no shadows" in layout_text or "no 3d" in layout_text,
        "no_gradients": "no gradients" in layout_text or "no shadows or gradients" in layout_text,
        "forbidden": ["pictorial metaphors, scenery, objects or characters standing in for the data",
                      "dramatic lighting, glows, lens effects, textures that reduce label contrast",
                      "subtitles, callout boxes, 'insight'/'conclusion'/'pattern' notes, explanatory sentences — "
                      "the only text is the title and the content labels"],
        "school": str(school),
    }
    return style


def _spec_dict(spec: Any) -> dict[str, Any]:
    if hasattr(spec, "model_dump"):
        return spec.model_dump()
    if isinstance(spec, dict):
        return spec
    raise TypeError("spec must be a FigureSpec or a dict")


def build_diagram_prompt(
    spec: Any,
    *,
    style_school: str | None = None,
    aspect: str | None = None,
    revision_notes: list[str] | str | None = None,
) -> str:
    """Compose the prompt for one labelled analytical diagram from a FigureSpec (or dict).

    Order (v1's): format enforcement block (must_have / must_not / GLOBAL_PROHIBITIONS /
    legibility) → style-school directive (MANDATORY STYLE OVERRIDE) → the labelled data
    spelled out + label manifest → title placement → text rules → aspect → revision
    notes (retry) → closing sentence → style closing (recency).
    """
    from src.display.enforcement import (
        aspect_for, collect_labels, enforcement_block, format_entry, normalize_format_key,
        render_data, validate_data,
    )

    d = _spec_dict(spec)
    fmt = normalize_format_key(str(d.get("visual_format") or ""))
    if fmt is None:
        raise ValueError(f"unknown visual_format {d.get('visual_format')!r}")
    entry = format_entry(fmt)
    title = str(d.get("title") or "").strip()
    if not title:
        raise ValueError("spec.title is required (it is rendered)")
    data = d.get("data") or {}
    errors = validate_data(fmt, data)
    if errors:
        raise ValueError("spec.data does not fit the format: " + "; ".join(errors[:5]))
    labels = collect_labels(data)
    aspect = aspect or d.get("aspect") or aspect_for(fmt)
    school = style_school or d.get("style_school") or None
    style = style_for_school(school)

    parts: list[str] = [
        f"Create a {entry['name'].upper()} — a single, clean, LABELLED ANALYTICAL DIAGRAM. Its title is: {title}",
        "It is a data visualization of the CONTENT below, the kind a consulting deck or a newspaper graphics "
        "desk would publish: flat shapes, lines, arrows and text. It is NOT a picture, a scene, an object or a metaphor.",
        enforcement_block(fmt).strip(),
        "",
    ]
    if style:
        parts.append(build_style_override(style).rstrip())
        parts.append(f"STYLE SCHOOL: {school} (the palette/typography above). Apply it to a DIAGRAM: colors on boxes, "
                     "arrows, bands and labels — never as illustration.")
        parts.append("")
    parts.append("CONTENT TO RENDER (this is the ENTIRE content of the diagram — render every label exactly as "
                 "written, spelled exactly, and invent no other words, names, numbers or dates):")
    parts.append(render_data(fmt, data))
    parts.append("")
    parts.append(f"LABEL MANIFEST — each of these {len(labels)} strings must appear exactly once, legibly, spelled as written:")
    parts.extend(f"  • {lab}" for lab in labels)
    parts.append("")
    parts.append(f"TITLE (render exactly this text once, at the top, larger than any other text, WITHOUT quotation "
                 f"marks around it): {title}")
    parts.append("Under the title: nothing. No subtitle, no byline, no source line, no logo, no watermark, no page furniture.")
    caption = str(d.get("caption") or "").strip()
    if caption:
        parts.append(f"CONTEXT (do NOT render this): the caption printed under the figure will say — “{caption}”. "
                     "Use it only to understand what the diagram must make visible.")
    parts.append("")
    parts.append("TEXT RULES:")
    parts.extend(f"  ✓ {r}" for r in DIAGRAM_TEXT_RULES)
    parts.append("")
    parts.append(f"FRAME: compose for a {aspect} aspect ratio; the diagram fills the frame with even margins; "
                 "nothing is cropped at the edges.")
    notes = revision_notes
    if isinstance(notes, str):
        notes = [notes]
    notes = [str(n).strip() for n in (notes or []) if str(n).strip()]
    if notes:
        parts.append("")
        parts.append("REVISION NOTES from the reviewer of the previous attempt — fix ALL of these:")
        parts.extend(f"  ! {n}" for n in notes)
    parts.append("")
    parts.append(DIAGRAM_CLOSER)
    parts.append(f"FINAL REMINDER: LAYOUT IS MANDATORY. You MUST use the {entry['name'].upper()} layout as specified "
                 "above. DO NOT substitute a generic network diagram, a freestyle chart or an illustration.")
    if style:
        parts.append(build_style_closing(style).rstrip())
    return "\n".join(parts).strip() + "\n"
