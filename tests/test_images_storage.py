"""Storage + route tests for src/images (no network)."""
from __future__ import annotations

import json
import struct
import zlib

import pytest
from fastapi.testclient import TestClient

from src.images import storage


def _png(w: int = 4, h: int = 3, color=(200, 30, 30)) -> bytes:
    """Minimal valid RGB PNG without Pillow."""
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    raw = b"".join(b"\x00" + bytes(color) * w for _ in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


_JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 64 + b"\xff\xd9"


@pytest.fixture(autouse=True)
def figures_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("FIGURES_DIR", str(tmp_path / "figs"))
    return tmp_path / "figs"


def test_save_and_read_roundtrip(figures_dir):
    png = _png()
    fid = storage.save_figure(png, "image/png", job_id="job-1", name="Lattice Figure",
                              meta={"prompt": "p", "provider": "gemini_pro", "model": "m",
                                    "cost_usd": 0.134, "size": "2K", "aspect": "16:9",
                                    "caption": "cap", "extra": {"k": 1}})
    assert fid.startswith("job-1-lattice-figure-")
    assert len(fid.split("-")[-1]) == 8
    assert (figures_dir / f"{fid}.png").read_bytes() == png
    meta = storage.figure_meta(fid)
    assert meta["figure_id"] == fid
    assert meta["job_id"] == "job-1"
    assert meta["mime_type"] == "image/png"
    assert meta["provider"] == "gemini_pro" and meta["cost_usd"] == 0.134
    assert meta["caption"] == "cap" and meta["size"] == "2K" and meta["aspect"] == "16:9"
    assert meta["meta"]["extra"] == {"k": 1}
    assert meta["url"] == f"/v1/figures/{fid}"
    assert meta["width"] == 4 and meta["height"] == 3      # Pillow available in venv
    assert storage.figure_path(fid).suffix == ".png"
    assert storage.figure_mime(fid) == "image/png"


def test_id_is_content_addressed_and_idempotent():
    a = storage.save_figure(_png(), "image/png", job_id="j", name="fig", meta={})
    b = storage.save_figure(_png(), "image/png", job_id="j", name="fig", meta={})
    c = storage.save_figure(_png(color=(1, 2, 3)), "image/png", job_id="j", name="fig", meta={})
    assert a == b and a != c
    assert len(storage.list_figures("j")) == 2


def test_jpeg_extension_and_mime_sniff():
    fid = storage.save_figure(_JPEG, "", job_id="j2", name="photo", meta={})
    assert storage.figure_path(fid).suffix == ".jpg"
    assert storage.figure_meta(fid)["mime_type"] == "image/jpeg"
    # wrong declared mime is corrected by sniffing
    fid2 = storage.save_figure(_png(), "image/jpeg", job_id="j2", name="png", meta={})
    assert storage.figure_meta(fid2)["mime_type"] == "image/png"


def test_path_safety():
    fid = storage.save_figure(_png(), "image/png", job_id="../../etc", name="x/../y", meta={})
    assert "/" not in fid and ".." not in fid
    with pytest.raises(ValueError):
        storage.figure_path("../x")
    with pytest.raises(FileNotFoundError):
        storage.figure_path("job-nope-12345678")
    with pytest.raises(ValueError):
        storage.save_figure(b"", "image/png", job_id="j", name="n", meta={})


def test_list_figures_scoped_to_job():
    storage.save_figure(_png(), "image/png", job_id="alpha", name="a", meta={})
    storage.save_figure(_png(color=(9, 9, 9)), "image/png", job_id="alpha", name="b", meta={})
    storage.save_figure(_png(), "image/png", job_id="alphabet", name="c", meta={})
    names = sorted(m["name"] for m in storage.list_figures("alpha"))
    assert names == ["a", "b"]
    assert storage.list_figures("nothing") == []


def test_delete_figure():
    fid = storage.save_figure(_png(), "image/png", job_id="d", name="x", meta={})
    assert storage.delete_figure(fid) is True
    with pytest.raises(FileNotFoundError):
        storage.figure_meta(fid)


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@pytest.fixture
def client():
    from fastapi import FastAPI

    from src.api.routes import figures as figures_routes

    app = FastAPI()
    app.include_router(figures_routes.router)
    return TestClient(app)


def test_routes_serve_figure_and_meta(client):
    png = _png()
    fid = storage.save_figure(png, "image/png", job_id="job-9", name="fig", meta={"prompt": "p"})
    r = client.get(f"/v1/figures/{fid}")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("image/png")
    assert r.content == png
    m = client.get(f"/v1/figures/{fid}/meta")
    assert m.status_code == 200 and m.json()["figure_id"] == fid
    j = client.get("/v1/figures/by-job/job-9")
    assert j.status_code == 200 and j.json()["count"] == 1
    assert j.json()["figures"][0]["url"] == f"/v1/figures/{fid}"
    assert client.get("/v1/figures/job-9-missing-00000000").status_code == 404
    assert client.get("/v1/figures/job-9-missing-00000000/meta").status_code == 404


def test_routes_providers_key_gated(client, monkeypatch):
    for k in ("GEMINI_API_KEY", "GOOGLE_VEO_API_KEY", "ARK_API_KEY", "DASHSCOPE_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    r = client.get("/v1/figures/providers")
    assert r.status_code == 200
    assert r.json()["providers"] == []
    assert "editorial" in r.json()["registers"]
    monkeypatch.setenv("GOOGLE_VEO_API_KEY", "x")
    keys = [p["key"] for p in client.get("/v1/figures/providers").json()["providers"]]
    assert keys == ["gemini_pro", "gemini_flash"]
    full = client.get("/v1/figures/providers?all=true").json()["providers"]
    assert {p["key"] for p in full} == {"gemini_pro", "gemini_flash", "seedream_5_pro", "qwen_image_2_pro"}
    for p in full:
        assert "usd_per_image" in p and "rpm" in p and p["model"]
        assert not any(v and str(v).startswith("x") for v in p.values() if isinstance(v, str))


def test_routes_generate_rejects_bad_input(client, monkeypatch):
    for k in ("GEMINI_API_KEY", "GOOGLE_VEO_API_KEY", "ARK_API_KEY", "DASHSCOPE_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    assert client.post("/v1/figures/generate", json={"prompt": "x", "provider": "nope"}).status_code == 400
    assert client.post("/v1/figures/generate", json={"prompt": "x", "register": "nope"}).status_code == 400
    assert client.post("/v1/figures/generate", json={"prompt": "x"}).status_code == 503


def test_routes_generate_with_fake_adapter(client, monkeypatch):
    """End-to-end through the route with the provider transport stubbed."""
    from src.images import adapter as A

    monkeypatch.setenv("GEMINI_API_KEY", "test")
    calls = {}

    def fake(info, prompt, size, aspect, refs, timeout_s, api_key):
        calls.update(prompt=prompt, size=size, aspect=aspect, model=info["model"])
        return _png(), "image/png", {"path": "fake"}

    monkeypatch.setitem(A._ADAPTERS, "gemini", fake)
    r = client.post("/v1/figures/generate", json={
        "prompt": "a five-level lattice", "provider": "gemini_pro", "size": "2K",
        "aspect": "16:9", "job_id": "job-7", "name": "Lattice", "register": "editorial",
        "caption": "The lattice"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["figure_id"].startswith("job-7-lattice-")
    assert body["url"] == f"/v1/figures/{body['figure_id']}"
    assert body["provider"] == "gemini_pro" and body["model"] == "gemini-3-pro-image-preview"
    assert body["cost_usd"] == 0.134 and body["compliance"] is None
    assert "Hand-drawn editorial illustration" in calls["prompt"]
    assert "No on-screen text" in calls["prompt"]
    assert calls["size"] == "2K" and calls["aspect"] == "16:9"
    meta = client.get(f"/v1/figures/{body['figure_id']}/meta").json()
    assert meta["register"] == "editorial" and meta["caption"] == "The lattice"
    assert meta["prompt"].startswith("Hand-drawn editorial illustration")
    assert client.get(body["url"]).headers["content-type"].startswith("image/png")
