"""Run-event ledger API: JSON list, summary, and SSE stream.

    GET /v1/events/{job_id}?after=<seq>&limit=<n>   JSON list of RunEvent
    GET /v1/events/{job_id}/summary                 JobSummary
    GET /v1/events/{job_id}/stream?after=<seq>      text/event-stream

SSE contract:
- replays events with seq > after, then polls the store every 1s and pushes new ones
- each event: `event: run_event` / `id: <seq>` / `data: <RunEvent JSON>`
- `: heartbeat` comment every 15s while idle
- closes once a job_finished/job_failed event has been sent and no further
  events arrive for 5s (also closes on client disconnect, or after
  `idle_timeout` seconds without any event — default 3600)

Aliases (thin delegations) live in src/api/routes/executor.py:
    GET /v1/executor/jobs/{job_id}/events, /events/summary, /events/stream
"""

import asyncio
import json
import logging
import time
from typing import Any, AsyncIterator, Optional

from fastapi import APIRouter, Query, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import StreamingResponse

from src.events.schemas import JobSummary, RunEvent, TERMINAL_KINDS
from src.events.store import job_summary, list_events

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/events", tags=["events"])

POLL_INTERVAL_S = 1.0
HEARTBEAT_INTERVAL_S = 15.0
CLOSE_AFTER_TERMINAL_S = 5.0
DEFAULT_IDLE_TIMEOUT_S = 3600.0
STREAM_BATCH = 500


def _to_model(ev: dict[str, Any]) -> RunEvent:
    return RunEvent(**{k: v for k, v in ev.items() if k in RunEvent.model_fields})


def _sse_frame(ev: dict[str, Any]) -> str:
    data = _to_model(ev).model_dump_json()
    return f"event: run_event\nid: {ev.get('seq', 0)}\ndata: {data}\n\n"


async def get_events(
    job_id: str,
    after: int = 0,
    limit: int = 1000,
) -> list[RunEvent]:
    events = await run_in_threadpool(list_events, job_id, after, limit)
    return [_to_model(ev) for ev in events]


async def get_summary(job_id: str) -> JobSummary:
    summary = await run_in_threadpool(job_summary, job_id)
    return JobSummary(**{k: v for k, v in summary.items() if k in JobSummary.model_fields})


async def event_stream(
    request: Request,
    job_id: str,
    after: int = 0,
    idle_timeout: float = DEFAULT_IDLE_TIMEOUT_S,
) -> AsyncIterator[str]:
    last_seq = int(after or 0)
    last_event_at = time.monotonic()
    last_heartbeat_at = time.monotonic()
    terminal_seen = False

    yield f": stream job={job_id} after={last_seq}\n\n"

    while True:
        try:
            if await request.is_disconnected():
                logger.debug("events stream %s: client disconnected", job_id)
                return
        except Exception:  # noqa: BLE001
            pass

        try:
            batch = await run_in_threadpool(list_events, job_id, last_seq, STREAM_BATCH)
        except Exception as e:  # noqa: BLE001
            logger.warning("events stream %s: list failed: %s", job_id, e)
            batch = []

        if batch:
            for ev in batch:
                yield _sse_frame(ev)
                last_seq = max(last_seq, int(ev.get("seq") or 0))
                if ev.get("kind") in TERMINAL_KINDS:
                    terminal_seen = True
            now = time.monotonic()
            last_event_at = now
            last_heartbeat_at = now
            if len(batch) >= STREAM_BATCH:
                continue  # drain backlog before sleeping
        else:
            now = time.monotonic()
            if terminal_seen and now - last_event_at >= CLOSE_AFTER_TERMINAL_S:
                yield f": closed job={job_id} last_seq={last_seq}\n\n"
                return
            if now - last_event_at >= idle_timeout:
                yield f": idle-timeout job={job_id} last_seq={last_seq}\n\n"
                return
            if now - last_heartbeat_at >= HEARTBEAT_INTERVAL_S:
                yield ": heartbeat\n\n"
                last_heartbeat_at = now

        await asyncio.sleep(POLL_INTERVAL_S)


def stream_response(request: Request, job_id: str, after: int = 0,
                    idle_timeout: float = DEFAULT_IDLE_TIMEOUT_S) -> StreamingResponse:
    return StreamingResponse(
        event_stream(request, job_id, after=after, idle_timeout=idle_timeout),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/{job_id}", response_model=list[RunEvent])
async def list_job_events(
    job_id: str,
    after: int = Query(0, ge=0, description="Return events with seq > after"),
    limit: int = Query(1000, ge=1, le=10000),
) -> list[RunEvent]:
    return await get_events(job_id, after=after, limit=limit)


@router.get("/{job_id}/summary", response_model=JobSummary)
async def job_events_summary(job_id: str) -> JobSummary:
    return await get_summary(job_id)


@router.get("/{job_id}/stream")
async def stream_job_events(
    request: Request,
    job_id: str,
    after: int = Query(0, ge=0, description="Replay events with seq > after, then follow live"),
    idle_timeout: float = Query(DEFAULT_IDLE_TIMEOUT_S, ge=5.0, le=86400.0),
) -> StreamingResponse:
    return stream_response(request, job_id, after=after, idle_timeout=idle_timeout)
