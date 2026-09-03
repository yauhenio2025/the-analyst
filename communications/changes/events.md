# Events agent (E1) — change notes for `feat/events`

> Per-call **run-event ledger + SSE stream** for the multi-phase executor
> (job → phase → chain → engine → pass → LLM call), with prompt/output excerpts,
> tokens, cost, duration, a one-line human `detail` per event and a Haiku
> narration per phase. Integrator: fold the CHANGELOG/FEATURES entries below into
> `docs/CHANGELOG.md` / `docs/FEATURES.md`.

Sample job used for verification: **`job-plan-d87b85c590db`** (workflow
`concept_inferential_single_concept`, engine `inferential_commitment_mapper`,
13.7K-char excerpt of the Kering study). Transcript of the full event stream:
`communications/changes/events-sample.jsonl` (one RunEvent JSON per line, as
received over SSE). See "Verification" at the end.

---

## CHANGELOG entries (for `docs/CHANGELOG.md` → [Unreleased])

### Added
- Run-event ledger: table `run_events` (lazy `CREATE TABLE IF NOT EXISTS` on both executor DB backends) with Pydantic `RunEvent`/`JobSummary` schemas, `append_event` / `list_events` / `job_summary` store API, per-model pricing + `estimate_cost`, and a `contextvars` execution context ([src/events/store.py](../../src/events/store.py), [src/events/schemas.py](../../src/events/schemas.py), [src/events/pricing.py](../../src/events/pricing.py), [src/events/context.py](../../src/events/context.py)).
- Executor hooks emitting `job_started/finished/failed`, `phase_started/finished`, `chain_started/finished`, `call_started/finished/failed` and `note` events, each with a one-sentence `detail` ([src/events/hooks.py](../../src/events/hooks.py); call sites in [src/executor/engine_runner.py](../../src/executor/engine_runner.py), [src/executor/chain_runner.py](../../src/executor/chain_runner.py), [src/executor/workflow_runner.py](../../src/executor/workflow_runner.py), [src/orchestrator/pipeline.py](../../src/orchestrator/pipeline.py)).
- Phase narrator: at `phase_started`, a daemon thread asks `claude-haiku-4-5-20251001` for one executive-reader sentence ("what this step does with the previous step's output and why") and emits a `narration` event; cached in memory by `(workflow_key, phase_key)`; silent without `ANTHROPIC_API_KEY` or with `EVENTS_NARRATOR=off` ([src/events/narrator.py](../../src/events/narrator.py)).
- Events API: `GET /v1/events/{job_id}?after=&limit=`, `GET /v1/events/{job_id}/summary`, `GET /v1/events/{job_id}/stream` (SSE: replay from `after`, 1s poll, `: heartbeat` every 15s, closes 5s after `job_finished`/`job_failed`) plus aliases `GET /v1/executor/jobs/{job_id}/events`, `/events/summary`, `/events/stream` ([src/api/routes/events.py](../../src/api/routes/events.py), [src/api/routes/executor.py](../../src/api/routes/executor.py), mounted in [src/api/main.py](../../src/api/main.py)).
- Tests: `tests/test_events_store.py` (SQLite temp DB: append/list/seq monotonicity/concurrency/summary/pricing/context/hooks/narrator cache + `/v1/events` JSON and SSE routes) ([tests/test_events_store.py](../../tests/test_events_store.py)).

### Fixed
- Anthropic SDK 1.x compatibility: every Anthropic client was constructed with `httpx.Timeout(...)`, which anthropic ≥1.0 (built on `httpx2`) rejects at request time as a bare `APIConnectionError: Connection error.` (`TypeError: 'Timeout' object cannot be interpreted as an integer`). All sites now use `src.llm.backends.sdk_timeout(**kw)` → `anthropic.Timeout`, which is the SDK's own alias in both 0.x and 1.x ([src/llm/backends.py](../../src/llm/backends.py), [src/llm/client.py](../../src/llm/client.py), [src/orchestrator/planner.py](../../src/orchestrator/planner.py), [src/orchestrator/sampler.py](../../src/orchestrator/sampler.py)). Without this, no engine call succeeds in the shared venv (anthropic 1.3.0) — and `requirements.txt` pins only `anthropic>=0.42.0`, so a fresh Render build would hit the same failure.

---

## FEATURES entries (for `docs/FEATURES.md`)

## Observability

### Run-event ledger (`run_events`)
- **Status**: Active
- **Description**: Per-call event log for executor jobs — job → phase → chain → engine → pass → LLM call — with prompt hash/excerpts, output excerpt, tokens, estimated cost, duration, one human `detail` sentence per event and an optional narrator line. Never raises into the executor.
- **Entry Points**:
  - `src/events/schemas.py:16` - `EVENT_KINDS` (13 kinds) and `TERMINAL_KINDS`
  - `src/events/schemas.py:35` - `RunEvent` (Pydantic v2; `payload` = parsed `payload_json`)
  - `src/events/schemas.py:74-102` - `PhaseSummary`, `JobSummary`
  - `src/events/store.py:52-101` - `_create_sql()` / `ensure_table()` — lazy `CREATE TABLE IF NOT EXISTS run_events` + unique index `(job_id, seq)` on Postgres (`SERIAL`) or SQLite (`AUTOINCREMENT`) via `src/executor/db.py` connection helpers
  - `src/events/store.py:119-136` - `prompt_hash()` (sha256 system+user), `prompt_excerpt()` (2000 system + `\n---\n` + 1000 user), `output_excerpt()` (2000)
  - `src/events/store.py:166` - `append_event(job_id, kind, **fields) -> seq` (0 on failure; auto-estimates `cost_usd` from model+tokens; unknown kwargs fold into payload)
  - `src/events/store.py:299` - `list_events(job_id, after_seq=0, limit=1000)`
  - `src/events/store.py:348` - `job_summary(job_id)` → `{status, calls, failed_calls, input_tokens, output_tokens, cost_usd, duration_ms, phases[...], events, last_seq, started_at, last_event_at}`
  - `src/events/pricing.py:18` - `PRICING` ($/M input, $/M output per model id) and `src/events/pricing.py:79` `estimate_cost(model, in_tok, out_tok)` (None for unpriced models; family-prefix fallback)
  - `src/events/context.py:32-65` - `current()/push()/pop()/scope()` ContextVar helpers and `phase_key()` (`"1.0"`, `"1.5"`)
- **Dependencies**: `src/executor/db.py` (dual backend), Pydantic v2
- **Added**: 2026-09-03

### Executor event hooks
- **Status**: Active
- **Description**: Exception-proof helpers that translate executor state changes into ledger events (with a human sentence each) and kick off the narrator at phase start.
- **Entry Points**:
  - `src/events/hooks.py:131` - `job_started(job_id, plan, workflow)` — payload lists every phase with engines/chain/depends_on/depth/model_hint
  - `src/events/hooks.py:180` - `job_finished(job_id, status, error)` → `job_finished` (completed) or `job_failed` (payload.status = failed | cancelled) with ledger totals
  - `src/events/hooks.py:233` - `phase_started(job_id, plan, wf_phase, plan_phase, workflow)` (+ narrator kick-off)
  - `src/events/hooks.py:311` - `phase_finished(job_id, plan_phase, result)` (per-phase calls/tokens/cost from the ledger, output excerpt)
  - `src/events/hooks.py:371-390` - `chain_started` / `chain_finished`
  - `src/events/hooks.py:427-511` - `call_started` / `call_finished` / `call_failed` (used by engine_runner; `call_failed` carries `attempt`, `will_retry`, `retry_delay_s`)
  - `src/executor/engine_runner.py:254-256` - reads the event context; `:272` call_started per attempt; `:314` call_finished; `:346` call_failed
  - `src/executor/chain_runner.py:118` - chain_started; `:182` context scope (job/phase/chain/work) around `_run_engine_passes`; `:217` chain_finished; `:388` per-pass scope (engine/pass_name/stance) around `run_engine_call_auto`; `:532` whole-engine scope; `:645` single-engine scope
  - `src/executor/workflow_runner.py:144-145` - job context + job_started; `:324` phase_started (single); `:352` phase_started (parallel group); `:371,383,398,422,427` job_finished (cancelled/failed/completed/InterruptedError/exception); `:409-411` auto-presentation notes; `:582` phase_finished (in `_record_phase_result`)
  - `src/orchestrator/pipeline.py:188,209,232` - `note` events (documents stored, plan generation started, plan ready); `:283` job_failed when the pipeline fails before execution
- **Dependencies**: Run-event ledger
- **Added**: 2026-09-03

### Phase narrator
- **Status**: Active
- **Description**: One plain-language sentence per phase for an executive reader, generated by `claude-haiku-4-5-20251001` from the phase spec (name, description, engines + problematiques, context_parameters, depends_on) and the plan's `strategy_summary` / `decision_trace.overall_strategy_rationale` / `context_emphasis` / `rationale`. Emitted as a `narration` event (`narrator` field). In-memory cache keyed by `(workflow_key, phase_key)`; runs in a daemon thread; skipped silently without `ANTHROPIC_API_KEY` or with `EVENTS_NARRATOR=off`.
- **Entry Points**:
  - `src/events/narrator.py:25-41` - `NARRATOR_MODEL`, `SYSTEM_PROMPT`
  - `src/events/narrator.py:54` - `build_narration_prompt(phase_spec, plan_context)`
  - `src/events/narrator.py:115` - `call_narrator(prompt)` (Anthropic SDK `messages.create`, 160 max tokens, 30s timeout)
  - `src/events/narrator.py:151` - `narrate_phase_async(job_id, workflow_key, phase_key, phase_spec, plan_context)`
- **Dependencies**: `anthropic` SDK, Run-event ledger
- **Added**: 2026-09-03

### Events API + SSE stream
- **Status**: Active
- **Description**: Read side of the ledger for consoles: JSON list, aggregate summary, and a Server-Sent-Events stream that replays then follows a job live.
- **Entry Points**:
  - `src/api/routes/events.py:34` - router (`prefix="/v1/events"`, mounted without extra prefix in `src/api/main.py:289`)
  - `src/api/routes/events.py:132` - `GET /v1/events/{job_id}?after=&limit=` → `list[RunEvent]`
  - `src/api/routes/events.py:141` - `GET /v1/events/{job_id}/summary` → `JobSummary`
  - `src/api/routes/events.py:146` - `GET /v1/events/{job_id}/stream?after=&idle_timeout=` → `text/event-stream` (`event_stream()` at `:65`)
  - `src/api/routes/executor.py:773-789` - aliases `GET /v1/executor/jobs/{job_id}/events`, `/events/summary`, `/events/stream` (thin delegations)
- **Dependencies**: FastAPI `StreamingResponse`, Run-event ledger
- **Added**: 2026-09-03

## LLM Infrastructure (modified)

### Anthropic client timeouts (`sdk_timeout`)
- **Status**: Active
- **Description**: Version-agnostic timeout construction for Anthropic clients (anthropic 0.x/httpx and ≥1.x/httpx2).
- **Entry Points**:
  - `src/llm/backends.py:54` - `sdk_timeout(**kwargs)`; used at `src/llm/backends.py:202,314`, `src/llm/client.py:48`, `src/orchestrator/planner.py:131,295,455`, `src/orchestrator/sampler.py:169`
- **Modified**: 2026-09-03

---

## New dependencies

None at runtime (uses `anthropic`, `fastapi`, `pydantic`, `psycopg2`/`sqlite3` already in `requirements.txt`). `pytest` is needed to run the tests; it is not in `requirements.txt` (the existing test suite already assumed it) and was installed into the shared venv.

---

## Contract as implemented

### 1. Storage — table `run_events`
Created lazily (`CREATE TABLE IF NOT EXISTS`) through `src/executor/db.get_connection()` on Postgres (`EXECUTOR_DATABASE_URL`) or SQLite (`src/executor/executor.db`); `db.py` itself is untouched.

| column | type | notes |
|---|---|---|
| id | pk (`SERIAL` / `INTEGER AUTOINCREMENT`) | |
| job_id | TEXT NOT NULL | executor job id (dossier jobs may use their own ids) |
| seq | INTEGER NOT NULL | monotonic per job, 1-based; `UNIQUE (job_id, seq)` index (`idx_run_events_job_seq`) |
| ts | TEXT | ISO-8601 UTC with offset, e.g. `2026-09-03T11:10:31.123456+00:00` |
| kind | TEXT | one of `job_started, job_finished, job_failed, phase_started, phase_finished, chain_started, chain_finished, call_started, call_finished, call_failed, narration, artifact, note` |
| phase | TEXT | phase key `"1.0"`, `"1.5"`, `"2.0"` (= executor `phase_statuses` keys) |
| chain, engine, pass_name, stance, work_key | TEXT | `pass_name` = `"Pass 2: Conflict Mapping & Dependency Analysis"`; `"Pass 1: whole-engine"` for engines without pass definitions |
| model | TEXT | the model id actually sent (`claude-sonnet-4-6` for the "opus" tier) |
| input_chars, output_chars, input_tokens, output_tokens | INTEGER | |
| cost_usd | REAL | estimated from `PRICING` when not supplied; NULL for unpriced models |
| duration_ms | INTEGER | |
| prompt_hash | TEXT | sha256(system + user) |
| prompt_excerpt | TEXT | first 2000 chars of system + `"\n---\n"` + first 1000 of user |
| output_excerpt | TEXT | first 2000 chars of output |
| detail | TEXT | one human sentence (≤1000 chars) |
| narrator | TEXT | LLM one-liner (narration events only) |
| payload_json | TEXT | JSON object with everything else (see per-kind payloads below) |

Extra index `idx_run_events_job_kind (job_id, kind)`.

### 2. Python API — `src/events/store.py`
- `append_event(job_id: str, kind: str, **fields) -> int` — returns `seq`; **never raises**, returns `0` if the write failed (logged). Recognised kwargs = the columns above (+ `ts`, `payload: dict`); any other kwarg is folded into `payload`. Excerpts/detail are truncated on write.
- `list_events(job_id: str, after_seq: int = 0, limit: int = 1000) -> list[dict]` — rows ordered by `seq`, with `payload` parsed (dict) instead of `payload_json`.
- `job_summary(job_id) -> dict` — `{calls, input_tokens, output_tokens, cost_usd, duration_ms, phases}` **plus** `status` (`running|completed|failed|cancelled|unknown`), `failed_calls`, `events`, `last_seq`, `started_at`, `last_event_at`. `calls` counts `call_finished`; `duration_ms` is wall-clock first event → terminal event (or last event). Each entry of `phases` = `{phase, name, status, calls, input_tokens, output_tokens, cost_usd, duration_ms, narrator, engines, started_at, finished_at}`.
- Also exported: `prompt_hash`, `prompt_excerpt`, `output_excerpt`, `last_seq`, `has_terminal_event`, `ensure_table`, `reset_for_tests`.
- Schemas: `src/events/schemas.py` — `RunEvent` (all columns; `payload: dict`), `PhaseSummary`, `JobSummary`, `EVENT_KINDS`, `TERMINAL_KINDS`.

### 3. Cost — `src/events/pricing.py`
`PRICING[model_id] = (usd_per_M_input, usd_per_M_output)`: `claude-sonnet-4-6` (3/15), `claude-opus-4-6` (5/25), `claude-haiku-4-5[-20251001]` (1/5), `claude-sonnet-4-5[-20250929]` (3/15), `claude-opus-4-5[-20251101]` (5/25), `claude-opus-4-7/4-8/5` (5/25), `claude-sonnet-5` (2/10), `gemini-3.1-pro-preview` / `gemini-3-pro-preview` (2/12), `gemini-3-flash-preview` (0.5/3), `gemini-2.5-pro` (1.25/10), `gemini-2.5-flash` (0.3/2.5). Claude prices are current Anthropic list prices; **Gemini prices are approximate list prices — verify before invoicing.** `estimate_cost(model, in_tok, out_tok)` → float (6 dp) or `None` when unpriced (family-prefix fallback for dated snapshots and `openrouter/<vendor>/<model>` ids; one warning per unknown model). Thinking tokens are already inside Anthropic's `output_tokens` and are recorded in `payload.thinking_tokens`.

### 4. Hooks
- **engine_runner.run_engine_call** — reads `src.events.context.current()`; when it contains `job_id` (i.e. the call originates from an executor job) emits `call_started` before **each attempt** (payload: `attempt`, `max_attempts`, `label`, `effort`, `mode` sync|streaming, `use_1m_context`, `max_tokens`, `system_chars`, `user_chars`), `call_finished` on success (tokens from the backend `usage`, `duration_ms`, `cost_usd`, excerpts, payload `thinking_tokens`, `partial`, `attempt`), `call_failed` on each failed attempt (payload `attempt`, `will_retry`, `retry_delay_s`, `error`). Calls made outside an executor job (presenter, planner, narrator) are not logged.
- **chain_runner** — `run_chain` emits `chain_started`/`chain_finished` and wraps each engine in a context scope `{job_id, phase, chain, work_key}`; `_run_engine_passes` / `_run_single_engine_call` wrap each LLM call in `{engine, pass_name, stance, work_key}`; `run_single_engine` scopes `{job_id, phase, chain=None, work_key}`. Per-work and parallel-phase thread pools are covered because chain_runner sets the fields from its own arguments (ContextVars do not cross threads).
- **workflow_runner** — `job_started` once the plan + workflow are resolved (payload: `workflow_key`, `workflow_name`, `plan_id`, `thinker_name`, `target_title`, `prior_works`, `phases[{phase, phase_name, engines, chain, depends_on, depth, model_hint, skip, iteration_mode}]`, `estimated_llm_calls`, `execution_model`, `strategy_summary`); `phase_started` before every `run_phase` (single and parallel groups; payload: `phase_name`, `description`, `engines`, `engine_details[{key,name,problematique}]`, `chain`, `depends_on`, `depth`, `model_hint`, `iteration_mode`, `context_emphasis`, `rationale`, `context_parameters`, `skip`, `skip_reason`, `requires_full_documents`); `phase_finished` in `_record_phase_result` (payload: `phase_name`, `status` completed|failed|skipped, `error`, `total_tokens`, `calls`, `engines`, `works`; columns `duration_ms`, tokens, `cost_usd`, `output_excerpt`); `job_finished` on completion; `job_failed` on failure **and on cancellation** (payload `status: "failed" | "cancelled"`, `error`, `calls`, `failed_calls`, per-phase mini summary). Two `note` events bracket auto-presentation (after `job_finished`).
- **orchestrator/pipeline** (addition beyond the three listed files): `note` events for "documents stored", "plan generation started", "plan ready" so a console shows activity during the 15-120s before `job_started`; `job_failed` if the pipeline fails before execution.
- All hooks are wrapped (`@_safe`) and the store itself swallows errors; a broken ledger can only log warnings.

### 5. Narration — `src/events/narrator.py`
At `phase_started` (non-skipped phases) → `narrate_phase_async(...)`: cache hit → immediate `narration` event (`payload.cached=true`); miss → daemon thread calls `claude-haiku-4-5-20251001` (`messages.create`, `max_tokens=160`, 30s timeout, 1 retry) and emits `narration` with `narrator` = the sentence, `detail` = same, `model` = the narrator model, payload `{cached, model, latency_ms}`. Prompt = phase name/description, engines (name + problematique from the capability definition), chain, depth, iteration mode, context_parameters, upstream phases (number + name), planner `context_emphasis`/`rationale`, and the plan's `strategy_summary` + `decision_trace.overall_strategy_rationale` when present. Skipped silently when `ANTHROPIC_API_KEY` is unset or `EVENTS_NARRATOR=off`.

### 6. API — `src/api/routes/events.py` (+ aliases in `executor.py`)
- `GET /v1/events/{job_id}?after=<seq>&limit=<1..10000>` → JSON array of `RunEvent`.
- `GET /v1/events/{job_id}/summary` → `JobSummary`.
- `GET /v1/events/{job_id}/stream?after=<seq>&idle_timeout=<s>` → `text/event-stream`; first frame is a comment `: stream job=… after=…`; each event frame is `event: run_event` / `id: <seq>` / `data: <RunEvent JSON>`; store polled every 1s; `: heartbeat` every 15s while idle; closes (`: closed …`) once a `job_finished`/`job_failed` frame was sent and no further event arrived for 5s; also closes on client disconnect or after `idle_timeout` (default 3600s) without events. Headers: `Cache-Control: no-cache, no-transform`, `X-Accel-Buffering: no`.
- Aliases: `GET /v1/executor/jobs/{job_id}/events`, `/events/summary`, `/events/stream` (same parameters).
- CORS: the app-wide `CORSMiddleware(allow_origins=["*"])` covers the new routes (verified with an `OPTIONS` preflight from `http://localhost:5173`).
- Unknown job ids return `[]` / an empty summary (status `unknown`) rather than 404, because dossier jobs may append their own ids to the ledger before/without an executor job.

### Deviations / additions to state explicitly
1. `RunEvent`/API JSON expose the payload as a parsed object named **`payload`** (not the raw `payload_json` string).
2. `job_summary()` returns the six required keys **plus** `status`, `failed_calls`, `events`, `last_seq`, `started_at`, `last_event_at`, and `phases` entries are objects (see §2).
3. `call_started` is emitted per **attempt** (a retry produces a new `call_started`), so a console pairing start/finish should key on `payload.attempt`.
4. There is no `job_cancelled` kind: cancellation is `job_failed` with `payload.status = "cancelled"`.
5. `append_event` returns `0` (not an exception) when the write fails; real sequence numbers start at 1.
6. Extra module `src/events/hooks.py` (executor-facing helpers) beyond the files named in the contract; extra `note` hooks in `src/orchestrator/pipeline.py`; incidental `sdk_timeout` fix in `src/llm/backends.py`, `src/llm/client.py`, `src/orchestrator/planner.py`, `src/orchestrator/sampler.py` (see Fixed).
7. Gemini pricing values are approximations (see §3).
8. `src/executor/executor.db` is a **tracked binary** in this repo (inherited from analyzer-v2); running local jobs modifies it. It was deliberately left unstaged on this branch; `-shm`/`-wal` sidecars are untracked and also unstaged.

---

## Verification

(see below — filled in after the sample run)
