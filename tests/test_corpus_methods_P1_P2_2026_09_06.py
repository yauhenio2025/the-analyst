"""P1/P2 source identities, corpus walls and mixed-scope desk handoff (no API calls)."""
import json
from pathlib import Path
import re

import pytest

from src.dossier.common import analysis_ledger, analysis_prose
from src.dossier.schemas import DossierJob
from src.engines.registry import get_engine_registry
from src.executor.ledger_walls import SourceIndex,parse_rows,render_rows,verify_rows
from src.executor.process_runner import run_process,run_oneshot_checked
from src.executor.scoped_outcomes import render_scope_json
from src.operationalizations.registry import get_operationalization_registry
from src.sources.schemas import Document
from src.stages.process_composer import compose_extract_prompt,compose_verify_prompt,compose_oneshot_prompt,compose_synthesize_prompt

KEYS=('compare_supplied_cases','reconcile_sources')
FIXTURES=Path(__file__).parent/'fixtures/argument_family_2026_09_05'
DOCS={k:(FIXTURES/f'{k}.txt').read_text() for k in ('archive_inventory','archive_policy','archive_fragment')}


def engine(key):
    return get_engine_registry().get_capability_definition(key),get_operationalization_registry().get(key)


@pytest.mark.parametrize('key',KEYS)
@pytest.mark.parametrize('count',[1,2,3])
def test_definitions_compose_at_document_and_corpus_scope(key,count):
    cap,op=engine(key);spec=op.process;docs=dict(list(DOCS.items())[:count])
    assert cap and len(cap.analytical_dimensions)==4
    assert [op.mode_for_depth(d) for d in ('surface','standard','deep')]==['oneshot','oneshot_checked','dvs']
    assert spec.scoped_outcomes
    assert 'gpt-5.6-sol' in spec.routing['strong'] and 'deepseek-v4-pro' in spec.routing['mid'] and 'luna' in spec.routing['cheap']
    corpus=next(d for d in spec.dimensions if d.scope=='corpus')
    one=compose_oneshot_prompt(cap,spec,docs)
    assert (corpus.questions[0] in one.system)==(count>1)
    for dk in docs:
        p=compose_extract_prompt(cap,spec,spec.steps[0],spec.dimensions[0],docs,doc_key=dk)
        assert f'SOURCE [{dk}]' in p.user and list(docs)[0] in docs
        critic=compose_verify_prompt(cap,spec,spec.steps[1],docs,'ledger',doc_key=dk)
        assert corpus.questions[0] not in critic.system
    if count>1:
        p=compose_extract_prompt(cap,spec,spec.steps[0],corpus,docs,prior_ledgers='scoped inventory')
        assert p.user=='scoped inventory' and 'anchor-b:' in p.system and 'doc-b:' in p.system
        assert 'distinct' in p.system and 'Required identities:' in p.system
        for prompt in (one,compose_synthesize_prompt(cap,spec,spec.final_step,docs,'')):
            assert 'actual Markdown' in prompt.system
            assert 'incommensurable' in prompt.system
            assert all(f'SOURCE [{dk}]' in prompt.user for dk in docs)


@pytest.mark.parametrize('key',KEYS)
@pytest.mark.parametrize('bad',['missing_pair','same_key','wrong_key','invented_third'])
def test_corpus_dimension_rejects_unpaired_or_misattributed_anchors(key,bad):
    _,op=engine(key);dim=op.process.dimensions[-1].key
    a='The catalogue lists three items: A17, a blue folder; A18, a grey folder; A19, a green folder.'
    b='Personal addresses should be removed from public copies.'
    base=f'- [F1] Two source answers — dim: {dim} — anchor: "{a}" — doc: archive_inventory'
    pair=f' — anchor-b: "{b}" — doc-b: archive_policy'
    good=base+pair
    assert verify_rows(parse_rows(good),SourceIndex(DOCS),corpus_dimensions={dim}).verified==1
    invalid={'missing_pair':base,'same_key':base+f' — anchor-b: "{a}" — doc-b: archive_inventory',
             'wrong_key':base+pair.replace('doc-b: archive_policy','doc-b: archive_fragment'),
             'invented_third':good+' — anchor-c: "Never supplied in any fragment" — doc-c: archive_fragment'}[bad]
    assert verify_rows(parse_rows(invalid),SourceIndex(DOCS),corpus_dimensions={dim}).failed_ids==['F1']


def outcomes(system,rows,reviewing):
    identities=json.loads(re.search(r'Required identities: (.*)',system).group(1))
    result=[]
    for ident in identities:
        ids=[r.id for r in rows if r.dim==ident['dimension_key'] and {a.doc for a in r.anchors}<=set(ident['document_keys'])]
        fragment='archive_fragment' in ident['document_keys']
        result.append({**ident,'outcome':'findings_present' if ids else 'inconclusive' if fragment else 'no_relevant_instance',
          'sections_inspected':['supplied note'],'coverage':'partial' if fragment else 'complete',
          'criterion':'Answers concerning access to original records and public copies.',
          'basis':'The policy supplies a position; inventory gives folder descriptions; fragment lacks the preceding page.',
          'limitations':['preceding page not supplied'] if fragment else ['Only the supplied note inspected.'],
          'finding_ids':ids,'review_state':'supported_within_stated_scope' if reviewing else 'unchecked',
          'review_basis':'Checked the supplied note against this criterion.' if reviewing else ''})
    return render_scope_json(result)


@pytest.mark.parametrize('key',KEYS)
@pytest.mark.parametrize('mode',['deep','standard'])
def test_mixed_scope_records_survive_real_runner_to_desks(key,mode):
    cap,op=engine(key);spec=op.process
    quote='Personal addresses should be removed from public copies.'
    seen=[]
    def fake(system,user,*,model_hint,label,**kwargs):
        seen.append(label)
        if '| extract |' in label:
            prefix=re.search(r'rows `\[([^]]+)\.F<n>\]`',system).group(1)
            dim=label.split(' | ')[2]
            row=f'- [{prefix}.F1] Public copies should be redacted — dim: {dim} — anchor: "{quote}" — doc: archive_policy'
            text='## Findings ledger\n'+(row if label.endswith('| archive_policy') else '')
            text+='\n\n'+outcomes(system,parse_rows(text),False)
        elif '| verify' in label:
            rows=parse_rows(user.split('EXTRACTION LEDGERS:',1)[1].split('## Scope outcomes')[0])
            for r in rows: r.status='confirmed'
            text=render_rows(rows)+'\n\n'+outcomes(system,rows,True)
        else:
            rows=parse_rows(user.split('VERIFIED FINDINGS LEDGER:',1)[1].split('## Scope outcomes')[0]) if mode=='deep' else []
            lineage=f' — from: {rows[0].id}' if rows else ''
            text=(f'# Access to archive records\nThe policy distinguishes public copies [F1].\n'
                  '| Source | Answer |\n|---|---|\n| archive_policy | Public copies are redacted [F1] |\n'
                  '| archive_inventory | No answer about access in this inventory |\n| archive_fragment | Insufficient evidence; preceding page missing |\n'
                  f'\n## Findings ledger\n- [F1] Public copies should be redacted — dim: {spec.dimensions[0].key} — anchor: "{quote}" — doc: archive_policy{lineage}')
            if mode=='standard': text+='\n\n'+outcomes(system,parse_rows(text),False)
        return {'content':text,'model_used':model_hint,'input_tokens':1,'output_tokens':1,'partial':False,'stop_reason':'stop'}
    runner=run_process if mode=='deep' else run_oneshot_checked
    result=runner(cap,spec,DOCS,call_fn=fake,tier_overrides=spec.routing,**({'parallelism':1} if mode=='deep' else {}))
    assert result.final_wall['failed_ids']==[]
    scopes=result.final_wall['scope_outcomes']
    assert len(scopes)==10
    assert any(r['document_keys']==['archive_inventory'] and r['outcome']=='no_relevant_instance' for r in scopes)
    assert any(r['document_keys']==['archive_fragment'] and r['outcome']=='inconclusive' for r in scopes)
    assert any(r['document_keys']==['archive_policy'] and r['outcome']=='findings_present' for r in scopes)
    job=DossierJob();job.analysis={'1.0':{'engine_key':key,'final_output':result.final_content}}
    desk=analysis_ledger(job,[Document(key=k,title=k,text=v) for k,v in DOCS.items()])
    assert 'archive_policy' in desk and quote in desk
    prose=analysis_prose(job)
    assert 'archive_inventory' in prose and 'archive_fragment' in prose and 'preceding page' in prose
    assert 'Scope assessment' in prose
    if mode=='deep': assert any(spec.dimensions[-1].key in call for call in seen)


def test_study_spend_keeps_unknown_invocations_reserved(tmp_path,monkeypatch):
    from scripts import study_corpus_methods_P1_P2_2026_09_06 as study
    monkeypatch.setattr(study,'OUT',tmp_path)
    study.write(tmp_path/'calls'/'job'/'0001.json',{'status':'failed','cost_usd':None,'reservation_usd':.8})
    study.write(tmp_path/'calls'/'job'/'0002.json',{'status':'complete','cost_usd':.2,'reservation_usd':.7})
    assert study.costs()['known_usd']==.2 and study.costs()['reserved_usd']==.8
    assert study.admission('strong','source','reading')>study.LIMITS['strong']*10/1e6


def test_study_denies_new_call_when_completed_and_unknown_costs_fill_cap(tmp_path,monkeypatch):
    from scripts import study_corpus_methods_P1_P2_2026_09_06 as study
    monkeypatch.setattr(study,'OUT',tmp_path)
    monkeypatch.setattr(study,'guard',lambda _:None)
    study.write(tmp_path/'calls'/'prior'/'0001.json',{'status':'complete','cost_usd':7.7,'reservation_usd':.5})
    study.write(tmp_path/'calls'/'prior'/'0002.json',{'status':'failed','cost_usd':None,'reservation_usd':.2})
    with pytest.raises(RuntimeError,match='USD8 admission cap'):
        study.Recorder('never_launched',{})("system","user",model_hint=study.MODELS['strong'],label='new call')
    assert not (tmp_path/'calls'/'never_launched').exists()


def test_reader_memo_binds_exact_completed_output_before_scoring(tmp_path,monkeypatch):
    from scripts import study_corpus_methods_P1_P2_2026_09_06 as study
    monkeypatch.setattr(study,'OUT',tmp_path/'data')
    monkeypatch.setattr(study,'ROOT',tmp_path)
    key='P1__deep__pair';p=study.OUT/'outputs'/f'{key}.md';p.parent.mkdir(parents=True);p.write_text('Original reading')
    sha=study.digest(p.read_bytes())
    study.write(study.OUT/'results'/f'{key}.json',{'status':'complete','output_sha256':sha})
    memo=tmp_path/'communications/study/corpus_methods_P1_P2_2026_09_06'/f'{key}.md';memo.parent.mkdir(parents=True)
    memo.write_text('Substantive source reading. '*50)
    with pytest.raises(RuntimeError,match='Source-read memo'):study.memo_binding(key,{})
    memo.write_text(sha+'\n'+'Substantive source reading. '*50)
    assert study.memo_binding(key,{})['output_sha256']==sha
    p.write_text('Changed output')
    with pytest.raises(RuntimeError,match='Output changed'):study.memo_binding(key,{})


def test_offline_audit_checks_ids_inside_final_citation_ranges():
    from scripts.audit_corpus_methods_P1_P2_2026_09_06 import expanded_final_citations
    assert expanded_final_citations('[F1–F3] and [F5, F7]')=={'F1','F2','F3','F5','F7'}
