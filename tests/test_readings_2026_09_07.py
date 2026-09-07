"""The readings ledger (Evgeny, 2026-09-07 18:30): every heavy reading leaves its rows behind, indexed by person and by text."""
import json

import src.readings.registry as rl


def _store(monkeypatch):
    store: dict[str, bytes] = {}
    monkeypatch.setattr(rl, "_put", lambda key, mime, data: store.__setitem__(key, data))
    monkeypatch.setattr(rl, "_get", lambda key: store.get(key))
    return store


def test_a_finished_job_is_indexed_by_person_and_text_and_read_back(monkeypatch):
    store = _store(monkeypatch)
    ip = ("[I2.F1] Brenner: the state responds to capital — dim: their_claim — interlocutor: Brenner — question: I1.F1 — role: foil — locus: pp. 88–90 — turn_says: no autonomy — anchor: \"the state is just a way to respond to capital\" — doc: em:BJ4R4EPJ — confidence: high\n"
          "[I2.F2] Arrighi: the territorial logic is a strategy of rulers — dim: their_claim — interlocutor: Arrighi — question: I1.F1 — role: encounter — locus: ch. 1 — turn_says: none — anchor: \"rival strategies of rulers\" — doc: em:ARR2005 — confidence: medium")
    tp = ("[P3.F1] Meek: not a candidate — dim: verdict — person: Meek, Ronald — verdict: not_a_candidate — reason: bibliographic — anchor: \"Meek is cited\" — doc: focal:em:CBT7B8CL — confidence: high")
    job = {"id": "d-r", "updated_at": "2026-09-07T15:00:00Z", "options": {"intent": "the state's logic against Brenner"},
           "analysis": {"4.4": {"engine_key": "interlocutor_position", "final_output": ip, "final_wall": {"failed_ids": ["I2.F2"]}, "cost_usd": 0.15, "depth": "surface"},
                        "4.7": {"engine_key": "thinker_placement", "final_output": tp, "final_wall": {"failed_ids": []}, "cost_usd": 0.23}}}
    entries = rl.index_job(job)
    assert [(e["engine"], e["n_rows"]) for e in entries] == [("interlocutor_position", 2), ("thinker_placement", 1)]
    got = rl.readings_for(person="Brenner")
    assert got["count"] == 1 and got["readings"][0]["job_id"] == "d-r" and got["readings"][0]["renders"] == ["/v1/dossier/jobs/d-r/distinctions"]
    assert rl.readings_for(person="Meek")["count"] == 1                      # 'Meek' finds 'Meek, Ronald' through the surname index
    assert rl.readings_for(person="Meek, Ronald")["readings"][0]["engine"] == "thinker_placement"
    assert rl.readings_for(text="em:BJ4R4EPJ")["count"] == 1 and rl.readings_for(text="em:CBT7B8CL")["count"] == 1 and rl.readings_for(text="em:NONE")["count"] == 0
    assert [e["phase"] for e in rl.readings_for(job="d-r")["readings"]] == ["4.7", "4.4"] or len(rl.readings_for(job="d-r")["readings"]) == 2
    r = rl.reading("d-r", "4.4")
    assert r["persons"] == ["Brenner", "Arrighi"] and r["texts"] == ["em:BJ4R4EPJ", "em:ARR2005"] and r["rows"][1]["conjecture"] is True and r["rows"][0]["locus"] == "pp. 88–90"
    # re-indexing the same job replaces, never duplicates
    rl.index_job(job)
    assert rl.readings_for(person="Brenner")["count"] == 1
    # what a planner reads before it spends
    block = rl.prior_block(["Brenner", "Nobody"], ["em:ARR2005"])
    assert len(block["readings"]) == 1 and block["readings"][0]["about"] == "Brenner" and "read only what is new" in block["note"]
    assert rl.prior_block(["Nobody"], []) is None
