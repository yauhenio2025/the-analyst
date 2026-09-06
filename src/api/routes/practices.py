"""GET /v1/practices[?task=] · /v1/practices/task-kinds · /v1/practices/{key} · POST /v1/practices · POST /v1/practices/{key}/evidence: how to
search, held in the Mastermind beside the engines (Evgeny, 2026-09-07). A planner asks for its task kind and carries the
records in its packet as a PRACTICES block; a retrospective seat posts the yield of each practice a run deployed, so a
practice carries its own evidence across organs. On Render the write-back is committed through GitHub like a
definition edit (GITHUB_TOKEN + GITHUB_REPO), with [skip render] so a write does not redeploy the API (eight
records registered by gs_revamp at 01:20 would otherwise have been eight deploys); without them it lives until the next deploy."""
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.practices.registry import PracticeEvidence, get_practice_registry, packet_block

router = APIRouter(prefix="/practices", tags=["practices"])


@router.get("")
def list_practices(task: Optional[str] = None):
    """The practices, as the records a planner's packet carries; `task` narrows to a task kind (person-harvest,
    paper-discovery, pdf-fetch, work-identity, institution-harvest)."""
    reg = get_practice_registry()
    return packet_block(reg.for_task(task) if task else reg.list())


@router.get("/task-kinds")
def task_kinds():
    return get_practice_registry().task_kinds()


@router.get("/{key}")
def get_practice(key: str):
    p = get_practice_registry().get(key)
    if p is None:
        raise HTTPException(status_code=404, detail=f"no practice {key}")
    return {**p.model_dump(), "totals": p.yield_totals()}


class PracticeIn(BaseModel):
    """A practice an organ's planner already knows (the Referee's fetch ladder, gs_revamp's query anatomy), registered
    here so every organ can read it. `owner` names the organ; only the owner may overwrite its record."""
    key: str = Field(..., description="a slug: lower-case words and hyphens")
    name: str
    task_kinds: list[str] = Field(..., min_length=1)
    when: str
    shape: str
    ingredients: list[str] = Field(default_factory=list)
    yields: str
    misses: str = ""
    origin: str = ""
    owner: str = Field("the-mastermind", description="the-mastermind | the-reporter | the-referee | gs-revamp | the-stacks")
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
async def create_practice(body: PracticeIn):
    """Register or update a practice. Fields: key, name, task_kinds[], when, shape, ingredients[], yields, misses, origin, owner."""
    from src.practices.registry import Practice

    reg = get_practice_registry()
    existed = reg.get(body.key) is not None
    try:
        p = reg.upsert(Practice(**body.model_dump()))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    persisted = await _persist(reg, p.key, f"Practice {p.key}: {'updated' if existed else 'registered'} by {p.owner} [skip render]")
    return {**p.model_dump(), "totals": p.yield_totals(), "created": not existed, "persisted": persisted}


class EvidenceIn(BaseModel):
    run: str = Field(..., description="the run id in the organ that scored it")
    organ: str = ""
    queries: int = Field(0, ge=0)
    new_relevant: int = Field(0, ge=0)
    note: str = ""


@router.post("/{key}/evidence")
async def post_evidence(key: str, body: EvidenceIn):
    """A run's yield for the practice it deployed: queries that used it and the relevant pages only they found."""
    reg = get_practice_registry()
    try:
        p = reg.add_evidence(key, PracticeEvidence(**body.model_dump()))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"no practice {key}")
    persisted = await _persist(reg, key, f"Practice {key}: yield from {body.organ or 'a run'} {body.run} [skip render]")
    return {"key": key, "totals": p.yield_totals(), "evidence": [e.model_dump() for e in p.evidence], "persisted": persisted}
