# Report: Claude Review Of Phase E Transient Second-Consumer Scope

Date: 2026-03-30
Reviewer: Claude (Opus 4.6)
Memo Under Review: `communications/MEMO_2026-03-30_phase_e_transient_second_consumer_scope.md`

## Verdict: Approve

This is the right next slice, the right target, and the right default proof path. The memo is strategically honest, well-bounded, and accurately grounded in the current codebase reality. No revisions are required before proceeding.

---

## What The Memo Gets Right

### 1. Strategic sequencing is correct

The first Phase E matrix kept the consumer fixed and varied the composition/handoff family across three cases (`source_profile`, `source_selection`, `direct_sections`). That question is answered. The next logical variable to test is the consumer surface itself while keeping the transient compose substrate fixed.

This matches the distilled strategic roadmap (Phase E active question), the state-of-play memo, and the fixed-direction roadmap's Phase 2 exit test (stronger host-neutral / second-consumer transient proof). The memo is reopening a seam that historically appeared in the Stage 13 ledger, but it correctly explains why this is acceptable: the first matrix already proved handoff-family breadth, so consumer-surface generality is now the remaining unresolved variable.

### 2. The honest claim boundary is well-calibrated

The memo's honest claim (line 207):

> analyzer-v2 transient compose is no longer structurally single-consumer-only for one bounded AOI transient path

and the four explicit non-claims (lines 210-214) are both accurate and appropriately bounded. This slice would not prove broad consumer generality, non-AOI second-consumer support, arbitrary engine/pass composition, or consumer-neutral product UX. The memo does not overstate what it would deliver.

### 3. The structural single-consumer diagnosis is code-verified

The memo's claim that "the transient compose substrate still hard-enforces one registered consumer adapter" is precisely accurate. The code boundary is:

```python
# src/presenter/compose_from_intent.py:54
TRANSIENT_COMPOSE_CONSUMER_KEY = "the-critic"

# src/presenter/compose_from_intent.py:158
_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS = frozenset({TRANSIENT_COMPOSE_CONSUMER_KEY})

# src/presenter/compose_from_intent.py:528-536
def _validate_handoff_capability(...):
    if consumer_key not in _REGISTERED_TRANSIENT_CONSUMER_ADAPTERS:
        raise ComposeFromIntentClientError(...)
```

All three compose entry points (`compose-from-intent`, `compose-from-source`, `compose-from-selection`) call `_validate_handoff_capability()` and will reject any consumer_key other than `the-critic`. The memo's scoping of the analyzer-side work (section 3: "add `aoi-canary` to the bounded transient consumer allowlist") correctly identifies the minimal required change.

### 4. The aoi-canary current state diagnosis is accurate

Code-verified findings from `/home/evgeny/projects/aoi-canary/`:

- **Result-backed only**: `resultsClient.ts` calls only `/v1/results/discovery`, `/v1/results/by-job/{job_id}`, `/v1/results/by-job/{job_id}/presentation`. No transient compose endpoints exist in the client.
- **consumer_key**: `aoi-canary` (App.tsx line 146)
- **State machine**: 11-state reducer-driven lifecycle covering `config_missing` through `ready`
- **No host-side analytical reconstruction**: RendererHost.tsx dispatches views directly by `renderer_type` with no semantic logic
- **Supported renderers**: accordion, card_grid, raw_json (in RendererHost), plus tab as root container

The memo's statement that aoi-canary "already has a bounded result-backed second-consumer proof, but not a transient one" is exactly right.

### 5. The renderer adaptation truth is correctly identified

The memo correctly identifies that aoi-canary does not declare top-level `prose` and that analyzer-side adaptation from `prose` to `raw_json` may be needed.

Code-verified: `adapt_renderer_for_consumer()` in `manifest_builder.py:105-135` checks the consumer's `supported_renderers` and falls back to `raw_json` if the target renderer is unsupported and `raw_json` is in the consumer's supported set. Since aoi-canary declares `raw_json` but not `prose`, any `prose` views (e.g., the `report_closeout` semantic role) will be adapted to `raw_json` automatically.

The memo correctly scopes this as acceptable if: (a) adaptation happens analyzer-side, (b) the host does not reconstruct analytical meaning locally, and (c) the proof states the claim is contract-serving and thin-hostness, not polished consumer parity.

### 6. Scope discipline is strong

The out-of-scope list (lines 195-201) is appropriate and comprehensive:

- No non-AOI second-consumer transient proof
- No more than one second consumer
- No generalized transient consumer marketplace/registry architecture
- No lifecycle expansion
- No new governance families
- No arbitrary engine/pass matrices
- No UI productization

The acceptance bar (lines 218-227) is mechanical and verifiable. Each criterion maps to a concrete code or artifact check.

---

## Observations (Not Revisions)

These are findings that do not require scope changes but should inform the implementation session.

### Observation 1: A second consumer gate exists in source_backed_readiness.py

The memo focuses on the `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS` allowlist in `compose_from_intent.py`. That is the primary barrier for the default `source_selection` proof path.

However, `src/analysis_products/source_backed_readiness.py:147` also has a hardcoded check:

```python
if consumer_key != TRANSIENT_COMPOSE_CONSUMER_KEY:
    followup_blockers.append(
        f"compose-from-source only supports consumer_key='{TRANSIENT_COMPOSE_CONSUMER_KEY}' in v1"
    )
```

This gate governs the `compose-from-source` path (the source_profile dossier fallback), not `compose-from-selection`. If the fallback path is ever needed, the implementation session should know about this second barrier. For the default `source_selection` proof path, only the `compose_from_intent.py` allowlist needs to change.

### Observation 2: The canary-side implementation surface is known and narrow

The aoi-canary repo currently has zero transient compose infrastructure. The implementation will need to add:

- A transient compose client (analogous to `the-critic`'s `composeFromIntentClient.ts`)
- A minimal transient compose UI shell (analogous to `AoiComposeFromIntentShell.tsx`)
- Integration of that shell into the existing app routing

The existing `RendererHost.tsx` should work unchanged for rendering the transient response, since it already dispatches by `renderer_type` without semantic logic. The existing renderer package (`@the-syllabus/analysis-renderers`) is already shared.

This is genuinely cross-repo work, as the memo acknowledges. But the canary-side surface should be small because aoi-canary was designed as a thin consumer from inception.

### Observation 3: The proof will show renderer adaptation in practice

The AOI `source_selection` path will likely produce views that use `prose` renderers (the `report_closeout` semantic role maps to `prose_narrative` pattern → `prose` renderer). Since aoi-canary doesn't support `prose`, these will be adapted to `raw_json`.

This means the proof will visually show some views rendered as raw JSON rather than formatted prose. That is an honest proof outcome — it demonstrates that the contract-serving and adaptation machinery works, not that both consumers produce identical visual experiences. The proof record should document which views were adapted and why.

### Observation 4: The presenter route DEFAULT_CONSUMER_KEY is a separate concern

`src/api/routes/presenter.py:45` sets `DEFAULT_CONSUMER_KEY = "the-critic"` for GET endpoints. This default is not relevant to the POST compose endpoints (which require consumer_key in the request body), so it should not block the proof path. But the implementation session should be aware that this default exists and should not rely on it.

---

## Answers To The Prompt Questions

### 1. Is this the right next Phase E slice, or is it reopening an older seam wrongly?

It is the right next slice. The memo correctly identifies that the first matrix already proved handoff-family breadth on one consumer, and the remaining unproved variable is consumer-surface generality. The fact that the second-consumer seam appeared earlier in the stage ledger does not make it wrong to address now — the strategic ordering has changed because the matrix proof changed which variable needs testing next.

### 2. Is the memo honest about what it would and would not prove?

Yes. The honest claim boundary is precise and code-grounded. The four explicit non-claims prevent the proof from being over-interpreted. The acceptance bar is mechanical and verifiable.

### 3. Is aoi-canary the right bounded target?

Yes. It is the only existing second consumer in the registry with an active result-backed proof. It is AOI-focused (keeping the proof surface narrow), and it was designed as a thin consumer from the start. Using an existing consumer rather than inventing a new one is the honest choice.

### 4. Is AOI source_selection the right default proof path?

Yes. It is the richer planner-backed transient AOI path. It reuses the four-family selection shape already ratified in the matrix proof. It proves that planner-backed serving works for a second consumer, not just for the-critic. The fallback to `source_profile` dossier is appropriate as a bounded unblocker if `source_selection` exposes unrelated consumer UI debt.

### 5. Is the memo accurate about the current codebase boundary?

Yes on all three points:

- **Transient compose is structurally single-consumer**: confirmed via `_REGISTERED_TRANSIENT_CONSUMER_ADAPTERS = frozenset({"the-critic"})` and the `_validate_handoff_capability()` gate.
- **aoi-canary is result-backed but not transient**: confirmed via `resultsClient.ts` which calls only result-contract endpoints, no compose endpoints.
- **Analyzer-side adaptation exists for unsupported renderers**: confirmed via `adapt_renderer_for_consumer()` in `manifest_builder.py` which falls back to `raw_json`.

### 6. Does the memo stay disciplined against drift?

Yes. The memo does not propose generic consumer architecture. It does not propose a consumer plugin system. It does not propose generic consumer discovery. It explicitly prohibits replacing the closed set with generic consumer discovery. The out-of-scope list is comprehensive and the acceptance bar is bounded.

---

## Strategic Assessment

This slice passes the distilled strategic roadmap's decision heuristic:

1. **Does this move intelligence upstream into analyzer-v2?** — Yes. It extends the transient compose substrate to serve a second consumer without host-local analytical reconstruction.
2. **Does this reduce host-specific analytical behavior?** — Yes. The canary-side implementation should be a thin compose client, not analytical logic.
3. **Does this strengthen generic law rather than one more special case?** — Yes. Proving the compose substrate serves two consumers strengthens the generality claim more than proving another composition family on the same consumer.
4. **Does this help eventual contract-based generality?** — Yes. The proof would demonstrate that the served response shape and adaptation machinery are consumer-portable.

The slice is also appropriately bounded. It does not claim more than one consumer, one proof path, and one proof record. It is the smallest honest next move for Phase E.

---

## Bottom Line

The memo is strategically sound, code-accurate, and well-bounded. Proceed with implementation.
