# GS Revamp: Deployed Research System

> Google Scholar research pipeline with agent-loop core (v2, live since 2026-07-02)

## Overview

`gs_revamp` is a Scholar-only backend system: take a research objective, plan a search program with **cluster strategies**, execute adaptively against live Google Scholar, return a ranked slate of papers. Deployed at https://gs-revamp-v2-sg.onrender.com (Singapore, co-located with the Postgres run store since the 2026-07-12 cutover); operators interact via `/v2/ui`. The legacy Frankfurt service (https://gs-revamp-v2.onrender.com) was DELETED from Render on 2026-07-19 (operator order) — that URL is dead; only the Singapore web + worker (+ staging pair) exist.

v1 (Apr 2026, frozen) was deterministic-heavy with 11 registered LLM seam operations (`domain/models.py:35-50`). v2 inverts to one agent per run, whole-run context, semantic judgment owned by the model. **Current state:** v2 works and won a blind A/B (5/5/4 vs v1's 3 — directionally credible but numerically inflated: v1's terminal baseline run never completed final curation, `final_paper_curation_summary: null`, status `paused`), but cluster strategist UI/cost-visibility layer is under-powered — 2-4 strategies, ~4 clusters, no cost estimates.

## Quick Reference

- Build: `uv sync --extra dev`
- Test: `uv run --extra dev pytest tests/agent/ -q` (61 tests)
- Run (local): `uv run python -m gs_revamp.agent.cli plan --objective "..."` + `approval` + `execute`
- Server: `uv run uvicorn gs_revamp.main:app --reload` (serves `/v2/ui`)
- Deploy: `https://gs-revamp-v2-sg.onrender.com` (Render Singapore, auto-deploys main; Frankfurt legacy service deleted 2026-07-19)

## Architecture Notes

### Package Structure
- **v2 (current):** `src/gs_revamp/agent/` — loop, tools, state/persistence, provider, prompts, UI
- **v1 (frozen):** `src/gs_revamp/` — deterministic stages, disabled for new work, parts donor only

### Governing Documents
- **v2 spec:** `docs/specs/2026-07-02-v2-agent-loop-rewrite-memo.md` (self-sufficient)
- **Cluster strategy vision:** `docs/decisions/2026-04-05-budgeted-cluster-strategy-and-transcluster-course-correction.md`
- **Live results log:** `docs/v2-log.md` (R6 ceremony cap: one per milestone)

### Key Concepts
- **Cluster strategist:** Agent proposes 2-4 slicing strategies (chronological/genealogical/thematic/by-industry/etc.); operator picks one
- **Plan lanes:** 4-7 research "clusters" with spine terms (required) + floating (lane-specific), term richness standard 15-40 terms/lane
- **Three phases:** Exploration (vocab harvest) → Targeting (exploit anchors) → Citation Expansion (walk cited-by)
- **Budget as central constraint:** 30 queries (configurable), allocated across lanes; agent adapts (BROADEN/TIGHTEN/PRUNE/GO-DEEPER/WALK/ABANDON)
- **Query-budget sovereignty (operator policy, 2026-07-19):** the user's query
  count is THE depth directive and outranks every other budget. Cost/wall-clock/
  model-call ceilings are runaway backstops auto-sized ABOVE the query program
  (fleet $/query × margin), never depth controls. A run must never terminate for
  cost before its query budget is spent. Explicit contradictions (user sets both,
  incompatibly) are resolved at CREATION, loudly — never accepted-then-truncated.
  Governed users' quotas are enforced at creation against expected cost, not
  mid-run by silent truncation. (Incident: agent_e152f4dfaf, 28/130 at a $5
  default cap.)
- **Truth artifact:** R5 honesty — actual transport per query, actual model per call, simulated vs live provenance

### Recent Work (v2 milestones, 2026-07-02)
- M0-M5: Core loop, approval gate, live validation, A/B eval (v2 won)
- Post-M5: Strategist layer (ask_operator + propose_plan), repertoire robustness, results browser
- Deployment: Live at gs-revamp-v2-sg.onrender.com (Singapore web + worker + Postgres run store since 2026-07-12; Frankfurt legacy service deleted from Render 2026-07-19)
- Current gap: Cost visibility + more cluster/strategy diversity

## Code Conventions
- Prompts: ONE system_prompt + ONE execution_preamble; edit in place (`prompts.py`), no versioning
- No semantic Python policy (R1): all judgment in the model, Python owns transport/truth/limits/lifecycle only
- Tools are thin wrappers: Oxylabs → text, truth ledger, state mutation — no logic
- Testing: ~950 tests in `tests/agent/` (offline loop, approval, resume, compaction, gates, scorecard, lab); v1's frozen tests do not run
- Commits: After every substantive change (R8); `docs/v2-log.md` + CHANGELOG on release
- Latency work goes to COMPLETION budgets, never context trims (field study
  P3.3 standing rule — latency is completion-bound, corr +0.90 three-arm
  converged; context diet buys money, not speed)

## Determinism Guardrails (R10–R13 — binding on every change; adopted 2026-07-18)

The four-study audit (`communications/STATE_OF_PLAY_{1,2,3,4}_*.md`, read before
any gate/doctrine/verifier work) found v2 clean of v1's disease — no semantic
judgment in Python — but accreting a *process-governance* layer at v1's growth
rate: 32–49% of run model-spend was harness negotiation; on one run, gate
traffic exceeded search traffic; the agent's best moves increasingly came from
verifier coercion rather than its own judgment. These rules exist so future
sessions do not smuggle determinism back in through procedure:

- **R10 — every constraint pays rent.** A new mechanical gate ships with a
  retirement criterion the same way it ships with a deadlock argument ("~0
  bounces in N runs = deterrent, or ≥X rescued yield; failing both → demote").
  The scorecard's friction metrics are the ledger. The demotion path (gate →
  verifier feed → doctrine line → deleted) is as legitimate as the promotion
  path. No gate is permanent; none has tenure.
- **R11 — feed, don't gate.** Before proposing ANY new bounce/refusal path,
  write down the feed alternative: surface the same evidence *to the agent at a
  decision moment* (card boundary, pressure-window entry) instead of to a
  verifier after the fact. New rejection paths and new mid-run verifiers
  require explicit operator sign-off; new context feeds don't. The bounce
  surface is already the dominant motor routine — hold the line.
- **R12 — doctrine stays lean.** A standing prompt rule that a mechanical gate
  already enforces is DELETED, not kept as lore (double-enforcement is
  attention theft — Study 3: the curriculum was ¾ rules and predicted the exact
  box-ticking pathologies the critics kept finding). Prefer principles over
  procedures; no new NEVER/MUST without a measured incident; every new recital
  names the measured confabulation it prevents.
- **R13 — judgment placement.** When the engine computes evidence, its default
  recipient is the agent *before* it decides, not a prosecutor after. Model-
  owned waivers-with-audit beat hard thresholds (measured: run A's accepted IIS
  waiver refuted the deep-page gate's premise). A magic-number threshold that
  overrules a model verdict on a semantic question is presumptively wrong —
  S8 (`seed_high_citation_depth`) ended its probation DELETED (2026-08-08:
  its page=3 direction manufactured the non-contiguous walk it then
  prosecuted — ADJUDICATION T1); its replacement is the canonical seed-table
  facts (missing indices, deepest page), fed not enforced.

- **R14 — the dead-channel law (measured 2026-07-18, three independent ways;
  `communications/MAX_EFFECT_VERDICTS_2026-07-18.md`).** Doctrine-only prompt
  text does NOT change motor behavior (0% and 2/7 adoption in controlled
  forks); context feeds and tool-schema shapes do (100% uptake). Never ship a
  behavioral change as a doctrine bullet alone — ride it on a feed or a schema
  field, and reserve doctrine for research principles.

Litmus for any proposed change: does it make the agent a better researcher, or
a better litigant? If the honest answer is "litigant," redesign it.

## Documentation
- Feature inventory: `docs/FEATURES.md` (read on demand)
- Change history: `docs/CHANGELOG.md` (read on demand)
- Current tasks: `docs/CURRENT-TASKS.md` (task tracking across sessions)
