/* Whether the Priestess is receiving: true within `hours` of the exact full moon. Needs Sky (src/sky.js).
   Used by the secret reading (/tarot/full-moon/) and by the tarot page, which shows a small moon only then. */
const CGGMoon = {
  window(Sky, now, hours) {
    const ms = hours * 3600000, t = +now;
    const fulls = Sky.phasesBetween(new Date(t - 4 * 86400000), new Date(t + 40 * 86400000)).filter(p => p.phase === "full");
    const cur = fulls.find(p => Math.abs(p.date - t) <= ms);
    if (cur) return { open: true, full: cur.date, closes: new Date(+cur.date + ms) };
    const next = fulls.find(p => +p.date > t);
    return { open: false, full: next.date, opens: new Date(+next.date - ms) };
  }
};

if (typeof module !== "undefined") module.exports = CGGMoon;
