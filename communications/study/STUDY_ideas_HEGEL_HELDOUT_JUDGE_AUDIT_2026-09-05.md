# Held-out Hegel study: independent judge-reason audit

Study `43f051bdd4d89076`. All sixteen completed Sonnet judgments were read after the [independent source memo](STUDY_ideas_HEGEL_HELDOUT_READING_MEMO_2026-09-05.md) was frozen before judging (commit `7124fd2`; SHA256 `25b8c86325bc9b854ab8ac0d7ab1fb383ba7c4e53f8a3569bf8b0cc58bf5b39a`). That memo is unchanged. This audit assesses reasons and displayed-order mapping; it does not select a winner for a split pair.

## Order mapping

For `previous_first`, A is previous and B revised; for `revised_first`, A is revised and B previous. These assignments were checked against the frozen plan, rather than inferred from the reasons. **Every judgment chooses A: eight previous and eight revised selections, with zero order-stable pairs.** All eight pairs reverse preference. Excluding the two pairs containing mechanically recovered outputs leaves six pairs, all still split. This records order sensitivity in this run; it does not identify its cause or estimate performance across other runs.

| Engine | Paper | Previous first | Revised first | Order-stable preference |
|---|---|---|---|---|
| Conditions | Ganzinger | Previous (slight) | Revised (clear) | None |
| Conditions | Elling | Previous (slight) | Revised (slight) | None |
| Argument | Ganzinger | Previous (clear) | Revised (clear) | None |
| Argument | Elling | Previous (slight) | Revised (clear) | None |
| Commitment | Ganzinger | Previous (slight) | Revised (clear) | None |
| Commitment | Elling | Previous (slight) | Revised (clear) | None |
| Epistemology | Ganzinger | Previous (slight) | Revised (clear) | None |
| Epistemology | Elling | Previous (slight) | Revised (slight) | None |

## Concrete reason-quality findings

References G and E use the full [Ganzinger](../../data/study/sources_ideas/hegels_concept_of_the_concept_2026.txt) and [Elling](../../data/study/sources_ideas/elling2025_amphibian_habits_hegel_second_nature.txt) sources, with the same newline-based line numbers as the frozen memo. Judgment identifiers below are exact keys in `results.json`; PF and RF in the coverage table mean previous-first and revised-first.

1. **A precise sentence is credited to the wrong reading.** `judge__argument_architecture__elling__previous_first` praises A's phrasing, “the abstract announces an enabling process that the body identifies only programmatically.” That exact sentence occurs in revised B, section 2. Previous A makes a related programme-versus-delivery point, but the quoted comparative advantage is misattributed. The same judgment's praise of stable institutions as a defeater needs the frozen memo's distinction between historical intensification and continuing vulnerability; E:631–634 permits actual free practice alongside risk.

2. **A claimed advantage is in neither compared output.** `judge__inferential_commitment_mapper__ganzinger__revised_first` credits revised A with detailed Koch/Henrich discussion and specific citations to Koch's bracketing illustration. Neither Commitment/Ganzinger final names Koch or Henrich or contains that illustration. The source discusses it at G:586–604, but source content cannot be attributed to an output that does not discuss it. The same judgment's praise of explicit independent branches is supported by revised **I4.F20–22**; the invented comparison does not erase that real gain.

3. **The last judgment invents conceptual tracking.** `judge__epistemological_method_detector__elling__revised_first` praises revised A's explicit tracking of *parabasis*, “normative illness,” and the Aesthetics amphibian passage as a diagnostic pivot. None of those terms occurs in the revised reading's prose; “amphibian” occurs only inside its document keys, and aesthetics lectures are merely listed among the works reconstructed. This is false novelty. Its praise of revised A's final question and attribution of the societal-death distinction to Elling is supported by the actual output.

4. **Verification failure is incorrectly equated with paraphrase.** `judge__epistemological_method_detector__ganzinger__revised_first` says the previous output's nine unverified anchors mean “paraphrase or approximate recall” and absence of textual discipline. At least **F17** and **F18** reproduce exact source wording after ordinary whitespace joining; F18 is at G:647–648. Their quotation-wrapper verification failure does not establish paraphrase. The output's other truncated anchors do impair evidence presentation, but neither a verification flag nor its absence establishes semantic accuracy. The previous-first epistemology judgment also rewards the same tentative-versus-necessary comparison already rejected in the source memo.

5. **Both Argument/Ganzinger orders reward the same misaligned modal comparison.** `judge__argument_architecture__ganzinger__previous_first` praises “can be understood” versus “only by contradicting itself”; `judge__argument_architecture__ganzinger__revised_first` praises sketch/suggest versus must/only. The frozen memo distinguishes their subjects: G:79 sketches Kantian readings, while G:85–89 already announces necessary contradiction-resolution. A compatibility interpretation and a proposed content-generation derivation are also different claims. The previous-first judgment further treats the revised critic's rejection of **F20** as a substantive gap, even though the strongest-form prose remains and its analytical adequacy requires argument, not deference to the receipt.

These cases qualify the judgments' evidential value. Several reasons correctly recognize independent routes, selective adoption, or the distinction between interpretation and empirical diagnosis. Those observations can inform review. The flipped votes and concrete attribution errors do not provide an order-stable treatment verdict, and this audit leaves the pre-judge source assessments intact.

## Complete judgment coverage and hashes

Each file below was read through its complete recorded judgment and its on-disk SHA256 checked against `results.json`. PF maps A=previous/B=revised; RF maps A=revised/B=previous. Every listed winner is A.

| Judgment output | SHA256 |
|---|---|
| [Conditions/Ganzinger/PF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__conditions_of_possibility_analyzer__ganzinger__previous_first.md) | `9beb135baaa0bc7b9d1ec1f6ac5c98a0c388e28265f7cf9031486f7291e70570` |
| [Conditions/Ganzinger/RF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__conditions_of_possibility_analyzer__ganzinger__revised_first.md) | `61f9e8bb60303c3c992378d547c0043809ec4bb5fb751e219f04dd8a34eb978f` |
| [Conditions/Elling/PF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__conditions_of_possibility_analyzer__elling__previous_first.md) | `d4da8473d9ace810f97a21126887e458047b05434b164272198343ae3adb0fde` |
| [Conditions/Elling/RF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__conditions_of_possibility_analyzer__elling__revised_first.md) | `21863c380b95a1706338b1f50e1ec59a854b44eb2b29370a3d10697c472d1fa3` |
| [Argument/Ganzinger/PF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__argument_architecture__ganzinger__previous_first.md) | `b1b9a5619dcd482654e4e6634dbbda4df226a5fe7946c3f3d6253e8c9c751bd7` |
| [Argument/Ganzinger/RF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__argument_architecture__ganzinger__revised_first.md) | `bdf5f2acae5771585164e78ee0eea1c16449f70e06e2a9f749b7a3b3b456808e` |
| [Argument/Elling/PF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__argument_architecture__elling__previous_first.md) | `4a7dbc89df240b7747771625ef6ad9a2435ba0191c97f0b9f80076566aec7665` |
| [Argument/Elling/RF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__argument_architecture__elling__revised_first.md) | `fee6fe73befc802ce5955a62d4089cdfa4d55aca9d2c91c3e27e4909c6ce7e12` |
| [Commitment/Ganzinger/PF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__inferential_commitment_mapper__ganzinger__previous_first.md) | `a1d478600c4af8bf105d1d36e3b66c21cb49257f71f60e75e7021b54939775b7` |
| [Commitment/Ganzinger/RF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__inferential_commitment_mapper__ganzinger__revised_first.md) | `4caa6a7c55f40c8a1add04fe65d720cc5040e15bb13ec0e86b8b14b9ab895f40` |
| [Commitment/Elling/PF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__inferential_commitment_mapper__elling__previous_first.md) | `4dc2fd5833f29d46a75f818c55809c11d8f90824e8b9da7f7bbeebae616ebd35` |
| [Commitment/Elling/RF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__inferential_commitment_mapper__elling__revised_first.md) | `a641f9b8a3dc50d2deac77ad477235f68a00489e032ed7950683570416b708d8` |
| [Epistemology/Ganzinger/PF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__epistemological_method_detector__ganzinger__previous_first.md) | `3555857fd103077b9c57c995ad20e06d2bb904ee72d21e5b9e4b37a441db215c` |
| [Epistemology/Ganzinger/RF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__epistemological_method_detector__ganzinger__revised_first.md) | `e671e7961e1763402e28626ea035e89abef826a2974bb35b80e892c3306f5c9d` |
| [Epistemology/Elling/PF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__epistemological_method_detector__elling__previous_first.md) | `d916edf1ebc8956016f2f9c907139a5eadbb624eecb167ed6a2bc8f6b4b3ae23` |
| [Epistemology/Elling/RF](../../data/study/ideas_hegel_heldout_2026_09_05/43f051bdd4d89076/outputs/judge__epistemological_method_detector__elling__revised_first.md) | `42f0214cb051ea324468424e7ef560d52e06977a0b9cb032b1591888aad278b5` |
