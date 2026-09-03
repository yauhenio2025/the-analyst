# DESIGN — The brief, deliverable-first

> Step 2 of The Analyst ("the brief") redesigned so that its options are framed by the DELIVERABLE and by what the reader will be able to UNDERSTAND and DO — not by engines. Design + prompt spec, 2026-09-03. No code changed by this document.

**Plain-language summary.** Today the brief offers three "angles" on the material: three topics, each dressed with the engines that would produce it and an identical price. The reader cannot tell what they would *do* with any of them. The redesign makes every option a promise about use: *what you get*, *what you will understand*, *what you will be able to do*, *what it will not tell you*, verified against the concrete shape (sections, tables with their row unit, figures with their format) and the documents that carry it. Engines become the secondary "how" line. Three ways in: say what you will use it for (default), pick the analysis yourself from a purpose-first catalog (competent user, the visualizer model), or let the material decide (the desk picks and explains why).

**The owner's words (2026-09-03):** "For the initial options that you present on how to structure the brief — look at the front end of the visualizer: there we assume the competent user who knows what kind of analysis they want. For some cases that would be the case. Sometimes the nature of the material will suggest what engines to use. Sometimes we want to use multiple ones. But when you present options and different ways to do it, make it really clear what are the possible uses of it, so the user figures out: 'I'm going to use this report to understand this and this' — and based on that they understand which option to choose. You have to understand what each path will allow them to understand and to do. Focus on the deliverables and what it will change in their action, more than anything else."

Sources read for this design: `src/dossier/brief.py`, `schemas.py`, `plan.py`, `common.py`, `runner.py`, `tables.py`/`figures.py`/`compose.py` (how the chosen option flows downstream), `src/api/routes/dossier.py`, `web/src/steps/BriefStep.tsx`, `pages/Library.tsx`, `lib/api.ts`, `types.ts`, `web/mock/brief.json`; the real briefs of `live-dossier-dce25aeed631` (state-capitalism bundle, no intent), `live-dossier-be00c33e5180` (fashion bundle) and `live-dossier-10656694ada2` (Kering study); the visualizer front end and MCP (`/home/evgeny/projects/_study/visualizer-master`: `app.py` picker markup, `mcp_server/mcp_server.py` tool docstrings, `docs/IMPLEMENTATION_PLAN_INTENT_BASED_ANALYSIS.md`, `docs/TEXTUAL_OUTPUT_TYPES.md`); the 28 capability YAMLs in `src/engines/capability_definitions/`; `src/audiences/definitions/*.json`; the OAAS vision notes (§D, §H); veo2's telling cards (`web/src/steps/LookStep.tsx`, `web/src/i18n.tsx`, `engine/telling.py`).

---

## A. Critique of the current options (with quotes from the real briefs)

### A1. What the prompt asks for, and what it gets

`src/dossier/brief.py` SYSTEM: *"you propose exactly THREE distinct angles (tellings) a dossier could take — three genuinely different readings, not three phrasings of one. Each angle names the executable analysis engines that would produce it… and says why each engine earns its place."* The only mention of use is one clause inside the `telling` field description: *"what the reader learns that they could act on"* — unenforced, unstructured, unverifiable.

Consequence: the three options always differ by **topic**, never by **use**. Live briefs:

| Job | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| state-capitalism (`dce25aeed631`, intent = none) | "Who Actually Benefits When States Back Tech and Defence" | "When Countries Can Say No to Great Powers—and When They Cannot" | "Investment Screening Is the New Tariff—What Luxury Must Know" |
| fashion (`be00c33e5180`) | "Where Your Sustainability Claims Will Break Under Scrutiny" | "How Platform Fast Fashion Undermines Your Ethical Supply Story" | "The Civic Commitment Trap: When Values Campaigns Turn Against You" |
| Kering (`10656694ada2`) | "The One Gap in Kering's AI Stack" | "Four Handovers, Zero Continuity Instrument" | "Gucci's China Problem Is Not a Product Problem" |

A reader who needs to *brief a board*, *prepare a negotiation*, or *decide whether to sign a partnership* gets no purchase on this split. The options are three essays, not three instruments.

### A2. The promise of use is either absent, rhetorical, or unsupported by the corpus

- **Absent / rhetorical.** State-capitalism option 1 ends: *"asks executives of a luxury house: when governments come to you with 'strategic partnership' language, what are they actually asking you to absorb on behalf of others?"* — a question is not an action. Option 3 ends: *"tells executives where the next boundary moves are likely to land"* — five academic papers (2020–2024) periodise; they do not forecast. That promise cannot be kept and the composed dossier did not keep it.
- **Unsupported by the corpus.** Fashion option 1 promises: *"Together the documents let executives see, claim by claim, which of their current positions are coherent and which are one investigative article away from collapse."* The corpus contains no house positions at all. The delivered "Claim-by-Claim Stress Test" table has **4 rows of claim *types*** (`Claim type | What legitimacy requires | Illegitimacy trigger | Opportunism trigger | Survival condition`), not claims. Option 2 likewise promises *"a concrete gap analysis: what the house's current supplier code and ESG reporting actually cover"* — no supplier code is in the documents. Nothing in the option says so. There is no `not_for`.
- **Closest to right.** The Kering option 1 comes nearest to a deliverable: *"so an executive walking into Wednesday's meeting knows the precise half-sentence that opens the pitch and the two things not to say."* This is the register the whole card should be in — and it is buried at the end of a 150-word paragraph.

### A3. The "understand / do" content exists — but hidden in `output_shape.sections`

The desk can already imagine decisions: fashion option 1's last section is *"Decisions: Which Claims to Advance, Which to Retire"*; option 2: *"Decisions: Traceability, Margin Floors, and Verification Investments"*; option 3: *"Decisions: The Three Conditions a Campaign Must Pass Before Launch"*. In the UI, `output_shape` is flattened to the string *"5 sections · 2 tables · 2 figures"* (`api.ts:normalizeBriefOption`). The one thing the reader needs to choose is the one thing collapsed to a count.

### A4. Engines are the most prominent structured element, in engine vocabulary, to an executive

The card shows raw keys as chips (`inferential commitment mapper`, `dialectical structure`) and a `why` line that is the concatenation of per-engine justifications: *"This engine surfaces those fault lines claim by claim."*, *"this engine makes those obligations explicit"*, *"Surfaces the repeating institutional template—state subsidy, discursive legitimation, corporate capture"*. The plan then speaks of *"inferential debts"* and *"dialectical fault lines"*. The executive vocabulary file (`src/audiences/definitions/executive.json`, 1,599 translations) already says: *"inferential commitment → hidden obligation (what you're really agreeing to)"*, *"dialectical → argument-focused (examining competing positions)"*, and its guidance intro is *"Executives should never encounter unfamiliar terms."* The brief prompt does not load it.

### A5. No trade-off between the options

Every option in a brief costs the same: **$1.55 · 17.8 min ×3** (state-capitalism), **$1.85 · 18.0 min ×3** (fashion). `estimate_option()` derives cost from `job.options.depth` and truncates every option to the same engine count, so price and time cannot differentiate. The mock fixture the front end was designed against (`web/mock/brief.json`) did carry trade-offs (*"Cheapest and safest for a careful counterpart in pre-results mode; thinner on the structural argument"*, $0.88 vs $2.15); the live prompt lost them.

### A6. "Recommended" never shows; autopilot is blind

`BriefStep.tsx` renders *"· recommended"* from `brief.defaults.option_key`, which the backend never sets (`BriefDefaults` has no such field). Autopilot (`runner.py:159`) takes `brief.options[0]` — *"autopilot: chose option 1"* — with no reason recorded. This is not "let the material decide"; it is "take the first".

### A7. Shape is not verifiable

Tables are captions without a row unit; figures are scene descriptions without a format; sections are headings without the question they answer. The reader cannot check "claim by claim" against "T1 has one row per claim type, 4–6 rows". Downstream, `tables.py` uses the captions only as *"Table ideas from the brief"*.

### A8. The brief is the right place, and the raw material is already there

Reconnaissance produces exactly what a deliverable-first card needs: `corpus_map.shared_questions` (the questions the corpus can answer), `disagreements`, `throughlines`, `candidate_angles`, per-document `key_claims` with verified anchors, entities and tensions. Nothing new has to be extracted; the brief has to be *asked differently and checked*.

---

## B. The new option card — `BriefOption v2`

### B1. Design rules (from the owner's words and the vision notes)

1. **Lead with use.** The first three things on a card are *what you get*, *what you will understand*, *what you will be able to do*. Engines are a secondary "how" line.
2. **Options differ in USE, not in engine or topic.** Each option serves a different job-to-be-done from a fixed *use register* (B5). If the requester stated a use, the three options serve it through three different deliverables whose "able to" sets do not overlap.
3. **Concrete to this material.** Every understand/do line names something from the documents (an entity, a number, a quote, a document). Test: swap the corpus and the line becomes false.
4. **Verifiable against the shape.** Every "you will be able to" line points at the section/table/figure that supports it. Every table declares its row unit. Every figure declares its format.
5. **Honest scope.** `not_for` states what the corpus cannot deliver (no house data, no forecast, single source…).
6. **Audience vocabulary.** Executive cards use the audience vocabulary file; no theory words. Analyst/researcher cards may use them.
7. **Real trade-offs.** Options carry their own depth and shape, so price and time differ (a light, a standard, a full).
8. **Ballot, not memo** (vision §H9): a card must be decidable in under a minute; hard caps on lengths.
9. **Recommended, with a reason** (vision §H2, §H6): the desk names one option and says why in the reader's terms — this is also what autopilot executes.

### B2. Schema (Pydantic v2, `src/dossier/schemas.py`)

```python
DELIVERABLE_KINDS = ("stress_test", "decision_memo", "briefing", "playbook", "comparison",
                     "watchlist", "reading_guide", "decoder", "risk_register", "case_file")

USE_KINDS = ("decide", "brief", "prepare", "stress_test", "compare", "watch", "learn", "argue")


class ShapeRef(BaseModel):
    """Pointer from a promise to the shape element that keeps it: S3 / T1 / F2."""
    kind: Literal["section", "table", "figure"]
    index: int                      # 1-based within its list


class SectionSpec(BaseModel):
    heading: str                    # <= 70 chars
    answers: str                    # the question (from questions_answered) this section answers, <= 120


class TableSpec(BaseModel):
    title: str                      # <= 90 chars
    row_unit: str                   # "one row per sustainability practice the house uses", <= 60
    columns: list[str]              # 3-5 column headings, each <= 30
    rows_expected: str              # "8-10"
    carried_by: list[str]           # doc_keys whose text will fill the cells


class FigureSpec(BaseModel):
    title: str                      # <= 90
    format: Literal["two_axis_grid", "timeline", "flow", "before_after", "map", "spectrum",
                    "stack", "network", "scene"]
    scene: str                      # depictable, no text in the image, <= 220


class Shape(BaseModel):
    sections: list[SectionSpec]     # 3-6
    tables: list[TableSpec]         # 1-3
    figures: list[FigureSpec]       # 0-3


class Promise(BaseModel):
    text: str                       # <= 140 (understand) / <= 120 (able_to), verb-first for able_to
    supported_by: list[ShapeRef]    # >= 1


class EvidenceBase(BaseModel):
    carrying_docs: list[dict]       # [{"doc_key": "U3PWD6J3", "carries": "the two legitimacy failure modes"}]
    thin_or_missing: list[str]      # "no house-specific claims are in the corpus", <= 140 each


class PathStep(BaseModel):
    engine_key: str
    plain_name: str                 # audience-register name, e.g. "hidden-obligations map"
    contributes: str                # one line, reader terms, <= 120
    depth: Literal["surface", "standard", "deep"] = "surface"


class Path(BaseModel):
    steps: list[PathStep]           # 1-4, run order
    depth: Literal["simple", "medium", "advanced"]
    primitives: list[str] = ["prose", "anchored_tables", "figures"]
    chain_key: Optional[str] = None # when a recipe/chain was chosen (path 2)


class BriefOption(BaseModel):
    version: int = 2
    key: str
    title: str                      # <= 10 words
    deliverable_kind: str           # one of DELIVERABLE_KINDS
    deliverable: str                # "a 5-section stress test with a claim-type scorecard", <= 110
    use_kind: str                   # one of USE_KINDS — the option's job-to-be-done
    you_will_understand: list[Promise]   # exactly 3
    you_will_be_able_to: list[Promise]   # 2-3
    questions_answered: list[str]        # 3-4, <= 120 each
    not_for: list[str]                   # 1-3, <= 120 each
    shape: Shape
    evidence_base: EvidenceBase
    path: Path
    best_when: str                  # <= 140, "Pick this when …"
    est_cost_usd: float = 0.0
    est_minutes: float = 0.0
    est_llm_calls: int = 0

    # ── back-compat views (computed; keep plan/tables/figures/compose untouched in step 1)
    @computed_field
    @property
    def telling(self) -> str:
        return f"{self.deliverable}. " + " ".join(p.text for p in self.you_will_understand)

    @computed_field
    @property
    def engines(self) -> list[EngineChoice]:
        return [EngineChoice(engine_key=s.engine_key, why=s.contributes) for s in self.path.steps]

    @computed_field
    @property
    def output_shape(self) -> OutputShape:
        return OutputShape(sections=[s.heading for s in self.shape.sections],
                           tables=[f"{t.title} — {t.row_unit}" for t in self.shape.tables],
                           figures=[f"{f.title} ({f.format}): {f.scene}" for f in self.shape.figures])


class Recommendation(BaseModel):
    option_key: str
    because: str                    # reader-register, <= 220; names the corpus reason
    runner_up: Optional[str] = None
    runner_up_because: Optional[str] = None


class Brief(BaseModel):
    version: int = 2
    entry: Literal["use", "chosen", "material"] = "use"
    options: list[BriefOption]
    recommendation: Optional[Recommendation] = None
    defaults: BriefDefaults
```

Notes.
- `telling`, `engines`, `output_shape` remain readable, so `plan.py:chosen_option`/`build_executor_plan`, `tables.py:64`, `figures.py:45`, `compose.py:73` keep working unchanged. Step 2 of the implementation map then lets tables/figures read `row_unit`/`format` directly.
- `est_*` stay code-computed (`estimate_option`), now from **the option's own** `path.depth` and step depths, so the three prices differ.
- `BriefDefaults` gains nothing; `Recommendation` replaces the never-set `option_key`.

### B3. Card anatomy (what the reader sees, top to bottom)

```
DELIVERABLE · A            stress test            ★ recommended — because <reason>
Where your sustainability claims will break
A 5-section stress test of the four claim types a house makes, with a scorecard of what each commits you to.

YOU WILL UNDERSTAND
 · the two ways a claim fails for consumers — no link to brand history, visible commercial motive — as 12 consumers described them [U3PWD6J3]
 · for each of the 10 practices (reduce, reuse, repair…), the market counter-move that turns it back into a sales story [SG4IGV3Y]
 · how a hashflag gesture is withdrawn when it collides with commercial interest, and what that does to trust [WUPV36YG]

YOU WILL BE ABLE TO
 · decide which claim types to advance and which to retire before the next campaign        T1
 · set the evidence a claim needs before launch — brand-history anchor, multi-action record  T3
 · brief comms on the three questions journalists will ask                                  §5

ANSWERS  What makes a claim legitimate? · Which practices are most exposed? · When does silence cost more than a campaign? · What track record survives an investigation?
NOT FOR  It does not score the house's actual claims — none are in these documents; it scores claim types. No consumer data beyond the 12 interviews.

SHAPE    5 sections · 3 tables · 1 figure            ▸ T1 one row per claim type (4–6) · T2 one row per 10-R practice (10) · T3 one row per active claim category · F1 two-axis grid
EVIDENCE U3PWD6J3 · SG4IGV3Y · WUPV36YG carry it; XDYU5FSQ, CW9WK9KL support §4        thin: no house data
HOW      hidden-obligations map → contradiction map · surface · 2 passes                    edit ▸
$1.85 · ~18 min      Pick this when a sustainability or values campaign is planned in the next two quarters.
```

The "how" line uses `path.steps[].plain_name`; hovering/expanding reveals `engine_key` and `contributes`. `edit ▸` opens the catalog picker (C, path 2) pre-loaded with this path.

### B4. The Sonnet prompt (v2) — `src/dossier/brief.py`

**System**

```
You are the brief desk of The Analyst. The desk has read a corpus (reconnaissance below) and must offer the requester
exactly THREE DELIVERABLES they could commission — three different USES of the same documents, not three topics and
not three phrasings of one idea. A deliverable is judged by what its reader will UNDERSTAND and be ABLE TO DO
afterwards, and by the honesty of what it will NOT tell them.

Rules (all are checked by code; a violation returns the brief to you for repair):
1. USE FIRST. Each option has one use_kind from the use register. The three use_kinds must differ. If the requester
   stated what they will use the dossier for, all three options serve that use through different deliverables and
   their you_will_be_able_to sets must not overlap. If no use was stated, propose the three uses this corpus and
   this audience most plausibly need, and say in best_when who should pick each.
2. CONCRETE TO THIS MATERIAL. Every you_will_understand line and every you_will_be_able_to line names at least one
   concrete thing from the documents — an entity, a number, a dated event, a verbatim phrase, or a document key in
   square brackets. A line that would still be true of a different corpus is rejected.
3. VERIFIABLE. Every promise carries supported_by: the section (S), table (T) or figure (F) that keeps it. Every
   table declares its row unit ("one row per …") and expected row count; every figure declares its format. A promise
   that no section/table/figure can keep must be dropped, not softened.
4. HONEST SCOPE. not_for states what these documents cannot deliver: house-internal data, forecasts, actors or
   countries not in the corpus, single-source limits, sample sizes. Never promise "where the next move lands" from
   documents that only periodise the past.
5. AUDIENCE REGISTER. Write in the register given below. For executives: no theory vocabulary; use the plain
   equivalents supplied (e.g. "hidden obligation", not "inferential commitment"); plain_name for every engine is
   supplied — use it verbatim. For analysts and researchers the technical names are allowed.
6. TRADE-OFF. The three options must differ in weight: one light (1 engine or 2 at surface, ≤2 tables, ≤1 figure),
   one standard, one full (3–4 engines, 3 tables, 2–3 figures) unless the depth preference forbids it. Cost and
   time are computed by code from your path; do not state prices.
7. ENGINES ARE THE HOW. Choose path.steps only from the executable catalog, in run order, 1–4 steps, no repeats.
   Each step's `contributes` says in reader terms what that step adds to THIS deliverable — never what the engine
   is in general.
8. LENGTHS. deliverable ≤110 chars; understand ≤140; able_to ≤120 and verb-first; questions ≤120; not_for ≤120;
   best_when ≤140; headings ≤70; table titles ≤90; row_unit ≤60. Exactly 3 understand, 2–3 able_to, 3–4 questions,
   1–3 not_for, 3–6 sections, 1–3 tables, 0–3 figures.
9. RECOMMEND. Name the option the material carries best and say why in one sentence the reader would accept
   (what the documents hold, what they lack). Name the runner-up and why.
```

**User (template)**

```
AUDIENCE: {audience} — {AUDIENCE_REGISTER[audience]}
VOCABULARY FOR THIS AUDIENCE (use the right-hand side; never the left):
{vocabulary_lines}                 # ~40 lines from src/audiences/definitions/{audience}.json translations,
                                    # filtered to terms that appear in the catalog problematiques + a fixed list
                                    # (inferential commitment, dialectical, counterfactual, hegemony, discourse,
                                    #  epistemology, genealogy, appropriation, legitimation, neoliberal, …)
ENGINE PLAIN NAMES FOR THIS AUDIENCE:
{plain_name_lines}                 # from src/dossier/catalog_purpose.json (section D), e.g.
                                    # inferential_commitment_mapper = "hidden-obligations map"

USE REGISTER (use_kind → what the reader is trying to do):
  decide       — choose between courses of action; retire/advance something
  brief        — bring a board, a CEO, a committee up to speed for a meeting
  prepare      — get ready for a negotiation, a pitch, a challenge, a hearing
  stress_test  — test our own position or claims before they are attacked
  compare      — set two or more cases/options side by side to choose
  watch        — set up what to monitor and the early signs to look for
  learn        — get up to speed on a field or a set of papers fast
  argue        — build or defend a case with the strongest evidence

REQUESTER'S USE: {use_frame.use_kind or "not stated"} — {intent or "no intent given"}
  occasion: {use_frame.occasion or "—"}   reads it: {use_frame.who_reads or audience}   decision due: {use_frame.decision or "—"}
DEPTH PREFERENCE: {depth} (options may sit one level lighter or heavier when the use demands it)
FIGURES PREFERENCE: {figures}
CORPUS: {n} documents, {chars:,} characters.

RECONNAISSANCE:
{compact_profiles(job.profiles)}          # profiles + corpus_map (shared_questions, disagreements, throughlines,
                                           # candidate_angles) — the candidate_angles are raw material, not options

EXECUTABLE ENGINES (choose path.steps only from these keys; "use when" and "yields" are for you, plain_name is for the reader):
{catalog_purpose_text(catalog, audience)}  # section D one-liners + depths/passes

Propose exactly three options and a recommendation. Return them through the tool.
```

**Tool schema.** `propose_brief` = the JSON Schema of `Brief` (via `schema_of(Brief)` with `_inline_defs`, as the other steps do), with `est_*` removed from the model-facing schema and enums for `use_kind`, `deliverable_kind`, `format`, `depth`.

**Translate mode (path 2, entry = "chosen").** Same system prompt with rule 7 replaced by: *"The path is FIXED: {steps}. Do not change it. Write the ONE option that this path yields for this corpus and audience, then ONE alternative the desk would propose instead (mark it `alternative: true`) with a one-line reason."* Returns two options; `recommendation` is the fixed one unless the desk flags a corpus mismatch (e.g. `chapter_role_analyzer` on a five-paper bundle → `not_for` says so and the recommendation names the alternative, with reason).

### B5. Code-side checks (`brief.py`, run after `call_json`, repair loop once, then fallback)

| Check | Rule | On failure |
|---|---|---|
| use disjointness | three `use_kind`s differ; if `use_frame.use_kind` given, the three `able_to` texts share < 50 % of content words pairwise | repair prompt: "options B and C serve the same use; replace C with a different use from the register" |
| concreteness | each understand/able_to line contains ≥1 doc_key in brackets **or** ≥1 entity from `profiles[].entities` **or** a number/date | repair; after repair, drop the line and log `note` |
| support refs | every `supported_by` resolves to an existing section/table/figure index | repair; else strip the ref and mark the promise `unsupported` (rendered muted) |
| row unit | every table has `row_unit` starting with "one row per" | repair |
| vocabulary | executive: no term from the vocabulary left-hand column appears in reader-facing fields (title, deliverable, promises, questions, not_for, best_when, headings, table titles, plain_name) | repair with the offending terms listed |
| lengths | caps in rule 8 | truncate at word boundary, log |
| engines | keys in executable catalog, unique, 1–4; `plain_name` matches the catalog for this audience (else overwritten) | drop unknown keys; if none left, `deep_summarization` |
| weight spread | at least two distinct `path.depth` values across the three options | no repair; log |
| recommendation | `option_key` exists | fall back to option 1 and note "recommendation missing" |

Estimates (`estimate_option`) run per option from its own `path.depth` and step depths. Everything above is arithmetic and string checks; judgment stays in the model (vision §H8).

### B6. Events

`artifact` payload gains `use_kind`, `deliverable_kind`, `deliverable`, `able_to` (texts), `recommendation` — the console's planner strip can show *"recommended: A — because the corpus carries the legitimacy criteria but no house claims"*.

---

## C. Three entry paths — UI and API

### C1. The three lanes

| Lane | Who | What the brief step shows | Vision anchor |
|---|---|---|---|
| **1. Tell me what you want to use it for** (default) | anyone | three deliverable cards (B3), differing by use, one recommended with a reason | §D4 "give me the right options for the choice"; §H9 ballots |
| **2. I know the analysis I want** | competent user (the visualizer model) | the purpose-first catalog picker → one card for the chosen path + one alternative the desk proposes, each saying what it lets them understand/do | visualizer Engine / Bundle / Pipeline tabs, "AI Recommended (85 %)" with rationale, output-format checkboxes |
| **3. Let the material decide** | the owner with five minutes | the desk chooses and explains why; writes straight through; the brief remains readable with the reason | §H2 back-narrative; §D6 "bother me only for high-value questions" |

Lane 2 is what the visualizer assumed for everyone; lane 1 is what the analyst desk adds; lane 3 is the existing autopilot made accountable.

### C2. What the visualizer did that we keep, and what we change

Kept: a **category-grouped catalog** with one-line purposes and a search box; **bundles/pipelines** as pre-composed sequences ("work well together" / "output of one feeds the next"); an **intent** lane with quick picks ("Map the key players", "Evaluate the strength of arguments", "Compare approaches…"); a **recommendation with a rationale and a confidence badge**; **output modes** chosen next to the engine (visual / smart table / report types, each with a core question: Snapshot "What do I need to know right now?", Gap Analysis "Where are the weaknesses?", Options Brief "What should I choose?").

Changed: the visualizer's groups are *disciplines* (Argument & Reasoning, Concepts & Frameworks, Epistemology…) and its engine cards say what the engine *is*; ours are grouped by *purpose* ("Test a position", "See the structure", "Follow the words", "Read it properly") and say *use when you need to…* and *yields…*. The visualizer's "intent → verb + noun → engine" classifier is replaced by the brief desk itself (LLM-first, no taxonomy code). Output modes are not checkboxes: the option's `shape` declares them and `primitives` records prose / anchored tables / figures.

### C3. API changes

**`POST /v1/dossier/jobs`** (`CreateDossierRequest`)

```jsonc
{
  "sources": [...],
  "entry": "use" | "chosen" | "material",        // default "use"; "material" replaces autopilot:true (kept as alias)
  "intent": "How do fashion brands … where will a house's claims be challenged?",
  "use_frame": {                                   // optional, lane 1
    "use_kind": "stress_test",                     // USE_KINDS or null
    "occasion": "campaign planning, Q4",
    "who_reads": "brand president + comms",
    "decision": "which claims go into the Q4 campaign"
  },
  "path": {                                        // required when entry = "chosen"
    "steps": [{"engine_key": "argument_architecture", "depth": "surface"},
              {"engine_key": "inferential_commitment_mapper", "depth": "surface"}],
    "chain_key": null                              // or a recipe/chain key; steps then filled from it
  },
  "audience": "executive", "depth": "medium", "output": {...}, "spend_cap_usd": null, "image_provider": null
}
```

Validation: `entry` in the enum; `path.steps` keys must be executable and ≤4; `use_kind` in `USE_KINDS`. `DossierOptions` gains `entry`, `use_frame`, `path`.

**`GET /v1/dossier/catalog?audience=executive&corpus_chars=350000`** (new) — the picker's source of truth; purpose-first, from `src/dossier/catalog_purpose.json` (section D) joined with the runtime capability registry (so a missing YAML drops an engine, never a stale entry).

```jsonc
{
  "groups": [
    {"key": "test_position", "title": "Test a position", "purpose": "what can be attacked, what accepting it commits you to",
     "engines": [
       {"engine_key": "inferential_commitment_mapper", "plain_name": "hidden-obligations map",
        "use_when": "you need to know what you are really signing up for if you adopt a position, framework or pledge",
        "yields": "a ledger of explicit → implicit commitments, their conflicts and what depends on what",
        "deliverable_kinds": ["stress_test", "decision_memo"], "row_unit": "one row per commitment",
        "depths": {"surface": {"passes": 1, "est_cost_usd": 0.62, "est_minutes": 6.1}, "standard": {"passes": 2, ...}},
        "pairs_with": ["argument_architecture", "dialectical_structure"],
        "fit": "ok" | "conditional" | "not_for_dossier", "fit_note": "…"}
     ]}
  ],
  "recipes": [
    {"key": "stress_test", "title": "Stress test", "use_when": "…", "steps": ["argument_architecture", "inferential_commitment_mapper"],
     "yields": "claim scorecard + hidden-obligations ledger", "est_cost_usd": 1.3, "est_minutes": 13}
  ],
  "excluded": [{"engine_key": "aoi_thematic_synthesis", "why": "presumes a selected source thinker"}, ...]
}
```

`est_*` per depth are `estimate_engine_run(corpus_chars, passes)` when `corpus_chars` is given (the Library knows it after upload/exemplar choice).

**`GET /v1/dossier/jobs/{id}/brief`** — returns `Brief v2` (`entry`, `options[]`, `recommendation`, `defaults`, `chosen_option`, `status`). Old clients still find `telling`, `engines`, `output_shape` on each option (computed fields serialise).

**`POST /v1/dossier/jobs/{id}/brief`** — unchanged body `{option_key, overrides}`; `overrides.path` (edited steps from the card's "how ▸ edit") is accepted and stored on the chosen option before planning.

**`POST /v1/dossier/jobs/{id}/brief/rewrite`** `{audience}` (step 4, optional) — re-runs the brief for another audience (~$0.06, ~45 s), keeps the same paths; the dial "Written for" on the brief step calls this instead of silently changing downstream register only.

**`POST /v1/dossier/brief/preview`** `{sources|job_id, path, audience}` (step 4, optional) — translate mode without creating a job, for the picker's live card.

**Runner** — `entry == "material"`: after the brief, `chosen_option = brief.recommendation.option_key`; event `note`: *"the material decided: A — because …"*. `entry == "chosen"`: brief runs in translate mode; `plan.py` keeps the fixed steps (no engine choice by Sonnet; Sonnet still writes `context_emphasis` per step and the `strategy_rationale`).

### C4. BriefStep layout

- **Header.** "The brief" · eyebrow *"3 deliverables · your choice"* (lane 1) / *"your path + the desk's alternative"* (lane 2) / *"the material decided"* (lane 3, with the reason under it).
- **Lede.** *"Each card says what you get, what you will understand and what you will be able to do. Pick by use; the how is underneath."*
- **Cards** (grid of three, B3 anatomy). `role=radio`. The recommended card wears the reason, not just a badge. `NOT FOR` is always visible (never behind a disclosure). `SHAPE` and `EVIDENCE` are one-line strips with a ▸ disclosure listing tables (title — row unit — rows) and figures (title — format). Promise refs (`T1`, `§5`, `F1`) are chips; hovering highlights the row in the shape disclosure.
- **How line.** `plain_name → plain_name · depth · N passes` in the machine font; `edit ▸` opens the picker drawer (C5) with the path loaded; on save the card's price re-computes (`estimate_option`) client-side from the catalog's per-depth estimates and is confirmed by the server on choose.
- **Dials panel → two dials.** *Figures* (0–4) and *Written for* (audience; changing it offers *"Rewrite the cards for an analyst · ~$0.06"*). Depth leaves the dials: it lives on each card's how-line.
- **Under the cards.** A quiet link: *"I know the analysis I want ▸"* opens the picker (lane 2) inside the step; the result appears as a fourth card "Your own path" via translate mode.
- **Dock.** `OutcomeButton` unchanged: *Write the draft · $1.85 · ~18 min · every step recorded*. Subline adds the chosen option's `deliverable`.

### C5. The catalog picker (`web/src/components/CatalogPicker.tsx`, used by Library and BriefStep)

- Left rail: groups (D) as tabs with counts; search box; a *"recipes"* tab (pre-composed paths).
- Engine card: `plain_name` (serif), `use_when` (the one-liner), `yields`, depth chips with passes + price on this corpus, `pairs with` chips, `fit` flag (`conditional` shows its note; `not_for_dossier` engines are listed greyed at the bottom with the reason — the competent user should see what exists and why it is off).
- Right: "Your path" — ordered steps (drag to reorder, depth per step), running estimate, and a live translate-mode preview card (step 4) or the promise *"the brief will say what this path lets you understand and do"* (step 3).

### C6. Library dials (≤5 decisions, no trivial defaults)

Replace the four dials + autopilot with:

1. **The use box** (primary, above the dials): *"What will you use this dossier for?"* — free text (`intent`) + use chips (`use_kind`: Decide something · Brief someone · Prepare for a meeting/negotiation · Stress-test our position · Compare cases · Watch for what's coming · Learn the field fast · Build an argument). Optional inline fields on chip selection: *occasion*, *who reads it*, *decision due*.
2. **Written for** (audience).
3. **Lane** (radio): *Propose deliverables* (default) · *I'll pick the analysis* (reveals the picker) · *Let the material decide*.
4. **Advanced** (collapsed `<details>`): depth preference, figures, spend cap, image provider.

Start button copy per lane: *"Start · you'll choose a deliverable"* / *"Start · your path, then the brief"* / *"Start · the desk chooses and explains"*.

### C7. Determinism ledger (vision §H8)

LLM decides: the three uses, deliverables, promises, shape, evidence base, path, recommendation, plain-language copy. Code decides: catalog membership, counts and caps, price/time arithmetic, reference resolution, vocabulary ban-list, disjointness measure, fallbacks. No regex meaning-classifiers; the use register is a vocabulary, not a router.

---

## D. The engine catalog presented by PURPOSE (28 executable engines)

Source for each line: the YAML `researcher_question`, `problematique`, `analytical_dimensions`, `composability.synergy_engines`, `depth_levels` in `src/engines/capability_definitions/`. `plain_name` is the executive register; analysts/researchers see the engine name. This table is the content of the proposed `src/dossier/catalog_purpose.json`.

### D1. Test a position — what can be attacked, what accepting it commits you to

| engine_key | plain name | use when you need to… | yields (deliverable) | row unit | fit |
|---|---|---|---|---|---|
| `argument_architecture` | claim scorecard | know where an argument is strong and where it can be attacked — the hidden premises, the weak joints, who bears the burden of proof | claim-by-claim scorecard (claim · evidence · unstated premise · weak joint · attack) | one row per major claim | ok |
| `inferential_commitment_mapper` | hidden-obligations map | know what you are really signing up for if you adopt a position, a framework, a pledge | ledger of explicit → implicit commitments, their conflicts, what depends on what, the practical "so what" | one row per commitment | ok |
| `dialectical_structure` | contradiction map | see the tensions a discourse cannot resolve, which side secretly depends on the other, and what it cannot think | map of tensions (tension · positions · what each excludes · how it plays out) | one row per tension | ok |
| `counterfactual_analyzer` | what-if audit | test claims that rest on "had X not happened…" — which what-ifs hold and which are rhetoric | audit of each counterfactual (the world it assumes · the causal chain · plausibility · abuse pattern) | one row per what-if claim | ok |
| `modal_reasoning_analyzer` | certainty ledger | know which "must / cannot / could" claims are real necessities and which are emphasis | inventory of necessity/possibility claims with their backing and confusions | one row per must/could/can't claim | ok |

### D2. See the structure — the template that repeats, the ideas that hold it up

| engine_key | plain name | use when you need to… | yields | row unit | fit |
|---|---|---|---|---|---|
| `structural_pattern_detector` | pattern map | have several cases or texts and need the one template that repeats across them (and where each case departs from it) | the template's stages with every case mapped onto them; departures flagged | one row per case × stage | ok |
| `concept_centrality_mapper` | load-bearing ideas | know which ideas hold the whole thing up — remove it and the argument collapses | ranking of concepts by what depends on them; hub/bridge topology | one row per concept | ok |
| `concept_taxonomy_argumentative_function` | vocabulary decoder | know what job each key term is doing (foundation, defence, bridge, conclusion) and where the argument is thin | term-by-job table + vulnerability points | one row per key term | ok |
| `conceptual_framework_extraction` | lens inventory | know which frameworks and lenses the material thinks with, and what each lets you see and not see | inventory of frameworks (where used · what it shows · what it hides · where it came from) | one row per framework | ok |
| `comparative_reasoning_analyzer` | comparison audit | the material argues by comparison (A vs B, typologies, scales) and you need to know whether the comparisons hold | audit of each comparison (what is transferred · where it breaks · would other criteria reverse it) | one row per comparison | ok |
| `theory_construction_analyzer` | theory build map | know how a theory was assembled — borrowed pieces, innovations, how it touches evidence | build map of the theoretical framework | one row per building block | researcher/analyst-leaning |
| `specialized_reasoning_classifier` | reasoning toolkit | know the kinds of reasoning a text relies on (probabilistic, strategic, normative…) and how rigorously | inventory of reasoning forms with rigor notes | one row per reasoning form | researcher-leaning; rarely an executive deliverable |

### D3. Follow the words — how terms move, get captured, change meaning

| engine_key | plain name | use when you need to… | yields | row unit | fit |
|---|---|---|---|---|---|
| `concept_evolution` | term trajectory | the same term appears across documents or years and you need to know how its meaning shifted | trajectory table (term · meaning in A · meaning in B · what changed · what it now licenses) | one row per term × document | ok on corpora; designed for prior/current work of one author |
| `concept_appropriation_tracker` | capture register | know who took a term and bent it to their purposes — co-optation, capture, borrowed authority | register of appropriations (term · origin · who uses it now · how it was bent · acknowledged?) | one row per term | ok |
| `concept_semantic_constellation` | word-field map | one concept is central and you need its whole neighbourhood — near-synonyms, opposites, boundary cases | field map for 3–5 concepts | one row per related term | ok |
| `concept_synthesis` | one picture of the ideas | you have per-document concept readings and need one cross-document picture with a verdict | unified concept picture + convergence/divergence + verdict | one row per concept | **conditional** — synthesis pass; needs prior phases |
| `evolution_tactics_detector` | line-change tactics | an author or organisation changed its line and you need to see how the change was managed (silent revision, reframing, disavowal) | tactic catalogue with evidence | one row per tactic instance | **conditional** — presumes the same author across time (e.g. successive annual reports); off for mixed-author bundles |

### D4. Read it properly — what a text argues, how it is built, what it hides

| engine_key | plain name | use when you need to… | yields | row unit | fit |
|---|---|---|---|---|---|
| `deep_summarization` | reading guide | know what each document actually argues, how, and what it foregrounds or suppresses — and, as a last pass, one synthesis across the phases | per-document argument map (thesis · moves · evidence · what is suppressed · key vocabulary) | one row per document | ok; also the default synthesis engine |
| `narrative_structure_analyzer` | story shape | how the story is told matters — voice, arc, what the sequencing does to the reader | story-shape reading per document | one row per document | ok |
| `epistemological_method_detector` | how-they-know audit | know how the authors claim to know what they claim — methods, standpoint, self-awareness — before you rely on them | credibility grounding per document | one row per document | ok; analyst/researcher-leaning |
| `conditions_of_possibility_analyzer` | what-had-to-be-true | know what had to be in place for this argument or practice to emerge, and what it forecloses | enabling/constraining conditions + paths not taken | one row per condition | **conditional** — designed around an author's prior work; usable at surface on a corpus |
| `chapter_role_analyzer` | chapter map | a single long work (book, long report) needs a map of what each part does and depends on | chapter role map with dependencies and weak points | one row per chapter | **conditional** — single long work only; off for multi-paper bundles |

### D5. Not for a document dossier (listed greyed in the picker, with the reason)

| engine_key | why not |
|---|---|
| `aoi_thematic_synthesis`, `aoi_engagement_mapping`, `aoi_sin_findings`, `aoi_thematic_report` | presume a *selected source thinker* and a *subject author* (Anxiety-of-Influence workflow); no such structure in a corpus dossier — already excluded by `EXCLUDED_PREFIXES` |
| `genealogy_relationship_classification`, `genealogy_final_synthesis` | presume an author's *prior works* discovered and classified upstream — already excluded |

Conditional flags (D3/D4) are new: today `engine_catalog()` offers all 22 non-excluded engines to the brief unconditionally; `catalog_purpose.json` carries `fit` + `fit_note`, and the brief prompt is told which are conditional for *this* corpus (single vs multiple documents, one author vs many — both known from reconnaissance profiles).

### D6. Recipes (pre-composed paths for lane 2; `src/dossier/recipes.json`)

Only fully executable sequences. Existing chains that qualify: `deep_text_profiling` (3), `genealogy_target_profiling` (4), `genealogy_synthesis` (4), `genealogy_prior_work_scanning` (2), `prior_work_profiling` (2), `logical_architecture_analysis` (10 — too heavy; offered as "full read" subset). All other 21 chains in `src/chains/definitions/` reference non-executable engines (0–2 of 5 executable) and must not be shown.

| recipe | steps | use when | yields |
|---|---|---|---|
| Stress test | `argument_architecture` → `inferential_commitment_mapper` | our position will be attacked | claim scorecard + hidden-obligations ledger |
| Pattern & playbook | `structural_pattern_detector` → `concept_taxonomy_argumentative_function` | several cases; need the template and the words that sell it | pattern map + vocabulary decoder |
| Two-case comparison | `comparative_reasoning_analyzer` → `counterfactual_analyzer` | choose between cases or learn from a contrast | comparison audit + what-if audit |
| Vocabulary decoder | `concept_evolution` → `concept_appropriation_tracker` | terms are moving or being captured | trajectory table + capture register |
| Reading guide | `deep_summarization` | new to the field; onboard a team | per-document argument maps |
| Credibility read | `epistemological_method_detector` → `argument_architecture` | before relying on the sources | how-they-know audit + claim scorecard |
| Full read | `deep_summarization` → `argument_architecture` → `dialectical_structure` → `deep_summarization`@synthesis | advanced depth; a report that will be reread | reading guide + scorecard + contradiction map + synthesis |

Deliverable kinds ↔ typical engines (used by the prompt as hints, not rules): stress_test → D1; playbook/decoder → `structural_pattern_detector`, `concept_taxonomy_argumentative_function`, `concept_appropriation_tracker`; decision_memo → `inferential_commitment_mapper` + `counterfactual_analyzer`; comparison → `comparative_reasoning_analyzer`; watchlist → `concept_evolution` + `inferential_commitment_mapper`; reading_guide → `deep_summarization` (+ `conceptual_framework_extraction`); risk_register → `structural_pattern_detector`; briefing → any D1/D2 pair at surface; case_file → `deep_summarization` + `argument_architecture`.

---

## E. Implementation map (smallest viable first) and three test briefs

### E1. Steps

**Step 0 — prompt-only lift (½ day, no schema break).** `src/dossier/brief.py`: rewrite `SYSTEM` with rules 1–5 and 9; add optional fields to `OPTION_SCHEMA` and `BriefOption` (`use_kind`, `deliverable`, `you_will_understand: list[str]`, `you_will_be_able_to: list[str]`, `not_for: list[str]`, `best_when`), and `recommendation` to `BRIEF_SCHEMA`/`Brief`; load the audience vocabulary lines (`src/audiences/registry.py:get_vocabulary_guidance` / `translate_term`) into the user prompt. `runner.py:159` uses `recommendation.option_key`. `BriefStep.tsx` renders the new fields above the engine chips when present; `api.ts:normalizeBriefOption` passes them through. Result: cards lead with use in the next run, with no downstream change.

**Step 1 — `BriefOption v2` (1–2 days).** `schemas.py` as in B2 with computed back-compat fields; `brief.py` full prompt (B4), tool schema from `schema_of(Brief)`, checks (B5), per-option estimates from `path.depth`; `common.py`: `USE_KINDS`, `catalog_purpose_text()`, vocabulary loader; new `src/dossier/catalog_purpose.json` (D) + `recipes.json` (D6); events payload (B6). `tables.py`/`figures.py`/`compose.py` read `shape.tables[].row_unit` / `figures[].format` / `sections[].answers` (tiny edits; the back-compat strings still work meanwhile). Tests: `tests/test_dossier_brief_v2.py` — v2 fixture validates; `telling`/`engines`/`output_shape` computed correctly; each B5 check on a bad fixture; estimates differ across depths.

**Step 2 — front end v2 (1–2 days).** `types.ts` (`BriefOption` v2, `Recommendation`, `Brief.entry`), `api.ts` (`normalizeBriefOption` v2 with v1 fallback), new `components/DeliverableCard.tsx`, `BriefStep.tsx` (C4), `styles.css` (card blocks; keep `.move/.telling` tokens), `web/mock/brief.json` v2 fixture + `mock.ts`. Playwright: cards render promises with refs, NOT FOR visible, recommended reason shown, choose → planning. **Mandatory Playwright pass before declaring done.**

**Step 3 — lanes + catalog (2 days).** `schemas.py`: `DossierOptions.entry/use_frame/path`, `CreateDossierRequest` same; `api/routes/dossier.py`: validation, `GET /v1/dossier/catalog`, brief GET returns `recommendation`; `brief.py` translate mode; `plan.py`: when `job.options.path` is set, phases = the fixed steps (Sonnet writes `context_emphasis` + `strategy_rationale` only; `_enforce_policy` respects the given depths); `runner.py` lane semantics (C3). Front end: `Library.tsx` (C6 use box, lane radio, advanced details), `components/CatalogPicker.tsx` (C5), BriefStep "edit ▸" and "I know the analysis I want ▸". Tests: catalog endpoint lists 22 engines with `fit`, 6 excluded with reasons, recipes all-executable; `POST /jobs` rejects a non-executable path; plan honours a chosen path exactly.

**Step 4 — polish (later).** `POST …/brief/rewrite {audience}`, `POST /v1/dossier/brief/preview`, live preview card in the picker, `not_for` learning loop (recurring `not_for` lines become reconnaissance prompts — vision §H10).

Files, in order: `src/dossier/brief.py` → `src/dossier/schemas.py` → `src/dossier/common.py` → `src/dossier/catalog_purpose.json`, `src/dossier/recipes.json` (new) → `src/dossier/runner.py` → `src/dossier/plan.py` → `src/dossier/tables.py`, `figures.py`, `compose.py` → `src/api/routes/dossier.py` → `web/src/types.ts` → `web/src/lib/api.ts` → `web/src/components/DeliverableCard.tsx`, `CatalogPicker.tsx` (new) → `web/src/steps/BriefStep.tsx` → `web/src/pages/Library.tsx` → `web/src/styles.css` → `web/mock/brief.json`, `web/src/lib/mock.ts` → `tests/test_dossier_brief_v2.py`, `tests/test_dossier_catalog.py` → `docs/FEATURES.md`, `docs/CHANGELOG.md`, `communications/changes/dossier.md`, `web.md`.

### E2. Test briefs — expected option texts (abridged cards; the shape lines are the verification targets)

Prices are illustrative from `estimate_engine_run` on the real corpus sizes (fashion 349K chars; Kering ≈ 60K; state-capitalism 270K); the point is that they differ.

#### E2.1 Fashion bundle (5 papers; intent "How do fashion brands legitimate themselves under sustainability and platform pressure, and where will a house's claims be challenged?"; executive)

**A · stress_test · "Where your sustainability claims will break"** — recommended.
Deliverable: *A 5-section stress test of the four claim types a house makes, with a scorecard of what each commits you to and what breaks it.*
Understand: (1) the two ways a claim fails for consumers — no link to brand history (illegitimacy) and a visible commercial motive (opportunism) — as the 12 interviewees described them [U3PWD6J3]; (2) for each of the 10-R practices (reduce, reuse, repair, recycle…), the market counter-move that turns it back into a sales story [SG4IGV3Y]; (3) how a hashflag-style gesture is withdrawn the moment it collides with commercial interest, and what that does to trust [WUPV36YG].
Able to: decide which claim types to advance and which to retire before the next campaign (T1); set the evidence a claim needs before launch — a brand-history anchor and a multi-action record (T3); brief comms on the three questions an investigation will ask (§5).
Not for: it does not score the house's own claims — none are in these documents; it scores claim types. Consumer evidence is 12 interviews. Bring the house's claims to a follow-up run.
Shape: 5 sections; T1 one row per claim type (4–6) · T2 one row per 10-R practice (10) · T3 one row per claim category (3–4); F1 two-axis grid (brand-cause link × visible commercial motive).
Evidence: U3PWD6J3, SG4IGV3Y, WUPV36YG carry it; XDYU5FSQ, CW9WK9KL support §4. How: hidden-obligations map → contradiction map · surface · 2 passes. ≈ $1.85 · ~18 min. Best when a sustainability or values campaign is planned in the next two quarters.
Recommendation reason: *the papers carry the legitimacy criteria and the counter-moves in full; they carry no house data, so the stress test is the deliverable they can keep honestly.*

**B · brief · "The Shein benchmark your sourcing story is judged against"**
Deliverable: *An ExCo briefing on how ultra-fast platform retail resets the yardstick for a sourcing story, with an exposure register.*
Understand: (1) what Shein's designer-cum-buyer scoring does to supplier margins and speed — 2,000+ new styles a day [XDYU5FSQ] — and why watchdogs now use it as the benchmark; (2) that supply-chain scrutiny is the largest cluster in 890 sustainable-fashion papers, 2000–2023 [CW9WK9KL] — where the attention already sits; (3) which circular practices platform consumption velocity hollows out [SG4IGV3Y].
Able to: name the three disclosures a credible sourcing story now needs (T2); rank where the house is most exposed against the benchmark (T1); decide whether traceability and third-party verification spend is a defence or a distraction (§6).
Not for: no house supply-chain data; not a forecast of Shein's next move; the Shein evidence is one case study.
Shape: 6 sections; T1 one row per exposure point (6–8) · T2 one row per disclosure (3); F1 flow (designer-cum-buyer → scoring → subcontractor margin). How: pattern map → comparison audit · surface. ≈ $1.60 · ~16 min. Best when someone will ask "how do we compare to Shein" at the next ExCo.

**C · learn · "The five papers in one hour"** — light.
Deliverable: *A reading guide: what each paper argues, where the five disagree, and the eight terms you will hear, in plain words.*
Understand: (1) the five theses, one page each — from "sustainability and capitalism are rivals" [SG4IGV3Y] to "brand activism can be a genuine compromise" [U3PWD6J3]; (2) the four disagreements (compatible or not; genuine or performative; harm to workers or to consumers; who leads the agenda); (3) the decoder: legitimation narrative, spatial-digital fix, platformed solidarity, economies of worth, 10-R, greenwashing/woke-washing.
Able to: onboard a team in an hour (§1–§5); choose which paper to send to whom (T1); spot when a consultant reuses one of these frames (T2).
Not for: no recommendation about the house; no ranking of risks.
Shape: 5 sections; T1 one row per paper (5) · T2 one row per term (8); no figure. How: reading guide · surface · 1 pass. ≈ $1.10 · ~10 min. Best when you are new to the topic or building a team.

#### E2.2 Kering study (1 document; intent "Read Kering's public record for where its meaning system is under strain and what a strategy decision should watch"; executive; simple)

**A · prepare · "The half-sentence that opens the pitch"** — recommended.
Deliverable: *A pre-meeting card: where de Meo's AI programme stops, the opening line in his own words, and the two things not to say.*
Understand: (1) what the stack already covers — Chief AI Officer, Google partnership, Gucci as "first laboratory" — and the layer it lacks; (2) which of de Meo's quotes point at that layer ("help the creative people get better, faster, stronger"); (3) why product, CRM and finance tooling cannot close it.
Able to: open with de Meo's words (§3); avoid the two misfires — platform logic against luxury singularity, front-facing AI after the Valentino ridicule (T2); position the offer above the stack, not beside it (§5).
Not for: single-source memo — its facts are its own; no financial modelling; no view on competitors beyond the LVMH "quiet tech" line.
Shape: 5 sections; T1 one row per stack layer (5–6) · T2 one row per de Meo quote (6); F1 stack. How: load-bearing ideas · surface · 1 pass. ≈ $0.45 · ~6 min. Best when the meeting is this week.

**B · argue · "Four handovers, no bridge"**
Deliverable: *A risk register of four creative-director handovers in 18 months, in operational-risk language, for a board conversation.*
Understand: (1) what each handover resets and what the memo says it costs in cultural relevance; (2) Gucci from De Sarno's exit to Demna with no instrument holding what Gucci means in between; (3) what a "house ontology" would have preserved at each of the four transitions.
Able to: state the exposure per house (T1); argue for a continuity instrument in risk terms (§4); pre-empt "this is just bad luck" (§1).
Not for: no revenue attribution per handover — the memo does not carry it; no view inside the houses.
Shape: 5 sections; T1 one row per handover (4) · T2 one row per reset cost vs instrument cost (4); F1 timeline. How: pattern map · surface. ≈ $0.45 · ~6 min. Best when the audience is the board or the CFO.

**C · decide · "Own the discourse or keep renting it"**
Deliverable: *A decision memo on Gucci's China problem: keep paying the platform tax on Gucci's meaning, or instrument the discourse.*
Understand: (1) the Q1 2026 filing's own phrase — "low cultural relevance" — and why it is not a product or CRM signal; (2) Demna's "I want Gucci to be a feeling" against where the feeling is currently made (Xiaohongshu, resale); (3) who extracts value from Gucci's meaning today and how.
Able to: rule out the product/CRM/distribution diagnoses (T1); name the actors and mechanisms taking the value (T2); choose between the two courses with their preconditions (§5).
Not for: no China market data beyond the memo; no platform economics.
Shape: 5 sections; T1 one row per diagnosis (4) · T2 one row per platform/actor (4–5); F1 flow. How: capture register · surface. ≈ $0.45 · ~6 min. Best when the China question is on the agenda.

#### E2.3 State-capitalism bundle (5 papers; **no intent given**; executive; medium) — the desk proposes the uses

**A · prepare · "Recognise the playbook when it is offered to you"** — recommended.
Deliverable: *A five-case playbook: the four-stage template (announce → national-interest framing → corporate beneficiary → community promise) with a decoder for the words that sell it.*
Understand: (1) the same template across Greece/Microsoft, AUKUS, Canada's BDC, France/ASN and CFIUS; (2) who captured the benefit in each — Microsoft, Lockheed Martin, Andreessen Horowitz, HMN Tech, BDC — against what was promised (300 jobs announced; ~12 FTE per data centre in Greece's own paperwork); (3) what "national security", "modernisation" and "strategic partnership" license and what they foreclose.
Able to: tell which stage a government proposal is at (T1); ask the three questions before signing a "strategic partnership" (§5); brief legal on which terms carry hidden obligations (T2).
Not for: no forecast of which sector is next; academic sources 2020–2024; no country outside the five.
Shape: 5 sections; T1 one row per case × stage (5×4) · T2 one row per term (5–6); F1 flow (money from announcement to named firm) · F2 before/after (headline jobs vs FTE). How: pattern map → vocabulary decoder · surface · 2 passes. ≈ $1.55 · ~18 min. Best when a government or agency is courting the house.
Recommendation reason: *five cases with a repeating structure is exactly what the pattern map is for; the papers name beneficiaries and figures, so the playbook can be filled without inference.*

**B · decide · "Be France, not Greece"**
Deliverable: *A leverage checklist from the France–Greece contrast: the conditions under which a firm or a state can hold its ground in a government partnership.*
Understand: (1) France nationalised Alcatel Submarine Networks because it already owned the chokepoint; (2) Greece conceded land, regulation and training because it had to bargain for one; (3) the difference is pre-deal asset position, not politics — and what Egypt, India and Singapore as network hubs add.
Able to: score a prospective partnership on the leverage indicators (T2); set walk-away conditions (§5); recognise the "pathological symbiosis" trap early (§3).
Not for: it will not tell you about a country not in these papers; the France and Greece cases are single studies.
Shape: 5 sections; T1 one row per case (2 + 4 secondary) · T2 one row per indicator (6–8); F1 spectrum · F2 timeline (ASN). How: comparison audit → what-if audit · surface. ≈ $1.55 · ~18 min. Best when you are deciding whether to enter or hold a government-backed deal.

**C · watch · "The screening perimeter around your inputs"** — full.
Deliverable: *A watch-list on investment screening: how the perimeter grew from CFIUS 1975 to today's connector-country pressure, and which luxury-adjacent inputs sit inside it.*
Understand: (1) screening was built against competitors, not spies — Japanese autos and semiconductors in 1975; (2) connector countries (Vietnam, Indonesia, Morocco, Mexico) are being pressed on nickel, EV batteries and electronics; (3) AUKUS Pillar II export controls now reach civilian conglomerates and venture funds.
Able to: list the materials and manufacturing steps under review in the markets named (T1); set a watch cadence on the regimes named, with the signals to look for (T2); brief M&A on screening risk before a cross-border deal (§5).
Not for: no prediction of the next boundary move — the papers periodise, they do not forecast; no legal advice.
Shape: 5 sections; T1 one row per input/step (8–10) · T2 one row per regime (5) · T3 one row per period (5); F1 map · F2 timeline. How: term trajectory → hidden-obligations map → reading guide@synthesis · standard · 5 passes. ≈ $3.20 · ~34 min. Best when cross-border sourcing or M&A is on the 18-month plan.

(Against the live brief: A is what the desk actually ran, now framed by use; C's *not_for* retracts the live promise "tells executives where the next boundary moves are likely to land".)

### E3. Acceptance tests for the redesign

1. Three cards, three different `use_kind`s; when `use_frame.use_kind` is given, `able_to` sets are disjoint.
2. Every `able_to` line has a resolvable ref; every table has a `row_unit`; every figure a `format`.
3. Executive cards contain none of the vocabulary file's left-hand terms.
4. Three different prices in a medium-depth brief.
5. `recommendation.because` names a corpus reason (mentions a doc key or an entity).
6. Lane 3 chooses `recommendation.option_key` and the event says why; lane 2 plans exactly the chosen steps.
7. Playwright: Library use box → brief cards → choose → planning; picker → own path → translated card; the reason under "recommended".

### E4. Open questions for the owner

- Should the audience be chosen before the brief (as now) or should the brief always be written for the executive register and rewritten on demand? (Rewrite costs ~$0.06.)
- Is `not_for` allowed to *propose* the follow-up ("bring the house's claims to a second run") — a commission loop — or should it only state limits?
- Recipes: hand-curated (D6) or minted from recurring chosen paths (vision §H10)?
