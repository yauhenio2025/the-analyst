# Codex brief: the shared-citations family (the overlap of two thinkers' universes), 6 Sep 2026, evening

You are Codex (gpt-6-astra, xhigh) in `~/projects/the-analyst`. Read `CLAUDE.md`, then `communications/BRIEF_shared_citations_overlap_2026-09-06.md`
(the owner's ask, dictated this evening), then your own cohort design `communications/study/cohort_2026_09_06/DESIGN_cohort_dimension_and_synthesis_2026-09-06.md`
(merged to master at 9d79431 with its YAMLs, patches, fixtures and tests), then `communications/PROPOSAL_stacks_cohort_contract_2026-09-06.md` (the Stacks'
cohort table and per-pair payload) and `communications/study/STUDY_citation_family_2026-09-06.md`. Division of labour as before: you design
questions, cards, answer shapes, tables, input contracts and validation methods; Claude plumbs and validates. Guidance for spend: USD 10; the
design needs no paid model calls; report cost as unmeasured if the CLI does not expose it.

## The same hard constraint

The Riley → Weber pilot (`dossier-bdc5eb48c407`) is still running in the main tree; do not modify any existing file under `src/executor/`,
`src/dossier/`, `src/engines/`, `src/operationalizations/`, `src/sources/` or `scripts/` in any tree. Work as you did tonight: a worktree
under `/tmp/the-analyst-overlap-2026-09-06` on branch `codex/overlap-design-2026-09-06`, new files under `communications/study/overlap_2026_09_06/`
and new tests under `tests/`, patches under `communications/study/overlap_2026_09_06/patches/` for anything else, generated against main HEAD.
Commit per phase; do not push; do not merge.

## What to design

Two engines, reusing the cohort machinery rather than inventing a fourth family, and the input contract they need:

1. **`citation_overlap_map`** (per shared person P; documents: A's passages citing P and B's passages citing P from a two-author evidence
   index, plus P's cited works held per side; context: the overlap table and the plan). Dimensions along the brief: the works of P each side
   cites and their overlap (the sharper question: 0.2 % of works against 2.9 % of persons); the move and stance per passage per side, read
   against the actual passages; the topic each side advances with P; the trajectory per side by year; the asymmetry verdict for P (shared
   authority · one's authority the other's foil · same person different texts · same text different reading · courtesy on one side · a
   turning-point citation on one side); anchors from both sides' texts with distinct document keys. Decide whether this is a new engine or
   two engagement-map runs (A on P, B on P) plus a comparison pass; justify.
2. **`citation_overlap_synthesis`** (over all shared persons' outputs + the overlap table with both sides' counts + the residues R_A and R_B +
   the collective block): the cohort synthesis with an author axis — the shared persons ranked by joint reliance against asymmetry; the shape
   of the shared canon (a tradition, a debate, a common teacher, a house bibliography); the disagreements inside the overlap; the
   periodization of convergence and divergence; the residues and what they suggest given who the unshared figures are; the fidelity of each
   side's reading of the shared figures where audits ran; the partiality paragraph (texts held per side, co-authored texts excluded, the
   threshold). Say precisely what changes against `cohort-packet/v1` (an `authors: [A, B]` axis, pair keys `<A_uid>__<P_uid>` on both sides,
   the residue lists, the collective block per side) and whether one packet schema can serve both families (`overlap-packet/v1` as an
   extension, or a `mode` field).
3. **The two-author evidence index**: what `prepare_citation_sources` must accept (`authors[]`, `texts[].author`, the roles map) — as a patch
   with tests, not applied.
4. **Validation** under the standard: shape harness on fixtures (build from the pilot's Riley → Weber output when it lands, plus a fixture-only
   second author marked as such); source read of every retained cross-author finding; Sonnet in both orders against the Stacks' one-to-one
   memos on each side for two shared persons (Riley on Marx and Brenner on Marx exist as Stacks memos; confirm which), the owner's read first.
5. **The questions for the Stacks**: the threshold for "shared" (the page uses at least 1 event per side), works overlap by registry edition or
   by key, co-authored texts excluded from both sides or shown as a third column, the residue's size (top 15 per side as the page shows, or
   all), and what the overlap table must carry.

## Deliverables (new files)

- `communications/study/overlap_2026_09_06/DESIGN_shared_citations_overlap_2026-09-06.md` — decisions, the contract, the questions/cards/answer
  shapes/tables in full, the validation method, the expected cost per overlap of K shared persons at standard depth, the questions for the
  Stacks, the ordered handoff for Claude, actual cost.
- `citation_overlap_map.capability.yaml` / `.operationalization.yaml` and `citation_overlap_synthesis.capability.yaml` / `.operationalization.yaml`
  under that directory, loadable by the existing loaders (a test like your `test_cohort_synthesis_definitions_2026_09_06.py`).
- `patches/` for the two-author index, the SourceRole additions, the catalogue offer after validation; `fixtures/` with the schema and a
  synthetic packet.
