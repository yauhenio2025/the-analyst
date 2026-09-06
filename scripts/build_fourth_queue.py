"""Install frozen fourth-queue capabilities and processes behind the offer exclusion."""
from pathlib import Path
import json
import yaml
ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT/'communications/study/fourth_queue_2026_09_06'

def build():
    designs = json.loads((ARCHIVE/'designs.json').read_text())
    methods = {m['id']: m for f in json.loads((ROOT/'data/study/triage/families_codex.json').read_text()) for m in f['methods']}
    for ident, design in designs.items():
        key = design['key']; method = methods[ident]
        prior = json.loads((ARCHIVE/f'original_definitions/{design["old"]}.json').read_text())
        cap = dict(engine_key=key, engine_name=method['name'], version=2 if key == design['old'] else 1,
            category=prior['category'], kind='synthesis', problematique=design['ideal']+' '+method['scope'],
            researcher_question=method['reader_question'], intellectual_lineage={'primary':'source_criticism'},
            analytical_dimensions=[dict(key=d['key'],description=d['name'],probing_questions=d['questions'])
                for d in design['process']['dimensions'] if d['scope']=='document'],
            apps=['critic'], function='genealogy', family='analytical', legacy_engine_key=design['old'])
        op = dict(engine_key=key,engine_name=method['name'],stance_operationalizations=[],
            depth_sequences=[{'depth_key':depth,'mode':mode} for depth,mode in [('surface','oneshot'),('standard','oneshot_checked'),('deep','dvs')]]+[{'depth_key':'dvs','process':'dvs'}],process=design['process'])
        for folder, obj in [('engines/capability_definitions',cap),('operationalizations/definitions',op)]:
            path=ROOT/f'src/{folder}/{key}.yaml'
            if path.exists():
                raise RuntimeError(f'Refusing to overwrite existing definition: {path}')
            path.write_text('# Fourth queue: communications/study/REDESIGN_fourth_queue_2026-09-06.md\n'+yaml.safe_dump(obj,sort_keys=False,allow_unicode=True,width=110))
    path=ROOT/'src/dossier/catalog_purpose.json';catalog=json.loads(path.read_text())
    for d in designs.values():
        catalog['excluded'].append({'engine_key':d['key'],'why':'Fourth queue research definition; withheld pending source-read validation. See communications/study/REDESIGN_fourth_queue_2026-09-06.md.'})
    path.write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__': build()
