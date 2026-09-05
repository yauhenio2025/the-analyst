"""Five-output P1/P2 revalidation, with a fresh owner-authorized USD8 cap.

Reuse the first study's no-retry provider recorder, frozen rubric and process calls.
The first campaign and its unresolved charge remain separate, intact artifacts.
All five source-read memos must be committed before either independent judge runs.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import fcntl
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import study_corpus_methods_P1_P2_2026_09_06 as study

ARCHIVE = ROOT / 'communications/study/corpus_methods_P1_P2_revalidation_2026_09_06'
study.OUT = ROOT / 'data/study/corpus_methods_P1_P2_revalidation_2026_09_06'
study.JOBS = {k: v for k, v in study.JOBS.items() if k != 'P2__deep__castoriadis'}
# Preserve the first campaign's explicit transport correction: DeepSeek's token
# cap includes reasoning. This is frozen before any revalidation invocation.
study.LIMITS['mid'] = 32000
_input_paths = study.input_paths
_guard = study.guard


def input_paths():
    return sorted(set(_input_paths() + [
        Path(__file__).relative_to(ROOT),
        Path('scripts/audit_corpus_methods_P1_P2_2026_09_06.py'),
        Path('communications/study/PROTOCOL_corpus_methods_P1_P2_revalidation_2026-09-06.md'),
    ]))


def guard(plan):
    _guard(plan)
    for field, value in [('models', study.MODELS), ('prices', study.PRICES),
                         ('output_limits', study.LIMITS), ('rubric', study.RUBRIC), ('tasks', study.TASKS)]:
        study.require(study.digest(plan[field]) == study.digest(value), f'Frozen campaign setting changed: {field}')


def memo_binding(key, plan):
    path = study.OUT / 'outputs' / f'{key}.md'
    result = study.read(study.OUT / 'results' / f'{key}.json')
    study.require(result['status'] == 'complete', 'No completed output')
    sha = study.digest(path.read_bytes())
    study.require(sha == result['output_sha256'], 'Output changed')
    memo = ARCHIVE / f'{key}.md'
    study.require(memo.exists() and sha in memo.read_text() and len(memo.read_text()) > 800,
                  'Substantive source-read memo must bind the exact output before scoring')
    relative = str(memo.relative_to(ROOT))
    committed = subprocess.check_output(['git', 'show', f'HEAD:{relative}'], cwd=ROOT)
    study.require(committed == memo.read_bytes(), 'Source-read memo must be committed before scoring')
    return {'output_sha256': sha, 'memo_sha256': study.digest(committed), 'memo_path': relative}


study.input_paths = input_paths
study.guard = guard
study.memo_binding = memo_binding


def audit():
    # The old auditor imports the same configured module. Use the production
    # citation parser, now supporting lists/ranges without splitting dotted IDs.
    from scripts import audit_corpus_methods_P1_P2_2026_09_06 as auditor
    from src.executor.ledger_walls import cited_ids
    auditor.expanded_final_citations = lambda text: {i for i in cited_ids(text) if i.startswith('F')}
    auditor.audit()


def export():
    """Copy reviewable artifacts, excluding full source/prompt bytes and credentials."""
    import shutil
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for name in ('plan.json', 'audit.json', 'all_memos_before_scores.json'):
        src = study.OUT / name
        if src.exists(): shutil.copy2(src, ARCHIVE / name)
    for folder in ('outputs', 'desk_ledgers', 'results', 'scores', 'judge_inputs'):
        src = study.OUT / folder
        if src.exists(): shutil.copytree(src, ARCHIVE / folder, dirs_exist_ok=True)
    calls = []
    for path in sorted((study.OUT / 'calls').glob('*/*.json')):
        if '.prompt.' in path.name: continue
        calls.append({'path': str(path.relative_to(study.OUT)), **study.read(path)})
    study.write(ARCHIVE / 'calls.json', {'costs': study.costs(), 'calls': calls})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--freeze', action='store_true')
    action.add_argument('--generate', nargs='+', choices=study.JOBS)
    action.add_argument('--score-all', action='store_true')
    action.add_argument('--audit', action='store_true')
    action.add_argument('--export', action='store_true')
    action.add_argument('--status', action='store_true')
    parser.add_argument('--workers', type=int, choices=(1, 2, 3), default=2)
    args = parser.parse_args()
    if args.freeze:
        study.freeze()
        export()
        return
    plan = study.read(study.OUT / 'plan.json')
    guard(plan)
    if args.status:
        print(json.dumps(study.costs(), indent=2))
        return
    if args.audit:
        audit()
        export()
        return
    if args.export:
        export()
        return
    from dotenv import load_dotenv
    load_dotenv(ROOT / '.env', override=False)
    with (study.OUT / 'campaign.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.score_all:
            bindings = {key: memo_binding(key, plan) for key in study.JOBS}
            binding_path = study.OUT / 'all_memos_before_scores.json'
            if binding_path.exists():
                study.require(study.read(binding_path)['bindings'] == bindings, 'Pre-score memos changed')
            else:
                study.write(binding_path, {'bindings': bindings,
                    'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                    'prepared_at': study.time.time()})
            jobs = [(key, rater) for key in study.JOBS for rater in ('sonnet', 'sol')
                    if not (study.OUT / 'scores' / f'{key}__{rater}.json').exists()]
            run = lambda item: study.judge(*item, plan)
        else:
            jobs = args.generate
            run = lambda key: study.generate(key, plan)
        errors = []
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(run, key): key for key in jobs}
            for future in as_completed(futures):
                key = futures[future]
                try: future.result()
                except Exception as exc:
                    errors.append({'job': key, 'error': str(exc)})
                    print(key, 'FAILED', str(exc), flush=True)
        export()
        print(json.dumps({'costs': study.costs(), 'errors': errors}), flush=True)
        if errors: raise SystemExit(1)


if __name__ == '__main__':
    main()
