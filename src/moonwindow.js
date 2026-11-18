/* Whether the Priestess is receiving: only on the day of the full moon, by the visitor's own calendar
   (the local date that holds the exact moment of the full moon). Needs Sky (src/sky.js).
   Used by the secret reading (/tarot/priestess/) and by the tarot page, which shows a small moon only then. */
const CGGMoon = {
  dayKey(d) { return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate(); },
  window(Sky, now) {
    const t = +now;
    const fulls = Sky.phasesBetween(new Date(t - 3 * 86400000), new Date(t + 40 * 86400000)).filter(p => p.phase === "full");
    const today = CGGMoon.dayKey(new Date(t));
    const cur = fulls.find(p => CGGMoon.dayKey(p.date) === today);
    const startOf = d => new Date(d.getFullYear(), d.getMonth(), d.getDate());
    if (cur) { const s = startOf(cur.date); return { open: true, full: cur.date, opens: s, closes: new Date(s.getFullYear(), s.getMonth(), s.getDate() + 1) }; }
    const next = fulls.find(p => +startOf(p.date) > t);
    return { open: false, full: next.date, opens: startOf(next.date) };
  }
};
if (typeof module !== "undefined") module.exports = CGGMoon;
