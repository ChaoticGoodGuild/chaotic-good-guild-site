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
| `src/alignment.json` | The alignment test: statements, answer scale, and the nine results. |
| `src/alignment.js` | How the alignment test runs and scores, entirely in the visitor's browser. |
| `src/alignments/` | The nine result portraits. |
| `docs/alignment-items.md` | A readable list of the test's statements for review (generated). |
| `tools/test_alignment.js` | Checks the scoring: `node tools/test_alignment.js` |

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
| `/alignment-test/` | The City on the Hill: the alignment test |
| `/alignment-test/<alignment>/` | One page for each of the nine alignments, e.g. `/alignment-test/chaotic-good/` |

## Making a change

1. Edit the files in `src/` or `tools/`.
2. Run `python3 tools/build.py` (and `node tools/test_alignment.js` if you changed the test) (and `python3 tools/share_images.py` if the artwork changed).
3. Commit and push. Netlify publishes the new version within a minute or two.
