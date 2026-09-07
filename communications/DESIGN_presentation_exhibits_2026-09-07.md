# From a wall of text to something a reader can grasp: exhibits as records, a layout desk, and the image bridge

Evgeny, 7 Sep 2026, 09:31, on the Stacks' page for the Brenner 1985 memo: *"a fantastic memo … but a wall of text with a little bit of
sidebars, and the sidebars are also walls of text. Should we start thinking about how to fully leverage the capacity to make images, tables
and HTML side parts — sidebars, boxes, things that help didactically grasp what's at stake; a timeline nicely rendered in SVG or HTML would
go a long way, so would a clean diagram of the direction of Brenner's ideas mapping them onto each other. Inside the analyst we have workflows
for taking text and producing images (six, seven stages, concretization…); many were super complex, we probably want simpler ones. Extra
agents thinking about the layout. And make it explicit, transparent, manipulable — present in the Mastermind as visible categories: inspirational
seeds an LLM can extrapolate for this particular use case."*

## 1. What the Analyst already holds (and the oeuvre run did not use)

The dossier lane has five desks after the engines — spine, tables, figures, plates, compose (then crosscheck) — and the oeuvre pilot ran
engines only, so none of them touched the memo. What they are:

| desk | what it does | the records behind it |
|---|---|---|
| spine | decides what the dossier argues before any exhibit exists; commissions each table and each figure to a section with the claim it must prove | `src/dossier/spine.py`; section kinds `section · table · figure` |
| tables | lifts tables from the engines' ledgers, every cell citing its row, through the wall | `src/dossier/tables.py`; the engines' `tables:` declarations |
| figures | a FigureSpec per commissioned diagram → one of twelve primitives → a visual format → the enforcement wall → one of six style schools → render → a vision check → one revision | `src/workflows/definitions/analyst_figure_pipeline.json`, `src/primitives`, `src/styles`, `src/images/providers.py` |
| plates | full-page images for the appendix, several perspectives | `src/dossier/plates.py` |
| compose | writes the body with the finished exhibits in hand and places each exactly once by a token; HTML / PDF / Markdown | `src/dossier/compose.py`, `templates/dossier.html.j2` |

The image fleet is registered (`src/images/providers.py`): Nano Banana Pro (Gemini 3 Pro Image, $0.13), Nano Banana 2 (Gemini 3.1 Flash
Image, $0.07), Seedream 5.0 Pro ($0.06), Qwen-Image 2.0 Pro ($0.075); a provider is a record with its price, sizes and reference-image
support, so adding one is a record. For HTML consumers the Mastermind already serves a catalogue of **renderers** (accordion, card_grid,
evidence_trail, prose, stat_summary, tab, table, timeline), **sub-renderers** (phase_timeline, timeline_strip, dialectical_pair,
comparison_panel, ordered_flow, move_repertoire, chip_grid, intensity_matrix, key_value_table, mini_card_list …) and **view patterns**
(timeline_sequential, card_grid_grouped …) with data-shape affinities — built for the Critic and the Visualizer, never wired to the
dossier's compose.

So the pieces exist twice: a print-minded pipeline (spine → exhibits → compose) and a screen-minded catalogue (renderers). Neither knows the
other, and neither knows what a *memo about a paper's place in an oeuvre* wants to show.

## 2. What is missing: exhibits as records, and a desk that plans the page

**A. An exhibits registry** (`src/exhibits/`, a sibling of practices and actions): a record per kind of presentation element, with `when`
(the finding kinds or memo parts it serves), `inputs` (the rows or fields it draws on), `medium` (html · svg · image · table · prose-box),
`renderer` (a Mastermind renderer or sub-renderer key, or a figure primitive), `shape` (what it shows and how, in one paragraph), `didactic`
(what the reader should grasp at a glance), `cost` and an `example`. The first seeds, from the oeuvre memo:

| exhibit | when | shape |
|---|---|---|
| `oeuvre-timeline` | oeuvre_trajectory.agenda + the packet's texts | the texts by year on one line, coloured by agenda, the focal text marked, the turns as ticks; SVG (sub-renderer `timeline_strip`) |
| `idea-map` | oeuvre_trajectory.turn + epistemic_rupture.break | a clean diagram of the direction of the ideas: concepts and questions as nodes, "developed into" and "dropped" as edges, the focal text as the hinge; a figure primitive (flow / lineage), rendered simple, one style |
| `two-halves` | epistemic_rupture.verdict | a split panel: the before-half and the after-half named, what persists across (E1) in the middle, what breaks (E2) on the seam; sub-renderer `dialectical_pair` |
| `verdict-chips` | the joined verdicts | five chips in the vocabularies' words (the Stacks' page has them) |
| `sidebar-persists-breaks` | E1 / E2 rows | two short boxes, three lines each, quotes as the anchors |
| `reading-route-cards` | oeuvre_position_memo.read_next | one card per text, ranked, with why and held; `mini_card_list` |
| `shift-table` | citation_shift.* | first cited · dropped · carried, with held / in_referee as marks and the action buttons |
| `pull-quote` | any row with a verified anchor the memo leans on | the sentence, large, with its locus |
| `glossary-box` | the concepts the profiles weight highest | the five terms the reader needs, one line each |

Each is a seed: an LLM extrapolates from these for a new workflow (a cohort memo wants a members-by-circle grid; a fidelity audit wants a
verdict matrix) the way it extrapolates a practice.

**B. A layout desk** (an engine, `page_layout`): reads a memo and its ledgers, the audience, and the exhibits registry, and commissions the
page: which exhibits, from which rows, in what order, with what didactic aim each — a plan as records, walled by code (every exhibit input a
real row id; no exhibit twice; a cap per page). The spine already does this for tables and figures in the print lane; the layout desk is the
same idea for the whole page, with the registry as its vocabulary.

**C. One composer for both media**: the compose desk places the commissioned exhibits by token as today, and the Stacks' page (or the
Analyst's own HTML) renders each by its `renderer` — SVG timelines and panels in HTML, images where an image earns its place. Simpler
figures than the genealogy pipeline's: one primitive, one style, a vision check, no concretization stage unless the desk asks for it.

**D. Write-back**: which exhibits a page used, and whether a reader opened them, goes back on the exhibit record as evidence, like a
practice's yield.

## 3. First steps

1. Run the existing desks on the oeuvre run's ledgers (spine → tables → figures → compose) to see what the print lane makes of them
   as they are — the cheapest measure of the gap.
2. The exhibits registry with the nine seeds above and a `GET /v1/exhibits[?finding=|?memo=]` route; the Stacks' page reads it.
3. The layout desk as an engine over the oeuvre memo; its plan rendered by the Stacks' page; the timeline and the two-halves panel first
   (SVG, no image call), the idea-map as the first image through the fleet.
4. The principle into CLAUDE.md: presentation is records too — exhibits, layouts, styles, providers — and a desk chooses among them.
