"""Adopt the reviewed, zero-API auxiliary-section recovery after the live run ends.

Default: validate and print a preview. --adopt installs exactly two missing output
files and atomically updates results.json, retaining original failed records and
receipts. Never run this concurrently with the study runner. This script refuses
active study processes, running invocation receipts, and unexpected pending judges.
It does not launch judgments or any other model call.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
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

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "data/study/ideas_2026_09_05/374325c24e6b10a1"
BUNDLE = RUN / "reader_notes/auxiliary_recovery/20260905T045321.120955Z"
ACCEPTED_MANIFEST_SHA256 = "84b58c975f296dc7c72cb49baacb23e631a06d622c6b6192cf01da4e5f394195"
ACCEPTED_TRANSFORMATION_SHA256 = "926acdc0df324d71daf82eb80e99d8ca5fdc0931c58b824cbd0ae5bcc95ef9ac"
IDENTITY = "374325c24e6b10a15663e9cbe9fd3520818964bc05f8f46b2d88944e0b7cbfca"
COMMIT = "c19513884a5453f54073e38cbabf2c6e7d5cfd28"
TARGETS = {"argument_architecture__checked__chen": "8ac1816319a7",
           "epistemological_method_detector__checked__harris": "a9c7c8d11194"}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def require_snapshot(path, expected):
    require(path.read_bytes() == expected, f"Concurrent modification detected: {path}")


def billing_receipts_hash():
    receipts = {str(p.relative_to(RUN)): sha(p.read_bytes()) for p in sorted(
        (RUN / "receipts").glob("*/*/call-[0-9][0-9][0-9][0-9].json"))}
    return sha(json.dumps(receipts, sort_keys=True).encode())


def require_idle(run_dir=RUN, process_root=Path("/proc")):
    require(process_root.is_dir(), "Process inspection unavailable; cannot establish an idle study")
    active = []
    for process in process_root.iterdir():
        if not process.name.isdigit() or int(process.name) == os.getpid():
            continue
        try:
            command = (process / "cmdline").read_bytes().split(b"\0")
        except FileNotFoundError:
            continue
        except PermissionError as exc:
            raise RuntimeError(f"Cannot inspect process {process.name}; refusing adoption") from exc
        if any(Path(os.fsdecode(part)).name == "study_ideas_material.py" for part in command if part):
            active.append(process.name)
    require(not active, f"Study runner process still active: PIDs {', '.join(active)}")
    results = json.loads((run_dir / "results.json").read_bytes())
    require(not any(r.get("status") == "running" for r in results.values()), "A study result is still running")
    for path in (run_dir / "receipts").glob("*/*/call-[0-9][0-9][0-9][0-9].json"):
        require(json.loads(path.read_bytes()).get("status") != "running", f"An invocation is still running: {path}")


def load_recovery():
    manifest_raw = (BUNDLE / "manifest.json").read_bytes()
    require(sha(manifest_raw) == ACCEPTED_MANIFEST_SHA256, "Reviewed recovery manifest changed")
    manifest = json.loads(manifest_raw)
    helper_path = BUNDLE / "recover_auxiliary_sections.py"
    require(sha(helper_path.read_bytes()) == ACCEPTED_TRANSFORMATION_SHA256 == manifest["transformation_code_sha256"],
            "Reviewed transformation code changed")
    require(manifest["plan_identity"] == IDENTITY and manifest["frozen_commit"] == COMMIT,
            "Recovery belongs to a different plan or runtime")
    require(manifest["status"] == "recovered_with_all_currently_complete_checked_outputs_unchanged" and
            manifest["completed_checked_compared"] == 10 and manifest["recovered_failed_jobs"] == 2 and
            manifest["skipped_incomplete"] == [], "Recovery equivalence comparison is incomplete")
    require(sha((BUNDLE / "results.snapshot.json").read_bytes()) == manifest["results_snapshot_sha256"],
            "Original recovery results snapshot changed")
    spec = importlib.util.spec_from_file_location("reviewed_ideas_recovery", helper_path)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    return manifest, helper


def prepare():
    require_idle()
    started = time.perf_counter()
    manifest, helper = load_recovery()
    plan_raw, before = (RUN / "plan.json").read_bytes(), (RUN / "results.json").read_bytes()
    plan, records = json.loads(plan_raw), json.loads(before)
    require(sha(plan_raw) == manifest["plan_file_sha256"] and plan["identity"] == IDENTITY and
            helper.digest({k: v for k, v in plan.items() if k != "identity"}) == IDENTITY,
            "Live plan differs from the reviewed recovery plan")
    for filename, expected in plan["code_sha256"].items():
        require(sha((ROOT / filename).read_bytes()) == expected, f"Judge-resume runtime has changed: {filename}")
    for key, entry in manifest["jobs"].items():
        record = records.get(key, {})
        if key in TARGETS:
            original_job = entry["original_job"]
            job_meta = next(j for j in plan["generations"] if j["key"] == key)
            require(record.get("status") == "failed" and record.get("attempt") == TARGETS[key] and
                    original_job == {**job_meta, **record}, f"Original failed result changed: {key}")
            attempt = RUN / "receipts" / key / record["attempt"]
            require(sha((attempt / "job.json").read_bytes()) == entry["original_job_sha256"], f"Failed job receipt changed: {key}")
            require(not (RUN / "outputs" / f"{key}.md").exists(), f"Refusing to overwrite an existing output: {key}")
        else:
            require(entry.get("byte_identical_to_baseline") is True and record.get("status") == "complete" and
                    record.get("output_sha256") == entry["output_sha256"] and
                    sha((RUN / record["output"]).read_bytes()) == entry["output_sha256"],
                    f"Previously compared completed output changed: {key}")
    archive = subprocess.run(["git", "archive", COMMIT, "src", "scripts"], cwd=ROOT,
                             check=True, stdout=subprocess.PIPE).stdout
    sys.addaudithook(helper.no_network)
    proposed, payloads, verifications = copy.deepcopy(records), {}, {}
    with tempfile.TemporaryDirectory(prefix="ideas-adoption-frozen-") as tmp:
        frozen = Path(tmp)
        with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
            bundle.extractall(frozen, filter="data")
        for filename, expected in plan["code_sha256"].items():
            require(sha((frozen / filename).read_bytes()) == expected, f"Frozen code mismatch: {filename}")
        sys.path.insert(0, str(frozen))
        sys.dont_write_bytecode = True
        for key, value in plan["runtime"].items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        from scripts import study_ideas_material as study
        from src.executor import process_runner as pr
        require(Path(pr.__file__).is_relative_to(frozen), "Runtime was not loaded from the frozen archive")
        fresh, sources = study.build_plan(ROOT / "data/study/sources_ideas")
        require(fresh["identity"] == IDENTITY and helper.digest(fresh) == helper.digest(plan), "Exact plan reconstruction failed")
        for key in TARGETS:
            entry, original = manifest["jobs"][key], records[key]
            artifact = BUNDLE / entry["output"]
            payload = artifact.read_bytes()
            require(sha(payload) == entry["output_sha256"], f"Recovered artifact changed: {key}")
            job = next(j for j in plan["generations"] if j["key"] == key)
            documents = sources[job["source"]]
            attempt = RUN / "receipts" / key / original["attempt"]
            replay, calls, cpu, error = helper.replay(pr, study, job, documents, attempt, pr._ledger_text, True)
            require(error is None and replay.final_content.encode() == payload, f"Exact saved-call recovery no longer reproduces {key}: {error}")
            require(calls == entry["calls"] and replay.receipts() == entry["replay_process"],
                    f"Original saved call/step receipts changed: {key}")
            # Exactly the unchanged study runner's final single-paper wall/coverage.
            _, ledger = study.split_ledger(payload.decode())
            rows = study.parse_rows(ledger.split("### Rejected by the critic")[0])
            require(bool(rows), f"Recovered output has no ledger: {key}")
            wall = study.verify_rows(rows, study.SourceIndex(documents)).as_dict()
            coverage = {"expected": list(documents), "verified": sorted({a.verified_doc for r in rows for a in r.anchors if a.verified and a.verified_doc})}
            output = f"outputs/{key}.md"
            updated = copy.deepcopy(original)
            updated.update(status="complete", output=output, output_sha256=sha(payload), process=replay.receipts(),
                           wall=wall, source_coverage=coverage, seconds_basis="original failed attempt elapsed; offline CPU recorded separately")
            updated.pop("error", None)
            updated.pop("error_type", None)
            updated["recovery"] = {
                "kind": "offline_auxiliary_section_recovery", "original_failed_record": original,
                "original_failed_job_sha256": entry["original_job_sha256"],
                "original_failed_attempt_seconds": original["seconds"],
                "original_receipts_unchanged": True, "api_calls_added": 0, "cost_usd_added": 0,
                "offline_recovery_cpu_seconds": entry["cpu_recovery_seconds"], "adoption_validation_cpu_seconds": round(cpu, 6),
                "manifest": str((BUNDLE / "manifest.json").relative_to(RUN)),
                "manifest_sha256": ACCEPTED_MANIFEST_SHA256, "transformation_code_sha256": ACCEPTED_TRANSFORMATION_SHA256,
                "raw_response_sha256": [c["response_sha256"] for c in entry["calls"]],
                "recovered_artifact_sha256": sha(payload), "plan_identity": IDENTITY, "frozen_commit": COMMIT,
            }
            proposed[key], payloads[output] = updated, payload
            verifications[key] = {"wall": wall, "source_coverage": coverage, "output_sha256": sha(payload)}
        expected_missing = {j["key"] for j in plan["judgments"] if j["A"] in TARGETS or j["B"] in TARGETS}
        actual_missing = {j["key"] for j in plan["judgments"] if not study.job_completed(j, records, RUN)}
        require(len(expected_missing) == 4 and actual_missing == expected_missing,
                f"Expected only the four recovery-dependent judgments to remain; actual pending: {sorted(actual_missing)}")
        require(all(study.completed(records.get(j[side]), RUN) for j in plan["judgments"]
                    for side in ("A", "B") if j[side] not in TARGETS), "An unchanged judgment input is incomplete")
        billing = study.receipts_summary(RUN)
        receipts_hash = billing_receipts_hash()
    require_idle()
    require_snapshot(RUN / "plan.json", plan_raw)
    require_snapshot(RUN / "results.json", before)
    return {"before": before, "plan_raw": plan_raw, "proposed": proposed, "payloads": payloads,
            "verifications": verifications, "pending_judgments": sorted(expected_missing), "billing_before": billing,
            "billing_receipts_sha256": receipts_hash,
            "validation_cpu_seconds": round(time.perf_counter() - started, 6)}


def adopt(prepared):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    folder = RUN / "reader_notes/auxiliary_recovery/adoptions" / stamp
    folder.mkdir(parents=True, exist_ok=False)
    before = prepared["before"]
    (folder / "results.before.json").write_bytes(before)
    report = {"status": "staged", "created_at": stamp, "plan_identity": IDENTITY,
              "adoption_script_sha256": sha(Path(__file__).read_bytes()), "recovery_manifest_sha256": ACCEPTED_MANIFEST_SHA256,
              "results_before_sha256": sha(before), "api_calls_added": 0, "cost_usd_added": 0,
              **{k: prepared[k] for k in ("verifications", "pending_judgments", "billing_before", "billing_receipts_sha256", "validation_cpu_seconds")}}
    installed = []
    try:
        for key in TARGETS:
            prepared["proposed"][key]["recovery"].update(adopted_at=stamp, adoption_manifest=str((folder / "manifest.json").relative_to(RUN)))
        after = json_bytes(prepared["proposed"])
        (folder / "results.after.json").write_bytes(after)
        report["results_after_sha256"] = sha(after)
        for relative, payload in prepared["payloads"].items():
            (folder / Path(relative).name).write_bytes(payload)
        require_idle()
        require_snapshot(RUN / "plan.json", prepared["plan_raw"])
        require_snapshot(RUN / "results.json", before)
        require(billing_receipts_hash() == prepared["billing_receipts_sha256"], "Billing receipts changed after validation")
        # Hard-link creation is atomic and refuses an existing destination.
        # No baseline output can be replaced, even if another writer races us.
        for relative in prepared["payloads"]:
            destination = RUN / relative
            os.link(folder / Path(relative).name, destination)
            installed.append(destination)
        require_idle()
        require_snapshot(RUN / "results.json", before)
        with tempfile.NamedTemporaryFile(dir=RUN, prefix=".recovery-results-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(after)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            require_snapshot(RUN / "results.json", before)
            require(billing_receipts_hash() == prepared["billing_receipts_sha256"], "Billing receipts changed before adoption")
            os.replace(temporary, RUN / "results.json")
        finally:
            temporary.unlink(missing_ok=True)
        report["status"] = "adopted"
        report["original_failed_job_receipts_preserved"] = True
        report["billing_receipts_unchanged"] = billing_receipts_hash() == prepared["billing_receipts_sha256"]
    except Exception as exc:
        report.update(status="refused_or_incomplete", error_type=type(exc).__name__, error=str(exc))
        # Remove only links created by this attempt, only while results is unchanged.
        if (RUN / "results.json").read_bytes() == before:
            for destination in installed:
                if destination.exists() and os.path.samefile(destination, folder / destination.name):
                    destination.unlink()
        raise
    finally:
        (folder / "manifest.json").write_bytes(json_bytes(report))
        print(f"Adoption audit: {folder}")
    return folder


def self_test():
    import unittest

    class Guards(unittest.TestCase):
        def test_snapshot_and_existing_output_refusal(self):
            with tempfile.TemporaryDirectory() as tmp:
                p = Path(tmp) / "results.json"
                p.write_bytes(b"original")
                require_snapshot(p, b"original")
                p.write_bytes(b"concurrent")
                with self.assertRaises(RuntimeError):
                    require_snapshot(p, b"original")
                q = Path(tmp) / "staged"
                q.write_bytes(b"replacement")
                with self.assertRaises(FileExistsError):
                    os.link(q, p)
                self.assertEqual(p.read_bytes(), b"concurrent")

        def test_live_process_result_and_invocation_refusal(self):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                proc = root / "proc"
                proc.mkdir()
                (root / "results.json").write_text('{}')
                require_idle(root, proc)
                process = proc / "99999999"
                process.mkdir()
                (process / "cmdline").write_bytes(b'python\0scripts/study_ideas_material.py\0--run\0')
                with self.assertRaises(RuntimeError):
                    require_idle(root, proc)
                (process / "cmdline").write_bytes(b'other-process\0')
                (root / "results.json").write_text('{"job":{"status":"running"}}')
                with self.assertRaises(RuntimeError):
                    require_idle(root, proc)
                (root / "results.json").write_text('{}')
                receipt = root / "receipts/job/attempt/call-0001.json"
                receipt.parent.mkdir(parents=True)
                receipt.write_text('{"status":"running"}')
                with self.assertRaises(RuntimeError):
                    require_idle(root, proc)

    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Guards))
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--adopt", action="store_true")
    modes.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    # Cooperating adoption processes share a lock; the study runner is separately
    # required to be absent because the frozen runner does not participate in it.
    lock_path = RUN / "reader_notes/auxiliary_recovery/adoption.lock"
    with lock_path.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        prepared = prepare()
        print(json.dumps({"mode": "adopt" if args.adopt else "preview", "outputs": prepared["verifications"],
                          "pending_judgments": prepared["pending_judgments"], "api_calls_added": 0}, indent=2))
        if args.adopt:
            adopt(prepared)
        else:
            print("Preview only. After reviewing it, repeat with --adopt while the study remains idle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
