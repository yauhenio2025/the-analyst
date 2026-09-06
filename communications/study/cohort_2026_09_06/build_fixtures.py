"""Build deliberately synthetic shape fixtures. Never label these release evidence."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def load_harness():
    patch = (HERE/'patches/030_cohort_harness.patch').read_text()
    body = patch.split('@@\n',1)[1]
    code = '\n'.join(line[1:] for line in body.splitlines() if line.startswith('+'))+'\n'
    ns = {'__name__':'cohort_fixture_harness'}
    exec(compile(code,'<new cohort harness patch>','exec'),ns)
    return ns


def example():
    h=load_harness(); sha=h['sha']; ENG=h['ENG']; FID=h['FID']; REC=h['REC']
    members=[]; pairs=[]; sources={}
    for n,letter in enumerate(('P','Q','N')):
        engaged=letter!='N'; u='fixture:'+letter
        counts={'total':int(engaged),'mentions':0,'bibliography_only':0,'by_text':[]}
        if engaged: counts['by_text']=[{'text_key':'fixture:text'+letter,'year':2000 if letter=='P' else None,'count':1,'event_ids':['fixture:event'+letter]}]
        m={'uid':u,'name':'Fixture '+letter,'membership_role':'fixture_comparator','membership_reason':'Invented solely to test shape; no historical membership.','membership_source':'fixture_definition','engaged':'yes' if engaged else 'no','counts':counts,'works_cited':[],'row_id':'COHORT.M'+str(n+1),'anchor':f'member: {u}; engaged: {"yes" if engaged else "no"}; count: {int(engaged)}; membership: fixture comparator.','fixture_only':True}
        members.append(m)
        if not engaged: continue
        text=f"I adopt {letter}'s distinction, but only for this example." if letter=='P' else "We dispute Q's example, while retaining its qualification."
        key='fixture:text'+letter
        sources[key]={'text':text+'\nFixture context; this is not Riley or any scholar.','sha256':sha(text+'\nFixture context; this is not Riley or any scholar.')}
        pair_key='fixture:A__'+u
        raw=f'[D3.F1] The fixture author uses {letter} on this proposition. — dim: citation_move — anchor: "{text}" — doc: {key}'
        row={'row_id':'D3.F1','ref':pair_key+'::'+ENG+'::D3.F1','dimension':'citation_move','claim':f'The fixture author uses {letter} on this proposition.','raw_row':raw,'status':'confirmed','anchor_status':'verified','canonical_ref':None,'event_ids':['fixture:event'+letter], 'anchors':[{'text':text,'source_doc_key':key,'locus':{'printed_page':'1','pdf_page':2,'section_uid':None,'section_title':None,'edition':'fixture','how':'page'},'voice':'A' if letter=='P' else 'A and coauthor'}], 'fields':{'move':'adopted_framework' if letter=='P' else 'foil','stance':'adopts' if letter=='P' else 'disputes','year':2000 if letter=='P' else None,'text_key':key}}
        alias=copy.deepcopy(row);alias.update(row_id='D3.F2',ref=pair_key+'::'+ENG+'::D3.F2',canonical_ref=row['ref'],status='superseded',raw_row=raw.replace('[D3.F1]','[D3.F2]'))
        artifact=raw+'\n'+alias['raw_row']
        pair={'pair_key':pair_key,'doc_key':'pair::'+pair_key,'author_uid':'fixture:A','member_uid':u,'fixture_only':True,'ledgers':[{'engine_key':ENG,'artifact_id':'fixture-artifact-'+letter,'artifact_sha256':sha(artifact),'artifact_text':artifact,'rows':[row,alias],'reviewed_empty':False}], 'lens_status':{ENG:'run',FID:'not_run',REC:'not_run'},'tables':[{'table_key':'passage_move_stance_locus','markdown':'Fixture table points to its canonical row.','row_refs':[row['ref']]}], 'memo':{'markdown':'Fixture memo: see canonical pair row; this is a restatement.','canonical_uri':'fixture://pair/'+letter}}
        pairs.append(pair)
    packet={'schema_version':'cohort-packet/v1','packet_id':'fixture-cohort-only','revision':1,'fixture_only':True,'author':{'uid':'fixture:A','name':'Fixture author; not Riley'},'cohort':{'role':'cohort','doc_key':'context:cohort','uid':'fixture:cohort','phrase':'Synthetic shape cohort, never a release cohort','approved':True,'members':members,'not_engaged_residue':['fixture:N'],'coverage':{'ledger_snapshot':'fixture-ledger-v1','count_unit':'canonical_citation_event','complete':True,'identities_resolved':True,'held_texts':list(sources),'inspected_texts':list(sources),'missing_texts':[],'date_range':[2000,None],'alias_scope':'All fixture identities explicitly listed','coauthorship':{'fixture:textQ':['fixture:A','fixture:coauthor']}},'collective_mentions':[]},'plan':{'role':'plan','doc_key':'context:plan','sections':[{'id':'reading','title':'Compare the supplied uses','questions':['Which member is a premise and which a foil?']}],'themes':[{'key':'example','label':'Example','origin':'plan_spine'}],'warnings':['Synthetic fixture only','Preserve coauthorship and the unknown date','No inference of historical membership']},'pairs':pairs,'source_documents':sources}
    evidence=[{'pair_row_ref':p['ledgers'][0]['rows'][0]['ref'],'anchors':copy.deepcopy(p['ledgers'][0]['rows'][0]['anchors'])} for p in pairs]
    findings=[]
    for n,m in enumerate(members):
        findings.append({'id':'C2.F'+str(n+1),'dimension':'cohort_residue','claim':m['anchor'],'members':[m['uid']],'status':'confirmed','evidence':[],'cohort_evidence':[{'row_id':m['row_id'],'anchor':m['anchor']}]})
    findings.append({'id':'C3.F1','dimension':'cross_member_reliance','claim':'The invented P is adopted and the invented Q is disputed, with qualifications.','members':['fixture:P','fixture:Q'],'status':'confirmed','evidence':evidence,'cohort_evidence':[]})
    def cell(column,text,ids=None): return {'column':column,'text':text,'kind':'supported' if ids else 'unknown','finding_ids':ids or []}
    tables=[]
    tables.append({'key':'member_text_year_counts','columns':['member','counts'],'rows':[{'member_uid':m['uid'],'text_key':m['counts']['by_text'][0]['text_key'] if m['counts']['by_text'] else None,'year':m['counts']['by_text'][0]['year'] if m['counts']['by_text'] else None,'count':m['counts']['total'],'cells':[cell('member',m['name'],['C2.F'+str(n+1)]),cell('counts',str(m['counts']['total']),['C2.F'+str(n+1)])]} for n,m in enumerate(members)]})
    tables.append({'key':'member_move_stance','columns':['reading'],'rows':[{'member_uid':m['uid'],'cells':[cell('reading','The cited fixture proposition and qualification.',['C3.F1'])]} for m in members[:2]]})
    tables.append({'key':'fidelity_by_member','columns':['member','verdict'],'rows':[{'member_uid':m['uid'],'cells':[cell('member',m['name'],['C2.F'+str(n+1)]),cell('verdict','not run')]} for n,m in enumerate(members[:2])]})
    tables.append({'key':'not_engaged_members','columns':['member','status'],'rows':[{'member_uid':'fixture:N','cells':[cell('member','Fixture N',['C2.F3']),cell('status','not engaged in the checked fixture corpus',['C2.F3'])]}]})
    tables.append({'key':'cohort_periods','columns':['period'],'rows':[{'member_uid':None,'cells':[cell('period','unresolved')]}]})
    output={'schema_version':'cohort-output/v1','packet_id':packet['packet_id'],'packet_revision':1,'fixture_only':True,'mode':'oneshot_checked','findings':findings,'tables':tables,'prose':[{'text':findings[-1]['claim'],'finding_ids':['C3.F1']},{'text':'Fixture N is not engaged in the checked invented corpus.','finding_ids':['C2.F3']}],'markdown':''}
    output['markdown']=h['render_output'](output)
    h['validate_output'](packet,output)
    return packet,output


def schema():
    # The harness supplies cross-field checks. Strict object keys make mistakes visible.
    def obj(properties,required=None): return {'type':'object','properties':properties,'required':required or list(properties),'additionalProperties':False}
    S={'type':'string','minLength':1}; B={'type':'boolean'}; N={'type':'integer','minimum':0}
    def arr(item): return {'type':'array','items':item}
    anchor=obj({'text':S,'source_doc_key':S,'locus':{'type':'object'},'voice':S})
    row=obj({'row_id':S,'ref':S,'dimension':S,'claim':S,'raw_row':S,'status':{'enum':['confirmed','rejected','unresolved','superseded']},'anchor_status':{'enum':['verified','failed','unverifiable']},'canonical_ref':{'type':['string','null']},'event_ids':arr(S),'anchors':arr(anchor),'fields':{'type':'object'}})
    ledger=obj({'engine_key':{'enum':['citation_engagement_map','citation_fidelity_audit','citation_reception_map']},'artifact_id':S,'artifact_sha256':{'type':'string','pattern':'^[a-f0-9]{64}$'},'artifact_text':{'type':'string'},'rows':arr(row),'reviewed_empty':B,'empty_reason':S},required=['engine_key','artifact_id','artifact_sha256','artifact_text','rows','reviewed_empty'])
    countrow=obj({'text_key':S,'year':{'type':['integer','null']},'count':N,'event_ids':arr(S)})
    member=obj({'uid':S,'name':S,'membership_role':S,'membership_reason':S,'membership_source':S,'engaged':{'enum':['yes','no','unknown']},'counts':obj({'total':{'type':['integer','null'],'minimum':0},'mentions':N,'bibliography_only':N,'by_text':arr(countrow)}),'works_cited':arr({'type':'object'}),'row_id':S,'anchor':S,'fixture_only':B})
    pair=obj({'pair_key':S,'doc_key':S,'author_uid':S,'member_uid':S,'fixture_only':B,'ledgers':arr(ledger),'lens_status':obj({k:{'enum':['run','not_run','unavailable']} for k in ['citation_engagement_map','citation_fidelity_audit','citation_reception_map']}),'tables':arr(obj({'table_key':S,'markdown':{'type':'string'},'row_refs':arr(S)})),'memo':obj({'markdown':{'type':'string'},'canonical_uri':S})})
    result=obj({'schema_version':{'const':'cohort-packet/v1'},'packet_id':S,'revision':N,'fixture_only':B,'author':obj({'uid':S,'name':S}),'cohort':obj({'role':{'const':'cohort'},'doc_key':{'const':'context:cohort'},'uid':S,'phrase':S,'approved':B,'members':arr(member),'not_engaged_residue':dict(arr(S),uniqueItems=True),'coverage':obj({'ledger_snapshot':S,'count_unit':{'const':'canonical_citation_event'},'complete':B,'identities_resolved':B,'held_texts':arr(S),'inspected_texts':arr(S),'missing_texts':arr(S),'date_range':arr({'type':['integer','null']}),'alias_scope':S,'coauthorship':{'type':'object'}}),'collective_mentions':arr({'type':'object'})}),'plan':obj({'role':{'const':'plan'},'doc_key':{'const':'context:plan'},'sections':arr(obj({'id':S,'title':S,'questions':arr(S)})),'themes':arr(obj({'key':S,'label':S,'origin':{'enum':['plan_spine','reader_addition']}})),'warnings':arr(S)}),'pairs':arr(pair),'source_documents':{'type':'object','additionalProperties':obj({'text':S,'sha256':{'type':'string','pattern':'^[a-f0-9]{64}$'}})}})
    return dict(result,**{'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:the-analyst:cohort-packet:v1','title':'Cohort packet v1; fixture_only forbids release'})

if __name__=='__main__':
    packet,output=example()
    for name,value in [('synthetic_packet.json',packet),('synthetic_output.json',output),('cohort_packet.schema.json',schema())]:
        (HERE/'fixtures'/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
