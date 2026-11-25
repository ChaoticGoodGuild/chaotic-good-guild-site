// Tests for the secret full-moon reading: when it opens, and Mira's reflection for every kind of draw.
const assert = require("assert");
const Sky = require("../src/sky.js");
const CGGMoon = require("../src/moonwindow.js");
const P = require("../src/priestess-read.js");
const D = Object.assign(require("../src/priestess.json"), { suits: require("../src/spread.json").suits });
const M = require("../src/meanings.json"), T = require("../src/tarot.json");
// Run in Michigan time (tools run this with TZ=America/Detroit). The full moon of 24 November 2026 is 9:53 AM there.
process.env.TZ = process.env.TZ || "America/Detroit";
const local = s => new Date(s);   // a time with no zone is read as local
let w = CGGMoon.window(Sky, local("2026-11-18T12:00:00"));
assert.ok(!w.open); assert.strictEqual(CGGMoon.dayKey(w.full), "2026-11-24");
assert.strictEqual(+w.opens, +local("2026-11-24T00:00:00"));
assert.ok(!CGGMoon.window(Sky, local("2026-11-23T23:59:00")).open);
assert.ok(CGGMoon.window(Sky, local("2026-11-24T00:01:00")).open);
assert.ok(CGGMoon.window(Sky, local("2026-11-24T23:59:00")).open);
assert.ok(!CGGMoon.window(Sky, local("2026-11-25T00:01:00")).open);
// exactly one day for each full moon, for two years
const days = new Set();
for (let t = +local("2027-01-01T00:30:00"); t < +local("2029-01-01T00:00:00"); t += 3600000) {
  const x = CGGMoon.window(Sky, new Date(t)); if (x.open) days.add(CGGMoon.dayKey(new Date(t)));
}
const fulls = Sky.phasesBetween(local("2027-01-01T00:00:00"), local("2029-01-01T00:00:00")).filter(p => p.phase === "full").length;
assert.strictEqual(days.size, fulls);

// the reading engine
assert.strictEqual(D.positions.length, 9);
assert.deepStrictEqual(D.positions.map(p => p.key), ["self", "crossing", "waning", "full", "waxing", "dark", "light", "sum", "secret"]);
assert.ok(D.positions[2].x < 50 && D.positions[4].x > 50);   // waning on the left, waxing on the right
const deck = T.map(c => ({ id: c.id, name: c.name, suit: c.suit, rank: c.rank, ...M[c.id] }));
let seed = 3; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
for (let i = 0; i < 3000; i++) {
  const pool = deck.slice(); const picks = [];
  for (let k = 0; k < 9; k++) { const c = pool.splice(Math.floor(rnd() * pool.length), 1)[0]; picks.push({ ...c, reversed: rnd() < .5 && !(k === 8 && c.suit === "major") }); }
  const shown = P.isMajor(picks[8]);
  const r = P.summarize(picks, D.positions, D, shown);
  const text = r.paras.join(" ");
  assert.ok(r.paras.length >= 7 && !/undefined|NaN|\[object/.test(text), text);
  assert.ok(text.includes(picks[0].name) && text.includes(picks[7].name));
  if (shown) assert.ok(text.includes("showed you her secret") && text.includes(picks[8].name));
  else assert.ok(text.includes("kept her secret") && !text.includes(picks[8].name + ","), "a kept secret must stay hidden");
  assert.ok(!/rebellion/i.test(text));
  assert.ok(text.indexOf("waning moon holds") < text.indexOf("full moon holds") && text.indexOf("full moon holds") < text.indexOf("waxing moon holds"));
}
console.log("all priestess tests passed");

// the app's three-card full-moon pull
{
  const PJ = require("../src/priestess.json");
  const pos = Object.fromEntries(PJ.positions.map(p => [p.key, p]));
  for (let i = 0; i < 2000; i++) {
    const pool = deck.slice(), take = () => pool.splice(Math.floor(rnd() * pool.length), 1)[0];
    const dark = { ...take(), reversed: rnd() < .5 }, lite = { ...take(), reversed: rnd() < .5 }, s = take();
    const shown = s.suit === "major", secret = { ...s, reversed: !shown && rnd() < .5 };
    const paras = P.moonDay([dark, lite, secret], pos, D, shown), text = paras.join(" ");
    assert.ok(!/undefined|NaN|\[object/.test(text), text);
    assert.ok(text.includes(dark.name) && text.includes(lite.name));
    if (shown) assert.ok(text.includes("showed you her secret") && text.includes(s.name));
    else assert.ok(text.includes("scroll stayed sealed") && !text.includes(s.name));
    assert.ok(!/rebellion/i.test(text));
  }
  console.log("all moon-day tests passed");
}
