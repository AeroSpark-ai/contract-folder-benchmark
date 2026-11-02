#!/usr/bin/env python3
"""Re-score the Tabular review run and print it beside the main run's three systems. No accounts, no API calls, standard library only.

    python3 results/2026-10-claude-tabular-review/scoring/reproduce.py            # print the tables
    python3 results/2026-10-claude-tabular-review/scoring/reproduce.py --write    # also rewrite scores/
    python3 results/2026-10-claude-tabular-review/scoring/reproduce.py --check    # exit 1 if the numbers differ from scores/headline.json

The rules are the benchmark's: every question counts the same, a list question earns the share of the key's contracts the answer names as a match, a count or a lookup 1 if
right and 0 if not. The lookups and the questions about a contract not in the folder are graded by reading (scores/graded_by_reading.json).
"""
import argparse
import csv
import json
import os
import random
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(RUN))
sys.path.insert(0, os.path.join(ROOT, 'scoring'))
import score  # noqa: E402

CLAUDE = os.path.join(ROOT, 'results', '2026-10-aerospark-chatgpt-claude', 'scores', 'per_question.csv')
SEED, REDRAWS = 20261028, 10000


def compute():
    qs = json.load(open(os.path.join(ROOT, 'benchmark', 'questions', 'questions.json'), encoding='utf-8'))
    key = {q['id']: q for q in json.load(open(os.path.join(ROOT, 'benchmark', 'key', 'key.json'), encoding='utf-8'))['questions']}
    graded = json.load(open(os.path.join(RUN, 'scores', 'graded_by_reading.json'), encoding='utf-8'))['questions']
    run = score.load_run(os.path.join(RUN, 'answers', 'answers.txt'), os.path.join(RUN, 'claims', 'claims.json'))
    per = {}
    for q in qs:
        a = run['answers'][q['id']]
        x = {'seconds': round((a.get('ms') or 0) / 1000, 1), 'how': a.get('how'), 'follow_up': a.get('followUp')}
        if q['scored_as'] in ('files', 'count'):
            x.update(score.score_question(run, key[q['id']]))
            x['score'] = float(x['count_right']) if q['scored_as'] == 'count' else x['found'] / x['key']
        else:
            g = graded[q['id']]
            x.update({'right': g['right'], 'note': g.get('note', ''), 'score': float(g['right'])})
        per[q['id']] = x
    return qs, per


def summary(qs, per):
    claude = {r['id']: r for r in csv.DictReader(open(CLAUDE, encoding='utf-8'))}
    L = [q for q in qs if q['scored_as'] == 'files']
    t = [per[q['id']]['seconds'] for q in qs]
    tab ={'score': round(100 * statistics.mean(per[q['id']]['score'] for q in qs), 1), 'key': sum(per[q['id']]['key'] for q in L),
           **{k: sum(per[q['id']][k] for q in L) for k in ('found', 'wrong', 'found_with_possibles', 'wrong_with_possibles')},
           'counts_right': sum(int(per[q['id']]['score']) for q in qs if q['scored_as'] == 'count'), 'lookups_right': sum(int(per[q['id']]['score']) for q in qs if q['scored_as'] in ('value', 'absent')),
           'under_a_minute': sum(x < 60 for x in t), 'median_seconds': round(statistics.median(t), 1), 'total_minutes_rounded': round(sum(t) / 60, 1)}

    def other(s):
        ot = [float(claude[q['id']][s + '_seconds']) for q in qs]
        return {'score': round(100 * statistics.mean(float(claude[q['id']][s + '_score']) for q in qs), 1), 'key': tab['key'],
                **{k: sum(int(claude[q['id']][f'{s}_{k}']) for q in L) for k in ('found', 'wrong', 'found_with_possibles', 'wrong_with_possibles')},
                'counts_right': sum(int(float(claude[q['id']][s + '_score'])) for q in qs if q['scored_as'] == 'count'), 'lookups_right': sum(int(float(claude[q['id']][s + '_score'])) for q in qs if q['scored_as'] in ('value', 'absent')),
                'under_a_minute': sum(x < 60 for x in ot), 'median_seconds': round(statistics.median(ot), 1), 'total_minutes_rounded': round(sum(ot) / 60, 1)}

    rnd = random.Random(SEED)
    n = len(qs)
    diff = [float(claude[q['id']]['claude_score']) - per[q['id']]['score'] for q in qs]
    v = sorted(100 * sum(diff[rnd.randrange(n)] for _ in range(n)) / n for _ in range(REDRAWS))
    return {'aerospark': other('aerospark'), 'plain_claude': other('claude'), 'tabular': tab, 'chatgpt': other('chatgpt'),
            'plain_minus_tabular': {'range_95': [round(v[250], 1), round(v[9750], 1)], 'plain_ahead_pct': round(100 * sum(x > 0 for x in v) / REDRAWS, 1)}}, claude


def fmt(sec):
    if sec < 1:
        return 'under 1 s'
    return f'{sec:.0f} s' if sec < 60 else f'{sec / 60:.1f} min'


def tables(qs, per, s, claude):
    t, c, r = s['tabular'], s['plain_claude'], s['plain_minus_tabular']
    o = [s['aerospark'], c, t, s['chatgpt']]

    def line(label, cell):
        return f'| {label} | ' + ' | '.join(cell(x) for x in o) + ' |'

    h = ['| | AeroSpark | Plain Claude | Tabular review | ChatGPT |', '|---|---|---|---|---|', line('**Score out of 100**', lambda x: f"**{x['score']:.1f}**"),
         line(f"Contracts found, the 30 list questions ({t['key']} in the key)", lambda x: f"{x['found']} ({100 * x['found'] / x['key']:.0f}%)"),
         line('Contracts named that are not in the key', lambda x: str(x['wrong'])),
         line('Found, with the contracts each hedged as "possible" credited too', lambda x: f"{x['found_with_possibles']} ({x['wrong_with_possibles']} not in the key)"),
         line('Counts right (of 5)', lambda x: str(x['counts_right'])), line('Lookups right (of 11)', lambda x: str(x['lookups_right'])),
         line('Questions answered in under a minute', lambda x: str(x['under_a_minute'])), line('Median time per question', lambda x: fmt(x['median_seconds'])), '',
         f"Redrawing the 46 questions {REDRAWS:,} times: plain Claude minus Tabular review is {r['range_95'][0]:+.1f} to {r['range_95'][1]:+.1f} in 95% of redraws, and plain Claude is ahead in {r['plain_ahead_pct']:.1f}% of them. "
         'Every pair: [COMPARISON.md](../../COMPARISON.md).', '',
         "Each cell is the result, then the time to answer. Tabular review's times are rounded.", '',
         '| # | Question | Key | AeroSpark | Plain Claude | Tabular review | ChatGPT | How Tabular answered |', '|---|---|---|---|---|---|---|---|']

    def cell(q, row, s):
        if q['scored_as'] == 'files':
            a = f"{row[s + '_found']} found, {row[s + '_wrong']} wrong"
        elif q['scored_as'] == 'count':
            a = f"said {row[s + '_count_given']}"
        else:
            a = 'right' if float(row[s + '_score']) else 'wrong'
        return f"{a}, {fmt(float(row[s + '_seconds']))}"

    for q in qs:
        x, cr = per[q['id']], claude[q['id']]
        if q['scored_as'] == 'files':
            b = f"{x['found']} found, {x['wrong']} wrong"
        elif q['scored_as'] == 'count':
            b = f"said {x['count_given']}"
        else:
            b = 'right' if x['right'] else 'wrong'
        h.append(f"| {q['n']} | {q['asked_of_aerospark']} | {cr['key_contracts']} | {cell(q, cr, 'aerospark')} | {cell(q, cr, 'claude')} | {b}, {fmt(x['seconds'])} | {cell(q, cr, 'chatgpt')} | {x['how']} |")
    return '\n'.join(h)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    qs, per = compute()
    s, claude = summary(qs, per)
    text = tables(qs, per, s, claude)
    print(text)
    sdir = os.path.join(RUN, 'scores')
    if args.write:
        json.dump(s, open(os.path.join(sdir, 'headline.json'), 'w'), indent=1)
        open(os.path.join(sdir, 'headline.md'), 'w', encoding='utf-8').write('# Tabular review beside the other three systems, re-scored from the recorded answers\n\nMade by `python3 results/2026-10-claude-tabular-review/scoring/reproduce.py --write`.\n\n' + text + '\n')
        print('\nwrote scores/')
    if args.check:
        if json.load(open(os.path.join(sdir, 'headline.json'))) != json.loads(json.dumps(s)):
            print('\nDIFFERS from scores/headline.json')
            sys.exit(1)
        print('\nmatches scores/headline.json')


if __name__ == '__main__':
    main()
