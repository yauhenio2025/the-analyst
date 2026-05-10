#!/usr/bin/env python3
"""Fail-loud preflight for repo-tracked renderer contracts.

Usage:
    python scripts/check_renderer_contracts.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.renderers.validator import validate_all_schemas, validate_renderer_registry_artifacts


def main() -> int:
    registry_preflight = validate_renderer_registry_artifacts()
    schema_health = validate_all_schemas()

    schema_issues: dict[str, dict[str, object]] = {}
    for renderer_key, entry in schema_health.items():
        if entry["input_schema_valid"] and entry["config_schema_valid"]:
            continue
        schema_issues[renderer_key] = entry

    payload = {
        "registry_preflight": registry_preflight,
        "schema_issues": schema_issues,
    }

    if registry_preflight["valid"] and not schema_issues:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
