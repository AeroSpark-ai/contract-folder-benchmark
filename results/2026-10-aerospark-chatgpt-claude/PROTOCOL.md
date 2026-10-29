# Protocol: how each system was run

All three were run in October 2026, on the same 99 contracts and the same 46 questions in the same words.

## The folder and the questions

A Google shared drive, "Benchmark Test", holding the 99 contract PDFs, flat. ChatGPT and Claude read it through their Google Drive connections; AeroSpark read the
same contracts added to a workspace through its normal import. ChatGPT and Claude were asked each question with one prefix naming the drive, and no hints,
instructions or follow-ups:

```
In my Google Drive shared drive "Benchmark Test" (all its folders): <the question>
```

AeroSpark was asked the question alone (the `asked_of_aerospark` column of [questions.csv](../../benchmark/questions/questions.csv)); it has only the one folder.

## Claude

**Plan and model.** Claude Max, claude.ai (its merged chat and Cowork mode, not Claude Code), model **Opus 5.5 at effort High**. The setting recorded with every answer:

```
Claude Max plan, claude.ai (merged Claude/Cowork mode, not Code), Opus 5.5 at effort "High", permission mode "Auto", Google Drive connector only (the
account's other connectors off), the Drive connector signed in with an account that is a member of the "Benchmark Test" shared drive only, fresh chat,
Memory OFF (both memory settings paused), code execution network egress OFF, three chats running at once, small batches with the usage meters read
before and after each, plain wording
```

Claude's larger model, Fable 5.1, was not used: its usage limits do not allow a full run of the questions.

**The folder.** Claude's connector lists shared drives without their names (each shows as "Drive"), so it cannot tell from the list which one a question means.
The connector was therefore signed in with an account that is a member of the "Benchmark Test" shared drive only; the account's other shared drive (the practice
pool) was not visible to it.

**The procedure.** Each question in a **new chat**, three at a time, in small batches. The model claude.ai showed (Opus 5.5 High) was checked for every send.
Nothing else was said in any chat. The answer was copied with Claude's Copy button, which takes
the whole turn, including the progress notes Claude writes while it works, and timed from claude.ai's own stored record of the conversation.

**Removed from the recorded answers.** Google Drive file and folder links and ids, claude.ai chat links, and the line giving claude.ai's internal model id.

## ChatGPT

**Plan and model.** ChatGPT Business, Chat mode (not "Work"), model GPT-6 at Thinking effort **High**. The setting recorded with every answer:

```
ChatGPT Business, chat, GPT-6 (= GPT-6 Sol) at Thinking effort "High", Google Drive plugin attached (verified in the composer), fresh chat,
Memory OFF + Web search OFF (Personalization; Fast answers ON, as found), three chats running at once, plain wording
```

Screenshots of the model selector, the memory setting and the web-search setting, cropped to the settings, are in [answers/chatgpt/settings/](answers/chatgpt/settings/).
The same screen shows the other settings as they were: "Fast answers", "Connector search" and "Space search" on.

**Why High.** Every setting was tried on one practice question (38 matching contracts, from the practice pool): High found 30, Extra High 29 and Pro 31. Pro took over
three times as long and is limited to 15 messages a month on Business. Over a longer practice run the default Instant setting often stopped early.

**The folder.** Connected through the workspace administrator's Google Drive connection, which indexes the drive in advance; it was in place before the first question.

**The procedure.** Each question in a **new chat**, with memory and web search off and the Drive connector attached (checked before sending). Three chats ran at once.
The answer was copied with the Copy button, which takes the whole turn (some answers posted a first result and kept working).

**Removed from the recorded answers.** Google Drive file and folder links, ChatGPT chat links, and the workspace's name. Nothing else was changed.

## AeroSpark

A workspace with default settings. The contracts of the folder were added through the normal import, in one batch. The questions were put through the same answer
function AeroSpark's question box uses, over all 99 contracts, one at a time, with nothing changed while they ran.

AeroSpark records, for each contract, which of its standard clause types the contract contains, with a quote from it, and its dates, parties and governing law. A
"which contracts contain [a standard clause]" question is answered from that record, and some date questions are worked out by code from the stored dates.

**Removed from the recorded answers.** Internal diagnostics: per-call technical details, costs, and the record of each internal search step. Everything the answer
says and the contracts it cites are kept.

To ask AeroSpark these questions yourself, in a workspace with the same 99 contracts, email **support@aerospark.ai**.
