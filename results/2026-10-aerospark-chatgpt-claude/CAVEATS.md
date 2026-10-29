# Limits of this run

## What this test does not show

- **One folder.** 99 contracts and 46 questions show large differences reliably, not small ones. How much the order depends on the questions asked is shown by
  redrawing them ([scores/headline.md](scores/headline.md)).
- **The systems as they were.** Claude Max with Opus 5.5 at High, ChatGPT Business with GPT-6 at High, and AeroSpark, each as it was in October 2026. Every system
  changes often, and asked again, any system might name a few more or a few fewer contracts.
- **Clean files only.** Signed, text-based filings; no scans, drafts or earlier versions. Those are harder, probably for every system.
- **Answering questions only.** Approvals, reminders, signature tracking and the other jobs of a contract system were not tested.
- **AeroSpark cannot be re-run from here.** It is a commercial product; the recorded answers are the evidence. To ask it these questions yourself, email support@aerospark.ai.
- **We build AeroSpark.** We chose the questions and wrote our own labels for the clauses CUAD does not label. Every rule is meant to be the same for every system.

## Known weaknesses in the numbers

- **How ChatGPT's and Claude's prose is read is a judgement.** A model reader copied out the names, code placed them, and Claude settled the names code could not place
  from the answer's own words. AeroSpark's answers cite contracts by id and are read by code. The rule for what counts is the same: the contract must be named.
- **Claude's answers include its progress notes.** Claude writes notes while it works ("Batch 3 is back: …"), and its Copy button takes the whole turn, as ChatGPT's does.
  The whole turn was read, as ChatGPT's was.
- **Some contracts are left out of a question.** Where a question needs something the contract or CUAD's labels do not give (a signing date or end date left
  blank or not recorded, or a governing law blacked out in the filing), the key cannot say yes or no for that contract, so it is left out of that question: naming it
  is neither right nor wrong. This affects seven questions; "still in force today", for example, is scored on 55 of the 99 contracts
  ([benchmark/docs/METHOD.md](../../benchmark/docs/METHOD.md), section 3).
- **Our own labels** (7 questions) were read by two AI readers and their 13 disagreements settled by us against written definitions; no lawyer has re-read them.
  Both readings and every settlement are in [benchmark/key/our_labels/](../../benchmark/key/README.md).
- **Timing differs in method.** AeroSpark is timed inside its service, Claude from claude.ai's stored record of each conversation, ChatGPT in the browser or from its
  stored record ([METHOD.md](METHOD.md), section 2).
