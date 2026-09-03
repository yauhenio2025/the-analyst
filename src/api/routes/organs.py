"""API routes for organ definitions — the services of the estate and their contributions."""

from fastapi import APIRouter, HTTPException

from src.organs.registry import get_organ_registry
from src.organs.schemas import OrganDefinition, OrganSummary

router = APIRouter(prefix="/organs", tags=["organs"])


@router.get("", response_model=list[OrganSummary])
async def list_organs():
    """All organs, ordered by layer (sources → search → reasoning → composition → creative → consumers → governance)."""
    return get_organ_registry().list_summaries()


@router.get("/by-layer")
async def organs_by_layer() -> dict[str, list[OrganSummary]]:
    """Organs grouped by layer, for the estate map."""
    return get_organ_registry().by_layer()


@router.get("/{organ_key}", response_model=OrganDefinition)
async def get_organ(organ_key: str):
    registry = get_organ_registry()
    organ = registry.get(organ_key)
    if organ is None:
        raise HTTPException(status_code=404, detail=f"Organ '{organ_key}' not found. Available: {registry.list_keys()}")
    return organ


@router.get("/{organ_key}/engines")
async def organ_engines(organ_key: str):
    """Engines whose home organ is this one (summaries)."""
    from src.engines.registry import get_engine_registry

    registry = get_organ_registry()
    if registry.get(organ_key) is None:
        raise HTTPException(status_code=404, detail=f"Organ '{organ_key}' not found")
    return [s for s in get_engine_registry().list_summaries() if s.home_organ == organ_key]
