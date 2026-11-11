// Claim extraction: turns each written answer of a run file into what it CLAIMS about the numbered contracts —
// yes (affirmed to have the property) / possible / no, and the count for a how-many question. Haiku 4.5, temperature 0. Scoring claims,
// not citations: an answer that says "[7] has no such clause" still cites [7].
// Contracts are numbered [1]..[N] in the run's CORPUS order; each finding is shown with the numbers of the contracts it cites.
//
//   node scripts/benchmark/extract_claims.js <run file> <claims file> [--runs 2]
//
// --runs 2 extracts twice (the rule for the real test: extract twice, review the disagreements); the claims file keeps the first
// extraction and lists every question where the two differ. The API key comes from app/.env (never printed).
const fs = require('fs');
const path = require('path');
const APP = path.resolve(__dirname, '..', '..', 'app');
require(path.join(APP, 'node_modules', 'dotenv')).config({ path: path.join(APP, '.env'), override: true });
const Anthropic = require(path.join(APP, 'node_modules', '@anthropic-ai', 'sdk'));
const { estimateCostUsd } = require(path.join(APP, 'src', 'db', 'pricing'));

if (!process.argv.includes('--api-ok')) {
  console.error('extract_claims.js calls the Anthropic API (Claude Haiku) and costs money. Add --api-ok to confirm.');
  process.exit(2);
}
const [IN, OUT] = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const runsArg = process.argv.indexOf('--runs');
const RUNS = runsArg > -1 ? Math.max(1, Number(process.argv[runsArg + 1]) || 1) : 1;
if (!IN || !OUT) { console.error('usage: node extract_claims.js <run file> <claims file> [--runs 2]'); process.exit(2); }
const MODEL = 'claude-haiku-4-5';
// A contract the answer LISTS as having the property, with a doubt, a limit or a narrow scope noted, is a "yes" (2026-10-12): the same
// answer, listing the same 20 verified contracts with similar notes ("thin", "narrow", "limited to"), was read once as 20 yes and once as
// 13 yes / 6 possible / 7 no (runs/2026-10-12, insurance + audit). Tightened the same day: the first wording also counted as "yes" a
// contract the answer doubted matched at all ("the matched clause is insurance only" on an insurance + audit question). Both readers.
const HEDGE_RULE = ' A contract the answer LISTS as matching the question counts as "yes" even when it adds a caveat about the scope or strength of a clause that does match (for example "narrow", "thin", "limited to", "one-sided", "with carve-outs"). If the answer doubts whether the contract matches at all - it says a required clause was not found, is only possible or is about something else, or it calls the match possible, likely, unconfirmed or not established - that is "possible". "no" is only for a contract it says does not match.';
const SYSTEM = 'You read an answer about a set of numbered contracts and extract exactly what it claims. Numbers like [12] are contract numbers. Return ONLY JSON: {"yes":[numbers the answer affirms HAVE the property asked about],"possible":[numbers it says only possibly or unconfirmed have it],"no":[numbers it explicitly says do NOT have it],"count":<the number it gives if the question asks how many, else null>}. Do not infer beyond what the answer says; a number merely mentioned as context or as lacking the property is not "yes".' + HEDGE_RULE;
// An AeroSpark answer's own text numbers contracts in the list the answer model was given (on a large register, only the contracts
// it read), not in the register's order: "[13] is excluded" in a summary is the answer's 13th, not the register's. Those numbers are
// masked as [#] before the text is shown, and only the numbers after "cites" (resolved by the service to real contracts) and in a
// count's groups are register numbers. 2026-10-11: reading them as register numbers put NEON (named, 1996) among the "no"s of a
// date question and added 4 unlabelled "possible"s across two questions. The note is added ONLY to an answer whose text had such
// numbers: Haiku's reading of a hedged answer moved with the wording of the instructions (Dev "cap": 27 vs 47 affirmed), so answers
// without them keep exactly the instructions they were scored with.
const LOCAL_NOTE = ' In the answer text, [#] marks a contract the answer referred to by a number of its own; it cannot be placed, so never list it. The only contract numbers are those after "cites" and in the count groups.';
// The answer model's own numbers, masked (see SYSTEM): "[13]", and the same numbers in plain prose, "contract 15's", "contracts 5, 6
// and 10", "4 contracts (5, 6, 10, 11)" (2026-10-11: read as register numbers, they were dropped and the 4 verified contracts of an
// exclusivity + non-compete answer scored as none). The code also keeps only numbers the answer cites or groups (validNums).
const maskLocal = (s) => String(s == null ? '' : s)
  .replace(/\[\d+\]/g, '[#]')
  .replace(/\b(contracts?)\s+\d{1,3}(?:\s*(?:,|and|&|or)\s*\d{1,3})*\b/gi, '$1 [#]')
  .replace(/\(\s*\d{1,3}(?:\s*(?:,|and|&)\s*\d{1,3})+\s*\)/g, '([#])');
// The first complete {...} in a reply (a model sometimes adds an explanation after the JSON, with braces of its own).
function firstObject(text) {
  const start = text.indexOf('{');
  if (start < 0) return '';
  let depth = 0, inStr = false, esc = false;
  for (let i = start; i < text.length; i++) {
    const ch = text[i];
    if (inStr) { if (esc) esc = false; else if (ch === '\\') esc = true; else if (ch === '"') inStr = false; continue; }
    if (ch === '"') inStr = true;
    else if (ch === '{') depth++;
    else if (ch === '}' && --depth === 0) return text.slice(start, i + 1);
  }
  return text.slice(start);
}

// A ChatGPT run file (chatgpt_run_file.py) has free text that names contracts by company or title, not by number. The model only copies
// out the NAMES the answer gives, as written; CODE maps each name to the roster (file name + parties). Asked to map names to roster numbers
// itself, Haiku put 3 of 19 contracts on the wrong number in the 2026-10-09 first look, the same way both times, so a second extraction
// did not catch it. A name the code cannot place on exactly one contract is listed for a person to settle.
const SYSTEM_ROSTER = 'You read an answer about a folder of contracts and extract exactly what it claims. The answer names contracts by company, party or title. Copy each name as the answer writes it (company and title, e.g. "Dynamex — Transportation Services"). Return ONLY JSON: {"yes":[names of contracts the answer affirms HAVE the property asked about],"possible":[names it says only possibly, likely, unconfirmed, pending review or "needs review" have it],"no":[names it explicitly says do NOT have it],"count":<the number it gives if the question asks how many, else null>}. Do not infer beyond what the answer says; a contract merely mentioned as context or as lacking the property is not "yes".' + HEDGE_RULE;
const NOT_DISTINCT = new Set(['inc', 'corp', 'corporation', 'company', 'ltd', 'limited', 'llc', 'plc', 'group', 'holdings', 'the', 'and', 'agreement', 'contract', 'services', 'service',
  'international', 'technologies', 'technology', 'systems', 'license', 'licence', 'supply', 'development', 'distribution', 'distributor', 'strategic', 'alliance', 'with', 'for', 'of']);
const squashText = (s) => String(s || '').normalize('NFKD').replace(/[^\x00-\x7f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '');
const wordsOf = (s) => [...new Set(String(s || '').normalize('NFKD').replace(/[^\x00-\x7f]/g, '').toLowerCase().split(/[^a-z0-9]+/).filter((w) => w.length >= 3 && !NOT_DISTINCT.has(w)))];
function placeName(name, roster) {
  // Each roster entry's text (file name + parties, letters and digits only); a name's distinctive words found in it (CUAD file names run words
  // together, e.g. DYNAMEXINC). The entry matching the most of the name's words, then the most letters, wins; a tie or no match is not placed.
  const ws = wordsOf(name);
  const scored = roster.map((text, i) => { const hit = ws.filter((w) => text.includes(w)); return { n: i + 1, k: hit.length, len: hit.join('').length }; })
    .filter((s) => s.k > 0).sort((a, b) => b.k - a.k || b.len - a.len);
  if (!scored.length) return { name, n: null, why: 'no roster entry has any of its words' };
  if (scored[1] && scored[1].k === scored[0].k && scored[1].len === scored[0].len) return { name, n: null, why: 'ties: ' + scored.filter((s) => s.k === scored[0].k && s.len === scored[0].len).map((s) => s.n).join(', ') };
  return { name, n: scored[0].n };
}

const lines = fs.readFileSync(IN, 'utf8').split('\n').filter(Boolean);
const corpus = JSON.parse(lines.find((l) => l.startsWith('CORPUS ')).slice(7));
const numOf = Object.fromEntries(corpus.order.map((r, i) => [r, i + 1]));
const ROSTER = ['chatgpt', 'claude', 'notebooklm', 'copilot'].includes(corpus.system)   // prose answers (Claude's, NotebookLM's and Copilot's were read from run files marked 'chatgpt'; same path)
  ? corpus.files.map((f, i) => squashText(f) + ' ' + ((corpus.parties && corpus.parties[i]) || []).map(squashText).join(' '))
  : null;
const answers = lines.filter((l) => l.startsWith('ANS ')).map((l) => JSON.parse(l.slice(4)));
const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
let usd = 0;

async function extract(a) {
  let system = SYSTEM, user, validNums = null;
  if (ROSTER) {
    system = SYSTEM_ROSTER;
    user = `QUESTION: ${a.q}\n\nANSWER:\n${a.summary}`;
  } else {
    const findings = (a.findings || []).map((f) => `- ${maskLocal(f.point)} (cites ${f.req.map((r) => '[' + (numOf[r] || '?') + ']').join(', ')})`).join('\n');
    // A count's groups (the lists the page shows under it; run files from 2026-10-11 on): the contracts the answer counts in each.
    const groups = ((a.tally && a.tally.groups) || []).map((g) => `- ${g.label}: ${g.count} — ${(g.req || []).map((r) => '[' + (numOf[r] || '?') + ']').join(', ')}`).join('\n');
    user = `QUESTION: ${a.q}\n\nANSWER SUMMARY:\n${maskLocal(a.summary)}\n\nANSWER FINDINGS:\n${findings || '(none)'}` + (groups ? `\n\nTHE ANSWER COUNTS THESE CONTRACTS, BY GROUP:\n${groups}` : '');
    validNums = new Set([...(a.findings || []).flatMap((f) => f.req), ...((a.tally && a.tally.groups) || []).flatMap((g) => g.req || [])]
      .map((r) => numOf[r]).filter(Boolean));
    const own = [a.summary, ...(a.findings || []).map((f) => f.point)].join('\n');
    if (maskLocal(own) !== String(own)) system = SYSTEM + LOCAL_NOTE;
  }
  // 4000: an answer naming ~90 contracts overflowed 1200 and came back as a parse error (2026-10-12)
  const r = await client.messages.create({ model: MODEL, max_tokens: 4000, temperature: 0, system, messages: [{ role: 'user', content: user }] });
  const u = r.usage || {};
  usd += estimateCostUsd(MODEL, u.input_tokens, u.output_tokens, { read: u.cache_read_input_tokens, write: u.cache_creation_input_tokens });
  const text = (r.content.find((c) => c.type === 'text') || {}).text || '';
  let j;
  try { j = JSON.parse(firstObject(text)); } catch (e) { return { parse_error: text.slice(0, 200) }; }
  if (!ROSTER) {
    // Only a number the answer cites (or groups) can be a contract it made a claim about; anything else is dropped and recorded.
    const dropped = [];
    for (const k of ['yes', 'possible', 'no']) {
      const xs = Array.isArray(j[k]) ? j[k].map(Number) : [];
      j[k] = xs.filter((n) => validNums.has(n));
      dropped.push(...xs.filter((n) => !validNums.has(n)).map((n) => ({ list: k, n })));
    }
    return dropped.length ? { ...j, dropped } : j;
  }
  // Names -> roster numbers, by code. The names are kept so a person can check the placing.
  const out = { count: j.count ?? null, names: {}, unplaced: [] };
  for (const k of ['yes', 'possible', 'no']) {
    const placed = (Array.isArray(j[k]) ? j[k] : []).map((nm) => placeName(nm, ROSTER));
    out[k] = [...new Set(placed.filter((p) => p.n).map((p) => p.n))];
    out.names[k] = placed.map((p) => ({ name: p.name, n: p.n }));
    out.unplaced.push(...placed.filter((p) => !p.n).map((p) => ({ list: k, name: p.name, why: p.why })));
  }
  return out;
}
const same = (x, y) => ['yes', 'possible', 'no'].every((k) => JSON.stringify([...(x[k] || [])].sort((p, q) => p - q)) === JSON.stringify([...(y[k] || [])].sort((p, q) => p - q))) && (x.count ?? null) === (y.count ?? null);

(async () => {
  const out = [];
  for (let i = 0; i < answers.length; i += 5) {
    const part = await Promise.all(answers.slice(i, i + 5).map(async (a) => {
      const all = [];
      for (let k = 0; k < RUNS; k++) all.push(await extract(a).catch((e) => ({ error: e.message })));
      const rec = { pass: a.pass, id: a.id, claims: all[0] };
      if (RUNS > 1) rec.agree = all.every((c) => same(c, all[0])), rec.others = all.slice(1);
      return rec;
    }));
    out.push(...part);
  }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 0));
  const bad = out.filter((o) => !o.claims || o.claims.parse_error || o.claims.error);
  console.log(`answers ${answers.length} | extracted ${out.length} x ${RUNS} | failures ${bad.length} | cost $${usd.toFixed(3)}`);
  for (const o of out) {
    for (const u of (o.claims && o.claims.unplaced) || []) console.log(`  NOT PLACED (${o.id}, pass ${o.pass}, ${u.list}): "${u.name}" — ${u.why}; settle by hand`);
  }
  if (RUNS > 1) {
    const dis = out.filter((o) => !o.agree);
    console.log(`the extractions disagree on ${dis.length} of ${out.length} answers` + (dis.length ? ': ' + dis.map((o) => `${o.id} (pass ${o.pass})`).join(', ') + ' — review these by hand' : ''));
  }
})().catch((e) => { console.error('ERR', e.message); process.exit(1); });
