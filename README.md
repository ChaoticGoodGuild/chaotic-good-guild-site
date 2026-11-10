# Chaotic Good Guild website

The website at [www.chaoticgoodguild.com](https://www.chaoticgoodguild.com): an illustrated village where each character leads to a room of the Guild.

## How it's organized

| Folder | What's in it |
|---|---|
| `site/` | The finished website that Netlify publishes. Generated, so don't edit it by hand. |
| `src/places.json` | Every room: its web address, title, popup text, sparkle marker, and the part of the village shown on its page. |
| `src/site.css` | Shared look for every page (colors, fonts, layout). |
| `src/logo.b64`, `src/star.b64` | The Guild logo and its star (PNG images stored as text). |
| `tools/scene.py` | The village artwork, drawn in code so every character stays consistent. |
| `tools/build.py` | Turns `src/` and `tools/scene.py` into the finished `site/`. |
| `tools/share_images.py` | Renders the preview pictures that appear when a page is shared. |

## Rooms

| Address | Room |
|---|---|
| `/tarot/` | The Star Spread |
| `/calendar/` | The Guild Calendar |
| `/notice-board/` | The Notice Board |
| `/guild-hall/` | The Guild Hall |
| `/stories/` | Reynard's Stump |
| `/market/` | The Galleon Market |
| `/about/` | The Raising |
| `/alignment-test/` | The City on the Hill |

## Making a change

1. Edit the files in `src/` or `tools/`.
2. Run `python3 tools/build.py` (and `python3 tools/share_images.py` if the artwork changed).
3. Commit and push. Netlify publishes the new version within a minute or two.
