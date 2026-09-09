"""Compose existing central methods and retain the exact records used by a call."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from src.engines.schemas_v2 import CapabilityEngineDefinition
from src.operationalizations.schemas import EngineOperationalization


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def freeze_method(key, *, version=None, trail=()):
    from src.engines.registry import get_engine_registry
    from src.operationalizations.registry import get_operationalization_registry
    if key in trail:
        raise ValueError(f"Cyclic central method reference: {key}")
    cap = get_engine_registry().get_capability_definition(key)
    op = get_operationalization_registry().get(key)
    if cap is None or op is None or op.process is None:
        raise ValueError(f"Central method is unavailable: {key}")
    if version is not None and (cap.version != version or op.version != version):
        raise ValueError(f"Unsupported central method version: {key}@{version}")
    dependencies = [freeze_method(r.engine_key, version=r.version, trail=(*trail, key)) for r in op.process.method_refs]
    return seal(cap.model_dump(mode="json"), op.model_dump(mode="json"), dependencies)


def seal(capability, operationalization, dependencies=()):
    value = {"schema_version": 1, "capability": capability, "operationalization": operationalization,
             "dependencies": list(dependencies)}
    return {**value, "sha256": digest(value)}


def validate_snapshot(snapshot, key=None):
    if snapshot.get("schema_version") != 1 or snapshot.get("sha256") != digest({k:v for k,v in snapshot.items() if k != "sha256"}):
        raise ValueError("Frozen method identity or hash did not verify")
    cap = CapabilityEngineDefinition.model_validate(snapshot["capability"])
    op = EngineOperationalization.model_validate(snapshot["operationalization"])
    if cap.engine_key != op.engine_key or key is not None and cap.engine_key != key or op.process is None:
        raise ValueError("Frozen method engine identity did not verify")
    refs = op.process.method_refs
    deps = snapshot["dependencies"]
    if len(refs) != len(deps):
        raise ValueError("Frozen method dependencies did not verify")
    for ref, dep in zip(refs, deps):
        dc, do = validate_snapshot(dep, ref.engine_key)
        if dc.version != ref.version or do.version != ref.version:
            raise ValueError("Frozen method dependency version did not verify")
    return cap, op


def guidance(snapshot):
    cap, op = validate_snapshot(snapshot)
    parts = [f"### {cap.engine_name} [{cap.engine_key}@{cap.version}; {snapshot['sha256']}]",
             json.dumps(op.method_metadata, ensure_ascii=False),
             op.process.framing or cap.problematique, op.process.description]
    for dim in op.process.dimensions:
        parts += [dim.name, dim.method_card, *dim.questions]
    parts += [guidance(d) for d in snapshot['dependencies']]
    return "\n\n".join(p for p in parts if p)


def compose_method(snapshot):
    cap, op = validate_snapshot(snapshot)
    spec = op.process.model_copy(deep=True)
    if snapshot['dependencies']:
        spec.framing = (spec.framing or cap.problematique) + "\n\n## Shared central methods\n\n" + "\n\n".join(guidance(d) for d in snapshot['dependencies'])
        spec.method_refs = []  # Already resolved from the frozen records, never refetch.
    return cap, spec


def method_receipt(snapshot):
    cap, op = validate_snapshot(snapshot)
    return {"engine_key": cap.engine_key, "version": cap.version, "operationalization_version": op.version,
            "sha256": snapshot['sha256'], "dependencies": [method_receipt(d) for d in snapshot['dependencies']]}


def field_methods(*, legacy=False, institutional=False):
    if legacy:
        raw = json.loads((Path(__file__).parent/'method_snapshots/field_investigation_2026_09_09.json').read_text())
        return {k:seal(v['capability'], v['operationalization']) for k,v in raw.items()}
    from src.workflows.registry import get_workflow_registry
    workflow = get_workflow_registry().get('institutional_inquiry' if institutional else 'field_investigation')
    versions = {'institutional_inquiry_plan': 1, 'institutional_inquiry_memo': 1,
                'field_investigation_field_read': 3, 'field_investigation_field_map': 3} if institutional else {}
    return {p.engine_key:freeze_method(p.engine_key, version=versions.get(p.engine_key)) for p in workflow.phases}


def validate_contract(packet):
    required = packet.get('method_contract')
    expected = {'key': 'institutional-inquiry' if packet.get('inquiry_type') == 'institutional' else 'field-critical-methods', 'version': 1}
    if required is not None and required != expected:
        raise ValueError('Unsupported field investigation method contract')
