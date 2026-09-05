"""Exact-ID coverage catches real saved critic handoff failures without repairing them."""
from types import SimpleNamespace

import pytest

from src.executor.ruling_coverage import critic_ruling_coverage


def row(rid, status=""):
    return SimpleNamespace(id=rid, status=status)


def test_all_28_renamed_ids_are_carried_not_explicitly_ruled():
    originals = [row(f"F{n}") for n in range(1, 29)]
    dimensions = [1] * 5 + [2] * 7 + [3] * 4 + [4] * 6 + [5] * 6
    decisions = [row(f"D{dimension}.F{n}", "confirmed") for n, dimension in enumerate(dimensions, 1)]
    decisions += [row("V.F1", "added")]
    result = critic_ruling_coverage(originals, decisions)
    assert result["original_count"] == 28 and result["explicitly_ruled_count"] == 0
    assert result["missing_or_unruled_ids"] == [r.id for r in originals]
    assert result["unexpected_nonadded_ids"] == [r.id for r in decisions[:-1]]
    assert not result["invalid_original_status_ids"] and not result["coverage_complete"]


def test_one_mistyped_id_is_not_inferred_from_similar_spelling():
    result = critic_ruling_coverage([row("D3.F1"), row("D3.F2")],
                                   [row("D3.F1", "confirmed"), row("D3.2", "confirmed")])
    assert result["explicitly_ruled_count"] == 1
    assert result["missing_or_unruled_ids"] == ["D3.F2"]
    assert result["unexpected_nonadded_ids"] == ["D3.2"]
    assert not result["coverage_complete"]


def test_legitimate_additions_do_not_count_as_original_rulings():
    result = critic_ruling_coverage([row("F1"), row("F2"), row("F3")],
        [row("F1", "confirmed"), row("F2", "weakened"), row("F3", "rejected"), row("V.F1", "added")])
    assert result["original_count"] == result["explicitly_ruled_count"] == 3
    assert result["coverage_complete"] and result["unexpected_nonadded_ids"] == []


@pytest.mark.parametrize("status", ["", "endorsed", "added", None])
def test_empty_or_invalid_original_status_is_not_a_ruling(status):
    result = critic_ruling_coverage([row("F1")], [row("F1", status)])
    assert result["explicitly_ruled_count"] == 0
    assert result["invalid_original_status_ids"] == result["missing_or_unruled_ids"] == ["F1"]
    assert not result["coverage_complete"]


def test_omitted_ruling_and_empty_original_ledger():
    omitted = critic_ruling_coverage([row("F1")], [])
    assert omitted["missing_or_unruled_ids"] == ["F1"]
    assert omitted["invalid_original_status_ids"] == []
    assert not omitted["coverage_complete"]
    empty = critic_ruling_coverage([], [row("V.F1", "added")])
    assert empty["original_count"] == empty["explicitly_ruled_count"] == 0
    assert not empty["coverage_complete"]


def test_rejecting_every_original_is_complete_coverage():
    result = critic_ruling_coverage((row(f"F{n}") for n in range(3)),
                                   (row(f"F{n}", "rejected") for n in range(3)))
    assert result["coverage_complete"] and result["explicitly_ruled_count"] == 3


def test_duplicate_original_ids_remain_ambiguous():
    result = critic_ruling_coverage([row("F1"), row("F1")], [row("F1", "confirmed")])
    assert result["original_count"] == 2 and result["explicitly_ruled_count"] == 0
    assert result["duplicate_original_ids"] == ["F1"]
    assert result["missing_or_unruled_ids"] == ["F1"]
    assert not result["coverage_complete"]


def test_conflicting_or_duplicate_rulings_are_never_chosen_arbitrarily():
    for second in ("confirmed", "rejected"):
        result = critic_ruling_coverage([row("F1")], [row("F1", "confirmed"), row("F1", second)])
        assert result["duplicate_ruling_ids"] == ["F1"]
        assert result["explicitly_ruled_count"] == 0 and not result["coverage_complete"]


def test_duplicate_addition_and_unexpected_status_are_diagnosed():
    result = critic_ruling_coverage([row("F1")],
        [row("F1", "confirmed"), row("V.F1", "added"), row("V.F1", "added"), row("V.F2", "")])
    assert result["explicitly_ruled_count"] == 1
    assert result["duplicate_ruling_ids"] == ["V.F1"]
    assert result["unexpected_nonadded_ids"] == ["V.F2"]
    assert not result["coverage_complete"]


def test_helper_does_not_modify_input_rows():
    originals, decisions = [row("F1")], [row("D1.F1", "weakened")]
    before = [vars(r).copy() for r in originals + decisions]
    critic_ruling_coverage(originals, decisions)
    assert before == [vars(r) for r in originals + decisions]


def test_checked_result_exposes_renamed_ids_without_guessing_or_retrying():
    from src.engines.registry import get_engine_registry
    from src.executor.process_runner import run_oneshot_checked
    from src.operationalizations.registry import get_operationalization_registry
    key = "conditions_of_possibility_analyzer"
    quote = "The account distinguishes an institutional premise from its independent support."
    calls = []
    def fake(system, user, *, model_hint, label, **kwargs):
        calls.append(label)
        if "| check" in label or "| verify" in label:
            content = ('## Findings ledger\n'
                       f'- [D1.F1] Renamed — anchor: "{quote}" — status: rejected\n'
                       f'- [V.F1] An addition — anchor: "{quote}" — status: added')
        else:
            content = f'# Reading\nOriginal prose [F1].\n\n## Findings ledger\n- [F1] Original — anchor: "{quote}"'
        return {"content": content, "model_used": model_hint}
    saved = []
    result = run_oneshot_checked(get_engine_registry().get_capability_definition(key),
        get_operationalization_registry().get(key).process, {"doc": quote}, call_fn=fake, on_call=saved.append)
    assert len(calls) == len(saved) == 2
    coverage = result.final_wall["check_ruling_coverage"]
    assert coverage == saved[-1].wall["check_ruling_coverage"]
    assert coverage["explicitly_ruled_count"] == 0 and coverage["missing_or_unruled_ids"] == ["F1"]
    assert coverage["unexpected_nonadded_ids"] == ["D1.F1"]
    assert result.final_wall["check_carried"] == 1 and result.final_wall["check_added"] == 1
    assert '- [F1] Original' in result.final_content and '- [F2] An addition' in result.final_content
    assert 'Check incomplete: 0 of 1' in result.final_content
    assert result.calls[-1].content.startswith('## Findings ledger\n- [D1.F1]')


@pytest.mark.parametrize("corpus", [False, True])
def test_deep_result_persists_per_document_and_corpus_ruling_coverage(corpus):
    import re
    from src.engines.registry import get_engine_registry
    from src.executor.ledger_walls import parse_rows, render_rows
    from src.executor.process_runner import run_process
    from src.operationalizations.registry import get_operationalization_registry
    key = "conditions_of_possibility_analyzer"
    spec = get_operationalization_registry().get(key).process.model_copy(deep=True)
    spec.dimensions = [next(d for d in spec.dimensions if d.scope == scope) for scope in ("document", "corpus")]
    docs = {"alpha": "The earlier account states its institutional premise with independent support."}
    if corpus:
        docs["beta"] = "The later account qualifies its institutional premise without discarding the support."
    pair = ' — '.join(f'{"anchor" if i == 0 else "anchor-b"}: "{quote}" — {"doc" if i == 0 else "doc-b"}: {dk}'
                      for i, (dk, quote) in enumerate(docs.items()))
    calls = []
    def fake(system, user, *, model_hint, label, **kwargs):
        calls.append(label)
        if "| extract |" in label:
            prefix = re.search(r"^- \[([^]]+)\.F1\]", system, re.M).group(1)
            if prefix == spec.dimensions[1].id_prefix:
                content = f'## Findings ledger\n- [{prefix}.F1] Relation — dim: {spec.dimensions[1].key} — {pair}'
            else:
                dk = re.search(r"SOURCE \[([^]]+)\]", user).group(1)
                content = f'## Findings ledger\n- [{prefix}.F1] Premise — dim: {spec.dimensions[0].key} — anchor: "{docs[dk]}" — doc: {dk}'
        elif "| verify" in label:
            rows = parse_rows(user.split("EXTRACTION LEDGERS:", 1)[1])
            # An exact valid ruling is covered; a valid quote with a changed ID is not.
            for r in rows:
                if len(r.anchors) > 1 or not corpus:
                    r.id = "Renamed." + r.id
                r.status = "confirmed"
            content = "## Findings ledger\n" + "\n".join(r.render() + " — status: confirmed" for r in rows)
        else:
            content = f'# Reading\nA premise [F1].\n\n## Findings ledger\n- [F1] Premise — anchor: "{docs["alpha"]}" — doc: alpha'
        return {"content": content, "model_used": model_hint}
    persisted = []
    result = run_process(get_engine_registry().get_capability_definition(key), spec, docs,
                         call_fn=fake, parallelism=1, reanchor=False, on_call=persisted.append)
    coverage = result.final_wall["check_ruling_coverage"]
    assert coverage == persisted[-1].wall["check_ruling_coverage"]
    assert not coverage["coverage_complete"]
    assert coverage["original_count"] == (3 if corpus else 1)
    assert coverage["explicitly_ruled_count"] == (2 if corpus else 0)
    assert len(coverage["reviews"]) == (3 if corpus else 1)
    assert len(calls) == (7 if corpus else 3)
    assert sum(len(r["unexpected_nonadded_ids"]) for r in coverage["reviews"]) == 1
