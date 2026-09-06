"""Offline adversarial contract fixtures; no runtime/provider calls."""
from copy import deepcopy
import importlib.util,json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1];STUDY=ROOT/'communications/study/overlap_2026_09_06'
spec=importlib.util.spec_from_file_location('overlap_guard',STUDY/'validate_overlap.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
def packet():return json.loads((STUDY/'fixtures/synthetic_packet.json').read_text())
def output():return json.loads((STUDY/'fixtures/synthetic_output.json').read_text())

def test_synthetic_packet_and_source_linked_output():assert guard.validate_output(packet(),output())

@pytest.mark.parametrize('mutation',[
 lambda p:p.update(authors=list(reversed(p['authors']))),
 lambda p:p['pairs'].pop(),
 lambda p:p['shared_maps'].pop(),
 lambda p:p['pairs'][0].update(author_uid='fixture:B'),
 lambda p:p['pairs'][0]['ledgers'][0].update(engine_key='citation_fidelity_audit'),
 lambda p:p['pairs'][0]['ledgers'][0].update(artifact_sha256='0'*64),
 lambda p:p['pairs'][0]['ledgers'][0]['rows'][0]['anchors'][0].update(text='Invented quote'),
 lambda p:p['pairs'][0]['ledgers'][0]['rows'][0].update(status='rejected'),
 lambda p:p['source_documents'].pop(next(iter(p['source_documents']))),
 lambda p:p['source_documents'][next(iter(p['source_documents']))].update(author_uid='fixture:B'),
 lambda p:p['source_documents'][next(iter(p['source_documents']))].update(coauthors=['fixture:B']),
 lambda p:p['overlap_table']['rows'][0]['by_author']['fixture:A'].update(count=999),
 lambda p:p['overlap_table']['rows'][0].update(common_work_keys=['made-up-equivalence']),
 lambda p:p['overlap_table']['residues'].pop('fixture:A'),
 lambda p:p['overlap_table']['residues']['fixture:A'].update(person_uids=[]),
 lambda p:p['overlap_table']['residues']['fixture:A'].update(person_uids=['fixture:P']),
 lambda p:p['overlap_table']['coverage']['fixture:B'].update(aliases_resolved=False),
 lambda p:p['overlap_table']['collective'].pop('fixture:B'),
 lambda p:p['overlap_table'].update(complete_union=False),
 lambda p:p['overlap_table']['metrics']['works'].update(intersection=999),
 lambda p:p['overlap_table']['settings'].update(min_events_per_side=3),
 lambda p:p['shared_maps'][0]['ledger']['rows'][0]['fields'].update(support_refs=[]),
 lambda p:p['shared_maps'][0]['ledger']['rows'][0]['fields']['support_refs'].pop(),
 lambda p:p['shared_maps'][0]['ledger']['rows'][0]['anchors'].pop(),
 lambda p:p.update(fixture_only=False),
])
def test_invalid_packet_refuses(mutation):
 p=packet();mutation(p)
 with pytest.raises(ValueError):guard.validate_packet(p)

@pytest.mark.parametrize('mutation',[
 lambda o:o.update(revision=999),
 lambda o:o['findings'][0]['anchors'].pop(),
 lambda o:o['findings'][0].update(author_uids=['fixture:A']),
 lambda o:o['findings'][0]['row_refs'].pop(),
 lambda o:o['findings'][0].update(row_refs=['made-up']),
 lambda o:o['findings'][0].update(metadata_refs=['context:plan']),
 lambda o:o['tables'][0]['cells'][0].update(finding_ids=['rejected-id']),
 lambda o:o['tables'][1]['cells'].pop(),
 lambda o:o['findings'][0].update(kind='fidelity'),
 lambda o:o.update(fixture_only=False),
])
def test_invalid_output_refuses(mutation):
 o=output();mutation(o)
 with pytest.raises(ValueError):guard.validate_output(packet(),o)

def test_two_authors_on_one_person_do_not_make_two_shared_persons():
 p=packet();o=output();o['findings'][0]['row_refs']=o['findings'][0]['row_refs'][:1];o['findings'][0]['person_uids']=['fixture:P'];o['findings'][0]['anchors']=p['shared_maps'][0]['ledger']['rows'][0]['anchors']
 with pytest.raises(ValueError,match='two shared persons'):guard.validate_output(p,o)
 o['findings'][0]['kind']='single_person';assert guard.validate_output(p,o)

def test_period_requires_all_four_author_person_cells_at_two_dates():
 p=packet();o=output();o['findings'][0]['kind']='period';assert guard.validate_output(p,o)
 # Keep source and event years consistent while removing one cell's temporal contrast.
 pair=p['pairs'][0];key=pair['ledgers'][0]['rows'][1]['fields']['text_key'];p['source_documents'][key]['year']=None
 p['overlap_table']['rows'][0]['by_author']['fixture:A']['events'][1]['year']=None
 with pytest.raises(ValueError,match='dated endpoints'):guard.validate_output(p,o)

def test_release_rejects_all_synthetic_and_mixed_fixtures():
 for mixed in [False,True]:
  p=packet()
  if mixed:
   p['pairs'][0]['fixture_only']=False
   for s in p['source_documents'].values():
    if s['author_uid']=='fixture:A':s['fixture_only']=False
  with pytest.raises(ValueError,match='synthetic'):guard.validate_packet(p,release=True)

def test_top_n_is_explicit_and_below_threshold_is_not_residue():
 p=packet();r=p['overlap_table']['residues']['fixture:A'];r.update(completeness='top_n',top_n=1);guard.validate_packet(p)
 # Raise threshold above both shared counts, explicitly deselect; persons stay positive below threshold.
 p['overlap_table']['settings']['min_events_per_side']=3;p['overlap_table']['selected']=[];p['overlap_table']['below_threshold']=['fixture:P','fixture:Q'];p['pairs']=[];p['shared_maps']=[]
 guard.validate_packet(p)
 assert p['overlap_table']['residues']['fixture:A']['person_uids']==['fixture:R_A']
