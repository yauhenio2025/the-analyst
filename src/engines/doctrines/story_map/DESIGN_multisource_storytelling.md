# Multi-source storytelling — design (2026-09-04)

> Owner: "the assumption is that we are using just one file to render video… we have multiple input files, and before we start storytelling we add a step where we read each of them with LLMs, and only after we read them we come up with common themes and narrative… not in a banal way, but in a serious way that would respect the main principles of storytelling and what we actually need to deliver at the end. What we are searching for has to be dependent on the rest of our process." To be built around the Master, not inside Wirecut alone. Not urgent.

## 1. The principle: read against demands, not for themes

A theme hunt over many documents produces a keyword cloud. A film needs something else: one question, a face on the stake, values that turn, antagonism at full strength, reveals released on a need-to-know basis, a motif that can be planted and paid off, and pictures that can be filmed (Wirecut's twelve laws, `veo2/communications/STORYTELLING_STUDY_2026-09-02/SYNTHESIS.md`). Every one of those is a *demand* that a downstream pass makes on the sources:

| Downstream pass (registered engine) | What it needs from the sources |
|---|---|
| Telling desk (`wirecut_telling_desk`) | the question each source raises or answers; the faces with a stake; verdict-capable facts; who the film could belong to |
| Spine (`wirecut_spine`) | turns: a value before/after and what turned it; recurring objects and images (motif candidates); the strongest opening fact (hook); the unresolved question (open loop) |
| Screenwriter (`wirecut_screenwriter`) | facts ordered by when a viewer must know them; lines quotable as narration; numbers with their units |
| Storyboard, prompt bench, text layer | filmable places, objects, people and numbers; named public figures (likeness law); verbatim phrases usable as titles |
| Grounding review (`wirecut_grounding_review`) | a verbatim anchor (document, quote) on every element above |
| Pacing, music | the intensity of each element; where the material itself breathes |

So the reading pass is defined by the *union of the demands declared by the passes that follow it*. That is the sense in which "what we search for depends on the rest of the process", and it is why the pass belongs in the Master: the demands are fields on registered engines, editable in one place; change what the telling desk asks for and the reading changes, without touching Wirecut.

## 2. The process (registered as `wirecut_multisource_story`, planned)

1. **Ingest many.** The Analyst's source resolver already turns uploads, stacks bundles and exemplars into a headed corpus (`the-analyst:src/sources/resolve.py`). Same input shape as a dossier.
2. **Story reconnaissance, per document** (`story_reconnaissance`, family storytelling). One call per document (1M-context path for long ones), producing a StoryProfile whose fields are the demand table above: `questions[]`, `faces[]` (name, stake, what they chose), `turns[]` (value, before, after, what turned it), `antagonisms[]`, `reveals[]` (what a reader assumed, what is true), `motif_candidates[]`, `filmables[]` (place/object/number/person, visual form), `quotables[]`, `intensity`, `gaps` (what this source cannot support). Every element carries `{doc_id, quote}`; the anchor wall from the Analyst's tables step (`the-analyst:src/dossier/walls.py`) drops any element whose quote is not in the source. Mirrors the Analyst's reconnaissance (`the-analyst:src/dossier/reconnaissance.py`), which builds a DocumentProfile per document and a corpus map.
3. **Story map, across sources** (`story_map`, kind comparison). Reads the profiles, not the documents: which faces, turns and objects recur; where sources contradict (antagonism the film can use) and where they corroborate; a timeline if the material is temporal; and **candidate through-lines**: each with its one question, face on the stake, the value that turns, the open loop, the sources that carry it (tributaries) and the sources that do not. Rule: a through-line is carried by at least two sources, or it is declared a single-source film with the rest as context. Output includes a coverage matrix (source × through-line) so the operator can see what a choice leaves out.
4. **Approach slate over the corpus.** `wirecut_narrative_approaches` ranks the twelve structures against the story map, per approach naming which sources carry it and what must be cut.
5. **Brief, deliverable-first** (`story_brief`, family composition; same law as the Analyst's brief v2): three options, each stating what the viewer will understand and feel, the length, the through-line, the approach, the sources it uses and the cost. Nothing is rendered before the operator chooses.
6. **Spine with tributaries.** `wirecut_spine` runs on the story map for the chosen through-line: movements are assigned to sources, the motif is chosen from the recurring elements, and each source's entry point is declared. The state-capitalism flow plate ("five cases, one current") is the visual of this: one current, tributaries entering at the station where each made its decisive commitment.
7. **The existing chain, unchanged in shape.** Telling desk → screenwriter → board → … → screening. Two adjustments: the grounding review checks each clip against the specific source it anchors to (doc_id + quote, not "the source"), and the screenwriter names the tributary each beat draws from.

**Harvest on demand.** The story profiles are a queryable ledger, not a one-shot summary. When a later pass needs something concrete (the screenwriter wants a scene for movement 3; the text layer wants a verbatim number), it asks the ledger first, and only re-reads a document if the ledger has nothing. This is the Referee's term-harvest pattern (`gs_revamp`: terms harvested at evaluation, deployed later) applied to story elements, and it is what keeps a ten-document film from re-reading ten documents at every pass.

**Concretization.** As in the Analyst's spine → exhibits → draft passes, the map is revised when later passes learn something the profiles did not say: a reveal discovered while scripting is written back to the ledger with its anchor, so the map, the spine and the script stay one thing.

## 3. What is reused, what is new

| Reused | From |
|---|---|
| Multi-input resolver, headed bundle | The Analyst `src/sources/` |
| Per-document reconnaissance pattern, anchor wall, brief v2 lanes | The Analyst `src/dossier/{reconnaissance,walls,brief}.py` |
| Twelve laws, telling dials, approaches, spine, grounding review | Wirecut `engine/prompts/*.md` (served by the Master's doctrine endpoint) |
| Term-harvest / ledger pattern | The Referee |

New: `story_reconnaissance`, `story_map`, `story_brief` engines (designed, registered today), the StoryProfile and StoryMap schemas, the coverage matrix, the demand fields on downstream engines (`source_demands`, to be added to the engine record), and Wirecut's "corpus" input (a job holds many sources; clips anchor to one).

## 4. Where it runs

Two options, decided later. (a) Wirecut gains a "corpus" ingest and calls the Master for the reading and mapping engines' doctrine (Phase B of the Master memo). (b) The Analyst runs steps 1–5 as a dossier-shaped job whose deliverable is a story brief and hands the chosen spine to Wirecut as a single structured input. (b) needs no Wirecut change beyond accepting a spine, and gives the story brief a library page; it is the faster first version.

## 5. LLM-first ledger

Judgment: everything in steps 2–6. Code: shape validation of profiles, the anchor wall, the coverage matrix arithmetic, sequence, receipts. No keyword clustering, no similarity math for themes, no thresholds deciding a through-line.
