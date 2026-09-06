"""Check pinned diffs using an alternate Git index, without applying to any files."""
from pathlib import Path
import ast,hashlib,json,os,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1];STUDY=ROOT/'communications/study/overlap_2026_09_06'

def apply_in_memory(before,patch):
 import re
 lines=before.splitlines(True);out=[];pos=0;items=patch.splitlines(True);i=0
 while i<len(items):
  if not items[i].startswith('@@ '):i+=1;continue
  m=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',items[i]);assert m
  start=int(m[1])-1;out+=lines[pos:start];pos=start;i+=1
  while i<len(items) and not items[i].startswith('@@ '):
   line=items[i];i+=1
   if line.startswith(' '):assert lines[pos]==line[1:];out.append(lines[pos]);pos+=1
   elif line.startswith('-'):assert lines[pos]==line[1:];pos+=1
   elif line.startswith('+'):out.append(line[1:])
   else:raise AssertionError('unexpected patch line')
 out+=lines[pos:];return ''.join(out)

def candidates():
 manifest=json.loads((STUDY/'patches/design_patch_baselines.json').read_text());out={}
 for e in manifest:
  before=subprocess.check_output(['git','show',e['base_commit']+':'+e['path']],cwd=ROOT,text=True)
  assert hashlib.sha256(before.encode()).hexdigest()==e['base_sha256']
  after=apply_in_memory(before,(STUDY/'patches'/e['patch']).read_text())
  assert hashlib.sha256(after.encode()).hexdigest()==e['candidate_sha256']
  out[e['path']]=after
 return manifest,out

def test_patch_bytes_hashes_and_combined_git_check():
 manifest,_=candidates()
 with tempfile.TemporaryDirectory(prefix='.patch-check-',dir=STUDY) as d:
  env=dict(os.environ,GIT_INDEX_FILE=str(Path(d)/'index'))
  subprocess.run(['git','read-tree',manifest[0]['base_commit']],cwd=ROOT,env=env,check=True,capture_output=True)
  subprocess.run(['git','apply','--cached','--check',*[str(STUDY/'patches'/e['patch']) for e in manifest]],cwd=ROOT,env=env,check=True,capture_output=True)

def test_source_roles_preserve_existing_and_add_only_wire_spellings():
 _,c=candidates();tree=ast.parse(c['src/sources/schemas.py'])
 assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SourceRole' for t in n.targets))
 roles=[x.value for x in assignment.value.slice.elts]
 assert len(roles)==len(set(roles)) and set(roles)=={'source','evidence_index','plan','profile','statements','cohort','cohort_table','overlap_table'}

def test_catalogue_preserves_trace_family_and_offers_two_candidates_only():
 _,c=candidates();data=json.loads(c['src/dossier/catalog_purpose.json']);serialized=json.dumps(data)
 for key in ['citation_engagement_map','citation_fidelity_audit','citation_reception_map','citation_overlap_map','citation_overlap_synthesis']:assert key in serialized
 def groups(x):
  if isinstance(x,dict):
   if x.get('title')=='Trace the citations':yield x
   for v in x.values():yield from groups(v)
  if isinstance(x,list):
   for v in x:yield from groups(v)
 found=list(groups(data));assert len(found)==1
 for key in ['citation_overlap_map','citation_overlap_synthesis']:
  assert json.dumps(found[0]).count('"engine_key": "'+key+'"')==1
 compile(c['src/sources/citation_evidence.py'],'deferred_index_candidate','exec')
