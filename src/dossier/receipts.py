"""Receipts — one row per model/image call (lifted from veo2/engine/receipts.py).

A receipt records what was asked (prompt hash), which model, what came back
(result hash), the usage and the cost. Prices are a small operator-editable
table; an unknown model is recorded with cost 0 and flagged `unpriced` in the
label so it is surfaced, never hidden.
"""
from __future__ import annotations

import hashlib
import logging
from typing import Optional

from src.dossier.schemas import Receipt

logger = logging.getLogger(__name__)

# USD per 1M tokens: (input, output). Long-context (>200K input) tiers for Sonnet 4.6.
PRICES: dict[str, tuple[float, float]] = {
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-sonnet-5": (2.0, 10.0),
    "claude-opus-4-6": (5.0, 25.0),
    "claude-opus-5": (5.0, 25.0),
    "claude-haiku-4-5": (1.0, 5.0),
    "claude-haiku-4-5-20251001": (1.0, 5.0),
    "gemini-3.1-pro-preview": (2.0, 12.0),
}
LONG_CONTEXT_PRICES: dict[str, tuple[float, float]] = {
    "claude-sonnet-4-6": (6.0, 22.5),
}


def sha256_text(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _price_for(model: str, input_tokens: int) -> Optional[tuple[float, float]]:
    key = model or ""
    if key not in PRICES:
        # tolerate dated suffixes / provider prefixes
        for known in PRICES:
            if key.startswith(known):
                key = known
                break
    if key not in PRICES:
        return None
    if input_tokens > 200_000 and key in LONG_CONTEXT_PRICES:
        return LONG_CONTEXT_PRICES[key]
    return PRICES[key]


def llm_cost(model: str, input_tokens: int, output_tokens: int) -> Optional[float]:
    price = _price_for(model, input_tokens)
    if price is None:
        return None
    return round(input_tokens / 1e6 * price[0] + output_tokens / 1e6 * price[1], 6)


def make_receipt(
    *,
    step: str,
    kind: str = "llm",
    model: str,
    label: str = "",
    input_tokens: int = 0,
    output_tokens: int = 0,
    duration_ms: int = 0,
    prompt_text: str = "",
    result_text: str = "",
    cost_usd: Optional[float] = None,
    source_job_id: Optional[str] = None,
) -> Receipt:
    if cost_usd is None and kind == "llm":
        cost_usd = llm_cost(model, input_tokens, output_tokens)
        if cost_usd is None:
            label = (label + " [UNPRICED]").strip()
            cost_usd = 0.0
    return Receipt(
        step=step,
        kind=kind,  # type: ignore[arg-type]
        model=model,
        label=label,
        input_tokens=int(input_tokens or 0),
        output_tokens=int(output_tokens or 0),
        cost_usd=float(cost_usd or 0.0),
        duration_ms=int(duration_ms or 0),
        prompt_hash=sha256_text(prompt_text)[:16] if prompt_text else "",
        result_hash=sha256_text(result_text)[:16] if result_text else "",
        source_job_id=source_job_id,
    )


def record(job_id: str, receipt: Receipt) -> None:
    """Persist a receipt on the job (incremental — after every call)."""
    try:
        if job_id.startswith("story-"):
            from src.story.store import append_receipt as story_append

            story_append(job_id, receipt)
            return
        from src.dossier.store import append_receipt

        append_receipt(job_id, receipt)
    except Exception as exc:  # bookkeeping never kills the run
        logger.warning(f"receipt persist failed for {job_id}: {exc}")
