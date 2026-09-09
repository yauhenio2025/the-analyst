# Cohort identities and school placements

The Stacks cohort table can show no Referee identity when the thinker already exists
under another name. Charles Post is Charlie Post (1832), whose biography explicitly
gives both names and whose memberships include Political Marxism & the Transition
Debate (384). The review must recover identity before proposing missing membership.
It must also assess never-cited members and missing affiliations of known thinkers.

`cohort_school_placement` is a central capability and operationalization, served by
the existing free `GET /v1/operationalizations/cohort_school_placement/process` route.
The Stacks adapter reads `framing` and the `shortlist` / `review` method cards,
freezes the complete record and its fingerprint, and supplies structured answer
schemas. Shortlisting sees the active school catalogue; review also sees selected
school identity profiles and memberships, Referee biographies/works, library work
profiles, citation passages, and completed citation-analysis findings. The output
keeps identity, additional memberships, possible provisional schools, uncertainty
and evidence limits separate. Structural source checks do not prove interpretation.

The existing oeuvre `thinker_placement` engine remains scoped to unknown people
cited in an oeuvre. This method broadens the input to all kept cohort members,
including people not cited in the local corpus and thinkers already in other schools.

Stacks owns jobs, model approval and a shared spending cap, saved reviews and decisions.
A dedicated `thinker_identity_reconciliation` method judges unresolved identities
before school placement. The Referee prepares the method and evidence for the approved
worker; supported aliases are remembered automatically, before the local member is
linked. Identity decisions no longer need an operator approval click. Later resolution, search, growth and duplicate checks
reuse that alias and evidence; Referee branch `fix/shared-thinker-identity` supplies
the shared endpoint. Existing
school proposals enter Referee's candidates API with full source evidence. Approved
new schools use its provisional-school creation API, with resolved seeds and unresolved
people as candidates. No discovery, harvesting or automatic thinker creation is invoked.

Companion implementation: `zotero-stacks`, branch `feat/cohort-school-placement`,
`communications/2026-09-09_cohort_school_placements.md`. Deploy these method records
before activating that Stacks implementation. No registry or live membership writes
were made during development; registry/route tests use no paid inference.

## Shared identity reasoning

`thinker_identity_reconciliation` is a generic strong-tier capability and process,
served by the existing process route. Its identity method asks the model to assess
every supplied candidate against biography, works, aliases, dates, identifiers and
caller evidence. A supported global alias declares `link_existing`; other verdicts
are `distinct` and `unresolved`. The Referee freezes the method with the case and
validates exact evidence quotes and current target records when completing it.

Stacks runs this method under the same displayed model and cap as the cohort review
(default DeepSeek V4 Pro, high identity reasoning). The placement method consumes
those saved receipts and cannot substitute a different identity judgment. School
memberships and new provisional schools remain proposals for the researcher.
No paid model was run during implementation. All three registry/route tests passed.

## Determinism ledger

- YAML capability/process records, registry discovery and response schemas (shape):
  expose the two methods through existing APIs.
- Reading and freezing the selected method before execution (sequence): the organs
  cannot substitute local reasoning prose on registry failure.
- Model-declared identity actions and school proposals (lifecycle-recording):
  the methods assign semantic judgment to the model; no code or confidence cutoff
  selects an identity or intellectual affiliation.
- Record fingerprints and evidence/receipt retention in calling organs
  (arithmetic-truth): retain which method and sources produced the judgment.
