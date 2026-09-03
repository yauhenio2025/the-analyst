"""Prompt-builder + adapter-policy tests for src/images (no network)."""
from __future__ import annotations

import pytest

from src.images import adapter as A
from src.images import providers as P
from src.images.figure_prompts import (
    FIGURE_PROHIBITIONS,
    NO_TEXT_CLOSER,
    REGISTERS,
    build_figure_prompt,
    build_style_override,
    declutter_scene,
    ensure_no_text,
)

SCENE = "A five-level lattice: group philosophy, house codes, collection, product, discourse."


def test_registers_present_with_openers():
    assert set(REGISTERS) == {"editorial", "diagrammatic", "photographic", "archival"}
    for reg in REGISTERS.values():
        assert reg["opener"].endswith("humans.") or reg["opener"].endswith("poses.")


@pytest.mark.parametrize("register", sorted(REGISTERS))
def test_prompt_opens_with_register_and_closes_no_text(register):
    p = build_figure_prompt(SCENE, register=register)
    assert p.startswith(REGISTERS[register]["opener"])
    assert SCENE in p
    assert p.rstrip().endswith(NO_TEXT_CLOSER)
    assert "No on-screen text, no captions, no subtitles, no signs, no lettering." in p
    assert "MAX 8 distinct visual elements" in p
    for prohibition in FIGURE_PROHIBITIONS[:3]:
        assert prohibition in p


def test_prompt_allow_text_switches_to_legibility_rules():
    p = build_figure_prompt(SCENE, no_text=False)
    assert NO_TEXT_CLOSER not in p
    assert "Minimum 14pt-equivalent" in p


def test_prompt_palette_caption_aspect_extras():
    p = build_figure_prompt(SCENE, palette="bone white, faded indigo", caption="The lattice",
                            aspect="16:9", extra_prohibitions=["mannequins", " "])
    assert "PALETTE (mandatory): bone white, faded indigo" in p
    assert "“The lattice”" in p and "NOT\ninside the image" not in p
    assert "compose for a 16:9 aspect ratio" in p
    assert "  ✗ mannequins" in p
    assert p.count("  ✗  ") == 0


def test_prompt_style_override_sandwich():
    style = {"background": "#FFFFFF", "primary_color": "#1B3A5C", "no_dark_backgrounds": True,
             "forbidden": ["3D effects"]}
    p = build_figure_prompt(SCENE, style=style)
    assert p.startswith("═")
    assert "MANDATORY STYLE OVERRIDE" in p
    assert "BACKGROUND (mandatory): #FFFFFF" in p
    assert "  • 3D effects" in p
    assert "FINAL STYLE OVERRIDE (REPEATED" in p
    assert p.index("MANDATORY STYLE OVERRIDE") < p.index(REGISTERS["editorial"]["opener"]) < p.index("FINAL STYLE OVERRIDE")
    assert build_style_override(None) == "" and build_style_override({}) == ""


def test_prompt_rejects_bad_input():
    with pytest.raises(ValueError):
        build_figure_prompt("   ")
    with pytest.raises(ValueError):
        build_figure_prompt(SCENE, register="oil_painting")


def test_ensure_no_text_idempotent():
    once = ensure_no_text("draw a lattice")
    assert once.rstrip().endswith(NO_TEXT_CLOSER)
    assert ensure_no_text(once) == once
    assert once.count("No on-screen text") == 1


def test_declutter_is_noop_without_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert declutter_scene(SCENE) == SCENE
    assert declutter_scene("  ") == ""


# --------------------------------------------------------------------------
# Provider registry / adapter policy (transport stubbed)
# --------------------------------------------------------------------------

def test_registry_contract():
    assert set(P.PROVIDERS) == {"gemini_pro", "gemini_flash", "seedream_5_pro", "qwen_image_2_pro"}
    assert P.PROVIDERS["gemini_pro"]["model"] == "gemini-3-pro-image-preview"
    assert P.PROVIDERS["gemini_flash"]["model"] == "gemini-3.1-flash-image-preview"
    assert P.PROVIDERS["seedream_5_pro"]["model"] == "doubao-seedream-5-0-pro-260628"
    assert P.PROVIDERS["qwen_image_2_pro"]["model"] == "qwen-image-2.0-pro"
    assert P.PROVIDERS["qwen_image_2_pro"]["rpm"] == 2
    assert set(P.PROVIDERS["gemini_pro"]["keys_any"]) == {"GEMINI_API_KEY", "GOOGLE_VEO_API_KEY"}
    for info in P.PROVIDERS.values():
        for size in info["sizes"]:
            assert size in ("1K", "2K", "4K")
        assert "16:9" in info["aspects"] and "1:1" in info["aspects"]


def test_size_coercion_and_cost():
    assert P.coerce_size("seedream_5_pro", "4K") == "2K"
    assert P.coerce_size("qwen_image_2_pro", "2K") == "1K"
    assert P.coerce_size("gemini_pro", "4K") == "4K"
    assert P.estimate_cost("gemini_pro", "4K") == 0.24
    assert P.estimate_cost("gemini_pro", "2K") == 0.134
    assert P.estimate_cost("seedream_5_pro", "2K", n_refs=3) == pytest.approx(0.066)
    with pytest.raises(ValueError):
        P.check_aspect("qwen_image_2_pro", "21:9")
    with pytest.raises(P.UnknownImageProvider):
        P.provider_info("dalle")


def test_available_providers_key_gated(monkeypatch):
    for k in ("GEMINI_API_KEY", "GOOGLE_VEO_API_KEY", "ARK_API_KEY", "DASHSCOPE_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    assert P.available_providers() == []
    monkeypatch.setenv("GEMINI_API_KEY", "a")
    monkeypatch.setenv("DASHSCOPE_API_KEY", "b")
    assert P.available_providers() == ["gemini_pro", "gemini_flash", "qwen_image_2_pro"]
    monkeypatch.delenv("GEMINI_API_KEY")
    monkeypatch.setenv("GOOGLE_VEO_API_KEY", "c")
    assert "gemini_pro" in P.available_providers()


_PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32


def test_generate_image_retries_on_no_image_then_succeeds(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "t")
    monkeypatch.setattr(A, "TRANSIENT_BACKOFF_S", 0.0)
    calls = []

    def flaky(info, prompt, size, aspect, refs, timeout_s, api_key):
        calls.append(prompt)
        if len(calls) == 1:
            raise A.NoImageReturned("text instead of image", text="Here is a description...")
        return _PNG, "image/png", {"path": "fake"}

    monkeypatch.setitem(A._ADAPTERS, "gemini", flaky)
    r = A.generate_image("draw a lattice", provider="gemini_pro", size="2K", aspect="16:9")
    assert len(calls) == 2
    assert r.image_bytes == _PNG and r.mime_type == "image/png"
    assert r.provider == "gemini_pro" and r.model == "gemini-3-pro-image-preview"
    assert r.cost_usd == 0.134 and r.raw["attempts"] == 2
    assert r.prompt_sent.rstrip().endswith(NO_TEXT_CLOSER)


def test_generate_image_policy_not_retried(monkeypatch):
    monkeypatch.setenv("ARK_API_KEY", "t")
    n = {"calls": 0}

    def blocked(*a, **k):
        n["calls"] += 1
        raise A.PolicyRejection("OutputImageSensitiveContentDetected")

    monkeypatch.setitem(A._ADAPTERS, "ark", blocked)
    with pytest.raises(A.PolicyRejection):
        A.generate_image("x", provider="seedream_5_pro")
    assert n["calls"] == 1


def test_generate_image_throttle_sleeps_retry_after(monkeypatch):
    monkeypatch.setenv("DASHSCOPE_API_KEY", "t")
    slept = []
    monkeypatch.setattr(A.time, "sleep", lambda s: slept.append(s))
    n = {"calls": 0}

    def throttled(*a, **k):
        n["calls"] += 1
        if n["calls"] == 1:
            raise A.Throttled("Throttling.RateQuota", retry_after=65)
        return _PNG, "image/png", {}

    monkeypatch.setitem(A._ADAPTERS, "dashscope-mm", throttled)
    r = A.generate_image("x", provider="qwen_image_2_pro", size="2K")
    assert slept == [65] and r.raw["size_used"] == "1K" and r.raw["throttles"] == 1


def test_generate_image_unconfigured_and_bad_args(monkeypatch):
    monkeypatch.delenv("ARK_API_KEY", raising=False)
    with pytest.raises(A.ImageProviderError):
        A.generate_image("x", provider="seedream_5_pro")
    monkeypatch.setenv("ARK_API_KEY", "t")
    with pytest.raises(ValueError):
        A.generate_image("x", provider="seedream_5_pro", aspect="21:9")
    with pytest.raises(ValueError):
        A.generate_image("  ", provider="seedream_5_pro")


def test_generate_with_fallback_skips_and_falls_through(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_VEO_API_KEY", raising=False)
    monkeypatch.setenv("ARK_API_KEY", "t")
    monkeypatch.setenv("DASHSCOPE_API_KEY", "t")

    def fail(*a, **k):
        raise A.ImageProviderError("boom", transient=False)

    def ok(*a, **k):
        return _PNG, "image/png", {}

    monkeypatch.setitem(A._ADAPTERS, "ark", fail)
    monkeypatch.setitem(A._ADAPTERS, "dashscope-mm", ok)
    r = A.generate_with_fallback("x", providers=["gemini_pro", "seedream_5_pro", "qwen_image_2_pro"])
    assert r.provider == "qwen_image_2_pro"
    trace = r.raw["fallback_trace"]
    assert trace[0]["skipped"] == "not configured"
    assert trace[1]["type"] == "ImageProviderError"
    assert trace[2]["ok"] is True
    with pytest.raises(A.ImageProviderError):
        A.generate_with_fallback("x", providers=["gemini_pro", "seedream_5_pro"])


def test_edit_image_non_gemini_not_implemented(monkeypatch):
    monkeypatch.setenv("ARK_API_KEY", "t")
    with pytest.raises(NotImplementedError):
        A.edit_image(_PNG, "make it blue", provider="seedream_5_pro")


def test_style_dict_wraps_prompt_in_adapter(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "t")
    seen = {}

    def fake(info, prompt, *a, **k):
        seen["prompt"] = prompt
        return _PNG, "image/png", {}

    monkeypatch.setitem(A._ADAPTERS, "gemini", fake)
    A.generate_image("a lattice", provider="gemini_pro", style={"background": "white"}, no_text=False)
    assert seen["prompt"].startswith("═") and "FINAL STYLE OVERRIDE" in seen["prompt"]
    assert NO_TEXT_CLOSER not in seen["prompt"]
