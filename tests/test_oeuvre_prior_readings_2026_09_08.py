"""The oeuvre door accepts both older job IDs and portable reading references."""
from src.readings import registry
from src.sources.oeuvre_bundle import _prior_readings


def test_explicit_job_and_phase_references_hydrate_only_central_entries(monkeypatch):
    monkeypatch.setattr(registry, "prior_block", lambda *args: None)
    entries = [{"job_id": "old-job", "phase": "4.1", "when": "2026-09-07", "n_rows": 2},
               {"job_id": "old-job", "phase": "4.2", "when": "2026-09-08", "n_rows": 3}]
    monkeypatch.setattr(registry, "readings_for", lambda job: {"readings": entries if job == "old-job" else []})
    block = _prior_readings({"prior_readings": [{"job_id": "old-job", "phase": "4.1", "n_rows": 999},
                                                {"job_id": "old-job", "phase": "4.1"}, "missing-job"]})
    assert len(block["readings"]) == 1
    assert block["readings"][0]["phase"] == "4.1" and block["readings"][0]["n_rows"] == 2
    assert block["unavailable"] == [{"job_id": "missing-job", "phase": None}]
    all_phases = _prior_readings({"prior_readings": ["old-job"]})
    assert len(all_phases["readings"]) == 2


def test_unresolved_explicit_readings_remain_visible(monkeypatch):
    monkeypatch.setattr(registry, "prior_block", lambda *args: None)
    monkeypatch.setattr(registry, "readings_for", lambda **kwargs: {"readings": []})
    assert _prior_readings({"prior_readings": []}) is None
    block = _prior_readings({"prior_readings": [{"job_id": "old-job", "phase": "4.1"}]})
    assert block["readings"] == []
    assert block["unavailable"] == [{"job_id": "old-job", "phase": "4.1"}]
