"""Generic summaries must not erase typed rows or bypass original support checks."""
import copy
import json
import pytest
from src.dossier.field_investigation import validate_claims
from src.dossier.investigation import recover_answer_rows


def fixture():
    result = {'rows': [], 'final_output': '''## Debate ledger
[E1.F1] Power is contested — dim: debate — claim_kind: field_finding — evidence_ids: source/F1 — anchor: "worker power" — doc: original — confidence: high
## Findings ledger
[F1] Worker power matters — dim: debate — evidence_ids: source/F1 — anchor: "worker power" — confidence: high
'''}
    return recover_answer_rows(result), [{'citation_id': 'source/F1', 'quote_verified': True, 'source_role': 'field'}]


def test_complete_paid_output_keeps_both_ledgers_and_validates_field_summary_support():
    rows, evidence = fixture()
    original = copy.deepcopy(rows)
    result = validate_claims(rows, evidence, required=True, field_map=True)
    assert result['supported'] and result['claim_count'] == 1
    assert result['unclassified_field_summaries'][0]['classification'] == 'unclassified_field_summary'
    assert rows == original and len(rows) == 2
    assert not validate_claims(rows, evidence, required=True)['supported']


@pytest.mark.parametrize('invalid', ['missing', 'unverified', 'primary', 'no_typed', 'invalid_typed', 'typed_missing'])
def test_summary_never_bypasses_original_evidence_or_required_typed_ledger(invalid):
    rows, evidence = fixture()
    if invalid == 'missing': rows[-1]['fields']['evidence_ids'] = 'source/F99'
    elif invalid == 'unverified': evidence[0]['quote_verified'] = False
    elif invalid == 'primary': evidence[0]['source_role'] = 'primary'
    elif invalid == 'no_typed': rows = rows[1:]
    elif invalid == 'invalid_typed': rows[0]['fields']['claim_kind'] = 'thinker_position'
    else: rows[0]['fields']['evidence_ids'] = 'source/F99'
    assert not validate_claims(rows, evidence, required=True, field_map=True)['supported']


@pytest.mark.parametrize('key', ['field_investigation_field_map',
                                'field_investigation_adjudicate', 'field_investigation_memo', 'institutional_inquiry_memo'])
def test_generic_output_shell_preserves_central_claim_fields_at_actual_model_boundary(key):
    from src.engines.methods import freeze_method
    from src.dossier.engine_call import call_engine
    from src.sources.schemas import SourceSpec
    from tests.test_shared_critical_methods import model
    frozen = freeze_method(key)
    captured = []
    call_engine(key, [SourceSpec(kind='paste', key='source', text='worker power')],
                method_snapshot=frozen, call_fn=model(captured), spend_cap_usd=1)
    output = captured[0][0].split('## Output')[-1]
    assert 'claim_kind:' in output and 'evidence_ids:' in output
    assert 'Do not add a second reduced summary ledger.' in output
    # This is schema transport; the frozen analytical record is unchanged.
    assert frozen['operationalization']['process']['framing'] in captured[0][0]


def test_explicitly_excluded_author_profiles_never_trigger_paid_selection_batches():
    from tests.test_field_investigation_2026_09_09 import fixture, freeze, fake
    from src.dossier.field_investigation import run_field_investigation, _baseline_context
    raw, *_ = fixture(prior=False)
    for i in range(35):
        raw['primary'].append({'uid':f'em:EXCLUDED{i}', 'title':'Outside chosen bundle', 'body_state':'excluded',
                               'body':'', 'profile':{'thesis':'Do not select this excluded work. '*1000}})
    _,packet,_,bodies=freeze(raw);calls=[]
    state=run_field_investigation(packet,bodies,call=fake(calls),save=lambda _:None)
    selected=[c for c in calls if c[0]=='field_investigation_author_select']
    assert len(selected)==2 and state['author_selection_scope']=='eligible_inventory'
    assert all('em:EXCLUDED' not in c[3][0].text for c in selected)
    assert len(state['inventory'])==37 and state['complete']
    baseline=json.loads(_baseline_context({'prior_investigations':[{'id':4,'memo':'Reviewed memo.',
                                     'answer':{'memo':'Original memo.','field_map':{'final_output':'Complete prior argument map.'}}}]}))
    assert baseline[0]['memo']=='Reviewed memo.' and baseline[0]['argument_map']=='Complete prior argument map.'


def test_prior_transport_validates_references_and_preserves_current_originals_before_paid_work():
    import hashlib
    from tests.test_field_investigation_2026_09_09 import fixture, freeze
    raw,*_=fixture(prior=False)
    metadata={'attribution':{'category':'guest_contribution'},'original':'retained original'}
    digest=hashlib.sha256(json.dumps(metadata,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    raw.update(research_transport={'version':1,'policy':'exact_prior_source_metadata_factoring'},
               retained_research_metadata={digest:metadata},
               parent_investigation={'id':4,'memo':'Prior memo','answer':{'evidence':[{'source_metadata':{'retained_source_metadata_ref':digest}}]}})
    _,packet,_,bodies=freeze(raw)
    assert bodies['field:referee:0']==raw['field'][0]['body']
    assert packet['retained_research_metadata'][digest]==metadata
    bad=copy.deepcopy(raw);bad['retained_research_metadata'][digest]['original']='Changed'
    with pytest.raises(ValueError,match='hash mismatch'):freeze(bad)
    bad=copy.deepcopy(raw);bad['parent_investigation']['answer']['evidence'][0]['source_metadata']['retained_source_metadata_ref']='missing'
    with pytest.raises(ValueError,match='Unresolved'):freeze(bad)
    bad=copy.deepcopy(raw);bad['research_transport']['version']=99
    with pytest.raises(ValueError,match='Unsupported'):freeze(bad)
