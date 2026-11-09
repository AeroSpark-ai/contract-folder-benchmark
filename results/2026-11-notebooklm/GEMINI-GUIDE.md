# Asking Gemini about a folder of contracts: what worked for us

In November 2026 we put the benchmark's 46 questions about 99 contracts to Google's Gemini on a Google Workspace work account, three ways. One worked far better than the other two. This is
what we would tell someone who keeps contracts in Google Drive and wants Gemini to answer questions about all of them.

## Use NotebookLM, with the contracts as its sources

NotebookLM (Google now calls it Gemini Notebook) scored 83.5 out of 100: about three in four of the contracts each list question should name, every one-contract lookup right, and a median of under a
minute per question. That puts it level with ChatGPT and a little behind Claude on the same questions ([all five systems](../COMPARISON.md)).

The other two ways did much worse for us:

- **The Gemini app** (gemini.google.com) with the Google Workspace connector. You can't point it at one folder; it searches your Workspace. It often answered from the wrong files (another shared drive,
  unrelated company documents), said it had no access, or failed with an error after several minutes. Before we upgraded our Workspace plan, its strongest model answered about two questions every few
  hours before switching to a lighter one. We stopped after 15 of the questions.
- **Gemini in Google Drive**, the Ask Gemini button on the folder itself. It mostly stays in the folder, and it's quick (about 40 seconds), but it read only a few files for each answer and often said it
  had only an excerpt of a file. It named fewer than one in five of the contracts the key lists. And with only the contract folder chosen, our own write-up of this benchmark still turned up as a
  source twice.

## Setting up the notebook

1. **Check your plan.** Third-party guides put the free tier at 50 sources a notebook; ours, on a Business Standard trial, showed a limit of 300. You need room for every contract.
2. **Add the contracts from Drive.** Add sources, then Google Drive, then your shared drive, and select the files. The picker takes 50 files at a time, so add a large folder in batches, and check that the
   notebook's source count matches the number of contracts.
3. **Wait** until every source has finished processing before you ask anything.
4. **Turn off the chat's Google Drive switch** if you want answers from the contracts only. It's in the menu next to the chat box, and it's on by default. With it on, the chat can also search the rest of
   your Drive: drafts, old versions, notes about the contracts. With it off, every one of NotebookLM's citations opened one of our 99 contracts.
5. **Leave web research off.** When NotebookLM can't find something, it offers to search the web. For questions about your own contracts, say no.

## Asking

- **One question per conversation.** We cleared the chat history before each question so that no earlier answer steered the next. (We didn't test leaving it in.)
- **Check its count against its own list.** Twice it gave a number one short of the list it wrote (33 for a list of 34, 67 for 68).
- **Click the citations.** Each number opens the passage it relied on. Where the answer shows "[suspicious link removed]" in place of a company name, the citation shows which contract it means.
- **If an answer looks thin, ask again in a fresh conversation.** On one question the second ask found 7 of the 9 contracts, against 2 the first time.

## Where it was weakest

- **Long lists of one clause.** It found 20 of the 54 contracts that cap liability, and 7 of the 14 with no end date. On a list question, expect it to miss some.
- **One count.** Asked how many contracts give a right of first refusal, offer or negotiation, it said 9, then 6 on a second ask; there are 13. Every system in the benchmark got that count wrong.
- **Waiting.** Most answers took under a minute; the slowest took five, most of it spent on "Verifying Dates and Parties...".

## What we didn't test

- Whether NotebookLM picks up a contract added to the folder after the notebook was made, or a change to one already in it. Until you know, add new contracts to the notebook yourself.
- Gemini in Drive with "Let Gemini search for sources" switched on, which might read more files but would also search the rest of your Drive and email.
- Gemini's Deep Research.
