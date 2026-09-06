# One-to-many citation analysis: what it is and what it involves (6 Sep 2026)

For the session that builds it. The coordination side (who owns which step, the bridge contract) is in `TASK_stacks_cohort_citation_flow_2026-09-06.md`; this is the substance.

## The idea

Every citation memo we make today is one-to-one: how thinker A engages thinker P (Riley on Weber). The one-to-many analysis asks how A engages a **cohort**: a school, a tradition, a debate, a generation, named by a phrase ("Brenner and the regulation school", "Riley and the Italian Marxists", "Castoriadis and the Frankfurt School"). The cohort is not a bundle of texts; it is a set of thinkers, and the question is about A's pattern across them: whom A leans on, whom A fights, whom A names once and drops, whom A never mentions though the school would expect it, and how that pattern moves over A's career.

The result is a memo a scholar of A could not write without weeks of work: not "Brenner cites Aglietta twelve times" but "Brenner takes the regulation school's periodization as an authority in the 1980s, turns Lipietz into a foil after 1998, engages Boyer only through Aglietta, and never engages the later Parisian generation at all; the treatment of Aglietta's own texts is fair on the wage relation and stretched on the crisis mechanism."

## The objects

- **A**, the citing thinker: all held texts by A, dated, with the citation ledger already extracted (references, footnotes, in-text citations, mentions, with the first citing sentence and the printed page).
- **The cohort C**: a list of thinkers with a reason each belongs (member · founder · associate · critic-from-inside · later generation), produced by a model from the phrase and then **checked against the ledger**: for each candidate, whether A cites or names them at all, how often, in which texts and years, which of their works. Members A never engages stay in the list as "not engaged", because that absence is one of the findings.
- **The pairs**: for each engaged member P, the one-to-one materials we already know how to make: A's passages citing P; P's cited works, held or to fetch; where wanted, the reception of P.
- **The plan**: written first by a strong model from the phrase alone: the memo's purpose and sections, the questions each section must answer, the themes the engagement turns on, and the warnings (editions and translations; the difference between citing a school and citing a person; nested attributions such as A citing P citing Q; namesakes; self-citation).

## The flow

1. **Plan** (one call, cached per cohort request): sections, questions, themes, warnings, and an estimate of the work.
2. **Expand the cohort** (one call), then **check it against the ledger** (no model): the candidate list becomes a table with counts, texts, years, works per member, and the "not engaged" residue. Show it before spending; the owner can strike or add members.
3. **Materials per member**: A's citing texts (shared across the cohort, gathered once); each member's cited works held or wanted; the fetch fired when the cohort is confirmed; the reception texts only for members where the reception lens is asked.
4. **Per-pair analysis**, one job per engaged member: the engagement map always (per-passage move and stance with verbatim anchors and pages; the trajectory of A's use of P by year); the fidelity audit where P's cited works are held (does A's attribution match what P says at the cited place); the reception map where asked. Each pair's ledger and tables are kept, and each pair's memo is filed on its own.
5. **The cohort synthesis**, one job over all the pairs' ledgers: the cohort dimension. Its rows are cross-member: the members ranked by A's reliance (authority, evidence, framework taken over) against those A uses as foil or dialogue partner; the asymmetries (a member cited constantly but only ever for one idea; a member cited once at a turning point); the periodization of A's engagement with the school as a whole; the members A never engages and what that silence suggests given who they are; where A's reading of the school as a whole is fair, selective or stretched, from the fidelity audits.
6. **The memo**: written to the plan's sections, from the cohort synthesis and the pair ledgers, every claim carrying a verbatim anchor with text and page; tables lifted from the ledgers (member × texts × years × counts; member × move × stance; the fidelity verdicts; the "not engaged" list with reasons); a partiality paragraph (which of A's texts and which of the members' works we hold, what was fetched, what could not be checked).

## What makes it hard, and what to decide up front

- **Membership is fuzzy.** Schools have founders, fellow travellers, critics from inside, and later generations; the plan should say which circles count, and the memo should say who was included and why. A wrong cohort makes a confident wrong memo.
- **Names collide.** Two people with one surname, initials in one text and full names in another; the ledger's person key rules are the defence, and every merge the model proposes is shown, never silent.
- **A cites the school, not the person.** "The regulationists argue…" is an engagement with the cohort without a member; count it under the cohort itself.
- **Nested attributions.** A citing P's account of Q; the reader records A's claim about P, never A's claim about Q as if it were about P.
- **Works not held.** The fidelity audit marks those pairs unverifiable and says so; the fetch may fill them later, and the memo can be re-run.
- **Cost scales with the cohort.** A pair through the engagement map costs a few dollars, the fidelity audit a couple, the reception map more; a ten-member cohort is a $30–80 run. Show the estimate before the button; default to the standard depth; cap per cohort; let the owner drop members or lenses.
- **The first cohort is the harness.** Run it both ways: this flow, and the old one-pair memo lane for two of its pairs; the owner reads both before anything is retired.

## What "done" looks like

A cohort page: the phrase, the plan, the member table with engaged and not-engaged, the per-pair memos, the cohort memo with its tables and partiality paragraph, the costs, and the button to re-run when fetched works arrive. The first cohort written and read by the owner. Every quote in every table re-found by code in the text it claims to come from.
