import assert from "assert";
import { clean } from "../netlify/functions/stats.mjs";
const good = { version: "1.0-draft", age: "25-34", result: "chaotic-good", x: 0.5, y: 0.75, answers: Array(16).fill([1, -1]).flat() };
assert.strictEqual(clean({ ...good, answers: Array(32).fill(1) }), null);   // straight-lining
const r = clean(good);
assert.strictEqual(r["form-name"], "alignment-stats"); assert.strictEqual(r.answers.split(",").length, 32);
assert.ok(/^\d{4}-\d{2}$/.test(r.month)); assert.ok(!("ip" in r) && !("email" in r));
assert.strictEqual(clean({ ...good, result: "evil-overlord" }), null);
assert.strictEqual(clean({ ...good, answers: [9, 9, 9, 9, 9, 9, 9, 9] }), null);
assert.strictEqual(clean({ ...good, x: 4 }), null);
assert.strictEqual(clean({ ...good, answers: [1, -1, ...Array(30).fill("")] }).answers.split(",").length, 32);
assert.strictEqual(clean({ ...good, age: "under-18" }), null);
assert.strictEqual(clean({ ...good, age: "rather-not-say" }), null);
assert.strictEqual(clean({ ...good, age: undefined }), null);
console.log("all stats tests passed");
