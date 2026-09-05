"""Process-wide drain flag for a graceful shutdown.

Render replaces the instance on every push to master and sends SIGTERM to the old one, then SIGKILL after
`maxShutdownDelaySeconds` (render.yaml, 300 s). Dossier and executor jobs run as daemon threads inside the web
process, so an immediate exit on SIGTERM used to kill every thread mid-call and cost a whole step. Instead the
SIGTERM handler calls `request_drain()`; long loops check `is_draining()` between units of work and stop at their
next checkpoint; `runner.start` refuses new dossier threads; the handler waits with `wait_for_idle` until nothing
is running (or the grace period is nearly spent) before it exits. Jobs that paused keep their active status, so
the next instance's boot recovery (`runner.recover_orphaned_dossiers`, `job_manager.recover_orphaned_jobs`)
restarts them from their checkpoint.

This module imports nothing from the dossier or executor packages so both can import it without cycles.
"""
from __future__ import annotations

import logging
import threading
import time
from typing import Callable, Optional

logger = logging.getLogger(__name__)

_draining = threading.Event()


def request_drain() -> None:
    """Flip the process into draining mode: no new dossier threads; running loops pause at their next checkpoint."""
    _draining.set()


def is_draining() -> bool:
    return _draining.is_set()


def reset_drain() -> None:
    """Clear the flag — for tests; a real process never leaves draining mode, it exits."""
    _draining.clear()


def _dossier_running_count() -> int:
    from src.dossier.runner import running_count  # lazy: runner imports this module

    return running_count()


def wait_for_idle(timeout_s: float, *, running_count: Optional[Callable[[], int]] = None,
                  poll_s: float = 0.25, progress_every_s: float = 15.0) -> bool:
    """Block until `running_count()` is 0 or `timeout_s` has passed. Returns True when idle, False on timeout.

    Logs how many jobs are still finishing every `progress_every_s`. Defaults to the dossier runner's count.
    Intended to be called from the SIGTERM handler on the main thread; the job threads keep running meanwhile.
    """
    count = running_count or _dossier_running_count
    start = time.monotonic()
    deadline = start + max(0.0, float(timeout_s))
    next_log = start + progress_every_s
    while True:
        n = count()
        if n <= 0:
            return True
        now = time.monotonic()
        if now >= deadline:
            return False
        if now >= next_log:
            logger.warning(f"drain: {n} dossier job(s) still finishing, {deadline - now:.0f} s left before the instance exits")
            next_log = now + progress_every_s
        time.sleep(max(0.0, min(poll_s, deadline - now)))
