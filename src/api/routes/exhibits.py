"""GET /v1/exhibits[?kind=&medium=] · /v1/exhibits/kinds · /v1/exhibits/{key} · POST /v1/exhibits · POST /v1/exhibits/{key}/use: the
presentation elements a page can show, as records a page planner chooses among (Evgeny, 2026-09-07); a reviewer's verdicts on
a page's elements write back. Persisted like the practices and the actions."""
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.exhibits.registry import Exhibit, ExhibitUse, get_exhibit_registry, planner_block

router = APIRouter(prefix="/exhibits", tags=["exhibits"])


@router.get("")
def list_exhibits(kind: Optional[str] = None, medium: Optional[str] = None):
    reg = get_exhibit_registry()
    rows = reg.for_kind(kind) if kind else reg.list()
    if medium:
        rows = [e for e in rows if e.medium == medium]
    return planner_block(rows)


@router.get("/kinds")
def kinds():
    return get_exhibit_registry().kinds()


@router.get("/{key}")
def get_exhibit(key: str):
    e = get_exhibit_registry().get(key)
    if e is None:
        raise HTTPException(status_code=404, detail=f"no exhibit {key}")
    return e.model_dump()


class ExhibitIn(BaseModel):
    key: str
    name: str
    when: list[str] = Field(..., min_length=1)
    inputs: list[str] = Field(default_factory=list)
    medium: str = "html"
    renderer: str = ""
    shape: str
    didactic: str
    cost: str = "none"
    owner: str = "the-mastermind"
    example: str = ""
    note: str = ""


async def _persist(reg, key: str, message: str):
    from src.persistence.github_client import CommitFile, GitHubPersistence, get_github_persistence

    github = get_github_persistence()
    if not github.enabled:
        return None
    path = reg.file_for(key)
    res = await github.commit_files([CommitFile(repo_path=GitHubPersistence.absolute_to_repo_path(path), content=path.read_text())], message)
    return {"success": res.success, "sha": res.sha, "message": res.message}


@router.post("", status_code=201)
async def create_exhibit(body: ExhibitIn):
    reg = get_exhibit_registry()
    existed = reg.get(body.key) is not None
    try:
        e = reg.upsert(Exhibit(**body.model_dump()))
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    except PermissionError as ex:
        raise HTTPException(status_code=403, detail=str(ex))
    persisted = await _persist(reg, e.key, f"Exhibit {e.key}: {'updated' if existed else 'registered'} by {e.owner} [skip render]")
    return {**e.model_dump(), "created": not existed, "persisted": persisted, "durable": reg.last_durable}


class UseIn(BaseModel):
    page: str
    organ: str = ""
    verdict: str = ""
    note: str = ""


@router.post("/{key}/use")
async def post_use(key: str, body: UseIn):
    from src.vocabularies.registry import values

    reg = get_exhibit_registry()
    if body.verdict and body.verdict not in values("page_review_verdicts"):
        raise HTTPException(status_code=400, detail=f"verdict must be one of {values('page_review_verdicts')}")
    try:
        e = reg.add_use(key, ExhibitUse(**body.model_dump()))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"no exhibit {key}")
    persisted = await _persist(reg, key, f"Exhibit {key}: used on {body.page} [skip render]")
    return {"key": key, "uses": len(e.evidence), "persisted": persisted, "durable": reg.last_durable}
