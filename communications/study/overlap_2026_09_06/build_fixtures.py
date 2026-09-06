"""Build self-contained schemas and explicitly synthetic evidence/outputs; no providers."""
from pathlib import Path
from copy import deepcopy
import hashlib,json
HERE=Path(__file__).resolve().parent
S={'type':'string','minLength':1}; N={'type':'integer','minimum':0}; B={'type':'boolean'}
def arr(v):return {'type':'array','items':v}
def obj(fields,optional=()):return {'type':'object','properties':fields,'required':[k for k in fields if k not in optional],'additionalProperties':False}
def enum(*values):return {'enum':list(values)}
def nullable(t):return {'type':[t,'null']}
def sha(text):return hashlib.sha256(text.encode()).hexdigest()
def dump(name,data): (HERE/'fixtures'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def schemas():
 cohort=json.loads((HERE.parent/'cohort_2026_09_06/fixtures/cohort_packet.schema.json').read_text())
 pair=deepcopy(cohort['properties']['pairs']['items']); ledger=pair['properties']['ledgers']['items']; row=ledger['properties']['rows']['items']; anchor=row['properties']['anchors']['items']
 ledger['properties']['engine_key']['enum'].append('citation_overlap_map')
 pair['properties']['lens_status']['properties']['citation_overlap_map']=enum('run','not_run','unavailable')
 pair['properties']['lens_status']['required'].append('citation_overlap_map')
 identity=obj({'uid':S,'name':S})
 event=obj({'event_id':S,'ref_id':{'type':['string','integer']},'text_key':S,'year':nullable('integer'),'kind':enum('reference','footnote','intext','mention','bibliography_only'),'work_keys':arr(S)})
 work=obj({'key':S,'title':S,'registry_work_id':nullable('string'),'edition_id':nullable('string'),'event_ids':arr(S),'held':B,'fetched':B,'wanted':B,'copies':arr(obj({'key':S,'edition':nullable('string'),'how':enum('works','library','resolve','editions')}))})
 side=obj({'count':nullable('integer'),'events':arr(event),'works':arr(work)})
 per= {'type':'object','additionalProperties':side}
 member=obj({'uid':S,'name':S,'fixture_only':B,'by_author':per,'common_work_keys':arr(S)})
 coverage=obj({'held':arr(S),'inspected':arr(S),'missing':arr(S),'unknown_years':arr(S),'ledger_complete':B,'aliases_resolved':B,'snapshot':S})
 residue=obj({'person_uids':arr(S),'total':N,'completeness':enum('all','top_n','unknown'),'top_n':nullable('integer'),'omitted':N})
 collective=obj({'terms':arr(S),'events':arr(obj({'event_id':S,'source_doc_key':S,'anchor':S,'locus':{'type':'object'}})),'analysis_status':enum('not_run','unavailable')})
 metrics=obj({'intersection':N,'union':N})
 table=obj({'role':{'const':'overlap_table'},'doc_key':{'const':'context:overlap'},'uid':S,'approved':B,'complete_union':B,'authors':arr(identity),'settings':obj({'min_events_per_side':{'type':'integer','minimum':1},'work_rule':enum('key','registry_work','edition'),'coauthored_policy':{'const':'exclude_both'},'kinds':arr(S),'types':arr(S),'self_citations':B}), 'rows':arr(member),'selected':arr(S),'selection_changes':arr(obj({'person_uid':S,'action':enum('add','strike'),'reason':S})), 'below_threshold':arr(S),'unselected_shared':arr(S),'coverage':{'type':'object','additionalProperties':coverage},'residues':{'type':'object','additionalProperties':residue},'collective':{'type':'object','additionalProperties':collective},'excluded_coauthored':arr(obj({'key':S,'author_uids':arr(S),'events':N})), 'metrics':obj({'persons':metrics,'works':metrics}), 'costs':obj({'total_usd':nullable('number'),'status':enum('measured','unmeasured')})})
 src=obj({'text':S,'sha256':{'type':'string','pattern':'^[a-f0-9]{64}$'},'author_uid':nullable('string'),'role':enum('citing_author','primary_window','secondary_reader'),'year':nullable('integer'),'coauthors':arr(S),'fixture_only':B})
 shared=obj({'person_uid':S,'map_key':S,'doc_key':S,'fixture_only':B,'ledger':ledger,'memo':pair['properties']['memo']})
 schema=obj({'schema_version':{'const':'overlap-packet/v1'},'packet_id':S,'revision':N,'fixture_only':B,'authors':dict(arr(identity),minItems=2,maxItems=2),'overlap_table':table,'plan':cohort['properties']['plan'],'pairs':arr(pair),'shared_maps':arr(shared),'source_documents':{'type':'object','additionalProperties':src}})
 schema['$schema']='https://json-schema.org/draft/2020-12/schema';dump('overlap_packet.schema.json',schema)
 finding=obj({'id':S,'dimension':S,'kind':enum('single_person','cross_person','period','fidelity','metadata'),'claim':S,'person_uids':arr(S),'author_uids':arr(S),'row_refs':arr(S),'anchors':arr(anchor),'metadata_refs':arr(S)})
 output=obj({'schema_version':{'const':'overlap-output/v1'},'packet_id':S,'revision':N,'fixture_only':B,'findings':arr(finding),'tables':arr(obj({'key':S,'cells':arr(obj({'value':S,'finding_ids':arr(S),'metadata_refs':arr(S)}))}))})
 dump('overlap_output.schema.json',output)
 return pair

def ledger(rows,identity,engine='citation_overlap_map'):
 raw='\n'.join(r['raw_row'] for r in rows)
 return dict(engine_key=engine,artifact_id='fixture:artifact:'+identity,artifact_text=raw,artifact_sha256=sha(raw),rows=rows,reviewed_empty=not rows,**({'empty_reason':'Fixture reviewed empty'} if not rows else {}))
def anchor(text,key):return dict(text=text,source_doc_key=key,voice='fixture author',locus={'printed_page':'1','pdf_page':2,'edition':'fixture','how':'page','section_uid':None,'section_title':None})
def row(ref,text,anchors,events,fields,dim='passage_use'):
 raw='['+ref.rsplit('::',1)[-1]+'] '+text+' — anchors: '+' | '.join(a['text'] for a in anchors)
 return dict(row_id=ref.rsplit('::',1)[-1],ref=ref,dimension=dim,claim=text,raw_row=raw,status='confirmed',anchor_status='verified',canonical_ref=None,event_ids=events,anchors=anchors,fields=fields)

def build():
 schemas()
 authors=[dict(uid='fixture:A',name='Fixture first author'),dict(uid='fixture:B',name='Fixture second author')]; aids=[a['uid'] for a in authors]
 p=dict(schema_version='overlap-packet/v1',packet_id='fixture:overlap',revision=1,fixture_only=True,authors=authors,plan=dict(role='plan',doc_key='context:plan',sections=[dict(id='reliance',title='Shared arguments?',questions=['What changes across the two fixture authors?'])],themes=[],warnings=['All passages and persons are synthetic.']),pairs=[],shared_maps=[],source_documents={})
 rows=[]
 for person in ['fixture:P','fixture:Q','fixture:R_A','fixture:R_B']:
  member=dict(uid=person,name=person+' (synthetic)',fixture_only=True,by_author={},common_work_keys=[])
  supports=[]
  for ai,author in enumerate(aids):
   count=2 if person in ['fixture:P','fixture:Q'] else int((person=='fixture:R_A' and ai==0) or (person=='fixture:R_B' and ai==1))
   events=[]; prows=[]; works={}
   pairkey=author+'__'+person
   for n in range(count):
    key=f'{author}:text:{person}:{n}'; eid=f'{author}::{person}-{n}'; year=2000+n*10 if person!='fixture:R_B' else None
    wk=person+':work'+('shared' if person=='fixture:P' else str(ai))
    text=f'[p. 1 | PDF p. 2] {author} fixture only: '+(f'I adopt {person} on {wk} for this example.' if ai==0 else f'I dispute {person} on {wk} for this example.')+f' Observation {n}.'
    p['source_documents'][key]=dict(text=text,sha256=sha(text),author_uid=author,role='citing_author',year=year,coauthors=[],fixture_only=True)
    events.append(dict(event_id=eid,ref_id=n+1,text_key=key,year=year,kind='footnote',work_keys=[wk]))
    works.setdefault(wk,dict(key=wk,title='Synthetic cited work',registry_work_id=None,edition_id=None,event_ids=[],held=False,fetched=False,wanted=True,copies=[]))['event_ids'].append(eid)
    ref=pairkey+'::citation_overlap_map::O2.F'+str(n+1)
    prows.append(row(ref,'Synthetic proposition', [anchor(text,key)],[eid],dict(move='authority' if ai==0 else 'foil',stance='adopts' if ai==0 else 'disputes',text_key=key,year=year,work_key=wk)))
   member['by_author'][author]=dict(count=count,events=events,works=list(works.values()))
   if person in ['fixture:P','fixture:Q']:
    supports+=prows
    p['pairs'].append(dict(pair_key=pairkey,doc_key='pair::'+pairkey,author_uid=author,member_uid=person,fixture_only=True,ledgers=[ledger(prows,pairkey)],lens_status={k:('run' if k=='citation_overlap_map' else 'not_run') for k in ['citation_overlap_map','citation_engagement_map','citation_fidelity_audit','citation_reception_map']},tables=[],memo=dict(markdown='Fixture side projection, not an independent memo.',canonical_uri='fixture://'+pairkey)))
  member['common_work_keys']=sorted(set(w['key'] for w in member['by_author'][aids[0]]['works']) & set(w['key'] for w in member['by_author'][aids[1]]['works']))
  rows.append(member)
  if supports:
   mk='fixture:universe__'+person; ref=mk+'::citation_overlap_map::O5.F1'
   r=row(ref,'Fixture A adopts what fixture B disputes.',[a for s in supports for a in s['anchors']],[e for s in supports for e in s['event_ids']],dict(support_refs=[s['ref'] for s in supports],verdict='authority_vs_foil'),dim='asymmetry_verdict')
   p['shared_maps'].append(dict(person_uid=person,map_key=mk,doc_key='shared::'+mk,fixture_only=True,ledger=ledger([r],mk),memo=dict(markdown='Synthetic comparison.',canonical_uri='fixture://'+mk)))
 table=dict(role='overlap_table',doc_key='context:overlap',uid='fixture:universe',approved=True,complete_union=True,authors=authors,settings=dict(min_events_per_side=1,work_rule='key',coauthored_policy='exclude_both',kinds=['footnote'],types=['article'],self_citations=False),rows=rows,selected=['fixture:P','fixture:Q'],selection_changes=[],below_threshold=[],unselected_shared=[],coverage={},residues={},collective={},excluded_coauthored=[dict(key='fixture:joint',author_uids=aids,events=4)],metrics={'persons':{'intersection':2,'union':4},'works':{'intersection':1,'union':5}},costs=dict(total_usd=None,status='unmeasured'))
 for i,a in enumerate(aids):
  keys=[k for k,v in p['source_documents'].items() if v['author_uid']==a]
  table['coverage'][a]=dict(held=keys,inspected=keys,missing=[],unknown_years=[k for k in keys if p['source_documents'][k]['year'] is None],ledger_complete=True,aliases_resolved=True,snapshot='fixture:snapshot')
  table['residues'][a]=dict(person_uids=['fixture:R_A' if i==0 else 'fixture:R_B'],total=1,completeness='all',top_n=None,omitted=0)
  table['collective'][a]=dict(terms=[],events=[],analysis_status='not_run')
 p['overlap_table']=table
 dump('synthetic_packet.json',p)
 refs=[r['ref'] for m in p['shared_maps'] for r in m['ledger']['rows']]
 anchors=[a for m in p['shared_maps'] for r in m['ledger']['rows'] for a in r['anchors']]
 f=dict(id='S2.F1',dimension='joint_reliance',kind='cross_person',claim='Fixture authority/foil contrast spans P and Q.',person_uids=table['selected'],author_uids=aids,row_refs=refs,anchors=anchors,metadata_refs=[])
 out=dict(schema_version='overlap-output/v1',packet_id=p['packet_id'],revision=p['revision'],fixture_only=True,findings=[f],tables=[dict(key='joint_reliance_asymmetries',cells=[dict(value=f['claim'],finding_ids=[f['id']],metadata_refs=[])]),dict(key='residues_by_side',cells=[dict(value=r, finding_ids=[],metadata_refs=['person:'+r]) for r in ['fixture:R_A','fixture:R_B']])])
 dump('synthetic_output.json',out)
 index=dict(role='evidence_index',version='overlap-index/v1',authors=authors,person=dict(uid='fixture:P',name='Fixture person'),texts=[],checks=[],unchecked=[],readers=[],roles={},plan={'questions':['How does each author use P?']})
 for a in aids:
  key='ATEXT' if a.endswith('A') else 'BTEXT'; index['roles'][key]='citing_author'
  index['texts'].append(dict(uid='em:'+key,key=key,author=a,coauthored_with=[],title='Fixture citing text',year=2000,passages=[dict(ref_id=5505,event_id=a+'::e5505',hit='Fixture '+a+' passage about P.',before='',after='',locus={'printed':1,'pdf':2,'how':'verbatim'},work={'key':'fixture:work'})]))
  index['checks'].append(dict(author=a,ref_ids=[5505],work_key='fixture:work',title='Fixture P work',copy={'uid':'em:PWORK','key':'PWORK','edition':'fixture'},windows=[{'how':'page','printed':[1],'text':'Fixture P primary witness.'}]))
 index['roles'].update(PWORK='primary_window',READER='secondary_reader')
 dump('synthetic_two_author_index.json',index)
if __name__=='__main__':build()
