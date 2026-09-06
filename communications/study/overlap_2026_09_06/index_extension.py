"""Candidate functions appended by 010; executed only in memory by the design tests."""
def _overlap_uid(value):
    if not isinstance(value, str) or not value or re.search(r'\s|__|::', value):
        raise ValueError('invalid overlap person UID')
    return value


def _strict_aliases(sources):
    aliases = {}
    for key, body in sources.items():
        names = {key, _bare(key), f'em:{_bare(key)}'}
        header = re.search(r'^ZOTERO UID: (\S+)', body[:600], re.M)
        if header:
            names.update({header[1], _bare(header[1]), f'em:{_bare(header[1])}'})
        for name in names:
            if name in aliases and aliases[name] != key:
                raise ValueError('duplicate physical document alias: ' + name)
            aliases[name] = key
    return aliases


def _validate_overlap_index(obj):
    if 'author' in obj or not isinstance(obj.get('authors'), list) or len(obj['authors']) != 2:
        raise ValueError('overlap index needs authors[2], never singular author')
    authors = [_overlap_uid(a.get('uid')) for a in obj['authors']]
    if len(set(authors)) != 2:
        raise ValueError('overlap author UIDs must differ')
    person = _overlap_uid(obj.get('person', {}).get('uid'))
    if person in authors:
        raise ValueError('shared person is not either author')
    roles = obj.get('roles')
    if not isinstance(roles, dict):
        raise ValueError('overlap index requires roles map')
    role_aliases = {}
    for key, role in roles.items():
        if role not in {'citing_author', 'primary_window', 'secondary_reader'}:
            raise ValueError('unknown source role')
        bare = _bare(key)
        if bare in role_aliases and role_aliases[bare] != role:
            raise ValueError('conflicting role aliases')
        role_aliases[bare] = role
    seen_texts, refs, events, sides = set(), set(), set(), set()
    for text in obj['texts']:
        author = text.get('author')
        if author not in authors:
            raise ValueError('every text needs an explicit known author UID')
        if 'coauthored_with' not in text or not isinstance(text['coauthored_with'], list):
            raise ValueError('coauthored_with must be explicit')
        if (set(authors) - {author}) & set(text['coauthored_with']):
            raise ValueError('A+B coauthored text excluded from overlap')
        keys = {_bare(text.get(k)) for k in ('uid', 'key') if text.get(k)}
        if not keys or keys & seen_texts:
            raise ValueError('missing or repeated original citing text identity')
        seen_texts.update(keys)
        assigned = {role_aliases[k] for k in keys if k in role_aliases}
        if assigned != {'citing_author'}:
            raise ValueError('citing text missing or conflicting roles-map entry')
        sides.add(author)
        for passage in text.get('passages', []):
            rid = passage.get('ref_id')
            if isinstance(rid, bool) or not isinstance(rid, (int, str)) or str(rid) == '':
                raise ValueError('passage needs integer/string ref_id')
            ref = (author, str(rid))
            event = passage.get('event_id')
            if ref in refs or not isinstance(event, str) or not event.startswith(author+'::') or event in events:
                raise ValueError('duplicate/missing/foreign author-qualified passage identity')
            refs.add(ref); events.add(event)
    if sides != set(authors):
        raise ValueError('both authors need citing texts')
    for check in obj['checks']:
        author = check.get('author')
        if author not in authors or not check.get('ref_ids'):
            raise ValueError('check needs author and ref_ids')
        if any((author, str(r)) not in refs for r in check['ref_ids']):
            raise ValueError('check refers outside its author passages')
        copy = check.get('copy') or {}
        keys = {_bare(copy.get(k)) for k in ('uid', 'key') if copy.get(k)}
        if not copy.get('uid') or keys & seen_texts:
            raise ValueError('primary witness must differ from both authors texts')
        if {role_aliases[k] for k in keys if k in role_aliases} != {'primary_window'}:
            raise ValueError('held witness needs primary_window role')
    for item in obj.get('unchecked', []):
        if (item.get('author'), str(item.get('ref_id'))) not in refs:
            raise ValueError('unchecked reference has no matching author passage')
    return authors


def slice_overlap_index(obj, author_uid):
    """Explicitly project the validated transport for one existing citation engine.

    This does not generate or alter evidence, schedule an audit, or rename refs.
    """
    authors = _validate_overlap_index(obj)
    if author_uid not in authors:
        raise ValueError('unknown slice author')
    result = json.loads(json.dumps(obj))
    result['author'] = next(a for a in result.pop('authors') if a['uid'] == author_uid)
    result['version'] = 'overlap-side-index/v1'
    result['texts'] = [t for t in result['texts'] if t['author'] == author_uid]
    result['checks'] = [c for c in result['checks'] if c['author'] == author_uid]
    result['unchecked'] = [c for c in result.get('unchecked', []) if c['author'] == author_uid]
    wanted = {_bare(x.get(k)) for x in result['texts'] + [c['copy'] for c in result['checks']] + result.get('readers', []) for k in ('uid', 'key') if x.get(k)}
    result['roles'] = {k: v for k, v in result['roles'].items() if _bare(k) in wanted}
    return result


def _prepare_overlap_sources(documents, indexes):
    if len(indexes) != 1:
        raise ValueError('one overlap index for one shared person is required')
    index_key, original = indexes[0]
    obj = json.loads(json.dumps(original))
    authors = _validate_overlap_index(obj)
    contexts, supplied = [], {}
    for key, body in documents.items():
        if key == index_key:
            continue
        try:
            meta = json.loads(body)
        except (ValueError, TypeError):
            meta = None
        if isinstance(meta, dict) and meta.get('role') in {'plan', 'overlap_table'}:
            if meta['role'] == 'overlap_table':
                if [a['uid'] for a in meta.get('authors', [])] != authors:
                    raise ValueError('overlap table author axis differs from index')
            contexts.append({'key': key, 'data': meta})
        else:
            supplied[key] = body
    aliases = _strict_aliases(supplied)
    roles = {}
    for rk, role in obj['roles'].items():
        sk = _meet(aliases, rk)
        if sk:
            if sk in roles and roles[sk] != role:
                raise ValueError('supplied source has conflicting roles')
            roles[sk] = role
    if set(roles) != set(supplied):
        raise ValueError('unclassified supplied source in overlap job')
    for key, role in roles.items():
        header = re.search(r'^SOURCE ROLE: (\w+)', supplied[key], re.M)
        if header and header[1] != role:
            raise ValueError('SOURCE ROLE header conflicts with roles map')
        if not header:
            supplied[key] = f'SOURCE ROLE: {role}\n' + supplied[key]
        elif not supplied[key].startswith('SOURCE ROLE:'):
            raise ValueError('SOURCE ROLE must be the first header')
    occupied = set()
    for entry in obj['texts']:
        met = _meet(aliases, entry.get('uid'), entry.get('key'))
        key = met or entry.get('uid') or entry['key']
        if key in occupied:
            raise ValueError('two index texts meet the same physical source')
        occupied.add(key)
        if met:
            header = re.search(r'^CITING AUTHOR UID: (\S+)', supplied[met], re.M)
            if header and header[1] != entry['author']:
                raise ValueError('source author header conflicts with index')
            if not header:
                supplied[met] = supplied[met].replace('SOURCE ROLE: citing_author\n', 'SOURCE ROLE: citing_author\nCITING AUTHOR UID: '+entry['author']+'\n', 1)
            entry['supplied_as'] = met
        else:
            parts = [p.get('section') or p.get('window') or '\n'.join(p.get(n, '') for n in ('before', 'hit', 'after')) for p in entry.get('passages', [])]
            body = entry.get('text') or '\n\n'.join(dict.fromkeys(p for p in parts if p.strip()))
            if not body.strip():
                raise ValueError('citing text has no literal witness')
            supplied[key] = f"SOURCE ROLE: citing_author\nCITING AUTHOR UID: {entry['author']}\nTITLE: {entry.get('title', key)}\nYEAR: {entry.get('year') if entry.get('year') is not None else 'unknown'}\nCOVERAGE: supplied citation witnesses\n\n{body}"
            entry['supplied_as'] = key
    # Every supplied citing source must have author identity in texts, not just a role.
    if any(role == 'citing_author' and key not in occupied for key, role in roles.items()):
        raise ValueError('citing source has no indexed author identity')
    aliases = _strict_aliases(supplied)
    for check in obj['checks']:
        copy = check['copy']
        met = _meet(aliases, copy.get('uid'), copy.get('key'))
        key = met or copy['uid']
        if key in occupied:
            raise ValueError('primary copy alias collides with citing source')
        parts = []
        for window in check.get('windows', []):
            if window.get('how') not in {'page', 'section', 'search'} or not isinstance(window.get('text'), str) or not window['text'].strip():
                raise ValueError('window needs literal text and page/section/search how')
            parts.append(window['text'])
        if not met and parts:
            supplied[key] = f"SOURCE ROLE: primary_window\nTITLE: {check.get('title', key)}\nCOPY: {json.dumps(copy, ensure_ascii=False)}\n\n"+'\n\n'.join(dict.fromkeys(parts))
            aliases = _strict_aliases(supplied)
        elif met:
            for part in dict.fromkeys(parts):
                if part not in supplied[key]:
                    supplied[key] += '\n\n'+part
        if key in supplied:
            check['supplied_as'] = key
    sources = {k: v for k, v in supplied.items() if re.match(r'SOURCE ROLE: (citing_author|primary_window)\n', v)}
    # Remove literal witnesses from metadata; keep every author/ref/work/locus join.
    slim = {k: v for k, v in obj.items() if k not in {'texts', 'checks', 'plan'}}
    slim['texts'] = [{k: v for k, v in t.items() if k not in {'text', 'passages'}} | {'passages': [{k: v for k, v in p.items() if k not in {'section', 'window', 'before', 'hit', 'after'}} for p in t.get('passages', [])]} for t in obj['texts']]
    slim['checks'] = [{k: v for k, v in c.items() if k != 'windows'} | {'windows': [{k: v for k, v in w.items() if k != 'text'} for w in c.get('windows', [])]} for c in obj['checks']]
    context = 'OVERLAP INDEX METADATA (not an anchor source):\n'+json.dumps(slim, ensure_ascii=False)
    context += '\nUPSTREAM PLAN (not evidence):\n'+json.dumps(obj.get('plan', {}), ensure_ascii=False)
    context += '\nSEPARATE CONTEXTS (table facts only; plan never evidence):\n'+json.dumps(contexts, ensure_ascii=False)
    return sources, context
