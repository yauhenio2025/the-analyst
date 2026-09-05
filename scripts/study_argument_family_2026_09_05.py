"""Frozen two-candidate comparison. Preview by default; no automatic paid job retries.

--run --phase initial generates single papers/absence controls. Corpus and judge
phases require separately reviewed output/memo bindings. The campaign cap is USD16.
The original capability and checked/deep candidate are complete product treatments.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
import fcntl
import hashlib
import io
import inspect
from importlib.metadata import version
import platform
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import time
from types import SimpleNamespace
import uuid

REPO = Path(__file__).resolve().parents[1]
RUNTIME = 'af5861a3be30e5a2b795d6cd20df69662b5ffda7'
CANDIDATE_COMMIT = '005cee58e4e80947d10ebe4935e3b0d4565c279c'
ENGINES = ('dialectical_structure', 'counterfactual_analyzer')
CANDIDATE_PATH = 'communications/study/candidates/argument_family_2026_09_05'
CONTROL_PATH = 'tests/fixtures/argument_family_2026_09_05'
CONTROL_NAMES = ('archive_inventory', 'archive_policy', 'archive_fragment')
PAPERS = {'ganzinger': 'hegels_concept_of_the_concept_2026.txt',
          'elling': 'elling2025_amphibian_habits_hegel_second_nature.txt',
          'zambrana': 'zambrana2025_philosophy_in_the_severe_style_rose.txt',
          'harris': 'harris2026_eight_arguments_against_honneth.txt'}
CORPORA = {
    'castoriadis': ('castoriadis1984_technique.md', 'castoriadis1990_what_democracy.md', 'castoriadis1997_rationality_of_capitalism.md'),
    'deutschmann': ('deutschmann2001_capitalism_as_religion.md', 'deutschmann2001_promise_of_absolute_wealth.md', 'deutschmann2022_interpretation_of_capitalism_as_religion.md'),
}
MODELS = {'read': 'openrouter/openai/gpt-5.6-sol', 'critic': 'openrouter/deepseek/deepseek-v4-pro',
          'extract': 'openrouter/openai/gpt-5.6-luna', 'synthesize': 'openrouter/openai/gpt-5.6-sol', 'judge': 'claude-sonnet-4-6'}
ROUTING = {'cheap': MODELS['extract'], 'mid': MODELS['critic'], 'strong': MODELS['read']}
CAP_USD = 16.0
SCOPE_CHARS = 1600  # Declared planning envelope per new scope object/report, not source/model content.
JUDGE_RUBRIC = (
    'Two analyses of the same supplied material by the same method. Which is the better reading for an expert '
    'who must decide what this material establishes: more specific, better grounded in actual passages, '
    'more coherent and useful, and fewer unsupported attributions, scope changes or inferential claims? '
    'An honest scoped negative or inconclusive assessment can be the better result. Do not reward the number '
    'of findings, length, technical receipts or the mere presence of scope fields. Distinguish conceptual, '
    'interpretive, normative, causal and historical warrants; assess a claim against the warrant it actually '
    'offers. A discussed but inadequately answered alternative is not absent. Judge the reading against '
    'the sources, preserving quantified/modal claims and independent argument routes. Answer as JSON: '
    '{"winner":"A"|"B"|"tie","margin":"slight"|"clear"|"decisive","why":"...",'
    '"what_A_has_that_B_lacks":"...","what_B_has_that_A_lacks":"..."}'
)


def require(condition, message):
    if not condition:
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
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    temporary.replace(path)


def validate_saved_campaign(output_root, plan):
    """A report must not hide the existing campaign behind a new empty identity."""
    saved = read_json(output_root / 'campaign.json')
    require(saved is None or saved.get('identity') == plan['identity'], 'Campaign identity changed; use the exact frozen inputs')
    folder = output_root / plan['identity'][:16]
    require(read_json(folder / 'plan.json') in (None, plan), 'Saved plan differs')


@contextmanager
def frozen_runtime():
    archive = git('archive', RUNTIME, 'src', 'scripts')
    temporary_root = project_root() / 'data/study/argument_family_frozen_tmp'
    temporary_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='runtime-', dir=temporary_root) as temporary:
        frozen = Path(temporary)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(frozen, filter='data')
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(frozen))
        from scripts import study_ideas_material as core, study_ideas_hegel_heldout_2026_09_05 as heldout
        from scripts import summarize_ideas_study_2026_09_05 as sums
        from src.executor import process_runner as pr, ledger_walls as lw, scoped_outcomes as scopes
        from src.stages import process_composer as composer
        from src.operationalizations.schemas import EngineOperationalization
        import yaml
        require(all(Path(module.__file__).is_relative_to(frozen) for module in (core, heldout, pr, lw, scopes, composer)),
                'Frozen modules were already imported elsewhere; use a fresh interpreter')
        yield SimpleNamespace(core=core, h=heldout, sums=sums, pr=pr, lw=lw, scopes=scopes, composer=composer,
                              schema=EngineOperationalization, yaml=yaml, archive_sha256=digest(archive))


def matrix():
    cases = {
        ENGINES[0]: ('ganzinger', 'elling', 'zambrana', 'absence', 'castoriadis', 'mixed'),
        ENGINES[1]: ('ganzinger', 'elling', 'harris', 'absence', 'deutschmann', 'mixed'),
    }
    generations = []
    judgments = []
    for engine, sources in cases.items():
        for source in sources:
            stage = 'corpus' if source in (*CORPORA, 'mixed') else 'initial'
            for condition in ('original', 'candidate'):
                generations.append({'key': f'{engine}__{condition}__{source}', 'engine': engine, 'source': source,
                                    'condition': condition, 'kind': 'generation', 'stage': stage})
            for a, b in (('original', 'candidate'), ('candidate', 'original')):
                judgments.append({'key': f'judge__{engine}__{source}__{a}_first', 'engine': engine, 'source': source,
                                  'kind': 'judge', 'stage': 'judge', 'order': a + '_first',
                                  'A': f'{engine}__{a}__{source}', 'B': f'{engine}__{b}__{source}'})
    return generations, judgments


def calibration(rt, directory):
    cal = rt.h.calibration(directory)  # Stable prior single-paper receipt validation.
    groups = {'extract': [], 'synthesize': [], 'critic': []}
    for path in sorted(directory.glob('receipts/*__deep__*/*/call-[0-9][0-9][0-9][0-9].json')):
        receipt = read_json(path)
        role = 'extract' if receipt.get('model_requested') == MODELS['extract'] else 'synthesize' if ' | synthesize' in receipt.get('label', '') else 'critic' if receipt.get('model_requested') == MODELS['critic'] else None
        if role is None:
            continue
        prompt_path, raw_path = path.with_name(path.stem + '.prompt.json'), path.with_suffix('.md')
        prompt, raw = read_json(prompt_path), raw_path.read_bytes()
        require(receipt['status'] == 'complete' and receipt.get('cost_usd') is not None, 'Incomplete deep calibration receipt')
        require(digest(prompt) == receipt['prompt_sha256'] and digest(raw) == receipt['output_sha256'], 'Deep calibration hash mismatch')
        groups[role].append((receipt['input_tokens'] / (len(prompt['system']) + len(prompt['user'])), receipt['output_tokens'], len(raw.decode())))
        for p in (path, prompt_path, raw_path):
            cal['input_hashes'][str(p.relative_to(directory))] = digest(p.read_bytes())
    require(len(groups['extract']) >= 64 and len(groups['synthesize']) == 4, 'Expected four completed deep corpora for extraction/synthesis calibration')
    for role, values in groups.items():
        previous = cal['roles'].get(role, {})
        cal['roles'][role] = {'calls': len(values) + previous.get('calls', 0),
                             'input_tokens_per_char': max(max(v[0] for v in values) * 1.10, previous.get('input_tokens_per_char', 0)),
                             'output_tokens_envelope': max(math.ceil(max(v[1] for v in values) * 1.25), previous.get('output_tokens_envelope', 0)),
                             'maximum_response_chars': max(max(v[2] for v in values), previous.get('maximum_response_chars', 0))}
    cal['scope_chars_per_record'] = SCOPE_CHARS
    cal['method'] = ('Per-role maximum prior input tokens/character ×1.10 and output tokens ×1.25; '
                     'actual static prompts/source bytes, conservative dynamic ledger character envelopes, '
                     'plus 1600 characters per scope object/report. Planning placeholders never enter real model calls.')
    return cal


def estimate(rt, cal, role, chars, scope_count=0):
    envelope = cal['roles'][role]
    output = envelope['output_tokens_envelope'] + math.ceil(scope_count * SCOPE_CHARS * envelope['input_tokens_per_char'])
    inputs = math.ceil(chars * envelope['input_tokens_per_char'])
    return {'role': role, 'prompt_chars': chars, 'scope_output_records': scope_count,
            'input_tokens_envelope': inputs, 'output_tokens_envelope': output,
            'estimate_usd': rt.core.estimate_cost(MODELS[role], inputs, output)}


def source_block(documents):
    return '\n\n=====\n\n'.join(f'SOURCE [{key}]:\n\n{text}' for key, text in documents.items())


def original_prompt(rt, cap, documents):
    system = rt.core.old_prompt(cap)
    if len(documents) > 1:
        system += '\n\n' + rt.composer.CORPUS_ANCHORS
    return {'system': system, 'user': source_block(documents)}


def envelope_calls(rt, cal, cap, spec, documents, *, original=False):
    if original:
        prompt = original_prompt(rt, cap, documents)
        return [estimate(rt, cal, 'read', sum(map(len, prompt.values())))], {'original': digest(prompt)}
    count = len(documents)
    outcomes = rt.scopes.expected_scopes(spec, documents)
    calls, prompt_hashes = [], {}
    if count == 1:
        prompt = rt.composer.compose_oneshot_prompt(cap, spec, documents)
        calls.append(estimate(rt, cal, 'read', len(prompt.system) + len(prompt.user), len(outcomes)))
        prompt_hashes['read'] = digest({'system': prompt.system, 'user': prompt.user})
        ledger = 'x' * (math.ceil(cal['roles']['read']['maximum_response_chars'] * 1.25) + len(outcomes) * SCOPE_CHARS)
        prompt = rt.composer.compose_verify_prompt(cap, spec, spec.get_step('verify'), documents, ledger)
        calls.append(estimate(rt, cal, 'critic', len(prompt.system) + len(prompt.user), len(outcomes)))
        return calls, prompt_hashes
    extract = spec.get_step('extract')
    document_dims = [dim for dim in spec.dimensions if dim.scope == 'document']
    corpus_dims = [dim for dim in spec.dimensions if dim.scope == 'corpus']
    extraction_chars = math.ceil(cal['roles']['extract']['maximum_response_chars'] * 1.25)
    for dim in document_dims:
        for dk in documents:
            prompt = rt.composer.compose_extract_prompt(cap, spec, extract, dim, documents, doc_key=dk)
            calls.append(estimate(rt, cal, 'extract', len(prompt.system) + len(prompt.user), 1))
            prompt_hashes[f'extract:{dk}:{dim.key}'] = digest({'system': prompt.system, 'user': prompt.user})
    merged = 'x' * (count * len(document_dims) * (extraction_chars + SCOPE_CHARS) + 200 * count)
    for dim in corpus_dims:
        prompt = rt.composer.compose_extract_prompt(cap, spec, extract, dim, documents, prior_ledgers=merged)
        calls.append(estimate(rt, cal, 'extract', len(prompt.system) + len(prompt.user), 1))
    for dk in documents:
        ledger = 'x' * (len(document_dims) * (extraction_chars + SCOPE_CHARS))
        identities = rt.scopes.expected_scopes(spec, documents, doc_key=dk)
        prompt = rt.composer.compose_verify_prompt(cap, spec, spec.get_step('verify'), documents, ledger, doc_key=dk, scope_identities=identities)
        calls.append(estimate(rt, cal, 'critic', len(prompt.system) + len(prompt.user), len(identities)))
    identities = [x for x in outcomes if len(x['document_keys']) > 1]
    ledger = 'x' * (len(corpus_dims) * (extraction_chars + SCOPE_CHARS))
    prompt = rt.composer.compose_verify_prompt(cap, spec, spec.get_step('verify'), documents, ledger, scope_identities=identities)
    calls.append(estimate(rt, cal, 'critic', len(prompt.system) + len(prompt.user), len(identities)))
    verified = 'x' * ((count + 1) * math.ceil(cal['roles']['critic']['maximum_response_chars'] * 1.25) + len(outcomes) * SCOPE_CHARS)
    prompt = rt.composer.compose_synthesize_prompt(cap, spec, spec.final_step, documents, verified)
    calls.append(estimate(rt, cal, 'synthesize', len(prompt.system) + len(prompt.user), len(outcomes)))
    return calls, prompt_hashes


def build_plan(rt, source_dir, calibration_dir, controls_dir, candidate_dir):
    documents, sources, file_bindings = {}, {}, {}
    groups = {**{k: (v,) for k, v in PAPERS.items()}, **CORPORA,
              'absence': ('archive_inventory.txt',), 'mixed': ('archive_policy.txt', 'archive_inventory.txt', 'archive_fragment.txt')}
    for group, filenames in groups.items():
        documents[group] = {}
        for filename in filenames:
            control = Path(filename).stem in CONTROL_NAMES
            path = (controls_dir if control else source_dir) / filename
            raw = path.read_bytes(); text = raw.decode('utf-8'); key = Path(filename).stem
            require(text.strip(), f'Empty selected source: {filename}')
            documents[group][key] = text
            sources[key] = {'filename': filename, 'sha256': digest(raw), 'bytes': len(raw), 'chars': len(text),
                            'provenance': 'Archive Working Group — authored validation fixture' if control else 'Local ideas source; see sources_ideas/PROVENANCE.md'}
            file_bindings[str(path.resolve())] = digest(raw)
    provenance = source_dir / 'PROVENANCE.md'
    file_bindings[str(provenance.resolve())] = digest(provenance.read_bytes())
    cal = calibration(rt, calibration_dir)
    definitions, contexts = {}, {}
    generations, judgments = matrix()
    candidate_commit = git('rev-parse', CANDIDATE_COMMIT).decode().strip()
    for engine in ENGINES:
        cap = rt.core.get_engine_registry().get_capability_definition(engine)
        path = candidate_dir / f'{engine}.yaml'; raw = path.read_bytes()
        require(raw == git('show', f'{candidate_commit}:{CANDIDATE_PATH}/{engine}.yaml'), 'Candidate differs from approved committed bytes')
        op = rt.schema.model_validate(rt.yaml.safe_load(raw)); spec = op.process
        require(spec and spec.scoped_outcomes and spec.framing and 'Eligibility:' in spec.framing, 'Candidate lost actual opt-in framing/eligibility')
        require(spec.routing == ROUTING, 'Candidate routing differs')
        require([s.key for s in spec.steps] == ['extract', 'verify', 'synthesize'], 'Unsupported candidate process chain')
        require(Counter(d.scope for d in spec.dimensions) == {'document': 5, 'corpus': 1}, 'Candidate dimensions changed')
        definitions[engine] = {'capability': cap.model_dump(mode='json'),
                               'baseline_capability_file_sha256': digest(git('show', f'{RUNTIME}:src/engines/capability_definitions/{engine}.yaml')),
                               'candidate_file_sha256': digest(raw),
                               'candidate_commit': candidate_commit, 'process': spec.model_dump(mode='json')}
        file_bindings[str(path.resolve())] = digest(raw)
        for job in (j for j in generations if j['engine'] == engine):
            contexts[job['key']] = {'cap': cap, 'spec': spec, 'documents': documents[job['source']]}
            calls, hashes = envelope_calls(rt, cal, cap, spec, documents[job['source']], original=job['condition'] == 'original')
            repairs = [estimate(rt, cal, 'extract', c['prompt_chars'] + math.ceil(cal['roles']['extract']['maximum_response_chars'] * 1.25) + 1500, 1)
                       for c in calls if c['role'] == 'extract']
            job.update(base_calls=len(calls), call_envelopes=calls, static_prompt_hashes=hashes,
                       estimate_usd=round(sum(c['estimate_usd'] for c in calls), 6),
                       maximum_reanchor_calls=len(repairs), reanchor_reserve_usd=round(sum(c['estimate_usd'] for c in repairs), 6))
    maximum_final = math.ceil(max(cal['maximum_checked_final_chars'], cal['roles']['synthesize']['maximum_response_chars']) * 1.25)
    for job in judgments:
        count = len(documents[job['source']])
        scopes = 5 * count + int(count > 1)
        chars = len(JUDGE_RUBRIC) + len(source_block(documents[job['source']])) + 2 * maximum_final + scopes * SCOPE_CHARS + 80
        job.update(call_envelopes=[estimate(rt, cal, 'judge', chars)], base_calls=1)
        job['estimate_usd'] = job['call_envelopes'][0]['estimate_usd']
    role_costs = {role: round(sum(c['estimate_usd'] for j in generations + judgments for c in j['call_envelopes'] if c['role'] == role), 6) for role in MODELS}
    repair_reserve = round(sum(j['reanchor_reserve_usd'] for j in generations), 6)
    payload = {'study': 'argument_family_2026_09_05', 'version': 1, 'runtime_commit': RUNTIME,
               'runtime_archive_sha256': rt.archive_sha256, 'harness_sha256': digest(Path(__file__).read_bytes()),
               'sources': sources, 'source_groups': {k: list(v) for k, v in documents.items()}, 'input_files_sha256': file_bindings,
               'definitions': definitions, 'models': MODELS, 'judge_rubric': JUDGE_RUBRIC,
               'judge_rubric_sha256': digest(JUDGE_RUBRIC.encode()), 'original_wrapper_sha256': digest(inspect.getsource(rt.core.old_prompt).encode()),
               'shared_anchoring_law_sha256': digest(rt.composer.ANCHORING_LAW.encode()),
               'calibration': cal, 'generations': generations, 'judgments': judgments,
               'planned_base_calls': sum(j['base_calls'] for j in generations + judgments),
               'estimated_cost_by_role': role_costs, 'estimated_base_usd': round(sum(role_costs.values()), 6),
               'maximum_reanchor_calls': sum(j['maximum_reanchor_calls'] for j in generations),
               'estimated_reanchor_reserve_usd': repair_reserve, 'estimated_total_usd': round(sum(role_costs.values()) + repair_reserve, 6),
               'interpreter': {'python': platform.python_version(), 'pydantic': version('pydantic'), 'yaml': version('PyYAML')},
               'cap_usd': CAP_USD, 'pricing': {r: rt.core.PRICING[m.split('/')[-1]] for r, m in MODELS.items()},
               'transport_environment': {k: os.environ.get(k) for k in ('ENABLE_STREAMING', 'LLM_SYNC_HARD_TIMEOUT_SECONDS', 'ANTHROPIC_EXTRACTION_READ_TIMEOUT_S', 'OPENROUTER_REASONING_EFFORT')},
               'execution': 'Sequential calls; original capability one-call vs checked/deep candidate. Existing incomplete logical jobs never receive automatic paid retries. Deep re-anchoring remains bounded by the frozen runner and separately gated.'}
    payload = json.loads(json.dumps(payload))
    return {'identity': digest(payload), **payload}, contexts, documents


def guard_inputs(plan):
    require(digest(Path(__file__).read_bytes()) == plan['harness_sha256'], 'Harness changed after freezing')
    for filename, expected in plan['input_files_sha256'].items():
        require(digest(Path(filename).read_bytes()) == expected, f'Frozen input changed: {filename}')


def receipt_paths(output_root):
    return sorted(output_root.glob('*/receipts/*/*/call-[0-9][0-9][0-9][0-9].json'))


def budget_guard(output_root, cap, next_estimate):
    require(isinstance(cap, (int, float)) and math.isfinite(cap) and 0 < cap <= CAP_USD, 'Budget must be positive and at most USD16')
    require(isinstance(next_estimate, (int, float)) and math.isfinite(next_estimate) and next_estimate >= 0, 'Invalid admission estimate')
    receipts = [read_json(p) for p in receipt_paths(output_root)]
    require(all(type(r.get('cost_usd')) in (int, float) and math.isfinite(r['cost_usd']) and r['cost_usd'] >= 0 for r in receipts), 'Unknown invocation cost; no further paid calls')
    require(all(r.get('status') == 'complete' for r in receipts), 'An invocation is failed/running; no automatic paid continuation')
    spent = sum(r['cost_usd'] for r in receipts)
    require(spent + next_estimate <= cap, f'Admission ceiling: ${spent:.6f} known + ${next_estimate:.6f} next exceeds ${cap:.2f}')
    return spent


def role_for(job, label):
    if job['kind'] == 'judge':
        return 'judge'
    if job['condition'] == 'original':
        return 'read'
    if ' | extract | ' in label:
        return 'extract'
    if ' | synthesize' in label:
        return 'synthesize'
    if ' | verify' in label:
        return 'critic'
    require(' | oneshot' in label, 'Unknown process invocation label')
    return 'read'


def scope_count(job, role, label):
    if job['kind'] == 'judge' or job.get('condition') == 'original':
        return 0
    if role == 'extract':
        return 1
    if role == 'synthesize':
        return 16
    return 1 if job['stage'] == 'corpus' and label.count(' | ') == 1 else 5


def judge_prompt(job, folder, records, documents):
    outputs = [(folder / records[job[side]]['output']).read_text() for side in ('A', 'B')]
    return {'system': JUDGE_RUBRIC, 'user': source_block(documents[job['source']]) + '\n\n=====\n\nANALYSIS A:\n\n'
            + outputs[0] + '\n\n=====\n\nANALYSIS B:\n\n' + outputs[1]}


def run_generation(job, context, rt, invoke):
    docs, spec, cap = context['documents'], context['spec'], context['cap']
    if job['condition'] == 'original':
        prompt = original_prompt(rt, cap, docs)
        response = invoke(prompt['system'], prompt['user'], model_hint=MODELS['read'], depth='standard', label='argument-family ' + job['key'])
        output = response['content']
        require(rt.core.split_ledger(output)[1], 'Original response lacks the required ledger section; not an absence result')
        rows = rt.lw.parse_rows(rt.pr._ledger_text(output))
        wall = rt.lw.verify_rows(rows, rt.lw.SourceIndex(docs), corpus_dimensions={d.key for d in spec.dimensions if d.scope == 'corpus'}).as_dict()
        return output, {'final_wall': wall, 'mode': 'original_capability', 'source_keys': list(docs)}
    if job['stage'] == 'initial':
        run = rt.pr.run_oneshot_checked(cap, spec, docs, depth='standard', check=True, tier_overrides=ROUTING, call_fn=invoke)
    else:
        run = rt.pr.run_process(cap, spec, docs, depth='deep', tier_overrides=ROUTING, call_fn=invoke, parallelism=1, reanchor=True)
    require(run.final_wall.get('scope_outcomes'), 'Candidate has no final scope inventory')
    expected = {rt.scopes.scope_key(r) for r in rt.scopes.expected_scopes(spec, docs)}
    require({rt.scopes.scope_key(r) for r in run.final_wall['scope_outcomes']} == expected, 'Final candidate scope inventory lost identities')
    return run.final_content, run.receipts()


def process_projection(process):
    """Timing is measured anew during replay; model, usage, stage and walls must match."""
    process = json.loads(json.dumps(process))
    process.pop('seconds', None)
    for call in process.get('calls', []):
        call.pop('duration_ms', None)
    return process


def saved_calls(folder, record):
    attempt = folder / 'receipts' / record['key'] / record['attempt']
    inventory = {str(p.relative_to(folder)): digest(p.read_bytes()) for p in attempt.glob('call-*') if p.is_file()}
    require(inventory and inventory == record.get('invocation_files_sha256'), 'Saved invocation inventory/hash changed')
    calls = []
    for path in sorted(attempt.glob('call-[0-9][0-9][0-9][0-9].json')):
        companions = [path.with_name(path.stem + '.prompt.json'), path.with_name(path.stem + '.response.json'), path.with_suffix('.md')]
        require(all(p.is_file() for p in companions), 'Missing raw prompt/response/receipt')
        receipt, prompt, response = read_json(path), read_json(companions[0]), read_json(companions[1])
        raw = companions[2].read_text()
        require(response.get('content') == raw, 'Raw response JSON and text differ')
        calls.append((receipt, prompt, response))
    require(len(calls) == record['invocations'], 'Saved invocation count differs')
    return calls


def validate_completed(job, record, plan, folder, records, contexts, documents, rt):
    require(record.get('status') == 'complete' and record.get('identity') == plan['identity'] and record.get('job_sha256') == digest(job), 'Completed job identity/status changed')
    output = (folder / record['output']).read_bytes()
    require(digest(output) == record['output_sha256'], 'Completed output hash changed')
    require(read_json(folder / 'receipts' / job['key'] / record['attempt'] / 'job.json') == record, 'Job and results records differ')
    calls = saved_calls(folder, record)
    position = 0
    def replay(system, user, **kwargs):
        nonlocal position
        require(position < len(calls), 'Replay requested another invocation')
        receipt, prompt, response = calls[position]
        rt.h.validate_call((receipt, prompt, response['content']), {'system': system, 'user': user}, kwargs['model_hint'], kwargs['label'])
        require(receipt['response_sha256'] == digest(response), 'Raw response JSON hash mismatch')
        position += 1
        return response
    if job['kind'] == 'judge':
        for side in ('A', 'B'):
            parent = next(j for j in plan['generations'] if j['key'] == job[side])
            validate_completed(parent, records.get(parent['key'], {}), plan, folder, records, contexts, documents, rt)
            require(record['inputs_sha256'][parent['key']] == records[parent['key']]['output_sha256'], 'Judge input binding changed')
        prompt = judge_prompt(job, folder, records, documents)
        response = replay(prompt['system'], prompt['user'], model_hint=MODELS['judge'], label='argument-family ' + job['key'])
        verdict = rt.core.parse_judgment(response['content'], job)
        require(verdict == record['judgment'] == json.loads(output), 'Both-order verdict mapping differs')
    else:
        content, process = run_generation(job, contexts[job['key']], rt, replay)
        require(content.encode() == output and process_projection(process) == process_projection(record['process']), 'Runtime replay differs from saved output/receipt')
    require(position == len(calls), 'Replay did not consume all saved invocations')
    return True


def execute_job(job, plan, folder, records, contexts, documents, output_root, cap, rt):
    key = job['key']
    if records.get(key, {}).get('status') == 'complete':
        return validate_completed(job, records[key], plan, folder, records, contexts, documents, rt)
    require(not records.get(key), f'{key} already has an incomplete logical record; no automatic retry')
    require(not list(output_root.glob(f'*/receipts/{key}/*/call-*')), f'{key} already has logical-job calls; no paid replay')
    guard_inputs(plan)
    if job['kind'] == 'judge':
        for side in ('A', 'B'):
            parent = next(j for j in plan['generations'] if j['key'] == job[side])
            validate_completed(parent, records.get(parent['key'], {}), plan, folder, records, contexts, documents, rt)
    record = {'key': key, 'kind': job['kind'], 'identity': plan['identity'], 'job_sha256': digest(job),
              'status': 'running', 'attempt': uuid.uuid4().hex[:12], 'started_at': time.time()}
    attempt = folder / 'receipts' / key / record['attempt']
    records[key] = record
    write_json(attempt / 'job.json', record); write_json(folder / 'results.json', records)
    counter = 0
    def invoke(system, user, **kwargs):
        nonlocal counter
        role = role_for(job, kwargs['label'])
        require(kwargs['model_hint'] == MODELS[role], 'Requested model differs from frozen route')
        require(counter < job['base_calls'] + (16 if job.get('stage') == 'corpus' and job.get('condition') == 'candidate' else 0), 'Unexpected extra invocation')
        prompt = {'system': system, 'user': user}
        hashes = job.get('static_prompt_hashes', {})
        if role == 'read':
            require(digest(prompt) == hashes.get('original' if job.get('condition') == 'original' else 'read'), 'Static read prompt differs')
        if role == 'extract' and not kwargs['label'].endswith('(re-anchor)'):
            fields = kwargs['label'].split(' | ')
            if len(fields) == 4:
                require(digest(prompt) == hashes.get(f'extract:{fields[3]}:{fields[2]}'), 'Static extraction prompt differs')
        guard_inputs(plan)
        envelope = estimate(rt, plan['calibration'], role, len(system) + len(user), scope_count(job, role, kwargs['label']))
        budget_guard(output_root, cap, envelope['estimate_usd'])
        counter += 1
        path = attempt / f'call-{counter:04d}.json'
        receipt = {'status': 'running', 'role': role, 'model_requested': kwargs['model_hint'], 'label': kwargs['label'],
                   'prompt_sha256': digest(prompt), 'admission': envelope, 'cost_usd': None, 'started_at': time.time()}
        write_json(path.with_name(path.stem + '.prompt.json'), prompt); write_json(path, receipt)
        try:
            backend = rt.core.run_engine_call if role == 'judge' else rt.core.run_engine_call_auto
            response = backend(system_prompt=system, user_message=user, phase_number=1.0, **kwargs)
            require(isinstance(response, dict), 'Backend response is not an object')
            write_json(path.with_name(path.stem + '.response.json'), response)
            raw = response.get('content') or ''; path.with_suffix('.md').write_text(raw)
            known = all(type(response.get(k)) is int and response[k] >= 0 for k in ('input_tokens', 'output_tokens'))
            receipt.update({k: response.get(k) for k in ('model_used', 'input_tokens', 'output_tokens', 'thinking_tokens', 'retries', 'partial', 'stop_reason', 'connection_error')})
            receipt.update(response_sha256=digest(response), output_sha256=digest(raw.encode()), backend_duration_ms=response.get('duration_ms'),
                           cost_usd=rt.core.estimate_cost(response.get('model_used') or kwargs['model_hint'], response['input_tokens'], response['output_tokens']) if known else None)
            require(response.get('model_used') == kwargs['model_hint'], 'Fallback differs from the fixed requested model')
            require(known and type(response.get('retries')) is int and response['retries'] >= 0, 'Usage/retry metadata is unknown')
            require(raw.strip() and not response.get('partial') and response.get('stop_reason') not in ('length', 'max_tokens', 'error')
                    and not response.get('error') and not response.get('connection_error'), 'Empty/partial/error response retained; job stops')
            receipt['status'] = 'complete'
            if role != 'judge':
                receipt['raw_quote_diagnostics'] = rt.h.quote_diagnostics(raw, rt, documents[job['source']])
            return response
        except Exception as exc:
            receipt.update(status='failed', error_type=type(exc).__name__, error=str(exc))
            raise
        finally:
            receipt['duration_ms'] = round((time.time() - receipt['started_at']) * 1000)
            write_json(path, receipt)
    try:
        if job['kind'] == 'judge':
            prompt = judge_prompt(job, folder, records, documents)
            record['inputs_sha256'] = {job[s]: records[job[s]]['output_sha256'] for s in ('A', 'B')}
            response = invoke(prompt['system'], prompt['user'], model_hint=MODELS['judge'], depth='standard', label='argument-family ' + key)
            record['judgment'] = rt.core.parse_judgment(response['content'], job)
            output = json.dumps(record['judgment'], ensure_ascii=False, indent=2)
        else:
            output, record['process'] = run_generation(job, contexts[key], rt, invoke)
        require(all(read_json(p)['status'] == 'complete' for p in attempt.glob('call-[0-9][0-9][0-9][0-9].json')), 'A swallowed invocation failure cannot publish a completed job')
        output_path = Path('outputs') / f'{key}.md'
        (folder / output_path).parent.mkdir(parents=True, exist_ok=True)
        with (folder / output_path).open('x') as handle:
            handle.write(output)
        record.update(status='complete', output=str(output_path), output_sha256=digest(output.encode()))
    except Exception as exc:
        record.update(status='failed', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        record['seconds'] = round(time.time() - record['started_at'], 3)
        record['invocations'] = counter
        record['invocation_files_sha256'] = {str(p.relative_to(folder)): digest(p.read_bytes()) for p in sorted(attempt.glob('call-*')) if p.is_file()}
        write_json(attempt / 'job.json', record); write_json(folder / 'results.json', records)


def review_gate(path, phase, plan, folder, records, contexts, documents, rt):
    required = [j for j in plan['generations'] if phase == 'judge' or j['stage'] == 'initial']
    bindings = {}
    for job in required:
        record = records.get(job['key'], {})
        validate_completed(job, record, plan, folder, records, contexts, documents, rt)
        bindings[job['key']] = record['output_sha256']
    require(path is not None and path.is_file(), f'{phase} requires a separate reviewed output/memo record')
    review = read_json(path)
    require(review.get('identity') == plan['identity'] and review.get('phase') == phase and review.get('decision') == 'proceed'
            and review.get('outputs_sha256') == bindings, 'Review gate does not bind these exact completed prerequisites')
    memo = Path(review.get('memo_path', ''))
    require(memo.is_file() and memo.read_text().strip() and digest(memo.read_bytes()) == review.get('memo_sha256'), 'Review memo is missing/changed')
    return {'record_sha256': digest(path.read_bytes()), 'memo_sha256': review['memo_sha256'], 'outputs_sha256': bindings}


def report(plan, folder, records, contexts, documents, rt):
    valid, errors = {}, {}
    for job in plan['generations'] + plan['judgments']:
        valid[job['key']] = False
        if records.get(job['key'], {}).get('status') == 'complete':
            try:
                valid[job['key']] = validate_completed(job, records[job['key']], plan, folder, records, contexts, documents, rt)
            except Exception as exc:
                errors[job['key']] = str(exc)
    pairs = []
    for engine, source in dict.fromkeys((j['engine'], j['source']) for j in plan['judgments']):
        jobs = [j for j in plan['judgments'] if j['engine'] == engine and j['source'] == source]
        winners = [records[j['key']]['judgment']['winner'] for j in jobs if valid[j['key']]]
        outcome = 'incomplete' if len(winners) != 2 else 'split' if winners[0] != winners[1] else 'tie' if winners[0] == 'tie' else winners[0].split('__')[1]
        pairs.append({'engine': engine, 'source': source, 'outcome': outcome, 'order_winners': winners})
    calls = [read_json(p) for p in folder.glob('receipts/*/*/call-[0-9][0-9][0-9][0-9].json')]
    return {'identity': plan['identity'], 'valid_generations': sum(valid[j['key']] for j in plan['generations']),
            'valid_judgments': sum(valid[j['key']] for j in plan['judgments']), 'validation_errors': errors,
            'status_counts': dict(Counter(r['status'] for r in records.values())), 'pairs': pairs,
            'usage': rt.sums.sum_calls(calls), 'usage_by_role': {r: rt.sums.sum_calls([c for c in calls if c['role'] == r]) for r in MODELS},
            'final_walls': {k: r.get('process', {}).get('final_wall') for k, r in records.items() if r['kind'] == 'generation'},
            'limits': ['A quote match, scoped review or two-order win is not semantic certification.',
                       'Unknown termination metadata remains unknown. Existing failed/running invocations block paid continuation.',
                       'Budget is an admission envelope, not a guarantee about provider billing or internal backend retries.']}


def main(argv=None):
    root = project_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--phase', choices=('initial', 'corpus', 'judge', 'report'), default='initial')
    parser.add_argument('--budget-usd', type=float)
    parser.add_argument('--review-record', type=Path)
    parser.add_argument('--output-root', type=Path, default=root / 'data/study/argument_family_2026_09_05')
    parser.add_argument('--sources-dir', type=Path, default=root / 'data/study/sources_ideas')
    parser.add_argument('--controls-dir', type=Path, default=root / CONTROL_PATH)
    parser.add_argument('--candidate-dir', type=Path, default=root / CANDIDATE_PATH)
    parser.add_argument('--calibration-dir', type=Path, default=root / 'data/study/ideas_2026_09_05/374325c24e6b10a1')
    parser.add_argument('--write-preview', type=Path, help='Write the complete no-call frozen plan for review')
    args = parser.parse_args(argv)
    require(not args.run or args.phase != 'report', 'Report never makes calls')
    require(not args.run or args.budget_usd is not None and math.isfinite(args.budget_usd) and 0 < args.budget_usd <= CAP_USD, '--run requires a positive --budget-usd at most16')
    require(not args.run or args.output_root.resolve() == (root / 'data/study/argument_family_2026_09_05').resolve(), 'Paid runs share the one canonical campaign root/lock')
    from dotenv import load_dotenv
    load_dotenv(root / '.env', override=False)
    with frozen_runtime() as rt:
        plan, contexts, documents = build_plan(rt, args.sources_dir, args.calibration_dir, args.controls_dir, args.candidate_dir)
        folder = args.output_root / plan['identity'][:16]
        if args.phase == 'report':
            validate_saved_campaign(args.output_root, plan)
        if args.write_preview:
            write_json(args.write_preview, plan)
        if args.run:
            require(plan['estimated_total_usd'] <= args.budget_usd, 'Full-matrix preview exceeds the authorized cap; review the envelope before any launch')
            args.output_root.mkdir(parents=True, exist_ok=True)
            with (args.output_root / 'campaign.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                validate_saved_campaign(args.output_root, plan)
                write_json(args.output_root / 'campaign.json', {'identity': plan['identity'], 'cap_usd': args.budget_usd})
                write_json(folder / 'plan.json', plan)
                records = read_json(folder / 'results.json', {})
                if args.phase in ('corpus', 'judge'):
                    gate = review_gate(args.review_record, args.phase, plan, folder, records, contexts, documents, rt)
                    write_json(folder / 'reviews' / f'{args.phase}.json', gate)
                jobs = plan['judgments'] if args.phase == 'judge' else [j for j in plan['generations'] if j['stage'] == args.phase]
                try:
                    for job in jobs:
                        print(f"{args.phase}: {job['key']}", flush=True)
                        execute_job(job, plan, folder, records, contexts, documents, args.output_root, args.budget_usd, rt)
                finally:
                    write_json(folder / 'report.json', report(plan, folder, records, contexts, documents, rt))
        if args.run or args.phase == 'report':
            result = report(plan, folder, read_json(folder / 'results.json', {}), contexts, documents, rt)
        else:
            result = {'mode': 'NO-CALL PREVIEW', 'identity': plan['identity'], 'runtime': RUNTIME, 'candidate_commit': CANDIDATE_COMMIT,
                      'generation_outputs': len(plan['generations']), 'judgments': len(plan['judgments']), 'base_calls': plan['planned_base_calls'],
                      'estimated_total_usd': plan['estimated_total_usd'], 'estimated_base_usd': plan['estimated_base_usd'],
                      'estimated_reanchor_reserve_usd': plan['estimated_reanchor_reserve_usd'], 'maximum_reanchor_calls': plan['maximum_reanchor_calls'], 'cap_usd': CAP_USD, 'fits_cap': plan['estimated_total_usd'] <= CAP_USD,
                      'estimated_cost_by_role': plan['estimated_cost_by_role'],
                      'jobs': [{'key': j['key'], 'base_calls': j['base_calls'], 'estimate_usd': j['estimate_usd']} for j in plan['generations'] + plan['judgments']],
                      'calibration': {k: v for k, v in plan['calibration'].items() if k != 'input_hashes'},
                      'review_record_shape': {'identity': plan['identity'], 'phase': 'corpus|judge', 'decision': 'proceed',
                                              'outputs_sha256': '<all exact prerequisite outputs>', 'memo_path': '<review memo>', 'memo_sha256': '<hash>'}}
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
