"""Checkpointed bilateral inquiry; intellectual judgments live in method records."""
from __future__ import annotations

import hashlib
import re

from src.dossier.evidence_routing import canonical_evidence, selection_groups, support_route

from src.dossier.investigation import (
    _context, _eligible, _excerpt, _field, _json, _now, _queries, _spec, citation_catalog,
    inspected_ranges, quote_span, recover_answer_rows, search_inventory,
    validate_memo_citations,
)

CHAIN = "field_investigation"


def _ids(value):
    if isinstance(value, list):
        return [str(v).strip("[]") for v in value if v]
    return [v.strip("[]") for v in re.split(r"[\s,;]+", str(value or "")) if "/" in v]


def validate_claims(rows, evidence, *, required=False, field_map=False):
    """Check support identities and source roles, without claiming semantic truth."""
    verified = {e["citation_id"]: e for e in evidence if e["quote_verified"]}
    errors, claims, summaries = [], [], []
    typed_debate = any(r.get('dim') == 'debate' and _field(r, 'claim_kind') in
                       ('field_finding', 'unresolved') for r in rows)
    for row in rows:
        if row.get("dim") not in ("answer", "judgment", "debate"):
            continue
        claims.append(row)
        ids = _ids(_field(row, "evidence_ids"))
        unknown = set(ids) - verified.keys()
        kind = _field(row, "claim_kind")
        roles = {verified[i]["source_role"] for i in ids if i in verified}
        # A oneshot answer can contain the method's E1 ledger followed by a
        # generic Fn summary ledger that omits method-specific fields. Retain
        # those summaries and check ALL their original support IDs, but do not
        # invent a claim classification or count them as typed method output.
        # This exception is confined to field maps with an actual typed ledger.
        if (field_map and typed_debate and row.get('dim') == 'debate' and not kind
                and re.fullmatch(r'F\d+', str(row.get('id', '')))
                and ids and not unknown and roles == {'field'}):
            claims.pop()
            summaries.append({'id': row['id'], 'evidence_ids': ids,
                              'classification': 'unclassified_field_summary'})
            continue
        needed = {"thinker_position": {"primary"}, "field_finding": {"field"},
                  "comparison": {"primary", "field"}, "unresolved": set()}.get(kind)
        if needed is None or unknown or (needed and (not ids or not needed <= roles)):
            errors.append({"id": row.get("id"), "claim_kind": kind, "evidence_ids": ids,
                           "unknown_or_unverified": sorted(unknown), "source_roles": sorted(roles)})
    if required and not claims:
        errors.append({"error": "missing_claim_ledger"})
    return {"supported": not errors, "errors": errors, "claim_count": len(claims),
            "unclassified_field_summaries": summaries,
            "semantic_attribution_checked_by": "method_not_code"}


def _pages(row, start, end):
    pages = [p["page"] for p in row.get("page_spans", []) if p["start"] < end and start < p["end"]]
    pdf = row.get("pdf_url")
    return pages, [f"{pdf.split('#')[0]}#page={p}" for p in pages] if pdf else []


def _memo_validation(memo, evidence, mode):
    prose = memo.get("prose") or memo.get("final_output", "")
    citations = validate_memo_citations(prose, evidence)
    claims = validate_claims(memo.get("rows", []), evidence, required=True)
    verified_ids = {e["citation_id"] for e in evidence if e["quote_verified"]}
    changes = [r for r in memo.get("rows", []) if r.get("dim") == "revision"]
    errors = [r.get("id") for r in changes if _field(r, "disposition") not in ("changed", "retained", "new", "unresolved")
              or _field(r, "baseline") != ("prior" if mode == "follow_up" else "standalone")
              or set(_ids(_field(r, "evidence_ids"))) - verified_ids]
    validation = {**citations, "claims": claims, "revision_errors": errors, "missing_revision_ledger": not bool(changes),
                  "supported": citations["supported"] and claims["supported"] and bool(changes) and not errors}
    return prose, changes, validation


def _limits(packet, inventories, bodies):
    configured = packet.get("limits") or {}
    limits = {}
    for role in ("field", "primary"):
        if role == "primary" and packet.get("inquiry_type") == "institutional":
            limits[role] = {"max_texts": 0, "max_chars": 0, "eligible_count": 0}
            continue
        text_ceiling = 80 if role == "field" else 40
        max_texts = min(text_ceiling, max(1, int(configured.get(f"max_{role}_texts", configured.get("max_read_texts", 80 if role == "field" else 12)))))
        max_chars = min(8000000 if role == "field" else 960000, max(1, int(configured.get(f"max_{role}_chars", 3000000 if role == "field" else 240000))))
        eligible = [r for r in inventories[role] if _eligible(r) and bodies.get(r["source_key"])]
        if not eligible:
            raise ValueError(f"field investigation needs at least one available {role} body")
        if role == "field" and len(eligible) > max_texts:
            raise ValueError(f"{role} inventory exceeds {max_texts} selected texts; narrow the packet before spending")
        # Every selected item receives an actual reading. Never silently drop a
        # text to meet the cap. Short texts require only their actual length.
        minimum = sum(sorted(min(len(bodies[r["source_key"]]), 5000) for r in eligible)[:max_texts])
        if max_chars < minimum:
            raise ValueError(f"{role} character cap cannot inspect every selected text; need at least {minimum}")
        limits[role] = {"max_texts": max_texts, "max_chars": max_chars, "eligible_count": len(eligible)}
    return limits


def _reading_allocations(rows, bodies, cap):
    """Read short works whole when affordable, reserving room for every long work."""
    lengths = {r["uid"]: len(bodies[r["source_key"]]) for r in rows}
    short = {uid: n for uid, n in lengths.items() if n <= 100000}
    long = [uid for uid in lengths if uid not in short]
    if sum(short.values()) + 5000 * len(long) <= cap:
        allocations = dict(short)
        remaining = cap - sum(short.values())
        for index, uid in enumerate(long):
            allocations[uid] = min(100000, remaining // (len(long) - index))
            remaining -= allocations[uid]
        return allocations
    allocations = {uid: min(n, 5000) for uid, n in lengths.items()}
    remaining = cap - sum(allocations.values())
    while remaining > 0:
        active = [uid for uid, n in lengths.items() if allocations[uid] < min(n, 100000)]
        if not active:
            break
        share = max(1, remaining // len(active))
        for uid in active:
            grant = min(share, remaining, min(lengths[uid], 100000) - allocations[uid])
            allocations[uid] += grant
            remaining -= grant
    return allocations


def _baseline_context(packet):
    """Keep reviewed memos whole without repeating multi-megabyte search artifacts."""
    priors = packet.get("prior_investigations") or []
    if isinstance(priors, dict):
        priors = [priors]
    entries = []
    for prior in priors:
        if not isinstance(prior, dict) or not isinstance(prior.get("answer"), dict):
            entries.append(prior)
            continue
        answer = prior["answer"]
        entry = {k: v for k, v in prior.items() if k != "answer"}
        entry.setdefault("memo", answer.get("memo", ""))
        if isinstance(answer.get('field_map'), dict):
            entry.setdefault('argument_map', answer['field_map'].get('final_output', ''))
        entry["answer_manifest"] = {"job_id": answer.get("job_id"), "coverage": answer.get("coverage"),
                                    "memo_validation": answer.get("memo_validation"),
                                    "read_uids": [r.get("uid") for r in answer.get("readings", [])],
                                    "evidence_count": len(answer.get("evidence", [])),
                                    "full_answer_retained_in_frozen_packet": True}
        entries.append(entry)
    return _json(entries)


def run_field_investigation(packet, bodies, *, call, save, state=None, check=lambda: None, spend_cap_usd=8.0):
    institutional = packet.get("inquiry_type") == "institutional"
    if institutional and (packet.get("author") or packet.get("primary") or packet.get("secondary")):
        raise ValueError("institutional inquiry cannot include a target thinker or primary inventory")
    inventories = {role: packet[role] for role in ("field", "primary")}
    # Metadata and body content must agree even on a resumed run; the hash in a
    # frozen plan cannot bless a replacement PDF rendition.
    for rows in [*inventories.values(), packet.get("secondary", [])]:
        for row in rows:
            body = bodies.get(row["source_key"], "")
            actual = hashlib.sha256(body.encode()).hexdigest() if body else None
            if actual != row["body_sha256"] or len(body) != row["body_chars"]:
                raise ValueError(f"source rendition changed: {row['source_key']}")
    limits = _limits(packet, inventories, bodies)
    fingerprint = hashlib.sha256(_json(packet).encode()).hexdigest()
    state = state or {"version": 1, "kind": CHAIN, "packet_sha256": fingerprint,
                      "author": packet["author"], "inquiry_type": packet.get("inquiry_type", "bilateral"),
                      "question": packet["question"], "scope": packet.get("scope", {}),
                      "inventory": packet["primary"], "field_inventory": packet["field"],
                      "field_collections": packet.get("field_collections", []), "field_gaps": packet.get("field_gaps", []),
                      "prior_readings_resolution": packet.get("prior_readings_resolution", []),
                      "mode": "follow_up" if packet.get("prior_investigations") else "standalone",
                      "stages": [], "calls": {}, "analysis": {}, "cost_usd": 0.0,
                      "evidence": [], "readings": [], "read_inputs": {}, "complete": False}
    if state.get("packet_sha256") != fingerprint:
        raise ValueError("the frozen investigation packet changed; create a new run")
    if state.get('complete'):
        return state  # A completed historical answer is not silently reinterpreted on resume.
    from src.engines.methods import field_methods, validate_contract, validate_snapshot, method_receipt
    validate_contract(packet)
    if 'method_snapshots' not in state:
        legacy = bool(state.get('calls'))
        state['method_snapshots'] = field_methods(legacy=legacy, institutional=institutional)
        state['method_origin'] = 'archived pre-refactor methods' if legacy else 'central registry frozen before first call'
    for key, snapshot in state['method_snapshots'].items():
        validate_snapshot(snapshot, key)
    state.setdefault("quote_layout_reviews", packet.get("quote_layout_reviews") or {})
    if not isinstance(state["quote_layout_reviews"], dict):
        raise ValueError("quote layout reviews must be keyed by source UID")

    def checkpoint(stage, **fields):
        state.update(fields, updated_at=_now(), current_stage=stage)
        state.setdefault("stage_status", {})[stage] = "running" if state.get("running_stage") == stage else "complete"
        if stage not in state["stages"]:
            state["stages"].append(stage)
        save(state)

    def engine(stage, key, sources, upstream):
        check()
        from src.engines.methods import digest
        contract = digest({'engine': key, 'sources': [(s.key, s.text) for s in sources], 'upstream': upstream})
        contracts = state.setdefault('call_contracts', {})
        if stage in contracts and contracts[stage] != contract:
            raise ValueError(f'{stage} frozen call input changed; fork a new investigation instead of reusing stale output')
        if stage in state["calls"]:
            previous_ids = state.get('call_input_manifests', {}).get(stage, {}).get('evidence_ids')
            if (stage not in contracts and 'evidence' in upstream and previous_ids is not None
                    and set(previous_ids) != {e['citation_id'] for e in upstream['evidence']}):
                raise ValueError(f'{stage} historical support inputs differ from the corrected route; '
                                 'create a separate replay instead of reusing a stale synthesis')
            result = state["calls"][stage]
            recover_answer_rows(result)
            return result
        remaining = spend_cap_usd - state["cost_usd"]
        if remaining <= 0:
            checkpoint(stage, paused_reason="spend_cap")
            raise ValueError("investigation spend cap reached; completed artifacts were saved")
        from src.dossier.context_packing import input_hash, pack_final_context
        from src.dossier.reporter_context import pack_reporter_context
        sources, upstream, reporter_packing = pack_reporter_context(stage, sources, upstream, packet_sha256=fingerprint)
        sources, upstream, packing = pack_final_context(stage, sources, upstream, packet_sha256=fingerprint)
        chars = sum(len(s.text) for s in sources) + len(_json(upstream))
        representation = "verified_quotations"
        final_stage = stage.split(":", 1)[0] in ("adjudication", "memo")
        if not final_stage and chars > 520000 and isinstance(upstream.get("evidence"), list):
            # The argument maps already state the field claims with original
            # support IDs. At the context limit, retain every such ID and its
            # verified role instead of repeating the same field quotations.
            # Author quotations remain present for direct thinker attribution.
            upstream = {**upstream, "evidence": [
                {k: e[k] for k in ("citation_id", "source_role", "quote_verified")}
                if e["source_role"] == "field" else e for e in upstream["evidence"]],
                "field_evidence_representation": "reference_index_to_supplied_argument_maps",
                "full_field_evidence_retained": True}
            representation = "field_reference_index_and_primary_quotations"
            chars = sum(len(s.text) for s in sources) + len(_json(upstream))
        state.setdefault("call_input_manifests", {})[stage] = {
            "chars": chars, "evidence_representation": representation,
            "evidence_ids": [e["citation_id"] for e in upstream.get("evidence", [])],
            "method_receipt": method_receipt(state['method_snapshots'][key])}
        if reporter_packing:
            state["call_input_manifests"][stage]["reporter_packing"] = reporter_packing
        if packing:
            # Full omitted metadata and exact input/text hashes remain durable.
            # Final-stage cited quotes stay protected even if the guard stops.
            packing.update(final_chars=chars, final_input_sha256=input_hash(sources, upstream),
                           field_reference_fallback_applied=representation != "verified_quotations",
                           all_evidence_quotes_and_findings_retained=representation == "verified_quotations")
            state["call_input_manifests"][stage]["packing"] = packing
        if chars > 640000:
            checkpoint(stage, paused_reason="input_limit", complete=False)
            raise ValueError(f"{stage} input is {chars:,} characters after evidence packing; "
                             "all completed research retained; additional source-preserving compaction is required")
        contracts[stage] = contract
        checkpoint(stage, running_stage=stage)
        from contextlib import nullcontext
        from src.executor.spend_guard import budget
        bounded = institutional or any((c.get('source_policy') or {}).get('institutions_only') for c in packet.get('field_collections', []))
        with budget(state, spend_cap_usd, save) if bounded else nullcontext():
            result = call(key, sources, packet=upstream, depth="surface", spend_cap_usd=remaining, max_chars=650000,
                          method_snapshot=state['method_snapshots'][key])
        recover_answer_rows(result)
        state["calls"][stage] = result
        state["cost_usd"] += float(result.get("cost_usd") or 0)
        phase = str(len(state["analysis"]) + 1)
        state["analysis"][phase] = {"phase_number": int(phase), "stage": stage, "engine_key": key,
                                    "method_receipt": method_receipt(state['method_snapshots'][key]),
                                    "depth": "surface", "final_output": result.get("final_output", ""),
                                    "final_wall": result.get("wall", {}), "cost_usd": result.get("cost_usd"),
                                    "sources": [s.key for s in sources], "finished": _now(), "calls": result.get("calls", [])}
        checkpoint(stage, running_stage=None)
        return result

    def supported_engine(stage, key, sources, upstream):
        result = engine(stage, key, sources, upstream)
        validation = validate_claims(result.get("rows", []), state["evidence"], required=True,
                                     field_map=key == 'field_investigation_field_map')
        if not validation["supported"]:
            # Keep the paid draft under its original stage. A bounded repair uses
            # the same source evidence; it cannot verify a fabricated quotation.
            result = engine(f"{stage}:repair", key, sources,
                            {**upstream, "previous_draft": result.get("final_output"), "validation_errors": validation})
            validation = validate_claims(result.get("rows", []), state["evidence"], required=True,
                                         field_map=key == 'field_investigation_field_map')
        return result, validation

    common = {"author": packet["author"], "inquiry_type": packet.get("inquiry_type", "bilateral"),
              "question": packet["question"], "scope": packet.get("scope", {}),
              "field_collections": packet.get("field_collections", []), "field_gaps": packet.get("field_gaps", []),
              "mode": state["mode"], "as_of": state.setdefault("as_of", _now())}
    state.setdefault('prior_context_policy', 'legacy_all' if state['calls'] else 'question_queries')
    if packet.get('research_feedback'):
        common['research_feedback'] = packet['research_feedback']
        state['research_feedback'] = packet['research_feedback']
    context = [c for c in _context(packet, bodies, cap=40000) if c["key"] != "prior_investigations"]
    baseline = _baseline_context(packet)
    baseline_ranges = [(0, len(baseline))] if len(baseline) <= 200000 else [(0, 100000), (len(baseline) - 100000, len(baseline))]
    context.append({"key": "prior_investigations", "kind": "prior_investigations", "title": "Prior investigation baseline",
                    "total_chars": len(baseline), "supplied_chars": min(len(baseline), 200000),
                    "answer_artifacts_summarized": True, "full_prior_packet_chars": len(_json(packet.get("prior_investigations") or [])),
                    "truncated": len(baseline) > 200000, "inspected_ranges": baseline_ranges,
                    "text": _excerpt(baseline, baseline_ranges), "selected_for_context": True})
    # The entire baseline memo is retained in the frozen packet; disclose windows
    # rather than accidentally presenting truncated JSON as a complete baseline.
    checkpoint("context", context_manifest=[{k: v for k, v in c.items() if k != "text"} for c in context], limits=limits)
    summary = {role: [{**{k: row.get(k) for k in ("uid", "title", "year", "authors", "date_scope", "body_state")},
                       "profile_summary": _json(row.get("profile") or {})[:1200],
                       "profile_summary_truncated": len(_json(row.get("profile") or {})) > 1200}
                      for row in rows] for role, rows in inventories.items()}
    plan = engine("plan", "institutional_inquiry_plan" if institutional else "field_investigation_plan", [_spec("investigation-question", _json(common)),
                  _spec("investigation-inventory", _json(summary)), _spec("prior-context", _json(context))], common)
    queries = _queries(plan.get("rows") or [])
    if not queries:
        checkpoint("plan", plan=plan, paused_reason="planner_returned_no_queries")
        raise ValueError("field planner returned no valid literal queries; output saved")
    if state['prior_context_policy'] == 'question_queries':
        # Use the planner's saved literal queries to select optional prior
        # context, as the shared context helper already supports. The complete
        # reviewed baseline remains supplied; every original remains frozen.
        queried_context = _context(packet, bodies, cap=40000, queries=queries)
        baseline_entry = context[-1]
        context = [c for c in queried_context if c['key'] != 'prior_investigations' and c['selected_for_context']]
        context.append(baseline_entry)
        checkpoint('context_selection', context_manifest=[{k:v for k,v in c.items() if k != 'text'}
                   for c in queried_context if c['key'] != 'prior_investigations'] +
                   [{k:v for k,v in baseline_entry.items() if k != 'text'}],
                   prior_context_selection={'queries': queries, 'policy': 'question_queries',
                                            'complete_prior_records_retained_in_packet': True})
    if "searches" not in state:
        checkpoint("search", plan=plan, queries=queries,
                   searches=search_inventory(packet["field"] + packet["primary"], bodies, queries))
    search_by = {r["uid"]: r for r in state["searches"]}

    def reading_context(role):
        return [{"uid": r["uid"], "title": r["title"], "source_role": role, "year": r.get("year"),
                 "reading": r["reading"], "source_metadata": r["source_metadata"],
                 "inspected_ranges": r["inspected_ranges"], "reading_mode": r["reading_mode"]}
                for r in state["readings"] if r["source_role"] == role]

    def evidence_context(role=None):
        return [{k: v for k, v in e.items() if k in ("citation_id", "uid", "source_key", "source_role", "finding",
                                                    "source_quote", "quote_verified", "conjecture", "quote_start", "quote_end",
                                                    "quote_match", "quote_layout", "pages", "page_urls", "title", "year", "fields")}
                for e in state["evidence"] if role is None or e["source_role"] == role]

    def read_population(role, guidance, selected_uids=None):
        eligible = [r for r in inventories[role] if _eligible(r) and bodies.get(r["source_key"])]
        if selected_uids is not None:
            by_uid = {r["uid"]: r for r in eligible}
            eligible = [by_uid[uid] for uid in selected_uids if uid in by_uid]
        if sum(min(len(bodies[r["source_key"]]), 5000) for r in eligible) > limits[role]["max_chars"]:
            raise ValueError(f"{role} cap cannot inspect every selected text")
        if role not in state.setdefault("reading_allocations", {}):
            state["reading_allocations"][role] = _reading_allocations(eligible, bodies, limits[role]["max_chars"])
            checkpoint("reading_allocations")
        allocations = state["reading_allocations"][role]
        consumed = 0
        for index, row in enumerate(eligible):
            check()
            uid, key = row["uid"], row["source_key"]
            stage = f"read:{key}"
            body = bodies[key]
            saved = state["read_inputs"].get(stage)
            if saved:
                ranges = saved["ranges"]
            else:
                if stage in state["calls"]:
                    raise ValueError(f"cached reading has no frozen source ranges: {key}")
                allocation = allocations[uid]
                more_queries = _queries((guidance or {}).get("rows", []))
                if role == "primary":
                    more_queries += [q.strip() for q in str(_field(decisions.get(uid, {}), "queries")).split(";") if q.strip()]
                ranges = inspected_ranges(body, search_by[uid], allocation, more_queries)
                if not ranges:
                    raise ValueError(f"no source window allocated for selected text: {key}")
                state["read_inputs"][stage] = {"ranges": ranges, "body_sha256": row["body_sha256"],
                                                "source_key": key, "allocation": allocation}
                checkpoint("reading_inputs")
            if saved and saved["body_sha256"] != row["body_sha256"]:
                raise ValueError(f"cached reading source hash changed: {key}")
            consumed += sum(hi - lo for lo, hi in ranges)
            if consumed > limits[role]["max_chars"]:
                raise ValueError(f"saved {role} reading spans exceed the frozen allowance")
            metadata = {k: v for k, v in row.items() if k not in ("profile", "citations", "page_spans")}
            result = engine(stage, f"field_investigation_{'field' if role == 'field' else 'author'}_read",
                            [_spec(key, _excerpt(body, ranges), row.get("title", ""))],
                            {**common, "plan": plan.get("final_output"), "source_metadata": metadata,
                             "selection_guidance": decisions.get(uid) if role == "primary" else None,
                             "inspected_ranges": ranges, "guidance": (guidance or {}).get("final_output", ""),
                             "page_spans": [p for p in row.get("page_spans", [])
                                            if any(p["start"] < hi and lo < p["end"] for lo, hi in ranges)]})
            reading = {"uid": uid, "source_key": key, "source_role": role, "title": row.get("title"),
                       "year": row.get("year"), "read_uid": row.get("read_uid"), "body_sha256": row["body_sha256"],
                       "source_metadata": metadata, "reading": result.get("prose") or result.get("final_output", ""),
                       "rows": result.get("rows", []), "inspected_ranges": ranges,
                       "inspected_chars": sum(hi - lo for lo, hi in ranges),
                       "reading_mode": "full" if ranges == [(0, len(body))] or ranges == [[0, len(body)]] else "windows"}
            state["readings"] = [r for r in state["readings"] if r["source_key"] != key] + [reading]
            state["evidence"] = [e for e in state["evidence"] if e["source_key"] != key]
            for r in result.get("rows", []):
                if r.get("dim") != "evidence":
                    continue
                quote = str(r.get("anchor") or "")
                span = quote_span(quote, body, ranges)
                layout_quote = None
                if span is None and role == "field" and row.get("page_spans"):
                    from src.dossier.pdf_quote_layout import pdf_column_quote
                    layout_quote = pdf_column_quote(
                        quote, body, ranges, row["page_spans"],
                        review=state["quote_layout_reviews"].get(uid),
                        pdf_sha256=row.get("pdf_sha256") or (row.get("source_metadata") or {}).get("pdf_sha256"))
                    if layout_quote:
                        span = (layout_quote["quote_start"], layout_quote["quote_end"], layout_quote["quote_match"])
                verified = bool(span) and r.get("doc") == key and _field(r, "uid") in ("", uid)
                pages, links = _pages(row, span[0], span[1]) if verified else ([], [])
                evidence = {**r, "uid": uid, "source_key": key, "source_role": role,
                    "title": row.get("title"), "year": row.get("year"), "source_metadata": metadata,
                    "read_uid": row.get("read_uid"), "body_sha256": row["body_sha256"],
                    "quote": quote, "model_quote": quote, "source_quote": body[span[0]:span[1]] if verified else None,
                    "quote_verified": verified, "anchor_verified": verified, "conjecture": not verified,
                    "quote_start": span[0] if verified else None, "quote_end": span[1] if verified else None,
                    "quote_match": span[2] if verified else None, "pages": pages, "page_urls": links,
                    "citation_id": f"{uid}/{r.get('id', '')}"}
                if verified and layout_quote:
                    evidence.update(layout_quote)
                state["evidence"].append(evidence)
            state['evidence'], duplicates = canonical_evidence(state['evidence'])
            state.setdefault('evidence_identity_receipts', {})[key] = duplicates
            checkpoint("reading")

    read_population("field", plan)
    field_readings = reading_context("field")
    field_evidence = evidence_context("field")
    bundles, current, chars = [], [], 0
    for reading in field_readings:
        item = {"reading": reading, "evidence": [e for e in field_evidence if e["uid"] == reading["uid"]]}
        size = len(_json(item))
        if current and chars + size > 200000:
            bundles.append(current)
            current, chars = [], 0
        current.append(item)
        chars += size
    if current:
        bundles.append(current)
    maps = []
    for index, bundle in enumerate(bundles):
        result, validation = supported_engine(f"field_map:{index + 1}", "field_investigation_field_map",
                        [_spec("field-readings", _json(bundle))],
                        {**common, "plan": plan.get("final_output"), "map_scope": "batch",
                         "batch_number": index + 1, "batch_count": len(bundles)})
        maps.append(result)
        checkpoint("field_mapping", field_maps=maps)
        if not validation["supported"]:
            checkpoint("field_mapping", field_map_validation=validation)
            raise ValueError("field map support validation failed; map and readings retained")
    batch_support = support_route(maps, field_evidence)
    checkpoint('support_routing', support_routes={'batch_to_global': batch_support})
    if len(maps) == 1:
        field_map = maps[0]
        field_validation = validate_claims(field_map.get("rows", []), state["evidence"], required=True, field_map=True)
    else:
        cited_ids = set(batch_support["eligible_ids"])
        field_map, field_validation = supported_engine("field_map", "field_investigation_field_map",
                       [_spec("field-map-batches", _json([m.get("final_output") for m in maps]))],
                       {**common, "plan": plan.get("final_output"), "map_scope": "global_reconciliation",
                        "evidence": [e for e in field_evidence if e["citation_id"] in cited_ids],
                        "evidence_selection": batch_support["policy"], "support_route": batch_support,
                        "field_evidence_total": len(field_evidence), "full_readings_retained": True,
                        "source_catalog": [{"uid": r["uid"], "title": r.get("title")} for r in packet["field"]]})
    checkpoint("field_map", field_map=field_map, field_map_validation=field_validation)
    if not field_validation["supported"]:
        raise ValueError("field map support validation failed; map and readings retained")
    if not institutional:
        # Explicit scope exclusions are already decisions, not paid semantic
        # selection candidates. Preserve the full inventory in the packet and
        # coverage, but supply complete profiles only for permitted candidates.
        # Older paid batches keep their original boundaries on resumption.
        legacy_selection = any(k.startswith('author_selection') for k in state['calls']) and state.get('author_selection_scope') is None
        if state.get('author_selection_scope') is None:
            state['author_selection_scope'] = 'legacy_full_inventory' if legacy_selection else 'eligible_inventory'
        candidates = [r for r in packet['primary'] if state['author_selection_scope'] == 'legacy_full_inventory' or _eligible(r)]
        batches, current, chars = [], [], 0
        for row in candidates:
            search = search_by[row["uid"]]
            item = {"inventory": {**row, "citations": citation_catalog(row.get("citations") or [])},
                    "search": {"match_count": search["match_count"],
                               "matches": [{"query": m["query"], "count": m["count"], "hits": m["hits"][:1]}
                                           for m in search["matches"][:12]]}}
            size = len(_json(item))
            if current and (chars + size > 180000 or len(current) >= 20):
                batches.append(current)
                current, chars = [], 0
            current.append(item)
            chars += size
        if current:
            batches.append(current)
        decisions = {}
        for index, batch in enumerate(batches):
            allowed = {r["inventory"]["uid"] for r in batch}
            result = engine(f"author_selection:{index + 1}", "field_investigation_author_select",
                            [_spec("author-inventory", _json(batch))],
                            {**common, "field_map": field_map.get("final_output"), "prior_context": context,
                             "selection_mode": "batch", "limits": limits["primary"]})
            decisions.update(selection_groups(result.get('rows', []), allowed))
            for uid in allowed - decisions.keys():
                decisions[uid] = {"uid": uid, "decision": "unjudged", "triage_missing": True,
                                  "reason": "No valid semantic decision returned; reconcile explicitly"}
            checkpoint("author_selection", triage=list(decisions.values()))
        reconciliation = engine("author_selection", "field_investigation_author_select",
                                [_spec("author-selection", _json([{"inventory": {k: row.get(k) for k in
                                     ("uid", "title", "year", "date_scope", "body_state", "body_chars")},
                                     "prior_decision": decisions[row["uid"]]} for row in candidates]))],
                                {**common, "field_map": field_map.get("final_output"), "selection_mode": "reconcile",
                                 "prior_context": context, "limits": limits["primary"]})
        resolved = selection_groups(reconciliation.get('rows', []), decisions)
        conflicts = {uid: r for uid, r in resolved.items() if r['selection_conflict']}
        conflicts.update({uid: r for uid, r in decisions.items() if r.get('selection_conflict') and uid not in resolved})
        if conflicts:
            checkpoint('author_selection_conflicts', selection_conflicts=conflicts)
            repair = engine('author_selection:conflict_repair', 'field_investigation_author_select',
                            [_spec('author-selection-conflicts', _json(list(conflicts.values())))],
                            {**common, 'selection_mode': 'resolve_conflicts',
                             'field_map': field_map.get('final_output'), 'limits': limits['primary'],
                             'previous_selection': reconciliation.get('final_output'),
                             'uncontested_decisions': [r for r in resolved.values() if not r['selection_conflict']]})
            repaired = selection_groups(repair.get('rows', []), conflicts)
            unresolved = [uid for uid in conflicts if uid not in repaired or repaired[uid]['selection_conflict']]
            checkpoint('author_selection_conflicts', selection_conflict_resolution=repair,
                       unresolved_selection_uids=unresolved)
            if unresolved:
                raise ValueError('author selection has unresolved conflicting decisions; all rationales and paid work retained')
            resolved.update(repaired)
        selection_order = list(resolved)
        available = {r['uid'] for r in packet['primary'] if _eligible(r) and bodies.get(r['source_key'])}
        for uid, decision in resolved.items():
            decisions[uid] = {**decision, 'prior_decision': decisions[uid]}
        # The method's global ordering defines the cap, never title or uid sorting.
        ordered_candidates = [uid for uid in selection_order if uid in available and decisions[uid]["decision"] == "read"]
        selected = ordered_candidates[:limits["primary"]["max_texts"]]
        for uid in ordered_candidates[limits["primary"]["max_texts"]:]:
            decisions[uid] = {**decisions[uid], "decision": "defer", "deferred_by_cap": True,
                              "model_decision": "read", "reason": "Global reading cap; " + str(decisions[uid].get("reason", ""))}
        checkpoint("author_selection", triage=list(decisions.values()), selected_primary_uids=selected,
                   selection=reconciliation)
        if not selected:
            raise ValueError("author selection returned no available core texts; decisions retained")
        read_population("primary", field_map, selected)
    coverage = {"inventory_count": sum(len(r) for r in inventories.values()),
                "field_gaps": packet.get("field_gaps", []),
                "read_count": len(state["readings"]), "inspected_chars": sum(r["inspected_chars"] for r in state["readings"]),
                "full_read_count": sum(r["reading_mode"] == "full" for r in state["readings"]),
                "window_read_count": sum(r["reading_mode"] == "windows" for r in state["readings"]),
                "absence_claims_supported": False, "limits": limits}
    for role, rows in inventories.items():
        reads = [r for r in state["readings"] if r["source_role"] == role]
        coverage[role] = {"inventory_count": len(rows), "read_count": len(reads),
                          "full_read_count": sum(r["reading_mode"] == "full" for r in reads),
                          "inspected_chars": sum(r["inspected_chars"] for r in reads),
                          "missing_uids": [r["uid"] for r in rows if _eligible(r) and not bodies.get(r["source_key"])],
                          "excluded_uids": [r["uid"] for r in rows if not _eligible(r)],
                          "unread_uids": [r["uid"] for r in rows if r["uid"] not in {read["uid"] for read in reads}]}
    for key in ("missing_uids", "excluded_uids", "unread_uids"):
        coverage[key] = sum((coverage[r][key] for r in inventories), [])
    checkpoint("coverage", coverage=coverage)
    final_support = support_route([field_map], field_evidence, batch_support['eligible_ids'])
    state['support_routes']['global_to_synthesis'] = final_support
    checkpoint('support_routing')
    mapped_ids = set(final_support['eligible_ids'])
    research = {**common, "coverage": coverage, "field_map": field_map.get("final_output"),
                "evidence": [e for e in evidence_context() if e["source_role"] == "primary" or e["citation_id"] in mapped_ids],
                "evidence_selection": "all primary evidence plus " + final_support["policy"], "support_route": final_support,
                "field_evidence_total": len(field_evidence), "full_field_evidence_retained": True, "prior_context": context}
    reading_sources = [_spec("field-argument-map", field_map.get("final_output", "")),
                       _spec("primary-readings", _json(reading_context("primary")))]
    if institutional:
        adjudication, adjudication_validation = field_map, field_validation
        reading_sources = [reading_sources[0]]
    else:
        adjudication, adjudication_validation = supported_engine("adjudication", "field_investigation_adjudicate", reading_sources, research)
        checkpoint("adjudication", adjudication=adjudication, adjudication_validation=adjudication_validation)
        if not adjudication_validation["supported"]:
            raise ValueError("adjudication support validation failed; research retained")
    memo_key = "institutional_inquiry_memo" if institutional else "field_investigation_memo"
    memo = engine("memo", memo_key, reading_sources,
                  {**research, "adjudication": adjudication.get("final_output")})
    prose, changes, validation = _memo_validation(memo, state["evidence"], state["mode"])
    checkpoint("memo_validation", memo=prose, memo_rows=memo.get("rows", []), memo_validation=validation, changes=changes)
    if not validation["supported"]:
        memo = engine("memo:repair", memo_key, reading_sources,
                      {**research, "adjudication": adjudication.get("final_output"),
                       "previous_draft": memo.get("final_output"), "validation_errors": validation})
        prose, changes, validation = _memo_validation(memo, state["evidence"], state["mode"])
        checkpoint("memo_validation", memo=prose, memo_rows=memo.get("rows", []), memo_validation=validation, changes=changes)
    if not validation["supported"]:
        checkpoint("memo_validation", paused_reason="memo_support_validation", complete=False)
        raise ValueError("memo support/revision validation failed; draft and full research retained")
    checkpoint("done", complete=True, running_stage=None, paused_reason=None)
    return state


def run_job_field_investigation(job, docs, *, cancel_check=None, persist=None):
    from src.dossier.investigation import run_job_investigation
    return run_job_investigation(job, docs, cancel_check=cancel_check, persist=persist,
                                 chain=CHAIN, executor=run_field_investigation)
