# Claims: how each written answer was read

The scorer needs, for each answer, which contracts it names as a match and which as a possible match. These files hold that: one per system (`claims.json`), a list of
`{"pass": 1, "id": <question>, "claims": {"yes": [...], "possible": [...], "no": [...], "count": N}}`. The numbers are positions in the run file's contract list (its
`CORPUS` line, 1 to 99).

| Folder | Reading |
|---|---|
| `aerospark/` | AeroSpark's answers, read by code (`python3 scoring/claims_by_code.py results/2026-10-aerospark-chatgpt-claude/answers/aerospark/answers.txt <out>` makes it again). A finding that cites a contract names it; the doubt AeroSpark writes into a finding ("Possible match only") makes it possible. `review` lists the findings that are not a plain yes |
| `claude/` | Claude's answers, read by an AI reader (`scoring/reference/extract_claims.js`) that copied out the names each answer gives and whether it affirms or hedges each, twice for every answer (`others` holds the second reading; `agree` says the two agreed). Code placed each name on the contract list; `names` shows what was read, and `unplaced` the names code could not place, with the contract Claude settled each on (`settled_by_claude`, `settled`) |
| `chatgpt/` | ChatGPT's answers, read the same way |

[names_settled_by_claude.md](names_settled_by_claude.md) lists every name Claude settled, with the reason. To use your own reading, write claims in this form and score
them with `python3 scoring/score.py <run file> <your claims>`.

`reference/extract_claims.js` is the model reader as it ran, for its prompt and rules. It ran inside our own codebase (it loads the Anthropic SDK and an API key from
there), so it needs adapting before it runs elsewhere.
