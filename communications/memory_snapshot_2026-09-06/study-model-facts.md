---
name: study-model-facts
description: Model ids, prices and quirks used by the engine studies (Fable via Anthropic; Sol, Luna, Kimi, DeepSeek via OpenRouter)
metadata:
  type: reference
---

Model ids the study scripts use: `claude-fable-5-1` and `claude-sonnet-4-6` direct; via OpenRouter (prefix `openrouter/`): `openai/gpt-5.6-sol` ($2/$10 per M), `openai/gpt-5.6-luna` ($0.2/$1.2), `moonshotai/kimi-k2.6` ($0.95/$4), `deepseek/deepseek-v4-pro` ($1.04/$2.09), `deepseek/deepseek-v4-flash` ($0.09/$0.18). Fable is $10/$50 (the v2 script's $15/$75 was an over-estimate). Prices live in `src/events/pricing.py` keyed by the trailing id segment.

Quirks (2026-09-05): Kimi K3 (`moonshotai/kimi-k3`, $3/$15) replaced K2.6, which is slow (474 s a call). Fable refuses the OLD four-stance prompts on any material (16/16 passes on two papers) but accepts the redesigned prompts; its billed output includes hidden reasoning (25K tokens for 34K chars); its critic step wrote 56K chars and needs `LLM_SYNC_HARD_TIMEOUT_SECONDS=1500`. OpenRouter streams sometimes end early (three truncated runs in 91; no error raised) and DeepSeek Flash chains take 13–38 min. DeepSeek formats ledger rows loosely (bare rows, page refs, quote in the finding); the walls now accept these. GPT-5.6 Sol as a pairwise judge picks the first-seen reading (80/87) and rates GPT-family outputs ~1 point higher; Sonnet as judge shows no position lean. Fable rejects forced tool_choice (dossier `call_json` answers JSON as text for it) and refuses some pass-1 prompts over defence material (`stop_reason: refusal`; the runner falls back once to Sonnet). OpenRouter calls stream with `reasoning.effort: low` and a 120s heartbeat. `OPENROUTER_API_KEY` is in `.env` locally and on Render.

**How to apply:** verify ids against `https://openrouter.ai/api/v1/models` (free) before a new study; the list was checked 2026-09-04. Related: [[engine-redesign-process-shape]].
