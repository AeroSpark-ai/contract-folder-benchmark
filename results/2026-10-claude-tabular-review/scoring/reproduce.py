#!/usr/bin/env python3
"""Re-score the Tabular review run and print it beside plain Claude's run. No accounts, no API calls, standard library only.

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
    ct = [float(claude[q['id']]['claude_seconds']) for q in qs]
    tab = {'score': round(100 * statistics.mean(per[q['id']]['score'] for q in qs), 1), 'key': sum(per[q['id']]['key'] for q in L),
           **{k: sum(per[q['id']][k] for q in L) for k in ('found', 'wrong', 'found_with_possibles', 'wrong_with_possibles')},
           'counts_right': sum(int(per[q['id']]['score']) for q in qs if q['scored_as'] == 'count'), 'lookups_right': sum(int(per[q['id']]['score']) for q in qs if q['scored_as'] in ('value', 'absent')),
           'under_a_minute': sum(x < 60 for x in t), 'median_seconds': round(statistics.median(t), 1), 'total_minutes_rounded': round(sum(t) / 60, 1)}
    cl = {'score': round(100 * statistics.mean(float(claude[q['id']]['claude_score']) for q in qs), 1), 'key': tab['key'],
          **{k: sum(int(claude[q['id']]['claude_' + k]) for q in L) for k in ('found', 'wrong', 'found_with_possibles', 'wrong_with_possibles')},
          'counts_right': sum(int(float(claude[q['id']]['claude_score'])) for q in qs if q['scored_as'] == 'count'), 'lookups_right': sum(int(float(claude[q['id']]['claude_score'])) for q in qs if q['scored_as'] in ('value', 'absent')),
          'under_a_minute': sum(x < 60 for x in ct), 'median_seconds': round(statistics.median(ct), 1), 'total_minutes_rounded': round(sum(ct) / 60, 1)}
    rnd = random.Random(SEED)
    n = len(qs)
    diff = [float(claude[q['id']]['claude_score']) - per[q['id']]['score'] for q in qs]
    v = sorted(100 * sum(diff[rnd.randrange(n)] for _ in range(n)) / n for _ in range(REDRAWS))
    return {'tabular': tab, 'plain_claude': cl, 'plain_minus_tabular': {'range_95': [round(v[250], 1), round(v[9750], 1)], 'plain_ahead_pct': round(100 * sum(x > 0 for x in v) / REDRAWS, 1)}}, claude


def fmt(sec):
    return f'{sec:.0f} s' if sec < 60 else f'{sec / 60:.1f} min'


def tables(qs, per, s, claude):
    t, c, r = s['tabular'], s['plain_claude'], s['plain_minus_tabular']
    h = ['| | Plain Claude | Tabular review |', '|---|---|---|', f"| **Score out of 100** | **{c['score']:.1f}** | **{t['score']:.1f}** |",
         f"| Contracts found, the 30 list questions ({t['key']} in the key) | {c['found']} ({100 * c['found'] / c['key']:.0f}%) | {t['found']} ({100 * t['found'] / t['key']:.0f}%) |",
         f"| Contracts named that are not in the key | {c['wrong']} | {t['wrong']} |",
         f"| Found, with the contracts each hedged as \"possible\" credited too | {c['found_with_possibles']} ({c['wrong_with_possibles']} not in the key) | {t['found_with_possibles']} ({t['wrong_with_possibles']} not in the key) |",
         f"| Counts right (of 5) | {c['counts_right']} | {t['counts_right']} |", f"| Lookups right (of 11) | {c['lookups_right']} | {t['lookups_right']} |",
         f"| Questions answered in under a minute | {c['under_a_minute']} | {t['under_a_minute']} |", f"| Median time per question | {fmt(c['median_seconds'])} | {fmt(t['median_seconds'])} |", '',
         f"Redrawing the 46 questions {REDRAWS:,} times: plain Claude minus Tabular review is {r['range_95'][0]:+.1f} to {r['range_95'][1]:+.1f} in 95% of redraws, and plain Claude is ahead in {r['plain_ahead_pct']:.1f}% of them.", '',
         '| # | Question | Key | Plain Claude | Tabular review | How Tabular answered | Tabular, about |', '|---|---|---|---|---|---|---|']
    for q in qs:
        x, cr = per[q['id']], claude[q['id']]
        if q['scored_as'] == 'files':
            a, b = f"{cr['claude_found']} found, {cr['claude_wrong']} wrong", f"{x['found']} found, {x['wrong']} wrong"
        elif q['scored_as'] == 'count':
            a, b = f"said {cr['claude_count_given']}", f"said {x['count_given']}"
        else:
            a, b = 'right' if float(cr['claude_score']) else 'wrong', 'right' if x['right'] else 'wrong'
        h.append(f"| {q['n']} | {q['asked_of_aerospark']} | {cr['key_contracts']} | {a} | {b} | {x['how']} | {fmt(x['seconds'])} |")
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
        open(os.path.join(sdir, 'headline.md'), 'w', encoding='utf-8').write('# Tabular review beside plain Claude, re-scored from the recorded answers\n\nMade by `python3 results/2026-10-claude-tabular-review/scoring/reproduce.py --write`.\n\n' + text + '\n')
        print('\nwrote scores/')
    if args.check:
        if json.load(open(os.path.join(sdir, 'headline.json'))) != json.loads(json.dumps(s)):
            print('\nDIFFERS from scores/headline.json')
            sys.exit(1)
        print('\nmatches scores/headline.json')


if __name__ == '__main__':
    main()
