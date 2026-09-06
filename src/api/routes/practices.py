"""GET /v1/practices[?task=] · /v1/practices/task-kinds · /v1/practices/{key} · POST /v1/practices/{key}/evidence: how to
search, held in the Mastermind beside the engines (Evgeny, 2026-09-07). A planner asks for its task kind and carries the
records in its packet as a PRACTICES block; a retrospective seat posts the yield of each practice a run deployed, so a
practice carries its own evidence across organs. On Render the write-back is committed through GitHub like a
definition edit (GITHUB_TOKEN + GITHUB_REPO); without them it lives until the next deploy."""
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


class EvidenceIn(BaseModel):
    run: str = Field(..., description="the run id in the organ that scored it")
    organ: str = ""
    queries: int = Field(0, ge=0)
    new_relevant: int = Field(0, ge=0)
    note: str = ""


@router.post("/{key}/evidence")
async def post_evidence(key: str, body: EvidenceIn):
    """A run's yield for the practice it deployed: queries that used it and the relevant pages only they found."""
    from src.persistence.github_client import CommitFile, GitHubPersistence, get_github_persistence

    reg = get_practice_registry()
    try:
        p = reg.add_evidence(key, PracticeEvidence(**body.model_dump()))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"no practice {key}")
    persisted = None
    github = get_github_persistence()
    if github.enabled:
        path = reg.file_for(key)
        res = await github.commit_files([CommitFile(repo_path=GitHubPersistence.absolute_to_repo_path(path), content=path.read_text())],
                                        f"Practice {key}: yield from {body.organ or 'a run'} {body.run}")
        persisted = {"success": res.success, "sha": res.sha, "message": res.message}
    return {"key": key, "totals": p.yield_totals(), "evidence": [e.model_dump() for e in p.evidence], "persisted": persisted}
