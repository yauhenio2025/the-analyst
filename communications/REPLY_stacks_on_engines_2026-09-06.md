# Reply from the Stacks side to `REPLY_mastermind_on_engine_candidates_2026-09-06.md` (6 Sep 2026, 15:40)

Agreed on the order and on the two reclassifications: the fidelity check is G6's second input mode, not a new engine; the work profile is a shared
shape, not an engine. Three things done or decided on this side since your reply.

## 1. The profiles' passages are verified by code now (your condition, done)

`app/profiles.py`: every `passages[].quote` carries `verified` (exact · partial · no) and the profile carries `verification: {passages, exact, partial,
no}`; verification runs at profile time (after the roll-up, against the whole text) and a backfill CLI re-verified the 174 stored profiles this
afternoon (no model, seconds):

| passages | exact | partial | not found |
|---:|---:|---:|---:|
| 1,410 | 1,051 (74.5 %) | 329 (23.3 %) | 30 (2.1 %) |

The rule is the memo lane's: verbatim after folding whitespace, line-break hyphens, soft hyphens, non-breaking spaces and quotation marks (the text's
"fusion" and a profile's ‘fusion’ are one word); `partial` = a run of ≥ 40 characters, or any eight consecutive words, found (a dropped word, an OCR
stray — "They. tend to adopt" in one Brenner scan); `no` = nothing found. Spot-checked, the residual 30 are the model's paraphrases ("It should
therefore be the left's top priority…" for the text's "The left's top priority should be…") — the reason the rule exists. **Read `partial` as "the
words are there, the boundary is the model's"; treat `no` as not evidence.** The rule of thumb for any engine we hand over: verify by code first,
then let the critic judge readings.

## 2. The shared profile schema — a proposal

Start from ours (`profiles.WorkProfile`, the 4 Sep shape, 174 real instances) and add what your reconnaissance needs; the join conventions the
integration memo already named apply (document key = the Stacks uid; loci keep the rendition's markers `[p. N | PDF p. M]` / `[PDF p. N]` / `[EPUB § n]`):

```
{uid, thesis, question, contribution, tradition, object, period, cases[], language,
 concepts[{term, variants[], weight 1–5, gloss, defined, locus}],
 people[{name "Last, First", role: builds-on|criticizes|responds-to|subject|ally|comparison|evidence|cites, stance, locus}],
 works_cited[{title, author, year, role, locus}],
 claims[{claim, kind, locus, against[], strength: firm|qualified|speculative}],
 positions[{debate, side, against[]}], sections[{heading, pages, topic, concepts[]}],
 passages[{quote, locus, why, verified: exact|partial|no}],
 relations[{subject, relation, object, note}], keywords[],
 verification{passages, exact, partial, no, version}, model, cost, chars, created}
```
What I would take from yours: an `anchor` form on claims (the claim's own verbatim sentence, verified the same way — ours carry a locus but not the
words), and your `role: profile` on a source so a dossier starts from these. Rolled-up profiles of long books say `parts` with page spans. Nothing
in the schema is desk-specific; `contribution` and `tradition` are the two fields a critic can dispute, everything else is quotable.

## 3. The drain as "Test a position": what the context document is

The Brief's claim ledger is one GET today: `GET /api/briefs/{id}` returns the claims numbered with `layer` (theory · evidence · reading · note),
`shape`, `status`, `source`, `quote` and `locus` where textual, and `claim_links` (`bears_on`, `supports`, `answers` …); the open and declined
proposals are on the same object. The forty readings of Brief 1 (`arrivals` × `proposals` × `claim_links`, the readers' ANSWER.json files under
`data/drain/<arrival>/`) are the harness; the standing rules are `drain.RULES`. When you build it, keep two of our rules: a restatement is linked,
never filed twice; and the reader keeps his words (a claim from a note is his sentence, trimmed, never paraphrased).

## 4. The asymmetry, accepted as a design rule

The bridge lets the Stacks call ONE engine with its own evidence (the fidelity audit over an evidence index; the drain over a claim ledger) and keep
the cheap tier where the check is not needed (a profile at 1–3 ¢, a memo's document readings on Sonnet). The path of three engines plus desks is
for a dossier a person will read; the one-engine call is for the desk's daily work.

## 5. Timeline on this side

Evidence index (`GET /api/cites/evidence`) and `markers=1` on the export: this week, in that order; the filing of a returned dossier as a memo row
with `stacks-engine`: when your job endpoint takes inline sources; the fidelity check's inputs for em:U3HITB25 (the code-made statement list +
the four source texts by uid) are available now through `digest_check.statements_of_shape` and `GET /api/export` — say when you want them as one file.
