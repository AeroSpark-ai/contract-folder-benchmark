#!/usr/bin/env python3
"""Score one run file against the answer key.

    python3 scoring/score.py <run file> <claims file> [--key benchmark/key/key.json] [--per-question]

    e.g. python3 scoring/score.py results/2026-10-aerospark-chatgpt-claude/answers/chatgpt/answers.txt results/2026-10-aerospark-chatgpt-claude/claims/chatgpt/claims.json --per-question

The rules (benchmark/docs/METHOD.md, section 4), the same for every system:
  - A list question is scored on the contracts the answer names. "Named as a match" is a contract the claims file lists under "yes";
    "with hedged matches credited" adds the ones it lists under "possible". A named contract in the key is found; one not in the key is wrong.
  - A contract the labels cannot settle for a question (its "skip" list in the key, e.g. no usable end date for "still in force today")
    is left out of that question: naming it is neither found nor wrong.
  - An answer marked as no answer scores as no answer: "firstAttempt": "stalled" (the attempt gave no answer) or "other_drive" (it read
    another shared drive, not this folder). An answer that failed with an error names nothing.
  - A count question ("count": true in the key) is scored on the number the answer gives, not in the list totals.
  - Lookups and the not-in-the-folder questions are graded by reading (results/2026-10-aerospark-chatgpt-claude/scores/graded_by_reading.md).
No model call, no network, standard library only.
"""
import argparse
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load_contracts():
    """AeroSpark contract id -> the file name the answer key uses."""
    with open(os.path.join(ROOT, 'benchmark', 'contracts', 'contracts.csv'), encoding='utf-8') as fh:
        return {r['aerospark_id']: r['key_name'] for r in csv.DictReader(fh) if r['aerospark_id']}


def load_run(run_file, claims_file):
    corpus, answers = None, {}
    with open(run_file, encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('CORPUS '):
                corpus = json.loads(line[7:])
            elif line.startswith('ANS '):
                a = json.loads(line[4:])
                answers[a['id']] = a
    with open(claims_file, encoding='utf-8') as fh:
        claims = {c['id']: c['claims'] for c in json.load(fh) if c.get('pass', 1) == 1}
    ids = load_contracts()
    names = [ids[i] for i in corpus['order']]          # position n (1-based) in the run's list -> key file name
    return {'corpus': corpus, 'answers': answers, 'claims': claims, 'names': names}


NO_ANSWER = ('stalled', 'other_drive')


def named(run, qid, tag):
    """The key file names the answer to qid lists under tag ('yes' or 'possible'); empty if the answer is marked as no answer."""
    a = run['answers'].get(qid) or {}
    if a.get('firstAttempt') in NO_ANSWER:
        return set()
    nums = (run['claims'].get(qid) or {}).get(tag) or []
    return {run['names'][n - 1] for n in nums if 1 <= n <= len(run['names'])}


def score_question(run, q):
    """Found / wrong for one list question, named as a match and with hedged matches credited; None for other questions."""
    t = q.get('truth') or {}
    if t.get('type') != 'files':
        return None
    key = set(t['files']) & set(run['names'])        # the key, limited to the contracts in this folder
    skip = set(t.get('skip') or [])                   # contracts the labels cannot settle for this question: naming one is neither found nor wrong
    yes = named(run, q['id'], 'yes') - skip
    both = (yes | named(run, q['id'], 'possible')) - skip
    a = run['answers'].get(q['id']) or {}
    out = {'id': q['id'], 'key': len(key), 'count_question': bool(t.get('count')),
           'found': len(key & yes), 'wrong': len(yes - key), 'found_with_possibles': len(key & both), 'wrong_with_possibles': len(both - key),
           'seconds': round((a.get('ms') or 0) / 1000, 1), 'first_attempt_stalled': a.get('firstAttempt') in NO_ANSWER,
           'no_answer_why': a.get('firstAttempt'), 'error': a.get('error')}
    if t.get('count'):
        given = None if out['first_attempt_stalled'] else (run['claims'].get(q['id']) or {}).get('count')
        out['count_given'] = given
        out['count_right'] = given == len(key)
    return out


def score_run(run_file, claims_file, key_file):
    with open(key_file, encoding='utf-8') as fh:
        questions = json.load(fh)['questions']
    run = load_run(run_file, claims_file)
    return [s for q in questions if q['id'] in run['answers'] for s in [score_question(run, q)] if s]


def totals(scored):
    lists = [s for s in scored if not s['count_question']]
    return {k: sum(s[k] for s in lists) for k in ('key', 'found', 'wrong', 'found_with_possibles', 'wrong_with_possibles')}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('run')
    ap.add_argument('claims')
    ap.add_argument('--key', default=os.path.join(ROOT, 'benchmark', 'key', 'key.json'))
    ap.add_argument('--per-question', action='store_true')
    args = ap.parse_args()
    scored = score_run(args.run, args.claims, args.key)
    t = totals(scored)
    print(f"list questions: {sum(1 for s in scored if not s['count_question'])}, contracts in the key: {t['key']}")
    print(f"  named as a match            : found {t['found']}, wrong {t['wrong']}, missed {t['key'] - t['found']}")
    print(f"  hedged matches credited too : found {t['found_with_possibles']}, wrong {t['wrong_with_possibles']}, missed {t['key'] - t['found_with_possibles']}")
    for s in scored:
        if s['count_question']:
            print(f"  count {s['id']}: answered {s['count_given']}, key {s['key']}, {'right' if s['count_right'] else 'not right'}")
    if args.per_question:
        for s in scored:
            why = {'stalled': 'first attempt stalled', 'other_drive': 'read the other shared drive'}.get(s['no_answer_why'], '')
            note = f' ({why}: no answer)' if s['first_attempt_stalled'] else (f" (error: {s['error']})" if s['error'] else '')
            print(f"  {s['id']:40s} key {s['key']:3d} | found {s['found']:3d} wrong {s['wrong']:3d} | with possibles {s['found_with_possibles']:3d} / {s['wrong_with_possibles']:3d}{note}")


if __name__ == '__main__':
    main()
