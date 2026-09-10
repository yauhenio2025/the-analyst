"""The research state: the one record of an inquiry's program that Stacks, the Reporter and the Analyst read and write.

Built by code from the `inquiry_program` engine's rows; revised by later stages (feedback rounds,
readings) as new versions. Nothing in it is evidence: explanations are hypotheses, lanes are
instructions, leads are unverified pointers.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Voice = Literal["participant", "official", "critic", "economist", "comparator", "record", "press", "thinker"]
VOICES = set(Voice.__args__)


class Stake(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    claim: str
    thinker: str = ""
    formulation: str = ""
    bears_on: list[str] = Field(default_factory=list)
    anchor: str = ""
    doc: str = ""
    anchor_verified: bool = False
    confidence: str = ""


class Explanation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    claim: str
    origin: str = ""
    supports_if: str = ""
    undercuts_if: str = ""
    voices: list[str] = Field(default_factory=list)
    venues: str = ""
    actors: str = ""
    discriminating: str = ""
    priority: Optional[int] = None
    confidence: str = ""
    row_id: str = ""
    status: str = "live"            # live | retained | revised | retired, revised by later rounds
    evidence_ids: list[str] = Field(default_factory=list)   # filled as readings bear on it


class Lane(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    purpose: str
    explanations: list[str] = Field(default_factory=list)
    voice: str = ""
    venues: str = ""
    actors: str = ""
    queries: list[str] = Field(default_factory=list)
    contrary: str = ""
    coverage: str = ""
    confidence: str = ""


class Reading(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    uid: str
    why: str
    explanations: list[str] = Field(default_factory=list)
    look_for: str = ""
    order: Optional[int] = None
    in_inventory: Optional[bool] = None
    confidence: str = ""


class Gap(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    text: str
    kind: str = ""
    lead: str = ""
    resolve_by: str = ""
    confidence: str = ""


class ResearchState(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: int = 1
    created_at: str = ""
    question: str
    hunch: str = ""
    leads: list[str] = Field(default_factory=list)
    good_answer: str = ""
    thinker: str = ""
    stakes: list[Stake] = Field(default_factory=list)
    explanations: list[Explanation] = Field(default_factory=list)
    lanes: list[Lane] = Field(default_factory=list)
    readings: list[Reading] = Field(default_factory=list)
    gaps: list[Gap] = Field(default_factory=list)
    prose: str = ""
    method_receipt: dict = Field(default_factory=dict)
    problems: list[str] = Field(default_factory=list)   # what the parser could not accept; never silently dropped

    def sha256(self) -> str:
        body = self.model_dump(mode="json", exclude={"created_at"})
        return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


_ID_LIST = re.compile(r"E\d+")
_PREFIX_DIM = {"P1": "stake", "P2": "explanation", "P3": "lane", "P4": "reading", "P5": "gap"}


def _ids(value: str) -> list[str]:
    return list(dict.fromkeys(_ID_LIST.findall(value or "")))


def _split(value: str) -> list[str]:
    return [p.strip() for p in re.split(r"[;|]", value or "") if p.strip()]


def _voices(value: str) -> tuple[list[str], list[str]]:
    found, unknown = [], []
    for token in re.split(r"[,;/|]| or | and ", (value or "").lower()):
        token = token.strip().strip(".")
        if not token:
            continue
        if token in VOICES:
            found.append(token)
        else:
            unknown.append(token)
    return list(dict.fromkeys(found)), unknown


def _int(value: str) -> Optional[int]:
    m = re.search(r"\d+", value or "")
    return int(m.group()) if m else None


def _dim(row: dict) -> str:
    dim = (row.get("dim") or "").strip().lower()
    if dim in _PREFIX_DIM.values():
        return dim
    return _PREFIX_DIM.get((row.get("id") or "")[:2], dim)


def research_state_from_program(result: dict, *, question: str, hunch: str = "", leads: list[str] | None = None,
                                good_answer: str = "", thinker: str = "", inventory_uids: set[str] | None = None) -> ResearchState:
    """Build the record from an `inquiry_program` engine result (as returned by `call_engine`).

    Rows that do not fit their declared shape are recorded under `problems`, not silently dropped
    or repaired: a missing discriminating observation or an unknown voice is a defect of the program
    the researcher should see.
    """
    state = ResearchState(question=question, hunch=hunch, leads=list(leads or []), good_answer=good_answer, thinker=thinker,
                          prose=result.get("prose") or "", method_receipt=result.get("method_receipt") or {},
                          created_at=datetime.now(timezone.utc).isoformat())
    seen_explanations: set[str] = set()
    for row in result.get("rows") or []:
        f = {k.lower(): (v or "").strip() for k, v in (row.get("fields") or {}).items()}
        rid = row.get("id") or ""
        text = (row.get("finding") or "").strip()
        dim = _dim(row)
        if dim == "stake":
            state.stakes.append(Stake(id=rid, claim=text, thinker=f.get("thinker", ""), formulation=f.get("formulation", ""),
                                      bears_on=_ids(f.get("bears_on", "")), anchor=row.get("anchor") or "", doc=row.get("doc") or "",
                                      anchor_verified=bool(row.get("anchor_verified")), confidence=row.get("confidence") or f.get("confidence", "")))
        elif dim == "explanation":
            eid = (re.search(r"E\d+", f.get("id", "")) or re.search(r"E\d+", rid) or [None])
            eid = eid.group() if hasattr(eid, "group") else None
            if not eid:
                state.problems.append(f"{rid}: explanation without an E<n> id")
                eid = f"E{len(state.explanations) + 1}"
            if eid in seen_explanations:
                state.problems.append(f"{rid}: duplicate explanation id {eid}")
            seen_explanations.add(eid)
            voices, unknown = _voices(f.get("voices", ""))
            if unknown:
                state.problems.append(f"{rid}: unknown voice(s) {unknown}")
            if not f.get("discriminating"):
                state.problems.append(f"{rid}: explanation {eid} has no discriminating observation")
            if not f.get("undercuts_if"):
                state.problems.append(f"{rid}: explanation {eid} says nothing that would undercut it")
            state.explanations.append(Explanation(id=eid, claim=text, origin=f.get("origin", ""), supports_if=f.get("supports_if", ""),
                                                  undercuts_if=f.get("undercuts_if", ""), voices=voices, venues=f.get("venues", ""),
                                                  actors=f.get("actors", ""), discriminating=f.get("discriminating", ""),
                                                  priority=_int(f.get("priority", "")), confidence=row.get("confidence") or f.get("confidence", ""), row_id=rid))
        elif dim == "lane":
            voice = f.get("voice", "").lower().strip()
            if voice and voice not in VOICES:
                state.problems.append(f"{rid}: lane voice {voice!r} is not a known voice")
            queries = _split(f.get("queries", ""))
            if not queries:
                state.problems.append(f"{rid}: lane without literal queries")
            state.lanes.append(Lane(id=rid, purpose=text, explanations=_ids(f.get("explanations", "")), voice=voice, venues=f.get("venues", ""),
                                    actors=f.get("actors", ""), queries=queries, contrary=f.get("contrary", ""), coverage=f.get("coverage", ""),
                                    confidence=row.get("confidence") or f.get("confidence", "")))
        elif dim == "reading":
            uid = f.get("uid", "")
            known = None if inventory_uids is None else uid in inventory_uids
            if known is False:
                state.problems.append(f"{rid}: reading names a uid not in the inventory: {uid}")
            state.readings.append(Reading(id=rid, uid=uid, why=text, explanations=_ids(f.get("explanations", "")), look_for=f.get("look_for", ""),
                                          order=_int(f.get("order", "")), in_inventory=known, confidence=row.get("confidence") or f.get("confidence", "")))
        elif dim == "gap":
            state.gaps.append(Gap(id=rid, text=text, kind=f.get("kind", ""), lead=f.get("lead", ""), resolve_by=f.get("resolve_by", ""),
                                  confidence=row.get("confidence") or f.get("confidence", "")))
        else:
            state.problems.append(f"{rid}: row with unknown dimension {dim!r}")
    # Cross-checks that make the program executable rather than plausible.
    eids = {e.id for e in state.explanations}
    for lane in state.lanes:
        for e in lane.explanations:
            if e not in eids:
                state.problems.append(f"{lane.id}: lane serves unknown explanation {e}")
    served = {e for lane in state.lanes for e in lane.explanations}
    for e in state.explanations:
        if e.id not in served:
            state.problems.append(f"explanation {e.id} has no lane")
    if hunch and not any(e.origin.lower().startswith("hunch") for e in state.explanations):
        state.problems.append("a hunch was supplied but no explanation is marked as originating from it")
    if len(state.explanations) < 2:
        state.problems.append("fewer than two competing explanations")
    state.readings.sort(key=lambda r: (r.order is None, r.order or 0))
    state.explanations.sort(key=lambda e: (e.priority is None, e.priority or 0))
    return state
