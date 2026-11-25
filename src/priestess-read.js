/* The Priestess by Moonlight: the secret full-moon reading (The High Priestess Spread).
   Nine cards laid like the High Priestess card. Card 9, the scroll, is the Priestess's secret: it is turned on its own,
   after a pause, and shown only when it is a Major Arcana card. Everything happens in the visitor's browser. */

// ---------- The reading engine (pure functions)
// picks[k] is the card in positions[k]; cards carry id, name, suit, rank, keywords, meaning, question, tone, reversed.
// shown: whether the Priestess revealed her secret (card 9 was a Major Arcana card).
const CGGPriestess = {
  list(xs) { return xs.length < 2 ? xs.join("") : xs.slice(0, -1).join(", ") + " and " + xs[xs.length - 1]; },
  // a sentence ends at . ! or ? followed by a capital letter (so "Chaos! celebrates..." stays whole)
  firstSentence(t) { const m = String(t).match(/^.*?[.!?](?=\s+["“A-Z]|\s*$)/); return (m ? m[0] : t).trim(); },
  count(n) { return ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"][n] || String(n); },
  isMajor(c) { return c.suit === "major"; },
  summarize(picks, positions, D, shown) {
    const L = CGGPriestess.list, at = key => picks[positions.findIndex(p => p.key === key)];
    const name = c => c.name + (c.reversed ? " (reversed)" : "");
    const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
    const kw0 = c => c.keywords[0];
    const self = at("self"), cross = at("crossing"), wax = at("waxing"), full = at("full"), wane = at("waning");
    const dark = at("dark"), lite = at("light"), sum = at("sum"), secret = at("secret");
    const paras = [], notes = [];

    // 1. The heart of it
    let p1 = `At the Priestess's heart sits ${name(self)}: ${L(self.keywords)}. This is where you are right now. `
      + `Across it lies ${cross.name}: ${L(cross.keywords)}. That's what surrounds you.`;
    if (self.suit === cross.suit && self.suit !== "major") p1 += ` Both are ${D.suits[self.suit].name}, so you and your surroundings are speaking the same language.`;
    paras.push(p1);
    notes.push(positions[0].how, positions[1].how);

    // 2. The three moons, in the order they were dealt
    const pk = c => `${c.name} (${kw0(c)}${c.reversed ? ", reversed" : ""})`;
    let p2 = `Above her, the three moons: the lenses you see it all through. The waning moon holds ${pk(wane)}, `
      + `the way you've seen what came before. The full moon holds ${pk(full)}, the lens you're looking through now. `
      + `The waxing moon holds ${pk(wax)}, the next step the path suggests.`;
    p2 += full.reversed
      ? ` The full moon came reversed, so ask whether this lens is magnifying things right now, or hiding them.`
      : ` The moon only reflects, so ask whether ${full.name} is showing things as they are, or larger than life.`;
    paras.push(p2);
    notes.push(positions[2].how, positions[3].how, positions[4].how);

    // 3. The pillars
    let p3 = `On either side stand her pillars. The dark pillar holds ${pk(dark)}: what moves you without your noticing. `
      + `The light pillar holds ${pk(lite)}: what you know drives you.`;
    if (dark.suit === lite.suit && dark.suit !== "major") p3 += ` Both pillars are ${D.suits[dark.suit].name}: what you know and what you don't are pulling the same way.`;
    else if ((dark.tone === "shadow") !== (lite.tone === "shadow") && (dark.tone === "shadow" || lite.tone === "shadow"))
      p3 += ` One pillar is heavy and one is not: the part of you that you can see and the part you can't may be pulling in different directions.`;
    paras.push(p3);
    notes.push(positions[5].how, positions[6].how);

    // 4. Patterns across the eight cards on the table (and the secret, if shown)
    const table = picks.filter((c, k) => positions[k].key !== "secret").concat(shown ? [secret] : []);
    const pat = [];
    const majors = table.filter(CGGPriestess.isMajor);
    if (majors.length === 0) pat.push("No Major Arcana sits on the table, so this reading lives in everyday choices you can shape.");
    else if (majors.length >= 3) pat.push(`With ${CGGPriestess.count(majors.length)} Major Arcana in the reading, this is a season of big lessons, larger than any one choice.`);
    else pat.push(`${L(majors.map(c => c.name))} ${majors.length === 1 ? "marks" : "mark"} a bigger current running beneath the everyday.`);
    const counts = {};
    table.filter(c => !CGGPriestess.isMajor(c)).forEach(c => { counts[c.suit] = (counts[c.suit] || 0) + 1; });
    const ranked = Object.entries(counts).sort((a, b) => b[1] - a[1]);
    if (ranked.length && ranked[0][1] >= 3 && (ranked.length === 1 || ranked[0][1] > ranked[1][1])) {
      const s = D.suits[ranked[0][0]];
      pat.push(`${cap(CGGPriestess.count(ranked[0][1]))} ${s.name} appear, so ${s.theme} color the whole reading.`);
      notes.push(`When a suit repeats, its element colors the reading. ${s.name} are ${s.element}: ${s.theme}.`);
    }
    const rev = table.filter(c => c.reversed && c !== self);
    if (rev.length >= 4) pat.push("Many cards came reversed, so this reading is about balance: where something has grown too loud, and where something is missing.");
    else if (rev.length) pat.push(`${L(rev.map(c => c.name))} came reversed. For ${rev.length === 1 ? "it" : "each"}, ask: is there too much of that energy right now, or not enough?`);
    if (table.some(c => c.reversed)) notes.push(D.reversed + " Only you can tell which.");
    paras.push(pat.join(" "));

    // 5. The crescent: how it fits together
    paras.push(`At her feet, the crescent holds ${name(sum)}: ${L(sum.keywords)}. This is how the pieces fit together. ${CGGPriestess.firstSentence(sum.meaning)}`);
    notes.push(positions[7].how);

    // 6. The secret
    paras.push(shown
      ? `And the scroll. The Priestess showed you her secret, ${name(secret)}: ${L(secret.keywords)}. This is the deeper lesson in why you're here. ${CGGPriestess.firstSentence(secret.meaning)}`
      : `The scroll stayed sealed. The Priestess kept her secret tonight: the lesson beneath all this is still writing itself.`);
    notes.push(positions[8].how);

    // 7. Questions to carry, then the mirror
    const ask = c => c.question + (c.reversed ? ` And since it came reversed: is there too much of it right now, or not enough?` : "");
    let q = `Questions to carry, from the Self: ${ask(self)} And from the crescent: ${ask(sum)}`;
    if (shown) q += ` And from the scroll: ${secret.question}`;
    paras.push(q);
    notes.push("Mira closes with questions, not answers. The answers are yours.");
    paras.push(D.reflection);
    return { paras, notes };
  }
};
// The app's full-moon pull: three cards, the two pillars and the Priestess's secret between them.
// picks = [dark, light, secret]; shown: the secret was a Major Arcana card (and so is always upright).
CGGPriestess.moonDay = function (picks, P, D, shown) {
  const L = CGGPriestess.list, [dark, lite, secret] = picks;
  const pk = c => `${c.name} (${c.keywords[0]}${c.reversed ? ", reversed" : ""})`;
  const paras = [];
  let p1 = `The moon is full, and Mira lays three cards the way the Priestess sits. The dark pillar holds ${pk(dark)}: ${P.dark.question.toLowerCase()} `
    + `The light pillar holds ${pk(lite)}: ${P.light.question.toLowerCase()}`;
  if (dark.suit === lite.suit && dark.suit !== "major") p1 += ` Both pillars are ${D.suits[dark.suit].name}: what you know and what you don't are pulling the same way.`;
  else if ((dark.tone === "shadow") !== (lite.tone === "shadow")) p1 += ` One pillar is heavy and one is not: the part of you that you can see and the part you can't may be pulling in different directions.`;
  paras.push(p1);
  const rev = [dark, lite].filter(c => c.reversed);
  if (rev.length) paras.push(`${L(rev.map(c => c.name))} came reversed. For ${rev.length === 1 ? "it" : "each"}, ask: is there too much of that energy right now, or not enough?`);
  paras.push(shown
    ? `Between the pillars, the Priestess showed you her secret: ${secret.name}, ${L(secret.keywords)}. This is the deeper lesson beneath it all. ${CGGPriestess.firstSentence(secret.meaning)}`
    : `Between the pillars, the scroll stayed sealed. The Priestess kept her secret tonight: the lesson beneath all this is still writing itself.`);
  let q = `Questions to carry: ${dark.question} ${lite.question}`;
  if (shown) q += ` ${secret.question}`;
  paras.push(q, D.reflection);
  return paras;
};
if (typeof module !== "undefined") module.exports = CGGPriestess;
