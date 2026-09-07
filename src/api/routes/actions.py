"""GET /v1/actions[?finding=&organ=] · /v1/actions/finding-kinds · /v1/actions/{key} · POST /v1/actions · POST /v1/actions/{key}/outcome
· POST /v1/actions/suggest: what an organ can do in response to a finding, held in the Mastermind (Evgeny, 2026-09-07). An organ
registers its actions (owner = the organ; only the owner overwrites); a renderer or a page asks what a finding row licenses and
gets the actions with their inputs filled; the organ that ran one posts the outcome. Persisted like the practices (GitHub when
enabled, the executor database always)."""
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.actions.register import record_event
from src.actions.registry import Action, ActionOutcome, get_action_registry, suggest

router = APIRouter(prefix="/actions", tags=["actions"])


def _row(a: Action) -> dict:
    return {**a.model_dump(exclude={"evidence"}), "totals": a.totals()}


@router.get("")
def list_actions(finding: Optional[str] = None, organ: Optional[str] = None):
    reg = get_action_registry()
    rows = reg.for_finding(finding) if finding else reg.list()
    if organ:
        rows = [a for a in rows if a.organ == organ]
    return [_row(a) for a in rows]


@router.get("/finding-kinds")
def finding_kinds():
    return get_action_registry().finding_kinds()


class SuggestIn(BaseModel):
    finding: str = Field(..., description="the finding kind, e.g. citation_shift.unexamined")
    fields: dict[str, Any] = Field(default_factory=dict, description="the row's fields (thinker_name, work_title, uid, referee_thinker_id …)")


@router.post("/suggest")
def suggest_actions(body: SuggestIn):
    return suggest(body.finding, body.fields)


@router.get("/{key}")
def get_action(key: str):
    a = get_action_registry().get(key)
    if a is None:
        raise HTTPException(status_code=404, detail=f"no action {key}")
    return {**a.model_dump(), "totals": a.totals()}


class ActionIn(BaseModel):
    key: str
    organ: str
    name: str
    when: list[str] = Field(..., min_length=1)
    inputs: list[str] = Field(default_factory=list)
    route: str = ""
    cost: str = "none"
    cost_note: str = ""
    side_effects: str = ""
    gated_by: str = ""
    yields: str = ""
    owner: str = "the-mastermind"
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
async def create_action(body: ActionIn):
    reg = get_action_registry()
    existed = reg.get(body.key) is not None
    try:
        a = reg.upsert(Action(**body.model_dump()))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    persisted = await _persist(reg, a.key, f"Action {a.key}: {'updated' if existed else 'registered'} by {a.owner} [skip render]")
    return {**a.model_dump(), "totals": a.totals(), "created": not existed, "persisted": persisted, "durable": reg.last_durable}


class OutcomeIn(BaseModel):
    run: str
    organ: str = ""
    finding: str = ""
    source: str = ""
    status: str = "done"
    cost_usd: Optional[float] = None
    result: str = ""
    batch: Optional[str] = None       # the macro action's id when the outcome came from an approved batch (2026-09-07)
    intent: Optional[str] = None


@router.post("/{key}/outcome")
async def post_outcome(key: str, body: OutcomeIn):
    reg = get_action_registry()
    try:
        a = reg.add_outcome(key, ActionOutcome(**body.model_dump()))
    except KeyError:
        raise HTTPException(status_code=404, detail=f"no action {key}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    record_event("outcome", action=key, organ=body.organ or a.organ, status=body.status, run=body.run, finding=body.finding, source=body.source, batch=body.batch,
                 intent=body.intent or (a.intents[0] if a.intents else None), cost_usd=body.cost_usd, summary=(body.result or "")[:200])   # the register (2026-09-07 18:30)
    persisted = await _persist(reg, key, f"Action {key}: outcome from {body.organ or 'a run'} {body.run} [skip render]")
    return {"key": key, "totals": a.totals(), "evidence": [e.model_dump() for e in a.evidence], "persisted": persisted, "durable": reg.last_durable}


class MacroIn(BaseModel):
    actions: list[dict[str, Any]] = Field(..., description="the page's suggested actions (the entries of GET /v1/dossier/jobs/{id}/oeuvre → actions)")
    context: dict[str, Any] = Field(default_factory=dict, description="the page's context: author, focal text, run")
    trajectory: Optional[str] = Field(default=None, description="the trajectory block; the stored narrative is used when absent")
    depth: str = "surface"
    model: Optional[str] = None
    spend_cap_usd: float = Field(2.0, ge=0.0, le=20.0)


@router.post("/macro")
def macro_actions(body: MacroIn):
    """A page's micro actions read against the trajectory and the intents → three to five macro actions the owner approves once
    (Evgeny, 2026-09-07 18:30). The engine macro_actions runs as a light call; the parser turns its rows into macros with what each enables."""
    from src.actions.macro import parse_macros, render_actions_document
    from src.actions.registry import allowed_intents
    from src.api.routes.trajectory import load_trajectory, trajectory_block
    from src.dossier.engine_call import call_engine
    from src.sources.schemas import SourceSpec
    from src.vocabularies.registry import get_vocabulary_registry

    if not body.actions:
        raise HTTPException(status_code=400, detail="no actions supplied")
    doc = render_actions_document(body.actions, body.context)
    intents = get_vocabulary_registry().get("intents")
    packet = {"role": "plan", "kind": "macro_actions", "intents": [{"value": v.value, "gloss": v.gloss} for v in (intents.values if intents else [])],
              "trajectory": body.trajectory or trajectory_block(load_trajectory()), "context": body.context}
    try:
        out = call_engine("macro_actions", [SourceSpec(kind="paste", role="source", key="actions", title="The page's suggested actions", text=doc)],
                          packet=packet, depth=body.depth, model=body.model, spend_cap_usd=body.spend_cap_usd)
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    parsed = parse_macros(out.get("rows") or [], allowed_intents())
    return {**parsed, "prose": out.get("prose") or "", "rows": len(out.get("rows") or []), "wall": out.get("wall"), "cost_usd": out.get("cost_usd"), "model": out.get("model")}
