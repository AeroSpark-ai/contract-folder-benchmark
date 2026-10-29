# Method: how this run was carried out and scored

The October 2026 run of AeroSpark, Claude and ChatGPT Business. The benchmark itself (the contracts, the questions, the key and the scoring rules) is in
[benchmark/docs/METHOD.md](../../benchmark/docs/METHOD.md). The limits of this run are in [CAVEATS.md](CAVEATS.md).

## 1. How an answer is read into "the contracts it names"

The scorer needs, for each answer, the contracts it names as a match and as a possible match: the **claims** file (`claims/`).

- **AeroSpark** answers cite contracts by id, and write any doubt into the finding ("Possible match only"). `scoring/claims_by_code.py` reads them; no model is involved.
  A count is the number in the answer's own tally (its groups added up, so "England 3, England and Wales 1" is 4).
- **ChatGPT and Claude** answers are prose: short company names, links and tables. They were read by an AI reader (Claude Haiku, temperature 0; the prompt is in
  `scoring/reference/extract_claims.js`) that copied out each name the answer gives and whether it is affirmed or hedged, twice for every answer (the two readings
  agreed). Code then placed each name on the contract list; the names it could not place were settled by Claude from the answer's own words
  ([claims/names_settled_by_claude.md](claims/names_settled_by_claude.md)).
- **The rule is the same for all three:** a contract counts only if the answer names it, by company or file name. The readers differ because the answers do: ids
  for AeroSpark, prose for the other two. A plain code reader does not fit the prose answers: it misses short company names ("Corio" for the Corio license and
  hosting agreement), and it takes the contracts Claude lists as *not* counted as claims.

ChatGPT's and Claude's answers carry no contract ids, so how they are read is a judgement. All the claims are here, so you can use your own.

## 2. Timing

- **AeroSpark** is timed inside its service, from the question to the finished answer; that is about a second less than a person would wait.
- **Claude** is timed from claude.ai's own stored record of each conversation: from the message the answer replies to until its last work finished.
- **ChatGPT** is timed on questions 1 to 35 in the browser, from pressing Enter until the answer's action buttons appeared, and on questions 36 to 46 from ChatGPT's
  own stored record of each conversation, from the question to its last message.
- ChatGPT and Claude were run three chats at a time.
