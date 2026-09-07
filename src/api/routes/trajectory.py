"""GET /v1/register · GET /v1/trajectory[?block=1] · POST /v1/trajectory/narrate (Evgeny, 2026-09-07 18:30): the action register — what we
did — and the narrative of what we are doing, written by the trajectory_narrative engine over the register and kept as a record every
organ's planner can read (his postscript: the Reporter contextualises what it searches for by understanding why we need it)."""
from __future__ import annotations

import json
import time
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.actions.register import events, record_event, render_register

router = APIRouter(tags=["trajectory"])
BLOB = "trajectory:latest"


def _put(key: str, content_type: str, data: bytes) -> bool:
    from src.dossier.blob_store import put_blob_safe
    return put_blob_safe(key, content_type, data)


def _get(key: str) -> Optional[bytes]:
    from src.dossier.blob_store import get_blob
    got = get_blob(key)
    return got[1] if isinstance(got, tuple) else got


@router.get("/register")
def get_register(since: Optional[str] = None, kind: Optional[str] = None, limit: int = 200):
    """What we did, newest first."""
    rows = events(since=since, kind=kind, limit=min(max(limit, 1), 2000))
    return {"events": rows, "count": len(rows)}


def load_trajectory() -> Optional[dict]:
    raw = _get(BLOB)
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except ValueError:
        return None


def trajectory_block(t: Optional[dict], limit: int = 2000) -> str:
    """The compact block a planner's prompt carries: the narrative's prose, then the next directions, within `limit` chars."""
    if not t:
        return "TRAJECTORY: no narrative yet (the register has not been narrated)."
    prose = (t.get("prose") or "").strip()
    nexts = [r for r in t.get("rows") or [] if r.get("dim") == "next"]
    tail = ("\nNEXT: " + " · ".join((r.get("finding") or r.get("text") or "").strip() for r in nexts)) if nexts else ""
    block = f"TRAJECTORY (what we are doing, narrated {t.get('when', '')}):\n{prose}{tail}"
    return block if len(block) <= limit else block[:limit - 1].rstrip() + "…"


@router.get("/trajectory")
def get_trajectory(block: int = 0):
    t = load_trajectory()
    if block:
        return {"block": trajectory_block(t), "when": (t or {}).get("when")}
    if t is None:
        raise HTTPException(status_code=404, detail="no narrative yet; POST /v1/trajectory/narrate")
    return t


class NarrateIn(BaseModel):
    events: int = Field(400, ge=20, le=2000, description="how many of the latest register events the narrative reads")
    depth: str = "surface"
    model: Optional[str] = None
    spend_cap_usd: float = Field(2.0, ge=0.0, le=20.0)


@router.post("/trajectory/narrate")
def narrate(body: Optional[NarrateIn] = None):
    """Run trajectory_narrative over the register as a light call and keep the narrative as the record."""
    from src.dossier.engine_call import call_engine
    from src.sources.schemas import SourceSpec
    from src.vocabularies.registry import get_vocabulary_registry

    body = body or NarrateIn()
    rows = events(limit=body.events)
    if not rows:
        raise HTTPException(status_code=409, detail="the register is empty; nothing to narrate")
    doc = render_register(rows, limit=body.events)
    intents = get_vocabulary_registry().get("intents")
    packet: dict[str, Any] = {"role": "plan", "kind": "trajectory", "intents": [{"value": v.value, "gloss": v.gloss} for v in (intents.values if intents else [])],
                              "previous": (load_trajectory() or {}).get("prose", "")[:1500] or None}
    try:
        out = call_engine("trajectory_narrative", [SourceSpec(kind="paste", role="source", key="register", title="The action register", text=doc)],
                          packet=packet, depth=body.depth, model=body.model, spend_cap_usd=body.spend_cap_usd)
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    t = {"when": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "prose": out.get("prose") or "", "rows": out.get("rows") or [], "wall": out.get("wall"),
         "cost_usd": out.get("cost_usd"), "model": out.get("model"), "events_read": len(rows)}
    _put(BLOB, "application/json", json.dumps(t, ensure_ascii=False).encode("utf-8"))
    record_event("narrative", events_read=len(rows), cost_usd=out.get("cost_usd"), summary=(out.get("prose") or "")[:200])
    return {**t, "block": trajectory_block(t)}


@router.post("/register/backfill")
def backfill(refresh: bool = False):
    """Record job_done events for the finished jobs made before the register existed (idempotent); `refresh=true` re-records them with
    their substance from the readings ledger (engines, persons, rows, renders)."""
    from src.actions.register import backfill_jobs
    from src.dossier.store import list_jobs
    jobs = [j.model_dump() for j in list_jobs(limit=200)]
    return {"recorded": backfill_jobs(jobs, refresh=refresh), "jobs_seen": len(jobs)}
