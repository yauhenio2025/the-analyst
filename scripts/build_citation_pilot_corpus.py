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


# Source-read location records. This is bibliography/pagination metadata, never
# an accuracy verdict. Every PDF window below is extracted afresh with -f/-l.
ES = 'NEVNCMNY'
FROM = 'VGJ3KBBJ'
RESOLUTIONS = {
 'RW0001': (FROM, [194], 'Class, Status, Party'),
 'RW0002': ('QM343SXS', [], 'Critical Studies in the Logic of the Cultural Sciences'),
 'RW0003': ('QM343SXS', [], 'Critical Studies in the Logic of the Cultural Sciences'),
 'RW0008': (FROM, [], 'Religious Rejections of the World and Their Directions'),
 'RW0010': (FROM, [], 'Politics as a Vocation'),
 'RW0011': (FROM, [], 'Politics as a Vocation'),
 'RW0016': (ES, [919], 'Political Communities: The Economic Foundations of Imperialism'),
 'RW0023': (FROM, list(range(77,88)), 'Politics as a Vocation'),
 'RW0029': (ES, list(range(1407,1411)), 'Parliament and Government in a Reconstructed Germany'),
 'RW0042': (ES, list(range(1028,1032)), 'Patriarchal and Patrimonial Domination'),
 'RW0045': (ES, [917], 'Political Communities: The Economic Foundations of Imperialism'),
 'RW0048': (ES, list(range(86,91)), 'Sociological Categories of Economic Action'),
 'RW0049': (ES, [91,92,93], 'Sociological Categories of Economic Action'),
 'RW0050': (FROM, [152,153], 'Science as a Vocation'),
 'RW0064': (FROM, [126], 'Politics as a Vocation'),
 'RW0074': ('GUWLLR3M', [], 'Parliament and Government in Germany under a New Political Order'),
 'RW0076': (ES, [53], 'Basic Sociological Terms: Power and Domination'),
 'RW0077': (ES, [954,1112], 'Domination and Legitimacy; Charisma'),
 'RW0078': (ES, [956,1006,1112], 'Bureaucracy; Patrimonial Domination; Charisma'),
 'RW0079': (ES, [956,1006,1112], 'Bureaucracy; Patrimonial Domination; Charisma'),
 'RW0080': ('NFJUV484', [], None),
 'RW0081': (ES, [942,973,974,975], 'Domination and Legitimacy; Bureaucracy'),
 'RW0082': (ES, [956,957,958,1417,1418], 'Bureaucracy; Parliament and Government'),
 'RW0083': (ES, [974], 'Bureaucracy'),
 'RW0084': (ES, [213], 'The Types of Legitimate Domination'),
 'RW0085': ('NFJUV484', [180], 'Kapitel IV. Stände und Klassen, §3. Ständische Lage und Stand'),
 'RW0088': (ES, [965,966], 'Bureaucracy: Economic Presuppositions of Bureaucracy'),
 'RW0096': (ES, [965,966], 'Bureaucracy: Economic Presuppositions of Bureaucracy'),
}
# A note and its body form one citation event, not two independent checks.
NOTE_LINKS = {'RW0013':'RW0011','RW0030':'RW0029','RW0043':'RW0042',
              'RW0046':'RW0045','RW0089':'RW0088','RW0097':'RW0096'}
CALIBRATIONS = {
 ES: {'offset':110, 'range':[1,1469], 'inspected':{'53':163,'917':1027,'919':1029,'965':1075,'1028':1138,'1407':1517},
      'note':'Source-read continuous body pagination; OCR edge heuristic rejected (e.g. 1177 misread as 77).'},
 FROM: {'offset':13, 'range':[1,490], 'inspected':{'126':139,'152':165,'194':207},
        'note':'Gerth/Mills 1948 held impression; cited 1946/1958 impressions differ in date; verify text, do not assert edition identity.'},
}


def pilot_plan():
    estates=STACKS/'communications/2026-09-03_riley_weber_estates.md'
    bundle=STACKS/'communications/2026-09-03_castoriadis_weber_bundle.md'
    plan={
      'provenance':{'saved_lane_plan':'absent in communications/2026-09-05_cites and Riley-Weber memo files in this clone',
        'status':'guide-derived plan, reconstructed from the Stacks estates memo and bundle 299; not the missing Fable plan',
        'sources':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in [estates,bundle]]},
      'questions':[
        'How do estates, closure, political capitalism and patrimonialism function across Riley’s dated texts?',
        'Does Riley fuse market closure and status honour, and what do the cited Weber places actually establish?',
        'How do the 2013 imperialism prognosis, the 2020 explicit adaptation, and the 2025–26 tax-farming citations differ?',
        'Does the 2018 criticism of estate concepts differ from the later society-of-estates thesis, and what explains the change?',
        'How do Marx/Weber standpoints, subjective meaning and imagined alternatives connect to the institutional concepts?',
        'Which supplied readers bear on those questions, and what concerns do those readers add?'],
      'warnings':[
        'The estates memo is an LLM-written guide, not evidence; test its interpretations against the PDFs.',
        'The September 3 guide predates acquisition of Roth/Wittich E&S; its not-held claims are historical, not current.',
        'Keep closure, status honour, estate and acquisition-class categories distinct; do not assume the guide’s fusion thesis.',
        'Weber 1922 p.180 is marginal A180 in MWG I/23, not printed MWG p.180; editions and translations need separate notes.',
        'Separate Riley’s claims from quoted Judt, Mann, Bourdieu, Brown and Lukács, and preserve Emigh/Brenner coauthorship.',
        'The Catalyst bundled reply includes adjacent authors; the separate Riley copy is the pilot witness.',
        'Citation-index name windows are a candidate inventory, not complete citation recall; note links are not extra events.',
        'Book excerpts cannot prove global silence; absent scholarly citation counts cannot support most-cited rankings.',
        'The Stacks export index text has no page markers; this pilot’s page-marked witnesses and windows come from PDFs.'],
      'themes':['Estates, status honour and social closure','Political capitalism, imperialism and tax-farming',
        'Patrimonialism, bureaucracy and political organisation','The historical applicability of estate concepts',
        'Marx and Weber as standpoints; meaning, imagined alternatives and class formation',
        'Science, political values and responsibility']}
    write(OUT/'pilot_plan.json',plan)
    return plan


def ranges(numbers):
    out=[]
    for n in sorted(set(numbers)):
        if out and n==out[-1][-1]+1:out[-1].append(n)
        else:out.append([n])
    return [(ns[0],ns[-1]) for ns in out]


def build_evidence():
    inventory=json.loads((OUT/'inventory.json').read_text())
    works={i['key']:i for i in json.loads((OUT/'work_maps.json').read_text())}
    selections=json.loads((OUT/'selection.json').read_text())['selected']
    selection={i['key']:i for i in selections}
    passages=json.loads((OUT/'passage_index.json').read_text())['passages']
    checks=[];unchecked=[];texts=[]
    word=lambda t:set(w.lower() for w in re.findall(r'\b[A-Za-zÀ-ž]{4,}\b',t) if w.lower() not in
      {'weber','which','their','there','these','those','would','could','about','other','political','sociology','society','economy'})
    for p in passages:
        ref=p['ref_id'];resolution=RESOLUTIONS.get(ref)
        if not resolution:
            unchecked.append({'ref_id':ref,'why':('same event as '+NOTE_LINKS[ref]) if ref in NOTE_LINKS else
                'No specific directly located Weber work in this name window; mention, reported reading, or unspecific attribution. Not certified as absent.'})
            continue
        key,nums,section=resolution;it=works[key];a=it['attachment'];pp=pages(extract(a))
        cited=nums[:];how='page';notes=[]
        if key in CALIBRATIONS and nums:
            cal=CALIBRATIONS[key];pdfnums=[n+cal['offset'] for n in nums]
            mapping={n:n-cal['offset'] for n in range(1,len(pp)+1) if cal['range'][0]<=n-cal['offset']<=cal['range'][1]}
            notes.append(cal['note'])
        elif ref=='RW0085':
            pdfnums=[625,626];mapping={n:n-27 for n in range(624,628)}
            notes.append('Cited 1922 p.180 corresponds to marginal A180 at MWG I/23 pp.598–599, PDF625–626; not MWG p.180.')
        else:
            how='search';terms=word(p['window']);scores=[len(terms&word(t)) for t in pp]
            best=max(range(len(pp)),key=lambda i:scores[i]);pdfnums=[best+1]
            mapping={int(k):v for k,v in it['printed_pages'].items()}
            notes.append('Simple term-overlap candidate (score '+str(scores[best])+'); no locus/edition equivalence established. Supplied section title names the cited target, not proof the search landed inside it.')
        want=[n for n in pdfnums for n in range(max(1,n-1),min(len(pp),n+1)+1)]
        wins=[]
        for lo,hi in ranges(want):
            raw=subprocess.run(['pdftotext','-enc','UTF-8','-f',str(lo),'-l',str(hi),a['path'],'-'],capture_output=True,check=True).stdout.decode()
            body=marked(pages(raw),mapping,start=lo)
            wins.append({'how':how,'section_title':section,'printed':[mapping.get(n) for n in range(lo,hi+1)],
                'pdf':list(range(lo,hi+1)),'text':body,'sha256':sha(body),
                'command':['pdftotext','-enc','UTF-8','-f',str(lo),'-l',str(hi),a['path'],'-']})
        check={'work_key':key,'title':it['title'],'year':it['year'],
            'copy':{'uid':it['uid'],'edition':it['date']+'; '+it['fields'].get('publisher',''),
                    'language':it['fields'].get('language') or ('German' if key=='NFJUV484' else 'English'),
                    'attachment_key':a['key'],'pdf_sha256':sha(Path(a['path']).read_bytes())},
            'cited_pages':cited,'windows':wins,'ref_ids':[ref], 'edition_pagination_notes':notes}
        if ref in ('RW0002','RW0003'):check['cited_pages']=[172];check['edition_pagination_notes'].append('Cites Methodology of the Social Sciences (1949), p.172; held German MWG I/7 is a different language/collection; English search may be uninformative. Collected Methodological Writings has no held PDF in this snapshot.')
        if ref=='RW0074':check['cited_pages']=[398];check['edition_pagination_notes'].append('Cited Gesammelte politische Schriften (1921); held English Political Writings is a different collection.')
        if ref=='RW0080':check['edition_pagination_notes'].append('Passage cites multiple German collections (1921 p397; 1922 p526; 1925 pp69–79,241–242). Search tests only E&S candidate; other works unchecked.')
        if ref=='RW0049':check['edition_pagination_notes'].append('Also cites General Economic History 1992[1927] pp275–277; this pair covers only E&S 91–93.')
        checks.append(check)
        p['cited_work']={'key':key,'title':it['title']};p['cited_locus']=check['cited_pages'];p['resolution']=how
    for it in selections:
        ps=[dict(p) for p in passages if p['text_key']==it['key']]
        raw=pages((ROOT/it['extraction']['cache']).read_text());mp={int(k):v for k,v in it['printed_pages'].items()}
        for p in ps:
            if p['ref_id'] in RESOLUTIONS:
                lo=max(1,p['pdf_page']-1);hi=min(len(raw),p['pdf_page']+1)
                # The selected article may start partway through a shared PDF page.
                actual=(ROOT/it['path']).read_text()
                parts=[marked([raw[n-1]],mp,start=n) for n in range(lo,hi+1)]
                p['section']='\n\n'.join(part for part in parts if part in actual)
                if not p['section']:p['section']=p['window']
            p['work']=p.pop('cited_work');p['locus']={'printed':p['page'],'pdf':p['pdf_page'],'cited':p.pop('cited_locus')}
        texts.append({'uid':it['uid'],'title':it['title'],'year':it['year'],'type':it['type'],
                      'creators':it['creators'],'passages':ps})
    index={'role':'evidence_index','author':'Dylan Riley','person':'Max Weber','plan':pilot_plan(),
      'texts':texts,'checks':checks,'unchecked':unchecked,
      'settings':{'extraction':'pdftotext without -layout; form feeds retained; PDF windows extracted with -f/-l',
        'coverage':{'citing_texts':len(texts),'candidate_name_windows':len(passages),'checked_pair_candidates':len(checks),
                    'unchecked_or_linked_windows':len(unchecked),'scholarly_citation_counts':'absent'},
        'note_links':NOTE_LINKS, 'calibrations':CALIBRATIONS}}
    write(OUT/'evidence_index.json',index)
    write(OUT/'passage_index.json',{'author':'Dylan Riley','person':'Max Weber','passages':passages})
    # Full A sources and bounded readers; W windows grouped under held-copy UID.
    docs={it['uid']:(ROOT/it['path']).read_text() for it in selections}
    for it in json.loads((OUT/'reception_manifest.json').read_text()):docs[it['uid']]=(ROOT/it['path']).read_text()
    docs['citation_index']=json.dumps(index,ensure_ascii=False)
    write(OUT/'documents.json',docs)
    lines=['# Riley → Weber pilot provenance', '', 'Local Zotero opened read-only and immutable; Stacks is read-only. No database copy. All PDF text retains form feeds; the Stacks export is not a paginated witness.', '',
      f"Scanned {len(inventory['riley'])} Riley records. Selected {len(texts)} complete articles/chapters, {len(passages)} candidate name windows, {len(checks)} located pair candidates; {len(unchecked)} unchecked or linked windows. Eight held secondary texts; books use a contiguous densest 40k-character excerpt. Name windows are not exhaustive citation recall.", '',
      'No saved lane plan was found. pilot_plan.json is explicitly reconstructed from the Stacks estates guide and bundle 299; its questions and warnings are context, not findings. The comparison uses the unchanged estates memo, whose materials and historical availability differ.', '',
      '## Citing texts', '', '| UID | Year | Text | SHA256 |','|---|---|---|---|']
    lines += [f"| {i['uid']} | {i['year'] or 'unknown'} | {i['title']} | {i['sha256']} |" for i in selections]
    lines += ['', '## Page custody', '', 'Every evidence window records its exact pdftotext -f/-l command, PDF hash, output hash, how, section title and edition notes. The naive OCR edge map is not used for Roth/Wittich page lookup; inspected +110 and +13 calibrations are recorded in the index. MWG A180 is mapped explicitly to PDF625–626. Search results are candidate evidence and can be irrelevant.', '', 'selection.json records exclusions and boundaries; inventory.json records the original Zotero size/mtime; reception_manifest.json records excerpt offsets and hashes. Locally held copyrighted source texts remain under ignored data/study, with manifests and study outputs exported for review.']
    (OUT/'PROVENANCE.md').write_text('\n'.join(lines)+'\n')
    print('EVIDENCE',len(checks),'pairs',len(json.dumps(index)), 'chars; corpus',sum(map(len,docs.values())),flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["scan", "passages", "works", "reception", "evidence"])
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

    elif args.action == "evidence":
        build_evidence()
