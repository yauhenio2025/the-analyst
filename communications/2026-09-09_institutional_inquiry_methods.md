# Institutional inquiry methods and consumption contract

The existing field investigation executor now accepts `inquiry_type: institutional`
and `method_contract: {key: institutional-inquiry, version: 1}` in its frozen
`field_investigation` source packet. It requires institutional field originals;
author, primary and secondary populations must be absent. It plans, reads every
selected original, maps the arguments and writes a memo without author selection
or a fictional comparison. A subsequent comparison is a separate bilateral run.

Submit using `POST /v1/dossier/jobs`, `entry: chosen`,
`path: {chain_key: field_investigation}`, one source with
`role: field_investigation`, and the normal disabled print-desk output flags.
Read the retained result at `/v1/dossier/jobs/{id}/investigation`.
The catalogue workflow `institutional_inquiry@1` declares the four stages.

## Instruction inventory and release matrix

| Operation | Central record/version | Former instruction or new requirement | Consumer | Discovery/API | Executed proof |
| --- | --- | --- | --- | --- | --- |
| Multimedia source criticism | `multimedia_source_criticism@1` | Existing September 9 adapter migration, retained | Institutional plan/read/map/memo; bilateral reading and comparison | `GET /v1/engines/multimedia_source_criticism/method?version=1`; `POST /v1/engines/multimedia_source_criticism/call` | [Paid independent call and exact model-input hashes](study/think_tank_inquiries_2026_09_10/independent-evaluation-receipts.json); composed paid workflow dependencies in [standalone receipts](study/think_tank_inquiries_2026_09_10/standalone-method-receipts.json) |
| Political mechanism and causal attribution | `causal_mechanism_audit@1` | Existing Tether extraction, retained | Institutional plan/read/map/memo; bilateral adjudication | Same method/call routes with this key | [Paid causal audit and model-input hashes](study/think_tank_inquiries_2026_09_10/independent-evaluation-receipts.json), plus institutional workflow receipts |
| Concept testing and warranted extension | `concept_case_stress_test@1` | Existing Tether extraction, retained; used for the later thinker comparison | Bilateral planning/author selection/read/adjudication/memo | Same method/call routes with this key | [Paid independent concept test and model-input hashes](study/think_tank_inquiries_2026_09_10/independent-evaluation-receipts.json); actual bilateral planning freezes this dependency |
| Institutional argument and framing criticism | `institutional_argument_criticism@1` | Official versus signed/guest/participant positions, disagreement and coverage limitations | Institutional plan/read/map/memo; bilateral adjudication | Same method/call routes with this key | [Paid institutional criticism call and model-input hashes](study/think_tank_inquiries_2026_09_10/independent-evaluation-receipts.json); dependency identities in every institutional phase |
| Author-independent planning and memo | `institutional_inquiry_plan@1`, `institutional_inquiry_memo@1` | New commission requirement | `institutional_inquiry@1` through existing field executor | Same method/call routes with these keys; `/v1/workflows/institutional_inquiry` | Completed live `dossier-90ee17aaf89c37c5bcc65af294ce0023`; [frozen methods, phase inputs and spend](study/think_tank_inquiries_2026_09_10/standalone-method-receipts.json) |
| Reusable field reading and disagreement mapping | `field_investigation_field_read@3`, `field_investigation_field_map@3` | Extend existing bilateral operations to permit a field-only population | Both institutional and bilateral workflows | Same method/call routes with these keys | Eight paid institutional readings, batch/global maps and final memo; [actual stage receipts](study/think_tank_inquiries_2026_09_10/standalone-method-receipts.json) |
| Institutional identity and source authority | `institutional_source_identity@1` | Original organizational classification, publishing relationships, signed/guest/adopted authority and disclaimers | Reporter commissioned identity and publication acquisition | `GET /v1/engines/institutional_source_identity/method?version=1`; `POST /v1/engines/institutional_source_identity/call` | Independent model-input composition test; Reporter exact-original relationship and disclaimer checks |
| Institutional discovery craft | `institutional-original-discovery@1` | Issue vocabulary, evidence-led selection, declared geographic/language/date coverage and original relationships | Reporter term planning, institution selection, agent opening and practice receipts | `/v1/practices/institutional-original-discovery` | Reporter deterministic agent/lane test captures the frozen practice in the opening model input |

Each new method has trigger, inputs, steps, structured outputs, limitations,
version and commission provenance in its operationalization. The four shared
critical operations reuse the deployed September 9 refactor; they are not copied
into adapters. Frozen snapshots are kept before the first model call, and phase
receipts retain method and dependency identities. Resumption at final synthesis
does not refetch methods or replay completed readings.

Focused validation: 38 tests passed covering independent calls, source resolution,
field-only execution, forbidden mixed populations, unavailable bodies, existing
bilateral behavior, frozen methods, restart continuity and workflow loading.
Those initial checks used scripted providers. The subsequent [paid evaluation and limitations](study/think_tank_inquiries_2026_09_10/README.md) used retained Tether evidence and a distinct institutional case. Four independent central-method calls cost $0.2603 within the standalone allocation. They demonstrate observed critical behavior, including a concept-test attribution failure, rather than measured general improvement.

Institutional runs and their frozen-source comparisons also retain per-provider-attempt
spend reservations. Before each request, the executor checks a conservative input-byte
and maximum-output ceiling against the approved cap, including unresolved attempts
from earlier execution. SDK retries are disabled within this context; executor retries
need their own reservation. Lost/partial responses keep their ceiling. Verified usage
settles it using conservative configured rates; actual research costs remain separately
reported by the existing call ledger. The current bounded receipt contract supports
OpenRouter and Anthropic; an unpriced or unsupported provider stops before spending.

Latest focused execution: 39 tests pass for the new guard, actual provider boundary,
SDK retry settings, central method consumption and existing process execution. Three
legacy `test_llm_backends.py` tests fail identically on untouched `a2e0df5a` because
they reference the removed `_thinking_config` method; this release does not restore
that superseded interface.


The live comparison freezes `field_investigation_author_select@3`, incorporating the concurrently integrated conflict-reconciliation contract; its other bilateral stages remain version 2 and field read/map remain version 3. Historical snapshots retain their original versions. Source upload factoring, progress hydration and document-key parsing are transport/integrity changes, not new interpretive method versions.
