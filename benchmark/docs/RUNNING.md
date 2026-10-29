# Running the benchmark

How to put the 46 questions to a system and score its answers. The rules every run follows are in [METHOD.md](METHOD.md), section 4.

## Before you start

- **Use the same words.** Ask each question exactly as `benchmark/questions/questions.csv` gives it, one question per fresh chat or session, with no instructions
  or follow-up about the question itself. If your system reads a folder, use the column `asked_of_chatgpt`, which names the folder; otherwise use `asked_of_aerospark`.
- **Let the system see only the test folder.** A connector that can see other drives or folders may read the wrong one.
- **Record what you ran.** The model, its setting, the date, and anything you did differently. Save every answer, timed from sending the question to the finished answer.
- **Ask again only where an answer gives you nothing to score.** If an answer stalls or fails, ask again in a fresh chat and score the retry.
- **Check that a copied answer kept its names.** A chat page can fail to show part of an answer (a table without its company column, for example); read the
  answer from the assistant's own record of the chat if it can be opened.
- **Score every answer by the same rules.** A contract counts when the answer names it, by company or file name, as a match; a hedged "possible" is shown both ways.

## ChatGPT, Copilot or another chat assistant with a connected folder

1. `python3 benchmark/contracts/fetch_contracts.py`, then upload `benchmark/contracts/pdf/` to a new Google shared drive named `Benchmark Test`. Keep it flat.
2. In a ChatGPT Business workspace, have an administrator connect Google Drive for the workspace so it is indexed in advance. Wait for the index, and check it by asking about the file you added last.
3. Choose the strongest comparable Thinking model your plan offers, and write down what you chose; model names change. Turn memory and web search off. Start each question in a new chat with the Drive connector attached.
4. Ask each question exactly as the `asked_of_chatgpt` column of [benchmark/questions/questions.csv](../questions/questions.csv) gives it. Save each answer to its own file, named `q01_<question id>.txt` and so on, in this form:

   ```
   QUESTION (id set-no-solicit-of-employees): <the exact words you sent>
   SETTING: <model, effort, memory, web search, date>
   WALL SECONDS (Enter pressed -> response actions appear): <seconds>
   -----
   <the answer, as ChatGPT gave it>
   ```

5. Turn the answers into a run file, read it, and score it. From the repository's root:

   ```
   python3 scoring/chatgpt_run_file.py <your answers folder> results/2026-10-aerospark-chatgpt-claude/answers/aerospark/answers.txt my-run.txt
   python3 scoring/claims_by_code.py my-run.txt my-claims.json
   python3 scoring/score.py my-run.txt my-claims.json --per-question
   ```

   The second argument is only the contract list (any run file over these 99 contracts gives it). The code reader under-reads prose answers
   ([how our run was read](../../results/2026-10-aerospark-chatgpt-claude/METHOD.md), section 1). Check the names it lists as "NOT PLACED" and add them to
   `my-claims.json` by hand, or read the answers yourself.

## Claude

1. Put the 99 contracts in a Google shared drive named `Benchmark Test`, as for ChatGPT. Sign Claude's Google Drive connector in with an account that can see only that drive: the connector does not show Claude the names of shared drives.
2. In claude.ai, connect Google Drive and turn the other connectors off. Turn both memory settings off. Choose the model and effort you want to test, and write down what you chose.
3. Ask each question exactly as the `asked_of_chatgpt` column of [benchmark/questions/questions.csv](../questions/questions.csv) gives it, each in a new chat. Save each answer in the same file form as
   ChatGPT's, and note any question Claude asked you and your reply.
4. Make a run file, read it and score it as in step 5 for ChatGPT. The code reader does not fit Claude's answers
   ([how our run was read](../../results/2026-10-aerospark-chatgpt-claude/METHOD.md), section 1): read the answers yourself, or use a model reader as we did (`scoring/reference/extract_claims.js`).

## Your own system

Write a run file yourself: one `CORPUS` line with the contract list, then one `ANS` line per question with its `id`, the words asked, the time in milliseconds and the
answer ([the run file form](../../results/2026-10-aerospark-chatgpt-claude/answers/README.md)). If your answers cite contracts by id, the code reader can read them as it
reads AeroSpark's; otherwise read them into a claims file and score it with `scoring/score.py`.
