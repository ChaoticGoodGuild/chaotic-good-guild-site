"""Renders the link-preview images (what shows when someone shares a page) into site/assets/share/.

Needs Playwright and Chrome. Run after build.py whenever the artwork changes:
    python3 tools/share_images.py
"""
import asyncio, json, os
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
PLACES = json.load(open(os.path.join(ROOT, "src", "places.json")))
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")


async def main():
    out = os.path.join(SITE, "assets", "share")
    os.makedirs(out, exist_ok=True)
    svg = "file://" + os.path.join(SITE, "assets", "village.svg")
    logo = "file://" + os.path.join(SITE, "assets", "logo.png")
    shots = [("home", "")] + [(p["slug"], "#v-" + p["slug"]) for p in PLACES]
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path=CHROME)
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for name, frag in shots:
            tmp = os.path.join(out, "_render.html")
            open(tmp, "w").write(f"""<html><body style="margin:0;background:#0d0418">
<img src="{svg}{frag}" style="width:1200px;height:630px;object-fit:cover;display:block">
<img src="{logo}" style="position:absolute;left:34px;top:24px;height:150px;filter:drop-shadow(0 3px 10px #000)">
</body></html>""")
            await pg.goto("file://" + tmp)
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=os.path.join(out, name + ".png"))
        await b.close()
    os.remove(os.path.join(out, "_render.html"))
    print("Rendered", len(shots), "share images")

asyncio.run(main())
