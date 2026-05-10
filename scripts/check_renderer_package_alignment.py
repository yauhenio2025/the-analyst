#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    renderers_root = repo_root / "renderers-ui"
    critic_root = repo_root.parent / "the-critic" / "webapp"

    if not critic_root.exists():
      fail(f"the-critic webapp not found at {critic_root}")

    renderer_pkg = read_json(renderers_root / "package.json")
    version = renderer_pkg["version"]

    tarball_name = f"the-syllabus-analysis-renderers-{version}.tgz"
    tarball_path = renderers_root / "release-artifacts" / tarball_name
    if not tarball_path.exists():
        fail(f"expected renderer artifact is missing: {tarball_path}")

    critic_pkg = read_json(critic_root / "package.json")
    critic_dep = critic_pkg["dependencies"]["@the-syllabus/analysis-renderers"]
    expected_dep = f"file:../../analyzer-v2/renderers-ui/release-artifacts/{tarball_name}"
    if critic_dep != expected_dep:
        fail(
            "the-critic dependency is misaligned: "
            f"expected {expected_dep!r}, found {critic_dep!r}"
        )

    installed_pkg_path = critic_root / "node_modules" / "@the-syllabus" / "analysis-renderers" / "package.json"
    if not installed_pkg_path.exists():
        fail(f"installed renderer package not found at {installed_pkg_path}")

    installed_pkg = read_json(installed_pkg_path)
    installed_version = installed_pkg["version"]
    if installed_version != version:
        fail(
            "installed renderer version is misaligned: "
            f"expected {version!r}, found {installed_version!r}"
        )

    print(
        json.dumps(
            {
                "renderer_package_version": version,
                "expected_tarball": str(tarball_path),
                "critic_dependency": critic_dep,
                "installed_package_version": installed_version,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
