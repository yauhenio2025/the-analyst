"""Build deferred patches from a committed revision; never write their targets.

Run with --base <main HEAD>. YAML edits replace scalar spans so unrelated cards
and questions retain their original bytes. Requires the existing PyYAML package.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import textwrap

import yaml

ROOT = Path(__file__).resolve().parents[3]
DEST = Path(__file__).resolve().parent / 'patches'

RENDITION = (
    "Do: Prefer the supplied Stacks markers=1 rendition of the same identified work and edition. "
    "Use the actual supplied bytes and document key; a card cannot fetch or replace a rendition. "
    "When unavailable, retain the supplied pdftotext window and label that fallback. Keep rendition identity, "
    "printed page and PDF page distinct, and preserve the works-registry section UID/title and edition "
    "where supplied. A section is a locus, not an inferred page mapping. Never infer edition equivalence "
    "from equal page numbers, invent a section title, correct OCR inside a quotation, or supply words from memory. "
    "A replacement rendition requires a new source snapshot and anchor checks; overlapping renditions remain one citation event."
)
INVENTORY = (
    "Do: Render verified_passage_inventory from the applied, wall-checked passage ledger, including retained "
    "passages not selected for the short narrative. Columns: canonical passage/event ID | A text and year "
    "(unknown when absent) | cited work/idea | move | stance toward the named proposition | bounded reading "
    "and qualification | final ledger IDs | exact carried anchors | original document keys | rendition, "
    "edition, printed/PDF pages and supplied section UID/title. Join dimension rows only by their explicit "
    "passage/event mapping, never by adjacency or topic. Preserve separate propositions and witnesses. "
    "Count canonical passages once across dimensions, overlapping windows, renditions and memo restatements; "
    "report eligible/inspected/retained/rejected/unresolved counts separately. Each positive cell must resolve "
    "to a retained verified ledger row with its unchanged meaning after reconciliation. Keep granular rows "
    "addressable in the final ledger/sidecar even when narrative findings are compressed. Rejected, superseded "
    "or anchor-failed rows go in a separate coverage report and cannot support inventory cells. If the full "
    "applied ledger or event mapping is unavailable, label the inventory partial and list missing inputs; "
    "never reconstruct omitted rows from a memo or call a narrative subset the full verified ledger. "
    "A restatement links its canonical row and is never filed or counted twice."
)
RECEPTION = (
    "Do: Carry role: reader|reference_point in reader rows and the reader_theme_position table. A's supplied "
    "texts are reference_point rows, retained for comparison and excluded from counts of secondary readers; "
    "deduplicate secondary readers by supplied person identity and report reader and text totals separately. "
    "Keep theme-origin plan_spine|reader_addition, dates and excerpt limits. An A-to-reader claim of never "
    "engages requires an explicit zero in the supplied Stacks citation ledger, with ledger row ID, snapshot, "
    "checked A texts/date range, citation-event unit and resolved identities/aliases. Report only not engaged "
    "in that checked corpus; an absent count or bounded reception excerpt is unknown, not zero. The reverse "
    "reader-to-A citation in cites_author cannot establish A-to-reader engagement. A most-cited uncited list "
    "also requires a separate supplied ranking/count basis and date eligibility; no local mention frequency "
    "ranking. Cite the literal metadata row for a count/zero and actual source passages for interpretations; "
    "metadata is not a substantive witness. Preserve count direction and authority in the final tables."
)
FIDELITY = (
    "Do: Preserve the supplied work identity, cited/held editions, rendition identity, section UID/title "
    "and printed/PDF pages in each audit row and final paired_citation_fidelity cell. Keep how: "
    "page|section|search as the actual retrieval method only when retrieved; a registry title does not change "
    "how: search into how: section. A registry section must identify the cited work/edition and lead to a "
    "held substantive witness before it supports a verdict. Editorial notes, contents, unrelated search hits, "
    "missing pages and OCR loss remain unverifiable when they do not carry the matter. Preserve the existing "
    "no-witness rule: p-says and anchor-b come from the held witness or stay empty; never fill them from memory. "
    "Do not label unverifiable as misattributed. Every paired_fidelity row retains explicit verdict: and how: "
    "fields (unknown/not applicable retrieval is kept in retrieval-status); all substantive verdicts retain "
    "both A and P anchors. Reconcile verdict totals and table cells against final wall and critic rulings."
)


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True)


def scalar_edits(before, edits):
    tree = yaml.compose(before)
    expected = yaml.safe_load(before)
    spans = []
    for path, transform in edits:
        node, parent = tree, expected
        for key in path[:-1]:
            node = node.value[key] if isinstance(key, int) else next(v for k, v in node.value if k.value == key)
            parent = parent[key]
        key = path[-1]
        node = node.value[key] if isinstance(key, int) else next(v for k, v in node.value if k.value == key)
        value = '\n'.join(line.rstrip() for line in transform(parent[key]).split('\n'))
        parent[key] = value
        line = before.splitlines()[node.start_mark.line]
        indent = len(line) - len(line.lstrip()) + 2
        folded = re.sub(r'\n+', lambda m: m[0] + '\n', value)
        block = '>-\n' + textwrap.indent('\n'.join(textwrap.fill(p, width=100, break_long_words=False, break_on_hyphens=False) for p in folded.split('\n')), ' ' * indent)
        spans.append((node.start_mark.index, node.end_mark.index, block))
    after = before
    for start, end, replacement in sorted(spans, reverse=True):
        after = after[:start] + replacement + after[end:]
    actual = yaml.safe_load(after)
    for path, _ in edits:
        left, right = actual, expected
        for key in path:
            left, right = left[key], right[key]
        assert left == right, (path, list(difflib.ndiff(right.splitlines(), left.splitlines())))
    assert actual == expected, 'scalar edit changed YAML meaning'
    return after


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--base', required=True, help='committed main-tree HEAD to freeze')
    args = ap.parse_args()
    base = git('rev-parse', args.base).strip()
    records = []

    def source(path):
        return git('show', f'{base}:{path}')

    def patch(name, rationale, changes):
        body = f'Rationale: {rationale} Generated against main-tree HEAD {base}; this file is deferred and does not authorize application before the pilot completes.\n\n'
        for path, before, after in changes:
            assert before != after
            body += f'diff --git a/{path} b/{path}\n'
            body += ''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='a/' + path, tofile='b/' + path))
            records.append({'patch': name, 'path': path, 'base_blob': git('rev-parse', f'{base}:{path}').strip(), 'base_sha256': hashlib.sha256(before.encode()).hexdigest(), 'candidate_sha256': hashlib.sha256(after.encode()).hexdigest()})
        (DEST / name).write_text(body)

    notes = {
        'engagement_map': ('010_engagement_design_notes.patch', INVENTORY, 'Expose the verified passage inventory in the synthesis while preserving canonical passage counts and source provenance. This changes retained evidence and final cells, so validate original versus revision with full source reads, anchor/cell checks and Sonnet in both orders; the table is not certified cosmetic.'),
        'reception_map': ('011_reception_design_notes.patch', RECEPTION, 'Make reference-point rows visible and exclude them from secondary-reader totals; require directed citation-ledger zeros for silence claims. The role label alone is cosmetic, but these combined counting/evidence changes require original/revision source reads, anchor/cell checks and both-order Sonnet validation.'),
        'fidelity_audit': ('012_fidelity_design_notes.patch', FIDELITY, 'Prefer supplied marked renditions and preserve work-registry sections and edition identity without relaxing the no-witness rule. Retrieval and evidence changes require affected index-only and held-source conditions, OCR/editorial-notes negative controls, source reads, anchor/cell checks and both-order original/revision comparison. Freeze rendition changes as separate evidence conditions.'),
    }
    for short, (name, note, rationale) in notes.items():
        key = 'citation_' + short
        cap_path = f'src/engines/capability_definitions/{key}.yaml'
        op_path = f'src/operationalizations/definitions/{key}.yaml'
        cap, op = source(cap_path), source(op_path)
        summary = {
            'engagement_map': 'Include a verified passage inventory from the applied ledger with stable passage IDs and final row/anchor links; report canonical passage coverage separately from finding counts.',
            'reception_map': 'Mark A as reference_point and exclude those rows from secondary-reader totals. A-to-reader silence requires a scoped explicit citation-ledger zero, with its direction and coverage; absent counts remain unknown.',
            'fidelity_audit': 'Use supplied marked page or registry-section witnesses and preserve work, section and edition identity. A section title alone is no witness; absent or irrelevant primary words leave the verdict unverifiable.',
        }[short]
        cap_after = scalar_edits(cap, [(('problematique',), lambda s: s + '\n' + summary + '\n' + RENDITION)])
        edits = [
            (('process', 'framing'), lambda s: s + '\n' + summary + '\n' + RENDITION),
            (('process', 'steps', 1, 'duties', 6), lambda s: s + '\n' + note + '\n' + RENDITION),
            (('process', 'steps', 2, 'brief'), lambda s: s + '\n\n' + note + '\n\n' + RENDITION),
        ]
        if short == 'engagement_map':
            edits += [
                (('process', 'dimensions', 1, 'method_card'), lambda s: s + '\n' + RENDITION + ' Preserve explicit canonical passage/event mappings across dimension rows.'),
                (('process', 'dimensions', 1, 'answer_shape'), lambda s: s + ' — canonical-event: <supplied mapping or unresolved> — rendition: <supplied identity> — edition: <supplied or unknown> — section-uid: <supplied or unknown> — section-title: <supplied or unknown>'),
            ]
        elif short == 'reception_map':
            for index in (0, 4, 5):
                edits.append((('process', 'dimensions', index, 'method_card'), lambda s: s + '\n' + RECEPTION))
            edits.append((('process', 'dimensions', 0, 'answer_shape'), lambda s: s.replace('<secondary reader or A reference point>', 'reader|reference_point')))
            edits.append((('process', 'dimensions', 2, 'answer_shape'), lambda s: s + ' — role: reader|reference_point'))
            edits.append((('process', 'dimensions', 4, 'answer_shape'), lambda s: s + ' — role: reader|reference_point — count-direction: <A-to-reader or ranking basis> — ledger-row: <supplied ID or absent> — checked-scope: <texts/dates/aliases/snapshot or unknown>'))
        else:
            for index in (2, 4, 5):
                edits.append((('process', 'dimensions', index, 'method_card'), lambda s: s + '\n' + FIDELITY + '\n' + RENDITION))
            for index in (4, 5):
                edits.append((('process', 'dimensions', index, 'answer_shape'), lambda s: s + ' — work-uid: <supplied identity or unresolved> — rendition: <supplied identity> — section-uid: <supplied or unknown>'))
            # Make the released framing's required how field explicit in the relational shape.
            edits.append((('process', 'dimensions', 2, 'answer_shape'), lambda s: s.replace('<printed/PDF pages>', '<supplied printed/PDF pages or registry section UID/title; edition>')))
        op_after = scalar_edits(op, edits)
        if short == 'engagement_map':
            op_after = op_after.replace('    - passage_move_stance_locus\n', '    - passage_move_stance_locus\n    - verified_passage_inventory\n', 1)
        if short == 'fidelity_audit':
            op_after = op_after.replace('— edition-locus: <limit>', '— how: page|section|search (only when retrieved) — retrieval-status: retrieved|unheld|unresolved — section-title: <supplied or unknown> — edition-locus: <limit>', 1)
        # Existing questions, dimensions, routes and depth selection are preserved.
        old, new = yaml.safe_load(op), yaml.safe_load(op_after)
        assert old['depth_sequences'] == new['depth_sequences']
        assert old['process']['routing'] == new['process']['routing']
        assert [d['questions'] for d in old['process']['dimensions']] == [d['questions'] for d in new['process']['dimensions']]
        patch(name, rationale, [(cap_path, cap, cap_after), (op_path, op, op_after)])

    path = 'src/dossier/catalog_purpose.json'
    before = source(path)
    catalog = json.loads(before)
    group = next(g for g in catalog['groups'] if g['key'] == 'trace_citations')
    assert all(e['engine_key'] != 'citation_cohort_synthesis' for e in group['engines'])
    group['engines'].append({
        'engine_key': 'citation_cohort_synthesis',
        'plain_name': 'cohort citation synthesis',
        'use_when': 'you have completed pair analyses for an approved school or cohort and want an argued comparison of how the author uses its members, including the members not engaged in the checked corpus',
        'yields': 'cross-member reliance, asymmetries, supported periods and audited fidelity, with member counts, move/stance tables and the complete not-engaged residue linked to pair ledgers and source passages',
        'row_unit': 'one member finding, cohort metadata observation or comparison supported by distinct members',
        'deliverable_kinds': ['briefing', 'case_file'],
        'pairs_with': ['citation_engagement_map', 'citation_fidelity_audit', 'citation_reception_map'],
        'fit': 'ok',
        'fit_note': 'requires approved membership and counts, a plan, and a completed engagement map for every engaged member; fidelity and reception are optional; fewer than two engaged members yield a limited coverage report',
    })
    after = json.dumps(catalog, indent=2, ensure_ascii=False) + '\n'
    patch('090_catalogue_offer_after_validation.patch', 'Offer cohort synthesis under Trace the citations only after adapter integration and the real Brenner-cohort release gate: source/anchor/cell checks, both-order comparison with the Stacks essay desk and owner reading. Apply this patch last. It uses existing catalogue fields and introduces no fictitious applicability gate.', [(path, before, after)])
    (DEST / 'design_patch_baselines.json').write_text(json.dumps({'base_commit': base, 'files': records}, indent=2) + '\n')
    print(f'Wrote four deferred patches at {base}; no target files changed.')


if __name__ == '__main__':
    main()
