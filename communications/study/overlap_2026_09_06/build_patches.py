"""Generate proposed diffs from pinned git blobs without editing protected files."""
from pathlib import Path
import difflib,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
BASE=json.loads((HERE/'input_receipt.json').read_text())['base_commit']

def candidate_sources():
 path='src/sources/citation_evidence.py'
 before=subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT,text=True)
 after=before.replace('"citation_reception_map"}', '"citation_reception_map", "citation_overlap_map"}',1)
 old='    if not indexes:\n        return documents, ""\n'
 new='''    if engine_key == "citation_overlap_map":
        return _prepare_overlap_sources(documents, indexes)
    if any("authors" in obj for _, obj in indexes):
        raise ValueError("two-author index requires citation_overlap_map or an explicit author slice")
'''+old
 assert old in after
 after=after.replace(old,new,1)+'\n\n'+(HERE/'index_extension.py').read_text()
 return path,before,after

def build():
 entries=[]
 def emit(name,path,before,after):
  diff=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='a/'+path,tofile='b/'+path))
  (HERE/'patches'/name).write_text(f'# Deferred proposal. Base: {BASE}. Recheck newer HEAD before applying.\n'+diff)
  entries.append({'patch':name,'path':path,'base_commit':BASE,'base_sha256':hashlib.sha256(before.encode()).hexdigest(),'candidate_sha256':hashlib.sha256(after.encode()).hexdigest()})
 emit('010_two_author_evidence_index.patch',*candidate_sources())
 path='src/sources/schemas.py'; before=subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT,text=True)
 old=re.search(r'^SourceRole = Literal\[.*\]$',before,re.M).group(0)
 values=json.loads('['+old.split('[',1)[1])
 for role in ['cohort','cohort_table','overlap_table']:
  if role not in values:values.append(role)
 after=before.replace(old,'SourceRole = Literal['+', '.join(json.dumps(v) for v in values)+']')
 emit('020_source_roles.patch',path,before,after)
 path='src/dossier/catalog_purpose.json'; before=subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT,text=True)
 data=json.loads(before)
 def visit(obj):
  if isinstance(obj,dict):
   if obj.get('title')=='Trace the citations': return obj
   for v in obj.values():
    found=visit(v)
    if found:return found
  if isinstance(obj,list):
   for v in obj:
    found=visit(v)
    if found:return found
 group=visit(data); assert group
 items=next(v for v in group.values() if isinstance(v,list) and v and isinstance(v[0],dict) and 'engine_key' in v[0])
 for key,name,use,yields,unit in [
 ('citation_overlap_map','two authors on a shared figure','both authors have independently authored passages citing the same person, with an approved overlap table','works overlap, per-passage moves and stances, topics, dated trajectories and qualified asymmetry with both authors’ anchors','one row per side passage or supported cross-author finding'),
 ('citation_overlap_synthesis','the shared citation canon','completed shared-person maps and both side ledgers with approved counts, residues and collective blocks','argued joint reliance and asymmetry, canon hypotheses, disagreements, periods, scoped residues and per-side audited fidelity','one row per supported cross-person finding or scoped metadata report')]:
  items.append(dict(engine_key=key,plain_name=name,use_when=use,yields=yields,row_unit=unit,deliverable_kinds=['briefing','case_file'],pairs_with=['citation_overlap_synthesis' if key.endswith('_map') else 'citation_overlap_map'],fit='ok',fit_note='Offer only after the documented real source/owner-first/both-order gate; requires author-aware adapter and provenance admission.'))
 emit('090_catalogue_offer_after_validation.patch',path,before,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 (HERE/'patches/design_patch_baselines.json').write_text(json.dumps(entries,indent=2)+'\n')
if __name__=='__main__':build()
