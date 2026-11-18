// Tests for the secret full-moon reading: when it opens, and Mira's reflection for every kind of draw.
const assert = require("assert");
const Sky = require("../src/sky.js");
const CGGMoon = require("../src/moonwindow.js");
const P = require("../src/priestess.js");
const D = Object.assign(require("../src/priestess.json"), { suits: require("../src/spread.json").suits });
const M = require("../src/meanings.json"), T = require("../src/tarot.json");
const H = D.window_hours;

// The full moon of 24 November 2026 is at 14:53 UTC.
let w = CGGMoon.window(Sky, new Date("2026-11-18T12:00:00Z"), H);
assert.ok(!w.open); assert.strictEqual(w.full.toISOString().slice(0, 13), "2026-11-24T14");
assert.strictEqual(w.opens.toISOString().slice(0, 13), "2026-11-23T02");
assert.ok(CGGMoon.window(Sky, new Date("2026-11-24T14:53:00Z"), H).open);
assert.ok(CGGMoon.window(Sky, new Date("2026-11-23T03:00:00Z"), H).open);
assert.ok(CGGMoon.window(Sky, new Date("2026-11-26T02:00:00Z"), H).open);
assert.ok(!CGGMoon.window(Sky, new Date("2026-11-26T04:00:00Z"), H).open);
// open on roughly three nights a month, every month for two years
let open = 0;
for (let t = Date.parse("2027-01-01"); t < Date.parse("2029-01-01"); t += 3600000) if (CGGMoon.window(Sky, new Date(t), H).open) open++;
const perMonth = open / 24 / 24;
assert.ok(perMonth > 2.9 && perMonth < 3.1, perMonth);

// the reading engine
assert.strictEqual(D.positions.length, 9);
assert.strictEqual(D.positions[8].key, "secret"); assert.ok(D.positions[8].upright && D.positions[1].upright);
const deck = T.map(c => ({ id: c.id, name: c.name, suit: c.suit, rank: c.rank, ...M[c.id] }));
let seed = 3; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
for (let i = 0; i < 3000; i++) {
  const pool = deck.slice(); const picks = [];
  for (let k = 0; k < 9; k++) picks.push({ ...pool.splice(Math.floor(rnd() * pool.length), 1)[0], reversed: !D.positions[k].upright && rnd() < .5 });
  const shown = P.isMajor(picks[8]);
  const r = P.summarize(picks, D.positions, D, shown);
  const text = r.paras.join(" ");
  assert.ok(r.paras.length >= 7 && !/undefined|NaN|\[object/.test(text), text);
  assert.ok(text.includes(picks[0].name) && text.includes(picks[7].name));
  if (shown) assert.ok(text.includes("showed you her secret") && text.includes(picks[8].name));
  else assert.ok(text.includes("kept her secret") && !text.includes(picks[8].name + ","), "a kept secret must stay hidden");
  assert.ok(!/rebellion/i.test(text));
}
console.log("all priestess tests passed");
