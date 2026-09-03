"""Shared helpers for the dossier steps: documents, corpus text, engine catalog, depth policy."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Optional

from src.dossier.schemas import DossierJob
from src.sources.schemas import Document

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[2]
DOSSIER_DIR = Path(os.environ.get("DOSSIER_DIR", str(REPO_ROOT / "data" / "dossiers")))

# Depth policy (the contract): simple = 1 engine × 1 pass; medium = 2-3 engines chained;
# advanced = 3-4 engines + a synthesis pass.
DEPTH_POLICY: dict[str, dict[str, Any]] = {
    "simple": {"min_engines": 1, "max_engines": 1, "engine_depth": "surface", "max_passes": 1, "synthesis": False},
    "medium": {"min_engines": 2, "max_engines": 3, "engine_depth": "surface", "max_passes": 4, "synthesis": False},
    "advanced": {"min_engines": 3, "max_engines": 4, "engine_depth": "standard", "max_passes": 10, "synthesis": True},
}
SYNTHESIS_ENGINES = ("deep_summarization", "concept_synthesis", "theory_construction_analyzer",
                     "genealogy_final_synthesis", "aoi_thematic_synthesis")

AUDIENCE_REGISTER = {
    "executive": ("Executives of a luxury fashion house. Plain language, no theory jargon, "
                  "decisions and implications first, every claim anchored in the documents. "
                  "Never lecture; show what the material says and what it means for them."),
    "researcher": ("Researchers. Precise, methodologically explicit, cite the documents exactly, "
                   "surface disagreements and open questions."),
    "analyst": ("Professional analysts. Structured, evidence-forward, explicit about confidence "
                "and about what the documents do not show."),
}


def job_dir(job_id: str) -> Path:
    p = DOSSIER_DIR / job_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_documents(job: DossierJob) -> list[Document]:
    """Documents with text, re-read from the executor document store (resumable, no re-fetch)."""
    from src.executor.document_store import get_document_text

    docs: list[Document] = []
    for meta in job.documents:
        text = ""
        doc_id = meta.get("executor_doc_id")
        if doc_id:
            text = get_document_text(doc_id) or ""
        if not text:
            logger.warning(f"document {meta.get('key')} has no stored text (doc_id={doc_id})")
        docs.append(Document(
            key=meta.get("key", "doc"), title=meta.get("title", ""), creators=meta.get("creators", ""),
            year=meta.get("year", ""), publication=meta.get("publication", ""), library=meta.get("library", ""),
            stacks_key=meta.get("stacks_key", ""), text=text, char_count=len(text),
        ))
    return docs


def doc_header(doc: Document, n: int, total: int) -> str:
    bits = [f"[{doc.key}]", f"[{n}/{total}]", doc.label()]
    if doc.publication:
        bits.append(f"— {doc.publication}")
    return " ".join(bits)


def corpus_text(docs: list[Document], max_chars_per_doc: Optional[int] = None) -> str:
    """The documents as one labeled text. doc_key labels are what anchors cite."""
    parts = []
    total = len(docs)
    for n, doc in enumerate(docs, start=1):
        text = doc.text
        if max_chars_per_doc and len(text) > max_chars_per_doc:
            text = text[:max_chars_per_doc] + f"\n\n[… truncated at {max_chars_per_doc:,} chars of {len(doc.text):,} …]"
        parts.append(f"===== DOCUMENT {doc_header(doc, n, total)} =====\n\n{text}")
    return "\n\n\n".join(parts)


def corpus_title(docs: list[Document], intent: Optional[str] = None) -> str:
    if intent:
        return intent.strip()[:120]
    if len(docs) == 1:
        return docs[0].title[:120]
    return f"{docs[0].title[:70]} (+{len(docs) - 1} documents)"


def documents_index(docs: list[Document]) -> str:
    lines = []
    for n, doc in enumerate(docs, start=1):
        lines.append(f"- {doc_header(doc, n, len(docs))} — {doc.char_count:,} chars")
    return "\n".join(lines)


# Executable engines that presume a workflow-specific structure (a selected source
# thinker, prior works) and cannot be run over a plain corpus.
EXCLUDED_PREFIXES = ("aoi_", "genealogy_")


def engine_catalog(for_dossier: bool = True) -> list[dict]:
    """The EXECUTABLE engines (capability YAML present), enumerated at runtime."""
    from src.engines.registry import get_engine_registry

    reg = get_engine_registry()
    out = []
    for cap in reg.list_capability_definitions():
        if for_dossier and cap.engine_key.startswith(EXCLUDED_PREFIXES):
            continue
        depths = {}
        for dl in getattr(cap, "depth_levels", []) or []:
            depths[dl.key] = {"passes": int(getattr(dl, "typical_passes", 1) or 1),
                              "description": (dl.description or "")[:220]}
        out.append({
            "engine_key": cap.engine_key,
            "engine_name": cap.engine_name,
            "category": str(getattr(cap.category, "value", cap.category)),
            "kind": str(getattr(cap.kind, "value", cap.kind)),
            "researcher_question": (getattr(cap, "researcher_question", "") or "")[:300],
            "problematique": (getattr(cap, "problematique", "") or "")[:500],
            "depths": depths,
        })
    out.sort(key=lambda e: e["engine_key"])
    return out


def catalog_text(catalog: list[dict], with_problematique: bool = False) -> str:
    lines = []
    for e in catalog:
        passes = ", ".join(f"{k}={v['passes']}p" for k, v in e["depths"].items())
        lines.append(f"- {e['engine_key']} — {e['engine_name']} [{e['category']}] ({passes})\n"
                     f"  asks: {e['researcher_question']}")
        if with_problematique:
            lines.append(f"  about: {e['problematique'][:300]}")
    return "\n".join(lines)


def passes_for(catalog_entry: dict, depth_key: str) -> int:
    depths = catalog_entry.get("depths") or {}
    if depth_key in depths:
        return int(depths[depth_key]["passes"])
    return 1


def estimate_engine_run(corpus_chars: int, passes: int, model: str = "claude-sonnet-4-6") -> tuple[float, float]:
    """(cost_usd, minutes) for `passes` engine calls over the corpus — code arithmetic, not judgment."""
    from src.dossier.receipts import llm_cost

    in_tokens = corpus_chars // 4 + 6_000  # system prompt overhead
    out_tokens = 6_000
    per_pass = llm_cost(model, in_tokens, out_tokens) or 0.0
    # ~40 tok/s sync output plus ~30 s of input processing per call
    minutes_per_pass = (out_tokens / 40 + 30 + in_tokens / 8000) / 60
    return round(per_pass * passes, 3), round(minutes_per_pass * passes, 1)


def compact_profiles(recon: Any) -> str:
    """Profiles as compact text for downstream prompts (anchors kept — they are reusable quotes)."""
    if recon is None:
        return "(no reconnaissance)"
    lines = []
    for p in recon.profiles:
        lines.append(f"## [{p.doc_key}] {p.title}\n- genre: {p.genre}\n- one line: {p.one_line}\n- thesis: {p.thesis}\n- method: {p.method}")
        if p.key_claims:
            lines.append("- key claims (with verbatim anchors):")
            for c in p.key_claims:
                lines.append(f"  • {c.claim}  ⟶ [{c.anchor.doc_key}] “{c.anchor.quote}”")
        if p.entities:
            lines.append(f"- entities: {', '.join(p.entities[:20])}")
        if p.tensions:
            lines.append("- tensions: " + " | ".join(p.tensions[:8]))
    cm = recon.corpus_map
    lines.append("## Corpus map")
    lines.append("- shared questions: " + " | ".join(cm.shared_questions))
    lines.append("- disagreements: " + " | ".join(cm.disagreements))
    lines.append("- throughlines: " + " | ".join(cm.throughlines))
    lines.append("- candidate angles: " + " | ".join(cm.candidate_angles))
    return "\n".join(lines)


def analysis_prose(job: DossierJob, max_chars_per_phase: int = 80_000) -> str:
    parts = []
    for pn in sorted(job.analysis.keys(), key=lambda k: float(k)):
        ph = job.analysis[pn]
        text = ph.get("final_output") or ""
        if len(text) > max_chars_per_phase:
            text = text[:max_chars_per_phase] + "\n\n[… truncated for the next step …]"
        parts.append(f"### Analysis phase {pn} — {ph.get('engine_name') or ph.get('engine_key')}\n\n{text}")
    return "\n\n---\n\n".join(parts) if parts else "(no analysis prose)"
