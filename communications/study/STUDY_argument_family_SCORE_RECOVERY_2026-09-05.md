# One rubric response: explicit offline syntax recovery

The independent-scoring phase stopped after 11 natively valid ratings because the twelfth response, **Sol / Dialectical Structure / candidate Zambrana**, is malformed JSON. It contains all six numeric scores, six nonempty reasons and a summary, but omits the closing brace for `reasons` immediately before `,"one_line":`. No paid retry has been made.

The raw response remains the evidence. It is 2,259 UTF-8 bytes with SHA-256 `ac18ed1c0137b0ee6e55599c8175a8e32bee650aae85ebec5f105e0055f8fb4e`. Inserting exactly one `}` at zero-based byte offset **2049** yields 2,260 bytes with SHA-256 `29a32930e0af258f16fa4a7129e8862d9142c10488a273094eac4f080cbb4d2e`. The corrected object has the required eight top-level keys: six criteria, `reasons` and `one_line`; `reasons` has exactly the six criterion keys. All numbers and reason/summary text remain byte-identical. The scores are **9, 8, 8, 7, 9, 8**, in the frozen criterion order.

Root inspected the raw response and the proposed insertion. An independent reviewer exhaustively tried every single-brace insertion position; only byte 2049 produces the required complete schema. The reason content is substantive: it identifies F12's incomplete anchor, credits selective method use and independent routes, and criticizes the scope display. Whether these reasons are correct remains a separate source-based judgment. Syntax recovery supplies no score, wording or interpretation that the model omitted.

This is an explicitly adopted exception to native strict parsing, not a change to the frozen rubric, prompts or generation runtime. The separate [recovery wrapper](../../scripts/study_argument_family_score_recovery_2026_09_05.py) is restricted to this exact raw response and its bound logical job. It must preserve the original failed job, error, raw response, receipt and prompt; verify the saved source/model/usage bindings; and create a separately derived score artifact. Every other response still uses the original strict parser. No general brace completion, default score or partial mean is permitted.

The ordinary frozen harness remains unchanged. Its native replay cannot accept this malformed response; subsequent continuation and final replay must explicitly use the recorded wrapper. The original failure remains inspectable, and the final results must report the adopted score separately from natively valid ratings and show whether excluding its pair changes the interpretation. The same campaign identity, cumulative spend ledger, lock, source-review gate and USD 16 admission limit remain authoritative. Recovery itself makes no provider call and cannot create another spend window.

Root reviewed the complete wrapper and tests, requested restriction to the pinned target's replay, and verified the implemented guard. An identical malformed response under a different fresh job still fails strict parsing. Exact manifest facts and snapshot membership are checked as well as their hashes. **116 offline tests passed**: 40 recovery cases, 60 unchanged argument-harness cases and 16 unchanged held-out-harness cases. The final actual-data preview independently replayed all 24 generation products and 11 native scores without changing campaign artifacts or making calls.

The accepted wrapper SHA-256 is `442553a7a57ba1c466a14ddfcb9968a4ff0f2698ebda3a50e3f3877a203c14ea`; its test file is `4403f99eb71ca0a04431c6afbb84b04e1920a43a8b32bfed11af88e0c382e642`. The derived score output is `818d51a1e8eb309fb7150f7e03b6d2db1afa22294834510e60e377508b7f4db2`. The [root acceptance record](../../data/study/argument_family_2026_09_05/530df62823ec1915/reader_notes/score_recovery/root_wrapper_review.json) records these checks.

**Adopted offline before continuation.** The [adoption manifest](../../data/study/argument_family_2026_09_05/530df62823ec1915/reader_notes/score_recovery/adoption/manifest.json), SHA-256 `6822061aee74cc83556b0df3af5827aed90e910b45c513dff05bda326d9729cb`, binds the original failed results/job/log, all four original call files, frozen plan, wrapper snapshot, one-byte corrected raw string and derived score. The active job now explicitly records its recovery provenance. Other jobs and all invocation bytes are unchanged. The original call's USD 0.040208 remains in the same cumulative ledger; recovery adds zero calls and zero recorded cost.

Continue and report explicitly with the wrapper:

```bash
python scripts/study_argument_family_score_recovery_2026_09_05.py --run --phase judge --budget-usd 16 --review-record /absolute/path/to/reader_notes/pre_score/judge_review.json
python scripts/study_argument_family_score_recovery_2026_09_05.py --phase report --require-complete
```
