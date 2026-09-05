# Triage rubric for the engine catalogue (2026-09-05)

The model reads engine DEFINITIONS (not papers) and answers, per engine, what the definition lets it answer. Code checks only shape: valid JSON, keys that exist, family names from the list. Nothing here asks the model to rank engines by taste; it asks what each engine is for, whether its questions are answerable from a text, and where it duplicates another.

## Per-engine judgment (pass A; cards arrive in small batches from the same category so duplicates are visible)

For each card, return:
- `use`: the one question this engine answers for a reader of a text, in plain words (what would a reader know after it ran that they did not know before). If the definition does not let you say, write "unclear" and say why.
- `family`: one of `genealogy_and_conditions`, `argument_and_logic`, `concept_mapping`, `structure_and_narrative`, `rhetoric_and_style`, `evidence_and_method`, `institutions_and_power`, `temporal_and_change`, `corpus_reports`, `other`.
- `text_facing`: what the engine's questions and focus ask about — `text` (answerable from the text alone: what it says, does, presupposes, cites, omits), `author_biography` (motives, careers, what the author knew or hid), `school_checklist` (whether the text conforms to a named school's method), `off_genre_demand` (evidence a text of its genre cannot contain), `not_analytical` (rendering, formatting, workflow), or `mixed` (say which parts).
- `text_facing_note`: the one phrase of the definition that decides `text_facing`.
- `overlaps_with`: keys of other engines (in the batch or known to you from the catalogue list) whose use is the same or a subset; empty if none.
- `distinctive_value`: what this engine would find that a careful general reading of the text would not; "none" if nothing.
- `verdict`: `keep` (run it under the shape with its questions as they are), `merge` (fold into `merge_into`), `rewrite` (the use is worth keeping but the questions are not text-facing or are too vague to produce anchored findings), `retire` (no distinct use, or not analytical).
- `merge_into`: an engine key when the verdict is merge, else "".
- `reason`: one sentence.

## Family consolidation (pass B; one call per family with all its cards and pass-A judgments)
Return the consolidated set of methods the family needs: for each, a name, the reader's question it answers, the engines that fold into it, whether an existing engine's questions can serve as its questions or new ones are needed, and the reading skills that recur across the family and belong in the critic's duties or a shared method card rather than in any one engine. Then the engines to retire, each with a reason.
