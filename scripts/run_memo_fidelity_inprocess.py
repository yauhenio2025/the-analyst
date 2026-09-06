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
ROW = re.compile(r"^(?:- |\* )?\[(?:[A-Z]\d\.)?F(\d+)\]", re.M)          # a ledger row: "- [F6] …" or "[X6.F6] …"
TABLE_ROW = re.compile(r"^\| *(st\d+/\S+?) *\|(.*?)\|(.*?)\|([^|]*?\b(accurate|fair|selective|stretched|misattributed|unverifiable)\b[^|]*)\|(.*?)\|\s*$", re.M | re.I)


def renumber(content: str, batch: int) -> str:
    """Fold the batch into every finding id: F6 of batch 2 → F206, wherever the id appears."""
    return re.sub(r"\[((?:[A-Z]\d\.)?)F(\d{1,2})\]", lambda m: f"[{m.group(1)}F{batch * 100 + int(m.group(2))}]", content)


VERDICTS = ("accurate", "fair", "selective", "stretched", "misattributed", "unverifiable")


def field(row: str, name: str) -> str:
    m = re.search(rf"— {re.escape(name)}: (.*?)(?= — [a-z-]+: |$)", row)
    return (m.group(1).strip() if m else "")


def audit_rows(content: str, batch: int) -> list[dict]:
    """Every pair verdict in an assembled reading: first the ledger rows of the paired_fidelity dimension (pair-ref and
    verdict as fields, the canonical form), then the paired-audit table where a batch rendered one; one entry per pair,
    the ledger row preferred."""
    out, seen = [], set()
    for line in content.splitlines():
        m = ROW.match(line)
        if not m or "dim: paired_fidelity" not in line:
            continue
        pair, verdict = field(line, "pair-ref"), field(line, "verdict").split("|")[0].strip().lower()
        if pair and verdict in VERDICTS and pair not in seen:
            seen.add(pair)
            out.append({"pair": pair, "verdict": verdict, "finding": f"F{int(m.group(1))}", "source": "ledger", "batch": batch,
                        "a_attributes": field(line, "a-attributes")[:240], "p_says": field(line, "p-says")[:240], "reason": field(line, "reason")[:300],
                        "anchor": field(line, "anchor")[:200], "anchor_b": field(line, "anchor-b")[:200], "confidence": field(line, "confidence")})
    for m in TABLE_ROW.finditer(content):
        if m.group(1) not in seen:
            seen.add(m.group(1))
            fid = re.search(r"\[(?:[A-Z]\d\.)?(F\d+)\]", m.group(4))
            out.append({"pair": m.group(1), "verdict": m.group(5).lower(), "finding": fid.group(1) if fid else "", "source": "table", "batch": batch,
                        "claim": m.group(2).strip()[:240], "comparison": m.group(3).strip()[:300], "locus": m.group(6).strip()[:120]})
    return out


def merge(out: Path, parts: list[dict], results: dict, start: float) -> dict:
    merged, rows, pairs, cost, all_pairs = [], [], [], 0.0, []
    for n in sorted(results):
        content, proc, index_pairs = results[n]; cost += float(proc.get("cost_usd") or 0); all_pairs += index_pairs
        renum = renumber(content, n)
        merged.append(f"\n\n<!-- batch {n}: statements {parts[n-1]['batch']['statements']} -->\n\n" + renum)
        rows += [l for l in renum.splitlines() if ROW.match(l)]
        pairs += audit_rows(renum, n)
    (out / "merged.md").write_text("".join(merged))
    (out / "pairs.json").write_text(json.dumps(pairs, indent=1, ensure_ascii=False))
    counts = {}
    for p in pairs:
        counts[p["verdict"]] = counts.get(p["verdict"], 0) + 1
    refs = {p["pair"] for p in pairs}
    held_pairs = [p["pair_id"] for p in all_pairs if p["held"]]
    summary = {"status": "complete" if len(results) == len(parts) else "partial", "batches": len(parts), "batches_done": sorted(results),
               "seconds": round(time.time() - start), "cost_usd": round(cost, 4), "ledger_rows": len(rows), "audit_rows": len(pairs),
               "verdicts": counts, "pairs_in_index": len(all_pairs), "held_pairs": len(held_pairs),
               "held_pairs_with_verdict": sum(1 for p in held_pairs if p in refs),
               "pairs_without_verdict": [p for p in held_pairs if p not in refs][:30],
               "unreferenced_pair_refs": sorted(refs - set(p["pair_id"] for p in all_pairs))[:20]}
    (out / "verdicts.json").write_text(json.dumps(summary, indent=1))
    (out / "run.json").write_text(json.dumps({**summary, "process": {n: results[n][1] for n in results}}, indent=1, default=str))
    return summary


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("file"); ap.add_argument("--batch", type=int, default=8); ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--merge-only", action="store_true", help="re-merge the batch outputs on disk; no model calls")
    a = ap.parse_args()
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=False)
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    from src.executor.process_runner import run_oneshot_checked
    from src.sources.memo_statements import batches, statements_to_evidence_index
    src = Path(a.file); out = OUT / src.stem; out.mkdir(parents=True, exist_ok=True)
    obj = json.loads(src.read_text())
    parts = batches(obj, size=a.batch)
    if a.merge_only:
        results = {}
        for part in parts:
            n = part["batch"]["index"]; bout = out / f"batch_{n}"
            if (bout / "output.md").exists():
                results[n] = ((bout / "output.md").read_text(), json.loads((bout / "run.json").read_text()), statements_to_evidence_index(part)["pairs"])
        summary = merge(out, parts, results, time.time())
        print(time.strftime("%H:%M:%S"), "MERGED", json.dumps(summary), flush=True); return
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
    summary = merge(out, parts, results, start)
    print(time.strftime("%H:%M:%S"), "DONE", json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
