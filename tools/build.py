"""Builds the site's pages from one shared header and footer.
The finished .html files are committed, so the site needs no build step to be hosted.
Run: python3 tools/build.py  (from the repository folder)"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

def ico(body, fill=False):
    if fill:
        return f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">{body}</svg>'
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>')

LOGO = ('<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false"><rect width="100" height="100" rx="24" fill="#0F5F5A"/>'
        '<path d="M40 18a23 23 0 1 1-10.6 43.4L18 66l3.4-11.2A23 23 0 0 1 40 18z" fill="#FFFFFF"/>'
        '<path d="M63 41a19 19 0 1 0 8.8 35.8L81 80.5l-2.8-9.3A19 19 0 0 0 63 41z" fill="#0F5F5A" stroke="#0F5F5A" stroke-width="11" stroke-linejoin="round"/>'
        '<path d="M63 41a19 19 0 1 0 8.8 35.8L81 80.5l-2.8-9.3A19 19 0 0 0 63 41z" fill="#0F5F5A" stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round"/></svg>')

I = {
  "check": ico('<path d="M12 3a8.5 8.5 0 1 1-4.2 15.9L3.5 20.5l1.4-4.1A8.5 8.5 0 0 1 12 3z"/><path d="M9.8 9.6a2.3 2.3 0 1 1 3.2 2.1c-.7.3-1 .8-1 1.5v.3"/><path d="M12 16.3h.01"/>'),
  "medicare": ico('<path d="M12 3a8.5 8.5 0 1 1-4.2 15.9L3.5 20.5l1.4-4.1A8.5 8.5 0 0 1 12 3z"/><path d="M12 15.2s-3.6-2.1-3.6-4.6a1.9 1.9 0 0 1 3.6-.9 1.9 1.9 0 0 1 3.6.9c0 2.5-3.6 4.6-3.6 4.6z"/>'),
  "alerts": ico('<path fill-rule="evenodd" d="M12 2.6c4.5 0 7.8 3.3 7.8 8v3.8c0 4-3.5 6.9-7.8 6.9s-7.8-2.9-7.8-6.9v-3.8c0-4.7 3.3-8 7.8-8z M7.4 8.4h9.2a2.1 2.1 0 0 1 0 4.2H7.4a2.1 2.1 0 0 1 0-4.2z M12 14.8c1.6 0 2.7.8 2.7 1.8s-1.1 1.8-2.7 1.8-2.7-.8-2.7-1.8 1.1-1.8 2.7-1.8z"/><circle cx="9" cy="10.5" r="1.2"/><circle cx="15" cy="10.5" r="1.2"/>', fill=True),
  "trusted": ico('<circle cx="9" cy="8" r="3"/><path d="M3.5 19.5a5.5 5.5 0 0 1 11 0"/><circle cx="16.5" cy="9" r="2.5"/><path d="M15.5 14.2a4.5 4.5 0 0 1 5.5 4.3"/>'),
  "tick": ico('<circle cx="12" cy="12" r="9.5"/><path d="m8 12.5 2.8 2.8L16.5 9.5"/>'),
  "mail": ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>'),
  "phone": ico('<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18.5h2"/>'),
  "heart": ico('<path d="M12 20s-7.5-4.4-7.5-10A4.2 4.2 0 0 1 12 7.6 4.2 4.2 0 0 1 19.5 10c0 5.6-7.5 10-7.5 10z"/>'),
  "arrow": ico('<path d="M5 12h14M13 6l6 6-6 6"/>'),
  "back": ico('<path d="M19 12H5M11 6l-6 6 6 6"/>'),
  "info": ico('<circle cx="12" cy="12" r="9.5"/><path d="M12 11v5M12 7.5h.01"/>'),
  "warn": ico('<path d="M10.3 3.9 2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>'),
  "question": ico('<circle cx="12" cy="12" r="9.5"/><path d="M9.6 9.4a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1.1.9-1.1 1.6v.3"/><path d="M12 16.8h.01"/>'),
  "handshake": ico('<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2l-3.9-3.9a2 2 0 0 0-2.8 0l-.9.9a1.4 1.4 0 0 1-2-2l2.8-2.8a3.5 3.5 0 0 1 4.3-.5l.6.4a2 2 0 0 0 1.4.3L21 6.5"/><path d="m21 5.5 1 9-2 1"/><path d="M3 5.5l-1 9 6.5 6.5a1.4 1.4 0 0 0 2-2"/><path d="M3 6.5h7"/>'),
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
    extra_head = f'<script src="{up}assets/examples.js"></script>' if path.startswith("examples/") else ""
    full_title = title if title.startswith("ChatRetiree") else f"{title} · ChatRetiree"
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#FAF7F2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121718" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://chatretiree.com/assets/icon.png">
<link rel="icon" href="{up}assets/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{up}assets/icon.png">
<link rel="stylesheet" href="{up}assets/site.css">
<script src="{up}assets/site.js"></script>
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header class="top"><div class="wrap">
  <a class="brand" href="{up or './'}" aria-label="ChatRetiree home">{LOGO}<span><b>Chat</b>Retiree</span></a>
  <nav class="nav" aria-label="Main">
    {nav("privacy/", "Privacy", "privacy", "hide-sm")}
    {nav("contact/", "Contact", "contact", "hide-sm")}
    <button class="theme" type="button" hidden aria-label="Switch to dark" aria-pressed="false">{I["moon"]}{I["sun"]}</button>
  </nav>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
  <div>
    <a class="brand" href="{up or './'}" aria-label="ChatRetiree home">{LOGO}<span><b>Chat</b>Retiree</span></a>
    <p class="tag">Let’s look at it together.</p>
  </div>
  <nav aria-label="Footer">
    {nav("privacy/", "Privacy policy", "privacy")}
    <a href="{up}#partner">Partner with us</a>
    {nav("contact/", "Contact us", "contact")}
  </nav>
  <small>© 2026 ChatRetiree. This website has no ads, no cookies and no tracking.</small>
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

NOTE = f'<p class="ex-note">{I["info"]}<span>These are samples you can tap through, with the answers ChatRetiree gives. To check your own messages, you’ll use the app.</span></p>'

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
    <h2>See more of what ChatRetiree can do</h2>
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

CHECK_EX = [
  example("package", "A text about a package", "You paste a text you got",
    '<p class="in-bubble">PARCEL NOTICE: Your package is on hold due to an unpaid $1.99 redelivery fee. Pay now to avoid return to sender: parcel-redelivery.example/pay?id=88213</p>',
    "Check it",
    verdict("strong", "This message has several signs that are common in scams.")
    + panel(WHATS_NEXT, ul(["Don’t reply, click links or pay. Contact the company using a phone number or website you already trust."], "ol"))
    + panel(WHY, ul(["It asks for a small fee. Fake delivery notices do this to collect card details.",
                     "It warns that something bad will happen to your account, benefits or device.",
                     "It pushes you to act right away, before you have time to check."]))),
  example("bank", "A picture of a bank text", "You add a picture of your screen",
    '<div class="shot" role="img" aria-label="A picture of a phone screen showing a text from First Harbor Bank">'
    '<div class="shot-screen"><p class="shot-from"><b>First Harbor Bank</b>Text Message · Today 9:14 AM</p>'
    '<p class="shot-msg">FIRST HARBOR BANK ALERT: Your account has been compromised. To protect your savings you must move your funds TODAY to a new safe account. A specialist will call you shortly. Do not tell branch staff, they may be involved. Reply YES to begin.</p></div></div>'
    '<p class="read-note">ChatRetiree reads the words in your picture right on your phone. You see them first, then we look.</p>',
    "Check it",
    verdict("strong", "This message has several signs that are common in scams.")
    + panel(WHATS_NEXT, ul(["Don’t reply or move any money. Call your bank using the number on the back of your card or on your statement."], "ol"))
    + panel(WHY, ul(["It asks you to move money to a so-called “safe account.” Real banks never ask you to do this.",
                     "It tells you to keep it secret. Scammers do this so no one can warn you.",
                     "It warns that something bad will happen to your account, benefits or device."]))),
  example("call", "A worrying phone call", "You tell us what happened",
    '<p class="in-bubble">A young man called crying and said he was my grandson. He said he was in jail after a car accident and needed $3,000 for bail. A lawyer then got on and said to pay with gift cards from the drugstore and not to tell his parents.</p>',
    "Check it",
    verdict("strong", "This situation has several signs that are common in scams.")
    + panel("If you’re worried someone you love is in trouble", ul([
        "If someone may be in danger right now, call 911.",
        "Hang up or stop replying. Then call your family member yourself, using a number you already have. If you can’t reach them, call another relative or a friend who would know.",
        "Don’t send any money, gift cards or cryptocurrency, not even part of what they ask for.",
        "To report it, contact your local police."], "ol"), "urgent")
    + '<p class="call911">If someone may be in danger, call 911.</p>'
    + panel(WHATS_NEXT, ul(["Don’t send money. Hang up and call your family member, or another relative, on a number you already have."], "ol"))
    + panel(WHY, ul(["It asks for payment with gift cards. Only scammers ask to be paid this way.",
                     "It tells you to keep it secret. Scammers do this so no one can warn you.",
                     "It describes a family emergency that needs money fast. This is a common way to cause panic."]))),
  example("doctor", "A message from a doctor’s office", "You paste a text you got",
    '<p class="in-bubble">Hi, this is Dr. Patel’s office calling about your recent test results. Please call us back when you get a chance.</p>',
    "Check it",
    verdict("verify", "Nothing proves this message is a scam, but some things need checking before you respond.")
    + panel(WHATS_NEXT, ul(["Before you respond, contact them yourself using a phone number or website you already have, not one from the message."], "ol"))
    + panel(WHY, ul(["It asks you to respond, but doesn’t say anything we can check. Scammers sometimes start this way too."]))
    + '<p class="cite">We never call something “safe.” When we can’t tell, we say so and help you check.</p>'),
]

MEDICARE_EX = [
  example("dental", "Does Medicare cover dental?", "You ask",
    '<p class="in-bubble question">Does Original Medicare cover dental care?</p>', "Ask",
    reply(ul(["In most cases, Original Medicare does not cover routine dental services like cleanings, fillings, tooth extractions, or dentures.",
              "Original Medicare may pay for dental services if they are closely related to certain covered medical procedures, such as cancer treatments, organ transplants, heart valve repairs, or dialysis for End-Stage Renal Disease."]))
    + '<p class="cite">From the official Medicare guides. In the app, “More detail and sources” shows the guide’s exact words.</p>',
    "Looking in the official guides…"),
  example("hearing", "Hearing aids", "You ask",
    '<p class="in-bubble question">Does Medicare pay for hearing aids?</p>', "Ask",
    reply('<p><strong>Short answer:</strong> Original Medicare does not cover hearing aids or exams for fitting them. Some Medicare Advantage Plans may offer coverage for hearing services that Original Medicare does not.</p>'
          + ul(["Original Medicare does not cover hearing aids or exams for fitting them, and you must pay all costs for these services.",
                "Medicare Advantage Plans are private plans that may offer extra benefits, such as some hearing services, that Original Medicare does not cover."]))
    + '<p class="cite">From the official Medicare guides. In the app, “More detail and sources” shows the guide’s exact words.</p>',
    "Looking in the official guides…"),
  example("signup", "When to sign up", "You ask",
    '<p class="in-bubble question">When can I sign up for Medicare?</p>', "Ask",
    reply(ul(["Your Initial Enrollment Period is a 7-month window that starts 3 months before the month you turn 65, includes your birthday month, and ends 3 months after.",
              "A Special Enrollment Period may be available if you did not sign up when first eligible because you had group health plan coverage based on current employment."]))
    + '<p class="cite">From the official Medicare guides. For questions about your own situation, we point you to 1-800-MEDICARE or your free local SHIP counselor.</p>',
    "Looking in the official guides…"),
]

SCAM_EX = [
  example("giftcards", "Why gift cards?", "You ask",
    '<p class="in-bubble question">Why do scammers ask for gift cards?</p>', "Ask",
    reply('<p>Scammers prefer gift cards because it is almost impossible to get your money back once they have collected it. Scammers want you to panic and send money quickly, before you have time to think or talk to someone you trust.</p>')
    + '<p class="cite">From official alerts by the FTC (November 2026). In the app, you can see the alert’s exact words and open the alert.</p>',
    "Looking through official alerts…"),
  example("bail", "A grandchild needs bail", "You ask",
    '<p class="in-bubble question">Someone says my grandson is in jail and needs bail money. What do I do?</p>', "Ask",
    reply('<p>If you get a call from someone claiming to be a family member in trouble, slow down and hang up the phone. Then call another family member or friend to check whether the story is true.</p>')
    + '<p class="cite">From an official FTC alert (November 2026).</p>',
    "Looking through official alerts…"),
  example("medicarescam", "Medicare scams", "You ask",
    '<p class="in-bubble question">What are scammers doing with Medicare?</p>', "Ask",
    reply('<p>Scammers target people on Medicare by enrolling them in hospice care they don’t need, or by billing for services that were never provided.</p>')
    + '<p class="cite">From an official FBI alert.</p>',
    "Looking through official alerts…"),
  example("haggle", "Paying them a little less", "You ask",
    '<p class="in-bubble question">Should I offer the scammer a smaller amount so they leave me alone?</p>', "Ask",
    reply('<p>The official alerts don’t cover this yet.</p>')
    + '<p class="cite">When the official alerts don’t answer a question, we say so instead of guessing. And we’ll never suggest paying a scammer anything.</p>',
    "Looking through official alerts…"),
]

TRUSTED_EMAIL = ("Hi Sarah, can you look at this with me before I do anything?\n\n"
  "ChatRetiree said: This has the signs of a scam.\nThis message has several signs that are common in scams.\n\n"
  "Here’s what I got:\n“PARCEL NOTICE: Your package is on hold due to an unpaid $1.99 redelivery fee. Pay now to avoid return to sender: hxxps://parcel-redelivery[.]example/pay?id=88213”\n\n"
  "(Links are broken on purpose so nobody taps them by accident.)")

TRUSTED_EX = [
  example("sarah", "Ask Sarah about a text", "After a check, you tap",
    '<p class="in-bubble">PARCEL NOTICE: Your package is on hold due to an unpaid $1.99 redelivery fee…</p>'
    + '<div style="margin-top:16px">' + verdict("strong", "This message has several signs that are common in scams.") + '</div>',
    f'{I["mail"]}Email Sarah',
    f'<p>Your own email app opens with this note. You can read it and change it. Nothing is sent until you press send.</p>'
    f'<div class="email"><div class="hdr"><div><strong>To:</strong> Sarah</div><div><strong>Subject:</strong> Can you look at this with me?</div></div>'
    f'<div class="body">{TRUSTED_EMAIL}</div></div>'
    '<p class="cite">The people you trust are kept only on your phone. Their names and email addresses are never sent to us.</p>',
    "Opening your email app…"),
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
<div class="hero"><div class="wrap">
  <div>
    <p class="pill">{I["phone"]}Coming soon to iPhone and Android</p>
    <h1>Let’s look at it together.</h1>
    <p class="lead">Got a text, email or call that doesn’t feel right? ChatRetiree is like a friend you can ask. Show us what you got, and we’ll talk it over with you in plain words, with clear next steps.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="#how">See how it works</a>
      <a class="btn btn-quiet" href="contact/">{I["mail"]}Contact us</a>
    </div>
  </div>
  <figure class="talk" aria-label="An example of talking it over with ChatRetiree">
    <figcaption class="talk-label">For example</figcaption>
    <p class="bubble me">I got a text saying my package is on hold and I owe $1.99. Is this real?</p>
    <div class="bubble us">
      <p class="who">{LOGO}ChatRetiree</p>
      <p>Let’s look at it together. This looks a lot like a common package scam. Here’s what I’d do:</p>
      <ol>
        <li>Don’t tap the link or reply.</li>
        <li>If you’re expecting a delivery, open the shipper’s own app or website yourself.</li>
      </ol>
    </div>
  </figure>
</div></div>

<section class="band" aria-labelledby="help-h"><div class="wrap">
  <div class="section-head">
    <h2 id="help-h">How we can help</h2>
    <p>One place to go when something feels off, or when you just have a question.</p>
  </div>
  <div class="cards">
    <a class="card" href="examples/check/">
      <div class="icon t-teal">{I["check"]}</div>
      <h3>Check a message that feels off</h3>
      <p>Paste a text or email, type in a web address, or add a picture of your screen. We’ll tell you what we noticed and what to do next.</p>
      <span class="more">See an example{I["arrow"]}</span>
    </a>
    <a class="card" href="examples/medicare/">
      <div class="icon t-blue">{I["medicare"]}</div>
      <h3>Medicare questions</h3>
      <p>Ask in your own words. Answers come only from official Medicare guides, and we show you where each one comes from.</p>
      <span class="more">See an example{I["arrow"]}</span>
    </a>
    <a class="card" href="examples/scams/">
      <div class="icon t-clay">{I["alerts"]}</div>
      <h3>Scams going around</h3>
      <p>Short, plain summaries of the latest scam warnings from the FTC, the FBI and the U.S. Department of Health and Human Services.</p>
      <span class="more">See an example{I["arrow"]}</span>
    </a>
    <a class="card" href="examples/trusted/">
      <div class="icon t-sage">{I["trusted"]}</div>
      <h3>Ask someone you trust</h3>
      <p>Want a second opinion? Send what we found to a family member or friend from your own email.</p>
      <span class="more">See an example{I["arrow"]}</span>
    </a>
  </div>
</div></section>

<section id="how" aria-labelledby="how-h"><div class="wrap">
  <div class="section-head">
    <h2 id="how-h">How it works</h2>
    <p>No forms and no jargon. Just a few taps.</p>
  </div>
  <ol class="steps">
    <li><h3>Copy it</h3><p>Copy the text or email that worries you, or take a picture of your screen.</p></li>
    <li><h3>Paste it in</h3><p>Open ChatRetiree and tap “Paste and check.” That’s it.</p></li>
    <li><h3>Talk it over</h3><p>We’ll show you the warning signs we found, in plain words, and what you can do next.</p></li>
  </ol>
</div></section>

<section class="band" aria-labelledby="privacy-h"><div class="wrap split">
  <div>
    <h2 id="privacy-h">Your privacy comes first</h2>
    <ul class="checks">
      <li>{I["tick"]}<span>We don’t keep your messages, pictures, links or questions.</span></li>
      <li>{I["tick"]}<span>Before anything leaves your phone, we hide things like Social Security, Medicare and card numbers.</span></li>
      <li>{I["tick"]}<span>We never sell your information or use it for ads.</span></li>
    </ul>
    <p><a href="privacy/">Read our privacy policy</a></p>
  </div>
  <div class="help" role="note" aria-labelledby="sent-h">
    <h3 id="sent-h">{I["heart"]}Think you’ve been scammed?</h3>
    <p>You’re not alone, and it’s not your fault.</p>
    <p><strong>If someone may be in danger, call 911.</strong></p>
    <p>If you already sent money or gift cards, call your bank or the gift card company right away.</p>
    <p>You can also report it to the FTC at <a href="https://reportfraud.ftc.gov/" rel="noopener">ReportFraud.ftc.gov</a>.</p>
  </div>
</div></section>

{PARTNER}
<section aria-labelledby="soon-h"><div class="wrap">
  <div class="cta">
    <h2 id="soon-h">Coming soon</h2>
    <p>We’re trying ChatRetiree with a small group of people first. It’s coming to iPhone and Android. Have a question in the meantime? We’d love to hear from you.</p>
    <a class="btn" href="mailto:support@chatretiree.com">{I["mail"]}Email us</a>
  </div>
</div></section>
'''

CONTACT = f'''
<div class="page">
  <h1>Contact us</h1>
  <p class="lead">Questions, ideas, or something not working? We’d love to hear from you.</p>
  <div class="contact-card">
    <p>Email us at</p>
    <p class="email"><a href="mailto:support@chatretiree.com">support@chatretiree.com</a></p>
    <a class="btn btn-primary" href="mailto:support@chatretiree.com">{I["mail"]}Write an email</a>
  </div>
  <div class="note">
    <h2>Partnering with us</h2>
    <p>If your organization looks after retirees or older adults and you’d like to work with us, <a href="mailto:support@chatretiree.com?subject=Partnering%20with%20ChatRetiree">email us about partnering</a>.</p>
  </div>
  <div class="note">
    <h2>Please don’t send us private details</h2>
    <p>There’s no need to include passwords, account numbers, or your Social Security or Medicare number. We’ll never ask you for them.</p>
  </div>
  <div class="note">
    <h2>Need help right now?</h2>
    <p><strong>If someone may be in danger, call 911.</strong> If you already sent money or gift cards, call your bank or the gift card company right away.</p>
  </div>
</div>
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
    note = '''
<div class="note">
  <h2>About this website</h2>
  <p>This policy is for the ChatRetiree app. This website, chatretiree.com, has no ads, cookies or tracking. It is hosted by GitHub Pages, which keeps short technical logs, such as your internet (IP) address, to keep the site running and secure.</p>
</div>'''
    return f'<div class="page">\n{inner}\n{note}\n</div>'

page("examples/check", "Example: check a message", "Tap through samples of ChatRetiree checking a message.",
     ex_page("check", "Check a message that feels off", "Paste a text or email, add a picture of your screen, or just tell us what happened. Here’s what ChatRetiree says back.", "Pick an example to try", CHECK_EX, "check"))
page("examples/medicare", "Example: Medicare questions", "Tap through sample Medicare questions and ChatRetiree’s answers from the official guides.",
     ex_page("medicare", "Medicare questions", "Ask in your own words. Answers come only from official Medicare guides, explained in plain language.", "Pick a question to try", MEDICARE_EX, "medicare"))
page("examples/scams", "Example: scams going around", "Tap through questions about scams, answered from official FTC, FBI and HHS alerts.",
     ex_page("scams", "Scams going around", "We keep up with official scam warnings from the FTC, the FBI and the U.S. Department of Health and Human Services, and put them in plain words. You can also ask about a scam.", "Pick a question to try", SCAM_EX, "scams"))
page("examples/trusted", "Example: ask someone you trust", "See how ChatRetiree helps you send what you found to someone you trust.",
     ex_page("trusted", "Ask someone you trust", "Add a family member or friend in the app. After any check, one tap opens your own email with a note to them, so you can decide together.", "Try it", TRUSTED_EX, "trusted"))
page("", "ChatRetiree: let’s look at it together",
     "ChatRetiree is like a friend you can ask when a text, email or call doesn’t feel right. Coming soon to iPhone and Android.", HOME)
page("privacy", "Privacy policy", "How the ChatRetiree app handles your information.", privacy_body(), "privacy")
page("contact", "Contact us", "Questions or ideas? Email support@chatretiree.com.", CONTACT, "contact")
page("404", "Page not found", "We couldn’t find that page.", NOT_FOUND)
print("built")
