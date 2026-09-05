"""Ideas-material checks 1–3; no API calls unless --run is explicitly supplied.

  python scripts/study_ideas_material.py --dry-run
  python scripts/study_ideas_material.py --run --budget-usd 20  # after spend approval
  python scripts/study_ideas_material.py --report

Successful jobs resume only with matching source, definition, routing, code and output
hashes. Failed jobs retry in full; every attempt keeps its invocation receipts, including
responses rejected as partial and failed judgments. Historical attempt costs count
towards the budget. The limit gates new calls on known token-cost estimates; provider
retries/errors can incur unreported charges, and a call already in flight can exceed it.
Corpus readings require a human memo and are never entered into pairwise judging.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.study_two_engines import PAIR, old_prompt  # noqa: E402
from src.engines.registry import get_engine_registry  # noqa: E402
from src.events.pricing import PRICING, estimate_cost  # noqa: E402
from src.executor.context_broker import split_ledger  # noqa: E402
from src.executor.engine_runner import run_engine_call, run_engine_call_auto  # noqa: E402
from src.executor.ledger_walls import SourceIndex, parse_rows, verify_rows  # noqa: E402
from src.executor.process_runner import run_oneshot_checked, run_process  # noqa: E402
from src.llm.client import parse_llm_json_response  # noqa: E402

from src.operationalizations.registry import get_operationalization_registry  # noqa: E402

ENGINES = (
    "conditions_of_possibility_analyzer", "argument_architecture",
    "inferential_commitment_mapper", "epistemological_method_detector",
)
CORPUS_ENGINES = (ENGINES[0], ENGINES[2])
PAPERS = {
    "harris": "harris2026_eight_arguments_against_honneth.txt",
    "zambrana": "zambrana2025_philosophy_in_the_severe_style_rose.txt",
    "chen": "chen2025_progress_without_progress_jaeggi.txt",
}
CORPORA = {
    "deutschmann": (
        "deutschmann2001_capitalism_as_religion.md",
        "deutschmann2001_promise_of_absolute_wealth.md",
        "deutschmann2022_interpretation_of_capitalism_as_religion.md",
    ),
    "castoriadis": (
        "castoriadis1984_technique.md", "castoriadis1990_what_democracy.md",
        "castoriadis1997_rationality_of_capitalism.md",
    ),
}
ROUTING = {
    "cheap": "openrouter/openai/gpt-5.6-luna",
    "mid": "openrouter/deepseek/deepseek-v4-pro",
    "strong": "openrouter/openai/gpt-5.6-sol",
}
JUDGE = "claude-sonnet-4-6"
DEFAULT_SOURCES = ROOT / "data/study/sources_ideas"
DEFAULT_OUT = ROOT / "data/study/ideas_2026_09_05"
CODE_FILES = (
    "scripts/study_ideas_material.py", "scripts/study_two_engines.py",
    "src/stages/process_composer.py", "src/executor/process_runner.py",
    "src/executor/ledger_walls.py", "src/executor/context_broker.py",
    "src/executor/engine_runner.py", "src/llm/backends.py",
    "src/events/pricing.py", "src/operationalizations/schemas.py",
)


def digest(value) -> str:
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def generation_jobs() -> list[dict]:
    jobs = [
        {"key": f"{engine}__{condition}__{paper}", "engine": engine,
         "source": paper, "condition": condition, "kind": "single"}
        for engine in ENGINES for paper in PAPERS for condition in ("old", "checked")
    ]
    jobs += [
        {"key": f"{engine}__deep__{corpus}", "engine": engine,
         "source": corpus, "condition": "deep", "kind": "corpus"}
        for engine in CORPUS_ENGINES for corpus in CORPORA
    ]
    return jobs


def judgment_jobs() -> list[dict]:
    return [
        {"key": f"judge__{engine}__{paper}__{order}", "engine": engine,
         "source": paper, "kind": "judge", "order": order,
         "A": f"{engine}__{a}__{paper}", "B": f"{engine}__{b}__{paper}"}
        for engine in ENGINES for paper in PAPERS
        for order, a, b in (("old_first", "old", "checked"), ("checked_first", "checked", "old"))
    ]


def build_plan(source_dir: Path = DEFAULT_SOURCES) -> tuple[dict, dict]:
    """Read local inputs and pin the complete experiment; never call a model or write."""
    sources, metadata = {}, {}
    for name, filenames in {**{k: (v,) for k, v in PAPERS.items()}, **CORPORA}.items():
        documents = {}
        for filename in filenames:
            path = source_dir / filename
            raw = path.read_bytes()
            text = raw.decode("utf-8")
            if not text.strip():
                raise ValueError(f"Empty study source: {path}")
            # Stable document keys preserve the two distinct Deutschmann 2001 papers.
            doc = Path(filename).stem
            documents[doc] = text
            metadata[doc] = {"file": filename, "sha256": digest(raw), "chars": len(text)}
        sources[name] = documents
    definitions = {}
    for engine in ENGINES:
        cap = get_engine_registry().get_capability_definition(engine)
        op = get_operationalization_registry().get(engine)
        if not cap or not op or not op.process:
            raise ValueError(f"Missing capability/process definition for {engine}")
        modes = {x.depth_key: x.mode or x.process for x in op.depth_sequences}
        if modes.get("standard") != "oneshot_checked" or modes.get("deep") != "dvs":
            raise ValueError(f"Production modes changed for {engine}: {modes}")
        if op.process.routing != ROUTING:
            raise ValueError(f"Production routing changed for {engine}; review the study routing")
        definitions[engine] = {"capability": cap.model_dump(mode="json"), "operationalization": op.model_dump(mode="json")}
    base_calls = 12 + 12 * 2 + 24
    for engine in CORPUS_ENGINES:
        dims = definitions[engine]["operationalization"]["process"]["dimensions"]
        base_calls += len(CORPORA) * (3 * sum(d["scope"] == "document" for d in dims)
                                     + sum(d["scope"] == "corpus" for d in dims) + 4 + 1)
    identity = {
        "study": "ideas_material_2026_09_05", "version": 1,
        "sources": metadata, "source_groups": {k: list(v) for k, v in sources.items()},
        "definitions": definitions, "routing": ROUTING, "judge": JUDGE,
        "code_sha256": {p: digest((ROOT / p).read_bytes()) for p in CODE_FILES},
        "pricing": PRICING,
        "runtime": {key: os.environ.get(key) for key in (
            "ENABLE_STREAMING", "LLM_SYNC_HARD_TIMEOUT_SECONDS", "OPENROUTER_REASONING_EFFORT",
        )},
        "generations": generation_jobs(), "judgments": judgment_jobs(),
        "base_calls": base_calls, "extract_parallelism": 1,
    }
    return {"identity": digest(identity), **identity}, sources


def completed(record: dict | None, output_dir: Path) -> bool:
    if not record or record.get("status") != "complete":
        return False
    path = output_dir / record["output"]
    if not path.is_file() or digest(path.read_bytes()) != record.get("output_sha256"):
        return False
    for key, expected in record.get("inputs_sha256", {}).items():
        dependency = output_dir / "outputs" / f"{key}.md"
        if not dependency.is_file() or digest(dependency.read_bytes()) != expected:
            return False
    return True


def job_completed(job: dict, results: dict, output_dir: Path) -> bool:
    return completed(results.get(job["key"]), output_dir) and (
        job["kind"] != "judge" or all(completed(results.get(job[side]), output_dir) for side in ("A", "B"))
    )


class BudgetReached(RuntimeError):
    pass


def receipts_summary(output_dir: Path) -> dict:
    receipts = [read_json(p, {}) for p in (output_dir / "receipts").glob("*/*/call-[0-9][0-9][0-9][0-9].json")]
    return {
        "calls": len(receipts),
        "cost_usd": round(sum(r.get("cost_usd") or 0 for r in receipts), 6),
        "input_tokens": sum(r.get("input_tokens") or 0 for r in receipts),
        "output_tokens": sum(r.get("output_tokens") or 0 for r in receipts),
        "uncosted_calls": sum(r.get("cost_usd") is None for r in receipts),
        "retry_calls": sum(bool(r.get("retries")) for r in receipts),
        "failed_calls": sum(r.get("status") != "complete" for r in receipts),
    }


class Recorder:
    """Persist each invocation, including reanchors and calls completed before a later error."""

    def __init__(self, output_dir: Path, attempt_dir: Path, budget_usd: float, *, judge: bool = False):
        self.output_dir, self.attempt_dir, self.budget_usd = output_dir, attempt_dir, budget_usd
        self.judge, self.counter = judge, 0

    def __call__(self, system_prompt: str, user_message: str, **kwargs) -> dict:
        if receipts_summary(self.output_dir)["cost_usd"] >= self.budget_usd:
            raise BudgetReached(f"Known token-cost estimate reached ${self.budget_usd:.2f}; no new call launched")
        self.counter += 1
        path = self.attempt_dir / f"call-{self.counter:04d}.json"
        model = kwargs["model_hint"]
        receipt = {"status": "running", "model_requested": model, "label": kwargs.get("label"),
                   "prompt_sha256": digest({"system": system_prompt, "user": user_message}),
                   "cost_usd": None, "started_at": time.time()}
        write_json(path.with_name(path.stem + ".prompt.json"), {"system": system_prompt, "user": user_message})
        write_json(path, receipt)
        try:
            call = run_engine_call if self.judge else run_engine_call_auto
            res = call(system_prompt=system_prompt, user_message=user_message, phase_number=1.0, **kwargs)
            content = res.get("content") or ""
            path.with_suffix(".md").write_text(content, encoding="utf-8")
            used = res.get("model_used") or model
            # Missing usage is unknown spend, never a free invocation.
            usage_known = res.get("input_tokens") is not None and res.get("output_tokens") is not None
            receipt.update({k: res.get(k) for k in (
                "input_tokens", "output_tokens", "thinking_tokens", "retries", "partial", "stop_reason",
            )})
            receipt.update(model_used=used, output_sha256=digest(content.encode()),
                           cost_usd=estimate_cost(used, res["input_tokens"], res["output_tokens"]) if usage_known else None)
            if not content.strip() or res.get("partial") or res.get("stop_reason") in ("length", "max_tokens"):
                raise ValueError("Model returned empty or partial output; retained for inspection")
            receipt["status"] = "complete"
            return res
        except Exception as exc:
            receipt.update(status="failed", error_type=type(exc).__name__, error=str(exc))
            raise
        finally:
            receipt["duration_ms"] = round((time.time() - receipt["started_at"]) * 1000)
            write_json(path, receipt)


def parse_judgment(content: str, job: dict) -> dict:
    parsed = parse_llm_json_response(content)
    if not isinstance(parsed, dict) or parsed.get("winner") not in ("A", "B", "tie"):
        raise ValueError("Judge must return one JSON object with winner A, B, or tie")
    if parsed.get("margin") not in ("slight", "clear", "decisive") or not isinstance(parsed.get("why"), str) or not parsed["why"].strip():
        raise ValueError("Judge must supply a supported margin and a nonempty reason")
    return {**parsed, "winner": job[parsed["winner"]] if parsed["winner"] != "tie" else "tie"}


def run_job(job: dict, documents: dict, output_dir: Path, record: dict, budget_usd: float) -> dict:
    attempt = uuid.uuid4().hex[:12]
    attempt_dir = output_dir / "receipts" / job["key"] / attempt
    record.update(status="running", attempt=attempt, started_at=time.time())
    write_json(attempt_dir / "job.json", {**job, **record})
    invoke = Recorder(output_dir, attempt_dir, budget_usd, judge=job["kind"] == "judge")
    try:
        if job["kind"] == "judge":
            texts = [(output_dir / "outputs" / f"{job[side]}.md").read_text(encoding="utf-8") for side in ("A", "B")]
            record["inputs_sha256"] = {job[side]: digest(text.encode()) for side, text in zip(("A", "B"), texts)}
            source = "\n\n".join(f"SOURCE [{doc}]:\n\n{text}" for doc, text in documents.items())
            user = f"{source}\n\n=====\n\nANALYSIS A:\n\n{texts[0]}\n\n=====\n\nANALYSIS B:\n\n{texts[1]}"
            res = invoke(PAIR, user, model_hint=JUDGE, depth="standard", label=f"ideas {job['key']}")
            judgment = parse_judgment(res["content"], job)
            if res.get("model_used", JUDGE) != JUDGE:
                raise ValueError("Judgment was not generated by the specified Sonnet judge")
            content = json.dumps(judgment, indent=2, ensure_ascii=False)
            record["judgment"] = judgment
        else:
            cap = get_engine_registry().get_capability_definition(job["engine"])
            spec = get_operationalization_registry().get(job["engine"]).process
            if job["condition"] == "old":
                source = "\n\n".join(f"SOURCE [{doc}]:\n\n{text}" for doc, text in documents.items())
                res = invoke(old_prompt(cap), source, model_hint=ROUTING["strong"], depth="standard", label=f"ideas {job['key']}")
                content = res["content"]
            else:
                def on_call(call):
                    # Wall metadata complements the per-invocation receipts; costs are counted only there.
                    name = f"step-{call.step_key}-{call.dimension_key}-{call.doc_key}"
                    write_json(attempt_dir / f"{name}.json", call.as_receipt())
                runner = run_process if job["kind"] == "corpus" else run_oneshot_checked
                options = {"parallelism": 1} if job["kind"] == "corpus" else {}
                result = runner(cap, spec, documents, depth="deep" if job["kind"] == "corpus" else "standard",
                                tier_overrides=ROUTING, call_fn=invoke, on_call=on_call, **options)
                content = result.final_content
                record["process"] = result.receipts()
                if job["condition"] == "checked" and not result.calls_for("check"):
                    raise ValueError("Production reading had no check call; not a completed checked run")
            _, ledger = split_ledger(content)
            rows = parse_rows(ledger.split("### Rejected by the critic")[0])
            if not content.strip() or not rows:
                raise ValueError("Reading has no findings ledger; output retained in invocation receipts")
            corpus_dims = [d.key for d in spec.dimensions if d.scope == "corpus"] if job["kind"] == "corpus" else []
            record["wall"] = verify_rows(rows, SourceIndex(documents), corpus_dimensions=corpus_dims).as_dict()
            record["source_coverage"] = {
                "expected": list(documents),
                "verified": sorted({a.verified_doc for row in rows for a in row.anchors if a.verified and a.verified_doc}),
            }
        relative = Path("outputs") / f"{job['key']}.md"
        path = output_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        record.update(status="complete", output=str(relative), output_sha256=digest(path.read_bytes()))
        record.pop("error", None)
    except BudgetReached as exc:
        record.update(status="budget_stopped", error=str(exc))
    except Exception as exc:
        record.update(status="failed", error_type=type(exc).__name__, error=str(exc))
    finally:
        record["seconds"] = round(time.time() - record["started_at"], 2)
        write_json(attempt_dir / "job.json", {**job, **record})
    return record


def agreement(engine: str, paper: str, results: dict, output_dir: Path) -> str:
    jobs = [j for j in judgment_jobs() if j["engine"] == engine and j["source"] == paper]
    records = [results.get(j["key"], {}) for j in jobs]
    if not all(job_completed(job, results, output_dir) for job in jobs):
        return "incomplete"
    winners = [r["judgment"]["winner"] for r in records]
    if winners[0] != winners[1]:
        return "split (excluded)"
    return "tie (both orders)" if winners[0] == "tie" else winners[0].split("__")[1]


def report(plan: dict, results: dict, output_dir: Path) -> str:
    total = receipts_summary(output_dir)
    jobs = plan["generations"] + plan["judgments"]
    done = sum(job_completed(j, results, output_dir) for j in jobs)
    failed = sum(results.get(j["key"], {}).get("status") == "failed" for j in jobs)
    lines = ["# Ideas-material study", "", f"Identity: `{plan['identity']}`", "",
             f"Complete {done}/{len(jobs)}; failed {failed}; pending, stale or stopped {len(jobs) - done - failed}.",
             f"Known token-cost estimate across all attempts: ${total['cost_usd']:.4f}; "
             f"{total['input_tokens']:,} input / {total['output_tokens']:,} output tokens; "
             f"{total['calls']} invocations; {total['uncosted_calls']} with unknown cost; "
             f"{total['retry_calls']} reporting retries; {total['failed_calls']} unsuccessful or interrupted.", "",
             "Cost is an estimate from repository prices. Retry/fallback/error charges may be absent from provider usage.", "",
             "## Single-paper comparisons", "", "Only agreement on both Sonnet orders counts as a result. Splits are excluded.", "",
             "| Engine | Paper | Both-order result |", "|---|---|---|"]
    for engine in ENGINES:
        for paper in PAPERS:
            lines.append(f"| {engine} | {paper} | {agreement(engine, paper, results, output_dir)} |")
    lines += ["", "## Reading receipts", "",
              "| Reading | Verified rows | Verified anchors | Cross-document rows / incomplete | Sources with matching quotes | Missing cited ids | Missing lineage ids |",
              "|---|---|---|---|---|---|---|"]
    for job in plan["generations"]:
        record = results.get(job["key"], {})
        if not completed(record, output_dir):
            continue
        final_wall = record.get("process", {}).get("final_wall", {})
        # The process also knows which rows descend from corpus findings. Its wall
        # catches lost pairs even if synthesis omitted the corpus dimension tag.
        wall = final_wall or record.get("wall", {})
        coverage = record.get("source_coverage", {})
        cited = ', '.join(final_wall['missing_cited']) or 'none' if 'missing_cited' in final_wall else 'not checked'
        lineage = ', '.join(final_wall['missing_lineage']) or 'none' if 'missing_lineage' in final_wall else 'not checked'
        lines.append(f"| {job['key']} | {wall.get('verified', 0)}/{wall.get('rows', 0)} | "
                     f"{wall.get('verified_anchors', 0)}/{wall.get('anchors', 0)} | "
                     f"{wall.get('cross_document_rows', 0)} / {len(wall.get('incomplete_cross_document_ids', []))} | "
                     f"{len(coverage.get('verified', []))}/{len(coverage.get('expected', []))} | "
                     f"{cited} | {lineage} |")
    lines += ["", "## All jobs", "", "| Job | Status | Output |", "|---|---|---|"]
    for job in jobs:
        record = results.get(job["key"], {})
        status = record.get("status", "pending")
        if status == "complete" and not job_completed(job, results, output_dir):
            status = "stale/missing output"
        link = f"[read]({record['output']})" if job_completed(job, results, output_dir) else ""
        lines.append(f"| {job['key']} | {status} | {link} |")
        if record.get("error"):
            lines.append(f"\n{job['key']}: {record['error']}\n")
    lines += ["", "## Reader review still required", "",
              "- Epistemology: Zambrana's method as object; whose testimony Chen credits. Write the two-page engine memo.",
              "- Commitments: what accepting Harris's eight arguments commits the reader to. Write the two-page engine memo.",
              "- Each corpus reading: inspect P6/X6 rows and both doc-keyed anchors in the step receipts; read the synthesis as a genealogy. No pairwise baseline exists.",
              "- Use these readings as tweak input before approving definition changes.", ""]
    return "\n".join(lines)


def execute(plan: dict, sources: dict, output_dir: Path, budget_usd: float, phase: str = "all") -> dict:
    previous_plan = read_json(output_dir / "plan.json", {})
    if previous_plan and previous_plan["identity"] != plan["identity"]:
        raise ValueError("Existing output directory belongs to a different study identity")
    write_json(output_dir / "plan.json", plan)
    results = read_json(output_dir / "results.json", {})
    jobs = (plan["generations"] if phase != "judge" else []) + (plan["judgments"] if phase != "generate" else [])
    for job in jobs:
        if job_completed(job, results, output_dir):
            continue
        if job["kind"] == "judge" and not all(completed(results.get(job[s]), output_dir) for s in ("A", "B")):
            results[job["key"]] = {"status": "blocked", "error": "Both generation outputs must be complete"}
        elif receipts_summary(output_dir)["cost_usd"] >= budget_usd:
            break
        else:
            results[job["key"]] = {"status": "running"}
            write_json(output_dir / "results.json", results)
            print(f"Running {job['key']}", flush=True)
            results[job["key"]] = run_job(job, sources[job["source"]], output_dir, results[job["key"]], budget_usd)
            print(f"  {results[job['key']]['status']}", flush=True)
        write_json(output_dir / "results.json", results)
        (output_dir / "REPORT.md").write_text(report(plan, results, output_dir), encoding="utf-8")
        if results[job["key"]]["status"] == "budget_stopped":
            break
    write_json(output_dir / "results.json", results)
    (output_dir / "REPORT.md").write_text(report(plan, results, output_dir), encoding="utf-8")
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--run", action="store_true", help="Launch API calls only after spend approval")
    modes.add_argument("--dry-run", action="store_true", help="Default: list the full matrix without calls or writes")
    modes.add_argument("--report", action="store_true", help="Rebuild the local report; no API calls")
    parser.add_argument("--budget-usd", type=float, help="Required with --run; cumulative known-cost gate for this identity")
    parser.add_argument("--phase", choices=("all", "generate", "judge"), default="all")
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT, help="Results go in a study-identity subdirectory")
    args = parser.parse_args(argv)
    if args.run and (args.budget_usd is None or not 0 < args.budget_usd < float("inf")):
        parser.error("--run requires a positive, finite --budget-usd approved by the owner")
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env", override=False)
    plan, sources = build_plan(args.source_dir)
    output_dir = args.output_dir / plan["identity"][:16]
    print(f"Study identity: {plan['identity']}\nOutput: {output_dir}")
    if args.run:
        results = execute(plan, sources, output_dir, args.budget_usd, args.phase)
        selected = (plan["generations"] if args.phase != "judge" else []) + (plan["judgments"] if args.phase != "generate" else [])
        print(report(plan, results, output_dir))
        return 0 if all(job_completed(j, results, output_dir) for j in selected) else 1
    if args.report:
        results = read_json(output_dir / "results.json", {})
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "REPORT.md").write_text(report(plan, results, output_dir), encoding="utf-8")
        print(report(plan, results, output_dir))
        return 0
    print(f"DRY RUN: {len(plan['generations'])} generations, {len(plan['judgments'])} Sonnet judgments; "
          f"{plan['base_calls']} planned base calls before reanchors, retries and fallbacks.\n"
          f"Routing: {json.dumps(ROUTING)}\nNo API calls or files written. Corpus readings need human memos.")
    for job in plan["generations"] + plan["judgments"]:
        detail = f"A={job['A']}; B={job['B']}" if job["kind"] == "judge" else ", ".join(sources[job["source"]])
        print(f"  {job['key']}: {detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
