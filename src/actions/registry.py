"""The actions registry: what an organ can DO in response to a finding, held in the Mastermind beside the engines, the
vocabularies and the practices (Evgeny, 2026-09-07: "break it down into actions tied to an analytical operation … if the paper
points to literature we never examined, commission harvesting of those thinkers in the Referee, fetch PDFs, look at whom they
cite"). An action is a record an organ registers: key · organ · name · when (the finding kinds that license it, e.g.
`citation_shift.unexamined`) · inputs (what a row must supply) · route and method · cost class · side effects · owner · evidence
(outcomes written back). A memo renderer turns a licensed row into a suggested action with its inputs filled; the owner clicks;
an organ runs it and posts the outcome. Nothing here runs anything.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field

DEFINITIONS = Path(__file__).parent / "definitions"
KEY = re.compile(r"^[a-z0-9]+(?:[-.][a-z0-9]+)*$")
BLOB_PREFIX = "action:"
COST_CLASSES = ("none", "cents", "dollars", "metered")
OUTCOME_STATUSES = ("handed", "done", "partial", "failed", "refused")   # the action_outcome_status vocabulary


class ActionOutcome(BaseModel):
    run: str                                   # the organ's id for the run (a job, a harvest, a fetch)
    organ: str = ""
    finding: str = ""                          # the finding kind that licensed it
    source: str = ""                           # the dossier job / row that suggested it
    status: str = "done"                       # handed | done | partial | failed | refused (action_outcome_status)
    cost_usd: Optional[float] = None
    result: str = ""                           # one line: what came of it
    recorded: str = ""


class Action(BaseModel):
    key: str                                   # organ.verb-object, e.g. referee.harvest-citations
    organ: str                                 # the-referee | the-stacks | the-reporter | the-mastermind | gs-revamp
    name: str
    when: list[str] = Field(default_factory=list)      # finding kinds: "<engine>.<dimension>" or "<engine>.*" or a plain kind
    inputs: list[str] = Field(default_factory=list)    # what the row must supply: thinker_name, work_title, uid, referee_thinker_id …
    route: str = ""                                    # METHOD path on the organ's API
    cost: str = "none"                                 # none | cents | dollars | metered
    cost_note: str = ""
    side_effects: str = ""
    gated_by: str = ""                                 # a pause, a budget, the owner's click
    yields: str = ""
    owner: str = "the-mastermind"
    version: str = ""
    evidence: list[ActionOutcome] = Field(default_factory=list)
    note: str = ""

    def licenses(self, finding_kind: str) -> bool:
        eng = finding_kind.split(".", 1)[0]
        return any(w == finding_kind or w == f"{eng}.*" or w == "*" for w in self.when)

    def totals(self) -> dict:
        return {"runs": len(self.evidence), "done": sum(1 for e in self.evidence if e.status == "done"),
                "cost_usd": round(sum(e.cost_usd or 0 for e in self.evidence), 4)}


def _durable_put(a: Action) -> bool:
    try:
        from src.dossier.blob_store import put_blob_safe
        return put_blob_safe(BLOB_PREFIX + a.key, "application/json", json.dumps(a.model_dump(), ensure_ascii=False).encode("utf-8"))
    except Exception:
        return False


def _durable_all() -> dict[str, Action]:
    try:
        from src.dossier.blob_store import get_blob, list_keys
        out = {}
        for row in list_keys(BLOB_PREFIX):
            key = (row.get("blob_key") or row.get("key") or "") if isinstance(row, dict) else (row[0] if row else "")
            got = get_blob(key)
            if got:
                a = Action.model_validate(json.loads(got[1].decode("utf-8")))
                out[a.key] = a
        return out
    except Exception:
        return {}


class ActionRegistry:
    def __init__(self, path: Path = DEFINITIONS, durable: bool = True):
        self.path = path
        self.durable = durable
        self.last_durable = False
        self._items: dict[str, Action] = {}
        for f in sorted(path.glob("*.json")):
            a = Action.model_validate(json.loads(f.read_text()))
            self._items[a.key] = a
        if durable:
            for key, a in _durable_all().items():
                old = self._items.get(key)
                if old is None or len(a.evidence) >= len(old.evidence):
                    self._items[key] = a

    def list(self) -> list[Action]:
        return list(self._items.values())

    def get(self, key: str) -> Optional[Action]:
        return self._items.get(key)

    def for_finding(self, finding_kind: str) -> list[Action]:
        return [a for a in self._items.values() if a.licenses(finding_kind)]

    def for_organ(self, organ: str) -> list[Action]:
        return [a for a in self._items.values() if a.organ == organ]

    def finding_kinds(self) -> list[str]:
        return sorted({w for a in self._items.values() for w in a.when})

    def upsert(self, action: Action) -> Action:
        if not KEY.match(action.key):
            raise ValueError(f"action key must be organ.verb-object in lower-case words, not {action.key!r}")
        if not action.organ or not action.name.strip() or not action.when:
            raise ValueError("an action needs organ, name and at least one finding kind in `when`")
        if action.cost not in COST_CLASSES:
            raise ValueError(f"cost must be one of {COST_CLASSES}")
        old = self._items.get(action.key)
        if old is not None and old.owner != action.owner:
            raise PermissionError(f"action {action.key} is {old.owner}'s; {action.owner} may not overwrite it")
        if old is not None and not action.evidence:
            action.evidence = old.evidence
        if not action.version:
            action.version = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self._items[action.key] = action
        self.file_for(action.key).write_text(json.dumps(action.model_dump(), ensure_ascii=False, indent=2) + "\n")
        self.last_durable = _durable_put(action) if self.durable else False
        return action

    def add_outcome(self, key: str, out: ActionOutcome) -> Action:
        a = self._items.get(key)
        if a is None:
            raise KeyError(f"no action {key}")
        if out.status not in OUTCOME_STATUSES:
            raise ValueError(f"status must be one of {OUTCOME_STATUSES}")
        if not out.recorded:
            out.recorded = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        a.evidence.append(out)
        self.file_for(key).write_text(json.dumps(a.model_dump(), ensure_ascii=False, indent=2) + "\n")
        self.last_durable = _durable_put(a) if self.durable else False
        return a

    def file_for(self, key: str) -> Path:
        return self.path / f"{key}.json"


def suggest(finding_kind: str, fields: dict[str, Any], registry: Optional["ActionRegistry"] = None) -> list[dict]:
    """The suggested actions for one finding row: every action the kind licenses, its inputs filled from the row's fields
    where the names match, the missing ones named. Shape only."""
    reg = registry or get_action_registry()
    out = []
    for a in reg.for_finding(finding_kind):
        filled = {k: fields[k] for k in a.inputs if k in fields and fields[k] not in (None, "")}
        out.append({"action": a.key, "organ": a.organ, "name": a.name, "route": a.route, "cost": a.cost, "gated_by": a.gated_by,
                    "inputs": filled, "missing": [k for k in a.inputs if k not in filled], "finding": finding_kind})
    return out


_registry: Optional[ActionRegistry] = None


def get_action_registry() -> ActionRegistry:
    global _registry
    if _registry is None:
        _registry = ActionRegistry()
    return _registry
