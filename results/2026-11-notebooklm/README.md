# November 2026 run: NotebookLM

The same 46 questions about the same 99 contracts as [the main run](../2026-10-aerospark-chatgpt-claude/README.md), put to **NotebookLM**, Google's notebook tool, which Google now calls
Gemini Notebook. The 99 contracts were its sources, and it answered from them.

**We build [AeroSpark](https://www.aerospark.ai/l/gh-comparison), a contract repository.** So everything needed to check this run is here.

## The result

Every question counts the same, out of 100, as in the main run. The other columns are from [the main run](../2026-10-aerospark-chatgpt-claude/README.md) and [the Tabular review run](../2026-10-claude-tabular-review/README.md).

| | AeroSpark | Plain Claude | Tabular review | NotebookLM | ChatGPT |
|---|---|---|---|---|---|
| **Score out of 100** | **89.8** | **85.6** | **83.9** | **83.5** | **82.2** |
| Contracts found, the 30 list questions (576 in the key) | 490 (85%) | 463 (80%) | 452 (78%) | 438 (76%) | 427 (74%) |
| Contracts named that are not in the key | 24 | 12 | 23 | 17 | 5 |
| Found, with the contracts each hedged as "possible" credited too | 508 (29 not in the key) | 495 (61 not in the key) | 482 (23 not in the key) | 439 (17 not in the key) | 462 (27 not in the key) |
| Counts right (of 5) | 4 | 4 | 4 | 4 | 4 |
| Lookups right (of 11) | 11 | 11 | 11 | 11 | 11 |
| Questions answered in under a minute | 46 | 11 | 24 | 27 | 8 |
| Median time per question | 10 s | 5.6 min | 42 s | 53 s | 5.9 min |
| All 46, added up | 9 minutes | 4.0 hours | About 85 minutes | 48 minutes | 4.9 hours |

The times are how long a person waits, from asking to the finished answer. The 99 contracts were added to the notebook once, before any question; adding them is not in the times.

NotebookLM's first answers scored 82.3. Any question where a system found 25% or less of the key was asked again in the same words: questions 11 and 33. On 33 the re-ask found 7 of the 9 contracts in
the key, against 2 the first time. On 11, a count, it said 9 the first time and 6 the second; the key has 13, and no system got it right. The re-ask's answer is the one scored, and both asks' time is in its total.

With the 46 questions redrawn at random 10,000 times, plain Claude minus NotebookLM is -1.2 to +5.9 in 95% of redraws, with plain Claude ahead in 87.6% of them; NotebookLM minus ChatGPT is -1.9 to +5.5,
with NotebookLM ahead in 73.8%. All five side by side: [COMPARISON.md](../COMPARISON.md). Question by question, with all five: [scores/headline.md](scores/headline.md).

## How it was run

- **The tool.** NotebookLM at notebook.google.com, which called itself Gemini Notebook, on a Google Workspace work account. The page showed a PRO badge and a limit of 300 sources. It does not show which model
  answers. Run on 7 November 2026 (questions 1, 40 and 42) and 9 November 2026 (the rest and the two re-asks).
- **The contracts.** One notebook, holding the benchmark's 99 PDFs and nothing else, added from the Google shared drive with the Drive picker. The picker takes 50 files at a time, so they went in as 50 and 49. Before
  every question the source list was checked: 99 sources, each title one of the 99.
- **One setting changed.** The chat's menu (the icon left of the chat box) has a Google Drive switch, on by default, that lets the chat search the account's whole Drive as well as the notebook's
  sources. It was switched off, so the answers come from the 99 contracts only. Every other setting was left as it was.
- **The questions.** The benchmark's words, with the drive prefix, as ChatGPT and Claude were asked. The chat history was cleared before each question, so each was asked on its own. No follow-ups.
- **The answers.** Copied with the answer's Copy button, which leaves out the citation numbers. NotebookLM wrote most contracts' file names into its answers. In 19 places across the 48 answers it showed
  "[suspicious link removed]" where a company name belonged; for those, the citation was opened to see which contract it meant.
- **Times.** From Send until the answer had finished (the Copy button showing, no Stop button, and the text no longer changing), measured in the page and, where the page recorded it, checked against the end
  of the answer's network request. The slowest, question 24, showed "Verifying Dates and Parties..." for about four minutes before the answer arrived whole.
- **Failures.** None. No question errored or had to be asked again for a fault.

## How it was scored

The scorer is the repository's own, on the same key. `python3 results/2026-11-notebooklm/scoring/reproduce.py` re-makes every figure.

- **What counts is what the answer names.** As for ChatGPT and Claude, a model reader (Claude Haiku, [scoring/reference/extract_claims.js](../../scoring/reference/extract_claims.js)) copied the names each answer
  gives and whether it affirms or hedges each, twice for every answer; the two readings agreed on all 48 answers. Code placed each name on the contract list.
- **Names code could not place** (a tie between two Reynolds agreements, or a name Gemini hid) were settled from the answer's own words and the contract its citation opens:
  [claims/names_settled_by_claude.md](claims/names_settled_by_claude.md).
- **The lookups** are graded by reading: [scores/graded_by_reading.json](scores/graded_by_reading.json).

## What is here

| Path | What it is |
|---|---|
| `answers/answers.txt` | Every answer scored, in the form `scoring/score.py` reads, with its time in milliseconds. The two re-asked questions carry both times |
| `answers/first_asks.txt` | The first answers to questions 11 and 33, which the re-asks replaced |
| `answers/citations_and_notes.json` | For each answer, its seconds and the citations read: which source each citation number opens. Where the answer names every contract by file name, only its first and last citations were read |
| `claims/claims.json`, `claims/first_asks_claims.json` | What the model reader read from each answer, and the names settled |
| `scores/` | The tables and the lookup grades |
