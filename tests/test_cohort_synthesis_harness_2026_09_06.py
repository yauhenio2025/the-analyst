"""Execute only our new deferred script in memory; adversarial provenance controls."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'communications/study/cohort_2026_09_06'
spec=importlib.util.spec_from_file_location('new_cohort_fixtures',STUDY/'build_fixtures.py')
fixtures=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
H=fixtures.load_harness()


class HarnessTests(unittest.TestCase):
    def setUp(self): self.packet,self.output=fixtures.example()
    def fail_packet(self, mutate):
        mutate(self.packet)
        with self.assertRaises((H['ContractError'],KeyError,TypeError)): H['validate_packet'](self.packet)
    def fail_output(self, mutate):
        mutate(self.output)
        self.output['markdown']=H['render_output'](self.output)
        with self.assertRaises(H['ContractError']): H['validate_output'](self.packet,self.output)
    def test_valid_packet_and_reviewed_tables(self):
        self.assertTrue(H['validate_output'](self.packet,self.output)['shape_pass'])
    def test_schema_matches_packet(self):
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(fixtures.schema())
        jsonschema.validate(self.packet,fixtures.schema())
    def test_fixture_cannot_release(self):
        with self.assertRaises(H['ContractError']): H['validate_output'](self.packet,self.output,release=True)
    def test_missing_engagement_ledger(self): self.fail_packet(lambda p:p['pairs'][0]['ledgers'].clear())
    def test_missing_pair(self): self.fail_packet(lambda p:p['pairs'].pop())
    def test_missing_residue(self): self.fail_packet(lambda p:p['cohort'].pop('not_engaged_residue'))
    def test_dropped_residue(self): self.fail_packet(lambda p:p['cohort']['not_engaged_residue'].clear())
    def test_false_zero(self): self.fail_packet(lambda p:p['cohort']['coverage'].update(complete=False))
    def test_count_is_not_finding_count(self): self.fail_packet(lambda p:p['cohort']['members'][0]['counts'].update(total=2))
    def test_foreign_author(self): self.fail_packet(lambda p:p['pairs'][0].update(author_uid='fixture:Other'))
    def test_duplicate_pair(self): self.fail_packet(lambda p:p['pairs'].append(copy.deepcopy(p['pairs'][0])))
    def test_duplicate_row(self): self.fail_packet(lambda p:p['pairs'][0]['ledgers'][0]['rows'].append(copy.deepcopy(p['pairs'][0]['ledgers'][0]['rows'][0])))
    def test_invented_carried_anchor(self): self.fail_packet(lambda p:p['pairs'][0]['ledgers'][0]['rows'][0]['anchors'][0].update(text='An invented quotation.'))
    def test_wrong_source_identity(self): self.fail_packet(lambda p:p['pairs'][0]['ledgers'][0]['rows'][0]['anchors'][0].update(source_doc_key='fixture:textQ'))
    def test_missing_original_source(self): self.fail_packet(lambda p:p['source_documents'].pop('fixture:textP'))
    def test_artifact_mutation(self): self.fail_packet(lambda p:p['pairs'][0]['ledgers'][0].update(artifact_text='different raw ledger'))
    def test_rejected_pair_table_cell(self): self.fail_packet(lambda p:p['pairs'][0]['ledgers'][0]['rows'][0].update(status='rejected'))
    def test_alias_cannot_be_cited_as_another_witness(self):
        alias=self.packet['pairs'][0]['ledgers'][0]['rows'][1]
        self.fail_output(lambda o:o['findings'][-1]['evidence'][0].update(pair_row_ref=alias['ref']))
    def test_same_member_twice_is_not_cross_member(self):
        def change(o):
            o['findings'][-1]['members']=['fixture:P']
            o['findings'][-1]['evidence']=[copy.deepcopy(o['findings'][-1]['evidence'][0])]*2
        self.fail_output(change)
    def test_fresh_output_quote(self): self.fail_output(lambda o:o['findings'][-1]['evidence'][0]['anchors'][0].update(text='new quote'))
    def test_reading_nonengaged_member(self): self.fail_output(lambda o:o['findings'][-1]['members'].append('fixture:N'))
    def test_plan_cannot_be_evidence(self): self.fail_output(lambda o:o['findings'][-1]['evidence'][0].update(pair_row_ref='context:plan'))
    def test_fidelity_without_audits(self): self.fail_output(lambda o:o['findings'][-1].update(id='C6.F1',dimension='school_fidelity'))
    def test_period_without_endpoints(self): self.fail_output(lambda o:o['findings'][-1].update(id='C5.F1',dimension='school_periodization'))
    def test_rejected_final_table_cell(self): self.fail_output(lambda o:o['tables'][0]['rows'][0]['cells'][0].update(finding_ids=['C3.F999']))
    def test_unknown_cell_cannot_hide_reading(self): self.fail_output(lambda o:o['tables'][-1]['rows'][0]['cells'][0].update(text='The school was abandoned.'))
    def test_final_residue_is_complete(self): self.fail_output(lambda o:o['tables'][3]['rows'].clear())
    def test_table_attribution_reversal(self): self.fail_output(lambda o:o['tables'][0]['rows'][0].update(member_uid='fixture:Q'))
    def test_actual_markdown_must_match_checked_cells(self):
        self.output['markdown']+='\nA stale unsupported conclusion [C3.F999].'
        with self.assertRaises(H['ContractError']): H['validate_output'](self.packet,self.output)
    def test_one_pair_is_allowed_but_has_no_cohort_comparison(self):
        self.packet['pairs'].pop()
        self.packet['cohort']['members'].pop(1)
        self.assertEqual(len(H['validate_packet'](self.packet)['pairs']),1)
    def test_explicit_empty_residue_is_valid(self):
        self.packet['cohort']['members'].pop()
        self.packet['cohort']['not_engaged_residue']=[]
        H['validate_packet'](self.packet)
    def test_no_engaged_members_yields_metadata_only(self):
        self.packet['pairs']=[]
        self.packet['cohort']['members']=self.packet['cohort']['members'][-1:]
        self.assertFalse(H['validate_packet'](self.packet)['pairs'])

if __name__=='__main__': unittest.main()
