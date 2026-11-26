# chatretiree.com

The public website for ChatRetiree: home, privacy policy and contact pages. Plain HTML and CSS, no build tools, no trackers, no requests to other sites.

- Hosted free on GitHub Pages from the `main` branch (Settings → Pages → Deploy from a branch → main, / (root)).
- Pages are generated from `tools/build.py` (shared header and footer). After editing it, run `python3 tools/build.py` and commit the generated `.html` files.
- `privacy/` comes from `tools/privacy-source.html`, the web copy of the app's policy. The app's `src/content/legal.ts` (chatretiree-app repo) is the master: when it changes, update the source file and the "Last updated" date, then rebuild.
- Don't link the app's invite-only beta, and don't add app store badges until the apps are live.
- Custom domain: a `CNAME` file with `chatretiree.com` is added only when the GoDaddy website records are switched. Never change the MX records (Google Workspace email) or anything under `send.` (Resend).
- Fonts: Atkinson Hyperlegible and Plus Jakarta Sans, self-hosted under the SIL Open Font License (see `assets/fonts/`).
