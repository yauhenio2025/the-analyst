"""Per-model token pricing and cost estimation for the run-event ledger.

PRICING maps a model id to (USD per 1M input tokens, USD per 1M output tokens).
Prices are Anthropic first-party API list prices as of 2026-06 (Claude) and
Google AI Studio list prices for Gemini (approximate — verify before invoicing).

The executor's "opus" tier actually sends `claude-sonnet-4-6`
(src/executor/engine_runner.py MODEL_CONFIGS), so cost is always computed from
the model id that was really sent, never from the tier name.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# model id -> ($ / 1M input tokens, $ / 1M output tokens)
PRICING: dict[str, tuple[float, float]] = {
    # --- Anthropic (ids that appear in src/executor/engine_runner.py, src/llm/, src/orchestrator/) ---
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-opus-4-6": (5.00, 25.00),
    "claude-haiku-4-5-20251001": (1.00, 5.00),
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-sonnet-4-5-20250929": (3.00, 15.00),
    "claude-sonnet-4-5": (3.00, 15.00),
    "claude-opus-4-5-20251101": (5.00, 25.00),
    "claude-opus-4-5": (5.00, 25.00),
    "claude-opus-4-7": (5.00, 25.00),
    "claude-opus-4-8": (5.00, 25.00),
    "claude-opus-5": (5.00, 25.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-fable-5-1": (10.00, 50.00),
    "claude-fable-5.1": (10.00, 50.00),
    "claude-fable-5": (10.00, 50.00),
    # --- OpenRouter frontier models (study 2026-09-04; ids are the trailing segment of `openrouter/<vendor>/<model>`) ---
    "gpt-5.6-sol": (2.00, 10.00),
    "gpt-5.6-luna": (0.20, 1.20),
    "gpt-5.6-terra": (2.00, 12.00),
    "gpt-5.5": (5.00, 30.00),
    "kimi-k2.6": (0.95, 4.00),
    "kimi-k3": (3.00, 15.00),
    "deepseek-v4-pro": (1.042, 2.085),
    "deepseek-v4-flash": (0.089, 0.177),
    "claude-sonnet-4.6": (3.00, 15.00),
    # --- Google Gemini (approximate list prices, standard context tier) ---
    "gemini-3.1-pro-preview": (2.00, 12.00),
    "gemini-3-pro-preview": (2.00, 12.00),
    "gemini-3-flash-preview": (0.50, 3.00),
    "gemini-2.5-pro": (1.25, 10.00),
    "gemini-2.5-flash": (0.30, 2.50),
}

# Family fallbacks used when an exact id is unknown (e.g. a new dated snapshot).
_FAMILY_FALLBACKS: tuple[tuple[str, tuple[float, float]], ...] = (
    ("claude-opus-", (5.00, 25.00)),
    ("claude-fable-", (10.00, 50.00)),
    ("claude-sonnet-5", (2.00, 10.00)),
    ("claude-sonnet-", (3.00, 15.00)),
    ("claude-haiku-", (1.00, 5.00)),
    ("gemini-3.1-pro", (2.00, 12.00)),
    ("gemini-3-pro", (2.00, 12.00)),
    ("gemini-2.5-pro", (1.25, 10.00)),
    ("gemini-2.5-flash", (0.30, 2.50)),
)

_warned_models: set[str] = set()


def resolve_pricing(model: Optional[str]) -> Optional[tuple[float, float]]:
    """Return (input_per_M, output_per_M) for a model id, or None if unknown.

    Accepts `openrouter/<vendor>/<model>` ids by trying the trailing segment.
    """
    if not model:
        return None
    key = model.strip()
    if key in PRICING:
        return PRICING[key]
    if key.startswith("openrouter/"):
        tail = key.split("/")[-1]
        if tail in PRICING:
            return PRICING[tail]
        key = tail
    for prefix, price in _FAMILY_FALLBACKS:
        if key.startswith(prefix):
            return price
    if key not in _warned_models:
        _warned_models.add(key)
        logger.warning("events.pricing: no pricing for model %r — cost will be null", model)
    return None


def estimate_cost(
    model: Optional[str],
    input_tokens: Optional[int],
    output_tokens: Optional[int],
) -> Optional[float]:
    """Estimate USD cost of one call. Returns None when the model is unpriced.

    Thinking tokens are billed as output tokens by Anthropic and are already
    included in the `output_tokens` usage figure the backends report.
    """
    price = resolve_pricing(model)
    if price is None:
        return None
    in_tok = int(input_tokens or 0)
    out_tok = int(output_tokens or 0)
    cost = (in_tok * price[0] + out_tok * price[1]) / 1_000_000.0
    return round(cost, 6)
