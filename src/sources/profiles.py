"""The shared work profile.

The Stacks' `WorkProfile` (zotero-stacks `app/profiles.py`, the 4 Sep 2026 shape, 174 real instances) is the base;
the Analyst adds a verbatim `anchor` on every claim (the claim's own sentence in the text) with the wall's verdict, and
provenance. A `role: profile` source carries one or more of these as JSON; the reconnaissance desk starts from them
instead of re-reading the document, and every claim's anchor goes through the Analyst's own wall (verbatim in the held
text, or dropped) whatever the profile says about it. The desk emits the same shape (`to_shared`), so a profile made
here can travel back to the Stacks.

Vocabularies are the Stacks' (kept as documentation; the fields are plain strings so a profile whose model drifted from
the vocabulary is still read rather than dropped):
  person role: self · builds-on · criticizes · responds-to · subject · ally · comparison · evidence · cites
  work role: target · source · evidence · comparison · cited
  claim kind: thesis · finding · definition · prediction · polemic · method
  passage why: thesis · definition · key-example · verdict · turn
  contribution: theory · history · empirical · polemic · review · method · programme · reply · survey · interview
  verified: exact (verbatim after folding whitespace, hyphens and quotation marks) · partial (the words are there, the
  boundary is the model's) · no (not evidence)
"""
from __future__ import annotations

import json
import re
from typing import Any, Optional

from pydantic import BaseModel, Field

from src.sources.schemas import Document

CONTRIBUTIONS = ("theory", "history", "empirical", "polemic", "review", "method", "programme", "reply", "survey", "interview")


class PConcept(BaseModel):
    term: str
    variants: list[str] = Field(default_factory=list)
    weight: int = 3
    gloss: str = ""
    defined: bool = False
    locus: str = ""


class PPerson(BaseModel):
    name: str
    role: str = "cites"
    stance: str = ""
    locus: str = ""


class PWorkCited(BaseModel):
    title: str
    author: str = ""
    year: str = ""
    role: str = "cited"
    locus: str = ""


class PClaim(BaseModel):
    claim: str
    kind: str = "thesis"
    locus: str = ""
    against: list[str] = Field(default_factory=list)
    strength: str = "firm"
    anchor: str = Field(default="", description="the claim's own verbatim sentence in the text (the Analyst's addition)")
    anchor_verified: Optional[str] = Field(default=None, description="exact | partial | no, by code")


class PPosition(BaseModel):
    debate: str
    side: str = ""
    against: list[str] = Field(default_factory=list)


class PSection(BaseModel):
    heading: str
    pages: str = ""
    topic: str = ""
    concepts: list[str] = Field(default_factory=list)


class PPassage(BaseModel):
    quote: str
    locus: str = ""
    why: str = "thesis"
    verified: Optional[str] = None


class PRelation(BaseModel):
    subject: str
    relation: str
    object: str
    note: str = ""


class Verification(BaseModel):
    passages: int = 0
    exact: int = 0
    partial: int = 0
    no: int = 0
    version: str = ""


class SharedWorkProfile(BaseModel):
    uid: str = Field(default="", description="the Stacks uid (em:…) or the Analyst's document key")
    thesis: str
    question: str = ""
    contribution: str = "theory"
    tradition: str = ""
    object: str = ""
    period: str = ""
    cases: list[str] = Field(default_factory=list)
    language: str = "en"
    concepts: list[PConcept] = Field(default_factory=list)
    people: list[PPerson] = Field(default_factory=list)
    works_cited: list[PWorkCited] = Field(default_factory=list)
    claims: list[PClaim] = Field(default_factory=list)
    positions: list[PPosition] = Field(default_factory=list)
    sections: list[PSection] = Field(default_factory=list)
    passages: list[PPassage] = Field(default_factory=list)
    relations: list[PRelation] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    verification: Optional[Verification] = None
    origin: str = Field(default="stacks", description="stacks | analyst")
    model: str = ""
    created: str = ""
    title: str = ""


# ── reading profiles off a `role: profile` document ─────────────────────────────

def _one(obj: dict, uid: str = "") -> Optional[SharedWorkProfile]:
    if "profile" in obj and isinstance(obj["profile"], dict):      # the Stacks' stored form {uid, profile, model, cost, …}
        inner = dict(obj["profile"])
        for k in ("uid", "model", "created", "title"):
            if obj.get(k) and not inner.get(k):
                inner[k] = obj[k]
        obj = inner
    if not isinstance(obj.get("thesis"), str):
        return None
    if uid and not obj.get("uid"):
        obj = {**obj, "uid": uid}
    try:
        return SharedWorkProfile.model_validate(obj)
    except Exception:
        return None


def parse_profiles(text: str) -> list[SharedWorkProfile]:
    """One profile, a list of profiles, {"profiles": [...]}, or a {uid: profile} map; anything else is no profile."""
    try:
        obj = json.loads(text)
    except (ValueError, TypeError):
        return []
    out: list[SharedWorkProfile] = []
    if isinstance(obj, list):
        out = [p for p in (_one(x) for x in obj if isinstance(x, dict)) if p]
    elif isinstance(obj, dict):
        if isinstance(obj.get("profiles"), list):
            out = [p for p in (_one(x) for x in obj["profiles"] if isinstance(x, dict)) if p]
        elif "thesis" in obj or "profile" in obj:
            p = _one(obj)
            out = [p] if p else []
        else:
            out = [p for p in (_one(v, uid=k) for k, v in obj.items() if isinstance(v, dict)) if p]
    return out


def profile_documents(docs) -> list[SharedWorkProfile]:
    out = []
    for d in docs or []:
        if getattr(d, "role", "source") == "profile":
            out.extend(parse_profiles(d.text))
    return out


def _norm_title(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def match_profiles(profiles: list[SharedWorkProfile], docs: list[Document]) -> dict[str, SharedWorkProfile]:
    """doc key → profile. A profile matches a document by uid (the document's key or stacks key, with or without the
    `em:` prefix), else by title. First match wins; a profile never covers two documents."""
    by_uid: dict[str, SharedWorkProfile] = {}
    by_title: dict[str, SharedWorkProfile] = {}
    for p in profiles:
        for k in {p.uid, p.uid.split(":", 1)[-1]} - {""}:
            by_uid.setdefault(k, p)
        if p.title:
            by_title.setdefault(_norm_title(p.title), p)
    out: dict[str, SharedWorkProfile] = {}
    taken: set[int] = set()
    for d in docs:
        cands = [d.key, d.stacks_key, d.stacks_key.split(":", 1)[-1] if d.stacks_key else ""]
        p = next((by_uid[c] for c in cands if c and c in by_uid), None) or by_title.get(_norm_title(d.title))
        if p is not None and id(p) not in taken:
            out[d.key] = p
            taken.add(id(p))
    return out


# ── the two directions ──────────────────────────────────────────────────────────

def to_document_profile(profile: SharedWorkProfile, doc: Document):
    """The reconnaissance shape, anchors still unverified: the desk's wall decides. A claim without its own anchor
    borrows the passage at the same locus; a claim with no verbatim words at all cannot be a key claim."""
    from src.dossier.schemas import Anchor, DocumentProfile, KeyClaim

    by_locus = {p.locus: p for p in profile.passages if p.locus}
    claims: list[KeyClaim] = []
    for c in profile.claims:
        quote = c.anchor.strip() or (by_locus[c.locus].quote if c.locus and c.locus in by_locus else "")
        if quote:
            claims.append(KeyClaim(claim=c.claim, anchor=Anchor(doc_key=doc.key, quote=quote[:200])))
    if not claims:
        for p in profile.passages:
            if p.why in ("thesis", "verdict", "turn") and p.quote.strip():
                claims.append(KeyClaim(claim=p.quote.strip()[:300], anchor=Anchor(doc_key=doc.key, quote=p.quote.strip()[:200])))
    entities: list[str] = []
    for name in [p.name for p in profile.people] + [c.term for c in profile.concepts]:
        if name and name not in entities:
            entities.append(name)
    tensions = [f"{p.debate}: {p.side}" + (f" (against {', '.join(p.against)})" if p.against else "") for p in profile.positions if p.debate]
    one_line = profile.question or re.split(r"(?<=[.!?])\s", profile.thesis.strip(), maxsplit=1)[0]
    method = "; ".join(x for x in (profile.contribution, profile.tradition, profile.object) if x)
    return DocumentProfile(doc_key=doc.key, title=doc.title or profile.title, genre=profile.contribution, one_line=one_line,
                           thesis=profile.thesis, method=method, key_claims=claims[:8], entities=entities[:30], tensions=tensions[:8])


def to_shared(dp, doc: Any = None) -> SharedWorkProfile:
    """The reconnaissance desk's profile in the shared shape: every key claim becomes a claim with its verified anchor
    and a passage; entities become keywords; tensions become relations of the work with itself."""
    meta = doc if isinstance(doc, dict) else (doc.meta() if doc is not None and hasattr(doc, "meta") else {})
    uid = (meta.get("stacks_key") or meta.get("key") or getattr(dp, "doc_key", "")) if meta else getattr(dp, "doc_key", "")
    claims, passages = [], []
    for c in dp.key_claims:
        v = "exact" if c.anchor.verified and not c.anchor.trimmed else ("partial" if c.anchor.verified else "no")
        claims.append(PClaim(claim=c.claim, anchor=c.anchor.quote, anchor_verified=v))
        passages.append(PPassage(quote=c.anchor.quote, why="thesis", verified=v))
    counts = Verification(passages=len(passages), exact=sum(1 for p in passages if p.verified == "exact"),
                          partial=sum(1 for p in passages if p.verified == "partial"),
                          no=sum(1 for p in passages if p.verified == "no"), version="analyst-2026-09-06")
    genre = (dp.genre or "").lower()
    contribution = next((c for c in CONTRIBUTIONS if c in genre), "theory")
    return SharedWorkProfile(uid=uid, title=dp.title or meta.get("title", ""), thesis=dp.thesis, question=dp.one_line,
                             contribution=contribution, tradition="", object=dp.method, claims=claims, passages=passages,
                             keywords=list(dp.entities), relations=[PRelation(subject=uid, relation="tension", object=t) for t in dp.tensions],
                             verification=counts, origin="analyst")
