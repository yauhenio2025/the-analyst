"""Image provider registry — the still-figure fleet for The Analyst.

Lifted from veo2/engine/images.py (registry shape, key gating, cost table,
size-per-aspect tables) and analyzer/src/llm/gemini.py (SDK model ids).
One registry, one cost table: callers record the number this module returns
at call time, so a later price edit never rewrites history.

Provider keys (the contract other agents build against):
  gemini_pro        gemini-3-pro-image-preview   (google-genai SDK; REST fallback)
  gemini_flash      gemini-3.1-flash-image-preview
  seedream_5_pro    doubao-seedream-5-0-pro-260628 (Volcengine Ark images/generations)
  qwen_image_2_pro  qwen-image-2.0-pro            (DashScope multimodal generation, 2 rpm)

Gemini accepts either GEMINI_API_KEY or GOOGLE_VEO_API_KEY (veo2's house
name for the same Google AI Studio key).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# .env loading (once, at import, never overriding real environment)
# ---------------------------------------------------------------------------

_ENV_LOADED = False


def _load_env() -> None:
    """Load the repo-root .env once (python-dotenv, optional). Real env wins."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    _ENV_LOADED = True
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return
    root = Path(__file__).resolve().parents[2]
    env_file = root / ".env"
    if env_file.exists():
        load_dotenv(env_file, override=False)


_load_env()

# ---------------------------------------------------------------------------
# Size tables. "1K" / "2K" / "4K" are the caller-facing size classes; each
# provider maps a (size, aspect) pair to what its API actually accepts.
# ---------------------------------------------------------------------------

GEMINI_ASPECTS = ("1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9")

# Ark (Seedream 5.0 Pro) takes free-form WxH. ≤2.36 MP is the cheap tier;
# the >2.36 MP tier costs more AND scored worse in the bench, so 4K is not
# offered — it coerces to 2K.
ARK_SIZES: dict[str, dict[str, str]] = {
    "1K": {"16:9": "1472x832", "9:16": "832x1472", "1:1": "1024x1024",
           "4:3": "1152x864", "3:4": "864x1152", "3:2": "1248x832", "2:3": "832x1248"},
    "2K": {"16:9": "1920x1080", "9:16": "1080x1920", "1:1": "1440x1440",
           "4:3": "1664x1248", "3:4": "1248x1664", "3:2": "1728x1152", "2:3": "1152x1728"},
}

# DashScope (Qwen-Image 2.0 Pro) takes W*H (asterisk) in the 1K class only.
DASHSCOPE_SIZES: dict[str, dict[str, str]] = {
    "1K": {"16:9": "1664*928", "9:16": "928*1664", "1:1": "1328*1328",
           "4:3": "1472*1140", "3:4": "1140*1472", "3:2": "1584*1056", "2:3": "1056*1584"},
}

# Reference images are bounded to this long edge before upload (a 4K ref
# timed out against cn-beijing; Anthropic vision also resizes above this).
REF_MAX_EDGE = 1568

# ---------------------------------------------------------------------------
# The registry
# ---------------------------------------------------------------------------

PROVIDERS: dict[str, dict[str, Any]] = {
    "gemini_pro": {
        "api": "gemini",
        "model": "gemini-3-pro-image-preview",      # google-genai SDK id (analyzer v1)
        "rest_model": "gemini-3-pro-image",         # interactions-endpoint id (veo2 fallback)
        "label": "Nano Banana Pro (Gemini 3 Pro Image)",
        "usd_per_image": 0.134,                     # 1K/2K tier
        "usd_by_size": {"1K": 0.134, "2K": 0.134, "4K": 0.24},
        "rpm": 60,
        "keys_any": ("GEMINI_API_KEY", "GOOGLE_VEO_API_KEY"),
        "sizes": ("1K", "2K", "4K"),
        "aspects": GEMINI_ASPECTS,
        "max_refs": 14,
        "supports_edit": True,
        "timeout_s": 600,
    },
    "gemini_flash": {
        "api": "gemini",
        "model": "gemini-3.1-flash-image-preview",
        "rest_model": "gemini-3.1-flash-image",
        "label": "Nano Banana 2 (Gemini 3.1 Flash Image)",
        "usd_per_image": 0.067,
        "usd_by_size": {"1K": 0.067, "2K": 0.067},
        "rpm": 60,
        "keys_any": ("GEMINI_API_KEY", "GOOGLE_VEO_API_KEY"),
        "sizes": ("1K", "2K"),
        "aspects": GEMINI_ASPECTS,
        "max_refs": 14,
        "supports_edit": True,
        "timeout_s": 300,
    },
    "seedream_5_pro": {
        "api": "ark",
        "model": "doubao-seedream-5-0-pro-260628",
        "label": "Seedream 5.0 Pro (Volcengine Ark)",
        "usd_per_image": 0.06,                      # ≤2.36 MP tier (+$0.003 per extra ref)
        "usd_by_size": {"1K": 0.06, "2K": 0.06},
        "usd_per_extra_ref": 0.003,
        "rpm": 30,
        "keys_any": ("ARK_API_KEY",),
        "sizes": tuple(ARK_SIZES),
        "aspects": tuple(ARK_SIZES["2K"]),
        "max_refs": 7,
        "supports_edit": False,
        "timeout_s": 300,
    },
    "qwen_image_2_pro": {
        "api": "dashscope-mm",
        "model": "qwen-image-2.0-pro",
        "label": "Qwen-Image 2.0 Pro (DashScope)",
        "usd_per_image": 0.075,
        "usd_by_size": {"1K": 0.075},
        "rpm": 2,                                   # per-model per-key; parallelism does not help
        "keys_any": ("DASHSCOPE_API_KEY",),
        "sizes": tuple(DASHSCOPE_SIZES),
        "aspects": tuple(DASHSCOPE_SIZES["1K"]),
        "max_refs": 3,
        "supports_edit": False,
        "timeout_s": 300,
    },
}

DEFAULT_PROVIDER = "gemini_pro"


class UnknownImageProvider(ValueError):
    pass


def provider_info(provider_key: str) -> dict[str, Any]:
    try:
        return PROVIDERS[provider_key]
    except KeyError:
        raise UnknownImageProvider(
            f"unknown image provider {provider_key!r}; known: {sorted(PROVIDERS)}"
        ) from None


def provider_api_key(provider_key: str) -> str | None:
    """First configured credential among the provider's accepted env names."""
    for name in provider_info(provider_key)["keys_any"]:
        val = os.environ.get(name)
        if val:
            return val
    return None


def is_available(provider_key: str) -> bool:
    return provider_api_key(provider_key) is not None


def available_providers() -> list[str]:
    """Registry order, filtered by configured credentials. An unconfigured
    provider is absent, not disabled (veo2's key-gate pattern)."""
    return [k for k in PROVIDERS if is_available(k)]


def coerce_size(provider_key: str, size: str) -> str:
    """Nearest size class the provider supports (4K→2K on Seedream, 2K→1K on Qwen)."""
    info = provider_info(provider_key)
    size = (size or "2K").upper()
    if size in info["sizes"]:
        return size
    order = ["1K", "2K", "4K"]
    if size not in order:
        raise ValueError(f"size {size!r} not one of {order}")
    idx = order.index(size)
    for candidate in reversed(order[: idx + 1]):
        if candidate in info["sizes"]:
            return candidate
    return info["sizes"][0]


def check_aspect(provider_key: str, aspect: str) -> str:
    info = provider_info(provider_key)
    if aspect not in info["aspects"]:
        raise ValueError(
            f"aspect {aspect!r} not supported by {provider_key}; "
            f"supported: {list(info['aspects'])}"
        )
    return aspect


def estimate_cost(provider_key: str, size: str = "2K", n_refs: int = 0) -> float:
    """What one generate() call will cost — shown BEFORE the call, recorded after."""
    info = provider_info(provider_key)
    size = coerce_size(provider_key, size)
    cost = float(info.get("usd_by_size", {}).get(size, info["usd_per_image"]))
    extra = info.get("usd_per_extra_ref")
    if extra and n_refs > 1:
        cost += extra * (n_refs - 1)
    return round(cost, 4)


def describe_providers(only_available: bool = True) -> list[dict[str, Any]]:
    """Serializable provider table for the API (never includes key values)."""
    out = []
    for key, info in PROVIDERS.items():
        avail = is_available(key)
        if only_available and not avail:
            continue
        out.append({
            "key": key,
            "label": info["label"],
            "model": info["model"],
            "api": info["api"],
            "available": avail,
            "usd_per_image": info["usd_per_image"],
            "usd_by_size": info.get("usd_by_size", {}),
            "rpm": info["rpm"],
            "sizes": list(info["sizes"]),
            "aspects": list(info["aspects"]),
            "max_refs": info["max_refs"],
            "supports_edit": info["supports_edit"],
            "required_env_any": list(info["keys_any"]),
        })
    return out
