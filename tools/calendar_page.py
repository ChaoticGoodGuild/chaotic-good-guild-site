"""Builds the Guild Calendar (/calendar/): moon phases, the wheel of the year, Guy Fox Day,
and the sun, moon and Mercury through the zodiac.

Words live in src/calendar.json (drafts for Ryan to rewrite). Sky math lives in src/sky.js and runs in the
visitor's browser, so the calendar works for any year. Behavior is in src/calendar.js.
"""
import json, os
import build as B


def build(p):
    e = B.e
    C = json.load(open(os.path.join(B.SRC, "calendar.json")))
    path = "/calendar/"
    desc = ("The Guild Calendar: the phases of the moon, the old wheel of the year from Imbolc to Yule, Guy Fox Day, "
            "and the sun, moon and Mercury through the zodiac, worked out for your own time zone.")
    ld = B.jsonld({"@context": "https://schema.org", "@type": "WebPage", "name": p["title"], "description": desc,
                   "url": B.DOMAIN + path, "isPartOf": {"@type": "WebSite", "name": B.NAME, "url": B.DOMAIN + "/"}})
    data = json.dumps({k: v for k, v in C.items() if not k.startswith("_")})
    days = "".join(f"<span>{d}</span>" for d in ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"))
    # a plain list of the holidays for readers without JavaScript (and for search engines)
    plain = "".join(f"<li><b>{e(h['name'])}</b> ({e(h['also'])}): {e(h['line'])}</li>" for h in C["holidays"])
    page = B.head(f"{p['title']} · {B.NAME}", desc, path, p["slug"], ld)
    page += f"""<header class="top">
  <a class="brand" href="/" aria-label="{B.NAME} home"><img src="/assets/logo.png" alt="{B.NAME}" width="345" height="360"></a>
  <a class="back-link" href="/">&larr; The village</a>
</header>

<main class="sp cal">
  <section class="sp-intro">
    <p class="who">{e(p['who'])}</p>
    <h1>{e(p['title'])}</h1>
    <p class="desc">{e(p['desc'])}</p>
  </section>

  <section class="cal-tonight" id="calTonight" aria-live="polite"></section>

  <section class="cal-month" id="calMonth" aria-label="Calendar">
    <div class="cal-bar">
      <button type="button" class="cal-nav" id="calPrev" aria-label="Previous month">&lsaquo;</button>
      <h2 class="cal-title" id="calTitle"></h2>
      <button type="button" class="cal-nav" id="calNext" aria-label="Next month">&rsaquo;</button>
      <button type="button" class="sp-ghost cal-todaybtn" id="calToday">Today</button>
    </div>
    <div class="cal-body">
      <div class="cal-gridwrap">
        <div class="cal-dow" aria-hidden="true">{days}</div>
        <div class="cal-grid" id="calGrid"></div>
        <p class="cal-key"><span class="k-hol">Wheel of the year</span><span class="k-moon">Full and new moons</span>
          <span class="k-sun">&#9737;&#xFE0E; The sun changes sign</span><span class="k-retro">Mercury retrograde</span></p>
      </div>
      <aside class="cal-day" id="calDay" aria-live="polite"></aside>
    </div>
  </section>

  <section class="cal-wheelsec">
    <h2 class="sp-h">The wheel of the year</h2>
    <div class="cal-wheelwrap">
      <svg class="cal-wheel" id="calWheel" viewBox="0 0 400 400" role="group" aria-label="The wheel of the year, ringed by the twelve signs. The gold sun marks today."></svg>
      <div>
        <p class="cal-wheelnote">Tap a festival to find it on the calendar, or a sign to learn its ways. The gold sun marks where the year stands today.</p>
        <ul class="cal-wheellist" id="calWheelList"></ul>
      </div>
    </div>
    <noscript><ul class="cal-plain">{plain}</ul><p class="raising">The calendar needs JavaScript turned on to read the sky.</p></noscript>
    <p class="cal-fine">{e(C['hemisphere'])}</p>
  </section>

  <div class="sp-light" id="calSign" role="dialog" aria-modal="true" aria-labelledby="calSignTitle" hidden>
    <div class="cal-signbox">
      <div id="calSignBody"></div>
      <button type="button" class="sp-ghost" id="calSignClose">Close</button>
    </div>
  </div>

  <h2 class="places-h">Other paths</h2>
  {B.directory(exclude=p['slug'])}
</main>

{B.foot()}<script type="application/json" id="calendar-data">{data}</script>
<script src="/assets/sky.js"></script>
<script src="/assets/calendar.js"></script>
</body>
</html>
"""
    B.write("calendar/index.html", page)
    B.write("assets/sky.js", open(os.path.join(B.SRC, "sky.js")).read())
    B.write("assets/calendar.js", open(os.path.join(B.SRC, "calendar.js")).read())
