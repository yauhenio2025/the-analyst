"""Collect complete independent JSON failures for manual review, without repair.

The pinned one-brace collector supplies all receipt/source/model/usage checks,
the campaign lock, budget and review gate. Existing one-brace pending entries
remain identical. Other native JSONDecodeError responses receive a manual-review
entry with no proposed corrected content, hash or insertion offset. They remain
failed and excluded from scores. No adoption or paid retry is implemented.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COLLECTOR_PATH = ROOT / 'scripts/study_argument_family_collect_scores_2026_09_05.py'
COLLECTOR_SHA = '2e4a345e5a4e33e1e32d474382dcf70d39fc3f012cef11a6356afe9626560970'
MANUAL_RULE = 'manual_syntax_review_no_correction'


def load_collector():
    if hashlib.sha256(COLLECTOR_PATH.read_bytes()).hexdigest() != COLLECTOR_SHA:
        raise RuntimeError('One-brace collector changed')
    spec = importlib.util.spec_from_file_location('argument_pinned_score_collector', COLLECTOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def install_manual(collector):
    original_candidate = collector.candidate
    original_rule = collector.one_brace

    def candidate(first, h, job, record, plan, run, records, contexts, documents, rt):
        manual = False

        def rule(harness, raw):
            nonlocal manual
            try:
                return original_rule(harness, raw)
            except (json.JSONDecodeError, RuntimeError):
                # This hook is reached only after the original candidate has
                # checked the complete invocation and all original bindings.
                # Reproduce the native failure; schema errors remain fatal.
                try:
                    harness.parse_score(raw.decode('utf-8'))
                except json.JSONDecodeError as error:
                    manual = True
                    return raw, None, str(error)
                raise RuntimeError('Manual deferral requires native JSONDecodeError')

        previous = collector.one_brace
        collector.one_brace = rule
        try:
            entry = original_candidate(first, h, job, record, plan, run, records, contexts, documents, rt)
        finally:
            collector.one_brace = previous
        if manual:
            entry.update(rule=MANUAL_RULE, corrected_sha256=None, insert_byte=None,
                         manual_adapter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        return entry

    collector.candidate = candidate


def main(argv=None):
    collector = load_collector()
    install_manual(collector)
    return collector.main(list(sys.argv[1:] if argv is None else argv))


if __name__ == '__main__':
    raise SystemExit(main())
