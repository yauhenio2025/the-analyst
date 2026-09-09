# Shared critical methods for source collections and field inquiries

The Tether integration added useful source criticism to Stacks and Reporter prompt strings. That reasoning now lives in central executable capability and operationalization records. Stacks supplies a method contract and original evidence; the Analyst selects and freezes the records. Reporter reads a central search practice. The standalone think-tank inquiry remains a separate commissioned feature.

## Deposited methods and consumers

All four methods below are version 1, discoverable through `/v1/engines/capability-definitions` and callable independently through `POST /v1/engines/{key}/call`. Their capability and operationalization YAMLs contain the reasoning, triggers, inputs, outputs, limits and provenance. They are also composed as guidance into existing field stages, without additional model calls or model changes.

| Key | Responsibility formerly in adapters or identified from Tether | Consuming field stages |
|---|---|---|
| `multimedia_source_criticism` | Reporting versus interested testimony; speaker and quotation attribution; native locators; extraction and independence limits. Formerly Stacks `app/field_investigations.py` and Reporter collection interpretation rules. | Plan, field read/map, author read, adjudication, memo |
| `causal_mechanism_audit` | Question-premise checking, mechanisms, incidence, outcome effects, alternatives and reversal conditions. Tether supplies an example, not a predefined answer. | Plan, field read/map, adjudication, memo |
| `concept_case_stress_test` | Definition and scope, case fit, counterexample versus misapplication, warranted extensions with discriminating criteria. | Plan, author selection/read, adjudication, memo |
| `institutional_argument_criticism` | Official adoption versus signed/guest views; argument framing, internal disagreement, affiliation and coverage limits. | Plan, field read/map, adjudication, memo |

The seven `field_investigation_*` engines and operationalizations, and their workflow, are version 2. Each process uses versioned `method_refs` to compose the relevant central records. Shared guidance preserves the host stage's existing output schema; standalone calls use each critical method's own anchored output dimensions.

Search craft is separately registered as `topical-multimedia-discovery`, version `1`, in `/v1/practices`. Its task kind is `topical-source-collection`. Reporter freezes this record in `brief.plan.topical_method` before paid search; terms, planner, agent and hit evaluation consume it. Snapshot exports retain it in discovery provenance. New briefs fail before model work if the required practice is unavailable or incompatible. Old frozen source packets retain their original content.

## Invocation and reproducibility

`GET /v1/engines/{key}/method?version=1` returns the complete capability, operationalization and recursively resolved dependencies, with a canonical SHA-256. A caller can pass this hash as `method_sha256` to the existing call route. A mismatch fails before spending. The result includes `method_receipt` and the complete `method_snapshot`; light-call consumers retain their own result as before.

New field investigations freeze all seven stage methods before the first model call. The investigation retains `method_snapshots`; per-call input manifests and analysis phases carry method receipts. Resume uses those frozen records even if the live registry changes or a method is removed. Hash, identity, dependency-version and cyclic-reference checks run before calls. Method composition and snapshot handling are generic infrastructure; interpretive content remains in the registered records.

For an unfinished pre-refactor field run without method snapshots, `src/engines/method_snapshots/field_investigation_2026_09_09.json` preserves the deployed version-1 records. Remaining calls use that archived baseline, without adding the new methods midway. `method_origin` states that provenance. This does not invent method receipts for historical calls. Existing paid results, source packets, costs and the completed Tether memo are preserved.

Stacks sends `method_contract: {key: field-critical-methods, version: 1}` for multimedia comparisons. Before submitting research, it checks the Analyst's version-2 adjudication method and its hash. The Analyst rejects unknown contract versions. No local interpretive-prompt fallback remains in the multimedia adapters.

## Validation and limits

Offline tests exercise real record loading, composed model prompts, independent executable calls, API discovery and required-hash rejection, full field workflow completion/resumption, archived legacy methods, unknown versions and tampered snapshots. Scripted provider responses demonstrate transport, routing and provenance; they do not demonstrate improved model judgment. The test evidence includes an explicit individual-view disclaimer and an alternative profit mechanism. The original Tether run is retained as the motivating case, not reanalysed or retrospectively relabelled as having used these methods.

The records disclose that no paid comparative evaluation of the revised methods has been performed. The think-tank commission requires a subsequent evaluation over retained Tether evidence and a distinct institutional case under that execution's approved budgets. No additional paid research was needed for this refactor.

Reporter commission: `../the-reporter/communications/COMMISSION_2026-09-09_think_tank_inquiries_in_stacks.md`. Deployment and cross-repository verification are recorded in Reporter's `communications/2026-09-09_shared_critical_methods_release.md`.
