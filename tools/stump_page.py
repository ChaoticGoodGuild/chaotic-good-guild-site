"""Builds Reynard's Stump (/stories/): the Guild's videos, sorted into segments, and its essays.

Videos: src/videos.json (TikTok and YouTube ids, titles, dates, segments). Players load only when a visitor
presses play, so nothing from TikTok or YouTube runs on the page until then.
Essays: one Markdown file per essay in src/essays/, with a short header:

    ---
    title: The essay's title
    date: 2026-11-13
    author: Ryan A. Stewart
    summary: One or two sentences for the list and for link previews.
    ---
    The essay, in plain paragraphs. Blank lines between paragraphs.
    ## A heading     **bold**     *italic*     [a link](https://...)     > a quote     - a list item

Each essay gets its own page at /stories/<file-name>/.
"""
import html, json, os, re
import build as B

E = html.escape


def inline(s):
    s = E(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*)\)", lambda m: f'<a href="{E(m.group(2))}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def markdown(text):
    """A small, safe Markdown: paragraphs, headings, quotes, lists, rules, bold, italic, links."""
    out, para, items, quote = [], [], [], []

    def flush():
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para.clear()
        if items: out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>"); items.clear()
        if quote: out.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>"); quote.clear()

    for line in text.splitlines():
        s = line.strip()
        if not s: flush(); continue
        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            flush(); level = min(len(m.group(1)) + 1, 4)
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>"); continue
        if re.match(r"^(-{3,}|\*{3,})$", s): flush(); out.append("<hr>"); continue
        if s.startswith(">"): (para and flush()); quote.append(s.lstrip("> ").strip()); continue
        m = re.match(r"^[-*]\s+(.*)$", s)
        if m: (para and flush()); items.append(m.group(1)); continue
        if items or quote: flush()
        para.append(s)
    flush()
    return "\n".join(out)


def load_essays():
    d = os.path.join(B.SRC, "essays")
    essays = []
    for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if not f.endswith(".md"): continue
        raw = open(os.path.join(d, f), encoding="utf-8").read()
        meta, body = {}, raw
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
        if m:
            body = m.group(2)
            for line in m.group(1).splitlines():
                k, _, v = line.partition(":")
                if k.strip(): meta[k.strip().lower()] = v.strip()
        slug = f[:-3]
        words = len(re.findall(r"\w+", body))
        essays.append({"slug": slug, "title": meta.get("title", slug.replace("-", " ").title()), "date": meta.get("date", ""),
                       "author": meta.get("author", B.NAME), "summary": meta.get("summary", ""), "body": body,
                       "minutes": max(1, round(words / 230))})
    essays.sort(key=lambda x: x["date"], reverse=True)
    return essays


def nice_date(d):
    import datetime
    try: return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")
    except ValueError: return d


def header():
    return f"""<header class="top">
  <a class="brand" href="/" aria-label="{B.NAME} home"><img src="/assets/logo.png" alt="{B.NAME}" width="345" height="360"></a>
  <a class="back-link" href="/">&larr; The village</a>
</header>
"""


def video_card(v, segs):
    tt = f"https://www.tiktok.com/@chaotic_good_guild/video/{v['tiktok']}"
    yt = v.get("youtube")
    thumb = (f'<img src="https://i.ytimg.com/vi/{yt}/hqdefault.jpg" alt="" loading="lazy" decoding="async">' if yt else "")
    line = f'<span class="st-line">{E(v["line"])}</span>' if v.get("line") else ""
    part = f'<span class="st-part">Part {v["part"]} of 9</span>' if v.get("part") else ""
    return (f'<li class="st-item" data-seg="{v["segment"]}" data-date="{v["date"]}"{" data-part=" + chr(34) + str(v["part"]) + chr(34) if v.get("part") else ""}>'
            f'<a class="st-vid{" has-thumb" if yt else ""}" href="{tt}" data-tt="{v["tiktok"]}"{" data-yt=" + chr(34) + yt + chr(34) if yt else ""}>'
            f'<span class="st-thumb" aria-hidden="true">{thumb}<span class="st-play"></span></span>'
            f'<span class="st-meta"><span class="st-seg">{E(segs[v["segment"]]["name"])}</span>{part}'
            f'<span class="st-title">{E(v["title"])}</span>{line}</span></a></li>')


def build(p):
    V = json.load(open(os.path.join(B.SRC, "videos.json"), encoding="utf-8"))
    segs = {s["key"]: s for s in V["segments"]}
    essays = load_essays()
    vids = V["videos"]
    counts = {k: sum(1 for v in vids if v["segment"] == k) for k in segs}
    path = "/stories/"
    desc = ("Reynard's Stump: the Chaotic Good Guild's short videos, sorted into segments, from Defense Against the LEOs "
            "to Ballads & Shanties, plus essays on living Chaotic Good.")
    ld = B.jsonld({"@context": "https://schema.org", "@type": "CollectionPage", "name": p["title"], "description": desc,
                   "url": B.DOMAIN + path, "isPartOf": {"@type": "WebSite", "name": B.NAME, "url": B.DOMAIN + "/"},
                   "hasPart": [{"@type": "Article", "headline": x["title"], "url": f"{B.DOMAIN}{path}{x['slug']}/",
                                "datePublished": x["date"], "author": {"@type": "Person", "name": x["author"]}} for x in essays]})
    chips = ['<button type="button" class="st-chip" data-seg="all" aria-pressed="true">Everything <span>' + str(len(vids)) + "</span></button>"]
    chips += [f'<button type="button" class="st-chip" data-seg="{k}" aria-pressed="false">{E(s["name"])} <span>{counts[k]}</span></button>'
              for k, s in segs.items() if counts[k]]
    seglines = "".join(f'<p class="st-segline" data-seg="{k}" hidden>{E(s["line"])}</p>' for k, s in segs.items())
    cards = "\n".join(video_card(v, segs) for v in vids)
    essay_list = "\n".join(
        f'<li><a class="st-essay" href="{path}{x["slug"]}/"><span class="st-edate">{E(nice_date(x["date"]))} · {x["minutes"]} min read</span>'
        f'<span class="st-etitle">{E(x["title"])}</span><span class="st-esum">{E(x["summary"])}</span></a></li>' for x in essays)
    w, h = p["view"][2], p["view"][3]
    page = B.head(f"{p['title']} · {B.NAME}", desc, path, p["slug"], ld)
    page += header() + f"""
<main class="st">
  <section class="room-hero">
    <figure class="vignette">
      <img src="/assets/village.svg#v-{p['slug']}" alt="{E(p['who'])}" width="{w}" height="{h}">
    </figure>
    <div>
      <p class="who">{E(p['who'])}</p>
      <h1>{E(p['title'])}</h1>
      <p class="desc">{E(p['desc'])}</p>
      <p class="st-jump"><a class="back-btn" href="#watch">Watch the fox</a> <a class="sp-ghost" href="#read">Read the essays</a></p>
    </div>
  </section>

  <section id="watch" class="st-watch" aria-labelledby="stWatchH">
    <h2 class="places-h" id="stWatchH">Watch</h2>
    <div class="st-chips" role="group" aria-label="Segments">{''.join(chips)}</div>
    {seglines}
    <ul class="st-grid" id="stGrid">
{cards}
    </ul>
    <p class="st-more"><button type="button" class="sp-ghost" id="stMore" hidden>Show more</button></p>
    <p class="st-follow">Follow along on <a href="{V['channels']['tiktok']}" rel="me noopener">TikTok</a> and <a href="{V['channels']['youtube']}" rel="me noopener">YouTube</a>.</p>
  </section>

  <section id="read" class="st-read" aria-labelledby="stReadH">
    <h2 class="places-h" id="stReadH">Read</h2>
    <ul class="st-essays">
{essay_list}
    </ul>
  </section>

  <div class="sp-light" id="stPlayer" role="dialog" aria-modal="true" aria-labelledby="stPTitle" hidden>
    <div class="st-pbox">
      <div class="st-frame" id="stFrame"></div>
      <div class="st-ptext">
        <p class="st-seg" id="stPSeg"></p>
        <h3 id="stPTitle"></h3>
        <p class="st-plinks" id="stPLinks"></p>
        <button type="button" class="sp-ghost" id="stClose">Close</button>
      </div>
    </div>
  </div>

  <h2 class="places-h">Other paths</h2>
  {B.directory(exclude=p['slug'])}
</main>

{B.foot()}<script src="/assets/stump.js"></script>
</body>
</html>
"""
    B.write("stories/index.html", page)
    B.write("assets/stump.js", open(os.path.join(B.SRC, "stump.js"), encoding="utf-8").read())

    for i, x in enumerate(essays):
        url = f"{path}{x['slug']}/"
        ld = B.jsonld({"@context": "https://schema.org", "@type": "Article", "headline": x["title"], "description": x["summary"],
                       "datePublished": x["date"], "author": {"@type": "Person", "name": x["author"]},
                       "publisher": {"@type": "Organization", "name": B.NAME, "url": B.DOMAIN + "/"},
                       "mainEntityOfPage": B.DOMAIN + url, "url": B.DOMAIN + url})
        others = [y for y in essays if y is not x][:3]
        more = ("<h2 class=\"places-h\">More from the Stump</h2><ul class=\"st-essays\">" + "".join(
            f'<li><a class="st-essay" href="{path}{y["slug"]}/"><span class="st-edate">{E(nice_date(y["date"]))}</span>'
            f'<span class="st-etitle">{E(y["title"])}</span><span class="st-esum">{E(y["summary"])}</span></a></li>' for y in others) + "</ul>") if others else ""
        page = B.head(f"{x['title']} · {B.NAME}", x["summary"] or x["title"], url, p["slug"], ld)
        page += header() + f"""
<main class="st st-article">
  <article>
    <p class="who"><a href="{path}">Reynard's Stump</a> · Essays</p>
    <h1>{E(x['title'])}</h1>
    <p class="st-byline">{E(x['author'])} · {E(nice_date(x['date']))} · {x['minutes']} min read</p>
    <div class="st-body">
{markdown(x['body'])}
    </div>
  </article>
  <p class="st-back"><a class="back-btn" href="{path}#read">&larr; Back to the Stump</a></p>
  {more}
</main>

{B.foot()}</body>
</html>
"""
        B.write(f"stories/{x['slug']}/index.html", page)
    return essays
