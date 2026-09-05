"""Isolated corpus synthesis follow-up; dry-run by default, no full-chain reruns.

Requires the original 52-job study to be complete and idle, including recovered
parents and judging. Replays the saved corpus calls exactly, then removes only
critic auxiliary-section references from the synthesis handoff and inserts the
pinned corpus-reading instruction into the original system prompt. --run
requires an explicit cumulative budget no greater than the existing $20 approval.
Original outputs/receipts and earlier follow-up attempts are never overwritten.
The cap gates new calls on known spend; an in-flight call or provider retries may
exceed its remaining estimate. Unknown costs stop subsequent scheduling.
Each corpus job may have at most one recorded follow-up invocation across all
follow-up identities. Failed, partial, or ambiguous attempts require offline review;
they never silently authorize another paid synthesis.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import time
import uuid
import difflib

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/study/ideas_2026_09_05/374325c24e6b10a1"
OUT = ROOT / "data/study/ideas_corpus_synthesis_followup_2026_09_05"
BASE_IDENTITY = "374325c24e6b10a15663e9cbe9fd3520818964bc05f8f46b2d88944e0b7cbfca"
COMMIT = "c19513884a5453f54073e38cbabf2c6e7d5cfd28"
MODEL = "openrouter/openai/gpt-5.6-sol"
INSTRUCTION = BASE / "reader_notes/corpus_reading_instruction.txt"
INSTRUCTION_SHA256 = "a598d16071667a9ae772a04b889ed56f66ece8e3450b7ccccc71bb2fedf46481"
MARKER = "## What the reading contains, in order"
VERIFIED_MARKER = "\n\n=====\n\nVERIFIED FINDINGS LEDGER:\n\n"
REJECTED_MARKER = "\n\n=====\n\nREJECTED BY THE CRITIC (do not reintroduce):\n\n"
AUXILIARY_HELPER = BASE / "reader_notes/auxiliary_recovery/20260905T045321.120955Z/recover_auxiliary_sections.py"
AUXILIARY_HELPER_SHA256 = "926acdc0df324d71daf82eb80e99d8ca5fdc0931c58b824cbd0ae5bcc95ef9ac"
JOBS = tuple(f"{engine}__deep__{corpus}" for engine in ("conditions_of_possibility_analyzer", "inferential_commitment_mapper")
             for corpus in ("deutschmann", "castoriadis"))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(value):
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def insert_instruction(system, user, instruction):
    require(system.count(MARKER) == 1, "Baseline system must contain exactly one insertion marker")
    require(instruction not in system, "Instruction already exists in baseline system")
    before, after = system.split(MARKER)
    revised = before + instruction + "\n\n" + MARKER + after
    require(revised.replace(instruction + "\n\n", "", 1) == system, "Insertion changed other baseline system text")
    return {"system": revised, "user": user}


class ReplayRefusal(BaseException):
    """Bypass the frozen re-anchor exception handler on a provenance mismatch."""


class SynthesisCaptured(BaseException):
    """Stop offline replay before the final model invocation."""


class SavedCorpusCalls:
    def __init__(self, saved, helper, *, capture_final=False):
        self.saved, self.helper, self.capture_final = saved, helper, capture_final
        self.position, self.captured = 0, None

    def __call__(self, system_prompt, user_message, **kwargs):
        try:
            require(self.position < len(self.saved), "Replay requested an unrecorded call")
            item = self.saved[self.position]
            actual = {"system": system_prompt, "user": user_message}
            if self.capture_final and self.position == len(self.saved) - 1:
                require(item['is_synthesis'], "Capture target is not the recorded final synthesis")
                require(system_prompt == item['prompt']['system'], "Reassembled synthesis system changed before instruction insertion")
                require(kwargs['model_hint'] == item['receipt']['model_requested'] == MODEL and
                        kwargs['label'] == item['receipt']['label'], "Reassembled synthesis model or label changed")
                require(user_message.count(VERIFIED_MARKER) == 1 and item['prompt']['user'].count(VERIFIED_MARKER) == 1,
                        "Ambiguous source/ledger boundary in reassembled synthesis")
                require(user_message.split(VERIFIED_MARKER)[0].encode() == item['prompt']['user'].split(VERIFIED_MARKER)[0].encode(),
                        "Reassembled synthesis source bytes changed")
                self.captured = actual
                raise SynthesisCaptured()
            self.helper.validate_saved_call(item['receipt'], item['prompt'], item['response'], actual,
                                            kwargs['model_hint'], kwargs['label'])
            self.position += 1
            return {**item['receipt'], 'content': item['response']}
        except SynthesisCaptured:
            raise
        except Exception as exc:
            raise ReplayRefusal(str(exc)) from exc


def reconstruct_corpus(job, cap, spec, documents, saved, baseline_output, pr, helper):
    """Only offline callbacks; actual model backends are never selected here."""
    started = time.perf_counter()
    original_view = pr._ledger_text
    original = SavedCorpusCalls(saved, helper)
    try:
        replayed = pr.run_process(cap, spec, documents, depth='deep', tier_overrides={
            'cheap':'openrouter/openai/gpt-5.6-luna', 'mid':'openrouter/deepseek/deepseek-v4-pro', 'strong':MODEL},
            call_fn=original, parallelism=1)
        require(original.position == len(saved), "Original replay did not consume every saved call")
        require(replayed.final_content.encode() == baseline_output, "Original corpus replay does not reproduce the final output exactly")
    except ReplayRefusal as exc:
        raise RuntimeError(f"Original corpus replay refused: {exc}") from exc

    critics = {digest(item['response'].encode()): item for item in saved if item['is_critic']}
    noncritics = {digest(item['response'].encode()) for item in saved if not item['is_critic']}
    require(not (set(critics) & noncritics), "A critic response is byte-identical to a noncritic response; cannot scope override unambiguously")
    changes = []
    for response_hash, item in critics.items():
        full = original_view(item['response'])
        bounded = helper.auxiliary_view(original_view, item['response'])
        original_rows, bounded_rows = pr.parse_rows(full), pr.parse_rows(bounded)
        require(len(bounded_rows) <= len(original_rows), "Auxiliary boundary unexpectedly added rows")
        removed = original_rows[len(bounded_rows):]
        positive = {r.id for r in bounded_rows if r.status in ('confirmed', 'weakened', 'added')}
        changes.append({'receipt':item['relative'], 'response_sha256':response_hash,
                        'parsed_ledger_before_sha256':digest(full.encode()), 'parsed_ledger_after_sha256':digest(bounded.encode()),
                        'removed_auxiliary_reference_ids':[r.id for r in removed],
                        'removed_positive_auxiliary_reference_ids':sorted({r.id for r in removed if r.id in positive}),
                        'removed_auxiliary_tail_sha256':digest(full[len(bounded):].encode())})

    def critic_only_view(content):
        fingerprint = digest(content.encode())
        item = critics.get(fingerprint)
        if item and content == item['response']:
            return helper.auxiliary_view(original_view, content)
        return original_view(content)

    corrected = SavedCorpusCalls(saved, helper, capture_final=True)
    pr._ledger_text = critic_only_view
    try:
        try:
            pr.run_process(cap, spec, documents, depth='deep', tier_overrides={
                'cheap':'openrouter/openai/gpt-5.6-luna', 'mid':'openrouter/deepseek/deepseek-v4-pro', 'strong':MODEL},
                call_fn=corrected, parallelism=1)
            raise RuntimeError("Corrected replay did not stop at synthesis")
        except SynthesisCaptured:
            pass
        except ReplayRefusal as exc:
            raise RuntimeError(f"Corrected pre-synthesis replay refused: {exc}") from exc
    finally:
        pr._ledger_text = original_view
    require(corrected.position == len(saved) - 1 and corrected.captured is not None,
            "Corrected replay did not match every pre-synthesis call")
    baseline_prompt = saved[-1]['prompt']
    any_removed = any(c['removed_auxiliary_reference_ids'] for c in changes)
    if not any_removed:
        require(corrected.captured['user'].encode() == baseline_prompt['user'].encode(),
                "Unaffected corpus synthesis user prompt changed")
    difference = ''.join(difflib.unified_diff(baseline_prompt['user'].splitlines(keepends=True),
                                             corrected.captured['user'].splitlines(keepends=True),
                                             fromfile='baseline-synthesis-user', tofile='reassembled-synthesis-user', n=2))
    proof = {'original_replay_output_sha256':digest(replayed.final_content.encode()),
             'original_calls_matched':original.position, 'presynthesis_calls_matched':corrected.position,
             'original_user_sha256':digest(baseline_prompt['user'].encode()),
             'reassembled_user_sha256':digest(corrected.captured['user'].encode()),
             'source_prefix_sha256':digest(baseline_prompt['user'].split(VERIFIED_MARKER)[0].encode()),
             'system_unchanged_before_instruction':corrected.captured['system'] == baseline_prompt['system'],
             'user_byte_identical':corrected.captured['user'] == baseline_prompt['user'],
             'critic_auxiliary_changes':changes, 'user_ledger_diff_sha256':digest(difference.encode()),
             'saved_calls':[{'receipt':s['relative'], 'receipt_sha256':digest(s['receipt']),
                             'prompt_sha256':digest(s['prompt']), 'response_sha256':digest(s['response'].encode()),
                             'model_requested':s['receipt']['model_requested'], 'model_used':s['receipt']['model_used'],
                             'label':s['receipt']['label']} for s in saved]}
    return corrected.captured, proof, difference, time.perf_counter() - started


def require_idle():
    require(Path("/proc").is_dir(), "Cannot inspect active study processes")
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit() or int(proc.name) == os.getpid():
            continue
        try:
            args = (proc / "cmdline").read_bytes().split(b"\0")
        except FileNotFoundError:
            continue
        require(not any(Path(os.fsdecode(x)).name == "study_ideas_material.py" for x in args if x),
                f"Original study process is active: {proc.name}")
    for root in [BASE, *sorted(OUT.glob("*"))]:
        if not root.is_dir():
            continue
        if (root / "results.json").exists():
            records = json.loads((root / "results.json").read_bytes())
            require(not any(r.get("status") == "running" for r in records.values()), f"Study/follow-up result is running: {root}")
        for path in root.glob("receipts/*/*/call-[0-9][0-9][0-9][0-9].json"):
            require(json.loads(path.read_bytes()).get("status") != "running", f"Invocation still running: {path}")


@contextmanager
def frozen_runtime():
    archive = subprocess.run(["git", "archive", COMMIT, "src", "scripts"], cwd=ROOT,
                             check=True, stdout=subprocess.PIPE).stdout
    with tempfile.TemporaryDirectory(prefix="ideas-corpus-followup-frozen-") as tmp:
        frozen = Path(tmp)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(frozen, filter="data")
        sys.path.insert(0, str(frozen))
        sys.dont_write_bytecode = True
        from scripts import study_ideas_material as study
        from src.executor import process_runner as pr
        from src.stages import process_composer as composer
        require(Path(pr.__file__).is_relative_to(frozen), "Runtime did not load from the frozen archive")
        yield frozen, study, pr, composer


def cost_totals():
    paths = [*BASE.glob("receipts/*/*/call-[0-9][0-9][0-9][0-9].json"),
             *OUT.glob("*/receipts/*/*/call-[0-9][0-9][0-9][0-9].json")]
    receipts = [json.loads(p.read_bytes()) for p in paths]
    return {"invocations": len(receipts), "known_cost_usd": round(sum(r.get("cost_usd") or 0 for r in receipts), 6),
            "unknown_cost_calls": sum(r.get("cost_usd") is None for r in receipts)}


def budget_guard(totals, cap):
    require(0 < cap <= 20, "Budget must be positive and no greater than the existing $20 approval")
    require(totals["unknown_cost_calls"] == 0, "Uncosted invocation exists; review it before another model call")
    require(totals["known_cost_usd"] < cap, f"Cumulative known spend reached ${cap:.2f}; no new call launched")


def load_context(frozen, study, pr, composer, selected):
    require_idle()
    pins = {}

    def raw(path):
        value = path.read_bytes()
        require(str(path) not in pins or pins[str(path)] == digest(value), f"Pinned input changed between reads: {path}")
        pins[str(path)] = digest(value)
        return value

    baseline = json.loads(raw(BASE / "plan.json"))
    records = json.loads(raw(BASE / "results.json"))
    require(baseline["identity"] == BASE_IDENTITY and digest({k: v for k, v in baseline.items() if k != "identity"}) == BASE_IDENTITY,
            "Original plan identity mismatch")
    for filename, expected in baseline["code_sha256"].items():
        require(digest((frozen / filename).read_bytes()) == expected, f"Frozen code mismatch: {filename}")
    fresh, sources = study.build_plan(ROOT / "data/study/sources_ideas")
    require(fresh["identity"] == BASE_IDENTITY and digest(fresh) == digest(baseline), "Frozen source/definition/runtime plan does not reproduce baseline")
    all_jobs = baseline["generations"] + baseline["judgments"]
    require(len(all_jobs) == 52 and all(study.job_completed(j, records, BASE) for j in all_jobs),
            "All 52 original jobs, including recovery judging, must validate before a follow-up plan can be made")
    for job in all_jobs:
        raw(BASE / records[job["key"]]["output"])
    for source in baseline["sources"].values():
        require(digest(raw(ROOT / "data/study/sources_ideas" / source["file"])) == source["sha256"], "Baseline source changed")
    instruction_raw = raw(INSTRUCTION)
    require(digest(instruction_raw) == INSTRUCTION_SHA256, "Reviewed corpus instruction changed")
    instruction = instruction_raw.decode("utf-8")
    require(digest(raw(AUXILIARY_HELPER)) == AUXILIARY_HELPER_SHA256, "Accepted auxiliary transform changed")
    helper_spec = importlib.util.spec_from_file_location('reviewed_corpus_auxiliary_helper', AUXILIARY_HELPER)
    helper = importlib.util.module_from_spec(helper_spec)
    helper_spec.loader.exec_module(helper)
    parents, contexts = {}, {}
    for key in JOBS:
        job = next(j for j in baseline["generations"] if j["key"] == key)
        record = records[key]
        documents = sources[job["source"]]
        cap = study.get_engine_registry().get_capability_definition(job["engine"])
        spec = study.get_operationalization_registry().get(job["engine"]).process
        step = spec.final_step
        attempt = BASE / "receipts" / key / record["attempt"]
        all_invocations = [(p, json.loads(raw(p))) for p in sorted(attempt.glob("call-[0-9][0-9][0-9][0-9].json"))]
        candidates = [(p, r) for p, r in all_invocations if r.get("label") == f"{job['engine']} | {step.key}"]
        require(len(candidates) == 1, f"Expected one original synthesis invocation: {key}")
        receipt_path, receipt = candidates[0]
        require(receipt_path == all_invocations[-1][0], f"Original synthesis was not the final saved call: {key}")
        prompt_raw = raw(receipt_path.with_name(receipt_path.stem + ".prompt.json"))
        prompt = json.loads(prompt_raw)
        output = raw(receipt_path.with_suffix(".md"))
        require(receipt.get("status") == "complete" and not receipt.get("partial") and
                receipt.get("stop_reason") not in ("length", "max_tokens"), f"Original synthesis is incomplete: {key}")
        require(receipt.get("model_requested") == MODEL == receipt.get("model_used"), f"Original synthesis model differs: {key}")
        require(digest(prompt) == receipt["prompt_sha256"] and digest(output) == receipt["output_sha256"] == record["output_sha256"],
                f"Original synthesis prompt/output hash mismatch: {key}")
        require(prompt["user"].count(VERIFIED_MARKER) == 1, f"Ambiguous verified-ledger handoff: {key}")
        _, ledger_and_rejected = prompt["user"].split(VERIFIED_MARKER)
        require(ledger_and_rejected.count(REJECTED_MARKER) <= 1, f"Ambiguous rejected-ledger handoff: {key}")
        sections = ledger_and_rejected.split(REJECTED_MARKER)
        verified, rejected = sections[0], sections[1] if len(sections) == 2 else ""
        recomposed = composer.compose_synthesize_prompt(cap, spec, step, documents, verified, rejected_text=rejected)
        require({"system": recomposed.system, "user": recomposed.user} == prompt, f"Frozen synthesis prompt reconstruction differs: {key}")
        saved = [{'receipt':r, 'relative':str(p.relative_to(BASE)),
                  'prompt':json.loads(raw(p.with_name(p.stem + '.prompt.json'))),
                  'response':raw(p.with_suffix('.md')).decode('utf-8'),
                  'is_critic':' | verify' in r.get('label',''), 'is_synthesis':p == receipt_path}
                 for p, r in all_invocations]
        reassembled, replay_proof, user_difference, replay_cpu = reconstruct_corpus(job, cap, spec, documents, saved, output, pr, helper)
        require(reassembled['system'] == prompt['system'], f"Baseline system changed during critic cleanup: {key}")
        revised = insert_instruction(reassembled["system"], reassembled["user"], instruction)
        _, amended_ledger = revised['user'].split(VERIFIED_MARKER)
        amended_sections = amended_ledger.split(REJECTED_MARKER)
        require(len(amended_sections) <= 2, f"Ambiguous reassembled rejected ledger: {key}")
        parents[key] = {
            "baseline_job": key, "attempt": record["attempt"], "record_sha256": digest(record),
            "synthesis_receipt": str(receipt_path.relative_to(BASE)), "receipt_sha256": digest(receipt),
            "baseline_prompt_sha256": digest(prompt), "baseline_system_sha256": digest(prompt["system"].encode()),
            "baseline_user_sha256": digest(prompt["user"].encode()), "baseline_output_sha256": digest(output),
            "followup_prompt_sha256": digest(revised), "followup_system_sha256": digest(revised["system"].encode()),
            "reassembled_user_sha256":digest(reassembled['user'].encode()),
            "user_byte_identical":replay_proof['user_byte_identical'], "replay_proof_sha256":digest(replay_proof),
            "removed_positive_auxiliary_reference_ids":sorted({rid for c in replay_proof['critic_auxiliary_changes'] for rid in c['removed_positive_auxiliary_reference_ids']}),
            "requested_model": MODEL, "used_model": receipt["model_used"], "source_documents": list(documents),
        }
        contexts[key] = {"job": job, "documents": documents, "spec": spec, "prompt": revised,
                         "baseline_prompt_raw": prompt_raw, "verified": amended_sections[0],
                         "rejected":amended_sections[1] if len(amended_sections) == 2 else '',
                         "replay_proof":replay_proof, "user_difference":user_difference, "replay_cpu_seconds":replay_cpu,
                         "label": receipt["label"], "step": step}
    payload = {"study": "ideas_corpus_synthesis_followup_2026_09_05", "version": 2,
               "baseline_identity": BASE_IDENTITY, "frozen_commit": COMMIT, "parents": parents,
               "treatment":"corpus-reading instruction plus narrow critic auxiliary-section cleanup of the synthesis handoff",
               "auxiliary_transform_sha256":AUXILIARY_HELPER_SHA256,
               "instruction": instruction, "instruction_sha256": INSTRUCTION_SHA256,
               "insertion": "instruction + two newlines immediately before the unique corpus synthesis order heading",
               "jobs": list(selected), "script_sha256": digest(Path(__file__).read_bytes()),
               "baseline_inputs_sha256": pins, "approved_cumulative_cap_usd": 20}
    for path, expected in pins.items():
        require(digest(Path(path).read_bytes()) == expected, f"Baseline changed during planning: {path}")
    return {"identity": digest(payload), **payload}, contexts


def audit_final(content, context, study, pr):
    prose, ledger = study.split_ledger(content)
    rows = study.parse_rows(ledger)
    require(bool(content.strip()) and bool(ledger) and bool(rows), "Follow-up response has no findings ledger")
    prior = study.parse_rows(context["verified"])
    rejected = study.parse_rows(context["rejected"])
    dimensions = {d.key for d in context["spec"].dimensions if d.scope == "corpus"}
    corpus_ids = {r.id for r in prior if r.dim in dimensions or len({a.doc for a in r.anchors if a.doc}) > 1}
    earlier = {r.id for r in prior} | {r.id for r in rejected}
    report = study.verify_rows(rows, study.SourceIndex(context["documents"]), corpus_dimensions=dimensions, corpus_ids=corpus_ids)
    report.missing_cited = pr.check_citations(prose, {r.id for r in rows}, also_ok=earlier)
    missing_lineage = sorted({rid for row in rows for rid in row.lineage if rid not in earlier})
    wall = {**report.as_dict(), "has_ledger": bool(ledger), "prose_chars": len(prose), "missing_lineage": missing_lineage}
    coverage = {"expected": list(context["documents"]),
                "verified": sorted({a.verified_doc for row in rows for a in row.anchors if a.verified and a.verified_doc})}
    # Sidecar only: the final reading remains the exact raw synthesis response,
    # just as in the frozen baseline. Rendering/normalization does not replace it.
    return wall, coverage, pr.render_rows(rows)


def validate_completed_record(record, folder, plan, key, context):
    """Reject stale or inconsistent completion instead of paying to replace it."""
    parent = plan['parents'][key]
    require(record.get('followup_identity') == plan['identity'] and record.get('parent') == parent,
            f'Completed follow-up is not tied to the expected plan/parent: {key}')
    require(record.get('instruction_sha256') == plan['instruction_sha256'] == INSTRUCTION_SHA256,
            f'Completed follow-up instruction differs: {key}')
    attempt = record.get('attempt', '')
    require(len(attempt) == 12 and all(c in '0123456789abcdef' for c in attempt), f'Invalid saved attempt: {key}')
    expected_output = str(Path('outputs') / key / f'{attempt}.md')
    require(record.get('output') == expected_output, f'Unexpected completed output path: {key}')
    attempt_dir = folder / 'receipts' / key / attempt
    invocations = sorted(attempt_dir.glob('call-[0-9][0-9][0-9][0-9].json'))
    require([p.name for p in invocations] == ['call-0001.json'], f'Expected one synthesis invocation: {key}')
    receipt_path = invocations[0]
    receipt_raw = receipt_path.read_bytes()
    receipt = json.loads(receipt_raw)
    require(digest(receipt_raw) == record.get('invocation_receipt_sha256'), f'Completed invocation receipt changed: {key}')
    require(receipt.get('status') == 'complete' and not receipt.get('partial') and
            receipt.get('stop_reason') not in ('length', 'max_tokens') and not receipt.get('error') and not receipt.get('error_type'),
            f'Completed follow-up has a failed/partial invocation: {key}')
    require(receipt.get('model_requested') == receipt.get('model_used') == parent['requested_model'] == MODEL and
            receipt.get('label') == context['label'], f'Completed invocation model/label differs: {key}')
    require(all(type(receipt.get(k)) is int and receipt[k] > 0 for k in ('input_tokens','output_tokens','duration_ms')) and
            type(receipt.get('retries')) is int and receipt['retries'] >= 0 and receipt.get('cost_usd') is not None,
            f'Completed invocation usage/timing is missing: {key}')
    prompt = json.loads(receipt_path.with_name('call-0001.prompt.json').read_bytes())
    require(prompt == context['prompt'] and digest(prompt) == receipt.get('prompt_sha256') == parent['followup_prompt_sha256'],
            f'Completed invocation prompt differs: {key}')
    require(digest(prompt['system'].encode()) == parent['followup_system_sha256'] and
            digest(prompt['user'].encode()) == parent['reassembled_user_sha256'], f'Completed prompt component hash differs: {key}')
    response = receipt_path.with_suffix('.md').read_bytes()
    output = (folder / expected_output).read_bytes()
    require(output == response and digest(output) == receipt.get('output_sha256') == record.get('output_sha256'),
            f'Completed output differs from the saved model response: {key}')
    require((attempt_dir / 'baseline.prompt.json').read_bytes() == context['baseline_prompt_raw'], f'Copied baseline prompt changed: {key}')
    proof = json.loads((attempt_dir / 'offline-replay-proof.json').read_bytes())
    require(proof == context['replay_proof'] and digest(proof) == parent['replay_proof_sha256'], f'Offline replay proof changed: {key}')
    require(digest((attempt_dir / 'synthesis-user-ledger.diff').read_bytes()) == proof['user_ledger_diff_sha256'], f'Ledger diff changed: {key}')
    step = json.loads((attempt_dir / 'step-synthesis.json').read_bytes())
    require(step == record.get('step') and step.get('wall') == record.get('wall'), f'Completed wall/step receipt changed: {key}')
    for field in ('model_requested','model_used','input_tokens','output_tokens','retries'):
        require(step.get(field) == receipt.get(field), f'Step/invocation {field} differs: {key}')
    require(step.get('cost_usd') == round(receipt['cost_usd'], 4) and step.get('chars') == len(output.decode()),
            f'Step/invocation cost or response size differs: {key}')
    require(json.loads((attempt_dir / 'job.json').read_bytes()) == record, f'Job/results completion records differ: {key}')
    return output.decode(), attempt_dir


def complete(record, folder, plan, key, context, study, pr):
    if not record or record.get('status') != 'complete':
        return False
    content, attempt_dir = validate_completed_record(record, folder, plan, key, context)
    wall, coverage, rendered = audit_final(content, context, study, pr)
    require(wall == record['wall'] and coverage == record.get('source_coverage'), f'Frozen output audit no longer matches: {key}')
    require((attempt_dir / 'audited-ledger.md').read_bytes() == rendered.encode(), f'Rendered ledger sidecar changed: {key}')
    return True


def require_unused_corpus_job(key, output_root=OUT):
    previous = sorted(output_root.glob(f'*/receipts/{key}/*/call-[0-9][0-9][0-9][0-9].json'))
    require(not previous, f'{key} already has a saved follow-up invocation; automatic paid retry is outside the fixed four-call scope. Preserve it for offline review.')


def execute(plan, contexts, study, pr, cap):
    folder = OUT / plan["identity"][:16]
    folder.mkdir(parents=True, exist_ok=True)
    previous = study.read_json(folder / "plan.json", {})
    require(not previous or digest(previous) == digest(plan), "Existing follow-up folder has a different plan")
    study.write_json(folder / "plan.json", plan)
    records = study.read_json(folder / "results.json", {})
    for key in plan["jobs"]:
        if complete(records.get(key), folder, plan, key, contexts[key], study, pr):
            continue
        require_idle()
        require_unused_corpus_job(key)
        budget_guard(cost_totals(), cap)
        for path, expected in plan["baseline_inputs_sha256"].items():
            require(digest(Path(path).read_bytes()) == expected, f"Pinned baseline changed before launch: {path}")
        context = contexts[key]
        attempt = uuid.uuid4().hex[:12]
        attempt_dir = folder / "receipts" / key / attempt
        record = {"status": "running", "attempt": attempt, "started_at": time.time(), "parent": plan["parents"][key],
                  "followup_identity": plan["identity"], "instruction_sha256": INSTRUCTION_SHA256}
        records[key] = record
        study.write_json(folder / "results.json", records)
        study.write_json(attempt_dir / "job.json", record)
        (attempt_dir / "baseline.prompt.json").write_bytes(context["baseline_prompt_raw"])
        study.write_json(attempt_dir / "offline-replay-proof.json", context['replay_proof'])
        study.write_json(attempt_dir / "offline-replay-timing.json", {'cpu_seconds':context['replay_cpu_seconds'], 'model_calls_added':0})
        (attempt_dir / "synthesis-user-ledger.diff").write_text(context['user_difference'], encoding='utf-8')
        recorder = study.Recorder(folder, attempt_dir, float("inf"))

        def invoke(system_prompt, user_message, **kwargs):
            require({"system": system_prompt, "user": user_message} == context["prompt"], "Follow-up invocation differs from pinned prompt")
            budget_guard(cost_totals(), cap)
            response = recorder(system_prompt, user_message, **kwargs)
            require(response.get("model_used") == MODEL, "Returned model differs from the original Sol synthesis model")
            require(all(type(response.get(k)) is int and response[k] > 0 for k in ("input_tokens", "output_tokens")), "Follow-up usage is missing or invalid")
            require(type(response.get('retries')) is int and response['retries'] >= 0, 'Follow-up retry metadata is missing or invalid')
            require(not response.get("partial") and response.get("stop_reason") not in ("length", "max_tokens"), "Follow-up response is partial")
            return response

        print(f"Running isolated synthesis {key}", flush=True)
        try:
            prompt = pr.ProcessPrompt(engine_key=context["job"]["engine"], step_key=context["step"].key, kind="synthesize",
                                      system=context["prompt"]["system"], user=context["prompt"]["user"],
                                      model_tier="strong", label=context["label"], id_prefix="F")
            sc = pr._invoke(invoke, prompt, MODEL, depth="deep", big=sum(len(v) for v in context["documents"].values()) > 600_000,
                            cancellation_check=None)
            wall, coverage, rendered = audit_final(sc.content, context, study, pr)
            sc.wall = wall
            output = Path("outputs") / key / f"{attempt}.md"
            (folder / output).parent.mkdir(parents=True, exist_ok=True)
            with (folder / output).open("x", encoding="utf-8") as handle:
                handle.write(sc.content)
            (attempt_dir / "audited-ledger.md").write_text(rendered, encoding="utf-8")
            study.write_json(attempt_dir / "step-synthesis.json", sc.as_receipt())
            record.update(status="complete", output=str(output), output_sha256=digest(sc.content.encode()),
                          wall=wall, source_coverage=coverage, step=sc.as_receipt(),
                          invocation_receipt_sha256=digest((attempt_dir/'call-0001.json').read_bytes()))
        except Exception as exc:
            record.update(status="failed", error_type=type(exc).__name__, error=str(exc))
        finally:
            record["seconds"] = round(time.time() - record["started_at"], 3)
            study.write_json(attempt_dir / "job.json", record)
            study.write_json(folder / "results.json", records)
        print(f"  {record['status']}", flush=True)
        if record["status"] != "complete":
            break
    return all(complete(records.get(key), folder, plan, key, contexts[key], study, pr) for key in plan["jobs"])


def self_test():
    from types import SimpleNamespace
    import unittest

    class Guards(unittest.TestCase):
        def test_exact_insertion_and_user_bytes(self):
            system, user, instruction = 'prefix\n\n' + MARKER + '\noriginal', ' source\n\nledger\t', '## Corpus\nreviewed'
            p = insert_instruction(system, user, instruction)
            self.assertEqual(p['user'].encode(), user.encode())
            self.assertEqual(p['system'], 'prefix\n\n' + instruction + '\n\n' + MARKER + '\noriginal')
            for invalid in ('missing', system + MARKER):
                with self.assertRaises(RuntimeError):
                    insert_instruction(invalid, user, instruction)

        def test_cumulative_budget_and_unknown_spend(self):
            budget_guard({'known_cost_usd':19.9,'unknown_cost_calls':0}, 20)
            for totals, cap in (({'known_cost_usd':20,'unknown_cost_calls':0},20),
                                ({'known_cost_usd':2,'unknown_cost_calls':1},20),
                                ({'known_cost_usd':2,'unknown_cost_calls':0},21)):
                with self.assertRaises(RuntimeError):
                    budget_guard(totals,cap)

        def test_resume_binds_parent_instruction_prompt_model_and_raw_output(self):
            with tempfile.TemporaryDirectory() as tmp:
                folder = Path(tmp)
                key, attempt, text = JOBS[0], 'a'*12, 'original synthesis response'
                attempt_dir = folder/'receipts'/key/attempt
                attempt_dir.mkdir(parents=True)
                output = str(Path('outputs')/key/f'{attempt}.md')
                (folder/output).parent.mkdir(parents=True)
                (folder/output).write_text(text)
                prompt = {'system':'reviewed system','user':'reassembled user'}
                proof = {'user_ledger_diff_sha256':digest(b'diff')}
                parent = {'requested_model':MODEL, 'followup_prompt_sha256':digest(prompt),
                          'followup_system_sha256':digest(prompt['system'].encode()),
                          'reassembled_user_sha256':digest(prompt['user'].encode()), 'replay_proof_sha256':digest(proof)}
                plan = {'identity':'identity', 'instruction_sha256':INSTRUCTION_SHA256, 'parents':{key:parent}}
                context = {'label':'engine | synthesize', 'prompt':prompt, 'baseline_prompt_raw':b'baseline prompt', 'replay_proof':proof}
                receipt = {'status':'complete','partial':None,'stop_reason':None,'model_requested':MODEL,'model_used':MODEL,
                           'label':context['label'],'input_tokens':1,'output_tokens':2,'duration_ms':3,'retries':0,'cost_usd':0.1,
                           'prompt_sha256':digest(prompt),'output_sha256':digest(text.encode())}
                wall = {'rows':1}
                step = {k:receipt[k] for k in ('model_requested','model_used','input_tokens','output_tokens','retries','cost_usd')}
                step.update(wall=wall, chars=len(text))
                def write_json(name, obj):
                    (attempt_dir/name).write_text(json.dumps(obj))
                write_json('call-0001.json',receipt)
                write_json('call-0001.prompt.json',prompt)
                (attempt_dir/'call-0001.md').write_text(text)
                (attempt_dir/'baseline.prompt.json').write_bytes(context['baseline_prompt_raw'])
                write_json('offline-replay-proof.json',proof)
                (attempt_dir/'synthesis-user-ledger.diff').write_bytes(b'diff')
                write_json('step-synthesis.json',step)
                record = {'status':'complete','attempt':attempt,'output':output,'output_sha256':digest(text.encode()),
                          'parent':parent,'followup_identity':'identity','instruction_sha256':INSTRUCTION_SHA256,
                          'invocation_receipt_sha256':digest((attempt_dir/'call-0001.json').read_bytes()),'step':step,'wall':wall}
                write_json('job.json',record)
                self.assertEqual(validate_completed_record(record,folder,plan,key,context)[0],text)
                for field, value in (('parent',{}),('instruction_sha256','changed'),('followup_identity','changed')):
                    changed = {**record,field:value}
                    with self.assertRaises(RuntimeError):
                        validate_completed_record(changed,folder,plan,key,context)
                for mutation in ({'model_used':'fallback'},{'partial':True},{'status':'failed'}):
                    write_json('call-0001.json',{**receipt,**mutation})
                    changed = {**record,'invocation_receipt_sha256':digest((attempt_dir/'call-0001.json').read_bytes())}
                    with self.assertRaises(RuntimeError):
                        validate_completed_record(changed,folder,plan,key,context)
                write_json('call-0001.json',receipt)
                write_json('call-0001.prompt.json',{**prompt,'user':'changed'})
                with self.assertRaises(RuntimeError):
                    validate_completed_record(record,folder,plan,key,context)
                write_json('call-0001.prompt.json',prompt)
                (folder/output).write_bytes(b'changed')
                with self.assertRaises(RuntimeError):
                    validate_completed_record(record,folder,plan,key,context)

        def test_failed_invocation_cannot_trigger_an_extra_paid_call(self):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                require_unused_corpus_job(JOBS[0],root)
                prior = root/'another-identity'/'receipts'/JOBS[0]/'old-attempt'/'call-0001.json'
                prior.parent.mkdir(parents=True)
                prior.write_bytes(b'{"status":"failed","partial":true}')
                with self.assertRaises(RuntimeError):
                    require_unused_corpus_job(JOBS[0],root)
                self.assertEqual(prior.read_bytes(),b'{"status":"failed","partial":true}')

        def test_capture_changes_only_ledger_and_never_returns_model_output(self):
            saved = [{'is_synthesis':True, 'prompt':{'system':MARKER, 'user':'SOURCE'+VERIFIED_MARKER+'original ledger'},
                      'receipt':{'model_requested':MODEL, 'label':'engine | synthesize'}}]
            caller = SavedCorpusCalls(saved, SimpleNamespace(), capture_final=True)
            with self.assertRaises(SynthesisCaptured):
                caller(MARKER, 'SOURCE'+VERIFIED_MARKER+'reassembled ledger', model_hint=MODEL, label='engine | synthesize')
            self.assertEqual(caller.position, 0)
            self.assertEqual(caller.captured['user'], 'SOURCE'+VERIFIED_MARKER+'reassembled ledger')
            for system, source in ((MARKER+'changed','SOURCE'), (MARKER,'CHANGED SOURCE')):
                caller = SavedCorpusCalls(saved, SimpleNamespace(), capture_final=True)
                with self.assertRaises(ReplayRefusal):
                    caller(system, source+VERIFIED_MARKER+'ledger', model_hint=MODEL, label='engine | synthesize')

        def test_provenance_refusal_escapes_frozen_reanchor_exception_handler(self):
            def reject(*args):
                raise RuntimeError('saved prompt mismatch')
            caller = SavedCorpusCalls([{'prompt':{}, 'receipt':{}, 'response':'r'}], SimpleNamespace(validate_saved_call=reject))
            with self.assertRaises(ReplayRefusal):
                try:
                    caller('s','u',model_hint=MODEL,label='re-anchor')
                except Exception:
                    self.fail('Frozen Exception handler must not swallow provenance refusal')

    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Guards))
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--run', action='store_true')
    modes.add_argument('--dry-run', action='store_true')
    modes.add_argument('--self-test', action='store_true')
    parser.add_argument('--budget-usd', type=float, help='Cumulative original + all follow-up known-cost gate, at most 20')
    parser.add_argument('--jobs', nargs='+', choices=JOBS, default=list(JOBS))
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    selected = [key for key in JOBS if key in args.jobs]
    if args.run:
        require(args.budget_usd is not None and 0 < args.budget_usd <= 20, '--run requires --budget-usd in (0, 20]')
        from dotenv import load_dotenv
        load_dotenv(ROOT / '.env', override=False)
    with frozen_runtime() as (frozen, study, pr, composer):
        plan, contexts = load_context(frozen, study, pr, composer, selected)
        print(f"Follow-up identity: {plan['identity']}\nInstruction: {INSTRUCTION_SHA256}\nMode: {'run' if args.run else 'dry-run'}")
        print(json.dumps({'jobs':selected, 'parents':plan['parents'], 'cumulative_usage':cost_totals()},indent=2))
        if not args.run:
            print('Dry run: no model calls or persistent files written. Treatment combines the corpus instruction with narrow critic-auxiliary cleanup; final readings remain raw responses with frozen wall/ledger sidecars.')
            return 0
        OUT.mkdir(parents=True, exist_ok=True)
        with (OUT/'followup.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return 0 if execute(plan, contexts, study, pr, args.budget_usd) else 1


if __name__ == '__main__':
    raise SystemExit(main())
