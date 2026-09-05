"""Offline corpus regressions: ids and every declared quote/document pair survive the chain."""
import re

import pytest

from src.dossier.common import analysis_ledger
from src.dossier.schemas import DossierJob
from src.engines.registry import get_engine_registry
from src.executor.ledger_walls import SourceIndex, check_citations, parse_rows, render_rows, verify_rows
from src.executor.process_runner import apply_rulings, run_process
from src.operationalizations.registry import get_operationalization_registry
from src.sources.schemas import Document
from src.stages.process_composer import compose_extract_prompt, compose_verify_prompt


DOCS = {
    "early-2001": "The social imaginary establishes the first shared premise of this position.",
    "middle-2001": "The institutional account adopts the inherited premise without a fresh argument.",
    "late-2022": "The final account revises the inherited premise through an explicit qualification.",
}
QUOTES = list(DOCS.values())
PAIR = (f'anchor: "{QUOTES[0]}" — doc: early-2001 — '
        f'anchor-b: "{QUOTES[1]}" — doc-b: middle-2001')


def test_every_anchor_is_verified_in_its_named_document_and_rendered_again():
    text = f'- [P6.F1] Continuity — dim: path_dependence — {PAIR} — confidence: high'
    row = parse_rows(text)[0]
    report = verify_rows([row], SourceIndex(DOCS), require_cross_document=True)
    assert report.verified == 1 and report.verified_anchors == 2 and report.cross_document_rows == 1
    assert [(a.quote, a.doc, a.verified_doc) for a in row.anchors] == [
        (QUOTES[0], "early-2001", "early-2001"), (QUOTES[1], "middle-2001", "middle-2001")]
    assert verify_rows(parse_rows(row.render()), SourceIndex(DOCS), require_cross_document=True).verified == 1
    # A second quote that exists elsewhere in the corpus does not verify under the wrong key.
    bad = parse_rows(text.replace("doc-b: middle-2001", "doc-b: late-2022"))
    assert verify_rows(bad, SourceIndex(DOCS), require_cross_document=True).failed_ids == ["P6.F1"]
    assert not bad[0].anchor_verified and bad[0].extra_anchors[0].verified_doc == ""
    # Re-verification must clear an earlier successful result.
    row.extra_anchors[0].quote = "This second quote occurs in no source whatsoever."
    assert verify_rows([row], SourceIndex(DOCS)).failed_ids == ["P6.F1"]
    assert not row.anchor_verified
    assert SourceIndex(DOCS).find(QUOTES[0], "missing-key") is None


@pytest.mark.parametrize("pair", [
    f'anchor: "{QUOTES[0]}" — doc: early-2001',
    f'anchor: "{QUOTES[0]}" — doc: early-2001 — anchor-b: "{QUOTES[1]}"',
    f'anchor: "{QUOTES[0]}" — doc: early-2001 — doc-b: middle-2001',
    f'anchor: "{QUOTES[0]}" — doc: early-2001 — anchor-b: "{QUOTES[0]}" — doc-b: early-2001',
])
def test_corpus_rows_require_two_quotes_with_distinct_document_keys(pair):
    rows = parse_rows(f'- [X6.F1] Shared score — dim: shared_score — {pair}')
    rep = verify_rows(rows, SourceIndex(DOCS), corpus_dimensions={"shared_score"})
    assert rep.verified == 0 and rep.failed_ids == ["X6.F1"]


def test_third_anchor_and_bracketed_keys_are_checked_and_quote_delimiters_survive():
    row = parse_rows(f'- [P6.F1] Three texts — {PAIR} — anchor-c: "{QUOTES[2]}" — doc-c: [late-2022]')[0]
    assert verify_rows([row], SourceIndex(DOCS), require_cross_document=True).verified_anchors == 3
    row.extra_anchors[1].doc = "missing-key"
    assert verify_rows([row], SourceIndex(DOCS)).verified == 0
    source = 'The text calls this a "shared premise" before qualifying the position.'
    quoted = parse_rows(f'- [F1] Quoted phrase — anchor: “{source}” — doc: [early-2001]')[0]
    assert quoted.doc == "early-2001"
    assert verify_rows([quoted], SourceIndex({"early-2001": source})).verified == 1
    assert parse_rows(quoted.render())[0].anchor == source


def test_two_anchors_within_one_document_inherit_its_key_and_trimmed_quotes_roundtrip():
    source = " ".join(QUOTES[:2])
    rows = parse_rows(f'- [I3.F1] Incompatibility — anchor: "{QUOTES[0]}" — doc: early-2001 '
                      f'— anchor-b: "{QUOTES[1]} invented ending absent from the source"')
    rep = verify_rows(rows, SourceIndex({"early-2001": source}))
    assert rep.verified == 1 and rep.trimmed == 1
    assert rows[0].extra_anchors[0].doc == "early-2001"
    assert "invented ending" not in rows[0].render()
    assert verify_rows(parse_rows(rows[0].render()), SourceIndex({"early-2001": source})).verified == 1


def _engine(key):
    cap = get_engine_registry().get_capability_definition(key)
    spec = get_operationalization_registry().get(key).process.model_copy(deep=True)
    # Keep the real corpus dimension/method and chain, with one document dimension for a bounded fixture.
    spec.dimensions = [next(d for d in spec.dimensions if d.scope == "document"),
                       next(d for d in spec.dimensions if d.scope == "corpus")]
    return cap, spec


@pytest.mark.parametrize("key", ["conditions_of_possibility_analyzer", "inferential_commitment_mapper"])
def test_corpus_prompts_have_unique_ids_and_explicit_two_anchor_shape(key):
    cap, spec = _engine(key)
    prefixes, additions = [], []
    for doc_key in DOCS:
        prompt = compose_extract_prompt(cap, spec, spec.steps[0], spec.dimensions[0], DOCS, doc_key=doc_key)
        prefixes.append(prompt.id_prefix)
        assert f'[{prompt.id_prefix}.F1]' in prompt.system and f'[{prompt.id_prefix}.F<n>]' in prompt.system
        critic = compose_verify_prompt(cap, spec, spec.steps[1], DOCS, "", doc_key=doc_key)
        additions.append(critic.id_prefix)
        assert spec.dimensions[1].questions[0] not in critic.system
    assert len(set(prefixes)) == len(set(additions)) == len(DOCS)
    corpus = compose_extract_prompt(cap, spec, spec.steps[0], spec.dimensions[1], DOCS, prior_ledgers="ledger")
    output_row = next(line for line in corpus.system.splitlines() if line.startswith("- ["))
    assert "anchor-b:" in output_row and "doc-b:" in output_row
    assert check_citations("Missing [D1.DOC2.F9].", {"D1.DOC1.F9"}) == ["D1.DOC2.F9"]


@pytest.mark.parametrize("key", ["conditions_of_possibility_analyzer", "inferential_commitment_mapper"])
def test_deep_corpus_chain_reanchors_both_pairs_and_preserves_them_for_desks(key):
    cap, spec = _engine(key)
    corpus_dim = spec.dimensions[1]
    synthesis_inputs = []

    def fake(system, user, *, model_hint, label, **_):
        if "| extract |" in label:
            prefix = re.search(r"^- \[([^]]+)\.F1\]", system, re.M).group(1)
            if f"| {corpus_dim.key}" in label:
                if "re-anchor" in label:
                    assert "anchor-b:" in user and "doc-b:" in user
                    content = f'## Findings ledger\n- [{prefix}.F1] Across the texts — dim: {corpus_dim.key} — {PAIR}'
                else:
                    content = (f'## Findings ledger\n- [{prefix}.F1] Across the texts — dim: {corpus_dim.key} — '
                               f'anchor: "{QUOTES[0]}" — doc: early-2001 — anchor-b: "An absent second quote." — doc-b: middle-2001'
                               f'\n- [{prefix}.F2] Missing pair — dim: {corpus_dim.key} — anchor: "{QUOTES[0]}" — doc: early-2001')
            else:
                doc_key = re.search(r"SOURCE \[([^]]+)\]", user).group(1)
                content = f'## Findings ledger\n- [{prefix}.F1] In this text — dim: {spec.dimensions[0].key} — anchor: "{DOCS[doc_key]}"'
        elif "| verify" in label:
            rows = parse_rows(user.split("EXTRACTION LEDGERS:", 1)[1])
            content = render_rows(rows) + "\n"
            # Preserve the corpus row and add one uniquely named miss per document.
            if len(rows[0].anchors) == 1:
                doc_key = re.search(r"SOURCE \[([^]]+)\]", user).group(1)
                prefix = re.search(r"^- \[(V[^]]+)\.F1\]", system, re.M).group(1)
                content += f'- [{prefix}.F1] A miss — anchor: "{DOCS[doc_key]}" — doc: {doc_key} — status: added'
        else:
            synthesis_inputs.append(user)
            rows = parse_rows(user.split("VERIFIED FINDINGS LEDGER:", 1)[1])
            assert len({r.id for r in rows}) == len(rows)
            corpus_row = next(r for r in rows if len(r.anchors) == 2)
            content = f'# Reading\nThe position changes [F1].\n\n## Findings ledger\n- [F1] Across the texts — dim: {corpus_dim.key} — {PAIR} — from: {corpus_row.id}'
        return {"content": content, "model_used": model_hint, "input_tokens": 1, "output_tokens": 1}

    result = run_process(cap, spec, DOCS, depth="deep", call_fn=fake, parallelism=1)
    corpus_call = next(c for c in result.calls if c.dimension_key == corpus_dim.key)
    assert corpus_call.reanchored == 1 and corpus_call.dropped_ids == [f"{corpus_dim.id_prefix}.F2"]
    assert corpus_call.wall["after_reanchor"]["verified_anchors"] == 2
    assert result.final_wall["verified_anchors"] == 2 and result.final_wall["failed_ids"] == []
    assert result.final_wall["duplicate_ids"] == [] and result.final_wall["missing_lineage"] == []
    assert "anchor-b:" in synthesis_inputs[0] and "doc-b: middle-2001" in synthesis_inputs[0]
    job = DossierJob()
    job.analysis = {"1.0": {"engine_key": key, "final_output": result.final_content}}
    desk = analysis_ledger(job, [Document(key=k, title=k, text=v) for k, v in DOCS.items()])
    assert f'anchor [early-2001]: "{QUOTES[0]}"' in desk
    assert f'anchor [middle-2001]: "{QUOTES[1]}"' in desk


def test_duplicate_ids_from_different_documents_stop_before_an_ambiguous_handoff():
    cap, spec = _engine("conditions_of_possibility_analyzer")
    def fake(system, user, *, model_hint, label, **_):
        assert "| extract |" in label
        doc_key = re.search(r"SOURCE \[([^]]+)\]", user).group(1)
        return {"content": f'## Findings ledger\n- [D1.F1] Ignored namespace — anchor: "{DOCS[doc_key]}"',
                "model_used": model_hint}
    with pytest.raises(RuntimeError, match="duplicate ledger ids: D1.F1"):
        run_process(cap, spec, DOCS, call_fn=fake, reanchor=False, parallelism=1)


def test_final_lineage_and_critic_rulings_cannot_lose_the_second_anchor():
    index = SourceIndex(DOCS)
    original = parse_rows(f'- [F1] Cross-document — dim: path_dependence — {PAIR}')
    verify_rows(original, index, corpus_dimensions={"path_dependence"})
    final = parse_rows(f'- [F2] Lost pair — anchor: "{QUOTES[0]}" — doc: early-2001 — from: F1')
    assert verify_rows(final, index, corpus_ids={"F1"}).failed_ids == ["F2"]
    weakened = parse_rows(f'- [F1] Narrower relation — {PAIR} — status: weakened')
    kept, _, unverified, _ = apply_rulings(original, weakened, index)
    assert len(kept[0].anchors) == 2 and unverified == []
    assert "anchor-b:" in kept[0].render()
    dropped_pair = parse_rows(f'- [F1] Lost pair — anchor: "{QUOTES[0]}" — doc: early-2001 — status: weakened')
    kept, _, unverified, _ = apply_rulings(kept, dropped_pair, index)
    assert unverified == kept and not kept[0].anchor_verified


def test_desks_do_not_reclassify_a_corpus_row_without_its_second_pair_as_citable():
    job = DossierJob()
    job.analysis = {"1.0": {"engine_key": "conditions_of_possibility_analyzer", "final_output":
        f'## Findings ledger\n- [F1] Lost pair — dim: path_dependence — anchor: "{QUOTES[0]}" — doc: early-2001'}}
    out = analysis_ledger(job, [Document(key=k, title=k, text=v) for k, v in DOCS.items()])
    assert "no row with a verified anchor" in out
    assert out.index("unverified or incomplete") < out.index("- [F1]")
