"""Format enforcement for labelled analytical diagrams.

Ported from analyzer v1 `src/renderers/gemini_image.py` (`GLOBAL_PROHIBITIONS`,
`FORMAT_ENFORCEMENT`, `FORMAT_VALIDATION_CRITERIA`, `get_format_enforcement_prompt`)
and `src/core/visualization_palettes.py` (`VISUAL_FORMAT_INSTRUCTIONS`), then
extended with must_have/must_not rules for every diagram format in the v2 catalog
(`src/display/definitions/visual_formats.json`) and for the primitives' visual
forms (`src/primitives/definitions/primitives.json`) that the catalog lacks.

Three things live here and nowhere else:

  * `GLOBAL_PROHIBITIONS`  — v1's universal data-viz rules, verbatim.
  * `FORMAT_ENFORCEMENT`   — one entry per canonical format: name, data-shape
    `family`, preferred `aspect`, `must_have`, `must_not`, `reference_style`,
    `visual_signature`, and the vision-check criteria `pass_if` / `fail_if`.
  * `DATA_SHAPES`          — one entry per data-shape family: the JSON template a
    FigureSpec's `data` must follow, a validator (shape only, never merit), a
    prose renderer for the prompt, and the label walker.

v1 formats that are metaphors rather than diagrams (bridge_diagram,
stress_fracture, reflexive_loop, parallax_view, inheritance_chain,
bundled_box, horizon_fade) are deliberately NOT ported: the owner's rule for
The Analyst is "diagrams, flows, venns — no drawings".
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Optional

# ---------------------------------------------------------------------------
# GLOBAL prohibitions — analyzer v1 gemini_image.py:1039-1052, verbatim
# ---------------------------------------------------------------------------

GLOBAL_PROHIBITIONS = [
    "Physical objects as containers (boxes, packages, cases, folders, vessels)",
    "3D rendered objects or isometric illustrations of real-world items",
    "Metaphorical imagery (bridges, buildings, landscapes, machinery)",
    "Photorealistic elements or photographs",
    "Artistic interpretations that prioritize aesthetics over data clarity",
    "Any representation that looks like a physical artifact rather than a data visualization",
    # TEXT LEGIBILITY - these are critical for usability
    "Text smaller than 14pt equivalent (all labels MUST be readable without zooming)",
    "Dramatic visual effects that compete with text readability (lightning, explosions, fractures, cracks)",
    "Natural phenomena as metaphors (waterfalls, storms, earthquakes, fires, waves)",
    "Background imagery that reduces text contrast below 4.5:1 ratio",
    "Overlapping text or text placed on busy/textured backgrounds",
]

LEGIBILITY_RULES = [
    "Minimum 14pt equivalent font size (readable without zooming)",
    "High contrast with background (dark on light OR light on dark)",
    "Placed on clean, uncluttered backgrounds",
    "NOT overlapping with other elements",
    "NOT placed on busy textures, dramatic effects, or photographic backgrounds",
]

_PRO = "PROFESSIONAL STYLING: Like a McKinsey/BCG consulting slide, NOT a plain technical diagram"
_RICH = "VISUALLY RICH: Use color coding, gradients, or subtle backgrounds to make elements visually distinct"
_LARGE = "LARGE, READABLE LABELS on every element (minimum 14pt equivalent), clean background, high contrast"
_NO_META = "Scenery, physical objects, people, machinery or any pictorial metaphor standing in for the data"
_NO_DRAMA = "Dramatic effects, lightning, cracks, storms, cosmic imagery — even if the topic says 'tension' or 'collision'"
_NO_SMALL = "Text smaller than 14pt or requiring zooming to read; busy or textured backgrounds"


def _entry(name: str, family: str, aspect: str, must_have: list[str], must_not: list[str],
           reference_style: str, visual_signature: str, *, source: str = "v2",
           pass_if: Optional[list[str]] = None, fail_if: Optional[list[str]] = None) -> dict[str, Any]:
    return {
        "name": name, "family": family, "aspect": aspect, "source": source,
        "must_have": must_have, "must_not": must_not,
        "reference_style": reference_style, "visual_signature": visual_signature,
        "pass_if": pass_if or [], "fail_if": fail_if or [],
    }


# ---------------------------------------------------------------------------
# FORMAT_ENFORCEMENT — canonical keys. v1 entries first (source="v1"), then the
# v1 VISUAL_FORMAT_INSTRUCTIONS that are diagrams (source="v1-palette"), then
# the v2 catalog and primitive forms (source="v2").
# ---------------------------------------------------------------------------

FORMAT_ENFORCEMENT: dict[str, dict[str, Any]] = {
    # ----- analyzer v1 FORMAT_ENFORCEMENT (gemini_image.py:1054-1427) -----
    "flowchart": _entry(
        "Process Flowchart", "steps", "16:9",
        ["Rectangular boxes connected by arrows",
         "Clear START and END points",
         "Left-to-right OR top-to-bottom sequential flow",
         "Decision diamonds with Yes/No branches (if applicable)",
         "Each step in its own labeled box",
         _RICH.replace("elements", "boxes"), _PRO],
        ["Spectrum or gradient bars", "Side-by-side comparisons or dual columns", "Radial/circular layouts",
         "Tree structures with branches", "Network webs with nodes", "Funnel diagrams", "Timeline formats",
         "Plain black lines on white background (BORING - add color!)", "Monochrome styling without visual interest"],
        "Like a premium consulting firm presentation slide - clear structure with professional color palette, subtle gradients, and visual hierarchy",
        "Color-coded boxes with professional styling, connected by clear directional arrows",
        source="v1",
        pass_if=["labeled boxes connected by arrows", "one sequential direction", "clear start and end"],
        fail_if=["network web", "radial layout", "timeline axis", "physical objects", "scenery"]),
    "timeline": _entry(
        "Chronological Timeline", "events", "16:9",
        ["Horizontal OR vertical time axis with dates/periods marked",
         "Events positioned along the axis by chronological order",
         "Clear date labels (years, periods, eras)",
         "Sequential progression from past to future",
         "Milestones marked on a single continuous line",
         "LARGE, READABLE TEXT labels for all events (minimum 14pt equivalent)",
         "Clean background with high text contrast"],
        ["Bridge/crossing metaphors", "Convergence diagrams", "Left-right bank imagery", "Parallel comparison columns",
         "Radial or circular layouts", "Network/web structures", "Tree or branching structures",
         "Historical scene illustrations or period imagery", "Dramatic backgrounds (battlefields, storms, fires)",
         "Text smaller than 14pt or requiring zooming to read", "Busy or textured backgrounds that reduce label readability"],
        "Like a clean museum exhibit timeline or Wikipedia history timeline - professional, readable, and data-focused",
        "A single horizontal/vertical line with dated events and LARGE READABLE LABELS",
        source="v1",
        pass_if=["time axis", "chronological", "dates marked", "horizontal or vertical line with events"],
        fail_if=["bridge metaphor", "crossing imagery", "convergence diagram", "architectural metaphor", "scene illustration"]),
    "sankey_diagram": _entry(
        "Sankey Flow Diagram", "flows", "16:9",
        ["Sources on LEFT, destinations on RIGHT",
         "Flowing bands/ribbons connecting sources to destinations",
         "Band WIDTH proportional to flow quantity",
         "Clear left-to-right directional flow",
         "Multiple streams merging or diverging",
         "LARGE, READABLE LABELS on sources and destinations (minimum 14pt equivalent)",
         "Clean background with high text contrast"],
        ["Collision/explosion/crack imagery", "Artistic metaphors or abstract representations", "Radial or circular layouts",
         "Network webs or graphs", "Tree/hierarchical structures", "Comparison charts or dual columns",
         "Natural phenomena (waterfalls, rivers, storms) - even if data is about 'flows'",
         "Dramatic visual effects or cosmic imagery", "Text smaller than 14pt or requiring zooming to read",
         "Busy backgrounds that reduce label readability"],
        "Like a clean D3.js Sankey diagram showing energy flows or budget allocations - professional and readable",
        "Curved ribbons flowing left-to-right with LARGE READABLE labels, width = quantity",
        source="v1",
        pass_if=["flowing ribbons", "left-to-right flow", "bands connecting", "width proportional"],
        fail_if=["collision", "explosion", "crash imagery", "comparison columns", "side-by-side", "river scenery"]),
    "structured_diagram": _entry(
        "Structured Organizational Diagram", "columns", "16:9",
        ["Clear hierarchical or grid-based organization", "Labeled boxes or sections",
         "Logical groupings (quadrants, categories, levels)", "Clean visual hierarchy with headers",
         "Organized spatial layout (not random placement)"],
        ["Artistic/metaphorical imagery", "Timeline or chronological elements", "Network webs or graphs",
         "Flow diagrams with arrows", "Radial/sunburst layouts"],
        "Like a business org chart or a 2x2 strategic matrix",
        "Boxes arranged in clear rows/columns or hierarchy",
        source="v1",
        pass_if=["hierarchical boxes", "grid organization", "clear sections", "labeled regions"],
        fail_if=["network web", "timeline", "flowing ribbons", "physical objects"]),
    "network_graph": _entry(
        "Network Relationship Graph", "network", "4:3",
        ["Nodes (circles or boxes) representing entities", "Edges (lines) connecting related nodes",
         "Labels on nodes identifying entities - TEXT MUST BE LARGE AND READABLE (minimum 14pt equivalent)",
         "Edge labels naming the relationship where one is given",
         "Visual clustering of related nodes", "Clean, uncluttered background (solid color or subtle gradient)",
         "High contrast between text and background (dark text on light, or light text on dark)"],
        ["Timeline/chronological layouts", "Flow diagrams with sequential steps", "Hierarchical tree structures",
         "Sankey/alluvial ribbons", "Spectrum/gradient bars", "Scorecards or checklists with checkmarks/X marks",
         "Gains/losses tables or pro/con layouts", "Tabular or grid layouts presenting items as lists",
         "Balance scale or ledger metaphors",
         "Lightning, cracks, fractures, or collision imagery - even if the TOPIC mentions 'stress' or 'tension'",
         "Natural phenomena backgrounds (storms, waterfalls, volcanoes, earthquakes)",
         "Dramatic visual effects that distract from the data (explosions, energy bursts, cosmic imagery)",
         "Busy or textured backgrounds that reduce text legibility", "Text smaller than 14pt or text requiring zooming to read"],
        "Like a clean social network visualization, knowledge graph, or D3.js force-directed graph - professional and readable",
        "Nodes connected by lines showing relationships, with LARGE READABLE LABELS on a clean background",
        source="v1",
        pass_if=["nodes connected by lines", "edges", "circles or boxes connected", "relationship arrows"],
        fail_if=["scorecard", "checklist", "gains/losses", "table format", "pro/con list", "ledger"]),
    "treemap": _entry(
        "Hierarchical Treemap", "regions", "4:3",
        ["Nested rectangles filling the space", "Rectangle SIZE proportional to value", "Color-coded categories",
         "Labels inside rectangles", "No whitespace - rectangles fill the area", "FLAT 2D rectangles only (no depth, no perspective)"],
        ["Circular/radial layouts", "Tree diagrams with branches", "Network webs", "Flow diagrams", "Timeline layouts",
         "3D boxes, containers, packages, or compartments", "Physical object metaphors (cases, folders, vessels, containers)",
         "Isometric or perspective views with depth", "Stacked or layered elements suggesting physical depth"],
        "Like a disk space visualization or stock market treemap",
        "Packed rectangles of varying sizes, no gaps",
        source="v1",
        pass_if=["nested rectangles", "flat 2D layout", "color-coded sections", "rectangles filling space"],
        fail_if=["3D box", "container", "package", "isometric", "depth perspective", "physical object", "compartments"]),
    "matrix": _entry(
        "Grid/Matrix Layout", "matrix", "4:3",
        ["Rows and columns forming a grid", "Clear row and column headers", "Cells containing values or indicators",
         "Consistent cell sizing", _LARGE],
        ["Network graphs", "Flow diagrams", "Timeline layouts", "Radial charts", "Tree structures", _NO_META],
        "Like a comparison matrix or feature grid",
        "Clean grid with labeled rows and columns",
        source="v1",
        pass_if=["grid of cells", "row headers", "column headers", "values in cells"],
        fail_if=["network", "flow ribbons", "timeline", "physical objects"]),
    "matrix_heatmap": _entry(
        "Color-Coded Heatmap Matrix", "matrix", "4:3",
        ["Grid of cells with color intensity", "Color scale from low to high values", "Row and column labels",
         "Legend showing color-to-value mapping", _LARGE],
        ["Network graphs", "Flow diagrams", "Tree structures", "Timeline layouts", _NO_META],
        "Like a correlation matrix or calendar heatmap",
        "Grid where color intensity shows magnitude",
        source="v1",
        pass_if=["grid of colored cells", "row and column labels", "color legend"],
        fail_if=["network", "flow ribbons", "timeline", "physical objects"]),
    "conceptual_landscape": _entry(
        "Conceptual Landscape/Territory Map", "regions", "16:9",
        ["Concepts as labeled REGIONS or TERRITORIES (like a political map)",
         "Related concepts share BORDERS (adjacency = relationship)",
         "Region SIZE proportional to importance or scope",
         "Color-coded by category or type (like biomes on a map)",
         "LARGE, readable labels INSIDE each region (minimum 16pt)",
         "Clear region boundaries with good contrast",
         "NO arrows - relationships shown purely through PROXIMITY and BORDERS"],
        ["Arrows or directional indicators", "Nodes and edges", "Flowchart elements", "3D terrain or topographic features",
         "Photorealistic landscape imagery", "Small text or labels outside regions"],
        "Like a flat political map or a board game territory map (Risk, Catan) - abstract regions, not realistic terrain",
        "Colored regions sharing borders, with large labels inside each region",
        source="v1",
        pass_if=["flat colored regions", "labels inside regions", "shared borders"],
        fail_if=["realistic terrain", "3D", "arrows", "photograph"]),
    "conceptual_layers": _entry(
        "Layered Depth Diagram", "layers", "4:3",
        ["Horizontal LAYERS or STRATA (like geological layers or architectural floors)",
         "Abstract concepts on TOP layers, concrete details on BOTTOM layers",
         "Each layer clearly labeled with LARGE text (minimum 16pt)",
         "Items within each layer as labeled boxes or regions",
         "Visual hierarchy through layer position (top = abstract, bottom = concrete)",
         "Color gradient from top to bottom showing abstraction level",
         "NO arrows between layers - relationship is CONTAINMENT/DERIVATION"],
        ["Arrows pointing between layers", "Network-style connections", "Realistic geological or architectural imagery",
         "3D perspective views", "Small or hard-to-read text"],
        "Like an OSI network model diagram or architectural floor plan - clean horizontal bands with content inside",
        "Horizontal stacked layers, abstract at top, concrete at bottom, large labels inside",
        source="v1",
        pass_if=["horizontal stacked bands", "labels inside each band", "items inside layers"],
        fail_if=["realistic geology", "3D perspective", "network edges", "photograph"]),
    "venn_diagram": _entry(
        "Conceptual Venn/Euler Diagram", "sets", "4:3",
        ["Overlapping circles or ellipses representing concept sets",
         "LARGE labels for each set (minimum 16pt, placed clearly)",
         "Overlap regions showing shared properties or intersections",
         "Labels in overlap regions explaining what concepts share",
         "Color-coded circles with transparency in overlaps",
         "Clean background for maximum readability",
         "2-4 overlapping sets maximum (more becomes unreadable)"],
        ["Arrows or directional indicators", "More than 4 overlapping sets", "Network nodes and edges",
         "Complex nested structures", "Small text or cluttered labels", "Artistic decorations"],
        "Like a classic Venn diagram but with rich colors and clear typography",
        "2-4 colored circles overlapping, with labels in each region including intersections",
        source="v1",
        pass_if=["overlapping circles", "labels in each circle", "labels in the overlap regions"],
        fail_if=["arrows", "network", "physical objects", "more than 4 circles"]),
    "constellation_map": _entry(
        "Constellation/Star Map", "network", "16:9",
        ["Concepts as STARS on a dark background", "Star BRIGHTNESS/SIZE proportional to importance",
         "Related stars grouped into CONSTELLATIONS with connecting lines",
         "Each star and constellation LABELED clearly (light text on dark, minimum 14pt)",
         "Subtle connecting lines within constellations (not arrows)",
         "Spatial clustering - related concepts are NEAR each other", "Professional astronomical chart aesthetic"],
        ["Directional arrows", "Flowchart elements", "Realistic space photography", "Complex network webs",
         "Small unreadable labels", "Cluttered or busy backgrounds"],
        "Like a star chart or constellation map - elegant, clean, with clear labels",
        "Stars of varying brightness on dark background, grouped into labeled constellations",
        source="v1",
        pass_if=["dark background", "labeled points grouped by lines", "clusters"],
        fail_if=["space photograph", "planets", "arrows", "flowchart"]),
    "weight_mass": _entry(
        "Visual Weight/Mass Diagram", "regions", "4:3",
        ["Concepts as shapes where SIZE = IMPORTANCE/WEIGHT",
         "Larger shapes for more important or foundational concepts",
         "Smaller shapes for derived or secondary concepts",
         "Shapes arranged so larger/foundational are at BOTTOM or CENTER",
         "Each shape LABELED clearly inside (minimum 14pt)", "Color-coding by category",
         "Clean, uncluttered layout with clear visual hierarchy", "NO arrows - relationships shown through SIZE and POSITION"],
        ["Arrows or connection lines", "Network edges", "Uniform sizing (defeats the purpose)",
         "Small text or external labels", "Realistic physical objects", "3D rendering or perspective"],
        "Like a bubble chart or weighted word cloud - size communicates importance",
        "Shapes of varying sizes, larger = more important, with labels inside",
        source="v1",
        pass_if=["shapes of clearly different sizes", "labels inside shapes"],
        fail_if=["arrows", "uniform sizes", "physical objects", "3D"]),
    "radial_hierarchy": _entry(
        "Radial/Mandala Hierarchy", "concentric", "1:1",
        ["CORE concept at the CENTER (largest, most prominent)", "Related concepts in RINGS radiating outward",
         "Inner rings = more fundamental, outer rings = more derived", "Each concept labeled clearly (minimum 14pt)",
         "Color-coding by ring or category", "Symmetrical or balanced layout",
         "NO arrows - relationship shown by DISTANCE from center"],
        ["Directional arrows", "Asymmetric or lopsided layouts", "Network-style edges between non-adjacent rings",
         "Small or cramped text", "More than 4-5 rings (becomes unreadable)", "Realistic mandala decorations"],
        "Like a radar chart or organizational wheel - center = core, rings = layers of detail",
        "Concentric rings with core concept at center, concepts placed in rings by derivation level",
        source="v1",
        pass_if=["concentric rings", "label at the center", "labels inside rings"],
        fail_if=["arrows", "network web", "decorative mandala", "physical objects"]),
    "spectrum_gradient": _entry(
        "Spectrum/Gradient Positioning", "spectrum", "16:9",
        ["Concepts positioned along a SPECTRUM or CONTINUUM",
         "Clear axis labels showing what the spectrum represents (e.g., abstract↔concrete, theory↔practice)",
         "Concepts as labeled boxes or circles placed along the spectrum", "LARGE readable labels (minimum 14pt)",
         "Color gradient background showing the continuum", "Can be horizontal OR vertical orientation",
         "NO arrows - position on spectrum shows the relationship"],
        ["Arrows or flow indicators", "Network connections", "Multiple axes (becomes a matrix, different format)",
         "Small or cramped labels", "Realistic imagery"],
        "Like a political spectrum chart or pH scale - concepts positioned by their property value",
        "Gradient background with labeled concepts placed along a continuum",
        source="v1",
        pass_if=["one gradient bar or axis", "labels placed along it", "end labels"],
        fail_if=["two axes", "network", "arrows", "physical objects"]),
    "containment_nesting": _entry(
        "Containment/Nesting Diagram", "tree", "4:3",
        ["Concepts as NESTED containers (outer contains inner)", "Larger outer containers for broader/foundational concepts",
         "Smaller inner elements for specific/derived concepts", "Each container clearly labeled (minimum 14pt)",
         "Color-coding to distinguish nesting levels", "Clean boundaries between containers",
         "NO arrows - relationship is CONTAINMENT (inside = derived from)"],
        ["Arrows or connection lines", "Network edges", "Physical container imagery (boxes, packages)",
         "More than 3-4 nesting levels (becomes unreadable)", "Small text or labels outside containers", "3D perspective"],
        "Like nested rectangles or Russian nesting dolls diagram - abstract, flat, clear labels",
        "Nested shapes showing containment hierarchy, largest = most general",
        source="v1",
        pass_if=["nested flat shapes", "labels on every level"],
        fail_if=["arrows", "physical boxes", "3D", "network"]),

    # ----- analyzer v1 VISUAL_FORMAT_INSTRUCTIONS that are diagrams -----
    "concentric_circles": _entry(
        "Concentric Circles (Core to Periphery)", "concentric", "1:1",
        ["Draw 2-3 CONCENTRIC CIRCLES (like a target/bullseye)", "INNER CIRCLE: the most central items (max 3-4)",
         "MIDDLE RING: secondary items (max 5-6)", "OUTER RING: peripheral items (max 6-8)",
         "Labels radiate outward from the center; every label readable (minimum 14pt)",
         "Warm colors at the core, cool colors at the edges"],
        ["Connection lines between items", "Network layout - this is NOT a network diagram", "Arrows", _NO_META],
        "Like a target diagram or a core/periphery map",
        "Bullseye rings with labeled items placed by centrality",
        source="v1-palette",
        pass_if=["concentric rings", "items placed in rings", "center label"],
        fail_if=["network edges", "arrows", "physical objects"]),
    "linear_flowchart": _entry(
        "Vertical Cascade Flowchart", "steps", "3:4",
        ["VERTICAL FLOW from TOP to BOTTOM only", "ONE source item at the very top", "Arrows pointing DOWN to the next level",
         "Maximum 3 LEVELS of depth beyond the source; each level 1-4 labeled boxes", "Each step in its own labeled box",
         _RICH.replace("elements", "boxes")],
        ["Circular layouts", "Side-to-side flow", "Network webs", "Timeline axis", _NO_META],
        "Like a cascade/waterfall of consequences on a consulting slide",
        "A top box cascading downward through arrows to labeled boxes",
        source="v1-palette",
        pass_if=["top-to-bottom flow", "boxes connected by downward arrows"],
        fail_if=["horizontal timeline", "network web", "physical objects"]),
    "two_column_split": _entry(
        "Two-Column Split", "columns", "16:9",
        ["A VERTICAL LINE or WALL down the center", "LEFT SIDE: one set of items under a large header",
         "RIGHT SIDE: the opposing set under a large header", "NO connections between the sides",
         "The divide is PROMINENT and CLEAR", "Contrasting colors: e.g. blue territory vs orange territory", _LARGE],
        ["Arrows or lines between the sides", "Network layout", "Timeline", "Physical wall imagery, bricks, fences", _NO_META],
        "Like a versus slide: two clearly separated territories",
        "Two labeled halves separated by a strong vertical divider",
        source="v1-palette",
        pass_if=["two labeled halves", "strong vertical divider", "items listed on each side"],
        fail_if=["physical wall", "bridge", "network", "photograph"]),
    "comparison_boxes": _entry(
        "Comparison Boxes", "columns", "16:9",
        ["2-4 distinct BOXES side by side (like a product comparison)", "Each box has a clear TITLE/HEADER",
         "Inside each box: a BULLETED LIST of 3-6 items", "Boxes are EQUAL SIZE with clear spacing", _LARGE],
        ["Network diagrams", "Connections between items inside boxes", "Physical boxes, packages or 3D containers", _NO_META],
        "Like a pricing-tier comparison or a side-by-side spec sheet",
        "Equal labeled panels side by side, each with a short list",
        source="v1-palette",
        pass_if=["side-by-side panels with headers", "lists inside panels"],
        fail_if=["3D boxes", "packages", "network", "photograph"]),
    "quadrant_chart": _entry(
        "2x2 Quadrant Chart", "quadrant", "1:1",
        ["A 2x2 GRID with clear dividing lines", "Both axes labeled with their low and high ends",
         "Each quadrant labeled with its name", "Items placed INSIDE their quadrants as labeled points or circles",
         "Consistent color coding (e.g. green for positive, red for negative) where the data gives categories", _LARGE],
        ["Network graphs", "Flow diagrams", "Timeline layouts", "Radial charts", "Tree structures", "More than 12 items", _NO_META],
        "Like a classic strategy 2x2 (power/interest, impact/effort) - think scatter plot on a strategic grid",
        "Four labeled quadrants with labeled axes and placed items",
        source="v1-palette",
        pass_if=["2x2 grid", "labeled axes", "quadrant labels", "labeled points inside quadrants"],
        fail_if=["network", "timeline", "physical objects", "no axes"]),
    "river_tributaries": _entry(
        "Tributaries Converging (Many-to-One Flow)", "flows", "4:3",
        ["Multiple SOURCES at the TOP (like tributaries)", "Streams FLOW DOWNWARD and MERGE",
         "The main stream/conclusion at the BOTTOM", "Flowing curved bands, not angular arrows",
         "Each tributary labeled with its source; band width = contribution", "Color code the source types"],
        ["Realistic river or water scenery, landscapes", "Network web", "Timeline", _NO_META],
        "Like a schematic river-basin diagram: abstract bands merging into one",
        "Labeled bands converging downward into one labeled band",
        source="v1-palette",
        pass_if=["several bands merging into one", "labels on each band"],
        fail_if=["realistic river", "landscape", "network", "photograph"]),
    "ledger_before_after": _entry(
        "Before/After Ledger", "before_after", "16:9",
        ["TWO COLUMNS: Before | After (or Action | Consequences)", "ACCOUNTING STYLE with +/- entries",
         "Clear debit/credit visual language", "Green for gains, red for losses",
         "The central action/move prominently displayed between the columns", _LARGE],
        ["Balance-scale imagery, coins, physical ledgers or books", "Network", "Timeline", _NO_META],
        "Like a clean two-column accounting statement",
        "Two labeled columns of +/- entries with the move in the middle",
        source="v1-palette",
        pass_if=["two columns", "plus/minus entries", "central move label"],
        fail_if=["physical scale", "coins", "book", "photograph"]),
    "delta_transform": _entry(
        "Before | Operator | After Transformation", "before_after", "16:9",
        ["THREE-PART horizontal layout: BEFORE | OPERATOR | AFTER", "LEFT: the state before the move as labeled items",
         "CENTER: the MOVE/ACTION prominently displayed", "RIGHT: the state after the move as labeled items",
         "Arrows or +/- marks showing what was added (green) and removed (red)", _LARGE],
        ["Two unrelated snapshots without the operator", "Network", "Timeline", _NO_META],
        "Like a state-transition slide: before, the operation, after",
        "Three labeled panels left-to-right with the change marked",
        source="v1-palette",
        pass_if=["three-part left-to-right layout", "central operator label", "before and after lists"],
        fail_if=["network", "physical objects", "photograph"]),
    "radiating_exposure": _entry(
        "Radiating Hub (Center and Spokes)", "hub", "1:1",
        ["A CENTRAL node (the commitment/claim/actor)", "RAYS/SPOKES extending outward to 3-8 labeled consequences",
         "Simultaneous multi-directional layout (NOT sequential)", "Different colors for different kinds of spoke where given",
         "Fan or starburst pattern; every label readable (minimum 14pt)"],
        ["Sequential chain A→B→C", "Network web with cross-links", "Spotlight, sun, explosion or burst imagery", _NO_META],
        "Like a hub-and-spoke diagram or a mind map with one level",
        "One labeled center with labeled spokes radiating outward",
        source="v1-palette",
        pass_if=["central label", "spokes to labeled items"],
        fail_if=["sun", "explosion", "chain", "photograph"]),
    "forced_fork": _entry(
        "Y-Fork Decision Diagram", "tree", "4:3",
        ["ONE path that SPLITS into two (or three) diverging labeled paths", "Visual emphasis on the SPLIT POINT",
         "Each path labeled with what lies down that road (2-4 labeled items each)", "No links between paths after the fork",
         "Clean geometric fork; every label readable (minimum 14pt)"],
        ["Abyss, cliff, wall, void or road scenery", "Network", "Timeline", _NO_META],
        "Like a decision-tree schematic with one juncture",
        "A trunk splitting into labeled branches at one marked point",
        source="v1-palette",
        pass_if=["one split point", "labeled branches"],
        fail_if=["road scenery", "cliff", "network", "photograph"]),

    # ----- v2 catalog: relational / network -----
    "chord_diagram": _entry(
        "Chord Diagram", "flows", "1:1",
        ["A circle divided into labeled arcs, one per entity", "Ribbons (chords) connecting arcs that exchange with each other",
         "Chord thickness proportional to the flow magnitude", "Each entity a distinct color", _LARGE],
        ["Network with nodes floating in space", "Pie chart", "Timeline", _NO_META],
        "Like a D3 chord diagram of bilateral trade flows",
        "A ring of labeled arcs joined by ribbons across the circle",
        pass_if=["circular ring of arcs", "ribbons across the circle", "labels on arcs"],
        fail_if=["pie chart", "network nodes", "physical objects"]),
    "hierarchical_tree": _entry(
        "Hierarchical Tree", "tree", "4:3",
        ["The ROOT at the top", "Levels of labeled boxes below, connected by straight lines to their parent",
         "Consistent spacing per level; siblings aligned", "Color code by level or by branch", _LARGE],
        ["Network web with cross-links", "Radial layout", "Timeline", "Realistic tree imagery with trunk and leaves", _NO_META],
        "Like an org chart or a taxonomy diagram",
        "Labeled boxes in levels joined by lines to a top root",
        pass_if=["root at top", "levels of boxes connected by lines"],
        fail_if=["realistic tree", "network web", "physical objects"]),
    "radial_tree": _entry(
        "Radial Tree", "hub", "1:1",
        ["The CENTER concept in the middle", "Branches extending outward to labeled related concepts",
         "Second-level items beyond their first-level parent where given", "Branch thickness = importance where given", _LARGE],
        ["Sun, flower, explosion or wheel imagery", "Rectangular org chart", "Timeline", _NO_META],
        "Like a mind map with a central node and radiating branches",
        "Center label with labeled branches radiating outward",
        pass_if=["central label", "branches radiating outward", "labels at branch ends"],
        fail_if=["sun", "flower", "photograph", "physical objects"]),
    "force_directed": _entry(
        "Force-Directed Network", "network", "4:3",
        ["Nodes as labeled circles; edges as lines", "Related nodes clustered together spatially; communities visible",
         "Node size = importance where given; color = group", "Edge labels naming the relationship where given", _LARGE],
        ["Timeline", "Tree hierarchy", "Sankey ribbons", _NO_DRAMA, _NO_META],
        "Like a D3 force-directed community graph",
        "Clusters of labeled nodes joined by lines",
        pass_if=["nodes connected by lines", "clusters", "labels on nodes"],
        fail_if=["timeline", "physical objects", "scenery"]),

    # ----- v2 catalog: flow / process -----
    "alluvial_diagram": _entry(
        "Alluvial Diagram", "flows", "16:9",
        ["Vertical labeled stages left-to-right", "Entities as bands that move between categories across stages",
         "Band width proportional to magnitude", "Each band colored by its origin", _LARGE],
        ["Network web", "Timeline", "Realistic river imagery", _NO_META],
        "Like an alluvial plot of how entities change category over time",
        "Bands flowing between labeled stage columns",
        pass_if=["stage columns", "bands flowing between them", "labels on stages and bands"],
        fail_if=["river scenery", "network", "photograph"]),
    "process_flow": _entry(
        "Process Flow (Inputs → Stages → Outputs)", "steps", "16:9",
        ["Stages as labeled boxes in one direction", "Inputs entering each stage and outputs leaving it, labeled where given",
         "Arrows between stages", "Color code stages", _LARGE],
        ["Network web", "Radial layout", "Machinery, pipes, factory imagery", _NO_META],
        "Like a clean process diagram on an operations slide",
        "Labeled stage boxes with labeled inputs/outputs and arrows",
        pass_if=["labeled stages with arrows", "inputs/outputs labeled"],
        fail_if=["machinery", "factory scene", "network", "photograph"]),
    "value_stream_map": _entry(
        "Value Stream Map", "steps", "16:9",
        ["Steps as labeled boxes left-to-right", "Under each step: its time / wait / note labels where given",
         "Bottleneck step highlighted in a warning color", "Arrows between steps", _LARGE],
        ["Network web", "Radial layout", "Factory or conveyor imagery", _NO_META],
        "Like a lean value-stream map",
        "A line of labeled step boxes with annotations beneath and a highlighted bottleneck",
        pass_if=["labeled step boxes in a line", "annotations under steps"],
        fail_if=["conveyor", "factory", "network", "photograph"]),

    # ----- v2 catalog: temporal -----
    "gantt_chart": _entry(
        "Gantt Chart", "gantt", "16:9",
        ["Tasks as labeled rows", "Horizontal bars spanning start to end along a labeled time axis",
         "Dependencies as arrows between bars where given", "Color code by group where given", _LARGE],
        ["Network", "Radial layout", "Calendar pages, clocks or hourglass imagery", _NO_META],
        "Like a project schedule Gantt chart",
        "Labeled rows of horizontal bars along a time axis",
        pass_if=["horizontal bars", "task labels", "time axis"],
        fail_if=["calendar imagery", "clock", "network", "photograph"]),
    "parallel_timelines": _entry(
        "Parallel Timelines", "events", "16:9",
        ["2-4 horizontal tracks, each labeled on the left", "A shared time axis across all tracks",
         "Events on each track at their dates, labeled", "Synchronous events aligned vertically", _LARGE],
        ["Network", "Radial layout", "Scene illustrations of the period", _NO_META],
        "Like a synchronoptic history chart",
        "Stacked labeled tracks sharing one time axis with dated labeled events",
        pass_if=["several horizontal tracks", "shared time axis", "dated labeled events"],
        fail_if=["scene illustration", "network", "photograph"]),
    "cycle_diagram": _entry(
        "Cycle Diagram", "cycle", "1:1",
        ["4-8 labeled phases arranged in a CIRCLE", "Curved arrows from each phase to the next, returning to the first",
         "Each phase in its own colored segment or node", "Phase duration or note under the label where given", _LARGE],
        ["A straight-line sequence", "Network web", "Wheel, gear, clock or ouroboros imagery", _NO_META],
        "Like a clean cycle diagram on a strategy slide",
        "Labeled phases around a circle joined by curved arrows",
        pass_if=["phases in a circle", "arrows around the circle", "labels on phases"],
        fail_if=["gear", "clock", "snake", "photograph", "straight line"]),
    "sparklines": _entry(
        "Sparkline Grid", "bars", "16:9",
        ["Small labeled trend lines, one per entity, in a grid", "Peaks and troughs marked", "Consistent scale per row", _LARGE],
        ["One large chart", "Network", _NO_META],
        "Like a dashboard of small multiples",
        "A grid of small labeled trend lines",
        pass_if=["several small trend lines", "labels"],
        fail_if=["physical objects", "photograph"]),

    # ----- v2 catalog: comparative -----
    "radar_chart": _entry(
        "Radar / Spider Chart", "radar", "1:1",
        ["3-8 labeled axes radiating from the center", "Each entity as a colored polygon over the axes",
         "A legend naming each polygon's entity", "Axis labels large and readable"],
        ["Network", "Pie chart", "Web, spider or target imagery", _NO_META],
        "Like a clean spider chart comparing profiles",
        "Labeled axes with overlapping colored polygons",
        pass_if=["radiating axes", "polygons", "axis labels"],
        fail_if=["spider web imagery", "photograph", "physical objects"]),
    "bar_chart": _entry(
        "Bar Chart", "bars", "16:9",
        ["Horizontal bars, one per labeled category, sorted by value", "A value label at the end of each bar",
         "One accent color for the emphasized bar where given", "An axis label stating the measure", _LARGE],
        ["3D bars", "Pictograms replacing bars", "Network", _NO_META],
        "Like a clean ranked bar chart in a broadsheet",
        "Labeled horizontal bars with value labels",
        pass_if=["bars", "category labels", "value labels"],
        fail_if=["3D bars", "pictograms", "photograph"]),
    "grouped_bar_chart": _entry(
        "Grouped Bar Chart", "matrix", "16:9",
        ["Categories along one axis; a cluster of bars per category, one per group", "A legend naming the groups",
         "Value labels on bars", _LARGE],
        ["3D bars", "Stacked bars", "Network", _NO_META],
        "Like a clustered bar comparison",
        "Clusters of colored bars per labeled category",
        pass_if=["clusters of bars", "legend", "category labels"],
        fail_if=["3D", "photograph", "physical objects"]),
    "dot_plot": _entry(
        "Dot Plot", "bars", "16:9",
        ["Labeled categories as rows", "Each item as a dot positioned along a shared value axis", "Dot labels where given", _LARGE],
        ["Bars", "Network", _NO_META],
        "Like a Cleveland dot plot",
        "Labeled rows with dots on a shared axis",
        pass_if=["dots on an axis", "row labels"],
        fail_if=["photograph", "physical objects"]),

    # ----- v2 catalog: part-of-whole -----
    "sunburst": _entry(
        "Sunburst", "tree", "1:1",
        ["The ROOT at the center", "Concentric rings of labeled arcs, one ring per hierarchy level",
         "Arc size proportional to value where given", "Color by top-level branch", _LARGE],
        ["Sun or flower imagery", "Pie chart with one ring only", "Network", _NO_META],
        "Like a sunburst hierarchy chart",
        "Concentric rings of labeled arcs around a root",
        pass_if=["concentric rings of arcs", "root at center", "labels on arcs"],
        fail_if=["sun imagery", "flower", "photograph"]),
    "stacked_bar": _entry(
        "Stacked Bar", "matrix", "16:9",
        ["One bar per labeled category", "Segments within each bar for the components, colored consistently",
         "A legend naming the components", "Segment value labels where given", _LARGE],
        ["3D bars", "Network", _NO_META],
        "Like a composition chart",
        "Labeled bars divided into colored segments",
        pass_if=["bars divided into segments", "legend", "category labels"],
        fail_if=["3D", "photograph", "physical objects"]),
    "waterfall_chart": _entry(
        "Waterfall Chart", "waterfall", "16:9",
        ["A starting bar on the left and an ending bar on the right", "Floating bars in between for each labeled change",
         "Increases in one color, decreases in another", "Value labels on every bar", _LARGE],
        ["Waterfall scenery or water", "Network", _NO_META],
        "Like a finance bridge/waterfall chart",
        "Start bar, floating change bars, end bar",
        pass_if=["start and end bars", "floating change bars", "labels"],
        fail_if=["water", "scenery", "photograph"]),
    "marimekko": _entry(
        "Marimekko Chart", "matrix", "16:9",
        ["Variable-width columns, one per labeled category", "Each column split into labeled segments",
         "A legend naming the segments", _LARGE],
        ["3D", "Network", _NO_META],
        "Like a mosaic/Marimekko chart",
        "Variable-width columns of colored segments",
        pass_if=["variable-width columns", "segments", "labels"],
        fail_if=["3D", "photograph", "physical objects"]),

    # ----- v2 catalog: spatial / set -----
    "euler_diagram": _entry(
        "Euler Diagram", "sets", "4:3",
        ["Labeled circles or ellipses for each set", "Only the overlaps that actually exist are drawn; disjoint sets do not touch",
         "Labels in the overlap regions where given", "Transparent fills so overlaps read clearly", _LARGE],
        ["Forced overlap of every pair", "Arrows", "Network", _NO_META],
        "Like a set diagram with accurate overlaps",
        "Labeled circles with only the true overlaps",
        pass_if=["labeled circles", "overlap labels where present"],
        fail_if=["arrows", "network", "physical objects"]),
    "positioning_map": _entry(
        "Positioning Map", "quadrant", "1:1",
        ["Two labeled axes, each with low and high ends", "Items as labeled points placed by their position",
         "Optional labeled zones/quadrants", "Color by group where given", _LARGE],
        ["Network", "Timeline", "Map of real geography", _NO_META],
        "Like a perceptual/competitive positioning map",
        "Labeled points on two labeled axes",
        pass_if=["two labeled axes", "labeled points"],
        fail_if=["geographic map", "network", "photograph"]),
    "bubble_chart": _entry(
        "Bubble Chart", "quadrant", "4:3",
        ["Two labeled axes", "Items as labeled circles placed by position", "Circle size = the third dimension, stated in a legend",
         "Color by group where given", _LARGE],
        ["Soap bubbles, balloons or spheres", "Network", _NO_META],
        "Like a clean bubble scatter",
        "Labeled circles of varying size on two axes",
        pass_if=["two axes", "circles of varying size", "labels"],
        fail_if=["balloons", "3D spheres", "photograph"]),

    # ----- v2 catalog: evidence / analytical -----
    "ach_matrix": _entry(
        "ACH Matrix (Competing Hypotheses)", "matrix", "16:9",
        ["Hypotheses as COLUMNS, evidence items as ROWS", "Cells colored: consistent (green), inconsistent (red), neutral (gray)",
         "A legend for the cell colors", "A short cell mark (C / I / N or +/−/0)", _LARGE],
        ["Network", "Flow", _NO_META],
        "Like an Analysis of Competing Hypotheses worksheet",
        "Evidence × hypotheses grid with color-coded cells",
        pass_if=["grid", "hypothesis column headers", "evidence row labels", "color-coded cells"],
        fail_if=["network", "photograph", "physical objects"]),
    "confidence_thermometer": _entry(
        "Confidence Scale", "spectrum", "3:4",
        ["A VERTICAL scale labeled at its ends (e.g. Remote → Almost Certain)", "Findings as labeled markers placed at their confidence level",
         "Graduations along the scale", _LARGE],
        ["A realistic glass thermometer, mercury, medical imagery", "Network", _NO_META],
        "Like an intelligence-community confidence scale",
        "A vertical labeled scale with labeled markers",
        pass_if=["vertical scale", "end labels", "labeled markers"],
        fail_if=["realistic thermometer", "medical", "photograph"]),
    "evidence_quality_matrix": _entry(
        "Evidence Quality Matrix", "matrix", "4:3",
        ["Source reliability as ROWS (A-F), information validity as COLUMNS (1-6) — or the grades the data gives",
         "Sources plotted as labeled cells or markers", "A legend", _LARGE],
        ["Network", "Flow", _NO_META],
        "Like the NATO Admiralty grading grid",
        "A graded grid with labeled sources placed in cells",
        pass_if=["graded grid", "labeled sources in cells"],
        fail_if=["network", "photograph", "physical objects"]),
    "indicator_dashboard": _entry(
        "Indicator Dashboard", "indicators", "16:9",
        ["One row or tile per labeled indicator", "A traffic-light status (green / amber / red) per indicator",
         "A trend arrow (up / flat / down) per indicator where given", "A legend for status colors", _LARGE],
        ["Realistic gauges, dials, cockpit imagery", "Network", _NO_META],
        "Like a clean status board",
        "Labeled rows/tiles with status colors and trend arrows",
        pass_if=["indicator labels", "status colors", "trend arrows"],
        fail_if=["gauges", "dials", "photograph"]),
    "gap_analysis": _entry(
        "Gap Analysis", "gap", "16:9",
        ["One labeled row per dimension", "Two markers or bars per row: current state and desired state, with a legend",
         "The gap between them highlighted and labeled where given", "Largest gaps emphasized", _LARGE],
        ["Chasm, canyon or bridge imagery", "Network", _NO_META],
        "Like a dumbbell/gap chart",
        "Labeled rows with current vs desired markers and highlighted gaps",
        pass_if=["rows with two markers", "legend", "labels"],
        fail_if=["canyon", "bridge", "photograph"]),

    # ----- v2 catalog: argumentative / logical -----
    "argument_tree": _entry(
        "Argument Tree", "argument", "4:3",
        ["The main CLAIM in a large box at the TOP", "PREMISES as labeled boxes in the row below, each linked upward to the claim",
         "EVIDENCE as smaller labeled boxes beneath the premise they support", "Rebuttals/objections in a contrasting color, linked to what they attack, where given",
         "Support links drawn as lines or arrows pointing UP toward the claim", _LARGE],
        ["Network web", "Timeline", "Scales of justice, pillars, foundations or building imagery", _NO_META],
        "Like an argument map (Rationale/Kialo style)",
        "Claim on top, premises below, evidence beneath, linked upward",
        pass_if=["claim box at top", "premise boxes below linked upward", "evidence boxes"],
        fail_if=["scales", "pillars", "network", "photograph"]),
    "toulmin_diagram": _entry(
        "Toulmin Diagram", "toulmin", "16:9",
        ["Six labeled components: GROUNDS → CLAIM across the top, WARRANT beneath the arrow, BACKING under the warrant, QUALIFIER at the claim, REBUTTAL branching off",
         "Each component box titled with its role AND filled with the text given", "Arrows showing grounds → claim and warrant supporting the arrow", _LARGE],
        ["Bridge or road imagery", "Network", _NO_META],
        "Like the textbook Toulmin model layout",
        "Grounds, claim, warrant, backing, qualifier, rebuttal boxes in the standard arrangement",
        pass_if=["labeled component boxes", "grounds to claim arrow", "warrant beneath"],
        fail_if=["bridge", "road", "photograph", "physical objects"]),
    "dialectical_map": _entry(
        "Dialectical Map", "dialectic", "16:9",
        ["THESIS in a box on the left and ANTITHESIS in a contrasting box on the right", "The named TENSIONS between them as labeled links across the middle",
         "SYNTHESIS in a box below (or above) the pair, drawn from both", "Arrows from thesis and antithesis into the synthesis", _LARGE],
        ["Tug-of-war, boxing, balance-scale or collision imagery", "Network web", _NO_DRAMA, _NO_META],
        "Like a clean thesis–antithesis–synthesis schema",
        "Two opposed labeled boxes, labeled tensions between, a synthesis box joined to both",
        pass_if=["thesis and antithesis boxes", "synthesis box", "labeled tensions"],
        fail_if=["tug of war", "scales", "collision", "photograph"]),
    "assumption_web": _entry(
        "Assumption Web", "tree", "4:3",
        ["CONCLUSIONS at the TOP", "Chains of labeled ASSUMPTIONS below, each linked to what depends on it",
         "Deeper (more hidden) assumptions lower down", "Dependency links as lines or arrows pointing up", _LARGE],
        ["Spider web imagery", "Archaeological dig scenery", "Network with no vertical order", _NO_META],
        "Like a dependency graph drawn top-down",
        "Top conclusions resting on descending chains of labeled assumptions",
        pass_if=["conclusions at top", "assumption boxes below", "links"],
        fail_if=["spider web", "excavation scene", "photograph"]),
    "scenario_cone": _entry(
        "Scenario Cone (Cone of Plausibility)", "scenarios", "16:9",
        ["The PRESENT as a labeled point on the left", "A cone widening to the right", "Branching labeled paths to 2-5 named futures at the cone's right edge",
         "Path thickness or shading = likelihood (with a small legend)", _LARGE],
        ["Traffic cone, ice-cream cone, funnel or trumpet imagery", "Network", _NO_META],
        "Like a futures-studies cone of plausibility",
        "A point on the left fanning into labeled future paths",
        pass_if=["present point", "fanning paths", "labeled futures"],
        fail_if=["funnel object", "cone object", "photograph"]),

    # ----- primitives' visual forms the catalog lacks -----
    "causal_loop_diagram": _entry(
        "Causal Loop Diagram", "cycle", "1:1",
        ["Variables as labeled nodes", "Curved arrows between variables showing causal influence",
         "Each arrow marked + (same direction) or − (opposite)", "Each loop marked R (reinforcing) or B (balancing) in its center",
         "Loops read as closed circuits; arrows curve back to their origin", _LARGE],
        ["A straight flowchart", "Gears, cogs, wheels, machinery", "Network without arrow polarity", _NO_META],
        "Like a system-dynamics causal loop diagram",
        "Labeled variables joined by curved polarity-marked arrows forming R/B loops",
        pass_if=["labeled nodes", "curved arrows forming loops", "+/- or R/B marks"],
        fail_if=["gears", "machinery", "straight flowchart", "photograph"]),
    "stock_flow_diagram": _entry(
        "Stock and Flow Diagram", "flows", "16:9",
        ["STOCKS as labeled rectangles", "FLOWS as double-line pipes with valve symbols between stocks",
         "Sources and sinks as cloud symbols", "Information links as thin arrows", _LARGE],
        ["Bathtubs, tanks, real pipes or plumbing scenery", "Network", _NO_META],
        "Like the standard system-dynamics stock-flow notation",
        "Rectangles joined by valve pipes, clouds at the ends",
        pass_if=["rectangles", "valve pipes", "labels"],
        fail_if=["bathtub", "plumbing scene", "photograph"]),
    "semiotic_square": _entry(
        "Semiotic Square", "square", "1:1",
        ["FOUR labeled corners: S1 (top-left), S2 (top-right), not-S2 (bottom-left), not-S1 (bottom-right)",
         "Contrary relation as the top edge, contradictory relations as the diagonals, implication as the vertical edges",
         "Each relation type drawn in its own line style with a small legend", _LARGE],
        ["Network", "Quadrant scatter with axes", _NO_META],
        "Like Greimas's semiotic square as drawn in semiotics textbooks",
        "Four labeled corners joined by contrary, contradictory and implication lines",
        pass_if=["four labeled corners", "diagonal and edge lines"],
        fail_if=["axes with plotted points", "photograph", "physical objects"]),
    "force_field": _entry(
        "Force-Field Diagram", "force_field", "16:9",
        ["The CHANGE/status quo as a vertical bar in the center, labeled",
         "DRIVING forces as labeled arrows pushing from the left", "RESTRAINING forces as labeled arrows pushing from the right",
         "Arrow length or thickness = strength", "Two colors: driving vs restraining, with a legend", _LARGE],
        ["Tug-of-war, wrestlers, magnets or physical forces", "Network", _NO_DRAMA, _NO_META],
        "Like Lewin's force-field analysis diagram",
        "Labeled arrows from both sides pressing on a central labeled bar",
        pass_if=["central bar", "arrows from left and right", "labels on arrows"],
        fail_if=["tug of war", "magnets", "photograph"]),
    "path_branching_tree": _entry(
        "Path-Dependency Branching Tree", "tree", "16:9",
        ["Time flows LEFT to RIGHT (or top to bottom)", "Labeled JUNCTURES where paths split",
         "The path actually taken drawn solid and highlighted", "Foreclosed paths drawn faded/dashed and labeled",
         "Lock-in shown as the taken path thickening", _LARGE],
        ["Road, forest or trail scenery", "Network web", "Realistic tree with leaves", _NO_META],
        "Like a decision tree with the chosen branch highlighted",
        "A branching diagram with one highlighted taken path and faded foreclosed branches",
        pass_if=["branching junctures", "highlighted taken path", "faded branches"],
        fail_if=["road scenery", "forest", "photograph"]),
    "commitment_cascade": _entry(
        "Commitment Cascade", "steps", "3:4",
        ["The initial COMMITMENT in a box at the TOP", "Arrows DOWN to the labeled commitments it entails",
         "Further arrows down to what those entail (max 3 levels)", "Each level shaded deeper to show accumulation", _LARGE],
        ["Dominoes, avalanche, waterfall or cascade scenery", "Network web", _NO_META],
        "Like an entailment tree on a consulting slide",
        "A top box cascading through labeled entailments downward",
        pass_if=["top box", "downward arrows to labeled boxes", "levels"],
        fail_if=["dominoes", "waterfall", "network web", "photograph"]),
}

# Aliases: v1 keys, catalog synonyms and the primitives' visual_forms → canonical.
FORMAT_ALIASES: dict[str, str] = {
    "sankey": "sankey_diagram", "heatmap": "matrix_heatmap", "venn_conceptual": "venn_diagram", "venn": "venn_diagram",
    "quadrant_grid": "quadrant_chart", "quadrant": "quadrant_chart", "network": "network_graph",
    "waterfall": "waterfall_chart", "gantt": "gantt_chart", "alluvial": "alluvial_diagram", "value_stream": "value_stream_map",
    "gap_analysis_visual": "gap_analysis", "tree": "hierarchical_tree", "cycle": "cycle_diagram",
    # primitives.json visual_forms
    "feedback_spiral": "causal_loop_diagram", "backing_cascade": "argument_tree", "support_hierarchy": "argument_tree",
    "dialectical_spiral": "dialectical_map", "contradiction_network": "network_graph",
    "counterfactual_comparison": "parallel_timelines", "lock_in_diagram": "path_branching_tree",
    "decision_tree": "path_branching_tree", "entailment_network": "commitment_cascade",
    "package_deal_diagram": "containment_nesting", "inference_chain": "linear_flowchart",
    "payoff_matrix": "matrix", "game_tree": "path_branching_tree", "incentive_flow": "sankey_diagram",
    "strategic_landscape": "positioning_map", "assumption_archaeology": "conceptual_layers",
    "presupposition_layers": "conceptual_layers", "epistemic_depth_diagram": "conceptual_layers",
    "foundation_stack": "conceptual_layers", "evolution_diagram": "timeline", "genealogical_tree": "hierarchical_tree",
    "concept_drift_flow": "alluvial_diagram", "competitive_landscape": "positioning_map", "criteria_matrix": "matrix",
    "transformation_pipeline": "process_flow", "rhetorical_move_diagram": "flowchart", "appeal_structure": "hierarchical_tree",
    "persuasion_flow": "flowchart", "audience_mapping": "quadrant_chart", "influence_map": "network_graph",
    "citation_network": "network_graph", "relationship_diagram": "network_graph",
    # v1 metaphor formats → nearest diagram
    "bridge_diagram": "toulmin_diagram", "stress_fracture": "force_field", "reflexive_loop": "causal_loop_diagram",
    "parallax_view": "two_column_split", "inheritance_chain": "hierarchical_tree", "bundled_box": "containment_nesting",
    "horizon_fade": "scenario_cone",
}


def normalize_format_key(value: str) -> Optional[str]:
    """Canonical format key for a v1 key, catalog key, primitive visual form or free-text name; None if unknown."""
    if not value:
        return None
    key = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")
    if key in FORMAT_ENFORCEMENT:
        return key
    if key in FORMAT_ALIASES:
        return FORMAT_ALIASES[key]
    for suffix in ("_diagram", "_chart", "_map", "_graph"):
        if key + suffix in FORMAT_ENFORCEMENT:
            return key + suffix
        if key.endswith(suffix) and key[: -len(suffix)] in FORMAT_ENFORCEMENT:
            return key[: -len(suffix)]
    return None


def format_entry(format_key: str) -> dict[str, Any]:
    canon = normalize_format_key(format_key)
    if canon is None:
        raise KeyError(f"unknown visual format {format_key!r}")
    return FORMAT_ENFORCEMENT[canon]


def aspect_for(format_key: str, default: str = "16:9") -> str:
    canon = normalize_format_key(format_key)
    return FORMAT_ENFORCEMENT[canon]["aspect"] if canon else default


def format_family(format_key: str) -> str:
    return format_entry(format_key)["family"]


# ---------------------------------------------------------------------------
# The enforcement block — v1 get_format_enforcement_prompt (gemini_image.py:1434-1480)
# ---------------------------------------------------------------------------

def enforcement_block(format_key: str) -> str:
    """The MANDATORY FORMAT block: must_have / must_not / global prohibitions / legibility."""
    canon = normalize_format_key(format_key)
    if canon is None:
        return f"""
**MANDATORY VISUAL FORMAT**: {format_key}
You MUST create a {format_key} visualization. This is NOT optional.
DO NOT substitute any other format type.
"""
    e = FORMAT_ENFORCEMENT[canon]
    must_have = "\n".join(f"  ✓ {item}" for item in e["must_have"])
    must_not = "\n".join(f"  ✗ {item}" for item in e["must_not"])
    global_prohibitions = "\n".join(f"  ⛔ {item}" for item in GLOBAL_PROHIBITIONS)
    legibility = "\n".join(f"  ✓ {item}" for item in LEGIBILITY_RULES)
    return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║        ⚠️ MANDATORY FORMAT: {e['name'].upper()} ⚠️
╠══════════════════════════════════════════════════════════════════════════════╣
║  THIS IS A HARD REQUIREMENT. WRONG FORMAT = COMPLETE FAILURE.
╚══════════════════════════════════════════════════════════════════════════════╝

**WHAT YOU MUST CREATE**: {e['name']}
**VISUAL SIGNATURE**: {e['visual_signature']}
**REFERENCE STYLE**: {e['reference_style']}

**REQUIRED ELEMENTS (your visualization MUST have these):**
{must_have}

**ABSOLUTE PROHIBITIONS (if you do ANY of these, you have FAILED):**
{must_not}

**UNIVERSAL DATA VISUALIZATION RULES (NEVER violate these):**
{global_prohibitions}

╔══════════════════════════════════════════════════════════════════════════════╗
║        📖 TEXT LEGIBILITY IS NON-NEGOTIABLE 📖
╚══════════════════════════════════════════════════════════════════════════════╝

**ALL text in your visualization MUST be:**
{legibility}

**THE #1 FAILURE MODE is dramatic visuals that make text unreadable.**
If your topic mentions "tension", "stress", "fracture", "collision", "conflict" -
DO NOT visualize these concepts literally with dramatic imagery.
"""


def check_criteria(format_key: str) -> tuple[list[str], list[str]]:
    """(pass_if, fail_if) for the vision check — v1 FORMAT_VALIDATION_CRITERIA where it existed,
    otherwise derived from must_have / must_not."""
    e = format_entry(format_key)
    pass_if = list(e["pass_if"]) or [m for m in e["must_have"][:4]]
    fail_if = list(e["fail_if"]) or [m for m in e["must_not"][:4]]
    return pass_if, fail_if


# ---------------------------------------------------------------------------
# DATA SHAPES — one family per way of laying out labelled content.
# Each: template (what the planner must produce), validate(data) -> errors,
# render(data) -> prose for the prompt. Labels are collected generically.
# ---------------------------------------------------------------------------

MAX_LABEL_WORDS = 6
MAX_LABEL_CHARS = 48
_NON_LABEL_KEYS = {"anchor", "anchors", "note", "notes", "why", "quote", "source_ref", "weight", "size",
                   "x", "y", "position", "value", "delta", "likelihood", "polarity", "strength", "status",
                   "trend", "kind", "group", "stage", "track", "loop_type", "start", "end", "level"}
_SHORT_VALUE_KEYS = {"value", "delta", "start", "end", "date", "time", "wait", "group", "kind", "stage", "track"}


def _s(v: Any) -> str:
    return str(v).strip() if v is not None else ""


# Keys whose strings are the diagram's scaffolding (axis names, quadrant names, the measure,
# a legend) rather than content drawn from the material. They are rendered and checked like
# any label, but the grounding wall does not require them to appear in the material.
STRUCTURAL_KEYS = {"x_axis", "y_axis", "axis", "quadrants", "measure", "legend", "divider", "tracks", "loop_type"}


def _labels_of(obj: Any, key: Optional[str] = None, out: Optional[list[str]] = None,
               structural: bool = False, include_structural: bool = True) -> list[str]:
    """Every string a diagram must render: values under label-ish keys and bare strings in lists."""
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in _NON_LABEL_KEYS and not isinstance(v, (dict, list)):
                continue
            _labels_of(v, k, out, structural or k in STRUCTURAL_KEYS, include_structural)
    elif isinstance(obj, list):
        for v in obj:
            _labels_of(v, key, out, structural, include_structural)
    elif isinstance(obj, str):
        text = obj.strip()
        if text and (key not in _NON_LABEL_KEYS) and (include_structural or not structural):
            out.append(text)
    return out


def _dedupe(labels: list[str]) -> list[str]:
    seen, out = set(), []
    for lab in labels:
        k = lab.lower()
        if k not in seen:
            seen.add(k)
            out.append(lab)
    return out


def collect_labels(data: dict[str, Any]) -> list[str]:
    """All rendered strings (content + structural), deduped, in data order."""
    return _dedupe(_labels_of(data or {}))


def content_labels(data: dict[str, Any]) -> list[str]:
    """Rendered strings that must come from the material (structural scaffolding excluded)."""
    return _dedupe(_labels_of(data or {}, include_structural=False))


def _req_list(data: dict, key: str, lo: int, hi: int, errors: list[str]) -> list:
    items = data.get(key)
    if not isinstance(items, list) or not items:
        errors.append(f"data.{key} must be a non-empty list")
        return []
    if len(items) < lo:
        errors.append(f"data.{key} needs at least {lo} items (got {len(items)})")
    if len(items) > hi:
        errors.append(f"data.{key} must have at most {hi} items (got {len(items)})")
    return items


def _lab(item: Any, errors: list[str], where: str, key: str = "label") -> str:
    if isinstance(item, str):
        return item.strip()
    if isinstance(item, dict):
        v = _s(item.get(key))
        if not v:
            errors.append(f"{where}: missing '{key}'")
        return v
    errors.append(f"{where}: expected an object with '{key}'")
    return ""


def _axis(data: dict, key: str, errors: list[str]) -> dict:
    ax = data.get(key)
    if not isinstance(ax, dict) or not _s(ax.get("label")):
        errors.append(f"data.{key} must be {{label, low, high}}")
        return {}
    for end in ("low", "high"):
        if not _s(ax.get(end)):
            errors.append(f"data.{key}.{end} is required")
    return ax


def _num(v: Any, lo: float, hi: float) -> Optional[float]:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if lo <= f <= hi else None


# --- validators ---------------------------------------------------------

def _v_steps(d: dict, e: list[str]) -> None:
    steps = _req_list(d, "steps", 3, 10, e)
    labels = [_lab(s, e, f"data.steps[{i}]") for i, s in enumerate(steps)]
    for b in d.get("branches", []) or []:
        if not isinstance(b, dict) or not _s(b.get("from")) or not _s(b.get("to")) or not _s(b.get("label")):
            e.append("data.branches[] entries must be {from, label, to}")
        elif b["from"] not in labels or b["to"] not in labels:
            e.append(f"data.branches: '{b.get('from')}'→'{b.get('to')}' must reference step labels")


def _v_sets(d: dict, e: list[str]) -> None:
    sets = _req_list(d, "sets", 2, 4, e)
    names = [_lab(s, e, f"data.sets[{i}]") for i, s in enumerate(sets)]
    inter = d.get("intersections")
    if not isinstance(inter, list) or not inter:
        e.append("data.intersections must list at least one {of: [set labels], label}")
        return
    for i, x in enumerate(inter):
        if not isinstance(x, dict) or not isinstance(x.get("of"), list) or len(x["of"]) < 2 or not _s(x.get("label")):
            e.append(f"data.intersections[{i}] must be {{of: [>=2 set labels], label}}")
        elif any(o not in names for o in x["of"]):
            e.append(f"data.intersections[{i}].of must name sets from data.sets")


def _v_quadrant(d: dict, e: list[str]) -> None:
    _axis(d, "x_axis", e)
    _axis(d, "y_axis", e)
    items = _req_list(d, "items", 4, 10, e)
    for i, it in enumerate(items):
        _lab(it, e, f"data.items[{i}]")
        if isinstance(it, dict) and (_num(it.get("x"), 0, 1) is None or _num(it.get("y"), 0, 1) is None):
            e.append(f"data.items[{i}] needs x and y in 0..1")
    q = d.get("quadrants")
    if q is not None and (not isinstance(q, dict) or any(k not in ("top_left", "top_right", "bottom_left", "bottom_right") for k in q)):
        e.append("data.quadrants must map top_left/top_right/bottom_left/bottom_right to labels")


def _v_events(d: dict, e: list[str]) -> None:
    events = _req_list(d, "events", 3, 12, e)
    for i, ev in enumerate(events):
        _lab(ev, e, f"data.events[{i}]")
        if isinstance(ev, dict) and not _s(ev.get("date")):
            e.append(f"data.events[{i}] needs a 'date' (year, period or era)")
    tracks = d.get("tracks")
    if tracks is not None and (not isinstance(tracks, list) or not all(isinstance(t, str) and t.strip() for t in tracks)):
        e.append("data.tracks must be a list of track labels")


def _v_flows(d: dict, e: list[str]) -> None:
    flows = _req_list(d, "flows", 3, 16, e)
    for i, f in enumerate(flows):
        if not isinstance(f, dict) or not _s(f.get("source")) or not _s(f.get("target")):
            e.append(f"data.flows[{i}] must be {{source, target, weight 1-5, label?}}")
        elif _num(f.get("weight"), 1, 5) is None:
            e.append(f"data.flows[{i}].weight must be 1..5")


def _v_network(d: dict, e: list[str]) -> None:
    nodes = _req_list(d, "nodes", 4, 12, e)
    names = {_lab(n, e, f"data.nodes[{i}]") for i, n in enumerate(nodes)}
    edges = _req_list(d, "edges", 3, 18, e)
    for i, ed in enumerate(edges):
        if not isinstance(ed, dict) or not _s(ed.get("source")) or not _s(ed.get("target")):
            e.append(f"data.edges[{i}] must be {{source, target, label?}}")
        elif ed["source"] not in names or ed["target"] not in names:
            e.append(f"data.edges[{i}] endpoints must be node labels")


def _v_cycle(d: dict, e: list[str]) -> None:
    stages = _req_list(d, "stages", 3, 8, e)
    names = [_lab(s, e, f"data.stages[{i}]") for i, s in enumerate(stages)]
    for i, ln in enumerate(d.get("links", []) or []):
        if not isinstance(ln, dict) or ln.get("from") not in names or ln.get("to") not in names:
            e.append(f"data.links[{i}] must be {{from, to, polarity?}} over stage labels")


def _v_matrix(d: dict, e: list[str]) -> None:
    rows = _req_list(d, "rows", 2, 8, e)
    cols = _req_list(d, "columns", 2, 6, e)
    cells = d.get("cells")
    if not isinstance(cells, list) or len(cells) != len(rows):
        e.append("data.cells must have one list per row")
        return
    for i, r in enumerate(cells):
        if not isinstance(r, list) or len(r) != len(cols):
            e.append(f"data.cells[{i}] must have exactly {len(cols)} values")


def _walk_tree(node: Any, depth: int, count: list[int], e: list[str], where: str) -> None:
    if not isinstance(node, dict) or not _s(node.get("label")):
        e.append(f"{where}: tree nodes are {{label, children?: [...]}}")
        return
    count[0] += 1
    if depth > 3:
        e.append(f"{where}: deeper than 3 levels")
        return
    for i, c in enumerate(node.get("children", []) or []):
        _walk_tree(c, depth + 1, count, e, f"{where}.children[{i}]")


def _v_tree(d: dict, e: list[str]) -> None:
    root = d.get("root")
    if not isinstance(root, dict):
        e.append("data.root must be {label, children: [...]}")
        return
    count = [0]
    _walk_tree(root, 0, count, e, "data.root")
    if count[0] < 3:
        e.append("the tree needs at least 3 nodes")
    if count[0] > 16:
        e.append("the tree must have at most 16 nodes")


def _v_argument(d: dict, e: list[str]) -> None:
    if not _s(d.get("claim")):
        e.append("data.claim is required")
    prem = _req_list(d, "premises", 2, 5, e)
    for i, p in enumerate(prem):
        _lab(p, e, f"data.premises[{i}]")
        if isinstance(p, dict):
            ev = p.get("evidence", []) or []
            if not isinstance(ev, list) or len(ev) > 3:
                e.append(f"data.premises[{i}].evidence must be a list of at most 3 labels")


def _v_layers(d: dict, e: list[str]) -> None:
    layers = _req_list(d, "layers", 3, 6, e)
    for i, layer in enumerate(layers):
        _lab(layer, e, f"data.layers[{i}]")
        if isinstance(layer, dict):
            items = layer.get("items", []) or []
            if not isinstance(items, list) or len(items) > 5:
                e.append(f"data.layers[{i}].items must be a list of at most 5 labels")


def _v_columns(d: dict, e: list[str]) -> None:
    cols = _req_list(d, "columns", 2, 4, e)
    for i, c in enumerate(cols):
        _lab(c, e, f"data.columns[{i}]")
        if isinstance(c, dict):
            items = c.get("items")
            if not isinstance(items, list) or not (1 <= len(items) <= 6):
                e.append(f"data.columns[{i}].items must list 1-6 labels")


def _v_concentric(d: dict, e: list[str]) -> None:
    if not _s(d.get("center")):
        e.append("data.center is required")
    rings = _req_list(d, "rings", 2, 4, e)
    for i, r in enumerate(rings):
        _lab(r, e, f"data.rings[{i}]")
        if isinstance(r, dict):
            items = r.get("items")
            if not isinstance(items, list) or not (1 <= len(items) <= 8):
                e.append(f"data.rings[{i}].items must list 1-8 labels")


def _v_spectrum(d: dict, e: list[str]) -> None:
    _axis(d, "axis", e)
    items = _req_list(d, "items", 3, 10, e)
    for i, it in enumerate(items):
        _lab(it, e, f"data.items[{i}]")
        if isinstance(it, dict) and _num(it.get("position"), 0, 1) is None:
            e.append(f"data.items[{i}].position must be 0..1")


def _v_bars(d: dict, e: list[str]) -> None:
    cats = _req_list(d, "categories", 3, 10, e)
    for i, c in enumerate(cats):
        _lab(c, e, f"data.categories[{i}]")
        if isinstance(c, dict) and not re.search(r"\d", _s(c.get("value"))):
            e.append(f"data.categories[{i}].value must be a number as written in the source (with its unit); "
                     "for non-numeric comparisons use comparison_boxes, gap_analysis or matrix")
    if not _s(d.get("measure")):
        e.append("data.measure (what the bars measure) is required")


def _v_regions(d: dict, e: list[str]) -> None:
    regs = _req_list(d, "regions", 4, 12, e)
    for i, r in enumerate(regs):
        _lab(r, e, f"data.regions[{i}]")
        if isinstance(r, dict) and _num(r.get("size"), 1, 5) is None:
            e.append(f"data.regions[{i}].size must be 1..5")


def _v_radar(d: dict, e: list[str]) -> None:
    dims = _req_list(d, "dimensions", 3, 8, e)
    ents = _req_list(d, "entities", 1, 4, e)
    for i, en in enumerate(ents):
        _lab(en, e, f"data.entities[{i}]")
        if isinstance(en, dict):
            sc = en.get("scores")
            if not isinstance(sc, list) or len(sc) != len(dims) or any(_num(s, 0, 5) is None for s in sc):
                e.append(f"data.entities[{i}].scores must have one 0..5 value per dimension")


def _v_hub(d: dict, e: list[str]) -> None:
    if not _s(d.get("center")):
        e.append("data.center is required")
    spokes = _req_list(d, "spokes", 3, 8, e)
    for i, s in enumerate(spokes):
        _lab(s, e, f"data.spokes[{i}]")
        if isinstance(s, dict):
            ch = s.get("children", []) or []
            if not isinstance(ch, list) or len(ch) > 3:
                e.append(f"data.spokes[{i}].children must be at most 3 labels")


def _v_gantt(d: dict, e: list[str]) -> None:
    tasks = _req_list(d, "tasks", 3, 10, e)
    for i, t in enumerate(tasks):
        _lab(t, e, f"data.tasks[{i}]")
        if isinstance(t, dict) and (not _s(t.get("start")) or not _s(t.get("end"))):
            e.append(f"data.tasks[{i}] needs start and end")


def _v_waterfall(d: dict, e: list[str]) -> None:
    for k in ("start", "end"):
        v = d.get(k)
        if not isinstance(v, dict) or not _s(v.get("label")) or not _s(v.get("value")):
            e.append(f"data.{k} must be {{label, value}}")
    changes = _req_list(d, "changes", 2, 8, e)
    for i, c in enumerate(changes):
        _lab(c, e, f"data.changes[{i}]")
        if isinstance(c, dict) and not _s(c.get("delta")):
            e.append(f"data.changes[{i}].delta is required (e.g. '+300 jobs', '−€40m')")


def _v_indicators(d: dict, e: list[str]) -> None:
    inds = _req_list(d, "indicators", 3, 10, e)
    for i, it in enumerate(inds):
        _lab(it, e, f"data.indicators[{i}]")
        if isinstance(it, dict) and _s(it.get("status")).lower() not in ("green", "amber", "red"):
            e.append(f"data.indicators[{i}].status must be green|amber|red")


def _v_gap(d: dict, e: list[str]) -> None:
    dims = _req_list(d, "dimensions", 3, 8, e)
    for i, x in enumerate(dims):
        _lab(x, e, f"data.dimensions[{i}]")
        if isinstance(x, dict) and (not _s(x.get("current")) or not _s(x.get("desired"))):
            e.append(f"data.dimensions[{i}] needs current and desired")


def _v_before_after(d: dict, e: list[str]) -> None:
    for k in ("before", "after"):
        v = d.get(k)
        if not isinstance(v, dict) or not _s(v.get("label")) or not isinstance(v.get("items"), list) or not v["items"]:
            e.append(f"data.{k} must be {{label, items: [labels]}}")
    if not _s(d.get("move")):
        e.append("data.move (the action/operator between the columns) is required")


def _v_toulmin(d: dict, e: list[str]) -> None:
    for k in ("claim", "grounds", "warrant"):
        if not _s(d.get(k)):
            e.append(f"data.{k} is required")


def _v_dialectic(d: dict, e: list[str]) -> None:
    for k in ("thesis", "antithesis", "synthesis"):
        if not _s(d.get(k)):
            e.append(f"data.{k} is required")
    t = d.get("tensions")
    if not isinstance(t, list) or not (1 <= len(t) <= 5):
        e.append("data.tensions must list 1-5 labels")


def _v_square(d: dict, e: list[str]) -> None:
    for k in ("s1", "s2", "not_s1", "not_s2"):
        if not _s(d.get(k)):
            e.append(f"data.{k} is required")


def _v_force_field(d: dict, e: list[str]) -> None:
    if not _s(d.get("change")):
        e.append("data.change is required")
    for k in ("driving", "restraining"):
        items = _req_list(d, k, 2, 6, e)
        for i, it in enumerate(items):
            _lab(it, e, f"data.{k}[{i}]")
            if isinstance(it, dict) and _num(it.get("strength"), 1, 5) is None:
                e.append(f"data.{k}[{i}].strength must be 1..5")


def _v_scenarios(d: dict, e: list[str]) -> None:
    if not _s(d.get("present")):
        e.append("data.present is required")
    futs = _req_list(d, "futures", 2, 5, e)
    for i, f in enumerate(futs):
        _lab(f, e, f"data.futures[{i}]")
        if isinstance(f, dict) and _s(f.get("likelihood")).lower() not in ("high", "medium", "low"):
            e.append(f"data.futures[{i}].likelihood must be high|medium|low")


# --- renderers (data → prose the image model reads) ----------------------
# Magnitudes and positions are spelled out in WORDS: a number in the content block gets
# printed by the image model ("(0.12, 0.92)"), and display_config forbids raw scores.

_FIVE = ("very thin", "thin", "medium", "thick", "very thick")
_SIZE5 = ("very small", "small", "medium", "large", "very large")
_STRENGTH5 = ("very weak", "weak", "moderate", "strong", "very strong")


def _five(v: Any, words: tuple[str, ...]) -> str:
    try:
        i = int(round(float(v)))
    except (TypeError, ValueError):
        return words[2]
    return words[max(1, min(5, i)) - 1]


def _hpos(x: Any) -> str:
    f = float(x)
    return ("at the far left" if f < 0.2 else "left of centre" if f < 0.4 else "at the horizontal centre"
            if f <= 0.6 else "right of centre" if f <= 0.8 else "at the far right")


def _vpos(y: Any) -> str:
    f = float(y)
    return ("at the very bottom" if f < 0.2 else "in the lower half" if f < 0.4 else "at mid-height"
            if f <= 0.6 else "in the upper half" if f <= 0.8 else "at the very top")


def _apos(p: Any) -> str:
    f = float(p)
    return ("at the low end" if f < 0.15 else "near the low end" if f < 0.4 else "around the middle"
            if f <= 0.6 else "near the high end" if f <= 0.85 else "at the high end")

def _line_items(items: list, key: str = "label") -> str:
    return "; ".join(_lab(x, [], "", key) for x in items)


def _r_steps(d: dict) -> list[str]:
    out = []
    for i, s in enumerate(d["steps"], 1):
        label = _lab(s, [], "")
        extras = ""
        if isinstance(s, dict):
            bits = [f"{k}: {_s(s[k])}" for k in ("inputs", "outputs", "time", "wait") if s.get(k)]
            extras = f"  ({'; '.join(bits)})" if bits else ""
        out.append(f"  Step {i}: {label}{extras}")
    for b in d.get("branches", []) or []:
        out.append(f"  Branch: from '{b['from']}' — decision '{b['label']}' — to '{b['to']}'")
    if d.get("bottleneck"):
        out.append(f"  Bottleneck (highlight): {_s(d['bottleneck'])}")
    return out


def _r_sets(d: dict) -> list[str]:
    out = []
    for s in d["sets"]:
        label = _lab(s, [], "")
        items = s.get("items") if isinstance(s, dict) else None
        out.append(f"  Set: {label}" + (f" — inside only this set: {'; '.join(map(_s, items))}" if items else ""))
    for x in d["intersections"]:
        out.append(f"  Overlap of {' ∩ '.join(x['of'])}: {x['label']}")
    return out


def _r_quadrant(d: dict) -> list[str]:
    xa, ya = d["x_axis"], d["y_axis"]
    out = [f"  X axis: {xa['label']} (left = {xa['low']}, right = {xa['high']})",
           f"  Y axis: {ya['label']} (bottom = {ya['low']}, top = {ya['high']})"]
    q = d.get("quadrants") or {}
    for k in ("top_left", "top_right", "bottom_left", "bottom_right"):
        if q.get(k):
            out.append(f"  Quadrant {k.replace('_', '-')}: {q[k]}")
    for it in d["items"]:
        extra = f", drawn {_five(it['size'], _SIZE5)}" if it.get("size") else ""
        grp = f", group: {it['group']}" if it.get("group") else ""
        out.append(f"  Item: {it['label']} — placed {_hpos(it['x'])}, {_vpos(it['y'])}{extra}{grp}")
    out.append("  (placements are instructions for you; print NO coordinates or numbers next to items)")
    return out


def _r_events(d: dict) -> list[str]:
    out = []
    if d.get("tracks"):
        out.append(f"  Tracks (top to bottom): {'; '.join(d['tracks'])}")
    for ev in d["events"]:
        tr = f" [track: {ev['track']}]" if isinstance(ev, dict) and ev.get("track") else ""
        out.append(f"  {ev['date']} — {ev['label']}{tr}")
    return out


def _r_flows(d: dict) -> list[str]:
    out = []
    if d.get("nodes"):
        out.append("  Nodes: " + "; ".join(
            (_lab(n, [], "") + (f" [stage: {n['stage']}]" if isinstance(n, dict) and n.get("stage") else "")) for n in d["nodes"]))
    for f in d["flows"]:
        lab = f" ({f['label']})" if f.get("label") else ""
        out.append(f"  {f['source']} → {f['target']}: {_five(f['weight'], _FIVE)} band{lab}")
    return out


def _r_network(d: dict) -> list[str]:
    out = ["  Nodes: " + "; ".join(
        _lab(n, [], "") + (f" [group: {n['group']}]" if isinstance(n, dict) and n.get("group") else "")
        + (f" [{_five(n['size'], _SIZE5)} node]" if isinstance(n, dict) and n.get("size") else "") for n in d["nodes"])]
    for ed in d["edges"]:
        lab = f" — labelled '{ed['label']}'" if ed.get("label") else ""
        out.append(f"  Edge: {ed['source']} — {ed['target']}{lab}")
    return out


def _r_cycle(d: dict) -> list[str]:
    out = ["  Phases in order around the circle: " + " → ".join(_lab(s, [], "") for s in d["stages"]) + " → (back to the first)"]
    for ln in d.get("links", []) or []:
        pol = f" marked {ln['polarity']}" if ln.get("polarity") else ""
        out.append(f"  Arrow {ln['from']} → {ln['to']}{pol}")
    if d.get("loop_type"):
        out.append(f"  Loop type marked in the center: {d['loop_type']}")
    return out


def _r_matrix(d: dict) -> list[str]:
    out = [f"  Column headers (left to right): {' | '.join(map(_s, d['columns']))}"]
    for r, row in zip(d["rows"], d["cells"]):
        out.append(f"  Row '{_s(r)}': " + " | ".join(_s(c) for c in row))
    return out


def _r_tree_node(n: dict, depth: int, out: list[str]) -> None:
    flags = " ".join(([f"[{n['status']}]"] if n.get("status") else []) + ([f"[{_five(n['size'], _SIZE5)}]"] if n.get("size") else []))
    out.append(f"  {'    ' * depth}{'└ ' if depth else ''}{n['label']}{(' ' + flags) if flags else ''}")
    for c in n.get("children", []) or []:
        _r_tree_node(c, depth + 1, out)


def _r_tree(d: dict) -> list[str]:
    out: list[str] = []
    _r_tree_node(d["root"], 0, out)
    return out


def _r_argument(d: dict) -> list[str]:
    out = [f"  CLAIM (top): {d['claim']}"]
    for p in d["premises"]:
        out.append(f"  Premise: {p['label']}")
        for ev in p.get("evidence", []) or []:
            out.append(f"      evidence beneath it: {_s(ev)}")
        if p.get("rebuttal"):
            out.append(f"      rebuttal (contrasting color): {p['rebuttal']}")
    return out


def _r_layers(d: dict) -> list[str]:
    out = []
    for i, layer in enumerate(d["layers"], 1):
        items = layer.get("items") if isinstance(layer, dict) else None
        out.append(f"  Layer {i} (top{' to bottom' if i == 1 else ''}): {_lab(layer, [], '')}"
                   + (f" — items: {'; '.join(map(_s, items))}" if items else ""))
    return out


def _r_columns(d: dict) -> list[str]:
    out = []
    for c in d["columns"]:
        out.append(f"  Column '{c['label']}': " + "; ".join(map(_s, c["items"])))
    if d.get("divider"):
        out.append(f"  Divider label: {_s(d['divider'])}")
    return out


def _r_concentric(d: dict) -> list[str]:
    out = [f"  Center: {d['center']}"]
    for i, r in enumerate(d["rings"], 1):
        out.append(f"  Ring {i} ('{r['label']}'): " + "; ".join(map(_s, r["items"])))
    return out


def _r_spectrum(d: dict) -> list[str]:
    ax = d["axis"]
    out = [f"  Axis: {ax['label']} — from '{ax['low']}' (0) to '{ax['high']}' (1)"]
    for it in d["items"]:
        out.append(f"  {it['label']} — placed {_apos(it['position'])}")
    out.append("  (placements are instructions for you; print NO numbers next to items)")
    return out


def _r_bars(d: dict) -> list[str]:
    out = [f"  Measure: {d['measure']}"]
    for c in d["categories"]:
        out.append(f"  {c['label']}: {c['value']}")
    if d.get("emphasize"):
        out.append(f"  Emphasize: {_s(d['emphasize'])}")
    return out


def _r_regions(d: dict) -> list[str]:
    out = []
    for r in d["regions"]:
        grp = f", group {r['group']}" if r.get("group") else ""
        nb = f", borders: {'; '.join(map(_s, r['neighbors']))}" if r.get("neighbors") else ""
        out.append(f"  Region '{r['label']}' ({_five(r['size'], _SIZE5)}{grp}{nb})")
    return out


def _r_radar(d: dict) -> list[str]:
    out = [f"  Axes: {'; '.join(map(_s, d['dimensions']))}"]
    for en in d["entities"]:
        out.append(f"  {en['label']}: " + ", ".join(f"{_s(dim)}={s}" for dim, s in zip(d["dimensions"], en["scores"])))
    return out


def _r_hub(d: dict) -> list[str]:
    out = [f"  Center: {d['center']}"]
    for s in d["spokes"]:
        kind = f" [{s['kind']}]" if isinstance(s, dict) and s.get("kind") else ""
        out.append(f"  Spoke: {_lab(s, [], '')}{kind}")
        for c in (s.get("children", []) if isinstance(s, dict) else []) or []:
            out.append(f"      beyond it: {_s(c)}")
    return out


def _r_gantt(d: dict) -> list[str]:
    out = []
    for t in d["tasks"]:
        dep = f" (after: {t['after']})" if t.get("after") else ""
        out.append(f"  {t['label']}: {t['start']} → {t['end']}{dep}")
    return out


def _r_waterfall(d: dict) -> list[str]:
    out = [f"  Start bar: {d['start']['label']} = {d['start']['value']}"]
    for c in d["changes"]:
        out.append(f"  Change: {c['label']} {c['delta']}")
    out.append(f"  End bar: {d['end']['label']} = {d['end']['value']}")
    return out


def _r_indicators(d: dict) -> list[str]:
    return [f"  {it['label']}: status {it['status']}" + (f", trend {it['trend']}" if it.get("trend") else "")
            for it in d["indicators"]]


def _r_gap(d: dict) -> list[str]:
    return [f"  {x['label']}: current '{x['current']}' → desired '{x['desired']}'" + (f" (gap: {x['gap']})" if x.get("gap") else "")
            for x in d["dimensions"]]


def _r_before_after(d: dict) -> list[str]:
    return [f"  Left column '{d['before']['label']}': " + "; ".join(map(_s, d["before"]["items"])),
            f"  Center (the move): {d['move']}",
            f"  Right column '{d['after']['label']}': " + "; ".join(map(_s, d["after"]["items"]))]


def _r_toulmin(d: dict) -> list[str]:
    return [f"  {k.upper()}: {_s(d[k])}" for k in ("grounds", "claim", "warrant", "backing", "qualifier", "rebuttal") if d.get(k)]


def _r_dialectic(d: dict) -> list[str]:
    return [f"  THESIS (left): {d['thesis']}", f"  ANTITHESIS (right): {d['antithesis']}",
            "  TENSIONS (labelled links between them): " + "; ".join(map(_s, d["tensions"])),
            f"  SYNTHESIS (below, joined to both): {d['synthesis']}"]


def _r_square(d: dict) -> list[str]:
    return [f"  Top-left S1: {d['s1']}", f"  Top-right S2: {d['s2']}",
            f"  Bottom-left not-S2: {d['not_s2']}", f"  Bottom-right not-S1: {d['not_s1']}"]


def _r_force_field(d: dict) -> list[str]:
    out = [f"  Central bar (the change): {d['change']}"]
    out += [f"  Driving (from the left): {x['label']} — {_five(x['strength'], _STRENGTH5)} arrow" for x in d["driving"]]
    out += [f"  Restraining (from the right): {x['label']} — {_five(x['strength'], _STRENGTH5)} arrow" for x in d["restraining"]]
    return out


def _r_scenarios(d: dict) -> list[str]:
    out = [f"  Present (left point): {d['present']}"]
    for f in d["futures"]:
        path = f" via {f['path']}" if f.get("path") else ""
        out.append(f"  Future: {f['label']} — likelihood {f['likelihood']}{path}")
    return out


DATA_SHAPES: dict[str, dict[str, Any]] = {
    "steps": {"template": {"steps": [{"label": "…", "note?": "…"}], "branches?": [{"from": "step label", "label": "decision", "to": "step label"}]},
              "rule": "3-10 ordered steps; optional decision branches", "validate": _v_steps, "render": _r_steps},
    "sets": {"template": {"sets": [{"label": "…", "items?": ["…"]}], "intersections": [{"of": ["set A", "set B"], "label": "what they share"}]},
             "rule": "2-4 named sets, every drawn overlap labelled", "validate": _v_sets, "render": _r_sets},
    "quadrant": {"template": {"x_axis": {"label": "…", "low": "…", "high": "…"}, "y_axis": {"label": "…", "low": "…", "high": "…"},
                              "quadrants?": {"top_left": "…", "top_right": "…", "bottom_left": "…", "bottom_right": "…"},
                              "items": [{"label": "…", "x": 0.2, "y": 0.8, "group?": "…"}]},
                 "rule": "two labelled axes with ends; 4-10 placed items (x,y in 0..1)", "validate": _v_quadrant, "render": _r_quadrant},
    "events": {"template": {"events": [{"date": "1999 | 2015-2020 | 'era'", "label": "…", "track?": "…"}], "tracks?": ["…"]},
               "rule": "3-12 dated events in order; tracks for parallel timelines", "validate": _v_events, "render": _r_events},
    "flows": {"template": {"nodes?": [{"label": "…", "stage?": "…"}], "flows": [{"source": "…", "target": "…", "weight": 3, "label?": "…"}]},
              "rule": "3-16 source→target flows with weight 1-5", "validate": _v_flows, "render": _r_flows},
    "network": {"template": {"nodes": [{"label": "…", "group?": "…", "size?": 3}], "edges": [{"source": "…", "target": "…", "label?": "relation"}]},
                "rule": "4-12 nodes, 3-18 edges with relation labels", "validate": _v_network, "render": _r_network},
    "cycle": {"template": {"stages": [{"label": "…", "note?": "…"}], "links?": [{"from": "…", "to": "…", "polarity?": "+|-"}], "loop_type?": "R|B"},
              "rule": "3-8 stages around a circle", "validate": _v_cycle, "render": _r_cycle},
    "matrix": {"template": {"rows": ["…"], "columns": ["…"], "cells": [["…"]]},
                          "rule": "2-8 rows × 2-6 columns, every cell 1-4 words", "validate": _v_matrix, "render": _r_matrix},
    "tree": {"template": {"root": {"label": "…", "children": [{"label": "…", "status?": "taken|foreclosed", "children?": []}]}},
             "rule": "root + children, ≤3 levels, 3-16 nodes", "validate": _v_tree, "render": _r_tree},
    "argument": {"template": {"claim": "…", "premises": [{"label": "…", "evidence?": ["…"], "rebuttal?": "…"}]},
                 "rule": "one claim, 2-5 premises, ≤3 evidence each", "validate": _v_argument, "render": _r_argument},
    "layers": {"template": {"layers": [{"label": "…", "items?": ["…"]}]},
               "rule": "3-6 layers top (abstract) to bottom (concrete)", "validate": _v_layers, "render": _r_layers},
    "columns": {"template": {"columns": [{"label": "…", "items": ["…"]}], "divider?": "…"},
                "rule": "2-4 labelled columns of 1-6 items", "validate": _v_columns, "render": _r_columns},
    "concentric": {"template": {"center": "…", "rings": [{"label": "…", "items": ["…"]}]},
                   "rule": "a center and 2-4 rings of items", "validate": _v_concentric, "render": _r_concentric},
    "spectrum": {"template": {"axis": {"label": "…", "low": "…", "high": "…"}, "items": [{"label": "…", "position": 0.7}]},
                 "rule": "one labelled axis; 3-10 items positioned 0..1", "validate": _v_spectrum, "render": _r_spectrum},
    "bars": {"template": {"measure": "…", "categories": [{"label": "…", "value": "as written in the source, with unit", "note?": "…"}], "emphasize?": "…"},
             "rule": "3-10 categories with NUMERIC values copied from the source", "validate": _v_bars, "render": _r_bars},
    "regions": {"template": {"regions": [{"label": "…", "size": 3, "group?": "…", "neighbors?": ["…"]}]},
                "rule": "4-12 regions sized 1-5", "validate": _v_regions, "render": _r_regions},
    "radar": {"template": {"dimensions": ["…"], "entities": [{"label": "…", "scores": [0, 5]}]},
              "rule": "3-8 dimensions, 1-4 entities scored 0-5", "validate": _v_radar, "render": _r_radar},
    "hub": {"template": {"center": "…", "spokes": [{"label": "…", "kind?": "…", "children?": ["…"]}]},
            "rule": "a center and 3-8 spokes", "validate": _v_hub, "render": _r_hub},
    "gantt": {"template": {"tasks": [{"label": "…", "start": "…", "end": "…", "after?": "…"}]},
              "rule": "3-10 tasks with start/end", "validate": _v_gantt, "render": _r_gantt},
    "waterfall": {"template": {"start": {"label": "…", "value": "…"}, "changes": [{"label": "…", "delta": "+… | −…"}], "end": {"label": "…", "value": "…"}},
                  "rule": "start, 2-8 signed changes, end", "validate": _v_waterfall, "render": _r_waterfall},
    "indicators": {"template": {"indicators": [{"label": "…", "status": "green|amber|red", "trend?": "up|flat|down"}]},
                   "rule": "3-10 indicators", "validate": _v_indicators, "render": _r_indicators},
    "gap": {"template": {"dimensions": [{"label": "…", "current": "…", "desired": "…", "gap?": "…"}]},
            "rule": "3-8 dimensions with current and desired", "validate": _v_gap, "render": _r_gap},
    "before_after": {"template": {"before": {"label": "…", "items": ["…"]}, "move": "…", "after": {"label": "…", "items": ["…"]}},
                     "rule": "before items, the move, after items", "validate": _v_before_after, "render": _r_before_after},
    "toulmin": {"template": {"claim": "…", "grounds": "…", "warrant": "…", "backing?": "…", "qualifier?": "…", "rebuttal?": "…"},
                "rule": "claim, grounds, warrant (+ backing, qualifier, rebuttal)", "validate": _v_toulmin, "render": _r_toulmin},
    "dialectic": {"template": {"thesis": "…", "antithesis": "…", "tensions": ["…"], "synthesis": "…"},
                  "rule": "thesis, antithesis, 1-5 tensions, synthesis", "validate": _v_dialectic, "render": _r_dialectic},
    "square": {"template": {"s1": "…", "s2": "…", "not_s1": "…", "not_s2": "…"},
               "rule": "four corner terms", "validate": _v_square, "render": _r_square},
    "force_field": {"template": {"change": "…", "driving": [{"label": "…", "strength": 3}], "restraining": [{"label": "…", "strength": 3}]},
                    "rule": "the change, 2-6 driving and 2-6 restraining forces (strength 1-5)", "validate": _v_force_field, "render": _r_force_field},
    "scenarios": {"template": {"present": "…", "futures": [{"label": "…", "likelihood": "high|medium|low", "path?": "…"}]},
                  "rule": "the present and 2-5 futures", "validate": _v_scenarios, "render": _r_scenarios},
}


# Bar-family formats drawn from the matrix shape encode LENGTH: their cells must be numbers.
NUMERIC_CELL_FORMATS = {"grouped_bar_chart", "stacked_bar", "marimekko"}


def validate_data(format_key: str, data: Any) -> list[str]:
    """Shape errors for `data` under the format's family (empty list = shape holds). Never raises."""
    errors: list[str] = []
    canon = normalize_format_key(format_key)
    if canon is None:
        return [f"unknown visual_format {format_key!r}"]
    if not isinstance(data, dict) or not data:
        return ["data must be a non-empty object"]
    fam = FORMAT_ENFORCEMENT[canon]["family"]
    try:
        DATA_SHAPES[fam]["validate"](data, errors)
    except Exception as exc:  # a malformed shape is an error, not a crash
        errors.append(f"data does not fit the {fam} shape: {exc.__class__.__name__}: {exc}")
    if not errors and canon in NUMERIC_CELL_FORMATS:
        for row in data.get("cells") or []:
            for cell in row:
                if not re.search(r"\d", _s(cell)):
                    errors.append(f"{canon} draws bar LENGTHS: every cell must be a number as written in the source "
                                  f"(got '{_s(cell)}'); for qualitative comparisons use gap_analysis, comparison_boxes or matrix")
                    break
            if errors:
                break
    if not errors:
        for lab in collect_labels(data):
            words = len(lab.split())
            if words > MAX_LABEL_WORDS or len(lab) > MAX_LABEL_CHARS:
                errors.append(f"label too long ({words} words / {len(lab)} chars, max {MAX_LABEL_WORDS} words): '{lab}'")
    return errors


def render_data(format_key: str, data: dict[str, Any]) -> str:
    """The data spelled out as prose lines for the prompt (assumes validate_data passed)."""
    canon = normalize_format_key(format_key)
    fam = FORMAT_ENFORCEMENT[canon]["family"]
    try:
        lines = DATA_SHAPES[fam]["render"](data)
    except Exception:
        lines = ["  " + json.dumps(data, ensure_ascii=False)]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Catalog text for the planner — primitives × preferred formats, format one-liners,
# family templates.
# ---------------------------------------------------------------------------

_PRIMITIVES_PATH = Path(__file__).resolve().parents[1] / "primitives" / "definitions" / "primitives.json"
_primitives_cache: Optional[list[dict[str, Any]]] = None


def primitives() -> list[dict[str, Any]]:
    global _primitives_cache
    if _primitives_cache is None:
        try:
            _primitives_cache = json.loads(_PRIMITIVES_PATH.read_text("utf-8")).get("primitives", [])
        except Exception:
            _primitives_cache = []
    return _primitives_cache


def primitive_keys() -> list[str]:
    return [p["key"] for p in primitives()]


def primitive_formats(primitive_key: str) -> list[str]:
    """Canonical formats a primitive prefers (its visual_forms, de-aliased, in order, deduped)."""
    out: list[str] = []
    for p in primitives():
        if p["key"] == primitive_key:
            for form in p.get("visual_forms", []):
                canon = normalize_format_key(form)
                if canon and canon not in out:
                    out.append(canon)
    return out


def catalog_text() -> str:
    """Compact catalog: primitives → preferred formats; every format's signature + data family; family templates."""
    lines = ["PRIMITIVES (the analytical relation a figure makes visible) and their preferred formats:"]
    for p in primitives():
        fmts = ", ".join(primitive_formats(p["key"])) or "(any)"
        lines.append(f"- {p['key']}: {p['description'].split('.')[0]}. Formats: {fmts}")
    lines.append("")
    lines.append("FORMATS (key — what it looks like — data family):")
    for key, e in FORMAT_ENFORCEMENT.items():
        lines.append(f"- {key} — {e['visual_signature']} — family: {e['family']}")
    lines.append("")
    lines.append("DATA FAMILIES (the exact JSON shape `data` must take; keys ending in ? are optional):")
    for fam, spec in DATA_SHAPES.items():
        lines.append(f"- {fam} ({spec['rule']}): {json.dumps(spec['template'], ensure_ascii=False)}")
    return "\n".join(lines)


def all_format_keys() -> list[str]:
    return list(FORMAT_ENFORCEMENT.keys())
