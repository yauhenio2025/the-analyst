"""Two natural-pair deep runs and four independent scores; separate hard USD6 cap.

Adapter to the existing P1/P2 revalidation PLAN, recorder, runner and audit.
Freeze -> generate -> source memos committed -> score-all -> audit/export.
"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import revalidate_corpus_methods_P1_P2_2026_09_06 as campaign
study=campaign.study
ARCHIVE=ROOT/'communications/study/corpus_methods_P1_P2_third_round_2026_09_06'
campaign.ARCHIVE=ARCHIVE
campaign.__doc__=__doc__
study.OUT=ROOT/'data/study/corpus_methods_P1_P2_third_round_2026_09_06'
study.CAP=6.0
study.JOBS={f'{ident}__deep__pair':{'engine':engine,'mode':'deep','corpus':'pair'} for ident,engine in zip(('P1','P2'),study.ENGINES)}
study.CORPORA={'pair':study.CORPORA['pair']}
study.LIMITS={'cheap':6000,'mid':32000,'strong':14000,'sonnet':1800,'sol':1800}
_previous_paths=study.input_paths
_previous_export=campaign.export
_previous_audit=campaign.audit


def input_paths():
    paths=_previous_paths()+[Path(__file__).relative_to(ROOT),
        Path('scripts/study_corpus_methods_P1_P2_2026_09_06.py'),
        Path('communications/study/REDESIGN_corpus_methods_P1_P2_third_round_2026-09-06.md'),
        Path('communications/study/PROTOCOL_corpus_methods_P1_P2_third_round_2026-09-06.md')]
    for directory in ('src/executor','src/stages','src/operationalizations','src/engines','src/dossier','src/llm','src/events'):
        paths += [p.relative_to(ROOT) for p in (ROOT/directory).glob('*.py')]
    return sorted(set(paths))


def export():
    _previous_export()
    if (study.OUT/'steps').exists():shutil.copytree(study.OUT/'steps',ARCHIVE/'steps',dirs_exist_ok=True)
    if (study.OUT/'validation.json').exists():shutil.copy2(study.OUT/'validation.json',ARCHIVE/'validation.json')


def audit():
    _previous_audit()
    plan=study.read(study.OUT/'plan.json');study.guard(plan)
    costs=study.costs();errors=[]
    if costs['known_usd']+costs['reserved_usd']>6:errors.append('USD6 exceeded')
    manifest=study.OUT/'all_memos_before_scores.json'
    binding=study.read(manifest) if manifest.exists() else None
    outputs=0;scores=0
    for key in study.JOBS:
        resultpath=study.OUT/'results'/f'{key}.json'
        if not resultpath.exists():continue
        result=study.read(resultpath)
        if result['status']!='complete':errors.append(key+': output failed');continue
        outputs+=1;output=study.OUT/'outputs'/f'{key}.md'
        if study.digest(output.read_bytes())!=result['output_sha256']:errors.append(key+': output changed')
        for rater in ('sonnet','sol'):
            sp=study.OUT/'scores'/f'{key}__{rater}.json'
            if not sp.exists():continue
            scores+=1;score=study.read(sp)
            if not binding:errors.append(key+': no pre-score manifest');continue
            frozen=binding['bindings'][key]
            if score['binding']!=frozen:errors.append(key+': score binding differs')
            committed=subprocess.check_output(['git','show',f"{binding['commit']}:{frozen['memo_path']}"],cwd=ROOT)
            if study.digest(committed)!=frozen['memo_sha256'] or result['output_sha256'] not in committed.decode():errors.append(key+': committed memo binding differs')
            for cp in (study.OUT/'calls'/f'judge__{key}__{rater}').glob('*.json'):
                if '.prompt.' in cp.name:continue
                if study.read(cp)['started_at']<binding['prepared_at']:errors.append(key+': score predates manifest')
    study.write(study.OUT/'validation.json',{'plan_identity':plan['identity'],'cap_usd':6,'costs':costs,'completed_outputs':outputs,'scores':scores,'errors':errors,'meaning_checked_by':'source-read memos, not this mechanical validator'})
    if errors:raise RuntimeError('; '.join(errors))

study.input_paths=input_paths
campaign.export=export
campaign.audit=audit
if __name__=='__main__':campaign.main()
