// Checks the reading engine: node tools/test_spread.js
const R = require(__dirname + "/../src/spread.js");
const D = require(__dirname + "/../src/spread.json");
const M = require(__dirname + "/../src/meanings.json");
const T = require(__dirname + "/../src/tarot.json");
const assert = require("assert");
const cards = T.map(c => Object.assign({}, c, M[c.id]));
const byId = Object.fromEntries(cards.map(c => [c.id, c]));
assert.strictEqual(cards.length, 78);
for (const c of cards) {
  assert.ok(M[c.id], "missing meaning for " + c.id);
  assert.strictEqual(c.keywords.length, 3, c.id);
  assert.ok(c.meaning.length > 40 && c.counsel.length > 8, c.id);
  assert.ok(["light", "mixed", "shadow"].includes(c.tone), c.id);
}
const P = D.positions;
const read = ids => R.summarize(ids.map(i => byId[i]), P, D);
const all = r => r.paras.join("\n");

// positions: star, lute, quill, mirror, galleon, heart
let r = read(["major-17", "lutes-03", "quills-04", "mirrors-02", "galleons-08", "major-03"]);
assert.ok(all(r).includes("At the heart of this reading sits The Empress"));
assert.ok(all(r).includes("what guides you is The Star (hope)"));
assert.ok(all(r).includes("Every suit found its own point"));
assert.ok(all(r).includes("mark a bigger current"));                 // 2 majors
console.log(all(r), "\n---"); console.log(r.notes.join("\n"), "\n===");

r = read(["galleons-05", "quills-03", "quills-09", "quills-10", "major-15", "lutes-10"]);
assert.ok(all(r).includes("Three Quills appear"));
assert.ok(all(r).includes("long shadow"));
assert.ok(all(r).includes("No Mirrors appeared"));
console.log(all(r), "\n===");

r = read(["lutes-12", "mirrors-11", "galleons-13", "quills-14", "lutes-02", "mirrors-02"]);
assert.ok(all(r).includes("No Major Arcana"));
assert.ok(all(r).includes("rats of the Guild"));
assert.ok(all(r).includes("Two Twos"));
console.log(all(r));

// random readings never throw and always produce 4 paragraphs or fewer, at least 3
for (let n = 0; n < 2000; n++) {
  const ids = cards.map(c => c.id).sort(() => Math.random() - .5).slice(0, 6);
  const x = read(ids);
  assert.ok(x.paras.length >= 3 && x.paras.length <= 4 && !all(x).includes("undefined"));
}
console.log("\nall spread tests passed");
