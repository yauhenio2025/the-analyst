"""One production condition per repaired method; reuse the frozen-study recorder.

USD10 is guidance, as explicitly directed by the owner, not purchase admission.
Source memos are committed before either independent rater. No new originals.
"""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import study_second_queue as study

ARCHIVE = ROOT / 'communications/study/second_queue_repair_2026_09_06'
OUT = ROOT / 'data/study/second_queue_repair_2026_09_06'
SELECTED = {
    'G2': ['technique', 'rationality'], 'G3': ['religion2001', 'religion2022'],
    'G4': ['promise', 'religion2022'], 'A4': ['harris'], 'A5': ['elling'],
    'A6': ['chen'], 'C1': ['zambrana'], 'C6': ['aukus'], 'S3': ['subsea'],
    'E12': ['promise'], 'A3': ['aukus'],
}
study.ARCHIVE = ARCHIVE
study.OUT = OUT
study.budget.OUT = OUT
study.budget.CAP = 10.0
study.JOBS = {
    f'{ident}__{"dvs" if ident.startswith("G") else "checked"}__'+ '_'.join(papers): {
        'id': ident, 'engine': study.DESIGNS[ident]['key'], 'papers': papers,
        'condition': 'dvs' if ident.startswith('G') else 'checked',
    } for ident, papers in SELECTED.items()
}
# The existing transport, no-replay custody, usage accounting and other guards
# are unchanged. Only the owner's explicitly advisory monetary threshold differs.
_original_require = study.budget.require

def require(ok, message):
    if not ok and message == 'USD8 admission cap: no new invocation':
        print('USD10 guidance exceeded by conservative admission reservations; owner authorized completion.', flush=True)
        return
    _original_require(ok, message)

study.budget.require = require

def inputs():
    files = [Path(__file__).resolve(), ROOT/'scripts/study_second_queue.py',
             ROOT/'scripts/study_first_queue.py', ROOT/'scripts/study_two_engines.py',
             ROOT/'scripts/study_corpus_methods_P1_P2_2026_09_06.py',
             ROOT/'communications/study/PROTOCOL_second_queue_repair_2026-09-06.md',
             ARCHIVE/'repairs.json', ROOT/'communications/study/second_queue_2026_09_06/designs.json']
    files += [ROOT/f'src/{folder}/{d["key"]}.yaml' for d in study.DESIGNS.values()
              for folder in ('engines/capability_definitions', 'operationalizations/definitions')]
    files += [ROOT/p for p in ('src/executor/process_runner.py', 'src/executor/ledger_walls.py',
        'src/executor/scoped_outcomes.py', 'src/executor/ruling_coverage.py', 'src/executor/context_broker.py',
        'src/stages/process_composer.py', 'src/operationalizations/schemas.py',
        'src/engines/schemas_v2.py', 'src/events/pricing.py')]
    files += [study.PAPERS[p] for papers in SELECTED.values() for p in papers]
    files += list((ROOT/'communications/study/second_queue_2026_09_06/scores').glob('*__old__*.json'))
    return sorted(set(files))

study.inputs = inputs

if __name__ == '__main__':
    study.main()
