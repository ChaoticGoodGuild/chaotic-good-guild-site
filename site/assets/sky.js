/* The Guild's sky: moon phases, the sun and moon through the zodiac, Mercury's retrogrades, eclipses
   and the turning points of the year. Everything is worked out in the visitor's browser from standard
   astronomical formulas (Jean Meeus, "Astronomical Algorithms", 2nd ed.; JPL's approximate planetary
   elements), so the calendar works for any year with no data files and nothing sent anywhere.
   Accuracy: moon phases and season turns to within a few minutes, sign changes to within an hour or so,
   Mercury's stations to within several hours. Plenty for a calendar that shows days. */
const Sky = (function () {
  const RAD = Math.PI / 180;
  const sin = d => Math.sin(d * RAD), cos = d => Math.cos(d * RAD);
  const norm = d => ((d % 360) + 360) % 360;
  const DT = 69 / 86400;                         // TT - UT, close enough for 2000-2040

  const jdOf = date => date.getTime() / 86400000 + 2440587.5;
  const dateOf = jd => new Date((jd - 2440587.5) * 86400000);
  const cent = jd => (jd + DT - 2451545) / 36525;  // Julian centuries of TT from J2000

  // ---------- the sun (Meeus ch. 25), apparent ecliptic longitude of date, degrees
  function sunLon(jd) {
    const T = cent(jd);
    const L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T;
    const M = 357.52911 + 35999.05029 * T - 0.0001537 * T * T;
    const C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * sin(M) + (0.019993 - 0.000101 * T) * sin(2 * M) + 0.000289 * sin(3 * M);
    const om = 125.04 - 1934.136 * T;
    return norm(L0 + C - 0.00569 - 0.00478 * sin(om));
  }

  // ---------- the moon (Meeus ch. 47, the larger terms), apparent ecliptic longitude of date, degrees
  const MOON_TERMS = [
    [0, 0, 1, 0, 6288774], [2, 0, -1, 0, 1274027], [2, 0, 0, 0, 658314], [0, 0, 2, 0, 213618], [0, 1, 0, 0, -185116],
    [0, 0, 0, 2, -114332], [2, 0, -2, 0, 58793], [2, -1, -1, 0, 57066], [2, 0, 1, 0, 53322], [2, -1, 0, 0, 45758],
    [0, 1, -1, 0, -40923], [1, 0, 0, 0, -34720], [0, 1, 1, 0, -30383], [2, 0, 0, -2, 15327], [0, 0, 1, 2, -12528],
    [0, 0, 1, -2, 10980], [4, 0, -1, 0, 10675], [0, 0, 3, 0, 10034], [4, 0, -2, 0, 8548], [2, 1, -1, 0, -7888],
    [2, 1, 0, 0, -6766], [1, 0, -1, 0, -5163], [1, 1, 0, 0, 4987], [2, -1, 1, 0, 4036], [2, 0, 2, 0, 3994],
    [4, 0, 0, 0, 3861], [2, 0, -3, 0, 3665], [0, 1, -2, 0, -2689], [2, 0, -1, 2, -2602], [2, -1, -2, 0, 2390],
    [1, 0, 1, 0, -2348], [2, -2, 0, 0, 2236], [0, 1, 2, 0, -2120], [0, 2, 0, 0, -2069], [2, -2, -1, 0, 2048],
    [2, 0, 1, -2, -1773], [2, 0, 0, 2, -1595], [4, -1, -1, 0, 1215], [0, 0, 2, 2, -1110], [3, 0, -1, 0, -892],
    [2, 1, 1, 0, -810], [4, -1, -2, 0, 759], [0, 2, -1, 0, -713], [2, 2, -1, 0, -700], [2, 1, -2, 0, 691],
    [2, -1, 0, -2, 596], [4, 0, 1, 0, 549], [0, 0, 4, 0, 537], [4, -1, 0, 0, 520], [1, 0, -2, 0, -487]
  ];
  function moonLon(jd) {
    const T = cent(jd);
    const Lp = 218.3164477 + 481267.88123421 * T - 0.0015786 * T * T + T * T * T / 538841;
    const D = 297.8501921 + 445267.1114034 * T - 0.0018819 * T * T + T * T * T / 545868;
    const M = 357.5291092 + 35999.0502909 * T - 0.0001536 * T * T;
    const Mp = 134.9633964 + 477198.8675055 * T + 0.0087414 * T * T + T * T * T / 69699;
    const F = 93.2720950 + 483202.0175233 * T - 0.0036539 * T * T;
    const E = 1 - 0.002516 * T - 0.0000074 * T * T;
    let s = 0;
    for (const [d, m, mp, f, c] of MOON_TERMS) {
      const e = m === 0 ? 1 : Math.abs(m) === 1 ? E : E * E;
      s += c * e * sin(d * D + m * M + mp * Mp + f * F);
    }
    s += 3958 * sin(119.75 + 131.849 * T) + 1962 * sin(Lp - F) + 318 * sin(53.09 + 479264.290 * T);
    const om = 125.04 - 1934.136 * T;
    return norm(Lp + s / 1e6 - 0.00478 * sin(om));
  }

  // how much of the moon is lit (0-1) and whether it is growing
  function moonLight(jd) {
    const el = norm(moonLon(jd) - sunLon(jd));
    return { fraction: (1 - cos(el)) / 2, waxing: el < 180, age: el / 360 };
  }

  // ---------- the four principal phases (Meeus ch. 49): exact moments
  function phaseJD(k) {                         // k integer = new, +.25 first quarter, +.5 full, +.75 last quarter
    const T = k / 1236.85;
    let jde = 2451550.09766 + 29.530588861 * k + 0.00015437 * T * T - 0.00000015 * T * T * T + 0.00000000073 * T ** 4;
    const E = 1 - 0.002516 * T - 0.0000074 * T * T;
    const M = 2.5534 + 29.1053567 * k - 0.0000014 * T * T - 0.00000011 * T * T * T;
    const Mp = 201.5643 + 385.81693528 * k + 0.0107582 * T * T + 0.00001238 * T ** 3 - 0.000000058 * T ** 4;
    const F = 160.7108 + 390.67050284 * k - 0.0016118 * T * T - 0.00000227 * T ** 3 + 0.000000011 * T ** 4;
    const Om = 124.7746 - 1.56375588 * k + 0.0020672 * T * T + 0.00000215 * T ** 3;
    const q = Math.round((k - Math.floor(k)) * 4) % 4;
    let c;
    if (q === 0 || q === 2) {
      const a = q === 0 ? [-0.40720, 0.17241, 0.01608, 0.01039, 0.00739, -0.00514, 0.00208]
                        : [-0.40614, 0.17302, 0.01614, 0.01043, 0.00734, -0.00515, 0.00209];
      c = a[0] * sin(Mp) + a[1] * E * sin(M) + a[2] * sin(2 * Mp) + a[3] * sin(2 * F) + a[4] * E * sin(Mp - M)
        + a[5] * E * sin(Mp + M) + a[6] * E * E * sin(2 * M) - 0.00111 * sin(Mp - 2 * F) - 0.00057 * sin(Mp + 2 * F)
        + 0.00056 * E * sin(2 * Mp + M) - 0.00042 * sin(3 * Mp) + 0.00042 * E * sin(M + 2 * F) + 0.00038 * E * sin(M - 2 * F)
        - 0.00024 * E * sin(2 * Mp - M) - 0.00017 * sin(Om) - 0.00007 * sin(Mp + 2 * M) + 0.00004 * sin(2 * Mp - 2 * F)
        + 0.00004 * sin(3 * M) + 0.00003 * sin(Mp + M - 2 * F) + 0.00003 * sin(2 * Mp + 2 * F) - 0.00003 * sin(Mp + M + 2 * F)
        + 0.00003 * sin(Mp - M + 2 * F) - 0.00002 * sin(Mp - M - 2 * F) - 0.00002 * sin(3 * Mp + M) + 0.00002 * sin(4 * Mp);
    } else {
      c = -0.62801 * sin(Mp) + 0.17172 * E * sin(M) - 0.01183 * E * sin(Mp + M) + 0.00862 * sin(2 * Mp) + 0.00804 * sin(2 * F)
        + 0.00454 * E * sin(Mp - M) + 0.00204 * E * E * sin(2 * M) - 0.00180 * sin(Mp - 2 * F) - 0.00070 * sin(Mp + 2 * F)
        - 0.00040 * sin(3 * Mp) - 0.00034 * E * sin(2 * Mp - M) + 0.00032 * E * sin(M + 2 * F) + 0.00032 * E * sin(M - 2 * F)
        - 0.00028 * E * E * sin(Mp + 2 * M) + 0.00027 * E * sin(2 * Mp + M) - 0.00017 * sin(Om) - 0.00005 * sin(Mp - M - 2 * F)
        + 0.00004 * sin(2 * Mp + 2 * F) - 0.00004 * sin(Mp + M + 2 * F) + 0.00004 * sin(Mp - 2 * M) + 0.00003 * sin(Mp + M - 2 * F)
        + 0.00003 * sin(3 * M) + 0.00002 * sin(2 * Mp - 2 * F) + 0.00002 * sin(Mp - M + 2 * F) - 0.00002 * sin(3 * Mp + M);
      const W = 0.00306 - 0.00038 * E * cos(M) + 0.00026 * cos(Mp) - 0.00002 * cos(Mp - M) + 0.00002 * cos(Mp + M) + 0.00002 * cos(2 * F);
      c += q === 1 ? W : -W;
    }
    const A = [[299.77, 0.107408, 325], [251.88, 0.016321, 165], [251.83, 26.651886, 164], [349.42, 36.412478, 126],
               [84.66, 18.206239, 110], [141.74, 53.303771, 62], [207.14, 2.453732, 60], [154.84, 7.306860, 56],
               [34.52, 27.261239, 47], [207.19, 0.121824, 42], [291.34, 1.844379, 40], [161.72, 24.198154, 37],
               [239.56, 25.513099, 35], [331.55, 3.592518, 23]];
    let extra = 0;
    A.forEach(([a, b, co], i) => { extra += co * 1e-6 * sin(a + b * k - (i === 0 ? 0.009173 * T * T : 0)); });
    jde += c + extra;
    return { jd: jde - DT, E, M, Mp, F, Om };
  }

  // eclipses at a new or full moon (Meeus ch. 54)
  function eclipseAt(k) {
    const { E, M, Mp, F, Om } = phaseJD(k);
    if (Math.abs(sin(F)) > 0.36) return null;
    const F1 = F - 0.02665 * sin(Om);
    const P = 0.2070 * E * sin(M) + 0.0024 * E * sin(2 * M) - 0.0392 * sin(Mp) + 0.0116 * sin(2 * Mp)
            - 0.0073 * E * sin(Mp + M) + 0.0067 * E * sin(Mp - M) + 0.0118 * sin(2 * F1);
    const Q = 5.2207 - 0.0048 * E * cos(M) + 0.0020 * E * cos(2 * M) - 0.3299 * cos(Mp) - 0.0060 * E * cos(Mp + M) + 0.0041 * E * cos(Mp - M);
    const W = Math.abs(cos(F1));
    const g = (P * cos(F1) + Q * sin(F1)) * (1 - 0.0048 * W);
    const u = 0.0059 + 0.0046 * E * cos(M) - 0.0182 * cos(Mp) + 0.0004 * cos(2 * Mp) - 0.0005 * cos(M + Mp);
    const ag = Math.abs(g);
    if (Number.isInteger(k)) {                   // solar
      if (ag > 1.5433 + u) return null;
      if (ag < 0.9972) return { body: "solar", kind: u < 0 ? "total" : u > 0.0047 ? "annular" : "hybrid" };
      return { body: "solar", kind: "partial" };
    }
    const umbral = (1.0128 - u - ag) / 0.5450, pen = (1.5573 + u - ag) / 0.5450;
    if (umbral >= 1) return { body: "lunar", kind: "total" };
    if (umbral > 0) return { body: "lunar", kind: "partial" };
    if (pen > 0) return { body: "lunar", kind: "penumbral" };
    return null;
  }

  // every principal phase whose moment falls between two dates
  function phasesBetween(from, to) {
    const out = [];
    const y = from.getUTCFullYear() + (from.getUTCMonth() + 0.5) / 12;
    let k = Math.floor((y - 2000) * 12.3685) - 2;
    for (;; k += 0.25) {
      const p = phaseJD(k), d = dateOf(p.jd);
      if (d > to) break;
      if (d >= from) {
        const q = Math.round((k - Math.floor(k)) * 4) % 4;
        const ev = { phase: ["new", "first", "full", "last"][q], date: d };
        if (q === 0 || q === 2) { const ec = eclipseAt(k); if (ec) ev.eclipse = ec; }
        out.push(ev);
      }
    }
    return out;
  }

  // ---------- Mercury, seen from Earth (JPL approximate elements, J2000 ecliptic, good 1800-2050)
  const EL = {
    mercury: [0.38709927, 0.00000037, 0.20563593, 0.00001906, 7.00497902, -0.00594749, 252.25032350, 149472.67411175, 77.45779628, 0.16047689, 48.33076593, -0.12534081],
    earth:   [1.00000261, 0.00000562, 0.01671123, -0.00004392, -0.00001531, -0.01294668, 100.46457166, 35999.37244981, 102.93768193, 0.32327364, 0, 0]
  };
  function helio(p, T) {
    const e0 = EL[p];
    const a = e0[0] + e0[1] * T, e = e0[2] + e0[3] * T, I = e0[4] + e0[5] * T;
    const L = e0[6] + e0[7] * T, w = e0[8] + e0[9] * T, O = e0[10] + e0[11] * T;
    const om = w - O, M = norm(L - w) * RAD;
    let E = M + e * Math.sin(M);
    for (let i = 0; i < 8; i++) E -= (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
    const xp = a * (Math.cos(E) - e), yp = a * Math.sqrt(1 - e * e) * Math.sin(E);
    return [(cos(om) * cos(O) - sin(om) * sin(O) * cos(I)) * xp + (-sin(om) * cos(O) - cos(om) * sin(O) * cos(I)) * yp,
            (cos(om) * sin(O) + sin(om) * cos(O) * cos(I)) * xp + (-sin(om) * sin(O) + cos(om) * cos(O) * cos(I)) * yp];
  }
  function mercuryLon(jd) {
    const T = cent(jd), m = helio("mercury", T), g = helio("earth", T);
    return norm(Math.atan2(m[1] - g[1], m[0] - g[0]) / RAD + 1.3969713 * T);   // + precession to the ecliptic of date
  }
  const dlon = (a, b) => ((b - a + 540) % 360) - 180;

  // Mercury's stations in a year: [{kind: "retrograde"|"direct", date, lon}]
  const stationCache = {};
  function mercuryStations(year) {
    if (stationCache[year]) return stationCache[year];
    const start = jdOf(new Date(Date.UTC(year - 1, 11, 1))), end = jdOf(new Date(Date.UTC(year + 1, 1, 1)));
    const speed = jd => dlon(mercuryLon(jd - 0.25), mercuryLon(jd + 0.25));
    const out = [];
    let prev = speed(start);
    for (let jd = start + 1; jd <= end; jd += 1) {
      const s = speed(jd);
      if ((prev > 0) !== (s > 0)) {
        let lo = jd - 1, hi = jd;
        for (let i = 0; i < 30; i++) { const mid = (lo + hi) / 2; ((speed(mid) > 0) === (prev > 0)) ? lo = mid : hi = mid; }
        const t = (lo + hi) / 2;
        out.push({ kind: prev > 0 ? "retrograde" : "direct", date: dateOf(t), lon: mercuryLon(t) });
      }
      prev = s;
    }
    return (stationCache[year] = out);
  }

  // ---------- signs
  const signOf = lon => Math.floor(norm(lon) / 30);   // 0 Aries ... 11 Pisces

  // when does a body's sign change between two moments? (body changes sign at most once in the window)
  function signChange(fn, a, b) {
    const sa = signOf(fn(jdOf(a))), sb = signOf(fn(jdOf(b)));
    if (sa === sb) return null;
    let lo = jdOf(a), hi = jdOf(b);
    for (let i = 0; i < 40; i++) { const mid = (lo + hi) / 2; signOf(fn(mid)) === sa ? lo = mid : hi = mid; }
    return { from: sa, to: sb, date: dateOf((lo + hi) / 2) };
  }

  // the moment the sun reaches a longitude (0 = March equinox, 90 June solstice, 180, 270), near a guess
  function sunAt(target, guess) {
    let jd = jdOf(guess);
    for (let i = 0; i < 8; i++) jd += dlon(sunLon(jd), target) / 0.98564736;
    return dateOf(jd);
  }
  function seasons(year) {
    return {
      march: sunAt(0, new Date(Date.UTC(year, 2, 20))), june: sunAt(90, new Date(Date.UTC(year, 5, 21))),
      september: sunAt(180, new Date(Date.UTC(year, 8, 22))), december: sunAt(270, new Date(Date.UTC(year, 11, 21)))
    };
  }

  return { jdOf, dateOf, sunLon, moonLon, moonLight, mercuryLon, phasesBetween, mercuryStations, signOf, signChange, seasons };
})();
if (typeof module !== "undefined") module.exports = Sky;
