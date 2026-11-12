// Checks the Guild's sky math against published values. Run: node tools/test_sky.js
const assert = require("assert");
const Sky = require(__dirname + "/../src/sky.js");
const U = s => new Date(s + "Z");
const mins = (a, b) => Math.abs(a - b) / 60000;
const near = (got, want, tol, label) => {
  const m = mins(got, U(want));
  console.log(`${label.padEnd(34)} ${got.toISOString().slice(0, 16)}  vs ${want}  (${m.toFixed(1)} min)`);
  assert.ok(m <= tol, label + " off by " + m.toFixed(1) + " minutes");
};

// Meeus example 47.a: 1992 April 12, 0h TD, apparent longitude 133.162655
const jd = 2448724.5 - 69 / 86400 + (59 - 69) / 86400;   // close enough: TD ~ UT + 59s in 1992
assert.ok(Math.abs(Sky.moonLon(jd) - 133.1627) < 0.02, "moon longitude " + Sky.moonLon(jd));
// Meeus example 25.a: 1992 Oct 13, 0h TD, apparent sun 199.90895
assert.ok(Math.abs(Sky.sunLon(2448908.5) - 199.909) < 0.01, "sun longitude " + Sky.sunLon(2448908.5));

// US Naval Observatory, 2026 moon phases (UTC)
const ph = Sky.phasesBetween(U("2026-01-01T00:00"), U("2027-01-01T00:00"));
const pick = (phase, day) => ph.find(p => p.phase === phase && p.date.toISOString().startsWith(day)).date;
near(pick("full", "2026-01-03"), "2026-01-03T10:03", 3, "full moon, Jan 3");
near(pick("last", "2026-01-10"), "2026-01-10T15:48", 3, "last quarter, Jan 10");
near(pick("new", "2026-01-18"), "2026-01-18T19:52", 3, "new moon, Jan 18");
near(pick("first", "2026-01-26"), "2026-01-26T04:47", 3, "first quarter, Jan 26");
near(pick("full", "2026-02-01"), "2026-02-01T22:09", 3, "full moon, Feb 1");
near(pick("new", "2026-02-17"), "2026-02-17T12:01", 3, "new moon, Feb 17");
near(pick("full", "2026-03-03"), "2026-03-03T11:38", 3, "full moon, Mar 3");
near(pick("full", "2026-12-24"), "2026-12-24T01:28", 3, "full moon, Dec 24");
assert.strictEqual(ph.filter(p => p.phase === "full").length, 13, "2026 has 13 full moons");

// 2026 eclipses: annular solar Feb 17, total lunar Mar 3, total solar Aug 12, partial lunar Aug 28
const ec = ph.filter(p => p.eclipse).map(p => p.date.toISOString().slice(0, 10) + " " + p.eclipse.kind + " " + p.eclipse.body);
console.log("eclipses:", ec.join("; "));
assert.deepStrictEqual(ec, ["2026-02-17 annular solar", "2026-03-03 total lunar", "2026-08-12 total solar", "2026-08-28 partial lunar"]);

// 2026 equinoxes and solstices (UTC)
const s = Sky.seasons(2026);
near(s.march, "2026-03-20T14:46", 20, "March equinox");
near(s.june, "2026-06-21T08:24", 20, "June solstice");
near(s.september, "2026-09-23T00:05", 20, "September equinox");
near(s.december, "2026-12-21T20:50", 20, "December solstice");

// Mercury's 2026 stations (UTC, from published ephemerides)
const st = Sky.mercuryStations(2026).filter(x => x.date.getUTCFullYear() === 2026);
const want = [["retrograde", "2026-02-26T06:48"], ["direct", "2026-03-20T19:33"], ["retrograde", "2026-06-29T17:35"],
              ["direct", "2026-07-23T22:57"], ["retrograde", "2026-10-24T07:12"], ["direct", "2026-11-13T15:53"]];
assert.strictEqual(st.length, 6, "six stations in 2026");
st.forEach((x, i) => { assert.strictEqual(x.kind, want[i][0]); near(x.date, want[i][1], 12 * 60, "Mercury stations " + x.kind + " (sign " + Sky.signOf(x.lon) + ")"); });
assert.deepStrictEqual(st.map(x => Sky.signOf(x.lon)), [11, 11, 3, 3, 7, 7], "Pisces, Cancer, Scorpio");

// the sun enters Scorpio around Oct 23, 2026; the moon changes sign every 2-3 days
const sc = Sky.signChange(Sky.sunLon, U("2026-10-22T00:00"), U("2026-10-24T00:00"));
console.log("sun enters sign", sc.to, "at", sc.date.toISOString());
assert.strictEqual(sc.to, 7);
let changes = 0;
for (let d = 0; d < 30; d++) if (Sky.signChange(Sky.moonLon, new Date(Date.UTC(2026, 10, 1 + d)), new Date(Date.UTC(2026, 10, 2 + d)))) changes++;
assert.ok(changes >= 11 && changes <= 14, "moon sign changes in 30 days: " + changes);
console.log("all sky tests passed");
