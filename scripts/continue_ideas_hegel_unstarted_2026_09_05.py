"""Continue only unstarted planned generations, preserving the one reviewed parser failure.

This launcher does not repair, repeat, or mark the failed job complete. It uses the
unchanged frozen harness, shared campaign lock, receipts, and USD6 admission gate.
"""
import argparse
import fcntl
import importlib.util
from pathlib import Path

HARNESS_SHA256 = 'bf781c7202f3e6e22de624bfe9929cfd8402ce0bb2a5a55b8756754ed0190ac1'
IDENTITY = '43f051bdd4d890762145163d0e1d41c9be46aa19234f61456962ded883530d7e'
FAILED_KEY = 'argument_architecture__revised__ganzinger'
FAILED_ATTEMPT = 'c5620c0d97c1'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--budget-usd', type=float)
    args = parser.parse_args()
    path = Path(__file__).with_name('study_ideas_hegel_heldout_2026_09_05.py')
    spec = importlib.util.spec_from_file_location('heldout_original_harness', path)
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    h.require(h.digest(path.read_bytes()) == HARNESS_SHA256, 'Original harness changed')
    h.require(not args.run or args.budget_usd == 6, '--run requires --budget-usd 6')
    from dotenv import load_dotenv
    root = h.project_root()
    load_dotenv(root / '.env', override=False)
    output_root = root / 'data/study/ideas_hegel_heldout_2026_09_05'
    sources = root / 'data/study/sources_ideas'
    with h.frozen_runtime() as rt:
        plan, contexts, docs = h.build_plan(rt, sources, root / 'data/study/ideas_2026_09_05/374325c24e6b10a1')
        h.require(plan['identity'] == IDENTITY, 'Original study identity changed')
        folder = output_root / IDENTITY[:16]
        with (output_root / 'heldout.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            h.require(h.read_json(folder / 'plan.json') == plan, 'Saved plan changed')
            records = h.read_json(folder / 'results.json')
            failed = records[FAILED_KEY]
            h.require(failed['status'] == 'failed' and failed['attempt'] == FAILED_ATTEMPT
                and failed['error'] == 'Ledger row I4 has repeated anchor fields; use distinct anchor/doc suffixes', 'Reviewed failure differs')
            unstarted = []
            for job in plan['generations']:
                if job['key'] == FAILED_KEY:
                    continue
                record = records.get(job['key'])
                if record:
                    h.validate_completed(job, record, plan, folder, records, contexts, docs, rt)
                else:
                    h.require(not list(output_root.glob(f"*/receipts/{job['key']}/*/call-[0-9][0-9][0-9][0-9].json")), 'Unrecorded invocation exists')
                    unstarted.append(job)
            amendment = {'study_identity': IDENTITY, 'harness_sha256': HARNESS_SHA256,
                'launcher_sha256': h.digest(Path(__file__).read_bytes()), 'excluded_failure': FAILED_KEY,
                'failed_record_sha256': h.digest(failed), 'planned_unstarted_jobs': [j['key'] for j in unstarted],
                'policy': 'Continue untouched remaining matrix jobs. Preserve failed attempt and all invocation costs. No repair, retry, or change to prompts/runtime/judging.',
                'budget_usd': 6}
            print(amendment, flush=True)
            if not args.run:
                return
            amendment_path = folder / 'amendments/continue_unstarted.json'
            h.require(not amendment_path.exists(), 'Continuation already recorded; inspect before any further continuation')
            h.write_json(amendment_path, amendment)
            try:
                for job in unstarted:
                    print('generate: ' + job['key'], flush=True)
                    h.execute_job(job, plan, folder, records, contexts, docs, sources, output_root, args.budget_usd, rt)
            finally:
                h.write_json(folder / 'report.json', h.report(plan, folder, contexts, docs, rt))


if __name__ == '__main__':
    main()
