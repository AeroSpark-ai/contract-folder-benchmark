# The result, re-scored from the recorded answers

Made by `python3 results/2026-10-aerospark-chatgpt-claude/scoring/reproduce.py --write`. The lookups are graded by reading: [graded_by_reading.md](graded_by_reading.md). Every question: [per_question.csv](per_question.csv).

**The score.** Every question counts the same, out of 100: a list question earns the share of the key's contracts the answer found; a count or a lookup is right or not.

| | AeroSpark | Claude | ChatGPT |
|---|---|---|---|
| **Score out of 100** | **89.8** | **85.6** | **82.2** |
| Contracts found, the 30 list questions (576 in the key) | 490 (85%) | 463 (80%) | 427 (74%) |
| Contracts named that are not in the key | 24 | 12 | 5 |
| Found, with the contracts each hedged as "possible" credited too | 508 (29 not in the key) | 495 (61 not in the key) | 462 (27 not in the key) |
| Counts right (of 5) | 4 | 4 | 4 |
| Lookups right (of 11) | 11 | 11 | 11 |
| Median time per question | 10 s | 5.6 min | 5.9 min |
| Slowest question | 35 s | 11.2 min | 19.4 min |
| All 46 questions | 9.3 min | 4.0 hours | 4.9 hours |

**Redrawing the questions.** The 46 questions redrawn at random 10,000 times (each redraw the same size, some questions twice, some not at all), and the score worked out again each time:

| | Difference in score, 95% of redraws | AeroSpark ahead in |
|---|---|---|
| AeroSpark minus Claude | +1.5 to +7.1 | 99.9% of redraws |
| AeroSpark minus ChatGPT | +3.4 to +12.9 | 100.0% of redraws |

**By kind of question** (the score out of 100 on the questions of each kind)

| Kind | Questions | AeroSpark | Claude | ChatGPT |
|---|---|---|---|---|
| Find every contract with a clause | 14 | 82.5 | 81.9 | 77.6 |
| Two or three conditions at once | 4 | 88.5 | 72.7 | 77.5 |
| Dates against a stated day | 6 | 94.6 | 82.8 | 64.3 |
| The most recent, the shortest notice | 2 | 100.0 | 83.3 | 83.3 |
| By party, by type, notice period, either of two clauses | 4 | 88.4 | 83.9 | 83.7 |
| Counts | 5 | 80.0 | 80.0 | 80.0 |
| One fact about one named contract | 9 | 100.0 | 100.0 | 100.0 |
| A contract that is not in the folder | 2 | 100.0 | 100.0 | 100.0 |

**Time per question**

| | Under 1 min | 1 to 5 min | 5 to 10 min | Over 10 min |
|---|---|---|---|---|
| AeroSpark | 46 | 0 | 0 | 0 |
| Claude | 11 | 9 | 23 | 3 |
| ChatGPT | 8 | 9 | 22 | 7 |
