# The answers, as recorded

| Folder | What |
|---|---|
| [by_question/](by_question/README.md) | **Start here.** One page per question: the words asked, the key, each system's answer, and which contracts each got right, wrong and missed |
| `aerospark/` | AeroSpark's 46 answers: `answers.txt` |
| `claude/` | Claude Opus 5.5's 46 answers: `answers.txt` |
| `chatgpt/` | ChatGPT's 46 answers: `answers.txt`; `settings/` has cropped screenshots of the model, memory and web-search settings |

## Run files

Each `answers.txt` is one line per record, `KEYWORD <json>`:

- `CORPUS`: the system, the run, and the contract list in the order the claims number it: `order` (AeroSpark's contract ids; `benchmark/contracts/contracts.csv` maps
  them to file names), `files` and `parties`. The three files list the contracts in the same order.
- `ANS`: one per question, in the order of [questions.csv](../../../benchmark/questions/questions.csv). `id`, the words asked `q`, `ms` (milliseconds to the
  finished answer), `error`, and `summary` (the written answer; for ChatGPT and Claude, the whole answer verbatim). AeroSpark's also carry `findings` (each point with the
  contracts it cites, by id, in `req`), `tally` (counts, with the contracts counted) and two notes the page shows (`clauseNote`, `scaleNote`).

## What was removed

- From AeroSpark's answers: internal diagnostics (per-call technical details, costs, and each internal search step's record).
- From ChatGPT's answers: Google Drive file and folder links, ChatGPT chat links, and the workspace's name.
- From Claude's answers: Google Drive file and folder links and ids, claude.ai chat links, and the line with claude.ai's internal model id.
