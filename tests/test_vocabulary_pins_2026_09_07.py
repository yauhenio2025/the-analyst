"""Enumerated fields are shape: the wall reports a value outside its vocabulary where the row is produced; a reader normalises."""
from src.executor.ledger_walls import parse_rows
from src.vocabularies.pins import drift_of, match_value, pinned_fields, vocabulary_drift


def test_the_wall_reports_drift_and_the_reader_normalises():
    pinned = pinned_fields("retrospective_reading")
    assert pinned["verdict"] == ["culmination", "continuation", "departure"]
    assert match_value("qualified culmination", pinned["verdict"]) == (None, "culmination") and match_value("Continuation", pinned["verdict"]) == ("continuation", None)
    assert drift_of({"verdict": "a fresh start"}, pinned) == [{"field": "verdict", "value": "a fresh start", "fixed": None}] and drift_of({"verdict": "departure"}, pinned) == []
    out = ("[R4.F1] The paper culminates the critique — dim: verdict — verdict: qualified culmination — anchor: \"x\" — doc: focal:em:F — confidence: high\n"
           "[R4.F2] Another — dim: verdict — verdict: continuation — anchor: \"y\" — doc: focal:em:F — confidence: low")
    rows = parse_rows(out)
    assert vocabulary_drift(rows, "retrospective_reading") == [{"id": "R4.F1", "field": "verdict", "value": "qualified culmination", "fixed": "culmination"}]
    assert vocabulary_drift(rows, "engine_with_no_vocabulary") == []
    from src.dossier.explainer import rows_with_fields
    read = rows_with_fields(out, engine_key="retrospective_reading")
    assert read[0]["fields"]["verdict"] == "culmination" and read[0]["fields"]["verdict_raw"] == "qualified culmination" and read[0]["drift"][0]["fixed"] == "culmination"
