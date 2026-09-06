"""Citation family: preserve the Stacks questions as explicit corpus processes."""
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "communications/study/citation_family_2026_09_06"
PREDICATE = (" Select literal spans that carry the actor, predicate, object and necessary qualification. "
    "A name or topic alone cannot support a reading. Use separate anchor-b/doc-b for a second span; "
    "never stitch quotations. Keep attribution, negation, modality, edition and chronology. "
    "Re-anchor, narrow or reject a claim whose quotation omits its predicate. Code checks only anchors and IDs; "
    "the model must judge the reading against the supplied text.")
LOCAL = ' — anchor: "<verbatim supporting clause, <=200 chars>" — doc: <actual supplied source key> — confidence: high|medium|low'
PAIR = ' — anchor: "<verbatim clause from A, <=200 chars>" — doc: <A source key> — anchor-b: "<verbatim clause from W or reader B, <=200 chars>" — doc-b: <different actual supplied source key> — confidence: high|medium|low'
COMMON = ("Use the supplied author/person identities and source roles. If a document is an evidence index, "
    "treat its routing, locations and counts as metadata; its duplicated quotations do not create an independent "
    "source. Anchor substantive claims in the actual citing text, held primary window or secondary text. "
    "Keep coauthorship and nested quotations. Read the body, not just titles, bibliographies or headers. "
    "A document outside a dimension's role gets no positive row in that dimension. Report that scope explicitly. "
    "Do not turn an incomplete check into a source's silence. The held sample is not the author's complete work "
    "or the thinker's entire reception. Dates missing from metadata stay unknown unless stated in the source.")


def dim(key, name, question, fields, card, signals, scope="document", load=True):
    return dict(key=key, name=name, questions=[question], fields=fields, method_card="Do: " + card + PREDICATE,
                indicators=signals, scope=scope, load_bearing=load)


def designs():
    return {
        "ENG": dict(key="citation_engagement_map", name="Engagement with a thinker across texts",
            map_contract="G5 companion, not a revision of citation_invocation_map v2",
            seeds=["DOC_SYSTEM", "ACROSS_SYSTEM"],
            question="How does this author use and read this thinker across the supplied citing texts?",
            ideal="A bibliographic reading of A on P, led by P's place in these arguments. Give a passage × cited object × move × stance × reading × locus table, then a text/year trajectory table. Distinguish evidence, foil and dialogue; pair the actual passages before claiming development. Give a scholar three to five passages to open first and say why.",
            tables=["passage_move_stance_locus", "trajectory_by_text_and_year"],
            dims=[
                dim("place_in_text", "The thinker's place in this argument", "What does this text argue, and what place does the named thinker have in that argument?", "text-argument: <claim> — place: <evidence, adopted framework, opponent, courtesy or qualified role>", "Read the whole citing text for its argument and P's role. A quoted reader's position is not automatically A's. On a secondary or primary-work document report outside scope.", ["argument", "framework", "however"]),
                dim("cited_object", "What each passage cites", "For each supplied passage, what work, idea or named thinker is cited, and at what locus?", "ref: <index ref or local passage ID> — cited: <work or idea> — locus: <printed/PDF page; cited locus if present> — access: <held window or unknown>", "Copy the cited identity and locus from the passage and bibliography. Record mentions without works. Separate a secondary reader's report of P from a direct citation of P. Never supply a work from memory.", ["Weber", "cites", "p."]),
                dim("citation_move", "The move made with the citation", "What does the author do with the thinker at each passage: authority, evidence, foil, dialogue, genealogy, illustration, courtesy, or self-positioning?", "ref: <passage ID> — move: authority|evidence|foil|dialogue|genealogy|illustration|courtesy|self-positioning — supports: <local claim>", "Classify the argumentative act, keeping the premise or contrast that makes the label true. The same cited work can serve different moves in different passages.", ["following", "against", "as an example"]),
                dim("citation_stance", "The stance toward what is cited", "At each passage does the author adopt, build on, qualify, dispute or merely mention the cited position?", "ref: <passage ID> — stance: adopts|builds_on|qualifies|disputes|mentions — object: <exact proposition>", "Classify stance toward a proposition, not toward the person globally. Adoption in one respect and dispute in another are separate findings. Preserve a report of another reader's stance as a report.", ["adapting", "rather different", "as noted"]),
                dim("passage_reading", "What the citation accomplishes here", "Which claim, evidence or distinction does the author advance with the thinker here, and what qualification limits that reading?", "ref: <passage ID> — reading: <specific interpretive move> — qualification: <limit>", "Explain two to four sentences of the local move using the source's distinctions. Do not certify what P actually wrote unless the primary window has separately been checked. Cover secondary uses as well as headline concepts.", ["distinction", "because", "in this sense"], load=False),
                dim("engagement_trajectory", "P's place across A's supplied work", "How does the thinker's role persist or change across the author's supplied texts, and which dated paired passages establish that trajectory?", "texts-years: <A1/year; A2/year> — relation: <continuity, change, contrast or unordered> — reading: <aligned role> — coverage: <texts actually supporting it>", "Align the same cited idea and argumentative role in two citing texts before assigning a trajectory. Coauthored works remain coauthored. Input order or same-year publication proves no sequence. Mere omission is neither abandonment nor concealment. State precisely what the inspected texts support.", ["earlier", "adapting", "paired formulations"], scope="corpus", load=False),
            ]),
        "G6": dict(key="citation_fidelity_audit", name="Citation fidelity audit",
            map_contract="G6", seeds=["ACCURACY_SYSTEM", "ACROSS_SYSTEM"],
            question="Does each attribution hold against the supplied page window of the work it cites?",
            ideal="A paired audit of the evidence index: for every indexed attribution, A's actual claim and anchor beside P's own words and anchor, attribution kind, accurate/fair/selective/stretched/misattributed/unverifiable verdict with a reason, and edition/locus notes. State how many pairs and works were checked, unresolved and outside the sample. A practice conclusion applies only to the checked sample.",
            tables=["paired_citation_fidelity", "checked_sample_coverage"],
            dims=[
                dim("attribution_kind", "Who attributes what to whom", "Does A directly attribute a claim to P, report P reporting another view, contrast P with another, or merely name P?", "pair-ref: <index ID> — attribution: direct|reported|contrast|none — voice-chain: <A to P to reported speaker, if any>", "Work from the A side of each indexed pair. Preserve nested attribution. A mere mention makes no substantive attribution to audit. In a W-only document defer A-side conclusions until the paired comparison.", ["according to", "reports", "in contrast"]),
                dim("attributed_claim", "A's actual attribution", "What exactly does A attribute at this citation, in A's own terms and with A's qualification?", "pair-ref: <index ID> — a-attributes: <one proposition> — cited-work-locus: <literal citation>", "Copy the supporting A clause; retain quotation versus paraphrase and creative adaptation versus a claim to literal fidelity. In a footnote pair, read the body sentence to which the note belongs. Do not use an index's generated description as A's words.", ["writes", "adapting", "termed"]),
                dim("source_position", "P's own position at the retrieved place", "What does P say in the held page window, and whose voice is speaking there?", "pair-ref: <index ID> — p-says: <position in two to three sentences> — voice: <P, editor, translator, quoted other or unresolved> — held-locus: <printed/PDF pages>", "Read only the W side. Copy P's own words verbatim. A translator's introduction, editorial note, table of contents or quoted opponent is not P's assertion. If nothing here settles the attribution, report that limit rather than recalling P's work.", ["therefore", "however", "by this we mean"]),
                dim("source_context", "Qualifications around the cited words", "Which surrounding distinction or qualification affects the weight of the words A invokes?", "pair-ref: <index ID> — qualification: <source-side limit> — bearing: <what comparison must retain>", "Read the whole retrieved window, including neighboring pages. True words may be selective if their argumentative weight is reversed. Record the limiting clause before judging a discrepancy; an unrelated retrieval proves no misattribution.", ["only", "on the other hand", "not"]),
                dim("edition_locus", "Edition and retrieval limits", "Which edition, printed page, PDF page and retrieval method are actually supplied, and what remains unresolved?", "pair-ref: <index ID> — edition: <held/cited> — how: page|search|unheld|unresolved — locus: <mapped printed/PDF pages> — limitation: <uncertainty>", "Read the evidence index as provenance. Separate PDF index from printed page. A term-overlap match is a candidate window, not confirmation of locus or edition equivalence. State missing works and missing locations without treating them as P's silence.", ["how: search", "edition", "PDF p."], load=False),
                dim("paired_fidelity", "Verdict on each supplied pair", "Does A's attribution hold against P's own words in this retrieved window: accurate, fair, selective, stretched, misattributed or unverifiable, and why?", "pair-ref: <index ID> — attribution: direct|reported|contrast|none — a-attributes: <claim> — p-says: <position> — verdict: accurate|fair|selective|stretched|misattributed|unverifiable — reason: <specific warrant> — edition-locus: <limit>", "Pair an anchor from the actual A text with anchor-b from the actual W window, using distinct supplied document keys. These are corpus rows because the verdict predicates a relation between two sources, even though the unit is one citation. Stretched or misattributed requires P's own contrary words; otherwise say unverifiable. Search-window irrelevance warrants unverifiable, not misattributed. Keep every index ID accounted for in the audit table, even when no positive verdict is possible.", ["paired attribution", "what P says", "retrieved window"], scope="corpus", load=False),
                dim("sample_practice", "Practice across the checked sample", "What pattern holds across the checked attributions, with precisely what pair and work coverage?", "sample: <checked/eligible/unresolved pairs; held/cited works> — pattern: <bounded finding> — exceptions: <paired evidence> — coverage: <explicit limit>", "Count checked pair IDs once; do not count multiple findings or overlapping windows as independent citations. Use supplied coverage counts and distinguish eligible, retrieved, assessed and settled. Anchor pattern claims in actual A and W sources. Never generalise to A's citation practice beyond this checked sample.", ["checked sample", "unresolved", "edition difference"], scope="corpus", load=False),
            ]),
        "G8": dict(key="citation_reception_map", name="Reception among a thinker's readers",
            map_contract="G8", seeds=["RECEPTION_SYSTEM", "ACROSS_SYSTEM"],
            question="Where does this author's reading sit among the supplied readers of this thinker?",
            ideal="A reader × theme × position table with the argument and stance of each secondary text, anchored in its own words, plus A among P's readers: consonance, explicit opposition, or no demonstrated engagement. Preserve dates, scope and excerpts. Separate counted uncited readers from inferred affinities; if citation counts are absent, no most-cited ranking can be made.",
            tables=["reader_theme_position", "author_among_readers"],
            dims=[
                dim("reader_argument", "Each reader's argument about P", "What does this secondary text argue about the thinker, and what problem is that reading meant to answer?", "reader-text-year: <identity/date> — argument: <specific thesis> — role: <secondary reader or A reference point>", "Read each held secondary text on its own terms. For A's text, record a reference reading, not a second member of the reception sample. Primary windows and indexes are not secondary readers.", ["argue", "interpretation", "reconstruction"]),
                dim("reader_stance", "Each reader's stance", "Does this reader defend, reconstruct, criticize, apply or survey P, and toward which proposition?", "reader: <identity> — stance: defends|reconstructs|criticizes|applies|surveys — object: <proposition>", "Anchor stance in what the text does with the position. A critical book can defend a particular distinction. A survey's reports are not automatically its own endorsements.", ["against", "reconstruct", "use"]),
                dim("theme_position", "Positions on the engagement's themes", "For each theme A's engagement turns on, how does this reader interpret P and what passage supports that position?", "reader: <identity> — theme: <theme grounded in A or supplied engagement themes> — position: <specific interpretation>", "Use themes supplied with the corpus or established by A's citing passages. Preserve each reader's terms and qualifications. Skip themes the text does not address; a bounded excerpt cannot establish book-wide absence. On A's documents record the reference position for later pairing.", ["class", "closure", "political capitalism", "meaning"]),
                dim("cites_author", "Documented engagement with A", "Does the supplied secondary text name or cite A, and what exactly does it do with that citation?", "reader: <identity> — cites-A: yes|not-found-in-inspected-text|unresolved — author-note: <named engagement or search scope>", "A positive citation needs A's name in this reader's text. A shared theme is not a citation. Record negative searches only with their inspection bounds; no quotation proves global absence. A's own text is outside this dimension.", ["Riley", "citation", "reference"], load=False),
                dim("reception_scope", "Dates, excerpts and count authority", "What date, excerpt coverage and supplied citation counts delimit this reader's relevance to A?", "reader: <identity> — year: <stated or unknown> — inspected: <full article or bounded book excerpt> — count-basis: <supplied count record or absent>", "Keep composition, translation and publication dates distinct. Do not make a later reader someone A failed to engage. Citation counts identify most-cited readers only when a supplied count table says so; name-overlap counts in a local sample are not scholarly citation counts.", ["published", "excerpt", "citation count"], load=False),
                dim("among_readers", "A's place among the supplied readers", "Which readings is A consonant with, explicitly opposed to, or not demonstrably engaging, on aligned themes and dates?", "A-text-year: <identity/date> — reader-text-year: <identity/date> — theme: <aligned question> — relation: consonant|explicit-opposition|interpretive-contrast|no-demonstrated-engagement — engagement-basis: <citation or bounded count/search> — limit: <coverage>", "Pair A's reading and the secondary reader's own words from distinct documents. Consonance is an analytical comparison, not evidence of influence. Distinguish explicit criticism from an analyst's contrast. An earlier date permits possible engagement but proves none. Any most-cited uncited list must come exclusively from supplied counts with coverage and date eligibility; when counts are absent state unavailable.", ["paired theme positions", "cites A", "chronology"], scope="corpus", load=False),
            ]),
    }


def build():
    result = designs()
    for ident, d in result.items():
        for i, dimension in enumerate(d.pop("dims"), 1):
            prefix = ("X" if dimension["scope"] == "corpus" else "D") + str(i)
            dimension["id_prefix"] = prefix
            dimension["answer_shape"] = f'[{prefix}.F<n>] <one scoped finding> — dim: {dimension["key"]} — ' + dimension.pop("fields") + (PAIR if dimension["scope"] == "corpus" else LOCAL)
            d.setdefault("dimensions", []).append(dimension)
        brief = "1. " + d["ideal"] + "\n2. Give the source-specific reading with qualifications, then render the named Markdown tables. Every positive cell cites its final supporting finding ID; unknown cells state the actual limit.\n3. Preserve granular evidence through reconciliation: inspect each final table cell against its cited final row and source context. Renumber citations with rows; no old ID may silently acquire a new meaning. Count passage/pair IDs, not findings, for coverage.\n4. Give a short read-first route and the unsettled question. No claim of exhaustive coverage without a complete supplied inventory and actual inspection. " + COMMON + PREDICATE
        d["process"] = dict(key="dvs", description=d["question"], framing=d["ideal"] + " " + COMMON,
            scoped_outcomes=True, routing={"cheap":"openrouter/openai/gpt-5.6-luna", "mid":"openrouter/deepseek/deepseek-v4-pro", "strong":"openrouter/openai/gpt-5.6-sol"},
            dimensions=d["dimensions"], steps=[
                dict(key="extract",kind="extract",parallel_over="dimension_x_document",model_tier="cheap",output="ledger",max_rows=12),
                dict(key="verify",kind="verify",consumes=["extract"],model_tier="mid",output="ledger",duties=["check_anchors_in_context","merge_duplicates","hunt_misses","name_must_keep",COMMON,PREDICATE,"Check every passage/pair against its actual source role and preserve both keys for relational claims. Verify table meanings, voice and edition uncertainty; a search hit is not a confirmed cited page."]),
                dict(key="synthesize",kind="synthesize",consumes=["verify"],model_tier="strong",output="prose_ledger",is_final=True,reader="a scholar of A with the cited works and secondary texts open",tables=d["tables"],brief=brief)])
        cap = dict(engine_key=d["key"],engine_name=d["name"],version=1,category="scholarly",kind="comparison",
            problematique=d["ideal"],researcher_question=d["question"],intellectual_lineage={"primary":"source_criticism"},
            analytical_dimensions=[dict(key=x["key"],description=x["name"],probing_questions=x["questions"]) for x in d["dimensions"] if x["scope"]=="document"], apps=["critic"],function="genealogy",family="analytical")
        op = dict(engine_key=d["key"],engine_name=d["name"],stance_operationalizations=[],depth_sequences=[dict(depth_key=k,mode=m) for k,m in [("surface","oneshot"),("standard","oneshot_checked"),("deep","dvs")]]+[dict(depth_key="dvs",process="dvs")],process=d["process"])
        for folder,obj in [("engines/capability_definitions",cap),("operationalizations/definitions",op)]:
            p=ROOT/f'src/{folder}/{d["key"]}.yaml'
            if p.exists():
                raise RuntimeError(f"Refusing to replace existing engine: {p}")
            p.write_text("# Citation family: Stacks prompts preserved in the study seed archive.\n"+yaml.safe_dump(obj,sort_keys=False,allow_unicode=True,width=110))
        d["inventory"]=True
    ARCHIVE.mkdir(parents=True,exist_ok=True)
    (ARCHIVE/"designs.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    p=ROOT/"src/dossier/catalog_purpose.json";cat=json.loads(p.read_text())
    for d in result.values():
        cat["excluded"].append(dict(engine_key=d["key"],why="Citation family research definition; withheld pending source-read validation."))
    p.write_text(json.dumps(cat,indent=2,ensure_ascii=False)+"\n")


if __name__=="__main__":
    build()
