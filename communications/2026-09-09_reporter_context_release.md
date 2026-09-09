# Reporter multimedia context in field investigations

The live Stacks Tether/Riley investigation (`dossier-f200618187ea`, Stacks run 3)
stopped before its first model call because the planner input repeated collection
and retrieval metadata and reached 691,461 characters. A retrieved 557-cue video
also carried 737,222 characters of metadata: duplicated cue text, URL locators,
and raw caption archives alongside a 20,524-character original transcript.

The field runner now prepares Reporter acquisition metadata for model input
before applying the existing final-context policy. The question source drops
only exact copies of collections/gaps already supplied in that same call's
packet. Recording metadata carries a table of exact character offsets, times,
pages and speaker/role fields; null attributions remain unknown. The full source
body stays unchanged. Raw cue archives and repeated passage URLs are retained
with hashes in each call's manifest and in the original frozen source.

Field argument mapping uses the same representation, preserving complete
readings and evidence. Stored readings, quotations and their original metadata
are unchanged, so Stacks still resolves quotations against native frozen spans.
Non-Reporter investigations retain their prior behavior. No method definitions,
model choices or budget ceilings changed.

Validation: 25 focused field, context-packing and new multimedia regression tests
passed. A no-network simulated run over the exact live frozen Tether packet
completed 52 calls and 27 source readings; its largest model input was 503,087
characters. This simulation verifies transport and stage compatibility, not
the quality of a generated memo. The paid run resumes its existing job identity
after deployment; no second collection or Analyst job is needed.
