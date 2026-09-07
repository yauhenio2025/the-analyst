# Codex brief: the Brief page's trace drawing — "this part with arrows has to look gorgeous and legible" (Evgeny, 2026-09-08 00:53)

## The complaint, in his words

Looking at the Brief page's right column (`http://127.0.0.1:8765/static/brief.html?id=1`, the drawing under "how your words moved the
model"): **"come on, this part with arrows has to look gorgeous and legible… we are not there yet — it's too dark, too small, doesn't seem
to expand/popup, and it's aesthetically not very nice."**

Four screenshots show the same failures: the drawing lives in a ~180px-tall strip with a horizontal scrollbar; nodes are clipped at both
edges (`PART part…`, `QUESTION · O… Sewell keeps…`); the type is ~10px on a dark node on a dark page; the selection highlight paints whole
nodes electric blue; edge labels ("moves", "identified · h…") are truncated mid-word; and nothing opens to full size.

## What it must become

The Mastermind's exhibit record for this drawing is `GET https://the-analyst-kcuc.onrender.com/v1/exhibits/trace-map` — read it; its
`shape` is the contract. In short:

1. **It opens.** In the column, the drawing is a **thumbnail with its counts in words** ("your comment of 6 Sep 23:28 · moves parts 1 and 6 ·
   1 edit · 3 questions · 2 hunches"), one line, no scrollbar. Clicking it opens a **layer over the page** at the window's width and at least
   70% of its height, with a close button and Esc to close. That layer is where the map is read.
2. **It is legible.** Node title ≥ 13px, node body ≥ 12px, never clipped: a node is at least 180px wide and its text wraps to at most three
   lines with a real ellipsis on the last. 24px between columns, 16px between rows. The drawing's surface is one step lighter than the page
   (a card, not the void), and node text is the page's primary ink, not a grey.
3. **It is beautiful in the plain way**: one hue per effect from a validated palette (moves · supports · complicates · contradicts), the same
   hue for a node's border and its edges; edges are 2px curves that never cross a node; an edge label sits on its own, in the ink colour,
   only where it fits, and the legend at the layer's foot names all four effects. No electric-blue selection wash: a selected node is marked
   by a 2px ring in its own hue and a slightly lighter fill.
4. **Every node is still a door** (that already works): clicking a part scrolls to it, a question or a hunch opens its row, a work or memo
   opens its record. Keep that, and make it obvious: the cursor, a hover lift, a title attribute naming what a click will do.
5. **It reads in both themes**: define the palette as tokens on `:root`, redefine them under `@media (prefers-color-scheme: dark)` guarded by
   `:root:not([data-theme="light"])`, and give the drawing's surface an explicit background so it never borrows the page's.

Use the house's dataviz rules: assign a hue per effect in a fixed order, never cycle; keep marks thin and the grid recessive; a legend is
always present for four series; text wears text tokens, never the series colour.

## Rules

- Branch off current main; touch only `app/static/trace.js`, `app/static/brief.css` (or the trace's own css), the trace fake and the harness
  (`tests/frontend/`), and a report in `communications/`. **Nothing in `app/briefs.py`, `app/static/brief.js`, `app/exchange.py`,
  `app/dictate.py`, `app/references.py`** — the Brief's owner is building there tonight.
- Run the trace harness in the FOREGROUND, once per message, and the documented pytest command for anything you touch. No pytest-asyncio.
- Screenshot the layer at 1440×900 and at 1100×800 and say in the report what each shows.
- No new dependencies; no charting library; the drawing stays hand-drawn SVG as it is now.
- Commit in the house style (a sentence saying what and why).
