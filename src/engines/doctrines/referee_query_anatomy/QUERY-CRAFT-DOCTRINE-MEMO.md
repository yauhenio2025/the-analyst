# Query-Craft Doctrine Memo — operator gate (2026-07-08)

> **STATUS: FULLY APPROVED AND SHIPPED (2026-07-08).** §A1 shipped first
> (operator confirmed the live probe manually; commit 1384e20 — 32-word
> doctrine + word-budget truth notice, tests 156→158). The operator then
> approved ALL THREE bundles for exhaustive implementation: A2/A3 doctrine
> patch + B1/B2 tool powers (+ cheap B3 riders: as_vis, scisbd, cluster_id
> in results, cluster= fallback; punctuation dedup was already covered by
> _annotate_novelty's normalization) shipped in commit 7d6836b (tests
> 158→165, deployed + verified). C validation ran same day: run
> agent_45185e7873 (14q, $1.53, 0 blocked) exercised wildcard-initial
> exclusion stacks, intitle OR-groups, domain-anchored homonym, lang=de,
> as_vis in discovery, a filtered two-page walk of a 1,689-cite anchor, and
> small-seed one-page economics. Not naturally exercised: positive
> author:/source: anchors, zero-rescue, cluster= fallback, the 32+-word
> warning (all unit-tested). Deferred rider still open: related:/cluster=
> as first-class doctrine got in; a dedicated scholar_related tool was NOT
> built (plain-query related: walk suffices).

> Short decision memo. Evidence: QUERY-CRAFT-RECOVERY-DOSSIER.md (102 findings,
> 4 codebases + live probe, coverage table §1 with per-finding dispositions).
> Everything below is prompt doctrine or model-declared transport parameters —
> no Python query rewriting, no ported auto-correction (R1 honored).

## A. Doctrine changes to prompts.py (the patch, in outline)

**A1. REPLACE the length rule (currently "under ~230 characters; Scholar
truncates silently") — it is wrong, live-disproven today:**

> Scholar has NO practical character limit (verified live to 1,867 chars) but
> reads only the first **32 positive term-words** — every word inside quotes
> counts, OR/operators do not. Words past the 32nd are SILENTLY IGNORED (the
> query looks successful while trailing terms do nothing), so front-load the
> terms that must bind. Minus-exclusions and author:/source: values are
> EXEMPT from the cap — exclusion stacks stay legal at any length. Budget
> each query's 32 words like the scarce resource it is.

**A2. Upgrade the effector-kind bullets in QUERY ANATOMY** (rewrites in
place; net growth ~40-50 lines of system prompt — this is the run agent's
core craft layer and every rule here has a live-observed failure mode):

- *quoted-phrase*: quote 2-4-word phrases only; compress longer concepts to
  their 2-3 most informative tokens (5+-word exact strings ~never occur).
- *or-group*: ≤3-4 quoted alternatives; parenthesize when mixed with required
  terms, anchor OUTSIDE and before the group; never quote a group and never
  put OR inside quotes — both degrade to literal strings; ≤2 OR-groups per
  query (nesting degrades); widen INSIDE a group with 4-8 synonyms instead of
  AND-stacking phrases — each AND'd quoted phrase narrows ~10x (3+ bare
  stacked phrases caused 40% of all zero-result queries in prior systems).
- *intitle/allintitle* (rewrite): the strongest precision move is ONE
  intitle:("A" OR "B" OR "C") group, ≤5 terms — OR is mandatory inside;
  space-separated title terms are an implicit AND that finds ~nothing.
  allintitle: must open the query and carry ≤2 terms.
- *author-anchor*: default to author:"F* Surname" (wildcard-initial subsumes
  every byline variant; mechanical for any middle name). Normalize: strip
  periods, diacritics, honorifics; un-invert "Last, First"; drop middle
  names; hyphens out of first names but KEPT in surnames. The initial form
  belongs ONLY inside author:"…" — as a plain keyword use bare surname or
  full name. Keep the topic payload minimal (1-2 short terms, no stacked
  requirements); NEVER combine author: with source: (measured: kills yield);
  ≤4 positive operators per query. A school-of-thought sweep may OR 3-10
  author: ops. In language-pivoted queries the anchor must be a scholar who
  published ORIGINAL work in that language. Watch namesakes (initial forms
  collide; a profile for a pre-2004/deceased figure is implausible).
- *author-exclude / source-exclude*: exclusions are word-cap-exempt — stack
  and ROTATE sets across queries rather than cramming one query. New third
  axis: -intitle:"first ~30 chars of a landmark title" stops known works
  flooding results (truncation works; batch up to ~10).
- *source-filter*: positive source: is a legitimate EXPLOITATION move on a
  proven venue (+ concepts + year window) and cannot drift; the ban applies
  to venue DISCOVERY only. Values must be real venue strings — prose or
  author names inside source: silently zero the query.
- *minus-exclusion*: quote multi-word minus terms (-"literature review", not
  -literature -review). Proven vocabularies: -survey -"systematic review"
  -"meta-analysis" (flip a lane to primary work; invert when reviews are the
  point); overview-noise pool (tutorial, handbook, overview, bibliometric).
  Patent/lawsuit/press-release/job-posting rows are the GARBAGE signature of
  commercially-loaded vocabulary — rephrase, don't prune.
- *domain-anchor* (new kind): homonyms ("bubble", "network", "friction")
  never travel alone — AND a domain OR-group or go venue-first; >1/3
  off-discipline rows means the TERM is broken, not the page. Country
  anchors pair demonym: AND ("India" OR "Indian").
- *zero-rescue* (new kind): on zero results from an author-anchored query,
  rerun identical with author: stripped (one query isolates anchor vs
  intersection); for a too-tight phrase, interleave wildcards
  ("social * market * economy"), de-quote only as last resort.
- *year-window / page-depth*: add — a page with <10 rows is the END of that
  query's corpus (never page past it); Scholar serves ~100 results max per
  query line including cited-by walks.
- *cited-by-walk*: add — resolve the CANONICAL row first (a title lookup
  returns editions/translations/reviews; pick the row that IS the work and
  has a "Cited by" link — only those carry walkable ids); never rewalk a
  walked cites_id; surveys/handbooks flood field-wide (Reverse Citation Test
  already covers judgment — add the mechanism); on big anchors the unique
  citers start pages ~6-10 and seeds under ~50 citations yield one page;
  after the walk, run "Title" author:"F Surname" as TEXT to catch informal
  references (broadening ladder: drop author → first ~6 title words).
  Title-lookup hygiene: quoted ~40-char prefix, inner quotes stripped,
  + first author's bare surname.
- *harvest hygiene* (execution preamble, harvested_terms bullet): byline
  names arrive as initials and are polluted (venues, fragments,
  institutions posing as authors) — launder/resolve before promoting a
  harvested name to an anchor, exclusion, or the slate.
- *signals*: "about N" is an unstable estimate (live: same corpus read 21K
  and 918K) — judge by rows returned; a bare "N results" (no "About") is an
  exact count and a definitive tiny-corpus signal.

**A3. Calibration examples (kept to 3-4 lines, marked as prior-system
calibration, not rules):** productive "about N" band ~30-500; >70% of a
batch already seen this run (min 5) = line exhausted; per-shape yield bands
(author+concept 60-75% relevant at 10-30 hits; concept∩concept 25-40% at
20-100; venue-filtered 5-30; cited-by 10-200).

**Judged NOT worth prompt space** (recorded in dossier only): per-operator
char-cost table, role-based char bands, site:, AROUND(n), num=20
(live-unverified, stalls Oxylabs), phase-graded minimum floors, author-format
probing, -source: batch sizes, source:-group tolerances (subsumed).

## B. Mechanical affordances (rare, each with determinism ledger)

1. **Filtered citation walks** — extend `scholar_cited_by(cites_id)` with
   optional `query`, `year_from`, `year_to`; Python appends `scipsc=1` iff
   `query` present (Scholar ignores q without it — dossier GM-F27/SA-F10).
   Ledger: shape validation + transport rendering of MODEL-declared
   parameters; zero semantic branching. Turns 3,000-citer floods into
   lane-shaped slices; doctrine bullet rides on it.
2. **Result-language restriction** — optional `lang` on scholar_search →
   `lr=lang_xx`. Ledger: transport rendering of a model-declared parameter.
   Without it, multilingual doctrine under-delivers (hl is interface-only).
3. **DEFERRED unless you want them now**: `related:<cluster_id>` /
   `cluster=` versions surfaces (new tool or param; parser already extracts
   cluster_id); `as_vis=1` / `scisbd` toggles; punctuation-stripped title
   normalization inside the seen_before computation (arithmetic role;
   Scholar re-serves punctuation-variant duplicates — GM-F25).

No other mechanics. Explicitly NOT porting sanya's `fix_author_queries`
rewriting — name-form rules live in doctrine; the anatomy declaration makes
violations visible and the micro-run checks them.

## C. Validation plan

1. Unit: tests for new cited_by/search params (green 156+ before push).
2. **Live micro-run (~12-15 queries)** on the deployed service with a brief
   engineered to force the risky forms: an author-exclusion lane (initial +
   wildcard forms), an intitle OR-group lane, a homonym term requiring a
   domain anchor, one deliberately term-rich query (tests 32-word budgeting),
   a source: exploitation move on a discovered venue, and a citation phase
   with one big-anchor filtered walk + one <50-citation seed. Pass = declared
   anatomy applies the new rules (no bare-surname exclusions, no spaces
   inside intitle groups, no author:+source:, front-loaded binding terms),
   and the filtered walk visibly narrows a citing set.
3. Push discipline as standing: code first (deploy, verify via
   `mcp render list_deploys`), docs after with [skip render]; format-string
   braces doubled in prompts.py (12c5560 lesson).

## Decision requested

- Approve A1-A3 doctrine patch? (net prompt growth ~45-55 lines)
- Approve B1 (filtered walks) + B2 (lr=)? B3 items now or deferred?
- Approve C micro-run (~$1-2 spend)?
