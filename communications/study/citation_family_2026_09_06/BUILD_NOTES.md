# Build validation and recovery

The focused contract/process tests passed. The full suite (workspace TMPDIR) reports 1324 passed, two skipped, the same ten pre-existing failures plus the known order-flaky events test, and eight pre-existing collection errors. The first suite attempt was invalidated by a full /tmp filesystem; its failure is not counted as a code regression.

Concurrent bridge commit 013d3c2 captured the key/role additions while introducing general source/context roles. The build resolves the duplicate role fields, keeps the source/evidence_index/plan contract, and hands citation envelopes from context bindings to the citation process adapter. Bibliographic roles stay in source headers. The brief receives the plan explicitly even though context documents are excluded from reconnaissance and corpus counts.

Initial ENG/G8 invocations received complete provider responses, but printing their receipts to a /tmp log raised ENOSPC after payment. Those original failed receipts and outputs are retained. The explicit recovery runner reuses only hash-identical complete provider responses and continues the frozen process. The index-only fidelity critic ended with provider stop_reason=error; its partial response is retained and a separately recorded new critic invocation is the repair. No other engine output enters that condition.
