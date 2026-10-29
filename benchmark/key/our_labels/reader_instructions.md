# Reading contracts for six labels

Each file in `in/` is one contract's full text. For each contract you are given, decide each of the six items below from the
contract text ALONE, using the meaning written here (not any other definition you know).

For every item answer "yes" or "no". For a "yes", copy the contract's own words that settle it into `quote` — at least a full
clause, character for character as the text has them (spacing aside), never paraphrased — and give the section number or
heading in `section`. For a "no", leave `quote` and `section` empty. Always give a one-sentence `reason`.
Read the whole contract, schedules and exhibits included, before answering "no".

## arbitration
**Does the contract require all or most disputes between the parties to be settled by binding arbitration?**

The contract requires all or most disputes between the parties to be settled by binding arbitration, not in court. It still counts if it carves out injunctions, IP claims or small claims. It does not count if arbitration happens only by later agreement, covers only a narrow issue (a price or accounting dispute, an expert's decision), or the clause requires only mediation or negotiation.

## confidentiality
**Does the contract contain a confidentiality provision?**

A party must keep the other's confidential or proprietary information secret or not misuse it, whether mutual or one-way, in the body or a schedule. A clause that keeps only the contract's own terms secret counts too. A clause only about personal data does not count.

## agreement_confidential
**Does the contract treat the agreement itself, or its terms, as confidential?**

The contract says the agreement itself, or its terms (for example its prices), are confidential or are confidential information. Protecting only the information the parties exchange does not count, and neither does a rule only about press releases or publicity.

## indemnification
**Does the contract contain an indemnification provision?**

A party must indemnify, defend or hold harmless the other, or its affiliates, officers or customers, against claims, losses or liabilities of any kind stemming from a particular act. A promise only to pay damages for its own breach, or a duty only to carry insurance, does not count. The indemnification may cover all causes or only specific causes.

## warranties
**Does the contract contain a warranty?**

A party warrants or represents something about its products, services, work, authority or compliance, whether or not a duration is stated. An "as is" disclaimer with no warranty given does not count.

## auto_renewal
**Does the contract renew automatically at the end of a term unless a party stops it?**

The contract renews at the end of a term unless a party stops it. A renewal only by agreement or by a party's option does not count.

## Answer
One JSON object: {"contracts": [{"contract": "NNN", "items": [{"id", "answer", "quote", "section", "reason"}, ... all six]}]}.
The item ids, in order: arbitration, confidentiality, agreement_confidential, indemnification, warranties, auto_renewal.
