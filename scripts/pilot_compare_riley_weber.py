"""The Riley → Weber pilot both ways: Sonnet rates the Mastermind's dossier and the Stacks' memo 2 on the family's
six-criterion rubric, then judges them head to head in both orders; only agreements count (Sol as a pairwise judge
picked the first-seen reading 80 of 87 times; Sonnet shows no position lean).

  TMPDIR=data/tmp python3 -u -m scripts.pilot_compare_riley_weber --ours <dossier.md> --theirs <memo.md> [--judge claude-sonnet-4-6]

The judge sees a bounded source packet, not the 2.8M-char corpus: every held primary window from the evidence index
whole, every citing text under 14,000 chars whole, and for the rest the index's passage windows (±400 normalized chars)
plus every quotation of 40+ chars that either memo makes and the text contains (±1,200). The owner reads both memos
before opening the scores (the handoff's rule); this script only produces them.
Writes data/study/citation_family_2026_09_06/pilot/compare/…
"""
from __future__ import annotations
import argparse, json, re, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
SOURCES = ROOT / "data/study/sources_citation"; OUT = ROOT / "data/study/citation_family_2026_09_06/pilot/compare"

RUBRIC_KEYS = ("specificity", "anchoring", "non_obviousness", "coherence", "usefulness", "hallucination_risk")
RUBRIC = ("Score the ANALYSIS on the SOURCES, 1-10 each. specificity: about THESE texts and this author's use of this thinker? "
          "anchoring: claims tied to verbatim quotes that exist in the sources? non_obviousness: what a careful expert finds and a casual "
          "reader misses? coherence: one reading of the engagement, not a list? usefulness: would a scholar of this author who must decide "
          "what the engagement amounts to act differently? hallucination_risk (10 = none): claims the sources do not support, including "
          "claims about the author's mind, career or texts not supplied? Answer as JSON: "
          '{"specificity": n, "anchoring": n, "non_obviousness": n, "coherence": n, "usefulness": n, "hallucination_risk": n, "one_line": "..."}')
PAIR = ("Two memos on the same question over the same sources: how this author engages this thinker across the supplied citing texts, whether "
        "the attributions hold against the thinker's cited pages, and where the author sits among the thinker's readers. Which is the better "
        "memo for a scholar who must decide what the engagement amounts to: more specific to these texts, better anchored in real quotes, less "
        "obvious, more coherent, more useful, fewer unsupported claims? Judge the reading, not the length or the format. Answer as JSON: "
        '{"winner": "A"|"B"|"tie", "margin": "slight"|"clear"|"decisive", "why": "...", "what_A_has_that_B_lacks": "...", "what_B_has_that_A_lacks": "..."}')
CAVEAT = ("\nThe sources are an explicitly bounded source-context packet: every held primary window, the indexed citation windows, and each "
          "memo's quotations with neighbouring context. Do not certify full-corpus coverage or global absence from this packet. Judge the "
          "readings and the tables against what is supplied. A location match is not fidelity. Keep reasons concise. Do not infer quality "
          "from the format (one memo is a dossier with tables and receipts, the other an essay with footnotes).")


def quotes(md: str) -> list[str]:
    qs = re.findall(r'[""]([^""]{40,400})[""]', md) + re.findall(r'"([^"\n]{40,400})"', md)
    return list(dict.fromkeys(q.strip() for q in qs))


def _windows(text, norm, qs, index_windows, rq, ri):
    intervals, hits = [], 0
    for q in qs:
        at = norm.find(q)
        if at >= 0:
            intervals.append((max(0, at - rq), min(len(norm), at + len(q) + rq))); hits += 1
    for w in index_windows:
        at = norm.find(w) if w else -1
        if at >= 0:
            intervals.append((max(0, at - ri), min(len(norm), at + len(w) + ri)))
    merged = []
    for lo, hi in sorted(intervals):
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(hi, merged[-1][1])
        else:
            merged.append([lo, hi])
    if not merged:
        return text[:12_000] + "\n\n[… the rest of this document is not quoted by either memo and is omitted from the packet]", hits
    body = text[:700] + "\n\nNORMALIZED SOURCE CONTEXTS (separate ranges, not continuous text):\n" + "\n\n".join(
        f"[normalized chars {lo}:{hi}]\n{norm[lo:hi]}" for lo, hi in merged)
    return body, hits


def packet(memos: list[str], cap_chars: int = 330_000) -> tuple[dict[str, str], dict]:
    """Primary windows and short citing texts whole; the rest windowed around the index's passages and the memos'
    quotations. Texts the Stacks' memo cites that the pilot corpus lacks (extra_texts_stacks_memo2.json, from the
    local Zotero) are windowed the same way, so the judge can check both memos' anchors. Radii shrink until the packet
    fits `cap_chars`, so the judge never exceeds its context."""
    from src.executor.ledger_walls import normalize
    from src.sources.citation_evidence import prepare_citation_sources
    documents = json.loads((SOURCES / "documents.json").read_text())
    documents["__index__"] = (SOURCES / "evidence_index.json").read_text()
    docs, _ = prepare_citation_sources("citation_fidelity_audit", documents)      # citing texts + primary windows, index unpacked
    extra = SOURCES / "extra_texts_stacks_memo2.json"
    if extra.exists():
        for key, v in json.loads(extra.read_text()).items():
            docs[key] = f"SOURCE ROLE: citing_author\nTITLE: {v['title']}\nCOVERAGE: held text outside the pilot corpus (cited by the Stacks' memo)\n\n{v['text']}"
    index = json.loads((SOURCES / "evidence_index.json").read_text())
    qs = [normalize(q) for m in memos for q in quotes(m)]
    iw = {}
    for t in index["texts"]:
        iw[t.get("uid")] = [normalize(p.get("window") or p.get("hit") or "") for p in t.get("passages", [])]
    # whole: primary windows and short texts, unless a document is huge (a work's accumulated page windows can run to
    # 190K chars): anything over 40K is windowed around the memos' quotations, with its head kept when nothing hits
    norms = {k: normalize(v) for k, v in docs.items() if len(v) > 40_000 or not ("SOURCE ROLE: primary_window" in v or len(v) < 14000)}
    for rq, ri in ((1200, 400), (800, 300), (500, 200), (300, 120), (160, 60)):
        out, meta = {}, {"docs": len(docs), "whole": 0, "windowed": 0, "quote_hits": 0, "radii": [rq, ri]}
        for key, text in docs.items():
            if key not in norms:
                out[key] = text; meta["whole"] += 1; continue
            out[key], hits = _windows(text, norms[key], qs, iw.get(key, []), rq, ri)
            meta["windowed"] += 1; meta["quote_hits"] += hits
        meta["chars"] = sum(map(len, out.values()))
        if meta["chars"] <= cap_chars:
            break
    return out, meta


def call(system: str, user: str, judge: str, label: str) -> tuple[dict, dict]:
    from src.executor.engine_runner import run_engine_call
    from src.events.pricing import estimate_cost
    from src.llm.client import parse_llm_json_response
    res = run_engine_call(system_prompt=system, user_message=user, model_hint=judge, depth="standard", label=label)
    used = res.get("model_used") or judge
    receipt = {"model": used, "input_tokens": res.get("input_tokens"), "output_tokens": res.get("output_tokens"),
               "cost_usd": estimate_cost(used, res.get("input_tokens"), res.get("output_tokens")) or 0.0, "label": label}
    return parse_llm_json_response(res["content"]), receipt


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--ours", required=True); ap.add_argument("--theirs", required=True)
    ap.add_argument("--judge", default="claude-sonnet-4-6"); ap.add_argument("--intent", default=(
        "How does Dylan Riley engage Max Weber across his work; is that engagement justified by the Weber texts he cites; and where does his "
        "reading sit among Weber's readers we hold?")); a = ap.parse_args()
    from dotenv import load_dotenv; load_dotenv(ROOT / ".env", override=False)
    OUT.mkdir(parents=True, exist_ok=True)
    ours, theirs = Path(a.ours).read_text(), Path(a.theirs).read_text()
    docs, meta = packet([ours, theirs])
    src_block = "\n\n=====\n\n".join(f"SOURCE [{k}]:\n{v}" for k, v in docs.items())
    (OUT / "packet_meta.json").write_text(json.dumps({**meta, "ours": a.ours, "theirs": a.theirs, "ours_chars": len(ours), "theirs_chars": len(theirs),
                                                      "judge": a.judge, "source_keys": list(docs)}, indent=1))
    print(time.strftime("%H:%M:%S"), "packet:", meta, flush=True)
    receipts, results = [], {}
    system_r = RUBRIC + "\nRequested artifact: a memo answering: " + a.intent + CAVEAT
    for name, memo in (("ours", ours), ("theirs", theirs)):
        score, r = call(system_r, src_block + "\n\nANALYSIS:\n" + memo, a.judge, f"rubric {name}")
        receipts.append(r); results[f"rubric_{name}"] = score
        (OUT / f"rubric_{name}.json").write_text(json.dumps(score, indent=1, ensure_ascii=False))
        print(time.strftime("%H:%M:%S"), name, {k: score.get(k) for k in RUBRIC_KEYS}, f"${r['cost_usd']:.2f}", flush=True)
    system_p = PAIR + "\nThe question both memos answer: " + a.intent + CAVEAT
    for order, (A, B) in (("ours_first", (ours, theirs)), ("theirs_first", (theirs, ours))):
        verdict, r = call(system_p, src_block + "\n\nMEMO A:\n" + A + "\n\n=====\n\nMEMO B:\n" + B, a.judge, f"pair {order}")
        receipts.append(r); results[f"pair_{order}"] = verdict
        (OUT / f"pair_{order}.json").write_text(json.dumps(verdict, indent=1, ensure_ascii=False))
        print(time.strftime("%H:%M:%S"), order, verdict.get("winner"), verdict.get("margin"), f"${r['cost_usd']:.2f}", flush=True)
    w1 = results["pair_ours_first"].get("winner"); w2 = results["pair_theirs_first"].get("winner")
    who1 = {"A": "ours", "B": "theirs"}.get(w1, "tie"); who2 = {"A": "theirs", "B": "ours"}.get(w2, "tie")
    agreement = who1 if who1 == who2 else "disagree"
    means = {n: round(sum(results[f"rubric_{n}"].get(k, 0) for k in RUBRIC_KEYS) / 6, 2) for n in ("ours", "theirs")}
    summary = {"rubric_means": means, "pairwise": {"ours_first": who1, "theirs_first": who2, "agreement": agreement},
               "cost_usd": round(sum(r["cost_usd"] for r in receipts), 4), "receipts": receipts, "packet": meta}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(time.strftime("%H:%M:%S"), "DONE", json.dumps({k: v for k, v in summary.items() if k != "receipts"}), flush=True)


if __name__ == "__main__":
    main()
