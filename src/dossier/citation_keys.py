"""Expand evidence finding ranges without borrowing identities across brackets."""
import re

_FINDING = re.compile(r"(?:(?P<uid>[^/\s;,]+)/)?(?P<prefix>[A-Z]\d+\.)?F(?P<lo>\d+)(?:[-–—](?P<endprefix>[A-Z]\d+\.)?F(?P<hi>\d+))?")


def citation_keys(group):
    """Expand bounded, ascending same-stage ranges; retain invalid keys visibly.

    A bare finding inherits only the last explicit source/stage in this bracket.
    Missing evidence is deliberately not filtered out here.
    """
    group = re.sub(r"(?<=\d)\s*([-–—])\s*(?=(?:[A-Z]\d+\.)?F\d)", r"\1", group)
    keys, uid, prefix = [], None, ""
    for token in re.split(r"[\s,;]+", group.strip()):
        match = _FINDING.fullmatch(token)
        if not match:
            if token:
                keys.append(token)
            uid, prefix = None, ""
            continue
        if match['uid']:
            uid, prefix = match['uid'], match['prefix'] or ""
        elif match['prefix']:
            prefix = match['prefix']
        start = int(match['lo'])
        end = int(match['hi'] or start)
        base = f"{uid}/" if uid else ""
        if end < start or end - start > 512 or (match['endprefix'] and match['endprefix'] != prefix):
            keys.append(base + token.rsplit('/', 1)[-1])
            continue
        keys.extend(f"{base}{prefix}F{n}" for n in range(start, end + 1))
    return keys
