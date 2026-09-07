# Readings that stay, and actions approved by intent (Evgeny, 2026-09-07 18:30)

## 0. His words

"That rows data should somehow enter our analysis manuals; it's pretty useful data now, it might help us when we ask about Hintze again.
Every time we do a massive API call on primary sources and we get only some high-level analysis from it, we should always be saving it,
and attaching it to this thinker in some capacity, so that later sessions can skim through it and have a map about what is where and
thus reduce costs — a bottom-up RAG." And, on the oeuvre page's Suggested actions: "they're still very chaotic; one needs to read them all
to figure out what to do because they're not organized based on our intent. What are we trying to do? Expand the network of people around
Brenner to understand whom he is having fights with? Expand our overall horizons? Expand our library? We need an LLM that looks at the
possible actions and at what we have been doing — an action register — and builds a metanarrative about what we do, so that instead of
approving ten similar actions individually we approve an action at the macro level and the ten are approved… a self-constructing
narrative that always narrates what we do so that macro actions become possible. This is what raising productivity is."

## 1. The readings ledger (the Mastermind), and the attachment (the Stacks, the Referee)

A **reading** is one engine's rows over primary sources: job id, engine, the rows with anchors and loci, the texts read (uids, windows),
the persons the rows name, the cost, when. The ledger indexes readings **by person** (every name a row carries as interlocutor · person ·
thinker · opponent · cited · author) and **by text** (every doc key or text uid a row anchors in), written by code the moment a phase or
an added step finishes (`src/readings/`, the executor DB; `GET /v1/readings?person=Hintze`, `?text=em:JZJL34ZJ`, `?job=`). What the
next planner does with it: (1) before a run, read the ledger for the packet's persons and texts; (2) feed the prior rows as a context
block (`PRIOR READINGS`) — the engine cites them by id and reads only what is new; (3) skip a text whose windows were read for the same
question. The Stacks attach the same readings to the author's page and the text's record ("what the Mastermind has read of this",
by run, with the rows' loci), and the Referee to the thinker. Rule, in CLAUDE.md: every heavy reading leaves its rows behind.

## 2. Intents, the register, the narrative, the macro actions

- **Intents** (vocabulary `intents`, owner the-mastermind, the owner's words): expand_network (the people around a thinker, whom he
  fights with), expand_library (hold what is cited), expand_horizons (schools and debates we do not have yet), sharpen_position (the
  distinction and encounter work), verify_holdings (identity, editions, copies), keep_current (harvests and re-runs). Every action
  record gains `intents` (which it serves); a suggested action inherits them.
- **The action register**: what we did — every action outcome posted (`POST /v1/actions/{key}/outcome`, already there), every run
  (jobs), every added step, every answer of his on the Brief — kept as one time-ordered record (`GET /v1/register?since=`).
- **The narrative** (engine `trajectory_narrative`, run once a session or on demand): reads the register and the intents and writes
  what we are doing — the projects in flight, the thinkers in play, the intents served, what stalled — as a record the sessions read
  (`GET /v1/trajectory`), in the owner's terms, never a log.
- **The macro actions** (engine `macro_actions`): given a page's suggested actions (the oeuvre page's sixteen), the trajectory and the
  intents, it groups them into three to five macro actions — "Expand Brenner's network: add Meek, Cohen, North, Thomas to the Referee,
  placed; harvest their citations — 8 actions, ~$3" — each with its intent, the micro actions it enables (their keys and inputs), the
  cost class, and what it would let us see; `POST /v1/actions/macro {actions, trajectory?}`. The page shows the macro actions first; one
  approval runs the batch under a cap on the organs' routes; outcomes feed the register; the narrative updates.

## 3. Seams

The Stacks: the sidebar grouped by intent with macro buttons (the micro list folds under each), the batch runner under a cap, the
readings attached to author and text records; the Referee: the readings on the thinker. Handoff for the idle Stacks sessions:
`communications/HANDOFF_stacks_readings_and_macro_actions_2026-09-07.md`.
