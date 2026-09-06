"""The evidential frame of a hypothesis test (owner's ask, 2026-09-06): the engine loads, sits under Test a position,
its rows render to the Stacks' JSON by code, and an engines-only job ends with its ledgers instead of running the desks."""
from src.dossier.frame import render_frame

FINAL = """## The form the argument must take

For the hypothesis to hold, Brenner would have to claim that competitive retention generates the property rules, and Hayek would have to grant that a selector can be politically constituted.

| evidence | kind | where | held | finding |
|---|---|---|---|---|
| a derivation of property rules from retention | primary text | Brenner, The Low Countries in the Transition to Capitalism (2001) | no | S1.F1 |

- [S1.F1] A derivation of the property rules from competitive retention in Brenner's own words — dim: strengthen — kind: primary text — where: Robert Brenner, The Low Countries in the Transition to Capitalism (2001); the section on Holland — held: no — anchor: "Brenner does not generally derive the property relations making competition compulsory" — doc: memo — confidence: high
- [S2.F1] A Hayek passage that makes the selector's constitution political — dim: weaken — kind: primary text — where: Friedrich A. Hayek, Law, Legislation and Liberty (2011) — held: yes — anchor: "it is at least conceivable that the formation of a spontaneous order relies entirely on rules that were deliberately made" — doc: memo — confidence: medium
- [S3.F1] The hypothesis must claim isomorphism of mechanisms, not identity of selectors — dim: form — account: hypothesis — anchor: "the two accounts differ only in the name of the selector" — doc: memo — confidence: high
- [S4.F1] Whether Brenner's Dutch case derives property rules from retention — dim: decisive_test — question: does the Dutch chapter derive the rules from sorting? — evidence-needed: a passage on the origin of Dutch property rules — sources: Robert Brenner, The Low Countries in the Transition to Capitalism (2001) — decidable-now: no — why: the work is not held — rank: 1 — anchor: "Peasants were separated from possession of their means of subsistence by ecological shifts" — doc: memo — confidence: medium
- [S4.F2] Whether Hayek's imitation channel needs a political author — dim: decisive_test — question: does imitation presuppose an authored rule? — evidence-needed: the Constitution of Liberty chapter on imitation — sources: Friedrich A. Hayek, The Constitution of Liberty (2011), p. 118 — decidable-now: yes — why: held — rank: 2 — anchor: "the selection by imitation of successful institutions and habits" — doc: memo — confidence: medium
- [S5.F1] Whether 'rule' means the same thing in both accounts — dim: residual — because: argument — anchor: "Hayek also distinguishes rules from order" — doc: memo — confidence: low
- [S5.F2] What the Fatal Conceit says about authored rules — dim: residual — because: coverage — confidence: low
"""


def _job(final=FINAL):
    return {"id": "d-frame", "status": "done", "analysis": {"4.1": {"engine_key": "hypothesis_evidential_frame", "final_output": final, "final_wall": {"failed_ids": []}}}}


def test_the_engine_loads_and_sits_under_test_a_position():
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.dossier.catalog import purpose_catalog
    cap = get_engine_registry().get_capability_definition("hypothesis_evidential_frame")
    assert cap and [d.key for d in cap.analytical_dimensions] == ["strengthen", "weaken", "form", "decisive_test", "residual"]
    op = get_operationalization_registry().get("hypothesis_evidential_frame")
    assert op and [d.id_prefix for d in op.process.dimensions] == ["S1", "S2", "S3", "S4", "S5"]
    cat = purpose_catalog("researcher")
    groups = cat.get("groups") if isinstance(cat, dict) else cat
    tp = next(g for g in groups if g.get("key") == "test_position")
    assert any(e.get("engine_key") == "hypothesis_evidential_frame" for e in tp.get("engines", []))


def test_the_frame_renders_from_the_rows_by_code():
    f = render_frame(_job())
    assert f["engine"] == "hypothesis_evidential_frame" and f["rows"] == 7 and f["conjectures"] == 1
    assert [e["id"] for e in f["strengthen"]] == ["S1.F1"] and f["strengthen"][0]["held"] == "no" and f["strengthen"][0]["kind"] == "primary text"
    assert f["weaken"][0]["where"].startswith("Friedrich A. Hayek") and f["weaken"][0]["conjecture"] is False
    assert f["form"]["paragraph"].startswith("For the hypothesis to hold") and f["form"]["conditions"][0]["account"] == "hypothesis"
    assert [t["rank"] for t in f["decisive_tests"]] == [1, 2] and f["decisive_tests"][0]["decidable_now"] == "no" and f["tests"] is f["decisive_tests"]
    assert f["residual"] == ["Whether 'rule' means the same thing in both accounts (because: argument)", "What the Fatal Conceit says about authored rules (because: coverage)"]
    assert f["works"][:2] == ["Robert Brenner, The Low Countries in the Transition to Capitalism (2001)", "Friedrich A. Hayek, Law, Legislation and Liberty (2011)"]
    assert render_frame({"id": "x", "analysis": {}}) is None


def test_an_engines_only_job_skips_the_desks(monkeypatch):
    from src.dossier import runner
    from src.dossier.schemas import DossierJob, DossierOptions, OutputOptions
    steps, notes = [], []
    job = DossierJob(id="d-eo", status="analysis", step="spine", options=DossierOptions(intent="x", output=OutputOptions(text=False, tables=False, figures=0, plates=0)))
    monkeypatch.setattr(runner, "get_job", lambda job_id: job)
    monkeypatch.setattr(runner, "load_documents", lambda job: [])
    monkeypatch.setattr(runner, "_next_step", lambda job: "spine")
    monkeypatch.setattr(runner, "_run_step", lambda job, step, docs: steps.append(step))
    monkeypatch.setattr(runner, "update_job", lambda job_id, **f: None)
    monkeypatch.setattr(runner.events, "emit", lambda job_id, kind, **kw: notes.append(kw.get("detail", "")))
    runner._run("d-eo")
    assert steps == ["receipts"] and any(d.startswith("engines only") for d in notes)
    full = DossierJob(id="d-f", options=DossierOptions(intent="x"))
    assert runner._engines_only(full) is False
