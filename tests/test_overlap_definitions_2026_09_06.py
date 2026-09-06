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
STUDY = ROOT/'communications/study/overlap_2026_09_06'
DATA = STUDY
sys.path.insert(0, str(DATA))
EngineRegistry = importlib.import_module('overlap_loader_snapshot.engine_registry').EngineRegistry
OperationalizationRegistry = importlib.import_module('overlap_loader_snapshot.op_registry').OperationalizationRegistry
KEYS = ['citation_overlap_map', 'citation_overlap_synthesis']

class OneDefinitionDirectory:
    def __init__(self, file): self.file=file
    def exists(self): return self.file.exists()
    def glob(self, pattern): return [self.file]

class DefinitionTests(unittest.TestCase):
    def test_existing_loaders_accept_both_candidates(self):
        for key in KEYS:
            registry=EngineRegistry(definitions_dir=STUDY/'unused_definitions')
            registry.capability_definitions_dir=OneDefinitionDirectory(STUDY/f'{key}.capability.yaml')
            cap=registry.get_capability_definition(key)
            op=OperationalizationRegistry(OneDefinitionDirectory(STUDY/f'{key}.operationalization.yaml')).get(key)
            self.assertIsNotNone(cap); self.assertIsNotNone(op)
            self.assertEqual(cap.engine_key,op.engine_key)
            self.assertEqual({d.key for d in cap.analytical_dimensions},{d.key for d in op.process.dimensions})
            self.assertEqual([op.mode_for_depth(d) for d in ['surface','standard','deep']],['oneshot','oneshot_checked','dvs'])
            self.assertEqual(op.process.routing,{'cheap':'openrouter/openai/gpt-5.6-luna','mid':'openrouter/deepseek/deepseek-v4-pro','strong':'openrouter/openai/gpt-5.6-sol'})
            self.assertEqual([s.kind for s in op.process.steps],['extract','verify','synthesize'])
            self.assertEqual(len({d.id_prefix for d in op.process.dimensions}),len(op.process.dimensions))
            for d in op.process.dimensions:
                self.assertTrue(d.questions); self.assertTrue(d.method_card.startswith('Do:'))
                self.assertIn('anchor:',d.answer_shape)
            self.assertEqual(len(op.process.final_step.tables),7 if key.endswith('synthesis') else 4)

    def test_snapshots_are_pinned(self):
        for entry in json.loads((DATA/'overlap_loader_snapshot/manifest.json').read_text()):
            self.assertEqual(hashlib.sha256((ROOT/entry['source']).read_bytes()).hexdigest(),entry['source_sha256'])
            self.assertEqual(hashlib.sha256((DATA/'overlap_loader_snapshot'/entry['snapshot']).read_bytes()).hexdigest(),entry['snapshot_sha256'])

    def test_full_method_appendix_matches_design(self):
        self.assertIn((STUDY/'METHOD_APPENDIX.md').read_text(),(STUDY/'DESIGN_shared_citations_overlap_2026-09-06.md').read_text())

if __name__=='__main__': unittest.main()
