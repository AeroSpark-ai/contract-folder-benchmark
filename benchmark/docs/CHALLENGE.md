# Disagree with something? How to challenge it

Open an issue in this repository; there is a template for each kind. For anything you would rather not post publicly, email support@aerospark.ai.

1. **"This label in the answer key is wrong."** Give the question id, the contract's file name, and the passage in the contract that settles it. For one of our own
   labels, say which definition in [key/our_labels/definitions.json](../key/our_labels/definitions.json) you are applying; for a CUAD label, which CUAD category. We
   decide the label again from the contract text, not from any system's answer, publish the decision with the quote, and re-run
   `results/2026-10-aerospark-chatgpt-claude/scoring/reproduce.py`. If a number changes, we add a line to
   [CAVEATS.md](../../results/2026-10-aerospark-chatgpt-claude/CAVEATS.md) saying what changed. If the disagreement is about a definition itself, we will show the result both ways.
2. **"This answer was read wrongly."** Give the question id, the system, and the contract the answer does or does not name, with the words. The claims that decide this are in
   [claims/](../../results/2026-10-aerospark-chatgpt-claude/claims/README.md), and the answers in
   [answers/by_question/](../../results/2026-10-aerospark-chatgpt-claude/answers/by_question/README.md).
3. **"I ran it again and got something different."** Give the model and setting, the date, and your answers as a run file ([RUNNING.md](RUNNING.md)), with your score.
   We want more runs, of newer models especially, and will list the ones we can reproduce.
4. **"A rule is unfair to one side."** Say which rule and which way it tilts. Every rule is in [METHOD.md](METHOD.md).

We will answer in the issue, and we will not change an answer, a label or a score without a line in CAVEATS.md.
