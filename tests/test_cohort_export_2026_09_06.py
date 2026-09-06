"""The job-store adapter (2026-09-06): a completed pair job exports as the generator's envelope; the envelope assembles into a
cohort-packet/v1 that Codex's validator admits; rows are exact lines of the artifact with their anchors and fields."""
import copy
import json
from pathlib import Path

import pytest

from src.dossier.cohort_export import export_pair, fields_of, rows_of

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "communications/study/cohort_2026_09_06/fixtures"

A_TEXT = "Riley writes: I adopt Weber's distinction between class and status, but only for the interwar cases. Later he disputes it."
W_TEXT = "Weber's own words: classes are not communities; they merely represent possible bases for communal action."
FINAL = (
    "# Reading\n\n## Ledger\n\n"
    '- [D3.F1] Riley adopts Weber\'s class/status distinction for the interwar cases — dim: citation_move — ref: 5505 — move: adopted framework '
    '— stance: adopts — anchor: "I adopt Weber\'s distinction between class and status, but only for the interwar cases" — doc: BEFGGK6M — confidence: high\n'
    '- [D3.F2] Riley later disputes the distinction — dim: citation_stance — ref: 5506 — stance: disputes — anchor: "Later he disputes it" — doc: BEFGGK6M — confidence: medium\n'
    '- [X6.F3] The attribution holds against Weber\'s page — dim: paired_fidelity — pair-ref: 5505 — attribution: direct — verdict: fair — how: page '
    '— reason: the qualifier is Riley\'s — anchor: "I adopt Weber\'s distinction between class and status" — doc: BEFGGK6M '
    '— anchor-b: "classes are not communities" — doc-b: Q4WEBER1 — confidence: high\n'
)
INDEX = {"role": "evidence_index", "texts": [{"uid": "em:BEFGGK6M", "key": "BEFGGK6M", "passages": [{"ref_id": 5505}, {"ref_id": 5506}]}], "checks": []}


def _job(final=FINAL, status="done"):
    return {"id": "dossier-test1", "status": status, "updated_at": "2026-09-06T18:00:00", "analysis_job_id": "exec-1",
            "options": {"path": {"steps": [{"engine_key": "citation_engagement_map", "depth": "standard"}, {"engine_key": "citation_fidelity_audit", "depth": "standard"}]}},
            "documents": [{"key": "BEFGGK6M", "role": "source", "executor_doc_id": "d1"}, {"key": "Q4WEBER1", "role": "source", "executor_doc_id": "d2"},
                          {"key": "index", "role": "evidence_index", "executor_doc_id": "d3"}],
            "analysis": {"4.1": {"phase_number": 4.1, "engine_key": "citation_engagement_map", "depth": "standard", "passes": [{"pass_number": 1, "model": "sol", "output_id": "o1"}],
                                 "final_output": final, "final_wall": {"rows": 3, "failed_ids": ["D3.F2"]}}},
            "tables": [{"key": "passage_move_stance", "caption": "Moves", "columns": ["passage", "move"], "rows": [{"cells": [{"value": "[D3.F1] interwar"}, {"value": "adopted"}]}], "note": ""}],
            "totals": {"cost_usd": 1.5}}


def test_fields_and_rows_are_exact_and_carry_anchors_events_and_fields():
    assert fields_of('[D3.F1] c — dim: x — ref: 5 — anchor: "q" — doc: k') == {"dim": "x", "ref": "5", "anchor": '"q"', "doc": "k"}   # values verbatim, quotes kept
    rows = rows_of(FINAL, pair_key="em:riley__em:weber", engine="citation_engagement_map", failed_ids={"D3.F2"}, known_events={"5505", "5506"})
    assert [r["row_id"] for r in rows] == ["D3.F1", "D3.F2", "X6.F3"]
    r1, r2, r3 = rows
    assert r1["ref"] == "em:riley__em:weber::citation_engagement_map::D3.F1" and r1["dimension"] == "citation_move"
    assert r1["claim"] == "Riley adopts Weber's class/status distinction for the interwar cases" and r1["raw_row"].startswith("- [D3.F1]")
    assert r1["anchors"][0]["text"] == "I adopt Weber's distinction between class and status, but only for the interwar cases" and r1["anchors"][0]["voice"] == "A"
    assert r1["event_ids"] == ["5505"] and r1["fields"]["move"] == "adopted framework" and "anchor" not in r1["fields"]
    assert r2["anchor_status"] == "failed" and r2["status"] == "unresolved"
    assert [a["voice"] for a in r3["anchors"]] == ["A", "W"] and r3["anchors"][1]["source_doc_key"] == "Q4WEBER1" and r3["anchors"][1]["locus"]["how"] == "page"
    assert r3["fields"]["verdict"] == "fair" and r3["fields"]["how"] == "page"


def test_export_refuses_an_unfinished_job():
    with pytest.raises(ValueError):
        export_pair(_job(status="analysis"), author={"uid": "em:riley", "name": "Dylan Riley"}, member_uid="em:weber", memo_markdown="m", source_texts={})


def test_export_envelope_assembles_into_a_packet_the_validator_admits():
    from scripts.build_citation_cohort_fixture_2026_09_06 import assemble
    from scripts.validate_citation_cohort_2026_09_06 import validate_packet

    author = {"uid": "em:riley", "name": "Dylan Riley"}
    env = export_pair(_job(), author=author, member_uid="em:weber", memo_markdown="# The memo\n\nRiley adopts, then disputes.",
                      source_texts={"BEFGGK6M": A_TEXT, "Q4WEBER1": W_TEXT}, index=INDEX)
    pair = env["pair"]
    assert pair["pair_key"] == "em:riley__em:weber" and pair["doc_key"] == "pair::em:riley__em:weber"
    assert pair["lens_status"] == {"citation_engagement_map": "run", "citation_fidelity_audit": "unavailable", "citation_reception_map": "not_run"}
    assert pair["tables"][0]["row_refs"] == ["em:riley__em:weber::citation_engagement_map::D3.F1"]
    assert set(env["source_documents"]) == {"BEFGGK6M", "Q4WEBER1"} and env["receipt"]["gaps"][0].startswith("the critic's rejected rows")
    # the exported ledger keeps only the engagement engine's rows under that engine; the fidelity row rode in the same final output here
    # and is exported under the engagement ledger, so validation of a fidelity verdict is exercised by the row's own fields
    template = json.loads((FIXTURES / "synthetic_packet.json").read_text())
    cohort = copy.deepcopy(template["cohort"]); plan = copy.deepcopy(template["plan"])
    member = copy.deepcopy(cohort["members"][0])
    member.update(uid="em:weber", name="Max Weber", fixture_only=False, engaged="yes", row_id="COHORT.M1", anchor="member: em:weber; engaged: yes; count: 2",
                  counts={"total": 2, "mentions": 0, "bibliography_only": 0, "by_text": [{"text_key": "BEFGGK6M", "year": 2003, "count": 2, "event_ids": ["5505", "5506"]}]})
    cohort["members"] = [member]; cohort["not_engaged_residue"] = []
    cohort["coverage"]["held_texts"] = ["BEFGGK6M"]; cohort["coverage"]["inspected_texts"] = ["BEFGGK6M"]
    identities = {"author": author, "weber_uid": "em:weber", "lachmann_uid": None}
    packet = assemble({"id": "dossier-test1", "status": "done"}, [env], identities, cohort, plan)
    admitted = validate_packet(packet)
    assert set(admitted["pairs"]) == {"em:riley__em:weber"} and len(admitted["rows"]) == 3
    assert admitted["rows"]["em:riley__em:weber::citation_engagement_map::D3.F2"]["status"] == "unresolved"


def test_anchors_are_checked_under_the_walls_law_and_unfound_rows_are_downgraded():
    from src.dossier.cohort_export import anchor_refound, check_anchors, norm_for_anchor
    src = "He wrote that the state “en-\nmeshes,  controls” civil society; and more."
    assert anchor_refound('the state "enmeshes, controls" civil society', src)
    assert not anchor_refound("words that are not there", src)
    assert norm_for_anchor("a – b") == norm_for_anchor("a - b")
    rows = [{"anchors": [{"text": 'the state "enmeshes, controls" civil society', "source_doc_key": "k"}], "status": "confirmed", "anchor_status": "verified"},
            {"anchors": [{"text": "words that are not there", "source_doc_key": "k"}], "status": "confirmed", "anchor_status": "verified"}]
    counts = check_anchors(rows, {"k": src})
    assert counts == {"checked": 2, "refound": 1, "downgraded": 1}
    assert rows[0]["anchors"][0]["text"] == 'the state "enmeshes, controls" civil society'      # the row's own text is kept
    assert rows[1]["status"] == "unresolved" and rows[1]["anchor_status"] == "unverifiable"
