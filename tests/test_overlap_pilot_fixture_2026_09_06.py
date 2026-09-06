"""Synthetic tests for the future completed-pilot assembler, never a real export."""
from copy import deepcopy
from pathlib import Path
import json,sys
import pytest
STUDY=Path(__file__).resolve().parents[1]/'communications/study/overlap_2026_09_06';sys.path.insert(0,str(STUDY))
from assemble_pilot_fixture import assemble,PILOT
from validate_overlap import validate_packet

def args():
 p=json.loads((STUDY/'fixtures/synthetic_packet.json').read_text())
 p['overlap_table']['selected']=['fixture:P'];p['overlap_table']['unselected_shared']=['fixture:Q']
 pair=deepcopy(p['pairs'][0]);pair['fixture_only']=False
 docs={k:v for k,v in p['source_documents'].items() if v['author_uid']=='fixture:A'}
 meta={k:{x:v[x] for x in ['author_uid','role','year','coauthors','fixture_only']} for k,v in docs.items()}
 for m in meta.values():m['fixture_only']=False  # simulate real export in a fixture-only test
 exp={'job_id':PILOT,'author':p['authors'][0],'pair':pair,'source_documents':{k:{x:v[x] for x in ['text','sha256']} for k,v in docs.items()},'receipt':{'gaps':[]}}
 return {'job':{'id':PILOT,'status':'done'},'export':exp,'seed':p,'riley_uid':'fixture:A','weber_uid':'fixture:P','source_metadata':meta}

def test_mixed_fixture_preserves_real_export_bytes_and_cannot_release():
 a=args();out=assemble(**a)
 assert out['fixture_only'] and len(out['shared_maps'])==1
 assert out['pairs'][0]['ledgers']==a['export']['pair']['ledgers']
 with pytest.raises(ValueError,match='synthetic'):validate_packet(out,release=True)

@pytest.mark.parametrize('mutation',[
 lambda a:a['job'].update(status='analysis'),
 lambda a:a['job'].update(id='another-job'),
 lambda a:a['export']['receipt'].update(gaps=['critic history not exported']),
 lambda a:a['export'].pop('receipt'),
 lambda a:a['seed']['authors'][1].update(name='Robert Brenner'),
 lambda a:a.update(riley_uid='invented'),
 lambda a:a['source_metadata'].clear(),
])
def test_missing_export_or_disguised_second_author_refuses(mutation):
 a=args();mutation(a)
 with pytest.raises(ValueError):assemble(**a)
