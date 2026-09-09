"""Real record composition, consumer routing, and immutable resumption; no model/network calls."""
import copy

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.engines import methods
from src.dossier.engine_call import call_engine
from src.sources.schemas import SourceSpec
from src.dossier.field_investigation import run_field_investigation
from tests.test_field_investigation_2026_09_09 import fixture, fake, freeze

KEYS = ['multimedia_source_criticism','causal_mechanism_audit','concept_case_stress_test','institutional_argument_criticism']
SOURCE = 'The speaker said these are my views, not the institute policy. The company reports profits from interest on reserves.'


def model(captured):
    def call(system, user, **kwargs):
        captured.append((system,user))
        return {'content':'# Reading\n\nThe speaker qualifies authority.\n\n## Findings ledger\n\n[E1.F1] The speaker denies institutional authority — dim: attribution — anchor: "these are my views, not the institute policy" — doc: source — confidence: high', 'input_tokens':10,'output_tokens':10}
    return call


@pytest.mark.parametrize('key', KEYS)
def test_new_methods_are_executable_by_an_independent_caller(key):
    frozen = methods.freeze_method(key, version=1)
    captured=[]
    result=call_engine(key,[SourceSpec(kind='paste',key='source',text=SOURCE)],spend_cap_usd=2,
                       expected_method_sha256=frozen['sha256'],call_fn=model(captured))
    assert len(captured)==1 and SOURCE in captured[0][1]
    assert frozen['operationalization']['process']['framing'] in captured[0][0]
    assert result['method_snapshot']==frozen and result['method_receipt']['sha256']==frozen['sha256']
    assert result['wall']['verified']==1


def test_field_prompt_composes_real_shared_records_without_adding_calls():
    snapshot=methods.freeze_method('field_investigation_adjudicate',version=2)
    assert {d['capability']['engine_key'] for d in snapshot['dependencies']}==set(KEYS)
    captured=[]
    call_engine('field_investigation_adjudicate',[SourceSpec(kind='paste',key='source',text=SOURCE)],
                spend_cap_usd=2,call_fn=model(captured),method_snapshot=snapshot)
    assert len(captured)==1
    for dep in snapshot['dependencies']:
        assert dep['sha256'] in captured[0][0]
        assert dep['operationalization']['process']['dimensions'][0]['method_card'] in captured[0][0]


def test_missing_versions_and_modified_snapshots_refuse_before_provider_call():
    with pytest.raises(ValueError,match='Unsupported central method version'):
        methods.freeze_method(KEYS[0],version=99)
    snap=methods.freeze_method(KEYS[0]);snap['capability']['problematique']='Silently changed'
    captured=[]
    with pytest.raises(ValueError,match='hash'):
        call_engine(KEYS[0],[SourceSpec(kind='paste',key='source',text=SOURCE)],call_fn=model(captured),method_snapshot=snap)
    with pytest.raises(ValueError,match='nothing was spent'):
        call_engine(KEYS[0],[SourceSpec(kind='paste',key='source',text=SOURCE)],call_fn=model(captured),expected_method_sha256='f'*64)
    assert captured==[]


def test_frozen_method_survives_registry_changes_or_removal(monkeypatch):
    snap=methods.freeze_method('field_investigation_adjudicate')
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    monkeypatch.setattr(get_engine_registry(),'get_capability_definition',lambda _:None)
    monkeypatch.setattr(get_operationalization_registry(),'get',lambda _:None)
    captured=[]
    result=call_engine('field_investigation_adjudicate',[SourceSpec(kind='paste',key='source',text=SOURCE)],
                       spend_cap_usd=2,call_fn=model(captured),method_snapshot=snap)
    assert result['method_snapshot']==snap and len(captured)==1


def test_all_paid_stages_and_resume_keep_the_first_method_bundle(monkeypatch):
    _,packet,_,bodies=fixture(primary_count=1)
    saves=[];calls=[]
    with pytest.raises(RuntimeError,match='simulated'):
        run_field_investigation(packet,bodies,call=fake(calls,fail_stage='field_investigation_adjudicate'),save=lambda s:saves.append(copy.deepcopy(s)))
    prior=saves[-1];bundle=copy.deepcopy(prior['method_snapshots']);n=len(prior['calls'])
    monkeypatch.setattr(methods,'field_methods',lambda **kw: (_ for _ in ()).throw(AssertionError('Must not load new methods during resume')))
    completed=run_field_investigation(packet,bodies,call=fake(calls),save=lambda s:None,state=prior)
    assert completed['complete'] and completed['method_snapshots']==bundle
    assert len(completed['calls'])==n+2
    assert all('method_receipt' in r for r in completed['call_input_manifests'].values())
    assert all('method_receipt' in r for r in completed['analysis'].values())


def test_legacy_partial_run_uses_archived_methods_not_current_additions():
    _,packet,_,bodies=fixture(primary_count=1)
    saves=[]
    with pytest.raises(RuntimeError):
        run_field_investigation(packet,bodies,call=fake([],fail_stage='field_investigation_adjudicate'),save=lambda s:saves.append(copy.deepcopy(s)))
    state=saves[-1];state.pop('method_snapshots');state.pop('method_origin')
    seen=[]
    def call(key,sources,**kw):
        seen.append(kw['method_snapshot'])
        return fake([])(key,sources,**kw)
    completed=run_field_investigation(packet,bodies,call=call,save=lambda _:None,state=state)
    assert completed['complete'] and completed['method_origin']=='archived pre-refactor methods'
    assert all(s['capability']['version']==1 and not s['dependencies'] for s in seen)


def test_api_discovers_records_and_checks_required_hash_without_spending():
    from src.api.routes.engines import router
    app=FastAPI();app.include_router(router,prefix='/v1');client=TestClient(app)
    r=client.get('/v1/engines/institutional_argument_criticism/method?version=1')
    assert r.status_code==200 and r.json()['operationalization']['method_metadata']['required_inputs']
    assert client.get('/v1/engines/institutional_argument_criticism/method?version=2').status_code==422
    r=client.post('/v1/engines/institutional_argument_criticism/call',json={'sources':[{'kind':'paste','key':'source','text':SOURCE}],'method_sha256':'f'*64,'spend_cap_usd':0})
    assert r.status_code==400 and 'nothing was spent' in r.json()['detail']


def test_unsupported_field_contract_rejects_source_expansion():
    raw,*_=fixture();raw['method_contract']={'key':'field-critical-methods','version':99}
    with pytest.raises(ValueError,match='Unsupported field'):
        freeze(raw)


def test_practice_registration_preserves_an_explicit_version():
    import json
    from pathlib import Path
    from src.api.routes.practices import PracticeIn
    raw=json.loads((Path(__file__).parents[1]/'src/practices/definitions/topical-multimedia-discovery.json').read_text())
    assert PracticeIn.model_validate(raw).version=='1'
