"""Offline contract prototype. No production imports, model calls or semantic verdicts.

Checks normalized exports; does NOT prove applied critic history or adapter fidelity.
"""
from pathlib import Path
import hashlib,json,re
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent

def require(ok,why):
    if not ok:raise ValueError(why)
def uid(v):require(isinstance(v,str) and v and not re.search(r'\s|__|::',v),'invalid person UID')
def digest(t):return hashlib.sha256(t.encode()).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False)
def citable(row):return row['status']=='confirmed' and row['anchor_status']=='verified' and row['canonical_ref'] is None

def shape(data,name):
    errs=list(Draft202012Validator(json.loads((HERE/'fixtures'/name).read_text())).iter_errors(data))
    require(not errs,'schema: '+('; '.join(e.json_path+': '+e.message for e in errs[:3])))

def validate_packet(p,release=False):
    shape(p,'overlap_packet.schema.json')
    aids=[a['uid'] for a in p['authors']]; [uid(a) for a in aids]; require(len(set(aids))==2,'authors must differ')
    t=p['overlap_table']; require(t['authors']==p['authors'],'table author axis mismatch'); uid(t['uid'])
    require(t['approved'] and t['complete_union'],'approved complete union required for analytical admission')
    for k in ['coverage','residues','collective']:require(set(t[k])==set(aids),k+' must carry exactly both authors')
    people={r['uid']:r for r in t['rows']}; require(len(people)==len(t['rows']),'person collision')
    [uid(k) for k in people]; require(not set(aids)&set(people),'authors cannot be shared subjects')
    selected=set(t['selected']); require(len(selected)==len(t['selected']),'duplicate selected person')
    sources=p['source_documents']; excluded={x['key'] for x in t['excluded_coauthored']}
    require(len(excluded)==len(t['excluded_coauthored']),'duplicate excluded text')
    for x in t['excluded_coauthored']: require(set(x['author_uids'])==set(aids),'excluded coauthor identity')
    all_event_docs={}; all_events={a:set() for a in aids}; work_sets={a:set() for a in aids}; known_persons={a:set() for a in aids}
    synthetic=p['fixture_only'] or any(x['fixture_only'] for x in sources.values()) or any(x['fixture_only'] for x in t['rows'])
    for k,s in sources.items():
        require(digest(s['text'])==s['sha256'],'source hash mismatch: '+k)
        require(k not in excluded,'excluded coauthor source leaked')
        require(s['author_uid'] in aids if s['role']=='citing_author' else s['author_uid'] is None,'source role/author mismatch')
        require(not (set(aids)-{s['author_uid']}) & set(s['coauthors']),'coauthor source cannot supply other author')
    for a in aids:
        cv=t['coverage'][a]
        for k in ['held','inspected','missing','unknown_years']:require(len(set(cv[k]))==len(cv[k]),'duplicate coverage key')
        require(set(cv['inspected'])<=set(cv['held']),'inspected outside held')
        require(not set(cv['held'])&set(cv['missing']),'held/missing overlap')
        require(not (set(cv['held'])|set(cv['inspected']))&excluded,'coauthors leaked into universe')
        for k in cv['unknown_years']: require(k in sources and sources[k]['year'] is None,'false unknown year')
    threshold=t['settings']['min_events_per_side']; eligible=set(); below=set()
    for person,r in people.items():
        require(set(r['by_author'])==set(aids),'person missing author counts')
        for a,side in r['by_author'].items():
            events=side['events']; eids=[e['event_id'] for e in events]
            require(len(set(eids))==len(eids),'duplicate canonical event')
            require(side['count'] is None or side['count']>=0,'negative count')
            require(not events if side['count'] is None else side['count']==len(eids),'count differs from canonical events')
            if side['count'] is not None and side['count']>0:known_persons[a].add(person)
            if side['count']==0:require(t['coverage'][a]['ledger_complete'] and t['coverage'][a]['aliases_resolved'],'zero without checked aliases/corpus')
            for e in events:
                require(e['event_id'].startswith(a+'::'),'foreign event author')
                k=e['text_key']; require(k in sources and sources[k]['author_uid']==a and sources[k]['role']=='citing_author','event wrong author/source')
                require(k in t['coverage'][a]['inspected'],'event outside inspected coverage')
                require(e['year']==sources[k]['year'],'event/source year mismatch')
                require(e['kind'] in t['settings']['kinds'],'event outside selected kinds')
                evmeta=(k,e['year'],e['kind'],str(e['ref_id']))
                require(e['event_id'] not in all_event_docs or all_event_docs[e['event_id']]==evmeta,'canonical event identity conflict across persons')
                all_event_docs[e['event_id']]=evmeta; all_events[a].add(e['event_id'])
            works={w['key']:w for w in side['works']};require(len(works)==len(side['works']),'duplicate cited work')
            for w in works.values():
                expected={e['event_id'] for e in events if w['key'] in e['work_keys']}
                require(set(w['event_ids'])==expected and expected,'work/event mapping mismatch')
                require(not w['held'] or bool(w['copies']),'held work without copy')
                require(not w['fetched'] or w['held'],'fetched work not held')
                fld={'key':'key','registry_work':'registry_work_id','edition':'edition_id'}[t['settings']['work_rule']]
                if w[fld] is not None:work_sets[a].add(w[fld])
            require(all(set(e['work_keys'])<=set(works) for e in events),'event cites unlisted work')
        common=set(w['key'] for w in r['by_author'][aids[0]]['works']) & set(w['key'] for w in r['by_author'][aids[1]]['works'])
        require(set(r['common_work_keys'])==common,'false common work keys')
        counts=[r['by_author'][a]['count'] for a in aids]
        if all(v is not None and v>=threshold for v in counts):eligible.add(person)
        elif all(v is not None and v>0 for v in counts):below.add(person)
    require(selected<=eligible,'selected person below shared threshold')
    require(set(t['unselected_shared'])==eligible-selected,'unselected shared mismatch')
    require(set(t['below_threshold'])==below,'below threshold mismatch')
    require(len(t['below_threshold'])==len(below) and len(t['unselected_shared'])==len(eligible-selected),'duplicate derived person list')
    for a in aids:
        b=next(x for x in aids if x!=a)
        expected={k for k,r in people.items() if (r['by_author'][a]['count'] or 0)>0 and r['by_author'][b]['count']==0}
        r=t['residues'][a]; got=r['person_uids'];require(len(got)==len(set(got)),'duplicate residue')
        require(r['total']==len(expected) and set(got)<=expected,'residue false zero/total')
        require(r['omitted']==r['total']-len(got),'residue omitted mismatch')
        if r['completeness']=='all':require(set(got)==expected and r['top_n'] is None,'incomplete all residue')
        elif r['completeness']=='top_n':
            require(isinstance(r['top_n'],int) and r['top_n']>0,'invalid residue cutoff')
            ranked=sorted(expected,key=lambda k:(-people[k]['by_author'][a]['count'],k))[:r['top_n']]
            require(got==ranked,'residue rank/cutoff mismatch')
        else:require(not selected,'unknown residue completeness permits metadata report only')
        collective=t['collective'][a]['events']; ceids=[x['event_id'] for x in collective]
        require(len(ceids)==len(set(ceids)),'duplicate collective event')
        for e in collective:
            k=e['source_doc_key'];require(e['event_id'].startswith(a+'::') and e['event_id'] not in all_events[a],'collective allocated to person')
            require(k in sources and sources[k]['author_uid']==a and e['anchor'] in sources[k]['text'],'collective anchor/side mismatch')
    for field,sets in [('persons',known_persons),('works',work_sets)]:
        expected={'intersection':len(sets[aids[0]]&sets[aids[1]]),'union':len(sets[aids[0]]|sets[aids[1]])}
        require(t['metrics'][field]==expected,'wrong '+field+' intersection/union')
    refs={}; owners={}; pairkeys=set(); doc_keys=set()
    def check_ledger(l,owner_key,author=None,person=None):
        require(digest(l['artifact_text'])==l['artifact_sha256'],'artifact hash mismatch')
        require(bool(l['rows']) or (l['reviewed_empty'] and l.get('empty_reason')),'missing reviewed-empty ledger')
        require(not l['rows'] or not l['reviewed_empty'],'nonempty ledger labelled empty')
        for r in l['rows']:
            require(r['ref']==owner_key+'::'+l['engine_key']+'::'+r['row_id'],'row namespace mismatch')
            require(r['ref'] not in refs,'row reference collision')
            require(r['raw_row'] in l['artifact_text'],'raw row not in artifact')
            require(bool(r['anchors']) or not citable(r),'citable row without anchors')
            for anchor in r['anchors']:
                k=anchor['source_doc_key']; require(k in sources,'missing original source')
                if citable(r): require(anchor['text'] in sources[k]['text'] and anchor['text'] in r['raw_row'],'anchor not in original source and row')
                if author and sources[k]['role']=='citing_author':require(sources[k]['author_uid']==author,'pair anchor wrong author')
            if author:
                universe={e['event_id'] for e in people[person]['by_author'][author]['events']}
                require(set(r['event_ids'])<=universe,'row event outside author-person universe')
                if citable(r) and l['engine_key'] in {'citation_engagement_map','citation_overlap_map'}:
                    require(r['event_ids'] and any(sources[x['source_doc_key']]['author_uid']==author for x in r['anchors']),'side row lacks author event/anchor')
            refs[r['ref']]=r;owners[r['ref']]=(author,person,l['engine_key'])
    for pair in p['pairs']:
        a,person=pair['author_uid'],pair['member_uid'];key=pair['pair_key'];uid(a);uid(person)
        require(a in aids and person in selected,'foreign pair')
        require(key==a+'__'+person and key not in pairkeys,'pair key collision/mismatch');pairkeys.add(key)
        require(pair['doc_key']=='pair::'+key and pair['doc_key'] not in doc_keys,'pair document collision');doc_keys.add(pair['doc_key'])
        engines=[l['engine_key'] for l in pair['ledgers']]; require(len(set(engines))==len(engines),'duplicate engine ledger')
        require(bool(set(engines)&{'citation_overlap_map','citation_engagement_map'}),'missing side reading ledger')
        for engine,status in pair['lens_status'].items():require((status=='run')==(engine in engines),'lens completion mismatch')
        for l in pair['ledgers']:check_ledger(l,key,a,person)
        synthetic|=pair['fixture_only']
    require(pairkeys=={a+'__'+person for a in aids for person in selected},'missing selected author-person pair')
    maps=set()
    for m in p['shared_maps']:
        person=m['person_uid']; key=t['uid']+'__'+person
        require(person in selected and person not in maps,'duplicate/foreign shared map');maps.add(person)
        require(m['map_key']==key and m['doc_key']=='shared::'+key and m['doc_key'] not in doc_keys,'shared map identity');doc_keys.add(m['doc_key'])
        require(m['ledger']['engine_key']=='citation_overlap_map','wrong shared-map engine')
        check_ledger(m['ledger'],key,person=person)
        for r in m['ledger']['rows']:
            if not citable(r):continue
            support=r['fields'].get('support_refs',[])
            require(support and all(s in refs and citable(refs[s]) for s in support),'missing/rejected shared support')
            require({owners[s][0] for s in support}==set(aids) and {owners[s][1] for s in support}=={person},'shared support lacks both sides of same person')
            require({canon(x) for x in r['anchors']}=={canon(x) for s in support for x in refs[s]['anchors']},'shared row lost/invented inherited anchor')
            require(set(r['event_ids'])=={e for s in support for e in refs[s]['event_ids']},'shared event ancestry mismatch')
        synthetic|=m['fixture_only']
    require(maps==selected,'missing selected shared map')
    for ref,r in refs.items():
        if r['canonical_ref'] is not None:require(r['canonical_ref'] in refs and citable(refs[r['canonical_ref']]),'bad canonical reference')
    for pair in p['pairs']:
        for table in pair['tables']:require(all(r in refs and citable(refs[r]) for r in table['row_refs']),'pair table rejected/missing row')
    require(not synthetic or p['fixture_only'],'mixed synthetic packet must be fixture_only')
    if release:require(not synthetic,'synthetic packet cannot be release evidence')
    metadata={'person:'+k:canon(v) for k,v in people.items()}
    metadata.update({'coverage:'+a:canon(t['coverage'][a]) for a in aids})
    metadata.update({'residue:'+a:canon(t['residues'][a]) for a in aids})
    metadata.update({'collective:'+a:canon(t['collective'][a]) for a in aids})
    metadata['settings']=canon(t['settings']);metadata['metrics']=canon(t['metrics'])
    return {'refs':refs,'owners':owners,'metadata':metadata}

def validate_output(p,out,release=False):
    state=validate_packet(p,release=release);shape(out,'overlap_output.schema.json')
    require(out['packet_id']==p['packet_id'] and out['revision']==p['revision'],'stale output packet')
    require(out['fixture_only']==p['fixture_only'],'output fixture flag mismatch')
    refs=state['refs'];owners=state['owners'];metadata=state['metadata'];ids={}
    aids={a['uid'] for a in p['authors']}
    for f in out['findings']:
        require(f['id'] not in ids,'duplicate output ID');ids[f['id']]=f
        require(set(f['metadata_refs'])<=set(metadata),'missing metadata reference; plan not evidence')
        require(all(r in refs and citable(refs[r]) for r in f['row_refs']),'output rejected/missing row')
        if f['kind']=='metadata':
            require(f['metadata_refs'] and not f['row_refs'] and not f['anchors'],'metadata cannot be substantive evidence');continue
        require(f['row_refs'],'substantive finding needs row refs')
        expected={canon(a) for ref in f['row_refs'] for a in refs[ref]['anchors']}
        require({canon(a) for a in f['anchors']}==expected,'output lost/invented inherited anchors')
        expanded=set()
        for ref in f['row_refs']:
            if owners[ref][0] is None:expanded.update(refs[ref]['fields']['support_refs'])
            else:expanded.add(ref)
        grid={(owners[r][0],owners[r][1]) for r in expanded}
        persons={v[1] for v in grid}; authors={v[0] for v in grid}
        require(set(f['person_uids'])==persons and set(f['author_uids'])==authors,'output identity declaration differs from witnesses')
        require(authors==aids and grid=={(a,b) for a in aids for b in persons},'incomplete author-person support grid')
        if f['kind'] in {'cross_person','period','fidelity'}:require(len(persons)>=2,'two shared persons required')
        for a,person in grid:
            keys={x['source_doc_key'] for r in expanded if owners[r][:2]==(a,person) for x in refs[r]['anchors'] if p['source_documents'][x['source_doc_key']]['author_uid']==a}
            require(keys,'missing citing-author anchor in grid cell')
            if f['kind']=='period':
                years={p['source_documents'][k]['year'] for k in keys}-{None}
                require(len(keys)>=2 and len(years)>=2,'period lacks distinct dated endpoints for each author-person pair')
        if f['kind']=='fidelity':
            for ref in expanded:
                r=refs[ref];a,person,engine=owners[ref]
                require(engine=='citation_fidelity_audit' and r['fields'].get('verdict') in {'accurate','fair','selective','stretched','misattributed'},'fidelity needs assessed audit rows')
                require(any(p['source_documents'][x['source_doc_key']]['role']=='primary_window' for x in r['anchors']),'fidelity lacks P witness')
                require(r['fields'].get('how') in {'page','section','search'},'audit missing how')
    residue_refs=set()
    for t in out['tables']:
        for cell in t['cells']:
            require(cell['finding_ids'] or cell['metadata_refs'],'unreferenced table cell')
            require(set(cell['finding_ids'])<=set(ids) and set(cell['metadata_refs'])<=set(metadata),'stale/rejected table cell')
            if t['key']=='residues_by_side':residue_refs.update(cell['metadata_refs'])
    expected={'person:'+u for block in p['overlap_table']['residues'].values() for u in block['person_uids']}
    require(expected<=residue_refs,'final residue table omitted a supplied residue')
    return True
