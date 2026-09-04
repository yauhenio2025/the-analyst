# Brief for the Wirecut (veo2) session — many sources, one film (2026-09-04)

Paste this into a fresh session in `~/projects/veo2`. Owner's ask: "we have multiple input files, and before we start storytelling we read each of them with LLMs, then find common themes and narrative, not in a banal way but respecting the principles of storytelling and what we need to deliver; what we search for depends on the rest of our process." The reading half is being built in The Analyst (the story desk). This brief is the Wirecut half.

## What already exists (do not rebuild)
- Design memo: `~/projects/the-analyst/communications/DESIGN_multisource_storytelling.md` (read first).
- The contract: `~/projects/the-analyst/communications/STORY_HANDOFF_SCHEMA.json` (JSON schema of `StoryHandoff`) and `STORY_HANDOFF_EXAMPLE.json`. Live: `GET https://the-analyst-kcuc.onrender.com/v1/story/handoff-schema`.
- The story desk API on The Analyst: `POST /v1/story/jobs {sources | from_job, intent, audience, length_seconds}` → reads every source against the demands the downstream Wirecut passes declare in the registry, maps through-lines with tributaries, writes a deliverable-first brief, waits for a choice (`POST /v1/story/jobs/{id}/brief {option_key}`), writes the spine with sources as tributaries, and serves `GET /v1/story/jobs/{id}/handoff`. Full source text: `GET /v1/story/jobs/{id}/sources/{doc_key}`. Events: `GET /v1/events/{id}/stream` (SSE).
- The demands themselves: `GET https://the-analyst-kcuc.onrender.com/v1/story/demands` (they are `source_demands` on `wirecut_telling_desk`, `wirecut_spine`, `wirecut_screenwriter`, `wirecut_storyboard`, `wirecut_text_layer`, `wirecut_grounding_review`, `wirecut_pacing_editor`, `wirecut_music_brief` in the registry, editable in the Master console at https://analyzer-mgmt-frontend.onrender.com/engines/wirecut_spine and siblings). If a Wirecut pass needs something else from the sources, change the demand there, not the reader.
- Wirecut's own doctrines are served hash-pinned by the registry: `GET /v1/engines/wirecut_spine/doctrine` etc. The handoff lists the doctrine hashes it was written under.

## What to build in Wirecut
1. **Corpus intake.** A film can start from a `StoryHandoff` (paste the JSON or give the URL) instead of one file. The film record keeps `sources[]` (doc_key, title, sha256, text fetched from `text_url` and stored locally), the `through_line`, the `spine` and the `ledger`. The single-file path stays as it is.
2. **Spine adoption.** When a handoff is present, the spine pass starts from `handoff.spine` (movements with `sources`, `entry_of`, `element_ids`; motif; hook; open loop) and may refine it under its own doctrine, but must keep each movement's source assignment or say why it changed it.
3. **Clip-level source anchoring.** Every clip carries `source_anchor = {doc_key, quote}` drawn from a ledger element (`element_ids`) or a fresh verbatim quote from that source. The grounding review checks each clip against its own source text, not "the source". A clip with no anchor is ungrounded by definition.
4. **Screenwriter names the tributary.** Each beat records which `doc_key` it draws from; the red-pen pass flags beats that draw on a source the movement does not list.
5. **Harvest on demand.** Before re-reading a source, a pass queries the ledger (by kind, by doc_key, by intensity). Only when the ledger has nothing does it read the source text. Log which happened in the receipt.
6. **Receipts.** The film's receipts record the handoff's `story_job_id`, its doctrine hashes, and per clip the `doc_key` + quote.

## Test material
- A real handoff from the first run (five state-capitalism papers, 4 movements, 99-element ledger): `~/projects/the-analyst/communications/STORY_HANDOFF_REAL_story-3813ecd195ee.json`. A live one on the Analyst API: `GET https://the-analyst-kcuc.onrender.com/v1/story/jobs/story-d3444a230015/handoff` (source texts at `.../sources/{doc_key}`; the desk view is https://the-analyst-desk.onrender.com/s/story-d3444a230015). `STORY_HANDOFF_EXAMPLE.json` is the small hand-written illustration.
- Verify with Playwright: a film started from a handoff shows its sources, its clips show their anchors, and the grounding review names the source per clip.

## Rules
- LLM-first doctrine as always: no keyword matching to assign sources; judgment assigns, code records.
- Do not change the registry from Wirecut; if a demand or a doctrine is wrong, say so in `communications/` and the Analyst session changes it in the Master.
- Keep the single-file path working; add, do not replace.
