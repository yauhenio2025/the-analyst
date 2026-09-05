"""Read-only aggregate of the pinned ideas study. No runtime imports or model calls.

Default prints Markdown; --json prints the complete aggregate. Shell redirection
can save a report. Inputs are hashed and checked again before output; concurrent
changes cause refusal rather than a mixed snapshot. Costs come only from original
invocation receipts, including historical failed attempts, never recovery copies.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN = ROOT / "data/study/ideas_2026_09_05/374325c24e6b10a1"
IDENTITY = "374325c24e6b10a15663e9cbe9fd3520818964bc05f8f46b2d88944e0b7cbfca"
COMMIT = "c19513884a5453f54073e38cbabf2c6e7d5cfd28"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


class Snapshot:
    def __init__(self, root):
        self.root, self.hashes, self.inventories = root, {}, {}

    def raw(self, path):
        raw = path.read_bytes()
        relative, fingerprint = str(path.relative_to(self.root)), digest(raw)
        require(relative not in self.hashes or self.hashes[relative] == fingerprint,
                f"Study changed between reads: {relative}; rerun")
        self.hashes[relative] = fingerprint
        return raw

    def json(self, path):
        return json.loads(self.raw(path))

    def glob(self, pattern):
        paths = sorted(self.root.glob(pattern))
        self.inventories[pattern] = [str(p.relative_to(self.root)) for p in paths]
        return paths

    def verify(self):
        for relative, expected in self.hashes.items():
            require(digest((self.root / relative).read_bytes()) == expected, f"Study changed while aggregating: {relative}; rerun")
        for pattern, expected in self.inventories.items():
            require([str(p.relative_to(self.root)) for p in sorted(self.root.glob(pattern))] == expected,
                    f"Receipt inventory changed while aggregating: {pattern}; rerun")


def complete(record, snapshot):
    if not record or record.get("status") != "complete" or not record.get("output"):
        return False
    path = snapshot.root / record["output"]
    return path.is_file() and digest(snapshot.raw(path)) == record.get("output_sha256")


def judgment_complete(job, records, snapshot):
    record = records.get(job["key"], {})
    if not complete(record, snapshot) or not all(complete(records.get(job[side]), snapshot) for side in ("A", "B")):
        return False
    expected = {job[side]: records[job[side]]["output_sha256"] for side in ("A", "B")}
    verdict = record.get("judgment", {})
    try:
        saved_verdict = json.loads(snapshot.raw(snapshot.root / record["output"]))
    except (ValueError, UnicodeDecodeError):
        return False
    return (saved_verdict == verdict and isinstance(verdict, dict)
            and record.get("inputs_sha256") == expected and verdict.get("winner") in ("tie", job["A"], job["B"])
            and verdict.get("margin") in ("slight", "clear", "decisive")
            and isinstance(verdict.get("why"), str) and bool(verdict["why"].strip()))


def pair_outcome(winners):
    if len(winners) != 2 or any(w is None for w in winners):
        return "incomplete"
    return winners[0] if winners[0] == winners[1] else "split"


def role(job, receipt):
    if job["kind"] == "judge":
        return "judge"
    if job["kind"] == "corpus":
        return "corpus"
    if job["condition"] == "checked" and " | verify" in (receipt.get("label") or ""):
        return "critic"
    return "generation"


def sum_calls(calls):
    return {
        "invocations": len(calls), "complete": sum(c.get("status") == "complete" for c in calls),
        "failed": sum(c.get("status") == "failed" for c in calls), "running": sum(c.get("status") == "running" for c in calls),
        "cost_usd": round(sum(c.get("cost_usd") or 0 for c in calls), 6),
        "unknown_cost_calls": sum(c.get("cost_usd") is None for c in calls),
        "input_tokens": sum(c.get("input_tokens") or 0 for c in calls),
        "output_tokens": sum(c.get("output_tokens") or 0 for c in calls),
        "unknown_usage_calls": sum(c.get("input_tokens") is None or c.get("output_tokens") is None for c in calls),
        "duration_seconds": round(sum(c.get("duration_ms") or 0 for c in calls) / 1000, 3),
        "unknown_duration_calls": sum(c.get("duration_ms") is None for c in calls),
        "reported_retry_calls": sum(bool(c.get("retries")) for c in calls),
        "reported_retry_count": sum(c.get("retries") or 0 for c in calls),
        "unknown_retry_calls": sum(c.get("retries") is None for c in calls),
        "fallback_calls": sum(bool(c.get("model_used")) and c.get("model_requested") != c.get("model_used") for c in calls),
        "unknown_model_used_calls": sum(not c.get("model_used") for c in calls),
        "partial_responses": sum(bool(c.get("partial")) or c.get("stop_reason") in ("length", "max_tokens") for c in calls),
    }


def failure_kind(job, calls):
    if job.get("status") != "failed":
        return None
    failed_calls = [c for c in calls if c.get("status") == "failed"]
    if failed_calls:
        if all(c.get("partial") or c.get("stop_reason") in ("length", "max_tokens") or
               c.get("error") == "Model returned empty or partial output; retained for inspection" for c in failed_calls):
            return "response_validation_failure"
        return "invocation_or_backend_failure"
    if calls and all(c.get("status") == "complete" for c in calls):
        return "postprocess_failure_after_complete_calls"
    return "before_call_or_unknown_failure"


def nominal_corpus_calls(plan, job):
    dims = plan["definitions"][job["engine"]]["operationalization"]["process"]["dimensions"]
    docs = len(plan["source_groups"][job["source"]])
    return docs * sum(d["scope"] == "document" for d in dims) + sum(d["scope"] == "corpus" for d in dims) + docs + 1 + 1


def aggregate(run):
    snap = Snapshot(run)
    plan, records = snap.json(run / "plan.json"), snap.json(run / "results.json")
    require(plan.get("identity") == IDENTITY and digest({k: v for k, v in plan.items() if k != "identity"}) == IDENTITY,
            "Unexpected or changed plan identity")
    frozen_runner = subprocess.run(["git", "show", f"{COMMIT}:src/executor/engine_runner.py"], cwd=ROOT,
                                   check=True, stdout=subprocess.PIPE).stdout
    require(digest(frozen_runner) == plan["code_sha256"]["src/executor/engine_runner.py"], "Chunking runtime hash differs from plan")
    threshold = int(re.search(rb"^CHUNK_THRESHOLD = ([\d_]+)", frozen_runner, re.M).group(1).replace(b"_", b""))
    jobs = {j["key"]: j for j in plan["generations"] + plan["judgments"]}
    calls, by_attempt, by_role, by_model = [], defaultdict(list), defaultdict(list), defaultdict(list)
    for path in snap.glob("receipts/*/*/call-[0-9][0-9][0-9][0-9].json"):
        receipt = snap.json(path)
        key, attempt = path.parents[1].name, path.parent.name
        require(key in jobs, f"Receipt outside the pinned matrix: {key}")
        prompt = snap.json(path.with_name(path.stem + ".prompt.json"))
        require(digest(prompt) == receipt.get("prompt_sha256"), f"Prompt hash mismatch: {path}")
        if receipt.get("output_sha256"):
            require(digest(snap.raw(path.with_suffix(".md"))) == receipt["output_sha256"], f"Response hash mismatch: {path}")
        call = {**receipt, "job": key, "attempt": attempt, "receipt": str(path.relative_to(run)),
                "role": role(jobs[key], receipt), "user_prompt_chars": len(prompt["user"]),
                "auto_chunk_route": jobs[key]["kind"] != "judge" and len(prompt["user"]) > threshold,
                "reanchor": "(re-anchor)" in (receipt.get("label") or "")}
        calls.append(call)
        by_attempt[(key, attempt)].append(call)
        by_role[call["role"]].append(call)
        by_model[(call.get("model_requested"), call.get("model_used"))].append(call)
    attempts, failures = [], []
    for path in snap.glob("receipts/*/*/job.json"):
        record = snap.json(path)
        related = by_attempt[(record["key"], record["attempt"])]
        item = {"job": record["key"], "attempt": record["attempt"], "status": record["status"],
                "seconds": record.get("seconds"), "started_at": record.get("started_at"), "invocations": len(related),
                "error_type": record.get("error_type"), "error": record.get("error"), "failure_kind": failure_kind(record, related)}
        attempts.append(item)
        if item["failure_kind"]:
            failures.append(item)
    by_engine, pairs = defaultdict(Counter), []
    for engine in plan["definitions"]:
        for paper in ("harris", "zambrana", "chen"):
            pair_jobs = [j for j in plan["judgments"] if j["engine"] == engine and j["source"] == paper]
            winners, orders = [], []
            for job in pair_jobs:
                record = records.get(job["key"], {})
                valid = judgment_complete(job, records, snap)
                invocations = by_attempt.get((job["key"], record.get("attempt")), [])
                valid = valid and bool(invocations) and all(c.get("model_used") == plan["judge"] and c.get("status") == "complete" for c in invocations)
                winner = record.get("judgment", {}).get("winner") if valid else None
                winner = winner.split("__")[1] if winner and winner != "tie" else winner
                winners.append(winner)
                orders.append({"job": job["key"], "order": job["order"], "valid": bool(valid), "winner": winner,
                               "margin": record.get("judgment", {}).get("margin")})
            outcome = pair_outcome(winners)
            recovered = [k for k in {j[s] for j in pair_jobs for s in ("A", "B")} if records.get(k, {}).get("recovery")]
            pairs.append({"engine": engine, "paper": paper, "outcome": outcome, "recovered_parents": sorted(recovered), "orders": orders})
            by_engine[engine][outcome] += 1
    corpus = []
    for job in plan["generations"]:
        if job["kind"] != "corpus":
            continue
        key, record = job["key"], records.get(job["key"], {})
        relevant = [c for c in calls if c["job"] == key]
        # execute() persists its initial running record before run_job adds the
        # attempt ID; the attempt's own job receipt already identifies it.
        related_attempts = [a for a in attempts if a["job"] == key]
        latest_attempt = record.get("attempt") or (max(related_attempts, key=lambda a: a["started_at"] or 0)["attempt"] if related_attempts else None)
        current = by_attempt.get((key, latest_attempt), [])
        labels = Counter((c.get("label") or "").split(" | ")[1] if " | " in (c.get("label") or "") else "unknown" for c in current if not c["reanchor"])
        nominal = nominal_corpus_calls(plan, job)
        verifier = [c for c in record.get("process", {}).get("calls", []) if c.get("kind") == "verify"]
        corpus.append({"job": key, "status": record.get("status", "pending"), "latest_attempt": latest_attempt, "nominal_calls": nominal,
                       "latest_attempt_calls": len(current), "all_attempt_calls": len(relevant),
                       "latest_reanchors": sum(c["reanchor"] for c in current), "latest_calls_above_nominal": len(current) - nominal,
                       "latest_base_calls_by_step": dict(labels), "automatic_chunk_routes": sum(c["auto_chunk_route"] for c in relevant),
                       "usage": sum_calls(relevant), "final_wall": record.get("process", {}).get("final_wall", {}),
                       "verification_receipts": [{"doc": c["doc"], "wall": c["wall"]} for c in verifier]})
    check_fields = ("in", "confirmed", "carried", "weakened", "rejected", "added", "added_dropped", "unverified")
    checks, walls = [], []
    for job in plan["generations"]:
        key, record = job["key"], records.get(job["key"], {})
        valid = complete(record, snap)
        if job["condition"] == "checked" and record.get("process"):
            wall = record["process"].get("final_wall", {})
            checks.append({"job": key, "valid_final": valid, "recovered": bool(record.get("recovery")),
                           **{field: wall.get(f"check_{field}") for field in check_fields}})
        walls.append({"job": key, "condition": job["condition"], "status": record.get("status", "pending"),
                      "valid_final": valid, "recovered": bool(record.get("recovery")), "wall": record.get("wall", {}),
                      "process_final_wall": record.get("process", {}).get("final_wall", {}),
                      "source_coverage": record.get("source_coverage", {})})
    starts = [c["started_at"] for c in calls if c.get("started_at") is not None]
    ends = [c["started_at"] + c["duration_ms"] / 1000 for c in calls if c.get("started_at") is not None and c.get("duration_ms") is not None]
    result = {
        "study_identity": IDENTITY, "frozen_commit": COMMIT,
        "aggregation_script_sha256": digest(Path(__file__).read_bytes()),
        "generation_complete": sum(complete(records.get(j["key"]), snap) for j in plan["generations"]),
        "generation_planned": len(plan["generations"]),
        "judgment_complete": sum(order["valid"] for pair in pairs for order in pair["orders"]),
        "judgment_planned": len(plan["judgments"]), "logical_status_counts": dict(Counter(r.get("status") for r in records.values())),
        "recovered_jobs": sorted(k for k, r in records.items() if r.get("recovery")),
        "both_order_counts": {engine: {outcome: count[outcome] for outcome in ("old", "checked", "tie", "split", "incomplete")} for engine, count in by_engine.items()},
        "pairs": pairs, "usage_total": sum_calls(calls), "usage_by_role": {r: sum_calls(by_role[r]) for r in ("generation", "critic", "corpus", "judge")},
        "model_routes": [{"requested": requested, "used": used, **sum_calls(group)} for (requested, used), group in sorted(by_model.items(), key=lambda x: str(x[0]))],
        "timing": {"summed_original_attempt_seconds": round(sum(a["seconds"] or 0 for a in attempts), 3),
                   "unknown_attempt_duration_count": sum(a["seconds"] is None for a in attempts),
                   "recorded_activity_span_seconds": round(max(ends) - min(starts), 3) if starts and ends else None,
                   "first_invocation_utc": datetime.fromtimestamp(min(starts), timezone.utc).isoformat() if starts else None,
                   "last_completed_invocation_utc": datetime.fromtimestamp(max(ends), timezone.utc).isoformat() if ends else None},
        "failure_counts": dict(Counter(f["failure_kind"] for f in failures)), "failures": failures,
        "chunking": {"threshold_chars": threshold, "maximum_saved_user_prompt_chars": max([c["user_prompt_chars"] for c in calls] or [0]),
                     "automatic_chunk_routes": sum(c["auto_chunk_route"] for c in calls),
                     "basis": "Saved prompt lengths versus the verified frozen run_engine_call_auto threshold. Recorder omits chunked/num_chunks; internal provider request counts are not asserted."},
        "corpus": corpus, "finding_dispositions": checks,
        "finding_disposition_totals": {field: sum(c[field] or 0 for c in checks if c["valid_final"]) for field in check_fields},
        "walls": walls, "attempts": attempts,
        "caveats": [
            "Only agreeing valid Sonnet judgments in both orders count as old/checked wins or ties; splits are excluded, incomplete pairs stay incomplete.",
            "Output formatting and check receipts may reveal treatment despite A/B labels and counterbalanced order.",
            "This compares whole production treatments: original questions plus one Sol reading versus redesigned questions, method cards, synthesis brief, a Sol reading, and a DeepSeek check. It does not isolate any question's benefit or the critic's contribution.",
            "Generation includes old-question and production single-paper Sol readings; critic includes their DeepSeek checks; corpus includes the full DVS runs; judge includes Sonnet comparisons.",
            "Costs are original invocation-receipt estimates using repository prices, including failed attempts; recovery copies and process receipts are not added again. Missing usage/cost is unknown, not zero.",
            "Invocation duration includes recorder overhead. Summed original job-attempt seconds exclude idle/review gaps; recorded activity span includes gaps. Offline recovery CPU adds no model latency or billing.",
            "Requested-versus-used model mismatch is a reported fallback. Provider retries, refusals, internal attempts, or charges may not be fully represented by returned usage.",
            "Old-prompt auxiliary sections can parse as findings; old/checked row counts are not directly comparable. Anchor occurrence and wall shape are not semantic validity.",
            "Carried findings were unmentioned by the critic and are separate from confirmed findings, even when frozen rendering assigns a confirmed status. Added/dropped counts are dispositions, not an accuracy score.",
            "Corpus verify receipts expose carried/rejected/added counts unevenly; absent counters are unknown. Final wall and source coverage do not establish a valid genealogy.",
        ],
    }
    snap.verify()
    result["input_snapshot_sha256"] = digest(snap.hashes)
    result["input_file_sha256"] = snap.hashes
    return result


def markdown(report):
    lines = ["# Ideas study aggregate", "", f"Identity: `{report['study_identity']}`. Snapshot: `{report['input_snapshot_sha256']}`.",
             f"Aggregator: `{report['aggregation_script_sha256']}`.", "",
             f"Valid outputs: {report['generation_complete']}/{report['generation_planned']} generations; {report['judgment_complete']}/{report['judgment_planned']} judgments. Recovered parents: {len(report['recovered_jobs'])}.", "",
             "## Both-order agreements", "", "| Engine | Old | Checked | Tie | Split, excluded | Incomplete |", "|---|---:|---:|---:|---:|---:|"]
    for engine, counts in report["both_order_counts"].items():
        lines.append("| " + " | ".join([engine] + [str(counts[k]) for k in ("old", "checked", "tie", "split", "incomplete")]) + " |")
    lines += ["", "| Engine / paper | Old first | Checked first | Result | Recovered parent |", "|---|---|---|---|---|"]
    for p in report["pairs"]:
        orders = {o["order"]: o["winner"] or "incomplete" for o in p["orders"]}
        lines.append(f"| {p['engine']} / {p['paper']} | {orders['old_first']} | {orders['checked_first']} | {p['outcome']} | {'yes' if p['recovered_parents'] else 'no'} |")
    lines += ["", "## Invocation usage and timing", "", "| Role | Calls | Estimated USD | Input tokens | Output tokens | Invocation seconds | Unknown cost | Retry calls / count | Fallbacks |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for role_name, u in [*report["usage_by_role"].items(), ("total", report["usage_total"])]:
        lines.append(f"| {role_name} | {u['invocations']} | {u['cost_usd']:.6f} | {u['input_tokens']} | {u['output_tokens']} | {u['duration_seconds']:.3f} | {u['unknown_cost_calls']} | {u['reported_retry_calls']} / {u['reported_retry_count']} | {u['fallback_calls']} |")
    t = report["timing"]
    lines += ["", f"Summed original attempt duration: {t['summed_original_attempt_seconds']} s. Recorded activity span, including gaps: {t['recorded_activity_span_seconds']} s. Unknown attempt durations: {t['unknown_attempt_duration_count']}.", "",
              "| Requested model | Used model | Calls | Estimated USD | Unknown usage / used model |", "|---|---|---:|---:|---:|"]
    for u in report["model_routes"]:
        lines.append(f"| {u['requested']} | {u['used'] or 'unknown'} | {u['invocations']} | {u['cost_usd']:.6f} | {u['unknown_usage_calls']} / {u['unknown_model_used_calls']} |")
    lines += ["", "## Original failures", "", f"Failure classes: `{json.dumps(report['failure_counts'], sort_keys=True)}`. Failed invocation receipts: {report['usage_total']['failed']}; partial responses: {report['usage_total']['partial_responses']}."]
    for f in report["failures"]:
        lines.append(f"\n- `{f['job']}` attempt `{f['attempt']}`: {f['failure_kind']}; {f['error_type']}: {f['error']}")
    lines += ["", "## Corpus call accounting", "", "| Job | Status | Nominal | Latest calls | Reanchors | All-attempt calls | Automatic chunk routes |", "|---|---|---:|---:|---:|---:|---:|"]
    for c in report["corpus"]:
        lines.append(f"| {c['job']} | {c['status']} | {c['nominal_calls']} | {c['latest_attempt_calls']} | {c['latest_reanchors']} | {c['all_attempt_calls']} | {c['automatic_chunk_routes']} |")
    lines += ["", f"Maximum saved user prompt: {report['chunking']['maximum_saved_user_prompt_chars']} characters; frozen automatic-chunk threshold: {report['chunking']['threshold_chars']}. {report['chunking']['basis']}", "",
              "| Corpus job | Missing cited IDs | Missing lineage IDs | Incomplete cross-document rows | Verify carried counts by document |", "|---|---|---|---|---|"]
    for c in report['corpus']:
        w = c['final_wall']
        carried = '; '.join(f"{v['doc'] or 'corpus'}: {v['wall'].get('carried_forward', 'unknown')}" for v in c['verification_receipts'])
        lines.append(f"| {c['job']} | {', '.join(w.get('missing_cited', [])) or '—'} | {', '.join(w.get('missing_lineage', [])) or '—'} | {', '.join(w.get('incomplete_cross_document_ids', [])) or '—'} | {carried or 'pending'} |")
    lines += ["",
              "## Checked finding dispositions", "", "| Job | In | Confirmed | Carried | Weakened | Rejected | Added | Added dropped | Unverified retained |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for c in report["finding_dispositions"]:
        lines.append("| " + " | ".join([c['job'] + (' (recovered)' if c['recovered'] else '')] + [str(c[k]) if c[k] is not None else "unknown" for k in ("in", "confirmed", "carried", "weakened", "rejected", "added", "added_dropped", "unverified")]) + " |")
    lines.append("| Total valid finals | " + " | ".join(str(report['finding_disposition_totals'][k]) for k in ("in", "confirmed", "carried", "weakened", "rejected", "added", "added_dropped", "unverified")) + " |")
    lines += ["", "## Final wall metrics", "", "| Job | Valid final | Wall provenance | Rows verified / parsed | Anchors verified / parsed | Cross-document rows | Incomplete pairs |", "|---|---|---|---:|---:|---:|---|"]
    for entry in report["walls"]:
        w = entry["process_final_wall"] or entry["wall"]
        provenance = "process final wall" if entry["process_final_wall"] else "runner post-output wall"
        lines.append(f"| {entry['job']} | {entry['valid_final']} | {provenance} | {w.get('verified', '?')} / {w.get('rows', '?')} | {w.get('verified_anchors', '?')} / {w.get('anchors', '?')} | {w.get('cross_document_rows', '?')} | {', '.join(w.get('incomplete_cross_document_ids', [])) or '—'} |")
    lines += ["", "Process final walls retain corpus ancestry information even when a synthesis omits its dimension tag; the table prefers them where available. The JSON aggregate preserves both wall records."]
    lines += ["", "## Interpretation limits", "", *[f"- {c}" for c in report["caveats"]], ""]
    return "\n".join(lines)


def self_test():
    import tempfile
    import unittest

    class AggregateTests(unittest.TestCase):
        def test_agreement_does_not_count_split_or_incomplete(self):
            self.assertEqual(pair_outcome(["checked", "old"]), "split")
            self.assertEqual(pair_outcome(["checked", None]), "incomplete")
            self.assertEqual(pair_outcome(["tie", "tie"]), "tie")
            self.assertEqual(pair_outcome(["checked", "checked"]), "checked")

        def test_unknown_usage_and_retries_not_hidden(self):
            u = sum_calls([dict(status="complete", cost_usd=0.1, retries=2, model_requested="a", model_used="b"), dict(status="failed")])
            self.assertEqual((u['cost_usd'], u['unknown_cost_calls'], u['unknown_usage_calls']), (0.1, 1, 2))
            self.assertEqual((u['reported_retry_count'], u['fallback_calls'], u['unknown_retry_calls']), (2, 1, 1))

        def test_postprocess_distinct_from_invocation_failure(self):
            self.assertEqual(failure_kind({'status':'failed'}, [{'status':'complete'}]), 'postprocess_failure_after_complete_calls')
            self.assertEqual(failure_kind({'status':'failed'}, [{'status':'failed','partial':True}]), 'response_validation_failure')
            self.assertEqual(failure_kind({'status':'failed'}, [{'status':'failed','error_type':'TimeoutError'}]), 'invocation_or_backend_failure')

        def test_stale_or_failed_parent_invalidates_existing_judgment(self):
            with tempfile.TemporaryDirectory() as tmp:
                root, records = Path(tmp), {}
                for key in ('old', 'checked', 'judge'):
                    payload = key.encode()
                    (root / key).write_bytes(payload)
                    records[key] = {'status':'complete', 'output':key, 'output_sha256':digest(payload)}
                verdict = {'winner':'checked','margin':'clear','why':'source support'}
                payload = json.dumps(verdict).encode()
                (root / 'judge').write_bytes(payload)
                records['judge'].update(output_sha256=digest(payload),
                                        inputs_sha256={k:records[k]['output_sha256'] for k in ('old','checked')},
                                        judgment=verdict)
                job = {'key':'judge', 'A':'old', 'B':'checked'}
                self.assertTrue(judgment_complete(job, records, Snapshot(root)))
                records['judge']['judgment'] = {**verdict, 'winner':'old'}
                self.assertFalse(judgment_complete(job, records, Snapshot(root)))
                records['judge']['judgment'] = verdict
                records['checked']['status'] = 'failed'
                self.assertFalse(judgment_complete(job, records, Snapshot(root)))
                records['checked']['status'] = 'complete'
                (root / 'checked').write_bytes(b'changed')
                self.assertFalse(judgment_complete(job, records, Snapshot(root)))

        def test_snapshot_refuses_mixed_reads(self):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                p = root / 'input'
                p.write_bytes(b'first')
                snap = Snapshot(root)
                snap.raw(p)
                p.write_bytes(b'second')
                with self.assertRaises(ValueError):
                    snap.raw(p)

    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(AggregateTests))
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir', type=Path, default=DEFAULT_RUN)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--require-complete', action='store_true', help='Refuse a final report until all 28 generations and 24 judgments validate')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    report = aggregate(args.run_dir.resolve())
    if args.require_complete:
        require(report['generation_complete'] == report['generation_planned'] and
                report['judgment_complete'] == report['judgment_planned'], 'Study is not fully complete; final aggregate refused')
    print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else markdown(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
