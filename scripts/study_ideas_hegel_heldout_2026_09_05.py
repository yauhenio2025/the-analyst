"""One held-out operationalization comparison; preview by default, never automatic paid retries.

Both conditions use frozen d9cfc6e runtime/composer/capabilities and oneshot_checked.
Only the process definition changes: 11beb77 production versus d9cfc6e revision.
--run --phase generate creates 16 checked readings; a separate --phase judge creates
16 counterbalanced judgments. The fresh study has its own USD6 admission ceiling.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
import fcntl
import hashlib
import io
import json
import math
import os
import re
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import time
from types import SimpleNamespace
import uuid

REPO = Path(__file__).resolve().parents[1]
RUNTIME = 'd9cfc6e4569d237a30174446f5c6a25e31f05f98'
PREVIOUS = '11beb77be8de7544be019237f512a56d9b5cd30a'
ORIGINAL_RUNTIME = 'c19513884a5453f54073e38cbabf2c6e7d5cfd28'
ENGINES = ('conditions_of_possibility_analyzer', 'argument_architecture', 'inferential_commitment_mapper', 'epistemological_method_detector')
SOURCES = {'ganzinger': 'hegels_concept_of_the_concept_2026.txt', 'elling': 'elling2025_amphibian_habits_hegel_second_nature.txt'}
CONDITIONS = {'previous': PREVIOUS, 'revised': RUNTIME}
MODELS = {'read': 'openrouter/openai/gpt-5.6-sol', 'critic': 'openrouter/deepseek/deepseek-v4-pro', 'judge': 'claude-sonnet-4-6'}
CAP_USD = 6.0


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def project_root():
    return Path(git('rev-parse', '--path-format=absolute', '--git-common-dir').decode().strip()).parent


def read_json(path, default=None):
    return json.loads(path.read_bytes()) if path.exists() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    tmp.replace(path)


@contextmanager
def frozen_runtime():
    archive = git('archive', RUNTIME, 'src', 'scripts')
    with tempfile.TemporaryDirectory(prefix='hegel-heldout-frozen-') as temporary:
        frozen = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(frozen, filter='data')
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(frozen))
        from scripts import study_ideas_material as core
        from scripts import summarize_ideas_study_2026_09_05 as sums
        from src.executor import process_runner as pr, ledger_walls as lw
        from src.stages import process_composer as composer
        from src.operationalizations.schemas import EngineOperationalization
        import yaml
        require(Path(pr.__file__).is_relative_to(frozen), 'Runtime was already imported outside the frozen archive; use a fresh interpreter')
        yield SimpleNamespace(core=core, sums=sums, pr=pr, lw=lw, composer=composer,
                              schema=EngineOperationalization, yaml=yaml, archive_sha256=digest(archive))


def matrix():
    generations = [{'key': f'{e}__{c}__{p}', 'engine': e, 'condition': c, 'source': p, 'kind': 'generation'}
                   for e in ENGINES for p in SOURCES for c in CONDITIONS]
    judges = [{'key': f'judge__{e}__{p}__{a}_first', 'engine': e, 'source': p, 'kind': 'judge', 'order': a + '_first',
               'A': f'{e}__{a}__{p}', 'B': f'{e}__{b}__{p}'}
              for e in ENGINES for p in SOURCES for a, b in [('previous', 'revised'), ('revised', 'previous')]]
    return generations, judges


def calibration(directory):
    """Receipt-derived budget envelope only; no prior analysis enters a model prompt."""
    groups = {r: [] for r in MODELS}
    pins = {}
    for path in sorted(directory.glob('receipts/*/*/call-[0-9][0-9][0-9][0-9].json')):
        if '__deep__' in path.parents[1].name:
            continue
        receipt = read_json(path)
        require(receipt['status'] == 'complete' and receipt.get('cost_usd') is not None, 'Calibration contains incomplete/uncosted calls')
        prompt_path = path.with_name(path.stem + '.prompt.json')
        prompt = read_json(prompt_path)
        require(digest(prompt) == receipt['prompt_sha256'], 'Calibration prompt mismatch')
        role = 'judge' if path.parents[1].name.startswith('judge__') else 'critic' if ' | verify' in receipt['label'] else 'read'
        response = path.with_suffix('.md').read_bytes()
        require(digest(response) == receipt['output_sha256'], 'Calibration response mismatch')
        groups[role].append((receipt['input_tokens'] / (len(prompt['system']) + len(prompt['user'])), receipt['output_tokens'], len(response.decode())))
        for p in (path, prompt_path, path.with_suffix('.md')):
            pins[str(p.relative_to(directory))] = digest(p.read_bytes())
    require({r: len(v) for r, v in groups.items()} == {'read': 24, 'critic': 12, 'judge': 24}, 'Expected the completed original baseline calibration')
    pins['results.json'] = digest((directory / 'results.json').read_bytes())
    records = read_json(directory / 'results.json')
    finals = []
    for key, record in records.items():
        if key.startswith('judge__') or '__deep__' in key:
            continue
        raw = (directory / record['output']).read_bytes()
        require(record['status'] == 'complete' and digest(raw) == record['output_sha256'], 'Calibration final invalid')
        pins[record['output']] = digest(raw)
        finals.append(len(raw.decode()))
    return {'method': 'Per-role maximum observed input tokens/character multiplied by 1.10 and maximum output tokens multiplied by 1.25; source and prompt sizes are actual held-out sizes. This is an admission estimate, not a billing guarantee.',
            'roles': {r: {'calls': len(v), 'input_tokens_per_char': max(x[0] for x in v) * 1.10,
                           'output_tokens_envelope': math.ceil(max(x[1] for x in v) * 1.25),
                           'maximum_response_chars': max(x[2] for x in v)} for r, v in groups.items()},
            'maximum_checked_final_chars': max(finals), 'input_hashes': pins}


def estimate(rt, calibration_data, role, chars):
    envelope = calibration_data['roles'][role]
    return rt.core.estimate_cost(MODELS[role], math.ceil(chars * envelope['input_tokens_per_char']), envelope['output_tokens_envelope'])


def build_plan(rt, source_dir, calibration_dir):
    docs, sources = {}, {}
    for paper, filename in SOURCES.items():
        raw = (source_dir / filename).read_bytes()
        text = raw.decode('utf-8')
        require(bool(text.strip()), f'Empty source: {filename}')
        docs[paper] = {Path(filename).stem: text}
        sources[paper] = {'file': filename, 'sha256': digest(raw), 'bytes': len(raw), 'chars': len(text)}
    cal = calibration(calibration_dir)
    definitions, contexts = {}, {}
    generations, judges = matrix()
    for engine in ENGINES:
        cap = rt.core.get_engine_registry().get_capability_definition(engine)
        definitions[engine] = {'capability': cap.model_dump(mode='json'), 'conditions': {}}
        for condition, commit in CONDITIONS.items():
            filename = f'src/operationalizations/definitions/{engine}.yaml'
            raw = git('show', f'{commit}:{filename}')
            if condition == 'previous':
                require(raw == git('show', f'{ORIGINAL_RUNTIME}:{filename}'), '11beb77 production definition differs from original baseline')
            op = rt.schema.model_validate(rt.yaml.safe_load(raw))
            require(op.process is not None, 'Operationalization has no process')
            definitions[engine]['conditions'][condition] = {'commit': commit, 'file': filename, 'sha256': digest(raw), 'process': op.process.model_dump(mode='json')}
            for paper in SOURCES:
                key = f'{engine}__{condition}__{paper}'
                prompt = rt.composer.compose_oneshot_prompt(cap, op.process, docs[paper])
                contexts[key] = {'cap': cap, 'spec': op.process, 'documents': docs[paper], 'read_prompt': {'system': prompt.system, 'user': prompt.user}}
    for job in generations:
        context = contexts[job['key']]
        prompt = context['read_prompt']
        spec = context['spec']
        sample = rt.composer.compose_verify_prompt(context['cap'], spec, spec.get_step('verify'), context['documents'],
                    rt.composer.LEDGER_HEADING + '\n' + 'x' * cal['roles']['read']['maximum_response_chars'])
        job.update(read_prompt_sha256=digest(prompt), read_prompt_chars=sum(map(len, prompt.values())),
                   read_estimate_usd=estimate(rt, cal, 'read', sum(map(len, prompt.values()))),
                   critic_estimate_usd=estimate(rt, cal, 'critic', len(sample.system) + len(sample.user)))
    for job in judges:
        source = '\n\n'.join(f'SOURCE [{k}]:\n\n{v}' for k, v in docs[job['source']].items())
        chars = len(rt.core.PAIR) + len(source) + 2 * cal['maximum_checked_final_chars'] + 80
        job['estimate_usd'] = estimate(rt, cal, 'judge', chars)
    payload = {'study': 'ideas_hegel_heldout_2026_09_05', 'version': 1, 'runtime_commit': RUNTIME,
               'runtime_archive_sha256': rt.archive_sha256, 'harness_sha256': digest(Path(__file__).read_bytes()),
               'conditions': CONDITIONS, 'sources': sources, 'definitions': definitions, 'models': MODELS,
               'shared_anchoring_law_sha256': digest(rt.composer.ANCHORING_LAW.encode()), 'shared_judge_prompt_sha256': digest(rt.core.PAIR.encode()),
               'transport_environment': {key: os.environ.get(key, default) for key, default in {'ENABLE_STREAMING': '', 'LLM_SYNC_HARD_TIMEOUT_SECONDS': '480', 'ANTHROPIC_EXTRACTION_READ_TIMEOUT_S': '180'}.items()},
               'execution': 'Both conditions use oneshot_checked, standard depth, same current runtime/composer/check and JSON-anchor contract; only process definitions differ.',
               'generations': generations, 'judgments': judges, 'planned_invocations': {'read': 16, 'critic': 16, 'judge': 16},
               'calibration': cal, 'estimated_cost_by_role': {'read': round(sum(j['read_estimate_usd'] for j in generations), 6),
                    'critic': round(sum(j['critic_estimate_usd'] for j in generations), 6), 'judge': round(sum(j['estimate_usd'] for j in judges), 6)},
               'approved_new_study_cap_usd': CAP_USD, 'pricing': {r: rt.core.PRICING[m.split('/')[-1]] for r, m in MODELS.items()}}
    payload = json.loads(json.dumps(payload))  # Stable in-memory/on-disk equality, including price tuples.
    return {'identity': digest(payload), **payload}, contexts, docs


def quote_diagnostics(content, rt, documents):
    """Canonical JSON is separate from legacy parsing and source matching."""
    stats = Counter(rows=0, supported_quote_fields=0, canonical_json=0, legacy_quoted=0, malformed=0, rows_without_quote_field=0)
    examples = []
    for line in rt.pr._ledger_text(content).splitlines():
        match = rt.lw._ROW_RE.match(line)
        if not match:
            continue
        stats['rows'] += 1
        fields = [(name, value) for name, value, _ in rt.lw._field_values(match[2])
                  if name in ('anchor', 'counter-anchor', 'revised-finding', 'finding rewritten to') or re.fullmatch(r'anchor-[a-z0-9]+', name)]
        if not fields:
            stats['rows_without_quote_field'] += 1
        for name, value in fields:
            stats['supported_quote_fields'] += 1
            try:
                decoded, end = json.JSONDecoder().raw_decode(value)
                canonical = value.startswith('"') and isinstance(decoded, str) and bool(decoded.strip()) and bool(rt.lw._ANCHOR_TRAILER_RE.fullmatch(value[end:]))
            except (ValueError, TypeError):
                canonical = False
            if canonical:
                stats['canonical_json'] += 1
            else:
                quoted, _, error = rt.lw._anchor_literal(value)
                category = 'legacy_quoted' if quoted and not error else 'malformed'
                stats[category] += 1
                examples.append({'id': match[1], 'field': name, 'category': category})
    membership = {}
    try:
        rows = rt.lw.parse_rows(rt.pr._ledger_text(content))
        membership = rt.lw.verify_rows(rows, rt.lw.SourceIndex(documents)).as_dict()
        membership['parseable_rows'] = len(rows)
    except Exception as exc:
        membership = {'parse_error_type': type(exc).__name__, 'parse_error': str(exc)}
    return {'raw_membership_wall': membership, 'scope': 'Tokenized supported quote/rewrite fields in raw call ledger view, before application/rendering; canonical JSON compliance is not matching or semantic accuracy.', **stats, 'noncanonical_fields': examples}


def receipt_paths(output_root):
    return sorted(output_root.glob('*/receipts/*/*/call-[0-9][0-9][0-9][0-9].json'))


def budget_guard(output_root, cap, next_estimate):
    require(0 < cap <= CAP_USD, 'Fresh-study budget must be positive and at most USD6')
    receipts = [read_json(p) for p in receipt_paths(output_root)]
    require(all(isinstance(r.get('cost_usd'), (int, float)) and math.isfinite(r['cost_usd']) and r['cost_usd'] >= 0 for r in receipts), 'Unknown invocation cost; preserve receipts and stop before another call')
    spent = sum(r['cost_usd'] for r in receipts)
    require(spent + next_estimate <= cap, f'Admission ceiling reached: ${spent:.6f} known + ${next_estimate:.6f} next envelope exceeds ${cap:.2f}')
    return spent


def guard_inputs(plan, source_dir):
    require(digest(Path(__file__).read_bytes()) == plan['harness_sha256'], 'Harness changed during study')
    for source in plan['sources'].values():
        require(digest((source_dir / source['file']).read_bytes()) == source['sha256'], 'Held-out source changed')


def saved_calls(folder, record):
    attempt = folder / 'receipts' / record['key'] / record['attempt']
    paths = sorted(attempt.glob('call-[0-9][0-9][0-9][0-9].json'))
    require(record.get('invocation_files_sha256'), 'Completed record has no invocation bindings')
    inventory = {str(p.relative_to(folder)) for p in attempt.glob('call-*') if p.is_file()}
    require(inventory == set(record['invocation_files_sha256']), 'Invocation inventory differs')
    for path in paths:
        require(all(str(p.relative_to(folder)) in inventory for p in (path, path.with_name(path.stem + '.prompt.json'), path.with_suffix('.md'))), 'Missing invocation receipt/prompt/response')
    for relative, expected in record['invocation_files_sha256'].items():
        require(digest((folder / relative).read_bytes()) == expected, f'Saved invocation artifact changed: {relative}')
    require(len(paths) == (1 if record['kind'] == 'judge' else 2), 'Completed job has unexpected call count')
    return [(read_json(p), read_json(p.with_name(p.stem + '.prompt.json')), p.with_suffix('.md').read_text()) for p in paths]


def validate_call(saved, actual, model, label):
    receipt, prompt, response = saved
    require(receipt['status'] == 'complete' and not receipt.get('partial') and receipt.get('stop_reason') not in ('length', 'max_tokens', 'error') and not receipt.get('error'), 'Saved call is failed/partial')
    require(receipt['model_requested'] == receipt['model_used'] == model and receipt['label'] == label, 'Saved requested/used model or label differs')
    require(actual == prompt and digest(prompt) == receipt['prompt_sha256'] and digest(response.encode()) == receipt['output_sha256'], 'Saved prompt/response hash differs')
    require(all(type(receipt.get(k)) is int and receipt[k] >= 0 for k in ('input_tokens', 'output_tokens', 'retries')) and isinstance(receipt.get('cost_usd'), (int, float)) and math.isfinite(receipt['cost_usd']) and receipt['cost_usd'] >= 0, 'Saved usage/cost unknown')
    return {**receipt, 'content': response, 'duration_ms': receipt.get('backend_duration_ms') or receipt['duration_ms']}


def judge_prompt(job, folder, records, docs, rt):
    source = '\n\n'.join(f'SOURCE [{k}]:\n\n{v}' for k, v in docs[job['source']].items())
    texts = [(folder / records[job[side]]['output']).read_text() for side in ('A', 'B')]
    return {'system': rt.core.PAIR, 'user': source + '\n\n=====\n\nANALYSIS A:\n\n' + texts[0] + '\n\n=====\n\nANALYSIS B:\n\n' + texts[1]}


def validate_completed(job, record, plan, folder, records, contexts, docs, rt):
    require(record.get('status') == 'complete' and record.get('identity') == plan['identity'] and record.get('job_sha256') == digest(job), 'Completed job identity differs')
    output = (folder / record['output']).read_bytes()
    require(digest(output) == record['output_sha256'], 'Completed output changed')
    require(read_json(folder / 'receipts' / job['key'] / record['attempt'] / 'job.json') == record, 'Job and results records differ')
    calls = saved_calls(folder, record)
    if job['kind'] == 'judge':
        for side in ('A', 'B'):
            parent = records.get(job[side], {})
            parent_job = next(j for j in plan['generations'] if j['key'] == job[side])
            validate_completed(parent_job, parent, plan, folder, records, contexts, docs, rt)
            require(parent.get('status') == 'complete' and record['inputs_sha256'][job[side]] == parent['output_sha256'] == digest((folder / parent['output']).read_bytes()), 'Judge parent failed or changed')
        prompt = judge_prompt(job, folder, records, docs, rt)
        response = validate_call(calls[0], prompt, MODELS['judge'], 'heldout ' + job['key'])
        verdict = rt.core.parse_judgment(response['content'], job)
        require(verdict == record['judgment'] == json.loads(output), 'Raw verdict does not map to saved judgment')
    else:
        context = contexts[job['key']]
        position = 0
        def replay(system_prompt, user_message, **kwargs):
            nonlocal position
            require(position < len(calls), 'Replay requested an extra call')
            response = validate_call(calls[position], {'system': system_prompt, 'user': user_message}, kwargs['model_hint'], kwargs['label'])
            position += 1
            return response
        result = rt.pr.run_oneshot_checked(context['cap'], context['spec'], context['documents'], depth='standard',
                    tier_overrides={'strong': MODELS['read'], 'mid': MODELS['critic']}, call_fn=replay)
        require(position == 2 and result.final_content.encode() == output and result.final_wall == record['process']['final_wall'], 'Checked replay differs from saved final')
    return True


def execute_job(job, plan, folder, records, contexts, docs, source_dir, output_root, cap, rt):
    key = job['key']
    previous = records.get(key)
    if previous and previous.get('status') == 'complete':
        validate_completed(job, previous, plan, folder, records, contexts, docs, rt)
        return
    require(not list(output_root.glob(f'*/receipts/{key}/*/call-[0-9][0-9][0-9][0-9].json')), f'{key} already has an invocation; no automatic paid retry or crash recovery is allowed')
    guard_inputs(plan, source_dir)
    if job['kind'] == 'judge':
        for side in ('A', 'B'):
            parent_job = next(j for j in plan['generations'] if j['key'] == job[side])
            validate_completed(parent_job, records.get(job[side], {}), plan, folder, records, contexts, docs, rt)
    attempt = uuid.uuid4().hex[:12]
    attempt_dir = folder / 'receipts' / key / attempt
    record = {'key': key, 'kind': job['kind'], 'identity': plan['identity'], 'job_sha256': digest(job), 'status': 'running', 'attempt': attempt, 'started_at': time.time()}
    records[key] = record
    write_json(attempt_dir / 'job.json', record)
    write_json(folder / 'results.json', records)
    inner = rt.core.Recorder(folder, attempt_dir, float('inf'), judge=job['kind'] == 'judge')
    def invoke(system_prompt, user_message, **kwargs):
        role = 'judge' if job['kind'] == 'judge' else ('read' if inner.counter == 0 else 'critic')
        require(inner.counter < (1 if job['kind'] == 'judge' else 2), 'Unplanned extra model call')
        require(kwargs['model_hint'] == MODELS[role], 'Unexpected requested model')
        prompt = {'system': system_prompt, 'user': user_message}
        if role == 'read':
            require(digest(prompt) == job['read_prompt_sha256'], 'Read prompt differs from plan')
        if role != 'judge':
            require(rt.composer.ANCHORING_LAW in system_prompt, 'Common JSON-anchor contract is absent')
        guard_inputs(plan, source_dir)
        envelope = estimate(rt, plan['calibration'], role, len(system_prompt) + len(user_message))
        budget_guard(output_root, cap, envelope)
        number = inner.counter + 1
        try:
            response = inner(system_prompt, user_message, **kwargs)
            require(response.get('model_used') == MODELS[role], 'Model fallback differs from fixed trial routing')
            require(all(type(response.get(k)) is int and response[k] >= 0 for k in ('input_tokens', 'output_tokens', 'retries')), 'Model usage/retry metadata missing')
            require(response.get('stop_reason') != 'error' and not response.get('error'), 'Model reported a response error')
            return response
        except Exception as exc:
            validation_error = {'error_type': type(exc).__name__, 'error': str(exc)}
            raise
        finally:
            path = attempt_dir / f'call-{number:04d}.json'
            if path.exists():
                receipt = read_json(path)
                receipt.update(role=role, admission_estimate_usd=envelope)
                if 'validation_error' in locals():
                    receipt.update(status='failed', **validation_error)
                if 'response' in locals():
                    receipt['backend_duration_ms'] = response.get('duration_ms')
                raw = path.with_suffix('.md')
                if raw.exists() and role != 'judge':
                    try:
                        receipt['raw_quote_diagnostics'] = quote_diagnostics(raw.read_text(), rt, docs[job['source']])
                    except Exception as diagnostic_error:
                        receipt['raw_quote_diagnostics'] = {'diagnostic_error': str(diagnostic_error)}
                write_json(path, receipt)
    try:
        if job['kind'] == 'judge':
            prompt = judge_prompt(job, folder, records, docs, rt)
            record['inputs_sha256'] = {job[side]: records[job[side]]['output_sha256'] for side in ('A', 'B')}
            result = invoke(prompt['system'], prompt['user'], model_hint=MODELS['judge'], depth='standard', label='heldout ' + key)
            verdict = rt.core.parse_judgment(result['content'], job)
            record['judgment'] = verdict
            output = json.dumps(verdict, indent=2, ensure_ascii=False)
        else:
            context = contexts[key]
            result = rt.pr.run_oneshot_checked(context['cap'], context['spec'], context['documents'], depth='standard',
                       tier_overrides={'strong': MODELS['read'], 'mid': MODELS['critic']}, call_fn=invoke)
            require(len(result.calls) == 2 and result.calls_for('check'), 'Missing reading/check stage')
            require(bool(rt.lw.parse_rows(rt.pr._ledger_text(result.final_content))), 'No final findings ledger')
            record['process'] = result.receipts()
            output = result.final_content
        output_path = Path('outputs') / f'{key}.md'
        (folder / output_path).parent.mkdir(parents=True, exist_ok=True)
        with (folder / output_path).open('x', encoding='utf-8') as handle:
            handle.write(output)
        record.update(status='complete', output=str(output_path), output_sha256=digest(output.encode()))
    except Exception as exc:
        record.update(status='failed', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        record['seconds'] = round(time.time() - record['started_at'], 3)
        record['invocation_files_sha256'] = {str(p.relative_to(folder)): digest(p.read_bytes()) for p in sorted(attempt_dir.glob('call-*')) if p.is_file()}
        write_json(attempt_dir / 'job.json', record)
        write_json(folder / 'results.json', records)


def report(plan, folder, contexts, docs, rt):
    records = read_json(folder / 'results.json', {})
    valid, errors = {}, {}
    for job in plan['generations'] + plan['judgments']:
        record = records.get(job['key'], {})
        valid[job['key']] = False
        if record.get('status') == 'complete':
            try:
                valid[job['key']] = validate_completed(job, record, plan, folder, records, contexts, docs, rt)
            except Exception as exc:
                errors[job['key']] = str(exc)
    calls = [read_json(p) for p in sorted(folder.glob('receipts/*/*/call-[0-9][0-9][0-9][0-9].json'))]
    pairs = []
    for engine in ENGINES:
        for paper in SOURCES:
            jobs = [j for j in plan['judgments'] if j['engine'] == engine and j['source'] == paper]
            winners = [records[j['key']]['judgment']['winner'].split('__')[1] if records[j['key']]['judgment']['winner'] != 'tie' else 'tie'
                       for j in jobs if valid[j['key']] and all(valid[j[s]] for s in ('A', 'B'))]
            pairs.append({'engine': engine, 'paper': paper, 'outcome': rt.sums.pair_outcome(winners), 'orders': [dict(order=j['order'], winner=records.get(j['key'], {}).get('judgment', {}).get('winner'), valid=valid[j['key']]) for j in jobs]})
    return {'identity': plan['identity'], 'valid_generations': sum(valid[j['key']] for j in plan['generations']),
            'valid_judgments': sum(valid[j['key']] for j in plan['judgments']), 'status_counts': dict(Counter(r['status'] for r in records.values())),
            'validation_errors': errors, 'pairs': pairs, 'usage_total': rt.sums.sum_calls(calls),
            'termination_metadata': {'unknown_partial': sum(r.get('partial') is None for r in calls), 'unknown_stop_reason': sum(r.get('stop_reason') is None for r in calls)},
            'final_walls': {key: r.get('process', {}).get('final_wall') for key, r in records.items() if r.get('kind') == 'generation'},
            'usage_by_role': {role: rt.sums.sum_calls([r for r in calls if r.get('role') == role]) for role in MODELS},
            'raw_quote_diagnostics': [{'job': p.parents[1].name, 'call': p.name, 'role': (r := read_json(p)).get('role'), 'diagnostics': r.get('raw_quote_diagnostics')}
                    for p in sorted(folder.glob('receipts/*/*/call-[0-9][0-9][0-9][0-9].json')) if read_json(p).get('role') != 'judge'],
            'limitations': ['Only matching valid decisions in both orders count; splits and incomplete pairs are separate.',
                'Both conditions share the repaired runtime and checking; this contrasts process-definition packages, not runtime repairs or any individual question.',
                'Visible formatting, length and check receipts may affect the judge; no corpus dimension is exercised by these single-paper inputs.',
                'Costs are saved invocation estimates. Unknown costs block another call; provider retries/charges or an in-flight overrun cannot be promised away.',
                'Canonical JSON quote compliance is measured on raw read/critic outputs separately from parsing and membership walls; neither is semantic accuracy.']}


def main(argv=None):
    default_root = project_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources-dir', type=Path, default=default_root / 'data/study/sources_ideas')
    parser.add_argument('--calibration-dir', type=Path, default=default_root / 'data/study/ideas_2026_09_05/374325c24e6b10a1')
    parser.add_argument('--output-root', type=Path, default=default_root / 'data/study/ideas_hegel_heldout_2026_09_05')
    parser.add_argument('--phase', choices=('generate', 'judge', 'report'), default='generate')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--budget-usd', type=float)
    parser.add_argument('--require-complete', action='store_true', help='Fail unless all 16 readings and 16 judgments validate')
    args = parser.parse_args(argv)
    require(not args.run or args.phase != 'report', '--phase report never launches calls')
    require(not args.run or args.budget_usd is not None and 0 < args.budget_usd <= CAP_USD, '--run requires --budget-usd at most6')
    from dotenv import load_dotenv
    load_dotenv(default_root / '.env', override=False)
    with frozen_runtime() as rt:
        plan, contexts, docs = build_plan(rt, args.sources_dir, args.calibration_dir)
        folder = args.output_root / plan['identity'][:16]
        saved_plan = read_json(folder / 'plan.json')
        require(saved_plan is None or saved_plan == plan, 'Existing plan differs')
        if args.run:
            args.output_root.mkdir(parents=True, exist_ok=True)
            with (args.output_root / 'heldout.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                old = read_json(folder / 'plan.json')
                require(old is None or old == plan, 'Existing plan differs')
                write_json(folder / 'plan.json', plan)
                records = read_json(folder / 'results.json', {})
                jobs = plan['generations'] if args.phase == 'generate' else plan['judgments']
                if args.phase == 'judge':
                    for job in plan['generations']:
                        validate_completed(job, records.get(job['key'], {}), plan, folder, records, contexts, docs, rt)
                try:
                    for job in jobs:
                        print(f"{args.phase}: {job['key']}", flush=True)
                        execute_job(job, plan, folder, records, contexts, docs, args.sources_dir, args.output_root, args.budget_usd, rt)
                finally:
                    write_json(folder / 'report.json', report(plan, folder, contexts, docs, rt))
        if args.phase == 'report' or args.run:
            result = report(plan, folder, contexts, docs, rt)
        else:
            result = {'mode': 'NO-CALL PREVIEW', 'identity': plan['identity'], 'folder': str(folder), 'runtime_commit': RUNTIME,
                      'sources': plan['sources'], 'definition_commits': CONDITIONS, 'matrix': plan['generations'] + plan['judgments'],
                      'planned_invocations': plan['planned_invocations'], 'estimated_cost_by_role': plan['estimated_cost_by_role'],
                      'estimated_total_usd': round(sum(plan['estimated_cost_by_role'].values()), 6), 'fresh_cap_usd': CAP_USD,
                      'phase': args.phase, 'calibration_method': plan['calibration']['method']}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if args.require_complete:
            require(result.get('valid_generations') == 16 and result.get('valid_judgments') == 16 and not result.get('validation_errors'), 'Study is not complete')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
