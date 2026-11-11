# November 2026 run: Microsoft 365 Copilot Researcher

The same 46 questions about the same 99 contracts as [the main run](../2026-10-aerospark-chatgpt-claude/README.md), put to the **Researcher agent of Microsoft 365 Copilot**, with the 99
contracts in a SharePoint site of their own. Researcher searched the site for each question and answered from what it found.

**We build [AeroSpark](https://www.aerospark.ai/l/gh-comparison), a contract repository.** So everything needed to check this run is here.

## The result

Every question counts the same, out of 100, as in the main run. The other columns are from [the main run](../2026-10-aerospark-chatgpt-claude/README.md), [the Tabular review run](../2026-10-claude-tabular-review/README.md)
and [the NotebookLM run](../2026-11-notebooklm/README.md).

| | AeroSpark | Plain Claude | Tabular review | NotebookLM | ChatGPT | Copilot Researcher |
|---|---|---|---|---|---|---|
| **Score out of 100** | **89.8** | **85.6** | **83.9** | **83.5** | **82.2** | **74.2** |
| Contracts found, the 30 list questions (576 in the key) | 490 (85%) | 463 (80%) | 452 (78%) | 438 (76%) | 427 (74%) | 315 (55%) |
| Contracts named that are not in the key | 24 | 12 | 23 | 17 | 5 | 19 |
| Found, with the contracts each hedged as "possible" credited too | 508 (29 not in the key) | 495 (61 not in the key) | 482 (23 not in the key) | 439 (17 not in the key) | 462 (27 not in the key) | 335 (43 not in the key) |
| Counts right (of 5) | 4 | 4 | 4 | 4 | 4 | 4 |
| Lookups right (of 11) | 11 | 11 | 11 | 11 | 11 | 11 |
| Questions answered in under a minute | 46 | 11 | 24 | 27 | 8 | 0 |
| Median time per question | 10 s | 5.6 min | 42 s | 53 s | 5.9 min | 5.2 min |
| All 46, added up | 9 minutes | 4.0 hours | About 85 minutes | 48 minutes | 4.9 hours | 4.0 hours |

The times are how long a person waits, from asking to the finished answer, including the questions Researcher asked before it started (below).

**Copilot's answers also named 55 contracts as matches that are not in the folder**, written in the same file-name style as the real ones and with section numbers and quoted wording. None
of those whose file name the answer gives is among the 510 contracts of CUAD, the public set the 99 come from. The benchmark scores only contracts it can place on the folder's list, so these
count neither as found nor as wrong. The reader found one such name in plain Claude's answers and none in the other systems'. All of Copilot's: [claims/names_settled_by_claude.md](claims/names_settled_by_claude.md).

Copilot's first answers scored 67.6. Any question where a system found 25% or less of the key was asked again in the same words: questions 7, 9, 10, 11 and 28. The re-asks got the counts in 7, 9 and
10 right. On 11, a count, it said 10 the first time and 9 the second; the key has 13, and no system got it right. On 28 it found 2 of the 28 contracts both times. The re-ask's answer is the one scored,
and both asks' time is in its total. Question 21 was also asked a second time, before the reader had scored its first answer; the reader credits that first answer with 2 of the 3 contracts, so only
the first answer counts, and the second is kept apart in `answers/not_counted.txt`.

With the 46 questions redrawn at random 10,000 times, ChatGPT minus Copilot Researcher is +4.0 to +12.7 in 95% of redraws, with ChatGPT ahead in all of them. All six side by side:
[COMPARISON.md](../COMPARISON.md). Question by question, with all six: [scores/headline.md](scores/headline.md).

## How it was run

- **The tool.** The Researcher agent in Microsoft 365 Copilot (copilot.cloud.microsoft), on a Microsoft 365 work account with a Microsoft 365 Copilot Business licence (a one-month trial). Its model
  menu was left on Auto (it also offers GPT and Claude models); it does not say which model answered. Run on 10 November 2026 (questions 1, 40 and 42) and 10 and 11 November 2026 (the rest and the re-asks).
- **Why Researcher.** Copilot was first tried two other ways, on three of the questions (1, 40 and 42; 167 contracts in the key between them), counted from the file names each answer gives:
  - **A Copilot Notebook** holding the 99 contracts as references found 33 of the 167. Every answer said it worked from "the 20 contracts", the same 20 each time.
  - **Copilot Chat** in Work mode, set to "Think deeper", found 23. It read a handful of contracts for each answer.
  - **Researcher** found 98 of the 167 counted the same way, so its answers are the ones recorded here.
- **The contracts.** One SharePoint site, "Benchmark Test", whose document library held the benchmark's 99 PDFs and nothing else (names and sizes checked). SharePoint indexes every file uploaded;
  phrases from near the end of three of the contracts each found the right file in its search. The Microsoft 365 account also held our own test site, about 118 documents (mostly test agreements from building
  AeroSpark's SharePoint connection), and Microsoft's small default sites; no answer cited or named any of them. The Copilot Notebook from the first try, holding the 99 as references, stayed in
  place for the run, and Researcher sometimes cited it as its list of the 99.
- **Web search off.** Copilot's web search was switched off for the whole account with Microsoft's policy "Allow web search in Copilot" (set to "Disabled in Microsoft 365 Copilot and Microsoft 365
  Copilot Chat"). Every Researcher page showed "Web search is off"; its Sources menu showed Microsoft 365 on and Web off. Every link in every answer was checked: they opened the site's contracts (a few
  through a Microsoft Loop link), the notebook, a chart or image Researcher made itself or a Microsoft help page, and no answer mentions this benchmark's results, its key or another system.
- **The questions.** The benchmark's words, with the prefix `In my SharePoint site "Benchmark Test" (all its folders):` in place of the Google Drive prefix the other systems were asked with. A new
  Researcher chat for each question.
- **Researcher's own questions.** Before every answer Researcher asked two or three questions of its own (amendments included? explicit wording only?) and offered report-length buttons. The reply
  each time was "Go ahead using your best judgment", the reply its own message suggested; no report length was chosen and there were no other follow-ups. What it asked, question by question:
  `answers/links_and_notes.json`.
- **The answers.** Copied with the answer's Copy Response button. Researcher writes each contract's file name into its answers; its links to SharePoint are kept as copied (they open only inside the
  account). A style block the copy carries was removed.
- **Times.** From pressing Enter on the question until the report's text stopped changing, measured in the page. They include Researcher's own questions and the reply.
- **Failures.** Two asks failed with "Oops! Something happened. Can you try again?" (questions 32 and 38) and were asked again at once in a new chat; those answers are the ones recorded.
- **Limits.** Microsoft's FAQ gives Researcher "a maximum of 25 queries per user per month". About 57 Researcher chats over two days were never stopped.

## How it was scored

The scorer is the repository's own, on the same key. `python3 results/2026-11-copilot-researcher/scoring/reproduce.py` re-makes every figure.

- **What counts is what the answer names.** As for every other system, a model reader (Claude Haiku, [scoring/reference/extract_claims.js](../../scoring/reference/extract_claims.js)) copied the names each
  answer gives and whether it affirms or hedges each, twice for every answer; the two readings agreed on all 52 answers (the 46 first answers and the six second asks). Code placed
  each name on the contract list.
- **Names code could not place** were settled from the full file name the answer gives (four names, two Reynolds agreements), or found to be contracts that are not in the folder (above):
  [claims/names_settled_by_claude.md](claims/names_settled_by_claude.md).
- **The lookups and the two questions about a contract not in the folder** are graded by reading: [scores/graded_by_reading.json](scores/graded_by_reading.json).

## What is here

| Path | What it is |
|---|---|
| `answers/answers.txt` | Every answer scored, in the form `scoring/score.py` reads, with its time in milliseconds. The five re-asked questions carry both times |
| `answers/first_asks.txt` | The first answers to questions 7, 9, 10, 11 and 28, which the re-asks replaced |
| `answers/not_counted.txt` | The second answer to question 21, asked before its first answer was scored, and not counted |
| `answers/links_and_notes.json` | For each answer, its seconds, what its links open, and the questions Researcher asked before answering |
| `claims/claims.json`, `claims/first_asks_claims.json` | What the model reader read from each answer, and the names settled |
| `claims/names_settled_by_claude.md` | The names settled by hand, and every contract named that is not in the folder |
| `scores/` | The tables and the lookup grades |
