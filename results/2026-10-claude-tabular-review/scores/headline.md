# Tabular review beside the other three systems, re-scored from the recorded answers

Made by `python3 results/2026-10-claude-tabular-review/scoring/reproduce.py --write`.

| | AeroSpark | Plain Claude | Tabular review | ChatGPT |
|---|---|---|---|---|
| **Score out of 100** | **89.8** | **85.6** | **83.9** | **82.2** |
| Contracts found, the 30 list questions (576 in the key) | 490 (85%) | 463 (80%) | 452 (78%) | 427 (74%) |
| Contracts named that are not in the key | 24 | 12 | 23 | 5 |
| Found, with the contracts each hedged as "possible" credited too | 508 (29 not in the key) | 495 (61 not in the key) | 482 (23 not in the key) | 462 (27 not in the key) |
| Counts right (of 5) | 4 | 4 | 4 | 4 |
| Lookups right (of 11) | 11 | 11 | 11 | 11 |
| Questions answered in under a minute | 46 | 11 | 24 | 8 |
| Median time per question | 10 s | 5.6 min | 42 s | 5.9 min |

Redrawing the 46 questions 10,000 times: plain Claude minus Tabular review is -1.5 to +6.3 in 95% of redraws, and plain Claude is ahead in 80.1% of them. Every pair: [COMPARISON.md](../../COMPARISON.md).

Each cell is the result, then the time to answer. Tabular review's times are rounded.

| # | Question | Key | AeroSpark | Plain Claude | Tabular review | ChatGPT | How Tabular answered |
|---|---|---|---|---|---|---|---|
| 1 | Which of these contracts contain a revenue or profit sharing provision? | 33 | 31 found, 2 wrong, 22 s | 27 found, 1 wrong, 4.7 min | 24 found, 2 wrong, 3.5 min | 26 found, 2 wrong, 9.3 min | Topic |
| 2 | Which of these contracts contain a right of first refusal, offer or negotiation? | 13 | 9 found, 1 wrong, 15 s | 10 found, 0 wrong, 8.6 min | 9 found, 0 wrong, 2.7 min | 7 found, 0 wrong, 8.1 min | Topic |
| 3 | Which of these contracts contain an irrevocable or perpetual license? | 17 | 17 found, 1 wrong, 16 s | 16 found, 1 wrong, 4.9 min | 16 found, 1 wrong, 3.1 min | 16 found, 1 wrong, 8.1 min | Topic |
| 4 | Which of these contracts contain a joint IP ownership provision? | 11 | 6 found, 0 wrong, 13 s | 7 found, 0 wrong, 9.6 min | 8 found, 0 wrong, 2.6 min | 6 found, 0 wrong, 5.4 min | Topic |
| 5 | Which of these contracts contain a no-solicit of employees provision? | 13 | 12 found, 0 wrong, 13 s | 12 found, 0 wrong, 5.4 min | 12 found, 0 wrong, 2.1 min | 11 found, 0 wrong, 7.2 min | Topic |
| 6 | Which of these contracts contain an unlimited-usage license? | 5 | 3 found, 0 wrong, 11 s | 3 found, 0 wrong, 8.7 min | 3 found, 1 wrong, 2.2 min | 3 found, 1 wrong, 6.7 min | Topic |
| 7 | How many of these contracts are governed by the laws of Texas? Give the number and list them. | 7 | said 7, 10 s | said 7, 2.7 min | said 7, 2.7 min | said 7, 5.6 min | Topic |
| 8 | How many of these contracts are governed by the laws of Illinois? Give the number and list them. | 3 | said 3, 6 s | said 3, 1.6 min | said 3, 2.7 min | said 3, 2.0 min | Topic, column rewritten |
| 9 | How many of these contracts are governed by the laws of England? Give the number and list them. | 4 | said 4, 6 s | said 4, 7.7 min | said 4, 18 s | said 4, 5.9 min | Reuse |
| 10 | How many of these contracts are governed by the laws of Canada? Give the number and list them. | 4 | said 4, 8 s | said 4, 3.4 min | said 4, 18 s | said 4, 6.0 min | Reuse |
| 11 | How many of these contracts give a party a right of first refusal, offer or negotiation? | 13 | said 10, 13 s | said 11, 7.3 min | said 9, 18 s | said 7, 8.8 min | Reuse |
| 12 | What law governs the Yield Maintenance Agreement between Wells Fargo Bank on behalf of Wells Fargo Mortgage Backed Securities 2006-6 Trust and UBS AG? |  | right, 6 s | right, 13 s | right, 18 s | right, 30 s | Reuse |
| 13 | What law governs the Cooperation Agreement between Otkritie Investments Cyprus Limited and QIWI plc? |  | right, 6 s | right, 13 s | right, 18 s | right, 42 s | Reuse |
| 14 | When was the Limited Power Of Attorney between FEDERATED INVESTMENT MANAGEMENT COMPANY and FEDERATED ADVISORY SERVICES COMPANY entered into? |  | right, 5 s | right, 11 s | right, 36 s | right, 31 s | Re-ask |
| 15 | When does the initial term of the Supply Agreement between HOVIONE INTER AG and INTERSECT ENT, Inc end? |  | right, 4 s | right, 12 s | right, 36 s | right, 33 s | Re-ask |
| 16 | When does the initial term of the Manufacturing Outsourcing Agreement between Nice Systems Ltd and Flextronics Israel Ltd end? |  | right, 7 s | right, 15 s | right, 42 s | right, 1.2 min | Re-ask |
| 17 | Who is the other party to the Master Operation And Maintenance Agreement with BLOOM ENERGY CORPORATION? |  | right, 6 s | right, 9 s | right, 42 s | right, 25 s | Re-ask |
| 18 | Who is the other party to the Co-Branding Agreement with Lucent Technologies Inc? |  | right, 5 s | right, 9 s | right, 42 s | right, 22 s | Re-ask |
| 19 | What is the renewal term of the Software License And Maintenance Agreement between GARMAN ROUTING SYSTEMS, INC and SPARKLING SPRING WATER GROUP LIMITED? |  | right, 6 s | right, 14 s | right, 42 s | right, 42 s | Re-ask |
| 20 | How much notice is needed to stop the Co-Branding Agreement between VerticalNet, Inc and PaperExchange.com, LLC from renewing? |  | right, 6 s | right, 13 s | right, 18 s | right, 32 s | Opened contract |
| 21 | Which contract requires the shortest notice to stop it from renewing? | 3 | 3 found, 1 wrong, under 1 s | 2 found, 0 wrong, 9.8 min | 2 found, 0 wrong, 3.0 min | 2 found, 0 wrong, 12.2 min | Topic |
| 22 | Which of these contracts was entered into most recently? | 1 | 1 found, 1 wrong, under 1 s | 1 found, 1 wrong, 1.1 min | 1 found, 0 wrong, 3.5 min | 1 found, 0 wrong, 2.6 min | Topic, follow-up |
| 23 | Which of these contracts were entered into between January 1, 2008 and December 31, 2012? | 9 | 8 found, 0 wrong, under 1 s | 7 found, 0 wrong, 4.3 min | 7 found, 0 wrong, 1.0 min | 8 found, 0 wrong, 8.4 min | Reuse, follow-up |
| 24 | Which of these contracts were entered into before January 1, 2001? | 14 | 14 found, 0 wrong, under 1 s | 14 found, 0 wrong, 7.0 min | 14 found, 0 wrong, 30 s | 14 found, 0 wrong, 7.1 min | Reuse |
| 25 | As of July 1, 2020, which of these contracts had an initial term due to end within the next 12 months? | 5 | 5 found, 0 wrong, under 1 s | 4 found, 0 wrong, 7.7 min | 4 found, 0 wrong, 5.0 min | 4 found, 0 wrong, 11.1 min | Topic, 4 reads failed |
| 26 | Which of these contracts run until a party ends them, with no fixed end date? | 14 | 11 found, 0 wrong, 11 s | 8 found, 0 wrong, 7.8 min | 7 found, 0 wrong, 1.0 min | 7 found, 0 wrong, 17.9 min | Re-ask |
| 27 | As of July 1, 2016, which of these contracts had a deadline within the next six months for giving notice to stop an automatic renewal? | 3 | 3 found, 2 wrong, 17 s | 3 found, 0 wrong, 11.2 min | 3 found, 0 wrong, 30 s | 2 found, 0 wrong, 7.5 min | Reuse |
| 28 | Which of these contracts are still in force today? | 28 | 28 found, 4 wrong, under 1 s | 23 found, 0 wrong, 9.8 min | 0 found, 0 wrong, 5.2 min | 0 found, 0 wrong, 19.4 min | Topic, re-ask, follow-up |
| 29 | Which contracts entered into after December 31, 2010 restrict a party from soliciting the other party's employees? | 9 | 9 found, 0 wrong, 20 s | 8 found, 0 wrong, 5.1 min | 9 found, 0 wrong, 30 s | 8 found, 0 wrong, 8.5 min | Reuse |
| 30 | Which contracts restrict soliciting the other party's employees or give a right of first refusal, offer or negotiation? | 25 | 19 found, 1 wrong, 21 s | 20 found, 0 wrong, 10.6 min | 20 found, 0 wrong, 30 s | 17 found, 0 wrong, 14.7 min | Reuse |
| 31 | Which contracts is Beijing Yisheng Leju Information Services Co., Ltd a party to? | 2 | 2 found, 0 wrong, 12 s | 2 found, 0 wrong, 25 s | 2 found, 0 wrong, 4.0 min | 2 found, 0 wrong, 1.9 min | Topic, follow-up |
| 32 | Which of these contracts are hosting agreements? | 4 | 4 found, 0 wrong, 20 s | 4 found, 0 wrong, 34 s | 3 found, 0 wrong, 30 s | 4 found, 0 wrong, 2.1 min | Reuse, file names |
| 33 | Which contracts require at least 60 days' notice to stop them from renewing? | 9 | 7 found, 0 wrong, 8 s | 5 found, 0 wrong, 5.7 min | 5 found, 0 wrong, 30 s | 6 found, 0 wrong, 18.0 min | Reuse |
| 34 | When does the initial term of the Intellectual Property Agreement between Marv Enterprises, LLC and Premier Biomedical, Inc end? |  | right, 7 s | right, 1.2 min | right, 30 s | right, 5.4 min | Reuse |
| 35 | What law governs the Master Services Agreement between Clear Capital and Radial Spark, LLC? |  | right, 6 s | right, 5.5 min | right, 18 s | right, 4.0 min | Reuse |
| 36 | Which of these contracts contain a non-compete or exclusivity clause? | 39 | 34 found, 7 wrong, 32 s | 38 found, 9 wrong, 8.1 min | 37 found, 13 wrong, 3.0 min | 35 found, 0 wrong, 7.1 min | Topic |
| 37 | Which contracts contain governing law provisions outside of the US? | 15 | 15 found, 0 wrong, 12 s | 15 found, 0 wrong, 7.8 min | 15 found, 0 wrong, 18 s | 15 found, 0 wrong, 6.7 min | Reuse |
| 38 | Which of these contracts contain an auto-renewal provision? | 28 | 18 found, 0 wrong, under 1 s | 15 found, 0 wrong, 7.2 min | 13 found, 0 wrong, 30 s | 17 found, 0 wrong, 10.3 min | Reuse |
| 39 | Which of these contracts require most disputes be settled by arbitration? | 21 | 19 found, 0 wrong, 20 s | 20 found, 0 wrong, 6.2 min | 20 found, 0 wrong, 3.0 min | 20 found, 0 wrong, 5.2 min | Topic |
| 40 | Which of these contracts contain a confidentiality provision? | 64 | 62 found, 2 wrong, 31 s | 62 found, 0 wrong, 9.1 min | 63 found, 1 wrong, 3.0 min | 62 found, 0 wrong, 9.1 min | Topic |
| 41 | Which of these contracts consider the agreement or terms in the agreement to be confidential? | 33 | 32 found, 1 wrong, 21 s | 31 found, 0 wrong, 7.5 min | 31 found, 2 wrong, 3.0 min | 28 found, 0 wrong, 9.6 min | Topic |
| 42 | Which of these contracts contain indemnification provisions? | 70 | 69 found, 0 wrong, 34 s | 69 found, 0 wrong, 10.2 min | 69 found, 1 wrong, 3.0 min | 67 found, 1 wrong, 5.2 min | Topic |
| 43 | Which of these contracts expressly cap the liabilities of one or both parties? | 54 | 27 found, 1 wrong, 20 s | 23 found, 0 wrong, 9.4 min | 38 found, 1 wrong, 4.0 min | 20 found, 0 wrong, 9.0 min | Topic, 1 read failed |
| 44 | Which contracts are governed by Texas law and include a confidentiality provision? | 4 | 4 found, 0 wrong, 27 s | 4 found, 0 wrong, 2.9 min | 4 found, 0 wrong, 30 s | 4 found, 0 wrong, 3.3 min | Reuse |
| 45 | Which of these contracts auto-renew and include a warranty? | 26 | 14 found, 0 wrong, 35 s | 7 found, 0 wrong, 9.8 min | 10 found, 0 wrong, 3.5 min | 12 found, 0 wrong, 4.8 min | Topic, paused about 30 min by the page limit |
| 46 | Which of these contracts contain a no-solicit of employees and consider the agreement confidential? | 4 | 4 found, 0 wrong, 19 s | 3 found, 0 wrong, 7.9 min | 3 found, 1 wrong, 30 s | 3 found, 0 wrong, 4.6 min | Reuse |
