"""Opt-in scope records: validate identity and evidence state, never semantic absence."""
from __future__ import annotations

import json
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.executor.ledger_walls import parse_rows

OUTCOME_HEADING = "## Scope outcomes"
_SECTION = re.compile(r"^\s{0,3}(?:#{1,4}[ \t]*|\*\*)scope[ -]outcomes?\b[^\n]*\n?(.*?)(?=^\s{0,3}#{1,4}[ \t]|\Z)", re.M | re.S | re.I)


class ScopeOutcome(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    document_keys: list[str] = Field(min_length=1)
    dimension_key: str = Field(min_length=1)
    outcome: Literal["findings_present", "no_relevant_instance", "inconclusive"]
    sections_inspected: list[str]
    coverage: Literal["complete", "partial", "unknown"]
    criterion: str = Field(min_length=1)
    basis: str = Field(min_length=1)
    limitations: list[str]
    finding_ids: list[str]
    review_state: Literal["unchecked", "supported_within_stated_scope", "disputed"] = "unchecked"
    review_basis: str = ""

    @field_validator("criterion", "basis", "dimension_key")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("scope text must not be blank")
        return value

    @field_validator("document_keys", "sections_inspected", "limitations", "finding_ids")
    @classmethod
    def text_items(cls, value):
        if any(not item.strip() for item in value) or len(set(value)) != len(value):
            raise ValueError("scope lists require distinct nonblank strings")
        return value


def scope_key(record):
    return (tuple(sorted(record["document_keys"])), record["dimension_key"])


def expected_scopes(spec, documents, *, doc_key="", dimension=None):
    """Only identities are inferred from dispatch; inspection coverage is model-reported."""
    out = []
    for dim in [dimension] if dimension is not None else spec.dimensions:
        if dim.scope == "corpus":
            if len(documents) > 1 and not doc_key:
                out.append({"document_keys": list(documents), "dimension_key": dim.key})
        else:
            out.extend({"document_keys": [key], "dimension_key": dim.key}
                       for key in ([doc_key] if doc_key else documents))
    return out


def strip_scope_outcomes(content):
    return _SECTION.sub("", content).rstrip()


def render_scope_json(records):
    return OUTCOME_HEADING + "\n```json\n" + json.dumps(records, ensure_ascii=False, indent=2) + "\n```"


def _read_records(content):
    matches = list(_SECTION.finditer(content))
    if len(matches) != 1:
        raise ValueError("expected exactly one Scope outcomes section")
    body = matches[0][1].strip()
    if body.startswith("```"):
        fenced = re.fullmatch(r"```(?:json)?\s*\n(.*?)\n```", body, re.S)
        if not fenced:
            raise ValueError("malformed scope JSON fence")
        body = fenced[1]
    raw = json.loads(body)
    if not isinstance(raw, list):
        raise ValueError("scope outcomes must be a JSON array")
    return [ScopeOutcome.model_validate(item).model_dump() for item in raw]


def assess_scopes(content, expected, rows, documents, *, reviewing=False, previous=(),
                  partial=None, stop_reason=None, error="", evidence_issue="", failed_rows=()):
    """Return every expected scope, with structural problems visibly inconclusive.

    `rows` are retained findings after the current wall/rulings. Rejected valid
    findings can support a reasoned negative review; missing/failed evidence cannot.
    A reviewer claim is recorded as that reviewer's assessment, not a code verdict.
    """
    previous_by_key = {scope_key(r): r for r in previous}
    expected_by_key = {scope_key(r): r for r in expected}
    dimension_keys = {r["dimension_key"] for r in expected}
    issue = ""
    try:
        records = _read_records(content)
        keys = [scope_key(r) for r in records]
        if len(set(keys)) != len(keys) or any(k not in expected_by_key for k in keys):
            raise ValueError("duplicate or unexpected scope identity")
        declared = {scope_key(r): r for r in records}
    except (ValueError, TypeError) as exc:
        declared, issue = {}, f"Malformed/missing scope records: {exc}"
    by_id = {r.id: r for r in rows}
    # Applied critic additions can acquire final IDs. Only an unambiguous lineage
    # alias may bind the review's original identifier to the retained finding.
    aliases = {}
    for row in rows:
        # apply_rulings appends lineage to an added row's rendered text while
        # renumbering its ID. Read that existing declaration, never guess an ID.
        rendered = parse_rows(row.render())
        for alias in set(row.lineage) | set(rendered[0].lineage if rendered else []):
            aliases.setdefault(alias, []).append(row)
    for alias, targets in aliases.items():
        if alias not in by_id and len(targets) == 1:
            by_id[alias] = targets[0]
    result = []
    for key, identity in expected_by_key.items():
        prior = previous_by_key.get(key)
        record = declared.get(key)
        problems = []
        if record is None:
            # A critic omission carries the previous scoped claim unchecked; it
            # cannot acquire support merely because the critic did not mention it.
            record = {**(prior or {}), **identity}
            record.update(outcome="inconclusive", sections_inspected=record.get("sections_inspected", []),
                          coverage=record.get("coverage", "unknown"), criterion=record.get("criterion", "Not reported; consult the process framing and method cards."),
                          basis=record.get("basis", "No valid scoped assessment was returned."),
                          limitations=record.get("limitations", []), finding_ids=record.get("finding_ids", []),
                          review_state="unchecked", review_basis="")
            problems.append(issue or "Missing scope record")
        record = dict(record)
        # Technical diagnostics never participate in model field validation.
        record.pop("evidence_state", None)
        inherited = (prior or {}).get("evidence_state", {}).get("blocking_issues", [])
        problems.extend(inherited)
        if evidence_issue:
            problems.append(evidence_issue)
        scope_docs = set(identity["document_keys"])
        for row in failed_rows:
            row_docs = {a.verified_doc or a.doc for a in row.anchors if a.verified_doc or a.doc}
            intersects = not row_docs or bool(row_docs & scope_docs) or not row_docs <= set(documents)
            if intersects and (row.dim not in dimension_keys or row.dim == identity["dimension_key"]):
                problems.append("Findings in this scope lost anchor evidence; this does not establish absence")
        if any(r.anchor_verified and r.dim not in dimension_keys and
               {a.verified_doc for a in r.anchors if a.verified_doc} & scope_docs for r in rows):
            problems.append("Retained finding has missing or unexpected dimension identity; its scope cannot be assigned")
        if partial or stop_reason in ("length", "max_tokens", "error") or error:
            problems.append("Invocation is known partial or failed")
        if any(not documents.get(d, "").strip() for d in identity["document_keys"]):
            problems.append("Selected source is missing or empty")
        scoped_rows = [r for r in rows if r.anchor_verified and r.dim == identity["dimension_key"]
                       and ({a.verified_doc for a in r.anchors if a.verified_doc} <= set(identity["document_keys"]))]
        if record["outcome"] == "no_relevant_instance":
            if not record["sections_inspected"]:
                problems.append("Negative claim has no inspected sections")
            if record["finding_ids"] or scoped_rows:
                problems.append("Negative claim conflicts with retained findings in this scope")
        if record["outcome"] == "findings_present":
            refs = [by_id.get(rid) for rid in record["finding_ids"]]
            if not refs:
                problems.append("Findings-present claim declares no finding references")
            elif any(r is None or not r.anchor_verified for r in refs):
                problems.append("One or more declared finding references lack retained verified evidence")
            elif any((r.dim != identity["dimension_key"]) or not {a.verified_doc for a in r.anchors if a.verified_doc} <= set(identity["document_keys"]) for r in refs):
                problems.append("Finding identity does not belong to the declared scope")
            else:
                record["finding_ids"] = list(dict.fromkeys(r.id for r in refs))
        if not reviewing:
            record.update(review_state="unchecked", review_basis="")
        elif record["review_state"] != "unchecked" and not record["review_basis"].strip():
            record["review_state"] = "unchecked"
            problems.append("Reviewer supplied no separate review basis")
        if problems:
            record["outcome"] = "inconclusive"
            record["review_state"] = "unchecked"
        record["evidence_state"] = {
            "scope_identity_validated": key in declared,
            "invocation_partial": partial, "invocation_stop_reason": stop_reason,
            "invocation_error": error or None,
            "source_access": {d: "provided" if documents.get(d, "").strip() else "missing" for d in identity["document_keys"]},
            "coverage_basis": "reader/reviewer report; source bytes do not establish inspection or completeness",
            "blocking_issues": list(dict.fromkeys(problems)),
        }
        result.append(record)
    return result


def scope_report(records):
    """A deterministic reader-facing account prevents synthesis from hiding scopes."""
    lines = ["## Scope assessment", "", "These are reader/reviewer assessments of the stated sections, not proofs of absence elsewhere."]
    outcomes = {"findings_present": "findings reported", "no_relevant_instance": "no relevant instance reported", "inconclusive": "inconclusive"}
    reviews = {"unchecked": "not supported by a completed scope review", "supported_within_stated_scope": "reviewer supports this within the stated scope", "disputed": "disputed by the reviewer"}
    def plain(value):
        # Scope text is prose. Embedded newlines cannot become ledger rows when
        # the report follows the ledger; the raw model JSON remains in receipts.
        return " ".join(value.split())

    for r in records:
        lines += ["", f"- Scope {', '.join(plain(k) for k in r['document_keys'])} / {plain(r['dimension_key'])}: {outcomes[r['outcome']]}; {reviews[r['review_state']]}. "
                  f"Inspected sections: {', '.join(plain(section) for section in r['sections_inspected']) or 'not reported'}. Reported coverage: {r['coverage']}. "
                  f"Criterion: {plain(r['criterion'])} Basis: {plain(r['basis'])}"]
        if r["outcome"] == "no_relevant_instance":
            lines.append("  This negative assessment is limited to the reported inspected sections; no wider absence follows.")
        if r["review_basis"]:
            lines.append("  Review basis: " + plain(r["review_basis"]))
        if r["limitations"]:
            lines.append("  Limits: " + "; ".join(plain(limit) for limit in r["limitations"]))
        problems = r.get("evidence_state", {}).get("blocking_issues", [])
        if problems:
            lines.append("  Evidence/record limits: " + "; ".join(plain(problem) for problem in problems))
    return "\n".join(lines)
