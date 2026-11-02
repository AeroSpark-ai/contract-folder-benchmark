# All four systems side by side

The same 46 questions about the same folder of 99 contracts, against the same answer key. **We build [AeroSpark](https://www.aerospark.ai/l/gh-comparison), a contract repository**, so every figure here is re-made from the recorded answers by `results/compare.py`.

| | AeroSpark | Plain Claude | Tabular review | ChatGPT |
|---|---|---|---|---|
| **Score out of 100** | **89.8** | **85.6** | **83.9** | **82.2** |
| Contracts found, the 30 list questions (576 in the key) | 490 (85%) | 463 (80%) | 452 (78%) | 427 (74%) |
| Contracts named that are not in the key | 24 | 12 | 23 | 5 |
| Found, with the contracts each hedged as "possible" credited too | 508 (29 not in the key) | 495 (61 not in the key) | 482 (23 not in the key) | 462 (27 not in the key) |
| Counts right (of 5) | 4 | 4 | 4 | 4 |
| Lookups right (of 11) | 11 | 11 | 11 | 11 |
| Median wait per question | 10 s | 5.6 min | 42 s | 5.9 min |
| Slowest question | 35 s | 11.2 min | 5.2 min | 19.4 min |
| All 46 questions | 9 minutes | 4.0 hours | About 85 minutes, plus about 30 blocked | 4.9 hours |

**The times are how long a person waits**, from asking to the finished answer. AeroSpark reads each contract when it is added, before any question is asked. Tabular review reads every contract when a question needs a new column, and that wait counts against the question. Plain Claude and ChatGPT read the folder for each question. Tabular review's times are rounded, from its stored run times and the clock.

## By kind of question

The score out of 100 on the questions of each kind.

| Kind | Questions | AeroSpark | Plain Claude | Tabular review | ChatGPT |
|---|---|---|---|---|---|
| Find every contract with a clause | 14 | 82.5 | 81.9 | 82.8 | 77.6 |
| Two or three conditions at once | 4 | 88.5 | 72.7 | 78.4 | 77.5 |
| Dates against a stated day | 6 | 94.6 | 82.8 | 68.0 | 64.3 |
| The most recent, the shortest notice | 2 | 100.0 | 83.3 | 83.3 | 83.3 |
| By party, by type, notice period, either of two clauses | 4 | 88.4 | 83.9 | 77.6 | 83.7 |
| Counts | 5 | 80.0 | 80.0 | 80.0 | 80.0 |
| One fact about one named contract | 9 | 100.0 | 100.0 | 100.0 | 100.0 |
| A contract that is not in the folder | 2 | 100.0 | 100.0 | 100.0 | 100.0 |

## Time per question

| | Under 1 min | 1 to 5 min | Over 5, up to 10 min | Over 10 min |
|---|---|---|---|---|
| AeroSpark | 46 | 0 | 0 | 0 |
| Plain Claude | 11 | 9 | 23 | 3 |
| Tabular review | 24 | 21 | 1 | 0 |
| ChatGPT | 8 | 9 | 22 | 7 |

## Redrawing the questions

The 46 questions redrawn at random 10,000 times (each redraw the same size, some questions twice, some not at all), and the score worked out again each time.

| | Difference in score, 95% of redraws | First named ahead in |
|---|---|---|
| AeroSpark minus Plain Claude | +1.5 to +7.1 | 99.9% of redraws |
| AeroSpark minus Tabular review | +1.4 to +11.7 | 99.7% of redraws |
| AeroSpark minus ChatGPT | +3.4 to +12.9 | 100.0% of redraws |
| Plain Claude minus Tabular review | -1.5 to +6.3 | 80.1% of redraws |
| Plain Claude minus ChatGPT | -0.1 to +8.0 | 97.1% of redraws |
| Tabular review minus ChatGPT | -1.0 to +4.5 | 87.5% of redraws |

## How the runs differ

- **AeroSpark, plain Claude and ChatGPT** got one fresh chat per question and no follow-ups: [the main run](2026-10-aerospark-chatgpt-claude/README.md), with [its limits](2026-10-aerospark-chatgpt-claude/CAVEATS.md).
- **Tabular review** ran in one review, in order, with the follow-ups it needed on four questions and each proposed column accepted as it stood. Its model could not be confirmed: [the Tabular run](2026-10-claude-tabular-review/README.md).
- **Asked again.** Any question where a system found 25% or less of the key was asked again in the same words, for every system, and the time was added. That took in eight questions for Tabular review and one for ChatGPT.

## Question by question

Every question with all four results and times: [the Tabular run's table](2026-10-claude-tabular-review/scores/headline.md). Each answer for AeroSpark, plain Claude and ChatGPT, word for word: [the question pages](2026-10-aerospark-chatgpt-claude/answers/by_question/README.md). What Tabular review's Ask panel showed: [its screenshots](2026-10-claude-tabular-review/answers/screens/README.md).
