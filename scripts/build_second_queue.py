"""Install the frozen second-queue designs; no provider calls or release decisions."""
from pathlib import Path
import json
import yaml
ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / 'communications/study/second_queue_2026_09_06/designs.json'

def build():
    designs = json.loads(DESIGN.read_text())
    families = {m['id']: m for f in json.loads((ROOT/'data/study/triage/families_codex.json').read_text()) for m in f['methods']}
    caps = ROOT/'src/engines/capability_definitions'
    ops = ROOT/'src/operationalizations/definitions'
    originals = DESIGN.parent/'original_capabilities'
    originals.mkdir(exist_ok=True)
    for ident, design in designs.items():
        key = design['key']; old = design['old']; method = families[ident]
        original = originals/f'{old}.yaml'
        if not original.exists():
            original.write_bytes((caps/f'{old}.yaml').read_bytes())
        prior = yaml.safe_load(original.read_text())
        capability = dict(engine_key=key, engine_name=method['name'], version=2 if key == old else 1,
            category=prior['category'], kind='comparison' if ident.startswith('G') else prior.get('kind', 'extraction'),
            problematique=design['ideal']+' '+method['scope'], researcher_question=method['reader_question'],
            intellectual_lineage=prior.get('intellectual_lineage', {'primary':'source_criticism'}),
            analytical_dimensions=[dict(key=d['key'],description=d['name'],probing_questions=d['questions'])
                for d in design['process']['dimensions'] if d.get('scope','document') == 'document'],
            apps=['critic'], function='genealogy', family='analytical', legacy_engine_key=old)
        (caps/f'{key}.yaml').write_text('# Frozen design: communications/study/REDESIGN_second_queue_2026-09-06.md\n'+yaml.safe_dump(capability,sort_keys=False,allow_unicode=True,width=110))
        path=ops/f'{key}.yaml'
        op=yaml.safe_load(path.read_text()) if path.exists() else {}
        op.update(engine_key=key,engine_name=method['name'],process=design['process'])
        op.setdefault('stance_operationalizations',[])
        seqs={s['depth_key']:s for s in op.get('depth_sequences',[])}
        for depth,mode in [('surface','oneshot'),('standard','oneshot_checked'),('deep','dvs')]:
            seqs.setdefault(depth,{'depth_key':depth}).update(mode=mode)
        seqs.setdefault('dvs',{'depth_key':'dvs'}).update(process='dvs')
        op['depth_sequences']=list(seqs.values())
        path.write_text('# Second queue: authored questions replace any earlier lifted process.\n'+yaml.safe_dump(op,sort_keys=False,allow_unicode=True,width=110))
    catalog_path=ROOT/'src/dossier/catalog_purpose.json'
    catalog=json.loads(catalog_path.read_text()); excluded={e['engine_key']:e for e in catalog['excluded']}
    for d in designs.values():
        excluded[d['key']]={'engine_key':d['key'],'why':'Second queue research definition; excluded pending source-read validation. See communications/study/REDESIGN_second_queue_2026-09-06.md.'}
    catalog['excluded']=list(excluded.values())
    catalog_path.write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    build()
