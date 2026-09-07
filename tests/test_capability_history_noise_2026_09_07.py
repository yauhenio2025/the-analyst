"""History records changes to records, not to the schema (2026-09-07: adding a field wrote 'No changes detected' into 166 files)."""
import json

import src.engines.history_tracker as ht
from src.engines.schemas_v2 import CapabilityEngineDefinition


def _def(**kw):
    base = {"engine_key": "t_engine", "engine_name": "T", "version": 1, "category": "scholarly", "kind": "synthesis",
            "problematique": "p", "researcher_question": "q", "intellectual_lineage": {"primary": "source_criticism"},
            "analytical_dimensions": [{"key": "d", "description": "d", "probing_questions": ["q?"]}], "apps": ["critic"]}
    return CapabilityEngineDefinition.model_validate({**base, **kw})


def test_a_schema_only_hash_change_writes_no_entry_but_a_real_change_does(tmp_path, monkeypatch):
    monkeypatch.setattr(ht, "HISTORY_DIR", tmp_path)
    for name in ("SNAPSHOT_DIR", "HISTORY_PATH"):
        if hasattr(ht, name):
            monkeypatch.setattr(ht, name, tmp_path)
    d = _def()
    assert ht.check_and_record_changes(d).is_baseline is True                 # first call: the baseline
    assert ht.check_and_record_changes(d) is None                             # unchanged: nothing
    # a field the diff did not compare before: the hash moves, the record does not → no entry, the snapshot settles
    same_but_new_field = _def(operation=None)
    assert ht.check_and_record_changes(same_but_new_field) is None
    entries = json.loads((tmp_path / "t_engine.json").read_text())["entries"]
    assert len(entries) == 1 and entries[0]["is_baseline"] is True
    # a real change to a record is recorded, and `operation` is now one of the compared fields
    e = ht.check_and_record_changes(_def(operation="ascent"))
    assert e is not None and any(c["field"] == "operation" for c in json.loads((tmp_path / "t_engine.json").read_text())["entries"][0]["changes"])
