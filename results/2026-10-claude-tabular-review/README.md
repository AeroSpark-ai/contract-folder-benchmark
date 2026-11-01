# October 2026 run: Claude's Tabular review

The same 46 questions about the same 99 contracts as [the main run](../2026-10-aerospark-chatgpt-claude/README.md), put to **Tabular review**, a ready-made artifact from the legal gallery
[Anthropic released on 28 October 2026](https://claude.com/resources/articles/introducing-artifacts-for-legal-work). It builds a table of contracts against questions, and answers from that table in an Ask panel.

**We build AeroSpark, a contract repository.** So everything needed to check this run is here.

## The result

Every question counts the same, out of 100, as in the main run. Plain Claude's figures are its run there: Claude Max, Opus 5.5 at High, Google Drive connector, a fresh chat per question.

| | Plain Claude | Tabular review |
|---|---|---|
| **Score out of 100** | **85.6** | **83.9** |
| Contracts found, the 30 list questions (576 in the key) | 463 (80%) | 452 (78%) |
| Contracts named that are not in the key | 12 | 23 |
| Found, with the contracts each hedged as "possible" credited too | 495 (61 not in the key) | 482 (23 not in the key) |
| Counts right (of 5) | 4 | 4 |
| Lookups right (of 11) | 11 | 11, six of them on a re-ask |
| Questions answered in under a minute | 11 | 24 |
| Median time per question | 5.6 min | 42 s |
| All 46, added up | 4.0 hours | About 85 minutes, plus about 30 minutes while the page was blocked |

Tabular review's first answers scored 69.7. Any question where a system found 25% or less of the key was asked again in the same words: questions 14 to 19, 26 and 28. The re-asks took it to 83.9, and their
time is in its total.

With the 46 questions redrawn at random 10,000 times, plain Claude minus Tabular review is -1.5 to +6.3 in 95% of redraws, and plain Claude is ahead in 80.1% of them. Question by question:
[scores/headline.md](scores/headline.md).

## How it was run

- **The tool.** A private, unchanged copy of Tabular review in claude.ai, on the page's default model tier. The page does not show which model that is. Run on 31 October 2026.
- **The contracts.** The 99 PDFs of the benchmark, uploaded to one review.
- **The questions.** The benchmark's words, without the drive prefix, in one review and in order: 1 to 3, then 11, 7 to 10, 37, 12, 13 and 35, then the rest. When Ask said the table could not answer and proposed a column,
  the column was accepted as proposed and the question asked again once it had filled.
- **Follow-ups.** The main run had none. This tool needed them on four questions: "I meant all 99 contracts" on 22 and 23, today's date on 28, and "please check all 99 contracts" on 31.
- **Failures.** Five document reads failed and were retried. From about 18:45 to about 19:15 CET the page refused all calls with "Claude is limiting calls from this page. It may be your usage limit", with the account's
  usage meter at 61% for the session and 45% for the week. The cause is unknown.

## How it was scored

The scorer is the repository's own, on the same key. `python3 results/2026-10-claude-tabular-review/scoring/reproduce.py` re-makes every figure.

- **What counts is what Ask wrote.** A contract counts when the written answer names it as a match. A contract marked Yes in the table but left out of the written answer does not count.
- **The last word stands.** When a later reply disowned an earlier answer ("you should not rely on that answer"), the question counted as not answered until it was asked again.
- **Hedges earn nothing.** On question 28 the answer says the table "cannot confirm that any contract is in force" and then sorts contracts by their stated terms, so all of them count as possible.
- **The lookups** are graded by reading: [scores/graded_by_reading.json](scores/graded_by_reading.json). Questions 19, 20 and 35 are judgment calls and the file says why. Each is worth about 2.2 points.

## What is here

| Path | What it is |
|---|---|
| `answers/screens/` | What the Ask panel showed, as screenshots, indexed by question. The panel keeps no history to export, so these are the record of its words |
| `answers/lists_as_read.json` | The contracts each answer named and hedged, typed from those screens |
| `answers/answers.txt`, `claims/claims.json` | The same lists in the form `scoring/score.py` reads. An answer's `summary` is the list as read, not the tool's own words |
| `table/table.json` | The finished table: for each contract and column, the value, status, quote, page, confidence and reasoning the tool stored |
| `scores/` | The tables and the lookup grades |

Times per question in `answers/answers.txt` are rounded, from the tool's stored fill times and the clock. They add up to less than the 85 minutes because they leave out moving between questions.
