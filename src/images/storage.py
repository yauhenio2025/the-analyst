"""Figure storage — local disk (Render persistent disk or ./data/figures).

Layout under FIGURES_DIR (env, default ./data/figures):
    <figure_id>.png|jpg|webp     the image
    <figure_id>.json             sidecar: prompt, provider, model, cost, size,
                                 aspect, caption, dims, hashes, created_at, meta

figure_id = "{job_id}-{slug}-{8hex}" where 8hex is the first 8 hex chars of
sha256(image_bytes) — saving the same bytes twice under the same name is
idempotent (overwrites in place), a different render gets a different id.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_FIGURES_DIR = "./data/figures"

_MIME_EXT = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/webp": "webp",
}
_EXT_MIME = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}

_SAFE = re.compile(r"[^A-Za-z0-9_-]+")
_FIGURE_ID = re.compile(r"^[A-Za-z0-9_-]+$")

# Keys lifted from meta to the sidecar's top level (the figure contract).
_PROMOTED = ("prompt", "prompt_sent", "provider", "model", "cost_usd", "size", "aspect", "caption",
             "register", "scene", "compliance", "latency_ms")


def figures_dir() -> Path:
    """Resolve FIGURES_DIR at call time (so tests and deploys can point it)."""
    d = Path(os.environ.get("FIGURES_DIR") or DEFAULT_FIGURES_DIR).expanduser()
    d.mkdir(parents=True, exist_ok=True)
    return d


def slugify(text: str, max_len: int = 40) -> str:
    s = _SAFE.sub("-", (text or "").strip().lower()).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return (s[:max_len].rstrip("-")) or "figure"


def sniff_mime_strict(image_bytes: bytes) -> str | None:
    """Magic-byte sniff; None when the bytes are not a recognized image."""
    if image_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if image_bytes[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
        return "image/webp"
    return None


def sniff_mime(image_bytes: bytes) -> str:
    """Magic-byte sniff; falls back to image/png."""
    return sniff_mime_strict(image_bytes) or "image/png"


def image_dimensions(image_bytes: bytes) -> tuple[int | None, int | None]:
    try:
        from io import BytesIO

        from PIL import Image  # type: ignore

        with Image.open(BytesIO(image_bytes)) as im:
            return int(im.width), int(im.height)
    except Exception:
        return None, None


def _validate_id(figure_id: str) -> str:
    if not figure_id or not _FIGURE_ID.match(figure_id):
        raise ValueError(f"invalid figure_id {figure_id!r}")
    return figure_id


def _write_atomic(path: Path, data: bytes) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def save_figure(
    image_bytes: bytes,
    mime_type: str,
    *,
    job_id: str,
    name: str,
    meta: dict[str, Any] | None = None,
) -> str:
    """Persist an image + sidecar; return the figure_id."""
    if not image_bytes:
        raise ValueError("image_bytes is empty")
    # The bytes are the authority: a recognizable magic number wins over the
    # declared mime; the declared mime is used only for unrecognized bytes.
    declared = (mime_type or "").lower().strip()
    mime = sniff_mime_strict(image_bytes) or (declared if declared in _MIME_EXT else "image/png")
    ext = _MIME_EXT[mime]
    digest = hashlib.sha256(image_bytes).hexdigest()
    job_slug = slugify(job_id or "adhoc", 48)
    figure_id = f"{job_slug}-{slugify(name)}-{digest[:8]}"
    _validate_id(figure_id)

    meta = dict(meta or {})
    width, height = image_dimensions(image_bytes)
    sidecar: dict[str, Any] = {
        "figure_id": figure_id,
        "job_id": job_id,
        "name": name,
        "mime_type": mime,
        "ext": ext,
        "bytes": len(image_bytes),
        "sha256": digest,
        "width": width,
        "height": height,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    for key in _PROMOTED:
        if key in meta:
            sidecar[key] = meta[key]
    sidecar.setdefault("prompt", meta.get("prompt_sent"))
    sidecar["url"] = figure_url(figure_id)
    sidecar["meta"] = meta

    d = figures_dir()
    sidecar_bytes = json.dumps(sidecar, indent=2, default=str).encode("utf-8")
    _write_atomic(d / f"{figure_id}.{ext}", image_bytes)
    _write_atomic(d / f"{figure_id}.json", sidecar_bytes)
    # Durable copy: the disk is wiped on every deploy (2026-09-04).
    from src.dossier.blob_store import put_blob_safe

    put_blob_safe(f"figure:{figure_id}", mime, image_bytes)
    put_blob_safe(f"figure-meta:{figure_id}", "application/json", sidecar_bytes)
    return figure_id


def _restore_from_blob(figure_id: str) -> bool:
    """Bring a figure (and its sidecar) back to disk from the blob store."""
    try:
        from src.dossier.blob_store import get_blob
    except Exception:  # noqa: BLE001
        return False
    try:
        found = get_blob(f"figure:{figure_id}")
    except Exception:  # noqa: BLE001
        return False
    if not found:
        return False
    mime, data = found
    mime = sniff_mime_strict(data) or (mime if mime in _MIME_EXT else "image/png")
    ext = _MIME_EXT[mime]
    d = figures_dir()
    _write_atomic(d / f"{figure_id}.{ext}", data)
    try:
        meta = get_blob(f"figure-meta:{figure_id}")
    except Exception:  # noqa: BLE001
        meta = None
    if meta:
        _write_atomic(d / f"{figure_id}.json", meta[1])
    else:
        width, height = image_dimensions(data)
        sidecar = {"figure_id": figure_id, "mime_type": mime, "ext": ext, "bytes": len(data),
                   "sha256": hashlib.sha256(data).hexdigest(), "width": width, "height": height,
                   "url": figure_url(figure_id), "restored": True}
        _write_atomic(d / f"{figure_id}.json", json.dumps(sidecar, indent=2).encode("utf-8"))
    return True


def figure_url(figure_id: str) -> str:
    return f"/v1/figures/{figure_id}"


def figure_meta(figure_id: str) -> dict[str, Any]:
    _validate_id(figure_id)
    p = figures_dir() / f"{figure_id}.json"
    if not p.exists() and not _restore_from_blob(figure_id):
        raise FileNotFoundError(figure_id)
    if not p.exists():
        raise FileNotFoundError(figure_id)
    return json.loads(p.read_text("utf-8"))


def figure_path(figure_id: str) -> Path:
    """Path to the image file (raises FileNotFoundError when absent)."""
    _validate_id(figure_id)
    d = figures_dir()
    sidecar = d / f"{figure_id}.json"
    if sidecar.exists():
        ext = json.loads(sidecar.read_text("utf-8")).get("ext") or "png"
        p = d / f"{figure_id}.{ext}"
        if p.exists():
            return p
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = d / f"{figure_id}.{ext}"
        if p.exists():
            return p
    if _restore_from_blob(figure_id):
        for ext in ("png", "jpg", "jpeg", "webp"):
            p = d / f"{figure_id}.{ext}"
            if p.exists():
                return p
    raise FileNotFoundError(figure_id)


def figure_mime(figure_id: str) -> str:
    try:
        return figure_meta(figure_id).get("mime_type") or "image/png"
    except FileNotFoundError:
        return _EXT_MIME.get(figure_path(figure_id).suffix.lstrip("."), "image/png")


def list_figures(job_id: str) -> list[dict[str, Any]]:
    """Sidecars for a job, oldest first."""
    prefix = slugify(job_id or "adhoc", 48) + "-"
    out: list[dict[str, Any]] = []
    for p in figures_dir().glob(f"{prefix}*.json"):
        try:
            m = json.loads(p.read_text("utf-8"))
        except Exception:
            continue
        if m.get("job_id") == job_id or p.stem.startswith(prefix):
            out.append(m)
    out.sort(key=lambda m: (m.get("created_at") or "", m.get("figure_id") or ""))
    return out


def delete_figure(figure_id: str) -> bool:
    try:
        from src.dossier.blob_store import delete_blob

        delete_blob(f"figure:{figure_id}")
        delete_blob(f"figure-meta:{figure_id}")
    except Exception:  # noqa: BLE001
        pass
    _validate_id(figure_id)
    d = figures_dir()
    removed = False
    for p in d.glob(f"{figure_id}.*"):
        p.unlink(missing_ok=True)
        removed = True
    return removed
