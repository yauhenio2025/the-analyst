"""Assemble a MIXED plumbing fixture only after an explicit completed-pilot export.

The caller supplies the real-side canonical count/coverage table in a one-person
seed, source-role metadata and a fixture-only second author. No essay parsing,
identity guessing, event manufacture or historical comparison is performed.
"""
from copy import deepcopy
import hashlib,json
from validate_overlap import validate_packet, require, citable
PILOT='dossier-bdc5eb48c407'

def assemble(job, export, seed, *, riley_uid, weber_uid, source_metadata):
    require(job.get('id')==PILOT and job.get('status')=='done','completed requested pilot required')
    require(export.get('job_id')==PILOT,'export job does not match pilot')
    require(export.get('receipt',{}).get('gaps')==[],'export has missing or undeclared provenance gaps')
    require(export.get('author',{}).get('uid')==riley_uid,'explicit Riley identity mismatch')
    p=deepcopy(seed); t=p['overlap_table']; pair=deepcopy(export['pair'])
    require(t['selected']==[weber_uid],'pilot fixture is exactly one shared person')
    require(pair['author_uid']==riley_uid and pair['member_uid']==weber_uid,'pilot pair identity mismatch')
    others=[a for a in p['authors'] if a['uid']!=riley_uid]
    require(len(others)==1 and others[0]['name']=='Fixture second author','second author must be explicitly fixture-only')
    b=others[0]['uid']; require(b.startswith('fixture:'),'fixture author namespace required')
    bpair=next((x for x in p['pairs'] if x['author_uid']==b and x['member_uid']==weber_uid),None)
    require(bpair is not None and bpair['fixture_only'],'missing synthetic second-author pair')
    require(set(source_metadata)==set(export['source_documents']),'complete explicit source-role metadata required')
    # Remove seed witnesses from the real side; never edit the export's literal bytes.
    p['source_documents']={k:v for k,v in p['source_documents'].items() if v['author_uid']==b}
    for k,doc in export['source_documents'].items():
        require(k not in p['source_documents'],'real/synthetic document collision')
        require(not source_metadata[k]['fixture_only'],'pilot original source cannot be synthetic')
        p['source_documents'][k]=dict(doc,**source_metadata[k])
    pair['lens_status'].setdefault('citation_overlap_map','not_run')
    p['pairs']=[pair,bpair];p['fixture_only']=True
    support=[]
    for side in p['pairs']:
        found=[r for l in side['ledgers'] if l['engine_key'] in {'citation_engagement_map','citation_overlap_map'} for r in l['rows'] if citable(r)]
        require(found,'each fixture side needs an admissible passage row')
        support.append(found[0])
    key=t['uid']+'__'+weber_uid; ref=key+'::citation_overlap_map::O5.F1'
    anchors=[deepcopy(a) for r in support for a in r['anchors']]
    raw='[O5.F1] Fixture-only paired support; no historical cross-author verdict. — anchors: '+' | '.join(a['text'] for a in anchors)
    row=dict(row_id='O5.F1',ref=ref,dimension='asymmetry_verdict',claim='Fixture-only paired support; no historical cross-author verdict.',raw_row=raw,status='confirmed',anchor_status='verified',canonical_ref=None,event_ids=[e for r in support for e in r['event_ids']],anchors=anchors,fields={'support_refs':[r['ref'] for r in support],'verdict':'unresolved'})
    ledger=dict(engine_key='citation_overlap_map',artifact_id='fixture:pilot-comparator',artifact_text=raw,artifact_sha256=hashlib.sha256(raw.encode()).hexdigest(),rows=[row],reviewed_empty=False)
    p['shared_maps']=[dict(person_uid=weber_uid,map_key=key,doc_key='shared::'+key,fixture_only=True,ledger=ledger,memo={'markdown':'Fixture-only comparator scaffolding.', 'canonical_uri':'fixture://pilot-comparator'})]
    validate_packet(p)
    return p
