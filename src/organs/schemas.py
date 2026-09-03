"""Organ definitions — the services of the estate.

An organ is a deployed (or planned) service. The Master maps organs by layer,
records what methods each one contributes to the registry, and points at where
each one runs. Organs are read-mostly definitions, JSON-per-file like every
other entity here.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class OrganLayer(str, Enum):
    SOURCES = "sources"          # where material comes from
    SEARCH = "search"            # discovery loops over the world
    REASONING = "reasoning"      # analytical engines, paradigms, workflows
    COMPOSITION = "composition"  # dossiers, figures, plates, presentation grammar
    CREATIVE = "creative"        # storytelling, editing, restructuring, film
    CONSUMERS = "consumers"      # thin hosts that display results
    GOVERNANCE = "governance"    # the registry itself, ontology, feedback


class OrganStatus(str, Enum):
    LIVE = "live"
    PARTIAL = "partial"
    FROZEN = "frozen"
    LOCAL = "local"
    PLANNED = "planned"
    SUSPENDED = "suspended"


class OrganDefinition(BaseModel):
    organ_key: str = Field(..., description="Stable key, e.g. 'wirecut'")
    organ_name: str = Field(..., description="Display name, e.g. 'Wirecut'")
    tagline: str = Field(..., description="One line: what it turns into what")
    layer: OrganLayer
    role: str = Field(..., description="A paragraph: what it does in the estate")
    contributes: list[str] = Field(
        default_factory=list,
        description="What this organ contributes to the Master's registry (methods, grammars, doctrines)",
    )
    families: list[str] = Field(
        default_factory=list, description="Engine families it hosts (see EngineFamily)"
    )
    counts: dict[str, int] = Field(
        default_factory=dict, description="Hand-curated snapshot counts (engines, passes, rules…)"
    )
    urls: dict[str, str] = Field(
        default_factory=dict,
        description="ui | api | health | console | repo | docs — whichever exist",
    )
    status: OrganStatus = OrganStatus.LIVE
    workspace: str = Field(default="caii", description="Render workspace or 'local'")
    sync: str = Field(
        default="mirrored",
        description="native: reads its methods from the registry at runtime | mirrored: registry mirrors its doctrines | planned",
    )
    depends_on: list[str] = Field(default_factory=list, description="Organ keys it calls")
    feeds: list[str] = Field(default_factory=list, description="Organ keys it delivers to")
    lineage: list[str] = Field(
        default_factory=list, description="Dictations and memos that define it"
    )
    notes: Optional[str] = None
    order: int = Field(default=50, description="Sort order within a layer")


class OrganSummary(BaseModel):
    organ_key: str
    organ_name: str
    tagline: str
    layer: OrganLayer
    families: list[str] = []
    counts: dict[str, int] = {}
    urls: dict[str, str] = {}
    status: OrganStatus = OrganStatus.LIVE
    sync: str = "mirrored"
    order: int = 50
