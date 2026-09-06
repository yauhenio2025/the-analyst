# What else in Stacks is an engine? A survey of the codebase against the Mastermind's definition (6 Sep 2026, 15:00)

Asked by Evgeny after the integration memo (`INTEGRATION_stacks_citation_universe_2026-09-06.md`) named the three citation lenses as engines:
"study the rest of our codebase to see what might be a good candidate for an engine as defined by the mastermind, beyond just these three".

**The definition used** (the Mastermind's memo §2–§3): an engine answers ONE question over a corpus by a method with **document dimensions** (what
is extracted per document, in parallel, on the cheap tier) and a **corpus dimension** (what is said across them), every finding a row in a **ledger**
with a verbatim **anchor** and a document key, a **critic** ruling on every row against the sources, tables lifted from the ledger, a cross-check,
a validation harness, and a place in the catalogue where a dossier's planner can choose it. Checked against the live catalogue this afternoon
(`GET /v1/operationalizations/`: 277 engines in 24 families — concepts 56, rhetoric 21, temporal 17, epistemology 16, scholarly 15, methodology 14,
argument 12, quality 12, search 11 …) so that nothing below duplicates what exists.

## 1. The inventory: 35 model-facing methods in Stacks, in four kinds

| kind | methods (file · prompt) | verdict |
|---|---|---|
| **A. text-facing readers with structured findings and loci** | the work profile (`profiles.py` SYSTEM · `WorkProfile`), the citation extractor (`cites_extract.py` EXTRACT_PROMPT · `Chunk`), the memo lane's four (`cites_memo.py`), the citation explanations (`cites_context.py` SYSTEM / ACROSS_SYSTEM), the digest of a conversation (`digest.py` · `Digest`), the memo across sources (`digest_pool.py` · `Across`), the fact-check of a memo (`digest_check.py` · `Check`), the memo index (`kinds.py` SEMANTICS_SYSTEM · `Semantics`), the thinker synthesis (`semantics.py` SYNTH_SYSTEM · `Synthesis`), the drain's reading of an arrival (`drain.py` RULES · `Reading`), the exchange's reading of an answer (`exchange.py`), the hunch's speculation run (`hunches.py` → `runs.py`), the runs lane's protocols (`runs.py`, the Mastermind's own engines run by a subscription worker with a code verifier) | **the candidates** (§2) |
| **B. judges that SELECT from a corpus** | the assembler's judge, curate and sort (`assemble.py` JUDGE / CURATE / SORT), populate's judge (`populate.py`), the reciprocal-citation judge (`cites_reciprocal.py` JUDGE), the reception judge (`cites_materials.py` JUDGE), the recordings judge (`media/judge.py`), the editions and dedupe judges, the kind gate (`kinds.py` KIND_SYSTEM) | not engines: reconnaissance and search (their `search` and `analyst_reconnaissance` families); one of them matters for the bridge (§3) |
| **C. bibliographic and rendering plumbing** | verify / harmonize / suggest (`verify.py`, `harmonize.py`, `llm.py`), the TOC readers (`sections.py`, `mecw.py`, `chapters.py`), the author-merge judge, bylines, transcript polish, dictation, the vision read of a photographed page (`capture.py`) | no |
| **D. writing desks** | the essay over the citation tables (`cites_essay.py`), the Brief's compose (`briefs.py`), a section drafted alone (`outline.py`), Ask the corpus (`ask.py`) and Ask the Brief (`ask_brief.py`), the pad's placement suggester (`pad.py`) | desks, not engines (their `composition` family); §3 notes the one worth exporting |

## 2. The candidates, ranked

Ranked by: faces the text, demands verbatim anchors with loci, has ground truth (real runs Evgeny read), and is NOT in the 277.

### 1. Fidelity of a synthesis to its sources — `app/digest_check.py` (the strongest)
- **Question**: is every statement of this memo supported by the sources it cites? **Documents**: the memo (its statements as a NUMBERED list made by
  code — `statements_of_shape`, never by the checker, because Sonnet counted 54 one run and 22 the next) and the sources' full texts labelled as the
  memo cites them. **Document dimension**: one verdict per statement — supported · partly · unsupported · misattributed — with a verbatim passage
  ≤ 300 chars and its `[p. N]` locus, or the nearest thing the source says. **Corpus dimension**: misreadings (a source read against its grain
  though the words hold), omissions (what the sources say that the memo leaves out), a summary of the kind of slips.
- **What exists**: calibrated on em:U3HITB25 (Sonnet 5 found 8 partly + 1 unsupported + 3 misreadings where Gemini Flash passed 59/59; 33 ¢ vs
  10 ¢); every run kept, a run promotable to the record's verdict; the record's "Checked" row; the pile's `check` notice; runs by itself at the end of
  every pool.
- **Against the catalogue**: `analyst_crosscheck` and the `quality` family judge a dossier's own coherence; nothing takes a finished synthesis and
  a set of full source texts and verdicts a code-made statement list. This is the critic pass the memo says the shape provides, as an engine of its
  own — usable on the Mastermind's own dossiers.
- **What the shape adds**: parallel per-statement extraction, a second critic on the verdicts, tables (verdict × section), the harness. **What Stacks
  provides**: the statement list, the source texts by uid, the memo's markers.

### 2. The work profile — `app/profiles.py` (the document engine every dossier starts from)
- **Question**: what does this work argue? **Document dimensions**: thesis, question, tradition, object, period, cases; concepts with weight and
  whether the work DEFINES them (with the definition passage); people with a role (builds-on · criticizes · responds-to · subject · ally ·
  comparison · evidence · cites) and what the work says of them; works cited with a role and a locus; 6–16 claims with kind, locus, what they argue
  against, strength; positions in named debates; sections with pages; 4–10 verbatim passages; relations (uses · extends · criticizes · rejects …).
  Parts of a long book profiled separately and rolled up (`ROLLUP`). **Corpus dimension**: `semantics.aggregate` per thinker (the person facets,
  the concept pages, "engaged by").
- **What exists**: 174 works profiled at 1–3 ¢ (Luna); the work layer's roles feed the citation universe's People table and the assembler; the
  4 Sep design memo (`direct-analysis`) priced the corpus pass at ≈ $460.
- **Against the catalogue**: the Mastermind's reconnaissance "profiles the sources", and `argument_architecture` / `assumption_excavation` read one
  text's argument; none carries the claims-with-loci + roles + relations shape that makes the profile a reusable ledger. **Caveat**: the passages
  and loci are NOT verified by code today (the memo lane's `verify_quote` is; the profile's is not) — the first thing to add before it is an engine.
- **Why it matters for the bridge**: a dossier over a bundle we profiled can start from the profiles instead of re-reading; the profile IS the
  document dimension of half the scholarly family.

### 3. An arrival read against a standing argument — `app/drain.py` (unique; the desk's own engine)
- **Question**: how does this new text bear on the position the scholar holds? **Documents**: one arrival (a capture, a dictation, a run's report,
  a conversation, a memo) and the Brief's numbered claim ledger + open and declined proposals. **Document dimensions**: `kind` (thesis · question ·
  example · evidence · reminder · run_request · correction · noise); claims in HIS words, each with a relation to an existing claim — supports ·
  complicates · answers · contradicts · extends · restates (a restatement is linked, never filed twice); `changes_position` with one sentence.
  **Corpus dimension** (over the Brief): at most one proposal that would change the argument (run · check · read · draft · acquire), deduped against
  the declined, when it should come back (next_session · when_run_done · when_drafting · never).
- **What exists**: ~40 readings on Brief 1 by the subscription workers (Fable/Codex, 50–550 s, $0 marginal); the standing rules (`RULES`), the
  reading of a run's whole report and ledger; the question loop (`reask_after_run`); the resurfacing.
- **Against the catalogue**: the `argument` and `vulnerability` families read a TEXT; nothing reads a text against a ledger of someone's claims. This
  is the engine the meaning-making memo asked for (rules 1/2/6) and it exists only here. **What Stacks provides**: the claim ledger as a source
  (`brief_claims` with layers, `claim_links`), the declined list. **What the shape adds**: the critic on each relation (does the arrival really
  contradict claim 62?), the harness over the 40 readings as ground truth.

### 4. The hypothesis test — `app/hunches.py` + `app/speculate.py` over `app/runs.py`
- **Question**: does this hunch hold against the texts? **Documents**: the bundle the assembler builds from the hunch (the named thinkers' texts on
  the terms, the named works resolved locally, the Referee's wants fetched). **Document dimensions**: evidence for and against per text with anchors
  (the runs lane's ledger.jsonl, quotations re-found by code, pages from the rendition). **Corpus dimension**: a VERDICT — holds · holds in part ·
  does not hold — with the reasons; the speculate formats (memo · steelman-then-attack · answer + ledger · an outline it would sustain).
- **What exists**: runs 23–24 (the first hypothesis runs), the hunch lane filed from the exchange's and the drain's readings, `STACKS_HUNCH_DAILY`.
- **Against the catalogue**: `adversarial_robustness_tester`, `charitable_reconstruction`, `competing_explanations_analyzer` are the neighbours; none
  takes a scholar's one-line hunch, assembles the corpus from a 20k-work library, fetches what is missing and returns a verdict. The engine is the
  protocol; the corpus assembly is the bridge (§3).

### 5. The conversation as a source: the digest and the memo across — `app/digest.py`, `app/digest_pool.py`
- **Question**: what ideas emerged in this conversation, and how did they travel across several? **Documents**: chat transcripts with exchange
  numbers (`## N · Evgeny`). **Document dimensions**: headline, summary, the arc (turning points by exchange), the ideas that EMERGED with origin
  (Evgeny · model · joint · source), exchange and fate (kept · corrected · dropped · open), Evgeny's positions, the corrections, then the semantic
  shapes (concepts, people, works, claims, questions). **Corpus dimension** (`Across`): themes with converges · diverges · evolves, the paths of
  ideas, divergences with positions, the standing positions, settled · open · next · reading.
- **What exists**: the Hintze–Lane digest (Sol Pro, 48 ¢, 12 ideas), the pools (bundle 620's four-paper synthesis at 19 ¢), the fact-check after
  each pool (candidate 1). **Against the catalogue**: nothing takes a conversation with its exchange structure as a source; the Mastermind's source
  kinds are texts. The meaning-making memo's whole premise (§4: the chats as the proxy for the engines) is this candidate.

### 6. The challenge compiler — `app/parts.py` + `app/exchange.py`
- **Question**: which contradictions among the units compile into a challenge to one of the argument's abstract parts, and how does his answer
  change the parts? **Documents**: the parts (5–9 abstract statements, versioned) and the units under them (exhibits, readings, notes). **Document
  dimension**: a challenge with an inspectable structure — the inference at risk, the shared reason, a reformulation, materiality, the inputs — in
  a family keyed by the inference (a rejection is remembered per family and inputs). **Corpus dimension**: his answer read against the parts —
  effects on parts, edits in his words to accept into a new version, ≤ 2 follow-ups, one new challenge queued.
- **What exists**: the tabletop (Codex's Riley parts and one challenge), the exchange, propagation (a revised part re-reads the units under it).
  **Against the catalogue**: the vulnerability family finds a text's exposed flank, inconsistency, overreach — per text; this works at the
  level of an argument's parts against its own evidence base, and remembers rejections. Unique, but young (one day old, one real exchange).

### 7. The thinker synthesis over analyses — `app/semantics.py` `synthesize`
- **Question**: what do the analyses about one thinker agree and disagree on? **Documents**: the memos' semantic annotations (claims with the
  evidence each cites, relations, positions, open questions). **Corpus dimension**: positions as checkable sentences with the memo numbers that
  assert, qualify or deny each; disagreements; consensus; open questions; a reading order; the gaps the analyses name.
- **Against the catalogue**: `scholarly_debate_m…` and `literature_gap_identifier` are close; ours runs over LLM-written analyses (a source kind the
  Mastermind produces but does not read back) and is cached per set with a staleness flag. A modest candidate; its real value is as the
  "what do our dossiers on X say, taken together" method.

**Not candidates, and why**: the citation explanations (`cites_context`) are subsumed by the engagement map (G5); the citation extractor is corpus
authority, not a question (the memo says so rightly); the essay over the citation tables has no document dimension — it reads numbers; the
selectors (kind B) are reconnaissance; Ask the corpus is retrieval Q&A; the term check and the questionnaires ARE Mastermind engines already run
here (`concept_evolution`, `concept_semantic_constellation`, `inferential_commitment_mapper` — runs 3, 7–22).

## 3. Three things that are not engines but that the bridge needs from Stacks

1. **Source selection from the library** (`assemble.py`: plan → gather over eleven routes → judge → compose → the Referee's scan → curate; the
   hunch's bundle; the materials of a pair). The Mastermind starts from "the supplied works"; Stacks is what supplies them from 20k works, with
   the Referee's "not in the library" list and the fetch. Every engine above is only as good as this step. Offer it as the dossier's source step
   (`stacks_brief` → a bundle → `stacks_uids`), not as an engine.
2. **The ledger as data** for their `citation_network`, `citation_politics_analyzer`, `influence_pass*` engines: the citation universe (persons,
   works, events by year, the overlap of two thinkers) is a table they can read directly, page-marked loci included — `GET /api/authors/{aid}/cites`
   and the evidence index of the reply memo.
3. **The essay over the tables** (`cites_essay`) as a DESK: a method that writes prose from a ledger's tables with a partiality paragraph is what
   their `analyst_compose` does over a dossier; the two should compare notes rather than compete.

## 4. What I would do

- Give the Mastermind session this list with the three top candidates first (the fidelity check, the work profile, the arrival-against-the-argument)
  and the two source-side requests of §3.1–3.2; the hypothesis test and the conversation digest as the second wave; the challenge compiler once it
  has a week of real exchanges to validate against.
- On our side, before any of them is seeded: **verify the work profile's passages by code** (one function, the memo lane's `verify_quote`), so the
  first document engine we hand over carries the same guarantee the memo lane does.
- The same rule as for the citation lenses: each candidate is run BOTH ways on one real case (the check on em:U3HITB25 with its Sonnet verdicts; the
  profiles of bundle 22's twelve Riley texts; the drain's forty readings of Brief 1) before anything is retired.
