#!/usr/bin/env python3
"""Re-score every recorded answer in this run and print the result. No accounts, no API calls, standard library only.

    python3 results/2026-10-aerospark-chatgpt-claude/scoring/reproduce.py            # print the tables
    python3 results/2026-10-aerospark-chatgpt-claude/scoring/reproduce.py --write    # also rewrite scores/ and answers/by_question/
    python3 results/2026-10-aerospark-chatgpt-claude/scoring/reproduce.py --check    # exit 1 if the numbers differ from scores/headline.json (the GitHub check runs this)

Each system's answers (answers/<system>/answers.txt) are read into claims (claims/<system>/claims.json): which contracts each answer names as
a match or as a possible match. The scorer (scoring/score.py) counts them against the key. The one-contract lookups and the questions about
a contract not in the folder are graded by reading (scores/graded_by_reading.json).

Every question counts the same: a list question earns the share of the key's contracts the answer found, a count or a lookup 1 if right and
0 if not, and the score is the average over the 46, out of 100.
"""
import argparse
import csv
import json
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)                       # this run's folder
ROOT = os.path.dirname(os.path.dirname(RUN))     # the repository
sys.path.insert(0, os.path.join(ROOT, 'scoring'))
import score  # noqa: E402

KEY = os.path.join(ROOT, 'benchmark', 'key', 'key.json')
SYSTEMS = [('aerospark', 'AeroSpark'), ('claude', 'Claude'), ('chatgpt', 'ChatGPT')]
NAME = dict(SYSTEMS)
SEED, REDRAWS = 20261028, 10000
KINDS = ['Find every contract with a clause', 'Two or three conditions at once', 'Dates against a stated day', 'The most recent, the shortest notice',
         'By party, by type, notice period, either of two clauses', 'Counts', 'One fact about one named contract', 'A contract that is not in the folder']


def fmt_time(sec):
    if sec < 1:
        return 'under 1 s'
    return f'{sec:.0f} s' if sec < 60 else f'{sec / 60:.1f} min'


def compute():
    qs = json.load(open(os.path.join(ROOT, 'benchmark', 'questions', 'questions.json'), encoding='utf-8'))
    key = {q['id']: q for q in json.load(open(KEY, encoding='utf-8'))['questions']}
    graded = json.load(open(os.path.join(RUN, 'scores', 'graded_by_reading.json'), encoding='utf-8'))['questions']
    res = {}
    for s, _ in SYSTEMS:
        run = score.load_run(os.path.join(RUN, 'answers', s, 'answers.txt'), os.path.join(RUN, 'claims', s, 'claims.json'))
        per = {}
        for q in qs:
            a = run['answers'][q['id']]
            x = {'seconds': round((a.get('ms') or 0) / 1000, 1)}
            if q['scored_as'] in ('files', 'count'):
                x.update(score.score_question(run, key[q['id']]))
                x['score'] = float(x['count_right']) if q['scored_as'] == 'count' else x['found'] / x['key']
            else:
                g = graded[q['id']]['grades'][s]
                x.update({'right': g['right'], 'note': g.get('note', ''), 'score': float(g['right'])})
            per[q['id']] = x
        res[s] = per
    return qs, key, graded, res


def summary(qs, res):
    L = [q for q in qs if q['scored_as'] == 'files']
    out = {}
    for s, _ in SYSTEMS:
        per = res[s]
        t = [per[q['id']]['seconds'] for q in qs]
        out[s] = {'score': round(100 * sum(per[q['id']]['score'] for q in qs) / len(qs), 1), 'questions': len(qs),
                  'list_questions': len(L), 'key': sum(per[q['id']]['key'] for q in L),
                  **{k: sum(per[q['id']][k] for q in L) for k in ('found', 'wrong', 'found_with_possibles', 'wrong_with_possibles')},
                  'counts_right': sum(int(per[q['id']]['score']) for q in qs if q['scored_as'] == 'count'), 'counts': sum(q['scored_as'] == 'count' for q in qs),
                  'lookups_right': sum(int(per[q['id']]['score']) for q in qs if q['scored_as'] in ('value', 'absent')),
                  'lookups': sum(q['scored_as'] in ('value', 'absent') for q in qs),
                  'median_seconds': round(statistics.median(t), 1), 'slowest_seconds': max(t), 'total_seconds': round(sum(t), 1),
                  'time_bands': [sum(x < 60 for x in t), sum(60 <= x < 300 for x in t), sum(300 <= x < 600 for x in t), sum(x >= 600 for x in t)],
                  'by_kind': {k: round(100 * statistics.mean(per[q['id']]['score'] for q in qs if q['kind'] == k), 1) for k in KINDS}}
    # How much the order depends on which questions were asked: the 46 redrawn at random, each redraw the same size.
    rnd = random.Random(SEED)
    sc = {s: [res[s][q['id']]['score'] for q in qs] for s, _ in SYSTEMS}
    n = len(qs)
    redraws = {}
    for other in ('claude', 'chatgpt'):
        v = []
        for _ in range(REDRAWS):
            draw = [rnd.randrange(n) for _ in range(n)]
            v.append(100 * sum(sc['aerospark'][i] - sc[other][i] for i in draw) / n)
        v.sort()
        redraws[f'aerospark_minus_{other}'] = {'range_95': [round(v[250], 1), round(v[9750], 1)], 'aerospark_ahead_pct': round(100 * sum(x > 0 for x in v) / len(v), 1)}
    return out, redraws


def tables(qs, out, redraws):
    cols = ' | '.join(n for _, n in SYSTEMS)
    o = [out[s] for s, _ in SYSTEMS]
    h = ['**The score.** Every question counts the same, out of 100: a list question earns the share of the key\'s contracts the answer found; a count or a lookup is right or not.', '',
         f'| | {cols} |', '|---|---|---|---|',
         '| **Score out of 100** | ' + ' | '.join(f"**{x['score']:.1f}**" for x in o) + ' |',
         f"| Contracts found, the {o[0]['list_questions']} list questions ({o[0]['key']} in the key) | " + ' | '.join(f"{x['found']} ({100 * x['found'] / x['key']:.0f}%)" for x in o) + ' |',
         '| Contracts named that are not in the key | ' + ' | '.join(str(x['wrong']) for x in o) + ' |',
         '| Found, with the contracts each hedged as "possible" credited too | ' + ' | '.join(f"{x['found_with_possibles']} ({x['wrong_with_possibles']} not in the key)" for x in o) + ' |',
         f"| Counts right (of {o[0]['counts']}) | " + ' | '.join(str(x['counts_right']) for x in o) + ' |',
         f"| Lookups right (of {o[0]['lookups']}) | " + ' | '.join(str(x['lookups_right']) for x in o) + ' |',
         '| Median time per question | ' + ' | '.join(fmt_time(x['median_seconds']) for x in o) + ' |',
         '| Slowest question | ' + ' | '.join(fmt_time(x['slowest_seconds']) for x in o) + ' |',
         f"| All {o[0]['questions']} questions | " + ' | '.join(fmt_time(x['total_seconds']) if x['total_seconds'] < 3600 else f"{x['total_seconds'] / 3600:.1f} hours" for x in o) + ' |',
         '', f'**Redrawing the questions.** The {len(qs)} questions redrawn at random {REDRAWS:,} times (each redraw the same size, some questions twice, some not at all), '
         'and the score worked out again each time:', '',
         '| | Difference in score, 95% of redraws | AeroSpark ahead in |', '|---|---|---|']
    for other in ('claude', 'chatgpt'):
        r = redraws[f'aerospark_minus_{other}']
        h.append(f"| AeroSpark minus {NAME[other]} | {r['range_95'][0]:+.1f} to {r['range_95'][1]:+.1f} | {r['aerospark_ahead_pct']:.1f}% of redraws |")
    h += ['', '**By kind of question** (the score out of 100 on the questions of each kind)', '', f'| Kind | Questions | {cols} |', '|---|---|---|---|---|']
    for k in KINDS:
        h.append(f"| {k} | {sum(q['kind'] == k for q in qs)} | " + ' | '.join(f"{x['by_kind'][k]:.1f}" for x in o) + ' |')
    h += ['', '**Time per question**', '', '| | Under 1 min | 1 to 5 min | 5 to 10 min | Over 10 min |', '|---|---|---|---|---|']
    for s, n in SYSTEMS:
        h.append(f'| {n} | ' + ' | '.join(str(b) for b in out[s]['time_bands']) + ' |')
    return '\n'.join(h)


# ---- the question pages

def contract_names():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'benchmark', 'contracts', 'contracts.csv'), encoding='utf-8')))
    return {r['aerospark_id']: r['key_name'] for r in rows}


def bullet_files(names):
    return ['- ' + n for n in sorted(names)] or ['- none']


def scored_lists(run, qid, key_files, skip):
    """In the key and named, named but not in the key, hedged as possible, missed; the question's left-out contracts in none of them."""
    yes, poss = score.named(run, qid, 'yes') - skip, score.named(run, qid, 'possible') - skip
    return yes & key_files, yes - key_files, poss - yes, key_files - yes - poss


def page(q, k, graded, res, runs, ids):
    qid = q['id']
    t = k['truth']
    h = [f"# {q['n']:02d}. {qid}", '', f"> **{q['asked_of_aerospark']}**", '', f"{q['kind']} · scored as: {q['scored_as']} · key from: {q['key_from']}", '',
         'ChatGPT and Claude were asked the same words after: *In my Google Drive shared drive "Benchmark Test" (all its folders):*', '', '## The key', '',
         f"From {k['source']}." + (f" {t['note']}" if t.get('note') else ''), '']
    key_files = set()
    if t['type'] == 'files':
        key_files = set(t['files']) & set(runs['aerospark']['names'])
        h += [f'**{len(key_files)} contract(s).**' + (f" Left out of this question (the labels cannot settle them; naming one is neither found nor wrong): {len(t['skip'])}." if t.get('skip') else ''),
              '', '<details><summary>The key</summary>', '', *bullet_files(key_files), '', '</details>', '']
    else:
        h += [f"**{graded[qid]['key']}**" + (f" (the contract it is about, `{t['contract_outside_folder']}`, is not in the folder)" if t['type'] == 'absent' else ''), '']
    for s, name in SYSTEMS:
        run, x = runs[s], res[s][qid]
        a = run['answers'][qid]
        h += [f"## {name}: {fmt_time(x['seconds'])}", '']
        if s == 'aerospark':
            h += [(a.get('summary') or '').strip(), '']
            for note in (a.get('clauseNote'), a.get('scaleNote')):
                if note:
                    h += [f'*{note}*', '']
            if a.get('findings'):
                h += ['**What the answer points to, with the contracts each point cites:**', '']
                for f in a['findings']:
                    cited = [ids[r] for r in (f.get('req') or []) if r in ids]
                    h.append(f"- {f.get('point') or ''}" + ('  \n  *' + '; '.join(cited) + '*' if cited else ''))
                h.append('')
            for g in ((a.get('tally') or {}).get('groups') or []):
                h += [f"**{g['label']}: {g['count']}**", '', *bullet_files(ids[r] for r in (g.get('req') or []) if r in ids), '']
        else:
            h += [f"<details><summary>{name}'s answer, verbatim (Drive links removed)</summary>", '', (a.get('summary') or '').strip(), '', '</details>', '']
        if q['scored_as'] in ('files', 'count'):
            found, wrong, poss, missed = scored_lists(run, qid, key_files, set(t.get('skip') or []))
            if q['scored_as'] == 'count':
                h += [f"**Scored:** the count given is {x['count_given']}; the key has {x['key']}: **{'right' if x['count_right'] else 'not right'}**.", '']
            else:
                h += [f"**Scored:** named as a match {len(found) + len(wrong)}: **{len(found)} of the {x['key']} in the key**, {len(wrong)} not in the key.", '']
            h += [f'<details><summary>In the key and named ({len(found)}), named but not in the key ({len(wrong)}), possible ({len(poss)}), missed ({len(missed)})</summary>', '',
                  '**In the key and named**', '', *bullet_files(found), '', '**Named but not in the key**', '', *bullet_files(wrong), '',
                  '**Hedged as possible**', '', *bullet_files(poss), '', '**In the key, not named**', '', *bullet_files(missed), '', '</details>', '']
        else:
            h += [f"**Graded by reading:** {'right' if x['right'] else 'wrong'}" + (f": {x['note']}" if x['note'] else '') + '.', '']
    return '\n'.join(h)


def write(qs, key, graded, res, out, redraws):
    sdir = os.path.join(RUN, 'scores')
    json.dump({'systems': out, 'redraws': redraws}, open(os.path.join(sdir, 'headline.json'), 'w'), indent=1)
    open(os.path.join(sdir, 'headline.md'), 'w', encoding='utf-8').write(
        '# The result, re-scored from the recorded answers\n\nMade by `python3 results/2026-10-aerospark-chatgpt-claude/scoring/reproduce.py --write`. '
        'The lookups are graded by reading: [graded_by_reading.md](graded_by_reading.md). Every question: [per_question.csv](per_question.csv).\n\n'
        + tables(qs, out, redraws) + '\n')
    with open(os.path.join(sdir, 'per_question.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        head = ['n', 'id', 'kind', 'scored_as', 'key_from', 'key_contracts']
        for s, _ in SYSTEMS:
            head += [f'{s}_{c}' for c in ('score', 'found', 'wrong', 'found_with_possibles', 'wrong_with_possibles', 'count_given', 'seconds', 'note')]
        w.writerow(head)
        for q in qs:
            row = [q['n'], q['id'], q['kind'], q['scored_as'], q['key_from'], q['key_contracts']]
            for s, _ in SYSTEMS:
                x = res[s][q['id']]
                if q['scored_as'] in ('files', 'count'):
                    row += [round(x['score'], 4), x['found'], x['wrong'], x['found_with_possibles'], x['wrong_with_possibles'], x.get('count_given', ''), x['seconds'], '']
                else:
                    row += [x['score'], '', '', '', '', '', x['seconds'], '; '.join(v for v in ('graded by reading: ' + ('right' if x['right'] else 'wrong'), x['note']) if v)]
            w.writerow(row)
    g = ['# The questions graded by reading', '',
         'The list and count questions are scored by code ([headline.md](headline.md)). Claude graded these by reading each answer against the key, the same rule for every '
         'system: the expected fact stated, a date in any form. The grades are ours and can be challenged ([CHALLENGE.md](../../../benchmark/docs/CHALLENGE.md)).', '',
         '| # | Question | Key | ' + ' | '.join(n for _, n in SYSTEMS) + ' |', '|---|---|---|---|---|---|']
    for q in qs:
        if q['scored_as'] in ('value', 'absent'):
            cells = []
            for s, _ in SYSTEMS:
                x = res[s][q['id']]
                cells.append(('right' if x['right'] else '**wrong**') + (f": {x['note']}" if x['note'] else ''))
            g.append(f"| {q['n']} | {q['id']} | {graded[q['id']]['key']} | " + ' | '.join(cells) + ' |')
    g.append('| | **Right** | | ' + ' | '.join(f"**{out[s]['lookups_right']} of {out[s]['lookups']}**" for s, _ in SYSTEMS) + ' |')
    g += ['', '## The counts', '', 'Scored by code on the number each answer gives ([claims/](../claims/README.md) holds the number read from each answer).', '',
          '| # | Question | Key | ' + ' | '.join(n for _, n in SYSTEMS) + ' |', '|---|---|---|---|---|---|']
    for q in qs:
        if q['scored_as'] == 'count':
            g.append(f"| {q['n']} | {q['id']} | {res['aerospark'][q['id']]['key']} | "
                     + ' | '.join(f"{res[s][q['id']]['count_given']}" + ('' if res[s][q['id']]['count_right'] else ' (not right)') for s, _ in SYSTEMS) + ' |')
    g.append('| | **Right** | | ' + ' | '.join(f"**{out[s]['counts_right']} of {out[s]['counts']}**" for s, _ in SYSTEMS) + ' |')
    open(os.path.join(sdir, 'graded_by_reading.md'), 'w', encoding='utf-8').write('\n'.join(g) + '\n')
    # the question pages
    ids = contract_names()
    runs = {s: score.load_run(os.path.join(RUN, 'answers', s, 'answers.txt'), os.path.join(RUN, 'claims', s, 'claims.json')) for s, _ in SYSTEMS}
    pdir = os.path.join(RUN, 'answers', 'by_question')
    os.makedirs(pdir, exist_ok=True)
    idx = ['# The answers, question by question', '',
           "One page per question: the words asked, the key, each system's answer and which contracts it got right, got wrong and missed. "
           'For a list question the cell shows the contracts found of the key, and the contracts named that are not in the key.', '',
           '| # | Question | Key | ' + ' | '.join(n for _, n in SYSTEMS) + ' |', '|---|---|---|---|---|---|']
    for q in qs:
        fname = f"q{q['n']:02d}_{q['id']}.md"
        open(os.path.join(pdir, fname), 'w', encoding='utf-8').write(page(q, key[q['id']], graded, res, runs, ids) + '\n')
        cells = []
        for s, _ in SYSTEMS:
            x = res[s][q['id']]
            if q['scored_as'] == 'files':
                cells.append(f"{x['found']}/{x['key']}" + (f" +{x['wrong']} wrong" if x['wrong'] else ''))
            elif q['scored_as'] == 'count':
                cells.append(f"{x['count_given']} {'right' if x['count_right'] else 'not right'}")
            else:
                cells.append('right' if x['right'] else 'wrong')
        kcell = res['aerospark'][q['id']]['key'] if q['scored_as'] in ('files', 'count') else graded[q['id']]['key']
        idx.append(f"| {q['n']} | [{q['asked_of_aerospark']}]({fname}) | {kcell} | " + ' | '.join(cells) + ' |')
    open(os.path.join(pdir, 'README.md'), 'w', encoding='utf-8').write('\n'.join(idx) + '\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    qs, key, graded, res = compute()
    out, redraws = summary(qs, res)
    print(tables(qs, out, redraws))
    if args.write:
        write(qs, key, graded, res, out, redraws)
        print('\nwrote scores/ and answers/by_question/')
    if args.check:
        saved = json.load(open(os.path.join(RUN, 'scores', 'headline.json')))
        if saved != json.loads(json.dumps({'systems': out, 'redraws': redraws})):
            print('\nDIFFERS from scores/headline.json')
            sys.exit(1)
        print('\nmatches scores/headline.json')


if __name__ == '__main__':
    main()
