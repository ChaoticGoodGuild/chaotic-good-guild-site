"""Join the Guild (/join/), its no-script thank-you page (/join/thanks/), and the privacy page (/privacy/)."""
import html
import build as B

e = lambda s: html.escape(str(s), quote=True)
def top():
    return f"""
<header class="top">
  <a class="brand" href="/" aria-label="{B.NAME} home"><img src="/assets/logo.png" alt="{B.NAME}" width="345" height="360"></a>
  <a class="back-link" href="/">&larr; The village</a>
</header>
"""


def page(path, title, desc, body, image="about", robots=""):
    out = B.head(title, desc, path, image, robots)
    out += top() + f'<main class="cj-page">\n{body}\n</main>\n\n{B.foot()}</body>\n</html>\n'
    B.write(path.strip("/") + "/index.html", out)


def build():
    page("/join/", f"Join the Guild · {B.NAME}",
         "Join the Chaotic Good Guild: letters from Reynard the Fox, new tales from the Stump, festivals on the Wheel of the Year, "
         "and first word when the Guild Hall opens.",
         f"""<p class="who">The Guild's door</p>
<h1>Join the Guild</h1>
<p class="cj-lede">There's no oath and no dues. Leave your name, and now and then a letter will find you: a new tale from Reynard's Stump,
a festival turning on the wheel, a card worth sitting with, and first word when the Guild Hall opens its doors and the deck goes to print.</p>
<p class="cj-lede">No more than a couple of letters a month. Every one has a way out at the bottom, and leaving is as easy as joining.</p>
{B.signup("join-page", "Leave your name at the door", "Rebels, misfits and good-hearted troublemakers welcome.", more=False)}""")

    page("/join/thanks/", f"Welcome to the Guild · {B.NAME}", "You've joined the Chaotic Good Guild.",
         """<p class="who">The Guild's door</p>
<h1>Welcome to the Guild.</h1>
<p class="cj-lede">Reynard has your name. Watch for his first letter, and keep an eye on the night sky.</p>
<p><a class="back-btn" href="/">Back to the village &rarr;</a></p>""", robots='<meta name="robots" content="noindex">\n')

    mail = B.CONFIG.get("contact_email", "")
    page("/privacy/", f"Privacy · {B.NAME}",
         "What the Chaotic Good Guild collects, why, where it's kept, and how to have it removed.",
         f"""<p class="who">The fine print, in plain words</p>
<h1>Privacy</h1>
<p class="cj-upd">Last updated {e(B.CONFIG.get("privacy_updated", ""))}</p>
<div class="cj-prose">
<h2>The short version</h2>
<p>We collect as little as we can, we never sell or share it, and you can have it removed anytime.</p>

<h2>If you join the Guild</h2>
<p>We keep your email address, and, only if you give them, the name you'd like us to call you and your alignment. We also note which page
you joined from and that you said you're 18 or older. We use this only to send you letters from the Guild. Signups are stored by our web host,
Netlify, and copied into the service we use to send letters. Every letter has an unsubscribe link at the bottom.</p>

<h2>The alignment test and the tarot</h2>
<p>Your answers are scored in your own browser. The test asks your age range first. If you're 18 or older, the Guild collects anonymous data
when you finish, to improve the test: your age range, your answers, your result, the version of the test and the month, with no name, no email
and no IP address. You can turn this off with the checkbox before you begin. If you're under 18 or would rather not say, nothing is collected.
Your browser also remembers your final alignment so the Guild Hall can offer it to you later; you can clear it from the result page with
"Forget my result." Tarot readings are dealt in your browser and aren't saved anywhere.
A reading or result you share as a picture is made on your device and goes only where you send it.</p>

<h2>Your journal and the app</h2>
<p>Readings you keep in your journal, your notes on them, and today's card are stored only in your own browser, on your own device.
They are never sent to us or anyone else, and we can't see them. Installing the Guild as an app saves pages on your device so they work
without a connection. Clearing your browser's data for this site removes all of it.</p>

<h2>Visits to the site</h2>
<p>We may count visits with Cloudflare Web Analytics, which uses no cookies and doesn't follow you around the web. It tells us things like which
pages are read and which countries visitors come from, never who you are. We don't use advertising trackers.</p>

<h2>Videos</h2>
<p>Videos on Reynard's Stump come from YouTube and TikTok. Nothing loads from them until you press play. Once you do, that service's own privacy
policy applies to what you watch.</p>

<h2>Younger visitors</h2>
<p>Anyone can explore the village. Joining the Guild's letters and sharing test answers are for people 18 and older, and we don't knowingly
collect anything from anyone under 18. If you think someone younger has signed up, write to us and we'll remove them.</p>

<h2>Removing your information</h2>
<p>To leave, use the unsubscribe link in any letter. To have everything we hold about you deleted, or to ask what we hold, write to
{f'<a href="mailto:{e(mail)}">{e(mail)}</a>' if mail else "us"} and we'll take care of it.</p>
</div>""")
