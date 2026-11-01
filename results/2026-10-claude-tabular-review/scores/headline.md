# Tabular review beside plain Claude, re-scored from the recorded answers

Made by `python3 results/2026-10-claude-tabular-review/scoring/reproduce.py --write`.

| | Plain Claude | Tabular review |
|---|---|---|
| **Score out of 100** | **85.6** | **83.9** |
| Contracts found, the 30 list questions (576 in the key) | 463 (80%) | 452 (78%) |
| Contracts named that are not in the key | 12 | 23 |
| Found, with the contracts each hedged as "possible" credited too | 495 (61 not in the key) | 482 (23 not in the key) |
| Counts right (of 5) | 4 | 4 |
| Lookups right (of 11) | 11 | 11 |
| Questions answered in under a minute | 11 | 24 |
| Median time per question | 5.6 min | 42 s |

Redrawing the 46 questions 10,000 times: plain Claude minus Tabular review is -1.5 to +6.3 in 95% of redraws, and plain Claude is ahead in 80.1% of them.

| # | Question | Key | Plain Claude | Tabular review | How Tabular answered | Tabular, about |
|---|---|---|---|---|---|---|
| 1 | Which of these contracts contain a revenue or profit sharing provision? | 33 | 27 found, 1 wrong | 24 found, 2 wrong | Topic | 3.5 min |
| 2 | Which of these contracts contain a right of first refusal, offer or negotiation? | 13 | 10 found, 0 wrong | 9 found, 0 wrong | Topic | 2.7 min |
| 3 | Which of these contracts contain an irrevocable or perpetual license? | 17 | 16 found, 1 wrong | 16 found, 1 wrong | Topic | 3.1 min |
| 4 | Which of these contracts contain a joint IP ownership provision? | 11 | 7 found, 0 wrong | 8 found, 0 wrong | Topic | 2.6 min |
| 5 | Which of these contracts contain a no-solicit of employees provision? | 13 | 12 found, 0 wrong | 12 found, 0 wrong | Topic | 2.1 min |
| 6 | Which of these contracts contain an unlimited-usage license? | 5 | 3 found, 0 wrong | 3 found, 1 wrong | Topic | 2.2 min |
| 7 | How many of these contracts are governed by the laws of Texas? Give the number and list them. | 7 | said 7 | said 7 | Topic | 2.7 min |
| 8 | How many of these contracts are governed by the laws of Illinois? Give the number and list them. | 3 | said 3 | said 3 | Topic, column rewritten | 2.7 min |
| 9 | How many of these contracts are governed by the laws of England? Give the number and list them. | 4 | said 4 | said 4 | Reuse | 18 s |
| 10 | How many of these contracts are governed by the laws of Canada? Give the number and list them. | 4 | said 4 | said 4 | Reuse | 18 s |
| 11 | How many of these contracts give a party a right of first refusal, offer or negotiation? | 13 | said 11 | said 9 | Reuse | 18 s |
| 12 | What law governs the Yield Maintenance Agreement between Wells Fargo Bank on behalf of Wells Fargo Mortgage Backed Securities 2006-6 Trust and UBS AG? |  | right | right | Reuse | 18 s |
| 13 | What law governs the Cooperation Agreement between Otkritie Investments Cyprus Limited and QIWI plc? |  | right | right | Reuse | 18 s |
| 14 | When was the Limited Power Of Attorney between FEDERATED INVESTMENT MANAGEMENT COMPANY and FEDERATED ADVISORY SERVICES COMPANY entered into? |  | right | right | Re-ask | 36 s |
| 15 | When does the initial term of the Supply Agreement between HOVIONE INTER AG and INTERSECT ENT, Inc end? |  | right | right | Re-ask | 36 s |
| 16 | When does the initial term of the Manufacturing Outsourcing Agreement between Nice Systems Ltd and Flextronics Israel Ltd end? |  | right | right | Re-ask | 42 s |
| 17 | Who is the other party to the Master Operation And Maintenance Agreement with BLOOM ENERGY CORPORATION? |  | right | right | Re-ask | 42 s |
| 18 | Who is the other party to the Co-Branding Agreement with Lucent Technologies Inc? |  | right | right | Re-ask | 42 s |
| 19 | What is the renewal term of the Software License And Maintenance Agreement between GARMAN ROUTING SYSTEMS, INC and SPARKLING SPRING WATER GROUP LIMITED? |  | right | right | Re-ask | 42 s |
| 20 | How much notice is needed to stop the Co-Branding Agreement between VerticalNet, Inc and PaperExchange.com, LLC from renewing? |  | right | right | Opened contract | 18 s |
| 21 | Which contract requires the shortest notice to stop it from renewing? | 3 | 2 found, 0 wrong | 2 found, 0 wrong | Topic | 3.0 min |
| 22 | Which of these contracts was entered into most recently? | 1 | 1 found, 1 wrong | 1 found, 0 wrong | Topic, follow-up | 3.5 min |
| 23 | Which of these contracts were entered into between January 1, 2008 and December 31, 2012? | 9 | 7 found, 0 wrong | 7 found, 0 wrong | Reuse, follow-up | 1.0 min |
| 24 | Which of these contracts were entered into before January 1, 2001? | 14 | 14 found, 0 wrong | 14 found, 0 wrong | Reuse | 30 s |
| 25 | As of July 1, 2020, which of these contracts had an initial term due to end within the next 12 months? | 5 | 4 found, 0 wrong | 4 found, 0 wrong | Topic, 4 reads failed | 5.0 min |
| 26 | Which of these contracts run until a party ends them, with no fixed end date? | 14 | 8 found, 0 wrong | 7 found, 0 wrong | Re-ask | 1.0 min |
| 27 | As of July 1, 2016, which of these contracts had a deadline within the next six months for giving notice to stop an automatic renewal? | 3 | 3 found, 0 wrong | 3 found, 0 wrong | Reuse | 30 s |
| 28 | Which of these contracts are still in force today? | 28 | 23 found, 0 wrong | 0 found, 0 wrong | Topic, re-ask, follow-up | 5.2 min |
| 29 | Which contracts entered into after December 31, 2010 restrict a party from soliciting the other party's employees? | 9 | 8 found, 0 wrong | 9 found, 0 wrong | Reuse | 30 s |
| 30 | Which contracts restrict soliciting the other party's employees or give a right of first refusal, offer or negotiation? | 25 | 20 found, 0 wrong | 20 found, 0 wrong | Reuse | 30 s |
| 31 | Which contracts is Beijing Yisheng Leju Information Services Co., Ltd a party to? | 2 | 2 found, 0 wrong | 2 found, 0 wrong | Topic, follow-up | 4.0 min |
| 32 | Which of these contracts are hosting agreements? | 4 | 4 found, 0 wrong | 3 found, 0 wrong | Reuse, file names | 30 s |
| 33 | Which contracts require at least 60 days' notice to stop them from renewing? | 9 | 5 found, 0 wrong | 5 found, 0 wrong | Reuse | 30 s |
| 34 | When does the initial term of the Intellectual Property Agreement between Marv Enterprises, LLC and Premier Biomedical, Inc end? |  | right | right | Reuse | 30 s |
| 35 | What law governs the Master Services Agreement between Clear Capital and Radial Spark, LLC? |  | right | right | Reuse | 18 s |
| 36 | Which of these contracts contain a non-compete or exclusivity clause? | 39 | 38 found, 9 wrong | 37 found, 13 wrong | Topic | 3.0 min |
| 37 | Which contracts contain governing law provisions outside of the US? | 15 | 15 found, 0 wrong | 15 found, 0 wrong | Reuse | 18 s |
| 38 | Which of these contracts contain an auto-renewal provision? | 28 | 15 found, 0 wrong | 13 found, 0 wrong | Reuse | 30 s |
| 39 | Which of these contracts require most disputes be settled by arbitration? | 21 | 20 found, 0 wrong | 20 found, 0 wrong | Topic | 3.0 min |
| 40 | Which of these contracts contain a confidentiality provision? | 64 | 62 found, 0 wrong | 63 found, 1 wrong | Topic | 3.0 min |
| 41 | Which of these contracts consider the agreement or terms in the agreement to be confidential? | 33 | 31 found, 0 wrong | 31 found, 2 wrong | Topic | 3.0 min |
| 42 | Which of these contracts contain indemnification provisions? | 70 | 69 found, 0 wrong | 69 found, 1 wrong | Topic | 3.0 min |
| 43 | Which of these contracts expressly cap the liabilities of one or both parties? | 54 | 23 found, 0 wrong | 38 found, 1 wrong | Topic, 1 read failed | 4.0 min |
| 44 | Which contracts are governed by Texas law and include a confidentiality provision? | 4 | 4 found, 0 wrong | 4 found, 0 wrong | Reuse | 30 s |
| 45 | Which of these contracts auto-renew and include a warranty? | 26 | 7 found, 0 wrong | 10 found, 0 wrong | Topic, paused about 30 min by the page limit | 3.5 min |
| 46 | Which of these contracts contain a no-solicit of employees and consider the agreement confidential? | 4 | 3 found, 0 wrong | 3 found, 1 wrong | Reuse | 30 s |
