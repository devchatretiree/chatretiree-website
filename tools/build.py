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
  "moon": '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>',
  "sun": '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
}

def page(path, title, description, body, current=""):
    depth = 0 if path in ("", "404") else path.count("/") + 1
    up = "../" * depth
    def nav(href, label, key, cls=""):
        cur = ' aria-current="page"' if key == current else ""
        c = f' class="{cls}"' if cls else ""
        return f'<a href="{up}{href}"{cur}{c}>{label}</a>'
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
        html = html.replace(f'href="{up}', 'href="/').replace('href="./"', 'href="/"').replace(f'src="{up}', 'src="/')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

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
    <article class="card">
      <div class="icon t-teal">{I["check"]}</div>
      <h3>Check a message that feels off</h3>
      <p>Paste a text or email, type in a web address, or add a picture of your screen. We’ll tell you what we noticed and what to do next.</p>
    </article>
    <article class="card">
      <div class="icon t-blue">{I["medicare"]}</div>
      <h3>Medicare questions</h3>
      <p>Ask in your own words. Answers come only from official Medicare guides, and we show you where each one comes from.</p>
    </article>
    <article class="card">
      <div class="icon t-clay">{I["alerts"]}</div>
      <h3>Scams going around</h3>
      <p>Short, plain summaries of the latest scam warnings from the FTC, the FBI and the U.S. Department of Health and Human Services.</p>
    </article>
    <article class="card">
      <div class="icon t-sage">{I["trusted"]}</div>
      <h3>Ask someone you trust</h3>
      <p>Want a second opinion? Send what we found to a family member or friend from your own email.</p>
    </article>
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

page("", "ChatRetiree: let’s look at it together",
     "ChatRetiree is like a friend you can ask when a text, email or call doesn’t feel right. Coming soon to iPhone and Android.", HOME)
page("privacy", "Privacy policy", "How the ChatRetiree app handles your information.", privacy_body(), "privacy")
page("contact", "Contact us", "Questions or ideas? Email support@chatretiree.com.", CONTACT, "contact")
page("404", "Page not found", "We couldn’t find that page.", NOT_FOUND)
print("built")
