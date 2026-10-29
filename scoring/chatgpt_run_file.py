"""
Turn a folder of saved ChatGPT answers into a run file that extract_claims.js and score.py read like an AeroSpark run.

    python3 scoring/chatgpt_run_file.py <answers folder> <roster run file> <out run file> [--match REGEX] [--setting TEXT]

Each answer file (one per question, saved while running ChatGPT in the browser) starts with a header, then a line of five dashes, then the answer:
    QUESTION (id audit): In my Google Drive folder "...": Which of these contracts give a party the right to audit the other party?
    SETTING: ChatGPT Business, model label "Instant", Google Drive attached, Temporary Chat
    WALL SECONDS (Enter pressed -> response actions appear): 101.6
    -----
    <the answer as ChatGPT gave it>
The roster is an AeroSpark run file over the SAME contracts: its CORPUS line gives the order the claim extractor numbers them in ([1]..[N])
and their file names (and parties, when recorded), which the extractor matches ChatGPT's company names against.
--match keeps only answer files whose name matches (default: q01_audit.txt style, one per question; retries such as q04b_..._xhigh.txt
are left out unless --match includes them).
"""
import argparse
import json
import os
import re
import sys


def parse(path):
    text = open(path, encoding='utf-8').read()
    head, sep, body = text.partition('\n-----\n')
    if not sep:
        sys.exit(f'{path}: no "-----" line between the header and the answer')
    m = re.search(r'^QUESTION \(id ([\w-]+)[^)]*\):\s*(.+)$', head, re.M)          # "(id coc)" or "(id coc, <note>)"
    if not m:
        sys.exit(f'{path}: no "QUESTION (id ...):" line')
    secs = re.search(r'^WALL SECONDS[^:]*:\s*(?:about\s*)?([\d.]+)', head, re.M)   # "101.6" or "about 135 (...)"
    setting = re.search(r'^SETTING:\s*(.+)$', head, re.M)
    return {'id': m.group(1), 'q': m.group(2).strip(), 'ms': int(float(secs.group(1)) * 1000) if secs else 0,
            'setting': setting.group(1).strip() if setting else None, 'answer': body.strip(), 'file': os.path.basename(path)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('folder'); ap.add_argument('roster'); ap.add_argument('out')
    ap.add_argument('--match', default=r'^q\d+_[a-z]+\.txt$'); ap.add_argument('--setting', help='overrides the SETTING line of every answer')
    ap.add_argument('--label', default='chatgpt')
    args = ap.parse_args()
    roster = json.loads(next(l for l in open(args.roster) if l.startswith('CORPUS '))[7:])
    if 'files' not in roster:
        sys.exit('the roster run file has no file names')
    rx = re.compile(args.match)
    answers = [parse(os.path.join(args.folder, f)) for f in sorted(os.listdir(args.folder)) if rx.search(f)]
    if not answers:
        sys.exit('no answer files matched')
    ids = [a['id'] for a in answers]
    if len(set(ids)) != len(ids):
        sys.exit(f'more than one answer for a question: {ids} (narrow --match)')
    corpus = {'system': 'chatgpt', 'label': args.label, 'rows': len(roster['order']), 'order': roster['order'], 'files': roster['files'],
              'parties': roster.get('parties'), 'rosterFrom': os.path.basename(args.roster), 'questionOrder': ids, 'passes': 1,
              'settings': sorted({args.setting or a['setting'] or '?' for a in answers})}
    # A question whose FIRST attempt stalled (a file stalled_qNN_<id>.txt beside the answers) is marked: score.py scores the first
    # attempt (no answer) — the same rule as AeroSpark, whose failed answers are not asked again.
    stalled = {m.group(1) for f in os.listdir(args.folder) for m in [re.match(r'^stalled_q\d+_([a-z0-9-]+)\.txt$', f)] if m}
    with open(args.out, 'w') as out:
        out.write('CORPUS ' + json.dumps(corpus) + '\n')
        for a in answers:
            out.write('ANS ' + json.dumps({'pass': 1, 'id': a['id'], 'q': a['q'], 'ms': a['ms'], 'error': None, 'route': 'chatgpt', 'summary': a['answer'],
                                           'findings': [], 'cm': None, 'skim': None, 'usd': 0, 'calls': [], 'source': a['file'],
                                           'setting': args.setting or a['setting'], **({'firstAttempt': 'stalled'} if a['id'] in stalled else {})}) + '\n')
    print(f'{len(answers)} answers -> {args.out} ({", ".join(ids)})')


if __name__ == '__main__':
    main()
