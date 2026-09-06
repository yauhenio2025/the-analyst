## Complete questions, cards, answer shapes and tables

### citation_overlap_map

What does each author do with this shared figure, and what does the comparison mean? Distinguish common names from common works, readings and argumentative reliance. Explain contrasts through the supplied passages and preserve the author axis, dated coverage and scoped residues.

#### O1 — Which works of P are actually shared?

`works_overlap`; scope `corpus`; load-bearing.

- Which works of P does each side cite, and which are shared under the declared work-identity rule?
- Is the apparent common person a shared text, different texts, different editions, or an unresolved bibliographic match?

Do: Read each side’s cited-work inventory and its passage-to-work links. Report exact key and edition intersections separately from supplied registry work-family equivalences; a held copy is not the cited edition. Preserve titles as cited, cited key, registry work/edition IDs, held copies, retrieval how and unresolved matches. Cite table rows for inventory arithmetic; accompany an interpretive claim with both sides’ passages. A person-only mention does not identify a work. The brief’s 0.2% works and 2.9% persons are global Jaccards from one snapshot, not P-specific probabilities or proof most shared people cite different texts. Test that sharper question per P. Distinguish no common identified work from proven disjoint reading.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

```text
[O1.F<n>] <one bounded finding> — dim: works_overlap — person: <P_uid> — claim-kind: bibliographic|interpretive — work-rule: key|registry_work|edition — works-a: <keys> — works-b: <keys> — intersection: <keys> — unresolved: <entries> — metadata-refs: <rows> — author-a: <A_uid> — pair-row-a: <immutable ref or direct map row> — anchor: "<A exact passage>" — doc: <A original key> — locus: <A locus> — author-b: <B_uid> — pair-row-b: <immutable ref or direct map row> — anchor-b: "<B exact passage>" — doc-b: <B distinct original key> — locus-b: <B locus>; repeat labelled groups for every additional endpoint and qualification — confidence: high|medium|low
For an inventory-only row use: [O1.F<n>] <bounded bibliographic report> — dim: works_overlap — person: <P_uid> — work-rule: <rule> — works-a/b: <keys> — intersection: <keys> — unresolved: <entries> — basis: overlap_metadata — metadata-refs: <exact table row IDs> — anchor: "<verbatim rendered metadata row>" — doc: context:overlap — limit: <scope> — confidence: high|medium|low
```

#### O2 — Move and stance in the passage

`passage_use`; scope `document`; load-bearing.

- What does this author accomplish with P at this exact place in the argument?
- Whose proposition is voiced, and which qualification changes the apparent move or stance?

Do: On a citing_author document read the actual surrounding argument for every indexed canonical event. Emit proposition-specific rows, preserving reference/footnote/intext/mention kind. Use move authority|evidence|foil|dialogue|genealogy|illustration|courtesy|self-positioning and stance adopts|builds_on|qualifies|disputes|mentions. Keep adopted_framework from older engagement maps as an explicit inherited move or proposition qualifier; do not silently relabel it authority. A quote attributed to a reviewer or third party is not automatically A or B’s view. Unlocated ledger hits are explicitly unlocated; they support neither page verification nor a decisive comparison. Primary windows are outside this dimension; reading them does not license a new fidelity audit.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

```text
[O2.F<n>] <one bounded finding> — dim: passage_use — move: <move> — stance: <stance> — proposition: <bounded reading> — cited-work: <key or unknown> — voice: <speaker/attributor chain> — qualification: <limit> — inspected: <event/eligible> — author: <uid> — person: <P_uid> — pair: <author_uid>__<P_uid> — event-ids: <author-qualified canonical IDs> — anchor: "<exact passage>" — doc: <original key> — locus: <printed/PDF page or registry section, edition, how> — confidence: high|medium|low
```

#### O3 — The question each side advances with P

`topic_alignment`; scope `corpus`; load-bearing.

- Do both authors use P to answer the same question, or does a shared phrase conceal different explanatory tasks?
- Where do comparable passages agree, disagree or remain incomparable?

Do: Align explicit propositions and their argumentative tasks, not topic keywords. Name each side’s question, concept and explanatory object, and retain difference of genre or target. Label theme origin plan_spine|passage_addition. Same text different reading requires an identified common work and a genuine interpretive contrast, not merely different page numbers; cite the registry equivalence if editions differ. Distinguish complementary uses from disagreement, and offer the strongest contrary passage or a coverage limit.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

```text
[O3.F<n>] <one bounded finding> — dim: topic_alignment — person: <P_uid> — theme: <key/origin> — topic-a: <task> — topic-b: <task> — relation: agreement|complement|disagreement|different_question|unresolved — counterevidence: <rows or limit> — author-a: <A_uid> — pair-row-a: <immutable ref or direct map row> — anchor: "<A exact passage>" — doc: <A original key> — locus: <A locus> — author-b: <B_uid> — pair-row-b: <immutable ref or direct map row> — anchor-b: "<B exact passage>" — doc-b: <B distinct original key> — locus-b: <B locus>; repeat labelled groups for every additional endpoint and qualification — confidence: high|medium|low
```

#### O4 — Each author’s dated trajectory

`side_trajectory`; scope `corpus`; load-bearing.

- How does each side’s use of P persist or change across dated texts?
- Is a proposed turn in the argument visible in passages, or only in counts and publication dates?

Do: Emit a separate trajectory for each author. A before/after claim needs that author in at least two distinct dated texts with ordered years; same-year material is unordered unless explicit sequence provenance is supplied. Quote every endpoint. Separate a turn within one text (argumentative hinge, with before/after clauses) from a career change. Report single-observation or unknown-date limits for the other side; do not invent a parallel trajectory. Distinguish altered works, topics and held coverage from conversion.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

```text
[O4.F<n>] <one bounded finding> — dim: side_trajectory — author: <uid> — person: <P_uid> — relation: continuity|change|argument_hinge|unordered|insufficient — endpoints: <text keys/years/events> — alternative: <coverage or changed question> — anchor: "<earlier passage>" — doc: <earlier original key> — locus: <locus> — anchor-b: "<later passage>" — doc-b: <later original key> — locus-b: <locus> — confidence: high|medium|low
```

#### O5 — What sharing P means

`asymmetry_verdict`; scope `corpus`; load-bearing.

- Is P a shared authority, one’s authority and the other’s foil, or a name covering different texts or readings?
- Is courtesy or a consequential argumentative hinge confined to one side, and how much of the eligible evidence supports that judgment?

Do: Give a primary verdict and optional coexisting tags: shared_authority|authority_vs_foil|same_person_different_texts|same_text_different_reading|courtesy_one_side|turning_point_one_side, plus mixed or unresolved. Name the authority/foil/courtesy/turning side by UID, not “first”. These tags can coexist. Joint authority requires substantive use on both sides; sparse counts alone prove neither courtesy nor a hinge. A one-sided hinge needs the argument’s before/after warrant and evidence of what the other side does, without asserting it never turns unless its full eligible scope was read. Give reliance a reasoned partial ordering with ties/incomparability, alongside weaker-side and normalized count measures labelled descriptive.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

```text
[O5.F<n>] <one bounded finding> — dim: asymmetry_verdict — person: <P_uid> — verdict: <tag> — tags: <list> — affected-author: <uid or both> — joint-reliance: <argued assessment> — asymmetry: <bounded contrast> — inspected-a/b: <eligible denominators> — exception: <row or limit> — author-a: <A_uid> — pair-row-a: <immutable ref or direct map row> — anchor: "<A exact passage>" — doc: <A original key> — locus: <A locus> — author-b: <B_uid> — pair-row-b: <immutable ref or direct map row> — anchor-b: "<B exact passage>" — doc-b: <B distinct original key> — locus-b: <B locus>; repeat labelled groups for every additional endpoint and qualification — confidence: high|medium|low
```

#### Final synthesis card and tables

Do: Follow the approved plan, lead with the supported comparison, and keep every substantive sentence and table cell attached to final retained IDs. Preserve all immutable ancestry and original witnesses after critic rulings. Unknowns remain unresolved; a count table cannot supply a semantic conclusion. Complete the passage inventory with explicit inspected/eligible counts; missing material prevents an exhaustive label. No unilateral source or coauthored text can satisfy the cross-author gate.

Tables (full columns):
person_work_overlap: P | cited-work key/title per side | registry work/edition IDs | held copy per side | shared exact key / registry equivalence / edition | unresolved | canonical event IDs | table row refs; interpretive cells additionally cite map IDs and both passage anchors.
person_passage_uses: P | author UID | pair key | original text key/title/year | event/ref ID/kind | work cited | proposition/topic/theme origin | move | stance | voice/qualification | map ID | exact anchor | printed/PDF/section/edition/how. One row per event × proposition; no max_rows truncation presented as exhaustive.
person_trajectories: P | author | dated original text endpoints | continuity/change/argument hinge/unordered/insufficient | topic/work shift | alternative | map IDs | every endpoint anchor/key/locus.
person_asymmetries: P | primary verdict/coexisting tags | affected author UID | joint reliance reasoning | weaker-side events | inspected/eligible each side | contrary finding | map IDs | both sides’ anchors/keys/loci.

The mandatory partiality paragraph names both authors and the ordered axis; held, inspected and missing text keys/counts and years per side; A+B co-authored keys excluded from both analytical universes (other coauthors and attribution limits separately); kinds/types/self-citation settings; ledger and identity/alias snapshots; exact shared threshold, eligible shared size, selected K, owner additions/strikes, unselected shared and below-threshold positives; person/work intersection and union denominators and identity rule; unresolved works/editions, held/fetched/wanted per side; inspected canonical events and rejected/unlocated anchors; unknown years; complete or top-N residues and omitted counts; separate collective terms and missing collective analyses; audits run/not run/unavailable with assessed denominators. Synthetic content disqualifies release even when mixed with a real pilot. Say which missing source or changed snapshot could change the result.

Close with three to five source passages worth opening, using existing memo links, original keys and inherited loci.

### citation_overlap_synthesis

What do the shared and unshared figures reveal about these two citation universes? Distinguish common names from common works, readings and argumentative reliance. Explain contrasts through the supplied passages and preserve the author axis, dated coverage and scoped residues.

#### S1 — The preserved per-person comparison

`shared_person_readings`; scope `document`; load-bearing.

- What does the final map establish about this shared person, and what remains uncertain?
- Do its side-specific qualifications survive condensation into the overlap memo?

Do: Read one shared-person document at a time. Preserve its works, passage uses, topics, trajectories and verdict; distinguish restating one map from a cross-person finding. Follow every inherited side-pair ref and preserve existing memo links. On table/plan documents return outside scope.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

Do: Read final applied ledgers, with immutable overlap-row and pair-row references, as the evidence layer. Tables and memos are navigation, never additional witnesses. Every substantive synthesis finding inherits ALL anchors from every cited row, its pair::<author_uid>__<person_uid> or shared::<overlap_uid>__<person_uid> document key, original source key/locus, and canonical row lineage. Do not silently re-anchor or broaden the upstream claim. Cross-person claims need at least two distinct shared persons, with BOTH authors supported for EACH person compared. Metadata rows can establish counts, work identities, scoped residue and partiality only. If the evidence needs a new passage reading, return that question to the map. Keep optional fidelity verdicts attached to the exact side, assessed citation and held edition; never majority-vote or average them.

```text
[S1.F<n>] <one bounded finding> — dim: shared_person_readings — persons: <P_uid> — basis: shared_person_map — verdict: <inherited> — qualification: <limit> — overlap-rows: <immutable refs> — pair-rows: <all endpoint refs> — carried-anchors: <all inherited spans, author UIDs, original keys and loci> — anchor: "<A carried span>" — doc: <pair or shared document key> — source-doc: <A original key> — anchor-b: "<B carried span>" — doc-b: <pair or shared document key> — source-doc-b: <B distinct original key>; repeat groups for each shared person and dated endpoint — confidence: high|medium|low
```

#### S2 — Joint reliance against asymmetry

`joint_reliance`; scope `corpus`; load-bearing.

- Which shared persons sustain both arguments, and which expose the sharpest unequal uses?
- How does the explanatory ordering differ from the weaker-side citation-count selection order?

Do: Compare at least two shared persons, with each author represented for each. Produce a reasoned partial ranking, retaining ties and incomparability: joint substantive reliance against differences of move, stance, text or topic. Display min(events_A,events_B), per-side event shares and inspected/eligible coverage separately. No formula converts counts into intellectual reliance. A rare consequential citation can outrank a repeated courtesy only with passage warrant. State the strongest exception.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

Do: Read final applied ledgers, with immutable overlap-row and pair-row references, as the evidence layer. Tables and memos are navigation, never additional witnesses. Every substantive synthesis finding inherits ALL anchors from every cited row, its pair::<author_uid>__<person_uid> or shared::<overlap_uid>__<person_uid> document key, original source key/locus, and canonical row lineage. Do not silently re-anchor or broaden the upstream claim. Cross-person claims need at least two distinct shared persons, with BOTH authors supported for EACH person compared. Metadata rows can establish counts, work identities, scoped residue and partiality only. If the evidence needs a new passage reading, return that question to the map. Keep optional fidelity verdicts attached to the exact side, assessed citation and held edition; never majority-vote or average them.

```text
[S2.F<n>] <one bounded finding> — dim: joint_reliance — persons: <P_uid,Q_uid,...> — ordering: <partial ranking/ties> — reliance-basis: <passages> — asymmetry-basis: <dimensions> — metadata-refs: <counts> — exception: <refs> — overlap-rows: <immutable refs> — pair-rows: <all endpoint refs> — carried-anchors: <all inherited spans, author UIDs, original keys and loci> — anchor: "<A carried span>" — doc: <pair or shared document key> — source-doc: <A original key> — anchor-b: "<B carried span>" — doc-b: <pair or shared document key> — source-doc-b: <B distinct original key>; repeat groups for each shared person and dated endpoint — confidence: high|medium|low
```

#### S3 — The shape of the common canon

`shared_canon`; scope `corpus`; load-bearing.

- Does the overlap look like a shared tradition, a debate, a common teacher, a house bibliography, or a mixture?
- Which explanation survives differences of texts, genres, venues, dates and the unshared figures?

Do: Treat tradition|debate|common_teacher|house_bibliography|mixed|unresolved as hypotheses tested across at least two shared persons and both sides of each. Common teacher needs explicit textual or supplied audited biographical evidence of teaching/acknowledgment; named together is insufficient. House bibliography needs supplied venue/editor metadata plus patterned courtesy references, not journal stereotyping. A tradition requires shared substantive propositions. A debate can share opponents. Keep collective terms as per-side metadata unless separate verified school-reading ledgers exist; do not allocate collective citations to persons. Give rival explanation and disconfirming row.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

Do: Read final applied ledgers, with immutable overlap-row and pair-row references, as the evidence layer. Tables and memos are navigation, never additional witnesses. Every substantive synthesis finding inherits ALL anchors from every cited row, its pair::<author_uid>__<person_uid> or shared::<overlap_uid>__<person_uid> document key, original source key/locus, and canonical row lineage. Do not silently re-anchor or broaden the upstream claim. Cross-person claims need at least two distinct shared persons, with BOTH authors supported for EACH person compared. Metadata rows can establish counts, work identities, scoped residue and partiality only. If the evidence needs a new passage reading, return that question to the map. Keep optional fidelity verdicts attached to the exact side, assessed citation and held edition; never majority-vote or average them.

```text
[S3.F<n>] <one bounded finding> — dim: shared_canon — persons: <UIDs> — canon-shape: <hypothesis> — warrant: <comparison> — rival: <alternative> — metadata-refs: <venue/collective if used> — disconfirmation: <row/limit> — overlap-rows: <immutable refs> — pair-rows: <all endpoint refs> — carried-anchors: <all inherited spans, author UIDs, original keys and loci> — anchor: "<A carried span>" — doc: <pair or shared document key> — source-doc: <A original key> — anchor-b: "<B carried span>" — doc-b: <pair or shared document key> — source-doc-b: <B distinct original key>; repeat groups for each shared person and dated endpoint — confidence: high|medium|low
```

#### S4 — Disagreement inside the overlap

`overlap_disagreements`; scope `corpus`; load-bearing.

- Where does one author adopt what the other contests, and do those readings address comparable propositions?
- Do disagreements cluster around a theme, or merely share a person’s name?

Do: Compare final proposition-level moves/stances from at least two shared persons with both author endpoints. Separate direct disagreement, distinct questions and divergent texts. A one-person disagreement is reported under S1, not inflated to a pattern. Keep same-text different-reading distinct from accuracy: incompatible uses do not establish which reading is faithful. Quote all qualifications and retain counterexamples.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

Do: Read final applied ledgers, with immutable overlap-row and pair-row references, as the evidence layer. Tables and memos are navigation, never additional witnesses. Every substantive synthesis finding inherits ALL anchors from every cited row, its pair::<author_uid>__<person_uid> or shared::<overlap_uid>__<person_uid> document key, original source key/locus, and canonical row lineage. Do not silently re-anchor or broaden the upstream claim. Cross-person claims need at least two distinct shared persons, with BOTH authors supported for EACH person compared. Metadata rows can establish counts, work identities, scoped residue and partiality only. If the evidence needs a new passage reading, return that question to the map. Keep optional fidelity verdicts attached to the exact side, assessed citation and held edition; never majority-vote or average them.

```text
[S4.F<n>] <one bounded finding> — dim: overlap_disagreements — persons: <UIDs> — theme: <key/origin> — relation: disagreement|different_question|mixed|unresolved — propositions: <A/B> — exceptions: <refs> — overlap-rows: <immutable refs> — pair-rows: <all endpoint refs> — carried-anchors: <all inherited spans, author UIDs, original keys and loci> — anchor: "<A carried span>" — doc: <pair or shared document key> — source-doc: <A original key> — anchor-b: "<B carried span>" — doc-b: <pair or shared document key> — source-doc-b: <B distinct original key>; repeat groups for each shared person and dated endpoint — confidence: high|medium|low
```

#### S5 — Convergence and divergence over time

`convergence_periods`; scope `corpus`; load-bearing.

- When do the two citation universes converge or diverge in their use of the same figures?
- Can the change be explained by changing holdings, interlocutors or different publication careers?

Do: An overlap-level before/after finding needs at least two shared persons, both authors for each person, and two dated endpoints per author-person pair. Keep a single-person evolution under S1 and a one-side change explicitly one-sided. Use comparable calendar windows with their coverage, not automatically aligned ages or first/last citation years. Missing dates cannot anchor periods. Same-year sequence needs supplied ordering provenance. Mark replacement of figures as composition_shift rather than conversion; cite metadata and read every substantive endpoint. Do not infer mutual influence from convergence.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

Do: Read final applied ledgers, with immutable overlap-row and pair-row references, as the evidence layer. Tables and memos are navigation, never additional witnesses. Every substantive synthesis finding inherits ALL anchors from every cited row, its pair::<author_uid>__<person_uid> or shared::<overlap_uid>__<person_uid> document key, original source key/locus, and canonical row lineage. Do not silently re-anchor or broaden the upstream claim. Cross-person claims need at least two distinct shared persons, with BOTH authors supported for EACH person compared. Metadata rows can establish counts, work identities, scoped residue and partiality only. If the evidence needs a new passage reading, return that question to the map. Keep optional fidelity verdicts attached to the exact side, assessed citation and held edition; never majority-vote or average them.

```text
[S5.F<n>] <one bounded finding> — dim: convergence_periods — persons: <UIDs> — period: <bounded windows> — relation: convergence|divergence|continuity|composition_shift|unresolved — endpoints: <dated pair refs> — alternatives: <coverage/genre> — overlap-rows: <immutable refs> — pair-rows: <all endpoint refs> — carried-anchors: <all inherited spans, author UIDs, original keys and loci> — anchor: "<A carried span>" — doc: <pair or shared document key> — source-doc: <A original key> — anchor-b: "<B carried span>" — doc-b: <pair or shared document key> — source-doc-b: <B distinct original key>; repeat groups for each shared person and dated endpoint — confidence: high|medium|low
```

#### S6 — What lies outside the overlap

`residues_collective_partiality`; scope `document`; load-bearing.

- Which figures belong only to each checked universe, and which merely fall below the shared threshold or top-K selection?
- What can the residues and each side’s collective terms suggest within the actual coverage?

Do: Read only context:overlap. Emit every R_A and R_B entry (including explicit empty lists), with own count, other-side checked zero and coverage/alias authority. Unshared means zero, not below threshold: put positive-but-below-threshold, unknown and unselected shared persons in separate lists. If only top 15 is supplied, report a truncated residue sample with total size, rank rule, cutoff and omitted count; never “all unshared”. Significance is a hypothesis tied to supplied identity/tradition metadata, not a reading or evidence of ignorance. Collective terms have separate event IDs per side and never inflate person counts. Record held/inspected/missing texts and excluded A+B coauthors by key, threshold and works rule. Metadata alone permits no semantic finding.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

Do: Read final applied ledgers, with immutable overlap-row and pair-row references, as the evidence layer. Tables and memos are navigation, never additional witnesses. Every substantive synthesis finding inherits ALL anchors from every cited row, its pair::<author_uid>__<person_uid> or shared::<overlap_uid>__<person_uid> document key, original source key/locus, and canonical row lineage. Do not silently re-anchor or broaden the upstream claim. Cross-person claims need at least two distinct shared persons, with BOTH authors supported for EACH person compared. Metadata rows can establish counts, work identities, scoped residue and partiality only. If the evidence needs a new passage reading, return that question to the map. Keep optional fidelity verdicts attached to the exact side, assessed citation and held edition; never majority-vote or average them.

```text
[S6.F<n>] <one bounded finding> — dim: residues_collective_partiality — author: <uid> — person-or-collective: <UID> — report: residue|below_threshold|unselected_shared|unknown|collective|coverage — own/other-events: <counts or unknown> — completeness: all|top_n|unknown — hypothesis: <bounded or none> — basis: overlap_metadata — metadata-refs: <exact table row IDs> — anchor: "<verbatim rendered metadata row>" — doc: context:overlap — limit: <scope> — confidence: high|medium|low
```

#### S7 — Fidelity on each side where audited

`side_fidelity`; scope `corpus`; load-bearing.

- Where audits ran, which attributions are accurate, fair, selective, stretched, misattributed or unverifiable on each side?
- Does the assessed coverage permit any comparison of reading practice across the overlap?

Do: Retain each audit verdict and reason under its author-person pair, with A-or-B attribution AND P’s held primary witness, cited/held edition, locus, how and assessed/eligible denominator. Report not_run|unavailable separately from unverifiable. No new audit here. A one-side audit can yield that side’s scoped inventory only; no cross-author superiority. A cross-author fidelity pattern requires assessed verdicts for BOTH authors for EACH of at least two shared persons, comparable assessed propositions and explicit sampling limits. Unverifiable/rejected rows are coverage, never adverse verdicts. No averaged accuracy score.

Do: Preserve the ordered authors axis as UIDs, never infer the side from prose, names or a document's position. A cross-author interpretation requires at least one exact passage anchor from each author, with distinct original document keys and author-qualified event IDs; repeated copies, a shared P witness, and co-authored texts cannot supply the second author. Keep every necessary qualification and nested voice. Counts and missingness come only from the frozen overlap table, never the number of findings. The plan is context, never evidence. Distinguish bibliographic sharing, argumentative sharing and fidelity. A missing or unresolved witness cannot become an adverse verdict. Code checks identities, arithmetic and anchors; the model must explain what the passages warrant. No new quotation from memory, repaired OCR, stitched anchor or unsourced chapter title. Rejected, superseded, unresolved or anchor-failed rows cannot support retained prose or a table cell. Co-authored A+B texts are excluded from the comparison and retained only in a separate metadata annex. Unknown dates remain unknown. Do not claim influence, mutual reading, personal affiliation, ignorance or intent from shared names or scoped zeros.

Do: Read final applied ledgers, with immutable overlap-row and pair-row references, as the evidence layer. Tables and memos are navigation, never additional witnesses. Every substantive synthesis finding inherits ALL anchors from every cited row, its pair::<author_uid>__<person_uid> or shared::<overlap_uid>__<person_uid> document key, original source key/locus, and canonical row lineage. Do not silently re-anchor or broaden the upstream claim. Cross-person claims need at least two distinct shared persons, with BOTH authors supported for EACH person compared. Metadata rows can establish counts, work identities, scoped residue and partiality only. If the evidence needs a new passage reading, return that question to the map. Keep optional fidelity verdicts attached to the exact side, assessed citation and held edition; never majority-vote or average them.

```text
[S7.F<n>] <one bounded finding> — dim: side_fidelity — persons: <UIDs> — audit-rows: <immutable refs> — verdict-pattern: <qualified or insufficient> — assessed/eligible-a/b: <counts> — edition/how: <preserved> — missing: <coverage> — overlap-rows: <immutable refs> — pair-rows: <all endpoint refs> — carried-anchors: <all inherited spans, author UIDs, original keys and loci> — anchor: "<A carried span>" — doc: <pair or shared document key> — source-doc: <A original key> — anchor-b: "<B carried span>" — doc-b: <pair or shared document key> — source-doc-b: <B distinct original key>; repeat groups for each shared person and dated endpoint — confidence: high|medium|low
```

#### Final synthesis card and tables

Do: Follow the approved plan, lead with the supported comparison, and keep every substantive sentence and table cell attached to final retained IDs. Preserve all immutable ancestry and original witnesses after critic rulings. Unknowns remain unresolved; a count table cannot supply a semantic conclusion. Zero selected shared persons yields metadata only; one yields a one-person comparison with residues, never a common-canon pattern. With two or more, require both authors for each person supporting a cross-person finding.

Tables (full columns):
shared_person_side_counts: P | selected/unselected | author UID | events | distinct texts | first/last year | by kind | canonical event IDs | table row ref | inspected/eligible. Global person/work intersections, unions and denominator settings in caption; never sum person counts to get unique events.
works_by_side: P | works A | works B | exact key intersection | registry/edition equivalence | unresolved | held/wanted/fetched per side | metadata refs | inherited map IDs for interpretation.
moves_stances_by_side: P | author | text/year/event | proposition/topic | move | stance | qualification | final synthesis IDs | map/pair refs | verbatim inherited anchors and original loci.
joint_reliance_asymmetries: rank/tie/incomparable | P | joint reliance reasoning | asymmetry verdict/tags/affected side | min events / per-side shares | inspected/eligible | counterexample | final IDs and all endpoint refs.
overlap_periods: period | persons | both authors’ dated endpoints | convergence/divergence/continuity/composition shift/unresolved | competing explanation | final IDs | all endpoint refs/anchors.
residues_by_side: author | unshared P | own events/texts/years | opposite checked zero | identity/alias and corpus scope | all/top_n/omitted count | hypothesized significance with supplied basis | metadata refs. Separate blocks for positive below threshold, unselected shared and unknown, and per-side collective metadata.
fidelity_by_side: P | author | audit event/pair ID | attribution | P position | verdict/reason | cited/held edition/how | assessed/eligible | not_run/unavailable/unverifiable/rejected | final IDs | immutable audit refs | all A-or-B and P anchors.

The mandatory partiality paragraph names both authors and the ordered axis; held, inspected and missing text keys/counts and years per side; A+B co-authored keys excluded from both analytical universes (other coauthors and attribution limits separately); kinds/types/self-citation settings; ledger and identity/alias snapshots; exact shared threshold, eligible shared size, selected K, owner additions/strikes, unselected shared and below-threshold positives; person/work intersection and union denominators and identity rule; unresolved works/editions, held/fetched/wanted per side; inspected canonical events and rejected/unlocated anchors; unknown years; complete or top-N residues and omitted counts; separate collective terms and missing collective analyses; audits run/not run/unavailable with assessed denominators. Synthetic content disqualifies release even when mixed with a real pilot. Say which missing source or changed snapshot could change the result.

Close with three to five source passages worth opening, using existing memo links, original keys and inherited loci.
