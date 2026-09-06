"""GET /v1/vocabularies · /v1/vocabularies/{key} · /v1/vocabularies/for-engine/{engine_key}: the enumerated values the
engines answer in, with glosses and the fields that use them. Consumers read their columns from here."""
from fastapi import APIRouter, HTTPException

from src.vocabularies.registry import get_vocabulary_registry

router = APIRouter(prefix="/vocabularies", tags=["vocabularies"])


@router.get("")
def list_vocabularies():
    return [{"key": v.key, "name": v.name, "family": v.family, "owner": v.owner, "values": v.value_list(), "used_by": [u.model_dump() for u in v.used_by]}
            for v in get_vocabulary_registry().list()]


@router.get("/for-engine/{engine_key}")
def vocabularies_for_engine(engine_key: str):
    return [v.model_dump() for v in get_vocabulary_registry().for_engine(engine_key)]


@router.get("/{key}")
def get_vocabulary(key: str):
    v = get_vocabulary_registry().get(key)
    if v is None:
        raise HTTPException(status_code=404, detail=f"no vocabulary {key}")
    return v.model_dump()
