# Redesign: Argument Architecture (2026-09-04)

> Designed from the ideal output backwards, without API spend. Evidence base: the study outputs under `data/study/outputs/` (AUKUS paper), the judgments, the two readers' memos, and `src/engines/capability_definitions/argument_architecture.yaml`. This engine's one-shot with the probing questions was the best single document in the study (Fable: spec 9 / anchor 8 / non-obv 9 / coherence 9 / halluc 8); its four-pass harness lost because the final pass was written for other engines (fixed since) and because re-mapping one object under four moods re-describes it. The definition is sound where it is textbook (Toulmin, Walton) and weak where it is generic (legal standards of proof, attack/defence duplicating quality assessment) and where it names schemes without listing their critical questions.

## 0. What the method is for

An argument-architecture reading answers: **what exactly is claimed, on what grounds, by what licence, and where does the whole thing rest?** Toulmin gives the skeleton (claim, grounds, warrant, backing, qualifier, rebuttal); Walton gives the schemes and the critical questions each scheme must survive; van Eemeren gives the dialectical rules (represent the target faithfully, carry your burden, do not label instead of argue); Johnson and Blair give relevance, sufficiency, acceptability; Aristotle gives the enthymeme, the suppressed premise the audience supplies. The unit of the reading is the *inference*, and every inference is anchored to the sentences that make it. Unlike the conditions engine, this method never needed the author's biography; its defect was a hand-off written for machines and a mapping repeated four times.

## 1. The ideal output

### 1a. One paper

An argumentation theorist, an editor, or a reader who must decide whether the paper proves what it says wants:

1. **The claim inventory, with the operative verbs.** The main claim in the text's words with its logical type (classificatory, causal, normative, methodological), the sub-claims that carry the empirical load, and the *strength* each is stated at, including where the strength drifts between abstract and body. The AUKUS reading found three claims of different types "stacked so that the weaker ones borrow credibility from the stronger": a modest negative methodological claim (the literature is incomplete), the real thesis (AUKUS "constitutes a mutation of neoliberalism", where "constitutes" sets the standard), three causal sub-claims, and a disclaimed normative claim smuggled in through Hugh White. Every claim gets a stable id (`C1`, `C2.1`) and an anchor.
2. **The skeleton per major claim.** Grounds as an inventory of evidence items with ids and anchors (USD 258m, "domestic source" under Title III, the 19.1% share jump, the Eximbank amendment, Sequoia's USD 6m); the warrant reconstructed as the strongest faithful general rule ("if a security arrangement is accompanied by state financing, regulatory relaxation and contracts flowing to identifiable business groups, then it is itself a mode of market coordination and accumulation"); the backing the text offers (intra-school citations, "self-referential"); the qualifiers actually present (anchored hedges) and those missing; the rebuttals acknowledged ("This is not to say that AUKUS ... is completely geopolitically fetishist") and those ignored.
3. **The schemes, with their critical questions run against the text.** Each inference matched to a scheme (sign, classification, cui bono / consequence, analogy, authority, cause, genetic) and *then* the scheme's own critical questions answered from the text: for sign, discriminating power ("a realist would predict defence-industrial mobilisation ... the grounds are consistent with 'security decision with distributional side-effects' as much as ..."); for classification, whether the category admits everything (G7, NATO, Quad, CHIPS Act all cited as instances); for cui bono, whether benefit is shown to cause the policy (one mechanism trace, Korea, and footnote 3 shows the driver was Polish orders); for analogy, whether disanalogies are stated (the Cold War analogy, "the best-handled scheme in the paper"); for authority, whether the authority's premises are accepted with its conclusion (White). Each answer anchored, each marked addressed / unaddressed by the text.
4. **The suppressed premises.** The bridging premises the argument needs and does not state, each anchored to the gap it fills and rated for how controversial it is: benefit implies constitution; bipartisanship expresses a class coalition (against the text's own "fear of being 'wedged'"); activist industrial policy is neoliberalism; everything cited is AUKUS; scale is significant; Japan and Korea are inside the phenomenon.
5. **The dialectic and the burden.** The targets attacked, with the attack type (rebut the claim, undercut the warrant, undermine the grounds), whether the target is represented faithfully ("'not simply' defeats a position nobody holds"), the concessions and what they cost ("once the authors admit AUKUS is genuinely a security partnership and an accumulation project, the thesis collapses into the uncontroversial claim"); who carries the burden, whether it is shifted by labelling ("underlying" does the work of an ontology), the standard the text actually applies (its verbs: "we observe", "what is discernible", "it is striking"), and whether the framework can lose ("confirmed by success and failure alike").
6. **Omissions and the strongest form.** What the argument needs and lacks: the counterfactual not isolated (would EXIM, the CHIPS Act exist without AUKUS), the losers not counted, the comparison not made, the method not what it says; then the charitable reconstruction: the strongest version of the position the text could hold ("successful re-description, unsuccessful causal thesis") and what would make it defensible.
7. **The verdict.** The lynchpin inference on which the whole rests, ranked vulnerabilities, what would defeat the argument, what would repair it, in the text's own material.

The artifact: a reading of 12-18K characters that moves 1→7, citing findings by id, followed by the ledger, counter-evidence, open questions, and three tables the desks can lift: the claim inventory (id, claim, type, verb, grounds ids, warrant, scheme, status), the grounds inventory (id, evidence item, anchor, which claims it supports, discriminating power), the suppressed premises (id, premise, needed for which inference, controversy).

### 1b. A five-paper corpus

Across five papers (a school, a debate, a special issue, an author over time) the ideal output adds:

- **Shared warrants**: the licence several papers use without stating, anchored in each.
- **Grounds that are another paper's conclusion**: paper B's evidence is paper A's finding, cited as fact.
- **The exchange**: who attacks whom, with what type, and whether the attack addresses the claim the target actually made; concessions across papers.
- **Scheme habits**: which schemes each paper leans on (a school that argues from sign; an author who argues from authority).
- **The corpus's suppressed premise**: what all five take for granted.
- **Burden across the debate**: who has met it, who has shifted it.

Tables become matrices: claim × paper (asserted / assumed / attacked), warrant × paper (stated / implicit / absent), attack × target (faithful / straw). The reading is then the map of the debate, not of a paper.

### 1c. What "depth" means here

Completeness of the inventory (every distinct ground located; every inference assigned a scheme), the critical questions actually *run* (not named), the lynchpin identified, the charitable reconstruction done, the verdict falsifiable ("what would defeat it"). Surface is items 1, 3 (dominant scheme) and 7; standard is 1-7 on one paper; deep is the corpus.

### 1d. What a weak output looks like

A summary of the paper with Toulmin labels attached; schemes named without their critical questions; "beyond reasonable doubt" applied to a journal article; attack/defence and quality assessment saying the same thing twice; "the argument would be stronger with more evidence"; sections addressed to other engines; four passes that each re-map the same enthymeme.

## 2. The questions that produce it

Six dimensions become five plus synthesis. Merged: structural_composition absorbs suppressed_element_reconstruction (the warrant *is* the suppressed premise most of the time; the study's harness repeated the unfalsifiability point three times because two dimensions asked for it); attack_defense_dynamics absorbs burden_presumption_structure (both are the dialectic); argument_quality_assessment becomes the synthesis. Added: an omissions-and-strongest-form dimension, which the one-shot supplied unprompted and the definition never asked for. Dropped: legal standards of proof as a menu; the standard is read off the text's verbs.

### A1. Claims and their strength
- What is the main claim in the text's own words, and what is its operative verb? What type of claim is it (classificatory, causal, normative, methodological)?
- Which sub-claims carry the empirical load, and how does each relate to the main claim (supports it, is it, is presupposed by it)?
- Where does the stated strength change between abstract, introduction, body and conclusion? Quote both versions.
- Which claims are disclaimed ("beyond the scope") and then made anyway? Quote both.
- Which hedges are present (anchored) and where would a careful author have hedged and did not?

Answer shape: `[F] Claim C<n>: "<verbatim claim>" — type — verb — relation to C1 — anchor — confidence`.

### A2. Grounds, warrants, backing and the suppressed premises
- What evidence items are offered? List each as its own ground (`G<n>`) with its anchor and the claim(s) it is offered for.
- For each major claim, what general rule would have to hold for these grounds to support it? State the strongest faithful warrant; is it stated (quote) or reconstructed?
- What backing does the text give the warrant: cited framework, prior work, definition? Is the backing independent of the claim or circular?
- Which premises does the inference need that the text does not state? For each: the gap it fills, how controversial it is, and whether the text's own evidence cuts against it.
- Which grounds are relevant to a weaker claim than the one they are offered for?

Answer shape: `[F] G<n>: <evidence item> — anchor — supports: C<n> — discriminates between C<n> and rival: yes|no` and `[F] Warrant for C<n>: <rule> — stated|reconstructed — backing: <what> — anchor` and `[F] Suppressed premise S<n>: <premise> — needed for: C<n> from G<m> — controversy: low|medium|high — counter-anchor if any`.

### A3. Schemes and their critical questions, run against the text
- For each major inference, which scheme is it: sign, classification, cui bono / consequence, analogy, authority, cause, generalisation, genetic? Quote the sentence that makes the inference.
- Run the scheme's critical questions (the method card lists them) and answer each from the text: addressed (quote where) or unaddressed.
- For sign and cause: does a rival hypothesis named in the text predict the same signs? Quote the rival and the sign.
- For classification: is the category defined so that anything in the period falls under it? Quote the definition and the instances.
- For authority: is the authority's conclusion borrowed while its framework is rejected? Quote both.
- For analogy: are the disanalogies stated? Quote them.

Answer shape: `[F] Inference I<n> (C<n> from G<m>): scheme — critical question "<q>": addressed at "<anchor>" | unaddressed — confidence`.

### A4. The dialectic: targets, attacks, concessions, burden
- Which positions does the text attack? For each: the target as the text states it (quote), the attack type (rebut the claim, undercut the warrant, undermine the grounds, discredit the source), and whether the target as stated is a position anyone in the text's references holds.
- What does the text concede ("this is not to say", "only partially resembles") and what does each concession cost the main claim?
- Who carries the burden for the main claim, and how does the text try to shift it: a label, a presumption in a single word ("underlying", "obscures"), an appeal to what is "discernible"?
- What standard of proof does the text actually apply? Quote its evidential verbs.
- Could the text's own evidence have come out against its thesis? Quote the passage where a contrary outcome is also read as confirmation, if there is one.

Answer shape: `[F] Attack on <target> ("<verbatim target>"): type — faithful: yes|no|partly — lands: yes|no — anchor` and `[F] Burden: <who> — shifted by "<verbatim device>" — standard applied: <verbs> — falsifiable by own evidence: yes|no — anchor`.

### A5. Omissions and the strongest form
- What comparison, counterfactual, proportion or mechanism would the main claim need, and does the text attempt it? Quote the closest it comes.
- What does the text promise (abstract, introduction) and not deliver? Quote the promise and the nearest delivery.
- What is the strongest claim the grounds actually support (the charitable reconstruction)? State it and the anchors it would rest on.
- What single addition from the text's own material (a case it has, a figure it cites, a rival it names) would most strengthen the argument?

Answer shape: `[F] Omission: <what> — promised at "<anchor>" — nearest delivery "<anchor>" — consequence for C<n>` and `[F] Strongest form: "<claim>" — rests on G<m>, G<k> — what it gives up`.

### S. Synthesis (the write step)
The lynchpin inference; the verdict (where the argument is strong, where it fails, in one line of argument, not a list); ranked vulnerabilities; what would defeat it; what would repair it; for a corpus, the map of the exchange. Cites findings by id; no claim without a row.

## 3. The step sequence

Same shape as the conditions engine: **extract → verify → synthesize**, ledger as hand-off. The difference is what the study already showed: this method is a well-defined mapping a strong model does in one pass, so the question the frontier study asks is not "do passes beat one call" but "can cheap models do the inventory and a strong model the verdict, for a tenth of the cost, without losing the catches" (the borrowed warrant, the two theses, the equifinality).

### Step 1. Extract (cheap model; parallel; one call per dimension)
A1 (claims), A2 (grounds, warrants, suppressed premises), A3 (schemes with critical questions), A4 (dialectic and burden), A5 (omissions and strongest form). A2 and A3 need the claim ids from A1 to be stable across calls: the extraction prompt asks every call to quote claims verbatim and the verify step reconciles ids (two calls will find the same main claim; the critic merges). Output per call: ledger rows in the dimension's shape, counter-evidence, open questions; no essay. Wall: anchors verbatim, ids unique per dimension, one re-anchor round.
Cost on Luna: five calls at about 25K input tokens each, ~2K output; about a fifteenth of one Fable one-shot in total; they run in parallel.

### Step 2. Verify (mid model; one call)
Same duties as the conditions critic, with two specific to this method: (a) **reconcile the inventories**: one claim list, one grounds list, ids rewritten (`C1`, `G7`, `S3`, `I4`) and cross-referenced; (b) **re-run the critical questions** on the three inferences that carry the most weight, because this is where a cheap extractor is most likely to have named a scheme and not run its questions. Then the usual: confirm / weaken / reject with reasons, reject rows that summarise rather than map, hunt for misses (a ground not inventoried, an attack not listed, a concession not costed), name the three rows the synthesis must not lose.
Where it earns its cost: cheap extraction; a corpus (reconciling claims across papers is the whole job). Where it does not: strong-model extraction on one paper, where the inventory is already clean; condition (d) tests this.

### Step 3. Synthesize (strong model; one call)
Input: source and the verified ledger. Output: the reading of §1a (lynchpin first, then the skeleton of the main claim, the schemes and what their questions showed, the dialectic, the omissions, the strongest form, the verdict), findings cited by id, then the final ledger (renumbered, with `from:` lineage), counter-evidence, open questions, and `### Tables` naming the rows for the claim inventory, the grounds inventory and the suppressed premises. Wall: cited ids exist; anchors verify.

### Corpus variant
Extract per paper per dimension; a cross-paper extraction over the merged ledgers for shared warrants, attacks between papers and the corpus's suppressed premise; verify per paper, then across; one synthesis with the sources in context.

### Hand-off example

```
- [A1.F1] C1: "AUKUS is not simply a security partnership, but rather constitutes a mutation of neoliberalism emerging in the context of bipartisanship" — type: classificatory — verb: constitutes — anchor: "constitutes a mutation of neoliberalism emerging in the context of bipartisanship" — confidence: high
- [A3.F4] I2 (C1 from G1-G12): scheme sign — critical question "could a rival cause produce the same signs?": unaddressed; the text names the rival ("domestic policy tools being deployed for primarily geoeconomic purposes") and sets it aside — anchor: "domestic policy tools being deployed for primarily geoeconomic purposes" — confidence: high
- [V.F3] MISS (A4): the framework reads Pillar I's failure as confirmation too — anchor: "the political manoeuvring of both political parties aimed at avoiding public backlash that the partnership is a failure" — confidence: high
- [F2] The lynchpin is the sign inference from distributional beneficiaries to "constitutes": the grounds do not discriminate between the thesis and the economic-statecraft rival the text itself cites — anchor: "domestic policy tools being deployed for primarily geoeconomic purposes" — from: A3.F4, A2.F2 — confidence: high
```

## 4. How the desks consume it

- **The spine** takes the claim inventory as its map of the paper: sections are commissioned per claim or per inference, `anchors_planned` are copied from the rows, the `buried_crux` is the lynchpin row.
- **Tables** lift the three inventories directly (`### Tables: claims — rows: F1, F4, F6, F9`); the rows already carry verified anchors and the desks' wall drops nothing. The grounds inventory is the natural evidence table for an executive reader: item, figure, what it is offered for, whether it discriminates.
- **Figures** draw the argument map from the rows' relations (`supports: C1`, `needed for: C1 from G3`, `attack on T2`): a dependency diagram with the lynchpin marked.
- **Under the hood** shows the five extraction ledgers and the critic's rulings as receipts.
- **Downstream engines** (dialectical structure, inferential commitment) consume the final ledger's claim and premise ids, which is what `composability.shares_with` was trying to say and should now say by id.

## 5. Lineage as method cards

**Toulmin (A1, A2).** Do: for each claim, list the grounds, then write the warrant as the general rule the text would accept, then find the backing the text gives it; note the field (an IR/IPE case study argues by illustration, so ask what illustration can and cannot establish); read qualifiers off the verbs and note where they drift. Indicators: "constitutes", "not simply", "we observe"; a figure offered as proof; "this attests to".

**Walton (A3).** Do: match each inference to a scheme and then run *these* questions:
- sign: is the sign reliable; could a rival cause produce it; does the text name such a rival?
- classification: is the category defined; are the criteria met; would anything in the period fail them?
- cui bono / consequence: did the beneficiary cause the policy or merely profit; is a mechanism traced?
- analogy: what is the relevant similarity; are the disanalogies stated; does the conclusion outrun them?
- authority: is the source expert in this field; is its framework accepted along with its conclusion; do other cited sources disagree?
- cause: is there a mechanism; does the temporal order hold; are alternative causes the text names ruled out?
- generalisation: how many cases; are they the same kind; are counter-cases in the text?
- genetic / ad hominem: is the origin relevant to the truth of the claim?
Indicators: enumerated instances offered as proof; "resembles", "similar"; a quoted expert; "in response to".

**van Eemeren and Grootendorst (A4).** Do: name the difference of opinion and the standpoints; for each attack, check the freedom rule (no discrediting instead of arguing), the burden rule (the proponent defends when asked), the standpoint rule (attack the position actually held), and the closure rule (a failed defence is conceded). Indicators: a label in place of an argument ("fetishism", "insider baseball"); "not simply X"; a hedge that concedes the rival's point.

**Johnson and Blair (S).** Do: for the lynchpin inference, ask relevance (do the grounds bear on *this* claim), sufficiency (enough for the strength claimed), acceptability (would a reader outside the school grant the premises). Indicators: grounds relevant to a weaker claim; strength claimed above the standard applied.

**Aristotle (A2).** Do: reconstruct each enthymeme by supplying the premise that makes it strongest and faithful; then ask whether that premise is acceptable, and whether the text's own evidence contradicts it. Indicators: an inferential leap; "therefore" without a rule; an appeal to what is "clear" or "striking".

## 6. What changes from the current definition

| current | redesign |
|---|---|
| 6 dimensions, two pairs overlapping | 5 dimensions (claims; grounds/warrants/premises; schemes with questions; dialectic and burden; omissions and strongest form) + synthesis |
| "the critical questions specific to each scheme" unlisted | the questions listed per scheme in the method card and run, each marked addressed / unaddressed with an anchor |
| legal standards of proof as a menu | the standard read off the text's own evidential verbs |
| no claim or ground ids | stable ids for claims, grounds, premises, inferences; tables built from them |
| four stances re-mapping one object | five extractions of different objects, one reconciliation, one verdict |
| final pass addressed to other engines | final pass for the reader; downstream engines consume ids |

## 7. What the frontier study should confirm or refute

- That the one-shot with the rewritten questions holds the study's best result (it should; the questions are sharper and the method card lists the critical questions).
- That cheap extraction plus a strong synthesis reaches the one-shot's catches (borrowed warrant, two theses, equifinality, framework-cannot-lose) at a tenth of the cost; the ledger makes this traceable (`from:` lines show which step found each catch).
- That the verify step's reconciliation is needed at all when extraction runs on a strong model (condition (d) versus (c)).
- Anchor verification rate by condition and model (code, not judge).
