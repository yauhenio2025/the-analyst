"""Organ registry — loads organ definitions from JSON files (same pattern as consumers)."""

import json
import logging
from pathlib import Path
from typing import Optional

from .schemas import OrganDefinition, OrganLayer, OrganSummary

logger = logging.getLogger(__name__)


class OrganRegistry:
    def __init__(self, definitions_dir: Optional[Path] = None):
        if definitions_dir is None:
            definitions_dir = Path(__file__).parent / "definitions"
        self.definitions_dir = definitions_dir
        self._organs: dict[str, OrganDefinition] = {}
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return
        if not self.definitions_dir.exists():
            logger.warning(f"Organ definitions directory not found: {self.definitions_dir}")
            self._loaded = True
            return
        for json_file in sorted(self.definitions_dir.glob("*.json")):
            try:
                with open(json_file, "r") as f:
                    data = json.load(f)
                organ = OrganDefinition.model_validate(data)
                self._organs[organ.organ_key] = organ
            except Exception as e:  # noqa: BLE001
                logger.error(f"Failed to load organ from {json_file}: {e}")
        self._loaded = True
        logger.info(f"Loaded {len(self._organs)} organ definitions")

    def get(self, organ_key: str) -> Optional[OrganDefinition]:
        self.load()
        return self._organs.get(organ_key)

    def list_all(self) -> list[OrganDefinition]:
        self.load()
        return sorted(self._organs.values(), key=lambda o: (list(OrganLayer).index(o.layer), o.order, o.organ_key))

    def list_keys(self) -> list[str]:
        self.load()
        return sorted(self._organs.keys())

    def list_summaries(self) -> list[OrganSummary]:
        return [
            OrganSummary(
                organ_key=o.organ_key, organ_name=o.organ_name, tagline=o.tagline,
                layer=o.layer, families=o.families, counts=o.counts, urls=o.urls,
                status=o.status, sync=o.sync, order=o.order,
            )
            for o in self.list_all()
        ]

    def by_layer(self) -> dict[str, list[OrganSummary]]:
        out: dict[str, list[OrganSummary]] = {layer.value: [] for layer in OrganLayer}
        for s in self.list_summaries():
            out[s.layer.value].append(s)
        return out


_registry: Optional[OrganRegistry] = None


def get_organ_registry() -> OrganRegistry:
    global _registry
    if _registry is None:
        _registry = OrganRegistry()
    return _registry
