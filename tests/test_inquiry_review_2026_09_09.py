import copy
import pytest
from test_inquiries_2026_09_08 import client, input_data, result_data, prepared, completion
from src.inquiries import service


def review(result, verdict='ready'):
    return {'result_fingerprint':service.digest(result), 'execution':{'provider':'fixture'}, 'assessment':{
        'verdict':verdict, 'problem_alignment':'Explains the supplied fiscal variation problem.',
        'competing_explanations':'Contrasts constraints with independent state capacity.',
        'next_step':'The comparison targets the unresolved causal difference.',
        'issues':['The rival mechanism is undeveloped.'] if verdict == 'revise' else []}}


def test_review_contract_freezes_method_and_requires_matching_ready_draft(client,input_data,result_data):
    input_data['context']['preparation']={'review_contract':'question-fidelity-v1'}
    p=prepared(client,input_data)
    assert p['review']['contract']=='question-fidelity-v1'
    saved = service._get('inquiry:' + p['prepared_id'])
    assert saved['review_method_record']['capability']['engine_key'] == 'constructive_inquiry_review'
    assert 'review_method_record' not in p
    assert 'desired outcome' in p['review']['system_prompt']
    data=completion(p,input_data,result_data)
    assert client.post('/v1/inquiries/complete',json=data).status_code==422
    data['review']=review(result_data,'revise')
    assert client.post('/v1/inquiries/complete',json=data).status_code==422
    data['review']=review(result_data)
    changed=copy.deepcopy(data);changed['result']['summary']='A different draft.'
    assert client.post('/v1/inquiries/complete',json=changed).status_code==422
    response=client.post('/v1/inquiries/complete',json=data)
    assert response.status_code==200,response.text
    assert response.json()['review']['assessment']['verdict']=='ready'
    from src.readings.registry import reading
    assert reading(response.json()['receipt_id'],'constructive_inquiry')['review']==response.json()['review']


def test_frozen_review_survives_method_change_and_legacy_completion_still_works(client,input_data,result_data,monkeypatch):
    legacy=prepared(client,input_data)
    assert 'review' not in legacy
    input_data['context']['preparation']={'review_contract':'question-fidelity-v1'}
    p=prepared(client,input_data)
    original=service.method_record
    def changed(key):
        value=copy.deepcopy(original(key))
        if key=='constructive_inquiry_review': value['operationalization']['process']['framing']+=' New review rule.'
        return value
    monkeypatch.setattr(service,'method_record',changed)
    newer=prepared(client,input_data)
    assert newer['method_fingerprint'] != p['method_fingerprint']
    data=completion(p,input_data,result_data);data['review']=review(result_data)
    assert client.post('/v1/inquiries/complete',json=data).status_code==200
    input_data['context'].pop('preparation')
    assert client.post('/v1/inquiries/complete',json=completion(legacy,input_data,result_data)).status_code==200


def test_unknown_contract_and_contradictory_verdict_are_rejected(client,input_data,result_data):
    input_data['context']['preparation']={'review_contract':'unknown'}
    assert client.post('/v1/inquiries/prepare',json=input_data).status_code==422
    input_data['context']['preparation']['review_contract']='question-fidelity-v1'
    p=prepared(client,input_data)
    data=completion(p,input_data,result_data);data['review']=review(result_data)
    data['review']['assessment']['issues']=['Unresolved omission']
    assert client.post('/v1/inquiries/complete',json=data).status_code==422
