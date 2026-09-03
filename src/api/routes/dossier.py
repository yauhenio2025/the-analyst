"""Dossier routes — The Analyst meaning-making workflow (owner: dossier agent).

Contract: communications/IMPLEMENTATION_TRACKER.md §4.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/dossier", tags=["dossier"])


@router.get("/health")
def dossier_health():
    return {"ok": True, "component": "dossier", "status": "stub"}
