"""Step 1 — reconnaissance: read every document → DocumentProfile per doc + corpus map.

One Sonnet call over the whole corpus (1M-context path when the input exceeds
150K tokens); for very large corpora, one call per document and then a
corpus-map call over the profiles. The anchor wall drops key claims whose
verbatim anchor is not in the source text.
"""
from __future__ import annotations

import logging

from src.dossier import events
from src.dossier.common import compact_profiles, corpus_text, doc_header, documents_index
from src.dossier.llm import call_json
from src.dossier.schemas import CorpusMap, DocumentProfile, DossierJob, Reconnaissance
from src.dossier.walls import NormalizedCorpus, verify_anchor
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

STEP = "reconnaissance"
SINGLE_CALL_MAX_CHARS = 700_000
PER_DOC_MAX_CHARS = 700_000

ANCHOR_SCHEMA = {"type": "object", "required": ["doc_key", "quote"], "additionalProperties": False,
                 "properties": {"doc_key": {"type": "string", "description": "the [doc_key] label of the document"},
                                "quote": {"type": "string", "description": "verbatim quote copied exactly from that document, 40-200 characters"}}}
PROFILE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["doc_key", "title", "genre", "one_line", "thesis", "method", "key_claims", "entities", "tensions"],
    "properties": {
        "doc_key": {"type": "string"}, "title": {"type": "string"},
        "genre": {"type": "string", "description": "e.g. empirical study, conceptual essay, bibliometric review, conference paper"},
        "one_line": {"type": "string", "description": "the document in one plain sentence"},
        "thesis": {"type": "string", "description": "its central claim, 1-3 sentences"},
        "method": {"type": "string", "description": "how it makes its case: data, cases, theory, review"},
        "key_claims": {"type": "array", "minItems": 3, "maxItems": 8,
                       "items": {"type": "object", "additionalProperties": False, "required": ["claim", "anchor"],
                                 "properties": {"claim": {"type": "string"}, "anchor": ANCHOR_SCHEMA}}},
        "entities": {"type": "array", "items": {"type": "string"}, "description": "named actors: brands, firms, places, concepts, authors cited"},
        "tensions": {"type": "array", "items": {"type": "string"}, "description": "internal tensions or unresolved questions in this document"},
    },
}
CORPUS_MAP_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["shared_questions", "disagreements", "throughlines", "candidate_angles"],
    "properties": {
        "shared_questions": {"type": "array", "items": {"type": "string"}},
        "disagreements": {"type": "array", "items": {"type": "string"}, "description": "where the documents pull apart, naming which ones"},
        "throughlines": {"type": "array", "items": {"type": "string"}, "description": "ideas that run across several documents"},
        "candidate_angles": {"type": "array", "items": {"type": "string"}, "description": "3-6 angles a dossier could take, one line each"},
    },
}
RECON_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["profiles", "corpus_map"],
                "properties": {"profiles": {"type": "array", "items": PROFILE_SCHEMA}, "corpus_map": CORPUS_MAP_SCHEMA}}
PROFILES_ONLY_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["profiles"],
                        "properties": {"profiles": {"type": "array", "items": PROFILE_SCHEMA}}}

SYSTEM = """You are the reconnaissance desk of The Analyst. You read documents closely before anyone decides what to do with them.
You produce a profile per document and a map of the corpus. You never invent: every key claim carries a verbatim anchor —
a quote copied character-for-character from the named document (40-200 characters, no ellipses, no paraphrase).
A quote that is not verbatim will be rejected by a mechanical check, so copy exactly. Use the [doc_key] labels given."""


def _user_prompt(docs: list[Document], intent: str | None, map_too: bool) -> str:
    task = (
        "TASK: profile every document below (one profile per document, doc_key exactly as labeled)"
        + (" and then map the corpus as a whole (shared questions, disagreements, throughlines, candidate angles)." if map_too else ".")
    )
    intent_line = f"\nThe requester's stated intent: {intent}\n" if intent else ""
    return f"{task}{intent_line}\nDOCUMENTS ({len(docs)}):\n{documents_index(docs)}\n\n{corpus_text(docs)}"


def _verify_profiles(profiles: list[DocumentProfile], corpus: NormalizedCorpus) -> tuple[list[DocumentProfile], int]:
    dropped_total = 0
    out = []
    for p in profiles:
        kept = []
        for c in p.key_claims:
            a = verify_anchor(c.anchor, corpus)
            if a is None:
                dropped_total += 1
                continue
            kept.append(c.model_copy(update={"anchor": a}))
        out.append(p.model_copy(update={"key_claims": kept, "claims_dropped": len(p.key_claims) - len(kept)}))
    return out, dropped_total


def run_reconnaissance(job: DossierJob, docs: list[Document]) -> Reconnaissance:
    total_chars = sum(d.char_count for d in docs)
    intent = job.options.intent
    corpus = NormalizedCorpus({d.key: d.text for d in docs})

    if total_chars <= SINGLE_CALL_MAX_CHARS:
        result, _ = call_json(
            job.id, STEP, label=f"reconnaissance over {len(docs)} documents ({total_chars:,} chars)",
            system=SYSTEM, user=_user_prompt(docs, intent, map_too=True),
            tool_name="record_reconnaissance", schema=RECON_SCHEMA, model_cls=Reconnaissance, max_tokens=16000,
        )
        recon: Reconnaissance = result
    else:
        events.emit(job.id, "note", phase=STEP, detail=f"corpus is {total_chars:,} chars; profiling document by document, then mapping")
        profiles: list[DocumentProfile] = []
        for n, doc in enumerate(docs, start=1):
            if doc.char_count > PER_DOC_MAX_CHARS:
                events.emit(job.id, "note", phase=STEP,
                            detail=f"{doc.key}: {doc.char_count:,} chars exceeds the per-document cap; the profile reads the first {PER_DOC_MAX_CHARS:,} chars")
            single = doc.model_copy(update={"text": doc.text[:PER_DOC_MAX_CHARS]})
            res, _ = call_json(
                job.id, STEP, label=f"profile {n}/{len(docs)}: {doc.title[:50]}",
                system=SYSTEM, user=_user_prompt([single], intent, map_too=False),
                tool_name="record_profiles", schema=PROFILES_ONLY_SCHEMA, model_cls=None, max_tokens=8000,
            )
            for p in (res or {}).get("profiles", []):
                try:
                    profiles.append(DocumentProfile.model_validate(p))
                except Exception as exc:
                    logger.warning(f"profile for {doc.key} rejected: {exc}")
        interim = Reconnaissance(profiles=profiles, corpus_map=CorpusMap())
        cm, _ = call_json(
            job.id, STEP, label="corpus map over profiles", system=SYSTEM,
            user="TASK: map this corpus from the profiles (shared questions, disagreements, throughlines, candidate angles).\n\n"
                 + compact_profiles(interim),
            tool_name="record_corpus_map", schema=CORPUS_MAP_SCHEMA, model_cls=CorpusMap, max_tokens=4000,
        )
        recon = Reconnaissance(profiles=profiles, corpus_map=cm)

    # Fill titles from the documents when the model left them thin; keep doc order.
    by_key = {d.key: d for d in docs}
    fixed = []
    for p in recon.profiles:
        if p.doc_key in by_key and not p.title:
            p.title = by_key[p.doc_key].title
        fixed.append(p)
    recon.profiles = fixed

    verified, dropped = _verify_profiles(recon.profiles, corpus)
    recon.profiles = verified
    kept = sum(len(p.key_claims) for p in verified)
    events.emit(job.id, "note", phase=STEP,
                detail=f"anchor wall: {kept} key claims verified verbatim, {dropped} dropped",
                payload_json={"claims_verified": kept, "claims_dropped": dropped})
    events.emit(job.id, "artifact", phase=STEP, detail=f"{len(recon.profiles)} document profiles + corpus map",
                payload_json={"kind": "profiles", "profiles": [p.doc_key for p in recon.profiles],
                              "candidate_angles": recon.corpus_map.candidate_angles})
    return recon
