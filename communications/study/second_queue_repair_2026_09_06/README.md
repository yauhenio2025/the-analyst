# Second queue repair record

`plan.json`, the top-level outputs, source memos, scores and `first_pass_audit.json` preserve the first repaired pass. All eleven source memos were committed before either rater scored those repaired outputs. The separately marked A3 original baseline rates the unchanged first-round original once; it does not regenerate it.

`post_score_source_adjudication.md` records the real S3 ending-order error and A3 comparison-coverage/score deficit. `final_repairs/` contains the two bounded same-paper checked repairs, with its own frozen plan, source memos and independent ratings. It supersedes only those two selected outputs. The first records remain unchanged.

`continuations/` preserves G3’s empty response, partial response and the explicit allowance change for its failed verifier. Completed upstream calls replayed locally. `model_outputs/` preserves raw model responses, including rejected candidates, and `model_outputs.json` binds them to receipts. Source memos and reports distinguish rejected attempts from final outputs.

`release_audit.json` selects final artifacts and combines costs without double-counting replayed calls. Its checks cover custody, normalized anchors, corpus source keys, table IDs, actual desk handoffs and score comparisons. Semantic decisions belong in the source memos and final adjudication. Scope-review metadata is not proof of source coverage.
