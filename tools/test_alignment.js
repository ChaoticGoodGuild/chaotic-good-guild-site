const S = require(__dirname + "/../src/alignment.js");
const data = require(__dirname + "/../src/alignment.json");
const assert = require("assert");
const N = data.items.length;
const it = data.items;
// item bank balance
const count = (ax, k) => it.filter(i => i.axis === ax && i.key === k).length;
assert.deepStrictEqual([count("order",1),count("order",-1),count("heart",1),count("heart",-1)],[8,8,8,8]);
assert.strictEqual(new Set(it.map(i=>i.id)).size, N);
// answer pattern helper: agree fully with items keyed toward target
const pattern = (ordWant, heartWant) => it.map(i => {
  const want = i.axis === "order" ? ordWant : heartWant;
  return want === 0 ? 0 : 2 * i.key * want;
});
const cases = [
  [-1, 1, "lawful-good"], [0, 1, "neutral-good"], [1, 1, "chaotic-good"],
  [-1, 0, "lawful-neutral"], [0, 0, "true-neutral"], [1, 0, "chaotic-neutral"],
  [-1, -1, "lawful-evil"], [0, -1, "neutral-evil"], [1, -1, "chaotic-evil"],
];
for (const [o, h, want] of cases) {
  const r = S.score(data, pattern(o, h));
  assert.strictEqual(r.slug, want, `${o},${h} -> ${r.slug}`);
  assert.ok(Math.abs(r.x - o) < 1e-9 && Math.abs(r.y - h) < 1e-9);
}
// acquiescence check: agreeing with everything lands neutral on both axes
const allAgree = S.score(data, new Array(N).fill(2));
assert.strictEqual(allAgree.slug, "true-neutral"); assert.strictEqual(allAgree.x, 0); assert.strictEqual(allAgree.y, 0);
// unanswered counts as neutral
assert.strictEqual(S.score(data, new Array(N).fill(null)).slug, "true-neutral");
// band edges
assert.strictEqual(S.label(0.25, 0.25, 0.25), "chaotic-good");
assert.strictEqual(S.label(0.249, -0.249, 0.25), "true-neutral");
assert.strictEqual(S.label(-0.3, 0.1, 0.25), "lawful-neutral");
// every result has a description
for (const [, , slug] of cases) assert.ok(data.results[slug] && data.results[slug].desc.length > 50);
console.log("lean:", S.lean(0.4, "Lawful", "Chaotic", .25), "|", S.lean(-0.1, "Evil", "Good", .25));
console.log("all scoring tests passed");
