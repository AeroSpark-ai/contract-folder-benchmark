# The answer key

| File | What |
|---|---|
| `key.json` | **The key.** One entry per question: its number, words, where its key comes from (`key_from`: CUAD, ours, or CUAD + ours; `source` says which labels), and its `truth`. Also the six contracts whose term is taken from the text for the date questions (`terms_settled_from_text`) |
| `our_labels/definitions.json` | The meaning of each item we labelled, in plain words, written before any reading |
| `our_labels/reader_instructions.md`, `reader_schema.json` | What each reader was given with the contract text, and the form of its answer |
| `our_labels/reading_claude.json` | Claude Opus 5.5's reading of all 99 contracts: for each item yes or no, with the contract's own words and section for a yes, and a reason |
| `our_labels/reading_chatgpt.json` | ChatGPT GPT-6.1 Sol's reading, the same way |
| `our_labels/settlements.json` | The 13 readings the two disagreed on, each settled by us: by one of four rules, or as a close call on the contract text |
| `our_labels/labels.json` | The final labels: the two readings where they agree, the settlements where they do not |

The readers labelled six items. Five are used: arbitration, confidentiality, agreement_confidential and indemnification (each a question of its own) and
warranties (with CUAD's renewal labels, in "auto-renew and include a warranty"). The sixth, auto-renewal, was read but is not used: the auto-renewal questions use
CUAD's Renewal Term labels.

## `truth` in `key.json`

- `files`: the contracts that should be named, by CUAD's file name, usually from one CUAD column (`column`). `count: true` means a count question, scored on the number.
  `skip` lists contracts the labels cannot settle for that question; naming one is neither found nor wrong. `weak`, `rule` and `as_of` describe a question whose key
  is weak or depends on the date.
- `value`: the expected answer to a one-contract question (`expected`), the contract (`file`) and a note.
- `absent`: the question is about a contract that is **not in the folder** (`contract_outside_folder` is the CUAD contract it was drawn from). The right answer says it is not there.

CUAD's file names match the PDFs after folding punctuation and accents; `benchmark/contracts/contracts.csv` gives both (`key_name` and `file_name`).

## How to check a label

Pick a question, take a contract from its list, fetch the contracts (`benchmark/contracts/fetch_contracts.py`) and find the clause the question asks about. For one of
our labels, both readers' quotes are in `our_labels/`; any other label is CUAD's. [docs/CHALLENGE.md](../docs/CHALLENGE.md) says how to dispute one.
