# The Contract Folder Test

A benchmark for one question: **can a system answer what a business asks about its contracts when the contracts sit in a folder?** Not one contract at a time,
but the whole folder: which contracts contain a given clause, how many are governed by a given law, which are still in force.

It is built for anyone who wants to measure a system that reads a folder of contracts: a general assistant connected to a drive (ChatGPT, Claude, Copilot), a
contract repository, or an agent of your own.

## What the benchmark is

- **99 real commercial contracts** from public SEC filings, drawn at random across contract types from [CUAD](https://doi.org/10.5281/zenodo.4595826), the
  Contract Understanding Atticus Dataset, whose clauses, parties and dates were labelled by lawyers. The PDFs are fetched from CUAD and checked against a SHA-256 for each.
- **46 plain-English questions**:

  | Kind | Questions | Example |
  |---|---|---|
  | Find every contract with a clause | 14 | "Which of these contracts contain a no-solicit of employees provision?" |
  | Two or three conditions at once | 4 | "Which contracts are governed by Texas law and include a confidentiality provision?" |
  | Dates against a stated day | 6 | "Which of these contracts are still in force today?" |
  | The most recent, the shortest notice | 2 | "Which contract requires the shortest notice to stop it from renewing?" |
  | By party, by type, notice period, either of two clauses | 4 | "Which of these contracts are hosting agreements?" |
  | Counts | 5 | "How many of these contracts are governed by the laws of Texas? Give the number and list them." |
  | One fact about one named contract | 9 | "What law governs the Cooperation Agreement between Otkritie Investments Cyprus Limited and QIWI plc?" |
  | A contract that is not in the folder | 2 | "What law governs the Master Services Agreement between Clear Capital and Radial Spark, LLC?" |

- **An answer key** for every question. 39 of the 46 are keyed from CUAD's labels as CUAD publishes them (the date questions are worked out from its date
  and renewal labels). The other 7 ask about clauses CUAD does not
  label (arbitration, confidentiality, the agreement itself being confidential, indemnification, and warranties in a combined question). For those we wrote
  the meaning of each clause down first, two AI readers read every contract against it, and we settled their disagreements one by one. The definitions,
  both readings and every settlement are here.
- **Scoring rules** that are the same for every system. Every question counts the same, out of 100: a question that asks which contracts have something earns
  the share of the key's contracts the answer names; a count, a lookup or a question about a contract not in the folder is right or not. A contract counts
  only when the answer names it, by company or file name, as a match; a contract the answer itself calls "possible" is shown both ways.

The full method: [benchmark/docs/METHOD.md](benchmark/docs/METHOD.md).

## Run it

1. **Get the contracts.** `python3 benchmark/contracts/fetch_contracts.py` downloads CUAD v1 and extracts the 99 PDFs into `benchmark/contracts/pdf/`, checking each one.
2. **Put them where your system reads.** A Google or SharePoint shared drive, a folder your agent can open, or an import into your contract tool. Let the system see only
   this folder.
3. **Ask the 46 questions** from [benchmark/questions/questions.csv](benchmark/questions/questions.csv) in their exact words, each in a fresh chat or session, and save every answer with its time.
4. **Score the answers** with the standard-library Python in [scoring/](scoring/): turn the answers into a run file, read which contracts each answer names, and score them against the key.

Step by step, for chat assistants and other systems: [benchmark/docs/RUNNING.md](benchmark/docs/RUNNING.md).

## Results

Each run is kept in [results/](results/README.md) with every answer as recorded, how each answer was read, and the code that re-makes its tables. The first is our own,
[October 2026: AeroSpark, Claude and ChatGPT Business](results/2026-10-aerospark-chatgpt-claude/README.md): out of 100, **AeroSpark 89.8, Claude 85.6, ChatGPT 82.2**.
AeroSpark answered all 46 questions in under a minute each (median 10 seconds); Claude and ChatGPT took about six minutes a question. A second run,
[Claude's Tabular review](results/2026-10-claude-tabular-review/README.md), put the same questions to the table-building tool Anthropic released on 28 October 2026: 83.9.

**We build AeroSpark**, a contract repository, and wrote this benchmark. That is why everything is public: the contracts, the questions, the key and how it was made,
the scoring code and every recorded answer. If you run it, we would like to see your results; if you disagree with a label, a reading or a rule,
[benchmark/docs/CHALLENGE.md](benchmark/docs/CHALLENGE.md) says how to raise it.

## What is here

| | |
|---|---|
| [benchmark/contracts/](benchmark/contracts/contracts.csv) | The 99 contracts: file name, parties, type, pages, SHA-256, and the script that fetches them from CUAD |
| [benchmark/questions/](benchmark/questions/questions.csv) | The 46 questions, in the exact words to ask, with how each is scored and where its key comes from |
| [benchmark/key/](benchmark/key/README.md) | The answer key, and our own labels for the clauses CUAD does not label: definitions, both readings, the settlements |
| [benchmark/docs/](benchmark/docs/) | [Method](benchmark/docs/METHOD.md), [running the benchmark](benchmark/docs/RUNNING.md), [how to challenge](benchmark/docs/CHALLENGE.md) |
| [scoring/](scoring/) | The scorer, the code reader for written answers, and the model reader's prompt; standard-library Python, no dependencies |
| [results/](results/README.md) | Runs of the benchmark, each with its answers, readings, scores and caveats |

## Licence and citation

The contracts and CUAD's labels are the Contract Understanding Atticus Dataset (CUAD) v1 by The Atticus Project, under CC BY 4.0
([10.5281/zenodo.4595826](https://doi.org/10.5281/zenodo.4595826)). The data we made is under CC BY 4.0 ([LICENSE-DATA.md](LICENSE-DATA.md)); the code under MIT
([LICENSE](LICENSE)). Please cite this repository and CUAD ([CITATION.cff](CITATION.cff)). Contact: support@aerospark.ai.
