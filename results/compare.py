#!/usr/bin/env python3
"""Put the six systems side by side, re-scored from each run's recorded answers. No accounts, no API calls, standard library only.

    python3 results/compare.py            # print the page
    python3 results/compare.py --write    # also rewrite results/COMPARISON.md and results/comparison.json
    python3 results/compare.py --check    # exit 1 if the numbers differ from results/comparison.json (the GitHub check runs this)

The scoring is each run's own scoring/reproduce.py, so a figure here cannot differ from the figure in that run's folder.
"""
import argparse
import importlib.util
import json
import os
import random
import statistics
import sys

RESULTS = os.path.dirname(os.path.abspath(__file__))
MAIN_RUN = '2026-10-aerospark-chatgpt-claude'
TABULAR_RUN = '2026-10-claude-tabular-review'
NOTEBOOKLM_RUN = '2026-11-notebooklm'
COPILOT_RUN = '2026-11-copilot-researcher'
SEED, REDRAWS = 20261028, 10000
SYSTEMS = [('aerospark', 'AeroSpark'), ('claude', 'Plain Claude'), ('tabular', 'Tabular review'), ('notebooklm', 'NotebookLM'), ('chatgpt', 'ChatGPT'),
           ('copilot', 'Copilot Researcher')]
# Every pair, in the order of SYSTEMS.
PAIRS = [(a, b) for i, (a, _) in enumerate(SYSTEMS) for b, _ in SYSTEMS[i + 1:]]
NAME = dict(SYSTEMS)
# Tabular review's per-question times are rounded and leave out moving between questions, so its total comes from the clock (its README says how).
TABULAR_TOTAL = 'About 85 minutes, plus about 30 blocked'


def load(run, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(RESULTS, run, 'scoring', 'reproduce.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fmt(sec):
    if sec < 1:
        return 'under 1 s'
    return f'{sec:.0f} s' if sec < 60 else f'{sec / 60:.1f} min'


def total(sec):
    return f'{sec / 60:.0f} minutes' if sec < 3600 else f'{sec / 3600:.1f} hours'


def compute():
    main_run, tabular, notebooklm = load(MAIN_RUN, 'main_run'), load(TABULAR_RUN, 'tabular_run'), load(NOTEBOOKLM_RUN, 'notebooklm_run')
    copilot = load(COPILOT_RUN, 'copilot_run')
    qs, _, _, res = main_run.compute()
    main_out, main_redraws = main_run.summary(qs, res)
    _, tab_per = tabular.compute()
    tab_summary, _ = tabular.summary(qs, tab_per)
    _, nb_per = notebooklm.compute()
    nb_summary, _, _ = notebooklm.summary(qs, nb_per)
    _, cp_per = copilot.compute()
    cp_summary, _, _ = copilot.summary(qs, cp_per)
    per = {'aerospark': res['aerospark'], 'claude': res['claude'], 'tabular': tab_per, 'notebooklm': nb_per, 'chatgpt': res['chatgpt'], 'copilot': cp_per}
    L = [q for q in qs if q['scored_as'] == 'files']
    systems = {}
    for s, _ in SYSTEMS:
        p = per[s]
        t = [p[q['id']]['seconds'] for q in qs]
        systems[s] = {'score': round(100 * statistics.mean(p[q['id']]['score'] for q in qs), 1), 'key': sum(p[q['id']]['key'] for q in L),
                      **{k: sum(p[q['id']][k] for q in L) for k in ('found', 'wrong', 'found_with_possibles', 'wrong_with_possibles')},
                      'counts_right': sum(int(p[q['id']]['score']) for q in qs if q['scored_as'] == 'count'),
                      'lookups_right': sum(int(p[q['id']]['score']) for q in qs if q['scored_as'] in ('value', 'absent')),
                      'median_seconds': round(statistics.median(t), 1), 'slowest_seconds': max(t), 'total_seconds': round(sum(t), 1),
                      'time_bands': [sum(x < 60 for x in t), sum(60 <= x <= 300 for x in t), sum(300 < x <= 600 for x in t), sum(x > 600 for x in t)],
                      'by_kind': {k: round(100 * statistics.mean(p[q['id']]['score'] for q in qs if q['kind'] == k), 1) for k in main_run.KINDS}}
    # The pairs each run already publishes keep their figures; the others are drawn the same way.
    redraws = {pair: {'range_95': main_redraws[pair]['range_95'], 'ahead_pct': main_redraws[pair]['aerospark_ahead_pct']} for pair in ('aerospark_minus_claude', 'aerospark_minus_chatgpt')}
    redraws['claude_minus_tabular'] = {'range_95': tab_summary['plain_minus_tabular']['range_95'], 'ahead_pct': tab_summary['plain_minus_tabular']['plain_ahead_pct']}
    for pair, src in (('claude_minus_notebooklm', 'plain_claude_minus_notebooklm'), ('notebooklm_minus_chatgpt', 'notebooklm_minus_chatgpt')):
        redraws[pair] = {'range_95': nb_summary[src]['range_95'], 'ahead_pct': nb_summary[src]['first_ahead_pct']}
    redraws['chatgpt_minus_copilot'] = {'range_95': cp_summary['chatgpt_minus_copilot']['range_95'], 'ahead_pct': cp_summary['chatgpt_minus_copilot']['first_ahead_pct']}
    n = len(qs)
    for a, b in PAIRS:
        if f'{a}_minus_{b}' in redraws:
            continue
        rnd = random.Random(SEED)
        diff = [per[a][q['id']]['score'] - per[b][q['id']]['score'] for q in qs]
        v = sorted(100 * sum(diff[rnd.randrange(n)] for _ in range(n)) / n for _ in range(REDRAWS))
        redraws[f'{a}_minus_{b}'] = {'range_95': [round(v[250], 1), round(v[9750], 1)], 'ahead_pct': round(100 * sum(x > 0 for x in v) / REDRAWS, 1)}
    systems['copilot']['named_not_in_folder'] = cp_summary['copilot']['named_not_in_folder']
    return {'systems': systems, 'redraws': redraws}, qs, main_run.KINDS


def row(label, cells):
    return f'| {label} | ' + ' | '.join(str(c) for c in cells) + ' |'


def page(data, qs, kinds):
    s = [data['systems'][k] for k, _ in SYSTEMS]
    cols = ' | '.join(n for _, n in SYSTEMS)
    sep = '|---' * (len(SYSTEMS) + 1) + '|'
    h = ['# All six systems side by side', '',
         'The same 46 questions about the same folder of 99 contracts, against the same answer key. **We build [AeroSpark](https://www.aerospark.ai/l/gh-comparison), a contract repository**, so every figure here is re-made from the recorded answers by `results/compare.py`.', '',
         f'| | {cols} |', sep,
         row('**Score out of 100**', [f"**{x['score']:.1f}**" for x in s]),
         row(f"Contracts found, the 30 list questions ({s[0]['key']} in the key)", [f"{x['found']} ({100 * x['found'] / x['key']:.0f}%)" for x in s]),
         row('Contracts named that are not in the key', [x['wrong'] for x in s]),
         row('Found, with the contracts each hedged as "possible" credited too', [f"{x['found_with_possibles']} ({x['wrong_with_possibles']} not in the key)" for x in s]),
         row('Counts right (of 5)', [x['counts_right'] for x in s]),
         row('Lookups right (of 11)', [x['lookups_right'] for x in s]),
         row('Median wait per question', [fmt(x['median_seconds']) for x in s]),
         row('Slowest question', [fmt(x['slowest_seconds']) for x in s]),
         row('All 46 questions', [TABULAR_TOTAL if k == 'tabular' else total(data['systems'][k]['total_seconds']) for k, _ in SYSTEMS]), '',
         '**The times are how long a person waits**, from asking to the finished answer. AeroSpark reads each contract when it is added, before any question is asked. Tabular review reads every contract when a question needs a new column, and that wait counts against the question. '
         'NotebookLM had the 99 contracts added to one notebook once, before any question; adding them is not in its times. Plain Claude and ChatGPT read the folder for each question. '
         'Copilot Researcher searched the SharePoint site for each question, and its times include the questions it asked before starting. '
         "Tabular review's times are rounded, from its stored run times and the clock.", '',
         '## By kind of question', '', 'The score out of 100 on the questions of each kind.', '', f'| Kind | Questions | {cols} |', sep + '---|']
    for k in kinds:
        h.append(row(k, [sum(q['kind'] == k for q in qs)] + [f"{x['by_kind'][k]:.1f}" for x in s]))
    h += ['', '## Time per question', '', '| | Under 1 min | 1 to 5 min | Over 5, up to 10 min | Over 10 min |', '|---|---|---|---|---|']
    for k, n in SYSTEMS:
        h.append(row(n, data['systems'][k]['time_bands']))
    h += ['', '## Redrawing the questions', '', f'The 46 questions redrawn at random {REDRAWS:,} times (each redraw the same size, some questions twice, some not at all), and the score worked out again each time.', '',
          '| | Difference in score, 95% of redraws | First named ahead in |', '|---|---|---|']
    for a, b in PAIRS:
        r = data['redraws'][f'{a}_minus_{b}']
        h.append(row(f'{NAME[a]} minus {NAME[b]}', [f"{r['range_95'][0]:+.1f} to {r['range_95'][1]:+.1f}", f"{r['ahead_pct']:.1f}% of redraws"]))
    h += ['', '## How the runs differ', '',
          '- **AeroSpark, plain Claude and ChatGPT** got one fresh chat per question and no follow-ups: [the main run](2026-10-aerospark-chatgpt-claude/README.md), with [its limits](2026-10-aerospark-chatgpt-claude/CAVEATS.md).',
          '- **Tabular review** ran in one review, in order, with the follow-ups it needed on four questions and each proposed column accepted as it stood. Its model could not be confirmed: [the Tabular run](2026-10-claude-tabular-review/README.md).',
          "- **NotebookLM** (now Gemini Notebook) had one notebook holding only the 99 contracts, with its chat's Google Drive search switched off, the chat cleared before each question and no follow-ups. Its model is not shown: [the NotebookLM run](2026-11-notebooklm/README.md).",
          "- **Copilot Researcher** (Microsoft 365 Copilot's Researcher agent, model Auto) got a new chat per question, with web search off for the whole Microsoft 365 account. "
          "Its questions named the SharePoint site holding the 99 contracts instead of a Google Drive folder. It always asked two or three questions of its own first, and got the same reply each time: "
          "\"Go ahead using your best judgment\". "
          f"Its answers also named {data['systems']['copilot']['named_not_in_folder']} contracts as matches that are not in the folder, which no score can count: [the Copilot run](2026-11-copilot-researcher/README.md).",
          '- **Asked again.** Any question where a system found 25% or less of the key was asked again in the same words, for every system, and the time was added. That took in eight questions for Tabular review, five for Copilot Researcher, two for NotebookLM and one for ChatGPT.', '',
          '## Question by question', '',
          'Every question with all six results and times: [the Copilot run\'s table](2026-11-copilot-researcher/scores/headline.md). '
          'Each answer for AeroSpark, plain Claude and ChatGPT, word for word: [the question pages](2026-10-aerospark-chatgpt-claude/answers/by_question/README.md). '
          "What Tabular review's Ask panel showed: [its screenshots](2026-10-claude-tabular-review/answers/screens/README.md). NotebookLM's answers: [its answers file](2026-11-notebooklm/answers/answers.txt). Copilot Researcher's: [its answers file](2026-11-copilot-researcher/answers/answers.txt)."]
    return '\n'.join(h)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    data, qs, kinds = compute()
    text = page(data, qs, kinds)
    print(text)
    if args.write:
        json.dump(data, open(os.path.join(RESULTS, 'comparison.json'), 'w'), indent=1)
        open(os.path.join(RESULTS, 'COMPARISON.md'), 'w', encoding='utf-8').write(text + '\n')
        print('\nwrote COMPARISON.md and comparison.json')
    if args.check:
        if json.load(open(os.path.join(RESULTS, 'comparison.json'))) != json.loads(json.dumps(data)):
            print('\nDIFFERS from results/comparison.json')
            sys.exit(1)
        print('\nmatches results/comparison.json')


if __name__ == '__main__':
    main()
