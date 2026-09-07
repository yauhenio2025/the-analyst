# From a wall of text to something a reader can grasp: exhibits as records, a layout desk, and the image bridge

Evgeny, 7 Sep 2026, 09:31, on the Stacks' page for the Brenner 1985 memo: *"a fantastic memo … but a wall of text with a little bit of
sidebars, and the sidebars are also walls of text. Should we start thinking about how to fully leverage the capacity to make images, tables
and HTML side parts — sidebars, boxes, things that help didactically grasp what's at stake; a timeline nicely rendered in SVG or HTML would
go a long way, so would a clean diagram of the direction of Brenner's ideas mapping them onto each other. Inside the analyst we have workflows
for taking text and producing images (six, seven stages, concretization…); many were super complex, we probably want simpler ones. Extra
agents thinking about the layout. And make it explicit, transparent, manipulable — present in the Mastermind as visible categories: inspirational
seeds an LLM can extrapolate for this particular use case."*

## 0. What the page is for (Evgeny, 09:45)

*"What really counts is for us to look at this and grasp the ideas immediately, in their best possible version, in the minimum time; to arrive at
clarity as fast as possible and absorb what is presented in the deepest rather than the shallowest way, using as many cognitive structuring
supports as help us penetrate the substance without feeling alienated, and build a mental model of it as soon as possible."* By reading text
alone we fail the first time and reread; every exhibit, sidebar, table and image is there to cut that. So the desks that plan and revise a page
optimise one thing: **time to clarity, at depth** — the reader grasps the argument on the first pass and keeps a model of it.

That is a loop, not a step: a planner decides the balance of text, images, tables, HTML elements and sidebars for this memo and this reader,
and commissions them; a reviewer reads the assembled page as the reader would and sends back what fails — a table too intimidating, an image
too detailed, a sidebar that repeats the text, a section that needs a timeline before it can be read — and the desks revise; several rounds if
needed, under a cap, until the page reads at the first pass. Proof of concept first; the cost of the rounds is not the constraint. The
planner, the strategist and the reviser are engines deposited in the Mastermind like the rest, with this goal as their brief.

A caution from the owner: the renderer catalogue for screens (§1) was built for the Critic and the Visualizer but never fully operationalised;
treat each renderer as untested until a page has used it, and prefer the few that a real page exercises.

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

## 2b. The loop, as desks

| desk | reads | writes | walled by |
|---|---|---|---|
| `page_planner` | the memo, its ledgers, the audience, the exhibits registry | the page plan: sections in order, each with its text budget, its exhibits (kind, rows, didactic aim), the sidebars | every input a real row id; no exhibit twice; a cap on exhibits per page; the registry's kinds only |
| the makers | one plan item each: a table desk, a figure desk (primitive · style · fleet · vision check), an SVG desk for timelines and panels, a sidebar desk, a prose desk that rewrites a section to its budget | the exhibit, with its provenance | the existing walls: tables cite rows; figures pass the vision check; SVG carries only what its rows carry |
| `page_reviewer` | the assembled page, as the stated reader | verdicts per element (keep · simplify · replace · drop · move) with the reason, and a time-to-clarity judgment per section | verdicts only on elements that exist; a reason names the element; a round limit |
| the composer | the plan and the revised exhibits | HTML for the screen, PDF/Markdown for print, the same tokens | every exhibit placed once, in the plan's order |

The reviewer's verdict vocabulary and the exhibits' kinds are registry records, so the owner can read and edit what the loop optimises for.

## 3. First steps

1. Run the existing desks on the oeuvre run's ledgers (spine → tables → figures → compose) to see what the print lane makes of them
   as they are — the cheapest measure of the gap.
2. The exhibits registry with the nine seeds above and a `GET /v1/exhibits[?finding=|?memo=]` route; the Stacks' page reads it.
3. The layout desk as an engine over the oeuvre memo; its plan rendered by the Stacks' page; the timeline and the two-halves panel first
   (SVG, no image call), the idea-map as the first image through the fleet.
4. The principle into CLAUDE.md: presentation is records too — exhibits, layouts, styles, providers — and a desk chooses among them.

## 4. Placement: the text is the main dish (Evgeny, 11:45)

The first pages put the exhibits at the top and the essay under them; the owner: "this giant tape… cannot be the main dish… placing those items at the top hides the rest of the essay… strategize about placement on the page." The rule now stands in three records and one piece of code, so the planner does not have to rediscover it:

- **The vocabulary** `exhibit_placements`: before (verdict chips only) · beside (a narrow element read with the text) · after (the evidence after the claim) · folded (a titled line after its section that the reader opens; a reference the reader consults, never the page's lead).
- **The exhibit record** carries a default `placement`; the timeline, the shift table, the idea map and the glossary fold; the sidebar and the pull quote sit beside; the two halves and the route cards follow their section; the chips lead.
- **The planner and the reviewer** say it in words: the reader meets the first paragraph at once; never two exhibits between two paragraphs; an exhibit between the reader and the first paragraph gets `move`.
- **The composer** enforces it by code whatever the plan says: a wide exhibit never floats and never leads; a folded exhibit is a `<details>` element titled by its maker in words (never an id); in the Stacks' page the same exhibits are thumbnails that open modals under the memo.

The essay itself: the memo's four parts (read backwards · read forwards · read whole · the route) were the engines' order, not an argument's; the owner found it mechanical. The memo brief now asks for one short essay with one line of argument, the readings as evidence inside it, at most three headings of the argument's own, the route as a ranked list and the open question in a sentence. The page planner then follows the argument, not the engines.

Drawing: the two-halves panel was a Sankey idea (lines crossing or stopping at a seam) applied to a list; the lines ran through the text. Its data's job is identity (persists / changes) between two named texts, which is a two-column comparison with a marker per row. When a form fights its text, change the form.

