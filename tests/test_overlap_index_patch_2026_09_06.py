"""Exercise the complete proposed adapter in memory, leaving protected paths untouched."""
from copy import deepcopy
import importlib.util,json,subprocess
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1];STUDY=ROOT/'communications/study/overlap_2026_09_06'
spec=importlib.util.spec_from_file_location('overlap_patch_builder',STUDY/'build_patches.py');builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
_,_,CANDIDATE=builder.candidate_sources()
# Execute real unchanged memo-statements adapter in memory, without src imports.
MEMO={};exec(compile(subprocess.check_output(['git','show',builder.BASE+':src/sources/memo_statements.py'],cwd=ROOT,text=True),'memo_statements_snapshot','exec'),MEMO)
NS={'statements_documents':MEMO['statements_documents']}
exec(compile(CANDIDATE.replace('    from src.sources.memo_statements import statements_documents\n',''),'candidate_citation_evidence','exec'),NS)
prepare=NS['prepare_citation_sources'];slice_index=NS['slice_overlap_index']

def index():return json.loads((STUDY/'fixtures/synthetic_two_author_index.json').read_text())
def docs(i=None,**extra):return {'index':json.dumps(i or index()),**extra}

def test_two_authors_same_ref_id_and_one_primary_copy():
 s,c=prepare('citation_overlap_map',docs())
 assert set(s)=={'em:ATEXT','em:BTEXT','em:PWORK'}
 assert 'CITING AUTHOR UID: fixture:A' in s['em:ATEXT']
 assert 'CITING AUTHOR UID: fixture:B' in s['em:BTEXT']
 assert '5505' in c and 'fixture:A::e5505' in c and 'fixture:B::e5505' in c
 assert 'Fixture P primary witness.' not in c

def test_full_text_meets_uid_key_and_header_without_extra_witness():
 s,c=prepare('citation_overlap_map',docs(ATEXT='Full A source.',arbitrary='ZOTERO UID: em:BTEXT\nFull B source.',PWORK='Full P source.',READER='Reader words.'))
 assert set(s)=={'ATEXT','arbitrary','PWORK'}
 assert 'Full A source.' in s['ATEXT'] and 'Full B source.' in s['arbitrary']
 assert s['PWORK'].count('Fixture P primary witness.')==1
 assert '"supplied_as": "arbitrary"' in c

def test_table_and_plan_never_become_source_documents():
 i=index();table={'role':'overlap_table','authors':i['authors']}
 s,c=prepare('citation_overlap_map',docs(i,table=json.dumps(table),plan=json.dumps({'role':'plan','questions':['plan hypothesis']})))
 assert 'table' not in s and 'plan' not in s and 'plan hypothesis' in c

@pytest.mark.parametrize('mutation',[
 lambda i:i.update(author={'uid':'fixture:A'}),
 lambda i:i.update(authors=[i['authors'][0],i['authors'][0]]),
 lambda i:i['texts'][1].pop('author'),
 lambda i:i['texts'][1].update(author='fixture:C'),
 lambda i:i['texts'][1].update(coauthored_with=['fixture:A']),
 lambda i:i['texts'][1].update(uid='em:ATEXT',key='ATEXT'),
 lambda i:i['roles'].update(ATEXT='primary_window'),
 lambda i:i['roles'].update({'em:ATEXT':'primary_window'}),
 lambda i:i['texts'][1]['passages'][0].update(event_id='fixture:A::e5505'),
 lambda i:i['checks'][1].update(ref_ids=[999]),
 lambda i:i['checks'][0]['copy'].update(uid='em:ATEXT',key='ATEXT'),
 lambda i:i['checks'][0]['windows'][0].update(how='memory'),
 lambda i:i['unchecked'].append({'author':'fixture:B','ref_id':999}),
])
def test_bad_author_identity_role_event_or_witness_is_rejected(mutation):
 i=index();mutation(i)
 with pytest.raises(ValueError):prepare('citation_overlap_map',docs(i))

@pytest.mark.parametrize('extra',[
 {'ATEXT':'A','em:ATEXT':'A'},
 {'ATEXT':'SOURCE ROLE: primary_window\nA'},
 {'ATEXT':'SOURCE ROLE: citing_author\nCITING AUTHOR UID: fixture:B\nA'},
 {'unclassified':'unknown actor'},
])
def test_bad_supplied_sources_are_rejected(extra):
 with pytest.raises(ValueError):prepare('citation_overlap_map',docs(**extra))

def test_wrong_table_axis_and_multiple_indexes_refuse():
 i=index()
 with pytest.raises(ValueError):prepare('citation_overlap_map',docs(i,table=json.dumps({'role':'overlap_table','authors':list(reversed(i['authors']))})))
 with pytest.raises(ValueError):prepare('citation_overlap_map',docs(i,index2=json.dumps(i)))

def test_overlap_cannot_pool_authors_in_old_engine_and_slices_are_explicit():
 i=index()
 for engine in ['citation_engagement_map','citation_fidelity_audit','citation_reception_map']:
  with pytest.raises(ValueError):prepare(engine,docs(i))
 a=slice_index(i,'fixture:A');assert 'authors' not in a and a['author']['uid']=='fixture:A'
 assert len(a['texts'])==len(a['checks'])==1 and a['checks'][0]['author']=='fixture:A'
 assert 'BTEXT' not in a['roles']
 s,_=prepare('citation_fidelity_audit',docs(a));assert set(s)=={'em:ATEXT','em:PWORK'}
 assert i==index()

def test_existing_one_author_tests_run_against_candidate_without_live_imports():
 text=(ROOT/'tests/test_citation_index_meets_supplied_2026_09_06.py').read_text()
 ns={'prepare_citation_sources':prepare};exec(compile(text.replace('from src.sources.citation_evidence import prepare_citation_sources',''),'legacy_index_tests','exec'),ns)
 tests=[v for k,v in ns.items() if k.startswith('test_')]
 assert len(tests)==4
 for test in tests:test()

def test_existing_memo_statement_mode_survives():
 o={'memo':{'uid':'fixture:memo','title':'Fixture memo'},'statements':[{'no':1,'section':'test','statement':'A statement.','sources':['S1']}],'sources':[{'uid':'fixture:source','label':'S1','title':'A source','text':'Source words.'}]}
 s,_=prepare('citation_fidelity_audit',{'statements':json.dumps(o)})
 assert set(s)=={'fixture:memo','fixture:source'}

def test_uid_and_key_cannot_resolve_to_different_supplied_documents():
 i=index();i['texts'][0]['key']='ANOTHER';i['roles']['ANOTHER']='citing_author'
 with pytest.raises(ValueError,match='different physical'):
  prepare('citation_overlap_map',docs(i,ATEXT='A source',ANOTHER='Different source'))

def test_claimed_held_check_without_source_or_windows_refuses():
 i=index()
 for c in i['checks']:c['windows']=[]
 with pytest.raises(ValueError,match='neither supplied copy'):
  prepare('citation_overlap_map',docs(i))
