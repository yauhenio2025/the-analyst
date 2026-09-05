"""Brief v2 (deliverable-first): the code-side checks of DESIGN_brief_deliverables §B5, the schema's
back-compat views, per-option estimates, the purpose catalog, and the plan honouring a fixed path.
No network: every test runs on fixtures and a fake engine registry."""
from __future__ import annotations

import json

import pytest

from src.dossier.brief import (CAPS, CheckContext, apply_code_fixes, check_brief, is_concrete, overlap, option_schema,
                               brief_schema, system_prompt, truncate)
from src.dossier.catalog import (EXECUTIVE_BAN_TERMS, estimate_path, jargon_hits, path_depth_from_steps, purpose_catalog,
                                 resolve_path_request, vocabulary_lines)
from src.dossier.schemas import (Brief, BriefOption, CreateDossierRequest, DossierJob, DossierOptions, Path, PathRequest,
                                 PathStep, PathStepRequest, Promise, Recommendation, Shape, ShapeRef, TableSpec, UseFrame)

FAKE = {
    k: {"engine_key": k, "engine_name": k.replace("_", " ").title(), "depths": {"surface": {"passes": 1}, "standard": {"passes": 2}, "deep": {"passes": 4}}}
    for k in ("argument_architecture", "inferential_commitment_mapper", "dialectical_structure", "structural_pattern_detector",
              "concept_taxonomy_argumentative_function", "deep_summarization", "comparative_reasoning_analyzer", "counterfactual_analyzer",
              "concept_evolution", "epistemological_method_detector")
}
DOC_KEYS = {"U3PWD6J3", "SG4IGV3Y", "WUPV36YG", "XDYU5FSQ", "CW9WK9KL"}
ENTITIES = {"shein", "house", "gucci", "the ceo"}


def ctx(**kw) -> CheckContext:
    base = dict(audience="executive", doc_keys=DOC_KEYS, entities=ENTITIES, by_key=FAKE, use_kind_given=False, ban=EXECUTIVE_BAN_TERMS)
    base.update(kw)
    return CheckContext(**base)


def promise(text: str, *refs: str) -> dict:
    kinds = {"T": "table", "S": "section", "F": "figure", "§": "section"}
    return {"text": text, "supported_by": [{"kind": kinds[r[0]], "index": int(r[1:])} for r in refs]}


def option(key="stress", use_kind="stress_test", steps=("inferential_commitment_mapper", "dialectical_structure"),
           depths=("surface", "surface"), able=None, understand=None, tables=2, figures=1, **over) -> dict:
    o = {
        "key": key, "title": "Where your sustainability claims will break", "deliverable_kind": "stress_test",
        "deliverable": "A 5-section stress test of the four claim types a house makes, with a scorecard of what each commits you to.",
        "use_kind": use_kind,
        "you_will_understand": understand or [
            promise("the two ways a claim fails for consumers as the 12 interviewees described them [U3PWD6J3]", "T1"),
            promise("for each of the 10 practices, the market counter-move that turns it back into a sales story [SG4IGV3Y]", "T2"),
            promise("how a hashflag gesture is withdrawn when it collides with commercial interest [WUPV36YG]", "S3"),
        ],
        "you_will_be_able_to": able or [
            promise("decide which claim types to advance and which to retire before the next campaign [U3PWD6J3]", "T1"),
            promise("brief comms on the three questions an investigation will ask [WUPV36YG]", "S4"),
        ],
        "questions_answered": ["What makes a claim legitimate?", "Which practices are most exposed?", "When does silence cost more?"],
        "not_for": ["It does not score the house's own claims — none are in these documents."],
        "shape": {
            "sections": [{"heading": f"Section {i}", "answers": "q"} for i in range(1, 5)],
            "tables": [{"title": f"Table {i}", "row_unit": "one row per claim type", "columns": ["a", "b", "c"], "rows_expected": "4-6", "carried_by": ["U3PWD6J3"]} for i in range(1, tables + 1)],
            "figures": [{"title": "Grid", "format": "two_axis_grid", "scene": "a grid"} for _ in range(figures)],
        },
        "evidence_base": {"carrying_docs": [{"doc_key": "U3PWD6J3", "carries": "the legitimacy criteria"}], "thin_or_missing": ["no house data"]},
        "path": {"steps": [{"engine_key": k, "plain_name": "x", "contributes": "adds the ledger", "depth": d} for k, d in zip(steps, depths)]},
        "best_when": "Pick this when a campaign is planned in the next two quarters.",
    }
    o.update(over)
    return o


def brief(*opts, rec="stress") -> Brief:
    opts = opts or (
        option(),
        option(key="bench", use_kind="brief", steps=("structural_pattern_detector",), depths=("surface",),
               able=[promise("rank where the house is most exposed against Shein [XDYU5FSQ]", "T1"), promise("name the three disclosures a sourcing story now needs [CW9WK9KL]", "T2")], tables=2, figures=1),
        option(key="guide", use_kind="learn", steps=("deep_summarization", "argument_architecture", "dialectical_structure", "counterfactual_analyzer"),
               depths=("surface", "standard", "standard", "standard"),
               able=[promise("onboard a team in an hour on the five papers [SG4IGV3Y]", "S1"), promise("choose which of the 5 papers to send to whom", "T1")], tables=3, figures=2),
    )
    return Brief.model_validate({"options": list(opts), "recommendation": {"option_key": rec, "because": "the papers carry the legitimacy criteria [U3PWD6J3] but no house data"},
                                 "defaults": {"audience": "executive", "depth": "medium", "figures": 2}})


# ── schema ─────────────────────────────────────────────────────────────────

def test_v2_option_validates_and_derives_legacy_views():
    o = BriefOption.model_validate(option())
    assert o.version == 2
    assert o.telling.startswith("A 5-section stress test") and "[U3PWD6J3]" in o.telling
    assert [e.engine_key for e in o.engines] == ["inferential_commitment_mapper", "dialectical_structure"]
    assert o.engines[0].why == "adds the ledger"
    assert o.output_shape.sections == ["Section 1", "Section 2", "Section 3", "Section 4"]
    assert o.output_shape.tables[0] == "Table 1 — one row per claim type"
    assert o.output_shape.figures[0].startswith("Grid (two_axis_grid)")
    assert o.refs() == ["T1", "T2", "§3", "T1", "§4"]
    # the derived views survive a store round-trip
    again = BriefOption.model_validate(json.loads(o.model_dump_json()))
    assert again.telling == o.telling and again.version == 2


def test_v1_option_keeps_its_stored_values():
    o = BriefOption.model_validate({"key": "k", "title": "T", "telling": "the old paragraph",
                                    "engines": [{"engine_key": "argument_architecture", "why": "w"}],
                                    "output_shape": {"sections": ["a"], "tables": ["b"], "figures": []}, "est_cost_usd": 1.5})
    assert o.version == 1 and o.telling == "the old paragraph" and o.engines[0].why == "w" and o.output_shape.tables == ["b"]
    b = Brief.model_validate({"options": [o.model_dump()], "defaults": {}})
    assert b.version == 1 and b.entry == "use" and b.recommendation is None and b.autopilot_key() == "k"
    assert "no recommendation" in b.autopilot_reason()


def test_autopilot_executes_the_recommendation_with_its_reason():
    b = brief(rec="bench")
    assert b.autopilot_key() == "bench"
    assert b.autopilot_reason().startswith("the material decided: Where your sustainability claims will break — because")


def test_model_facing_schema_has_no_prices_and_enums():
    s = brief_schema()
    props = s["properties"]["options"]["items"]["properties"]
    assert "est_cost_usd" not in props and "telling" not in props and "engines" not in props
    assert "stress_test" in props["use_kind"]["enum"] and "two_axis_grid" in props["shape"]["properties"]["figures"]["items"]["properties"]["format"]["enum"]
    assert s["properties"]["options"]["minItems"] == 3 and brief_schema(translate=True)["properties"]["options"]["maxItems"] == 2
    assert "alternative" in option_schema(translate=True)["properties"]
    assert "THE PATH IS FIXED: a → b" in system_prompt("a → b") and "no repeats" in system_prompt()


# ── checks ─────────────────────────────────────────────────────────────────

def test_good_brief_passes_the_model_checks():
    rep = check_brief(brief(), ctx())
    assert rep.model_issues == [], rep.lines()


def test_use_kinds_must_differ():
    b = brief(option(), option(key="b", use_kind="stress_test"), option(key="c", use_kind="learn"))
    rep = check_brief(b, ctx())
    assert any(i.field == "use_kind" and "share" in i.message for i in rep.model_issues)


def test_able_to_sets_must_not_overlap_when_a_use_was_stated():
    same = [promise("decide which claim types to advance and which to retire before the next campaign [U3PWD6J3]", "T1"),
            promise("brief comms on the three questions an investigation will ask [WUPV36YG]", "S4")]
    b = brief(option(), option(key="b", use_kind="brief", able=same), option(key="c", use_kind="learn"))
    assert not any(i.field == "you_will_be_able_to" and "same things" in i.message for i in check_brief(b, ctx()).model_issues)
    rep = check_brief(b, ctx(use_kind_given=True))
    assert any(i.option_key == "b" and "same things" in i.message for i in rep.model_issues)
    assert overlap("decide which claims to retire", "set the walk-away conditions") == 0.0


def test_concreteness_rejects_lines_true_of_any_corpus():
    assert not is_concrete("decide which claims to advance and which to retire", DOC_KEYS, ENTITIES)
    assert is_concrete("decide … [U3PWD6J3]", DOC_KEYS, ENTITIES)
    assert is_concrete("what Shein's scoring does to supplier margins", DOC_KEYS, ENTITIES)
    assert is_concrete("2,000 new styles a day", DOC_KEYS, ENTITIES)
    assert is_concrete('the filing\'s own phrase — “low cultural relevance”', DOC_KEYS, ENTITIES)
    assert is_concrete("key terms — 'national security', 'modernisation' — and what they license", DOC_KEYS, ENTITIES)
    assert not is_concrete("the programme's aims and the board's claims", DOC_KEYS, ENTITIES)  # apostrophes are not quotes
    b = brief(option(able=[promise("decide which claims to advance and retire", "T1"), promise("brief comms [WUPV36YG]", "S4")]))
    rep = check_brief(b, ctx())
    assert any("not concrete" in i.message for i in rep.model_issues)


def test_support_refs_must_resolve_and_are_stripped_after_repair():
    b = brief(option(able=[promise("decide which claim types to retire [U3PWD6J3]", "T5"), promise("brief comms [WUPV36YG]", "S4")]))
    rep = check_brief(b, ctx())
    assert any("T5 does not exist" in i.message for i in rep.model_issues)
    apply_code_fixes(b, ctx(), corpus_chars=100_000)
    p = b.options[0].you_will_be_able_to[0]
    assert p.supported_by == [] and p.unsupported is True
    assert any("unresolvable" in n for n in b.options[0].notes)


def test_row_unit_must_start_with_one_row_per_and_is_normalised():
    o = option()
    o["shape"]["tables"][0]["row_unit"] = "claim types"
    b = brief(o)
    assert any("one row per" in i.message for i in check_brief(b, ctx()).model_issues)
    apply_code_fixes(b, ctx(), corpus_chars=100_000)
    assert b.options[0].shape.tables[0].row_unit == "one row per claim types"


def test_executive_vocabulary_is_banned_but_quoted_and_analyst_are_not():
    o = option(deliverable="A stress test of the house's inferential commitments and dialectical structure.")
    rep = check_brief(brief(o), ctx())
    hit = [i for i in rep.model_issues if i.field == "vocabulary"]
    assert hit and "inferential commitment" in hit[0].message and "deliverable" in hit[0].message
    assert check_brief(brief(o), ctx(audience="analyst", ban=())).model_issues == []
    assert jargon_hits('the paper calls it a “spatial-digital fix” and a hegemonic frame', EXECUTIVE_BAN_TERMS) == ["hegemonic"]
    assert jargon_hits("the house's claims and the firm's promises", EXECUTIVE_BAN_TERMS) == []
    assert jargon_hits("post-structuralist", EXECUTIVE_BAN_TERMS) == ["post-structuralist"]
    assert len(vocabulary_lines("executive")) >= 30 and vocabulary_lines("analyst") == []


def test_lengths_are_truncated_at_word_boundaries():
    long = "word " * 60
    o = option(deliverable=long.strip(), best_when=long.strip())
    b = brief(o)
    rep = check_brief(b, ctx())
    length_issue = [i for i in rep.model_issues if i.field == "lengths"]
    assert length_issue and "deliverable (" in length_issue[0].message and "best_when (" in length_issue[0].message
    apply_code_fixes(b, ctx(), corpus_chars=100_000)
    d = b.options[0].deliverable
    assert len(d) <= CAPS["deliverable"] + 1 and d.endswith("…")
    assert truncate("short", 10) == "short"


def test_engines_unknown_dropped_plain_names_overwritten_and_fallback():
    o = option(steps=("not_an_engine", "inferential_commitment_mapper", "inferential_commitment_mapper"), depths=("surface", "surface", "surface"))
    b = brief(o)
    rep = check_brief(b, ctx())
    assert any("not executable" in i.message for i in rep.model_issues)
    apply_code_fixes(b, ctx(), corpus_chars=100_000)
    steps = b.options[0].path.steps
    assert [s.engine_key for s in steps] == ["inferential_commitment_mapper"]
    assert steps[0].plain_name == "hidden-obligations map"
    assert b.options[0].engines[0].engine_key == "inferential_commitment_mapper"  # derived view re-computed
    b2 = brief(option(steps=("nope",), depths=("surface",)))
    apply_code_fixes(b2, ctx(), corpus_chars=100_000)
    assert [s.engine_key for s in b2.options[0].path.steps] == ["deep_summarization"]
    b3 = brief(option())
    apply_code_fixes(b3, ctx(audience="analyst", ban=()), corpus_chars=100_000)
    assert b3.options[0].path.steps[0].plain_name == "Inferential Commitment Mapper"


def test_weight_spread_is_a_note_not_a_repair():
    b = brief(option(), option(key="b", use_kind="brief"), option(key="c", use_kind="learn"))
    rep = check_brief(b, ctx())
    assert any("weight spread" in n for n in rep.notes) and not any(i.field == "path.depth" for i in rep.model_issues)


def test_recommendation_falls_back_to_option_one():
    b = brief(rec="nowhere")
    rep = check_brief(b, ctx())
    assert any(i.field == "recommendation" for i in rep.issues)
    notes = apply_code_fixes(b, ctx(), corpus_chars=100_000)
    assert b.recommendation.option_key == "stress" and any("recommendation missing" in n for n in notes)


def test_estimates_differ_across_the_three_weights():
    b = brief()
    apply_code_fixes(b, ctx(), corpus_chars=349_233)
    light, standard, full = (b.options[1], b.options[0], b.options[2])
    assert light.path.depth == "simple" and standard.path.depth == "medium" and full.path.depth == "advanced"
    assert light.est_cost_usd < standard.est_cost_usd < full.est_cost_usd
    assert light.est_minutes < standard.est_minutes < full.est_minutes
    assert full.est_llm_calls == 1 + 2 + 2 + 2 + 4
    cost1, _, _ = estimate_path(Path(steps=[PathStep(engine_key="deep_summarization", depth="surface")]), 60_000, FAKE)
    cost2, _, _ = estimate_path(Path(steps=[PathStep(engine_key="deep_summarization", depth="deep")]), 60_000, FAKE)
    assert cost1 < cost2
    assert path_depth_from_steps([PathStep(engine_key="deep_summarization", depth="surface")], FAKE) == "simple"


# ── catalog and paths ──────────────────────────────────────────────────────

def test_purpose_catalog_joins_the_runtime_registry():
    c = purpose_catalog("executive", corpus_chars=349_233, n_docs=5, same_author=False)
    engines = [e for g in c["groups"] for e in g["engines"]]
    import json as _json
    purpose = _json.load(open("src/dossier/catalog_purpose.json"))
    listed = {e["engine_key"] for g in purpose["groups"] for e in g["engines"]}
    excluded = {e["engine_key"] for e in purpose["excluded"]}
    offered = {e["engine_key"] for e in engines}
    # Eligible purpose entries and unlisted capabilities are offered; explicit exclusions are withheld.
    assert listed - excluded <= offered and not (excluded & offered)
    assert len(engines) == len(offered) >= 22 and {e["engine_key"] for e in c["excluded"]} == excluded and len(c["recipes"]) == 7
    assert {"aoi_thematic_synthesis", "aoi_engagement_mapping", "aoi_sin_findings", "aoi_thematic_report",
            "genealogy_relationship_classification", "genealogy_final_synthesis"} <= excluded
    by = {e["engine_key"]: e for e in engines}
    assert by["chapter_role_analyzer"]["fit"] == "off" and by["evolution_tactics_detector"]["fit"] == "off"
    assert by["inferential_commitment_mapper"]["plain_name"] == "hidden-obligations map"
    assert by["inferential_commitment_mapper"]["depths"]["surface"]["est_cost_usd"] > 0
    assert all(jargon_hits(e["plain_name"], EXECUTIVE_BAN_TERMS) == [] for e in engines)
    single = purpose_catalog("analyst", n_docs=1)
    by1 = {e["engine_key"]: e for g in single["groups"] for e in g["engines"]}
    assert by1["chapter_role_analyzer"]["fit"] == "conditional" and by1["argument_architecture"]["plain_name"] == "Argument Architecture Mapper"
    assert all(r["est_cost_usd"] > 0 for r in c["recipes"]) and c["own_overhead"]["calls"] == 4


def test_resolve_path_request_fills_recipes_and_rejects_bad_paths():
    p = resolve_path_request(PathRequest(chain_key="stress_test"), "executive", FAKE)
    assert [s.engine_key for s in p.steps] == ["argument_architecture", "inferential_commitment_mapper"] and p.depth == "medium"
    assert p.steps[0].plain_name == "claim scorecard"
    with pytest.raises(ValueError):
        resolve_path_request(PathRequest(steps=[PathStepRequest(engine_key="aoi_thematic_synthesis")]), "executive", FAKE)
    with pytest.raises(ValueError):
        resolve_path_request(PathRequest(steps=[PathStepRequest(engine_key=k) for k in ("argument_architecture", "dialectical_structure", "deep_summarization", "concept_evolution", "counterfactual_analyzer")]), "executive", FAKE)
    with pytest.raises(ValueError):
        resolve_path_request(PathRequest(chain_key="no_such_recipe"), "executive", FAKE)
    full = resolve_path_request(PathRequest(chain_key="full_read"), "executive", FAKE)
    assert [s.engine_key for s in full.steps][-1] == "deep_summarization" and len(full.steps) == 4  # trailing synthesis may repeat


def test_validate_lane_rejects_non_executable_paths_and_maps_autopilot():
    from src.api.routes.dossier import validate_lane

    req = CreateDossierRequest(sources=[], autopilot=True)
    assert validate_lane(req)["entry"] == "material"
    req = CreateDossierRequest(sources=[], entry="chosen", path=PathRequest(steps=[PathStepRequest(engine_key="argument_architecture")]))
    assert validate_lane(req)["entry"] == "chosen"
    with pytest.raises(ValueError):
        validate_lane(CreateDossierRequest(sources=[], entry="chosen"))
    with pytest.raises(ValueError):
        validate_lane(CreateDossierRequest(sources=[], entry="chosen", path=PathRequest(steps=[PathStepRequest(engine_key="aoi_sin_findings")])))
    with pytest.raises(ValueError):
        validate_lane(CreateDossierRequest(sources=[], use_frame=UseFrame(use_kind="dance")))
    with pytest.raises(ValueError):
        validate_lane(CreateDossierRequest(sources=[], entry="sideways"))


def test_plan_honours_a_fixed_path_exactly():
    from src.dossier.plan import fixed_path, fixed_phases
    from src.dossier.schemas import DossierPlanPhase

    v2 = BriefOption.model_validate(option(steps=("dialectical_structure", "inferential_commitment_mapper"), depths=("standard", "surface")))
    job = DossierJob(options=DossierOptions(entry="use"), brief=Brief(options=[v2]), chosen_option=v2.key)
    fp = fixed_path(job, v2, FAKE)
    assert fp is not None and [s.engine_key for s in fp.steps] == ["dialectical_structure", "inferential_commitment_mapper"]
    proposed = [DossierPlanPhase(phase_number=0, engine_key="argument_architecture", why="model's idea", context_emphasis="x"),
                DossierPlanPhase(phase_number=0, engine_key="inferential_commitment_mapper", depth="deep", why="w2", context_emphasis="ledger first")]
    phases = fixed_phases(fp, proposed, FAKE)
    assert [(p.engine_key, p.depth, p.passes) for p in phases] == [("dialectical_structure", "standard", 2), ("inferential_commitment_mapper", "surface", 1)]
    assert phases[1].context_emphasis == "ledger first" and phases[0].why == "adds the ledger"
    assert [p.phase_number for p in phases] == [4.1, 4.2]
    # lane 2: the request's own path wins
    job2 = DossierJob(options=DossierOptions(entry="chosen", path=PathRequest(chain_key="reading_guide")), brief=Brief(options=[v2]))
    assert [s.engine_key for s in fixed_path(job2, v2, FAKE).steps] == ["deep_summarization"]
    # legacy v1 option: the old planner
    v1 = BriefOption.model_validate({"key": "k", "title": "T", "telling": "t", "engines": [{"engine_key": "argument_architecture"}]})
    assert fixed_path(DossierJob(options=DossierOptions()), v1, FAKE) is None


def test_bare_string_promises_are_coerced_not_rejected():
    """The the house sample's first answer gave promises as strings: a shape-only coercion saves the $0.10 re-ask;
    the refs check then sends the missing supported_by to the single repair round."""
    o = option(understand=["Why the CEO's 'follow the creatives' line is the pitch's entry point [house_study_md]"] * 3,
               able=["decide the opening line [house_study_md]", "avoid the two misfires [house_study_md]"])
    o["evidence_base"]["carrying_docs"] = ["house_study_md"]
    o["shape"]["sections"] = ["What the stack does", "The layer nobody builds", "The opening line"]
    o["path"]["steps"] = ["argument_architecture"]
    bo = BriefOption.model_validate(o)
    assert bo.you_will_understand[0].supported_by == [] and bo.you_will_understand[0].text.startswith("Why the CEO")
    assert bo.evidence_base.carrying_docs[0].doc_key == "house_study_md"
    assert bo.shape.sections[1].heading == "The layer nobody builds" and bo.path.steps[0].engine_key == "argument_architecture"
    rep = check_brief(Brief(options=[bo]), ctx(doc_keys={"house_study_md"}))
    assert any("no supported_by" in i.message for i in rep.model_issues)


def test_fallback_option_and_shape_ref_labels():
    assert ShapeRef(kind="section", index=5).label() == "§5" and ShapeRef(kind="figure", index=1).label() == "F1"
    o = BriefOption(key="k", title="T", shape=Shape(tables=[TableSpec(title="t", row_unit="one row per x")]),
                    you_will_be_able_to=[Promise(text="x", supported_by=[ShapeRef(kind="table", index=1)])])
    assert o.version == 2 and o.output_shape.tables == ["t — one row per x"]
    assert Recommendation(option_key="k").because == ""
