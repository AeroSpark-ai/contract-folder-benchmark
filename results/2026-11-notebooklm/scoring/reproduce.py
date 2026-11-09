#!/usr/bin/env python3
"""Re-score the NotebookLM run and print it beside the other four systems. No accounts, no API calls, standard library only.

    python3 results/2026-11-notebooklm/scoring/reproduce.py            # print the tables
    python3 results/2026-11-notebooklm/scoring/reproduce.py --write    # also rewrite scores/
    python3 results/2026-11-notebooklm/scoring/reproduce.py --check    # exit 1 if the numbers differ from scores/headline.json

The rules are the benchmark's: every question counts the same, a list question earns the share of the key's contracts the answer names as a match, a count or a lookup 1 if
right and 0 if not. The lookups and the questions about a contract not in the folder are graded by reading (scores/graded_by_reading.json).
"""
import argparse
import csv
import importlib.util
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

MAIN = os.path.join(ROOT, 'results', '2026-10-aerospark-chatgpt-claude', 'scores', 'per_question.csv')
TABULAR = os.path.join(ROOT, 'results', '2026-10-claude-tabular-review', 'scoring', 'reproduce.py')
SEED, REDRAWS = 20261028, 10000


def compute():
    qs = json.load(open(os.path.join(ROOT, 'benchmark', 'questions', 'questions.json'), encoding='utf-8'))
    key = {q['id']: q for q in json.load(open(os.path.join(ROOT, 'benchmark', 'key', 'key.json'), encoding='utf-8'))['questions']}
    graded = json.load(open(os.path.join(RUN, 'scores', 'graded_by_reading.json'), encoding='utf-8'))['questions']
    run = score.load_run(os.path.join(RUN, 'answers', 'answers.txt'), os.path.join(RUN, 'claims', 'claims.json'))
    per = {}
    for q in qs:
        a = run['answers'][q['id']]
        x = {'seconds': round((a.get('ms') or 0) / 1000, 1), 'reasked': bool(a.get('reasked'))}
        if q['scored_as'] in ('files', 'count'):
            x.update(score.score_question(run, key[q['id']]))
            x['score'] = float(x['count_right']) if q['scored_as'] == 'count' else x['found'] / x['key']
        else:
            g = graded[q['id']]
            x.update({'right': g['right'], 'note': g.get('note', ''), 'score': float(g['right'])})
        per[q['id']] = x
    return qs, per


def tabular_per():
    spec = importlib.util.spec_from_file_location('tabular_run', TABULAR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compute()[1]


def totals(qs, scores, found, secs):
    L = [q for q in qs if q['scored_as'] == 'files']
    t = [secs(q) for q in qs]
    return {'score': round(100 * statistics.mean(scores(q) for q in qs), 1), 'key': sum(found(q, 'key') for q in L),
            **{k: sum(found(q, k) for q in L) for k in ('found', 'wrong', 'found_with_possibles', 'wrong_with_possibles')},
            'counts_right': sum(int(scores(q)) for q in qs if q['scored_as'] == 'count'),
            'lookups_right': sum(int(scores(q)) for q in qs if q['scored_as'] in ('value', 'absent')),
            'under_a_minute': sum(x < 60 for x in t), 'median_seconds': round(statistics.median(t), 1), 'total_minutes_rounded': round(sum(t) / 60, 1)}


def redraw(a, b):
    rnd = random.Random(SEED)
    n = len(a)
    diff = [x - y for x, y in zip(a, b)]
    v = sorted(100 * sum(diff[rnd.randrange(n)] for _ in range(n)) / n for _ in range(REDRAWS))
    return {'range_95': [round(v[250], 1), round(v[9750], 1)], 'first_ahead_pct': round(100 * sum(x > 0 for x in v) / REDRAWS, 1)}


def summary(qs, per):
    main = {r['id']: r for r in csv.DictReader(open(MAIN, encoding='utf-8'))}
    tab = tabular_per()

    def other(s):
        return totals(qs, lambda q: float(main[q['id']][s + '_score']), lambda q, k: int(main[q['id']][f'{s}_{k}']) if k != 'key' else int(main[q['id']]['key_contracts']),
                      lambda q: float(main[q['id']][s + '_seconds']))

    nb = totals(qs, lambda q: per[q['id']]['score'], lambda q, k: per[q['id']][k], lambda q: per[q['id']]['seconds'])
    tb = totals(qs, lambda q: tab[q['id']]['score'], lambda q, k: tab[q['id']][k], lambda q: tab[q['id']]['seconds'])
    mine = [per[q['id']]['score'] for q in qs]
    return {'aerospark': other('aerospark'), 'plain_claude': other('claude'), 'tabular': tb, 'notebooklm': nb, 'chatgpt': other('chatgpt'),
            'plain_claude_minus_notebooklm': redraw([float(main[q['id']]['claude_score']) for q in qs], mine),
            'notebooklm_minus_chatgpt': redraw(mine, [float(main[q['id']]['chatgpt_score']) for q in qs])}, main, tab


def fmt(sec):
    if sec < 1:
        return 'under 1 s'
    return f'{sec:.0f} s' if sec < 60 else f'{sec / 60:.1f} min'


def tables(qs, per, s, main, tab):
    order = [('aerospark', 'AeroSpark'), ('plain_claude', 'Plain Claude'), ('tabular', 'Tabular review'), ('notebooklm', 'NotebookLM'), ('chatgpt', 'ChatGPT')]
    o = [s[k] for k, _ in order]

    def line(label, cell):
        return f'| {label} | ' + ' | '.join(cell(x) for x in o) + ' |'

    r1, r2 = s['plain_claude_minus_notebooklm'], s['notebooklm_minus_chatgpt']
    h = ['| | ' + ' | '.join(n for _, n in order) + ' |', '|---|---|---|---|---|---|', line('**Score out of 100**', lambda x: f"**{x['score']:.1f}**"),
         line(f"Contracts found, the 30 list questions ({o[0]['key']} in the key)", lambda x: f"{x['found']} ({100 * x['found'] / x['key']:.0f}%)"),
         line('Contracts named that are not in the key', lambda x: str(x['wrong'])),
         line('Found, with the contracts each hedged as "possible" credited too', lambda x: f"{x['found_with_possibles']} ({x['wrong_with_possibles']} not in the key)"),
         line('Counts right (of 5)', lambda x: str(x['counts_right'])), line('Lookups right (of 11)', lambda x: str(x['lookups_right'])),
         line('Questions answered in under a minute', lambda x: str(x['under_a_minute'])), line('Median time per question', lambda x: fmt(x['median_seconds'])), '',
         f"Redrawing the 46 questions {REDRAWS:,} times: plain Claude minus NotebookLM is {r1['range_95'][0]:+.1f} to {r1['range_95'][1]:+.1f} in 95% of redraws, with plain Claude ahead in "
         f"{r1['first_ahead_pct']:.1f}% of them; NotebookLM minus ChatGPT is {r2['range_95'][0]:+.1f} to {r2['range_95'][1]:+.1f}, with NotebookLM ahead in {r2['first_ahead_pct']:.1f}%. "
         'Every pair: [COMPARISON.md](../../COMPARISON.md).', '',
         'Each cell is the result, then the time to answer. "Re-ask" marks the two questions NotebookLM was asked again; their time includes both asks.', '',
         '| # | Question | Key | AeroSpark | Plain Claude | Tabular review | NotebookLM | ChatGPT |', '|---|---|---|---|---|---|---|---|']

    def main_cell(q, row, s):
        if q['scored_as'] == 'files':
            a = f"{row[s + '_found']} found, {row[s + '_wrong']} wrong"
        elif q['scored_as'] == 'count':
            a = f"said {row[s + '_count_given']}"
        else:
            a = 'right' if float(row[s + '_score']) else 'wrong'
        return f"{a}, {fmt(float(row[s + '_seconds']))}"

    def cell(q, x):
        if q['scored_as'] == 'files':
            a = f"{x['found']} found, {x['wrong']} wrong"
        elif q['scored_as'] == 'count':
            a = f"said {x['count_given']}"
        else:
            a = 'right' if x['right'] else 'wrong'
        return f"{a}, {fmt(x['seconds'])}"

    for q in qs:
        x, row = per[q['id']], main[q['id']]
        h.append(f"| {q['n']} | {q['asked_of_aerospark']} | {row['key_contracts']} | {main_cell(q, row, 'aerospark')} | {main_cell(q, row, 'claude')} | {cell(q, tab[q['id']])} | "
                 f"{cell(q, x)}{' (re-ask)' if x['reasked'] else ''} | {main_cell(q, row, 'chatgpt')} |")
    return '\n'.join(h)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    qs, per = compute()
    s, main_rows, tab = summary(qs, per)
    text = tables(qs, per, s, main_rows, tab)
    print(text)
    sdir = os.path.join(RUN, 'scores')
    if args.write:
        json.dump(s, open(os.path.join(sdir, 'headline.json'), 'w'), indent=1)
        open(os.path.join(sdir, 'headline.md'), 'w', encoding='utf-8').write('# NotebookLM beside the other four systems, re-scored from the recorded answers\n\nMade by `python3 results/2026-11-notebooklm/scoring/reproduce.py --write`.\n\n' + text + '\n')
        print('\nwrote scores/')
    if args.check:
        if json.load(open(os.path.join(sdir, 'headline.json'))) != json.loads(json.dumps(s)):
            print('\nDIFFERS from scores/headline.json')
            sys.exit(1)
        print('\nmatches scores/headline.json')


if __name__ == '__main__':
    main()
