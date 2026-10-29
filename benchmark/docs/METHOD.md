# Method: the contracts, the questions, the answer key and the scoring rules

What the benchmark is made of and how an answer is scored. How our own October 2026 run was carried out and scored is in
[its own method](../../results/2026-10-aerospark-chatgpt-claude/METHOD.md).

## 1. The contracts

- **Source.** CUAD v1: 510 commercial contracts from public SEC filings, each labelled by lawyers for 41 clause categories plus parties and dates. The Atticus Project, CC BY 4.0.
- **The draw.** Before any system saw any of them, the 510 were split by a seeded random draw (seed 20261008), stratified by CUAD contract type, into a test pool, a practice pool and a reserve.
  The practice pool was used to develop the questions and AeroSpark; it is not part of this release.
- **The folder.** 99 contracts drawn at random within each contract type from the test pool, listed in `benchmark/contracts/contracts.csv`.
- Every contract is a signed, text-based filing. There are no scans and no drafts.

## 2. The questions

46 questions in plain English, the same words for every system:

| Kind | Questions | Scored |
|---|---|---|
| Find every contract with a clause | 14 | on the contracts named |
| Two or three conditions at once | 4 | on the contracts named |
| Dates against a stated day | 6 | on the contracts named |
| The most recent, the shortest notice | 2 | on the contracts named |
| By party, by type, notice period, either of two clauses | 4 | on the contracts named |
| Counts | 5 | on the number given |
| One fact about one named contract | 9 | by reading |
| A contract that is not in the folder | 2 | by reading: the right answer says it is not there |

No question's text, and no run of six words in a row from one, appears in AeroSpark's software,
and no practice-pool company name; an automated test in AeroSpark's code fails if one does. The exact words: `benchmark/questions/questions.csv`.

## 3. The answer key

**From CUAD's labels** (39 questions). For "every contract with clause X", the key is the contracts CUAD labels "yes" for X; for a count, the contracts the
same labels give; for a lookup, CUAD's label for that contract. The date questions are worked out from CUAD's date and renewal labels; for six
contracts whose own text departs from CUAD's renewal labels, the term is taken from the text, and the six are listed in the key (`terms_settled_from_text`).

**From our own labels** (7 questions). CUAD does not label arbitration, confidentiality, the agreement itself being confidential, indemnification or warranties. For those:

- **The meaning first.** Each item's meaning was written down in plain words before any reading (`benchmark/key/our_labels/definitions.json`).
- **Two readers.** Two AI readers, Claude Opus 5.5 and ChatGPT GPT-6.1 Sol, each read all 99 contracts, given only the definitions and the contract text
  (`reader_instructions.md`). Each answered yes or no for each item, with the contract's own words and section for every yes, and a reason.
- **The disagreements settled.** The two agreed on 581 of the 594 readings. Each of the other 13 was settled by us against the definitions: eight by one of four
  rules (a recital is not a warranty; an indemnity only in another agreement does not count; a document marking or SEC redaction notice is not a contract term;
  a duty only to keep a password secret is not a confidentiality provision), five as close calls decided on the contract text (`settlements.json`).
- Three questions combine a CUAD label with one of ours (Texas law and confidentiality; auto-renewal and a warranty; a no-solicit and the agreement confidential).

**Contracts a question leaves out.** Where the labels cannot settle a contract for a question, it is on that question's `skip` list, and naming it is neither found nor
wrong. "Still in force today" is scored on the 55 contracts whose labels can settle it, as of October 2026, when every system answered (the set is the same on every
day of that month from the 13th on). "No fixed end date": the 35 contracts with no end-date label are left out. Coherus's governing law is redacted, so it is left
out of "governing law outside the US".

## 4. How answers are scored

- **A contract counts only if the answer names it**, by company or file name, as a match. A generic title with no name ("Content License Agreement", company blank) does not count.
- **A system's own hedge counts the same way for all.** A contract an answer calls "possible", "needs review" or "unconfirmed" is shown both ways: not credited in the
  score, and credited (or counted wrong) in the "possible credited too" figures.
- **The score.** Every question counts the same, out of 100. A list question earns the share of the key's contracts the answer named as a match; a count earns 1 if the
  number is right; a lookup or a not-in-the-folder question earns 1 if it is graded right by reading (`results/2026-10-aerospark-chatgpt-claude/scores/graded_by_reading.md`).
  The score is the average over the 46.
- **Also shown.** The contracts found across the 30 list questions, added up (a question with 70 contracts in the key then weighs 70 times one with 1), and the
  contracts named that are not in the key ("wrong").
- **How much the order depends on the questions asked.** The 46 questions are redrawn at random 10,000 times (seeded), each redraw the same size, and the score worked
  out again each time; the spread of the difference between two systems shows how much of a lead would survive a different set of questions.
