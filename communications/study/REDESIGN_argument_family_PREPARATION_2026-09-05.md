# Next argument-family pair: preparation from the ideas sources

**Design preparation only.** The ideas matrix and its bounded corpus follow-ups are complete; see the final synthesis and appended corpus assessments. Neither engine below has been changed, exposed, or validated by this document. The next pair named in the handoff is `dialectical_structure` and `counterfactual_analyzer`; their capability definitions were inspected alongside the [held-out source notes](STUDY_ideas_HELD_OUT_READING_NOTES_2026-09-05.md). Final questions should incorporate the completed commitment, epistemology, and corpus memos before wiring.

The existing definitions contain useful distinctions but also instructions that can prejudge a reading. The dialectical problem statement says there is always a contradiction and asks what authors cannot acknowledge. The counterfactual definition asks whether errors are strategic, requires closest-world and historical reasoning even where the conditional is conceptual, and proposes probability estimates without specifying an evidential basis. These instructions can turn a useful question into an expected accusation. Their replacements should identify a textual operation, preserve attribution and scope, and permit a finding that the alleged conflict disappears on examination.

## Dialectical Structure Mapper

The reader's question is: **which opposed positions or requirements organize this argument, what does the text do with them, and does the claimed transformation follow?** A paired quotation can establish that two formulations occur; the model must explain whether they concern the same object, time, speaker, respect, and modality before calling them incompatible.

Five document dimensions and one corpus dimension are a workable starting point:

| Dimension | Questions and method | Finding fields |
|---|---|---|
| Positions and attribution | Which positions are juxtaposed? Who undertakes each: this paper, an interpreted thinker, a rival, or a hypothetical interlocutor? Quote both and the passage identifying their relation. Do not treat a quoted objection as the paper's own commitment. | `relation-id`, `position-a`, `owner-a`, `position-b`, `owner-b`, two anchors |
| Kind of opposition | Does the pair express contradiction, a performative conflict, practical tension, a difference in scope, or an apparent conflict resolved by a qualification? State the incompatible requirements, if any, in the text's terms. If the two claims can coexist, explain how. | `relation`, `same-respect`, `qualification`, two anchors |
| Response and transformation | Where does the text distinguish, reject, revise, mediate, or preserve the opposition? What is retained and what changes? Quote the transition and identify the premise that licenses this particular response rather than merely showing that the initial formulation fails. | `response`, `retains`, `changes`, `warrant`, anchors |
| Dependence and self-application | Does a position rely on a resource it criticizes, and is that reliance acknowledged or incompatible with its actual criticism? Does the argument apply its stated standard to itself? Selective appropriation alone is not a contradiction. | `depends-on`, `standard`, `application`, two anchors |
| Remainder and consequence | What is left unresolved, by the paper's own acknowledgment or by a passage that resists its proposed resolution? Does the text claim complete resolution, a local distinction, or continuing mediation? What consequence follows, and what remains a reader's proposed test? | `resolution-scope`, `remainder`, `consequence`, `text-or-reader`, anchors |
| Across the corpus | Does another text retain, change, or refuse the same relation or response? Identify the shared object and relevant scope before alleging a new incompatibility. Keep composition, edition, and argumentative stage distinct. | `doc`, `doc-b`, two anchors, `relation`, `change`, lineage |

The answer shape for the second dimension must allow “compatible after qualification” and “unresolved practical tension”; it must not require every row to say “A excludes B.” A successful dialectical reading can find that an apparent contradiction was the author's carefully distinguished starting point.

The synthesis should begin with the central opposition and the paper's response, then show the attributed positions, the warrant for the transition, what remains, and the strongest unresolved question. Name a relation table, a transition table, and a remainder table. Use the same identifiers in prose and ledger. For a corpus, establish each document's position briefly before tracing relations across documents; similarity of vocabulary is not sufficient evidence of transmission or development.

The supplied papers give discriminating tests. Zambrana adopts Rose's method while disputing Rose's interpretation of Marx. Ganzinger distinguishes an act/concept contradiction from sentential contradiction and distinguishes initially presupposed organic unity from subsequently derived unity. Elling distinguishes necessary exposure to unfreedom from inevitable submission to it, and continuing mediation from a final synthesis. An engine should reconstruct these distinctions before challenging whether the arguments sustain them.

## Counterfactual Analyzer

The reader's question is: **what is being varied or granted, what is held fixed, and which conclusion actually depends on that supposition?** The first operation should distinguish an explicit counterfactual from an open conditional, an even-if concession, a reductio, or a reader's reconstruction of a dependency. These forms need not receive the same historical test.

| Dimension | Questions and method | Finding fields |
|---|---|---|
| Supposition and function | Quote the antecedent and consequent, preserve their modal force, and identify who makes the supposition. Is its job to explain a cause, test a concept, grant a rival premise, or establish robustness? Is the antecedent denied, left open, or merely granted? | `scenario-id`, `kind`, `owner`, `antecedent`, `consequent`, `function`, anchors |
| Fixed and changed conditions | What does the text explicitly preserve or change? Which further changes follow from the supposition, and which are additional assumptions? Distinguish an inconsistency in the scenario from a scenario the paper deliberately uses to test a concept's limits. | `held-fixed`, `changed`, `additional-assumption`, `basis`, anchors |
| Inferential path | What connects the supposition to the result: a definition, conceptual requirement, causal mechanism, historical regularity, or cited argument? Identify each missing step and the passage requiring it. Do not assign numerical probabilities without evidence. | `link`, `kind`, `stated-or-reconstructed`, `support`, anchors |
| Alternatives and scope | Does another relevant case or interpretation in the text yield a different result? For historical scenarios, do earlier conditions also have to change, and does the argument acknowledge that? For conceptual arguments, which conditions make the contrast relevant? | `alternative`, `relevant-similarity`, `scope`, `revision`, paired anchors |
| What survives | If a disputed premise or extra change is withdrawn, which route to the conclusion fails and which independent evidence remains? Distinguish losing this formulation, losing this argument, and losing every route to the result. Mark the analyst's proposed counterfactual as such. | `withdrawn`, `affected-route`, `surviving-route`, `conclusion-strength`, anchors |
| Across the corpus | Do two texts vary the same condition while holding comparable background conditions fixed? Does one grant an antecedent the other denies? Compare the inferential role, not just the presence of “if.” | document pair, two anchors, `shared-variable`, `background`, `divergence`, lineage |

The synthesis should present a compact scenario inventory, the most consequential dependency, the fixed/changed conditions, relevant alternatives, and the conclusion that survives. Name scenario, dependency, and robustness tables. The method should allow “no relevant instance found”; implementation must give that outcome a truthful form rather than force an invented scenario merely to populate a ledger.

Elling's even-if fully free society is a particularly useful test: it grants objective realization for argument's sake while retaining the requirement of subjective mediation, and expressly declines to assume Prussia's completion or the possibility of an end of history. Ganzinger offers conceptual dependency tests, not alternate histories. Harris provides the proposed removal of monism, where the analysis must still consider separate objections to recognition's primacy. These cases can expose historical templates imposed on conceptual arguments and excessive subtraction of surviving support.

## Before implementation and exposure

Use the completed study to settle the exact answer shapes, especially attribution, paired anchors, qualifications, and stable references. Preserve original capability definitions as the comparison baseline; add operationalizations with the established surface/standard/deep modes and routing. A new engine's absence-of-relevant-material behavior and its corpus document identities need an explicit contract.

Validation should compare original questions and the proposed production treatment on the ideas sources with Sonnet in both orders, under a separately recorded authorized spend scope. Select cases that distinguish the failure modes above, not only cases rich in obvious contradictions or historical hypotheticals. This document launches no such calls and makes no claim that either engine has reached the exposure standard.
