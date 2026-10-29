"""
What each written answer claims, read by CODE — no model call. Writes the same claims file the model reader
(reference/extract_claims.js) wrote:  [{pass, id, claims: {yes, possible, no, count[, names, unplaced]}, review}]

AeroSpark answers are data: every finding cites its contracts by id, and the service writes the doubt into the finding itself ("Possible
match only: …", "unclear — the search found a clause that may be one"). A cited contract is "possible" when its finding says so, "no" when
the finding says it does not match, else "yes" (a caveat about scope does not make it "possible": the rule extract_claims.js used).
A count is the tally's groups' own counts added up (one group: its count), else the tally's total, else the number the summary opens with.

ChatGPT answers are text. Code takes the NAMES the answer gives each contract — a link's text, a table row's first cell, a numbered or
bulleted item's lead — and places each on the roster the way extract_claims.js did after its model copied the names out (placeName:
the distinctive words of the name found in a contract's file name and parties; a tie is left unplaced). The claim is read from the line
and the heading it sits under: "possible" under a heading such as "Additional … / borderline / requiring review", "no" under one such
as "Related language, but not …", else "yes". Lines the rules are unsure of are listed under "review"; nothing is guessed silently.

    python3 scoring/claims_by_code.py <run file> <claims file> [--compare <old claims file>]
"""
import json
import re
import sys

POSSIBLE = re.compile(r'\b(possible|possibly|unclear|not established|unconfirmed|not confirmed|unlikely to qualify|may be one|requir\w* (?:verification|qualification|review)|needs? review|borderline|partial match|worth (?:reviewing|attention)|ambiguous|uncertain)\b', re.I)
NO = re.compile(r'\b(not an? [\w\- ]{0,30}in substance|does not (?:match|qualify|count)|do not (?:count|qualify)|not counted|excluded from|i (?:did not|didn.t) count|related language,? but not)\b', re.I)
# A heading's own words say what the list under it is: "Additional contracts …", "Related language, but not …".
HEAD_POSSIBLE = re.compile(r'\b(additional|related|borderline|possible|possibly|partial|qualif\w*|worth (?:reviewing|distinguishing|attention)|ambiguous|conditional|weaker|secondary|unclear|unconfirmed|requiring (?:review|verification|interpretation))\b', re.I)
HEAD_NO = re.compile(r'\b(not counted|excluded|but not|do not qualify|does not qualify|not included|rejected|did not count|non-matches)\b', re.I)
# extract_claims.js's NOT_DISTINCT and placeName, ported: words that name no one contract
NOT_DISTINCT = {'inc', 'corp', 'corporation', 'company', 'ltd', 'limited', 'llc', 'plc', 'group', 'holdings', 'the', 'and', 'agreement',
                'contract', 'services', 'service', 'international', 'technologies', 'technology', 'systems', 'license', 'licence', 'supply',
                'development', 'distribution', 'distributor', 'strategic', 'alliance', 'with', 'for', 'of'}
squash = lambda s: re.sub(r'[^a-z0-9]+', '', (s or '').lower())
words_of = lambda s: list(dict.fromkeys(w for w in re.split(r'[^a-z0-9]+', (s or '').lower()) if len(w) >= 3 and w not in NOT_DISTINCT))
LINK = re.compile(r'\[([^\]]{3,200})\]\((?:https?://)[^)]*\)')


def place_name(name, roster):
    ws = words_of(name)
    scored = []
    for i, text in enumerate(roster):
        hit = [w for w in ws if w in text]
        if hit:
            scored.append((len(hit), len(''.join(hit)), i + 1))
    if not scored:
        return None, 'no roster entry has any of its words'
    scored.sort(reverse=True)
    if len(scored) > 1 and scored[1][:2] == scored[0][:2]:
        return None, 'ties: ' + ', '.join(str(s[2]) for s in scored if s[:2] == scored[0][:2])
    return scored[0][2], None


def names_in(line):
    """The contract names a line gives: link texts; else a table row's first cell; else a numbered / bulleted item's lead."""
    st = line.strip()
    found = LINK.findall(st)
    if found:
        return found
    if st.startswith('|'):
        cells = [c.strip() for c in st.strip('|').split('|')]
        first = re.sub(r'[*_`]', '', cells[0]) if cells else ''
        if first and not re.fullmatch(r'[-: ]+', first) and first.lower() not in {'contract', 'contracts', 'agreement', 'document', 'file'}:
            return [re.sub(r'^\d+\.\s*', '', first)]
        return []
    m = re.match(r'^(?:\d+\.|[-*•])\s+\**([^:|]{3,140}?)(?:\**\s*(?::|—|–| - )|$)', st)
    if m:
        return [m.group(1)]
    m = re.match(r'^#{2,6}\s+(?:\d+\.\s*)?(.{3,140})$', st)
    if m and ('—' in m.group(1) or ' - ' in m.group(1)):
        return [m.group(1)]
    return []


def count_of(text, asks_count):
    if not asks_count:
        return None
    for pat in (r'^\s*#\s*(\d+)\b', r'\bI (?:found|identified|counted)\s+(\d+)\b', r'\b(\d+)\s+(?:of these\s+)?contracts?\b', r'^\s*(\d+)\b'):
        m = re.search(pat, text, re.M | re.I)
        if m:
            return int(m.group(1))
    return None


def aerospark(run_lines):
    corpus = json.loads(next(l for l in run_lines if l.startswith('CORPUS '))[7:])
    num = {r: i + 1 for i, r in enumerate(corpus['order'])}
    out = []
    for l in run_lines:
        if not l.startswith('ANS '):
            continue
        a = json.loads(l[4:])
        yes, poss, no, review = [], [], [], []
        for f in a.get('findings') or []:
            pt = f.get('point') or ''
            kind = 'no' if NO.search(pt) else 'possible' if POSSIBLE.search(pt) else 'yes'
            for r in f.get('req') or []:
                if r in num:
                    {'yes': yes, 'possible': poss, 'no': no}[kind].append(num[r])
            if kind != 'yes':
                review.append({'kind': kind, 'nums': [num[r] for r in f.get('req') or [] if r in num], 'text': pt[:240]})
        for g in ((a.get('tally') or {}).get('groups') or []):
            for r in g.get('req') or []:
                if r in num:
                    yes.append(num[r])
        t = a.get('tally') or {}
        asks = bool(re.search(r'\bhow many\b', a.get('q') or '', re.I))
        groups = t.get('groups') or []
        # A count over a register tally is its groups' own counts added up (one group: its count; "England 3, England and Wales 1": 4);
        # the tally's total is the whole register (99).
        if groups and all(isinstance(g.get('count'), int) for g in groups):
            cnt = sum(g['count'] for g in groups)
        elif isinstance(t.get('total'), int):
            cnt = t['total']
        else:
            cnt = count_of(a.get('summary') or '', asks)
        y = sorted(set(yes))
        p = [n for n in sorted(set(poss)) if n not in y]
        n_ = [n for n in sorted(set(no)) if n not in y and n not in p]
        out.append({'pass': a['pass'], 'id': a['id'], 'claims': {'yes': y, 'possible': p, 'no': n_, 'count': cnt}, 'review': review})
    return out


def chatgpt(run_lines):
    corpus = json.loads(next(l for l in run_lines if l.startswith('CORPUS '))[7:])
    roster = [squash(f) + ' ' + ' '.join(squash(p) for p in ((corpus.get('parties') or [[]] * len(corpus['files']))[i] or []))
              for i, f in enumerate(corpus['files'])]
    out = []
    rank = {'yes': 0, 'possible': 1, 'no': 2}
    for l in run_lines:
        if not l.startswith('ANS '):
            continue
        a = json.loads(l[4:])
        text = a.get('summary') or ''
        head_kind, best, names, review, unplaced = 'yes', {}, {'yes': [], 'possible': [], 'no': []}, [], []
        for line in text.split('\n'):
            st = line.strip()
            if not st:
                continue
            ns = names_in(st)
            is_head = '|' not in st and not LINK.search(st) and (st.startswith('#') or bool(re.fullmatch(r'\*\*[^*]+\*\*:?', st))
                                                               or (len(st) <= 70 and st[0].isupper() and not st.endswith(('.', ';', ','))))
            if is_head:
                head_kind = 'no' if (HEAD_NO.search(st) or NO.search(st)) else 'possible' if HEAD_POSSIBLE.search(st) else 'yes'
                if not ns:
                    continue
            if not ns:
                continue
            kind = head_kind
            if NO.search(st):
                kind = 'no'
            elif POSSIBLE.search(st) and kind == 'yes':
                kind = 'possible'
            for nm in ns:
                n, why = place_name(nm, roster)
                names[kind].append({'name': nm, 'n': n})
                if n is None:
                    unplaced.append({'list': kind, 'name': nm, 'why': why})
                    continue
                if n not in best or rank[kind] < rank[best[n]]:
                    best[n] = kind          # a contract named twice keeps its strongest claim (yes over possible over no)
            if kind != 'yes':
                review.append({'kind': kind, 'names': ns, 'line': st[:220]})
        asks = bool(re.search(r'\bhow many\b', a.get('q') or '', re.I))
        cl = {'yes': sorted(n for n, k in best.items() if k == 'yes'), 'possible': sorted(n for n, k in best.items() if k == 'possible'),
              'no': sorted(n for n, k in best.items() if k == 'no'), 'count': count_of(text, asks), 'names': names, 'unplaced': unplaced}
        out.append({'pass': a['pass'], 'id': a['id'], 'claims': cl, 'review': review})
    return out


def main():
    run, dst = sys.argv[1], sys.argv[2]
    lines = open(run, encoding='utf-8').read().split('\n')
    corpus = json.loads(next(l for l in lines if l.startswith('CORPUS '))[7:])
    out = chatgpt(lines) if corpus.get('system') in ('chatgpt', 'claude') else aerospark(lines)    # ChatGPT's and Claude's answers are prose
    json.dump(out, open(dst, 'w'), ensure_ascii=False)
    print(f'{len(out)} answers read by code -> {dst}')
    for o in out:
        for u in o['claims'].get('unplaced') or []:
            print(f'  NOT PLACED ({o["id"]}, {u["list"]}): "{u["name"][:80]}" — {u["why"]}')
    if '--compare' in sys.argv:
        old = {(c['pass'], c['id']): c['claims'] for c in json.load(open(sys.argv[sys.argv.index('--compare') + 1]))}
        for o in out:
            c, d = o['claims'], old.get((o['pass'], o['id'])) or {}
            diffs = []
            for k in ('yes', 'possible', 'no'):
                a_, b_ = set(c.get(k) or []), set(d.get(k) or [])
                if a_ != b_:
                    diffs.append(f'{k}: code +{sorted(a_ - b_)} -{sorted(b_ - a_)}')
            if re.match(r'\s*how many', o['id']) or o['id'].startswith('count-'):
                if (c.get('count') or None) != (d.get('count') or None):
                    diffs.append(f'count: code {c.get("count")} vs earlier {d.get("count")}')
            if diffs:
                print(f'  DIFF {o["id"]}: ' + ' | '.join(diffs))


if __name__ == '__main__':
    main()
