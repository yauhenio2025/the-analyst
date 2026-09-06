"""Build the local Riley -> Weber pilot; Zotero and Stacks are read-only inputs.

Extract all Riley PDF attachments once, retaining form feeds. The manifest keeps
every inclusion/exclusion and hash. Primary books are searched in a local cache;
only retrieved page windows are admitted to the corpus, never entire volumes.
"""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/study/sources_citation"
ZOTERO = Path.home() / "Zotero"
STACKS = Path.home() / "projects/zotero-stacks"
NAME = re.compile(r"\bWeber(?:ian|’s|'s)?\b", re.I)


def sha(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def connect():
    c = sqlite3.connect(f"file:{ZOTERO}/zotero.sqlite?mode=ro&immutable=1", uri=True)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA query_only=ON")
    return c


def item(c, ident):
    row = dict(c.execute("SELECT i.*, t.typeName FROM items i JOIN itemTypes t USING(itemTypeID) WHERE itemID=?", (ident,)).fetchone())
    fields = dict(c.execute("SELECT fieldName,value FROM itemData JOIN fields USING(fieldID) JOIN itemDataValues USING(valueID) WHERE itemID=?", (ident,)))
    creators = [dict(r) for r in c.execute("SELECT firstName,lastName,creatorTypeID FROM itemCreators JOIN creators USING(creatorID) WHERE itemID=? ORDER BY orderIndex", (ident,))]
    attachments = []
    for a in c.execute("SELECT i.key,a.path FROM itemAttachments a JOIN items i USING(itemID) WHERE parentItemID=? AND contentType='application/pdf' AND i.itemID NOT IN (SELECT itemID FROM deletedItems) ORDER BY i.key", (ident,)):
        p = ZOTERO / "storage" / a["key"] / a["path"].removeprefix("storage:")
        attachments.append({"key": a["key"], "path": str(p), "exists": p.is_file()})
    date = fields.get("date", "")
    year = re.search(r"\b(?:18|19|20)\d{2}\b", date)
    return {"key": row["key"], "uid": "em:" + row["key"], "type": row["typeName"],
            "title": fields.get("title", ""), "date": date, "year": int(year[0]) if year else None,
            "creators": creators, "fields": fields, "attachments": attachments}


def author_items(c, first, last):
    return [item(c, r[0]) for r in c.execute("SELECT DISTINCT i.itemID FROM items i JOIN itemCreators USING(itemID) JOIN creators USING(creatorID) WHERE firstName=? AND lastName=? AND i.itemID NOT IN (SELECT itemID FROM deletedItems)", (first, last))]


def extract(attachment):
    path = Path(attachment["path"])
    cache = OUT / "cache" / (attachment["key"] + ".txt")
    if not cache.exists():
        res = subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"], capture_output=True, check=True)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(res.stdout)
    return cache.read_text()


def pages(text):
    result = text.split("\f")
    return result[:-1] if result and not result[-1].strip() else result


def printed_pages(parts):
    """Use exposed page numerals at page edges, with an adjacent-page vote.

    Never equate PDF indices to printed pagination. Ambiguous or unnumbered
    pages remain unknown; confirmed offsets may bridge OCR-missing numerals.
    """
    candidates = []
    for i, p in enumerate(parts, 1):
        lines = [s.strip() for s in p.splitlines() if s.strip()]
        nums = set()
        for s in lines[:3] + lines[-3:]:
            for pat in (r"^(\d{1,4})(?:\s|$)", r"(?:^|\s)(\d{1,4})$"):
                m = re.search(pat, s)
                if m:
                    nums.add(int(m[1]))
        candidates.append(nums)
    offsets = Counter(n - i for i, nums in enumerate(candidates, 1) for n in nums)
    result = {}
    for i, nums in enumerate(candidates, 1):
        valid = [n for n in nums if offsets[n - i] >= 3]
        if valid:
            result[i] = max(valid, key=lambda n: offsets[n - i])
    # Fill a missing numeral only when both adjacent exposed pages agree.
    for i in range(2, len(parts)):
        if i not in result and i-1 in result and i+1 in result and result[i+1] == result[i-1]+2:
            result[i] = result[i-1]+1
    return result


def marked(parts, mapping=None, start=1):
    mapping = mapping or printed_pages(parts)
    return "\f\n".join(f"[p. {mapping.get(i, 'unknown')} | PDF p. {i}]\n{p}" for i, p in enumerate(parts, start))


def scan():
    c = connect()
    riley, weber = author_items(c, "Dylan", "Riley"), author_items(c, "Max", "Weber")
    secondary = []
    for r in c.execute("SELECT DISTINCT i.itemID FROM items i JOIN itemData USING(itemID) JOIN fields USING(fieldID) JOIN itemDataValues USING(valueID) WHERE fieldName='title' AND value LIKE '%Weber%' AND i.itemID NOT IN (SELECT itemID FROM deletedItems)"):
        it = item(c, r[0])
        if it["attachments"] and it["creators"] and not any(x["firstName"] in ("Max", "Dylan") and x["lastName"] in ("Weber", "Riley") for x in it["creators"]):
            secondary.append(it)
    c.close()

    def read(it):
        it["extractions"] = []
        for a in it["attachments"]:
            if not a["exists"]:
                continue
            try:
                t = extract(a)
                pp = pages(t)
                matches = sum(len(NAME.findall(p)) for p in pp)
                it["extractions"].append({"attachment_key": a["key"], "sha256": sha(t),
                    "pdf_sha256": sha(Path(a["path"]).read_bytes()), "pages": len(pp),
                    "chars": len(t), "weber_mentions": matches,
                    "cache": str((OUT / "cache" / (a["key"] + ".txt")).relative_to(ROOT))})
            except subprocess.CalledProcessError as e:
                it["extractions"].append({"attachment_key": a["key"], "error": str(e)})
        return it

    with ThreadPoolExecutor(max_workers=4) as pool:
        riley = list(pool.map(read, riley))
    write(OUT / "inventory.json", {"riley": riley, "weber": weber, "secondary_candidates": secondary,
        "zotero_uri": f"file:{ZOTERO}/zotero.sqlite?mode=ro&immutable=1",
        "zotero_stat": {"size": (ZOTERO / 'zotero.sqlite').stat().st_size,
                        "mtime_ns": (ZOTERO / 'zotero.sqlite').stat().st_mtime_ns}})
    for it in riley:
        ex = next((x for x in it["extractions"] if x.get("weber_mentions")), None)
        if ex:
            print(it["key"], it["type"], ex["chars"], ex["weber_mentions"], it["title"], flush=True)
    print("SCANNED", len(riley), "Riley records;", sum(bool(i["extractions"]) for i in riley), "with extracted PDF", flush=True)


def passage_windows(parts):
    """Locate literal name windows, excluding references and repeated furniture."""
    counts = Counter(s.strip() for p in parts for s in p.splitlines() if len(s.strip()) > 15)
    result = []
    in_references = False
    for number, p in enumerate(parts, 1):
        refs = re.search(r"(?im)^\s*(?:r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s(?: cited)?|bibliography)\s*$", p)
        stop = refs.start() if refs else len(p)
        if in_references:
            continue
        intervals = []
        for m in NAME.finditer(p[:stop]):
            line_start, line_end = p.rfind("\n", 0, m.start()) + 1, p.find("\n", m.end())
            line = p[line_start:line_end if line_end >= 0 else len(p)].strip()
            if counts[line] > 2 or "http" in line.lower():
                continue
            # Two nearby sentence boundaries each side; cap exceptionally long sentences.
            before = list(re.finditer(r"[.!?][”’\"']?\s+(?=[A-Z“\"'])|\n\n", p[:m.start()]))
            start = before[-2].end() if len(before) >= 2 else 0
            after = list(re.finditer(r"[.!?][”’\"']?\s+(?=[A-Z“\"'])|\n\n", p[m.end():stop]))
            end = m.end() + after[min(1, len(after)-1)].start() + 1 if after else stop
            start, end = max(start, m.start()-650), min(end, m.end()+750)
            if intervals and start <= intervals[-1][1] and end-intervals[-1][0] <= 2200:
                intervals[-1][1] = max(end, intervals[-1][1])
            else:
                intervals.append([start,end])
        result.extend({"pdf_page": number, "start": a, "end": b, "window": p[a:b].strip()} for a,b in intervals)
        if refs:
            in_references = True
    return result


def build_passages(include_podcast=False):
    inventory = json.loads((OUT / "inventory.json").read_text())
    selected, excluded, passages = [], [], []
    types = {"journalArticle", "magazineArticle", "bookSection"}
    if include_podcast:
        types |= {"audioRecording", "podcast"}
    # These are source-read duplicate/ownership decisions, not text classifiers.
    skips = {
        "FNI5R43Z": "PDF bundles Heilbron/Steinmetz and Burawoy replies with Riley; Riley's complete reply is EJJLVCUC.",
        "JD34AWGB": "Web print of the same Bourdieu article held as the paginated X7K39J6C; retained copy includes print notes.",
    }
    for it in sorted(inventory["riley"], key=lambda i: (i["year"] or 9999, i["key"])):
        ex = next((e for e in it["extractions"] if "error" not in e), None)
        why = skips.get(it["key"])
        if not ex:
            why = "No extractable held PDF."
        elif it["type"] not in types:
            why = "Outside article/chapter pilot scope (book, thesis, or recording); PDF still scanned."
        if why:
            excluded.append({"key":it["key"],"title":it["title"],"reason":why})
            continue
        text = (ROOT / ex["cache"]).read_text()
        pp = pages(text)
        if it["key"] == "PSYPHAPS":
            # The opening of this PDF finishes a different review. Preserve Riley
            # from his article heading onward, keeping the original PDF indices.
            begin = pp[0].find("Routes or Rivals?")
            if begin < 0:
                raise ValueError("Riley article boundary missing")
            pp[0] = pp[0][begin:]
        wins = passage_windows(pp)
        if not wins:
            excluded.append({"key":it["key"],"title":it["title"],"reason":"No body Weber-name window after reference/header exclusion."})
            continue
        pm = printed_pages(pp)
        path = OUT / "a" / (it["key"] + ".txt")
        path.parent.mkdir(parents=True, exist_ok=True)
        # No truncation of an admitted citing work.
        header = f"SOURCE ROLE: citing_author\nAUTHOR: {', '.join(a['firstName']+' '+a['lastName'] for a in it['creators'])}\nTARGET THINKER: Max Weber\nZOTERO UID: {it['uid']}\nTITLE: {it['title']}\nYEAR: {it['year'] or 'unknown'} (Zotero date: {it['date'] or 'missing'})\n\n"
        content = header + marked(pp, pm)
        path.write_text(content)
        selected.append({**it, "path":str(path.relative_to(ROOT)),"sha256":sha(content),"extraction":ex,"printed_pages":pm})
        for w in wins:
            passages.append({"ref_id": f"RW{len(passages)+1:04d}","text_key":it["key"],"uid":it["uid"],
                "title":it["title"],"year":it["year"],"page":pm.get(w["pdf_page"]), **w,
                "cited_work":None,"cited_locus":None,"resolution":"not yet resolved"})
    write(OUT / "passage_index.json", {"author":"Dylan Riley","person":"Max Weber","method":"literal surname/Weberian sentence windows; body/reference/header filter; not an exhaustive citation ledger", "passages":passages})
    write(OUT / "selection.json", {"selected":selected,"excluded":excluded,"include_podcast":include_podcast})
    print("SELECTED",len(selected),"texts",sum(len((ROOT/i['path']).read_text()) for i in selected),"chars;",len(passages),"windows",flush=True)
    for p in passages:
        print(p['ref_id'],p['text_key'],p['page'],p['pdf_page'],re.sub(r'\s+',' ',p['window']),flush=True)


WORK_KEYS = ["NEVNCMNY", "5AZK3B3X", "T3TU9KPR", "VGJ3KBBJ", "ZJ3WLWCS", "GUWLLR3M", "NFJUV484", "QM343SXS", "TTMQKP3D"]
SECONDARY_KEYS = ["ZYGH3ALE", "SNF5KW47", "SN6NRCTG", "PL4C6Y9V", "TDSPYHWK", "5TK5DW6T", "RJKSEUD6", "AN9YUUG9"]


def prepare_works():
    inventory = json.loads((OUT/"inventory.json").read_text())
    works = [i for i in inventory["weber"] if i["key"] in WORK_KEYS]
    for it in works:
        a = next(a for a in it["attachments"] if a["exists"])
        t = extract(a); pp=pages(t); mapping=printed_pages(pp)
        it["attachment"]=a; it["cache_sha256"]=sha(t);it["pdf_sha256"]=sha(Path(a["path"]).read_bytes())
        it["printed_pages"]=mapping;it["pdf_pages"]=len(pp)
        print(it["key"], len(pp), "pages",len(t),"chars;",len(mapping),"mapped; offsets",Counter(n-i for i,n in mapping.items()).most_common(5),flush=True)
    write(OUT/"work_maps.json",works)


def build_reception():
    inventory=json.loads((OUT/"inventory.json").read_text()); selected=[]
    for key in SECONDARY_KEYS:
        it=next(i for i in inventory["secondary_candidates"] if i["key"]==key)
        a=next(a for a in it["attachments"] if a["exists"])
        raw=extract(a);pp=pages(raw);mapping=printed_pages(pp)
        t=marked(pp,mapping)
        # Densest contiguous 40k-character window. The selected range is explicit,
        # not a collage that silently removes contrary intervening passages.
        begin=0;end=len(t)
        if it["type"]=="book" and len(t)>40_000:
            hits=[m.start() for m in NAME.finditer(t)]
            candidates={0,len(t)-40_000}|{max(0,min(h-20_000,len(t)-40_000)) for h in hits}
            begin=max(sorted(candidates),key=lambda n:sum(n<=h<n+40_000 for h in hits))
            end=begin+40_000
        body=t[begin:end]
        scope=f"contiguous densest 40000-character excerpt; marked-text character range [{begin}, {end})" if end-begin<len(t) else "full held text"
        header=f"SOURCE ROLE: secondary_reader\nAUTHOR: {', '.join(a['firstName']+' '+a['lastName'] for a in it['creators'])}\nTARGET THINKER: Max Weber\nREFERENCE AUTHOR: Dylan Riley\nZOTERO UID: {it['uid']}\nTITLE: {it['title']}\nYEAR: {it['year'] or 'unknown'}\nCOVERAGE: {scope}\n\n"
        content=header+body;p=OUT/"secondary"/(key+".txt");p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        selected.append({**it,"path":str(p.relative_to(ROOT)),"sha256":sha(content),"attachment":a,"extraction_sha256":sha(raw),"pdf_sha256":sha(Path(a['path']).read_bytes()),"coverage":scope,"excerpt_start":begin,"excerpt_end":end,"full_marked_chars":len(t)})
        print(key,it['year'],it['title'],len(content),scope,flush=True)
    write(OUT/"reception_manifest.json",selected)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["scan", "passages", "works", "reception"])
    ap.add_argument("--include-podcast", action="store_true")
    args = ap.parse_args()
    if args.action == "scan":
        scan()
    elif args.action == "passages":
        build_passages(args.include_podcast)
    elif args.action == "works":
        prepare_works()
    elif args.action == "reception":
        build_reception()
