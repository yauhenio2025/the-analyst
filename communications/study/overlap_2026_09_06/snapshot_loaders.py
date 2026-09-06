"""Make isolated, new-file copies of existing loaders; never import the live package.

The engine registry's automatic history hook is replaced with a no-op. All loader
and schema bodies are unchanged except package-relative imports. See manifest.
"""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT/'communications/study/overlap_2026_09_06/overlap_loader_snapshot'
SOURCES = {
 'stage_schemas.py': 'src/stages/schemas.py',
 'composition_roles.py': 'src/engines/composition_roles.py',
 'engine_schemas.py': 'src/engines/schemas.py',
 'capability_schemas.py': 'src/engines/schemas_v2.py',
 'engine_registry.py': 'src/engines/registry.py',
 'op_schemas.py': 'src/operationalizations/schemas.py',
 'op_registry.py': 'src/operationalizations/registry.py',
}

def main():
 DEST.mkdir(parents=True,exist_ok=True)
 manifest=[]
 for filename,original in SOURCES.items():
  before=(ROOT/original).read_text()
  after=before.replace('from ..stages.schemas import','from .stage_schemas import').replace('from src.engines.schemas import','from .engine_schemas import').replace('from src.engines.schemas_v2 import','from .capability_schemas import')
  if filename=='capability_schemas.py': after=after.replace('from .schemas import','from .engine_schemas import')
  if filename=='op_registry.py': after=after.replace('from .schemas import','from .op_schemas import')
  (DEST/filename).write_text(after)
  manifest.append({'snapshot':filename,'source':original,'source_sha256':hashlib.sha256(before.encode()).hexdigest(),'snapshot_sha256':hashlib.sha256(after.encode()).hexdigest()})
 (DEST/'__init__.py').write_text('"""Isolated loader snapshots created for the cohort design test."""\n')
 (DEST/'history_tracker.py').write_text('"""Disable only the production registry history-write hook in this snapshot."""\ndef check_and_record_changes(definition):\n    return None\n')
 (DEST/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__': main()
