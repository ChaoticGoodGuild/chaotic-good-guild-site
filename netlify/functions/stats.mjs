// Anonymous alignment-test answers. The browser sends them here; this function checks them and passes them
// on to the site's own "alignment-stats" Netlify form. Because the function makes that request, Netlify
// records the function's address with each entry, not the visitor's. Nothing else about the visitor is kept.
const ADULT = ["18-24", "25-34", "35-44", "45-54", "55-plus"];
const SLUGS = ["lawful-good", "neutral-good", "chaotic-good", "lawful-neutral", "true-neutral", "chaotic-neutral",
               "lawful-evil", "neutral-evil", "chaotic-evil"];

export function clean(b) {
  if (!b || typeof b !== "object") return null;
  if (!Array.isArray(b.answers) || b.answers.length < 8 || b.answers.length > 80) return null;
  const answers = b.answers.map(a => (a === "" || a === null ? "" : Number(a)));
  if (answers.some(a => a !== "" && !(Number.isInteger(a) && a >= -2 && a <= 2))) return null;
  if (!SLUGS.includes(b.result)) return null;
  if (!ADULT.includes(b.age)) return null;                                  // never anything from under-18s
  if (new Set(answers.filter(a => a !== "")).size < 2) return null;         // same answer to everything
  const x = Number(b.x), y = Number(b.y);
  if (!(Math.abs(x) <= 1 && Math.abs(y) <= 1)) return null;
  return {
    "form-name": "alignment-stats",
    version: String(b.version || "").slice(0, 20),
    age: b.age,
    month: new Date().toISOString().slice(0, 7),
    result: b.result, x: x.toFixed(3), y: y.toFixed(3),
    answers: answers.join(","),
  };
}

export default async (req) => {
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405 });
  let body;
  try { body = await req.json(); } catch (e) { return new Response("Bad request", { status: 400 }); }
  const row = clean(body);
  if (!row) return new Response("Bad request", { status: 400 });
  const origin = new URL(req.url).origin;
  const r = await fetch(origin + "/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" },
                                        body: new URLSearchParams(row).toString() });
  return new Response(r.ok ? "ok" : "relay failed", { status: r.ok ? 200 : 502 });
};
