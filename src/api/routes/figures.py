"""Figure serving routes — generated images (owner: images agent)."""
from fastapi import APIRouter

router = APIRouter(prefix="/v1/figures", tags=["figures"])


@router.get("/health")
def figures_health():
    return {"ok": True, "component": "figures", "status": "stub"}
