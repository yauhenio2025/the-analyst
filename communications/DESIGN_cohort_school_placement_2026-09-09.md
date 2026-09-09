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
An approved identity is persisted in the Referee's shared identity registry before
the local member is linked. Later resolution, search, growth and duplicate checks
reuse that alias and evidence; Referee branch `fix/shared-thinker-identity` supplies
the shared endpoint. Existing
school proposals enter Referee's candidates API with full source evidence. Approved
new schools use its provisional-school creation API, with resolved seeds and unresolved
people as candidates. No discovery, harvesting or automatic thinker creation is invoked.

Companion implementation: `zotero-stacks`, branch `feat/cohort-school-placement`,
`communications/2026-09-09_cohort_school_placements.md`. Deploy these method records
before activating that Stacks implementation. No registry or live membership writes
were made during development; registry/route tests use no paid inference.
