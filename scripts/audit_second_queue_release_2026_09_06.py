"""Consolidate the preserved first pass and its two explicitly bounded final repairs."""
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import study_second_queue_final_repairs_2026_09_06 as repair
from scripts import audit_second_queue_repair_2026_09_06 as audit_module
s=repair.s
base=repair.parent.ARCHIVE

def main():
    first=s.budget.read(base/'first_pass_audit.json');manifest=s.budget.read(s.ARCHIVE/'manifest.json')
    s.budget.require(s.budget.digest((base/'first_pass_audit.json').read_bytes())==manifest['initial_audit_sha256'],'Initial audit changed')
    original=s.budget.read(base/'plan.json');allowed={c['path']:c for c in manifest['changes']}
    for path,sha in original['inputs'].items():
        current=s.budget.digest((ROOT/path).read_bytes())
        if current==sha:continue
        change=allowed.get(path);s.budget.require(change and change['before_sha256']==sha and change['after_sha256']==current,'Unapproved input drift: '+path)
        prior=subprocess.check_output(['git','show',manifest['base_commit']+':'+path],cwd=ROOT)
        s.budget.require(s.budget.digest(prior)==sha,'Original source snapshot changed')
    for key,job in first['jobs'].items():
        p=base/'outputs'/f'{key}.md';s.budget.require(s.budget.digest(p.read_bytes())==job['output_sha256'],'Initial output changed')
        for rater,mean in job['scores'].items():
            sp=base/'scores'/f'{key}__{rater}.json'
            old=subprocess.check_output(['git','show',manifest['base_commit']+':'+str(sp.relative_to(ROOT))],cwd=ROOT)
            s.budget.require(old==sp.read_bytes() and s.budget.read(sp)['mean']==mean,'Initial score changed')
    audit_module.audit(prior_known_usd=first['costs']['known_usd'],review_receipt=base/'claude_review_receipt.json')
    final=s.budget.read(s.ARCHIVE/'audit.json');jobs={**first['jobs'],**final['jobs']}
    for key,j in jobs.items():
        j['selected_artifact_directory']='final_repairs' if key in final['jobs'] else '.'
        original_mean=j['frozen_original_scores'].get('sonnet',j.get('supplemental_original_sonnet_mean'))
        j['original_sonnet_comparison_passes']=j['inventory_exception'] or original_mean is None or j['scores']['sonnet']>=original_mean
    result={'first_plan_identity':original['identity'],'final_plan_identity':final['plan_identity'],'jobs':jobs,
            'costs':{'initial_known_usd':first['costs']['known_usd'],'final_repairs_known_usd':final['costs']['known_usd'],
                     'direct_claude_review_usd':first['direct_claude_review_usd'],'known_round_usd':final['known_round_usd'],
                     'unknown_cli_cost':first['terminated_cli_cost'],'reserved_provider_usd':first['costs']['reserved_usd']+final['costs']['reserved_usd']},
            'first_pass_audit':'first_pass_audit.json','final_repair_audit':'final_repairs/audit.json',
            'errors':first['errors']+final['errors'],'semantic_decisions':'Source memos and final source adjudication; this audit checks custody, anchors, IDs and score comparisons.'}
    s.budget.write(base/'release_audit.json',result)
    print(json.dumps({'costs':result['costs'],'score_comparison_failures':[k for k,j in jobs.items() if not j['original_sonnet_comparison_passes']],'errors':result['errors']},indent=2))
if __name__=='__main__':main()
