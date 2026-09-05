# Corpus follow-up: resume and crash limits

The [follow-up runner](../../scripts/study_ideas_corpus_synthesis_followup_2026_09_05.py) completed all four approved calls under identity `d04d447a6d944d02`, at $0.886604 estimated cost and $7.621792 cumulative study cost. It exited successfully after validating all four recorded completions. No crash or paid retry occurred. The production runtime was updated afterward; the historical frozen-input guards should now refuse a new live plan from that changed checkout. This document records the completed run’s resume contract, not an instruction to launch more calls.

A completed follow-up is reusable only when its record matches the expected follow-up identity, baseline parent, reviewed instruction, and attempt path. Its sole invocation must have complete status, valid usage, the expected requested/used Sol model and label, and the exact planned system/user prompt hashes. The saved raw response must equal the final output byte for byte. The record also pins the invocation receipt's file hash.

Resume checks the original prompt copy, offline replay proof, ledger diff, and step/job receipts. It recomputes the wall, source coverage, and rendered ledger through the frozen runtime and compares the saved audit artifacts. Any mismatch stops execution; it does not turn a damaged completed output into permission for a fresh model call.

The approved follow-up scope remains one recorded synthesis invocation for each of the four corpus jobs. Before launching an unfinished job, the runner checks every follow-up identity for an existing invocation of that job. A failed, partial, or completed invocation in another identity blocks another paid call. Changing the selected jobs or obtaining a new plan hash therefore cannot silently duplicate an attempted synthesis. Original and follow-up invocation receipts remain the sole cumulative cost source; the $20 known-spend gate still applies.

There is deliberately no automatic stale-running reset. The runner refuses running results or invocation receipts even if the process has died. A crash can leave a successfully returned response waiting for offline assembly, or it can leave an unresolved request whose response and billing are unknown. These cases require different treatment.

If a crash occurs, preserve the record, response, prompt and receipts. A complete, hash-verified saved response may support a separately recorded offline recovery using the same frozen wall; an incomplete or missing response does not justify a blind paid retry. No such crash has required a recovery command during this preparation, so none has been added. Do not delete running markers or failed receipts to bypass the refusal.

Six offline tests pass, covering parent/instruction/prompt/model/output binding, refusal of an additional invocation after a failed attempt, exact prompt insertion, synthesis capture, cumulative budgeting, and replay provenance failures.
