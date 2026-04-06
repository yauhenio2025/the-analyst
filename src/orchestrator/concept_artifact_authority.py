"""Translator helpers for analyzer-v2-backed concept analysis."""

from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from datetime import UTC, datetime
from typing import Any, Optional

from src.executor.db import _json_dumps, _json_loads, execute, init_db
from src.executor.job_manager import get_job
from src.executor.output_store import load_phase_outputs
from src.orchestrator.concept_host_contracts import (
    InferentialAnalysisResult,
    LogicalAnalysisResult,
)
from src.transformations.executor import get_transformation_executor
from src.transformations.registry import get_transformation_registry

INFERENTIAL_HOST_TEMPLATE_KEY = "concept_inferential_host_contract_extraction"
LOGICAL_HOST_TEMPLATE_KEY = "concept_logical_host_contract_extraction"
CONCEPT_ARTIFACT_VALIDATION_PASSED = "passed"
CONCEPT_ARTIFACT_VALIDATION_FAILED = "failed"
CONCEPT_WORKFLOW_KEYS = {
    "concept_inferential_single_concept",
    "concept_logical_single_concept",
}

logger = logging.getLogger(__name__)

LOGICAL_ENGINE_ORDER = {
    "concept_semantic_constellation": 1,
    "concept_structural_landscape": 2,
    "concept_argument_formalization": 3,
    "concept_chain_building": 4,
    "concept_taxonomy_function": 5,
    "concept_causal_mechanisms": 6,
    "concept_conditional_web": 7,
    "concept_argumentative_weight": 8,
    "concept_vulnerability_inferential_gaps": 9,
    "concept_cross_text_comparison": 10,
    "concept_quote_retrieval": 11,
    "concept_synthesis": 12,
}


def _serialize_outputs(
    *,
    concept: str,
    analysis_mode: str,
    phase_outputs: list[dict[str, Any]],
    job_id: str,
    subject_author: str | None,
    subject_name: str | None,
) -> str:
    def sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
        engine_key = item.get("engine_key") or ""
        if analysis_mode == "logical":
            engine_rank = LOGICAL_ENGINE_ORDER.get(engine_key, 999)
        else:
            engine_rank = 0
        try:
            pass_rank = int(float(item.get("pass_number") or 0))
        except (TypeError, ValueError):
            pass_rank = 0
        return (
            engine_rank,
            pass_rank,
            str(item.get("id") or ""),
        )

    lines = [
        "# analyzer-v2 concept translation packet",
        f"concept: {concept}",
        f"analysis_mode: {analysis_mode}",
        f"job_id: {job_id}",
        f"subject_author: {subject_author or ''}",
        f"subject_name: {subject_name or ''}",
        "",
    ]

    for output in sorted(phase_outputs, key=sort_key):
        engine_key = output.get("engine_key") or "unknown_engine"
        pass_number = output.get("pass_number") or 0
        stance_key = output.get("stance_key") or ""
        role = output.get("role") or ""
        content = output.get("content") or ""
        lines.extend(
            [
                f"## engine={engine_key} pass={pass_number} stance={stance_key} role={role}",
                "",
                content,
                "",
            ]
        )

    return "\n".join(lines)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _translate_with_template(template_key: str, packet: str) -> dict[str, Any]:
    template = get_transformation_registry().get(template_key)
    if template is None:
        raise RuntimeError(f"analyzer-v2 transformation '{template_key}' is not registered")

    executor = get_transformation_executor()
    last_error = f"analyzer-v2 transformation '{template_key}' returned no response"
    for attempt in range(2):
        response = asyncio.run(
            executor.execute(
                data=packet,
                transformation_type=template.transformation_type,
                field_mapping=template.field_mapping,
                llm_extraction_schema=template.llm_extraction_schema,
                llm_prompt_template=template.llm_prompt_template,
                stance_key=template.stance_key,
                aggregate_config=template.aggregate_config,
                model=template.model,
                model_fallback=template.model_fallback,
                max_tokens=template.max_tokens,
                cache_key=f"concept-translation::{template_key}::{hash(packet)}",
            )
        )
        if response.success:
            if isinstance(response.data, dict):
                return response.data
            last_error = f"analyzer-v2 transformation '{template_key}' returned non-object data"
        else:
            last_error = (
                f"analyzer-v2 transformation '{template_key}' failed: "
                f"{response.error or 'unknown error'}"
            )
        if attempt == 0:
            time.sleep(1.0)
    raise RuntimeError(last_error)


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = [_coerce_text(item) for item in value]
        return "\n".join(part for part in parts if part)
    if isinstance(value, dict):
        preferred_keys = [
            "summary",
            "description",
            "analysis",
            "text",
            "label",
            "title",
            "value",
        ]
        collected = [_coerce_text(value.get(key)) for key in preferred_keys if key in value]
        collected = [item for item in collected if item]
        if collected:
            return "\n".join(collected)
        return json.dumps(value, ensure_ascii=True)
    return str(value).strip()


def _coerce_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    if score > 1.0 and score <= 100.0:
        score /= 100.0
    return max(0.0, min(score, 1.0))


def _coerce_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in (_coerce_text(entry) for entry in value) if item]
    text = _coerce_text(value)
    return [text] if text else []


def _normalize_key_quotes(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    quotes: list[dict[str, str]] = []
    for item in value:
        if isinstance(item, dict):
            quote = _coerce_text(item.get("quote"))
            if not quote:
                continue
            quotes.append(
                {
                    "quote": quote,
                    "source": _coerce_text(item.get("source")),
                    "analysis": _coerce_text(item.get("analysis")),
                }
            )
        else:
            quote = _coerce_text(item)
            if quote:
                quotes.append({"quote": quote, "source": "", "analysis": ""})
    return quotes


def _split_surface_hidden(text: str) -> tuple[str, str]:
    if not text:
        return "", ""
    marker = "The hidden analytical weight"
    if marker in text:
        surface, hidden = text.split(marker, 1)
        surface = surface.strip().rstrip(":")
        hidden = f"{marker}{hidden}".strip()
        return surface or text, hidden or text
    sentences = [segment.strip() for segment in text.split(". ") if segment.strip()]
    if len(sentences) > 1:
        surface = sentences[0].rstrip(".")
        hidden = ". ".join(sentences[1:])
        return surface, hidden
    return text, text


def _normalize_the_deceptively_simple(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        surface = _coerce_text(
            value.get("surface_presentation")
            or value.get("surface")
            or value.get("presentation")
        )
        hidden = _coerce_text(
            value.get("hidden_weight")
            or value.get("hidden")
            or value.get("analysis")
            or value.get("weight")
        )
        if not surface and hidden:
            surface = hidden
        if not hidden and surface:
            hidden = surface
        return {
            "surface_presentation": surface,
            "hidden_weight": hidden,
            "key_quotes": _normalize_key_quotes(value.get("key_quotes")),
        }

    text = _coerce_text(value)
    surface, hidden = _split_surface_hidden(text)
    return {
        "surface_presentation": surface,
        "hidden_weight": hidden,
        "key_quotes": [],
    }


def _split_commitment_chain(entries: list[str]) -> tuple[list[str], list[str], list[str]]:
    practical_keywords = (
        "publish",
        "policy",
        "teach",
        "training",
        "curriculum",
        "department",
        "institution",
        "practical",
        "obligation",
        "decision",
        "employment",
        "action",
    )
    practical = [item for item in entries if any(keyword in item.lower() for keyword in practical_keywords)]
    non_practical = [item for item in entries if item not in practical]
    immediate = non_practical[:2]
    downstream = non_practical[2:]
    return immediate, downstream, practical


def _normalize_commitment_cascade(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        relations = value.get("commitment_relations")
        if isinstance(relations, list):
            hidden = value.get("hidden_commitments")
            if isinstance(hidden, list):
                return value

    items = value if isinstance(value, list) else []
    commitment_relations: list[dict[str, Any]] = []
    hidden_commitments: list[dict[str, str]] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        label = _coerce_text(
            item.get("source_label")
            or item.get("if_you_endorse")
            or item.get("commitment")
            or f"Commitment {index}"
        )
        chain_entries = _coerce_string_list(
            item.get("inferential_chain")
            or item.get("chain")
            or item.get("commitments")
        )
        immediate, downstream, practical = _split_commitment_chain(chain_entries)
        commitment_relations.append(
            {
                "if_you_endorse": label,
                "you_are_committed_to": {
                    "immediate": immediate,
                    "downstream": downstream,
                    "practical": practical,
                },
                "strength": item.get("strength") or "strong",
                "commonly_recognized": bool(item.get("explicit", True)),
                "textual_evidence": None,
            }
        )
        if item.get("explicit") is False:
            hidden_commitments.append(
                {
                    "commitment": label,
                    "why_hidden": _coerce_text(item.get("commitment_type") or chain_entries[:1]),
                    "textual_evidence": _coerce_text(chain_entries[:1]),
                }
            )
    return {
        "commitment_relations": commitment_relations,
        "hidden_commitments": hidden_commitments,
    }


def _normalize_incompatibility_map(value: Any) -> dict[str, Any]:
    if isinstance(value, dict) and isinstance(value.get("incompatibility_relations"), list):
        return value
    items = value if isinstance(value, list) else []
    relations: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        relations.append(
            {
                "concept_a": _coerce_text(item.get("concept_a") or item.get("commitment_a")),
                "concept_b": _coerce_text(item.get("concept_b") or item.get("commitment_b")),
                "severity": item.get("severity") or "strong",
                "why_incompatible": _coerce_text(
                    item.get("why_incompatible") or item.get("incompatibility_description")
                ),
                "who_is_caught": _coerce_text(item.get("who_is_caught")),
                "textual_evidence": _coerce_text(item.get("textual_evidence")),
            }
        )
    return {
        "incompatibility_relations": relations,
        "unstable_combinations": "",
    }


def _normalize_tensions(value: Any) -> dict[str, Any]:
    if isinstance(value, dict) and isinstance(value.get("unresolved_tensions"), list):
        return value
    items = value if isinstance(value, list) else []
    tensions: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        label = _coerce_text(item.get("tension_label"))
        description = _coerce_text(item.get("description"))
        status = _coerce_text(item.get("resolution_status"))
        lowered = status.lower()
        stability = "unresolved"
        if "unstable" in lowered:
            stability = "unstable"
        elif "precarious" in lowered:
            stability = "precarious"
        conflicts = [part.strip() for part in label.split(" vs ") if part.strip()] if " vs " in label else []
        if not conflicts and label:
            conflicts = [label]
        tensions.append(
            {
                "conflicting_commitments": conflicts,
                "source_of_tension": description or label,
                "stability": stability,
                "textual_evidence": [],
                "why_it_resists_resolution": description or status or label,
            }
        )
    return {
        "unresolved_tensions": tensions,
        "intellectual_fault_lines": "",
    }


def _normalize_practical_stakes(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {
            "obligations": _coerce_string_list(value.get("obligations")),
            "prohibitions": _coerce_string_list(value.get("prohibitions")),
            "affected_decisions": _coerce_string_list(value.get("affected_decisions")),
            "normative_entanglements": _coerce_text(value.get("normative_entanglements")),
        }
    items = value if isinstance(value, list) else []
    obligations: list[str] = []
    prohibitions: list[str] = []
    decisions: list[str] = []
    entanglements: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        kind = _coerce_text(item.get("stake_type")).lower()
        description = _coerce_text(item.get("description"))
        if not description:
            continue
        if "oblig" in kind:
            obligations.append(description)
        elif "prohib" in kind:
            prohibitions.append(description)
        elif "decision" in kind or "affected" in kind:
            decisions.append(description)
        else:
            entanglements.append(description)
    return {
        "obligations": obligations,
        "prohibitions": prohibitions,
        "affected_decisions": decisions,
        "normative_entanglements": "\n".join(entanglements),
    }


def _normalize_commitment_packages(value: Any) -> list[dict[str, Any]]:
    items = value if isinstance(value, list) else []
    packages: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        if isinstance(item, dict):
            package_name = _coerce_text(item.get("package_name") or item.get("package_label"))
            members = _coerce_string_list(item.get("core_commitments") or item.get("members"))
            if not package_name:
                package_name = members[0] if members else f"Package {index}"
            packages.append(
                {
                    "package_name": package_name,
                    "core_commitments": members or _coerce_string_list(item.get("description")),
                    "incompatible_packages": _coerce_string_list(item.get("incompatible_packages")),
                    "who_endorses": _coerce_text(item.get("who_endorses") or item.get("description")),
                }
            )
        else:
            text = _coerce_text(item)
            if text:
                packages.append(
                    {
                        "package_name": text,
                        "core_commitments": [text],
                        "incompatible_packages": [],
                        "who_endorses": "",
                    }
                )
    return packages


def _normalize_inferential_synthesis(value: Any, commitment_cascade: dict[str, Any]) -> dict[str, Any]:
    if isinstance(value, dict):
        summary = _coerce_text(
            value.get("inferential_definition")
            or value.get("summary")
            or value.get("definition")
        )
        most_consequential = _coerce_text(value.get("most_consequential_commitment"))
        if not most_consequential:
            first_relation = (commitment_cascade.get("commitment_relations") or [{}])[0]
            most_consequential = _coerce_text(first_relation.get("if_you_endorse"))
        key_revelation = _coerce_text(value.get("key_revelation") or value.get("stability_note") or summary)
        return {
            "inferential_definition": summary,
            "centrality_score": _coerce_score(value.get("centrality_score")),
            "stability_score": _coerce_score(value.get("stability_score")),
            "most_consequential_commitment": most_consequential,
            "key_revelation": key_revelation,
        }
    text = _coerce_text(value)
    first_relation = (commitment_cascade.get("commitment_relations") or [{}])[0]
    return {
        "inferential_definition": text,
        "centrality_score": 0.0,
        "stability_score": 0.0,
        "most_consequential_commitment": _coerce_text(first_relation.get("if_you_endorse")),
        "key_revelation": text,
    }


def _normalize_inferential_translation(translated: dict[str, Any], concept: str) -> dict[str, Any]:
    commitment_cascade = _normalize_commitment_cascade(translated.get("commitment_cascade"))
    return {
        "concept": translated.get("concept") or concept,
        "analysis_type": "inferential",
        "framework": _coerce_text(translated.get("framework")) or "Brandomian Inferential Role Analysis",
        "the_deceptively_simple": _normalize_the_deceptively_simple(
            translated.get("the_deceptively_simple")
        ),
        "commitment_cascade": commitment_cascade,
        "incompatibility_map": _normalize_incompatibility_map(
            translated.get("incompatibility_map")
        ),
        "tensions": _normalize_tensions(translated.get("tensions")),
        "practical_stakes": _normalize_practical_stakes(translated.get("practical_stakes")),
        "commitment_packages": _normalize_commitment_packages(
            translated.get("commitment_packages")
        ),
        "synthesis": _normalize_inferential_synthesis(
            translated.get("synthesis"),
            commitment_cascade,
        ),
        "thinking_preview": _coerce_text(translated.get("thinking_preview")) or None,
    }


def translate_inferential_result(
    *,
    concept: str,
    phase_outputs: list[dict[str, Any]],
    analyzer_job_id: str,
    subject_author: str | None,
    subject_name: str | None,
    depth: str,
) -> dict[str, Any]:
    packet = _serialize_outputs(
        concept=concept,
        analysis_mode="inferential",
        phase_outputs=phase_outputs,
        job_id=analyzer_job_id,
        subject_author=subject_author,
        subject_name=subject_name,
    )
    translated = _translate_with_template(INFERENTIAL_HOST_TEMPLATE_KEY, packet)
    normalized = _normalize_inferential_translation(translated, concept)
    normalized["analyzed_at"] = datetime.now().isoformat()
    validated = InferentialAnalysisResult.model_validate(normalized).model_dump()
    validated["_analysis_provenance"] = {
        "execution_owner": "analyzer-v2",
        "workflow_key": "concept_inferential_single_concept",
        "engine_or_chain_key": "inferential_commitment_mapper",
        "depth": depth,
        "analyzer_v2_job_id": analyzer_job_id,
        "translation_template_key": INFERENTIAL_HOST_TEMPLATE_KEY,
    }
    return validated


def _normalize_logical_form(value: Any, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    source = value if isinstance(value, dict) else {}
    fallback = fallback or {}
    premises = _coerce_string_list(
        source.get("premises")
        or fallback.get("premises")
        or source.get("supports")
        or fallback.get("supports")
    )
    conclusion = _coerce_text(
        source.get("conclusion")
        or fallback.get("conclusion")
        or source.get("claim")
        or fallback.get("claim")
        or source.get("summary")
        or fallback.get("summary")
    )
    if not premises and conclusion:
        premises = [conclusion]
    return {
        "premises": premises,
        "conclusion": conclusion or (premises[0] if premises else ""),
        "argument_type": source.get("argument_type")
        or fallback.get("argument_type")
        or source.get("type")
        or fallback.get("type")
        or "deductive",
        "form_name": _coerce_text(
            source.get("form_name")
            or fallback.get("form_name")
            or source.get("form")
            or fallback.get("form")
        )
        or None,
    }


def _normalize_logical_argument_inventory(value: Any) -> list[dict[str, Any]]:
    items = value if isinstance(value, list) else []
    arguments: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        logical_form = _normalize_logical_form(item.get("logical_form"), item)
        quote = _coerce_text(
            item.get("quote")
            or item.get("textual_evidence")
            or item.get("evidence_quote")
            or item.get("evidence")
            or item.get("claim")
            or logical_form["conclusion"]
        )
        arguments.append(
            {
                "id": _coerce_text(item.get("id") or item.get("argument_id") or f"A{index}"),
                "source": _coerce_text(item.get("source") or item.get("location") or f"source-{index}"),
                "quote": quote,
                "logical_form": logical_form,
                "unstated_premises": _coerce_string_list(item.get("unstated_premises")),
                "concept_role": _coerce_text(
                    item.get("concept_role")
                    or item.get("role")
                    or item.get("argumentative_function")
                    or "important"
                ),
            }
        )
    return arguments


def _normalize_argument_dependencies(
    value: Any,
    sequence: list[str],
    chain_id: str,
) -> list[dict[str, str]]:
    dependencies: list[dict[str, str]] = []
    items = value if isinstance(value, list) else []
    for index, item in enumerate(items):
        if isinstance(item, dict):
            from_arg = _coerce_text(item.get("from") or item.get("from_arg"))
            to_arg = _coerce_text(item.get("to") or item.get("to_arg"))
            relationship = _coerce_text(item.get("relationship") or item.get("description"))
            if from_arg and to_arg:
                dependencies.append(
                    {
                        "from": from_arg,
                        "to": to_arg,
                        "relationship": relationship or "supports",
                    }
                )
            continue

        relationship = _coerce_text(item)
        if not relationship:
            continue
        if len(sequence) >= 2:
            pair_index = min(index, len(sequence) - 2)
            from_arg = sequence[pair_index]
            to_arg = sequence[pair_index + 1]
        else:
            from_arg = sequence[0] if sequence else chain_id
            to_arg = sequence[-1] if sequence else chain_id
        dependencies.append(
            {
                "from": from_arg,
                "to": to_arg,
                "relationship": relationship,
            }
        )

    if not dependencies and len(sequence) >= 2:
        for from_arg, to_arg in zip(sequence, sequence[1:]):
            dependencies.append(
                {
                    "from": from_arg,
                    "to": to_arg,
                    "relationship": "supports",
                }
            )
    return dependencies


def _normalize_argument_chains(value: Any) -> list[dict[str, Any]]:
    items = value if isinstance(value, list) else []
    chains: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        chain_id = _coerce_text(item.get("chain_id") or item.get("id") or f"chain-{index:02d}")
        sequence = _coerce_string_list(
            item.get("sequence")
            or item.get("arguments")
            or item.get("steps")
            or item.get("argument_ids")
        )
        if not sequence:
            sequence = [chain_id]
        chains.append(
            {
                "chain_id": chain_id,
                "sequence": sequence,
                "dependencies": _normalize_argument_dependencies(
                    item.get("dependencies"), sequence, chain_id
                ),
                "ultimate_conclusion": _coerce_text(
                    item.get("ultimate_conclusion")
                    or item.get("conclusion")
                    or item.get("summary")
                    or sequence[-1]
                ),
                "visualization": _coerce_text(item.get("visualization")),
                "inferential_mode": item.get("inferential_mode"),
                "causal_structure": item.get("causal_structure"),
                "dialectical_function": item.get("dialectical_function"),
                "inferential_role": item.get("inferential_role"),
                "argumentative_function": item.get("argumentative_function"),
            }
        )
    return chains


def _normalize_causal_claims(value: Any) -> list[dict[str, str]]:
    items = value if isinstance(value, list) else []
    claims: list[dict[str, str]] = []
    for item in items:
        if isinstance(item, dict):
            claims.append(
                {
                    "effect": _coerce_text(item.get("effect")),
                    "cause": _coerce_text(item.get("cause")),
                    "mechanism": _coerce_text(item.get("mechanism") or item.get("description")),
                    "evidence_quote": _coerce_text(
                        item.get("evidence_quote") or item.get("quote") or item.get("evidence")
                    ),
                    "source": _coerce_text(item.get("source")),
                }
            )
    return claims


def _normalize_causal_architecture(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    return {
        "concept_as_cause": _normalize_causal_claims(value.get("concept_as_cause")),
        "concept_as_effect": _normalize_causal_claims(value.get("concept_as_effect")),
        "mechanism_detail": value.get("mechanism_detail") or "medium",
        "interventionist_claims": _coerce_string_list(value.get("interventionist_claims")),
    }


def _normalize_conditional_entries(value: Any) -> list[dict[str, str]]:
    items = value if isinstance(value, list) else []
    entries: list[dict[str, str]] = []
    for item in items:
        if isinstance(item, dict):
            entries.append(
                {
                    "conditional": _coerce_text(
                        item.get("conditional") or item.get("structure") or item.get("description")
                    ),
                    "quote": _coerce_text(item.get("quote") or item.get("evidence")),
                    "source": _coerce_text(item.get("source")),
                }
            )
        else:
            text = _coerce_text(item)
            if text:
                entries.append({"conditional": text, "quote": "", "source": ""})
    return entries


def _normalize_conditional_web(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    return {
        "antecedent_uses": _normalize_conditional_entries(value.get("antecedent_uses")),
        "consequent_uses": _normalize_conditional_entries(value.get("consequent_uses")),
        "biconditionals": _normalize_conditional_entries(value.get("biconditionals")),
        "nested_conditionals": _normalize_conditional_entries(value.get("nested_conditionals")),
    }


def _normalize_argumentative_weight(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    return {
        "load_bearing": _coerce_string_list(value.get("load_bearing")),
        "supporting": _coerce_string_list(value.get("supporting")),
        "defensive": _coerce_string_list(value.get("defensive")),
        "illustrative": _coerce_string_list(value.get("illustrative")),
    }


def _normalize_logical_vulnerabilities(value: Any) -> list[dict[str, Any]]:
    items = value if isinstance(value, list) else []
    vulnerabilities: list[dict[str, Any]] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        vulnerabilities.append(
            {
                "vulnerability_type": item.get("vulnerability_type") or "inferential_gap",
                "argument_id": _coerce_text(
                    item.get("argument_id") or item.get("target_argument") or f"A{index}"
                ),
                "description": _coerce_text(item.get("description") or item.get("summary")),
                "potential_challenge": _coerce_text(
                    item.get("potential_challenge") or item.get("challenge")
                ),
                "severity": item.get("severity") or "medium",
            }
        )
    return vulnerabilities


def _normalize_textual_shifts(value: Any) -> list[dict[str, str]]:
    items = value if isinstance(value, list) else []
    shifts: list[dict[str, str]] = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            continue
        analysis = _coerce_text(
            item.get("analysis") or item.get("description") or item.get("shift_summary")
        )
        nlr_version = _coerce_text(
            item.get("nlr_version") or item.get("prior_version") or item.get("before")
        )
        response_version = _coerce_text(
            item.get("response_version") or item.get("current_version") or item.get("after")
        )
        location = _coerce_text(item.get("location") or item.get("source") or f"shift-{index}")
        if not nlr_version:
            nlr_version = location
        if not response_version:
            response_version = analysis or location
        shifts.append(
            {
                "argument_id": _coerce_text(item.get("argument_id") or location or f"A{index}"),
                "change_type": item.get("change_type") or item.get("change") or "introduced",
                "nlr_version": nlr_version,
                "response_version": response_version,
                "analysis": analysis or location,
            }
        )
    return shifts


def _normalize_logical_synthesis(
    value: Any,
    arguments: list[dict[str, Any]],
    vulnerabilities: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        if not arguments and not vulnerabilities:
            return None
        return {
            "argument_density": len(arguments),
            "logical_centrality": "important",
            "causal_weight": "moderate",
            "strongest_arguments": [argument["id"] for argument in arguments[:2]],
            "weakest_arguments": [vulnerability["argument_id"] for vulnerability in vulnerabilities[:2]],
            "vulnerability_summary": _coerce_text(
                vulnerabilities[0]["description"] if vulnerabilities else ""
            ),
            "overall_assessment": "Analyzer-v2 logical translation completed with derived synthesis.",
        }

    return {
        "argument_density": value.get("argument_density") or len(arguments),
        "logical_centrality": value.get("logical_centrality") or "important",
        "causal_weight": value.get("causal_weight") or "moderate",
        "strongest_arguments": _coerce_string_list(value.get("strongest_arguments")),
        "weakest_arguments": _coerce_string_list(value.get("weakest_arguments")),
        "vulnerability_summary": _coerce_text(value.get("vulnerability_summary")),
        "overall_assessment": _coerce_text(value.get("overall_assessment")),
    }


def _normalize_logical_translation(translated: dict[str, Any], concept: str) -> dict[str, Any]:
    arguments = _normalize_logical_argument_inventory(translated.get("argument_inventory"))
    vulnerabilities = _normalize_logical_vulnerabilities(
        translated.get("logical_vulnerabilities")
    )
    return {
        "concept": translated.get("concept") or concept,
        "analysis_type": "logical",
        "framework": _coerce_text(translated.get("framework")) or "Logical Structure Analysis",
        "argument_inventory": arguments,
        "argument_chains": _normalize_argument_chains(translated.get("argument_chains")),
        "causal_architecture": _normalize_causal_architecture(
            translated.get("causal_architecture")
        ),
        "conditional_web": _normalize_conditional_web(translated.get("conditional_web")),
        "argumentative_weight": _normalize_argumentative_weight(
            translated.get("argumentative_weight")
        ),
        "logical_vulnerabilities": vulnerabilities,
        "textual_shifts": _normalize_textual_shifts(translated.get("textual_shifts")),
        "synthesis": _normalize_logical_synthesis(
            translated.get("synthesis"),
            arguments,
            vulnerabilities,
        ),
        "thinking_preview": _coerce_text(translated.get("thinking_preview")) or None,
    }


def translate_logical_result(
    *,
    concept: str,
    phase_outputs: list[dict[str, Any]],
    analyzer_job_id: str,
    subject_author: str | None,
    subject_name: str | None,
    depth: str,
) -> dict[str, Any]:
    packet = _serialize_outputs(
        concept=concept,
        analysis_mode="logical",
        phase_outputs=phase_outputs,
        job_id=analyzer_job_id,
        subject_author=subject_author,
        subject_name=subject_name,
    )
    translated = _translate_with_template(LOGICAL_HOST_TEMPLATE_KEY, packet)
    normalized = _normalize_logical_translation(translated, concept)
    normalized["analyzed_at"] = datetime.now().isoformat()
    validated = LogicalAnalysisResult.model_validate(normalized).model_dump()
    validated["_analysis_provenance"] = {
        "execution_owner": "analyzer-v2",
        "workflow_key": "concept_logical_single_concept",
        "engine_or_chain_key": "concept_analysis_12_phase",
        "depth": depth,
        "analyzer_v2_job_id": analyzer_job_id,
        "translation_template_key": LOGICAL_HOST_TEMPLATE_KEY,
    }
    return validated


def _parse_json_field(value: Any) -> Any:
    if isinstance(value, str):
        return _json_loads(value)
    return value


def _parse_artifact_row(row: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    for field in ("translated_artifact_json", "validation_errors", "analysis_context"):
        row[field] = _parse_json_field(row.get(field))
    for field in ("produced_at", "updated_at"):
        value = row.get(field)
        if hasattr(value, "isoformat"):
            row[field] = value.isoformat()
    if row.get("validation_errors") is None:
        row["validation_errors"] = []
    return row


def _concept_defaults_for_mode(analysis_mode: str) -> tuple[str, str, str, str]:
    if analysis_mode == "inferential":
        return (
            "concept_inferential_single_concept",
            "inferential_commitment_mapper",
            INFERENTIAL_HOST_TEMPLATE_KEY,
            "standard",
        )
    return (
        "concept_logical_single_concept",
        "concept_analysis_12_phase",
        LOGICAL_HOST_TEMPLATE_KEY,
        "deep",
    )


def extract_concept_job_context(job: dict[str, Any]) -> Optional[dict[str, Any]]:
    workflow_key = job.get("workflow_key") or ""
    if workflow_key not in CONCEPT_WORKFLOW_KEYS:
        return None

    plan_data = job.get("plan_data") or {}
    if isinstance(plan_data, str):
        plan_data = _json_loads(plan_data)
    if not isinstance(plan_data, dict):
        return None

    context = plan_data.get("_concept_by_ref_context") or {}
    if not isinstance(context, dict):
        context = {}

    analysis_mode = context.get("analysis_mode")
    if analysis_mode not in {"inferential", "logical"}:
        analysis_mode = "inferential" if workflow_key == "concept_inferential_single_concept" else "logical"

    default_workflow_key, engine_or_chain_key, template_key, default_depth = _concept_defaults_for_mode(analysis_mode)
    depth = (
        context.get("depth")
        or plan_data.get("estimated_depth_profile")
        or ((plan_data.get("phases") or [{}])[0].get("depth"))
        or default_depth
    )

    return {
        "consumer_key": context.get("consumer_key") or "",
        "external_project_id": context.get("external_project_id") or job.get("project_id") or "",
        "concept_name": context.get("concept_name") or "",
        "analysis_mode": analysis_mode,
        "workflow_key": workflow_key or default_workflow_key,
        "engine_or_chain_key": engine_or_chain_key,
        "subject_author": context.get("subject_author"),
        "subject_name": context.get("subject_name"),
        "depth": depth,
        "translation_template_key": template_key,
        "external_doc_keys": context.get("external_doc_keys") or [],
    }


def upsert_concept_translated_artifact(
    *,
    consumer_key: str,
    external_project_id: str,
    concept_name: str,
    analysis_mode: str,
    workflow_key: str,
    engine_or_chain_key: str,
    depth: str,
    analyzer_v2_job_id: str,
    translation_template_key: str,
    contract_validation_status: str,
    translated_artifact: dict[str, Any],
    validation_errors: Optional[list[str]] = None,
    analysis_context: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    init_db()
    now = _now_iso()
    artifact_id = f"caa-{uuid.uuid4().hex[:12]}"
    execute(
        """INSERT INTO concept_translated_artifacts
           (artifact_id, consumer_key, external_project_id, concept_name, analysis_mode,
            workflow_key, engine_or_chain_key, depth, analyzer_v2_job_id,
            translation_template_key, contract_validation_status, translated_artifact_json,
            validation_errors, analysis_context, produced_at, updated_at)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           ON CONFLICT (analyzer_v2_job_id) DO UPDATE SET
             consumer_key = EXCLUDED.consumer_key,
             external_project_id = EXCLUDED.external_project_id,
             concept_name = EXCLUDED.concept_name,
             analysis_mode = EXCLUDED.analysis_mode,
             workflow_key = EXCLUDED.workflow_key,
             engine_or_chain_key = EXCLUDED.engine_or_chain_key,
             depth = EXCLUDED.depth,
             translation_template_key = EXCLUDED.translation_template_key,
             contract_validation_status = EXCLUDED.contract_validation_status,
             translated_artifact_json = EXCLUDED.translated_artifact_json,
             validation_errors = EXCLUDED.validation_errors,
             analysis_context = EXCLUDED.analysis_context,
             produced_at = EXCLUDED.produced_at,
             updated_at = EXCLUDED.updated_at""",
        (
            artifact_id,
            consumer_key,
            external_project_id,
            concept_name,
            analysis_mode,
            workflow_key,
            engine_or_chain_key,
            depth,
            analyzer_v2_job_id,
            translation_template_key,
            contract_validation_status,
            _json_dumps(translated_artifact or {}),
            _json_dumps(validation_errors or []),
            _json_dumps(analysis_context or {}),
            now,
            now,
        ),
    )
    return load_concept_translated_artifact(
        consumer_key=consumer_key,
        external_project_id=external_project_id,
        concept_name=concept_name,
        analysis_mode=analysis_mode,
        analyzer_v2_job_id=analyzer_v2_job_id,
    ) or {}


def load_concept_translated_artifact(
    *,
    consumer_key: str,
    external_project_id: str,
    concept_name: str,
    analysis_mode: str,
    analyzer_v2_job_id: str | None = None,
) -> Optional[dict[str, Any]]:
    init_db()
    if analyzer_v2_job_id:
        row = execute(
            """SELECT *
               FROM concept_translated_artifacts
               WHERE consumer_key = %s
                 AND external_project_id = %s
                 AND concept_name = %s
                 AND analysis_mode = %s
                 AND analyzer_v2_job_id = %s
               LIMIT 1""",
            (
                consumer_key,
                external_project_id,
                concept_name,
                analysis_mode,
                analyzer_v2_job_id,
            ),
            fetch="one",
        )
        return _parse_artifact_row(row)

    row = execute(
        """SELECT *
           FROM concept_translated_artifacts
           WHERE consumer_key = %s
             AND external_project_id = %s
             AND concept_name = %s
             AND analysis_mode = %s
             AND contract_validation_status = %s
           ORDER BY produced_at DESC, updated_at DESC
           LIMIT 1""",
        (
            consumer_key,
            external_project_id,
            concept_name,
            analysis_mode,
            CONCEPT_ARTIFACT_VALIDATION_PASSED,
        ),
        fetch="one",
    )
    return _parse_artifact_row(row)


def materialize_concept_translated_artifact(job_id: str) -> Optional[dict[str, Any]]:
    job = get_job(job_id)
    if job is None:
        raise ValueError(f"Job not found: {job_id}")

    context = extract_concept_job_context(job)
    if context is None:
        return None

    phase_outputs = load_phase_outputs(job_id=job_id, phase_number=1.0)
    if not phase_outputs:
        raise ValueError(f"No phase outputs found for concept job {job_id}")

    validation_errors: list[str] = []
    translated_artifact: dict[str, Any] = {}
    validation_status = CONCEPT_ARTIFACT_VALIDATION_FAILED
    try:
        if context["analysis_mode"] == "inferential":
            translated_artifact = translate_inferential_result(
                concept=context["concept_name"],
                phase_outputs=phase_outputs,
                analyzer_job_id=job_id,
                subject_author=context.get("subject_author"),
                subject_name=context.get("subject_name"),
                depth=context["depth"],
            )
        else:
            translated_artifact = translate_logical_result(
                concept=context["concept_name"],
                phase_outputs=phase_outputs,
                analyzer_job_id=job_id,
                subject_author=context.get("subject_author"),
                subject_name=context.get("subject_name"),
                depth=context["depth"],
            )
        validation_status = CONCEPT_ARTIFACT_VALIDATION_PASSED
    except Exception as error:
        validation_errors.append(str(error))
        logger.error("Concept translated artifact materialization failed for %s: %s", job_id, error)
        upsert_concept_translated_artifact(
            consumer_key=context["consumer_key"],
            external_project_id=context["external_project_id"],
            concept_name=context["concept_name"],
            analysis_mode=context["analysis_mode"],
            workflow_key=context["workflow_key"],
            engine_or_chain_key=context["engine_or_chain_key"],
            depth=context["depth"],
            analyzer_v2_job_id=job_id,
            translation_template_key=context["translation_template_key"],
            contract_validation_status=validation_status,
            translated_artifact=translated_artifact,
            validation_errors=validation_errors,
            analysis_context=context,
        )
        raise

    return upsert_concept_translated_artifact(
        consumer_key=context["consumer_key"],
        external_project_id=context["external_project_id"],
        concept_name=context["concept_name"],
        analysis_mode=context["analysis_mode"],
        workflow_key=context["workflow_key"],
        engine_or_chain_key=context["engine_or_chain_key"],
        depth=context["depth"],
        analyzer_v2_job_id=job_id,
        translation_template_key=context["translation_template_key"],
        contract_validation_status=validation_status,
        translated_artifact=translated_artifact,
        validation_errors=validation_errors,
        analysis_context=context,
    )
