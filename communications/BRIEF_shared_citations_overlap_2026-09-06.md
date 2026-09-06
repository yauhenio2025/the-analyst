# Shared citations: the overlap of two thinkers' citation universes (6 Sep 2026, evening)

For the Stacks session and for Codex, from the-analyst session, on the owner's ask of 17:52: the Stacks' citation universe already shows the
overlap of two thinkers (`cites.html?overlap=riley-dylan,brenner-robert`: Riley 67 texts in scope, Brenner 56; 60 shared persons, Jaccard 2.9 %
on persons and 0.2 % on works; the four co-authored texts excluded, "evidence for each universe, never for the overlap"; each shared person with
events / texts per side, the outer fans each thinker's own top 15). The owner wants essays over that overlap of the kind the one-to-one memos
are: not "they share 60 names" but what the sharing means. Do they cite the same texts of a shared figure, for the same reasons, on the same
topics, in the same periods? Where does one lean on a figure the other uses as a foil? What does each cite that the other never does, and what
does that residue say about the two universes?

## The shape: one × one with a shared middle

The cohort flow (`BRIEF_one_to_many_citation_analysis_2026-09-06.md`, `TASK_stacks_cohort_citation_flow_2026-09-06.md`) is one author A over a
cohort of persons C. The overlap is two authors A and B over the set of persons S they both cite. The per-pair machinery is the same: the
engagement map reads one author on one person. What is new is the comparison across the author axis, per shared person and across the overlap.

- **The objects.** A and B (all held texts, dated, the ledgers extracted); S = the shared persons with both sides' counts (events, texts, first
  and last year, by kind), each side's works cited of that person (the works overlap is the sharper question: 0.2 % of works against 2.9 % of
  persons means they mostly cite different texts of the same people); the residues R_A and R_B (each side's top fans the other never cites);
  the collective terms if the phrase names a school; the plan (a strong model from "Riley ∩ Brenner": sections, questions, themes, warnings —
  co-authorship, shared students and editors, the same journal's house references, namesakes).
- **The per-person pair.** For each shared person P selected (top-K by the weaker side's count, owner strikes/adds): A's passages citing P and
  B's passages citing P, with loci and page windows; P's cited works held per side.
- **The per-person comparison** (`citation_overlap_map`, ours to build): works cited of P per side and their overlap; the move and stance per
  passage per side (authority · evidence · foil · dialogue · genealogy · illustration · courtesy · self-positioning; adopt · build on · qualify ·
  dispute · mention), read against the actual passages; the topic each side advances with P (the passage readings); the trajectory per side by
  year; the asymmetry verdict for P (shared authority · one's authority the other's foil · same person different texts · same text different
  reading · courtesy on one side · a turning-point citation on one side); anchors from both sides' texts with distinct document keys.
- **The overlap synthesis** (`citation_overlap_synthesis`, ours to build; the cohort synthesis with an author axis): the shared persons ranked by
  joint reliance against asymmetry; the shape of the shared canon (a tradition both write from, a debate both enter, a common teacher, a house
  bibliography); the disagreements inside the overlap (adopted by one, disputed by the other); the periodization of the overlap (when the two
  universes converge and diverge); the residues and what they suggest given who the unshared figures are; the fidelity of each side's reading of
  the shared figures where the audits ran; a partiality paragraph (texts held per side, co-authored texts excluded, persons below the threshold).
- **The memo.** Written to the plan's sections from the synthesis and the per-person ledgers; tables lifted from the ledgers (shared person ×
  side × events × texts × years; person × works cited per side with the overlap marked; person × move × stance per side; the asymmetry verdicts;
  the residues); every claim with a verbatim anchor and page from the side it is about.

## The split

- **Stacks**: the overlap table (a JSON document, `role: overlap_table`, the sibling of the cohort table: authors A and B, settings, plan,
  shared persons with per-side counts/texts/works/held/materials/pair job ids, the residues, the collective block, costs, partiality); the
  evidence index per shared person carrying BOTH authors' passages (the §3.1 shape with `texts[]` for A's and B's citing texts and a `roles`
  map; `author` becomes `authors: [A, B]`); the materials per shared person (both sides' citing texts gathered once each); the per-person job
  posted to `POST /v1/dossier/jobs` with the chosen path; the filing on return; the overlap page under the universe (the shared persons with
  the per-person memos and the overlap memo). The old one-pair memo lane is not extended.
- **Mastermind**: `citation_overlap_map` and `citation_overlap_synthesis` designed by Codex under the standard (questions, cards, answer
  shapes, tables, validation method), plumbed and validated by Claude; a two-author evidence index accepted by `prepare_citation_sources`
  (`authors[]`, `texts[].author`); the same both-ways rule: the first overlap (Riley ∩ Brenner) written by this flow and, for two shared
  persons, by the old lane's one-to-one memos on each side (Riley on Marx, Brenner on Marx), read by the owner before anything is decided.

## Order

After the cohort design lands and the Riley → Weber pilot is reported: Codex designs the two engines from this brief and the cohort design
(reuse, not a fourth family); the Stacks builds the overlap table and the two-author index behind the same `pair_payload()` function; the first
overlap runs both ways. Questions either side should raise before building: the threshold for "shared" (min events per side; the page uses
"at least 1"); whether the works overlap is computed by the works registry's editions or by key; how co-authored texts' citations are handled
(excluded from both, as the page does, or shown as a third column).
