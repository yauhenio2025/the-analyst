# Handoff to the Stacks (Evgeny, 2026-09-07 18:30, via the Mastermind): readings attached to thinkers and texts; the actions sidebar by intent

Two asks of the owner, the Mastermind's part is under way (design: the-analyst `communications/DESIGN_readings_and_macro_actions_2026-09-07.md`); these are the Stacks' parts. Take them in an idle session; say which you take.

## A. Attach the Mastermind's readings to the author and to the text ("a bottom-up RAG")

- Read `GET https://the-analyst-kcuc.onrender.com/v1/readings?person=<name>` and `?text=<uid>` (live once the Mastermind's ledger deploys; shape: readings[] with job_id, engine, when, cost_usd, rows[] {id, dim, text, anchor, doc, locus, fields}, texts[] {uid, windows read}).
- On the author's page and on the text's record, a section "what has been read of this": by run, the engine, the number of rows, the loci read, a door to the Mastermind's rendering (/oeuvre, /distinctions, /encounter/page) — so a later session sees at a glance what is where before it spends.
- When a new run is commissioned from a Stacks page (oeuvre, brief, hunch), pass the prior readings' job ids in the request's packet as `prior_readings` so the Mastermind feeds them as context and reads only what is new.

## B. The Suggested actions sidebar, by intent, with macro actions

- The owner: "they're still very chaotic; one needs to read them all to figure out what to do because they're not organized based on our intent — expand the network around Brenner? expand our horizons? expand our library?"
- The Mastermind serves `GET /v1/vocabularies/intents` (expand_network · expand_library · expand_horizons · sharpen_position · verify_holdings · keep_current) and `POST /v1/actions/macro {actions: <the page's suggested actions>, context?}` → macro_actions[] {intent, title, says (what it lets us see), enables[] (action key + inputs + organ), cost_class, estimate}.
- The sidebar shows the macro actions first (three to five buttons: "Expand Brenner's network — 8 actions, cents"), the micro list folded under each; one press runs the batch through your composite runner under a cap (the same way stacks.add-placed chains resolve → create → candidates), posting each outcome to `POST /v1/actions/{key}/outcome` with the macro's id as `batch`, so the register and the narrative see them.
- Every action outcome you post already reaches the register; add `intent` when you know it.

## What the Mastermind builds (so you can plan against it)
- `src/readings`: the ledger written by code when a phase or an added step finishes; the routes above.
- `intents` vocabulary; `trajectory_narrative` and `macro_actions` engines; `GET /v1/register`, `GET /v1/trajectory`, `POST /v1/actions/macro`.
