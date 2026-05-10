# Report: Phase E Host-Neutral Transient Harness Scope Audit

Verdict: Reject

The memo identifies a real strategic concern, but it picks the wrong next bounded variable. A new proof harness that still sends `consumer_key = aoi-canary` would not prove the stronger thing the memo claims. It would mostly replay the already-thin `aoi-canary` transient proof surface under a different shell while keeping the same analyzer-side consumer contract, renderer adaptation law, and pinned fixture lineage.

## Highest-Signal Findings

### 1. The memo overstates what is still unproved at the host layer.

The current `aoi-canary` transient proof path is already much thinner than the memo implies.

What the host actually does today:

- `/home/evgeny/projects/aoi-canary/src/App.tsx:850-906` chooses one pinned fixture, calls exactly one compose route, normalizes the response, and validates the returned surface.
- `/home/evgeny/projects/aoi-canary/src/App.tsx:1203-1209` renders `tab` roots through `TabShell` and all other roots directly through `RendererHost`.
- `/home/evgeny/projects/aoi-canary/src/components/RendererHost.tsx:10-57` is just a renderer map over `accordion`, `card_grid`, and `raw_json`.
- `/home/evgeny/projects/aoi-canary/src/components/TabShell.tsx:11-63` is just a generic tab container over returned child views.

Most of the remaining `aoi-canary` specificity is shell copy and proof-case UI:

- `/home/evgeny/projects/aoi-canary/src/App.tsx:1008-1016` still brands the app as "AOI Thin Consumer Canary".
- `/home/evgeny/projects/aoi-canary/src/App.tsx:1071-1091` exposes proof-case selection.
- `/home/evgeny/projects/aoi-canary/src/App.tsx:1095-1187` shows AOI-shaped status/meta framing.

So the actual analyzer-facing render boundary is already close to a minimal harness. A second shell over the same payload would mostly duplicate what already exists rather than proving a new substrate law.

### 2. Keeping `consumer_key = aoi-canary` fixed preserves the strongest remaining coupling, so the proposed harness is not genuinely host-neutral.

The analyzer still keys transient capability on explicit consumer identity:

- `src/presenter/compose_from_intent.py:148-176` hard-codes transient handoff admission by consumer key.
- `src/presenter/compose_from_intent.py:1325-1354` adapts every served view through consumer-specific renderer support.
- `src/presenter/manifest_builder.py:105-135` falls back unsupported renderers to `raw_json` based on the consumer definition.

And the consumer definition being reused is still explicitly AOI-branded:

- `src/consumers/definitions/aoi-canary.json:2-30` names the consumer `AOI Canary`, gives it page key `anxiety-of-influence`, and tags it `aoi`.

The host also hard-codes that same identity:

- `/home/evgeny/projects/aoi-canary/src/App.tsx:186`
- `/home/evgeny/projects/aoi-canary/src/lib/transientClient.ts:9-42`

That means the proposed harness would still depend on:

- the `aoi-canary` allowlist entry
- the `aoi-canary` supported renderer set
- the `aoi-canary` raw-json fallback behavior

So the memo's phrase "genuinely host-neutral proof harness" is misleading as written. The shell would be different, but the analyzer contract under it would still be the `aoi-canary` contract.

### 3. The current proof artifacts already show that host-local analytical reconstruction is absent for the two target cases.

The memo is right that broader host-neutral generality is not yet proved. But the specific negative it names is mostly already answered for these two cases inside the existing second consumer:

- `communications/PROOF_phase_e_transient_second_consumer_aoi_canary_source_selection_live_closeout_2026-03-31.json`
  - `observed_request_json_equals_pinned_fixture_request = true`
  - `compose_request_count_in_session = 1`
  - `forbidden_analytical_requests_observed = []`
- `communications/PROOF_phase_e_aoi_canary_genealogy_direct_sections_live_closeout_2026-03-31.json`
  - `observed_request_json_equals_pinned_fixture_request = true`
  - `compose_request_count_in_session = 1`
  - `forbidden_analytical_requests_observed = []`
  - `observed_root_renderer = card_grid`
  - `raw_json_leaf_keys = []`

Those two live captures already demonstrate that:

- the host is replaying analyzer-owned request truth
- the host is not fetching planner/lowering/discovery truth locally
- the host can structurally render both `tab` and non-`tab` roots

So a new shell over the same consumer identity would not answer a materially stronger "no host-local analytical reconstruction" question than the repo has already answered.

### 4. The memo drifts toward proof-vehicle multiplication instead of codifying the next stable host contract.

The strategy docs consistently say app work is justified when it codifies reusable host law or removes host-owned analytical intelligence, not when it creates one more proof shell:

- `communications/MEMO_2026-03-26_fixed_direction_phased_roadmap_from_brain_audit.md`
  - current-app work is justified only if it unblocks honest proof, codifies a stable host contract, or removes host-owned analytical intelligence
- `communications/MEMO_2026-03-30_distilled_strategic_roadmap.md`
  - prefer representative substrate proof over more workflow or host theater
- `communications/DYNAMIC_BESPOKE_APPS_VISION.md`
  - the durable target is analyzer-owned composition plus disposable thin hosts

There is also already one older dedicated proof vehicle outside the AOI page stack:

- `communications/MEMO_2026-03-28_phase2_host_neutral_transient_proof_completion.md`

So the next Phase E move should not be "one more shell" unless it breaks a real remaining contract dependency. The current memo does not do that because it keeps the `aoi-canary` consumer identity fixed.

### 5. The acceptance bar is missing the key thing that would make this slice strategically meaningful: breaking `aoi-canary` consumer dependence.

The memo has detailed fixture, proof, and live-capture acceptance criteria. But it never requires proof that:

- the analyzer no longer depends on the `aoi-canary` consumer definition for these cases
- the served renderer adaptation law is no longer specifically `aoi-canary`-shaped
- the new shell teaches a reusable host contract that future consumers could reuse

Without that, the slice can succeed by copy-pasting the existing `aoi-canary` transient mode into a new shell and replaying the same adapted payloads. That is a documentary variation, not a stronger platform proof.

## What Should Come First Instead

The stronger narrower next step is:

- one proof-only transient consumer contract plus one minimal harness over it

Concretely:

1. Add one explicit proof-only consumer definition, separate from `aoi-canary`.

- It should be proof-oriented, not product-oriented.
- It should expose only the renderer surface the harness actually supports:
  - `tab`
  - `accordion`
  - `card_grid`
  - `raw_json`
- It can reuse the same bounded sub-renderer set currently required by the AOI proof surfaces.
- It should not carry AOI-branded page keys or AOI tags.

2. Admit only the two already-proved route families needed for this proof consumer.

- `source_selection`
- `direct_sections`

Do not widen to `source_profile`.
Do not reopen generic consumer architecture.
Do not broaden readiness or live result discovery in the same slice.

3. Freeze fresh analyzer-owned fixtures and proof bundles with the new proof-only `consumer_key`.

- one AOI `source_selection` request fixture
- one genealogy `direct_sections` request fixture
- one fresh analyzer proof bundle per case

4. Build one minimal harness shell on top of the already-proved render law.

- top-level `tab` goes through `TabShell`
- non-`tab` goes directly through `RendererHost`
- no planner fetches
- no lowering fetches
- no result discovery
- no semantic reconstruction

5. Close it with the same live proof bar the memo already wants.

- observed request equals pinned fixture
- one compose request per session
- no forbidden analytical upstream calls
- AOI case preserves exact root and raw-json leaf expectations
- genealogy case preserves `card_grid` root and empty raw-json set

That step is stronger than the current memo's recommendation because it varies both:

- the host shell
- and the analyzer consumer identity

while still staying bounded and proof-only.

## Why This Alternative Is Better

It answers the real remaining question:

- can the transient compose substrate survive outside the `aoi-canary` consumer contract itself?

The current memo does not. It only asks whether the same `aoi-canary` contract can be replayed inside another wrapper.

This alternative is also still narrower than generic consumer architecture because it does not require:

- open-ended registration machinery
- broad readiness law
- third-product runtime ambition
- arbitrary workflow-family admission

It is one explicit proof consumer, two explicit route families, and one minimal render harness.

## Corrections Needed In The Memo

If the current memo is kept as a reference document, it should be corrected at minimum to say:

1. the proposed harness is shell-neutral over the `aoi-canary` contract, not genuinely host-neutral in the stronger analyzer-contract sense
2. the real hidden coupling is the reused `consumer_key = aoi-canary`
3. success on the memo's current bar would not yet prove consumer-contract independence
4. a proof-only consumer contract is the stronger next bounded variable

## Bottom Line

Reject the memo as the next Phase E scope.

One more shell over `consumer_key = aoi-canary` is not the strongest next move. The stronger bounded next move is one proof-only transient consumer plus one minimal harness over it, using the same two already-proved cases:

- AOI `source_selection`
- genealogy `direct_sections`

That is the smallest step that actually tests whether the remaining dependency is the shell or the consumer contract itself.
