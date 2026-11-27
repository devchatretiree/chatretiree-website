"""Builds the site's pages from one shared header and footer.
The finished .html files are committed, so the site needs no build step to be hosted.
Run: python3 tools/build.py  (from the repository folder)"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Bump when site.css or a script changes, so browsers fetch the new copy.
VERSION = "42"

def ico(body, fill=False):
    if fill:
        return f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">{body}</svg>'
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>')

# The porch light mark (app, 2026-11-27): a speech bubble made of warm light on a sky split between day and night.
# Gradients live once per page in SPRITE, so every copy of the mark can share them.
LOGO = ('<svg viewBox="0 0 120 120" aria-hidden="true" focusable="false"><clipPath id="crClip"><rect width="120" height="120" rx="28"/></clipPath>'
        '<g clip-path="url(#crClip)"><rect width="120" height="120" fill="url(#crDusk)"/><path d="M0 0H120L0 120z" fill="url(#crDay)"/></g>'
        '<g transform="translate(-10.29 -6.31) scale(1.1778)"><path d="M60 26a30 30 0 1 1-13.8 56.6L29.5 86.5l4.6-14.6A30 30 0 0 1 60 26z" fill="url(#crGlow)"/><path d="M48 70V54a12 12 0 0 1 24 0v16z" fill="#FFF8EA" stroke="#D29B66" stroke-width="2.6" stroke-linejoin="round"/><path d="M60 42v28M48 57h24" stroke="#D29B66" stroke-width="2.6"/></g></svg>')
# The light on its own, with its arched window (app PR 86: "we are always home for them"), for the hero.
GLOW = ('<svg viewBox="16 20 90 76" aria-hidden="true" focusable="false">'
        '<path d="M60 26a30 30 0 1 1-13.8 56.6L29.5 86.5l4.6-14.6A30 30 0 0 1 60 26z" fill="url(#crGlow)"/>'
        '<path d="M48 70V54a12 12 0 0 1 24 0v16z" fill="#FFF8EA" stroke="#D29B66" stroke-width="2.6" stroke-linejoin="round"/>'
        '<path d="M60 42v28M48 57h24" stroke="#D29B66" stroke-width="2.6"/></svg>')
SPRITE = ('<svg class="sprite" width="0" height="0" aria-hidden="true" focusable="false"><defs>'
          '<radialGradient id="crGlow" cx="45%" cy="40%" r="60%"><stop offset="0" stop-color="#FFF6DF"/><stop offset=".45" stop-color="#FFD58A"/><stop offset="1" stop-color="#F09A3E"/></radialGradient>'
          '<linearGradient id="crDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B2147"/><stop offset=".55" stop-color="#3A3566"/><stop offset=".85" stop-color="#7A4F72"/><stop offset="1" stop-color="#B9746C"/></linearGradient>'
          '<linearGradient id="crDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8DB8E2"/><stop offset=".6" stop-color="#C3DAEC"/><stop offset="1" stop-color="#F7DCC4"/></linearGradient>'
          '<radialGradient id="crHalo" cx="50%" cy="50%" r="50%"><stop offset=".3" stop-color="#FFC56E" stop-opacity=".55"/><stop offset="1" stop-color="#FFC56E" stop-opacity="0"/></radialGradient>'
          '<linearGradient id="crPuff" x1="0" y1="0" x2="0" y2="1"><stop offset=".35" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E3EAF4"/></linearGradient>'
          '</defs></svg>')

def cloud(shape):
    puffs = [[(42,50,20),(72,36,28),(106,40,24),(132,53,16)],[(38,54,16),(62,44,22),(96,30,30),(132,50,18)],[(44,46,24),(80,40,22),(108,50,18),(134,56,13)]][shape]
    c = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#crPuff)"/>' for x, y, r in puffs)
    return (f'<svg viewBox="0 0 160 80" aria-hidden="true" focusable="false"><ellipse cx="84" cy="74" rx="62" ry="5" fill="#B7C6DA" fill-opacity=".18"/>{c}'
            f'<rect x="24" y="48" width="124" height="24" rx="12" fill="url(#crPuff)"/><circle cx="{puffs[1][0]-8}" cy="{puffs[1][1]-8}" r="9" fill="#fff" fill-opacity=".7"/></svg>')

# A sky that follows the visitor's own clock (set by site.js): sun or moon on a low arc, drifting clouds by day, stars at night.
SKY = ('<div class="sky" aria-hidden="true"><div class="sky-stars"></div><div class="sky-body"><span class="sky-sun"></span>'
       '<svg class="sky-moon" viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" class="moon-dark"/><path class="moon-lit" d="M20 4a16 16 0 1 1 0 32a16 16 0 1 1 0-32z"/></svg></div>'
       f'<span class="cloud c1">{cloud(0)}</span><span class="cloud c2">{cloud(1)}</span><span class="cloud c3">{cloud(2)}</span></div>')

I = {
  "check": ico('<path d="M12 3a8.5 8.5 0 1 1-4.2 15.9L3.5 20.5l1.4-4.1A8.5 8.5 0 0 1 12 3z"/><path d="M9.8 9.6a2.3 2.3 0 1 1 3.2 2.1c-.7.3-1 .8-1 1.5v.3"/><path d="M12 16.3h.01"/>'),
  "medicare": ico('<path d="M12 3a8.5 8.5 0 1 1-4.2 15.9L3.5 20.5l1.4-4.1A8.5 8.5 0 0 1 12 3z"/><path d="M12 15.2s-3.6-2.1-3.6-4.6a1.9 1.9 0 0 1 3.6-.9 1.9 1.9 0 0 1 3.6.9c0 2.5-3.6 4.6-3.6 4.6z"/>'),
  "alerts": ico('<path fill-rule="evenodd" d="M12 2.6c4.5 0 7.8 3.3 7.8 8v3.8c0 4-3.5 6.9-7.8 6.9s-7.8-2.9-7.8-6.9v-3.8c0-4.7 3.3-8 7.8-8z M7.4 8.4h9.2a2.1 2.1 0 0 1 0 4.2H7.4a2.1 2.1 0 0 1 0-4.2z M12 14.8c1.6 0 2.7.8 2.7 1.8s-1.1 1.8-2.7 1.8-2.7-.8-2.7-1.8 1.1-1.8 2.7-1.8z"/><circle cx="9" cy="10.5" r="1.2"/><circle cx="15" cy="10.5" r="1.2"/>', fill=True),
  "trusted": ico('<circle cx="9" cy="8" r="3"/><path d="M3.5 19.5a5.5 5.5 0 0 1 11 0"/><circle cx="16.5" cy="9" r="2.5"/><path d="M15.5 14.2a4.5 4.5 0 0 1 5.5 4.3"/>'),
  "lifering": ico('<circle cx="12" cy="12" r="9.5"/><circle cx="12" cy="12" r="4"/><path d="m4.9 4.9 4.3 4.3M14.8 14.8l4.3 4.3M14.8 9.2l4.3-4.3M4.9 19.1l4.3-4.3"/>'),
  "tick": ico('<circle cx="12" cy="12" r="9.5"/><path d="m8 12.5 2.8 2.8L16.5 9.5"/>'),
  "mail": ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>'),
  "phone": ico('<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18.5h2"/>'),
  "heart": ico('<path d="M12 20s-7.5-4.4-7.5-10A4.2 4.2 0 0 1 12 7.6 4.2 4.2 0 0 1 19.5 10c0 5.6-7.5 10-7.5 10z"/>'),
  "paste": ico('<rect x="5" y="4" width="14" height="17" rx="2"/><rect x="9" y="2" width="6" height="4" rx="1"/><path d="M9 11h6M9 15h4"/>'),
  "arrow": ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
  "back": ico('<path d="M19 12H5M11 6l-6 6 6 6"/>'),
  "info": ico('<circle cx="12" cy="12" r="9.5"/><path d="M12 11v5M12 7.5h.01"/>'),
  "warn": ico('<path d="M10.3 3.9 2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>'),
  "question": ico('<circle cx="12" cy="12" r="9.5"/><path d="M9.6 9.4a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1.1.9-1.1 1.6v.3"/><path d="M12 16.8h.01"/>'),
  "handshake": ico('<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2l-3.9-3.9a2 2 0 0 0-2.8 0l-.9.9a1.4 1.4 0 0 1-2-2l2.8-2.8a3.5 3.5 0 0 1 4.3-.5l.6.4a2 2 0 0 0 1.4.3L21 6.5"/><path d="m21 5.5 1 9-2 1"/><path d="M3 5.5l-1 9 6.5 6.5a1.4 1.4 0 0 0 2-2"/><path d="M3 6.5h7"/>'),
  "lock": ico('<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>'),
  "eyeoff": ico('<path d="M3 3l18 18"/><path d="M10.6 5.1A9.8 9.8 0 0 1 12 5c5 0 8.5 4.5 9.5 7-.4 1-1.2 2.3-2.4 3.5M6.3 6.3C4.4 7.6 3 9.6 2.5 12c1 2.5 4.5 7 9.5 7 1.7 0 3.2-.5 4.5-1.2"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/>'),
  "noad": ico('<circle cx="12" cy="12" r="9.5"/><path d="M5.3 5.3l13.4 13.4"/>'),
  "link": ico('<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/>'),
  "trash": ico('<path d="M4 7h16M9.5 7V4.5h5V7M6.5 7l1 13h9l1-13"/>'),
  "moon": '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>',
  "sun": '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
}

def page(path, title, description, body, current=""):
    depth = 0 if path in ("", "404") else path.count("/") + 1
    up = "/" if path == "404" else "../" * depth
    def nav(href, label, key, cls=""):
        cur = ' aria-current="page"' if key == current else ""
        c = f' class="{cls}"' if cls else ""
        return f'<a href="{up}{href}"{cur}{c}>{label}</a>'
    extra_head = f'<script src="{up}assets/examples.js?v={VERSION}"></script>' if path.startswith("examples/") else ""
    full_title = title if title.startswith("ChatRetiree") else f"{title} · ChatRetiree"
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#F7F1E9">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://chatretiree.com/assets/icon.png?v={VERSION}">
<link rel="icon" href="{up}assets/favicon.png?v={VERSION}" type="image/png">
<link rel="apple-touch-icon" href="{up}assets/icon.png?v={VERSION}">
<link rel="stylesheet" href="{up}assets/site.css?v={VERSION}">
<script src="{up}assets/site.js?v={VERSION}"></script>
{extra_head}
</head>
<body>
{SPRITE}
<a class="skip" href="#main">Skip to main content</a>
<header class="top"><div class="wrap">
  <a class="brand" href="{up or './'}" aria-label="ChatRetiree home">{LOGO}<span><b>Chat</b>Retiree</span></a>
  <nav class="nav" aria-label="Main">
    {nav("about/", "About", "about", "hide-sm")}
    {nav("privacy/", "Privacy", "privacy", "hide-sm")}
    {nav("contact/", "Contact", "contact", "hide-sm")}
    <a class="get-app" href="{up}app/"{' aria-current="page"' if current=="app" else ""}>Get the app</a>
    <button class="theme" type="button" hidden aria-label="Switch to dark" aria-pressed="false">{I["moon"]}{I["sun"]}</button>
  </nav>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
  <div>
    <a class="brand" href="{up or './'}" aria-label="ChatRetiree home">{LOGO}<span><b>Chat</b>Retiree</span></a>
    <p class="tag">Always home. Always here to help.</p>
  </div>
  <nav aria-label="Footer">
    {nav("about/", "About us", "about")}
    {nav("privacy/", "Privacy policy", "privacy")}
    <a href="{up}#partner">Partner with us</a>
    {nav("contact/", "Contact us", "contact")}
  </nav>
  <small>© 2026 ChatRetiree. This website uses no cookies and no tracking.</small>
</div></footer>
</body>
</html>
'''
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    if path == "404":
        out = ROOT / "404.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

# ---------- Example pages: made-up inputs, the app's own answers ----------
# Scam-check answers below are the app's check engine output (shared/assess.ts in chatretiree-app)
# for its own sample messages. Medicare and scam-question answers are real answers the system gave
# to made-up questions on November 25, 2026. Never write new "answers" by hand.

LEVELS = {
  "strong": ("lv-strong", I["warn"], "This has the signs of a scam", "We looked at everything"),
  "verify": ("lv-verify", I["question"], "Check with them before you do anything", "We looked at everything"),
}

def ul(items, tag="ul"):
    return f"<{tag}>" + "".join(f"<li>{x}</li>" for x in items) + f"</{tag}>"

def verdict(level, summary):
    cls, icon, title, status = LEVELS[level]
    return (f'<div class="verdict {cls}"><div class="top"><span class="badge">{icon}</span><h3>{title}</h3></div>'
            f'<p>{summary}</p><span class="status">{status}</span></div>')

def panel(title, inner, cls=""):
    return f'<div class="panel {cls}"><h4>{title}</h4>{inner}</div>'

def reply(inner):
    return f'<div class="reply"><p class="who">{LOGO}ChatRetiree</p>{inner}</div>'

def example(eid, chip, label, shown, button, answer, thinking="Looking at it with you…"):
    return f"""
<article class="ex" id="{eid}" data-chip="{chip}">
  <h2 class="ex-h">{chip}</h2>
  <div class="stage">
    <p class="who-label">{label}</p>
    {shown}
    <button class="btn btn-primary go" type="button">{button}</button>
    <p class="thinking" aria-hidden="true"><span class="dots"><i></i><i></i><i></i></span>{thinking}</p>
    <div class="answer" tabindex="-1">
      {answer}
    </div>
  </div>
</article>"""

NOTE = f'<p class="ex-note">{I["info"]}<span>These are real screens from the ChatRetiree app, using sample messages and questions.</span></p>'

def ex_page(slug, title, lead, chips_title, examples, current):
    others = [x for x in EX_LINKS if x[0] != current]
    nxt = "".join(f'<a href="../{s}/">{f"<span class=\"icon {t}\">{I[i]}</span>"}{n}</a>' for s, n, i, t in others)
    return f"""
<div class="ex-page">
  <a class="back" href="../../#help">{I["back"]}All the ways we help</a>
  <h1>{title}</h1>
  <p class="lead">{lead}</p>
  {NOTE}
  <div class="pick">
    <h2>{chips_title}</h2>
    <div class="chips" role="group" aria-label="{chips_title}"></div>
    <div class="examples" aria-live="polite">
      {"".join(examples)}
    </div>
  </div>
  <div class="next-ex">
    <h2>See more of what <span class="wm"><b>Chat</b>Retiree</span> can do</h2>
    <div class="next-list">{nxt}</div>
  </div>
</div>"""

EX_LINKS = [
  ("check", "Check a message", "check", "t-teal"),
  ("medicare", "Medicare questions", "medicare", "t-blue"),
  ("scams", "Scams going around", "alerts", "t-clay"),
  ("trusted", "Ask someone you trust", "trusted", "t-sage"),
]

WHATS_NEXT = "What we’d do next"
WHY = "Why we think so"

def device(img, alt, cls=""):
    return (f'<figure class="device {cls}"><div class="device-screen" tabindex="0" role="group" aria-label="App screen. Scroll to see more.">'
            f'<img src="../../assets/app/{img}.webp?v={VERSION}" alt="{alt}" width="390"></div></figure>')

def phone_ex(eid, chip, label, result_img, result_alt, input_img=None, input_alt="", button="Send it", after="", thinking="Looking at it with you…"):
    first = (device(input_img, input_alt, "step-in") + f'<button class="btn btn-primary go" type="button">{button}{I["arrow"]}</button>'
             f'<p class="thinking" aria-hidden="true"><span class="dots"><i></i><i></i><i></i></span>{thinking}</p>') if input_img else ""
    ans_cls = "answer" if input_img else "answer shown"
    return f"""
<article class="ex" id="{eid}" data-chip="{chip}">
  <h2 class="ex-h">{chip}</h2>
  <p class="who-label">{label}</p>
  <div class="ex-row">
    <div class="ex-phone">{first}<div class="{ans_cls}" tabindex="-1">{device(result_img, result_alt)}<p class="scroll-hint">Scroll inside the phone to see more.</p></div></div>
    {f'<div class="ex-side">{after}</div>' if after else ''}
  </div>
</article>"""

CHECK_NOTE = '<p>The app looks for the warning signs scammers rely on, checks links against Google’s list of known harmful websites without opening them, and tells you what to do next.</p><p style="margin-top:12px">It never calls something “safe.” When it can’t tell, it says so and helps you check another way.</p>'

CHECK_EX = [
  phone_ex("package", "A text about a package", "Someone pastes a text they got into the message bar, then taps send.",
    "package", "The app’s answer: This has the signs of a scam. This message has several signs that are common in scams. What we’d do next: Don’t reply, click links or pay. Contact the company using a phone number or website you already trust. Why we think so: It asks for a small fee. Fake delivery notices do this to collect card details. It warns that something bad will happen to your account, benefits or device. It pushes you to act right away, before you have time to check.",
    "package-input", "The app with a pasted text: PARCEL NOTICE: Your package is on hold due to an unpaid $1.99 redelivery fee. Pay now to avoid return to sender, with a link.", after=CHECK_NOTE),
  phone_ex("bank", "A picture of a bank text", "Someone taps + and adds a screenshot. The app reads the words right on the phone, and only the words are checked.",
    "bank", "The app’s answer: This has the signs of a scam. What we’d do next: Don’t reply or move any money. Call your bank using the number on the back of your card or on your statement. Why we think so: It asks you to move money to a so-called safe account. Real banks never ask you to do this. It tells you to keep it secret. It warns that something bad will happen to your account.",
    "bank-input", "The app’s message bar holding the words it read from a screenshot of a text from First Harbor Bank, ready to send.", after=CHECK_NOTE),
  phone_ex("call", "A worrying phone call", "Someone types or says what happened on a call.",
    "call", "The app’s answer: This has the signs of a scam. If you’re worried someone you love is in trouble: if someone may be in danger right now, call 911. Hang up, then call your family member yourself on a number you already have. Don’t send any money, gift cards or cryptocurrency. Why we think so: it asks for payment with gift cards, it tells you to keep it secret, and it describes a family emergency that needs money fast.",
    "call-input", "The app with a description: a young man called saying he was my grandson, in jail, needing $3,000 bail paid in gift cards.", after=CHECK_NOTE),
  phone_ex("doctor", "A message from a doctor’s office", "Not everything is a scam. When we can’t tell, we say so.",
    "doctor", "The app’s answer: Check with them before you do anything. Nothing proves this message is a scam, but some things need checking before you respond. What we’d do next: contact them yourself using a phone number or website you already have, not one from the message.",
    "doctor-input", "The app with a pasted text: Hi, this is Dr. Patel’s office calling about your recent test results. Please call us back.", after=CHECK_NOTE),
]

MED_NOTE = '<p>Answers come only from the official Medicare guides. Tap “More detail and sources” in the app to see the guide’s exact words and page.</p><p style="margin-top:12px">For questions about your own plan, the app points you to 1-800-MEDICARE or your free local SHIP counselor.</p>'
MEDICARE_EX = [
  phone_ex("dental", "Does Medicare cover dental?", "Someone asks in their own words.", "medicare-dental",
    "Question: Does Original Medicare cover dental care? The app’s answer: In most cases, Original Medicare does not cover routine dental services like cleanings, fillings, tooth extractions, or dentures.", after=MED_NOTE),
  phone_ex("hearing", "Hearing aids", "Someone asks in their own words.", "medicare-hearing",
    "Question: Does Medicare pay for hearing aids? The app’s answer: Original Medicare does not cover hearing aids or exams for fitting them. Some Medicare Advantage Plans may offer coverage for hearing services that Original Medicare does not.", after=MED_NOTE),
  phone_ex("signup", "When to sign up", "Someone asks in their own words.", "medicare-signup",
    "Question: When can I sign up for Medicare? The app’s answer: Your Initial Enrollment Period is a 7-month window that starts 3 months before the month you turn 65, includes your birthday month, and ends 3 months after.", after=MED_NOTE),
]

SCAM_NOTE = '<p>Answers come only from official warnings by the FTC, the FBI and the U.S. Department of Health and Human Services. The app shows which alert each answer comes from.</p><p style="margin-top:12px">When the official warnings don’t cover something, we say so instead of guessing. And we never suggest paying a scammer anything.</p>'
SCAM_EX = [
  phone_ex("giftcards", "Why gift cards?", "Someone asks about a scam.", "scam-giftcards",
    "Question: Why do scammers ask for gift cards? The app first says: Please don’t send them anything. Then the short answer: Scammers prefer gift cards because it is almost impossible to get your money back once they have collected it. Scammers want you to panic and send money quickly, before you have time to think or talk to someone you trust.", after=SCAM_NOTE),
  phone_ex("bail", "A grandchild needs bail", "Someone asks about a scam.", "scam-bail",
    "Question: Someone says my grandson is in jail and needs bail money. What do I do? The app first says: Please don’t send them anything. Then: If you get a call from someone claiming to be a family member in trouble, slow down and hang up the phone. Then call another family member or friend to check whether the story is true.", after=SCAM_NOTE),
  phone_ex("haggle", "Paying them a little less", "Someone asks about a scam.", "scam-haggle",
    "Question: Should I offer the scammer a smaller amount so they leave me alone? The app says: Please don’t send them anything. Please don’t send them any money or gift cards, and don’t offer a smaller amount. If you already sent money or gift cards, call your bank or the gift card company right away.", after=SCAM_NOTE),
]

TRUSTED_EMAIL = ("Hi Sarah, can you look at this with me before I do anything?\n\n"
  "ChatRetiree said: This has the signs of a scam.\nThis message has several signs that are common in scams.\n\n"
  "Here’s what I got:\n“PARCEL NOTICE: Your package is on hold due to an unpaid $1.99 redelivery fee. Pay now to avoid return to sender: hxxps://parcel-redelivery[.]example/pay?id=88213”\n\n"
  "(Links are broken on purpose so nobody taps them by accident.)")

TRUSTED_EX = [
  phone_ex("sarah", "Ask Sarah about a text", "After a check, someone taps “Email Sarah.”", "trusted",
    "The app’s result screen with an Ask someone you trust card and an Email Sarah button.",
    after=('<p>Their own email app opens with this note. They can read it and change it. Nothing is sent until they press send.</p>'
           f'<div class="email" style="margin-top:16px"><div class="hdr"><div><strong>To:</strong> Sarah</div><div><strong>Subject:</strong> Can you look at this with me?</div></div>'
           f'<div class="body">{TRUSTED_EMAIL}</div></div>'
           '<p class="cite" style="margin-top:16px">The people you trust are kept only on your phone. Their names and email addresses are never sent to us.</p>')),
]

PARTNER = f"""
<section id="partner" aria-labelledby="partner-h"><div class="wrap split">
  <div>
    <h2 id="partner-h">Partner with us</h2>
    <p class="lead">Do you look after retirees or older adults? We’d love to talk about helping the people you serve stay a step ahead of scams.</p>
  </div>
  <div class="card">
    <div class="icon t-teal">{I["handshake"]}</div>
    <h3>For organizations</h3>
    <p>School districts, retiree associations, insurers, credit unions, and community and public groups. Tell us a little about your organization and the people you serve.</p>
    <p style="margin-top:20px"><a class="btn btn-primary" href="mailto:support@chatretiree.com?subject=Partnering%20with%20ChatRetiree">{I["mail"]}Email us about partnering</a></p>
  </div>
</div></section>
"""


HOME = f'''
<section class="h-hero" aria-labelledby="hero-h">
  {SKY}
  <div class="h-hero-in">
    <div class="h-hero-copy">
      <a class="h-pill" href="app/">{I["phone"]}Coming soon to iPhone and Android{I["arrow"]}</a>
      <div class="porch" aria-hidden="true"><span class="porch-halo"></span>{GLOW}</div>
      <h1 id="hero-h"><span>Always home.</span> <span>Always here to help.</span></h1>
      <p class="h-lead">One simple place for what’s on your mind: check a message before you act, get straight answers about Medicare and Social Security, and get help if a scam already happened. In plain words, from sources you can trust.</p>
      <div class="h-actions">
        <a class="btn h-btn-light" href="#help">See it in action{I["arrow"]}</a>
        <a class="btn h-btn-ghost" href="#partner">Partner with us</a>
      </div>
    </div>
    <div class="h-phones">
      <figure class="h-ph h-ph-back" role="img" aria-label="The ChatRetiree app answering: Does Medicare pay for hearing aids? Original Medicare does not cover hearing aids or exams for fitting them. Some Medicare Advantage Plans may offer coverage for hearing services that Original Medicare does not.">
        <div class="h-ph-screen live has-compose" aria-hidden="true">
          <div class="lv-bar lv-slim"><i><svg viewBox="0 0 24 24"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></i><span>Medicare</span><i class="lv-me"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></i></div>
          <p class="lv-q" data-type="Does Medicare pay for hearing aids?">Does Medicare pay for hearing aids?</p>
          <span class="lv-dots"><i></i><i></i><i></i></span>
          <div class="lv-a"><p data-type="Original Medicare does not cover hearing aids or exams for fitting them. Some Medicare Advantage Plans may offer coverage for hearing services that Original Medicare does not.">Original Medicare does not cover hearing aids or exams for fitting them. Some Medicare Advantage Plans may offer coverage for hearing services that Original Medicare does not.</p></div>
          <span class="lv-more lv-after"><svg viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg>More detail and sources</span>
          <span class="lv-c lv-mic lv-spk lv-after"><svg viewBox="0 0 24 24"><path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z"/><path d="M16 9a5 5 0 0 1 0 6"/><path d="M19.364 18.364a9 9 0 0 0 0-12.728"/></svg></span>
          <span class="lv-more lv-after"><svg viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg>Talk to a person, and more</span>
          <div class="lv-compose"><span class="lv-c lv-plus"><svg viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M12 5v14"/></svg></span><span class="lv-box">Ask a follow-up…</span><span class="lv-c lv-mic"><svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/></svg></span></div>
          <div class="lv-tabs"><span class="on"><i><svg viewBox="0 0 24 24"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></i>Home</span><span><i><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path d="M9.6 9.4a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1.1.9-1.1 1.6v.3"/><path d="M12 16.8h.01"/></svg></i>Help</span><span><i><svg viewBox="0 0 24 24"><path d="M18 20a6 6 0 0 0-12 0"/><circle cx="12" cy="10" r="4"/><circle cx="12" cy="12" r="10"/></svg></i>Me</span></div>
        </div>
      </figure>
      <figure class="h-ph h-ph-front" role="img" aria-label="The ChatRetiree app checking a pasted text that claims to be from Medicare about a new Medicare card. Its answer: This has the signs of a scam. What we’d do next: Don’t call any number in the message. Contact the agency using the number on your card or its official website.">
        <div class="h-ph-screen live has-compose" aria-hidden="true">
          <div class="lv-bar lv-slim"><i><svg viewBox="0 0 24 24"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></i><span>Check for a scam</span><i class="lv-me"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg></i></div>
          <p class="lv-msg lv-sent">MEDICARE ALERT: Your new Medicare card is ready, but your benefits will be suspended today unless you confirm your Medicare number. Call 1-888-555-0147 now to keep your coverage.</p>
          <span class="lv-dots"><i></i><i></i><i></i></span>
          <div class="lv-a lv-verdict"><b data-type="This has the signs of a scam">This has the signs of a scam</b><p data-type="This message has several signs that are common in scams.">This message has several signs that are common in scams.</p></div>
          <div class="lv-a lv-next"><b>What we’d do next</b><p data-type="Don’t call any number in the message. Contact the agency using the number on your card or its official website.">Don’t call any number in the message. Contact the agency using the number on your card or its official website.</p></div>
          <div class="lv-compose lv-front"><span class="lv-c lv-plus"><svg viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M12 5v14"/></svg></span><span class="lv-box"><span class="lv-in lv-ph" data-type="MEDICARE ALERT: Your new Medicare card is ready, but your benefits will be suspended today unless you confirm your Medicare number. Call 1-888-555-0147 now to keep your coverage.">Paste or type it here</span></span><span class="lv-c lv-mic"><svg viewBox="0 0 24 24"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/></svg></span><span class="lv-c lv-send lv-btn"><svg viewBox="0 0 24 24"><path d="M3.714 3.048a.498.498 0 0 0-.683.627l2.843 7.627a2 2 0 0 1 0 1.396l-2.842 7.627a.498.498 0 0 0 .682.627l18-8.5a.5.5 0 0 0 0-.904z"/><path d="M6 12h16"/></svg></span></div>
          <div class="lv-tabs"><span class="on"><i><svg viewBox="0 0 24 24"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></i>Home</span><span><i><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path d="M9.6 9.4a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1.1.9-1.1 1.6v.3"/><path d="M12 16.8h.01"/></svg></i>Help</span><span><i><svg viewBox="0 0 24 24"><path d="M18 20a6 6 0 0 0-12 0"/><circle cx="12" cy="10" r="4"/><circle cx="12" cy="12" r="10"/></svg></i>Me</span></div>
        </div>
      </figure>
    </div>
  </div>
</section>

<section class="h-sources" aria-label="Where our answers come from">
  <div class="wrap h-sources-in">
    <p class="h-sources-label">Answers drawn from official sources</p>
    <ul class="h-sources-list">
      <li><a href="https://www.medicare.gov/" rel="noopener">Official Medicare guides</a></li>
      <li><a href="https://www.ssa.gov/pubs/" rel="noopener">Social Security publications</a></li>
      <li><a href="https://consumer.ftc.gov/consumer-alerts" rel="noopener">Federal Trade Commission</a></li>
      <li><a href="https://www.ic3.gov/" rel="noopener">FBI Internet Crime Complaint Center</a></li>
      <li><a href="https://oig.hhs.gov/" rel="noopener">HHS Office of Inspector General</a></li>
      <li><a href="https://cloud.google.com/web-risk" rel="noopener">Google Web Risk</a></li>
    </ul>
  </div>
</section>

<section class="h-why" aria-labelledby="why-h">
  <div class="wrap">
    <p class="h-eyebrow" id="why-h">Why We Built <span class="wm"><b>Chat</b>Retiree</span></p>
    <p class="h-statement">You’ve spent a lifetime figuring things out. <span>We’ll help you sort through the noise, so you can get back to what matters.</span></p>
    <p class="h-why-sub">It’s the flood of fake texts, look-alike emails, robocalls and fine print that lands on everyone, every day. ChatRetiree cuts through it, so you spend less time wondering and worrying.</p>
    <div class="h-why-grid">
      <div><h3>There’s too much noise</h3><p>Scam texts and fake alerts are everywhere, and they look more like the real thing every year.</p></div>
      <div><h3>Good answers are buried</h3><p>The right information is out there, spread across long guides and official websites that take time to dig through.</p></div>
      <div><h3>Wondering takes time</h3><p>One “Is this real?” moment can eat up an afternoon. You have better things to do with your day.</p></div>
    </div>
    <div class="h-believe">
      <p class="h-eyebrow">What We Believe</p>
      <p>Everyone deserves easy access to clear, trustworthy information, and a quick way to check before they act. So ChatRetiree answers only from official sources, in plain words, and shows you where each answer comes from.</p>
    </div>
  </div>
</section>

<section class="h-features" id="help" aria-labelledby="help-h">
  <div class="wrap">
    <div class="h-sec-head">
      <p class="h-eyebrow">What <span class="wm"><b>Chat</b>Retiree</span> Does</p>
      <h2 id="help-h">One friendly place for it all</h2>
    </div>

    <article class="h-row h-row-flip">
      <div class="h-row-copy">
        <span class="icon t-teal">{I["question"]}</span>
        <h3>Just ask what’s on your mind</h3>
        <p>Start with one box. Type a question, paste a message that seems off, or just say it out loud. We’ll take it to the right place, whether that’s a scam check, Medicare, Social Security or help after a scam.</p>
        <ul class="h-ticks">
          <li>{I["tick"]}One message bar everywhere: tap + to paste a message or add a picture, or tap the mic to say it</li>
          <li>{I["tick"]}Not sure where to start? Tap an example question</li>
          <li>{I["tick"]}Every answer ends with where to go next, so it all fits together</li>
        </ul>
      </div>
      <div class="h-row-art t-teal-bg"><figure class="h-ph"><div class="h-ph-screen"><img src="assets/app/home.webp?v={VERSION}" width="390" alt="The app’s home screen: What’s on your mind? Ask about Medicare, Social Security or scams, or share a message that seems off. Below it is the message bar with a plus button, a box and a microphone. Below it are example questions and sections for staying safe from scams and your benefits."></div></figure></div>
    </article>

    <article class="h-row">
      <div class="h-row-copy">
        <span class="icon t-teal">{I["check"]}</span>
        <h3>Check a message before you act</h3>
        <p>Paste a text or email, add a picture of your screen, or just tell us what happened. In a few seconds you’ll see what we found and exactly what to do next. It’s more than an opinion: every message goes through real checks.</p>
        <ul class="h-ticks">
          <li>{I["tick"]}Looks for the warning signs scammers rely on</li>
          <li>{I["tick"]}Checks links against Google’s list of known dangerous websites, without opening them</li>
          <li>{I["tick"]}Compares it with the latest scam alerts from the FTC, FBI and HHS</li>
          <li>{I["tick"]}Never calls anything “safe.” When we can’t tell, we say so</li>
        </ul>
        <a class="h-link" href="examples/check/">See four real samples{I["arrow"]}</a>
      </div>
      <div class="h-row-art t-teal-bg"><figure class="h-ph"><div class="h-ph-screen"><img src="assets/app/bank.webp?v={VERSION}" width="390" alt="The app’s answer to a bank text asking to move savings to a safe account: This has the signs of a scam. Don’t reply or move any money. Call your bank using the number on the back of your card."></div></figure></div>
    </article>

    <article class="h-row h-row-flip">
      <div class="h-row-copy">
        <span class="icon t-blue">{I["medicare"]}</span>
        <h3>Straight answers about your benefits</h3>
        <p>Ask about Medicare or Social Security in your own words, like you would ask a friend who knows them inside out. Answers come only from the official Medicare guides and Social Security publications, and you can see the exact words they’re based on.</p>
        <ul class="h-ticks">
          <li>{I["tick"]}Plain-language answers in a simple back-and-forth, like texting a friend. Type it or just say it</li>
          <li>{I["tick"]}Every point checked against the official guide</li>
          <li>{I["tick"]}For your own plan or benefits, we point you to the free official help: 1‑800‑MEDICARE, your local SHIP counselor, or Social Security</li>
        </ul>
        <a class="h-link" href="examples/medicare/">See sample Medicare questions{I["arrow"]}</a>
      </div>
      <div class="h-row-art t-blue-bg"><figure class="h-ph"><div class="h-ph-screen"><img src="assets/app/medicare-hearing.webp?v={VERSION}" width="390" alt="Question: Does Medicare pay for hearing aids? The app’s answer: Original Medicare does not cover hearing aids or exams for fitting them. Some Medicare Advantage Plans may offer coverage for hearing services. A box at the bottom lets you ask a follow-up by typing or speaking."></div></figure></div>
    </article>

    <article class="h-row">
      <div class="h-row-copy">
        <span class="icon t-clay">{I["alerts"]}</span>
        <h3>Know what’s going around</h3>
        <p>We follow the official scam warnings from the FTC, the FBI and the U.S. Department of Health and Human Services, and sum each one up in plain words. Ask about a scam and get an answer straight from those warnings.</p>
        <ul class="h-ticks">
          <li>{I["tick"]}New warnings summarized as they come out</li>
          <li>{I["tick"]}When the warnings don’t cover something, we say so instead of guessing</li>
          <li>{I["tick"]}We never suggest paying a scammer anything</li>
        </ul>
        <a class="h-link" href="examples/scams/">See sample questions{I["arrow"]}</a>
      </div>
      <div class="h-row-art t-clay-bg"><figure class="h-ph"><div class="h-ph-screen"><img src="assets/app/scam-giftcards.webp?v={VERSION}" width="390" alt="Question: Why do scammers ask for gift cards? The app replies like a text conversation: Please don’t send them any money or gift cards, and don’t offer a smaller amount. If you already sent money or gift cards, call your bank or the gift card company right away. A box at the bottom lets you ask another question."></div></figure></div>
    </article>

    <article class="h-row h-row-flip">
      <div class="h-row-copy">
        <span class="icon t-blue">{I["lifering"]}</span>
        <h3>Help after a scam</h3>
        <p>It happens to careful, smart people every day, and it’s not your fault. Pick what happened, like sending money or sharing your Social Security number, and we’ll go through the next steps together, one at a time.</p>
        <ul class="h-ticks">
          <li>{I["tick"]}Steps from official sources like the FTC and IdentityTheft.gov, with links to their own websites</li>
          <li>{I["tick"]}Reach Social Security, Medicare, the IRS or the Postal Service yourself, using their official contacts</li>
          <li>{I["tick"]}What you type there is matched to the steps on your phone. It isn’t sent or saved</li>
        </ul>
      </div>
      <div class="h-row-art t-blue-bg"><figure class="h-ph"><div class="h-ph-screen"><img src="assets/app/protect.webp?v={VERSION}" width="390" alt="The app’s Get help after a scam screen: Let’s work out the next steps. Choices include I paid or sent money, I gave my Social Security number, I gave a password or account number, I let someone into my computer or phone, and I clicked a link."></div></figure></div>
    </article>

    <article class="h-row">
      <div class="h-row-copy">
        <span class="icon t-sage">{I["trusted"]}</span>
        <h3>Decide together</h3>
        <p>Add a family member or friend you trust. After any check, one tap opens your own email with a note to them, so you can talk it over before doing anything.</p>
        <ul class="h-ticks">
          <li>{I["tick"]}You see the note first, and nothing is sent until you press send</li>
          <li>{I["tick"]}Links are broken on purpose so nobody taps them by accident</li>
          <li>{I["tick"]}Your trusted people stay on your phone, never on our servers</li>
        </ul>
        <a class="h-link" href="examples/trusted/">See how it works{I["arrow"]}</a>
      </div>
      <div class="h-row-art t-sage-bg"><figure class="h-ph"><div class="h-ph-screen"><img src="assets/app/trusted.webp?v={VERSION}" width="390" alt="The app’s result screen with an Email Sarah button to ask someone you trust."></div></figure></div>
    </article>
  </div>
</section>

<section class="h-trust" aria-labelledby="trust-h">
  <div class="wrap">
    <div class="h-sec-head">
      <p class="h-eyebrow">Private by Design</p>
      <h2 id="trust-h">Your information stays yours</h2>
    </div>
    <div class="h-trust-grid">
      <div><span class="h-trust-ic">{I["tick"]}</span><h3>We don’t keep what you check</h3><p>Your messages, pictures, links and questions are looked at, answered, and let go.</p></div>
      <div><span class="h-trust-ic">{I["tick"]}</span><h3>Private details hidden first</h3><p>Before anything leaves your phone, we hide Social Security, Medicare and card numbers, passwords and codes.</p></div>
      <div><span class="h-trust-ic">{I["tick"]}</span><h3>Your information is never for sale</h3><p>What you share with ChatRetiree is yours. We never sell it or pass it along to anyone who wants to market to you.</p></div>
    </div>
    <a class="h-link h-link-light" href="privacy/">Read our privacy policy{I["arrow"]}</a>
  </div>
</section>

<section class="h-help" aria-labelledby="sent-h">
  <div class="wrap">
    <div class="h-help-card">
      <div>
        <h2 id="sent-h">Think you’ve been scammed?</h2>
        <p>You’re not alone, and it’s not your fault.</p>
      </div>
      <ul>
        <li><strong>If someone may be in danger, call 911.</strong></li>
        <li>If you already sent money or gift cards, call your bank or the gift card company right away.</li>
        <li>You can also report it to the FTC at <a href="https://reportfraud.ftc.gov/" rel="noopener">ReportFraud.ftc.gov</a>.</li>
        <li>In the app, “Get help after a scam” walks you through the next steps, one at a time.</li>
      </ul>
    </div>
  </div>
</section>

<section class="h-end" aria-label="Coming soon and partners">
  <div class="wrap h-end-grid">
    <div class="h-end-card h-end-soon">
      <p class="h-eyebrow">Coming Soon</p>
      <h2>On iPhone and Android</h2>
      <p>We’re trying ChatRetiree with a small group of people first. Have a question in the meantime? We’d love to hear from you.</p>
      <a class="btn h-btn-light" href="mailto:support@chatretiree.com">{I["mail"]}Email us</a>
    </div>
    <div class="h-end-card" id="partner">
      <p class="h-eyebrow">Partner with Us</p>
      <h2>For organizations</h2>
      <p>School districts, retiree associations, insurers, credit unions, and community and public groups: let’s talk about helping the people you serve stay a step ahead of scams.</p>
      <a class="btn btn-primary" href="mailto:support@chatretiree.com?subject=Partnering%20with%20ChatRetiree">{I["handshake"]}Email us about partnering</a>
    </div>
  </div>
</section>
'''

ABOUT = f'''
<section class="a-hero a-hero-photo" aria-labelledby="about-h">
  <div class="a-photo-bg" role="img" aria-label="A smiling older woman looking at her phone at home."></div>
  <div class="wrap a-hero-copy">
    <p class="h-eyebrow">About <span class="wm"><b>Chat</b>Retiree</span></p>
    <h1 id="about-h">Clear answers, and a calm second look, whenever you need one.</h1>
    <p class="a-lead">ChatRetiree helps you check a message before you act, understand Medicare and Social Security in plain words, keep up with the scams going around, and know what to do if a scam already happened. It works like a knowledgeable friend: it looks at things with you and lets you decide.</p>
  </div>
  <p class="a-credit">Photo by Vitaly Gariev on <a href="https://unsplash.com/photos/elderly-woman-smiling-while-looking-at-smartphone-cHbyGVOQspk" rel="noopener">Unsplash</a></p>
</section>

<section class="a-sec" aria-labelledby="story-h">
  <div class="wrap a-split">
    <h2 id="story-h">Why we started</h2>
    <div class="a-prose">
      <p>People who have spent a lifetime working, raising families and running households know how to figure things out. What’s changed is the amount of noise. Fake texts, look-alike emails, robocalls and fine print arrive every day, and they get more convincing every year.</p>
      <p>Meanwhile, the good answers are out there, spread across long guides and official websites that take time to find and read. One “Is this real?” moment can turn into an afternoon of wondering and worrying.</p>
      <p>We built ChatRetiree to make the trustworthy information easy to reach and quick to check, so you can get on with your day.</p>
      <p>Our logo is a porch light: someone’s home, and they’ve left the light on for you. Day or night, it’s there when something doesn’t feel right.</p>
    </div>
  </div>
</section>

<section class="a-sec a-tint" aria-labelledby="promise-h">
  <div class="wrap">
    <p class="h-eyebrow">Our Promises</p>
    <h2 id="promise-h">What you can count on</h2>
    <ul class="a-promises">
      <li>{I["tick"]}<div><h3>Official sources only</h3><p>Medicare answers come from the official Medicare guides, and Social Security answers from Social Security’s own publications. Scam news comes from the FTC, the FBI and the U.S. Department of Health and Human Services, and help after a scam follows the FTC and IdentityTheft.gov.</p></div></li>
      <li>{I["tick"]}<div><h3>Plain words</h3><p>No jargon and no alarm bells. Just what we found and what we’d do next.</p></div></li>
      <li>{I["tick"]}<div><h3>Honest about what we don’t know</h3><p>We never call anything “safe.” When we can’t tell, or the official sources don’t cover something, we say so.</p></div></li>
      <li>{I["tick"]}<div><h3>You stay in charge</h3><p>We suggest next steps. You decide. Nothing is sent to anyone unless you press send.</p></div></li>
      <li>{I["tick"]}<div><h3>Your information stays yours</h3><p>We don’t keep what you check, we hide private details before anything leaves your phone, and we never sell your data.</p></div></li>
      <li>{I["tick"]}<div><h3>Your peace of mind comes first</h3><p>Everything we suggest is meant to protect you and your money. That’s why we’ll never suggest paying a scammer anything, not even a smaller amount to make them go away.</p></div></li>
    </ul>
  </div>
</section>

<section class="a-sec" aria-labelledby="src-h">
  <div class="wrap a-split">
    <h2 id="src-h">Where our answers come from</h2>
    <div class="a-prose">
      <p>We only use sources you could look up yourself:</p>
      <ul class="a-src">
        <li><a href="https://www.medicare.gov/" rel="noopener">Medicare.gov</a>, including the official “Medicare &amp; You” handbook and guides</li>
        <li><a href="https://www.ssa.gov/pubs/" rel="noopener">Social Security publications</a> from SSA.gov</li>
        <li><a href="https://consumer.ftc.gov/consumer-alerts" rel="noopener">Federal Trade Commission consumer alerts</a></li>
        <li><a href="https://www.ic3.gov/" rel="noopener">FBI Internet Crime Complaint Center</a></li>
        <li><a href="https://oig.hhs.gov/" rel="noopener">HHS Office of Inspector General</a></li>
        <li><a href="https://www.identitytheft.gov/" rel="noopener">IdentityTheft.gov</a>, for the official steps after your information is stolen</li>
        <li><a href="https://cloud.google.com/web-risk" rel="noopener">Google Web Risk</a>, to check links against known harmful sites without opening them</li>
      </ul>
      <p>For questions about your own plan or benefits, we point you to the free official help that can look at your situation: 1‑800‑MEDICARE, your local SHIP counselor, or Social Security.</p>
    </div>
  </div>
</section>

<section class="h-end" aria-label="Get in touch">
  <div class="wrap h-end-grid">
    <div class="h-end-card h-end-soon">
      <p class="h-eyebrow">Get in Touch</p>
      <h2>We’d love to hear from you</h2>
      <p>Questions, ideas, or a story about a scam you spotted? Write to us any time.</p>
      <a class="btn h-btn-light" href="mailto:support@chatretiree.com">{I["mail"]}Email us</a>
    </div>
    <div class="h-end-card">
      <p class="h-eyebrow">Partner with Us</p>
      <h2>For organizations</h2>
      <p>School districts, retiree associations, insurers, credit unions, and community and public groups: let’s talk about helping the people you serve.</p>
      <a class="btn btn-primary" href="mailto:support@chatretiree.com?subject=Partnering%20with%20ChatRetiree">{I["handshake"]}Email us about partnering</a>
    </div>
  </div>
</section>
'''

GETAPP = f'''
<section class="a-hero" aria-labelledby="app-h">
  <div class="wrap">
    <p class="h-eyebrow">Get the App</p>
    <h1 id="app-h"><span class="wm"><b>Chat</b>Retiree</span> is coming to iPhone and Android.</h1>
    <p class="a-lead">We’re trying it with a small group of people first, so we can make it as simple and helpful as possible. It’s not in the app stores yet.</p>
  </div>
</section>

<section class="a-sec" aria-labelledby="stores-h">
  <div class="wrap">
    <h2 id="stores-h" class="sr-only">App stores</h2>
    <div class="store-grid">
      <div class="store"><span class="store-ic">{I["phone"]}</span><div><p class="store-name">App Store</p><p>For iPhone</p></div><span class="store-soon">Coming soon</span></div>
      <div class="store"><span class="store-ic">{I["phone"]}</span><div><p class="store-name">Google Play</p><p>For Android phones</p></div><span class="store-soon">Coming soon</span></div>
    </div>
    <div class="h-end-card h-end-soon notify">
      <p class="h-eyebrow">Be the First to Know</p>
      <h2>Want us to tell you when it’s ready?</h2>
      <p>Send us a quick email and we’ll write back when ChatRetiree is in the app stores. We’ll only use your address for that.</p>
      <a class="btn h-btn-light" href="mailto:support@chatretiree.com?subject=Tell%20me%20when%20the%20ChatRetiree%20app%20is%20ready">{I["mail"]}Email us</a>
    </div>
    <p class="app-more">Until then, you can <a href="../#help">see what the app does</a> with real screens from the app.</p>
  </div>
</section>
'''

CONTACT = f'''
<section class="a-hero" aria-labelledby="contact-h">
  <div class="wrap">
    <p class="h-eyebrow">Contact Us</p>
    <h1 id="contact-h">We’d love to hear from you.</h1>
    <p class="a-lead">Questions, ideas, or something not working? Write to us any time. A real person reads every email.</p>
  </div>
</section>

<section class="a-sec c-sec" aria-label="Ways to reach us">
  <div class="wrap c-grid">
    <div class="c-card c-main">
      <span class="store-ic">{I["mail"]}</span>
      <h2>Email us</h2>
      <p class="c-addr">support@chatretiree.com</p>
      <a class="btn btn-primary" href="mailto:support@chatretiree.com">{I["mail"]}Write an email</a>
    </div>
    <div class="c-card">
      <span class="store-ic">{I["handshake"]}</span>
      <h2>Partnering with us</h2>
      <p>If your organization looks after retirees or older adults and you’d like to work with us, we’d be glad to talk.</p>
      <a class="h-link" href="mailto:support@chatretiree.com?subject=Partnering%20with%20ChatRetiree">Email us about partnering{I["arrow"]}</a>
    </div>
    <div class="c-card">
      <span class="store-ic">{I["info"]}</span>
      <h2>Please don’t send private details</h2>
      <p>There’s no need to include passwords, account numbers, or your Social Security or Medicare number.</p>
    </div>
    <div class="c-card c-urgent">
      <span class="store-ic">{I["warn"]}</span>
      <h2>Need help right now?</h2>
      <p><strong>If someone may be in danger, call 911.</strong></p>
      <p>If you already sent money or gift cards, call your bank or the gift card company right away. You can also report it at <a href="https://reportfraud.ftc.gov/" rel="noopener">ReportFraud.ftc.gov</a>.</p>
    </div>
  </div>
</section>
'''

NOT_FOUND = '''
<div class="page">
  <h1>We couldn’t find that page</h1>
  <p class="lead">It may have moved. Let’s get you back on track.</p>
  <p style="margin-top:28px"><a class="btn btn-primary" href="/">Go to the home page</a></p>
</div>
'''


def privacy_body():
    src = (ROOT / "tools" / "privacy-source.html").read_text(encoding="utf-8")
    inner = re.search(r"<main>(.*)</main>", src, re.S).group(1).strip()
    m = re.match(r"<h1>(.*?)</h1>\s*<p class=\"date\">(.*?)</p>", inner, re.S)
    date = m.group(2)
    inner = inner[m.end():].strip()
    parts = re.split(r"<h2>(.*?)</h2>", inner)[1:]
    secs, toc = [], []
    for i in range(0, len(parts), 2):
        title, body = parts[i], parts[i+1].strip()
        sid = re.sub(r"[^a-z]+", "-", title.lower()).strip("-")
        toc.append(f'<li><a href="#{sid}">{title}</a></li>')
        secs.append(f'<section class="pv-sec" id="{sid}" aria-labelledby="{sid}-h"><h3 id="{sid}-h">{title}</h3>{body}</section>')
    secs.append('<section class="pv-sec" id="this-website" aria-labelledby="this-website-h"><h3 id="this-website-h">About this website</h3><p>This policy is for the ChatRetiree app. This website, chatretiree.com, has no cookies or tracking. It is hosted by GitHub Pages, which keeps short technical logs, such as your internet (IP) address, to keep the site running and secure.</p></section>')
    toc.append('<li><a href="#this-website">About this website</a></li>')
    glance = [
      ("tick", "We don’t keep what you check", "Your messages, pictures, links and questions are looked at, answered, and let go."),
      ("eyeoff", "Private details hidden first", "Before anything leaves your phone, we hide Social Security, Medicare and card numbers, passwords and codes."),
      ("noad", "Never sold", "We never sell your information or use it for advertising."),
      ("link", "We never open your links", "Links are looked up on Google’s list of known dangerous websites. We never open them."),
      ("trusted", "Your trusted people stay with you", "Their names and email addresses stay on your phone and are never sent to us."),
      ("trash", "Leave any time", "You can delete your account in Settings whenever you like."),
    ]
    cards = "".join(f'<div class="pv-card"><span class="pv-ic">{I[ic]}</span><h3>{t}</h3><p>{d}</p></div>' for ic, t, d in glance)
    return f'''
<section class="a-hero" aria-labelledby="privacy-h">
  <div class="wrap">
    <p class="h-eyebrow">Privacy</p>
    <h1 id="privacy-h">Your information stays yours.</h1>
    <p class="a-lead">We built ChatRetiree to protect you, and that includes your privacy. Here’s what that means, in plain words.</p>
  </div>
</section>
<section class="a-sec pv-glance" aria-labelledby="glance-h">
  <div class="wrap">
    <p class="h-eyebrow" id="glance-h">At a Glance</p>
    <div class="pv-grid">{cards}</div>
  </div>
</section>
<section class="a-sec a-tint" aria-labelledby="full-h">
  <div class="wrap pv-full">
    <aside class="pv-toc">
      <h2 id="full-h">The full policy</h2>
      <p class="pv-date">{date}</p>
      <nav aria-label="Privacy policy sections"><ol>{"".join(toc)}</ol></nav>
    </aside>
    <div class="pv-body">{"".join(secs)}</div>
  </div>
</section>'''

page("examples/check", "Example: check a message", "Tap through samples of ChatRetiree checking a message.",
     ex_page("check", "Check a message that feels off", "Paste a text or email, add a picture of your screen, or just tell us what happened. Here’s what ChatRetiree says back.", "Pick an example to try", CHECK_EX, "check"))
page("examples/medicare", "Example: Medicare questions", "Tap through sample Medicare questions and ChatRetiree’s answers from the official guides.",
     ex_page("medicare", "Medicare questions", "Ask in your own words. Answers come only from official Medicare guides, explained in plain language.", "Pick a question to try", MEDICARE_EX, "medicare"))
page("examples/scams", "Example: scams going around", "Tap through questions about scams, answered from official FTC, FBI and HHS alerts.",
     ex_page("scams", "Scams going around", "We keep up with official scam warnings from the FTC, the FBI and the U.S. Department of Health and Human Services, and put them in plain words. You can also ask about a scam.", "Pick a question to try", SCAM_EX, "scams"))
page("examples/trusted", "Example: ask someone you trust", "See how ChatRetiree helps you send what you found to someone you trust.",
     ex_page("trusted", "Ask someone you trust", "Add a family member or friend in the app. After any check, one tap opens your own email with a note to them, so you can decide together.", "Try it", TRUSTED_EX, "trusted"))
page("", "ChatRetiree: always home, always here to help",
     "ChatRetiree is like a friend you can ask when a text, email or call doesn’t feel right. Coming soon to iPhone and Android.", HOME)
page("privacy", "Privacy policy", "How the ChatRetiree app handles your information.", privacy_body(), "privacy")
page("about", "About us", "Why we built ChatRetiree, what we believe, and where our answers come from.", ABOUT, "about")
page("app", "Get the app", "ChatRetiree is coming soon to iPhone and Android.", GETAPP, "app")
page("contact", "Contact us", "Questions or ideas? Email support@chatretiree.com.", CONTACT, "contact")
page("404", "Page not found", "We couldn’t find that page.", NOT_FOUND)
print("built")
