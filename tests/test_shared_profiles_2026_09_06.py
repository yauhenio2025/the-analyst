"""The shared work profile (2026-09-06): a `role: profile` source carries the Stacks' WorkProfile (plus a verified
anchor per claim); the reconnaissance desk starts from it and its claims go through the anchor wall; the desk emits
the same shape back."""
import json

from src.dossier import reconnaissance
from src.dossier.schemas import Anchor, CorpusMap, DocumentProfile, DossierJob, KeyClaim, Reconnaissance
from src.sources.profiles import SharedWorkProfile, match_profiles, parse_profiles, profile_documents, to_document_profile, to_shared
from src.sources.resolve import resolve_sources
from src.sources.schemas import Document, SourceSpec

TEXT = ("Political society is reducible neither to interests in civil society, nor to the state. "
        "The argument proceeds by comparison of Italy and Spain. Weber's definition of power is too agentic.")

STACKS_PROFILE = {
    "uid": "em:BEFGGK6M", "title": "Privilege and Property",
    "profile": {
        "thesis": "Political society is irreducible to civil society and to the state.",
        "question": "Why did class formation fail in Austrian Lombardy?",
        "contribution": "history", "tradition": "historical sociology",
        "concepts": [{"term": "political society", "weight": 5, "locus": "[p. 1 | PDF p. 1]"}],
        "people": [{"name": "Weber, Max", "role": "builds-on", "stance": "adopts the class/status/party distinction"}],
        "claims": [
            {"claim": "Political society is irreducible.", "kind": "thesis", "locus": "[PDF p. 1]"},
            {"claim": "Weber's definition of power is too agentic.", "kind": "polemic", "locus": "[PDF p. 9]",
             "anchor": "Weber's definition of power is too agentic."},
            {"claim": "A claim the text never states.", "kind": "finding", "locus": "[PDF p. 3]", "anchor": "words that are not in the text at all"},
        ],
        "positions": [{"debate": "state autonomy", "side": "relational", "against": ["Skocpol"]}],
        "passages": [{"quote": "Political society is reducible neither to interests in civil society, nor to the state.",
                      "locus": "[PDF p. 1]", "why": "thesis", "verified": "exact"}],
        "keywords": ["Lombardy"],
    },
    "model": "openai/gpt-5.6-luna",
}


def _doc(key, text, **kw):
    return Document(key=key, title=kw.pop("title", f"Title {key}"), text=text, char_count=len(text), **kw)


def test_parse_accepts_the_stacks_stored_form_a_list_a_map_and_a_bare_profile():
    one = parse_profiles(json.dumps(STACKS_PROFILE))
    assert len(one) == 1 and one[0].uid == "em:BEFGGK6M" and one[0].model == "openai/gpt-5.6-luna" and len(one[0].claims) == 3
    assert [p.uid for p in parse_profiles(json.dumps([STACKS_PROFILE, {"uid": "em:X", "thesis": "t"}]))] == ["em:BEFGGK6M", "em:X"]
    assert [p.uid for p in parse_profiles(json.dumps({"em:Y": {"thesis": "t"}, "em:Z": {"profile": {"thesis": "u"}}}))] == ["em:Y", "em:Z"]
    assert parse_profiles(json.dumps({"profiles": [{"thesis": "bare"}]}))[0].thesis == "bare"
    assert parse_profiles("not json") == [] and parse_profiles(json.dumps({"author": "x"})) == []


def test_profiles_match_documents_by_uid_stacks_key_or_title_once_each():
    profiles = parse_profiles(json.dumps([STACKS_PROFILE, {"uid": "em:OTHER", "thesis": "t", "title": "The Other Paper"}]))
    docs = [_doc("privilege-and-property", TEXT, stacks_key="BEFGGK6M"),        # stacks key without the prefix
            _doc("d2", "x", title="The other paper!"),                              # title, case and punctuation folded
            _doc("d3", "y", title="Privilege and Property")]                        # same title again: the profile is spent
    m = match_profiles(profiles, docs)
    assert set(m) == {"privilege-and-property", "d2"} and m["privilege-and-property"].uid == "em:BEFGGK6M"
    assert match_profiles(profiles, [_doc("em:OTHER", "z")])["em:OTHER"].uid == "em:OTHER"


def test_to_document_profile_borrows_the_passage_at_the_claims_locus_and_keeps_explicit_anchors():
    p = parse_profiles(json.dumps(STACKS_PROFILE))[0]
    dp = to_document_profile(p, _doc("k", TEXT))
    assert dp.doc_key == "k" and dp.genre == "history" and dp.one_line.startswith("Why did class formation fail")
    assert [c.anchor.quote[:20] for c in dp.key_claims] == ["Political society is", "Weber's definition o", "words that are not i"]
    assert "Weber, Max" in dp.entities and "political society" in dp.entities
    assert dp.tensions == ["state autonomy: relational (against Skocpol)"]


def test_reconnaissance_starts_from_a_supplied_profile_and_walls_its_claims(monkeypatch):
    monkeypatch.setattr(reconnaissance.events, "emit", lambda *a, **k: None)
    monkeypatch.setattr(reconnaissance, "documents_index", lambda docs: " ".join(f"[{d.key}]" for d in docs))
    monkeypatch.setattr(reconnaissance, "corpus_text", lambda docs, max_chars_per_doc=None: "")
    calls = []

    def call_json(job_id, step, *, label, system, user, tool_name, schema, model_cls, max_tokens):
        calls.append(label)
        if tool_name == "record_profiles":
            key = user.split("[")[1].split("]")[0]
            return {"profiles": [{"doc_key": key, "title": "", "genre": "g", "one_line": "o", "thesis": "t", "method": "m",
                                  "key_claims": [], "entities": [], "tensions": []}]}, None
        return CorpusMap(candidate_angles=["a"]), None
    monkeypatch.setattr(reconnaissance, "call_json", call_json)
    docs = [_doc("em:BEFGGK6M", TEXT), _doc("B", "beta text")]
    context = [Document(key="profiles", title="profiles", role="profile", text=json.dumps([STACKS_PROFILE]))]
    recon = reconnaissance.run_reconnaissance(DossierJob(), docs, persist=lambda **f: None, context_documents=context)
    assert [c for c in calls if c.startswith("profile")] == ["profile 2/2: Title B"]     # the profiled document was not read
    assert [p.doc_key for p in recon.profiles] == ["em:BEFGGK6M", "B"]
    first = recon.profiles[0]
    assert first.thesis.startswith("Political society is irreducible") and first.claims_dropped == 1   # the invented anchor fell
    assert [c.anchor.verified for c in first.key_claims] == [True, True]
    # without profiles the small corpus still takes the single call
    calls.clear()
    monkeypatch.setattr(reconnaissance, "call_json", lambda *a, **k: (Reconnaissance(profiles=[DocumentProfile(doc_key="B")]), None))
    reconnaissance.run_reconnaissance(DossierJob(), [docs[1]], persist=lambda **f: None)


def test_the_desk_emits_the_shared_shape_with_verified_anchors():
    dp = DocumentProfile(doc_key="k", title="T", genre="empirical study", one_line="o", thesis="th", method="cases",
                         key_claims=[KeyClaim(claim="c1", anchor=Anchor(doc_key="k", quote="q1", verified=True)),
                                     KeyClaim(claim="c2", anchor=Anchor(doc_key="k", quote="q2", verified=True, trimmed=True))],
                         entities=["Weber, Max"], tensions=["a tension"])
    shared = to_shared(dp, {"key": "k", "stacks_key": "em:K", "title": "T"})
    assert shared.uid == "em:K" and shared.origin == "analyst" and shared.contribution == "empirical"
    assert [(c.claim, c.anchor, c.anchor_verified) for c in shared.claims] == [("c1", "q1", "exact"), ("c2", "q2", "partial")]
    assert shared.verification.model_dump() == {"passages": 2, "exact": 1, "partial": 1, "no": 0, "version": "analyst-2026-09-06"}
    assert shared.keywords == ["Weber, Max"] and shared.relations[0].relation == "tension"
    # and it parses back as a profile the desk can start from
    back = parse_profiles(shared.model_dump_json())
    assert back and back[0].claims[0].anchor == "q1"


def test_a_profile_source_resolves_as_a_context_document():
    specs = [SourceSpec(kind="paste", title="Paper", text=TEXT),
             SourceSpec(kind="paste", role="profile", title="profiles", text=json.dumps([STACKS_PROFILE]))]
    docs = resolve_sources(specs)
    assert [d.role for d in docs] == ["source", "profile"]
    assert [p.uid for p in profile_documents(docs)] == ["em:BEFGGK6M"]
