# Develop the question before requiring an account

Implemented on `feat/question-development-2026-09-08`, based on the paired inquiry
feature branch. This is a companion to constructive inquiry, not a deployed service
claim or completion of the broader research agenda programme.

An unresolved problem can need a more useful question before the author has a
settled account to develop. Constructive inquiry requires supplied commitments;
author investigation answers a question about a named author's work. Neither should
stand in for developing the question itself. July's
[questions dictation](vision_2026-07/DICTATION_2026-07-14_questions_VERBATIM.md) gives
question development equal standing with answers, and the
[meta-improvements dictation](vision_2026-07/DICTATION_2026-07-16_meta_improvements_VERBATIM.md)
asks that methods start from needs, recognize exploration and spare operational work.

This activity accepts a problem, optional current question and motivation, and
optional commitments and prior context. It proposes a question, explains the change,
labels assumptions, identifies what earlier work survives and what the framing would
retire, and offers a few alternatives or prerequisites with a next activity. Nothing
accepts the question or turns an inferred assumption into the author's belief.
Stacks owns accepted versions, actual responses, source operations and dispatch.

## Methods and worker contract

`question_preparation` and `question_development` are capability/process records.
Their intellectual instructions live in YAML; the API composes their framing,
dimensions, method cards and synthesis into the worker prompt. The owning organ runs
its subscription worker. These routes make no model call and provide no local method
fallback when the central record is unavailable.

Preparation discovery decides whether development requires primary reading. A useful
conceptual clarification can return `ready`, `needs_sources: false` without
commitments or sources. When evidence is needed, it writes a bounded research brief
for the organ's existing assembly and text preparation. Selection chooses actual
candidates and prior-reading IDs under a budget, with coverage and gaps. If missing
evidence only blocks a later step, selection can explicitly narrow the immediate
task to conceptual development without sources; it must disclose the deferred
evidence and cannot claim an unread source supports the question.

`POST /v1/questions/prepare` accepts `src/questions/schemas.py:PrepareRequest`:

```json
{
  "method": "question_development",
  "phase": "development",
  "context": {
    "question_id": "stacks:question:1",
    "revision": 1,
    "problem": "Why do similar market relations accompany development and underdevelopment?",
    "current_question": null,
    "motivation": "Make the difference intelligible.",
    "commitments": [],
    "prior_readings": [],
    "previous_result": null,
    "author_responses": [],
    "origin_inquiry": null,
    "preparation": {}
  },
  "sources": [],
  "candidates": [],
  "prior_readings": [],
  "discovery_plan": null,
  "availability": {},
  "budget": {"max_sources": 20, "max_chars": 400000, "max_prior_readings": 8}
}
```

Use `method: question_preparation` for `discovery` and `selection`. Candidates,
top-level prior readings and budgets reuse the inquiry planner's typed models.
Preparation receives metadata; development receives actual primary `sources` and
hydrated `context.prior_readings`. `context.preparation` carries the organ's bounded
Brief/history, origins, planning receipts, selected source ranges and coverage gaps.
These context values are frozen, not independently verified by their presence.

Selection requires a ready discovery plan that initially needed sources. Development
can omit `discovery_plan`; if supplied, its declared source requirement is enforced.
When selection narrows an earlier evidence requirement to conceptual work, retain
both planning results/receipts in `context.preparation` and omit the earlier plan
from this optional field. The actual frozen source list governs valid evidence.

`context.previous_result` must be a complete earlier QuestionResult; wall flags on
its evidence are accepted and retained. An originating constructive inquiry travels
in `origin_inquiry` or preparation history. Accepted wording remains separate in
`current_question`, alongside actual author responses.

The response carries `prepared_id`, `input_fingerprint`, `method_fingerprint`,
`method`, `phase`, `source_manifest`, `system_prompt`, `user_prompt` containing
`{input, output_schema}`, and `output_schema`. The existing blob store freezes input,
central records and schema. `POST /v1/questions/complete` accepts those three identity
fields, exact `input`, worker `result` and the existing execution metadata shape.

Preparation result:

```text
phase, status: ready|blocked, needs_sources,
research_brief, rationale, evidence_requirements[],
selected_sources[{source_key, window_ids[]}], selected_prior_reading_ids[],
coverage, gaps[]
```

Empty window IDs mean the whole supplied rendition; otherwise one supplied
contiguous window is allowed per source. A blocked result requires a gap. A ready
conceptual selection has no primary source selections. Readability and budgets are
checked mechanically; source completeness and adequate coverage remain judgments.

Development result:

```text
summary,
proposal{status: proposed, question, motivation, change,
  assumptions[{text, status: author_stated|inferred|proposed, commitment_ids[]}],
  enables, preserves[], retires[]},
alternatives[{id, question, reason}], prerequisites[{id, question, reason}],
evidence[{id, source_key, quote, claim, role, locus}],
next_activity{kind, question, reason, commitment_ids[]}
```

Next-activity kinds are `constructive_inquiry`, `author_investigation`, `exploration`,
`author_clarification` and `pause`. Constructive inquiry requires at least one
supplied approved or explicit commitment ID; an author-stated assumption also needs
such a reference. Unknown IDs and explicitly unapproved commitments are rejected.
Other activities need no settled account. An author-investigation suggestion does
not invent an author ID: the owning app resolves that before dispatch. Suggestions
neither authorize themselves nor report completed work.

Evidence must name an actual supplied primary source. The wall marks quotes as
verified, too short or absent in that source, retaining failures visibly. It checks
presence, not interpretation, attribution or intellectual merit. Without sources,
development admits no source evidence rows. Proposal, alternative, prerequisite and
evidence IDs are globally distinct; `proposal` is reserved.

## Persistence, feedback and scope

Receipts are immutable and retry-safe. Changed problem, purpose, wording, source,
coverage or context requires a new preparation. Catalogue edits do not invalidate
pending completions. Concurrent different results have one database winner.

`GET /v1/questions/receipts/{receipt_id}` returns the result and authoritative
feedback. `POST /v1/questions/receipts/{receipt_id}/feedback` accepts `feedback_id`,
`text`, optional `decision` and optional `revision_id`; the last may name `proposal`,
an alternative or a prerequisite. Identical retries deduplicate; changed event
content conflicts. Feedback remains situated judgment, not a learned method or
accepted application state.

Development uses the existing readings ledger with `kind: question_development`.
Its proposed question row is conjectural and has no source attribution. A conceptual
record has no invented author/text index; it remains retrievable by job/phase and
receipt. Source-dependent development indexes the actual supplied sources and keeps
hashes, context, coverage and method identity. Planning receipts are not primary
readings. Completion retry repairs interrupted index writes; retrieval resolves
immutable feedback events so an older snapshot cannot hide a later correction.

This does not build a general cross-project agenda, migrate every local method,
replace author investigation or weaken constructive inquiry's commitment requirement.
The Stacks companion preserves question versions and can hand an appropriate accepted
question to an existing activity, retaining its origin and actual author judgment.

## Validation

Focused tests use isolated SQLite and actual records, with no model execution. They
cover conceptual-only development, sources and coverage, phase/budget/reference
checks, missing evidence, unapproved/invented premises, handoff conditions, purpose
changes, prior corrections, immutable/concurrent receipts, index repair and feedback.
All 55 new question tests pass; the combined inquiry, planning, readings and oeuvre
regression run below passes 131 tests.

```sh
python -m pytest -q tests/test_questions_2026_09_09.py tests/test_inquiry_planning_2026_09_08.py tests/test_inquiries_2026_09_08.py tests/test_readings_2026_09_07.py tests/test_oeuvre_prior_readings_2026_09_08.py
```

Engineering checks do not establish a worthwhile question. The acceptance case
starts with an unresolved problem and no accepted account, asks the actual author
to judge the proposal, then exercises the appropriate existing activity. The question
can remain exploratory or pause; progress is not measured solely by whether another
constructive inquiry runs.
