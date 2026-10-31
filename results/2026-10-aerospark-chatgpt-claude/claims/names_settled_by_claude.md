# Names settled by Claude

ChatGPT's and Claude's answers were read by a model reader (Claude Haiku), which copied each name an answer gives; code placed each name on the contract list. Code could not place these on one contract (a tie, or a name with no word in the contract list, such as "FIS" for Fidelity National Information Services), so Claude settled each from the answer's own words. Names under "no" are left unplaced: a "no" changes no score.

| System | # | Question | List | Name as read | Contract | Why |
|---|---|---|---|---|---|---|
| ChatGPT | 41 | set-agreement-confidential | yes | Reynolds Consumer Products — Supply Agreement | 77 ReynoldsConsumerProductsInc_20191115_S-1_EX-1 | the Reynolds Supply Agreement is file 77 |
| ChatGPT | 42 | set-indemnification | yes | Reynolds Consumer Products — Service | 78 ReynoldsConsumerProductsInc_20200121_S-1A_EX- | the Reynolds Service Agreement (a transition services agreement) is file 78 |
| ChatGPT | 42 | set-indemnification | yes | Reynolds Consumer Products — Supply | 77 ReynoldsConsumerProductsInc_20191115_S-1_EX-1 | the Reynolds Supply Agreement is file 77 |
| ChatGPT | 42 | set-indemnification | yes | Soupman — Franchise Agreement 2 | 83 SoupmanInc_20150814_8-K_EX-10.1_9230148_EX-10 | Soupman Franchise Agreement 2 is file 83 |
| Claude | 1 | set-revenue-profit-sharing | possible | Global Technologies | 36 GLOBALTECHNOLOGIESLTD_06_08_2020-EX-10.16-CON | the only contract of Global Technologies Ltd (the tie was Clickstream) |
| Claude | 8 | count-illinois | yes | Reynolds Consumer Products — Master Supply Agreement | 77 ReynoldsConsumerProductsInc_20191115_S-1_EX-1 | the Reynolds Supply Agreement is file 77 |
| Claude | 8 | count-illinois | yes | Reynolds Consumer Products — Transition Services Agreement | 78 ReynoldsConsumerProductsInc_20200121_S-1A_EX- | the Reynolds Service Agreement (a transition services agreement) is file 78 |
| Claude | 25 | date-ending-asof-2020 | possible | Reynolds transition services agreement | 78 ReynoldsConsumerProductsInc_20200121_S-1A_EX- | the Reynolds Service Agreement (a transition services agreement) is file 78 |
| Claude | 26 | date-no-end | possible | FIS IP Agreement | 30 FIDELITYNATIONALINFORMATIONSERVICES_INC_08_05 | FIS = Fidelity National Information Services; its IP agreement (Equifax/Certegy) is file 30, the only FIS file |
| Claude | 28 | date-in-force-today | yes | FIS (Equifax–Certegy) IP agreement | 30 FIDELITYNATIONALINFORMATIONSERVICES_INC_08_05 | FIS = Fidelity National Information Services; its IP agreement (Equifax/Certegy) is file 30, the only FIS file |
| Claude | 28 | date-in-force-today | possible | Aimmune–Xencor | 3 AimmuneTherapeuticsInc_20200205_8-K_EX-10.3_1 | the Aimmune development agreement with Xencor is file 3 |
| Claude | 30 | or-nosolicit-rofr | possible | Leju | 51 LEJUHOLDINGSLTD_03_12_2014-EX-10.34-INTERNET_ | "Leju" = the Leju Holdings agreement, file 51 (the only file named Leju) |
| Claude | 31 | party | yes | Domain Name and Content License Agreement | 17 ChinaRealEstateInformationCorp_20090929_F-1_E | the answer gives its file, ChinaRealEstateInformationCorp ... Content License Agreement = file 17 |
| Claude | 36 | set-noncompete-or-exclusivity | yes | FIS IP Agreement | 30 FIDELITYNATIONALINFORMATIONSERVICES_INC_08_05 | FIS = Fidelity National Information Services; its IP agreement (Equifax/Certegy) is file 30, the only FIS file |
| Claude | 40 | set-confidentiality | yes | Reynolds Consumer Products – Service Agreement | 78 ReynoldsConsumerProductsInc_20200121_S-1A_EX- | the Reynolds Service Agreement (a transition services agreement) is file 78 |
| Claude | 41 | set-agreement-confidential | possible | Soupman | 83 SoupmanInc_20150814_8-K_EX-10.1_9230148_EX-10, 84 SoupmanInc_20150814_8-K_EX-10.1_9230148_EX-10 | the answer says "both Soupman files" (Franchise Agreements 2 and 4, files 83 and 84), under "Can't be confirmed from the file" |
| Claude | 42 | set-indemnification | yes | FIS IP Agreement | 30 FIDELITYNATIONALINFORMATIONSERVICES_INC_08_05 | FIS = Fidelity National Information Services; its IP agreement (Equifax/Certegy) is file 30, the only FIS file |
| Claude | 42 | set-indemnification | yes | Soupman Franchise part 2 | 83 SoupmanInc_20150814_8-K_EX-10.1_9230148_EX-10 | Soupman Franchise Agreement 2 is file 83 |
| Claude | 43 | set-cap-on-liability | yes | Reynolds – Transition Services Agmt | 78 ReynoldsConsumerProductsInc_20200121_S-1A_EX- | the Reynolds Service Agreement (a transition services agreement) is file 78 |

## One question read by hand

ChatGPT, question 28 (date-in-force-today). The reader took the names in the first answer's first two sections as affirmed. That answer calls them "strongest candidates" and contracts that "may remain in force", and ends by calling them "a list of potentially continuing contracts, not 20 legally verified active agreements". It says of none of them that it is in force. All of them count as possible (`read_by_hand` in `chatgpt/claims.json`). The other answers were checked for a hedge over the whole list; this is the only one.

With none named as a match, question 28 was asked again in the same words on 31 October 2026, under the same settings, taking 530 seconds, added to its time. The second answer also hedges all of them ("none can be certified as legally active today", "not a verified register"), so it scores the same. It is the answer recorded; the first is kept beside it in `answers/chatgpt/answers.txt` (`firstAnswer`).
