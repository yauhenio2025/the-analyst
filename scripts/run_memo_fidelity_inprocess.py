"""The fidelity audit's second input, run directly: a memo's statements against the sources they cite.

  TMPDIR=data/tmp python3 -u -m scripts.run_memo_fidelity_inprocess communications/inputs/<file>.json [--batch 8] [--parallel 4]

No desks. The Stacks' digest_check inputs file is cut into batches of statements (every source kept), each batch runs
citation_fidelity_audit as one checked call (oneshot_checked: a read on the strong tier, the critic on the mid tier,
rulings applied by code), and the ledgers are merged by code with the batch number folded into every row id
(X6.F3 of batch 2 → X6.F203). Sol declined an unbatched run on 2026-09-06: 105 pairs against a ledger capped at a few
dozen rows, and rightly refused to audit a partial selection as if complete. Writes
data/study/memo_fidelity_2026_09_06/<stem>/{batch_<n>/…, merged.md, verdicts.json, run.json}.
"""
from __future__ import annotations
import argparse, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
OUT = ROOT / "data/study/memo_fidelity_2026_09_06"
ROW = re.compile(r"^\[([A-Z]\d)\.F(\d+)\]", re.M)


def renumber(content: str, batch: int) -> str:
    def sub(m):
        return f"[{m.group(1)}.F{batch * 100 + int(m.group(2))}]"
    content = ROW.sub(sub, content)
    return re.sub(r"\b([DX]\d)\.F(\d{1,2})\b", lambda m: f"{m.group(1)}.F{batch * 100 + int(m.group(2))}", content)


def field(row: str, name: str) -> str:
    m = re.search(rf"— {re.escape(name)}: (.*?)(?= — [a-z-]+: |$)", row)
    return (m.group(1).strip() if m else "")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--batch", type=int, default=8); ap.add_argument("--parallel", type=int, default=4)
    a = ap.parse_args()
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=False)
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_oneshot_checked
    from src.sources.memo_statements import batches, statements_to_evidence_index
    src = Path(a.file); out = OUT / src.stem; out.mkdir(parents=True, exist_ok=True)
    obj = json.loads(src.read_text())
    parts = batches(obj, size=a.batch)
    cap = get_engine_registry().get_capability_definition("citation_fidelity_audit")
    spec = get_operationalization_registry().get("citation_fidelity_audit").process
    print(time.strftime("%H:%M:%S"), f"{len(obj['statements'])} statements, {len(obj['sources'])} sources → {len(parts)} batches of {a.batch}", flush=True)
    start = time.time()

    def one(part):
        n = part["batch"]["index"]; bout = out / f"batch_{n}"; bout.mkdir(parents=True, exist_ok=True)
        receipts = []
        def on_call(call):
            receipts.append(call.as_receipt()); (bout / "receipts.json").write_text(json.dumps(receipts, indent=1, default=str))
            r = receipts[-1]; print(time.strftime("%H:%M:%S"), f"batch {n}", r.get("step"), r.get("kind"), r.get("model_used"), f"${r.get('cost_usd')}", f"rows={r.get('wall',{}).get('rows')}", flush=True)
        idx = statements_to_evidence_index(part)
        (bout / "index_pairs.json").write_text(json.dumps(idx["pairs"], indent=1))
        result = run_oneshot_checked(cap, spec, {"statements": json.dumps(part, ensure_ascii=False)}, depth="standard", on_call=on_call)
        content = result.final_content
        (bout / "output.md").write_text(content)
        proc = result.receipts()
        (bout / "run.json").write_text(json.dumps(proc, indent=1, default=str))
        return n, content, proc, idx["pairs"]

    results = {}
    with ThreadPoolExecutor(max_workers=a.parallel) as ex:
        futs = {ex.submit(one, p): p["batch"]["index"] for p in parts}
        for f in as_completed(futs):
            try:
                n, content, proc, pairs = f.result(); results[n] = (content, proc, pairs)
                print(time.strftime("%H:%M:%S"), f"batch {n} done: {len(content)} chars, ${proc.get('cost_usd', 0):.2f}", flush=True)
            except BaseException as exc:
                print(time.strftime("%H:%M:%S"), f"batch {futs[f]} FAILED {type(exc).__name__}: {str(exc)[:300]}", flush=True)
    merged, rows, cost, all_pairs = [], [], 0.0, []
    for n in sorted(results):
        content, proc, pairs = results[n]; cost += float(proc.get("cost_usd") or 0); all_pairs += pairs
        renum = renumber(content, n)
        merged.append(f"\n\n<!-- batch {n}: statements {parts[n-1]['batch']['statements']} -->\n\n" + renum)
        rows += [l for l in renum.splitlines() if ROW.match(l)]
    (out / "merged.md").write_text("".join(merged))
    verdict_rows = [r for r in rows if "dim: paired_fidelity" in r]
    counts = {}
    for r in verdict_rows:
        v = field(r, "verdict").split("|")[0].strip().lower() or "?"
        counts[v] = counts.get(v, 0) + 1
    refs = {field(r, "pair-ref") for r in verdict_rows}
    held_pairs = [p["pair_id"] for p in all_pairs if p["held"]]
    summary = {"status": "complete" if len(results) == len(parts) else "partial", "batches": len(parts), "batches_done": sorted(results),
               "seconds": round(time.time() - start), "cost_usd": round(cost, 4), "rows": len(rows), "verdict_rows": len(verdict_rows),
               "verdicts": counts, "pairs_in_index": len(all_pairs), "held_pairs": len(held_pairs),
               "held_pairs_with_verdict": sum(1 for p in held_pairs if p in refs), "unreferenced_pair_refs": sorted(refs - set(p["pair_id"] for p in all_pairs))[:20]}
    (out / "verdicts.json").write_text(json.dumps(summary, indent=1))
    (out / "run.json").write_text(json.dumps({**summary, "process": {n: results[n][1] for n in results}}, indent=1, default=str))
    print(time.strftime("%H:%M:%S"), "DONE", json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
