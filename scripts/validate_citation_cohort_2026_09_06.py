"""Offline cohort shape/provenance checks; no production imports or LLM calls.

Usage: python scripts/validate_citation_cohort_2026_09_06.py packet.json
       ... packet.json --output output.json --release
The --release switch blocks synthetic evidence; it is NOT a semantic release certificate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ENG = 'citation_engagement_map'
FID = 'citation_fidelity_audit'
REC = 'citation_reception_map'
ENGINES = {ENG, FID, REC}
CROSS = {'cross_member_reliance', 'engagement_asymmetries', 'school_periodization', 'school_fidelity', 'reception_alignment'}
PREFIX = dict(member_uses='C1', cohort_residue='C2', cross_member_reliance='C3', engagement_asymmetries='C4', school_periodization='C5', school_fidelity='C6', reception_alignment='C7')
TABLES = {'member_text_year_counts', 'member_move_stance', 'fidelity_by_member', 'not_engaged_members', 'cohort_periods'}
VERDICTS = {'accurate', 'fair', 'selective', 'stretched', 'misattributed', 'unverifiable'}


class ContractError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise ContractError(message)


def required(obj, keys, label):
    need(isinstance(obj, dict), f'{label}: expected object')
    missing = set(keys) - set(obj)
    need(not missing, f'{label}: missing {sorted(missing)}')


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def uid(value):
    return nonempty(value) and not any(x in value for x in ('__', '::')) and not re.search(r'\s', value)


def integer(value):
    return type(value) is int and value >= 0


_QUOTES = "\"'\u201c\u201d\u2018\u2019\u00ab\u00bb"


def norm_anchor(s):
    """The walls' law for a verbatim quotation (whitespace folded, quotation marks and soft hyphens dropped, a hyphen at a
    line break closed, dashes unified); the packet's anchor rules apply it on both sides (2026-09-06, after the first real
    export: the engines quote under this law, so byte-exact matching refused rows the wall had verified)."""
    s = (s or '').replace('\u00ad', '')
    s = re.sub(r'-\s*\n\s*', '', s)
    s = re.sub(r'[\u2010-\u2015]', '-', s)
    s = ''.join(c for c in s if c not in _QUOTES)
    return re.sub(r'\s+', ' ', s).strip()


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def citable(row):
    return row['status'] == 'confirmed' and row['anchor_status'] == 'verified' and row['canonical_ref'] is None


def render_pair(pair):
    parts = ['SOURCE ROLE: pair_output', f"pair-key: {pair['pair_key']}", f"member: {pair['member_uid']}"]
    for ledger in pair['ledgers']:
        parts.extend([ledger['engine_key'], ledger['artifact_id'], ledger['artifact_sha256']])
        for row in ledger['rows']:
            parts.extend([row['ref'], row['raw_row']])
            for a in row['anchors']:
                parts.append(f"CARRIED ANCHOR [{row['ref']}] [{a['source_doc_key']}]: {a['text']}")
    parts.append('NAVIGATION ONLY: tables and memo, not independent evidence')
    parts.extend(t['markdown'] for t in pair['tables'])
    parts.append(pair['memo']['markdown'])
    return '\n'.join(parts)


def validate_packet(packet, release=False):
    required(packet, ['schema_version','packet_id','revision','fixture_only','author','cohort','plan','pairs','source_documents'], 'packet')
    need(packet['schema_version'] == 'cohort-packet/v1', 'packet version')
    need(nonempty(packet['packet_id']) and integer(packet['revision']), 'packet identity/revision')
    need(type(packet['fixture_only']) is bool, 'fixture_only must be boolean')
    if release:
        need(not packet['fixture_only'], 'fixture-only packet cannot support release')
    required(packet['author'], ['uid','name'], 'author')
    need(uid(packet['author']['uid']), 'invalid author UID')
    required(packet['plan'], ['role','doc_key','sections','themes','warnings'], 'plan')
    need(packet['plan']['role']=='plan' and packet['plan']['doc_key']=='context:plan', 'plan role/key')
    need(isinstance(packet['plan']['sections'], list) and packet['plan']['sections'], 'plan sections missing')
    cohort = packet['cohort']
    required(cohort, ['role','doc_key','uid','phrase','approved','members','not_engaged_residue','coverage','collective_mentions'], 'cohort')
    need(cohort['role']=='cohort' and cohort['doc_key']=='context:cohort', 'cohort role/key')
    need(cohort['approved'] is True, 'cohort not approved')
    coverage = cohort['coverage']
    required(coverage, ['ledger_snapshot','count_unit','complete','identities_resolved','held_texts','inspected_texts','missing_texts','date_range','alias_scope','coauthorship'], 'coverage')
    need(coverage['count_unit']=='canonical_citation_event', 'unsupported count unit')
    need(nonempty(coverage['ledger_snapshot']), 'ledger snapshot missing')
    members, cohort_rows = {}, {}
    for m in cohort['members']:
        required(m, ['uid','name','membership_role','membership_reason','membership_source','engaged','counts','works_cited','row_id','anchor','fixture_only'], 'member')
        need(uid(m['uid']) and m['uid'] not in members, 'duplicate/invalid member UID')
        need(nonempty(m['row_id']) and m['row_id'] not in cohort_rows, 'duplicate cohort row')
        need(nonempty(m['membership_reason']) and nonempty(m['anchor']), 'missing membership basis/anchor')
        need(m['engaged'] in ('yes','no','unknown'), 'bad engaged state')
        need(type(m['fixture_only']) is bool, 'member fixture flag')
        need(not m['fixture_only'] or packet['fixture_only'], 'unlabelled synthetic member')
        if release:
            need(not m['fixture_only'] and not m['uid'].startswith('fixture:'), 'synthetic member cannot support release')
        counts = m['counts']
        required(counts, ['total','mentions','bibliography_only','by_text'], 'counts')
        if m['engaged']=='unknown':
            need(counts['total'] is None and counts['by_text']==[], 'unknown engagement is not zero')
        else:
            need(integer(counts['total']), 'count must be nonnegative integer')
            seen, text_keys = set(), set()
            for t in counts['by_text']:
                required(t, ['text_key','year','count','event_ids'], 'count row')
                need(nonempty(t['text_key']) and t['text_key'] not in text_keys, 'duplicate count text/rendition')
                text_keys.add(t['text_key'])
                need(t['year'] is None or type(t['year']) is int, 'invalid year')
                need(integer(t['count']) and t['count']==len(t['event_ids']), 'event count mismatch')
                need(all(nonempty(e) for e in t['event_ids']), 'empty event ID')
                need(len(set(t['event_ids']))==len(t['event_ids']) and not seen.intersection(t['event_ids']), 'duplicate event within member')
                seen.update(t['event_ids'])
            need(len(seen)==counts['total'], 'member total differs from unique events')
            need(all(integer(counts[k]) and counts[k]<=counts['total'] for k in ('mentions','bibliography_only')), 'invalid count subtype')
            need(counts['mentions']+counts['bibliography_only']<=counts['total'], 'count subtypes overlap')
            need((counts['total']>0)==(m['engaged']=='yes'), 'engaged/count contradiction')
        if m['engaged']=='no':
            need(coverage['complete'] is True and coverage['identities_resolved'] is True, 'zero without completed ledger/alias check')
        members[m['uid']] = m
        cohort_rows[m['row_id']] = m
    residue = cohort['not_engaged_residue']
    need(isinstance(residue,list) and len(residue)==len(set(residue)), 'residue duplicate/type')
    need(set(residue)=={u for u,m in members.items() if m['engaged']=='no'}, 'residue does not equal approved zero members')
    for key, source in packet['source_documents'].items():
        required(source, ['text','sha256'], 'source document')
        need(nonempty(key) and nonempty(source['text']) and sha(source['text'])==source['sha256'], 'source digest/text mismatch')
    pairs, rows, pair_of, rendered = {}, {}, {}, {}
    for pair in packet['pairs']:
        required(pair, ['pair_key','doc_key','author_uid','member_uid','fixture_only','ledgers','lens_status','tables','memo'], 'pair')
        member = pair['member_uid']
        need(member in members and members[member]['engaged']=='yes', 'pair belongs to non-engaged/unknown member')
        need(pair['author_uid']==packet['author']['uid'], 'foreign author')
        expected = f"{packet['author']['uid']}__{member}"
        need(pair['pair_key']==expected and pair['doc_key']=='pair::'+expected, 'pair key/doc identity')
        need(expected not in pairs, 'duplicate pair document')
        need(type(pair['fixture_only']) is bool, 'pair fixture flag')
        need(not pair['fixture_only'] or packet['fixture_only'], 'unlabelled synthetic pair')
        if release:
            need(not pair['fixture_only'], 'synthetic pair cannot support release')
        engines = set()
        events = {e for t in members[member]['counts']['by_text'] for e in t['event_ids']}
        for ledger in pair['ledgers']:
            required(ledger, ['engine_key','artifact_id','artifact_sha256','artifact_text','rows','reviewed_empty'], 'ledger')
            engine = ledger['engine_key']
            need(engine in ENGINES and engine not in engines, 'duplicate/unknown engine ledger')
            engines.add(engine)
            need(sha(ledger['artifact_text'])==ledger['artifact_sha256'], 'ledger digest mismatch')
            need(ledger['rows'] or (ledger['reviewed_empty'] is True and nonempty(ledger.get('empty_reason'))), 'unreviewed empty ledger')
            for row in ledger['rows']:
                required(row, ['row_id','ref','dimension','claim','raw_row','status','anchor_status','canonical_ref','event_ids','anchors','fields'], 'pair row')
                ref = f"{expected}::{engine}::{row['row_id']}"
                need(nonempty(row['row_id']) and row['ref']==ref and ref not in rows, 'row identity collision')
                need(row['status'] in ('confirmed','rejected','unresolved','superseded'), 'bad row status')
                need(row['anchor_status'] in ('verified','failed','unverifiable'), 'bad anchor status')
                need(nonempty(row['raw_row']) and row['raw_row'] in ledger['artifact_text'], 'raw row not in ledger artifact')
                need(f"[{row['row_id']}]" in row['raw_row'] and row['claim'] in row['raw_row'] and f"dim: {row['dimension']}" in row['raw_row'], 'row export differs from raw ledger')
                need(len(set(row['event_ids']))==len(row['event_ids']) and set(row['event_ids'])<=events, 'row event outside member ledger')
                if citable(row):
                    need(row['anchors'], 'citable row without anchors')
                for a in row['anchors']:
                    required(a, ['text','source_doc_key','locus','voice'], 'anchor')
                    need(nonempty(a['text']) and nonempty(a['source_doc_key']), 'empty anchor/source')
                    if citable(row):
                        need(norm_anchor(a['text']) in norm_anchor(row['raw_row']), 'fresh anchor not carried in raw row')
                        need(a['source_doc_key'] in packet['source_documents'], 'missing original source witness')
                        need(norm_anchor(a['text']) in norm_anchor(packet['source_documents'][a['source_doc_key']]['text']), 'anchor not re-found in claimed original source')
                if engine==FID and citable(row) and row.get('dimension')=='paired_fidelity':   # only the paired rows carry a verdict; D1–D5 describe
                    need(row['fields'].get('verdict') in VERDICTS, 'missing fidelity verdict')
                    if row['fields']['verdict']!='unverifiable':
                        need(len({a['source_doc_key'] for a in row['anchors']})>=2, 'fidelity verdict without distinct A/P witnesses')
                        need(row['fields'].get('how') in ('page','section','search'), 'missing fidelity how')
                rows[ref], pair_of[ref] = row, pair
        need(ENG in engines, 'pair without engagement-map ledger')
        for engine in ENGINES:
            need(pair['lens_status'].get(engine) in ('run','not_run','unavailable'), 'missing lens status')
            need((pair['lens_status'][engine]=='run')==(engine in engines), 'lens/ledger mismatch')
        required(pair['memo'], ['markdown','canonical_uri'], 'memo')
        for table in pair['tables']:
            required(table, ['table_key','markdown','row_refs'], 'pair table')
            for ref in table['row_refs']:
                need(ref in rows and pair_of[ref] is pair and citable(rows[ref]), 'pair table cites missing/rejected row')
        pairs[expected] = pair
        rendered[pair['doc_key']] = render_pair(pair)
    need({p['member_uid'] for p in pairs.values()}=={u for u,m in members.items() if m['engaged']=='yes'}, 'engaged member missing required pair ledger')
    for ref,row in rows.items():
        if row['canonical_ref'] is not None:
            target = rows.get(row['canonical_ref'])
            need(target is not None and citable(target), 'restatement has dangling/noncanonical target')
            need(pair_of[ref]['pair_key']==pair_of[row['canonical_ref']]['pair_key'], 'restatement crosses pair identities')
        if citable(row):
            need(all(a['text'] in rendered[pair_of[ref]['doc_key']] for a in row['anchors']), 'anchor absent from pair document')
    return dict(members=members, cohort_rows=cohort_rows, pairs=pairs, rows=rows, pair_of=pair_of, documents=rendered)


def render_output(output):
    """Render the exact reviewed sidecar, making prose/table equality checkable."""
    parts = []
    for p in output['prose']:
        parts.append(p['text']+' '+ ' '.join('['+x+']' for x in p['finding_ids']))
    for table in output['tables']:
        parts.extend(['', '## '+table['key']])
        columns = table['columns']
        parts.append('| '+' | '.join(columns)+' |')
        parts.append('| '+' | '.join('---' for _ in columns)+' |')
        for row in table['rows']:
            values = []
            for cell in row['cells']:
                value = cell['text'].replace('|','\\|').replace('\n','<br>')
                values.append(value+' '+ ' '.join('['+x+']' for x in cell['finding_ids']))
            parts.append('| '+' | '.join(values)+' |')
    return '\n'.join(parts).strip()+'\n'


def validate_output(packet, output, release=False):
    index = validate_packet(packet, release=release)
    required(output, ['schema_version','packet_id','packet_revision','fixture_only','mode','findings','tables','prose','markdown'], 'output')
    need(output['schema_version']=='cohort-output/v1', 'output version')
    need(output['packet_id']==packet['packet_id'] and output['packet_revision']==packet['revision'], 'stale output packet revision')
    need(output['fixture_only'] is packet['fixture_only'], 'output fixture flag differs')
    need(output['mode'] in ('oneshot','oneshot_checked','dvs'), 'unknown execution mode')
    final = {}
    for f in output['findings']:
        required(f, ['id','dimension','claim','members','status','evidence','cohort_evidence'], 'finding')
        dim = f['dimension']
        need(dim in PREFIX and re.fullmatch(re.escape(PREFIX[dim])+r'\.F[1-9][0-9]*',f['id']) is not None, 'dimension/id prefix mismatch')
        need(f['id'] not in final and f['status']=='confirmed', 'duplicate or rejected final finding')
        need(nonempty(f['claim']), 'empty finding')
        need(len(set(f['members']))==len(f['members']) and set(f['members'])<=set(index['members']), 'finding member identity')
        evidence_members, cited_rows = set(), []
        for e in f['evidence']:
            required(e, ['pair_row_ref','anchors'], 'finding evidence')
            ref = e['pair_row_ref']
            need(ref in index['rows'] and citable(index['rows'][ref]), 'finding cites missing/rejected/noncanonical pair row')
            row = index['rows'][ref]
            need(e['anchors']==row['anchors'], 'output invented, edited or dropped an inherited anchor')
            evidence_members.add(index['pair_of'][ref]['member_uid'])
            cited_rows.append(row)
        metadata_members = set()
        for e in f['cohort_evidence']:
            required(e, ['row_id','anchor'], 'metadata evidence')
            need(e['row_id'] in index['cohort_rows'], 'missing cohort row')
            m = index['cohort_rows'][e['row_id']]
            need(e['anchor']==m['anchor'], 'cohort anchor changed')
            metadata_members.add(m['uid'])
        need(set(f['members'])==evidence_members|metadata_members, 'missing or extraneous member support')
        if dim=='cohort_residue':
            need(not f['evidence'] and f['cohort_evidence'], 'residue must cite cohort metadata only')
        else:
            need(f['evidence'], 'interpretation without pair-ledger evidence')
            need(all(index['members'][u]['engaged']=='yes' for u in f['members']), 'reading of non-engaged/unknown member')
        if dim in CROSS:
            need(len(evidence_members)>=2, 'cross-member claim needs distinct engaged pairs')
        if dim in ('cross_member_reliance','engagement_asymmetries','school_periodization'):
            supported = {index['pair_of'][e['pair_row_ref']]['member_uid'] for e in f['evidence'] if '::'+ENG+'::' in e['pair_row_ref']}
            need(supported==evidence_members, 'member comparison lacks engagement warrant')
        if dim=='engagement_asymmetries':
            need(metadata_members==evidence_members, 'asymmetry needs counted cohort rows for each member')
        if dim in ('school_fidelity','reception_alignment'):
            engine = FID if dim=='school_fidelity' else REC
            supported = {index['pair_of'][e['pair_row_ref']]['member_uid'] for e in f['evidence'] if '::'+engine+'::' in e['pair_row_ref'] and (dim!='school_fidelity' or index['rows'][e['pair_row_ref']]['fields'].get('verdict')!='unverifiable')}
            need(supported==evidence_members, 'cross-lens claim without assessed lens rows for each member')
        if dim=='school_periodization':
            endpoints = f.get('temporal_endpoints',[])
            need(len(endpoints)>=2, 'period lacks dated endpoints')
            cited = {e['pair_row_ref'] for e in f['evidence']}
            for endpoint in endpoints:
                required(endpoint, ['pair_row_ref','text_key','year'], 'endpoint')
                need(endpoint['pair_row_ref'] in cited, 'uncited temporal endpoint')
                fields = index['rows'][endpoint['pair_row_ref']]['fields']
                need(type(endpoint['year']) is int and endpoint['year']==fields.get('year') and endpoint['text_key']==fields.get('text_key'), 'invented date/text endpoint')
            need(len({e['text_key'] for e in endpoints})>=2 and len({e['year'] for e in endpoints})>=2, 'period lacks distinct dated texts')
        final[f['id']] = f
    need(len(output['tables'])==len(TABLES) and {t['key'] for t in output['tables']}==TABLES, 'required tables missing or duplicated')
    for table in output['tables']:
        required(table, ['key','columns','rows'], 'output table')
        need(table['columns'] and len(set(table['columns']))==len(table['columns']), 'table columns')
        for row in table['rows']:
            required(row, ['member_uid','cells'], 'table row')
            need(row['member_uid'] is None or row['member_uid'] in index['members'], 'foreign table member')
            need([c['column'] for c in row['cells']]==table['columns'], 'table cell/column mismatch')
            for cell in row['cells']:
                required(cell, ['column','text','kind','finding_ids'], 'cell')
                need(cell['kind'] in ('supported','unknown'), 'unreviewable cell kind')
                need(all(i in final for i in cell['finding_ids']), 'table cites rejected or missing final row')
                if cell['kind']=='supported':
                    need(cell['finding_ids'], 'positive cell lacks final finding')
                else:
                    need(cell['text'] in ('not run','unverifiable','unresolved','not supplied') and not cell['finding_ids'], 'unknown cell smuggles unsupported reading')
                if row['member_uid'] is not None:
                    need(all(row['member_uid'] in final[i]['members'] for i in cell['finding_ids']), 'table member/row attribution mismatch')
        if table['key']=='not_engaged_members':
            need(len(table['rows'])==len(packet['cohort']['not_engaged_residue']) and {r['member_uid'] for r in table['rows']}==set(packet['cohort']['not_engaged_residue']), 'final table dropped/duplicated residue')
            need(all(final[i]['dimension']=='cohort_residue' for r in table['rows'] for c in r['cells'] for i in c['finding_ids']), 'non-engaged table contains a reading')
    for prose in output['prose']:
        required(prose, ['text','finding_ids'], 'prose')
        need(prose['finding_ids'] and all(i in final for i in prose['finding_ids']), 'prose has unsupported or rejected reference')
    need(output['markdown']==render_output(output), 'actual markdown differs from reviewed prose/table cells')
    for ref in re.findall(r'\[(C[1-7]\.F[0-9]+)\]', output['markdown']):
        need(ref in final, 'dangling citation in actual markdown')
    return {'shape_pass': True, 'findings': len(final), 'pair_rows': len(index['rows']), 'synthetic': packet['fixture_only'], 'semantic_release': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--release', action='store_true')
    args = parser.parse_args()
    packet = json.loads(args.packet.read_text())
    try:
        if args.output:
            result = validate_output(packet, json.loads(args.output.read_text()), release=args.release)
        else:
            result = validate_packet(packet, release=args.release)
            result = {'shape_pass': True, 'pairs': len(result['pairs']), 'rows': len(result['rows']), 'semantic_release': False}
    except (ContractError, KeyError, TypeError, ValueError) as exc:
        raise SystemExit(f'REFUSED: {exc}')
    print(json.dumps(result, indent=2))


if __name__=='__main__':
    main()
