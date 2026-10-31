# October 2026 run: AeroSpark, Claude and ChatGPT Business

Our own run of [the Contract Folder Test](../../README.md): the same 46 questions about the same folder of 99 contracts, put to **Claude Max** (Opus 5.5 at High) and
**ChatGPT Business** (GPT-6 at High), each reading the folder through its Google Drive connection, and to **AeroSpark**, a contract repository. All runs were made
in October 2026.

**We build AeroSpark.** So everything needed to check this run is here: every system's answers word for word, how each answer was read, and the code that scores them.

## The result

Every question counts the same, out of 100: a question that asks which contracts have something earns the share of the key's contracts the answer names as a match;
a count, a lookup or a question about a contract not in the folder is right or not.

| | AeroSpark | Claude | ChatGPT |
|---|---|---|---|
| **Score out of 100** | **89.8** | **85.6** | **82.2** |
| Contracts found, the 30 list questions (576 in the key) | 490 (85%) | 463 (80%) | 427 (74%) |
| Contracts named that are not in the key | 24 | 12 | 5 |
| Counts right (of 5) | 4 | 4 | 4 |
| Lookups right (of 11) | 11 | 11 | 11 |
| Median time per question | 10 s | 5.6 min | 5.9 min |
| All 46 questions | 9 minutes | 4.0 hours | 4.8 hours |

- **Finding contracts.** AeroSpark found the most contracts and named more that are not in the key; ChatGPT named the fewest that are not in the key. All three got
  the same four of the five counts right (each missed the count of contracts with a right of first refusal) and all eleven lookups.
- **Redrawing the questions.** With the 46 questions redrawn at random 10,000 times, AeroSpark stays ahead of Claude in 99.9% of redraws (by 1.5 to 7.1 points in
  95% of them) and of ChatGPT in 100.0% of them (by 3.4 to 12.9).
- **Time.** AeroSpark answered all 46 in under a minute each; its slowest took 35 seconds. Claude and ChatGPT typically took five to ten minutes a question.

Every figure is made by `scoring/reproduce.py` from the recorded answers ([scores/headline.md](scores/headline.md), by kind of question and with the contracts each system
hedged as "possible" credited too). The lookups are graded in [scores/graded_by_reading.md](scores/graded_by_reading.md). The limits of the run are in [CAVEATS.md](CAVEATS.md).

## How each system was run

- **Claude Max**, Opus 5.5 at High, with Google Drive its only connection and memory off. Claude's Drive connection lists shared drives without their names, so it was
  signed in to an account that can see only this folder's drive.
- **ChatGPT Business**, GPT-6 at High, in chat with memory and web search off, reading the shared drive through the workspace's Google Drive connection.
- **AeroSpark**, a workspace with default settings and the 99 contracts added through its normal import.

Every system got the same 46 questions in the same words, one per fresh chat, with no instructions or follow-up about the question itself. The exact settings and steps
are in [PROTOCOL.md](PROTOCOL.md).

## Check it yourself

```
python3 results/2026-10-aerospark-chatgpt-claude/scoring/reproduce.py          # re-score every recorded answer: every table here, in seconds, no accounts
```

- **Read the answers.** [answers/by_question/](answers/by_question/README.md) has one page per question: the words asked, the key, each system's answer, and which
  contracts it got right, got wrong and missed.
- **Check the key.** CUAD's labels are CUAD's; for our own labels, both readers' quotes and every settlement are in [benchmark/key/](../../benchmark/key/README.md).
- **Ask AeroSpark yourself.** To put these questions to AeroSpark in a workspace with these 99 contracts, email **support@aerospark.ai**.
- **Disagree?** Open an issue: [CHALLENGE.md](../../benchmark/docs/CHALLENGE.md) says how.

## What is in this folder

| | |
|---|---|
| [answers/](answers/README.md) | Every system's answers as recorded, and one readable page per question |
| [claims/](claims/README.md) | How each written answer was read into "this contract is named" |
| [scores/](scores/headline.md) | The numbers, question by question, and the questions graded by reading |
| [scoring/](scoring/) | `reproduce.py`, which re-makes every table here with the shared scorer in [scoring/](../../scoring/) |
| [METHOD.md](METHOD.md) | How this run was scored: how answers were read, and timing |
| [PROTOCOL.md](PROTOCOL.md) | The exact settings, words and steps for each system |
| [CAVEATS.md](CAVEATS.md) | What this run does not show |
