"""Offline definition checks. Imports only new project modules, never live src/.

Copies execute the existing loaders and schemas with relative import relocation
and an explicit no-op history writer. SHA receipts pin every original body.
"""
import hashlib
import importlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT/'communications/study/cohort_2026_09_06'
DATA = ROOT/'data/study/cohort_2026_09_06'
sys.path.insert(0, str(DATA))
EngineRegistry = importlib.import_module('cohort_loader_snapshot.engine_registry').EngineRegistry
OperationalizationRegistry = importlib.import_module('cohort_loader_snapshot.op_registry').OperationalizationRegistry
KEY = 'citation_cohort_synthesis'


class OneDefinitionDirectory:
    """Let the unchanged registry read exactly the supplied communications file."""
    def __init__(self, file): self.file = file
    def exists(self): return self.file.exists()
    def glob(self, pattern):
        assert pattern == '*.yaml'
        return [self.file]


class DefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = EngineRegistry(definitions_dir=STUDY/'unused_definitions')
        registry.capability_definitions_dir = OneDefinitionDirectory(STUDY/f'{KEY}.capability.yaml')
        cls.cap = registry.get_capability_definition(KEY)
        cls.op = OperationalizationRegistry(OneDefinitionDirectory(STUDY/f'{KEY}.operationalization.yaml')).get(KEY)

    def test_existing_loaders_accept_candidates(self):
        self.assertIsNotNone(self.cap)
        self.assertIsNotNone(self.op)
        self.assertIn('family: analytical', (STUDY/f'{KEY}.capability.yaml').read_text())  # legacy capability loader ignores this catalogue metadata
        self.assertEqual(self.cap.engine_key,self.op.engine_key)
        self.assertEqual({d.key for d in self.cap.analytical_dimensions},{d.key for d in self.op.process.dimensions})

    def test_depths_and_model_routes(self):
        self.assertEqual([self.op.mode_for_depth(d) for d in ['surface','standard','deep']],['oneshot','oneshot_checked','dvs'])
        self.assertEqual(self.op.process.routing,{'cheap':'openrouter/openai/gpt-5.6-luna','mid':'openrouter/deepseek/deepseek-v4-pro','strong':'openrouter/openai/gpt-5.6-sol'})
        self.assertEqual([s.kind for s in self.op.process.steps],['extract','verify','synthesize'])

    def test_question_card_and_evidence_identity_contract(self):
        dims=self.op.process.dimensions
        self.assertEqual(len({d.id_prefix for d in dims}),len(dims))
        for d in dims:
            self.assertTrue(d.questions)
            self.assertTrue(d.method_card.startswith('Do:'))
            self.assertIn('anchor:',d.answer_shape)
            if d.scope=='corpus':
                self.assertIn('pair-row-b:',d.answer_shape)
                self.assertIn('doc-b:',d.answer_shape)
                self.assertIn('at least two distinct engaged member keys',d.method_card)
        self.assertTrue(next(d for d in dims if d.key=='cross_member_reliance').load_bearing)
        self.assertEqual(len(self.op.process.final_step.tables),5)

    def test_snapshots_are_pinned_and_no_protected_imports(self):
        for entry in json.loads((DATA/'cohort_loader_snapshot/manifest.json').read_text()):
            self.assertEqual(hashlib.sha256((ROOT/entry['source']).read_bytes()).hexdigest(),entry['source_sha256'])
            self.assertEqual(hashlib.sha256((DATA/'cohort_loader_snapshot'/entry['snapshot']).read_bytes()).hexdigest(),entry['snapshot_sha256'])
        self.assertFalse(any(k.startswith(('src.executor','src.dossier','src.engines','src.operationalizations','src.sources')) for k in sys.modules))

if __name__=='__main__': unittest.main()
