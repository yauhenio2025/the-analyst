"""Every workflow JSON must validate and load — a silently skipped definition breaks live runs
("Workflow not found: dossier_standard", 2026-09-03)."""
import json
from pathlib import Path

from src.workflows.registry import WorkflowRegistry
from src.workflows.schemas import WorkflowDefinition

DEFS = Path(__file__).resolve().parents[1] / "src" / "workflows" / "definitions"


def test_every_workflow_definition_validates():
    files = sorted(DEFS.glob("*.json"))
    assert files, "no workflow definitions found"
    for f in files:
        WorkflowDefinition.model_validate(json.loads(f.read_text()))  # raises on failure


def test_registry_loads_all_definitions():
    reg = WorkflowRegistry()
    n_files = len(list(DEFS.glob("*.json")))
    assert len(reg.list_all()) == n_files, "a workflow definition failed to load"


def test_dossier_standard_has_the_eleven_phases_in_order():
    d = json.loads((DEFS / "dossier_standard.json").read_text())
    keys = [p.get("function_key") for p in d["phases"]]
    assert keys == ["dossier_reconnaissance", "dossier_brief", "dossier_plan", "dossier_analysis", "dossier_spine",
                    "dossier_tables", "dossier_figures", "dossier_plates", "dossier_compose", "dossier_crosscheck",
                    "dossier_receipts"]
    for p in d["phases"]:
        assert all(isinstance(x, (int, float)) for x in (p.get("depends_on_phases") or []))
